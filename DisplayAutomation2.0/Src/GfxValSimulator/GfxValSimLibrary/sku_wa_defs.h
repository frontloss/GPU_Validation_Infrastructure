/*========================== begin_copyright_notice ============================

INTEL CONFIDENTIAL

Copyright (C) 2021-2022 Intel Corporation

This software and the related documents are Intel copyrighted materials,
and your use of them is governed by the express license under which they were
provided to you ("License"). Unless the License provides otherwise,
you may not use, modify, copy, publish, distribute, disclose or transmit this
software or the related documents without Intel's prior written permission.

This software and the related documents are provided as is, with no express or
implied warranties, other than those that are expressly stated in the License.

============================= end_copyright_notice ===========================*/

/*
File Name: sku_wa.h

Description:
    Common hardware sku and workaround information structures.

    This file is commented in a manner allowing automated parsing of WA information.
    Each entry inside WA table should include comments in form of:
        @WorkaroundName           <name-mandatory> //this field is mandatory
        @HWBugLink                <hsd-link>
        @HWSightingLink           <hsd-link>
        @Description              <short description (can be multiline)
        @PerfImpact               <performance impact>
        @BugType                  <hang,crash etc.>
        @Component                <Sv/2D/DD/ocl/3d/PwrCons/Core/KMD_render/Gmm/DXVA/SoftBIOS>
        @EndWorkaroundMetadata    //this field is mandatory
*/
// struct _wa_Sv
WA_DECLARE(WaOpromReadThroughMmio, "WA to read OPROM from DG1 SPI through MMIO interface", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaEnableTypeCAuxPGForLegacyHdmi, "Enable TYPE C port AUX PG for legacy HDMI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDpDklPllProgramming, "TGL H P0 has a different DKL Phy PLL programming value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBltSubmissionCapture, "WA to capture the 1st blt submission for MSFT telemetry issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaFirstTimeEnable, "WA to capture the 1st time enable only during boot or enable device", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaIncreaseDefaultTLBEntries, "WA for a improve performance of OCL benchmark(Luxmark) by increasing TLB entries", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisSvClkGating, "WA_DISABLE_SV_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_MASF_ClkGating, "WA_DISABLE_MASF_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_ISC_ClkGating, "WA_DISABLE_ISC_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_VFE_ClkGating, "WA_DISABLE_VFE_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_Clipper_ClkGating, "WA_DISABLE_CL_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_VF_ClkGating, "WA_DISABLE_VF_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_GS_ClkGating, "WA_DISABLE_GS_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTempDisableDOPClkGating, "Temporarily disable DOP Clk gating while changing L3SQCREG1 value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_RCPH_RCC_RCZ_ClkGating, "WA_DISABLE_RCPH_RCC_RCZ_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_ECOSKPD_Chicken_Bits, "WA_DISABLE_ECOSKPD_CHICKEN_BITS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct _wa_2D

WA_DECLARE(Wa1280Cursor, "WA_1280x1024_75HZ_CURSOR for ALM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSyncFlush, "WA for INSTPM sync Flush mask bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa1stBlt, "WA for BDG 1st Blt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetupBlt, "WA for context setup", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTextImmBlt, "WA for Text IMM Blt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlipStatus, "ISR flip-status definition change.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIIRReadEnable, "IIR Read Enable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIsrFlipStatusRevert, "Turn on chicken-bit for ISR flip-status revert", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUserToggleIir, "Toggle WaFlipStatus with a registry key", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAsynchMMIOFlip,
           "Work Around to disable Asynchronous MMIO Flip if necessary for a platform. This Work around will be checked in function __KmQueryDriverCaps in KMRender component "
           "while reporting capabilities of Adapter to OS",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNonPipelinedStateCommandFlush, "or else blitter-to-renderer won't flush before pipe-control", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIlkEnableBothDispAndSPR, "WA for MBM Hardware Issue 2208943", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLoadHDCPKeys, "WA for HDCP Key Load issue on A stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaExtendedWaitForFlush, "Wa for Extended wait on ring buffer to idle.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBitBashingForILKHDCP, "Wa for using bitbashing for HDCP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBitBashingForILKEDID, "Wa for using bitbashing for Edid", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReadAksvFromDebugRegs, "Wa for reading Aksv Using Debug Registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDPHDMIBlankOutIssueOnSamePort, "Wa for DP/HDMI blankout issue on same port", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPruneModeWithIncorrectHsyncOffset, "Wa to prune mode when hsync front porch is zero", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePartialDPSFeatures, "Only for ILK. For LVDS, HW DRRS Feature is broken and hence needs to be disabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableIPLLinkLaneReversal, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSDVORxTerminationWA, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStrapStateInvalidforeDPifDisabled, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIPLPLLandDPLLRecoveryWA, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePF3BeforePipeDisable, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaeDPPLL162MhzWA, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableVGAAccessThroughIOPort, "From ILK Onwards, MMIO Index based method for accessing VGA is removed and hence we need to use VGA based IO Port Access method",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIlkFlipMMIO, "Flip using MMIO until ILK C0 for MBM to avoid corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableDPIdlePatternforOnlyx4Lane, "Don't enable idle pattern for 1x and 2x configs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRgbToYuvCSCInCenteredMode,
           "In ILK centering is achieved via PF3. When CSC unit is configured in RGB->YUV mode and the PF3 is active in centered mode, the black borders turn green.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaYuvToRgbCSCConversionDisable, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableClockGatingForMiWaitForEvent, "Also, related to ILK HW sighting 1114508", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableVDIPerformanceChickenBits, "VDI performance bits are not enabled by default by HW. Enable it in the driver. ILK HW Sighting 1114607", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSimDisableVblankInterrupt, "WA to disable vblank interrupt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaConvertAlphaToXORCursorForxvYCC, "WA to convert Alpha to XOR cursor when Sprite is in pass thorugh mode with xvYCC enabled", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTContextSaveIssue, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceVDD, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSNBA0VSwingPreEmphasisSelect, "WA to select the VSwing/PreEmphasis Combn. in SNB FDI for A Stepping. The Values are different from B.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSNBA0FDITxPLLOn, "WA to keep FDI PLL ON, as some of the port registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSNBIPLLaneCountSwitch, "Temporary WA for HW issue in switching lane count within x1, x2 & x3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTRbRvSyncIssue, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTRbsyncReadIssue, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSaveLastRingObj, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseStaticWMLatencyValues, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableeDPAfterEnableFDIPLL, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableNullVSDPkt, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSyncFlushVTDFix, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFDITrainLink, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFDIAutoLinkSetTimingOverrride, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(DisableSpritePassThroughMode, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFP16GammaEnabling, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WADP0ClockGatingDisable, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct _wa_DD

WA_DECLARE(Wa2DNegativeStart, "WA_2D_NEGATIVE, negative destination", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoAsyncFlip, "WA_NO_ASYNC_FLIP, WA for Almador A5, need to always set", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBatchBufferForWaitOnEvent, "WA_USE_BATCH_BUFFER_FOR_WAIT_ON_EVENT for 2nd sprite on Almador", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOvlFastHDownScale, "WA_OVERLAY_DOWN_SCALE on BDG", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOverlayPitch, "WA_OVERLAY_PITCH on Almador and BDG", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableVblank, "WA_ENABLE_VBLANK on Almador", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa2ndSpritePanning, "WA_PANNING_SECOND_SPRITE, No 2nd Sprite panning when overlay is panning", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOvHunitCounter, "OVHunit counter reset fails after >= 16x downscale (Alm family)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOvlPipeSwitching, "PipeSwitching overlay fails for napa family (sighting #54180)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPackedtoPlanar, "8 bit linear depth buffer broken (sighting #65500)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDdbmunitClkGating, "Overlay hangs on 63rd overlay flip CEG Tibet #1963931 Crestline A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSpriteClkGating, "Display is blanking out on disable of sprite for Gen5/6 (cantiga hw s304894, pcgsw b2555275)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSpriteAsOverlay, "Overlay HW broken on BWG.  Force Sprite as overlay.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoAsyncFlip180degree, "BWG has a HW issue due to which Async Flip should be turned off(HSD 300122)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaToggleRenderClockThrottle, "Disable the feature before overlay flip-on, enable it after flip-off", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableOverlayFlipsInAwayMode, "Disable overlay flips while in Vista 'Away' Mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaProgramDisplayPlaneWMforSprite, "Program Display Plane WM for Sprite Enable.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHas2CSLStubDisplay, "Wa to Enable Display for VLV on HAS 2.0 Env (HAS 2 only supports IVB Display presently )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableYTileForS3D, "Wa to disable YTile allocation for S3D usage (No S3D + RC support until B0) ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSKLDPAfeOverride, "Wa to overload customer specific AFE", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaKBLDPAfeOverride, "Wa to overload customer specific AFE", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaHDMIVswingChickenBitOverride, "Wa to override chicken bit to make vswing values effective for HDMI", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaLttprPowerCycleTransition, "Wa to Lttpr Transparent Mode transition until GOP/BBR FW has the resume cycle fix", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaEdpLinkRateDataReload, "Wa to Read DPCD 00010 ~ 0001F before writing DPCD00115 for Dell Rialto design with MUX (Parade PS8461E)", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDpMstDscHwImprovementsNotImplemented,
           "DP MST HW improvements wrt Audio and FEC Jitter are implemented from ADL-P D0, which reduces the minimum target dsc bpp needed to support minimum audio (48KHz, 2 Ch) "
           "and reduces flickering on display monitors connected to the MST/DSC docks . In order to differentiate the code b/w multiple platforms, defined this software w/a flag.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDpMstDscAudioBwFixImplemented,
           "DP MST HW improvements wrt Audio is implemented from RPLS B0 (ADLS D0), which reduces the minimum target dsc bpp needed to support minimum audio (48KHz, 2 Ch) . In "
           "order to differentiate the code b/w multiple platforms, defined this software w/a flag.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDpDklPhyPllUpdateRplP, "Some DKl Pll Programmings are RPLP specific only. In order to differentiate the code b/w multiple platforms, defined this software w/a flag.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(
WaDpMstDscJitter2FixesNotImplemented,
"DP MST DSC BS-to-BS Jitter-2 Fixes are implemented from RPL-P (ADL-P E0) onwards. In order to differentiate the code b/w multiple platforms, defined this software w/a flag.",
WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

// struct _wa_ocl

WA_DECLARE(WaOCLDisableMaxThreads, "Max simultaneous threads are limited to 1 until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLDisableBarriers, "Barriers are not supported until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLDisableImageWrites, "Image writes are not supported until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLDisableA64Messages, "A64 Messages are not supported on BDW A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLLimitCurbeSize, "Limit the CURBE size for IVB A0 GT2 Only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLAddMSFlushForPreemption, "( Bpsec ) DevHSW:A0 only: There should be two media state flush commands in a row for this stepping to ensure proper preemption",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLEnableFMaxFMinPlusZero,
           "Enable FMax(x+0, y+0)/FMin(x+0, y+0) for BDW A-step Only. In OCL, FMin/FMax behave not match the IEEE 754 with regard to signaling NaN. Specifically, FMax(0, SNaN) = "
           "0. While, on BDW A-step, it is IEEE-compliant:  FMax(0, SNaN) = QNaN. @                   Thus, FMax(0, SNaN) ==> FMax(0+0, SNaN+0) = FMax(0, QNaN) = 0",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLUseLegacyTiming, "SKL A0 needs to use escape calls to get GPU timing (and must disable preemption)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2006645518, "Disable HDC PWmerge if workload uses coherent accesses", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMaskUnmaskRegisterWriteForMBOinFlip, "WA to mask unmask the pipe_mis reg for MBO bandwidth savings.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnsureLP7WMInPSR2, "Bug#4712784: Work around to ensure LP7 is enabled for enabled Planes when in PSR2.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableL3ErrorDetectionHangOnError, "SKL A0 should not use hang on error bit (bit 9) in the L3CNTLREG (0x7034)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLGAMRepeaterBug, "WA To GAM repeater issue until B0-Step of BXT", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePooledEuFor2x6, "Enable Pooled EU feature on fused off 2x6 configs to fix another HW issue", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// struct _wa_3d

WA_DECLARE(WaStallBeforePostSyncOpOnGPGPU, "In the GPGPU pipeline, insert a PC with a CS stall before any PC with a post sync op.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceCsStallOnTimestampQuery, "Sets the CS stall bit in the pipe control that issues the timestamp query", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceCsStallOnTimestampQueryOrDepthCount, "Sets the CS stall bit in the pipe control that issues the timestamp query or depth count", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceRCPFEHangWorkaround,
           "Enable Depth Stall on every Post Sync Op if Render target Cache Flush is not enabled in same PIPE CONTROL  and  Enable Pixel score board stall if  Render target cache "
           "flush is enabled.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMSFWithNoWatermarkTSGHang, "Replace media state flush for GPGPU with pipe control", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAtomicFlushOnInterfaceDescriptor, "Add an atomic flush between interface descriptors.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHwzFlushStrDword, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSecondLevelVertexCache, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHwbClockGating, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDagRounding, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHwbRingSize, "WA_HWB_RING_SIZE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBorderColorChromaKey, "WA_BORDERCOLOR_CHROMAKEY", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMixedModeForceRead, "WA_MIXED_MODE_FORCE_READ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa4DTextureCoordinates, "WA_4D_TEXTURE_COORDINATES", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMixedModeLinear, "WA_MIXEDLINEAR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZBiasUseVtxTransform, "WA_ZBIAS_USE_TRANSFORM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAsyncMMIOBusyWait, "WA_ASYNC_MMIO_BUSY_WAIT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushGWB, "WA_FLUSH_GWB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEndSceneNoPrimitives, "WA_END_SCENE_NO_PRIMITIVES", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaConfirmHWBOOM, "WA_CONFIRM_HWB_OOM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAsyncEndSceneBPLCorrupt, "WA_ASYNC_END_SCENE_BPL_CORRUPT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFastClearContextSwitch, "WA_FASTCLEAR_CONTEXT_SWITCH", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHWBExpandOBR, "WA_HWB_EXPAND_OBR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndexVertexNOP, "WA_INDEX_VERTEX_NOP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndirectVerticesPRB, "WA_INDIRECT_VERTICES_PRB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHWBStaleSlowState, "WA_HWB_STALE_SLOWSTATE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableA2R10G10B10Target, "WA_DISABLE_A2R10G10B10_TARGET", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisbaleIndirectLoadWideMode, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZoneInitCorruption, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushGWBOnBPLReset, "Flush GWB, every time we touch BPL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOneOverW, "Workaround for 1/W silicon bug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIdleRingForSyncFlush, "Idle ring first before issue a SyncFlush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWIZSingleSubspanDispatch, "For Broadwater A0, dispatch only one subspan", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_RenderCache_OperationalFlush, "Operational flush cannot be enabled on BWG A0 [Errata BWT006]", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnable_BugFix_RCCAllocation, "BWG A-step bug fix chicken bit for rcc allocation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_Suppress_CacheableIndicator, "Suppress cacheable indicator from render command stream cannot be enabled on BWG A0 [Errata BWT010]", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_WIZUnit_ScratchSpace, "Set max scratch space as 12KB (BWG A0, Source: Michael Apodaca)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStateless_Accesses_Allowed, "Set Bit for in MMIO Register 0x7408 (BWG A0) (Source: Hitesh K. Patel)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMiSetContext_Hang, "add NOOP after MI_SET_CONTEXT; URB_FENCE must lie within a 64 byte cache line", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_StateBaseAddress_Hang, "Invalidate State Cache before programmin State Base Address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_TexturesOnlyForA0, "Disable textures that do not work correctly in A0 Silicon", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable_Trickle_Feed, "Disable trickle feed", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHWBAutoReportHead, "Disable the HWBR auto-report head pointer", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestoreInhibit, "Set bit for Restore Inhibit in MI_SET_CONTEXT on BWG", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableMTConstantReadFix, "enable fix for constant buffer reads through MT cache", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_MI_SET_CONTEXT_Hang, "WA for MI_SET_CONTEXT hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableStencilBufferTestOnStencilBufferDisable, "WA to prevent hang when STC PMA stall avoidance is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDontTurnOffCRClkInCStates, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoopHWContextLoadRegImm, "WA for hang at MI_LOAD_REGISTER_IMM during MI_SET_CONTEXT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPPGTTSteeringRegisterPresent, "WA to clear Steering Register for Gen3.5 before doing Present on display surfaces", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVSHWBug_Option1_DisableVertexCache, "VS HW bug.  HSD 300136, option 1 - Disable Vertex Cache", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_CS_URB_STATE_Hang, "Send CS_URB_STATE command to h/w twice to prevent subsequent ring hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseMediaEngineForPaging, "Use Media Engine to do paging transfers.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInitAuxBuffersToTiled, "WA for intermediate Z issue to initialize aux buffers to tiled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRenderCachePipelinedFlush, "Disable Render Cache Pipelined Flush for Cantiga/Eaglelake (set bit 8 of 0x2120)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTimedSingleVertexDispatch, "Workaround for deadlock - Enable timed dispatch of single vertex in Gen4 and later products", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFastClear, "Do not use fast depth buffer clear", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHiZ, "Disable HiZ overall for SNB A steppings", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTDisableHiZ, "DCN 787402, Gen6 Bug_DE 2877644, disable HiZ for certain non-promoted cases", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHiZMSAAPerPixelLineAAEnabled, "Gen6 Bug_DE 3046987", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFastClearYOffsetNonX4Aligned, "Sub-resources with YOffset that is not multiple of 4 can't be fast cleared - ILK sighting 3573303", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDepthStallAfterFastClear, "Depth buffer clear pass must be followed by a PIPE_CONTROL command with DEPTH_STALL bit set.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVertexShader96And128CacheEntries, "Disable use of 96 or 128 vertex shader URB/cache entries", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClampSamplerArrayIndex, "WA for clamp sampler array index - SURFTYPE_1D, SURFTYPE_2D and SURFTYPE_CUBE.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSampleSeparateStencil, "DCN787227. ILK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForce8PSThreads, "IVB HAS-Fulsim: force MaxNumThreads to 8 in 3DSTATE_PS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitWmMaxNumThreads, "SNB Ax WA to limit the maximum number of threads for WM state", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePerPixelMSAA, "Per Pixel MSAA is broken (HSD 2851051, HSD 2877632)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAlphaToCoverage1x, "Replace A2C with AlphaTest if numSamples is 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAlphaToCoverage4x, "Replace A2C with AlphaTest if numSamples is 4", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLd2dmsSurfaceArrayOfSize1, "Ld2dms should return 0's if surface is array, array size is one, and srcAddress is out of range", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAlphaToCoverageDither, "A2C Dither Enable is not supported", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForcePushConstantEvenReadLength, "force push constants to read an even number of 256 bit entries (HSD 3046567)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSQRORDClockGating, "Disable SQRORD Rejections for GT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCorrectionForCosine0, "Cosine(0.0) is not 1.0 and requires correction to pass WHQL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHeaderBypassForPSDepthOutput, "Disable header bypass for PS ouputting source depth", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceHeaderForKillPixInstructions, "Force header for all RT writes which kill pixels.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDecomposePowToLogMulExp, "Decompose IL FPOW instruction to equivalent FLOG2, FMUL, FEXP2 instructions.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSStallOnAllPipeControls, "Set CS stall on all PIPE_CONTROL commands (HSD sighting 3639613)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMultisampledArrays, "Render engine and sampler have mismatch when indexing nonzero array slice", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable128bppRTClears, "SNB WA to disable 128bpp render target clears.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsPsdHang, "limit max GS threads when rendering is enabled (HSD bug_de 3047711)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceThreadSwitchWhenUpdateMRFBeforeSend, "WA for EU dependency HW bug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushAfterPerspectiveDivideStateChange, "Non-pipelined flush after perspective divide state change (HSD sighting 3715225)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSampleFromStencil, "Wa - Cannot sample from or disable separate stencil on IVB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReadAfterWriteHazard, "Send 8 store dword commands after flush for read after write hazard (HSD Gen6 bug_de 3047871)", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMadSrc0Replicate, "WA disables replication for src0 in MAD instruction (HSD 3639565)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSamplerChannelDisables, "don't use sampler message channel disables (HSD gesher sighting 3715686)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSFCorruption, "workaround for SF corruption when polys are clipped (HSD gesher sighting 3715346)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBeforeStateCacheInvalidate, "Send 8 store dword commands after flush for read after write hazard (HSD Gen6 bug_de 3047871)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallAtEveryFourthPipecontrol, "PSD flush logic is broken on IVB. Hence the WA to send CS stall at every 4th pipecontrol", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUAVTypedWriteOverlapping, "Split any UAV write messages if they have overlapping identical U/V/R/LOD values. IVB HSD3378851.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUAVTypedReadOverwritesAllDestChannels,
           "WA for IVB HSD 3378971 Typed Surface Read and Typed Imm Atomic overwrite all destination channels regardless of execution mask", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPSInvocation, "WA for IVB HSD 3664422 PSInvocation count doesn't decrease when pixels are discarded by shader early depth test.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseOnlySIMD8UntypedRead, "Use only SIMD8 for Untyped Surface Read and Untyped Imm Atomic messages. IVB HSD bde3378886.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMscWithGS, "WA for IVB HSD 3664439 on A0 MCS unit is calculating incorrect VA when r2t is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSurface3DForceHorizontalAlignment4, "Force horizontal alignment of 4 for 3D surfaces. IVB HSD Bug_DE 3664432", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUVoffsetToZeroForLd2dms, "WA for IVB HSD 3378967 on A0 MSC resolve test shows corruption when ld2dms instruction. with u v offset not zero", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMsaaDisableMinArrayOffset, "WA for IVB HSD 3664555 on all IVB steppings.  Disable min array idnex and use address offset instead.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableAllCubeFacesForNonCubeSurfaces, "Force all cube face enables to be true for non cube surfaces. IVB HSD Bug_DE 3379081", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushStateCacheOnDepthRangeChange, "Flush state caches when Z min /max changes on GT1 only (HSD gesher sighting 3715904)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPerThreadScratchSpaceInGPGPUIncrease, "WA for IVB HSD 3664465 on A0 scratch space per GPGPU thread limit (12k bytes max) too small", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseFDP3InsteadOfFDP2, "WA for IVB HSD 3379383 - we have to use FDP3 with 0.0f in channel Z instead of FDP2 with is broken.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaApplyAbsToFrcInstruction, "WA for IVB HSD 3664897 - have to add absolute modifier for FFRC instruction destination.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForPlusInfRoundingModeFrcInstruction, "WA for IVB HSD 3665820 - mismatch in result of frc instruction in +inf rounding mode.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDsNeedMoreThan138UrbHandlesAllocated, "WA for IVB HSD 3379232 - DS must have more than 138 URB handles allocated in IVB A0.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEmulateIBFEInstrucion, "BFE signed works incorrectly.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBeforeWriteCacheFlush, "set CS stall and send dummy post sync op before flushing write cache (HSD gesher sighting 3715383)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaShaderCalculateResourceOffsets, "Calculate resource offsets in shader code for better performance (SNB, IVB)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseThreadPayloadCompression, "WA for IVB HSD 3378726. Compress thread ids in compute shader thread payload. WA for too small (16KB) ROB storage size on IVB A0.",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT(20), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableTransformedVerticesHWClipping, "Enable HW clipper in case of tranformed vertices (SNB, HSD DCN 3368671)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHiZPlanesWhenMSAAEnabled, "Disable HiZ Planes when msaa enabled via 2084[10] (Gen6 bug_de 3047992)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUnlitCentroidInterpolation, "WA for IVB HSD 3665165. The centroid interpolation is not right for unlit pixels.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMcsForSINTFormat, "WA for IVB HSD 3665244. Disable Mcs for SINT formats", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAddCallToEOTEnabled, "WA for IVB HSD 3664649 - Place call to EOT instruction at the end of shader with function calls", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignDrawScissorRectTo2x2MSAA, "Drawing rectangle and scissor rectangles must be 2x2 aligned when MSAA is enabled (Gen6 sighting 3716147)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTimestampMaskDefectiveBits, "The highest significant bits of the 1st DWORD of the Timestamp register value are frequently destroyed. (HSD gesher sighting 3716223)",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDX9MSAARasterization, "DX9 MSAA rasterization not adjusting pixel location by 0.5,0.5. (Cloned from SNB: HSD 3715757)", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZeroUnusedSampleDGradientsParameters, "Sampler LOD: 1D,2D surface LOD calculation for sample_d and sample_d_c not spec compliant.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlphaToOneOGL, "if more than 1 render target will be written and when RT write message sends src0 alpha payload, place 1.0f in pixel alpha payload.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMsaaFastClear, "ld2dms shows corruption when resolve from a texture cleared with fast clear.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMcsFastClear, "WA for IVB bug, HW hang when MCS is enabled with MRT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDummyRenderForAdderIssue, "There is an issue with a bit in an adder when coming from cold boot, need to flush pipeline via dummy blt", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaROBUnitVertexCorruption, "WA for SNB HSD 3048040 - Full flush after vertex shader enable/disable (ROB Unit Workaround)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOGLGSVertexReordering,
           "WA for IVB, BDW/CHV, SKL A0-B0 - VertexReordering for OGL GS, enables software reordering for TRIANGLESTRIP and TRIANGLESTRIP_ADJACENCY input topologies",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOGLGSVertexReorderingTriStripAdjOnly,
           "WA for BDW/CHV, SKL A0-B0 - VertexReordering for OGL GS for TRIANGLESTRIP_ADJACENCY input topology only, the same software reordering WA as WaOGLGSVertexReordering "
           "but enabled only for one topology",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvEnableSWTurbo, "WA to enable software turbo until SKL D0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvDisableTurbo, "Workaround to disable turbo on BXT A0/A1", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT, WA_COMPONENT_PWRCONS)

WA_DECLARE(WaGatherEUTimestampDispersion,
           "WA for IVB HSD - Runs a special CS kernel program with barrier opcode in order to obtain information about EU timestamp registers dispersion", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaXScaledFormatConversion, "Wrong format conversion from S/USCALED to float.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCMPInstFlagDepClearedEarly,
           "When CMP instruction has both flag and grf destination dependency clear in a flag register gets cleared early. We break SIMD16 CMP into 2 SIMD8 ones. Workaround "
           "options: Disable co-issue, which has performance implications. On compare instruction performance will reduce by 50%. This is one of the most used opcodes. Or can "
           "break SIMD16 CMP into 2 SIMD8 which also affects performance. (Cloned for HSW: HSD hswgth 3991431 & 3991361 & 3991339)",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT(50), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceUAVOnlyToFalse,
           "Force bit UAVOnly to be off. Program Rasterization number of samples to whatever is required by the app (1X/2X/4X/8X/16X) - polygon sample mask to all samples lit "
           "(exact number of bits depends on number of samples from above, example 2X = sample mask 0x3 and so on) - pixel shader dispatch mode needs to be set to \"per pixel\" - "
           "we do not program UAV only mode bit (leave it at zero) - we enable RTTIR rasterization",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlphaCompareAlwaysWhenAlphaTestDisabled, "When Alpha Test is disabled, Alpha Test Function must be COMPAREFUNCTION_ALWAYS.(Cloned from IVB: HSD 3925837)",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaScalarAtomic, "WA for HW performance optimization for faster handling of atomic appends.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVSThreadDispatchOverride, "Performance optimization - Hardware will decide which half slice the thread will dispatch.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3UseSamplerForLoadDualConstant,
           "WA to avoid L3 Constant Cache problems on IVB (HSD BUG 3799329) - use sampler in Vertex Shader for LOADDUALCONSTANT with response length == 1 or 2 (using 1 or 2 "
           "sampler sends SIMD4x2) and for response length == 4 (using 1 sampler send and SIMD8). For response length == 4 the WA is enabled only for shaders with less "
           "instruction count than specified by L3WAMaxShortVSLength.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaL3UseSamplerForVectorLoadScatter,
"WA for Apple Cascaded_Shadow_Map test to avoid L3 Constant Cache problems on IVB - it replaces LOADSCATTEREDCONSTANT instructions which are Vectors with "
"LOADSCATTEREDCONSTANT_SAMPLER instruction, which is sampler SIMD8/SIMD16 LOAD with response length 4/8. It also merges LOADSCATTEREDCONSTANT instructions differing only by "
"ConstantBufferChannel to one LOADSCATTEREDCONSTANT_SAMPLER instruction and removes SHL instruction before them, since sampler LOAD has oword granularity and SHL is not needed.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa1DSurfaceSIMD4x2ArrayIndexInRAddress,
           "SurfaceArray bit is always set in SurfaceState on IVB and HSW. Resinfo's results should be adjusted as well as sampler's address in channel parallel. For 1D surface "
           "type SIMD4x2, the array index must be placed in R address parameter instead of the V address parameter.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndexBufferOffsetOverflow, "Guarantee that the hw calculated offset into the index buffer does not overflow at draw time.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBreakSimd16TernaryInstructionsIntoSimd8, "Cannot use SIMD16 3 SRC Instruction - w/a by breaking them into 2 SIMD8's (Cloned HSD: hswgth  bde 3992063)",
           WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGSPullModelForPatchlistInputTopology, "Enable GS Pull Model for topologies with > 4 input vertices: PATCHLIST_5PATCHLIST_32", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGSSingleDispatchModeForTriangleInput,
           "HSW GT2|GT3 rev A and B is forced to work in single dispatch mode when executing TRILIST_ADJ or TRISTRIP_ADJ as an input topology.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceSIMD8ForBFIInstruction,
           "BFI instruction is forced to SIMD8 because of HW bug. If BFI is executed in SIMD16 , under controlflow, only lower 8 bits of execution mask are applied correctly.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable4x2SubspanOptimization, "Disable combining of two 2x2 subspans into a 4x2 subspan.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBreakSimd16InstWhenAccIsUsedIntoSimd8, "This Wa breaks SIMD 16 instructions intro two SIMD8 when accumulator is used explict as source or destination",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendMiFlushAfterMediaStateFlush, "Sends a MI_FLUSH after MEDIA_STATE_FLUSH.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvcCabacDistortionBasedMinQp, "Add distortion based Min QP for Cabac issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableDummyMovInGpgpuContextSave, "Execute a dummy mov at the end of Context Save.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearNotificationRegInGpgpuContextSave, "The notify counters need to be reset from SIP during context save.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGrfDepClearOnOutstandingSamplerInGpgpuContextSave, "Clearing dependency on all grf registers in case of potential pending sampler message", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStoreAcc2to9InAlign16InGpgpuContextSave, "Access to acc2 - acc9 arfs in Align16 to prevent corruption in preempted workload", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGrfDependecyClearInGpgpuContextRestore, "Clearing dependency on all grf registers in preemption context restore", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestoreFCandMSGRegistersFromUpperOword, "Restores message and flow control ARF registers in preemption context restore.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestoreFC4RegisterDW0fromDW1, "Restores fc4.0 register restore DW0 from DW1 in preemption context restore", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestoreFc0RegistersWithOffset, "Restores fc0.4 to fc0.31 register with special offset in preemption context restore.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGrfScoreboardClearInGpgpuContextSave, "Special handling for sr1 from SIP during context save/restore and masking sr0 register", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearFlowControlGpgpuContextSave, "Clears flow control registers after context save for the next thread", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearCr0SpfInGpgpuContextRestore, "Clears control register SPF value in context restore", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDbg0Register, "Don't allow to use EU arf Dbg0 register", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRSBeforeBTPoolDisable, "Disable resource streamer before disabling BT pool to fix HSW hang on GPGPU preemption (RS context does not save BT edits).",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseRSChickenFor3DMidBatchPreempt, "Don't allow Resource Streamer to stop at 3DPrim cmds when preemption is enabled (set RS_CHICKEN reg / RS_PREEMPT_DEBUG bit)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNotifRegSwapInGpGpuContextRestore, "Swap n0.0 and n0.2 registers in preemption context restore.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStoreSlmOffsetInSRDuringGpGpuPreemption,
           "SLM Offest isn't stored by H/W context during preemption, when WA is enabled gpgpu SIP kernel preserves SLM Offset during in preemption.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSampleGCToSampleLC, "WA for IVB, SAMPLE_G_C is not supported. Change to SAMPLE_LC with Lod computed from gradients.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaResetMSAAStates, "WA for SNB Q0, need to reset MSAA states at the end of every batch buffer to avoid issues in media workload", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCMPInstNullDstForcesThreadSwitch, "CMP instructions with NULL destination needs to have Thread Switch enabled (Cloned from IVB GT2 HW WA 3665996)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCMPInstNullDstBreaksR0Scoreboarding, "CMP instructions with NULL destination break R0 scoreboarding", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVSPreventFullTrackingFifo, "disable vertex cache and limit VS number of URB entries to less than 1280", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVFInvalidate, "Use PIPE_CONTROL to invalidate vertex fetch instead of VERTEX_BUFFER.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceHeaderForDualSourceBlendHi, "Force header for dual source write high message.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFixedFormatConversion, "WA for lack of support for fixed_point type on the IVB and VLV platforms", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceHSPullModel, "WA for HSW, force HS pull model", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPreventHSTessLevelsInterference, "WA for IVB, HSW, BDW: inner tess levels can interfere with outer tess levels.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidDomainShaderCacheStall, "WA for BDW: Disable domain shader cache if there are domain points involved in more than 11 triangles (hsd bdwgfx 1910089).",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndirectDispatchPredicate, "WA for predication for Indirect dispatches in compute shaders - hsd 1691333, sighting 3926330", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetTriLinearFilterForLODPreclamp, "WA for HSW, enable DX11 LOD pre-clamp mode by setting tri-linear filter quality to HIGH", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSScratchSpaceSize, "WA for HSW: Must allocate enough scratch space for 70 threads for half slice 0 and 128 threads for other half slices present in the system.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSNoWayToLimitScratchSpace, "WA for HSW: Must allocate enough scratch space for 70 threads for half slice 0 and", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInsertNopToHaltDestination, "WA for IVB/VLV, HALT jump destination should point to NOP for single program flow", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceL3Serialization, "WA for IVB/VLV, Set bit 27 of B034 to 0 to force multiple URB reads to the same cacheline to be serialized", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHizAmbiguate8x4Aligned, "WA for HSW: HiZ ambiguate passes must be 8x4 aligned for each LOD", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHizAmbiguateRequiredNonAlignedBeforeRender, "WA for HSW, HiZ ambiguate pass required on non-8x4 sections before clearing or rendering", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushWriteCachesOnMultisampleChange, "WA for BDW HSD 1897292, flush depth and render caches on Multisample change", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceTypeConvertF32To16ToAlign1, "WA for BDW HSD 1898640, type convert F32To16 is not allowed in Align16, must be done in Align1", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAdditionalMovWhenSrc1ModOnMulMach, "WA for BDW to support source modifiers on src1 when using mul/mach macro", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceMulSrc1WordToAlign1, "WA for CHV to produce only Align1 mul instructions when src1 type is :w", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoNotPushConstantsForAllPulledGSTopologies,
           "SKL, BXT: 'Dispatch GRF Start Register For URB Data' state for the GS is too small to adress GRF bigger than 15, so constants can not be pushed when more than 14 (13 "
           "in case of PrimID existance) vertex handles for pulling are input for GS",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCallForcesThreadSwitch, "WA for BDW call instruction needing Switch thread control", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaThreadSwitchAfterCall,
           "BDW, CHV, SKL, BXT: Follow every call by a dummy non-JEU and non-send instruction with a switch for both cases whether a subroutine is taken or not",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSIMD32PixelShaderDispatchFor2xMSAA, "WA to disable SIMD32 PS dispatch for BDW A0 only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WANOPBeetweenIndirectAdressingAndBranch, "WA to add NOP beetween indirect data instruction and control flow instruction.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDX9MSAAonDX10HW,
           "Wa to notify the DX9 UMD to shift the SF viewport for DX9 MSAA on DX10 HW.  Feature isn't necessary on HSW+ as the HW now supports this.  HW support exists in HSW+, "
           "but the bit is not properly context save/restored for A stepping so we need to use the traditional behavior.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInvalidateAndHDCDeadlock,
           "WA for HSW, PIPECONTROL with RO Cache Invalidation: Prior to programming a PIPECONTROL command with any of the RO cache invalidation bit set program a PIPECONTROL "
           "flush command with CS stall bit and HDC Flush bit set.  3D_STATE_BASE_ADDRESS : Prior to programming a 3D_STATE_BASE_ADDRESS command program a PIPECONTROL flush "
           "command with CS stall bit and HDC Flush bit set.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3WriteIncomplete, "WA for HSW, send a data cache flush after any draw or dispatch with a UAV.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMiUrbClearAfterMiSetContext,
           "WA for IVB & HSW - the order in which the L3Config registers and the MI_URB_CLEAR happen durring a HW context restore is incorrect.  The MI_URB_CLEAR occurs before "
           "the L3Conig registers have been restored.  Yet the L3Config registers contain the info necessary for HW to clear the correct part of the URB area.  The WA for this is "
           "to reissue the MI_URB_CLEAR after the MI_SET_CONTEXT completes since the L3Config will have been restored by that time.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceNonZeroSBEOutputAttributeCount, "Force SBE output attribute count floor to 1. Extra attribute won't be dispatched to EU if PS_EXTRA::AttributeEnable = 0;.",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaScoreboardStallBeforeStateCacheInvalidate,
           "Before PIPE_CONTROL with State Cache Invalidation Enable bit set, PIPE_CONTROL with Stall At Pixel Scoreboard  bit set, must be issued.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoNotUseMIReportPerfCount,
           "MI_REPORT_PERF_COUNT reports are lost or corrupted when other MI_REPORT_PERF_COUNT is in progress and/or other MI commands access memory. There seems to be no SW "
           "workaround proven to work in all cases. Using SRM to capture OA counters.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseOaReportTriggersForQuery, "Use OaReportTriggers instead of MI_REPORT_PERF_COUNT reports to capture OA counters for PerfQuery measurements.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceClearBindingTableEntries, "Forces clearing the HW-generated binding table entries by manually editing each entry.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitMaxPSThreadsToPhysical, "WA for HSW: limit max PS threads to physical threads in system.  70 for GT1, 140 for GT2, 280 for GT3.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitMaxHSUrbHandles, "WA for BDW: limit max HS Urb Handles programming to 184 due to FIFO size issue with DS.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaA32StatelessMessagesRequireHeader, "Need to include a header for all A32 stateless messages.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoA32ByteScatteredStatelessMessages, "Use A64 byte scattered stateless messages instead of A32 byte scattered stateless messages.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSingleSubspanDispatchOnAALinesAndPoints, "If AALines/AAPoints, HALF_SLICE_CHICKEN1 : 0E100h[10] = 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLSLMAddressDisable, "B2b atomics to the same address with a bubble in between is not bieng handled correctly in LSLMunit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPipelineFlushCoherentLines, "B2B Walkers one using BTI 255 Coherent and other using BTI 253 Non-coherent using same surface we need flush Cohrent Lines in between",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAuxCCSForMRTBlend, "Disables AUXCCS when surface is part of MRT or blend write mask scenario", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUrbAtomics, "B2B Global Atomics to the same address is extremely slow (10x slower than IVB)", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushOpOnCSStall, "Flush or PostSyncOp must be enabled with CS Stall", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPSRandomCSNotDone, "Add a PipeControl with CS Stall after every NonPipelined State belonging to WM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDCFlushOnL3CacheConfig, "Send a pipe control with DC Flush before and after setting L3ControlReg 0x7034", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(WaLimitSLMSizeTo16KBOnA0, "Limit SLM Size to 16 KB on BXT A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitSLMSizeTo8KBOnB0, "Limit SLM Size to 8 KB on BXT B0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBasicCompilationForDPInstructions,
           "Perform double precision calculations with pre-BDW specific algorithm. Since BDW-B0 platform double precision calculations will be perform with new MADM instructions.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHalfFloatSelNotAllowedWithSourceModifiers,
           "In LIR instructions that convert to floating-point sel (FSEL, FMIN, FMAX) we raise precision from 16b to 32b when some modifiers (negation or absolute values) is used "
           "on sources. Alternatively additional MOV-s could be generated to perform these operations.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLowPrecWriteRTOnlyFloat, "16-bit render target write can be used only with float data type, not int/uint.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBreakF32MixedModeIntoSimd8, "SIMD16 instruction not allowed when using mixed mode and destination type is float. Must be broken into 2 x SIMD8.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDSDualPatchMode,
           "When cull patch comes after do-min patch, and number of cull patches are high then it leads to hang. WA is to disable DS dual patch dispatch.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDispatchGRFHWIssueInGSAndHSUnit,
           "When cull patch comes after do-min patch, and number of cull patches are high then it leads to hang. WA is to disable DS dual patch dispatch.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisallow64BitImmMov, "Mov with 64 bit immediate is not allowed.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)
WA_DECLARE(WaDisallowDFImmMovWithSimd8, "Mov with DF immediate is not allowed with Simd8.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNoSrcDepSetBeforeEOTSend,
           "HW hang occurs if the send before an EOT send has NoSrcDepSet flag. WA is to disable NoSrcDepSet for these kind of send instructions.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDstSubRegNumNotAllowedWithLowPrecPacked, "Math and mixed mode instructions with 16-bit packed destination not allowed to use destination SubRegNum.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSendsSrc0DstOverlap, "sends instruction hangs if there is overlap of src0 and destination registers. So disable Sends as a WA", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSIMD16On3SrcInstr, "Do not enable using SIMD16 on 3 source instructions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHeaderRequiredOnSimd16Sample16bit, "SIMD16 send to sampler using 16-bit format must use header.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLodRequiredOnTypedMsaaUav, "In typed UAV load/store to MSAA surface, the R and LOD parameters must be specified.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(AccWrEnNotAllowedToAcc1With16bit, "Implicit write (AccWrEn) to acc1 (e.g. H1, Q3) not allowed with 16-bit data type (e.g. hf, w).", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendsSrc1Length0NotAllowed, "Src1 length of sends should not be 0.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEuBypassOnSimd16Float16, "EU bypass must not be used in SIMD16 when low precision is used.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEuBypassOnSimd16Float32, "EU bypass must not be used in SIMD16 when full precision is used.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableThreadDispatchToEU0, "EU 0 is bad in inital CHV Si. Disable thread dispatch to prevent hangs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSrc1ImmHfNotAllowed, "Src1 cannot have HF immediate.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReturnZeroforRTReadOutsidePrimitive, "RenderTarget Read should return 0 if sample is outside primitive.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCselUnsupported, "csel instruction is not supported and must not be used.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDSCaching, "Disable DS Caching to avoid a hang due to internal HW corruption of some tracking state.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSubtract1FromMaxNoOfThreads, "Subtract 1 from Max No of Threads per PSD State beacuse the PSD RTL incorrectly adds 1 to the max thread programmed.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaSendColorCalcAndBlendStateTogether,
"When either the BLEND_STATE or the CC_STATE pointer changes the driver needs to send both of them prior to the next primitive to improve blend performance in pixel backend.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaEmitVtxWhenOutVtxCntIsZero,
"Force output vtx cnt = 1 to avoid a GS hang in case static output is 0 and Control Data Header Size>0 and output vtx cnt = 0. RTL will drop partial object for all topologies.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBeforeURBVS, "Prevents a potential state thread data corruption by inserting a pipe control with CS stall bit set before any 3DSTATE_URB_VS command.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignIndexBuffer,
           "Force the end of the index buffer to be cacheline-aligned to work around a hardware bug that performs no bounds checking on accesses past the end of the index buffer "
           "when it only partially fills a cacheline.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuardbandSize, "Resize the dimensions of the guardband to -16K,+32K in both X and Y", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRCCByteSharingDisableFor3DRT, "Disable RCC Byte-Sharing for RT with Surface Format = 3D", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable4x2SubSpanOptimizationForDS, "Disable 4x2 subspan optimization for singlesample RT with depth enable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFixCentroidInterpolationRTIR16X, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIndirectDataForGPGPUWalker,
           "Indirect data usage for payloads on Media pipe is broken for A0 on BDW.To prevent hang/corruption, avoid using Indirect data for walker.",
           WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIndirectDataAndFlushGPGPUWalker, "Issue with too many entries causing a hang, solution to always use CURBE_LOAD & wrap with a MI_ATOMIC when too many entries.",
           WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIndirectDataForIndirectDispatch,
           "Indirect data usage for payloads on Media pipe is broken on BDW.To prevent hang/corruption, GPGPU walker needs to use only curbe while doing indirect dispatch",
           WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendMediaStateFlushAfterGPGPUWalker,
           "TSG is not sending the preemption down to TDG in GPGPU Walker mid-thread preemption with MMIO writes. To prevent a potential hang, this fix sends a MEDIA_STATE_FLUSH "
           "with the Flush to GO bit set after each GPGPU_WALKER.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDeferredDeallocation, "WA to DisableDeferredDeallocation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePushConstantHSGS,
           "Feature: Dereference for HS in TDL. To prevent a potential hang, a dispatch pull model must be forced for HS,GS with push constant use or just disable push constant "
           "for HS and GS.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableAllWriteChannelMask, "Pixel Corruption (X's) in main path for point sample under special conditions.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaGather4WithGreenChannelSelectOnR32G32Float,
"When issued a gather4 instruction with channel select green on R32G32_FLOAT/R32G32_UINT or R32G32_SINT Sampler will return the Red channel instead of the selected Green channel. "
"For Haswell the workaround is to use the resource swizzle .RBBB. The workaround will be applied only if gather4 is the only instruction type associated with the resource type.",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaStateBindingTableOverfetch,
"HW over fetches two cache lines of of binding table indices.  When using the resource streamer, SW needs to pad binding table pointer updates with an additional two cache lines.",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncreaseL3CreditsForVLVB0, "L3Sqc Register will be having a different value from VLVB0.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUAVCoherency, "Must use pipe control with cs stall and dc flush to maintain uav coherency if any fixed function besides PS requires UAV coherency", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAInsertNOPBetweenMathPOWDIVAnd2RegInstr, "Inserts NOP instruction between POW/FDIV instruction and following instruction that cope with 2 GRFs registers",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBeforeEnabling3DstateHS, "Issue CS Stall before enabling HS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBefore3DStateVS, "To prevent a potential hang, this fix sends a pipe_control with a pipeline flush before every 3DSTATE_VS.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendMiRsStoreDataImmBeforeRsSyncCommand,
           "To prevent a hang on HSW/BDW during preemption, the driver must send an MI_RS_STORE_DATA_IMM prior to sending a resource stream sync command (e.g. MI_RS_CONTROL).",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaB0ParityHangDisable,
           "To prevent a hang on BDW B0 when there is a Parity Error on the L3, you must explicitly disable the hang condition C0 is supposed to change this behavior.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaDisableObjectLevelPreemptionDuringUAVDrawCall,
"VF holds CS during pre-emption request. To prevent a potential hang, this fix notifies KMD of a Draw call which utilizes UAV so that they can disable Object level Pre-emption.",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushBefore3DStateConstant, "Insert pipe control flush before push constant state change.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendExtraRSGatherConstantAndRSStoreImmCmds, "Send extra RS Store Immediate, GatherConstant and 3DConstant cmds to stall CS reads until writes by RS are committed",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoPreemptionWhenBarrierEnabled, "Disable preemption if barrier is used in compute shader kernel. Only affects GT1.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionMMIOWhenBarrierEnabled, "Disable preemption if barrier is used in compute shader kernel. Uses MMIO pre-emption enable/disable.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidRCZCounterRollover, "Must send CCStatePointers at the end of a batch buffer and after 3D preemption to avoid RCZ counter rollover and HW hang", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPreemptOnArbCheckOnly, "WA for SNB HSD #3716501 - Use 32bpp WM with FBC enabled in 16bpp mode", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTSGStarvation, "WA for TSG Starvation Issue thats fixed in BDW E stepping", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInhibitPreemptionForOCLProfiling, "WA for OCL Profiling Preempt - BUG_DE 1911601", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMediaStateFlushBeforePipeControl, "GPGPU Preemption requires MSF without Flush2GO before any pipe control", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUAVDisableMinimumArrayElement,
           "HW is not able to write to an UAV with MinimumArrayElement > 0 on IVB and VLV. Workaround is to program the SurfaceOffset for every array element manually instead of "
           "HW calculating the offset.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNonSlm, "WA to avoid turning off SLM for power saving", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa4x4STCOptimizationDisable, "Disable 4x4 RCPFE-STC optimization and therefore only send one valid 4x4 to STC on 4x4 interface.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableKernelDebugFeatureInHWUsingCsDebugMode1, "WA to enable kernel debug feature in HW as CS_DEBUG_MODE1 is set to non-privileged", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnsureMemCoherencyBeforeLoadRegisterMem,
           "Any updates to the memory location exercised by MI_LOAD_REGISTER_MEM command must be ensured to be coherent in memory prior to programming of this command. This must "
           "be achieved by programming 16 dummy MI_STORE_DATA_IMM (write to scratch space) commands prior to programming of this command for pre-BDW and MI_ATOMIC (write to "
           "scratch space) with CS STALL set prior to programming of this command on BDW and CHV",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearCCStatePriorPipelineSelect,
           "Restore from a preempted GPGPU workload and the indirect states(3DSTATE_CC_STATE_POINTERS and 3DSTATE_DEPTH_STENCIL) are valid, it may be possible due to a clock "
           "gating of Fixed Function blocks, we will drop the read return of the indirect data and cause a hang in BDW+",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendDummyVFEafterPipelineSelect,
           "Need to send a dummy VFE after Pipeline select, in preemption HW signal may be stuck in a bad state and is only cleared by VFE_STATE", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendMIFLUSHBeforeVFE, "Need to send MI_FLUSH before VFE", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGunitClockGating, "WA to disable Gunit clock gating for CHV till A0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetMaskForGfxBusyness, "WA to Mask bit for Graphics Busyness for CHV till A0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInvalidateROCacheOnCxtSwitch, "WA to invalidate all RO caches for every context switch for CHV till A0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetRbWaitForAsyncFlip, "WA to set RbWait for WAIT_FOR_EVENT on async flip for CHV", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSDEUnitClockGating, "WA to disable SDE Unit clock gating for CHV", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMidBatchPreempt, "Disable 3D MidBatch preemption until validated", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePerCtxtPreemptionGranularityControl, "Disable per context preemption granularity control on SKL D0- & BXT B0-", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT(0),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePreemptionGranularityControlByUMD, "Enable preemption granularity control by UMD", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSemaphoreAndSyncFlipWait, "Disable Semaphore wait event idle message and Sync Flip/V-blank Wait For Event Power Down", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearSlmSpaceAtContextSwitch,
           "Clear SLM/URB space of L3 cache at context switch because of propagation of parity error which is caused during L3 allocation with change in SLM mode",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushCoherentL3CacheLinesAtContextSwitch, "Coherent L3 cache lines are not getting flushed during context switch which is causing issues", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPerCtxtBbInvalidateRoCaches, "Invalidate all RO caches via pipe control in per context batch buffer (as per bspec)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetPipeControlCSStallforGPGPUAndMediaWorkloads,
           "CS Stall bit must be always set when PipeControl is programmed by GPGPU and MEDIA workloads. This is to WA FFDOP Clock Gating issue.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFenceDestinationToSLM, "HDC_CHICKEN0 bit 14 must be programmed by software to 1h (Disable) to work around a LSLM unit issue.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLSQCROPERFforOCL, "L3SQCREG4 LQSC RO PERF DIS must be programmed by software to 1h (Disable) to work around a Gsync Issue in HDC  ", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)
WA_DECLARE(WaForceMinMaxGSThreadCount, "Force the minimum max threads count for GS to be 8 to prevent a potential hang or corruption.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAtomicsForceCoherency, "BDW until G1 OCL Thread Dimensions test cases fail because of a GAM Read/Write Ordering Issue", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLowPrecisionWriteRTRepData, "Disable low precision 16bit float with repcol ( Replicated Data Instruction )", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAResetN0AfterRenderTargetRead, "Add reset N- flag after render target read.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionOnSimd32, "Disable GPGPU preemption when SIMD32 kernels are used.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetDepthToArraySizeForUAV, "Set Depth to the array size for 3D Texture UAV.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndependentAlphaBlend, "Only enable independent alpha blend if needed.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPushConstantsFromBTP, "If not using RS, we must send BTP per enabled unit to trigger push constants", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPushConstantsFromMMIO, "If not using RS, we must send two MMIO registers at context create to trigger push constants at 3D primitive", WA_BUG_TYPE_SPEC,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPipeControlWithProtectedMemoryDisable, "Send Pipecontrol with Protected Memory Disable After 3D Pipeline Select and Before GPGPU Pipeline Select",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNullStateDepthBufferAsD16And2d, "WA for BDW hang when pixel shader writes to depth buffer in case of lack bound depth buffer", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// There is no software workaround possible.  This is simply an errata case
// where the HW doesn't behave as expected.
WA_DECLARE(WaAvoid16KWidthForTiledSurfaces, "WA for HW bug: Max tiled surface width can only be 16K-2", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRsInPostRestoreWaBb, "WA for CNL hang while executing RS enabled WA BB during context restore of a preempted RS enabled batch.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaInsertGSforConstInterpolatedTrailingVertex, "Insert pass-through GS when rendering a triangle strip and PS uses const interpolated attributes from trailing vertex.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(WaForceCB0ToBeZeroWhenSendingPC, "Force constant buffer 0 to be null and use constant buffer 3 instead", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(WaDefaultCrossAndSubSliceHashingForSimplePS,
           "Performance fix applied for GEN10+, when PS is simple enought cross slice hashing require to be forced to 32 x 32 and sub slice hashing to be forced to 16x16 and "
           "3DSTATE_PS_EXTRA bit has to be lit to indicate if this is a small shader",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(WaPipeControlBeforeGpgpuImplicitFlushes, "Add PIPE_CONTROL with CS stall and Render Target Cache Flush Enable bits set before non-pipelined commands in GPGPU mode.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableDSCacheWorkAround,
           "Disable DS cache in DX10/11 UMD.This is added to identify hang issues in SKL due to DS cache and to find performance impact of disabling DS cache. When this WA is "
           "enabled, performance drop is observed in 3DMark, UnigineHeaven, Thief, Lost Planet apps on SKL and CNL_D3D11_WIN10_Island_1576_LowRes test on CNL A0",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaSampleOffsetIZ, "Add load register immediate after 3DSTATE_SAMPLER_STATE command.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushHangWhenNonPipelineStateAndMarkerStalled,
           "Flush hang when Non pipeline state is being programmed when marker is stalled. Stalling Flush prior to 3DSTATE_SAMPLE_PATTERN and adding an LRR to an SVL register "
           "after 3DSTATE_SAMPLE_PATTERN resolves issue",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreBlendColorClampForR11G11B10_FLOAT, "Disable Pre-Blend color clamp for R11G11B10_FLOAT Render Target format due to HW bug from Gen11+",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDrawTrivialRejectPreemptHang, "Disable preemption on 3DPRIM commands (0x2580, bit 10) and add MI_ARB_CHECK at preemption points for CNL", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

// struct wa_PwrCons

// Temp WA
WA_DECLARE(WaPcSlpcUseBxtGucBinaryVer1219, "Temp WA on BXT to use the old guc binary until key signing issue is resolved", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// Todo: Change this workaround with a finer level workaround conditions
WA_DECLARE(WaRccHangDisableMCSUnrefined, "Disable MCS through Chicken bit. Need to refine the wa condition.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGafsUnitClkGating, "Disable GAFS unit clock gating to avoid BGF corruption which results in TDR", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaToEnableHwFixForPushConstHWBug, "WA is needed to enable HW fix for push constant issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_220856683, "Inner coverage is incorreclty ANDed with sample mask, it needs to be fixed in the EU", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

// BLC
WA_DECLARE(WaBlcOutputHighInverterPWMFreq, "WA for HSD #5262786 - Allows display engine to output high PWM frequency by not ensuring minimum 101 achievable brightness steps.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// FBC
WA_DECLARE(Wa32bppWmWithFbc, "WA for SNB HSD #3716501 - Use 32bpp WM with FBC enabled in 16bpp mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcAsynchFlipDisableFbcQueue, "WA HSD#1114573, BUN#09ww04", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisabledForOverlaySprite, "WA BUN#08ww29.1 FBC can not be enabled when Overlay/Sprite on", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcLimitedTo1MBStolenMemory, "WA FBC size limited to 1 MB stolen memory size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcOnlyForNativeModeOnLFP, "WA BUN#08ww34.1 - Enable FBC for native mode on LFP only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcOnly1to1Ratio, "CTG/ILK hw - WA BUN 2073_di5vk69m/HSD2955233 - Only use FBC compression 1:1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisableDpfdClockGating, "WA for ILK HW HSD #1114788", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisable, "WA to disable FBC feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisableDpfcClockGating, "WA for SNB HW HSD #3715402", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcFlickers, "WA for ILK HW HSD #3573465", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFbcOnFixedMuxless, "Power data shows benefit when enabling FBC during fixed muxless SG on certain platforms.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcWaitForVBlankBeforeEnable, "WaitForVBlank before enabling FBC to avoid white lines and/or hangs during S3/mode switch", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcNukeOn3DBlt, "BUN 2831472 for various FBC corruption issues IVB HW# 3925243, #3925761", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcExceedCdClockThreshold, "Disable FBC when Pixel clock exceeds 95% of CD clock to avoid corruption HSW HW# 3745290", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcCdClkFreqTooLow, "FBC may cause corruption when the pixel rate is greater than the cdclk frequency. Either increase the cdclk frequency or disable FBC.CNL:A0",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisableRleCompressionForVTD, "Disable RLE compression above 2K lines BDW HW#4394320", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsDisableOnCdClockThreshold, "Disable IPS when Pixel clock exceeds 95% of CD clock to avoid corruption HSW HW# 1912230", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcRequireStrideBeMultipleOfCompressionRatio, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2127304 ", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisableOnCompressionRatio2Or4, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2127304 ", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDisableOnNonZeroPlanePosition, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2123660", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcProgramYTileCbStrideRegister, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2124241", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcProgramLinTileCbStrideRegister, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2134903", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcInvalidateCompressedLines, "Invalidates FBC SLB on sync flips to workaround line corruption", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcTurnOffFbcWatermark, "Turns off FBC watermarks in linear and X-tile to avoid pixel underrun (HSD 2135555)", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// WA #0883 in the B-Spec
WA_DECLARE(WaFbcHighMemBwCorruptionAvoidance, "Avoid system hangs and corruption when FBC is enabled under high memory bandwidth conditions.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcWakeMemOn, "Set ARB_CTRL bit 31 FBC Memory Wake to 1'b1 for better idle power savings", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409120013, "Set the FBC chicken register bit 14 to 1'b1 to avoid screen corruption when plane size is odd for vertical and horizontal", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcTurnOffFbcWhenHyperVisorIsUsed, "https://vthsd.fm.intel.com/hsd/mpg_customer_enabling/sighting/default.aspx?sighting_id=5022343", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcNukeOnHostModify, "https://hsdes.intel.com/home/default.html#article?id=1404569388", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcPavpDisableDpfcClkGating, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2137158", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFixR32G32FloatBorderTextureAddressingMode, "Fix sampling from R32G32_FLOAT surfaces when using border texture addressing mode", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIPS, "WA to disable IPS feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsWaitForPcodeOnDisable, "WA to wait for pcode to disable IPS before disabling the display plane (HSD 4393936)", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsDisableOnAsyncFlips, "WA to disable IPS on asyc flips to improve frame rates in 3D apps.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrExitBlockedOnFbcNuke, "W/A WaFbcNukeOn3DBlt prevents PSR from exiting self refresh", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrDisableDpfcClkGating, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1945614", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvGtFreq200MhzMultiple, "W/A Driver to make sure requested a GT freq is multiple of 200Mhz", "GT hang", WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvBringDownFreqInRc6, "W/A Driver to set RPe when enters RC6", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRSDisableOn8504CorruptionDetected, "Workaround to disable RC6 when aspen2a attack is detected ", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipDisplayPowerGating, "W/A to skip Display Power Gating for Bayley Bay for Sleep/Hibernate", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcEnableDuringAeroModeOnly, "Enable FBC only in Win7 Aero mode, otherwise disabled. Addresses various FBC H/W issues on IVB.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcDontLimitCfbAllocationTo2K, "Limit FBC compressed buffer allocation to 2K lines from HSW B0+.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// CxSR
WA_DECLARE(WaOvlSpriteCxSR, "Send Overlay and Sprite events for CxSR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHpllOffDuringSr, "Decides whether to disable HPLL Off During Self Refresh Mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisable, "WA to disable CxSR feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRUseFixedWmark, "WA for using a fixed watermark for Display SR watermarks", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSROnAndOffForVistaCursorSupport,
           "WA for temporarily disabling and then re-enableing self-refresh for Vista when the cursor plane is getting enabled.  Refer to Crestline HSD #306884.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisableDparbClockGating, "WA for ILK HW HSD #1114564 - Screen goes black shortly after booting into windows with CxSR enabled", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisableHpllPowerDownForMedia, "BUN# BUN08WW15.  WA to disable HPLL shutdown while running Media clip", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisableFBCWaterMark, "WA for ILK - Display Flicker and Corruption seen with CxSR + FBC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRLimitFBCWaterMark, "WA for ILK HW HSD #1114471 - Display Flicker and Corruption seen with CxSR + FBC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(waCxSRLimitFifo, "WA for ILK C1 - Display Flicker and Corruption seen with CxSR + FBC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisableDparbFix, "WA to disable DPARB fix on ILK C1 (HSD#3573130)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDelayFrameStart,
           "BUN# 08WW5. During SR with HPLL power down enabled, default framestart time is not sufficient for HPLL to lock up. So, framestart is delayed by 2 more lines.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEmiBurstSizeMitigation, "WA for Toshiba for EMI mitigation (Cantiga Hardware HSD #3218358)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRDisableLp2Watermarks, "Disable LP2 watermarks all the time.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCxSRWmLatencyUnitIdentity, "On HSW B+ SKU's, the latency field is doubled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// Render Geyserville Features
WA_DECLARE(WaSyncFlushWaitOnSyncFlushBit, "WA for Sync Flush with RS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrUseSwCursor, "WA use SW cursor instesad of hw cursor for PSR.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseSwCursorInCommandMode, "WA use SW cursor instesad of hw cursor for Command Mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrDisableFbcAndIps, "WA - Hardware PSR disable FBC and IPS.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrForceUseLinkDisableMode, "WA - Forcibily Use Link Disable Mode for PSR.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRS2RenderRegReadHangBug, "WA for render register read HW hang in RS2 state.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsForcewakeWaitTC0, "WA to add wait for Thread C0 after setting forcewake bit to allow HW to fully exit RC6 state. Gesher Sighting# 3716542", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsForcewakeDelayAckPoll, "WA to delay the forcewake ack regsiter poll to avoid hardware hang Gen9LPBug_DE #2124970", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsForcewakeAddDelayForAck, "WA to add delay between forcewake and ack register to solve hardware issue- ack write is blocked from hardware for unknown reason",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsForcewakeAddExtendedDelayForAck, "WA to increase the retry count to wait for the ACK which takes longer than expected time to arrive", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMarkerFlow, "Disable marker flow", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMarkerFlow2, "Disable marker flow (ELK/GHAL)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsConsecutiveOptimizedWrite, "WA to apply long term Force Wake for the four consecutive writes to the Execlist Scheduler", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsUseTimeoutMode, "Use timeout mode instead of EI mode for RC6 promotion", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvAxSteppingRegisters, "Different registers are read in Turbo for different steppings", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvHighRingFreqScalingForUlt, "Use Ring Freq Scaling Factor 3.0 for ULT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsDontPollForAckOnClearingFWBits, "WA for VLV where driver shouldnt poll and wait for acknowlededge while doing an unforcewake in multithreaded scenario",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRC6PavpDisableDuringKeyExchange, "WA to disable RC6 during PAVP key exchange, otherwise h/w hang on wake if unsolicited attack occurred", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvLimitCpuTurboInRp0, "When Gfx is in RP0, do not allow CPU to go to turbo range", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDPSTHistogramErrorTolerance, "WA to allow enabling DPST if pixel count in histogram is <= of total pixels for resolution", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsDisplayPMReq, "Wa to set 0x45280[2:0]=7 if all planes are off.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsPkgCStateDisplayPMReq, "Wa to set 0x42080[14]=1 before all planes are off.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsRCSIdleBlockedInPSMI, "Wa to set 0x2054=0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsForceSingleThreadFW, "Use Single Thread Froce Wake Algorithm when Force Wake is set to Multi-threaded mode in HW.  Sighting was found in SV OS.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsDisableDecoupledMMIO, "Disable decoupled MMIO mechanism and use regular SW forcewake for MMIO register access because of slowness.", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsClearFWBitsAtFLR, "Initialize by clearing all FW bits when driver loads before setting any forcewake request.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSyncSameMMIORegAccess, "Synchronization fix for System hang when two cores try to use same MMIO Register", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_PWRCONS)

WA_DECLARE(WaRsDoubleRc6WrlWithCoarsePowerGating, "Double RC6 WRL when Coarse Power Gating is Enabled", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_PWRCONS)

WA_DECLARE(WaRsDisableCoarsePowerGating, "Disable coarse power gating for GT4 until GT F0 stepping.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsDisableRenderPowerGating, "Disable render engine power gating to workaround GVFSM hang during 4k video playback.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipRC6Enable, "Never Enable RC6 for DG2-256-A0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_PWRCONS)

WA_DECLARE(WaFidMismatch, "Disable PwrCons Features RC6 and Turbo which require Punit interaction if FID mismatch.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDpstDisableDlcdGating, "Disable DLCDunit Gating  as a WA for issue that Guardband interupt status bit enabled sporadically when Guardband interupt enabled.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsEnableOutsideOfVblankRegion,
           "Enforce IPS enable to be outsite VBLANK to workaround corruption seen when the primary plane is enabled/disabled at the same time that IPS is enabled",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsEnableOnMediaPlaybackOnly,
           "There is currently a power inversion problem with IPS. Power savings with IPS is seen only in media workloads. Enable IPS during media playback only as a workaround.",
           "Power inversion", WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIpsDisableOnPaletteAccess,
           "There is a hardware hang when split gamma mode is enabled and pipe gamma/palette data is accessed while IPS is enabled. This workaround disables IPS before accessing "
           "the gamma/palette registers in split gamma mode.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// General
WA_DECLARE(WaUsePipeAFlipTimestamp, "WA to use 7004C as timestamp for ILK A Stepping WA", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTurboEnergyCounterMask, "Energy counters bits are changed from ILK C0.  Wa flag is to use old values on A and B stepping.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRc6Ppgtt, "WA to prevent page table error when RC6 and PPGTT are both enabled at the same time.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLaceIEModeLUT, "Use LUT mode of LACE image enhancement as multiplier mode is not supported.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLaceRAMGatedClockForLPDSTAutoIndexing, "WA to use RAM-gated clock instead of FCN-gated clock to fix LDPST auto-index increment.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLaceIEWriteDuringPSR, "WA to explicitly exit PSR as LACE IE writes do not trigger in frame update when in PSR.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePwrmtrEvent, "WA to disable PWMTR event 16 and 17 for CHV till A0.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDPSTWhenPipeBandCActive, "Disable DPST when pipe B and C are active", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipWOPCMSetupPavp, "WA to skip WOPCM setup by CoreU.  This w/a, when enabled, skips writing the secure storage offset to PAVP register", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableTiledResourceTranslationTables, "WA to support Tiled Resource Translation Tables.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct _wa_Core

WA_DECLARE(WaDisableCpClockGating, "WA_MGM_DISABLE_CP_CLOCK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableReorderBuffer, "WA_DISABLE_REORDER_BUFFER", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableL2CacheClockGating, "WA_DISABLE_L2CACHE_CLOCK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLowPriorityGracePeriodDisable, "WA_LOW_PRIORITY_GRACE_PERIOD_DISABLE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMiBatchBuffer, "WA_SDG_MI_BATCHBUFFER", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBlueCorruption, "WA_MGM_BLUE_CORRUPTION", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClockGatingDisable, "WA_CLOCK_GATING_DISABLE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNearestTexelRound, "WA_DISABLE_NEAREST_TEXEL_ROUND", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFBCSetupUseRing, "Work around for enabling FBC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFBCSetStopCompOnModify, "WA for setting Bit 15 in FBC_CONTROL Register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFBCDisablePerAlvRev, "WA for disabling FBC on certain Alviso Revisions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFBCWaitForVblankOnPlaneState, "WA to wait for one Vblank and enable/disable FBC when Display Plane event occurs", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFBCPlanePipeSizeMismatch, "WA to Disable FBC if plane size is not equal to pipe size", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushGWBBeforeReads, "WA for flushing GWB before any memory read updated by HW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSnoopOnCacheWriteCyl, "Wa to disable snoop on cachable write cycle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable36BitPhysAddress, "Wa to disable 36 bit physical address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUpdateOnCacheLineBoundary, "Wa to pad memory so updates occur on cache line boundaries.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUpdateBCSOnCacheLineBoundary, "Wa to pad memory so updates in BCS RING occur on cache line boundaries.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCSUnitClockGating, "Wa to disable clock gating in CS unit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePhysAddrForMiInstr, "Wa to enable physical address for MI instruction", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_Disable_C0_Fix_For_Req_Perf, "Wa to Disable Crestline C0 fix for requests performance", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCrClkThrottlingDuringC2, "Wa to Disable BL_B CR CLK Throttling during C2 power state", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearRingBufHeadRegAtInit, "WA for CTG Ring buffer head address being written with ring address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForcePhysAddrForMiStoreDword, "WA for LKP/CAL/BW, need MI store dword to always physical address.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisIndStatePointersForSubmit, "WA which sets Indirect State Pointers Disable bit in MI_FLUSH for KMD submits", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDpst4DIETMultiplicativeMode, "WA for DPST4 DIET multiplicative mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMediaReset, "WA for media reset disable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRenderResetOnly, "WA for resetting Render only on ILK.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDmaBufferPadding, "WA for DMA buffers to have a certain amount of padding at the bottom based on platform", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAGPUResetPCIRead, "WA for using PCI Read and Write on a Render\Media reset.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInitStopRenderWatchdogCounter, "WA to stop the initially running main engine watchdog counter", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMediaResetMainRingCleanup, "WA for media reset: main engine ring does not reset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVcpClkGateDisableForMediaReset, "WA to disable VCP unit clock gating before media reset, and re-enable after.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVfeClockGating, "WA to disable VFE clock gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEmUnitClockGating, "WA to disable EM unit clock gating. ILK HW DCN 2378545", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableStcUnitClockGating, "WA to disable STCunit clock gating. ILK HW DCN 2378378", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMtmUnitClockGating, "WA to disable MTM unit clock gating. ILK HW DCN 2379187", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHizUnitClockGating, "WA to disable Hiz unit clock gating. ILK HW DCN 2379381", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSamplerL2L1BandwidthPerformance, "WA to disable Sampler L2-L1 Bandwidth Performance ILK HW DCN 2378899", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTDSandwichDispatchMode, "WA to disable sandwiching of threads by TD. ILK DW DCN 2379515", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNonLRAReplacementPolicy, "WA to disable LRA replacement policy by STCUnit. ILK DW DCN 2378954, 2379200", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCZMUnitClockGating, "WA to disable RCZ unit clock gating ILK HW DCN 2379651, 2379638", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVS0MUnitClockGating, "WA to disable VS0 unit clock gating ILK HW DCN 2379726", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSFMUnitClockGating, "WA to disable SF  unit clock gating ILK HW DCN 2379727", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaIlkMariUnitOverrun,
"Set of WAs for ILK Aero (and XP) hang - until A1. Set debug registers for unit level EU mask mariunit and urbunit clk disable. See ILK HW sighting 1114059 for details.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIlkFlushAfterMiSetContext, "WA to issue a flush after set context to avoid a HW race condition. ILK HW sighting:", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoNotInhibitDepthCacheFlush, "WA to not use depth cache flush inhibit bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPipeControlISCFlushDisable, "WA to not use ISC flush disable instead use MI_FLUSH HW bug: 2379980", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSVSMUnitClockGating, "WA Disable SVSM unit clock gating ILK HW bug 2379811 and BSpec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoNotUseSingleThreadGSMode, "WA to set minimum GS threads number to 2 {b2379894}", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushBeforeGSDisabled, "DCN702442 A pipeline flush must occur before clearing the GS Enable if the GS Enable was set on the previous 3DSTATE_PIPELINED_POINTERS",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHiZNonPromoted, "Disable HiZ when in non-promoted mode.  DCN-702590, HSD-2380094", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoCubeCornerAddressMode, "ILK WA, SURFACE_STATE 'Cube Map Corner Mode' doesn't work with AVERAGE set on ILK A0/A1.  Should work on B0+", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIlkEnableDisableSuspendFlush, "To enable and disable Suspend Flush before and after Set context.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestrictURBWriteMsgLength, "Restrict URB_WRITE msg length to be lesser or equal than to 9HWORDs. ILK A/B/C0, HW 2380247, DCN786959", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableConstantCacheDualScattered, "Disable constant cache for dual and scattered messages (Gen6 3046494)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableConstantCache, "Disable constant cache for GT1 until Gen6 B1 ( 3046984 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoPipelinedURBFenceChange, "Don't allow pipelined URB_FENCE commands by placing MI_FLUSH in front and dummy PRIM and second URB_FENCE after  ILK sighting 3573145.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableStcLraEviction, "Set STC Eviction policy in MI_CACHE_MODE_0 to Non-LRA ( 3047068 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPipelinedStateWithPsPushConstants, "send a pipelined state whenever 3DSTATE_CONSTANT_PS is sent (gesher sighting 3639897)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGsDwordScatteredWrites, "disable scattered dword write for GS svbi's ( 3047402 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushStateCacheOnViewportScissorEnable, "flush state cache when viewport or scissor enable state goes from disabled to enabled ( 3047435 )", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendAllDepthState, "Send all 4 depth states if any dirty for IVB.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallPriorToDepthState, "Send CS_STALL with post sync op prior to any depth state.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDepthStallAfterAnyPSState, "Issue depth stall after any ps state.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPipeControlBeforePushConstantUpdate, "send PIPE_CONTROL before push constant update for XP only ( 3925260 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPixelShaderKillPixelHang, "reduce thread count when pixel shader kill pixel is enabled (IVB sighting 3925401 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDepthBiasCsStall, "CS stall whenever any depth bias state changes (IVB sighting 3925501 )", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaValign2For96bppFormats, "VALIGN_2 only for 96bpp formats.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaValign2ForR8G8B8UINTFormat, "sampler format decoding error in HW for this particular format double fetching is happening, WA is to use VALIGN_2 instead of VALIGN_4",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushBefore3DPrimIfTopologyFilterEnabled, "Send PIPE_CONTROL with posy-sync op before every 3dprim if topology filter is enabled.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT(0.5), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDummyRenderForAdderIssueXP, "Issue a dummy render for 3d pipeline after comming back from 0 volts.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaB2BPipeControlFlush, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitGsUrbToTop256kb, "GS can only occupy top 256kb of URB.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT(1), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePSDDualDispatchEnable,
           "When tessellation is enabled, set MMIO 0x0E100 and 0x0F100 to 0x80008 (PSD Single Dispatch Port Enable) to avoid hang. This is for GT1 only.(IVB bug_de 3925871). This "
           "is also for VLV/VLVT (bug_de 261436).",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSystemThreadCacheFlushEnabled, "force data cache flush to make sure that all data was written to data port during kernel debug cycle", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVSRefCountFullforceMissDisable, "A HSW bug #3992601 that needs VS_REFERENCE_COUNT_FULL_FORCE_MISS_ENABLE bit to be disabled in all HSW and BDW steppings.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(20), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDSRefCountFullforceMissDisable, "A BDW bug that needs DS_REFERENCE_COUNT_FULL_FORCE_MISS_ENABLE bit to be disabled in all BDW steppings.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT(20), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSampleCChickenBitEnable, "HSD: 3246385. Starting with B0, we can set this bit to improve sample c perf.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidPMAStall, "HSW HSD: 3246426. Starting with D0.  BDW HSD:  1897031.  Starting with A0.  Avoids PMA stall.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT(60),
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePixelBackendOptimization, "Disables this optimization and therefore only one valid sub-span is sent to RCZ on the 4X2 interface.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetCacheModeForVLV, "For VLV Pixel Backend sub-span collection Optimization is disabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGunitPFIClkGating, "Gunit Clock gating disabled for Connected standby", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGtWakeFifoManagement, "Enables Wake Fifo Managment on Mmio writes for VLV", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGsvRC0ResidencyMethod, "Enables RC0 Residency WA for turbo on VLV", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseMediaScratchRegister, "On VLV FulSim use of Render Scratch register in Read after Write Hazard results in Hang so use media scratch register", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsdDispatchEnable, "Makes PSD dispatch on port 0 only compared to port 0,1 when disabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableGunitDisplayInterruptMask, "Enable the GUnit mask for forwarding the display interrupts to GT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDividePSInvocationCountBy4, "Divide PS INVOCATION COUNT counter by 4 to get correct number of PS invocations.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSbeConservativeCacheMode, "Set SBE Cache Mode to conservative", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaCPUPushConstants,
"Create push constant buffers with CPU instead of resource streamer gather. Hang in some cases when using gather buffers. Seen on Far Cry 2 and Splinter Cell Conviction.",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidPMAStallA0Conditionals, "Avoids PMA stall. BDW A0 Specific workarounds. BDW HSD: 1898690, 1903626 and more in BSpec.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseOnlySIMD8PixelShaderDispatchForMSAA, "Restrictions on dispatch modes with multisampling - cannot enable SIMD8 and SIMD16 together", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendLRITwice,
           "Program MI_LOAD_REGISTER_IMM command twice when exercising non-privilege register writes. OR Ensure all dwords of MI_LOAD_REGISTER_IMM command including header of the "
           "command gets programmed in a single cacheline (64B).",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidStcPMAStall, "SKL HSD: 731063. Starting with A0.  Avoids stencil PMA stall.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT(60), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidStcPMAStallShaderFiltering, "Filter shaders allowed to use WaAvoidStcPMAStall.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct __wa_KMD_render

WA_DECLARE(WaHDCL3Deadlock, "HDC not sending ack as L3 fifo has some cycles which it is waiting to complete.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIommuPendingInvalidationHang,
           "Queue based Invalidation is in progress, IDLE msg comes from CS to GAM. GAM will abandon the invalidation flow and after that both HDC and GAM hangs.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIndexBufferBoundsCheck, "WA for Index buffer: When index buffer is NULL. HW doesn't do bound check resulting into DX10 WHQL issue.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMediaResetBeforeFullReset, "WA for media reset: main engine ring does not reset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableOverlayDSQualityFix, "WA is turned on/off via Registry key.  Some vendors do not want fix because of CPU utilization increase", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEUInstructionPrefetch, "Disable Eu prefetch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSpriteRegisterUpdateViaMMIO, "Sprite / Display register write via LRI is broken until C0. See ILK HW sighting 1114190", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignMIReportPerfCount, "Align MI_REPORT_PERF_COUNT command to lie within 64 bytes.  See ILK HW bug 2380048", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableASModeReplayFifo, "Disable AS mode replay FIFOs that are enabled by default in non-AS mode and degrading performance.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePAVPLiteByPAVPCOverwrite, "WA for bad BIOSes where they don't enable PAVP by default. WA to enable PAVPC by writing to it.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaPAVPReadNonExistentDisplayRegister, "WA for display bus being corrupted prior to PAVP register read of 31034", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaPAVPPreventUnsolicitedAttackDetection, "WA for when HDCP is disabled or an output port is enabled while PAVP session is active", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaPavpClearAppIdRegisterDueToError, "No WA actually exists, but flag the condition for IVB pre C1  HSD 3665378", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaEnableSpriteBUpdateForUnderflowFix,
           "Fix an underflow that happens when moving sprite between pipe A/B and also from dual pipe to single pipe. See SW bug 2561712, CTG HW sighting 3404023.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAWakeVCRDuringCSProtectionOnAndOffReq, "WA for VLV HSD 4600092", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WADisplayTriggerAESKeyExpansion, "WA for VLV HSD 4600040", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSpriteDestColorKey, "Wa to disable Dest color key when display plane is off. This WA for a bug in HW (ILK s1114430)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableD3D9OverlayScaling, "Wa to disable D3D9Overlay scaling for G45 family(CTG/ELK)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignBltUpdateGttCmdHeader, "Wa for blitter MI_UPDATE_GTT command header alignment.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMediaResetSpecialSequence, "Wa for a hw issue with Media Reset requiring a special reset sequence", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWakeUp3DForRs2, "WA to issue MI_SET_CONTEXT to make CCID valid to allow Rs2 to kick in Switchable gfx mode. ILK HW s3573446.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisplayFlipAWaitAFlipBWaitB, "WA to fix Display Flip Issue. This WA will enforce Display FlipA, WaitA, FlipB, WaitB sequence.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInsertFlushBetween3DOverlappingBlts, "Wa to insert Flush between consecutive overlapping blts (HSD: 3527548)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRc6OnWaitForEvent, "WA to disable Rs2 on Wait for event in the RCS. IVB A0 HW: 3378975.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableAllByteWritesForLRI, "WA to enable all bytes. Using byte enables causes a hang on IVB A0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlwaysClearIndirectStatePointersDisable, "WA to always keep ISPDisable as false. IVB A0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLoadDummyCB2, "WA to send dummy CB^2 on pre SNB D0 steppings, else Clear Buffer will cause HW hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableLRIPostedOverrideBit, "WA for IVB bug 3664435.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3RowRedundancyUnavailable, "L3 row redundancy not available to driver since being used by BIOS for IVB A0 WA.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3ErrorRegistersInHwContext, "L3 error registers are stored in HW context (which complicates SW's L3 row reconfiguration ability).", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAdditionalMiUserIntCmdNeeded, "WA to add additional MI_USER_INTERRUPT command for Lateral BLTs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaPSMIHandlerSemaphore,
"A Semaphore req. for PSMI handler to avoid interference in critical routines (e.g. PAVP Key Exchange) https://vthsd.fm.intel.com/hsd/pcgsw/#rcr/default.aspx?rcr_id=1023900",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTerminatePAVPSessionsOnSoCS0ixEntry, "WA to terminate all alive PAVP sessions while entering S0ix in SOCs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInjectFlushInB2BFastCopyBlts,
           "WA to inject a MI_FLUSH in back-to-back Fast Copy BLTs case where src/dest are coming as same. FastCopy(X,Y), MI_FLUSH, FastCopy(Y,Z) "
           "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2119877",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAllowAsyncMMIOFlips, "Enable Async MMIO flips for display emulation team, because any CS flips during boot blocks their display validation", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCtxRestoreArbitration, "WA is to add MI_ARB_OFF in INDIRECT_CTXT buffer and MI_ARB_ON in PER_CTXT to prevent preemption during context restore",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableWaBBUse, "WA to disable WA_BB use in specific SKUs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableOcaLogging, "Disable OCA logging since new features development isn't yet handled in OCA which causes TDR/BSOD (To be used for Gen8+ platforms)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceL3LlcCoherencyInDescriptor, "BSpec Restriction for BDW context descriptor programming see Context Descriptor Format in the Bspec", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPipeControlUpperDwordCorruption, "WA a potential HW issue where the upper DWORD of a PIPECONTROL dword write is corrupted", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseGfxModeFor3DPreemptionGranularity, "Use GFX_MODE register for 3d preemption granularity", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUsePseudoL3AddressingScheme, "WA to switch to pseudo LRU scheme for L3 addressing due to L3 related bug.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUmdToEnableL3CycleThruZTLB, "WA to allow UMD to route L3 cycles through p1 Z TLB.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUmdToModifySamplerMode, "WA to allow UMD to dynamically program sampler mode based on the API.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDToModifyHDCChicken1, "WA to allow UMD to dynamically program HDC Chicken1 register for performance gain.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDToModifyHalfSliceChicken2,
           "WA to allow UMD to dynamically program ('Small PL Lossless Fix Enable' in) 'Chicken bit for Command Slice Register 2' for performance gain.", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDToModifyHalfSliceChicken7,
           "WA to allow UMD to dynamically program ('Trilinear Filter Quality Mode' in) 'Chicken bit for Sampler register 2' for performance gain.", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEnableStateCacheRedirectToCS,
           "WA to program the redirection of the state cache from the Unified/RO sections of the L3 to the CS Command buffer section Reg:SLICE_COMMON_ECO_CHICKEN1(731Ch) .",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDToModify3DPrimitiveExtParam, "WA to allow UMD to program 3D primitive extended parameters.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaBindlessSamplerStateBoundsCheckingDefeature,
           "WA for Bindless Samplers to defeature bounds checking for Bindless Sampler State Heap. Bounds check is at wrong granularity.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableGatherAtSetShaderCommonSlice, "WA to reset Disable Gather at Set Shader Common Slice bit in COMMON_SLICE_CHICKEN2 register for every context submitted.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAvoidBackToBackIdAndCurbeCommandsViaPipeControl,
           "WA to add a stalling PC in WA BB to avoid back to back interface_desc_load or curbe_load commands that can occur due to re-submission of a preempted context",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(FtrEnableFastAnisoL1BankingFix, "WA to enable HW L1 Banking fix that allows aniso to operate at full sample rate.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaDisableRc6Wabb, "WA to disallow use of RC6 WA BB due to HW bug", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableBlitterFbcTracking, "WA to disable the Blitter FBC front buffer modification tracking. Instead nuke the compressed buffer.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableI2mCycleOnWRPort, "WA to disable I2m cycle going on WR port", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaThrottleEUPerfToAvoidTDBackPressure, "WA for a hang issue that requires throttling EU performace to 12.5% to avoid back pressure to thread dispatch", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT, WA_COMPONENT_KMD)

WA_DECLARE(
WaDisableEnhancedSBEVertexCaching,
"WA forTDS handle reallocation getting dropped by SDE, which may result in PS attribute corruption. Disable enhanced SBE vertex caching in COMMON_SLICE_CHICKEN2 offset.",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaToggleSubsliceEnableBitsToClearCam, "WA to toggle PM mode sub-slice enable bits to clear CAM to avoid GPGPU preemptio hang", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableReplayBufferBankArbitrationOptimization, "WA to disable replay buffer destination buffer arbitration optimization", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPerDmaStallRcsForPocsCompletion, "WA to stall RCS, using sem_wait until POCS completion, at the end of every POSH enabled DMA submission.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPerDmaStallPocsForRcsCompletion, "WA to stall POCS, using sem_wait until RCS completion, at the end of every POSH enabled DMA submission.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaSarbUnitClockGatingDisable, "WA to disable Sarbunit Clock Gating.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604370585, "WA to disable hold of push constant dereference.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDToControlCoherency, "WA to allow UMD to control coherency.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaWatchDogTimerEnabledByUMD, "WA to allow UMD to enable watchdong timer.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604366864, "WA to HW issue if 3DSTATE_PTBR_PAGE_POOL_BASE_ADDRESS is executed within 256 clocks after the context restore is done", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1405779004, "Clock gating Bug in MSC for PTBR feature", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_220166154, "HW Issue with VTD mode ON and IOTLB invlidation", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaProgramMgsrForL3BankSpecificMmioReads, "Shadow Reg 119 (MGSR) needs to be programmed appropriately to get the correct reads from specific L3 banks related MMIOs",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1406463099, "Disable the TLB miss allocate stall Perf fix", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableNewGucInterface, "Disable New GUC Interface", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableEncryptedSysInfo, "Disable Encrypted SysInfo", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDAccessToCullBits, "Whitelist MMIO that controls cull bits with R/W access but only for non-release builds.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDAccessToCommonSliceChicken3, "Allow-list access to Common Slice Chicken register 3 to control State Cache Performance fix", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaWarhammerCorruption, "Temporary Workaround to program PSS_MODE2 register to fix warhead corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaAllowKmdNullPresent, "Allow null submission for present request. UMD will do explcit present via BCS/Copy Engine", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaShrinkIdiSq, "Shrink the IDI SQ for platforms where this gives a performance gain", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012541948, "After programming push constant alloc command immediately program push constant command(ZERO length)", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

// ------ KMD WAs only above this line -------

WA_DECLARE(WaSkip16thBindingTableIndices, "DCN702073. ILK B0 WA: Avoiding unintended sampling of non-URB SFID messages.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceRenderingEnabled, "DCN702074. ILK All steps HW WA: Force rendering enabled {s1114045}", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableFFSyncWithOutAllocate, "DCN855159. ILK C2 allows FFSync w/o allocate.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDiscardAdjacency, "DCN702400 (HW 2380059, ILK A0/A1/B0 WA}. Discard adjacency is broken and should not be set {s1114254}", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDePipelineReadFlushes, "ILK B0 HW bug: 2380201 - DX10 SDK apps cause hardware hang when rendering menu objects", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableBindingTableSamplerCountPrefetch, "Disable BindTableEntryCount and SamplerCount used in prefetch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncorrectSampleInfoSampleCount, "HW Bug 2877676 SampleInfo returns incorrect sample count.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncorrectSampleInfoPaletteIndex, "HW Bug 2877676 SampleInfo returns incorrect palette index.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCubesAreNot2DArray, "Memory layout of cubes is not same as 2D array", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushOnMaxNumberClipperThreadsChange, "WA to insert MI_FLUSH when max number of clipper threads change - DCN726186", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableForceWakeForRc6WaBb, "Wa to enable RC6 Wa Batch buffer by performing Force-wake during each execlist port submit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDuplicateMiDisplayFlip, "MI_WAIT_FOR_EVENT does not wait for async flip, suggested workaround is to duplicate MI_DISPLAY_FLIP command to force implicit wait",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreservingDenormsInPixelBackend, "only DX10 needs to preserve denorms", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSampleLPerformance, "replace sample_l with sample when possible to increase sampler performance", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWGFVertexBufferMaxIndex, "WA to apply buffer WA logic to vertex buffers due to improper HW support for MaxIndex \ Instance counts", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNullVertexBufferWhenZeroSize, "Set NullVertexBuffer bit when vertex buffer size is zero", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushBetweenBindingTablePointers, "WA to insert MI_FLUSH between BTP - DCN726399", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHizCorruptionRenderArbWriteMaskDisable,
           "ILK s1114684: WA to fix blocky corruption in Hiz by setting render arbiter to not mask write requests if the write data queue is full.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFastClearFor16bpp, "WA to disable fast clears if format is 16bpp and width of lod 0 is not multiple of 16", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetNoOverlapBltCaps, "WA to not allow overlapping blt in caps", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable128bppCopyBlt, "SNB WA to disable 128bpp copy blt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceWindowerMinThreadsTo6, "SNB A0 WA: Adjusts the windower minimum thread count to 6", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUsePostSyncOpWithROCacheFlushPipeControl,
           "HW Bug 2850330: Whenever a PIPE_CONTROL is sent with RO cache flush only, post-sync op must be set to something other than 0.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRHWOOptimization, "HW Bug 2878194: Disable read-hit-write optimization when depth buffer format is d24_s8", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitMaxGSThreads, "HW Bug 2877765 and 3639703: Limit GS threads to 29 (big GT)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaToggleDepthStallOnDepthWrite, "HW Bug 2944684: Send an extra PIPE_CONTROL with no DepthStallEnable whenever DepthStallEnable is set", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVertexShaderPushConstants, "HW Bug 2944932: Disables Vertex shader push constants (CURBE)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePixelShaderPushConstants, "HW Bug 2944932: Disables Pixel shader push constants (CURBE)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDropZEvictions, "Drop Z evictions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitEusTo5ThreadsWhenSystemThreadPresent, "ILK Sighting 1114964 - system thread hangs when threadid is 5", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCZWatermark, "Disable RCZ Watermark (ironlake HSD 3573030)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHizNoDepthTestWrite, "Disable HiZ under certain conditions (Ironlake 3573054)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVfFix, "Disable C1 VF hw fix (Ironlake 3573128)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTlbInvalidateStoreDataAfter, "After pipecontrol with TLB invalidate set, need 6 store data commands, then another pipecontrol", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTlbInvalidateStoreDataBefore, "Before pipecontrol with TLB invalidate set, need 2 store data commands", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAsyncFlipPerfMode, "Must set 209c bit 14 to 1, disabling async flip performance mode (used to fix multiple issues).", WA_BUG_TYPE_SPEC,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableUrbDataShuffleMode, "HW Bug 2877845: Must set 2090 bit 6 to 1, enabling URB data shuffle mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableBlbUnitClkGating, "HW Bug 2877578: Must set 9400 bit 5 to 1, Disabling BLB unit clock gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitAllowedPsThreadDependencies, "HW Bug 2877810: Must set 20d4 bit 15:12 to 0, limiting max allowed PS thread dependencies", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSurfaceStateBaseDwordAlignment, "HW Bug 2851103: Surface state base address must be dword aligned", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVcsBcsQwordWriteCacheLineAlignment, "HW Bug 2877845, 2878101: address for qword writes in MI_STORE_DATA_IMM, STORE_DATA_INDEX, and MI_FLUSH_DW must be 64B aligned",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPipeControlBeforeWmMaxThreadCountChange, "HW Bug 2877574: must issue pipe control after changing max thread count in 3DSTATE_WM", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNopWithIdWriteAfterLastFlush, "An MI_NOOP with NOP_ID bit set must be programmed after the last MI_FLUSH_DW before head = tail on VCS and BCS", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDisplayFetchStrideStretching, "Set bit 21 of 42000 to disable fetch-stride stretching for display A/B", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDapOneStateCacheLookUp, "Bspec erratum, set bit 14 on 208c", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaChickenReadModifyWrite, "HW Bug 2878278: Must set all masks and read modify writeback", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaExtendedStateSaveRestoreAlwaysEnable, "Bspec rule for MI_SET_CONTEXT, always set extended state save and restore enable bits", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVFUnitClockGating, "Enable bit 31 For 9404.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSOUnitClockGating, "Enable bit 18 For 9404 : Unit level clock gating Control 1.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSFUnitClockGating, "Enable bit 16 For 9404 : Unit level clock gating Control 1.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCCUnitClockGating, "Enable bit 11 For 9404 : Unit level clock gating Control 1. (HSD 3639253)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSCUnitClockGating, "Enable bit 14 For 9404 : Unit level clock gating Control 1. (HSD 3639369)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIZUnitClockGating, "Enable bit 0 For 9404 : Unit level clock gating Control 1. (HSD 3047076)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCPBUnitClockGating, "Enable bit 12 For 9404 : Unit level clock gating Control 1. (HSD 3639372, also HSWGTH HSD 3991468)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseBlitterForPresent, "Forces use of 2D blitter for present", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMbcDriverBootEnable, "Need to set 907c register before boot up.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReEnableInterrupts, "Turn interupts back on in PCI 0 2 0 offset 4 bit 10", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendPipeControlBeforeNonPipelinedState, "Any non-pipelined state must be preceded with a PIPE_CONTROL with non-zero post sync op", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetCsStallPipeControlBeforeNonPipelinedState, "PIPE_CONTROL sent due to WaSendPipeControlBeforeNonPipelinedState must also have CS Stall set", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTEnableMIFlush, "Enabling MIFLUSH in MI_MODE register for GT.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIdleBcsBeforeUpdateTail, "Idle the BCS ring before calling update tail buffer", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// Enable this WA for all platforms until we have alternate solution to unmask display interrupts.
WA_DECLARE(WaClearRenderResponseMasks, "RenderResponse mask default to all masked.  WA will clear masks until we get proper interface", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTSyncRegister, "Save sync register to context prior to restore", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDummyPipelinedStateBeforeIspDisable, "WA to ensure we have pipelined state sent to hw before sending a pipecontrol with ISP disable set", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCacheabilityControl, "Wa to prevent sw from writing surface state CacheabilityControl field.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSlowFenceIdPropagation, "ILK H/W s3573502: Wa to ensure enough time passes between when the fence id is written and when the notify interrupt is generated",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHardcodeMediaResetTimerClkFreq, "DCN 895815 - Hardcode Media Reset timer clock frequency", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableContinueAfterPageFault, "New SNB Chicken bits in CStep default to hang on page fault write bits to change behavior", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTileWalkYIsInvalidWhenNotTiled, "HW issue with TileWalkY if valign = valign_4 and tiled surface = false", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSampleinfoForUnboundTextures, "WA to handle 'sampleinfo' sampler message when resource is not bound", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMSAABandwidthOptimization, "WA to disable L1->L2 MSAA bandwidth performance optimization in B-Step. (HSD Gesher Sighting 3640020 )", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSampleLPerfFix, "WA - sample_l performance fix conflicts round_enable bits (gesher sighting 3715109)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDopClockGating,
           "WA to disable DOP clock gating for render HW GEN6 HSD: 3047761, HW gesher sighting 3715330. Gen8 HSD is here: "
           "https://vthsd.fm.intel.com/hsd/bdwgfx/#bug_de/default.aspx?bug_de_id=1899180",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRowChickenDopClockGating, "WA to disable DOP clock gating in ROW_CHICKEN2", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFfDopClockGating, "WA to disable FF DOP clock gating", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCSUnitLevelClockGating, "WA to disable CS unit level clock gating gesher sighting 3715329", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableFlushTlbInvalidationMode, "Wa - set GFX_MODE Tlb Invalidation Mode bit to enable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBCSVCSTlbInvalidationMode, "Wa - This is a new WA for WaEnableFlushTlbInvalidationMode since SNB WA", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStripsFansDisableFastClipPerformanceFix, "Wa - Disable strips fans performance fix (HSD sighting 3715494)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVcsIdleWhileWritingTp,
           "Wa- Issue on SNB with VCS TailPointer going to 0x10000 when TP update and occurs on same clock as idle sequence begins HSD Sighting 3715548)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEuUnitClockGatingForOA, "NOA/ MI_REPORT_PERF WA  Gen 6 HW bug 3047743", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVerticalAlignment4Power2, "Wa - surface vertical alignment of 2 should be used when possible if w/h not pow2 to avoid performance problem", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSStallBefore3DStateGSEnableToggle, "Wa - Send a Pipecontrol with CS Stall bit set to 1 before toggling GSEnable bit in 3DSTATE_GS", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVDSUnitClockGating, "IVB HW bug 3378689.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRevertDopClockGateFix2, "SNB D2 HW fix for 3047834 provides chicken bit to disable the fix. To be disabled on D2 to ensure behavior between D1/D2 is same",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRevertAsynchFlushFix, "SNB D2 HW fix for 3047897 provides chicken bit to disable the fix. To be disabled on D2 to ensure behavior between D1/D2 is same",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTDLUnitClockGating, "IVB HW bug 3379170.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushPipelineBeforeStreamOutState, "IVB HW bug 3379360 and 3379390", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceAllSOLDecls1Dword, "IVB HW bug 3379209 and 3379267 - each decl should only write or skip 1 dword.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendAllSOLDecls, "IVB HW bug 3665176 - send all decls for all streams.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPostSyncOpBeforeVSState, "IVB HW bug 3665834 - send post sync op write immediate before any VS state. (Cloned for HSW: HSD hswgth 3991788)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT(15), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableEwaLodOnlyForAniso, "IVB HW bug 3665834 - send post sync op write immediate before any VS state. (Cloned for HSW: HSD hswgth 3991687)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT(15), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEarlyCull, "Disable early cull always.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(2), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushAfterCubeTexCordClamp, "Flush after every 3Dprim that uses a cube map with address ctrl mode TEXCOORDMODE_CLAMP.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRSPushConstantCoherencyBug, "Coherency issue seen on Si. SW W/A proposed and mostly will remain permanent.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRSStoreDataImmDeadlock, "This one is only specify to OGL usages, this was really a WA to allow OGL to use the RS for constant creation and gathering.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePerfMonGathering, "Reading of perfmon registers causes hang in early BDW revisions.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReportPerfCountUseSpecificContextID, "Enables counters to work on a context specific workload only.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForcePcBbFullCfgRestore, "Force metrics full config restore on context switch via CTX WA BB.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEmptyOaBufferAsOverflow, "Set buffer overflow flag if there is no data in the oaBuffer.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableNonPresentRenderTargetChannels, "Component Write disables must be set for non-present color channels.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFixRenderSyncFlush, "Wa - apply SyncFlush fix for Render engine (Gesher sighting: 3715935 currenlty for SNB only).", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetupGtModeTdRowDispatch, "Wa - Setup GT Mode TD Row Dispatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPutSRMBetweenBackToBackLRIForDisplayReg, "Put SRM between two LRIs for display register with range 0x40000-0xBFFFF. As per bspec (under LRI definition)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGSNoDualModeWhenPrimId, "Changed primID +1 logic to primID + condition for second obj.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBarrierGrfReturnOffset, "Wa - allocate additional grf for BarrierReturnMessage", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPreservePayloadR0, "Wa - preserve grf R0 from writing (Gen6)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWaitForRingIdleIndicatorBeforeSyncFlush, "Wa - We need to wait for PSMI_CTRL (2050) bit 3 to indicate ring idle before issuing sync flush.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIgnoreRingIdleIndicator, "Wa - IVB ring idle indicator register is not supported in HAS-Fulsim yet. Temporary ignoring ring idle check.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVertexFifo, "Wa - Disable Vertex FIFO to improve performance.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSMLimitPresentDmaBufferSize, "Wa - Limit State Manger Present DMA buffer size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForTogglingDopClkGatingBit, "SNB D2 fix for S3/S4 resume issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetIspCounterToNonZeroBeforeCsRingEnable, "Wa - Set ISP counter to non zero before CS ring Enable - IVB HW sighting 3925170", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableL3Bank2xClockGate, "Disabling L3 clock gating- MMIO 940c[25] = 1.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInsertNoopAfterMiWaitForEvent, "IVB - Insert NOOP right after MI_WAIT_FOR_EVENT to prevent CS hang caused by MI_FLIP with idle flush enabled.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEUInstructionShootdown, "Disable EU instruction shootdown.", "Corruption.", WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaProgramMiArbOnOffAroundMiSetContext, "Enable programming MI_ARB_ON_OFF around MI_SET_CONTEXT.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCatErrorRejectionIssue, "Set chicken bit to fix CAT error issue caused by cycle rejection.(Cloned for HSW: HSD hswgth 3946253)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableBackToBackFlipFix, "Needs WaDisplayFlipAWaitAFlipBWaitB and WaDisableAsyncFlipPerfMode also set.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisplayPitchPowerOf2, "Display pitch should be power of 2 pitch aligned.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDoNotFailNonLocalOnlyCompressedFlagCombo,
           "Boot failure WA with compression enabled: Do Not Fail NonLocalOnly = 1 + NotCompressed = 0 FlagCombo on Xe2 till Compression integration is complete",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaApplyL3ControlAndL3ChickenMode, "IVB WA to set L3 Control register and L3 Chicken Mode register with specific values.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendDummy3dPrimitveAfterSetContext, "Send a dummy 3D_PRIMITVE after every MI_SET_CONTEXT.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableL3CacheAging, "WA - VLV sighting hardware bug # 261401 - needs L3 Control Register1 : L3 Aging Disable Bit (L3AGDIS): to be set on every context save/restore",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDivideLLCHitsCounterBy16, "Divide LLC hits count by 16.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSaveVscRegisters, "Send KMD WA Batch Buffer to save Media VSC MMIO register space into user-mode mapped resource", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCZUnitClockGating, "Disable RCZ Unit Clock Gating. (cloned HSD ivbgt2 bug_de: 3665923 )", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSerializeKmdDisplayAccess, "Serialize KMD Render DDIs to prevent MMIO access to Display range registers on the same cache line.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIssueContextSwitchBeforePreempt, "IVB issue where HW does not completely save the HW context during a GPGPU preemption. SW to force save the preempted context.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVfePreemptionFix, "HSW C0 issue where hw fix leaves old VFE/GPGPU_WALKER data in HW context after preemption, causing hang later", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRHWOOptimizationForRenderHang, "Set BIT 10 of COMMON_SLICE_CHICKEN1 in IVB to prevent render ring hang during WHQL CRASH.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIVBInstrumentedVLV, "Wa - To reduce the Execution Units of IVB down to 4 or 2 for VLV1 Performance Testing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDAPRHSClockGating, "Disable DAPRHS Clock Gating.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMidThreadPreempt, "Disable GPGPU thread-level (a.k.a. mid-thread) preemption", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreempt, "Disable 3D ObjectLevel preemption until HW fixes are in", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionForVgt, "Disable preemption for vGT", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPostSyncOpBefore3DSTATEGS,
           "Adjacency discard hold with state change causing hang.    Send PIPE_CONTROL with dummy post sync op when GS is enabled before 3DSTATE_GS command.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSRUncachable, "Declare CSR resource as uncachable", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushBefore3DSTATEGS, "Send pipe flush on every gs state change if allocated GS handle is less than 16 and it is SIMD8 mode.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSwitchSolVfFArbitrationPriority, "HSW hw has the priority switched by accident - this WA switches back to expected.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBBSNonPrivilegedBit, "WA - Use BBS Non-privileged bit (only HSW B0+) to force HW security parsing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlternateSigKeys, "HSW CB2/NO_OP signature keys are different for A step", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseNoopClearBuffer, "Use NO_OP Clear buffer instead of actual CB2", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCCCheckIn2DPresentPath, "Disable color conversion check in 2D Present", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceToNonPrivFifthRegisterNonFunctional, "On BDW A0 one of the entries in the ForceToNonPriv list of registers isn't usable", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSamplerPowerBypassForSOPingPong, "Disable sampler power bypass to avoid negatively impacting SO 'ping-pong' performance", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitSizeOfSDEPolyFifo, "Limit the size of the FIFO to prevent overlflow of FIFO counters.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSamplerPowerBypass, "Disable sampler power bypass to prevent MsaaBasic.level16 hang on mi_set_context", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableBcCentroidPerformanceOptimization, "Set Chicken bit to disable optimization for per-sample dispatch mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInsertNOPViaChickenBit,
           "Dirty Fill followed by Dirty Fill to same set and way causes 2nd Dirty Fill to evict wrong data Need to insert NOPs via chicken bit to fix the issue. Rare chance of "
           "happening but adding WA anyways.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBlockMsgChannelDuringGfxReset, "Block Msg Channel before Gfx Reset otherwise MC error happens & system crash with specific OCL/OGL WL", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForcePreemptWaitForIdleOnNonRcsEngines,
           "HW bug on *CS engines where a hang could occur if the 2nd element of an execlist is empty and a preemption request occurs at the wrong time. Workaround is to require "
           "idle before executing a preempt request on *CS",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncreaseTagClockTimer, "HW bug requires programing L3 tag clock timing register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLRIToDEUnsupported, "HW limitation on VLV and VLV Plus display engine registers reside outside the scope of LRI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableThreadStallDopClockGating, "Thread stall clockgating is in ROW_CHICKEN", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableInstructionShootdown, "Instruction Shootdown in ROW_CHICKEN must be disabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePartialInstShootdown, "Partial Instruction Shootdown in ROW_CHICKEN must be disabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGpGpuPreemptOnGt1, "GPGPU preemption will not work on GT1 skus", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaControlPrimaryTLBUtilization, "Control the Primary Display TLB utilization. WA is only needed for Win Blue feature Hybrid graphics. (linear surface for async flip)",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLiteRestore, "Disable Lite Restore", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHdcDisableFetchWhenMasked, "Set desired default value for HDCCHICKEN register for BDW/CHV platforms, default value is fixed in SKL+", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetVfGuardbandPreemptionVertexCount, "Preemption vertex count needs to be increased to 0x20 or above", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTdsClockGating, "Disable TDS unit clock gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableContextRestoreSubsliceAck, "Disable slice ack (for hsw gt1 sku only)", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCoherency, "Don't upgrade OCL contexts to be Coherent because of HW bug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableCoherencyHWFixes, "L3 coherency issue fixed in HW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceEnableNonCoherent, "Set default state of context to be Force Non-Coherent", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceSyncFlipWithVisibilityOff, "Work Around to Convert CS Async flips to sync. It is used for CHV when SetSourceVisibility is off.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableGamClockGating, "Work Around to disable GAM clock gating to avoid issue where GAMW does not send invalidation end to HDC", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisDdbClkWhileProgVisibilityOn, "DDB clock gating should be disabled while programming visibility ON in Gen5 display,", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaDisableFusedThreadScheduling, "WA to disable fused thread scheduling", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409543006, "WA to set chicken bit (9) in Command slice register to use ChromaKey Table For Compute Command Stream", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

// struct __wa_GuC

WA_DECLARE(DisableClockGatingForGucClocks, "Clock Gating must be disabled for GuC Clocks in BDW A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaProgramMgsrForCorrectSliceSpecificMmioReads, "Shadow Reg 119 (MGSR) needs to be programmed appropriately to get the correct reads from specific slice-related MMIOs",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEngineResetAfterMidThreadPreemption, "Perform an engine reset after a mid-thread preemption is detected (before resubmission)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaModifyVFEStateAfterGPGPUPreemption, "With specific scenarios of mid thread and thread group preemption, VFE state needs to be modfied before resubmission",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableuKernelHeaderValidFix, "Workaround for 0xC014 uKernel header valid bit bug for GuC load failures at higher GT frequency", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableGoMsgToGAMDuringCPD,
           "GuC to enable GPM GAM GO message during CPD to workaround for message channel hang and GPM hang. It could be used to solve more than one hang issues",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableGoMsgAckDuringCPD, "GuC to enable GO message channel ACK during CPD to workaround for message channel hang", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuCInitSramToZeroes, "Initialize SRAM to zero before GuC load to avoid Micro App DMA issue that causes HW to pick wrong key", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableGuCBootHashCheckNotSet, "Workaround for 0xC010 uKernel hash update bit not set randomly bug for GuC load failures", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGuCClockGating, "Workaround for HuC CSS header not getting populated in Gen9 and Gen10 platforms", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuCForceFenceByTlbInvalidateReg, "Workaround for Fence/Flush request is not asserting 'wfence' towards GAB.Hence Use TLB Invalidate register to do fence cycle",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuCCopyHuCKernelHashToSramVar, "Workaround for HuC kernel HASH lost after forcewake is released", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuCDummyWriteBeforeFenceCycle, "Workaround for fence cycle last write miss issue. WA is to send dummy write before fence", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGuCDisableSRAMRestoreDisable, "Workaround to Disable SRAM restore disable feature", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct _wa_Gmm

WA_DECLARE(WaCursor16K, "Cursor memory need to be mapped in GTT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVtdErrorCursor64K,
           "To prevent false VT-d type 6 errors, use 64KB address alignment and allocate an extra 2 Page Table Entries (PTEs) beyond the end of the displayed surface",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGWBFlushOnFenceChange, "Flush GWB on Fence Change (DCN #483613 (Napa), 504493 (Crestline))", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGWBFlushOnGTTUpdateEvenViaGTTADDR, "Flush GWB on GTT Change (Even via GTTADDR; DCN #504493 (Crestline); Current implementation not fit for pre-Gen3.5 enabling)",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa8kAlignforAsyncFlip,
           "Enable 8k pitch alignment for Asynchronous Flips in rotated mode. (!) Unconventional use! When used, set each XP mode-change (not in platform WA file)!",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa29BitDisplayAddrLimit, "Sprite/Overlay/Display addresses limited to 29 bits (512MB)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForce1MBGTTSize, "WA for Cantiga where 2MB GTT size causes hang.  Force to 1MB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncreaseFixedSegSize, "INF based. For select OEM's to improve per. See DCN 682743", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVistaTempResourceWA, "WA for 3DMarkVantage. See DCN 726505", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignContextImage, "WA for context alignment. HW Gen6 b2944797", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceGlobalGTT, "WA for cmds requiring memory address to come from global GTT, not PPGTT.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReportPerfCountForceGlobalGTT, "WA for MI_REPORT_PERF_COUNT cmd requiring memory address to come from global GTT, not PPGTT.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOaAddressTranslation, "WA for STDW and PIPE_CONTROL cmd requiring memory address to come from global GTT, not PPGTT.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa2RowVerticalAlignment, "WA to set VALIGN of sample and rt buffers. See DCN 787017", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableRingHostMapping, "WA to use host mapping rather than aperture mapping to rings. See DCN 855177", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMfx2ndLevelBatchRingSizeAlign, "Wa to align 2nd level batchs consumed by MFX ring. See DCN 856778 & DCN 857436", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePhysAddrBelow1MB, "WA to avoid OS allocations of physical pages above 1MB boundary : See DCN 897756", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMediaResetBeforePAVPCWrite, "WA to do a media reset after RC6 and before writing PAVPC register. See DCN 897504.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPpgttAliasGlobalGttSpace, "Disallow independent PPGTT space--i.e. the PPGTT must simply alias global GTT space. (N/A without FtrPageDirectory set.)",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearFenceRegistersAtDriverInit, "WA to clear all fence registers at driver init time. See DCN 2143231.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPcmBase1MBGranularity, "PAVP:PCMBASE allowed only 1MB granularity (per ConfigDb:Gen6:PCMBASE; Granularity = 128KB on C0+).", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRestrictPitch128KB, "Restrict max surface pitch to 128KB. See DCN 2145462.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidLLC, "Avoid LLC use. (Intended for debug purposes only.)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidL3, "Avoid L3 use (but don't reconfigure; and naturally URB/etc. still need L3). (Intended for debug purposes only.)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa16TileFencesOnly, "Limit to 16 tiling fences (e.g. when on or HAS'ing on pre-Gen7)--Set at run-time by GMM.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCacheHizBufferState, "Caches HiZ buffer in HiZ buffer state memory object do to potential bug in PTE based HiZ Caching", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3ParitySupportDisable, "WA to disable L3 parity handling on BDW steppings", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3ParityInterruptUnmask, "WA to unmask L3 parity interrupts on BDW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEmulationSmartCacheFlush, "WA to invalidate cache lines in LLC/eLLC in emulation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa32bitGeneralStateOffset, "GeneralStateOffset's capped at 32-bit (despite rest of gfx system supporting >32-bit).", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa32bitInstructionBaseOffset, "InstructionBaseOffset's capped at 32-bit (despite rest of gfx system supporting >32-bit).", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLateL3ErrorInterrupts, "WA to always check for parity error before reporting workload completion, only necessary for GPGPU workloads.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOAStatus2MemSelect, "HSW Wa to select aliased PPGTT mode using Registry Key \"HswOATimerPpgttMode\"", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa16MBOABufferAlignment, "WA align the base address of the OA buffer to 16mb", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3ErrorHwHanging, "(Not actual HW WA.) WA to disable HW hanging on L3 parity error", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIommuUncoreUnavailable, "WA to simulate uncore commands when using emulation model where uncore is not available", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIommuCCInvalidationHang, "WA to avoid boundary condition hang when a context cache invalidation follows a IOTLB invalidation.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTranslationTableUnavailable, "WA for BXT and SKL skus without Tiled-Resource Translation-Table (TR-TT)", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaExtIotlbInvHang, "WA to avoid the hang issue that occurs when using Extended IOTLB Invalidation Descriptor", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaL3IACoherencyRequiresIoMmu, "Gen8 only supports IA-coherent L3 for Advanced Context. (By design--Not actual HW bug.)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIommuTEBit, "Disable Translation Enable bit for IOMMU", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoMinimizedTrivialSurfacePadding,
           "(Not actual HW WA.) On BDW:B0+ trivial surfaces (single-LOD, non-arrayed, non-MSAA, 1D/2D/Buffers) are exempt from the samplers large padding requirements. This WA "
           "identifies platforms that dont yet support that.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoBufferSamplerPadding, "Client agreeing to take responsibility for flushing L3 after sampling/etc.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReusePteL3BitforSecurity, "WA to re-use the L3 Bit in the PTE for indicating security indication from VLV B0.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableWTCaching, "WA to disable WT caching on CRW until GT E1 stepping due to HW bug b4392165 [CRW Write Through Caching Minor Corruption]", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSecureSegmentInPpgtt, "In VLV DMA buffer is in PPGTT Secure Segment", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetDVMSizeToStolenMemorySize, "On LP platforms, 31 MB of stolen memory was not utilized(No FBC). To avoid this we report the DVM size equal to Stolen memory size",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAllPasidInvHang, "WA to use use PASID selective invalidation instead of All Pasid invalidation to avoid a hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSurfaceStatePlanarYOffsetAlignBy2, "WA to align SURFACE_STATE Y Offset for UV Plane by 2", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGttCachingOffByDefault, "WA to enable the caching if off by defaultboth at driver init and Resume", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableOnlyGpgpuCommandLevelPreemption, "WA to enable only the GPGPU Command Level Preemption and disable other GPGPU preemptions", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCompressedResourceSamplerPbeMediaNewHashMode, "3D and Media compressed resources use LLC/eLLC hot spotting avoidance mode", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCompressedResourceDisplayNewHashMode, "3D and Media compressed resources use LLC/eLLC hot spotting avoidance mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCompressedResourceDisplayOldHashMode, "3D and Media compressed resources use LLC/eLLC hot spotting avoidance mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInPlaceDecompressionHang, "WA to avoid the hang issue that occurs when using in-place decompression", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTouchAllSvmMemory, "When in WDDM2 / SVM mode, all VA memory buffers/surfaces/etc need to be touched to ensure proper PTE mapping", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIOBAddressMustBeValidInHwContext, "IndirectObjectBase address (of SBA cmd) in HW Context needs to be valid because it gets used every Context load", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableKillLogic, "WA to disable kill logic (for page faulting), which causes hang when TR-TT and RC6 are both enabled", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushTlbAfterCpuGgttWrites, "WA to flush TLB after CPU GTT writes because TLB entry invalidations on GTT writes use wrong address for look-up", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMsaa8xTileYDepthPitchAlignment, "WA to use 256B pitch alignment for MSAA 8x + TileY depth surfaces.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIommuAccessedDirtyBit, "WA to disable A/D bits usage for IOMMU", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisableNullPageAsDummy, "WA to disable use of NULL bit in dummy PTE", WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa64kbMappingAt2mbGranularity, "WA to force 2MB alignment for 64KB-LMEM pages", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaUseVAlign16OnTileXYBpp816, "WA to make VAlign = 16, when bpp == 8 or 16 for both TileX and TileY on BDW", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(WaDisableRFOSelfSnoop, "RFO Self-snoop must be disabled when in adv ctxt mode to avoid perf issue", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaDisableDynamicCreditSharing,
           "Dynamic credit sharing (used for memory cycles) between various HW units must be disabled to avoid hardware hang with page fault injection", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaGttPat0, "GTT accesses hardwired to PAT0", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaGttPat0WB, "WA to set WB cache for GTT accessess on PAT0", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaMemTypeIsMaxOfPatAndMocs,
           "WA to set PAT.MT = UC. Since TGLLP uses MAX function to resolve PAT vs MOCS MemType So unless PTE.PAT says UC, MOCS won't be able to set UC!", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaDSMPage0OffLimits,
           "WA for driver to continue to stay of DSM Page#0, on dGpu(XeHP SDV+) can freely use DSM Pg#0 (which can coexist with SQID's write-mask-disabled use) !",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaGttPat0GttWbOverOsIommuEllcOnly, "WA to set PAT0 to full cacheable (LLC+eLLC) for GTT access over eLLC only usage for OS based SVM", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

WA_DECLARE(WaAddDummyPageForDisplayPrefetch, "WA to add dummy page row after display surfaces to avoid issues with display pre-fetch", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisableSingletonEscape, "Temp WA to prevent GMM escapes for UMD's running in container/VM", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDefaultTile4, "[XeHP SDV] Keep Tile4 as default on XeHP SDV till B stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisableUnifiedCompression43Ratio, "[DG2] Keep Disable Unified Compression 4:3 Ratio till B stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(WaGamDeadLock, "[DG2/XeHP SDV] Avoid Host LMEM access to WA the GAM dead lock issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaForceSaveRestoreFlatCcsOnPaging, "[DG2/XeHP SDV] Force Save/restore of FlatCCS for LocalOnly surfaces irrespective of whether it is compressed or not",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaBootGpuInSystemMemoryOnlyMode, "Survivability System-only mode for Si bring-up when issues with device local memory", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(WaTile64Optimization, "Tile64 wastge a lot of memory so WA provides optimization to fall back to Tile4 when waste is relatively higher", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaEnableMemProfileLogInUmd, "Wa Enable Mem Profiler logs in UMD from the KMD based regkey through QueryAdapter", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(WaCompressionLimitedByLocalOnlyRequirement,
           "XE-HPG compression can only be LocalOnly, so limited by LocalOnly commit limit, otherwise it would result into OOM, Poor perf/UX", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

// struct _wa_DXVA

WA_DECLARE(WaRestore3DBufVarMpeg, "Must switch decoding type back to MC after VLD decoding", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDefaultNoGfxMemoryTile64, "[DG2] Use private GMM Alloc for Tile64", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaNo2ndLevelBatchBuffer, "Disable AVC Encoding multislice until 2nd batch buffer support on B0, HSD 3046603", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaForceAllocationToAperture, "Certain buffers in Memory segment exposes corruption. See DCN 682743", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSuppressReconPicForNonRefPic, "HSW A-stepping does not support suppressing the reconstructed picture for non reference pictures", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaAddMediaStateFlushCmd, "BDW and CHV require Media_State_flush command to be added at the end of command buffer or the batch buffer", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa8BitFrameIn10BitHevc, "Before Gen11 HW cannot output 8bit decoded frame correctly into P010 RT for 8b/10b mixed bit depth clip", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVC1UnequalFieldHeights, "SNB+ requires that all VC1 fields be of equal height as HW assumes that this is the case, HSD 3715550", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableLockForTranscodePerf, "IVB Transcode performance temp WA fix to remove Lock in Decoder", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaInsertAVCFrameForFormatSwitchToJPEG,
           "Format switch from any Codec decode/encode ending with Skipped MB to Jpeg results in a hang on IVB/VLV/HSW. Fixed from HSW B0, HSD 3665967.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableJPEGHSWNewFeatures, "New features are supported from HSW C0: The output formats of NV12/YUY2/UYVY and minimal size to 8x8.", WA_BUG_TYPE_FAIL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaJPEGHeightAlignYUV422H2YToNV12, "Chroma type 422h_2Y and output format NV12 aligned with 8 to Jpeg results in a hang on HSW ULT/BDW. Fixed from CHV.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaVC1DecodingMaxResolution, "For VC1 decoding, HW only can support resolution<=3840*3840.", WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaParseVC1PicHeaderInSlice,
           "For VC1 advanced profile, if PIC_HEADER_FLAG in slice header is set, parse picture header in subsequent slice headers to get MB data offset. HW expects MB data offset "
           "while WMP provideS bitplane offset if bitplane presents.",
           WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaParseVC1FirstFieldPictureHeader,
           "For first field of picture in VC1 advanced profile, if it is I or P picture, parse picture header to get REFDIST value. HW expects REFDIST for I/P/B fields while WMP "
           "send it with B pictures only.",
           WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaParseVC1BPictureHeader,
           "Parse B picture header to get BFRACTION in VC1 advanced profile and main profile. HW expects BFRACTION for B pictures while WMP does not provide it.", WA_BUG_TYPE_FAIL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaLinearMediaBlockAccess64BytePitchAlign, "Linear surfaces accessed with Media Block Read/Write commands require 64-byte-aligned pitch.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaLLCCachingUnsupported, "There is no H/w support for LLC in VLV or VLV Plus", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableMFXCryptoCopy, "WA for disabling MFX_CRYPTO_COPY command as it is not supported in HSW HAL-Fulsim (this WA should not be applied in any production code)",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableNonStallingScoreboard, "Disable NonStalling Scoreboard on SNB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableNonStallingScoreboardBasedOnNumSlices, "Disable NonStalling Scoreboard based on Number of Slices", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaResetVLineStrideInRenderCacheAfterMedia, "Reset Vertical Line Stride In Render Cache After Interlaced Media Workload", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

//  This is just a Temp WA not an official WA, just to unlock PC Val in PO.
WA_DECLARE(WaPopulateScratchRegistersWithMCHBarRegsforDG1A0, "DG1 A0 can't read from MCHBar, temp fix for PO is to use scratch regs to populate it in Host.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMFX48bitAddressing, "Disable 48-bit addressing mode on HSW A stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(
WaUseVP8DecodePrivateInputBuffer,
"Create a private Gfx buffer in driver and copy bitstream and Coefficient Probability table to it to avoid upper bound check failure in BDW A0. It's for VP8 decode in BDW A0.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDummyDMVBufferForMVCInterviewPred, "Insert dummy DMV buffer for MVC decode HW issue (colZeroFlag for interview reference should always be 0).", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaVeboxSliceEnable, "DAC has to turn off before programming the PLL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaIs64BInstrEnabled, "64-byte instructions are enabled on BDW B0+.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaIgnoreCSXRStateForWMProgramming, "Ignore CSXR State and Program the Watermark registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_PWRCONS)

WA_DECLARE(WaSwWOPCMSetup, "Enable SW generated WOPCM setup", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaProgramAppIDFor2VDBox, "Program AppID to restore PAVP HW context in WOPCM for Slave VDBox", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaAssumeSubblockPresent, "Subblock coding information not present in bNumCoef for Interlace Frame intra MBs (VC1 IT mode)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(
WaEnableDscale,
"If the SampleUnorm delta for U direction is more than 3, driver divides into two subspans and sends the request as regular sample instead of SampleUnorm. bug_de_id=2123853",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableGroupIDLoopSelect, "Set Group ID loop select to 0 if scoreboard is used.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaDisableHuCBasedDRM, "Disable HuC based DRM on CHV.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_MEDIA)

WA_DECLARE(WaNeedHeightAlignmentForTiledYCaptureSurface, "Need to align the height to Tile Y block height if Capture Surface is Tiled Y.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLinearCaptureSurface, "ISP outputs Linear Capture Surface instead of Tiled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSuperSliceHeaderPacking, "Need to modify slice header when PPS/AUD is not present for super slice case", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// struct _wa_SoftBIOS

WA_DECLARE(WaProgramDpll, "DAC has to turn off before programming the PLL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaADD2DetectBit, "sDVOB control register bit2 on BWG(Crestline maybe) A0 doesn't indicate the right status", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTVDetect, "TV Detection sense bits reversed in Crestline", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableSCWBPPeriodicFlush, "Disable/Enable preiodic flush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaExtModeFSDOSBlankScreen, "FSDOS blankout/hang in extended desktop (HSD: 545700 & 545671)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTVEncoderDisable, "TV encoder when disabled, we should wait for vsync", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWaitForVBlankAfterTVDisableOREnable, "Wait for vblank, while disabling/enabling TV encoder. BUN#06ww06#6", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCenteringDuringVGADisable, "VGA centering mode should be disabled in Non-VGA mode. HSD# 306526. Bug# 2156169", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDynamicNormalWaterMark, "Disable dynamic normal watermark computation & programming in Softbios", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClosedCaptionHotplug, "Crestline only can't have CC control register on and hot plug enabled simultaneously", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetCR17regAfterS3Resume,
           "Bug# 2078297: Crestline - No Display on TV when coming back from Stand-by. Need to set Bit 7 of CR17 VGA register after Standby-Resume on CRL only, otherwise IntTV "
           "blanks out. As per HW DEs: if bit 7 is set to 0, it suggests that the vertical/horizontal retrace updates have been turned off and therefore are not making it to "
           "ST01. Thus the issue happens.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaDisableHPLLShutdown,
"Bun 07ww02:Disable HPLL shutdown when accessing 6XXXh MMIO addresses. If we try to access it when in HPLL shutdown mode and read/write to these locations will result in a hang.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWaitForVSyncAfterPortEnable, "BWG BUN to WaitforVSync After enabling port. Fix for 2440922.GEN4_BUN_07WW24.3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPF2ForDisplayPort, "BUN:07ww24#1. Need to reset bit 27 of PF2, for DisplayPort. Only from CTG B0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDPHDMISupriousHpd, "BUN 08ww9.5: Workaround for suprious interrupts on DP/HDMI on ELK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePFinMultiPlaneMode, "Flicker seen when we enable more than 1 plane during native mode on eDP/DP, flicker goes away with PF enabled", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDPHDMIHpdEnable, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTVFullScreenHotUnplug, "WA for TV FullScreen HotUnplug Issue.(only for CTG B3).", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRandomAnGeneration, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUse32BppForSRWM, "WA for using 32BPP for WaterMark calculations for ELK\CTG to take usual BytesPerPixel.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHDCPDoubleRead, "WA for doing double reads of all HDCP registers for ELK.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa9DotDisableinVGA, "HSD 2209669.Problem when switching frm 8 dot to 9 Dot can cause Permanent underrun", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHPDVrefValue, "WA for correcting vref in PCI-E band register to avoid spurios inteerrut", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDelayAfterSetDisplayStart, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePF3ForInterlaced, "Keep PF3 on for interlaced modes from ilk c2 only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTurnDPOffAfterCPUPipe, "BUN#09: DisplayPort Corruption during modeset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableESFVPwhenFBCisON, "Disabling display plane reduces SR resisdency when FBC is ON. Thus, won't enable ESFVP with FBC.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClkGatingForEmbDPPortD, "vol4h [DevCPT] Embedded DP on DP-D clock gating ww19 BUN.doc,", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUpdateFBCasPlaneStatusChanges, "BUN#027: This BUN is to workaround problems with enabling FBC while the primary plane is disabled.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWaitForVBBeforeEDPLLON, "Wait for VB before turning on edp pll, if other pipe is enabled on FDI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablebyPassModePllForMIPI,
           "Wa to Enable bypass mode PLL for MIPI while sending initial commands in LP mode due to HW bug "
           "https://vthsd.an.intel.com/hsd/valleyview/default.aspx#bug/default.aspx?bug_id=4600712",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMipiDispShiftIssue, "WA for Dual link FB Video mode/ Normal Command mode Shift issues", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaMIPIDualLinkPixelOverlapCount, "Dual Link MIPI needs programming of Pixel Overlap count from VLV C0 onwards", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableTxrequest_0,
           "WA to Enable TxRequest from VLV C0 onwards to make sure LP to HS transitions are in sync due to HW bug "
           "https://vthsd.an.intel.com/hsd/valleyview/default.aspx#bug/default.aspx?bug_id=4600191",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMipiDPOUnitClkGateEnable,
           "WA to Enable DPO Unit Clk gating function to use CDClk function for MIPI enable/disable seq. due to HW design "
           "https://vthsd.an.intel.com/hsd/valleyview/sighting/default.aspx?sighting_id=4693697",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAudioInactiveReset, "Wa to Reset Audio Inactive bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaConvertorToPinMapping, "Wa for bug :converter widget to pin widget mapping before playing the audio stream in HDMI for HSW B0", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaResetChickenBitForAutoLinkTrain, "Wa to reset the chicken bit for the autolink trainin on IVB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPortWriteforAudioControllerinBIOS, "Wa to enable/disable the audio Dev 3 config register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCheckforAudioPowerStateRegister, " Wa to poll the power state register while going to CS. Only for HSW+ platforms.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCRCDisabledForMBO, "Wa to keep CRC disabled in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrSfuMaskSprite, "Wa to mask Sprite Enable while in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIsAudioControllerinLPSPWell, "Wa to Check if Audio Controller is in Power Well", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForBlackFlashInMBOMode, "Wa to avoid black flashes in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePrimaryFlipsForMBO, "Wa to disable primary flips in MBO disable sequence which would otherwise lead to jitter after entering back legacy PSR.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLSPCONAuxTransactionInLSMode, "Wa to disable AuxTransactions In LSMode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoubleCursorLP3Latency, "Wa to increase cursor latency value in LP3 case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableHDMI8bpcBefore12bpc, "Wa to enable HDMI port in 8bpc before 12bpc", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFrameStartDelayWaForSDRRS, "Wa to eliminate flicker/screen shift seen during SDRRS Transition.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHDCPDisable, "Wa to Enable/Disable  HDCP using Registry Key \"DisableHDCP\"", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearPSRReset, "Wa to clear PSR reset bit after setting it", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaS3DSoftwareMode, "Wa to use S3D Software mode when the right address in not on tile boundary", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableBwgTlbClockGating, "Disable BwgTlb Clock Gating on BDW A-Step", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFdiRxMiscProgramming, "Program FDI_RX_MISC register from LPT B0 onwards as part of VGA modeset BUN", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMPhyProgramming, "Program mPHY Registers from LPT B0 onwards as part of SSC Enable/Disable sequence", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVLVClockGating_VBIIssue, "Disable VLV Clock Gating till B0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOGLCubemapWrapModes, "TileW with RCC will not work; page fault occurs, data corruption.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHSWBorderColorCalculation, "From HSW C0 integer emulation is disabled and different border color structure has to be used", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIntegerTextureSamplingEmulation, "Till HSW C0 we have to emulate integer textures sampling", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTileWInRcc, "TileW with RCC will not work; page fault occurs, data corruption.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFastClearRegistersInPrivilegedList, "These registers are no-oped and cause corruption in pre-si", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSpriteYUVOffset, "From HSW C0, we preserve the 1/2 offset on U and V channels if sprite output is YUV", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableVBlankForOnlyActivePipe, "To restrict enabling of VBlanks to only Active Pipes.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEDPModeSetSequenceChange, "Required for Clock gating disable in ULT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPartitionLevelClockGatingDisable, "Upto VLV B0 :Required for enabling audio on DP.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVLVDPAudioEnable, "Upto VLV B0 :Required for enabling audio on DP.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVLVPMCiCLK5WriteEnable, "VLV B0 :Door Bell write to iCLK5 is SAi protected. Write needs to be enabled through PMC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearArfDependenciesBeforeEot,
           "ARF dependencies unlike GRF dependencies are not cleared by the HW after receiving SEND messages with EOF (End Of Thread). This can be an issue on platforms with per "
           "thread clock gating which disable the EU thread clock right after the EOT. With the clock disabled all pending ARF dependencies are not cleared and stay valid even "
           "when the EU thread gets rescheduled. The WA is to make sure all ARF dependencies are cleared before the EOT. This can be done either by making sure the ARF register "
           "is read before the EOT or the last instruction writing the ARF has the {Switch} bit set.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMADMMacros, "Accordig to Bspec IEEE Madm macros for FDIV and FSQRT will be provied in BDW B0 step.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPMICRegisterReadWrite, "This is a temporary WA to enable PMIC reads/writes for PMIC register reads/writes.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable1DDepthStencil, "WA on SKL to disable 1D Depth Stencil buffers and use 2D with ht of 1 instead.  Still in discussion when or if this will be fixed.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZeroOneClearValues, "SKL clear values Bspec restriction: Only 0/1 values allowed.     SKL:GT2:A,SKL:GT3:A,SKL:GT4:A", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// See the bspec RENDER_SURFACE_STATE command in the '* Clear Color' DWORDs.
// It says: "If programmed to non 0/1 values, SW must ensure a render target partial resolve pass before binding a cleared RT to texture."
// This was added for bspec update bug https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2122362.
// On CNL, this was fixed so the resolve is no longer needed.
WA_DECLARE(WaZeroOneClearValuesAtSampler, "SKL clear values other than 0/1 need resolve pass before being sampled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZeroOneClearValuesMSAA, "If Number of Multisamples is not MULTISAMPLECOUNT_1,  only 0/1 values allowed", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCCSClearsIfRtCompressionEnabledInGT3,
           "Lossless compression and CCS initialized to all F (using HW Fast Clear or SW direct Clear) on the same surface is not supported", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLosslessCompressionForSampleL, "Disable lossless compression when sample_l in a loop is detected", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHizAndClearedResourcesBoundToSamplerAtSameTime,
           "Use Partial Resolve pass before binding a fast cleared resource as texture.  This is due to hang issue when hiz and rt compressed textures are bound at same time, "
           "which can include a mix from multiple draws.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHizAndCompressedAtSamplerAtSameTime, "issue when sampler is sampling from hiz and from lossless compressed resource at same time", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSamplerL2BypassForTextureCompressedFormats,
           "BSpec restriction: Sampler L2 Bypass Mode Disable. This bit must be set for the following surface types:BC2_UNORM, BC3_UNORM, BC5_UNORM, BC5_SNORM, BC7_UNORM",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSamplerTexCoordModeMirror, "BSpec restriction: Sampler TCX and TCY must be the same if TEXCOORDMODE_MIRROR is selected", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDCFlushOnCacheInvalidate, "BSpec restriction: Set PIPE_CONTORL::DC_FLUSH when either Texture Invalidate or Constant Cache Invalidate PIPE_CONTROL bits are set.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPCFlushBeforeRTCacheFlush,
           "Before any PIPE_CONTROL with RenderTargetFlushEnable set, send a PIPE_CONTROL with RenderTargetFlushEnable = 0 and PipeControlFlushEnable = 1", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaResendURBWhenGSorHSGetsEnabled, "Resend URB state when GS or HS goes from disabled to enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAuxRetryOnUnknownError, "For the Aux jitter issue in HSW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAsyncFlipPow2Pitch, "WA to fix Display Flip Issue on VLV. This WA will enforce display stride to be power of two and Max Pitch to 16k.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDoubleFastClearWidthAlignment, "For all HSW GT3 skus and for all HSW GT E0+ skus, must double the width alignment when performing fast clears.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNoMMIOWhenPGOff, "For BDW B0, accessing PG2 registers during PG off causes CatERR.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsNullConstantBuffer, "Work around the HW resource streamer issue in which the RS still fetches when the surface type is NULL", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseNonPrivRegisterForObjectLevelPreemption, "Pre-G0 use GFX_MODE(229c) and G0+ use INSTPM(20c0) MMIO regs to disable Object level preemption for draw call.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionSequentialMode,
           "Disable Object level preemption when primitive will be in sequential(non-index) mode. Program ReplayMode bit of appropriate MMIO reg before and after primtive draw "
           "call to turn off midobj preemption for that draw call.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForInstancedDraw,
           "Disable Object level preemption when instancing is used in indexed draw calls. Program ReplayMode bit of appropriate MMIO reg before and after primtive draw call to "
           "turn off midobj preemption for that draw call.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForDraw,
           "Disable Object level preemption when primitive will be in line loop, tri-fan, polygon, quadstrip modes. Program ReplayMode bit of appropriate MMIO reg before and "
           "after primtive draw call to turn off midobj preemption for that draw call.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForGSLineStripAdj, "Disable Object level preemption when draw-call is a linestrip_adj and GS is enabled. ", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMaskRegWriteinPSR2AndPSR2Playback, "Need to mask reg writes in PSR2 idle and PSR2 playback mode", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrDPRSUnmaskVBlankInSRD, "Work around to unmask VBI and flips while link is in PSR to unblock flips", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLimitSqIdiCounterToEleven, "Bug# 4392931 Work Around To Enable GuC based KMD submissions via Doorbells", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaC6DisallowByGfxPause, "Bug# 2133391 SKL: MSNP: MSNP sends snoops L3 even after ACK'ing L3_Bypass to GPM", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMinuteIaClockGating, "Bug# 2127939 Work Around for MinuteIa Clock Gating bug Hang", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRepcolMessages, "Work around issue with replicated color write messages", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPsrDPAMaskVBlankInSRD, "Work around to trigger flips and VBI on first frame during PSR exit to ensure remote frame buffer gets updated with new image",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendsSrc1SizeLimitWhenEOT, "Work around to limit size of src1 up to 2 GRFs, on Sends/Sendsc instructions when they are EOT.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMixedModeLog, "Math LOG doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMixedModePow, "Math POW doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMixedModeFdiv, "Math FDIV doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaResetN0BeforeGatewayMessage, "Gateway is sending spurious clear to notify register resulting in a EU hang.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFloatMixedModeSelNotAllowedWithPackedDestination, "sel doesn't work correctly when using mixed mode and destination is <1>:hf.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDSPushConstantsInFusedDownModeWithOnlyTwoSubslices,
           "If pm_mode_subsliceen is set to 101 or 110, Domain shader must use pull constants instead of push constants", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableVSPushConstantsInFusedDownModeWithOnlyTwoSubslices,
           "If pm_mode_subsliceen is set to 101 or 110, Vertex shader must use pull constants instead of push constants", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDgMirrorFixInHalfSliceChicken5, "Wa to solve issues in wgf11Filter used in 3D sampler -by Disabling DG Mirror Fix enable bit in Half_Slice_Chicken5 register.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetDisablePixMaskCammingAndRhwoInCommonSliceChicken,
           "Wa to fix failure in 3D pix mask cam_match for Tile X cases  -by setting RHWO Optimization Disable bit in Common_Slice_Chicken1 register AND setting Disable Pixel "
           "Masked Camming in Slice_Common_Eco_Chicken0.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaSetMDRBunitClckGatingDisable,
"Wa for Jasper Gold SEC: Fixing clkgating bugs - by setting MDRBunit Clock Gating Disable in Uncore Well bit in RCPCONFIG - Configuration Register for RCPunit register.",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetGAPSunitClckGateDisable,
           "Wa for fixing RTL Clock gating issue in gapsunit(Snoop Data Response) - by setting GAPSunit clock gate disable bit in Unit Level Clock Gating Control6 register.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableAutostripInFFMode, "Wa for DX11 Frame hangs by Disabling TE Autostrip in FF_MODE Thread Mode register.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNativeDWxDWMultiplication, "Work around to disable DWxDW multiplication due to hardware bug which cause thread hang", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WADisableWriteCommitForPageFault, "Work Around to disable the commit bit when we have Page Faults in Memfence ", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNullDepthBuffer, "Prevent a null depth buffer from being bound by setting a fake depth buffer without depth or stencil writes enabled.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipInvalidSubmitsFromOS, "[MSFT 416192] For Invalid submits from OS - simply report fence completion without submitting the DMA buffer to GPU", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAGPGPUMidThreadPreemption, "This is used by any kernel change needed to support mid thread preemption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableHGAsyncFlipLinearToTileConvert, "Enables the Linear to Tile Conversion before Displaying needed for Hybrid Graphics Async Flip.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableGPGPUSlmPerfFix, "When 20e4[9] is set it disables the performance fix for GPGPU no barrier and no SLM case", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMIPICControlRegAndTERegRead, "MIPIC port control 61700 and TE register 61704 read returns the values from a legacy (currently) non-functional register space",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMIPIDSIRegRead, "Read from MIPI DSI Clock and PLL Register is failing", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCompressedResourceRequiresConstVA21, "3D and Media compressed resources should not have addresses that change within bit range [20:0]", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCsStallBeforeNonZeroInstanceCount, "Issue CS Stall when going from 3DSTATE_HS zero instance count or HS disabled to 3DSTATE_HS nonzero instance count",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRCFlushEvery16RTVOnBTPUpdate, "Issue RC Flush if number of render targets exceeds 16 on generation of binding table", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPipeControlBeforeVFCacheInvalidationEnable, "Issue Pipe Control with all bits set to zero before issuing Pipe Control with VF Cache Invalidation Eanble set to 1",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisregardPlatformChecks, "Disable plarform checks to support pre-si features on MediaSolo.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAMMCDUseSlice0Subslice0, "WA for MMCD by using slice0 subslice0 only to avoid hang caused by missing HDC repeaters", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WAMMCDDisableStallBitInPipeControl, "WA for MMCD by initiating regular fence before issuing Atomic Fences to avoid random hang", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWmMemoryReadLatency, "WA to account for pcode not putting the memory read latency in the mailbox response", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

// WA for RTL testing
WA_DECLARE(WaForceGrfInitializationAtBoot, "This will put the EU GRFs in an initialized state. Required for RTL validation with aub captures.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIntegerDivisionSourceModifierNotSupported, "Source modifiers for integer division are not supported.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMIPIPhaseDelay, "MIPI DSI Clock lanes are 180 degree of out phase with data lanes. WA is added to compensate for the delays", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSCDisable, "Disabling CSC when MIPI pipe is running is causing display controller to hang, WA is added to keep CSC enabled if MIPI Pipe is running",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemtionForVertexCount, "Disable Object level preemption for indirect or draws with vertex count < VF_PREMPTION guardband set by KMD",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPlaneCxTilingFailure, "Switch of plane programming from linear to tiled is failing in Plane C", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRealignCursorC, "Realign the cursor buffer in Pipe C when position becomes negative on 0 orientation and fail HW cursor on 180 orientation", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSSCClockOverride, "A0 and A1 parts does not have support for non SSC Clock, causing blankout when used, forcing usage of SSC", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCCKClkSkuIncorrect, "Invalid value is being returned when CCK Fuse Register 0 is read", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPixelRepeatModeFixForC0, "Chicken bit register implementation is provided in C0 for selecting the Mul/Div factor between Pipe B and PipeC", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHPDPeriodIncorrect, "HPD period is incorrect which causes driver not to diffrentiate between long pulse and short pulse", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAllocateSLML3CacheCtrlOverride, "Allocate SLM WA to fix media resets via L3 cache control register on BDW D0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemtionForInstanceId, "Disables Object level preemption for draws that reference InstanceID in the VS kernel", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForLineLoop, "Disables Object level preemption for draws with line loop topology", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForTrifanOrPolygon, "Disables Object level preemption for draws with triangle fan or polygon topology", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceDX10BorderColorSampleC, "Will use DX10 Border Color format and use DX10 sampler mode for depth textures", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceDX10BorderColorFor64BPTTextures, "Will use DX10 Border Color format and use DX10 sampler mode for 64BPT textures", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// struct _wa_HuC

WA_DECLARE(WaHuCStreamOutOffsetIsStreamInOffsetForPAVP,
           "If HUC_STREAM_OBJECT StreamOutOffset not equal to StreamInOffset, wrong data will be sent to HuC & StreamOut during decryption when HUC_AES_STATE used",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHucStreamoutEnable,
           "To prevent corruption in the case where a HUC workload with bitstream streamout DISABLE followed by another HUC workload with bitstream streamout ENABLE",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHucStreamoutOnlyDisable, "To prevent mode switching problems related to stream out only mode, add a HuC workload which uses FW after a stream out only workload",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaZeroHuCImemDmemAttributes, "HuC setting incorrect dmem_imem_attributes on read to wopcm via GAM causing b2b HuC loads to hang", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForQuadStrip, "This is used to prevent preemption when doing quadstrip topology", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableObjectLevelPreemptionForLineStripAdjLineStripContPolygon, "Object level preemption has to be disable for linestrip_adj_cont and polygon topology",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable3DPreemptionDuringUAVDrawCall, "Limit preemption for 3D workloads only to MI_ARB_CHK when UAV state is enabled for any shader", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRCWithAsyncFlip,
           "Shouldnt use Render Compression with async flip on SKL A due HW issue and SKL B+ as they are converted to sync Flips internally.  Fixed in GLK, GWL, GLV, and Gen10+",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHBR2, "Shouldn't report HBR2 Support on SKL A1 boards due to HW Issue", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableRCNV12, "For SKL C0 stepping, the RC fix that asserts the stall can be disabled by CHICKEN_PIPESL bit 22", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableChickenDCPR, "For SKL underrun is seen during multiple modeswitch due to SAGV. This WA is to overcome this issue", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableBandWidthLimitation,
           "For SKL underrun/flicker is seen during multiple 4K planes enabled in multiple displays due to BW limitation. This WA is to overcome this issue",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaKeepAllPGsActive, // 15.45: WaKeepPG2Active. Changing name in mainline to keep it as generic for higher platforms to handle > PG2.
           "keeping all PGs always active", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaKeepPG1ActiveDueToDMCIssue, "Keep PG1 always enabled", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDisableRCWithS3D, "Shouldnt use Render Compression with S3D flip", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaProgramL3SqcReg1Default, "Program the default initial value of the L3SqcReg1 on BDW for performance", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetHdcUnitClockGatingDisableInUcgctl6, "Prevent Flush hang in hdc when susbslice 0 or sublsice 2 is active", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableFtrSubSliceIzHashing, "Disable the feature FtrSubSliceIzHashing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDither, "Disable dither", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSPTMmioAccessSbi, "Access SPT MMIO through sideband interface", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSPTMmioReadFailure, "SW WA to skip SPT MMIO Read error", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePlaneGamma, "SW WA to avoid Plane Gamma unit", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVfPostSyncWrite, "Workaround for BDW to set post sync op of write for PIPE_CONTROL when only VF cache invalidate set", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIdleLiteRestore, "Workaround for a HW issue with lite restore.  SW must ensure that any context always has Head!=Tail when attempting lite restore",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableYV12BugFixInHalfSliceChicken7, "Set YV12BugFixEnable bit. Chroma cycles(U, V) will use half the value of pitch in Y-cycle.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaDisableSFCSrcCrop,
"Workaround for SFC src cropping HW issue SW HSD#8157496/10031162/10032751 and HW sighting#4712168 and HW bug_de#2136628. SW need fallback to EU path under hang condition",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSFC270DegreeRotation,
           "Workaround for SFC 270 degree rotation issue SW HSD#10003260 and HW sighting#4712694 and HW bug_de#2137174(Gen9) and HW bug_de#1945663(Gen10) and HW "
           "bug_de#1604124754(Gen11). Make sure Scaled Region Size Width < Output Frame Width && Scaled Region Size Height < Output Frame Height on Gen9 and Gen10",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTargetTopYOffset, "Workaround for TDR issue HW HSD#15010311178", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDummyReference, "Workaround for dummy reference issue SW HSD#1407112793 and HW HSD#1407806467", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSliceMissingMB, "Workaround for slice missing macroblock issue SW HSD#1507525571", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableClearCCS, "Workaround for green corruption issue with 8K60FPS monitor SW HSD#14013957777", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCodecMmc, "Disable Codec MMC on new platforms due to function not ready", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVeboxInputHeight16Aligned, "Workaround for Vebox input alignment issue on LKF, HW bug_de 1506769438, Make sure Vebox input is 16 aligned", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePowerCompilerClockGating, "Set DisablePowerCompilerClockGating bit. This is to prevent corruption while hiz raw stall in partial span .", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPreventSoftResetHangUsingGamtArbReg, "Set/reset GAMTARBMODE reg bit before and after Soft reset to avoid hangs and prevent HDC invalidations.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDC5DC6, "Disable DC5/6 on SKL", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIgnoreDDIAStrap, "Ignore Strap state for DDI A on SKL", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsRestoreWithPerCtxtBb, "Workaround for a HW issue with the PerCtxtBb and the RS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRSFlushRequiredBefore3DPrimitivePreemption,
           "Resource Streamer Flush required between RS produce commands (Binding Table Pointer, DX9 Generate Active, or Gather Constant) and 3D Primitive command when preemption "
           "is enabled.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHuCAuthentication, "Do not enable authentication when using GuC DMA to load HuC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaModeSwitchDummyFrame, "VEBOX Dummy frame for SKL GT3/GT4 Mode Switch WA. SW HSD#5619023 and HW bug_de#2133079", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAddDelayInVDEncDynamicSlice, "WA for hang on VDEnc with small dynamic slice size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReadVDEncOverflowStatus, "WA for reading VDEnc slice size overflow bit in MFX MMIO ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSklLpt, "WA For LPT with SKL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionDuringPavp, "Preemption needs to be disabled for Pavp workloads on HSW", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUnitLevelClockGatingDisableGMBUS_PCH, "SW WA to disbale unit level clock gating for GMBUS", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUnitLevelClockGatingDisableGMBUS_SOC, "SW WA to disbale unit level clock gating for GMBUS for BXT and GLK", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableChickenBits_Hypervisor, "KBL Display C0 step fix, enable chicken bits when Hypervisor is enabled", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaS3DCurrentFieldLeft, "Required untill HW team provides a solution for S3D current field not changing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableForceRestoreInCtxtDescForVCS, "On Video engine, set Force Restore bit on Context submission", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceNullSurfaceTileY, "Set all RT Null Surface states to have Y-Major tiling to avoid HW hang on BDW", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBindlessSurfaceStateModifyEnable, "Bindless Surface State Base Address Modify Enable does not apply to Bindless Surface State Size", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPreventPavpHeavyModeContextCorruption, "Prevents corruption that can occur in the HW context image when executing protected workloads", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionForWatchdogTimer, "If Watchdog timer is enabled, we need to turn OFF preemption to prevent incorrect reporting of watchdog interrupt",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableEUChangeForSs0DisableDieRecovery, "When Subslice0 is disabled in die recovery mode, CS unit requesting EU resource change can't be enabled",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSlicePowerGating, "Disable Slice power gating to workaround HW hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCur180BufAddressCalcForPipeA, "WA for a HW issue with Cursor 180 rotation on Pipe A", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCHVBxMPOHWSupport, "MPO specific HW features support like Plane CSC, Scalar on Primary plane on Pipe B is available from B0 onwards", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCHVKxPlaneScalarSupport, "Plane scalar support for sprite planes on Pipe B is available from K0 onwards", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCHVMPO, "HW support for MPO is not symmetric across planes/pipes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCHVDisableScalar, "HW support for MPO is not symmetric across planes/pipes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableChickenBitTSGBarrierAckForFFSliceCS, "Set Chicken Bit for TSG Barrier Ack Disable in FF Slice CS, to prevent hangs when Barrier Ram valids gets restored.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBindlessHeapTestSupport, "This WA is to allow bindless heap testing over DX11 until DX_ is ready. For rel_int/debug modes only", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCLVertexCache, "WA to disable CLVertex cache bit in FF_Slice_Chicken register.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendSEnableIndirectMsgDesc, "WA to enable indirect MSG descriptor for split send in GPGPU mode with pre-emption.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStructuredBufferAsRawBufferOverride, "Set all structured buffers as raw buffers to allow DX Tiled Resource null-tile status feedback via LD_STRUCTURED_S",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGpgpuTextureCacheInvalidate, "CS Stall bit in PIPE_CONTROL command must be always set for GPGPU workloads when Texture Cache Invalidation Enable bit is set",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaConservativeRasterization,
           "If Conservative Rasterization is enabled and degenerate triangles are back face culled, set pixel shader kills pixel in the PS extra state programming.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMSFAfterWalkerWithoutSLMorBarriers, "MEDIA_STATE_FLUSH requried after GPGPU_WALKER without SLM or Barriers.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRendCompFeature, "WA to disable Render Compression Feature until C0.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableNonLinearGammaCheckWin7, "WA to block the non-linear gamma curve check for win 7.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBarrierPerformanceFixDisable, "WA to set Disable Barrier Performance bit in HDC_CHICKEN0 register.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceContextSaveRestoreNonCoherent, "WA to force context save/restore access to be non-coherent", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableGapsTsvCreditFix, "WA to enable TSV credit fix because it's not on by default?!", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSkipCaching, "Disable Skip Caching", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLosslessCompressionSurfaceStride, "WA to align surface stride for unified aux surfaces", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcLinearSurfaceStride, "WA to align surface stride for linear primary surfaces", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFbcPsrUpdateOnCpuHostModifyWrite, "WA to allow update by CPU host modify writes on display when FBC in enabled in DisplayPort PSR mode.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDPFCGatingForFrontBufModifySignal, "WA to Disable DPFC gating in the ungated clocks to use for FrontBuffer modification signal", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaLimit64BppScenarios, "Limiting 64bpp support for 1 plane only and single pipe scenario", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa4kAlignUVOffsetNV12LinearSurface, "WA to align UV plane offset at 4k page for NV12 Linear FlipChain surfaces", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableIPC, "WA to disable IPC.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableIPCMemoryConfigWA, "WA to disable IPC.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaIncreaseLatencyIPCEnabled, "WA to increment latency by 4us for all levels when IPC is enbaled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTWM, "WA to disable Transitional WM.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaProgramHalfLineTimeForIPC, "WA to programm Line time to half of Actual Line time value calculated in WM programming", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWatermarkLinesBlocks, "WA to adjust Result Line and Result Block value for Watermark SKL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSamplerResponseLengthMustBeGreaterThan1, "Forces sampler response length > 1 when compute workloads have preemption enabled", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMixModeSelInstDstNotPacked, "Disable HF dist for mix mode select instruction. Even if it's not packed.", WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePooledEuLoadBalancingFix, "WA to Disable Pooled Eu Load Balancing Fix to achieve GPGPU performance gain", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePartialResolveInVc, "WA to Disable Partial Resolve in Victim Cache to achieve performance gain", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePreemptionWithCoherency, "WA to Disable premeption if L3 Coherency is required as both can not co-exist.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReadVcrDebugRegister, "To read the VCR debug register (0x320F4) we disable media clock, read register, then enable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHDCInvalidation, "WA to Disable HDC Invalidation by default", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSplitPipeControlForTlbInvalidate,
           "WA to split pipecontrols that invalidate the tlb in order to force handling IOTLB invalidation for IOMMU on SKL. Note: this is only applies to currently existing "
           "pipecontrols with TLB invalidate",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSbeCacheDispatchPortSharing, "Disable Shared SBE subslice cache dispatch port sharing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWGBoxAndWDtranscoderEnable, "Wa related to enabling of WGtarnscoder and WGBOx ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableLbsSlaRetryTimerDecrement, "WA to Enable LBS SLA Retry Timer Decrement on SKL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCcsTlbPrefetchDisable, "For DX10 performance improvement as recommended by the Bspec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTrickleFeedForNV12, "WA for HW bug: YF NV12 split transaction with the EOB is sending a different blkid in between", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableSoftwarePCDDelay, "WA for HW bug: PCD_Delay registers not hooked up correctly in BXT and GLK PPS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePWMClockGating, "WA for HW bug: To bring down PWM when it is turned OFF in BXT and GLK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSouthDisplayDisablePWMCGEGating, "WA for HW bug: Temporarily disable South Display PWM Clock Gating in CNL, ICL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaNorthDisplayDisablePWMCGEGating, "WA for HW bug: Temporarily disable North Display PWM Clock Gating in GLK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSTUnitPowerOptimization, "Disable STunit Power Optimization", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePixelMaskBasedCammingInRcpbe, "Disable Pixel Mask Based Camming in RCPBE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMtpRenderPowerGatingBug, "Workaroung for a render power gating bug with GW in MTP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePUnitMailboxMMIODisable, "Disable Punit Mailbox MMIO", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetClckGatingDisableMedia, "WA Disable DOP Clock Gating for PM.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetSDEunitClckGatingDisable, "WA for PM to set SDE Clock gating disable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetHDCunitClckGatingDisable, "WA for PM to set HDC Clock gating disable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaStoreMultiplePTEenable, "WA for data getting corrupted going into the TLB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableHostToGucInterrupt, "Enable HostToGuc Interrupt mode instead of doorbell", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReInitRingContextLriPostedWrite,
           "Due to HW bug on CHV, on repeated Cold reboot cycles LRI Posted Write bit was getting reset in the Global Ring Context used for loading WOPCM kernels.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableDefaultEUCount, "Enable Default EU count instead of dynamic value from FUSE register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCheckEU10Disabled, "Check if EU10 is disabled in FUSE register (due to bug) and if so send new EU count that needs to be used for each SubSlice ", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaC0AstcCorruptionForOddCompressedBlockSizeX,
           "Enable CHV C0 WA for ASTC HW bug: sampling from mip levels 2+ returns wrong texels. WA redescribes ASTC texture as 4*w, 4*d and uses only mips2+",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRCCByteSharingDisableForHSWGT3, "RCC byte sharing must be disabled for HSW GT3", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAstcCorruptionForOddCompressedBlockSizeX,
           "Enable CHV D0+ WA for ASTC HW bug: sampling from mip levels 2+ returns wrong texels. WA adds XOffset to mip2+, requires D0 HW ECO fix.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
WaDisableDeepLoopsUnrolling,
"WA to reduce memory usage of tests with large number of nested loops, such as GLCTS ES31-CTS.arrays_of_arrays.InteractionArgumentAliasing tests for CHV CR with 1GB memory.",
WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableDMCForNV12MPO, "WA to enable DMC to wake up the memory for NV12 MPO case", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDups1GatingDisableClockGatingForMPO, "WA to disable clock gating for MPO", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableScalarClockGating, "WA to disable clock gating During modeset for Gen 10", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFirstSyncFlipAfterMPOExit, "WA to do first sync flip after MPO exit", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSendsPreemption, "Disable preemption for sends with non-null src1 to work-around HW hang bug on CNL A0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableSamplerGPGPUPreemptionSupport, "WA Enable GPGPU Preemption Support for SIMD32/64 messages.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableChromaTrellisQuantization, "WA Enable Chroma Trellis Quantization when Luma Trellis Quantization is enabled", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMIPIChangesFromBStep, "WA To limit setting certain fields of MIPI_CLOCK_CTL to AX steppings as per BSPEC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDisableMipiDsrWithExtPhyON,
           "WA to exit MIPI DSR whenever an external display is plugged in (DDI Phy active) and enter when all the external displays are plugged out ", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDisplayYtiling, "WA To disable Y-tiling", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDDdiHPDSwapUntilBStep, "WA To keep HPD pins swapped until B-step of BXTN", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

// Due to the WA for a BXT GWL issue with a different solution on A stepping and B0 stepping,
// we have to use two different flags to address this.
WA_DECLARE(WaOCLEnableSLMSizeGWLWA1, "WA To GWL Size issue until A-Step of BXT", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOCLEnableSLMSizeGWLWA2, "WA To GWL Size issue until B0-Step of BXT", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGlobalDepthConstantScaleUp, "Global depth constant required to be scaled by 1.5 to always give a definite unique depth value", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSetDCFlushOnReadOnlyInvalidate, "HDC L1$ not getting invalidated on read only invalidation from CS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableDC5InPavpActivePeriod, "Display power state DC5/6 disable is required in pavp session active period, impact SKL/BXT.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRasterisationOfDegenerateTriangles, "GEN9+ does not eliminate degenerate triangles neither in wire nor in point mode. Occurs also on GEN7.5, GEN8 when HiZ is off",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAvoidURBAllocationSizeMultipleOf3, "URb allocation size must not be a multiple of 3 times 64B which is cache line size", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMidBatchPreemption,
           "When Per Context Preemption Granularity Control is used and media preemption is not supported, set CS_CHICKEN1 (02580h) to mid-batch level preemption (bit2:1 = 10b) "
           "for media workloads in render engine. Otherwise, there will be GPU hang (b9023364).",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceWakeRenderDuringMmioTLBInvalidate, "Asserts render force wake while invalidating render TLB via MMIO", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

// Due to Hardware issue giving the WA from GFX driver for Surprise Removal (b9024950) HW HSD -
// https://hsdskl.iil.intel.com/hsd/skylake/default.aspx#sighting/default.aspx?sighting_id=4712464
WA_DECLARE(WaAudioSetEPSS, "WA_Set_EPSS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAllowUmdWriteTRTTRootTable, "Allow UMD to update privileged TRTT L3 address  register via BB", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDualMapUntil3DOnlyTRTT, "Dual map Tiled Resources ie on both PPGTT and TRTT until all-engine TRTT.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAuxTable16KGranular, "AuxTable map granularity changed to 16K ", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAuxTable64KGranular, "AuxTable map granularity changed to 64K ..Remove once Neo switches reference to WaAuxTable16KGranular", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisablePtePageSize64, "PPGTT Pte doesn't support 64KB-page indication", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableSysmemInLocalPreference, "Disable sysmem as high P2 preference in local-preferred segment settings, for a specific process (AIL)", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGucSizeUsedWhenValidatingHucCopy, "HW uses GuC size when validing the HuC DMA copy size", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaGucDisable2ElementSubmission, "HW doesnot allow submissions with head==tail which fails 2 element submissions", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaDisable4KPushConstant, "Ensure nonzero curbe start", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaClearTdlStateAckDirtyBits, "WA to avoid message collision in TDL, by not doing NP state ack ", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaSendDummyGPGPUWalkerBeforeHSWithBarrier, "Send dummy GPGPU_WALKER command before HS with barrier to work-around HW hang bug on BXT.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaVFEStateAfterPipeControlwithMediaStateClear,
           "WA to disable preemption between VFE state and pipe control when VFS state is after pipe control with media state clear.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSendDummyConstantsForPS, "Send dummy 3DSTATE_CONSTANT_PS command for PS to work-around HW hang bug.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaUseAuxSurfaceMode, "WA to use AuxiliarySurfaceMode in surface state and set CACHE_MODE1.MCSCacheDisable", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaHwManagedClearConvertDepthFormat, "Ensure the clear depth value for HW Managed Clear is stored in memory, in a correct surface format", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHwManagedClearResolveDepth, "No support for HW Managed Depth Clear", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableHSEightPatchIfInputControlGeq29, "Disable HSEightPatch if input control point count is >= 29, as this leaves very few registers for push constants",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRsGatherPoolEnable, "Always enable Gather Pool with base address zero and size set to max value.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1207137018, "Set the value of RENDER_SURFACE_STATE.Mip Tail Start LOD to a mip that larger than those present in the surface (i.e. 15)", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

// This is added to workaround a HW issue on platforms till gen9, which is shown due to CL 608126
WA_DECLARE(WaDisableSamplerRoundingDisableFix,
           "Disable sampler address rounding fix - which disables U, R, V address rounding in Sampler State, due to a hardware issue on platforms till Gen9.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaForGAMHang, "Disable HW TRTT or literestore in order to avoid GAM hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaGAMWrrbClkGateDisable, "Disable GAMWrrb clock gate", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

/*This issue is applicable from SKL+ 22200 is applicable as non privilege reg list.
  GEN:BUG:1946649 [CNL], GEN:BUG:2137393 [GLK], GEN:BUG:2227519 [KBL] */
WA_DECLARE(WaBlockBLTSubmissionFromUMD, "Disable BLT submission from UMD", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

/*This WA is for aspen issue#7 with residual context cleanup.*/
WA_DECLARE(WaAspen7ResidualContextCleanup, "WA is for aspen issue#7 with residual context cleanup", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaMediaPoolStateCmdInWABB, "WA to avoid VFE/TSG hang, on BXT/GLK GPGPU, by using MediaPoolState configured in MidCtxt WA BB", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPlanePosPlusWidthLessThanPipeHorSize, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1939307", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPSR2MultipleRegionUpdateCorruption, "Wa to set 0x42080[3] = 1 before PSR2 enable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnablePSRExitOn3DLutUpdate, "WA: Write 0x00000000 to MMIO register 0x49028: https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1942473",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableCursorWith1LineInInterlacedMode, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1941458", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableAccessToDisplayIO, "WA: Set 0x162088 bit 0 and 0x162090 bit 0 to 1b to enable access to display IO registers, Before the display initialize sequence.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHDMIRestrict12BpcRgbYuv444Modes, "WA: Restrict HDMI to 8 bpc when the Htotal is >= 5461 pixels and the format is RGB or YUV444, \
         This means standard 4k CEA 24 - 30Hz resolutions cannot be supported with 12bpc and RGB or YUV444 ",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaEnableBitBashingFor4BlockEDID,
           "WA: Do not use GMBUS with 4 block EDID reads or similar cases where there is a wait between block reads. "
           "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1946232",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaVRRDisableBackToBackMasterFlipHWSupport, "https://gfxspecs.intel.com/Predator/ContentEdit/Content/Bun/GEN10_BUG_1945857", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaVRRSynchronizeSlaveAndMasterFlips,
           "WA: Set bit 17 of MMIO register 0x4208C to 1 when using VRR with hardware port sync mode . https://hsdes.intel.com/appstore/article/#/2006613073/main",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaWaitOnLiveVRRStatusBeforeSendingMasterFlip, "https://vthsd.fm.intel.com/hsd/gen10lp/#bug_de/default.aspx?bug_de_id=1947011", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaGTCLockAcquisitionDelay, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1937506", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaHDCP2StatusUpdateToAudio, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1943408", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaCDClkPLLLockCorrection, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1946276", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaRCWaterMarkCalculation, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1938466", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaRecomputeMGPHYRCOMP, "https://hsdes.intel.com/appstore/article/#/1405863085", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaPipeControlBefore3DStateSamplePattern, "Send CS stall PIPE_CONTROL prior to 3DSTATE_SAMPLE_PATTERN and LRR to an SVL register after 3DSTATE_SAMPLE_PATTERN",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceShaderChannelSelects, "Force Shader Channel Selects for missing channels", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRCCCacheMissFix, "WaRCCCacheMissFix", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaTlbAllocationForAvcVdenc, "Set TLB Allocation to VMC=240 for VDEnc performance improvement", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaConextSwitchWithConcurrentTLBInvalidate,
           "Disable GPGPU sync switch preemption to avoid inhibition of context restore if TLB invalidation happens during context switch", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableDOPRenderClkGatingAroundSubmit, "Disable-Enable DOP Clk gating 0x9424[2] around GuC submission boundary, to prevent MidThread Preemption hangs.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaProgramL3SqcReg1DefaultForPerf, "Program the default initial value of the L3SqcReg1 to improve DX performance (on BXT)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaInsertDummyPushConstPs,
           "Send two zero length const_ps, each followed by null primitive, before sending non-zero length const_ps. Send dummy non-zero length const_ps before const_alloc_ps",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaClearTDRRegBeforeEOTForNonPS, "Clear tdr register before every EOT in non-PS shader kernels", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaReducedGMBusReadRetryCount, "To reduce the time delay for GMBus read on SKL", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEncryptedEdramOnlyPartials, "Disable Edram only caching for encrypted usage", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisableEdramForDisplayRT, "WA to disable EDRAM cacheability of Displayable Render Targets on SKL Steppings until I0", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT,
           WA_COMPONENT_GMM)

WA_DECLARE(WaLimit128BMediaCompr, "WA to limit media decompression on Render pipe to 128B (2CLs) 4:n.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaUntypedBufferCompression, "WA to allow untyped raw buffer AuxTable mapping", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisablePreemptForMediaWalkerWithGroups, "Disable Pre-emption bit (bit 11) in register CS_CHICKEN1 for media walker with groups", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaAllocateExtraVBPageForGpuMmuPageFaults, "Allocate extra page in vertex buffers to prevent gpu page faults when Gpu Mmu Page Faults are enabled", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSamplerCacheFlushBetweenRedescribedSurfaceReads, "A texture cache invalidate must be issued between sampling from one view and other", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRetrialOfKsvReadlistHDCPCompiliance, "Call GetHDCPReceiverData function again, if we get failure for first read", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaKBLVECSSemaphoreWaitPoll, "WA for VECS reset failure in KBL. Increased the poll interval in VECS_SEMA_WAIT_POLL(0x1A24C) by 1usec.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaClearHIZ_WM_CHICKEN3,
           "RCZ unit (Render Cash Z), PSD (Pixel Shader dispatcher) is waiting for High Z and then RCZ is the one that is waiting/hang. W/A - changes mode for HIZ clears - clear "
           "every time is needed.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaNV12YfTileHWCursorUnderrun, "Display underrun with Yf tiled NV12 surface + Cursor", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDDIIOTimeout, "Phy enable, Disable and re enable causing Power well enable time out casing display blankout", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaDSIRcompFailure, "MIPI DSI Rcomp failures which can cause image corruption at hot temperatures", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaAlwaysEnableAlphaMode, "Enable Alpha mode in Plane_Color_Ctl for passing DP Link layer compliance. Will remove WA once HW sighting (1604297325) is concluded.",
           WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1405595945, "Add alpha blending source pixel bypass and destination bypass for plane alpha blending.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaEnableVoidExtentBlockPatchingforASTCLDRTextures, "WA for mishandled fixed-to-float conversion in ASTC LDR mode", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(WaDisableKmPresentForRtlSim, "WA to disable KmPresent calls in RTL simulation environment", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaRtlSimulation, "WA for driver to run in RTL simulation environment", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisablePagingFill, "WA for driver to disable paging fill for memory intialization in simulation environment", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaModifyGamTlbPartitioning, "WA to adjust default GAM TLB partitioning to back up C/Z L3 cache traffic", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT(25), WA_COMPONENT_KMD)

WA_DECLARE(Wa_1405543622, "WA to set arbitration priority in arbiter register (0xB004)", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604223664, "WA to set correct L3 bank address hashing", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1405733216, "WA to disable clean evict", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_2006611047, "WA to disable improved TDL clock gating", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1405766107, "WA to reduce the max allocation to CL2 and SF", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPAVPEncryptionOffAtContextRestore, "WA to terminate all encryption sessions at context restore", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaNoSimd16TernarySrc0Imm, "Wa to avoid src0 imm in ternary simd16 inst", WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSSEUPowerGatingControlByUMD, "WA for UMD to program SSEU power gating on GEN11+", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDPFRGatingDisableWhenScalarEnabled, "WA to disable the clock gating to the Scaler's register block when Plane/Pipe Scalar is enabled", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEnable32PlaneMode, "WA to enable 32-plane mode on GEN11+", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaMaskGuCRMRForFlipDone, "WA to to mask/unmask GucRMR register for flip done interrupt", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaArbitraryNumMbsInSlice, "WA to avoid MBEnc stall issue by forcing arbitrary MBs in slice", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaInterlacedmodeReqPlaneHeightMinTwoScanlines, "InterlacedMode requires Planeheight minimum of Two Scalines", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPruneModesHavingHfrontPorchBetween122To130, "WA for prunning the modes which has HfrontPorch Value between 122 to 130 to fix the H/W Bug till Icelake.",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaMPOReqMinPlaneLeftFourBelowHActive, "HW WA - 1175. To fail MPO if plane's left coordinate is less than four pixels from HActive", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// Wa_1406240351 is same as WaMPOReqMinPlaneLeftFourBelowHActive and is applicable ICL+ only
WA_DECLARE(Wa_1406240351, "HW WA - 1175. To fail MPO if plane's left coordinate is less than four pixels from HActive", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMpoNv12Rot270ReqPlaneHeightMultipleOf4, "HW WA - 1106. To fail MPO if plane height is not a multiple of 4 in case of NV12 - 270 rotation or (90 rotation + Horz Flip)",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

// https://hsdes.intel.com/appstore/article/#/14014251458
WA_DECLARE(WaOsRestrictMaxQueuedMultiPlaneOverlayFlipVSync, "By default it will be enabled, OEMs can disable it based of the OS version, since there is an underlying OS bug",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

// Refer : https://hsdes.intel.com/appstore/article/#/22010516885
WA_DECLARE(WaOsRemove64BppSupportFor8kTiled, "With HDR On use case, we are getting an issues where Resoluiton list for 8k is getting greyed out becuase of 64bpp support for 8k,",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaDisableDelayedVblank, "By default it will be enabled, OEMs can disable it based on the need, disabling will result in perf impact when vblank is very high",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOsEnableNv12ForOddWindowSizeMediaPlayBack, "OS WA to allow NV12 enabling for odd window size media playback", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

// Refer to this for more information https://hsdes.intel.com/appstore/article/#/1504753783
WA_DECLARE(WaOsDoNotReportYUVModeIfRGBModeIsSupported, "OS WA for removing YUV420 mode from the mode table if RGB Mode for the same is present and supported",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

// Only for RS5 : Bug Details https://hsdes.intel.com/appstore/article/#/1506980552
WA_DECLARE(WaOsUseEDIDLuminaceValueForEdpHdr, "OS WA to Use the EDID MaxCLL,FALL and MinCLL values for eDP HDR", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

// From 19H1 : Bug Details https://hsdes.intel.com/appstore/article/#/1506980552
WA_DECLARE(WaOsUseEDIDLuminaceValueInSDRModeForEdpHdr,
           "OS WA to Use the EDID MaxCLL,FALL and MinCLL values when not in HDR mode and use the AdjustTargetColorimetry Value only in HDR mode for eDP HDR",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOsAsyncFlipsDuringVideoPlayback, "OS WA to convert async flips to sync during video playback", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaOsRecommendAllTargetModesAsMonitorModes, "WA to report all target modes as monitor modes", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaOSReportVotEdpAsVotInternal, "WA to report VOT for eDP as Internal", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOSUpdateDurationToMaxOfAllPlanes, "WA to disable DMRRS feature when multiple planes are enabled", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOSEnableVBIOnModeSet, "WA to enable VBI on SetTiming", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOSReportDummyChildIdForDisplayLessAdapter, "WA to report a dummy VidPn target to OS for Display less adapter", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOSDisableMpoPlanesPostSetTiming, "Temp WA for RS2 OS issue where post mode set plane info is lost in OS and it does not disable planes > 1", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(WaOSLdaFseFlipRect, "Temp WA for SV2 OS issue where in Full screen excl mode, null rects are passed in Flip call", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

WA_DECLARE(WaPlaneSizeAlignmentForXPanningOr180Rotation,
           "WA for HW bug: with 180 rotation panels, alligning plane width to multiple of 64, 32, 16 for NV12, YUV and RGB planes respectively + To fail CheckMPO if plane x "
           "offset is not 32 pixel aligned",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaSkipPortRegisterAccess, "WA for HW bug: access phy port registers in power up sequence is resulting in a hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WADisableGTPAndSetISPDisable, "Disable Gather Pool Allocation when Resource Streamer is disabled. WA applicable for Gen9", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSamplerFIFOBug, "Sampler FIFO bug", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_220160979, "Windower hardware will filter all semi-pipelined states except for hiz-op if unchanged changedfrom the current state (ICL LP B0+)", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_220160786, "Subspan combining in Pixel Pipe for higher thruput efficiency (ICL LP B0+)", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaSetPerfSuperQueueFullLimit, "WA to set default value of arbiter register 0x902C[9:3]", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1406306137, "WA for HW bug: an EU with atomic HDC and SLM messages cause a hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604420678, "WA for HW Bug: Combining Subspans with blend enables causes corruption for some RT formats", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMultiChannelAudioForDP, "WA for HW bug: Enable maximum 2 audio channels for GLK and CNL until CNL C0 stepping in case of DP display.", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1406817180,
           "WA for HW bug: TimeStamp and InfoFrame packets are not handled together for DP display, WA: program N Value in driver to limit TimeStamp packets to 1 per frame.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_220579888, "On 3DSTATE_3D_MODE, driver must always program bits 31:16 of DW1 a value of 0xFFFF.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406252905, "WA to disable slice common PTBR discard in case of hang signature.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2006665173, "The WA is to disable blend embellishment in RCC.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableDcStatesWhenPSR_3DLUTEnabled, "Disable DC states when both PSR & 3DLUT enabled", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaHardHangonHotPlug, "CNL PCH has a chance of hang, Program 0xC2000[11:8] = 0xF before enabling south display hotplug detection", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaForIcompVarations, "WA for Screen flickering due to large Icomp variations impacting port link voltage", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable10BpcHDMIForYUV420WithHBlankMod8Reminder2, "https://hsdes.intel.com/resource/1405510057", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisable10BpcHDMIFor4XPixelRepeatModes, "https://hsdes.intel.com/resource/1405529773", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCheckCrossComponentPredictionEnabledFlag, "Wa for ICL A0/A1. The WA only needs to print the flag out once the decoding hit it", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaCSStallBefore3DSamplePattern, "WA to make sure engine is idle before programming 3DSTATE_SAMPLE_PATTERN in context restore", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaInitCDClkNewSeq, "WA 1183 : New Init Sequence as WA for failures with eDP 2.16 and 4.32 GHz link rates and CDCLK 308.57 and 617.14 MHz", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaForcePLLDisableEnableForFreqChange, "WA: PLL frequency should not be changed while the PLL is enabled", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaIncreaseAuxChVswing,
           "WA to increase Aux channel voltage swing as its observed to be too low with some type C dongles. Adjustment can be applied to all external ports even if they are not "
           "going to type-C. This programming does not apply to Aux A",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableRenderComputeDataSharing, "On TGL_LP A0 Si Disable Render Compute Data Sharing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableDARBFClkGating, "WA:PM Rsp is not sent when plane is turned off at around the time that a PM fill Req is received by display, WA: disable arbiter clock gating",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaEnableFloatBlendOptimization, "WA to enable Float blend optimization bit in Cache_Mode_SS register. It is a privilege register, UMD should not write it",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaTLBInvalidationOptimization, "WA to skip TLB invalidation when the process' TLB is already invalidated. This is an OS WA for performance improvement.",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaTLBInvOptInGmmUpdatePT, "WA to skip TLB invalidation flag in GmmUpdatePageTable. Remove this WA as part of WaTLBInvalidationOptimization Removal ", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1504612072, "WA for Posh SVL Ack hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaRenderConstantStateOptimizationEnable, "WA to enable state delivery optimization for 3D state commands for POSH enabled - Gen11LP and LKF", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaRenderOtherStateOptimizationEnable, "WA to enable state delivery optimization for 3D state commands for POSH enabled - Gen11LP and LKF", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaReadHitWriteOnlyDisable, "WA to disable RCC clock gating. There is a clock gating bug in RCC unit which results in hang for Read Write Only scenario.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableEarlyEOT, "WA to disable Early EOT of thread.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableRc6ForPerfMeasurements, "Wa to disable RC6 Wa Batch buffer. There is a metrics bug (on CNL+) where defective data are returned when RC6 is enabled.",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaVFUnitClockGatingDisable, "WA to disable VF Unit clock gating in register 9434(bit 20).", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaUseStallingScoreBoard, "Wa to use stalling score board. There is a MA bug (on CNL C0) which results GPU hang and requires to use stalling score board.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// TODO: Get perf data for Gen11+ and enable it.
WA_DECLARE(WaL3LraGpgpuOverride, "WA to change L3 LRA register for GPGPU to new values, it helps in perf improvement of HEVC workload", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1209644611, "Clone from gen10lp: CNL: Blitter: Need Bspec update for updating workaround for a known issue found on Apple", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1405638134, "VRR off on GT flip test failing with DDI CRC miscompare: Turning off from VRR MaxShift with HW Pipeline full", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1405916266, "[Gen11LPB0] MHTF: Filter semi-pipelined states at WMunit", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1406185002, "[Gen11LP B0] MHTF: Add a mechanism to disable the PS scoreboard with pipelined state.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_220818474, "Incorrect blue channel value when sampling from R32G32_FLOAT surface with border texture addressing mode", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_2201039848, "AUTOCLONE: Clone from gen10lp: CNL C0: Mid thread preemption hangs with sends instruction", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406609255, "TDL prefetches for binding table pointer is not shifting based on binding table pool alloc and GT mode bit 10",
           WA_BUG_TYPE_HANG,                                        // pagefault
           WA_BUG_PERF_IMPACT, WA_COMPONENT_OGL | WA_COMPONENT_D3D) // expect 3D UMDs to use this WA

WA_DECLARE(Wa_1406614636, "Use {NoPreempt} when r2 is used as src0 of sends in regular kernel.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406680159, "[Gen11/Gen12] GWL Clockgating Issue on EOT & Barrier Ram Valid", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604302699, "Gen11 HP : GPGPU GT: Coherent L3 & LLC cacheable full $Line writes did not implement HAS defined flow when Line is in M/E state", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604432879, "POCS: semaphore wait on reg poll is not part of Ok2switch in POCS", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1604542237, "AUTOCLONE [Gen12] : SVL should use gated version of cuclk or crclk to sample non-pipelined states", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_2201674230, "GFXDRV: Hang in cs tsg and eu with OCL workload test_ocl_3D \half\test_half64.exe vloada_half -w CL_DEVICE_TYPE_GPU in ICL-LP", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2201832410, "WA to disable the GWL clock gating", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604555607, "TGL-LP WA - Gang Timer set for TDS dual disptach", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT(70), WA_COMPONENT_D3D)

WA_DECLARE(WaSetIndirectStateOverride, "Enable Indirect state override to dynamic state", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaDisableHizFor16xMSAA, "WA to disable Hiz for 16x MSAA sampling", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAlignYUVResourceToLCU,
           "OS Page fault caused by HEVC PAK, it seems PAK is expecting the source and recon surfaces to be allocated in a way so they are always aligned to the LCU size",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaEnableHardwareBypassForPerPixelAlphaValues0AndFF, "Enable per - pixel alpha blending to bypass alpha when the per - pixel alpha value is FF or 00",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaPerformDisableDuringModeset, "Disable display as part of enable call flow", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaSendLRMBeforeNotifyInterrupt, "Add dummy LRM to read Gfx memory before Notify interrupt", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPreSiDataFlushBeforeNotifyInterrupt, "Split the Pipe controls/ MI_FLUSH_DW to write Gfx memory and generate interrupt separately", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaOptimizedGTTInit, "Optimize Initialization of GGTT/PPGTT in local memory", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1406606421, "[Gen12LP B0] Gen 12: HDC RTL does not support 16-bit typed atomics", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa2DSurfacePitchAlways64BAligned, "[DG1 A0] Gen 12HP: HDC sequencer combining/compressing writes to one cacheline", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_1406798080, "TGL GFXDRV Regression in sanity suite ww05 model - CS H/W fix", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa32bppTileY2DColorNoHAlign4,
           "Wa to defeature HALIGN_4 for 2D 32bpp RT surfaces, due to bug introduced from daprsc changes to help RCPB generate correct offsets to deal with cam match",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(WaDisplaySupport39BitPhyAddr, "Wa to ensure that display access physical addresses below 39bit address range, corner case for ADL-S/HU", WA_BUG_TYPE_SPEC,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(
Wa_1406689936,
"PoshPreemptionTilePassInfoCmd - Tile Count value programmed must be same in the 3DSTATE_PTBR_TILE_PASS_INFO command programmed for 'Start of Tile Pass' and 'End of Tile Pass'.",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1406838659, "WA to disable the CGPSFunit clock gating", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableRepackCompression, "Wa to disable repacking components of certain pixel formats before compression in JSL.", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_1406941453, "TGL LP : Enable Small PL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22060034, "Clone from gen10lp: VRR: sending master flip immediately after enabling VRR causes hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1405510057, "ICL: HDMI 10bpc w/ YUV420 will fail with resolutions that have a remainder of 2 when divided by 8", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1405529773, "hdmi symbol mismatch in hblank when pll=4", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1406796446, "ICLLP FF DOP clock gating causes deref from TDL to be lost in SBE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604578095, "HS Hang & TDG mismatches when dual_instance_enable is zero AND HS is handle limited.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1805811773, "Invalid stencil buffer access leading to page faults (Gen9) and Fulsim crash (Gen11LP)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_2006604312, "[RTL issue] Clock gating issue in dpsrunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_2006613073, "VRR port sync mode - Flips in Slave Pipe are not serviced in sync with master pipe", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_2202389218, "Clone from gen10lp: CLONE from gen9lp: PROMOTE from skylake: Invalid occlusion query results with Pixel Shader Does not write to RT bit",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1405764967, "COMMON_SLICE_CHICKEN2 (0x7014) needs to be non-privileged on ICL HP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)
WA_DECLARE(Wa_1406950495, "ICL B0 -  EU hang with Timespy(DX12) workload", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604643595, "Non RCC aligned mip should not be fast cleared.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(WaPSThreadPanicDispatchDisable, "WA for disabling panic dispatch till Icelake D0.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaPruneModesHavingHBlank106, "WA for prunning the modes which has HBlank 106 to fix the H/W Bug till Icelake A0.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaHEVCVDEncForceDeltaQpRoiNotSupported, "DG2: force delta qp roi will be supported from B stepping", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaHEVCVDEncY210LinearInputNotSupported, "TGLLP: Y210 Linear and Tile X input will be supported from B0 stepping", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaHEVCVDEncROINumMergeCandidateSetting, "TGLHP: NumMergeCandidate setting of 3322 for ROI will be supported from B0 stepping", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaVDEncStreamingBufferSupported, "TGLLP: AVC/HEVC VDEnc streaming buffer will be supported from B0 stepping", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaForceAllocateLML3, "workaround for XeHP SDV deadlock issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaForceAllocateLML4, "L4 workaround for XeHP SDV deadlock issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1805992985, "ICLLP GPU hangs on one of tessellation vkcts tests with DS not done.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

/*
Workaround Name: WaSamplerSupportForHeaderlessMessage

Description:
IGC always sends headerless message to sampler for ICL+.
Sampler_Mode register (0xE18C)[5] defines support for headerless sampler messages.
bit[5] = 0; Headers must be used on all sampler messages for Pre-emptable contexts.
bit[5] = 1; Headerless sampler messages may be used for pre-emptable contexts.

Issue on Gen11:
The default behaviour of this register on Gen11 is bit[5] = 0;
This results in PF on GPGPU_WALKER command in case of Mid-Thread Preemption.

Solution: Sampler_Mode register 0xE18C[5] should be programmed as 1.
All UMDs will need to program this before sending GPGPU_WALKER command.
In spirit of simplicity , KMD is implementing this requirement.
Please note, this is not a generic KMD requirement and KMD is just implementing this
for sake of simplicity.

Gen12:
The default behaviour of this register on Gen11 is bit[5] = 1;
https://gfxspecs.intel.com/Predator/Home/Index/11507
https://gfxspecs.intel.com/Predator/ContentEdit/(S(rtxuccmyvzti0vkkv3k554dd))/Content/Bun/GEN_HAS_1209978232

As this is fixed in Gen12. This WA should not be ported to future platforms.
*/
WA_DECLARE(WaSamplerSupportForHeaderlessMessage, "Program sampler to support headerless message", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1305657336, "OVR Issue where initialize that follows the restart is not deferred causing an invalid page to be allotted for storing the tokens", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1207126087, "FPF - AUTO CLONE from gen10lp: CNL GT: Vsim cleanup. GAM SCB Test case Virtual address bits", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1405856998, "The Aux Rcomp values get lost because dig-pwr gating is enabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_1406497326, "DCIPHSUNIT: CCSPAVP Indication Not Factoring in Stall ", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1406909873, "mem_diff Corruption in WGF11Compute in ICL-HP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_2202751293, "Clone from gen10lp: CS  not reporting idle if context switch to idle with watchdog armed.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1806114211, "[ICL-LP][3DC] Unigine Heaven/Valley colorful rectangles/flares corruptions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1407240128, "Gen11 TDL - Issue with Message Channel Ack Getting Dropped", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD | WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(WaDisablePFinPFINT, "Disable PF in PF INT to avoid more PFs from HW till the engine reset is complete", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaDummyFixWhenPFRecoveryInProgress, "Program the SW Fault Repair register with Dummy fix when PF INT is received during recovery", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22050150, "Clone from gen10lp: CLONE from gen9p5lp: HDMI violates HDCP spec with null packets spilling into Keepout region for 1920x1200 with audio enable case",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_220137458, "Clone from gen10lp: MSB replication and 16 to 12 bit round off causing unexpected pixel changes", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_220325445,
           "Clone from gen10lp: AUTO CLONE from gen9lp: 2160x1200@90hz HSYNC[106px] Seeing progressive timing issue on HDMI port for a custom resolution HDCP enable case",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406182298, "ICL - Audio - Layout 0 to 1 changes result in dacbe audio output corruption / hang if last sample sent is non-multiple of 4",
           WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406460724, "D11: arbf clockgating not waiting the last data to exit from darbf before disabling darbf clock", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604331009, "Gen11 ICL_A0 Display  : Pipe Underflow seen When Trusted Sprite and Cursor is enabled with HDR plane and doing disable non KVMR planes",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2204188704, "PSD is enabling panic dispatch when there is SBE hold, causing issues with thread termination", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1604061319, "Gen11_FPF CS Rtl not sending flush to VF and SVG after Fence during PC sequence of commands causing hang at ffclt", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

// This WA is applicable only for Gen9 platforms.
WA_DECLARE(WaAllowUMDToDisableVFAutoStrip, "Sw Wa to disable VF autostrip for Titanfal and Lego Ninjago work loads from UMD", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaMapDummyPagesForWhitelistedApps, "Dummy map the allocations for Apps which are white listed by UMD passing the flag during create context", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaCheckCryptoCopyRollover, "Gen12 SW WA for Audio Transcryption Issue", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaCheckTranscodeAppCharRegister, "Gen11/Gen12 SW WA to check app char register for transcode session creation", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(WaReadCtrNounceRegister, "Gen11 SW WA to check widi0 kcr counter nounce register for secure encode", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1605461763, "Gen11 LP - Thunder War hang with FF units not done. VFCACHE is in deadlock", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1605541469, "Gen11LP: OGL CarChase Hang : POCS needs to do command cache invalidation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1406740894, "[ICL_LP] [B0] OGL conformance blendFunc test miscompare on gen11_trunk_common-18ww01b_EMUL model", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1806068545, "[ICL][D3D11][HLK][3DC] WGF11ResourceAccess test failing in Discard\ResourceView1\RenderTarget test group", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1305770284, "[3DC] GT Hang with Subslices PSD hang running OGL apps", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1605460711, "GEN 11 LP SVL Hang when running DX12 + Media", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406697149, "Default value of the control bit that controls the dropping out put to the client Data return from Bank is Incorrect.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1407352427, "Disable PSD clock gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1806230709, "[3DC]Page fault when access border color from SAMPLER_INDIRECT_STATE in POSh.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1407596294, "Direct3D11 on eDP hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1408615072, "Assassin's Creed UAV counter hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1806186540, "[ICL-LP]Hang on 3DPRIMITIVE indirect when preemption is enabled during Carchase", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1407685933, "Superbible6 hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1606682166, "[ICL-LP]Incorrect TDL's SSP address shift in SARB for 16:6 & 18:8 modes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1407925466, "ICLLP :  3DSTATE_SAMPLE_PATTERN is not restored as part of POCS CTXT Restore", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1605967699, "[TGL-LP] Hang on stencil resolve.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

// This is a WA for enabling Medusa DCN on platforms - https://hsdes.intel.com/appstore/article/#/1407002653
WA_DECLARE(WaAddMissedHwWhitelistRegisters, "SW Wa to allow UMD to read from registers which were made priviledged by medusa DCN", WA_BUG_TYPE_FUNCTIONAL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1506855762, "OVR causes a Page fault when running out of free pages in PTBR PAGE POOL", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1408224581, "WM needs extra commit message to get the correct value of stencil state", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1604278689, "Issue with FBC Modify/Clear message generated on GEN11 with color cached in L3 (tile cache or data cache) in PTBR mode.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1306055483, "[ICL][B4] TDR on WGF11RenderTargets test with calc.bat", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa16KInputHeightNV12Planar420,
           "Corruption if NV12 input && input height > 16352(16384-32) && planar420_8 read. SW sighting HSDES#1606071163, HW sighting HSDES#1506950039 ", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(WaIgnorePlaneSurfLiveAddressOnPlaneEnable, "On D11.5+, Plane Surface Live Address is not getting update on Plane Enable, which is causing OS TDR",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(WaNotifyAsyncFlipCompletionInFlipCall, "On simulation, flip done interrupt reporting is not accurate, so let OS know the Async flip completed in Flip call itself",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(Wa_2006625184, "[SSCLT] Tdl RTL fix for clock gating issues with ctx_save_ctr signal", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1406872168, "WW09.4_TGL_ET_1405_Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407528679, "while loop cases causing issues in jeu fused mask", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407917427, "HDC L3 write moves forward for a L1 cacheable write when Sampler is stalling and can result in RAW hazard", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407928979, "GFXDRV: TGLLP DX11 CRYSIS3_AB-G3_IVB-CAP30_F00038 Hang - Bspec update needed", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1605787622, "DualContext : During CSB update GAM will not have dualcontext information causeing issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_2006704411, "[Gen12LP][SVM][Gen12LPB0 Revisit] Cs - Gam Deadlock after Root Entry Not Present Fault", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaAllowPMDepthAndInvocationCountAccessFromUMD,
           "UMD needs to access PM Invocation count and PM depth count registers, which needs to be whitelisted from SW until fixed in HW.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2205427594, "AUTOCLONE: ICL LP: Datavalid of the state generation is not de-asserted when a stall happens at the end of the Macroblock during concealment",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1606376872, "Gen12LP : AMFS : Multi Eval perf test is having traffic only on 3 TSL ports instead of all 6 ports during the 2nd half of the run", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1407901919, "HDC: HDCTLB tdl_mode bits incorrectly decoded for hdctlbl3arb", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606679103, "[CLONE from Gen11lp]: XeHP: SARB to correct address shifting for TDL's SSP accesses for it's effectiveness", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaBlacklistL3SQCREG4,
           "Writing to this register is suspected to cause a ring hang. Blacklisting this register from CFL C0 to avoid this since it has been added to the HW whitelist",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606700617, "GTPM:GEN12 : TRTT_Multi_engine:[memoryPathStress_600960]:[memdiff]", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1408936778, "D11 pipe seam excess double buffer mask bits incorrect in bspec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407939571, "Firestrike Performance Drop Due to DAPRSS Float Blend Optimization", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606931601, "GFXDRV: TGLLP dx10 whql test WGF11Filter_Filter\Mip\Linear\3D:8000 failure on emulation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableMidObjectPreemptioninUMD, "Disabling MidObject Preemption in UMD around Optimized InstanceID enabled 3D Primitives", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEnableWriteToOAPERFReg, "Enabling Write access to OCA Perf registers, required for instrumentation.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaAllowUMDAccesstoOARegisters, "Allowing UMD access to OA registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1406952165, "AUTOCLONE: D11p5 LKF1: MST+VDSC : VDSC_deleteAddStream test failing with underrun", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408136926, "LKF: plane_surface_live_address does not get updated at next vblank when plane is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408264532,
           "[Gen12LP : Backport from DG1] : PSS X-prop issue in quad_valid when we see an unlit poly on the back of a chg marker with no SIMD modes enabled by the programmer",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1806565034, "Sampler L1 set aliasing in GTA5  g-buffer draws", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1408556865, "PS Invocation Count and PS Depth Count unavailable to UMD", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1408981979, "Change MBUS_DBOX_CTL Bcredit default  to 12", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408908852, "[ICL-LP][D0][1x8x8] Rome 2 Dx11 Stream - VF Bank Collision Bug", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1606857333, "DG1 Emulation: PixelAdvanced test failing with cat interrupt error", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1606928324, "DG1 Emulation: l3RangeFlush hang - flush range address register is getting swapped", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607087056, "ICL-LP LNI completion clock gating issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1506917727, "[Gen12] [CP][TGLLP][Emu]MMC + PAVP unalign decode hang @2nd frame", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1408767742, "[ICL-LP]Corruption observed if TE DOP Clock Gating enabled - Batman AO - DX11 - G3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409178092, "[ICL LP D1]: 3-strike MCA with SVMBench application", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1807004938, "AUTOCLONE: [ACS] [ICL-U] Sandra - Observing TDR while running the benchmark with eDP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409085225, "[XeHP][GPSS] TDL urb ctrl hang in PM flexing case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607076429, "TGLLP : pipe3d: HDC sequencer combining/compressing writes to one cacheline", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406756463, "ICL LP: A2: Sampler chicken bit 0xe190[0] to disable DFR doesn't work properly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407859004, "PSMI  n/8th interrupt write to GUC (0xC4B4) is not blocked when GT endpoints are not available during RC6 exit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409273501, "[Apple][ICL-YN] Depth buffer corruption when state cache invalidate is triggered from POCS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604402567, "AUTOCLONE: VFURB dropping data in some scenarios involving 256 bit element format ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604727933, "pipe select command changing media-sampler dop on incomplete preemption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407723970, "Disable Vertex Components Packing for 64-bit formats", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1507169263, "[LKF B0][TCSS] [PO] [Display Port over TypeC] Display Port Aux transactions are failing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_EnableGDieLmemInit, "Initialize Gdie local memory in pre-si", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1408979724, "E2E Compression - X-propagation from DAPRSS on CoarsePixelShading_CFG83", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409178076, "DAPRSS Data Mismatch on dap_cps_random for R11G11B10_FLOAT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409207793, "DAPRSS EOS Mismatch and OA X-Prop (FIFO Desync)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409217633, "DAPRSS - X on cla_vld, cla2, and Pixel Mask for 16X MSAA", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409226450, "ICunit writes tag on a flushed request, leading to incorrect data in cache", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409252684, "DAPRSS RTL Dropping CP Subspan Due to Alpha2Coverage", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_2201730850, "[Bspec Only] Z Clear Color Location", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1408413580, "ICLLP-U - : Hardware hang on running Transcode app+ Netflix", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1607156449, "Gen12LP: Flush mismatches and preemption post sync operation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607030317, "Suspecting issue on CCS active ctx IDLE flush due to not sending to VFE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607102045, "[XeHP] PSS is not aware of viewport pointer change resulting in overlapping cpsize", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1306463417, "ICL-U TF - GFX Hang Seen at 1.1 GHz with Final Fantasy 14", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607027200, "[Clone from XeHP][GPSSCLT] MI_Predicate command dropped by CCS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1408961008, "Underrun seen on PM fill with LP WM1-7 disabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409392000, "[GEN-12LP] [UNIT DAPRSS] Data Corruption with CPS + Dual Source + Dual SIMD8", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409420604, "[TGL A0][PO] Command Streamer hangs on Flush Control ( gpucaps Viewer)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2201998765, "AUTOCLONE: Clone from gen10lp: CNP PCH GMBUS i2c DDC clk first cycle fails HDMI compliance check >100khz", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1506657464, "[EHL][Pipe2D]: MIPI DSI Lane data not coming properly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406337848, "Atomic operation does not work on compressed data", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607186500, "[Gen12LP] CS  should look for rd completion and credits from GA before clk gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409142259, "[Backport from XeHP] [UNIT DAPRSS] Color: daprss_gadss_ss_ss_phase0_sample_mask_cpq_mask_cp_blend_en and cp_blend_no_rd Mismatch", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409347922, "[GEN-12LP] [UNIT DAPRSS] Color: RTL Sending WMBE Stats Count When Fulsim is Not", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1606664663, "virtualizationCommandSecurityConcurrency* test memdiff-  issue in OAG reg read", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606932921, "[Gen12 LP B0 revisit] CS is not waking up cfclk when specific 3d related bits are programmed in pipcontrol in compute mode", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1806527549, "GFXPERF: Shadow of Mordor: frame 253 hang in WW40d model", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409077218, "AUTOCLONE: dmux_transen signal falls a clock prior to vblank_rise", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409210145, "DPT should send VRR enable indicator to DCPR even while Push mode is enabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409497877, "[XeHP SDV A0][DG2 A0] - L3 Range Flush without eviction cannot be used. Until B0 stepping, Tile Cache Flush will be used instead.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1406928334, "TGL - Audio 8K1port - For certain VDSC bpp settings, hblank asserts before hblank_early, leading to a bad audio state", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407909967, "[TGL LP] HW whitelist OA registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
Wa_2207587034,
"[Trending FPF][HSLE] GAM needs to service SW initiated Register based invalidation even if the engine is power down [ causing windows boot hang  as SW keeps polling on it ] ",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1606662791,
           "[Gen12 LP A0]: AMFSTest_835726 test failing with x popagation from SARB, due to state_base_Address implicit flush not flushing DC before reprogramming states",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1606788787, "[Gen12LP B0Fix] CCS BE ctx image is not correct", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607063988, "Gen12LP B0 SRIOV: CS doesn't go idle after ringdone. ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507096982, "Vs-CL Edge Flag mismatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607138336, "GEN12LP : Deadlock between pwr management (blocking context switch ) and context switch -> Corner case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607225878, "CMD_BUF_CCTL - 2084 register does not get context save/restore correctly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_2201643543, "DISPLAY ENGINE needs to configure SSCEN is DLCPLL register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409328477, "LSQC not rejecting snoops when in LKUP_REQ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409342910, "[TGL GT2 A0 PO] [DX12] WGF11RenderTargets failure", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1807690870, "AUTOCLONE: MI_ATOMIC uses wrong address for atomic operation in RCS.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607297627, "[Gen12LP B0] CS should stop making new DMA req once decided to go to RDOP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409336315, "[DEFER TO XeHP SDV:B0] [GEN-12HP] [UNIT DAPRSS] Color: RTL Data Corruption on DS8/CPS/DualSource", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607314724, "AUTOCLONE: GEN12LP : CSB update and interrupt are not sent on element switch with RCS done and POCS not done.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409502670, "[XeHP] XeHP SDV: Unexpected fault report with unexpected address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1607367895, "FFCLT SV Random - TED runs - VF,VS hang ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607138353, "[Gen12LP] RCS reports inconsistent context status in case of Head = Tail and Posh Freeze", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableLogFlushToFile, "Wa to avoid in loop GuC log flushes", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableMediaLogFlushToFile, "Wa to avoid in loop Media GuC log flushes", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409600907, "Gen12LP - Fifo full results in multiple flush dones resulting in eventual hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409086356, "[DG1][SW] Read to RCU_CHICKEN (0x149b0) fails right after RCS is powered up", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409689360, "FBC: Corruption with FBC enable/disable sequence when MPO is enabled in SKL", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507100340, "[Revisit XeHP B0 ]PS Invocation Count and PS Depth Count unavailable to UMD", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409725701, "GFXDRV: XeHP SDV DX11 ww29 tdg Homefront Corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607030476, "XeHP: Pipeblt : Support of Buffer, Structured Buffer, Scratch and NULL  Surface in CopyEngine", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607306630, "Gen11 : RTL going from active to idle unexpectedly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607458937, "[Gen12LP] Protection reset flow and Idle flow clashing in CS/CCS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408330847, "PSR2 in Manual tracking stalls pipe when manual tracking is enabled before SU frames", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409460247, "Clone from XeHP SDV: GFXDRV: XeHP SDV Firestrike f556 SVL Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409639622, "[XeHP] Unexpected fault report when rd/wr bit is corrupted in TLBMOD", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1409842195, "[XeHP] XeHP SDV: Null Read cycle not treated as Null after write perm fault on the same 64KB page", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_1607359242, "compression_en and aux_mode set for stateless compression", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409081093, "XeHP: [MERTXG_PSMI] The upstream_capture_throttle_en bit in register MERTG_PSMI_PRIORITY_THRT_HYST should be ctx restored.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2206241108, "GFXDRV:[XeHP SDV][pipeGT emulation] DRIVER PROGRAMMING: Blitter hang on render workload or after boot", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1606784864, "XeHP:: L1 Cache WriteBack", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606888369, "XeHP: Explicit Port for GuC - GuC Inter Tile Communication", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606909735, "XeHP: Memory protection unit (MPU)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606933487, "XeHP :: GUC+ multi-context test hang at doorbell arming stage", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607031484, "Guc Bspec & FW updates required", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607135819, "[Debug]: Bypass MPU programming during Boot ROM execution on Pre-Production devices", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607662426, "XeHP:Pipe3D:TBIMR: X prop in CL unit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607854226, "Non-Pipelined States from RCS to SVL should be on CRCLK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607268193, "RKL SV emulation : B-spec update required for RKL- half_slice_chicken6[14:11]", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606955757, "[GPSSCLT] [XeHP] Multicontext (LB) : out-of-order write-read access to scratch space from hdctlbunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_1409498409, "E2E Compression - BLT CCS write corruption to uncomp surface - xy_specialCopy_256B_LM2LM_CFG0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408990602, "[TGL][Media][HEVC_VME][Win][Emul][FI1.0]: Dual Context hang on concurrency test", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1607307600, "WM RTL enhancement for the Xprop caused to due workaround of adding pipe control before 3D STATE Coarse PS pointer", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409473501, "[XeHP : XeHP SDV] Walker cycle from tile 1 going to DDR intf in tile 0 is not routed to MDFI but routed to CI instead by request streamer",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409751771, "XeHP: GTPM : OA sends interrupts on funny IO path and has not moved to SG path", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409359629, "Gen12LP/GT1/DG1/RKL: Dec400 issue - flush request on 1 port sets cache line to Pending state incorrectly on another port.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607658902, "XeHP SDV Perf: 3D_STATE_3D_MODE State decoding issue (A0: Metal ECO + WA)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1408973011, "bspec updates needed for removed chicken bits/clarification", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607390583, "[XeHP] OA buffer size calculated in RTL is less than the programmed value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010035994, "[XeHP SDV][Sampler][SSLA] Issue with pipelining of  power optimization signal", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_14010017096, "[SECURITY] Accumulator is not currently cleared with GRF clear exposing its content to new context.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1409877655, "[DG1] Display IP reserves lowest 1MB for Legacy IO", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14010013414, "Need BSPEC Update to indicate initialization of Address Registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409804808, "[TGLLP][A2] 3DMARK_NIGHTRAID_DX12 - CS not done on PIPE_CONTROL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607304331, "Gen12LP B0: DS GS checker mismatch on UAV increment marker", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607720396, "GEN12 DG1 B0 : PIPE3d: DualQ : So-Eu return mismatch causing memdiff -t multiContext_Preemption_1133061", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1507384622, "PIPE3d : WMBE mcr_pkt_data mismatch -t PixelAdvanced_876532", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409807616, "Tracking HSD to update BSpec to add back support for Tap Discard in XeHP SDV BStep", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409979015, "AUTOCLONE: TGL MCR Issue with DEC IP Wrapper for  VDBOX2  mimio address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010103792, "TGL PSR2 Manual tracking does full frame update if the previous SU end is programmed to last block + 1", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607488474, "TE Hang - TED runs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607937755, "VCS/VECS to L3 flush request must be go after unit FLUSHDONE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1409371443, "[TGL-A0][PO] GFX: System hangs when performing FLR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1407902540, "[CLONE] TGL: Allow Double buffer update disable register bit default should be 0 instead of 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607983814, "TGLLP:MOCS logic in render reset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409954639, "XeHP SDV : TDL -EU dop gate need repeater", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010216232, "[RKL] Distributed Doorbell register(0xD08) has incorrect data", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409723837, "XeHP : msc_sampReso_4xSml_CFG0 test failing with x-prop at GT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409825376, "[TGL GT2 A0 PO] CPU reading (Display offsets) 0xA0000-BFFFC causes CATERR at UEFI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010204209, "GFXDRV: XeHP SDV OCL Bruteforce log2 Failure", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507106434, "WM dropping transactions on AMFS_TXT_PTR-only state change", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409932735, "[TGL-U PO]Corruption is seen on the top part of the Edge browser during Netflix AVC/HEVC playback at 4K resolution.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010018976, "TGL LP: Back to back read and flush order issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408785368, "Gen12LP : Official drop from dec400 for the TSC hang issue - Bstep", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010254185, "TGL: Last block not updating when continuous full frame fetch is set", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607934025, "[VEBOX][TGL]: 3dlut + Gec_at_back VE-SFC test hanging for slow ga rd-return schmoo case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(Wa16kWidth32kPitchNV12ReconForP010Input,
           "WA to change NV12 recon surface width to 16k and pitch to 32k for P010 16kx4k input since MEDIA_SURFACE_STATE_CMD has only 14 bits to sepcify width", WA_BUG_TYPE_FAIL,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1408797083, "Gen11+  Bspec clarification request for Compliance tests with no pixel rounding", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409216368, "DPT should send VRR enable indicator to DCPR even while Push mode is enabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1604225280, "Gen11 ICL_A0 Display  : Port Crc miscompares when Pipe Config change happen with KVMR enabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409451116, "[TREND B0][Known issue] GAM needs to remove WA to enable some of the Range Checks.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409759559, "Need MBC to write XE_HP_SDV_TILE registers as part of the RC6 exit - XeHP SDV B0 change ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaMSAADepthResolveToZWriteThru, "Gen12LP - Optimize multiple MSAA depth resolves using Z write-through", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1306835611, "[TGL-LP] GLView benchmark hangs with CS, POCS not done - preemption specific", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1409710010, "XeHP - GAMCMDI missed as pwr ctx client for GPM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608132035, "AUTOCLONE: TGLLP: cs_oa_busy signal is not driven correctly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409733798, "XeHP SDV 2x4x16: 3DMark11 GT2 F00402 Image Corruption With TBIMR Enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409740324, "XeHP: [SQIDI PSMI] Base bit encoding is incorrect for Node size = 1KB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409757795, "[XeHP SDV]: Nurb Clk gating Xprop", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409782245, "Error reporting PCIe Spec compliance issues", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607196519, "[XeHP SDV - B0] XeHP: Pipe3d: Multicontext: r5 coming before transparent header from TDL to Eu in RTL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608062173, "Gen12LP/GT1/DG1/RKL: Dec400 issue - One port will not issue flush done when other port is in use", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607433951, "MSC RTL not recognizing combined subspans as first subspan is unlit for RTRs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1608127078, "For call/callA register source JIP offset incorrectly decoded by GA", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1808050305, "[XeHP SDV Perf] PS threads are dispatched with NULL RT and promoted depth test", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010239330, "EM/DPAS collision is causing EM W2W data hazard", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409320138, "AUTOCLONE: GFXDRV- XeHP SDV DX12 WGF11RenderTarget miscompare", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_14010198302, "Allow for Backup Mode for LSC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010368787, "[Gen12] Non-Snoop Bypass  Removal", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408609636, "[XeHP][New Sampler] Chroma Key is not supported on XeHP SDV A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409870903, "GFXDRV: XeHP SDV WGF11TiledResources Texture3D Filter Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010118943, "XeHP SDV A0 - PSS non-fulsim compatible mode - dep_clr for the oldest hex has to stall schedule event (sch_event_xfer)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010403030, "Port GT1 RTL into GT2 EU", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1808326800, "AUTOCLONE: AUTOCLONE: [TGL] EU not able to handle B2B Integer Divide with EM on SBID clear path. ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_14010480278, "DARBFunit early clock gating leading to underrun", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409644639, "GFXDRV: XeHP SDV Resnet 59-60 Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010469329, "[DEFER TO DG2:B0] E2E Compression - memdiff corrupt write by RCC - Error Pfe-Msc Read - RTCompression_CFG200", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1808850743, "TGL U A0: EU: goto instruction with uniform predicate in CS SIMD32 kernel does not work as expected.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607720814, "[XeHP SDV] - LNCF not sending out updated data to l3node units", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607780492, "XeHP SDV Perf: 3D_STATE_3D_MODE State decoding issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409796055, "[TGLLP] MSFT SDK - D3D12EXECUTEINDIRECT - TDR CCS0: CS, TSG, VFE NOT DONE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010230801, "AUTOCLONE: DAPRSS and DAPRSC Clock Needs To Move to crclk", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409013255, "XeHP - GTPM multicontext-  MGSR to remove CCS0 registers from shadow list", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607466415, "[XeHP SDV]Blank images with tri001 with slice hashing enabled for 8x4", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1808121037, "[TGL][DX11][Corruption] 3DMark IceStorm/IceStormExtreme Demo - corruptions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607021226,
           "XeHP : GT : RTR 32bpp, 64bpp and 128bpp (MSAA and non MSAA) cases are not meeting peak TPTs due to row hotspotting at HDC - Degradations are from 45% to 60%",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607364857, "Gen12LP: VCS/VECS does KCR protection handshake before flsuh completion", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010078124, "Cdie VF MMIO access to non-existent register returns UR, should return 0's", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010564730,
           "[TGL U/Y A-step][GTCHE SV]: Bspec update required for GoP and Gfx SW driver to clear firmware_is_ready_for_control status bits in dekel "
           "registers[PCS_GLUE_LANE][Tx2_PMD_LANE_MISC1_Lane]",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607850162, "[DG2][MI MATH] Enhancement in fence support in mi math", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010477008, "Display fetch path enters unrecoverable hang from corrupted media compression control codes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_KMD | WA_COMPONENT_GMM)

WA_DECLARE(Wa_1609660580, "DG2: Pipe3d: A0 step :[lsc integration] : Remove UGM from HP list. Add both new and legacy SLM decoding for HP", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1809012548, "[TGL][MPEG2] Panic mode issue on TGL Windows", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010594013, "Display underrun when PM fill is issued while an interrupt is pending", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608008084, "AUTOCLONE: Register reads to 0x6604 is incorrect", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010229206, "Dg2: pipe3D: chicken bit flexing : TDL is blocking deref when 8th bit of tdl chicken", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1807084924, "ICLLPD0 TRTT Aliased Buffers Data Mismatch - Possible race condition between Mem Wr and HDC Flush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1609337546, "Dg2: Pipe3d: 3d+async: Multicontext: TDL is not dispatching missing barrier threads", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608949956, "DG2: Pipe3d: B0 step :[lsc integration] Memdiff in AtomicMessages due to EuObus mismatchtestname : AtomicMessages_CFG15", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409767108, "D12 TGL & D13DG2+ BW BUDDY MASK updates", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010672679, "W/A for [TGL U A2 Alpha][ACS][RS6]: Corruption observed in MS Excel [RANK0]", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607313915, "AUTOCLONE: [Gen12 LP B0][RCSUNIT] Preempt delay counter should not be reset on heqt restore abort", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608137851, "[DG2] Reduce the number of instances of OAC from 4 to 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607871015, "[AMFS] SW Workarounds for AMFS flush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010443199, "[DAPRSS] Color: DaprSsDaprSc.ss_phase0.cpq_mask.sample_mask Mismatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1408862008, "[DEFER TO XeHP SDV:B0][Power/Perf] DAPRSS Data Path Enabled for Dropped Render Targets", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010443297, "[Defer to B0 DG2] RTFUnit, STSUnit: RTF needs to cache SIMD Mode bit from callStackHandlerKSP in GC data", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409028688, "AUTOCLONE: VP9 VDEnc segmentation test has corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_1608126559, "Handle deref issue in SF", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1409836686, "[TGL GT2 A0 PO] CPU and Sideband reading any (Video Transcoder data) 0x60298-6029c, 0x62298-6229c causes CATERR at UEFI halted", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010698770, "[DAPRSS] DAPRSS Sending Blend CData Encoding For Fill CPQ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEnable47bAddressInSingleContextMode, "To Fix override to respect kmd set FtrPAAC + enable 47b addressing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaDisableCCS, "Disable CCS for tgllp and dg1 A0 only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010079397, "[DG1] -- DCPR/DPRZ dcpr_dpt_cg2ddis & dcpr_vrh_cg2ddis bug fixes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010096844, "[DG1] -- DCPR/DPRZ dcpr_dpt_cg2ddis & dcpr_vrh_cg2ddis bug fixes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010357528, "[Apple] ICL-YN Link training fails with HBR3 with FEC enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607304346, "AUTOCLONE: AUTOCLONE: Gen12LP B0: Shaderlib component sending incorrect value for HS & GS thread fusing disable inside CS RTL", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1609337769, "Dg2: pipe3d: 3d+async: multicontext: TDL allocation exceeds", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010688211, "[TGL][MPEG2] Panic mode issue on TGL Windows", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(
Wa_1207131584,
"AUTOCLONE: AUTOCLONE: AUTOCLONE: [XeHP Revisit]Gen11_FPF CLONE from gen10lp: MI_SET_PREDICATE with # of slices does not work in the condition that the slices are not contiguious",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406609750, "AUTOCLONE: AUTOCLONE: Blitter RAW hazard between blits", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1808774947, "[GEN12] DG1: need read/write access to OAG registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010509756, "SfWbus_err_slice_s7.txt: ERROR :  Mismatch of sf_wmfe_strtsprspn", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409909237, "GFXDRV: XeHP SDV OCL Resnet Inference 56 Corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010626361, "GAM-Walker is incorrectly propagating the cycle type on PTE fetch allowing writes to update the Rd only pages. [Write perm faults] ",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_16010658896, "[DG2] SVL : cpsize control buffer state data mismatches with tbimr(sv test)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010595310, "[TGLLP] hdcreqcmdunit not properly sequencing A64 scatter messages if Addr[47:32] differ in a msg among simd lanes", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1609774216, "DG2: RTL is not sending PRIMID_BASE cycle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010569222, "DG2: gamediaunit clock gating bug in port_arb fub", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010146351, "SGR : clock gating issue in logging interrupt to mstr_tile_intr register on SGCI command parity error", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010755945, "AUTOCLONE: PSDunit is dropping MSB of the blend state pointer from SD FIFO", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607424602,
           "XeHP: Pipeblt : Write to the same cacheline address going out of order across blits due to overlap for control surface copy followed by other copy commands.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809761432, "[XeHP] OAG MMIO trigger report doesn't have the correct ReportReason bit set in ReportId", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809761434, "[XeHP] OAG MMIO trigger report doesn't have SourceId field", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010728863, "[PVC][CS_CLUSTER] Ctx image getting updated with current states in case of imcomplete preemption in state_sip & BTP commands", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010818508, "[XeHP SDV] [DAPRSS] Data Corruption on R10G10B10_FLOAT_A2_UNORM After Blend2Fill", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607956946, "Handle block deref size is part of 3dstate_sf & is non-priveleged register bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1607221026, "[Gen12 GT1] CS can issue an extra flush due to pipe control in corner case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010096081, "GFXDRV: DG2 WGF11VertexShader Failure", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409416963, "[XeHP SDV] Driver test failure with Sampler FL optimization feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010733611, "SGGI unit: Clocks gated when SGLI is returning completion credits", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010037835, "GFXDRV : DG2 Perf TDL Returning incorrect data for LSC Chicken Bit Registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607285576, "[Gen12 RKL] RCUUNIT register mask not working", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409467035,
           "XeHP: [GAMXBE_PSMI / MERTXG_PSMI] psmi sends X's for interrupt data if guc_intr_en is pulled down when psmi is in the middle of sending an interrupt to guc.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010665080, "SGunit missing 10 bit tag supported/enable bits in SR-IOV Cap register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607794140, "[TGL] [3D-WHCK] wgf11resourceaccess workload fail", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14010449647, "XeHP : DG2/XeHP SDV - TDL Issue with BTP/CPS Fifo Overflow", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010064115, "[PVC][DG2]: batchBufferPredication_CFG0 MEMDIFF debug due to RTL missed transactions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010796394, "[DG2] [DAPRSS] Data Corruption on R10G10B10_FLOAT_A2_UNORM After Blend2Fill", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010648519, "DG2 : GTPM: FLR + render PG with media WL: X prop in LNE when internal fuse signal is changing based on pm mode changes due to render PG flow",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010685332, "ICL-YN/ICL-UN - PCH display clock remains active when it shouldn't; impact to power and sleep state residency", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409053698, "[XeHP SDV B0]: TDL needs to predict loadcount for linked threads before picking EU", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010840176, "[TGL B0][PO] GFX DX12 - Hang with TimeSPy : CCS, VFE, TSG, EUs, HDC, GW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010178259, "BW Buddy CTL Register has incorrect default value for TLB Request timeout", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409689353, "Panel Power Status hangs when PCH programming happens early", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010670810, "XeHP : GTPM: FLR + render PG with media WL: X prop in LNE when internal fuse signal is changing based on pm mode changes due to render PG flow",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010915987, "DPST IET data writes do not trigger PSR exit due to lack of write event indication to DMUX", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010948348, "[DG2] [RTL_CLK_GATE_VIOL_NEED_A0_WAIVER_AND_BO_RTL_FIX] gtsqdimpar1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010915640, "[TGL] [DAPRSS] Repcol with R10G10B10_FLOAT_A2_UNORM Not Properly Down-converted", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_1607906894, "DG2 :  Pipeblt : Need testbench force to disable 3D Tile64 fix in RTL till Fulsim fix is available", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_14010527661, "[Passive VIP]CoG + PSR xclkfifo not dropping dummy pixel for ODD segment resolution in COG 2x2 or 4x1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010717987, "E2E Compression - corruption due to missing flush between resolve/read - scalableCopyEngine_CFG106", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607610283, "TGLLP B0: Multicontext preemption tests hang with sampler, sc & hdc not done", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608104793, "XeHP: Dec400 issue - Port2 will not issue flush done unless port1 cache pending empty is asserted", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010511442, "GFXDRV: DG2 WW47 0xdeadbeef", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14011037102, "DG2 A0 RTL CLK GATE DISABLE - gtl3bank ltcd_dataunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010242925, "[RKL] -- DCPR/DPRZ dcpr_dpt_cg2ddis & dcpr_vrh_cg2ddis bug fixes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809940648, "[XeHP] XeHP SDV: need read/write access to 0xDB1C register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010828422, "[XeHP SDV-GT] GT is not releasing credits to sg for SG to GT Rd completions", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010837590, "[DG2] Sampler Perf degradation due to R16_UNORM not bypass in MT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14010783208, "DP1.4 MST+FEC+HDCP2.2: symbol corruption for 1clock on a type-1 MST stream", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1807013722, "AUTOCLONE: AUTOCLONE: AUTOCLONE: [GEN11] need write access to some OA registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1808183159, "AUTOCLONE: AUTOCLONE: AUTOCLONE: [GEN11] need write access to some OAPERF registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaRRFreeDistrModeUnsupported, "Disable Distribution Mode RR_FREE in 3DSTATE_VFG and 3DSTATE_TE on DG2 steppings prior to B0 which is when feature was added",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012178217, "Disable TED for DG2 512 A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_2209975292, "[DG2][AV1 VDEnc] Simulation / emulation mismatch for I frame", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010680813, "[DG2] [RTL_CLK_GATE_VIOL_NEED_A0_WAIVER_AND_BO_RTL_FIX] gtgamwalk", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010875903, "[DG2][LSC][A0]MixedMessages_CFG0 test failing as memdiff", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010918519, "[DG2][GT][LSC] HANG in LSCSLMAllocation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011068795, "DG2_B0: PSS span allocation and deallocation for a 16X + Fully Compressed 8x8 can cause performance deterioration and hang", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

// SW WA for issue - https://hsdes.intel.com/appstore/article/#/16010906683
WA_DECLARE(WaRegisterContextMultipleRetry, "TGLLP VF Register Context requires multiple retry", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1808692196, "[GEN12] TGL: need read/write access to OAG registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010222001, "DG2:  test mcmpr_concurrency_hevcFieldSFCScal_VESFCSplit_CFGdg2 :  xpropagation in sfaunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608424662, "Gen12LP/GT1/DG1/RKL: Dec400 issue - : Multi-port operation( one port is idle) - flush flush done on idle port is not getting latched.",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1406664125, "Gen12 euunit NISA - Acc SB needs to be handled per fused EU pair", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408914664, "[XeHP SDV B0][Perf TBIMR] SBE to squash completely unlit push constant requests", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14010847105, "[DG2 GTPM SIM ] dual ctx test render wl hang on 3d primitive instruction debug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14011124694, "Disable expansion+write_thru optimization for DG2 BSTEP", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1609314070, "DG2 Compression : VE-SFC test miscompares on histogram surface", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010744264, "DG2 B - ve-sfc hang with 64K tiling enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14011093645, "[PVC] : Range check calculation seems to be using a wrong base value for the RC6 range calculation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011050563, " dupunit not generating line_pop indication for plane with minimum size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1609102037, "TGNE focused test failing with memdiff", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_14010720793, "DG2 transcoder WD max cdclk frequency limited (fix for PV)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010465259, "[TGL] [DAPRSS] DAPRSS Sending CPQ with No Pixels Lit Causing X-Prop in PFE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_KMD)

WA_DECLARE(Wa_1606766515, "[Gen12LP B0Fix] RCU should ignore(reset) Media Sampler DOP status of engine which is idle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607087382, "XeHP :  Pipeblt : Fastclear enabling in B0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809042626, " ww42.3 8X model is hang for BattlefieldDX11 F00652 : XeHP SDV clone", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010989788, "D12ADLS: DMASD clkgateen dangling", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608590955, "[PVC] : BSPEC: Special flags required in XY_FAST_COPY_BLT command to use it for accessing compressed main memory data during verbatim copy",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_22010493298, "DG1 Corruption while running Sky Diver Demo - but not GT1 and GT2 benchmark", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010465075, "[DG2] [DAPRSS] DAPRSS Sending CPQ with No Pixels Lit Causing X-Prop in PFE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011264657, "dupunit not generating line_pop indication for plane with minimum size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010942852, "Clone (DG1): TGL - Audio 8K1port - For certain VDSC bpp settings, hblank asserts before hblank_early, leading to a bad audio state",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010960887, "[XeHP SDV] Commands with WPARID enable calculates wrong address when command body crosses CL boundary", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010968989, "[XeHP SDV] Large draw detection is wrong when indirect param is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16010981488, "DG2: B0: Assertion error due to tbimr close batch bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010507618, "[Tracking] AMFS is not supported on XeHP SDV", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011060649, "DG2: Media Emulation Reset test failing with a hang in VECS with a reset to VCS2 in a concurrent WL scenario", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010515920, "[DG2] RTL_CLK_GATE_VIOL_NEED_A0_WAIVER for alnunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607220555, "[TRACKING]: Copy Engines Floorplan Dependency with Node Scalability", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607314024, "GUC Device ID addition", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606599854, "PSS state only programmed from CS between nullprim, PSD will hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011274333, "[Gen 12] Sampler power context is not saved/restored", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010458760, "DG2 512 A0 : Display clock - dedp_mc_cd2xdpclk Frequency is not meeting 1300 Mhz (SoC level PV issue)", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010284036, "PVC - Byte Indirect - Vx1 and VxH cases not working", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607446692, "Vs-CL Edge Flag mismatch - revert fix", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010487853, "[PVC] ocl_cts_khr_2_1_conversions_char_sat_int_wimpy_reduction_factor_16384 showing data corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011059788, "Disable DFR for gen12 and beyond", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010655327, "[TGLA0] [E2EC] [FastClear] BSPEC update to mention ClearValueAddressEnable should be set to TRUE when Surface aux type is AUX_CCS_E",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010904313, "AUTOCLONE: [CS] Issue in ctx time stamp register restore", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010984377, "DG2: HSunit Launching Threads Above And Beyond MaxThreads Value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010638130, "GFXDRV: DG2 ww50 stsfix BVH Ray Tracing Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010795479, "RTL_CLK_GATE_VIOL_NEED_A0_WAIVER GADSS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011006942, "RTL_CLK_GATE_VIOL_NEED_A0_WAIVER DSS_ROUTER", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011220139, "Media 12.7 DG2: Reset emulation test failing with hang on SFC forced lock ack", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010430635, "GFXDRV: DG2 B0 DX12 Strange Brigade F215 Hang - TDL GRF Clear Issue with Handle Fifo Write", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010554215, "Incorrect decoding of DW67 in MFX_PIPE_BUF_ADDR state.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010368296, "[PVC] Fuse table to updated with Link copy and SubCopy configurations", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1605795544, "3D: AMFS:  pipe3d : Same virtual address is being sent/used by amfs for different LODs, resulting in dropping of some LODs resulting in corruption",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010733141, "DG2: Media Emulation Reset HCP + SFC test failing with a hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010656390, "GFXDRV: DG2 ww50 stsfix gfx-driver-user-master-38239 BVH Ray Tracing Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010532751, "DG2: ‘btd_multi_ctx_CFG0’ test hang at GT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010566810, "[Dg2 GPSSCLT] Byte enables not set for LSC -> EU rbus data", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011264804, "GFX: System hangs when performing Driver FLR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010946120, "XeHP SDV: Dec400 issue - TSC will issue premature flush done in case of large tsc read data latency", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18011246551, "Diagonal error propagation for vertical intra refresh on H264 VDEnc", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607219886, "[Gen12LPB0/GT1/RKL]DualContext to DualQueue: RCU need to ask cs for CB2 on first context execution after reset", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011315852, "AUTOCLONE: [PVC] incorrect RSA offset check in bootrom", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011082271, "PVC: Guc bootrom update to include the AES keys", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010493955, "PVC - NISA Byte Failure - saturate on byte dst is failing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011235173, "XeHP SDV GLS: Hang due to vp9_cxform_dv going high in hitvertunit (gthcppar3)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011403231, "AUTOCLONE: [DAPRSS] X-Prop from daprsc_cts[1] with CPS Aware", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607945841, "[ADLP] GT Emulation: ComputeShader_Eval_Amfs test hang (DAPRSS, DAPRSC, AMFS, & GAPC Clock Needs To Move to crclk)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010731762, "DG2 gtmidslice gtgabcs gpmunit RTL_CLK_GATE_VIOL_NEED_A0_WAIVER", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011040754, "RaytracingUTP_CFG20 test hanging at GT simulation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011020653, "Dg2: pipe3d: TDL isnt forwarding thread", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010523718, "DG2 Midslice - cfegunit (gtcs partition) - RTL_CLK_GATE_VIOL_NEED_A0_WAIVER", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010613112, "[DG2] [DAPRSS] X-Prop from daprsc_cts[1] with CPS Aware", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1409820462, "AUTOCLONE: AV1 ALN LR temp flops need to be reloaded at top of new tile", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011331455,
           "[XeHP SDV] DFD-RESTORE GPM reads are phy and get set as coherenttype=1 which causes to sqidi to do idi_rd instead of idi_ncrd and slot hangs waiting for u2c_rsp",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010598502, "[D12ADLS]: Display VTd walk request from cursor with SRIOV enabled can cause a hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011371138, "[ACTIVE VIP] : PSR2 : PSR2 fsm stuck on SU_STANDBY when su_end is on the last line of the active region", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011013199, "[DG2][Geometry Distribution] Do not check for cut index in VFL when in batch level granularity", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010614224, "[DG2] [DAPRSS] DAPRSS RTL Dropping Subspan While Fulsim is Not", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011107343, "[TGL] Control and Header Fifo in TRG going out of sync", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14011411649,
           "Incorrect page size used for GGTT walk targeting SM memory if the table entries are not initialized with same LM/SM indication for entries in same cache line. ",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14010675428, "[ACTIVE VIP] : DP2.0 incorrect SDP CRC is sent", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011028019, "RTF FE clock gating incorrectly enabled when QUERY counters full", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011441408, "L3 Node sending Cntl = 01 write cycle to bank", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_16010684351, "Update SystemMemoryFenceError bit in ESR, EMR and EIR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011224835, "[RKL] Display SW workaround needed for combo PHY B rcomp bug", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010614185, "AUTOCLONE: DAPRSS RTL not detecting 1-bit “alpha”  for B5G5R5X1", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_22010271021, "AUTOCLONE: 3DState programming on RCS while in PIPELINE_SELECT= GPGPU mode can cause system hang due to FFDOP clock gating.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010547955, "DG2: DCMPunit de-compression IP(Unified de-compressor) update for 4_3_MONO(0x9) ccs code support in render cases", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010817573, "[ACTIVE VIP] : VRR + Adaptive Sync SDP : two adaptive sync sdps sent in one frame", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011195421, "D13DG2 : DPCCPunit anti collision logic fixes", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011241162, "D13DG2: DPCCPunit readback data path fixes for CSC coefficient registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011370238, "[DG2 B0] DAPRSS RTL not detecting 1-bit “alpha”  for B5G5R5X1", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14011373928, "DG2: GTPM: Soft reset flow: KCR not acking back a protection cycle that VCS sent leading to hangs in VCS flush", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011388525, "[DG2 512EU B0 resyn] GFXDRV DG2PERF: A0 native 128EU timespy GT1 3frame trace hang in async compute phase", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010494446, "DPRP claim and ready are generated along with drm_posted_cycle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507979211, "PVC.GSV.Pre-Si.Media VP: PVC emu output tiny diff with simu output.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011027912, "[PVC A0] MCR Steering update to upper 8 SQIDIs to use sliceid along with dual_subsliceid (SQIDIID)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaBlacklistPreemptionCtrlRegister, "Blacklist Preemption granularity ctrl register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011060172, "[XeHP SDV CFEG ULT] CFEG hang due to command level preempt when all 16 postsync ids used", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010662072, "Pixel mask for the fragmented CPQ is not properly indexed for TRUE_COLOR + STC_ONLY message type, 2X MSAA & cpsize2x2", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409638368, "GFXDRV: XeHP SDV ww26.3 rpt 3dmk11 f644 Tessellation Distribution Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD | WA_COMPONENT_OGL)

WA_DECLARE(Wa_16011062782, "PVC: credit reservation for 128B/256B cycles", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipFirst2MBLmemForVFs, "XeHP SDV PostSi, First 2MB of VF Bar needs to be skipped", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_22010432703, " dcpr memory up indication to pipes does not reflect the actual memory status", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011034162, "DG2 B0: pipe3d: AMFS: [fast clear and security DCN]: amfs counter rollunder in test multiContext_Preemption_CFG395 seed 1", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011539587, "SWA Disable Apple Rounding fix on DX9 Driver", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011163337, "HS  / DS hang seen on TGL", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011155188, "TGL GT2 C0 Step: Revert the security fix added in tsgunit related to rogue mtp restore context running ghost threads in EU", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010772959,
           "TGL-LP/ DG1 SILICON: With pixel scoreboard disabled, PSS is creating an extra thread with no slotquads loaded when it sees an FC64 8x8 with a different topology have "
           "an overlapping X/Y with two already committed partial threads",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010060943, "Encrypted cycles going to SM should be invalidated.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14011507807, "GFXDRV: DG2 DX12 VRS f1903 Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1409327454, "Gen12LP: Compression  enabled runs - ctype 27 requires tile status to be updated as a byte", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_14011508470, "TGL B0+ Remove PM Req with unblock/memup + fill support -- SAGV enhacement not working as expected", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2209620131, "[DG1 A0][TGL-U A0][19H1] Gfx Media: YouTube+Movies&TV WL Resulting in TDR", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010492432, "TGL Display combo PHY DPLL and thunderbolt PLL fractional divider error", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010446606, "3D Surface Type Height\Width Restricted to 2047 in render_surface_state", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010554937, "Hard hang when RCU posted cycle coming within 2 clks of non-posted cycle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011227922, "DG1: Range based flush does not support 48 bit addressing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14011545558, "SGCI unit : Tag Pointers should reset to 1 after FLR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010811838, "Truncation issue in compaction table implementation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011503030, "AUTOCLONE: [ADL-P/DG2] - Display Error Fatal Mask - default register value should be all 1's", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011371254, "GFXDRV: DG2 Cadscene Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010961369, "[PVC GT] Main Copy Engine: Observing 60% throughput drop in read+write test cases and 8% drop in write only test cases.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010493906, "[PVC B0][LSC] Buffer size calculation incorrect for typed buffers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010725011, "PVC - Dpas src2 read suppression issue with HF datatype", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaGTIpNotPresent, "WA to avoid certain GT access (MMIO read/writes mostly) when the GT IP is not present (MTL+)", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(WaIGfxDisplayLess, "This is dummy entry in SKU file and needs to be removed. DO NOT use this in code", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

WA_DECLARE(WaUseSimulationFlowForCB2, "WA to use simulation flow in oprom parsing until CB2 uses full oprom image in GTA", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MINIPORT)

WA_DECLARE(Wa_22010594632, "Hang can occur at context switch with RCS+CCS concurrency due to bug in const cache invalidate @ context switch", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011555645, "AUTOCLONE: [SVSM] Dual Context Invalidate hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011155590, "[XeHP SDV CFEG] CFEG uses crclk at mcr interface", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011069516, "[ADL-P Pipe2D] CMTG offset read returns invalid value at first read.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010744585, "GFXDRV: DG2 OCL non_uniform_work_group Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14011431319, "[DG2 128] Clock gating FPV failed on gammodunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011157294, "[DG2] Chkn bit missing to disable preemption on compute walker command", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011233814, "Clone: Dg2: pipe3d: TDL isnt forwarding thread", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011273609, "Bspec: Enable new message layout for cube array , should be set by SW from DG2:B0+", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010847520, "LTCDunit violating EBB sleep spec - reads/writes being issued the next clock of sleep enable fall", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010582375, "RKL: HEVC PAK MMIO B2B Req- stale data return", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011765242, "Circuit flaw in scaler RAM results in portions unusable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010413229, "DG2: [DPIO/DMAPunit] Lanes enable going through an intermediate value during DP x1/x2 modeset disable", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaKCRMMioRegistertoWhitelist, "KCR MMIO registers to be added to SW Whitelist", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaHCPCrcMMioRegistertoWhitelist, "HCP CRC MMIO registers to be added to SW Whitelist", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaLcpllAfcStartUpAdjustment, "Configure the afc start up bit to avoid lcpll unlock", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507889896, "INSTDONE_CCS is only implemented in CCS0 and not present in CCS1/2/3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011323389, "Tracking - DG2 512EU A0 Clk Gate Waivers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaEnableOnlyASteppingFeatures, "Limit the media scope to A stepping features", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_18011464164, "[TGL-B0]dx10_sdksamples_sc-default-effect-pools-msaa-2_win-skl_main - triangular corruptions", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010931296, "TGL/DG1: TDS clk gating causing corruption in gen12 render workloads", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14010919138, "[TGLLP][B-Step] assassins-creed-origins-sc-custom-benchmark-g1-dx11 : Stream Crash TDR: cs ds svg svl urbm vfg Other", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607220452, "[SF-XeHP SDV][TBIMR-RTL] lo0/man field mismatches", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16011181970, "[DG2] Chkn bit missing to disable preemption on compute walker command", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011167964, "D13ADL: DMUX doing pixel rounding on top of dithering", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409054076, "Display 11: Coding error in pipe enable logic used in dpceunit when DSI is enabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2208288063, "AUTOCLONE: Mid-frame VTD Disable toggle leading to underrun", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409012119, "GT1 : Official drop from dec400 for the TSC hang issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011280238, "Privilege Escalation Issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011260251, "Audio SDP CRC calculation is incorrect", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
Wa_14011279519,
"E2E Compression - Writes from a subsequent BLIT can overtake writes from a previous BLIT to the same address when surfaces overlap between them resulting in corruption",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010954014, "XeHP SDV B0: Sideclk pointers stalled from resetting due to clock gating issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010429828, "Disp VIP in Emulation: 4 streams DP2 test fails with UVM errors", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011807268, "During Object-Level preemption and an odd number of objects VF does no change the Topology correctly in the Ctx Restore", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1608975824, "[XeHP SDV] PERF: HDC issues an uncacheable 'clear' color read when compression is enabled, using MOCS#0 instead of MOCS#3", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1609676403, "PVC: MI_UPDATE_GTT command is not writing to page aligned address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809083394, "[DG2][OAM] OAM producing 3 cputs while reporting post 64bit change", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010777351, "[Emulation] Uncompressed Joiner 8K tests are failing with underrun for 13.5G link rate", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010860707, "Video Dip Data register values are not updated at Vblank", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010868443, "DG2: 16-bit CRC calculation incorrect for Panel Replay with YUV 422/420 formats", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011066335, "DG2-a AV1_vdenc partial sb hang due to ARS not sending sb done to hmdc for last sb in first row", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011539577, "[ACTIVE VIP]: Panel replay + Audio (sdp splitting enabled): VSC SDP is not being sent", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011244400, "DG2 PERF: BF1: LSC stalls for SLM accesses with Tiley walk", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011265925, "Sarbunit: Register update for E2E Compression --4:3 Compression default chicken bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_16011384926, "DG2 hang in CS , WM dirty bit not getting reset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14011943648, "PVC: Hang during ctx save when PSMI DOP gating is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011448509, "DX11 Dota2 LRCA cCaorruption in DG1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011294188, "[TGL B0] FLR cycling test causes hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011944581, "[DGT A0][Perf] Defualt LSC Chicken bit is not matching performance setting", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011240282, "[PVC A0p/B0]Clone from DG2:pipe3d: LSC L1 return seems wrong", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011780169, "[XeHP SDV B0][Manual Clone][DG2 128] Clock gating FPV failed on gammodunit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM | WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010973110, "[DG2 CFEG ULT] CFEG hang due to command level preempt when all 16 postsync ids used", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011294842, "CL sending down extra nullprim", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1508059477, "[GPSSCLT]: FENCE Message Stuck inside the LSC", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011478345, "SVG RTL not zeroing out address bit 5 when PC buffer length is 0 causing additional derefs to be generated.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011091694, "Display change is not getting triggered for dual pipe test", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18012201914, "[DG2]Fulsim incorrectly interprets the sample msg type for GEN12:HAS:1209978020 feature.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1809626530, "TGLLP: Unexpected ResInfo results with LOD out of bounds.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011508199, "Corruption in viewmask token coming into CL for POSH enabled workloads when TE DOP is disabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_18012154892, "[DG2 PERF] Volumetric fast clear 2X slower in 8x4x16", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_22010960976, "GFXDRV : disable untyped l1 flush for uav barrier chicken bit set in tdlunit by default", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22011142311, "DG2 ST bankblock inuse counter overflow", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012119218, "PVC: TILE PSMI drops incoming completions (mdfi_bfm -> GT) received over the serdes link in PSMI mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011054531,
           "[Cayucos] Checkerboard background on text input and composition rendering across multiple apps - Chromium Edge, Google chrome, Windows email app, whatsapp QR code "
           "render / EV2 repro",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14011996739, "[PVC] ocl_opencv-341_ab-default-opticalflowpyrlk1-6987_win-skl_main failing with data corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011372332, "DG2: SVL cpsize state buffer state delivery happening without credits", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011411144, "DG2: MESH SVRANDOM:SOL input and output bypass out of syn, causing distrib cycle to get dropped", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_1508060568, "PVC:GTPM: bdssftldist output credits not getting reset when render power down happened", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011776591, "PVC - L3 CLT Perf - Functional failure in FTL due to RPT", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011943930, "[PVC A0] Defualt LSC Chicken bit is not matching performance setting", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011235395, "PVC: GTPM:  RC6 Abort issue : Test stuck at Render Pm mode state as request is not reaching to Gpmxmt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011254478, "PVC: GTPM: PM mode ack from GPMXMT not reaching GPM due to credit release issue in MCR fld unit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011439413, "0x9684 STS register read hanging as ack to message channel in STS in on crclk", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1508208842, "[TGL][PV blocker] AV1 decode corruption on some TGL silicon", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011157800, "XeHP SDV A0 Silicon Hang - Compubench Facedetect ST/SC Deadlock", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1607352404, "AUTOCLONE: mov with bfloat source support not added in hardware", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012167491, "[XeHP SDV][DG2][TBIMR] Wrong dirty bits in Nullprim because of implicit reset of TBIMR bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_22010493002, "[TGL-B0][PO] [DG1-B0]MediaMFX File Transcoding does not generate correct CRC when using -d3d", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011557634, "[DG2][XeHP SDV] [2 tile] Corruption while atomics are used in WPARID mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_2006612137, "[GEN11 GTPM LP] Fixes for L3 not working due to a hang in GFX Flush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1607801587, "[RKL]:SVL MCR is on gated clock.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011453668, "GFXDRV DG2PERF: Native128 timespy GT2-F1622 random hang with ww19+svsmfunctionalbug+asyncfixes(tsl+tdl)+bczwiccredit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011468763, "WMBE datapath mismatch on flipping chicken bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011405638, "XeHP SDV: compip_mediaunit   RTLFix Required : When compression is disabled in DECIP, it should convert compression CType to normal CType",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011543251, "[XeHP SDV] [TBIMR] Wrong dirty bits in Nullprim because of implicit reset of TBIMR bit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011186057, "GFXDRV: ADL-P  DX TR test Texture2D/DepthStencilView hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_16011303918, "CLONE: RKL: Underflow and screen shift when PSR2 enable/disable during update frames", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010751166, "[lg][hp]Display Corruption seen while re-sizing the  MSFT visio application", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010657660, "[PVC] Pwr context image changes related", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012343524, "Disable production or consumption of compressed surfaces in media engines.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1608254475, "XeHP SDV: compip_mediaunit - TSC incorrect HASH-ing for read/write to NODE/GAM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18011725039, "[XeHP SDV] [2 tile] Corruption while atomics are used in WPARID mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1508038496, "[Gen12.7] [Encode][DG2 B][HEVC VDEnc][bug]: HEVC VDEnc SCC Palette mode sim & emu mismatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_14012104677, "RCS, CCS and KCR in different reset domain", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012362059,
           "[DG2 512EU B0 ECO] Memory corruption in case of MERT cycles with VFID non zero: MERT TLB looses 1 nibble from Physical address on TLB entry allocation ",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011544354, "PVC A0: HDC Sbus translator code change for L1/L3 Flush handling", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409364714, "AUTOCLONE: [TGL-A0][PO] GFX : Reserved fields in Instdone Registers are tied to 0 instead of  1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1507105019, "AUTOCLONE: GEN12LP B0: WM Assertion failure in wm_rand_ctx_all_CFG0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011088594, "PVC:GTPM: Credit handshake for FTL read pointer in 1.5x domain is not getting reset", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606927058, "AUTOCLONE: XeHP : *CS Runlist fix for Use HW pointer reloading completed context", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012375360, "D13 ADL-P | For PG2 disabling DCPR is in-correctly looking for darb_darbf_lp_idle indication.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011356768, "[DG2/512-A0-PO] VRS Tier2 Test2 Corruption - Image Based", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011660586, "GS not launching thread waiting on fused EU 2nd thread", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011620976, "[DG2 512EU B0 ECO] [DG2][GPSSCLT]: Assertion fired from LSC - L1-UC write/atomic chaining for V1 messages broken.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012419201, "[DG2/512-A0-PO] DX11 Firestrike GT1 EU Hang on Headed Config", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012420496, "DG2-512: Observing XPROP in EUDPAS as the EUGA input ga_dpas_denorm is X with ga_dpas_dv", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011759253, "[DG2 512EU B0 ECO] DG2: Guc DMA Restore issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011428000, "Registers missing in PWR CTX SAVE/RESTORE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14011503117, "AUTOCLONE: [DG2/ADL-P] - X prop on dps_lnbuf_subbnk_rdpipeline.single_err_pre", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011168373, "AUTOCLONE: [ACTIVE VIP] : PSR2 : PSR2 fsm stuck on SU_STANDBY when su_end is on the last line of the active region - follow up turnin",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011100796, "DG2 GTPM : Full soft reset: GUC HW is unable to support Full soft reset flow", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011524941, "[XeHP SDV][A1][FV-VV][2T] GT is not coming out of RC6 while running molten, this caused an MCA.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012128494, "gamxbe unit is not getting original ADDR16 for the FlatCCS cycles.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011383443, "[DG2 A0 PO ] - H2G Timeouts resulting in TDR's, BSOD", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011827334, "[PVC GTPM]: PM flush doesnt flush out bevause PMflushdis is default high and it is a HW only register", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011217531, "[TGL U B0][ACS][20H1] Adobe Lightroom flickering underrun while using brush tool [REGRESSION]", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010707541, "ADL-P : FEC not starting after Deep Sleep exit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012504847, "[DG2/512-A0-PO] Fire Strike Graphics Test 2 (GT2) test hang with SVG/URBM/GS/VS/VFL not done", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011859583, "x prop in systolic unit when src1 operand dispatched partially from ga", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012612099, "[DG2/512-A0-PO] Dx12 StrangeBrigade hang with GAM/MERT not done", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011622088, "[PVCB0]MMIO queue full status not being set", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012385139, "Clk gating issue: MSTR_TILE INTR Tile 0 intr is not set when correctable error is set GFX_MSTR_INTR", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011086106, "[PVC B0][OAM]:  Clock ratio signal not connected to OAM", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011588650, "[PVC] [Clone from DG2] OAM: Context ID or Unique_ID is not forwarded on the Report for MMIO Triggerred report", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012170143, "GFXDRV: DG2 A0 WGF11Shader5x ControlFlow TrueValueNC Hang: Driver programming issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14012197797, "DG2 clone: GFXDRV: MTL 64EU DX12 NightRaid f1464 Corruption", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011777198, "[DG2/512-A0-PO] DX11 Battlefield V hang with TE not done due to midslice TEDunit not getting reset when dgslice TEunit get reset", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011440098, "[DG2/512-A0-PO] PCPunit receiving extra push constant due to uncommitted push const from the SVG engine context restore", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14012562260, "[DG2/512-A0-PO] DX11 Battlefield V Hang - CS, VFE, TSL, EUs NOT DONE", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011450934, "[DG2][128/512-A0-PO] Render restore hang due to SVG FSM arcs not being mutually exclusive", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22011494591, "DG2 512A0 fused down to 128EU :  BF5 Dx12 G2 - CS, VFE NOT DONE due to Sampler hang", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012691775, "Random fast clear causes L3 to hang and expose security Issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22011537839, "GFXDRV DG2PERF: 8x4x16 B0 dynamic SLM is not happening, TSL is not releasing all SLM back to LSC$ cache for timespy(perf GT1 F1388) lighting phase",
           WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14010826681, "Driver writes to SVL register offsets sometimes don't work correctly due to FFDOP clk gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22011327657, "CSB data in hw status page may be stale when read out by SW (memory ordering for CS write vs engine interrupt delivery)", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012688715, "AUTOCLONE: End of context GRF clear in large GRF mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
Wa_14012294832,
"PVC: The last write request sent by TILE PSMI in response to a drain request is dropped in lnep as lnep receives a blockreq from GPM much before TILE PSMI receives a drain",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011735627, "[PVC] SPM4 counter not counting due to AND gate issue", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011744553, "[PVC] OAAL not sending signals related to SPM", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011628239, "cache invalidation from POCS in render pipe causing hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012729893, "[DG2-A0][512EU][Manual] UnrealEngine Infiltrator hangs due to a deadlock in L3node", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011902670, "[PVC B0][Cloned from MTL SM OACLT] : UVM TB[OAG]  : Report Reason in the report format for MMIO Trigger is not coming.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011879768, "[Gen12LP][CS RTL] Timestamp Reporting  in RCS compute mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011969663, "OVR does not send init_abort to POCS when it runs out of free pages", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16011877939, "bfloat operands dont support scalar regioning", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010703925, "[DG2][OAR] counter_overflow bit not being set when the counters have overflown", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010537631, "DG2 B0: PSD RTL bug caught through UVM: disp_reg_addr going to X (PSD_REG_ERR) instead of R67 phase", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012611968, "PVC FLATCCSBASEANDRANGE Register should be on Bus reset", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16010799899, "[PVC B0] SLM A16 and Load/Store_block message", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011371856, "[PVC GT EMU] BatchBuffer test Memdiff with Frontdoor enabled getting read return for upper 32 dwords", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011914836, "[XeHP SDV][Cloned from MTL SM OAMCLT] : UVM TB[OAG]  : Report getting triggered twice for a single clock ratio change.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011773973, "DG2: SVRANDOM: SOL ACK message to CS  from 1 of the 8 slices not sent correctly.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010476401, "DG2 GTPM :  RC6 flow: X-prop in hcresunit in media test", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012862603, "[XeHP SDV] [Cloned from MTL PipeSM]: PM: OAG ctx restore sequence not correct. OA Debug register not restored before A counter registers",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012713469, "[DG2 - 512] GFXDRV: DG2 128EU WGF11RenderTargets Swapchain Hang", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_14012760189, "DG2 FTunit seqABCD_req_num counter overflow and cause smp_pipe_id changed unexpected", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012866954, "[DG2-A1][512EU]L3Node CBE deadlock fixes", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011481064, "[DG2 B0][CS RTL]  CCS is not sending flush to cfeg  for  chromakey command ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011310033, "DG2 AV1 VDEnc   Emu segmentation test corruption when segDeltaQ + baseQp <= 0", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011531258, "DG2: LCU64 merge left Issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011539496, "[128/512] Sampler Hang with DX12 Battlefiled-V G2 stream due to a missing hold in WE flopping in DMunit steering FIFO", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_22011549751, "DG2: RDOB, HCRES: AV1 Encode hang with slow vdx row store data -  associated to post Si HSD - 14012697594 ", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011689089, "DG2: Async throttle deadlock between TSL and TDL", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011983264, "AUTOCLONE: MTL: PIPE3D: X-prop in EUTC unit for test 'TE_Basic_CFG161'", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012437816, "LSC is downgrading the fence to LOCAL when flush is none", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012832783, "[PVC][XT][B0] ocl_cts_khr_2_1_commonfns_clamp failing with data corruption", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409337719, "Defeature Color Clear in LKF", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_220981846, "3D TYF surface corruption in MIP tail LODs because of X-adjacent RCC cacheline composition", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1408556878, "AUTOCLONE: AUTOCLONE: PS Invocation Count and PS Depth Count unavailable to UMD", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22011320316, "ADLP: DMC trap status register not getting cleared as expected", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14011491398, "TDL is not propagating SIP STATE to EU", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011184234, "[DG2][HAS]RCS, CCS and KCR in different reset domain", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013111325, "AUTOCLONE: AUTOCLONE: AUTOCLONE: TGL U B0 Battlefield 4 + AA causing hang in MTunit", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22011767781, "XeHP SDV C0: FULL FIX TDL is not propagating SIP STATE to EU", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011700429, "AUTOCLONE: DG2 PAVP: KCR to reset Cryptocopy flags before sending Go-0 ack for engine reset", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011652428, "[Deadlock] TLB invalidation, GAM cycles going to SM and MERT going to local", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16012215873,
           "[Gen11 GT]: During MTP flow and when Dispatch Pipeline is idle- Done signal from TDC to TSG going inactive after some extra clocks than what TSG is expecting",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_18013889147, "[TGL] Read data corruption due to delayed Writes with State Access --  Sporadic failures in dEQP-VK.subgroups.basic.graphics.subgroupbarrier test",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011342517, "[ADL-TYPEC] : HDMI 2.0/DP1p62Gbps skew violation when there is skew between DL PCLK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011863758, "[TGL UP3][RVP][20H1] Edp panel will flicker when system idle at desktop with specific background picture", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012061344, "grf read supression reset by writeback in one of fused EUs causing issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013202645, "[DG2-128-B0] GFXDRV: DG2 B0 Raytracing RayQuery Hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_18013852970, "[DG2-A0][512EU] CPS rate is always 1x1 when written by a shader for non-zero view when primitive replication is used", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18013755946, "[DG-2][A0] Corruption with TBIMR and RC6", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_18012318098, "PVC mixed mode bfloat16 * float32 point multiplication rounding issue", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013297064, "AUTOCLONE: [New Sampler][DG]:DG2 - SSLA not adding LOD state bias for SAMPLE_LZ messages", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012688258, "GFXDRV: MTL OGL Texture Stencil8 advanced.sampling.Image Failure", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011373099, "PSS flush done does not comprehend PSD state change, it only comprehends all PS threads completed.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL)

WA_DECLARE(Wa_14013120569, "PCH display HPD IRQ is not detected with default filter value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011954496, "AUTOCLONE: Circular deadlock between VCS/KCR/KIN due to lack of VCS stall after CryptoKeyExchange followed VCS processing other PAVP commands.",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22010893396, "ICL Hang observed: MT Sampler issues erroneous requests to L3 when the lossless control surface queue is full.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013475917, "vsc_framedone flag not clearing on PSR entry", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013341720, "dpas src0 fifo overflow with no src2 read suppression", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013232017, "AUTOCLONE: DG2: GA dpas perf optimization corner case results in Xs to dpas", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18014480127, "AUTOCLONE: Copy engine sampling corruption when compression is enabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012383669, "[Bspec_Update_Only] src1 byte swizzle additional cases not working in hardware", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010275992, "Page Faults: Write access to page marked as read only results in write being dropped, but fault may not be reported", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_1508761755, "XeHP SDV C0: EU signals are connected to NOA varnode on gated clock", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013347512, "[DG2-512][128 EU-PO] DX11 Corruption Observed Firestrike GT2 and 3DMark11 due to missing flush between UAV events", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(
Wa_16012552413,
"[DG2][PCIe Compliance][128] SGUnit compliance run is failing for Read Completion Boundary, Common Clock Configuration, 'Extended Synch after SBR and LDE reset mechanisms",
WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16012555157, "[DG2][PCIe Compliance][128] SGUnit compliance run is failing for ARI Capable Hierarchy for SBR and LDE resets", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14013392000, "[DG2 128 A0][OCL] BGEMM - CS, VFE, GW, EU hang due to kernel using large GRF and RTL hangs", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_1807209625, "AUTOCLONE: AUTOCLONE: [Gen11][Post-Si][Encode][HEVC]GPUMMU page fault seen with non lcu-aligned source", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_22011848744, "[DG2-512-C0] HSD file for DCN : Spec Bug Fix for Tier 2 VRS related to COMBINER_SUM", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_14013444872, "AUTOCLONE: [DAPRSS] Carry-out Ignored on Surface State Address/Tag Calculation", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013435475, "[128EU Native][DG2 A0] Unigine Valley hang with TBIMR due to Arbitration Deadlock", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012376754, "[DG2 C0, MTL] Fix bug to enable Typed write atomic chaining", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaWddm48bGPUVA, "WDDM2: No support for 5 level page table", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa57bAddressingSupportOn48bSystemWithPML5, "Temp WA : this Wa helps to support both 57b and 48b CanonicalAddressing in GTX. this WA helps for Xe3 boot time",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_22012278275, "D13ADL PSR2 IO/Fast wake times not matching with programming", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceTile64ReconSurfaceToTile4, "DG2 B: Tile64 won't apply on recon surface for AV1/HEVC/VP9 VDEnc to avoid special alignment for variant surface",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_22010551662, "[TGL U B0 ][MF][20h1] Blank screen seen  with 4 MST  Displays", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012358565, "AUTOCLONE: 32bpp Cursor can cause underrun in high BW scenarios", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22010947358, "ADL: KPI Display IP Residency table indicators", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012279113, "D13ADL PSR2 No SU seen when start line is 0 and SDP scanline bit is set to 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012360555, "[ADL-P][J0][PO][LP5-T4][Display]MIPI display is not working on LP5-T4 motherboard", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012244936, "FPU1 output mismatch for AVG instruction due to illegal srcmod on src1 acc", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013672992, "AUTOCLONE: [dg2-native 128] dx12 hitman hang due to EU allowing a subsequent thread to use data from current thread", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010265089, "FBC to force 512B segment alignment", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013805541, "SSLA output qaddr 1 on 2D non-array surface", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1508744258, "Hang due to deadlock created by RHWO scenario with RHWO optimization enabled.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012532006,
           "[New Sampler][DG2][SSLA]:SSLA float2fix not clamping correctly float16/float32 down to s1.14 for the case of mirror mode when the integer component of input float "
           "addr is >=2 and even",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012281344, "AUTOCLONE: [DG2][128 A0] WLK Certification failures in MeshShader Stats tests", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1606707513, "GEN12LP Test CoarsePixelShading_817250 failing with FATAL_ERROR at GT due to X-propogation from RCC unit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_18012660806, "AUTOCLONE: AUTOCLONE: [TGL/DG1][DX11] 3DMark - Firestrike - corruption in OOTB run", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL | WA_COMPONENT_KMD)

WA_DECLARE(Wa_16010947053, "Memory compression block may issue premature flush done resulting in data corruption", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011023677, "DG2: B0: HS handle reused and not sent down, causing hang", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012463389, "DG2B: HMDCunit - hevc p frame support ( A late customer requirement), disable L1REfid when BMEdisable set to 1", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012594490, "DG2-512-C0 - [BUG for TI] for HDC Read to support all renderable formats", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011391025, "Potential security issue when a thread ends while FPU instructions without any dependency are present before a send/sendc with EOT flag set",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012292205, "Predicated mov with diverging fuse mask kills read suppression causing EUs to go out of sync seen in dx12 horizon zero dawn", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18015444900, "[DG2-128 A0] LSC writes and reads from Scratch works incorrectly for SIMD8", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012654132, "AUTOCLONE: DG2/MTL/PVC: E420[3] default value mismatch between bspec and rtl", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012655426, "AUTOCLONE: [New Sampler][DG2][FT]:Wrong L1 to L2 address conversion for YCRCB formats", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_22011802037, "MI_FORCE_WAKEUP and engine reset happen at almost same time, then hang can occur", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14013723622, "[TGL] DARBF read pointer does not clear upon DC5 entry causing spurious requests to be sent out during DC5 exit", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012725990, "[ATS][A0/A1][1T]: GPU hang with L4WA with concurrent media WLs.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012924563, "[DG2][WHQL] VFL does an invalid memory access when the first index address is out of addressable memory.", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_22012725308, "WAR hazard for ARF access", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1508540814, "PVC B0: GTPM Stateless Compression: DSS_UM_COMPRESSION_REG in TDL is not part of power context save/restore", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1508652630, "PVC B0 - Credit Counter Underflow Error on MDFI-LNEP Interface when RC6 is enabled.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012038966, "[PVC B0] unexpected duplicated migration report when triggering threshold is 1", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012254246, "Disable read pre-fetch  for out of package request or targeting to SM", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013258106, "dpas src2 read suppression buffer overflow in dpas_stresse_73 due to non 8x8 use", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012311025, "Address Translation Service PCIe capability reporting - add chicken bit to disable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013646056, "integer dpas data corruption due to upconvert of srcb and invalidation of RS", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013677893, "mach/macl implied acc causes incorrect read suppression with most ops", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011234808, "PVC:GTPM: Base compute PLL mode: CPunit not sending ack to GPM for clk gate request (crclk), hung in gate row wait", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011945578, "PVC:GTPM:B0 compute PLL mode: render wake hung due to deadlock for crclk ack and SPC handshake from GPM/CP", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012239583, "PVC:credit reservation count need to be increased to make each flow to progress", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012244550, "PVC : FTLB is not caching all subsequent ATS responses if the page size is greater than 4KB", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012607674, "PVC B0 : FTL hang due to 128B cycles", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012666875, "PVC: FABRIC Dead lock for  multi-tile copy", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012200645, "dpas data corruption on acc_stress_afp_0120n_1022 due to RS WAR hazard", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012237902, "PVC:GTPM B0: X-prop from FTL due to reset_prep not asserted during render power down as deassertion of pmmode not happening", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013163432, "AUTOCLONE: TGL BS-BS Jitter in  DP output with MST + DSC + FEC enabled", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16013063087, "DG2/MTL: State Cache Invalidate in Compute Mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16013164648, "[DG2][512] GS MESH SHader Stats is incorrect for SIMD32 threads", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012727170, "[DG2-512]Security issue related to Barrier message", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013215631, "[DG2-A0][512 in 256 fused down] Corruption on media playback when Compression is enabled when 2-mem slices enabled", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22012699309, "[DG2][512 B0 PO] Unigine Heaven FF Hang - TE Distribution FIFO Running Full", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_1308578152, "[DG2][512 B0] Corruption + Hang with TimeSpy (GT2/Extreme) on Fusedown Configs 448EU and 384EU When Geometry Slice0 is Disabled", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012766191, "[DG2] Omask does not work with CPS and MSAA", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012826095, "[DG2] [512-B0] SLM deadlock due to read tracker contention", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012841360, "ARF registers not getting clear leave potential security issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012727685, "[MTL-64]Security issue related to BTD child threads", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012968468, "AUTOCLONE: DG2/ATS/PVC: OAbuffer overflow causing a CS hang in Overrun disable mode", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012832779, "[MIPI] GOP workaround for Combo-PHY LDO operation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013590282, "AUTOCLONE: [512-A0-PO][DG2][OCL] hang/timeout on 10 function pointers tests", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16013000631, "[DG2] CS needs to serialize Flushes and Inv to TDL", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16013032496, "[DG2 512 B0 PO] Unigine_valley hang with CS/WM not done", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_18015881830, "[DG2] OAbuffer overflow causing a CS hang in Overrun disable mode", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14010939305, "E2E Compression - DG2 B0 - 4:3 compression Mode 3 possible HW incorrect bit spying - cc_4to3#c_mode3", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_22012856258, "[Dg2]dx12 Cyberpunk 2077 live game hang with EU not done due to read suppression logic going out of sync", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012778468, "MTL 3D: GMDID Mirror Register missing in RPM", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_SwControlVscSelectForVscSdp, "SW should Set VSC_SELECT Value to SW Control in PSR + Color Usecases. HSD:16012349876 ", WA_BUG_TYPE_FUNCTIONAL | WA_BUG_TYPE_SPEC,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

WA_DECLARE(Wa_22012972280, "AUTOCLONE: RTL using pre_zero instead for condmod with non-cmp causing incorrect result for F + F -> BF", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012841275, "AUTOCLONE: AUTOCLONE: [TGL][AMFS] Page Fault when small number of pixels using Sampler Feedback are rendered", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014063774, "[DG2] Need a sync before inter-thread access to an SLM location -- to avoid SLM data race", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(
Wa_22013037850,
"[DG2][512B0][Manual] OpenCV (opencv_bgSubMOG21) CCS Hang with Current Instruction 0x7a000a04 (PIPE_CONTROL) since LSC -> GADSS 128B Packet is not Adhering to B2B Protocol",
WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22013059131, "[DG2] [512-C0][4-29] SLM and UGM deadlock due to read-tracker/way contention", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22013073587, "[DG2 512 C0] Fix global WAR check for SLM in LSC bank", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1509018438, "[MTL-3D] OACLT: UVMTB [OAG] : A24 and A25 counter value mismatch", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014068406, "[DG2][OCL] YCRCB Border Color on Black", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16013271637, "MSC reorder buffer calculates fragments incorrectly leading to a hang in per pixel dispatch", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_14014097488, "[DG2] Vulkan Red dead Redemption 2 hang,  due to a HW issue in WM when Nulprim combines pipelined state changes and semi-pipeline state changes",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_1608133521, "[DG2 512EU B0 ECO] [DG2][Cloned from PVC] Add Time_stamp[55:32] to the OA reports and trigger report based on [55:32] bits", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011879834, "[Lenovo_IdealPad][S360-TGL][LCFC][HF][20H2]17' AUO Panel Flicker after press F11 or Alt+Tab switch tasks under system.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012773006, "TE DOP disable with idle flush enabled causes CS/CL/SVG  hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1509235366, "[ATS-P][B0][2T] benchmark_app of OpenVINO inference workload got system hang if run multiple streams and need BMC rebooting", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011186671, "AUTOCLONE: [DG2 512EU B0 Resyn] FFCLT: VF slice Arb mismatch in reduced FIFO validation", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014078854, "HDMI FRL + Audio - Implementation overheads can lead to max audio support < Spec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013045878, "[DG2][B0] GPU Hang with Openvino benchmark app with multiple processes", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18015390431, "[DG2-128Native][DX11] Sea of Thieves - TDR / Video driver crashed", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14014191401, "[DG2] TG DDA LinkM/LINKN >4 required for DP2.0 8K60", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1605284233, "Gen11 LP : Issues found in CSULT during Medusa  Whitelist DCN", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22012718247, "TGL-H eDP HBR3 panel flicker one UI jitter workaround", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18016882379, "[DG2] Memory corruption when reading linear compressed image 2d due to sampler not supporting Linear compression for some formats",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// This WA is temporary fix, for permanent fix Os Managed GTT should be clubbed with DPT
WA_DECLARE(WaIncreasedApertureMemorySize, "Increase the Aperture Memory Size in PPGTT to reslove Out Of Memory", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14014176256, "[dg2] Divergent TG  barrier causing hang in some 3d game titles", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014265947,
           "[DG2][CFL + 512B0] CS WMFE Hang with PSMI Enabled on TimeSpy GT1 (Range Based Flush Entry Incorrectly Valid Along with Flush Done from WM due to VF Incomplete Status "
           "on Preemption)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014414195, "AUTOCLONE: Pixel swap logic bug on volume+aniso case", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16013835468, "[TGL-U B0][21H2][Surface Lucca]:Display junk and underrun on Pipe A while playing video using MTA with PSR2 enabled.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014475959, "[DG2][TGLH + 128B0] Page Fault (VA 0x0) with TimeSpy extreme WL run due to EUTC not clearing the previous QID state when EOT clear is observed",
           WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014738593, "DG2/PVC/MTL: Eu Attn Clear Registers reading 0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014037440, "Autoclone :: [DG2 3D] OACLT: UVMTB [OAR] : Context ID and timestamp fields in the report output is incorrect", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014595444, "[Sampler][DG2][SI]: Sampler dropping MLOD parameter for SAMPLE_B instructions w/ MLOD", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaSkipCondBbEndInWaBb, "Skip MI_CONDITIONAL_BATCH_BUFFER_END in CTX WA BB during metrics config restoring.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_16014451276, "[ADL-P/M] Default setting for all POR BOM - X-granularity as 1-based", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014889975, "d13adl dpst vblank delay counter does not reset", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013689345, "[Dg2] Morton Sort with async. compute - LSC sends flush ACK without waiting for all transactions to complete",
           WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012604467, "[ADLP][GATE][AUTO] Underrun on Pipe A and B is observed when PSR2 disabled in CAPTURE frame and SU in next frame", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14012342262, "[DG2/512-A0-PO] Cannot read to MMIO Register 0xE420 to disable IC prefetch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014830051,
           "[DG2][128B0] DX11 Unigine Heaven CS, SBE, IZFE, HIZ, WMFE, SVL, SDE, SO, SSLA, EU*, IC, BC Hang - Compressed_data bit incorrectly signaled back to client in 4:3 "
           "Compression + Read Squashing enabled case",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_22011428412, "Register have issue with Reading", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1508657967, "[DG2-512 A0/A1] GAM results in PF when running PAVP Stout Mode test", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16013338947, "ELG: MMIOROCI_CFG4 hang in EU - SIP kernel not invoked in render context", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014947963, "[DG2][512 B0] Microsoft-DirectX-SDK-June2010_SUBD11_3600_DX11 Hangs with EU-HDC not done", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_16012705079, "[DG2 VF ULT ][WHQL] VFG culls an indexed draw based on IndexBuf Size in some corner case scenario", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_14014851047, "[DG2 ][128B0]dx11 world-of-warships_unknown-2020.05.25_ac-g2 stream hangs due to VFL sending partial object to clipper", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableStateCachePerfFix, "State cache perf fix disabled - RCC uses BTP+BTI as address tag in its state cache instead of BTI only", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14014949591, "TDL RCS and CCS State Update Issues with Compute mode and State Base address", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16014538804, "Xprop in VFL unit due indxfifo due to issue draw states pipelining", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL | WA_COMPONENT_D3D)

WA_DECLARE(Wa_14014617373, "[Xe2] Accumulator HWSB RAW hazard dependency check bug for destination stride more than 1 (crossing acc boundary)", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaKmdDisableDualContextLimitingtoDualQueue, "Dual context disabled either by HW or by GuC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16013830515, "AUTOCLONE: [ATS-P][B0][Media] : GPU hang of mfx_player with VD+SFC on ATS-P B0", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16014719453, "[xe2] increase RCC clear value cache size to 16 entries", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014631288, "OAC counter registers not getting reset during ccs select change", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015141709, "[DG2] Preemption control for object level preemption is now controlled only inside VFG and not CS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD | WA_COMPONENT_D3D)

WA_DECLARE(Wa_1309179469, "[ADLP] Workaround for DP cross connection failure leading to IOM disconnect hang due to Phy wrong status", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16013190616, "[ADL-M][ADL-P][BKC][A0][TCSS][Cobalt]: FORCE_PG_POK_ACK_TIMEOUT caterr observed after pressing restart button with DP display connected over TBT ports",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1406758939, "AUTOCLONE: Sel Denorm Failure in Mixed Mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014929598, "AUTOCLONE: AUTOCLONE: CFEG RTL not interpreting the CFE_MAX threads programming correctly", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013880840, "[DG2][128 B0][512 B0][DX9 Native] SEL Opcode for FP32 Not Supported in ALT Floating Point Mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012260983, "AUTOCLONE: GAMCCS issue when invalidation occurs on non-idle boundary", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_14015055625, "SFFE handling of the Primid high cycle when primids greater than 64k and tessellation is enabled has a bug", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14015150844, "[DG2][128 B0] Fused Typed Write issue - Hang on enabling feature", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WA_1509727124, "SC disable power optimization for back to back cache EBB read.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(WaDisableFtlb, "[DG2] disable FTLB on all engines", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDrawWaterMarkOverride, "Custom draw watermark value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1508691897, "PVC XT A0: GTPM: Systolic license be disabled by default using TDL throttle register on XT A0 (B-spec update)", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1509372804, "PVC:GTPM: RC6 save restore results in error injection on Compute traffic", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013755176, "dpas causes em to incorrectly calculate if early SB clear is allowed", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14013811964, "mac implied acc causes incorrect read suppression after mul for word datatype if dst is also acc", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014152387, "consecutive DF mac instructions with same src0 cause read suppression logic to incorrectly send stale source", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014171572, "[PVC ] : RTL missing to do an ATS translation (PASID) incase of the DM=1 on PTE entry", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014238785, "[PVC] [XT+] HW thread number for scratch access allows for 12 threads per EU, wasting memory space", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014944017, "PVC Link CP reset needs to be separate from Link Clk Compensator reset", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014999345, "AUTOCLONE: PVC -B0 :Icunit ECC logic - Mie addr mux issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015035993, "Shift left data output mismatch when shift amount (inA) format is Q, shift data source (inC)/destination (out) is W or DW", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015227452, "AUTOCLONE: AUTOCLONE: TDL EU Bubble Rate Randomization causing dpas & em write collision", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015305692, "EU EMON event IPC count missing the 2nd DP event", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011643596, "EUFPUUNIT(PVC B0): hp2wdw move op fpu_ga_out mismatch (HECTOR)", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011764597, "[PVC-XTA0]: LSC Stuck on Fence Message", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012312241, "[PVC] OAC A7 Counter is 24 Bit instead of 32 Bit due to typo", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012725276, "SIMD16 QW results in mismatch in HW", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012857344, "PVC:GTPM B0: 1X4  : Rc6 Entry is broken  during media power down due to acm_vr_settled_up condition", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012863088, "PVC: wake from MDFI, LNEP", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16012943437, "Byte swizzle write combine focused test failing on hardware", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16013122114, "PVCXT A0 : DTS Temperature calculation logic issue", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16013172390, "PVC XTB0- Update definition of GADSS 128B Compression chicken bit", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18015335494, "[PVC PO] fpu_uncorr_err on integer conformance test cases ", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014440446, "[PVC XT A0]: Mismatch for register observed while running gt_lrc selftest ( blacklist TRTT registers & security concern ) ", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015004472, "PVC: CFEG Fixed mode bug when rcu_ccs_mode == 7", WA_BUG_TYPE_HANG | WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015065592, "PVC:GTPM B0:: RC6 entry hang in 0vdbox config", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011179476, "Use new clock gating chicken bit for RAMBO_FTL in PVC B-step", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011647401, "[PVC][XT][A0] Math HF packed instructions doesnt work for destination subregnum != 0", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011786182, "[PVC][XT][A0 B0] Read suppression data corruption in FPU0 when you switch between sp and non-sp FPU data bus", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012539442, "[PVC B0] VF_INT_TRIGGER register (10_2030h) writes from remote sgunit dropped", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012557804, "mixed mode f/bf ops in vector datapath that output bf using float rounding semantics with truncate", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012746875, "word bfn with acc src1 and acc:dst results in mismatch", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012747633, "[PVC][XT][B0] ocl_cts_khr_2_1_conversions_short_sat_double_wimpy_reduction_factor_16384 failing with corruption on ww13p3 1x4 emulation model",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012878696, "PVC/Xe2: Write pointer not restored after power context save", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18017747507, "AUTOCLONE: Xe2: geom_feclt_svr: VF RTL is not inserting common vtx after batch level preemption for TRIFAN", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14015301095, "[DG2] EU_INST_EXECUTED_BITCONV/BARRIER/PREDICATION/NONDIVERGENT, and EU_STALL_PIPESTALL_CYCLES, EU_STALL_CONTROL_CYCLES events are not implemented",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015301706, "[DG2] Clone from Xe2 - SAMPLER_INPUT_AVAILABLE external events counting incorrectly", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18018781329, "[DG2-512  CLONE] Memory ordering violation in GAM", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1509727124, "[DG2][512 / 128 EU FRD][B0] genshin impact hangs due to sampler bug in sc power optimization", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_18013277190, "[DG2] EU events not implemented", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18013277277, "[DG2] Raster events not implemented", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014590583, "[TigerLake UP4][20H2]MIPI panel  in command mode, can't enter low power state in Idle screen on scenario", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014971508, "PSR2 SFF override will not work if DC6v entry after write before SFF serviced", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013746327, "[ASUS][ADL][Win11][9885]There was screen flicker on the 6bit+ FRC panel.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015401596, "Panel Replay VSC SDP not getting sent when VRR is enabled and W1 and W2 are 0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015402699, "GMP VDIP gets dropped when enabled without VSC DIP being enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015463033, "[DG2] [AV1 VDEnc] BRC 4K TU7 test hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015436713, "D14MTL overwrite fbc 32bpp compressed data extension bits with zero when PIPE_MISC pixel extension bit is configured to zero extend",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014892111, "AUTOCLONE: ATS: DRAW_WATERMARK (26c0h) not getting context save/restored", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22013824413, "AUTOCLONE: [DG2] LSC byte read/write external event counters reporting incorrect results", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1508916338, "AUTOCLONE: Xe2: geom_feclt_svr: Wrong vtxcntperinst sent by VFG RTL on GDI bus", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16012775297, "AUTOCLONE: Xe2: geom_feclt_svr: Ctrl cycle on odd pkt at VF-VS intf", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14015447018, "AUTOCLONE: xe2: rowult: breakpoint en : not propogating due to snapshot_en is zero", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013824369, "[DG2] GPU_MEMORY_L3_READ/WRITE external events reporting incorrect values", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015402006, "AUTOCLONE: xe2: rowult: back 2 back exceptions in eu during halt mode", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014019105, "AUTOCLONE: AUTOCLONE: TDL to TDC URB deref is not back pressuring with credit", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14015300958, "[DG2]  SHADER_PIX_KILL external event is broken for DG2-128-B0 Silicon", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14015465469, "GRF corruption issue in divergent nested calls in", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015015624, "[DG2] Driver workaround for Audio PME issue", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015573800, "[DG2-512 C0]: Read suppression bug with instruction with indirect access", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_InitializeKcrChicken, "KCR_CHICKEN value is lost on D3Cold in hybrid configuration", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD | WA_COMPONENT_GMM | WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_14014971492, "MSO+PSR2 can result in underflow if vblank is synchronized after hblank to cdclk", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015648006, "Underrun observed on PSR exit in HRR timings with small vblank", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15010089951, "[Gen12.7][E2EC][DG2][Silicon][Perf]DG2 VESFC performance lower ~15% when E2EC feature is enabled.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_14015527373,
           "[DG2 512 C0] mlOPs tester WL hang on DG 512 C0 with systolic hysteresis 100us due to Render Power down immediately (Render Power gate Hysteresis being zero)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14014372222, "AUTOCLONE: D14HPG pipe scaler2 not supporting vertical initial phase of 1.5", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015574849, "SGCI unit:  POISON_DATA_HANDLING_ENABLE  should be used to virally poison", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014612214, "[PVC A0][2T] [ES1] Observed GuC tlb validation failed while running binocle/molten full memory test (increase the timeout in GuC to 500us )",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015480095, "reset domain crossing violation can potentially lead to FSM state corruption.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015397755, "AUTOCLONE: AUTOCLONE: AUTOCLONE: [XE2] mad ga data mismatch on xe2_accf_wscalar_1025a_450", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014263786, "[Dell_Horizon MLK] 240hz/360hz Panel flikcer after change specfic desktop wallpaper.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014912113, "TGL: Handle corruption in TDS", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(WaOverrideMaxSliceSubSliceGucSysInfoValues, "Due to UM Regressions, Sending older static values only. Temp WA.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_16015201720, "[ADL M/P][Cobalt]: Observing TDR 117 [ GEN12LP_0_DISPLAY] during Sx cycling.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015420481, "AUTOCLONE: [DG2][DPCLT] Fast Clear  ss phase 0 drop_rtw EXP = 1 ACTUAL = 0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16014476788, "AUTOCLONE: PVC XT+ : SLM Perf Improvement fix found in GRL workloads (RT)", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015433399, "[DG2] DATAPORT_TEXTURE_CACHE_HIT OA programmable external event is reporting incorrect info", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015498118, "[DG2] EU_DATAPORT_FENCE_MESSAGE_COUNT OA programmable external event is reporting 0s", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015528146, "AUTOCLONE: [DPCLT] EOS/SOS Mismatch Due to CPQ Fragmentation", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18013179988, "[DG2] OA timestamp != command streamer timestamp", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015782607, "[512-DG2][C0][Vulkan] Doom Eternal hang with RT enabled due to TDL sending incorrect ExID to LSC", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_14015795083, "TDL to use cuclk for mcr registers", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18019110168, "[DG2] Incorrect per-primitive constant data in clipped triangle", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014226127, "[DG2][DML] fp16 precision error in mcconv.exe test", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16014390852, "AUTOCLONE: AUTOCLONE: AUTOCLONE: Geom_feclt_SVR: Reduced FIFO: Hang as HS URBM not done when TASK shader is disabled", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18019816803, "[DG2] Diablo III.dx11-g6 - Tdr.HwHang due to duplicate transactions from Pfe to IZ for a given cacheline", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_16011698357, "EUFPUUNIT(PVC B0): dp2qw move op fpu_ga_flags mismatch (HECTOR)", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015161906, "AUTOCLONE: [ALT mode] [XE2] csel RTL outputs INF even know we are in ALT mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_18019627453, "[DG2-512 B0/C0] Red Dead Redemption TDR visible on stream", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22014344549, "[COFECLT] PFE Sending Fast Clear & Resolve to MSC When drop_rtw Was Set", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D | WA_COMPONENT_OGL)

WA_DECLARE(Wa_14015568240, "AUTOCLONE: AUTOCLONE: [PVC PO][XT B0] OA timestamp frequency is not the same as CS timestamp frequency", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015076503, "[MTL][GSC]Production GSC FW Engine Reset time is too high", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14015784397, "AUTOCLONE: AUTOCLONE: AUTOCLONE: [ARL-384] Mcfg sending multiple interrupts for parity instead of being sticky", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16015282277, "[DG2] small/large drawcall detection in CS and VFG not in sync", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_1509820217, "AUTOCLONE: AUTOCLONE: XE2: SO DECL issue - CRC Assertion Failure", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14015965466, "ATS: Latency for invalidation read suppression buffer doesn't match between 2 EU can cause EU going out of sync", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015907227, "ARL - D3D12-MeshShader-LargeMesh#0#0 - Hang", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015461347, "AUTOCLONE: AUTOCLONE: LNL: Device error status registers to be reset on FLR(fatal, non-fatal and correctable)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22014412737, "[Dell_Compal_ADL_Odyssey]Final Fantasy XV benchmark will auto exit after test for few minutes.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016074189, "[DG2-512 ][C0] EUGA Read Suppression Assumes that Writebacks for a “send instruction” will be received for both fused EUs",
           WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014263458, "[DG2][128B1] EUTC Unit Read Suppression Issue With Fused Off Send Instruction Causing Flag Register Dependency To Not Clear For One of The 2 Fused EUs",
           WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016243945, "AUTOCLONE: AUTOCLONE: GRF corruption issue in divergent nested calls in - HSD to track SW WA with HW fix", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaFlushTLBOnDestroyContext, "[CFL][GMM] Invalid access to stale TLB was causing BSOD on Gen9 systems.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_GMM)

WA_DECLARE(Wa_1309217326, "[ADL] P 282– GRITS – Fail to run GRITS seeds (EFI and OBJ types) when TBT enable in IFWI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016153635, "[ADLP] AV1 decode failures due to Incorrect DFTRING hub bypass", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_14016303323, "PSR2 disable and frame change event in CAPTURE frame causes RFB storage error", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014559856, "IC Prefetch buffer with stale entries", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18018999230, "Indirect call through function pointers with EU fusion enabled corrupts data or hangs up the GPU (TGL+)", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015204835, "GMP VDIP gets dropped when enabled without VSC DIP being enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22013704877, "AUTOCLONE: [DG2] A33 counters are broken", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014600077, "xe2: [ICUNIT] ensure entire prefetch pipeline is flushed before sending ack back to TDL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015327058, "DG2 WA to program display PHY registers at run time for DP 2 compliance", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016368929, "TDL is using same chicken bit for two different issues", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22012751935, "Gen12LP: GAMCCS drops cycles when aux invalidation occurs at a non-idle boundary.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14015497455, "ADL RGB32bpp on 8bpc/6bpc port output does not have input/output accuracy", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015601265,
           "AUTOCLONE: AUTOCLONE: AUTOCLONE: [PVC B0/B1][GTPM][RC6][2T] Tile1 RC6 entry is failing at WT_GAM_GO0 during cross tile access (issue will not be in B3/B4 parts - INF "
           "SEC pattern coverage enabled from MFG side ) ( HW bug)",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaPeriodicDccUnstallCheck, "[TGL+] Provide a period wake-up H2G to help GUC unstall DCC if ARAT timer fails to occur", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_PWRCONS)

WA_DECLARE(Wa_HdmiNoNullPacketAndAudio,
           "Sharp-NEC Panels observed Display Blankouts due to Large number of Null Packets send during the Hsync/VSync period. This WA is to Operate Display in HDMI Mode except "
           "Null Packets and Audio.",
           WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MINIPORT)

WA_DECLARE(Wa_16015675438,
           "[DG2] [From PVC B3][2T][XT][Compute] [Semaphore Wait] Observing Test hang while executing OCL test_bruteforce  ( pipe control hang signature) [ CFEG hangs on a "
           "compute walker before state delivery] - HW bug",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_KMD | WA_COMPONENT_OGL)

WA_DECLARE(Wa_22014672072, "[DG2] [Dell_Compal_ADL_Odyssey] Perf Issues in DG2 due to RC6 not accounting for Lmem access through MERT for RCIdle Hysteresis", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18018076418, "AUTOCLONE: No support for CS_MI_ADDRESS_OFFSET in MI_REPORT_PERF_COUNT command", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015775764, "AUTOCLONE: [PVC PO] [PVC B0] The reset domain issue : DSS_UM_COMPRESSION(0xE4C0) -  bspec update", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015275368, "PVC EUSTALL Flush not waiting write completions", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015363166, "EU_INST_EXECUTED_NONDIVERGENT OA external event implemented incorrectly as DIVERGENT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015474168,
           "EUTC HW bug on Exception Handling at the same time execution instructions like WHILE using BTB buffer (AUTOCLONE: WMTP : thread hung with notify2 dependency )",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015611258, "AUTOCLONE: GFXDRV: ELG ww47.3_7x4_EMUL Resnet Inference res2a-21ww09.1 Hang", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16014617026, "Parity error detected L3Bank for PSMI packets", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015411855, "Few of CCS CLs which are modified is not evicted", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15010524387, "[PVC B0][GTPM][RC6][2T] GT is hung when attempting to load 2T RC6 enabled driver -- tracking for gpmunit issue", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015856466, "[PVC B1] [2T] global timestamps out of sync - HW bug(due to di/dt programming)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015840385, "PVC -lnhec*unit clock gating issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015649647, "AUTOCLONE: AUTOCLONE: ARL: IP entering into RC1P (16MHz frequency state) during GuC's DMA memory transactions", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016291713, "[ASUS][ADL-P][UX8402][21H2][1369]There was screen flicker(underrun) on excel launched or excel sheet switched aging", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_15010599737, "AUTOCLONE: [DG2] WHQL multisample centroid test fail", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015997824, "AUTOCLONE: AUTOCLONE: Security Issue with Copy Engine caching in L3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_18020335297, "[DG2-128 B1] Geometry flickering if guardbound clip test is enabled.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18018699957, "[DG2][C-step] NOA programming lost.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16016575796, "AUTOCLONE: AUTOCLONE: SfWbus mismatches due to mismatch in hash table data coming to fulsim and RTL", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18018764978,
           "AUTOCLONE: [DG2][CFL-S][DX11][512FRD B0][Top200] Warhammer: Vermintide 2 - Transparency corruptions due to WAR hazard introduced by default PS SYNC stall behavior",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16016576128, "AUTOCLONE: AUTOCLONE: [Xe2] Send UAV cycles for a culled draw in VFG", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16016462106, "AUTOCLONE: AUTOCLONE: SF WM mismatches for the clear rect poly generated by SF for WM_HZ_OP", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_D3D)

WA_DECLARE(Wa_14015868140, "AUTOCLONE: [DG2:Refresh]Enable CS caching in L3$ for the Flat cache config", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14016747170, "MTL A0: Fuse Mirror 0x9114 in GCD is always reading 0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16011819756, "[TGL-H_GC][20H1][Cons][Display]white color screen observed 2 to 3 sec during restart with HDR enabled eDP", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(
Wa_16013994831,
"AUTOCLONE: Observed TDR while running 3dsmax-07 benchmark of  SPECviewperf® 2020 in 4k HDMI display(DGPU) due to SOL not waiting for write completions prior to sending OK to CS",
WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18020603990, "[RPL-S A0] Sporadic failures with clip distances in VS", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22014953428, "[ADLP_384_MRB][DG2][Gaming][Vulkan] Rage 2 - BSOD during gameplay due to PCPunit not handling read/completions correctly for disabled slices",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15011116421, "[DG2][128 & 512] Screen flash due to need re-emit of 3DSTATE_VIEWPORT_STATE_POINTERS_SF_CLIP instruction for each draw", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_14015353694, "AUTOCLONE:  Hardware Needs to Add Support For Standalone Dual Source Messages, Hangs on SI", WA_BUG_TYPE_HANG | WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableTsHsDs, "Temporary Fix for IOTG. Disabling Tesselation, HS and DS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18019271663, "[DG2][FRD128 B1 QS][DX11] Unigine Valley Benchmark, Unigine Heaven | Corruption with MSAA x4", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_22014451693, "[RPL-P][CVF][QAC] UF camera preview is black screen after privacy enable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaOSPostponePcEventForMultiOsMenu, "WA to Postpone PC Event on multi-OS selection screen", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_PWRCONS)

WA_DECLARE(Wa_18021976375, "[DG1][ADL-S\RPL-S][HW Bug] GPU Hang observed on stream from RedDead Redemption2 when RCS+CCS are working at same time", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18020744125, "[PVC 2T Bx/A0] Unexpected catastrophic memory error from GPU - TDL interrupt always gets generated to RCS/CCCS - HW bug", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16016694945, "PVC [XT B4]: MOCS State Override Mode by LSC based instructions to enforce L3 Cacheability disabled by default", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016969963, "Xe2 WMTP:  Fatal in sampler path due to the scheme of TDL populating SSP is broken", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016790560, "FUSE3_MBC_MEDIA register (0x389118) not reflecting the value from meml3_en fuse", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16015636889, "[PVC B0] OA free running counters not incrementing -SPM4", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaDisableInvalidTlbEntriesNotCachedSupport, "Disable OS TLB invalidation optimization", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_18020355813, "[DG2][B0] Breakpoint after jump/goto instruction doesn't wait for jump/goto to be resolved", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22015279794, "[ICUNIT] track IC prefetch before sending flush ack back to TDL", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18022508906,
           "Render is getting disabled in SOL unit when stencil test, depth test, depth write, PS, legacy depth buffer clear and depth buffer resol enable are low. ",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14016407139, "[MSI Press Kit][DG2 128]Far Cry 6 - Character flickering hair corruption", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_22015475538, "[DG2] When running multiple global fences along with large block messages LSC deadlock happens", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016833923, "MTL type-C DP-alt MFD (DPx2) not working after plugging DPx4 dongle first", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016880151, "AUTOCLONE: AUTOCLONE: EOC clear not clearing EUGAunit internal RS buffer  in Large GRF mode - security risk", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015889097, "TGL display PLL afc startup adjustment workaround", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017073508, "[MTL-P] media transactions stuck on path to memory with MC6 and pkg c3 enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16017351516, "[ADL]: Gamma LUT is corrupted when programing Index and Data via DSB in MMIO Mode", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017066071, "[MTL-P][A0][A2]Auto restart and Hang Observed with Unigine Heaven Benchmark due to an issue in the sampler OOO arbiter algorithm", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016712196, "AUTOCLONE: AUTOCLONE: AUTOCLONE: Potential HW bug with PipeControl colliding with internal state changes", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14016740474, "[MTL-P PO][Display]: PMA Standardization - PM Response timeout not getting cleared", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017202303, "MTL type-C display PLL lock delay", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016945807, "SEL_FETCH_CUR_CTL is not disabling cursor in selective fetch frames", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14016777647, "'PICA_DEVICE_ID' Needs To Be Restored After FLR", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18023229625, "[DG2] Sequence of DPAS instructions cause incorrect RS buffer invalidation resulting Fused EUs to go Out Of Sync", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16011627967, "AUTOCLONE: MTL : pipe3d: EOT conflicting with ARF dependency", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaEnableCcsAnd47BForCrossConfigVf, "Disabling CCS & 47B Addressing is Causing some issues on Cross Config SRIOV cases. Temp WA to enable CCS and 47bit Addressing",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017245111, "[MTLP-A0]: Deadlock observed in lsc due to contention between 2 sequencers for the same 2 sets", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_Vp9UnalignedHeight, "[TGL] Unaligned to 8 height (270) VP9 encode corruption", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_14017131883, "AUTOCLONE: Reading r0 between barrier msg and sync.bar breaks eu read suppression logic", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017110345, "AUTOCLONE: SEL_FETCH_CUR_CTL is not disabling cursor in selective fetch frames", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017322320, "grf read supression reset by writeback in one of fused EUs causing issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017397744, "[ICUNIT] IC prefetch tracking counter width increase", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017240301, "AUTOCLONE: [MTL-P][A0][A2]3D Aux Walker reads from incorrect cache location resulting in hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_14016945873, "SEL_FETCH_CUR_CTL is not disabling cursor in selective fetch frames", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017179389, "xe2_LPD: DPFC WB FIFO is in-correctly reading from an entry which is being invalidated", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22011428074, "AUTOCLONE: AUTOCLONE: AUTOCLONE: Registers E700missing in PWR CTX SAVE/RESTORE", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_18022502561, "POCS is not considering csdvr to go high while sampling csdatar", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1409203812, "AUTOCLONE: AUTOCLONE: AUTOCLONE: [GEN-12HP] [UNIT DAPRSS] ColorFE: Mismatch on pfe_msc_blend_without_dest", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_16018038193, "ACMR : EU : GA going out of sync as dpas in predicared branch cause FPU buffers to go out of sync", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18022330953, "AUTOCLONE: AUTOCLONE: [MTL-PO] SVL unit Constant state is made zero in RTL for both header and data after fence.", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14017468336, "AUTOCLONE: MTL[P] DIRT5 -EU -WM hang with SIMD32", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017574792, "ADL: DP HDR Looks Desaturated with Few Panels When using VSC_EXT_SDP DIP for HDR Metadata", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017574489, "xe2_LPD: DPFC WB FIFO is in-correctly reading from an entry which is being invalidated - SW WA tracking", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15010203763, "[DG2] D64-SIMT scratch-surface messages does not work", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15010685871, "[DG2 512 C1] CDCLK switch hung in CLK Ungate when Disabling/enabling CDCLK with Squash enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017387313, "MGSR Steering Semaphore for GAM register reads can lead to driver deadlock", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017204320, "xe2lpd cdclkpll/squash clk enable wrong connectivity", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16016772977, "AUTOCLONE: Ran NISA with odd number of threads, seeing DPAS data mismatches", WA_BUG_TYPE_CORRUPTION | WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18022196608, "[DG2][128MRB B1][DX12] Gears 5 - TDR with BSOD at specific location", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017427316, "exip corruption when single stepping on EOT send", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16016805146, "[PVC B4] : LSC hangs when running concurrent stress compute tests (TLB invalidation) (FTLB miss completion dropped) - HW bug", WA_BUG_TYPE_PERF,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16017236439, "Fabric deadlock in lniblsn due to read/write  meta pack credit check issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16017272135, "[PVC Bx][PSMI]With PSMI enabled (Sqidi/MERT), on full config, observing GT hang with molten workloads - HW bug", WA_BUG_TYPE_HANG,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14015566243, "FWD:  [PVC B0] T2T MDFI counters show non-zero value after the cold boot/RC6", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18022722726, "[PVC] : Missing EU attention bits when breakpoint on a first instruction.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_1509220884, "AUTOCLONE: PVC B0: Disable Copy Engine Fast Clear as it does not work across devices", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_16016485408, "AUTOCLONE: DG2: Gflush is happening before all the memory writes are completed", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_22015983198, "GMP VDIP gets dropped when enabled without VSC DIP being enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18023963327, "[MTL-P][OAG] OA A36/A37 counter increments are 4* greater than expected", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18023884638, "[MTL-P][SAMEDIA]OAM OaBuffer tail pointer doesn't wrap after reaching buffer limit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017171315, "AUTOCLONE: xe2 - rowult.DOP gating causing Incorrect eu_tdl_perf_counter0 count (PES7) programmed count captured", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017333800,
           "AUTOCLONE: AUTOCLONE: AUTOCLONE: AUTOCLONE: AUTOCLONE: AUTOCLONE: GFXDRV: ELG xe2_gt_ww32.2_2x2_EMUL_LSC_Patch DX12 WGF11PixelShader PipelineStats Failure",
           WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

WA_DECLARE(Wa_14017654203, "AUTOCLONE: [MTL-P][A0][A2]Auto restart and Hang Observed with Unigine Heaven Benchmark due to ST inused_hold issue", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018063123, "AUTOCLONE: AUTOCLONE: AUTOCLONE: Xe2: Pipeblt: state machine is reaching to idle state before all subblits got completed", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_14017868169, "Streamer waking up too late while in a never ending PM Fill", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22015614752, "[DG2] - tile4 corruption caused by Compressed surface not aligned to 64Kb", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

WA_DECLARE(Wa_16018255862, "[LNL-Media] [OAM]: OA behaviour in Overrun mode needs change to support OA Buffer size not being multiple of Report size cases", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18023881693, "[MTL] Dither Enable is not properly tied causes a incorrect output when slow clear is used with Repcol", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D)

WA_DECLARE(Wa_15011264113, "[MTL-P Linux PO][Media][VP]: SFC interlaced to interlaced scaling case output R2R corruption", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_MEDIA)

WA_DECLARE(Wa_14017986919, "AUTOCLONE: [Manual clone] xe2: rowult : send atomic should have zero at reset as emask 1 in first instruction causes x prop", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_13010300992, "[Manual clone] GFXDRV: MTL B0 Dx12  World of Warcraft Hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017987381, "[Manual clone] xe2: rowult : send atomic should have zero at reset as emask 1 in first instruction causes x prop", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018031267, "AUTOCLONE: AUTOCLONE: AUTOCLONE: AUTOCLONE: AUTOCLONE: ARLP  Pipeblt: state machine is reaching to idle state before all subblits got completed",
           WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017794102, "AUTOCLONE: [Xe2 - BMG/LNL] Disable WMTP for RT/BTD kernels", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018650333, "AUTOCLONE: [Xe2-3D] [CS CLUSTER] BCSPC hang when autotail sampling takes precedence over lite restore causing to be stuck in WAIT_PREMEPT state",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_22016140776, "AUTOCLONE: AUTOCLONE: [PVC] operation unexpectedly results in NAN", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(WaForceMediaResetOnStretchBltPF, "Force a media reset via a timeout when a PF is hit during a stretch blt", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_KMD)

WA_DECLARE(Wa_13010300985, "[Manual clone] GFXDRV: MTL B0 Dx12  World of Warcraft Hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017987365, "[Manual clone] xe2: rowult : send atomic should have zero at reset as emask 1 in first instruction causes x prop", WA_BUG_TYPE_CORRUPTION,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_15012014987, "AUTOCLONE: [Dg2][512]  X prop in eutcunit due to first instruction in the kernel getting shot down due to emask being 0.", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018610683, "AUTOCLONE: DPCLT: 160K SLM Ray Tracing deadlock", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_D3D | WA_COMPONENT_KMD)

WA_DECLARE(Wa_14017715663, "AUTOCLONE: AUTOCLONE: [PVC] incorrect result on byte operations", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_18024947630, "AUTOCLONE: AUTOCLONE: [PVC][USM] HW bug in GAM - Compute workload never ends in scenario with KMD migration", WA_BUG_TYPE_UNKNOWN,
           WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018807274, "[Xe2-Media] [CS CLUSTER] BCSPC hang when autotail sampling takes precedence over lite restore causing to be stuck in WAIT_PREMEPT state",
           WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

WA_DECLARE(Wa_15011665187, "[MTL-P Win][Media][VP][Gate][RTL Simulation Debug]: VE DN mismatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018712365, "AUTOCLONE: LNL GT : SLM Atomics perf dropping ~22% - LSC Chicken Bit Polarity Incorrect", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
           WA_COMPONENT_UNKNOWN)

WA_DECLARE(Wa_16018737384, "AUTOCLONE: GFXDRV: ELG TimeSpy hang on cim 12607 with igc key Enable2xGRFRetry", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

// Add new Workarounds here
WA_DECLARE(WaPcode10msTimeOut, "Increasing the PcodeTimeout to 10ms", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)