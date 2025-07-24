########################################################################################################################
# @file         idd_basic.py
# @brief        This test script contains basic test for IDD
#                   * Enable testsigning
#                   * Install IDD driver using devcon method
#                   * Verify an IDD monitor is enumerated using QDC
#                   * Uninstall the IDD driver using devcon method
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import unittest

from Libs import env_settings
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger, etl_tracer, gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.Yangra import virtual_display_helper
from Tests.VirtualDisplay.Yangra.IDD.idd_base import IDDBase


##
# @brief    This class contains basic test for IDD
class IDDBasic(IDDBase):

    ##
    # @brief        Unittest runTest function
    # @return       None
    def runTest(self):
        logging.info("Step: Enable TestSigning")
        if virtual_display_helper.enable_disable_testsigning(virtual_display_helper.TestSigning.ENABLE) is False:
            gdhm.report_test_bug_os(f"{virtual_display_helper.GDHM_IDD} Test Signing not enabled")
            self.fail("")

        logging.info("Step: Install IDD Driver")
        if virtual_display_helper.install_uninstall_idd_driver(virtual_display_helper.IddDriver.INSTALL,
                                                               self.monitor_resolution) is False:
            gdhm.report_test_bug_os(f"{virtual_display_helper.GDHM_IDD} IDD Driver not installed")
            self.fail("")

        logging.info("Step: Verify IDD Display Enumeration")
        if virtual_display_helper.verify_idd_display_enumeration(self.monitor_resolution) is False:
            gdhm.report_driver_bug_os(f"{virtual_display_helper.GDHM_IDD} IDD Displays are not enumerated")
            self.fail("")


if __name__ == '__main__':
    env_settings.set('SIMULATION', 'simulation_type', 'NONE')
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    virtual_display_helper.initialize(sys.argv)
    etl_tracer._register_trace_scripts()
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
