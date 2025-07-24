########################################################################################################################
# @file         async_flip_latency.py
# @brief        Test submits async flips and computes flip to flip-done time from ETL
#               * Run FlipAt with more than 600 FPS
#               * Capture ETL
#               * Parse ETL to measure Flip-NotifyVSync time
# @author       Joshi, Prateek
########################################################################################################################
import os
import time
import logging
import sys
import unittest

from Libs.Core import enum, winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper
from Tests.Flips.Dxflips import dxflips_base


##
# @brief    Contains test functions that are used to verify flips submitted are Async and measure async flip latency
class AsyncFlipLatency(dxflips_base.DxflipsBase):

    ##
    # @brief    Test function to verify app is running in Async, fullscreen mode and measure async flip latency
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "FULLSCREEN",
                     "Skip the test step as the action type is not playing app in Fullscreen")
    # @endcond
    def test_01_fullscreen(self):

        self.change_power_plan(self.power_plan)

        bfullscreen = True
        mode = "fullscreen" if bfullscreen else "windowed"
        logging.info(f"Opening App {self.app} in {mode} mode")

        # Minimize all windows
        winkb_helper.press('WIN+M')

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        # Open any app
        flip_helper.play_app(self.app, bfullscreen=bfullscreen, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)

        # Start ETL capture
        etl_file_name = "Before_fullscreen_scenario" if bfullscreen else "Before_windowed_scenario"
        if flip_helper.start_etl_capture(etl_file_name) is False:
            assert False, "FAIL: Failed to start GfxTrace"

        # App will run for one minute
        time.sleep(60)

        # Stop ETL Trace
        etl_file_name = "After_fullscreen_scenario" if bfullscreen else "After_windowed_scenario"
        etl_file = flip_helper.stop_etl_capture(etl_file_name)

        # Close the application
        flip_helper.close_app(self.app)
        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_async_flip_latency(self.feature, etl_file, panel.pipe) is False:
                    self.fail("verify_async_flip_latency failed !! ")

    ##
    # @brief    Helper Function to change the power plan
    # @param    power_plan - power plan
    # @return   None
    # @cond
    # @endcond
    def change_power_plan(self, power_plan):
        # Power Plan GUID
        power_plans = {
            'PERFORMANCE': '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
            'BALANCE': '381b4222-f694-41f0-9685-ff5bb260df2e',
            'SAVER': 'a1841308-3541-4fab-bc81-f71556f20b4a'
        }

        # Power plan check
        if power_plan not in power_plans:
            logging.warning(f"Invalid power plan name: {power_plan}, continuing with balanced power plan")

        # Set Power Plan
        os.system(f'powercfg /s {power_plans[power_plan]}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Submit Async flips and measure flip to flip done time")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
