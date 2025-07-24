import ctypes

'''
Register instance and offset
'''
VIDEO_DIP_DRM_DATA_0_A = 0x60440
VIDEO_DIP_DRM_DATA_0_B = 0x61440
VIDEO_DIP_DRM_DATA_0_C = 0x62440
VIDEO_DIP_DRM_DATA_0_D = 0x63440

VIDEO_DIP_DRM_DATA_1_A = 0x60444
VIDEO_DIP_DRM_DATA_1_B = 0x61444
VIDEO_DIP_DRM_DATA_1_C = 0x62444
VIDEO_DIP_DRM_DATA_1_D = 0x63444

VIDEO_DIP_DRM_DATA_2_A = 0x60448
VIDEO_DIP_DRM_DATA_2_B = 0x61448
VIDEO_DIP_DRM_DATA_2_C = 0x62448
VIDEO_DIP_DRM_DATA_2_D = 0x63448


'''
Register field expected values
'''

'''
Register bitfield definition structure
'''
class VIDEO_DIP_DRM_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data" , ctypes.c_uint32, 32), # 0 to 31
    ]

class VIDEO_DIP_DRM_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VIDEO_DIP_DRM_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]

