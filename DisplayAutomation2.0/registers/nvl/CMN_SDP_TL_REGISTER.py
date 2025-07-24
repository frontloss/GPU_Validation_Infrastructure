##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/74384

import ctypes

##
# Register instance and offset
CMN_SDP_TL_A = 0x6020C
CMN_SDP_TL_B = 0x6120C
CMN_SDP_TL_C = 0x6220C
CMN_SDP_TL_D = 0x6320C
CMN_SDP_TL_E = 0x6B20C
CMN_SDP_TL_F = 0x6C20C


##
# Register bitfield definition structure
class CmnSdpTlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("base_transmission_line", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_18", ctypes.c_uint32, 18),  # 13 to 30
        ("enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class CMN_SDP_TL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CmnSdpTlReg),
        ("asUint", ctypes.c_uint32)
    ]