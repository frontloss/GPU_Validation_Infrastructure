import ctypes
 
'''
Register instance and offset 
'''
TRANS_VRR_STATUS_A = 0x6042C 
TRANS_VRR_STATUS_B = 0x6142C 
TRANS_VRR_STATUS_C = 0x6242C 
TRANS_VRR_STATUS_D = 0x6342C 
TRANS_VRR_STATUS_EDP = 0x6F42C 

 
'''
Register field expected values 
'''
flip_before_decision_boundary_DEFAULT = 0b1 
flips_serviced_DEFAULT = 0b1 
no_flip_frame_DEFAULT = 0b1 
no_flip_till_decision_boundary_DEFAULT = 0b1 
vmax_reached_NOT_REACHED = 0b0 
vmax_reached_REACHED = 0b1 
vrr_enable_live_DISABLED = 0b0 
vrr_enable_live_ENABLED = 0b1 

 
'''
Register bitfield defnition structure 
'''
class TRANS_VRR_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                    , ctypes.c_uint32, 20), # 0 to 19 
        ("current_region_in_vblank"      , ctypes.c_uint32, 3), # 20 to 22 
        ("reserved_23"                   , ctypes.c_uint32, 3), # 23 to 25 
        ("flips_serviced"                , ctypes.c_uint32, 1), # 26 to 26 
        ("vrr_enable_live"               , ctypes.c_uint32, 1), # 27 to 27 
        ("no_flip_frame"                 , ctypes.c_uint32, 1), # 28 to 28 
        ("flip_before_decision_boundary" , ctypes.c_uint32, 1), # 29 to 29 
        ("no_flip_till_decision_boundary" , ctypes.c_uint32, 1), # 30 to 30 
        ("vmax_reached"                  , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class TRANS_VRR_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VRR_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
