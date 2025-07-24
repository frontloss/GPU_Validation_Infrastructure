import ctypes
 
'''
Register instance and offset 
'''
DSI_LRX_H_TO_DSI0 = 0x6B048 
DSI_LRX_H_TO_DSI1 = 0x6B848 

 
'''
Register field expected values 
'''
lrx_h_to_DEFAULT = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DSI_LRX_H_TO_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("lp_rx_h_timeout" , ctypes.c_uint32, 16), # 0 to 15 
        ("lrx_h_to"       , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"    , ctypes.c_uint32, 15), # 17 to 31 
    ]

 
class DSI_LRX_H_TO_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_LRX_H_TO_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
