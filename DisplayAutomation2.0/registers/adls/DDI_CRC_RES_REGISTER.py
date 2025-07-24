import ctypes

'''
Register instance and offset 
'''
DDI_CRC_RES_A = 0x64064
DDI_CRC_RES_B = 0x64164
DDI_CRC_RES_C = 0x64264
DDI_CRC_RES_D = 0x64364
DDI_CRC_RES_E = 0x64464
DDI_CRC_RES_F = 0x64564

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class DDI_CRC_RES_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("crc_result_value", ctypes.c_uint32, 32),  # 0 to 31
    ]


class DDI_CRC_RES_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DDI_CRC_RES_REG),
        ("asUint", ctypes.c_uint32)]
