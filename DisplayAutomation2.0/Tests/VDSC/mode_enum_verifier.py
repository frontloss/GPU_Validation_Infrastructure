#######################################################################################################################
# @file         mode_enum_verifier.py
# @brief        Contains ModeEnumVerifier Class to Verify the Enumerated Modes and To Apply and Verify the Enumerated
#               Modes Along with DSC Verification For Each of the Mode Applied.
#
# @author       Praburaj Krishnan
#######################################################################################################################
import ctypes
import logging
from typing import Dict, Set, List, Optional

from Libs.Core import enum
from Libs.Core.display_config import display_config_enums
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper.control_api_args import ctl_genlock_target_mode_list_t, ctl_display_timing_t
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import DisplayMode, DisplayModeBlock, ColorFormat, bpc_mapping
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey
from Libs.Feature.vdsc.dsc_helper import DSCHelper


##
# @brief        Contains Functions For Verify Enumerated Modes and to Apply Modes and Verify it.
class ModeEnumerationVerifier:
    under_run_status = UnderRunStatus()
    display_configuration = DisplayConfiguration()
    DISPLAY_HARDWARE_INFO = SystemInfo().get_gfx_display_hardwareinfo()

    ##
    # @brief        Exposed API to Verify the Enumerated Modes Against the Golden Modes and Ignore Mode List
    #               That are Defined in the XML.
    # @param[in]    gfx_index: str
    #                   Graphics Index On Which the Display is Plugged.
    # @param[in]   port_name: str
    #                   Contains the Port Name on Which the Display is Plugged.
    # @param[in]   golden_mode_dict: Dict[str, DisplayModeBlock]
    #                   Dictionary Containing Golden Modes That are Parsed From the XML.
    # @param[in]   ignore_mode_dict: Dict[str, DisplayModeBlock]
    #                   Dictionary Containing Modes to be Ignored That are Parsed From the XML.
    # @return       is_success: bool
    #                   Returns True if Os Reported Modes Matches with the Golden Modes and Ignore Modes.
    @classmethod
    def verify_enumerated_modes(cls, gfx_index: str, port_name: str, golden_mode_dict: Dict[str, DisplayModeBlock],
                                ignore_mode_dict: Dict[str, DisplayModeBlock]) -> bool:
        is_success: bool = True
        index = int(gfx_index[-1])
        platform: str = cls.DISPLAY_HARDWARE_INFO[index].DisplayAdapterName

        # Get Display and Adapter Info Using Graphics Index and Port Name.
        display_adapter_info: DisplayAndAdapterInfo = cls.display_configuration.get_display_and_adapter_info_ex(
            port_name, gfx_index)
        if type(display_adapter_info) is list:
            display_adapter_info = display_adapter_info[0]

        # Get Os Reported Modes and Create Set From it.
        supported_mode_dict = {}
        if platform == "ELG":
            logging.info("\tRe-Init Control Library")
            if not control_api_wrapper.configure_control_api(flag=False):
                logging.error("\tFailed to close Control API post driver restart")
                return False
            if not control_api_wrapper.configure_control_api(flag=True):
                logging.error("\tFailed to re-init Control API post driver restart")
                return False
            is_success, ctl_timings_ptr = DisplayConfiguration().get_all_supported_modes_igcl(display_adapter_info)
            if is_success is False:
                logging.error("Failed to get supported modes")
                return is_success

            target_id = display_adapter_info.TargetID
            supported_mode_dict[target_id] = cls.map_igcl_mode_to_os_mode_struct(display_adapter_info, ctl_timings_ptr)
        else:
            supported_mode_dict = cls.display_configuration.get_all_supported_modes([display_adapter_info], False)

        for target_id, supported_mode_list in supported_mode_dict.items():
            logging.debug(f"List of supported modes for Target id: {target_id}")

            for display_mode in supported_mode_list:
                logging.debug(f'HRes:{display_mode.HzRes} VRes:{display_mode.VtRes} RR:{display_mode.refreshRate}'
                              f' BPP:{display_mode.BPP}')

        os_reported_modes: Set[DisplayMode] = set(supported_mode_dict[display_adapter_info.TargetID])

        # Get Display Mode From Display Mode Block Structure and Create Set From it.
        # all_supported_modes_igcl() fails to return scaled modes - HSD-16022562362
        # Hence ignore scaled modes from the golden_modes set[DisplayMode].
        # WA: In case of Scalar modes, skip verify_enum_modes -> apply the scaled modes -> do scalar verifications.
        golden_modes: Set[DisplayMode] = set(
            display_mode_block.display_mode for display_mode_block in golden_mode_dict.values() if display_mode_block.display_mode.scaling == 64)

        # Contains Supported Modes but Reported as Unsupported by the Driver to the OS.
        supported_modes: Set[DisplayMode] = golden_modes.difference(os_reported_modes)

        if len(supported_modes) > 0:
            is_success &= False
            logging.error("[Driver Issue] - Below Modes Are Not Enumerated by the Driver for " + platform)
            gdhm.report_driver_bug_di("Driver didn't enumerate supported Modes")
            cls.log_display_modes("ERROR", display_modes=supported_modes)

        ignore_mode_set = set(display_mode_block.display_mode for display_mode_block in ignore_mode_dict.values())

        # Contains Unsupported Modes Reported as Supported by the Driver to the OS.
        unsupported_modes = ignore_mode_set.intersection(os_reported_modes)

        if len(unsupported_modes) > 0:
            is_success &= False
            logging.error("[Driver Issue] - Below Modes Should not be Enumerated by the Driver for " + platform)
            gdhm.report_driver_bug_di(f"Driver reported modes({unsupported_modes}) as supported are unsupported")
            cls.log_display_modes("ERROR", display_modes=unsupported_modes)

        return is_success

    ##
    # @brief        Exposed API to Apply and Verify All the Modes That are Defined in the XML.
    # @param[in]    gfx_index: str
    #                   Graphics Index On Which the Display is Plugged. Currently Unused but Will be Used Once
    #                   Set Display Mode and Verify DSC Supports MA Scenarios.
    # @param[in]   port: str
    #                   Contains the Port Name on Which the Display is Plugged.
    # @param[in]   apply_mode_list: List[DisplayModeBlock]
    #                   Dictionary Containing Set of Modes That Needs to be Applied, Which are Parsed From the XML.
    # @return       is_success: bool
    #                   Returns True if All Modes Defined the XML are Applied Successfully, False Otherwise.
    @classmethod
    def apply_mode_and_verify(cls, gfx_index: str, port: str, apply_mode_list: List[DisplayModeBlock]) -> bool:
        f_status = True
        reset_bpc = False
        index = int(gfx_index[-1])
        platform: str = cls.DISPLAY_HARDWARE_INFO[index].DisplayAdapterName

        # Iterate Through Each of the Mode in Apply Mode Dict, Apply the Mode and Verify it.
        for display_mode_block in apply_mode_list:
            mode_to_apply: DisplayMode = display_mode_block.display_mode
            cls.log_display_modes("APPLYING:", {mode_to_apply})

            # 0x1 - Represents 8 BPC, if anything else we need to set bpc using reg key
            bpc = display_mode_block.display_mode_control_flags.data.bpc
            if bpc != 0x1:
                bpc = bpc_mapping[bpc]
                f_status = DSCHelper.set_bpc_in_registry(gfx_index, bpc)
                reset_bpc = True

            display_adapter_info = cls.display_configuration.get_display_and_adapter_info_ex(port, gfx_index)

            if platform == "ELG":
                logging.info("\tRe-Init Control Library")
                is_success, supported_modes = DisplayConfiguration().get_all_supported_modes_igcl(display_adapter_info)
                if is_success is False:
                    logging.error(f"Could not get supported modes from IGCL for display at {gfx_index}: {port}")
                    return is_success
                igcl_mode = cls.find_match_for_os_mode_in_igcl_modes(supported_modes, mode_to_apply)
                if igcl_mode is None:
                    logging.error("Could not find matching mode in the IGCL modes for the mode in the xml")
                    return False
                is_success = cls.display_configuration.set_higher_pixel_clock_mode(display_adapter_info, igcl_mode)
            else:
                is_success = cls.display_configuration.set_display_mode([mode_to_apply])

            is_under_run_observed = cls.under_run_status.verify_underrun()
            f_status = f_status and is_success

            if is_under_run_observed is True:
                logging.error("Under-run Observed After Set Display Mode.")

            if is_success is True:
                color_format: ColorFormat = ColorFormat(display_mode_block.display_mode_control_flags.data.color_format)
                test_data = {TestDataKey.COLOR_FORMAT: color_format}

                is_dsc_capable = not (bool(display_mode_block.display_mode_control_flags.data.is_dsc_not_capable))
                if is_dsc_capable is True:
                    verification_status = dsc_verifier.verify_dsc_programming(gfx_index, port, test_data)
                    if verification_status is True:
                        logging.info(f"DSC Verification Successful for {port} Display on {gfx_index}")
                    else:
                        logging.error(f"DSC Verification Failed for {port} Display on {gfx_index}")
                        f_status = False
                else:
                    is_fec_capable = not (bool(display_mode_block.display_mode_control_flags.data.is_fec_not_capable))

                    is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
                    is_fec_enabled = DSCHelper.get_fec_ready_status(display_adapter_info)

                    # Timing can be driven with FEC enabled but FEC is not enabled or for some reason DSC is enabled, we
                    # fail the test case
                    if is_fec_capable is True and (is_fec_enabled is False or is_dsc_enabled is True) is True:
                        logging.error(f"DSC/FEC should not be enabled for Display on {port} on {gfx_index}")
                        f_status = False

                    # Timing cannot be driven with FEC enabled but FEC is enabled or for some reason DSC is enabled, we
                    # fail the test case
                    if is_fec_capable is False and (is_dsc_enabled or is_fec_enabled) is True:
                        logging.error(f"DSC/FEC should not be enabled for Display on {port} on {gfx_index}")
                        f_status = False

            # Disable the registry.
            if reset_bpc is True:
                reset_bpc = False
                f_status = f_status and DSCHelper.enable_disable_bpc_registry(gfx_index, enable_bpc=0)

        return f_status

    ##
    # @brief        Logs the DisplayMode Structure Values.
    # @param[in]   status: str
    #                   Status will tell whether the mode should be printed with ERROR or INFO or DEBUG.
    # @param[in]   display_modes: Set[DisplayMode]
    #                   Set of Modes For Which the Values Has to be Logged.
    # @return       None
    @classmethod
    def log_display_modes(cls, status: str, display_modes: Set[DisplayMode]) -> None:
        enumerated_displays = cls.display_configuration.get_enumerated_display_info()
        if len(display_modes) == 0:
            logging.error('Display Mode List is Empty')
            gdhm.report_bug(
                title="[Interfaces][DP_DSC] Display Mode Link cannot be empty",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        for display_mode in display_modes:
            logging.info("{} - {}".format(status, display_mode.to_string(enumerated_displays)))

    ##
    # @brief        Helper function to map the genlock mode to the display mode structure
    # @param[in]    display_adapter_info: DisplayAndAdapterInfo
    #                   Display and adapter details of the display for which supported modes has to be mapped.
    # @param[in]    modes: ctypes.POINTER(ctl_genlock_target_mode_list_t)
    #                   Ctype pointer to an array of type ctl_display_timing_t which has supported modes.
    # @return       display_modes_list: Optional[List[DisplayMode]]
    #                   Contains the converted modes from IGCL API
    @classmethod
    def map_igcl_mode_to_os_mode_struct(cls, display_adapter_info: DisplayAndAdapterInfo,
                                        modes: ctypes.POINTER(ctl_genlock_target_mode_list_t)):
        display_modes_list: Optional[List[DisplayMode]] = []

        for mode_index in range(modes.NumModes):
            display_mode = DisplayMode()
            display_mode.status = display_config_enums.enum.DISPLAY_CONFIG_SUCCESS
            display_mode.targetId = display_adapter_info.TargetID
            display_mode.HzRes = modes.pTargetModes[mode_index].HActive
            display_mode.VtRes = modes.pTargetModes[mode_index].VActive
            display_mode.rotation = enum.ROTATE_0
            display_mode.refreshRate = int(modes.pTargetModes[mode_index].RefreshRate)
            display_mode.BPP = enum.PIXELFORMAT_32BPP
            display_mode.scanlineOrdering = enum.PROGRESSIVE
            display_mode.scaling = enum.MDS
            display_modes_list.append(display_mode)

        return display_modes_list

    ##
    # @brief        Helper function to get the matching mode for the provided os mode struct of type DisplayMode using
    #               hActive, vActive and rr.
    # @param[in]    igcl_modes: ctypes.POINTER(ctl_genlock_target_mode_list_t)
    #                   Contains the list of timings supported for a particular display fetched from IGCL API.
    # @param[in]    mode: DisplayMode
    #                   Mode for which corresponding IGCL mode has to be obtained.
    # @return       Optional[ctl_display_timing_t]
    #                   Returns the matching IGCL mode if found else None.
    @classmethod
    def find_match_for_os_mode_in_igcl_modes(cls, igcl_modes: ctypes.POINTER(ctl_genlock_target_mode_list_t),
                                             mode: DisplayMode) -> Optional[ctl_display_timing_t]:
        for mode_index in range(igcl_modes.NumModes):
            igcl_mode = igcl_modes.pTargetModes[mode_index]
            if (igcl_mode.HActive == mode.HzRes and igcl_mode.VActive == mode.VtRes and
                    int(igcl_mode.RefreshRate) == mode.refreshRate):
                return igcl_mode

        gdhm.report_driver_bug_os("Could not find matching mode in the IGCL mode list for the provided os mode")
        logging.error("Could not find matching mode in the IGCL mode list for the provided os mode")
        return None
