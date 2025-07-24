#################################################################################################################
# @file         pr_base.py
# @brief        implements panel replay helper functions.
# @author       ashishk2
#################################################################################################################

import logging
import os
import unittest

import Tests.PowerCons.Modules.dpcd as PrDpcd
from Libs.Core import driver_escape, display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_fbc import fbc
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase
from Tests.PowerCons.Functional.PSR import pr
from Tests.PowerCons.Modules import common
from Tests.PowerCons.PnP.tools import socwatch
from registers.mmioregister import MMIORegister


##
# @brief This class contains functions that helps in validating PR enable and other basic check.
class PrBase(unittest.TestCase):
    __SOC_WATCH_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "SocWatch")
    __PSR_CONFIG_PATH = os.path.join(test_context.ROOT_FOLDER, "Libs\\Feature\\psr_config.ini")
    socwatch_check = -1
    _port_index = 0
    _duration = 120
    # Platform details for all connected adapters
    PLATFORM_INFO = {
        gfx_index: {
            'gfx_index': gfx_index,
            'name': adapter_info.get_platform_info().PlatformName
        }
        for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
    }
    config = DisplayConfiguration()
    mstBase = DisplayPortMSTBase()
    mmio_read = MMIORegister()
    pr_capability_dpcd = PrDpcd.PanelReplayCapsSupported()
    pr_sink_status_dpcd = PrDpcd.SinkPanelReplayEnableAndConfiguration()

    ##
    # @brief        This method is the entry point for PR test cases. This enables the regkey required
    #               for execution of PR tests
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        logging.info("Enable PR in Registry")
        for gfx_index in cls.PLATFORM_INFO.values():
            status = pr.enable_for_efp(gfx_index['gfx_index'])
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    assert False, "FAILED to restart the driver"
            elif status is False:
                assert False, "Failed to enable PR"
        logging.info('Successfully enabled PR in registry')

    ##
    # @brief        This method is the exit point for PR test cases. This resets the regkey changes done
    #               for execution of PR tests
    # @return       None
    @classmethod
    def tearDownClass(cls) -> None:
        logging.info("TearDown: Disable PR in Registry")
        for gfx_index in cls.PLATFORM_INFO.values():
            status = pr.disable_for_efp(gfx_index['gfx_index'])
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    assert False, "FAILED to restart the driver"
            elif status is False:
                assert False, "Failed to disable PR"
        logging.info('TearDown: Successfully Disabled PR in registry')

    ##
    # @brief        This class method is the entry point for PR MST Scenario tests.
    #               Helps to initialize parameters required for test execution.
    # @return       None
    def setUp(self):
        logging.debug("1.  Entry: setUpClass")

        self.mstBase.setUp()
        self.mmio_read = MMIORegister()
        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for index in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[index].DisplayAdapterName)
            break
        logging.debug("2. Exit: PrBase -> setUpClass")

    ##
    # @brief get pipe suffix
    # @param[in]    port
    # @return       pipe suffix
    @staticmethod
    def getPipeSuffix(port):
        pr_disp_base = DisplayBase(port)
        pipe_suffix = pr_disp_base.pipe_suffix
        logging.info("Pipe suffic is : {}".format(pipe_suffix))
        return pipe_suffix

    ##
    # @brief Check if PR is enabled or not by driver
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def isPrEnable(self, port, platform, gfx_index='gfx_0'):
        pipe_suffix = self.getPipeSuffix(port)

        # Panel Replay should be enabled in TRANS_DP2_CTL
        if pipe_suffix is not None:
            dp2_pr_ctl = self.mmio_read.read('TRANS_DP2_CTL_REGISTER', "TRANS_DP2_CTL_%s" % pipe_suffix,
                                             platform, 0x0, gfx_index)
        else:
            logging.error("Pipe suffix is None")
            return False

        # Check if PR is enabled or not
        if dp2_pr_ctl.pr_enable:
            logging.info("Panel Replay enabled")
            return True

        logging.warning("Panel Replay is not enabled")
        return False

    ##
    # @brief Check if FBC is enabled or not, if its not enabled then enable it.
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def checkAndEnableFBC(self, platform, gfx_index='gfx_0'):
        # Check if FBC is enabled or not. To enable PR, FBC should be mandatorily enabled
        fbc_ctl = self.mmio_read.read('FBC_CTL_REGISTER', "FBC_CTL", platform, 0x0, gfx_index)

        if fbc_ctl.enable_fbc:
            logging.info("FBC is enabled")
            return True
        # Enable FBC
        logging.info("FBC is not enabled")
        fbc_enable_status = fbc.enable("gfx_0")
        if fbc_enable_status is False:
            logging.error("Failed to enable FBC on gfx_0")
            return False
        driver_restart_status, system_reboot_required = display_essential.restart_gfx_driver()
        if driver_restart_status is False:
            logging.error("Failed to restart graphics driver")
            return False
        return True
            

    ##
    # @brief Check if FEC is enabled or not after sink is plugged.
    # @param[in]    port
    # @param[in]    platform
    # @return       True/False
    def checkFECStatus(self, port, platform):
        pipe_suffix = self.getPipeSuffix(port)
        is_fec_enabled = False
        if pipe_suffix is not None:
            is_fec_enabled: bool = DSCHelper.get_fec_status('gfx_0', platform, pipe_suffix)
            if is_fec_enabled:
                logging.info("FEC is enabled")
            else:
                logging.error("FEC is not enabled")
        return is_fec_enabled

    ##
    # @brief Check if Continuous Full Frame is enabled or not by driver
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def isCffEnable(self, port, platform, gfx_index='gfx_0'):
        pipe_suffix = self.getPipeSuffix(port)

        # To check if Continuous Full frame fetch and update is set
        if pipe_suffix is None:
            logging.error("Pipe suffix is None")
            return False
        psr2_man_trk = self.mmio_read.read('PSR2_MAN_TRK_CTL_REGISTER', "PSR2_MAN_TRK_CTL_%s" % pipe_suffix,
                                            platform, 0x0, gfx_index)
        if platform not in common.PRE_GEN_15_PLATFORMS:
            cff_ctl = self.mmio_read.read('CFF_CTL_REGISTER', 'CFF_CTL_' + pipe_suffix, platform, 0x0, gfx_index)

        # Check if CFF is enabled or not
        if platform in common.PRE_GEN_15_PLATFORMS:
            if psr2_man_trk.sf_partial_frame_enable and psr2_man_trk.sf_continuous_full_frame:
                logging.info("SF Continuous Full Frame is Enabled")
                return True
        else:
            # For Gen-15+ platforms there is a dedicated register for CFF
            if psr2_man_trk.sf_partial_frame_enable and cff_ctl.sf_continuous_full_frame:
                logging.info("SF Continuous Full Frame is Enabled")
                return True
        logging.error("SF Continuous Full Frame is not enabled")
        return False


    ##
    # @brief Check if Continuous Full Frame is enabled or not by driver for gen13
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def getSRDStatusforPREnable(self, port, platform, gfx_index='gfx_0'):
        pipe_suffix = self.getPipeSuffix(port)
        if pipe_suffix is None:
            logging.error("Pipe suffix is None")
            return False

        if platform in common.PRE_GEN_16_PLATFORMS:

            srd_status = self.mmio_read.read('SRD_STATUS_REGISTER', "SRD_STATUS_%s" % pipe_suffix,
                                                 platform, 0x0, gfx_index)

            logging.debug("SRD STATUS REGISTER = {0}".format(srd_status.srd_state))

            # Check the SRD status once PR is enabled
            if srd_status.srd_state == 7:
                logging.info("SRD Status Register is programmed correctly")
                return True

            logging.error("SRD Status Register is not programmed correctly")
            return False
        else:
            psr2_status = MMIORegister.read("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + pipe_suffix,
                                            platform, gfx_index=gfx_index)
            logging.info(f"PR state = {psr2_status.psr2_pr_state}")
            if psr2_status.psr2_pr_state == 0x2 and psr2_status.link_status == 0x1:
                logging.info("PanelReplay with Link-on enabled")
                return True
            else:
                logging.error(f"PanelReplay with link-on is not enabled on {pipe_suffix}")
                return False


    ##
    # @brief Check if Panel Replay Enable is supported in Sink DPCD
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def PanelReplaySupportedinDPCD(self, port, platform, gfx_index='gfx_0'):
        display_and_adapter_info = self.config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]
        dpcd_flag, reg_values = driver_escape.read_dpcd(display_and_adapter_info, self.pr_capability_dpcd.offset)
        logging.info("Checking Panel Replay Support DPCD status on{}".format(port))

        if not dpcd_flag:
            logging.error("DPCD Read Failed For Offset: {}".format(self.pr_capability_dpcd.offset))
            return False

        self.pr_capability_dpcd.value = reg_values[0]

        if self.pr_capability_dpcd.panel_replay_support:
            logging.info("Panel Replay Capability is supported in Sink")
            return True

        logging.warning("Panel Replay Capability is not supported in Sink")
        return False

    ##
    # @brief Check if Panel Replay Enable is configured in Sink DPCD
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def PanelReplayEnabledinSinkDPCD(self, port, platform, gfx_index='gfx_0'):
        display_and_adapter_info = self.config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]
        dpcd_flag, reg_values = driver_escape.read_dpcd(display_and_adapter_info, self.pr_sink_status_dpcd.offset)
        logging.info("Checking Panel Replay Enable DPCD status on{}".format(port))

        if not dpcd_flag:
            logging.error("DPCD Read Failed For Offset: {}".format(self.pr_sink_status_dpcd.offset))
            return False

        self.pr_sink_status_dpcd.value = reg_values[0]

        if self.pr_sink_status_dpcd.panel_replay_enable_in_sink:
            logging.info("Panel Replay is Enabled in Sink")
            return True

        logging.warning("Panel Replay is not Enabled in Sink")
        return False

    ##
    # @brief Check if Selective Update is Enable is configured in Sink DPCD
    # @param[in]    port
    # @param[in]    platform
    # @param[in]    gfx_index
    # @return       True/False
    def SelectiveUpdateEnabledinSinkDPCD(self, port, platform, gfx_index='gfx_0'):
        display_and_adapter_info = self.config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]
        dpcd_flag, reg_values = driver_escape.read_dpcd(display_and_adapter_info, self.pr_sink_status_dpcd.offset)
        logging.info("Checking Selective Update Enable DPCD status on{}".format(port))

        if not dpcd_flag:
            logging.error("DPCD Read Failed For Offset: {}".format(self.pr_sink_status_dpcd.offset))
            return False

        self.pr_sink_status_dpcd.value = reg_values[0]

        if self.pr_sink_status_dpcd.selective_update_enable:
            logging.info("Selective Update is Enabled in Sink")
            return True

        logging.error("Selective Update is not Enabled in Sink")
        return False

    ##
    # @brief Check if Socwatch io Bandwidth is less for PR panel or not
    # @param[in]    io_bw_pr
    # @param[in]    io_bw_nonpr
    # @return       True/False
    @staticmethod
    def PrSocWatchBwVerification(io_bw_pr, io_bw_nonpr):
        return True if io_bw_pr <= io_bw_nonpr else False


##
# @brief        Check if Socwatch io Bandwidth is less for PR panel or not
# @param[in]    duration duration is secs
# @return       True/False
def get_io_bw_using_socwatch(duration=60):
    io_requests_bw = 0
    log_file = socwatch.run_workload("IDLE", duration=duration)
    result, soc_output = socwatch.parse_socwatch_output(log_file)
    if result:
        io_requests_bw = soc_output[socwatch.SocWatchFields.IO_REQUESTS]
        p_state_str = ""
        for key, value in soc_output.items():
            if "PACKAGE" in socwatch.SocWatchFields(key).name.upper():
                p_state_str = f"{socwatch.SocWatchFields(key).name} = {value}"
        logging.info("Package Residency: %s", p_state_str)
        logging.info(f"IO Request Memory Bandwidth in PR: {io_requests_bw}")
    else:
        logging.error("socwatch log parse is failed")
    return result, io_requests_bw
