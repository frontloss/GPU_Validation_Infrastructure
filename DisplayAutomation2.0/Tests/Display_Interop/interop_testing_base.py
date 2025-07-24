########################################################################################################################
# @file         interop_testing_base.py
# @brief        It contains setUp and tearDown methods of unittest framework.
# @details      For all Display Interop tests which is derived from this,
#               will make use of setup/teardown of this base class.
#               This script contains helper functions that will be used by test scripts.
# @author       Chandrakanth Pabolu
########################################################################################################################
import time
import unittest
from subprocess import call

from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core import enum, display_utility, window_helper, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration, configure_hdr
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import etl_tracer
from Libs.manual.modules import alert
from Tests.Color.Common.color_enums import RgbQuantizationRange
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Display_Interop import score_card

from score_card import *


##
# @brief        Base class
class InteropTestingBase(unittest.TestCase):
    display_config = DisplayConfiguration()
    gfx_index = "gfx_0"

    ##
    # @brief        This method initializes score card and other pre-requisites
    # @return       None
    def pretest_setup(self):
        self.__generate_topology()

        monitor_name = None
        enumerated_display = self.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = display_utility.get_vbt_panel_type(port_type, self.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and port_type != "VIRTUALDISPLAY":
                    monitor_name = enumerated_display.ConnectedDisplays[index].FriendlyDeviceName.replace(' ', '_')
                    break

        if not monitor_name:
            msg = alert.prompt('Please enter Monitor Name:', [{'name': 'Message'}])
            logging.info(f"User observations: {msg['Message']}")
            monitor_name = msg['Message'].replace(' ', '_')
        msg = alert.prompt('Please enter your idsid Name:', [{'name': 'Message'}])
        logging.info(f"User idsid: {msg['Message']}")
        idsid = msg['Message'].replace(' ', '_')
        score_card.init(monitor_name, idsid)

    ##
    # @brief        This method performs post processing
    # @return       None
    def post_process(self):
        panel_name = score_card.get_panel_name()
        dest_path = os.path.join(test_context.ROOT_FOLDER, panel_name)

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        dest_score_card = os.path.join(dest_path, "score_card.json")
        logging.info(f"Copying: {SCORE_CARD} to {dest_score_card}")
        shutil.copyfile(SCORE_CARD, dest_score_card)

        src_telemetry = os.path.join(test_context.ROOT_FOLDER, "TelemetryReport.json")
        if not os.path.exists(src_telemetry):
            logging.error(f"{src_telemetry} doesn't exist.")
            return
        dest_telemetry = os.path.join(dest_path, "TelemetryReport.json")
        logging.info(f"Copying: {src_telemetry} to {dest_telemetry}")
        shutil.copyfile(src_telemetry, dest_telemetry)

    ##
    # @brief        This method generates telemetry file by running -topo command
    # @return       None
    def __generate_topology(self):
        if not etl_tracer.stop_etl_tracer():
            logging.error("Failed to stop ETL capture")
            return False
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):

            try:
                DIANA_EXE = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna", "DiAna.exe")
                diana_cmd = " ".join([DIANA_EXE, etl_tracer.GFX_TRACE_ETL_FILE, "-topo"])
                logging.info(f"Parsing ETL file {etl_tracer.GFX_TRACE_ETL_FILE} with DiAna command {diana_cmd}")
                diana_return_error_code = call(diana_cmd, universal_newlines=True)
                logging.info("return_err_code : {0}".format(hex(diana_return_error_code)))

            except Exception as e:
                logging.error(f"Failed to parse ETL through DiAna with error - {e}")

            etl_file_path = os.path.join(
                test_context.LOG_FOLDER, 'GfxTrace_setup_' + str(time.time()) + '.etl')
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")
            return False

    ##
    # @brief        Unit-test setup function.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        if self.__class__.abort is True:
            self.skipTest("Aborting test.")

    def abort(self, msg):
        self.__class__.abort = True
        self.fail(msg)

    def apply_native_mode(self, display_and_adapterinfo: DisplayAndAdapterInfo):
        status = False

        mode = self.__class__.display_config.get_current_mode(display_and_adapterinfo)
        if mode is None:
            logging.error(f"Failed to get current mode for {display_and_adapterinfo.TargetID}")
            return False

        native_mode = self.__class__.display_config.get_native_mode(display_and_adapterinfo.TargetID)
        if native_mode is None:
            logging.error(f"Failed to get native mode for {display_and_adapterinfo.TargetID}")
            return False

        logging.info("Applying native mode")
        mode.HzRes, mode.VtRes = native_mode.hActive, native_mode.vActive
        mode.refreshRate, mode.scaling = native_mode.refreshRate, enum.MDS

        logging.info("Applying native mode")
        result = self.__class__.display_config.set_display_mode([mode])

        if result:
            current_mode = self.__class__.display_config.get_current_mode(display_and_adapterinfo)
            if (current_mode.HzRes == mode.HzRes and current_mode.VtRes == mode.VtRes and
                    current_mode.refreshRate == mode.refreshRate and current_mode.scaling == mode.scaling):
                logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3}".format(
                    current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
                status = True
        return status

    ##
    # @brief        Applies mode set with different resolutions and RR
    # @return       None
    def mode_change(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = display_utility.get_vbt_panel_type(port_type, self.__class__.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and port_type != "VIRTUALDISPLAY":
                    # Commenting for now. Will revisit if extending for multiple panels.
                    # ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [port_type])
                    # if not ret_val:
                    #     alert.info(f"Applying Single Display {port_type} failed")
                    #     self.fail(f"Applying Single Display {port_type} failed")
                    # alert.info(f"Successfully applied Single Display {port_type}")

                    target_id = int(enumerated_display.ConnectedDisplays[index].TargetID)
                    supported_modes = self.__class__.display_config.get_all_supported_modes([target_id])

                    for key, values in supported_modes.items():
                        for mode in values:
                            # Set all the supported modes
                            if mode.scaling == enum.MDS:
                                logging.info("Applying display mode: %s" % mode.to_string(enumerated_display))
                                alert.info("Applying display mode: %s" % mode.to_string(enumerated_display))

                                self.__class__.display_config.set_display_mode([mode])
                                time.sleep(3)
                                user_msg = (
                                    "[Expectation]: Ensure no corruption/issues seen.\n"
                                    "[CONFIRM]:Enter yes if expectation met, else enter no")
                                result = alert.confirm(user_msg)
                                if not result:
                                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                                    logging.error(f"User observations: {msg['Message']}")

    ##
    # @brief        Verifies audio on EFP
    # @return       None
    def audio_verification(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                display = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = display_utility.get_vbt_panel_type(display, self.__class__.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and display != "VIRTUALDISPLAY":
                    # Commenting for now. Will revisit if extending for multiple panels.
                    # ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE,
                    #                                                                      [display])
                    # if not ret_val:
                    #     alert.info(f"Applying Single Display {display} failed")
                    #     self.fail(f"Applying Single Display {display} failed")
                    # alert.info(f"Successfully applied Single Display {display}")

                    alert.info("Note: Step to be done by user manually.\n"
                               "Connect required audio device to output of EFP.\n"
                               "Play Tears_of_Steel_1920x800.mp4 clip.\n"
                               "Audio should play successfully and no distortion or corrupted audio should be heard.\n"
                               "Keeping timeout of 3min to complete this.")
                    time.sleep(3*60)
                    user_msg = ("[Expectation]: Audio should play successfully, and should be able to hear audio "
                                "without any corruption/issues."
                                "\n[CONFIRM]:Enter yes if expectation met, else enter no")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info(f"Audio played without any corruption/issues.")

    ##
    # @brief        This will verify VRR with game play
    # @return       None
    def game_play(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                display = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = display_utility.get_vbt_panel_type(display, self.__class__.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and display != "VIRTUALDISPLAY":
                    # Commenting for now. Will revisit if extending for multiple panels.
                    # alert.info(f"Applying single display {display}")
                    # logging.info(f"Applying single display {display}")
                    # status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE,
                    #                                                                     [display])
                    # if not status:
                    #     alert.info(f"Applying single display failed {display}")
                    #     self.fail(f"Applying single display failed {display}")

                    alert.info("Note: Step to be done by user manually.\n"
                               "Using steam (or similar software), run the game Warthunder. Play the game for 2 min."
                               "Keeping timeout of 3min to complete this.\n"
                               f"Game should launch without issues and gameplay should be smooth without any "
                               f"corruption/blankout issues.\n"
                               f"For VRR panel, in OSD tool info: VBI rate - value should change if the Content FPS is"
                               f"within the panel VRR Range.")
                    logging.info("Launching Warthunder game using steam software.")
                    time.sleep(180)

                    user_msg = (f"[Expectation]: Game should launch on EFP without issues. "
                                f"Gameplay should be smooth without any corruption/blankout issues."
                                f"For VRR panel, in OSD tool info: VBI rate - value should change if the Content FPS is"
                                f"within the panel VRR Range."
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info(f"Gameplay Warthunder was smooth on {display}")

                    alert.info("Note: Step to be done by user manually."
                               "\nUsing steam (or similar software), run any other game. Play the game for 2 min."
                               "Keeping timeout of 3min to complete this."
                               f"Game should launch on EFP without issues. Gameplay should be smooth without any "
                               f"corruption/blankout issues."
                               f"For VRR panel, in OSD tool info: VBI rate - value should change if the Content FPS is"
                               f"within the panel VRR Range.")
                    logging.info("Launching Game using steam software.")
                    time.sleep(180)

                    user_msg = (f"[Expectation]: Game should launch on EFP without issues. "
                                f"Gameplay should be smooth without any corruption/blankout issues."
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info(f"Gameplay is smooth on {display}")

    ##
    # @brief        This function will verify HDR
    # @return       None
    def hdr_verification(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        display_and_adapterinfo = enumerated_display.ConnectedDisplays[0].DisplayAndAdapterInfo

        logging.info(f"Step: Enabling HDR on {display_and_adapterinfo.ConnectorNPortType}")
        if configure_hdr(display_and_adapterinfo, True) is False:
            alert.info(f"Failed to enable HDR on {display_and_adapterinfo.port}. Enable manually and click OK.")

        logging.info("User playing HDR Video.")

        alert.info("Launching VPB in full screen mode.\nNo visual artifacts seen during video playback.\n"
                   "User to move player randomly and perform fullscreen and window mode.")
        media_path = os.path.join(test_context.SHARED_BINARY_FOLDER, 'Color\\HDR\\Video')
        video_file = os.path.join(media_path, 'Life_of_Pi_draft_Ultra-HD_HDR.mp4')
        window_helper.open_uri(video_file)

        logging.info("Successfully launched video playback")
        time.sleep(5 * 60)

        window_helper.close_media_player()

        alert.info("Press OK to proceed for disabling HDR.")

        if configure_hdr(display_and_adapterinfo, False) is False:
            alert.info(f"Failed to disable HDR on panel. Disable manually and click OK.")

    ##
    # @brief        This function will verify HDR
    # @return       None
    def verify_hdcp(self):
        alert.info("Note: Make sure latest CSME/GSC FW/HEVC codec installed. Check HDCP caps from OPM Lite tool.\n"
                   "Click OK to proceed.")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                display = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = display_utility.get_vbt_panel_type(display, self.__class__.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and display != "VIRTUALDISPLAY":

                    user_msg = (f"[Expectation]: Does {display} supports HDCP?"
                                f"\n[CONFIRM]:Enter yes if supports, else enter No")
                    result = alert.confirm(user_msg)
                    if not result:
                        logging.info(f"{display} doesn't support HDCP")
                        continue
                    else:
                        # Commenting for now. Will revisit if extending for multiple panels.
                        # alert.info(f"Applying single display {display}")
                        # logging.info(f"Applying single display {display}")
                        # status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE,
                        #                                                                     [display])
                        # if not status:
                        #     alert.info(f"Applying single display failed {display}")
                        #     self.fail(f"Applying single display failed {display}")

                        alert.info(f"Note: Step to be done by user manually."
                                   f"\nLaunch the Netflix app. Play any 2K video."
                                   f"\nKeeping timeout of 2 mins to perform this")
                        time.sleep(120)

                        user_msg = (f"[Expectation]: Netflix Video playback should run without issues. Video should be "
                                    f"playing in 2k mode."
                                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                        else:
                            logging.info(f"Successfully verified 2k video on Netflix")

                        alert.info(f"Note: Step to be done by user manually."
                                   f"\nLaunch the Netflix app. Play any 4K video."
                                   f"\nKeeping timeout of 2 mins to perform this")
                        time.sleep(120)

                        user_msg = (f"[Expectation]: Netflix Video playback should run without issues. Video should be "
                                    f"playing in 4k mode."
                                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                        else:
                            logging.info(f"Successfully verified 4k video on Netflix.")

    ##
    # @brief        Applies Quantization range for a particular display
    # @return       None
    def __apply_quantization_range(self, connector_port_type, display_and_adapterInfo, quant_range: RgbQuantizationRange):

        alert.info(f"Applying Quantization {quant_range.name}.")

        if configure_aviinfo(connector_port_type, display_and_adapterInfo, quant_range.value):
            logging.info("Successfully set quantization range: {0} through escape".format(quant_range))
        else:
            self.fail(
                "Fail to set quantization range: {0} through escape failed".format(quant_range))

        time.sleep(2)

        user_msg = (f"[Expectation]: Images look brighter with Quantization FULL and dull with Limited range."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"Successfully applied Quantization Range: {quant_range}")

    ##
    # @brief        This function will verify Quantization range
    # @return       return False if feature not supported else True
    def verify_quantization_range(self):
        #alert.info("Scenario: Verifying Quantization Range for supported panels.")
        logging.info("Scenario: Verifying Quantization Range for supported panels.")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                display = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                displayAndAdapterInfo = enumerated_display.ConnectedDisplays[index].DisplayAndAdapterInfo
                is_lfp_dp = display_utility.get_vbt_panel_type(display, self.__class__.gfx_index)
                if is_lfp_dp != display_utility.VbtPanelType.LFP_DP and display != "VIRTUALDISPLAY":
                    if is_lfp_dp == display_utility.VbtPanelType.DP or is_lfp_dp == display_utility.VbtPanelType.PLUS:
                        logging.info("RGB Quantization not supported for DP.")
                        return False

                    # Commenting for now. Will revisit if extending for multiple panels.
                    # alert.info(f"Applying single display {display}")
                    # logging.info(f"Applying single display {display}")
                    # status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE,
                    #                                                                     [display])
                    # if not status:
                    #     alert.info(f"Applying single display failed {display}")
                    #     self.fail(f"Applying single display failed {display}")

                    alert.info(f"Note: Step to be done by user manually.\n"
                               f"Launch the Quantization sample image in fullscreen. Click OK to proceed.")
                    time.sleep(5)

                    quant_range = RgbQuantizationRange.DEFAULT
                    self.__apply_quantization_range(display, displayAndAdapterInfo, quant_range)

                    quant_range = RgbQuantizationRange.FULL
                    self.__apply_quantization_range(display, displayAndAdapterInfo, quant_range)

                    quant_range = RgbQuantizationRange.LIMITED
                    self.__apply_quantization_range(display, displayAndAdapterInfo, quant_range)

                    quant_range = RgbQuantizationRange.DEFAULT
                    self.__apply_quantization_range(display, displayAndAdapterInfo, quant_range)
        return True

    ##
    # @brief        Unit-test teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    user_msg = f"Does panel:  supports HDR and is HDR option visible?\n" \
               "Enter yes if expectation met, else enter no."
    result = alert.confirm(user_msg)
    logging.info(result)
    # TestEnvironment.initialize()
    # outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    # TestEnvironment.cleanup(outcome.result)
    verify_observation_assign_score(Features.VRR)
