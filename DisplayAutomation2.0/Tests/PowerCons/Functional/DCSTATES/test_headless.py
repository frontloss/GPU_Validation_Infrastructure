########################################################################################################################
# @file         test_headless.py
# @brief        Tests to verify DC9 state with headless scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains basic tests for DC9 states
class TestHeadless(DCStatesBase):

    ##
    # @brief        This function verifies DC9 with headless display
    # @return       None
    # @cond
    # @endcond
    def t_10_state_dc9_basic(self):
        for adapter in dut.adapters.values():
            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed with external display")
            logging.info("\tDC9 verification is successful with external display")

            ##
            # Unplug all the external displays connected apart from eDP/MIPI
            display_port_ = DisplayPort()
            enumerated_displays = self.display_config_.get_enumerated_display_info()
            logging.debug(f"Enumerated displays: {enumerated_displays.to_string()}")
            for idx in range(enumerated_displays.Count):
                disp_config = enumerated_displays.ConnectedDisplays[idx]
                display_port = CONNECTOR_PORT_TYPE(disp_config.ConnectorNPortType)
                display_port = str(display_port)
                if display_port[:2] == "DP":
                    result = display_port_.set_hpd(display_port, False)
                    if result is False:
                        self.fail(f"Failed to unplug simulated {display_port} display")
                    logging.info(f"Unplug of simulated {display_port} display successful")

            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed with headless display")
            logging.info("\tDC9 verification is successful with headless display")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestHeadless))
    test_environment.TestEnvironment.cleanup(test_result)
