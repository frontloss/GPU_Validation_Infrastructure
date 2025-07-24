########################################################################################################################
# @file         fms_cs_s3.py
# @brief        This file contains tests for FMS verification after CS/S3 power event
# @author       Tulika
########################################################################################################################

import os
import shutil
import time

from Libs.Core import display_power, enum
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.FMS import fms
from Tests.LFP_Common.FMS.fms_base import *
from Tests.PowerCons.Modules import common

##
# @brief        This class contains tests for FMS verification after CS/S3 power event. It inherits the LfpFmsBase clas


class LfpFmsCsS3(LfpFmsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verfies FMS after CS/S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3", "POST_SI"])
    # @endcond
    def runTest(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_event = display_power.PowerEvent.CS
        else:
            power_event = display_power.PowerEvent.S3

        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event %s' % power_event.name)

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
                result = fms.verify_fms_during_power_events(new_boot_etl_file, panel.transcoder, adapter.name, panel.target_id, True)
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
