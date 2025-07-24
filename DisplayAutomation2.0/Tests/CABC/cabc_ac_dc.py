########################################################################################################################
# @file         cabc_ac_dc.py
# @brief        Test to verify CABC with user requested optimization level
# @author       Tulika
########################################################################################################################
import logging
import unittest

from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.CABC import cabc
from Tests.CABC.cabc_base import CabcBase
from Tests.PowerCons.Modules import common, dut, workload


##
# @brief        This class contains test to validate CABC status in driver
class CabcAcDc(CabcBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function validates CABC status in driver
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_ac_dc_persistence(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_cabc = False
                if (cabc.optimization_params[panel.port].feature_2.level is not None and
                        cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                    panel.port].feature_2.level):
                    skip_igcl_for_cabc = True
                for trial in range(3):
                    for src in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
                        if self.verify_with_power_source(adapter, panel, src, skip_igcl_for_cabc) is False:
                            test_status = False
                            logging.error(f"FAIL: Feature verification failed in {src.name} mode")
                        else:
                            logging.info(f"PASS: Feature verification passed in {src.name} mode")
        if test_status is False:
            self.fail(f"FAIL: CABC persistence failed post AC_DC switch")
        logging.info(f"PASS: CABC persistence passed post AC_DC switch")

    ##
    # @brief        CABC verification in AC/DC switch
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    power_source
    # @param[in]    skip_igcl_for_cabc
    # @return       None
    def verify_with_power_source(self, adapter, panel, power_source, skip_igcl_for_cabc):
        status = True
        if workload.change_power_source(power_source) is False:
            logging.error(f"Failed to switch power source {power_source}")
            return False

        expected_level_feature_1 = cabc.optimization_params[panel.port].feature_1.level
        expected_level_feature_2 = cabc.optimization_params[panel.port].feature_2.level
        # In AC mode we have XPST as level 1, IGCL get call will always have OPST level due to existing bug
        level_in_ac_mode = 1
        if cabc.optimization_params[panel.port].feature_2.name is not None and power_source == display_power.PowerSource.AC:
            expected_level_feature_1 = expected_level_feature_2 = level_in_ac_mode

        if cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                       expected_level_feature_1, skip_igcl_for_cabc, pwr_src=power_source) is False:
            status = False

        if cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                       expected_level_feature_2, skip_igcl_for_cabc, pwr_src=power_source) is False:
            status = False

        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CabcAcDc))
    test_environment.TestEnvironment.cleanup(test_result)
