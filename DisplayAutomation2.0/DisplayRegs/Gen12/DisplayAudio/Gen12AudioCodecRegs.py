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
# @file Gen12AudioCodecRegs.py
# @brief contains Gen12AudioCodecRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PIXEL_CLOCK_HDMI(Enum):
    PIXEL_CLOCK_HDMI_25_2_1_001_MHZ = 0x0  # 25.2 / 1.001 MHz
    PIXEL_CLOCK_HDMI_25_2_MHZ = 0x1  # 25.2 MHz (Program this value for pixel clocks not listed in this field)
    PIXEL_CLOCK_HDMI_27_MHZ = 0x2  # 27 MHz
    PIXEL_CLOCK_HDMI_27_1_001_MHZ = 0x3  # 27  1.001 MHz
    PIXEL_CLOCK_HDMI_54_MHZ = 0x4  # 54 MHz
    PIXEL_CLOCK_HDMI_54_1_001_MHZ = 0x5  # 54  1.001 MHz
    PIXEL_CLOCK_HDMI_74_25_1_001_MHZ = 0x6  # 74.25 / 1.001 MHz
    PIXEL_CLOCK_HDMI_74_25_MHZ = 0x7  # 74.25 MHz
    PIXEL_CLOCK_HDMI_148_5_1_001_MHZ = 0x8  # 148.5 / 1.001 MHz
    PIXEL_CLOCK_HDMI_148_5_MHZ = 0x9  # 148.5 MHz
    PIXEL_CLOCK_HDMI_297_1_001_MHZ = 0xA  # 297 / 1.001 MHz
    PIXEL_CLOCK_HDMI_297_MHZ = 0xB  # 297 MHz
    PIXEL_CLOCK_HDMI_594_1_001_MHZ = 0xC  # 594 / 1.001 MHz
    PIXEL_CLOCK_HDMI_594_MHZ = 0xD  # 594 MHz


class ENUM_N_VALUE_INDEX(Enum):
    N_VALUE_INDEX_HDMI = 0x0  # N value read on bits 27:20 and 15:4 reflects HDMI N value. Bits 27:20 and 15:4 are prog
                              # rammable to any N value. Default h7FA6 when bit 28 is not set.
    N_VALUE_INDEX_DISPLAYPORT = 0x1  # N value read on bits 27:20 and 15:4 reflects DisplayPort N value. Set this bit t
                                     # o 1 before programming N value register. When this bit is set to 1, 27:20 and
                                     # 15:4 will reflect the current N value. Default is h8000 when bit 28 is not set.


class OFFSET_AUD_CONFIG:
    AUD_TCA_CONFIG = 0x65000
    AUD_TCB_CONFIG = 0x65100
    AUD_TCC_CONFIG = 0x65200
    AUD_TCD_CONFIG = 0x65300


class _AUD_CONFIG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 3),
        ('DisableNcts', ctypes.c_uint32, 1),
        ('LowerNValue', ctypes.c_uint32, 12),
        ('PixelClockHdmi', ctypes.c_uint32, 4),
        ('UpperNValue', ctypes.c_uint32, 8),
        ('NProgrammingEnable', ctypes.c_uint32, 1),
        ('NValueIndex', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_AUD_CONFIG(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    DisableNcts = 0  # bit 3 to 4
    LowerNValue = 0  # bit 4 to 16
    PixelClockHdmi = 0  # bit 16 to 20
    UpperNValue = 0  # bit 20 to 28
    NProgrammingEnable = 0  # bit 28 to 29
    NValueIndex = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_CONFIG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_CONFIG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISABLE_HBLANK_OVERFLOW_FIX_(Enum):
    DISABLE_HBLANK_OVERFLOW_FIX_HBLANK_OVERFLOW_FIX_ENABLED = 0x0  # When set to 0, the fix to recover from the audio 
                                                                    # overflow due to smaller Hblanks is enabled.
    DISABLE_HBLANK_OVERFLOW_FIX_HBLANK_OVERFLOW_FIX_DISABLED = 0x1  # When set to 1, the fix to recover from the audio
                                                                     #  overflow due to smaller Hblanks is disabled.


class OFFSET_AUD_CONFIG_2:
    AUD_TCA_CONFIG_2 = 0x65004
    AUD_TCB_CONFIG_2 = 0x65104
    AUD_TCC_CONFIG_2 = 0x65204
    AUD_TCD_CONFIG_2 = 0x65304


class _AUD_CONFIG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UpperBitsForMctsValue', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 4),
        ('UpperBitsForNValue', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 4),
        ('Dpspecversion', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 10),
        ('DisableHblankOverflowFix', ctypes.c_uint32, 1),
    ]


class REG_AUD_CONFIG_2(ctypes.Union):
    value = 0
    offset = 0

    UpperBitsForMctsValue = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 8
    UpperBitsForNValue = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 16
    Dpspecversion = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 31
    DisableHblankOverflowFix = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_CONFIG_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_CONFIG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PRO_ALLOWED(Enum):
    PRO_ALLOWED_CONSUMER = 0x0  # Consumer use only
    PRO_ALLOWED_PROFESSIONAL = 0x1  # Professional use allowed


class ENUM_SAMPLE_FABRICATION_EN_BIT(Enum):
    SAMPLE_FABRICATION_EN_BIT_DISABLE = 0x0  # Audio fabrication disabled
    SAMPLE_FABRICATION_EN_BIT_ENABLE = 0x1  # Audio fabrication enabled


class OFFSET_AUD_MISC_CTRL:
    AUD_C1_MISC_CTRL = 0x65010
    AUD_C2_MISC_CTRL = 0x65110
    AUD_C3_MISC_CTRL = 0x65210
    AUD_C4_MISC_CTRL = 0x65310


class _AUD_MISC_CTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('ProAllowed', ctypes.c_uint32, 1),
        ('SampleFabricationEnBit', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('OutputDelay', ctypes.c_uint32, 4),
        ('SamplePresentDisable', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_AUD_MISC_CTRL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    ProAllowed = 0  # bit 1 to 2
    SampleFabricationEnBit = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    OutputDelay = 0  # bit 4 to 8
    SamplePresentDisable = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_MISC_CTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_MISC_CTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ELD_VALIDA(Enum):
    ELD_VALIDA_INVALID = 0x0  # ELD data invalid (default, when writing ELD data, set 0 by software)
    ELD_VALIDA_VALID = 0x1  # ELD data valid (Set by video software only)


class ENUM_CP_READYA(Enum):
    CP_READYA_NOT_READY = 0x0  # CP request pending or not ready to receive requests
    CP_READYA_READY = 0x1  # CP request ready


class ENUM_AUDIO_OUTPUT_ENABLEA(Enum):
    AUDIO_OUTPUT_ENABLEA_DISABLE = 0x0  # No audio output
    AUDIO_OUTPUT_ENABLEA_ENABLE = 0x1  # Audio is enabled


class ENUM_AUDIO_INACTIVEA(Enum):
    AUDIO_INACTIVEA_DISABLE = 0x0  # Device is active for streaming audio data
    AUDIO_INACTIVEA_ENABLE = 0x1  # Device is connected but not active


class ENUM_ELD_VALIDB(Enum):
    ELD_VALIDB_INVALID = 0x0  # ELD data invalid (default, when writing ELD data, set 0 by software)
    ELD_VALIDB_VALID = 0x1  # ELD data valid (Set by video software only)


class ENUM_CP_READYB(Enum):
    CP_READYB_NOT_READY = 0x0  # CP request pending or not ready to receive requests
    CP_READYB_READY = 0x1  # CP request ready


class ENUM_AUDIO_OUTPUT_ENABLEB(Enum):
    AUDIO_OUTPUT_ENABLEB_DISABLE = 0x0  # No audio output
    AUDIO_OUTPUT_ENABLEB_ENABLE = 0x1  # Audio is enabled


class ENUM_AUDIO_INACTIVEB(Enum):
    AUDIO_INACTIVEB_DISABLE = 0x0  # Device is active for streaming audio data
    AUDIO_INACTIVEB_ENABLE = 0x1  # Device is connected but not active


class ENUM_ELD_VALIDC(Enum):
    ELD_VALIDC_INVALID = 0x0  # ELD data invalid (default, when writing ELD data, set 0 by software)
    ELD_VALIDC_VALID = 0x1  # ELD data valid (Set by video software only)


class ENUM_CP_READYC(Enum):
    CP_READYC_PENDING_OR_NOT_READY = 0x0  # CP request pending or not ready to receive requests
    CP_READYC_READY = 0x1  # CP request ready


class ENUM_AUDIO_OUTPUT_ENABLEC(Enum):
    AUDIO_OUTPUT_ENABLEC_DISABLE = 0x0  # No Audio output
    AUDIO_OUTPUT_ENABLEC_VALID = 0x1  # Audio is enabled


class ENUM_AUDIO_INACTIVEC(Enum):
    AUDIO_INACTIVEC_DISABLE = 0x0  # Device is active for streaming audio data
    AUDIO_INACTIVEC_ENABLE = 0x1  # Device is connected but not active


class ENUM_ELD_VALIDD(Enum):
    ELD_VALIDD_INVALID = 0x0  # ELD data invalid (default, when writing ELD data, set 0 by software)
    ELD_VALIDD_VALID = 0x1  # ELD data valid (Set by video software only)


class ENUM_CP_READYD(Enum):
    CP_READYD_PENDING_OR_NOT_READY = 0x0  # CP request pending or not ready to receive requests.
    CP_READYD_READY = 0x1  # CP request ready


class ENUM_AUDIO_OUTPUT_ENABLED(Enum):
    AUDIO_OUTPUT_ENABLED_DISABLE = 0x0  # No Audio output
    AUDIO_OUTPUT_ENABLED_VALID = 0x1  # Audio is enabled


class ENUM_AUDIO_INACTIVED(Enum):
    AUDIO_INACTIVED_DISABLE = 0x0  # Device is active for streaming audio data
    AUDIO_INACTIVED_ENABLE = 0x1  # Device is connected but not active


class OFFSET_AUD_PIN_ELD_CP_VLD:
    AUD_PIN_ELD_CP_VLD = 0x650C0


class _AUD_PIN_ELD_CP_VLD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EldValida', ctypes.c_uint32, 1),
        ('CpReadya', ctypes.c_uint32, 1),
        ('AudioOutputEnablea', ctypes.c_uint32, 1),
        ('AudioInactivea', ctypes.c_uint32, 1),
        ('EldValidb', ctypes.c_uint32, 1),
        ('CpReadyb', ctypes.c_uint32, 1),
        ('AudioOutputEnableb', ctypes.c_uint32, 1),
        ('AudioInactiveb', ctypes.c_uint32, 1),
        ('EldValidc', ctypes.c_uint32, 1),
        ('CpReadyc', ctypes.c_uint32, 1),
        ('AudioOutputEnablec', ctypes.c_uint32, 1),
        ('AudioInactivec', ctypes.c_uint32, 1),
        ('EldValidd', ctypes.c_uint32, 1),
        ('CpReadyd', ctypes.c_uint32, 1),
        ('AudioOutputEnabled', ctypes.c_uint32, 1),
        ('AudioInactived', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_AUD_PIN_ELD_CP_VLD(ctypes.Union):
    value = 0
    offset = 0

    EldValida = 0  # bit 0 to 1
    CpReadya = 0  # bit 1 to 2
    AudioOutputEnablea = 0  # bit 2 to 3
    AudioInactivea = 0  # bit 3 to 4
    EldValidb = 0  # bit 4 to 5
    CpReadyb = 0  # bit 5 to 6
    AudioOutputEnableb = 0  # bit 6 to 7
    AudioInactiveb = 0  # bit 7 to 8
    EldValidc = 0  # bit 8 to 9
    CpReadyc = 0  # bit 9 to 10
    AudioOutputEnablec = 0  # bit 10 to 11
    AudioInactivec = 0  # bit 11 to 12
    EldValidd = 0  # bit 12 to 13
    CpReadyd = 0  # bit 13 to 14
    AudioOutputEnabled = 0  # bit 14 to 15
    AudioInactived = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_PIN_ELD_CP_VLD),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_PIN_ELD_CP_VLD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ENABLE_MMIO_PROGRAMMING(Enum):
    ENABLE_MMIO_PROGRAMMING_HDAUDIO = 0x0  # Programming through HDAudio Azalia
    ENABLE_MMIO_PROGRAMMING_MMIO_PIO = 0x1  # Programming through MMIO PIO Debug registers. Chicken bit 0 needs to be s
                                            # et when link is off to use the back door mechanism. Back door programming
                                            # needs the frame sync if the chicken bit is not set. And when link is
                                            # off/sleep, the frame sync is not generated (when bit 14 is 1, it means
                                            # link is in sleep state). Chicken bit 0 can be used to overwrite and use
                                            # back door for verb programming.


class ENUM_EPSS_DISABLE(Enum):
    EPSS_ENABLE = 0x0  # Allow audio EPSS.
    EPSS_DISABLE = 0x1  # Disable audio EPSS.


class ENUM_FABRICATION_32_44_DISABLE(Enum):
    FABRICATION_32_44_ENABLE = 0x0  # Allow sample fabrication for 32 or 44 KHz (non-48).
    FABRICATION_32_44_DISABLE = 0x1  # Disable sample fabrication for 32 or 44 KHz (non-48).


class ENUM_PATTERN_GEN_2CH_EN(Enum):
    PATTERN_GEN_2CH_EN_DISABLE = 0x0  # Disable 2 channel pattern generator.
    PATTERN_GEN_2CH_EN_ENABLE = 0x1  # Enable 2 channel pattern generator.


class ENUM_PATTERN_GEN_8CH_EN(Enum):
    PATTERN_GEN_8CH_EN_DISABLE = 0x0  # Disable 8 channel pattern generator.
    PATTERN_GEN_8CH_EN_ENABLE = 0x1  # Enable 8 channel pattern generator.


class ENUM_DISABLE_TIMESTAMP_FIX_FOR_DPHBR(Enum):
    DISABLE_TIMESTAMP_FIX_FOR_DPHBR_ENABLE = 0x0  # Enable Timestamps for DP HBR.
    DISABLE_TIMESTAMP_FIX_FOR_DPHBR_DISABLE = 0x1  # Disable Timestamps for DP HBR.


class ENUM_DISABLE_TIMESTAMP_DELTA_ERROR_FOR_32_44_KHZ(Enum):
    DISABLE_TIMESTAMP_DELTA_ERROR_FOR_32_44_KHZ_ENABLE = 0x0  # Enable Timestamp Delta Error for 32 or 44 KHz.
    DISABLE_TIMESTAMP_DELTA_ERROR_FOR_32_44_KHZ_DISABLE = 0x1  # Disable Timestamp Delta Error for 32/44 KHz.


class ENUM_DISABLE_PRESENCE_DETECT_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED(Enum):
    DISABLE_PRESENCE_DETECT_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_ENABLE = 0x0  # Enable Presence Detect Pulse Transi
                                                                                  # tion When unsol is Disabled.
    DISABLE_PRESENCE_DETECT_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_DISABLE = 0x1  # Disable Presence Detect Pulse Tran
                                                                                   # sition When unsol is Disabled.


class ENUM_DISABLE_ELD_VALID_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED(Enum):
    DISABLE_ELD_VALID_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_ENABLE = 0x0  # Enable ELD Valid Pulse Transition When un
                                                                            # sol is Disabled.
    DISABLE_ELD_VALID_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_DISABLE = 0x1  # Disable ELD Valid Pulse Transition When 
                                                                             # unsol is Disabled.


class ENUM_BLOCK_AUDIO_DATA_FROM_REACHING_THE_PORT(Enum):
    BLOCK_AUDIO_DATA_FROM_REACHING_THE_PORT_ENABLE = 0x0  # Allow audio data to reach the port.
    BLOCK_AUDIO_DATA_FROM_REACHING_THE_PORT_DISABLE = 0x1  # Block audio data from reaching the port.


class ENUM_SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACWD_UNIT(Enum):
    SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACWD_UNIT_DISABLE = 0x0  # Sample Present bit in the each channel is set to 
                                                                    # 0 for non mapped channels in layout 1 mode.
    SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACWD_UNIT_ENABLE = 0x1  # Sample Present bit in the each channel is set to 1
                                                                   #  for non mapped channels in layout 1 mode.


class ENUM_CODEC_SLEEP_STATE(Enum):
    CODEC_SLEEP_STATE_SLEEP_STATE = 0x1  # When set the Codec is in sleep state.
    CODEC_SLEEP_STATE_ACTIVE_STATE = 0x0  # If it is zero, codec is not in sleep state. The codec may be transitioning 
                                          # to Active state. It might several hundred micro seconds to go to active
                                          # state depending on when Audio controller sends the frame syncs to bring the
                                          # codec to active state (establish the link).


class ENUM_SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT(Enum):
    SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT_DISABLE = 0x0  # Sample Present bit in the each channel is set to 
                                                                    # 0 for non mapped channels in layout 1 mode.
    SAMPLE_PRESENT_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT_ENABLE = 0x1  # Sample Present in the each channel is set to 1 for
                                                                   #  non mapped channels in layout 1 mode.


class ENUM_ECC_OVERWRITE_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT(Enum):
    ECC_OVERWRITE_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT_DISABLE = 0x0  # ECC bits in the each channel is set to 0 for non m
                                                                   # apped channels in layout 1 mode.
    ECC_OVERWRITE_ENABLE_CHICKEN_BIT_FOR_DACBE_UNIT_ENABLE = 0x1  # ECC bits in the each channel is set to 3Bh for non 
                                                                  # mapped channels in layout 1 mode.


class OFFSET_AUD_CHICKENBIT_REG:
    AUD_CHICKENBIT_REG = 0x65F10


class _AUD_CHICKENBIT_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EnableMmioProgramming', ctypes.c_uint32, 1),
        ('AudioTimestampTestMode', ctypes.c_uint32, 1),
        ('EpssDisable', ctypes.c_uint32, 1),
        ('Fabrication3244Disable', ctypes.c_uint32, 1),
        ('PatternGen2ChEn', ctypes.c_uint32, 1),
        ('PatternGen8ChEn', ctypes.c_uint32, 1),
        ('DisableTimestampFixForDphbr', ctypes.c_uint32, 1),
        ('DisableTimestampDeltaErrorFor32_44Khz', ctypes.c_uint32, 1),
        ('DisablePresenceDetectPulseTransitionWhenUnsolIsDisabled', ctypes.c_uint32, 1),
        ('DisableEldValidPulseTransitionWhenUnsolIsDisabled', ctypes.c_uint32, 1),
        ('BlockAudioDataFromReachingThePort', ctypes.c_uint32, 1),
        ('ChickenBitsForDacwdUnit', ctypes.c_uint32, 2),
        ('SamplePresentEnableChickenBitForDacwdUnit', ctypes.c_uint32, 1),
        ('CodecSleepState', ctypes.c_uint32, 1),
        ('CodecWakeOverwriteToDacfeunit', ctypes.c_uint32, 1),
        ('DpComplianceFixDisableForDacbeUnit', ctypes.c_uint32, 1),
        ('ChickenBitsForDacbeUnit', ctypes.c_uint32, 1),
        ('DisableDacfeProtocolFixForDataFlitErrorInTheEndOfFrame', ctypes.c_uint32, 1),
        ('Dp1_2DeviceIndexFixDisable', ctypes.c_uint32, 1),
        ('Enable20BitSupportForSampleRate', ctypes.c_uint32, 1),
        ('DisableBclkFrameSyncFixOnBclkCounter', ctypes.c_uint32, 1),
        ('SamplePresentEnableChickenBitForDacbeUnit', ctypes.c_uint32, 1),
        ('EccOverwriteEnableChickenBitForDacbeUnit', ctypes.c_uint32, 1),
        ('DisableTheConvSampleFifoFix', ctypes.c_uint32, 1),
        ('ChickenBits25ForDacfpUnit', ctypes.c_uint32, 1),
        ('ChickenBits26ForDacfpUnit', ctypes.c_uint32, 1),
        ('ChickenBits29To27ForDacfpUnit', ctypes.c_uint32, 3),
        ('VanillaBitEnableForThreeWidgets', ctypes.c_uint32, 1),
        ('VanillaBitEnableForDp1_2', ctypes.c_uint32, 1),
    ]


class REG_AUD_CHICKENBIT_REG(ctypes.Union):
    value = 0
    offset = 0

    EnableMmioProgramming = 0  # bit 0 to 1
    AudioTimestampTestMode = 0  # bit 1 to 2
    EpssDisable = 0  # bit 2 to 3
    Fabrication3244Disable = 0  # bit 3 to 4
    PatternGen2ChEn = 0  # bit 4 to 5
    PatternGen8ChEn = 0  # bit 5 to 6
    DisableTimestampFixForDphbr = 0  # bit 6 to 7
    DisableTimestampDeltaErrorFor32_44Khz = 0  # bit 7 to 8
    DisablePresenceDetectPulseTransitionWhenUnsolIsDisabled = 0  # bit 8 to 9
    DisableEldValidPulseTransitionWhenUnsolIsDisabled = 0  # bit 9 to 10
    BlockAudioDataFromReachingThePort = 0  # bit 10 to 11
    ChickenBitsForDacwdUnit = 0  # bit 11 to 13
    SamplePresentEnableChickenBitForDacwdUnit = 0  # bit 13 to 14
    CodecSleepState = 0  # bit 14 to 15
    CodecWakeOverwriteToDacfeunit = 0  # bit 15 to 16
    DpComplianceFixDisableForDacbeUnit = 0  # bit 16 to 17
    ChickenBitsForDacbeUnit = 0  # bit 17 to 18
    DisableDacfeProtocolFixForDataFlitErrorInTheEndOfFrame = 0  # bit 18 to 19
    Dp1_2DeviceIndexFixDisable = 0  # bit 19 to 20
    Enable20BitSupportForSampleRate = 0  # bit 20 to 21
    DisableBclkFrameSyncFixOnBclkCounter = 0  # bit 21 to 22
    SamplePresentEnableChickenBitForDacbeUnit = 0  # bit 22 to 23
    EccOverwriteEnableChickenBitForDacbeUnit = 0  # bit 23 to 24
    DisableTheConvSampleFifoFix = 0  # bit 24 to 25
    ChickenBits25ForDacfpUnit = 0  # bit 25 to 26
    ChickenBits26ForDacfpUnit = 0  # bit 26 to 27
    ChickenBits29To27ForDacfpUnit = 0  # bit 27 to 30
    VanillaBitEnableForThreeWidgets = 0  # bit 30 to 31
    VanillaBitEnableForDp1_2 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_CHICKENBIT_REG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_CHICKENBIT_REG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ENABLE_VARIABLE_REFRESH_RATE_COUNTER(Enum):
    ENABLE_VARIABLE_REFRESH_RATE_COUNTER_DISABLE = 0x0  # Variable Refresh Rate Counter is not taken into consideration
                                                        #  when sending the timestamps and Audio Info frames packets.
    ENABLE_VARIABLE_REFRESH_RATE_COUNTER_ENABLE = 0x1  # Variable Refresh Rate Counter is taken into consideration when
                                                       #  sending the timestamps and Audio Info frames packets.


class ENUM_ENABLE_RESPONSE_TO_INVALID_VERBS(Enum):
    ENABLE_RESPONSE_TO_INVALID_VERBS_DISABLE = 0x0  # No responses to the invalid verbs.
    ENABLE_RESPONSE_TO_INVALID_VERBS_ENABLE = 0x1  # Enable responses to the invalid verbs as per the HDA spec. Added a
                                                   # s part of addition of this new chicken bit register.


class ENUM_DISABLE_SYNC_COUNT_ERROR_GENERATION_(Enum):
    DISABLE_SYNC_COUNT_ERROR_GENERATION_ENABLED = 0x0  # Sync Count error generation is enabled
    DISABLE_SYNC_COUNT_ERROR_GENERATION_DISABLED = 0x1  # Sync Count error generation is disabled.


class ENUM_DISABLE_CODEC_WAKE_EVENT_TO_CONTROLLER_(Enum):
    DISABLE_CODEC_WAKE_EVENT_TO_CONTROLLER_ENABLED = 0x0  # Enable codec wake event to the controller
    DISABLE_CODEC_WAKE_EVENT_TO_CONTROLLER_DISABLED = 0x1  # Disable codec wake event to the controller.


class ENUM_PIPEA_STICKY_BIT_FOR_VRR_DEBUG_(Enum):
    PIPEA_STICKY_BIT_FOR_VRR_DEBUG_DISABLE = 0x0  # Timestamps not sent for VRR
    PIPEA_STICKY_BIT_FOR_VRR_DEBUG_TIME_STAMPS_SENT = 0x1  # Time stamps sent with VRR enabled. SW needs to clear if n
                                                            # eeded to check again.


class ENUM_PIPEB_STICKY_BIT_FOR_VRR_DEBUG_(Enum):
    PIPEB_STICKY_BIT_FOR_VRR_DEBUG_DISABLE = 0x0  # Timestamps not sent for VRR
    PIPEB_STICKY_BIT_FOR_VRR_DEBUG_TIME_STAMPS_SENT = 0x1  # Time stamps sent with VRR enabled. SW needs to clear if n
                                                            # eeded to check again.


class ENUM_PIPEC_STICKY_BIT_FOR_VRR_DEBUG_(Enum):
    PIPEC_STICKY_BIT_FOR_VRR_DEBUG_DISABLE = 0x0  # Timestamps not sent for VRR
    PIPEC_STICKY_BIT_FOR_VRR_DEBUG_TIME_STAMPS_SENT = 0x1  # Time stamps sent with VRR enabled. SW needs to clear if n
                                                            # eeded to check again.


class ENUM_PIPED_STICKY_BIT_FOR_VRR_DEBUG_(Enum):
    PIPED_STICKY_BIT_FOR_VRR_DEBUG_DISABLE = 0x0  # Timestamps not sent for VRR
    PIPED_STICKY_BIT_FOR_VRR_DEBUG_TIME_STAMPS_SENT = 0x1  # Time stamps sent with VRR enabled. SW needs to clear if n
                                                            # eeded to check again.


class ENUM_DISABLE_8T_MODE_FIX(Enum):
    DISABLE_8T_MODE_FIX_ENABLE = 0x0  # 8T mode fix available for any delays in the routing.
    DISABLE_8T_MODE_FIX_DISABLE = 0x1  # 8T mode delay fix is disabled. 8T mode can be used only if the routing delays 
                                       # are greater than 20ns between Display IO and display core IP.


class ENUM_PORT_SELECT(Enum):
    PORT_SELECT_DDIA = 0x0  # Port DDIA is selected. Valid only in single pin mode.
    PORT_SELECT_DDIB = 0x1  # Port DDIB is selected. Valid only in single pin mode.
    PORT_SELECT_DDIC = 0x2  # Port DDIC is selected. Valid only in single pin mode.
    PORT_SELECT_USBC1 = 0x3  # Port USBC1 is selected. Valid only in single pin mode.
    PORT_SELECT_USBC2 = 0x4  # Port USBC2 is selected. Valid only in single pin mode.
    PORT_SELECT_USBC3 = 0x5  # Port USBC3 is selected. Valid only in single pin mode.
    PORT_SELECT_USBC4 = 0x6  # Port USBC4 is selected. Valid only in single pin mode.
    PORT_SELECT_USBC5 = 0x7  # Port USBC5 is selected. Valid only in single pin mode.
    PORT_SELECT_USBC6 = 0x8  # Port USBC6 is selected. Valid only in single pin mode.


class OFFSET_AUD_CHICKENBIT_REG_2:
    AUD_CHICKENBIT_REG_2 = 0x65F0C


class _AUD_CHICKENBIT_REG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EnableVariableRefreshRateCounter', ctypes.c_uint32, 1),
        ('EnableResponseToInvalidVerbs', ctypes.c_uint32, 1),
        ('CodecSleepStateMachineStatus', ctypes.c_uint32, 3),
        ('LinkStatus', ctypes.c_uint32, 1),
        ('DisableSyncCountErrorGeneration', ctypes.c_uint32, 1),
        ('DisableCodecWakeEventToController', ctypes.c_uint32, 1),
        ('DacfpExtraChickens', ctypes.c_uint32, 8),
        ('PipeaStickyBitForVrrDebug', ctypes.c_uint32, 1),
        ('PipebStickyBitForVrrDebug', ctypes.c_uint32, 1),
        ('PipecStickyBitForVrrDebug', ctypes.c_uint32, 1),
        ('PipedStickyBitForVrrDebug', ctypes.c_uint32, 1),
        ('DacbeExtraChickens', ctypes.c_uint32, 4),
        ('Disable8TModeFix', ctypes.c_uint32, 1),
        ('DacfeExtraChickens', ctypes.c_uint32, 3),
        ('PortSelect', ctypes.c_uint32, 4),
    ]


class REG_AUD_CHICKENBIT_REG_2(ctypes.Union):
    value = 0
    offset = 0

    EnableVariableRefreshRateCounter = 0  # bit 0 to 1
    EnableResponseToInvalidVerbs = 0  # bit 1 to 2
    CodecSleepStateMachineStatus = 0  # bit 2 to 5
    LinkStatus = 0  # bit 5 to 6
    DisableSyncCountErrorGeneration = 0  # bit 6 to 7
    DisableCodecWakeEventToController = 0  # bit 7 to 8
    DacfpExtraChickens = 0  # bit 8 to 16
    PipeaStickyBitForVrrDebug = 0  # bit 16 to 17
    PipebStickyBitForVrrDebug = 0  # bit 17 to 18
    PipecStickyBitForVrrDebug = 0  # bit 18 to 19
    PipedStickyBitForVrrDebug = 0  # bit 19 to 20
    DacbeExtraChickens = 0  # bit 20 to 24
    Disable8TModeFix = 0  # bit 24 to 25
    DacfeExtraChickens = 0  # bit 25 to 28
    PortSelect = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_CHICKENBIT_REG_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_CHICKENBIT_REG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_AUD_EDID_DATA:
    AUD_TCA_EDID_DATA = 0x65050
    AUD_TCB_EDID_DATA = 0x65150
    AUD_TCC_EDID_DATA = 0x65250
    AUD_TCD_EDID_DATA = 0x65350


class _AUD_EDID_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EdidDataBlock', ctypes.c_uint32, 32),
    ]


class REG_AUD_EDID_DATA(ctypes.Union):
    value = 0
    offset = 0

    EdidDataBlock = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_EDID_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_EDID_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DIP_TRANSMISSION_FREQUENCY(Enum):
    DIP_TRANSMISSION_FREQUENCY_DISABLE = 0x0  # Disabled
    DIP_TRANSMISSION_FREQUENCY_SEND_ONCE = 0x2  # Send Once
    DIP_TRANSMISSION_FREQUENCY_BEST_EFFORT = 0x3  # Best effort (Send at least every other vsync)


class ENUM_DIP_BUFFER_INDEX(Enum):
    DIP_BUFFER_INDEX_AUDIO = 0x0  # Audio DIP (31 bytes of address space, 31 bytes of data)
    DIP_BUFFER_INDEX_GEN_1 = 0x1  # Generic 1 (ACP) Data Island Packet (31 bytes of address space, 31 bytes of data)
    DIP_BUFFER_INDEX_GEN_2 = 0x2  # Generic 2 (ISRC1) Data Island Packet (31 bytes of address space, 31 bytes of data)
    DIP_BUFFER_INDEX_GEN_3 = 0x3  # Generic 3 (ISRC2) Data Island Packet (31 bytes of address space, 31 bytes of data)


class ENUM_DIP_TYPE_ENABLE_STATUS(Enum):
    DIP_TYPE_ENABLE_STATUS_DIP_DISABLE = 0x0  # Audio DIP disabled
    DIP_TYPE_ENABLE_STATUS_DIP_ENABLE = 0x0  # Audio DIP enabled
    DIP_TYPE_ENABLE_STATUS_ACP_DISABLE = 0x0  # Generic 1 (ACP) DIP disabled
    DIP_TYPE_ENABLE_STATUS_ACP_ENABLE = 0x0  # Generic 1 (ACP) DIP enabled
    DIP_TYPE_ENABLE_STATUS_GENERIC_2_DISABLE = 0x0  # Generic 2 DIP disabled
    DIP_TYPE_ENABLE_STATUS_GENERIC_2_ENABLE = 0x0  # Generic 2 DIP enabled, can be used by ISRC1 or ISRC2


class ENUM_DIP_PORT_SELECT(Enum):
    DIP_PORT_SELECT_DIGITAL_PORT_B = 0x1  # Digital Port B
    DIP_PORT_SELECT_DIGITAL_PORT_C = 0x2  # Digital Port C
    DIP_PORT_SELECT_USBC1 = 0x3  # USBC1
    DIP_PORT_SELECT_USBC2 = 0x4  # USBC2
    DIP_PORT_SELECT_USBC3 = 0x5  # USBC3
    DIP_PORT_SELECT_USBC4 = 0x6  # USBC4
    DIP_PORT_SELECT_USBC5 = 0x7  # USBC5
    DIP_PORT_SELECT_USBC6 = 0x8  # USBC6


class OFFSET_AUD_DIP_ELD_CTRL_ST:
    AUD_TCA_DIP_ELD_CTRL_ST = 0x650B4
    AUD_TCB_DIP_ELD_CTRL_ST = 0x651B4
    AUD_TCC_DIP_ELD_CTRL_ST = 0x652B4
    AUD_TCD_DIP_ELD_CTRL_ST = 0x653B4


class _AUD_DIP_ELD_CTRL_ST(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DipAccessAddress', ctypes.c_uint32, 4),
        ('EldAck', ctypes.c_uint32, 1),
        ('EldAccessAddress', ctypes.c_uint32, 5),
        ('EldBufferSize', ctypes.c_uint32, 5),
        ('Reserved15', ctypes.c_uint32, 1),
        ('DipTransmissionFrequency', ctypes.c_uint32, 2),
        ('DipBufferIndex', ctypes.c_uint32, 3),
        ('DipTypeEnableStatus', ctypes.c_uint32, 4),
        ('Reserved25', ctypes.c_uint32, 3),
        ('DipPortSelect', ctypes.c_uint32, 4),
    ]


class REG_AUD_DIP_ELD_CTRL_ST(ctypes.Union):
    value = 0
    offset = 0

    DipAccessAddress = 0  # bit 0 to 4
    EldAck = 0  # bit 4 to 5
    EldAccessAddress = 0  # bit 5 to 10
    EldBufferSize = 0  # bit 10 to 15
    Reserved15 = 0  # bit 15 to 16
    DipTransmissionFrequency = 0  # bit 16 to 18
    DipBufferIndex = 0  # bit 18 to 21
    DipTypeEnableStatus = 0  # bit 21 to 25
    Reserved25 = 0  # bit 25 to 28
    DipPortSelect = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_DIP_ELD_CTRL_ST),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_DIP_ELD_CTRL_ST, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_AUD_ICOI:
    AUD_ICOI = 0x65F00


class _AUD_ICOI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Icw', ctypes.c_uint32, 32),
    ]


class REG_AUD_ICOI(ctypes.Union):
    value = 0
    offset = 0

    Icw = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_ICOI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_ICOI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_AUD_IRII:
    AUD_IRII = 0x65F04


class _AUD_IRII(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Irr', ctypes.c_uint32, 32),
    ]


class REG_AUD_IRII(ctypes.Union):
    value = 0
    offset = 0

    Irr = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_IRII),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_IRII, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ICB(Enum):
    ICB_COMMAND_DONE = 0x0  # Command_done
    ICB_COMMAND_AVAILABLE = 0x1  # Command_available


class ENUM_IRV(Enum):
    IRV_RESPONSE_READ = 0x0  # Response_read
    IRV_RESPONSE_AVAILABLE = 0x1  # Response_available


class OFFSET_AUD_ICS:
    AUD_ICS = 0x65F08


class _AUD_ICS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Icb', ctypes.c_uint32, 1),
        ('Irv', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 30),
    ]


class REG_AUD_ICS(ctypes.Union):
    value = 0
    offset = 0

    Icb = 0  # bit 0 to 1
    Irv = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_ICS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_ICS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DETECT_FRAME_SYNC_EARLY(Enum):
    DETECT_FRAME_SYNC_EARLY_PULL_IN_BY_0_BCLKS = 0x0  # Frame sync is detected at bclk = 1998.
    DETECT_FRAME_SYNC_EARLY_PULL_IN_BY_1_BCLKS = 0x1  # Frame sync is detected at bclk = 1997.
    DETECT_FRAME_SYNC_EARLY_PULL_IN_BY_2_BCLKS = 0x2  # Frame sync is detected at bclk = 1996.
    DETECT_FRAME_SYNC_EARLY_PULL_IN_BY_3_BCLKS = 0x3  # Frame sync is detected at bclk = 1995.


class ENUM_BYPASS_FLOP(Enum):
    BYPASS_FLOP_NO_BYPASS = 0x0  # Flop in the AUDIO OUT IO is not bypassed.
    BYPASS_FLOP_BYPASS = 0x1  # Flop in the AUDIO OUT IO is bypassed.


class ENUM_TMODE(Enum):
    TMODE_4T = 0x0  # 4T mode with sdi data held for 4 bit clks.
    TMODE_2T = 0x1  # 2T Mode with sdi data held for 2 bit clocks. To use 2T mode, the bclk has to be 48MHz and flop i
                     # n the IO needs to bypass by setting the chicken bit 13 of this register. BIOS has to program
                     # 48MHz in the controller also to use this mode.
    TMODE_8T = 0x2  # 8T Mode with sdi data held for 8 bit clocks.
    TMODE_16T = 0x3  # 16T Mode with sdi data held for 16 bit clocks.


class OFFSET_AUD_FREQ_CNTRL:
    AUD_FREQ_CNTRL = 0x65900


class _AUD_FREQ_CNTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 3),
        ('_48MhzBclk', ctypes.c_uint32, 1),
        ('_96MhzBclk', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 6),
        ('DetectFrameSyncEarly', ctypes.c_uint32, 2),
        ('BypassFlop', ctypes.c_uint32, 1),
        ('TMode', ctypes.c_uint32, 2),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_AUD_FREQ_CNTRL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    _48MhzBclk = 0  # bit 3 to 4
    _96MhzBclk = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 11
    DetectFrameSyncEarly = 0  # bit 11 to 13
    BypassFlop = 0  # bit 13 to 14
    TMode = 0  # bit 14 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_FREQ_CNTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_FREQ_CNTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ENABLE(Enum):
    ENABLE_DISABLE = 0x0
    ENABLE_ENABLE = 0x1


class OFFSET_AUDIO_PIN_BUF_CTL:
    AUDIO_PIN_BUF_CTL = 0x48414


class _AUDIO_PIN_BUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PullupSlew', ctypes.c_uint32, 4),
        ('PullupStrength', ctypes.c_uint32, 5),
        ('Reserved9', ctypes.c_uint32, 3),
        ('PulldownSlew', ctypes.c_uint32, 4),
        ('PulldownStrength', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Spare', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Hysteresis', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 1),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_AUDIO_PIN_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    PullupSlew = 0  # bit 0 to 4
    PullupStrength = 0  # bit 4 to 9
    Reserved9 = 0  # bit 9 to 12
    PulldownSlew = 0  # bit 12 to 16
    PulldownStrength = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 24
    Spare = 0  # bit 24 to 27
    Reserved27 = 0  # bit 27 to 28
    Hysteresis = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 31
    Enable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUDIO_PIN_BUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUDIO_PIN_BUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_A(Enum):
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_A_ALL_SAMPLES_AVAILABLE_IN_BUFFER = 0x0  # When set to this value, all the coll
                                                                                 # ected samples in the buffer are
                                                                                 # unloaded on the line in the hblank
                                                                                 # region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_A_1_SAMPLE_PER_LINE = 0x1  # When set to this value, maximum of one sample(eac
                                                                    # h sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer is
                                                                    # unloaded on the line in the hblank region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_A_2_SAMPLE_PER_LINE = 0x2  # When set to this value, maximum of two samples(ea
                                                                    # ch sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer are
                                                                    # unloaded on the line in the hblank region.


class ENUM_HBLANK_START_COUNT_FOR_PIPE_A(Enum):
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_8_TCACLKS = 0x0  # Hblank is generated 8 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_16_TCACLKS = 0x1  # Hblank is generated 16 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_32_TCACLKS = 0x2  # Hblank is generated 32 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_64_TCACLKS = 0x3  # Hblank is generated 64 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_96_TCACLKS = 0x4  # Hblank is generated 96 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_A_DELAY_OF_128_TCACLKS = 0x5  # Hblank is generated 128 tcclks early.


class ENUM_NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_B(Enum):
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_B_ALL_SAMPLES_AVAILABLE_IN_BUFFER = 0x0  # When set to this value, all the coll
                                                                                 # ected samples in the buffer are
                                                                                 # unloaded on the line in the hblank
                                                                                 # region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_B_1_SAMPLE_PER_LINE = 0x1  # When set to this value, maximum of one sample(eac
                                                                    # h sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer is
                                                                    # unloaded on the line in the hblank region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_B_2_SAMPLE_PER_LINE = 0x2  # When set to this value, maximum of two samples(ea
                                                                    # ch sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer are
                                                                    # unloaded on the line in the hblank region.


class ENUM_HBLANK_START_COUNT_FOR_PIPE_B(Enum):
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_8_TCBCLKS = 0x0  # Hblank is generated 8 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_16_TCBCLKS = 0x1  # Hblank is generated 16 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_32_TCBCLKS = 0x2  # Hblank is generated 32 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_64_TCBCLKS = 0x3  # Hblank is generated 64 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_96_TCBCLKS = 0x4  # Hblank is generated 96 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_B_DELAY_OF_128_TCBCLKS = 0x5  # Hblank is generated 128 tcclks early.


class ENUM_NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_C(Enum):
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_C_ALL_SAMPLES_AVAILABLE_IN_BUFFER = 0x0  # When set to this value, all the coll
                                                                                 # ected samples in the buffer are
                                                                                 # unloaded on the line in the hblank
                                                                                 # region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_C_1_SAMPLE_PER_LINE = 0x1  # When set to this value, maximum of one sample(eac
                                                                    # h sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer is
                                                                    # unloaded on the line in the hblank region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_C_2_SAMPLE_PER_LINE = 0x2  # When set to this value, maximum of two samples(ea
                                                                    # ch sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer are
                                                                    # unloaded on the line in the hblank region.


class ENUM_HBLANK_START_COUNT_FOR_PIPE_C(Enum):
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_8_TCCCLKS = 0x0  # Hblank is generated 8 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_16_TCCCLKS = 0x1  # Hblank is generated 16 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_32_TCCCLKS = 0x2  # Hblank is generated 32 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_64_TCCCLKS = 0x3  # Hblank is generated 64 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_96_TCCCLKS = 0x4  # Hblank is generated 96 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_C_DELAY_OF_128_TCCCLKS = 0x5  # Hblank is generated 128 tcclks early.


class ENUM_NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_D(Enum):
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_D_ALL_SAMPLES_AVAILABLE_IN_BUFFER = 0x0  # When set to this value, all the coll
                                                                                 # ected samples in the buffer are
                                                                                 # unloaded on the line in the hblank
                                                                                 # region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_D_1_SAMPLE_PER_LINE = 0x1  # When set to this value, maximum of one sample(eac
                                                                    # h sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer is
                                                                    # unloaded on the line in the hblank region.
    NUMBER_OF_SAMPLES_PER_LINE_FOR_PIPE_D_2_SAMPLE_PER_LINE = 0x2  # When set to this value, maximum of two samples(ea
                                                                    # ch sample has 2 channels data for layout0 and 8
                                                                    # channels data in layout 1 mode) in the buffer are
                                                                    # unloaded on the line in the hblank region.


class ENUM_HBLANK_START_COUNT_FOR_PIPE_D(Enum):
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_8_TCACLKS = 0x0  # Hblank is generated 8 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_16_TCACLKS = 0x1  # Hblank is generated 16 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_32_TCACLKS = 0x2  # Hblank is generated 32 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_64_TCACLKS = 0x3  # Hblank is generated 64 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_96_TCACLKS = 0x4  # Hblank is generated 96 tcclks early.
    HBLANK_START_COUNT_FOR_PIPE_D_DELAY_OF_128_TCACLKS = 0x5  # Hblank is generated 128 tcclks early.


class ENUM_HBLANK_EARLY_ENABLE_FOR_PIPEA(Enum):
    HBLANK_EARLY_ENABLE_FOR_PIPEA_HBLANK_EARLY_DISABLE = 0x0  # The default Hblank is used and a delay of 16 tcclks is 
                                                              # added before the SM arcs during each hblank for Pipe A.
    HBLANK_EARLY_ENABLE_FOR_PIPEA_HBLANK_EARLY_ENABLE = 0x1  # The early hblank programmed by fields hblank_start count
                                                             #  for Pipe A will be used to trigger samplecount
                                                             # calculation for Pipe A.


class ENUM_HBLANK_EARLY_ENABLE_FOR_PIPEB(Enum):
    HBLANK_EARLY_ENABLE_FOR_PIPEB_HBLANK_EARLY_DISABLE = 0x0  # The default Hblank is used and a delay of 16 tcclks is 
                                                              # added before the SM arcs during each hblank for Pipe B
    HBLANK_EARLY_ENABLE_FOR_PIPEB_HBLANK_EARLY_ENABLE = 0x1  # The early hblank programmed by fields hblank_start count
                                                             #  for Pipe B will be used to trigger samplecount
                                                             # calculation for Pipe B.


class ENUM_HBLANK_EARLY_ENABLE_FOR_PIPEC(Enum):
    HBLANK_EARLY_ENABLE_FOR_PIPEC_HBLANK_EARLY_DISABLE = 0x0  # The default Hblank is used and a delay of 16 tcclks is 
                                                              # added before the SM arcs during each hblank for Pipe C
    HBLANK_EARLY_ENABLE_FOR_PIPEC_HBLANK_EARLY_ENABLE = 0x1  # The early hblank programmed by fields hblank_start count
                                                             #  for Pipe C will be used to trigger samplecount
                                                             # calculation for Pipe C.


class ENUM_HBLANK_EARLY_ENABLE_FOR_PIPED(Enum):
    HBLANK_EARLY_ENABLE_FOR_PIPED_HBLANK_EARLY_DISABLE = 0x0  # The default Hblank is used and a delay of 16 tcclks is 
                                                              # added before the SM arcs during each hblank for Pipe D
    HBLANK_EARLY_ENABLE_FOR_PIPED_HBLANK_EARLY_ENABLE = 0x1  # The early hblank programmed by fields hblank_start count
                                                             #  for Pipe D will be used to trigger samplecount
                                                             # calculation for Pipe D.


class ENUM_DELAY_SAMPLE_COUNT_LATCH_PIPE_A(Enum):
    DELAY_SAMPLE_COUNT_LATCH_PIPE_A_DELAY_BY_16_CLOCKS = 0x0  # When set to 0, sample count latch is delayed by 16 cloc
                                                              # ks after Hblank starts.
    DELAY_SAMPLE_COUNT_LATCH_PIPE_A_DELAY_BY_32_CLOCKS = 0x1  # When set to 1, sample count latch is delayed by 32 cloc
                                                              # ks after Hblank starts.


class ENUM_DELAY_SAMPLE_COUNT_LATCH_PIPE_B_(Enum):
    DELAY_SAMPLE_COUNT_LATCH_PIPE_B_DELAY_BY_16_CLOCKS = 0x0  # When set to 0, sample count latch is delayed by 16 clo
                                                               # cks after Hblank starts.
    DELAY_SAMPLE_COUNT_LATCH_PIPE_B_DELAY_BY_32_CLOCKS = 0x1  # When set to 1, sample count latch is delayed by 32 clo
                                                               # cks after Hblank starts.


class ENUM_DELAY_SAMPLE_COUNT_LATCH_PIPE_C(Enum):
    DELAY_SAMPLE_COUNT_LATCH_PIPE_C_DELAY_BY_16_CLOCKS = 0x0  # When set to 0, sample count latch is delayed by 16 cloc
                                                              # ks after Hblank starts.
    DELAY_SAMPLE_COUNT_LATCH_PIPE_C_DELAY_BY_32_CLOCKS = 0x1  # When set to 1, sample count latch is delayed by 32 cloc
                                                              # ks after Hblank starts.


class ENUM_DELAY_SAMPLE_COUNT_LATCH_PIPE_D(Enum):
    DELAY_SAMPLE_COUNT_LATCH_PIPE_D_DELAY_BY_16_CLOCKS = 0x0  # When set to 0, sample count latch is delayed by 16 cloc
                                                              # ks after Hblank starts.
    DELAY_SAMPLE_COUNT_LATCH_PIPE_D_DELAY_BY_32_CLOCKS = 0x1  # When set to 1, sample count latch is delayed by 32 cloc
                                                              # ks after Hblank starts.


class OFFSET_AUD_CONFIG_BE:
    AUD_CONFIG_BE = 0x65EF0


class _AUD_CONFIG_BE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('NumberOfSamplesPerLineForPipeA', ctypes.c_uint32, 2),
        ('DpMixerMainstreamPriorityEnableForPipeA', ctypes.c_uint32, 1),
        ('Hblank_StartCountForPipeA', ctypes.c_uint32, 3),
        ('NumberOfSamplesPerLineForPipeB', ctypes.c_uint32, 2),
        ('DpMixerMainstreamPriorityEnableForPipeB', ctypes.c_uint32, 1),
        ('Hblank_StartCountForPipeB', ctypes.c_uint32, 3),
        ('NumberOfSamplesPerLineForPipeC', ctypes.c_uint32, 2),
        ('DpMixerMainstreamPriorityEnableForPipeC', ctypes.c_uint32, 1),
        ('Hblank_StartCountForPipeC', ctypes.c_uint32, 3),
        ('NumberOfSamplesPerLineForPipeD', ctypes.c_uint32, 2),
        ('DpMixerMainstreamPriorityEnableForPipeD', ctypes.c_uint32, 1),
        ('Hblank_StartCountForPipeD', ctypes.c_uint32, 3),
        ('HblankEarlyEnableForPipea', ctypes.c_uint32, 1),
        ('HblankEarlyEnableForPipeb', ctypes.c_uint32, 1),
        ('HblankEarlyEnableForPipec', ctypes.c_uint32, 1),
        ('HblankEarlyEnableForPiped', ctypes.c_uint32, 1),
        ('DelaySampleCountLatchPipeA', ctypes.c_uint32, 1),
        ('DelaySampleCountLatchPipeB', ctypes.c_uint32, 1),
        ('DelaySampleCountLatchPipeC', ctypes.c_uint32, 1),
        ('DelaySampleCountLatchPipeD', ctypes.c_uint32, 1),
    ]


class REG_AUD_CONFIG_BE(ctypes.Union):
    value = 0
    offset = 0

    NumberOfSamplesPerLineForPipeA = 0  # bit 0 to 2
    DpMixerMainstreamPriorityEnableForPipeA = 0  # bit 2 to 3
    Hblank_StartCountForPipeA = 0  # bit 3 to 6
    NumberOfSamplesPerLineForPipeB = 0  # bit 6 to 8
    DpMixerMainstreamPriorityEnableForPipeB = 0  # bit 8 to 9
    Hblank_StartCountForPipeB = 0  # bit 9 to 12
    NumberOfSamplesPerLineForPipeC = 0  # bit 12 to 14
    DpMixerMainstreamPriorityEnableForPipeC = 0  # bit 14 to 15
    Hblank_StartCountForPipeC = 0  # bit 15 to 18
    NumberOfSamplesPerLineForPipeD = 0  # bit 18 to 20
    DpMixerMainstreamPriorityEnableForPipeD = 0  # bit 20 to 21
    Hblank_StartCountForPipeD = 0  # bit 21 to 24
    HblankEarlyEnableForPipea = 0  # bit 24 to 25
    HblankEarlyEnableForPipeb = 0  # bit 25 to 26
    HblankEarlyEnableForPipec = 0  # bit 26 to 27
    HblankEarlyEnableForPiped = 0  # bit 27 to 28
    DelaySampleCountLatchPipeA = 0  # bit 28 to 29
    DelaySampleCountLatchPipeB = 0  # bit 29 to 30
    DelaySampleCountLatchPipeC = 0  # bit 30 to 31
    DelaySampleCountLatchPipeD = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _AUD_CONFIG_BE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_AUD_CONFIG_BE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

