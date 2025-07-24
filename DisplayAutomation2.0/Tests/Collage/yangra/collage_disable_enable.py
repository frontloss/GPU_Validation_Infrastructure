#######################################################################################################################
# @file         collage_disable_enable.py
# @brief        Test to verify the enable and disable functionality of the collage in both HORIZONTAL and VERTICAL
#               collage type. Also with disable enable of driver based on user_event.
# @details      Test Scenario:
#                   1. Plugs the panel as per the arguments in the command line.
#                   2. Gets possible collage types based on the number of displays plugged.
#                   3. Apply Collage(say HC) and check if all displays are in collage mode and verify collage max mode.
#                   4. Restart the display driver and verify the collage functionality if user event is set to 1 in cmd
#                      user_event = 0 - do enable disable of collage only.
#                      user_event = 1 - do enable disable of collage along with driver disable enable.
#                   5. Disable the collage and check if collage is disabled and all displays came out of collage mode.
#                   6. Repeat step 3 to 5 for other collage types.
#                   6. Unplug all the external displays.
#
#
# @author       Praburaj Krishnan
#######################################################################################################################
import ctypes
import logging
import sys
import unittest

from Libs.Core import display_essential
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Feature.display_fbc import fbc

from Tests.Collage.yangra.collage_enum_constants import Action
from Tests.Collage.yangra.collage_yangra_base import CollageYangraBase


##
# @brief         This class contains functions to perform test steps for two types of enable -> disable collage
class TestCollageDisableEnable(CollageYangraBase):
    ##
    # @brief        Restarts the display driver and check if collage persists after disable -> enable of driver
    # @return       None
    def restart_driver_and_verify_collage(self) -> None:
        r_status, reboot_required = display_essential.restart_gfx_driver()
        self.assertEquals(r_status, True, 'Failure occurred after disabling and enabling Graphics driver. Exiting..')
        logging.info("Graphics driver was disabled and enabled Successfully...")

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

        # Verify the enumerated collage and the displays in collage after enabling back the driver.
        r_status = CollageYangraBase.is_collage_display_enumerated(collage_display_info_list[0])
        if r_status is False:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Display is not enumerated after disable -> enable driver",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertEquals(r_status, True, 'Collage display is not enumerated after disable -> enable of driver')
        logging.info("Collage display successfully enumerated after disable -> enable of driver")

        self.verify_displays_in_collage()

    ##
    # @brief    Test to perform the test steps as mentioned in the test scenario.
    # @return   None
    def runTest(self) -> None:
        logging.info('*********************  TEST BEGINS HERE *********************')

        # Hot plug all the displays passed in the command line.
        self.hot_swap_display(action=Action.HOT_PLUG_ALL)

        user_event = int(CollageYangraBase.cmd_dict['USER_EVENT'][0])

        display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(display_info_list, 'DisplayInfo not found.')
        # Gdhm bug reporting handled in get_display_info_list_to_be_in_collage

        # Temporarily Disabling PTL CD Clock Verification on Collage
        # # Clock verification
        # gfx_index = display_info_list[0].DisplayAndAdapterInfo.adapterInfo.gfxIndex
        # is_success = CollageYangraBase.displayClock.verify_clocks(gfx_index)
        # if is_success is False:
        #     self.fail("[Driver Issue] : Clock Verification failed!")
        # logging.info("PASS : Clock Verification!")

        logging.info("Verifying VDSC status before enabling collage")
        status = self._verify_vdsc(display_info_list)
        self.assertTrue(status, '[Driver Issue] - VDSC verification failed.')

        collage_types = CollageYangraBase.get_possible_collage_types(len(display_info_list))
        # Set Horizontal and Vertical collage topology and verify

        for collage_type in collage_types:
            self.set_and_verify_collage_topology(collage_type, display_info_list)
            # Do a restart of the driver if the user even is 1 else only disable collage and verify.
            if user_event == 1:
                self.restart_driver_and_verify_collage()

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

            # Temporarily Disabling PTL CD Clock Verification on Collage
            # if self.actual_cd_clock is None:
            #     self.fail("[Test Issue] : Failed to initialize clk object.")
            # logging.debug(f"CD Clock after invoking collage: {self.actual_cd_clock}")
            # if self.expected_cd_clock == self.actual_cd_clock:
            #     logging.info(f"Pass: CD Clock Expected: {self.expected_cd_clock}, Actual: {self.actual_cd_clock}")
            # else:
            #     self.fail(f"[Driver Issue] - CD Clock Expected: {self.expected_cd_clock}, Actual: {self.actual_cd_clock}")

            status = self._verify_vdsc(display_info_list, collage_display_info_list[0])
            self.assertTrue(status, '[Driver Issue] - VDSC verification failed.')

            fbc_status = fbc.verify_fbc(is_display_engine_test=False)
            self.assertTrue(fbc_status, '[Driver Issue] - FBC verification failed.')

            displayEncoderProperties = control_api_args.ctl_adapter_display_encoder_properties_t()
            displayEncoderProperties.Size = ctypes.sizeof(displayEncoderProperties)
            enumerated_display_info = self.display_config.get_enumerated_display_info()

            logging.info("IGCL Display Type Verification")
            for index in range(enumerated_display_info.Count):
                target_id = enumerated_display_info.ConnectedDisplays[index].TargetID
                if control_api_wrapper.get_display_encoder_properties(displayEncoderProperties, target_id):
                    if target_id == displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID:
                        logging.info("Display Target_ID {}, EncoderConfigFlags {}".format(
                            displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID,
                            displayEncoderProperties.EncoderConfigFlags))
                        if control_api_args.ctl_encoder_config_flags_v.COLLAGE_DISPLAY.value and \
                                displayEncoderProperties.EncoderConfigFlags:
                            logging.info("Collage Display Enabled {}".format(
                                control_api_args.ctl_encoder_config_flags_v.COLLAGE_DISPLAY.value and
                                displayEncoderProperties.EncoderConfigFlags))
                            logging.info("Pass: IGCL Collage Display Type Verified")
                        else:
                            logging.error("Collage Display Config Flag is not reported from IGCL {}".format(
                                control_api_args.ctl_encoder_config_flags_v.COLLAGE_DISPLAY.value and
                                displayEncoderProperties.EncoderConfigFlags))

            self.disable_collage_and_verify(collage_display_info_list[0])

        logging.info('*********************  TEST ENDS HERE *********************')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
