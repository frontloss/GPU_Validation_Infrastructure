########################################################################################################################
# @file             test_ac_dc.py
# @brief            Test to check VDSC programming of EDP/MIPI VDSC display in AC and DC Mode.
# @details          Test Scenario:
#                   1. Enables Simulated battery to switch between AC and DC
#                   2. Enters AC/DC mode based on the command line and verifies VDSC programming for the VDSC display.
#                   This test can be planned with MIPI and EDP VDSC displays
#
# @author           Bhargav Adigarla, Praburaj Krishnan
########################################################################################################################
import logging
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_power import PowerSource
from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains two test case one to test VDSC in AC mode and other to test in DC mode.
class VdscBasic(VdscBase):

    ##
    # @brief        This test enables the simulated battery which helps to switch between AC and DC mode.
    # @return       None
    def t_11_enable_simbat(self) -> None:
        # Enable Simulated Battery for AC/DC switch
        logging.info("Enabling Simulated Battery")
        if VdscBase._display_power.enable_disable_simulated_battery(True) is False:
            self.fail("Failed to enable Simulated Battery")
        logging.info("\tPASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")

    ##
    # @brief        This test acts as a wrapper to verify VDSC in AC mode.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "AC_DC"])
    # @endcond
    def t_12_ac(self) -> None:
        self.verify_vdsc_with_power_source(PowerSource.AC)

    ##
    # @brief        This test acts as a wrapper to verify VDSC in DC mode.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "AC_DC"])
    # @endcond
    def t_13_dc(self) -> None:
        self.verify_vdsc_with_power_source(PowerSource.DC)

    ##
    # @brief        Helper function to check VDSC with power source
    # @param[in]    power_source: PowerSource
    #                   Enum variable to set power line status to AC or DC mode.
    # @return       None
    def verify_vdsc_with_power_source(self, power_source: PowerSource) -> None:
        is_success, config = VdscBase.get_config_to_apply()
        topology_name = DisplayConfigTopology(config.topology).name

        logging.info("Applying Display Config {} for {}".format(topology_name, config.port_list))
        is_success = VdscBase._display_config.set_display_configuration_ex(config.topology, config.port_list)
        self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")

        common.print_current_topology()

        # Set current power line status
        is_success = VdscBase._display_power.set_current_powerline_status(power_source)
        self.assertTrue(is_success, "[Test Issue] - Failed to switch power line status to {0}".format(power_source.name))

        # Check VDSC
        for adapter_display_dict in VdscBase.vdsc_panels:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating over dictionary is not needed
            [(gfx_index, panel)] = adapter_display_dict.items()

            is_success = dsc_verifier.verify_dsc_programming(gfx_index, panel)
            self.assertTrue(is_success, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(panel,
                                                                                                             gfx_index))

            logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(panel, gfx_index))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VdscBasic))
    test_environment.TestEnvironment.cleanup(test_result)
