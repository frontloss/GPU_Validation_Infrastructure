########################################################################################################################
# @file         virtual_display_multi_atsm.py
# @brief        To verify if Multi Virtual Display is enabled and enumerated correctly
# @author       Pai Vinayak1
########################################################################################################################
import logging
import os
import shutil
import sys
import time
import unittest

from Libs import env_settings
from Libs.Core import reboot_helper, display_essential
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger, etl_tracer
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.Yangra import virtual_display_helper

TARGET_ID = ['20117C', '20227C', '20337C', '20447C']


##
# @brief   It contains methods to verify multi virtual display in headless mode
class VirtualDisplayATSM(unittest.TestCase):

    ##
    # @brief        Setup - Starts the etl event
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        virtual_display_helper.enable_disable_regkey(virtual_display_helper.Status.ENABLE)
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart the driver")

        # Plug the Displays using IGCL Edid Mgmt API
        for target_id in TARGET_ID:
            logging.info(f"Attaching display with TargetID: {target_id}")
            virtual_display_helper.run_powershell_cmd(f"{virtual_display_helper.SAMPLE_APPS_PATH} -lock -t {target_id}")

        if etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT) is False:
            logging.info("failed to start etl")
            return False
        if reboot_helper.reboot(self, callee="test_after_reboot") is False:
            self.fail("Failed to reboot the system(Test Issue)")

    ##
    # @brief        Unittest test_after_reboot function - To perform verification after reboot scenario
    # @return       None
    def test_after_reboot(self):
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

        status = virtual_display_helper.verify_multi_virtual_display(new_boot_etl_file)

        if status is False:
            self.fail("Multi Virtual display verification failed")
        else:
            logging.info("Multi Virtual display verification passed")

    ##
    # @brief        This method logs teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        virtual_display_helper.enable_disable_regkey(delete=True)
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart the driver")

        virtual_display_helper.run_powershell_cmd(f"{virtual_display_helper.SAMPLE_APPS_PATH} -unlock")

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
        "Test purpose: To verify if Multi Virtual Display is enabled and enumerated correctly")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
