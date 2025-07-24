########################################################################################################################
# @file         psr_with_igcc_lid.py
# @brief        Manual sanity test to verify PSR with IGCC
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3418843/ TI.
#               Manual test name: PSR with IGCC_Lid
# @author       Golwala, Ami
########################################################################################################################
import logging
import os
import time
import unittest

from Libs.Core.wrapper import control_api_wrapper

from Libs.Core import display_power, enum, reboot_helper, winkb_helper, display_essential, window_helper, app_controls
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower, PowerScheme, PowerEvent
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert, action
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class PsrWithIgccLid(unittest.TestCase):
    display_pwr = DisplayPower()
    display_config = DisplayConfiguration()

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief        This step checks PSR status in IGCC
    # @return       None
    def test_01_step(self):
        status = True
        user_msg = ("[Expectation]:Make sure user login with password is enabled in the system."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("System is configured with login with password")

        user_msg = ("[Expectation]:Make sure to select option 'EveryTime' for 'If you have been away, When should "
                    "windows require you to sign in again?' under settings ->Accounts -> sign-in options  -> "
                    "Additional settings page"
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("System is configured to ask sign in everytime if you have been away")

        dut.prepare()
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(PowerEvent.CS)
        if is_cs_supported:
            logging.info("CS is Supported")
        else:
            alert.info("Fail: CS is not supported. Rerun test with CS supported system")
            self.fail("CS is not supported. Rerun test with CS supported system")

        logging.info("Enabling Simulated Battery")
        assert self.__class__.display_pwr.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("PASS: Enabled Simulated Battery successfully")

        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
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
        else:
            alert.info("Powerline is in DC mode")
            logging.info("Powerline is in DC mode")

        alert.info("In following step, user will plug external panel. No TDR/Underrun & flicker should be observed "
                   "during plug")
        result = action.plug('external')
        if not result:
            self.fail("Failed to plug external panel")
        user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed during plug" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No TDR/Underrun & flicker was seen during plug")

        alert.info("Applying extended mode")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            enum_port_list = []
            if enumerated_display.Count >= 2:
                for index in range(0, enumerated_display.Count):
                    enum_port_list.append(
                        str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
                ret_val = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                                     enum_port_list)
                if not ret_val:
                    alert.info("Applying Extended mode failed")
                    self.fail("Applying Extended mode failed")
                alert.info("Successfully applied extended mode")
                logging.info("Successfully applied extended mode")
            else:
                alert.info("Fail: Enumerated display count is less than 2, we can't apply extended mode")
                self.fail("Enumerated display count is is less than 2, we can't apply extended mode")
        else:
            alert.info("Fail: Enumerated display count is 0")
            self.fail("Enumerated display count is 0")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info("Getting PSR Status via IGCC")
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

        if not status:
            self.fail("test_step_01 failed")

    ##
    # @brief This step keeps IDLE Desktop
    # @return None
    def test_02_step(self):
        alert.info("Keeping system IDLE for 1min")
        logging.info("Keeping system IDLE for 1min")
        winkb_helper.press('WIN+M')
        winkb_helper.press('WIN+D')
        time.sleep(60)

        alert.info("In following step, user will unplug external panel. No TDR/Underrun & flicker should be observed "
                   "during unplug ")
        result = action.unplug('external')
        if not result:
            self.fail("Failed to unplug external panel")
        user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed during unplug" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No TDR/Underrun & flicker was seen during unplug")

        alert.info("Keeping system IDLE for 10min")
        logging.info("Keeping system IDLE for 10min")
        winkb_helper.press('WIN+M')
        winkb_helper.press('WIN+D')

        time.sleep(600)

    ##
    # @brief This step performs AC - DC toggle
    # @return None
    def test_03_step(self):
        status = True
        for i in range(10):
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

            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if not panel.is_lfp:
                        continue

                    logging.info("Getting PSR Status via IGCC")
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

            alert.info("Keeping system IDLE for 1min")
            logging.info("Keeping system IDLE for 1min")
            winkb_helper.press('WIN+M')
            winkb_helper.press('WIN+D')
            time.sleep(60)

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
                status = False
            else:
                logging.info("No TDR/Underrun & flicker was seen during plug")

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

            alert.info(
                "In following step, user will unplug external panel. No TDR/Underrun & flicker should be observed "
                "during unplug ")
            result = action.unplug('external')
            if not result:
                self.fail("Failed to unplug external panel")
            user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed during unplug" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("No TDR/Underrun & flicker was seen during unplug")

            if i == 0:
                alert.info("Keeping system IDLE for 1min")
                logging.info("Keeping system IDLE for 1min")
                winkb_helper.press('WIN+M')
                winkb_helper.press('WIN+D')
                time.sleep(60)

        if not status:
            self.fail("test_step_03 failed")

    ##
    # @brief This step enables HDR and AC mode
    # @return None
    def test_04_step(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                if panel.hdr_caps.is_hdr_supported:
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
                    logging.info(f"Panel caps before enabling HDR: {panel}")
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"Failed to enable HDR on {panel.port}")
                else:
                    logging.info(f"eDP doesn't support HDR")
        if not status:
            self.fail("test_step_04 failed")

    ##
    # @brief This step checks PSR status
    # @return None
    def test_05_step(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info("Getting PSR Status via IGCC")
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
        if not status:
            self.fail("test_step_05 failed")

    ##
    # @brief This step checks PSR in PowerSaver
    # @return None
    def test_06_step(self):
        self.check_psr_in_power_mode(PowerScheme.POWER_SAVER)

    ##
    # @brief This step checks PSR in Best Performance
    # @return None
    def test_07_step(self):
        self.check_psr_in_power_mode(PowerScheme.HIGH_PERFORMANCE)

    ##
    # @brief This step checks PSR in Balanced
    # @return None
    def test_08_step(self):
        self.check_psr_in_power_mode(PowerScheme.BALANCED)

    ##
    # @brief This step toggles PSR for 15 times
    # @return None
    def test_09_step(self):
        status = True
        alert.info("Enabling-disabling PSR in IGCC for 15 times.\nNo visual artifacts should be seen during PSR toggle")
        for i in range(15):
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    logging.info(f"Toggling PSR in IGCC for {i + 1} time ")
                    psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=False)
                    if not psr_status:
                        alert.info("Failed to disable PSR in IGCC")
                        self.fail("Failed to disable PSR in IGCC")
                    else:
                        logging.info("Disabled PSR in IGCC")
                        # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                        alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                                   "Check panel self refresh feature status. PSR status should be disabled in IGCC "
                                   "for On Battery. Keeping 1 minute of timeout to perform this activity")
                        time.sleep(60)
                        user_msg = "[Expectation]:PSR status should be disabled in IGCC for On Battery" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info("PSR is disabled in IGCC")
                            driver_status = psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1)
                            if driver_status:
                                logging.error("PSR is enabled in driver")
                                status = False
                            else:
                                logging.info("PSR is disabled in driver")

                    time.sleep(2)
                    psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=True)
                    if not psr_status:
                        alert.info("Failed to enable PSR in IGCC")
                        self.fail("Failed to enable PSR in IGCC")
                    else:
                        logging.info("Enabled PSR in IGCC")
                        # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                        alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                                   "Check panel self refresh feature status. PSR status should be enabled in IGCC for "
                                   "On Battery. Keeping 1 minute of timeout to perform this activity")
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

                    user_msg = (f"[Expectation]:No visual artifacts should be seen during PSR toggle"
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                        status = False
                    else:
                        logging.info(f"No visual artifacts were seen during PSR toggle")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info("disabling PSR in IGCC")
                psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=False)
                if not psr_status:
                    alert.info("Failed to disable PSR in IGCC")
                    self.fail("Failed to disable PSR in IGCC")
                else:
                    logging.info("Disabled PSR in IGCC")
                    # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                    alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                               "Check panel self refresh feature status. PSR status should be disabled in IGCC for On "
                               "Battery. Keeping 1 minute of timeout to perform this activity")
                    time.sleep(60)
                    user_msg = "[Expectation]:PSR status should be disabled in IGCC for On Battery" \
                               "[CONFIRM]:Enter yes if expectation met, else enter no"
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                        status = False
                    else:
                        logging.info("PSR is disabled in IGCC")
        if not status:
            self.fail("test_step_09 failed")

    ##
    # @brief This step reboots the system
    # @return None
    def test_10_step(self):
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        if reboot_helper.reboot(self, 'test_11_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step checks PSR status
    # @return None
    def test_11_step(self):
        status = True
        logging.info("Successfully booted to Desktop")
        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info("Getting PSR Status via IGCC")
                # TODO: Automate PSR status from IGCC once VSDI-43945 JIRA is fixed
                alert.info("[Expectation]:Open IGCC App (Go to system-> power->power settings) "
                           "Check panel self refresh feature status. PSR status should be disabled in IGCC for On "
                           "Battery. Keeping 1 minute of timeout to perform this activity")
                time.sleep(60)
                user_msg = "[Expectation]:PSR status should be disabled in IGCC for On Battery" \
                           "[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    logging.info("PSR is disabled in IGCC")
        if not status:
            self.fail("test_step_11 failed")

    ##
    # @brief This step enables PSR and HDR
    # @return None
    def test_12_step(self):
        status = True
        alert.info("Enabling PSR in IGCC.\nNo visual artifacts should be seen during PSR toggle")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=True)
                if not psr_status:
                    alert.info("Failed to enable PSR in IGCC")
                    self.fail("Failed to enable PSR in IGCC")
                else:
                    logging.info("Enabled PSR in IGCC")
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

                    user_msg = (f"[Expectation]:No visual artifacts should be seen during PSR enable"
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                        status = False
                    else:
                        logging.info(f"No visual artifacts were seen during PSR enable")

                    if panel.hdr_caps.is_hdr_supported:
                        alert.info("Disabling HDR.\nNo visual artifacts should be seen while disabling HDR")
                        logging.info(f"Panel caps before disabling HDR: {panel}")
                        logging.info(f"Step: Disabling HDR on {panel.port}")
                        if pc_external.enable_disable_hdr([panel.port], False) is False:
                            self.fail(f"Failed to disable HDR on {panel.port}")
                        dut.refresh_panel_caps(adapter)
                        logging.info(f"Panel caps after disabling HDR: {panel}")

                        user_msg = (f"[Expectation]:No visual artifacts should be seen while disabling HDR"
                                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info(f"No visual artifacts were seen while disabling HDR")
                    else:
                        logging.info(f"eDP doesn't support HDR")
        if not status:
            self.fail("test_step_12 failed")

    ##
    # @brief This step plays windowed video with AC
    # @return None
    def test_13_step(self):
        status = True
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

        alert.info("Launching video. Video should get launch in Windowed Mode. No visual artifacts should be seen "
                   "during video playback.")
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, 'ElephantsDream_H264_1920x1080.MP4'), False)
        winkb_helper.press('CTRL+T')  # play in loop
        time.sleep(5)

        user_msg = "[Expectation]:Video should get launched in Windowed Mode." \
                   "No visual artifacts should be seen during video playback." \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Video launched in windowed mode and no visual artifacts were seen during video playback")

        if not status:
            self.fail("test_step_13 failed")

    ##
    # @brief This step enables HDR
    # @return None
    def test_14_step(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                if panel.hdr_caps.is_hdr_supported:
                    logging.info(f"Panel caps before enabling HDR: {panel}")
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"Failed to enable HDR on {panel.port}")
                    dut.refresh_panel_caps(adapter)
                    logging.info(f"Panel caps after enabling HDR: {panel}")
                else:
                    logging.info(f"eDP doesn't support HDR")

    ##
    # @brief This step plays video in Full screen for 1 min
    # @return None
    def test_15_step(self):
        logging.info("Switch VPB to Full Screen Mode")
        media_window_handle = window_helper.get_window('Media Player')
        if media_window_handle is None:
            self.fail("Application Media player is not open")
        media_window_handle.set_foreground()
        winkb_helper.press('F11')
        time.sleep(60)

    ##
    # @brief This step switches to Windowed mode and Disable HDR
    # @return None
    def test_16_step(self):
        status = True
        logging.info("Switching to Windowed mode")
        winkb_helper.press('F11')
        time.sleep(5)

        user_msg = "[Expectation]:Did video switched to windowed mode?" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Successfully switched video to windowed mode")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                if panel.hdr_caps.is_hdr_supported:
                    alert.info("Disabling HDR.\nNo visual artifacts should be seen while disabling HDR")
                    logging.info(f"Panel caps before disabling HDR: {panel}")
                    logging.info(f"Step: Disabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], False) is False:
                        self.fail(f"Failed to disable HDR on {panel.port}")
                    dut.refresh_panel_caps(adapter)
                    logging.info(f"Panel caps after disabling HDR: {panel}")

                    user_msg = (f"[Expectation]:No visual artifacts should be seen while disabling HDR"
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                        status = False
                    else:
                        logging.info(f"No visual artifacts were seen while disabling HDR")
                else:
                    logging.info(f"eDP doesn't support HDR")
        if not status:
            self.fail("test_step_16 failed")

    ##
    # @brief This step toggles HDR 5 times
    # @return None
    def test_17_step(self):
        status = True
        for i in range(5):
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if not panel.is_lfp:
                        continue
                    if panel.hdr_caps.is_hdr_supported:
                        logging.info(f"Toggling HDR for {i + 1} time")
                        alert.info("Enabling HDR.\nNo visual artifacts should be seen while enabling HDR")
                        logging.info(f"Panel caps before enabling HDR: {panel}")
                        logging.info(f"Step: Enabling HDR on {panel.port}")
                        if pc_external.enable_disable_hdr([panel.port], True) is False:
                            self.fail(f"Failed to enable HDR on {panel.port}")
                        dut.refresh_panel_caps(adapter)
                        logging.info(f"Panel caps after enabling HDR: {panel}")

                        alert.info("Disabling HDR.\nNo visual artifacts should be seen while disabling HDR")
                        logging.info(f"Step: Disabling HDR on {panel.port}")
                        if pc_external.enable_disable_hdr([panel.port], False) is False:
                            self.fail(f"Failed to disable HDR on {panel.port}")
                        dut.refresh_panel_caps(adapter)
                        logging.info(f"Panel caps after disabling HDR: {panel}")

                        user_msg = (f"[Expectation]:No visual artifacts should be seen while toggling HDR"
                                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info(f"No visual artifacts were seen while toggling HDR")
                    else:
                        logging.info(f"eDP doesn't support HDR")
        if not status:
            self.fail("test_step_17 failed")

    ##
    # @brief This step switches to Min RR
    # @return None
    def test_18_step(self):
        logging.info("Switching to Min RR")
        alert.info("Switching to Min RR")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                modes = common.get_display_mode(panel.target_id, panel.min_rr, limit=2)
                if len(modes) != 0:
                    if self.__class__.display_config.set_display_mode([modes[-1]]) is False:
                        self.fail(f"FAILED to set display mode for {panel.port}")
                    logging.info(
                        f'Successfully applied display mode with {modes[-1].HzRes}x{modes[-1].VtRes}@'
                        f'{modes[-1].refreshRate}Hz on {panel.port}')

    ##
    # @brief This step toggles HDR 5 times
    # @return None
    def test_19_step(self):
        self.test_17_step()

    ##
    # @brief This step switched to DC mode and Enables HDR
    # @return None
    def test_20_step(self):
        status = True
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

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                if panel.hdr_caps.is_hdr_supported:
                    alert.info("Note: Step to be done by user manually."
                               "\nUnder Windows HD color settings ->Battery options -> select 'Optimize for Image "
                               "quality'."
                               "Keeping timeout of 2min to complete this.")
                    time.sleep(120)

                    alert.info("Enabling HDR.\nNo visual artifacts should be seen while enabling HDR")
                    logging.info(f"Panel caps before enabling HDR: {panel}")
                    logging.info(f"Step: Enabling HDR on {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        logging.info("Closing media player")
                        window_helper.close_media_player()
                        self.fail(f"Failed to enable HDR on {panel.port}")
                    dut.refresh_panel_caps(adapter)
                    logging.info(f"Panel caps after enabling HDR: {panel}")

                    user_msg = (f"[Expectation]:No visual artifacts should be seen while enabling HDR"
                                f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                        status = False
                    else:
                        logging.info(f"No visual artifacts were seen while enabling HDR")
                else:
                    logging.info(f"eDP doesn't support HDR")

        logging.info("Closing media player")
        window_helper.close_media_player()
        if not status:
            self.fail("test_step_20 failed")

    ##
    # @brief This step performs Lid Switch with Do Nothing
    # @return None
    def test_21_step(self):
        status = True
        logging.info("Configuring lid switch close to Do Nothing and closing the lid")
        alert.info("Note: Configure lid switch close->Do Nothing under Control Panel-> Hardware and Sound-> Power "
                   "Options-> System Settings page. Close the lid. While closing the lid, system should NOT be Power "
                   "OFF. Wait for 10sec. "
                   "\nOpen the lid. No visual artifacts should be seen during Lid re-open")
        time.sleep(40)

        user_msg = (f"[Expectation]: While closing the lid, system should NOT be Power OFF."
                    f"\nNo visual artifacts should be seen during Lid re-open"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"Lid close and open performed successfully")

        if not status:
            self.fail("test_step_21 failed")

    ##
    # @brief This step performs Lid switch with Sleep
    # @return None
    def test_22_step(self):
        status = True
        logging.info("Configuring lid switch close to SLEEP and closing the lid")
        alert.info("Note: Configure lid switch close->sleep. Close the lid. While closing the lid, System should go "
                   "to Sleep"
                   "\nWait for 30sec. "
                   "\nOpen the lid. No visual artifacts should be seen during Lid re-open"
                   "\nEnter login credentials")
        time.sleep(100)

        user_msg = (f"[Expectation]: While closing the lid, System should go to Sleep"
                    f"\nNo visual artifacts should be seen during Lid re-open"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"Lid close and open performed successfully")

        winkb_helper.press('WIN+M')
        winkb_helper.press('WIN+D')
        if not status:
            self.fail("test_step_22 failed")

    ##
    # @brief This step keeps desktop IDLE
    # @return None
    def test_23_step(self):
        status = True
        alert.info("Keeping system IDLE for 1min. No flicker/underrun should be seen during IDLE desktop")
        logging.info("Keeping system IDLE for 1min. No flicker/underrun should be seen during IDLE desktop")
        time.sleep(60)

        user_msg = (f"[Expectation]:No visual artifacts should be seen during IDLE desktop"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"No visual artifacts were seen during IDLE desktop")

        if not status:
            self.fail("test_step_23 failed")

    ##
    # @brief This step performs Lid switch with Hibernate
    # @return None
    def test_24_step(self):
        status = True
        logging.info("Configuring lid switch close to Hibernate and closing the lid")
        alert.info("Note: Configure lid switch close->Hibernate. Close the lid. While closing the lid, System should "
                   "go to Hibernate"
                   "\nWait for 30sec. "
                   "\nOpen the lid. Press any key to resume. No visual artifacts should be seen during Lid re-open"
                   "\nEnter login credentials")
        time.sleep(100)

        user_msg = (f"[Expectation]: While closing the lid, System should go to Hibernate"
                    f"\nNo visual artifacts should be seen during Lid re-open"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"Lid close and open performed successfully")

        if not status:
            self.fail("test_step_24 failed")

    ##
    # @brief This step performs Lid switch with external Panel
    # @return None
    def test_25_step(self):
        status = True
        logging.info("Configuring lid switch close to sleep and closing the lid")
        alert.info("Note: Configure lid switch close->sleep")
        time.sleep(30)

        user_msg = (f"[Expectation]: Lid switch close should be configured to sleep"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"Lid switch close was configured to sleep successfully")

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
            status = False
        else:
            logging.info("No TDR/Underrun & flicker was seen during plug")

        alert.info("In following step, user will unplug external panel. No TDR/Underrun & flicker should be observed "
                   "during unplug ")
        result = action.unplug('external')
        if not result:
            self.fail("Failed to unplug external panel")
        user_msg = "[Expectation]:No TDR/Underrun & flicker should be observed during unplug" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False

        else:
            logging.info("No TDR/Underrun & flicker was seen during unplug")

        alert.info("Note: Close the lid. While closing the lid, System should go to sleep"
                   "\nWait for 30sec. "
                   "\nOpen the lid. No visual artifacts should be seen during Lid re-open"
                   "\nEnter login credentials")
        time.sleep(100)

        user_msg = (f"[Expectation]: While closing the lid, System should go to sleep"
                    f"\nNo visual artifacts should be seen during Lid re-open"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(f"Lid close and open performed successfully")

        if not status:
            self.fail("test_step_25 failed")

    ##
    # @brief This step disables PSR2 and restarts driver
    # @return None
    def test_26_step(self):
        status = True
        alert.info("PSR2 will be disabled as requested by test")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info(f"Panel caps before disabling PSR2 : {panel}")
                # Disable complete PSR2 using PSR2Disable
                logging.info("Disabling PSR2 via reg key (PSR2Disable)")
                psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR2 for {panel.port}")

                ret_status, reboot_required = display_essential.restart_gfx_driver()
                if ret_status is False:
                    self.fail(f"FAILED to restart display driver for {adapter.name}")
                user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                           "[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

                logging.info("Getting PSR Status via IGCC")
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

                alert.info("Enables PSR2 regkey as requested by test")
                logging.info(f"Panel caps before enabling PSR2  : {panel}")
                # Re-enable complete PSR2 using PSR2Disable
                logging.info("Enabling PSR2 via reg key (PSR2Disable)")
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr_status is False:
                    self.fail(f"FAILED to enable PSR2 for {panel.port}")

                ret_status, reboot_required = display_essential.restart_gfx_driver()
                if ret_status is False:
                    self.fail(f"FAILED to restart display driver for {adapter.name}")
                user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                           "[CONFIRM]:Enter yes if expectation met, else enter no"
                result = alert.confirm(user_msg)
                if not result:
                    msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                    logging.error(f"User observations: {msg['Message']}")
                    status = False
                else:
                    logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_step_26 failed")

    ##
    # @brief        Function for setting power state and PSR status
    # @param[in]    power_plan - Power scheme to be applied of type PowerScheme
    # @return       None
    def check_psr_in_power_mode(self, power_plan):
        status = True
        logging.info(f"Setting lid switch to default option sleep and Power plan mode to {power_plan.name}")
        alert.info(f"Note: Configure lid switch close->sleep and power plan mode to {power_plan.name}")
        user_msg = (
            f"[Expectation]: Lid switch close should be configured to sleep and power plan mode to {power_plan.name}"
            f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info(
                f"Lid switch close was configured to sleep successfully and power plan mode to {power_plan.name}")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                logging.info("Getting PSR Status via IGCC")
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
        if not status:
            self.fail(f"test_step to set lid switch to do nothing and Power mode to {power_plan.name} failed")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('PsrWithIgccLid'))
    TestEnvironment.cleanup(outcome)
