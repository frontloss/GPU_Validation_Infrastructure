#######################################################################################################################
# @file         collage_config_switching_yangra.py
# @brief        Test to verify collage config switching functionalities in both HORIZONTAL and VERTICAL collage type.
# @details      Test Scenario:
#                   1. Plugs the panel as per the arguments in the command line.
#                   2. Performs Hybrid config switching / normal config switching based on custom tag named "user_event"
#                      user_event 0 - Represents standard config switching
#                      user_event 1 - Represents Hybrid config switching
#                   3. Unplugs all the external displays.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import sys
import unittest
from typing import List

from Libs.Core.wrapper.driver_escape_args import CollageType
from Libs.Core.display_config.display_config_struct import DisplayInfo
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.yangra.collage_enum_constants import Action
from Tests.Collage.yangra.collage_yangra_base import CollageYangraBase


##
# @brief        This class contains functions to perform test steps for two types of config switching test cases.
class TestCollageConfigSwitching(CollageYangraBase):

    ##
    # @brief        This test verifies, if collage is able to co-exist with other config like EXTENDED/CLONE.
    # @details      Code flow:
    #                   Apply HC and Verify.
    #                   Get all possible display combinations for a given topology.
    #                   For each of the combination apply the config. E.g. EXTENDED [edp_a + COLLAGE_0].
    #                   Disable Collage and Verify if its disabled.
    #                   Repeat for VC.
    # @param[in]    config_to_apply: str
    #                   Display config like EXTENDED/CLONE.
    # @param[in]    display_info_list: List[DisplayInfo]
    #                   Contains target ids that will be part of collage.
    # @return       None
    def collage_hybrid_config_switching(self, config_to_apply: str, display_info_list: List[DisplayInfo]) -> None:
        no_of_pipe_occupied_by_collage = len(display_info_list)

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            self.set_and_verify_collage_topology(collage_type, display_info_list)
            target_id_combination_list = CollageYangraBase.get_possible_Configurations(config_to_apply,
                                                                                       no_of_pipe_occupied_by_collage)

            for target_id_list in target_id_combination_list:
                r_status = CollageYangraBase.set_display_config_and_verify(config_to_apply, target_id_list)
                self.assertEquals(r_status, True, "Aborting the test as applying the display config failed")

            collage_display_info_list = CollageYangraBase.get_collage_display_info_list()
            if len(collage_display_info_list) == 0:
                gdhm.report_bug(
                    title="[Interfaces][Display_Collage] Collage Display info not found ",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
            self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found.')

            self.disable_collage_and_verify(collage_display_info_list[0])

    ##
    # @brief        This test verifies whether driver is able to do a config switch from collage display to other config
    #               like SINGLE/EXTENDED/CLONE.
    # @details      Code Flow:
    #                   Get all possible display combinations for a given topology.
    #                   Iterate through each of the possible combinations of displays.
    #                       Apply HC and Verify -> Disable Collage and Verify if its disabled.
    #                       Apply config on displays obtained over the iteration based on the config_to_apply argument
    #                       like SINGLE/EXTENDED/CLONE and verify it.
    #                   Repeat for VC.
    # @param[in]    config_to_apply: str
    #                   Display config like SINGLE/EXTENDED/CLONE.
    # @param[in]    display_info_list: List[DisplayInfo]
    #                   Contains target ids that will be part of collage.
    # @return       None
    def collage_config_switching(self, config_to_apply: str, display_info_list: List[DisplayInfo]) -> None:

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            # Get and Set the display configuration.
            target_id_combination_list = CollageYangraBase.get_possible_Configurations(config_to_apply)

            # Iterate through each of target id list and apply the topology mentioned in command line.
            for target_id_list in target_id_combination_list:
                # Enable collage and verify
                self.set_and_verify_collage_topology(collage_type, display_info_list)
                collage_display_info_list = CollageYangraBase.get_collage_display_info_list()
                gdhm.report_bug(
                    title="[Interfaces][Display_Collage] Collage Display info not found ",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found.')

                # Disable collage before applying any other config.
                self.disable_collage_and_verify(collage_display_info_list[0])

                # Apply the config.
                r_status = CollageYangraBase.set_display_config_and_verify(config_to_apply, target_id_list)
                self.assertEquals(r_status, True, "Aborting the test as applying the display config failed")
                # Gdhm bug reporting handled in set_display_config_and_verify

    ##
    # @brief    Triggers the test based on the user_event in the command line.
    # @return   None
    def runTest(self) -> None:
        logging.info('*********************  TEST BEGINS HERE  *********************')

        config_to_apply = CollageYangraBase.cmd_dict['CONFIG']
        user_event = int(CollageYangraBase.cmd_dict['USER_EVENT'][0])

        CollageYangraBase.hot_swap_display(self, action=Action.HOT_PLUG_ALL)
        display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(display_info_list, 'DisplayInfo not found.')

        if user_event == 0:
            self.collage_config_switching(config_to_apply, display_info_list)
        elif user_event == 1:
            self.collage_hybrid_config_switching(config_to_apply, display_info_list)
        else:
            self.fail("Invalid user event passed in the command line")

        logging.info('*********************  TEST ENDS HERE  *********************')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
