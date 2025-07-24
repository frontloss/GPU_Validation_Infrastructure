#######################################################################################################################
# @file         display_mode_enum_combined_wireformat.py
# @brief        This file currently contains validation of combined color formats and different mode enumerations for
#               given HDMI display. Necessary changes for DP can be done once driver supports it
# @details      The main aim of this test is to verify if combined wireformat is reported for a given mode instead of
#               reporting them seperately. And the apply each of the supported color formats to the given modes and
#               verify DE for each of them.
# @author       Supriya Krishnamurthi
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.ModeEnumAndSet.display_mode_enumeration_base import *


##
# @brief        A class which has test method to apply modeset with combined color formats.
class CombinedWireformatModeEnumAndSet(ModeEnumAndSetBase):

    ##
    # @brief        Unit-test runTest function.
    # @return       None
    def runTest(self):
        ##
        # Get default bpc and encoding after reset
        display_adapter_info = self.display_config.get_display_and_adapter_info_ex(self.display, 'gfx_0')
        status, _, default_bpc, default_encoding = color_escapes.get_bpc_encoding(display_adapter_info,
                                                                                  self.platform_type)
        self.assertTrue(status, "Failed to get the BPC and Encoding via color escape")
        logging.info(f"Before the test default bpc: {default_bpc} default encoding: {default_encoding}")

        ##
        # Get all supported OS modes
        self.get_os_supported_modes()

        ##
        # Verify Modes enumerated across golden_mode_list, ignore_mode_list with os_mode_list
        status = self.verify_golden_and_ignore_modes_with_combined_wireformat()
        if status is False:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Verification of enumerated modes across golden & ignore mode list failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Verification of enumerated modes across golden & ignore mode list failed")

        ##
        # Apply and verify mode set.
        self.verify_mode_enum_modeset_with_combined_wireformat()

        # setting BPC and color encoding to default value supported by IGCC
        status = color_escapes.set_bpc_encoding(display_adapter_info, 'BPCDEFAULT', 'DEFAULT', self.Platform, False, feature="ModeEnum")
        self.assertTrue(status, "Failed to reset BPC and Encoding to default")

        ##
        # Get default bpc and encoding after reset
        status, _, default_bpc, default_encoding = color_escapes.get_bpc_encoding(display_adapter_info,
                                                                                  self.platform_type)
        self.assertTrue(status, "Failed to get the BPC and Encoding via color escape")
        logging.info(f"Reset values after the test : default bpc: {default_bpc} default encoding: {default_encoding}")

        # Delay to reflect the BPC and Encoding reset
        time.sleep(1)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)