import ctypes
 
'''
Register instance and offset 
'''
PORT_PLL_0_A = 0x162100 
PORT_PLL_0_B = 0x6C100 
PORT_PLL_0_C = 0x163100 

 
'''
Register field expected values 
'''
i_fbdivratio_DEFAULT = 0b00011111 
i_fracdiv_DEFAULT = 0b1001100110011001100110 
i_fracnen_h_DEFAULT = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PORT_PLL_0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("i_fbdivratio" , ctypes.c_uint32, 8), # 0 to 7 
        ("i_fracdiv"   , ctypes.c_uint32, 22), # 8 to 29 
        ("i_fracnen_h" , ctypes.c_uint32, 1), # 30 to 30 
        ("reserved_31" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PORT_PLL_0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_PLL_0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
