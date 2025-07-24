########################################################################################################################
# @file         planes_ui_basic.py
# @brief        Basic test to verify MPO in different scenarios.
#                   * Exercise the below scenarios and verify different features
#                       1. Fullscreen and windowed playback
#                       2. Fullscreen and windowed playback with charms and (media controls)
#                       3. Snapmode
#                           - Media + Desktop
#                           - 3D App + Desktop
#                           - Media + 3D App
#                           - 3D App + 3D App
#                       4. Windowed
#                           - Media + 3D App
#                           - 3D App + 3D App
#                       5. Open and Close
#                           - Media
#                           - Media + 3D App
#                           - 3D App + 3D App
#                       6. Fullscreen and windowed scenario with PresentAt
#                       7. Fullscreen media playback with captions
# @author       Gopikrishnan R
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper, window_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI import planes_ui_base
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI.Common import planes_ui_verification


##
# @brief    Contains basic PlanesUI tests
class PlanesUIBasic(planes_ui_base.PlanesUIBase):
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'FULLSCREEN_AND_WINDOWED',
                     "Skip the test step as the scenario type is not FULLSCREEN_AND_WINDOWED")
    ##
    # @brief        Test to verify MPO for app opened in Fullscreen/windowed mode
    # @return       None
    def test_01_fullscreen_and_windowed(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = planes_ui_helper.create_app_instance(self.app[1]) if len(self.app) > 1 else None

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        for is_full_screen in [True, False]:
            for app_instance in app_instance_list:
                app_instance.open_app(is_full_screen=is_full_screen, minimize=True)
                ##
                # Wait for a minute during video playback
                time.sleep(60)
                ##
                # Close media player
                app_instance.close_app()

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
    # @brief        Test to verify MPO for app opened in Fullscreen/windowed mode with charms enabled
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'FULLSCREEN_AND_WINDOWED_WITH_CHARMS',
                     "Skip the test step as the scenario type is not FULLSCREEN_AND_WINDOWED_WITH_CHARMS")
    def test02_app_with_charms(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")
        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = planes_ui_helper.create_app_instance(self.app[1]) if len(self.app) > 1 else None

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        # open and close apps in Fullscreen/windowed mode, one at a time
        for is_full_screen in [True, False]:
            for app_instance in app_instance_list:
                app_instance.open_app(is_full_screen=is_full_screen, minimize=True)
                time.sleep(60)
                # Enable and disable charms every 5 seconds, enable media controls in case of media
                for i in range(10):
                    app_instance.enable_charms()
                    time.sleep(5)
                    app_instance.disable_charms()
                    if not i % 3:
                        app_instance.enable_media_controls()
                time.sleep(15)
                ##
                # Close media player
                app_instance.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO when multiple apps are opened in snap_mode
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'SNAPMODE',
                     "Skip the test step as the scenario type is not SNAPMODE")
    def test03_app_snapmode(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # start app1 (Media/3D) and snap to left
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False)
        app_instance_1.snap_mode('left')

        app_instance_2 = None
        ##
        # start app2 (Media/3D) and snap to right, if two apps are there in commandline
        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)
            app_instance_2.snap_mode('right')

        ##
        # sleep for 30 seconds and close the apps
        time.sleep(60)
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
    # @brief        Test to verify MPO when multiple apps are opened in windowed_mode
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'WINDOWED',
                     "Skip the test step as the scenario type is not WINDOWED")
    def test04_app_windowed(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Play media/3D in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False, minimize=False)

        ##
        # every 5 seconds enable media controls if app_instance_1/app_instance_2 is media
        if 'MEDIA' in self.app:
            for i in range(10):
                if self.app[0] == 'MEDIA':
                    app_instance_1.enable_media_controls()

                if app_instance_2 is not None and self.app[1] == 'MEDIA':
                    app_instance_2.enable_media_controls()
                time.sleep(10)

        ##
        # close the apps
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
    # @brief        Test to verify plane enabling/disabling when multiple apps are opened/closed
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'OPEN_AND_CLOSE',
                     "Skip the test step as the scenario type is not mode switch")
    def test05_open_and_close_app(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])

        ##
        # if 2 apps are enabled, defined actions based on which apps will be opened and closed
        if app_instance_2 is not None:
            actions = [1, 3, 4, 3, 4, 3, 2, 1, 4, 2, 1, 3, 4, 3, 4, 2, 1, 3, 4, 3, 4, 2,
                       3, 1, 2, 1, 2, 4, 3, 1, 4, 2, 1, 2, 1, 3, 2, 4, 1, 2]
            action_dict = {
                1: app_instance_1.open_app,
                2: app_instance_1.close_app,
                3: app_instance_2.open_app,
                4: app_instance_2.close_app,
            }
            for i in actions:
                action_dict[i]()
                time.sleep(10)
            app_instance_1.close_app()
            app_instance_2.close_app()

        ##
        # if only 1 app is enabled open and close in a loop of 10
        else:
            for i in range(10):
                app_instance_1.open_app(is_full_screen=False, minimize=False)
                time.sleep(60)
                app_instance_1.close_app()

        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO for app opened in Fullscreen/windowed mode for presentAt
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'FULLSCREEN_AND_WINDOWED_PRESENTAT',
                     "Skip the test step as the scenario type is not FULLSCREEN_AND_WINDOWED_PRESENTAT")
    def test_06_fullscreen_windowed_presentAt(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Create app instances
        app_instance = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = None

        app_instance.open_app()

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.position = app_instance_2.ORIENTATION["RIGHT_PANE"]
            app_instance_2.open_app()

        time.sleep(20)
        ##
        # Wait for a minute during video playback

        ##
        # Close app instance 1
        app_instance.close_app()

        if app_instance_2 is not None:
            app_instance_2.close_app()

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
    # @brief        Test to verify MPO for app opened in Fullscreen/windowed mode for presentAt
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'MEDIA_FULLSCREEN_WITH_CAPTIONS',
                     "Skip the test step as the scenario type is not MEDIA_FULLSCREEN_WITH_CAPTIONS")
    def test_07_full_screen_media_with_captions(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        planes_ui_helper.play_video_with_subtitles(
            planes_ui_helper.Videos[f"{planes_ui_helper.get_config_type('-MEDIA_TYPE')}"].value)

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'FULLSCREEN',
                     "Skip the test step as the scenario type is not FULLSCREEN")
    ##
    # @brief        Test to verify MPO for app opened in Fullscreen mode
    # @return       None
    def test_08_fullscreen(self):
        ##
        # Create app instances
        app_instance = planes_ui_helper.create_app_instance(self.app[0])

        app_instance.open_app(is_full_screen=True, minimize=True)

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        ##
        # Close media player
        app_instance.close_app()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_verification.verify_flip_time(etl_file, panel.target_id, panel.pipe) is False:
                    self.fail("Flip Execution time verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to verify MPO functionality during single/multiple app scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
