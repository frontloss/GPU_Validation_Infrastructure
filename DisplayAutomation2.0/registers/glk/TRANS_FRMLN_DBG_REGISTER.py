import ctypes
 
'''
Register instance and offset 
'''
TRANS_FRMLN_DBG_A = 0x70050 
TRANS_FRMLN_DBG_B = 0x71050 
TRANS_FRMLN_DBG_C = 0x72050 
TRANS_FRMLN_DBG_D = 0x73050 
TRANS_FRMLN_DBG_DSI0 = 0x7B050 
TRANS_FRMLN_DBG_DSI1 = 0x7B850 
TRANS_FRMLN_DBG_EDP = 0x7F050 
TRANS_FRMLN_DBG_WD0 = 0x7E050 
TRANS_FRMLN_DBG_WD1 = 0x7D050 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_FRMLN_DBG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("line_counter_for_display" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"             , ctypes.c_uint32, 3), # 13 to 15 
        ("frame_counter_lsbs"      , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class TRANS_FRMLN_DBG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_FRMLN_DBG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
