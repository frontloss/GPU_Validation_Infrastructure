######################################################################################
# @file     fbc_base.py
# @brief    Python wrapper helper module providing setUp and tearDown methods
# @author   Suraj Gaikwad, Amit Sau
######################################################################################
import logging
import sys
import unittest

from Libs.Core import reboot_helper, cmd_parser, enum, display_utility, display_essential, display_power
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_fbc import fbc
from Libs.Feature.display_psr import DisplayPsr, DriverPsrVersion
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

##
# Fbc base class
class FbcBase(unittest.TestCase):
    enumerated_displays = None
    display_list = list()
    display_config = disp_cfg.DisplayConfiguration()
    display_psr = DisplayPsr()
    custom_tags = {'-POWER_EVENT': ['S3', 'CS']}
    power_event = None
    is_edp_present = False


    ##
    # @brief    Set up method
    # @return   None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags.keys())

        ##
        # Display_list[] is a list of Port Names of the connected Displays
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.display_list.insert(value['index'], value['connector_port'])
                if key in ['EDP_A', 'EDP_B']:
                    self.is_edp_present = True

        ##
        # Iterate through the command line to get the Power Event type (if mentioned in the command line)
        if self.cmd_line_param['POWER_EVENT'] != 'NONE':
            pwr_evnt_arg = self.cmd_line_param['POWER_EVENT'][0]
            if pwr_evnt_arg in self.custom_tags.get('-POWER_EVENT'):
                self.power_event = display_power.PowerEvent.CS if pwr_evnt_arg == 'CS' else display_power.PowerEvent.S3
            else:
                self.fail('Invalid Power Event command line argument provided')

        ##
        # Get Enumerated displays details
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        self.verify_test_control_flag()

    ##
    # @brief    Tear down method
    # @return   None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        if self.plugged_display is not None:
            for display in self.plugged_display:
                if display_utility.unplug(display) is False:
                    self.fail("Failed to unplug the display %s" % display)
                logging.info("Successfully unplugged the display %s" % display)
        self.verify_test_control_flag()

    ##
    # @brief     Verify feature test control flag
    # @return     None
    def verify_test_control_flag(self):
        for adapter in fbc.PLATFORM_INFO.values():
            gfx_index = adapter['gfx_index']
            feature_test_ctl = registry.FeatureTestControl(gfx_index)
            if feature_test_ctl.fbc_disable == 1:
                logging.info('FBC is disable from driver on {}'.format(gfx_index))
                logging.info('Enabling FBC through feature test control flag on {}'.format(gfx_index))
                feature_test_ctl.fbc_disable = 0
                if feature_test_ctl.update(gfx_index):
                    status, reboot_required = display_essential.restart_gfx_driver()
                logging.info('Successfully enabled FBC through feature test control flag on {}'.format(gfx_index))

    ##
    # @brief    check psr2 support method
    # @return   Boolean
    def check_psr2_support(self):
        status = False
        # Proceed only in case of EDP is passed in command-line args
        if self.is_edp_present:
            for adapter in fbc.PLATFORM_INFO.values():
                gfx_index = adapter['gfx_index']
                if adapter['name'] in common.PRE_GEN_14_PLATFORMS:
                    pipe_list = ['PIPE_A']
                else:
                    pipe_list = ['PIPE_A', 'PIPE_B']
                port_data = display_base.get_port_to_pipe(gfx_index=gfx_index).items()
                for port, pipe in port_data:
                    if pipe not in pipe_list:
                        continue
                    is_psr_supported = self.display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_2, edp_port=port) or \
                        self.display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_1, edp_port=port)
                    transcoder = pipe.split('_')[1]
                    if display_utility.get_vbt_panel_type(port, gfx_index.lower()) == \
                            display_utility.VbtPanelType.LFP_DP and is_psr_supported:
                        srd_ctl_edp = MMIORegister.read(
                            'SRD_CTL_REGISTER', 'SRD_CTL_' + transcoder, adapter['name'], gfx_index=gfx_index)
                        psr2_ctl_edp = MMIORegister.read(
                            'PSR2_CTL_REGISTER', 'PSR2_CTL_' + transcoder, adapter['name'], gfx_index=gfx_index)

                        is_psr1_enabled = srd_ctl_edp.srd_enable == 1
                        is_psr2_enabled = psr2_ctl_edp.psr2_enable == 1

                        if is_psr1_enabled or is_psr2_enabled:
                            # Check that FBC is disabled automatically in the driver
                            if fbc.get_fbc_enable_status(gfx_index, transcoder):
                                gdhm.report_bug(
                                    title="[PowerCons][FBC] FBC not disabled when PSR enabled in driver",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail(f"FBC is not disabled for {port}")
                            logging.info("FBC is disabled when PSR panel is connected")
                            status = True
                        else:
                            logging.info(f"PSR1/PSR2 is not enabled in {adapter['name']}")
        return status


    ##
    # @brief        Helper function to get currently plugged displays' port and target_id mapping
    # @param[in]    gfx_index: str, graphics index of adapter
    # @return       target_id_mapping: Dict[{port_name: target_id}]
    def get_port_targetid_map(self, gfx_index: str) -> dict:
        enumerated_displays = self.display_config.get_enumerated_display_info()
        target_id_mapping = dict()

        for display_index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[display_index]
            if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

        return target_id_mapping
