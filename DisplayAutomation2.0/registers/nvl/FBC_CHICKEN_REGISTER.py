import ctypes

'''
Register instance and offset 
'''
FBC_CHICKEN_A = 0x43224
FBC_CHICKEN_B = 0x43264


'''
Register bitfield definition structure 
'''
class FBC_CHICKEN_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('comptag_gating_fix_disable', ctypes.c_uint32, 1),  # BIT 0
        ('slb_invalidate_nuke_fix_disable', ctypes.c_uint32, 1),  # BIT 1
        ('spare_2', ctypes.c_uint32, 1),  # BIT 2
        ('underrun2_ppc_fix_disable', ctypes.c_uint32, 1),  # BIT 3
        ('rc_nuke_for_psr_fix_disable', ctypes.c_uint32, 1),  # BIT 4
        ('override_automatic_disable', ctypes.c_uint32, 1),  # BIT 5
        ('dst_comptag_offset', ctypes.c_uint32, 2),  # BIT 6 to BIT 7
        ('spare_8', ctypes.c_uint32, 1),  # BIT 8
        ('spare_9', ctypes.c_uint32, 1),  # BIT 9
        ('skip_seg_count', ctypes.c_uint32, 2),  # BIT 10 to BIT 11
        ('skip_seg_enable', ctypes.c_uint32, 1),  # BIT 12
        ('force_slb_invalidation', ctypes.c_uint32, 1),  # BIT 13
        ('comp_dummy_pixel', ctypes.c_uint32, 1),  # BIT 14
        ('psr_link_off_nuke_fix_disable', ctypes.c_uint32, 1),  # BIT 15
        ('init_state_clear_fix_disable', ctypes.c_uint32, 1),  # BIT 16
        ('flush_last_segment_fix_enable', ctypes.c_uint32, 1),  # BIT 17
        ('spare_18', ctypes.c_uint32, 1),  # BIT 18
        ('disable_slb_read_count_hold', ctypes.c_uint32, 1),  # BIT 19
        ('spare_20', ctypes.c_uint32, 1),  # BIT 20
        ('dis_vtd_fault_nuke', ctypes.c_uint32, 1),  # BIT 21
        ('height_4096_fix_disable', ctypes.c_uint32, 1),  # BIT 22
        ('spare_23', ctypes.c_uint32, 1),  # BIT 23
        ('read_write_collision_fix_disable', ctypes.c_uint32, 1),  # BIT 24
        ('wb_ignore_fill', ctypes.c_uint32, 1),  # BIT 25
        ('dis_comptag_underrun_nuke', ctypes.c_uint32, 1),  # BIT 26
        ('multiframe_nuke_recovery', ctypes.c_uint32, 1),  # BIT 27
        ('dis_flip_nuke', ctypes.c_uint32, 1),  # BIT 28
        ('dis_Pipe_underrun_nuke', ctypes.c_uint32, 1),  # BIT 29
        ('dis_count_nuke', ctypes.c_uint32, 1),  # BIT 30
        ('dis_cwb_nuke', ctypes.c_uint32, 1),  # BIT 31
    ]


class FBC_CHICKEN_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_CHICKEN_REG),
        ("asUint", ctypes.c_uint32)]
