import ctypes
 
'''
Register instance and offset 
'''
SBLC_PWM_DUTY = 0xC8258 
SBLC_PWM_DUTY_2 = 0xC8358 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class SBLC_PWM_DUTY_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("duty_cycle" , ctypes.c_uint32, 32), # 0 to 31 
    ]

 
class SBLC_PWM_DUTY_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SBLC_PWM_DUTY_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
