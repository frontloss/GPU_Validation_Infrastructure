import ctypes
 
##
# Register instance and offset
DPST_GUARD_A = 0x490C8
DPST_GUARD_B = 0x491C8
DPST_GUARD_C = 0x492C8


##
# Register bitfield definition structure
class DpstGuardReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("threshold_guardband", ctypes.c_uint32, 22),           # 0 to 21
        ("guardband_interrupt_delay", ctypes.c_uint32, 8),      # 22 to 29
        ("histogram_event_status", ctypes.c_uint32, 1),         # 30
        ("histogram_interrupt_enable", ctypes.c_uint32, 1),     # 31
    ]


class DPST_GUARD_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstGuardReg),
        ("asUint", ctypes.c_uint32)
    ]
