import ctypes

'''
Register instance and offset
'''
VSC_EXT_SDP_DATA_0_A = 0x60298
VSC_EXT_SDP_DATA_0_B = 0x61298
VSC_EXT_SDP_DATA_0_C = 0x62298
VSC_EXT_SDP_DATA_0_D = 0x63298
VSC_EXT_SDP_DATA_1_A = 0x6029C
VSC_EXT_SDP_DATA_1_B = 0x6129C
VSC_EXT_SDP_DATA_1_C = 0x6229C
VSC_EXT_SDP_DATA_1_D = 0x6329C

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''
class VSC_EXT_SDP_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data" , ctypes.c_uint32, 32), # 0 to 31
    ]

class VSC_EXT_SDP_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VSC_EXT_SDP_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]

