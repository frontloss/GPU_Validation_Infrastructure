########################################################################################################################
# @file         test_ac_dc.py
# @brief        Test for BRT Optimization power source (AC/DC) scenario
#
# @author       Tulika
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains Brightness Optimization verification in AC/DC switch
#               This class inherits the BrtOptimizationBase class.


class BrtAcDcSwitch(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Brightness verification in AC/DC switch
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC"])
    # @endcond
    def t_11_power_ac_dc(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_elp = False
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_elp = True
                for trial in range(3):
                    for src in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
                        if self.verify_with_power_source(adapter, panel, src, skip_igcl_for_elp) is False:
                            status = False
                            logging.error(f"FAIL: BRT OPTIMIZATION feature verification failed in {src.name} mode")
                        else:
                            logging.info(f"PASS: BRT OPTIMIZATION feature verification passed in {src.name} mode")

        if status is False:
            self.fail(f"FAIL: BRT OPTIMIZATION features persistence failed post AC_DC switch")
        logging.info(f"PASS: BRT OPTIMIZATION features persistence passed post AC_DC switch")

    ##
    # @brief        Brightness Optimization verification in AC/DC switch
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    power_source
    # @param[in]    skip_igcl_for_elp
    # @return       None
    def verify_with_power_source(self, adapter, panel, power_source, skip_igcl_for_elp):
        status = True
        if workload.change_power_source(power_source) is False:
            logging.error(f"Failed to switch power source {power_source}")
            return False

        if brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                      brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp, power_source) is False:
            status = False

        if brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                      brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp, power_source) is False:
            status = False

        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BrtAcDcSwitch))
    test_environment.TestEnvironment.cleanup(test_result)
