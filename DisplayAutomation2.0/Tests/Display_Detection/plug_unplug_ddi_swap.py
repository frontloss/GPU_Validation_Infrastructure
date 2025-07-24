########################################################################################################################
# @file         plug_unplug_ddi_swap.py
# @brief        Validate display hot plug and unplug during low power mode and plug in all supported DDI
#               displays are edp_a, dp_b, dp_c, hdmi_b, hdmi_c, etc
# @details      This test_script follows:
#               1. Hot Plug Displays passed in command-line arguments except Internal Display
#               2. Unplug Display1 (DP_portname) and if HDMI_portname in supported ports
#               3. plug HDMI_portname during CS/S3 mode
#               4. Unplug HDMI_portname and plug Display1 (DP_portname) during CS/S3 mode
#               5. Unplug Display1 (DP_portname) and plug HDMI_portname during S4 mode
#               6. Unplug HDMI_portname and plug Display1 (DP_portname) during S4 mode
#               7. Continues above steps(1 to 6) for other Displays mentioned in cmd line.
#               CommandLine: python plug_unplug_ddi_swap.py [-eDP_A][-DP_B][-DP_C][-DP_D] -sleepstate cs/s3
#               Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
# @author       Raghupathy, Dushyanth Kumar, Balaji Gurusamy
########################################################################################################################
import sys

from Libs.Core import cmd_parser, reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Detection.display_hpd_base import *

##
# @brief        PlugUnplugOneByOneDdiSwapInPm base class : To be used in Display Detection tests
class PlugUnplugOneByOneDdiSwapInPm(DisplayHPDBase):

    ##
    # @brief        setup function. Parse displays to plug and hpd_mode from cmdline params
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUp Method")

        # Variable Initializing
        self.input_display_list = []
        self.adapter_list = []
        self.panel_index = {}
        self.hdmi_display = None
        self.hpd_mode = None
        self.low_power_mode = None
        self.low_power_state = None

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
                            self.input_display_list.insert(value['index'], value['connector_port'])
                            self.panel_index[value['gfx_index'].lower() + "_" + value['connector_port']] = value['panel_index']

                # Set control variable based on command line options for CS/S3
                if (key == 'SLEEPSTATE'):
                    self.sleep_state = value[0].upper()

        # Verify Low Power State: S3 | CS
        cs_enabled = self.power.is_power_state_supported(display_power.PowerEvent.CS)
        if (self.sleep_state == "CS") and (cs_enabled is True):
            self.low_power_mode = "CS"
        elif (self.sleep_state == "S3") and (cs_enabled is False):
            self.low_power_mode = "S3"
        else:
            actual_sleep_state = "CS" if cs_enabled else "S3"
            logging.error("DUT does not support Sleep State. Expected: {0} Actual: {1}".format(
                self.sleep_state, actual_sleep_state))

        logging.info(
            "Test Flow : Plug DP Port given, UnPlug DP and Plug HDMI on same port in Low Power State, vice-versa")
        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUp Method")


    ##
    # @brief        unittest to test the plug
    # @details      Plugs and unplugs every display in cmdline in low power state,
    #               for all CS/S3 and S4 and repeat the same for all DDIs
    # @return       None
    def test_plug_unplug_swap(self):
        """
        Description:
        This test step as follows:
            Unplug Display1 (DP_portname) and if HDMI_portname in supported ports
            plug HDMI_portname during CS/S3 mode
            Unplug HDMI_portname and plug Display1 (DP_portname) during CS/S3 mode
            Unplug Display1 (DP_portname) and plug HDMI_portname during S4 mode
            Unplug HDMI_portname and plug Display1 (DP_portname) during S4 mode
            Follows above scenarios for displays in input_display_list
        :return: None
        """
        logging.debug("Entry: test_plug_unplug_swap()")
        step_count = 1

        if self.hpd_mode == "EMU":
            self.fail("Displays DP and HDMI plug/unplug on same port is not yet enabled on HW Emulator")
        # Plug all displays in input_display_list
        for display_port, gfx_index in zip(self.input_display_list, self.adapter_list):
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                    display_utility.VbtPanelType.LFP_MIPI] or "HDMI" in display_port:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display on adapter {}".format(display_port, gfx_index))
                continue
            else:
                logging.info("    STEP {} : Plugging Display on {}".format(step_count, display_port))
                step_count += 1
                if self.plug_display(port=display_port, panel_index=self.panel_index.get(gfx_index + "_" + display_port),
                                     hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                    enum_display_dict = self.get_display_names(gfx_index)
                    logging.info(
                        "    STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful on adapter {}".format(
                            step_count, display_port, enum_display_dict[display_port], gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection -->Display {} Plug Failed".format(step_count,
                                                                                                     display_port))
            step_count += 1

        for display_port, gfx_index in zip(self.input_display_list, self.adapter_list):
            # v: Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display".format(display_port))
                continue
            for power_state in [self.low_power_mode, "S4"]:
                if power_state == "CS":
                    self.low_power_state = display_power.PowerEvent.CS
                if power_state == "S3":
                    self.low_power_state = display_power.PowerEvent.S3
                if power_state == "S4":
                    self.low_power_state = display_power.PowerEvent.S4

                self.get_supported_ports = display_config.get_supported_ports(gfx_index)
                self.hdmi_display = "HDMI_" + str(display_port[-1])

                if not self.hdmi_display in self.get_supported_ports:
                    logging.error(
                        "VBT settings has some issue, couldn't find {} in supported ports".format(self.hdmi_display))

                # Unplug of DP_portname and plug HDMI_portname during CS/S3/S4
                displays = [display_port, self.hdmi_display]

                logging.info(
                    "STEP {} : Initiating UnPlug of {} and Plug of {} Display ( on Same Port : Swapping {} with {} "
                    "Panel in Low Power State {} on adapter {})".format(
                        step_count, displays[0], displays[1], displays[0], displays[1], power_state, gfx_index))
                step_count += 1
                if self.unplug_during_lowpower_state(port=displays[0], lowpower_state=None, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                    time.sleep(10)
                    if self.plug_during_lowpower_state(port=displays[1], panel_index=self.panel_index.get(gfx_index + "_" + displays[1]),
                                                       lowpower_state=self.low_power_state, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                        logging.info(
                            "Test Machine Went to {} and Resumed After 60s Successfully !!".format(power_state))
                        logging.info(
                            "    STEP {} : Verifying Display Detection --> Resume from {}, UnPlug of {} and Plug of {} Display during Low Power State {} Successful on adapter {}".format(
                                step_count, power_state, displays[0], displays[1], power_state, gfx_index))
                    else:
                        logging.error(
                            "    STEP {} : Verifying Display Detection --> Resume from {}, Display {} Plug After {} Failed on adapter {}".format(
                                step_count, power_state, displays[1], power_state, gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection --> Resume from {}, Display {} Unplug After {} Failed on adapter {}".format(
                            step_count, power_state, displays[0], power_state, gfx_index))
                time.sleep(5)
                step_count += 1
                # Plug of DP_portname and Unplug HDMI_portname during CS/S3/S4
                logging.info(
                    "    STEP {} : Initiating Plug of {} and UnPlug of {} Display ( on Same Port : Swapping {} with {} Panel in Low Power State {} )".format(
                        step_count, displays[0], displays[1], displays[1], displays[0], power_state))
                step_count += 1
                if self.unplug_during_lowpower_state(port=displays[1], lowpower_state=None, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                    time.sleep(10)
                    if self.plug_during_lowpower_state(port=displays[0], panel_index=self.panel_index.get(gfx_index + "_" + displays[0]),
                                                       lowpower_state=self.low_power_state, hpd_mode=self.hpd_mode, gfx_index=gfx_index):
                        logging.info(
                            "Test Machine Went to {} and Resumed After 60s Successfully !!".format(power_state))
                        logging.info(
                            "    STEP {} : Verifying Display Detection --> Resume from {}, Plug of {} and UnPlug of {} Display during Low Power State {} Successful on adapter {}".format(
                                step_count, power_state, displays[0], displays[1], power_state, gfx_index))
                    else:
                        logging.error(
                            "    STEP {} : Verifying Display Detection --> Resume from {}, Display {} Plug After {} Failed on adapter {}".format(
                                step_count, power_state, displays[0], power_state, gfx_index))
                else:
                    logging.error(
                        "    STEP {} : Verifying Display Detection --> Resume from {}, Display {} UnPlug After {} Failed on adapter {}".format(
                            step_count, power_state, displays[1], power_state, gfx_index))
                step_count += 1
            step_count += 1

        if (len(self.de_flag) < 1) or (False in self.de_flag):
            self.fail("Display Engine Verification Failed")

        logging.debug("Exit: test_plug_unplug_swap()")

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
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PlugUnplugOneByOneDdiSwapInPm'))
    TestEnvironment.cleanup(outcome)
