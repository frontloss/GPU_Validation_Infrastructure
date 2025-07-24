/*=================================================================================================
;
;   Copyright (c) Intel Corporation (2000 - 2018)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;------------------------------------------------------------------------------------------------*/

//=================================================================================================
//									Display Config Get & Set
//=================================================================================================

/*------------------------------------------------------------------------------------------------*
*
* @file  DisplayConfig.h
* @brief This file contains Implementation of GetDisplayConfigInterfaceVersion, SetDisplayConfiguration
*        GetDisplayConfiguration, GetActiveDisplayConfiguration, GetAllSupportedModes, GetCurrentMode,
         GetOSPrefferedMode, SetDisplayMode, GetDisplayTimings, QueryDisplayConfigEx, PrintDriverModeTable,
         GetEnumeratedDisplayInfo, GetAllGfxAdapterDetails, EDSMemoryCleanup
*------------------------------------------------------------------------------------------------*/

#include "windows.h"
#include "CommonInclude.h"

#define EXPORT_API __declspec(dllexport)

#define TARGET_ID_MASK 0x00FFFFFF
#define DISPLAY_CONFIG_INTERFACE_VERSION 0x10
#define MAX_SUPPORTED_DISPLAYS 16
#define DEVICE_NAME_SIZE 64

#define NVIDIA_ADAPTER L"10DE"
#define AMD_ADAPTER L"1002"
#define DEFAULT_DESKTOPIMAGEINFO_INDEX 65535

#define SDC_VIRTUAL_REFRESH_RATE_AWARE 0x00020000
#define QDC_VIRTUAL_REFRESH_RATE_AWARE 0x00000040
#define DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE 0x00000010

// Macro that defines build number for windows 21H2 Cobalt OS
#define WIN_21H2_BUILD_NUMBER 19044

/* Macro to Unmask windows target id if OS is Win 10 or above we are masking windows target id
 *  since win 10 onwords though driver reports 24 bit target id, OS enumerate as 28 bit target id. */
#define UNMASK_TARGET_ID(a) (a & TARGET_ID_MASK)

#ifndef DISPLAY_CONFIG_H
#define DISPLAY_CONFIG_H

/** Structure Defination to hold OS Information */
typedef struct _OS_VERSION_INFO
{
    ULONG MajorVersion;
    ULONG MinorVersion;
    ULONG BuildNumber;
    ULONG PlatformId;
} OS_VERSION_INFO, *POS_VERSION_INFO;

/*! From 21H2 OS supports dynamic Mode RR setting, following enum defines whether the RR mode is dynamic or legacy */
typedef enum _RR_MODE
{
    LEGACY_RR  = 0,
    DYNAMIC_RR = 1
} RR_MODE;

/*! Configuration topology for switching display configuration */
typedef enum _DISPLAYCONFIG_TOPOLOGY
{
    TOPOLOGY_NONE = 0,
    SINGLE        = 1, ///< Single Display Configuration
    CLONE         = 2, ///< Clone Display Configuration [DDC, TDC, QDC etc.,.]
    EXTENDED      = 3, ///< Extended Display Configuration [ED, TED, QED etc.,.]
    HYBRID        = 4  ///< Hybrid Display Configuration
} DISPLAYCONFIG_TOPOLOGY;

/*! Supported Display Rotation  */
typedef enum _ROTATION
{
    ROTATE_UNSPECIFIED = 0,
    ROTATE_0           = 1, ///< Rotate Display Resolution to 0 degree
    ROTATE_90          = 2, ///< Rotate Display Resolution to 90 degree
    ROTATE_180         = 3, ///< Rotate Display Resolution to 180 degree
    ROTATE_270         = 4  ///< Rotate Display Resolution to 270 degree
} ROTATION;

/*! Supported Display Scanline Ordering  */
typedef enum _SCANLINE_ORDERING
{
    SCANLINE_ORDERING_UNSPECIFIED = 0,
    PROGRESSIVE                   = 1, ///< Progressive Scanline Ordering
    INTERLACED                    = 2  ///< Interlaced Scanline Ordering
} SCANLINE_ORDERING;

/*! Supported Pixel Format  */
typedef enum _PIXELFORMAT
{
    PIXELFORMAT_UNSPECIFIED = 0,
    PIXELFORMAT_8BPP        = 1,
    PIXELFORMAT_16BPP       = 2,
    PIXELFORMAT_24BPP       = 3,
    PIXELFORMAT_32BPP       = 4
} PIXELFORMAT;

/*! Supported Display Scaling  */
typedef enum _SCALING
{
    SCALING_NOTSPECIFIED = 0,
    CI                   = 1,
    FS                   = 2,
    MAR                  = 4,
    CAR                  = 8,
    MDS                  = 64
} SCALING;

/*! Pre-defined flags for QueryDisplayConfig and SetDisplayConfig calls */
typedef enum _FLAG_TYPES
{
    QDC_ACTIVE_PATHS               = 0, ///< QDC flags which includes active paths, current usage : used for QDC call prior to SDC
    QDC_FLAGS                      = 1, ///< QDC flags for fetching the current mode info
    SDC_FLAGS                      = 2, ///< SDC flags for setting display mode
    SDC_FLAGS_WITHOUT_OPTIMIZATION = 3  ///< SDC flag for setting display mode without optimization
} FLAG_TYPES;

/* Data structures detail */
#pragma pack(1)

/* Contains enumerated display specific */
typedef struct _DISPLAY_INFO
{
    _Out_ CONNECTOR_PORT_TYPE ConnectorNPortType; //< Connected Display Type (EDP/DP/HDMI)
    _Out_ UINT32 TargetID;                        //< Windows monitor ID
    _Out_ WCHAR FriendlyDeviceName[128];          //< Display Name (eg Digital Display / Built-in Display)
    _Out_ BOOLEAN IsActive;                       //< Display device is active or not
    _Out_ WCHAR PortType[128];                    //< Display is TC/TBT/Native
    _Out_ PANEL_INFO panelInfo;
} DISPLAY_INFO, *PDISPLAY_INFO;

/* Contains enumerated display details*/
typedef struct _ENUMERATED_DISPLAYS
{
    _In_ INT Size;                                                //< Size of ENUMERATED_DISPLAYS
    _Out_ DISPLAY_INFO ConnectedDisplays[MAX_SUPPORTED_DISPLAYS]; //< Connected Display List
    _Out_ INT Count;                                              //< No of connected display (active or inactive)
} ENUMERATED_DISPLAYS, *PENUMERATED_DISPLAYS;

typedef struct _OS_TOPOLOGY_INFO
{
    _Out_ DISPLAYCONFIG_TARGET_MODE targetModeInfo;
    _Out_ DISPLAYCONFIG_SOURCE_MODE sourceModeInfo;
    _Out_ DISPLAYCONFIG_DESKTOP_IMAGE_INFO desktopImageInfo;
    _Out_ DISPLAYCONFIG_PATH_INFO pathInfo;
} OS_TOPOLOGY_INFO, *POS_TOPOLOGY_INFO;

/*! Display Path Information */
typedef struct _DISPLAY_PATH_INFO
{
    _Inout_ INT pathIndex;        //< Connector type (Display Type) connected to which path
    _Inout_ UINT targetId;        //< Windows Monitor ID. Tobe removed in later
    _Out_ INT   sourceId;         //< Source device ID
    _Inout_opt_ BOOLEAN isActive; //< Specify whether display is currently active or not
    _Inout_ PANEL_INFO panelInfo;
    _Out_ UINT cloneGroupCount;
    _Out_ UINT extendedGroupCount;
    _Out_ UINT cloneGroupPathIds[MAX_SUPPORTED_DISPLAYS];
    _Out_ UINT extendedGroupPathIds[MAX_SUPPORTED_DISPLAYS];
    _Out_ OS_TOPOLOGY_INFO osTopologyInfo;
} DISPLAY_PATH_INFO, *PDISPLAY_PATH_INFO;

/*! Structure definition for Get/Set Display Configuration */
typedef struct _DISPLAY_CONFIG
{
    _In_ INT size;                                                     //< Size of DISPLAY_CONFIG
    _Inout_ DISPLAYCONFIG_TOPOLOGY topology;                           //< Display Configuration topology (SINGLE/CLONE/EXTENDED)
    _Inout_ DISPLAY_PATH_INFO displayPathInfo[MAX_SUPPORTED_DISPLAYS]; //< Array of displaypath info of type DISPLAY_PATH_INFO
    _Inout_ INT numberOfDisplays;                                      //< No of display to be part of configuration (active or inactive)
    _Out_ DISPLAY_CONFIG_ERROR_CODE status;                            //< Error Code
} DISPLAY_CONFIG, *PDISPLAY_CONFIG;

/*! Structure definition for Display Modes */
typedef struct _DISPLAY_MODE
{
    _Inout_ UINT targetId;                      //< Windows Monitor ID
    _Inout_ PANEL_INFO panelInfo;               //<Display and Adpater Information
    _Inout_ UINT HzRes;                         //< Horizontal Resolution
    _Inout_ UINT VtRes;                         //< Vertical Resolution
    _Inout_ ROTATION rotation;                  //< Display Rotation ( 0 Degree, 90 Degree, 180 Degree, 270 Degree)
    _Inout_ UINT refreshRate;                   //< Refresh Rate
    _Inout_ PIXELFORMAT BPP;                    //< Bit per pixel
    _Inout_ SCANLINE_ORDERING scanlineOrdering; //< Scanline Ordering (PROGRESSIVE or INTERLACED)
    _Inout_ SCALING scaling;                    //< Scaling for particular display mode
    _Inout_ UCHAR samplingMode;                 //< Sampling Mode (1 - RGB, 2 - YUV420)
    _Out_ UINT64 pixelClock_Hz;                 //< Pixel Clock (Hz)
    _Inout_ RR_MODE rrMode;                     //< Dynamic Refresh Rate Mode
    _Out_ DISPLAY_CONFIG_ERROR_CODE status;     //< Error Code for get/Set display mode
} DISPLAY_MODE, *PDISPLAY_MODE;

typedef struct _SCREEN_CAPTURE_ARGS
{
    _In_ UINT HzRes;
    _In_ UINT VtRes;
    _In_ PIXELFORMAT BPP;
} SCREEN_CAPTURE_ARGS;

typedef struct _QUERY_DISPLAY_CONFIG
{
    _Out_ UINT qdcFlag;
    _Out_ UINT targetId;
    _Out_ UINT topology;
    _Out_ DISPLAYCONFIG_PATH_INFO pathInfo;
    _Out_ DISPLAYCONFIG_TARGET_MODE modeInfoTargetMode;
    _Out_ DISPLAYCONFIG_SOURCE_MODE modeInfoSourceMode;
    _Out_ DISPLAYCONFIG_DESKTOP_IMAGE_INFO modeInfoDesktopInfo;
    _Out_ ULONG status;
} QUERY_DISPLAY_CONFIG, *PQUERY_DISPLAY_CONFIG;

typedef struct _ACTIVE_DISPLAY_INFO
{
    _Inout_ UINT targetId;
    _Inout_ UINT sourceId;
    _Inout_ UINT pathIndex;
    _Inout_ UINT cloneGroupCount;
    _Inout_ UINT extendedGroupCount;
    _Inout_ UINT cloneGroupTargetIds[MAX_SUPPORTED_DISPLAYS];
    _Inout_ UINT extendedGroupTargetIds[MAX_SUPPORTED_DISPLAYS];
    _Inout_ PANEL_INFO panelInfo; //<Display and Adpater Information
} ACTIVE_DISPLAY_INFO, *PACTIVE_DISPLAY_INFO;

typedef struct _ACTIVE_DISPLAY_CONFIG
{
    _Inout_ UINT size;
    _Inout_ DISPLAYCONFIG_TOPOLOGY topology;
    _Inout_ UINT numberOfDisplays;
    _Inout_ ACTIVE_DISPLAY_INFO displayInfo[MAX_SUPPORTED_DISPLAYS];
    _Out_ DISPLAY_CONFIG_ERROR_CODE status;
} ACTIVE_DISPLAY_CONFIG, *PACTIVE_DISPLAY_CONFIG;

/*! Structure definition for query Supported Mode list for all active displays  */
typedef struct _ENUMERATED_DISPLAY_MODES
{
    _In_ INT size;                          // Size of SUPPORTED_MODE_LIST
    _Inout_ PDISPLAY_MODE pDisplayMode;     // Pointer of DISPLAY_MODE Structure
    _Out_ INT noOfSupportedModes;           // No of active display mode list
    _Out_ DISPLAY_CONFIG_ERROR_CODE status; // Error Code
} ENUMERATED_DISPLAY_MODES, *PENUMERATED_DISPLAY_MODES;

/** Structure definition for Target Device Information */
typedef struct _TARGET_DEVICE_INFO
{
    _Out_ UINT width;                                                  //<Horizon Resolution for target Device
    _Out_ UINT height;                                                 //<Vertical Resolution for target Device
    _Out_ UINT vSyncFreqNumerator;                                     //<vSync timmings (Numerator)
    _Out_ UINT vSyncFreqDenominator;                                   //<vSync timmings (Denominator)
    _Out_ UINT hSyncFreqNumerator;                                     //<hSync timmings (Numerator)
    _Out_ UINT hSyncFreqDenominator;                                   //<hSync timmings (Denominator)
    _Out_ UINT64 pixelRate;                                            //<pixelRate
    _Out_ UINT videoStandard;                                          //<Video Standard
    _Out_ WCHAR monitorFriendlyDeviceName[DEVICE_NAME_SIZE];           //<Monitor Friendly Device Name
    _Out_ DISPLAYCONFIG_PIXELFORMAT pixelFormat;                       //<Pixel format 32 BPP or 24 BPP
    _Out_ DISPLAYCONFIG_ROTATION rotation;                             //<Display rotation
    _Out_ DISPLAYCONFIG_SCALING scaling;                               //<Scaling
    _Out_ DISPLAYCONFIG_SCANLINE_ORDERING scanLineOrdering;            //<Scanline ordering (PROGRESSIVE or INTERLACED)
    _Out_ DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY videoOutputTechnology; //<Output technology
} TARGET_DEVICE_INFO, *PTARGET_DEVICE_INFO;

/** Structure definition to hold dynamically allocated memory base address */
typedef struct _MEMORY_MGR
{
    _In_ PDISPLAY_MODE pDisplayMode; //< Pointer to Display Mode List for active target Id
    _In_ PINT noOfSupportedModes;    //< No of supported modes for active target Id
} MEMORY_MGR, *PMEMORY_MGR;

/** Structure definition for GFX Adpter Details */
typedef struct _GFX_ADAPTER_DETAILS
{
    UINT             size;
    UINT             numDisplayAdapter;
    GFX_ADAPTER_INFO adapterInfo[MAX_GFX_ADAPTER];
    UINT             status;
} GFX_ADAPTER_DETAILS, *PGFX_ADAPTER_DETAILS;

#pragma pack()

typedef struct _BDF_INFO
{
    UINT  bus;
    UINT  device;
    UINT  function;
    WCHAR busDeviceID[MAX_DEVICE_ID_LEN];
    bool  isActive;
} BDF_INFO;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// New DisplayConfig Rewrite Exposed functions.
EXPORT_API VOID __cdecl GetConfig(_Inout_ PDISPLAY_CONFIG pConfig);
EXPORT_API VOID __cdecl SetConfig(_Inout_ PDISPLAY_CONFIG pConfig);

EXPORT_API VOID __cdecl GetMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_MODE pDisplayMode);
EXPORT_API VOID __cdecl SetMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset);
EXPORT_API VOID __cdecl SetIgclMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset,
                                    _In_ PDISPLAY_TIMINGS pDisplayTimings);
EXPORT_API VOID __cdecl GetModes(_Inout_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes);
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

EXPORT_API VOID __cdecl GetDisplayConfigInterfaceVersion(_Out_ PINT pVersion);

EXPORT_API VOID __cdecl SetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig, _In_ BOOLEAN addForceModeEnumFlag);

EXPORT_API VOID __cdecl GetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig);

EXPORT_API VOID __cdecl GetActiveDisplayConfiguration(_Out_ PACTIVE_DISPLAY_CONFIG pDisplayConfig);

EXPORT_API LONG __cdecl ConfigureHDR(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable);

EXPORT_API VOID __cdecl GetAllSupportedModes(_Inout_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes);

EXPORT_API VOID __cdecl GetCurrentMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_MODE pDisplayMode);

EXPORT_API BOOLEAN __cdecl GetOSPrefferedMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_TIMINGS pDisplayTimings);

EXPORT_API BOOLEAN CaptureScreen(_In_ UINT instance, _In_ GFX_ADAPTER_INFO gfxAdapter, _In_ SCREEN_CAPTURE_ARGS captureArgs);

EXPORT_API VOID __cdecl SetDisplayMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset);

EXPORT_API VOID __cdecl GetDisplayTimings(_In_ PDISPLAY_MODE pCurrentMode, _Out_ PDISPLAY_TIMINGS pDisplayTimings);

EXPORT_API VOID __cdecl QueryDisplayConfigEx(_In_ UINT qdcFlag, _In_ PPANEL_INFO pPanelInfo, _Out_ PQUERY_DISPLAY_CONFIG pQueryDisplayConfig);

EXPORT_API VOID __cdecl PrintDriverModeTable(_In_ PPANEL_INFO pPanelInfo);

EXPORT_API VOID __cdecl GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode);

EXPORT_API VOID __cdecl GetAllGfxAdapterDetails(_Out_ PGFX_ADAPTER_DETAILS pAdapterDetails);

EXPORT_API VOID __cdecl EDSMemoryCleanup(VOID);

EXPORT_API UINT __cdecl GetBDFDetails(_Out_ BDF_INFO bdfData[], _Out_ UINT *numDisplayAdapter);

BOOLEAN CompareDisplayPathInfo(_In_ DISPLAY_PATH_INFO getConfig[], _In_ DISPLAY_PATH_INFO requestedConfig[], _In_ INT getConfigLength, _In_ INT requestedConfigLength);

#endif
