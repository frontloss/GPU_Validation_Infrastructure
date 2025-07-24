#################################################################################################################
# @file         drrs_basic.py
# @brief        Contains DRRS basic test
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DRRS.drrs_base import *

##
# @brief       This class contains basic tests for DRRS


class DrrsBasicTest(DrrsBase):

    ##
    # @brief        Basic test to verify DRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic(self):
        self.verify_drrs(wm_during_rr_switch=True)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsBasicTest))
    test_environment.TestEnvironment.cleanup(test_result)
