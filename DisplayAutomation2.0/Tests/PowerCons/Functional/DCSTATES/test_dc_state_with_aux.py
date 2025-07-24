########################################################################################################################
# @file         test_dc_state_with_aux.py
# @brief        Tests to check Aux transaction while system is in DC state.
#
# @author       Vinod D S
########################################################################################################################

import threading

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains basic tests DC6 with Aux transaction
class TestDcStateWithAux(DCStatesBase):

    ##
    # @brief        This function is for DC6 with Aux transaction
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6"])
    # @endcond
    def t_11_dc6_with_aux(self):
        for adapter in dut.adapters.values():

            if self.display_config_.set_display_configuration_ex(enum.SINGLE, [self.lfp_panels[0].port]) is False:
                self.fail(f"Failed to apply DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
            logging.info(f"Applied DisplayConfig SINGLE {[self.lfp_panels[0].port]}")

            thread = threading.Thread(target=self._hot_plug_function, args=(adapter,))
            thread.start()

            logging.info("Verifying DC5/6 with Idle desktop")
            etl_file = dc_state.get_etl_trace(method='IDLE', duration=60)
            thread.join()

            if dc_state.verify_dc_state(adapter, 'DC6', etl_file) is False:
                self.fail("SW DC5 verification failed")
            logging.info("SW DC5/6 verification is successful")

    ##
    # @brief        This function is for DC6V with Aux transaction
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_12_dc6v_with_aux(self):
        for adapter in dut.adapters.values():
            if self.display_config_.set_display_configuration_ex(enum.SINGLE, [self.lfp_panels[0].port]) is False:
                self.fail(f"Failed to apply DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
            logging.info(f"Applied DisplayConfig SINGLE {[self.lfp_panels[0].port]}")

            thread = threading.Thread(target=self._hot_plug_function, args=(adapter,))
            thread.start()

            logging.info("Verifying DC6v with Video playback")
            etl_file = dc_state.get_etl_trace(method='VIDEO', duration=24)
            thread.join()

            if dc_state.verify_dc_state(adapter, 'DC6V', etl_file) is False:
                self.fail("DC6V verification with video playback failed")
            logging.info("DC6V verification with video playback is successful")

    ##
    # @brief        Helper function to hotplug external panel
    # @return       None
    # @cond
    def _hot_plug_function(self, adapter):
        # @endcond
        time.sleep(20)  # Allowing system to enter DC state
        if self.ext_panels is not None:
            if dut.plug_wrapper(adapter, self.ext_panels[0]) is False:
                self.fail("Failed to plug external display")
        logging.info("Hotplug external panel successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDcStateWithAux))
    test_environment.TestEnvironment.cleanup(test_result)
