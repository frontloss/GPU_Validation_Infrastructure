import ctypes

##
# Register instance and offset
PIPE_MISC_A = 0x70030
PIPE_MISC_B = 0x71030
PIPE_MISC_C = 0x72030
PIPE_MISC_D = 0x73030

##
# Register field expected values
bits_per_color_10_BPC = 0b001
bits_per_color_12_BPC = 0b011
bits_per_color_6_BPC = 0b010
bits_per_color_8_BPC = 0b000
yuv420_enable_ENABLE = 0b1
yuv420_enable_DISABLE = 0b0
yuv420_mode_BYPASS = 0b0
yuv420_mode_FULL_BLEND = 0b1
hdr_mode_DISABLE = 0b0
hdr_mode_ENABLE = 0b1
pipe_output_color_space_select_RGB = 0b0
pipe_output_color_space_select_YUV = 0b1
dithering_type_SPATIAL = 0b00
dithering_type_ST1 = 0b01
dithering_type_ST2 = 0b10
dithering_type_TEMPORAL = 0b11


##
# Register bitfield definition structure
class PIPE_MISC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("bfi_enable", ctypes.c_uint32, 1),                             # Bit 0
        ("reserved_1", ctypes.c_uint32, 1),                             # Bit 1
        ("dithering_type", ctypes.c_uint32, 2),                         # Bit 2:3
        ("dithering_enable", ctypes.c_uint32, 1),                       # Bit 4
        ("dithering_bpc", ctypes.c_uint32, 3),                          # Bit 5:7
        ("pixel_rounding", ctypes.c_uint32, 1),                         # Bit 8
        ("pixel_extension", ctypes.c_uint32, 1),                        # Bit 9
        ("xvycc_color_range_limit", ctypes.c_uint32, 1),                # Bit 10
        ("pipe_output_color_space_select", ctypes.c_uint32, 1),         # Bit 11
        ("oled_compensation", ctypes.c_uint32, 1),                      # Bit 12
        ("reserved_13", ctypes.c_uint32, 1),                            # Bit 13
        ("rotation_info", ctypes.c_uint32, 2),                          # Bit 14:15
        ("override_blue_channel", ctypes.c_uint32, 1),                  # Bit 16 - debug
        ("override_green_channel", ctypes.c_uint32, 1),                 # Bit 17 - debug
        ("override_red_channel", ctypes.c_uint32, 1),                   # Bit 18 - debug
        ("override_pipe_output", ctypes.c_uint32, 1),                   # Bit 19 - debug
        ("change_mask_for_vblank_vsync_int", ctypes.c_uint32, 1),       # Bit 20
        ("change_mask_for_register_write", ctypes.c_uint32, 1),         # Bit 21
        ("change_mask_for_ldpst", ctypes.c_uint32, 1),                  # Bit 22
        ("hdr_mode", ctypes.c_uint32, 1),                               # Bit 23
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1),     # Bit 24
        ("pipe_gamma_input_clamp_disable", ctypes.c_uint32, 1),         # Bit 25
        ("yuv420_mode", ctypes.c_uint32, 1),                            # Bit 26
        ("yuv420_enable", ctypes.c_uint32, 1),                          # Bit 27
        ("stereo_mask_pipe_render", ctypes.c_uint32, 2),                # Bit 28:29
        ("stereo_mask_pipe_int", ctypes.c_uint32, 2),                   # Bit 30:31
    ]


class PIPE_MISC_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PIPE_MISC_REG),
        ("asUint", ctypes.c_uint32)
    ]
