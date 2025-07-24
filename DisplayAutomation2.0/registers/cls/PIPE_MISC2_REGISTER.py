import ctypes
 
'''
Register instance and offset 
'''
PIPE_MISC2_A = 0x7002C
PIPE_MISC2_B = 0x7102C
PIPE_MISC2_C = 0x7202C
PIPE_MISC2_D = 0x7302C

 
'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''
class PIPE_MISC2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("flip_info_plane_select"             , ctypes.c_uint32, 3), # 2 to 0
        ("reserved_3"                         , ctypes.c_uint32, 1), # 3 to 3
        ("scanline_plane_select"              , ctypes.c_uint32, 3), # 6 to 4
        ("reserved_7"                         , ctypes.c_uint32, 1), # 7 to 7
        ("asfu_flip_exception"                , ctypes.c_uint32, 1), # 8 to 8
        ("reserved_10"                        , ctypes.c_uint32, 2), # 10 to 9
		("yuv_422_mode"                       , ctypes.c_uint32, 1), # 11 to 11
        ("ipc_demote_req_chunk_size"          , ctypes.c_uint32, 4), # 15 to 12
        ("underrun_replacement_pixel_value"   , ctypes.c_uint32, 3), # 18 to 16
        ("underrun_manual_pixel_override"     , ctypes.c_uint32, 1), # 19 to 19
        ("reserved_23"                       ,  ctypes.c_uint32, 6),  # 23 to 18
        ("underrun_bubble_counter"            , ctypes.c_uint32, 8), # 31 to 24
    ]

 
class PIPE_MISC2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_MISC2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
