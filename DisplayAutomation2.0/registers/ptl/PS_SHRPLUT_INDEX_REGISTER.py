import ctypes

'''
Register instance and offset 
'''
PS_SHRPLUT_INDEX_A = 0x682B4
PS_SHRPLUT_INDEX_B = 0x68AB4
PS_SHRPLUT_INDEX_C = 0x692B4
PS_SHRPLUT_INDEX_D = 0x69AB4

'''
Register field expected values 
'''
index_auto_increment_NO_INCREMENT = 0b0
index_auto_increment_AUTO_INCREMENT = 0b1

'''
Register bitfield definition structure 
'''


class PS_SHRPLUT_INDEX_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('index_value',             ctypes.c_uint32, 5),    # 0 to 4
        ('reserved5',               ctypes.c_uint32, 5),    # 5 to 9
        ('index_auto_increment',    ctypes.c_uint32, 1),    # 10 to 10
        ('reserved11',              ctypes.c_uint32, 21),   # 11 to 31
    ]


class PS_SHRPLUT_INDEX_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PS_SHRPLUT_INDEX_REG),
        ("asUint", ctypes.c_uint32)]
