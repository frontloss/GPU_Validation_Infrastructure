########################################################################################################################
# @file     mipi_dsi_dcs_args.py
# @brief    Python wrapper which contains structures used for MIPI DSI DCS funtionality.
# @author   Chandrakanth Pabolu
########################################################################################################################
import ctypes
from enum import Enum

DXGK_DSI_PACKET_EMBEDDED_PAYLOAD_SIZE  = 8

#mipi DSI DCS Data Types in DSI Packet Transmission
MIPI_DSI_DCS_DATATYPE_GENERIC_SHORT_WRITE_NO_PARAM = 0x03
MIPI_DSI_DCS_DATATYPE_GENERIC_SHORT_WRITE_1_PARAM = 0x13
MIPI_DSI_DCS_DATATYPE_GENERIC_SHORT_WRITE_2_PARAM = 0x23
MIPI_DSI_DCS_DATATYPE_GENERIC_READ_NO_PARAM = 0x04
MIPI_DSI_DCS_DATATYPE_GENERIC_READ_1_PARAM = 0x14
MIPI_DSI_DCS_DATATYPE_GENERIC_READ_2_PARAM = 0x24
MIPI_DSI_DCS_DATATYPE_DCS_SHORT_WRITE_NO_PARAM = 0x05
MIPI_DSI_DCS_DATATYPE_DCS_SHORT_WRITE_1_PARAM = 0x15
MIPI_DSI_DCS_DATATYPE_DCS_SHORT_READ_NO_PARAM = 0x06
MIPI_DSI_DCS_DATATYPE_GENERIC_LONG_WRITE = 0x29
MIPI_DSI_DCS_DATATYPE_DCS_LONG_WRITE_OR_WRITE_LUT = 0x39


##
# @brief Enum for MIPI DSI control for transmission mode
class DXGK_DSI_CONTROL_TRANSMISSION_MODE(Enum):
    DXGK_DCT_DEFAULT = 0,
    DXGK_DCT_FORCE_LOW_POWER = 1,
    DXGK_DCT_FORCE_HIGH_SPEED = 2


##
# @brief Structure definition for MIPI DSI buffer caps
class DXGK_DSI_CAPS(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('DSITypeMajor', ctypes.c_ubyte),
                ('DSITypeMinor', ctypes.c_ubyte),
                ('SpecVersionMajor', ctypes.c_ubyte),
                ('SpecVersionMinor', ctypes.c_ubyte),
                ('SpecVersionPatch', ctypes.c_ubyte),
                ('TargetMaximumReturnPacketSize', ctypes.c_ushort),
                ('ResultCodeFlags', ctypes.c_ubyte),
                ('SpecVersionMinor', ctypes.c_ubyte),
                ('ResultCodeStatus', ctypes.c_ubyte),
                ('Revision', ctypes.c_ubyte),
                ('Level', ctypes.c_ubyte),
                ('DeviceClassHi', ctypes.c_ubyte),
                ('DeviceClassLo', ctypes.c_ubyte),
                ('ManufacturerHi', ctypes.c_ubyte),
                ('ManufacturerLo', ctypes.c_ubyte),
                ('ProductHi', ctypes.c_ubyte),
                ('ProductLo', ctypes.c_ubyte),
                ('LengthHi', ctypes.c_ubyte),
                ('LengthLo', ctypes.c_ubyte)]


##
# @brief Structure definition for MIPI DSI Datatype
class DXGK_DSI_DATATYPE_STR(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('DataType', ctypes.c_ubyte,6),
        ('VirtualChannel', ctypes.c_ubyte,2)
    ]


##
# @brief wrapper class for class DXGK_DSI_DATATYPE_STR
class _U(ctypes.Union):
    _fields_ = [
        ('DataId',ctypes.c_ubyte),
        ('DsiDatatype', DXGK_DSI_DATATYPE_STR)
    ]


##
# @brief Structure definition for MIPI DSI data that will be transmitted.
class DXGK_DSI_DATA(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('Data0', ctypes.c_ubyte),
        ('Data1', ctypes.c_ubyte)
    ]


##
# @brief wrapper class for class DXGK_DSI_DATA
class _U1(ctypes.Union):
    _fields_ = [
        ('DsiData', DXGK_DSI_DATA),
        ('LongWriteWordCount',ctypes.c_ushort)
    ]


##
# @brief Structure definition for bitfields contained in MIPI DSI packet.
class DXGK_DSI_PACKET(ctypes.Structure):
    _anonymous_ = ("u", "u1",)
    _fields_ = [
        ('u', _U),
        ('u1', _U1),
        ('EccFiller', ctypes.c_ubyte),
        ('Payload', ctypes.c_ubyte * DXGK_DSI_PACKET_EMBEDDED_PAYLOAD_SIZE)
    ]


##
# @brief Structure definition for bitfields contained in MIPI DSI transmission mode
class DXGK_DSI_TRANSMISSION_MODE_STR(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('TransmissionMode', ctypes.c_ushort,2),
        ('ReportMipiErrors', ctypes.c_ushort,1),
        ('ClearMipiErrors', ctypes.c_ushort,1),
        ('SecondaryPort', ctypes.c_ushort,1),
        ('ManufacturingMode', ctypes.c_ushort,1),
        ('Reserved', ctypes.c_ushort,10),
    ]


##
# @brief wrapper class for class DXGK_DSI_TRANSMISSION_MODE_STR
class DXGK_DSI_TRANSMISSION_MODE(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ('u', DXGK_DSI_TRANSMISSION_MODE_STR),
        ('asUint', ctypes.c_ushort)
    ]


##
# @brief Structure definition for bitfields contained in MIPI DSI transmission
class DXGK_DSI_TRANSMISSION(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('TotalBufferSize', ctypes.c_uint),
        ('PacketCount', ctypes.c_ubyte),
        ('FailedPacket', ctypes.c_ubyte),
        ('DsiTransmissionMode', DXGK_DSI_TRANSMISSION_MODE),
        ('ReadWordCount', ctypes.c_ushort),
        ('FinalCommandExtraPayload', ctypes.c_ushort),
        ('MipiErrors', ctypes.c_ushort),
        ('HostErrors', ctypes.c_ushort),
        ('DsiPacket', 8 * DXGK_DSI_PACKET)
    ]


##
# @brief Structure definition for parameters for MIPI DSI Reset
class DXGK_DSI_RESET_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ('MipiErrors', ctypes.c_uint),
        ('ResetFailed', ctypes.c_uint),
        ('NeedModeSet', ctypes.c_uint)
    ]


##
# @brief wrapper class for class DXGK_DSI_RESET_PARAMETERS
class _U2(ctypes.Union):
    _fields_ = [
        ('DsiResetParameters', DXGK_DSI_RESET_PARAMETERS),
        ('Results', ctypes.c_uint)
    ]


##
# @brief Structure definition for MIPI DSI Reset
class DXGK_DSI_RESET(ctypes.Structure):
    _anonymous_ = ("u2",)
    _fields_ = [
        ('Flags', ctypes.c_uint),
        ('u2', _U2),
        ('FailedPacket', ctypes.c_ubyte)
    ]
