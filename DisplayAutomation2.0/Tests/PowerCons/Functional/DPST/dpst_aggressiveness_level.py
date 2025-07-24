########################################################################################################################
# @file         dpst_aggressiveness_level.py
# @brief        Tests for DPST/OPST verification with DpstAggressivenessLevel
#
# @author       Ashish Tripathi
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DPST.dpst_base import *


##
# @brief        This class contains tests for DPST/OPST with Aggressiveness Level
class DpstAggressivenessLevel(DpstBase):

    ##
    # @brief        This function verifies DPST/OPST with Aggressiveness Level
    #               1. Set Level 1 using RegKey
    #               2. Set Level 2 using IGCL if Gen13+ else use Regkey
    #               3. Set Level 3 using IGCL if Gen13+ else use Regkey
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_aggressiveness_level(self):
        power_source = self.display_power_.get_current_powerline_status()
        power_scheme = self.display_power_.get_current_power_scheme()
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # From MTL+, both DPST and OPST will have 3 aggressiveness levels
                if self.xpst_feature == dpst.XpstFeature.OPST or adapter.name not in common.PRE_GEN_14_PLATFORMS:
                    supported_levels = list(range(1, 4))
                else:
                    supported_levels = list(range(1, 7))

                for level in supported_levels:
                    if level in [2, 3] and adapter.name not in common.PRE_GEN_13_PLATFORMS:
                        if dpst.igcl_set_aggressiveness_level(panel, level, power_source, power_scheme) is False:
                            self.fail("FAILED to set Aggressiveness level")
                    else:
                        status = dpst.set_dpst_aggressiveness_level(adapter, level)
                        if status is False:
                            self.fail("FAILED to set Aggressiveness level")
                        if status is True:
                            result, reboot_required = display_essential.restart_gfx_driver()
                            if result is False:
                                self.fail(f"FAILED to restart display driver for {adapter.name}")

                    etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
                    if etl_file is False:
                        self.fail("FAILED to run the workload")

                    test_status &= self.validate_xpst(
                        etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)

            # currently DPST IGCL is global for all the panels so break after first iteration
            break

        if test_status is False:
            self.fail(f"FAIL: {self.xpst_feature_str} feature verification")
        logging.info(f"PASS: {self.xpst_feature_str} feature verification")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstAggressivenessLevel))
    test_environment.TestEnvironment.cleanup(test_result)
