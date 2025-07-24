import ctypes

##
# Register instance and offset
TRANS_VRR_FLIPLINE_A = 0x60438
TRANS_VRR_FLIPLINE_B = 0x61438
TRANS_VRR_FLIPLINE_C = 0x62438
TRANS_VRR_FLIPLINE_D = 0x63438
TRANS_VRR_FLIPLINE_CMTG0 = 0x6F438
TRANS_VRR_FLIPLINE_CMTG1 = 0x6F538

 
##
# Register bitfield definition structure
class TransVrrFlipLineReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vrr_flipline", ctypes.c_uint32, 20),      # 0 to 19
        ("reserved_16", ctypes.c_uint32, 12),   # 20 to 31
    ]

 
class TRANS_VRR_FLIPLINE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrFlipLineReg),
        ("asUint", ctypes.c_uint32)
    ]
