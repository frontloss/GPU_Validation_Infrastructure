#######################################################################################################################
# @file         emp_data_structures.py
# @brief        This file contains Extended Metadata packets(EMP) Data Structures required to program for EMP packets
# @details      For more information related to EMP refer https://gfxspecs.intel.com/Predator/Home/Index/66670
#
# @author       Doriwala Nainesh
#######################################################################################################################

import ctypes


##
# @brief        Structure that contains the bit definitions for the payload byte zero in EMP
class _PayloadByteZero(ctypes.Structure):
    _fields_ = [
        ("rsvd", ctypes.c_uint8, 1),
        ("sync", ctypes.c_uint8, 1),
        ("vfr", ctypes.c_uint8, 1),
        ("afr", ctypes.c_uint8, 1),
        ("ds_type", ctypes.c_uint8, 2),
        ("end", ctypes.c_uint8, 1),
        ("new", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 0th payload byte value of EMP
class PayloadByteZero(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteZero),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte one in EMP
class _PayloadByteOne(ctypes.Structure):
    _fields_ = [
        ("rsvd", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 1st payload byte value of EMP
class PayloadByteOne(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteOne),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte two in EMP
class _PayloadByteTwo(ctypes.Structure):
    _fields_ = [
        ("organization_id", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 2nd payload byte value of EMP
class PayloadByteTwo(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteTwo),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte three in EMP
class _PayloadByteThree(ctypes.Structure):
    _fields_ = [
        ("data_set_tag_msb", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 3rd payload byte value of EMP
class PayloadByteThree(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteThree),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte four in EMP
class _PayloadByteFour(ctypes.Structure):
    _fields_ = [
        ("data_set_tag_lsb", ctypes.c_uint8, 1)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 4th payload byte value of EMP
class PayloadByteFour(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteFour),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte five in EMP
class _PayloadByteFive(ctypes.Structure):
    _fields_ = [
        ("data_set_length_msb", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 5th payload byte value of EMP
class PayloadByteFive(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteFive),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte six and seven in EMP
class _PayloadByteSix(ctypes.Structure):
    _fields_ = [
        ("data_set_length_lsb", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 6th and 7th payload byte value of EMP
class PayloadByteSix(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteSix),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte six and seven in EMP
class _PayloadByteSeven(ctypes.Structure):
    _fields_ = [
        ("vrr_en", ctypes.c_uint8, 1),
        ("m_const", ctypes.c_uint8, 1),
        ("rsvd", ctypes.c_uint8, 2),
        ("fva_factor_m1", ctypes.c_uint8, 4)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 6th and 7th payload byte value of EMP
class PayloadByteSeven(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteSeven),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte eight in EMP
class _PayloadByteEight(ctypes.Structure):
    _fields_ = [
        ("base_vfornt", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 8th payload byte value of EMP
class PayloadByteEight(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteEight),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte nine in EMP
class _PayloadByteNine(ctypes.Structure):
    _fields_ = [
        ("base_refresh_rate_biteightnine", ctypes.c_uint8, 2),
        ("rsvd", ctypes.c_uint8, 1),
        ("next_tfr", ctypes.c_uint8, 5)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 9th payload byte value of EMP
class PayloadByteNine(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteNine),
        ("Value", ctypes.c_uint8)
    ]


##
# @brief        Structure that contains the bit definitions for the payload byte ten in EMP
class _PayloadByteTen(ctypes.Structure):
    _fields_ = [
        ("base_refresh_rate_bitzeroseven", ctypes.c_uint8, 8)
    ]


##
# @brief        Union that needs to be used by the outside world to store the 10th payload byte value of EMP
class PayloadByteTen(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PayloadByteTen),
        ("Value", ctypes.c_uint8)
    ]
