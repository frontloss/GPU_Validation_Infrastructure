import ctypes
 
'''
Register instance and offset 
'''
TRANS_DDI_FUNC_CTL2_A = 0x60404 
TRANS_DDI_FUNC_CTL2_B = 0x61404 
TRANS_DDI_FUNC_CTL2_C = 0x62404 
TRANS_DDI_FUNC_CTL2_D = 0x63404 
TRANS_DDI_FUNC_CTL2_DSI0 = 0x6B404 
TRANS_DDI_FUNC_CTL2_DSI1 = 0x6BC04 
TRANS_DDI_FUNC_CTL2_EDP = 0x6F404 

 
'''
Register field expected values 
'''
port_sync_mode_enable_DISABLE = 0b0 
port_sync_mode_enable_ENABLE = 0b1 
port_sync_mode_master_select_TRANSCODER_A = 0b001 
port_sync_mode_master_select_TRANSCODER_B = 0b010 
port_sync_mode_master_select_TRANSCODER_C = 0b011 
port_sync_mode_master_select_TRANSCODER_D = 0b100 
port_sync_mode_master_select_TRANSCODER_EDP = 0b000 

 
'''
Register bitfield defnition structure 
'''
class TRANS_DDI_FUNC_CTL2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("port_sync_mode_master_select" , ctypes.c_uint32, 3), # 0 to 2 
        ("reserved_3"                  , ctypes.c_uint32, 1), # 3 to 3 
        ("port_sync_mode_enable"       , ctypes.c_uint32, 1), # 4 to 4 
        ("reserved_5"                  , ctypes.c_uint32, 27), # 5 to 31 
    ]

 
class TRANS_DDI_FUNC_CTL2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_DDI_FUNC_CTL2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
