######################################################################################
# @file         multichip_genlock_base.py
# @brief        This is base script for multichip_genlock feature tests.
#
# @author       Sri Sumanth Geesala
######################################################################################
import logging
import sys
import math
import ctypes
import unittest
from enum import IntEnum

from Libs.Core import cmd_parser
from Libs.Core import enum, registry_access
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower
from Libs.Core.system_utility import SystemUtility
from Libs.Core import display_essential
from Libs.Core import display_utility
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.driver_escape import get_set_genlock
from Libs.Core.wrapper import driver_escape_args
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.powercons import registry
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.clock import clock_helper as clk_helper
from DisplayRegs.Gen12.Transcoder import Gen12TranscoderRegs
from DisplayRegs.Gen12.Pll import AdlsPllRegs
from DisplayRegs.Gen14 import Gen14NonAutoGenRegs
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14.Transcoder import Gen14TranscoderRegs
from DisplayRegs import DisplayArgs

REGISTRY_MULTICHIP_GENLOCK_MASK = (1 << 28)  # 28th bit is EnableMultichipGenlock


##
# @brief Base class for Multichip Genlock tests
class MultichipGenlockBase(unittest.TestCase):
    display_power = DisplayPower()
    system_utility = SystemUtility()
    disp_config = display_config.DisplayConfiguration()
    machine_info = SystemInfo()

    ##
    # @brief        Defines pipe frame stamp offset for each pipe
    class PipeFRMTMSTMP(IntEnum):
        PIPE_0 = 0x70048
        PIPE_1 = 0x71048
        PIPE_2 = 0x72048
        PIPE_3 = 0x73048

    # Map of ddi to bspec name convention
    ddi_to_bspec_name_map = dict([
        ('A', 'A'),
        ('F', 'USBC1'),
        ('G', 'USBC2'),
        ('H', 'USBC3'),
        ('I', 'USBC4')
    ])

    ##
    # @brief setup method for Multichip Genlock tests
    # @return None
    def setUp(self):
        logging.info('Starting Test Setup')
        self.my_custom_tags = ['-master_dut', '-master_display', '-wait_with_genlock']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        # Handle multi-adapter scenario. Since sync feature is for LFPs on same adapter,
        # we are interested with first adapter only.
        if isinstance(self.cmd_line_param, list):
            self.cmd_line_param = self.cmd_line_param[0]
        self.platform = None
        self.display_list = []
        self.adapter_list = []
        self.master_display = None
        self.master_display_transcoder = None
        self.slave_disp_list = []
        self.lfp_display = None
        self.master_dut = False
        self.wait_with_genlock_enabled = False
        self.plugged_displays = []
        self.genlock_args = None
        self.default_gfx_index = "gfx_0"  # hardcoded for now. Will have to refactor for multi-adapter
        self.TIMESTAMP_CTR_OFFSET = 0x44070

        # get platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        self.platform = ("%s" % gfx_display_hwinfo[0].DisplayAdapterName).lower()

        ##
        # Process command line params.
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None and value['connector_port'] is not None:
                if value['connector_port'] not in self.display_list:
                    if value['connector_port'].startswith('DP') or value['connector_port'].startswith('HDMI'):
                        self.adapter_list.insert(value['index'],
                                                 value['gfx_index'].lower() if value['gfx_index'] is not None
                                                 else self.default_gfx_index)
                        self.display_list.insert(value['index'], value['connector_port'])

            if key == 'MASTER_DISPLAY' and value != 'NONE':
                if cmd_parser.display_key_pattern.match(value[0].upper()) is not None:
                    self.master_display = value[0].upper()
                    logging.info(
                        f'Display {value[0].upper()} on {self.platform} selected as master display for genlock')
                else:
                    self.fail(f'Invalid display {value[0].upper()} passed as master display for genlock')

            if key == 'MASTER_DUT' and value != 'NONE' and value[0].upper() == 'TRUE':
                self.master_dut = True
                logging.info(f'Current DUT has been selected as master DUT')

            if key == 'WAIT_WITH_GENLOCK' and value != 'NONE' and value[0].upper() == 'TRUE':
                self.wait_with_genlock_enabled = True

        self.slave_disp_list = [disp for disp in self.display_list if disp != self.master_display]

        ##
        # Enable EnableMultichipGenlock bit in DisplayFeatureControl regkey. Restart driver.
        reg_value = registry.read(self.default_gfx_index, registry.RegKeys.DISPLAY_FEATURE_CONTROL)
        reg_value = reg_value | REGISTRY_MULTICHIP_GENLOCK_MASK
        ret = registry.write(self.default_gfx_index, registry.RegKeys.DISPLAY_FEATURE_CONTROL,
                             registry_access.RegDataType.DWORD, reg_value)
        if ret is None:
            logging.info('DisplayFeatureControl already has MultichipGenlock enabled.')
        elif ret is True:
            logging.info('Successfully enabled MultichipGenlock in DisplayFeatureControl.')
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is True:
                logging.info('Successfully Restarted Driver')
            else:
                self.fail('[Driver Issue]: Failed to Disable and Enable Driver')
        else:
            self.fail('Failed to enable MultichipGenlock in DisplayFeatureControl.')

        ##
        # Verify and plug the display.
        self.plugged_displays, enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        # find LFP display if any connected
        for index in range(enumerated_displays.Count):
            port = str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
            if display_utility.get_vbt_panel_type(port, self.default_gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                self.lfp_display = port
                break

    ##
    # @brief Teardown method for Multichip Genlock tests
    # @return None
    def tearDown(self):
        logging.info('Starting Test Cleanup')

        ##
        # Unplug the displays and restore the configuration to the initial configuration.
        # We have to unplug master display at the last. So removing and appending it at end to the self.plugged_displays
        if self.master_display is not None:
            self.plugged_displays.remove(self.master_display)
            self.plugged_displays.append(self.master_display)
        for display in self.plugged_displays:
            logging.info(f'Trying to unplug {display}')
            flag = display_utility.unplug(display)
            enumerated_displays = self.disp_config.get_enumerated_display_info()
            self.assertNotEquals(enumerated_displays, None, 'Aborting the test as enumerated_displays is None')

            plug_status = display_config.is_display_attached(enumerated_displays, display)
            if display == self.master_display and self.platform.upper() == 'ELG' and plug_status == True:
                    logging.warning(
                        f"WARN: Display {display} reported as still Attached. Sometimes OS does not update Unplug Status for last display, in case where "
                        "Virtual Display not plugged by driver. Ignoring unplug status for such cases")
            else:
                self.assertNotEquals(plug_status, True, 'Aborting the test as unplugging the display failed.')

        ##
        # Disable EnableMultichipGenlock bit in DisplayFeatureControl regkey. Restart driver.
        reg_value = registry.read(self.default_gfx_index, registry.RegKeys.DISPLAY_FEATURE_CONTROL)
        disable_mask = (pow(2, 32) - 1) ^ REGISTRY_MULTICHIP_GENLOCK_MASK
        reg_value = reg_value & disable_mask
        ret = registry.write(self.default_gfx_index, registry.RegKeys.DISPLAY_FEATURE_CONTROL,
                             registry_access.RegDataType.DWORD, reg_value)
        if ret is None:
            logging.info('DisplayFeatureControl already has MultichipGenlock disabled.')
        elif ret is True:
            logging.info('Successfully disabled MultichipGenlock in DisplayFeatureControl.')

            execution_environment_type = SystemUtility().get_execution_environment_type()

            if execution_environment_type != "POST_SI_ENV":
                logging.info("WA: Skipping driver restart for supporting validation on pre-Si, as it sporadically crashes after restart even though test passes.")
                status = True
            else:
                status, reboot_required = display_essential.restart_gfx_driver()

            if status:
                logging.info('Successfully Restarted Driver')
            else:
                self.fail('[Driver Issue]: Failed to Disable and Enable Driver')
        else:
            self.fail('Failed to disable MultichipGenlock in DisplayFeatureControl.')

    ##
    # @brief        compares the expected and actual values passed, and print PASS or FAIL log.
    # @param[in]    register register name of the current feature being verified
    # @param[in]    field field name in the register of the current feature
    # @param[in]    expected expected value (can be either number/string)
    # @param[in]    actual actual value (can be either number/string)
    # @param[in]    expected_value_name readable name of the expected value (since expected can be an integer value)
    # @param[in]    message any extra message to be printed in log (say, for describing current case)
    # @return       bool; returns True if comparison matched, False otherwise
    def verify_and_log_helper(self, register, field, expected, actual, expected_value_name='', message=''):
        res_template = "{res} : {register} - {field} {message} \t \t : Expected= {expected}{expected_value_name} " \
                       "\t Actual= {actual}"
        # e.g: 'FAIL : TRANS_HTOTAL_DSI0 - HActive - must be divisible by 4                  : Expected= 1080        Actual= 1081'

        if message != '':
            message = '- ' + message
        if expected_value_name != '':
            expected_value_name = '(' + expected_value_name + ')'

        if actual == expected:
            logging.info(
                res_template.format(res='PASS', register=register, field=field, message=message, expected=expected,
                                    expected_value_name=expected_value_name, actual=actual))
            return True
        else:
            logging.error(
                res_template.format(res='FAIL', register=register, field=field, message=message, expected=expected,
                                    expected_value_name=expected_value_name, actual=actual))
            return False

    ##
    # @brief        reads DPCLKA_CFGCR0 and DPCLKA_CFGCR1 registers to find which PLL is selected for current display
    # @param[in]    display display name like DP_A, DP_B, HDMI_B, etc
    # @return       string; returns the DPLL value like DPLL0, DPLL1, etc
    def gen12_get_selected_dpll_for_display(self, display):
        adls_ddi_pll_map = dict([
            (0, 'DPLL0'),
            (1, 'DPLL1'),
            (2, 'DPLL4'),
            (3, 'DPLL3')
        ])

        gfx_index = self.adapter_list[0]
        offset = AdlsPllRegs.OFFSET_DPCLKA_CFGCR0.DPCLKA_CFGCR0
        value = DisplayArgs.read_register(offset, gfx_index)
        dpclka_cfgcr0 = AdlsPllRegs.REG_DPCLKA_CFGCR0(offset, value)

        offset = AdlsPllRegs.OFFSET_DPCLKA_CFGCR1.DPCLKA_CFGCR1
        value = DisplayArgs.read_register(offset, gfx_index)
        dpclka_cfgcr1 = AdlsPllRegs.REG_DPCLKA_CFGCR1(offset, value)

        if '_A' in display.upper():
            dpllValue = adls_ddi_pll_map[dpclka_cfgcr0.DdiaMuxSelect]
        elif '_B' in display.upper():
            dpllValue = adls_ddi_pll_map[dpclka_cfgcr0.DdibMuxSelect]
        elif '_C' in display.upper():
            dpllValue = adls_ddi_pll_map[dpclka_cfgcr0.DdiiMuxSelect]
        elif '_D' in display.upper():
            dpllValue = adls_ddi_pll_map[dpclka_cfgcr1.DdijMuxSelect]
        else:
            dpllValue = adls_ddi_pll_map[dpclka_cfgcr1.DdikMuxSelect]

        logging.info(f'Display {display} selected PLL is : {dpllValue}')

        return dpllValue

    ##
    # @brief Set the given config along with displays
    # @param[in] config enumeration SINGLE/CLONE/EXTENDED
    # @param[in] displays Display list to set config with
    # @param[in] adapters adapter list to set the config ['GFX_0','GFX_1',..'GFX_N']
    # @return None
    def set_and_validate_config(self, config, displays, adapters):
        if len(self.display_list) < len(displays):
            logging.info(f'Ignoring the config {config} in sequence since planned test has '
                         f'only {len(self.display_list)} displays')
            return

        enumerated_displays = self.disp_config.get_enumerated_display_info()
        self.display_and_adapter_list = []

        logging.info(f'Enumerated display count:{enumerated_displays.Count}, Displays count:{len(displays)}')
        for count in range(enumerated_displays.Count):
            display_name = ((CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[count].ConnectorNPortType)).name)
            gfx_adapter = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            for i in range(len(displays)):
                if ((display_name == displays[i]) and (gfx_adapter == adapters[i].lower())):
                    logging.debug(
                        "Adapter:{0}, Display added to set config params:{1}".format(adapters[i], display_name))
                    self.display_and_adapter_list.append(
                        enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)

        if self.disp_config.set_display_configuration_ex(config, self.display_and_adapter_list) is False:
            self.fail("SetDisplayConfigurationEX returned false")

    ##
    # @brief Fills the genlock args structure for the displays with target ids passed
    # @param[in] display_list list of displays for setting genlock
    # @return genlock_args - filled in structure of type DdCapiEscGetSetGenlockArgs
    def fill_genlock_args(self, display_list) -> driver_escape_args.DdCapiEscGetSetGenlockArgs:
        enumerated_displays = self.disp_config.get_enumerated_display_info()
        target_id_list = [self.disp_config.get_target_id(display, enumerated_displays) for display in display_list]

        genlock_args = driver_escape_args.DdCapiEscGetSetGenlockArgs()
        genlock_args.IsGenlockSupported = True
        genlock_args.IsGenlockPossible = True
        genlock_args.GenlockTopology.NumGenlockDisplays = len(display_list)
        genlock_args.GenlockTopology.IsMasterGenlockSystem = self.master_dut

        display_and_adapter_info = self.disp_config.get_display_and_adapter_info(target_id_list[0])
        display_timings = self.disp_config.get_display_timings(display_and_adapter_info)
        try:
            genlock_args.GenlockTopology.CommonTargetModeTiming.PixelClock = display_timings.targetPixelRate
            genlock_args.GenlockTopology.CommonTargetModeTiming.HActive = display_timings.hActive
            genlock_args.GenlockTopology.CommonTargetModeTiming.VActive = display_timings.vActive
            genlock_args.GenlockTopology.CommonTargetModeTiming.HTotal = display_timings.hTotal
            genlock_args.GenlockTopology.CommonTargetModeTiming.VTotal = display_timings.vTotal
            genlock_args.GenlockTopology.CommonTargetModeTiming.HBlank = \
                display_timings.hTotal - display_timings.hActive
            genlock_args.GenlockTopology.CommonTargetModeTiming.VBlank = \
                display_timings.vTotal - display_timings.vActive
            genlock_args.GenlockTopology.CommonTargetModeTiming.RefreshRate = \
                math.ceil(display_timings.vSyncNumerator / display_timings.vSyncDenominator)
            genlock_args.GenlockTopology.CommonTargetModeTiming.SignalStandard = 3  # setting it to VESA CVT by default
        except ZeroDivisionError:
            self.fail('Divide by 0 error in RefreshRate calculation')

        for index, target_id in enumerate(target_id_list):
            genlock_args.GenlockTopology.GenlockDisplayInfo[index].TargetId = target_id
            genlock_args.GenlockTopology.GenlockDisplayInfo[index].IsMaster = True \
                if self.master_display == display_list[index] else False
            genlock_args.GenlockTopology.GenlockDisplayInfo[index].LinkRateMbps = \
                int(dpcd_helper.DPCD_getLinkRate(target_id) * 1000)
            genlock_args.GenlockTopology.GenlockDisplayInfo[index].DpLaneWidthSelection = \
                dpcd_helper.DPCD_getNumOfLanes(target_id)

            display_and_adapter_info = self.disp_config.get_display_and_adapter_info(target_id)
            display_timings = self.disp_config.get_display_timings(display_and_adapter_info)

            # Keeping NumModes as 1 since we are interested in only one mode i.e, common mode
            num_of_modes = 1
            genlock_args.GenlockTopology.GenlockModeList[index].TargetId = target_id
            genlock_args.GenlockTopology.GenlockModeList[index].NumModes = num_of_modes
            genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes = \
                ctypes.pointer(driver_escape_args.CapiTiming())
            try:
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].PixelClock = \
                    display_timings.targetPixelRate
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].HActive = display_timings.hActive
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].VActive = display_timings.vActive
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].HTotal = display_timings.hTotal
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].VTotal = display_timings.vTotal
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].HBlank = \
                    display_timings.hTotal - display_timings.hActive
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].VBlank = \
                    display_timings.vTotal - display_timings.vActive
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].RefreshRate = \
                    math.ceil(display_timings.vSyncNumerator / display_timings.vSyncDenominator)
                # setting SignalStandard to VESA CVT by default
                genlock_args.GenlockTopology.GenlockModeList[index].pTargetModes[0].SignalStandard = 3
            except ZeroDivisionError:
                self.fail('Divide by 0 error in RefreshRate calculation')

        return genlock_args

    ##
    # @brief Fills the genlock args structure for the displays with target ids passed
    # @param[in] display_list list of displays for setting number of targets
    # @return genlock_args - filled in structure of type DdCapiGetVblankTimestampForTarget
    def fill_genlock_args_for_fetching_vblank_ts(self,
                                                 display_list) -> driver_escape_args.DdCapiGetVblankTimestampForTarget:
        num_targets = len(display_list)
        genlock_args = driver_escape_args.DdCapiGetVblankTimestampForTarget()
        genlock_args.NumOfTargets = num_targets
        return genlock_args

    ##
    # @brief        Verifies the genlock bits in registers for the displays in genlock as per the Display Gen
    # @param[in]    display_list list of displays for verifying genlock programming
    # @param[in]    verify_prog flag to tell whether to verify register programmming or not. Verifies by default.
    # @return       True if verification passed, False otherwise.
    def print_verify_genlock_registers(self, display_list, verify_prog=True):
        if self.platform.upper() in ['ADLS']:
            return self.gen12_print_verify_genlock_registers(display_list, verify_prog)
        # Genlock bits in registers are same for MTL, ELG and PTL
        elif self.platform.upper() in ['MTL', 'ELG', 'PTL']:
            return self.gen14_print_verify_genlock_registers(display_list, verify_prog)
        else:
            logging.error(f'Genlock not supported on {self.platform}')
            return False

    ##
    # @brief        Gen14 specific. Does register programming verification for the displays in genlock
    # @param[in]    display_list list of displays for verifying genlock programming
    # @param[in]    verify_prog flag to tell whether to verify register programmming or not. Verifies by default.
    # @return       True if verification passed, False otherwise.
    def gen14_print_verify_genlock_registers(self, display_list, verify_prog=True):

        # Logging Genlock defuse bit.
        # Single chip Genlock is un-affected by this.
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', self.default_gfx_index)
        value = clock_helper_.get_value_by_range(reg_value, 0, 0, '',"genlock_disable")

        logging.info(f'Genlock disable fuse status: {value}')


        ret = True

        # Board related Genlock fields
        gfx_index = self.adapter_list[0]
        offset = Gen14NonAutoGenRegs.OFFSET_SPIN_MISC_CTL.SPIN_MISC_CTL  # Genlock Board Pin fields in south display
        value = DisplayArgs.read_register(offset, gfx_index)
        spin_misc_ctl = Gen14NonAutoGenRegs.REG_SPIN_MISC_CTL(offset, value)
        logging.info(f'SPIN_MISC_CTL = {hex(spin_misc_ctl.value)}')

        offset = Gen14NonAutoGenRegs.OFFSET_GENLOCK_PLL_ENABLE.GENLOCK_PLL_ENABLE
        value = DisplayArgs.read_register(offset, gfx_index)
        genlock_pll_enable = Gen14NonAutoGenRegs.REG_GENLOCK_PLL_ENABLE(offset, value)
        logging.info(f'GENLOCK_PLL_ENABLE = {hex(genlock_pll_enable.value)}')

        if verify_prog:
            ret = self.verify_and_log_helper(register='SPIN_MISC_CTL', field='GenlockBoardEnablePinEnable',
                                             expected=1, actual=spin_misc_ctl.GenlockBoardEnablePinEnable) and ret

            ret = self.verify_and_log_helper(register='SPIN_MISC_CTL', field='GenlockBoardEnablePinData',
                                             expected=1, actual=spin_misc_ctl.GenlockBoardEnablePinData) and ret

            ret = self.verify_and_log_helper(register='SPIN_MISC_CTL', field='GenlockBoardDirectionPinEnable',
                                             expected=1, actual=spin_misc_ctl.GenlockBoardDirectionPinEnable) and ret

            ret = self.verify_and_log_helper(register='SPIN_MISC_CTL', field='GenlockBoardDirectionPinData',
                                             expected=0 if self.master_dut else 1,
                                             actual=spin_misc_ctl.GenlockBoardDirectionPinData) and ret

            # PLL ENABLE & PLL LOCK BIT will not be written for Master DUT(Primary system). In case of single chip Genlock we only have master DUT(Primary system). Hence it will not be written.
            # Auto test covers only single chip Genlock
            if not self.master_dut:
                ret = self.verify_and_log_helper(register='GENLOCK_PLL_ENABLE', field='PllEnable',
                                                 expected=1, actual=genlock_pll_enable.PllEnable) and ret

                ret = self.verify_and_log_helper(register='GENLOCK_PLL_ENABLE', field='PllLock',
                                                 expected=1, actual=genlock_pll_enable.PllLock) and ret

        # Display related Genlock fields
        if self.master_display is not None:
            display_base_obj = DisplayBase(self.master_display)
            self.master_display_transcoder, pipe = display_base_obj.get_transcoder_and_pipe(self.master_display)

        for display in display_list:
            gfx_index = self.adapter_list[self.display_list.index(display)]
            display_base_obj = DisplayBase(display)
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
            port = display.split('_')[-1].upper()
            trans = chr(current_transcoder + 64)

            offset = eval('Gen14PllRegs.OFFSET_PORT_CLOCK_CTL.PORT_CLOCK_CTL_' + self.ddi_to_bspec_name_map[port])
            value = DisplayArgs.read_register(offset, gfx_index)
            port_clock_ctl = Gen14PllRegs.REG_PORT_CLOCK_CTL(offset, value)
            logging.info(f'PORT_CLOCK_CTL_{port} = {hex(port_clock_ctl.value)}')

            offset = eval('Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL2.TRANS_DDI_FUNC_CTL2_' + trans)
            value = DisplayArgs.read_register(offset, gfx_index)
            trans_ddi_func_ctl2 = Gen14TranscoderRegs.REG_TRANS_DDI_FUNC_CTL2(offset, value)
            logging.info(f'TRANS_DDI_FUNC_CTL2_{trans} = {hex(trans_ddi_func_ctl2.value)}')

            if verify_prog:
                # REFCLK_SELECT = 0 as per bspec in case of single chip genlock (Auto test covers only single chip genlock)
                # Bspec: https://gfxspecs.intel.com/Predator/ContentEdit/(S(qmfjykiawm1qx5xirebyujfe))/Content/Bun/GEN_HAS_14014583703
                ret = self.verify_and_log_helper(register='PORT_CLOCK_CTL', field='RefclkSelect',
                                                 expected=Gen14PllRegs.ENUM_REFCLK_SELECT.REFCLK_SELECT_NORMAL.value,
                                                 actual=port_clock_ctl.RefclkSelect, expected_value_name=
                                                 Gen14PllRegs.ENUM_REFCLK_SELECT.REFCLK_SELECT_GENLOCK.name) and ret

                ret = self.verify_and_log_helper(register='PORT_CLOCK_CTL', field='RequestPhyReleaseRefclk',
                                                 expected=0, actual=port_clock_ctl.RequestPhyReleaseRefclk) and ret

                expected = Gen14TranscoderRegs.ENUM_GENLOCK_ENABLE.GENLOCK_ENABLE
                ret = self.verify_and_log_helper(register='TRANS_DDI_FUNC_CTL2', field='GenlockEnable',
                                                 expected=expected.value, actual=trans_ddi_func_ctl2.GenlockEnable,
                                                 expected_value_name=expected.name) and ret

                if self.master_dut:
                    if self.master_display == display:
                        expected_mode = Gen14TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_MASTER
                        expected_port_sync_mode_master_select = 0
                    else:
                        expected_mode = Gen14TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_LOCAL_SLAVE
                        expected_port_sync_mode_master_select = self.master_display_transcoder
                else:
                    expected_mode = Gen14TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_REMOTE_SLAVE
                    expected_port_sync_mode_master_select = 0

                ret = self.verify_and_log_helper(register=f'TRANS_DDI_FUNC_CTL2_{trans}', field='GenlockMode',
                                                 expected=expected_mode.value, actual=trans_ddi_func_ctl2.GenlockMode,
                                                 expected_value_name=expected_mode.name) and ret

                ret = self.verify_and_log_helper(register=f'TRANS_DDI_FUNC_CTL2_{trans}',
                                                 field='PortSyncModeMasterSelect',
                                                 expected=expected_port_sync_mode_master_select,
                                                 actual=trans_ddi_func_ctl2.PortSyncModeMasterSelect,
                                                 expected_value_name='Transcoder ' +
                                                                     chr(expected_port_sync_mode_master_select + 64)) and ret
        return ret

    ##
    # @brief        Gen12 specific. Does register programming verification for the displays in genlock
    # @param[in]    display_list list of displays for verifying genlock programming
    # @param[in]    verify_prog flag to tell whether to verify register programmming or not. Verifies by default.
    # @return       True if verification passed, False otherwise.
    def gen12_print_verify_genlock_registers(self, display_list, verify_prog=True):
        ret = True

        # verify platform overall registers UTIL_PIN_CTL and UTIL2_PIN_CTL.
        gfx_index = self.adapter_list[0]
        offset = Gen12TranscoderRegs.OFFSET_UTIL_PIN_CTL.UTIL_PIN_CTL
        value = DisplayArgs.read_register(offset, gfx_index)
        util_pin_ctl = Gen12TranscoderRegs.REG_UTIL_PIN_CTL(offset, value)
        logging.info(f'UTIL_PIN_CTL = {hex(util_pin_ctl.value)}')

        offset = Gen12TranscoderRegs.OFFSET_UTIL2_PIN_CTL.UTIL2_PIN_CTL
        value = DisplayArgs.read_register(offset, gfx_index)
        util2_pin_ctl = Gen12TranscoderRegs.REG_UTIL2_PIN_CTL(offset, value)
        logging.info(f'UTIL2_PIN_CTL = {hex(util2_pin_ctl.value)}')

        if verify_prog:
            expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_ENABLE.UTIL_PIN_ENABLE
            ret = self.verify_and_log_helper(register='UTIL_PIN_CTL', field='UtilPinEnable',
                                             expected=expected.value,
                                             actual=util_pin_ctl.UtilPinEnable,
                                             expected_value_name=expected.name) and ret

            expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_ENABLE.UTIL_PIN_ENABLE
            ret = self.verify_and_log_helper(register='UTIL2_PIN_CTL', field='UtilPinEnable',
                                             expected=expected.value,
                                             actual=util2_pin_ctl.UtilPinEnable,
                                             expected_value_name=expected.name) and ret

            if self.master_dut:
                expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_DIRECTION.UTIL_PIN_DIRECTION_OUTPUT
                ret = self.verify_and_log_helper(register='UTIL_PIN_CTL', field='UtilPinDirection',
                                                 expected=expected.value, actual=util_pin_ctl.UtilPinDirection,
                                                 expected_value_name=expected.name) and ret

                expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_MODE.UTIL_PIN_MODE_FRAMESTART
                ret = self.verify_and_log_helper(register='UTIL_PIN_CTL', field='UtilPinMode',
                                                 expected=expected.value, actual=util_pin_ctl.UtilPinMode,
                                                 expected_value_name=expected.name) and ret

                display_base_obj = DisplayBase(self.master_display)
                current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.master_display)
                pipe = chr(int(current_pipe) + 65)
                logging.info(f'Master display {self.master_display} is active on pipe {pipe}')
                # UTIL_PIN_CTL Pipe Select = <pipe attached to the master transcoder>
                expected = eval('Gen12TranscoderRegs.ENUM_PIPE_SELECT.PIPE_SELECT_PIPE_' + pipe)
                ret = self.verify_and_log_helper(register='UTIL_PIN_CTL', field='PipeSelect',
                                                 expected=expected.value, actual=util_pin_ctl.PipeSelect,
                                                 expected_value_name=expected.name) and ret

                expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_DIRECTION.UTIL_PIN_DIRECTION_OUTPUT
                ret = self.verify_and_log_helper(register='UTIL2_PIN_CTL', field='UtilPinDirection',
                                                 expected=expected.value, actual=util2_pin_ctl.UtilPinDirection,
                                                 expected_value_name=expected.name) and ret
            else:
                expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_DIRECTION.UTIL_PIN_DIRECTION_INPUT
                ret = self.verify_and_log_helper(register='UTIL_PIN_CTL', field='UtilPinDirection',
                                                 expected=expected.value, actual=util_pin_ctl.UtilPinDirection,
                                                 expected_value_name=expected.name) and ret

                expected = Gen12TranscoderRegs.ENUM_UTIL_PIN_DIRECTION.UTIL_PIN_DIRECTION_INPUT
                ret = self.verify_and_log_helper(register='UTIL2_PIN_CTL', field='UtilPinDirection',
                                                 expected=expected.value, actual=util2_pin_ctl.UtilPinDirection,
                                                 expected_value_name=expected.name) and ret

        for display in display_list:
            gfx_index = self.adapter_list[self.display_list.index(display)]
            display_base_obj = DisplayBase(display)
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
            trans = chr(current_transcoder + 64)

            offset = eval('Gen12TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL2.TRANS_DDI_FUNC_CTL2_' + trans)
            value = DisplayArgs.read_register(offset, gfx_index)
            trans_ddi_func_ctl2 = Gen12TranscoderRegs.REG_TRANS_DDI_FUNC_CTL2(offset, value)
            logging.info(f'TRANS_DDI_FUNC_CTL2_{trans} = {hex(trans_ddi_func_ctl2.value)}')

            dpll = self.gen12_get_selected_dpll_for_display(display)
            offset = eval('AdlsPllRegs.OFFSET_DPLL_CFGCR1.' + dpll + '_CFGCR1')
            value = DisplayArgs.read_register(offset, gfx_index)
            dpll_cfgcr1 = AdlsPllRegs.REG_DPLL_CFGCR1(offset, value)
            logging.info(f'{dpll}_CFGCR1 = {hex(dpll_cfgcr1.value)}')

            if verify_prog:
                expected = Gen12TranscoderRegs.ENUM_GENLOCK_ENABLE.GENLOCK_ENABLE
                ret = self.verify_and_log_helper(register=f'TRANS_DDI_FUNC_CTL2_{trans}', field='Genlock enable',
                                                 expected=expected.value, actual=trans_ddi_func_ctl2.GenlockEnable,
                                                 expected_value_name=expected.name) and ret

                if self.master_dut:
                    if self.master_display == display:
                        expected_mode = Gen12TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_MASTER
                    else:
                        expected_mode = Gen12TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_LOCAL_SLAVE
                    expected_cfselovrd = AdlsPllRegs.ENUM_CFSELOVRD.CFSELOVRD_NORMAL_XTAL
                else:
                    expected_mode = Gen12TranscoderRegs.ENUM_GENLOCK_MODE.GENLOCK_MODE_REMOTE_SLAVE
                    expected_cfselovrd = AdlsPllRegs.ENUM_CFSELOVRD.CFSELOVRD_FILTERED_GENLOCK_REF

                ret = self.verify_and_log_helper(register=f'TRANS_DDI_FUNC_CTL2_{trans}', field='Genlock Mode',
                                                 expected=expected_mode.value, actual=trans_ddi_func_ctl2.GenlockMode,
                                                 expected_value_name=expected_mode.name) and ret

                ret = self.verify_and_log_helper(register=f'{dpll}_CFGCR1', field='cfselovrd',
                                                 expected=expected_cfselovrd.value, actual=dpll_cfgcr1.Cfselovrd,
                                                 expected_value_name=expected_cfselovrd.name) and ret

        return ret

    ##
    # @brief    It disables the genlock and does modeset on the earlier genlocked displays. This ensures that each
    #           display unlatches from genlock reference PLL and gets fresh modesets with individual non-genlock PLLs.
    # @return   None
    def disable_genlock_and_do_modeset_on_displays(self):
        if self.wait_with_genlock_enabled:
            input('Displays are in Genlock enabled state. Press any key to continue disabling Genlock...')

        ##
        # disable genlock
        display_and_adapter_info = self.disp_config.get_display_and_adapter_info_ex(self.display_list[0],
                                                                                    self.default_gfx_index)
        if get_set_genlock(display_and_adapter_info, False, self.genlock_args):
            logging.info(f'Disable genlock successful on {display_and_adapter_info.adapterInfo.gfxIndex}')
        else:
            logging.error(f'Disable genlock failed on {display_and_adapter_info.adapterInfo.gfxIndex}')
            self.fail('Disable genlock call failed')

        # Do display switching so as to do modeset on all displays after genlock is disabled.
        # Post disabling genlock, slaves should get modeset, and master should get modeset at the last.
        # first turn off slaves, and only keep master enabled (since master should turn off last).
        adapter_list = [self.default_gfx_index] * len(self.display_list)
        if self.master_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.master_display], adapter_list)

        # turn off master also now by switching to SD LFP.
        if self.lfp_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.lfp_display], adapter_list)
        elif len(self.slave_disp_list) > 0:
            self.set_and_validate_config(enum.SINGLE, [self.slave_disp_list[0]], adapter_list)

        # turn on all EFP displays now so they get modeset now with their individual PLLs (non-genlock mode).
        self.set_and_validate_config(enum.EXTENDED if len(self.display_list) > 1 else enum.SINGLE,
                                     self.display_list, adapter_list)
