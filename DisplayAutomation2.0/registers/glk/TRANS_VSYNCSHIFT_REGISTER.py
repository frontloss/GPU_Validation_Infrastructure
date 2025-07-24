import ctypes
 
'''
Register instance and offset 
'''
TRANS_VSYNCSHIFT_A = 0x60028 
TRANS_VSYNCSHIFT_B = 0x61028 
TRANS_VSYNCSHIFT_C = 0x62028 
TRANS_VSYNCSHIFT_D = 0x63028 
TRANS_VSYNCSHIFT_DSI0 = 0x6B028 
TRANS_VSYNCSHIFT_DSI1 = 0x6B828 
TRANS_VSYNCSHIFT_EDP = 0x6F028 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_VSYNCSHIFT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("second_field_vsync_shift" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"             , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class TRANS_VSYNCSHIFT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VSYNCSHIFT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
