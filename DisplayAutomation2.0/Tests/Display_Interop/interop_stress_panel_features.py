########################################################################################################################
# @file         interop_stress_panel_features.py
# @brief        Semi-Auto sanity test to verify Interop with different features like HDR, VRR Game workload, Audio,
#               HDCP, Quantization Range and applying all Resolutions.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3284924/ TI.
#               Manual test name: Interop_Stress_Testing
# Sample CommandLine: python .\Tests\Display_Interop\interop_stress_panel_features.py
# @author       Chandrakanth Pabolu
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from interop_testing_base import *
import score_card


##
# @brief        This class contains test method of unittest framework.
class InteropStressPanelFeatures(InteropTestingBase):
    panel_name = None

    ##
    # @brief        This step performs pre test setup.
    # @return       None
    def test_00_step(self):
        logging.info(
            "This step ensures booted with correct panel and initializes score card.")

        user_msg = "[Expectation]:Ensure the system is booted with all planned panels.\n" \
                   "[CONFIRM]:Enter Yes if expectation met, else No."
        result = alert.confirm(user_msg)
        if not result:
            logging.error("Aborting. Test is not started with planned panel. Rerun the test with planned panel.")
            self.abort("Aborting. Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panel.")

        self.pretest_setup()

    ##
    # @brief        This step enables HDR on panel and checks corruption.
    # @return       None
    def test_01_step(self):
        alert.info("Scenario: Enabling HDR on supported displays. No Corruption, Screen Blankout should be visible.")
        logging.info("Scenario: Enabling HDR on all supported displays.")

        user_msg = f"Does panel supports HDR?\n Enter yes if supports HDR, else enter no."
        hdr_support = alert.confirm(user_msg)
        hdr_support_string = "HDR" if hdr_support is True else "Non HDR"
        logging.info(f"Current panel is {hdr_support_string} panel.")
        user_msg = f"Expectation: For HDR panel, HDR option should be seen in OS page else should not be seen.\n" \
                   "Enter yes if criteria met, else enter no."
        result = alert.confirm(user_msg)

        if not result:
            hdr_support_string = "HDR option not seen" if hdr_support is True else "HDR option seen"
            logging.error(f"Mismatch in HDR capability for panel. {hdr_support_string}")
            if not verify_observation_assign_score(score_card.Features.HDREnable_Default):
                self.fail("Step1: HDR verification failed.")
        else:
            self.hdr_verification()
            if not verify_observation_assign_score(score_card.Features.HDREnable_Default):
                self.fail("Step1: HDR verification failed.")

    ##
    # @brief        This step enables VRR on panel and checks corruption.
    # @return       None
    def test_02_step(self):
        alert.info("Scenario: Verifying VRR with Game workloads.")
        logging.info("Scenario: Verifying VRR with Game workloads.")

        self.game_play()

        if not verify_observation_assign_score(score_card.Features.VRR):
            self.fail("Step2: VRR verification failed.")

    ##
    # @brief        This step performs Audio playback
    # @return       None
    def test_03_step(self):
        logging.info("Scenario: This step verifies Audio playback.")
        alert.info("Scenario: This step verifies Audio playback.")
        time.sleep(2)

        self.audio_verification()

        if not verify_observation_assign_score(score_card.Features.AudioPlayback):
            self.fail("Step3: Audio verification failed.")

    ##
    # @brief        This step verifies HDCP
    # @return       None
    def test_04_step(self):
        logging.info("Scenario: This step Verifies HDCP with netflix.")
        alert.info("Scenario: This step Verifies HDCP with netflix.")
        self.verify_hdcp()
        if not verify_observation_assign_score(score_card.Features.HDCP):
            self.fail("Step4: HDCP verification failed.")

    ##
    # @brief        This step verifies Quantization Range.
    # @return       None
    def test_05_step(self):
        logging.info("Scenario: This step Verifies Quantization Range.")
        alert.info("Scenario: This step Verifies Quantization Range.")
        feature_support = self.verify_quantization_range()
        if feature_support is True:
            if not verify_observation_assign_score(score_card.Features.QuantizationRange):
                self.fail("Step5: Quantization verification failed.")

    ##
    # @brief        This step performs Resolutions apply
    # @return       None
    def test_06_step(self):
        logging.info("Scenario: This step Applies all MDS modes.")
        alert.info("Scenario: This step Applies all MDS modes.")
        time.sleep(2)

        self.mode_change()
        alert.info("Press OK to proceed.")

        if not verify_observation_assign_score(score_card.Features.AllResolutions):
            self.fail("Step6: All Resolutions verification failed.")

##
    # @brief        This step performs post processing
    # @return       None
    def test_post_process(self):
        logging.info("Scenario: This step performs post processing.")
        self.post_process()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('InteropStressPanelFeatures'))
    TestEnvironment.cleanup(outcome)
