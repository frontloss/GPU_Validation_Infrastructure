import ctypes
 
'''
Register instance and offset 
'''
DSI_IO_MODECTL_DSI0 = 0x6B094 
DSI_IO_MODECTL_DSI1 = 0x6B894 

 
'''
Register field expected values 
'''
combo_phy_mode_DDI_MODE = 0b0 
combo_phy_mode_MIPI_DSI_MODE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DSI_IO_MODECTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("combo_phy_mode" , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"    , ctypes.c_uint32, 31), # 1 to 31 
    ]

 
class DSI_IO_MODECTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_IO_MODECTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
