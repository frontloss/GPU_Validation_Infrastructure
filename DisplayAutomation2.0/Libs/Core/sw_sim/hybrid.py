######################################################################################
# @file     hybrid.py
# @brief    Python wrapper helper to Simulate displays and MMIO Access
# @author   Chandrakanth Pabolu
######################################################################################
import logging
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.hw_emu import she_utility as hwemu


##
# @brief        Helper function to return the IO_PORT of SHE2.0 corresponding to physical ports.
# @param[in]    connector_port - connector port type
# @return       dict - IO_PORT of SHE2.0
#               Note: This mapping is not yet finalized. It might need to be changed based on platform.
def __she_display_id(connector_port):
    return {'B': 1,
            'C': 2,
            'D': 3,
            'E': 9,
            'F': 10,
            'G': 11,
            'H': 12,
            }[connector_port]


##
# @brief        Helper function to Plug display in hybrid mode(SHE + Valsim)
# @param[in]    gfx_adapter_info - Graphics Adapter Information
# @param[in]    port - connector port
# @param[in]    edid_path - EDID file Path
# @param[in]    dpcd_path - DPCD file Path
# @param[in]    is_low_power - True if Low Power State, False otherwise
# @param[in]    port_type - connector port type
# @param[in]    is_lfp - True if LFP , False otherwise
# @return       bool - True if plug Successful, False otherwise
def hybrid_plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type='NATIVE', is_lfp=False):
    she_utility = hwemu.SHE_UTILITY()
    if (she_utility.intialize() != 2):
        logging.error("SHE 2.0 HYBRID not connected.")
        return False
    status = gfxvalsim.GfxValSim()._plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type, is_lfp,
                                         None, None)
    if status is False:
        logging.error("gfxvalsim_plug() failed in hybrid mode.")
        return False
    return she_utility.hot_plug_unplug(__she_display_id(port[-1:]), True, 0)


##
# @brief        Helper function to UnPlug display in hybrid mode(SHE + Valsim)
# @param[in]    gfx_adapter_info - Graphics Adapter Information
# @param[in]    port - connector port
# @param[in]    is_low_power - True if Low Power State, False otherwise
# @param[in]    port_type - connector port type
# @return       bool - True if unplug successful, False otherwise
def hybrid_unplug(gfx_adapter_info, port, is_low_power, port_type='NATIVE'):
    she_utility = hwemu.SHE_UTILITY()
    if (she_utility.intialize() != 2):
        logging.error("SHE 2.0 HYBRID not connected.")
        return False
    status = gfxvalsim.GfxValSim()._unplug(gfx_adapter_info, port, is_low_power, port_type)
    if status is False:
        logging.error("gfxvalsim_unplug() failed in hybrid mode.")
        return False
    return she_utility.hot_unplug(__she_display_id(port[-1:]), False, 0)
