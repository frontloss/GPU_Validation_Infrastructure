########################################################################################################################
# @file         test_driver_restart.py
# @brief        Test for DMC load & unload during driver restart
#
# @author       Chandrakanth Reddy
########################################################################################################################

import os

from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment, test_context
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains tests to verify DMC with driver restarts
class DriverRestart(DCStatesBase):
    ##
    # @brief        This function verifies DMC load & unload during DriverRestart operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_driver_restart(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False or panel.psr_caps.is_psr_supported is False:
                    continue

                driver_disable_etl = None
                logging.info(f"Step: Restart display driver for {adapter.name}")
                if start_capture() is False:
                    self.fail("ETL Trace start Failed")
                try:
                    if display_essential.disable_driver(adapter.gfx_index) is False:
                        self.fail(f"Failed to disable display driver for {adapter.gfx_index}")
                    driver_disable_etl = end_capture('GfxTrace_during_driver_disable')
                except Exception as e:
                    self.fail(e)
                finally:
                    if display_essential.enable_driver(adapter.gfx_index) is False:
                        self.fail(f"Failed to enable display driver for {adapter.gfx_index}")
                logging.info("\tPASS: Restarted display driver successfully")
                etl_file = end_capture('GfxTrace_during_driver_enable')
                logging.info(f"Step: Verify during driver disable on {panel.port}")
                if dc_state.verify_dmc_unload(adapter, panel, driver_disable_etl) is False:
                    error_title = "DMC disable check during driver disable is Failed"
                    gdhm.report_driver_bug_pc("[PowerCons][DcState] " + error_title)
                    self.fail(error_title)
                logging.info(f"PASS: DMC disable verification during driver disable on {panel.port}")
                logging.info(f"Step: Verify after driver enable on {panel.port}")
                if dc_state.verify_dmc_load(adapter, panel, etl_file) is False:
                    error_title = "DMC enable check during driver enable is Failed"
                    gdhm.report_driver_bug_pc("[PowerCons][DcState] " + error_title)
                    self.fail(error_title)
                logging.info(f"PASS: DMC enable verification after driver restart on {panel.port}")


##
# @brief        Helper function to start the etl tracer
# @return       True if ETL tracer start is successful, False otherwise
def start_capture():
    assert etl_tracer.stop_etl_tracer(), "Failed to stop etl trace"
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceBefore_driver_disable_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False
    return True


##
# @brief        Helper function to stop the etl tracer
# @param[in]    name string name of the etl file
# @return       True if ETL tracer stop is successful, False otherwise
def end_capture(name):
    assert etl_tracer.stop_etl_tracer(), "Failed to stop etl trace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = name + '_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer after driver disable")
    return etl_file_path


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DriverRestart))
    test_environment.TestEnvironment.cleanup(test_result)