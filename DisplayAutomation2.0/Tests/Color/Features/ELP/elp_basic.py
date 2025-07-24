#######################################################################################################################
# @file                 elp_basic.py
# @brief                This test script is a basic script where optimization levels are applied
#                       in both increasing and decreasing orders. Read of DPCD address 0x358
#                       to verify if the optimization levels are set correctly
# Sample CommandLines:  python elp_basic.py -edp_a SINK_EDP076 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ELP.elp_test_base import *


class elpBasic(ELPTestBase):

    ##
    # @brief - ELP Stress test
    def test_01_basic(self):
        # ##
        # # Enable ELP on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels by iterating through all the optimization levels"
        " in both increasing and decreasing orders"
        " and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
