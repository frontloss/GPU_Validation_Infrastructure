import ctypes
 
'''
Register instance and offset 
'''
DISPIO_CR_TX_BMU_CR0 = 0x6C00C 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DISPIO_CR_TX_BMU_CR0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("tx_h_mode"             , ctypes.c_uint32, 8), # 0 to 7 
        ("tx_blnclegsctl_0"      , ctypes.c_uint32, 3), # 8 to 10 
        ("tx_blnclegsctl_1"      , ctypes.c_uint32, 3), # 11 to 13 
        ("tx_blnclegsctl_2"      , ctypes.c_uint32, 3), # 14 to 16 
        ("tx_blnclegsctl_3"      , ctypes.c_uint32, 3), # 17 to 19 
        ("tx_blnclegsctl_4"      , ctypes.c_uint32, 3), # 20 to 22 
        ("tx_blnclegdisbl"       , ctypes.c_uint32, 5), # 23 to 27 
        ("tx_glb_vs_loc_vref_sel" , ctypes.c_uint32, 1), # 28 to 28 
        ("digital_analog"        , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class DISPIO_CR_TX_BMU_CR0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DISPIO_CR_TX_BMU_CR0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
