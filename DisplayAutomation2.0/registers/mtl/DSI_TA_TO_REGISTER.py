import ctypes
 
'''
Register instance and offset 
'''
DSI_TA_TO_DSI0 = 0x6B04C 
DSI_TA_TO_DSI1 = 0x6B84C 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DSI_TA_TO_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("turnaround_timeout" , ctypes.c_uint32, 16), # 0 to 15 
        ("ta_to"             , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"       , ctypes.c_uint32, 15), # 17 to 31 
    ]

 
class DSI_TA_TO_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_TA_TO_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
