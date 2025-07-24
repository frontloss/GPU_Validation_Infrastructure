import ctypes
 
'''
Register instance and offset 
'''
SWF_32 = 0x4F080


 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class SWF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("software_flags" , ctypes.c_uint32, 32), # 0 to 31 
    ]

 
class SWF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SWF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
