##
# @file         dxflips_basic.py
# @brief        This test script verifies flips are submitted in async / sync mode.
#               Test consists of below scenarios:
#               * Plays FlipAt app maximized/windowed mode with higher fps than RR.
#               * Plays FlipAt app maximized/windowed mode with lower fps than RR.
#               * Plays FlipAt app maximized/windowed mode with switch between higher/lower fps than RR.
#               * Plays FLipAt/TrivFlip/FlipModelD3D12 app in windowed mode .
#               * Plays FLipAt/TrivFlip/FlipModelD3D12 app and media app in fullscreen mode.
# @author       Sunaina Ashok

import logging
import sys
import unittest
import ctypes
from Libs.Core import enum
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper, flip_verification
from Tests.Flips.Dxflips import dxflips_base

##
# @brief    Contains test functions that are used to verify flips submitted in Async and sync mode
class DxflipsBasic(dxflips_base.DxflipsBase):

    ##
    # @brief    Test function to verify AsyncFlips while app is playing in windowed mode
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "WINDOWED",
                     "Skip the test step as the action type is not playing app in windowed mode")
    # @endcond
    def test_01_windowed_3DApp(self):
        etl_file = flip_helper.run_dx_app(self.app, self.fps, False, self.feature)

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                monitor_info = control_api_args.ctl_intel_arc_sync_monitor_params_t()
                monitor_info.Version = 0
                monitor_info.Size = ctypes.sizeof(monitor_info)

                logging.info(f"Monitor_info: {monitor_info}")
                logging.info(f"Panel_target_id : {panel.target_id}")
                if control_api_wrapper.get_intel_arc_sync_info(monitor_info, panel.target_id):
                    logging.info("Pass: Get Monitor Info from Control Library")
                    max_rr = monitor_info.MaximumRefreshRateInHz
                    min_rr = monitor_info.MinimumRefreshRateInHz
                    logging.info(f"IsIntelArcSyncSupported (VRR) : {monitor_info.IsIntelArcSyncSupported} Min RR:{min_rr} MaxRR: {max_rr}")

                # getting the RR for the current panel
                mode = self.display_config.get_current_mode(panel.target_id)
                self.refreshRate = mode.refreshRate
                logging.info(f'Active Refresh Rate for {panel.connector_port_type} : {self.refreshRate}')

                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe, (self.eg_mode, self.refreshRate, monitor_info.IsIntelArcSyncSupported)) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if (self.context_args.test.cmd_params.topology == enum.CLONE or self.context_args.test.cmd_params.topology == enum.EXTENDED) and self.feature == "ENDURANCE_GAMING":
                    break

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief    Test function to verify AsyncFlips while app is playing in fullscreen mode
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "FULLSCREEN",
                     "Skip the test step as the action type is not playing app in Fullscreen")
    # @endcond
    def test_02_fullscreen(self):
        etl_file = flip_helper.run_dx_app(self.app, self.fps, True, self.feature)


        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                monitor_info = control_api_args.ctl_intel_arc_sync_monitor_params_t()
                monitor_info.Version = 0
                monitor_info.Size = ctypes.sizeof(monitor_info)

                logging.info(f"Monitor_info: {monitor_info}")
                logging.info(f"Panel.target_id : {panel.target_id}")
                if control_api_wrapper.get_intel_arc_sync_info(monitor_info, panel.target_id):
                    logging.info("Pass: Get Monitor Info from Control Library")
                    max_rr = monitor_info.MaximumRefreshRateInHz
                    min_rr = monitor_info.MinimumRefreshRateInHz
                    logging.info(f"get_intel_arc_sync_info : Min RR:{min_rr} MaxRR: {max_rr}")
                    logging.info(f"IsIntelArcSyncSupported : {monitor_info.IsIntelArcSyncSupported}")

                # getting the RR for the current panel
                mode = self.display_config.get_current_mode(panel.target_id)
                self.refreshRate = mode.refreshRate
                logging.info(f'Refresh Rate for {panel.connector_port_type} : {self.refreshRate}')

                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe, (self.eg_mode, self.refreshRate, monitor_info.IsIntelArcSyncSupported)) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.feature == 'VSYNC_ON' and self.app == 'FLIPMODELD3D12':
                    if flip_verification.verify_vsync_rate(etl_file, panel.pipe, flip_helper.get_app_name(self.app)) \
                            is False:
                        flip_helper.report_to_gdhm(self.feature, "VSync reporting rate is not matching with RR of "
                                                                 "Panel")
                        self.fail("Rate at which VSync reporting is not matching with RR of panel")

                if (self.context_args.test.cmd_params.topology == enum.CLONE or self.context_args.test.cmd_params.topology == enum.EXTENDED) and self.feature == "ENDURANCE_GAMING":
                    break

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify Async Flips related features functionality while running any application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)