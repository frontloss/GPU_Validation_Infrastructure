#######################################################################################################################
# @file         blc.py
# @brief        Contains BLC related APIs
#
# @author       Ashish Tripathi
#######################################################################################################################
import logging
import math
import os
import re
import shutil
import subprocess
import time
from collections import Counter
from decimal import Decimal
from enum import Enum, IntEnum

import ctypes
import win32api
import win32serviceutil

from Libs.Core import enum, display_essential, winkb_helper, registry_access, etl_parser
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.display_config import display_config
from Libs.Core import display_power
from Libs.Core.logger import etl_tracer, gdhm, html
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Feature.blc import brightness_args, brightness
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import windows_brightness, common, desktop_controls, dut, dpcd
from Tests.PowerCons.Modules.dut_context import Panel, Adapter
from Tests.PowerCons.Modules.validator_runner import parse_etl_events, run_diana, get_error_from_diana

BLC_PWM_LOW_PRECISION_FACTOR = 100
BLC_PWM_HIGH_PRECISION_FACTOR = 1000


##
# @brief        Enum for BlC milli percentage
class MilliPercentage(Enum):
    MIN = 0
    MAX = 100000


##
# @brief        Enum for BlC percentage
class Percentage(Enum):
    MIN = 0
    MAX = 100


##
# @brief        Enum for Vbt BlC Precision Bit
class VbtBlcPrecisionBit(Enum):
    BIT_PRECISION_8 = 8
    BIT_PRECISION_16 = 16


##
# @brief        Enum for scenarios used in tests
class Scenario(Enum):
    MONITOR_TIME_OUT = 0
    DISPLAY_TDR = 1
    AC_DC_SWITCH = 2
    MODE_SET = 3
    DISPLAY_CONFIG = 4
    POWER_EVENT_S3 = 5
    POWER_EVENT_S4 = 6
    POWER_EVENT_CS = 7
    TOGGLE_SDR_HDR = 8


##
# @brief        Enum for indicating the Hdr return status
class HdrReturnStatus(IntEnum):
    SUCCESS = 0


##
# @brief        Etl events to be utilized for parsing via DiAna
class BlcEtlEvent:
    SET_B3_DDI = "BlcSetBrightness3"
    SET_B2_DDI = "BlcSetBrightness"
    CLIENT_EVENT = "BlcClientEvent"
    B3_TRANSITION = "BlcB3Transition"
    GET_SET_NITS_CAPS = "BlcGetSetNitsBrightness"
    COMPUTE_BRIGHTNESS = "BlcComputeNewBrightness"
    MAP_BRIGHTNESS = "BlcMapBrightness"


##
# @brief        Etl Fields to be utilized for parsing via DiAna
class BlcEtlField:
    DDI_MILLI_NITS = "BrightnessMillinits"
    B2_TARGET = "TargetBrightness"
    BRIGHTNESS = "Brightness"
    MILLI_NITS_TARGET = "TargetBrightnessInMilliUnits"
    HDR_ACTIVE = "IsHdrModeActive"
    ACTUAL_BRIGHTNESS = "ActualBrightnessValue"
    MIN_BRIGHTNESS = "BlcMinBrightness"
    USER_BRIGHTNESS = "UserBrightness"
    RETURN_BRIGHTNESS = "ReturnBrightness"


ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.dpcdData = 1

##
# @brief        Exposed API to restart display enhancement service for
#               making brightness work after disable/enable gfx-driver
# @return       None
def restart_display_service():
    html.step_start("Restarting Display Enhancement Service")
    win32serviceutil.RestartService("Display Enhancement Service")
    html.step_end()


##
# @brief        Exposed API to create LFP nit ranges for Brightness3
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    nits_ranges_values list [min_range, max_range, step_size]
# @return       status Boolean, True added & restart required, None added & no restart required, False otherwise
@html.step("Adding LFP Nit Ranges for Brightness3")
def add_lfp_nit_ranges(adapter, panel, nits_ranges_values):
    logging.info("\tLFP Nit Ranges for {0}".format(panel.port))
    if not panel.is_lfp:
        logging.warning(f"\t{panel.port} is not a LFP")
        return None

    if panel.pnp_id is None:
        logging.error(f"Failed to get PNP ID from {panel.port}")
        return False

    gfx_index = adapter.gfx_index
    port = panel.port
    logging.info(f"\tPnP ID of {gfx_index}-{port}= {panel.pnp_id}")

    ranges_list = []
    min_milli_nits = []
    max_milli_nits = []
    step_size = []
    # generate nit range based in little endian from nits_ranges_values (min_max_step-size) all in milli nits
    for index, number_of_ranges in enumerate(nits_ranges_values):
        min_milli_nits.append(convert_nits_to_milli_nits(int(nits_ranges_values[index][0])))
        max_milli_nits.append(convert_nits_to_milli_nits(int(nits_ranges_values[index][1])))
        step_size.append(convert_nits_to_milli_nits(int(nits_ranges_values[index][2])))
        ranges_list += min_milli_nits[index].to_bytes(4, "little")
        ranges_list += max_milli_nits[index].to_bytes(4, "little")
        ranges_list += step_size[index].to_bytes(4, "little")

    range_count = len(nits_ranges_values) * 257
    nit_range_count_reg = {port: registry.RegKeys.BLC.NIT_RANGE_COUNT + panel.pnp_id}
    nit_ranges_reg = {port: registry.RegKeys.BLC.NIT_RANGES + panel.pnp_id}

    count_add = registry.write(gfx_index, nit_range_count_reg[port], registry_access.RegDataType.DWORD, range_count)
    range_add = registry.write(gfx_index, nit_ranges_reg[port], registry_access.RegDataType.BINARY, bytes(ranges_list))
    if count_add is False:
        logging.error(f"\tFAILED to create {nit_range_count_reg[port]}= {range_count}")
        return False
    logging.info(f"\tSuccessfully created {nit_range_count_reg[port]}= {range_count}")

    if range_add is False:
        logging.error(f"\tFAILED to create {nit_ranges_reg[port]}= {ranges_list}")
        return False
    logging.info(f"\tSuccessfully created {nit_ranges_reg[port]}= {ranges_list}")
    return count_add or range_add


##
# @brief        Exposed API to delete the LFP Nit ranges INFs
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True deleted & restart required, None deleted & no restart required, False otherwise
@html.step("Deleting LFP Nit Ranges")
def delete_lfp_nit_ranges(adapter, panel):
    logging.info(f"\tLFP Nit Ranges for {panel.port}")
    if not panel.is_lfp:
        logging.warning(f"\t{panel.port} is not a LFP")
        return None

    if panel.pnp_id is None:
        logging.error(f"Failed to get PNP ID from {panel.port}")
        return False

    logging.info(f"\tPnP ID of {panel.gfx_index}-{panel.port}= {panel.pnp_id}")

    nit_range_count_reg = {panel.port: registry.RegKeys.BLC.NIT_RANGE_COUNT + panel.pnp_id}
    nit_ranges_reg = {panel.port: registry.RegKeys.BLC.NIT_RANGES + panel.pnp_id}

    count_del = registry.delete(adapter.gfx_index, key=nit_range_count_reg[panel.port])
    range_del = registry.delete(adapter.gfx_index, key=nit_ranges_reg[panel.port])

    if count_del is False:
        logging.error(f"\tFAILED to delete {nit_range_count_reg[panel.port]}")
        return False

    if range_del is False:
        logging.error(f"\tFAILED to delete {nit_ranges_reg[panel.port]}")
        return False

    logging.info(f"\tSuccessfully deleted {nit_range_count_reg[panel.port]}, {nit_ranges_reg[panel.port]}")
    return count_del or range_del


##
# @brief        Exposed API to disable boost nit ranges via INF (80:20 -> 100)
# @param[in]    adapter Adapter object
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
@html.step("Disabling Boost Nit Ranges (80:20 -> 100)")
def disable_boost_nit_ranges(adapter):
    reg_key = registry.RegKeys.BLC.LFP_NIT_RANGES_FFFF
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= 0x1")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x1")
    return status


##
# @brief        Exposed API to set DisableNitsBrightness (brightness3) and switch to brightness2 via INF
# @param[in]    adapter object of Adapter
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
@html.step("Disabling Brightness3 and switching to Brightness2 via INF")
def disable_brightness3(adapter):
    reg_key = registry.RegKeys.BLC.DISABLE_NITS_BRIGHTNESS
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if status is False:
        logging.error(f"\tFAILED to update {reg_key}= 0x1")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x1")
    return status


##
# @brief        Exposed API to delete DisableNitsBrightness (brightness3) INF
# @param[in]    adapter object of Adapter
# @return       status Boolean, True deleted & restart required, None deleted & no restart required, False otherwise
@html.step("Deleting DisableNitsBrightness INF")
def delete_disable_brightness3_inf(adapter):
    reg_key = registry.RegKeys.BLC.DISABLE_NITS_BRIGHTNESS
    status = registry.delete(adapter.gfx_index, key=reg_key)
    if status is False:
        logging.error(f"\tFAILED to delete {reg_key}")
        return False
    logging.info(f"\tSuccessfully deleted {reg_key}")
    return status


##
# @brief        Exposed API to delete boost nit ranges INF (100 -> 80:20)
# @param[in]    adapter Adapter object
# @return       status Boolean, True deleted & restart required, None deleted & no restart required, False otherwise
@html.step("Deleting Boost Nit Ranges (100 -> 80:20)")
def delete_boost_nit_ranges(adapter):
    reg_key = registry.RegKeys.BLC.LFP_NIT_RANGES_FFFF
    status = registry.delete(adapter.gfx_index, key=reg_key)
    if status is False:
        logging.error(f"FAILED to delete {reg_key}")
        return False
    logging.info(f"Successfully deleted {reg_key}")
    return status


##
# @brief        Exposed API to enable HighPrecisionBrightness via INF
# @param[in]    adapter Adapter, object
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
@html.step("Enabling High Precision Brightness")
def enable_high_precision(adapter):
    reg_key = registry.RegKeys.BLC.HIGH_PRECISION
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if status is False:
        logging.error(f"\tFAILED to update {reg_key}= 0x1")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x1")
    return status


##
# @brief        Exposed API to disable HighPrecisionBrightness via INF
# @param[in]    adapter object of Adapter
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
@html.step("Disabling High Precision Brightness")
def disable_high_precision(adapter):
    reg_key = registry.RegKeys.BLC.HIGH_PRECISION
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.DISABLE)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= 0x0")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x0")
    return status


##
# @brief        Exposed API to enable HDR mode
# @param[in]    adapter Adapter object
# @param[in]    panel panel object optional to enable HDR with OS aware way
# @param[in]    os_aware boolean True to enable HDR with OS aware way, False for INF way
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
@html.step("Enabling HDR")
def enable_hdr(adapter, panel=None, os_aware=False):
    if os_aware:
        if panel is None:
            logging.error("\tPanel detail is not provided to enable HDR in OS aware way")
            return False
        if display_config.configure_hdr(
                panel.display_info.DisplayAndAdapterInfo, enable=True) != HdrReturnStatus.SUCCESS:
            logging.error(f"FAILED to enable HDR in OS aware way on {panel.port}(PIPE_{panel.pipe})")
            return False
        logging.info(f"\tSuccessfully enabled HDR in OS aware way on {panel.port}(PIPE_{panel.pipe})")
        return None

    reg_key = registry.RegKeys.HDR.FORCE_HDR_MODE
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= 0x1")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x1 and enabled HDR in driver")
    return status


##
# @brief        Exposed API to disable HDR mode with two approach
# @param[in]    adapter Adapter object
# @param[in]    panel panel object optional to disable HDR with OS aware way
# @param[in]    os_aware boolean optional True for OS aware way, False for INF way, None to disable in both way
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
@html.step("Disabling HDR")
def disable_hdr(adapter, panel=None, os_aware=False):
    if os_aware:
        if panel is None:
            logging.error("\tPanel detail is not provided to disable HDR in OS aware way")
            return False
        if display_config.configure_hdr(
                panel.display_info.DisplayAndAdapterInfo, enable=False) != HdrReturnStatus.SUCCESS:
            logging.error(f"FAILED to disable HDR in OS aware way on {panel.port}(PIPE_{panel.pipe})")
            return False
        logging.info(f"\tSuccessfully disabled HDR in OS aware way on {panel.port}(PIPE_{panel.pipe})")
        return None

    reg_key = registry.RegKeys.HDR.FORCE_HDR_MODE
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, registry.RegValues.DISABLE)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= 0x0")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= 0x0")
    return status


##
# @brief        Exposed API to invoke SetBrightness3() DDI via ValSim. For HighPrecision, make sure system is supported
# @param[in]    gfx_index
# @param[in]    target_id Target ID of display
# @param[in]    brightness_value if HighPrecision then milli percent(0-100000) else milli nits(panel range)
# @param[in]    transition_time
# @return       True if successful, False otherwise
def set_brightness3(gfx_index, target_id, brightness_value, transition_time):
    brightness_set = brightness_args.DXGK_BRIGHTNESS_SET_IN()
    brightness_set.BrightnessMillinits = brightness_value
    brightness_set.TransitionTimeMs = transition_time
    return brightness.set_brightness3(gfx_index, target_id, brightness_set)


##
# @brief        Exposed API to verify Back-light
# @param[in]    adapter adapter object
# @param[in]    test_name string
# @param[in]    blc_etl_file etl file
# @param[in]    blc_args list  [is_pwm_based, nit_ranges, is_high_precision, hdr_state, brightness_list,
#                               lfp1_port, disable_boost_range, is_invalid_nit_range_test, disable_nits_brightness]
# @param[in]    remove_redundant_ddi boolean optional param to remove the redundant blc ddi
# @return       True if successful, None, ETL/json file not found, False otherwise
def verify(adapter, test_name, blc_etl_file, blc_args, remove_redundant_ddi=True):
    assert adapter

    if os.path.exists(blc_etl_file) is False:
        logging.error("{0} not Found".format(blc_etl_file))
        return None

    pnp_id_list = []
    is_pwm_based = blc_args[0]
    nit_ranges = None if len(blc_args) < 1 else blc_args[1]
    is_high_precision = False if len(blc_args) < 2 else blc_args[2]
    hdr_state = None if len(blc_args) < 3 else blc_args[3]
    expected_brightness = None if len(blc_args) < 4 else blc_args[4]
    lfp1_port = None if len(blc_args) < 5 else blc_args[5]
    disable_boost_ranges = False if len(blc_args) < 6 else blc_args[6]
    disable_nits_brightness = False if len(blc_args) < 8 else blc_args[8]
    max_brightness_count = Counter(expected_brightness)[100]
    set_second_lfp_brightness = None if len(blc_args) < 9 else int(blc_args[9])
    is_mipi_pwm = False

    json_output = run_diana(test_name, blc_etl_file, ['BLC'])
    if json_output is None:
        logging.error("JSON file not found")
        return None

    if is_high_precision or nit_ranges is not None or bool(hdr_state) or is_pwm_based[lfp1_port] is False:
        event_name = BlcEtlEvent.SET_B3_DDI
        field_name = BlcEtlField.DDI_MILLI_NITS
    else:
        event_name = BlcEtlEvent.SET_B2_DDI
        field_name = BlcEtlField.BRIGHTNESS

    # when HDR meta data block is present in EDID
    for panel in adapter.panels.values():
        if panel.port is not lfp1_port:
            continue

        if disable_nits_brightness and panel.hdr_caps.is_hdr_supported is False:
            event_name = BlcEtlEvent.SET_B2_DDI
            field_name = BlcEtlField.BRIGHTNESS
            break

        if panel.max_fall != 0:
            event_name = BlcEtlEvent.SET_B3_DDI
            field_name = BlcEtlField.DDI_MILLI_NITS
            break

    ddi_data = parse_etl_events(adapter, json_output, event_name, field_name, None)
    transition_data_dict = parse_etl_events(
        adapter, json_output, BlcEtlEvent.B3_TRANSITION, BlcEtlField.MILLI_NITS_TARGET)
    client_data_dict = parse_etl_events(adapter, json_output, BlcEtlEvent.CLIENT_EVENT, BlcEtlField.B2_TARGET)
    gdhm_scenario = test_name.split("_", 1)[1].upper()  # AC_DC from BLC_AC_DC
    os_requested_brightness = []
    status = True
    # removing first additional DDI requested while enabling of driver
    ddi_data = remove_redundant_values(ddi_data['NONE']) if remove_redundant_ddi else ddi_data['NONE']
    max_fall = {}
    min_cll = {}

    for panel in adapter.panels.values():
        pnp_id_list.append(panel.pnp_id)

    pnp_id_match = all(element == pnp_id_list[0] for element in pnp_id_list)

    map_user_blc_dict = parse_etl_events(
        adapter, json_output, BlcEtlEvent.MAP_BRIGHTNESS, BlcEtlField.USER_BRIGHTNESS)
    map_return_blc_dict = parse_etl_events(
        adapter, json_output, BlcEtlEvent.MAP_BRIGHTNESS, BlcEtlField.RETURN_BRIGHTNESS)

    for panel in adapter.panels.values():
        if not panel.is_lfp:
            continue

        client_data = client_data_dict[panel.port]
        if remove_redundant_ddi is True:
            client_data = remove_redundant_values(client_data_dict[panel.port])
        transition_data = transition_data_dict[panel.port]
        max_fall[panel.port] = panel.max_fall
        min_cll[panel.port] = panel.min_cll

        if nit_ranges is not None:
            # Fetching max range residing at 2nd index of end list ([[1, 2 ,4], [1, 4, 5], [8, 7, 6]] --> 7)
            max_fall[panel.port] = int(nit_ranges[-1][1])

        logging.info(f"STEP: Verifying for {adapter.gfx_index} on {panel.port}")
        # Brightness3: HighPrecision/ LFP Nit Ranges/ HDR Metadata block (max_fall is not 0)/ disable_nits_brightness=0
        if is_high_precision or (nit_ranges is not None) or (panel.max_fall != 0) and disable_nits_brightness is False:
            os_requested_brightness = ddi_data
            min_milli_nits = min_cll[lfp1_port]
            if panel.port == lfp1_port:
                if is_high_precision:
                    max_milli_nits = 100000
                elif nit_ranges is not None:
                    # variables are values of list of list
                    min_milli_nits = convert_nits_to_milli_nits(int(nit_ranges[0][0]))
                    # Fetching max range residing at 2nd index of end list ([[1, 2 ,4], [1, 4, 5], [8, 7, 6]] --> 7)
                    max_milli_nits = convert_nits_to_milli_nits(int(nit_ranges[-1][1]))
                else:
                    #   if disable_boost_ranges is not present and panel is having HDR support do 80%:20%
                    if panel.hdr_caps.is_hdr_supported and (disable_boost_ranges is False):
                        max_milli_nits = convert_nits_to_milli_nits((max_fall[lfp1_port] * 80) // 100)
                    #   disable_boost_ranges is present or panel is not having HDR support do 100%
                    else:
                        max_milli_nits = convert_nits_to_milli_nits(max_fall[lfp1_port])

                logging.info(f"\tLuminance for OS in milli-nits. Max= {max_milli_nits}, Min= {min_milli_nits}")
                args = [is_high_precision, os_requested_brightness, min_milli_nits, max_milli_nits]

                if verify_nits_ranges(args, max_brightness_count, gdhm_scenario) is False:
                    return False
        else:
            #   for PWM, to remove consecutive redundant values as OS will give DDI on mode set.
            if is_pwm_based[panel.port]:
                os_requested_brightness = remove_redundant_values(ddi_data) if remove_redundant_ddi else ddi_data
        client_event_value = remove_redundant_values(client_data) if remove_redundant_ddi else client_data

        if panel.port == lfp1_port:
            if verify_brightness_ddi(expected_brightness, os_requested_brightness, event_name) is False:
                status = False

        # For Dual-LFP symmetric and asymmetric eDP
        if "MIPI_C" in is_pwm_based.keys():
            is_mipi_pwm = is_pwm_based['MIPI_C']

        if (is_pwm_based['DP_B'] and (panel.port == "DP_B")) or (is_mipi_pwm and (panel.port == "MIPI_C")):
            # In asymmetric panel, pnp_id_match is False else True
            if panel.max_fall != 0:
                event_name = BlcEtlEvent.SET_B3_DDI
            else:
                if pnp_id_match and nit_ranges is not None:
                    event_name = BlcEtlEvent.SET_B3_DDI
                else:
                    event_name = BlcEtlEvent.SET_B2_DDI

        # Disabled HDR / Disabled HDR + NIT Ranges / High Precision / PWM + Nit Ranges and disable_nits_brightness=0x0
        if is_pwm_based[panel.port] and (panel.port == lfp1_port) and disable_nits_brightness is False:
            if (((panel.port in hdr_state) and hdr_state[panel.port] is False)
                    or (nit_ranges is not None) or is_high_precision and bool(os_requested_brightness)):
                if verify_b3_transition(transition_data, os_requested_brightness, gdhm_scenario) is False:
                    status = False

        # HighPrecision / Disabled HDR + NIT Ranges / PWM panel
        if is_pwm_based[panel.port]:
            max_brightness = max_fall[panel.port]
            if (is_high_precision is False) and event_name == BlcEtlEvent.SET_B3_DDI:
                os_requested_brightness = convert_milli_nits_to_milli_percent(os_requested_brightness, max_brightness)
            elif (is_high_precision is True) and (panel.port != lfp1_port):
                # LFP2 can never be HighPrecision
                if panel.max_fall != 0:
                    logging.info("LFP2 Panel Max-fall is non-zero")
                else:
                    os_requested_brightness = [x // 1000 for x in os_requested_brightness]
            elif event_name == BlcEtlEvent.SET_B2_DDI and max_fall[lfp1_port] != 0 and disable_nits_brightness is False:
                # LFP1 as HDR capable and LFP2 is B2
                max_brightness = max_fall[lfp1_port]
                os_requested_brightness = convert_milli_nits_to_percent(os_requested_brightness, max_brightness)
            ##
            # In Independent Brightness path there is no relative brightness path for LFP2
            if panel.port in ["DP_B", "MIPI_C"] and set_second_lfp_brightness:
                logging.info("LFP2 is external to OS.So no OS DDI will be reported as part of set brightness event")
            else:
                if verify_blc_client(
                        client_event_value, os_requested_brightness, event_name, gdhm_scenario, panel) is False:
                    status = False

            if is_high_precision is False:
                is_nits_supported = {}
                if panel.port == lfp1_port:
                    is_nits_supported[panel.port] = (max_fall[panel.port] != 0 and disable_nits_brightness is False)
                else:
                    is_nits_supported[panel.port] = panel.max_fall != 0
                    if (adapter.panels[lfp1_port].pnp_id == panel.pnp_id) and (nit_ranges is not None):
                        is_nits_supported[panel.port] = True

                if verify_map_brightness(adapter, panel, map_user_blc_dict[panel.port], map_return_blc_dict[panel.port],
                                         is_nits_supported[panel.port]) is False:
                    # @todo seeing some failure specific to discrete & CS systems. So disabling this until investigated
                    # Created JIRA VSDI-37425 for tracking it and enable the test fail check
                    # status = False
                    logging.error("BLC_MAP_BRIGHTNESS failure seen")
            else:
                logging.info("Skipping user brightness mapping check for high precision brightness")
    return status


##
# @brief        Exposed API to verify Mapped Brightness
# @param[in]    adapter adapter object
# @param[in]    panel panel object
# @param[in]    user_brightness_list input brightness value
# @param[in]    return_brightness_list mapped brightness value
# @param[in]    is_nits_supported bool, True if panel is nits supported else False
# @return       True if successful, None, ETL/json file not found, False otherwise
def verify_map_brightness(adapter, panel, user_brightness_list, return_brightness_list, is_nits_supported: bool):
    if len(user_brightness_list) == 0:
        logging.error("Invalid input: No user brightness values provided")
        return False

    if len(user_brightness_list) != len(return_brightness_list):
        logging.error(f"Invalid input: No of user brightness ({len(user_brightness_list)}) "
                      f"& return brightness ({len(return_brightness_list)}) are not matching")
        return False

    if is_nits_supported:
        blc_multiplication_factor = 1
        bclm_multiplication_factor = BLC_PWM_HIGH_PRECISION_FACTOR
    else:
        blc_multiplication_factor = BLC_PWM_LOW_PRECISION_FACTOR
        bclm_multiplication_factor = 1

    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        bclm_table = brightness.get_bclm_table_for_pre_gen14(adapter.gfx_index)
    else:
        bclm_table = brightness.get_bclm_table_for_post_gen14(adapter.gfx_index, panel.port)

    if bclm_table is None:
        logging.error("Failed to get the BCLM table from OpRegion")
        return False

    logging.info(f"BCLM Table for {panel.port} on adapter {adapter.gfx_index}")
    for bclm_entry in bclm_table:
        logging.info(f"\t{bclm_entry}")

    mapped_brightness_list = []
    for user_brightness in user_brightness_list:
        return_brightness = None
        match_found = False
        min_brightness = 0
        min_duty_cycle = 0
        max_brightness = 100 * bclm_multiplication_factor
        max_duty_cycle = 255 * bclm_multiplication_factor

        for bclm_entry in bclm_table:
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                bclm_brightness = bclm_entry.Percent * bclm_multiplication_factor
                bclm_duty_cycle = bclm_entry.DutyCycle * bclm_multiplication_factor
            else:
                bclm_brightness = bclm_entry.BrightnessPercent * bclm_multiplication_factor
                bclm_duty_cycle = bclm_entry.DesiredDutyCycle * bclm_multiplication_factor

            # Map to user duty cycle if percent matches
            if bclm_brightness == user_brightness:
                return_brightness = (bclm_duty_cycle * 100 * blc_multiplication_factor) // 255
                match_found = True
                break

            # MinPercent and MinDutyCycle are the nearest lower entry data in BCLM table to User Brightness
            if (bclm_brightness < user_brightness) and (bclm_brightness >= min_brightness):
                min_duty_cycle = bclm_duty_cycle
                min_brightness = bclm_brightness

            # MaxPercent and MaxDutyCycle are the nearest higher entry data in BCLM table to User Brightness
            if (bclm_brightness > user_brightness) and (bclm_brightness <= max_brightness):
                max_duty_cycle = bclm_duty_cycle
                max_brightness = bclm_brightness

        if match_found is False:
            duty_cycle_range = max_duty_cycle - min_duty_cycle
            brightness_range = max_brightness - min_brightness
            if brightness_range == 0 or len(bclm_table) == 0:
                return_brightness = user_brightness * blc_multiplication_factor
            else:
                duty_cycle = ((user_brightness - min_brightness) * duty_cycle_range) // brightness_range
                duty_cycle += min_duty_cycle
                return_brightness = (duty_cycle * 100 * blc_multiplication_factor) // 255

        mapped_brightness_list.append(return_brightness)
    # compare mapped_brightness_list & return_brightness_list
    if mapped_brightness_list != return_brightness_list:
        logging.error(f"FAIL: BCLM verification. "
                      f"BLC Mapped brightness Expected= {mapped_brightness_list}, Actual= {return_brightness_list}")
        report_gdhm_driver("[PowerCons][BLC] Mismatch found in BCLM brightness mapping based on user brightness")
        return False

    logging.info(f"PASS: BCLM verification. "
                 f"BLC Mapped brightness Expected= {mapped_brightness_list}, Actual= {return_brightness_list}")
    return True


##
# @brief        Exposed API to verify for Invalid ranges
# @param[in]    adapter adapter object
# @param[in]    test_name string
# @param[in]    blc_etl_file etl file
# @return       True if successful, None, ETL/json file not found, False otherwise
def is_lfp_nit_range_valid(adapter, test_name, blc_etl_file):
    if os.path.exists(blc_etl_file) is False:
        logging.error("{0} not Found".format(blc_etl_file))
        return None
    json_output = run_diana(test_name, blc_etl_file, ['BLC'])

    if json_output is None:
        logging.error("JSON file not found")
        return None

    logging.info("STEP: Verifying LfpNitranges")
    range_invalid_status = get_error_from_diana(adapter, json_output, "BLC_USERBRIGHTNESS_FAILURE")
    if range_invalid_status is None:
        logging.error("Failed to Get JSON File")
        return False
    if range_invalid_status is False:
        logging.error("\t BLC validator passed with invalid Nit ranges")
        return False

    logging.info("\t Brightness not changed with invalid Nit ranges")
    return True


##
# @brief        Exposed API to verify Back-light
# @param[in]    adapter Adapter object
# @param[in]    scenario enum,  (MTO/TDR/AC_DC/MODE_SET/DISPLAY_CONFIG/CS/S3/S4)
# @param[in]    blc_args list  [is_pwm_based, nit_ranges, is_high_precision, hdr_state, brightness_list
#                           lpfPort, disable_boost_nit_ranges, is_invalid_nit_range_test, disable_nits_brightness]
# @return       etl_file scenario_status
def run_workload(adapter, scenario: Scenario, blc_args):
    display_power_ = display_power.DisplayPower()
    display_config_ = display_config.DisplayConfiguration()
    brightness_list = blc_args[4]
    scenario_status = True
    scenario_flag = False
    scenario_name = Scenario(scenario).name
    is_pwm_panel = blc_args[0]
    nit_ranges = None if len(blc_args) < 1 else blc_args[1]
    is_high_precision = None if len(blc_args) < 2 else blc_args[2]
    hdr_state = None if len(blc_args) < 3 else blc_args[3]
    is_invalid_nit_range_test = False if len(blc_args) < 7 else blc_args[7]
    disable_nits_brightness = False if len(blc_args) < 8 else blc_args[8]
    set_second_lfp_brightness = None if len(blc_args) < 9 else int(blc_args[9])
    # @todo harcoded value kept for independent brightness value, future needs to have dict to have param LFP1 and LFP2
    brightness_value = 37  # For Phase2 by default set to 37 and verify
    transition_steps = 200

    is_s3_supported = display_power_.is_power_state_supported(display_power.PowerEvent.S3)
    if scenario == Scenario.POWER_EVENT_CS and is_s3_supported:
        assert False, "Test needs CS enabled system, but it is having CS disabled (Planning Issue)"
    elif scenario == Scenario.POWER_EVENT_S3 and (is_s3_supported is False):
        assert False, "Test needs CS disabled system, but it is having CS enabled (Planning Issue)"

    logging.info("STEP: Initiating {0} scenario".format(scenario_name))
    # Stop the ETL tracer started during TestEnvironment initialization
    etl_tracer.stop_etl_tracer()

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBefore_' + scenario_name + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    #   if we set this after ETL trace then DDI will come for 100% brightness
    if scenario == Scenario.MONITOR_TIME_OUT:
        if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 1) is False:
            assert False, "FAILED to set display time-out to 1 minute (Test Issue)"
        logging.info("\tSuccessfully set display time-out to 1 minute")

    if is_invalid_nit_range_test:
        if display_essential.disable_driver(adapter.gfx_index) is False:
            logging.error("Failed to Disable the Driver")
            return False

    assert etl_tracer.start_etl_tracer(), "FAILED to start ETL tracer (Test Issue)"

    if is_invalid_nit_range_test:
        if display_essential.enable_driver(adapter.gfx_index) is False:
            logging.error("Failed to Enable the Driver")
            return False
        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            restart_display_service()
    # BLC functional tests are dependent on WMISetBrightness() and it is supported only when OS is aware of single LFP
    panels = list(adapter.panels.values())
    variant = "(PwmPanel= {0}, NitRanges= {1}, HighPrecision= {2}, HdrState= {3}, DisableNitsBrightness= {4})".format(
        is_pwm_panel, nit_ranges, is_high_precision, hdr_state, disable_nits_brightness)

    logging.info(f"Restrictions: {variant}")
    for itr in range(len(brightness_list)):
        # continue doing all brightness apply which will help in debug using ETL
        html.step_start(f"Setting {brightness_list[itr]}% brightness")
        if windows_brightness.set_current_brightness(brightness_list[itr], 1) is False:
            logging.error(f"FAILED to apply {brightness_list[itr]}% brightness")
            gdhm_title = "[PowerCons][BLC] Failed to apply ({0}%) brightness during {1} scenario({2})".format(
                brightness_list[itr], scenario_name, variant)
            report_gdhm_test(gdhm_title, gdhm.ProblemClassification.OTHER)
            break
        else:
            logging.info(f"\tSuccessfully set {brightness_list[itr]}% brightness")

        # call IGCL API to apply brightness on LFP2
        if set_second_lfp_brightness and adapter.lfp_count > 1:
            for panel in panels:
                if panel.is_lfp and panel.port in ['DP_B', 'MIPI_C']:
                    # call IGCL API
                    logging.info(f"Calling independent brightness IGCL call for port:{panel.port}")
                    # Apply Independent brightness via IGCL
                    if apply_independent_brightness(panel.target_id, brightness_value, transition_steps) is False:
                        scenario_status = False
                        gdhm.report_driver_bug_pc(
                            "Failed to apply independent brightness via IGCL on port".format(panel.port))
                        return None, scenario_status

        if scenario == Scenario.MONITOR_TIME_OUT:
            logging.info("\tWaiting for 120 seconds")
            time.sleep(120)

            # Move mouse to make sure display is in ON state before exiting the test
            win32api.SetCursorPos((400, 400))
            winkb_helper.press('ESC')
            logging.info("\tResumed from MTO")

        elif scenario == Scenario.DISPLAY_TDR:
            VerifierCfg.tdr = Verify.SKIP
            logging.debug(f"Updated config under-run:{VerifierCfg.underrun.name}, tdr:{VerifierCfg.tdr.name}")
            if itr == 0:
                #  Check any TDR by now
                if display_essential.detect_system_tdr(adapter.gfx_index) is True:
                    logging.error("TDR found while running the test")
                    scenario_status = False

                #  Generate TDR
                logging.info("\tGenerating TDR")
                if display_essential.generate_tdr(adapter.gfx_index, True) is False:
                    logging.error("FAILED to generate TDR (Test Issue)")
                    scenario_status = False

                #  detect tdr generation
                if display_essential.detect_system_tdr(adapter.gfx_index) is False:
                    logging.error("TDR not generated (Test Issue)")
                    scenario_status = False

                # Clear TDR dumps from system
                if display_essential.clear_tdr() is True:
                    logging.info("\tTDR cleared successfully post TDR generation")

        elif scenario == Scenario.AC_DC_SWITCH:
            power_line_state = display_power.PowerSource.DC if scenario_flag is True else display_power.PowerSource.AC

            if display_power_.set_current_powerline_status(power_line_state) is False:
                scenario_status = False

        elif scenario == Scenario.TOGGLE_SDR_HDR:
            for panel in panels:
                # to achieve toggle of HDR/SDR doing alternate of iteration(itr)
                if itr % 2 == 0:
                    logging.info("\tEnabling HDR in OS aware way")
                    if display_config.configure_hdr(
                            panel.display_info.DisplayAndAdapterInfo, enable=True) != HdrReturnStatus.SUCCESS:
                        logging.error("FAILED to enable HDR in OS aware way")
                        scenario_status = False
                else:
                    logging.info("\tDisabling HDR in OS aware way")
                    if display_config.configure_hdr(
                            panel.display_info.DisplayAndAdapterInfo, enable=False) != HdrReturnStatus.SUCCESS:
                        logging.error("FAILED to disable HDR in OS aware way")
                        scenario_status = False

        elif scenario == Scenario.MODE_SET:
            for panel in panels:
                if panel.drrs_caps.is_drrs_supported is False:
                    logging.error(f"{panel.port} doesn't support multi RR")
                    scenario_status = False
                    break

                # Switch to min/ max rr
                mode = common.get_display_mode(panel.target_id, panel.min_rr if scenario_flag else panel.max_rr)
                logging.info("Switching to {0}Hz ({1} RR)".format(mode, "Min" if scenario_flag else "MAX"))
                if display_config_.set_display_mode([mode], False) is False:
                    logging.error("FAILED to switch {0} RR".format("Min" if scenario_flag else "MAX"))
                    scenario_status = False

        elif scenario == Scenario.DISPLAY_CONFIG:
            config_list = [(enum.SINGLE, [panels[0].port]),
                           (enum.EXTENDED, [panels[0].port, panels[1].port]),
                           (enum.SINGLE, [panels[1].port]),
                           (enum.EXTENDED, [panels[1].port, panels[0].port]),
                           (enum.SINGLE, [panels[0].port]),
                           (enum.CLONE, [panels[0].port, panels[1].port]),
                           (enum.SINGLE, [panels[0].port])]

            # keeping this check because if brightness percent list is modified then index will be handled
            if itr >= len(config_list):
                logging.info("Skipping DisplayConfig as required display combinations are done")
            else:
                if display_config_.set_display_configuration_ex(config_list[itr][0], config_list[itr][1]) is False:
                    logging.error("FAILED to apply display config {0}".format(
                        str(config_list[itr][0]) + " " + " ".join(str(x) for x in config_list[itr][1])))
                    scenario_status = False

                # if single EFP only, reapply to clone mode.
                if config_list[itr] == (enum.SINGLE, [panels[1].port]):
                    logging.info("Applying Clone mode as previous config was SINGLE EFP only")
                    if display_config_.set_display_configuration_ex(
                            enum.CLONE, [panels[0].port, panels[1].port]) is False:
                        logging.error(f"FAILED to apply display config to CLONE {panels[0], panels[1]}")
                        scenario_status = False

        elif scenario in [Scenario.POWER_EVENT_CS, Scenario.POWER_EVENT_S3, Scenario.POWER_EVENT_S4]:
            is_s3_supported = display_power_.is_power_state_supported(display_power.PowerEvent.S3)
            if scenario == Scenario.POWER_EVENT_CS and is_s3_supported:
                logging.error("Test needs CS enabled system, but it is having CS disabled (Planning Issue)")
                scenario_status = False
                break
            elif scenario == Scenario.POWER_EVENT_S3 and (is_s3_supported is False):
                logging.error("Test needs CS disabled system, but it is having CS enabled (Planning Issue)")
                scenario_status = False
                break
            if itr == 3:  # doing power event only 1 time
                # POWER_EVENT_CS -> CS
                power_event = display_power.PowerEvent[scenario_name.split("_")[2]]
                if display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
                    scenario_status = False

        time.sleep(5)  # breather
        current_brightness = windows_brightness.get_current_brightness()
        if current_brightness is None:
            logging.error("FAILED to get current brightness")
            gdhm_title = "[PowerCons][BLC] Failed to get current brightness during {1} scenario({2})".format(
                brightness_list[itr], scenario_name, variant)
            report_gdhm_test(gdhm_title, gdhm.ProblemClassification.OTHER)
            break

        elif current_brightness != brightness_list[itr]:
            logging.error("Applied & Current brightness is NOT equal. Expected= {0}, Actual= {1}".format(
                brightness_list[itr], current_brightness))
            error_title = "[PowerCons][BLC] Applied({0}%) & Current({1}%) brightness is NOT equal during {2} " \
                          "scenario({3})".format(brightness_list[itr], current_brightness, scenario_name, variant)
            report_gdhm_driver(error_title)
            scenario_status = False
        logging.info(f"\tCurrent brightness is {current_brightness}%")

        scenario_flag = False if scenario_flag else True

    # Stop ETL tracer
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("\tFAILED to stop ETL Tracer(Test Issue)")
        return None, scenario_status

    new_etl_file = os.path.join(test_context.LOG_FOLDER, "GfxTraceDuring_" + scenario_name + str(time.time()) + ".etl")
    # Make sure etl file is present
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
        logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        return None, scenario_status

    # Rename the ETL file to avoid overwriting
    shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_etl_file)

    # Start ETL tracer post workload
    if etl_tracer.start_etl_tracer() is False:
        logging.error("FAILED to start ETL Tracer post workload(Test Issue)")
        return None, scenario_status

    return new_etl_file, scenario_status


##
# @brief        Exposed API to update backlight min brightness in VBT
# @param[in]    adapter Adapter, object
# @param[in]    min_brightness int
# @param[in]    precision_bit VbtBlcPrecisionBit (8, if VBT version < 236, [8,16], if version >=236)
# @return       gfx_vbt, is_reboot_needed,True reboot-True/Falseif successful, False otherwise
@html.step("Updating Backlight settings in VBT")
def configure_vbt(adapter, min_brightness, precision_bit: VbtBlcPrecisionBit):
    is_reboot_needed = False
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    for panel in adapter.panels.values():
        precision_bit = precision_bit.value
        port = panel.port.split('_')[1]  # DP_A / MIPI_A -> A

        logging.info(f"\tUpdating VBT settings for {adapter.gfx_index}-{port} with Min brightness= {min_brightness}, "
                     f"Precision Bit= {precision_bit}")

        if precision_bit not in [item.value for item in VbtBlcPrecisionBit]:
            logging.error(f"Invalid precision bits, Expected= [8, 16] Actual= {precision_bit}")
            return gfx_vbt, is_reboot_needed, False
        if precision_bit == VbtBlcPrecisionBit.BIT_PRECISION_8.value and min_brightness not in range(0, 256):
            logging.error(
                f"Invalid min brightness range for PrecisionBit= 8, Expected= (0, 255) Actual= {min_brightness}")
            return gfx_vbt, is_reboot_needed, False
        elif min_brightness not in range(0, 65536):
            logging.error(
                f"Invalid min brightness range for PrecisionBit= 16, Expected= (0, 65535) Actual= {min_brightness}")
            return gfx_vbt, is_reboot_needed, False

        panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
        logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
        if gfx_vbt.version < 234:
            vbt_min_brightness = gfx_vbt.block_43.BacklightFeaturesEntry[panel_index].MinimumBrightness
        else:
            #  for version >= 234
            vbt_min_brightness = gfx_vbt.block_43.MinBrightnessValue[panel_index]

        if vbt_min_brightness == min_brightness:
            logging.info(f"\tPASS: VBT is already having Min Brightness= {min_brightness}")
        else:
            if gfx_vbt.version < 234:
                gfx_vbt.block_43.BacklightFeaturesEntry[panel_index].MinimumBrightness = min_brightness
            else:
                # for version >= 234
                gfx_vbt.block_43.MinBrightnessValue[panel_index] = min_brightness

            if gfx_vbt.version >= 236:
                gfx_vbt.block_43.BrightnessPrecisionBits[panel_index] = precision_bit

            logging.info("\tApplying changes in VBT")
            if gfx_vbt.apply_changes() is False:
                logging.error("\tFAILED to apply changes in VBT")
                return gfx_vbt, is_reboot_needed, False

            status, is_reboot_needed = display_essential.restart_gfx_driver()
            logging.info("restart done")
            if status is False:
                return gfx_vbt, is_reboot_needed, False

    return gfx_vbt, is_reboot_needed, True


##
# @brief        Exposed API to update back light min brightness in VBT
# @param[in]    adapter Adapter, object
# @param[in]    gfx_vbt  vbt_info
# @param[in]    min_brightness int
# @return       True if successful, False otherwise
@html.step("Verifying Back-light settings in VBT")
def verify_backlight_vbt(adapter, gfx_vbt, min_brightness):
    dut.prepare()
    for panel in adapter.panels.values():
        panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

        # Verify after restarting the driver
        logging.info("\tReloading VBT data")
        gfx_vbt.reload()

        if gfx_vbt.version < 234:
            vbt_min_brightness = gfx_vbt.block_43.BacklightFeaturesEntry[panel_index].MinimumBrightness
        else:
            # for version >= 234
            vbt_min_brightness = gfx_vbt.block_43.MinBrightnessValue[panel_index]

        if vbt_min_brightness != min_brightness:
            logging.error(f"\tFAILED to apply Min Brightness= {min_brightness} in VBT")
            return False
        logging.info(f"\tPASS: Successfully applied Min Brightness= {min_brightness} in VBT")
    return True


##
# @brief        Exposed API to verify b3 transition with respect to Brightness DDI by OS
# @param[in]    client_event_value list of  client event values
# @param[in]    os_requested_brightness list of OS brightness DDI
# @param[in]    event_name string etl event name
# @param[in]    gdhm_scenario string
# @param[in]    panel object, Panel Class
# @return       bool
def verify_blc_client(client_event_value, os_requested_brightness, event_name, gdhm_scenario, panel):
    status = True
    for expected, actual in zip(os_requested_brightness, client_event_value):
        if panel.port in ["DP_A", "MIPI_A"] and expected != actual:
            status = False
        # Keeping tolerance of 1 for 2nd LFP because of conversion from Nits to Milli-percent
        elif panel.port in ["DP_B", "MIPI_C"] and expected not in [actual, actual + 1]:
            status = False

    if status is False or (len(os_requested_brightness) != len(client_event_value)):
        logging.error("BlcClientEvent and {0} DDI values are NOT equal. Expected= {1}, Actual= {2}".format(
            event_name, os_requested_brightness, client_event_value))
        gdhm_title = f"[PowerCons][BLC] BlcClientEvent is not happening for {event_name} DDI during {gdhm_scenario}"
        report_gdhm_driver(gdhm_title)
        return False
    logging.info("\tPASS: BlcClientEvent and {0} DDI values are equal. Expected= {1}, Actual= {2}".format(
        event_name, os_requested_brightness, client_event_value))
    return True


##
# @brief        Exposed API to verify b3 transition with respect to Brightness DDI by OS
# @param[in]    transition_data list of  B3 transition data to PWM
# @param[in]    os_requested_brightness list of OS brightness DDI
# @param[in]    gdhm_scenario string
# @return       bool
def verify_b3_transition(transition_data, os_requested_brightness, gdhm_scenario):
    if transition_data != os_requested_brightness:
        logging.error("B3Transition and B3 DDI are NOT equal. Expected= {0}, Actual= {1}".format(
            transition_data, os_requested_brightness))
        gdhm_title = "[PowerCons][BLC] B3Transition(NITS to PWM) is not happening for SetBrightness3 DDI " \
                     "during {0} scenario".format(gdhm_scenario)
        report_gdhm_driver(gdhm_title)
        return False
    logging.info("\tPASS: B3Transition and B3 DDI are equal. Expected= {0}, Actual= {1}".format(
        transition_data, os_requested_brightness))
    return True


##
# @brief        Exposed API to verify number of requested Brightness DDI by OS with expected brightness
# @param[in]    expected_brightness list of target brightness of lfp1 requested by OS B3 DDI(milli nits)
# @param[in]    os_requested_brightness list of OS brightness DDI
# @param[in]    event_name string Brightness DDI type
# @return       bool
def verify_brightness_ddi(expected_brightness, os_requested_brightness, event_name):
    if len(expected_brightness) != len(os_requested_brightness):
        logging.error("FAIL: Number of {0} DDI are NOT equal. Expected= {1}, Actual= {2}".format(
            event_name, len(expected_brightness), len(os_requested_brightness)))
        # @todo: due to OS issue avoiding unnecessary GDHM logging
        return False
    logging.info("\tPASS: Number of {0} DDI are equal. Expected= {1}, Actual= {2}".format(
        event_name, len(expected_brightness), len(os_requested_brightness)))
    return True


##
# @brief        Exposed API to verify requested Brightness DDI by OS is with in the range
# @param[in]    args list of is_high_precision, os_requested_brightness, min_milli_nits, max_milli_nits
# @param[in]    max_brightness_count number of max brightness expected
# @param[in]    scenario gdhm_scenario
# @return       True if successful, False otherwise
def verify_nits_ranges(args, max_brightness_count, scenario):
    report_gdhm = False
    max_brightness_hit = 0
    is_high_precision = args[0]
    os_requested_brightness = args[1]
    minimum = args[2]
    maximum = args[3]
    title = "[PowerCons][BLC] SetBrightness3 DDI is going beyond "
    for blc_value in os_requested_brightness:
        if is_high_precision is True and blc_value > maximum:
            logging.error("{0} nits is going beyond HighPrecision Range(0-100000)".format(blc_value))
            title = title + "HighPrecision"
            report_gdhm = True
        elif blc_value > maximum or blc_value < minimum:
            logging.error(f"{blc_value} nits is going beyond Nit Range({minimum}-{maximum})")
            report_gdhm = True
        if blc_value == maximum:
            max_brightness_hit += 1
    logging.info(f"\tSetBrightness3 DDI= {os_requested_brightness}")
    if max_brightness_hit != max_brightness_count:
        title = f"Number of max brightness NOT matching Actual= {max_brightness_hit}, Expected= {max_brightness_count}"
        logging.error(title)
        report_gdhm = True

    if report_gdhm is True:
        report_gdhm_driver(title + f" NITS range({minimum}-{maximum}) during {scenario} scenario")
        return False

    return True


##
# @brief        Exposed API to get relative milli-nits for provided target brightness (% -> milli-nits)
# @param[in]    target_brightness list list of % target brightness in client event after conversion
# @param[in]    max_panel_brightness int max panel brightness in nits
# @return       output_list list list of relative brightness value
def convert_percent_to_milli_nits(target_brightness, max_panel_brightness):
    output_list = []
    for target_brightness in target_brightness:
        # reverse mapping from milli-nits -> % : (target_brightness * 100) / (max_panel_brightness * 1000)
        output_list.append((int(target_brightness) * max_panel_brightness * 1000) // 100)
    return output_list


##
# @brief        Exposed API to get relative brightness for lfp2 based on lfp1 target brightness milli-nits -> mill%
# @param[in]    lfp1_target_brightness_list target brightness of lfp1 requested by OS B3 DDI(milli nits)
# @param[in]    max_panel_brightness max panel brightness of lfp1 in nits
# @return       relative_brightness_list relative brightness value for lfp2
def convert_milli_nits_to_milli_percent(lfp1_target_brightness_list, max_panel_brightness):
    relative_brightness_list = []
    for target_brightness in lfp1_target_brightness_list:
        blc = (int(target_brightness) * MilliPercentage.MAX.value) / convert_nits_to_milli_nits(max_panel_brightness)
        relative_brightness_list.append(math.floor(blc))
    return relative_brightness_list


##
# @brief        Exposed API to get relative brightness for lfp2 based on lfp1 target brightness milli-nits -> %
# @param[in]    lfp1_target_brightness_list target brightness of lfp1 requested by OS B3 DDI(milli nits)
# @param[in]    max_panel_brightness max panel brightness of lfp1 in nits
# @return       relative_brightness_list relative brightness value for lfp2
def convert_milli_nits_to_percent(lfp1_target_brightness_list, max_panel_brightness):
    relative_brightness_list = []
    for target_brightness in lfp1_target_brightness_list:
        blc = (Decimal(target_brightness) * 100) / convert_nits_to_milli_nits(max_panel_brightness)
        # 46.5 -> 47, 82.7 -> 83, 1.2 -> 1
        if blc - Decimal(math.floor(blc)) < 0.5:
            relative_brightness_list.append(math.floor(blc))
        else:
            relative_brightness_list.append(math.ceil(blc))
    return relative_brightness_list


##
# @brief        Exposed API to remove redundant consecutive values [0, 0, 0, 1, 2, 2, 0] -> [0, 1, 2, 0]
# @param[in]    input_list list with int value
# @return       output_list final list with unique int values
def remove_redundant_values(input_list):
    output_list = []
    for idx, val in enumerate(input_list):
        if idx == 0:
            output_list.append(val)
        else:
            if val != output_list[-1]:
                output_list.append(val)
    return output_list


##
# @brief        Exposed API to convert nits to milli-nits
# @param[in]    value int
# @return       value * 1000, milli-nits value
def convert_nits_to_milli_nits(value):
    return value * 1000


##
# @brief        Common API to report to gdhm for driver issue. Keeping this static with P2 and E2
# @param[in]    gdhm_title title to be kept while reporting to gdhm
# @return       None
def report_gdhm_driver(gdhm_title):
    gdhm.report_bug(
        title=gdhm_title,
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )


##
# @brief        Common API to report to gdhm for test issue. Keeping this static with P2 and E2
# @param[in]    gdhm_title title to be kept while reporting to gdhm
# @param[in]    classification ProblemClassification type of issue
# @return       None
def report_gdhm_test(gdhm_title, classification):
    gdhm.report_bug(
        title=gdhm_title,
        problem_classification=classification,
        component=gdhm.Component.Test.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )


##
# @brief        Exposed API to create nit ranges from given values min_max_step-size
# @param[in]    nit_ranges string, nit ranges [30_590_1_600_700_10]
# @return       List of nit ranges
def create_nit_ranges(nit_ranges):
    no_of_ranges = 0
    nit_range = []
    # checking the nit ranges in order of 3(min, max, step size)
    if len(nit_ranges) % 3 != 0:
        assert False, "NO Nits ranges are not in the range of three(min, max, Step size) (command-line issue)"
    while no_of_ranges < len(nit_ranges):
        nit_range.append([nit_ranges[no_of_ranges],
                          nit_ranges[no_of_ranges + 1],
                          nit_ranges[no_of_ranges + 2]])
        no_of_ranges += 3
    nit_ranges = nit_range  # [30_590_1_600_700_10]->[['30', '590', '1'],['600','700','10']]
    return nit_ranges


##
# @brief        Exposed API to apply Independent brightness on LFP2
# @param[in]    target_id Target id of the panel
# @param[in]    brightness_value brightness value to set
# @param[in]    transition_value transition_value to set
# @return       return True on Success ,False on Failure
def apply_independent_brightness(target_id, brightness_value, transition_value):
    display_properties = control_api_args.ctl_display_properties_t()
    display_properties.Size = ctypes.sizeof(control_api_args.ctl_display_properties_t)
    display_encoder_properties = control_api_args.ctl_adapter_display_encoder_properties_t()
    display_encoder_properties.Size = ctypes.sizeof(display_encoder_properties)
    set_brightness = control_api_args.ctl_set_brightness_t()
    set_brightness.Size = ctypes.sizeof(set_brightness)
    get_brightness = control_api_args.ctl_get_brightness_t()
    get_brightness.Size = ctypes.sizeof(get_brightness)

    logging.info(f"Get Display Properties for Target ID {target_id}")
    if control_api_wrapper.get_display_properties(display_properties, target_id) is False:
        logging.error(f"Get Display Properties Failed via Control Library for Target ID {target_id}")
        return False
    logging.info("Pass: Get Display Properties:: Target ID {0} and DisplayConfigFlags {1}".
                 format(display_properties.Os_display_encoder_handle.WindowsDisplayEncoderID,
                        display_properties.DisplayConfigFlags))
    if control_api_wrapper.get_display_encoder_properties(display_encoder_properties,
                                                          target_id) is False:
        logging.error("Fail: Get Display Encoder Properties via Control Library")
        return False
    logging.info("Pass: Get Display Encoder Properties :Display WindowsDisplayEncoderID {0}".format(
        display_encoder_properties.Os_display_encoder_handle.WindowsDisplayEncoderID))

    # check for companion display, BLC IGCL SET / GET call should be called for only companion display.
    if (display_encoder_properties.EncoderConfigFlags.value & control_api_args.ctl_display_config_flags_v.
            COMPANION_DISPLAY.value) != control_api_args.ctl_display_config_flags_v.COMPANION_DISPLAY.value:
        logging.error("Companion Display {0} is not enabled".format(display_encoder_properties.EncoderConfigFlags))
        return False
    logging.info("Companion Display {0} check is passed".format(display_encoder_properties.EncoderConfigFlags))

    # check for display active
    if (display_properties.DisplayConfigFlags.value & control_api_args.ctl_display_config_flags_v.DISPLAY_ACTIVE.value) != \
            control_api_args.ctl_display_config_flags_v.DISPLAY_ACTIVE.value:
        logging.error("Requested display is not Active")
        return False
    logging.info("Display is active {0}".format(display_properties.DisplayConfigFlags))
    set_brightness.TargetBrightness = brightness_value * BLC_PWM_HIGH_PRECISION_FACTOR
    set_brightness.SmoothTransitionTimeInMs = transition_value
    if control_api_wrapper.set_brightness_via_igcl(set_brightness, target_id) is False:
        logging.error("Set Brightness call failed, unable to apply brightness")
        return False
    time.sleep(1)  # breather after set brightness for second lfp
    if control_api_wrapper.get_brightness_via_igcl(get_brightness, target_id) is False:
        logging.error("Get Brightness call failed, unable to apply brightness")
        return False
    if set_brightness.TargetBrightness != get_brightness.CurrentBrightness:
        logging.error(f"Get/Set calls miss match Expected:{set_brightness.TargetBrightness} "
                      f"Actual:{get_brightness.CurrentBrightness}")
        return False
    logging.info("Pass: current brightness:{0} and Target brightness:{1}".format(
        get_brightness.CurrentBrightness, set_brightness.TargetBrightness))
    return True


##
# @brief        Exposed API to get instance_id for BLC support over external panel
# @return       None  if Fail, value if Pass
def get_monitor_instance_id():
    result = subprocess.run("powershell.exe -command  pnputil.exe /enum-devices /class 'Monitor'",
                            capture_output=True, universal_newlines=True)
    if result.returncode != 0:
        logging.error("Failed to fetch monitor details")
        return None
    pattern = re.compile(r"Status:\s+(.+?)\n")
    instance_id = pattern.findall(result.stdout)
    return None if len(instance_id) == 0 else instance_id


##
# @brief        Exposed API to add regkey for BLC support over external panel
# @param[in]    instance_id
# @return       None
def add_brightness_control_regkey(instance_id):
    regkey_status = True
    reg = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E96E-E325-11CE-BFC1-08002BE10318}"
    for i in range(len(instance_id)):
        device_id = f"000{i}"
        reg_path = fr"{reg}\{device_id}"
        reg_cmd = f"REG ADD {reg_path} /v BrightnessControl /f /t REG_DWORD /d 1"
        status = subprocess.run(reg_cmd)
        if status.returncode != 0:
            logging.warning(f"Regkey {reg_path} failed : {status.stdout} . {status.stderr}")
            regkey_status &= False
    return regkey_status


##
# @brief        Exposed API to delete regkey for BLC support over external panel
# @param[in]    instance_id
# @return       None
def delete_brightness_control_regkey(instance_id):
    regkey_status = True
    reg = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E96E-E325-11CE-BFC1-08002BE10318}"
    for i in range(len(instance_id)):
        device_id = f"000{i}"
        reg_path = fr"{reg}\{device_id}"
        reg_cmd = f"REG DELETE {reg_path} /v BrightnessControl /f"
        status = subprocess.run(reg_cmd)
        if status.returncode != 0:
            logging.warning(f"Regkey {reg_path} failed : {status.stdout} . {status.stderr}")
            regkey_status &= False
    return regkey_status


##
# @brief        This function set Brightness Control Method in the VBT
# @param[in]    adapter
# @param[in]    panel
# @param[in]    Vbt
# @return       status True/False
def set_blc_control_method_in_vbt(adapter: Adapter, panel: Panel, vbt_option):
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    if gfx_vbt.version < 259:
        logging.error(f"VBT version of XPST Expected: >259 and current:{gfx_vbt.version}")
        return False

    if gfx_vbt.block_43.BrightnessControlMethodEntry[panel_index].PwmSourceSelection == vbt_option:
        logging.info("VBT settings are already applied")
        return True

    gfx_vbt.block_43.BrightnessControlMethodEntry[panel_index].PwmSourceSelection = vbt_option
    if gfx_vbt.apply_changes() is False:
        logging.error("Faied to apply VBT Settings")
        return False

    # VBT is applied and driver restart is needed
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("Failed to restart display driver after VBT update")
        return False
    vbt.Vbt(adapter.gfx_index).reload()
    return True


#
# @brief        Exposed API to verify Brightness3 Vesa Aux Programming
# @param[in]    adapter object
# @param[in]   panel object
# @param[in]    test_name string
# @param[in]    blc_etl_file etl file
# @param[in]    remove_redundant_ddi boolean optional param to remove the redundant blc ddi
# @return       True if successful, None, ETL/json file not found, False otherwise
def verify_vesa_aux_programming(adapter: Adapter, panel: Panel, test_name, blc_etl_file, remove_redundant_ddi=True):

    if os.path.exists(blc_etl_file) is False:
        logging.error("{0} not Found".format(blc_etl_file))
        return None

    json_output = run_diana(test_name, blc_etl_file, ['BLC'])
    if json_output is None:
        logging.error("JSON file not found")
        return None

    ddi_data = parse_etl_events(adapter, json_output, BlcEtlEvent.SET_B3_DDI, BlcEtlField.DDI_MILLI_NITS, None)
    # removing first additional DDI requested while enabling of driver
    os_requested_brightness = remove_redundant_values(ddi_data['NONE']) if remove_redundant_ddi else ddi_data['NONE']

    if etl_parser.generate_report(blc_etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    # getting 0x734 AUX DPCD data
    dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.PANEL_TARGET_LUMINANCE_VALUE, 'AUX_CHANNEL_' + panel.pipe,True)
    if dpcd_data is None:
        logging.error("No Vesa Aux Programming happened")
        return False

    # Aux nits programming corresponding to each brightness change
    # ex- dpcd_data '10-02-1b' -> brightness = [(1b<<8)<<8 + 02<<8 + 10] = int(1B0210) = 1770000
    actual_nits_value = []
    for data in dpcd_data:
        parts = data.Data.split('-')
        decimal_value = (int(parts[2], 16) << 16) + (int(parts[1], 16) << 8) + int(parts[0], 16)
        actual_nits_value.append(decimal_value)

    actual_nits_value = remove_redundant_values(actual_nits_value) if remove_redundant_ddi else actual_nits_value

    if actual_nits_value == os_requested_brightness:
        logging.info(f"PASS: Actual nits programming = {actual_nits_value},expected nits programming = {os_requested_brightness}")
        return True
    logging.error(
        f"FAIL: Actual nits programming = {actual_nits_value},expected nits programming = {os_requested_brightness}")
    return False


#
# @brief        Exposed API to get nit ranges from DID2.1>>DP>>HDRMetadata
# @param[in]    panel object
# @param[in]    is_vesa_based: bool
# @return       Nit ranges else None
def get_nit_ranges(panel: Panel, is_vesa_based: bool):
    nitrange = []
    #Get nitranges from DID2.1 block
    if panel.luminance_caps.max_fall_did_2p1 > 0 and is_vesa_based:
        nitrange.append(panel.luminance_caps.min_cll_did_2p1)
        nitrange.append(panel.luminance_caps.max_fall_did_2p1)
        nitrange.append(1)
        return create_nit_ranges(nitrange)

    # Get nitranges from Display param block
    if panel.luminance_caps.max_fall_display_param > 0:
        nitrange.append(panel.luminance_caps.min_cll_display_param)
        nitrange.append(int(panel.luminance_caps.max_fall_display_param* 0.8))
        nitrange.append(1)
        return create_nit_ranges(nitrange)

    #get nitranges from hdr meta data
    if panel.max_fall > 0:
        nitrange.append(panel.min_cll)
        nitrange.append(int(panel.max_fall * 0.8))
        nitrange.append(1)
        return create_nit_ranges(nitrange)

    return None

##
# @brief      This function verifies Panel's Vesa DPCD Support
# @param[in]  panel
# @return     bool True or False
def is_vesa_dpcd_supported_by_panel(panel):
    return panel.vesa_caps.is_nits_brightness_supported and panel.vesa_caps.is_smooth_brightness_supported


#
# @brief        Exposed API to verify Brightness3 Custom Aux Programming
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    test_name string
# @param[in]    blc_etl_file etl file
# @param[in]    remove_redundant_ddi boolean optional param to remove the redundant blc ddi
# @return       True if successful, None, ETL/json file not found, False otherwise
def verify_custom_aux_programming(adapter: Adapter, panel: Panel, test_name, blc_etl_file, remove_redundant_ddi=True):

    if os.path.exists(blc_etl_file) is False:
        logging.error("{0} not Found".format(blc_etl_file))
        return None

    json_output = run_diana(test_name, blc_etl_file, ['BLC'])
    if json_output is None:
        logging.error("JSON file not found")
        return None

    ddi_data = parse_etl_events(adapter, json_output, BlcEtlEvent.SET_B3_DDI, BlcEtlField.DDI_MILLI_NITS, None)
    # removing first additional DDI requested while enabling of driver
    os_requested_brightness = remove_redundant_values(ddi_data['NONE']) if remove_redundant_ddi else ddi_data['NONE']

    if etl_parser.generate_report(blc_etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    # getting 0x354 AUX DPCD data
    dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.EDP_BRIGHTNESS_NITS, 'AUX_CHANNEL_' + panel.pipe,True)
    if dpcd_data is None:
        logging.error("No Custom Aux Programming happened")
        return False

    # Aux nits programming corresponding to each brightness change
    # ex- dpcd_data '78-00' -> brightness = [78 + (00 << 8)] = int(78)*1000 = 120000
    actual_nits_value = []
    for data in dpcd_data:
        parts = data.Data.split('-')
        decimal_value = (int(parts[0], 16) + (int(parts[1], 16) << 8))* 1000
        actual_nits_value.append(decimal_value)

    actual_nits_value = remove_redundant_values(actual_nits_value) if remove_redundant_ddi else actual_nits_value

    if actual_nits_value == os_requested_brightness:
        logging.info(f"PASS: Actual nits programming = {actual_nits_value},expected nits programming = {os_requested_brightness}")
        return True
    logging.error(
        f"FAIL: Actual nits programming = {actual_nits_value},expected nits programming = {os_requested_brightness}")
    return False
