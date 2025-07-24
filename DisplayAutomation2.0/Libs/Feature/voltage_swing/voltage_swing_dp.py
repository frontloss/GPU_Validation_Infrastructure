#################################################################################################################
# @file         voltage_swing_dp.py
# @brief        Library having voltage swing verification related APIs for display port.
# @author       Rohit Kumar, Tulika
#################################################################################################################
import csv
import ctypes
import logging
import os
import time

from enum import IntEnum

from Libs.Core import display_utility, driver_escape
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.display_port import dpcd_helper
from registers.mmioregister import MMIORegister

GDHM_VSWING = "[Display_Interfaces][EDP][VSWING]"


##
# @brief This class has the protocol values
class Protocol:
    DpHbr2AndHbr3 = "DPHBR2andHBR3"
    EdpUptoHbr2 = "eDPuptoHBR2"
    EdpHbr3 = "eDPHBR3"


# Voltage Swing programming file path, voltage swing tables for all the platforms will be stored in this file
VOLTAGE_SWING_PROGRAMMING = os.path.join(test_context.ROOT_FOLDER,
                                         "Libs\\Feature\\voltage_swing\\voltage_swing_programming.csv")

##
# Supported voltage swing and pre-emphasis level combinations
# [voltage swing level, pre emphasis level]
MAX_VOLTAGE_SWING_LEVELS = 10
VSWING_EMP_SEL = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]]

##
# Max string length to store protocol (Up to HBR2, HBR3)
MAX_PROTOCOL_LENGTH = 20

##
# DPCD Offsets
# TRAINING_LANE_SET : used to read voltage swing and pre-emphasis levels for each lane (0 to 3)
# bits 1:0 - voltage swing level (0, 1, 2, 3)
# bits 4:3 - pre-emphasis level (0, 1, 2, 3)
# LANE_COUNT_SET: number of active lanes
# bits 4:0 - number of lanes (1, 2, 4)
__DPCD_OFFSET_TRAINING_LANE_SET = [0x103, 0x104, 0x105, 0x106]
__DPCD_MASK_TRAINING_LANE_SET = 0x3
__DPCD_OFFSET_LANE_COUNT_SET = 0x101
__DPCD_MASK_LANE_COUNT_SET = 0xF


##
# Enum for voltage swing and pre-emphasis levels
class VSwingEmpSel(IntEnum):
    SEL0 = 0
    SEL1 = 1
    SEL2 = 2
    SEL3 = 3
    SEL4 = 4
    SEL5 = 5
    SEL6 = 6
    SEL7 = 7
    SEL8 = 8
    SEL9 = 9
    SEL_MAX = 10


##
# Structure to store voltage swing programming table entry
class VoltageSwingEntry(ctypes.Structure):
    _fields_ = [('protocol', ctypes.c_char * MAX_PROTOCOL_LENGTH),
                ('voltage_swing_level', ctypes.c_int),
                ('pre_emphasis_level', ctypes.c_int),
                ('swing_sel_dw2', ctypes.c_int),
                ('n_scalar_dw7', ctypes.c_int),
                ('cursor_coeff_dw4', ctypes.c_int),
                ('post_cursor_2_dw4', ctypes.c_int),
                ('post_cursor_1_dw4', ctypes.c_int),
                ('rcomp_scalar_dw2', ctypes.c_int),
                ('rterm_select_dw5', ctypes.c_int),
                ('_3_tap_disable_dw5', ctypes.c_int),
                ('_2_tap_disable_dw5', ctypes.c_int),
                ('cursor_program_dw5', ctypes.c_int),
                ('coeff_polarity_dw5', ctypes.c_int)
                ]


##
# Structure for voltage swing table
class VoltageSwingTable(ctypes.Structure):
    _fields_ = [('data', VoltageSwingEntry * (MAX_VOLTAGE_SWING_LEVELS * 2)),
                ('count', ctypes.c_int)
                ]


##
# @brief        Exposed function to verify the PHY programming for DP by comparing voltage swing level programmed
#               in DPCD with voltage swing level programmed in PHY registers.
# @param[in]    display the DP display for which verification needs to be done Ex. DP_A, DP_B
# @return       voltage swing levels, if verification is successful, False otherwise
def verify_voltage_swing(display):
    # Voltage swing programming is verified for 'DP' if panel index is in range(0,16) using below steps:
    # VSwingPreEmphasisTableSelection (https://gfxspecs.intel.com/Predator/Home/Index/49291)
    # Bit 3:0/7:4 - based on panel index
    #               eDP Vswing Pre-emph setting table
    #               0 =  Low Power Swing setting(200 mV)
    #               1 =  Default Swing settings(400 mV)
    # Step 1: Parse both low and default values from .csv file for the particular platform.
    # Step 2: Check for the voltage table settings in VBT by default it will be 'LOW' else can be set as 'DEFAULT'
    # Step 3: Get the expected number of lanes from DPCD
    # Step 4: Get the active number of lanes from DDI_BUF_CTL and compare both expected and active lanes.
    #         bits 3:1, Number of lanes
    #                   0b000 - 1 Lane
    #                   0b001 - 2 Lanes
    #                   0b011 - 4 Lanes
    # Step 5: Verify voltage swing and pre-emphasis levels for the number of active lanes.
    # Step 6: Get the expected voltage swing and pre-emphasis levels from DPCD and validate it from VSWING_EMP_SEL
    # Step 7: Get the programmed voltage and actual pre_emphasis values from PHY registers.
    # Step 8: Get expected voltage and expected pre_emphasis values from .csv file for the respected protocol
    # Step 9: Compare both expected, actual; voltage swing and pre-emphasis values

    machine_info = SystemInfo()
    display_config_ = display_config.DisplayConfiguration()
    vbt = Vbt()
    platform_name = None

    # Set display type and display port from 'DP_A'
    display_type = display.split('_')[0]
    display_port = display.split('_')[-1]

    # Check if targeted display type is DP
    if display_type != 'DP':
        logging.error(f"\tDisplay type {display_type} is NOT supported for voltage swing verification")
        return False

    panel_index = vbt.get_lfp_panel_type(display)
    logging.debug(f"\tPanel Index for {display}= {panel_index}")

    # Make sure panel_index is present
    if panel_index not in range(16):
        logging.error(f"\tInvalid panel index {panel_index}")
        return False

    # Get the target id
    enumerated_displays = display_config_.get_enumerated_display_info()
    if enumerated_displays is None:
        logging.error("\tget_enumerated_display_info() API call failed")
        return False
    target_id = display_config_.get_target_id(display, enumerated_displays)

    # Get current platform
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # Once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform_name = gfx_display_hwinfo[i].DisplayAdapterName
        break

    if platform_name is None:
        logging.error("\tAPI get_system_info() failed to return platform details")
        return False

    # Check if voltage swing verification is supported on current platform
    if is_platform_supported(platform_name) is False:
        logging.error(f"\tVoltage Swing verification is NOT supported on {platform_name}")
        return False

    # Parse voltage swing tables for current platform
    voltage_swing_table, vswing_table_selection = __get_voltage_swing_table(platform_name, 'DEFAULT')
    low_voltage_swing_table, vswing_table_selection = __get_voltage_swing_table(platform_name, 'LOW')

    # Check if targeted display is eDP, if yes check the voltage table settings in VBT
    if display_utility.get_vbt_panel_type(display, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
        shift = 0
        if panel_index % 2 != 0:
            shift = 3
        if (vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == 0:
            voltage_swing_table = low_voltage_swing_table
            logging.info("\tVBT VSwingPreEmphasis Table Selection= LOW VOLTAGE TABLE")
        else:
            logging.info("\tVBT VSwingPreEmphasis Table Selection= DEFAULT VOLTAGE TABLE")

    # Get number of expected number of lanes from DPCD_OFFSET_LANE_COUNT_SET
    dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(target_id, __DPCD_OFFSET_LANE_COUNT_SET)
    # If DPCD read fails, try reading after 1 second
    if dpcd_read_flag is False:
        time.sleep(1)
        dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(target_id, __DPCD_OFFSET_LANE_COUNT_SET)
    if dpcd_read_flag:
        dpcd_value = dpcd_value[0]
        logging.debug(f"\tDPCD_OFFSET_LANE_COUNT_SET({hex(__DPCD_OFFSET_LANE_COUNT_SET)})= {hex(dpcd_value)}")
    else:
        logging.error(f"\tFailed to read DPCD offset {hex(__DPCD_OFFSET_LANE_COUNT_SET)}")
        return False
    expected_number_of_lanes = dpcd_value & __DPCD_MASK_LANE_COUNT_SET

    # Get number of active lanes from DDI_BUF_CTL
    offset_name = f"DDI_BUF_CTL_{display_port}"
    ddi_buf_ctl = MMIORegister.read("DDI_BUF_CTL_REGISTER", offset_name, platform_name)
    reg_value = ddi_buf_ctl.__getattribute__("dp_port_width_selection")

    logging.debug(f"\tDDI_BUF_CTL_{display_port} dp_port_width_selection= {hex(reg_value)}")
    if reg_value == 0:
        actual_number_of_lanes = 1
    elif reg_value == 1:
        actual_number_of_lanes = 2
    elif reg_value == 3:
        actual_number_of_lanes = 4
    else:
        logging.error(f"\tInvalid number of lanes({reg_value}) are programmed in DDI_BUF_CTL_{display_port}.")
        gdhm.report_driver_bug_di(
            f"{GDHM_VSWING}Invalid number of lanes are programmed in DDI_BUF_CTL")
        return False

    # Verify expected and actual number of lanes are equal
    if expected_number_of_lanes == actual_number_of_lanes:
        logging.info(f"\tPASS: Expected number of lanes= {expected_number_of_lanes}, Actual= {actual_number_of_lanes}")
    else:
        logging.error(f"\tFAIL: Expected number of lanes= {expected_number_of_lanes}, Actual= {actual_number_of_lanes}")
        return False

    # Verify voltage swing and pre-emphasis for each lane
    lane_status = True
    voltage_swing_levels = {}
    for lane_index in range(actual_number_of_lanes):
        # Read voltage swing and pre-emphasis levels from DPCD
        dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(target_id, __DPCD_OFFSET_TRAINING_LANE_SET[lane_index])
        # If DPCD read fails, try reading after 1 second
        if dpcd_read_flag is False:
            time.sleep(1)
            dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(target_id, __DPCD_OFFSET_LANE_COUNT_SET)
        if dpcd_read_flag:
            dpcd_value = dpcd_value[0]
            logging.debug(
                f"\tDPCD_OFFSET_TRAINING_LANE_SET({hex(__DPCD_OFFSET_TRAINING_LANE_SET[lane_index])})= {hex(dpcd_value)}")
        else:
            logging.error(
                f"\tFailed to read DPCD offset {hex(__DPCD_OFFSET_TRAINING_LANE_SET[lane_index])} for lane={lane_index}")
            lane_status = False
            continue

        # bits 1:0 - voltage swing level
        dpcd_voltage_swing_level = (dpcd_value & __DPCD_MASK_TRAINING_LANE_SET)
        # bits 4:3 - pre-emphasis level
        dpcd_pre_emphasis_level = (dpcd_value >> 3) & __DPCD_MASK_TRAINING_LANE_SET

        # Validate the dpcd voltage swing and pre-emphasis levels
        if [dpcd_voltage_swing_level, dpcd_pre_emphasis_level] in VSWING_EMP_SEL:
            expected_vswing_emp_sel = VSWING_EMP_SEL.index(
                [dpcd_voltage_swing_level, dpcd_pre_emphasis_level])
        else:
            logging.error(f"\tDPCD training parameters for lane {lane_index}")
            logging.error(f"\t\tDPCD VSwing Level={dpcd_voltage_swing_level}")
            logging.error(f"\t\tDPCD Pre-emphasis Level={dpcd_pre_emphasis_level}")
            logging.error("\tInvalid voltage swing and pre-emphasis levels are programmed in DPCD")
            gdhm.report_driver_bug_di(
                f"{GDHM_VSWING}Invalid voltage swing and pre-emphasis levels are programmed in DPCD")
            lane_status = False
            continue

        # Get the programmed voltage and expected pre_emphasis values from PHY registers
        actual_vswing_emp_sel = None
        offset_name = f"PORT_TX_DW2_LN{lane_index}_{display_port}"
        port_tx_dw2_lnx = MMIORegister.read("PORT_TX_DW2_REGISTER", offset_name, platform_name)
        offset_name = f"PORT_TX_DW4_LN{lane_index}_{display_port}"
        port_tx_dw4_lnx = MMIORegister.read("PORT_TX_DW4_REGISTER", offset_name, platform_name)
        offset_name = f"PORT_TX_DW5_LN{lane_index}_{display_port}"
        port_tx_dw5_lnx = MMIORegister.read("PORT_TX_DW5_REGISTER", offset_name, platform_name)
        offset_name = f"PORT_TX_DW7_LN{lane_index}_{display_port}"
        port_tx_dw7_lnx = MMIORegister.read("PORT_TX_DW7_REGISTER", offset_name, platform_name)

        logging.info(f"\t\tDriver programmed values for lane {lane_index} in PHY registers:")
        logging.info(f"\t\tswing_sel:         {port_tx_dw2_lnx.swing_sel_upper:b}{port_tx_dw2_lnx.swing_sel_lower:03b}")
        logging.info(f"\t\tn_scalar_dw7:      {hex(port_tx_dw7_lnx.NScalar)}")
        logging.info(f"\t\tcursor_coeff_dw4:  {hex(port_tx_dw4_lnx.cursor_coeff)}")
        logging.info(f"\t\tpost_cursor_2_dw4: {hex(port_tx_dw4_lnx.post_cursor_2)}")
        logging.info(f"\t\tpost_cursor_1_dw4: {hex(port_tx_dw4_lnx.post_cursor_1)}")
        logging.info(f"\t\trcomp_scalar_dw2:  {hex(port_tx_dw2_lnx.rcomp_scalar)}")
        logging.info(f"\t\trterm_select_dw5:  {bin(port_tx_dw5_lnx.RtermSelect)}")
        logging.info(f"\t\t_3_tap_disable_dw5:{bin(port_tx_dw5_lnx.Disable3Tap)}")
        logging.info(f"\t\t_2_tap_disable_dw5:{bin(port_tx_dw5_lnx.Disable2Tap)}")
        logging.info(f"\t\tcursor_program_dw5:{bin(port_tx_dw5_lnx.CursorProgram)}")
        logging.info(f"\t\tcoeff_polarity_dw5:{bin(port_tx_dw5_lnx.CoeffPolarity)}")

        # Get expected voltage and expected pre_emphasis values from DP_VOLTAGE_SWING table
        start_index = 0
        end_index = 10
        is_hbr3 = False
        protocol = Protocol.EdpUptoHbr2 if vswing_table_selection == 'LOW' else Protocol.DpHbr2AndHbr3

        # Get link rate from DPCD
        link_rate = dpcd_helper.DPCD_getLinkRate(target_id)
        logging.info(f"\tLink rate supported in DPCD={link_rate} GHz/lane")

        # In case of HBR3, change the index of voltage swing table
        if link_rate > 5.4:
            start_index = 10 if vswing_table_selection == 'LOW' else 0
            end_index = 20 if vswing_table_selection == 'LOW' else 10
            is_hbr3 = True
            protocol = Protocol.EdpHbr3 if vswing_table_selection == 'LOW' else Protocol.DpHbr2AndHbr3
            logging.info(f"\tVerifying PHY programming for {protocol}")
        else:
            logging.info(f"\tVerifying PHY programming for {protocol}")

        index = 0
        is_voltage_swing_level_present = False
        # @Todo Helper function can be created for better read-ablity
        for record in voltage_swing_table.data[start_index:end_index]:
            if (
                    ((int(f"{port_tx_dw2_lnx.swing_sel_upper:b}{port_tx_dw2_lnx.swing_sel_lower:03b}",
                          2)) == record.swing_sel_dw2) and
                    (port_tx_dw2_lnx.rcomp_scalar == record.rcomp_scalar_dw2) and
                    (port_tx_dw4_lnx.cursor_coeff == record.cursor_coeff_dw4) and
                    (port_tx_dw4_lnx.post_cursor_2 == record.post_cursor_2_dw4) and
                    (port_tx_dw4_lnx.post_cursor_1 == record.post_cursor_1_dw4) and
                    (port_tx_dw5_lnx.RtermSelect == record.rterm_select_dw5) and
                    (port_tx_dw5_lnx.Disable3Tap == record._3_tap_disable_dw5) and
                    (port_tx_dw5_lnx.Disable2Tap == record._2_tap_disable_dw5) and
                    (port_tx_dw5_lnx.CursorProgram == record.cursor_program_dw5) and
                    (port_tx_dw5_lnx.CoeffPolarity == record.coeff_polarity_dw5) and
                    (port_tx_dw7_lnx.NScalar == record.n_scalar_dw7)
            ):
                actual_vswing_emp_sel = index
                is_voltage_swing_level_present = True
                break
            index += 1

        if is_voltage_swing_level_present is True:
            if is_hbr3 is True:
                logging.info(f"\tExpected protocol= eDPHBR3, Actual= {protocol}")
            if vswing_table_selection == 'DEFAULT':
                logging.info(f"\tExpected protocol= DPHBR2andHBR3, Actual= {protocol}")
            else:
                logging.info(f"\tExpected protocol= eDPuptoHBR2, Actual= {protocol}")
        else:
            logging.error(
                f"\tInvalid voltage swing and pre-emphasis levels are programmed for lane {lane_index} by driver")
            gdhm.report_driver_bug_di(
                f"{GDHM_VSWING}Invalid voltage swing and pre-emphasis levels are programmed by driver")
            lane_status = False

        if expected_vswing_emp_sel is None or actual_vswing_emp_sel is None:
            logging.error("\tUnable to find expected or actual vswing_emp_sel value")
            lane_status = False
            continue

        # Verify expected and actual levels are equal
        if expected_vswing_emp_sel == actual_vswing_emp_sel:
            logging.info(
                f"\tPASS: Expected voltage swing pre-emphasis level for Lane "
                f"{lane_index}= {VSwingEmpSel(expected_vswing_emp_sel)}, Actual= {VSwingEmpSel(actual_vswing_emp_sel)}")
            voltage_swing_levels[lane_index] = actual_vswing_emp_sel
        else:
            logging.error(
                f"\tFAIL: Expected voltage swing pre-emphasis level for Lane "
                f"{lane_index}= {VSwingEmpSel(expected_vswing_emp_sel)}, Actual= {VSwingEmpSel(actual_vswing_emp_sel)}")
            gdhm.report_driver_bug_di(
                f"{GDHM_VSWING} Expected voltage swing pre-emphasis level for Lane does not match with Actual")
            lane_status = False
            continue

    if lane_status is True:
        return voltage_swing_levels
    return False


##
# @brief        To get supported Platforms
# @param[in]    platform
# @return       List of all the platforms
def is_platform_supported(platform):
    if os.path.exists(VOLTAGE_SWING_PROGRAMMING) is False:
        logging.error(f"\tVoltage Swing Configuration file is NOT found in path")
        return False
    with open(VOLTAGE_SWING_PROGRAMMING) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if platform in row['Platform']:
                return True
        return False


##
# @brief        Helper function to get voltage swing programming table data from file into given list
# @param[in]    platform_name, platform name for which table data has to be read
# @param[in]    table_selection, default_voltage_swing or low_voltage_swing table selection
# @return       table_selection, table, object of VoltageSwingTable type, having requested table data
def __get_voltage_swing_table(platform_name, table_selection):
    table = VoltageSwingTable()
    if table_selection == 'LOW':
        protocol = [Protocol.EdpUptoHbr2, Protocol.EdpHbr3]
    elif table_selection == 'DEFAULT':
        protocol = [Protocol.DpHbr2AndHbr3]
    index = 0
    # Get the table data from CSV
    with open(VOLTAGE_SWING_PROGRAMMING) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row['Protocol'] in protocol and platform_name in row['Platform']:
                table.data[index].protocol = row['Protocol'].encode()
                table.data[index].voltage_swing_level = int(row['Voltage Swing Level'])
                table.data[index].pre_emphasis_level = int(row['Pre-Emphasis Level'])
                table.data[index].swing_sel_dw2 = int(row['Swing Sel DW2 binary'], 2)
                table.data[index].n_scalar_dw7 = int(row['N Scalar DW7 hex'], 16)
                table.data[index].cursor_coeff_dw4 = int(row['Cursor Coeff DW4 hex'], 16)
                table.data[index].post_cursor_2_dw4 = int(row['Post Cursor 2 DW4 hex'], 16)
                table.data[index].post_cursor_1_dw4 = int(row['Post Cursor 1 DW4 hex'], 16)
                table.data[index].rcomp_scalar_dw2 = int(row['Rcomp Scalar DW2 hex'], 16)
                table.data[index].rterm_select_dw5 = int(row['Rterm Select DW5 binary'], 2)
                table.data[index]._3_tap_disable_dw5 = int(row['3 Tap Disable DW5'], 2)
                table.data[index]._2_tap_disable_dw5 = int(row['2 Tap Disable DW5'], 2)
                table.data[index].cursor_program_dw5 = int(row['Cursor program DW5'], 2)
                table.data[index].coeff_polarity_dw5 = int(row['Coeff Polarity DW5'], 2)
                index += 1
    return table, table_selection
