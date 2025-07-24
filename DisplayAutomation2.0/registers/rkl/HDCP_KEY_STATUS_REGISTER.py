##
# BSpec link : https://gfxspecs.intel.com/Predator/Home/Index/50276
import ctypes

'''
Register instance and offset
'''
HDCP_KEY_STATUS = 0x66C04


'''
Register bitfield definition structure
'''


class HDCP_KEY_STATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("key_load_done", ctypes.c_uint32, 1),  # 0 to 0
        ("key_load_status", ctypes.c_uint32, 1),  # 1 to 1
        ("reserved_2", ctypes.c_uint32, 3),  # 2 to 4
        ("fuse_done", ctypes.c_uint32, 1),  # 5 to 5
        ("fuse_error", ctypes.c_uint32, 1),  # 6 to 6
        ("fuse_in_progress", ctypes.c_uint32, 1),  # 7 to 7
        ("reserved_8", ctypes.c_uint32, 24),  # 8 to 31

    ]


class HDCP_KEY_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP_KEY_STATUS_REG),
        ("asUint", ctypes.c_uint32)]

