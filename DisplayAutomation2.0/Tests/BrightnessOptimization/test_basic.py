########################################################################################################################
# @file         test_basic.py
# @brief        Test to verify ELP with user requested optimization level
# @author       Tulika
########################################################################################################################
import unittest

from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import BrtOptimizationBase
from Tests.PowerCons.Modules import common, dut
from Tests.BrightnessOptimization import brightness_optimization as brt


##
# @brief        This class contains test to validate ELP status in driver
class TestBasic(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function validates ELP status in driver
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_brt_optimization_basic(self):
        status = True
        skip_igcl_for_elp= False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_elp = True
                status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                     brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                     brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)

        if status is False:
            self.fail()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestBasic))
    test_environment.TestEnvironment.cleanup(test_result)
