import ctypes
 
'''
Register instance and offset 
'''
PIPE_CD_CRC_EXP_A = 0x60054 
PIPE_CD_CRC_EXP_B = 0x61054 
PIPE_CD_CRC_EXP_C = 0x62054 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CRC_EXP_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("crc_expected_value" , ctypes.c_uint32, 32), # 0 to 31 
    ]

 
class CRC_EXP_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CRC_EXP_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
