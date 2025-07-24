#######################################################################################################################
# @file         collage_negative_scenario.py
# @brief        Test to verify if the collage is possible in case of various negative scenarios
#               Eg. Collage with YUV420 panels/Tiled panels.
# @details      Test Scenario:
#                   1. Plugs the panel as per the arguments in the command line.
#                   2. Gets display info to be in collage.
#                   3. Check if collage is possible with given topology
#                   4. Unplug all the external displays.
#
#
# @author       Goutham N
#######################################################################################################################
import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.yangra.collage_enum_constants import Action
from Tests.Collage.yangra.collage_yangra_base import CollageYangraBase


##
# @brief         This class contains functions to validate negative collage scenarios

class TestCollageNegativeScenario(CollageYangraBase):

    ##
    # @brief    Test to perform the test steps as mentioned in the test scenario.
    # @return   None
    def runTest(self) -> None:
        logging.info('*********************  TEST BEGINS HERE *********************')

        # Hot plug all the displays passed in the command line.
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)

        display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(display_info_list, 'DisplayInfo not found.')

        is_collage_config_possible = self.is_collage_topology_possible(display_info_list)

        self.assertFalse(is_collage_config_possible, "[Driver Issue] As per current driver policy, collage shouldn't be supported with yuv 420 or Tiled monitors.")

        logging.info("As per current driver policy, Collage is not possible with YUV420 or tiled monitors.")

        logging.info('*********************  TEST ENDS HERE *********************')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
