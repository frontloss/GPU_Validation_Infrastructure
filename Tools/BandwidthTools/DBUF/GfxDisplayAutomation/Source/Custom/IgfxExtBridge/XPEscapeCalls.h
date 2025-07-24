#ifndef __XP_ESCAPE_CALLS_H__
#define __XP_ESCAPE_CALLS_H__

#define DISPLAYUID_DFP				0x3030300
#define DISPLAYUID_CRT				0x1010100
#define DISPLAYUID_TV				0x2090200
#define DISPLAYUID_LFP				0x4070400

#pragma pack(push, ESCAPECALLS)
#pragma pack(1)

// Some Data types from outside
// Display port type enumeration
typedef enum {
	NULL_PORT_TYPE = -1,
	ANALOG_PORT = 0,
	DVOA_PORT,
	DVOB_PORT,
	DVOC_PORT,
	LVDS_PORT,
	INT_TVOUT_PORT,		// From Alviso onwards
	INTHDMIB_PORT,
	INTHDMIC_PORT,
	INT_DVI_PORT,		// NA
	INTDPB_PORT,			//From cantiga onwards. These ports are present
	INTDPC_PORT,			// - do -
	INTDPD_PORT,			// - do - 
	MAX_PORTS
} PORT_TYPES, *PPORT_TYPES;


//	Maximum number of display pipes and devices
#define MAX_PIPES		2
#define MAX_DISPLAYS	(MAX_PORTS * 2)	  // Allows for combo codecs
#define MAX_PLANES		4	// VGA, DisplayA/B & C
#define MAX_CURSOR_PLANES 2

typedef struct _DISPLAY_LIST {
	UINT	nDisplays;
    ULONG   ulDisplayUID[MAX_DISPLAYS];      
    ULONG   ulDeviceConfig;         // device configuration (Usefull for dual display)

} DISPLAY_LIST, *PDISPLAY_LIST;



#ifdef __cplusplus
    extern "C" {
#endif //__cplusplus

/////Driver and CUI should communicate w/o structure packing 


 
#define CUICOM_ESCAPE    0x00435044    //Stands for 'CPL'

#ifndef BYTE 
typedef unsigned char BYTE; 
#endif 

#ifndef BOOLEAN
typedef BYTE BOOLEAN;
#endif

#define COM_DEVICE_CRT        0x01
#define COM_DEVICE_TV        0x02
#define COM_DEVICE_EXTLCD    0x04    // external LCD
#define COM_DEVICE_LFP        0x08    // local LCD (Flat Panel)
#define COM_DEVICE_ADDTV    0x10    // add-on TV
#define COM_DEVICE_ADDDFP    0x20    // add-on flat panel


enum COM_DEVICE_MODE{
    COM_DDMODE_SINGLE_PIPE = 0,
    COM_DDMODE_DUALVIEW_TWIN,
    COM_DDMODE_DUALVIEW_TWINPLUS,
    COM_DDMODE_MDS,
    COM_DDMODE_DUALVIEW_CINEMA,
    COM_DDMODE_DUALVIEW_MULTI,
    COM_DDMODE_MOSAIC
};

//When Adding new Escape functions , do add it at the end , since SoftBios Makes Call
//based on the Enum numbers(ID)
enum CUI_COM_FUNCTIONS{
// these escape functions begin with SB_ 'cause they will be implemented by SoftBIOS
SB_GET_CONTROLLER_INFO,
SB_GET_ROM_BIOS_INFO,
SB_GET_REFRESH_RATE,
SB_GET_MODE_SUPPORT,  //Now ONly GDI needs it, CUICOM does not need it anymore
SB_SET_COMPENSATION,
SB_GET_COMPENSATION,
SB_GET_DISPLAY_DEVICE,
SB_GET_DISPLAY_DEVICE_INFO,
COM_GET_EDID,
COM_TEST_CONFIG,

COM_GET_MODE_TABLE,
COM_SET_GAMMA,
COM_GET_GAMMA,
COM_VIDEO_PARAMETERS,
COM_PASS_EVENT_HANDLE,
COM_I2C_OPEN,           //CUI is not using this one, but some application in AZ is using it
COM_I2C_ACCESS,
SB_GETVBT_INFO,
SB_SETSCRATCHBIT,  //This is for Driver internal to use, CUICOM does not use it at all...
COM_CUI_REGISTRY_DWORD,

COM_CUI_REGISTRY_BINARY,
SB_ROTATION_GET_SETTINGS,
COM_GET_CURRENT_DEVICE_REFRESH_RATE,
COM_GET_DEVICE_REFRESH_RATES,
COM_SET_DEVICE_REFRESH_RATES,
COM_CUI_GET_VIEWPORT, 
///////////////////////PC12.0 Escape Codes Go Bellow///////////////////////////
COM_SYSTEM_NOTIFY,    // PC11.1 and 12+ escape
COM_GET_DVMT_INFO,  // Get DVMT infomation 
COM_ATOMIC_I2C_ACCESS,
COM_DETECT_DEVICE,   //Detect Display Devices
COM_GET_SET_OVERLAY_COLORS,
COM_POWER_CONSERVATION,
COM_SET_DDC_CONFIGURATION,
COM_SET_MDS_CONFIGURATION,
COM_GET_MODE_TABLE2,
COM_GET_OPTIMAL_MODE,
COM_GET_VALID_CONFIGS,
COM_VALIDATE_ADVISE_CFG_MODE,
COM_VALIDATE_ADVISE_CFG,
COM_GET_COMPENSATION_IN_CONFIG,
COM_GET_OVERLAY_STATUS,
COM_GET_DOWNSCALE,
COM_SET_DOWNSCALE,
COM_ADVISENEXT_CONFIG_PERSISTENCE,
COM_SET_USERINFO_PERS,
COM_SET_DISPLAYSET_ARGS,
COM_GET_CUIPERSIST_DATA,
COM_GET_IND_ROT_CAPS,
COM_GET_SKU_FEATURE,
COM_TMM_MODIFY_APPEND_CONFIG,
COM_GET_CURRCONFIG_VISTA,
COM_VALIDATE_ADVISE_VIDPN_DATA,
COM_GET_PANELFIT,
COM_NOTIFY_FAKING,
COM_GET_EVENTS,
COM_TV_STD_CHANGE
};

typedef struct _COM_NOTIFY_FAKING_ARGS  {
   /*IN*/   ULONG    Cmd;
} COM_NOTIFY_FAKING_ARGS, *PCOM_NOTIFY_FAKING_ARGS;

//Acutally this is to get display device info!!! -- 0x5F640005
#define ENABLE_ACTIVE_DETECTION      0x00000001
#define ENABLE_CRT_LEGACY_DETECTION  0x00000002
#define ENABLE_STATIC_DETECTION      0x00000004
#define ENABLE_HOTKEY_DETECTION      0x00000008
#define ENABLE_REPORT_LFP_UID         0x00000010
#define	ENABLE_EMDISPLIST_UPDATE	 0x00000020
#define ENABLE_ENCODER_DETECTION		0x00000040
#define ENABLE_OPREGION_UPDATE		 0x00000080

typedef struct _COM_DETECT_DEVICE_ARGS   { 
    ULONG         Cmd;      //Always COM_DETECT_DEVICE
    ULONG         ulFlags;  //Bit0:  Do Redetect
                            //Bit1:  Do Legacy Detection 
    DISPLAY_LIST  DispList; //Refer to SbArgs for define
    
}COM_DETECT_DEVICE_ARGS, *PCOM_DETECT_DEVICE_ARGS; 


// Bit definitions for indicating inverted portrait & landscape
#define CUICOM_INVERTED_LANDSCAPE        0x0001        // First bit when 1 indicates inverted landscape
#define CUICOM_INVERTED_PORTRAIT        0x0002        // Seconda bit when 1 indicates inverted portrait

// Value defined for policy in the registry & shared between rotation & CUI
#define CUICOM_ORIENTATION_POLICY_LANDSCAPE        0x0001    // bit 0
#define CUICOM_ORIENTATION_POLICY_PORTRAIT        0x0002    // bit 1

#define  COM_MAX_DISPLAYS           2
#define  COM_MAX_UID_PER_DISPLAY    2





#ifndef MAX_BUFFER_SIZE 
#   define MAX_BUFFER_SIZE 2048
#endif

#define GET_REG_VALUE        0x0001
#define SET_REG_VALUE        0x0010
    
typedef struct _COM_CUIREGISTRY_DWORD_ARGS {
    /*IN*/ ULONG            Cmd;
    /*IN*/ USHORT            Action;
    /*IN*/ WCHAR            pwszValueName[64];
    /*IN*/ /*OUT*/ DWORD    dwValue;
    /*OUT*/ NTSTATUS        Status;
} COM_CUIREGISTRY_DWORD_ARGS, *PCOM_CUIREGISTRY_DWORD_ARGS;

typedef struct _COM_CUIREGISTRY_BINARY_ARGS {
    /*IN*/ ULONG            Cmd;
    /*IN*/ USHORT            Action;
    /*IN*/ WCHAR            pwszValueName[64];
    /*IN*/ /*OUT*/ BYTE        buffer[MAX_BUFFER_SIZE];
    /*IN*/ DWORD            dwSize;
    /*OUT*/ NTSTATUS        Status;
} COM_CUIREGISTRY_BINARY_ARGS, *PCOM_CUIREGISTRY_BINARY_ARGS;

#if 0 
//XXX: Think about it later -- what PC14 is supporting
//     Application could enumerate display setting by itself 
//     and find out the capabilities.
typedef struct _CUI_REF_ESC {
    ULONG Cmd;
    ULONG ulDevice;
    ULONG ulRefreshRates;
} CUI_REF_ESC, *PCUI_REF_ESC , FAR *LPCUI_REF_ESC;
#endif 


#ifdef __cplusplus
        }; 
#endif  //__cplusplus

#pragma pack(pop, ESCAPECALLS)

#endif //end of #if!defined(__XP_ESCAPE_CALLS_H__)