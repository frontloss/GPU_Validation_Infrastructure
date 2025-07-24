import ctypes
 
'''
Register instance and offset 
'''
MIPIA_DSI_FUNC_PRG_REG = 0x6B00C 
MIPIC_DSI_FUNC_PRG_REG = 0x6B80C 

 
'''
Register field expected values 
'''
data_lanes_prg_r_eg_DEFAULT = 0b001 
supported_data_width_in_command_mode_16_BIT_DATA = 0b001 
supported_data_width_in_command_mode_COMMAND_MODE_NOT_SUPPORTED = 0b000 
supported_data_width_in_command_mode_OPTION_2 = 0b101 
supported_data_width_in_command_mode_OPTION_2_SKIP_LAST_BYTE = 0b110 
supported_data_width_in_command_mode_OPTION_2_SKIP_LAST_TWO_BYES = 0b111 
supported_data_width_in_command_mode_RESERVED = 0b0 
supported_format_in_video_mode_COMPRESSED_IMAGE_DATA = 0b1000 
supported_format_in_video_mode_RGB565 = 0b0001 
supported_format_in_video_mode_RGB666 = 0b0010 
supported_format_in_video_mode_RGB888 = 0b0100 
supported_format_in_video_mode_RGB_666_LOOSELY_PACKED_FORMAT = 0b0011 
supported_format_in_video_mode_VIDEO_MODE_NOT_SUPPORTED = 0b0000 

 
'''
Register bitfield defnition structure 
'''
class MIPI_DSI_FUNC_PRG_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data_lanes_prg_r_eg"                 , ctypes.c_uint32, 3), # 0 to 2 
        ("channel_number_for_video_mode"       , ctypes.c_uint32, 2), # 3 to 4 
        ("channel_number_for_command_mode"     , ctypes.c_uint32, 2), # 5 to 6 
        ("supported_format_in_video_mode"      , ctypes.c_uint32, 4), # 7 to 10 
        ("reserved_1"                          , ctypes.c_uint32, 2), # 11 to 12 
        ("supported_data_width_in_command_mode" , ctypes.c_uint32, 3), # 13 to 15 
        ("reserved_16"                         , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_DSI_FUNC_PRG_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_DSI_FUNC_PRG_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
