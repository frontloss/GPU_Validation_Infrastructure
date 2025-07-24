#################################################################################################
# @file         lace_reboot.py
# @brief        Test calls for get and set lace functionality with reboot scenario as persistence
# @author       Vimalesh D
#################################################################################################
import time
import unittest

from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.Lace.lace_base import *


##
# @brief - To perform persistence verification for BPC and Encoding
class Lacereboot(LACEBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for primary LFP")
                        else:
                            self.fail("Lace enable/disable with verification failed")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

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
                if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                    if trigger_type == 0:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                  panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Post reboot Lace was enabled and verified successfully")
                        else:
                            self.fail("Post reboot Lace enable/disable with verification failed")
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, str(1), panel.transcoder,
                              self.panel_props_dict[gfx_index, port].Bpc,
                              self.panel_props_dict[gfx_index, port].Encoding):
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get/set lace IGCL API Verification with reboot scenario')
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Lacereboot'))
    TestEnvironment.cleanup(outcome)
