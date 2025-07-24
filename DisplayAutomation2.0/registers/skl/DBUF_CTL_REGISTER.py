import ctypes
 
'''
Register instance and offset 
'''
DBUF_CTL = 0x45008 
DBUF_CTL_S1 = 0x45008 
DBUF_CTL_S2 = 0x44FE8 

 
'''
Register field expected values 
'''
dbuf_power_request_DISABLE = 0b0 
dbuf_power_request_ENABLE = 0b1 
dbuf_power_state_DISABLED = 0b0 
dbuf_power_state_ENABLED = 0b1 
power_gate_dis_override_DO_NOT_OVERRIDE = 0b0 
power_gate_dis_override_OVERRIDE = 0b1 
tracker_state_service_DEFAULT = 0b1100 

 
'''
Register bitfield defnition structure 
'''
class DBUF_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"             , ctypes.c_uint32, 19), # 0 to 18 
        ("tracker_state_service"  , ctypes.c_uint32, 5), # 19 to 23 
        ("power_gate_delay"       , ctypes.c_uint32, 2), # 24 to 25 
        ("reserved_26"            , ctypes.c_uint32, 1), # 26 to 26 
        ("power_gate_dis_override" , ctypes.c_uint32, 1), # 27 to 27 
        ("reserved_28"            , ctypes.c_uint32, 2), # 28 to 29 
        ("dbuf_power_state"       , ctypes.c_uint32, 1), # 30 to 30 
        ("dbuf_power_request"     , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DBUF_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBUF_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
