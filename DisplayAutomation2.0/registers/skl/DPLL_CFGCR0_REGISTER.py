import ctypes
 
'''
Register instance and offset 
'''
DPLL0_CFGCR0 = 0x6C000 
DPLL1_CFGCR0 = 0x6C080 
DPLL2_CFGCR0 = 0x6C100 

 
'''
Register field expected values 
'''
dco_fraction_DEFAULT = 0x4000 
dco_integer_DEFAULT = 0x151 
dp_link_rate_1080 = b0100 
dp_link_rate_1350 = b0001 
dp_link_rate_1620 = b0011 
dp_link_rate_2160 = b0101 
dp_link_rate_2700 = b0000 
dp_link_rate_3240 = b0110 
dp_link_rate_4050 = b0111 
dp_link_rate_810 = b0010 
hdmi_mode_DP_MODE = b0 
hdmi_mode_HDMI_MODE = b1 
ssc_enable_DISABLE = b0 
ssc_enable_ENABLE = b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CFGCR0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dco_integer ",    ctypes.c_uint32,9), # 0 to 8 
        ("dco_fraction",    ctypes.c_uint32,15), # 9 to 23 
        ("dp_link_rate",    ctypes.c_uint32,4), # 24 to 27 
        ("ssc_enable  ",    ctypes.c_uint32,1), # 28 to 28 
        ("hdmi_mode   ",    ctypes.c_uint32,1), # 29 to 29 
        ("reserved_30 ",    ctypes.c_uint32,2), # 30 to 31 
        ("reserved_31 ",    ctypes.c_uint32,1), # 31 to 31 
    ]

 
class DPLL_CFGCR0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CFGCR0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
