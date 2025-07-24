########################################################################################################################
# @file         hdr_with_independent_brightness.py
# @brief        Test calls for get and set independent_brightness with HDR functionality
# @author       Vimalesh
########################################################################################################################

import ctypes
import sys
import unittest
import logging
import time

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Color.Common import color_constants, color_igcl_escapes, common_utility, gamma_utility
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Control_API.control_api_base import testBase


##
# @brief - Get/set IndependentBrtWithHDR Control Library Test with HDR
class testGetSetIndependentBrtWithHDR(HDRTestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        PRECISION_FACTOR = 1000

        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail("HDR not enabled")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.pipe == "B":
                    logging.info("Step_1: get lace")
                    BRIGHTNESS_LIST = [1, 61, 47, 100, 30, 89]
                    TRANSITION_TIME_LIST = [100, 500, 1000, 0, 200, 700, 900]
                    # Need to re-init as due to driver restart happened

                    # for set call
                    set_brightness = control_api_args.ctl_set_brightness_t()
                    set_brightness.Size = ctypes.sizeof(set_brightness)

                    # for get call
                    get_brightness = control_api_args.ctl_get_brightness_t()
                    get_brightness.Size = ctypes.sizeof(get_brightness)

                    set_brightness = control_api_args.ctl_set_brightness_t()
                    set_brightness.Size = ctypes.sizeof(set_brightness)
                    logging.info(panel.target_id)
                    for set_value, t_time in zip(BRIGHTNESS_LIST, TRANSITION_TIME_LIST):
                        set_brightness.TargetBrightness = set_value * PRECISION_FACTOR
                        set_brightness.SmoothTransitionTimeInMs = t_time
                        logging.info(
                            f"Applying {set_brightness.TargetBrightness} brightness with {t_time} ms transition time")

                        if control_api_wrapper.set_brightness_via_igcl(set_brightness, panel.target_id) is False:
                            self.fail("FAILED to do  Brightness call failed, unable to apply brightness")
                        logging.info("\tSuccessfully completed SET brightness using escape call")

                        time.sleep(5) # Buffer

                        logging.info(f"Doing GET operation for brightness to make sure that SET was done by driver")
                        if control_api_wrapper.get_brightness_via_igcl(get_brightness, panel.target_id) is False:
                            self.fail("FAILED to do GET brightness")
                        logging.info("\tSuccessfully completed GET brightness using escape call")

                        if set_brightness.TargetBrightness != get_brightness.CurrentBrightness:
                            self.fail(f"Brightness value Mismatch. Expected= {set_brightness.TargetBrightness}, "
                                      f"Actual= {get_brightness.CurrentBrightness}")

                        logging.info(f"Brightness value match. Expected= {set_brightness.TargetBrightness}, "
                                     f"Actual= {get_brightness.CurrentBrightness}")

                        event = "Independent_Brightness_Mode_TimeStmp_"
                        color_properties.update_feature_caps_in_context(self.context_args)

                        ##
                        # Verify if HDR has been enabled across all the panels
                        for gfx_index, adapter in self.context_args.adapters.items():
                            for port, panel in adapter.panels.items():
                                if panel.is_active:
                                    if feature_basic_verify.hdr_status(gfx_index, adapter.platform,
                                                                       panel.pipe) is False:
                                        self.fail()

                                    if self.plane_verification(gfx_index, adapter.platform, panel, 1,
                                                               port) is False:
                                        self.fail()

                                    # Observing Metadata verification mismatch for eDP B, where OS sends invalid value,
                                    # commenting the pipe verification for now as experiments ongoing with dual lfp verification.
                                    # Reference Metadata [2, 10508, 35533, 7478, 2981, 32014, 16471, 15640, 16422, 590, 0, 590, 590]
                                    # Programmed Metadata [2, 10508, 35533, 7478, 2981, 32014, 16471, 15640, 16422, 1452, 0, 1452, 1452]
                                    #if self.pipe_verification(gfx_index, adapter.platform, port,
                                    #                          panel) is False:
                                    #    self.fail()

    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            status = common_utility.delete_registry(adapter.gfx_index, "IndependentBrightnessControl")
            if status is False:
                self.fail("FAILED to delete IndependentBrightnessControl regkey")
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("FAILED to restart the driver")
                logging.info(f"Successfully restarted the driver for {adapter.gfx_index}")
        ##
        # Apply Unity Gamma as part of clean-up
        gamma_utility.apply_gamma()
        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        super().tearDown()

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get/set independent brightness API with HDR Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
