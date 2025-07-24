/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayPort.h
 * @brief    This header file contains Implementation of macros, GUIDs and structures used in
 *           Display Port SDK library
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "SdkSharedHeader.h"

#pragma once

#define MAX_VALID_CONFIG 500
#define MAX_MONITORS_PER_ADAPTER 6

#define MAX_LINK_COUNT 15
// As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

#define IGFX_VIDEO_MODE_LIST_SIZE_ONLY 1

#define CONFIGEX_VERSIONS_SUPPORTED 1
#define IS_CONFIGEX_VERSION_SUPPORTED(x) (x <= CONFIGEX_VERSIONS_SUPPORTED)

#define COLLAGE_STATUS_VERSION_SUPPORTED 1
#define IS_COLLAGE_STATUS_VERSION_SUPPORTED(x) (x <= COLLAGE_STATUS_VERSION_SUPPORTED)

#define VIDEO_MODELIST_VERSIONS_SUPPORTED 1
#define IS_VIDEO_MODELIST_VERSION_SUPPORTED(x) (x <= VIDEO_MODELIST_VERSIONS_SUPPORTED)

static const GUID IGFX_SUPPORTED_CONFIGURATIONS_EX = { 0x70fd0da7, 0xf8bd, 0x4afc, { 0x98, 0x98, 0xa5, 0xc1, 0x31, 0x7, 0xa4, 0x45 } };
static const GUID IGFX_GET_SET_N_VIEW_CONFIG_GUID  = { 0x21ada76b, 0xa70e, 0x4d4e, { 0x94, 0xe2, 0x4b, 0x8e, 0xe0, 0xcc, 0x32, 0x84 } };
static const GUID IGFX_GET_VIDEO_MODE_LIST_GUID    = { 0x42029a4, 0xf5f6, 0x4c4e, { 0x95, 0x19, 0xcf, 0xff, 0x76, 0x18, 0x82, 0xed } };
static const GUID IGFX_GET_SET_COLLAGE_STATUS_GUID = { 0x61a8470b, 0x918e, 0x48fb, { 0xb6, 0x5b, 0xa6, 0x84, 0x66, 0x78, 0xc2, 0xf1 } };

typedef struct _DPDeviceContext
{
    BOOL   gfxValSimStatus; // This flag says whether DP AUX Stub initialized or not
    HANDLE gfxValSimHandle; // Handle to DP AUX Stub driver
} DPDeviceContext;

/* Structure contains MST topology information */
struct DPMSTTopology
{
    CHAR node[8];   /* Array to hold name of the node where node can be Branch or Display */
    UINT parentId;  /* Parent id of the node */
    BOOL isVisited; /* Flag indicates whether node processed/compared or not */
};

typedef struct _IGFX_COLLAGE_STATUS
{
    IGFX_VERSION_HEADER versionHeader;
#if IS_COLLAGE_STATUS_VERSION_SUPPORTED(1)
    BOOL isCollageModeSupported;
    BOOL defaultCollageStatus; // This is always FALSE
    BOOL isCollageModeEnabled;
#endif
#if IS_COLLAGE_STATUS_VERSION_SUPPORTED(2)
    // For future extention
#endif
} IGFX_COLLAGE_STATUS;

typedef struct
{
    DWORD opMode;
    DWORD numDisplays;        // Number of displays
    DWORD primaryDeviceUID;   // Device on Primary Display( For Single Pipe Simultaneous mode, both devices are here )
    DWORD secondaryDeviceUID; // Device on Secondary Display
    DWORD thirdDeviceUID;     // Device on Third Display
    DWORD fourthDeviceUID;    // Device on Fourth Display
} IGFX_CONFIG_DATA_EX;

typedef struct
{
    IGFX_VERSION_HEADER versionHeader;
#if IS_CONFIGEX_VERSION_SUPPORTED(1)
    DWORD               numTotalConfig; // Total of validation configuration in the following array
    DWORD               reserved1;      // Reserved
    DWORD               reserved2;
    IGFX_CONFIG_DATA_EX configList[MAX_VALID_CONFIG]; // Valid device combinations, upto 7 devices
#endif
} IGFX_TEST_CONFIG_EX;

typedef struct _IGFX_DISPLAY_RESOLUTION_EX
{
    DWORD hResolution;       // Horizontal Resolution
    DWORD vResolution;       // Vertical Resolution
    DWORD refreshRate;       // Refresh Rate
    DWORD bitsPerPixel;      // Color Depth
    DWORD supportedStandard; // Reserved
    DWORD preferredStandard; // Reserved
    WORD  interlaceFlag;     // Resreved
} IGFX_DISPLAY_RESOLUTION_EX;

typedef struct _IGFX_DISPLAY_POSITION
{
    int left;   // Position - Left      ***********************************************************
    int right;  // Position - Right     ** Position Fields are optional. They are valid only for **
    int top;    // Position - Top       ** Secondary Display device in Extended Desktop.         **
    int bottom; // Position - Bottom    ***********************************************************

} IGFX_DISPLAY_POSITION;

typedef struct _IGFX_DISPLAY_CONFIG_DATA_EX
{
    DWORD                      displayUID;  // Display Device UID for this display
    IGFX_DISPLAY_RESOLUTION_EX resolution;  // Display Mode
    IGFX_DISPLAY_POSITION      position;    // Display Position
    DWORD                      tvStandard;  // Reserved
    BOOL                       isHDTV;      // Reserved
    DWORD                      orientation; // Orientation
    DWORD                      scaling;     // Reserved
    DWORD                      flags;       // Flags
} IGFX_DISPLAY_CONFIG_DATA_EX;

typedef struct _IGFX_VIDEO_MODE_LIST_EX
{
    IGFX_VERSION_HEADER versionHeader;
#if IS_VIDEO_MODELIST_VERSION_SUPPORTED(1)
    DWORD                       opMode;
    UINT                        numDisplays; // Number of active displays
    IGFX_DISPLAY_CONFIG_DATA_EX dispConfig[MAX_MONITORS_PER_ADAPTER];
    DWORD                       deviceID;
    DWORD                       flags;       // Flags: IGFX_VIDEO_MODE_LIST_SIZE_ONLY - to retrieve in
    WORD                        vmlNumModes; // Number of video modes in list
    DWORD                       reserved;    // Reserved
    IGFX_DISPLAY_RESOLUTION_EX  vmlModes[1]; // Array of modes
#endif
#if IS_VIDEO_MODELIST_VERSION_SUPPORTED(2)
    // add new code here for future releases
#endif
} IGFX_VIDEO_MODE_LIST_EX;

typedef struct _IGFX_SYSTEM_CONFIG_DATA_N_VIEW
{
    DWORD opMode;                               // Operating Mode
    DWORD flags;                                // Flags
    UINT  size;                                 // Reserved
    UINT  numDisplays;                          // Reserved
                                                // IGFX_DISPLAY_CONFIG_DATA_EX DispCfg[1]; // Array of Display Data
    IGFX_DISPLAY_CONFIG_DATA_EX dispConfig[16]; // Array of Display Data
} IGFX_SYSTEM_CONFIG_DATA_N_VIEW;
