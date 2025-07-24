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
# @file Gen14InterruptRegs.py
# @brief contains Gen14InterruptRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_GRAPHICS_MASTER_INTERRUPT:
    GFX_MSTR_INTR = 0x190010


class _GRAPHICS_MASTER_INTERRUPT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GtDw0', ctypes.c_uint32, 1),
        ('GtDw1', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 6),
        ('Reserved8', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 5),
        ('Display', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 9),
        ('Correctable_Error', ctypes.c_uint32, 1),
        ('Non_Fatal_Error', ctypes.c_uint32, 1),
        ('Fatal_Error', ctypes.c_uint32, 1),
        ('Gu_Misc', ctypes.c_uint32, 1),
        ('Pcu', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_GRAPHICS_MASTER_INTERRUPT(ctypes.Union):
    value = 0
    offset = 0

    GtDw0 = 0  # bit 0 to 1
    GtDw1 = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 8
    Reserved8 = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 16
    Display = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 26
    Correctable_Error = 0  # bit 26 to 27
    Non_Fatal_Error = 0  # bit 27 to 28
    Fatal_Error = 0  # bit 28 to 29
    Gu_Misc = 0  # bit 29 to 30
    Pcu = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GRAPHICS_MASTER_INTERRUPT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GRAPHICS_MASTER_INTERRUPT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAY_INTERRUPT_ENABLE(Enum):
    DISPLAY_INTERRUPT_DISABLE = 0x0
    DISPLAY_INTERRUPT_ENABLE = 0x1


class OFFSET_DISPLAY_INT_CTL:
    DISPLAY_INT_CTL = 0x44200


class _DISPLAY_INT_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 16),
        ('DePipeAInterruptsPending', ctypes.c_uint32, 1),
        ('DePipeBInterruptsPending', ctypes.c_uint32, 1),
        ('DePipeCInterruptsPending', ctypes.c_uint32, 1),
        ('DePipeDInterruptsPending', ctypes.c_uint32, 1),
        ('DePortInterruptsPending', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 1),
        ('DeMiscInterruptsPending', ctypes.c_uint32, 1),
        ('DePchInterruptsPending', ctypes.c_uint32, 1),
        ('AudioCodecInterruptsPending', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 5),
        ('DisplayInterruptEnable', ctypes.c_uint32, 1),
    ]


class REG_DISPLAY_INT_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 16
    DePipeAInterruptsPending = 0  # bit 16 to 17
    DePipeBInterruptsPending = 0  # bit 17 to 18
    DePipeCInterruptsPending = 0  # bit 18 to 19
    DePipeDInterruptsPending = 0  # bit 19 to 20
    DePortInterruptsPending = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 22
    DeMiscInterruptsPending = 0  # bit 22 to 23
    DePchInterruptsPending = 0  # bit 23 to 24
    AudioCodecInterruptsPending = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 31
    DisplayInterruptEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DISPLAY_INT_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DISPLAY_INT_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_ALT_STATUS(Enum):
    DP_ALT_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DP_ALT_STATUS_SHORT_PULSE_DETECTED = 0x1
    DP_ALT_STATUS_LONG_PULSE_DETECTED = 0x2
    DP_ALT_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DP_ALT_ENABLE(Enum):
    DP_ALT_DISABLE = 0x0
    DP_ALT_ENABLE = 0x1


class ENUM_TBT_STATUS(Enum):
    TBT_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    TBT_STATUS_SHORT_PULSE_DETECTED = 0x1
    TBT_STATUS_LONG_PULSE_DETECTED = 0x2
    TBT_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_TBT_ENABLE(Enum):
    TBT_DISABLE = 0x0
    TBT_ENABLE = 0x1


class OFFSET_PORT_HOTPLUG_CTL:
    PORT_HOTPLUG_CTL_USBC1 = 0x16F270
    PORT_HOTPLUG_CTL_USBC2 = 0x16F470
    PORT_HOTPLUG_CTL_USBC3 = 0x16F670
    PORT_HOTPLUG_CTL_USBC4 = 0x16F870


class _PORT_HOTPLUG_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DpAltStatus', ctypes.c_uint32, 2),
        ('DpAltEnable', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('TbtStatus', ctypes.c_uint32, 2),
        ('TbtEnable', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 25),
    ]


class REG_PORT_HOTPLUG_CTL(ctypes.Union):
    value = 0
    offset = 0

    DpAltStatus = 0  # bit 0 to 2
    DpAltEnable = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    TbtStatus = 0  # bit 4 to 6
    TbtEnable = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_HOTPLUG_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_HOTPLUG_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PICA_INTERRUPT_DEFINITION:
    PICAINTERRUPTDEFINITION_0 = 0x16FE50
    PICAINTERRUPTDEFINITION_1 = 0x16FE54
    PICAINTERRUPTDEFINITION_2 = 0x16FE58
    PICAINTERRUPTDEFINITION_3 = 0x16FE5C


class _PICA_INTERRUPT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TbtHotplugPort1', ctypes.c_uint32, 1),
        ('TbtHotplugPort2', ctypes.c_uint32, 1),
        ('TbtHotplugPort3', ctypes.c_uint32, 1),
        ('TbtHotplugPort4', ctypes.c_uint32, 1),
        ('Unused4', ctypes.c_uint32, 1),
        ('Unused5', ctypes.c_uint32, 1),
        ('Unused6', ctypes.c_uint32, 1),
        ('Unused7', ctypes.c_uint32, 1),
        ('AuxPort1', ctypes.c_uint32, 1),
        ('AuxPort2', ctypes.c_uint32, 1),
        ('AuxPort3', ctypes.c_uint32, 1),
        ('AuxPort4', ctypes.c_uint32, 1),
        ('Unused12', ctypes.c_uint32, 1),
        ('Unused13', ctypes.c_uint32, 1),
        ('Unused14', ctypes.c_uint32, 1),
        ('Unused15', ctypes.c_uint32, 1),
        ('DpAltHotplugPort1', ctypes.c_uint32, 1),
        ('DpAltHotplugPort2', ctypes.c_uint32, 1),
        ('DpAltHotplugPort3', ctypes.c_uint32, 1),
        ('DpAltHotplugPort4', ctypes.c_uint32, 1),
        ('Unused20', ctypes.c_uint32, 1),
        ('Unused21', ctypes.c_uint32, 1),
        ('Unused22', ctypes.c_uint32, 1),
        ('Unused23', ctypes.c_uint32, 1),
        ('Unused24', ctypes.c_uint32, 1),
        ('Unused25', ctypes.c_uint32, 1),
        ('Unused26', ctypes.c_uint32, 1),
        ('Unused27', ctypes.c_uint32, 1),
        ('Unused28', ctypes.c_uint32, 1),
        ('Unused29', ctypes.c_uint32, 1),
        ('Unused30', ctypes.c_uint32, 1),
        ('TypecMailbox', ctypes.c_uint32, 1),
    ]


class REG_PICA_INTERRUPT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    TbtHotplugPort1 = 0  # bit 0 to 1
    TbtHotplugPort2 = 0  # bit 1 to 2
    TbtHotplugPort3 = 0  # bit 2 to 3
    TbtHotplugPort4 = 0  # bit 3 to 4
    Unused4 = 0  # bit 4 to 5
    Unused5 = 0  # bit 5 to 6
    Unused6 = 0  # bit 6 to 7
    Unused7 = 0  # bit 7 to 8
    AuxPort1 = 0  # bit 8 to 9
    AuxPort2 = 0  # bit 9 to 10
    AuxPort3 = 0  # bit 10 to 11
    AuxPort4 = 0  # bit 11 to 12
    Unused12 = 0  # bit 12 to 13
    Unused13 = 0  # bit 13 to 14
    Unused14 = 0  # bit 14 to 15
    Unused15 = 0  # bit 15 to 16
    DpAltHotplugPort1 = 0  # bit 16 to 17
    DpAltHotplugPort2 = 0  # bit 17 to 18
    DpAltHotplugPort3 = 0  # bit 18 to 19
    DpAltHotplugPort4 = 0  # bit 19 to 20
    Unused20 = 0  # bit 20 to 21
    Unused21 = 0  # bit 21 to 22
    Unused22 = 0  # bit 22 to 23
    Unused23 = 0  # bit 23 to 24
    Unused24 = 0  # bit 24 to 25
    Unused25 = 0  # bit 25 to 26
    Unused26 = 0  # bit 26 to 27
    Unused27 = 0  # bit 27 to 28
    Unused28 = 0  # bit 28 to 29
    Unused29 = 0  # bit 29 to 30
    Unused30 = 0  # bit 30 to 31
    TypecMailbox = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_INTERRUPT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_INTERRUPT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DE_PIPE_INTERRUPT:
    DE_PIPE_INTERRUPT_A_0 = 0x44400
    DE_PIPE_INTERRUPT_A_1 = 0x44404
    DE_PIPE_INTERRUPT_A_2 = 0x44408
    DE_PIPE_INTERRUPT_A_3 = 0x4440C
    DE_PIPE_INTERRUPT_B_0 = 0x44410
    DE_PIPE_INTERRUPT_B_1 = 0x44414
    DE_PIPE_INTERRUPT_B_2 = 0x44418
    DE_PIPE_INTERRUPT_B_3 = 0x4441C
    DE_PIPE_INTERRUPT_C_0 = 0x44420
    DE_PIPE_INTERRUPT_C_1 = 0x44424
    DE_PIPE_INTERRUPT_C_2 = 0x44428
    DE_PIPE_INTERRUPT_C_3 = 0x4442C
    DE_PIPE_INTERRUPT_D_0 = 0x44430
    DE_PIPE_INTERRUPT_D_1 = 0x44434
    DE_PIPE_INTERRUPT_D_2 = 0x44438
    DE_PIPE_INTERRUPT_D_3 = 0x4443C


class _DE_PIPE_INTERRUPT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Vblank', ctypes.c_uint32, 1),
        ('Vsync', ctypes.c_uint32, 1),
        ('Scan_Line_Event', ctypes.c_uint32, 1),
        ('Plane1_Flip_Done', ctypes.c_uint32, 1),
        ('Plane2_Flip_Done', ctypes.c_uint32, 1),
        ('Plane3_Flip_Done', ctypes.c_uint32, 1),
        ('Plane4_Flip_Done', ctypes.c_uint32, 1),
        ('Plane1_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Plane2_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Plane3_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Plane4_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Cursor_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Dpst_Histogram_Event', ctypes.c_uint32, 1),
        ('Dsb_0_Interrupt', ctypes.c_uint32, 1),
        ('Dsb_1_Interrupt', ctypes.c_uint32, 1),
        ('Dsb_2_Interrupt', ctypes.c_uint32, 1),
        ('Plane5_Flip_Done', ctypes.c_uint32, 1),
        ('PipeDmcError', ctypes.c_uint32, 1),
        ('Plane_Ats_Fault_Status', ctypes.c_uint32, 1),
        ('VblankUnmodified', ctypes.c_uint32, 1),
        ('Plane5_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('PipeHardUnderrunInterrupt', ctypes.c_uint32, 1),
        ('PipeSoftUnderrunInterrupt', ctypes.c_uint32, 1),
        ('LaceFastAccessInterrupt', ctypes.c_uint32, 1),
        ('Pipedmc_Ats_Fault_Status', ctypes.c_uint32, 1),
        ('Pipedmc_Gtt_Fault_Status', ctypes.c_uint32, 1),
        ('Pipedmc_Interrupt', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Cdclk_Crc_Done', ctypes.c_uint32, 1),
        ('Cdclk_Crc_Error', ctypes.c_uint32, 1),
        ('VrrDoubleBufferUpdate', ctypes.c_uint32, 1),
        ('Underrun', ctypes.c_uint32, 1),
    ]


class REG_DE_PIPE_INTERRUPT(ctypes.Union):
    value = 0
    offset = 0

    Vblank = 0  # bit 0 to 1
    Vsync = 0  # bit 1 to 2
    Scan_Line_Event = 0  # bit 2 to 3
    Plane1_Flip_Done = 0  # bit 3 to 4
    Plane2_Flip_Done = 0  # bit 4 to 5
    Plane3_Flip_Done = 0  # bit 5 to 6
    Plane4_Flip_Done = 0  # bit 6 to 7
    Plane1_Gtt_Fault_Status = 0  # bit 7 to 8
    Plane2_Gtt_Fault_Status = 0  # bit 8 to 9
    Plane3_Gtt_Fault_Status = 0  # bit 9 to 10
    Plane4_Gtt_Fault_Status = 0  # bit 10 to 11
    Cursor_Gtt_Fault_Status = 0  # bit 11 to 12
    Dpst_Histogram_Event = 0  # bit 12 to 13
    Dsb_0_Interrupt = 0  # bit 13 to 14
    Dsb_1_Interrupt = 0  # bit 14 to 15
    Dsb_2_Interrupt = 0  # bit 15 to 16
    Plane5_Flip_Done = 0  # bit 16 to 17
    PipeDmcError = 0  # bit 17 to 18
    Plane_Ats_Fault_Status = 0  # bit 18 to 19
    VblankUnmodified = 0  # bit 19 to 20
    Plane5_Gtt_Fault_Status = 0  # bit 20 to 21
    PipeHardUnderrunInterrupt = 0  # bit 21 to 22
    PipeSoftUnderrunInterrupt = 0  # bit 22 to 23
    LaceFastAccessInterrupt = 0  # bit 23 to 24
    Pipedmc_Ats_Fault_Status = 0  # bit 24 to 25
    Pipedmc_Gtt_Fault_Status = 0  # bit 25 to 26
    Pipedmc_Interrupt = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 28
    Cdclk_Crc_Done = 0  # bit 28 to 29
    Cdclk_Crc_Error = 0  # bit 29 to 30
    VrrDoubleBufferUpdate = 0  # bit 30 to 31
    Underrun = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DE_PIPE_INTERRUPT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DE_PIPE_INTERRUPT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DE_PORT_INTERRUPT_DEFINITION:
    DE_PORT_INTERRUPT_0 = 0x44440
    DE_PORT_INTERRUPT_1 = 0x44444
    DE_PORT_INTERRUPT_2 = 0x44448
    DE_PORT_INTERRUPT_3 = 0x4444C


class _DE_PORT_INTERRUPT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxDdia', ctypes.c_uint32, 1),
        ('AuxDdib', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 5),
        ('Reserved8', ctypes.c_uint32, 6),
        ('CmtgVblank', ctypes.c_uint32, 1),
        ('CmtgDelayedVblank', ctypes.c_uint32, 1),
        ('CmtgVsync', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 4),
        ('Reserved21', ctypes.c_uint32, 2),
        ('Reserved23', ctypes.c_uint32, 2),
        ('Reserved25', ctypes.c_uint32, 5),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_DE_PORT_INTERRUPT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    AuxDdia = 0  # bit 0 to 1
    AuxDdib = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 8
    Reserved8 = 0  # bit 8 to 14
    CmtgVblank = 0  # bit 14 to 15
    CmtgDelayedVblank = 0  # bit 15 to 16
    CmtgVsync = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 21
    Reserved21 = 0  # bit 21 to 23
    Reserved23 = 0  # bit 23 to 25
    Reserved25 = 0  # bit 25 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DE_PORT_INTERRUPT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DE_PORT_INTERRUPT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DE_MISC_INTERRUPT_DEFINITION:
    DE_MISC_INTERRUPT_0 = 0x44460
    DE_MISC_INTERRUPT_1 = 0x44464
    DE_MISC_INTERRUPT_2 = 0x44468
    DE_MISC_INTERRUPT_3 = 0x4446C


class _DE_MISC_INTERRUPT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('SagvTimeoutInterrupt', ctypes.c_uint32, 1),
        ('PmDemandResponse', ctypes.c_uint32, 1),
        ('PmRequestReceived', ctypes.c_uint32, 1),
        ('PmResponseSent', ctypes.c_uint32, 1),
        ('DeWakeAsserted', ctypes.c_uint32, 1),
        ('DePokeAsserted', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 7),
        ('Reserved15', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 2),
        ('Wd1_Interrupts_Combined', ctypes.c_uint32, 1),
        ('Srd_Interrupts_Combined', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 3),
        ('Wd0_Interrupts_Combined', ctypes.c_uint32, 1),
        ('Dmc_Interrupt_Event', ctypes.c_uint32, 1),
        ('Dmc_Error', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 1),
        ('Pm_Dmd_Rsptimeout_Error', ctypes.c_uint32, 1),
        ('Pm_Dmd_Msg_Error', ctypes.c_uint32, 1),
        ('RegisterTimeout', ctypes.c_uint32, 1),
        ('Ecc_Double_Error', ctypes.c_uint32, 1),
        ('Poison', ctypes.c_uint32, 1),
    ]


class REG_DE_MISC_INTERRUPT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    SagvTimeoutInterrupt = 0  # bit 2 to 3
    PmDemandResponse = 0  # bit 3 to 4
    PmRequestReceived = 0  # bit 4 to 5
    PmResponseSent = 0  # bit 5 to 6
    DeWakeAsserted = 0  # bit 6 to 7
    DePokeAsserted = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 15
    Reserved15 = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 18
    Wd1_Interrupts_Combined = 0  # bit 18 to 19
    Srd_Interrupts_Combined = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 23
    Wd0_Interrupts_Combined = 0  # bit 23 to 24
    Dmc_Interrupt_Event = 0  # bit 24 to 25
    Dmc_Error = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 27
    Pm_Dmd_Rsptimeout_Error = 0  # bit 27 to 28
    Pm_Dmd_Msg_Error = 0  # bit 28 to 29
    RegisterTimeout = 0  # bit 29 to 30
    Ecc_Double_Error = 0  # bit 30 to 31
    Poison = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DE_MISC_INTERRUPT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DE_MISC_INTERRUPT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_AUDIO_CODEC_INTERRUPT_DEFINITION:
    AUD_INTERRUPT_0 = 0x44480
    AUD_INTERRUPT_1 = 0x44484
    AUD_INTERRUPT_2 = 0x44488
    AUD_INTERRUPT_3 = 0x4448C


class _AUDIO_CODEC_INTERRUPT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Audio_Mailbox_Write', ctypes.c_uint32, 1),
        ('Audio_Cp_Change_Transcoder_A', ctypes.c_uint32, 1),
        ('Audio_Cp_Request_Transcoder_A', ctypes.c_uint32, 1),
        ('Unused_Int_4_3', ctypes.c_uint32, 2),
        ('Audio_Cp_Change_Transcoder_B', ctypes.c_uint32, 1),
        ('Audio_Cp_Request_Transcoder_B', ctypes.c_uint32, 1),
        ('Audio_Cp_Change_Transcoder_C', ctypes.c_uint32, 1),
        ('Audio_Cp_Request_Transcoder_C', ctypes.c_uint32, 1),
        ('Audio_Cp_Change_Transcoder_D', ctypes.c_uint32, 1),
        ('Audio_Cp_Request_Transcoder_D', ctypes.c_uint32, 1),
        ('Audio_Power_State_Change_Transcoder_A', ctypes.c_uint32, 1),
        ('Audio_Frequency_Change_Transcoder_A', ctypes.c_uint32, 1),
        ('Audio_Frequency_Change_Transcoder_B', ctypes.c_uint32, 1),
        ('Audio_Frequency_Change_Transcoder_C', ctypes.c_uint32, 1),
        ('Audio_Frequency_Change_Transcoder_D', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Audio_Conv4_Power_State_Change', ctypes.c_uint32, 1),
        ('Audio_Conv3_Power_State_Change', ctypes.c_uint32, 1),
        ('Audio_Conv2_Power_State_Change', ctypes.c_uint32, 1),
        ('Audio_Conv1_Power_State_Change', ctypes.c_uint32, 1),
        ('Audio_Function_Group_Power_State_Change', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('Audio_Power_State_Change_Transcoder_B', ctypes.c_uint32, 1),
        ('Audio_Power_State_Change_Transcoder_C', ctypes.c_uint32, 1),
        ('Audio_Power_State_Change_Transcoder_D', ctypes.c_uint32, 1),
    ]


class REG_AUDIO_CODEC_INTERRUPT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    Audio_Mailbox_Write = 0  # bit 0 to 1
    Audio_Cp_Change_Transcoder_A = 0  # bit 1 to 2
    Audio_Cp_Request_Transcoder_A = 0  # bit 2 to 3
    Unused_Int_4_3 = 0  # bit 3 to 5
    Audio_Cp_Change_Transcoder_B = 0  # bit 5 to 6
    Audio_Cp_Request_Transcoder_B = 0  # bit 6 to 7
    Audio_Cp_Change_Transcoder_C = 0  # bit 7 to 8
    Audio_Cp_Request_Transcoder_C = 0  # bit 8 to 9
    Audio_Cp_Change_Transcoder_D = 0  # bit 9 to 10
    Audio_Cp_Request_Transcoder_D = 0  # bit 10 to 11
    Audio_Power_State_Change_Transcoder_A = 0  # bit 11 to 12
    Audio_Frequency_Change_Transcoder_A = 0  # bit 12 to 13
    Audio_Frequency_Change_Transcoder_B = 0  # bit 13 to 14
    Audio_Frequency_Change_Transcoder_C = 0  # bit 14 to 15
    Audio_Frequency_Change_Transcoder_D = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Audio_Conv4_Power_State_Change = 0  # bit 22 to 23
    Audio_Conv3_Power_State_Change = 0  # bit 23 to 24
    Audio_Conv2_Power_State_Change = 0  # bit 24 to 25
    Audio_Conv1_Power_State_Change = 0  # bit 25 to 26
    Audio_Function_Group_Power_State_Change = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    Audio_Power_State_Change_Transcoder_B = 0  # bit 29 to 30
    Audio_Power_State_Change_Transcoder_C = 0  # bit 30 to 31
    Audio_Power_State_Change_Transcoder_D = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUDIO_CODEC_INTERRUPT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUDIO_CODEC_INTERRUPT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PCU_INTERRUPT_DEFINITION:
    PCU_INTERRUPT_0 = 0x444E0
    PCU_INTERRUPT_1 = 0x444E4
    PCU_INTERRUPT_2 = 0x444E8
    PCU_INTERRUPT_3 = 0x444EC


class _PCU_INTERRUPT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare_0', ctypes.c_uint32, 1),
        ('Spare_1', ctypes.c_uint32, 1),
        ('Spare_2', ctypes.c_uint32, 1),
        ('Spare_3', ctypes.c_uint32, 1),
        ('Spare_4', ctypes.c_uint32, 1),
        ('Spare_5', ctypes.c_uint32, 1),
        ('Spare_6', ctypes.c_uint32, 1),
        ('Spare_7', ctypes.c_uint32, 1),
        ('Spare_8', ctypes.c_uint32, 1),
        ('Spare_9', ctypes.c_uint32, 1),
        ('Spare_10', ctypes.c_uint32, 1),
        ('Spare_11', ctypes.c_uint32, 1),
        ('Spare_12', ctypes.c_uint32, 1),
        ('Spare_13', ctypes.c_uint32, 1),
        ('Spare_14', ctypes.c_uint32, 1),
        ('Spare_15', ctypes.c_uint32, 1),
        ('Spare_16', ctypes.c_uint32, 1),
        ('Spare_17', ctypes.c_uint32, 1),
        ('Spare_18', ctypes.c_uint32, 1),
        ('Spare_19', ctypes.c_uint32, 1),
        ('Spare_20', ctypes.c_uint32, 1),
        ('Spare_21', ctypes.c_uint32, 1),
        ('Spare_22', ctypes.c_uint32, 1),
        ('Spare_23', ctypes.c_uint32, 1),
        ('Pcu_Thermal_Event', ctypes.c_uint32, 1),
        ('Pcu_Pcode2Driver_Mailbox_Event', ctypes.c_uint32, 1),
        ('Spare_26', ctypes.c_uint32, 1),
        ('Spare_27', ctypes.c_uint32, 1),
        ('Spare_28', ctypes.c_uint32, 1),
        ('DdicDc9Hpd', ctypes.c_uint32, 1),
        ('DdibDc9Hpd', ctypes.c_uint32, 1),
        ('DdiaDc9Hpd', ctypes.c_uint32, 1),
    ]


class REG_PCU_INTERRUPT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    Spare_0 = 0  # bit 0 to 1
    Spare_1 = 0  # bit 1 to 2
    Spare_2 = 0  # bit 2 to 3
    Spare_3 = 0  # bit 3 to 4
    Spare_4 = 0  # bit 4 to 5
    Spare_5 = 0  # bit 5 to 6
    Spare_6 = 0  # bit 6 to 7
    Spare_7 = 0  # bit 7 to 8
    Spare_8 = 0  # bit 8 to 9
    Spare_9 = 0  # bit 9 to 10
    Spare_10 = 0  # bit 10 to 11
    Spare_11 = 0  # bit 11 to 12
    Spare_12 = 0  # bit 12 to 13
    Spare_13 = 0  # bit 13 to 14
    Spare_14 = 0  # bit 14 to 15
    Spare_15 = 0  # bit 15 to 16
    Spare_16 = 0  # bit 16 to 17
    Spare_17 = 0  # bit 17 to 18
    Spare_18 = 0  # bit 18 to 19
    Spare_19 = 0  # bit 19 to 20
    Spare_20 = 0  # bit 20 to 21
    Spare_21 = 0  # bit 21 to 22
    Spare_22 = 0  # bit 22 to 23
    Spare_23 = 0  # bit 23 to 24
    Pcu_Thermal_Event = 0  # bit 24 to 25
    Pcu_Pcode2Driver_Mailbox_Event = 0  # bit 25 to 26
    Spare_26 = 0  # bit 26 to 27
    Spare_27 = 0  # bit 27 to 28
    Spare_28 = 0  # bit 28 to 29
    DdicDc9Hpd = 0  # bit 29 to 30
    DdibDc9Hpd = 0  # bit 30 to 31
    DdiaDc9Hpd = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PCU_INTERRUPT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PCU_INTERRUPT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PART_A_HISTOGRAM_LATE(Enum):
    PART_A_HISTOGRAM_LATE_NOT_LATE = 0x0
    PART_A_HISTOGRAM_LATE_LATE = 0x1


class ENUM_PART_A_HISTOGRAM_OVERLAP(Enum):
    PART_A_HISTOGRAM_OVERLAP_NOT_OVERLAP = 0x0
    PART_A_HISTOGRAM_OVERLAP_OVERLAP = 0x1


class ENUM_PART_A_IET_LATE(Enum):
    PART_A_IET_LATE_NOT_LATE = 0x0
    PART_A_IET_LATE_LATE = 0x1


class ENUM_PART_A_IET_OVERLAP(Enum):
    PART_A_IET_OVERLAP_NOT_LATE = 0x0
    PART_A_IET_OVERLAP_LATE = 0x1


class ENUM_PART_A_HISTOGRAM_READY(Enum):
    PART_A_HISTOGRAM_READY_NOT_READY = 0x0
    PART_A_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_A_LOAD_IE(Enum):
    PART_A_LOAD_IE_READY_DONE = 0x0
    PART_A_LOAD_IE_LOADING = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE(Enum):
    PART_A_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_A_HISTOGRAM_COPY_DONE_DONE = 0x1


class ENUM_PART_B_HISTOGRAM_LATE(Enum):
    PART_B_HISTOGRAM_LATE_NOT_LATE = 0x0
    PART_B_HISTOGRAM_LATE_LATE = 0x1


class ENUM_PART_B_HISTOGRAM_OVERLAP(Enum):
    PART_B_HISTOGRAM_OVERLAP_NOT_OVERLAP = 0x0
    PART_B_HISTOGRAM_OVERLAP_OVERLAP = 0x1


class ENUM_PART_B_IET_LATE(Enum):
    PART_B_IET_LATE_NOT_LATE = 0x0
    PART_B_IET_LATE_LATE = 0x1


class ENUM_PART_B_IET_OVERLAP(Enum):
    PART_B_IET_OVERLAP_NOT_LATE = 0x0
    PART_B_IET_OVERLAP_LATE = 0x1


class ENUM_PART_B_HISTOGRAM_READY(Enum):
    PART_B_HISTOGRAM_READY_NOT_READY = 0x0
    PART_B_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_B_LOAD_IE(Enum):
    PART_B_LOAD_IE_READY_DONE = 0x0
    PART_B_LOAD_IE_LOADING = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE(Enum):
    PART_B_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_B_HISTOGRAM_COPY_DONE_DONE = 0x1


class OFFSET_DPLC_FA_IIR:
    DPLC_FA_IIR_A = 0x49468
    DPLC_FA_IIR_B = 0x494E8


class _DPLC_FA_IIR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramLate', ctypes.c_uint32, 1),
        ('PartAHistogramOverlap', ctypes.c_uint32, 1),
        ('PartAIetLate', ctypes.c_uint32, 1),
        ('PartAIetOverlap', ctypes.c_uint32, 1),
        ('PartAHistogramReady', ctypes.c_uint32, 1),
        ('PartALoadIe', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 9),
        ('PartBHistogramLate', ctypes.c_uint32, 1),
        ('PartBHistogramOverlap', ctypes.c_uint32, 1),
        ('PartBIetLate', ctypes.c_uint32, 1),
        ('PartBIetOverlap', ctypes.c_uint32, 1),
        ('PartBHistogramReady', ctypes.c_uint32, 1),
        ('PartBLoadIe', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_DPLC_FA_IIR(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramLate = 0  # bit 0 to 1
    PartAHistogramOverlap = 0  # bit 1 to 2
    PartAIetLate = 0  # bit 2 to 3
    PartAIetOverlap = 0  # bit 3 to 4
    PartAHistogramReady = 0  # bit 4 to 5
    PartALoadIe = 0  # bit 5 to 6
    PartAHistogramCopyDone = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 16
    PartBHistogramLate = 0  # bit 16 to 17
    PartBHistogramOverlap = 0  # bit 17 to 18
    PartBIetLate = 0  # bit 18 to 19
    PartBIetOverlap = 0  # bit 19 to 20
    PartBHistogramReady = 0  # bit 20 to 21
    PartBLoadIe = 0  # bit 21 to 22
    PartBHistogramCopyDone = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_IIR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_IIR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PART_A_HISTOGRAM_LATE_MASK(Enum):
    PART_A_HISTOGRAM_LATE_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_LATE_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_OVERLAP_MASK(Enum):
    PART_A_HISTOGRAM_OVERLAP_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_A_IET_LATE_MASK(Enum):
    PART_A_IET_LATE_MASK_UNMASK = 0x0
    PART_A_IET_LATE_MASK_MASK = 0x1


class ENUM_PART_A_IET_OVERLAP_MASK(Enum):
    PART_A_IET_OVERLAP_MASK_UNMASK = 0x0
    PART_A_IET_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_READY_MASK(Enum):
    PART_A_HISTOGRAM_READY_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_READY_MASK_MASK = 0x1


class ENUM_PART_A_LOAD_IE_MASK(Enum):
    PART_A_LOAD_IE_MASK_UNMASK = 0x0
    PART_A_LOAD_IE_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE_MASK(Enum):
    PART_A_HISTOGRAM_COPY_DONE_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_COPY_DONE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_LATE_MASK(Enum):
    PART_B_HISTOGRAM_LATE_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_LATE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_OVERLAP_MASK(Enum):
    PART_B_HISTOGRAM_OVERLAP_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_B_IET_LATE_MASK(Enum):
    PART_B_IET_LATE_MASK_UNMASK = 0x0
    PART_B_IET_LATE_MASK_MASK = 0x1


class ENUM_PART_B_IET_OVERLAP_MASK(Enum):
    PART_B_IET_OVERLAP_MASK_UNMASK = 0x0
    PART_B_IET_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_READY_MASK(Enum):
    PART_B_HISTOGRAM_READY_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_READY_MASK_MASK = 0x1


class ENUM_PART_B_LOAD_IE_MASK(Enum):
    PART_B_LOAD_IE_MASK_UNMASK = 0x0
    PART_B_LOAD_IE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE_MASK(Enum):
    PART_B_HISTOGRAM_COPY_DONE_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_COPY_DONE_MASK_MASK = 0x1


class OFFSET_DPLC_FA_IMR:
    DPLC_FA_IMR_A = 0x49464
    DPLC_FA_IMR_B = 0x494E4


class _DPLC_FA_IMR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramLateMask', ctypes.c_uint32, 1),
        ('PartAHistogramOverlapMask', ctypes.c_uint32, 1),
        ('PartAIetLateMask', ctypes.c_uint32, 1),
        ('PartAIetOverlapMask', ctypes.c_uint32, 1),
        ('PartAHistogramReadyMask', ctypes.c_uint32, 1),
        ('PartALoadIeMask', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDoneMask', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 9),
        ('PartBHistogramLateMask', ctypes.c_uint32, 1),
        ('PartBHistogramOverlapMask', ctypes.c_uint32, 1),
        ('PartBIetLateMask', ctypes.c_uint32, 1),
        ('PartBIetOverlapMask', ctypes.c_uint32, 1),
        ('PartBHistogramReadyMask', ctypes.c_uint32, 1),
        ('PartBLoadIeMask', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDoneMask', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_DPLC_FA_IMR(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramLateMask = 0  # bit 0 to 1
    PartAHistogramOverlapMask = 0  # bit 1 to 2
    PartAIetLateMask = 0  # bit 2 to 3
    PartAIetOverlapMask = 0  # bit 3 to 4
    PartAHistogramReadyMask = 0  # bit 4 to 5
    PartALoadIeMask = 0  # bit 5 to 6
    PartAHistogramCopyDoneMask = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 16
    PartBHistogramLateMask = 0  # bit 16 to 17
    PartBHistogramOverlapMask = 0  # bit 17 to 18
    PartBIetLateMask = 0  # bit 18 to 19
    PartBIetOverlapMask = 0  # bit 19 to 20
    PartBHistogramReadyMask = 0  # bit 20 to 21
    PartBLoadIeMask = 0  # bit 21 to 22
    PartBHistogramCopyDoneMask = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_IMR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_IMR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_STATUS:
    PIPE_STATUS_A = 0x70058
    PIPE_STATUS_B = 0x71058
    PIPE_STATUS_C = 0x72058
    PIPE_STATUS_D = 0x73058


class _PIPE_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ValidBlockOverwritten', ctypes.c_uint32, 1),
        ('ValidBlockAtFramestart', ctypes.c_uint32, 1),
        ('NotUsed2', ctypes.c_uint32, 1),
        ('ICreditsPendingAtVblank', ctypes.c_uint32, 1),
        ('ACreditsPendingAtVblank', ctypes.c_uint32, 1),
        ('BCreditsPendingAtVblank', ctypes.c_uint32, 1),
        ('BwCreditsPendingAtVblank', ctypes.c_uint32, 1),
        ('PipeAtsPanic', ctypes.c_uint32, 1),
        ('NotUsed8', ctypes.c_uint32, 1),
        ('NotUsed9', ctypes.c_uint32, 1),
        ('NotUsed10', ctypes.c_uint32, 1),
        ('NotUsed11', ctypes.c_uint32, 1),
        ('NotUsed12', ctypes.c_uint32, 1),
        ('NotUsed13', ctypes.c_uint32, 1),
        ('NotUsed14', ctypes.c_uint32, 1),
        ('NotUsed15', ctypes.c_uint32, 1),
        ('NotUsed16', ctypes.c_uint32, 1),
        ('NotUsed17', ctypes.c_uint32, 1),
        ('NotUsed18', ctypes.c_uint32, 1),
        ('NotUsed19', ctypes.c_uint32, 1),
        ('NotUsed20', ctypes.c_uint32, 1),
        ('NotUsed21', ctypes.c_uint32, 1),
        ('NotUsed22', ctypes.c_uint32, 1),
        ('NotUsed23', ctypes.c_uint32, 1),
        ('NotUsed24', ctypes.c_uint32, 1),
        ('NotUsed25', ctypes.c_uint32, 1),
        ('PortUnderrun', ctypes.c_uint32, 1),
        ('PipeHardUnderrun', ctypes.c_uint32, 1),
        ('PipeSoftUnderrun', ctypes.c_uint32, 1),
        ('FrameStart', ctypes.c_uint32, 1),
        ('Vblank', ctypes.c_uint32, 1),
        ('Underrun', ctypes.c_uint32, 1),
    ]


class REG_PIPE_STATUS(ctypes.Union):
    value = 0
    offset = 0

    ValidBlockOverwritten = 0  # bit 0 to 1
    ValidBlockAtFramestart = 0  # bit 1 to 2
    NotUsed2 = 0  # bit 2 to 3
    ICreditsPendingAtVblank = 0  # bit 3 to 4
    ACreditsPendingAtVblank = 0  # bit 4 to 5
    BCreditsPendingAtVblank = 0  # bit 5 to 6
    BwCreditsPendingAtVblank = 0  # bit 6 to 7
    PipeAtsPanic = 0  # bit 7 to 8
    NotUsed8 = 0  # bit 8 to 9
    NotUsed9 = 0  # bit 9 to 10
    NotUsed10 = 0  # bit 10 to 11
    NotUsed11 = 0  # bit 11 to 12
    NotUsed12 = 0  # bit 12 to 13
    NotUsed13 = 0  # bit 13 to 14
    NotUsed14 = 0  # bit 14 to 15
    NotUsed15 = 0  # bit 15 to 16
    NotUsed16 = 0  # bit 16 to 17
    NotUsed17 = 0  # bit 17 to 18
    NotUsed18 = 0  # bit 18 to 19
    NotUsed19 = 0  # bit 19 to 20
    NotUsed20 = 0  # bit 20 to 21
    NotUsed21 = 0  # bit 21 to 22
    NotUsed22 = 0  # bit 22 to 23
    NotUsed23 = 0  # bit 23 to 24
    NotUsed24 = 0  # bit 24 to 25
    NotUsed25 = 0  # bit 25 to 26
    PortUnderrun = 0  # bit 26 to 27
    PipeHardUnderrun = 0  # bit 27 to 28
    PipeSoftUnderrun = 0  # bit 28 to 29
    FrameStart = 0  # bit 29 to 30
    Vblank = 0  # bit 30 to 31
    Underrun = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

