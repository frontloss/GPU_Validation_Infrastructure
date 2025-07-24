########################################################################################################################
# @file         interop_stress_auxiliary_features.py
# @brief        Semi-Auto sanity test to verify Interop of auxiliary features like Color format/depth override in HDR
#               and SDR mode, Overriding Link Rates for DP and Overriding FRL rates and TMDS for HDMI panel.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-4193818/ TI.
#               Manual test name: Interop_Stress_Auxiliary_Features
# Sample CommandLine: python \\Tests\\Display_Interop\\interop_stress_auxiliary_features.py
# @author       Chandrakanth Pabolu
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from interop_testing_base import *
import score_card


##
# @brief        This class contains test method of unittest framework.
class InteropStressAuxiliaryFeatures(InteropTestingBase):
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
    # @brief        This step enables HDR Color Override on panel and checks corruption.
    # @return       None
    def test_01_step(self):
        alert.info(f"Scenario: {score_card.Features.HDR_Color_Override.name}.")
        logging.info(f"Scenario: {score_card.Features.HDR_Color_Override.name}.")

        user_msg = f"Does panel supports HDR?\n Enter yes if supports HDR, else enter no."
        hdr_support = alert.confirm(user_msg)
        hdr_support_string = "HDR" if hdr_support is True else "Non HDR"
        logging.info(f"Current panel is {hdr_support_string} panel.")

        if hdr_support is True:
            if not verify_observation_assign_score(score_card.Features.HDR_Color_Override):
                self.fail("Step1: HDR Color Override verification failed.")

    ##
    # @brief        This step enables SDR Color Override on panel and checks corruption.
    # @return       None
    def test_02_step(self):
        alert.info(f"Scenario: {score_card.Features.SDR_Color_Override.name}.")
        logging.info(f"Scenario: {score_card.Features.SDR_Color_Override.name}.")

        if not verify_observation_assign_score(score_card.Features.SDR_Color_Override):
            self.fail("Step2: SDR Color Override verification failed.")

    ##
    # @brief        This step performs Link Config DP and checks corruption
    # @return       None
    def test_03_step(self):
        alert.info(f"Scenario: {score_card.Features.LinkConfig_DP.name}.")
        logging.info(f"Scenario: {score_card.Features.LinkConfig_DP.name}.")

        user_msg = f"Is it DP Panel?\n Enter yes if it is DP panel, else enter no."
        panel = alert.confirm(user_msg)
        panel_string = "DP" if panel is True else "Not DP"
        logging.info(f"Current panel is {panel_string}.")

        if panel is True:
            if not verify_observation_assign_score(score_card.Features.LinkConfig_DP):
                self.fail("Step3: LinkConfig DP verification failed.")

    ##
    # @brief        This step performs Link Config FRL and checks corruption
    # @return       None
    def test_04_step(self):
        alert.info(f"Scenario: {score_card.Features.LinkConfig_FRL.name}.")
        logging.info(f"Scenario: {score_card.Features.LinkConfig_FRL.name}.")
        user_msg = f"Is it HDMI2.1 Panel?\n Enter yes if it is HDMI2.1 panel, else enter no."
        panel = alert.confirm(user_msg)
        panel_string = "HDMI2.1" if panel is True else "Not HDMI2.1"
        logging.info(f"Current panel is {panel_string}.")

        if panel is True:
            if not verify_observation_assign_score(score_card.Features.LinkConfig_FRL):
                self.fail("Step4: LinkConfig HDMI FRL verification failed.")

    ##
    # @brief        This step performs Link Config TMDS and checks corruption.
    # @return       None
    def test_05_step(self):
        alert.info(f"Scenario: {score_card.Features.LinkConfig_TMDS.name}.")
        logging.info(f"Scenario: {score_card.Features.LinkConfig_TMDS.name}.")
        user_msg = f"Is it HDMI2.1 Panel?\n Enter yes if it is HDMI2.1 panel, else enter no."
        panel = alert.confirm(user_msg)
        panel_string = "HDMI2.1" if panel is True else "Not HDMI2.1"
        logging.info(f"Current panel is {panel_string}.")

        if panel is True:
            if not verify_observation_assign_score(score_card.Features.LinkConfig_TMDS):
                self.fail("Step5: LinkConfig HDMI TMDS verification failed.")

##
    # @brief        This step performs post processing
    # @return       None
    def test_post_process(self):
        logging.info("Scenario: This step performs post processing.")
        self.post_process()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('InteropStressAuxiliaryFeatures'))
    TestEnvironment.cleanup(outcome)
