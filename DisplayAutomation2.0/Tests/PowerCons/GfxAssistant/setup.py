#######################################################################################################################
# @file         setup.py
# @brief        (to be completed)
#
# @author       Ashish Tripathi, Rohit Kumar
#######################################################################################################################

import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief        This is a test class. It contains blank setup and teardown methods. It contains blank tests
class GfxAssistantTriageSetup(unittest.TestCase):
    ##
    # @brief        This is the blank setup function
    # @return       None
    def setUp(self) -> None:
        pass

    ##
    # @brief        This is the blank teardown function
    # @return       None
    def tearDown(self) -> None:
        pass

    ##
    # @brief        This is the blank test function
    # @return       None
    def runTest(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
