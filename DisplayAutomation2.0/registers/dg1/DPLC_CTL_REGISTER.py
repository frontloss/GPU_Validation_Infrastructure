##
# BSpec link : https://gfxspecs.intel.com/Predator/Home/Index/50020
import ctypes

'''
Register instance and offset
'''
DPLC_CTL_A = 0x49400
DPLC_CTL_B = 0x49480

'''
Register field expected values
'''
allow_double_buffer_update_disable_ALLOWED = 0b1
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0
arbitration_option_1 = 0b0
arbitration_option_2 = 0b1
enhancement_mode_DIRECT = 0b00
enhancement_mode_MULTIPLICATIVE = 0b01
enhancement_mode_RESERVED = 0b0
fast_access_mode_enable_DISABLE = 0b0
fast_access_mode_enable_ENABLE = 0b1
frame_histogram_done_DONE = 0b1
frame_histogram_done_NOT_DONE = 0b0
function_enable_DISABLE = 0b0
function_enable_ENABLE = 0b1
histogram_buffer_id_BANK0 = 0b0
histogram_buffer_id_BANK1 = 0b1
histogram_ram_readback_return_DISABLE = 0b0
histogram_ram_readback_return_ENABLE = 0b1
ie_buffer_id_BANK0 = 0b0
ie_buffer_id_BANK1 = 0b1
ie_enable_DISABLE = 0b0
ie_enable_ENABLE = 0b1
load_ie_LOADING = 0b1
load_ie_READY_DONE = 0b0
mask_dmc_trigger_DISABLE = 0b0
mask_dmc_trigger_ENABLE = 0b1
orientation_LANDSCAPE = 0b0
orientation_PORTRAIT = 0b1
tile_size_128X128 = 0b1
tile_size_256X256 = 0b0

'''
Register bitfield definition structure
'''


class DPLC_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("tile_size", ctypes.c_uint32, 1),  # 0 to 0
        ("hist_buffer_delay", ctypes.c_uint32, 1),  # 1 to 1
        ("spare_2", ctypes.c_uint32, 1),  # 2 to 2
        ("spare_3", ctypes.c_uint32, 1),  # 3 to 3
        ("spare_4", ctypes.c_uint32, 1),  # 4 to 4
        ("spare_5", ctypes.c_uint32, 1),  # 5 to 5
        ("spare_6", ctypes.c_uint32, 1),  # 6 to 6
        ("spare_7", ctypes.c_uint32, 1),  # 7 to 7
        ("spare_8", ctypes.c_uint32, 1),  # 8 to 8
        ("spare_9", ctypes.c_uint32, 1),  # 9 to 9
        ("spare_10", ctypes.c_uint32, 1),  # 10 to 10
        ("spare_11", ctypes.c_uint32, 1),  # 11 to 11
        ("enhancement_mode", ctypes.c_uint32, 2),  # 12 to 13
        ("reserved_14", ctypes.c_uint32, 6),  # 14 to 19
        ("reserved_20", ctypes.c_uint32, 3),  # 20 to 22
        ("reserved_23", ctypes.c_uint32, 1),  # 23 to 23
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1),  # 24 to 24
        ("ie_buffer_id", ctypes.c_uint32, 1),  # 25 to 25
        ("histogram_buffer_id", ctypes.c_uint32, 1),  # 26 to 26
        ("frame_histogram_done", ctypes.c_uint32, 1),  # 27 to 27
        ("orientation", ctypes.c_uint32, 1),  # 28 to 28
        ("load_ie", ctypes.c_uint32, 1),  # 29 to 29
        ("ie_enable", ctypes.c_uint32, 1),  # 30 to 30
        ("function_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class DPLC_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLC_CTL_REG),
        ("asUint", ctypes.c_uint32)]
