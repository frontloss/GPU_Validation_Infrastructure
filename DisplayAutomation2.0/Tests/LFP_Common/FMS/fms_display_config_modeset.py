########################################################################################################################
# @file         fms_display_config_modeset.py
# @brief        This file contains tests for FMS verification after modeset on external display
# @author       Tulika
########################################################################################################################

import os
import shutil
import time

from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.FMS import fms
from Tests.LFP_Common.FMS.fms_base import *


##
# @brief        This class contains tests for FMS verification after modeset on external display
class LfpFmsDisplaySwitchModeset(LfpFmsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verfies FMS after display switch
    # @return       None
    def runTest(self):

        # Stop ETL Tracer from initialization
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")

        # Start ETL tracing for test
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    continue
                supported_mode_list = self.display_config_.get_all_supported_modes([panel.target_id])
                test_modes = []

                for key, values in supported_mode_list.items():
                    for i in values:
                        test_modes.append(i)

                resolution = self.display_config_.get_current_mode(panel.target_id)
                logging.info(f"Current mode= {resolution.HzRes}x{resolution.VtRes}@{resolution.refreshRate}")

                ##
                # Apply modes one by one
                for mode in test_modes:
                    if mode.refreshRate < resolution.refreshRate:
                        self.display_config_.set_display_mode([mode])
                        resolution = self.display_config_.get_current_mode(panel.target_id)
                        logging.info(f"Applied mode on external display is:"
                                     f"{resolution.HzRes}x{resolution.VtRes}@{resolution.refreshRate}")
                        break

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")

        file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            self.fail(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.port in ["MIPI_A", "DP_A"]:
                    result = fms.verify_fms(new_boot_etl_file, panel.transcoder, adapter.name)
                    if result is False:
                        gdhm.report_driver_bug_di(f"{fms.GDHM_FMS} Display is not active")
                        self.fail("FAIL: Display is not active")
                    if result != "FAST_MODE_SET":
                        gdhm.report_driver_bug_di(f"{fms.GDHM_FMS} ModeSet Expected= FAST_MODE_SET, Actual= {result}")
                        self.fail(f"FAIL: ModeSet Expected= FAST_MODE_SET, Actual= {result}")
                    logging.info("PASS: ModeSet Expected= FAST_MODE_SET, Actual= FAST_MODE_SET")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
