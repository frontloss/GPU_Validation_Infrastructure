#######################################################################################################################
# @file         collage_audio_verification.py
# @brief        Verifies Audio endpoint and playback by applying horizontal and vertical collage
# @details      Test Scenario:
#                   1. Plugs the panel as per the arguments in the command line.
#                   2. Gets possible collage types based on the number of displays plugged.
#                   3. Apply Collage and check if all displays are in collage mode and verify collage max mode.
#                   4. Invoke power event (S3/S4/CS) based on custom tag in command.
#                   5. Verify Audio endpoint is enumerated for all the child displays connected in collage.
#                   6. Verify playback for all the enumerated endpoints.
#                   7. Disable the collage and check if collage is disabled and all displays are out of collage mode.
#                   8. Repeat step 3 to 6 for other collage types.
#                   9. Unplug all the external displays.
#                   a. Sample command: Tests\Collage\yangra\collage_audio_verification.py -edp_a -dp_f -dp_g
#                      -config_path SST/DUAL_COLLAGE -ID DC100001 -selective BASIC
#                   b. Sample command: Tests\Collage\yangra\collage_audio_verification.py -edp_a -dp_f -dp_g
#                      -config_path SST/DUAL_COLLAGE -ID DC100001 -selective S4
#
# @author       Nivetha
#######################################################################################################################

import logging
import unittest
from typing import Optional

from Libs.Core import display_power, enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_audio import DisplayAudio
from Tests.Collage.yangra.collage_enum_constants import Action
from Tests.Collage.yangra.collage_yangra_base import CollageYangraBase
from Tests.PowerCons.Modules import common
from Tests.Audio.display_audio_base import AudioBase


##
# @brief         This class contains functions to perform audio verification by applying collage modes
class CollageAudioBase(CollageYangraBase):
    display_info_list = None
    display_info = []

    ##
    # @brief        Verifies audio endpoint and playback with applied collage nodes
    # @return       None
    # @cond
    @common.configure_test(selective=['BASIC'])
    # @endcond
    def t_1_basic(self) -> None:
        logging.info('{:*^80}'.format('COLLAGE AUDIO BASIC TEST STARTS'))

        # Hot plug all the displays passed in the command line.
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)
        self.set_display_info()
        self.display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(self.display_info_list, 'DisplayInfo not found.')

        collage_types = CollageYangraBase.get_possible_collage_types(len(self.display_info_list))
        # Set Horizontal and Vertical collage topology and verify
        for collage_type in collage_types:
            self.set_and_verify_collage_topology(collage_type, self.display_info_list)
            self.verify_audio()

        logging.info('{:*^80}'.format('COLLAGE AUDIO BASIC TEST ENDS'))

    ##
    # @brief        Verifies audio endpoint and playback with collage after resuming back from CS
    # @return       None
    # @cond
    @common.configure_test(selective=['CS'])
    # @endcond
    def t_2_power_event_cs(self) -> None:
        logging.info('{:*^80}'.format('COLLAGE AUDIO CS TEST STARTS'))
        # Hot plug the displays based on the command line
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)
        self.set_display_info()
        self.display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(self.display_info_list, 'DisplayInfo not found.')

        collage_types = CollageYangraBase.get_possible_collage_types(len(self.display_info_list))
        # Set Horizontal and Vertical collage topology and verify
        for collage_type in collage_types:
            self.set_and_verify_collage_topology(collage_type, self.display_info_list)
            self.verify_audio(power_event=display_power.PowerEvent.CS)

        logging.info('{:*^80}'.format('COLLAGE AUDIO CS TEST ENDS'))

    ##
    # @brief        Verifies audio endpoint and playback with collage after resuming back from S3
    # @return       None
    # @cond
    @common.configure_test(selective=['S3'])
    # @endcond
    def t_3_power_event_s3(self) -> None:
        logging.info('{:*^80}'.format('COLLAGE AUDIO S3 TEST STARTS'))
        # Hot plug the displays based on the command line
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)
        self.set_display_info()
        self.display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(self.display_info_list, 'DisplayInfo not found.')

        collage_types = CollageYangraBase.get_possible_collage_types(len(self.display_info_list))
        # Set Horizontal and Vertical collage topology and verify
        for collage_type in collage_types:
            self.set_and_verify_collage_topology(collage_type, self.display_info_list)
            self.verify_audio(power_event=display_power.PowerEvent.S3)

        logging.info('{:*^80}'.format('COLLAGE AUDIO S3 TEST ENDS'))

    ##
    # @brief        Verifies audio endpoint and playback with collage after resuming back from S4
    # @return       None
    # @cond
    @common.configure_test(selective=['S4'])
    # @endcond
    def t_4_power_event_s4(self) -> None:
        logging.info('{:*^80}'.format('COLLAGE AUDIO S4 TEST STARTS'))
        # Hot plug the displays based on the command line
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)
        self.set_display_info()
        self.display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(self.display_info_list, 'DisplayInfo not found.')

        collage_types = CollageYangraBase.get_possible_collage_types(len(self.display_info_list))
        # Set Horizontal and Vertical collage topology and verify
        for collage_type in collage_types:
            self.set_and_verify_collage_topology(collage_type, self.display_info_list)
            self.verify_audio(power_event=display_power.PowerEvent.S4)

        logging.info('{:*^80}'.format('COLLAGE AUDIO S4 TEST ENDS'))

    ##
    # @brief        Retrieves the display info for connected displays
    # @return       None
    def set_display_info(self):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays.Count != 0:
            for i in range(enumerated_displays.Count):
                if enumerated_displays.ConnectedDisplays[i].IsActive is True:
                    display_adapter_info = enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo
                    if DisplayAudio().is_audio_capable(display_adapter_info):
                        self.display_info.append(enumerated_displays.ConnectedDisplays[i])

    ##
    # @brief        Verifies Audio endpoint and playback along with power event if requested
    # @param[in]    power_event - Enum
    #                       Power State to be invoked
    # @return       None
    def verify_audio(self, power_event: Optional[int] = None):
        if power_event is not None:
            if self.display_power.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
                gdhm.report_bug(
                    title=f"[Interfaces][Display_Collage] Failed To Invoke Power Event:"
                          f" {power_event.name}",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail(f'Failed To Invoke Power Event: {power_event.name} [Driver issue]')
        AudioBase().verify_audio_driver()
        endpoint_name_list = DisplayAudio().get_audio_endpoint_name(only_unique_endpoint=False)
        no_of_endpoints_ospage = DisplayAudio().get_audio_endpoints()
        if no_of_endpoints_ospage == len(self.display_info_list):
            logging.info(f"\tPASS: Expected Audio Endpoints= {len(self.display_info_list)} Actual="
                         f" {no_of_endpoints_ospage}")
            for display in self.display_info:
                for endpoint_name in endpoint_name_list:
                    status = DisplayAudio().audio_playback_verification(display_info=display,
                                                                        end_point_name=endpoint_name)
                    if status:
                        logging.info(f"\tPass: Audio Playback Verification success for {endpoint_name}")
                    else:
                        self.assertTrue(endpoint_name, 'Audio playback verification failed')
                break
        else:
            logging.error(f"\tFAIL: Expected Audio Endpoints= {len(self.display_info_list)}"
                          f"Actual= {no_of_endpoints_ospage}")
            gdhm.report_bug(
                title=f"Display Audio endpoint verification failed with Collage enabled",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_AUDIO,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail(f"\tFAIL: Expected Audio Endpoints= {len(self.display_info_list)}"
                      f"Actual= {no_of_endpoints_ospage}")

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

        # Disables collage and verify
        self.disable_collage_and_verify(collage_display_info_list[0])


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CollageAudioBase))
    TestEnvironment.cleanup(test_result)
