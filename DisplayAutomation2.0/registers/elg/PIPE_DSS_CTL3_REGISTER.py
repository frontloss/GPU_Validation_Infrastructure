import ctypes

'''
Register instance and offset 
'''
PIPE_DSS_CTL3_PA = 0x780F0
PIPE_DSS_CTL3_PB = 0x782F0
PIPE_DSS_CTL3_PC = 0x784F0
PIPE_DSS_CTL3_PD = 0x786F0

'''
Register bitfield definition structure 
'''


class PIPE_DSS_CTL3_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dsc_pixel_replication", ctypes.c_uint32, 16),  # 0 to 15
        ("reserved", ctypes.c_uint32, 16),  # 16 to 31
    ]


class PIPE_DSS_CTL3_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PIPE_DSS_CTL3_REG),
        ("asUint", ctypes.c_uint32)]
