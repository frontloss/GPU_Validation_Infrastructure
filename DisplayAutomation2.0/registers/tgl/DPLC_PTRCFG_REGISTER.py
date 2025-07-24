import ctypes
 
'''
Register instance and offset 
'''
DPLC_PTRCFG_PARTA_A = 0x49434 
DPLC_PTRCFG_PARTA_B = 0x494B4 
DPLC_PTRCFG_PARTB_A = 0x49438 
DPLC_PTRCFG_PARTB_B = 0x494B8 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DPLC_PTRCFG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dw_index", ctypes.c_uint32, 5),  # 0 to 4
        ("reserved_5", ctypes.c_uint32, 3),  # 5 to 7
        ("x_index", ctypes.c_uint32, 4),  # 8 to 11
        ("reserved_12", ctypes.c_uint32, 1),  # 12 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("y_index", ctypes.c_uint32, 4),  # 16 to 19
        ("reserved_20", ctypes.c_uint32, 1),  # 20 to 20
        ("reserved_21", ctypes.c_uint32, 11),  # 21 to 31
    ]

 
class DPLC_PTRCFG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLC_PTRCFG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
