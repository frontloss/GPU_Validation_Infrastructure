
import ctypes
 
'''
Register instance and offset 
'''
PS_COEF_SET_0_INDEX_1_A = 0x68198
PS_COEF_SET_0_INDEX_1_B = 0x68998
PS_COEF_SET_0_INDEX_1_C = 0x69198
PS_COEF_SET_0_INDEX_1_D = 0x69998
PS_COEF_SET_0_INDEX_2_A = 0x68298
PS_COEF_SET_0_INDEX_2_B = 0x68A98
PS_COEF_SET_0_INDEX_2_C = 0x69298
PS_COEF_SET_0_INDEX_2_D = 0x69A98
PS_COEF_SET_1_INDEX_1_A = 0x681A0
PS_COEF_SET_1_INDEX_1_B = 0x689A0
PS_COEF_SET_1_INDEX_1_C = 0x691A0
PS_COEF_SET_1_INDEX_1_D = 0x699A0
PS_COEF_SET_1_INDEX_2_A = 0x682A0
PS_COEF_SET_1_INDEX_2_B = 0x68AA0
PS_COEF_SET_1_INDEX_2_C = 0x692A0
PS_COEF_SET_1_INDEX_2_D = 0x69AA0

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''
class PS_COEF_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value", ctypes.c_uint32, 6),  # 0 to 5
        ("reserved_6", ctypes.c_uint32, 4),  # 6 to 9
        ("index_auto_increment", ctypes.c_uint32, 1),  # 10 to 10
        ("reserved_11", ctypes.c_uint32, 21),  # 11 to 31
    ]

 
class PS_COEF_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_COEF_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
