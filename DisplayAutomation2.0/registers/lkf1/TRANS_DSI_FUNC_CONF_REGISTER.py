import ctypes
 
'''
Register instance and offset 
'''
TRANS_DSI_FUNC_CONF_DSI0 = 0x6B030 
TRANS_DSI_FUNC_CONF_DSI1 = 0x6B830 

 
'''
Register field expected values 
'''
bgr_transmission_TRANSMIT_ORDER_IS_B_G_R = 1 
bgr_transmission_TRANSMIT_ORDER_IS_R_G_B = 0 
continuous_clock_ALWAYS_ENTER_LP_AFTER_DATA_LANES = 0b00 
continuous_clock_CONTINUOUS_HS_CLOCK = 0b11 
continuous_clock_OPPORTUNISTICALLY_KEEP_CLOCK_IN_HS_OR_LP = 0b10 
continuous_clock_RESERVED = 0b0 
eotp_disabled_EOTP_DISABLED = 1 
eotp_disabled_EOTP_ENABLED = 0 
link_calibration_CALIBRATION_DISABLED = 0b00 
link_calibration_CALIBRATION_ENABLED___INITIAL_AND_PERIODIC = 0b11 
link_calibration_CALIBRATION_ENABLED___INITIAL_ONLY = 0b10 
link_calibration_RESERVED = 0b0 
link_ready_LINK_IS_NOT_READY_TO_ACCEPT_TRAFFIC = 0 
link_ready_LINK_IS_READY_TO_ACCEPT_TRAFFIC = 1 
mode_of_operation_COMMAND_MODE_NO_GATE = 0b00 
mode_of_operation_COMMAND_MODE_TE_GATE = 0b01 
mode_of_operation_VIDEO_MODE_SYNC_EVENT = 0b10 
mode_of_operation_VIDEO_MODE_SYNC_PULSE = 0b11 
pixel_buffer_threshold_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_1_2_FULL = 0b01 
pixel_buffer_threshold_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_1_4_FULL = 0b00 
pixel_buffer_threshold_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_3_4_FULL = 0b10 
pixel_buffer_threshold_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_FULL = 0b11 
pixel_format_16_BIT_RGB__5_6_5 = 0b000 
pixel_format_18_BIT_RGB__6_6_6_LOOSE = 0b010 
pixel_format_18_BIT_RGB__6_6_6_PACKED = 0b001 
pixel_format_24_BIT_RGB__8_8_8 = 0b011 
pixel_format_30_BIT_RGB__10_10_10 = 0b100 
pixel_format_36_BIT_RGB__12_12_12 = 0b101 
pixel_format_COMPRESSED = 0b110 
pixel_format_RESERVED = 0b0 
te_deglitch_enable_DISABLED = 0b0 
te_deglitch_enable_ENABLED = 0b1 
te_source_IN_BAND_TE_EVENT_SOURCE = 0 
te_source_OUT_OF_BAND_TE_EVENT_SOURCE_I_E__GPIO = 1 
s3d_orientation_PORTRAIT_ORIENTATION = 0b0
s3d_orientation_LANDSCAPE_ORIENTATION = 0b1
blanking_packet_during_bllp_DISABLED = 0b0
blanking_packet_during_bllp_ENABLED = 0b1
lp_clock_during_lpm_DISABLED = 0b0
lp_clock_during_lpm_ENABLED = 0b1
te_accumulation_DISABLED = 0b0
te_accumulation_ENABLED = 0b1

 
'''
Register bitfield defnition structure 
'''
class TRANS_DSI_FUNC_CONF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("eotp_disabled"                , ctypes.c_uint32, 1), # 0 to 0
        ("s3d_orientation"              , ctypes.c_uint32, 1), # 1 to 1
        ("blanking_packet_during_bllp"  , ctypes.c_uint32, 1), # 2 to 2
        ("reserved_3"                   , ctypes.c_uint32, 1), # 3 to 3
        ("link_calibration"             , ctypes.c_uint32, 2), # 4 to 5
        ("reserved_6"                   , ctypes.c_uint32, 1), # 6 to 6
        ("lp_clock_during_lpm"          , ctypes.c_uint32, 1), # 7 to 7
        ("continuous_clock"             , ctypes.c_uint32, 2), # 8 to 9
        ("pixel_buffer_threshold"       , ctypes.c_uint32, 2), # 10 to 11
        ("pixel_virtual_channel"        , ctypes.c_uint32, 2), # 12 to 13
        ("reserved_14"                  , ctypes.c_uint32, 1), # 14 to 14
        ("bgr_transmission"             , ctypes.c_uint32, 1), # 15 to 15
        ("pixel_format"                 , ctypes.c_uint32, 3), # 16 to 18
        ("reserved_19"                  , ctypes.c_uint32, 1), # 19 to 19
        ("link_ready"                   , ctypes.c_uint32, 1), # 20 to 20
        ("reserved_21"                  , ctypes.c_uint32, 4), # 21 to 24
        ("te_accumulation"              , ctypes.c_uint32, 1), # 25 to 25
        ("te_deglitch_enable"           , ctypes.c_uint32, 1), # 26 to 26
        ("te_source"                    , ctypes.c_uint32, 1), # 27 to 27
        ("mode_of_operation"            , ctypes.c_uint32, 2), # 28 to 29
        ("reserved_30"                  , ctypes.c_uint32, 2), # 30 to 31
    ]

 
class TRANS_DSI_FUNC_CONF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_DSI_FUNC_CONF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
