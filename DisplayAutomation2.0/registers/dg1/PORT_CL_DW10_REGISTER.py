import ctypes
 
##
# Register instance and offset
PORT_CL_DW10_A = 0x162028 
PORT_CL_DW10_B = 0x6C028
PORT_CL_DW10_C = 0x160028
PORT_CL_DW10_D = 0x161028

 
##
# Register field expected values
pg_seq_delay_override_enable_DISABLE = 0b0 
pg_seq_delay_override_enable_ENABLE = 0b1 
static_power_down_ddi_POWER_UP_ALL_LANES = 0b0000 
static_power_down_ddi_POWER_DOWN_LANES_3_2 = 0b1100 
static_power_down_ddi_POWER_DOWN_LANES_3_2_1 = 0b1110 
static_power_down_ddi_POWER_DOWN_LANES_1_0 = 0b0011 
static_power_down_ddi_POWER_DOWN_LANES_2_1_0 = 0b0111 
static_power_down_ddi_POWER_DOWN_LANE_3 = 0b1000
static_power_down_ddi_POWER_DOWN_LANES_3_1 = 0b1010 
static_power_down_ddi_POWER_DOWN_LANES_3_1_0 = 0b1011 

 
##
# Register bitfield definition structure
class PORT_CL_DW10_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("o_rterm100en_h_ovrd_val", ctypes.c_uint32, 1),        # Bit 0
        ("o_rterm100en_h_ovrd_en", ctypes.c_uint32, 1),         # Bit 1
        ("o_edp4k2k_mode_ovrd_val", ctypes.c_uint32, 1),        # Bit 2
        ("o_edp4k2k_mode_ovrd_en", ctypes.c_uint32, 1),         # Bit 3
        ("static_power_down_ddi", ctypes.c_uint32, 4),          # Bit 4:7
        ("spare_8", ctypes.c_uint32, 1),                        # Bit 8
        ("spare_9", ctypes.c_uint32, 1),                        # Bit 9
        ("spare_10", ctypes.c_uint32, 1),                       # Bit 10
        ("spare_11", ctypes.c_uint32, 1),                       # Bit 11
        ("reserved_1", ctypes.c_uint32, 4),                     # Bit 12:15
        ("ospare_cri_ret", ctypes.c_uint32, 6),                 # Bit 16:21
        ("spare_22", ctypes.c_uint32, 1),                       # Bit 22
        ("ohvpg_ctrl_mipia", ctypes.c_uint32, 1),               # Bit 23
        ("pg_seq_delay_override_enable", ctypes.c_uint32, 1),   # Bit 24
        ("pg_seq_delay_override", ctypes.c_uint32, 2),          # Bit 25:26
        ("reserved_2", ctypes.c_uint32, 5),                     # Bit 27:31
    ]

 
class PORT_CL_DW10_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_CL_DW10_REG),
        ("asUint", ctypes.c_uint32)
    ]
