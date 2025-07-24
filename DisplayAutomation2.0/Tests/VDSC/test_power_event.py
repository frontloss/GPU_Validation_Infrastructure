########################################################################################################################
# @file         test_power_event.py
# @brief        Test to check VDSC programming of VDSC displays when system goes into low power mode and comes back.
# @details      Test Scenario:
#               1. Plug the VDSC display and apply the appropriate display config.
#               2. Invoke power event (CS, S3, S4) based on the command line.
#               3. Resume from power event and verify VDSC programming for the active VDSC displays before the PE.
#               This test can be planned with MIPI, EDP and DP VDSC displays
#
# @author       Bhargav Adigarla, Praburaj Krishnan
########################################################################################################################
import logging
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_power import PowerEvent
from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a multiple test function which can invoked separately by providing the value to the
#               selective command line argument like CS, S3, S4
class VdscPowerEvent(VdscBase):

    ##
    # @brief        This test method is invoked if CS is provided as value for the Selective argument. Acts as wrapper
    #               method which checks if CS is supported and then invokes a function which does power event and
    #               verifies VDSC programming.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "CS"])
    # @endcond
    def t_11_power_event_cs_s3(self) -> None:
        if VdscBase._display_power.is_power_state_supported(PowerEvent.CS):
            self.verify_vdsc_with_power_event(PowerEvent.CS)
        else:
            self.fail("CS is not supported in this platform, aborting the test")

    ##
    # @brief        This test method is invoked if S3 is provided as value for the Selective argument. Acts as wrapper
    #               method which checks if CS is not supported and then invokes a function which does power event and
    #               verifies VDSC programming.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "S3"])
    # @endcond
    def t_12_power_event_s3(self) -> None:
        if VdscBase._display_power.is_power_state_supported(PowerEvent.CS) is False:
            self.verify_vdsc_with_power_event(PowerEvent.S3)
        else:
            self.fail("S3 can not be tested since CS is supported, aborting the test")

    ##
    # @brief        This test method is invoked if S4 is provided as value for the Selective argument. Acts as wrapper
    #               method to invokes a function which does power event and verifies VDSC programming.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "S4"])
    # @endcond
    def t_13_power_event_s4(self) -> None:
        self.verify_vdsc_with_power_event(PowerEvent.S4)

    ##
    # @brief        Helper method which applies the display config based on the no. of displays connected, then
    #               invokes power event based on the power_event param and verifies VDSC programming after coming
    #               back from the power event.
    # @param[in]    power_event: PowerEvent
    #                   Enum variable which tells to which low power mode the system has to enter.
    # @return       None
    def verify_vdsc_with_power_event(self, power_event: PowerEvent) -> None:
        is_success, config = VdscBase.get_config_to_apply()
        self.assertTrue(is_success, "[Planning Issue] - Invalid Command Line")

        topology_name = DisplayConfigTopology(config.topology).name

        logging.info("Applying Display Config {} for {}".format(topology_name, config.port_list))
        if VdscBase._display_config.set_display_configuration_ex(config.topology, config.port_list) is False:
            self.fail("[Driver Issue] - Applying Display Config Failed")
            # Gdhm bug reporting handled in set_display_configuration_ex

        if VdscBase._display_power.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail("Power event {0} Expected = PASS Actual = FAIL".format(power_event.name))
            # Gdhm bug reporting handled in invoke_power_event

        for adapter_display_dict in VdscBase.vdsc_panels:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed
            [(gfx_index, panel)] = adapter_display_dict.items()

            is_success = dsc_verifier.verify_dsc_programming(gfx_index, panel)
            self.assertTrue(is_success, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(panel,
                                                                                                             gfx_index))

            logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(panel, gfx_index))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VdscPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
