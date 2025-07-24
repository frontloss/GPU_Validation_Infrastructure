##
# @file  dd_ddi_tdr.py
# @brief To verify the driver is able to give display diagnostics information to OS after TDR
# @author Prateek Joshi



from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify

from Tests.TDR.Display_Diagnostic.dd_base import *


##
# @brief It contains the methods to verify whether the driver is able to collect diagnostic information after
#        TDR
class DisplayDiagnosticTDR(DisplayDiagnosticBase):

    ##
    # @brief runTest - Apply display configuration based on command lines and run display diagnostic tool
    #                  Verify Diagnostic details, generate TDR and verify diagnostic details
    # @return None
    def runTest(self):

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
        logging.debug("Running Display Diagnostics Tool before TDR")
        self.run_DDI_test_tool()

        logging.info("---------- Display Diagnostics verification before TDR ----------")
        if not self.verify_Display_Diagnostics():
            self.fail("FAIL: Display Diagnostics verification failed before TDR")
        logging.info("PASS: Display Diagnostics verification passed before TDR")

        # Generate TDR
        logging.debug("Generating TDR")
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))

        if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
            logging.info("TDR is not generated")
        if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
            logging.info("TDR generated Successfully")

        # Clear TDR
        display_essential.clear_tdr()
        logging.info("TDR cleared successfully post TDR generation")

        # Run tool to test Display Diagnostic
        logging.debug("Running Display Diagnostics Tool after TDR")
        self.run_DDI_test_tool()

        logging.info("---------- Display Diagnostics verification post TDR ----------")
        if not self.verify_Display_Diagnostics():
            self.fail("FAIL: Display Diagnostics verification failed after TDR ")
        logging.info("PASS: Display Diagnostics verification passed after TDR")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
