#######################################################################################################################
# @file         hdcp_displayswitch.py
# @brief        HDCP activate & deactivate verification with display switch
# @details      Test for verifying HDCP 1.4 & 2.2 verification with each display config to SD, DDC, ED, TED, TDC
#               using OPM tool
#
# @author       Sridharan.V, Kumar Rohit, chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with display switching
class HDCPDisplaySwitch(HDCPBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        display_count = []
        platforms = []
        temp = []
        connected_displays = []

        if len(self.display_list) < 2:
            self.fail("Display Switch test case needs minimum 2 displays")

        current_config = self.display_config.get_current_display_configuration_ex()
        logging.info("current display config is {0}:{1}".format(current_config[0], current_config[1]))
        ##
        # Verify HDCP activation/deactivation
        if self.multi_display_single_session(disable=False) is False:
            self.fail('HDCP Verification Failed')
        logging.info('HDCP Enabled successfully')

        self.config_list = display_utility.get_possible_configs(self.display_list)
        for config, display_list in self.config_list.items():
            topology = eval("%s" % config)

            # remove the repeated configurations from the display list
            if config != "enum.SINGLE":
                for displays in display_list:
                    displays.sort()
                    if displays not in temp:
                        temp.append(displays)
                display_list = temp

            for displays in display_list:
                connected_displays = displays
                logging.info("displays = %r & config = %r" % (displays, config))
                if self.display_config.set_display_configuration_ex(topology, displays,
                                                                    self.enumerated_displays) is False:
                    self.fail("Display switching: {} Failed for displays {}".format(config, displays))
                # wait for OPM Tool to re-initialize
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
                display_count = [port for port in displays if display_utility.get_vbt_panel_type(port, 'gfx_0')
                                 not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
                for port in display_count:
                    if len(displays) == 1:
                        status = self.enable_hdcp(None)
                    else:
                        if self.enable_hdcp(displays.index(port)) is False:
                            self.fail("HDCP Verification Failed on Port {} after Display switch ".format(port))
                        logging.info("HDCP protection level verified successfully")

                    # wait to ensure no link lost occurred
                    time.sleep(HDCP_ENABLE_CHECK_DURATION)

        for port in display_count:
            if len(connected_displays) == 1:
                status = self.disable_hdcp()
            else:
                status = self.disable_hdcp(connected_displays.index(port))
            if status is True:
                logging.info('HDCP Disabled successfully for port %r' % port)
            else:
                self.fail("HDCP not Disabled on port {}".format(port))

        # set the config to initial config state before exit the test case(enum.EXTENDED)
        prev_config = eval("enum.%s" % current_config[0])
        if self.display_config.set_display_configuration_ex(prev_config, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("Display switching to {0}:{1} is Failed".format(current_config[0], current_config[1]))
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
