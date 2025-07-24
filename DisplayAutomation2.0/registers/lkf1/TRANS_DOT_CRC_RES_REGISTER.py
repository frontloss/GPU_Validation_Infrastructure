import ctypes

'''
Register instance and offset 
'''
TRANS_DOT_CRC_RES_A = 0x60094
TRANS_DOT_CRC_RES_B = 0x61094
TRANS_DOT_CRC_RES_C = 0x62094
TRANS_DOT_CRC_RES_D = 0x63094

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class TRANS_DOT_CRC_RES_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("crc_result_value", ctypes.c_uint32, 32),  # 0 to 31
    ]


class TRANS_DOT_CRC_RES_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_DOT_CRC_RES_REG),
        ("asUint", ctypes.c_uint32)]
