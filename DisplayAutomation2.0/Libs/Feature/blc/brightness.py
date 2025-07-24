########################################################################################################################
# @file         brightness.py
# @brief        Python wrapper which exposes API's related to Brightness3 Functionalities
# @author       Vinod D S
########################################################################################################################
import array
import ctypes
import logging
import os

from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.test_env import test_context
from Libs.Core.sw_sim import driver_interface
from Libs.Feature.blc import brightness_args
from Tests.PowerCons.Modules import common

MB3_BCLM_TABLE_START = 0x31C
MB3_BCLM_TABLE_SIZE = 0x28
MB2_LFP1_BCM_TABLE_START = 0x210
MB2_LFP2_BCM_TABLE_START = 0x288
MB2_BCM_TABLE_SIZE = 0x78

gfxValSimDLL = None


##
# @brief        Brightness3 Load Library.
# @return       None
def load_library():
    global gfxValSimDLL
    ##
    # Load DisplayConfig C library
    gfxValSimDLL = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(), 'GfxValSim.dll'))


##
# @brief        API to SetBrightness3
# @param[in]    gfx_index
# @param[in]    target_id target id of display
# @param[in]    brightness3_buffer of type DXGK_DSI_TRANSMISSION
# @return       status - bool value
def set_brightness3(gfx_index, target_id, brightness3_buffer):
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_uint, ctypes.c_uint,
                                  ctypes.POINTER(brightness_args.DXGK_BRIGHTNESS_SET_IN))
    func = prototype(('GfxValSimSetBrightness3', gfxValSimDLL))

    status = func(ctypes.byref(adapter_info), ctypes.sizeof(GfxAdapterInfo), target_id,
                  ctypes.byref(brightness3_buffer))
    if not status:
        logging.error("Failed to trigger Set Brightness3")

    return status


##
# @brief        API to get BCLM table for pre Gen14 platforms
# @param[in]    gfx_index - Graphics Adapter Index
# @return       status - None if error else list having BCLM entries
def get_bclm_table_for_pre_gen14(gfx_index):
    bclm_table = []
    opregion_data, opregion_size = driver_interface.DriverInterface().get_default_opregion(gfx_index)
    if opregion_data is None:
        return None

    if opregion_size <= (MB3_BCLM_TABLE_START + MB3_BCLM_TABLE_SIZE):
        return None
    bclm_data = array.array('B', opregion_data[MB3_BCLM_TABLE_START:MB3_BCLM_TABLE_START + MB3_BCLM_TABLE_SIZE])
    for index in range(0, MB3_BCLM_TABLE_SIZE, 2):
        bclm_entry = brightness_args.BCLMEntry()
        bclm_entry.byte_data[0] = bclm_data[index]
        bclm_entry.byte_data[1] = bclm_data[index + 1]
        if not bclm_entry.ValidBit:
            break
        bclm_table.append(bclm_entry)
    if len(bclm_table) == 0:
        return None
    return bclm_table


##
# @brief        API to get BCLM table for Gen14 platform onwards
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    port - DP_A,DP_B,MIPI_C
# @return       status - None if error else list having BCLM entries
def get_bclm_table_for_post_gen14(gfx_index, port):
    ##
    # From Gen14, Dual LFP will have individual bclm table as LFP1 and LFP2 blocks
    bclm_table = []
    opregion_data, opregion_size = driver_interface.DriverInterface().get_default_opregion(gfx_index)
    if opregion_data is None:
        return None

    if port in ["DP_B", "MIPI_C"]:
        start_index = MB2_LFP2_BCM_TABLE_START
    else:
        start_index = MB2_LFP1_BCM_TABLE_START
    end_index = start_index + MB2_BCM_TABLE_SIZE

    if end_index >= opregion_size:
        return None
    bclm_data = array.array('B', opregion_data[start_index:end_index])

    for index in range(0, MB2_BCM_TABLE_SIZE, 4):
        bclm_entry = brightness_args.BCMEntry()
        bclm_entry.byte_data[0] = bclm_data[index]
        bclm_entry.byte_data[1] = bclm_data[index + 1]
        bclm_entry.byte_data[2] = bclm_data[index + 2]
        bclm_entry.byte_data[3] = bclm_data[index + 3]
        if not bclm_entry.FieldValidBit:
            break
        bclm_table.append(bclm_entry)
    if len(bclm_table) == 0:
        return None
    return bclm_table
