import ctypes
 
'''
Register instance and offset 
'''
PLANE_AUX_OFFSET_1_A = 0x701C4 
PLANE_AUX_OFFSET_1_B = 0x711C4 
PLANE_AUX_OFFSET_1_C = 0x721C4 
PLANE_AUX_OFFSET_2_A = 0x702C4 
PLANE_AUX_OFFSET_2_B = 0x712C4 
PLANE_AUX_OFFSET_2_C = 0x722C4 
PLANE_AUX_OFFSET_3_A = 0x703C4 
PLANE_AUX_OFFSET_3_B = 0x713C4 
PLANE_AUX_OFFSET_3_C = 0x723C4 
PLANE_AUX_OFFSET_4_A = 0x704C4 
PLANE_AUX_OFFSET_4_B = 0x714C4 
PLANE_AUX_OFFSET_4_C = 0x724C4 
PLANE_OFFSET_1_A = 0x701A4 
PLANE_OFFSET_1_B = 0x711A4 
PLANE_OFFSET_1_C = 0x721A4 
PLANE_OFFSET_2_A = 0x702A4 
PLANE_OFFSET_2_B = 0x712A4 
PLANE_OFFSET_2_C = 0x722A4 
PLANE_OFFSET_3_A = 0x703A4 
PLANE_OFFSET_3_B = 0x713A4 
PLANE_OFFSET_3_C = 0x723A4 
PLANE_OFFSET_4_A = 0x704A4 
PLANE_OFFSET_4_B = 0x714A4 
PLANE_OFFSET_4_C = 0x724A4 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_OFFSET_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("start_x_position" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"     , ctypes.c_uint32, 3), # 13 to 15 
        ("start_y_position" , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"     , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PLANE_OFFSET_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_OFFSET_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
