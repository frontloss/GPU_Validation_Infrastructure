import ctypes

'''
Register instance and offset
'''
CHICKEN_DCPR_1 = 0x46430


'''
Register bitfield definition structure
'''
class CHICKEN_DCPR_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('sw_reset_length', ctypes.c_uint32, 5),
        ('spare5', ctypes.c_uint32, 1),
        ('spare6', ctypes.c_uint32, 1),
        ('ddi_clock_reg_access', ctypes.c_uint32, 1),
        ('PortRegAccessOverride', ctypes.c_uint32, 1),
        ('spare9', ctypes.c_uint32, 1),
        ('spare10', ctypes.c_uint32, 1),
        ('idle_threshold', ctypes.c_uint32, 2),
        ('idle_wakemem_Mask', ctypes.c_uint32, 1),
        ('memup_response_wait', ctypes.c_uint32, 1),
        ('disable_flr_srd', ctypes.c_uint32, 1),
        ('spare16', ctypes.c_uint32, 1),
        ('spare17', ctypes.c_uint32, 1),
        ('spare18', ctypes.c_uint32, 1),
        ('display_clock_gating_override', ctypes.c_uint32, 1),
        ('block_block_fill_response_override', ctypes.c_uint32, 1),
        ('dg_empty_de_wake_overwrite', ctypes.c_uint32, 1),
        ('spare22', ctypes.c_uint32, 1),
        ('spare23', ctypes.c_uint32, 1),
        ('spare24', ctypes.c_uint32, 1),
        ('spare25', ctypes.c_uint32, 1),
        ('spare26', ctypes.c_uint32, 1),
        ('spare27', ctypes.c_uint32, 1),
        ('spare28', ctypes.c_uint32, 1),
        ('spare29', ctypes.c_uint32, 1),
        ('spare30', ctypes.c_uint32, 1),
        ('spare31', ctypes.c_uint32, 1),
    ]


class CHICKEN_DCPR_1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CHICKEN_DCPR_REG ),
        ("asUint", ctypes.c_uint32 ) ]
