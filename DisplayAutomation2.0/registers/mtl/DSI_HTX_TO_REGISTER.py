import ctypes
 
'''
Register instance and offset 
'''
DSI_HTX_TO_DSI0 = 0x6B044 
DSI_HTX_TO_DSI1 = 0x6B844 

 
'''
Register field expected values 
'''
hs_tx_timeout_DEFAULT = 0xFFFF 

 
'''
Register bitfield defnition structure 
'''
class DSI_HTX_TO_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("htx_to"       , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"   , ctypes.c_uint32, 15), # 1 to 15 
        ("hs_tx_timeout" , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class DSI_HTX_TO_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_HTX_TO_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
