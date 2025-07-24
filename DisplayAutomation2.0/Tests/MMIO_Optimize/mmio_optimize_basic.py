########################################################################################################################
# @file         mmio_optimize_basic.py
# @brief        The test script contains basic test to verify MMIO Optimization when DC6v and FlipQ is enabled
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import os
import sys
import time
import unittest

from Libs.Core import cmd_parser, window_helper, display_essential
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.app import AppMedia
from Tests.FlipQ import flipq_helper
from Tests.MMIO_Optimize import mmio_optimize
from Tests.PowerCons.Functional.DCSTATES import dc_state
from Tests.PowerCons.Modules import dut

LINE_WIDTH = 64


##
# @brief    This class contains basic test for MMIO optimization
class MmioOptimize(unittest.TestCase):

    ##
    # @brief        Unittest setUp function
    # @return       None
    def setUp(self):
        logging.info("TEST STARTS HERE".center(LINE_WIDTH, '*'))
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        dut.prepare()
        for adapter in dut.adapters.values():
            status = dc_state.enable_dc6v(adapter)
            if status is False:
                self.fail("FAILED to enable DC6v via DisplayPcFeatureControl registry")
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("Failed to restart display driver")

    ##
    # @brief        Unittest runTest function
    # @return       None
    def runTest(self):
        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_Fullscreen_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in Full Screen mode
        app_media = AppMedia(os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos/24.000.mp4"))
        app_media.open_app(True, minimize=True)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Close media player
        window_helper.close_media_player()

        ##
        # Stop ETL capture
        media_playback_etl = flipq_helper.stop_etl_capture("After_fullscreen_scenario")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                cmtg_status = mmio_optimize.cmtg_enable_status(adapter)
                result, register_offsets = mmio_optimize.verify_mmio_data(media_playback_etl, panel, adapter,
                                                                          cmtg_status)
                if result is False:
                    logging.error("FAIL: MMIO Optimization verification failed")
                    logging.error(f"Read/Write Register List : {register_offsets}")
                    gdhm.report_driver_bug_os(
                        title=f"[MMIO Optimization] Detecting MMIO Access when FlipQ and Dc6V is enabled",
                        priority=gdhm.Priority.P1,
                        exposure=gdhm.Exposure.E1)
                else:
                    logging.info("PASS: MMIO Optimization verification passed")

    ##
    # @brief        unittest tearDown function
    # @return       None
    def tearDown(self):
        logging.info("TEST ENDS HERE".center(LINE_WIDTH, '*'))
        dut.reset()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to verify MMIO Optimization when DC6v and FlipQ is enabled")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
