########################################################################################################################
# @file    planes_ui_app_events.py
# @brief   Basic test to verify MPO in different scenarios.
#           * Exercise the below scenarios and verify different features in these combinations
#               - 3D App + 3D App
#               - Media + 3D App
#               - Media / 3D App
#               1. Resize the app(s) to different sizes
#               2. Drag the app(s) to different displays
#               3. Window Switch for app(s)
#               4. Min-Max for app(s)
#               5. Move window for app(s)
#               6. Play pause video
# @author   Gopikrishnan R
########################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI import planes_ui_base


##
# @brief    Contains PlanesUI app event specific tests
class PlanesUIAppEvents(planes_ui_base.PlanesUIBase):
    ##
    # @brief        Test to verify MPO functionality when app(s) are resized into different sizes.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'RESIZE',
                     "Skip the test step as the scenario type is not resize")
    def test_01_resize(self):
        target_id_list = self.get_target_id_list()

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        time.sleep(5)
        resize_multipliers = [(20, 20), (-10, -15), (10, 10), (-20, -15), (10, 0), (0, -20), (0, 20), (-10, 0)]

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        directions = [('right', 'bottom'), ('right', 'top'), ('left', 'top'), ('left', 'bottom')]

        for direction in directions:
            for multiplier in resize_multipliers:
                for app_instance in app_instance_list:
                    app_instance.resize(multiplier, direction=direction)
                    time.sleep(5)

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

    ##
    # @brief        Test to verify MPO functionality when app(s) dragged from one screen to other in extended
    #               configuration.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'DRAG',
                     "Skip the test step as the scenario type is not drag")
    def test_02_drag(self):
        adapter_tid_dict = self.get_tid_adapter_dict()
        target_id_list = self.get_target_id_list()

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None
        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]
        source = 0
        for tid_list in target_id_list, target_id_list[::-1]:
            for i in range(5):
                for app_instance in app_instance_list:
                    if i is 0:
                        source = app_instance.get_app_screen(app_instance_1.hwnd)
                    destination = (source + 1) % len(tid_list)
                    port, gfx_adapter = adapter_tid_dict[tid_list[destination]]
                    app_instance.drag(port, gfx_adapter)
                    time.sleep(10)
                    source = destination

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

    ##
    # @brief        Test to verify MPO functionality when app(s) window is switched from fullscreen to windowed
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'WINDOW_SWITCH',
                     "Skip the test step as the scenario type is not window switch")
    def test_03_window_switch(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = planes_ui_helper.create_app_instance(self.app[1]) if len(self.app) > 1 else None

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        for app_instance in app_instance_list:
            ##
            # Play the app(s) in windowed mode
            app_instance.open_app(is_full_screen=False, minimize=True)
            ##
            # Switch to fullscreen
            winkb_helper.press('ALT_ENTER')
            logging.info("Switched to fullscreen")

            ##
            # Wait for a minute after switching to fullscreen
            time.sleep(60)

            ##
            # Switch to windowed mode
            winkb_helper.press('ALT_ENTER')
            logging.info("Switched to windowed mode")

            ##
            # Wait for a minute after switching to windowed mode
            time.sleep(60)

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
    # @brief        Test to verify MPO functionality when app(s) window is minimized and maximized
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'MIN_MAX',
                     "Skip the test step as the scenario type is not min max")
    def test_04_min_max(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = planes_ui_helper.create_app_instance(self.app[1]) if len(self.app) > 1 else None

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        for app_instance in app_instance_list:
            ##
            # Play the app(s) in windowed mode
            app_instance.open_app(is_full_screen=False, minimize=True)
            ##
            # Minimize video playback window
            winkb_helper.press('WIN+D')
            logging.info("Minimized the window")

            ##
            # Wait for 10 seconds after minimize
            time.sleep(10)

            ##
            # Maximize video playback window
            winkb_helper.press('WIN+D')
            logging.info("Maximized the window")

            ##
            # Wait for 10 seconds after maximizing
            time.sleep(10)

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
    # @brief        Test to verify MPO functionality when media is paused and replayed
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'PLAY_PAUSE',
                     "Skip the test step as the scenario type is not play pause")
    def test_05_play_pause(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])

        app_instance_2 = planes_ui_helper.create_app_instance(self.app[1]) if len(self.app) > 1 else None

        app_instance_list = [app_instance_1] if app_instance_2 is None else [app_instance_1, app_instance_2]

        for app_instance in app_instance_list:
            ##
            # Play the app(s) in windowed mode
            app_instance.open_app(is_full_screen=False, minimize=True)
            ##
            # Pause video
            winkb_helper.press(' ')
            logging.info("Paused the video")

            ##
            # Wait for 20 seconds after pause
            time.sleep(20)

            ##
            # Play video
            winkb_helper.press(' ')
            logging.info("Continue playing the video")

            ##
            # Wait for 20 seconds after play
            time.sleep(20)

            # Close media player
            app_instance.close_app()
            time.sleep(2)

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id, adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to verify MPO functionality during single/multiple app scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)