import ctypes
 
'''
Register instance and offset 
'''
DSI_CMD_FRMCTL_DSI0 = 0x6B034 
DSI_CMD_FRMCTL_DSI1 = 0x6B834

 
'''
Register field expected values 
'''
null_packet_enable_NULL_PACKET_INJECTION_DISABLED = 0 
null_packet_enable_NULL_PACKET_INJECTION_ENABLED = 1 
periodic_frame_update_enable_PERIODIC_FRAME_UPDATE_DISABLED = 0
periodic_frame_update_enable_PERIODIC_FRAME_UPDATE_ENABLED = 1
frame_update_request_NO_FRAME_REQUEST_PRESENT = 0
frame_update_request_FRAME_REQUEST_PRESENT = 1

 
'''
Register bitfield defnition structure 
'''
class DSI_CMD_FRMCTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
		("frame_in_progress" ,          ctypes.c_uint32, 1), # 0 to 0         
		("reserved_1" ,                 ctypes.c_uint32, 27), # 1 to 27
        ("null_packet_enable" ,         ctypes.c_uint32, 1), # 28 to 28
        ("periodic_frame_update_enable" , ctypes.c_uint32, 1), # 29 to 29
        ("reserved_30" ,                ctypes.c_uint32, 1), # 30 to 30
        ("frame_update_request" ,       ctypes.c_uint32, 1), # 31 to 31        
    ]

 
class DSI_CMD_FRMCTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_CMD_FRMCTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
