import ctypes
# Bspec link : https://gfxspecs.intel.com/Predator/Home/Index/50216
 
'''
Register instance and offset 
'''
FBC_CTL_A = 0x43208
FBC_CTL_B = 0x43248
FBC_CTL_C = 0x43288
FBC_CTL_D = 0x432C8

'''
Register field expected values 
'''
fbc_enable_DISABLE = 0b0
fbc_enable_ENABLE = 0b1
fbc_compression_limit_1_1 = 0b00
fbc_compression_limit_2_1 = 0b01 
fbc_compression_limit_4_1 = 0b10
fbc_compression_limit_reserved = 0b00
fbc_plane_binding_plane_1      = 0b00
fbc_plane_binding_plane_2      = 0b01
fbc_plane_binding_plane_3      = 0b10
 
'''
Register bitfield definition structure
'''


class FBC_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cpu_fence_number"                 , ctypes.c_uint32, 4),  # 0 to 3
        ("write_Back_watermark"             , ctypes.c_uint32, 2),  # 4 to 5
        ("compression_limit"                , ctypes.c_uint32, 2),  # 6 to 7
        ("refill_fifo_write_watermark"      , ctypes.c_uint32, 2),  # 8 to 9
        ("flash_color_control"              , ctypes.c_uint32, 1),  # 10 to 10
        ("plane_binding"                    , ctypes.c_uint32, 2),  # 11 to 12
        ("reserved_11"                      , ctypes.c_uint32, 2),  # 13 to 14
        ("slb_flush_disable"                , ctypes.c_uint32, 1),  # 15 to 15
        ("disable_delta"                    , ctypes.c_uint32, 1),  # 16 to 16
        ("disable_pal"                      , ctypes.c_uint32, 1),  # 17 to 17
        ("disable_run"                      , ctypes.c_uint32, 1),  # 18 to 18
        ("reserved_19"                      , ctypes.c_uint32, 9),  # 19 to 27
        ("cpu_fence_enable"                 , ctypes.c_uint32, 1),  # 28 to 28
        ("reserved_29"                      , ctypes.c_uint32, 1),  # 29 to 29
        ("allow_db_stall"                   , ctypes.c_uint32, 1),  # 30 to 30
        ("enable_fbc"                       , ctypes.c_uint32, 1)   # 31 to 31
    ]

 
class FBC_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
