#######################################################################################################################
# @file                 elp_with_invalid_opt_levels.py
# @brief                This test script is a basic script where optimization levels are applied
#                       in both increasing and decreasing orders. Read of DPCD address 0x358
#                       to verify if the optimization levels are set correctly
# Sample CommandLines:  python elp_with_invalid_opt_levels.py -edp_a SINK_EDP076 -opt_level 3
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ELP.elp_test_base import *


class elpWithInvalidOptLevels(ELPTestBase):
    ##
    # @brief - ELP Stress test
    def test_01_basic(self):
        # ##
        # # Enable ELP on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 3 : Setting invalid Optimization Levels and verify ELP persistence***")
        logging.info("Invalid Optimization Level requested is : 8")
        if self.enable_elp_optimization_and_verify(level=8):
            self.fail()

        logging.info("Invalid Optimization Level requested is : -5")
        if self.enable_elp_optimization_and_verify(level=-5):
            self.fail()

        logging.info("Optimization Level requested is : 0")
        if self.enable_elp_optimization_and_verify(level=0) is False:
            self.fail()

        logging.info("Optimization Level requested is {0}".format(self.user_opt_level))
        if self.enable_elp_optimization_and_verify(level=self.user_opt_level) is False:
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels by setting the opt level provided by User;"
        "Also, set invalid Opt levels and verify the behavior")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
