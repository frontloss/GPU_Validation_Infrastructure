import ctypes
 
'''
Register instance and offset 
'''
DSI_PWAIT_TO_DSI0 = 0x6B040 
DSI_PWAIT_TO_DSI1 = 0x6B840 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DSI_PWAIT_TO_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("peripheral_response_timeout" , ctypes.c_uint32, 16), # 0 to 15 
        ("peripheral_reset_timeout"   , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class DSI_PWAIT_TO_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_PWAIT_TO_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
