import ctypes
 
'''
Register instance and offset 
'''
DSC_PICTURE_PARAMETER_SET_1_DSC0_PA = 0x78074
DSC_PICTURE_PARAMETER_SET_1_DSC0_PB = 0x78274
DSC_PICTURE_PARAMETER_SET_1_DSC0_PC = 0x78474
DSC_PICTURE_PARAMETER_SET_1_DSC0_PD = 0x78674
DSC_PICTURE_PARAMETER_SET_1_DSC1_PA = 0x78174
DSC_PICTURE_PARAMETER_SET_1_DSC1_PB = 0x78374
DSC_PICTURE_PARAMETER_SET_1_DSC1_PC = 0x78574
DSC_PICTURE_PARAMETER_SET_1_DSC1_PD = 0x78774

'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DSC_PICTURE_PARAMETER_SET_1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("bits_per_pixel"             , ctypes.c_uint32, 10), # 0 to 9 
        ("psr2_su_slice_row_per_frame" , ctypes.c_uint32, 12), # 20 to 31 
    ]

 
class DSC_PICTURE_PARAMETER_SET_1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSC_PICTURE_PARAMETER_SET_1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
