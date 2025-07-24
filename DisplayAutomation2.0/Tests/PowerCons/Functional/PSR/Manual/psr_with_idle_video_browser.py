########################################################################################################################
# @file         psr_with_idle_video_browser.py
# @brief        Manual sanity test to verify PSR with Video_Idle_Browser_Snip_And_sketch
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3415035/ TI.
# TI name       PSR with Idle_video_browser
# @author       Golwala, Ami
########################################################################################################################
import logging
import os
import time
import unittest

from Libs.Core.wrapper import control_api_wrapper

from Libs.Core import display_power, enum, reboot_helper, winkb_helper, display_essential, window_helper, app_controls, \
    display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.app import Youtube, App
from Libs.Feature.powercons import registry
from Libs.manual.modules import alert, action
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut, workload


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class PsrWithIdleVideoBrowser(unittest.TestCase):
    display_pwr = DisplayPower()
    display_config = DisplayConfiguration()
    snip_sketch_obj = workload.DxAppSnipAndSketchActivities()
    yt_obj = Youtube()
    gfx_index = 'gfx_0'
    registry_key = "FBRLatencyWA"

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief        This step does 24 FPS VPB with AC mode
    # @return       None
    def test_01_step(self):
        status = True
        user_msg = ("[Expectation]: Boot the system with only eDP planned in the grid."
                    "Make sure user login with password is enabled in the system."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("System is configured with login with password")

        user_msg = ("[Expectation]:Make sure to select option 'EveryTime' for 'If you have been away, When should "
                    "windows require you  to sign in again?' under settings ->Accounts -> sign-in options  -> "
                    "Additional settings page"
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False

        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(PowerEvent.CS)
        if is_cs_supported:
            logging.info("CS is supported by system")
        else:
            alert.info("Fail: CS is not supported. Rerun test with CS supported system")
            self.fail("CS is not supported. Rerun test with CS supported system")

        logging.info("Enabling Simulated Battery")
        assert self.__class__.display_pwr.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("PASS: Enabled Simulated Battery successfully")

        alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
        result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
        self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")

        user_msg = "[Expectation]:Power line should switch to AC mode" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Powerline changed to AC")

        alert.info("Launching VPB in full screen mode. \nNo visual artifacts seen during video playback")
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, '24.000.mp4'), False)
        time.sleep(5)
        # Switching to full screen
        winkb_helper.press('F11')
        logging.info("Playing the video in loop")
        winkb_helper.press('CTRL+T')  # play in loop
        time.sleep(60)
        # Switching to windowed mode for pop-ups to appear
        logging.info("Switching video to windowed mode")
        winkb_helper.press('F11')

        user_msg = "[Expectation]:No visual artifacts seen during video playback" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during video playback")

        if not status:
            self.fail("test_step_01 failed")

    ##
    # @brief        This step Pauses unpauses video
    # @return       None
    def test_02_step(self):
        status = True
        alert.info("Note: Step to be done by user manually."
                   "\nPause the video using mouse."
                   "\nWaiting for 30 sec")

        time.sleep(35)
        logging.info("User paused video using mouse")
        alert.info("Note: Step to be done by user manually."
                   "\nUnpause the video using mouse. Giving timeout of 10 seconds to perform this activity"
                   "\nNo visual artifacts seen during video playback")
        time.sleep(10)
        logging.info("User unpaused video using mouse")

        user_msg = "[Expectation]:No visual artifacts seen during video playback" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during video playback")

        if not status:
            self.fail("test_step_02 failed")

    ##
    # @brief        This step toggles AC DC
    # @return       None
    def test_03_step(self):
        status = True
        alert.info("Performing AC-DC switch for 5 times."
                   "\nThere shouldn't be any sudden brightness change during the AC-DC switch")

        for i in range(5):
            # Switching to full screen
            winkb_helper.press('F11')
            logging.info("Switching powerline to DC")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
            self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")

            time.sleep(10)
            # Switching to windowed mode for pop-up to appear
            winkb_helper.press('F11')
            user_msg = "[Expectation]:Power line should be in DC mode" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Powerline changed to DC")

            # Switching to full screen
            winkb_helper.press('F11')
            time.sleep(5)
            logging.info("Switching powerline to AC")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
            self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")

            time.sleep(10)
            # Switching to windowed mode for pop-up to appear
            winkb_helper.press('F11')
            user_msg = "[Expectation]:Power line should be in AC mode" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Powerline changed to AC")

            user_msg = ("[Expectation]: There shouldn't be any sudden brightness change during the AC-DC switch"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False

        # Switching to full screen
        winkb_helper.press('F11')

        if not status:
            self.fail("test_step_03 failed")

    ##
    # @brief        This step does VPB in windowed
    # @return       None
    def test_04_step(self):
        status = True
        logging.info("Switch VPB to windowed mode")
        winkb_helper.press('F11')
        time.sleep(60)

        user_msg = "[Expectation]:No visual artifacts seen during video playback" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during video playback")

        alert.info("Note: Step to be done by user manually."
                   "\nDrag the Video player across the screen for 30 sec."
                   "\nNo visual artifacts seen during video playback"
                   "Keeping timeout of 50s to perform this activity")
        logging.info("Dragging video player across the screen for 30sec")
        time.sleep(50)
        user_msg = "[Expectation]:No visual artifacts seen during video playback" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during video playback")

        window_helper.close_media_player()
        if not status:
            self.fail("test_step_04 failed")

    ##
    # @brief        This step plays Full screen video on YouTube
    # @return       None
    def test_05_step(self):
        status = True
        logging.info("Changing power line to DC mode")
        alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
        result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
        self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")

        user_msg = "[Expectation]:Power line should switch to DC mode" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Powerline changed to DC")

        alert.info("Opening youtube and playing video for 5mins."
                   "\n it will go to full screen mode, turn on caption, "
                   "switch to mini player mode and will play video for 5mins in mini player mode"
                   "\nNo visual artifacts seen during video playback")
        logging.info("Opening Youtube")
        self.__class__.yt_obj = Youtube(video_path="https://www.youtube.com/watch?v=YE7VzlLtp-4")
        handle = self.__class__.yt_obj.open_app(is_full_screen=False)
        time.sleep(10)
        logging.info("Switching youtube full screen mode")
        winkb_helper.press('f')
        time.sleep(5)
        logging.info("Turning caption on")
        winkb_helper.press('c')
        time.sleep(5)

        time.sleep(300)

        if not status:
            self.fail("test_step_05 failed")

    ##
    # @brief        This step enables Mini player mode video
    # @return       None
    def test_06_step(self):
        logging.info("Switching to mini player mode ")
        winkb_helper.press('i')
        time.sleep(5)
        time.sleep(300)

    ##
    # @brief        This step switches to normal mode
    # @return       None
    def test_07_step(self):
        status = True
        logging.info("Switching to normal mode")
        winkb_helper.press('i')
        time.sleep(5)
        winkb_helper.press('c')
        time.sleep(5)
        user_msg = "[Expectation]:No visual artifacts seen during video playback" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during video playback")

        if not status:
            self.fail("test_step_07 failed")

    ##
    # @brief        This step performs Web page scrolling
    # @return       None
    def test_08_step(self):
        status = True
        WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Wikipedia"
        alert.info("Opening wikipedia")
        logging.info("Open Wikipedia from Browser")
        workload.WinAppActivities.launch(True, workload.AppType.BROWSER, WIKIPEDIA_URL)
        hwnd = window_helper.get_window_handle('EDGE')
        if hwnd is None:
            self.fail("Application wikipedia is not open")
        App.set_foreground(hwnd)

        alert.info("Note: Step to be done by user manually."
                   "\nScroll the web page from top to bottom slowly using keyboard arrow keys."
                   "\nNo lag/flicker should be seen during scrolling through the web page"
                   "Keeping timeout of 20sec to perform this activity")
        time.sleep(20)

        user_msg = "[Expectation]:No lag/flicker should be seen during scrolling through the web page" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No lag/flicker were seen during scrolling through the web page")

        alert.info("Note: Step to be done by user manually."
                   "\nScroll faster the web page from bottom to top using the right side slider."
                   "\nNo lag/flicker should be seen during scrolling through the web page"
                   "Keeping timeout of 20sec to perform this activity")
        time.sleep(20)

        user_msg = "[Expectation]:No lag/flicker should be seen during scrolling through the web page" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No lag/flicker were seen during scrolling through the web page")

        logging.info("Closing Youtube")
        self.__class__.yt_obj.close_app()
        if not status:
            self.fail("test_step_08 failed")

    ##
    # @brief        This step performs preview mode video
    # @return       None
    def test_09_step(self):
        status = True
        logging.info("Opening youtube home")
        alert.info("Opening youtube home")
        self.__class__.yt_obj = Youtube(video_path="https://www.youtube.com/")
        handle = self.__class__.yt_obj.open_app(is_full_screen=False)
        alert.info("Note: Step to be done by user manually."
                   "\nHover the mouse and play any video."
                   "\nPlay video in preview mode"
                   "\nLet the preview mode play for 1 min"
                   "\nFlicker/corruption should not be seen"
                   "Keeping timeout of 70sec to perform this activity")
        logging.info("Hovering mouse and playing any video")
        time.sleep(70)

        user_msg = "[Expectation]:Flicker/corruption should not be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Flicker/corruption not seen")

        logging.info("Closing youtube")
        self.__class__.yt_obj.close_app()
        if not status:
            self.fail("test_step_09 failed")

    ##
    # @brief        This step checks PSR status in IGCC
    # @return       None
    def test_10_step(self):
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        if reboot_helper.reboot(self, 'test_11_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step opens Snip & Sketch APP
    # @return       None
    def test_11_step(self):
        status = True
        logging.info("Successfully booted to Desktop")

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info("Checking PSR status in IGCC")
                # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                           "Check panel self refresh feature status. PSR status should be enabled in IGCC for On "
                           "Battery. Keeping 1 minute of timeout to perform this activity")
                time.sleep(60)
                user_msg = "[Expectation]:PSR status should be enabled in IGCC for On Battery" \
                           "[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    logging.info("PSR is enabled in IGCC")

                driver_status = psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1)
                if not driver_status:
                    logging.error("PSR is disabled in driver")
                    status = False
                else:
                    logging.info("PSR is enabled in driver")

        alert.info("Launching Snipping tool."
                   "\nNo flicker/underrun/visual artifacts should be seen")
        self.__class__.snip_sketch_obj.launch(True)
        time.sleep(10)
        user_msg = "[Expectation]:No flicker/underrun/visual artifacts should be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No flicker/underrun/visual artifacts was seen")

        if not status:
            self.fail("test_step_11 failed")

    ##
    # @brief        This step does drawing with Snip & Sketch
    # @return       None
    def test_12_step(self):
        status = True
        alert.info("Drawing randomly for 60 seconds."
                   "\nLook for any visual artifacts seen during the drawing")
        logging.info("Drawing randomly for 60 seconds.")
        self.__class__.snip_sketch_obj.draw_random()
        self.__class__.snip_sketch_obj.draw_random()
        user_msg = "[Expectation]:any visual artifacts seen during the drawing?" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during the drawing")

        alert.info("Waiting for 30 seconds")
        time.sleep(30)

        self.__class__.snip_sketch_obj.close()
        alert.info("Launching Snipping tool")
        self.__class__.snip_sketch_obj.launch(True)

        alert.info("Note: Step to be done by user manually."
                   "\nStart Drawing again on screen."
                   "\nClick on Ball Point Pen Icon in APP and change Pencil size to 15 from the APP menu."
                   "\nVisual artifacts should be resolved after regkey addition"
                   "Keeping 40 seconds timeout to perform this activity")
        time.sleep(40)

        user_msg = "[Expectation]:No visual artifacts should be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen")

        for i in range(5):
            alert.info("Drawing randomly for 60 seconds."
                       "\nLook for any visual artifacts seen during the drawing")
            logging.info("Drawing randomly for 60 seconds.")
            self.__class__.snip_sketch_obj.draw_random()
            self.__class__.snip_sketch_obj.draw_random()
            user_msg = "[Expectation]:any visual artifacts seen during the drawing?" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("No visual artifacts were seen during the drawing")

            alert.info("Waiting for 30 seconds")
            time.sleep(30)

        if not status:
            self.fail("test_step_12 failed")

    ##
    # @brief        This step does Refresh Rate Change
    # @return       None
    def test_13_step(self):
        status = True
        alert.info("Note: Step to be done by user manually."
                   "\n Minimize Snip & sketch App."
                   "Keeping 20 seconds timeout to perform this activity")
        time.sleep(20)

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                current_mode = self.__class__.display_config.get_current_mode(
                    enumerated_display.ConnectedDisplays[index].DisplayAndAdapterInfo.TargetID)
                display_and_adapter_info = self.__class__.display_config.get_display_and_adapter_info_ex(port_type,
                                                                                                         self.__class__.gfx_index)
                if type(display_and_adapter_info) is list:
                    display_and_adapter_info = display_and_adapter_info[0]

                all_supported_modes = (self.__class__.display_config.get_all_supported_modes
                                       ([display_and_adapter_info]))
                for _, modes in all_supported_modes.items():
                    for mode in modes:
                        if (mode.HzRes == current_mode.HzRes and mode.VtRes == current_mode.VtRes and
                                mode.refreshRate != current_mode.refreshRate):
                            alert.info("Performing modeset with different RR")
                            logging.info("Performing modeset with different RR")
                            if not self.__class__.display_config.set_mode(mode):
                                alert.info("Fail: Failed to apply mode with refresh rate change")
                                self.fail("Failed to apply mode with refresh rate change")
                            logging.info(
                                f"Successfully set desired mode on {port_type}")
                            time.sleep(5)

        alert.info("Launching Snipping tool")
        self.__class__.snip_sketch_obj.launch(True)
        alert.info("Drawing randomly for 60 seconds."
                   "\nLook for any visual artifacts seen during the drawing")
        self.__class__.snip_sketch_obj.draw_random()
        self.__class__.snip_sketch_obj.draw_random()
        self.__class__.snip_sketch_obj.close()

        user_msg = "[Expectation]:No visual artifacts seen during drawing" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No visual artifacts were seen during drawing")

        if not status:
            self.fail("test_step_13 failed")

    ##
    # @brief        This step disables PSR in AC mode
    # @return       None
    def test_14_step(self):
        status = True
        alert.info("Changing regkey PsrDisableInAc val to 1 in driver key path"
                   "\nNo flicker/underrun/visual artifacts should be seen")
        logging.info("Changing regkey PsrDisableInAc val to 1 in driver key path")
        for adapter in dut.adapters.values():
            psr_ac = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=False)
            if psr_ac is False:
                logging.info("Failed to update the PsrDisableInAC reg key")
                self.fail("Failed to update the PsrDisableInAC reg key")
            elif psr_ac is None:
                logging.info("Successfully set PsrDisableInAc val to 1. Display driver restart is not required.")
            else:
                is_success, _ = display_essential.restart_gfx_driver()
                if is_success is False:
                    logging.error(f"Failed to restart display driver after updating PsrDisableInAC registry key")
                    status = False
                else:
                    logging.info("Successfully restarted display driver post updating PsrDisableInAc val to 1")

        user_msg = "[Expectation]:No flicker/underrun/visual artifacts should be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No flicker/underrun/visual artifacts was seen")

        alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
        result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
        self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")

        user_msg = "[Expectation]:Power line should switch to AC mode" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Powerline changed to AC")

        if not status:
            self.fail("test_step_14 failed")

        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        if reboot_helper.reboot(self, 'test_15_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step checks PSR status
    # @return       None
    def test_15_step(self):
        status = True
        logging.info("Successfully booted to Desktop")

        alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
        result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
        self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")

        user_msg = "[Expectation]:Power line should switch to DC mode" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Powerline changed to DC")

        alert.info("Note: Step to be done by user manually."
                   "\nMove the Mouse all over all the screen."
                   "\nThere should be no Lag /corruption during the mouse movement"
                   "Keeping timeout of 20sec for the activity")
        time.sleep(20)

        user_msg = "[Expectation]:There should be no Lag /corruption during the mouse movement" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Lag /corruption seen during the mouse movement")

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                    # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                logging.info("Checking PSR Status via IGCC")
                alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                           "Check panel self refresh feature status. PSR status should be enabled in IGCC for On "
                           "Battery. Keeping 1 minute of timeout to perform this activity")
                time.sleep(60)
                user_msg = "[Expectation]:PSR status should be enabled in IGCC for On Battery" \
                           "[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    logging.info("PSR is enabled in IGCC")

                driver_status = psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1)
                if not driver_status:
                    logging.error("PSR is disabled in driver")
                    status = False
                else:
                    logging.info("PSR is enabled in driver")

        if not status:
            self.fail("test_step_15 failed")

    ##
    # @brief        This step resets Regkey value
    # @return       None
    def test_16_step(self):
        status = True
        alert.info("Changing regkey PsrDisableInAc val to 0 in driver key path"
                   "\nNo flicker/underrun/visual artifacts should be seen")
        logging.info("Changing regkey PsrDisableInAc val to 0 in driver key path")
        for adapter in dut.adapters.values():
            # reset the reg key value
            psr_ac = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=True)
            if psr_ac is False:
                logging.info("Failed to update the PsrDisableInAC reg key")
                self.fail("Failed to update the PsrDisableInAC reg key")
            elif psr_ac is None:
                logging.info("Successfully set PsrDisableInAC val to 0. Display driver restart is not required.")
            else:
                is_success, _ = display_essential.restart_gfx_driver()
                if is_success is False:
                    logging.error(f"Failed to restart display driver after updating PsrDisableInAC registry key")
                    status = False
                else:
                    logging.info("Successfully restarted display driver post updating PsrDisableInAC val to 0.")

        user_msg = "[Expectation]:No flicker/underrun/visual artifacts should be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No flicker/underrun/visual artifacts was seen")

        # Delete FBRLatencyWA regkey in driver key path
        alert.info("Deleting FBRLatencyWA registry."
                   "\nNo flicker/underrun/visual artifacts should be seen")
        logging.info("Deleting FBRLatencyWA registry.")
        is_success = registry.delete(self.__class__.gfx_index, self.__class__.registry_key)
        if is_success is True:  # Registry deletion is successful, restart the display driver
            ret_val, _ = display_essential.restart_gfx_driver()
            if ret_val is False:
                logging.error(f"Failed to restart display driver after deleting "
                              f"{self.__class__.registry_key} registry key")
                status = False
            else:
                logging.info("Successfully deleted FBRLatencyWA registry")
        elif is_success is False:  # Registry deletion is failed.
            logging.error(f"Failed to delete {self.__class__.registry_key} registry value to 0x1 ")
            status = False
        else:  # Registry deletion not done
            logging.info(f"Skipping registry deletion for"
                         f"{self.__class__.registry_key} registry")

        user_msg = "[Expectation]:No flicker/underrun/visual artifacts should be seen" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No flicker/underrun/visual artifacts was seen")

        if not status:
            self.fail("test_step_16 failed")

        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        if reboot_helper.reboot(self, 'test_17_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step performs Video playback with external display
    # @return       None
    def test_17_step(self):
        status = True
        logging.info("Successfully booted to Desktop")
        user_msg = "Is external panel planned in grid?" \
                   "[CONFIRM]:Enter yes if planned, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            self.skipTest("Test is not planned with external panel.")

        alert.info("In following step, user will plug external panel. No TDR/Underrun & flicker should be observed "
                   "during plug ")
        result = action.plug('external')
        if not result:
            self.fail("Failed to plug external panel")
        user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed during plug" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Underrun & flicker was seen during plug")

        alert.info("Applying extended mode. No flicker/underrun/visual artifacts should be seen")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        enum_port_list = []
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                if display_utility.get_vbt_panel_type(port_type,
                                                      self.__class__.gfx_index) == display_utility.VbtPanelType.LFP_DP:
                    enum_port_list.append(port_type)

            for index in range(0, enumerated_display.Count):
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                if port_type not in enum_port_list:
                    enum_port_list.append(port_type)

            if len(enum_port_list) >= 2:
                ret_val = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                                     enum_port_list)
                if not ret_val:
                    alert.info("Applying Extended mode failed")
                    self.fail("Applying Extended mode failed")
                alert.info("Successfully applied extended mode")
            else:
                alert.info("Fail: Enumerated display count is less than 2, we can't apply extended mode")
                self.fail("Enumerated display count is is less than 2, we can't apply extended mode")
        else:
            alert.info("Fail: Enumerated display count is 0")
            self.fail("Enumerated display count is 0")

        user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No TDR/Underrun & flicker was seen while applying extended mode")

        alert.info("Launching video and switching to full screen mode."
                   "\nStep to be done by user manually: Unplug external panel once video is switched to full screen "
                   "mode")

        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, '24.000.mp4'), False)
        logging.info("Playing the video in loop")
        time.sleep(10)
        winkb_helper.press('CTRL+T')  # play in loop

        media_window_handle = window_helper.get_window('Media Player')
        if media_window_handle is None:
            self.fail("Application Media player is not open")
        media_window_handle.set_foreground()
        winkb_helper.press('F11')

        window_helper.close_media_player()

        if not status:
            self.fail("test_step_17 failed")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('PsrWithIdleVideoBrowser'))
    TestEnvironment.cleanup(outcome)
