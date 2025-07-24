import ctypes
 
##
# Register instance and offset
TRANS_VRR_VTOTAL_PREV_A = 0x60480 
TRANS_VRR_VTOTAL_PREV_B = 0x61480 
TRANS_VRR_VTOTAL_PREV_C = 0x62480 
TRANS_VRR_VTOTAL_PREV_D = 0x63480 
TRANS_VRR_VTOTAL_PREV_EDP = 0x6F480 

 
##
# Register bitfield definition structure
class TransVrrVTotalPrevReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vtotal_previous", ctypes.c_uint32, 20),           # 0 to 19
        ("reserved_20", ctypes.c_uint32, 9),                # 20 to 28
        ("flip_after_double_buffer", ctypes.c_uint32, 1),   # 29 to 29
        ("flip_after_boundary", ctypes.c_uint32, 1),        # 30 to 30
        ("flip_before_boundary", ctypes.c_uint32, 1),       # 31 to 31
    ]

 
class TRANS_VRR_VTOTAL_PREV_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrVTotalPrevReg),
        ("asUint", ctypes.c_uint32)
    ]
