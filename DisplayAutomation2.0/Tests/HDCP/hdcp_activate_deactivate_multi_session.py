#######################################################################################################################
# @file         hdcp_activate_deactivate_multi_session.py
# @brief        HDCP activate & deactivate verification with multi session
# @details      Test for verifying HDCP 1.4 & 2.2 activation & deactivation with multiple sessions using OPM tool
#
# @author       Sridharan.V, Kumar Rohit, chandrakanth Reddy y
#######################################################################################################################


from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with multiple OPM sessions
class HDCPActivateDeactivateMultiSession(HDCPBase):

    ##
    # @brief        Method to verify HDCP with Multi session
    # @return       None
    def test_multisession(self):
        status = False
        ##
        # set configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail(
                "FAIL: Failed to apply display configuration {} on displays {}".format(self.cmd_line_param['CONFIG'],
                                                                                       self.display_list))
        # Wait time for OPM to re-initialize the session
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        ##
        # Verify HDCP activation/deactivation
        logging.info("HDCP Verification started ....")
        if len(self.display_list) == 1:
            status = self.single_display_multi_session()
        elif len(self.display_list) > 1:
            status = self.multi_display_multi_session()

        if status is False:
            self.fail('HDCP verification failed')
        logging.info('HDCP verification passed successfully')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
