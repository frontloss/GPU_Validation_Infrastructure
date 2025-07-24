

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:04 2015
 */
/* Compiler settings for IgfxBridgeUDT.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.00.0595 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__


#ifndef __IgfxBridgeUDT_h__
#define __IgfxBridgeUDT_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

/* header files for imported files */
#include "ocidl.h"

#ifdef __cplusplus
extern "C"{
#endif 


/* interface __MIDL_itf_IgfxBridgeUDT_0000_0000 */
/* [local] */ 

typedef /* [uuid] */  DECLSPEC_UUID("F6042533-B986-407a-87F7-02E542B3E351") 
enum GENERIC
    {
        MAX_GAMMA_ELEMENTS	= 256,
        MAX_NUM_MCCS_CTLS	= 0xff,
        MAX_NUM_VALUES	= 0xf,
        MAX_VALID_CONFIG	= 140,
        MAX_GRAPHICS_MODE	= 1200,
        BAR_INFO_SIZE	= 8,
        MAX_MONITORS_PER_ADAPTER	= 6,
        IGFX_FLAG_HDMI_DEIVCE_SUPPORT	= ( 1 << 31 ) ,
        IGFX_FLAG_NIVO_DEIVCE_SUPPORT	= ( 1 << 30 ) ,
        IGFX_FLAG_DP_DEVICE_SUPPORT	= ( 1 << 29 ) ,
        IGFX_CENTERING	= 0x1,
        IGFX_PANEL_FITTING	= 0x2,
        IGFX_ASPECT_SCALING	= 0x4,
        IGFX_SCALING_CUSTOM	= 0x8,
        IGFX_MEDIASCALING_FS	= 0x10,
        IGFX_MEDIASCALING_MAS	= 0x20,
        IGFX_MAINTAIN_DISPLAY_SCALING	= 0x40,
        IGFX_DATA_NOT_AVAILABLE	= 0,
        IGFX_DISABLE_DRIVER_PERSISTENCE	= 0x1,
        IGFX_ENABLE_DRIVER_PERSISTENCE	= 0x2,
        IGFX_DOUBLE_PRESISION_GAMMA	= 0x1000
    } 	GENERIC;

typedef /* [uuid] */  DECLSPEC_UUID("20F6C13C-B9A8-4fe6-8146-40312E4ECCFF") 
enum MCCS_STATUS_CODE
    {
        MCCS_OPEN	= 0x1,
        MCCS_CLOSE	= 0x2,
        MCCS_GET_MAX	= 0x3,
        MCCS_GET_MIN	= 0x4,
        MCCS_GET_CURRENT	= 0x5,
        MCCS_SET_CURRENT	= 0x6,
        MCCS_RESET_CONTROL	= 0x7,
        MCCS_GET_SUPPORTED	= 0x8,
        MCCS_GET_POSSIBLE	= 0x9
    } 	MCCS_STATUS_CODE;

typedef /* [uuid] */  DECLSPEC_UUID("45CDBED3-EB9F-4dd5-9D65-BCFAF9B56320") 
enum DISPLAY_ORIENTATION
    {
        IGFX_DISPLAY_ORIENTATION_0	= 0,
        IGFX_DISPLAY_ORIENTATION_90	= 0x1,
        IGFX_DISPLAY_ORIENTATION_180	= 0x2,
        IGFX_DISPLAY_ORIENTATION_270	= 0x3
    } 	DISPLAY_ORIENTATION;

typedef /* [uuid] */  DECLSPEC_UUID("687079F5-8076-4eb4-8336-6FB7AC2F253D") 
enum DISPLAY_DEVICE_CONFIG_FLAG
    {
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE	= 0x1,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDTWIN	= 0x2,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE	= 0x3,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDZOOM	= 0x4,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD	= 0x5,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE	= 0x6,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE	= 0x7,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE	= 0x8,
        IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE	= 0x9
    } 	DISPLAY_DEVICE_CONFIG_FLAG;

typedef /* [uuid] */  DECLSPEC_UUID("16FBBD97-4D23-4787-86A7-AF5FE0027268") 
enum REFRESHRATE_FLAGS
    {
        INTERLACED	= 0x1,
        PROGRESSIVE	= 0x2,
        MAX_REFRESH_RATE	= 0x14
    } 	REFRESHRATE_FLAGS;

typedef /* [uuid] */  DECLSPEC_UUID("AC23D61C-1F5E-4c0a-9FD4-CD023A1785A5") 
enum DISPLAY_CONFIG_CODES
    {
        IGFX_DISPLAY_CONFIG_FLAG_HORIZONTAL_PANNING	= 0x1,
        IGFX_DISPLAY_CONFIG_FLAG_VERTICAL_PANNING	= 0x2,
        IGFX_DISPLAY_CONFIG_FLAG_HORIZONTAL_SCALING	= 0x4,
        IGFX_DISPLAY_CONFIG_FLAG_VERTICAL_SCALING	= 0x8,
        IGFX_DISPLAY_CONFIG_FLAG_PHYSICAL_WIDTH	= 0x10,
        IGFX_DISPLAY_CONFIG_FLAG_PHYSICAL_HEIGHT	= 0x20,
        IGFX_DISPLAY_CONFIG_FLAG_DISPLAY_WIDTH	= 0x40,
        IGFX_DISPLAY_CONFIG_FLAG_DISPLAY_HEIGHT	= 0x80,
        IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION	= 0x100,
        IGFX_DISPLAY_CONFIG_FLAG_VIEWPORT	= 0x200,
        IGFX_DISPLAY_CONFIG_FLAG_ROTATION	= 0x400,
        IGFX_DISPLAY_CONFIG_FLAG_ROTATION_PORTRAIT	= 0x800,
        IGFX_DISPLAY_CONFIG_FLAG_ROTATION_LANDSCAPE	= 0x1000
    } 	DISPLAY_CONFIG_CODES;

typedef /* [uuid] */  DECLSPEC_UUID("10B686D9-FF06-4c92-9042-79A8992B658B") 
enum IGFX_ERROR_CODES
    {
        IGFX_SUCCESS	= 0,
        IGFX_REGISTRATION_ERROR	= 0x1,
        IGFX_INVALID_EVENTHANDLE	= 0x2,
        IGFX_INVALID_EVENTMASK	= 0x3,
        IGFX_CORRUPT_BUFFER	= 0x4,
        IGFX_UNSUPPORTED_GUID	= 0x5,
        IGFX_GETCONFIGURATION_ERROR	= 0x6,
        IGFX_DEREGISTRATION_ERROR	= 0x7,
        IGFX_INVALIDMONITOR_ID	= 0x8,
        IGFX_INVALIDCONFIG_FLAG	= 0x9,
        IGFX_SETCONFIGATION_ERROR	= 0xa,
        IGFX_INVALID_MCCS_HANDLE	= 0xc,
        IGFX_INVALID_MCCS_CONTROLCODE	= 0xd,
        IGFX_INVALID_MCCS_SIZE	= 0xe,
        IGFX_MCCS_DRIVER_ERROR	= 0xf,
        IGFX_MCCS_DEVICE_ERROR	= 0x10,
        IGFX_MCCS_INVALID_MONITOR	= 0x11,
        IGFX_POWER_API_NOT_SUPPORTED	= 0x13,
        IGFX_POWER_API_LOCKED	= 0x14,
        IGFX_POWER_API_INVALID_UNLOCK_REQUEST	= 0x15,
        IGFX_INVALID_POWER_HANDLE	= 0x16,
        IGFX_INVALID_POWER_POLICY	= 0x17,
        IGFX_UNSUPPORTED_POWER_POLICY	= 0x18,
        IGFX_POWERDEVICE_ERROR	= 0x19,
        IGFX_INVALID_DISPLAYID	= 0x1a,
        IGFX_WRONG_ASPECT_PREFERENCE	= 0x1b,
        IGFX_INVAILD_OPERATING_MODE	= 0x1c,
        IGFX_INVALID_GAMMA_RAMP	= 0x1d,
        IGFX_INVALID_CONNECTOR_SELECTION	= 0x1e,
        IGFX_INVALID_DEVICE_COMBINATION	= 0x1f,
        IGFX_SETCLONE_FAILED	= 0x20,
        IGFX_INVALID_RESOLUTION	= 0x21,
        IGFX_INVALID_CONFIGURATION	= 0x22,
        IGFX_UNSUPPORTED_INVERTER	= 0x23,
        IGFX_BACKLIGHT_PARAMS_INVALID_FREQ	= 0x24,
        IGFX_FAILURE	= 0x25,
        IGFX_INVALID_INDEX	= 0x26,
        IGFX_INVALID_INPUT	= 0x27,
        IGFX_INCORRECT_RESOLUTION_FORMAT	= 0x28,
        IGFX_INVALID_ORIENTATION_COMBINATION	= 0x29,
        IGFX_INVALID_ORIENTATION	= 0x2a,
        IGFX_INVALID_CUSTOM_MODE	= 0x2b,
        IGFX_EXISTING_MODE	= 0x2c,
        IGFX_EXISTING_BASIC_MODE	= 0x2d,
        IGFX_EXISTING_ADVANCED_MODE	= 0x2e,
        IGFX_EXCEEDING_BW_LIMITATION	= 0x2f,
        IGFX_EXISTING_INSUFFICIENT_MEMORY	= 0x30,
        IGFX_UNSUPPORTED_FEATURE	= 0x31,
        IGFX_PF2_MEDIA_SCALING_NOT_SUPPORTED	= 0x32,
        IGFX_INVALID_QUAN_RANGE	= 0x33,
        IGFX_INVALID_SCAN_INFO	= 0x34,
        IGFX_INVALID_BUS_TYPE	= 0x35,
        IGFX_INVALID_OPERATION_TYPE	= 0x36,
        IGFX_INVALID_BUS_DATA_SIZE	= 0x37,
        IGFX_INVALID_BUS_ADDRESS	= 0x38,
        IGFX_INVALID_BUS_DEVICE	= 0x39,
        IGFX_INVALID_BUS_FLAGS	= 0x40,
        IGFX_INVALID_POWER_PLAN	= 0x41,
        IGFX_INVALID_POWER_OPERATION	= 0x42,
        IGFX_INVALID_AUX_DEVICE	= 0x43,
        IGFX_INVALID_AUX_ADDRESS	= 0x44,
        IGFX_INVALID_AUX_DATA_SIZE	= 0x45,
        IGFX_AUX_DEFER	= 0x46,
        IGFX_AUX_TIMEOUT	= 0x47,
        IGFX_AUX_INCOMPLETE_WRITE	= 0x48,
        IGFX_INVALID_PAR_VALUE	= 0x49,
        IGFX_NOT_ENOUGH_RESOURCE	= 0x4a,
        IGFX_NO_S3D_MODE	= 0x4b,
        IGFX_LAYOUT_ERROR	= 0x37,
        IGFX_UNSUPPORTED_VERSION	= 0x50,
        IGFX_S3D_ALREADY_IN_USE_BY_ANOTHER_PROCESS	= 0x4c,
        IGFX_S3D_INVALID_MODE_FORMAT	= 0x4d,
        IGFX_S3D_INVALID_MONITOR_ID	= 0x4e,
        IGFX_S3D_DEVICE_NOT_PRIMARY	= 0x4f,
        IGFX_S3D_INVALID_GPU_MODE	= 0x50,
        IGFX_INADEQUATE_PRIVILEGES	= 0x51,
        IGFX_PWR_INVALID_DISPLAY	= 0x52,
        IGFX_PWR_INVALID_PARAMETER	= 0x53,
        IGFX_PWR_OPERATION_FAILED	= 0x54,
        UNKNOWN_ERROR	= 0x3e7
    } 	IGFX_ERROR_CODES;

typedef /* [uuid] */  DECLSPEC_UUID("FB098838-2757-421e-AD78-48B1338341D3") 
enum IGFX_DISPLAY_TYPES
    {
        IGFX_NULL_DEVICE	= 0,
        IGFX_CRT	= 0x1,
        IGFX_LocalFP	= 0x2,
        IGFX_ExternalFP	= 0x3,
        IGFX_TV	= 0x4,
        IGFX_HDMI	= 0x5,
        IGFX_NIVO	= 0x6,
        IGFX_DP	= 0x7
    } 	IGFX_DISPLAY_TYPES;

typedef /* [uuid] */  DECLSPEC_UUID("77929DBC-01E6-45c8-A6DD-DC0DD6CD676D") 
enum IGFX_TV_CONNECTOR_FLAGS
    {
        IGFX_FORCE_TV	= ( 1 << 17 ) ,
        IGFX_FLAG_DACMODERGB	= ( 1 << 0 ) ,
        IGFX_FLAG_DACMODEYC	= ( 1 << 1 ) ,
        IGFX_FLAG_DACMODECOMPOSITE	= ( 1 << 2 ) ,
        IGFX_FLAG_DACMODEHDTV	= ( 1 << 3 ) ,
        IGFX_FLAG_DACMODEHDRGB	= ( 1 << 4 ) ,
        IGFX_FLAG_DACMODECOMPONENT	= ( 1 << 5 ) ,
        IGFX_FLAG_DACMODEDCONNECTOR	= IGFX_FLAG_DACMODECOMPONENT,
        IGFX_FLAG_AUTO_CONNECTOR_SELECTION	= ( 1 << 6 ) 
    } 	IGFX_TV_CONNECTOR_FLAGS;

typedef /* [uuid] */  DECLSPEC_UUID("F3A19AD9-97AA-4e89-A2DA-9C656131ECCF") 
enum IGFX_SDVO_CMD_STATUS
    {
        IGFX_SDVO_POWER_ON_STATE	= 0,
        IGFX_SDVO_SUCCESS	= 1,
        IGFX_SDVO_COMMAND_NOT_SUPPORTED	= 2,
        IGFX_SDVOINVALID_ARGUEMENT	= 3,
        IGFX_SDVO_PENDING	= 4,
        IGFX_SDVO_TARGET_NOT_SPECIFIED	= 5,
        IGFX_SDVO_DEVICE_SCALING_NOT_SUPPORTED	= 6
    } 	IGFX_SDVO_CMD_STATUS;

typedef /* [uuid] */  DECLSPEC_UUID("60591CB6-E8D6-4adb-8073-917D4E698B8F") 
enum CUIErrorCode
    {
        CUIERROR_NO_ERROR	= 0,
        CUIERROR_INVALID_DRIVERNAME	= ( CUIERROR_NO_ERROR + 1 ) ,
        CUIERROR_INVALID_EDID	= ( CUIERROR_INVALID_DRIVERNAME + 1 ) ,
        CUIERROR_UNKNOWN_OPERATING_SYSTEM	= ( CUIERROR_INVALID_EDID + 1 ) ,
        CUIERROR_INVALID_DDC	= ( CUIERROR_UNKNOWN_OPERATING_SYSTEM + 1 ) ,
        CUIERROR_DRIVER_FAIL	= ( CUIERROR_INVALID_DDC + 1 ) ,
        CUIERROR_INCORRECT_DEVICE	= ( CUIERROR_DRIVER_FAIL + 1 ) ,
        CUIERROR_DRIVER_NOTSUPPORTED	= ( CUIERROR_INCORRECT_DEVICE + 1 ) ,
        CUIERROR_INVALID_STATE	= ( CUIERROR_DRIVER_NOTSUPPORTED + 1 ) ,
        CUIERROR_REGISTRY	= ( CUIERROR_INVALID_STATE + 1 ) ,
        CUIERROR_UNKNOWN_GENERIC	= ( CUIERROR_REGISTRY + 1 ) ,
        CUIERROR_INVALID_PARAMETER	= ( CUIERROR_UNKNOWN_GENERIC + 1 ) ,
        CUIERROR_CFG_DRV_NOT_SUPPORT	= ( CUIERROR_INVALID_PARAMETER + 1 ) ,
        CUIERROR_CFG_DRV_NOT_SUPPORT_PRIMARY	= ( CUIERROR_CFG_DRV_NOT_SUPPORT + 1 ) ,
        CUIERROR_CFG_DRV_NOT_SUPPORT_SECONDARY	= ( CUIERROR_CFG_DRV_NOT_SUPPORT_PRIMARY + 1 ) ,
        CUIERROR_CFG_DEV_NOT_SUPPORT	= ( CUIERROR_CFG_DRV_NOT_SUPPORT_SECONDARY + 1 ) ,
        CUIERROR_CFG_DEV_NOT_SUPPORT_PRIMARY	= ( CUIERROR_CFG_DEV_NOT_SUPPORT + 1 ) ,
        CUIERROR_CFG_DEV_NOT_SUPPORT_SECONDARY	= ( CUIERROR_CFG_DEV_NOT_SUPPORT_PRIMARY + 1 ) ,
        CUIERROR_CFG_DEV_NOT_SUPPORT_THIRD	= ( CUIERROR_CFG_DEV_NOT_SUPPORT_SECONDARY + 1 ) ,
        CUIERROR_CFG_DEV_NOT_SUPPORT_FOURTH	= ( CUIERROR_CFG_DEV_NOT_SUPPORT_THIRD + 1 ) ,
        CUIERROR_OUT_OF_MEMORY	= ( CUIERROR_CFG_DEV_NOT_SUPPORT_FOURTH + 1 ) ,
        CUIERROR_CUSTOMMODE_INVALID_PARAMETER	= ( CUIERROR_OUT_OF_MEMORY + 1 ) ,
        CUIERROR_EXISTING_MODE	= ( CUIERROR_CUSTOMMODE_INVALID_PARAMETER + 1 ) ,
        CUIERROR_CUSTOMMODE_EXISTING_BASIC_MODE	= ( CUIERROR_EXISTING_MODE + 1 ) ,
        CUIERROR_CUSTOMMODE_EXISTING_DETAIL_MODE	= ( CUIERROR_CUSTOMMODE_EXISTING_BASIC_MODE + 1 ) ,
        CUIERROR_CUSTOMMODE_OUT_OF_BW_LIMIT	= ( CUIERROR_CUSTOMMODE_EXISTING_DETAIL_MODE + 1 ) ,
        CUIERROR_CUSTOMMODE_INSUFFICIENT_MEMORY	= ( CUIERROR_CUSTOMMODE_OUT_OF_BW_LIMIT + 1 ) ,
        CUIERROR_CUSTOMMODE_INVALID_LFP_RR	= ( CUIERROR_CUSTOMMODE_INSUFFICIENT_MEMORY + 1 ) ,
        CUIERROR_AUX_DEFER	= ( CUIERROR_CUSTOMMODE_INVALID_LFP_RR + 1 ) ,
        CUIERROR_AUX_TIMEOUT	= ( CUIERROR_AUX_DEFER + 1 ) ,
        CUIERROR_AUX_INCOMPLETE_WRITE	= ( CUIERROR_AUX_TIMEOUT + 1 ) ,
        CUIERROR_MAX_ERROR	= ( CUIERROR_AUX_INCOMPLETE_WRITE + 1 ) 
    } 	CUIErrorCode;

typedef /* [uuid] */  DECLSPEC_UUID("563776B8-0D4D-43c3-A2A9-3B22E26123F4") struct IGFX_DFGT_POLICY_1_0
    {
    BOOL bEnabled;
    } 	IGFX_DFGT_POLICY_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("CEBBAEBD-5A0A-4a1b-89D9-F014E9F17837") struct IGFX_DPST_POLICY_1_0
    {
    BOOL bEnabledDC;
    BOOL bReserved1;
    ULONG ulMaxLevels;
    ULONG ulCurrentAggressivenessDC;
    ULONG ulReserved2;
    } 	IGFX_DPST_POLICY_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("E376E512-AD0A-49ef-84B6-E80FD2EF3E47") struct GAMMARAMP
    {
    unsigned short Red[ 256 ];
    unsigned short Green[ 256 ];
    unsigned short Blue[ 256 ];
    } 	GAMMARAMP;

typedef /* [uuid] */  DECLSPEC_UUID("355488D2-EE9C-4871-B199-A09F4B095D23") struct REFRESHRATE
    {
    unsigned short usRefRate;
    unsigned short usReserved;
    } 	REFRESHRATE;

typedef /* [uuid] */  DECLSPEC_UUID("6FD4DC75-C81E-42c8-BEEE-56AB20C94B80") struct DISPLAY_CONFIG
    {
    DWORD uidMonitorPrimary;
    DWORD uidMonitorSecondary;
    DWORD XResolution;
    DWORD YResolution;
    DWORD BPP;
    } 	DISPLAY_CONFIG;

typedef /* [uuid] */  DECLSPEC_UUID("30D7ECBC-01D0-4c77-9957-980CAC468C98") struct IGFX_EXTV_DATA
    {
    DWORD dwValue;
    DWORD dwDefault;
    DWORD dwMin;
    DWORD dwMax;
    DWORD dwStep;
    } 	IGFX_EXTV_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("3DBB0A2F-A205-4367-84F2-FAD0F5A6CE2E") struct IGFX_TV_PARAMETER_DATA
    {
    DWORD dwFlags;
    DWORD dwMode;
    DWORD dwTVStandard;
    DWORD dwAvailableTVStandard;
    IGFX_EXTV_DATA PositionX;
    IGFX_EXTV_DATA PositionY;
    IGFX_EXTV_DATA SizeX;
    IGFX_EXTV_DATA SizeY;
    IGFX_EXTV_DATA Brightness;
    IGFX_EXTV_DATA Contrast;
    IGFX_EXTV_DATA Flicker;
    IGFX_EXTV_DATA Sharpness;
    IGFX_EXTV_DATA AdaptiveFlicker;
    IGFX_EXTV_DATA TwoDFlicker;
    IGFX_EXTV_DATA Saturation;
    IGFX_EXTV_DATA Hue;
    IGFX_EXTV_DATA DotCrawl;
    IGFX_EXTV_DATA LumaFilter;
    IGFX_EXTV_DATA ChromaFilter;
    DWORD dwLetterBox;
    } 	IGFX_TV_PARAMETER_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("8A111648-F11E-416e-9961-E90A2883F7B7") struct IGFX_POWER_PARAMS_0
    {
    UINT uiInverterType;
    ULONG ulInverterFrequency;
    } 	IGFX_POWER_PARAMS_0;

typedef /* [uuid] */  DECLSPEC_UUID("8A401310-E453-4bee-8E25-F8F2D91FDFFE") struct IGFX_DVMT_1_0
    {
    DWORD dwMinDVMTMemory;
    DWORD dwMaxDVMTMemory;
    DWORD dwCurrentUsedDVMTMemory;
    DWORD dwTotalSystemMemory;
    } 	IGFX_DVMT_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("603E3171-697B-49e8-B42B-97915BCF96E6") struct IGFX_OVERLAY_1_0
    {
    BOOL bIsOverlayActive;
    } 	IGFX_OVERLAY_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("5C6D4330-77DF-4bfb-8418-59CDF372988E") struct IGFX_EDID_1_0
    {
    DWORD dwDisplayDevice;
    DWORD dwEDIDBlock;
    DWORD dwEDIDVersion;
    unsigned char EDID_Data[ 256 ];
    } 	IGFX_EDID_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("699B8927-2389-41ba-8ABB-D10B3A1C4CA9") struct IGFX_CUSTOM_SCALING
    {
    DWORD dwCustomScalingMax;
    DWORD dwCustomScalingMin;
    DWORD dwCustomScalingCurrent;
    DWORD dwCustomScalingStep;
    DWORD dwCustomScalingDefault;
    } 	IGFX_CUSTOM_SCALING;

typedef /* [uuid] */  DECLSPEC_UUID("5DC79B60-54FF-411e-9A32-868AB497C473") struct IGFX_DISPLAY_RESOLUTION
    {
    DWORD dwHzRes;
    DWORD dwVtRes;
    DWORD dwRR;
    DWORD dwBPP;
    } 	IGFX_DISPLAY_RESOLUTION;

typedef /* [uuid] */  DECLSPEC_UUID("4655D88F-0BA0-42e3-9BB7-DD485B5377BC") struct IGFX_DISPLAY_RESOLUTION_EX
    {
    DWORD dwHzRes;
    DWORD dwVtRes;
    DWORD dwRR;
    DWORD dwBPP;
    DWORD dwSupportedStandard;
    DWORD dwPreferredStandard;
    WORD InterlaceFlag;
    } 	IGFX_DISPLAY_RESOLUTION_EX;

typedef /* [uuid] */  DECLSPEC_UUID("40AE4AA9-166C-403a-AA2C-9C2DBC2AF951") struct IGFX_SCALING_1_0
    {
    DWORD dwPrimaryDevice;
    DWORD dwSecondaryDevice;
    DWORD dwOperatingMode;
    BOOL bIsSecondaryDevice;
    IGFX_DISPLAY_RESOLUTION PrimaryResolution;
    IGFX_DISPLAY_RESOLUTION SecondaryResolution;
    DWORD dwCurrentAspectOption;
    DWORD dwSupportedAspectOption;
    IGFX_CUSTOM_SCALING customScalingX;
    IGFX_CUSTOM_SCALING customScalingY;
    } 	IGFX_SCALING_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("55C2CBF9-5D69-45f7-B8A7-10245AF39AC6") struct IGFX_VERSION_HEADER
    {
    DWORD dwVersion;
    DWORD dwReserved;
    } 	IGFX_VERSION_HEADER;

typedef /* [uuid] */  DECLSPEC_UUID("C023E063-0303-4faf-96F9-6FC27635CCCD") struct IGFX_SCALING_2_0
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwDeviceID;
    IGFX_DISPLAY_RESOLUTION_EX resolution;
    DWORD dwSupportedAspectOption;
    DWORD dwCurrentAspectOption;
    IGFX_CUSTOM_SCALING customScalingX;
    IGFX_CUSTOM_SCALING customScalingY;
    } 	IGFX_SCALING_2_0;

typedef /* [uuid] */  DECLSPEC_UUID("8203E244-A8D5-4414-9FE0-6D5CCE5E710D") struct IGFX_GAMUT_EXPANSION
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwDeviceID;
    BOOL bIsFeatureSupported;
    DWORD dwGamutExpansionLevel;
    BOOL bUseCustomCSC;
    float CustomCSCMatrix[ 3 ][ 3 ];
    DWORD dwReserved;
    } 	IGFX_GAMUT_EXPANSION;

typedef /* [uuid] */  DECLSPEC_UUID("1C456BDA-CCDE-4451-BC31-6B6426A7892D") struct IGFX_DOWNSCALING_DATA
    {
    BOOL bIsSupported;
    IGFX_DISPLAY_RESOLUTION MaxSupportedMode;
    IGFX_DISPLAY_RESOLUTION SourceMode;
    IGFX_DISPLAY_RESOLUTION LastMode;
    } 	IGFX_DOWNSCALING_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("96F2DFD2-8639-4fbb-BBD9-4C29100E56BF") struct IGFX_MCCS_DATA
    {
    DWORD Cmd;
    UINT uiHandle;
    DWORD dwDevice;
    UINT uiControlCode;
    UINT uiSize;
    DWORD dwNCValueIndex;
    DWORD dwValue;
    UINT iNumSupportedControls;
    UINT iSupportedControls[ 255 ];
    UINT iNCValue[ 15 ];
    } 	IGFX_MCCS_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("36403B87-63E7-4fd5-8F1F-5C077F0B03A8") struct IGFX_TV_FORMAT_EX
    {
    DWORD dwReserved;
    DWORD dwDevice;
    DWORD dwTVStandard;
    DWORD dwTVType;
    DWORD dwAvailableTVStd;
    } 	IGFX_TV_FORMAT_EX;

typedef /* [uuid] */  DECLSPEC_UUID("9E48E080-E305-4a4c-9DCF-6E71660979EE") struct IGFX_CONNECTOR_STATUS
    {
    DWORD dwConnectorSupported;
    DWORD dwConnectorDispAttached;
    DWORD dwConnectorDispActive;
    } 	IGFX_CONNECTOR_STATUS;

typedef /* [uuid] */  DECLSPEC_UUID("E22906E9-7D79-4c08-9E17-E29924059B2E") struct IGFX_OVERLAY_COLOR_DATA
    {
    long lValue;
    long lDefault;
    long lMin;
    long lMax;
    long lStep;
    } 	IGFX_OVERLAY_COLOR_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("211A2CB3-6EC4-4c71-9142-752E9DF0A3BF") struct IGFX_OVERLAY_COLOR_SETTINGS
    {
    DWORD dwFlags;
    IGFX_OVERLAY_COLOR_DATA GammaSettings;
    IGFX_OVERLAY_COLOR_DATA BrightnessSettings;
    IGFX_OVERLAY_COLOR_DATA SaturationSettings;
    IGFX_OVERLAY_COLOR_DATA ContrastSettings;
    IGFX_OVERLAY_COLOR_DATA HueSettings;
    } 	IGFX_OVERLAY_COLOR_SETTINGS;

typedef /* [uuid] */  DECLSPEC_UUID("7DC8A9A6-BE8D-4989-8679-B864B160B73F") struct IGFX_FEATURE_SUPPORT_ARGS
    {
    DWORD dwFeatureSupport;
    DWORD Reserved1;
    } 	IGFX_FEATURE_SUPPORT_ARGS;

typedef /* [uuid] */  DECLSPEC_UUID("07F5914B-1D7C-44f9-A927-98DF6E26EF16") struct IGFX_ERROR
    {
    BOOL ErrorOccured;
    DWORD LastSystemErrorVal;
    BSTR ExtendedErrorBstr;
    } 	IGFX_ERROR;

typedef /* [uuid] */  DECLSPEC_UUID("0107C991-905B-45c8-B6CD-EDCF95F55EB7") struct IGFX_VENDOR_OPCODE_ARGS
    {
    IGFX_ERROR ErrorInfo;
    GUID guid;
    DWORD dwDeviceAddress;
    DWORD dwOpcode;
    BYTE ParamIn[ 8 ];
    DWORD dwParamInCount;
    BYTE Return[ 8 ];
    DWORD dwReturnCount;
    IGFX_SDVO_CMD_STATUS CmdStatus;
    DWORD Reserved1;
    DWORD Reserved2;
    } 	IGFX_VENDOR_OPCODE_ARGS;

typedef /* [uuid] */  DECLSPEC_UUID("42278E6C-B522-452e-A5F9-97010B594386") struct IGFX_CONFIG_DATA
    {
    DWORD dwOperatingMode;
    DWORD dwPriDevUID;
    DWORD dwSecDevUID;
    } 	IGFX_CONFIG_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("3FE31558-C8B7-4f75-8480-81C74E05F0D9") struct IGFX_TEST_CONFIG
    {
    DWORD dwNumTotalCfg;
    DWORD dwReserved1;
    DWORD dwReserved2;
    IGFX_CONFIG_DATA ConfigList[ 140 ];
    } 	IGFX_TEST_CONFIG;

typedef /* [uuid] */  DECLSPEC_UUID("3EF814DA-5B38-4934-9FB3-7BA962E2801E") struct IGFX_VIDEO_MODE_LIST
    {
    DWORD dwOperatingMode;
    DWORD dwPriDevUID;
    DWORD dwSecDevUID;
    BOOL bIsPrimary;
    WORD vmlNumModes;
    DWORD dwReserved1;
    DWORD dwReserved2;
    IGFX_DISPLAY_RESOLUTION vmlModes[ 1200 ];
    } 	IGFX_VIDEO_MODE_LIST;

typedef /* [uuid] */  DECLSPEC_UUID("EBB526B5-CD25-468d-97E8-7800D7B3E250") struct IGFX_DESKTOP_GAMMA_ARGS
    {
    DWORD dwDeviceUID;
    DWORD dwFlags;
    long lGammaValues[ 9 ];
    } 	IGFX_DESKTOP_GAMMA_ARGS;

typedef /* [uuid] */  DECLSPEC_UUID("92CACCFA-0C92-409c-8E48-797AEDA2F74B") struct IGFX_DISPLAY_POSITION
    {
    int iLeft;
    int iRight;
    int iTop;
    int iBottom;
    } 	IGFX_DISPLAY_POSITION;

typedef /* [uuid] */  DECLSPEC_UUID("DDAC4497-6E1F-4943-83FC-67749CD0F353") struct IGFX_DISPLAY_CONFIG_DATA_EX
    {
    DWORD dwDisplayUID;
    IGFX_DISPLAY_RESOLUTION_EX Resolution;
    IGFX_DISPLAY_POSITION Position;
    DWORD dwTvStandard;
    BOOL bIsHDTV;
    DWORD dwOrientation;
    DWORD dwScaling;
    DWORD dwFlags;
    } 	IGFX_DISPLAY_CONFIG_DATA_EX;

typedef /* [uuid] */  DECLSPEC_UUID("0A3A39A0-3B45-486b-B0DD-7373A334F1CF") struct IGFX_DISPLAY_CONFIG_DATA
    {
    DWORD dwDisplayUID;
    IGFX_DISPLAY_RESOLUTION_EX Resolution;
    IGFX_DISPLAY_POSITION Position;
    DWORD dwTvStandard;
    BOOL bIsHDTV;
    DWORD dwOrientation;
    DWORD dwScaling;
    } 	IGFX_DISPLAY_CONFIG_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("B4297023-A533-4fa6-B432-B838A10EE166") struct IGFX_MONITOR_CONTROL_HEADER
    {
    DWORD dwVersion;
    DWORD dwReserved;
    IGFX_ERROR ErrorInfo;
    } 	IGFX_DIPSLAY_CONFIG_HEADER;

typedef /* [uuid] */  DECLSPEC_UUID("1C5C9CC9-4413-4cff-9E5D-53B6785AF91B") struct IGFX_BEZEL_VALUES
    {
    DWORD lBezelX;
    DWORD lBezelY;
    DWORD lMaxBezelX;
    DWORD lMaxBezelY;
    } 	IGFX_BEZEL_VALUES;

typedef /* [uuid] */  DECLSPEC_UUID("DA29D67A-7FD7-4302-B18F-0949371682BC") struct IGFX_BEZEL_CONFIG
    {
    IGFX_VERSION_HEADER versionHeader;
    BOOL bEnableBezelCorrection;
    IGFX_BEZEL_VALUES bezelValues[ 2 ];
    } 	IGFX_BEZEL_CONFIG;

typedef /* [uuid] */  DECLSPEC_UUID("0FE052A2-5678-427d-ADBB-A09BEDAF98D0") struct IGFX_COLLAGE_STATUS
    {
    IGFX_VERSION_HEADER versionHeader;
    BOOL bIsCollageModeSupported;
    BOOL bDefaultCollageStatus;
    BOOL bIsCollageModeEnabled;
    } 	IGFX_COLLAGE_STATUS;

typedef /* [uuid] */  DECLSPEC_UUID("0608FCA2-BF1D-41a1-A283-F77AC3D0F1A4") struct IGFX_VIDEO_MODE_LIST_EX
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwOpMode;
    UINT uiNDisplays;
    IGFX_DISPLAY_CONFIG_DATA_EX DispCfg[ 6 ];
    DWORD dwDeviceID;
    DWORD dwFlags;
    WORD vmlNumModes;
    DWORD dwReserved;
    IGFX_DISPLAY_RESOLUTION_EX vmlModes[ 1 ];
    } 	IGFX_VIDEO_MODE_LIST_EX;

typedef /* [uuid] */  DECLSPEC_UUID("BAC3C5D5-F9F6-47b2-A374-11625CC842E2") struct IGFX_SYSTEM_CONFIG_DATA
    {
    DWORD dwOpMode;
    IGFX_DISPLAY_CONFIG_DATA PriDispCfg;
    IGFX_DISPLAY_CONFIG_DATA SecDispCfg;
    } 	IGFX_SYSTEM_CONFIG_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("1B6DC7D4-B5DC-45cd-A4DA-35DCC7E9B98B") struct IGFX_MEDIA_SCALAR
    {
    BOOL bSupported;
    BOOL bEnable;
    DWORD MediaScalingOption;
    IGFX_DISPLAY_RESOLUTION SourceMode;
    IGFX_DISPLAY_RESOLUTION LastMode;
    } 	IGFX_MEDIA_SCALAR;

typedef /* [uuid] */  DECLSPEC_UUID("EA3D4FE0-D9CA-48df-AB0B-D6480FDFD165") struct IGFX_CUSTOM_MODE
    {
    DWORD dwHzRes;
    DWORD dwVtRes;
    DWORD dwRR;
    DWORD dwBPP;
    BOOL bInterlacedMode;
    } 	IGFX_CUSTOM_MODE;

typedef /* [uuid] */  DECLSPEC_UUID("251260B7-BD17-4bec-A94B-3A66A13940D7") struct IGFX_ADVANCED_MODE
    {
    DWORD dwBPP;
    DWORD dwHFPorch;
    DWORD dwHBPorch;
    DWORD dwHSWidth;
    DWORD dwHActive;
    BOOL bHSPolarity;
    float fHSRate;
    DWORD dwVFPorch;
    DWORD dwVBPorch;
    DWORD dwVSWidth;
    DWORD dwVActive;
    BOOL bVSPolarity;
    float fVSRate;
    float fPixelClock;
    BOOL bInterlacedMode;
    } 	IGFX_ADVANCED_MODE;

typedef /* [uuid] */  DECLSPEC_UUID("EF82D81B-1EF2-4ff3-BC99-D73BD83F54F3") struct IGFX_CUSTOM_MODELIST
    {
    DWORD dwDisplayUID;
    DWORD dwFlags;
    DWORD dwTotalModes;
    IGFX_CUSTOM_MODE ModeList[ 1200 ];
    } 	IGFX_CUSTOM_MODELIST;

typedef /* [uuid] */  DECLSPEC_UUID("907D51FE-820D-4def-A8ED-CE2A894120F4") struct IGFX_CUSTOM_MODE_TIMING_DATA
    {
    DWORD dwDisplayUID;
    DWORD dwFlags;
    IGFX_CUSTOM_MODE AddedMode;
    IGFX_ADVANCED_MODE TimingInfo;
    } 	IGFX_CUSTOM_MODE_TIMING_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("58EE272B-F456-4f38-8144-200F67364403") struct IGFX_ADD_BASIC_CUSTOM_MODE_DATA
    {
    DWORD dwDisplayUID;
    DWORD dwFlags;
    BOOL bForcedModeAddition;
    float fUnderscan;
    DWORD dwTimingStandard;
    IGFX_CUSTOM_MODE BasicMode;
    } 	IGFX_ADD_BASIC_CUSTOM_MODE_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("926E14AE-28E9-41b5-9F3E-9480147D2C26") struct IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA
    {
    DWORD dwDisplayUID;
    DWORD dwFlags;
    BOOL bForcedModeAddition;
    IGFX_ADVANCED_MODE AdvancedMode;
    } 	IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("5FCC50CF-919D-40f3-BDF5-0E22A882DDCD") 
enum IGFX_MEDIA_FEATURE_TYPES
    {
        IGFX_MEDIA_FEATURE_CVT	= 0x1,
        IGFX_MEDIA_FEATURE_FMD	= 0x2,
        IGFX_MEDIA_FEATURE_NOISE_REDUCTION	= 0x4,
        IGFX_MEDIA_FEATURE_SHARPNESS	= 0x8,
        IGFX_MEDIA_FEATURE_COLOR	= 0x10,
        IGFX_MEDIA_FEATURE_SCALING	= 0x20,
        IGFX_MEDIA_FEATURE_TCC	= 0x40,
        IGFX_MEDIA_FEATURE_STE	= 0x80,
        IGFX_MEDIA_FEATURE_ACE	= 0x100,
        IGFX_MEDIA_FEATURE_IS	= 0x200,
        IGFX_MEDIA_FEATURE_GC	= 0x400
    } 	IGFX_MEDIA_FEATURE_TYPES;

typedef /* [uuid] */  DECLSPEC_UUID("B23322B3-E18E-41af-8E10-6AEC7EC13720") struct IGFX_MEDIA_SETTINGS_DATA
    {
    float fValue;
    float fDefault;
    float fMin;
    float fMax;
    float fStep;
    } 	IGFX_MEDIA_SETTINGS_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("3486DC90-3D15-465c-AFA5-F8D9122DE7D2") struct IGFX_MEDIA_ENABLE_DATA
    {
    BOOL bEnable;
    BOOL bDefault;
    } 	IGFX_MEDIA_ENABLE_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("9D0D7CBA-D168-4c1f-9ECB-6206310E4175") struct IGFX_VIDEO_QUALITY_DATA
    {
    DWORD dwSupportedFeatures;
    IGFX_MEDIA_ENABLE_DATA EnableFMD;
    IGFX_MEDIA_ENABLE_DATA AlwaysEnableNR;
    IGFX_MEDIA_ENABLE_DATA AlwaysEnableSharpness;
    DWORD dwFlags;
    IGFX_MEDIA_SETTINGS_DATA SharpnessSettings;
    } 	IGFX_VIDEO_QUALITY_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("4B18998E-E5ED-4fbb-9E9F-FC63467A4A5D") struct IGFX_MEDIA_COLOR_DATA
    {
    DWORD dwSupportedFeatures;
    IGFX_MEDIA_ENABLE_DATA EnableAlways;
    DWORD dwFlags;
    IGFX_MEDIA_SETTINGS_DATA HueSettings;
    IGFX_MEDIA_SETTINGS_DATA SaturationSettings;
    IGFX_MEDIA_SETTINGS_DATA ContrastSettings;
    IGFX_MEDIA_SETTINGS_DATA BrightnessSettings;
    } 	IGFX_MEDIA_COLOR_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("4E276FE3-852C-464b-A55F-35209DBD0F4E") struct IGFX_MEDIA_SCALING_DATA
    {
    DWORD dwSupportedFeatures;
    IGFX_MEDIA_ENABLE_DATA EnableNLAS;
    DWORD dwFlags;
    IGFX_MEDIA_SETTINGS_DATA VerticalCropSettings;
    IGFX_MEDIA_SETTINGS_DATA HLinearRegionSettings;
    IGFX_MEDIA_SETTINGS_DATA NonLinearCropSettings;
    } 	IGFX_MEDIA_SCALING_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("9BFE95AB-DF7B-4b03-A7D3-47BC3CE4D165") struct IGFX_AVIINFOFRAME
    {
    UINT uiTypeCode;
    UINT uiVersion;
    UINT uiLength;
    BOOL bR3R0Valid;
    BOOL bITContent;
    BYTE barInfo[ 8 ];
    DWORD dwDeviceID;
    DWORD dwActiveFormatAspectRatio;
    DWORD dwNonUniformScaling;
    DWORD dwRGBYCCIndicator;
    DWORD dwExtColorimetry;
    DWORD dwPixelFactor;
    DWORD bBarInfoValid;
    DWORD dwColorimetry;
    DWORD dwAspectRatio;
    DWORD dwQuantRange;
    DWORD dwVideoCode;
    DWORD dwScanInfo;
    DWORD dwFlags;
    } 	IGFX_AVIINFOFRAME;

typedef /* [uuid] */  DECLSPEC_UUID("2DD1AFA1-881C-4cf5-BE3F-E22659DEEBC5") struct IGFX_SYSTEM_CONFIG_DATA_N_VIEW
    {
    DWORD dwOpMode;
    DWORD dwFlags;
    UINT uiSize;
    UINT uiNDisplays;
    IGFX_DISPLAY_CONFIG_DATA_EX DispCfg[ 1 ];
    } 	IGFX_SYSTEM_CONFIG_DATA_N_VIEW;

typedef /* [uuid] */  DECLSPEC_UUID("A1D915F6-3517-496f-8BFA-9208BBA8A2B5") struct IGFX_SYSTEM_CONFIG_DATA_N_VIEWS
    {
    DWORD dwOpMode;
    DWORD dwFlags;
    UINT uiSize;
    UINT uiNDisplays;
    IGFX_DISPLAY_CONFIG_DATA_EX DispCfg[ 6 ];
    } 	IGFX_SYSTEM_CONFIG_DATA_N_VIEWS;

typedef /* [uuid] */  DECLSPEC_UUID("985A7694-2949-4e80-8B9E-A719F55CAAE2") struct IGFX_DISPLAY_CONFIG_1_1
    {
    UINT nSize;
    DWORD uidMonitor;
    DWORD dwFlags;
    BOOL bHorizontalPanningEnabled;
    BOOL bVerticalPanningEnabled;
    POINT ptViewPortPosition;
    LONG lHorizontalScaling;
    LONG lVerticalScaling;
    UINT ulPhysicalWidth;
    UINT ulPhysicalHeight;
    UINT ulDisplayWidth;
    UINT ulDisplayHeight;
    BOOL bRotationEnabled;
    BOOL bPortraitPolicy;
    BOOL bLandscapePolicy;
    DWORD dwOrientation;
    } 	IGFX_DISPLAY_CONFIG_1_1;

typedef /* [uuid] */  DECLSPEC_UUID("BBD627C9-B745-4684-839C-C6350B20239D") struct IGFX_AVI_INFOFRAME
    {
    UINT uiTypeCode;
    UINT uiVersion;
    UINT uiLength;
    BOOL bR3R0Valid;
    BOOL bITContent;
    BYTE barInfo[ 8 ];
    DWORD dwDeviceID;
    DWORD dwActiveFormatAspectRatio;
    DWORD dwNonUniformScaling;
    DWORD dwRGBYCCIndicator;
    DWORD dwExtColorimetry;
    DWORD dwPixelFactor;
    DWORD bBarInfoValid;
    DWORD dwColorimetry;
    DWORD dwAspectRatio;
    DWORD dwQuantRange;
    DWORD dwVideoCode;
    DWORD dwScanInfo;
    DWORD dwFlags;
    } 	IGFX_AVI_INFOFRAME;

typedef /* [uuid] */  DECLSPEC_UUID("D64FD045-48ED-4c2d-98C5-140B16471C4C") struct IGFX_AVI_INFOFRAME_EX
    {
    IGFX_VERSION_HEADER versionHeader;
    IGFX_AVI_INFOFRAME aviFrameInfo;
    DWORD dwSupportedAspectRatios;
    DWORD dwSupportedITContentTypes;
    DWORD dwITContentTypeValue;
    } 	IGFX_AVI_INFOFRAME_EX;

typedef /* [uuid] */  DECLSPEC_UUID("DED5BE46-59BE-463f-A43B-E4600E59D07D") struct DEVICE_DISPLAYS
    {
    UINT nSize;
    WCHAR strDeviceName[ 40 ];
    DWORD dwFlags;
    DWORD primaryMonitorID;
    UINT nMonitors;
    DWORD monitorIDs[ 6 ];
    } 	DEVICE_DISPLAYS;

typedef /* [uuid] */  DECLSPEC_UUID("130B77C6-7910-4bc3-9049-1AE555088729") 
enum OSTYPE
    {
        XP	= 1729,
        VISTA	= ( XP + 1 ) 
    } 	OSTYPE;

typedef /* [uuid] */  DECLSPEC_UUID("6B40625D-A978-42d2-B1DF-4CC1A38CC3AB") 
enum DISPLAY_RELATED
    {
        UNKNOWN	= -1,
        CRT1	= 1,
        CRT2	= 2,
        CRT3	= 4,
        CRT4	= 8,
        TV1	= 16,
        TV2	= 32,
        TV3	= 64,
        TV4	= 128,
        DFP1	= 256,
        DFP2	= 512,
        DFP3	= 1024,
        DFP4	= 2048,
        LFP1	= 4096,
        LFP2	= 8192,
        LFP3	= 16384,
        LFP4	= 32768,
        CRT	= CRT1,
        TV	= TV1,
        DFP	= DFP1,
        LFP	= LFP1,
        ALL_DEVICES	= ( ( ( CRT | TV )  | DFP )  | LFP ) ,
        DISPLAYUID_DFP	= 0x3030300,
        DISPLAYUID_CRT	= 0x1010100,
        DISPLAYUID_TV	= 0x2090200,
        DISPLAYUID_LFP	= 0x4070400
    } 	DISPLAY_RELATED;

typedef /* [uuid] */  DECLSPEC_UUID("1438740C-8CEF-498d-A56C-FCAC6280F02F") 
enum OPERATING_MODE
    {
        SD	= ( 1 << 0 ) ,
        DT	= ( 1 << 1 ) ,
        DC	= ( 1 << 2 ) ,
        ED	= ( 1 << 3 ) 
    } 	OPERATING_MODE;

typedef /* [uuid] */  DECLSPEC_UUID("898DA772-E7DC-47e3-AB0D-32DEB2748816") 
enum NEW_DEVICE_TYPE
    {
        NEWPRIMARY_DEVICE	= 0,
        NEWSECONDARY_DEVICE	= 1
    } 	NEW_DEVICE_TYPE;

typedef /* [uuid] */  DECLSPEC_UUID("7673D240-6271-4842-9D70-11BF16DB99AE") 
enum DISPLAY_DEVICE_STATUS
    {
        IGFX_DISPLAY_DEVICE_NOTATTACHED	= 0x1,
        IGFX_DISPLAY_DEVICE_ATTACHED	= 0x2,
        IGFX_DISPLAY_DEVICE_OVERRIDE	= 0x4,
        IGFX_DISPLAY_DEVICE_ACTIVE	= 0x10,
        IGFX_DISPLAY_DEVICE_PRIMARY	= 0x100,
        IGFX_DISPLAY_DEVICE_SECONDARY	= 0x200,
        IGFX_DISPLAY_DEVICE_ALL	= ( ( ( ( ( IGFX_DISPLAY_DEVICE_NOTATTACHED | IGFX_DISPLAY_DEVICE_ATTACHED )  | IGFX_DISPLAY_DEVICE_OVERRIDE )  | IGFX_DISPLAY_DEVICE_ACTIVE )  | IGFX_DISPLAY_DEVICE_PRIMARY )  | IGFX_DISPLAY_DEVICE_SECONDARY ) 
    } 	DISPLAY_DEVICE_STATUS;

typedef /* [uuid] */  DECLSPEC_UUID("EE9596B4-E36C-45fb-9028-3086186BE00A") struct DISPLAY_MODE
    {
    int vmHzRes;
    int vmVtRes;
    int vmPixelDepth;
    int vmRefreshRate;
    } 	DISPLAY_MODE;

typedef /* [uuid] */  DECLSPEC_UUID("75543EA9-CB6A-4a8d-A438-536103B91CB5") 
enum IGFX_COLOR_QUALITIES
    {
        IGFX_COLOR_QUALITY_8	= 8,
        IGFX_COLOR_QUALITY_16	= 16,
        IGFX_COLOR_QUALITY_32	= 32,
        IGFX_COLOR_QUALITY_ALL	= ( ( IGFX_COLOR_QUALITY_8 | IGFX_COLOR_QUALITY_16 )  | IGFX_COLOR_QUALITY_32 ) 
    } 	IGFX_COLOR_QUALITIES;

typedef /* [uuid] */  DECLSPEC_UUID("CBB76BDD-E13F-47a6-B23A-ABB83E77F671") 
enum IGFX_TIMING_STANDARDS
    {
        IGFX_TIMING_STANDARD_GTF	= 0x1,
        IGFX_TIMING_STANDARD_CVT	= 0x2,
        IGFX_TIMING_STANDARD_CVT_RB	= 0x3,
        IGFX_TIMING_STANDARD_CEA_861_B	= 0x4
    } 	IGFX_TIMING_STANDARDS;

typedef /* [uuid] */  DECLSPEC_UUID("2786A068-0EE5-4c59-9E4E-C2C8B2169B00") 
enum IGFX_CUSTOM_MODES
    {
        IGFX_BASIC_CUSTOM_MODES	= 0x1,
        IGFX_ADVANCED_CUSTOM_MODES	= 0x2
    } 	IGFX_CUSTOM_MODES;

typedef /* [uuid] */  DECLSPEC_UUID("cedce755-27d8-4ed0-969d-b487ee4e14cf") struct IGFX_COLOR_DATA
    {
    float fValue;
    float fDefault;
    float fMin;
    float fMax;
    float fStep;
    } 	IGFX_COLOR_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("bb6844be-0b8f-4d33-96c1-807346eb41b0") struct IGFX_HUESAT_INFO
    {
    BOOL bIsFeatureSupported;
    BOOL bIsRGB;
    DWORD dwDeviceID;
    IGFX_COLOR_DATA HueSettings;
    IGFX_COLOR_DATA SaturationSettings;
    DWORD dwFlags;
    } 	IGFX_HUESAT_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("AF259B5A-2EA3-4705-8EEE-61333A43623D") struct IGFX_DISPLAY_CSC_MATRIX
    {
    float fLFPCSCMatrix_601[ 3 ][ 3 ];
    float fLFPCSCMatrix_709[ 3 ][ 3 ];
    UCHAR flag;
    } 	IGFX_DISPLAY_CSC_MATRIX;

typedef /* [uuid] */  DECLSPEC_UUID("6BD1EE22-8CD6-4da7-887C-674691A6B7BD") struct IGFX_SOURCE_DISPLAY_CSC_DATA
    {
    BOOL bEnable;
    ULONG ulReserved;
    IGFX_DISPLAY_CSC_MATRIX CSCMatrix;
    DWORD dwIsSupported;
    DWORD dwFlag;
    } 	IGFX_SOURCE_DISPLAY_CSC_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("7e4b0552-868d-40df-9b04-bb6852dfac92") struct IGFX_VIDEO_QUALITY_DATA_EX
    {
    IGFX_VIDEO_QUALITY_DATA VideoQualityData;
    IGFX_MEDIA_ENABLE_DATA EnableDriverPreference;
    IGFX_MEDIA_ENABLE_DATA EnableOptimalSharpness;
    IGFX_MEDIA_SETTINGS_DATA NoiseReductionSettings;
    DWORD dwFlags;
    } 	IGFX_VIDEO_QUALITY_DATA_EX;

typedef /* [uuid] */  DECLSPEC_UUID("5c3776fb-4c3a-4155-8610-4db04142e6b0") 
enum IGFX_IPS_DEVICE
    {
        IGFX_PWRCONS_IPS_DEVICE_UNKNOWN	= 0,
        IGFX_PWRCONS_IPS_DEVICE_CPU	= ( IGFX_PWRCONS_IPS_DEVICE_UNKNOWN + 1 ) ,
        IGFX_PWRCONS_IPS_DEVICE_GFX	= ( IGFX_PWRCONS_IPS_DEVICE_CPU + 1 ) 
    } 	IGFX_IPS_DEVICE;

typedef /* [uuid] */  DECLSPEC_UUID("258731d9-1a70-41db-87aa-75f9b840ea10") 
enum IGFX_POWER_PLAN
    {
        IGFX_PWR_PLAN_GET_CURRENT	= 0,
        IGFX_PWR_PLAN_BEST_POWER_SAVINGS	= ( IGFX_PWR_PLAN_GET_CURRENT + 1 ) ,
        IGFX_PWR_PLAN_BETTER_POWER_SAVINGS	= ( IGFX_PWR_PLAN_BEST_POWER_SAVINGS + 1 ) ,
        IGFX_PWR_PLAN_GOOD_POWER_SAVINGS	= ( IGFX_PWR_PLAN_BETTER_POWER_SAVINGS + 1 ) ,
        IGFX_PWR_PLAN_DISABLE_POWER_SAVINGS	= ( IGFX_PWR_PLAN_GOOD_POWER_SAVINGS + 1 ) ,
        IGFX_PWR_PLAN_CUSTOM	= ( IGFX_PWR_PLAN_DISABLE_POWER_SAVINGS + 1 ) ,
        IGFX_NUM_OF_PWR_USER_PLANS	= ( IGFX_PWR_PLAN_CUSTOM + 1 ) 
    } 	IGFX_POWER_PLAN;

typedef /* [uuid] */  DECLSPEC_UUID("6e83f78c-243d-4a45-87ff-ca64bb465c44") struct IGFX_POWER_CONSERVATION_DATA
    {
    DWORD dwPowerState;
    DWORD dwOperation;
    IGFX_POWER_PLAN PowerPlan;
    DWORD dwDisplayDevice;
    DWORD dwCapability;
    DWORD dwChangedFeatures;
    DWORD dwEnabledFeatures;
    DWORD dwDPSTCurLevel;
    DWORD dwDPSTTotalLevel;
    DWORD dwGSVCurLevel;
    DWORD dwGSVTotalLevel;
    BOOL bIsMFD;
    BOOL IsSupportForStaticDRRS;
    DWORD dwRR[ 20 ];
    DWORD dwLowRR;
    DWORD dwNumRR;
    IGFX_IPS_DEVICE IPSDevice;
    BOOL bIsIPSSupported;
    BOOL bEnableIPS;
    DWORD dwIPSREnderFrequency;
    DWORD dwFlags;
    } 	IGFX_POWER_CONSERVATION_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("8cdee4b5-8a21-430b-aa01-5211ec08820e") struct IGFX_ADB_POLICY_1_0
    {
    BOOL bEnabledDC;
    BOOL bEnabledAC;
    ULONG ulReserved1;
    ULONG ulReserved2;
    ULONG ulReserved3;
    } 	IGFX_ADB_POLICY_1_0;

typedef /* [uuid] */  DECLSPEC_UUID("9b0a6f2f-c8b8-4293-8224-bb2e02b37784") struct IGFX_D3D_INFO
    {
    long lBasicVal;
    long lBasicValDef;
    long lVertexProcessingVal;
    long lVertexProcessingValDef;
    long lTextureQualityVal;
    long lTextureQualityValDef;
    long lAnisotrophicVal;
    long lAnisotrophicValDef;
    long lFlipVsyncVal;
    long lFlipVsyncValDef;
    DWORD dwFlags;
    } 	IGFX_D3D_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("18C9ECDB-7D36-40f8-A70D-C418015480BF") struct IGFX_D3D_INFO_EX
    {
    IGFX_VERSION_HEADER versionHeader;
    long lBasicVal;
    long lBasicValDef;
    long lVertexProcessingVal;
    long lVertexProcessingValDef;
    long lTextureQualityVal;
    long lTextureQualityValDef;
    long lAnisotropicVal;
    long lAnisotropicValDef;
    long lFlipVSyncVal;
    long lFlipVSyncValDef;
    DWORD dwFlags;
    long lAILVal;
    long lAILDef;
    long lMSAAVal;
    long lMSAADef;
    long lCMAAVal;
    long lCMAADef;
    } 	IGFX_D3D_INFO_EX;

typedef /* [uuid] */  DECLSPEC_UUID("A3C7BC45-E69C-44ec-9F16-B58547084552") struct IGFX_SYSTEM_IGPU_STATUS_STRUCT
    {
    BOOL bIsGPUSwitchinProgress;
    BYTE ConfigType;
    BYTE TPVType;
    BYTE MLScheme;
    BYTE Display;
    BYTE Render;
    BYTE Reserved1;
    BYTE Reserved2;
    BYTE Reserved3;
    } 	IGFX_SYSTEM_IGPU_STATUS_STRUCT;

typedef /* [uuid] */  DECLSPEC_UUID("9DA3FCA2-C79E-4df9-BBEB-1FA912221BC0") struct IGFX_VIDEO_HEADER
    {
    DWORD dwVersion;
    DWORD dwReserved;
    } 	IGFX_VIDEO_HEADER;

typedef /* [uuid] */  DECLSPEC_UUID("9650548E-0980-4a1e-B676-D587F3C8830E") struct IGFX_VIDEO_QUALITY_DATA_EX2
    {
    IGFX_VIDEO_HEADER header;
    DWORD dwSupportedFeatures;
    BOOL bCurrentFMD;
    BOOL bDefaultFMD;
    BOOL bCurrentNR;
    BOOL bDefaultNR;
    BOOL bCurrentSharpness;
    BOOL bDefaultSharpness;
    DWORD dwFlags;
    float fSharpnessCurrent;
    float fSharpnessDefault;
    float fSharpnessMin;
    float fSharpnessMax;
    float fSharpnessStep;
    BOOL bCurrentDriverPreference;
    BOOL bDefaultDriverPreference;
    BOOL bCurrentOptimalSharpness;
    BOOL bDefaultOptimalSharpness;
    float fNoiseReductionCurrent;
    float fNoiseReductionDefault;
    float fNoiseReductionMin;
    float fNoiseReductionMax;
    float fNoiseReductionStep;
    DWORD dwFlags2;
    BOOL bEnableDenoiseAutoDetect;
    BOOL bEnableDenoiseAutoDetectDef;
    BOOL bSkinToneEnhancement;
    BOOL bSkinToneEnhancementDef;
    BOOL bAutoContrastEnhancement;
    BOOL bAutoContrastEnhancementDef;
    float fSkinToneEnhancementCurrent;
    float fSkinToneEnhancementDefault;
    float fSkinToneEnhancementMin;
    float fSkinToneEnhancementMax;
    float fSkinToneEnhancementStep;
    DWORD dwNoiseReductionType;
    DWORD dwNoiseReductionTypeDef;
    BOOL bImageStabilization;
    BOOL bImageStabilizationDef;
    float fNoiseReductionLCCurrent;
    float fNoiseReductionLCDefault;
    float fNoiseReductionLCMin;
    float fNoiseReductionLCMax;
    float fNoiseReductionLCStep;
    float fACELevelCurrent;
    float fACELevelDefault;
    float fACELevelMin;
    float fACELevelMax;
    float fACELevelStep;
    } 	IGFX_VIDEO_QUALITY_DATA_EX2;

typedef /* [uuid] */  DECLSPEC_UUID("2F992B84-25CD-4de5-8C8E-5657C00E4D88") struct IGFX_MEDIA_COLOR_DATA_EX2
    {
    IGFX_VIDEO_HEADER header;
    DWORD dwSupportedFeatures;
    BOOL bEnableColor;
    BOOL bDefaultColor;
    DWORD dwFlags;
    float fHueCurrent;
    float fHueDefault;
    float fHueMin;
    float fHueMax;
    float fHueStep;
    float fSaturationCurrent;
    float fSaturationDefault;
    float fSaturationMin;
    float fSaturationMax;
    float fSaturationStep;
    float fContrastCurrent;
    float fContrastDefault;
    float fContrastMin;
    float fContrastMax;
    float fContrastStep;
    float fBrightnessCurrent;
    float fBrightnessDefault;
    float fBrightnessMin;
    float fBrightnessMax;
    float fBrightnessStep;
    BOOL bTotalColorControl;
    BOOL bTotalColorControlDef;
    float fRedCurrent;
    float fRedDefault;
    float fRedMin;
    float fRedMax;
    float fRedStep;
    float fGreenCurrent;
    float fGreenDefault;
    float fGreenMin;
    float fGreenMax;
    float fGreenStep;
    float fBlueCurrent;
    float fBlueDefault;
    float fBlueMin;
    float fBlueMax;
    float fBlueStep;
    float fYellowCurrent;
    float fYellowDefault;
    float fYellowMin;
    float fYellowMax;
    float fYellowStep;
    float fCyanCurrent;
    float fCyanDefault;
    float fCyanMin;
    float fCyanMax;
    float fCyanStep;
    float fMagentaCurrent;
    float fMagentaDefault;
    float fMagentaMin;
    float fMagentaMax;
    float fMagentaStep;
    DWORD dwInputYUVRange;
    DWORD dwInputYUVRangeDef;
    } 	IGFX_MEDIA_COLOR_DATA_EX2;

typedef /* [uuid] */  DECLSPEC_UUID("0A8B3748-DDD0-4ab8-8C54-BF17364857F5") struct IGFX_MEDIA_SCALING_DATA_EX2
    {
    IGFX_VIDEO_HEADER header;
    DWORD dwSupportedFeatures;
    BOOL bEnableNLAS;
    BOOL bDefaultNLAS;
    DWORD dwFlags;
    float fVerticalCropCurrent;
    float fVerticalCropDefault;
    float fVerticalCropMin;
    float fVerticalCropMax;
    float fVerticalCropStep;
    float fHLinearRegionCurrent;
    float fHLinearRegionDefault;
    float fHLinearRegionMin;
    float fHLinearRegionMax;
    float fHLinearRegionStep;
    float fNonLinearCropCurrent;
    float fNonLinearCropDefault;
    float fNonLinearCropMin;
    float fNonLinearCropMax;
    float fNonLinearCropStep;
    } 	IGFX_MEDIA_SCALING_DATA_EX2;

typedef /* [uuid] */  DECLSPEC_UUID("25416282-2EC5-425a-9F29-DBCDE0FA92F4") 
enum MEDIA_GAMUT_COMPRESSION_VALUES
    {
        IGFX_MEDIA_GAMUT_COMPRESSION_DISABLED	= 0,
        IGFX_MEDIA_GAMUT_COMPRESSION_RELATIVE	= 1,
        IGFX_MEDIA_GAMUT_COMPRESSION_PERCEPTUAL	= 2
    } 	MEDIA_GAMUT_COMPRESSION_VALUES;

typedef /* [uuid] */  DECLSPEC_UUID("57B8A330-4E6C-4cfc-8EDC-0FD5A1FA5C79") struct IGFX_MEDIA_GAMUT_MAPPING
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwSupportedFeatures;
    DWORD dwMediaGamutCompressionVal;
    DWORD dwMediaGamutCompressionValDef;
    DWORD dwFlags;
    } 	IGFX_MEDIA_GAMUT_MAPPING;

typedef /* [public][public][uuid] */  DECLSPEC_UUID("0127C6DA-5609-4532-89F7-A8667A62888C") struct __MIDL___MIDL_itf_IgfxBridgeUDT_0000_0000_0001
    {
    DWORD dwOperatingMode;
    DWORD dwNDisplays;
    DWORD dwPriDevUID;
    DWORD dwSecDevUID;
    DWORD dwThirdDevUID;
    DWORD dwFourthDevUID;
    } 	IGFX_CONFIG_DATA_EX;

typedef /* [public][uuid] */  DECLSPEC_UUID("427D299B-9161-4dbf-AE58-CE80D6712A58") struct __MIDL___MIDL_itf_IgfxBridgeUDT_0000_0000_0002
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwNumTotalCfg;
    DWORD dwReserved1;
    DWORD dwReserved2;
    IGFX_CONFIG_DATA_EX ConfigList[ 140 ];
    } 	IGFX_TEST_CONFIG_EX;

typedef /* [uuid] */  DECLSPEC_UUID("1970505e-817e-462b-a8b1-227455370b55") struct IGFX_AUX_INFO
    {
    DWORD dwDeviceUID;
    DWORD dwOpType;
    DWORD dwSize;
    DWORD dwAddress;
    BYTE Data[ 16 ];
    } 	IGFX_AUX_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("D49BF5D9-A2F3-414b-95FC-8A98CFBB5A90") struct IGFX_BUS_INFO
    {
    DWORD dwDeviceUID;
    DWORD dwOpType;
    DWORD dwSize;
    DWORD dwAddress;
    DWORD dwSubAddress;
    DWORD dwFlags;
    BYTE byBusType;
    BYTE Data[ 128 ];
    } 	IGFX_BUS_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("25fcc1da-39e5-4d02-ac33-0374d268ad59") struct IGFX_MEDIA_SOURCE_HDMI_GBD
    {
    WORD Version;
    DWORD Size;
    BYTE GBDPayLoad[ 28 ];
    } 	IGFX_MEDIA_SOURCE_HDMI_GBD;

typedef /* [uuid] */  DECLSPEC_UUID("4cbfa50e-e9d1-4213-b687-28dcd1347496") struct IGFX_SOURCE_HDMI_GBD_DATA
    {
    DWORD dwSourceID;
    BOOL IsXVYCCSupported;
    BOOL IsXVYCCEnabled;
    DWORD dwFlags;
    IGFX_MEDIA_SOURCE_HDMI_GBD MediaSourceHDMIGBD;
    } 	IGFX_SOURCE_HDMI_GBD_DATA;

typedef /* [uuid] */  DECLSPEC_UUID("048bc691-5b3c-4070-8cc5-01db5fc3d111") struct IGFX_XVYCC_INFO
    {
    BOOL bEnableXvYCC;
    BOOL bIsXvYCCSupported;
    DWORD dwDeviceID;
    DWORD dwFlags;
    } 	IGFX_XVYCC_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("03623AE4-945C-45ec-B32D-C50282598D85") struct IGFX_YCBCR_INFO
    {
    BOOL bEnableYCbCr;
    BOOL bIsYCbCrSupported;
    DWORD dwDeviceID;
    DWORD dwFlags;
    } 	IGFX_YCBCR_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("C99CBF80-C812-4AB2-838D-5E5BA31E7D71") struct IGFX_AUDIO_FEATURE_INFO
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwNumberofAudio;
    DWORD dwAudioCapDisplays[ 3 ];
    DWORD dwAudioConfig;
    DWORD dwActiveAudioDisplays[ 3 ];
    DWORD dwAudioWoutVideo;
    DWORD dwAudioSupport;
    DWORD dwAudioWOVideoSupport;
    } 	IGFX_AUDIO_FEATURE_INFO;

typedef /* [uuid] */  DECLSPEC_UUID("34351E2B-3248-4d92-9A86-C223ADA222EC") struct IGFX_GAMUT
    {
    IGFX_VERSION_HEADER versionHeader;
    DWORD dwDeviceUID;
    BOOL bIsFeatureSupported;
    BOOL bEnableDisable;
    DWORD dwReserved;
    } 	IGFX_GAMUT;

typedef /* [uuid] */  DECLSPEC_UUID("B7B5138A-4FE4-4564-AC06-0212C400BA1B") struct IGFX_GOP_VERSION
    {
    ULONG ulMajorVersion;
    ULONG ulMinorVersion;
    ULONG ulBuildNumber;
    BOOLEAN bGOP_VBIOS;
    } 	IGFX_GOP_VERSION;

typedef /* [uuid] */  DECLSPEC_UUID("B7354D53-F75E-4330-8279-84A8824DFF50") struct IGFX_RESTORE_GRAPHICS_DEFAULT_VERSION_HEADER
    {
    DWORD dwVersion;
    DWORD dwReserved;
    IGFX_ERROR ErrorInfo;
    } 	IGFX_RESTORE_GRAPHICS_DEFAULT_VERSION_HEADER;

typedef /* [uuid] */  DECLSPEC_UUID("E5FDE929-A42F-46f3-BED4-CA16D0704A29") struct IGFX_RESTORE_GRAPHICS_DEFAULT_INFO
    {
    IGFX_RESTORE_GRAPHICS_DEFAULT_VERSION_HEADER header;
    } 	IGFX_RESTORE_GRAPHICS_DEFAULT_INFO;



extern RPC_IF_HANDLE __MIDL_itf_IgfxBridgeUDT_0000_0000_v0_0_c_ifspec;
extern RPC_IF_HANDLE __MIDL_itf_IgfxBridgeUDT_0000_0000_v0_0_s_ifspec;

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


