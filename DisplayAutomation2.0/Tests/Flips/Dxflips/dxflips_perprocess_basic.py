##
# @file         dxflips_perprocess_basic.py
# @brief        This test script verifies Per Process Gaming Features
# @author       Joshi, Prateek

import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper, per_process_helper, flip_verification
from Tests.Flips.Dxflips.dxflips_base import DxflipsBase


##
# @brief    Contains test functions that are used to verify Per Process Basic
class DxFlipsPerProcess(DxflipsBase):

    ##
    # @brief        Test function to verify Per Process during basic scenario
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "BASIC",
                     "Skip the test step as the scenarios is not basic")
    # @endcond
    def test_01_basic(self):
        app_feature_mapping = per_process_helper.FeatureMapping[self.feature_set].value

        for key, value in app_feature_mapping.items():
            self.per_app = key
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if flip_helper.enable_disable_asyncflip_feature(value, panel, self.per_app) is False:
                        self.fail(f"FAIL: {self.feature} setting for feature {value} is not enabled via IGCL for "
                                  f"app {self.per_app}")
                    logging.info(f"PASS: {self.feature} setting for feature {value} is enabled via IGCL for app "
                                 f"{self.per_app}")

                    etl_file_name = "Before_" + self.per_app.split('.')[0] + "_" + self.feature + str(time.time())

                    if flip_helper.start_etl_capture(etl_file_name) is False:
                        assert False, "FAIL: Failed to start GfxTrace"

                    if self.per_app == "FLIPAT":
                        fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
                    else:
                        fps_pattern = None
                        fps_pattern2 = None

                    ##
                    # Open any app
                    flip_helper.play_app(self.per_app, bfullscreen=True, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)

                    ##
                    # App will run for one minute
                    time.sleep(60)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")

    ##
    # @brief        Test function to verify Per Process persistence during open and close scenario
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "OPEN_CLOSE",
                     "Skip the test step as the scenario is not Open and Close")
    # @endcond
    def test_02_open_close(self):
        app_feature_mapping = per_process_helper.FeatureMapping[self.feature_set].value

        for key, value in app_feature_mapping.items():
            self.per_app = key
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if flip_helper.enable_disable_asyncflip_feature(value, panel, self.per_app) is False:
                        self.fail(f"FAIL: {self.feature} setting for feature {value} is not enabled via IGCL for "
                                  f"app {self.per_app}")
                        logging.info(f"PASS: {self.feature} setting for feature {value} is enabled via IGCL for app "
                                     f"{self.per_app}")

                    etl_file_name = "Before_" + self.per_app.split('.')[0] + "_" + self.feature + str(time.time())

                    if flip_helper.start_etl_capture(etl_file_name) is False:
                        assert False, "FAIL: Failed to start GfxTrace"

                    if self.per_app == "FLIPAT":
                        fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
                    else:
                        fps_pattern = None
                        fps_pattern2 = None

                    ##
                    # Open any app
                    flip_helper.play_app(self.per_app, bfullscreen=True, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)
                    ##
                    # App will run for one minute
                    time.sleep(60)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")

                    etl_file_name = "Before_" + self.per_app.split('.')[0] + "_" + self.feature + "_persistence" \
                                    + str(time.time())

                    if flip_helper.start_etl_capture(etl_file_name) is False:
                        assert False, "FAIL: Failed to start GfxTrace"

                    ##
                    # Open any app
                    flip_helper.play_app(self.per_app, bfullscreen=True, fps_pattern=fps_pattern,
                                         fps_pattern2=fps_pattern2)
                    ##
                    # App will run for one minute
                    time.sleep(60)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + "_persistence" \
                                    + str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify PerProcess functionality while running any application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)