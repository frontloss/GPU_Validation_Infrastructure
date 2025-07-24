######################################################################################
# @file         port_sync_turn_off_on_second_lfp.py \n
# @brief        This file contains tests for LFP port when the second LFP is turned off and on
# @brief        When second LFP turned off and on, port sync should be reestablished.
#               Verify port sync after this scenario.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.Port_Sync.port_sync_base import *


##
# @brief       This class contains basic LFP Port Sync tests when second LFP is turned off and then turned on
class PortSyncTurnOffOnSecondLfp(PortSyncBase):

    ##
    # @brief        This test function verifies LFP Port Sync before the second display is turned off
    #               and after it is turned
    #               on
    # @return       None
    def runTest(self):

        # verify port sync before scenario
        logging.info('Step :\t Check for port sync initially')
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        for iteration in range(5):
            logging.info('***********Iteration {0}*************'.format(iteration))
            for lfp in self.lfps_in_cmdline:
                # turn off second LFP by applying SD config and again turn on second LFP by applying clone config
                logging.info('Step :\t Turn off one LFP by applying SD config, again turn on second LFP by applying '
                             'clone config and check for port sync')
                result = self.display_config.set_display_configuration_ex(enum.SINGLE, [lfp],
                                                                          self.enumerated_displays)
                self.assertNotEquals(result, False, "Aborting the test as applying SINGLE {0} config failed."
                                     .format(lfp))

                result = self.display_config.set_display_configuration_ex(enum.CLONE, [self.lfps_in_cmdline[0],
                                                                                       self.lfps_in_cmdline[1]],
                                                                          self.enumerated_displays)
                self.assertNotEquals(result, False, "Aborting the test as applying CLONE {0} + {1} config failed."
                                     .format(self.lfps_in_cmdline[0], self.lfps_in_cmdline[1]))

                # verify port sync after scenario
                self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        # report test failure if any verifications failed
        if self.test_result == False:
            self.fail('Some checks in the test have failed. Check ERROR logs.')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
