#######################################################################################################################
# @file         test_escape_set1.py
# @brief        Combination of tests to verify all Yangra based escape calls under set-1
# @details      Test Scenario:
#               1. Pre-requisite - Plug the VRR-supported eDP display.
#               2. Plug 2 displays - HDMI_B with YCbCr support (for color escapes) and any external DP panel.
#               3. Verifies all the required Escape calls.
#               Supported command-lines:
#               1. test_escape_set1.py -gfx_0 -EDP_A SINK_EDP095 -HDMI_B SINK_HDM026 -DP_D SINK_DPS043
#               2. test_escape_set1.py -gfx_0 -EDP_A SINK_EDP096 -HDMI_B SINK_HDM026 -DP_F SINK_DPS043
#               3. test_escape_set1.py -gfx_0 -EDP_A SINK_EDP040 -HDMI_B SINK_HDM026 -DP_C SINK_DPS043
#               Note: Test supports only command-lines with Panel Sink Index passed for all displays
#
# @author       Kiran Kumar Lakshmanan, Chandrakanth Pabolu,
#######################################################################################################################
import logging
import os
import random
import unittest
from typing import Dict, List, Tuple

from Libs.Core import display_utility, registry_access, enum, system_utility
from Libs.Core import driver_escape, reboot_helper
from Libs.Core.display_config.display_config_enums import DriverType
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.logger import html
from Libs.Core.sw_sim import dpcd_container
from Libs.Core.test_env import test_environment, test_context
from Libs.Core.wrapper import driver_escape_args as args
from Tests.ULT.DriverEscape.test_escape_base import DriverEscapeBase


##
# @brief        DriverEscapeSet1 Class
class DriverEscapeSet1(DriverEscapeBase):

    ##
    # @brief    Test: Validate Miscellaneous System Info
    # @return   None
    @html.step("Validate Miscellaneous System Info")
    def test_00_validate_misc_info(self) -> None:
        # Get Escape Call
        status, misc_sys_info = driver_escape.get_misc_system_info(gfx_index=self.gfx_index)
        if not status:
            self.fail("[MiscSysInfo] Get Misc System Info Escape call Failed")
        logging.info("[MiscSysInfo] Get Misc System Info Escape call Passed")

        # Verification condition: Compare Device ID returned from GfxDriver and AdapterInfo
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[self.gfx_index]
        expected_device_id = hex(int(adapter_info.deviceID, 16)).upper()
        actual_device_id = hex(misc_sys_info.platformInfo.deviceID).upper()
        if expected_device_id != actual_device_id:
            self.fail(f"[MiscSysInfo][Verify] Device ID Expected {expected_device_id}, Actual {actual_device_id}")
        logging.info(f"[MiscSysInfo][Verify] Device ID returned matches AdapterInfo Device ID: {actual_device_id}")

    ##
    # @brief    Test: Validate EDID Data
    # @return   None
    @html.step("Validate Get EDID Data")
    def test_02_validate_edid_data(self) -> None:
        edid_failure_count: Dict[str, int] = {}
        # Example: {'DP_A': -1, 'HDMI_B': 10, 'DP_D': 0}
        # Reference: -1 = Port is not available in port_list, 0 = no read failure, >0 = EDID read failure count

        for ports in self.port_list:
            for gfx_index, port in ports.items():
                edid_failure_count[port] = -1
                logging.info(f"[Edid] Fetching EDID for {port} on {gfx_index}!!")
                display_and_adapter_info_list = self.config.get_display_and_adapter_info(gfx_index, port)
                for display_and_adapter_info in display_and_adapter_info_list:
                    logging.info(f"{display_and_adapter_info.__str__()}")
                    edid_failure_count[port] = 0
                    # Header-only validation Approach
                    status, edid_data, block_count = driver_escape.get_edid_data(display_and_adapter_info)
                    if not status:
                        self.fail("[Edid] Get EDID Escape call Failed")
                    logging.info("[Edid] Get EDID Escape call Passed")
                    logging.debug(f"[Edid] #Blocks: {block_count} Edid Data: {edid_data}")

                    # Actual EDID File validation Approach
                    if port not in self.panel_dict.keys():
                        logging.error(f"Requested Port {port} is not available in Panel Dictionary {self.panel_dict}")
                        edid_failure_count[port] = 1
                        continue
                    status, expected_edid_data = DriverEscapeBase.get_edid_data_from_file(self.panel_dict[port]['edid'])
                    if not status:
                        logging.error(f"[Edid] Failed to Get EDID from file path - {self.panel_dict[port]['edid']}")
                    logging.debug(f"[Edid] Expected EDID data - {expected_edid_data}")
                    # Verification condition: Compare Expected EDID from File and Actual EDID from Driver Escape
                    if bool(expected_edid_data) and edid_data[:len(expected_edid_data)] == expected_edid_data:
                        logging.info(f"[Edid][Verify] Successfully Verified EDID data for panel in {port}!")
                    else:
                        fail_count = 0
                        if not bool(expected_edid_data):
                            logging.error("[Edid][Verify] EDID File parser returned empty list.")
                        else:
                            mismatch_edid_list = [(index, e1, e2) for index, (e1, e2) in
                                                  enumerate(zip(expected_edid_data, edid_data)) if e1 != e2]
                            logging.error(f"[Edid][Verify] Mismatch EDID data list [(index, panel data, escape data)]: "
                                          f"{mismatch_edid_list}")
                            fail_count = len(mismatch_edid_list)
                        edid_failure_count[port] += fail_count
                        logging.error("[Edid][Verify] Failed to Verify EDID data")

        self.assertTrue(not any(edid_failure_count.values()), f"EDID Verification Failed {edid_failure_count}")
        logging.info("[Edid][Verify] Successfully Verified EDID values for all Panels")

    ##
    # @brief    Test: Validate YCbCr
    # @details  Pre-requisite: supported only on HDMI panel with YCbCr support
    # @return   None
    @html.step("Validate YCbCr")
    def test_05_09_validate_ycbcr(self) -> None:
        SUPPORTED_PLATFORMS = ["TGL", "RKL", "DG1", "ADLS"]
        for port in self.hdmi_list:
            display_and_adapter_info_list = self.config.get_display_and_adapter_info(self.gfx_index, port)
            for display_and_adapter_info in display_and_adapter_info_list:
                logging.info(f"{display_and_adapter_info.__str__()}")
                # Get YCbCr support
                platform_name = display_and_adapter_info.adapterInfo.get_platform_info().PlatformName.upper()
                is_ycbcr = driver_escape.is_ycbcr_supported(display_and_adapter_info)
                if platform_name in SUPPORTED_PLATFORMS and is_ycbcr is not True:
                        self.fail(f"[YCbCrSupport] YCbCr is not supported on {hex(display_and_adapter_info.TargetID)}")
                # Verification condition: YCbCr should be supported on HDMI panel connected
                logging.info(f"[YCbCrSupport] YCbCr is supported on {hex(display_and_adapter_info.TargetID)}")

                # Configure YCbCr
                status = driver_escape.configure_ycbcr(display_and_adapter_info, True)
                if not status:
                    self.fail("[ConfigureYCbCr] Configure YCbCr Escape call Failed")
                # Verification condition: YCbCr should be configurable on HDMI panel connected
                logging.info("[ConfigureYCbCr] Configure YCbCr Escape call Passed")
                # Todo: Check if needs to be configured to False on exit
                _ = driver_escape.configure_ycbcr(display_and_adapter_info, False)
                logging.info("[ConfigureYCbCr] Reset Configure YCbCr Escape call - Completed")

    ##
    # @brief    Test: Validate Custom Scaling
    # @details  Pre-requisite: Escape call not supported on LFPs/Collage/Tiled and displays with pipe out format YUV420
    # @return   None
    @html.step("Validate Custom Scaling")
    def test_06_validate_custom_scaling(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        # Note: Custom Scaling value can be in range - 20 < (X, Y) < 100
        test_scaling_x = test_scaling_y = 80
        for ports in self.port_list:
            for gfx_index, port in ports.items():
                display_and_adapter_info_list = self.config.get_display_and_adapter_info(gfx_index, port)
                # Not supported for LFPs/Tiled/Collage and displays with pipe out format YUV420
                if display_utility.get_vbt_panel_type(port, gfx_index) == display_utility.VbtPanelType.LFP_DP or \
                        'HDMI' in port:
                    continue
                for display_and_adapter_info in display_and_adapter_info_list:
                    logging.info(f"{display_and_adapter_info.__str__()}")
                    # Get Scaling
                    scaling_args = args.CustomScalingArgs(100, 100, display_and_adapter_info.TargetID,
                                                          args.CustomScalingOperation.GET_STATE.value)
                    status, scaling_args = driver_escape.get_set_custom_scaling(display_and_adapter_info, scaling_args)
                    (default_x, default_y) = (scaling_args.customScalingX, scaling_args.customScalingY) \
                        if (scaling_args.customScalingX != 0 and scaling_args.customScalingY != 0) else (100, 100)
                    if not status:
                        self.fail("[CustomScaling][Get] Custom Scaling Escape call Failed")
                    logging.info(f"[CustomScaling][Get] Custom Scaling Escape call Passed. "
                                 f"Current Scaling: {scaling_args.customScalingX}x{scaling_args.customScalingY}")

                    # Verification condition: Check Scaling is supported on current panel
                    if scaling_args.scalingSupported is False:
                        self.fail(f"[CustomScaling][Verify] Custom Scaling is not Supported in {scaling_args.targetId}")

                    # Set Scaling
                    scaling_args = args.CustomScalingArgs(test_scaling_x, test_scaling_x,
                                                          display_and_adapter_info.TargetID,
                                                          args.CustomScalingOperation.SET_STATE.value)
                    status, scaling_args = driver_escape.get_set_custom_scaling(display_and_adapter_info, scaling_args)
                    if not status:
                        self.fail("[CustomScaling][Set] Custom Scaling Escape call Failed")
                    logging.info(f"[CustomScaling][Set] Custom Scaling Escape call Passed. "
                                 f"Applied scaling: {scaling_args.customScalingX}x{scaling_args.customScalingY}")

                    # Verify Applied Scaling
                    scaling_args1 = args.CustomScalingArgs(100, 100, display_and_adapter_info.TargetID,
                                                           args.CustomScalingOperation.GET_STATE.value)
                    status, scaling_args1 = driver_escape.get_set_custom_scaling(display_and_adapter_info,
                                                                                 scaling_args1)

                    # Verification condition: Check if applied scaling is reflected
                    if scaling_args1.customScalingX != test_scaling_x or scaling_args1.customScalingY != test_scaling_y:
                        self.fail(f"[CustomScaling][Verify] Failed to Apply Custom Scaling. (X, Y) Expected  "
                                  f"({test_scaling_x}, {test_scaling_y}) Actual ({scaling_args1.customScalingX}, "
                                  f"{scaling_args1.customScalingY})")

                    # Reset Scaling to default values
                    scaling_args1.customScalingX, scaling_args1.customScalingY = default_x, default_y
                    _, _ = driver_escape.get_set_custom_scaling(display_and_adapter_info, scaling_args1)
                    logging.info("[CustomScaling] Reset Custom Scaling - Completed")

    ##
    # @brief    Test: Validate Apply CSC
    # @return   None
    @html.step("Validate Apply CSC")
    def test_07_validate_apply_csc(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        logging.warning("Skipping Apply CSC test")

    ##
    # @brief    Test: Validate Read DPCD data
    # @return   None
    @html.step("Validate Native DPCD Read")
    def test_10_validate_read_dpcd(self) -> None:
        dpcd_failure_count: Dict[str, int] = {}
        # Example: {'DP_A': -1, 'DP_B': 10, 'DP_D': 0}
        # Reference: -1 = Port is not available in panel_dict, 0 = no read failure, >0 = DPCD read failure count
        for port in self.dp_list:
            dpcd_failure_count[port] = -1
            display_and_adapter_info_list = self.config.get_display_and_adapter_info(self.gfx_index, port)
            for display_and_adapter_info in display_and_adapter_info_list:
                logging.info(f"{display_and_adapter_info.__str__()}")
                if port not in self.panel_dict.keys():
                    logging.error(f"Requested Port {port} is not available in Panel Props Dictionary {self.panel_dict}")
                    dpcd_failure_count[port] = 1
                    continue
                expected_dpcd_data = dpcd_container._parse_dpcd_txt_file(self.panel_dict[port]['dpcd'])
                dpcd_failure_count[port] = 0
                for dpcd_data in expected_dpcd_data:
                    # Note: Expected Failure in below offset. Skipping for this offset to avoid Test Failure.
                    if dpcd_data.offset == 0x116:
                        continue
                    status, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info, dpcd_data.offset)
                    if not status:
                        self.fail(f"[DpcdRead] Read DPCD Escape call Failed for {dpcd_data.offset}")

                    # Verification condition: Compare Expected DPCD from File and Actual DPCD value from Driver Escape
                    if dpcd_val[0] != dpcd_data.mask:
                        dpcd_failure_count[port] += 1
                        logging.error(f"[DpcdRead][Verify] {hex(dpcd_data.offset).upper()}: "
                                      f"Expected {dpcd_data.mask} Actual {dpcd_val[0]}")

        self.assertTrue(not any(dpcd_failure_count.values()), f"DPCD Verification Failed {dpcd_failure_count}")
        logging.info("[DpcdRead][Verify] Successfully Verified DPCD values for DP Panels")

    ##
    # @brief    Test: Validate Write DPCD data
    # @return   None
    @html.step("Validate Native DPCD Write")
    def test_10_validate_write_dpcd(self) -> None:
        # ToDo: Implement in phase 2
        logging.warning("Skipping DPCD Write")

    ##
    # @brief    Test: ALS Aggressiveness Level Override
    # @return   None
    @html.step("Validate ALS Aggressiveness Level Override")
    def test_12_als_aggressiveness_level_override(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        lux, lux_operation, aggressiveness, aggressiveness_operation = 2000, True, 0, True
        for port in self.dp_list:
            # Works only for eDP panel
            if display_utility.get_vbt_panel_type(port, self.gfx_index) != display_utility.VbtPanelType.LFP_DP:
                continue

            display_and_adapter_info_list = self.config.get_display_and_adapter_info(self.gfx_index, port)
            for display_and_adapter_info in display_and_adapter_info_list:
                logging.info(f"{display_and_adapter_info.__str__()}")
                status = driver_escape.als_aggressiveness_level_override(display_and_adapter_info, lux, lux_operation,
                                                                         aggressiveness, aggressiveness_operation)
                if not status:
                    self.fail("[AlsAggressiveness] Als Aggressiveness Level Override Escape call Failed")
                logging.info("[AlsAggressiveness] Als Aggressiveness Level Override Escape call Passed")
                # Verification condition: Lux and Aggressiveness values should be verified from ETL

    ##
    # @brief    Test: Validate Hw3DLut
    # @details  Pre-requisite: bin files should be present under SHAREDBINARY folder
    # @return   None
    @html.step("Validate HW3DLut")
    def test_13_validate_hw_3dlut(self) -> None:
        bin_file_list: List[str] = ["CustomLUT_no_R.bin", "CustomLUT_no_G.bin", "CustomLUT_no_B.bin"]
        default_bin_file: str = "CustomLUT_default.bin"
        # Chooses any one of available bin files
        bin_file_path: str = "Color\\Hw3DLUT\\CustomLUT\\" + random.choice(bin_file_list)
        default_bin_file_path: str = "Color\\Hw3DLUT\\CustomLUT\\" + default_bin_file
        bin_file: str = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)
        default_bin: str = os.path.join(test_context.SHARED_BINARY_FOLDER, default_bin_file_path)
        if not os.path.exists(bin_file):
            self.fail(f"File doesn't exist - {bin_file_path}!")
        expected_depth = 17

        for port in self.dp_list:
            # Skip for non-EDP displays
            if display_utility.get_vbt_panel_type(port, self.gfx_index) != display_utility.VbtPanelType.LFP_DP:
                continue

            display_and_adapter_info_list = self.config.get_display_and_adapter_info(self.gfx_index, port)
            for display_and_adapter_info in display_and_adapter_info_list:
                logging.info(f"{display_and_adapter_info.__str__()}")
                # Get Escape call
                dpp_hw_lut_info = args.DppHwLutInfo(display_and_adapter_info.TargetID,
                                                    args.DppHwLutOperation.UNKNOWN.value, 0)
                status, dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(self.gfx_index, dpp_hw_lut_info)
                if not status:
                    self.fail(f"[Hw3DLut][Get] Hw3DLut Escape call Failed for {display_and_adapter_info.TargetID}")
                logging.info(f"[Hw3DLut][Get] Hw3DLut Escape call Passed")
                logging.info(f"[Hw3DLut][Verify] Hw3DLut depth: {dpp_hw_lut_info.depth}")

                # Set Escape call
                dpp_hw_lut_info.opType = args.DppHwLutOperation.APPLY_LUT.value
                if not dpp_hw_lut_info.convert_lut_data(bin_file):
                    self.fail(f"[Hw3DLut][Set] Failed to Convert Lut Data {bin_file}")
                if not driver_escape.set_dpp_hw_lut(self.gfx_index, dpp_hw_lut_info):
                    self.fail(f"[Hw3DLut][Set] Hw3DLut Escape call Failed for {display_and_adapter_info.TargetID}")
                logging.info(f"[Hw3DLut][Set] Hw3DLut Escape call Passed for {display_and_adapter_info.TargetID}")

                # Get Escape call
                dpp_hw_lut_info1 = args.DppHwLutInfo(display_and_adapter_info.TargetID,
                                                     args.DppHwLutOperation.UNKNOWN.value, 0)
                status, dpp_hw_lut_info1 = driver_escape.get_dpp_hw_lut(self.gfx_index, dpp_hw_lut_info1)

                # Verification condition: Compare Expected depth and Actual depth after applying via Driver Escape
                if dpp_hw_lut_info1.depth != expected_depth:
                    self.fail(f"[Verify][Set] Depth Expected : {expected_depth} Actual {dpp_hw_lut_info1.depth}")
                logging.info(f"[Verify][Set] Hw3DLut depth : {dpp_hw_lut_info1.depth}")

                # Reset Default LUT
                dpp_hw_lut_info1 = args.DppHwLutInfo(display_and_adapter_info.TargetID,
                                                     args.DppHwLutOperation.APPLY_LUT.value, expected_depth)
                if not dpp_hw_lut_info1.convert_lut_data(default_bin):
                    self.fail(f"[Hw3DLut] Failed to Convert Default Lut Data {default_bin}")
                _ = driver_escape.set_dpp_hw_lut(self.gfx_index, dpp_hw_lut_info1)
                logging.info("[Hw3DLut] Reset Default Lut - Completed")

    ##
    # @brief    Test: Validate Quantization Range
    # @return   None
    @html.step("Validate Quantization Range")
    def test_14_validate_quantization_range(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        for port in self.hdmi_list:
            display_and_adapter_info_list = self.config.get_display_and_adapter_info(self.gfx_index, port)
            for display_and_adapter_info in display_and_adapter_info_list:
                logging.info(f"{display_and_adapter_info.__str__()}")
                # Get Escape call
                avi_info = args.AviInfoFrameArgs()
                avi_info.TargetID = display_and_adapter_info.TargetID
                avi_info.Operation = args.AviInfoOperation.GET.value
                status, avi_info = driver_escape.get_set_quantisation_range(display_and_adapter_info.TargetID, avi_info)
                if not status:
                    self.fail("[QuantizationRange][Get] AVI Info Frame Escape call Failed")
                logging.info("[QuantizationRange][Get] AVI Info Frame Escape call Passed")

                # Set Escape call
                avi_info.Operation = args.AviInfoOperation.SET.value
                avi_info.AVIInfoFrame.QuantRange = 1
                # Todo: Update Enum; Currently enums are defined within Feature. Need to check for moving to args
                status, avi_info = driver_escape.get_set_quantisation_range(display_and_adapter_info.TargetID, avi_info)
                if not status:
                    self.fail("[QuantizationRange][Set] AVI Info Frame Escape call Failed")
                logging.info("[QuantizationRange][Set] AVI Info Frame Escape call Passed")

                # Verification condition: Compare Expected range and Actual range after applying via Driver Escape
                avi_info1 = args.AviInfoFrameArgs()
                avi_info1.TargetID = display_and_adapter_info.TargetID
                avi_info1.Operation = args.AviInfoOperation.GET.value
                _, avi_info1 = driver_escape.get_set_quantisation_range(display_and_adapter_info.TargetID, avi_info1)
                if avi_info1.AVIInfoFrame.QuantRange != avi_info.AVIInfoFrame.QuantRange:
                    self.fail(f"[QuantizationRange][Verify] Failed to set quantization range for "
                              f"{display_and_adapter_info.TargetID}")
                logging.info("[QuantizationRange][Verify] Successfully Verified Quantization Range")

    ##
    # @brief    Test: Validate Variable Refresh Rate
    # @return   None
    @html.step("Validate Variable Refresh Rate")
    def test_15_validate_vrr(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        vrr_operations: List[args.VrrOperation] = [args.VrrOperation.DISABLE.value, args.VrrOperation.ENABLE.value]
        # Get Escape call
        vrr_args = args.VrrArgs()
        vrr_args.operation = args.VrrOperation.GET_INFO.value
        status, vrr_args = driver_escape.get_set_vrr(self.gfx_index, vrr_args)
        if not status:
            self.fail("[Vrr][Get] Vrr Escape call Failed")
        logging.info(f"[Vrr][Get] Vrr Escape call Passed. VRR status={vrr_args.vrrEnabled}")

        # Step is required to identify current VRR Enable status for given adapter
        # If: Enable -> Verify -> Disable
        # Else: Disable -> Verify -> Enable
        if vrr_args.vrrEnabled is False:
            vrr_operations.reverse()

        # Set Escape call
        vrr_args.operation = vrr_operations[0]
        status, vrr_args = driver_escape.get_set_vrr(self.gfx_index, vrr_args)
        if not status:
            self.fail(f"[Vrr][Set] Vrr Escape call Failed: {args.VrrOperation(vrr_args.operation).name}")
        logging.info(f"[Vrr][Set] Vrr Escape call Passed: {args.VrrOperation(vrr_args.operation).name}")

        # Get Escape call
        vrr_args = args.VrrArgs()
        vrr_args.operation = args.VrrOperation.GET_INFO.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(self.gfx_index, vrr_args)
        if not vrr_flag:
            self.fail(f"[Vrr][Get] Get Vrr Escape call Failed: {args.VrrOperation(vrr_args.operation).name}")

        # Verification condition: Check if VRR is enabled/disabled based on Set operation
        if (vrr_args.operation == args.VrrOperation.ENABLE.value and vrr_args.vrrEnabled is False) or \
                (vrr_args.operation == args.VrrOperation.DISABLE.value and vrr_args.vrrEnabled is True):
            self.fail(f"[Vrr][Verify] Failed to Enable VRR: {args.VrrOperation(vrr_args.operation).name}")
        logging.info("[Vrr][Verify] Vrr Enabled Successfully")

        # Reset to default VRR Enable status
        vrr_args.operation = vrr_operations[1]
        _, _ = driver_escape.get_set_vrr(self.gfx_index, vrr_args)
        logging.info("[Vrr] Reset Default VRR setting - Completed")

    ##
    # @brief    Test: Validate Custom Mode
    # @return   None
    @html.step("Validate Add Custom Mode")
    def test_16_validate_custom_mode(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        enum_displays = self.display_config_.get_enumerated_display_info()
        logging.info(f"Enumerated Displays: {enum_displays}")

        resolution: Tuple[int, int] = (1000, 800)
        display_and_adapter_info_list = []
        # Store initial mode for displays to restore state
        initial_mode_dict: Dict[str, Dict[str, List[DisplayMode]]] = {}
        custom_mode_dict: Dict[str, Dict[str, List[DisplayMode]]] = {}

        self.apply_display_config_all_displays(enum.EXTENDED)
        for ports in self.port_list:
            for gfx_index, port in ports.items():
                if gfx_index not in custom_mode_dict.keys():
                    custom_mode_dict[gfx_index] = {}
                if gfx_index not in initial_mode_dict.keys():
                    initial_mode_dict[gfx_index] = {}
                display_and_adapter_info_list = self.config.get_display_and_adapter_info(gfx_index, port)
                if len(display_and_adapter_info_list) == 0:
                    self.fail(f"[CustomMode] Failed to fetch DisplayAndAdapterInfo for {port} on {gfx_index}")

                display_and_adapter_info = display_and_adapter_info_list[0]
                logging.debug(f"{display_and_adapter_info.__str__()}")
                logging.info(f"[CustomMode] Adding mode - {resolution[0]} && {resolution[1]} for {gfx_index}:{port}")
                status = driver_escape.add_custom_mode(display_and_adapter_info, resolution[0], resolution[1])
                if not status:
                    self.fail("[CustomMode] Add Custom Mode Escape call Failed")
                logging.info(f"[CustomMode] Add Custom Mode Escape call Passed for {port} on {gfx_index}")

                initial_mode_dict[gfx_index][port] = [self.display_config_.get_current_mode(display_and_adapter_info)]
                mode = DisplayMode()
                mode.targetId = display_and_adapter_info.TargetID
                mode.HzRes = resolution[0]
                mode.VtRes = resolution[1]
                mode.refreshRate = 60
                mode.BPP = enum.PIXELFORMAT_32BPP  # Assuming RGB888
                mode.rotation = enum.ROTATE_0
                mode.scanlineOrdering = enum.PROGRESSIVE
                mode.scaling = enum.MAR
                custom_mode_dict[gfx_index][port] = [mode]

        status: bool = True  # Verification flag
        failed_displays: List[Tuple[str, str]] = []  # display list for which escape call failed

        # Verification condition: Check if Expected Resolution from Tuple can be applied to connected panels
        for gfx_index, display in custom_mode_dict.items():
            for port, mode_list in display.items():
                if self.display_config_.set_display_mode(mode_list, enumerated_displays=enum_displays) is not True:
                    logging.error(f"[CustomMode][Verify] Failed to set custom mode {resolution} for {gfx_index}:{port}")
                    status = False
                    failed_displays.append((gfx_index, port))
                else:
                    logging.info(f"[CustomMode][Verify] Applied custom mode {resolution[0]}x{resolution[1]} for "
                                 f"{gfx_index}:{port}")

        # Restore initial mode for each display
        for gfx_index, display in initial_mode_dict.items():
            for port, mode_list in display.items():
                if self.display_config_.set_display_mode(mode_list, enumerated_displays=enum_displays) is not True:
                    logging.error(f"[CustomMode] Failed to restore initial mode "
                                  f"{mode_list[0].to_string(enum_displays)} for {gfx_index}:{port}")

        assert status, f"[CustomMode][Verify] Failed to verify Add Custom Mode for {failed_displays}"
        logging.info("[CustomMode][Verify] Successfully Verified Custom Mode for all Panels")

    ##
    # @brief    Test: Validate NN Scaling
    # @return   None
    @html.step("Validate Nearest-Neighbour Scaling")
    def test_20_validate_nn_scaling(self) -> None:
        if self.driver_branch != DriverType.YANGRA or\
                system_utility.SystemUtility().get_execution_environment_type() not in ['POST_SI_ENV']:
            logging.info("Skipping this test, since it is supported only on Post-Si with Yangra Driver")
            return

        for ports in self.port_list:
            for gfx_index, port in ports.items():
                if display_utility.get_vbt_panel_type(port, gfx_index) != display_utility.VbtPanelType.LFP_DP:
                    continue

                display_and_adapter_info_list = self.config.get_display_and_adapter_info(gfx_index, port)
                for display_and_adapter_info in display_and_adapter_info_list:
                    logging.info(f"{display_and_adapter_info.__str__()}")
                    # Get NN Scaling
                    nn_args = args.NNArgs()
                    nn_args.opCode = args.ScalingOperation.GET_NN_SCALING_STATE.value
                    status, nn_args = driver_escape.get_set_nn_scaling(display_and_adapter_info, nn_args)
                    if not status:
                        self.fail("[NnScaling][Get] NN Scaling Escape call Failed")
                    logging.info("[NnScaling][Get] NN Scaling Escape call Passed")

                    # Verification condition: Check for NN/IS Scaling support
                    if nn_args.NNScalingSupport.isNNScalingSupport is False or \
                            nn_args.NNScalingSupport.forceIntegerScalingSupport is False:
                        self.fail("[NnScaling][Verify] NN/IS scaling is not supported")
                    logging.info("[NnScaling][Verify] NN/IS scaling is supported")

                    # Enable NN scaling
                    nn_args.NNScalingState = args.NNScalingState.NN_SCALING_ENABLE.value
                    nn_args.opCode = args.ScalingOperation.SET_NN_SCALING_STATE.value
                    status, nn_args = driver_escape.get_set_nn_scaling(display_and_adapter_info, nn_args)
                    if not status:
                        self.fail("[NnScaling][Set] NN Scaling Escape call Failed")
                    logging.info("[NnScaling][Set] NN Scaling Escape call Passed")

                    # Verification condition: Check if Registry value for NNScalingState is set to NNScalingState value
                    # 0 = Disable NNScaling, 1 = Set NN scaling, 2 = Force IS scaling
                    ss_reg_args = registry_access.StateSeparationRegArgs(display_and_adapter_info.adapterInfo.gfxIndex)
                    reg_val, reg_type = registry_access.read(args=ss_reg_args, reg_name="NNScalingState")
                    if registry_access.RegDataType.BINARY is registry_access.RegDataType(reg_type):
                        reg_val = int.from_bytes(reg_val, byteorder="little")
                    if nn_args.NNScalingState != reg_val:
                        self.fail("[NnScaling][Verify] Failed to Set NN Scaling")
                    logging.info("[NnScaling][Verify] Successfully Set NN Scaling")

                    # Reset NN scaling
                    nn_args.NNScalingState = args.NNScalingState.NN_SCALING_DISABLE.value
                    nn_args.opCode = args.ScalingOperation.SET_NN_SCALING_STATE.value
                    _, _ = driver_escape.get_set_nn_scaling(display_and_adapter_info, nn_args)
                    logging.info("[NnScaling] Reset Default Scaling - Completed")

    ##
    # @brief    Test: Validate Query Writeback Device
    # @return   None
    @html.step("Validate Query Writeback Device")
    def test_24_validate_query_wb(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        logging.warning("Skipping Query WB test")
        # Todo: Unplug External Displays before this test

    ##
    # @brief    Test: Validate Plug and Unplug Writeback Device
    # @return   None
    @html.step("Validate Plug-Unplug Writeback Device")
    def test_25_validate_plug_unplug_wb(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        logging.warning("Skipping Plug/Unplug WB test")
        # Todo: Unplug External Displays before this test

    ##
    # @brief    Test: Validate Dump Writeback Buffer
    # @return   None
    @html.step("Validate Dump Writeback Buffer")
    def test_26_validate_dump_wb_buffer(self) -> None:
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        logging.warning("Skipping Dump WB test")
        # Todo: Unplug External Displays before this test


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    result = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite("DriverEscapeSet1"))
    test_environment.TestEnvironment.cleanup(result)
