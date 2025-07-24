########################################################################################################################
# @file         cabc_power_events.py
# @brief        Test for CABC power event (CS/S3/S4) scenario
#
# @author       Tulika
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Tests.CABC import cabc
from Tests.CABC.cabc_base import CabcBase


##
# @brief        This class contains test cases for CABC with power events
class CabcPowerEvents(CabcBase):
    ##
    # @brief        This function verifies CABC with S3/CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3_CS"])
    # @endcond
    def t_11_s3_cs(self):
        test_status = True
        skip_igcl_for_cabc = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                if (cabc.optimization_params[panel.port].feature_2.level is not None and
                        cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                            panel.port].feature_2.level):
                    skip_igcl_for_cabc = True

                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                           cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                           cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)

                if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
                    power_event = display_power.PowerEvent.CS.name
                else:
                    power_event = display_power.PowerEvent.S3.name

                invoke_power_event(self, power_event)

                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                           cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                           cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)
        if test_status is False:
            self.fail(f"FAIL: CABC persistence failed post power event CS")
        logging.info(f"PASS:  CABC persistence passed post power event CS")

    ##
    # @brief        This function verifies CABC with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_12_s4(self):
        test_status = True
        skip_igcl_for_cabc = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_cabc = True

                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                           cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                           cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)

                invoke_power_event(self, "S4")

                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                           cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
                test_status &= cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                           cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)
        if test_status is False:
            self.fail("FAIL:  CABC persistence failed post power event S4")
        logging.info("PASS:  CABC persistence passed post power event S4")


##
# @brief        This is a helper function to verify CABC with the provided power event
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
    test_result = runner.run(common.get_test_suite(CabcPowerEvents))
    test_environment.TestEnvironment.cleanup(test_result)
