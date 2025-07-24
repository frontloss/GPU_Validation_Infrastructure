# # https://gfxspecs.intel.com/Predator/Home/Index/49437
import ctypes

'''
Register instance and offset
'''
DC_STATE_EN = 0x45504

'''
Register field expected values
'''
dc_state_enable_DISABLE = 0b00
dc_state_enable_ENABLE_UPTO_DC5 = 0b01
dc_state_enable_ENABLE_UPTO_DC6 = 0b10
dc_state_clock_off_ENABLE = 0b1
dc_state_clock_off_DISABLE = 0b0
dc9_allow_DO_NOT_ALLOW = 0b0
dc9_allow_ALLOW = 0b1

'''
Register bitfield definition structure
'''


class DC_STATE_EN_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dc_state_enable", ctypes.c_uint32, 2),  # 0 to 1
        ("reserved_2", ctypes.c_uint32, 1),  # 2 to 2
        ("dc9_allow", ctypes.c_uint32, 1),  # 3 to 3
        ("mask_poke", ctypes.c_uint32, 1),  # 4 to 4
        ("reserved_5", ctypes.c_uint32, 3),  # 5 to 7
        ("block_outbound_traffic", ctypes.c_uint32, 1),  # 8 to 8
        ("in_csr_flow", ctypes.c_uint32, 1),  # 9 to 9
        ("reserved_10", ctypes.c_uint32, 18),  # 10 to 27
        ("dsi_plls_turn_off_disallowed", ctypes.c_uint32, 1),  # 28 to 28
        ("display_clock_off_state_status", ctypes.c_uint32, 1),  # 29 to 29
        ("display_clock_off_enable", ctypes.c_uint32, 1),  # 30 to 30
        ("mode_set_in_progress", ctypes.c_uint32, 1),  # 31 to 31
    ]


class DC_STATE_EN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DC_STATE_EN_REG),
        ("asUint", ctypes.c_uint32)]