import ctypes
 
'''
Register instance and offset 
'''
PLANE_CUS_CTL_1_A = 0x701C8 
PLANE_CUS_CTL_1_B = 0x711C8 
PLANE_CUS_CTL_1_C = 0x721C8 
PLANE_CUS_CTL_2_A = 0x702C8 
PLANE_CUS_CTL_2_B = 0x712C8 
PLANE_CUS_CTL_2_C = 0x722C8 
PLANE_CUS_CTL_3_A = 0x703C8 
PLANE_CUS_CTL_3_B = 0x713C8 
PLANE_CUS_CTL_3_C = 0x723C8 
PLANE_CUS_CTL_1_D = 0x731C8
PLANE_CUS_CTL_2_D = 0x732C8
PLANE_CUS_CTL_3_D = 0x733C8

 
'''
Register field expected values 
'''
chroma_upsampler_enable_DISABLE = 0b0 
chroma_upsampler_enable_ENABLE = 0b1 
horz_initial_phase_0 = 0b00 
horz_initial_phase_0_25 = 0b01 
horz_initial_phase_0_5 = 0b10 
horz_initial_phase_RESERVED = 0b0 
horz_initial_phase_sign_NEGATIVE_INITIAL_PHASE = 0b1 
horz_initial_phase_sign_POSITIVE_INITIAL_PHASE = 0b0 
power_gate_disable_DISABLE = 0b1 
power_gate_disable_ENABLE = 0b0 
vert_initial_phase_0 = 0b00 
vert_initial_phase_0_25 = 0b01 
vert_initial_phase_0_5 = 0b10 
vert_initial_phase_RESERVED = 0b0 
vert_initial_phase_sign_NEGATIVE_INITIAL_PHASE = 0b1 
vert_initial_phase_sign_POSITIVE_INITIAL_PHASE = 0b0 
y_binding_PLANE_6 = 0b0 
y_binding_PLANE_7 = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PLANE_CUS_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("power_up_in_progress"   , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"             , ctypes.c_uint32, 3), # 1 to 3 
        ("ecc_double_error"       , ctypes.c_uint32, 1), # 4 to 4 
        ("ecc_single_error"       , ctypes.c_uint32, 1), # 5 to 5 
        ("reserved_6"             , ctypes.c_uint32, 2), # 6 to 7 
        ("ecc_bypass"             , ctypes.c_uint32, 1), # 8 to 8 
        ("power_up_delay"         , ctypes.c_uint32, 2), # 9 to 10 
        ("power_gate_disable"     , ctypes.c_uint32, 1), # 11 to 11 
        ("vert_initial_phase"     , ctypes.c_uint32, 2), # 12 to 13 
        ("reserved_14"            , ctypes.c_uint32, 1), # 14 to 14 
        ("vert_initial_phase_sign" , ctypes.c_uint32, 1), # 15 to 15 
        ("horz_initial_phase"     , ctypes.c_uint32, 2), # 16 to 17 
        ("reserved_18"            , ctypes.c_uint32, 1), # 18 to 18 
        ("horz_initial_phase_sign" , ctypes.c_uint32, 1), # 19 to 19 
        ("reserved_20"            , ctypes.c_uint32, 10), # 20 to 29 
        ("y_binding"              , ctypes.c_uint32, 1), # 30 to 30 
        ("chroma_upsampler_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PLANE_CUS_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CUS_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
