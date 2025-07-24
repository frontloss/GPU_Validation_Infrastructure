########################################################################################################################
# @file         mpo_ui_basic.py
# @brief        Basic test method for validating common test base
# @author       Gurusamy, Balaji
########################################################################################################################

from Tests.Planes.Common.mpo_ui_base import *
from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief    MPO UI Basic class
class MPOUIBasic(MPOUIBase):

    ##
    # @brief            basic test method
    # @return           None
    def test_01_basic(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO getting enabled for given display with given application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
