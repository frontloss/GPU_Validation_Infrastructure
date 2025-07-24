import ctypes
 
'''
Register instance and offset 
'''
MIPIA_DEVICE_RESET_TIMER = 0x6B01C 
MIPIC_DEVICE_RESET_TIMER = 0x6B81C 

 
'''
Register field expected values 
'''
device_reset_timer_DEFAULT = 0x00FF

 
'''
Register bitfield defnition structure 
'''
class MIPI_DEVICE_RESET_TIMER_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("device_reset_timer" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"       , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_DEVICE_RESET_TIMER_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_DEVICE_RESET_TIMER_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
