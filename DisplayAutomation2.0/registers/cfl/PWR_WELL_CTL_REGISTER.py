import ctypes

##
# Register instance and offset
PWR_WELL_CTL1 = 0x45400
PWR_WELL_CTL2 = 0x45404
PWR_WELL_CTL4 = 0x4540C


##
# Register bitfield definition structure
class PWR_WELL_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("misc_io_power_state", ctypes.c_uint32, 1),                # 0 to 0
        ("misc_io_power_request", ctypes.c_uint32, 1),              # 1
        ("ddi_a_and_ddi_e_io_power_state", ctypes.c_uint32, 1),     # 2
        ("ddi_a_and_ddi_e_io_power_request", ctypes.c_uint32, 1),   # 3
        ("ddi_b_io_power_state", ctypes.c_uint32, 1),               # 4
        ("ddi_b_io_power_request", ctypes.c_uint32, 1),             # 5
        ("ddi_c_io_power_state", ctypes.c_uint32, 1),               # 6
        ("ddi_c_io_power_request", ctypes.c_uint32, 1),             # 7
        ("ddi_d_io_power_state", ctypes.c_uint32, 1),               # 8
        ("ddi_d_io_power_request", ctypes.c_uint32, 1),             # 9
        ("reserved_1", ctypes.c_uint32, 18),                        # 10 to 27
        ("power_well_1_state", ctypes.c_uint32, 1),                 # 28 to 28
        ("power_well_1_request", ctypes.c_uint32, 1),               # 29 to 29
        ("power_well_2_state", ctypes.c_uint32, 1),                 # 30 to 30
        ("power_well_2_request", ctypes.c_uint32, 1),               # 31 to 31
    ]

 
class PWR_WELL_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PWR_WELL_CTL_REG),
        ("asUint", ctypes.c_uint32)
    ]
