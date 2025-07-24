import ctypes
 
'''
Register instance and offset 
'''
MIPIA_LP_RX_TIMEOUT_REG = 0x6B014 
MIPIC_LP_RX_TIMEOUT_REG = 0x6B814 

 
'''
Register field expected values 
'''
low_power_reception_timeout_counter_DEFAULT = 0x00FFFF

 
'''
Register bitfield defnition structure 
'''
class MIPI_LP_RX_TIMEOUT_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("low_power_reception_timeout_counter" , ctypes.c_uint32, 24), # 0 to 23 
        ("reserved_24"                        , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class MIPI_LP_RX_TIMEOUT_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_LP_RX_TIMEOUT_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
