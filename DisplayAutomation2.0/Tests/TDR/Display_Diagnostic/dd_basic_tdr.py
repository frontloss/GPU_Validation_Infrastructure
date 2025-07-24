##
# @file dd_basic_tdr.py
# @brief To verify the driver is able to give display diagnostic information to OS after driver installation
#       * and after returning from a TDR.
# @author Nainesh Doriwala


from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.TDR.Display_Diagnostic.dd_base import *


##
# @brief It contains the methods to verify whether the driver is able to collect diagnostic information after TDR
class CollectDiagnosticBasic(DisplayDiagnosticBase):
    ##
    # @brief step 1 rebooting system to handle reg key update to save tdr dumps
    # @return None
    def test_1_step(self):
        logging.debug("Entry: test_1_step()")

        if reboot_helper.reboot(self, 'test_2_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief apply config and verify DD , Apply TDR and verify DD
    # @return None
    def test_2_step(self):
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))

        # Set valid configuration as per command line parameter
        logging.info("Verifying enumerated display and Apply config post TDR generation on GFX_0"),
        self.enumerated_display = self.config.get_enumerated_display_info()
        # enumerated_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.is_teardown_required = True
            self.fail("Required displays are not enumerated")
        self.assertNotEqual(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")
        display_adapter_info_list = []
        for item in self.input_display_list:
            logging.info("0: {}, 1: {}".format(item[0], item[1]))
            display_adapter_info_list.append(self.config.get_display_and_adapter_info_ex(item[0], item[1]))
        self.assertEqual(self.config.set_display_configuration_ex(self.cmd_config, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")

        # Run tool to test Display Diagnostic
        self.run_CDI_test_tool()

        if not self.verify_Collect_Diagnostics():
            logging.critical("Collect Diagnostic Test Failed")
            self.fail("FAIL: Collect Diagnostic test Failed after Driver Installation")
        logging.info("PASS: Collect Diagnostic test Passed after Driver Installation")

        # Generate TDR
        if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
            logging.info("TDR is not generated")
        if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
            logging.info("TDR generated Successfully")

        # Clear TDR
        display_essential.clear_tdr()
        logging.info("TDR cleared successfully post TDR generation")

        # Run tool to test Display Diagnostic
        self.run_CDI_test_tool()

        if not self.verify_Collect_Diagnostics():
            logging.critical("Collect Diagnostic Test Failed")
            self.fail("FAIL: Collect Diagnostic test Failed after TDR")
        logging.info("PASS: Collect Diagnostic test Passed after TDR")

        self.is_teardown_required = True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('CollectDiagnosticBasic'))
    TestEnvironment.cleanup(outcome)
