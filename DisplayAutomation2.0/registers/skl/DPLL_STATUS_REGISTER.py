import ctypes
 
'''
Register instance and offset 
'''
DPLL_STATUS = 0x6C060 

 
'''
Register field expected values 
'''
dpll0_lock_LOCKED = 0b1 
dpll0_lock_NOT_LOCKED = 0b0 
dpll0_sem_done_DONE = 0b1 
dpll0_sem_done_NOT_DONE = 0b0 
dpll1_lock_LOCKED = 0b1 
dpll1_lock_NOT_LOCKED = 0b0 
dpll1_sem_done_DONE = 0b1 
dpll1_sem_done_NOT_DONE = 0b0 
dpll2_lock_LOCKED = 0b1 
dpll2_lock_NOT_LOCKED = 0b0 
dpll2_sem_done_DONE = 0b1 
dpll2_sem_done_NOT_DONE = 0b0 
dpll3_lock_LOCKED = 0b1 
dpll3_lock_NOT_LOCKED = 0b0 
dpll3_sem_done_DONE = 0b1 
dpll3_sem_done_NOT_DONE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DPLL_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dpll0_lock"    , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"    , ctypes.c_uint32, 3), # 1 to 3 
        ("dpll0_sem_done" , ctypes.c_uint32, 1), # 4 to 4 
        ("reserved_5"    , ctypes.c_uint32, 3), # 5 to 7 
        ("dpll1_lock"    , ctypes.c_uint32, 1), # 8 to 8 
        ("reserved_9"    , ctypes.c_uint32, 3), # 9 to 11 
        ("dpll1_sem_done" , ctypes.c_uint32, 1), # 12 to 12 
        ("reserved_13"   , ctypes.c_uint32, 3), # 13 to 15 
        ("dpll2_lock"    , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"   , ctypes.c_uint32, 3), # 17 to 19 
        ("dpll2_sem_done" , ctypes.c_uint32, 1), # 20 to 20 
        ("reserved_21"   , ctypes.c_uint32, 3), # 21 to 23 
        ("dpll3_lock"    , ctypes.c_uint32, 1), # 24 to 24 
        ("reserved_25"   , ctypes.c_uint32, 3), # 25 to 27 
        ("dpll3_sem_done" , ctypes.c_uint32, 1), # 28 to 28 
        ("reserved_29"   , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class DPLL_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
