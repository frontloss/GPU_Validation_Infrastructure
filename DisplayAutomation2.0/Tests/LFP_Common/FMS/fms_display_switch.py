########################################################################################################################
# @file         fms_display_switch.py
# @brief        This file contains tests for FMS verification after display switch
# @author       Tulika
########################################################################################################################

import os
import shutil
import time

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.FMS import fms
from Tests.LFP_Common.FMS.fms_base import *


##
# @brief        This class contains tests for FMS verification after display switch
class LfpFmsDisplaySwitch(LfpFmsBase):
    display_power_ = display_power.DisplayPower()
    display_config_ = display_config.DisplayConfiguration()

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verfies FMS after display switch
    # @return       None
    def runTest(self):

        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        self.lfp_panels = []
        self.external_panels = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    self.lfp_panels.append(panel.port)
                else:
                    self.external_panels.append(panel.port)

        disp_config_flow = [[enum.SINGLE, self.external_panels[0]],
                            [enum.SINGLE, self.lfp_panels[0]]]

        for disp_conf in disp_config_flow:
            logging.info("Step: Setting display configuration {0} {1}".format(
                DisplayConfigTopology(disp_conf[0]).name, ' '.join(disp_conf[1:])))
            if self.display_config_.set_display_configuration_ex(disp_conf[0], disp_conf[1:]) is False:
                self.fail("Failed to set display configuration {0} {1} (Test Issue)".format(
                    DisplayConfigTopology(disp_conf[0]).name, ' '.join(disp_conf[1:])))
            logging.info("\tSet display configuration successfully")

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")

        file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
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
                    if result != "FULL_MODE_SET":
                        gdhm.report_driver_bug_di(f"{fms.GDHM_FMS} ModeSet Expected= FULL_MODE_SET, Actual= {result}")
                        self.fail(f"FAIL: ModeSet Expected= FULL_MODE_SET, Actual= {result}")
                    logging.info("PASS: ModeSet Expected= FULL_MODE_SET, Actual= FULL_MODE_SET")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
