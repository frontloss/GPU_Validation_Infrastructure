import ctypes
 
##
# Register instance and offset
DPST_CTL_A = 0x490C0
DPST_CTL_B = 0x491C0
DPST_CTL_C = 0x492C0
DPST_CTL_D = 0x493C0


##
# Register bitfield definition structure
class DpstCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("bin_register_index", ctypes.c_uint32, 7),                         # 0 to 6
        ("reserved_1", ctypes.c_uint32, 4),                                 # 7 to 10
        ("bin_register_function_select", ctypes.c_uint32, 1),               # 11
        ("reserved_2", ctypes.c_uint32, 1),                                 # 12
        ("enhancement_mode", ctypes.c_uint32, 2),                           # 13 to 14
        ("ie_table_value_format", ctypes.c_uint32, 1),                      # 15
        ("reserved_3", ctypes.c_uint32, 8),                                 # 16 to 23
        ("histogram_mode_select", ctypes.c_uint32, 1),                      # 24
        ("reserved_4", ctypes.c_uint32, 2),                                 # 25 to 26
        ("ie_modification_table_enable", ctypes.c_uint32, 1),               # 27
        ("reserved_5", ctypes.c_uint32, 3),                                 # 28 to 30
        ("ie_histogram_enable", ctypes.c_uint32, 1),                        # 31
    ]


class DPST_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
