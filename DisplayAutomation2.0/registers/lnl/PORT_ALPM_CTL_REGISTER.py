##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/70277

import ctypes

##
# Register instance and offset

PORT_ALPM_CTL_A = 0x16FA2C
PORT_ALPM_CTL_B = 0x16FC2C


##
# Register bitfield definition structure
class PortAlpmCtlReg(ctypes.LittleEndianStructure):

    _fields_ = [
        ('silence_period', ctypes.c_uint32, 8),  # 0 to 7
        ('reserved_8', ctypes.c_uint32, 8),  # 8 to 15
        ('max_phy_swing_hold', ctypes.c_uint32, 4),  # 16 to 19
        ('max_phy_swing_setup', ctypes.c_uint32, 4),  # 20 to 23
        ('reserved_24', ctypes.c_uint32, 7),
        ('alpm_aux_less_enable', ctypes.c_uint32, 1),  # 31 to 31
    ]


class PORT_ALPM_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PortAlpmCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
