#######################################################################################################################
# @file         hdcp_activate_deactivate.py
# @brief        HDCP activate & deactivate verification
# @details      Test for verifying HDCP 1.4 & 2.2 activation & deactivation with reboot using OPM tool
#
# @author       Sridharan.V, Kumar Rohit, chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP test verification using OPM tool
class HDCPActivateDeactivate(HDCPBase):
    ##
    # @brief        Method to verify HDCP on external panel
    # @return       None
    def verify_hdcp(self):
        # Verify HDCP activation on Multi-port
        status = self.multi_display_single_session(disable=False)
        if status is False:
            self.fail('HDCP verification failed')
        else:
            logging.info('HDCP verification passed successfully')

    ##
    # @brief        Method to verify HDCP before reboot
    # @return       None
    def test_before_reboot(self):
        logging.info("--------------------- HDCP verification before Reboot--------------------- ")
        ##
        # set configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail(
                "FAIL: Failed to apply display configuration {} on displays {}".format(self.cmd_line_param['CONFIG'],
                                                                                       self.display_list))
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
        self.verify_hdcp()

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Method to verify HDCP after reboot
    # @return       None
    def test_after_reboot(self):
        logging.info("--------------------- HDCP verification After Reboot--------------------- ")
        ##
        # Apply display configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail(
                "FAIL: Failed to apply display configuration {} on displays {}".format(self.cmd_line_param['CONFIG'],
                                                                                       self.display_list))
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
        if self.multi_display_single_session() is False:
            self.fail('HDCP Enable failed for Iteration 1')
        logging.info('HDCP Enabled successfully for Iteration 1')

        # get the HDCP display list
        display_count = [self.display_list.index(port) for port in self.display_list if
                         display_utility.get_vbt_panel_type(port, 'gfx_0') not in
                         [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        for i in range(4):
            # disable HDCP 
            for port in display_count:
                if self.disable_hdcp(port) is False:
                    self.fail("HDCP Disable Failed for iteration {}".format(i + 1))
                logging.info("HDCP Disable successful for iteration {}".format(i + 1))

            # Verify HDCP Protection level for 4 iterations
            for port in display_count:
                if self.enable_hdcp(port) is False:
                    self.fail('HDCP Enable failed for iteration {}'.format(i + 2))
                logging.info('HDCP Enabled successfully for iteration {}'.format(i + 2))

            # wait for some time to ensure no linklost occured
            time.sleep(HDCP_ENABLE_CHECK_DURATION)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HDCPActivateDeactivate'))
    TestEnvironment.cleanup(outcome)
