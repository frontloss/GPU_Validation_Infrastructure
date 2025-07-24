#######################################################################################################################
# @file         hdcp_hotplug_unplug_power_event.py
# @brief        HDCP verification using hot plug & unplug with external display
# @details      Test for verifying HDCP 1.4 & 2.2 activation & deactivation with external display hot unplug & plug
#               using OPM tool with Power events (CS/S3/S4/MonitorPower)
#
# @author       chandrakanth Reddy y
##################################################################################################################

from Libs.Core import enum
from Libs.Core.display_power import PowerEvent, MonitorPower
from Tests.HDCP.hdcp_base import *



##
# @brief        Contains HDCP tests with display unplug & plug
class HDCPHotplugUnplugPowerEvent(HDCPBase):
    plugged_display = []
    internal_display = []

    ##
    # @brief        Method to remove LFP displays from display list
    # @return       None
    def remove_internal_display(self):
        self.internal_display = []

        internal_display_list = self.display_config.get_internal_display_list(self.enumerated_displays)

        # get edp/mipi PortName
        if len(internal_display_list) != 0:
            for i in range(len(internal_display_list)):
                self.internal_display.append(internal_display_list[i][1])
        else:
            logging.error("Internal display interface EDP or MIPI not enumerated")
            self.fail("Internal display missing")

        ##
        # Remove Internal display from display list
        [self.display_list.remove(display) for display in self.internal_display if display in self.display_list]

    ##
    # @brief        Method to reboot system with SD EDP
    # @return       None
    def test_reboot_with_EDP(self):

        # Verify CS/Non-CS system
        if self.display_power.is_power_state_supported(PowerEvent.CS) is not self.is_cs_system_expected:
            logging.error(
                " Current System configuration is CS = %s which is not expected" % (not self.is_cs_system_expected))
            self.fail("System configuration mismatch")

        self.remove_internal_display()
        ##
        # Set display configuration to SINGLE Display EDP & reboot 
        if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                            [self.internal_display[0]],
                                                            self.enumerated_displays) is False:
            self.fail("Failed to apply display configuration")

        if reboot_helper.reboot(self, 'test_verify_hdcp_power_event') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Method to verify HDCP with power event after display plug
    # @return       None
    def test_verify_hdcp_power_event(self):
        self.plugged_display = []
        config_display_list = []

        self.remove_internal_display()
        ##
        # Set display configuration to SINGLE Display EDP
        if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                            [self.internal_display[0]],
                                                            self.enumerated_displays) is False:
            self.fail("Failed to apply display configuration")
        ##
        # Connected displays list; used for applying display configurations
        config_display_list = self.internal_display

        ##
        # Plug displays one by one and verify HDCP activation/deactivation
        for index, display in enumerate(self.display_list):
            if self.manual_hot_unplug_plug(display) is False:
                self.fail('Plugging of display %s was unsuccessful' % display)
            ##
            # Maintaining plugged_display list for unplugging displays
            self.plugged_display.append(display)
            config_display_list.append(display)

            ##
            # Apply display configuration on the plugged displays based on command dictionary
            config = eval('enum.%s' % self.cmd_line_param['CONFIG'])
            if self.display_config.set_display_configuration_ex(config, config_display_list) is False:
                self.fail("Failed to apply display configuration after Display plug")
            # wait for OPM Tool to re-initialize
            time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
            if len(self.plugged_display) == 1:
                # HDCP session create
                if self.multi_display_single_session(disable=False) is False:
                    self.fail(" Failed to Enable HDCP")
                logging.info('HDCP Enabled successfully')
            else:
                # Verify HDCP activation
                if self.enable_hdcp(config_display_list.index(display)) is False:
                    self.fail('Failed to Enable HDCP')
                logging.info('HDCP Enable passed successfully')
                # wait for sometime to ensure no link lost occurred.
                time.sleep(HDCP_ENABLE_CHECK_DURATION)

        # Invoke Power Event
        if self.is_monitor_turn_off:
            result = self.display_power.invoke_monitor_turnoff(self.power_event, POWER_EVENT_DURATION)
            power_event = self.power_event.name
        else:
            result = self.display_power.invoke_power_event(self.power_event, POWER_EVENT_DURATION)
            power_event = self.power_event.name

        if result is False:
            self.fail("Failed to invoke power event %r" % power_event)

        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        ##
        # Verify HDCP activation
        for display in self.plugged_display:
            if self.enable_hdcp(config_display_list.index(display)) is False:
                self.fail('HDCP Enable after Power event failed')
            logging.info('HDCP verification after Power Event passed successfully')

        ##
        # Unplug displays one by one and verify HDCP activation/deactivation
        for display in reversed(self.display_list):
            ##
            # Unplug the display
            if self.manual_hot_unplug(display) is False:
                self.fail("Failed to unplug display {}".format(display))
            self.plugged_display.remove(display)
            config_display_list.remove(display)

            if not self.plugged_display:
                if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                                    [self.internal_display[0]],
                                                                    self.enumerated_displays) is False:
                    self.fail("Failed to apply SD on {} ".format(self.internal_display))
            else:
                ##
                # Apply display configuration on the plugged displays based on command dictionary
                config = eval('enum.%s' % self.cmd_line_param['CONFIG'])
                if self.display_config.set_display_configuration_ex(config, config_display_list) is False:
                    self.fail("FAIL: Failed to apply display configuration {} on displays {}".format(
                        self.cmd_line_param['CONFIG'], self.display_list))
                # wait for OPM Tool to re-initialize
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

                ##
                # Verify HDCP Protection level on Un-plugged ports
                for port in self.plugged_display:
                    if self.enable_hdcp(config_display_list.index(port)) is False:
                        self.fail('HDCP verification failed on Un-plugged ports')
                    logging.info('HDCP verification passed successfully')
                time.sleep(HDCP_ENABLE_CHECK_DURATION)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HDCPHotplugUnplugPowerEvent'))
    TestEnvironment.cleanup(outcome)
