##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/69985

import ctypes

'''
Register instance and offset 
'''
TRANS_SET_CONTEXT_LATENCY_A = 0X6007C
TRANS_SET_CONTEXT_LATENCY_B = 0X6107C
TRANS_SET_CONTEXT_LATENCY_C = 0X6207C
TRANS_SET_CONTEXT_LATENCY_D = 0X6307C
TRANS_SET_CONTEXT_LATENCY_CMTG = 0X6F07C

'''
Register bitfield defnition structure 
'''


class TRANS_SET_CONTEXT_LATENCY_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("context_latency", ctypes.c_uint32, 16),  # 0 to 15
        ("reserved_16", ctypes.c_uint32, 16),  # 16 to 31
    ]


class TRANS_SET_CONTEXT_LATENCY_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_SET_CONTEXT_LATENCY_REG),
        ("asUint", ctypes.c_uint32)]
