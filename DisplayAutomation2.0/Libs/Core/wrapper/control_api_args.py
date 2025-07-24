########################################################################################################################
# @file         control_api_args.py
# @brief        Module contains Control Library Args, Constants, Structure and Enums calling CDLL API's
# @author       Prateek Joshi
########################################################################################################################

import ctypes
from enum import Enum, IntEnum

##
# @brief API major version of this implementation (New features)
CTL_IMPL_MAJOR_VERSION = 1

##
# @brief API minor version of this implementation (Enhancements and Bug-fixes)
CTL_IMPL_MINOR_VERSION = 0

##
# @brief Maximum IPC handle size
CTL_MAX_DEVICE_NAME_LEN = 100

##
# @brief Aux Maximum data size
CTL_AUX_MAX_DATA_SIZE = 132

##
# @brief I2C Maximum data size
CTL_I2C_MAX_DATA_SIZE = 0x0080

##
# @brief Max Samples per channel
CTL_MAX_NUM_SAMPLES_PER_CHANNEL_1D_LUT = 8192

##
# @brief Maximum reserved size for future members.
CTL_MAX_RESERVED_SIZE = 124

##
# @brief Maximum EDID block.
MAX_EDID_BLOCK = 8

##
# @brief EDID block size.
EDID_BLOCK_SIZE = 128


##
# @brief            Function to get CTL_MAKE_VERSION
# @param[in]        _major - Major version
# @param[in]        _minor - Minor version
# @return           version - CTL_MAKE_VERSION
def CTL_MAKE_VERSION(_major, _minor):
    return (_major << 16) | (_minor & 0x0000ffff)


##
# @brief            Function to get CTL_MAJOR_VERSION
# @param[in]        _ver - Version
# @return           version - CTL_MAJOR_VERSION
def CTL_MAJOR_VERSION(_ver):
    return _ver >> 16


##
# @brief            Function to get CTL_MINOR_VERSION
# @param[in]        _ver - Version
# @return           version - CTL_MINOR_VERSION
def CTL_MINOR_VERSION(_ver):
    return _ver & 0x0000ffff


##
# @brief            Function to get CTL_BIT
# @param[in]        _i - Bit input
# @return           value - Bit value
def CTL_BIT(_i):
    return 1 << _i


##
# @brief CTL_IMPL_VERSION
CTL_IMPL_VERSION = CTL_MAKE_VERSION(CTL_IMPL_MAJOR_VERSION, CTL_IMPL_MINOR_VERSION)


##
# @brief Defines Return/Error codes. Bit30 indicates error.
# All generic error codes are between 0x40000000-0x4000FFFF.
# All 3D specific ones are between 0x60000000-0x6000FFFF.
# All media specific ones are between 0x50000000-0x5000FFFF.
# All display specific ones are between 0x48000000-0x4800FFFF
class ctl_result(Enum):
    SUCCESS = 0                                                 # success
    ERROR_GENERIC_START = 0x40000000                            # Generic error code starting value
    ERROR_NOT_INITIALIZED = 0x40000001                          # Result not initialized
    ERROR_ALREADY_INITIALIZED = 0x40000002                      # Already initialized
    ERROR_DEVICE_LOST = 0x40000003                              # Device hung/reset/removed/driver update occurred
    ERROR_OUT_OF_HOST_MEMORY = 0x40000004                       # Insufficient host memory to satisfy call
    ERROR_OUT_OF_DEVICE_MEMORY = 0x40000005                     # Insufficient device memory to satisfy call
    ERROR_INSUFFICIENT_PERMISSIONS = 0x40000006                 # Access denied due to permission level
    ERROR_NOT_AVAILABLE = 0x40000007                            # Resource was removed
    ERROR_UNINITIALIZED = 0x40000008                            # Library not initialized
    ERROR_UNSUPPORTED_VERSION = 0x40000009                      # Generic error code for unsupported versions
    ERROR_UNSUPPORTED_FEATURE = 0x4000000a                      # Generic error code for unsupported features
    ERROR_INVALID_ARGUMENT = 0x4000000b                         # Generic error code for invalid arguments
    ERROR_INVALID_API_HANDLE = 0x4000000c                       # API handle in invalid
    ERROR_INVALID_NULL_HANDLE = 0x4000000d                      # Handle argument is not valid
    ERROR_INVALID_NULL_POINTER = 0x4000000e                     # Pointer argument may not be nullptr
    ERROR_INVALID_SIZE = 0x4000000f                             # Size argument is invalid
    ERROR_UNSUPPORTED_SIZE = 0x40000010                         # Size argument is not supported by the device
    ERROR_UNSUPPORTED_IMAGE_FORMAT = 0x40000011                 # Image format is not supported by the device
    ERROR_DATA_READ = 0x40000012                                # Data read error
    ERROR_DATA_WRITE = 0x40000013                               # Data write error
    ERROR_DATA_NOT_FOUND = 0x40000014                           # Data not found error
    ERROR_NOT_IMPLEMENTED = 0x40000015                          # Function not implemented
    ERROR_OS_CALL = 0x40000016                                  # Operating system call failure
    ERROR_KMD_CALL = 0x40000017                                 # Kernel mode driver call failure
    ERROR_UNLOAD = 0x40000018                                   # Library unload failure
    ERROR_ZE_LOADER = 0x40000019                                # Level0 loader not found
    ERROR_INVALID_OPERATION_TYPE = 0x4000001a                   # Invalid operation type
    ERROR_NULL_OS_INTERFACE = 0x4000001b                        # Null OS interface
    ERROR_NULL_OS_ADAPATER_HANDLE = 0x4000001c                  # Null OS adapter handle
    ERROR_NULL_OS_DISPLAY_OUTPUT_HANDLE = 0x4000001d            # Null display output handle
    ERROR_WAIT_TIMEOUT = 0x4000001e                             # Timeout in Wait function
    ERROR_PERSISTANCE_NOT_SUPPORTED = 0x4000001f                # Persistence not supported
    ERROR_PLATFORM_NOT_SUPPORTED = 0x40000020                   # Platform not supported
    ERROR_UNKNOWN_APPLICATION_UID = 0x40000021                  # Unknown Application UID in Initialization call
    ERROR_INVALID_ENUMERATION = 0x40000022                      # The enum is not valid
    ERROR_FILE_DELETE = 0x40000023                              # Error in file delete operation
    ERROR_UNKNOWN = 0x4000FFFF                                  # Unknown or internal error
    ERROR_GENERIC_END = 0x4000FFFF                              # Generic error code end value
    ERROR_3D_START = 0x60000000                                 # 3D error code starting value
    ERROR_3D_END = 0x6000FFFF                                   # 3D error code end value
    ERROR_MEDIA_START = 0x50000000                              # Media error code starting value
    ERROR_MEDIA_END = 0x5000FFFF                                # Media error code end value
    ERROR_DISPLAY_START = 0x48000000                            # Display error code starting value
    ERROR_INVALID_AUX_ACCESS_FLAG = 0x48000001                  # Invalid flag for Aux access
    ERROR_INVALID_SHARPNESS_FILTER_FLAG = 0x48000002            # Invalid flag for Sharpness
    ERROR_DISPLAY_NOT_ATTACHED = 0x48000003                     # Error for Display not attached
    ERROR_DISPLAY_NOT_ACTIVE = 0x48000004                       # Error for display attached but not active
    ERROR_INVALID_POWERFEATURE_OPTIMIZATION_FLAG = 0x48000005   # Error for invalid power optimization flag
    ERROR_INVALID_POWERSOURCE_TYPE_FOR_DPST = 0x48000006        # DPST is supported only in DC Mode
    ERROR_INVALID_PIXTX_GET_CONFIG_QUERY_TYPE = 0x48000007      # Invalid query type for get pixel transformation get
    ERROR_INVALID_PIXTX_SET_CONFIG_OPERATION_TYPE = 0x48000008  # Invalid operation type for set pixel transformation
    ERROR_INVALID_SET_CONFIG_NUMBER_OF_SAMPLES = 0x48000009     # Invalid number of samples for set pixel transformation
    ERROR_INVALID_PIXTX_BLOCK_ID = 0x4800000a                   # Invalid block id for pixel transformation
    ERROR_INSUFFICIENT_PIXTX_BLOCK_CONFIG_MEMORY = 0x4800000b   # Insufficient memory allocated for BlockConfigs
    ERROR_3DLUT_INVALID_PIPE = 0x4800000c                       # Invalid pipe for 3DLUT
    ERROR_3DLUT_INVALID_DATA = 0x4800000d                       # Invalid 3DLUT data
    ERROR_3DLUT_NOT_SUPPORTED_IN_HDR = 0x4800000e               # 3DLUT not supported in HDR
    ERROR_3DLUT_INVALID_OPERATION = 0x4800000f                  # Invalid 3DLUT operation
    ERROR_3DLUT_UNSUCCESSFUL = 0x48000010                       # 3DLUT call unsuccessful
    ERROR_DISPLAY_END = 0x4800FFFF                              # Display error code end value


##
# @brief Application Unique ID
class ctl_application_id_t(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_uint32),  # [in] Data1
        ("Data2", ctypes.c_uint16),  # [in] Data2
        ("Data3", ctypes.c_uint16),  # [in] Data3
        ("Data4", ctypes.c_uint8 * 8)  # [in] Data4
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Data1 = 0
        self.Data2 = 0
        self.Data3 = 0
        for index in range(0, 8):
            self.Data4[index] = 0

    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @param[in]    data1 - GUID ID
    # @param[in]    data2 - GUID ID
    # @param[in]    data3 - GUID ID
    # @param[in]    data4 - GUID ID
    def __init__(self, data1, data2, data3, data4):
        self.Data1 = data1
        self.Data2 = data2
        self.Data3 = data3
        for index in range(0, 8):
            self.Data4[index] = data4[index]


##
# @brief CTL INIT Args Class
class ctl_init_args(ctypes.Structure):
    _fields_ = [
        ('Size', ctypes.c_uint32),
        ('Version', ctypes.c_uint8),
        ('AppVersion', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('SupportedVersion', ctypes.c_uint32),
        ("ApplicationUID", ctl_application_id_t)
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.AppVersion = CTL_MAKE_VERSION(CTL_IMPL_MAJOR_VERSION, CTL_IMPL_MINOR_VERSION)
        self.flags = 0
        self.SupportedVersion = 0
        self.ApplicationUID = \
            ctl_application_id_t(0x372464b5, 0xd1b4, 0x419d, [0x82, 0xe7, 0xef, 0xe5, 0x1b, 0x84, 0xfd, 0x8b])

    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @param[in]    app_version - App version
    # @param[in]    application_uid - App UID
    def __init__(self, app_version=None, application_uid=None):
        self.Size = 0
        self.Version = 0
        self.AppVersion = app_version if app_version is not None else \
            CTL_MAKE_VERSION(CTL_IMPL_MAJOR_VERSION, CTL_IMPL_MINOR_VERSION)
        self.flags = 0
        self.SupportedVersion = 0
        self.ApplicationUID = application_uid if application_uid is not None else \
            ctl_application_id_t(application_uid[0], application_uid[1], application_uid[2], application_uid[3])


##
# @brief Supported Functions Flags
class ctl_supported_functions_flags_t(Enum):
    DISPLAY = CTL_BIT(0)  # [out] Is Display supported
    _3D = CTL_BIT(1)  # [out] Is 3D supported
    MEDIA = CTL_BIT(2)  # [out] Is Media supported


##
# @brief Supported Functions Flags hex value
class ctl_supported_functions_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_supported_functions_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Adapter Properties
class ctl_adapter_properties_flags_v(Enum):
    INTEGRATED = CTL_BIT(0)                         # [out] Is Integrated Graphics adapter


##
# @brief Adapter Properties hex value
class ctl_adapter_properties_flags_t(ctypes.c_int):

    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_adapter_properties_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Supported Functions Flags hex value
class ctl_adapter_properties_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_supported_functions_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Firmware version
class ctl_firmware_version(ctypes.Structure):
    _fields_ = [
        ("major_version", ctypes.c_ulonglong),  # [out] Major version
        ("minor_version", ctypes.c_ulonglong),  # [out] Minor version
        ("build_number", ctypes.c_ulonglong)  # [out] Build number
    ]


##
# @brief DeviceType
class ctl_device_type_t(Enum):
    GRAPHICS = 1  # Graphics Device type
    SYSTEM = 2  # System Device type


##
# @brief DeviceType string value
class ctl_device_type(ctypes.c_int):

    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_device_type_t
    def __str__(self):
        return str(ctl_device_type_t(self.value))


##
# @brief Device Adapter properties
class ctl_device_adapter_properties(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("pDeviceID", ctypes.c_void_p),  # [in,out] OS specific Device ID
        ("device_id_size", ctypes.c_ulong),  # [in] size of the device ID
        ("device_type", ctl_device_type),  # [out] Device Type
        ("supported_subfunction_flags", ctl_supported_functions_flags),  # [out] Supported functions
        ("driver_version", ctypes.c_ulonglong),  # [out] Driver version
        ("firmware_version", ctl_firmware_version),  # [out] Firmware version
        ("pci_vendor_id", ctypes.c_ulong),  # [out] PCI Vendor ID
        ("pci_device_id", ctypes.c_ulong),  # [out] PCI Device ID
        ("rev_id", ctypes.c_ulong),  # [out] PCI Revision ID
        ("num_eus_per_sub_slice", ctypes.c_ulong),  # [out] Number of EUs per sub-slice
        ("num_sub_slices_per_slice", ctypes.c_ulong),  # [out] Number of sub-slices per slice
        ("num_slices", ctypes.c_ulong),  # [out] Number of slices
        ("name", ctypes.c_char * CTL_MAX_DEVICE_NAME_LEN),  # [out] Device name
        ("graphics_adapter_properties", ctl_adapter_properties_flags_t),  # [out] Graphics Adapter Properties
        ("reserved", ctypes.c_char * CTL_MAX_RESERVED_SIZE)  # [out] Reserved
    ]


##
# @brief Adapter LUID
class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.c_ulong),
        ("HighPart", ctypes.c_long),
    ]


##
# @brief Various display types
class ctl_display_output_types_t(Enum):
    INVALID = 0
    DISPLAYPORT = 1
    HDMI = 2
    DVI = 3
    MIPI = 4
    CRT = 5


##
# @brief Various display types string value
class ctl_display_output_types(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_display_output_types_t
    def __str__(self):
        return str(ctl_display_output_types_t(self.value))


##
# @brief Supported output bits per color (bpc) bitmasks
class ctl_output_bpc_flags_t(IntEnum):
    _6BPC = CTL_BIT(0)  # [out] Is 6bpc supported
    _8BPC = CTL_BIT(1)  # [out] Is 8bpc supported
    _10BPC = CTL_BIT(2)  # [out] Is 10bpc supported
    _12BPC = CTL_BIT(3)  # [out] Is 12bpc supported


##
# @brief Supported output bits per color (bpc) bitmasks hex value
class ctl_output_bpc_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_output_bpc_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Various standard display feature flags
class ctl_std_display_feature_flags_v(Enum):
    HDCP = CTL_BIT(0)  # [out] Is HDCP supported
    HD_AUDIO = CTL_BIT(1)  # [out] Is HD Audio supported
    PSR = CTL_BIT(2)  # [out] Is VESA PSR supported
    ADAPTIVESYNC_VRR = CTL_BIT(3)  # [out] Is VESA Adaptive Sync or HDMI VRR supported
    VESA_COMPRESSION = CTL_BIT(4)  # [out] Is display compression (VESA DSC) supported
    HDR = CTL_BIT(5)  # [out] Is HDR supported
    HDMI_QMS = CTL_BIT(6)  # [out] Is HDMI QMS supported


##
# @brief Various standard display feature flags hex value
class ctl_std_display_feature_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_std_display_feature_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Intel display feature flags
class ctl_intel_display_feature_flags_v(Enum):
    DPST = CTL_BIT(0)  # [out] Is DPST supported
    LACE = CTL_BIT(1)  # [out] Is LACE supported
    DRRS = CTL_BIT(2)  # [out] Is DRRS supported


##
# @brief Intel display feature flags
class ctl_intel_display_feature_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_intel_display_feature_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Attached display mux type
class ctl_attached_display_mux_type_v(Enum):
    NATIVE = 0  # [out] Native DP / HDMI
    THUNDERBOLT = 1  # [out] Thunderbolt
    TYPE_C = 2  # [out] USB Type C
    USB4 = 3  # [out] USB4


##
# @brief Attached display mux type string value
class ctl_attached_display_mux_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_attached_display_mux_type_v
    def __str__(self):
        return str(ctl_attached_display_mux_type_v(self.value))


##
# @brief Supported display output features
class ctl_output_feature_flags_t(Enum):
    SUPPORTS_HDCP = CTL_BIT(0)  # [out] Is HDCP supported
    SUPPORTS_AUDIO = CTL_BIT(1)  # [out] Is Audio supported
    SUPPORTS_PSR = CTL_BIT(2)  # [out] Is VESA PSR supported
    SUPPORTS_ADAPTIVESYNC = CTL_BIT(3)  # [out] Is VESA Adaptive Sync supported
    SUPPORTS_COMPRESSION = CTL_BIT(4)  # [out] Is display compression (VESA DSC) supported
    SUPPORTS_HDR10 = CTL_BIT(5)  # [out] Is HDR10 supported
    SUPPORTS_DOLBYVISION = CTL_BIT(6)  # [out] Is Dolby Vision supported


##
# @brief Supported display output features hex value
class ctl_output_feature_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_output_feature_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Signal standard type
class ctl_signal_standard_type_v(Enum):
    UNKNOWN = 0  # [out] Unknown Signal Standard
    CUSTOM = 1  # [out] Custom added timing
    DMT = 2  # [out] DMT timing
    GTF = 3  # [out] GTF Timing
    CVT = 4  # [out] CVT Timing
    CTA = 5  # [out] CTA Timing


##
# @brief Signal standard type string value
class ctl_signal_standard_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_signal_standard_type_v
    def __str__(self):
        return str(ctl_signal_standard_type_v(self.value))


##
# @brief Protocol Converter location flags
class ctl_protocol_converter_location_flags_v(Enum):
    ONBOARD = CTL_BIT(0)  # [out] OnBoard Protocol Converter
    EXTERNAL = CTL_BIT(1)  # [out] External Dongle


##
# @brief Protocol Converter location flags hex value
class ctl_protocol_converter_location_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_protocol_converter_location_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Display Output configuration related flags which indicate how the output pixel stream drive the panel
class ctl_display_config_flags_v(Enum):
    DISPLAY_ACTIVE = CTL_BIT(0)  # [out] Set if Display Active - 0: InActive 1: Active
    DISPLAY_ATTACHED = CTL_BIT(1)  # [out] Set if Display Attached - Dongle/Display/Hub to the encoder
    IS_DONGLE_CONNECTED_TO_ENCODER = CTL_BIT(2)  # [out] Set if Dongle/Hub/OnBoard protocol converter is attached
    DITHERING_ENABLED = CTL_BIT(3)  # [out] Set if Dithering is enabled on the encoder
    COMPANION_DISPLAY = CTL_BIT(9)  # [out] set if this is a companion display


##
# @brief Display Output configuration flags
class ctl_display_config_flags_t(ctypes.c_uint32):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_display_config_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Encoder configuration related flags
class ctl_encoder_config_flags_v(Enum):
    INTERNAL_DISPLAY = CTL_BIT(0)  # [out] Internal connection or not
    VESA_TILED_DISPLAY = CTL_BIT(1)  # [out] VESA DisplayID based tiled display
    TYPEC_CAPABLE = CTL_BIT(2)  # [out] This is set if encoder supports type c display
    TBT_CAPABLE = CTL_BIT(3)  # [out] This is set if encoder supports Thunderbolt display
    DITHERING_SUPPORTED = CTL_BIT(4)  # [out] This is set if encoder supports dithering
    VIRTUAL_DISPLAY = CTL_BIT(5)  # [out] This is set if virtual display
    HIDDEN_DISPLAY = CTL_BIT(6)  # [out] This is set if display is hidden from OS
    COLLAGE_DISPLAY = CTL_BIT(7)  # [out] This is set if collage display
    SPLIT_DISPLAY = CTL_BIT(8)  # [out] This is set if split display


##
# @brief Encoder configuration related flags hex value
class ctl_encoder_config_flags_t(ctypes.c_uint32):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_encoder_config_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Generic data type
class ctl_generic_void_datatype_t(ctypes.Structure):
    _fields_ = [
        ("pData", ctypes.c_void_p),  # [in,out] void pointer to memory
        ("size", ctypes.c_ulong)  # [in,out] size of the allocated memory
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.pData = None
        self.size = 0


##
# @brief Revision data type
class ctl_revision_datatype_t(ctypes.Structure):
    _fields_ = [
        ("major_version", ctypes.c_ubyte),  # [in,out] Major Version
        ("minor_version", ctypes.c_ubyte),  # [in,out] Minor Version
        ("revision_version", ctypes.c_ubyte)  # [in,out] Revision Version
    ]


##
# @brief OS specific Display identifiers
class ctl_os_display_encoder_identifier_t(ctypes.Union):
    _fields_ = [
        ("WindowsDisplayEncoderID", ctypes.c_ulong),  # [out] Windows OS Display encoder ID
        ("DisplayEncoderID", ctl_generic_void_datatype_t)  # [out] Display encoder ID for non-windows OS
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.WindowsDisplayEncoderID = 0
        self.DisplayEncoderID = ctl_generic_void_datatype_t()


##
# @brief Display Timing
class ctl_display_timing_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("PixelClock", ctypes.c_ulonglong),  # [out] Pixel Clock in Hz
        ("HActive", ctypes.c_ulong),  # [out] Horizontal Active
        ("VActive", ctypes.c_ulong),  # [out] Vertical Active
        ("HTotal", ctypes.c_ulong),  # [out] Horizontal Total
        ("VTotal", ctypes.c_ulong),  # [out] Vertical Total
        ("HBlank", ctypes.c_ulong),  # [out] Horizontal Blank
        ("VBlank", ctypes.c_ulong),  # [out] Vertical Blank
        ("HSync", ctypes.c_ulong),  # [out] Horizontal Blank
        ("VSync", ctypes.c_ulong),  # [out] Vertical Blank
        ("RefreshRate", ctypes.c_float),  # [out] Refresh Rate
        ("SignalStandard", ctl_signal_standard_type_t),  # [out] Signal Standard
        ("VicId", ctypes.c_ubyte)  # [out] VIC ID for CTA timings
    ]

    ##
    # @brief        Overridden String Method
    # @return       mode_str - String representation ctl_display_timing_t structure
    def __str__(self):
        mode_str = f" HzRes {self.HActive: <6}  VtRes {self.VActive: <6} RR {self.RefreshRate: <4} Hz Scaling ?? BPP ??"
        mode_str += f" ScanlineOrdering ?? Sampling Mode ?? PixelClock {self.PixelClock: <16} Hz"
        mode_str += f" HzTotal {self.HTotal: <6}  VtTotal {self.VTotal: <6}"
        mode_str += f" HzBlank {self.HBlank: <6}  VtBlank {self.VBlank: <6}"
        mode_str += f" HzSync {self.HSync: <6}  VtSync {self.VSync: <6}"
        mode_str += f" SignalStandard {str(self.SignalStandard): <20} VicId {self.VicId}"
        return mode_str


##
# @brief Display Properties
class ctl_display_properties_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("Os_display_encoder_handle", ctl_os_display_encoder_identifier_t),  # [out] OS specific Display ID
        ("Type", ctl_display_output_types),  # [out] Device Type from display HW
        ("AttachedDisplayMuxType", ctl_attached_display_mux_type_t),  # [out] Attached Display Mux Type
        ("ProtocolConverterOutput", ctl_display_output_types),  # [out] Protocol output type
        ("SupportedSpec", ctl_revision_datatype_t),  # [out] Supported industry spec version
        ("SupportedOutputBPCFlags", ctl_output_bpc_flags),  # [out] Supported output bits per color
        ("ProtocolConverterType", ctl_protocol_converter_location_flags_t),  # [out] Current Active Protocol Converter
        ("DisplayConfigFlags", ctl_display_config_flags_t),  # [out] Display Config Flags
        ("FeatureEnabledFlags", ctl_std_display_feature_flags_t),  # [out] Enabled Display features
        ("FeatureSupportedFlags", ctl_std_display_feature_flags_t),  # [out] Display Supported feature
        ("AdvancedFeatureEnabledFlags", ctl_intel_display_feature_flags_t),  # [out] Enabled advanced feature
        ("AdvancedFeatureSupportedFlags", ctl_intel_display_feature_flags_t),  # [out] Supported advanced feature
        ("Display_Timing_Info", ctl_display_timing_t),  # [out] Applied Timing on the Display
        ("ReservedFields", ctypes.c_ulong * 16)  # [out] Reserved field of 64 bytes
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Os_display_encoder_handle = ctl_os_display_encoder_identifier_t()
        self.Type = 0
        self.DisplayConfigFlags = 0


##
# @brief Adapter Display Encoder Properties
class ctl_adapter_display_encoder_properties_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("Os_display_encoder_handle", ctl_os_display_encoder_identifier_t),  # [out] OS specific Display ID
        ("Type", ctl_display_output_types),  # [out] Device Type from display HW
        ("IsOnBoardProtocolConverterOutputPresent", ctypes.c_bool),  # [out] Protocol output type
        ("SupportedSpec", ctl_revision_datatype_t),  # [out] Supported industry spec version
        ("SupportedOutputBPCFlags", ctl_output_bpc_flags),  # [out] Supported output bits per color
        ("EncoderConfigFlags", ctl_encoder_config_flags_t),  # [out] Output configuration flags
        ("FeatureSupportedFlags", ctl_std_display_feature_flags_t),  # [out] Adapter Supported feature flag
        ("AdvancedFeatureSupportedFlags", ctl_intel_display_feature_flags_t),  # [out] Advanced Features Supported
        ("ReservedFields", ctypes.c_ulong * 16)  # [out] Reserved field of 64 bytes
    ]


##
# @brief Property range details, a generic struct to hold min/max/step size information of various feature properties
class ctl_property_range_info(ctypes.Structure):
    _fields_ = [
        ("min_possible_value", ctypes.c_float),  # [out] Minimum possible value
        ("max_possible_value", ctypes.c_float),  # [out] Maximum possible value
        ("step_size", ctypes.c_float),  # [out] Step size possible
        ("default_value", ctypes.c_float)  # [out] Default value
    ]


##
# @brief Various sharpness filter types
class ctl_sharpness_filter_type_flags_t(Enum):
    NON_ADAPTIVE = CTL_BIT(0)  # Non-adaptive sharpness
    ADAPTIVE = CTL_BIT(1)  # Adaptive sharpness


##
# @brief Various sharpness filter value
class ctl_sharpness_filter_type_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_sharpness_filter_type_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief Sharpness filter properties
class ctl_sharpness_filter_properties(ctypes.Structure):
    _fields_ = [
        ("FilterType", ctl_sharpness_filter_type_flags),  # [out] Filter type
        ("FilterDetails", ctl_property_range_info)  # [out] Min, Max & Step size information
    ]


##
# @brief Various sharpness filter types
class ctl_sharpness_caps(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("SupportedFilterFlags", ctl_sharpness_filter_type_flags),  # [out] Supported sharpness filters
        ("NumFilterTypes", ctypes.c_ubyte),  # [out] Number of elements in filters
        ("pFilterProperty", ctypes.POINTER(ctl_sharpness_filter_properties))  # [in,out] Array of filter properties
    ]


##
# @brief Current sharpness setting
class ctl_sharpness_settings(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("Enable", ctypes.c_bool),  # [in,out] Current or new state of sharpness setting
        ("FilterType", ctl_sharpness_filter_type_flags),  # [in,out] Current or new filter to be set
        ("Intensity", ctypes.c_float)  # [in,out] Setting intensity to be applied
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Enable = 0
        self.FilterType = 0
        self.Intensity = 0


##
# @brief I2CFlags bit-masks
class ctl_i2c_flags_t(Enum):
    ATOMICI2C = CTL_BIT(0)  # Force Atomic I2C


##
# @brief I2CFlags bit-masks value
class ctl_i2c_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_i2c_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief OperationType
class ctl_operation_type(Enum):
    READ = 1  # Read operation
    WRITE = 2  # Write operation


##
# @brief I2C access arguments
class ctl_i2c_access_args(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("DataSize", ctypes.c_ulong),  # [in,out] Valid data size
        ("Address", ctypes.c_ulong),  # [in] Address to read or write
        ("OpType", ctypes.c_uint),  # [in] Operation type, 1 for Read, 2 for Write
        # For Write App needs to run with admin privileges
        ("Offset", ctypes.c_ulong),  # [in] Offset
        ("Flags", ctl_i2c_flags),  # [in] I2C Flags. Refer ::ctl_i2c_flags
        ("RAD", ctypes.c_ulonglong),  # [in] RAD, For Future use
        ("Data", ctypes.c_ubyte * CTL_I2C_MAX_DATA_SIZE)  # [in,out] Data array
    ]


##
# @brief AUX Flags bit-masks
class ctl_aux_flags_t(Enum):
    NATIVE_AUX = CTL_BIT(0)  # For Native AUX operation
    I2C_AUX = CTL_BIT(1)  # For I2C AUX operation


##
# @brief AUX Flags bit-masks value
class ctl_aux_flags(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_aux_flags_t
    def __str__(self):
        return hex(self.value)


##
# @brief AUX access arguments
class ctl_aux_access_args(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("OpType", ctypes.c_uint),  # [in] Operation type, 1 for Read, 2 for Write
        # For Write, App needs to run with admin privileges
        ("Flags", ctl_aux_flags),  # [in] Aux Flags. Refer ::ctl_aux_flags
        ("Address", ctypes.c_ulong),  # [in] Address to read or write
        ("RAD", ctypes.c_ulonglong),  # [in] RAD, For Future use
        ("PortID", ctypes.c_ulong),  # [in] Port ID, For Future use, SST Tiled Device
        ("DataSize", ctypes.c_ulong),  # [in,out] Valid data size
        ("Data", ctypes.c_ubyte * CTL_AUX_MAX_DATA_SIZE)  # [in,out] Data array
    ]


##
# @brief Panel Descriptor access arguments
class ctl_panel_descriptor_access_args_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("OpType", ctypes.c_uint),  # [in] Operation type, 1 for Read, 2 for Write
        ("BlockNumber", ctypes.c_uint32),  # [in] Block number
        ("DescriptorDataSize", ctypes.c_uint32),  # [in] Descriptor data size
        ("pDescriptorData", ctypes.POINTER(ctypes.c_uint8))  # [in,out] Panel descriptor data
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.OpType = 0
        self.BlockNumber = 0
        self.DescriptorDataSize = 0
        self.pDescriptorData = None


##
# @brief Pixel Transformation pipe set configuration flags bitmasks
class ctl_pixtx_pipe_set_config_flags_v(IntEnum):
    PERSIST_ACROSS_POWER_EVENTS = CTL_BIT(0)  # For maintaining persistence across power events


##
# @brief Pixel Transformation pipe set configuration flags bitmasks value
class ctl_pixtx_pipe_set_config_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_pixtx_pipe_set_config_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Pixel transformation block types
class ctl_pixtx_block_type_v(IntEnum):
    _1D_LUT = 1  # Block type 1D LUT
    _3D_LUT = 2  # Block type 3D LUT
    _3X3_MATRIX = 3  # Block type 3x3 matrix
    _3X3_MATRIX_AND_OFFSETS = 4  # Block type 3x3 matrix and offsets


##
# @brief Pixel transformation block types value
class ctl_pixtx_block_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_block_type_v
    def __str__(self):
        return str(ctl_pixtx_block_type_v(self.value))


##
# @brief Pixel transformation LUT sampling types
class ctl_pixtx_lut_sampling_type_v(IntEnum):
    UNIFORM = 0  # Uniform LUT sampling
    NONUNIFORM = 1  # Non uniform LUT sampling, Required mainly in HDR mode


##
# @brief Pixel transformation LUT sampling types value
class ctl_pixtx_lut_sampling_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_lut_sampling_type_v
    def __str__(self):
        return str(ctl_pixtx_lut_sampling_type_v(self.value))


##
# @brief Configuration query types
class ctl_pixtx_config_query_type_v(IntEnum):
    CAPABILITY = 0  # Get complete pixel processing pipeline capability
    CURRENT = 1  # Get the configuration set through last set call


##
# @brief Configuration query types value
class ctl_pixtx_config_query_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_config_query_type_v
    def __str__(self):
        return str(ctl_pixtx_config_query_type_v(self.value))


##
# @brief Configuration operation types
class ctl_pixtx_config_opertaion_type_v(IntEnum):
    RESTORE_DEFAULT = 1  # Restore block by block or entire pipe line
    SET_CUSTOM = 2  # Custom LUT or matrix can be set through this option.


##
# @brief Configuration operation types value
class ctl_pixtx_config_opertaion_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_config_opertaion_type_v
    def __str__(self):
        return str(ctl_pixtx_config_opertaion_type_v(self.value))


##
# @brief Pixel transformation gamma encoding types
class ctl_pixtx_gamma_encoding_type_v(IntEnum):
    SRGB = 0  # Gamma encoding SRGB
    REC709 = 1  # Gamma encoding REC709, Applicable for REC2020 as well
    ST2084 = 2  # Gamma encoding ST2084
    HLG = 3  # Gamma encoding HLG
    LINEAR = 4  # Gamma encoding linear


##
# @brief Pixel transformation gamma encoding types value
class ctl_pixtx_gamma_encoding_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_gamma_encoding_type_v
    def __str__(self):
        return str(ctl_pixtx_gamma_encoding_type_v(self.value))


##
# @brief Pixel transformation color space types
class ctl_pixtx_color_space_v(IntEnum):
    REC709 = 0  # Color space REC709
    REC2020 = 1  # Color space REC2020
    ADOBE_RGB = 2  # Color space AdobeRGB
    P3_D65 = 3  # Color space P3_D65
    P3_DCI = 4  # Color space P3_DCI
    P3_D60 = 5  # Color space P3_D60
    CUSTOM = 0xFFFF  # Color space custom


##
# @brief Pixel transformation color space types value
class ctl_pixtx_color_space_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_color_space_v
    def __str__(self):
        return str(ctl_pixtx_color_space_v(self.value))


##
# @brief Pixel transformation color model types
class ctl_pixtx_color_model_v(IntEnum):
    RGB_FR = 0  # Color model RGB full range
    RGB_LR = 1  # Color model RGB limited range
    YCBCR_422_FR = 2  # Color model YCBCR 422 full range
    YCBCR_422_LR = 3  # Color model YCBCR 422 limited range
    YCBCR_420_FR = 4  # Color model YCBCR 420 full range
    YCBCR_420_LR = 5  # Color model YCBCR 420 limited range


##
# @brief Pixel transformation color model types value
class ctl_pixtx_color_model_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_color_model_v
    def __str__(self):
        return str(ctl_pixtx_color_model_v(self.value))


##
# @brief Pixel transformation color primaries
class ctl_pixtx_color_primaries_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("xR", ctypes.c_double),  # [out] CIE1931 x value with maximum red pixel value
        ("yR", ctypes.c_double),  # [out] CIE1931 y value with maximum red pixel value
        ("xG", ctypes.c_double),  # [out] CIE1931 x value with maximum green pixel value
        ("yG", ctypes.c_double),  # [out] CIE1931 y value with maximum green pixel value
        ("xB", ctypes.c_double),  # [out] CIE1931 x value with maximum blue pixel value
        ("yB", ctypes.c_double),  # [out] CIE1931 y value with maximum blue pixel value
        ("xW", ctypes.c_double),  # [out] CIE1931 x value with maximum white pixel value
        ("yW", ctypes.c_double)  # [out] CIE1931 y value with maximum white pixel value
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.xR = 0
        self.yR = 0
        self.xG = 0
        self.yG = 0
        self.xB = 0
        self.yB = 0
        self.xW = 0
        self.yW = 0


##
# @brief Pixel transformation pixel format
class ctl_pixtx_pixel_format_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("BitsPerColor", ctypes.c_ulong),  # [out] Bits per color, 16 for FP16 case
        ("IsFloat", ctypes.c_bool),  # [out] Set if floating point encoding
        ("EncodingType", ctl_pixtx_gamma_encoding_type_t),  # [out] Encoding type
        ("ColorSpace", ctl_pixtx_color_space_t),  # [out] Color space
        ("ColorModel", ctl_pixtx_color_model_t),  # [out] Color model
        ("ColorPrimaries", ctl_pixtx_color_primaries_t),  # [out] Color primaries
        ("MaxBrightness", ctypes.c_double),  # [out] Maximum brightness of pixel values
        ("MinBrightness", ctypes.c_double)  # [out] Minimum brightness of pixel values
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.BitsPerColor = 0
        self.IsFloat = False
        self.EncodingType = -1
        self.ColorSpace = -1
        self.ColorModel = -1
        self.ColorPrimaries = ctl_pixtx_color_primaries_t()
        self.MaxBrightness = 0
        self.MinBrightness = 0


##
# @brief Pixel transformation 1D LUT configuration
class ctl_pixtx_1dlut_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("SamplingType", ctl_pixtx_lut_sampling_type_t),  # [in,out] Blocks with non-uniform sampling
        ("NumSamplesPerChannel", ctypes.c_ulong),  # [in,out] Number of samples per channel
        ("NumChannels", ctypes.c_ulong),  # [in,out] Number of channels
        ("pSampleValues", ctypes.POINTER(ctypes.c_double)),  # [in,out] Pointer to sample values
        ("pSamplePositions", ctypes.POINTER(ctypes.c_double))  # [out] LUT sampling positions
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.SamplingType = -1
        self.NumSamplesPerChannel = 0
        self.NumChannels = 0
        self.pSampleValues = None
        self.pSamplePositions = None


##
# @brief Pixel transformation matrix configuration
class ctl_pixtx_matrix_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("PreOffsets", ctypes.c_double * 3),  # [in,out] Pre offsets
        ("PostOffsets", ctypes.c_double * 3),  # [in,out] Post offsets
        ("Matrix", (ctypes.c_double * 3) * 3)  # [in,out] 3x3 Matrix
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        for index in range(0, 3):
            self.PreOffsets[index] = 0
            self.PostOffsets[index] = 0
        for row in range(0, 3):
            for column in range(0, 3):
                self.Matrix[row][column] = 0


##
# @brief Pixel transformation 3D LUT sample
class ctl_pixtx_3dlut_sample_t(ctypes.Structure):
    _fields_ = [
        ("Red", ctypes.c_double),  # [in,out] Red output value
        ("Green", ctypes.c_double),  # [in,out] Green output value
        ("Blue", ctypes.c_double)  # [in,out] Blue output value
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Red = 0
        self.Green = 0
        self.Blue = 0


##
# @brief Pixel transformation 3D LUT configuration
class ctl_pixtx_3dlut_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("NumSamplesPerChannel", ctypes.c_ulong),  # [in,out] Number of samples per channel
        ("pSampleValues", ctypes.POINTER(ctl_pixtx_3dlut_sample_t))  # [in,out] Pointer to sample values
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.NumSamplesPerChannel = 0
        self.pSampleValues = None


##
# @brief Pixel transformation configuration
class ctl_pixtx_config_t(ctypes.Union):
    _fields_ = [
        ("OneDLutConfig", ctl_pixtx_1dlut_config_t),  # [in,out] 1D LUT configuration
        ("ThreeDLutConfig", ctl_pixtx_3dlut_config_t),  # [in,out] 3D LUT configuration
        ("MatrixConfig", ctl_pixtx_matrix_config_t)  # [in,out] Matrix configuration
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.OneDLutConfig = ctl_pixtx_1dlut_config_t()
        self.ThreeDLutConfig = ctl_pixtx_3dlut_config_t()
        self.MatrixConfig = ctl_pixtx_matrix_config_t()


##
# @brief Pixel transformation block configuration
class ctl_pixtx_block_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("BlockId", ctypes.c_ulong),  # [in,out] Unique block ID
        ("BlockType", ctl_pixtx_block_type_t),  # [in,out] Block type
        ("Config", ctl_pixtx_config_t)  # [in,out] Configuration
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.BlockId = 0
        self.BlockType = ctl_pixtx_block_type_t()
        self.Config = ctl_pixtx_config_t()


##
# @brief Pixel transformation pipe get configuration
class ctl_pixtx_pipe_get_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("QueryType", ctl_pixtx_config_query_type_t),  # [in] Query operation type
        ("InputPixelFormat", ctl_pixtx_pixel_format_t),  # [out] Input pixel format
        ("OutputPixelFormat", ctl_pixtx_pixel_format_t),  # [out] Output pixel format
        ("NumBlocks", ctypes.c_ulong),  # [out] Number of blocks
        ("pBlockConfigs", ctypes.POINTER(ctl_pixtx_block_config_t))  # [out] Pointer to specific configs
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.QueryType = -1
        self.InputPixelFormat = ctl_pixtx_pixel_format_t()
        self.OutputPixelFormat = ctl_pixtx_pixel_format_t()
        self.NumBlocks = 0
        self.pBlockConfigs = None

##
# @brief Pixel transformation pipe set configuration
class ctl_pixtx_pipe_set_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("OpertaionType", ctl_pixtx_config_opertaion_type_t),  # [in] Set operation type
        ("Flags", ctl_pixtx_pipe_set_config_flags_t),  # [in] Flags
        ("NumBlocks", ctypes.c_ulong),  # [in] Number of blocks
        ("pBlockConfigs", ctypes.POINTER(ctl_pixtx_block_config_t))  # [in,out] Array of block specific configs
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.OpertaionType = 0
        self.Flags = 0
        self.NumBlocks = 0
        self.pBlockConfigs = None


##
# @brief ctl_wire_format_color_model Configuration types
class ctl_wire_format_color_model_v(IntEnum):
    BPC6 = CTL_BIT(0)
    BPC8 = CTL_BIT(1)
    BPC10 =CTL_BIT(2)
    BPC12 =CTL_BIT(3)
    BPC14 =CTL_BIT(4)
    BPC16 =CTL_BIT(5)



##
# @brief ctl_wire_format_color_model_t Configuration query types value
class ctl_wire_format_color_model_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_wire_format_color_model_t
    def __str__(self):
        return hex(self.value)


##
# @brief ctl_wire_format_color_depth_flags_v Configuration query types
class ctl_wire_format_color_depth_flags_v(IntEnum):
    RGB = 0  # Color Model RGB
    YCBCR420 = 1  # Color Model YCBCR420
    YCBCR422 = 2  # Color Model YCBCR422
    YCBCR444 = 3  # Color Model YCBCR444


##
# @brief ctl_wire_format_color_depth_flags_t Configuration query types value
class ctl_wire_format_color_depth_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_wire_format_color_depth_flags_t
    def __str__(self):
        return str(ctl_wire_format_color_depth_flags_v(self.value))


##
# @brief Configuration query types
class ctl_wire_format_operation_type_v(IntEnum):
    WIRE_FORMAT_GET = 0  # Get Request
    WIRE_FORMAT_SET = 1  # Set Request
    CTL_RESTORE_DEFAULT = 2


##
# @brief Configuration query types value
class ctl_wire_format_operation_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_wire_format_operation_type_v
    def __str__(self):
        return str(ctl_wire_format_operation_type_v(self.value))


##
# @brief ctl_wire_format_t structure Configuration
class ctl_wire_format_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),
        ("Version", ctypes.c_int8),
        ("ColorModel", ctl_wire_format_color_depth_flags_t),
        ("ColorDepth", ctl_wire_format_color_model_t),
        ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.ColorModel = 0
        self.ColorDepth = 0

##
# @brief ctl_wire_format_t structure Configuration
class ctl_get_set_wireformat(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),
        ("Version", ctypes.c_int8),
        ("Operation", ctl_wire_format_operation_type_t),
        ("SupportedWireFormat", ctl_wire_format_t * 4),
        ("WireFormat", ctl_wire_format_t),
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Operation = -1
        for index in range(0,4):
            self.SupportedWireFormat[index] = ctl_wire_format_t()
        self.WireFormat = ctl_wire_format_t()

##
# @brief Ze native kernel uuid
class ze_native_kernel_uuid_t(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int8 * 16),
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.id = 0


##
# @brief Ze device module properties
class ze_device_module_properties_t(ctypes.Structure):
    _fields_ = [
        ("stype", ctypes.c_ulong),
        ("pNext", ctypes.POINTER(ctypes.c_void_p)),
        ("spirvVersionSupported", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("fp16flags", ctypes.c_ulong),
        ("fp32flags", ctypes.c_ulong),
        ("fp64flags", ctypes.c_ulong),
        ("maxArgumentsSize", ctypes.c_ulong),
        ("printfBufferSize", ctypes.c_ulong),
        ("nativeKernelSupported", ze_native_kernel_uuid_t),
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.stype = 0
        self.pNext = 0
        self.spirvVersionSupported = 0
        self.flags = 0
        self.fp16flags = 0
        self.fp32flags = 0
        self.fp64flags = 0
        self.maxArgumentsSize = 0
        self.printfBufferSize = 0
        self.nativeKernelSupported = ze_native_kernel_uuid_t()


##
# @brief Power saving features flags
class ctl_power_optimization_flags_v(IntEnum):
    FBC = CTL_BIT(0)  # Frame buffer compression
    PSR = CTL_BIT(1)  # Panel self refresh
    DPST = CTL_BIT(2)  # Display back-light power saving technology
    LRR = CTL_BIT(3)  # Low refresh rate (LRR/ALRR/UBRR)
    LACE = CTL_BIT(4) # Lighting Aware Contrast Enhancement


##
# @brief GPU/Panel/TCON dependent power optimization technology Flags
class ctl_power_optimization_dpst_flag_t(IntEnum):
    DPST_FLAG_BKLT = CTL_BIT(0)  # Intel DPST with Backlight control
    DPST_FLAG_PANEL_CABC = CTL_BIT(1)   # Panel TCON specific Content Adaptive Control mechanism
    DPST_FLAG_OPST = CTL_BIT(2)  # Intel OLED Power Saving Technology
    DPST_FLAG_ELP = CTL_BIT(3)  # TCON based Edge Luminance Profile
    DPST_FLAG_EPSM = CTL_BIT(4)  # Extra power saving mode


##
# @brief Power saving features flags value
class ctl_power_optimization_flags_t(ctypes.c_uint32):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_power_optimization_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Power Source
class ctl_power_source_v(IntEnum):
    AC = 0  # Power Source AC
    DC = 1  # Power Source DC


##
# @brief Power Source value
class ctl_power_source_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_power_source_v
    def __str__(self):
        return str(ctl_power_source_v(self.value))


##
# @brief Power Optimization Plan
class ctl_power_optimization_plan_v(IntEnum):
    BALANCED = 0  # Balanced mode
    HIGH_PERFORMANCE = 1  # High Performance Mode
    POWER_SAVER = 2  # Power Saver Mode


##
# @brief Power Optimization Plan string
class ctl_power_optimization_plan_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_power_optimization_plan_v
    def __str__(self):
        return str(ctl_power_optimization_plan_v(self.value))


##
# @brief Type of low refresh rate feature
class ctl_power_optimization_lrr_flags_v(IntEnum):
    LRR10 = CTL_BIT(0)  # LRR 1.0
    LRR20 = CTL_BIT(1)  # LRR 2.0
    LRR25 = CTL_BIT(2)  # LRR 2.5
    ALRR = CTL_BIT(3)  # Autonomous LRR
    UBLRR = CTL_BIT(4)  # User based low refresh rate
    UBZRR = CTL_BIT(5)  # User based zero refresh rate


##
# @brief Type of low refresh rate feature value
class ctl_power_optimization_lrr_flags_t(ctypes.c_uint32):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_power_optimization_lrr_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Power optimization caps
class ctl_power_optimization_caps_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("SupportedFeatures", ctl_power_optimization_flags_t)  # [out] Supported power optimization features
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.SupportedFeatures = -1


##
# @brief LRR detailed settings
class ctl_power_optimization_lrr_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("SupportedLRRTypes", ctl_power_optimization_lrr_flags_t),  # [out] LRR type(s)
        ("CurrentLRRTypes", ctl_power_optimization_lrr_flags_t),  # [in,out] Current enabled LRR type(s)
        ("bRequirePSRDisable", ctypes.c_bool),  # [out] Require PSR disable
        ("LowRR", ctypes.c_uint16)  # [out] Lowest RR used for LRR functionality
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.SupportedLRRTypes = -1
        self.CurrentLRRTypes = -1
        self.bRequirePSRDisable = False
        self.LowRR = 0


##
# @brief PSR detailed settings
class ctl_power_optimization_psr_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("PSRVersion", ctypes.c_uint8),  # [in,out] 1 means PSR1, 2 means PSR2
        ("FullFetchUpdate", ctypes.c_bool)  # [in,out] Full fetch and update
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.PSRVersion = 0
        self.FullFetchUpdate = False


##
# @brief Type of dpst feature flags value
class ctl_power_optimization_dpst_flags_v(IntEnum):
    BKLT = CTL_BIT(0)                               # Intel DPST with Backlight control
    PANEL_CABC = CTL_BIT(1)                         # Panel TCON specific Content Adaptive Control mechanism
    OPST = CTL_BIT(2)                               # Intel OLED Power Saving Technology
    ELP = CTL_BIT(3)                                # TCON based Edge Luminance Profile
    EPSM = CTL_BIT(4)                               # Extra power saving mode
    APD = CTL_BIT(5)                                # TCON based Adaptive Pixel Dimming
    PIXOPTIX = CTL_BIT(6)                           # TCON+ based DPST like solution


##
# @brief Type of dpst feature flags value
class ctl_power_optimization_dpst_flags_t(ctypes.c_uint32):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_power_optimization_dpst_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief DPST detailed settings
class ctl_power_optimization_dpst_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("MinLevel", ctypes.c_uint8),  # [out] Maximum supported levels from 0
        ("MaxLevel", ctypes.c_uint8),  # [out] Maximum supported aggressiveness level
        ("Level", ctypes.c_uint8),  # [in,out] Current aggressiveness level to be set
        ("SupportedFeatures", ctl_power_optimization_dpst_flags_t),  # [out] Supported features
        ("EnabledFeatures", ctl_power_optimization_dpst_flags_t)  # [in,out] Features enabled or to be enabled
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.MinLevel = 0
        self.MaxLevel = 0
        self.Level = 0
        self.SupportedFeatures = ctl_power_optimization_dpst_flags_t()
        self.EnabledFeatures = ctl_power_optimization_dpst_flags_t()


##
# @brief Feature specific power optimization data
class ctl_power_optimization_feature_specific_info_t(ctypes.Union):
    _fields_ = [
        ("LRRInfo", ctl_power_optimization_lrr_t),  # [out] LRR info
        ("PSRInfo", ctl_power_optimization_psr_t),  # [in,out] PSR info
        ("DPSTInfo", ctl_power_optimization_dpst_t)  # [in,out] DPST info
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.LRRInfo = ctl_power_optimization_lrr_t()
        self.PSRInfo = ctl_power_optimization_psr_t()
        self.DPSTInfo = ctl_power_optimization_dpst_t()


##
# @brief Power optimization settings
class ctl_power_optimization_settings_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),  # [in] size of this structure
        ("Version", ctypes.c_uint8),  # [in] version of this structure
        ("PowerOptimizationPlan", ctl_power_optimization_plan_t),  # [in] Power optimization power plan
        ("PowerOptimizationFeature", ctl_power_optimization_flags_t),  # [in] Power optimization feature
        ("Enable", ctypes.c_bool),  # [in,out] Enable state
        ("FeatureSpecificData", ctl_power_optimization_feature_specific_info_t),  # [in,out] Feature specific Data
        ("PowerSource", ctl_power_source_t)  # [in] AC/DC
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.PowerOptimizationPlan = -1
        self.PowerOptimizationFeature = 0
        self.Enable = False
        self.FeatureSpecificData = ctl_power_optimization_feature_specific_info_t()
        self.PowerSource = -1


##
# @brief  Retro Scaling Types
class ctl_retro_scaling_type_flags_v(IntEnum):
    INTEGER = CTL_BIT(0)                            # Integer Scaling
    NEAREST_NEIGHBOUR = CTL_BIT(1)                  # Nearest Neighbour Scaling


##
# @brief  Retro Scaling Types
class ctl_retro_scaling_type_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_retro_scaling_type_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Set/Get Retro Scaling Type
class ctl_retro_scaling_settings_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                                       # [in] size of this structure
        ("Version", ctypes.c_ubyte),                                    # [in] version of this structure
        ("Get", ctypes.c_bool),                                         # [in][release] True to get current scaling, False to Set
        ("Enable", ctypes.c_bool),                                      # [in,out] State of the scaler
        ("RetroScalingType", ctl_retro_scaling_type_flags_t)            # [out] Requested retro scaling types. Refer
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Get = False
        self.Enable = False
        self.RetroScalingType = ctl_retro_scaling_type_flags_v.NEAREST_NEIGHBOUR.value


##
# @brief Retro Scaling caps
class ctl_retro_scaling_caps_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                                       # [in] size of this structure
        ("Version", ctypes.c_ubyte),                                    # [in] version of this structure
        ("SupportedRetroScaling", ctl_retro_scaling_type_flags_t)       # [out] Supported retro scaling types
    ]


##
# @brief Scaling Types
class ctl_scaling_type_flags_v(IntEnum):
    IDENTITY = CTL_BIT(0)                           # No scaling is applied and display manages scaling itself
    CENTERED = CTL_BIT(1)                           # Source is not scaled but place in the center of the target display
    STRETCHED = CTL_BIT(2)                          # Source is stretched to fit the target size
    ASPECT_RATIO_CENTERED_MAX = CTL_BIT(3)          # The aspect ratio is maintained with the source centered
    CUSTOM = CTL_BIT(4)                             # None of the standard types match this


##
# @brief Scaling Types
class ctl_scaling_type_flags_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_scaling_type_flags_v
    def __str__(self):
        return hex(self.value)


##
# @brief Scaling caps
class ctl_scaling_caps_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                         # [in] size of this structure
        ("Version", ctypes.c_ubyte),                      # [in] version of this structure
        ("SupportedScaling", ctl_scaling_type_flags_t)    # [out] Supported scaling types
    ]


##
# @brief Set/Get Scaling type
class ctl_scaling_settings_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                          # [in] size of this structure
        ("Version", ctypes.c_ubyte),                       # [in] version of this structure
        ("Enable", ctypes.c_bool),                         # [in,out] State of the scaler
        ("ScalingType", ctl_scaling_type_flags_t),         # [in,out] Requested scaling types.
        ("CustomScalingX", ctypes.c_ulong),                # [in,out] Custom Scaling X resolution
        ("CustomScalingY", ctypes.c_ulong),                # [in,out] Custom Scaling Y resolution
        ("HardwareModeSet", ctypes.c_bool),                # [in] Flag to indicate hardware modeset to apply the scaling
        ("PreferredScalingType", ctl_scaling_type_flags_t) # [out] Indicates OS persisted scaling type
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Enable = False
        self.ScalingType = ctl_scaling_type_flags_v.IDENTITY.value
        self.CustomScalingX = 0
        self.CustomScalingY = 0
        self.HardwareModeSet = False
        self.PreferredScalingType = 0


##
# @brief Endurance Gaming control possible
class ctl_3d_endurance_gaming_control_v(IntEnum):
    TURN_OFF = 0    # Endurance Gaming disable
    TURN_ON = 1     # Endurance Gaming enable
    AUTO = 2        # Endurance Gaming auto


##
# @brief Endurance Gaming control possible
class ctl_3d_endurance_gaming_control_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_3d_endurance_gaming_control_v
    def __str__(self):
        return str(ctl_3d_endurance_gaming_control_v(self.value))


##
# @brief Endurance Gaming modes possible
class ctl_3d_endurance_gaming_mode_v(IntEnum):
    BETTER_PERFORMANCE = 0  # Endurance Gaming better performance mode
    BALANCED = 1            # Endurance Gaming balanced mode
    MAXIMUM_BATTERY = 2     # Endurance Gaming maximum battery mode


##
# @brief Endurance Gaming modes possible
class ctl_3d_endurance_gaming_mode_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_3d_endurance_gaming_mode_v
    def __str__(self):
        return str(ctl_3d_endurance_gaming_mode_v(self.value))


##
# @brief Enumeration feature details
class ctl_property_info_enum_t(ctypes.Structure):
    _fields_ = [
        ("SupportedTypes", ctypes.c_ulonglong),     # [out] Supported possible values represented as a bitmask
        ("DefaultType", ctypes.c_ulong)             # [out] Default type
    ]


##
# @brief Enumeration feature for get/set
class ctl_property_enum_t(ctypes.Structure):
    _fields_ = [
        ("EnableType", ctypes.c_ulong)          # [in,out] Enable with specific type
    ]


##
# @brief Endurance Gaming caps
class ctl_endurance_gaming_caps_t(ctypes.Structure):
    _fields_ = [
        ("EGControlCaps", ctl_property_info_enum_t),    # [out] Endurance Gaming control capability
        ("EGModeCaps", ctl_property_info_enum_t)        # [out] Endurance Gaming mode capability
    ]


##
# @brief Endurance Gaming Get/Set
class ctl_endurance_gaming_t(ctypes.Structure):
    _fields_ = [
        ("EGControl", ctl_3d_endurance_gaming_control_t),   # [in,out] Endurance Gaming control - Off/On/Auto
        ("EGMode", ctl_3d_endurance_gaming_mode_t)          # [in,out] Endurance Gaming mode - Better Perf/Balance/Max
    ]


##
# @brief Feature type
class ctl_3d_feature_v(IntEnum):
    FRAME_PACING = 0        # Frame pacing. Contains generic enum type fields
    ENDURANCE_GAMING = 1    # Endurance gaming. Contains generic integer type fields. Value will be
    # interpreted as the max FPS to be used when in DC mode globally or per
    # application
    FRAME_LIMIT = 2         # Frame limit for games. Contains generic integer type fields. Value
    # will be interpreted as the max FPS to be used independent of system
    # power state
    ANISOTROPIC = 3         # ANISOTROPIC. Contains generic enum type fields
    CMAA = 4                # CMAA. Contains generic enum type fields
    TEXTURE_FILTERING_QUALITY = 5   # Texture filtering quality. Contains generic enum type fields
    ADAPTIVE_TESSELLATION = 6       # Adaptive tessellation quality. Contains generic integer type fields
    SHARPENING_FILTER = 7           # Sharpening Filter. Contains generic integer type fields
    MSAA = 8                        # Msaa. Contains generic enum type fields
    ASYNC_FLIP_MODES = 9            # Various async flips modes like speed frame, smooth sync & force aync
                                    # flip. Contains generic enum type fields
    ADAPTIVE_SYNC_PLUS = 10         # Adaptive sync plus. Refer custom field ::ctl_adaptivesync_caps_t &


##
# @brief Feature type
class ctl_3d_feature_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_3d_feature_v
    def __str__(self):
        return str(ctl_3d_feature_v(self.value))


##
# @brief Value type
class ctl_property_value_type_v(IntEnum):
    BOOL = 0  # Boolean
    FLOAT = 1  # Float
    INT32 = 2  # Int32
    UINT32 = 3  # Unsigned Int32
    ENUM = 4  # Enum
    CUSTOM = 5  # Custom argument


##
# @brief Value type
class ctl_property_value_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_property_value_type_v
    def __str__(self):
        return str(ctl_property_value_type_v(self.value))

##
# @brief Property range details, a generic struct to hold min/max/step size
class ctl_property_range_info_t(ctypes.Structure):
    _fields_ = [
        ("min_possible_value", ctypes.c_float),  # [out] Minimum possible value
        ("max_possible_value", ctypes.c_float),  # [out] Maximum possible value
        ("step_size", ctypes.c_float),  # [out] Step size possible
        ("default_value", ctypes.c_float)  # [out] Default value
    ]


##
# @brief Property range details of integer type, a generic struct to hold
# min/max/step size information of various feature properties
class ctl_property_range_info_int_t(ctypes.Structure):
    _fields_ = [
        ("min_possible_value", ctypes.c_int32),  # [out] Minimum possible value
        ("max_possible_value", ctypes.c_int32),  # [out] Maximum possible value
        ("step_size", ctypes.c_int32),  # [out] Step size possible
        ("default_value", ctypes.c_int32)  # [out] Default value
    ]


##
# @brief Property range details of unsigned integer type, a generic struct to
# hold min/max/step size information of various feature properties
class ctl_property_range_info_uint_t(ctypes.Structure):
    _fields_ = [
        ("min_possible_value", ctypes.c_ulong),  # [out] Minimum possible value
        ("max_possible_value", ctypes.c_ulong),  # [out] Maximum possible value
        ("step_size", ctypes.c_ulong),  # [out] Step size possible
        ("default_value", ctypes.c_ulong)  # [out] Default value
    ]


##
# @brief Bool feature details
class ctl_property_info_boolean_t(ctypes.Structure):
    _fields_ = [
        ("DefaultState", ctypes.c_bool)  # [out] Default state
    ]


##
# @brief Bool feature for get/set
class ctl_property_boolean_t(ctypes.Structure):
    _fields_ = [
        ("Enable", ctypes.c_bool)  # [in,out] Enable
    ]


##
# @brief Float feature details
class ctl_property_info_float_t(ctypes.Structure):
    _fields_ = [
        ("DefaultEnable", ctypes.c_bool),  # [in,out] DefaultEnable
        ("RangeInfo", ctl_property_range_info_t)  # [out] Min/max/default/step details
    ]


##
# @brief Float feature for get/set
class ctl_property_float_t(ctypes.Structure):
    _fields_ = [
        ("Enable", ctypes.c_bool),  # [in,out] Enable
        ("Value", ctypes.c_float)  # [in,out] Value
    ]


##
# @brief Int32 feature details
class ctl_property_info_int_t(ctypes.Structure):
    _fields_ = [
        ("DefaultEnable", ctypes.c_bool),  # [in,out] DefaultEnable
        ("RangeInfo", ctl_property_range_info_int_t)  # [out] Min/max/default/step details
    ]


##
# @brief Int32 feature for get/set
class ctl_property_int_t(ctypes.Structure):
    _fields_ = [
        ("Enable", ctypes.c_bool),  # [in,out] Enable
        ("Value", ctypes.c_int32)  # [in,out] Value
    ]


##
# @brief Int32 feature details
class ctl_property_info_uint_t(ctypes.Structure):
    _fields_ = [
        ("DefaultEnable", ctypes.c_bool),  # [in,out] DefaultEnable
        ("RangeInfo", ctl_property_range_info_uint_t)  # [out] Min/max/default/step details
    ]


##
# @brief Int32 feature for get/set
class ctl_property_uint_t(ctypes.Structure):
    _fields_ = [
        ("Enable", ctypes.c_bool),  # [in,out] Enable
        ("Value", ctypes.c_ulong)  # [in,out] Value
    ]


##
# @brief Feature element details, union of bool/float/enum property_info
class ctl_property_info_t(ctypes.Structure):
    _fields_ = [
        ("BoolType", ctl_property_info_boolean_t),  # [in,out] Boolean type fields
        ("FloatType", ctl_property_info_float_t),  # [in,out] Float type fields
        ("IntType", ctl_property_info_int_t),  # [in,out] Int type fields
        ("EnumType", ctl_property_info_enum_t),  # [in,out] Enum type fields
        ("UIntType", ctl_property_info_uint_t)  # [in,out] Unsigned Int type fields
    ]


##
# @brief Feature element details, union of bool/float/enum property structs. Used for get/set calls
class ctl_property_t(ctypes.Structure):
    _fields_ = [
        ("BoolType", ctl_property_boolean_t),  # [in,out] Boolean type fields
        ("FloatType", ctl_property_float_t),  # [in,out] Float type fields
        ("IntType", ctl_property_int_t),  # [in,out] Int type fields
        ("EnumType", ctl_property_enum_t),  # [in,out] Enum type fields
        ("UIntType", ctl_property_uint_t)  # [in,out] Unsigned Int type fields
    ]


##
# @brief 3D feature for get/set
class ctl_3d_feature_getset_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("FeatureType", ctl_3d_feature_t),  # [in] Features interested in
        ("ApplicationName", ctypes.c_char_p),  # [in] Application name for which the property type is applicable. If
        # this is an empty string then this will get/set global settings for the
        # given adapter. Note that this should contain only the name of the
        # application and not the system specific path
        ("ApplicationNameLength", ctypes.c_int8),  # [in] Length of ApplicationName string
        ("bSet", ctypes.c_bool),  # [in] Set this if it's a set call
        ("ValueType", ctl_property_value_type_t),  # [in] Type of value. Caller has to ensure it provides the
        # right value type which decides how one read the union structure below
        ("Value", ctl_property_t),  # [in,out] Union of various type of values for 3D features. For enum types this
        # can be anisotropic/frame pacing etc. This member is valid
        # if ValueType is not CTL_PROPERTY_VALUE_TYPE_CUSTOM
        ("CustomValueSize", ctypes.c_int32),  # [in] CustomValue buffer size.
        ("pCustomValue", ctypes.c_void_p)  # [in,out] Pointer to a custom structure. Caller should allocate this
    ]


##
# @brief Ambient Mode params table value
class ctl_lace_lux_aggr_map_entry_t(ctypes.Structure):

    _fields_ = [
        ("Lux", ctypes.c_ulong),  # [in] size of this structure
        ("AggressivenessPercent", ctypes.c_int8)  # [in] version of this structure
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Lux = 0
        self.AggressivenessPercent = 0


##
# @brief Ambient Mode params for Lace
class ctl_lace_lux_aggr_map_t(ctypes.Structure):

    _fields_ = [
        ("MaxNumEntries", ctypes.c_ulong),  # [in] size of this structure
        ("NumEntries", ctypes.c_ulong), # [in] version of this structure
        ("pLuxToAggrMappingTable",ctypes.POINTER(ctl_lace_lux_aggr_map_entry_t))
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.MaxNumEntries = -1
        self.NumEntries = -1



##
# @brief Lace config to set via mode
class ctl_lace_aggr_config_t(ctypes.Union):

    _fields_ = [
        ("FixedAggressivenessLevelPercent", ctypes.c_int8),  # [in] size of this structure
        ("AggrLevelMap", ctl_lace_lux_aggr_map_t)
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.FixedAggressivenessLevelPercent = 0
        self.AggrLevelMap = ctl_lace_lux_aggr_map_t()

##
# @brief get Configuration operation types
class ctl_lace_get_operation_code_type_v(IntEnum):
    CTL_OPERATION_QUERY_CURRENT    = CTL_BIT(0) # Get the details set through last set call
    CTL_OPERATION_QUERY_DEFAULT    = CTL_BIT(1) # Get the driver default values
    CTL_OPERATION_QUERY_CAPABILITY = CTL_BIT(2) # Get capability


##
# @brief Configuration operation types value
class ctl_lace_get_operation_code_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       hex of ctl_lace_get_operation_code_type_v
    def __str__(self):
        return hex(ctl_lace_get_operation_code_type_v(self.value))

##
# @brief set Configuration operation types
class ctl_lace_set_operation_code_type_v(IntEnum):
    CAPI_OPERATION_RESTORE_DEFAULT  = 0 # Restore default values.
    CAPI_OPERATION_SET_CUSTOM       = 1 # Set custom values.


##
# @brief Configuration operation types value
class ctl_lace_set_operation_code_type_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_pixtx_config_opertaion_type_v
    def __int__(self):
        return int(ctl_lace_set_operation_code_type_v(self.value))

##
# @brief Configuration operation types
class ctl_lace_operation_mode_type_v(IntEnum):
    CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT = CTL_BIT(0)  # Via set ambient mode
    CTL_LACE_TRIGGER_FLAG_FIXED_AGGRESSIVENESS = CTL_BIT(1)  # via aggressive percent mode


##
# @brief Configuration operation types value
class ctl_lace_operation_mode_type_t(ctypes.c_int):

    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_lace_operation_mode_type_v
    def __str__(self):
        return hex(ctl_lace_operation_mode_type_v(self.value))

##
# @brief Pixel transformation pipe get configuration
class ctl_lace_config_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),  # [in] size of this structure
        ("Version", ctypes.c_ubyte),  # [in] version of this structure
        ("Enabled", ctypes.c_bool),  # [in] Query operation type
        ("OpTypeGet", ctl_lace_get_operation_code_type_t),  # [out] Operation type get
        ("OpTypeSet", ctl_lace_set_operation_code_type_t),  # [out] Operation type set
        ("Trigger", ctl_lace_operation_mode_type_t),  # [out] Trigger
        ("LaceConfig", ctl_lace_aggr_config_t)
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.Enabled = False
        self.OpTypeGet = -1
        self.OpTypeSet = -1
        self.Trigger = -1
        self.LaceConfig = ctl_lace_aggr_config_t()


##
## @brief Intel Arc Sync Monitor Params
class ctl_intel_arc_sync_monitor_params_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                   # [in] size of this structure
        ("Version", ctypes.c_ubyte),                # [in] version of this structure
        ("IsIntelArcSyncSupported", ctypes.c_bool), # [out] Intel Arc Sync support for the monitor
        ("MinimumRefreshRateInHz", ctypes.c_float),
                                                    # [out] Minimum Intel Arc Sync refresh rate supported by the monitor
        ("MaximumRefreshRateInHz", ctypes.c_float),
                                                    # [out] Maximum Intel Arc Sync refresh rate supported by the monitor
        ("MaxFrameTimeIncreaseInUs", ctypes.c_ulong),
                                                    # [out] Max frame time increase in micro seconds from DID2.1 Adaptive
                                                    # Sync block
        ("MaxFrameTimeDecreaseInUs", ctypes.c_ulong)
                                                    # [out] Max frame time decrease in micro seconds from DID2.1 Adaptive
                                                    # Sync block
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.IsIntelArcSyncSupported = False
        self.MinimumRefreshRateInHz = 0
        self.MaximumRefreshRateInHz = 0
        self.MaxFrameTimeIncreaseInUs = 0
        self.MaxFrameTimeDecreaseInUs = 0


##
# @brief Intel Arc Sync profile
class ctl_intel_arc_sync_profile_v(IntEnum):
    INVALID = 0  # Invalid profile
    RECOMMENDED = 1  # Default. Selects appropriate profile based on the monitor. COMPATIBLE
                     # profile is applied if profile is not available for the monitor
    EXCELLENT = 2    # Unconstrained. Full VRR range of the monitor can be used
    GOOD = 3         # Some minor range constraints, unlikely to effect user experience but
                     # can reduce flicker on some monitors
    COMPATIBLE = 4   # Significant constraints that will reduce flicker considerably but are
                     # likely to cause some level of judder onscreen especially when refresh
                     # rates are changing rapidly
    OFF = 5          # Disable Intel Arc Sync on this monitor. This disables variable rate
                     # flips on this monitor. All sync flips will occur at the OS requested
                     # refresh rate
    VESA = 6         # Applies vesa specified constraints if the monitor has provided them,
                     # COMPATIBLE profile if not
    CUSTOM = 7       # Unlocks controls to set a custom Intel Arc Sync profile


##
# @brief Intel Arc Sync Profile
class ctl_intel_arc_sync_profile_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @return       str of ctl_intel_arc_sync_profile_v
    def __str__(self):
        return str(ctl_intel_arc_sync_profile_v(self.value))


##
# @brief Intel Arc Sync Profile Params
class ctl_intel_arc_sync_profile_params_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),                               # [in] size of this structure
        ("Version", ctypes.c_ubyte),                            # [in] version of this structure
        ("IntelArcSyncProfile", ctl_intel_arc_sync_profile_t),  # [in,out] Intel Arc Sync profile used by driver. Refer
                                                                # ::ctl_intel_arc_sync_profile_t
        ("MaxRefreshRateInHz", ctypes.c_float),                 # [in,out] Maximum refresh rate utilized by the driver
        ("MinRefreshRateInHz", ctypes.c_float),                 # [in,out] Minimum refresh rate utilized by the driver
        ("MaxFrameTimeIncreaseInUs", ctypes.c_ulong),           # [in,out] Maximum frame time increase
                                                                # (in micro seconds) imposed by the driver
        ("MaxFrameTimeDecreaseInUs", ctypes.c_ulong)            # [in,out] Maximum frame time decrease
                                                                # (in micro seconds) imposed by the driver
    ]

    ##
    # @brief        Constructor
    # @param[in]    self - self
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.IntelArcSyncProfile = 0
        self.MaxRefreshRateInHz = 0
        self.MinRefreshRateInHz = 0
        self.MaxFrameTimeIncreaseInUs = 0
        self.MaxFrameTimeDecreaseInUs = 0


##
# @brief    control set brightness to set target Brightness and smooth Brightness values.
class ctl_set_brightness_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),       # [in] size of this structure
        ("Version", ctypes.c_ubyte),    # [in] version of this structure
        ("TargetBrightness", ctypes.c_ulong),   # [in] The brightness level that the display need to transitioning to in
                                                # milli-percentage. Range is 0-100000 (100%)
        ("SmoothTransitionTimeInMs", ctypes.c_ulong),   # [in] Transition Time for brightness to take effect in
                                                        # milli-seconds If its 0 then it will be an immediate change.
                                                        # Maximum possible value is 1000ms.
        ("ReservedFields", ctypes.c_ulong * 4)  # [in] Reserved for future use
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.TargetBrightness = 0
        self.SmoothTransitionTimeInMs = 0


##
# @brief    control get brightness to get target Brightness and current Brightness values.
class ctl_get_brightness_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),       # [in] size of this structure
        ("Version", ctypes.c_ubyte),    # [in] version of this structure
        ("TargetBrightness", ctypes.c_ulong),   # [out] The brightness level that the display is currently transitioning
                                                # to in milli-percentage. If not in a transition, this should equal the
                                                # current brightness. Range is 0-100000 (100%)
        ("CurrentBrightness", ctypes.c_ulong),  # [out] The current brightness level of the display in milli-percentage
        ("ReservedFields", ctypes.c_ulong * 4)  # [out] Reserved for future use
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.Size = 0
        self.Version = 0
        self.TargetBrightness = 0
        self.CurrentBrightness = 0


##
# @brief EDID Management OpTypes
class ctl_edid_management_optype_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_management_optype_v
    def __int__(self):
        return int(ctl_edid_management_optype_v(self.value))


##
# @brief EDID Management OpTypes Values
class ctl_edid_management_optype_v(IntEnum):
    READ_EDID = 1
    LOCK_EDID = 2
    UNLOCK_EDID = 3
    OVERRIDE_EDID = 4
    REMOVE_EDID = 5
    MAX = 6


##
# @brief EDID Management EDID types
class ctl_edid_type_t(ctypes.c_uint):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_type_v
    def __int__(self):
        return int(ctl_edid_type_v(self.value))


##
# @brief EDID Management EDID types Values
class ctl_edid_type_v(IntEnum):
    EDID_TYPE_CURRENT = 1
    EDID_TYPE_OVERRIDE = 2
    EDID_TYPE_MONITOR = 3
    EDID_TYPE_MAX = 4


##
# @brief EDID Management Output flags
class ctl_edid_management_out_flag_t(ctypes.c_uint):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_management_out_flag_v
    def __int__(self):
        return hex(ctl_edid_management_out_flag_v(CTL_BIT(self.value)))


##
# @brief EDID Management Output Flags Values
class ctl_edid_management_out_flag_v(IntEnum):
    FLAG_OS_CONN_NOTIFICATION = CTL_BIT(0)
    FLAG_SUPPLIED_EDID = CTL_BIT(1)
    FLAG_MONITOR_EDID = CTL_BIT(2)
    FLAG_DISPLAY_CONNECTED = CTL_BIT(3)
    FLAG_DISPLAYID_BLOCK = CTL_BIT(4)
    FLAG_MAX = 0x80000000


##
# @brief EDID Management Error Codes
class ctl_edid_mgmt_error_code(IntEnum):
    EDID_MGMT_NO_ERROR = 0
    EDID_MGMT_ERROR_INVALID_PARAM = 1
    EDID_MGMT_ERROR_NO_MEMORY = 2
    EDID_MGMT_ERROR_NO_EDID = 3  # for Case when READ Request came and data not present, say Supplied EDID read when no override happened.
    EDID_MGMT_ERROR_CORRUPTED_EDID = 4  # For EDID Checksum invalid, or incorrect size etc.
    EDID_MGMT_ERROR_INVALID_OPERATION = 5  # e.g. wrong interleaved Lock/override sequence.
    EDID_MGMT_ERROR_UNSUPPORTED_TARGET_TYPE = 6
    EDID_MGMT_ERROR_TARGET_DETACHED = 7


##
# @brief EDID Management Arguments
class ctl_edid_management_args_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),
        ("Version", ctypes.c_uint8),
        ("OpType", ctl_edid_management_optype_t),
        ("EdidType", ctl_edid_type_t),
        ("EdidSize", ctypes.c_uint32),
        ("pEdidBuf", ctypes.c_uint8),
        ("OutFlags", ctl_edid_management_out_flag_t)
    ]


##
# @brief Display Genlock Operations
class ctl_genlock_operation_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_management_optype_v
    def __int__(self):
        return int(ctl_genlock_operation_v(self.value))


##
# @brief Display Genlock Operations values
class ctl_genlock_operation_v(IntEnum):
    GET_TIMING_DETAILS = 0
    VALIDATE = 1
    ENABLE = 2
    DISABLE = 3
    GET_TOPOLOGY = 4
    MAX = 5


##
# @brief Display Genlock Info
class ctl_genlock_display_info_t(ctypes.Structure):
    _fields_ = [
        ("hDisplayOutput", ctypes.c_void_p),
        ("IsPrimary", ctypes.c_bool)
    ]


##
# @brief Genlock Target Mode List
class ctl_genlock_target_mode_list_t(ctypes.Structure):
    _fields_ = [
        ("hDisplayOutput", ctypes.c_void_p),
        ("NumModes", ctypes.c_uint32),
        ("pTargetModes", ctypes.POINTER(ctl_display_timing_t))
    ]
##
# @brief Genlock Topology
class ctl_genlock_topology_t(ctypes.Structure):
    _fields_ = [
        ("NumGenlockDisplays", ctypes.c_uint8),
        ("IsPrimaryGenlockSystem", ctypes.c_bool),
        ("CommonTargetMode", ctl_display_timing_t),
        ("pGenlockDisplayInfo", ctypes.POINTER(ctl_genlock_display_info_t)),
        ("pGenlockModeList", ctypes.POINTER(ctl_genlock_target_mode_list_t))
    ]


##
# @brief Display Genlock Arg Type
class ctl_genlock_args_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),
        ("Version", ctypes.c_uint8),
        ("Operation", ctl_genlock_operation_t),
        ("GenlockTopology", ctl_genlock_topology_t),
        ("IsGenlockEnabled", ctypes.c_bool),
        ("IsGenlockPossible", ctypes.c_bool)
    ]


##
# @brief Combined Display OpTypes
class ctl_combined_display_optype_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_management_optype_v
    def __int__(self):
        return int(ctl_combined_display_optype_v(self.value))

##
# @brief Combined Display OpTypes Values
class ctl_combined_display_optype_v(IntEnum):
    CTL_COMBINED_DISPLAY_OPTYPE_IS_SUPPORTED_CONFIG = 1
    CTL_COMBINED_DISPLAY_OPTYPE_ENABLE = 2
    CTL_COMBINED_DISPLAY_OPTYPE_DISABLE = 3
    CTL_COMBINED_DISPLAY_OPTYPE_QUERY_CONFIG = 4
    CTL_COMBINED_DISPLAY_OPTYPE_MAX = 5

##
# @brief Combined Display Orientation
class ctl_display_orientation_t(ctypes.c_int):
    ##
    # @brief        Constructor
    # @param[in]    self - self
    # @return       str of ctl_edid_management_optype_v
    def __int__(self):
        return int(ctl_display_orientation_v(self.value))

##
# @brief Combined Display Orientation Values
class ctl_display_orientation_v(IntEnum):
    CTL_DISPLAY_ORIENTATION_0 = 0
    CTL_DISPLAY_ORIENTATION_90 = 1
    CTL_DISPLAY_ORIENTATION_180 = 2
    CTL_DISPLAY_ORIENTATION_270 = 3
    CTL_DISPLAY_ORIENTATION_MAX = 4

##
# @brief Combined Display Rectangle Arg Type
class ctl_rect_t(ctypes.Structure):
    _fields_ = [
        ("Left", ctypes.c_uint32),
        ("Top", ctypes.c_uint32),
        ("Right", ctypes.c_uint32),
        ("Bottom", ctypes.c_uint32)
    ]

##
# @brief Combined Display Target Mode Type
class ctl_child_display_target_mode_t(ctypes.Structure):
    _fields_ = [
        ("Width", ctypes.c_uint32),
        ("Height", ctypes.c_uint32),
        ("RefreshRate", ctypes.c_float),
        ("ReservedFields", ctypes.c_uint32 * 4)
    ]

##
# @brief Combined Display Child Info
class ctl_combined_display_child_info_t(ctypes.Structure):
    _fields_ = [
        ("hDisplayOutput", ctypes.c_void_p),
        ("FbSrc", ctl_rect_t),
        ("FbPos", ctl_rect_t),
        ("DisplayOrientation", ctl_display_orientation_t),
        ("TargetMode", ctl_child_display_target_mode_t)
    ]

##
# @brief Combined Display Arguments
class ctl_combined_display_args_t(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_uint32),
        ("Version", ctypes.c_uint8),
        ("OpType", ctl_combined_display_optype_t),
        ("IsSupported", ctypes.c_bool),
        ("NumOutputs", ctypes.c_uint8),
        ("CombinedDesktopWidth", ctypes.c_uint32),
        ("CombinedDesktopHeight", ctypes.c_uint32),
        ("pChildInfo", ctypes.POINTER(ctl_combined_display_child_info_t)),
        ("hCombinedDisplayOutput", ctypes.c_void_p)
    ]