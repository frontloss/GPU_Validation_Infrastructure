import ctypes
 
##
# Register instance and offset
TRANS_VRR_VMAX_A = 0x60424
TRANS_VRR_VMAX_B = 0x61424
TRANS_VRR_VMAX_C = 0x62424
TRANS_VRR_VMAX_D = 0x63424 
TRANS_VRR_VMAX_EDP = 0x6F424

 
##
# Register bitfield definition structure
class TransVrrVMaxReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vrr_vmax", ctypes.c_uint32, 20),      # 0 to 19
        ("reserved_20", ctypes.c_uint32, 12),   # 20 to 31
    ]

 
class TRANS_VRR_VMAX_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransVrrVMaxReg),
        ("asUint", ctypes.c_uint32)
    ]
