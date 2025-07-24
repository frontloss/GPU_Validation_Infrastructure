#################################################################################################
# @file         apply_csc_reboot.py
# @brief        This scripts comprises of Test_before_reboot() and test_after_reboot ()
#               and will perform below functionalities
#               1.To configure applycsc info for the display
#               2.To perform register verification OCSC,Coeff, and gamma register
#               3.Will perform reboot event
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ApplyCSC.apply_csc_base import *


##
# @brief - To perform persistence verification for apply csc reboot scenario
class ApplyCscTestReboot(ApplyCSCTestBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo, port,True) is False:
                        self.fail()

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
                if panel.is_active:
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo, port,False) is False:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ApplyCscTestReboot'))
    TestEnvironment.cleanup(outcome)