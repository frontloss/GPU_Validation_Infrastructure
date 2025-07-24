import ctypes
 
'''
Register instance and offset 
'''
TRANS_DDI_FUNC_CTL_A = 0x60400 
TRANS_DDI_FUNC_CTL_B = 0x61400 
TRANS_DDI_FUNC_CTL_C = 0x62400 
TRANS_DDI_FUNC_CTL_D = 0x63400 
TRANS_DDI_FUNC_CTL_DSI0 = 0x6B400 
TRANS_DDI_FUNC_CTL_DSI1 = 0x6BC00 

 
'''
Register field expected values 
'''
bits_per_color_10_BPC = 0b001
bits_per_color_12_BPC = 0b011 
bits_per_color_6_BPC = 0b010 
bits_per_color_8_BPC = 0b000 
bits_per_color_RESERVED = 0b0 
ddi_select_DDI_A = 0b0001 
ddi_select_DDI_B = 0b0010 
ddi_select_DDI_C = 0b0011 
ddi_select_DDI_USBC1 = 0b0100 
ddi_select_DDI_USBC2 = 0b0101 
ddi_select_DDI_USBC3 = 0b0110
ddi_select_DDI_USBC4 = 0b0111
ddi_select_DDI_USBC5 = 0b1000 
ddi_select_DDI_USBC6 = 0b1001 
ddi_select_NONE = 0b0000 
ddi_select_RESERVED = 0b0  
dp_vc_payload_allocate_DISABLE = 0b0 
dp_vc_payload_allocate_ENABLE = 0b1 
dss_branch_select_for_edp_LEFT_BRANCH = 0b0 
dss_branch_select_for_edp_RIGHT_BRANCH = 0b1 
edp_dsi_input_select_PIPE_A = 0b000 
edp_dsi_input_select_PIPE_B = 0b101 
edp_dsi_input_select_PIPE_C = 0b110 
edp_dsi_input_select_PIPE_D = 0b111 
edp_dsi_input_select_RESERVED = 0b0 
edp_input_select_A___ALWAYS_ON = 0b000 
edp_input_select_B___ON_OFF = 0b101 
edp_input_select_C___ON_OFF = 0b110 
edp_input_select_PIPE_D = 0b111 
edp_input_select_RESERVED = 0b0 
hdmi_dvi_hdcp_signaling_DISABLE = 0b0 
hdmi_dvi_hdcp_signaling_ENABLE = 0b1 
hdmi_scrambler_cts_enable_DISABLE = 0b0 
hdmi_scrambler_cts_enable_TRUE = 0b1 
hdmi_scrambler_reset_frequency_EVERY_LINE = 0b0 
hdmi_scrambler_reset_frequency_EVERY_OTHER_LINE = 0b1 
hdmi_scrambling_enabled_DISABLE = 0b0 
hdmi_scrambling_enabled_ENABLE = 0b1 
high_tmds_char_rate_DISABLE = 0b0 
high_tmds_char_rate_ENABLE = 0b1 
multistream_hdcp_select_NO_HDCP = 0b0 
multistream_hdcp_select_SELECT_HDCP = 0b1 
port_sync_mode_enable_DISABLE = 0b0 
port_sync_mode_enable_ENABLE = 0b1 
port_sync_mode_master_select_TRANSCODER_A = 0b01 
port_sync_mode_master_select_TRANSCODER_B = 0b10 
port_sync_mode_master_select_TRANSCODER_C = 0b11 
port_sync_mode_master_select_TRANSCODER_EDP = 0b00 
port_width_selection_RESERVED = 0b0 
port_width_selection_X1 = 0b000 
port_width_selection_X2 = 0b001 
port_width_selection_X3 = 0b010 
port_width_selection_X4 = 0b011 
sync_polarity_HIGH = 0b11 
sync_polarity_LOW = 0b00 
sync_polarity_VS_HIGH__HS_LOW = 0b10 
sync_polarity_VS_LOW__HS_HIGH = 0b01 
trans_ddi_function_enable_DISABLE = 0b0 
trans_ddi_function_enable_ENABLE = 0b1 
trans_ddi_mode_select_DP_MST = 0b011 
trans_ddi_mode_select_DP_SST = 0b010 
trans_ddi_mode_select_DVI = 0b001 
trans_ddi_mode_select_HDMI = 0b000 
trans_ddi_mode_select_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class TRANS_DDI_FUNC_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("hdmi_scrambling_enabled"     , ctypes.c_uint32, 1), # 0 to 0 
        ("port_width_selection"        , ctypes.c_uint32, 3), # 1 to 3 
        ("high_tmds_char_rate"         , ctypes.c_uint32, 1), # 4 to 4 
        ("multistream_hdcp_select"     , ctypes.c_uint32, 1), # 5 to 5 
        ("hdmi_scrambler_reset_frequency", ctypes.c_uint32, 1), # 6 to 6 
        ("hdmi_scrambler_cts_enable"   , ctypes.c_uint32, 1), # 7 to 7 
        ("dp_vc_payload_allocate"      , ctypes.c_uint32, 1), # 8 to 8 
        ("hdmi_dvi_hdcp_signaling"     , ctypes.c_uint32, 1), # 9 to 9 
        ("mst_transport_select"        , ctypes.c_uint32, 2), # 10 to 11 
        ("edp_dsi_input_select"        , ctypes.c_uint32, 3), # 12 to 14 
        ("reserved_15"                 , ctypes.c_uint32, 1), # 15 to 15 
        ("sync_polarity"               , ctypes.c_uint32, 2), # 16 to 17 
        ("reserved_18"                 , ctypes.c_uint32, 2), # 18 to 19 
        ("bits_per_color"              , ctypes.c_uint32, 3), # 20 to 22 
        ("dss_branch_select_for_edp"   , ctypes.c_uint32, 1), # 23 to 23 
        ("trans_ddi_mode_select"       , ctypes.c_uint32, 3), # 24 to 26        
        ("ddi_select"                  , ctypes.c_uint32, 4), # 27 to 30 
        ("trans_ddi_function_enable"   , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class TRANS_DDI_FUNC_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_DDI_FUNC_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
