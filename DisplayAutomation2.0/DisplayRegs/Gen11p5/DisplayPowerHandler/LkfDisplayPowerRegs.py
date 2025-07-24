# ===========================================================================
#
#    Copyright (c) Intel Corporation (2000 - 2020)
#
#    INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
#    ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
#    INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
#    ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
#    MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
#    OTHER WARRANTY.  Intel disclaims all liability, including liability for
#    infringement of any proprietary rights, relating to use of the code. No license,
#    express or implied, by estoppel or otherwise, to any intellectual property
#    rights is granted herein.
#
# --------------------------------------------------------------------------
#
# @file LkfDisplayPowerRegs.py
# @brief contains LkfDisplayPowerRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DYNAMIC_DC_STATE_ENABLE(Enum):
    DYNAMIC_DC_STATE_DISABLE = 0x0
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC5 = 0x1
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC6 = 0x2


class ENUM_DC9_ALLOW(Enum):
    DC9_ALLOW_DO_NOT_ALLOW = 0x0
    DC9_ALLOW_ALLOW = 0x1


class ENUM_MASK_POKE(Enum):
    MASK_POKE_UNMASK = 0x0
    MASK_POKE_MASK = 0x1


class ENUM_BLOCK_OUTBOUND_TRAFFIC(Enum):
    BLOCK_OUTBOUND_TRAFFIC_DO_NOT_BLOCK = 0x0
    BLOCK_OUTBOUND_TRAFFIC_BLOCK = 0x1


class ENUM_IN_CSR_FLOW(Enum):
    IN_CSR_FLOW_NOT_IN_CSR = 0x0
    IN_CSR_FLOW_IN_CSR = 0x1


class ENUM_DSI_PLLS_TURN_OFF_DISALLOWED(Enum):
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_ALLOWED = 0x0
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_DISALLOWED = 0x1


class ENUM_DISPLAY_DCCO_STATE_STATUS(Enum):
    DISPLAY_DCCO_STATE_STATUS_DMC_DCCO_EXIT_COMPLETED = 0x1


class ENUM_DISPLAY_CLOCK_OFF_ENABLE(Enum):
    DISPLAY_CLOCK_OFF_ENABLE_DCCO_IS_DISALLOWED = 0x0
    DISPLAY_CLOCK_OFF_ENABLE_DCCO_IS_ALLOWED = 0x1


class ENUM_MODE_SET_IN_PROGRESS(Enum):
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_NOT_GATED = 0x0
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_IS_GATED = 0x1


class OFFSET_DC_STATE_EN:
    DC_STATE_EN = 0x45504


class _DC_STATE_EN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DynamicDcStateEnable', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('Dc9Allow', ctypes.c_uint32, 1),
        ('MaskPoke', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('BlockOutboundTraffic', ctypes.c_uint32, 1),
        ('InCsrFlow', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 18),
        ('DsiPllsTurnOffDisallowed', ctypes.c_uint32, 1),
        ('DisplayDcCoStateStatus', ctypes.c_uint32, 1),
        ('DisplayClockOffEnable', ctypes.c_uint32, 1),
        ('ModeSetInProgress', ctypes.c_uint32, 1),
    ]


class REG_DC_STATE_EN(ctypes.Union):
    value = 0
    offset = 0

    DynamicDcStateEnable = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    Dc9Allow = 0  # bit 3 to 4
    MaskPoke = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    BlockOutboundTraffic = 0  # bit 8 to 9
    InCsrFlow = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 28
    DsiPllsTurnOffDisallowed = 0  # bit 28 to 29
    DisplayDcCoStateStatus = 0  # bit 29 to 30
    DisplayClockOffEnable = 0  # bit 30 to 31
    ModeSetInProgress = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_EN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_EN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

