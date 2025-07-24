########################################################################################################################
# @file             adapter_info_struct.py
# @brief            Contains the Information about Graphics Adapter, Platform Details
# @author           Amit Sau, Chandrakanth Pabolu
########################################################################################################################

import ctypes

MAX_GFX_ADAPTER = 5
MAX_DEVICE_ID_LEN = 200
CCH_DEVICE_NAME = 32


##
# @brief        Structure Definition for LUID (OS API). LUID will be 0 if Gfx Driver is in disabled state.
class LUID(ctypes.Structure):
    _fields_ = [
        ('LowPart', ctypes.c_ulong),  # [Inout] Source Adaptor ID LowPart
        ('HighPart', ctypes.c_long)  # [Inout] Source Adaptor ID HighPart
    ]

    ##
    # @brief    Overridden str method
    # @return   str - String representation of LUID Class
    def __str__(self):
        return f" LUID:Low-{self.LowPart}, High-{self.HighPart}"


##
# @brief        GUID( Globally Unique Identifier)
# @details      A GUID is a 128-bit integer (16 bytes) that can be used across all computers and networks wherever a
#               unique identifier is required. Such an identifier has a very low probability of being duplicated.
class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_short),
        ('Data3', ctypes.c_short),
        ('Data4', ctypes.c_ubyte * 8)
    ]

    ##
    # @brief        Overridden str method
    # @return       String representation of GUID class
    def __str__(self):
        return "{{{:08x}-{:04x}-{:04x}-{}-{}}}".format(
            self.Data1, self.Data2, self.Data3, ''.join(["{:02x}".format(d) for d in self.Data4[:2]]),
            ''.join(["{:02x}".format(d) for d in self.Data4[2:]]),
        )


##
# @brief        Display Adapter Caps Structure
class DisplayAdapterCaps(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('busDeviceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),
        ('adapterLUID', LUID),
        ('adapterGUID', GUID),
        ('displayLessAdapter', ctypes.c_bool),
        ('displayOnlyDriver', ctypes.c_bool),
        ('isGfxReady', ctypes.c_bool),
        ('devicePowerState', ctypes.c_ulong),
        ('powerAction', ctypes.c_ulong),
    ]

    ##
    # @brief        Overridden str Method
    # @return       String representation of DisplayAdapterCaps Class
    def __str__(self):
        return f"BusDeviceID: {self.busDeviceID}; {self.adapterLUID}; {self.adapterGUID}; displayLessAdapter: " \
               f"{self.displayLessAdapter}; DoD: {self.displayOnlyDriver}; isGfxReady: {self.isGfxReady}; " \
               f"devicePowerState: {self.devicePowerState}; powerAction: {self.powerAction}"


##
# @brief        Display Adapter Caps details
class DisplayAdapterCapsDetails(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('numAdapterCaps', ctypes.c_ulong),
        ('adapterCaps', DisplayAdapterCaps * MAX_GFX_ADAPTER)
    ]

    ##
    # @brief        Overridden str Method
    # @return       String representation of DisplayAdapterCapsDetails Class
    def __str__(self):
        data = {}
        for index in range(self.numAdapterCaps):
            data[index] = str(self.adapterCaps[index])
        return str(data)


##
# @brief        Definition for GfxAdapterInfo Information.
class GfxAdapterInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('busDeviceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),
        # Bus DeviceID (Ex: PCI\VEN_8086&DEV_0166&SUBSYS_21F917AA&REV_09\3&33FD14CA&0&10)
        ('vendorID', ctypes.c_wchar * 6),  # GFX Adapter Vendor ID
        ('deviceID', ctypes.c_wchar * 6),  # GFX Adapter Device ID
        ('deviceInstanceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),  # GFX Adapter Instance ID
        ('gfxIndex', ctypes.c_wchar * 6),  # GFX Adapter Index Value (Ex: gfx_0)
        ('isActive', ctypes.c_bool),  # GFX Adapter is Active ( Driver Enabled )  or Not ( Driver Disabled)
        ('adapterLUID', LUID)  # GFX Adapter LUID information
    ]

    ##
    # @brief        Overridden str method
    # @return       String representation of GfxAdapterInfo Class
    def __str__(self):
        return f"GfxAdapterInfo - Index: {self.gfxIndex}, Platform: {self.get_platform_info().PlatformName}, " \
               f"IsActive: {self.isActive}, Bus: {str(self.busDeviceID)}, Vendor: {str(self.vendorID)}, " \
               f"Device: {str(self.deviceID)}, DeviceInstance: {str(self.deviceInstanceID)}, {self.adapterLUID}"

    ##
    # @brief       Get Platform Information.
    # @return      dict - Returns the Platform details.
    def get_platform_info(self):
        from Libs.Core.machine_info.machine_info import SystemInfo
        return SystemInfo().get_platform_details(self.deviceID)

    ##
    # @brief        String representation of GfxAdapterInfo class
    # @return       str - Returns adapter info details
    def to_string(self):
        return (" " + str(self.gfxIndex) + " " + self.get_platform_info().PlatformName +
                " vendor id: " + str(self.vendorID) + " device id: " + str(self.deviceID) +
                " device instance id: " + str(self.deviceInstanceID) + str(self.adapterLUID))


##
# @brief        Structure Definition for GfxAdapterDetails Information.
class GfxAdapterDetails(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('size', ctypes.c_uint),
        ('numDisplayAdapter', ctypes.c_uint),
        ('adapterInfo', GfxAdapterInfo * MAX_GFX_ADAPTER),
        ('status', ctypes.c_uint)
    ]

    ##
    # @brief        Get Adapter Information.
    # @param[in]    gfx_index - Graphics adapter info
    # @return       adapter_info - Returns the Adapter Information.
    def get_adapter_info(self, gfx_index):
        adapter_info = None
        gfx_index = gfx_index.lower().strip()
        for adapter_index in range(self.numDisplayAdapter):
            if self.adapterInfo[adapter_index].gfxIndex == gfx_index:
                return self.adapterInfo[adapter_index]
        return adapter_info


##
# @brief        Structure to store Display adapters' BDF information in current environment
class BdfInfo(ctypes.Structure):
    _fields_ = [
        ('bus', ctypes.c_uint),
        ('device', ctypes.c_uint),
        ('function', ctypes.c_uint),
        ('busDeviceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),
        ('isActive', ctypes.c_bool)
    ]

    ##
    # @brief        Overridden str method
    # @return       String representation of BdfInfo Class
    def __str__(self):
        return f"{self.bus}:{self.device}:{self.function}"
