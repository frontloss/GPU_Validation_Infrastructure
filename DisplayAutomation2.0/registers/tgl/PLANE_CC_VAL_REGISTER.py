import ctypes

'''
Register instance and offset 
'''
PLANE_CC_VAL_1_A = 0x701B4
PLANE_CC_VAL_2_A = 0x702B4
PLANE_CC_VAL_3_A = 0x703B4
PLANE_CC_VAL_4_A = 0x704B4
PLANE_CC_VAL_5_A = 0x705B4
PLANE_CC_VAL_6_A = 0x706B4
PLANE_CC_VAL_7_A = 0x707B4
PLANE_CC_VAL_1_B = 0x711B4
PLANE_CC_VAL_2_B = 0x712B4
PLANE_CC_VAL_3_B = 0x713B4
PLANE_CC_VAL_4_B = 0x714B4
PLANE_CC_VAL_5_B = 0x715B4
PLANE_CC_VAL_6_B = 0x716B4
PLANE_CC_VAL_7_B = 0x717B4
PLANE_CC_VAL_1_C = 0x721B4
PLANE_CC_VAL_2_C = 0x722B4
PLANE_CC_VAL_3_C = 0x723B4
PLANE_CC_VAL_4_C = 0x724B4
PLANE_CC_VAL_5_C = 0x725B4
PLANE_CC_VAL_6_C = 0x726B4
PLANE_CC_VAL_7_C = 0x727B4
PLANE_CC_VAL_1_D = 0x731B4
PLANE_CC_VAL_2_D = 0x732B4
PLANE_CC_VAL_3_D = 0x733B4
PLANE_CC_VAL_4_D = 0x734B4
PLANE_CC_VAL_5_D = 0x735B4
PLANE_CC_VAL_6_D = 0x736B4
PLANE_CC_VAL_7_D = 0x737B4

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class PLANE_CC_VAL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('clearcolorvaluedw0', ctypes.c_uint32, 32),  # 0 to 31
    ]


class PLANE_CC_VAL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PLANE_CC_VAL_REG),
        ("asUint", ctypes.c_uint32)]
