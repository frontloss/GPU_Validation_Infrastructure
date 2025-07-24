import ctypes
 
'''
Register instance and offset 
'''

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PIPE_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dirty_block_plane_1" , ctypes.c_uint32, 1), # 0 to 0 
        ("dirty_block_plane_2" , ctypes.c_uint32, 1), # 1 to 1 
        ("dirty_block_plane_3" , ctypes.c_uint32, 1), # 2 to 2 
        ("dirty_block_plane_4" , ctypes.c_uint32, 1), # 3 to 3 
        ("dirty_block_plane_5" , ctypes.c_uint32, 1), # 4 to 4 
        ("dirty_block_plane_6" , ctypes.c_uint32, 1), # 5 to 5 
        ("dirty_block_plane_7" , ctypes.c_uint32, 1), # 6 to 6 
        ("not_used"           , ctypes.c_uint32, 1), # 7 to 7 
        ("frame_start"        , ctypes.c_uint32, 1), # 29 to 29 
        ("vblank"             , ctypes.c_uint32, 1), # 30 to 30 
        ("underrun"           , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PIPE_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
