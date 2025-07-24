import ctypes

'''
Register instance and offset 
'''
PLANE_STRIDE_1_A = 0x70188  
PLANE_STRIDE_1_B = 0x71188  
PLANE_STRIDE_1_C = 0x72188  
PLANE_STRIDE_1_D = 0x73188  
PLANE_STRIDE_2_A = 0x70288  
PLANE_STRIDE_2_B = 0x71288  
PLANE_STRIDE_2_C = 0x72288  
PLANE_STRIDE_2_D = 0x73288  
PLANE_STRIDE_3_A = 0x70388  
PLANE_STRIDE_3_B = 0x71388  
PLANE_STRIDE_3_C = 0x72388  
PLANE_STRIDE_3_D = 0x73388  
PLANE_STRIDE_4_A = 0x70488  
PLANE_STRIDE_4_B = 0x71488  
PLANE_STRIDE_4_C = 0x72488  
PLANE_STRIDE_4_D = 0x73488  
PLANE_STRIDE_5_A = 0x70588  
PLANE_STRIDE_5_B = 0x71588  
PLANE_STRIDE_5_C = 0x72588  
PLANE_STRIDE_5_D = 0x73588  
PLANE_STRIDE_6_A = 0x70688  
PLANE_STRIDE_6_B = 0x71688  
PLANE_STRIDE_6_C = 0x72688  
PLANE_STRIDE_6_D = 0x73688  
PLANE_STRIDE_7_A = 0x70788  
PLANE_STRIDE_7_B = 0x71788  
PLANE_STRIDE_7_C = 0x72788  
PLANE_STRIDE_7_D = 0x73788  

'''
Register bitfield defnition structure 
'''
class PLANE_STRIDE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("stride", ctypes.c_uint32, 12), # 0 to 11
        ("reserved", ctypes.c_uint32, 6), # 12 to 17
        ("async_flipped_line", ctypes.c_uint32, 14), # 18 to 31 
    ]

 
class PLANE_STRIDE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_STRIDE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
