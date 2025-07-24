import logging
import sys
import time
import unittest

from Libs.Core.logger import etl_tracer
from Libs.Core.display_power import *
from Libs.Core.logger import display_logger
from Libs.Core.test_env import test_environment
from Libs.Core.gta import gta_state_manager
from Libs.Core import test_header


def etl_tracer_ult(trace_level):
    ret = etl_tracer.start_etl_tracer(tracing_options=trace_level)
    if not ret:
        return ret

    time.sleep(60)
    ret = etl_tracer.stop_etl_tracer()
    return ret


class etl_trace_ult(unittest.TestCase):
    log_handle = None
    display_power = DisplayPower()

    def setUp(self):
        logging.info("ULT Start")

    def test_0_1_sanity_check_trace_all(self):
        ret = etl_tracer_ult(etl_tracer.TraceType.TRACE_ALL)
        self.assertTrue(ret, "Sanity check for TRACE_ALL enum failed!!")

    def test_0_2_sanity_check_trace_lite(self):
        ret = etl_tracer_ult(etl_tracer.TraceType.TRACE_LITE)
        self.assertTrue(ret, "Sanity check for TRACE_LITE enum failed!!")

    def test_0_3_sanity_check_ddi_trace(self):
        ret = etl_tracer_ult(etl_tracer.TraceType.DDI_TRACE)
        self.assertTrue(ret, "Sanity check for DDI_TRACE enum failed!!")

    def test_0_4_sanity_check_ddi_trace(self):
        ret = etl_tracer_ult(etl_tracer.TraceType.DXGKRNL_TRACE)
        self.assertTrue(ret, "Sanity check for DXGKRNL_TRACE enum failed!!")

    def test_0_5_sanity_check_pc_trace(self):
        ret = etl_tracer_ult(etl_tracer.TraceType.TRACE_PC_ONLY)
        self.assertTrue(ret, "Sanity check for TRACE_PC_ONLY enum failed!!")

    def todo_0_6_trace_with_boot_before(self):
        etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT)
        logging.info("Reboot is required. Post Reboot Call stop_trace_with_boot")
        ##
        # Invoke System Restart
        self.display_power.invoke_power_event(PowerEvent.S5)

    def todo_0_7_trace_with_boot_after(self):
        ret = etl_tracer.stop_etl_tracer()
        self.assertTrue(ret, "ETL generation failed for reboot scenario!!")

    def todo_0_8_trace_with_boot_pc_before(self):
        etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT_PC_ONLY)
        logging.info("Reboot is required. Post Reboot Call stop_trace_with_boot")
        ##
        # Invoke System Restart
        self.display_power.invoke_power_event(PowerEvent.S5, 60)

    def todo_0_9_trace_with_boot_pc_after(self):
        ret = etl_tracer.stop_etl_tracer()
        self.assertTrue(ret, "ETL generation failed for reboot (PC Only) scenario!!")

    def tearDown(self):
        logging.info("ULT Complete")


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()
