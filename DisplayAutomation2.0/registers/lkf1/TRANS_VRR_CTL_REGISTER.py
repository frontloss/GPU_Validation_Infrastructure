import ctypes
 
##
# Register instance and offset
TRANS_VRR_CTL_A = 0x60420
TRANS_VRR_CTL_B = 0x61420 
TRANS_VRR_CTL_C = 0x62420 
TRANS_VRR_CTL_D = 0x63420 
TRANS_VRR_CTL_EDP = 0x6F420 


##
# Register bitfield definition structure
class TransVrrCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("pipeline_full_override", ctypes.c_uint32, 1),                     # 0 to 0
        ("reserved_1", ctypes.c_uint32, 2),                                 # 1 to 2
        ("framestart_to_pipeline_full_linecount", ctypes.c_uint32, 8),      # 3 to 10
        ("reserved_2", ctypes.c_uint32, 18),                                # 11 to 28
        ("flip_line_enable", ctypes.c_uint32, 1),                           # 29 to 29
        ("ignore_max_shift", ctypes.c_uint32, 1),                           # 30 to 30
        ("vrr_enable", ctypes.c_uint32, 1),                                 # 31 to 31
    ]


class TRANS_VRR_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
