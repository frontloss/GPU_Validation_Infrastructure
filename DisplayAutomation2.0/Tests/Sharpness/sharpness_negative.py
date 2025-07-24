########################################################################################################################
# @file         sharpness_negative.py
# @brief        Test to verify Sharpness in different negative scenarios.
#                   * Exercise the below scenarios and verify different features
#                       1. HDR
#                       2. Plane and Pipe Scalar
#                       3. Intensity (Range 0-100) and Negative range (-5,150)
# @author       Prateek Joshi
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.Color.Common.color_escapes import configure_hdr
from Tests.Sharpness import sharpness_helper, sharpness_verification
from Tests.Sharpness.sharpness_base import sharpness_base, SharpnessBase


##
# @brief    Contains Sharpness negative tests
class SharpnessNegative(SharpnessBase):
    @unittest.skipIf(sharpness_helper.get_config_type('-SCENARIO') != 'PIPE_AND_PLANE_SCALAR',
                     "Skipping test step as the scenario type is not PIPE_AND_PLANE_SCALAR")
    ##
    # @brief        Test to verify Sharpness when pipe and plane scalar are getting enabled.
    # @return       None
    def test01_pipe_and_plane_scalar(self):

        ##
        # Get Target ID list
        targetID_list = self.get_target_id_list(include_inactive=False)

        flag = False
        panel = None
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    flag = True
                    break
            if flag:
                break

        ##
        # Set the display to native mode
        supported_modes = self.config.get_all_supported_modes(targetID_list)
        native_mode = planes_ui_helper.apply_native_mode(panel)
        vt, hz, rr = native_mode.VtRes, native_mode.HzRes, native_mode.refreshRate

        ##
        # change the resolution of the panel wrt to the native mode to enable pipe scalar
        target_res = {
            (2160, 3840, 30): [(1024, 1280, 24)],
            (1080, 2048, 60): [(768, 1024, 60)],
            (1600, 2560, 60): [(1680, 1050, 60)],
            (1600, 2560, 59): [(1680, 1050, 59)],
            (1080, 1920, 60): [(768, 1024, 60), (768, 1280, 60)]
        }
        for target_id, modes in supported_modes.items():
            for mode in modes:
                if (mode.VtRes, mode.HzRes, mode.refreshRate) in target_res[(vt, hz, rr)]:
                    self.config.set_display_mode([mode], virtual_mode_set_aware=False)
                    logging.info(
                        "Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                            mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
                    break

        ##
        # start app (Media)
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        # perform resize so that up-scaling is done and plane scalar is enabled.
        for param in ((10, 10), (10, 10), (10, 10)):
            app_instance_1.resize(multiplier=param, direction=('right', 'bottom'))
            time.sleep(5)

        app_instance_1.close_app()

        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during PlanePipe Scalar Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

    ##
    # @brief        Test to verify Sharpness is disabled in HDR mode
    # @return       None
    @unittest.skipIf(sharpness_helper.get_config_type('-SCENARIO') != 'HDR',
                     "Skipping test step as the scenario type is not HDR")
    def test02_hdr(self):

        ##
        # Configure HDR
        flag = False
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if not configure_hdr(port, panel.display_and_adapterInfo, enable=True):
                        self.fail("Failed to enable HDR")
                    flag = True
                    break
            if flag:
                break

        ##
        # Play media in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')
        app_instance_1.open_app(is_full_screen=False)

        ##
        # Wait for a minute during video playback
        time.sleep(30)

        app_instance_1.close_app()

        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during HDR Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

        ##
        # Disable HDR
        flag = False
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if not configure_hdr(port, panel.display_and_adapterInfo, enable=False):
                        logging.error("Failed to disable HDR")
                        self.fail("Failed to disable HDR")
                    flag = True
                    break
            if flag:
                break

    ##
    # @brief        Test to verify Sharpness in odd intensity range
    # @return       None
    @unittest.skipIf(sharpness_helper.get_config_type('-SCENARIO') != 'INTENSITY',
                     "Skipping test step as the scenario type is not INTENSITY change")
    def test03_intensity_range(self):
        positive_strength = [5.0, 30.0, 45.0, 60.0, 85.0, 100.0]
        negative_strength = [-5.0, 150.0]

        ##
        # Feature Enabling through IGCL
        for strength_index in range(0, len(positive_strength)):
            strength = positive_strength[strength_index]
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if sharpness_helper.enable_disable_feature_igcl(strength, panel, self.filter_type,
                                                                    enable_disable=1) is True:
                        logging.info(f"PASS: Sharpness feature is enabled via IGCL for intensity: {strength}")
                    else:
                        logging.error(f"FAIL: Sharpness feature is not enabled via IGCL for intensity: {strength}")
                        self.fail(f"FAIL: Sharpness feature is not enabled via IGCL")

            ##
            # Play media/3D in windowed mode
            app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')
            app_instance_1.open_app(is_full_screen=False)

            ##
            # Wait for a minute during video playback
            time.sleep(30)

            app_instance_1.close_app()

            etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario_{strength}')

            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                               self.resolution) is False:
                        sharpness_helper.report_to_gdhm("Verification of Sharpness failed during sharpness intensity"
                                                        "change")
                        self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

        for strength_index in range(0, len(negative_strength)):
            strength = negative_strength[strength_index]
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if sharpness_helper.enable_disable_feature_igcl(strength, panel, self.filter_type,
                                                                    enable_disable=1) is False:
                        logging.info(f"PASS: Sharpness feature is not enabled via IGCL for unsupported strength")
                    else:
                        logging.error(f"FAIL: Sharpness feature is not enabled via IGCL for intensity: {strength}")
                        self.fail(f"FAIL: Sharpness feature is enabled via IGCL for unsupported strength")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Test to verify Sharpness Negative scenarios during media playback scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
