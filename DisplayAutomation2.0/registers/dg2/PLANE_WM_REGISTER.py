import ctypes
 
'''
Register instance and offset 
'''
CUR_WM_A = 0x70140 
CUR_WM_B = 0x71140 
CUR_WM_C = 0x72140
CUR_WM_D = 0x73140
CUR_WM_TRANS_A = 0x70168 
CUR_WM_TRANS_B = 0x71168 
CUR_WM_TRANS_C = 0x72168
CUR_WM_TRANS_D = 0x73168
PLANE_WM_1_A = 0x70240 
PLANE_WM_1_B = 0x71240 
PLANE_WM_1_C = 0x72240
PLANE_WM_1_D = 0x73240
PLANE_WM_2_A = 0x70340 
PLANE_WM_2_B = 0x71340 
PLANE_WM_2_C = 0x72340
PLANE_WM_2_D = 0x73340
PLANE_WM_3_A = 0x70440 
PLANE_WM_3_B = 0x71440 
PLANE_WM_3_C = 0x72440
PLANE_WM_3_D = 0x73440
PLANE_WM_4_A = 0x70540 
PLANE_WM_4_B = 0x71540 
PLANE_WM_4_C = 0x72540
PLANE_WM_4_D = 0x73540
PLANE_WM_5_A = 0x70640
PLANE_WM_5_B = 0x71640
PLANE_WM_5_C = 0x72640
PLANE_WM_5_D = 0x73640
PLANE_WM_0_1_A = 0x70240
PLANE_WM_1_1_A = 0x70244
PLANE_WM_2_1_A = 0x70248
PLANE_WM_3_1_A = 0x7024C
PLANE_WM_4_1_A = 0x70250
PLANE_WM_5_1_A = 0x70254
PLANE_WM_6_1_A = 0x70258
PLANE_WM_7_1_A = 0x7025C
PLANE_WM_0_1_B = 0x71240
PLANE_WM_1_1_B = 0x71244
PLANE_WM_2_1_B = 0x71248
PLANE_WM_3_1_B = 0x7124C
PLANE_WM_4_1_B = 0x71250
PLANE_WM_5_1_B = 0x71254
PLANE_WM_6_1_B = 0x71258
PLANE_WM_7_1_B = 0x7125C
PLANE_TRANS_WM_1_A = 0x70268
PLANE_TRANS_WM_1_B = 0x71268
PLANE_TRANS_WM_1_C = 0x72268
PLANE_TRANS_WM_1_D = 0x73268
PLANE_TRANS_WM_2_A = 0x70368
PLANE_TRANS_WM_2_B = 0x71368
PLANE_TRANS_WM_2_C = 0x72368
PLANE_TRANS_WM_2_D = 0x73368
PLANE_TRANS_WM_3_A = 0x70468
PLANE_TRANS_WM_3_B = 0x71468
PLANE_TRANS_WM_3_C = 0x72468
PLANE_TRANS_WM_3_D = 0x73468
PLANE_TRANS_WM_4_A = 0x70568
PLANE_TRANS_WM_4_B = 0x71568
PLANE_TRANS_WM_4_C = 0x72568
PLANE_TRANS_WM_4_D = 0x73568
PLANE_TRANS_WM_5_A = 0x70668
PLANE_TRANS_WM_5_B = 0x71668
PLANE_TRANS_WM_5_C = 0x72668
PLANE_TRANS_WM_5_D = 0x73668

'''
Register field expected values 
'''
blocks_DEFAULT = 0x007 
enable_DISABLE = 0b0 
enable_ENABLE = 0b1 
ignore_lines_IGNORE_LINES = 0b1 
ignore_lines_USE_LINES = 0b0 
lines_DEFAULT = 0x01 

'''
Register bitfield defnition structure 
'''
class PLANE_WM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("blocks"      , ctypes.c_uint32, 12), # 0 to 11
        ("reserved_11" , ctypes.c_uint32, 2), # 12 to 13
        ("lines"       , ctypes.c_uint32, 13), # 14 to 26
        ("reserved_19" , ctypes.c_uint32, 3), # 27 to 29
        ("ignore_lines" , ctypes.c_uint32, 1), # 30 to 30 
        ("enable"      , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PLANE_WM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_WM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
