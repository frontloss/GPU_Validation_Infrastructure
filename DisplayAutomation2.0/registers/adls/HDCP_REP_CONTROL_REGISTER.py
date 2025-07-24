import ctypes

'''
Register instance and offset
'''
HDCP_REP_CONTROL = 0x66D00

'''
Register field expected values
'''
sha1_control_COMPLETE_THE_HASHING = 0b010
sha1_control_IDLE = 0b000
sha1_control_INPUT_16_BIT_TEXT_AND_16_BIT_M0_INTERNAL_VALUE = 0b101
sha1_control_INPUT_24_BIT_TEXT_AND_8_BIT_M0_INTERNAL_VALUE = 0b100
sha1_control_INPUT_32_BIT_M0_INTERNAL_VALUE = 0b111
sha1_control_INPUT_32_BIT_TEXT = 0b001
sha1_control_INPUT_8_BIT_TEXT_AND_24_BIT_M0_INTERNAL_VALUE = 0b110
sha1_m0_select_TRANSCODER_A = 0b000
sha1_m0_select_TRANSCODER_B = 0b010
sha1_m0_select_TRANSCODER_C = 0b011
sha1_m0_select_TRANSCODER_D = 0b100
sha1_status_BUSY = 0b0001
sha1_status_COMPLETE_WITH_V_AND_V_PRIME_MATCH = 0b1100
sha1_status_COMPLETE_WITH_V_AND_V_PRIME_MISMATCH = 0b0100
sha1_status_IDLE = 0b0000
sha1_status_READY_FOR_NEXT_DATA_INPUT = 0b0010
transcoder_a_repeater_present_NOT_REPEATER = 0b0
transcoder_a_repeater_present_REPEATER = 0b1
transcoder_b_repeater_present_NOT_REPEATER = 0b0
transcoder_b_repeater_present_REPEATER = 0b1
transcoder_c_repeater_present_NOT_REPEATER = 0b0
transcoder_c_repeater_present_REPEATER = 0b1
transcoder_d_repeater_present_NOT_REPEATER = 0b0
transcoder_d_repeater_present_REPEATER = 0b1


'''
Register bitfield definition structure
'''


class HDCP_REP_CONTROL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0"                   , ctypes.c_uint32, 1),  # 0 to 0
        ("sha1_control"                 , ctypes.c_uint32, 3),  # 1 to 3
        ("reserved_4"                   , ctypes.c_uint32, 12),  # 4 to 15
        ("sha1_status"                  , ctypes.c_uint32, 4),  # 16 to 19
        ("sha1_m0_select"               , ctypes.c_uint32, 3),  # 20 to 22
        ("reserved_23"                  , ctypes.c_uint32, 2),  # 23 to 24
        ("reserved_25"                  , ctypes.c_uint32, 3),  # 25 to 27
        ("transcoder_d_repeater_present" , ctypes.c_uint32, 1),  # 28 to 28
        ("transcoder_c_repeater_present" , ctypes.c_uint32, 1),  # 29 to 29
        ("transcoder_b_repeater_present" , ctypes.c_uint32, 1),  # 30 to 30
        ("transcoder_a_repeater_present" , ctypes.c_uint32, 1),  # 31 to 31
    ]


class HDCP_REP_CONTROL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      HDCP_REP_CONTROL_REG),
        ("asUint", ctypes.c_uint32)]

