import ctypes
 
'''
Register instance and offset 
'''
MIPIA_STATUS = 0x6B0C4 
MIPIC_STATUS = 0x6B8C4 

 
'''
Register field expected values 
'''
sideband_te_NO_TE = 0b0 
sideband_te_TE = 0b1 
mipi_idle_MIPI_IDLE = 0b1 
mipi_idle_MIPI_NOT_IDLE = 0b0 
te_message_in_lp_mode_NO_TE = 0b0 
te_message_in_lp_mode_TE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class MIPI_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"           , ctypes.c_uint32, 29), # 0 to 28 
        ("mipi_idle"            , ctypes.c_uint32, 1), # 29 to 29 
        ("te_message_in_lp_mode" , ctypes.c_uint32, 1), # 30 to 30 
        ("_sideband_te"         , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class MIPI_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
