#######################################################################################################################
# @file                 hdr_did_2_0_negative.py
# @addtogroup           Test_Color
# @section              hdr_did_2_0_negative
# @remarks              @ref hdr_did_2_0_negative.py \n
#                       The test script is a negative verification for the DID 2.0 EDIDs
#                       SINK_EDP217 - Qualified DID + HDR Support only in CTA Block in DID
#                       SINK_EDP225 - DID with No HDR Support
#                       SINK_EDP226 - Invalid DID with HDR Support
#                       SINK_EDP222 - Invalid DID; HDR support present in CTA Block within DID
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


class HDRDid20Negative(HDRTestBase):

    def setUp(self):
        TestBase().setUp()
        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)
        if num_of_hdr_supported_panels == 0:
            logging.info("The EDIDs are either invalid or do not have HDR support as per OS Policy")
        else:
            logging.error("The invalid EDIDs are reporting support for HDR")
            self.fail()

        status = common_utility.apply_power_mode((display_power.PowerSource.AC).value)
        if status is False:
            self.fail()

    def runTest(self):
        if self.toggle_hdr_on_all_supported_panels(enable=True):
            logging.error("HDR modeset is successful on Invalid EDIDs")
            self.fail()
        else:
            logging.info("PASS : HDR Modeset is unsuccessful as expected")


    ##
    # Since the runTest would have already disabled HDR across all the panels in Step2
    # Need to only clean up by applying a Unity Gamma and Unplug of the displays
    def tearDown(self):
        ##
        # Apply Unity Gamma as part of clean-up
        gamma_utility.apply_gamma()
        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        TestBase().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables HDR on supported panels and perform verification on all panels"
        " when HDR is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

