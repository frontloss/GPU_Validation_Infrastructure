##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/50054
import ctypes

'''
Register instance and offset
'''
CHICKEN_TRANS_A = 0x604E0
CHICKEN_TRANS_B = 0x614E0
CHICKEN_TRANS_C = 0x624E0
CHICKEN_TRANS_D = 0x634E0


'''
Register bitfield definition structure
'''
class CHICKEN_TRANS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('spare0', ctypes.c_uint32, 1),
        ('spare1', ctypes.c_uint32, 1),
        ('spare2', ctypes.c_uint32, 1),
        ('spare3', ctypes.c_uint32, 1),
        ('spare4', ctypes.c_uint32, 1),
        ('spare5', ctypes.c_uint32, 1),
        ('spare6', ctypes.c_uint32, 1),
        ('spare7', ctypes.c_uint32, 1),
        ('spare8', ctypes.c_uint32, 1),
        ('qux_frame_sync_event_timing', ctypes.c_uint32, 2),
        ('spare11', ctypes.c_uint32, 1),
        ('spare12', ctypes.c_uint32, 1),
        ('spare13', ctypes.c_uint32, 1),
        ('spare14', ctypes.c_uint32, 1),
        ('spare15', ctypes.c_uint32, 1),
        ('spare16', ctypes.c_uint32, 1),
        ('spare17', ctypes.c_uint32, 1),
        ('y_coordinate_base', ctypes.c_uint32, 1),
        ('cmtg_resync', ctypes.c_uint32, 1),
        ('spare20', ctypes.c_uint32, 1),
        ('spare21', ctypes.c_uint32, 1),
        ('spare22', ctypes.c_uint32, 1),
        ('spare23', ctypes.c_uint32, 1),
        ('hdmi_vbi_while_port_off', ctypes.c_uint32, 1),
        ('spare25', ctypes.c_uint32, 1),
        ('dda_accumulate_count_update', ctypes.c_uint32, 1),
        ('frame_start_delay', ctypes.c_uint32, 2),
        ('dp_active_video_disable', ctypes.c_uint32, 1),
        ('spare30', ctypes.c_uint32, 1),
        ('spare31', ctypes.c_uint32, 1),
    ]


class CHICKEN_TRANS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CHICKEN_TRANS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
