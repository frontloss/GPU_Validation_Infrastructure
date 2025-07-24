import ctypes
 
'''
Register instance and offset 
'''
SBLC_PWM_CTL1 = 0xC8250 
SBLC_PWM_CTL1_2 = 0xC8350 

 
'''
Register field expected values 
'''
backlight_polarity_ACTIVE_HIGH = 0b0 
backlight_polarity_ACTIVE_LOW = 0b1 
pwm_pch_enable_DISABLE = 0b0 
pwm_pch_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class SBLC_PWM_CTL1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"        , ctypes.c_uint32, 29), # 0 to 28 
        ("backlight_polarity" , ctypes.c_uint32, 1), # 29 to 29 
        ("reserved_30"       , ctypes.c_uint32, 1), # 30 to 30 
        ("pwm_pch_enable"    , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class SBLC_PWM_CTL1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SBLC_PWM_CTL1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
