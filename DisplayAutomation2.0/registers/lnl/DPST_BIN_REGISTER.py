import ctypes

##
# Register instance and offset
DPST_BIN_A = 0x490C4
DPST_BIN_B = 0x491C4
DPST_BIN_C = 0x492C4
DPST_BIN_D = 0x493C4


##
# Register bitfield definition structure
class DpstBinReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("data", ctypes.c_uint32, 24),  # 0 to 23
        ("reserved", ctypes.c_uint32, 7),  # 24 to 30
        ("busy_bit", ctypes.c_uint32, 1),  # 31
    ]


class DPST_BIN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstBinReg),
        ("asUint", ctypes.c_uint32)
    ]
