import ctypes
 
'''
Register instance and offset 
'''
UTIL_PIN_CTL = 0x48400 

 
'''
Register field expected values 
'''
pipe_select_PIPE_A = 0b00 
pipe_select_PIPE_B = 0b01 
pipe_select_PIPE_C = 0b10 
pipe_select_RESERVED = 0b0 
util_pin_direction_INPUT = 0b1 
util_pin_direction_OUTPUT = 0b0 
util_pin_enable_DISABLE = 0b0 
util_pin_enable_ENABLE = 0b1 
util_pin_mode_DATA = 0b0000 
util_pin_mode_PWM = 0b0001 
util_pin_mode_RESERVED = 0b0 
util_pin_mode_RIGHT_LEFT_EYE_LEVEL = 0b1000 
util_pin_mode_VBLANK = 0b0100 
util_pin_mode_VSYNC = 0b0101 
util_pin_output_data_0 = 0b0 
util_pin_output_data_1 = 0b1 
util_pin_output_polarity_INVERTED = 0b1 
util_pin_output_polarity_NOT_INVERTED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class UTIL_PIN_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"              , ctypes.c_uint32, 16), # 0 to 15 
        ("util_pin_input_data"     , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"             , ctypes.c_uint32, 2), # 17 to 18 
        ("util_pin_direction"      , ctypes.c_uint32, 1), # 19 to 19 
        ("reserved_20"             , ctypes.c_uint32, 2), # 20 to 21 
        ("util_pin_output_polarity" , ctypes.c_uint32, 1), # 22 to 22 
        ("util_pin_output_data"    , ctypes.c_uint32, 1), # 23 to 23 
        ("util_pin_mode"           , ctypes.c_uint32, 4), # 24 to 27 
        ("reserved_28"             , ctypes.c_uint32, 1), # 28 to 28 
        ("pipe_select"             , ctypes.c_uint32, 2), # 29 to 30 
        ("util_pin_enable"         , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class UTIL_PIN_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      UTIL_PIN_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
