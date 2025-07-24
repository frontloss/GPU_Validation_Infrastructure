########################################################################################################################
# @file           vrr_with_multi_display.py
# @brief          To verify VRR(DcBalancing Enabled) with Multi Display
# Manual of       https://gta.intel.com/procedures/#/procedures/TI-3495156/ TI
# Manual TI name  VRR with Multi Display
# @author         Golwala, Ami
########################################################################################################################
import logging
import time
import unittest

from Libs.Core.wrapper import control_api_args

from Libs.Core import enum, window_helper, display_power, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Modules import dut, workload
from Tests.VRR import vrr


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class VrrWithMultiDisplay(unittest.TestCase):
    enum_port_list = []
    display1 = None
    display2 = None
    display_pwr = display_power.DisplayPower()
    display_config = DisplayConfiguration()
    gfx_index = "gfx_0"
    app = workload.Apps.FlipAt
    app_cfg = workload.FlipAtAppConfig()
    app_cfg.pattern_1 = [20, 5, 2, 1, 100]
    app_cfg.pattern_2 = [6, 3, 50, 1, 100]
    app_cfg.primary_color = [85, 78, 15]
    app_cfg.secondary_color = [80, 73, 15]
    app_cfg.game_args = [0, 1, 1]

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief This step enables VRR and Adaptive sync plus in IGCC
    # @return None
    def test_00_step(self):
        status = True
        alert.info("Follow steps mentioned next for Multiple display settings")
        # TODO: Later check if below step can be automated?
        user_msg = "Multiple display settings." \
                   "\nReference image: " \
                   "https://wiki.ith.intel.com/pages/viewpage.action?pageId=2615019917#ReferenceforManualTests-ConfigureoptionsforMultipleDisplays" \
                   "\nUncheck minimized Windows when a monitor is disconnected" \
                   "\n[CONFIRM]: Enter yes one done, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Multiple display settings completed. "
                         "Unchecked minimized Windows when a monitor is disconnected")

        alert.info("VRR, adaptive sync plus and HDR will be enabled based on panel's capability")
        dut.prepare()
        # Enable VRR and HDR from IGCC for each panel.
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Panel caps before enabling VRR, Adaptive sync plus, HDR(if panel supports) : {panel}")
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"VRR is not supported on {panel.port}")
                else:
                    logging.info(f"VRR is supported on {panel.port}")
                    logging.info(f"Enabling Adaptive sync plus on {panel.port}")
                    vrr.set_profile(panel, control_api_args.ctl_intel_arc_sync_profile_v.RECOMMENDED)
                    vrr_flag = vrr.enable_disable_adaptive_sync_plus(gfx_index=self.__class__.gfx_index, enable=True)
                    if not vrr_flag:
                        alert.info("Failed to enable adaptive sync plus in IGCC")
                        self.fail("Failed to enable adaptive sync plus in IGCC")
                    logging.info("Enabled adaptive sync plus in IGCC")
                if panel.hdr_caps.is_hdr_supported:
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"Failed to enable HDR on {panel.port}")
                dut.refresh_panel_caps(adapter)
                logging.info(f"Panel caps after enabling VRR, Adaptive sync plus, HDR(if panel supports)  : {panel}")
                logging.info(f"Modifying the appconfig based on vrr min:{panel.min_rr} and vrr max rr:{panel.max_rr}")
                self.__class__.app_cfg.pattern_1 = vrr.get_fps_pattern(panel.max_rr)
                self.__class__.app_cfg.pattern_2 = vrr.get_fps_pattern(panel.min_rr, False)

        # FPS tracking setting on monitor
        user_msg = "[Expectation]:Open Game Optimizer from settings and check monitor's running FPS." \
                   "\nsimilar setting should be there for all VRR panel to check monitor running FPS." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Monitor's running FPS is verified")

        if not status:
            self.fail("test_00_step failed")

    ##
    # @brief This step sets single display
    # @return None
    def test_01_step(self):
        status = True
        alert.info("Setting Single Display1. Look for any corruption while applying config")
        logging.info("Step1: Set Single Display with Display 1")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        self.__class__.display1 = self.__class__.enum_port_list[0]
        ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [self.__class__.display1])
        if not ret_val:
            self.fail(f"Applying SD on port {self.__class__.display1} failed.")
        alert.info("Please change to max rr if it is in lower rr and click OK.")
        user_msg = "[Expectation]: No corruption should be seen" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No corruption was seen when single display Display1 applied")

        user_msg = "[Expectation]:VRR options should show in IGCC if VRR supported panel is connected." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("VRR options are seen in IGCC for VRR supported panel")

        if not status:
            self.fail("test_01_step failed")

    ##
    # @brief This step runs Workload
    # @return None
    def test_02_step(self):
        status = True
        alert.info("Launching gaming app. Look for FPS change in FPS tracker")
        if workload.open_gaming_app(self.__class__.app, False, 'None', self.__class__.app_cfg) is False:
            self.fail(f"\tFailed to open {self.__class__.app} app(Test Issue)")
        logging.info(f"\t Step2: Launched {self.__class__.app} app successfully")
        alert.info("FPS should change in monitor FPS track if panel is external VRR panel."
                   "\nfor EDP we can't check FPS changed when Gaming workload running.")
        time.sleep(20)

        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                   "\nfor EDP we can't check FPS changed when Gaming workload running." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("FPS changed in monitor FPS track if panel is external VRR panel. for eDP we can't check FPS "
                         "when Gaming workload is running")

        if not status:
            self.fail("test_02_step failed")

    ##
    # @brief This step Hot Plugs display 2/ changes display config
    # @return None
    def test_03_step(self):
        status = True
        user_msg = "Hot plug Display2." \
                   "\n[CONFIRM]:Enter yes if Display is plugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Step3: Hot plugged Display2")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        updated_enum_port_list = []
        for index in range(0, enumerated_display.Count):
            updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if enumerated_display.Count == len(self.__class__.enum_port_list):
            if workload.close_gaming_app() is False:
                logging.error(f"Failed to close {self.__class__.app} app(Test Issue)")
            self.fail("After hot plug of display2, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = updated_enum_port_list

        status = status and self.check_and_open_flipat()

        # Enabling HDR, adaptive sync plus if panel supports
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
                if panel.hdr_caps.is_hdr_supported:
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"Failed to enable HDR on {panel.port}")
                dut.refresh_panel_caps(adapter)
                logging.info(f"Panel caps after enabling VRR, Adaptive sync plus, HDR(if panel supports)  : {panel}")

        alert.info("Setting Single Display2 and look for FPS change in FPS tracker")
        logging.info("Set Single Display with Display2")
        for disp in self.__class__.enum_port_list:
            if disp is not self.__class__.display1:
                self.__class__.display2 = disp
                ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [self.__class__.display2])
                if not ret_val:
                    self.fail(f"Applying SD on port {disp} failed.")

        alert.info("Please change to max rr if it is in lower rr and click OK.")

        status = status and self.check_and_open_flipat()

        if not status:
            self.fail("test_03_step failed")

    ##
    # @brief This step runs Workload
    # @return None
    def test_04_step(self):
        status = True
        time.sleep(10)
        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                   "\n(for EDP we can't check FPS changed) when Gaming workload running." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Step4: FPS changed in monitor FPS track for external VRR panel.")

        if not status:
            self.fail("test_04_step failed")

    ##
    # @brief This step Hot unplugs display2
    # @return None
    def test_05_step(self):
        status = True
        user_msg = "Hot unplug Display2. Keep looking at workload app." \
                   "\n[CONFIRM]:Enter yes if Display is unplugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Step5: Hot unplugged Display2")

        time.sleep(5)
        updated_enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if enumerated_display.Count >= len(self.__class__.enum_port_list):
            if workload.close_gaming_app() is False:
                logging.error(f"Failed to close {self.__class__.app} app(Test Issue)")
                status = False
            self.fail("After unplug of display2, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = updated_enum_port_list

        status = status and self.check_and_open_flipat()

        user_msg = "[Expectation]:Make sure workload app switch back to Display1 and running without any issue." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Workload app switched back to Display1 and running without any issue")

        alert.info("Closing app")
        if workload.close_gaming_app() is False:
            self.fail(f"Failed to close {self.__class__.app} app(Test Issue)")

        if not status:
            self.fail("test_05_step failed")

    ##
    # @brief This step Hotplugs display2
    # @return None
    def test_06_step(self):
        status = True
        user_msg = "Hot plug Display2." \
                   "\n[CONFIRM]:Enter yes if Display is plugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Step6: Hot plugged Display2")

        updated_enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if enumerated_display.Count == len(self.__class__.enum_port_list):
            self.fail("After hot plug of display2, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = updated_enum_port_list

        # Get current configuration
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        ret = self.__class__.display_config.get_current_display_configuration_ex(enumerated_display)
        logging.info(f'Current display configuration is {ret[0]}, {ret[1]}')

        user_msg = "[Expectation]:Confirm the config. Single Display display2 should come." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Single Display Display2 is current config post plugging Display2")

        alert.info("Please change to max rr if it is in lower rr and click OK.")

        alert.info("Launching workload app and look for FPS change in tracker")
        if workload.open_gaming_app(self.__class__.app, False, 'None', self.__class__.app_cfg) is False:
            self.fail(f"\tFailed to open {self.__class__.app} app(Test Issue)")
        logging.info(f"\tLaunched {self.__class__.app} app successfully")
        time.sleep(20)

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
            self.fail("test_06_step failed")

    ##
    # @brief This step applies extended mode
    # @return None
    def test_07_step(self):
        status = True
        alert.info("Applying extended mode")
        self.__class__.enum_port_list = []
        logging.info("Step7: Apply Extended Mode")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        ret_val = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                            self.__class__.enum_port_list)
        if not ret_val:
            self.fail("Applying Extended mode failed.")

        alert.info("Please change to max rr if it is in lower rr and click OK.")

        status = status and self.check_and_open_flipat()

        if not status:
            self.fail("test_07_step failed")

    ##
    # @brief This step drags app
    # @return None
    def test_08_step(self):
        status = True
        alert.info("Dragging and moving workload. Look for FPS change in tracker")
        logging.info("Step8: Drag and Move Workload from Display2 to Display1")
        # winkb_helper.press('WIN+D')
        app_handle = window_helper.get_window('D3D12')
        if app_handle is not None:
            app_handle.set_foreground()
        window_helper.drag_app_across_screen("D3D12", self.__class__.display1, self.__class__.gfx_index)
        time.sleep(30)

        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                   "\nfor EDP we can't check FPS changed when Gaming workload running." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("FPS changed in monitor FPS track if panel is external VRR panel "
                         "for eDP we can't check FPS when Gaming workload is running")

        if not status:
            self.fail("test_08_step failed")

    ##
    # @brief This step applies display config
    # @return None
    def test_09_step(self):
        status = True
        alert.info("Applying Single Display2")
        self.__class__.enum_port_list = []
        logging.info("Step9: Apply Single Display Display2 while running workload")
        status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [self.__class__.display2])
        if not status:
            self.fail("Applying Single Display Display2 mode failed.")

        alert.info("Please change to max rr if it is in lower rr and click OK.")
        status = status and self.check_and_open_flipat()

        if not status:
            self.fail("test_09_step failed")

    ##
    # @brief This step invokes power event CS/S3
    # @return None
    def test_10_step(self):
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)
        if is_cs_supported:
            alert.info("Performing power event CS")
            logging.info("Step10: Power event CS")
            self.perform_power_event(display_power.PowerEvent.CS, 30)
        else:
            alert.info("Performing power event S3")
            logging.info("Step10: Power event S3")
            self.perform_power_event(display_power.PowerEvent.S3, 30)

    ##
    # @brief This step invokes power event S4
    # @return None
    def test_11_step(self):
        alert.info("Performing power event S4")
        logging.info("Step11: Power event S4")
        self.perform_power_event(display_power.PowerEvent.S4, 30)

    ##
    # @brief This step invokes power event S5
    # @return None
    def test_12_step(self):
        data = {'display1': self.__class__.display1, 'display2': self.__class__.display2}
        alert.info("Performing power event S5. Once system boots back to Desktop, rerun the test with same "
                   "commandline to continue execution")
        logging.info("Step12: Power event S5")
        if reboot_helper.reboot(self, 'test_13_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This function gets executed after reboot.
    # @return None
    def test_13_step(self):
        status = True
        logging.info("Successfully applied power event S5 state")
        data = reboot_helper._get_reboot_data()
        self.__class__.display1 = data['display1']

        alert.info("Launching workload app")
        if workload.open_gaming_app(self.__class__.app, False, 'None', self.__class__.app_cfg) is False:
            self.fail(f"\tFailed to open {self.__class__.app} app(Test Issue)")
        logging.info(f"\tLaunched {self.__class__.app} app successfully")
        alert.info("Keep track of FPS change in tracker")
        time.sleep(20)

        user_msg = f"[Expectation]:VRR options should show in IGCC if VRR supported panel is connected" \
                   "\n[CONFIRM]:Enter Yes is expectation met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("VRR options is seen in IGCC if VRR supported panel is connected")

        alert.info("Applying Single Display1")
        logging.info("Setting Single Display with Display 1")
        ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [self.__class__.display1])
        if not ret_val:
            self.fail(f"Applying SD on port {self.__class__.display1} failed.")

        alert.info("Please change to max rr if it is in lower rr and click OK.")
        status = status and self.check_and_open_flipat()

        alert.info("Closing FlipAt app")
        logging.info("Closing FlipAt app")
        if workload.close_gaming_app() is False:
            self.fail(f"Failed to close {self.__class__.app} app(Test Issue)")

        if not status:
            self.fail("test_13_step failed")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
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
    # @brief        This method helps in Setting Power Events- S3, S4, S5
    # @param[in]    power_state: Power state to be invoked
    #                   power state to be applied EX: CS, s3, s4, s5
    # @param[in]    resume_time: int
    #                   It is the time the system has to wait before resuming from the power state
    # @return       None
    def perform_power_event(self, power_state: display_power.PowerEvent, resume_time: int):
        status = True
        time.sleep(2)
        if self.display_pwr.invoke_power_event(power_state, resume_time) is False:
            self.fail(f'Failed to invoke power event')

        status = status and self.check_and_open_flipat()

        alert.info("Keep track of FPS change in tracker")
        time.sleep(10)
        user_msg = "[Expectation]:FPS should change in monitor FPS track if panel is external VRR panel." \
                   "\nfor EDP we can't check FPS changed when Gaming workload running." \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Monitor's running FPS is verified")

        if not status:
            self.fail("Verification post power event failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('VrrWithMultiDisplay'))
    TestEnvironment.cleanup(outcome)
