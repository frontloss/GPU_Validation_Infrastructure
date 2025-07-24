import ctypes

'''
Register instance and offset 
'''
TIMESTAMP_CTR = 0X44070

'''
Register field expected values 
'''

'''
Register bitfield defnition structure
'''

class TIMESTAMP_CTR_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TimestampCounter', ctypes.c_uint32, 32),
    ]

class TIMESTAMP_CTR_REGISTER(ctypes.Union):
    value = 0
    offset = 0

    TimestampCounter = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', TIMESTAMP_CTR_REG),
        ('value', ctypes.c_uint32)
    ]