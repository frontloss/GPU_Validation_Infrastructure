import ctypes
 
'''
Register instance and offset 
'''
DPHY_DATA_TIMING_PARAM_DSI0 = 0x162184 
DPHY_DATA_TIMING_PARAM_DSI1 = 0x06C184 


 
'''
Register field expected values 
'''
hs_exit_override_HW_MAINTAINS = 0 
hs_exit_override_SW_OVERRIDES = 1 
hs_prepare_0_25_ESCAPE_CLOCKS = 0b001 
hs_prepare_0_50_ESCAPE_CLOCKS = 0b010 
hs_prepare_0_75_ESCAPE_CLOCKS = 0b011 
hs_prepare_1_0_ESCAPE_CLOCKS = 0b100 
hs_prepare_1_25_ESCAPE_CLOCKS = 0b101 
hs_prepare_1_50_ESCAPE_CLOCKS = 0b110 
hs_prepare_1_75_ESCAPE_CLOCKS = 0b111 
hs_prepare_RESERVED = 0b0 
hs_prepare_override_HW_MAINTAINS = 0 
hs_prepare_override_SW_OVERRIDES = 1 
hs_trail_override_HW_MAINTAINS = 0 
hs_trail_override_SW_OVERRIDES = 1 
hs_zero_override_HW_MAINTAINS = 0 
hs_zero_override_SW_OVERRIDES = 1 

 
'''
Register bitfield defnition structure 
'''
class DPHY_DATA_TIMING_PARAM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("hs_exit"            , ctypes.c_uint32, 3), # 0 to 2 
        ("reserved_3"         , ctypes.c_uint32, 4), # 3 to 6 
        ("hs_exit_override"   , ctypes.c_uint32, 1), # 7 to 7 
        ("hs_trail"           , ctypes.c_uint32, 3), # 8 to 10 
        ("reserved_11"        , ctypes.c_uint32, 4), # 11 to 14 
        ("hs_trail_override"  , ctypes.c_uint32, 1), # 15 to 15 
        ("hs_zero"            , ctypes.c_uint32, 4), # 16 to 19 
        ("reserved_20"        , ctypes.c_uint32, 3), # 20 to 22 
        ("hs_zero_override"   , ctypes.c_uint32, 1), # 23 to 23 
        ("hs_prepare"         , ctypes.c_uint32, 3), # 24 to 26 
        ("reserved_27"        , ctypes.c_uint32, 4), # 27 to 30 
        ("hs_prepare_override" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DPHY_DATA_TIMING_PARAM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPHY_DATA_TIMING_PARAM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
