import ctypes
 
'''
Register instance and offset 
'''
DC_STATE_EN = 0x45504


 
'''
Register field expected values 
'''
dc_state_enable_DISABLE          = 0b00
dc_state_enable_ENABLE_UPTO_DC5  = 0b01
dc_state_enable_ENABLE_UPTO_DC6  = 0b10
dc9_allow_DO_NOT_ALLOW           = 0b0
dc9_allow_ALLOW                  = 0b1

 
'''
Register bitfield defnition structure 
'''
class DC_STATE_EN_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dc_state_enable"          , ctypes.c_uint32, 2), # 0 to 1
        ("reserved_2"               , ctypes.c_uint32, 1), # 2 to 2
        ("reserved_3"               , ctypes.c_uint32, 1), # 3 to 3
        ("mask_poke"                , ctypes.c_uint32, 1), # 4 to 4
        ("reserved_5"               , ctypes.c_uint32, 3), # 5 to 7
        ("block_outbound_traffic"   , ctypes.c_uint32, 1), # 8 to 8 
        ("in_csr_flow"              , ctypes.c_uint32, 1), # 9 to 9
        ("reserved_10"              , ctypes.c_uint32, 22) # 10 to 31 
    ]

 
class DC_STATE_EN_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DC_STATE_EN_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
