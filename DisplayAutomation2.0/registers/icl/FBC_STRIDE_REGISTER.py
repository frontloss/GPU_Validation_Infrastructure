import ctypes
 
'''
Register instance and offset
'''
FBC_STRIDE = 0x43228



 
'''
Register bitfield defnition structure
'''
class FBC_STRIDE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        
        ("override_stride"               , ctypes.c_uint32, 13), # 0  to 12
        ("spare_13"                      , ctypes.c_uint32, 1), # 13 to 13
        ("spare_14"                      , ctypes.c_uint32, 1), # 14 to 14
        ("override_stride_enable"        , ctypes.c_uint32, 1), # 15 to 15
        ("spare_16"                      , ctypes.c_uint32, 1), # 16 to 16
        ("spare_17"                      , ctypes.c_uint32, 1), # 17 to 17
        ("spare_18"                      , ctypes.c_uint32, 1), # 18 to 18
        ("spare_19"                      , ctypes.c_uint32, 1), # 19 to 19
        ("spare_20"                      , ctypes.c_uint32, 1), # 20 to 20
        ("spare_21"                      , ctypes.c_uint32, 1), # 21 to 21
        ("spare_22"                      , ctypes.c_uint32, 1), # 22 to 22
        ("spare_23"                      , ctypes.c_uint32, 1), # 23 to 23
        ("spare_24"                      , ctypes.c_uint32, 1), # 24 to 24
        ("spare_25"                      , ctypes.c_uint32, 1), # 25 to 25
        ("spare_26"                      , ctypes.c_uint32, 1), # 26 to 26
        ("spare_27"                      , ctypes.c_uint32, 1), # 27 to 27
        ("spare_28 "                     , ctypes.c_uint32, 1), # 28 to 28
        ("spare_29"                      , ctypes.c_uint32, 1), # 29 to 29
        ("spare_30"                      , ctypes.c_uint32, 1), # 30 to 30
        ("spare_31"                      , ctypes.c_uint32, 1), # 31 to 31
    ]

 
class FBC_STRIDE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_STRIDE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
