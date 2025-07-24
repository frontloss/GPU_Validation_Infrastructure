import ctypes
 
'''
Register instance and offset 
'''
PORTA_PLL_ENABLE = 0x46010
PORTB_PLL_ENABLE = 0x46014
PORTC_PLL_ENABLE = 0x46018
PORTD_PLL_ENABLE = 0x4601C
PORTTC1_PLL_ENABLE = 0x46030
DPLL0_ENABLE = 0x46010
DPLL1_ENABLE = 0x46014
DPLL4_ENABLE = 0x46018

 
'''
Register field expected values 
'''
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 
power_enable_DISABLE = 0b0
power_enable_ENABLE = 0b1 
power_state_DISABLED = 0b0 
power_state_ENABLED = 0b1 

'''
Register bitfield defnition structure 
'''


class DPLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 26),  # 0 to 25
        ("power_state", ctypes.c_uint32, 1),  # 26 to 26
        ("power_enable", ctypes.c_uint32, 1),  # 27 to 27
        ("reserved_28", ctypes.c_uint32, 2),  # 28 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DPLL_ENABLE_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]
 
