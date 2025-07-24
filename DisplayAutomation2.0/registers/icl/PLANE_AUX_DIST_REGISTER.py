import ctypes

'''
Register instance and offset 
'''
PLANE_AUX_DIST_1_A = 0x701C0
PLANE_AUX_DIST_2_A = 0x702C0
PLANE_AUX_DIST_3_A = 0x703C0
PLANE_AUX_DIST_4_A = 0x704C0
PLANE_AUX_DIST_5_A = 0x705C0
PLANE_AUX_DIST_6_A = 0x706C0
PLANE_AUX_DIST_7_A = 0x707C0
PLANE_AUX_DIST_1_B = 0x711C0
PLANE_AUX_DIST_2_B = 0x712C0
PLANE_AUX_DIST_3_B = 0x713C0
PLANE_AUX_DIST_4_B = 0x714C0
PLANE_AUX_DIST_5_B = 0x715C0
PLANE_AUX_DIST_6_B = 0x716C0
PLANE_AUX_DIST_7_B = 0x717C0
PLANE_AUX_DIST_1_C = 0x721C0
PLANE_AUX_DIST_2_C = 0x722C0
PLANE_AUX_DIST_3_C = 0x723C0
PLANE_AUX_DIST_4_C = 0x724C0
PLANE_AUX_DIST_5_C = 0x725C0
PLANE_AUX_DIST_6_C = 0x726C0
PLANE_AUX_DIST_7_C = 0x727C0

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class PLANE_AUX_DIST_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("auxiliary_surface_stride",    ctypes.c_uint32, 10),  # 0 to 9
        ("reserved_10",                 ctypes.c_uint32, 2),  # 10 to 11
        ("auxiliary_surface_distance",  ctypes.c_uint32, 20),  # 12 to 31
    ]


class PLANE_AUX_DIST_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PLANE_AUX_DIST_REG),
        ("asUint", ctypes.c_uint32)]
