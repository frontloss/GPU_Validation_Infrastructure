########################################################################################################################
# @file         test_power_events.py
# @brief        Test for BRT Optimization power event (CS/S3/S4) scenario
#
# @author       Tulika
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *


##
# @brief        This class contains test cases for Brightness Optimization with power events
class BrtPowerEvent(BrtOptimizationBase):
    ##
    # @brief        This function verifies Brightness Optimization with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_11_s3_cs(self):
        test_status = True
        skip_igcl_for_elp = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_elp = True

                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                          brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                          brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)

                invoke_power_event(self,"CS")

                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                          brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                          brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)
                if test_status is False:
                    self.fail(f"FAIL: BRT OPTIMIZATION feature verification with CS")
                logging.info(f"PASS: BRT OPTIMIZATION feature verification with CS")

    ##
    # @brief        This function verifies Brightness Optimization with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_12_s4(self):
        test_status = True
        skip_igcl_for_elp = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_elp = True

                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                          brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                          brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)

                invoke_power_event(self, "S4")

                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                          brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                test_status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                          brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)
                if test_status is False:
                    self.fail("FAIL: BRT OPTIMIZATION feature verification with S4")
                logging.info("PASS: BRT OPTIMIZATION feature verification with S4")


##
# @brief        This is a helper function to verify Brightness Optimization with the provided power event
# @param[in]    event_type enum PowerEvent
# @return       None
def invoke_power_event(self, event_type):
    display_power_ = display_power.DisplayPower()
    power_event = display_power.PowerEvent[event_type]
    logging.info(f"\tInitiating power event {event_type}")
    if display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
        self.fail(f"FAILED to initiate and resume from {event_type} (Test Issue)")
    logging.info(f"\tSuccessfully resumed from {event_type}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BrtPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
