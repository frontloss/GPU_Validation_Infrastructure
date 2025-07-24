import ctypes

'''
Register instance and offset
'''
VSC_EXT_SDP_CTL_0_A = 0x60200
VSC_EXT_SDP_CTL_0_B = 0x61290
VSC_EXT_SDP_CTL_0_C = 0x62290
VSC_EXT_SDP_CTL_0_D = 0x63290
VSC_EXT_SDP_CTL_1_A = 0x60294
VSC_EXT_SDP_CTL_1_B = 0x61294
VSC_EXT_SDP_CTL_1_C = 0x62294
VSC_EXT_SDP_CTL_1_D = 0x63294

'''
Register field expected values 
'''
vsc_extension_sdp_metadata_disable  = 0b0
vsc_extension_sdp_metadata_enable   = 0b1
buffer_empty                        = 0b1
buffer_not_empty                    = 0b0
buffer_ready_for_hw_use             = 0b1
buffer_not_ready_for_hw_use         = 0b0


'''
Register bitfield definition structure
'''
class VSC_EXT_SDP_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value" 						, ctypes.c_uint32, 8)		, # 0 to 7
        ("reserved_8"    					, ctypes.c_uint32, 5)		, # 8 to 13
        ("index_auto_increment" 			, ctypes.c_uint32, 1) 		, # 14 to 14
        ("reserved_15"    					, ctypes.c_uint32, 1)		, # 15 to 15
        ("buffer_ready" 					, ctypes.c_uint32, 1)		, # 16 to 16
        ("reserved_17"    					, ctypes.c_uint32, 7)		, # 17 to 23
        ("buffer_empty"						, ctypes.c_uint32, 1)		, # 24 to 24
		("reserved_25"    					, ctypes.c_uint32, 6)		, # 25 to 30
        ("vsc_extension_sdp_metadata_enable", ctypes.c_uint32, 1)		, # 31 to 31
    ]

 
class VSC_EXT_SDP_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VSC_EXT_SDP_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]

