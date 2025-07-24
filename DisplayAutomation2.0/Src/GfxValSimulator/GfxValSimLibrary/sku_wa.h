/*========================== begin_copyright_notice ============================

INTEL CONFIDENTIAL

Copyright (C) 2011-2022 Intel Corporation

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

#ifndef __SKU_WA_H__
#define __SKU_WA_H__

#ifdef _USC_
// Sku_Wa is defined by usc.h
#include "usc.h"
#define SKU_FEATURE_TABLE SUscSkuFeatureTable
#define PSKU_FEATURE_TABLE SUscSkuFeatureTable *

#else                     //! defined(_USC_)
#include "Driver_Model.h" // For our XP and LH Macros

// Prevent the following...
// warning: ISO C++ prohibits anonymous structs [-pedantic]
// warning: ISO C90 doesn't support unnamed structs/unions [-pedantic]
#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wpedantic" // clang only recognizes -Wpedantic
#elif defined(__GNUC__)
#pragma GCC diagnostic push
#if __GNUC__ >= 6
#pragma GCC diagnostic ignored "-Wpedantic"
#else
#pragma GCC diagnostic ignored "-pedantic" // gcc <= 4.7.4 only recognizes -pedantic
#endif
#endif

#pragma warning(push)
#pragma warning(disable : 4201)
//********************************** SKU ****************************************

// Sku Table structure to abstract sku based hw feature availability
// For any Sku based feature, add a field in this structure

typedef struct _SKU_FEATURE_TABLE
{
    // flags 1 = available, 0 = not available
    struct //_sku_Core
    {
        unsigned int FtrDesktop : 1;                    // Whether Desktop
        unsigned int FtrMultiFunc : 1;                  // Whether Multi func device
        unsigned int FtrGttBar : 1;                     // Gtt bar
        unsigned int FtrGmadrBar : 1;                   // Gmadr bar
        unsigned int FtrStolenAsLmemBar : 1;            // Stolen as Bar
        unsigned int FtrMmioBar : 1;                    // Mmio bar
        unsigned int FtrDioBar : 1;                     // Direct io bar
        unsigned int FtrOptionRomBar : 1;               // Supports Option ROM or not
        unsigned int FtrPrimaryVga : 1;                 // Adapter is primary Vga
        unsigned int FtrBandwidthLimit : 1;             // Core frequency is limited
        unsigned int FtrCoreClkLimit : 1;               // Limit core clock
        unsigned int Ftr36BitPhysAddress : 1;           // 36 bit physical address support
        unsigned int FtrVTdEnabled : 1;                 // VT-d support
        unsigned int FtrPgtblEnableSupported : 1;       // PGTBL_CTL supports "Page Table Enable" (Bit 0)
        unsigned int FtrVERing : 1;                     // Separate Ring for VideoEnhancement commands
        unsigned int FtrBlitterRing : 1;                // Separate Ring for Blitter commands
        unsigned int FtrMFXRing : 1;                    // Separate Media decode Engine from Gen 6 onwards
        unsigned int FtrVcs2 : 1;                       // Second VCS engine supported on Gen8 to Gen10 (in some configurations);
                                                        // GEN11 also has multiple VCS engines, but all are mapped to a single VCS node, so this feature flag is disabled on GEN11+.
        unsigned int Ftr3dRing : 1;                     // Separate Ring for for 3D commands
        unsigned int FtrPics : 1;                       // A pinning engine supported on CNL+ (in specific SKUs only)
        unsigned int FtrGtBigDie : 1;                   // Indicate Big Die Silicon
        unsigned int FtrGtMediumDie : 1;                // Indicate Medium Die Silicon
        unsigned int FtrGtSmallDie : 1;                 // Indicate Small Die Silicon
        unsigned int FtrGT1 : 1;                        // Indicates GT1 part
        unsigned int FtrNativeGT1 : 1;                  // Indicates GT1 part (regardless whether it was fused down)
        unsigned int FtrGT1_5 : 1;                      // Indicates GT1.5 part // new for HSW
        unsigned int FtrGT1_75 : 1;                     // Indicates GT 1.75 part, new for HSW
        unsigned int FtrGT1_6 : 1;                      // Indicates GT1.6 part //New for IVB
        unsigned int FtrGT2 : 1;                        // Indicates GT2 part
        unsigned int FtrNativeGT2 : 1;                  // Indicates GT2 part (regardless whether it was fused down)
        unsigned int FtrGT2_5 : 1;                      // Indicates GT2.5 part
        unsigned int FtrGT3 : 1;                        // Indicates GT3 part
        unsigned int FtrNativeGT3 : 1;                  // Indicates GT3 part (regardless whether it was fused down)
        unsigned int FtrGT4 : 1;                        // Indicates GT4 part
        unsigned int FtrPureGT1 : 1;                    // Indicates Pure GT1 part (GT1 die, not fused down)
        unsigned int FtrGTEuRowSelectLower : 1;         // Indicates GT1 with lower row of EUs selected. (2,3) Only applies to GT2 fused to GT1.
        unsigned int FtrGTEuRowSelectUpper : 1;         // Indicates GT1 with upper row of EUs selected. (0,1) Only applies to GT2 fused to GT1.
        unsigned int FtrGT4plus2 : 1;                   // Indicates 4+2 GT part
        unsigned int FtrGT4plus1 : 1;                   // Indicates 4+1 GT part
        unsigned int FtrGT2plus2 : 1;                   // Indicates 2+2 GT part
        unsigned int FtrGT2plus1 : 1;                   // Indicates 2+1 GT part
        unsigned int FtrEmbeddedPlatformEnabled : 1;    // Indiciates ECG Platform Support
        unsigned int FtrULT : 1;                        // Indicates ULT SKU
        unsigned int FtrIVBK0Platform : 1;              // Indicates whether the platform is IVB K0
        unsigned int FtrIVBM0M1Platform : 1;            // Indicates whether the platform in IVB M0/M1
        unsigned int FtrIVBL0Platform : 1;              // Indicates whether the platform in IVB L0
        unsigned int FtrIVBL1Platform : 1;              // Indicates whether the platform in IVB L1
        unsigned int FtrIVBN0Platform : 1;              // Indicates whether the platform in IVB N0
        unsigned int FtrIVBE0E1Platform : 1;            // Indicates whether the platform in IVB E0/E1
        unsigned int FtrIVBE2Platform : 1;              // Indicates whether the platform in IVB E2
        unsigned int FtrVXDEnabled : 1;                 // Indicates that VXD device from IMG is enabled
        unsigned int FtrInternalSSC : 1;                // Indicates if Internal SSAC is available
        unsigned int FtrUseMuxedSSCAsRef : 1;           // Indicates if Muxed SSC can be used as reference to PLLs
        unsigned int FtrChannelSwizzlingXOREnabled : 1; // Indicates Channel Swizzling XOR feature support
        unsigned int FtrULX : 1;                        // Indicates ULX SKU
        unsigned int FtrPipeCDisabled : 1;              // PipeC disabled for DSKU
        unsigned int FtrPipeDDisabled : 1;
        unsigned int FtrNumOfPipes : 3;                  //
        unsigned int FtrGTA : 1;                         // Indicates BXT SKU A 3X6 - USED FOR GLV too, 3x6 SKU
        unsigned int FtrGTC : 1;                         // Indicates BXT SKU C 2X6
        unsigned int FtrGTX : 1;                         // Indicates BXT SKU X 3*8
        unsigned int Ftr5Slice : 1;                      // Indicates KBL 15x8 SKU
        unsigned int FtrLLCMLCNotSupported : 1;          // LLC or MLC support not there in VLV
        unsigned int FtrGfxClientSubmission : 1;         // Gfx Client Submissions via GuC (iTouch, Clifton, etc.)
        unsigned int FtrLCIA : 1;                        // Indicates Atom (Low Cost Intel Architecture)
        unsigned int FtrPinning : 1;                     // To indicate whether pinning is supported.
        unsigned int FtrHalo : 1;                        // Indicates HALO SKU
        unsigned int FtrDt : 1;                          // Indicates DT SKU
        unsigned int FtrPosh : 1;                        // To indicate if POSH is enabled.
        unsigned int FtrResourceStreamer : 1;            // To indicate if the HW supports RS.
        unsigned int FtrShaderDoubleSupportDisabled : 1; // To indicate shader support for double-precision floating-point numbers
        unsigned int FtrHwSemaphore : 1;
        unsigned int FtrCCSRing : 1;                         // To indicate if CCS hardware ring support is present.
        unsigned int FtrPAAC : 1;                            // To indicate if dual context support requires Partitioned address space between RCS/CCS.
        unsigned int FtrEnableCCSViaIGCC : 1;                // To enable async compute via IGCC app.
        unsigned int FtrCCSViaIGCCLimitedToDx12Vk : 1;       // To allow CCS submissions only in Dx12 and Vulkan via IGCC app. KMD to set this Ftr and later used by the UMDs
        unsigned int FtrCCSUsageRestricedToDx12Vk : 1;       // KMd to restrict CCS usage in gen12lp and only allow Dx12/VK.
        unsigned int FtrCCSNode : 1;                         // To indicate if CCS Node support is present.
        unsigned int FtrCCSMultiInstance : 1;                // To indicate if driver supports MultiContext mode on RCS and more than 1 CCS.
        unsigned int FtrSuperSku : 1;                        // Indicates SuperSku system. Reserved for internal validation purposes and generally enable all feature sets.
        unsigned int Ftr3rdLevelBB : 1;                      // Indicates if CS's support 3rd level Batch Buffer.
        unsigned int FtrRSDisabledHWBindingTableEnabled : 1; // To indicate if the HW supports Hw Binding table mainly applicable for Gen11+
        unsigned int FtrAdvancedMMIOWhitelist : 1;           // Indicates if medusa DCN is enabled or not for SW Whitelisting
        unsigned int FtrMediaIPSeparation : 1;               // Indicates if media IP is separated from GT (MTL+)
        unsigned int FtrRAMode : 1;                          // Indicate if RunAlone is required for protected workload
        unsigned int FtrProtectedEnableBitRequired : 1;      // Whether enable bit programming is required for protected workloads
        unsigned int FtrGTGuC : 1;    // Indicates the presence of GT GuC. Req with media IP separation (MTL+). In legacy platforms, this will be set to indicate Guc is supported.
        unsigned int FtrMediaGuC : 1; // Indicates the presence of media GuC (MTL+)
        unsigned int FtrMediaTile64NotSupported : 1; // Media tile64 not supported for TGL_HP and DG2 a-step
        unsigned int FtrMemoryRemapSupport : 1;      // Indicate if mmio remap is needed.
        unsigned int FtrL3TransientDataFlush : 1;    // Transient data flush from L3 cache
        unsigned int FtrTDFMonitorAddress : 1;       // when set indicates that HW should send a Store DW to indicate completion of the requested Transient Flush
        unsigned int FtrHwStateDumpByGuc : 1;        // When Hw State dumping via guc is enabled on reset.
        unsigned int FtrOCACSRegRange : 1;           // When csgeneric register range have to dump
        unsigned int FtrPagingNode : 1;              // New paging node added on ELG+ product.
        unsigned int FtrPerformRangeBasedTlbInvalidation : 1;
        unsigned int FtrPerformRangeBasedGucTlbInvalidation : 1;
        unsigned int FtrPerformSystemCacheInvalidation : 1;
        unsigned int FtrStateSeparation : 1; // State Separation Support
        unsigned int FtrEuDebug : 1;
        unsigned int FtrForceFlrOnTdrFailure : 1;            // Forcing FLR if adapter wide reset failed
        unsigned int FtrOcaMiniScandump : 1;                 // Allow gathering HW Scandump at OCA data collection
        unsigned int FtrRestrictInvalidFenceIdReporting : 1; // Enable FailSafe only for release driver; restrict Invalid Fence_Id to reporting to OS
        unsigned int FtrSkipInvalidSubmitsFromOS : 1;        // For OS BUG WA[MSFT 416192], Valid SegmentIDs always start with 1
        unsigned int FtrTLBInvalidationOptimization : 1;
        unsigned int FtrKernelSyncLocksProfiler : 1;
        unsigned int FtrEnableComputeAsync : 1;
        unsigned int FtrGucLoadFailSafe : 1;      // Enable FailSafe only for release driver; Increase GuC Load Dma Timeout to 2.5 seconds
        unsigned int FtrLinearCaptureSurface : 1; // Flag to Enable Linear Memory usage for IPU use cases- https://hsdes.intel.com/appstore/article/#/14017613213
    };

    struct //_sku_Display
    {
        unsigned int FtrMultiPipe : 1;            // Multi pipe
        unsigned int Ftr3Pipes : 1;               // 3 display pipes
        unsigned int FtrInternalLvds : 1;         // Internal Lvds
        unsigned int FtrCrtOnPipeB : 1;           // Crt on Pipe B
        unsigned int FtrSerialDvo : 1;            // Serial Dvo
        unsigned int FtrSDVOHDMI : 1;             // SDVO HDMI
        unsigned int FtrDualView : 1;             // DualView Support from Ironlake onwards.
        unsigned int FtrHandleSplRotation : 1;    // SPl Rotation handling case RCR for ILK
        unsigned int FtrHWRotation : 1;           // HW Rotation Support
        unsigned int FtrWirelessDisplayNndi : 1;  // Nndi based Wireless display supported
        unsigned int FtreDPonPortD : 1;           // Support for eDP on Port D
        unsigned int FtreDPonPortC : 1;           // Support for eDP on Port C
        unsigned int FtreDPonPortB : 1;           // Support for eDP on Port B
        unsigned int FtrWirelessDisplay_2_1 : 1;  // Wireless display 2.1 using desktop compose supported
        unsigned int FtrDisplayDisabled : 1;      // Server skus with Display
        unsigned int FtrSGTPVSKUStrapPresent : 1; // TPV Strap present - To defeature
        unsigned int FtrS0ixSKU : 1;              // S0ix supported SKU
        unsigned int FtrS0ixSRByGunit : 1;        // Indicate if register save/restore while S0ix transition is done by Gunit
        unsigned int FtrGfxS0ixCapable : 1;       // Gfx S0ix capable = (HSW+ && ULT && Win8) || (FtrS0ixSKU && Win8)
        unsigned int FtrConnectedStandby : 1;     // Connected Standby capable = (FtrS0ixSKU && Win8)
        unsigned int FtrVRAMSelfRefresh : 1;      // VRAM self-refresh support for DG1 and possibly later platforms
        unsigned int FtrGfxPowerShare : 1;        // Power share feature between SOC and DGPU in MBD config / AIC Config
        unsigned int FtrMPO180HWRotation : 1;     // SKU check for supporting only 180 HW Rotation, LKF+
        unsigned int FtrHwRotOffset : 1;          // SKU where for hw Rotation calculation of offsets is NOT req
        unsigned int FtrSKU4KDisplay : 1;         // 4K Display Support in IGD
        unsigned int
                     FtrSupportModesGreaterThan3840Horizontal : 1; // Modes larger than 3840x should be enabled only on certain SKU's, this flag can be used for enabling in such SKUs
        unsigned int FtrCollageSupport : 1;                        // From BDW onwards, collage is not supported on pentium and celeron SKUs
        unsigned int FtrLPEAudio : 1;                              // Indicates LPE audio support
        unsigned int FtrHDMIPixelMax225Mhz : 1;  // Display resolution/refresh rate w / pixel clock > 225; This limits the HDMI resolution to 1920x1080 when the pixel clock is
                                                 // 225Mhz and enable 4k when it is around 300Mhz. It will also disable 120hz 1080p when pixel clock is 225mhz
        unsigned int FtrDPMaxRes25x16_60 : 1;    // DP 1.x Max Res  2560x1600@60Hz
        unsigned int FtrCRTNotSupported : 1;     // Support for CRT
        unsigned int FtrMipi : 1;                // Mipi support
        unsigned int FtrCommandModeMIPI : 1;     // Mipi Command mode support
        unsigned int FtrAllowDC9WithMIPIDSR : 1; // Allow DC9 with command mode MIPI
        unsigned int FtrDualMipi : 1;            // Dual Mipi support
        unsigned int FtrSF1_0 : 1;               // Support Smart Frame version1 (inactive/non rendered Smart Frame )
        unsigned int FtrMPOSupport : 1;          // Indicates Multi Plane Overlay(MPO) Support
        unsigned int FtrDisableMPOMultiDisplayConfig : 1;      // Indicates Multi Plane Overlay(MPO) Support for Clone
        unsigned int FtrMPOSupportForMultiPipeDisplayPath : 1; // Indicates MPO support for Tiled/Pipe Joined Displays. No Collage MPO Support. Comment to be changed when Collage
                                                               // MPO is supported
        unsigned int FtrFractional48Hz : 1;                    // Fractional 48 Hz support
        unsigned int FtrCHVBxSku : 1;                          // Indicates CHV Bx Stepping
        unsigned int FtrSplitScreenMPO : 1;
        unsigned int FtrInvertRotation : 1; // Inverted Rotation for Razer RCR: 1024246
        unsigned int FtrPortraitLFP : 1;
        unsigned int FtrGunitOffset : 1;                     // GUNIT offset
        unsigned int FtrHWScalingNotSupported : 1;           // Hw Scaling not Supported on VLV and CHV
        unsigned int FtrDynamicCDClkOnlyForSDInternal : 1;   // Dynamic CD clk enabled only on Single Display internal panel config
        unsigned int FtrDDI4 : 1;                            // 4th DDI on CNL
        unsigned int FtrEnablePipePanelFitterFlipPath : 1;   // This is to be used for testing from OS side via regkey to test Pipe PF in Flip path
        unsigned int FtrEnableUnderRun : 1;                  // Set this bit for Enable Under run request, so after PM based on this bit enable under run again.
        unsigned int FtrEnable10bitRGBMPO : 1;               // Enable 10bit RGB MPO.
        unsigned int FtrSAGVNotifyPCode : 1;                 // Driver notification of PCode in interlace mode or single/multi display mode to enable/disable SAGV
        unsigned int FtrPSFNotifyPCode : 1;                  // Driver notification of PCode for single/multi display mode to enable/disable PSF freq
        unsigned int FtrValidateDramBw : 1;                  // When set, driver will check for Dram Bw and fail config if the incoming BW is > allowed Bw.
        unsigned int FtrCoG : 1;                             // CoG Support
        unsigned int FtreDPVDSC : 1;                         // eDP VDSC Support
        unsigned int FtrPeriodicFrameNotification : 1;       // Periodic Frame Notification Support
        unsigned int FtrEnableAssertOnOnUnderrun : 1;        // Set this bit for Enable BSOD if pipe underrun happens (only for validation purpose).
        unsigned int FtrDPVDSC : 1;                          // DP SST VDSC Support
        unsigned int FtrDPMSTVDSC : 1;                       // DP MST VDSC Support
        unsigned int FtrDpSinkPreferredMstDsc : 1;           // DP MST Sink Preferred VDSC Support
        unsigned int FtrFecSupportOnEdp : 1;                 // Fec support on eDP
        unsigned int FtrRestrictDPFecForX1 : 1;              // DP FEC not supported for x1 lane
        unsigned int FtrSupportYCbCrDsc : 1;                 // DSC Support for YCbCr420/YCbCr422
        unsigned int FtrDualLfpPortSync : 1;                 // Set this bit for platforms supporting dual internal panels.
        unsigned int FtrCmtgSupported : 1;                   // Set this bit for platforms supporting common primary timing generator.
        unsigned int FtrMultiPipeScalingWithSeamExcess : 1;  // Multi-pipe SD Scaling with excess pixels
        unsigned int FtrWriteback : 1;                       // Wireless Writeback Support
        unsigned int FtrDualDisplayPkgCImprovement : 1;      // VSRI-4386 : For ASUS DualDisplayPkgCImprovement Issue
        unsigned int FtrSetSourceOUI : 1;                    // VSRI-4458 - Program the Source OUI details into DPCD 300-302h for Sink device to identify Source
        unsigned int FtrSupportYCbCrAndSaturationEnable : 1; // VSRI-4337 : For Dell RCR to support YCbCr & Saturation together
        unsigned int FtrSupportReleaseofEmptyDongle : 1;     // VSRI-4230 , inform IOM when there is an empty dongle connected and let them unplug it
        unsigned int FtrSupportSmoothSync : 1;               // This is to indicate support for smooth sync capability to avoid tearing effect.
        unsigned int FtrSupportHwDarkScreenDetection : 1;    // This is to indicate support for dark screen detection hardware.
        unsigned int FtrSpeedFrame : 1;                      // This is to indicate support for speed frame capability
        unsigned int FtrVsyncOn : 1;                         // Support for converting all async flips to sync
        unsigned int FtrGamingSyncModeSupport : 1;           // Support combined interface for controlling all the gaming features
        unsigned int FtrHrrSupported : 1;                    // Half refresh rate support
        unsigned int FtrHrrTempD13 : 1;                      // Temp soln of Half refresh rate for D13
        unsigned int FtrAdaptiveSharpness : 1;               // This flag is to check whether AdaptiveSharpness Feature is supported for specific platform.
        unsigned int FtrDisableLayerReordering : 1;          // Disable plane layer re-ordering
        unsigned int FtrVirtualDisplaySupport : 1;           // This is flag to check virtual display support
        unsigned int FtrDisableSinglePipe5kModeSupport : 1;  // This is to disable 5k mode for plane size restriction of width size = 5120 to 4096
        unsigned int FtrEnhancedUnderrunRecovery : 1;        // If a SKU supports Enhanced underrun recovery
        unsigned int FtrUnderrunClassificationSupport : 1;   // When set, it indicates registers will show the classification of underrun as pipe/port etc
        unsigned int FtrPlaneSizeOffSetRestriction : 1;      // Need to do Plane Size + Offset check is this is supported.
        unsigned int FtrAsyncFlipClearColorSupport : 1;      // MTL and above platfomr support clear color changes as part of async flips, no need to convert them to sync.
        unsigned int FtrKeepGPUAwake : 1;                    // Flag to report just F0 state in D3 transition comp for a GPU
        unsigned int
                     FtrDisableSinglePipe5kPlaneSizeRestriction : 1; // Gen9 max plane size restriction we have 5120 but customer has pipe splitter design with higher plane width like 5760.
        unsigned int FtrReduceHWMaxDownScalingLimitWa : 1;           // Flag to restrict max downscale percentage on GLK to -8
        unsigned int Ftr3DLutPersistancePostPowerEvents : 1; // Flag to enable persistance post power events for 3dlut.
        unsigned int FtrUse2XWMLatencies : 1;                // Flag to use 2x pcode reported WM latencies.
        unsigned int FtrHwCasfSupport : 1;                   // Flag to indicate hardware based condional async flip support.
        unsigned int FtrPixelTransformationApiSupport : 1;   // Flag to enable pixel transformation API.
        unsigned int Ftr480MhzVoltageChangeSupport : 1;      // Flag to enable support for changing voltage at 480Mhz cd clock

#if (_DEBUG || _RELEASE_INTERNAL)
        unsigned int FtrLoadDmcFwFromFile : 1;               // Load DMC FW from %SystemRoot%\dmcfw.bin
#else
        unsigned int ReservedBitA : 1;
#endif // (_DEBUG || _RELEASE_INTERNAL)
        unsigned int FtreDPCoGonPipeB : 1;                   // Support for COG on Pipe B
        unsigned int Ftr4x1Cog : 1;                          // Support for 4X1 Cog
        unsigned int FtrDscFractionalBpp : 1;                // Support for DSC Fractional BPP
        unsigned int FtrDisableExternalDisplaysFirst : 1;    // prioritize disabling of external displays first
        unsigned int FtrReportExternalDisplayAsEDP2 : 1;     // AML Dual eDP - Report DDI_B DP as EDP2. To be removed once we have proper EDP2 detection via VBT path implemented
        unsigned int FtrDualLFPSupported : 1;                // This is to indicate Dual eDP support on Gen9 platforms
        unsigned int FtrDisablePsrInVpbWithLace : 1;         // Indicate to Disable PSR in VBP when lace is enabled to reduce panel power
        unsigned int FtrSdpDoubleBuffering : 1;              // Double Buffering support for Dynamic metadata
        unsigned int CdClockby2DivChange : 1;    // Support for direct CD2XDividerChange(Quick Change) to switch betwenn max and max/2 cdclock in CdClkPll without unlocking the PLL
        unsigned int FtrAdaptiveSyncSdp : 1;     // adaptive sync SDP support for Dp to HDMI 2.1 dongle
        unsigned int FtrNativeHdmi21Support : 1; // Support for HDMI 2.1 from MTL onwards
        unsigned int
                     FtrScalerGateCountOptimization : 1; // Gate count optimization: Defeature non-common functionalities. i.e. > 4K src scaling and second scaler downscaling support
        unsigned int FtrEnablePlanePostModeset : 1;
        unsigned int FtrReportSecondLfpAsExternal : 1;       // Support to enable dual lfp without OS's dual lfp support
        unsigned int FtrMinDbufSupportForFBR : 1;            // Flip support with Min Dbuf when FBR is active
        unsigned int FtrDpInSupport : 1;                     // Support for DP-In feature. Supported on TGL-H for now.
        unsigned int FtrGenLockEnabled : 1;                  // Support for Multichip Genlock.
        unsigned int FtrGenLockFuseDisabled : 1;             // Support  for MultiChip Genlock HW
        unsigned int FtrSupportS3D;                          // Suppport for S3D feature in Pre Gen13+ Platforms
        unsigned int FtrVirtualRefreshRateSupport : 1;       // Support for Virtual Refresh Rate feature
        unsigned int FtrAlwaysInVrrMode : 1;                 // Support for always keeping VRR TG ON for VRR supported monitors
        unsigned int FtrAlwaysInVrrModeOnNonVrrPanels : 1;   // Support for always keeping VRR TG ON for non VRR monitors
        unsigned int FtrPsrSupportWithVrrInFixedMode : 1;    // Support for PSR+VRR in fixed mode. D14+.
        unsigned int FtrPsrSupportWithVrrInVariableMode : 1; // Support for PSR+VRR in gaming mode. Future.
        unsigned int
                     FtrSupportClockBasedRrSwitchingWithoutMultiPixelClocks : 1; // Legacy support for clock based RR switching without panel having multiple modes with different pixel clocks.
        unsigned int FtrExtendedXSize : 1;                                       // Support for plane/pipe size 5760, default max is 5120.
        unsigned int FtrDisplayShiftSupport : 1;        // Support for eDP display shift between iGfx and dGfx - https://jira.devtools.intel.com/browse/VSRI-5313
        unsigned int FtrSupportInterlacedMode : 1;      // This flag is to support interlaced mode.
        unsigned int FtrDispGttFaultNotSupported : 1;   // If a SKU supports does not support GTT Page Fault handling
        unsigned int FtrDp14MstDscAudSdpSplitting : 1;  // This flag is to enable SDP Splitting for DP1.4 in MST DSC.
        unsigned int FtrEnableDbufOverlapDetection : 1; // This flag is to support the Dbuf Overlap detection interrupt which start from LNL.
        unsigned int FtrFlipQBasedVbiMasking : 1;       // FlipQ based HRR / NRR support
    };

    struct //_sku_Media_Features.
    {
        unsigned int FtrClearVideoTechnology : 1;        // ClearVideoTechnology Support
        unsigned int FtrPooledEuEnabled : 1;             // Media pooled state(enabled/disabled)
        unsigned int FtrMediaSupportResourcePooling : 1; // Meida pooled resource enable or disable
    };

    struct // TV Wizard support. This bit is used by CUI.
    {
        unsigned int FtrTVWizardSupport : 1; // Bit to indicate support for TV Wizard based
        // on sku.
    };

    struct                                 //_sku_KMD_render
    {                                      // MI commends are capable to set
        unsigned int FtrCapGttMapAddr : 1; // Gtt mapped address,eg, BLB Bit 8
        // MI_SET_CONTEXT - virtual addrss
        unsigned int FtrOverlay : 1;              // If overlays are enabled (Vista)
        unsigned int FtrOverlayMmioFlip : 1;      // Use overlay MMIO flip
        unsigned int FtrFullOverlayDownscale : 1; // Enable full overlay downscaling using 3d engine
        unsigned int FtrFixedGfxMem64MbMax : 1;   // Fixed Gfx Mem Capped at 64MB
        unsigned int FtrTotalGfxMem256MbMax : 1;  // Total Gfx Mem Capped at 256MB
        unsigned int FtrAsyncMMIOFlipSupport : 1; // Indicates support for AsynchMMIO Flip, supported
        // from Cantiga onwards as of now.
        // from Cantiga onwards as of now.
        unsigned int FtrMediaReset : 1;     // Media reset feature is supported.
        unsigned int FtrParallelEngine : 1; // Parallel engine support (Vista)

        unsigned int FtrEnableCloneOverlay : 1;         // Enable Overlay for Clone mode.
        unsigned int FtrEnableCollageOverlay : 1;       // Enable Overlay for collage mode.
        unsigned int FtrEnableTDDebugControlRegKey : 1; // Enable control of TD_DebugControl2 via Reg Key

        unsigned int FtrGpGpuMidBatchPreempt : 1;         // Enable GP GPU Mid batch/Command level preemption and resubmission mechanism (IVB+).
        unsigned int FtrGpGpuThreadGroupLevelPreempt : 1; // Enable GP GPU Thread Group Level preemption (IVB+)
        unsigned int FtrGpGpuMidThreadLevelPreempt : 1;   // Enable GP GPU Thread Level preemption (HSW+) - NOTE: FtrGpGpuMidBatchPreempt must also be set for this feature to work
        unsigned int Ftr3dMidBatchPreempt : 1;            // Enable 3D Mid batch preemption and resubmission mechanism (HSW+)
        unsigned int Ftr3dObjectLevelPreempt : 1;         // Enable 3D Object level preemption
        unsigned int FtrMediaMidBatchPreempt : 1;         // Enable Media Mid batch preemption
        unsigned int FtrMediaThreadGroupLevelPreempt : 1; // Enable Media Thread Group Level preemption (CNL+)
        unsigned int FtrMediaMidThreadLevelPreempt : 1;   // Enable Media Thread Level preemption (Not a POR for CNL)
        unsigned int FtrPerCtxtPreemptionGranularityControl : 1; // Ftr to enable preemption granularity control via MMIOs that are part of ctxt image
        unsigned int FtrDisableWDDMPreempt : 1;                  // Ftr to disable Preemption caps for driver (Win8 +)
        unsigned int FtrWalkerMTP : 1;                           // Ftr to control WMPT (Xe2+)

        unsigned int FtrBigPage : 1;             // Large pages for media encode
        unsigned int FtrPPGTT : 1;               // Per-Process GTT
        unsigned int FtrIA32eGfxPTEs : 1;        // GTT/PPGTT's use 64-bit IA-32e PTE format.
        unsigned int FtrMemTypeMocsDeferPAT : 1; // Pre-Gen12 MOCS can defers to PAT,  e.g. eLLC Target Cache for MOCS
        unsigned int FtrPml4Support : 1;         // PML4-based gfx page tables are supported (in addition to PD-based tables).
        unsigned int FtrPml3OnHwPml4Support : 1; // LKF PPGTT VA space is reduced to 36bits but h/w still use 4 Level Walk.
        unsigned int FtrSVM : 1; // Shared Virtual Memory (i.e. support for SVM buffers which can be accessed by both the CPU and GPU at numerically equivalent addresses.)
        unsigned int
                     FtrUSM : 1; // OneAPI feature Unified Shared Memory (i.e. support for portable kernels across devices/host in parallel via unified virtual address & shared allocations)
        unsigned int FtrTileMappedResource : 1;               // Tiled Resource support aka Sparse Textures.
        unsigned int FtrTranslationTable : 1;                 // Translation Table support for Tiled Resources.
        unsigned int FtrUserModeTranslationTable : 1;         // User mode managed Translation Table support for Tiled Resources.
        unsigned int FtrNullPages : 1;                        // Support for PTE-based Null pages for Sparse/Tiled Resources).
        unsigned int FtrL3IACoherency : 1;                    // Graphics L3 coherency with IA is supported.
        unsigned int FtrMIUpdateGTTCanUpdatePPGTT : 1;        // MI_UPDATE_GTT can update PPGTT - new feature added from IVB+
        unsigned int FtrReportCombinedDVMSSVM : 1;            // Combine DVM and SVM for Win7
        unsigned int FtrRemoteFx : 1;                         // Enable 1.5GB dedicated video memory. RCR 1023713
        unsigned int FtrDriverManagedL3ParityErrors : 1;      // Driver manages L3 parity errors since not ECC ( This Flag is no longer used in new Platforms ).
        unsigned int FtrL3HangOnParityError : 1;              // Enable HW hanging on L3 parity error
        unsigned int FtrEDram : 1;                            // embedded DRAM enable
        unsigned int FtrL4Cache : 1;                          // L4 cache support
        unsigned int FtrLLCBypass : 1;                        // Partial tunneling of UC memory traffic via CCF (LLC Bypass)
        unsigned int FtrCrystalwell : 1;                      // Crystalwell Sku
        unsigned int FtrCentralCachePolicy : 1;               // Centralized Cache Policy  /*This Flag is no longer used in new Platforms*/
        unsigned int FtrIoMmu : 1;                            // IOMMU exists on platform
        unsigned int FtrDriverControlledIoMmu : 1;            // Driver controlling IOMMU
        unsigned int FtrIoMmuPageFaulting : 1;                // IOMMU Page Faulting Support
        unsigned int FtrDmaBufferMemSpaceSplitting : 1;       // DMA buffer is in global memory space, and indirect heap is paged to per-process memory space
        unsigned int FtrSecurePPGTTUpdate : 1;                // Segment providing mapping to PPGTT is in Global GTT space ( This Flag is no longer used in new Platforms )
        unsigned int FtrPigms : 1;                            // Process-Isolated Gfx Memory Spaces
        unsigned int FtrWddm2GpuMmu : 1;                      // WDDMv2 GpuMmu Model (Set in platform SKU files, but disabled by GMM as appropriate for given system.)
        unsigned int FtrWddm2Svm : 1;                         // WDDMv2 SVM Model (Set in platform SKU files, but disabled by GMM as appropriate for given system.)
        unsigned int FtrStandardMipTailFormat : 1;            // Dx Standard MipTail Format for TileYf/Ys
        unsigned int FtrDisplayColorEnhancement : 1;          // Asus Display color enhancement support
        unsigned int FtrWddm2_1_64kbPages : 1;                // WDDMv2.1 64KB page support
        unsigned int FtrWddm2_2_2MBPages : 1;                 // WDDMv2.2 2MB page Support
        unsigned int FtrGttCacheInvalidation : 1;             // GTT cache invalidation support
        unsigned int FtrDynamicDisplayAliasing : 1;           // Enable Dynamic Display Aliasing for Displayable surfaces in  GlobalGTTHeap
        unsigned int FtrE2ECompression : 1;                   // E2E Compression ie Aux Table support
        unsigned int FtrForceGlobalE2ECompState : 1;          // Global Compression
        unsigned int FtrLinearCCS : 1;                        // Linear Aux surface is supported
        unsigned int FtrCopyEngineCompressionSupport : 1;     // Copy Engine's compression, resolve and fast clear feature
        unsigned int FtrEnableLegacyBltMOCS : 1;              // MOCS for Legacy Blitter commands
        unsigned int FtrFP16SurfaceRenderDecompression : 1;   // Support FP16 surface in render/display decompression
        unsigned int FtrLocalMemory : 1;                      // HBM local memory present
        unsigned int FtrTemp2020AprUMACacheCoherent : 1;      // UMA coherent - auto snoop vs costly snoop of LLC (Cpu-caches)
        unsigned int FtrPpgtt64KBWalkOptimization : 1;        // XeHP_SDV+ 64KB Page table walk optimization on PPGTT.
        unsigned int FtrPTEPageSize64 : 1;                    // XeHP_SDV(B0)/DG2+ 64KB page support in PTE (as 16x4KB - allow sys/lmem mixing)
        unsigned int FtrDiscrete : 1;                         // Discrete-gfx
        unsigned int FtrTileY : 1;                            // Legacy TileY feature to differeniate between TileY/Yf/Ys(legacy) and Tile4/Tile64(XeHP_SDV/Gen14LP+)
        unsigned int FtrXe2PlusTiling : 1;                    // Tile64 MSAA Layout Change for Physical L3 and 256B RCC
        unsigned int FtrFlatPhysCCS : 1;                      // XeHP_SDV compression ie flat physical CCS
        unsigned int FtrXe2Compression : 1;                   // Wave 2.5 and above, stateless compression
        unsigned int FtrControlSurfCmdAvailable : 1;          // XeHP_SDV compression CCSCopy cmd- remove when Blitter ready
        unsigned int Ftr2LmDism : 1;                          // 2LM for Display Stolen Memory on TGL-LP, H and S Skus
        unsigned int FtrMultiTileArch : 1;                    // 4x XeHP_SDV, mulitple GPU instances on single PCIe card exposed as single device
        unsigned int FtrLocalMemoryAllows4KB : 1;             // DG1-only allows 4KB LMEM page access.
        unsigned int FtrDisplayXTiling : 1;                   // Fallback to Legacy TileX Display, used for Pre-SI platforms.
        unsigned int FtrFastCopyWith3DOperation : 1;          // TGLLP+ BLOCK_COPY_BLT, FAST_COLOR_BLT with support for 3D gfx resources
        unsigned int FtrUnified3DMediaCompressionFormats : 1; // DG2+ has unified Render/media compression IP blocks(versus TGLLP/XeHP_SDV 's multiple instances) and requires
                                                              // changes to RC format h/w encodings.
        unsigned int FtrDisplayPageTables : 1;                // Display Page Tables: 2-Level Page walk for Displayable Frame buffers in GGTT.
        unsigned int Ftr57bGPUAddressing : 1;                 // 57b GPUVA support eg PVC, Xe3+
        unsigned int FtrUnifiedCompression43Ratio : 1;        // Enable 4:3 ratio for Unified Compression on DG2+
        unsigned int FtrOsManagedGlobalGtt : 1;   // Reports Global GTT segments to OS, so that build paging buffer updates the Global GTT directly and bypass GmmHandleAliasing()
        unsigned int FtrCameraCaptureCaching : 1; // Allow GPU's LLC caching on IPU buffers
        unsigned int FtrLimitedLMemBar : 1;       // Flag to control Small LMem BAR ( CPU Visible and Non Cpu Visible) code
        unsigned int FtrBLTSaveRestore : 1;       // Enable BLT DMA to save/restore during Power transitions (restore not enabled yet)
        unsigned int FtrGpuPageTableUpdates : 1;  // Gpu update of Page Table entries
        unsigned int FtrPml5Support : 1;          // ELG+ 5-level page tables hw support
        unsigned int FtrUMA : 1;                  // Integrated with Memory controller ( i.e. opposite of Discrete) - Used by UMD's(like dx12) to report gfx api caps to runtime
        unsigned int FtrCacheCoherentUMA : 1;     // UMA that automatically snoops CPU caches—i.e. no benefit/ability for non-coherent memory access.
        unsigned int FtrKmdManagedDPTAllocation : 1; // 1: KMD manages DPT pages allocation; 0: OS manages DPT pages allocation
        unsigned int FtrPoolAllocRecycler : 1;       // enable allocation-recycling via GmmLib2 interface

        unsigned int FtrKMDTestSupportFromRegKey : 1;        // Enable KMD testing support from registry keys.
        unsigned int FtrKmdDaf : 1;                          // KMD:DAF/Aubcapture (Enabled via regkey--never via xxx_sku.c)
        unsigned int FtrDisableOverlayRotation : 1;          // Disable overlay rotation when value is 1
        unsigned int FtrUnmapPagingReservedGTTSeg : 1;       // Enables ring buffer initiated unmapping of GTT's paging reserved segment
        unsigned int FtrKmdNotifyUmd : 1;                    // Enables KMD -> UMD notification instead of Spinloop/Sleep in UMD.
        unsigned int FtrDeferredWaitForEventOnAsyncFlip : 1; // Enables Deferred waits for workloads that do not render to a render target
        unsigned int FtrPerfModeSdiWrite : 1;                // Enabled performance mode ( long range ) STORE_DATA_IMM write capability
        unsigned int FtrUse3DEngineforLateralBlts : 1;       // Exposes 3D engine for lateral blt submissions. Otherwise only 2D engine is used. (BDW+)
        unsigned int FtrPreemptTestMode : 1;                 // Preemption Test mode is used to force preemption requests without OS interactions
        unsigned int FtrGuCWriteCombineEnable : 1;           // Feature to enable Write Combine in GuC SHIM (CNL+)
        unsigned int FtrGuCInternalMsgChannelEnable : 1;     // Feature to enable Internal Msg Channel in CNL+. MMIO reads / writes handled internally and donot appear on MSGCH.

        unsigned int FtrSubSliceIzHashing : 1;           // Sub-slice hashing change for Die Recovery with single EU disabled
        unsigned int FtrFrameBufferLLC : 1;              // Displayable Frame buffers cached in LLC
        unsigned int FtrGpuMmuPageFault : 1;             // To enable Page faults on WDDM2.0 GpuMmu.
        unsigned int FtrDriverFLR : 1;                   // Enable Function Level Reset (Gen11+)
        unsigned int FtrOSManagedAllocations : 1;        // use OS managed allocations instead of GMM allocations WDDM2.0+.
        unsigned int FtrCsResponseEventOptimization : 1; // Enable render response events via 0x44050 only when needed
        unsigned int FtrRuntimeLogBuffer : 1;            // Enable/Disable runtime log buffer feature
        unsigned int FtrWatchdogTimerEnabledByUMD : 1;   // Wachtdog timer is enabled by UMD in the BB; CNL+
        unsigned int FtrContextBasedScheduling : 1;      // GEN11 Media Scalability 2.0: context based scheduling
        unsigned int FtrSfcScalability : 1;              //  Media Scalability 2.0: sfc scalability support
        unsigned int FtrVeboxScalabilitywith4K : 1;      //  Media Scalability 2.0: vebox scalability support
        unsigned int FtrWithSlimVdbox : 1;               //  Has slim vdbox on the platform
        unsigned int FtrHwScheduling : 1;                // WDDM2.5+ MS Stage 1 HW scheduling support
        unsigned int FtrSwAssistedOCA : 1;               // S/W Assisted OCA
        unsigned int
                     FtrLRMLiteRestore : 1; // LRM based lite restore, applicable for all platforms from SKL+, Perf regression HSD: https://hsdes.intel.com/appstore/article/#/1808514600
        unsigned int FtrCrossAdapterResourceTexture : 1; // Cross adapter resource texture. support from WDDM3.0. UMD and KMD use this ftr to report Vidmm cap's
        unsigned int FtrCrossAdapterResourceScanout : 1; // Cross adapter scan out support from WDDM3.0. UMD and KMD use this ftr to report Vidmm cap's
        unsigned int FtrVfLogging : 1;                   // To enable Vf Logging

        unsigned int FtrEnableKmdPerf : 1;
        unsigned int FtrUtilizeMemDimondLane : 1;
        unsigned int FtrNewEncodingForSAMediaWOPCM : 1;   // Additional WOPCM size encodings to support GSC virtualization for XE2
        unsigned int FtrReserveADMXbarHashGuardBand : 1;  // Enable reserving Unusable memory region allocation due to Bdie XBAR.
        unsigned int FtrXe2HiZPlaneCompression : 1;       // Flag to indicate the HiZplane compression in Xe2
        unsigned int FtrKmdPresentCompressionSupport : 1; // Flag for UMDs to control resolving the surface

        unsigned int FtrVtdErrorCursor64K : 1; // To prevent false VT-d type 6 errors, use 64KB address alignment and allocate an extra
                                               // 2 Page Table Entries (PTEs) beyond the end of the displayed surface
        unsigned int FtrOptimizedGTTInit : 1;  // Flag to Optimize Initialization of GGTT/PPGTT in local memory, feature tied to Ftr Discrete

        unsigned int FtrVirtualTileScalabilityDisable : 1; // Flag for media to disable virtual tile scalability

#if (_DEBUG || _RELEASE_INTERNAL)
        unsigned int FtrLoadGucFwFromFile : 1;             // Load GuC FW from %SystemRoot%\gucfw.bin
        unsigned int FtrDisable3DSubmissions : 1;          // 3D node is exposed to OS but not 3D submissions are supported.
        unsigned int FtrWhitelistTdCtl : 1;                // Needed for UMD shader debug
#else
        unsigned int ReservedBitB : 1;
        unsigned int ReservedBitC : 1;
        unsigned int ReservedBitE : 1;
#endif // (_DEBUG || _RELEASE_INTERNAL)
    };

    struct //_sku_2d
    {
        unsigned int FtrImmText128 : 1; // Imm text size only 128 byte
    };

    struct //_sku_DD
    {
        unsigned int FtrSecondSprite : 1;      // Second Sprite (Display C)
        unsigned int FtrOvl3LineBuffer : 1;    // Three line buffer for overlay
        unsigned int FtrRGBOverlay : 1;        // RGB Overlay
        unsigned int FtrOneLineMode : 1;       // One Line Mode
        unsigned int FtrAsyncFlipOnPlaneB : 1; // Async Flip on Plane B
        unsigned int FtrDiscardAlpha : 1;      // Discard Alpha
        unsigned int FtrOvlDownScale : 1;      // Overlay down scale beyound 2:1
        unsigned int FtrPlanarToPacked : 1;    // PlanarToPacked Blt
        unsigned int FtrTwoSprites : 1;        // 2 sprites, one on pipe A, one on pipe B
        unsigned int FtrSprites17Gamma : 1;    // For ILK+ there is a new gamma with 17 reference points
        unsigned int FtrMELockableSprite : 1;  // For ILK+, ME can lock sprite for its own use
        unsigned int FtrOverlaySynch : 1;      // For CTG+ we implement overlay synchronization
    };

    struct //_sku_3d
    {
        unsigned int FtrHwBin : 1;                                       // Hw binner
        unsigned int Ftr8BitPalette : 1;                                 // 8bit index color texture
        unsigned int FtrPixelShader : 1;                                 // Pixel shader
        unsigned int FtrPixelShader30 : 1;                               // Pixel shader 3.0
        unsigned int FtrBWGConsumerTextures : 1;                         // Enable new texture formats for BW-G 14.21 consumer skus
        unsigned int FtrMultiRenderTarget : 1;                           // Multiple Render Targets (Gen4)
        unsigned int FtrHWTnL : 1;                                       // HW T&L (Gen4)
        unsigned int FtrOcclusionQuery : 1;                              // Occlusion Query (Gen4 D3D)
        unsigned int FtrOcclusionQueryOGL : 1;                           // Occlusion Query (Gen4 OGL)
        unsigned int FtrAutoGenMipMap : 1;                               // Auto MipMap Generation (Gen4 D3D)
        unsigned int FtrDX10Support : 1;                                 // DX10 driver enumeration
        unsigned int FtrDX10_1Support : 1;                               // DX10.1 driver enumeration
        unsigned int FtrDX11_Xon10Support : 1;                           // DX11on10 driver enumeration
        unsigned int FtrDX11Support : 1;                                 // DX11 driver enumeration
        unsigned int FtrDX11_1Support : 1;                               // DX11.1 driver enumeration
        unsigned int FtrWorkstation : 1;                                 // Workstation Direct3D
        unsigned int FtrEtcFormats : 1;                                  // ETC formats support
        unsigned int FtrAstcLdr2D : 1;                                   // ASTC 2D LDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrAstcHdr2D : 1;                                   // ASTC 2D HDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrAstc3D : 1;                                      // ASTC 3D LDR/HDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrUmdThreadingShim : 1;                            // Enable multithreaded UMD.
        unsigned int FtrBoundingBoxOptOGL : 1;                           // Enable bounding box Optimization in OpenGL
        unsigned int FtrResourceStreamerEnabled : 1;                     // Resource Streamer Support (For 3D UMD use only)
        unsigned int FtrHiZSamplerDisabled : 1;                          // HiZ Sampling capability
        unsigned int FtrDisableDX10IdleGpuFlushOnPresi : 1;              // DX10 UMD trigger to disable IdleGpuFlush optimization only when running on pre-si platforms
        unsigned int FtrE2ECompressionOnGen11 : 1;                       // SKU check for E2EC feature for LKF
        unsigned int FtrEnableHardwareFilteringOfSemiPipelinedState : 1; // Windower hardware will filter all semi-pipelined states except for hiz-op if unchanged changedfrom the
                                                                         // current state (Gen11 B0+)
        unsigned int FtrEfficientCombiningOfSubspans : 1;                // Enables efficient combining of subspans in daprsc. combined if subspans fall in same RCC CL (Gen11 B0+)
        unsigned int FtrIsCCSAllowedWithoutMSAAComp : 1; // Sampling from CCS is allowed without MCS : DG1, XeHP_SDV DCN : https://hsdes.intel.com/appstore/article/#/1408321355
        unsigned int FtrRangedFlush : 1;                 // Range based flush
        unsigned int FtrURBReconfigure : 1;              // Reconfigure URB allocation for tess heavy RP, TGLLP B0 DCN : https://hsdes.intel.com/resource/1408411110
        unsigned int
                     FtrHWManagedZClearValue : 1; // Sampler to use depth clear value stored in memory : XeHP_SDV B stepping & DG2 DCN : https://hsdes.intel.com/appstore/article/#/1209977576
        unsigned int FtrHSPatchCountThreshold : 1;               // TGLLP B0 DCN : https://hsdes.intel.com/appstore/article/#/2206999503
        unsigned int FtrPartialDepthResolveSupport : 1;          // Partial depth resolve support
        unsigned int FtrTBIMR : 1;                               // TBIMR
        unsigned int FtrRayTracing : 1;                          // Ray Tracing
        unsigned int FtrEnhancedL3Control : 1;                   // Enhanced L3 Control
        unsigned int FtrVariableRateShading : 1;                 // Variable Rate Shading
        unsigned int FtrMeshShading : 1;                         // Mesh Shading
        unsigned int FtrLowQualityFilterAllowed : 1;             // Flag to allow/disallow Low Quality Filter
        unsigned int Ftr1MbGPUVAAlignment : 1;                   // GPU VA 1Mb Alignment
        unsigned int FtrAllowSIMD32ForCPSWithCPSize1x1 : 1;      // Allow Simd32 PS kernels with CPS for Coarse rate 1x1
        unsigned int FtrAtomicInt64OnDescriptorHeapResource : 1; // Shader capability enabled starting from DG2+
        unsigned int FtrMeshShaderWritingShadingRate : 1;        // Mesh Shader writing SV_ShadingRate - Supported from DG2 B0+
        unsigned int FtrFramePacing : 1;                         // Frame Pacing
        unsigned int FtrNativeDX9 : 1;                           // Set when Native DX9 is enabled. If unset, we have DX9on12
        unsigned int FtrExecuteIndirectHwLoopUnroll : 1;         // HW capability to unroll Execute Indirect loops. DCN: https://hsdes.intel.com/appstore/article/#/14015171903
        unsigned int FtrGameCompatibilityProfiles : 1;           // Game Compatibility Profiles
    };

    struct //_sku_IGC
    {
        unsigned int FTrEnableAIParameterCombiningWithLODBias : 1; // IGC feature: Enable API parameter to combine with LOD bias; [XeHP_SDV,DG2]
                                                                   // https://hsdes.intel.com/appstore/article/#/1406916861
        unsigned int FtrDPASSupported : 1;                         // To expose DX12 UMD caps on platforms where WaveMMA is supported using systoplic / dpas path
        unsigned int FtrReadSuppressionDisable : 1;                // EU optmization that is turned off on some platforms due to unfixable bugs
        unsigned int FtrAdvancedTextureOpsSupported : 1;
        unsigned int FtrWriteableMSAATexturesSupported : 1;
    };

    struct //_sku_PwrMgmt
    {
        unsigned int FtrPM : 1; // Pwr Mgmt Capabilites
        unsigned int FtrD1 : 1; // D1 state
    };

    struct //_sku_PwrCons
    {
        // Global Power Conservation Support Flag
        unsigned int FtrPwrCons : 1;           // Is Power Conservation Supported
        unsigned int FtrPwrConsStaticOnly : 1; // Flag to indicate features that are enabled but which doesn't need a event infrastructure or dynamic controlling

        // CxSR
        unsigned int FtrCxSR : 1;                          // C-State Self-Refresh
        unsigned int FtrCxSRSpriteWatermarksSupported : 1; // CxSR Sprite Watermarks support
        unsigned int FtrCxSRLp3WatermarksSupported : 1;    // CxSR LP3 Watermarks support
        unsigned int FtrCxSRWmLpMemoryLevelSupport : 1;    // WM_LPx latency field programming support

        // FBC
        unsigned int FtrFbc : 1; // Frame Buffer Compression
        unsigned int
                     FtrFbc2AddressTranslation : 1; // This bit indicates whether the platform needs the FBC-2 Address Translation Register usage.  This is used starting with IronLake.
        unsigned int FtrFbcBlitterTracking : 1;     // FBC support for blitter tracking.
        unsigned int FtrFbcWatermarkSupport : 1; // FBC watermark support enabling
        unsigned int FtrFbcCpuTracking : 1;      // FBC support for CPU tracking
        unsigned int FtrFbcInMultiDisplay : 1;   // FBC support for multi display configurations
        unsigned int FtrFbcDualPipe : 1;         // FBC support for PIPE B
        unsigned int FtrFbcPsr2Coexistence : 1;  // FBC with PSR/PSR2/Panel replay

        // DPS Features
        unsigned int FtrDps : 1;                                 // Display P-States (DPS)
        unsigned int FtrSupportCuiDrrsFeature : 1;               // Indicates whether the platform supports the CUI-driven Static DRRS feature
        unsigned int FtrEnableDpsForMIPI : 1;                    // Indicates enable/disable of MIPI DPS feature
        unsigned int FtrDisablePixelClockBasedDpsOnMultiEdp : 1; // Indicates no pixel clock based DPS support on multi Edp starting from Alderlake-P
        unsigned int FtrInternalDisplayDmrrs : 1;                // DMRRS for internal display

        // DPST
        unsigned int FtrDpst : 1;                             // Display Power Savings Technology (DPST)
        unsigned int FtrDpstEnginePerPipe : 1;                // Separate DPST engine supported on each pipe
        unsigned int FtrDpstHistogramBinClamping : 1;         // DPST histogram bin clamping support to enable resolutions upto 8MPixels
        unsigned int FtrDpstAfterPipeScaler : 1;              // DPST hardware lies after panel fitter on HSW platforms
        unsigned int FtrDpst7_x_Support : 1;                  // DPST7.0+ Algo Support from Gen13+
        unsigned int FtrTconBacklightOptimizationSupport : 1; // Control the support for TCON Backlight Optimization Features like CABC/ELP
        unsigned int FtrSourceSideDitheringSupported : 1;     // To enable or disable Dithering from VBT.
        unsigned int FtrElpSupport : 1;                       // Support for ELP Feature
        unsigned int FtrFullScreenSolidColorSupport : 1;      // Full Screen Solid Color feature
        unsigned int FtrOpst_1_1_Support : 1;                 // OPST 1.1 Algo support from RPL-P+.

        // GHE
        unsigned int FtrGhe : 1; // Global Histogram Enhancement (GHE)

        // LACE
        unsigned int FtrDisplayLace : 1;                 // Local Area Contrast Enhancement (LACE)
        unsigned int FtrLaceOnPipeB : 1;                 // Indicates if LACE feature is supported on PipeB.
        unsigned int FtrDisplayLacePhaseIn : 1;          // Display LACE Phase-in
        unsigned int FtrFlatModeSupported : 1;           // Indicates if Flat mode is supported by platform.
        unsigned int FtrFastLaceModeSupported : 1;       // Indicates if Fast Lace mode is supported.
        unsigned int FtrDisplayLaceTriggerSupported : 1; // Display LACE Trigger supported features, Aggr Mode & Ambient Light Mode (Gen 13+)

        // Backlight Control
        unsigned int FtrBlc : 1;                               // Backlight Control (BLC)
        unsigned int FtrBlcDxgkDdi : 1;                        // Vista Backlight Control DxgkDdi interface
        unsigned int FtrDynamicPWMFreqMinBrightness : 1;       // Dynamic PWM frequency and minimum brightness support
        unsigned int FtrBlcPerPipe : 1;                        // Separate backlight control supported on each pipe
        unsigned int FtrBlcSmoothTransition : 1;               // Support for BLC smooth brightness control on Windows 8+
        unsigned int FtrBlcFlexiblePWMGranularity : 1;         // Support flexible PWM granularity
        unsigned int FtrBlcAssertiveDisplay : 1;               // Assertive Display Support
        unsigned int FtrBlcBIOSNotification : 1;               // Send BIOS SCI notification on driver backlight adjustments
        unsigned int FtrBlcPwmFreqCdClkDependent : 1;          // PWM frequency is based on CDCLK
        unsigned int FtrDisableBrightness3DdiSupport : 1;      // Disable Brightness3 support from registry
        unsigned int FtrIndependentBrightnessControl : 1;      // Brightness control on secondary display using App.
        unsigned int FtrAcpiBrightnessControlPortOverride : 1; // Flag to be enabled through hidden regkey for getting port details to notify ACPI for brightness control

        // Event Handling
        unsigned int FtrLhdmDxvaNotifications : 1;      // Service DxVA notification in LHDM
        unsigned int FtrTrackDPC : 1;                   // Track dropped interrupt DPC's
        unsigned int FtrMonitorPowerDown : 1;           // Indicates whether we should turn off PC features when Monitor powers down
        unsigned int FtrAdaptiveVBIDynamicRRChange : 1; // Dynamic Refresh Change Change when Adpative VBI is used.
        unsigned int FtrMediaWorkloadDetection : 1;     // PC subsystem for detecting active media playback

        // General
        unsigned int FtrDppe : 1;       // Indicates whether or not we should register to get notifications from the OS DPPE control panel (also affects the Turbo feature)
        unsigned int FtrFlrRecover : 1; // Handle First Level Reset Recover
        unsigned int FtrLPSP : 1;       // Support Low Power Single Pipe Sku
        unsigned int FtrVEBOX : 1;      // Support Video Enhancement Pipe
        unsigned int FtrSWCapULP : 1;   // Support for IVB 8 watt SKU detection

        // ***
        // !!! The FtrForceWake MUST be managed for all platforms starting with GT EVEN IF Power Conservation is not enabled or initiated !!! ***
        unsigned int FtrForceWake : 1;          // Indicates platforms that require the Force Wake handling on render registers read
        unsigned int FtrForceWakeMMIOWrite : 1; // Indicates platforms that require the Force Wake handling on render registers write
        unsigned int FtrDecoupledMMIO : 1;      // Indicates platforms that support decoupled MMIO handling
                                                // This feature is no longer used. drv functionality related this ftr cleaned up in below gerrit
                                                // https://gerrit-gfx.intel.com/1028177
        // ***

        unsigned int FtrMediaTurboMode : 1; // Media Turbo Mode support

        // Render Geyserville RP State Switching Features
        unsigned int FtrGsvTurbo : 1;                    // Turbo frequency scaling
        unsigned int FtrGsvDynamicOverclocking : 1;      // Indicates whether or not dynamic overclocking can occur.
        unsigned int FtrGsvRingFreqScaling : 1;          // Indicates whether IA ring scaling is supported.
        unsigned int FtrGsvConfigTdp : 1;                // Determine IA-P1 freq based on TDP configuration.
        unsigned int FtrGsvCrl : 1;                      // CPU/ring power limiter.
        unsigned int FtrGsvCrlRingControl : 1;           // Indicates if CRL will control ring frequency as well (and not only CPU freq)
        unsigned int FtrGsvIntelligentBiasControl : 1;   // Intelligent Bias Control. Current implementation requires CRL. FtrGsvCrl must be set in prior to set this flag.
        unsigned int FtrGsvScenarioBasedBiasControl : 1; // Scenario Based Bias Control, different power policy for Fullscreen 3D and regular desktop
        unsigned int FtrGsvEfficientMinFreq : 1;         // Clamp Min GT to efficent Freq
        unsigned int FtrWeightsProgrammedByDriver : 1;   // Indictes whether driver program the weights
        unsigned int FtrGsvBurstWorkloadTurbo : 1;       // Burst workload turbo algorithm
        unsigned int FtrGsvSliceUnsliceThrottle : 1;     // Slice unslice freuqnecy throttling
        unsigned int FtrGsvOclBoost : 1;                 // Set RP0 GT frequecy for ocl workloads
        unsigned int FtrGsvMdfBoost : 1;                 // Set RP0 GT frequecy for Mdf workloads
        unsigned int FtrGsvDxComputeBoost : 1;           // Set RP0 GT frequecy for DX compute workloads
        unsigned int FtrGsvAdaptiveTurbo : 1;            // Adaptive burst turbo
        unsigned int FtrAsyncMMIOTurbo : 1;              // Adaptive burst turbo
        unsigned int FtrCommandThrottlePolicy : 1;       // Set RP0 GT frequency for specific WLs shared between dGPU and iGPU so that iGPU is not a bottleneck
        unsigned int FtrIAFreqCapping : 1;               // Enable IFL (IA frequency Limiting) in GUC based on CPU/GPU boundedness of the WL
        unsigned int FtrTurboV2 : 1;                     // Enable Turbo V2 on supported platform
        unsigned int FtrDptf : 1;                        // Dptf interface implementation for DG1

        // XTU interface - Overclocking and Fan control
        unsigned int FtrXTU : 1;             // XTU interface support which enabled overclocking and fan control for discrete platforms
        unsigned int FtrXTUOverClocking : 1; // Overclocking feature exposed by XTU interface for Discrete platforms
        unsigned int FtrXTUFanControl : 1;   // Fan control feature exposed by XTU interface for Discrete platforms

        // Render Geyserville Sleep State Features
        unsigned int FtrRS : 1;                              // Render Standby
        unsigned int FtrRsLowerRc6PromotionTimeForMedia : 1; // Lower Promotion Time for Media
        unsigned int FtrRsCoarsePowerGating : 1;             // Support individual media/render power gating
        unsigned int FtrRsMediaSubEngineForceWake : 1;
        unsigned int FtrRsMediaSamplerPowerGating : 1;
        unsigned int FtrRsMediaSubpipePowerGating : 1; // Support MFX/HCP within VDbox power gating

        unsigned int FtrSysman : 1; // Sysman Interface

        // Slice Shutdown
        unsigned int FtrSliceShutdown : 1; // For PreGen9, Support shutting down a GT Slice dynamically on media workload for power saving.

        // Slice/Sub-Slice Shutdown/EU Power gating support
        unsigned int FtrSSEUPowerGating : 1;             // For SKL+, Support shutting down a Slice/Sub-slice/EU power gating dynamically.
        unsigned int FtrSSEUPowerGatingControlByUMD : 1; // Support SSEU power gating control by UMD.

        // Panel Self Refresh
        unsigned int FtrPsr : 1;                     // PSR Support
        unsigned int FtrPsrSfu : 1;                  // Single Frame Update for PSR
        unsigned int FtrPsrSu : 1;                   // Selective Update for PSR
        unsigned int FtrPsrPowerDownLcpll : 1;       // Turn off LCPLL in PSR mode
        unsigned int FtrPsrInMultiDisplay : 1;       // PSR Support in Multi Display
        unsigned int FtrPsr2DrrsCoexistence : 1;     // PSR2 and DRRS coexistence (LRR)
        unsigned int FtrVTotalBasedLrrSupport : 1;   // 1: PSR2 + SW Vblank adjustment for VRR panels during LRR/DMRRS, 0: HW Vblank adjustment for VRR panels
        unsigned int FtrPsrSuSupportOnDualPipe : 1;  // Support for PSR2 on second display
        unsigned int FtrPsrSuSdpTransLineConfig : 1; // Support for PSR2 SDP Transmission Line Configuration
        unsigned int FtrLrrDynamicDpcdSupport : 1;
        unsigned int FtrSfsuDpstHandling : 1;
        unsigned int FtrNoEarlyFrameCaptureIndicationSupport : 1; // Support for no early frame capture indication

        // FPS Tracking / DFPS
        unsigned int FtrFpsTracking : 1; // FPS tracking functionality
        unsigned int FtrDfps : 1;        // Frame Rate Control
        unsigned int FtrPvqc : 1;        // Adaptive Rendering Control (a.k.a PVQC)

        // Capped FPS
        unsigned int FtrCappedFps : 1; // Refresh Rate Capped FPS

        // DCC
        unsigned int FtrDcc : 1; // Duty Cycle Control
        unsigned int FtrDct : 1; // Duty Cycle Throttling

        // Valleyview specific turbo changes
        unsigned int FtrGsvTurboVLV : 1; // Valleyview turbo changes

        unsigned int FtrIps : 1; // Intermediate Pixel Storage feature

        unsigned int FtrWriteMCHRegsViaPcu : 1; // Write MCHBAR registers through the PCU if they are R/O through MMIO

        // Single-loop power management
        unsigned int FtrSLPM : 1; // Single-loop power management (primary switch)

        // Real-Time Command Queue support for RS2 to boost the GT frequency to MAX for Real time workload
        unsigned int FtrRealTimeWLBoost : 1;

        // Dynamic Frequency Rebalancing - aims to reduce Sampler power by dynamically changing its clock frequency in low-throughput conditions
        unsigned int FtrSamplerDFR : 1;

        // GuC based dynamic RC management
        unsigned int FtrGUCRC : 1; // If FtrRS is enabled, this indicates if GUCRC should be activated.

        // EDR mode power optimization
        unsigned int FtrEDRTurboMode : 1;

        // Ftr Flag to disable DC-States
        unsigned int FtrDcStates : 1;

        // Ftr Flag to disable Powerwell when only Virtual display is enabled
        unsigned int FtrDisplayPowerwell : 1;
    };

    struct //_sku_SwBios
    {
        unsigned int FtrScalerForBothPipes : 1;           // Scaler can be configured for both pipes
        unsigned int FtrSDVOPowerDown : 1;                // SDVO Power Down
        unsigned int FtrIntHDCPEnable : 1;                // Integrated HDCP
        unsigned int FtrIntHDMIEnable : 1;                // Integrate HDMI
        unsigned int FtrMultiHdcpCipher : 1;              // Multi Cipher
        unsigned int FtrMultiHdmiDIPEncoders : 1;         // Multi Cipher
        unsigned int FtrPF2Available : 1;                 // PF2 Available
        unsigned int FtrIntDPEnable : 1;                  // Integrated display port
        unsigned int FtrPNMEnabled : 1;                   // Platform Noise Mitigation feature
        unsigned int FtrEmbeddedDPEnable : 1;             // Embedded Display Port
        unsigned int FtrXVYCCSupported : 1;               // XVYCC support
        unsigned int FtrGCPSupported : 1;                 // GCP packet transmission support
        unsigned int FtrSendDPInfoEnable : 1;             // Send ELD, SPD and AVI Informations for DP
        unsigned int FtrEELDSupport : 1;                  // EELD support
        unsigned int FtrESFVP : 1;                        // Exclusive Sprite Full Screen Video Playback (Supported ILK onwards)
        unsigned int FtrSDVODVIEnable : 1;                // Enable SDVO DVI
        unsigned int FtrEnumerateSingleHDMI : 1;          // Enumerate Single HDMI only
        unsigned int Ftr12BPCSupport : 1;                 // Enable 12BPC support
        unsigned int FtrHDMI10BPCSupport : 1;             // Enable 10 BPC support for HDMI 2.0
        unsigned int FtrEnableProjectorColorControl : 1;  // Enable Projector color control using Hue and Saturation.
        unsigned int FtrEnableAudioContentProtection : 1; // Enable audio content protection by reporting HBR SADs
        unsigned int FtrDisableEdpHdcp : 1;               // Disable HDCP for eDP port
        unsigned int FtrAltScrambler : 1;                 // Alternate Scrambler Support for eDP
        unsigned int FtrEnablePlaneTrickleFeed : 1;       // trickle feed bit per plane
        unsigned int FtrEnable5PlanesPerPipeICL : 1;      // this is set based on reg key. default disabled.
        unsigned int FtrSDVOTV : 1;                       // SDVO TV
        unsigned int FtrClkBendingSupported : 1;          // Support for clock bending for HDMI displays
        unsigned int FtrGamutExpansion : 1;               // Gamut Exapnsion Support
        unsigned int FtrSupportsWiderDisplayPipeLine : 1; // Supports Wider Display Pipeline
        unsigned int FtrNarrowGamut : 1;                  // Narrow Gamut Support
        unsigned int FtrDisableHigherPRModes : 1;         // Don't enumerate pixel repeat modes greater than 2 as CHV has a hardware limitation
        unsigned int FtrDisplayNV12 : 1;                  // Display NV12 format support
        unsigned int FtrDisplayYUY2 : 1;                  // Display YUY2 Scalingsupport
        unsigned int FtrDisplayYUY2Scaling : 1;           // Display YUY2 Scalingsupport
        unsigned int FtrDisplayNV12Scaling : 1;           // Display NV12 Scalingsupport
        unsigned int FtrDisplayP0xx : 1;                  // Display P0xx format support
        unsigned int FtrFlipImmediateOnHSync : 1;
        unsigned int FtrDelayForTypeCTBTDisplays : 1;          // Perform 750ms delay for TypeC/TBT Displays
        unsigned int Ftr2ConnectorFIA : 1;                     // only 2 ports per FIA module is supported versus the other option of 4 ports per FIA module
        unsigned int FtrAStepSupport : 1;                      // Flag for features supported for A Step only.
        unsigned int FtrGammaRegisterWriteUsingDsb : 1;        // Gamma register writes can be done using DSB Gen12+
        unsigned int FtrHdmiTmdsMaxDataRateSupportPerSpec : 1; // Indicate HW support for 340Mhz Max TMDS Char Rate for HDMI 1.4 and 600Mhz Max TMDS Char Rate for HDMI 2.0 as per
                                                               // HDMI Spec requirement.
        // Dp 1.2 related
        unsigned int FtrLinkTrainingBeforeGMCHSetTiming : 1; // DP Link training is done in the beginning of enable sequence
        unsigned int FtrTPS3Supported : 1;                   // DP Training Pattern 3 is support
        unsigned int FtrHBR2Supported : 1;                   // DP HBR2 Linkrate support
        unsigned int FtrEnableDPMST : 1;                     // DP Multi Stream Transport support
        unsigned int FtrReenableDpMstOnPrimaryDisable : 1;   // Reenable DP MST topology on Primary disable
        unsigned int FtrDynamicTUComputation : 1;            // Compute DP TU dynamically
        unsigned int FtrSinglePFOnly : 1;                    // CDV, VLV platforms
        unsigned int FtrPPSAttachedtoPipe : 1;               // VLV platforms where 2 per pipe PPS is present
        unsigned int FtrLoadHDCPKeys : 1;                    // HDCP keys needs to be loaded in VLV
        unsigned int FtrColorRangeClipByPort : 1;            // For VLV.Color Range clipping  to be done by port[HDMI/DP],instead of pipe.
        unsigned int FtrDPInterlacedModeRemoval : 1;         // For VLV we want removal of interlaced mode in case of DP.
                                                             // Also added a hidden reg key through which this flag can be enabled using INF
        // Dp 1.3 Related
        unsigned int FtrTPS4Supported : 1; // DP Training Pattern 4 support
        unsigned int FtrHBR3Supported : 1;
        unsigned int FtrDPYUV420PixelEncodingSupported : 1;

        // DP 2.0
        unsigned int Ftr128b132bSupported : 1;    // 128b/132b channel coding support
        unsigned int FtrUsb4DisplayReporting : 1; // Report Display over USB4 properties, Defined for Windows Cobalt and DP 2.0.

        // Work Item Based DP Detection Post Resume
        unsigned int FtrDelayedDpDetectionPostResume : 1;

        // eDP1.4 Related
        unsigned int FtrLowVswingSupport : 1; // for eDP1.4 lower vswing and pre-emphasis support
        unsigned int
                     FtrCHVEnableScalerForExternalDisplay : 1; // [VLV RCR-1024545 Porting on CHV] Enable the single scalar for External Panel when device config is LFP native clone
        unsigned int FtrLpDpSupport : 1;                       // Support for low power dual pipe
        unsigned int FtrEnableDC5DC6 : 1;
        unsigned int FtrEnableDC5 : 1;
        unsigned int FtrEnableDC6v : 1;
        unsigned int FtrEnableDC6 : 1;
        unsigned int FtrEnableDC9 : 1;
        unsigned int FtrDeepPkgC8 : 1;
        unsigned int FtrEnableDc6vLinkoff : 1;  // Linkoff b/w active frames for Dc6v Enhancements
        unsigned int FtrEnableIOUngatedDMC : 1; // WA for IO HW HSD: https://hsdes.intel.com/appstore/article/#/1304976242
        unsigned int FtrEnableDCStateinPSR : 1;
        unsigned int FtrVrrToDC6vTransition : 1;       // WA for ADL-P HW limitation for CMTG+VRR support
        unsigned int FtrRendComp : 1;                  // For Render Compression Feature on Gen9+
        unsigned int FtrClearColor : 1;                // For Clear Color Gen11.5+
        unsigned int FtrMediaComp : 1;                 // LKF+
        unsigned int FtrDisplayYTiling : 1;            // For Y Tile Feature on Gen9+
        unsigned int FtrDisplay4TilingSupport : 1;     // For Tile 4 Memory . From Gen13 onwards
        unsigned int FtrAlwaysEnableAllDBUFSlices : 1; // Enables DBUF_S1 and DBUF_S2 all the time on Gen11
        unsigned int FtrNNScalingSupport : 1;          // Nearest Neighbour Scaling Support available on Gen11+
        unsigned int FtrEnableDisplayableSupport : 1;  // Enable Displayable Support for "Present At" feature in Nickel OS
        // HDMI 2.0 LS-PCON specific
        unsigned int FtrEnableLsPcon : 1; // for HDMI2.0 support using LS-PCON
        unsigned int FtrDDIeEnabled : 1;  // enabling of DDI-E for DP->VGA on Skl Desktop systems
        // HDMI 2.0 specific
        unsigned int FtrNativeHDMI2_0Support : 1; // From GEMINILAKE onwards Native HDMI2.0 is supported
        unsigned int FtrDdiAEnabledasVGA : 1;     // Enabling eDP - DDI-A as VGA
        unsigned int FtrDdiAEnabledasDP : 1;      // Enabling eDP - DDI-A as DP
        // HDCP 2.2 specific
        unsigned int FtrNativeHDCP2_2Support : 1;
        unsigned int FtrKmdHdcp2Protocol : 1; // For HDCP KMD authentication on DashG
        // WIGIG Related
        unsigned int FtrEnableWGBoxWigig : 1; // Enable Wigig using WGBox
        // Display only Driver
        unsigned int FtrWinDoD : 1; // for Display only Driver support
        // HDR Feature related to HDMI2.0a
        unsigned int FtrEnableHDRSupport : 1;      // Enable HDR Feature
        unsigned int FtrEnableOSHDR : 1;           // Enable OS HDR.
        unsigned int FtrEnableEdpHDR : 1;          // Enable eDP HDR
        unsigned int FtrHdrFP16ScanoutSupport : 1; // Indicates capability of handling FP16/scRGB input and scanout with PQ/2084 encoding, BT2020 Colorspace to produce HDR10 Signal
        unsigned int FtrHdrARGB10ScanoutSupport : 1; // Indicates capability of handling ARGB10 surface which are already BT2020 colorspace and  PQ/2084 encoded as input and
                                                     // scanout it as HD10 signal.
        unsigned int FtrColorTransform3x4Matrix : 1; // Indicates Color Transformation Matrix in display pipeline hardware.
        unsigned int FtrColorTransform3x4MatrixWideColor : 1;       // Indicates support for color transform matrix when scanning out WideColor Data.
        unsigned int FtrColorTransform3x4MatrixHighColor : 1;       // Indicates support for color transform matrix when scanning out HighColor Data.
        unsigned int FtrOSHdr10MetadataPolicySupported : 1;         // Indicates support for HDR10 Metadata Policy from OS which is introduced from WDDM2.7
        unsigned int FtrHdrStaticMetadataViaVscExtSdpSupported : 1; // Indicate if Platform can support HDR Static Metadata via VSC EXT DIP
        unsigned int FtrEscapeOverrideEncodingBpc : 1;              // Indicated support for Override Encoding and Bpc through escape call
        unsigned int FtrOsWcgSupported : 1;                         // Indicate support for OS WCG Mode termed as ACM (Auto Color Management)
        unsigned int FtrDisplayLinearScalingSupported : 1;          // Indicates the Platforms where Linear scaling Feature Supported ; HW has removed POR till ADL
        unsigned int FtrVRR : 1;                                    // VRR Support
        unsigned int FtrNoVrrDoubleBufferUpdate : 1;                // VRR Support without VRR Double Buffer Update Interrupt support in HW
        unsigned int FtrVrrDcBalance : 1;                           // Indicates driver support for DC Balancing
        unsigned int FtrVrrDcBalanceHwCounter : 1;                  // Indicates support for DC Balancing Counters in HW
        unsigned int FtrVrrDcBalanceHwSupport : 1;                  // Indicates HW support for temporary flipline and vmax
        unsigned int FtrVrrPCodeSupport : 1;
        unsigned int FtrCmrr : 1;
        // Bt2020 CS support
        unsigned int FtrPlaneCscSupport : 1; // Plane CSC support for Bt2020

        // HDCP 2_2 GMBUS WA
        unsigned int FtrGMBusSizeOverride : 1; // GMBUS WA enabled
        unsigned int FtrHDCP2_2_HDMI : 1;      // Native HDCP 2.2 support for HDMI enabled
        unsigned int FtrHDCP2_2_DP : 1;        //  Native HDCP 2.2 support for DP enabled

        unsigned int FtrYCBCRSupported : 1; // YCBCR support

        unsigned int FtrPipeJoining : 1;                 ///< Pipe joined mode support for 8k DP 2 pipes/1 port feature and 4 pipes/1 port feature
        unsigned int FtrUltraJoinerSupport : 1;          ///< Ultra Joiner Support for Four Pipe Joined Modes
        unsigned int FtrIsPixelReplicationSupported : 1; ///< DSC Pixel Replication Support for Modes where HActive is not completely divisible by SlicesPerScanline
        unsigned int FtrUncompressedTwoPipeJoiner : 1;   ///< Uncompressed Two Pipe Joiner mode support for DP 2.0 8k
        unsigned int FtrMSTStreamLock : 1;               // for mst pipe lock feature for tile display
        unsigned int FtrDSBSupport : 1;                  // DSB support
        unsigned int FtrDpVscSdpChaining : 1;            // Platform Supports DP1.4 VscSdpChanining
        unsigned int Ftr3DLUTSupportInPipeB : 1;
        unsigned int Ftr3dLutDmcRestore : 1;         // Feature flag to indicate 3DLUT Data Restore support on Dc5/Dc6 Exit using DMC
        unsigned int FtrSharedGfxPowerComponent : 1; // Feature flag to enable shared gfx power component for a platform
        unsigned int Ftr8kModeSupport : 1;           ///< Feature flag to enable/disable 8k resolution i.e. 7680 or 8192.

        unsigned int FtrPsr2ManTrkSupport : 1;                 // Support for PSR2 SW Tracking Selective Update
        unsigned int FtrSelectiveFetchSupport : 1;             // Support for selective fetch and fall back to Full fetch
        unsigned int FtrPanelReplaySupport : 1;                // Display Port Panel Replay
        unsigned int FtrPanelReplaySelectiveUpdateSupport : 1; // Display Port Panel Replay Selective Update
        unsigned int FtrPsr2VdscCoexistance : 1;               // Selective Fetch and PSR2 SW Tracking Selective Update
        unsigned int FtrHWFlipQSupport : 1;                    // HW flip queue support.
        unsigned int FtrFlipQSupport : 1;          // Flip queue support. This will be acting as Primary Ftr flag. If this is False then FtrHWFlipQSupport value is ignored.
        unsigned int FtrOsUnawareFlipQSupport : 1; // For Supporting FlipQ without OS FlipQ support for DC6V.
        unsigned int FtrDisplayEngineToneMappingSupport : 1; // Support Display Engine Tone Mapping
        unsigned int FtrMultiplaneSupport : 1;               // Support Selective fetch in Multiple Planes with DB Stall support
        unsigned int FtrSimpleFlipQSupport : 1;              // Simple Flip Queue Feature support
        unsigned int FtrSWFlipQSupport : 1;                  // SW flipQ support
        unsigned int FtrMinDbufForAsyncFlips : 1;            // If driver should use min dbuf/min WM for async flips or not
        unsigned int FtrEnduranceGaming : 1;                 // Endurance Gaming Feature - Limits frames to given FPS using flip queue
        unsigned int FtrPMAStdSupport : 1;                   // Support PMA Standardization. Available for D14+ platforms
        unsigned int FtrNeedWaitForFlipDone : 1;             // Does not allow surface update on Async planes before previous flip done
        unsigned int FtrCenteredScalingSupport : 1;          // Support the Centered Scaling support
        unsigned int FtrEdidManagement : 1;                  // Enable EDID management feature via IGCL interface
        unsigned int FtrHwFlipQSyncMode : 1;                 // Support for Sync mode of FlipQ (Scanline mode in D13/D14)
        unsigned int FtrFlipQVbiOptimization : 1;
        // eDP 1.5
        unsigned int FtrLobf : 1; // Ftr flag for Link off between active frames
    };

    struct //_sku_dxva
    {
        unsigned int FtrMediaDisable : 1;                    // Media Disabled
        unsigned int Ftr3DIndirectLoad : 1;                  // 3DSTATE_LOAD_INDIRECT is used
        unsigned int Ftr1080pPlusDecoding : 1;               // 1080p Plus Decoding support
        unsigned int FtrNV12 : 1;                            // NV12 format support
        unsigned int FtrAVCMCDecoding : 1;                   // AVC MC w/o FGT decoding enabled
        unsigned int FtrAVCITDecoding : 1;                   // AVC IT w/o FGT decoding enabled
        unsigned int FtrIntelAVCVLDDecoding : 1;             // AVC VLD w/o FGT decoding enabled
        unsigned int FtrAVCFGTDecoding : 1;                  // AVC w FGT decoding enabled
        unsigned int FtrStatusReporting : 1;                 // Status query Reporting for SNB and IVB
        unsigned int FtrAVCVLDLongDecoding : 1;              // MS AVC GUID with long format slice data enabled
        unsigned int FtrAVCVLDShortDecoding : 1;             // MS AVC GUID with short format slice data enabled
        unsigned int FtrIntelAVCVLDHigh422Decoding : 1;      // Intel AVC GUID High 422 decoding enabled
        unsigned int FtrIntelMVCShortDecoding : 1;           // Intel MVC GUID with short format slice data enabled
        unsigned int FtrMVCVLDDecoding : 1;                  // MS MVC VLD decoding enabled
        unsigned int FtrWMV9MCDecoding : 1;                  // WMV9 MC(WMV9B) decoding enabled
        unsigned int FtrWMV9ITDecoding : 1;                  // WMV9 IT(WMV9C) decoding enabled
        unsigned int FtrVC1MCDecoding : 1;                   // VC1 MC decoding enabled
        unsigned int FtrVC1ITDecoding : 1;                   // VC1 IT decoding enabled
        unsigned int FtrIntelVC1VLDAdvancedDecoding : 1;     // Intel proprietary VC1 VLD decoding enabled for Advanced profile
        unsigned int FtrIntelVC1VLDDecoding : 1;             // Intel proprietary VC1 VLD decoding enabled for Simple/Main/Advanced profile
        unsigned int FtrVC1VLDDecoding : 1;                  // MS VC1 VLD decoding enabled
        unsigned int FtrMPEG2MCDecoding : 1;                 // MPEG2 MC decoding enabled
        unsigned int FtrMPEG2IDCTDecoding : 1;               // MPEG2 IDCT decoding enabled
        unsigned int FtrMPEG2VLDDecoding : 1;                // MPEG2 VLD (Bitstream) decoding enabled
        unsigned int FtrVP8VLDDecoding : 1;                  // MS VP8 VLD decoding enabled
        unsigned int FtrIntelVP8VLDDecoding : 1;             // Intel proprietary VP8 VLD decoding enabled
        unsigned int FtrVp8OnVxdEnabled : 1;                 // Indicates that VP8 decode on VXD device is enabled.
        unsigned int FtrIntelHEVCVLDMainDecoding : 1;        // Intel proprietary HEVC VLD main profile decoding enabled, both SF and LF
        unsigned int FtrHEVCVLDMainShortDecoding : 1;        // MS HEVC VLD main profile decoding enabled, SF
        unsigned int FtrIntelHEVCVLDMain10Decoding : 1;      // Intel proprietary HEVC VLD main 10 profile decoding enabled, both SF and LF
        unsigned int FtrHEVCVLDMain10ShortDecoding : 1;      // MS HEVC VLD main 10 profile decoding enabled, SF
        unsigned int FtrDecodeHEVC422VTScalaDisable : 1;     // HEVC 422 VT Scalability Disable
        unsigned int FtrIntelHEVCVLD42210bitDecoding : 1;    // Intel proprietary HEVC VLD main 422 10bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLD4448bitDecoding : 1;     // Intel proprietary HEVC VLD main 444 8bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLD44410bitDecoding : 1;    // Intel proprietary HEVC VLD main 444 10bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMainIntraDecoding : 1;   // Intel proprietary HEVC VLD main intra profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10IntraDecoding : 1; // Intel proprietary HEVC VLD main10 intra profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain12bit420Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain12bit422Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain12bit444Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain8bit420SCC : 1;              // Intel proprietary HEVC VLD main  8bit 420 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10bit420SCC : 1;             // Intel proprietary HEVC VLD main 10bit 420 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain8bit444SCC : 1;              // Intel proprietary HEVC VLD main  8bit 444 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10bit444SCC : 1;             // Intel proprietary HEVC VLD main 10bit 444 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDDecodingSubsetBuffer : 1;        // Intel proprietary HEVC LF real tile decoding Subset buffer
        unsigned int FtrIntelHybridHEVCVLDMainDecoding : 1;          // Hybrid: Intel proprietary HEVC VLD main profile decoding enabled, both SF and LF
        unsigned int FtrHybridHEVCVLDMainShortDecoding : 1;          // Hybrid: MS HEVC VLD main profile decoding enabled, SF
        unsigned int FtrIntelHybridHEVCVLDMain10Decoding : 1;        // Hybrid: Intel proprietary HEVC VLD main 10 profile decoding enabled, both SF and LF
        unsigned int FtrHybridHEVCVLDMain10ShortDecoding : 1;        // Hybrid: MS HEVC VLD main 10 profile decoding enabled, SF
        unsigned int FtrHybridHEVCSliceShutdownEnable : 1;           // Hybrid: Enable Slice Shutdown
        unsigned int FtrIntelVP9VLDProfile0Decoding8bit420 : 1;      // Intel proprietary VP9 VLD 420 8 bit (Profile0) decoding enabled
        unsigned int FtrVP9VLDDecoding : 1;                          // MS VP9 VLD profile0 decoding enabled
        unsigned int FtrVP9VLD10bProfile2Decoding : 1;               // MS VP9 VLD profile2 10-bit decoding enabled
        unsigned int FtrHybridIntelVP9VLDDecoding : 1;               // Intel proprietary VP9 VLD decoding enabled.
        unsigned int FtrIntelVP9VLDProfile1Decoding8bit444 : 1;      // Intel Proprietary VP9 VLD 444 8 bit (Profile1) decoding enabled
        unsigned int FtrIntelVP9VLDProfile2Decoding10bit420 : 1;     // Intel Proprietary VP9 VLD 420 10 bit (Profile2) decoding enabled
        unsigned int FtrIntelVP9VLDProfile3Decoding10bit444 : 1;     // Intel Proprietary VP9 VLD 444 10 bit (Profile3) decoding enabled
        unsigned int FtrIntelVP9VLDProfile2Decoding12bit420 : 1;     // Intel Proprietary VP9 VLD 420 12 bit (Profile2) decoding enabled
        unsigned int FtrIntelVP9VLDProfile3Decoding12bit444 : 1;     // Intel Proprietary VP9 VLD 444 12 bit (Profile3) decoding enabled
        unsigned int FtrHybridVP9SliceShutdownEnable : 1;            // Hybrid VP9: Enable Slice Shutdown
        unsigned int FtrAV1VLDProfile0Decoding : 1;                  // MS AV1 VLD profile0 decoding enabled
        unsigned int FtrIntelAV1VLDDecoding8bit420 : 1;              // Intel proprietary AV1 VLD 420 8 bit (Profile1) decoding enabled
        unsigned int FtrIntelAV1VLDDecoding10bit420 : 1;             // Intel proprietary AV1 VLD 420 10 bit (Profile2) decoding enabled
        unsigned int FtrAV1VLDLSTDecoding : 1;                       // AV1 VLD Large Scale Tile (LST) decoding mode supported
        unsigned int FtrIntelVVCVLDDecodingMain10 : 1;               // VVC VLD Main10 profile decoding enabled
        unsigned int FtrMPEG2Deblocking : 1;                         // OLDB for MPEG2 enabled
        unsigned int FtrMPEG2ErrorConcealment : 1;                   // MPEG2 error concealment enabled
        unsigned int FtrIntelJPEGDecoding : 1;                       // Intel proprietary JPEG decoding enabled
        unsigned int FtrIntelMpeg4VLDDecoding : 1;                   // Intel proprietary Mpeg4 pt2 VLD decoding enabled.
        unsigned int FtrIntelAvsVLDDecoding : 1;                     // Intel proprietary AVS VLD decoding enabled
        unsigned int FtrDecodeSync : 1;                              // Synchronize between 2 decoding engines using a semaphore
        unsigned int FtrProcAmpControl : 1;                          // ProcAmp Control enabled
        unsigned int FtrFilmModeDetection : 1;                       // Film Mode Detection is enabled in media post-processing path
        unsigned int Reserved0 : 1;                                  // DXVA2 Support for screen capture protection when DWM is off
        unsigned int Reserved1 : 1;                                  // DXVA2 Support for screen capture protection for DWM mode
        unsigned int FtrDetailFilter : 1;                            // Support Detail Filter
        unsigned int FtrHDDVDCompositing : 1;                        // DXVA2 Support for HD DVD Compositing
        unsigned int FtrNLAScaling : 1;                              // Support Non-Linear Anamorphic Scaling
        unsigned int FtrNoPerSurfaceTiling : 1;                      // No support for per-surface tiling
        unsigned int FtrPAVP : 1;                                    // Protected Audio Video Path enabled
        unsigned int FtrPAVPSerpent : 1;                             // Support PAVP serpent mode
        unsigned int FtrPAVP2VDBox : 1;                              // Enable PAVP for 2VDBox mode.
        unsigned int FtrPAVPWinWidevine : 1;                         // Enable Widevine drm mode.
        unsigned int FtrPAVPCBCSMode : 1;                            // Enable CBCS mode.
        unsigned int FtrTranscodeAvcInHeavyMode : 1;                 // Support AVC secured transcode in heavy mode
        unsigned int FtrTranscodeMpeg2InHeavyMode : 1;               // Support MPEG-2 secured transcode in heavy mode
        unsigned int FtrPAVPAllowAllSessions : 1;                    // Support the full range of PAVP sessions
        unsigned int FtrPAVPIsolatedDecode : 1;                      // Enable PAVP Isolated Decode for BXT+
        unsigned int FtrHWCounterAutoIncrementSupport : 1;           // Enable HW counter read out for WiDi for KBL+
        unsigned int FtrPAVPStout : 1;                               // Enable PAVP Stout mode for KBL+
        unsigned int FtrPAVPStoutTranscode : 1;                      // Enable PAVP stout transcode mode
        unsigned int FtrPAVPOneOrOne : 1;                            // Enforce PAVP 1-or-1 (ID/Stout or Lite&Heavy)
        unsigned int FtrPAVPLiteModeHucStreamoutDisabled : 1;        // Indicates PAVP lite mode huc streamout is disabled
        unsigned int FtrCencDecodeRemove2ndLevelBatchBufferCopy : 1; // Remove CENC decode temporary 2nd level batch buffer copy for DG2+
        unsigned int FtrHDProcAmp : 1;                               // ProcAmp Control enabled for HD
        unsigned int Ftr3DMediaDefeature : 1;                        // Indicates whether 3D/Media is defeatured
        unsigned int FtrVC1NV12 : 1;                                 // Decoding VC1 using NV12
        unsigned int FtrMPEG2NV12 : 1;                               // Decoding MPEG2 using NV12
        unsigned int FtrDynamicLinking : 1;                          // Dynamic Linking Support
        unsigned int FtrFFDNFilter : 1;                              // Fixed Function Noise Filter
        unsigned int FtrFFDIFilter : 1;                              // Fixed Function Advanced Deinterlacing
        unsigned int FtrDNUVFilter : 1;                              // Chroma Denoise Filter
        unsigned int FtrAVScaling : 1;                               // Adaptive Video Scaling
        unsigned int FtrIEFilter : 1;                                // Image Enhancement Filter (Detail)
        unsigned int FtrHDIEFilter : 1;                              // Image Enhancement Filter (Detail) for HD
        unsigned int FtrNestedBatchBuffer : 1;                       // HW CAP. Nested batch buffer for media object command
        unsigned int FtrHDEnhancedProcessing : 1;                    // Support for HD Enhanced Deinterlacing/Denoise (FastDI+/DN+)
        unsigned int FtrEncodeAVC : 1;                               // Support for AVC ENC + PAK encoding.
        unsigned int FtrEncodeAVCVdenc : 1;                          // Support for AVC VDENC + PAK encoding.
        unsigned int FtrEncode16xME : 1;                             // Support for AVC ENC 16xME
        unsigned int FtrEncodeMPEG2 : 1;                             // Support for MPEG2 ENC + PAK encoding.
        unsigned int FtrEncodeMPEG2Enc : 1;                          // Support for MPEG2 ENC encoding only.
        unsigned int FtrEncodeVP8 : 1;                               // Support for VP8 encoding.
        unsigned int FtrEncodeVP9HybridPAK : 1;                      // Support for VP9 ENC + HyBrid PAK encoding.
        unsigned int FtrEncodeJPEG : 1;                              // Support for JPEG PAK encoding.
        unsigned int FtrEncodeHEVC : 1;                              // Support for HEVC encoding.
        unsigned int FtrEncodeHEVCVdencMain : 1;                     // Support for HEVC VDENC + PAK encoding. Main profile.
        unsigned int FtrEncodeHEVCVdencMain10 : 1;                   // Support for HEVC VDENC + PAK encoding. Main 10 profile.
        unsigned int FtrEncodeHEVC10bit : 1;                         // Support for HEVC encoding 10 bit.
        unsigned int FtrEncodeHEVC10bit422 : 1;                      // Support for HEVC encoding 422 10 bit.
        unsigned int FtrEncodeHEVC12bit : 1;                         // Support for HEVC encoding 12 bit.
        unsigned int FtrEncodeHEVC12bit422 : 1;                      // Support for HEVC encoding 422 12 bit.
        unsigned int FtrEncodeHEVC444 : 1;                           // Support for HEVC encoding 444.
        unsigned int FtrEncodeHEVC10bit444 : 1;                      // Support for HEVC encoding 444 10 bit.
        unsigned int FtrEncodeHEVCVdencMain422 : 1;                  // Support for HEVC VDEnc encoding 422.
        unsigned int FtrEncodeHEVCVdencMain10bit422 : 1;             // Support for HEVC VDEnc encoding 422 10 bit.
        unsigned int FtrEncodeHEVCVdencMain444 : 1;                  // Support for HEVC VDEnc encoding 444 bit.
        unsigned int FtrEncodeHEVCVdencMain10bit444 : 1;             // Support for HEVC VDEnc encoding 444 10 bit.
        unsigned int FtrDecodeOutputSync : 1;                        // Synchronize use of decoding output between 2 engines or contexts
        unsigned int FtrCPFilter : 1;                                // Color Pipe
        unsigned int FtrGamutExpansionMedia : 1;                     // Gamut Expansion for Media
        unsigned int FtrGamutCompressionMedia : 1;                   // Gamut Compression for Media
        unsigned int FtrPreprocessing : 1;                           // Pre-Processing
        unsigned int FtrFastCopyInterface : 1;                       // Support for FastCopy interface
        unsigned int FtrCompositingRate30fps : 1;                    // Compositing frame rate limited to 30fps
        unsigned int FtrVFEWalker : 1;                               // VFE Walker
        unsigned int FtrConcurrentMultiSliceEncode : 1;              // Concurrent Multi-Slice Encode usinf Media Objects
        unsigned int FtrFrameRateConversion24p60p : 1;               // Frame Rate Conversion,24p->60p
        unsigned int FtrFrameRateConversion30p60p : 1;               // Frame Rate Conversion,30p->60p
        unsigned int FtrFrameRateConversionFullHD : 1;               // Frame Rate Conversion for Full HD (1080p)
        unsigned int FtrIStabAffineFilter : 1;                       // Image Stabilization Filter
        unsigned int FtrIStabFilter : 1;                             // Image Stabilization Filter
        unsigned int FtrS3D : 1;                                     // Stereoscopic 3D
        unsigned int FtrDisplayEngineS3d : 1;                        // Display Engine Stereoscopic 3D
        unsigned int FtrCm : 1;                                      // C for Media runtime support
        unsigned int FtrWidiCompose : 1;                             // WiDi compose interface support
        unsigned int FtrCinematicSync : 1;                           // WiDi feature: Supporting Cinematic Sync
        unsigned int FtrPatchWiDiBbWithLastFlippedAddress : 1;       // To allow WiDi BB patching at submit time with last flipped addresses.
        unsigned int FtrDesktopScreen : 1;                           // Desktop Screen interface support
        unsigned int Ftr3pPlugin : 1;                                // 3P Plug-in support (SNB+)
        unsigned int FtrHalfSliceSelect : 1;                         // select half-slice VME unit from IVB+
        unsigned int FtrEncodeAVCMBBRC : 1;                          // Macroblock based Bit Rate Control
        unsigned int FtrCapturePipe : 1;                             // Capture Pipe from BDW+
        unsigned int FtrLensCorrectionFilter : 1;                    // LGCA from SKL+
        unsigned int FtrHwSupportForFieldSeqS3D : 1;                 // Hardware support for field sequential S3D from HSW onwards
        unsigned int FtrSFCPipe : 1;                                 // Scaler & Format Converter Pipe from SKL+
        unsigned int FtrHCP2SFCPipe : 1;                             // HCP to SFC pipe
        unsigned int FtrAVP2SFCPipe : 1;                             // AVP to SFC pipe
        unsigned int FtrSFCHistogramStreamOut : 1;                   // SFC Histogram Stream Out for Gen12+
        unsigned int FtrDisableVDBox2SFC : 1;                        // Disable SFC from VDBOX
        unsigned int FtrDisableVEBoxFeatures : 1;                    // LKF and platforms that VEBOX can only be used in bypass mode
        unsigned int FtrLace : 1;                                    // Local Adaptive Contrast Enhancement from SKL+
        unsigned int FtrFDFB : 1;                                    // Face Detection and Face Beautification from Gen8+
        unsigned int FtrRowstoreCachingEnabled : 1;                  // Rowstore Caching for CHV+ LP platforms
        unsigned int FtrEnableMflDecoder : 1;                        // Multi Format Legacy Decoder
        unsigned int FtrEnableHuC : 1;                               // HuC is a programmable Microcontroller added to the VDBox pipeline
        unsigned int FtrHuCLoadingFromPPGTT : 1;                     // HuC FW is load from PPGTT rather than WOPCM, for non-PAVP platform like GWL.
        unsigned int FtrConditionalBatchBuffEnd : 1;                 // Enable condidtional BB END.
        unsigned int FtrMemoryCompression : 1;                       // Media memory compression from SKL+
        unsigned int FtrEnableMediaKernels : 1;                      // Multi Format Legacy Decoder, HuC is a programmable Microcontroller added to the VDBox pipeline
        unsigned int FtrLegacyMediaKernelLoading : 1;                // Load Media kernels using crypto copy
        unsigned int FtrSliceShutdownOverride : 1;                   // Registry Key Support for Slice Shutdown
        unsigned int FtrEncodeFlatnessCheck : 1;                     // Flatness check support
        unsigned int FtrEncodeMAD : 1;                               // Mean Absolute Difference
        unsigned int FtrVpDisableFor4K : 1;                          // Disable VP features for 4K
        unsigned int FtrVpDisableFor8K : 1;                          // Disable VP features for 8K
        unsigned int FtrMediaPatchless : 1;                          // Enable of patchless support in media for PIGMS.  Expected to be the same value of FtrPigms by default.
                                            // So GMM will initilize the flag after FtrPigms is finalized. Currently implemented in GmmInitContext() ( This Flag is no longer used
                                            // in new Platforms ).

        unsigned int Reserved2 : 1;                        // Enables GPU MMU for WDDM2.0 with limited VA space 2GB or 4GB
        unsigned int FtrForceSCISupport : 1;               // Forced SCI over DSM from SKL+
        unsigned int FtrSingleVeboxSlice : 1;              // Indicate this production have single Vebox slice. SW HSD#5619023 and HW bug_de#2133079 for SFC is tied to VEBOX0.
        unsigned int FtrMedia4KLace : 1;                   // Enable LACE for 4K
        unsigned int FtrHDR : 1;                           // HDR content support from KBL+
        unsigned int Ftr360Stitch : 1;                     // 360 video stitch support from KBL+
        unsigned int FtrSuperResolution : 1;               // Super Resolution support from SKL+
        unsigned int FtrSuperResolutionFor1080P : 1;       // Super Resolution 1080p input support from ADL+
        unsigned int FtrCompsitionMemoryCompressedOut : 1; // Composition Memory compression output support from XeHP
        unsigned int FtrSegmentation : 1;                  // Segmentation support from TGL+
        unsigned int Ftr10bitDecMemoryCompression : 1;     // 10bit decode memory compression from ICL
        unsigned int FtrHcpDecMemoryCompression : 1;       // HCP pipeline decode memory compression from KBL
        unsigned int FtrSimulationMode : 1;
        unsigned int FtrMPOBehaviorHints : 1; // Flag is enable Behavior hints for MPO.
        unsigned int FtrVpP010Output : 1;     // VP P010 output from KBL+
        unsigned int FtrVp10BitSupport : 1;   // VP Y210/Y410 in/out support from Gen11
        unsigned int FtrPaletteRemove : 1;    // Remove Palette for LKF/Gen11HP/Gen12 +
        unsigned int FtrVp16BitSupport : 1;   // VP Y216/Y416 in/out support from Gen12
        unsigned int FtrVpAYUVSupport : 1;    // VP AYUV in/out support from Gen11
        unsigned int FtrDNDisableFor4K : 1;   // Disable DN for 4K
        unsigned int
                     FtrDisableVeboxDIScalar : 1; // Disable Diagonal Interpolation in VEBOX from Gen10 sinze it is ZBBed in https://hsdes.intel.com/appstore/article/#/1208852601/main
        unsigned int FtrSFC420LinearOutputSupport : 1;      // Support new SFC linear output format
        unsigned int FtrSFCRGBPRGB24OutputSupport : 1;      // Support new SFC RGBP tile/linear RGB24 linear output format
        unsigned int FtrDisableRenderTargetWidthAdjust : 1; // Media Render target for kernel output disable width adjust in Dwords
        unsigned int FtrAOTDRCSupport : 1;                  // Array of Textures (AOT) and DRC support for SKL+
        unsigned int FtrEncodeVP9 : 1;                      // Support for VP9 encoding 420 8 bit.
        unsigned int FtrEncodeVP9Vdenc : 1;                 // Support for VP9 Vdenc encoding 420 8 bit
        unsigned int FtrEncodeVP98bit444 : 1;               // Support for VP9 encoding 444 8 bit
        unsigned int FtrEncodeVP9Vdenc8bit444 : 1;          // Support for VP9 Vdenc encoding 444 8 bit
        unsigned int FtrEncodeVP910bit420 : 1;              // Support for VP9 encoding 420 10 bit
        unsigned int FtrEncodeVP9Vdenc10bit420 : 1;         // Support for VP9 Vdenc encoding 420 10 bit
        unsigned int FtrEncodeVP910bit444 : 1;              // Support for VP9 encoding 444 10 bit
        unsigned int FtrEncodeVP9Vdenc10bit444 : 1;         // Support for VP9 Vdenc encoding 444 10 bit
        unsigned int FtrFenceIDRing : 1;                    // FenceID Ring Enable/Disable flag.
        unsigned int FtrCtxtFenceIDList : 1;                // FenceID Ring but at context level instead of DMA level
        unsigned int FtrEncodeHEVCVdencMainSCC : 1;         // Support for HEVC VDENC + PAK SCC extension 8 bit
        unsigned int FtrEncodeHEVCVdencMain10bitSCC : 1;    // Support for HEVC VDENC + PAK SCC extension 10 bit
        unsigned int FtrEncodeHEVCVdencMain444SCC : 1;      // Support for HEVC VDENC + PAK SCC extension 444 8 bit,
        unsigned int FtrEncodeHEVCVdencMain10bit444SCC : 1; // Support for HEVC VDENC + PAK SCC extension 444 10 bit
        unsigned int FtrEnableLogDumpToFile : 1;            // Temporary Ftr to control file dump. Escape call based tool is WIP.
        unsigned int FtrEncodeMFE : 1;                      // Support for MFE
        unsigned int FtrEnableCPHS : 1;                     // Use HECI Service CPHS header
        unsigned int FtrHeciDriverDirectComm : 1;           // KMD will perform driver to driver communication with Heci-Driver. Heci service is not required.
        unsigned int FtrDisableDrDb : 1;                    // Disable File Mode Detection
        unsigned int FtrDisableDIADI : 1;                   // Disable DeInterlace ADAPTIVE support
        unsigned int FtrEncodeAV1Vdenc8bit420 : 1;
        unsigned int FtrEncodeAV1Vdenc10bit420 : 1;
        unsigned int FtrMediaTile64 : 1;
        unsigned int FtrHeight8AlignVE3DLUTDualPipe : 1;
        unsigned int FtrSWMediaReset : 1;
        unsigned int FtrScalingFirst : 1; // Scaling(SFC) first, then VEBOX features
        unsigned int FtrEnablePPCFlush : 1;
        unsigned int FtrSFCTargetRectangle : 1;
        unsigned int FtrVpFP16Input : 1;        // VP FP16 input support from ACM for HDR capture

#if (_DEBUG || _RELEASE_INTERNAL)
        unsigned int FtrLoadHucFwFromFile : 1;  // Load HuC FW from %SystemRoot%\hucfw.bin
#else
        unsigned int ReservedBitD : 1;
#endif // (_DEBUG || _RELEASE_INTERNAL)
        unsigned int FtrSAMediaCachePolicy : 1; // for stand alone media cache policy
        unsigned int FtrPAVPLMemOnly : 1;       // Flag to identify platform on which system mem cannot be accessed by PAVP
        unsigned int FtrForceTile4 : 1;         // Flag to force Tile4 usage as default in Tile64 supported platforms. To be used only for Debug purpose.

        unsigned int FtrMediaNative9 : 1; // Flag to indicate re-enable Media Native DX9
    };
    struct
    {
        unsigned int FtrQT_Performance : 1; // Performance check
    };
    struct // WDDM Version Support
    {
        unsigned int FtrWin7 : 1;
        unsigned int FtrWin8 : 1;
        unsigned int FtrWddm1_3 : 1;
        unsigned int FtrWddm2_0 : 1;
        unsigned int FtrWddm2_1 : 1;
        unsigned int FtrWddm2_2 : 1;
        unsigned int FtrWddm2_3 : 1;
        unsigned int FtrWddm2_4 : 1;
        unsigned int FtrWddm2_5 : 1;
        unsigned int FtrWddm2_6 : 1;
        unsigned int FtrWddm2_7 : 1;
        unsigned int FtrWddm2_8 : 1;
        unsigned int FtrWddm2_9 : 1;
        unsigned int FtrWddm3_0 : 1;
        unsigned int FtrWddm3_1 : 1;
        unsigned int FtrWddm3_2 : 1;
    };

    struct // IPU version, Ftr is mutually exclusive
    {
        unsigned int FtrIpuVersion_5_5 : 1;
        unsigned int FtrIpuVersion_6_0 : 1;
    };

    struct // Minute IA / GuC Related Features
    {
        unsigned int FtrEnableGuC : 1;                    // Minute IA / GuC is enabled
        unsigned int FtrGucBasedPavp : 1;                 // Support Guc Based Pavp
        unsigned int FtrDisableRxSessionAutoTearDown : 1; // For Rx sessions auto teardown should be disabled
                                                          // Todo: Remove once feature is default in mainline
        unsigned int FtrGuCDistributedDoorbell : 1;       // Support for Gen12 Distributed doorbell DCN
        unsigned int FtrGucPcieDoorbell : 1;              // Indicates if PCIE doorbells are supported on this platform.
                                                          // Todo: Remove once Fulsim is ready with complete DDB drop
        unsigned int FtrGuCDDBGT2LimitedConfig : 1;       // Support for Fulsim Phase 1 GT2 ;128 doorbell config supported
        unsigned int Ftr11GuCOn9 : 1;                     // Use Gen11 GuC interfaces, also use Gen11 unified GuC source for Gen9 GuC binary.
        unsigned int FtrGuCEngineClassScheduling : 1;     // Use Gen11 GuC interfaces, also use Gen11 unified GuC source for Gen9 GuC binary.
        unsigned int FtrNewGucInterface : 1;              // Use new GuC interfaces
        unsigned int FtrEncryptedSysInfo : 1;             // Load guc in 2 steps and get sysinfo from guc
        unsigned int FtrEnablePreemptionDataLogging : 1;  // Guc log support for preemption
    };

    struct // Security features
    {
        unsigned int FtrKmSecurityParser : 1;
    };

    struct // Win optional features
    {
        unsigned int FtrOsManagedHwContext : 1;
        unsigned int FtrIoMmuSecureModeSupported : 1;
        unsigned int FtrDmaRemapSupported : 1;
    };

    struct // Features for the Child Drivers of the GFX Driver
    {
        unsigned int FtrEnableISPChild : 1; // Adds camera as child of Graphics.
        unsigned int FtrEnableI2CChild : 1; // Adds I2C as child of Graphics.
        unsigned int FtrEnableCTAChild : 1;
    };

    struct // Virtualization features
    {
        unsigned int FtrVgt : 1;
        unsigned int FtrIsVF : 1;
        unsigned int FtrSriovEnable : 1;
        unsigned int FtrGPUPartitionEnable : 1;
        unsigned int Ftr3LevelLmtt : 1;
        unsigned int FtrH2GSubmitContext : 1;
    };

    struct // OGL related features
    {
        unsigned int FtrOGLTexelOffsetPrecisionFix : 1;
    };

    struct
    {
        unsigned int FtrRGBColorSeparation : 1;
    };

    struct // OCL related features
    {
        unsigned int FtrEnableMissingAlpaFormatFilter : 1;
        unsigned int FtrEnablePlanarYUVFilteringFix : 1;
    };

    struct
    {
        unsigned int FtrEnableSCDCInterrupt : 1;
        unsigned int FtrWiGigEnableLivePCRReporting : 1;
    };

    // GEN10+ GT PSMI
    struct
    {
        unsigned int FtrGtPsmi : 1; // GEN10+ GT PSMI capable
    };

    struct // Graphics Security Controller (GSC) - for PAVP/CP/DRM on GEN12-based Dash-G* products
    {
        unsigned int FtrGSC : 1;                      // Indicates that GSC node (real or simulated) exists
        unsigned int FtrGscCS : 1;                    // Indicates GSC Commmand streamer is supported MTL+
        unsigned int FtrGscHeci2ChildDevice : 1;      // indicates that the driver supports instantiating the HECI-2 child device
        unsigned int FtrGucDepriv : 1;                // indicates that GuC is de-priviledged
        unsigned int FtrGscBasedHucLoad : 1;          // indicates that HuC is loaded and authenticated by GSC
        unsigned int FtrGscSwProxy : 1;               // indicates SW Proxy flows are supported.
        unsigned int FtrGscBasedWOPCMProgramming : 1; // Indicates that the GSC FSP will program the GuC WOPCM offset and base.
        unsigned int FtrGscSimPhase : 3;              // Phase 1: KMD simulates GSC node via HECI tunneling SW.
                                                      // Phase 2: KMD fakes GSC node via MMIO register trapping to HECI tunneling
                                                      // Explicitly setting the registry value to a 0 indicates that GSC support should be disabled (even if real GSC exists)
                                                      // any other simulation phase values are currently undefined (and ignored)
    };

    struct // For MultiTileArch, KMD reports default tile assignment to UMD-GmmLib - via __KmQueryDriverPrivateInfo
    {
        unsigned int FtrAssignedGpuTile : 3; // Indicates Gpu Tile number assigned to a process for Naive apps.
    };

    struct // LDA related
    {
        unsigned int FtrSlsSupported : 1; // MGPU SLS/ Combined Display support
        unsigned int FtrLdaMode : 1;      // Indicates LDA mode of operation enabled or not
    };
} SKU_FEATURE_TABLE, *PSKU_FEATURE_TABLE;

#if defined(__clang__)
#pragma clang diagnostic pop
#elif defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

#endif // defined(_USC_)

//********************************** WA ****************************************

enum WA_BUG_TYPE
{
    WA_BUG_TYPE_UNKNOWN    = 0,
    WA_BUG_TYPE_CORRUPTION = 1,
    WA_BUG_TYPE_HANG       = 2,
    WA_BUG_TYPE_PERF       = 4,
    WA_BUG_TYPE_FUNCTIONAL = 8,
    WA_BUG_TYPE_SPEC       = 16,
    WA_BUG_TYPE_FAIL       = 32
};

#define WA_BUG_PERF_IMPACT(f) f
#define WA_BUG_PERF_IMPACT_UNKNOWN -1

enum WA_COMPONENT
{
    WA_COMPONENT_UNKNOWN  = 0,
    WA_COMPONENT_KMD      = 0x1,
    WA_COMPONENT_MINIPORT = 0x2,
    WA_COMPONENT_GMM      = 0x4,
    WA_COMPONENT_D3D      = 0x8,
    WA_COMPONENT_OGL      = 0x10,
    WA_COMPONENT_SOFTBIOS = 0x20,
    WA_COMPONENT_PWRCONS  = 0x40,
    WA_COMPONENT_MEDIA    = 0x80,
    WA_COMPONENT_OCL      = 0x100,
};

// Workaround Table structure to abstract WA based on HW and rev ID
typedef struct _WA_TABLE
{

#define WA_DECLARE(wa, wa_comment, wa_bugType, wa_impact, wa_component) unsigned int wa : 1;
#include "sku_wa_defs.h"
#undef WA_DECLARE
} WA_TABLE, *PWA_TABLE;

#ifdef _USC_
/*****************************************************************************\

STRUCT:
    HW_STATUS

Description:
    holds WA info for compiler

\*****************************************************************************/
struct HW_STATUS
{
    SKU_FEATURE_TABLE SkuTable;
    WA_TABLE          WaTable;

    SKU_FEATURE_TABLE *pSkuTable;
    WA_TABLE *         pWaTable;
};
#endif //_USC_

//********************************** SKU/WA Macros *************************************

#if (defined(__MINIPORT) || defined(__KCH) || defined(__SOFTBIOS) || defined(__GRM) || defined(__PWRCONS))
#if LHDM || LINUX

#if (!defined __cplusplus) || (defined __KMDULT)
#define GFX_IS_SKU(s, f) ((s)->SkuTable.f)
#define GFX_IS_WA(s, w) ((s)->WaTable.w)
#define GFX_WRITE_WA(x, y, z) ((x)->WaTable.y = z)
// No checking is done in the GFX_WRITE_SKU macro that z actually fits into y.
//   It is up to the user to know the size of y and to pass in z accordingly.
#define GFX_WRITE_SKU(x, y, z) ((x)->SkuTable.y = z)
#else
#define GFX_IS_SKU(s, f) ((s)->SystemConfigInfo.SkuTable.f)
#define GFX_IS_WA(s, w) ((s)->SystemConfigInfo.WaTable.w)
#define GFX_WRITE_WA(x, y, z) ((x)->SystemConfigInfo.WaTable.y = z)
#define GFX_WRITE_SKU(x, y, z) ((x)->SystemConfigInfo.SkuTable.y = z)
#endif

#else
#define GFX_IS_SKU(h, f) (((PHW_DEVICE_EXTENSION)(h))->pHWStatusPage->pSkuTable->f)
#define GFX_IS_WA(h, w) (((PHW_DEVICE_EXTENSION)(h))->pHWStatusPage->pWaTable->w)
#define GFX_WRITE_WA(x, y, z) (((HW_DEVICE_EXTENSION *)(x))->pHWStatusPage->pWaTable->y = z)
// No checking is done in the GFX_WRITE_SKU macro that z actually fits into y.
//   It is up to the user to know the size of y and to pass in z accordingly.
#define GFX_WRITE_SKU(x, y, z) (((HW_DEVICE_EXTENSION *)(x))->pHWStatusPage->pSkuTable->y = z)
#endif // end LHDM
#else
#if XPDM
#define GFX_IS_SKU(s, f) ((s)->pSkuTable->f)
#define GFX_IS_WA(s, w) ((s)->pWaTable->w)
#else
#define GFX_IS_SKU(s, f) ((s)->SkuTable.f)
#define GFX_IS_WA(s, w) ((s)->WaTable.w)
#endif
#endif
#define GRAPHICS_IS_SKU(s, f) ((s)->f)
#define GRAPHICS_IS_WA(s, w) ((s)->w)

#pragma warning(pop)

#endif //__SKU_WA_H__
