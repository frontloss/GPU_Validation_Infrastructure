########################################################################################################################
# @file         port_sync_with_power_events.py
# @brief        This file contains LFP Port Sync tests with Power Events.
# @details      After waking from power events, driver brings up each display sequentially;
#               here port sync should be reestablished. Verify port sync after this scenario.
# @author       Sri Sumanth Geesala
########################################################################################################################
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.Port_Sync.port_sync_base import *


##
# @brief       This class contains basic LFP Port Sync tests before and after reboot with power events
class PortSyncWithPowerEvents(PortSyncBase):

    ##
    # @brief        This test function verifies LFP Port Sync before with the invocation of different power events
    # @return       None
    def test_before_reboot(self):

        # verify port sync before scenario
        logging.info('Step :\t Check for port sync initially')
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        # Perform CS/S3 power event and check MIPI status
        logging.info('Step :\t Perform CS/S3 power event and check for port sync')
        if self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
            logging.info("Performing CS power event and checking dual LFP port sync")
            power_state = self.display_power.invoke_power_event(display_power.PowerEvent.CS, 60)
            if power_state is True:
                self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()
        else:
            logging.info("Performing S3 power event and checking dual LFP port sync")
            power_state = self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60)
            if power_state is True:
                self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        logging.info('Step :\t Perform S4 power event and check for port sync')
        power_state = self.display_power.invoke_power_event(display_power.PowerEvent.S4, 60)

        if power_state is True:
            self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        logging.info('Step :\t Perform S5 power event and check for port sync')
        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This test function verifies LFP Port Sync after reboot and reports if any failure is found
    # @return       None
    def test_after_reboot(self):
        logging.info("After Reboot")
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        # report test failure if any verifications failed
        if self.test_result == False:
            self.fail('Some checks in the test have failed. Check ERROR logs.')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PortSyncWithPowerEvents'))
    TestEnvironment.cleanup(results)
