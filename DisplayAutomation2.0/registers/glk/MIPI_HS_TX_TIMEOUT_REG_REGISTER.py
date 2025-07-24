import ctypes
 
'''
Register instance and offset 
'''
MIPIA_HS_TX_TIMEOUT_REG = 0x6B010 
MIPIC_HS_TX_TIMEOUT_REG = 0x6B810 

 
'''
Register field expected values 
'''
high_speed_tx_timeout_counter_DEFAULT = 0x00FFFF

 
'''
Register bitfield defnition structure 
'''
class MIPI_HS_TX_TIMEOUT_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("high_speed_tx_timeout_counter" , ctypes.c_uint32, 24), # 0 to 23 
        ("reserved_24"                  , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class MIPI_HS_TX_TIMEOUT_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_HS_TX_TIMEOUT_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
