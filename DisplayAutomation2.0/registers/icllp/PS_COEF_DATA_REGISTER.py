
import ctypes
 
'''
Register instance and offset 
'''
PS_COEF_SET_0_DATA_1_A = 0x6819C
PS_COEF_SET_0_DATA_1_B = 0x6899C
PS_COEF_SET_0_DATA_1_C = 0x6919C
PS_COEF_SET_0_DATA_1_D = 0x6999C
PS_COEF_SET_0_DATA_2_A = 0x6829C
PS_COEF_SET_0_DATA_2_B = 0x68A9C
PS_COEF_SET_0_DATA_2_C = 0x6929C
PS_COEF_SET_0_DATA_2_D = 0x69A9C
PS_COEF_SET_1_DATA_1_A = 0x681A4
PS_COEF_SET_1_DATA_1_B = 0x689A4
PS_COEF_SET_1_DATA_1_C = 0x691A4
PS_COEF_SET_1_DATA_1_D = 0x699A4
PS_COEF_SET_1_DATA_2_A = 0x682A4
PS_COEF_SET_1_DATA_2_B = 0x68AA4
PS_COEF_SET_1_DATA_2_C = 0x692A4
PS_COEF_SET_1_DATA_2_D = 0x69AA4

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''
class PS_COEF_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coefficient1"                            , ctypes.c_uint32, 16), # 0 to 15
        ("coefficient2"                            , ctypes.c_uint32, 16), # 16 to 31
    ]

 
class PS_COEF_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_COEF_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
