#######################################################################################################################
# @file         sink_caps_data_structures.py
# @brief        This file contains ths Sink Capability Data Structures required to parse HF-VSDB block
# @details      For more information related to the block refer HDMI2.1 Spec E-EDID section
#
# @author       Praburaj Krishnan
#######################################################################################################################

import ctypes


##
# @brief        Structure that contains the bit definitions for the payload byte three in SCDS
class _PayloadByteThree(ctypes.Structure):
    _fields_ = [
        ("three_d_osd_disparity", ctypes.c_uint8, 1),
        ("dual_view", ctypes.c_uint8, 1),
        ("independent_view", ctypes.c_uint8, 1),
        ("lte_340MHz_scramble", ctypes.c_uint8, 1),
        ("ccbpci", ctypes.c_uint8, 1),
        ("cable_status", ctypes.c_uint8, 1),
        ("rr_capable", ctypes.c_uint8, 1),
        ("scdc_present", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 3rd payload byte value of SCDS
class PayloadByteThree(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteThree),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte four in SCDS
class _PayloadByteFour(ctypes.Structure):
    _fields_ = [
        ("dc_30bit_420", ctypes.c_uint8, 1),
        ("dc_36bit_420", ctypes.c_uint8, 1),
        ("dc_48bit_420", ctypes.c_uint8, 1),
        ("uhd_vic", ctypes.c_uint8, 1),
        ("max_frl_rate", ctypes.c_uint8, 4),
    ]


##
# @brief        Union that needs to be used by the outside world to store the 4th payload byte value of SCDS
class PayloadByteFour(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteFour),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte five in SCDS
class _PayloadByteFive(ctypes.Structure):
    _fields_ = [
        ("fafa_start_location", ctypes.c_uint8, 1),
        ("allm", ctypes.c_uint8, 1),
        ("fast_v_active", ctypes.c_uint8, 1),
        ("cnmvrr", ctypes.c_uint8, 1),
        ("cinema_vrr", ctypes.c_uint8, 1),
        ("m_delta", ctypes.c_uint8, 1),
        ("reserved_one", ctypes.c_uint8, 1),
        ("reserved_two", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 5th payload byte value of SCDS
class PayloadByteFive(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteFive),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte six and seven in SCDS
class _PayloadByteSix(ctypes.Structure):
    _fields_ = [
        ("vrr_min", ctypes.c_uint8, 6),
        ("vrr_max_biteightnine", ctypes.c_uint8, 2),
    ]


##
# @brief        Union that needs to be used by the outside world to store the 6th and 7th payload byte value of SCDS
class PayloadByteSix(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteSix),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte six and seven in SCDS
class _PayloadByteSeven(ctypes.Structure):
    _fields_ = [
        ("vrr_max_bitzerotoseven", ctypes.c_uint8, 8),
    ]


##
# @brief        Union that needs to be used by the outside world to store the 6th and 7th payload byte value of SCDS
class PayloadByteSeven(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteSeven),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte eight in SCDS
class _PayloadByteEight(ctypes.Structure):
    _fields_ = [
        ("dsc_10bpc", ctypes.c_uint8, 1),
        ("dsc_12bpc", ctypes.c_uint8, 1),
        ("dsc_16bpc", ctypes.c_uint8, 1),
        ("dsc_all_bpp", ctypes.c_uint8, 1),
        ("reserved_one", ctypes.c_uint8, 1),
        ("reserved_two", ctypes.c_uint8, 1),
        ("dsc_native_420", ctypes.c_uint8, 1),
        ("dsc_1p2", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 8th payload byte value of SCDS
class PayloadByteEight(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteEight),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte nine in SCDS
class _PayloadByteNine(ctypes.Structure):
    _fields_ = [
        ("dsc_max_slices", ctypes.c_uint8, 4),
        ("dsc_max_frl_rate", ctypes.c_uint8, 4),
    ]


##
# @brief        Union that needs to be used by the outside world to store the 9th payload byte value of SCDS
class PayloadByteNine(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteNine),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte ten in SCDS
class _PayloadByteTen(ctypes.Structure):
    _fields_ = [
        ("dsc_total_chunk_bytes", ctypes.c_uint8, 6),
        ("reserved_one", ctypes.c_uint8, 1),
        ("reserved_two", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 10th payload byte value of SCDS
class PayloadByteTen(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteTen),
        ("Value", ctypes.c_uint8)
    ]
