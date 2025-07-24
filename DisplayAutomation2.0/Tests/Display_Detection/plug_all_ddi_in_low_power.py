########################################################################################################################
# @file         plug_all_ddi_in_low_power.py
# @brief        Validate display hot plug during low power mode.
#               displays are edp_a, dp_b, hdmi_b, hdmi_c, etc
#
# @details      This test_script follows:
#               1. Plug Display1 in Low Power State CS/S3 and unplug back for next plug.
#               2. Plug Display1 in Low Power State S4 and unplug back for next plug.
#               3. Plug Display1 in Low Power State Monitor Turn OFF.
#               4. Continues above steps(1 to 3) for other Displays mentioned in cmd line.
#               CommandLine:python plug_all_ddi_in_low_power.py -edp_a <-DP_B> <-HDMI_C> -sleepstate cs/s3 -SIM/-EMU
#               Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
#
#               Test will pass only if all the configurations are successfully applied otherwise it fail.
# @author       Raghupathy, Dushyanth Kumar, Balaji Gurusamy
########################################################################################################################
import sys

from Libs.Core import cmd_parser, reboot_helper
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Detection.display_hpd_base import *


##
# @brief        PlugAllDDIInLowPower base class : To be used in Display Detection tests
class PlugAllDDIInLowPower(DisplayHPDBase):

    ##
    # @brief        setup function. Parse displays to plug and hpd_mode from cmdline params
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUp Method")

        # Variable Initializing
        self.input_display_list = []
        self.adapter_list = []
        self.panel_index = {}
        self.cmd_line_param = {}
        self.hpd_mode = None

        user_args = sys.argv
        # Set control variable based on command line options
        for arg in user_args:
            if arg.upper() == "-SIM":
                self.hpd_mode = "SIM"
                user_args.remove("-SIM")
            elif arg.upper() == "-EMU":
                self.hpd_mode = "EMU"
                user_args.remove("-EMU")

        if self.hpd_mode is None:
            self.hpd_mode = "SIM"

        # Parse the commandline params
        self.cmd_line_param = cmd_parser.parse_cmdline(user_args, ['-sleepstate'])

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        # input_display_list[] is a list of Port Names from user args
        for i in self.cmd_line_param:
            cmd_line_param_adapter = i
            for key, value in cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if self.input_display_list.__contains__(value['connector_port']):
                            adapter = self.adapter_list[self.input_display_list.index(value['connector_port'])]
                        if not self.input_display_list.__contains__(value['connector_port']) or (
                                self.input_display_list.__contains__(value['connector_port']) and adapter != value['gfx_index']):
                            if (value['gfx_index'] == None):
                                value['gfx_index'] = 'gfx_0'
                            if str(value['gfx_index']).lower() in self.adapter_display_dict.keys():
                                self.adapter_display_dict[str(value['gfx_index']).lower()].append(
                                    value['connector_port'])
                            else:
                                self.adapter_display_dict.update(
                                    {str(value['gfx_index']).lower(): [value['connector_port']]})
                            self.adapter_list.insert(value['index'], value['gfx_index'].lower())
                            self.input_display_list.insert(value['index'], (value['connector_port'],
                                                                            value['connector_port_type']))
                            self.panel_index[value['gfx_index'].lower() + "_" + value['connector_port']] = value['panel_index']

                # Set control variable based on command line options for CS/S3
                if (key == 'SLEEPSTATE'):
                    self.sleep_state = value[0].upper()

        logging.info(
            "Test Flow : Plug each Display Port in Low Power States [CS/S3] and Unplug the same port for next Plug in S4 and Monitor Turn OFF")
        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUp Method")

    ##
    # @brief        unittest to test the plug
    # @details      Plugs and unplugs every display in cmdline in low power state, for all CS/S3 and S4
    # @return       None
    def test_plug_all_ddi(self):
        logging.debug("Entry: test_plug_all_ddi()")
        step_count = 1
        for (display_port, port_connector_type), gfx_index in zip(self.input_display_list, self.adapter_list):
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display on adapter {}".format(display_port, gfx_index))
                continue
            else:
                # Verify Low Power State: S3 | CS
                cs_enabled = self.power.is_power_state_supported(display_power.PowerEvent.CS)
                if (self.sleep_state == "CS") and (cs_enabled is True):
                    logging.info("    STEP {} : Initiating Plug of {} Display in Low Power State CS on adapter {}".format(step_count,
                                                                                                            display_port, gfx_index))
                    lp_state = self.low_pow_state['CS_STATE']
                elif (self.sleep_state == "S3") and (cs_enabled is False):
                    logging.info("    STEP {} : Initiating Plug of {} Display in Low Power State S3 on adapter {}".format(step_count,
                                                                                                            display_port, gfx_index))
                    lp_state = self.low_pow_state['S3_STATE']
                else:
                    lp_state = None
                    actual_sleep_state = "CS" if cs_enabled else "S3"
                    logging.error(
                        "    STEP {} : DUT does not support Sleep State. Expected: {} Actual: {}".format(step_count,
                                                                                                         self.sleep_state,
                                                                                                         actual_sleep_state))
                step_count += 1
                # Plug Display in Low Power State CS/S3
                if lp_state is not None:
                    if self.plug_during_lowpower_state(port=display_port,
                                                       panel_index=self.panel_index.get(gfx_index + "_" + display_port),
                                                       lowpower_state=lp_state, hpd_mode=self.hpd_mode, gfx_index=gfx_index, port_connector_type=port_connector_type):
                        logging.info(
                            "Test Machine Went to {} and Resumed After 60s Successfully !!".format(self.sleep_state))
                        target_id= self.get_display_names(gfx_index)[display_port]
                        logging.info(
                            "    STEP {0} : Verifying Display Detection --> Resume from {1}, Display {2} (Target ID : {3}) Plug Successful during Low Power State {1} on adapter {4}".format(
                                step_count, self.sleep_state, display_port, target_id, gfx_index))
                    else:
                        logging.error(
                            "    STEP {0} : Verifying Display Detection --> Resume from {1}, Display {2} Plug Failed during Low Power State {1} on adapter {3}".format(
                                step_count, self.sleep_state, display_port, gfx_index))
                        self.fail()
                else:
                    self.fail()
                step_count += 1
                # Unplug display to plug back with next Power state
                logging.info("    STEP {} : Un-Plugging Display {} on adapter {}".format(step_count, display_port, gfx_index))
                step_count += 1
                if self.unplug_display(display_port, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                    logging.info(
                        "    STEP {} : Verifying Display Detection --> Display {} Unplug Successful on {}".format(step_count,
                                                                                                            display_port, gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection --> Display {} Unplug Failed on {}".format(step_count,
                                                                                                        display_port, gfx_index))
                    self.fail()
                step_count += 1
                # Verify Low Power State: S4
                logging.info("    STEP {} : Initiating Plug of {} on adapter {} in Low Power State S4".format(step_count,
                                                                                                        display_port, gfx_index))
                step_count += 1
                # Plug Display in Low Power State S4
                if self.plug_during_lowpower_state(port=display_port, panel_index=self.panel_index.get(gfx_index + "_" + display_port),
                                                   lowpower_state=self.low_pow_state['S4_STATE'], hpd_mode=self.hpd_mode, gfx_index=gfx_index, port_connector_type=port_connector_type):

                    logging.info("Test Machine Went to S4 and Resumed After 60s Successfully !!")
                    target_id = self.get_display_names(gfx_index)[display_port]
                    logging.info(
                        "    STEP {} : Verifying Display Detection --> Resume from S4, Display {} (Target ID : {}) Plug Successful during Low Power State S4 on adapter {}".format(
                            step_count, display_port, target_id, gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection --> Resume from S4, Display {} Plug Failed during Low Power State S4 on adapter {}".format(
                            step_count, display_port, gfx_index))
                step_count += 1
                logging.info("   STEP {} : Un-Plugging {} on {}".format(step_count, display_port, gfx_index))
                step_count += 1
                # Unplug display to plug back with next Power state
                if self.unplug_display(display_port, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                    logging.info(
                        "    STEP {} : Verifying Display Detection --> Display {} Unplug Successful on adapter {}".format(step_count,
                                                                                                            display_port, gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection --> Display {} Unplug Failed on adapter {}".format(step_count,
                                                                                                        display_port, gfx_index))
                    self.fail()
                step_count += 1
                # Verify with Monitor turn OFF
                if self.sleep_state == "S3":
                    logging.info(
                        "    STEP {} : Initiating Plug of {} Display on adapter {} in Low Power State Monitor Turn Off".format(
                            step_count, gfx_index, display_port))
                    step_count += 1
                    logging.debug("Entering Monitor Turnoff State for 60 sec")
                    # Plug Display in Low Power State Monitor Turn OFF
                    if self.plug_during_lowpower_state(port=display_port,
                                                       panel_index=self.panel_index.get(gfx_index + "_" + display_port),
                                                       lowpower_state=self.low_pow_state['MONITOR_TURNOFF'],
                                                       hpd_mode=self.hpd_mode, gfx_index=gfx_index, port_connector_type=port_connector_type):
                        logging.info(
                            "    STEP {} : Verifying Display Detection --> Resume from Monitor Turn Off, Display {} (Target ID : {}) Plug Successful during Low Power State Monitor Turn Off on adapter {}".format(
                                step_count, display_port, target_id, gfx_index))
                    else:
                        logging.error(
                            "    STEP {} : Verifying Display Detection --> Resume from Monitor Turn Off, Display {} Plug Failed during Low Power State Monitor Turn Off on adapter {}".format(
                                step_count, display_port, gfx_index))
            step_count += 1
        if (len(self.de_flag) < 1) or (False in self.de_flag):
            self.fail("Display Engine Verification Failed")

        logging.debug("Exit : test_plug_all_ddi()")


    ##
    # @brief        teardown function
    # @details      Unplugs all the displays connected in the test
    # @return       None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.debug("Unplugging all Displays")
        enum_display_list = self.config.get_enumerated_display_info()

        for count in range(enum_display_list.Count):
            connector_port = CONNECTOR_PORT_TYPE(enum_display_list.ConnectedDisplays[count].ConnectorNPortType).name
            gfx_index = enum_display_list.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI] and connector_port not in [
                'DispNone', 'VIRTUALDISPLAY']:
                self.unplug_display(connector_port, hpd_mode=self.hpd_mode, de_verification=False, gfx_index=gfx_index)

        logging.info("Test Completed")
        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PlugAllDDIInLowPower'))
    TestEnvironment.cleanup(outcome)
