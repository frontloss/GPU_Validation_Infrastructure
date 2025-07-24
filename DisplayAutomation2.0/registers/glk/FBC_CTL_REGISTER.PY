import ctypes
 
'''
Register instance and offset 
'''
FBC_CTL = 0x43208


 
'''
Register field expected values 
'''
fbc_enable_DISABLE = 0b0 
fbc_enable_ENABLE = 0b1
fbc_compression_limit_1_1 = 0b00 
fbc_compression_limit_2_1 = 0b01 
fbc_compression_limit_4_1 = 0b10
fbc_compression_limit_reserved = 0b00

 
'''
Register bitfield defnition structure 
'''
class FBC_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cpu_fence_number"                 , ctypes.c_uint32, 4), # 0 to 3
        ("write_back_watermark"             , ctypes.c_uint32, 2), # 4 to 5
        ("compression_limit"                , ctypes.c_uint32, 2), # 6 to 7
        ("refill_ffio_write_watermark"      , ctypes.c_uint32, 2), # 8 to 9
        ("false_color_control"              , ctypes.c_uint32, 1), # 10 to 10
        ("reserved_11"                      , ctypes.c_uint32, 4), # 11 t0 14
        ("slb_init_flush_disable"           , ctypes.c_uint32, 1), # 15 to 15
        ("compression_control"              , ctypes.c_uint32, 9), # 16 to 24
        ("reserved_25"                      , ctypes.c_uint32, 3), # 25 to 27
        ("cpu_fence_enable"                 , ctypes.c_uint32, 1), # 28 to 28 
        ("reserved_29"                      , ctypes.c_uint32, 2), # 29 to 30 
        ("enable_fbc"                       , ctypes.c_uint32, 1) # 31 to 31 
    ]

 
class FBC_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
