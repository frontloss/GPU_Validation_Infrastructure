#######################################################################################################################
# @file         w2_driver_restart.py
# @brief        This file contains unit tests to validate Set Contect Latency (Window2/W2) feature.
# @details      Flow of the unit test is as follows
#               * Simulate required panels (As specified in the command line)
#               * Perform driver disable & enable operation
#               * Verify SCL is programmed in Vactive region
#
# @author       Chandrakanth Reddy
#######################################################################################################################

import logging
import os
import time
import unittest

from Libs.Core import display_essential, etl_parser
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dut


##
# @brief        Exposed Class to write W2 tests. Any new W2 test can inherit this class to use common setUp and
#               tearDown functions. W2Basic also includes some functions that can be used across all W2 tests.
class W2DriverRestart(unittest.TestCase):
    
    ##
    # @brief        This class method is the entry point for W2 test cases. Helps to initialize some of the
    #               parameters required for W2 test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        dut.prepare(pruned_mode_list=False)

    ##
    # @brief        This API contains the test to be run
    # @return       None
    def runTest(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"Skipping W2 verification on Pipe-{panel.pipe} as it is not VRR supported")
                    continue
                logging.info("Step: Restart display driver for {0}".format(adapter.name))
                if start_capture() is False:
                    self.fail("ETL Trace start Failed")
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
                etl_tracer.stop_etl_tracer()
                etl_file_path = end_capture('GfxTrace_during_driver_enable')
                if self.verify_scl_programming(adapter, panel, etl_file_path) is False:
                    self.fail("Set Context Latency verification failed")
                logging.info(f"PASS : Set Context Latency verification on {panel.port}")

    ##
    # @brief        This method is the exit point for W2 test cases. This resets the environment changes done
    #               for the execution of W2 tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()

    ##
    # @brief        This API contains SCL programming verification in active region
    # @param[in]    adapter: Adapter type
    # @param[in]    panel: Panel type
    # @param[in]    etl_file: ETL file path
    # @return       True if success else False
    def verify_scl_programming(self, adapter, panel,  etl_file):
        if os.path.exists(etl_file) is False:
            self.fail("{0} not found".format(etl_file))
        etl_parser.generate_report(etl_file)
        vbi_data = etl_parser.get_vbi_data('PIPE_' + panel.pipe)
        if vbi_data is None:
            logging.error("\tVBI data is empty")
            gdhm.report_driver_bug_pc("[PowerCons][W2] VBI Data is Empty in ETL")
            return False
        # 7F014h - 7F018h
        scl_data = etl_parser.get_mmio_data(0x6007C, is_write=True)
        if scl_data is None:
            logging.error("\t0x6007C mmio data not found in ETL file")
            gdhm.report_driver_bug_pc("[PowerCons][W2] 0x6007C mmio data not found in ETL file")
            return False
        vbi_time = vbi_data[0].TimeStamp
        scl_time = scl_data[0].TimeStamp

        if scl_time >= vbi_time:
            logging.error("\tSCL is programmed in VBI region")
            gdhm.report_driver_bug_pc("[PowerCons][W2] SCL is programmed in VBI region")
            return False
        logging.info(f'PASS: SCL is programmed in Vactive region')
        return True


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
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(W2DriverRestart)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
