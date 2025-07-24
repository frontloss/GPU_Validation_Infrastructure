########################################################################################################################
# @file         planes_ui_yt.py
# @brief        The test script
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI import planes_ui_base
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI.Common import yt_scenarios


##
# @brief    Contains basic PlanesUI tests
class PlanesUIYT(planes_ui_base.PlanesUIBase):
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'YOUTUBE',
                     "Skip the test step as the scenario type is not YOUTUBE")
    ##
    # @brief        Test to execute stress scenarios
    # @return       None
    def test_01_youtube(self):
        each_scenario = 1
        yt_scenarios.scenario_dict[each_scenario](self.app[0])


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to execute youtube Scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)