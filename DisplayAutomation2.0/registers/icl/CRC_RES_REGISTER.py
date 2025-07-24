import ctypes
 
'''
Register instance and offset 
'''
DDI_CRC_RES_A = 0x64064 
DDI_CRC_RES_B = 0x64164 
DDI_CRC_RES_C = 0x64264 
DDI_CRC_RES_D = 0x64364 
DDI_CRC_RES_E = 0x64464 
DDI_CRC_RES_F = 0x64564 
DDI_CRC_RES_SRD_A = 0x6406C 
DDI_CRC_RES_SRD_B = 0x6416C 
DDI_CRC_RES_SRD_C = 0x6426C 
DDI_CRC_RES_SRD_D = 0x6436C 
DDI_CRC_RES_SRD_E = 0x6446C 
DDI_CRC_RES_SRD_F = 0x6456C 
PIPE_CD_CRC_RES_A = 0x60064 
PIPE_CD_CRC_RES_B = 0x61064 
PIPE_CD_CRC_RES_C = 0x62064 
TRANS_DOT_CRC_RES_A = 0x60094 
TRANS_DOT_CRC_RES_B = 0x61094 
TRANS_DOT_CRC_RES_C = 0x62094 
TRANS_DOT_CRC_RES_D = 0x63094 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CRC_RES_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("crc_result_value" , ctypes.c_uint32, 32), # 0 to 31 
    ]

 
class CRC_RES_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CRC_RES_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
