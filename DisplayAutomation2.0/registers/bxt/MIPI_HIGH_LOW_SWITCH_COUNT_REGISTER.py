import ctypes
 
'''
Register instance and offset 
'''
MIPIA_HIGH_LOW_SWITCH_COUNT = 0x6B044 
MIPIC_HIGH_LOW_SWITCH_COUNT = 0x6B844 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_HIGH_LOW_SWITCH_COUNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("high_speed_to_low_power_or_low_power_to_high_speed_switch_count" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"                                                    , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_HIGH_LOW_SWITCH_COUNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_HIGH_LOW_SWITCH_COUNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
