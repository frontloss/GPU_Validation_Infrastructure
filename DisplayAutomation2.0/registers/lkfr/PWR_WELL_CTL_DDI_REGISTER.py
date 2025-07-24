import ctypes
 
##
# Register instance and offset
PWR_WELL_CTL_DDI1 = 0x45450
PWR_WELL_CTL_DDI2 = 0x45454 
PWR_WELL_CTL_DDI4 = 0x4545C 

 
##
# Register bitfield definition structure
class PWR_WELL_CTL_DDI_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ddi_a_io_power_state",    ctypes.c_uint32, 1),            # 0 to 0
        ("ddi_a_io_power_request",  ctypes.c_uint32, 1),            # 1 to 1
        ("ddi_b_io_power_state",    ctypes.c_uint32, 1),            # 2 to 2
        ("ddi_b_io_power_request",  ctypes.c_uint32, 1),            # 3 to 3
        ("ddi_c_io_power_state",    ctypes.c_uint32, 1),            # 4 to 4
        ("ddi_c_io_power_request",  ctypes.c_uint32, 1),            # 5 to 5
        ("ddi_usb_c_1_io_power_state",    ctypes.c_uint32, 1),      # 6 to 6
        ("ddi_usb_c_1_io_power_request",  ctypes.c_uint32, 1),      # 7 to 7
        ("ddi_usb_c_2_io_power_state",    ctypes.c_uint32, 1),      # 8 to 8
        ("ddi_usb_c_2_io_power_request",  ctypes.c_uint32, 1),      # 9 to 9
        ("ddi_usb_c_3_io_power_state",    ctypes.c_uint32, 1),      # 10 to 10
        ("ddi_usb_c_3_io_power_request",  ctypes.c_uint32, 1),      # 11 to 11
        ("ddi_usb_c_4_io_power_state",    ctypes.c_uint32, 1),      # 12 to 12
        ("ddi_usb_c_4_io_power_request",  ctypes.c_uint32, 1),      # 13 to 13
        ("ddi_usb_c_5_io_power_state",    ctypes.c_uint32, 1),      # 14 to 14
        ("ddi_usb_c_5_io_power_request",  ctypes.c_uint32, 1),      # 15 to 15
        ("ddi_usb_c_6_io_power_state",    ctypes.c_uint32, 1),      # 16 to 16
        ("ddi_usb_c_6_io_power_request",  ctypes.c_uint32, 1),      # 17 to 17
        ("reserved_1",             ctypes.c_uint32, 14),            # 18 to 31
    ]


class PWR_WELL_CTL_DDI_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_DDI_REG),
        ("asUint", ctypes.c_uint32)
    ]
