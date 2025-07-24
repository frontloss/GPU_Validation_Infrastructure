########################################################################################################################
# @file         cmtg_driver_enable_disable.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification with display driver disable/enable.
# @author       Bhargav Adigarla
########################################################################################################################
import logging
import os
import time

from Libs.Core import display_essential
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_environment, test_context
from Tests.PowerCons.Functional.CMTG.cmtg_base import *


##
# @brief        Contains CMTG driver restart tests
class CmtgDriverRestart(CmtgBase):
    ##
    # @brief        This function verifies CMTG before driver disable/enable
    # @return       None
    def t_10_before_driver_restart(self):
        etl_tracer.stop_etl_tracer()
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTraceBeforeDriverRestart.' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")
        for adapter in dut.adapters.values():
            logging.info("Step: Restart display driver for {adapter.name}")
            try:
                if display_essential.disable_driver(adapter.gfx_index) is False:
                    self.fail("Failed to disable display driver for {0}".format(adapter.gfx_index))
                driver_disable_etl = end_capture('GfxTrace_during_driver_disable')
            except Exception as e:
                self.fail(e)
            finally:
                if display_essential.enable_driver(adapter.gfx_index) is False:
                    self.fail("Failed to enable display driver for {0}".format(adapter.gfx_index))
            logging.info("\tPASS: Restarted display driver successfully")
            etl_file = end_capture('GfxTrace_during_driver_enable')
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if cmtg.verify(adapter, [panel]) is False:
                    logging.error("CMTG verification failed after driver restart")
                    self.fail("CMTG verification failed after driver restart")
                logging.info(f"PASS: CMTG verification successful on {panel.port}")
                if cmtg.verify_cmtg_reg_access(adapter, panel, etl_file) is False:
                    self.fail("CMTG registers check failed")
                logging.info(f"PASS: CMTG registers read check after CLK enable on {panel.port}")


##
# @brief        Helper function to stop the etl tracer
# @param[in]    name string name of the etl file
# @return       True if ETL tracer stop is successful, False otherwise
def end_capture(name):
    assert etl_tracer.stop_etl_tracer(), "Failed to start etl trace"
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
    test_result = runner.run(common.get_test_suite(CmtgDriverRestart))
    test_environment.TestEnvironment.cleanup(test_result)