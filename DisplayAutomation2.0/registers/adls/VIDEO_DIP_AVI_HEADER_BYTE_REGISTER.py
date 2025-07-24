import ctypes
 
'''
Register instance and offset 
'''
VIDEO_DIP_AVI_DATA_A_0 = 0x60220
VIDEO_DIP_AVI_DATA_B_0 = 0x61220
VIDEO_DIP_AVI_DATA_C_0 = 0x62220
VIDEO_DIP_AVI_DATA_D_0 = 0x63220


'''
Register bitfield definition structure 
'''
class VIDEO_DIP_AVI_HEADER_BYTE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("header_byte_0" , ctypes.c_uint32, 8), # 0 to 7
        ("header_byte_1" , ctypes.c_uint32, 8), # 8 to 15
        ("header_byte_2" , ctypes.c_uint32, 8), # 16 to 23
        ("header_byte_3" , ctypes.c_uint32, 8), # 24 to 31
    ]

 
class VIDEO_DIP_AVI_HEADER_BYTE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", VIDEO_DIP_AVI_HEADER_BYTE_REG),
        ("asUint", ctypes.c_uint32)]
