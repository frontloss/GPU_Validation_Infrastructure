import ctypes
 
'''
Register instance and offset 
'''
MIPIA_CTRL = 0x6B104 
MIPIC_CTRL = 0x6B904 

 
'''
Register field expected values 
'''
dsc_enable_DSC_DISABLE = 0b0 
dsc_enable_DSC_ENABLE = 0b1 
mipi_mode_DISABLE_MIPI_IO_BLOCK = 0b0 
mipi_mode_ENABLE_MIPI_IO_BLOCK = 0b1 
mipio_reset_MIPI_IO_BLOCK_IN_RESET_STATE = 0b1 
mipio_reset_MIPI_IO_BLOCK_RELEASED_FROM_RESET_STATE = 0b0 
phy_status_MIPI_PORT_NOT_READY = 0b0 
phy_status_MIPI_PORT_READY = 0b1 
pipe_select_PIPE_A = 0b000 
pipe_select_PIPE_B = 0b001 
pipe_select_PIPE_C = 0b010 
pipe_select_RESERVED = 0b0 
power_ack_MIPIO_PORT_IS_POWERED = 0b1 
power_ack_MIPIO_PORT_IS_POWERGATED = 0b0 
rgb_flip_DISABLE = 0b1 
rgb_flip_ENABLE = 0b0 
ulps_not_active_MIPI_LANES_IN_ULPS_STATE = 0b0 
ulps_not_active_MIPI_LANES_NOT_IN_ULPS_STATE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class MIPI_CTRL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"         , ctypes.c_uint32, 2), # 0 to 1 
        ("rgb_flip"           , ctypes.c_uint32, 1), # 2 to 2 
        ("dsc_enable"         , ctypes.c_uint32, 1), # 3 to 3 
        ("reserved_4"         , ctypes.c_uint32, 3), # 4 to 6 
        ("pipe_select"        , ctypes.c_uint32, 3), # 7 to 9 
        ("z_inversion_overlap" , ctypes.c_uint32, 4), # 10 to 13 
        ("reserved_14"        , ctypes.c_uint32, 2), # 14 to 15 
        ("reserved_16"        , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"        , ctypes.c_uint32, 3), # 17 to 19 
        ("reserved_20"        , ctypes.c_uint32, 3), # 20 to 22 
        ("reserved_23"        , ctypes.c_uint32, 2), # 23 to 24 
        ("reserved_25"        , ctypes.c_uint32, 1), # 25 to 25 
        ("reserved_26"        , ctypes.c_uint32, 2), # 26 to 27 
        ("reserved_28"        , ctypes.c_uint32, 1), # 28 to 28 
        ("reserved_29"        , ctypes.c_uint32, 1), # 29 to 29 
        ("reserved_30"        , ctypes.c_uint32, 1), # 30 to 30 
        ("reserved_31"        , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class MIPI_CTRL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_CTRL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
