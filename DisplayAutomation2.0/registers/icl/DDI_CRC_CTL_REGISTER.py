import ctypes
 
'''
Register instance and offset 
'''
DDI_CRC_CTL_A = 0x64050 
DDI_CRC_CTL_B = 0x64150 
DDI_CRC_CTL_C = 0x64250 
DDI_CRC_CTL_D = 0x64350 
DDI_CRC_CTL_E = 0x64450 
DDI_CRC_CTL_F = 0x64550 

 
'''
Register field expected values 
'''
accum_enable_DISABLE = 0b0 
accum_enable_ENABLE = 0b1 
crc_change_CHANGE = 0b1 
crc_change_NO_CHANGE = 0b0 
crc_channel_mask_ALL_CHANNELS_UN_MASKED = 0b0000 
crc_channel_mask_MASK_CHANNEL_0 = 0b01
crc_channel_mask_MASK_CHANNEL_1 = 0b10
crc_channel_mask_MASK_CHANNEL_2 = 0b111
crc_channel_mask_MASK_CHANNEL_3 = 0b1000
crc_channel_mask_UN_MASK_CHANNEL_0 = 0b1110
crc_channel_mask_UN_MASK_CHANNEL_1 = 0b1101
crc_channel_mask_UN_MASK_CHANNEL_2 = 0b1011
crc_channel_mask_UN_MASK_CHANNEL_3 = 0b0111
crc_done_DONE = 0b1 
crc_done_NOT_DONE = 0b0 
enable_crc_DISABLE = 0b0 
enable_crc_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DDI_CRC_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("accum_start_frame" , ctypes.c_uint32, 4), # 0 to 3 
        ("accum_end_frame"  , ctypes.c_uint32, 4), # 4 to 7 
        ("accum_enable"     , ctypes.c_uint32, 1), # 8 to 8 
        ("reserved_9"       , ctypes.c_uint32, 7), # 9 to 15 
        ("crc_channel_mask" , ctypes.c_uint32, 4), # 16 to 19 
        ("reserved_20"      , ctypes.c_uint32, 4), # 20 to 23 
        ("crc_done"         , ctypes.c_uint32, 1), # 24 to 24 
        ("crc_change"       , ctypes.c_uint32, 1), # 25 to 25 
        ("reserved_26"      , ctypes.c_uint32, 5), # 26 to 30 
        ("enable_crc"       , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DDI_CRC_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DDI_CRC_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
