import ctypes

##
# Register instance and offset
TRANS_PUSH_A = 0x60A70
TRANS_PUSH_B = 0x61A70
TRANS_PUSH_C = 0x62A70
TRANS_PUSH_D = 0x63A70
TRANS_PUSH_CMTG0 = 0x6F430
TRANS_PUSH_CMTG1 = 0x6F530

 
##
# Register bitfield definition structure
class TransPushReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0"                 , ctypes.c_uint32, 16),    # 0 to 15
        ("psr_pr_frame_change_enable" , ctypes.c_uint32, 1),     # 16 to 16
        ("reserved_17"                , ctypes.c_uint32, 13),    # 17 to 29
        ("send_push"                  , ctypes.c_uint32, 1),     # 30 to 30
        ("push_enable"                , ctypes.c_uint32, 1),     # 31 to 31
    ]

 
class TRANS_PUSH_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransPushReg),
        ("asUint", ctypes.c_uint32)
    ]
