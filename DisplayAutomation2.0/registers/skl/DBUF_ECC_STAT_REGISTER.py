import ctypes
 
'''
Register instance and offset 
'''
DBUF_ECC_STAT = 0x45010 
DBUF_ECC_STAT_S1 = 0x45010 
DBUF_ECC_STAT_S2 = 0x44FF0 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DBUF_ECC_STAT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("single_error_bank_0" , ctypes.c_uint32, 1), # 0 to 0 
        ("single_error_bank_1" , ctypes.c_uint32, 1), # 1 to 1 
        ("single_error_bank_2" , ctypes.c_uint32, 1), # 2 to 2 
        ("single_error_bank_3" , ctypes.c_uint32, 1), # 3 to 3 
        ("single_error_bank_4" , ctypes.c_uint32, 1), # 4 to 4 
        ("single_error_bank_5" , ctypes.c_uint32, 1), # 5 to 5 
        ("single_error_bank_6" , ctypes.c_uint32, 1), # 6 to 6 
        ("single_error_bank_7" , ctypes.c_uint32, 1), # 7 to 7 
        ("single_error_bank_8" , ctypes.c_uint32, 1), # 8 to 8 
        ("single_error_bank_9" , ctypes.c_uint32, 1), # 9 to 9 
        ("single_error_bank_10" , ctypes.c_uint32, 1), # 10 to 10 
        ("single_error_bank_11" , ctypes.c_uint32, 1), # 11 to 11 
        ("single_error_bank_12" , ctypes.c_uint32, 1), # 12 to 12 
        ("single_error_bank_13" , ctypes.c_uint32, 1), # 13 to 13 
        ("single_error_bank_14" , ctypes.c_uint32, 1), # 14 to 14 
        ("single_error_bank_15" , ctypes.c_uint32, 1), # 15 to 15 
        ("double_error_bank_0" , ctypes.c_uint32, 1), # 16 to 16 
        ("double_error_bank_1" , ctypes.c_uint32, 1), # 17 to 17 
        ("double_error_bank_2" , ctypes.c_uint32, 1), # 18 to 18 
        ("double_error_bank_3" , ctypes.c_uint32, 1), # 19 to 19 
        ("double_error_bank_4" , ctypes.c_uint32, 1), # 20 to 20 
        ("double_error_bank_5" , ctypes.c_uint32, 1), # 21 to 21 
        ("double_error_bank_6" , ctypes.c_uint32, 1), # 22 to 22 
        ("double_error_bank_7" , ctypes.c_uint32, 1), # 23 to 23 
        ("double_error_bank_8" , ctypes.c_uint32, 1), # 24 to 24 
        ("double_error_bank_9" , ctypes.c_uint32, 1), # 25 to 25 
        ("double_error_bank_10" , ctypes.c_uint32, 1), # 26 to 26 
        ("double_error_bank_11" , ctypes.c_uint32, 1), # 27 to 27 
        ("double_error_bank_12" , ctypes.c_uint32, 1), # 28 to 28 
        ("double_error_bank_13" , ctypes.c_uint32, 1), # 29 to 29 
        ("double_error_bank_14" , ctypes.c_uint32, 1), # 30 to 30 
        ("double_error_bank_15" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DBUF_ECC_STAT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBUF_ECC_STAT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
