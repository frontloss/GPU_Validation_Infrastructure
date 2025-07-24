import ctypes
 
##
# Register instance and offset
TRANS_VRR_CTL_A = 0x60420
TRANS_VRR_CTL_B = 0x61420 
TRANS_VRR_CTL_C = 0x62420 
TRANS_VRR_CTL_D = 0x63420 
TRANS_VRR_CTL_CMTG0 = 0x6F420
TRANS_VRR_CTL_CMTG1 = 0x6F520


##
# Register bitfield definition structure
class TransVrrCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vrr_guard_band", ctypes.c_uint32, 16),               # 0 to 15
        ("reserved_16", ctypes.c_uint32, 9),                   # 16 to 24
        ("adaptive_sync_cfg_select", ctypes.c_uint32, 1),      # 25 to 25
        ("adaptive_sync_status", ctypes.c_uint32, 1),          # 26 to 26
        ("cmrr_enable", ctypes.c_uint32, 1),                   # 27 to 27
        ("dcb_adj_enable", ctypes.c_uint32, 1),                # 28 to 28
        ("flipline_enable", ctypes.c_uint32, 1),               # 29 to 29
        ("reserved_30", ctypes.c_uint32, 1),                   # 30 to 30
        ("vrr_enable", ctypes.c_uint32, 1),                    # 31 to 31
    ]


class TRANS_VRR_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
