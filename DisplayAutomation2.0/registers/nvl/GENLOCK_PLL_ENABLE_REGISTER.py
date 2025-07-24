import ctypes

'''
Register instance and offset 
'''
GENLOCK_PLL_ENABLE = 0X46020

'''
Register field expected values 
'''
genlock_pll_enable_DISABLE = 0b0
genlock_pll_enable_ENABLE = 0b1
genlock_pll_lock_LOCKED = 0b1
genlock_pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0

'''
Register bitfield defnition structure
'''

class GENLOCK_PLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('reserved', ctypes.c_int32, 30), # 0 to 30
        ('genlock_pll_lock', ctypes.c_uint32, 1), # 30 to 30
        ('genlock_pll_enable', ctypes.c_uint32, 1), # 31 to 31
    ]

class GENLOCK_PLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ('u', GENLOCK_PLL_ENABLE_REG),
        ('value', ctypes.c_uint32)
    ]
