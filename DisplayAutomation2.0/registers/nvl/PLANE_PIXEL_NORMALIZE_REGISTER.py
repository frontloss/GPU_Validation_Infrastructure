import ctypes
 
'''
Register instance and offset 
'''
PLANE_PIXEL_NORMALIZE_1_A = 0x701A8 
PLANE_PIXEL_NORMALIZE_1_B = 0x711A8 
PLANE_PIXEL_NORMALIZE_1_C = 0x721A8 
PLANE_PIXEL_NORMALIZE_2_A = 0x702A8 
PLANE_PIXEL_NORMALIZE_2_B = 0x712A8 
PLANE_PIXEL_NORMALIZE_2_C = 0x722A8 
PLANE_PIXEL_NORMALIZE_3_A = 0x703A8 
PLANE_PIXEL_NORMALIZE_3_B = 0x713A8 
PLANE_PIXEL_NORMALIZE_3_C = 0x723A8 
PLANE_PIXEL_NORMALIZE_1_D = 0x731A8
PLANE_PIXEL_NORMALIZE_2_D = 0x732A8
PLANE_PIXEL_NORMALIZE_3_D = 0x733A8

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_PIXEL_NORMALIZE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("normalization_factor" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"         , ctypes.c_uint32, 15), # 16 to 30 
        ("enable"              , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PLANE_PIXEL_NORMALIZE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_PIXEL_NORMALIZE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
