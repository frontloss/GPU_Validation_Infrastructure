import ctypes

##
# Register instance and offset
TRANS_VRR_STATUS2_A = 0x6043C
TRANS_VRR_STATUS2_B = 0x6143C
TRANS_VRR_STATUS2_C = 0x6243C
TRANS_VRR_STATUS2_D = 0x6343C
TRANS_VRR_STATUS2_EDP = 0x6F43C

 
##
# Register bitfield definition structure
class TransVrrStatus2Reg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vertical_line_counter_status", ctypes.c_uint32, 20),      # 0 to 19
        ("reserved_16", ctypes.c_uint32, 12),                       # 20 to 31
    ]

 
class TRANS_VRR_STATUS2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrStatus2Reg),
        ("asUint", ctypes.c_uint32)
    ]
