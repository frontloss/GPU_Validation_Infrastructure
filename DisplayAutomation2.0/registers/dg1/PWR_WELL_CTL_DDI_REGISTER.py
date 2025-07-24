import ctypes
 
'''
Register instance and offset 
'''
PWR_WELL_CTL_DDI1 = 0x45450 
PWR_WELL_CTL_DDI2 = 0x45454 
PWR_WELL_CTL_DDI4 = 0x4545C 

 
'''
Register field expected values 
'''
ddi_a_io_power_request_DISABLE = 0b0
ddi_a_io_power_request_ENABLE = 0b1
ddi_a_io_power_state_DISABLED = 0b0 
ddi_a_io_power_state_ENABLED = 0b1

ddi_b_io_power_request_DISABLE = 0b0
ddi_b_io_power_request_ENABLE = 0b1
ddi_b_io_power_state_DISABLED = 0b0 
ddi_b_io_power_state_ENABLED = 0b1

ddi_c_io_power_request_DISABLE = 0b0
ddi_c_io_power_request_ENABLE = 0b1
ddi_c_io_power_state_DISABLED = 0b0
ddi_c_io_power_state_ENABLED = 0b1

ddi_d_io_power_request_DISABLE = 0b0
ddi_d_io_power_request_ENABLE = 0b1 
ddi_d_io_power_state_DISABLED = 0b0
ddi_d_io_power_state_ENABLED = 0b1


'''
Register bitfield defnition structure 
'''
class PWR_WELL_CTL_DDI_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ddi_a_io_power_state",    ctypes.c_uint32, 1), # 0 to 0 
        ("ddi_a_io_power_request",  ctypes.c_uint32, 1), # 1 to 1 
        ("ddi_b_io_power_state",    ctypes.c_uint32, 1), # 2 to 2 
        ("ddi_b_io_power_request",  ctypes.c_uint32, 1), # 3 to 3
        ("reserved_4", ctypes.c_uint32, 1),              # 4 to 4
        ("reserved_5", ctypes.c_uint32, 1),              # 5 to 5
        ("ddi_usb_c_1_io_power_state",    ctypes.c_uint32, 1), # 6 to 6
        ("ddi_usb_c_1_io_power_request",  ctypes.c_uint32, 1), # 7 to 7
        ("ddi_usb_c_2_io_power_state",    ctypes.c_uint32, 1), # 8 to 8
        ("ddi_usb_c_2_io_power_request",  ctypes.c_uint32, 1), # 9 to 9
        ("reserved_10",             ctypes.c_uint32, 22), # 10 to 31
    ]

 
class PWR_WELL_CTL_DDI_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_DDI_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
