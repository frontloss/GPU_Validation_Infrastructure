##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/49533
import ctypes

'''
Register instance and offset 
'''
DDI_BUF_CTL_A = 0x64000
DDI_BUF_CTL_B = 0x64100
DDI_BUF_CTL_C = 0x64200
DDI_BUF_CTL_D = 0x64300
DDI_BUF_CTL_E = 0x64400
DDI_BUF_CTL_F = 0x64500

'''
Register field expected values 
'''
ddi_buffer_enable_DISABLE = 0b0
ddi_buffer_enable_ENABLE = 0b1
override_training_enable_DISABLE_OVERRIDE = 0b0
override_training_enable_ENABLE_OVERRIDE = 0b1
phy_param_adjust_DISABLE = 0b0
phy_param_adjust_ENABLE = 0b1
phy_lane_width_10BIT = 0b00
phy_lane_width_20BIT = 0b01
phy_lane_width_40BIT = 0b10
port_reversal_NOT_REVERSED = 0b0
port_reversal_REVERSED = 0b1
ddi_idle_status_BUFFER_IDLE = 0b1
ddi_idle_status_BUFFER_NOT_IDLE = 0b0
type_c_phy_ownership_RELEASE = 0b0
type_c_phy_ownership_TAKE = 0b1
dp_port_width_selection_RESERVED = 0b100 - 0b111
dp_port_width_selection_X1 = 0b000
dp_port_width_selection_X2 = 0b001
dp_port_width_selection_X4 = 0b011
init_display_detected_DETECTED = 0b1
init_display_detected_NOT_DETECTED = 0b0

'''
Register bitfield defnition structure 
'''


class DDI_BUF_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("init_display_detected", ctypes.c_uint32, 1),  # 0 to 0
        ("dp_port_width_selection", ctypes.c_uint32, 3),  # 1 to 3
        ("reserved_4", ctypes.c_uint32, 2),  # 4 to 5
        ("type_c_phy_ownership", ctypes.c_uint32, 1),  # 6 to 6
        ("ddi_idle_status", ctypes.c_uint32, 1),  # 7 to 7
        ("usb_type_c_dp_lane_staggering_delay", ctypes.c_uint32, 8),  # 8 to 15
        ("port_reversal", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 1),  # 17 to 17
        ("phy_lane_width", ctypes.c_uint32, 2),  # 18 to 19
        ("phy_link_rate", ctypes.c_uint32, 4),  # 20 to 23
        ("reserved_24", ctypes.c_uint32, 4),  # 24 to 27
        ("phy_param_adjust", ctypes.c_uint32, 1),  # 28 to 28
        ("override_training_enable", ctypes.c_uint32, 1),  # 29 to 29
        ("reserved_30", ctypes.c_uint32, 1),  # 30 to 30
        ("ddi_buffer_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class DDI_BUF_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DDI_BUF_CTL_REG),
        ("asUint", ctypes.c_uint32)]

