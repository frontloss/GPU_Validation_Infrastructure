import ctypes
 
'''
Register instance and offset 
'''
PIPE_DSS_CTL1_PA = 0x78000
PIPE_DSS_CTL1_PB = 0x78200
PIPE_DSS_CTL1_PC = 0x78400
PIPE_DSS_CTL1_PD = 0x78600

 
'''
Register field expected values 
'''
dual_link_mode_FRONT_BACK_MODE = 0b0 
dual_link_mode_INTERLEAVE_MODE = 0b1
master_big_joiner_enable_SLAVE = 0b0
master_big_joiner_enable_MASTER = 0b1
big_joiner_enable_DISABLE = 0b0
big_joiner_enable_ENABLE = 0b1
joiner_enable_DISABLE = 0b0 
joiner_enable_ENABLE = 0b1 
splitter_enable_DISABLE = 0b0 
splitter_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PIPE_DSS_CTL1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("left_dl_buffer_target_depth" , ctypes.c_uint32, 12), # 0 to 11
        ("reserved_12"                ,  ctypes.c_uint32, 4), # 12 to 15
        ("overlap"                    ,  ctypes.c_uint32, 4), # 16 to 19
        ("uncompressed_joiner_slave",    ctypes.c_uint32, 1), # 20 to 20
        ("uncompressed_joiner_master",   ctypes.c_uint32, 1), # 21 to 21
        ("reserved_22",                  ctypes.c_uint32, 2), # 22 to 23
        ("dual_link_mode"             ,  ctypes.c_uint32, 1), # 24 to 24
        ("splitter_configuration"     ,  ctypes.c_uint32, 2), # 25 to 26
        ("vga_centering_enable"       ,  ctypes.c_uint32, 1), # 27 to 27
        ("master_big_joiner_enable"   ,  ctypes.c_uint32, 1), # 28 to 28
        ("big_joiner_enable"          ,  ctypes.c_uint32, 1), # 29 to 29
        ("joiner_enable"              ,  ctypes.c_uint32, 1), # 30 to 30
        ("splitter_enable"            ,  ctypes.c_uint32, 1), # 31 to 31
    ]


class PIPE_DSS_CTL1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DSS_CTL1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
