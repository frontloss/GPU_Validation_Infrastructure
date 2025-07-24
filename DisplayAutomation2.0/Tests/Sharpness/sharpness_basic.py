########################################################################################################################
# @file         sharpness_basic.py
# @brief        Basic test to verify Sharpness in different scenarios.
#                   * Exercise the below scenarios and verify Sharpness
#                       1. Fullscreen  playback
#                       2. Windowed - Media
#                       3. Open and Close - Media
# @author       Prateek Joshi
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper, display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.Sharpness import sharpness_helper, sharpness_verification
from Tests.Sharpness.sharpness_base import SharpnessBase


##
# @brief    Contains basic Sharpness tests
class SharpnessBasic(SharpnessBase):
    @unittest.skipIf(sharpness_helper.get_action_type('-SCENARIO') != 'FULLSCREEN',
                     "Skipping test step as the scenario type is not FULLSCREEN")
    ##
    # @brief        Test to verify Sharpness for app opened in Fullscreen mode
    # @return       None
    def test_01_fullscreen(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')

        app_instance_1.open_app(is_full_screen=True, minimize=True)
        ##
        # Wait for a minute during video playback
        time.sleep(60)
        ##
        # Close media player
        app_instance_1.close_app()

        ##
        # Stop ETL capture
        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during Fullscreen Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

    @unittest.skipIf(sharpness_helper.get_action_type('-SCENARIO') != 'WINDOWED',
                     "Skipping test step as the scenario type is not WINDOWED")
    ##
    # @brief        Test to verify Sharpness when playback in windowed_mode
    # @return       None
    def test02_app_windowed(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Play media/3D in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        ##
        # close the apps
        app_instance_1.close_app()

        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during Windowed Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

    @unittest.skipIf(sharpness_helper.get_action_type('-SCENARIO') != 'OPEN_AND_CLOSE',
                     "Skipping test step as the scenario type is not mode switch")
    ##
    # @brief        Test to verify plane enabling/disabling when multiple apps are opened/closed
    # @return       None
    def test03_open_and_close_app(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')

        ##
        # 1 app is enabled open and close in a loop of 10
        for i in range(10):
            app_instance_1.open_app(is_full_screen=False, minimize=False)
            time.sleep(60)
            app_instance_1.close_app()

        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during Open_Close Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

 ##
    # @brief        Test function to verify Speedframe during power events while app is running.
    # @return       None
    # @cond
    @unittest.skipIf(sharpness_helper.get_action_type('-SCENARIO') not in ["POWER_EVENT_S3", "POWER_EVENT_S4"],
                     "Skip the test step as the action type is not power event S3/S4")
    # @endcond
    def test_03_power_events(self):
        disp_power = display_power.DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_S4": display_power.PowerEvent.S4}

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Create app instances
        app_instance_1 = planes_ui_helper.create_app_instance('MEDIA')

        ##
        # Invoke power event
        if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
            sharpness_helper.report_to_gdhm("Failed to invoke power event {self.scenario}")
            self.fail("Failed to invoke power event {}".format(power_state_dict[self.scenario]))
        else:
            logging.info("Power event {} success".format(power_state_dict[self.scenario]))

        ##
        # Wait for 10 seconds after power event
        time.sleep(10)

        ##
        # 1 app is enabled open and close in a loop of 10
        app_instance_1.open_app(is_full_screen=False, minimize=False)
        time.sleep(60)
        app_instance_1.close_app()

        ##
        # Stop ETL Trace
        etl_file = sharpness_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_verification.verify_sharpness(etl_file, panel, self.strength, self.filter_type,
                                                           self.resolution) is False:
                    sharpness_helper.report_to_gdhm("Verification of Sharpness failed during Open_Close Scenario")
                    self.fail(f"Verification of Sharpness failed during {self.scenario} Scenario")

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to verify Sharpness functionality during media playback scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
