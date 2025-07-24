##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/50462

import ctypes

'''
Register instance and offset 
'''
PP_ON_DELAYS = 0xC7208
PP_ON_DELAYS_2 = 0xC7308


'''
Register bitfield defnition structure 
'''
class PP_ON_DELAYS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("power_on_to_backlight_on", ctypes.c_uint32, 13), # 0 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("power_up_delay"   , ctypes.c_uint32, 13), # 16 to 28
        ("reserved_29"       , ctypes.c_uint32, 3), # 29 to 31
    ]


class PP_ON_DELAYS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PP_ON_DELAYS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
