/*
 *  Copyright© 1999-2003, Intel Corporation
 *
 *  $Workfile: mccsconsts.h
 *  $Revision: 
 *  $Modtime: 
 *
 *  Purpose:	
 *
 *
 *  Compiler:       Visual C++ 6.0  SP4
 *
 *  Ext Packages:   None
 *
 *  $Author: 
 *
 *  Revisions:	
 *
 *  Ashok V Huded,  PC 14.0 cleanup
 * 
 *
 */ 

#if !defined(_CUI_MCCSCONSTS_H_112512052000_E750_INCLUDED_)
#define _CUI_MCCSCONSTS_H_112512052000_E750_INCLUDED_


// AccessBUS addresses
#define	AB_HOST_ADDR			0x51
#define	AB_DEVICE_ADDR			0x6E

// Set VCP codes
#define AB_SETVCP_OPCODE		0x03
#define AB_SETVCP_LEN_BYTE		0x84

// Get VCP codes
#define AB_GETVCP_OPCODE		0x01
#define AB_GETVCP_LEN_BYTE		0x82
#define AB_GETVCP_REPLY_LEN		11		// 8+3

// Get Capabilities string code
#define AB_GETCAP_OPCODE		0xF3
#define AB_GETCAP_LEN_BYTE		0x83
#define AB_CAP_REPLY_LEN		38		// = 35 + 3(SourceByte + LengthByte + ChecksumByte)

// VCP REPLY return codes
#define AB_VCPCODE_SUPPORTED	0x00
#define AB_VCPCODE_NOTSUPPORTED 0x01


// Reset VCP code
#define AB_RESETVCP_OPCODE		0x09
#define AB_RESETVCP_LEN_BYTE	0x82


// Macro to get actual message len from the message len byte
#define	AB_GET_ABMSG_LEN(x)	((x) & 0x7F)

enum Command_OpCodes {
		ab_GetVCP			= 0x01,
		ab_GetVCPReply		= 0x02,
		ab_SetVCP			= 0x03,
		ab_Attention		= 0xE0,
		ab_IdentReply		= 0xE1,
		ab_CapabReply		= 0xE3,
		ab_ResourceRequest	= 0xE5,
		ab_PowerUsgReply	= 0xE6,
		ab_DevBWUsgReply	= 0xE8,
		ab_Reset			= 0xF0,
		ab_IdentRequest		= 0xF1,
		ab_AssignAddr		= 0xF2,
		ab_CapabRequest		= 0xF3,
		ab_ResourceGrant	= 0xF4,
		ab_EnableAppReport	= 0xF5,
		ab_PowerMgt			= 0xF6,
		ab_PresenceCheck	= 0xF7,
		ab_DevBWMgt			= 0xF8,
		ab_AppTest			= 0xB1,
		ab_AppHWSignal		= 0xA0,
		ab_AppTestReply		= 0xA1,
		ab_AppStatusMsg		= 0xA2
};

enum Continuous_Controls {
        mccs_Brightness              = 0x10,
        mccs_Contrast                = 0x12,
        mccs_RedVideoGain            = 0x16,
        mccs_GreenVideoGain          = 0x18,
        mccs_BlueVideoGain           = 0x1a,
        mccs_RedVideoBlackLevel      = 0x6c,
        mccs_GreenVideoBlackLevel    = 0x6e,
        mccs_BlueVideoBlackLevel     = 0x70,
        mccs_Focus                   = 0x1c,
        mccs_HorizPos                = 0x20,
        mccs_HorizSize               = 0x22,
        mccs_HorizPin                = 0x24,
        mccs_HorizPinBal             = 0x26,
        mccs_HorizMisconv            = 0x28,
        mccs_HorizLin                = 0x2a,
        mccs_HorizLinBal             = 0x2c,
        mccs_VertPos                 = 0x30,
        mccs_VertSize                = 0x32,
        mccs_VertPin                 = 0x34,
        mccs_VertPinBal              = 0x36,
        mccs_VertMisconv             = 0x38,
        mccs_VertLin                 = 0x3a,
        mccs_VertLinBal              = 0x3c,
        mccs_ParalDist               = 0x40,
        mccs_TrapDist                = 0x42,
        mccs_Tilt                    = 0x44,	// implemeted till here. donald
        mccs_TopCornerDistControl    = 0x46,
        mccs_TopCornerDistBal        = 0x48,
        mccs_BottomCornerDistControl = 0x4a,
        mccs_BottomCornerDistBal     = 0x4c,
        mccs_HorizMoire              = 0x56,
        mccs_VertMoire               = 0x58,
        mccs_HorizAdd                = 0x72,
        mccs_VertAdd                 = 0x74,
        mccs_BufferAdd               = 0x76,
        mccs_Update                  = 0x78,
        mccs_AdjustFocalPlane        = 0x7a,
        mccs_Trapezoid               = 0x7e,
        mccs_Keystone                = 0x80,
        mccs_HorizFlip               = 0x82,
        mccs_VertFlip                = 0x84,
        mccs_DisplayScaling          = 0x86,
        mccs_VelocityScanMod         = 0x88,
        mccs_TVColorSat              = 0x8a,
        mccs_TVSharpness             = 0x8c,
        mccs_TVHue                   = 0x90,
        mccs_TVBrightness            = 0x92
};

enum Non_Continuous_Controls {
		mccs_FactoryDefaults		 = 0x04,
        mccs_InputLevelSelect1       = 0x5e,
        mccs_OnScreenDisplay         = 0xca,
        mccs_InputLevelSelect2       = 0xcc,
        mccs_InputSourceSelect1      = 0x60,
        mccs_InputSourceSelect2      = 0xce,
        mccs_OutputSourceSelect1     = 0xd0,
        mccs_StereoMode              = 0xd4,
        mccs_DisplayPowerMode        = 0xd6,
        mccs_PresetColorTemp         = 0xd8,
        mccs_ScanFormat              = 0xda,
        mccs_DisplayMode             = 0xdc,
        mccs_OperationMode           = 0xde
};

enum Non_Continuous_RO_Controls {
        mccs_AutoSizeCenter          = 0xa2,
        mccs_PolarityHorizSync       = 0xa4,
        mccs_PolarityVertSync        = 0xa6,
        mccs_SyncType                = 0xa8,
        mccs_ScreenOrientation       = 0xaa,
        mccs_HorizFrequency          = 0xac,	// implemented
        mccs_VertFrequency           = 0xae		// implemented
};

enum Non_Continuous_WO_Controls {
        mccs_Degauss     = 0x01,				// implemented
        mccs_Settings    = 0xB0					
};

enum InputLevelSelectPoss {
        ilsp_None    = 0,
        ilsp_First   = 1, // 0.700 , 0.300 (1.0 Vpp)
        ilsp_Second  = 2, // 0.714 , 0.286 (1.0 Vpp)
        ilsp_Third   = 3, // 1.000 , 0.400 (1.0 Vpp)
        ilsp_Forth   = 4  // 0.700 , 0.000 (0.700 Vpp)
};

enum BooleanPoss {
        bp_None        = 0,
        bp_Disabled    = 1,
        bp_Enabled     = 2
};

enum InputSourceSelectPoss {
        issp_None            = 0,
        issp_DB_15HD_VGA1    = 1,
        issp_DB_15HD_VGA2    = 2,
        issp_DB_15HD_VGA3    = 3,
        issp_BNC_RGB1        = 4,
        issp_BNC_RGB2        = 5,
        issp_BNC_RGB3        = 6,
        issp_EVC1            = 7,
        issp_EVC2            = 8,
        issp_EVC3            = 9,
        issp_MAC1            = 10,
        issp_MAC2            = 11,
        issp_MAC3            = 12,
        issp_RCA_Comp1       = 13,
        issp_RCA_Comp2       = 14,
        issp_RCA_Comp3       = 15,
        issp_S_Video1        = 16,
        issp_S_Video2        = 17,
        issp_S_Video3        = 18,
        issp_SCART_Comp1     = 19,
        issp_SCART_Comp2     = 20,
        issp_SCART_RGB       = 21,
        issp_SCART_S_Video   = 22,
        issp_Tuner1          = 23,
        issp_Tuner2          = 24,
        issp_Tuner3          = 25,
        issp_YUV1            = 26,
        issp_YUV2            = 27,
        issp_YUV3            = 28
};

enum StereoModePoss {
        smp_None    = 0,
        smp_Mono    = 1,
        smp_FSREF   = 2,
        smp_FSLEF   = 3,
        smp_2WIREF  = 4,
        smp_2WILEF  = 5,
        smp_4WIDSB0 = 6,
        smp_4WIDSB1 = 7,
        smp_SBSI    = 8
};

enum DisplayPowerModePoss {
        dpmp_None    = 0,
        dpmp_On      = 1,
        dpmp_Standby = 2,
        dpmp_Suspend = 3,
        dpmp_Off     = 4
};

enum ScanFormatPoss {
        sfp_None        = 0,
        sfp_UnderScan   = 1,
        sfp_OverScan    = 2,
        sfp_LetterBox   = 3
};

enum DisplayModePoss {
        dmp_None            = 0,
        dmp_Productivity    = 1,
        dmp_Games           = 2,
        dmp_Movies          = 3
};

enum OperationModePoss {
        omp_None        = 0,
        omp_StandAlone  = 1,
        omp_Slave       = 2
};

//
// the following possiblity enums may not be correct.  The doc
// has them starting at 3 (PolaritySyncPoss::None) and going to
// 15 (ScreenOrientatinoPoss::Portrait) some how this looks like
// a documentation error (dwright)
//

enum PolaritySyncPoss {
        psp_None        = 0,
        psp_Negative    = 1,
        psp_Positive    = 2
};

enum SyncTypePoss {
        stp_None                = 0,
        stp_Separate            = 1,
        stp_DigitalComposite    = 2,
        stp_CompositeOnGreen    = 3
};

enum ScreenOrientationPoss {
        sop_None        = 0,
        sop_Landscape   = 1,
        sop_Portrait    = 2
};

enum SettingsPoss {
        sp_None            = 0,
        sp_Store           = 1,
        sp_RestoreFactory  = 2,
        sp_RestoreUser     = 3
};

enum Vendor_Controls {
        mccs_Vendor1 = 0xe0,
        mccs_Vendor2 = 0xe1,
        mccs_Vendor3 = 0xe2,
        mccs_Vendor4 = 0xe3,
        mccs_Vendor5 = 0xe4,
        mccs_Vendor6 = 0xe5,
        mccs_Vendor7 = 0xe6,
        mccs_Vendor8 = 0xe7,
        mccs_Vendor9 = 0xe8,
        mccs_Vendor10 = 0xe9,
        mccs_Vendor11 = 0xea,
        mccs_Vendor12 = 0xeb,
        mccs_Vendor13 = 0xec,
        mccs_Vendor14 = 0xed,
        mccs_Vendor15 = 0xee,
        mccs_Vendor16 = 0xef,
        mccs_Vendor17 = 0xf0,
        mccs_Vendor18 = 0xf1,
        mccs_Vendor19 = 0xf2,
        mccs_Vendor20 = 0xf3,
        mccs_Vendor21 = 0xf4,
        mccs_Vendor22 = 0xf5,
        mccs_Vendor23 = 0xf6,
        mccs_Vendor24 = 0xf7,
        mccs_Vendor25 = 0xf8,
        mccs_Vendor26 = 0xf9,
        mccs_Vendor27 = 0xfa,
        mccs_Vendor28 = 0xfb,
        mccs_Vendor29 = 0xfc,
        mccs_Vendor30 = 0xfd,
        mccs_Vendor31 = 0xfe,
        mccs_Vendor32 = 0xff
};

#endif	// _CUI_MCCSCONSTS_H_112512052000_E750_INCLUDED_
