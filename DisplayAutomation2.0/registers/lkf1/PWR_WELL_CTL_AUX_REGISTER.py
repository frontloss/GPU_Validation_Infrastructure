import ctypes
 
##
# Register instance and offset
PWR_WELL_CTL_AUX1 = 0x45440
PWR_WELL_CTL_AUX2 = 0x45444
PWR_WELL_CTL_AUX4 = 0x4544C


##
# Register bitfield definition structure
class PWR_WELL_CTL_AUX_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("aux_a_io_power_state",    ctypes.c_uint32, 1),            # 0 to 0
        ("aux_a_io_power_request",  ctypes.c_uint32, 1),            # 1 to 1
        ("aux_b_io_power_state",    ctypes.c_uint32, 1),            # 2 to 2
        ("aux_b_io_power_request",  ctypes.c_uint32, 1),            # 3 to 3
        ("aux_c_io_power_state",    ctypes.c_uint32, 1),            # 4 to 4
        ("aux_c_io_power_request",  ctypes.c_uint32, 1),            # 5 to 5
        ("aux_usb_c_1_io_power_state",    ctypes.c_uint32, 1),      # 6 to 6
        ("aux_usb_c_1_io_power_request",  ctypes.c_uint32, 1),      # 7 to 7
        ("aux_usb_c_2_io_power_state",    ctypes.c_uint32, 1),      # 8 to 8
        ("aux_usb_c_2_io_power_request",  ctypes.c_uint32, 1),      # 9 to 9
        ("aux_usb_c_3_io_power_state",    ctypes.c_uint32, 1),      # 10 to 10
        ("aux_usb_c_3_io_power_request",  ctypes.c_uint32, 1),      # 11 to 11
        ("aux_usb_c_4_io_power_state",    ctypes.c_uint32, 1),      # 12 to 12
        ("aux_usb_c_4_io_power_request",  ctypes.c_uint32, 1),      # 13 to 13
        ("aux_usb_c_5_io_power_state",    ctypes.c_uint32, 1),      # 14 to 14
        ("aux_usb_c_5_io_power_request",  ctypes.c_uint32, 1),      # 15 to 15
        ("aux_usb_c_6_io_power_state",    ctypes.c_uint32, 1),      # 16 to 16
        ("aux_usb_c_6_io_power_request",  ctypes.c_uint32, 1),      # 17 to 17
        ("aux_tbt_1_io_power_state",    ctypes.c_uint32, 1),        # 18
        ("aux_tbt_1_io_power_request",  ctypes.c_uint32, 1),        # 19
        ("aux_tbt_2_io_power_state",    ctypes.c_uint32, 1),        # 20
        ("aux_tbt_2_io_power_request",  ctypes.c_uint32, 1),        # 21
        ("aux_tbt_3_io_power_state",    ctypes.c_uint32, 1),        # 22
        ("aux_tbt_3_io_power_request",  ctypes.c_uint32, 1),        # 23
        ("aux_tbt_4_io_power_state",    ctypes.c_uint32, 1),        # 24
        ("aux_tbt_4_io_power_request",  ctypes.c_uint32, 1),        # 25
        ("aux_tbt_5_io_power_state",    ctypes.c_uint32, 1),        # 26
        ("aux_tbt_5_io_power_request",  ctypes.c_uint32, 1),        # 27
        ("aux_tbt_6_io_power_state",    ctypes.c_uint32, 1),        # 28
        ("aux_tbt_6_io_power_request",  ctypes.c_uint32, 1),        # 29
        ("reserved_1",             ctypes.c_uint32, 2),             # 30 to 31
    ]

 
class PWR_WELL_CTL_AUX_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_AUX_REG),
        ("asUint", ctypes.c_uint32)
    ]
