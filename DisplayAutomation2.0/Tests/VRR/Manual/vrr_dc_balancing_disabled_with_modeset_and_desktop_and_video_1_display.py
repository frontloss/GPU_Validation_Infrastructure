########################################################################################################################
# @file           vrr_dc_balancing_disabled_with_modeset_and_desktop_and_video_1_display.py
# @brief          To verify VRR(DcBalancing Disabled) with ModeSet(ModeRr_Resolution) and Desktop and Video
# Manual of       https://gta.intel.com/procedures/#/procedures/TI-3495140/
# Manual TI name  VRR(DcBalancing Disabled) with ModeSet(ModeRr_Resolution) and Desktop and Video 1-display
# @author         Golwala, Ami
########################################################################################################################
import logging
import os
import time
import unittest
from math import floor, ceil

from Libs.Core import winkb_helper, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_args
from Libs.manual.modules import alert
from Tests.BFR import bfr
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Modules import dut, workload, common
from Tests.VRR import vrr


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class VrrDcBalancingDisabledWithModesetAndDesktopAndVideo1Display(unittest.TestCase):
    enum_port_list = []
    display_config = DisplayConfiguration()
    is_bfr_supported_panel = False
    app = workload.Apps.FlipAt
    app_cfg = workload.FlipAtAppConfig()
    app_cfg.pattern_1 = [20, 5, 2, 1, 100]
    app_cfg.pattern_2 = [6, 3, 50, 1, 100]
    app_cfg.primary_color = [85, 78, 15]
    app_cfg.secondary_color = [80, 73, 15]
    app_cfg.game_args = [0, 1, 1]
    gfx_index = 'gfx_0'
    mode_list = []
    multi_rr_supported = False
    target_id = 0
    min_rr = 0
    max_rr = 0
    mid_rr = 0

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @classmethod
    def setUpClass(cls):
        pass

    ##
    # @brief This step enables VRR and Adaptive sync plus in IGCC
    # @return None
    def t_00_step(self):

        user_msg = "[Expectation]:Boot the system with planned panel." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panel")

        dut.prepare()
        # Enable VRR and HDR from IGCC for each panel.
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Panel caps before enabling VRR/HDR if supported : {panel}")
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"VRR is not supported on current panel {panel.port}")
                else:
                    logging.info(f"VRR is supported on current panel {panel.port}")
                    logging.info(f"Enabling Adaptive sync plus on {panel.port}")
                    vrr.set_profile(panel, control_api_args.ctl_intel_arc_sync_profile_v.RECOMMENDED)
                    vrr_flag = vrr.enable_disable_adaptive_sync_plus(gfx_index=self.__class__.gfx_index, enable=True)
                    if not vrr_flag:
                        alert.info("Failed to enable adaptive sync plus in IGCC")
                        self.fail("Failed to enable adaptive sync plus in IGCC")
                    alert.info("Enabled adaptive sync plus in IGCC")
                if panel.hdr_caps.is_hdr_supported:
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"Failed to enable HDR on {panel.port}")
                else:
                    logging.info("HDR is not supported on this panel")
                dut.refresh_panel_caps(adapter)
                logging.info(f"Panel caps after enabling VRR/HDR if supported : {panel}")

    ##
    # @brief This step Disables "Adaptive Sync Plus" in IGCC
    # @return None
    def t_01_step(self):
        alert.info("Disabling Adaptive Sync plus in IGCC.")
        logging.info("Step 1: Disable Adaptive Sync Plus")
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Panel caps before disabling Adaptive sync plus : {panel}")
                vrr_flag = vrr.enable_disable_adaptive_sync_plus(gfx_index=self.__class__.gfx_index, enable=False)
                if not vrr_flag:
                    logging.info("Failed to disable adaptive sync plus in IGCC")
                    self.fail("Failed to disable adaptive sync plus in IGCC")
                alert.info("Disabled adaptive sync plus in IGCC")
                dut.refresh_panel_caps(adapter)
                logging.info(f"Panel caps after disabling Adaptive sync plus  : {panel}")
                if len(panel.rr_list) > 2:
                    logging.info("More than 2 RR supported on this panel")
                    self.__class__.multi_rr_supported = True
                    panel.rr_list = sorted(panel.rr_list)
                    self.__class__.mid_rr = panel.rr_list[floor(len(panel.rr_list) / 2)]
                self.__class__.max_rr = panel.max_rr
                self.__class__.min_rr = panel.min_rr

    ##
    # @brief This step does Modeset during VRR workload in Min RR
    # @return None
    def t_02_step(self):
        # VRR is not expected to work if active RR is equals to min RR.
        # So, avoid applying min RR for positive test cases.
        alert.info("Performing Modeset during VRR workload in Min RR")
        # Apply Min RR from OS settings
        logging.info("Step 2:Modeset during VRR workload in Min RR")

        self.__class__.enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        for display_index in range(self.__class__.enumerated_displays.Count):
            if self.__class__.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                self.__class__.target_id = self.__class__.enumerated_displays.ConnectedDisplays[
                    display_index].TargetID
                all_supported_modes = self.__class__.display_config.get_all_supported_modes(
                    [self.__class__.target_id])
                for key, values in all_supported_modes.items():
                    for mode in values:
                        if mode.refreshRate == self.__class__.min_rr:
                            self.__class__.mode_list.append(mode)

        if len(self.__class__.mode_list) != 0:
            if self.__class__.display_config.set_display_mode([self.__class__.mode_list[0]]) is False:
                self.fail("Failed to set display mode with Minimum RR")
            logging.info("Successfully set display mode with Minimum RR ")
        else:
            self.fail("Mode list shouldn't be empty with MinRR.")

        alert.info("Launching FlipAt app")
        if workload.open_gaming_app(self.__class__.app, False, 'None', self.__class__.app_cfg) is False:
            self.fail(f"\tFailed to open {self.__class__.app} app(Test Issue)")
        logging.info(f"\tLaunched {self.__class__.app} app successfully")

        # Apply low/mid/high resolution, while workload running and visible in windowed mode
        logging.info(
            "Applying low/mid/high resolution with Min RR while workload running and visible in windowed mode ")
        self.apply_rr_and_set_mode(self.__class__.target_id, rr=self.__class__.min_rr)

    ##
    # @brief This step does Modeset during VRR workload in Mid RR
    # @return None
    def t_03_step(self):
        if self.__class__.multi_rr_supported:
            alert.info("Performing modeset during VRR workload in Mid RR")
            logging.info("Panel supports multiple RR")
            logging.info("Step 3: Applying low/mid/high resolution with Mid RR while workload running and visible in "
                         "windowed mode")
            self.apply_rr_and_set_mode(self.__class__.target_id, rr=self.__class__.mid_rr)

    ##
    # @brief This step does Modeset during VRR workload in Max RR
    # @return None
    def t_04_step(self):
        alert.info("Performing modeset during VRR workload in Max RR")
        logging.info("Step 4:Modeset during VRR workload in Max RR")
        logging.info(
            "Applying low/mid/high resolution with Max RR while workload running and visible in windowed mode ")
        self.apply_rr_and_set_mode(self.__class__.target_id, rr=self.__class__.max_rr)

    ##
    # @brief This step does Game (Async Flip) + Desktop mode (Sync Flip)
    # @return None
    def t_05_step(self):
        status = True
        alert.info("Keep eye on monitor FPS track while Game is running")
        logging.info("Step 5:Game (Async Flip) + Desktop mode (Sync Flip)")

        for i in range(4):
            winkb_helper.press('WIN+D')
            time.sleep(1)
            winkb_helper.press('WIN+D')
            user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                       "\n(for EDP we can't check FPS changed) when Gaming workload running." \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("FPS changed in monitor FPS track if panel is external VRR panel "
                             "(for eDP we can't check FPS) when Gaming workload is running")

            status = status and self.check_and_open_flipat()

        if not status:
            self.fail("test_05_step failed")

    ##
    # @brief This step does Game (Async Flip) + Desktop mode (Sync Flip)
    # @return None
    def t_06_step(self):
        status = True
        alert.info("Setting dynamic RR if supported and keep eye on monitor FPS track")
        # Note: If panel is not BFR supported, skip this section
        logging.info("Step 6: Game (Async Flip) + Desktop mode (Sync Flip). Skip this step if panel is not BFR "
                     "supported")
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Panel caps before setting Dynamic RR mode : {panel}")
                if panel.bfr_caps.is_bfr_supported:
                    if bfr.set_dynamic_rr(panel) is False:
                        if workload.close_gaming_app() is False:
                            self.fail(f"Failed to close {self.__class__.app} app(Test Issue)")
                        self.fail("Unable to set to Dynamic RR mode")
                    else:
                        logging.info("Successfully set dynamic RR mode")
                    dut.refresh_panel_caps(adapter)
                    logging.info(f"Panel caps after setting Dynamic RR mode : {panel}")
                    status = status and self.check_and_open_flipat()
                    for i in range(5):
                        winkb_helper.press('WIN+D')
                        time.sleep(5)
                        winkb_helper.press('WIN+D')
                        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR " \
                                   "panel. \n(for EDP we can't check FPS changed) when Gaming workload " \
                                   "running." \
                                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info("FPS changed in monitor FPS track if panel is external VRR panel "
                                         "(for eDP we can't check FPS) when Gaming workload is running")
        if not status:
            self.fail("test_06_step failed")

    ##
    # @brief This step Enables "Adaptive Sync Plus"
    # @return None
    def t_07_step(self):
        status = True
        alert.info("Enabling adaptive sync plus in IGCC")
        logging.info("Enable Adaptive Sync Plus")
        self.__class__.mode_list = []
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Panel caps before enabling VRR, Adaptive sync plus, HDR(if panel supports) : {panel}")
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"VRR is not supported on current panel {panel.port}")
                else:
                    logging.info(f"VRR is supported on current panel {panel.port}")
                    logging.info(f"Enabling Adaptive sync plus on {panel.port}")
                    vrr.set_profile(panel, control_api_args.ctl_intel_arc_sync_profile_v.RECOMMENDED)
                    vrr_flag = vrr.enable_disable_adaptive_sync_plus(gfx_index=self.__class__.gfx_index, enable=True)
                    if not vrr_flag:
                        alert.info("Failed to enable adaptive sync plus in IGCC")
                        self.fail("Failed to enable adaptive sync plus in IGCC")
                    logging.info("Enabled adaptive sync plus in IGCC")
                dut.refresh_panel_caps(adapter)
                logging.info(f"Panel caps after enabling Adaptive sync plus : {panel}")

                status = status and self.check_and_open_flipat()
                if len(panel.rr_list) > 2:
                    logging.info("More than 2 RR supported on this panel")
                    self.__class__.multi_rr_supported = True
                    panel.rr_list = sorted(panel.rr_list)
                    total_rr_supported = len(panel.rr_list)
                    self.__class__.mid_rr = panel.rr_list[floor(total_rr_supported / 2)]
                self.__class__.max_rr = panel.max_rr
                self.__class__.min_rr = panel.min_rr

        if not status:
            self.fail("test_07_step failed")

    ##
    # @brief This step does Modeset during VRR workload in Min RR
    # @return None
    def t_08_step(self):
        self.t_02_step()

    ##
    # @brief This step does Modeset during VRR workload in Mid RR
    # @return None
    def t_09_step(self):
        self.t_03_step()

    ##
    # @brief This step does Modeset during VRR workload in Max RR
    # @return None
    def t_10_step(self):
        alert.info("Performing modeset during VRR workload in Max RR")
        logging.info("Step10: Applying low/mid/high resolution with Max RR while workload running and visible in "
                     "windowed mode ")
        self.apply_rr_and_set_mode(self.__class__.target_id, rr=self.__class__.max_rr)

    ##
    # @brief This step does Game playback (windowed) + video playback( Full screen ) in single display
    # @return None
    def t_11_step(self):
        status = True
        alert.info("Performing game and video playback in single display")
        logging.info("Step 11: Game playback ( windowed) + video playback( Full screen ) in single display")

        window_helper.open_uri(os.path.join(common.TEST_VIDEOS_PATH, '24.000.mp4'))
        time.sleep(5)
        logging.info("Launched 24 FPS video successfully.")

        app_handle = window_helper.get_window('D3D12')
        if app_handle is not None:
            app_handle.set_foreground()
            logging.info("Gaming app is set in foreground")
            winkb_helper.press(' ')

        winkb_helper.press('ALT+TAB')
        winkb_helper.press('ENTER')
        winkb_helper.press("F11")
        time.sleep(10)
        winkb_helper.press('ALT+TAB')
        winkb_helper.press('ENTER')
        time.sleep(10)

        status = status and self.check_and_open_flipat()
        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                   "\n(for EDP we can't check FPS changed) when Gaming workload running." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("FPS changed in monitor FPS track if panel is external VRR panel "
                         "(for eDP we can't check FPS) when Gaming workload is running")

        if not status:
            self.fail("test_11_step failed")

    ##
    # @brief This step closes apps and does Modeset during VRR workload in Min RR
    # @return None
    def t_12_step(self):
        alert.info("Closing apps")
        # Step 12: Close App
        logging.info("Step 12: Close Apps")
        if workload.close_gaming_app() is False:
            logging.error(f"Failed to close {self.__class__.app} app(Test Issue)")

        window_helper.close_media_player()
        logging.info("Closing video playback")

        logging.info(
            f"Applying display mode {self.__class__.mode_list[0].HzRes}x{self.__class__.mode_list[0].VtRes}@{self.__class__.mode_list[0].refreshRate}Hz")
        if self.__class__.display_config.set_display_mode([self.__class__.mode_list[0]]) is False:
            self.fail("Failed to set display mode with Minimum RR")
        logging.info("Successfully set display mode with Minimum RR")

        alert.info("Test completed")

    ##
    # @brief        This method is the exit point for test.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        pass

    ##
    # @brief        This method helps checking if FlipAt app is running and if not running, launch the app
    # @return       status: bool. Returns True if app is running, else False
    def check_and_open_flipat(self):
        status = True
        if not window_helper.is_process_running("FlipAt.exe"):
            logging.error("FlipAt is not running")
            if workload.open_gaming_app(self.__class__.app, False, 'None', self.__class__.app_cfg) is False:
                self.fail(f"\tFailed to open {self.__class__.app} app(Test Issue)")
            logging.info(f"\tLaunched {self.__class__.app} app successfully")
            status = False
        return status

    ##
    # @brief        This method helps in applying given RR and do modeset
    # @param[in]    target_id: int
    # @param[in]    rr: int
    # @return       None
    def apply_rr_and_set_mode(self, target_id: int, rr: int):
        status = True
        status = status and self.check_and_open_flipat()

        alert.info("Please keep an eye on change in monitor FPS track")
        apply_mode_list = []
        modes = common.get_display_mode(target_id, rr, limit=None)

        # Apply Min/Mid/High resolution
        if len(modes) != 0:
            apply_mode_list.append(modes[0])
            apply_mode_list.append(modes[-1])

            if len(modes) >= 3:
                mid_length = ceil(len(modes) / 2)
                apply_mode_list.append(modes[mid_length])

            alert.info("Performing display modeset")
            for mode in apply_mode_list:
                if self.__class__.display_config.set_display_mode([mode]) is False:
                    if workload.close_gaming_app() is False:
                        self.fail(f"Failed to close {self.__class__.app} app(Test Issue)")
                    self.fail("FAILED to set display mode")
                logging.info(f'Successfully applied display mode with {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz')
                time.sleep(20)

                status = status and self.check_and_open_flipat()

                if rr == self.__class__.min_rr:
                    user_msg = "[Expectation]:FPS should not change in monitor FPS track when RR value is low." \
                               "\nVRR options should show in IGCC if VRR supported panel is connected." \
                               "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                else:
                    user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                               "\n(for EDP we can't check FPS changed) when Gaming workload running." \
                               "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    if rr == self.__class__.min_rr:
                        logging.info("FPS is not changed in monitor FPS track when RR value is low."
                                     "VRR options seen in IGCC when VRR supported panel is connected")
                    else:
                        logging.info("FPS changed in monitor FPS track if panel is external VRR panel "
                                     "(for eDP we can't check FPS) when Gaming workload is running")
        else:
            self.fail(f"There are no modes supported with {rr} RR")

        if not status:
            self.fail("FlipAt is not running")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class, verbosity=2)
    test_result = runner.run(common.get_test_suite(VrrDcBalancingDisabledWithModesetAndDesktopAndVideo1Display))
    TestEnvironment.cleanup(test_result)
