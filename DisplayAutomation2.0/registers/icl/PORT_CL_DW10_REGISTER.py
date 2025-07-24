import ctypes
 
'''
Register instance and offset 
'''
PORT_CL_DW10_A = 0x162028 
PORT_CL_DW10_B = 0x6C028 

 
'''
Register field expected values 
'''
enable_1_2v_DISABLE = 0b0 
enable_1_2v_ENABLE = 0b1 
pg_seq_delay_override_enable_DISABLE = 0b0 
pg_seq_delay_override_enable_ENABLE = 0b1 
static_power_down_ddi_POWER_UP_ALL_LANES = 0b0000 
static_power_down_ddi_POWER_DOWN_LANES_3_2 = 0b1100 
static_power_down_ddi_POWER_DOWN_LANES_3_2_1 = 0b1110 
static_power_down_ddi_POWER_DOWN_LANES_1_0 = 0b0011 
static_power_down_ddi_POWER_DOWN_LANES_2_1_0 = 0b0111 
static_power_down_ddi_POWER_DOWN_LANE_3 = 0b1000
static_power_down_ddi_POWER_DOWN_LANES_3_1 = 0b1010 
static_power_down_ddi_POWER_DOWN_LANES_3_1_0 = 0b1011 

 
'''
Register bitfield defnition structure 
'''
class PORT_CL_DW10_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                  , ctypes.c_uint32, 4), # 0 to 3 
        ("static_power_down_ddi"       , ctypes.c_uint32, 4), # 4 to 7 
        ("reserved_8"                  , ctypes.c_uint32, 13), # 8 to 20 
        ("reserved_21"                 , ctypes.c_uint32, 2), # 21 to 22 
        ("enable_1.2v"                 , ctypes.c_uint32, 1), # 23 to 23 
        ("pg_seq_delay_override_enable" , ctypes.c_uint32, 1), # 24 to 24 
        ("pg_seq_delay_override"       , ctypes.c_uint32, 2), # 25 to 26 
        ("reserved_27"                 , ctypes.c_uint32, 5), # 27 to 31 
    ]

 
class PORT_CL_DW10_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_CL_DW10_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
