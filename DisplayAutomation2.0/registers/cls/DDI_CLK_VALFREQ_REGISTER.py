import ctypes

'''
Register instance and offset 
'''
DDI_CLK_VALFREQ_A = 0X64030
DDI_CLK_VALFREQ_B = 0X64130
DDI_CLK_VALFREQ_C = 0X64230

'''
Register field expected values 
'''

'''
Register bitfield defnition structure
'''

class DDI_CLK_VALFREQ_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ddi_validation_frequency', ctypes.c_uint32, 32),
    ]

class DDI_CLK_VALFREQ_REGISTER(ctypes.Union):
    value = 0
    offset = 0

    TimestampCounter = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', DDI_CLK_VALFREQ_REG),
        ('value', ctypes.c_uint32)
    ]