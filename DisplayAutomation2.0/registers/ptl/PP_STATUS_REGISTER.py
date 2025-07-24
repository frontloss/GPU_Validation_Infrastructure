import ctypes
 
'''
Register instance and offset 
'''
PP_STATUS = 0xC7200 
PP_STATUS_2 = 0xC7300 

 
'''
Register field expected values 
'''
internal_sequence_state_POWER_OFF__WAIT_FOR_CYCLE_DELAY_S0_1 = 0b0001 
internal_sequence_state_POWER_OFF_IDLE_S0_0 = 0b0000 
internal_sequence_state_POWER_OFF_S0_2 = 0b0010 
internal_sequence_state_POWER_OFF_S0_3 = 0b0011 
internal_sequence_state_POWER_ON__WAIT_FOR_CYCLE_DELAY_S1_3 = 0b1011 
internal_sequence_state_POWER_ON_IDLE_S1_0 = 0b1000 
internal_sequence_state_POWER_ON_S1_1 = 0b1001 
internal_sequence_state_POWER_ON_S1_2 = 0b1010 
internal_sequence_state_RESET = 0b1111 
panel_power_on_status_OFF = 0b0 
panel_power_on_status_ON = 0b1 
power_cycle_delay_active_ACTIVE = 0b1 
power_cycle_delay_active_NOT_ACTIVE = 0b0 
power_sequence_progress_NONE = 0b00 
power_sequence_progress_POWER_DOWN = 0b10 
power_sequence_progress_POWER_UP = 0b01 
power_sequence_progress_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class PP_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("internal_sequence_state" , ctypes.c_uint32, 4), # 0 to 3 
        ("reserved_4"              , ctypes.c_uint32, 23), # 4 to 26 
        ("power_cycle_delay_active" , ctypes.c_uint32, 1), # 27 to 27 
        ("power_sequence_progress" , ctypes.c_uint32, 2), # 28 to 29 
        ("reserved_30"             , ctypes.c_uint32, 1), # 30 to 30 
        ("panel_power_on_status"   , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PP_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PP_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
