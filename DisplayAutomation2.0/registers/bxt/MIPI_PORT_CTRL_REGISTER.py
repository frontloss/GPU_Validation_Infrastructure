import ctypes
 
'''
Register instance and offset 
'''
MIPIA_PORT_CTRL = 0x6B0C0 
MIPIC_PORT_CTRL = 0x6B8C0 

 
'''
Register field expected values 
'''
adjdly_hstx_DEFAULT = 0b0100 
afe_latchout_LP00 = 0 
afe_latchout_LP11 = 1 
effect_NO_TEARING_EFFECT_REQUIRED = 0b00 
effect_RESERVED = 0b0 
effect_TE_TRIGGER_BY_GPIO_PIN = 0b10 
effect_TE_TRIGGER_BY_MIPI_DPHY_AND_DSI_PROTOCOL = 0b01 
en_DISABLE = 0 
en_ENABLE = 1 
flisdsi_adjdly_hstx_mipi_c_lower_order_DEFAULT = 0b011 
flisdsi_adjdly_hstx_mipia_DEFAULT = 0b0100 
flisdsi_adjdly_hstx_mipic_high_order_DEFAULT = 1 
lpoutput_hold_DISABLE = 0 
lpoutput_hold_ENABLE = 1 
mipi4dphy_adjdly_hstx_mipi_c_DEFAULT = 0b0100 
mipi_dual_link_mode_FRONT_BACK = 0 
mipi_dual_link_mode_PIXEL_ALTERNATIVE = 1 
mipi_lanes_configuration_DISABLE = 0b0 
mipi_lanes_configuration_ENABLE = 0b1 
selflopped_hstx_DISABLE = 0 
selflopped_hstx_ENABLE = 1 
te_counter_delay_DISABLE = 0 
te_counter_delay_ENABLE = 1 
te_deglitch_enable_DISABLE = 0 
te_deglitch_enable_ENABLE = 1 

 
'''
Register bitfield defnition structure 
'''
class MIPI_PORT_CTRL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("mipi_lanes_configuration"              , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"                            , ctypes.c_uint32, 1), # 1 to 1 
        ("effect"                                , ctypes.c_uint32, 2), # 2 to 3 
        ("te_counter_delay"                      , ctypes.c_uint32, 1), # 4 to 4 
        ("flisdsi_adjdly_hstx_mipi_c_lower_order" , ctypes.c_uint32, 3), # 5 to 7 
        ("spare_10_to_8"                         , ctypes.c_uint32, 3), # 8 to 10 
        ("mipi4dphy_adjdly_hstx_mipi_c"          , ctypes.c_uint32, 4), # 11 to 14 
        ("flisdsi_adjdly_hstx_mipic_high_order"  , ctypes.c_uint32, 1), # 15 to 15 
        ("lpoutput_hold"                         , ctypes.c_uint32, 1), # 16 to 16 
        ("afe_latchout"                          , ctypes.c_uint32, 1), # 17 to 17 
        ("flisdsi_adjdly_hstx_mipia"             , ctypes.c_uint32, 4), # 18 to 21 
        ("reserved_22"                           , ctypes.c_uint32, 1), # 22 to 22 
        ("selflopped_hstx"                       , ctypes.c_uint32, 1), # 23 to 23 
        ("reserved_24"                           , ctypes.c_uint32, 2), # 24 to 25 
        ("mipi_dual_link_mode"                   , ctypes.c_uint32, 1), # 26 to 26 
        ("adjdly_hstx"                           , ctypes.c_uint32, 4), # 27 to 30 
        ("en"                                    , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class MIPI_PORT_CTRL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_PORT_CTRL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
