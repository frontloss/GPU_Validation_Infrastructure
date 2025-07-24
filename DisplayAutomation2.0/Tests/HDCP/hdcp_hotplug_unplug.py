#######################################################################################################################
# @file         hdcp_hotplug_unplug.py
# @brief        HDCP verification using hot plug & unplug with external display
# @details      Test for verifying HDCP 1.4 & 2.2 activation & deactivation with external display hot unplug & plug
#               using OPM tool
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with display unplug & plug
class HDCPHotplugUnplug(HDCPBase):
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
            self.fail("Internal display interface EDP or MIPI not enumerated")

        ##
        # Remove Internal display from display list
        [self.display_list.remove(display) for display in self.internal_display if display in self.display_list]

    ##
    # @brief        Method to reboot with SD HDMI/DP
    # @return       None
    def test_reboot_with_ExtDisplay(self):

        self.remove_internal_display()
        ##
        # Set display configuration to SINGLE
        if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                            [self.display_list[0]], self.enumerated_displays) is False:
            self.fail("Failed to apply single display configuration on display {}".format(self.display_list[0]))

        if reboot_helper.reboot(self, 'test_verify_hdcp') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Method to verify HDCP with hot unplug & plug using North gate
    # @return       None
    def test_verify_hdcp(self):
        self.plugged_display = []
        self.config_display_list = []

        self.remove_internal_display()
        ##
        # Set display configuration to SINGLE
        if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                            [self.display_list[0]], self.enumerated_displays) is False:
            self.fail("Failed to apply single display configuration on display {}".format(self.display_list[0]))
        ##
        # Connected displays list; used for applying display configurations
        self.config_display_list = self.internal_display

        for index, display in enumerate(self.display_list):
            ##
            # Maintaining plugged_display list for unplugging displays
            self.plugged_display.append(display)
            self.config_display_list.append(display)

            if index == 0:
                # HDCP session create
                status = self.single_display_single_session(disable=False)
                if status is True:
                    logging.info('HDCP Enabled successfully')
            else:
                # Ask user to hotplug the display
                if self.manual_hot_unplug_plug(display) is False:
                    self.fail('Plugging of display %s was unsuccessful' % display)
                # wait for OPM Tool to re-initialize
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

                ##
                # Apply display configuration on the plugged displays based on command dictionary
                config = eval('enum.%s' % self.cmd_line_param['CONFIG'])
                if self.display_config.set_display_configuration_ex(config, self.config_display_list) is False:
                    if len(self.plugged_display) > 1:
                        self.fail("Failed to apply display configuration")
                # wait for OPM Tool to re-initialize
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

                ##
                # Verify HDCP activation
                if self.enable_hdcp(self.config_display_list.index(display)) is False:
                    self.fail(" HDCP Enable Failed")
                logging.info('HDCP Enable passed successfully')
                # wait for 30 sec to ensure no Linklost occurred
                time.sleep(HDCP_ENABLE_CHECK_DURATION)
        ##
        # Unplug displays one by one and verify HDCP activation/deactivation
        logging.info(" Unplugging the Displays one by one and verifying HDCP ..")
        for display in reversed(self.display_list):
            ##
            # Unplug the display
            if self.manual_hot_unplug(display) is False:
                self.fail("Failed to unplug display {} ".format(display))
            # wait for OPM Tool to re-initialize
            time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

            self.plugged_display.remove(display)

            self.config_display_list.remove(display)
            if not self.plugged_display:
                if self.display_config.set_display_configuration_ex(enum.SINGLE, self.internal_display,
                                                                    self.enumerated_displays) is False:
                    self.fail("Failed to apply SINGLE %s display configuration as " % self.internal_display)
            else:
                ##
                # Apply display configuration on the plugged displays based on command dictionary
                config = eval('enum.%s' % self.cmd_line_param['CONFIG'])
                if self.display_config.set_display_configuration_ex(config, self.config_display_list) is False:
                    self.fail("Failed to apply display configuration")
                # wait for OPM Tool to re-initialize
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
                logging.info("unplugged the {} display".format(display))

                ##
                # Verify HDCP protection level
                for port in self.plugged_display:
                    if self.enable_hdcp(self.config_display_list.index(port)) is False:
                        self.fail(" HDCP not enabled on port {}".format(port))
                    logging.info('HDCP verification passed successfully for %r' % port)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HDCPHotplugUnplug'))
    TestEnvironment.cleanup(outcome)
