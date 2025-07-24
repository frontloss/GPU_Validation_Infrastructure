import ctypes

'''
Register instance and offset 
'''
SBLC_PWM_FREQ = 0xC8254
SBLC_PWM_FREQ_2 = 0xC8354


class SBlcPwmFreqReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("frequency", ctypes.c_uint32, 31)  # 0 to 31
    ]


class SBLC_PWM_FREQ_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SBlcPwmFreqReg),
        ("asUint", ctypes.c_uint32)]
