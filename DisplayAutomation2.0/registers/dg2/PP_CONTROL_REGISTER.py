import ctypes
 
'''
Register instance and offset 
'''
PP_CONTROL = 0xC7204 
PP_CONTROL_2 = 0xC7304 

 
'''
Register field expected values 
'''
backlight_enable_DISABLE = 0b0 
backlight_enable_ENABLE = 0b1 
power_cycle_delay_400_MS = 0b00101 
power_cycle_delay_NO_DELAY = 0b00000 
power_down_on_reset_DO_NOT_RUN_POWER_DOWN_ON_RESET = 0b0 
power_down_on_reset_RUN_POWER_DOWN_ON_RESET = 0b1 
power_state_target_OFF = 0b0 
power_state_target_ON = 0b1 
vdd_override_FORCE = 0b1 
vdd_override_NOT_FORCE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class PP_CONTROL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("power_state_target" , ctypes.c_uint32, 1), # 0 to 0 
        ("power_down_on_reset" , ctypes.c_uint32, 1), # 1 to 1 
        ("backlight_enable"   , ctypes.c_uint32, 1), # 2 to 2 
        ("vdd_override"       , ctypes.c_uint32, 1), # 3 to 3 
        ("power_cycle_delay"  , ctypes.c_uint32, 5), # 4 to 8 
        ("reserved_9"         , ctypes.c_uint32, 7), # 9 to 15 
        ("spare_31_16"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class PP_CONTROL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PP_CONTROL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
