import ctypes
 
'''
Register instance and offset 
'''
PLANE_SURFLIVE_1_A  = 0x701ac 
PLANE_SURFLIVE_1_B  = 0x711ac 
PLANE_SURFLIVE_1_C  = 0x721ac 
PLANE_SURFLIVE_1_D  = 0x731ac 

PLANE_SURFLIVE_2_A  = 0x702ac 
PLANE_SURFLIVE_2_B  = 0x712ac 
PLANE_SURFLIVE_2_C  = 0x722ac 
PLANE_SURFLIVE_2_D  = 0x732ac 

PLANE_SURFLIVE_3_A  = 0x703ac 
PLANE_SURFLIVE_3_B  = 0x713ac 
PLANE_SURFLIVE_3_C  = 0x723ac 
PLANE_SURFLIVE_3_D  = 0x733ac 

PLANE_SURFLIVE_4_A  = 0x704ac 
PLANE_SURFLIVE_4_B  = 0x714ac 
PLANE_SURFLIVE_4_C  = 0x724ac 
PLANE_SURFLIVE_4_D  = 0x734ac 

PLANE_SURFLIVE_5_A  = 0x705ac 
PLANE_SURFLIVE_5_B  = 0x715ac 
PLANE_SURFLIVE_5_C  = 0x725ac 
PLANE_SURFLIVE_5_D  = 0x735ac


'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_SURFLIVE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_1"                  , ctypes.c_uint32, 9), # 0 to 8
        ("current_frame_counter_entry" , ctypes.c_uint32, 2), # 9 to 10
        ("reserved_11"                 , ctypes.c_uint32, 1), # 11 to 11
        ("live_surface_base_address"   , ctypes.c_uint32, 20), # 12 to 31

    ]

 
class PLANE_SURFLIVE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_SURFLIVE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
