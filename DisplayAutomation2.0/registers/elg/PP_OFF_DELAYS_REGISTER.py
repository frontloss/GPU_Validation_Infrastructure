##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/50461

import ctypes

'''
Register instance and offset 
'''
PP_OFF_DELAYS = 0xC720C
PP_OFF_DELAYS_2 = 0xC730C


'''
Register bitfield defnition structure 
'''
class PP_OFF_DELAYS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("backlight_off_to_power_down", ctypes.c_uint32, 13), # 0 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("power_down_delay"   , ctypes.c_uint32, 13), # 16 to 28
        ("reserved_29"       , ctypes.c_uint32, 3), # 29 to 31
    ]


class PP_OFF_DELAYS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PP_OFF_DELAYS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
