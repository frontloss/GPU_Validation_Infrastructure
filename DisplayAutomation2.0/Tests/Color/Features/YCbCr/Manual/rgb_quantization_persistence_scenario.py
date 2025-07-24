########################################################################################################################
# @file         rgb_quantization_persistence_scenario.py
# @brief        Manual Test to verify IGCC Override Feature
# Manual TI     https://gta.intel.com/procedures/#/procedures/TI-3554667/
# TI name:      RGB quantization + Persistence Scenario - 2 Displays (Non-HDR eDP + 4K HDR EFP)
# @author       Golwala, Ami
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import enum, reboot_helper, display_utility, display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower
from Libs.Core.test_env import context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.Color.Common import csc_utility, color_etl_utility
from Tests.Color.Common.color_enums import RgbQuantizationRange
from Tests.Color.Common.color_escapes import get_bpc_encoding, set_bpc_encoding, configure_aviinfo
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Verification import gen_verify_pipe
from Tests.PowerCons.Modules import common


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class RgbQuantizationPersistenceScenario(unittest.TestCase):
    display_pwr = DisplayPower()
    display_config = DisplayConfiguration()
    context_args = context.Context()
    is_12_bpc_supported = False

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief This step sets display config and enables HDR
    # @return None
    def test_01_step(self):
        user_msg = "[Expectation]: Boot with all the displays planned" \
                   "\n[CONFIRM]: Enter Yes if expectations met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            alert.info("Fail: Please run test with displays planned in the grid")
            self.fail("Fail: Please run test with displays planned in the grid")
        else:
            logging.info("Test started with all planned panels connected")

        alert.info("Applying extended mode")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        enum_port_list = []
        if enumerated_display.Count >= 2:
            for index in range(0, enumerated_display.Count):
                enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            status = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED, enum_port_list)
            if not status:
                alert.info("Applying Extended mode failed")
                self.fail("Applying Extended mode failed")
            alert.info("Successfully applied extended mode")
        else:
            alert.info("Fail: Enumerated display count is less than 2. Minimum 2 displays required to apply Extended "
                       "mode")
            self.fail("Enumerated display count is less than 2. Minimum 2 displays required to apply Extended mode")

        alert.info("Enabling Simulated Battery")
        logging.info("Enabling Simulated Battery")
        assert self.__class__.display_pwr.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("PASS: Enabled Simulated Battery successfully")

        # Checking current power line status and if it is not AC, then changing it to AC
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.AC:
            alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
            self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")

            user_msg = "[Expectation]:Power line should switch to AC mode" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                self.fail(f"User observations: {msg['Message']}")
            else:
                logging.info("Powerline changed to AC")
        else:
            alert.info("Powerline is in AC mode")
            logging.info("Powerline is in AC mode")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    if default_bpc == "BPC8" and default_encoding in ["YCBCR444", "YCBCR422", "YCBCR420"]:
                        alert.info("Failing the test as for HDR, we shouldn't expect YUV with BPC8 for external "
                                   "displays. Current mode of EFP is YUV with BPC8")
                        self.fail("For HDR, we shouldn't expect YUV with BPC8 for external displays. "
                                  "Current mode of EFP is YUV with BPC8")

        alert.info("Enabling HDR on EFP. No Corruption, Screen Blankout should be visible.")
        logging.info("Enabling HDR on EFP")
        # Enable HDR on EFP
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            alert.info("Failed to enable HDR on EFP")
            logging.error("Enabling HDR on EFP failed")
            alert.info("Step to be performed by user manually. \n Enable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        alert.info("Successfully enabled HDR on EFP")
        logging.info("Successfully enabled HDR on EFP")

        user_msg = "[Expectation]:No Corruption, Screen Blankout should be visible while enabling HDR" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No Corruption, Screen Blankout was visible while enabling HDR")

        supported_bpc_list = []
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    for index in range(len(combo_bpc_encoding)):
                        bpc = str(combo_bpc_encoding[index][0])
                        if bpc not in supported_bpc_list:
                            supported_bpc_list.append(bpc)

            if "BPC12" in supported_bpc_list:
                self.__class__.is_12_bpc_supported = True

    ##
    # @brief This step Unplugs-Plugs panel
    # @return None
    def test_02_step(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()

        user_msg = ("Note: Step to be performed by user manually."
                    "\n Unplug external panel. Plug back again, without any delay."
                    "\n[CONFIRM]: Press enter to continue with the test\n")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Unplug-plug of external panel is done successfully")

        updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if updated_enumerated_display.Count != enumerated_display.Count:
            alert.info(f"Post unplug plug of external panel, enumerated display count is not matching. "
                       f"Expected: {enumerated_display.Count}, Actual: {updated_enumerated_display.Count}")
            self.fail(f"Post unplug plug of external panel, enumerated display count is not matching. "
                      f"Expected: {enumerated_display.Count}, Actual: {updated_enumerated_display.Count}")

        user_msg = "[Expectation]:No artifacts or TDR, BSOD should be observed" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No artifacts or TDR, BSOD was observed")

    ##
    # @brief This step switched range
    # @return None
    def test_03_step(self):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    port_name = panel.connector_port_type
                    display_type = port_name.split('_')[0]  # DP/HDMI/...
                    if display_type == "HDMI":
                        alert.info(f"Setting quantization range to Limited range")
                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             RgbQuantizationRange.LIMITED.value):
                            alert.info(f"Successfully set quantization range to Limited range")
                            logging.info(f"Successfully set quantization range to Limited range")
                        else:
                            alert.info(f"Fail: Failed to set quantization range to Limited range")
                            self.fail(f"Failed to set quantization range to Limited range")

                        alert.info(f"Setting quantization range to Full range")
                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             RgbQuantizationRange.FULL.value):
                            alert.info(f"Successfully set quantization range to Full range")
                            logging.info(f"Successfully set quantization range to Full range")
                        else:
                            alert.info(f"Fail: Failed to set quantization range to Full range")
                            self.fail(f"Failed to set quantization range to Full range")

                        user_msg = "[Expectation]:No Screen Blankout should be visible on all screens" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                        else:
                            logging.info("No Screen Blankout was visible on all screens")

                    else:
                        alert.info("Test is not planned with HDMI display. Skipping to change Quantization range")
                        logging.info("Test is not planned with HDMI display. Skipping to change Quantization range")

    ##
    # @brief This step updates color depth to 12BPC
    # @return None
    def test_04_step(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                connector_port = str(
                    CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType))
                is_lfp_dp = (display_utility.get_vbt_panel_type(connector_port,
                                                                'gfx_0') == display_utility.VbtPanelType.LFP_DP)
                if not is_lfp_dp:
                    display_and_adapter_info = (self.__class__.display_config.
                                                get_display_and_adapter_info_ex(connector_port))
                    alert.info("Applying Native mode on external display")
                    logging.info("Applying native mode on external display")
                    native_mode = self.__class__.display_config.get_native_mode(display_and_adapter_info.TargetID)
                    current_mode = self.__class__.display_config.get_current_mode(display_and_adapter_info.TargetID)
                    current_mode.HzRes = native_mode.hActive
                    current_mode.VtRes = native_mode.vActive
                    current_mode.refreshRate = native_mode.refreshRate
                    if self.__class__.display_config.set_mode(current_mode):
                        alert.info("Successfully set native mode for external display")
                        logging.info("Successfully set native mode for external display")
                    else:
                        alert.info("Fail: Failed to set native mode for external display")
                        self.fail("Failed to set native mode for external display")
        else:
            alert.info("Fail: Enumerated display count is 0")
            self.fail("Enumerated display count is 0")

        if self.__class__.is_12_bpc_supported:
            for gfx_index, adapter in self.__class__.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and not panel.is_lfp:
                        status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                            panel.display_and_adapterInfo, adapter.platform_type)
                        alert.info("Setting 12BPC on external panel")
                        if not set_bpc_encoding(panel.display_and_adapterInfo, "BPC12",
                                                default_encoding, adapter.platform_type, panel.is_lfp):
                            alert.info("Fail: Failed to set the override bpc and encoding")
                            self.fail("Fail: Failed to set the override bpc and encoding")
                        else:
                            logging.info("Successfully switched to 12BPC for external panel")
                            self.check_quantization_persistence(RgbQuantizationRange.FULL)
        else:
            logging.info("Panel doesn't support 12BPC")

    ##
    # @brief This step updates color depth to 8BPC
    # @return None
    def test_05_step(self):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    alert.info("Setting 8BPC on external panel")
                    if not set_bpc_encoding(panel.display_and_adapterInfo, "BPC8",
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info("Fail: Failed to set the override bpc and encoding")
                        self.fail("Fail: Failed to set the override bpc and encoding")
                    else:
                        alert.info("Successfully switched to 8BPC for external panel")
                        # With persistence scenario quantization range should be "Full Range"
                        self.check_quantization_persistence(RgbQuantizationRange.FULL)

    ##
    # @brief This step disables HDR
    # @return None
    def test_06_step(self):
        alert.info("Disabling HDR on external panel")
        logging.info("Disabling HDR on external panel")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            alert.info("Fail: Disabling HDR on EFP failed")
            logging.error("Disabling HDR on EFP failed")
            alert.info("Step to be performed by user manually. \n Disable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        alert.info("Disabling HDR on EFP failed")
        logging.info("Disabling HDR on EFP failed")

    ##
    # @brief This step changes the range to LIMITED
    # @return None
    def test_07_step(self):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    port_name = panel.connector_port_type
                    display_type = port_name.split('_')[0]  # DP/HDMI/...
                    if display_type == "HDMI":
                        # Quantization range before switch should be Full range
                        self.check_quantization_persistence(RgbQuantizationRange.FULL)

                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             RgbQuantizationRange.LIMITED.value):
                            alert.info(f"Successfully set quantization range to Limited range")
                            logging.info(f"Successfully set quantization range to Limited range")
                        else:
                            alert.info(f"Fail: Failed to set quantization range to Limited range")
                            self.fail(f"Failed to set quantization range to Limited range")
                    else:
                        alert.info("Test is not planned with HDMI display. Skipping to change Quantization range")
                        logging.info("Test is not planned with HDMI display. Skipping to change Quantization range")

    ##
    # @brief This step enables HDR on display2
    # @return None
    def test_08_step(self):
        alert.info("Enabling HDR on EFP. No Corruption, Screen Blankout should be visible.")
        logging.info("Enabling HDR on EFP")
        # Enable HDR on EFP
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            alert.info("Failed to enable HDR on EFP")
            logging.error("Enabling HDR on EFP failed")
            alert.info("Step to be performed by user manually. \n Enable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        alert.info("Successfully enabled HDR on EFP")
        logging.info("Successfully enabled HDR on EFP")

    ##
    # @brief This step switches range to FULL and LIMITED
    # @return None
    def test_09_step(self):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    port_name = panel.connector_port_type
                    display_type = port_name.split('_')[0]  # DP/HDMI/...
                    if display_type == "HDMI":
                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             RgbQuantizationRange.FULL.value):
                            alert.info(f"Successfully set quantization range to full range")
                            logging.info(f"Successfully set quantization range to full range")
                        else:
                            alert.info(f"Fail: Failed to set quantization range to full range")
                            self.fail(f"Failed to set quantization range to full range")

                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             RgbQuantizationRange.LIMITED.value):
                            alert.info(f"Successfully set quantization range to limited range")
                            logging.info(f"Successfully set quantization range to limited range")
                        else:
                            alert.info(f"Fail: Failed to set quantization range to limited range")
                            self.fail(f"Failed to set quantization range to limited range")

                        user_msg = "[Expectation]:No Screen Blankout should be visible on all screens" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                        else:
                            logging.info("No Screen Blankout was visible on all screens")

                    else:
                        alert.info("Test is not planned with HDMI display. Skipping to change Quantization range")
                        logging.info("Test is not planned with HDMI display. Skipping to change Quantization range")

    ##
    # @brief This step switches color depth
    # @return None
    def test_10_step(self):
        self.test_04_step()

        self.check_quantization_persistence(RgbQuantizationRange.LIMITED)

    ##
    # @brief This step Switches Range and resolution
    # @return None
    def test_11_step(self):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for panel in adapter.panels.values():
                if panel.is_active and not panel.is_lfp:
                    port_name = panel.connector_port_type
                    display_type = port_name.split('_')[0]  # DP/HDMI/...
                    if display_type == "HDMI":
                        mode = common.get_display_mode(panel.target_id, refresh_rate=None, limit=1)
                        if mode.HzRes == 3840:
                            alert.info("Applying 4k mode with highest RR")
                            logging.info(
                                f"Applying display mode {mode.HzRes}x{mode.VtRes}"
                                f"@{mode.refreshRate}Hz on {panel.connector_port_type}")
                            if self.__class__.display_config.set_display_mode([mode], False) is False:
                                alert.info("Failed to set display mode with Maximum RR")
                                self.fail("Failed to set display mode with Maximum RR")

                            # Quantization range should be Limited range
                            self.check_quantization_persistence(RgbQuantizationRange.LIMITED)

                            status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                                panel.display_and_adapterInfo, adapter.platform_type)
                            if default_bpc != "BPC12":
                                alert.info(f"Fail: Persistence of BPC is not maintained, expected BPC is BPC12, "
                                           f"current BPC is {default_bpc}")
                                self.fail(f"Persistence of BPC is not maintained, expected BPC is BPC12, "
                                          f"current BPC is {default_bpc}")
                            logging.info("Persistence of BPC is maintained")
                        else:
                            alert.info("Fail: Panel doesn't support 4k mode")
                            self.fail("Fail: Panel doesn't support 4k mode")

    ##
    # @brief This step performs S4
    # @return None
    def test_12_step(self):
        alert.info("Performing power event S4. No TDR/Artifacts should be observed")
        logging.info("Performing power event S4")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 10) is False:
            self.fail(f'Failed to invoke power event S4')
        logging.info("Successfully performed power event S4")

        self.check_quantization_persistence(RgbQuantizationRange.LIMITED)

    ##
    # @brief This step performs reboot
    # @return None
    def test_13_step(self):
        logging.info("Rebooting the system")
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        if reboot_helper.reboot(self, 'test_14_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step verifies quantization post reboot
    # @return None
    def test_14_step(self):
        logging.info("Successfully applied power event S5 state")
        user_msg = ("[Expectation]: No artifacts should be observed over display or resume back from power events "
                    "during boot process and post boot"
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No artifacts observed during reboot")

            self.check_quantization_persistence(RgbQuantizationRange.LIMITED)

    ##
    # @brief        This method checks the persistence of quantization range
    # @param[in]    connector_port: Connected Port
    # @param[in]    display_and_adapterInfo: display_and_adapterInfo - Target ID and Complete Adapter ID details
    # @param[in]    expected_quant_range: expected quant range of RgbQuantizationRange
    # @return       None
    def check_quantization_persistence(self, expected_quant_range):
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    port_name = panel.connector_port_type
                    display_type = port_name.split('_')[0]  # DP/HDMI/...
                    plane_id = color_etl_utility.get_plane_id(pipe=panel.pipe, gfx_index=gfx_index)
                    pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(adapter.platform, gfx_index)
                    if display_type == "HDMI":
                        output_range = csc_utility.get_output_range(gfx_index, adapter.platform, plane_id,
                                                                    panel.pipe, panel.transcoder,
                                                                    pipe_verifier.mmio_interface)
                        if output_range == RgbQuantizationRange(expected_quant_range).value:
                            logging.info(
                                f"Persistence of quantization range is met. Current range is {RgbQuantizationRange(output_range).name}")
                        else:
                            logging.error(
                                f"Persistence of quantization range is met. Current range is {RgbQuantizationRange(output_range).name}, expected is {RgbQuantizationRange(expected_quant_range).name}")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('RgbQuantizationPersistenceScenario'))
    TestEnvironment.cleanup(outcome)
