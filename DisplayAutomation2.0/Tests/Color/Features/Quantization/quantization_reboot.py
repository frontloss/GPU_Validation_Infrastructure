#################################################################################################
# @file         quantization_reboot.py
# @brief        This scripts comprises of Test_before_reboot() and test_after_reboot ()
#               and will perform below functionalities
#               1.To configure avi info for the display
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantization range
#               3.Will perform reboot event
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.Quantization.quantization_test_base import *


##
# @brief - To perform persistence verification for Quantisation reboot scenario
class QuantisationTestReboot(QuantizationTestBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform,
                                           panel.pipe, plane_id, panel.transcoder, panel.connector_port_type,
                                           configure_avi=True)

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):

        logging.info("Successfully applied power event S5 state")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform,
                                           panel.pipe, plane_id, panel.transcoder, panel.connector_port_type,
                                           configure_avi=False)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the quantization range and perform verification on all panels")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('QuantisationTestReboot'))
    TestEnvironment.cleanup(outcome)
