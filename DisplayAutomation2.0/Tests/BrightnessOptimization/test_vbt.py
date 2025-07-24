########################################################################################################################
# @file         test_vbt.py
# @brief        Test for Brightness Optimization test with different optimization level in VBT
# @author       Simran Setia
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Libs.Feature.powercons import registry


##
# @brief        This class contains Brightness Optimization verification with different opt level in VBT
#               This class inherits the BrtOptimizationBase class.


class BrtVbtUpdate(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function verifies Brightness Optimization features with different opt level in VBT
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_brt_opt_vbt_update(self):
        skip_igcl_for_elp = False
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Changing level in vbt Minimum=1, Medium =2, Maximum=3
                opt_level_in_vbt = [1, 2, 3]
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[
                    panel.port].feature_2.level:
                    skip_igcl_for_elp = True

                for level in opt_level_in_vbt:
                    if brt.optimization_params[panel.port].feature_1.level == level:
                        continue
                    status, do_driver_restart = brt.configure_level_in_vbt(adapter, panel,
                                                                           brt.optimization_params[
                                                                               panel.port].feature_1.name, level)
                    if status is False:
                        self.fail("FAIL: Optimization level not updated in VBT")

                    # Deleting persistence RegKey for ELP to reflect VBT changes in IGCL
                    if brt.optimization_params[panel.port].feature_1.name == 'ELP':
                        status = registry.delete(adapter.gfx_index, key="ElpUserPreference")

                    # Deleting persistence RegKey for APD to reflect VBT changes in IGCL
                    elif brt.optimization_params[panel.port].feature_1.name == 'APD':
                        status = registry.delete(adapter.gfx_index, key="ApdUserPreference")

                    if do_driver_restart or status:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            self.fail("Failed to restart display driver after VBT update")
                        vbt.Vbt(adapter.gfx_index).reload()

                    if brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                  level, skip_igcl_for_elp):
                        logging.info(f"PASS: {brt.optimization_params[panel.port].feature_1.name} feature "
                                     f"verification successful post VBT update")
                    else:
                        self.fail(f"FAIL: {brt.optimization_params[panel.port].feature_1.name} feature "
                                  f"verification failed post VBT update")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BrtVbtUpdate))
    test_environment.TestEnvironment.cleanup(test_result)
