#################################################################################################################
# @file         powerwell_basic.py
# @brief        Contains test for powerwell register programming verification.
#               This script is meant to cover corner cases which are not covered with DE verification. Some of them
#               are given below:
#               - TGL dual eDP
#               - Non audio capable panels
#
# @author       Rohit Kumar
#################################################################################################################

import logging
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_powerwell import powerwell
from Tests.PowerCons.Modules import dut, common

##
# @brief        This class contains powerwell register programming verification tests


class PowerWellBasicTest(unittest.TestCase):

    ##
    # @brief        This class method is the entry point for power test cases. Helps to initialize some of the
    #               parameters for the execution of powerwell test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: POWERWELL_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.prepare()

    ##
    # @brief        This method is the exit point for powerwell test cases. This resets the environment changes done
    #               for the powerwell test execution
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: POWERWELL_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other powerwell
    #               test functions. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info("Panel Capabilities for {0}".format(panel))
                logging.info("\t{0}".format(panel.vdsc_caps))

    ##
    # @brief        Test function for basic powerwell verification
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_basic(self):
        for adapter in dut.adapters.values():
            panel_str = str([panel.port for panel in adapter.panels.values()])
            if powerwell.verify_adapter_power_well(adapter.gfx_index) is False:
                self.fail("PowerWell verification failed with {0} on {1}".format(panel_str, adapter.name))


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PowerWellBasicTest))
    TestEnvironment.cleanup(test_result)
