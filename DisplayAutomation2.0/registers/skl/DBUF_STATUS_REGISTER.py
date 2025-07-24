import ctypes
 
'''
Register instance and offset 
'''
DBUF_STATUS = 0x4500C 
DBUF_STATUS_S1 = 0x4500C 
DBUF_STATUS_S2 = 0x44FEC 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DBUF_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("trackers_available"     , ctypes.c_uint32, 16), # 0 to 15 
        ("not_used"               , ctypes.c_uint32, 1), # 16 to 16 
        ("tracker_over_allocated" , ctypes.c_uint32, 1), # 21 to 21 
        ("dataout_fifo_overrun"   , ctypes.c_uint32, 1), # 30 to 30 
        ("valid_block_overwritten" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DBUF_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBUF_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
