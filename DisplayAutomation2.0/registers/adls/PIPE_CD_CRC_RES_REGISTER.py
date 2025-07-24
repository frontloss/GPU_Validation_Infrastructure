import ctypes

'''
Register instance and offset 
'''
PIPE_CD_CRC_RES_A = 0x60064
PIPE_CD_CRC_RES_B = 0x61064
PIPE_CD_CRC_RES_C = 0x62064
PIPE_CD_CRC_RES_D = 0x63064

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class PIPE_CD_CRC_RES_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("crc_result_value", ctypes.c_uint32, 32),  # 0 to 31
    ]


class PIPE_CD_CRC_RES_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PIPE_CD_CRC_RES_REG),
        ("asUint", ctypes.c_uint32)]
