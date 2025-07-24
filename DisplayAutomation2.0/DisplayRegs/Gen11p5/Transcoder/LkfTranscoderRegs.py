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
# @file LkfTranscoderRegs.py
# @brief contains LkfTranscoderRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PORT_SYNC_MODE_MASTER_SELECT(Enum):
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_A = 0x1
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_B = 0x2
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_C = 0x3
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_D = 0x4


class ENUM_PORT_SYNC_MODE_ENABLE(Enum):
    PORT_SYNC_MODE_DISABLE = 0x0
    PORT_SYNC_MODE_ENABLE = 0x1


class ENUM_DUAL_PIPE_SYNC_ENABLE(Enum):
    DUAL_PIPE_SYNC_DISABLED = 0x0  # Both transcoders are being driven by a single Pipe (Dual Link - Single Pipe
                                          # )
    DUAL_PIPE_SYNC_ENABLED = 0x1  # Each transcoder is being driven by a separate Pipe (Dual Link - Dual Pipe)


class ENUM_AUDIO_MUTE_OVERRIDE(Enum):
    AUDIO_MUTE_OVERRIDE_OVERRIDE_AND_RESET = 0x2  # Override audio mute bit to '0'.
    AUDIO_MUTE_OVERRIDE_OVERRIDE_AND_SET = 0x3  # Override audio mute bit to '1'.


class OFFSET_TRANS_DDI_FUNC_CTL2:
    TRANS_DDI_FUNC_CTL2_A = 0x60404
    TRANS_DDI_FUNC_CTL2_B = 0x61404
    TRANS_DDI_FUNC_CTL2_C = 0x62404
    TRANS_DDI_FUNC_CTL2_D = 0x63404
    TRANS_DDI_FUNC_CTL2_DSI0 = 0x6B404
    TRANS_DDI_FUNC_CTL2_DSI1 = 0x6BC04


class _TRANS_DDI_FUNC_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PortSyncModeMasterSelect', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 1),
        ('PortSyncModeEnable', ctypes.c_uint32, 1),
        ('DualPipeSyncEnable', ctypes.c_uint32, 1),
        ('AudioMuteOverride', ctypes.c_uint32, 2),
        ('Reserved8', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 20),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_TRANS_DDI_FUNC_CTL2(ctypes.Union):
    value = 0
    offset = 0

    PortSyncModeMasterSelect = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 4
    PortSyncModeEnable = 0  # bit 4 to 5
    DualPipeSyncEnable = 0  # bit 5 to 6
    AudioMuteOverride = 0  # bit 6 to 8
    Reserved8 = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_DDI_FUNC_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_DDI_FUNC_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

