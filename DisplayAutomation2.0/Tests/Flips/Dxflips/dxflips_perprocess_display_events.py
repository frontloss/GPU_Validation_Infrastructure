##
# @file         dxflips_perprocess_display_events.py
# @brief        This test script verifies Per Process Gaming Features
# @author       Joshi, Prateek

import logging
import sys
import time
import unittest

from Libs.Core import display_essential, display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.wrapper import control_api_wrapper
from Tests.Flips import flip_helper, per_process_helper, flip_verification
from Tests.Flips.Dxflips.dxflips_base import DxflipsBase


##
# @brief    Contains test functions that are used to verify Per Process Basic
class DxFlipsPerProcess(DxflipsBase):


    ##
    # @brief        Test function to verify Per Process after generating TDR
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "GENERATE_TDR",
                     "Skip the test step as the scenario is not generate TDR")
    # @endcond
    def test_01_generate_tdr(self):
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
                    # Generate & Verify TDR
                    VerifierCfg.tdr = Verify.SKIP
                    logging.debug(f"Config under-run:{VerifierCfg.underrun.name}, tdr:{VerifierCfg.tdr.name}")
                    logging.info("Generating TDR during ")
                    if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
                        self.fail("Failed to generate TDR")

                    if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
                        logging.info('TDR generated successfully')
                    else:
                        self.fail("TDR is not detected")

                    time.sleep(5)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + "_tdr" + \
                                    str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + "_tdr_playback" \
                                    + str(time.time())
                    if flip_helper.start_etl_capture(etl_file_name) is False:
                        assert False, "FAIL: Failed to start GfxTrace"

                    ##
                    # Open any app
                    flip_helper.play_app(self.per_app, bfullscreen=True, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)
                    ##
                    # App will run for one minute
                    time.sleep(60)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)
                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + "_playback" \
                                    + str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)

    ##
    # @brief        Test function to verify Per Process after Mode Switch
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "MODE_SWITCH",
                     "Skip the test step as the scenario is not Mode Switch")
    # @endcond
    def test_02_mode_switch(self):
        app_feature_mapping = per_process_helper.FeatureMapping[self.feature_set].value

        target_id_list = []

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        ##
        # Get enumerated display info
        enumerated_displays = self.config.get_enumerated_display_info()

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
                    # fetch all the modes supported by each of the displays connected
                    supported_modes = self.config.get_all_supported_modes(target_id_list)
                    for keys, values in supported_modes.items():
                        for mode in values:
                            ##
                            # set all the supported modes
                            self.config.set_display_mode([mode])
                            logging.info("Applied Display mode during app run {}".format(mode.to_string(enumerated_displays)))

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)

    ##
    # @brief        Test function to verify Per Process after driver restart
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "RESTART_DRIVER",
                     "Skip the test step as the scenario is not restart driver")
    # @endcond
    def test_03_restart_driver(self):
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
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)

                    etl_file_name = "Before_" + self.per_app.split('.')[0] + "_" + self.feature + "_driver_restart" \
                                    + str(time.time())

                    if flip_helper.start_etl_capture(etl_file_name) is False:
                        assert False, "FAIL: Failed to start GfxTrace"

                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver")
                    else:
                        logging.info("Successfully restarted display driver")

                    ##
                    # Wait for 10 seconds after display driver restart
                    time.sleep(10)

                    ##
                    # Open any app
                    flip_helper.play_app(self.per_app, bfullscreen=True, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)

                    ##
                    # App will run for one minute
                    time.sleep(60)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.per_app.split('.')[0] + "_" + self.feature + "_driver_restart" + \
                                    str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for feature {value} and app {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for feature {value} and app {self.per_app}")
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)

    ##
    # @brief        Test function to verify Per Process after Mode Switch
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') not in ["POWER_EVENT_S3", "POWER_EVENT_S4"],
                     "Skip the test step as the scenario is not Power Event")
    # @endcond
    def test_04_power_event(self):
        app_feature_mapping = per_process_helper.FeatureMapping[self.feature_set].value

        disp_power = display_power.DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_S4": display_power.PowerEvent.S4}

        for key, value in app_feature_mapping.items():
            self.per_app = key
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if flip_helper.enable_disable_asyncflip_feature(value, panel, self.per_app) is False:
                        self.fail(f"FAIL: {self.feature} setting for feature {value} is not enabled via IGCL for "
                                  f"app {self.per_app}")
                        logging.info(f"PASS: {self.feature} setting for feature {value} is enabled via IGCL for app "
                                     f"{self.per_app}")

                    etl_file_name = "Before_" + self.per_app.split('.')[0] + "_" + self.feature + "_power_event" + \
                                    str(time.time())

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
                    # Invoke power event
                    if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
                        flip_helper.report_to_gdhm(self.feature, f"Failed to invoke power event {self.scenario}",
                                                   driver_bug=False)
                        self.fail(f"Failed to invoke power event {power_state_dict[self.scenario]}")
                    else:
                        logging.info(f"Power event {power_state_dict[self.scenario]} success")

                    ##
                    # Wait for 10 seconds after power event
                    time.sleep(10)

                    ##
                    # Close the application
                    flip_helper.close_app(self.per_app)

                    etl_file_name = "After_" + self.app.split('.')[0] + "_" + self.feature + "_power_event" + \
                                    str(time.time())
                    etl_file = flip_helper.stop_etl_capture(etl_file_name)

                    if flip_verification.verify_per_process(etl_file, flip_helper.get_app_name(self.per_app), value):
                        logging.info(f"Per process verification passed for Feature {value} and App {self.per_app}")
                    else:
                        self.fail(f"Per process verification failed for Feature {value} and App {self.per_app}")
                        flip_helper.report_to_gdhm(self.feature, f"Per process verification failed for feature {value} "
                                                                 f"and app {self.per_app}", driver_bug=True)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify PerProcess functionality while running any application during display events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)