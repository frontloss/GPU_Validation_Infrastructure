##
# @file         display_clock.py
# @brief        Python Wrapper that exposes the interface for Displays Clock Validation
# @details      Checks for the platform and calls the respective platform implementation
# @author       rradhakr, Doriwala Nainesh P


import logging
from typing import List

from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.machine_info.machine_info import GEN_14_PLATFORMS, GEN_15_PLATFORMS, GEN_16_PLATFORMS
from Libs.Feature.clock import clock_helper
from Libs.Feature.clock.clock_helper import GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ, PTL_EFFECTIVE_CD_CLOCK_MHZ, NVL_EFFECTIVE_CD_CLOCK_MHZ


##
# @brief Clock verification class for CDCLK and port CLK
class DisplayClock:
    display_list = list()
    display_and_adapter_info_list = []
    platform = None
    # Please use this common variable for future platform to get benefit for divider and pll verification.
    clk = None

    ##
    # @brief Checks for the platform and calls the correct implementation to verify clock
    # @param[in] display_port -  Display Type and Port details of the display
    # @param[in] gfx_index - Graphics Index to which verify clock
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        # call get_gfx_display_hardwareinfo() to get the platform type from system_info
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

        # clock_object = getattr(importlib.import_module(
        #     'Libs.clock.' + str(self.platform).lower() + '.' + str(self.platform).lower() + '_clock_base'),
        #                        str(self.platform).lower().title() + 'Clock')
        # clock_object.verify_clock(display_port)
        if self.platform == 'TGL':
            from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
            clock = TglClock()
            return clock.verify_clock(display_port, gfx_index)
        elif self.platform == 'RKL':
            return self.clk.verify_clock(display_port, gfx_index)
        elif self.platform == 'ADLS':
            from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
            clock = AdlsClock()
            return clock.verify_clock(display_port, gfx_index)
        elif self.platform == 'DG1':
            from Libs.Feature.clock.dg1.dg1_clock_base import Dg1Clock
            clock = Dg1Clock()
            return clock.verify_clock(display_port, gfx_index)
        elif self.platform == 'DG2':
            return self.clk.verify_clock(display_port, gfx_index)
        elif self.platform == "ADLP":
            return self.clk.verify_clock(display_port, gfx_index)
        elif self.platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
            return MtlClock.verify_clock(display_port, gfx_index)
        elif self.platform == "ELG":
            return self.clk.verify_clock(display_port, gfx_index)
        elif self.platform in ["LNL", "PTL", "NVL"]:
            from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
            clock = LnlClock()
            # Todo: Add actual port clock verification steps for LNL/PTL
            return clock.verify_clock(gfx_index, display_port)
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]Clock verification is not Supported for platform: {}".format(
                    self.platform),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Platform Not Supported: %s" % self.platform)
            return False

    ##
    # @brief Checks for the platform and calls the correct implementation for clocks verification
    # @param[in] gfx_index - Graphics Index to which verify clocks
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clocks(self, gfx_index='gfx_0'):
        # call get_gfx_display_hardwareinfo() to get the platform type from system_info
        config = display_config.DisplayConfiguration()
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        gfx_index_list = []
        display_list_per_adapter = []
        topology, self.display_list, self.display_and_adapter_info_list = config.get_current_display_configuration_ex()
        logging.info('Current Display Config: Topology: %s Displays List = %s' %
                     (topology, self.display_list))
        # Extracting adapter wise display list dictionary form display list and adapter list of display and adapter info
        for each_display_and_adapter_info in self.display_and_adapter_info_list:
            gfx_index_list.append(each_display_and_adapter_info.adapterInfo.gfxIndex)
        gfx_index_list = map(str, gfx_index_list)
        gfx_display_dict = DisplayClock.get_gfx_display_dict(self.display_list, gfx_index_list)
        # clock_object = getattr(importlib.import_module(
        #     'Libs.clock.' + str(self.platform).lower() + '.' + str(self.platform).lower() + '_clock_base'),
        #                        str(self.platform).lower().title() + 'Clock')
        # clock_object.verify_clock(display_port)
        verify = True

        # For requested adapter, getting display list from gfx_display_dict dictionary
        for key, value in gfx_display_dict.items():
            logging.info("Gfx_index as key of gfx_display_dict is:{} and display port as value is: {}"
                         .format(key, value))
            if str(key) == gfx_index.lower():
                display_list_per_adapter = value

        for i in range(len(display_list_per_adapter)):
            if display_list_per_adapter[i].startswith("WD_"):
                display_list_per_adapter.remove(display_list_per_adapter[i])

        if len(display_list_per_adapter) == 0:
            return verify
        verify &= self.verify_cdclock(display_list_per_adapter, gfx_index)

        for display_port in display_list_per_adapter:
            verify &= self.verify_clock(display_port, gfx_index)

        return verify

    ##
    # @brief Checks for the platform and calls the correct implementation for CD clocks verification
    # @param[in] display_list_per_adapter - List of display per graphics adapter
    # @param[in] gfx_index - Graphics Index to which verify clocks
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_cdclock(self, display_list_per_adapter, gfx_index='gfx_0'):

        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

        # clock_object = getattr(importlib.import_module(
        #     'Libs.clock.' + str(self.platform).lower() + '.' + str(self.platform).lower() + '_clock_base'),
        #                        str(self.platform).lower().title() + 'Clock')
        # clock_object.verify_clock(display_port)

        if self.platform == 'TGL':
            from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
            clock = TglClock()
            return clock.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == 'RKL':
            from Libs.Feature.clock.rkl.rkl_clock_base import RklClock
            self.clk = RklClock()
            return self.clk.verify_cdclock(self.display_list, gfx_index)
        elif self.platform == 'ADLS':
            from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
            clock = AdlsClock()
            return clock.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == 'DG1':
            from Libs.Feature.clock.dg1.dg1_clock_base import Dg1Clock
            clock = Dg1Clock()
            return clock.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == 'DG2':
            from Libs.Feature.clock.dg2.dg2_clock_base import Dg2Clock
            self.clk = Dg2Clock()
            return self.clk.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == "ADLP":
            from Libs.Feature.clock.adlp.adlp_clock_base import AdlpClock
            self.clk = AdlpClock()
            return self.clk.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
            self.clk = MtlClock()
            return self.clk.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == "ELG":
            from Libs.Feature.clock.elg.elg_clock_base import ElgClock
            self.clk = ElgClock()
            return self.clk.verify_cdclock(display_list_per_adapter, gfx_index)
        elif self.platform == 'LNL':
            from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
            clock = LnlClock()
            return clock.verify_cdclock(gfx_index, display_list_per_adapter)
        elif self.platform == 'PTL':
            from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
            clock = PtlClock()
            return clock.verify_cdclock(gfx_index, display_list_per_adapter)
        elif self.platform == 'NVL':
            logging.info("Currently CD Clock verification is skipped of NVL Auto 2.0 test - DCN Implementation "
                         "planned in "
                         "Auto 3.0")
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine] CD Clock verification is not Supported for platform: {}".format(
                    self.platform),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Platform Not Supported: %s" % self.platform)
            return False

    ##
    # @brief        Checks for the platform and calls the correct implementation for calculating symbol frequency
    # @param[in]    display_port - Display port
    # @param[in]    gfx_index - Graphics Index to which verify clocks
    # @return       BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def calculate_symbol_freq(self, display_port, gfx_index='gfx_0'):
        # call get_gfx_display_hardwareinfo() to get the platform type from system_info
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

        if self.platform == 'TGL':
            from Libs.Feature.clock.tgl.tgl_clock_hdmi import TglClockHdmi
            clock = TglClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == 'RKL':
            from Libs.Feature.clock.rkl.rkl_clock_hdmi import RklClockHdmi
            clock = RklClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == 'ADLS':
            from Libs.Feature.clock.adls.adls_clock_hdmi import AdlsClockHdmi
            clock = AdlsClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == 'DG1':
            from Libs.Feature.clock.dg1.dg1_clock_hdmi import Dg1ClockHdmi
            clock = Dg1ClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == 'DG2':
            from Libs.Feature.clock.dg2.dg2_clock_hdmi import Dg2ClockHdmi
            clock = Dg2ClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == "ADLP":
            from Libs.Feature.clock.adlp.adlp_clock_hdmi import AdlpClockHdmi
            clock = AdlpClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_hdmi import MtlClockHdmi
            clock = MtlClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform in ["ELG", "CLS"]:
            from Libs.Feature.clock.elg.elg_clock_hdmi import ElgClockHdmi
            clock = ElgClockHdmi()
            return clock.calculate_symbol_freq(display_port, gfx_index)
        elif self.platform in ["LNL", "PTL", "NVL"]:
            from Libs.Feature.clock.lnl.lnl_clock_hdmi import LnlClockHdmi
            clock = LnlClockHdmi()
            return clock.calculate_symbol_freq(gfx_index, display_port)
        else:
            logging.error("Platform Not Supported: %s" % self.platform)
            return False

    ##
    # @brief        Verifies PCode notified Voltage Level as part of CD clock programming
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    ports - Active Ports list
    # @return       bool - Returns True if verification is successful, False otherwise
    @classmethod
    def verify_voltage_level_notified_to_pcode(cls, gfx_index: str, ports: List[str]) -> bool:
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

        if platform not in GEN_14_PLATFORMS + GEN_15_PLATFORMS + GEN_16_PLATFORMS + ['NVL']:
            gdhm.report_bug(
                title=f"[Interfaces][Display_Engine][CD Clock] DVFS VoltageLevel verification not Supported for"
                      f" {platform}",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f"Platform not supported for DVFS VoltageLevel verification : {platform}")
            return False

        if platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
            clock = MtlClock()
        elif platform == "ELG":
            from Libs.Feature.clock.elg.elg_clock_base import ElgClock
            clock = ElgClock()
        elif platform == "LNL":
            from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
            clock = LnlClock()
        elif platform == "NVL":
            logging.info("Skipping DVFS verification for  NVL Auto 2.0 test - DCN implementation planned in Auto 3.0")
            return True
        else:
            # Assuming max supported platform
            from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
            clock = PtlClock()

        return clock.verify_voltage_level_notified_to_pcode(gfx_index, ports)

    ##
    # @brief generate dictionary containing key as gfx adapter and value as displays attached to respective gfx adapter.
    # @param[in] display_list - List of Display
    # @param[in] gfx_index_list - List of Graphics adapter
    # @return dictionary - with key as gfx adapter and value as displays attached to respective adapter
    @staticmethod
    def get_gfx_display_dict(display_list, gfx_index_list):
        gfx_display_dict = {k: v for k, v in zip(display_list, gfx_index_list)}

        flipped = {}

        for key, value in gfx_display_dict.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)

        return flipped

    ##
    # @brief Exposed API to know if Pipe Joiner is required to drive the display.
    # @param[in] gfx_index - String - Graphics Index to which verify clocks
    # @param[in] port_name - String - Port Name on which pipe joiner check called.
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    @classmethod
    def is_pipe_joiner_required(cls, gfx_index: str, port_name: str):
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        gfx_index_str = gfx_index.lower()

        logging.debug("Platform: {}".format(platform))
        # Until Gen13 and DG2, driver enum precision changes are not done.
        # Following legacy calculation to compute effective cd clock in such cases
        if platform == 'TGL':
            from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
            sys_clk = TglClock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform == 'RKL':
            from Libs.Feature.clock.rkl.rkl_clock_base import RklClock
            sys_clk = RklClock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform == 'ADLS':
            from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
            sys_clk = AdlsClock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform == 'DG1':
            from Libs.Feature.clock.dg1.dg1_clock_base import Dg1Clock
            sys_clk = Dg1Clock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform == 'DG2':
            from Libs.Feature.clock.dg2.dg2_clock_base import Dg2Clock
            sys_clk = Dg2Clock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform == "ADLP":
            from Libs.Feature.clock.adlp.adlp_clock_base import AdlpClock
            sys_clk = AdlpClock()
            max_cd_clock = sys_clk.get_system_max_cd_clk(gfx_index_str)
            effective_cd_clock_mhz = sys_clk.cdclock_ctl_freq_dict[max_cd_clock]
        elif platform in ["MTL", "ELG", "LNL"]:
            # Gen14+ platforms will have constant effective CD clock for RefClk 38.4 frequency
            effective_cd_clock_mhz = GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ  # MHz
        elif platform == "PTL":
            effective_cd_clock_mhz = PTL_EFFECTIVE_CD_CLOCK_MHZ  # MHz
        elif platform == "NVL":
            effective_cd_clock_mhz = NVL_EFFECTIVE_CD_CLOCK_MHZ
        else:
            logging.error("Platform %s Not Supported pipe joiner, retuning false" % platform)
            return False, 1

        effective_cd_clock_hz = effective_cd_clock_mhz * 1000000

        logging.debug(f"Effective Cd Clock for {gfx_index_str}: {effective_cd_clock_hz}hz")
        is_pipe_joiner_required, no_of_pipe_required = clock_helper.ClockHelper.is_pipe_joiner_required(
            gfx_index_str, port_name, effective_cd_clock_hz)

        return is_pipe_joiner_required, no_of_pipe_required

    ##
    # @brief        Checks for the platform and calls the correct implementation to get current cd clock
    # @param[in]    gfx_index: str - Graphics index on which register read
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str) -> int:
        # call get_gfx_display_hardwareinfo() to get the platform type from system_info
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        clk = None
        current_cd_clock = None

        if platform == 'DG2':
            from Libs.Feature.clock.dg2.dg2_clock_base import Dg2Clock
            clk = Dg2Clock()
        elif platform == "ADLP":
            from Libs.Feature.clock.adlp.adlp_clock_base import AdlpClock
            clk = AdlpClock()
        elif platform == "TGL":
            from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
            clk = TglClock()
        elif platform == "RKL":
            from Libs.Feature.clock.rkl.rkl_clock_base import RklClock
            clk = RklClock()
        elif platform == "ADLS":
            from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
            clk = AdlsClock()
        elif platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
            clk = MtlClock()
        elif platform == "ELG":
            from Libs.Feature.clock.elg.elg_clock_base import ElgClock
            clk = ElgClock()
        elif platform == "LNL":
            from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
            clk = LnlClock()
        elif platform == "PTL":
            from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
            clk = PtlClock()
        elif platform == "WCL":
            from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
            clk = PtlClock(sku_name=platform)
        elif platform == "NVL":
            from Libs.Feature.clock.nvl.nvl_clock_base import NvlClock
            clk = NvlClock()
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine] Unable to get current CD clock for given platform: {}".format(
                    self.platform),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Platform Not Supported: %s" % self.platform)

        if clk is not None:
            current_cd_clock = clk.get_current_cd_clock(gfx_index)

        return current_cd_clock

    ##
    # @brief        Computes possible optimal CD clock for the child displays to be in collage
    # @param[in]    gfx_index: str - Graphics index on which register read
    # @param[in]    max_pixel_rate: float - max pixel rate computed among child displays to be in collage
    # @param[in]    display_list: List[str] - contains list of displays e.g. ['DP_F']
    # @return       current cd clock
    def get_optimal_cd_clock_from_pixelclock(self, gfx_index: str, max_pixel_rate: float,
                                             display_list: List[str], supported_pixel_rate_target_id = None) -> float:
        # call get_gfx_display_hardwareinfo() to get the platform type from system_info
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        clk = None
        optimal_cd_clock = None
        if platform == 'DG2':
            from Libs.Feature.clock.dg2.dg2_clock_base import Dg2Clock
            clk = Dg2Clock()

        elif platform == "ADLP":
            from Libs.Feature.clock.adlp.adlp_clock_base import AdlpClock
            clk = AdlpClock()

        elif platform == "TGL":
            from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
            clk = TglClock()

        elif platform == "RKL":
            from Libs.Feature.clock.rkl.rkl_clock_base import RklClock
            clk = RklClock()

        elif platform == "ADLS":
            from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
            clk = AdlsClock()

        elif platform == "MTL":
            from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
            clk = MtlClock()

        elif platform == "ELG":
            from Libs.Feature.clock.elg.elg_clock_base import ElgClock
            clk = ElgClock()

        elif platform == "LNL":
            from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
            clk = LnlClock()
        elif platform == "PTL":
            from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
            clk = PtlClock()
        elif platform == "NVL":
            from Libs.Feature.clock.nvl.nvl_clock_base import NvlClock
            clk = NvlClock()
        else:
            gdhm.report_test_bug_di(
                title=f"[Interfaces][Display_Engine] Unsupported platform to get optimal CD clock from given pixel "
                      f"clock: {self.platform}")
            logging.error("Platform Not Supported: %s" % self.platform)

        if clk is not None:
            if platform == "PTL":
                optimal_cd_clock = clk.get_optimal_cd_clock_from_pixelclock(gfx_index, max_pixel_rate, display_list, supported_pixel_rate_target_id)
            else:
                optimal_cd_clock = clk.get_optimal_cd_clock_from_pixelclock(gfx_index, max_pixel_rate, display_list)
        else:
            gdhm.report_test_bug_di("[Interfaces][Display_Engine] Invalid clock object found to get optimal CD clock "
                                    "from pixel clock")

        return optimal_cd_clock
