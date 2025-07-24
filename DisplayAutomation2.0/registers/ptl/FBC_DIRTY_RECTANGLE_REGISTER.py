import ctypes
# Bspec link : https://gfxspecs.intel.com/Predator/Home/Index/50216
 
'''
Register instance and offset 
'''
FBC_DIRTY_RECTANGLE_A = 0x43230
FBC_DIRTY_RECTANGLE_B = 0x43270
FBC_DIRTY_RECTANGLE_C = 0x432B0
FBC_DIRTY_RECTANGLE_D = 0x432F0
FBC_DIRTY_RECTANGLE_E = 0x43330
FBC_DIRTY_RECTANGLE_F = 0x43370



class FBC_DIRTY_RECTANGLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("start_line", ctypes.c_uint32, 16),   # 0 to 15
        ("end_line", ctypes.c_uint32, 16)   # 16 to 31
    ]

 
class FBC_DIRTY_RECTANGLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_DIRTY_RECTANGLE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 