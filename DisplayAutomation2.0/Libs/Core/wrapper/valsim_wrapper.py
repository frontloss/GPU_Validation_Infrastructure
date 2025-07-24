########################################################################################################################
# @file         valsim_wrapper.py
# @brief        Contains wrapper functions calling Val-Sim CDLL exposed APIs.
# @author       Pabolu, Chandrakanth, Amit Sau
########################################################################################################################


import ctypes
import logging
import os
from ctypes.wintypes import HANDLE

from Libs.Core.Verifier import dispdiag_verification_args
from Libs.Core.display_config import adapter_info_struct
from Libs.Core.sw_sim import dpcd_model_data_struct
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import valsim_args

_valsim_dll = None


##
# @brief        Val-Sim Load Library.
# @return       None
def load_library():
    global _valsim_dll
    try:
        _valsim_dll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'GfxValSim.dll'))
    except IOError as error:
        logging.error("Unable to load GfxValSim DLL! Error : {0}".format(error))


##
# @brief            Private Function to initialize requested ports.
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port_list - Ports to be initialized EFPs or LFPs
# @param[in]        is_lfp port - True if its LFP port, False if its EFP port
# @return           bool - True on Success, False otherwise
def __init_ports(gfx_adapter_info, port_list, is_lfp=False):
    port_number_list = []
    sink_type_list = []
    no_of_ports = len(port_list)
    if no_of_ports == 0:
        return False
    for index, port in enumerate(port_list):
        port_number_list.insert(index, getattr(valsim_args.ValSimPort, port_list[index]).value)
        if port_list[index].startswith('DP_'):
            sink_type_list.insert(index, valsim_args.ValSimSink.DP.value)
        elif port_list[index].startswith('HDMI_'):
            sink_type_list.insert(index, valsim_args.ValSimSink.HDMI.value)
        else:
            sink_type_list.insert(index, valsim_args.ValSimSink.INVALID.value)

    port_list = (ctypes.c_uint * no_of_ports)()
    sink_list = (ctypes.c_uint * no_of_ports)()
    lfp_list = (ctypes.c_bool * no_of_ports)()

    for index, port in enumerate(port_number_list):
        port_list[index] = port_number_list[index]
        sink_list[index] = sink_type_list[index]
        lfp_list[index] = is_lfp

    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.c_uint * no_of_ports, ctypes.c_uint * no_of_ports,
                                  ctypes.c_bool * no_of_ports)
    func = prototype(('InitAllPorts', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  no_of_ports, port_list, sink_list, lfp_list)

    return True if status == 0 else False


##
# @brief        Wrapper API to initialize Gfx val simulation driver.
# @return       HANDLE - Valsim handle
def init_gfx_val_sim():
    prototype = ctypes.PYFUNCTYPE(HANDLE)
    func = prototype(('GetGfxValSimHandle', _valsim_dll))
    return func()


##
# @brief        Wrapper API to initialize all the efp ports.
# @param[in]    gfx_adapter_info - Graphics Adapter Info
# @param[in]    efp_ports - list of EFP Ports
# @return       ports - True on Success, False otherwise.
def init_efp_ports(gfx_adapter_info, efp_ports):
    return __init_ports(gfx_adapter_info, efp_ports, False)


##
# @brief            Wrapper API to initialize all the lfp ports.
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        lfp_ports list - list of LFP Ports
# @return           bool - True on Success False otherwise.
def init_lfp_ports(gfx_adapter_info, lfp_ports):
    return __init_ports(gfx_adapter_info, lfp_ports, True)


##
# @brief            Wrapper API to simulate plug
# @param[in]        gfx_adapter_info - Graphics Adapter Index
# @param[in]        port - connector port name
# @param[in]        edid_path - EDID File path
# @param[in]        dpcd_path - DPCD File Path
# @param[in]        is_low_power - specify plug request on low power state or not
# @param[in]        port_type - connector port type
# @param[in]        is_lfp - True if its LFP port, False if its EFP port
# @param[in]        dp_dpcd_model_data - DPCD Model Data
# @param[in]        dongle_type - Specifies Type of Dongle
# @return           bool - True on Success otherwise return False
def plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type, is_lfp, dp_dpcd_model_data,
         dongle_type):
    connector_type = 'NATIVE' if port_type == 'PLUS' else port_type
    port_num = getattr(valsim_args.ValSimPort, port).value
    port_phy_type = getattr(valsim_args.PortPhyType, connector_type).value
    if dpcd_path is not None:
        dpcd_path = dpcd_path.encode()
    if edid_path is not None:
        edid_path = edid_path.encode()
    if dongle_type is None:
        dongle_type = valsim_args.DongleType.Default

    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo),
                                  ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_char_p,
                                  ctypes.POINTER(dpcd_model_data_struct.DPDPCDModelData),
                                  ctypes.c_bool, ctypes.c_uint, ctypes.c_bool, ctypes.c_uint)
    func = prototype(('Plug', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  port_num, edid_path, dpcd_path,
                  ctypes.byref(dp_dpcd_model_data) if dp_dpcd_model_data is not None else None,
                  is_low_power, port_phy_type, is_lfp, dongle_type)
    return True if status == 0 else False


##
# @brief            Wrapper API to simulate unplug
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port - connector port name
# @param[in]        is_low_power - specify unplug request on low power state or not
# @param[in]        port_type - connector port type
# @return           bool - True on Success otherwise return False
def unplug(gfx_adapter_info, port, is_low_power=False, port_type='NATIVE'):
    connector_type = 'NATIVE' if port_type == 'PLUS' else port_type
    port_num = getattr(valsim_args.ValSimPort, port).value
    port_phy_type = getattr(valsim_args.PortPhyType, connector_type).value
    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.c_bool, ctypes.c_uint)
    func = prototype(('UnPlug', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  port_num, is_low_power, port_phy_type)
    return True if status == 0 else False


##
# @brief            Wrapper API to simulate plug/unplug
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port - connector port name
# @param[in]        attach_detach - flag to specify request type as attach or detach
# @param[in]        port_type - connector port type
# @return           bool - True on Success, False otherwise
def set_hpd(gfx_adapter_info, port, attach_detach, port_type):
    connector_type = 'NATIVE' if port_type == 'PLUS' else port_type
    port_num = getattr(valsim_args.ValSimPort, port).value
    port_phy_type = getattr(valsim_args.PortPhyType, connector_type).value
    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.c_bool, ctypes.c_uint)
    func = prototype(('SetHPDInterrupt', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  port_num, attach_detach, port_phy_type)
    return True if status == 0 else False


##
# @brief            Wrapper API to simulate hpd interrupt
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port - connector port name
# @param[in]        attach_detach - flag to specify request type as attach or detach
# @param[in]        port_type - connector port type
# @return           bool - True on Success, False otherwise
def trigger_interrupt(gfx_adapter_info, port, attach_detach, port_type):
    connector_type = 'NATIVE' if port_type == 'PLUS' else port_type
    port_num = getattr(valsim_args.ValSimPort, port).value
    port_phy_type = getattr(valsim_args.PortPhyType, connector_type).value
    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.c_bool, ctypes.c_uint)
    func = prototype(('TriggerHPDInterrupt', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  port_num, attach_detach, port_phy_type)
    return True if status == 0 else False


##
# @brief            Wrapper API to Acquire or release wakelock
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        acquire_release - flag to specify request type as wakelock acquire or release
# @return           bool - True on Success, False otherwise
def Handle_Wakelock(gfx_adapter_info, acquire_release):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint, ctypes.c_bool)
    func = prototype(('ValSimWakeLockAccess', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo), acquire_release)
    return status


##
# @brief            Wrapper API to generate MIPI TE
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port - connector port name
# @return           bool - True on Success otherwise return False
def generate_mipi_te(gfx_adapter_info, port):
    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint)
    func = prototype(('SetTEInterrupt', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo), port)
    return True if status == 0 else False


##
# @brief            Wrapper API to read display MMIO register.
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        offset - Offset value in Hex.
# @return           out_buffer - MMIO offset value if read successful, None otherwise
def read_mmio(gfx_adapter_info, offset):
    out_buffer = ctypes.c_ulong()
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong))
    func = prototype(('ValSimReadMMIO', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  offset, ctypes.byref(out_buffer))
    return out_buffer.value if status is True else None


##
# @brief            Wrapper API to write display MMIO register
# @param[in]        gfx_adapter_info -Graphics Adapter Index
# @param[in]        offset register - offset in Hex.
# @param[in]        value - in Hex.
# @return -         status - True on MMIO Write Success, False otherwise
def write_mmio(gfx_adapter_info, offset, value):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool,
                                  ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_ulong, ctypes.c_ulong)
    func = prototype(('ValSimWriteMMIO', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  offset, value)
    return status


##
# @brief            API to Perform Valsim IOCTL Call
# @param[in]        gfx_adapter_info - Graphics Adapter Index
# @param[in]        ioctl_code - IOCTL call to be performed
# @param[in]        buffer - associated buffer for the ioctl code.
# @return           status - True if IOCTL call is successful, False otherwise
def perform_ioctl_call(gfx_adapter_info, ioctl_code, buffer):
    # ToDo: Temporary WA to handle display adapter caps before dll modules are loaded
    if _valsim_dll is None or buffer is None or ioctl_code is None:
        return False
    # WA: Currently, output buffer is not used from python, so passing a dummy buffer to Exposed API.
    # When required, move the implementation of out_buffer to test/libs side appropriately.
    out_buffer_size = 0
    out_buffer = ctypes.c_void_p(0)

    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.POINTER(type(buffer)), ctypes.c_uint, ctypes.c_void_p,
                                  ctypes.c_uint)
    func = prototype(('ValsimIoctlCall', _valsim_dll))

    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo), ioctl_code,
                  ctypes.byref(buffer), ctypes.sizeof(type(buffer)), ctypes.byref(out_buffer), out_buffer_size)

    return status


##
# @brief            API to Get Driver WA Table data
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        driver_wa - Driver WA operation
# @return           (status, data) - (True on Success otherwise return False, DriverWA Data)
def get_driver_wa_table(gfx_adapter_info: adapter_info_struct.GfxAdapterInfo, driver_wa: int):
    data = ctypes.c_uint()
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_int, ctypes.POINTER(ctypes.c_uint))
    func = prototype(('GetDriverWATable', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo), driver_wa,
                  ctypes.byref(data))
    return status, data.value


##
# @brief            Wrapper API to Get Display NonIntrusive Data
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        dispdiagdata - DisplayStateNonIntrusive object
# @return           status - True on Success, False otherwise
def get_display_nonintrusivedata(gfx_adapter_info: adapter_info_struct.GfxAdapterInfo,
                                 dispdiagdata: dispdiag_verification_args.DisplayStateNonIntrusive):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.POINTER(dispdiag_verification_args.DisplayStateNonIntrusive))
    func = prototype(('GfxValSimGetDisplayNonIntrusiveData', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  ctypes.byref(dispdiagdata))
    return status

##
# @brief            Wrapper API to Get Display Intrusive Data - DisplayScanoutState data
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        dispdiagdata - DisplayStateIntrusive object
# @return           status - True on Success, False otherwise
def get_display_intrusivedata(gfx_adapter_info: adapter_info_struct.GfxAdapterInfo,
                                 dispdiagdata: dispdiag_verification_args.DisplayStateIntrusive):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.POINTER(dispdiag_verification_args.DisplayStateIntrusive))
    func = prototype(('GfxValSimGetDisplayIntrusiveData', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo),
                  ctypes.byref(dispdiagdata))
    return status


##
# @brief        Wrapper API to close handle of GfxValSim
# @return       bool - True on success, False otherwise
def close_gfx_val_simulator():
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
    func = prototype(('CloseGfxValSimHandle', _valsim_dll))
    status = func()
    return True if status == 1 else False


##
# @brief            Wrapper API to write Panel DPCD
# @param[in]        gfx_adapter_info -Graphics Adapter Info
# @param[in]        port - Port Enum.
# @param[in]        offset register - offset in Hex.
# @param[in]        value - in Hex.
# @return -         status - True on DPCD Write Success, False otherwise
def set_panel_dpcd(gfx_adapter_info, port, offset, value):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint16, ctypes.c_uint8)
    func = prototype(('ValSimDpcdWrite', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), port, offset, value)
    return True if status == 0 else False


##
# @brief            Wrapper API to simulate SCDC interrupt
# @param[in]        gfx_adapter_info - Graphics Adapter Info
# @param[in]        port - connector port
# @param[in]        scdc_failure_type - flag to specify request type
# @return           bool - True on Success, False otherwise
def trigger_scdc_interrupt(gfx_adapter_info: adapter_info_struct.GfxAdapterInfo, port: str,
                           scdc_failure_type: valsim_args.SpiEventType) -> bool:
    port_num = getattr(valsim_args.ValSimPort, port).value
    prototype = ctypes.PYFUNCTYPE(ctypes.HRESULT, ctypes.POINTER(adapter_info_struct.GfxAdapterInfo), ctypes.c_uint,
                                  ctypes.c_uint, ctypes.c_uint)
    func = prototype(('TriggerSCDCInterrupt', _valsim_dll))
    status = func(ctypes.byref(gfx_adapter_info), ctypes.sizeof(adapter_info_struct.GfxAdapterInfo), port_num,
                  scdc_failure_type)
    return True if status == 0 else False
