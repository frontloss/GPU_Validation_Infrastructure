#######################################################################################################################
# @file         hdcp_basic_2_2.py
# @brief        This test aims to check basic hdcp 2.2 functionality.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3424801/ HDCP 2.2_Basic
# @author       Chandrakanth Pabolu
#######################################################################################################################
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import winkb_helper as kb, winkb_helper
from Libs.Core import app_controls, display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Tests.HDCP.hdcp_base import *

TEST_VIDEOS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos")

##
# @brief        Contains HDCP tests with ETL based verification
class HdcpBasic22(HDCPBase):
    initial_config = None
    enum_port_list = None
    display_pwr = display_power.DisplayPower()
    display_config = DisplayConfiguration()

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.hdcp_type = HDCPType.HDCP_2_2

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass

    ##
    # @brief This step confirms from user if booted with all displays correctly.
    # @return None
    def test_1_step(self):
        user_msg = "[Expectation]:Ensure the system is booted with all planned panels.\n" \
                   "[CONFIRM]:Enter Yes if expectation met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panel")

        config_to_be_applied = enum.CLONE
        enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count <= 1:
            alert.info("FAIL: Two are more displays to be connected.")
            self.fail("FAIL: Two are more displays to be connected.")

        for i in range(0, enumerated_display.Count):
            enum_port_list.append(str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType)))

        alert.info(f"Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration.")
        logging.info(f"Step1: Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration.")
        status = self.__class__.display_config.set_display_configuration_ex(config_to_be_applied, enum_port_list)
        if not status:
            self.fail(f"Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration failed.")

        user_msg = "[Expectation]:Make sure Display configuration applied successfully. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")
        self.__class__.enum_port_list = enum_port_list
        self.__class__.initial_config = self.__class__.display_config.get_current_display_configuration()

    ##
    # @brief This step involves verifying hdcp2.2 post reboot with media playback
    # @return None
    def test_2_step(self):
        self.verify_hdcp_with_media()

        data = {'initial_config': self.__class__.initial_config}
        alert.info("Performing power event S5. Once system boots back to Desktop, rerun the test with same"
                   "commandline to continue execution")
        logging.info("Step2: Performing Power event S5.")
        if reboot_helper.reboot(self, 'test_3_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step involves verifying hdcp2.2 post reboot with media playback
    # @return None
    def test_3_step(self):
        logging.info("Successfully resumed from power event S5.")
        data = reboot_helper._get_reboot_data()
        self.__class__.initial_config = data['initial_config']
        self.verify_config(self.__class__.initial_config)

        self.verify_hdcp_with_media()

        alert.info("Closing media player")
        window_helper.close_media_player()

    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def verify_hdcp_with_media(self):
        status = False
        logging.info("Launching ElephantsDream_H264_1920x1080.mp4 video in Windowed mode.")
        alert.info("Launching ElephantsDream_H264_1920x1080.mp4 video in Windowed mode.")
        video_path = os.path.join(TEST_VIDEOS_PATH, 'ElephantsDream_H264_1920x1080.mp4')
        app_controls.launch_video(video_path, False)
        time.sleep(5)

        alert.info("Activating HDCP2.2 and verifying in the background. Ensure no corruption.")
        logging.info("Activating HDCP2.2 on {}".format(self.__class__.enum_port_list))
        status = self.multi_display_single_session()

        if status is False:
            alert.info("FAIL: HDCP2.2 Activation Failed.")
            self.fail("HDCP2.2 Activation Failed.")

        user_msg = "[Expectation]:Make sure no corruption in Media Player or Displays. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed.")

        time.sleep(2)
        alert.info("Toggling Windowed to Fullscreen then Windowed operation for Media Player")
        time.sleep(2)

        self.toggle_window(True)
        self.toggle_window(False)

        alert.info("Note: Step to be done by user manually.\n"
                   "Move media player randomly across display.\n"
                   "Keeping timeout of 2min to complete this.\n"
                   "Expectation:There shouldn't be any corruption/flicker/blankout on display during video playback."
                   "Video playback should be smooth.")
        logging.info("Dragging media player across display.")
        # TODO: make it 120
        time.sleep(10)

        alert.info("Deactivating HDCP2.2 and verifying in the background. Ensure no corruption.")
        logging.info("Deactivating HDCP2.2 on {}".format(self.__class__.enum_port_list))
        status = self.multi_display_single_session()

        if status is False:
            alert.info("FAIL: HDCP2.2 Deactivation Failed.")
            self.fail("HDCP2.2 Deactivation Failed")

        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed.")

    ##
    # @brief Helper function to verify display configuration
    # @return None
    def verify_config(self, expected_config):
        if expected_config is None:
            alert.info("FAIL: expected config is None which is not expected.")
            self.fail("Passed config is None. Failing...")
        current_config = self.__class__.display_config.get_current_display_configuration()
        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        if expected_config.equals(current_config) is False:
            logging.error(f"Display configuration doesn't match. expected: "
                          f"{expected_config.to_string(enumerated_displays)} "
                          f"observed: {current_config.to_string(enumerated_displays)}")
            self.fail(f"Display configuration doesn't match.")
        else:
            logging.info(f"Display configuration matches: {current_config.to_string(enumerated_displays)}")

        user_msg = "[Expectation]:Make sure that display comes in previous configuration. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

    ##
    # @brief        Exposed method to toggle window of VideoPlayer
    # @param[in]    to_fullscreen bool, this will be just for logging purpose. Either way code will press "ALT+Enter"
    # @return       bool, True if successful False otherwise
    @staticmethod
    def toggle_window(to_fullscreen: bool) -> bool:
        app_handle = window_helper.get_window('Media')
        if app_handle is not None:
            app_handle.set_foreground()
            logging.info("Media player set to foreground")
        else:
            logging.info("Couldn't find media player.")

        winkb_helper.press("ALT_ENTER")
        logging.info(f"\tSuccessfully toggled video player to {'Fullscreen' if to_fullscreen else 'Windowed'}")
        time.sleep(2)
        return True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HdcpBasic22'))
    TestEnvironment.cleanup(outcome)