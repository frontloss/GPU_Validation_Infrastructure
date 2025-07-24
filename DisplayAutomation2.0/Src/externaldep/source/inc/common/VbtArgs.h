/*===========================================================================
; VbtArgs.h
;----------------------------------------------------------------------------
;   Copyright (c) 2004-2005  Intel Corporation.
;   All Rights Reserved.  Copyright notice does not imply publication.
;   This software is protected as an unpublished work.  This software
;   contains the valuable trade secrets of Intel Corporation, and must
;   and must be maintained in confidence.
;
; File Description:
;   This file declares the Arguments of Virtual Members of VBTMANAGER CLASS
;
;--------------------------------------------------------------------------*/

/*===========================================================================
; VBT Driver Feature Block (12) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/
// enum for LVDS configuration, VBT setting in Block 12
// SDVO LVDS VBT settings
// Currently No_LVDS and Integrated_And_SDVO_LVDS are not implemented in driver
// but are available in VBT options, for these two options we take the default
// action i.e, enable the integrated LVDS and disable the external LFP
#ifdef _COMMON_PPA
#include "OMPTool.h"
#endif

typedef enum LVDS_CONFIG_ENUM
{
    No_LVDS         = 0, // not implemented, take default action
    Integrated_LVDS = 1,
#ifndef _COMMON_PPA
    SDVO_LVDS = 2,
#endif
    Integrated_And_SDVO_LVDS = 3, // not implemented take default action
    Undefined_config         = 0xffff
} LVDS_CONFIG_EN;

typedef struct _VBT_CHROMATICITY_DETAILS
{
#pragma pack(1)
    union {
        UCHAR ucVBTSupportEnable;
        struct
        {
            UCHAR bChromaticitySupportEnable : 1;
            UCHAR bEDIDChromaticityOverride : 1;
            UCHAR ucReserved : 6;
        };
    };

    union {
        UCHAR RedGreenLowBits; // Byte 1
        struct
        {
            UCHAR ucGreenYLowBits : 2; // bit 1:0
            UCHAR ucGreenXLowBits : 2; // bit 3:2
            UCHAR ucRedYLowBits : 2;   // bit 5:4
            UCHAR ucRedXLowBits : 2;   // bit 7:6
        };
    };

    union {
        UCHAR ucBlueWhiteLowBits; // Byte 2
        struct
        {
            UCHAR ucWhiteYLowBits : 2; // bit 1:0
            UCHAR ucWhiteXLowBits : 2; // bit 3:2
            UCHAR ucBlueYLowBits : 2;  // bit 5:4
            UCHAR ucBlueXLowBits : 2;  // bit 7:6
        };
    };

    UCHAR ucRedXUpperBits; // Byte 3
    UCHAR ucRedYUpperBits; // Byte 4

    UCHAR ucGreenXUpperBits; // Byte 5
    UCHAR ucGreenYUpperBits; // Byte 6

    UCHAR ucBlueXUpperBits; // Byte 7
    UCHAR ucBlueYUpperBits; // Byte 8

    UCHAR ucWhiteXUpperBits; // Byte 9
    UCHAR ucWhiteYUpperBits; // Byte 10

#pragma pack()
} VBT_CHROMATICITY_DETAILS, *PVBT_CHROMATICITY_DETAILS;

typedef struct _VBT_LUMINANCE_AND_GAMMA
{
#pragma pack(1)
    /**
    Defines the chromaticity feature enable bits
    Bits 7:2  : Reserved
    Bit 1     : Enable Gamma feature.
    : if enabled, use gamma values from this block.
    0 : Disable
    1 : Enable
    Bit 0     : Enable Luminance feature.
    : if enabled, use values from this block.
    0 : Disable
    1 : Enable
    **/
    union {
        UCHAR ucVBTSupportEnable;
        struct
        {
            UCHAR bLuminanceOverrideEnable : 1;
            UCHAR bGammaOverrideEnable : 1;
            UCHAR ucReserved : 6;
        };
    };

    /**
    Luminance info (refer DisplayID 2.0)
    2 byte value, encoded in IEEE 754 half-precision binary floating point format
    **/
    UINT16 MinLuminance;          ///< Native minimum luminance
    UINT16 MaxFullFrameLuminance; ///< Native maximum luminance (Full Frame)
    UINT16 MaxLuminance;          ///< Native Maximum Luminance (1% Rectangular Coverage)
                                  /**
                                  Gamma EOTF
                                  Value shall define the gamma range, from 1.00 to 3.54, as follows:
                                  Field Value = (Gamma + 100) / 100
                                  Field values range from 00h through FFh.
                                  FFh = No gamma information shall be provided
                                  **/
    UINT8 Gamma;
#pragma pack()
} VBT_LUMINANCE_AND_GAMMA, *PVBT_LUMINANCE_AND_GAMMA;

typedef struct _VBT_BLOCK46_DATA
{
    VBT_CHROMATICITY_DETAILS ChromaticityData[16];
    VBT_LUMINANCE_AND_GAMMA  LuminanceAndGammaData[16];
} VBT_BLOCK46_DATA, *PVBT_BLOCK46_DATA;

typedef struct _VBT_DRIVER_FEATURE
{
#pragma pack(1)

    union {
        struct
        {
            UCHAR bEnableDefaultBootMode : 1; // 1 = Customized Driver Default, 0 = OS default
            UCHAR bBlockOverlay : 1;
            UCHAR bAllowFSDOSSwitch : 1;
            UCHAR bHotPlugDVO : 1;
            UCHAR bEnableZoom : 1;          // RCR 258064
            UCHAR bSBIOSInt10 : 1;          // RCR 211835
            UCHAR bEnableSpriteInDPSIM : 1; // RCR 230205
            UCHAR bUse_0110h_ForLFP : 1;    // RCR 236382
        };
        UCHAR ucEnable;
    };
    USHORT usXRes;  // Default X Resolution
    USHORT usYRes;  // Default Y Resolution
    UCHAR  ucBpp;   // Default Color Depth
    UCHAR  ucRRate; // Default Refresh Rate

    union {
        struct
        {
            USHORT bLFPAlwaysPrimary : 1; // RCR 208761
            USHORT bGTFCheckEnabled : 1;
            USHORT bDynFreqSwitchEnabled : 1;
            USHORT bHighFreqRenderClkEnabled : 1;
            USHORT bNT4DualDisplayCloneSupport : 1;
            USHORT bDefaultPwrSchemeUI : 1; // RCR 236382
            USHORT bSpriteDisplayAssignment : 1;
            USHORT bAspectScalingEnabled : 1; // Aspect scaling RCR
            USHORT bPreserveAspectRatio : 1;  // Aspect scaling RCR
            USHORT bSDVOPowerDownFeature : 1; // RCR 288502 Sdvo power down
            USHORT bHotPlugCRT : 1;           // CRT Hotplug for Lakeport
            USHORT bLvdsConfig : 2;           // RCR LVDS configuration bits (Valid only from VBT version 125)
                                              //  0x00,   "No LVDS"
                                              //  0x01,   "Integrated LVDS"
                                              //  0x02,   "SDVO-LVDS"
                                              //  0x03,   "Both Integrated and SDVO LVDS"
            USHORT bHotPlugTVOut : 1;
            USHORT bExtReserved : 2;
        };
        USHORT usExtDriverBits;
    };

    union {
        struct
        {
            UCHAR bStaticDevice : 1;            // RCR 211997
            UCHAR bEmbeddedPlatformEnable : 1;  // RCR 1023524
            UCHAR bDisplayDisabledPlatform : 1; // RCR 1023713
            UCHAR bCUIReserved : 5;
        };
        UCHAR ucCUIStatic;
    };

    // From 1.16 version onwards
    USHORT usMaxBSModeXRes;
    USHORT usMaxBSModeYRes;
    // From 1.17 version onwards
    UCHAR usMaxBSModeRRate;

    // RCR #992509 - Structure for external encoder related details
    union {
        struct
        {
            UCHAR bInternalTermination : 1; // For internal source termination
            UCHAR ucSDVOReserved : 7;
        };
        UCHAR ucSDVO;
    };
    // RCR #1003210 - New flag indicating VBIOS minor version
    UCHAR ucVBIOSMinorVersion;

    // RCR# 1023383 Structure for PC features enable/disable
    union {
        struct
        {
            USHORT usRMPM : 1;
            USHORT usFBC : 1;
            USHORT usDPST : 1;
            USHORT usDxgkDdiBlc : 1;
            USHORT usADB : 1;
            USHORT usDRRS : 1;
            USHORT usRS : 1;
            USHORT usReserved1 : 1;
            USHORT usTurboBoost : 1;
            USHORT usPSR : 1;
            USHORT usDFPS : 1;
            USHORT usReserved2 : 1;
            USHORT usDMRRS : 1;
            USHORT usADT : 1;
            USHORT usReserved3 : 1;
            USHORT usValidBit : 1;
        };
        USHORT usPCOverride;
    };
#pragma pack()
} VBT_DRIVER_FEATURE, *PVBT_DRIVER_FEATURE;

/*===========================================================================
; VBT Driver Persistence Feature Block (13) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/

typedef struct _VBT_DRVIER_PERSISTENCE
{
#pragma pack(1)

    union {
        USHORT usPersistenceEnable;
        struct
        {
            USHORT bPersistHotkey : 1; // Persistence on Hot-Key event
            USHORT bPersistLid : 1;    // Persistence on Lid Switch event
            USHORT bPersistPower : 1;  // Persistence on Power Management event
            USHORT bPersistMDS : 1;    // Persistence on MDS/Twin
            USHORT bPersistRRate : 1;  // Persistence on RefreshRate
            USHORT bPersistPipe : 1;   // Persistence on RestorePipe
            USHORT bPersistMode : 1;   // Persistence on Mode
            USHORT bPersistEDID : 1;   // Persistence on EDID  (RCR 208507)

            USHORT bPersistHotPlug : 1; // Persistence on HotPlug RCR 205534
            USHORT bPersistDock : 1;    // Persistence on DOCK RCR 236751
            USHORT bReserved : 6;       // Reserved bits
        };
    };

    UCHAR ucEDIDMaxConfig; // Maximum number of EDID, tied to bPersistEDID above.

#pragma pack()
} VBT_DRVIER_PERSISTENCE, *PVBT_DRVIER_PERSISTENCE;

/*===========================================================================
; VBT rotation driver Block (18) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/

typedef struct _VBT_ROTATION_CONFIG
{
#pragma pack(1)

    UCHAR ucRotationEnable; // bit0 : 0 - Disable Rotation
                            //        1 - Enable Rotation

    // DDR (Display Device level Rotation) Flags
    // These flags define the VBT Display Policy as per SAS 0.44

    UCHAR ucDispDevicePolicy;

    // DDR_ENABLE_ALL    (0x0)
    // DDR_CRT_DISABLE   (0x1)
    // DDR_LFP_DISABLE   (0x2)
    // DDR_DFP_DISABLE   (0x4)
    // DDR_TV_DISABLE    (0x8)
    //
    UCHAR ucReserved[10]; // slack bytes for future use

#pragma pack()
} VBT_ROTATION_CONFIG, *PVBT_ROTATION_CONFIG;

/*===========================================================================
; VBT BLC Block (42) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/

typedef struct _VBT_BLC_DATA
{
#pragma pack(1)

    union {
        ULONG ulBlcCaps; // BLC capabilities
        struct
        {
            ULONG bBlcSupported : 1;              // BLC Supported? (from VBT)
            ULONG bBlcEnabled : 1;                // BLC Enabled? (from SBIOS)
            ULONG bBlcMinBrightnessSupported : 1; // BLC Minimum brightness field supported?
            ULONG bBlcI2CAddrSupported : 1;       // BLC I2CAddr invertor field supported?
            ULONG bBlcBrightnessCmd : 1;          // BLC I2C inverter command code supported?
            ULONG bBlcReserved : 27;              // Reserved
        };
    };
    UCHAR  ucBlcType;          // BLC Inverter Type
    UCHAR  ucBlcPolarity;      // BLC Inverter Polarity
    UCHAR  ucBlcGpioPins;      // BLC Inverter GPIO Pins (I2C)
    ULONG  ulBlcBlockSize;     // BLC VBT Block Size
    USHORT usBlcFrequency;     // BLC Inverter Frequency (PWM)
    UCHAR  ucBlcGMBusSpeed;    // BLC inverter GMBus speed
    UCHAR  ucMinBrightness;    // Minimum Brightness, 0 - 255
    UCHAR  ucBlcI2cAddr;       // I2C inverter Slave address
    UCHAR  ucBlcBrightnessCmd; // I2C inverter command code
    UCHAR  ucBlcPWMControllerNumber;
    UCHAR  ucBlcPWMControllerType;

#pragma pack()
} VBT_BLC_DATA, *PVBT_BLC_DATA;

/*===========================================================================
; VBT DPST Block (43) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/

typedef struct _VBT_DPST_DATA
{
#pragma pack(1)

    union {
        ULONG ulDpst; // See matching definition in SoftBIOS.H
        struct
        {
            ULONG bDpstSupported : 1; // DPST Supported? (from VBT)
            ULONG bDpstEnabled : 1;   // DPST Enabled? (from SBIOS)
            ULONG bDpstLevel : 3;     // DPST Default Aggressiveness Level
            ULONG bDpstBlockSize : 7; // DPST VBT Block Size
            ULONG bDpstReserved : 20; // DPST Reserved Bits
        };
    };

#pragma pack()
} VBT_DPST_DATA, *PVBT_DPST_DATA;

/*===========================================================================
; VBT ALS Block (44) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/
typedef struct _VBT_ALS_DATA
{
#pragma pack(1)

    union {
        ULONG ulAls; // BLC capabilities
        struct
        {
            ULONG bAlsSupported : 1; // ALS Supported? (from VBT)
            ULONG bAlsReserved : 31; // Reserved
        };
    };

    USHORT ALSResponseData[5][2]; // ALS Response Data (Brightness,Lux(5 values))

#pragma pack()
} VBT_ALS_DATA, *PVBT_ALS_DATA;

/*===========================================================================
; VBT Display LACE Block (44) - Must match VBIOS VBT Data struct
;--------------------------------------------------------------------------*/
typedef struct _VBT_DISPLAYLACE_DATA
{
#pragma pack(1)

    union {
        ULONG ulDisplayLace; // ALS Display LACE capabilities
        struct
        {
            ULONG bDisplayLaceEnabled : 1;                     // Display LACE default enabled status
            ULONG bDisplayLaceSupported : 1;                   // Display LACE Supported ?
            ULONG ucDisplayLaceAggressivenessLevelProfile : 3; // Display LACE Aggressiveness Level Profile.
            ULONG ulDisplayLaceReserved : 27;                  // Reserved
        };
    };

#pragma pack()
} VBT_DISPLAYLACE_DATA, *PVBT_DISPLAYLACE_DATA;

#define NUMBER_OF_TOGGLE_LISTS 4

typedef struct _VBT_TOGGLE_LIST
{
    ULONG  ulToggleListSize;
    PUCHAR pucToggleList;
} VBT_TOGGLE_LIST, *PVBT_TOGGLE_LIST;

typedef struct _VBT_TOGGLE_TABLE
{
    VBT_TOGGLE_LIST stVBTToggleList[NUMBER_OF_TOGGLE_LISTS];
} VBT_TOGGLE_TABLE, *PVBT_TOGGLE_TABLE;

#ifdef __cplusplus // For CUI/COM

typedef struct _SB_GETVBTINFO_ARGS
{

    VBT_DRIVER_FEATURE     Feats;
    VBT_DRVIER_PERSISTENCE Persist;
    VBT_ROTATION_CONFIG    Rotation;
    VBT_BLC_DATA           Blc;
    VBT_DPST_DATA          Dpst;
    VBT_ALS_DATA           Als;
    VBT_DISPLAYLACE_DATA   DisplayLace;

    union {
        ULONG ulMisc;
        struct
        {
            ULONG bHotkeyNoDetect : 1;
            ULONG bUseBIOSBootDevice : 1;
            ULONG bFtrInvertRotation : 1; // This is VBT value comes from Razer related BIOS
            ULONG bFtrRGBColorSeparation : 1;
            ULONG ulReserved : 28;
        };
    };
    BOOLEAN bDownscalingenabled;
    BOOLEAN bKVMVirtualDVISupported;
} SB_GETVBTINFO_ARGS, *PSB_GETVBTINFO_ARGS;

#else  // __cplusplus
typedef struct _SB_GETVBTINFO_ARGS
{

    VBT_DRIVER_FEATURE;
    VBT_DRVIER_PERSISTENCE;
    VBT_ROTATION_CONFIG;
    VBT_BLC_DATA Blc;
    VBT_DPST_DATA;
    VBT_ALS_DATA         Als;
    VBT_DISPLAYLACE_DATA DisplayLace;

    // Miscellaneous bits that are not in the driver BIOS data blocks.
    union {
        ULONG ulMisc;
        struct
        {
            ULONG bHotkeyNoDetect : 1;
            ULONG bUseBIOSBootDevice : 1;
            ULONG bFtrInvertRotation : 1; // This is VBT value comes for Razer related BIOS
            ULONG bFtrRGBColorSeparation : 1;
            ULONG ulReserved : 28;
        };
    };
    BOOLEAN bDownscalingenabled;
    BOOLEAN bKVMVirtualDVISupported;
} SB_GETVBTINFO_ARGS, *PSB_GETVBTINFO_ARGS;

typedef struct _SB_CURRENT_VBT
{
    OUT ULONG ulVBTSize;
    OUT DDU8 *pulVBTData;
} SB_CURRENT_VBT_ARGS, *PSB_CURRENT_VBT_ARGS;
#endif // __cplusplus

/////////////////////////////////////////////
//
// Arguments for GetAimVbtList
//
/////////////////////////////////////////////
typedef enum
{
    VBT_SDVO_LVDS = 0,
    VBT_INT_HDTV  = 1,
    VBT_SDVO_DFP  = 2
} AIM_VBT_TYPE;

//#ifndef _COMMON_PPA
//    typedef struct _MODE_LIST
//    {
//        ULONG ulXRes;
//        ULONG ulYRes;
//        UCHAR ucBpp;
//        UCHAR ucRRates;
//    }MODE_LIST,*PMODE_LIST;
//#endif

#define MAX_MODE_REMOVAL_ENTRY 20
// RCR 2262182: Added 48Hz support in the modes removal table in VBT
#define MODE_REMOVAL_NUM_REFRESH_RATES 15             // Number of refresh rates supported as part of mode removal
#define MODE_REMOVAL_ALL_REFRESH_RATES_BITMASK 0x0FFF // First 12 bits set to 1
typedef struct _MODE_REMOVAL_LIST
{
    ULONG   ulXRes;
    ULONG   ulYRes;
    UCHAR   ucBpp;
    USHORT  usRRatesBitMask; // For details on how to interpret this see VBT_REFRESH_RATE in VbtManager.h
    BOOLEAN bInterlaced;     // Flag added for indicating Interlaced or progressive. RCR - 1003209
} MODE_REMOVAL_LIST, *PMODE_REMOVAL_LIST;

typedef struct _VBT_MODE_REMOVAL_TABLE
{
    MODE_REMOVAL_LIST ModeRemovalList[MAX_MODE_REMOVAL_ENTRY];
    ULONG             ulNumMode;
    ULONG             ulDisplayType;
} VBT_MODE_REMOVAL_TABLE, *PVBT_MODE_REMOVAL_TABLE;

/////////////////////////////////////////////
//
// Arguments for GetModeAdditionList
//
/////////////////////////////////////////////
typedef struct _VBT_EDID_DTD
{
#pragma pack(1)
    WORD wPixelClock; // Pixel clock / 10000

    UCHAR ucHA_low;  // Lower 8 bits of H. active pixels
    UCHAR ucHBL_low; // Lower 8 bits of H. blanking
    union {
        UCHAR ucHAHBL_high;
        struct
        {
            UCHAR ucHBL_high : 4; // Upper 4 bits of H. blanking
            UCHAR ucHA_high : 4;  // Upper 4 bits of H. active pixels
        };
    };

    UCHAR ucVA_low;  // Lower 8 bits of V. active lines
    UCHAR ucVBL_low; // Lower 8 bits of V. blanking
    union {
        UCHAR ucVAVBL_high;
        struct
        {
            UCHAR ucVBL_high : 4; // Upper 4 bits of V. blanking
            UCHAR ucVA_high : 4;  // Upper 4 bits of V. active pixels
        };
    };

    UCHAR ucHSO_low;  // Lower 8 bits of H. sync offset
    UCHAR ucHSPW_low; // Lower 8 bits of H. sync pulse width
    union {
        UCHAR ucVSOVSPW_low;
        struct
        {
            UCHAR ucVSPW_low : 4; // Lower 4 bits of V. sync pulse width
            UCHAR ucVSO_low : 4;  // Lower 4 bits of V. sync offset
        };
    };
    union {
        UCHAR ucHSVS_high;
        struct
        {
            UCHAR ucVSPW_high : 2; // Upper 2 bits of V. sync pulse width
            UCHAR ucVSO_high : 2;  // Upper 2 bits of V. sync offset
            UCHAR ucHSPW_high : 2; // Upper 2 bits of H. sync pulse width
            UCHAR ucHSO_high : 2;  // Upper 2 bits of H. sync offset
        };
    };

    UCHAR ucHIS_low; // Lower 8 bits of H. image size in mm
    UCHAR ucVIS_low; // Lower 8 bits of V. image size in mm
    union {
        UCHAR ucHISVIS_high;
        struct
        {
            UCHAR ucVIS_high : 4; // Upper 4 bits of V. image size
            UCHAR ucHIS_high : 4; // Upper 4 bits of H. image size
        };
    };

    UCHAR ucHBorder; // H. border in pixels
    UCHAR ucVBorder; // V. border in pixels

    union {
        UCHAR ucFlags; // Hsync & Vsync polarity, etc. flags
        struct
        {
            UCHAR ucStereo1 : 1;    // Stereo definition with bit[6:5]
            UCHAR ucHSync_Pol : 1;  // Hsync polarity (0: Neg, 1: Pos)
            UCHAR ucVSync_Pol : 1;  // Vsync polarity (0: Neg, 1: Pos)
            UCHAR ucSync_Conf : 2;  // Sync configuration
                                    // 00 : Analog composite
                                    // 01 : Bipolar analog composite
                                    // 00 : Digital composite
                                    // 00 : Digital separate
            UCHAR ucStereo2 : 2;    // Stereo definition
                                    // 00 : Normal display, no stereo
                                    // xx : Stereo definition with bit0
            UCHAR ucInterlaced : 1; // Interlaced / Non-interlaced
                                    // 0 : Non-interlaced
                                    // 1 : Interlaced
        };
    };
#pragma pack()
} VBT_EDID_DTD, *PVBT_EDID_DTD;

typedef struct _VBT_OEM_CUSTOM_TIMING
{
    VBT_EDID_DTD DTD_Data;
} VBT_OEM_CUSTOM_TIMING, *PVBT_OEM_CUSTOM_TIMING;

#define MAX_MODE_ADDITION_ENTRY 6

typedef struct _MODE_ADDITION_LIST
{
    ULONG                 ulXRes;
    ULONG                 ulYRes;
    UCHAR                 ucBppBitMask; // Note: Starts from 8bpp (not one 4bpp)
    USHORT                usRRate;
    VBT_OEM_CUSTOM_TIMING OemTiming;
} MODE_ADDITION_LIST, *PMODE_ADDITION_LIST;

typedef struct _VBT_MODE_ADDITION_TABLE
{
    MODE_ADDITION_LIST ModeAdditionList[MAX_MODE_ADDITION_ENTRY];
    ULONG              ulNumMode;
    ULONG              ulDisplayType;
} VBT_MODE_ADDITION_TABLE, *PVBT_MODE_ADDITION_TABLE;

/////////////////////////////////////////////
//
// Arguments for GetLvdsSSCVbt
//
/////////////////////////////////////////////
typedef union _VBT_LVDS_SSC {
    UCHAR LvdsSsc;
    struct
    {
        UCHAR LVDS_SSC_Enabled : 1;
        UCHAR LVDS_SSC_66MHz : 1;
        UCHAR Disable_SSC_In_DDT : 1;
        UCHAR Reserved : 5;
    };
} VBT_LVDS_SSC, *PVBT_LVDS_SSC;

/////////////////////////////////////////////
//
// GetExtDPSsc
/////////////////////////////////////////////
typedef struct _VBT_EXT_DP_SSC
{
    BOOLEAN bExtDPSscEnabled;
    BOOLEAN bExtDPEnableSscForDongle;
    ULONG   ulExtDPSscFreq; // In Khz
} VBT_EXT_DP_SSC, *PVBT_EXT_DP_SSC;

/////////////////////////////////////////////
//
// Arguments for GetGeneralVbtInfo
//
/////////////////////////////////////////////
typedef struct _VBT_GENERAL_INFO
{
    union {
        ULONG VbtGeneralInfo;

        struct
        {
            ULONG bAllowFSDOSSwitch : 1;
            ULONG bStaticDevice : 1;
            ULONG bNoDetectToggle : 1;
            ULONG bLegacyMonitorDetect : 1;
            ULONG bNonACPIDPMS : 1;
            ULONG bUsePrimaryTiming : 1;
            ULONG bGTFCheckEnabled : 1;
            ULONG bSDVOPowerDownFeature : 1;
            ULONG bSBIOSInt10 : 1;
            ULONG bAspectScalingEnabled : 1;
            ULONG bPreserveAspectRatio : 1;
            ULONG bDVI_I_ConnectorEnabled : 1;
            ULONG ucLvdsConfig : 2; // RCR LVDS configuration bits (Valid only from VBT version 125)
                                    //  0x00,  "No LVDS"
                                    //  0x01,  "Integrated LVDS"
                                    //  0x02,  "SDVO-LVDS"
                                    //  0x03,  "Both Integrated and SDVO LVDS" (This option is valid till BDB version 140)
            // RCR 929577
            ULONG bIntCRTSupported : 1;
            ULONG bIntTVSupported : 1;
            ULONG bIntHDMISupport : 1;
            ULONG bEmbeddedDPSupport : 1; // embedded DP support from BDB version 141
            // Platform Clock Mode..
            ULONG bAllowCDClockChange : 1; // Support for dynamic cd clock change
            UCHAR bEmbeddedPlatformEnable : 1;
            ULONG bDisplayDisabledPlatform : 1; // 0 = Display not disabled, 1 = Display Disabled.
            ULONG bIgnoreStrapState : 1;        // 1 = ignore strap state for DP, HDMI ports
            ULONG bIntMIPISupportOnPortA : 1;   // 0 - MIPI not present on Port-A, 1 - MIPI present on Port-A
            ULONG bIntMIPISupportOnPortC : 1;   // 0 - MIPI not present on Port-C, 1 - MIPI present on Port-C
            ULONG bMIPIRGBColorSeparation : 1;  // 1 - MIPI panel requires color separation
            ULONG ulDDIEEnabledinVBT : 1;
            ULONG ulDDIAEnabledAsDP : 1; // DDI-A enabled as Dp or VGA
            ULONG ulReserved : 5;
        };
    };

    // CRT DDC port info
    ULONG ulAnalogCRTDDCGPIOPort;
    ULONG ulAnalogCRTDDC_SDVOAddress;      // valid if ulAnalogCRTDDCGPIOPort is the sDVO GPIO pin (Value is 70/72)
    UCHAR ucAnalogCRTDDC_SDVODDCSelection; // DDC1/DDC2 selection if ulAnalogCRTDDCGPIOPort is sDVO pin (default is DDC1)
    UCHAR ucCompressionStrucIndex;         // Compression Struc Index

} VBT_GENERAL_INFO, *PVBT_GENERAL_INFO;

/////////////////////////////////////////////
//
// Arguments for GetIntLvdsPanelDetails
//
/////////////////////////////////////////////
typedef struct _VBT_PANEL_PARAMETERS
{
    ULONG ulRegisterOffset;
    ULONG ulRegisterValue;
} VBT_PANEL_PARAMETERS, *PVBT_PANEL_PARAMETERS;

typedef struct _VBT_PANEL_BLC_PARAMETERS
{
#pragma pack(1)

    union {
        ULONG ulBlcCaps; // BLC capabilities
        struct
        {
            ULONG bBlcSupported : 1;              // BLC Supported? (from VBT)
            ULONG bBlcEnabled : 1;                // BLC Enabled? (from SBIOS)
            ULONG bBlcMinBrightnessSupported : 1; // BLC Minimum brightness field supported?
            ULONG bBlcI2CAddrSupported : 1;       // BLC I2CAddr invertor field supported?
            ULONG bBlcBrightnessCmd : 1;          // BLC I2C inverter command code supported?
            ULONG bBlcReserved : 27;              // Reserved
        };
    };
    UCHAR  ucBlcType;          // BLC Inverter Type
    UCHAR  ucBlcPolarity;      // BLC Inverter Polarity
    UCHAR  ucBlcGpioPins;      // BLC Inverter GPIO Pins (I2C)
    ULONG  ulBlcBlockSize;     // BLC VBT Block Size
    USHORT usBlcFrequency;     // BLC Inverter Frequency (PWM)
    UCHAR  ucBlcGMBusSpeed;    // BLC inverter GMBus speed
    UCHAR  ucMinBrightness;    // Minimum Brightness, 0 - 255
    UCHAR  ucBlcI2cAddr;       // I2C inverter Slave address
    UCHAR  ucBlcBrightnessCmd; // I2C inverter command code

#pragma pack()
} VBT_PANEL_BLC_PARAMETERS, *PVBT_PANEL_BLC_PARAMETERS;

#define MAX_VBT_PANEL_PARAMETERS_SIZE 5

typedef struct tag_VBT_LVDS_PNP_ID_DATA
{
#pragma pack(1)
    USHORT IdMfgName;     // ID Manufacturer Name
    USHORT IdProductCode; // ID Product Code
    ULONG  IdSerialNum;   // ID Serial Number
    UCHAR  MfgWeek;       // Week of Manufacture
    UCHAR  MfgYear;       // Year of Manufacture
#pragma pack()
} VBT_LVDS_PNP_ID_DATA, *PVBT_LVDS_PNP_ID_DATA, VBT_EDP_PNP_ID_DATA, *PVBT_EDP_PNP_ID_DATA;

typedef struct _VBT_PANEL_INFO
{
    // Panel Name
    UCHAR ucPanelName[13];

    // Panel width & height
    ULONG ulPanelWidth;
    ULONG ulPanelHeight;

    // Panel parameters
    UCHAR ucMaxPanelParameters;

    VBT_PANEL_PARAMETERS stPanelParameters[MAX_VBT_PANEL_PARAMETERS_SIZE];

    // Panel timings
    VBT_EDID_DTD stPanelTiming;

} VBT_PANEL_INFO, *PVBT_PANEL_INFO;

#define MAX_VBT_PANEL_TYPES 16

//////////////////////////////////////////////////
//
// GMCH_DOTCLOCK_OVERRIDE_ENTRY
//
//////////////////////////////////////////////////
typedef struct _GMCH_DOTCLOCK_OVERRIDE_ENTRY
{
#pragma pack(1)
    ULONG ulFrequency; // In Hz

    UCHAR ulNDivisor;
    UCHAR ulM1Divisor;
    UCHAR ulM2Divisor;
    UCHAR ulP1PostDivisor;
    UCHAR ulP2ClockDivide;
#pragma pack()
} GMCH_DOTCLOCK_OVERRIDE_ENTRY, *PGMCH_DOTCLOCK_OVERRIDE_ENTRY;

#define MAX_VBT_DOTCLOCK_OVERRIDE_ENTRIES 10

typedef struct _VBT_DOTCLOCK_OVERRIDE_TABLE
{
    UCHAR                        ucMaxDotClockOverideEntries;
    GMCH_DOTCLOCK_OVERRIDE_ENTRY stDotClockOverrideTable[MAX_VBT_DOTCLOCK_OVERRIDE_ENTRIES];
} VBT_DOTCLOCK_OVERRIDE_TABLE, *PVBT_DOTCLOCK_OVERRIDE_TABLE;

#define MAX_VBT_LVDS_DOTCLOCK_OVERRIDE_ENTRIES 5

typedef struct _VBT_PANEL_DATA
{
    // Panel type as set in VBT/CMOS
    UCHAR ucPanelType; // Note: Starts from 1..16
    // Panel Name;
    UCHAR ucPanelName[13];

    // Panel width & height
    ULONG ulPanelWidth;
    ULONG ulPanelHeight;

    // PnPID
    VBT_LVDS_PNP_ID_DATA stPnPID;

    // Does the panel supports EDID?
    BOOLEAN bEDIDSupportedPanel;

    // LVDS DDC GPIO port value (used if bEDIDSupportedPanel is set)
    ULONG ulDDCGPIOPort;
    // GPIO port for BLC
    ULONG ulBLCGPIOPort;

    // SSC Information
    BOOLEAN bIsSSCEnabled;
    ULONG   ulSSCFrequency;        // In Hz
    BOOLEAN bDisableSSCInTwin;     // Overrides bIsSSCEnabled for twin configs
    UCHAR   ucNoOfChannels;        // No. of Channels for LVDS. i.e Single or Dual.
    UCHAR   ucDPSPanel_Type;       // 1 = Static DRRS, 2 = D2PO(Obsolete) 3 = Seamless.
    UCHAR   ucBackLightTechnology; // 0 = Dont care, 1 = CCFL, 2 = LED.
    UCHAR   ucBlcType;             // BLC Inverter Type
    // Dot clock override table for LVDS
    // TODO
    UCHAR                        ucMaxDotClockOverideEntries;
    GMCH_DOTCLOCK_OVERRIDE_ENTRY stLVDSDotClockOverrideTable[MAX_VBT_LVDS_DOTCLOCK_OVERRIDE_ENTRIES];

    // Panel specific information (timings, PnPID etc.)
    // Note: Panel info for panel type X is at stPanelInfo[X-1]
    UCHAR          ucMaxPanelInfo;
    VBT_PANEL_INFO stPanelInfo[MAX_VBT_PANEL_TYPES];

    BOOLEAN bIs24bitPanel;       // Panel Color Depth value.
    BOOLEAN bDownscalingenabled; // 0 -Downscaling disabled, 1 - Downscaling enabled
    UCHAR   ucMipiDrrsMinRR;     // Min RR coming in from VBT/Inf

    UCHAR        ucBlcPWMControllerNumber; // If PMIC pin is used for brightness control, this says 0 = PMIC PWM0, 1 = PWM1, 2 = PWM2, 3 = PWM3
    UCHAR        ucBlcPWMControllerType;   // 0 = PMIC pin, 1 = LPSS PWM, 2 = Display DDI, 3 = CABC, Others = Reserved
    VBT_BLC_DATA Blc;
} VBT_PANEL_DATA, *PVBT_PANEL_DATA;

////////////////////////////////////////////////////
// Embedded DP data structures
//
////////////////////////////////////////////////////
#define MAX_VBT_EMBEDDED_DP_PANEL_TYPES 16
#define VBT_EDP_COLORDEPTH_MASK 0x3

//
// Panel power sequencing delays
//

// The panel power sequence delays are as per Vesa eDP spec.
// For more details please refer to VESA eDP spec
typedef enum _VBT_PP_SEQUENCING_REGISTER_TYPE_ENUM
{
    eT1AndT2PowerUpDelay           = 0, // T1 + T2 (Row 1) -  Power-Up delay.
    eT5PwrOnToBackLightEnDelay     = 1, // T5 (Row 2) - Power-On to Backlight Enable delay.
    eT6BackLightOffToPowerDwnDelay = 2, // T6 (Row 3) - Backlight-Off to Power-Down delay.
    eT3PowerDwnDelay               = 3, // T3 (Row 4) - Power-Down delay.
    eT4PowerCycleDelay             = 4, // T4 (Row 5) - Power cycle delay
} VBT_PP_SEQUENCING_REGISTER_TYPE_EN;

typedef enum _VBT_PP_SEQUENCING_FOR_PWM
{
    ePwmOntoBkltOnDelay        = 6,
    eBkltOfftoPwmoffDelay      = 7,
    eMaxPanelPowerSeqIntervals = 8
} VBT_PP_SEQUENCING_WITH_PWM;

typedef enum _VBT_EDP_PP_SEQUENCING_REGISTER_TYPE_ENUM
{
    eEmbDPT3PowerUpDelay                = 0, // T3 -  Power-Up delay.
    eEmbDPT8PwrOnToBackLightEnDelay     = 1, // T8 (Row 2) - Power-On to Backlight Enable delay.
    eEmbDPT9BackLightOffToPowerDwnDelay = 2, // T9 (Row 3) - Backlight-Off to Power-Down delay.
    eEmbDPT10PowerDwnDelay              = 3, // T10 (Row 4) - Power-Down delay.
    eEmbDPT12PowerCycleDelay            = 4, // T12 (Row 5) - Power cycle delay
    eEmbDPMaxPanelPowerSeqIntervals     = 5
} VBT_EDP_PP_SEQUENCING_REGISTER_TYPE_ENUM;

#pragma pack(1)
typedef struct _VBT_EDP_PANELPOWER_SEQUENCING_TABLE
{
    // Panel power seuencing registers
    // 1. T1+T2
    // 2. T5
    // 3. T6
    // 4. T3
    // 5. T4
    USHORT regdata[eEmbDPMaxPanelPowerSeqIntervals]; // Uses VBT_PP_SEQUENCING_REGISTER_TYPE_EN for indexing
} VBT_EDP_PANELPOWER_SEQUENCING_TABLE, *PVBT_EDP_PANELPOWER_SEQUENCING_TABLE;

typedef struct _VBT_PWM_ON_OFF_DELAY_TABLE
{
    USHORT ulPwmOntoBkltOnDelay;
    USHORT ulBkltOfftoPwmOffDelay;
} VBT_PWM_ON_OFF_DELAY_TABLE, *PVBT_PWM_ON_OFF_DELAY_TABLE;

#pragma pack()
//
// Panel Parameters : Needed to support
// aux without any handshake
//
typedef enum _VBT_EMBEDDED_PANEL_LINKRATE_ENUM
{
    eVbt1_62Gbps = 0,
    eVbt2_7Gbps  = 1,
    eVbt5_4Gbps  = 2,
    eVbtReservedLinkRate // for future usage
} VBT_EMBEDDED_PANEL_LINKRATE_EN;

typedef enum _VBT_EMBEDDED_PANEL_LANECFG_ENUM
{
    eVbt1xLaneConfig = 0,
    eVbt2xLaneConfig = 1,
    eVbt4xLaneConfig = 3,
    eVbtInvalidLaneConfig
} VBT_EMBEDDED_PANEL_LANECFG_EN;

typedef enum _VBT_EMBEDDED_PANEL_PREEMPH_CFG_ENUM
{
    eVbtNoPreemp    = 0,
    eVbt3_5DbPreemp = 1,
    eVbt6DbPreemp   = 2,
    eVbt9_5DbPreemp = 3,
    eVbtReservedPreemp
} VBT_EMBEDDED_PANEL_PREEMPH_CFG_EN;

typedef enum _VBT_EMBEDDED_PANEL_VSWING_CFG_ENUM
{
    eVbtVswing0_4V = 0,
    eVbtVswing0_6V = 1,
    eVbtVswing0_8V = 2,
    eVbtVswing1_2V = 3,
    eVbtVswingRserved
} VBT_EMBEDDED_PANEL_VSWING_CFG_EN;

typedef enum _VBT_EMBEDDED_PANEL_BLC_CONTROLLER_PIN_CFG
{
    eBLC_CTRL_PMIC = 0,
    eBLC_CTRL_LPSS,
    eBLC_CTRL_Display,
    eBLC_CTRL_CABC,
    eBLC_CTRL_Reserved
} VBT_EMBEDDED_PANEL_BLC_CONTROLLER_PIN_CFG;

typedef enum _VBT_EMBEDDED_PANEL_BLC_PMIC_PWM_CFG
{
    eBLC_PWM0 = 0,
    eBLC_PWM1,
    eBLC_PWM2,
    eBLC_PWM3,
    eBLC_Reserved
} VBT_EMBEDDED_PANEL_BLC_CONTROLLER_PIN_NUM;

//
// Structure define various panel params
//
typedef union _VBT_EMBEDDED_PANEL_PARAMETERS {
    USHORT usPanelParams;
    struct
    {
        USHORT usLinkRate : 4;           // bit[3:0]  uses VBT_EMBEDDED_PANEL_LINKRATE_EN
        USHORT usNumOfLanesInUse : 4;    // bit[7:4]  uses VBT_EMBEDDED_PANEL_LANECFG_EN
        USHORT usCurrentPreEmpLevel : 4; // bit[11:8] uses VBT_EMBEDDED_PANEL_PREEMPH_CFG_EN
        USHORT usCurrentSwingLevel : 4;  // bit[15:12]uses VBT_EMBEDDED_PANEL_VSWING_CFG_EN
    };
} VBT_EMBEDDED_PANEL_PARAMETERS, *PVBT_EMBEDDED_PANEL_PARAMETERS;

typedef union _VBT_EDP_START_PRESET_VALUES {
    UCHAR ucStartPresetValue;
    struct
    {
        UCHAR ucStartPreEmpLevel : 4;
        UCHAR ucStartVSwingLevel : 4;
    };
} VBT_EMBEDDED_PANEL_START_PRESET_VALUES, *PVBT_EMBEDDED_PANEL_START_PRESET_VALUES;

//
// Embedded DP Per panel info
//
typedef struct _VBT_EMBEDDED_DP_PANEL_INFO
{
    // Panel Name
    UCHAR ucPanelName[13];
    // Panel width & height
    ULONG ulPanelWidth;
    ULONG ulPanelHeight;

    // Panel Power sequencing registers
    VBT_EDP_PANELPOWER_SEQUENCING_TABLE stPanelPowerSeqParams;

    // Panel timings
    VBT_EDID_DTD stPanelTiming;
    // Link Parameters
    VBT_EMBEDDED_PANEL_PARAMETERS stPanelLinkParams;

    // Link Training starting parameters
    VBT_EMBEDDED_PANEL_START_PRESET_VALUES stPanelStartPresetValues;

    // TBD : Add dithering algo to be used
} VBT_EMBEDDED_DP_PANEL_INFO, *PVBT_EMBEDDED_DP_PANEL_INFO;

typedef struct _VBT_EMBEDDED_DP_PANEL_DATA
{
    // Panel Name
    UCHAR ucPanelName[13];
    // Panel width & height
    ULONG ulPanelWidth;
    ULONG ulPanelHeight;

    // Panel type as set in VBT/CMOS
    UCHAR ucPanelType;

    // Pnp ID
    VBT_LVDS_PNP_ID_DATA stPnPID;

    // GPIO port for BLC
    ULONG ulBLCGPIOPort;

    // Panel specific information
    UCHAR                      ucMaxPanelInfo;
    VBT_EMBEDDED_DP_PANEL_INFO stPanelInfo[MAX_VBT_EMBEDDED_DP_PANEL_TYPES];

    // SSC specfic data
    BOOLEAN bIsSSCEnabled;
    ULONG   ulSSCFrequency; // In Hz

    // Parameters valid when EDID is not present
    // Bits Per Color
    UCHAR ucPanelColorDepth; // 6/8/10

    // Does the panel supports EDID?
    BOOLEAN bEDIDSupportedPanel;

    UCHAR        ucDPSPanel_Type;          // 0 = Static DRRS, 1 = D2PO(obsolete), 2 = Seamless.
    UCHAR        ucBackLightTechnology;    // 0 = Dont care, 1 = CCFL, 2 = LED.
    UCHAR        ucBlcType;                // BLC Inverter Type
    UCHAR        ucBlcPWMControllerNumber; // If PMIC pin is used for brightness control, this says 0 = PMIC PWM0, 1 = PWM1, 2 = PWM2, 3 = PWM3
    UCHAR        ucBlcPWMControllerType;   // 0 = PMIC pin, 1 = LPSS PWM, 2 = Display DDI, 3 = CABC, Others = Reserved
    VBT_BLC_DATA Blc;
    UCHAR        ucMSA_Timing_Delay; // 0 = Line1, 1 = Line2, 2 = Line3, 3 = Line4

    // Does the panel supports S3D
    BOOLEAN bS3DSupported;

    BOOLEAN bIsT3OptimizationEnabled;
    BOOLEAN bEdpFLTSupportOnPanel;
    UCHAR   ucVswingPreemphTable; // 0 =Table 1, 1 = Table 2, others reserved
    USHORT  usPwmOntoBkltOndelay;
    USHORT  usBkltOfftoPwmOffdelay;
    BOOLEAN bDownscalingenabled; // 0 -Downscaling disabled, 1 - Downscaling enabled
    BOOLEAN bTrainLinkStartParamEnabled;

    BOOLEAN bPPSWaForeDP2LVDSBridge;

    BOOLEAN bForceLCDVCCOnS0;
    USHORT  usPWMFrequency;
} VBT_EMBEDDED_DP_PANEL_DATA, *PVBT_EMBEDDED_DP_PANEL_DATA;

/////////////////////////////////////////////
//
// Arguments for UaimGetEncoderData
//
/////////////////////////////////////////////
#define VBT_AIMID_SIZE 9

typedef struct _VBT_UAIM_ENCODER_INFO
{
#pragma pack(1)
    UCHAR  ucVBTDisplayIndexType; // This will be used to get the Display Type Index
    UCHAR  ucReserved1;
    USHORT usDevType;               // Child device type
    UCHAR  ucI2C_Speed;             // I2C Speed
    UCHAR  ucDevID[VBT_AIMID_SIZE]; // 9 byte device ID (spare field, not used by vbios or softbios)
    USHORT usPresent;               // 0 = Not present, Non-zero = present
    UCHAR  ucDVO;                   // DVO port child device attached to
    UCHAR  ucI2C_Pins;              // I2C bus type
    UCHAR  ucI2C_Addr;              // I2C Slave address
    UCHAR  ucDDC_Pins;              // DDC bus type
    USHORT Reserved2;
    UCHAR  ucDVO_Config; // DVO configuration
    UCHAR  Reserved3;    // Earlier definition: ucDVO_2; // Secondary DVO port if Dual Link DVO
    // Following byte can be defined in different ways by VBIOS
    union {
        // Earlier definition: UCHAR   ucI2C_Pins_2;  // Secondary I2C bus type if Dual Link DVO
        UCHAR ucCompatibilityFlag;
        struct
        {
            UCHAR bIsHDMICompatible : 1; // This bit reflects the HDMI compatible bit in device class defn.
            UCHAR bIsDPCompatible : 1;   // This bit reflects the DP compatible bit in device class defn
            UCHAR bIsTMDSCompatible : 1; // This bit reflects the DVI compatiblity
            UCHAR ucReserved5 : 5;
        };
    };
    USHORT
    Reserved4; // Earlier Definition: UCHAR   ucI2C_Addr_2;  // Secondary I2C Slave Addr if Dual Link DVO &  UCHAR   ucDDC_Pins_2;  // Secondary DDC bus type if Dual Link DVO
    UCHAR  ucCapabilities;  // Capabilities bits:
    UCHAR  ucDVOWiring;     // DVO Wiring
    UCHAR  ucSec_DVOWiring; // Secondary DVO Wiring if Dual Link DVO
    USHORT usDeviceClassEx; // Extended Upperword of Device Class
    UCHAR  ucDVO_Function;  // SDVO functions
#pragma pack()
} VBT_UAIM_ENCODER_INFO, *PVBT_UAIM_ENCODER_INFO;

//
// Struct representing all the VBT encoder data
//
#define MAX_VBT_ENCODERS 5
#define MAX_INT_HDMI_ENCODERS 2
#define MAX_INT_DP_ENCODERS 2

typedef struct _VBT_UAIM_ENCODER_DATA
{
    UCHAR                 ucNumEncoders;
    VBT_UAIM_ENCODER_INFO stVBTEncoder[MAX_VBT_ENCODERS];
} VBT_UAIM_ENCODER_DATA, *PVBT_UAIM_ENCODER_DATA;

////////////////////////////////////////////////
//
// Under scan data from VBTManager
//
////////////////////////////////////////////////
// RCR 288519 : HDTV Modes through DVI
typedef enum _VBT_UNDERSCAN_OPTIONS
{
    eEnableUnderScanAndOverScan = 0x0,
    eEnableOverScanOnly         = 0x1,
    eEnableUnderScanOnly        = 0x2
} VBT_UNDERSCAN_OPTIONS;
typedef struct _VBT_UNDERSCAN_INFO
{
    VBT_UNDERSCAN_OPTIONS eComponentUnderScanOptions; // Options for HDTV via YPrPb
    VBT_UNDERSCAN_OPTIONS eDVIUnderScanOptions;       // Options for HDTV via DVI/HDMI
} VBT_UNDERSCAN_INFO, *PVBT_UNDERSCAN_INFO;

/////////////////////////////////////////////////
// TBD:  The VBT block for HDMI dispalys is not
// done. This structure is just the basic data
// that it can have and will change as per the
// actual implementation
// Integrated HDMI VBT data block
//
////////////////////////////////////////////////
#define MAX_VBT_INT_EFP_ENCODERS 5

// BMP defined port definitions for integrated EFP type
typedef enum _VBT_INT_EFP_PORT_TYPE
{
    eNotApplicable = 0,
    eHDMI_B        = 1,
    eHDMI_C        = 2,
    eHDMI_D        = 3,
    eDPORT_B       = 7,
    eDPORT_C       = 8,
    eDPORT_D       = 9,
    eDPORT_A       = 10, // From ILK onwards
    eDPORT_E       = 11,
    eHDMI_E        = 12,
    eDPORT_F       = 13,
    eHDMI_F        = 14,
    eMIPI_A        = 21, // VLV onwards
    eMIPI_C        = 23,
    eUndefined
} VBT_INT_EFP_PORT_TYPE;

// BMP defined physical connector. This enum will
// be useful for configuring the driver based upon physical
// connector out on the motherboard
typedef enum _VBT_INT_EFP_PHY_CONNECTOR_TYPE
{
    eInvalidConnector       = 0,
    eHDMICertifiedConnector = 1,
    eDPConnector            = 2,
    eDVIConnecor            = 3,
    eReservedConnector
} VBT_INT_EFP_PHY_CONNECTOR_TYPE;

//
// VBT_DEVICE_CLASS_DEFN : Device class defn
//
typedef union _VBT_DEVICE_CLASS_DEFN {
    USHORT usDevType;
    struct
    {
        USHORT usAnalogPort : 1;          // bit 0
        USHORT usDigitalOp : 1;           // bit 1
        USHORT usDisplayPort : 1;         // bit 2
        USHORT usVideoSignalling : 1;     // bit 3
        USHORT usTMDSSignalling : 1;      // bit 4
        USHORT usLVDSSignalling : 1;      // bit 5
        USHORT usHighSpeedSignalling : 1; // bit 6
        USHORT usContentProtection : 1;   // bit 7
        USHORT usReserved1 : 1;           // bit 8
        USHORT usCompositeOp : 1;         // bit 9
        USHORT usComponentOp : 1;         // bit 10
        USHORT usNotHDMICapable : 1;      // bit 11
        USHORT usInternalConnection : 1;  // bit 12
        USHORT usHPDSignalling : 1;       // bit 13
        USHORT usPowerMgmt : 1;           // bit 14
        USHORT usClassExtension : 1;      // bit 15
    };
} VBT_DEVICE_CLASS_DEFN;

typedef union _VBT_DP_ONDOCK_REDRIVER_DEFN {
    UCHAR ucOnDockRedriver;
    struct
    {
        UCHAR ucDockPreempLevel : 3;        // bit 2-0
        UCHAR ucDockVolSwing : 3;           // bit 5-3
        UCHAR ucOnDockRedriverPresence : 1; // bit 6
        UCHAR ucReserved : 1;               // bit 7
    };
} VBT_DP_ONDOCK_REDRIVER_DEFN;

typedef union _VBT_DP_ONBOARD_REDRIVER_DEFN {
    UCHAR ucOnBoardRedriver;
    struct
    {
        UCHAR ucBoardPreempLevel : 3;        // bit 2-0
        UCHAR ucBoardVolSwing : 3;           // bit 5-3
        UCHAR ucOnBoardRedriverPresence : 1; // bit 6
        UCHAR ucReserved : 1;                // bit 7
    };
} VBT_DP_ONBOARD_REDRIVER_DEFN;

// VBT structure for integrated EFP(HDMI/DP)
typedef struct _VBT_INT_EFP_ENCODER_INFO
{
#pragma pack(1)
    UCHAR                        ucVBTDisplayIndexType; // This will be used to get the Display Type Index
    UCHAR                        ucReserved1;           // Reserved
    VBT_DEVICE_CLASS_DEFN        stDevClass;            // Defines the device class type
    UCHAR                        ucI2CSpeed;
    VBT_DP_ONBOARD_REDRIVER_DEFN stOnBoardRedriver;
    VBT_DP_ONDOCK_REDRIVER_DEFN  stOnDockRedriver;
    union {
        UCHAR ucHDMILSIndex; // HDMI Level Shifter RCR
        struct
        {
            UCHAR ucHDMILSIndexValue : 5;
            UCHAR ucHDMIDataRateIndex : 3;
        };
    };
    UCHAR ucReserved2[2]; // Unused 2 bytes
    union {
        UCHAR ucFlags0; // Flags 0
        struct
        {
            UCHAR bIsEDIDlessEnabled : 1;  // RCR 1023193: EDID-less external displays;This bit reflects if the panel is EDIDless Enabled
            UCHAR bCompressionEnabled : 1; // 1 = Enable/0 = Disable compression for the particular display
            UCHAR bCompressionMethof : 1;  // Compression Method Selection; 0 : Compression using PPS, 1 : Compression using CPS
            UCHAR ucReserved9 : 5;
        };
    };
    UCHAR ucCompressionStrucIndex; // Compression structure index in block 55; 0x0 = Struc 0, 0x1 - Struc 1, ; others Rsvd.
    UCHAR ucReserved10[4];         // Unused 5 bytes
    UCHAR ucEFPPort;               // iHDMI/iDP port child device attached to. Of type VBT_INT_EFP_PORT_TYPE
    UCHAR ucReserved3[2];          // 2 bytes reserved
    UCHAR ucDDC_Pins;              // DDC bus type
    UCHAR ucReserved4[3];          // 3 bytes reserved
    union {
        UCHAR ucFlags1; // Flags 1
        struct
        {
            UCHAR bIsDockablePort : 1;
            UCHAR bIsLaneReversed : 1;
            UCHAR bHDMI2MBDownSupported : 1;
            UCHAR bIsIBoostEnabled : 1;
            UCHAR bIsHPDSenseInverted : 1;
            UCHAR ucReserved : 3;
        };
    };
    union {
        UCHAR ucCompatibilityFlag;
        struct
        {
            UCHAR bIsHDMICompatible : 1; // This bit reflects the HDMI compatible bit in device class defn.
            UCHAR bIsDPCompatible : 1;   // This bit reflects the DP compatible bit in device class defn
            UCHAR bIsTMDSCompatible : 1; // This bit reflects the DVI compatiblity
            UCHAR ucReserved5 : 5;
        };
    };
    UCHAR   ucAuxChannelType; // DP Aux channel type, uses enum DP_AUX_CHANNEL_TYPE_EN. Valid from BDB version 140
    BOOLEAN bDongleDetection; // For controlling Enabling/Disabling HDMI if Dongle detection feature is Enabled/Disabled in VBT
    union {
        UCHAR ucCapabilities; // Capabilities bits:
        struct
        {
            UCHAR ucPipeCaps : 2;
            UCHAR ucDVOStallAvail : 1;
            UCHAR ucHpdConnectStaus : 2;
            UCHAR bIsIntegratedEncoder : 1; // 1 = Integrated Encoder ; 0 = SDVO encoder
            UCHAR ucReserved7 : 2;
        };
    };
    UCHAR ucReserved8[5];
    union {
        UCHAR ucFlags2; // Flags 2
        struct
        {
            UCHAR bIsUSBTypeCEnabled : 1;
            UCHAR bIsTBTConnectorEnabled : 1;
            UCHAR ucReserved11 : 2;
            UCHAR ucVswingTableSel : 4;
        };
    };
    UCHAR  ucDP2XGpioResourceID; // Used for GPIO implementation of USB-C. Un-used in dynamic lane detection implementation
    USHORT ucDP2XGpioNumber;     // Used for GOP purposes only
    union {
        UCHAR ucIBoostMagnitude;
        struct
        {
            UCHAR ucDPIBoostMagnitude : 4;
            UCHAR ucHDMIIBoostMagnitude : 4;
        };
    };
#pragma pack()
} VBT_INT_EFP_ENCODER_INFO, *PVBT_INT_EFP_ENCODER_INFO;

//
// This structure will be used to gather the VBT specfici
// configuration data and will be used for enumeration of encoder
//
typedef struct _VBT_INT_EFP_ENCODER_DATA
{
    UCHAR                    ucNumEncoders;
    VBT_INT_EFP_ENCODER_INFO stIntEFPEncoder[MAX_VBT_INT_EFP_ENCODERS];
} VBT_INT_EFP_ENCODER_DATA, *PVBT_INT_EFP_ENCODER_DATA;

typedef struct _VBT_PSR_DETAILS
{
    BOOLEAN bPSREnable;
    BOOLEAN bLinkinStandby;       // 1-Yes....reverse of VBT setting
    BOOLEAN bSkipHandShakeOnExit; // 1-Yes
    UCHAR   ucIdleFramesNum;
    UCHAR   ucLinesNeededForLinkStandby;
    USHORT  usTP1WakeUpTime;
    USHORT  usTP2TP3WakeUpTime;
} VBT_PSR_DETAILS, *PVBT_PSR_DETAILS;
