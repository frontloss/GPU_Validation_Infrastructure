/*****************************************************************************\

INTEL CONFIDENTIAL
Copyright 2013-2017
Intel Corporation All Rights Reserved.

The source code contained or described herein and all documents related to the
source code ("Material") are owned by Intel Corporation or its suppliers or
licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential
information of Intel or its suppliers and licensors. The Material is protected by
worldwide copyright and trade secret laws and treaty provisions. No part of the
Material may be used, copied, reproduced, modified, published, uploaded, posted
transmitted, distributed, or disclosed in any way without Intel's prior express
written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel
or otherwise. Any license under such intellectual property rights must be
express and approved by Intel in writing.

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

\*****************************************************************************/
#ifndef __SKU_WA_H__
#define __SKU_WA_H__

#if (_DEBUG || _RELEASE_INTERNAL)
#define GLOBAL_WAFTR_ENABLED 1
#endif

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
        unsigned int FtrMmioBar : 1;                    // Mmio bar
        unsigned int FtrDioBar : 1;                     // Direct io bar
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
        unsigned int FtrCCSNode : 1; // To indicate if Compute Only Ring is supported in Gen12+
        unsigned int FtrCCSRing : 1; // To indicate if CCS hardware ring support is present.
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
        unsigned int FtrDisableMPOMultiDisplayConfig : 1; // Indicates Multi Plane Overlay(MPO) Support for Clone
        unsigned int FtrFractional48Hz : 1;               // Fractional 48 Hz support
        unsigned int FtrCHVBxSku : 1;                     // Indicates CHV Bx Stepping
        unsigned int FtrSplitScreenMPO : 1;
        unsigned int FtrInvertRotation : 1; // Inverted Rotation for Razer RCR: 1024246
        unsigned int FtrPortraitLFP : 1;
        unsigned int FtrGunitOffset : 1;                   // GUNIT offset
        unsigned int FtrHWScalingNotSupported : 1;         // Hw Scaling not Supported on VLV and CHV
        unsigned int FtrDynamicCDClkOnlyForSDInternal : 1; // Dynamic CD clk enabled only on Single Display internal panel config
        unsigned int FtrDDI4 : 1;                          // 4th DDI on CNL
        unsigned int FtrEnableUnderRun : 1;                // Set this bit for Enable Under run request, so after PM based on this bit enable under run again.
        unsigned int FtrEnable10bitRGBMPO : 1;             // Enable 10bit RGB MPO.
        unsigned int FtrSAGVNotifyPCode : 1;               // Driver notification of PCode in interlace mode or single/multi display mode to enable/disable SAGV
        unsigned int FtrCoG : 1;                           // CoG Support
        unsigned int FtreDPVDSC : 1;                       // eDP VDSC Support
        unsigned int FtrPeriodicFrameNotification : 1;     // Periodic Frame Notification Support
        unsigned int FtrEnableAssertOnOnUnderrun : 1;      // Set this bit for Enable BSOD if pipe underrun happens (only for validation purpose).
        unsigned int FtrDPVDSC : 1;                        // DP VDSC Support
    };

    struct //_sku_Media_Features.
    {
        unsigned int FtrClearVideoTechnology : 1; // ClearVideoTechnology Support
        unsigned int FtrPooledEuEnabled : 1;      // Media pooled state(enabled/disabled)
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

        unsigned int FtrBigPage : 1;             // Large pages for media encode
        unsigned int FtrPPGTT : 1;               // Per-Process GTT
        unsigned int FtrIA32eGfxPTEs : 1;        // GTT/PPGTT's use 64-bit IA-32e PTE format.
        unsigned int FtrPml4Support : 1;         // PML4-based gfx page tables are supported (in addition to PD-based tables).
        unsigned int FtrPml3OnHwPml4Support : 1; // LKF PPGTT VA space is reduced to 36bits but h/w still use 4 Level Walk.
        unsigned int FtrSVM : 1; // Shared Virtual Memory (i.e. support for SVM buffers which can be accessed by both the CPU and GPU at numerically equivalent addresses.)
        unsigned int FtrTileMappedResource : 1;          // Tiled Resource support aka Sparse Textures.
        unsigned int FtrTranslationTable : 1;            // Translation Table support for Tiled Resources.
        unsigned int FtrUserModeTranslationTable : 1;    // User mode managed Translation Table support for Tiled Resources.
        unsigned int FtrNullPages : 1;                   // Support for PTE-based Null pages for Sparse/Tiled Resources).
        unsigned int FtrL3IACoherency : 1;               // Graphics L3 coherency with IA is supported.
        unsigned int FtrMIUpdateGTTCanUpdatePPGTT : 1;   // MI_UPDATE_GTT can update PPGTT - new feature added from IVB+
        unsigned int FtrReportCombinedDVMSSVM : 1;       // Combine DVM and SVM for Win7
        unsigned int FtrRemoteFx : 1;                    // Enable 1.5GB dedicated video memory. RCR 1023713
        unsigned int FtrDriverManagedL3ParityErrors : 1; // Driver manages L3 parity errors since not ECC.
        unsigned int FtrL3HangOnParityError : 1;         // Enable HW hanging on L3 parity error
        unsigned int FtrEDram : 1;                       // embedded DRAM enable
        unsigned int FtrLLCBypass : 1;                   // Partial tunneling of UC memory traffic via CCF (LLC Bypass)
        unsigned int FtrCrystalwell : 1;                 // Crystalwell Sku
        unsigned int FtrCentralCachePolicy : 1;          // Centralized Cache Policy
        unsigned int FtrIoMmu : 1;                       // IOMMU exists on platform
        unsigned int FtrDriverControlledIoMmu : 1;       // Driver controlling IOMMU
        unsigned int FtrIoMmuPageFaulting : 1;           // IOMMU Page Faulting Support
        unsigned int FtrDmaBufferMemSpaceSplitting : 1;  // DMA buffer is in global memory space, and indirect heap is paged to per-process memory space
        unsigned int FtrSecurePPGTTUpdate : 1;           // Segment providing mapping to PPGTT is in Global GTT space
        unsigned int FtrPigms : 1;                       // Process-Isolated Gfx Memory Spaces
        unsigned int FtrWddm2GpuMmu : 1;                 // WDDMv2 GpuMmu Model (Set in platform SKU files, but disabled by GMM as appropriate for given system.)
        unsigned int FtrWddm2Svm : 1;                    // WDDMv2 SVM Model (Set in platform SKU files, but disabled by GMM as appropriate for given system.)
        unsigned int FtrStandardMipTailFormat : 1;       // Dx Standard MipTail Format for TileYf/Ys
        unsigned int FtrDisplayColorEnhancement : 1;     // Asus Display color enhancement support
        unsigned int FtrWddm2_1_64kbPages : 1;           // WDDMv2.1 64KB page support
        unsigned int FtrGttCacheInvalidation : 1;        // GTT cache invalidation support
        unsigned int FtrMemorySeg : 1;                   // Defines GMM Memory Segment, For ICXG's HBM, Pre-Si usage, POC etc,
        unsigned int FtrCacheCoherentMemSeg : 1;         // For ICX-G CacheCoherent HBM Mem Segment
        unsigned int FtrDynamicDisplayAliasing : 1;      // Enable Dynamic Display Aliasing for Displayable surfaces in  GlobalGTTHeap
        unsigned int FtrE2ECompression : 1;              // E2E Compression ie Aux Table support
        unsigned int FtrLinearCCS : 1;                   // Linear Aux surface is supported

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
        unsigned int FtrHwBin : 1;                          // Hw binner
        unsigned int Ftr8BitPalette : 1;                    // 8bit index color texture
        unsigned int FtrPixelShader : 1;                    // Pixel shader
        unsigned int FtrPixelShader30 : 1;                  // Pixel shader 3.0
        unsigned int FtrBWGConsumerTextures : 1;            // Enable new texture formats for BW-G 14.21 consumer skus
        unsigned int FtrMultiRenderTarget : 1;              // Multiple Render Targets (Gen4)
        unsigned int FtrHWTnL : 1;                          // HW T&L (Gen4)
        unsigned int FtrOcclusionQuery : 1;                 // Occlusion Query (Gen4 D3D)
        unsigned int FtrOcclusionQueryOGL : 1;              // Occlusion Query (Gen4 OGL)
        unsigned int FtrAutoGenMipMap : 1;                  // Auto MipMap Generation (Gen4 D3D)
        unsigned int FtrDX10Support : 1;                    // DX10 driver enumeration
        unsigned int FtrDX10_1Support : 1;                  // DX10.1 driver enumeration
        unsigned int FtrDX11_Xon10Support : 1;              // DX11on10 driver enumeration
        unsigned int FtrDX11Support : 1;                    // DX11 driver enumeration
        unsigned int FtrDX11_1Support : 1;                  // DX11.1 driver enumeration
        unsigned int FtrWorkstation : 1;                    // Workstation Direct3D
        unsigned int FtrEtcFormats : 1;                     // ETC formats support
        unsigned int FtrAstcLdr2D : 1;                      // ASTC 2D LDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrAstcHdr2D : 1;                      // ASTC 2D HDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrAstc3D : 1;                         // ASTC 3D LDR/HDR Mode Support (mutually exclusive from other ASTC Ftr's)
        unsigned int FtrUmdThreadingShim : 1;               // Enable multithreaded UMD.
        unsigned int FtrBoundingBoxOptOGL : 1;              // Enable bounding box Optimization in OpenGL
        unsigned int FtrResourceStreamerEnabled : 1;        // Resource Streamer Support (For 3D UMD use only)
        unsigned int FtrHiZSamplerDisabled : 1;             // HiZ Sampling capability
        unsigned int FtrDisableDX10IdleGpuFlushOnPresi : 1; // DX10 UMD trigger to disable IdleGpuFlush optimization only when running on pre-si platforms
        unsigned int FtrE2ECompressionOnGen11 : 1;          // SKU check for E2EC feature for LKF
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

        // DPS Features
        unsigned int FtrDps : 1;                   // Display P-States (DPS)
        unsigned int FtrSupportCuiDrrsFeature : 1; // Indicates whether the platform supports the CUI-driven Static DRRS feature

        // DPST
        unsigned int FtrDpst : 1;                     // Display Power Savings Technology (DPST)
        unsigned int FtrDpstEnginePerPipe : 1;        // Separate DPST engine supported on each pipe
        unsigned int FtrDpstHistogramBinClamping : 1; // DPST histogram bin clamping support to enable resolutions upto 8MPixels
        unsigned int FtrDpstAfterPipeScaler : 1;      // DPST hardware lies after panel fitter on HSW platforms

        // LACE
        unsigned int FtrDisplayLace : 1;        // Local Area Contrast Enhacement (LACE)
        unsigned int FtrDisplayLacePhaseIn : 1; // Display LACE Phase-in

        // Backlight Control
        unsigned int FtrBlc : 1;                         // Backlight Control (BLC)
        unsigned int FtrBlcDxgkDdi : 1;                  // Vista Backlight Control DxgkDdi interface
        unsigned int FtrDynamicPWMFreqMinBrightness : 1; // Dynamic PWM frequency and minimum brightness support
        unsigned int FtrBlcPerPipe : 1;                  // Separate backlight control supported on each pipe
        unsigned int FtrBlcSmoothTransition : 1;         // Support for BLC smooth brightness control on Windows 8+
        unsigned int FtrBlcFlexiblePWMGranularity : 1;   // Support flexible PWM granularity
        unsigned int FtrBlcAssertiveDisplay : 1;         // Assertive Display Support
        unsigned int FtrBlcBIOSNotification : 1;         // Send BIOS SCI notification on driver backlight adjustments
        unsigned int FtrBlcPwmFreqCdClkDependent : 1;    // PWM frequency is based on CDCLK

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

        // DPTF / Camarillo
        unsigned int FtrDptfProcMgmt : 1;                        // Indicates whether or not driver support Graphics/Proc Participant
        unsigned int FtrDptfProcCommunicationActive : 1;         // The link between DPTF and Graphics/Proc stack is active
        unsigned int FtrDptfDisplayMgmt : 1;                     // Display Driver support for DPTF
        unsigned int FtrDptfDisplayDriverCommActive : 1;         // The link between DPTF and display stack is active
        unsigned int FtrDptfEnhancedDisplayMgmt : 1;             // Enhanced Display Driver support for DPTF
        unsigned int FtrDptfEnhancedDisplayDriverCommActive : 1; // The link between DPTF and enhanced display stack is active

        // Render Geyserville Sleep State Features
        unsigned int FtrRS : 1;                              // Render Standby
        unsigned int FtrRsLowerRc6PromotionTimeForMedia : 1; // Lower Promotion Time for Media
        unsigned int FtrRsCoarsePowerGating : 1;             // Support individual media/render power gating
        unsigned int FtrRsMediaSubEngineForceWake : 1;
        unsigned int FtrRsMediaSamplerPowerGating : 1;
        unsigned int FtrRsMediaSubpipePowerGating : 1; // Support MFX/HCP within VDbox power gating

        // Slice Shutdown
        unsigned int FtrSliceShutdown : 1; // Support shutting down a GT Slice dynamically on media workload for power saving.

        // Panel Self Refresh
        unsigned int FtrPsr : 1;               // PSR Support
        unsigned int FtrPsrSfu : 1;            // Single Frame Update for PSR
        unsigned int FtrPsrSu : 1;             // Selective Update for PSR
        unsigned int FtrPsrPowerDownLcpll : 1; // Turn off LCPLL in PSR mode
        unsigned int FtrPsrInMultiDisplay : 1; // PSR Support in Multi Display

        // FPS Tracking / DFPS
        unsigned int FtrFpsTracking : 1; // FPS tracking functionality
        unsigned int FtrDfps : 1;        // Frame Rate Control
        unsigned int FtrPvqc : 1;        // Adaptive Rendering Control (a.k.a PVQC)

        // DCC
        unsigned int FtrDcc : 1; // Duty Cycle Control
        unsigned int FtrDct : 1; // Duty Cycle Throttling

        // Valleyview specific turbo changes
        unsigned int FtrGsvTurboVLV : 1; // Valleyview turbo changes

        unsigned int FtrIps : 1; // Intermediate Pixel Storage feature

        unsigned int FtrWriteMCHRegsViaPcu : 1; // Write MCHBAR registers through the PCU if they are R/O through MMIO

        // Slice/Sub-Slice Shutdown/EU Power gating support
        unsigned int FtrSSEUPowerGating : 1; // Support shutting down a Slice/Sub-slice/EU power gating dynamically.

        unsigned int FtrSSEUPowerGatingControlByUMD : 1; // Support SSEU power gating control by UMD.

        // Single-loop power management
        unsigned int FtrSLPM : 1; // Single-loop power management (master switch)

        // Real-Time Command Queue support for RS2 to boost the GT frequency to MAX for Real time workload
        unsigned int FtrRealTimeWLBoost : 1;

        // Dynamic Frequency Rebalancing - aims to reduce Sampler power by dynamically changing its clock frequency in low-throughput conditions
        unsigned int FtrSamplerDFR : 1;
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
        // Dp 1.2 related
        unsigned int FtrLinkTrainingBeforeGMCHSetTiming : 1; // DP Link training is done in the beginning of enable sequence
        unsigned int FtrTPS3Supported : 1;                   // DP Training Pattern 3 is support
        unsigned int FtrHBR2Supported : 1;                   // DP HBR2 Linkrate support
        unsigned int FtrEnableDPMST : 1;                     // DP Multi Stream Transport support
        unsigned int FtrDynamicTUComputation : 1;            // Compute DP TU dynamically
        unsigned int FtrSinglePFOnly : 1;                    // CDV, VLV platforms
        unsigned int FtrPPSAttachedtoPipe : 1;               // VLV platforms where 2 per pipe PPS is present
        unsigned int FtrLoadHDCPKeys : 1;                    // HDCP keys needs to be loaded in VLV
        unsigned int FtrColorRangeClipByPort : 1;            // For VLV.Color Range clipping  to be done by port[HDMI/DP],instead of pipe.
        unsigned int FtrDPInterlacedModeRemoval : 1;         // For VLV we want removal of interlaced mode in case of DP.
        // Dp 1.3 Related
        unsigned int FtrTPS4Supported : 1; // DP Training Pattern 4 support
        unsigned int FtrHBR3Supported : 1;
        unsigned int FtrDPYUV420PixelEncodingSupported : 1;

        // eDP1.4 Related
        unsigned int FtrLowVswingSupport : 1; // for eDP1.4 lower vswing and pre-emphasis support
        unsigned int
                     FtrCHVEnableScalerForExternalDisplay : 1; // [VLV RCR-1024545 Porting on CHV] Enable the single scalar for External Panel when device config is LFP native clone
        unsigned int FtrEnableDC5DC6 : 1;
        unsigned int FtrEnableDC9 : 1;
        unsigned int FtrEnableIOUngatedDMC : 1; // WA for IO HW HSD: https://hsdes.intel.com/appstore/article/#/1304976242
        unsigned int FtrEnableDCStateinPSR : 1;
        unsigned int FtrRendComp : 1;                  // For Render Compression Feature on Gen9+
        unsigned int FtrClearColor : 1;                // For Clear Color Gen11.5+
        unsigned int FtrMediaComp : 1;                 // LKF+
        unsigned int FtrDisplayYTiling : 1;            // For Y Tile Feature on Gen9+
        unsigned int FtrAlwaysEnableAllDBUFSlices : 1; // Enables DBUF_S1 and DBUF_S2 all the time on Gen11
        // HDMI 2.0 LS-PCON specific
        unsigned int FtrEnableLsPcon : 1; // for HDMI2.0 support using LS-PCON
        unsigned int FtrDDIeEnabled : 1;  // enabling of DDI-E for DP->VGA on Skl Desktop systems
        // HDMI 2.0 specific
        unsigned int FtrNativeHDMI2_0Support : 1; // From GEMINILAKE onwards Native HDMI2.0 is supported
        unsigned int FtrDdiAEnabledasVGA : 1;     // Enabling eDP - DDI-A as VGA
        unsigned int FtrDdiAEnabledasDP : 1;      // Enabling eDP - DDI-A as DP
        // HDCP 2.2 specific
        unsigned int FtrNativeHDCP2_2Support : 1;
        // WIGIG Related
        unsigned int FtrEnableWGBoxWigig : 1; // Enable Wigig using WGBox
        // Display only Driver
        unsigned int FtrWinDoD : 1; // for Display only Driver support
        // HDR Feature related to HDMI2.0a
        unsigned int FtrEnableHDRSupport : 1; // Enable HDR Feature
        unsigned int FtrEnableOSHDR : 1;      // Enable OS HDR.

        unsigned int FtrVRR : 1;                     // VRR Support
        unsigned int FtrNoVrrDoubleBufferUpdate : 1; // VRR Support without VRR Double Buffer Update Interrupt support in HW
        // Bt2020 CS support
        unsigned int FtrPlaneCscSupport : 1; // Plane CSC support for Bt2020

        // HDCP 2_2 GMBUS WA
        unsigned int FtrGMBusSizeOverride : 1; // GMBUS WA enabled
        unsigned int FtrHDCP2_2_HDMI : 1;      // Native HDCP 2.2 support for HDMI enabled
        unsigned int FtrHDCP2_2_DP : 1;        //  Native HDCP 2.2 support for DP enabled

        unsigned int FtrYCBCRSupported : 1; // YCBCR support

        unsigned int FtrPipeGanging : 1;   ///< Pipe ganged mode support for 8k DP 2 pipes/1 port feature
        unsigned int FtrMSTStreamLock : 1; // for mst pipe lock feature for tile display
    };

    struct //_sku_dxva
    {
        unsigned int FtrAdaptiveDIFilter : 1;                // Adaptive Deinterlacing filter support
        unsigned int Ftr3DIndirectLoad : 1;                  // 3DSTATE_LOAD_INDIRECT is used
        unsigned int FtrMODEASTFilter : 1;                   // MODEAST filter support
        unsigned int FtrEncryption : 1;                      // VLD Encryption enabled
        unsigned int Ftr1080pPlusDecoding : 1;               // 1080p Plus Decoding support
        unsigned int FtrNV12 : 1;                            // NV12 format support
        unsigned int FtrAVCMCDecoding : 1;                   // AVC MC w/o FGT decoding enabled
        unsigned int FtrAVCITDecoding : 1;                   // AVC IT w/o FGT decoding enabled
        unsigned int FtrIntelAVCVLDDecoding : 1;             // AVC VLD w/o FGT decoding enabled
        unsigned int FtrAVCFGTDecoding : 1;                  // AVC w FGT decoding enabled
        unsigned int FtrStatusReporting : 1;                 // Status query Reporting for SNB and IVB
        unsigned int FtrAVCVLDLongDecoding : 1;              // MS AVC GUID with long format slice data enabled
        unsigned int FtrAVCVLDShortDecoding : 1;             // MS AVC GUID with short format slice data enabled
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
        unsigned int FtrIntelHEVCVLD42210bitDecoding : 1;    // Intel proprietary HEVC VLD main 422 10bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLD4448bitDecoding : 1;     // Intel proprietary HEVC VLD main 444 8bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLD44410bitDecoding : 1;    // Intel proprietary HEVC VLD main 444 10bit profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMainIntraDecoding : 1;   // Intel proprietary HEVC VLD main intra profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10IntraDecoding : 1; // Intel proprietary HEVC VLD main10 intra profile decoding enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain12bit420Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain12bit422Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain12bit444Decoding : 1;
        unsigned int FtrIntelHEVCVLDMain8bit420SCC : 1;          // Intel proprietary HEVC VLD main  8bit 420 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10bit420SCC : 1;         // Intel proprietary HEVC VLD main 10bit 420 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain8bit444SCC : 1;          // Intel proprietary HEVC VLD main  8bit 444 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDMain10bit444SCC : 1;         // Intel proprietary HEVC VLD main 10bit 444 SCC enabled, both SF and LF
        unsigned int FtrIntelHEVCVLDDecodingSubsetBuffer : 1;    // Intel proprietary HEVC LF real tile decoding Subset buffer
        unsigned int FtrIntelHybridHEVCVLDMainDecoding : 1;      // Hybrid: Intel proprietary HEVC VLD main profile decoding enabled, both SF and LF
        unsigned int FtrHybridHEVCVLDMainShortDecoding : 1;      // Hybrid: MS HEVC VLD main profile decoding enabled, SF
        unsigned int FtrIntelHybridHEVCVLDMain10Decoding : 1;    // Hybrid: Intel proprietary HEVC VLD main 10 profile decoding enabled, both SF and LF
        unsigned int FtrHybridHEVCVLDMain10ShortDecoding : 1;    // Hybrid: MS HEVC VLD main 10 profile decoding enabled, SF
        unsigned int FtrHybridHEVCSliceShutdownEnable : 1;       // Hybrid: Enable Slice Shutdown
        unsigned int FtrIntelVP9VLDProfile0Decoding8bit420 : 1;  // Intel proprietary VP9 VLD 420 8 bit (Profile0) decoding enabled
        unsigned int FtrVP9VLDDecoding : 1;                      // MS VP9 VLD profile0 decoding enabled
        unsigned int FtrVP9VLD10bProfile2Decoding : 1;           // MS VP9 VLD profile2 10-bit decoding enabled
        unsigned int FtrHybridIntelVP9VLDDecoding : 1;           // Intel proprietary VP9 VLD decoding enabled.
        unsigned int FtrIntelVP9VLDProfile1Decoding8bit444 : 1;  // Intel Proprietary VP9 VLD 444 8 bit (Profile1) decoding enabled
        unsigned int FtrIntelVP9VLDProfile2Decoding10bit420 : 1; // Intel Proprietary VP9 VLD 420 10 bit (Profile2) decoding enabled
        unsigned int FtrIntelVP9VLDProfile3Decoding10bit444 : 1; // Intel Proprietary VP9 VLD 444 10 bit (Profile3) decoding enabled
        unsigned int FtrIntelVP9VLDProfile2Decoding12bit420 : 1; // Intel Proprietary VP9 VLD 420 12 bit (Profile2) decoding enabled
        unsigned int FtrIntelVP9VLDProfile3Decoding12bit444 : 1; // Intel Proprietary VP9 VLD 444 12 bit (Profile3) decoding enabled
        unsigned int FtrHybridVP9SliceShutdownEnable : 1;        // Hybrid VP9: Enable Slice Shutdown
        unsigned int FtrIntelAV1VLDDecoding8bit420 : 1;          // Intel proprietary AV1 VLD 420 8 bit decoding enabled
        unsigned int FtrMPEG2Deblocking : 1;                     // OLDB for MPEG2 enabled
        unsigned int FtrMPEG2ErrorConcealment : 1;               // MPEG2 error concealment enabled
        unsigned int FtrIntelJPEGDecoding : 1;                   // Intel proprietary JPEG decoding enabled
        unsigned int FtrIntelMpeg4VLDDecoding : 1;               // Intel proprietary Mpeg4 pt2 VLD decoding enabled.
        unsigned int FtrIntelAvsVLDDecoding : 1;                 // Intel proprietary AVS VLD decoding enabled
        unsigned int FtrDecodeSync : 1;                          // Synchronize between 2 decoding engines using a semaphore
        unsigned int FtrProcAmpControl : 1;                      // ProcAmp Control enabled
        unsigned int FtrFilmModeDetection : 1;                   // Film Mode Detection is enabled in media post-processing path
        unsigned int FtrHQScaling : 1;                           // Support 4x4 scaling
        unsigned int FtrPolyScaling : 1;                         // Support 6x6 polyphase scaling
        unsigned int FtrScreenCaptureOverlay : 1;                // DXVA2 Support for screen capture protection when DWM is off
        unsigned int FtrScreenCaptureDwm : 1;                    // DXVA2 Support for screen capture protection for DWM mode
        unsigned int FtrScreenCaptureAuxDev : 1;                 // Support for SCD through the auxiliary device
        unsigned int FtrNoiseFilter : 1;                         // Support Noise Filter
        unsigned int FtrDetailFilter : 1;                        // Support Detail Filter
        unsigned int FtrHDDVDCompositing : 1;                    // DXVA2 Support for HD DVD Compositing
        unsigned int FtrNLAScaling : 1;                          // Support Non-Linear Anamorphic Scaling
        unsigned int FtrNoPerSurfaceTiling : 1;                  // No support for per-surface tiling
        unsigned int FtrPAVP : 1;                                // Protected Audio Video Path enabled
        unsigned int FtrPAVPSerpent : 1;                         // Support PAVP serpent mode
        unsigned int FtrPAVP2VDBox : 1;                          // Enable PAVP for 2VDBox mode.
        unsigned int FtrPAVPWinWidevine : 1;                     // Enable Widevine drm mode.
        unsigned int FtrTranscodeAvcInHeavyMode : 1;             // Support AVC secured transcode in heavy mode
        unsigned int FtrTranscodeMpeg2InHeavyMode : 1;           // Support MPEG-2 secured transcode in heavy mode
        unsigned int FtrPAVPAllowAllSessions : 1;                // Support the full range of PAVP sessions
        unsigned int FtrPAVPIsolatedDecode : 1;                  // Enable PAVP Isolated Decode for BXT+
        unsigned int FtrHWCounterAutoIncrementSupport : 1;       // Enable HW counter read out for WiDi for KBL+
        unsigned int FtrPAVPStout : 1;                           // Enable PAVP Stout mode for KBL+
        unsigned int FtrPAVPOneOrOne : 1;                        // Enforce PAVP 1-or-1 (ID/Stout or Lite&Heavy)
        unsigned int FtrHDProcAmp : 1;                           // ProcAmp Control enabled for HD
        unsigned int Ftr3DMediaDefeature : 1;                    // Indicates whether 3D/Media is defeatured
        unsigned int FtrVC1NV12 : 1;                             // Decoding VC1 using NV12
        unsigned int FtrMPEG2NV12 : 1;                           // Decoding MPEG2 using NV12
        unsigned int FtrDynamicLinking : 1;                      // Dynamic Linking Support
        unsigned int FtrFastDIFilter : 1;                        // Fast MODEAST / FMD  for HD
        unsigned int FtrFFDNFilter : 1;                          // Fixed Function Noise Filter
        unsigned int FtrFFDIFilter : 1;                          // Fixed Function Advanced Deinterlacing
        unsigned int FtrDNUVFilter : 1;                          // Chroma Denoise Filter
        unsigned int FtrAVScaling : 1;                           // Adaptive Video Scaling
        unsigned int FtrIEFilter : 1;                            // Image Enhancement Filter (Detail)
        unsigned int FtrHDIEFilter : 1;                          // Image Enhancement Filter (Detail) for HD
        unsigned int FtrNestedBatchBuffer : 1;                   // HW CAP. Nested batch buffer for media object command
        unsigned int FtrHDEnhancedProcessing : 1;                // Support for HD Enhanced Deinterlacing/Denoise (FastDI+/DN+)
        unsigned int FtrEncodeAVC : 1;                           // Support for AVC ENC + PAK encoding.
        unsigned int FtrEncodeAVCVdenc : 1;                      // Support for AVC VDENC + PAK encoding.
        unsigned int FtrEncode16xME : 1;                         // Support for AVC ENC 16xME
        unsigned int FtrEncodeMPEG2 : 1;                         // Support for MPEG2 ENC + PAK encoding.
        unsigned int FtrEncodeMPEG2Enc : 1;                      // Support for MPEG2 ENC encoding only.
        unsigned int FtrEncodeVP8 : 1;                           // Support for VP8 encoding.
        unsigned int FtrEncodeVP9HybridPAK : 1;                  // Support for VP9 ENC + HyBrid PAK encoding.
        unsigned int FtrEncodeJPEG : 1;                          // Support for JPEG PAK encoding.
        unsigned int FtrEncodeHEVC : 1;                          // Support for HEVC encoding.
        unsigned int FtrEncodeHEVCVdencMain : 1;                 // Support for HEVC VDENC + PAK encoding. Main profile.
        unsigned int FtrEncodeHEVCVdencMain10 : 1;               // Support for HEVC VDENC + PAK encoding. Main 10 profile.
        unsigned int FtrEncodeHEVC10bit : 1;                     // Support for HEVC encoding 10 bit.
        unsigned int FtrEncodeHEVC10bit422 : 1;                  // Support for HEVC encoding 422 10 bit.
        unsigned int FtrEncodeHEVC444 : 1;                       // Support for HEVC encoding 444.
        unsigned int FtrEncodeHEVC10bit444 : 1;                  // Support for HEVC encoding 444 10 bit.
        unsigned int FtrEncodeHEVCVdencMain10bit422 : 1;         // Support for HEVC VDEnc encoding 422 10 bit.
        unsigned int FtrEncodeHEVCVdencMain444 : 1;              // Support for HEVC VDEnc encoding 444 bit.
        unsigned int FtrEncodeHEVCVdencMain10bit444 : 1;         // Support for HEVC VDEnc encoding 444 10 bit.
        unsigned int FtrDecodeOutputSync : 1;                    // Synchronize use of decoding output between 2 engines or contexts
        unsigned int FtrCPFilter : 1;                            // Color Pipe
        unsigned int FtrGamutExpansionMedia : 1;                 // Gamut Expansion for Media
        unsigned int FtrGamutCompressionMedia : 1;               // Gamut Compression for Media
        unsigned int FtrPreprocessing : 1;                       // Pre-Processing
        unsigned int FtrFastCopyInterface : 1;                   // Support for FastCopy interface
        unsigned int FtrCompositingRate30fps : 1;                // Compositing frame rate limited to 30fps
        unsigned int FtrVDIWalker : 1;                           // VDI Walker
        unsigned int FtrVFEWalker : 1;                           // VFE Walker
        unsigned int FtrConcurrentMultiSliceEncode : 1;          // Concurrent Multi-Slice Encode usinf Media Objects
        unsigned int FtrFrameRateConversion24p60p : 1;           // Frame Rate Conversion,24p->60p
        unsigned int FtrFrameRateConversion30p60p : 1;           // Frame Rate Conversion,30p->60p
        unsigned int FtrFrameRateConversionFullHD : 1;           // Frame Rate Conversion for Full HD (1080p)
        unsigned int FtrIStabAffineFilter : 1;                   // Image Stabilization Filter
        unsigned int FtrIStabFilter : 1;                         // Image Stabilization Filter
        unsigned int FtrS3D : 1;                                 // Stereoscopic 3D
        unsigned int FtrDisplayEngineS3d : 1;                    // Display Engine Stereoscopic 3D
        unsigned int FtrCm : 1;                                  // C for Media runtime support
        unsigned int FtrWidiCompose : 1;                         // WiDi compose interface support
        unsigned int FtrCinematicSync : 1;                       // WiDi feature: Supporting Cinematic Sync
        unsigned int FtrPatchWiDiBbWithLastFlippedAddress : 1;   // To allow WiDi BB patching at submit time with last flipped addresses.
        unsigned int FtrDesktopScreen : 1;                       // Desktop Screen interface support
        unsigned int Ftr3pPlugin : 1;                            // 3P Plug-in support (SNB+)
        unsigned int FtrHalfSliceSelect : 1;                     // select half-slice VME unit from IVB+
        unsigned int FtrDeringDeblockFilter : 1;                 // Deringing/Deblocking filter
        unsigned int FtrEncodeAVCMBBRC : 1;                      // Macroblock based Bit Rate Control
        unsigned int FtrVeboxParallelExecution : 1;              // MP vebox and render engine parallel execution
        unsigned int FtrCapturePipe : 1;                         // Capture Pipe from BDW+
        unsigned int FtrLensCorrectionFilter : 1;                // LGCA from SKL+
        unsigned int FtrHwSupportForFieldSeqS3D : 1;             // Hardware support for field sequential S3D from HSW onwards
        unsigned int FtrSFCPipe : 1;                             // Scaler & Format Converter Pipe from SKL+
        unsigned int FtrHCP2SFCPipe : 1;                         // HCP to SFC pipe
        unsigned int FtrDisableVEBoxFeatures : 1;                // LKF and platforms that VEBOX can only be used in bypass mode
        unsigned int FtrLace : 1;                                // Local Adaptive Contrast Enhancement from SKL+
        unsigned int FtrFDFB : 1;                                // Face Detection and Face Beautification from Gen8+
        unsigned int FtrRowstoreCachingEnabled : 1;              // Rowstore Caching for CHV+ LP platforms
        unsigned int FtrEnableMflDecoder : 1;                    // Multi Format Legacy Decoder
        unsigned int FtrEnableHuC : 1;                           // HuC is a programmable Microcontroller added to the VDBox pipeline
        unsigned int FtrHuCLoadingFromPPGTT : 1;                 // HuC FW is load from PPGTT rather than WOPCM, for non-PAVP platform like GWL.
        unsigned int FtrMemoryCompression : 1;                   // Media memory compression from SKL+
        unsigned int FtrEnableMediaKernels : 1;                  // Multi Format Legacy Decoder, HuC is a programmable Microcontroller added to the VDBox pipeline
        unsigned int FtrLegacyMediaKernelLoading : 1;            // Load Media kernels using crypto copy
        unsigned int FtrSliceShutdownOverride : 1;               // Registry Key Support for Slice Shutdown
        unsigned int FtrEncodeFlatnessCheck : 1;                 // Flatness check support
        unsigned int FtrEncodeMAD : 1;                           // Mean Absolute Difference
        unsigned int FtrVpDisableFor4K : 1;                      // Disable VP features for 4K
        unsigned int FtrMediaPatchless : 1;                      // Enable of patchless support in media for PIGMS.  Expected to be the same value of FtrPigms by default.
                                                                 // So GMM will initilize the flag after FtrPigms is finalized.  Currently implemented in GmmInitContext()
        unsigned int FtrMediaGpuMmuWithLimitedVa : 1;            // Enables GPU MMU for WDDM2.0 with limited VA space 2GB or 4GB
        unsigned int FtrForceSCISupport : 1;                     // Forced SCI over DSM from SKL+
        unsigned int FtrSingleVeboxSlice : 1;          // Indicate this production have single Vebox slice. SW HSD#5619023 and HW bug_de#2133079 for SFC is tied to VEBOX0.
        unsigned int FtrLaceDisableFor4K : 1;          // Disable LACE for 4K
        unsigned int FtrHDR : 1;                       // HDR content support from KBL+
        unsigned int Ftr360Stitch : 1;                 // 360 video stitch support from KBL+
        unsigned int Ftr10bitDecMemoryCompression : 1; // 10bit decode memory compression from ICL
        unsigned int FtrHcpDecMemoryCompression : 1;   // HCP pipeline decode memory compression from KBL
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
        unsigned int FtrAOTDRCSupport : 1;        // Array of Textures (AOT) and DRC support for SKL+
        unsigned int FtrEncodeVP9 : 1;            // Support for VP9 encoding 420 8 bit.
        unsigned int FtrEncodeVP9Vdenc : 1;       // Support for VP9 Vdenc encoding 420 8 bit
        unsigned int FtrEncodeVP98bit444 : 1;     // Support for VP9 encoding 444 8 bit
        unsigned int FtrEncodeVP9Vdenc8bit444 : 1;          // Support for VP9 Vdenc encoding 444 8 bit
        unsigned int FtrEncodeVP910bit420 : 1;              // Support for VP9 encoding 420 10 bit
        unsigned int FtrEncodeVP9Vdenc10bit420 : 1;         // Support for VP9 Vdenc encoding 420 10 bit
        unsigned int FtrEncodeVP910bit444 : 1;              // Support for VP9 encoding 444 10 bit
        unsigned int FtrEncodeVP9Vdenc10bit444 : 1;         // Support for VP9 Vdenc encoding 444 10 bit
        unsigned int FtrEncodeHEVCStill : 1;                // Support for HEVC Still Image encoding.
        unsigned int FtrEncodeHEVCVdencMainStill : 1;       // Support for HEVC VDENC + PAK encoding. Main profile Still
        unsigned int FtrEncodeHEVC444Still : 1;             // Support for HEVC encoding 444 Still
        unsigned int FtrEncodeHEVCVdencMain444Still : 1;    // Support for HEVC VDENC + PAK encoding. Main profile Still
        unsigned int FtrFenceIDRing : 1;                    // FenceID Ring Enable/Disable flag.
        unsigned int FtrEncodeHEVCVdencMainSCC : 1;         // Support for HEVC VDENC + PAK SCC extension 8 bit
        unsigned int FtrEncodeHEVCVdencMain10bitSCC : 1;    // Support for HEVC VDENC + PAK SCC extension 10 bit
        unsigned int FtrEncodeHEVCVdencMain444SCC : 1;      // Support for HEVC VDENC + PAK SCC extension 444 8 bit,
        unsigned int FtrEncodeHEVCVdencMain10bit444SCC : 1; // Support for HEVC VDENC + PAK SCC extension 444 10 bit
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
    };
    struct // Minute IA / GuC Related Features
    {
        unsigned int FtrEnableGuC : 1;              // Minute IA / GuC is enabled
        unsigned int FtrGucBasedPavp : 1;           // Support Guc Based Pavp
                                                    // Todo: Remove once feature is default in mainline
        unsigned int FtrGuCDistributedDoorbell : 1; // Support for Gen12 Distributed doorbell DCN
        // Todo: Remove once Fulsim is ready with complete DDB drop
        unsigned int FtrGuCDDBGT2LimitedConfig : 1; // Support for Fulsim Phase 1 GT2 ;128 doorbell config supported
    };

    struct // Security features
    {
        unsigned int FtrKmSecurityParser : 1;
    };

    struct // Win8 optional features
    {
        unsigned int FtrOsManagedHwContext : 1;
    };

    struct // Feature to Enumerate Camera Device as Child of GFX
    {
        unsigned int FtrEnableISPChild : 1; // Adds camera as child of Graphics.
    };

    struct // Virtualization features
    {
        unsigned int FtrVgt : 1;
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
} SKU_FEATURE_TABLE, *PSKU_FEATURE_TABLE;

#if defined(__clang__)
#pragma clang diagnostic pop
#elif defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

#endif // defined(_USC_)

//********************************** WA ****************************************

#define WA_DECLARE(wa, wa_comment, wa_bugType, wa_impact, wa_component) unsigned int wa : 1;

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

// Workaround Table structure to abstract WA based on hw and rev id
typedef struct _WA_TABLE
{
    // struct _wa_Sv

    WA_DECLARE(WaIncreaseDefaultTLBEntries, "WA for a improve performance of OCL benchmark(Luxmark) by increasing TLB entries", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisSvClkGating, "WA_DISABLE_SV_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_MASF_ClkGating, "WA_DISABLE_MASF_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_ISC_ClkGating, "WA_DISABLE_ISC_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_VFE_ClkGating, "WA_DISABLE_VFE_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_Clipper_ClkGating, "WA_DISABLE_CL_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_VF_ClkGating, "WA_DISABLE_VF_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_GS_ClkGating, "WA_DISABLE_GS_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTempDisableDOPClkGating, "Temporarily disable DOP Clk gating while changing L3SQCREG1 value", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_RCPH_RCC_RCZ_ClkGating, "WA_DISABLE_RCPH_RCC_RCZ_CLK_GATING", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable_ECOSKPD_Chicken_Bits, "WA_DISABLE_ECOSKPD_CHICKEN_BITS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    // struct _wa_2D
    unsigned int : 0;

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

    WA_DECLARE(WaNonPipelinedStateCommandFlush, "or else blitter-to-renderer won't flush before pipe-control", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIlkEnableBothDispAndSPR, "WA for MBM Hardware Issue 2208943", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLoadHDCPKeys, "WA for HDCP Key Load issue on A stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaExtendedWaitForFlush, "Wa for Extended wait on ring buffer to idle.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaKVMNotificationOnConfigChange, "Wa to Notify KVM only if config changes. KVM was getting notified erroneously on reads too.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaSNBIPLLaneCountSwitch, "Temporary WA for HW issue in switching lane count within x1, x2 & x3", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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
    unsigned int : 0;

    WA_DECLARE(Wa2DNegativeStart, "WA_2D_NEGATIVE, negative destination", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNoAsyncFlip, "WA_NO_ASYNC_FLIP, WA for Almador A5, need to always set", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaBatchBufferForWaitOnEvent, "WA_USE_BATCH_BUFFER_FOR_WAIT_ON_EVENT for 2nd sprite on Almador", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOvlFastHDownScale, "WA_OVERLAY_DOWN_SCALE on BDG", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOverlayPitch, "WA_OVERLAY_PITCH on Almador and BDG", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableVblank, "WA_ENABLE_VBLANK on Almador", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(Wa2ndSpritePanning, "WA_PANNING_SECOND_SPRITE, No 2nd Sprite panning when overlay is panning", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOvHunitCounter, "OVHunit counter reset fails after >= 16x downscale (Alm family)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOvlPipeSwitching, "PipeSwitching overlay fails for napa family (sighting #54180)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPackedtoPlanar, "8 bit linear depth buffer broken (sighting #65500)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDdbmunitClkGating, "Overlay hangs on 63rd overlay flip CEG Tibet #1963931 Crestline A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    // struct _wa_ocl
    unsigned int : 0;

    WA_DECLARE(WaOCLDisableMaxThreads, "Max simultaneous threads are limited to 1 until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLDisableBarriers, "Barriers are not supported until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLDisableImageWrites, "Image writes are not supported until SNB C0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLDisableA64Messages, "A64 Messages are not supported on BDW A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLLimitCurbeSize, "Limit the CURBE size for IVB A0 GT2 Only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLAddMSFlushForPreemption, "( Bpsec ) DevHSW:A0 only: There should be two media state flush commands in a row for this stepping to ensure proper preemption",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLEnableFMaxFMinPlusZero,
               "Enable FMax(x+0, y+0)/FMin(x+0, y+0) for BDW A-step Only. In OCL, FMin/FMax behave not match the IEEE 754 with regard to signaling NaN. Specifically, FMax(0, "
               "SNaN) = 0. While, on BDW A-step, it is IEEE-compliant:  FMax(0, SNaN) = QNaN. @                   Thus, FMax(0, SNaN) ==> FMax(0+0, SNaN+0) = FMax(0, QNaN) = 0",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaOCLUseLegacyTiming, "SKL A0 needs to use escape calls to get GPU timing (and must disable preemption)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCohPWmergeDisable, "Disable HDC PWmerge if workload uses coherent accesses", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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
    unsigned int : 0;

    WA_DECLARE(WaStallBeforePostSyncOpOnGPGPU, "In the GPGPU pipeline, insert a PC with a CS stall before any PC with a post sync op.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceCsStallOnTimestampQuery, "Sets the CS stall bit in the pipe control that issues the timestamp query", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceCsStallOnTimestampQueryOrDepthCount, "Sets the CS stall bit in the pipe control that issues the timestamp query or depth count", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceRCPFEHangWorkaround,
               "Enable Depth Stall on every Post Sync Op if Render target Cache Flush is not enabled in same PIPE CONTROL  and  Enable Pixel score board stall if  Render target "
               "cache flush is enabled.",
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

    WA_DECLARE(WaDisable_WIZUnit_ScratchSpace, "Set max scratch space as 12KB (BWG A0, Source: Michael Apodaca)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaVSHWBug_Option1_DisableVertexCache, "VS HW bug.  HSD 300136, option 1 - Disable Vertex Cache", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(Wa_CS_URB_STATE_Hang, "Send CS_URB_STATE command to h/w twice to prevent subsequent ring hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUseMediaEngineForPaging, "Use Media Engine to do paging transfers.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaInitAuxBuffersToTiled, "WA for intermediate Z issue to initialize aux buffers to tiled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableRenderCachePipelinedFlush, "Disable Render Cache Pipelined Flush for Cantiga/Eaglelake (set bit 8 of 0x2120)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaVertexShader96And128CacheEntries, "Disable use of 96 or 128 vertex shader URB/cache entries", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaCSStallOnAllPipeControls, "Set CS stall on all PIPE_CONTROL commands (HSD sighting 3639613)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaMultisampledArrays, "Render engine and sampler have mismatch when indexing nonzero array slice", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable128bppRTClears, "SNB WA to disable 128bpp render target clears.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGsPsdHang, "limit max GS threads when rendering is enabled (HSD bug_de 3047711)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceThreadSwitchWhenUpdateMRFBeforeSend, "WA for EU dependency HW bug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushAfterPerspectiveDivideStateChange, "Non-pipelined flush after perspective divide state change (HSD sighting 3715225)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableSampleFromStencil, "Wa - Cannot sample from or disable separate stencil on IVB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaReadAfterWriteHazard, "Send 8 store dword commands after flush for read after write hazard (HSD Gen6 bug_de 3047871)", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMadSrc0Replicate, "WA disables replication for src0 in MAD instruction (HSD 3639565)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaUseOnlySIMD8UntypedRead, "Use only SIMD8 for Untyped Surface Read and Untyped Imm Atomic messages. IVB HSD bde3378886.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMscWithGS, "WA for IVB HSD 3664439 on A0 MCS unit is calculating incorrect VA when r2t is enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSurface3DForceHorizontalAlignment4, "Force horizontal alignment of 4 for 3D surfaces. IVB HSD Bug_DE 3664432", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUVoffsetToZeroForLd2dms, "WA for IVB HSD 3378967 on A0 MSC resolve test shows corruption when ld2dms instruction. with u v offset not zero",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaUnlitCentroidInterpolation, "WA for IVB HSD 3665165. The centroid interpolation is not right for unlit pixels.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMcsForSINTFormat, "WA for IVB HSD 3665244. Disable Mcs for SINT formats", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAddCallToEOTEnabled, "WA for IVB HSD 3664649 - Place call to EOT instruction at the end of shader with function calls", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAlignDrawScissorRectTo2x2MSAA, "Drawing rectangle and scissor rectangles must be 2x2 aligned when MSAA is enabled (Gen6 sighting 3716147)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTimestampMaskDefectiveBits,
               "The highest significant bits of the 1st DWORD of the Timestamp register value are frequently destroyed. (HSD gesher sighting 3716223)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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
               "WA for BDW/CHV, SKL A0-B0 - VertexReordering for OGL GS for TRIANGLESTRIP_ADJACENCY input topology only, the same software reordering WA as "
               "WaOGLGSVertexReordering but enabled only for one topology",
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
               "(exact number of bits depends on number of samples from above, example 2X = sample mask 0x3 and so on) - pixel shader dispatch mode needs to be set to \"per "
               "pixel\" - we do not program UAV only mode bit (leave it at zero) - we enable RTTIR rasterization",
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

    WA_DECLARE(WaL3UseSamplerForVectorLoadScatter,
               "WA for Apple Cascaded_Shadow_Map test to avoid L3 Constant Cache problems on IVB - it replaces LOADSCATTEREDCONSTANT instructions which are Vectors with "
               "LOADSCATTEREDCONSTANT_SAMPLER instruction, which is sampler SIMD8/SIMD16 LOAD with response length 4/8. It also merges LOADSCATTEREDCONSTANT instructions "
               "differing only by ConstantBufferChannel to one LOADSCATTEREDCONSTANT_SAMPLER instruction and removes SHL instruction before them, since sampler LOAD has oword "
               "granularity and SHL is not needed.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(Wa1DSurfaceSIMD4x2ArrayIndexInRAddress,
               "SurfaceArray bit is always set in SurfaceState on IVB and HSW. Resinfo's results should be adjusted as well as sampler's address in channel parallel. For 1D "
               "surface type SIMD4x2, the array index must be placed in R address parameter instead of the V address parameter.",
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

    WA_DECLARE(WaNotifRegSwapInGpGpuContextRestore, "Swap n0.0 and n0.2 registers in preemption context restore.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaStoreSlmOffsetInSRDuringGpGpuPreemption,
               "SLM Offest isn't stored by H/W context during preemption, when WA is enabled gpgpu SIP kernel preserves SLM Offset during in preemption.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSampleGCToSampleLC, "WA for IVB, SAMPLE_G_C is not supported. Change to SAMPLE_LC with Lod computed from gradients.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaResetMSAAStates, "WA for SNB Q0, need to reset MSAA states at the end of every batch buffer to avoid issues in media workload", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCMPInstNullDstForcesThreadSwitch, "CMP instructions with NULL destination needs to have Thread Switch enabled (Cloned from IVB GT2 HW WA 3665996)",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaFlushWriteCachesOnMultisampleChange, "WA for BDW HSD 1897292, flush depth and render caches on Multisample change", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceTypeConvertF32To16ToAlign1, "WA for BDW HSD 1898640, type convert F32To16 is not allowed in Align16, must be done in Align1", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAdditionalMovWhenSrc1ModOnMulMach, "WA for BDW to support source modifiers on src1 when using mul/mach macro", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceMulSrc1WordToAlign1, "WA for CHV to produce only Align1 mul instructions when src1 type is :w", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDoNotPushConstantsForAllPulledGSTopologies,
               "SKL, BXT: 'Dispatch GRF Start Register For URB Data' state for the GS is too small to adress GRF bigger than 15, so constants can not be pushed when more than 14 "
               "(13 in case of PrimID existance) vertex handles for pulling are input for GS",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCallForcesThreadSwitch, "WA for BDW call instruction needing Switch thread control", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaThreadSwitchAfterCall,
               "BDW, CHV, SKL, BXT: Follow every call by a dummy non-JEU and non-send instruction with a switch for both cases whether a subroutine is taken or not",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableSIMD32PixelShaderDispatchFor2xMSAA, "WA to disable SIMD32 PS dispatch for BDW A0 only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WANOPBeetweenIndirectAdressingAndBranch, "WA to add NOP beetween indirect data instruction and control flow instruction.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDX9MSAAonDX10HW,
               "Wa to notify the DX9 UMD to shift the SF viewport for DX9 MSAA on DX10 HW.  Feature isn't necessary on HSW+ as the HW now supports this.  HW support exists in "
               "HSW+, but the bit is not properly context save/restored for A stepping so we need to use the traditional behavior.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaInvalidateAndHDCDeadlock,
               "WA for HSW, PIPECONTROL with RO Cache Invalidation: Prior to programming a PIPECONTROL command with any of the RO cache invalidation bit set program a PIPECONTROL "
               "flush command with CS stall bit and HDC Flush bit set.  3D_STATE_BASE_ADDRESS : Prior to programming a 3D_STATE_BASE_ADDRESS command program a PIPECONTROL flush "
               "command with CS stall bit and HDC Flush bit set.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaL3WriteIncomplete, "WA for HSW, send a data cache flush after any draw or dispatch with a UAV.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaMiUrbClearAfterMiSetContext,
               "WA for IVB & HSW - the order in which the L3Config registers and the MI_URB_CLEAR happen durring a HW context restore is incorrect.  The MI_URB_CLEAR occurs "
               "before the L3Conig registers have been restored.  Yet the L3Config registers contain the info necessary for HW to clear the correct part of the URB area.  The WA "
               "for this is to reissue the MI_URB_CLEAR after the MI_SET_CONTEXT completes since the L3Config will have been restored by that time.",
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

    WA_DECLARE(WaForceClearBindingTableEntries, "Forces clearing the HW-generated binding table entries by manually editing each entry.", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLimitMaxPSThreadsToPhysical, "WA for HSW: limit max PS threads to physical threads in system.  70 for GT1, 140 for GT2, 280 for GT3.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLimitMaxHSUrbHandles, "WA for BDW: limit max HS Urb Handles programming to 184 due to FIFO size issue with DS.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaA32StatelessMessagesRequireHeader, "Need to include a header for all A32 stateless messages.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNoA32ByteScatteredStatelessMessages, "Use A64 byte scattered stateless messages instead of A32 byte scattered stateless messages.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNearestFilterLODClamp, "If mipfilter_nearest, MaxLOD = floor(MaxLOD) and MinLOD = floor(MinLOD)", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSingleSubspanDispatchOnAALinesAndPoints, "If AALines/AAPoints, HALF_SLICE_CHICKEN1 : 0E100h[10] = 1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLSLMAddressDisable, "B2b atomics to the same address with a bubble in between is not bieng handled correctly in LSLMunit", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPipelineFlushCoherentLines,
               "B2B Walkers one using BTI 255 Coherent and other using BTI 253 Non-coherent using same surface we need flush Cohrent Lines in between", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(
    WaBasicCompilationForDPInstructions,
    "Perform double precision calculations with pre-BDW specific algorithm. Since BDW-B0 platform double precision calculations will be perform with new MADM instructions.",
    WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaHalfFloatSelNotAllowedWithSourceModifiers,
               "In LIR instructions that convert to floating-point sel (FSEL, FMIN, FMAX) we raise precision from 16b to 32b when some modifiers (negation or absolute values) is "
               "used on sources. Alternatively additional MOV-s could be generated to perform these operations.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLowPrecWriteRTOnlyFloat, "16-bit render target write can be used only with float data type, not int/uint.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaBreakF32MixedModeIntoSimd8, "SIMD16 instruction not allowed when using mixed mode and destination type is float. Must be broken into 2 x SIMD8.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaEmitVtxWhenOutVtxCntIsZero,
               "Force output vtx cnt = 1 to avoid a GS hang in case static output is 0 and Control Data Header Size>0 and output vtx cnt = 0. RTL will drop partial object for all "
               "topologies.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCsStallBeforeURBVS, "Prevents a potential state thread data corruption by inserting a pipe control with CS stall bit set before any 3DSTATE_URB_VS command.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAlignIndexBuffer,
               "Force the end of the index buffer to be cacheline-aligned to work around a hardware bug that performs no bounds checking on accesses past the end of the index "
               "buffer when it only partially fills a cacheline.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuardbandSize, "Resize the dimensions of the guardband to -16K,+32K in both X and Y", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRCCByteSharingDisableFor3DRT, "Disable RCC Byte-Sharing for RT with Surface Format = 3D", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable4x2SubSpanOptimizationForDS, "Disable 4x2 subspan optimization for singlesample RT with depth enable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFixCentroidInterpolationRTIR16X, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIndirectDataForGPGPUWalker,
               "Indirect data usage for payloads on Media pipe is broken for A0 on BDW.To prevent hang/corruption, avoid using Indirect data for walker.",
               WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIndirectDataAndFlushGPGPUWalker,
               "Issue with too many entries causing a hang, solution to always use CURBE_LOAD & wrap with a MI_ATOMIC when too many entries.",
               WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIndirectDataForIndirectDispatch,
               "Indirect data usage for payloads on Media pipe is broken on BDW.To prevent hang/corruption, GPGPU walker needs to use only curbe while doing indirect dispatch",
               WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSendMediaStateFlushAfterGPGPUWalker,
               "TSG is not sending the preemption down to TDG in GPGPU Walker mid-thread preemption with MMIO writes. To prevent a potential hang, this fix sends a "
               "MEDIA_STATE_FLUSH with the Flush to GO bit set after each GPGPU_WALKER.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDeferredDeallocation, "WA to DisableDeferredDeallocation", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePushConstantHSGS,
               "Feature: Dereference for HS in TDL. To prevent a potential hang, a dispatch pull model must be forced for HS,GS with push constant use or just disable push "
               "constant for HS and GS.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableAllWriteChannelMask, "Pixel Corruption (X's) in main path for point sample under special conditions.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGather4WithGreenChannelSelectOnR32G32Float,
               "When issued a gather4 instruction with channel select green on R32G32_FLOAT/R32G32_UINT or R32G32_SINT Sampler will return the Red channel instead of the selected "
               "Green channel. For Haswell the workaround is to use the resource swizzle .RBBB. The workaround will be applied only if gather4 is the only instruction type "
               "associated with the resource type.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaStateBindingTableOverfetch,
               "HW over fetches two cache lines of of binding table indices.  When using the resource streamer, SW needs to pad binding table pointer updates with an additional "
               "two cache lines.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIncreaseL3CreditsForVLVB0, "L3Sqc Register will be having a different value from VLVB0.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUAVCoherency, "Must use pipe control with cs stall and dc flush to maintain uav coherency if any fixed function besides PS requires UAV coherency",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisableObjectLevelPreemptionDuringUAVDrawCall,
               "VF holds CS during pre-emption request. To prevent a potential hang, this fix notifies KMD of a Draw call which utilizes UAV so that they can disable Object level "
               "Pre-emption.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushBefore3DStateConstant, "Insert pipe control flush before push constant state change.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSendExtraRSGatherConstantAndRSStoreImmCmds, "Send extra RS Store Immediate, GatherConstant and 3DConstant cmds to stall CS reads until writes by RS are committed",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNoPreemptionWhenBarrierEnabled, "Disable preemption if barrier is used in compute shader kernel. Only affects GT1.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePreemptionMMIOWhenBarrierEnabled, "Disable preemption if barrier is used in compute shader kernel. Uses MMIO pre-emption enable/disable.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAvoidRCZCounterRollover, "Must send CCStatePointers at the end of a batch buffer and after 3D preemption to avoid RCZ counter rollover and HW hang",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPreemptOnArbCheckOnly, "WA for SNB HSD #3716501 - Use 32bpp WM with FBC enabled in 16bpp mode", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTSGStarvation, "WA for TSG Starvation Issue thats fixed in BDW E stepping", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaInhibitPreemptionForOCLProfiling, "WA for OCL Profiling Preempt - BUG_DE 1911601", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaMediaStateFlushBeforePipeControl, "GPGPU Preemption requires MSF without Flush2GO before any pipe control", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUAVDisableMinimumArrayElement,
               "HW is not able to write to an UAV with MinimumArrayElement > 0 on IVB and VLV. Workaround is to program the SurfaceOffset for every array element manually instead "
               "of HW calculating the offset.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableNonSlm, "WA to avoid turning off SLM for power saving", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(Wa4x4STCOptimizationDisable, "Disable 4x4 RCPFE-STC optimization and therefore only send one valid 4x4 to STC on 4x4 interface.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableKernelDebugFeatureInHWUsingCsDebugMode1, "WA to enable kernel debug feature in HW as CS_DEBUG_MODE1 is set to non-privileged", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnsureMemCoherencyBeforeLoadRegisterMem,
               "Any updates to the memory location exercised by MI_LOAD_REGISTER_MEM command must be ensured to be coherent in memory prior to programming of this command. This "
               "must be achieved by programming 16 dummy MI_STORE_DATA_IMM (write to scratch space) commands prior to programming of this command for pre-BDW and MI_ATOMIC (write "
               "to scratch space) with CS STALL set prior to programming of this command on BDW and CHV",
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

    WA_DECLARE(WaPerCtxtBbInvalidateRoCaches, "Invalidate all RO caches via pipe control in per context batch buffer (as per bspec)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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
    WA_DECLARE(WaAvoid16KWidthForTiledSurfaces, "WA for HW bug: Max tiled surface width can only be 16K-2", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableRsInPostRestoreWaBb, "WA for CNL hang while executing RS enabled WA BB during context restore of a preempted RS enabled batch.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaInsertGSforConstInterpolatedTrailingVertex,
               "Insert pass-through GS when rendering a triangle strip and PS uses const interpolated attributes from trailing vertex.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

    WA_DECLARE(WaForceCB0ToBeZeroWhenSendingPC, "Force constant buffer 0 to be null and use constant buffer 3 instead", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_OGL)

    WA_DECLARE(WaDefaultCrossAndSubSliceHashingForSimplePS,
               "Performance fix applied for GEN10+, when PS is simple enought cross slice hashing require to be forced to 32 x 32 and sub slice hashing to be forced to 16x16 and "
               "3DSTATE_PS_EXTRA bit has to be lit to indicate if this is a small shader",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

    WA_DECLARE(WaResetPSDoesNotWriteToRT, "Setting PSDoesNotWriteToRT bit in 3DSTATE_PSEXTRA cause issue with occlusion query samples_pass results when PS is discarding pixels",
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

    // struct wa_PwrCons
    unsigned int : 0;

    // Temp WA
    WA_DECLARE(WaPcSlpcUseBxtGucBinaryVer1219, "Temp WA on BXT to use the old guc binary until key signing issue is resolved", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    // Todo: Change this workaround with a finer level workaround conditions
    WA_DECLARE(WaRccHangDisableMCSUnrefined, "Disable MCS through Chicken bit. Need to refine the wa condition.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableGafsUnitClkGating, "Disable GAFS unit clock gating to avoid BGF corruption which results in TDR", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaToEnableHwFixForPushConstHWBug, "WA is needed to enable HW fix for push constant issue", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    // BLC
    WA_DECLARE(WaBlcOutputHighInverterPWMFreq, "WA for HSD #5262786 - Allows display engine to output high PWM frequency by not ensuring minimum 101 achievable brightness steps.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    // FBC
    WA_DECLARE(Wa32bppWmWithFbc, "WA for SNB HSD #3716501 - Use 32bpp WM with FBC enabled in 16bpp mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcAsynchFlipDisableFbcQueue, "WA HSD#1114573, BUN#09ww04", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcDisabledForOverlaySprite, "WA BUN#08ww29.1 FBC can not be enabled when Overlay/Sprite on", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcLimitedTo1MBStolenMemory, "WA FBC size limited to 1 MB stolen memory size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcOnlyForNativeModeOnLFP, "WA BUN#08ww34.1 - Enable FBC for native mode on LFP only", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcOnly1to1Ratio, "CTG/ILK hw - WA BUN 2073_di5vk69m/HSD2955233 - Only use FBC compression 1:1", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcDisableDpfdClockGating, "WA for ILK HW HSD #1114788", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcDisable, "WA to disable FBC feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcDisableDpfcClockGating, "WA for SNB HW HSD #3715402", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcFlickers, "WA for ILK HW HSD #3573465", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableFbcOnFixedMuxless, "Power data shows benefit when enabling FBC during fixed muxless SG on certain platforms.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcWaitForVBlankBeforeEnable, "WaitForVBlank before enabling FBC to avoid white lines and/or hangs during S3/mode switch", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcNukeOn3DBlt, "BUN 2831472 for various FBC corruption issues IVB HW# 3925243, #3925761", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcExceedCdClockThreshold, "Disable FBC when Pixel clock exceeds 95% of CD clock to avoid corruption HSW HW# 3745290", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcCdClkFreqTooLow, "FBC may cause corruption when the pixel rate is greater than the cdclk frequency. Either increase the cdclk frequency or disable FBC.CNL:A0",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcDisableRleCompressionForVTD, "Disable RLE compression above 2K lines BDW HW#4394320", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIpsDisableOnCdClockThreshold, "Disable IPS when Pixel clock exceeds 95% of CD clock to avoid corruption HSW HW# 1912230", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcRequireStrideBeMultipleOfCompressionRatio, "https://vthsd.iind.intel.com/hsd/gen9lp/default.aspx#bug_de/default.aspx?bug_de_id=2127304 ",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaFbcWakeMemOn, "Set ARB_CTRL bit 31 FBC Memory Wake to 1'b1 for better idle power savings", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcSkipSegments,
               "Skip compressing 1 segment at the end of the frame, avoid a pixel count mismatch nuke event when last active pixel and dummy pixel has same color for Odd Plane "
               "Width / Height",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcTurnOffFbcWhenHyperVisorIsUsed, "https://vthsd.fm.intel.com/hsd/mpg_customer_enabling/sighting/default.aspx?sighting_id=5022343", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFbcNukeOnHostModify, "https://hsdes.intel.com/home/default.html#article?id=1404569388", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFixR32G32FloatBorderTextureAddressingMode, "Fix sampling from R32G32_FLOAT surfaces when using border texture addressing mode", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIPS, "WA to disable IPS feature", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIpsWaitForPcodeOnDisable, "WA to wait for pcode to disable IPS before disabling the display plane (HSD 4393936)", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIpsDisableOnAsyncFlips, "WA to disable IPS on asyc flips to improve frame rates in 3D apps.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPsrExitBlockedOnFbcNuke, "W/A WaFbcNukeOn3DBlt prevents PSR from exiting self refresh", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGsvGtFreq200MhzMultiple, "W/A Driver to make sure requested a GT freq is multiple of 200Mhz", "GT hang", WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGsvBringDownFreqInRc6, "W/A Driver to set RPe when enters RC6", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaRsForceSingleThreadFW, "Use Single Thread Froce Wake Algorithm when Force Wake is set to Multi-threaded mode in HW.  Sighting was found in SV OS.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRsDisableDecoupledMMIO, "Disable decoupled MMIO mechanism and use regular SW forcewake for MMIO register access because of slowness.", WA_BUG_TYPE_PERF,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRsClearFWBitsAtFLR, "Initialize by clearing all FW bits when driver loads before setting any forcewake request.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSyncSameMMIORegAccess, "Synchronization fix for System hang when two cores try to use same MMIO Register", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_PWRCONS)

    WA_DECLARE(WaRsDoubleRc6WrlWithCoarsePowerGating, "Double RC6 WRL when Coarse Power Gating is Enabled", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_PWRCONS)

    WA_DECLARE(WaRsDisableCoarsePowerGating, "Disable coarse power gating for GT4 until GT F0 stepping.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFidMismatch, "Disable PwrCons Features RC6 and Turbo which require Punit interaction if FID mismatch.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDpstDisableDlcdGating, "Disable DLCDunit Gating  as a WA for issue that Guardband interupt status bit enabled sporadically when Guardband interupt enabled.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIpsEnableOutsideOfVblankRegion,
               "Enforce IPS enable to be outsite VBLANK to workaround corruption seen when the primary plane is enabled/disabled at the same time that IPS is enabled",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(
    WaIpsEnableOnMediaPlaybackOnly,
    "There is currently a power inversion problem with IPS. Power savings with IPS is seen only in media workloads. Enable IPS during media playback only as a workaround.",
    "Power inversion", WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIpsDisableOnPaletteAccess,
               "There is a hardware hang when split gamma mode is enabled and pipe gamma/palette data is accessed while IPS is enabled. This workaround disables IPS before "
               "accessing the gamma/palette registers in split gamma mode.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    // General
    WA_DECLARE(WaUsePipeAFlipTimestamp, "WA to use 7004C as timestamp for ILK A Stepping WA", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTurboEnergyCounterMask, "Energy counters bits are changed from ILK C0.  Wa flag is to use old values on A and B stepping.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRc6Ppgtt, "WA to prevent page table error when RC6 and PPGTT are both enabled at the same time.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLaceIEModeLUT, "Use LUT mode of LACE image enhancement as multiplier mode is not supported.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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
    unsigned int : 0;

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

    WA_DECLARE(WaFlushGWBBeforeReads, "WA for flushing GWB before any memory read updated by HW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableSnoopOnCacheWriteCyl, "Wa to disable snoop on cachable write cycle", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable36BitPhysAddress, "Wa to disable 36 bit physical address", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUpdateOnCacheLineBoundary, "Wa to pad memory so updates occur on cache line boundaries.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUpdateBCSOnCacheLineBoundary, "Wa to pad memory so updates in BCS RING occur on cache line boundaries.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableCSUnitClockGating, "Wa to disable clock gating in CS unit", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnablePhysAddrForMiInstr, "Wa to enable physical address for MI instruction", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(Wa_Disable_C0_Fix_For_Req_Perf, "Wa to Disable Crestline C0 fix for requests performance", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableCrClkThrottlingDuringC2, "Wa to Disable BL_B CR CLK Throttling during C2 power state", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaInitStopRenderWatchdogCounter, "WA to stop the initially running main engine watchdog counter", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisableTDSandwichDispatchMode, "WA to disable sandwiching of threads by TD. ILK DW DCN 2379515", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableNonLRAReplacementPolicy, "WA to disable LRA replacement policy by STCUnit. ILK DW DCN 2378954, 2379200", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableRCZMUnitClockGating, "WA to disable RCZ unit clock gating ILK HW DCN 2379651, 2379638", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisableSVSMUnitClockGating, "WA Disable SVSM unit clock gating ILK HW bug 2379811 and BSpec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaNoPipelinedURBFenceChange,
               "Don't allow pipelined URB_FENCE commands by placing MI_FLUSH in front and dummy PRIM and second URB_FENCE after  ILK sighting 3573145.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaValign2ForR8G8B8UINTFormat,
               "sampler format decoding error in HW for this particular format double fetching is happening, WA is to use VALIGN_2 instead of VALIGN_4", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushBefore3DPrimIfTopologyFilterEnabled, "Send PIPE_CONTROL with posy-sync op before every 3dprim if topology filter is enabled.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT(0.5), WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDummyRenderForAdderIssueXP, "Issue a dummy render for 3d pipeline after comming back from 0 volts.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaB2BPipeControlFlush, "No description provided", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLimitGsUrbToTop256kb, "GS can only occupy top 256kb of URB.", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT(1), WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePSDDualDispatchEnable,
               "When tessellation is enabled, set MMIO 0x0E100 and 0x0F100 to 0x80008 (PSD Single Dispatch Port Enable) to avoid hang. This is for GT1 only.(IVB bug_de 3925871). "
               "This is also for VLV/VLVT (bug_de 261436).",
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

    WA_DECLARE(WaEnableGunitDisplayInterruptMask, "Enable the GUnit mask for forwarding the display interrupts to GT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT(0),
               WA_COMPONENT_UNKNOWN)

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
               "Program MI_LOAD_REGISTER_IMM command twice when exercising non-privilege register writes. OR Ensure all dwords of MI_LOAD_REGISTER_IMM command including header of "
               "the command gets programmed in a single cacheline (64B).",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAvoidStcPMAStall, "SKL HSD: 731063. Starting with A0.  Avoids stencil PMA stall.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT(60), WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAvoidStcPMAStallShaderFiltering, "Filter shaders allowed to use WaAvoidStcPMAStall.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    // struct __wa_KMD_render
    unsigned int : 0;

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

    WA_DECLARE(WaDisableRc6OnWaitForEvent, "WA to disable Rs2 on Wait for event in the RCS. IVB A0 HW: 3378975.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableAllByteWritesForLRI, "WA to enable all bytes. Using byte enables causes a hang on IVB A0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAlwaysClearIndirectStatePointersDisable, "WA to always keep ISPDisable as false. IVB A0.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLoadDummyCB2, "WA to send dummy CB^2 on pre SNB D0 steppings, else Clear Buffer will cause HW hang.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableLRIPostedOverrideBit, "WA for IVB bug 3664435.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaL3RowRedundancyUnavailable, "L3 row redundancy not available to driver since being used by BIOS for IVB A0 WA.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaL3ErrorRegistersInHwContext, "L3 error registers are stored in HW context (which complicates SW's L3 row reconfiguration ability).", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAdditionalMiUserIntCmdNeeded, "WA to add additional MI_USER_INTERRUPT command for Lateral BLTs", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaAllowUMDToModify3DPrimitiveExtParam, "WA to allow UMD to program 3D primitive extended parameters.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaBindlessSamplerStateBoundsCheckingDefeature,
               "WA for Bindless Samplers to defeature bounds checking for Bindless Sampler State Heap. Bounds check is at wrong granularity.", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableGatherAtSetShader, "There are RS hangs due to CS restore happening in parallel with RS restore. The fix requires not to disable 'Gather at Set Shader'.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

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

    WA_DECLARE(WaThrottleEUPerfToAvoidTDBackPressure, "WA for a hang issue that requires throttling EU performace to 12.5% to avoid back pressure to thread dispatch",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT, WA_COMPONENT_KMD)

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

    WA_DECLARE(WaPushConstantDereferenceHoldDisable, "WA to disable hold of push constant dereference.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaAllowUMDToControlCoherency, "WA to allow UMD to control coherency.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaPocsOvrRestart, "WA to HW issue if 3DSTATE_PTBR_PAGE_POOL_BASE_ADDRESS is executed within 256 clocks after the context restore is done", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableMSCunitClkGating, "Clock gating Bug in MSC for PTBR feature", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisCtxReload, "HW Issue with VTD mode ON and IOTLB invlidation", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaProgramMgsrForL3BankSpecificMmioReads, "Shadow Reg 119 (MGSR) needs to be programmed appropriately to get the correct reads from specific L3 banks related MMIOs",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

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

    WA_DECLARE(WaIncorrectSampleInfoPaletteIndex, "HW Bug 2877676 SampleInfo returns incorrect palette index.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCubesAreNot2DArray, "Memory layout of cubes is not same as 2D array", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushOnMaxNumberClipperThreadsChange, "WA to insert MI_FLUSH when max number of clipper threads change - DCN726186", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisablePixelShaderPushConstants, "HW Bug 2944932: Disables Pixel shader push constants (CURBE)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaVcsBcsQwordWriteCacheLineAlignment,
               "HW Bug 2877845, 2878101: address for qword writes in MI_STORE_DATA_IMM, STORE_DATA_INDEX, and MI_FLUSH_DW must be 64B aligned", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPipeControlBeforeWmMaxThreadCountChange, "HW Bug 2877574: must issue pipe control after changing max thread count in 3DSTATE_WM", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNopWithIdWriteAfterLastFlush, "An MI_NOOP with NOP_ID bit set must be programmed after the last MI_FLUSH_DW before head = tail on VCS and BCS",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaOverlaySynchViaVblank, "In Ctg/Elk we use VBlanks to report completion of sprite flips", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaFlushAfterCubeTexCordClamp, "Flush after every 3Dprim that uses a cube map with address ctrl mode TEXCOORDMODE_CLAMP.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRSPushConstantCoherencyBug, "Coherency issue seen on Si. SW W/A proposed and mostly will remain permanent.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRSStoreDataImmDeadlock, "This one is only specify to OGL usages, this was really a WA to allow OGL to use the RS for constant creation and gathering.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePerfMonGathering, "Reading of perfmon registers causes hang in early BDW revisions.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT(0), WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaReportPerfCountUseGlobalContextID, "WA for MI_REPORT_PERF_COUNT cmd requiring memory address to come from global GTT, not PPGTT.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForcePcBbFullCfgRestore, "Force metrics full config restore on context switch via CTX WA BB.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableNonPresentRenderTargetChannels, "Component Write disables must be set for non-present color channels.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFixRenderSyncFlush, "Wa - apply SyncFlush fix for Render engine (Gesher sighting: 3715935 currenlty for SNB only).", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSetupGtModeTdRowDispatch, "Wa - Setup GT Mode TD Row Dispatch", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNoBackToBackLriInSCD, "Wa - Apply SCD Sprite register writes WA - HW Gesher sighting: 3716035", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaApplyL3ControlAndL3ChickenMode, "IVB WA to set L3 Control register and L3 Chicken Mode register with specific values.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSendDummy3dPrimitveAfterSetContext, "Send a dummy 3D_PRIMITVE after every MI_SET_CONTEXT.", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableL3CacheAging,
               "WA - VLV sighting hardware bug # 261401 - needs L3 Control Register1 : L3 Aging Disable Bit (L3AGDIS): to be set on every context save/restore",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDivideLLCHitsCounterBy16, "Divide LLC hits count by 16.", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSaveVscRegisters, "Send KMD WA Batch Buffer to save Media VSC MMIO register space into user-mode mapped resource", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableRCZUnitClockGating, "Disable RCZ Unit Clock Gating. (cloned HSD ivbgt2 bug_de: 3665923 )", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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
               "Adjacency discard hold with state change causing hang.    Send PIPE_CONTROL with dummy post sync op when GS is enabled before 3DSTATE_GS command.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCSRUncachable, "Declare CSR resource as uncachable", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushBefore3DSTATEGS, "Send pipe flush on every gs state change if allocated GS handle is less than 16 and it is SIMD8 mode.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSwitchSolVfFArbitrationPriority, "HSW hw has the priority switched by accident - this WA switches back to expected.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaBBSNonPrivilegedBit, "WA - Use BBS Non-privileged bit (only HSW B0+) to force HW security parsing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAlternateSigKeys, "HSW CB2/NO_OP signature keys are different for A step", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableEarlyEOT, "Use NO_OP Clear buffer instead of actual CB2", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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
               "Dirty Fill followed by Dirty Fill to same set and way causes 2nd Dirty Fill to evict wrong data Need to insert NOPs via chicken bit to fix the issue. Rare chance "
               "of happening but adding WA anyways.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaBlockMsgChannelDuringGfxReset, "Block Msg Channel before Gfx Reset otherwise MC error happens & system crash with specific OCL/OGL WL", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForcePreemptWaitForIdleOnNonRcsEngines,
               "HW bug on *CS engines where a hang could occur if the 2nd element of an execlist is empty and a preemption request occurs at the wrong time. Workaround is to "
               "require idle before executing a preempt request on *CS",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIncreaseTagClockTimer, "HW bug requires programing L3 tag clock timing register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaLRIToDEUnsupported, "HW limitation on VLV and VLV Plus display engine registers reside outside the scope of LRI", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableThreadStallDopClockGating, "Thread stall clockgating is in ROW_CHICKEN", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableInstructionShootdown, "Instruction Shootdown in ROW_CHICKEN must be disabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePartialInstShootdown, "Partial Instruction Shootdown in ROW_CHICKEN must be disabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableGpGpuPreemptOnGt1, "GPGPU preemption will not work on GT1 skus", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaControlPrimaryTLBUtilization,
               "Control the Primary Display TLB utilization. WA is only needed for Win Blue feature Hybrid graphics. (linear surface for async flip)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableLiteRestore, "Disable Lite Restore", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaHdcDisableFetchWhenMasked, "Set desired default value for HDCCHICKEN register for BDW/CHV platforms, default value is fixed in SKL+", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSetVfGuardbandPreemptionVertexCount, "Preemption vertex count needs to be increased to 0x20 or above", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableTdsClockGating, "Disable TDS unit clock gating", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableVMEReferenceWindowCheck,
               "Reference Window size must be <= Surface Size, otherwise VME behavior is undefined for BDW/CHV/SKL platforms, this is fixed from CNL+", WA_BUG_TYPE_SPEC,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableContextRestoreSubsliceAck, "Disable slice ack (for hsw gt1 sku only)", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableCoherency, "Don't upgrade OCL contexts to be Coherent because of HW bug", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableCoherencyHWFixes, "L3 coherency issue fixed in HW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceEnableNonCoherent, "Set default state of context to be Force Non-Coherent", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForceSyncFlipWithVisibilityOff, "Work Around to Convert CS Async flips to sync. It is used for CHV when SetSourceVisibility is off.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableGamClockGating, "Work Around to disable GAM clock gating to avoid issue where GAMW does not send invalidation end to HDC", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisDdbClkWhileProgVisibilityOn, "DDB clock gating should be disabled while programming visibility ON in Gen5 display,", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)
    // struct __wa_GuC
    unsigned int : 0;

    WA_DECLARE(DisableClockGatingForGucClocks, "Clock Gating must be disabled for GuC Clocks in BDW A0", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaProgramMgsrForCorrectSliceSpecificMmioReads,
               "Shadow Reg 119 (MGSR) needs to be programmed appropriately to get the correct reads from specific slice-related MMIOs", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEngineResetAfterMidThreadPreemption, "Perform an engine reset after a mid-thread preemption is detected (before resubmission)", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaModifyVFEStateAfterGPGPUPreemption, "With specific scenarios of mid thread and thread group preemption, VFE state needs to be modfied before resubmission",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableuKernelHeaderValidFix, "Workaround for 0xC014 uKernel header valid bit bug for GuC load failures at higher GT frequency", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableGoMsgToGAMDuringCPD,
               "GuC to enable GPM GAM GO message during CPD to workaround for message channel hang and GPM hang. It could be used to solve more than one hang issues",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableGoMsgAckDuringCPD, "GuC to enable GO message channel ACK during CPD to workaround for message channel hang", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuCInitSramToZeroes, "Initialize SRAM to zero before GuC load to avoid Micro App DMA issue that causes HW to pick wrong key", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableGuCBootHashCheckNotSet, "Workaround for 0xC010 uKernel hash update bit not set randomly bug for GuC load failures", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableGuCClockGating, "Workaround for HuC CSS header not getting populated in Gen9 and Gen10 platforms", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuCForceFenceByTlbInvalidateReg, "Workaround for Fence/Flush request is not asserting 'wfence' towards GAB".Hence Use TLB Invalidate register to do fence cycle,
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuCCopyHuCKernelHashToSramVar, "Workaround for HuC kernel HASH lost after forcewake is released", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuCDummyWriteBeforeFenceCycle, "Workaround for fence cycle last write miss issue. WA is to send dummy write before fence", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaGuCDisableSRAMRestoreDisable, "Workaround to Disable SRAM restore disable feature", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    // struct _wa_Gmm
    unsigned int : 0;

    WA_DECLARE(WaCursor16K, "Cursor memory need to be mapped in GTT", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaOaAddressTranslation, "WA for STDW and PIPE_CONTROL cmd requiring memory address to come from global GTT, not PPGTT.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaL3IACoherencyRequiresIoMmu, "Gen8 only supports IA-coherent L3 for Advanced Context. (By design--Not actual HW bug.)", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIommuTEBit, "Disable Translation Enable bit for IOMMU", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaNoMinimizedTrivialSurfacePadding,
               "(Not actual HW WA.) On BDW:B0+ trivial surfaces (single-LOD, non-arrayed, non-MSAA, 1D/2D/Buffers) are exempt from the samplers large padding requirements. This "
               "WA identifies platforms that dont yet support that.",
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

    WA_DECLARE(WaCompressedResourceDisplayNewHashMode, "3D and Media compressed resources use LLC/eLLC hot spotting avoidance mode", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCompressedResourceDisplayOldHashMode, "3D and Media compressed resources use LLC/eLLC hot spotting avoidance mode", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaInPlaceDecompressionHang, "WA to avoid the hang issue that occurs when using in-place decompression", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTouchAllSvmMemory, "When in WDDM2 / SVM mode, all VA memory buffers/surfaces/etc need to be touched to ensure proper PTE mapping", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIOBAddressMustBeValidInHwContext, "IndirectObjectBase address (of SBA cmd) in HW Context needs to be valid because it gets used every Context load",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableKillLogic, "WA to disable kill logic (for page faulting), which causes hang when TR-TT and RC6 are both enabled", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFlushTlbAfterCpuGgttWrites, "WA to flush TLB after CPU GTT writes because TLB entry invalidations on GTT writes use wrong address for look-up",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaMsaa8xTileYDepthPitchAlignment, "WA to use 256B pitch alignment for MSAA 8x + TileY depth surfaces.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableIommuAccessedDirtyBit, "WA to disable A/D bits usage for IOMMU", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

    WA_DECLARE(WaDisableNullPageAsDummy, "WA to disable use of NULL bit in dummy PTE", WA_BUG_TYPE_HANG | WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

    WA_DECLARE(WaUseVAlign16OnTileXYBpp816, "WA to make VAlign = 16, when bpp == 8 or 16 for both TileX and TileY on BDW", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_GMM)

    WA_DECLARE(WaDisableRFOSelfSnoop, "RFO Self-snoop must be disabled when in adv ctxt mode to avoid perf issue", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

    WA_DECLARE(WaDisableDynamicCreditSharing,
               "Dynamic credit sharing (used for memory cycles) between various HW units must be disabled to avoid hardware hang with page fault injection", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

    WA_DECLARE(WaNoMocsEllcOnly, "WA to get eLLC Target Cache for MOCS surfaces, when MOCS defers to PAT", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

    WA_DECLARE(WaGttPat0, "GTT accesses hardwired to PAT0", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

    WA_DECLARE(WaGttPat0WB, "WA to set WB cache for GTT accessess on PAT0", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

    WA_DECLARE(WaGttPat0GttWbOverOsIommuEllcOnly, "WA to set PAT0 to full cacheable (LLC+eLLC) for GTT access over eLLC only usage for OS based SVM", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT, WA_COMPONENT_GMM)

    WA_DECLARE(WaAddDummyPageForDisplayPrefetch, "WA to add dummy page row after display surfaces to avoid issues with display pre-fetch", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_GMM)

    // struct _wa_DXVA
    unsigned int : 0;

    WA_DECLARE(WaRestore3DBufVarMpeg, "Must switch decoding type back to MC after VLD decoding", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisableLockForTranscodePerf, "IVB Transcode performance temp WA fix to remove Lock in Decoder", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_MEDIA)

    WA_DECLARE(WaInsertAVCFrameForFormatSwitchToJPEG,
               "Format switch from any Codec decode/encode ending with Skipped MB to Jpeg results in a hang on IVB/VLV/HSW. Fixed from HSW B0, HSD 3665967.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDisableJPEGHSWNewFeatures, "New features are supported from HSW C0: The output formats of NV12/YUY2/UYVY and minimal size to 8x8.", WA_BUG_TYPE_FAIL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaJPEGHeightAlignYUV422H2YToNV12, "Chroma type 422h_2Y and output format NV12 aligned with 8 to Jpeg results in a hang on HSW ULT/BDW. Fixed from CHV.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaVC1DecodingMaxResolution, "For VC1 decoding, HW only can support resolution<=3840*3840.", WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaParseVC1PicHeaderInSlice,
               "For VC1 advanced profile, if PIC_HEADER_FLAG in slice header is set, parse picture header in subsequent slice headers to get MB data offset. HW expects MB data "
               "offset while WMP provideS bitplane offset if bitplane presents.",
               WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaParseVC1FirstFieldPictureHeader,
               "For first field of picture in VC1 advanced profile, if it is I or P picture, parse picture header to get REFDIST value. HW expects REFDIST for I/P/B fields while "
               "WMP send it with B pictures only.",
               WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaParseVC1BPictureHeader,
               "Parse B picture header to get BFRACTION in VC1 advanced profile and main profile. HW expects BFRACTION for B pictures while WMP does not provide it.",
               WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaAddVC1StuffingBytesForSPMP, "HW skips the first byte in bitstream buffer, so driver needs to allocate private buffer and add stuffing bytes ahead of bitstream.",
               WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaLinearMediaBlockAccess64BytePitchAlign, "Linear surfaces accessed with Media Block Read/Write commands require 64-byte-aligned pitch.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaLLCCachingUnsupported, "There is no H/w support for LLC in VLV or VLV Plus", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDisableMFXCryptoCopy, "WA for disabling MFX_CRYPTO_COPY command as it is not supported in HSW HAL-Fulsim (this WA should not be applied in any production code)",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDisableNonStallingScoreboard, "Disable NonStalling Scoreboard on SNB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDisableNonStallingScoreboardBasedOnNumSlices, "Disable NonStalling Scoreboard based on Number of Slices", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_MEDIA)

    WA_DECLARE(WaResetVLineStrideInRenderCacheAfterMedia, "Reset Vertical Line Stride In Render Cache After Interlaced Media Workload", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDisableMFX48bitAddressing, "Disable 48-bit addressing mode on HSW A stepping", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(
    WaUseVP8DecodePrivateInputBuffer,
    "Create a private Gfx buffer in driver and copy bitstream and Coefficient Probability table to it to avoid upper bound check failure in BDW A0. It's for VP8 decode in BDW A0.",
    WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaDummyDMVBufferForMVCInterviewPred, "Insert dummy DMV buffer for MVC decode HW issue (colZeroFlag for interview reference should always be 0).",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaVeboxSliceEnable, "DAC has to turn off before programming the PLL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaIs64BInstrEnabled, "64-byte instructions are enabled on BDW B0+.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaIgnoreCSXRStateForWMProgramming, "Ignore CSXR State and Program the Watermark registers", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_PWRCONS)

    WA_DECLARE(WaDisableDSHEncryptionForWiDi, "Disable DSH encryption data for WiDi on BDW", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

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
    unsigned int : 0;

    WA_DECLARE(WaProgramDpll, "DAC has to turn off before programming the PLL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaADD2DetectBit, "sDVOB control register bit2 on BWG(Crestline maybe) A0 doesn't indicate the right status", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTVDetect, "TV Detection sense bits reversed in Crestline", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableSCWBPPeriodicFlush, "Disable/Enable preiodic flush", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaExtModeFSDOSBlankScreen, "FSDOS blankout/hang in extended desktop (HSD: 545700 & 545671)", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaTVEncoderDisable, "TV encoder when disabled, we should wait for vsync", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaWaitForVBlankAfterTVDisableOREnable, "Wait for vblank, while disabling/enabling TV encoder. BUN#06ww06#6", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableCenteringDuringVGADisable, "VGA centering mode should be disabled in Non-VGA mode. HSD# 306526. Bug# 2156169", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDynamicNormalWaterMark, "Disable dynamic normal watermark computation & programming in Softbios", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaClosedCaptionHotplug, "Crestline only can't have CC control register on and hot plug enabled simultaneously", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSetCR17regAfterS3Resume,
               "Bug# 2078297: Crestline - No Display on TV when coming back from Stand-by. Need to set Bit 7 of CR17 VGA register after Standby-Resume on CRL only, otherwise "
               "IntTV blanks out. As per HW DEs: if bit 7 is set to 0, it suggests that the vertical/horizontal retrace updates have been turned off and therefore are not making "
               "it to ST01. Thus the issue happens.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableHPLLShutdown,
               "Bun 07ww02:Disable HPLL shutdown when accessing 6XXXh MMIO addresses. If we try to access it when in HPLL shutdown mode and read/write to these locations will "
               "result in a hang.",
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

    WA_DECLARE(WaResetChickenBitForAutoLinkTrain, "Wa to reset the chicken bit for the autolink trainin on IVB", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPortWriteforAudioControllerinBIOS, "Wa to enable/disable the audio Dev 3 config register", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCheckforAudioPowerStateRegister, " Wa to poll the power state register while going to CS. Only for HSW+ platforms.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCRCDisabledForMBO, "Wa to keep CRC disabled in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPsrSfuMaskSprite, "Wa to mask Sprite Enable while in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIsAudioControllerinLPSPWell, "Wa to Check if Audio Controller is in Power Well", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaForBlackFlashInMBOMode, "Wa to avoid black flashes in MBO mode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePrimaryFlipsForMBO, "Wa to disable primary flips in MBO disable sequence which would otherwise lead to jitter after entering back legacy PSR.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableLSPCONAuxTransactionInLSMode, "Wa to disable AuxTransactions In LSMode", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDoubleCursorLP3Latency, "Wa to increase cursor latency value in LP3 case", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableHDMI8bpcBefore12bpc, "Wa to enable HDMI port in 8bpc before 12bpc", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFrameStartDelayWaForSDRRS, "Wa to eliminate flicker/screen shift seen during SDRRS Transition.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaHDCPDisable, "Wa to Enable/Disable  HDCP using Registry Key \"DisableHDCP\"", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaClearPSRReset, "Wa to clear PSR reset bit after setting it", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaS3DSoftwareMode, "Wa to use S3D Software mode when the right address in not on tile boundary", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaVLVPMCiCLK5WriteEnable, "VLV B0 :Door Bell write to iCLK5 is SAi protected. Write needs to be enabled through PMC", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaClearArfDependenciesBeforeEot,
               "ARF dependencies unlike GRF dependencies are not cleared by the HW after receiving SEND messages with EOF (End Of Thread). This can be an issue on platforms with "
               "per thread clock gating which disable the EU thread clock right after the EOT. With the clock disabled all pending ARF dependencies are not cleared and stay valid "
               "even when the EU thread gets rescheduled. The WA is to make sure all ARF dependencies are cleared before the EOT. This can be done either by making sure the ARF "
               "register is read before the EOT or the last instruction writing the ARF has the {Switch} bit set.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMADMMacros, "Accordig to Bspec IEEE Madm macros for FDIV and FSQRT will be provied in BDW B0 step.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPMICRegisterReadWrite, "This is a temporary WA to enable PMIC reads/writes for PMIC register reads/writes.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisable1DDepthStencil, "WA on SKL to disable 1D Depth Stencil buffers and use 2D with ht of 1 instead.  Still in discussion when or if this will be fixed.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaZeroOneClearValues, "SKL clear values Bspec restriction: Only 0/1 values allowed.     SKL:GT2:A,SKL:GT3:A,SKL:GT4:A", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaResendURBWhenGSorHSGetsEnabled, "Resend URB state when GS or HS goes from disabled to enabled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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
               "Disable Object level preemption when primitive will be in sequential(non-index) mode. Program ReplayMode bit of appropriate MMIO reg before and after primtive "
               "draw call to turn off midobj preemption for that draw call.",
               WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableObjectLevelPreemptionForInstancedDraw,
               "Disable Object level preemption when instancing is used in indexed draw calls. Program ReplayMode bit of appropriate MMIO reg before and after primtive draw call "
               "to turn off midobj preemption for that draw call.",
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

    WA_DECLARE(WaDisableMinuteIaClockGating, "Bug# 2127939 Work Around for MinuteIa Clock Gating bug Hang", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableRepcolMessages, "Work around issue with replicated color write messages", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPsrDPAMaskVBlankInSRD, "Work around to trigger flips and VBI on first frame during PSR exit to ensure remote frame buffer gets updated with new image",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSendsSrc1SizeLimitWhenEOT, "Work around to limit size of src1 up to 2 GRFs, on Sends/Sendsc instructions when they are EOT.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMixedModeLog, "Math LOG doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMixedModePow, "Math POW doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMixedModeFdiv, "Math FDIV doesn't work correctly in mixed mode.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaFloatMixedModeSelNotAllowedWithPackedDestination, "sel doesn't work correctly when using mixed mode and destination is <1>:hf.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDSPushConstantsInFusedDownModeWithOnlyTwoSubslices,
               "If pm_mode_subsliceen is set to 101 or 110, Domain shader must use pull constants instead of push constants", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableVSPushConstantsInFusedDownModeWithOnlyTwoSubslices,
               "If pm_mode_subsliceen is set to 101 or 110, Vertex shader must use pull constants instead of push constants", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDgMirrorFixInHalfSliceChicken5,
               "Wa to solve issues in wgf11Filter used in 3D sampler -by Disabling DG Mirror Fix enable bit in Half_Slice_Chicken5 register.", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaSkipInvalidSubmitsFromOS, "[MSFT 416192] For Invalid submits from OS - simply report fence completion without submitting the DMA buffer to GPU",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WAMMCDUseSlice0Subslice0, "WA for MMCD by using slice0 subslice0 only to avoid hang caused by missing HDC repeaters", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaRealignCursorC, "Realign the cursor buffer in Pipe C when position becomes negative on 0 orientation and fail HW cursor on 180 orientation",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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
    unsigned int : 0;

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

    WA_DECLARE(
    WaDisableRCWithAsyncFlip,
    "Shouldnt use Render Compression with async flip on SKL A due HW issue and SKL B+ as they are converted to sync Flips internally.  Fixed in GLK, GWL, GLV, and Gen10+",
    WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableHBR2, "Shouldn't report HBR2 Support on SKL A1 boards due to HW Issue", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableRCNV12, "For SKL C0 stepping, the RC fix that asserts the stall can be disabled by CHICKEN_PIPESL bit 22", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaVfPostSyncWrite, "Workaround for BDW to set post sync op of write for PIPE_CONTROL when only VF cache invalidate set", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisablePowerCompilerClockGating, "Set DisablePowerCompilerClockGating bit. This is to prevent corruption while hiz raw stall in partial span .",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPreventSoftResetHangUsingGamtArbReg, "Set/reset GAMTARBMODE reg bit before and after Soft reset to avoid hangs and prevent HDC invalidations.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableDC5DC6, "Disable DC5/6 on SKL", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaIgnoreDDIAStrap, "Ignore Strap state for DDI A on SKL", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRsRestoreWithPerCtxtBb, "Workaround for a HW issue with the PerCtxtBb and the RS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRSFlushRequiredBefore3DPrimitivePreemption,
               "Resource Streamer Flush required between RS produce commands (Binding Table Pointer, DX9 Generate Active, or Gather Constant) and 3D Primitive command when "
               "preemption is enabled.",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableHuCAuthentication, "Do not enable authentication when using GuC DMA to load HuC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaHuCNoStreamObject, "HuC Dummy StreamIn for encrypted workload after VDEnc BRC", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaHucBitstreamSizeLimitationEnable, "HW Read/Peek operation issue when BistreamSize < 4", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaModeSwitchDummyFrame, "VEBOX Dummy frame for SKL GT3/GT4 Mode Switch WA. SW HSD#5619023 and HW bug_de#2133079", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAddDelayInVDEncDynamicSlice, "WA for hang on VDEnc with small dynamic slice size", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaReadVDEncOverflowStatus, "WA for reading VDEnc slice size overflow bit in MFX MMIO ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSklLpt, "WA For LPT with SKL", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePreemptionDuringPavp, "Preemption needs to be disabled for Pavp workloads on HSW", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUnitLevelClockGatingDisableGMBUS_PCH, "SW WA to disbale unit level clock gating for GMBUS", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaIncreaseLatencyIPCEnabled, "WA to increment latency by 4us for all levels when IPC is enbaled", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableTWM, "WA to disable Transitional WM.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaProgramHalfLineTimeForIPC, "WA to programm Line time to half of Actual Line time value calculated in WM programming", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaReadVcrDebugRegister, "To read the VCR debug register (0x320F4) we disable media clock, read register, then enable", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableHDCInvalidation, "WA to Disable HDC Invalidation by default", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSplitPipeControlForTlbInvalidate,
               "WA to split pipecontrols that invalidate the tlb in order to force handling IOTLB invalidation for IOMMU on SKL. Note: this is only applies to currently existing "
               "pipecontrols with TLB invalidate",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableSbeCacheDispatchPortSharing, "Disable Shared SBE subslice cache dispatch port sharing", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaWGBoxAndWDtranscoderEnable, "Wa related to enabling of WGtarnscoder and WGBOx ", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableLbsSlaRetryTimerDecrement, "WA to Enable LBS SLA Retry Timer Decrement on SKL.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaCcsTlbPrefetchDisable, "For DX10 performance improvement as recommended by the Bspec", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableTrickleFeedForNV12, "WA for HW bug: YF NV12 split transaction with the EOB is sending a different blkid in between", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableSoftwarePCDDelay, "WA for HW bug: PCD_Delay registers not hooked up correctly in BXT and GLK PPS", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisablePWMClockGating, "WA for HW bug: To bring down PWM when it is turned OFF in BXT and GLK", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
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

    WA_DECLARE(WaCheckEU10Disabled, "Check if EU10 is disabled in FUSE register (due to bug) and if so send new EU count that needs to be used for each SubSlice ",
               WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaC0AstcCorruptionForOddCompressedBlockSizeX,
               "Enable CHV C0 WA for ASTC HW bug: sampling from mip levels 2+ returns wrong texels. WA redescribes ASTC texture as 4*w, 4*d and uses only mips2+",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRCCByteSharingDisableForHSWGT3, "RCC byte sharing must be disabled for HSW GT3", WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaAstcCorruptionForOddCompressedBlockSizeX,
               "Enable CHV D0+ WA for ASTC HW bug: sampling from mip levels 2+ returns wrong texels. WA adds XOffset to mip2+, requires D0 HW ECO fix.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaUseYCordforPSR2, "WA To use Y cord for PSR2", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(
    WaDisableDeepLoopsUnrolling,
    "WA to reduce memory usage of tests with large number of nested loops, such as GLCTS ES31-CTS.arrays_of_arrays.InteractionArgumentAliasing tests for CHV CR with 1GB memory.",
    WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnableDMCForNV12MPO, "WA to enable DMC to wake up the memory for NV12 MPO case", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDups1GatingDisableClockGatingForMPO, "WA to disable clock gating for MPO", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaChickenBitsMidBatchPreemption,
               "When Per Context Preemption Granularity Control is used and media preemption is not supported, set CS_CHICKEN1 (02580h) to mid-batch level preemption (bit2:1 = "
               "10b) for media workloads in render engine. Otherwise, there will be GPU hang (b9023364).",
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

    WA_DECLARE(WaGucSizeUsedWhenValidatingHucCopy, "HW uses GuC size when validing the HuC DMA copy size", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaGucDisable2ElementSubmission, "HW doesnot allow submissions with head==tail which fails 2 element submissions", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaDisable4KPushConstant, "Ensure nonzero curbe start", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaClearTdlStateAckDirtyBits, "WA to avoid message collision in TDL, by not doing NP state ack ", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaSendDummyGPGPUWalkerBeforeHSWithBarrier, "Send dummy GPGPU_WALKER command before HS with barrier to work-around HW hang bug on BXT.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaVFEStateAfterPipeControlwithMediaStateClear,
               "WA to disable preemption between VFE state and pipe control when VFS state is after pipe control with media state clear.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaSetMipTailStartLODLargertoSurfaceLOD, "Set the value of RENDER_SURFACE_STATE.Mip Tail Start LOD to a mip that larger than those present in the surface (i.e. 15)",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_3D)

    // This is added to workaround a HW issue on platforms till gen9, which is shown due to CL 608126
    WA_DECLARE(WaDisableSamplerRoundingDisableFix,
               "Disable sampler address rounding fix - which disables U, R, V address rounding in Sampler State, due to a hardware issue on platforms till Gen9.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_3D)

    WA_DECLARE(WaForGAMHang, "Disable HW TRTT or literestore in order to avoid GAM hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaGAMWrrbClkGateDisable, "Disable GAMWrrb clock gate", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaMediaPoolStateCmdInWABB, "WA to avoid VFE/TSG hang, on BXT/GLK GPGPU, by using MediaPoolState configured in MidCtxt WA BB", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaPlanePosPlusWidthLessThanPipeHorSize, "https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1939307", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPSR2MultipleRegionUpdateCorruption, "Wa to set 0x42080[3] = 1 before PSR2 enable", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaEnablePSRExitOn3DLutUpdate,
               "WA: Write 0x00000000 to MMIO register 0x49028: https://vthsd.fm.intel.com/hsd/gen10lp/default.aspx#bug_de/default.aspx?bug_de_id=1942473", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

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

    WA_DECLARE(WaDisablePreemptForMediaWalkerWithGroups, "Disable Pre-emption bit (bit 11) in register CS_CHICKEN1 for media walker with groups", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaAllocateExtraVBPageForGpuMmuPageFaults, "Allocate extra page in vertex buffers to prevent gpu page faults when Gpu Mmu Page Faults are enabled", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaRetrialOfKsvReadlistHDCPCompiliance, "Call GetHDCPReceiverData function again, if we get failure for first read", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaKBLVECSSemaphoreWaitPoll, "WA for VECS reset failure in KBL. Increased the poll interval in VECS_SEMA_WAIT_POLL(0x1A24C) by 1usec.", WA_BUG_TYPE_HANG,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaNV12YfTileHWCursorUnderrun, "Display underrun with Yf tiled NV12 surface + Cursor", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)
    WA_DECLARE(WaDDIIOTimeout, "Phy enable, Disable and re enable causing Power well enable time out casing display blankout", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaDSIRcompFailure, "MIPI DSI Rcomp failures which can cause image corruption at hot temperatures", WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaAlwaysEnableAlphaMode, "Enable Alpha mode in Plane_Color_Ctl for passing DP Link layer compliance. Will remove WA once HW sighting (1604297325) is concluded.",
               WA_BUG_TYPE_SPEC, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaAddSourceAndDestinationPixelBypassForPlaneAlphaBlending, "Add alpha blending source pixel bypass and destination bypass for plane alpha blending.",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaEnableVoidExtentBlockPatchingforASTCLDRTextures, "WA for mishandled fixed-to-float conversion in ASTC LDR mode", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_OGL)

    WA_DECLARE(WaDisableKmPresentForRtlSim, "WA to disable KmPresent calls in RTL simulation environment", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaRtlSimulation, "WA for driver to run in RTL simulation environment", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaModifyGamTlbPartitioning, "WA to adjust default GAM TLB partitioning to back up C/Z L3 cache traffic", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT(25), WA_COMPONENT_KMD)

    WA_DECLARE(WaGAPZPriorityScheme, "WA to set arbitration priority in arbiter register (0xB004)", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaL3BankAddressHashing, "WA to set correct L3 bank address hashing", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableCleanEvicts, "WA to disable clean evict", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDisableImprovedTdlClkGating, "WA to disable improved TDL clock gating", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaCL2SFHalfMaxAlloc, "WA to reduce the max allocation to CL2 and SF", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaForwardProgressSoftReset, "WA for flush sequence in the L3 Node that can impact forward progress in the presence of traffic during soft reset",
               WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaPAVPEncryptionOffAtContextRestore, "WA to terminate all encryption sessions at context restore", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_KMD)

    WA_DECLARE(WaNoSimd16TernarySrc0Imm, "Wa to avoid src0 imm in ternary simd16 inst", WA_BUG_TYPE_FAIL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSSEUPowerGatingControlByUMD, "WA for UMD to program SSEU power gating on GEN11+", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaDPFRGatingDisableWhenScalarEnabled, "WA to disable the clock gating to the Scaler's register block when Plane/Pipe Scalar is enabled", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaEnable32PlaneMode, "WA to enable 32-plane mode on GEN11+", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaArbitraryNumMbsInSlice, "WA to avoid MBEnc stall issue by forcing arbitrary MBs in slice", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_MEDIA)

    WA_DECLARE(WaInterlacedmodeReqPlaneHeightMinTwoScanlines, "InterlacedMode requires Planeheight minimum of Two Scalines", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPruneModesHavingHfrontPorchBetween122To130, "WA for prunning the modes which has HfrontPorch Value between 122 to 130 to fix the H/W Bug till Icelake.",
               WA_BUG_TYPE_CORRUPTION, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaMPOReqMinPlaneLeftFourBelowHActive, "HW WA - 1174. To fail MPO if plane's left coordinate is less than four pixels from HActive", WA_BUG_TYPE_FUNCTIONAL,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaPlaneSizeAlignmentFor180Rotation,
               "WA for HW bug: with 180 rotation panels, alligning plane width to multiple of 64, 32, 16 for NV12, YUV and RGB planes respectively.", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WaSkipPortRegisterAccess, "WA for HW bug: access phy port registers in power up sequence is resulting in a hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(WADisableGTPAndSetISPDisable, "Disable Gather Pool Allocation when Resource Streamer is disabled. WA applicable for Gen9", WA_BUG_TYPE_UNKNOWN,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaSetPerfSuperQueueFullLimit, "WA to set default value of arbiter register 0x902C[9:3]", WA_BUG_TYPE_PERF, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_KMD)

    WA_DECLARE(WaNoAtomicForSend, "WA for HW bug: an EU with atomic HDC and SLM messages cause a hang", WA_BUG_TYPE_HANG, WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableUnormPathForBlending, "WA for HW Bug: Combining Subspans with blend enables causes corruption for some RT formats", WA_BUG_TYPE_CORRUPTION,
               WA_BUG_PERF_IMPACT_UNKNOWN, WA_COMPONENT_UNKNOWN)

    WA_DECLARE(WaDisableMultiChannelAudioForDP, "WA for HW bug: Enable maximum 2 audio channels for GLK in case of DP display.", WA_BUG_TYPE_FUNCTIONAL, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_SOFTBIOS)

    WA_DECLARE(Wa3DStateMode, "On 3DSTATE_3D_MODE, driver must always program bits 31:16 of DW1 a value of 0xFFFF.", WA_BUG_TYPE_UNKNOWN, WA_BUG_PERF_IMPACT_UNKNOWN,
               WA_COMPONENT_UNKNOWN)

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
#define GFX_IS_SKU(s, f) ((s)->SkuTable.f)
#define GFX_IS_WA(s, w) ((s)->WaTable.w)
#define GFX_WRITE_WA(x, y, z) ((x)->WaTable.y = z)
// No checking is done in the GFX_WRITE_SKU macro that z actually fits into y.
//  It is up to the user to know the size of y and to pass in z accordingly.
#define GFX_WRITE_SKU(x, y, z) ((x)->SkuTable.y = z)
#else
#define GFX_IS_SKU(h, f) (((PHW_DEVICE_EXTENSION)(h))->pHWStatusPage->pSkuTable->f)
#define GFX_IS_WA(h, w) (((PHW_DEVICE_EXTENSION)(h))->pHWStatusPage->pWaTable->w)
#define GFX_WRITE_WA(x, y, z) (((HW_DEVICE_EXTENSION *)(x))->pHWStatusPage->pWaTable->y = z)
// No checking is done in the GFX_WRITE_SKU macro that z actually fits into y.
//  It is up to the user to know the size of y and to pass in z accordingly.
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

#endif //__SKU_WA_H__
