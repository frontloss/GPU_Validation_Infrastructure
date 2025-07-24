########################################################################################################################
# @file         planes_ui_concurrency.py
# @brief        Basic test to verify MPO in different concurrency scenarios.
#                   * Exercise the below scenarios
#                   * Verify the ETL's
#                       1. 48Hz
#                       2. Async and media playback
#                       3. Pipe and Plane Scalar
#                       4. HDR
# @author       Gopikrishnan R
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.color_escapes import configure_hdr
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI import planes_ui_base


##
# @brief    Contains PlanesUI concurrency tests
class PlanesUIConcurrency(planes_ui_base.PlanesUIBase):
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != '48HZ',
                     "Skip the test step as the scenario type is not 48Hz")
    ##
    # @brief        Test to verify RR change for app_instance_1 opened in Fullscreen mode
    # @return       None
    def test_01_48HzRR(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        display_list = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp:
                    display_list.append(panel.display_and_adapterInfo)
                    break
            if display_list is not []:
                break

        if display_list is []:
            self.fail("lfp panel-edp was not found in connected list")
        else:
            if planes_ui_helper.set_display_config(enum.SINGLE, display_list) is True:
                logging.info("Successfully applied display configuration to single mode")
                # Wait for 10 seconds after display switch
                time.sleep(10)
            else:
                self.fail("Failed to set display configuration")
        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')

        app_instance_1.open_app(is_full_screen=True, minimize=True)
        ##
        # Wait for a minute during video playback
        time.sleep(30)
        ##
        # Close media player
        app_instance_1.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO for async and media app is ran simultaneously
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'ASYNC_AND_MEDIA',
                     "Skip the test step as the scenario type is not ASYNC AND MEDIA")
    def test02_async_and_media(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        if self.app[0] not in ["FLIPAT", "TRIVFLIP", "FLIPMODELD3D12", "CLASSICD3D", "PRESENTAT"]:
            self.fail("Provided app is not an async app")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(minimize=True)

        app_instance_2 = planes_ui_helper.create_app_instance('MEDIA')
        app_instance_2.open_app(position='down')

        time.sleep(30)

        app_instance_1.close_app()
        app_instance_2.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify scalars are getting enabled.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'PIPE_AND_PLANE_SCALAR',
                     "Skip the test step as the scenario type is not PIPE_AND_PLANE_SCALAR")
    def test03_pipe_and_plane_scalar(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        target_id_list = self.get_target_id_list(include_inactive=False)

        flag = False
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    flag = True
                    break
            if flag:
                break
        ##
        # Set the display to native mode
        supported_modes = self.config.get_all_supported_modes(target_id_list)

        native_mode = planes_ui_helper.apply_native_mode(panel)
        vt, hz, rr = native_mode.VtRes, native_mode.HzRes, native_mode.refreshRate
        ##
        # change the resolution of the panel wrt to the native mode so as to enable pipe scalar
        target_res = {
            (2160, 3840, 30): [(1024, 1280, 24)],
            (1080, 2048, 60): [(768, 1024, 60)],
            (1600, 2560, 60): [(1680, 1050, 59)],
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

        # perform resize so that upscaling is done and plane scalar is enabled.
        for param in ((10, 10), (10, 10), (10, 10)):
            app_instance_1.resize(multiplier=param, direction=('right', 'bottom'))
            time.sleep(5)

        app_instance_1.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify HDR mode getting enabled
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'HDR',
                     "Skip the test step as the scenario type is not HDR")
    def test04_hdr(self):

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

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
        # Play media/3D in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False)

        app_instance_2 = None
        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

            ##
            # Wait for a minute during video playback
            time.sleep(30)

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify feature while media and DxApps are played
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'MEDIA_ASYNC',
                     "Skip the test step as the scenario type is not Media Async")
    def test05_media_dx_app(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        if self.app[0] not in ["FLIPAT", "TRIVFLIP", "FLIPMODELD3D12", "CLASSICD3D", "PRESENTAT"]:
            self.fail("Provided app is not an async app")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_2 = planes_ui_helper.create_app_instance('MEDIA')

        ##
        # Play media
        app_instance_2.open_app(is_full_screen=True)

        ##
        # Wait for 30 seconds after playing media
        time.sleep(30)

        ##
        # Close media
        app_instance_2.close_app()

        ##
        # Run DxApp
        app_instance_1.open_app(is_full_screen=True)

        ##
        # Wait for 30 seconds after running DxApp
        time.sleep(30)

        ##
        # Close DxApp
        app_instance_1.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify feature while DxApps are played followed by Media
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'ASYNC_MEDIA',
                     "Skip the test step as the scenario type is not Media Async")
    def test06_media_dx_app(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        if self.app[0] not in ["FLIPAT", "TRIVFLIP", "FLIPMODELD3D12", "CLASSICD3D", "PRESENTAT"]:
            self.fail("Provided app is not an async app")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_2 = planes_ui_helper.create_app_instance('MEDIA')

        ##
        # Run DxApp
        app_instance_1.open_app(is_full_screen=True)

        ##
        # Wait for 30 seconds after running DxApp
        time.sleep(30)

        ##
        # Close DxApp
        app_instance_1.close_app()

        ##
        # Play media
        app_instance_2.open_app(is_full_screen=True)

        ##
        # Wait for 30 seconds after playing media
        time.sleep(30)

        ##
        # Close media
        app_instance_2.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Test to verify concurrency for single/multiple app scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)