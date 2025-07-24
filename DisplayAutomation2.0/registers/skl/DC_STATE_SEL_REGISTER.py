import ctypes
 
'''
Register instance and offset 
'''
DC_STATE_SEL = 0x45500 

 
'''
Register field expected values 
'''
dc_state_select_0 = 0b000 
dc_state_select_1 = 0b001 
dc_state_select_2 = 0b010 
dc_state_select_3 = 0b011 
dc_state_select_4 = 0b100 
dc_state_select_5 = 0b101 
dc_state_select_6 = 0b110 
dc_state_select_7 = 0b111 

 
'''
Register bitfield defnition structure 
'''
class DC_STATE_SEL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dc_state_select" , ctypes.c_uint32, 3), # 0 to 2 
        ("reserved_3"     , ctypes.c_uint32, 29), # 3 to 31 
    ]

 
class DC_STATE_SEL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DC_STATE_SEL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
