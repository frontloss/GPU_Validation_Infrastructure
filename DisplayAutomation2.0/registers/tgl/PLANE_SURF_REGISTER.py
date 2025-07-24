import ctypes
 
'''
Register instance and offset 
'''
PLANE_SURF_1_A = 0x7019C 
PLANE_SURF_1_B = 0x7119C 
PLANE_SURF_1_C = 0x7219C
PLANE_SURF_1_D = 0x7319C
PLANE_SURF_2_A = 0x7029C 
PLANE_SURF_2_B = 0x7129C 
PLANE_SURF_2_C = 0x7229C
PLANE_SURF_2_D = 0x7329C
PLANE_SURF_3_A = 0x7039C 
PLANE_SURF_3_B = 0x7139C 
PLANE_SURF_3_C = 0x7239C
PLANE_SURF_3_D = 0x7339C
PLANE_SURF_4_A = 0x7049C 
PLANE_SURF_4_B = 0x7149C 
PLANE_SURF_4_C = 0x7249C
PLANE_SURF_4_D = 0x7349C
PLANE_SURF_5_A = 0x7059C
PLANE_SURF_5_B = 0x7159C
PLANE_SURF_5_C = 0x7259C
PLANE_SURF_5_D = 0x7359C
PLANE_SURF_6_A = 0x7069C
PLANE_SURF_6_B = 0x7169C
PLANE_SURF_6_C = 0x7269C
PLANE_SURF_6_D = 0x7369C
PLANE_SURF_7_A = 0x7079C
PLANE_SURF_7_B = 0x7179C
PLANE_SURF_7_C = 0x7279C
PLANE_SURF_7_D = 0x7379C

 
'''
Register field expected values 
'''
decryption_request_NOT_REQUESTED = 0b0 
decryption_request_REQUESTED = 0b1 
key_select_ID_1 = 0b001 
key_select_PAVP = 0b000 
key_select_RESERVED = 0b0 
ring_flip_source_BCS = 0b1 
ring_flip_source_CS = 0b0 
vrr_master_flip_DISABLE = 0b0 
vrr_master_flip_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PLANE_SURF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"          , ctypes.c_uint32, 2), # 0 to 1 
        ("decryption_request"  , ctypes.c_uint32, 1), # 2 to 2 
        ("ring_flip_source"    , ctypes.c_uint32, 1), # 3 to 3 
        ("key_select"          , ctypes.c_uint32, 3), # 4 to 6 
        ("reserved_7"          , ctypes.c_uint32, 4), # 7 to 10 
        ("vrr_master_flip"     , ctypes.c_uint32, 1), # 11 to 11 
        ("surface_base_address" , ctypes.c_uint32, 20), # 12 to 31 
    ]

 
class PLANE_SURF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_SURF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
