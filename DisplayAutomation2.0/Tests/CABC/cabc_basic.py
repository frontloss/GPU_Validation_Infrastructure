########################################################################################################################
# @file         cabc_basic.py
# @brief        Test to verify CABC with user requested optimization level
# @author       Tulika
########################################################################################################################
import logging
import random
import unittest

from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Core import display_power, display_essential
from Tests.CABC import cabc
from Tests.CABC.cabc_base import CabcBase
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Modules import common, dut, workload


##
# @brief        This class contains test to validate CABC status in driver
class CabcBasic(CabcBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function validates CABC status in driver
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_cabc = False
                if (cabc.optimization_params[panel.port].feature_2.level is not None and
                        cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                            panel.port].feature_2.level):
                    skip_igcl_for_cabc = True

                if self.os_option is not None:
                    for trial in range(2):
                        toggle_status, pwr_src = cabc.toggle_power_source()
                        if toggle_status is False:
                            self.fail(f"FAILED to toggle power source")
                        status, new_level = cabc.set_optimization_level(self.feature_to_enable[panel.port])
                        if status is False:
                            gdhm.report_driver_bug_pc(f" Failed to set {new_level} optimization level via IGCL")
                            self.fail(f"FAILED to set Optimization level")
                        test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                                   new_level, skip_igcl_for_cabc, self.os_option, pwr_src)
                        test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                                   new_level, skip_igcl_for_cabc, self.os_option, pwr_src)
                else:
                    test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                               cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc,
                                               self.os_option)
                    test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                               cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc,
                                               self.os_option)

        if test_status is False:
            self.fail(f"FAIL: CABC feature verification failed")
        logging.info(f"PASS:  CABC feature verification passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CabcBasic))
    test_environment.TestEnvironment.cleanup(test_result)
