import ctypes

'''
Register instance and offset 
'''
SBLC_PWM_DUTY = 0xC8258
SBLC_PWM_DUTY_2 = 0xC8358


class SBlcPwmDutyReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("duty_cycle", ctypes.c_uint32, 31)  # 0 to 31
    ]


class SBLC_PWM_DUTY_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SBlcPwmDutyReg),
        ("asUint", ctypes.c_uint32)]
