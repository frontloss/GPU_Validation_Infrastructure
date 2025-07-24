#######################################################################################################################
# @file         test_asymmetric.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in asymmetric Dual eDP non PSR scenario,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with Asymmetric config
class TestAsymmetric(PortSyncBase):

    ##
    # @brief        this function verifies port sync in asymmetric config
    # @return       None
    def t_10_test_asymmetric(self):
        self.verify_basic()

    ##
    # @brief        this function verifies port sync in asymmetric config
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels, expected_port_sync=False) is True:
                logging.info("\tPort sync programming verification successful")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestAsymmetric))
    test_environment.TestEnvironment.cleanup(test_result)