#######################################################################################################################
# @file         hdcp_power_event.py
# @brief        hdcp verification with power event
# @details      Test for verifying HDCP 1.4 & 2.2 activation/deactivation before
#               and after power event(S3,CS,S4,MonitorTurnOFF)
#
# @author       chandrakanth Reddy y
#######################################################################################################################


from Libs.Core.display_power import PowerEvent, MonitorPower
from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with power events
class HDCPPowerEvent(HDCPBase):
    display_count = []

    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):

        # Verify CS/Non-CS system
        if self.display_power.is_power_state_supported(PowerEvent.CS) is not self.is_cs_system_expected:
            logging.error("System configuration as CS = {} was not expected".format((not self.is_cs_system_expected)))
            self.fail("Expected system configuration CS = {}".format(self.is_cs_system_expected))

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology,
                                                            self.display_list, self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display config {0} on displays {1}".format(self.cmd_line_param['CONFIG'],
                                                                                        self.display_list))
        # Wait time for OPM to re-initialize the session
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        # Get the HDCP display list
        display_count = [self.display_list.index(port) for port in self.display_list if
                         display_utility.get_vbt_panel_type(port, 'gfx_0') not in
                         [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        status = False
        ##
        # Verify HDCP activation/deactivation
        logging.info("HDCP Verification started ....")
        if len(self.display_list) == 1:
            status = self.single_display_single_session()
        elif len(self.display_list) > 1:
            status = self.multi_display_single_session()

        # Verify HDCP activation/deactivation
        if status is False:
            self.fail('HDCP verification before power event failed ')
        logging.info('HDCP verification before power event passed successfully ')
        # wait to ensure no Link lost occurred
        time.sleep(HDCP_ENABLE_CHECK_DURATION)

        # Invoke Power Event
        if self.is_monitor_turn_off:
            result = self.display_power.invoke_monitor_turnoff(self.power_event, POWER_EVENT_DURATION)
            power_event = self.power_event.name
        else:
            result = self.display_power.invoke_power_event(self.power_event, POWER_EVENT_DURATION)
            power_event = self.power_event.name
        if result is False:
            self.fail('Failed to invoke sleep state {}'.format(power_event))
        # Wait time for OPM to get Re-initialize
        time.sleep(15)

        ##
        # Verify HDCP activation/deactivation
        logging.info(" HDCP Verification start after Power event ...")
        if len(self.display_list) > 1:
            for port in display_count:
                status = self.enable_hdcp(port)
        else:
            # for single display , Port number is not required
            status = self.enable_hdcp()
        if status is False:
            self.fail('HDCP verification after power event failed')
        logging.info('HDCP verification after Power event passed successfully')
        time.sleep(10)

        # Disable HDCP
        if len(self.display_list) > 1:
            for port in display_count:
                status = self.disable_hdcp(port)
        else:
            # for single display , Port number is not required
            status = self.disable_hdcp()
        if status is False:
            self.fail("HDCP Disable Failed")
        logging.info("HDCP Disable successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
