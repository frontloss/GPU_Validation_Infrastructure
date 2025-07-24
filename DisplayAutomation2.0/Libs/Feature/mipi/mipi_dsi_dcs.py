########################################################################################################################
# @file     mipi_dsi_dcs.py
# @brief    Python wrapper which exposes API's related to MIPI DSI DCS Functionalities
# @author   Chandrakanth Pabolu
########################################################################################################################
import ctypes
import logging
import os

from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.test_env import test_context
from Libs.Feature.mipi import mipi_dsi_dcs_args

gfxValSimDLL = None


##
# @brief helper function to Load GfxValsim Library.
# @return None
def load_library():
    global gfxValSimDLL
    ##
    # Load DisplayConfig C library
    gfxValSimDLL = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(), 'GfxValSim.dll'))


##
# @brief        API to Get MIPI DSI Caps based on DCS. It fills caps into the passed dsi_buffer_caps object
# @param[in]    gfx_index Gfx Adapter index
# @param[in]    target_id target id of display
# @param[in]    dsi_buffer_caps of type DXGK_DSI_CAPS
# @return       True if call successful, False otherwise
def get_mipi_dsi_caps(gfx_index, target_id, dsi_buffer_caps):
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_uint, ctypes.c_uint,
                                  ctypes.POINTER(mipi_dsi_dcs_args.DXGK_DSI_CAPS))
    func = prototype(('GfxValSimGetMIPIDSICaps', gfxValSimDLL))

    status = func(ctypes.byref(adapter_info), ctypes.sizeof(GfxAdapterInfo), target_id, ctypes.byref(dsi_buffer_caps))
    if not status:
        logging.error("Failed to trigger MIPI DSI Caps .")

    return status


##
# @brief        API to Perform MIPI DSI DCS Transmission
# @param[in]    gfx_index Gfx Adapter index
# @param[in]    target_id target id of display
# @param[in]    dsi_buffer_transmission of type DXGK_DSI_TRANSMISSION
# @return       True if MIPI DSI transmission triggered successfully, False otherwise
def perform_mipi_dsi_transmission(gfx_index, target_id, dsi_buffer_transmission):
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_uint, ctypes.c_uint,
                                  ctypes.POINTER(mipi_dsi_dcs_args.DXGK_DSI_TRANSMISSION))
    func = prototype(('GfxValSimPerformMIPIDSITransmission', gfxValSimDLL))

    status = func(ctypes.byref(adapter_info), ctypes.sizeof(GfxAdapterInfo), target_id,
                  ctypes.byref(dsi_buffer_transmission))
    if not status:
        logging.error("Failed to trigger MIPI DSI transmission .")

    return status
