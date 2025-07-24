import os
import sys
import logging
import time
import unittest
import xml.etree.ElementTree as ET

from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core import test_header
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import display_logger
from Libs.Core.gta import gta_state_manager
from Libs.Core.test_env import test_environment


def test_executed_before_boot(test_name):
    return False


class etl_tracer_reboot_ult(unittest.TestCase):

    def setUp(self):
        logging.info("ULT Start")

    @unittest.skip("API broken due to non-generation of ETL from driver")
    def test_tracing_across_reboot(self):
        def before_reboot():
            etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT)
            logging.info("Reboot is required. Post Reboot Call stop_trace_with_boot")

        def after_reboot():
            ret = etl_tracer.stop_etl_tracer()
            self.assertTrue(ret, "ETL generation failed for reboot scenario!!")

        if test_executed_before_boot(self._testMethodName) is True:
            after_reboot()
        else:
            before_reboot()

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
