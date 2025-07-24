import ctypes
 
'''
Register instance and offset 
'''
PORT_PLL_2_A = 0x162108 
PORT_PLL_2_B = 0x6C108 
PORT_PLL_2_C = 0x163108 

 
'''
Register field expected values 
'''
i_feedfwrdcal_en_h_DEFAULT = 0b1 
i_feedfwrdgain_DEFAULT = 0b01010101 
i_sscen_h_DEFAULT = 0b1 
i_sscstepsize_DEFAULT = 0b0000011110 

 
'''
Register bitfield defnition structure 
'''
class PORT_PLL_2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("i_feedfwrdgain"       , ctypes.c_uint32, 8), # 0 to 7 
        ("i_feedfwrdcal_en_h"   , ctypes.c_uint32, 1), # 8 to 8 
        ("i_feedfwrdcal_pause_h" , ctypes.c_uint32, 1), # 9 to 9 
        ("i_sscen_h"            , ctypes.c_uint32, 1), # 10 to 10 
        ("reserved_11"          , ctypes.c_uint32, 5), # 11 to 15 
        ("i_sscstepsize"        , ctypes.c_uint32, 10), # 16 to 25 
        ("reserved_26"          , ctypes.c_uint32, 6), # 26 to 31 
    ]

 
class PORT_PLL_2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_PLL_2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
