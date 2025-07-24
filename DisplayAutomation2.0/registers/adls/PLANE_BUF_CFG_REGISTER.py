import ctypes
 
'''
Register instance and offset 
'''
CUR_BUF_CFG_A = 0x7017C 
CUR_BUF_CFG_B = 0x7117C 
CUR_BUF_CFG_C = 0x7217C
CUR_BUF_CFG_D = 0x7317C
PLANE_BUF_CFG_1_A = 0x7027C
PLANE_BUF_CFG_1_B = 0x7127C
PLANE_BUF_CFG_1_C = 0x7227C
PLANE_BUF_CFG_1_D = 0x7327C
PLANE_BUF_CFG_2_A = 0x7037C
PLANE_BUF_CFG_2_B = 0x7137C
PLANE_BUF_CFG_2_C = 0x7237C
PLANE_BUF_CFG_2_D = 0x7337C
PLANE_BUF_CFG_3_A = 0x7047C
PLANE_BUF_CFG_3_B = 0x7147C
PLANE_BUF_CFG_3_C = 0x7247C
PLANE_BUF_CFG_3_D = 0x7347C
PLANE_BUF_CFG_4_A = 0x7057C
PLANE_BUF_CFG_4_B = 0x7157C
PLANE_BUF_CFG_4_C = 0x7257C
PLANE_BUF_CFG_4_D = 0x7357C
PLANE_BUF_CFG_5_A = 0x7067C
PLANE_BUF_CFG_5_B = 0x7167C
PLANE_BUF_CFG_5_C = 0x7267C
PLANE_BUF_CFG_5_D = 0x7367C

 
'''
Register field expected values 
'''
buffer_end_DEFAULT = 0x000 
buffer_start_DEFAULT = 0x000 

 
'''
Register bitfield defnition structure 
'''
class PLANE_BUF_CFG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("buffer_start" , ctypes.c_uint32, 11), # 0 to 10 
        ("reserved_11" , ctypes.c_uint32, 5), # 11 to 15 
        ("buffer_end"  , ctypes.c_uint32, 11), # 16 to 26 
        ("reserved_27" , ctypes.c_uint32, 5), # 27 to 31 
    ]

 
class PLANE_BUF_CFG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_BUF_CFG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
