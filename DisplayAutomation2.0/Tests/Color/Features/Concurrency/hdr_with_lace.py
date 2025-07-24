#################################################################################################################
# @file         hdr_with_lace.py
# @brief        The test script aims at verifying concurrency of LACE and HDR. Below steps are performed by the
#               test script to verify that both the features are mutually exclusive
#               This scripts comprises of basic test function and the function will perform below functionalities
#               1. Enable OS Aware HDR - Verifying that HDR has got enabled successfully.
#               2. Invoking an  Escape Call to enable LACE, and verifying that LACE has not got enabled since
#                  LACE and HDR are mutually exclusive
#               3. Disabling HDR and verifying that HDR has got disabled.
#               4. Following Step2 again, LACE should get enabled successfully.
#               5. Enable HDR. Verifying that LACE has got disabled.
# @author       Siva Thangaraja
#################################################################################################################
import time
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.LACE.lace_base import *


class hdrWithLACE(HDRTestBase, LACEBase):
    lace_version = None

    ##
    # @brief        Performs super().setUp() and setting lace version is done.
    # @return       None
    def setUp(self):
        self.custom_tags["-VERSION"] = None
        super().setUp()
        self.lace_version = str(self.context_args.test.cmd_params.test_custom_tags["-VERSION"][0])
        logging.info("Lace version:{0} set sucessfully".format(self.lace_version))

    ##
    # @brief        test executes the actual test steps.
    # @return       None
    def runTest(self):

        for gfx_index, adapter in self.context_args.adapters.items():

            for port, panel in adapter.panels.items():

                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
                            self.fail("HDR connot be enabled")

                        if color_escapes.configure_als_aggressiveness_level(port, panel.display_and_adapterInfo, lux=7500,
                                                                            aggressiveness_level=1,
                                                                            aggressiveness_operation=True,
                                                                            lux_operation=True) is False:
                            self.fail("Lace Escape call failed")

                        logging.info("Status : escape call for lace is successful")

                        time.sleep(2)
                        if feature_basic_verify.verify_lace_feature(gfx_index, platform, panel.pipe, False,
                                                                    self.lace_version) is False:
                            self.fail("Lace and hdr both enabled")
                        logging.info("Lace not Enabled")

                        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                            self.fail("HDR not disabled")
                        logging.info("HDR disabled")

                        if color_escapes.configure_als_aggressiveness_level(port, panel.display_and_adapterInfo, lux=7500,
                                                                            aggressiveness_level=1,
                                                                            aggressiveness_operation=True,
                                                                            lux_operation=True) is False:
                            self.fail("Lace Escape call failed")

                        logging.info("Status : escape call for lace is successful")

                        time.sleep(2)
                        if feature_basic_verify.verify_lace_feature(gfx_index, platform, panel.pipe, True,
                                                                    self.lace_version) is False:
                            self.fail("Lace not Enabled")
                        logging.info("Status : Lace Enabled")

                        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
                            self.fail("HDR connot be enabled")

                        time.sleep(2)

                        if feature_basic_verify.verify_lace_feature(gfx_index, platform, panel.pipe, False,
                                                                    self.lace_version) is False:
                            self.fail("Lace and HDR both enabled")
                        logging.info("Status : Lace not enabled as HDR is currently enabled")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                                    panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

    ##
    # If the test enables HDR and fails in between, then HDR has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: To apply SINGLE or CLONE display configuration and apply and verify Lace and HDR")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)