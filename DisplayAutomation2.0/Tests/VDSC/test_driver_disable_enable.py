########################################################################################################################
# @file         test_driver_disable_enable.py
# @brief        Tests the VDSC programming for VDSC displays before and after disable enable of driver.
# @details      Test Scenario:
#               1. Verify DSC Programming for the Plugged DSC displays.
#               2. Disable the Gfx driver and Enable the Gfx driver.
#               3. Verify DSC programming for the same DSC displays.
#               This test can be planned with MIPI, EDP and DP VDSC displays
#
# @author       Sri Sumanth Geesala, Praburaj Krishnan
########################################################################################################################
import logging
import unittest

from Libs.Core import display_essential
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDriverDisableEnable(VdscBase):

    ##
    # @brief        This test method verifies VDSC programming for VDSC displays before and after disabling and
    #               enabling of the gfx driver.
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_driver_disable_enable(self) -> None:

        is_success, config = VdscBase.get_config_to_apply()
        topology_name = DisplayConfigTopology(config.topology).name

        logging.info("Applying Display Config {} for {}".format(topology_name, config.port_list))
        is_success = VdscBase._display_config.set_display_configuration_ex(config.topology, config.port_list)
        self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")

        common.print_current_topology()

        # Verify VDSC
        for adapter_display_dict in VdscBase.vdsc_panels:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed
            [(gfx_index, panel)] = adapter_display_dict.items()

            is_success = dsc_verifier.verify_dsc_programming(gfx_index, panel)
            self.assertTrue(is_success, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(panel,
                                                                                                             gfx_index))
            logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(panel, gfx_index))

        logging.info('Doing a restart of display driver')
        is_success, reboot_required = display_essential.restart_gfx_driver()
        self.assertTrue(is_success, 'restarting display driver failed')

        # Verify VDSC after Gfx driver disable enable
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
    test_result = runner.run(common.get_test_suite(TestDriverDisableEnable))
    test_environment.TestEnvironment.cleanup(test_result)
