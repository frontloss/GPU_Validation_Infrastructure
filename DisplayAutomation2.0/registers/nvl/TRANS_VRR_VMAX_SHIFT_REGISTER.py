import ctypes

##
# Register instance and offset
TRANS_VRR_VMAX_SHIFT_A = 0x60428
TRANS_VRR_VMAX_SHIFT_B = 0x61428
TRANS_VRR_VMAX_SHIFT_C = 0x62428
TRANS_VRR_VMAX_SHIFT_D = 0x63434
TRANS_VRR_VMAX_SHIFT_EDP = 0x6F428

 
##
# Register bitfield definition structure
class TransVrrVMaxShiftReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("increment", ctypes.c_uint32, 14),         # 0 to 13
        ("reserved_2", ctypes.c_uint32, 2),         # 14 to 15
        ("decrement", ctypes.c_uint32, 14),         # 16 to 29
        ("reserved_2", ctypes.c_uint32, 2),         # 29 to 31
    ]

 
class TRANS_VRR_VMAX_SHIFT_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrVMaxShiftReg),
        ("asUint", ctypes.c_uint32)
    ]
