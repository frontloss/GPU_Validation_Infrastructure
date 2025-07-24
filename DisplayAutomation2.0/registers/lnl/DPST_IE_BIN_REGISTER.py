import ctypes

##
# Register instance and offset
DPST_IE_BIN_A = 0x490CC
DPST_IE_BIN_B = 0x491CC
DPST_IE_BIN_C = 0x492CC
DPST_IE_BIN_D = 0x493CC


##
# Register bitfield definition structure
class DpstIeBinReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("data", ctypes.c_uint32, 10),  # 0 to 9
        ("reserved", ctypes.c_uint32, 6),  # 10 to 15
        ("residual", ctypes.c_uint32, 10),  # 16 to 25
        ("reserved", ctypes.c_uint32, 6),  # 26 to 31)
    ]


class DPST_IE_BIN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstIeBinReg),
        ("asUint", ctypes.c_uint32)
    ]