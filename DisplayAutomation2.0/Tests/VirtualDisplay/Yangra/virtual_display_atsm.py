########################################################################################################################
# @file         virtual_display_atsm.py
# @brief        Virtual Display Headless scenario is covered in below scenarios:
#               * Virtual Display verification in headless mode
#               * Custom Virtual Display verification for 19*10, 2k and 4k
#               * Vsync interval verification between each VBI enable and disable timings
# @author       Sunaina Ashok, Pai Vinayak1
########################################################################################################################
import logging
import os
import shutil
import sys
import time
import unittest

from Libs import env_settings
from Libs.Core import reboot_helper, cmd_parser
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger, etl_tracer
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.Yangra import virtual_display_helper

RESOLUTIONS_SUPPORTED = ['DEFAULT', '2K', '4K']


##
# @brief   It contains methods to verify virtual display in headless mode, custom virtual display and Vsync interval
class VirtualDisplayATSM(unittest.TestCase):
    custom_tags = ["-resolution"]

    ##
    # @brief        Setup - Starts the etl event
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        if self.cmd_line_param['RESOLUTION'] != 'NONE':
            self.display_resolution = self.cmd_line_param['RESOLUTION'][0]
        else:
            self.fail(f"Incomplete command line, please provide the display resolution {RESOLUTIONS_SUPPORTED}")
        if etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT) is False:
            logging.info("failed to start etl")
            return False
        if reboot_helper.reboot(self, callee="test_after_reboot") is False:
            self.fail("Failed to reboot the system(Test Issue)")

    ##
    # @brief        Unittest test_after_reboot function - To perform verification after reboot scenario
    # @return       None
    def test_after_reboot(self):
        status = True
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer (Test Issue)")

        file_name = "GfxTrace_atsm_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_BOOT_TRACE_ETL_FILE) is False:
            self.fail(etl_tracer.GFX_BOOT_TRACE_ETL_FILE + " NOT found (Test Issue)")

        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_BOOT_TRACE_ETL_FILE, new_boot_etl_file)

        ##
        # Start ETL capture
        if virtual_display_helper.start_etl_capture("Before_Fullscreen_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in Full Screen mode
        app_instance = virtual_display_helper.play_app("MEDIA")

        ##
        # Wait for a minute during video play
        time.sleep(60)

        ##
        # Close media player
        app_instance.close_app()

        ##
        # Stop ETL capture
        media_playback_etl = virtual_display_helper.stop_etl_capture("After_fullscreen_scenario")

        status &= virtual_display_helper.verify_virtual_display(new_boot_etl_file, self.display_resolution)
        status &= virtual_display_helper.calculate_vsync_interval(media_playback_etl)

        if status is False:
            self.fail("Virtual display verification failed")
        else:
            logging.info("Virtual display verification passed")

    ##
    # @brief        This method logs teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Cleanup Completed")


if __name__ == '__main__':
    env_settings.set('SIMULATION', 'simulation_type', 'NONE')
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    if virtual_display_helper.disable_msft_display_driver() is False:
        assert False, "Driver is not Disabled"
    virtual_display_helper.initialize(sys.argv)
    etl_tracer._register_trace_scripts()
    gta_state_manager.create_gta_default_state()
    logging.info(
        "Test purpose: To verify if Virtual Display is enabled with default/custom edid and Verify Vsync interval")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)