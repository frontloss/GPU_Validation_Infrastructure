#######################################################################################################################
# @file         registry.py
# @addtogroup   PowerCons
# @section      Libs
# @brief        Contains registry keys, registry values and APIs to access registry
#
# @author       Rohit Kumar
#######################################################################################################################

import ctypes

from Libs.Core import enum, registry_access
from Libs.Core import system_utility

__system_utility = system_utility.SystemUtility()


##
# @brief        Exposed object having common and feature specific registry values
class RegValues(object):
    ENABLE = 0x1
    DISABLE = 0x0

    ##
    # @brief        Registry key values for DRRS keys
    class DRRS(object):
        STATIC_DRRS_ENABLE = 0x1
        SEAMLESS_DRRS_ENABLE = 0x2
        MDRRS_ENABLE = 0x803F
        MDRRS_DISABLE = 0x80000000
        DMRRS_DISABLE_INTERNAL_PANEL_PC_FTR_CTL = 0x200000
        DMRRS_ENABLE_INTERNAL_PANEL_PC_FTR_CTL = 0xFFDFFFFF
        DMRRS_DISABLE_EXTERNAL_PANEL_PC_FTR_CTL = 0x400000
        DMRRS_ENABLE_EXTERNAL_PANEL_PC_FTR_CTL = 0xFFBFFFFF

    ##
    # @brief        Registry key values for FMS enable 0th bit 1 for enabled, 0 for disabled
    class FMS(object):
        ENABLED = 0x1d
        DISABLED = 0x1c

    ##
    # @brief        Registry key values for LRR keys
    class LRR:
        LRR_VERSION_INVALID = 0
        LRR_VERSION_1_0 = 1
        LRR_VERSION_2_0 = 2
        LRR_VERSION_2_5 = 3

    ##
    # @brief        Registry key values for VRR keys
    class VRR(object):
        USER_SETTING_LOW_FPS_ONLY = 0x3
        USER_SETTING_HIGH_FPS_ONLY = 0x5
        USER_SETTING_LOW_HIGH_FPS = 0x7

    ##
    # @brief        Registry keys for BPC
    class BPC(object):
        SELECT_BPC = "SelectBPC"
        SELECT_BPC_FROM_REGISTRY = "SelectBPCFromRegistry"


##
# @brief        Exposed object having common and feature specific registry keys
class RegKeys(object):
    # Common
    FEATURE_TEST_CONTROL = "FeatureTestControl"
    DISPLAY_FEATURE_CONTROL = "DisplayFeatureControl"
    DISPLAY_FEATURE_CONTROL2 = "DisplayFeatureControl2"
    AC_POWER_POLICY_DATA = "DISPPCACPowerPolicyData"
    DC_POWER_POLICY_DATA = "DISPCDCPowerPolicyData"
    AC_USER_PREFERENCE_POLICY = "DISPCACUserPreferencePolicy"
    DC_USER_PREFERENCE_POLICY = "DISPCDCUserPreferencePolicy"
    POWER_PLAN_AWARE_SETTINGS = "PowerPlanAwareFeatureSettings"
    DISPLAY_SW_WA_CONTROL = "DisplaySoftwareWaControl"

    ##
    # @brief        Registry keys for ASSR
    class ASSR(object):
        ALTERNATE_SCRAMBLER_SUPPORT = "AlternateScramblerSupport"

    ##
    # @brief        Registry keys for BLC
    class BLC(object):
        HIGH_PRECISION = "HighPrecisionBrightnessEnable"
        NIT_RANGE_COUNT = "LFP_NitRangeCount_"
        NIT_RANGES = "LFP_NitRanges_"
        LFP_NIT_RANGES_FFFF = "LFP_NitRanges_FFFF"
        DISABLE_NITS_BRIGHTNESS = "DisableNitsBrightness"
        INDEPENDENT_BRIGHTNESS_CTL = "IndependentBrightnessControl"     # driver persistence regkey

    ##
    # @brief        Registry keys for DPST
    class DPST(object):
        OVERRIDE_BPP = "DpstTurnOffBppPanelReq"
        AGGRESSIVENESS_LEVEL = "PowerDpstAggressivenessLevel"
        EPSM_STATUS = "Dpst6_3ApplyExtraDimming"
        DPST_BACKLIGHT_THRESHOLD = "DpstBacklightThreshold"
        DPST_BACKLIGHT_THRESHOLD_LOWER = "DpstBacklightLowerThreshold"
        DPST_BACKLIGHT_THRESHOLD_UPPER = "DpstBacklightUpperThreshold"
        SMOOTHENING_MIN_SPEED = "DpstSmootheningMinSpeed"
        SMOOTHENING_MAX_SPEED = "DpstSmootheningMaxSpeed"
        SMOOTHENING_PERIOD = "DpstSmootheningPeriod"
        SMOOTHENING_TOLERANCE = "DpstSmootheningTolerance"
        VERSION = "DpstVersion"
        EPSM_WEIGHT = "DpstEpsmWeight"

    ##
    # @brief        Registry keys for DRRS
    class DRRS(object):
        DRRS_ENABLE = "Display1_DPSPanel_Type"
        DRRS_MAM_SUPPORT = "DPSMotionArtifactMitigation"
        MEDIA_REFRESH_RATE_SUPPORT = "MediaRefreshRateSupport"

    ##
    # @brief        Registry keys for HRR
    class HRR(object):
        FORCE_ENABLE_D13_HRR = "ForceEnableD13Hrr"

    ##
    # @brief        Registry keys for FLT
    class FLT(object):
        NO_FLT_FOR_EDP = "NoFastLinkTrainingForeDP"

    ##
    # @brief        Registry keys for FMS
    class FMS(object):
        DISPLAY_OPTIMIZATION = "DisplayOptimizations"

    ##
    # @brief        Registry keys for HDR
    class HDR(object):
        FORCE_HDR_MODE = "ForceHDRMode"

    ##
    # @brief        Registry keys for LRR
    class LRR:
        LRR_VERSION_CAPS_OVERRIDE = "LRRVersionCapsOverride"

    ##
    # @brief        Registry keys for DisplayPc
    class PC(object):
        FEATURE_CONTROL = "DisplayPcFeatureControl"
        FEATURE_CONTROL_DEBUG = "DisplayPcFeatureControlDebug"

    ##
    # @brief        Registry keys for PSR
    class PSR(object):
        PSR2_DISABLE = "PSR2Disable"
        PSR_DISABLE_IN_AC = "PsrDisableInAc"
        PSR_DEBUG_CTRL = "PSRDebugCtrl"
        PSR2_DRRS_ENABLE = "PSR2DrrsEnable"
        PSR1_SETUP_TIME_OVERRIDE = "Psr1SetupTime_"

    ##
    # VRR RegKeys
    # @note Source: gfx-driver\Source\inc\common\regkeys.h : 613
    class VRR(object):
        # OEM + Platform Support : 1 = Feature Enable, 0 = Feature Disable
        VRR_ADAPTIVE_VSYNC_ENABLE = "AdaptiveVsyncEnable"
        # User setting : 1 = Feature Enable, 0 = Feature Disable
        VRR_USER_SETTING = "VRRFtrUserSetting"
        # VRR MaxShift value for eDP. To be read if panel does not support DPCD with max shift value
        VRR_MAX_SHIFT_VALUE_LFP = "VRRMaxShiftValueLFP"
        # Adaptive Vsync value set by the user through the CUI. 1 = Enable and 0 = Disable
        # BIT0: Adaptive Sync Enable, BIT1: AdaptiveSync Low FPS Enable, BIT2: Adaptive Sync High FPS Enable
        VRR_ADAPTIVE_VSYNC_USER_SETTING = "AdaptiveVsyncEnableUserSetting"


##
# @brief    bit representation for DisplayFeatureControl reg key
class DisplayFeatureControlFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('y_tiling_enabled_flag', ctypes.c_uint32, 1),  # Bit 0
        ('mpo_nv12_enabled_flag', ctypes.c_uint32, 1),  # Bit 1
        ('rend_comp_enabled_flag', ctypes.c_uint32, 1),  # Bit 2
        ('gt_type_fused_enabled_flag', ctypes.c_uint32, 1),  # Bit 3
        ('reserved_1', ctypes.c_uint32, 1),  # Bit 4
        ('mpo_enabled_flag', ctypes.c_uint32, 1),  # Bit 5
        ('mpo_in_multi_display_enabled_flag', ctypes.c_uint32, 1),  # Bit 6
        ('mpo_yuv2_enabled_flag', ctypes.c_uint32, 1),  # Bit 7
        ('mpo_yuv2_scaling_enabled', ctypes.c_uint32, 1),  # Bit 8
        ('hdr_fp16_scanout_support', ctypes.c_uint32, 1),  # Bit 9
        ('reserved_2', ctypes.c_uint32, 3),  # Bit 10:12
        ('disable_dram_bw_check', ctypes.c_uint32, 1),  # Bit 13
        ('disable_smooth_sync', ctypes.c_uint32, 1),  # Bit 14
        ('disable_tile4_memory', ctypes.c_uint32, 1),  # Bit 15
        ('disable_nn_scaling', ctypes.c_uint32, 1),  # Bit 16
        ('display_engine_tone_mapping_enabled_flag', ctypes.c_uint32, 1),  # Bit 17
        ('disable_hrr', ctypes.c_uint32, 1),  # Bit 18
        ('disable_dp_yuv420_encoding_support', ctypes.c_uint32, 1),  # Bit 19
        ('flip_queue_enable_flag', ctypes.c_uint32, 1),  # Bit 20
        ('disable_min_dbuf_for_async_flips', ctypes.c_uint32, 1),  # Bit 21
        ('disable_gamma_register_writes_using_dsb', ctypes.c_uint32, 1),  # Bit 22
        ('disable_adaptive_sync_sdp', ctypes.c_uint32, 1),  # Bit 23
        ('disable_enhanced_underrun_recovery', ctypes.c_uint32, 1),  # Bit 24
        ('disable_cmtg', ctypes.c_uint32, 1),  # Bit 25
        ('reserved_3', ctypes.c_uint32, 6)  # Bit 26:31
    ]


##
# @brief    class for DisplayFeatureControl reg key
class DisplayFeatureControl(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DisplayFeatureControlFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(DisplayFeatureControl, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.DISPLAY_FEATURE_CONTROL):
            self.value = read(adapter, RegKeys.DISPLAY_FEATURE_CONTROL)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.DISPLAY_FEATURE_CONTROL, registry_access.RegDataType.DWORD, self.value)


##
# @brief    bit representation for DisplayFeatureControl2 reg key
class DisplayFeatureControl2Fields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('OsFlipQueueEnableFlag', ctypes.c_uint32, 1),  # Bit 0
        ('DFTFlipQueueEnableFlag', ctypes.c_uint32, 1),  # Bit 1
        ('DisableDmcFlipQueue', ctypes.c_uint32, 1),  # Bit 2
        ('EnableOsUnawareFlipQ', ctypes.c_uint32, 1),  # Bit 3
        ('EnableVscSDPChainingSupport', ctypes.c_uint32, 1),  # Bit 4
        ('EnableCenteredScalingSupport', ctypes.c_uint32, 1),  # Bit 5
        ('DisableDisplayShiftSupport', ctypes.c_uint32, 1),  # Bit 6
        ('DisableLayerReordering', ctypes.c_uint32, 1),  # Bit 7
        ('DisableVirtualRefreshRateSupport', ctypes.c_uint32, 1),  # Bit 8
        ('DisableHwDarkScreenDetection', ctypes.c_uint32, 1),  # Bit 9
        ('DisableFlipQVbiOptimization', ctypes.c_uint32, 1),  # Bit 10
        ('reserved_2', ctypes.c_uint32, 20)  # Bit 11:31
    ]


##
# @brief    class for DisplayFeatureControl reg key
class DisplayFeatureControl2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DisplayFeatureControl2Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(DisplayFeatureControl2, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.DISPLAY_FEATURE_CONTROL2):
            self.value = read(adapter, RegKeys.DISPLAY_FEATURE_CONTROL2)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.DISPLAY_FEATURE_CONTROL2, registry_access.RegDataType.DWORD, self.value)


##
# @brief        Exposed object having common and feature specific registry keys
class FeatureTestControlFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('cxsr_disable', ctypes.c_uint32, 1),  # Bit 0
        ('fbc_disable', ctypes.c_uint32, 1),  # Bit 1
        ('gsv_disable', ctypes.c_uint32, 1),  # Bit 2
        ('blc_disable', ctypes.c_uint32, 1),  # Bit 3
        ('dpst_disable', ctypes.c_uint32, 1),  # Bit 4
        ('reserved_1', ctypes.c_uint32, 1),  # Bit 5
        ('dps_disable', ctypes.c_uint32, 1),  # Bit 6
        ('rs_disable', ctypes.c_uint32, 1),  # Bit 7
        ('blc_dxgkddi_disable', ctypes.c_uint32, 1),  # Bit 8
        ('reserved_2', ctypes.c_uint32, 1),  # Bit 9
        ('turbo_disable', ctypes.c_uint32, 1),  # Bit 10
        ('psr_disable', ctypes.c_uint32, 1),  # Bit 11
        ('dfps_disable', ctypes.c_uint32, 1),  # Bit 12
        ('adt_disable', ctypes.c_uint32, 1),  # Bit 13
        ('reserved_3', ctypes.c_uint32, 1),  # Bit 14
        ('lace_disable', ctypes.c_uint32, 1),  # Bit 15
        ('reserved_4', ctypes.c_uint32, 16)  # Bit 16:31
    ]


##
# @brief    class for FeatureTestControl reg key
class FeatureTestControl(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", FeatureTestControlFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(FeatureTestControl, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.FEATURE_TEST_CONTROL):
            self.value = read(adapter, RegKeys.FEATURE_TEST_CONTROL)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.FEATURE_TEST_CONTROL, registry_access.RegDataType.DWORD, self.value)


##
# @brief    bit representation for DisplayPcFeatureControl reg key
class DisplayPcFeatureControlFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisablePixelClkSupportOnVrrPanel', ctypes.c_uint32, 1),  # Bit 0
        ('reserved', ctypes.c_uint32, 9),  # Bit 1:9
        ('DisableSelectiveFetch', ctypes.c_uint32, 1),  # Bit 10
        ('reserved_1', ctypes.c_uint32, 2),  # Bit 11:12
        ('DisableDC5', ctypes.c_uint32, 1),  # Bit 13
        ('DisableDC6', ctypes.c_uint32, 1),  # Bit 14
        ('DisableDC9', ctypes.c_uint32, 1),  # Bit 15
        ('DisableCappedFps', ctypes.c_uint32, 1),  # Bit 16
        ('reserved_2', ctypes.c_uint32, 1),  # Bit 17
        ('DisableDC6v', ctypes.c_uint32, 1),  # Bit 18
        ('DisableDpPanelReplay', ctypes.c_uint32, 1),  # Bit 19
        ('DisableCdClkBy2Change', ctypes.c_uint32, 1),  # Bit 20
        ('DisableDmrrsInternalDisplay', ctypes.c_uint32, 1),  # Bit 21
        ('DisableDmrrsExternalDisplay', ctypes.c_uint32, 1),  # Bit 22
        ('DisableTconBacklightOptimization', ctypes.c_uint32, 1),  # Bit 23
        ('DisableEnduranceGaming', ctypes.c_uint32, 1),  # Bit 24
        ('DisableOpst', ctypes.c_uint32, 1),  # Bit 25
        ('reserved_3', ctypes.c_uint32, 2),  # Bit 26:27
        ('DisableFsscSupport', ctypes.c_uint32, 1),  # Bit 28 , Full Screen Solid Color support
        ('reserved_4', ctypes.c_uint32, 1),  # Bit 29
        ('DisableAlrr', ctypes.c_uint32, 1),  # Bit 30
        ('reserved_5', ctypes.c_uint32, 1)  # Bit 31
    ]


##
# @brief    class for DisplayPcFeatureControl reg key
class DisplayPcFeatureControl(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DisplayPcFeatureControlFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(DisplayPcFeatureControl, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.PC.FEATURE_CONTROL):
            self.value = read(adapter, RegKeys.PC.FEATURE_CONTROL)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.PC.FEATURE_CONTROL, registry_access.RegDataType.DWORD, self.value)


##
# @brief    bit representation for DisplayPcFeatureCtrlDbg reg key
class DisplayPcFeatureCtrlDbgFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisableDmcPeriodicAsSdp', ctypes.c_uint32, 1),  # Bit 0
        ('DisableHwPeriodicAsSdp', ctypes.c_uint32, 1),  # Bit 1
        ('DisableDpAlpmSupport', ctypes.c_uint32, 1),  # Bit 2
        ('DisableEdpPanelReplay', ctypes.c_uint32, 1),  # Bit 3
        ('DisableLobf', ctypes.c_uint32, 1),  # Bit 4
        ('DisableFbcPsr2Coexistence', ctypes.c_uint32, 1),  # Bit 5
        ('DisableDeepPkgC8', ctypes.c_uint32, 1),  # Bit 6
        ('DisableFbcSelectiveFetch', ctypes.c_uint32, 1),  # Bit 7
        ('DisablePanelReplaySelectiveFetch', ctypes.c_uint32, 1),  # Bit 8
        ('reserved', ctypes.c_uint32, 22),  # Bit 9:31
    ]


##
# @brief    class for DisplayPcFeatureCtrlDbg reg key
class DisplayPcFeatureCtrlDbg(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DisplayPcFeatureCtrlDbgFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(DisplayPcFeatureCtrlDbg, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.PC.FEATURE_CONTROL_DEBUG):
            self.value = read(adapter, RegKeys.PC.FEATURE_CONTROL_DEBUG)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.PC.FEATURE_CONTROL_DEBUG, registry_access.RegDataType.DWORD, self.value)


##
# @brief    bit representation for MediaRefreshRateSupportFields reg key
class MediaRefreshRateSupportFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rr24', ctypes.c_uint32, 1),
        ('Rr25', ctypes.c_uint32, 1),
        ('Rr30', ctypes.c_uint32, 1),
        ('Rr48', ctypes.c_uint32, 1),
        ('Rr50', ctypes.c_uint32, 1),
        ('Rr60', ctypes.c_uint32, 1),
        ('reserved_1', ctypes.c_uint32, 9),
        ('FractionalRrSupported', ctypes.c_uint32, 1),
        ('reserved_1', ctypes.c_uint32, 15),
        ('InfOverride', ctypes.c_uint32, 1),
    ]


##
# @brief    class for MediaRefreshRateSupport reg key
class MediaRefreshRateSupport(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MediaRefreshRateSupportFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Method to initialize above class when object is created
    # @param[in]    adapter object, Adapter
    def __init__(self, adapter):
        super(MediaRefreshRateSupport, self).__init__()
        self.value = 0
        if exists(adapter, RegKeys.DRRS.MEDIA_REFRESH_RATE_SUPPORT):
            self.value = read(adapter, RegKeys.DRRS.MEDIA_REFRESH_RATE_SUPPORT)

    ##
    # @brief        method to update reg key
    # @param[in]    adapter object, Adapter
    # @return       bool status
    def update(self, adapter):
        if self.value is None:
            self.value = 0
        return write(adapter, RegKeys.DRRS.MEDIA_REFRESH_RATE_SUPPORT, registry_access.RegDataType.DWORD, self.value)


##
# @brief        Exposed API to read any given registry
# @param[in]    adapter Enum, targeted adapter
# @param[in]    key String, registry key
# @return       data registry value if registry read is successful, None otherwise
def read(adapter, key):
    reg_args = registry_access.StateSeparationRegArgs(adapter)
    data, reg_type = registry_access.read(reg_args, key)
    if data is not None and registry_access.RegDataType.BINARY == registry_access.RegDataType(reg_type):
        data = int.from_bytes(data, byteorder="little")
    return data


##
# @brief        Exposed API to write any given registry
# @param[in]    adapter Enum, targeted adapter
# @param[in]    key String registry key
# @param[in]    data_type Enum, registry data type
# @param[in]    data DWORD/BINARY, registry data
# @return       True if write is successful, False if failed, None if expected value is already present
def write(adapter, key, data_type, data):
    reg_args = registry_access.StateSeparationRegArgs(adapter)
    if exists(adapter, key):
        current_value, value_type = registry_access.read(reg_args, key)
        if current_value == data:
            return None

    return registry_access.write(reg_args, key, data_type, data)


##
# @brief        Exposed API to check if a given registry key exists or not
# @param[in]    adapter Enum, targeted adapter
# @param[in]    key String, registry key
# @return       True if exists, False otherwise
def exists(adapter, key):
    reg_args = registry_access.StateSeparationRegArgs(adapter)
    reg_val, _ = registry_access.read(reg_args, key)
    if reg_val is None:
        return False
    return True


##
# @brief        Exposed API to delete any given registry
# @param[in]    adapter Enum, targeted adapter
# @param[in]    key String, registry key
# @return       Boolean True if registry delete is successful, None if not required and False otherwise
def delete(adapter, key):
    # delete registry is required only if key exists
    if exists(adapter, key):
        reg_args = registry_access.StateSeparationRegArgs(adapter)
        return registry_access.delete(reg_args, key)
    return None
