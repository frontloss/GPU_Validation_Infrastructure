##
# @file  dd_ddi_basic.py
# @brief To verify the driver is able to give display diagnostics information to OS after driver installation
# @author Prateek Joshi

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.TDR.Display_Diagnostic.dd_base import *


##
# @brief It contains the methods to verify whether the driver is able to collect diagnostic information after
#        driver installation
class DisplayDiagnosticBasic(DisplayDiagnosticBase):

    ##
    # @brief runTest - Apply display configuration based on command lines and run display diagnostic tool
    #                  Verify Diagnostic details
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
        logging.debug("Running Display Diagnostics Tool after Driver Installation")
        self.run_DDI_test_tool()

        logging.info("---------- Display Diagnostics verification ----------")
        if not self.verify_Display_Diagnostics():
            self.fail("FAIL: Display Diagnostics verification failed after Driver Installation")
        logging.info("PASS: Display Diagnostics verification passed after Driver Installation")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
