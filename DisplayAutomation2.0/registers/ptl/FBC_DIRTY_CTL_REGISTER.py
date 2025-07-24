import ctypes
# Bspec link : https://gfxspecs.intel.com/Predator/Home/Index/50216

'''
Register instance and offset 
'''
FBC_DIRTY_CTL_A = 0x43234
FBC_DIRTY_CTL_B = 0x43274
FBC_DIRTY_CTL_C = 0x432F4
FBC_DIRTY_CTL_D = 0x432C8
FBC_DIRTY_CTL_E = 0x43334
FBC_DIRTY_CTL_F = 0x43374


class FBC_DIRTY_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_uint32, 31),   # 0 to 30
        ("dirty_rectangle_enable", ctypes.c_uint32, 1)   # 31
    ]

 
class FBC_DIRTY_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_DIRTY_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 