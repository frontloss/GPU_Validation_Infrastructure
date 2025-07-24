########################################################################################################################
# @file         blc_milli_nits_levels.py
# @brief        Test for granularity in milli nits brightness levels
#
# @author       Vinod D S
########################################################################################################################
import os
import shutil
import time

from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_context, test_environment
from Libs.Feature.blc import brightness

from Tests.PowerCons.Functional.BLC.blc_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains BLC tests for milli-nits granularity brightness levels
class BlcMilliNitsLevels(BlcBase):

    ##
    # @brief        This test verifies blc with milli nits levels
    # @return       None
    def test_blc_milli_nits_levels(self):
        self.setup_and_validate_blc()
        if self.is_high_precision is True:
            self.fail("This test is not applicable for High Precision Brightness (Test Issue)")

        if not (self.is_inf_nit_range or self.is_hdr_panel):
            self.fail("This test needs either HDR panel or INF nits range specified (Test Issue)")

        # Stop the ETL tracer
        etl_tracer.stop_etl_tracer()

        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            etl_file_path = os.path.join(test_context.LOG_FOLDER, 'GfxTraceBefore_' + str(time.time()) + '.etl')
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        logging.info("Starting PC ETL Tracer")
        if etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_PC_ONLY) is False:
            self.fail("FAILED to start PC ETL tracer (Test Issue)")

        brightness_list = []
        brightness.load_library()
        start_milli_nits = 200
        if self.is_inf_nit_range:
            if len(self.nit_ranges) > 0:
                # Calculate the mid value
                start_milli_nits = int(self.nit_ranges[0][0]) + \
                                   ((int(self.nit_ranges[0][0]) + int(self.nit_ranges[0][1])) // 2)
        start_milli_nits *= 1000

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    logging.info(f"Step: Applying milli-nits for {panel.port} on {adapter.gfx_index}")
                    for milli_nits in range(start_milli_nits, start_milli_nits + 100):
                        # Applying milli nits values
                        logging.info(f"\tApplying milli-nits= {milli_nits}")
                        brightness_list.append(milli_nits)

                        if blc.set_brightness3(panel.gfx_index, panel.target_id, milli_nits, 200) is False:
                            logging.error(f"\t\tFAILED to apply milli-nits= {milli_nits}")
                            status = False
                        else:
                            logging.info(f"\t\tSuccessfully applied milli-nits= {milli_nits}")
                        time.sleep(4)

        etl_status, new_etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuring_MilliNitsLevels")
        if etl_status is False:
            self.fail("FAILED to get ETL")

        if status is False:
            self.fail("FAILED to set milli nits brightness")

        blc_args = [
            self.is_pwm_based, self.nit_ranges, self.is_high_precision, self.hdr_state, brightness_list,
            self.lfp1_port, self.disable_boost_nit_ranges, self.is_invalid_inf_nit_range, self.disable_nits_brightness,
            self.independent_brightness
        ]

        for adapter in dut.adapters.values():
            blc_status = blc.verify(adapter, self.cmd_test_name, new_etl_file, blc_args, remove_redundant_ddi=False)
            if blc_status is None:
                self.fail("FAILED to get DiAna result (Test Issue)")
            if blc_status is False:
                self.fail("FAIL: MilliNitsLevels verification failed")
            logging.info("PASS: MilliNitsLevels verification passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcMilliNitsLevels'))
    test_environment.TestEnvironment.cleanup(outcome)
