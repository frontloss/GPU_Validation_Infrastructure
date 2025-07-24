import ctypes

'''
Register instance and offset 
'''
CDCLK_CTL = 0x46000

'''
Register field expected values 
'''

phy_clock_lane_select_LANE0=0b0
phy_clock_lane_select_LANE1=0b1
ssc_enable_pll_a_ENABLE = 0b1
ssc_enable_pll_a_DISABLE = 0b0
ssc_enable_pll_b_ENABLE = 0b1
ssc_enable_pll_b_DISABLE = 0b0
#to-do - add the poasible values for all fields based on requirement

'''
Register bitfield definition structure 
'''



class PORT_CLK_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ssc_enable_pll_b", ctypes.c_uint32, 1),  # 0 to 0
        ("ssc_enable_pll_a", ctypes.c_uint32, 1),  # 1 to 1
        ("reserved_6", ctypes.c_uint32, 6),  # 2 to 7
        ("phy_clock_lane_select", ctypes.c_uint32, 1),  #8 to 8
        ("maxpclk_ungate", ctypes.c_uint32, 1),  # 9 to 9
        ("forward_clk_ungate", ctypes.c_uint32, 1),  # 10 to 10
        ("reserved_1", ctypes.c_uint32, 1),  # 11 to 11
        ("ddi_clock_select", ctypes.c_uint32, 4), # 12 to 15
        ("tbt_clk_ack", ctypes.c_uint32, 1), # 18 to 18
        ("tbt_clk_request", ctypes.c_uint32, 1), # 19 to 19
        ("reserved_1", ctypes.c_uint32, 1), # 20 to 20
        ("ack_phy_release_refclk", ctypes.c_uint32, 1), #21 to 21
        ("requst_phy_release_refclk", ctypes.c_uint32, 1), #22 to 22
        ("refclk_select", ctypes.c_uint32, 1), #23 to 23
        ("pclk_refclk_ackln1", ctypes.c_uint32, 1), #24 to 24
        ("pclk_refclk_request_ln1", ctypes.c_uint32, 1), #25 to 25
        ("pclk_pll_ack_ln1", ctypes.c_uint32, 1), #26 to 26
        ("pclk_pll_request_ln1", ctypes.c_uint32, 1), #27 to 27
        ("pclk_refclk_ackln0", ctypes.c_uint32, 1), #28 to 28
        ("pclk_refclk_request_ln0", ctypes.c_uint32, 1), #29 to 29
        ("pclk_pll_ack_ln0", ctypes.c_uint32, 1), #30 to 30
        ("pclk_pll_request_ln0", ctypes.c_uint32, 1), #31 to 31

    ]


class PORT_CLK_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_CLK_CTL_REG),
        ("asUint", ctypes.c_uint32)]

