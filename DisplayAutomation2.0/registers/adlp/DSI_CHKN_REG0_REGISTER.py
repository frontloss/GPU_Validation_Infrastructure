# https://gfxspecs.intel.com/Predator/Home/Index/50184
import ctypes
 
'''
Register instance and offset 
'''
DSI_CHKN_REG0_0 = 0x6B0C0
DSI_CHKN_REG0_1 = 0x6B8C0

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DSI_CHKN_REG0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("hs_to_hs_turnaround_guardband", ctypes.c_uint32, 8),  # 0 to 7
        ("spare_9"                      , ctypes.c_uint32, 4),  # 8 to 11
        ("lp_to_hs_wakeup_guardband"    , ctypes.c_uint32, 4),  # 12 to 15
        ("stereoscopic_3d_hbp_as_vertical_space", ctypes.c_uint32, 1),  # 16 to 16
        ("stereoscopic_3d_update_frequency", ctypes.c_uint32, 1),  # 17 to 17
        ("dual_link_mirroring_disable",  ctypes.c_uint32, 1),  # 18 to 18
        ("dsc_payload_format_disable", ctypes.c_uint32, 1),  # 19 to 19
        ("ignore_reset_warning", ctypes.c_uint32, 1),  # 20 to 20
        ("no_vertical_space_delay", ctypes.c_uint32, 1),  # 21 to 21
        ("line_count_adjustment_disable", ctypes.c_uint32, 1),  # 22 to 22
        ("spare_23", ctypes.c_uint32, 9),  # 23 to 31
    ]

 
class DSI_CHKN_REG0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_CHKN_REG0_REG),
        ("asUint", ctypes.c_uint32)]
 
