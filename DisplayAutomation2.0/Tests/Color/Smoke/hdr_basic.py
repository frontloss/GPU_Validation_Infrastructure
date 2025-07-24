########################################################################################################################
# @file         hdr_basic.py
# @brief        Basic test to verify HDR feature
#               * Enable HDR on all panels
#               * Verify HDR is enabled
#               * Disable HDR on all panels
#               * Verify HDR is disabled
# @author       Pai, Vinayak1
########################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


##
# @brief    Contains basic test to verify HDR
class HDRBasic(HDRTestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        ##
        # Enable HDR on all the supported panels and perform verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail("FAIL: HDR verification after HDR enable failed")

        logging.info("*** Step 2 : Disable HDR/WCG on all supported panels and verify ***")
        ##
        # Disable HDR on all the supported panels and perform verification
        # Here the intent is that, the panels are all in SDR Mode
        if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail("FAIL: HDR verification after HDR disable failed")

    ##
    # Since the runTest would have already disabled HDR across all the panels in Step2
    # Need to only clean up by applying a Unity Gamma and Unplug of the displays
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe)
                if is_hdr_enabled:
                    if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail("FAIL: HDR verification after HDR disable failed")
                    else:
                        ##
                        # Apply Unity Gamma as part of clean-up
                        gamma_utility.apply_gamma()
                        ##
                        # Invoking the Base class's tearDown() to perform the general clean-up activities
                        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify HDR feature")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
