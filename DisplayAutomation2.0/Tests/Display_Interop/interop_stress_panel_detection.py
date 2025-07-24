########################################################################################################################
# @file         interop_stress_panel_detection.py
# @brief        Manual sanity test to verify Interop with different events like Cold boot, restart, Power events(CS/S4)
#               Native resolution check and hot plug/unplug.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3284924/ TI.
#               Manual test name: Interop_Stress_Testing
# Sample GOP CommandLine: python .\Tests\Display_Interop\interop_stress_panel_detection.py
# Sample VBIOS CommandLines: python .\Tests\Display_Interop\interop_stress_panel_detection.py -BIOS VBIOS
# @author       Chandrakanth Pabolu
########################################################################################################################
import time
import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import cmd_parser, display_power
from interop_testing_base import *
from Libs.Core.hw_emu import bellwin_power_splitter
import score_card

MAX_REBOOT_COUNT = 6
MAX_POWER_EVENT_COUNT = 6
MAX_HOT_PLUG_COUNT = 10


##
# @brief        This class contains test method of unittest framework.
class InteropStressPanelDetection(InteropTestingBase):
    panel_name = None
    is_vbios = False

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @details      It parses the command line checks for VBIOS passed.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=["-BIOS"])

        # Handle multi-adapter scenario
        if not isinstance(cmd_line_param, list):
            cmd_line_param = [cmd_line_param]

        # Get game playback duration
        if 'VBIOS' in cmd_line_param[0]['BIOS']:
            cls.is_vbios = True

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        super().setUp()

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
    # @brief        This step performs reboot
    # @return       None
    def test_01_step(self):
        logging.info("Scenario: Detection of display post rebooting system: 5 iterations.")
        alert.info("Scenario: Detection of display post rebooting system: 5 iterations.")
        time.sleep(2)
        alert.info("Note: Step to be done by user manually.\n System will be restarted.\n"
                   "Rerun same commandline to continue the test post boot.")

        logging.info(f"Rebooting the system. Iteration: 1.")
        data = {'reboot_counter': 1}

        if reboot_helper.reboot(self, 'test_01_reboot_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step resumes from Reboot and verifies corruption.
    # @return       None
    def test_01_reboot_step(self):
        logging.info("Successfully booted to Desktop")
        data = reboot_helper._get_reboot_data()
        reboot_counter = data['reboot_counter'] + 1
        data = {'reboot_counter': reboot_counter}

        if reboot_counter != MAX_REBOOT_COUNT:
            time.sleep(2)
            alert.info(f"Note: Step to be done by user manually.\n"
                       f"System will be restarted. Iteration: {reboot_counter}\n"
                       "Rerun same commandline to continue the test post boot.\n"
                       "Ensure no corruption seen during cold boot in BIOS and OS environment.")
            if reboot_helper.reboot(self, 'test_01_reboot_step', data=data) is False:
                self.fail("Failed to reboot the system")

        if not verify_observation_assign_score(score_card.Features.Restart):
            self.fail("Step1: Reboot verification failed.")

    ##
    # @brief        This step performs shutdown and cold boot.
    # @return       None
    def test_02_step(self):
        logging.info("Scenario: Cold Boot. Ensures, no corruption seen during cold boot in BIOS and OS environment.")

        alert.info("Scenario: Cold Boot.\n"
                   "Note: Below step to be done by user manually.\n"
                   "Once system is turned off completely, turn on the system.\n"
                   "Post boot, rerun same commandline to continue the test.\n"
                   "Ensure no corruption seen during cold boot in BIOS and OS environment.")

        logging.info("Shutting down the system.")
        if reboot_helper.shutdown(self, 'test_03_step') is False:
            self.fail("Failed to shutdown the system")

    ##
    # @brief        This step resumes from shutdown and verifies corruption.
    # @return       None
    def test_03_step(self):
        logging.info("System booted to Desktop.")
        if not verify_observation_assign_score(score_card.Features.ColdBoot):
            self.fail("Step2: Shutdown verification failed.")


    ##
    # @brief        This step performs power events(S3/CS, S4)
    # @return       None
    def test_04_step(self):
        issue_seen = False
        display_pwr = display_power.DisplayPower()
        power_events = [display_power.PowerEvent.S4]

        logging.info("Scenario: Detection of display post Power events(S3/CS/S4) and MonitorTurnoff.")

        alert.info("Scenario: Detection of display post Power events.\n"
                   "Note:Instruction for User.\n System will be performing S3/CS, S4 and Monitor Turnoff for 5 times.\n"
                   "Please watch out display for any issues.")
        if InteropStressPanelDetection.is_vbios is False:
            power_event_type = display_power.PowerEvent.CS
            is_cs_supported = display_pwr.is_power_state_supported(display_power.PowerEvent.CS)
            if not is_cs_supported:
                power_event_type = display_power.PowerEvent.S3
            power_events.append(power_event_type)
        try:
            for power_event in power_events:
                logging.info(f"Performing {power_event.name} for 6 times")
                for i in range(MAX_POWER_EVENT_COUNT):
                    if display_pwr.invoke_power_event(power_event, 30) is False:
                        self.fail(f'Failed to invoke power event {power_event.name}')
                    logging.info(f"Successfully performed power event {power_event.name}")
                    alert.info(f"Resumed from power event {power_event.name}")
                    time.sleep(2)
        except Exception as e:
            logging.error(f"Exception seen - {e}")
            issue_seen = True

        logging.info(f"Performing MonitorTurnoff for 5 times")
        for i in range(MAX_POWER_EVENT_COUNT):
            alert.info("Note: Step to be performed by user manually.\n"
                       "Scenario: Turn off monitor from Panel OSD page and Turn on after 20sec.")
            logging.info("User Turns off monitor from monitor Off button on panel and Turns it on after 20 sec.")
            time.sleep(25)
            logging.info("Waiting for user to turnon monitor")
            alert.info("Click Ok to resume the test.")

        if not verify_observation_assign_score(score_card.Features.PowerEvents) or issue_seen is True:
            self.fail("Step4: Power Events verification failed.")

    ##
    # @brief        This step performs Native resolution apply and verification
    # @return       None
    def test_05_step(self):
        logging.info("Scenario: Test would apply Native resolution and check no issues.")

        alert.info("Scenario: Test would apply Native resolution and check no issues.\n"
                   "Note: Instruction for User.\n Check if there is any corruption during modeset.")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        display_and_adapterinfo = enumerated_display.ConnectedDisplays[0].DisplayAndAdapterInfo

        if enumerated_display.Count > 1:
            self.fail("More than 1 display connected.")
        if not self.apply_native_mode(display_and_adapterinfo):
            self.fail(f"Applying Native mode failed.")
        time.sleep(5)
        if not verify_observation_assign_score(score_card.Features.NativeResolutionCheck):
            self.fail("Step5: Native resolution verification failed.")

    ##
    # @brief        This step performs Unplug/Plug
    # @return       None
    def test_06_step(self):
        if InteropStressPanelDetection.is_vbios is True:
            self.skipTest("Skipping as run with VBIOS.")

        logging.info("Scenario: Test step would perform unplug and plug and check no issues.")
        alert.info("Scenario: Test step would perform unplug and plug and check no issues.\n"
                   "Note: Check if there is any corruption during unplug/plug.")

        if bellwin_power_splitter.is_connected() is True:
            for i in range(MAX_HOT_PLUG_COUNT):
                logging.info(f"Iteration: {i+1}. Unplugging and plugging display.")
                bellwin_power_splitter.unplug_display(1)
                bellwin_power_splitter.plug_display(1)
                alert.info("Click Ok to proceed.")
        else:
            for i in range(MAX_HOT_PLUG_COUNT):
                logging.info(f"Iteration: {i+1}. Unplugging and plugging display.")
                alert.info("Note: This step to be done by user manually.\n"
                           "After clicking OK, Unplug display from system and plug it back.")
                time.sleep(5)
            alert.info("Click OK to proceed.")

        if not verify_observation_assign_score(score_card.Features.Unplug_Plug):
            self.fail("Step6: Unplug/Plug verification failed.")

##
    # @brief        This step performs post processing
    # @return       None
    def test_post_process(self):
        logging.info("Scenario: This step performs post processing.")
        self.post_process()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('InteropStressPanelDetection'))
    TestEnvironment.cleanup(outcome)
