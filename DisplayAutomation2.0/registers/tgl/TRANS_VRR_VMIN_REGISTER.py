import ctypes

##
# Register instance and offset
TRANS_VRR_VMIN_A = 0x60434
TRANS_VRR_VMIN_B = 0x61434
TRANS_VRR_VMIN_C = 0x62434
TRANS_VRR_VMIN_D = 0x63434 
TRANS_VRR_VMIN_EDP = 0x6F434

 
##
# Register bitfield definition structure
class TransVrrVMinReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vrr_vmin", ctypes.c_uint32, 16),      # 0 to 15
        ("reserved_16", ctypes.c_uint32, 16),   # 16 to 31
    ]

 
class TRANS_VRR_VMIN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrVMinReg),
        ("asUint", ctypes.c_uint32)
    ]
