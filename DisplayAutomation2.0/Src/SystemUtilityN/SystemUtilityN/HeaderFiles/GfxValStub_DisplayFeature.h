/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2015 Intel Corporation All Rights Reserved.      **
**                                                                      **
**  The source code contained or described herein and all documents     **
**  related to the source code ("Material") are owned by Intel          **
**  Corporation or its suppliers or licensors. Title to the Material    **
**  remains with Intel Corporation or its suppliers and licensors. The  **
**  Material contains trade secrets and proprietary and confidential    **
**  information of Intel or its suppliers and licensors. The Material   **
**  is protected by worldwide copyright and trade secret laws and       **
**  treaty provisions. No part of the Material may be used, copied,     **
**  reproduced, modified, published, uploaded, posted, transmitted,     **
**  distributed, or disclosed in any way without Intel's prior express  **
**  written permission.                                                 **
**                                                                      **
**  No license under any patent, copyright, trade secret or other       **
**  intellectual property right is granted to or conferred upon you by  **
**  disclosure or delivery of the Materials, either expressly, by       **
**  implication, inducement, estoppel or otherwise. Any license under   **
**  such intellectual property rights must be express and approved by   **
**  Intel in writing.                                                   **
**                                                                      **
*************************************************************************/

/**
 * file name       GfxValStub_DisplayFeature.h (This file has been copied from mainline driver (Source\miniport\LHDM\GfxValStub\inc). This file has to be maintained in sync with
 * driver file.) Date:           27/01/2015
 * @version        0.1
 * @Author		  Naveen SG /Darshan/Chandrakanth
 * Modified by
 * Description:
 */

/*
*********************************************************************************************
*********************************************************************************************
GVSTUB is an acronym for 'GFX VAL STUB'
*********************************************************************************************
*********************************************************************************************
*/

#include "GfxValStub_MetaData.h"

// Gfx Driver and Validation Driver/App should communicate w/o structure packing

/////////////////////////////////////////////////////////////////////////
// GfxValStub_DisplayFeature.h Content.               //
/////////////////////////////////////////////////////////////////////////

#ifndef GVSTUB_DISPLAY_FEATURE_H
#define GVSTUB_DISPLAY_FEATURE_H

#pragma pack(push, GFX_VAL_STUB_GFX_ACCESS)
#pragma pack(1)
/* To avoid warning*/
#pragma warning(disable : 4201)
#pragma warning(disable : 4214)

//
// ----- Type of Display -----
//
typedef enum
{
    GVSTUB_NULL_DISPLAY_TYPE = 0,
    GVSTUB_CRT_TYPE,
    GVSTUB_RESERVED_TYPE,
    GVSTUB_DFP_TYPE,
    GVSTUB_LFP_TYPE,
    GVSTUB_MAX_DISPLAY_TYPES = GVSTUB_LFP_TYPE
} GVSTUB_DISPLAY_TYPE;

// Different ports supported.
typedef enum
{
    GVSTUB_NULL_PORT_TYPE = -1,
    GVSTUB_ANALOG_PORT    = 0,
    GVSTUB_DVOA_PORT,
    GVSTUB_DVOB_PORT,
    GVSTUB_DVOC_PORT,
    GVSTUB_DVOD_PORT,
    GVSTUB_LVDS_PORT,
    GVSTUB_INTDPE_PORT,
    GVSTUB_INTHDMIB_PORT,
    GVSTUB_INTHDMIC_PORT,
    GVSTUB_INTHDMID_PORT,
    GVSTUB_INT_DVI_PORT,
    GVSTUB_INTDPA_PORT, // Embedded DP For ILK
    GVSTUB_INTDPB_PORT,
    GVSTUB_INTDPC_PORT,
    GVSTUB_INTDPD_PORT,
    GVSTUB_TPV_PORT, // This is for all the TPV Ports..
    GVSTUB_INTMIPIA_PORT,
    GVSTUB_INTMIPIC_PORT,
    GVSTUB_WIGIG_PORT,
    GVSTUB_DVOF_PORT,
    GVSTUB_INTHDMIF_PORT,
    GVSTUB_INTDPF_PORT,
    GVSTUB_DVOE_PORT,
    GVSTUB_INTHDMIE_PORT,
    GVSTUB_MAX_PORTS
} GVSTUB_PORT_TYPE;

/* ---------- Macro Definitions  ----------*/
/* --- MPO Simulation --- */
#define GVSTUB_MAX_PIPES 3
#define GVSTUB_MAX_DISPLAYS (GVSTUB_MAX_PORTS * 2)
#define GVSTUB_EDID_BLOCK_SIZE 128
#define GVSTUB_MAX_DIRTY_RECTS 8
#define GVSTUB_MAX_PLANES 13
#define GVSTUB_MAX_DPCD_ADDRESS 16

/* --- Device Simulation --- */
#define GVSTUB_MAX_EDID_BLOCKS 6
#define GVSTUB_MAX_DPCD_DATA 512
#define GVSTUB_MAX_ENCODERS 20
#define GVSTUB_VBT_MAX_SIZE 8192 // OpRegion Max size

#define GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION 0x1

// Error codes used by Gfx and Validation Driver to indicate the operation success/failure in this layer
#define GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS 0x00000000
#define GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE 0x00000001
#define GVSTUB_DISPLAY_FEATURE_STATUS_FW_NOT_ENABLED 0x00000002
#define GVSTUB_DISPLAY_FEATURE_STATUS_FEATURE_NOT_ENABLED 0x00000004
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_SIZE_MISMATCH 0x00000008
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_INVALID_FEATURE 0x00000010
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_INVALID_PARAMETER 0x00000020
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_PARAM_NULL_POINTER 0x00000040
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_FUNC_NULL_POINTER 0x00000080
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_MEMORY_ALLOCATION 0x00000100
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_DEV_SIM_ATTACH_ON_ATTACH 0x00000200
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_DEV_SIM_DETACH_WITHOUT_ATTACH 0x00000400
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_NO_DPCD_DATA 0x00000800
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_NO_MEMORY 0x00001000
#define GVSTUB_DISPLAY_FEATURE_STATUS_ERROR_INTERNAL 0x00000016 // Internal API errors
#define GVSTUB_DISPLAY_FEATURE_STATUS_VBT_REQUESTED_SIZE_EXCEEDS_6K_FAILURE 0x00002000
#define GVSTUB_DISPLAY_FEATURE_STATUS_REGISTRY_WRITE_FAILURE 0x00004000
#define GVSTUB_DISPLAY_FEATURE_STATUS_VBT_FETCH_FAILURE 0x00008000

// Enum specifying Features supported by the framework
typedef enum _GVSTUB_DISPLAY_FEATURE_REQUEST_TYPE
{
    GVSTUB_ENABLE_DISABLE_FRAMEWORK = 0, // Enable Disable the ULT mode
    GVSTUB_ENABLE_DISABLE_FEATURE,       // Enable Disable the feature in ULT
    GVSTUB_GET_SYSTEM_INFO,              // Get System Info
    GVSTUB_ENUM_DEVICE,                  // Enumerate Display Devices
    GVSTUB_GET_DEVICE_CONNECTIVITY,      // Get the HPD state of a DispUID
    GVSTUB_GET_EDID,                     // Get the EDID of a DispUID
    GVSTUB_CREATE_RESOURCE,              // Allocate the Surface
    GVSTUB_FREE_RESOURCE,                // Freeup the allocated resource
    GVSTUB_SET_SRC_ADDRESS,              // MMIO flip
    GVSTUB_GET_MPO_CAPS,                 // Get the MPO capability
    GVSTUB_GET_MPO_GROUP_CAPS,           // Get the MPO Group caps
    GVSTUB_CHECK_MPO,                    // Check MPO DDI
    GVSTUB_SET_SRC_ADD_MPO,              // MPO flip
    GVSTUB_DEV_SIM_CACHE_DPCD_DATA,      // Cache DPCD Info
    GVSTUB_GET_SET_SIMULATE_DEVICE,      // Device Simulation
    GVSTUB_CONFIGURE_UNDERRUN_INTERRUPT, // Configure Under-Run interrupt (Enable/Disable)
    GVSTUB_GET_SET_VBT_DATA,             // VBT Simulation
    GVSTUB_CHECK_MPO3,                   // Check MPO3 DDI
    GVSTUB_SET_SOURCE_ADDRESS_MPO3,      // MPO3 Flips
    GVSTUB_TRIGGER_DSB,                  // Trigger DSB
    // MAX_GVSTUB_FW_FUNCTIONS should be the last value in this enum
    MAX_GVSTUB_FW_FUNCTIONS
} GVSTUB_DISPLAY_FEATURE_REQUEST_TYPE;

/*********************************************************
 *  ---------    DFT Version Information     -------------
 *  Note: If any change in GfxValStub_DisplayFeature.h header file, version numbers should also be modified.
 **********************************************************/
#define GVSTUB_MAJ_VERSION_NUMBER 2
#define GVSTUB_MIN_VERSION_NUMBER 0

/* ---------- Macro to Read/Write ULT Return Code ---------- */

// Macro to set an error code
#define GVSTUB_STATUS_WRITE(GVSTUB_STATUS) pDisplayFeatureArgs->stDisplayFeatureMetaData.ulStatus = pDisplayFeatureArgs->stDisplayFeatureMetaData.ulStatus | GVSTUB_STATUS

// Specifies whether to set or get a feature
typedef enum _GVSTUB_OP_TYPE
{
    GVSTUB_OP_GET,
    GVSTUB_OP_SET,
} GVSTUB_OP_TYPE;

typedef enum _GVSTUB_REGISTRY_CONTROL
{
    GVSTUB_RESET = 0,
    GVSTUB_SET
} GVSTUB_REGISTRY_CONTROL;

//
// Specifies the types of features for Display Framework
//
typedef enum _GVSTUB_DISPLAY_FEATURE
{
    GVSTUB_FEATURE_PRIVATE_FLIP,
    GVSTUB_FEATURE_PRIVATE_MPOFLIP,
    GVSTUB_FEATURE_DEV_SIM
} GVSTUB_DISPLAY_FEATURE;

//
// Structure for enable or Disable Framework.
//
typedef struct _GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS
{
    IN BOOLEAN bEnableFramework; // Enable/Disable DFT framework in Gfx Driver
    IN ULONG ulBufferSize;       // Size of the Buffer
    IN OUT BYTE Buffer[1];       // Security cookie. WIP
    OUT ULONG ucMajVer;          // Max Version Number
    OUT ULONG ucMinVer;          // Min Version Number
} GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS, *PGVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS;

//
// Structure for enable or Disable a particular feature.
//
typedef struct _GVSTUB_ENABLE_DISABLE_FEATURE_ARGS
{
    IN BOOLEAN bEnableFeature;                // Enable/Disable the Specific Feature in ULT
    IN GVSTUB_DISPLAY_FEATURE eFeatureEnable; //  Enum indicating which feature to enable
} GVSTUB_ENABLE_DISABLE_FEATURE_ARGS, *PGVSTUB_ENABLE_DISABLE_FEATURE_ARGS;

/* ----- ULT Escape - "GVSTUB_GET_SYSTEM_INFO" ----- */
typedef struct _GVSTUB_CHIPSET_INFO
{
    OUT ULONG eChipsetFamily;
    OUT ULONG ePlatformType;
} GVSTUB_CHIPSET_INFO, *PGVSTUB_CHIPSET_INFO;

//
// structure for CPU Information
//
typedef struct _GVSTUB_CPU_INFO
{
    OUT ULONG ulCPU_ID;
    OUT WCHAR wcAdpterType[256];
} GVSTUB_CPU_INFO, *PGVSTUB_CPU_INFO;

//
// Structure for Sytem inforamtion.
//
typedef struct _GVSTUB_SYSTEM_INFO_ARGS
{
    OUT ULONG ulSkuFeatureList;
    OUT GVSTUB_CHIPSET_INFO stChipSetInfo;
    OUT GVSTUB_CPU_INFO stCPUInfo;
} GVSTUB_GET_SYSTEM_INFO_ARGS, *PGVSTUB_GET_SYSTEM_INFO_ARGS;

//
// Structure for display information
//
typedef struct _GVSTUB_DISPLAY_DETAILS_ARGS
{
    OUT ULONG ulDisplayUID;               // unique id for display
    OUT GVSTUB_DISPLAY_TYPE eDisplayType; // display type
    OUT BOOLEAN bExternalEncoderDriven;   // can it be driven by external encoder
    OUT BOOLEAN bTPVDrivenEncoder;
    OUT GVSTUB_PORT_TYPE ePortType;     // port type
    OUT BOOLEAN bInternalPortraitPanel; // is it an internal portrait panel
    OUT ULONG ulConnectorType;          // connector type
} GVSTUB_DISPLAY_DETAILS_ARGS, *PGVSTUB_DISPLAY_DETAILS_ARGS;

//
// Structure for VBT Get/Set
//
typedef struct _GVSTUB_GET_SET_VBT_ARGS
{
    IN ULONG ulVBTSize;                     // VBT Size
    IN BYTE ulVBTData[GVSTUB_VBT_MAX_SIZE]; // VBT Data
    IN BOOLEAN bEnable;                     // 0: Disable, 1: Enable
    IN BOOLEAN bSet;                        // 0: Get, 1: Set
} GVSTUB_GET_SET_VBT_ARGS, *PGVSTUB_GET_SET_VBT_ARGS;

//
// Structure to list all the supported display/port information.
//
typedef struct _GVSTUB_ENUM_DEVICE_ARGS
{
    OUT ULONG ulNumDisplays;                                                   // number of displays with valid data
    OUT GVSTUB_DISPLAY_DETAILS_ARGS stDisplayDetailsArgs[GVSTUB_MAX_DISPLAYS]; // max display info list
} GVSTUB_ENUM_DEVICE_ARGS, *PGVSTUB_ENUM_DEVICE_ARGS;

//
// Structure for device connnectivity Status.
//
typedef struct _GVSTUB_GET_DEVICE_CONNECTIVITY_ARGS
{
    IN ULONG ulDisplayUID; // Display UID
    OUT BOOLEAN bAttached; // HPD state of the Display
} GVSTUB_GET_DEVICE_CONNECTIVITY_ARGS, *PGVSTUB_GET_DEVICE_CONNECTIVITY_ARGS;

//
// Structure to get or set EDID Data.
//
typedef struct _GVSTUB_GET_EDID_ARGS
{
    IN ULONG ulDisplayUID;                        // Which target ID
    IN ULONG ulEdidBlockNum;                      // EDID Block
    OUT UCHAR ucEdidData[GVSTUB_EDID_BLOCK_SIZE]; // the Raw EDID data
} GVSTUB_GET_EDID_ARGS, *PGVSTUB_GET_EDID_ARGS;

//
// Structure to set DPCD Data
//
typedef struct _GVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS
{
    IN ULONG ulDisplayUID;                    // which Target ID
    IN ULONG ulDPCDAddress;                   // DPCD address it should be written to.
    IN BYTE ucDPCDData[GVSTUB_MAX_DPCD_DATA]; // DPCD Data
    IN ULONG ulSize;                          // number of valid dpcd bytes.
    IN ULONG ulIndex;                         // Index of the dpcd transaction.
} GVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS, *PGVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS;

//
// Structure contains information for a device
//
typedef struct _GVSTUB_DEVICE_INFO
{
    IN GVSTUB_OP_TYPE OpType;  // Get or Set
    IN OUT BOOLEAN bAttach;    // HPD state of display
    IN OUT ULONG ulDisplayUID; // Target ID to attach/detach
    IN OUT ULONG ulPortType;
    IN OUT BYTE ucDisplayEdid[GVSTUB_MAX_EDID_BLOCKS][GVSTUB_EDID_BLOCK_SIZE]; // Applicable for attach or query for connected device. For detach, this field is irrelevant
    IN BOOLEAN bSimConnnectionInLowPower;                                      // If set, the action of attach or detach is deferred till low power mode.
} GVSTUB_DEVICE_INFO, *PGVSTUB_DEVICE_INFO;

//
// Structure for Simulate a set of Devices(Hotplug/unplug) at a time
//
typedef struct _GVSTUB_GET_SET_SIMULATE_DEVICE_ARGS
{
    IN ULONG ulNumDevices;                                   // Number of devices for simulation
    IN GVSTUB_DEVICE_INFO stDeviceInfo[GVSTUB_MAX_ENCODERS]; // Device information of each device to be simulated.
} GVSTUB_GET_SET_SIMULATE_DEVICE_ARGS, *PGVSTUB_GET_SET_SIMULATE_DEVICE_ARGS;

/* ---------- GVSTUB_FRAMEWORK_DATA  ----------*/
typedef struct _GVSTUB_COMMON_FW_CONTEXT
{
    BOOLEAN bInULTMode;
    ULONG   ucMajVer; // Major Version Number
    ULONG   ucMinVer; // Minor Version Number
} GVSTUB_COMMON_FW_CONTEXT, *PGVSTUB_COMMON_FW_CONTEXT;

typedef struct _GVSTUB_FLIP_CONTEXT
{
    UCHAR ucMPOPipeIndex[GVSTUB_MAX_PIPES];
    UCHAR ucMMIOPipeIndex[GVSTUB_MAX_PIPES];
} GVSTUB_FLIP_CONTEXT, *PGVSTUB_FLIP_CONTEXT;

typedef struct _GVSTUB_DPCD_DATA
{
    IN ULONG ulDPCDAddress;
    IN BYTE ucDPCDData[GVSTUB_MAX_DPCD_DATA];
    IN ULONG ulSize;
} GVSTUB_DPCD_DATA, *PGVSTUB_DPCD_DATA;

typedef struct _GVSTUB_DPCD_CONTEXT
{
    ULONG            ulNumAuxTransactions; // Caching this as useful information
    BOOLEAN          bIsDPCDDataSet;
    GVSTUB_DPCD_DATA stDPCDData[GVSTUB_MAX_DPCD_ADDRESS];
} GVSTUB_DPCD_CONTEXT, *PGVSTUB_DPCD_CONTEXT;

typedef struct _GVSTUB_INTERNAL_DEVICE_INFO
{
    ULONG               ulDisplayUID;
    ULONG               ulPort;
    BOOLEAN             bAttach;
    BYTE                ucDisplayEdid[GVSTUB_MAX_EDID_BLOCKS][GVSTUB_EDID_BLOCK_SIZE];
    BOOLEAN             bSimConnnectionInLowPower;
    GVSTUB_DPCD_CONTEXT stDPCDContext;
} GVSTUB_INTERNAL_DEVICE_INFO, *PGVSTUB_INTERNAL_DEVICE_INFO;

typedef struct _GVSTUB_DEVICE_SIM_CONTEXT
{
    ULONG                       ulNumDevices;
    GVSTUB_INTERNAL_DEVICE_INFO stDeviceInfo[GVSTUB_MAX_ENCODERS];
} GVSTUB_DEVICE_SIM_CONTEXT, *PGVSTUB_DEVICE_SIM_CONTEXT;

typedef struct _GVSTUB_FRAMEWORK_FEATURE
{
    union {
        struct
        {
            ULONG ulIntFlip : 1;
            ULONG ulIntMPOFlip : 1;
            ULONG ulDeviceSim : 1;
            ULONG ulRESERVED : 28;
        };
        ULONG ulValue;
    };
} GVSTUB_FRAMEWORK_FEATURE, *PGVSTUB_FRAMEWORK_FEATURE;

typedef struct _GVSTUB_VAL_DISPLAY_CONTEXT
{
    GVSTUB_COMMON_FW_CONTEXT  stCommonDisplayContext;
    GVSTUB_FLIP_CONTEXT       stFlipContext;
    GVSTUB_DEVICE_SIM_CONTEXT stDevSimContext;
    HANDLE                    hFileHandleForSimContextData;
    GVSTUB_FRAMEWORK_FEATURE  stFwFeature;
} GVSTUB_VAL_DISPLAY_CONTEXT, *PGVSTUB_VAL_DISPLAY_CONTEXT;

typedef struct _GVSTUB_VAL_CONTEXT
{
    GVSTUB_VAL_DISPLAY_CONTEXT stValStubDisplayContext; // Context Related to display.
    // Other component context to be declared below if any.
} GVSTUB_VAL_CONTEXT, *PGVSTUB_VAL_CONTEXT;

#pragma region Structures for Enable PIPE Under Run Interrupt Start

/*
PIPE configuration type
*/
typedef enum _GVSTUB_UNDER_RUN_EVENTS
{
    GVSTUB_UNDERRUN_UNDEFINED,
    GVSTUB_UNDERRUN_PIPEA,    // Also Provide support for enable only PIPE A Underrun
    GVSTUB_UNDERRUN_PIPEB,    // Also Provide support for enable only PIPE B Underrun
    GVSTUB_UNDERRUN_PIPEC,    // Also Provide support for enable only PIPE C Underrun
    GVSTUB_UNDERRUN_ALL_PIPE, // By Default we should use All PIPE for capture Underrun
} GVSTUB_UNDER_RUN_EVENTS;

/*
Structure defination to configure Under-Run Interrupt (ENABLE/DISABLE)
*/
typedef struct _GVSTUB_PIPE_UNDER_RUN_ARGS
{
    IN BOOLEAN bEnable;                            // 1 for Enable Interrupt 0 for Disable Interrupt
    IN GVSTUB_UNDER_RUN_EVENTS eUnderRunEventType; // specify which PIPE need to configure

} GVSTUB_PIPE_UNDER_RUN_ARGS, *PGVSTUB_PIPE_UNDER_RUN_ARGS;

#pragma endregion Structures for Enable PIPE Under Run Interrupt End

// MPO & MMIO Related structures. Kept as place holder. will be enabled in Phase2 check-in.

// ----- "GVSTUB_CREATE_RESOURCE" -----
// Src Pixel Format.
// There is 1:1 maping between GVSTUB_PIXELFORMAT and SB_PIXELFORMAT. Any change in SB_PIXELFORMAT should be updated here also.
typedef enum _GVSTUB_PIXELFORMAT
{
    GVSTUB_PIXEL_FORMAT_UNINITIALIZED = 0,
    GVSTUB_PIXEL_FORMAT_8BPP_INDEXED, // for 8bpp
    GVSTUB_PIXEL_FORMAT_B5G6R5X0,     // for 16bpp
    GVSTUB_PIXEL_FORMAT_B8G8R8X8,     // for 32bpp (default)
    GVSTUB_PIXEL_FORMAT_B8G8R8A8,
    GVSTUB_PIXEL_FORMAT_R8G8B8X8,
    GVSTUB_PIXEL_FORMAT_R8G8B8A8,
    GVSTUB_PIXEL_FORMAT_R10G10B10X2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_R10G10B10A2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_B10G10R10X2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_B10G10R10A2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    GVSTUB_PIXEL_FORMAT_R16G16B16X16F,       // for 64bpp, 16bit floating
    GVSTUB_PIXEL_FORMAT_R16G16B16A16F,
    GVSTUB_PIXEL_FORMAT_NV12YUV420,
    GVSTUB_PIXEL_FORMAT_YUV422,
    GVSTUB_PIXEL_FORMAT_MAX_PIXELFORMAT,
} GVSTUB_PIXELFORMAT;

typedef struct _GVSTUB_CREATE_RES_ARGS
{
    IN GVSTUB_PIXELFORMAT eFormat; // Surface format
    IN BOOLEAN bAuxSurf;           // Flag to indicate req for aux surface
    struct
    {
        ULONG ulLinear : 1;
        ULONG ulTiledW : 1;
        ULONG ulTiledX : 1;
        ULONG ulTiledY : 1;
        ULONG ulTiledYf : 1;
        ULONG ulTiledYs : 1;
        ULONG Reserved : 26;
    } Info;
    IN ULONG ulBaseWidth;  // Surface Width
    IN ULONG ulBaseHeight; // Surface Height
    // Out parameters
    OUT UINT64 pGmmBlock;           // To be used in the Setsource address calls
    OUT UINT64 pUserVirtualAddress; // For the app to access the ubuffer using CPU
    OUT UINT64 u64SurfaceSize;      // For app to copy the private framebuffer content
    OUT ULONG ulPitch;
} GVSTUB_CREATE_RES_ARGS, *PGVSTUB_CREATE_RES_ARGS;

//----- GVSTUB_FREE_RESOURCE -----
typedef struct _GVSTUB_FREE_RES_ARGS
{
    IN UINT64 pGmmBlock;
} GVSTUB_FREE_RES_ARGS, *PGVSTUB_FREE_RES_ARGS;

// ----- "GVSTUB_SET_SRC_ADDRESS" -----
typedef struct _GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS
{
    union {
        struct
        {

            UINT uiModeChange : 1;              // 0x00000001
            UINT uiFlipImmediate : 1;           // 0x00000002
            UINT uiFlipOnNextVSync : 1;         // 0x00000004
            UINT uiFlipStereo : 1;              // 0x00000008 This is a flip from a stereo alloc. Used in addition to FlipImmediate or FlipOnNextVSync.
            UINT uiFlipStereoTemporaryMono : 1; // 0x00000010 This is a flip from a stereo alloc. The left image should used. Used in addition to FlipImmediate or FlipOnNextVSync.
            UINT uiFlipStereoPreferRight : 1;   // 0x00000010 This is a flip from a stereo alloc. The right image should used when cloning to a mono monitor. Used in addition to
                                                // FlipImmediate or FlipOnNextVSync.
            UINT uiSharedPrimaryTransition : 1; // 0x00000020 We are transitioning to or away from a shared managed primary allocation
            UINT Reserved : 25;                 // 0xFFFFFFC0
        };
        UINT Value;
    };
} GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS;

typedef struct _GVSTUB_SET_SRC_ADD_ARGS
{
    IN GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS stFlags;
    IN ULONG ulSrcID;    // The Vidpn source ID
    IN UINT64 pGmmBlock; // The Surface allocated in create resource call
    IN ULONG ulDuration; // the Duarion parameter for entering 48 Hz
} GVSTUB_SET_SRC_ADD_ARGS, *PGVSTUB_SET_SRC_ADD_ARGS;

//  ----- MPO Specific Structure/Enum Definitions -----

// ------ "GVSTUB_GET_MPO_CAPS" -----
typedef struct _GVSTUB_MPO_CAPS
{
    UINT uiMaxPlanes;
    UINT uiNumCapabilityGroups;
} GVSTUB_MPO_CAPS, *PGVSTUB_MPO_CAPS;

typedef struct _GVSTUB_MPO_CAPS_ARGS
{
    IN ULONG ulVidpnSourceID;
    OUT GVSTUB_MPO_CAPS stMPOCaps;
} GVSTUB_MPO_CAPS_ARGS, *PGVSTUB_MPO_CAPS_ARGS;

// ------ "GVSTUB_MPO_GROUP_CAPS" -----
typedef struct _GVSTUB_MPO_GROUP_CAPS
{
    UINT uiMaxPlanes;
    UINT uiMaxStretchFactorNum;
    UINT uiMaxStretchFactorDenm;
    UINT uiMaxShrinkFactorNum;
    UINT uiMaxShrinkFactorDenm;
    UINT uiOverlayFtrCaps;
    UINT uiStereoCaps;
} GVSTUB_MPO_GROUP_CAPS, *PGVSTUB_MPO_GROUP_CAPS;

typedef struct _GVSTUB_MPO_GROUP_CAPS_ARGS
{
    // Need not Escape code inside this as UMD_GENERAL_ESCAPE_BUFFER of which this structure //would be part will have it.
    IN ULONG ulVidpnSourceID;
    IN UINT uiGroupIndex;
    OUT GVSTUB_MPO_GROUP_CAPS stMPOGroupCaps;
} GVSTUB_MPO_GROUP_CAPS_ARGS, *PGVSTUB_MPO_GROUP_CAPS_ARGS;

// ------ "GVSTUB_CHECK_MPO" -----
typedef struct _GVSTUB_M_RECT
{
    LONG left;
    LONG top;
    LONG right;
    LONG bottom;
} GVSTUB_M_RECT, *PGVSTUB_M_RECT;

typedef enum _GVSTUB_MPO_ROTATION
{
    GVSTUB_MPO_ROTATION_IDENTITY = 1,
    GVSTUB_MPO_ROTATION_90       = 2,
    GVSTUB_MPO_ROTATION_180      = 3,
    GVSTUB_MPO_ROTATION_270      = 4
} GVSTUB_MPO_ROTATION;

typedef enum _GVSTUB_MPO_PLANE_ORIENTATION
{
    GVSTUB_MPO_ORIENTATION_DEFAULT = 0,                              // Default value
    GVSTUB_MPO_ORIENTATION_0       = GVSTUB_MPO_ORIENTATION_DEFAULT, // 0 degree
    GVSTUB_MPO_ORIENTATION_90      = 1,                              // 90 degree, supported Gen9 onwards
    GVSTUB_MPO_ORIENTATION_180     = 2,                              // 180 degree
    GVSTUB_MPO_ORIENTATION_270     = 3,                              // 270 degree, supported Gen9 onwards
} GVSTUB_MPO_PLANE_ORIENTATION;

typedef struct _GVSTUB_MPO_BLEND_VAL
{
    union {
        struct
        {
            UINT AlphaBlend : 1;
            UINT Reserved : 31;
        };
        UINT uiValue;
    };
} GVSTUB_MPO_BLEND_VAL, *PGVSTUB_MPO_BLEND_VAL;

// Not in Dx9 spec
// Matches Kernel flip attribute.
typedef enum _GVSTUB_MPO_VIDEO_FRAME_FORMAT
{
    GVSTUB_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE                   = 0x0,
    GVSTUB_MPO_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST    = 0x1,
    GVSTUB_MPO_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST = 0x2
} GVSTUB_MPO_VIDEO_FRAME_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _GVSTUB_MPO_STEREO_FORMAT
{
    GVSTUB_MPO_FORMAT_MONO               = 0,
    GVSTUB_MPO_FORMAT_HOR                = 1,
    GVSTUB_MPO_FORMAT_VER                = 2,
    GVSTUB_MPO_FORMAT_SEPARATE           = 3,
    GVSTUB_MPO_FORMAT_ROW_INTERLEAVED    = 5, //??????? 4 is missing ?????
    GVSTUB_MPO_FORMAT_COLUMN_INTERLEAVED = 6,
    GVSTUB_MPO_FORMAT_CHECKBOARD         = 7
} GVSTUB_MPO_STEREO_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _GVSTUB_MPO_STEREO_FLIP_MODE
{
    GVSTUB_MPO_FLIP_NONE   = 0,
    GVSTUB_MPO_FLIP_FRAME0 = 1,
    GVSTUB_MPO_FLIP_FRAME1 = 2
} GVSTUB_MPO_STEREO_FLIP_MODE;

typedef enum _GVSTUB_MPO_STRETCH_QUALITY
{
    GVSTUB_MPO_STRETCH_QUALITY_BILINEAR = 0x1, // Bilinear
    GVSTUB_MPO_STRETCH_QUALITY_HIGH     = 0x2  // Maximum
} GVSTUB_MPO_STRETCH_QUALITY;

typedef struct _GVSTUB_MPO_PLANE_ATTRIBUTES
{
    UINT                         uiMPOFlags;
    GVSTUB_M_RECT                stMPOSrcRect;
    GVSTUB_M_RECT                stMPODstRect;
    GVSTUB_M_RECT                stMPOClipRect;
    GVSTUB_MPO_ROTATION          eMPORotation;
    GVSTUB_MPO_PLANE_ORIENTATION eHWOrientation;
    GVSTUB_MPO_BLEND_VAL         stMPOBlend;
    // Commenting the filters part as of now since it is not in latest Spec but it might come back, so it can be commented out for now.
    // UINT	uiMPONumFilters;
    // MPO_FILTER_VAL	stFilterVal[MAX_FILTERS];
    GVSTUB_MPO_VIDEO_FRAME_FORMAT eMPOVideoFormat;
    UINT                          uiMPOYCbCrFlags;

    // Not in Dx9 Spec
    GVSTUB_MPO_STEREO_FORMAT    eMPOStereoFormat;
    BOOLEAN                     bMPOLeftViewFrame0;
    BOOLEAN                     bMPOBaseViewFrame0;
    GVSTUB_MPO_STEREO_FLIP_MODE eMPOStereoFlipMode;
    GVSTUB_MPO_STRETCH_QUALITY  eStretchQuality;
    // Currently Driver may not use this info.
    UINT          uiDirtyRectCount;
    GVSTUB_M_RECT DIRTYRECTS[GVSTUB_MAX_DIRTY_RECTS];
} GVSTUB_MPO_PLANE_ATTRIBUTES, *PGVSTUB_MPO_PLANE_ATTRIBUTES;

// Surface memory type
typedef enum _GVSTUB_SURFACE_MEMORY_TYPE
{
    GVSTUB_SURFACE_MEMORY_INVALID        = 0,
    GVSTUB_SURFACE_MEMORY_LINEAR         = 1, // Surface uses linear momory
    GVSTUB_SURFACE_MEMORY_TILED          = 2, // Surface uses tiled memory
    GVSTUB_SURFACE_MEMORY_X_TILED        = GVSTUB_SURFACE_MEMORY_TILED,
    GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED = 4, // Surface uses Legacy Y tiled memory (Gen9+)
    GVSTUB_SURFACE_MEMORY_Y_F_TILED      = 8, // Surface uses Y F tiled memory
} GVSTUB_SURFACE_MEMORY_TYPE;

// Struct representing surface memory offset data
typedef struct _GVSTUB_SURFACE_MEM_OFFSET_INFO
{
    IN GVSTUB_SURFACE_MEMORY_TYPE eSurfaceMemType;
    union {
        IN ULONG ulLinearOffset;

        struct
        {
            IN ULONG ulTiledXOffset;
            IN ULONG ulTiledYOffset;
            IN ULONG ulTiledUVXOffset; // NV12 case
            IN ULONG ulTiledUVYOffset; // NV12 case
        };
    };

    IN ULONG ulUVDistance;  // For NV12 surface
    IN ULONG ulAuxDistance; // Control surface Aux Offset.
} GVSTUB_SURFACE_MEM_OFFSET_INFO, *PGVSTUB_SURFACE_MEM_OFFSET_INFO;

// GVSTUB_PIXELFORMAT is defined in GVSTUB_CREATE_RESOURCE escape structures/enums section of header.
typedef struct _GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO
{
    UINT                           uiLayerIndex;
    BOOLEAN                        bEnabled;
    GVSTUB_MPO_PLANE_ATTRIBUTES    stPlaneAttributes;
    GVSTUB_SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    GVSTUB_PIXELFORMAT             eULTPixelFormat;
    BOOLEAN                        bIsAsyncMMIOFlip;
} GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO, *PGVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO;

typedef struct _GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO
{
    IN UINT uiPlaneCount;
    IN GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO stMPOPlaneInfo[GVSTUB_MAX_PLANES];
} GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO, *PGVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO;

typedef struct _GVSTUB_CHECKMPOSUPPORT_RETURN_INFO
{
    union {
        struct
        {
            UINT uiFailingPlane : 4; // 0 based index of first plane that is //causing the CheckMPOSupport to fail.
            UINT TryAgain : 1;       // Configuration not supported due to hw in //transition condition, this should shortly go away.
        };
        UINT uiValue;
    };
} GVSTUB_CHECKMPOSUPPORT_RETURN_INFO, *PGVSTUB_CHECKMPOSUPPORT_RETURN_INFO;

typedef struct _GVSTUB_CHECK_MPO_ARG
{
    IN DWORD dwSourceID;
    IN GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO stCheckMPOPathInfo[GVSTUB_MAX_PIPES];
    IN ULONG ulNumPaths;
    IN ULONG ulConfig;

    OUT BOOLEAN bSupported;
    OUT ULONG ulFailureReason;
    OUT GVSTUB_CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo;
} GVSTUB_CHECK_MPO_ARGS, *PGVSTUB_CHECK_MPO_ARGS;
// stMPOCheckSuppReturnInfo

// ----- ULT Escape - "GVSTUB_SET_SRC_ADD_MPO" -----
// GVSTUB_MPO_PLANE_ATTRIBUTES is defined in GVSTUB_CHECK_MPO escape structures/enums section of header.
typedef struct GVSTUB_MPO_FLIP_PLANE_INFO
{
    UINT                        uiLayerIndex;
    BOOLEAN                     bEnabled;
    BOOLEAN                     bAffected;
    UINT                        uiAllocationSegment;
    ULONG                       AllocationAddress;
    HANDLE                      hAllocation;
    GVSTUB_MPO_PLANE_ATTRIBUTES stPlaneAttributes;
} GVSTUB_MPO_FLIP_PLANE_INFO, *PGVSTUB_MPO_FLIP_PLANE_INFO;

// GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS is defined in GVSTUB_SET_SRC_ADDRESS escape structures/enums section of header.
typedef struct _GVSTUB_SET_SRC_ADD_MPO_ARGS
{
    GVSTUB_MPO_FLIP_PLANE_INFO         stDxgkMPOPlaneArgs[GVSTUB_MAX_PLANES];
    ULONG                              ulNumPlanes;
    GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS ulFlags;
    DWORD                              dwSourceID;
} GVSTUB_SET_SRC_ADD_MPO_ARGS, *PGVSTUB_SET_SRC_ADD_MPO_ARGS;

#pragma region Structures for DSB Update Start

typedef enum _GVSTUB_DSB_SELECTOR
{
    GVSTUB_DSB_SELECTOR_NONE = -1,
    GVSTUB_DSB_SELECTOR_PIPE, // The General purpose pipe DSB
    GVSTUB_DSB_SELECTOR_LACE, // DSB dedicated to LACE
    GVSTUB_DSB_SELECTOR_HDR,  // DSB dedicated for HDR
    GVSTUB_DSB_SELECTOR_MAX
} GVSTUB_DSB_SELECTOR;

typedef enum _GVSTUB_DSB_TRIGGER_MODE
{
    GVSTUB_DSB_TRIGGER_MODE_NONE = 0,
    GVSTUB_DSB_TRIGGER_MODE_SYNC,     // Call waits for the DSB execution to be complete
    GVSTUB_DSB_TRIGGER_MODE_ASYNC,    // Async option: Call returns before the execution is complete. Next call will wait for first DSB execution to complete
    GVSTUB_DSB_TRIGGER_MODE_OVERRIDE, // Async option: Advanced Async type which supports clearing an already queued Async request and put a new one in place// TBD
    GVSTUB_DSB_TRIGGER_MODE_APEND,
    GVSTUB_DSB_TRIGGER_MODE_MAX
} GVSTUB_DSB_TRIGGER_MODE;

typedef struct _GVSTUB_DSB_OFFSET_DATA_PAIR
{
    ULONG Offset;
    ULONG Data;
} GVSTUB_DSB_OFFSET_DATA_PAIR, *PGVSTUB_DSB_OFFSET_DATA_PAIR;

typedef struct _GVSTUB_DSB_PIPE_ARGS
{
    ULONG PipeIndex;
    ULONG ScanlineCountOffset;
    ULONG FrameCountOffset;
} GVSTUB_DSB_PIPE_ARGS, *PGVSTUB_DSB_PIPE_ARGS;

typedef enum _GVSTUB_DSB_SYNC_TYPE
{
    GVSTUB_DSB_WAIT_FOR_NONE = 0,
    GVSTUB_DSB_WAIT_FOR_VBLANK,
    GVSTUB_DSB_WAIT_FOR_U_SEC,
    GVSTUB_DSB_WAIT_FOR_SCANLINES,
    GVSTUB_DSB_WAIT_FOR_SCANLINE_IN_RANGE,
    GVSTUB_DSB_WAIT_FOR_SCANLINE_OUT_OF_RANGE,
    GVSTUB_DSB_WAIT_FOR_POLL_REG,
} GVSTUB_DSB_SYNC_TYPE;

/* Structure for DSB write with contiguous polling */
typedef struct _GVSTUB_DSB_POLL_ARGS
{
    ULONG PollOffset;
    ULONG PollValue;
    ULONG PollMask;
} GVSTUB_DSB_POLL_ARGS, *PGVSTUB_DSB_POLL_ARGS;

/* DSB buffer to trigger DSB per pipe */
typedef struct _GVSTUB_DSB_BUFFER_ARGS
{
    GVSTUB_DSB_PIPE_ARGS         PipeArgs;              // DSB pipe args
    GVSTUB_DSB_SELECTOR          DsbSelection;          // DSB select type
    GVSTUB_DSB_TRIGGER_MODE      DsbTriggerMode;        // DSB trigger mode
    GVSTUB_DSB_SYNC_TYPE         DsbSyncType;           // DSB synchronization type
    ULONG                        DsbSyncData;           // waiting time if Sync Type is DSB_WAIT_FOR_U_SEC or Scanline Count
    GVSTUB_DSB_POLL_ARGS         DsbPollArgs;           // DSB polling args
    BOOLEAN                      IsContiguousMMIORange; // Specify whether offsets are contiguous or not
    BOOLEAN                      BackToBackDsbWrite;    // Specify whether DSB write should trigger back to back or not
    BOOLEAN                      InterruptOnCompletion; // Specify whether HW will generate interrupt on completion or not.
    PGVSTUB_DSB_OFFSET_DATA_PAIR pOffsetDataPair;       // offset data pair
    ULONG                        DataCount;             // offset data pair count
} GVSTUB_DSB_BUFFER_ARGS, *PGVSTUB_DSB_BUFFER_ARGS;

#pragma endregion Structures for DSB Update End

/**++
Structure for perform DisplayFeature Access
In this stage Data Structure is defined as [Header2 + Data]

Header2 -> GVSTUB_META_DATA
Data can be any one of GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS/GVSTUB_ENABLE_DISABLE_FEATURE_ARGS/GVSTUB_ENUM_DEVICE_ARGS etc

Meta data is used for below specific reason
the size of Input data (ie sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS) - as a example
ulServiceType as GVSTUB_DISPLAY_FEATURE_REQUEST_TYPE type.
ulStatus will specify Status of Display Feature Access Call
All Display Feature Access Error code is defined in this file.
*/
typedef struct _GVSTUB_DISPLAY_FEATURE_ARGS
{
    IN_OUT GVSTUB_META_DATA stDisplayFeatureMetaData;
    union {
        GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS stEnableDisableFramework;
        GVSTUB_ENABLE_DISABLE_FEATURE_ARGS           stEnableDisableFeature;
        GVSTUB_GET_SYSTEM_INFO_ARGS                  stSystemInfo;
        GVSTUB_ENUM_DEVICE_ARGS                      stEnumDevice;
        GVSTUB_GET_DEVICE_CONNECTIVITY_ARGS          stDeviceConnectivity;
        GVSTUB_GET_EDID_ARGS                         stEDID;
        GVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS          stDPCDInfo;
        GVSTUB_GET_SET_SIMULATE_DEVICE_ARGS          stGetSetSimulateDevice;
        GVSTUB_CREATE_RES_ARGS                       stCreateResource;
        GVSTUB_FREE_RES_ARGS                         stFreeResource;
        GVSTUB_SET_SRC_ADD_ARGS                      stSetSourceAddress;
        GVSTUB_MPO_CAPS_ARGS                         stMPOCaps;
        GVSTUB_MPO_GROUP_CAPS_ARGS                   stMPOGroupCaps;
        GVSTUB_CHECK_MPO_ARGS                        stCheckMPO;
        GVSTUB_SET_SRC_ADD_MPO_ARGS                  stSetSrcAddMPO;
        GVSTUB_PIPE_UNDER_RUN_ARGS                   stPipeUnderRunArgs;
        GVSTUB_GET_SET_VBT_ARGS                      stGetSetVBT;
        GVSTUB_DSB_BUFFER_ARGS                       stDSBBufferArgs;
        // any new Display feature service data structure should be added here.
    };
} GVSTUB_DISPLAY_FEATURE_ARGS, *PGVSTUB_DISPLAY_FEATURE_ARGS;

#pragma pack(pop, GFX_VAL_STUB_GFX_ACCESS)

#endif // GVSTUB_DISPLAY_FEATURE_H

// MPO & MMIO Related structures. Kept as place holder. will be enabled in Phase2 check-in.
//
//// ----- "GVSTUB_CREATE_RESOURCE" -----
//// Src Pixel Format.
//// There is 1:1 maping between GVSTUB_PIXELFORMAT and SB_PIXELFORMAT. Any change in SB_PIXELFORMAT should be updated here also.
// typedef enum _GVSTUB_PIXELFORMAT {
//	GVSTUB_PIXEL_FORMAT_UNINITIALIZED = 0,
//	GVSTUB_PIXEL_FORMAT_8BPP_INDEXED,        // for 8bpp
//	GVSTUB_PIXEL_FORMAT_B5G6R5X0,            // for 16bpp
//	GVSTUB_PIXEL_FORMAT_B8G8R8X8,            // for 32bpp (default)
//	GVSTUB_PIXEL_FORMAT_B8G8R8A8,
//	GVSTUB_PIXEL_FORMAT_R8G8B8X8,
//	GVSTUB_PIXEL_FORMAT_R8G8B8A8,
//	GVSTUB_PIXEL_FORMAT_R10G10B10X2,         // for 32bpp 10bpc
//	GVSTUB_PIXEL_FORMAT_R10G10B10A2,         // for 32bpp 10bpc
//	GVSTUB_PIXEL_FORMAT_B10G10R10X2,         // for 32bpp 10bpc
//	GVSTUB_PIXEL_FORMAT_B10G10R10A2,         // for 32bpp 10bpc
//	GVSTUB_PIXEL_FORMAT_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
//	GVSTUB_PIXEL_FORMAT_R16G16B16X16F,       // for 64bpp, 16bit floating
//	GVSTUB_PIXEL_FORMAT_MAX_PIXELFORMAT,
//	GVSTUB_PIXEL_FORMAT_NV12YUV420,
//	GVSTUB_PIXEL_FORMAT_YUV422,
//} GVSTUB_PIXELFORMAT;
//
//
// typedef struct _GVSTUB_CREATE_RES_ARGS  {
//	IN  GVSTUB_PIXELFORMAT             eFormat;    // Surface format
//	IN  BOOLEAN					    bAuxSurf;   // Flag to indicate req for aux surface
//	struct
//	{
//		ULONG ulTiledW : 1;
//		ULONG ulTiledX : 1;
//		ULONG ulTiledY : 1;
//		ULONG ulTiledYf : 1;
//		ULONG ulTiledYs : 1;
//		ULONG Reserved : 27;
//	} Info;
//	IN  ULONG         ulBaseWidth;   // Surface Width
//	IN  ULONG         ulBaseHeight;  // Surface Height
//	//Out parameters
//	OUT UINT64        pGmmBlock;           //To be used in the Setsource address calls
//	OUT UINT64        pUserVirtualAddress; //For the app to access the ubuffer using CPU
//	OUT UINT64        u64SurfaceSize;      //For app to copy the private framebuffer content
//	OUT ULONG         ulPitch;
//} GVSTUB_CREATE_RES_ARGS, *PGVSTUB_CREATE_RES_ARGS;
//
//
//
//
////----- GVSTUB_FREE_RESOURCE -----
// typedef struct _GVSTUB_FREE_RES_ARGS  {
//	IN  UINT64          pGmmBlock;
//} GVSTUB_FREE_RES_ARGS, *PGVSTUB_FREE_RES_ARGS;
//
//
//
//
//// ----- "GVSTUB_SET_SRC_ADDRESS" -----
// typedef struct _GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS  {
//	union
//	{
//		struct
//		{
//
//			UINT uiModeChange : 1;    // 0x00000001
//			UINT uiFlipImmediate : 1;    // 0x00000002
//			UINT uiFlipOnNextVSync : 1;    // 0x00000004
//			UINT uiFlipStereo : 1;    // 0x00000008 This is a flip from a stereo alloc. Used in addition to FlipImmediate or FlipOnNextVSync.
//			UINT uiFlipStereoTemporaryMono : 1;    // 0x00000010 This is a flip from a stereo alloc. The left image should used. Used in addition to FlipImmediate or
// FlipOnNextVSync. 			UINT uiFlipStereoPreferRight : 1;    // 0x00000010 This is a flip from a stereo alloc. The right image should used when cloning to a mono monitor.
// Used in addition to FlipImmediate or FlipOnNextVSync. 			UINT uiSharedPrimaryTransition : 1;    // 0x00000020 We are transitioning to or away from a shared managed
// primary allocation 			UINT Reserved : 25;   // 0xFFFFFFC0
//		};
//		UINT Value;
//	};
//} GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS;
//
//
// typedef struct _GVSTUB_SET_SRC_ADD_ARGS  {
//	IN  GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS stFlags;
//	IN  ULONG           ulSrcID;    // The Vidpn source ID
//	IN  UINT64          pGmmBlock;  // The Surface allocated in create resource call
//	IN  ULONG           ulDuration; // the Duarion parameter for entering 48 Hz
//} GVSTUB_SET_SRC_ADD_ARGS, *PGVSTUB_SET_SRC_ADD_ARGS;
//
//
//
//
////  ----- MPO Specific Structure/Enum Definitions -----
//
//// ------ "GVSTUB_GET_MPO_CAPS" -----
// typedef struct _GVSTUB_MPO_CAPS
//{
//	UINT uiMaxPlanes;
//	UINT uiNumCapabilityGroups;
//} GVSTUB_MPO_CAPS, *PGVSTUB_MPO_CAPS;
//
//
// typedef struct _GVSTUB_MPO_CAPS_ARGS  {
//	IN  ULONG               ulVidpnSourceID;
//	OUT GVSTUB_MPO_CAPS        stMPOCaps;
//} GVSTUB_MPO_CAPS_ARGS, *PGVSTUB_MPO_CAPS_ARGS;
//
//
//
//
//// ------ "GVSTUB_MPO_GROUP_CAPS" -----
// typedef struct _GVSTUB_MPO_GROUP_CAPS
//{
//	UINT uiMaxPlanes;
//	UINT uiMaxStretchFactorNum;
//	UINT uiMaxStretchFactorDenm;
//	UINT uiMaxShrinkFactorNum;
//	UINT uiMaxShrinkFactorDenm;
//	UINT uiOverlayFtrCaps;
//	UINT uiStereoCaps;
//} GVSTUB_MPO_GROUP_CAPS, *PGVSTUB_MPO_GROUP_CAPS;
//
//
// typedef struct _GVSTUB_MPO_GROUP_CAPS_ARGS  {
//	//Need not Escape code inside this as UMD_GENERAL_ESCAPE_BUFFER of which this structure //would be part will have it.
//	IN  ULONG               ulVidpnSourceID;
//	IN  UINT                uiGroupIndex;
//	OUT GVSTUB_MPO_GROUP_CAPS  stMPOGroupCaps;
//} GVSTUB_MPO_GROUP_CAPS_ARGS, *PGVSTUB_MPO_GROUP_CAPS_ARGS;
//
//
//
//
//// ------ "GVSTUB_CHECK_MPO" -----
// typedef struct _GVSTUB_M_RECT
//{
//	LONG    left;
//	LONG    top;
//	LONG    right;
//	LONG    bottom;
//} GVSTUB_M_RECT, *PGVSTUB_M_RECT;
//
//
// typedef enum _GVSTUB_MPO_ROTATION
//{
//	GVSTUB_MPO_ROTATION_IDENTITY = 1,
//	GVSTUB_MPO_ROTATION_90 = 2,
//	GVSTUB_MPO_ROTATION_180 = 3,
//	GVSTUB_MPO_ROTATION_270 = 4
//} GVSTUB_MPO_ROTATION;
//
//
// typedef enum _GVSTUB_MPO_PLANE_ORIENTATION
//{
//	GVSTUB_MPO_ORIENTATION_DEFAULT = 0,                      // Default value
//	GVSTUB_MPO_ORIENTATION_0 = GVSTUB_MPO_ORIENTATION_DEFAULT,  // 0 degree
//	GVSTUB_MPO_ORIENTATION_90 = 1,                           // 90 degree, supported Gen9 onwards
//	GVSTUB_MPO_ORIENTATION_180 = 2,                          // 180 degree
//	GVSTUB_MPO_ORIENTATION_270 = 3,                          // 270 degree, supported Gen9 onwards
//} GVSTUB_MPO_PLANE_ORIENTATION;
//
//
// typedef struct _GVSTUB_MPO_BLEND_VAL
//{
//	union
//	{
//		struct
//		{
//			UINT    AlphaBlend : 1;
//			UINT	Reserved : 31;
//		};
//		UINT	uiValue;
//	};
//} GVSTUB_MPO_BLEND_VAL, *PGVSTUB_MPO_BLEND_VAL;
//
//
////Not in Dx9 spec
////Matches Kernel flip attribute.
// typedef enum _GVSTUB_MPO_VIDEO_FRAME_FORMAT
//{
//	GVSTUB_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE = 0x0,
//	GVSTUB_MPO_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST = 0x1,
//	GVSTUB_MPO_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST = 0x2
//} GVSTUB_MPO_VIDEO_FRAME_FORMAT;
//
//
////Not in Dx9 Spec
////Matches Kernel flip attribute.
// typedef enum _GVSTUB_MPO_STEREO_FORMAT
//{
//	GVSTUB_MPO_FORMAT_MONO = 0,
//	GVSTUB_MPO_FORMAT_HOR = 1,
//	GVSTUB_MPO_FORMAT_VER = 2,
//	GVSTUB_MPO_FORMAT_SEPARATE = 3,
//	GVSTUB_MPO_FORMAT_ROW_INTERLEAVED = 5, //??????? 4 is missing ?????
//	GVSTUB_MPO_FORMAT_COLUMN_INTERLEAVED = 6,
//	GVSTUB_MPO_FORMAT_CHECKBOARD = 7
//} GVSTUB_MPO_STEREO_FORMAT;
//
//
////Not in Dx9 Spec
////Matches Kernel flip attribute.
// typedef enum _GVSTUB_MPO_STEREO_FLIP_MODE
//{
//	GVSTUB_MPO_FLIP_NONE = 0,
//	GVSTUB_MPO_FLIP_FRAME0 = 1,
//	GVSTUB_MPO_FLIP_FRAME1 = 2
//} GVSTUB_MPO_STEREO_FLIP_MODE;
//
//
// typedef enum _GVSTUB_MPO_STRETCH_QUALITY
//{
//	GVSTUB_MPO_STRETCH_QUALITY_BILINEAR = 0x1,      //Bilinear
//	GVSTUB_MPO_STRETCH_QUALITY_HIGH = 0x2           //Maximum
//} GVSTUB_MPO_STRETCH_QUALITY;
//
//
// typedef struct _GVSTUB_MPO_PLANE_ATTRIBUTES
//{
//	UINT                         uiMPOFlags;
//	GVSTUB_M_RECT                   stMPOSrcRect;
//	GVSTUB_M_RECT                   stMPODstRect;
//	GVSTUB_M_RECT                   stMPOClipRect;
//	GVSTUB_MPO_ROTATION             eMPORotation;
//	GVSTUB_MPO_PLANE_ORIENTATION    eHWOrientation;
//	GVSTUB_MPO_BLEND_VAL            stMPOBlend;
//	//Commenting the filters part as of now since it is not in latest Spec but it might come back, so it can be commented out for now.
//	//UINT	uiMPONumFilters;
//	//MPO_FILTER_VAL	stFilterVal[MAX_FILTERS];
//	GVSTUB_MPO_VIDEO_FRAME_FORMAT  eMPOVideoFormat;
//	UINT                        uiMPOYCbCrFlags;
//
//	//Not in Dx9 Spec
//	GVSTUB_MPO_STEREO_FORMAT       eMPOStereoFormat;
//	BOOLEAN                     bMPOLeftViewFrame0;
//	BOOLEAN                     bMPOBaseViewFrame0;
//	GVSTUB_MPO_STEREO_FLIP_MODE    eMPOStereoFlipMode;
//	GVSTUB_MPO_STRETCH_QUALITY     eStretchQuality;
//	//Currently Driver may not use this info.
//	UINT                        uiDirtyRectCount;
//	GVSTUB_M_RECT                  DIRTYRECTS[GVSTUB_MAX_DIRTY_RECTS];
//} GVSTUB_MPO_PLANE_ATTRIBUTES, *PGVSTUB_MPO_PLANE_ATTRIBUTES;
//
//
//// Surface memory type
// typedef enum _GVSTUB_SURFACE_MEMORY_TYPE
//{
//	GVSTUB_SURFACE_MEMORY_INVALID = 0,
//	GVSTUB_SURFACE_MEMORY_LINEAR = 1,                      // Surface uses linear momory
//	GVSTUB_SURFACE_MEMORY_TILED = 2,                       // Surface uses tiled memory
//	GVSTUB_SURFACE_MEMORY_X_TILED = GVSTUB_SURFACE_MEMORY_TILED,
//	GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED = 4,              // Surface uses Legacy Y tiled memory (Gen9+)
//	GVSTUB_SURFACE_MEMORY_Y_F_TILED = 8,                   // Surface uses Y F tiled memory
//} GVSTUB_SURFACE_MEMORY_TYPE;
//
//
//// Struct representing surface memory offset data
// typedef struct _GVSTUB_SURFACE_MEM_OFFSET_INFO
//{
//	IN  GVSTUB_SURFACE_MEMORY_TYPE eSurfaceMemType;
//	union
//	{
//		IN  ULONG ulLinearOffset;
//
//		struct
//		{
//			IN  ULONG ulTiledXOffset;
//			IN  ULONG ulTiledYOffset;
//			IN  ULONG ulTiledUVXOffset;   // NV12 case
//			IN  ULONG ulTiledUVYOffset;   // NV12 case
//		};
//	};
//
//	IN ULONG ulUVDistance;     // For NV12 surface
//	IN ULONG ulAuxDistance;    // Control surface Aux Offset.
//} GVSTUB_SURFACE_MEM_OFFSET_INFO, *PGVSTUB_SURFACE_MEM_OFFSET_INFO;
//
//
//// GVSTUB_PIXELFORMAT is defined in GVSTUB_CREATE_RESOURCE escape structures/enums section of header.
// typedef struct _GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO
//{
//	UINT		                   uiLayerIndex;
//	BOOLEAN		                   bEnabled;
//	GVSTUB_MPO_PLANE_ATTRIBUTES	   stPlaneAttributes;
//	GVSTUB_SURFACE_MEM_OFFSET_INFO    stSurfaceMemInfo;
//	GVSTUB_PIXELFORMAT		           eULTPixelFormat;
//	BOOLEAN		     	           bIsAsyncMMIOFlip;
//} GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO, *PGVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO;
//
//
// typedef struct _GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO
//{
//	IN  UINT    uiPlaneCount;
//	IN  GVSTUB_MPO_CHECKMPOSUPPORT_PLANE_INFO stMPOPlaneInfo[GVSTUB_MAX_PLANES];
//} GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO, *PGVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO;
//
// typedef struct _GVSTUB_CHECKMPOSUPPORT_RETURN_INFO
//{
//	union
//	{
//		struct
//		{
//			UINT    uiFailingPlane : 4; //0 based index of first plane that is //causing the CheckMPOSupport to fail.
//			UINT    TryAgain : 1; //Configuration not supported due to hw in //transition condition, this should shortly go away.
//		};
//		UINT    uiValue;
//	};
//} GVSTUB_CHECKMPOSUPPORT_RETURN_INFO, *PGVSTUB_CHECKMPOSUPPORT_RETURN_INFO;
//
// typedef struct _GVSTUB_CHECK_MPO_ARG
//{
//	IN  DWORD   dwSourceID;
//	IN  GVSTUB_MPO_CHECKMPOSUPPORT_PATH_INFO stCheckMPOPathInfo[GVSTUB_MAX_PIPES];
//	IN  ULONG   ulNumPaths;
//	IN  ULONG   ulConfig;
//
//	OUT BOOLEAN bSupported;
//	OUT ULONG   ulFailureReason;
//	OUT GVSTUB_CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo;
//} GVSTUB_CHECK_MPO_ARGS, *PGVSTUB_CHECK_MPO_ARGS;
////stMPOCheckSuppReturnInfo
//
//
//// ----- ULT Escape - "GVSTUB_SET_SRC_ADD_MPO" -----
//// GVSTUB_MPO_PLANE_ATTRIBUTES is defined in GVSTUB_CHECK_MPO escape structures/enums section of header.
// typedef struct GVSTUB_MPO_FLIP_PLANE_INFO
//{
//	UINT                           uiLayerIndex;
//	BOOLEAN                        bEnabled;
//	BOOLEAN                        bAffected;
//	UINT                           uiAllocationSegment;
//	ULONG                          AllocationAddress;
//	HANDLE                         hAllocation;
//	GVSTUB_MPO_PLANE_ATTRIBUTES	   stPlaneAttributes;
//} GVSTUB_MPO_FLIP_PLANE_INFO, *PGVSTUB_MPO_FLIP_PLANE_INFO;
//
//
//// GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS is defined in GVSTUB_SET_SRC_ADDRESS escape structures/enums section of header.
// typedef struct _GVSTUB_SET_SRC_ADD_MPO_ARGS  {
//	GVSTUB_MPO_FLIP_PLANE_INFO             stDxgkMPOPlaneArgs[GVSTUB_MAX_PLANES];
//	ULONG                               ulNumPlanes;
//	GVSTUB_SETVIDPNSOURCEADDRESS_FLAGS ulFlags;
//	DWORD                               dwSourceID;
//} GVSTUB_SET_SRC_ADD_MPO_ARGS, *PGVSTUB_SET_SRC_ADD_MPO_ARGS;
