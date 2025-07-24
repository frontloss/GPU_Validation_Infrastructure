######################################################################################
# @file         port_sync_basic.py \n
# @brief        Verify port sync between 2 LFPs in basic scenario
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.Port_Sync.port_sync_base import *


##
# @brief       This class contains basic LFP Port Sync tests between 2 attached LFP's
class PortSyncBasic(PortSyncBase):

    ##
    # @brief        This function verifies LFP Port Sync in basic scenario
    # @return       None
    def runTest(self):
        logging.info('Step :\t Check for port sync initially')
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback()

        # report test failure if any verifications failed
        if self.test_result == False:
            self.fail('Some checks in the test have failed. Check ERROR logs.')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
