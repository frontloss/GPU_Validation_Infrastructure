import ctypes

'''
Register instance and offset 
'''
FBC_CHICKEN_A = 0x43224


'''
Register bitfield definition structure 
'''
class FBC_CHICKEN_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('spare_0', ctypes.c_uint32, 1),
        ('spare_1', ctypes.c_uint32, 1),
        ('spare_2', ctypes.c_uint32, 1),
        ('spare_3', ctypes.c_uint32, 1),
        ('spare_4', ctypes.c_uint32, 1),
        ('spare_5', ctypes.c_uint32, 1),
        ('dst_comptag_offset', ctypes.c_uint32, 2),
        ('dis_dummy_0', ctypes.c_uint32, 1),
        ('force_off', ctypes.c_uint32, 1),
        ('skip_seg_count', ctypes.c_uint32, 2),
        ('skip_seg_enable', ctypes.c_uint32, 1),
        ('force_slb_invalidation', ctypes.c_uint32, 1),
        ('spare_14', ctypes.c_uint32, 1),
        ('spare_15', ctypes.c_uint32, 1),
        ('spare_16', ctypes.c_uint32, 1),
        ('spare_17', ctypes.c_uint32, 1),
        ('spare_18', ctypes.c_uint32, 1),
        ('spare_19', ctypes.c_uint32, 1),
        ('spare_20', ctypes.c_uint32, 1),
        ('spare_21', ctypes.c_uint32, 1),
        ('spare_22', ctypes.c_uint32, 1),
        ('nuke_on_any_modification', ctypes.c_uint32, 1),
        ('read_write_collision_fix_disable', ctypes.c_uint32, 1),
        ('dpfc_ctrl_chicken', ctypes.c_uint32, 1),
        ('dis_comptag_underrun_nuke', ctypes.c_uint32, 1),
        ('dis_rc_nuke', ctypes.c_uint32, 1),
        ('dis_flip_nuke', ctypes.c_uint32, 1),
        ('dis_pipe_underrun_nuke', ctypes.c_uint32, 1),
        ('dis_count_nuke', ctypes.c_uint32, 1),
        ('dis_cwb_nuke', ctypes.c_uint32, 1),
    ]


class FBC_CHICKEN_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      FBC_CHICKEN_REG),
        ("asUint", ctypes.c_uint32)]
