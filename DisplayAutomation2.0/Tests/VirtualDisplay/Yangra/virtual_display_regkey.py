########################################################################################################################
# @file         virtual_display_regkey.py
# @brief        Virtual Display Headless scenario is covered in below scenarios:
#               * Virtual Display verification in headless mode
#               * Virtual Display verification after adding 'ForceVirtualDisplay' regkey
# @author       Pai Vinayak1
########################################################################################################################
import logging
import os
import shutil
import sys
import time
import unittest

from Libs import env_settings
from Libs.Core import reboot_helper, registry_access, display_essential
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger, etl_tracer
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.Yangra import virtual_display_helper


##
# @brief   It contains methods to verify virtual display in headless mode
class VirtualDisplayRegkey(unittest.TestCase):

    ##
    # @brief        Setup - Starts the etl event
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
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

        file_name = "GfxTrace_regkey_" + str(time.time()) + ".etl"
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
        if virtual_display_helper.start_etl_capture("Before_regkey_addition") is False:
            self.fail("Failed to start ETL capture")

        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        registry_access.write(args=ss_reg_args, reg_name="ForceVirtualDisplay",
                              reg_type=registry_access.RegDataType.DWORD, reg_value=0)
        logging.info(f"Disabling ForceVirtualDisplay")

        status, _ = display_essential.restart_gfx_driver()

        ##
        # Stop ETL capture
        regkey_addition_etl = virtual_display_helper.stop_etl_capture("After_regkey_addition")

        status &= virtual_display_helper.verify_virtual_display(new_boot_etl_file, 'DEFAULT')
        status &= virtual_display_helper.verify_no_virtual_display(regkey_addition_etl)

        if status is False:
            self.fail("Virtual display verification failed")
        else:
            logging.info("Virtual display verification passed")

    ##
    # @brief        This method logs teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        registry_access.delete(ss_reg_args, "ForceVirtualDisplay")
        status, _ = display_essential.restart_gfx_driver()
        logging.info("ForceVirtualDisplay regkey deleted successfully")
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
        "Test purpose: To verify if Virtual Display is not enabled when disabled from regkey")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
