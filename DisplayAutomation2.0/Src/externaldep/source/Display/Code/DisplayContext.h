/*===========================================================================
;
;   Copyright (c) Intel Corporation (2017)
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
;--------------------------------------------------------------------------*/

/**
********************************************************************
*
* @file DisplayContext.h
* @brief Private context definition and internal function declarations.
*
* Display internal code is divided in to 3 modules:
*   1. Display OS Service Layer a.k.a. DOSL/OSL/DSL
*   2. Display Protocol Layer a.k.a. DPL
*   3. Display HW Abstraction Layer a.k.a. DHL/DHAL/HAL
*
* *** All Display internal files are supposed to include this file *only* to get required interfaces and struct definitions ***
*
* The Interface access are limited to required components only via macro defines
* e.g. only OS layer can call Protocol interfaces.
* Each component does not have access to its own interface function table
*
*
*
*********************************************************************
**/
#ifndef _DISPLAY_CTXT_H_
#define _DISPLAY_CTXT_H_
#define _DIPLAY_CTXT_INC_START_

//-----------------------------------------------------------------------------
// read-only macros
//-----------------------------------------------------------------------------
#ifdef _DISPLAY_INTERNAL_
#define _MINIRW_ const
#define _DDRW_
#else // ! (_DISPLAY_)
#define _MINIRW_
#define _DDRW_ const
#endif // #ifdef _DISPLAY_

#if (defined(_DISPLAY_PROTOCOL_))
#define _DPL_RW_
#else
#define _DPL_RW_ const
#endif

#if (defined(_DISPLAY_HAL_))
#define _DHL_RW_
#else
#define _DHL_RW_ const
#endif

#define IS_GFX_FAMILY_BELOW(family1, family2) ((family1) < (family2) ? TRUE : FALSE)
#define IS_GFX_FAMILY_EQUAL_OR_ABOVE(family1, family2) ((family1) >= (family2) ? TRUE : FALSE)
#define IS_GFX_PRODUCT_EQUAL_OR_ABOVE(product1, product2) (((product1) >= (product2) ? TRUE : FALSE))
#define IS_GFX_PRODUCT_EQUAL_OR_BELOW(product1, product2) (((product1) <= (product2) ? TRUE : FALSE))

//-----------------------------------------------------------------------------
// forward declaration
//-----------------------------------------------------------------------------

typedef struct _HW_DEVICE_EXTENSION HW_DEV_EXT;

_DDRW_ typedef struct _DD_OSL_CONTEXT        DD_OSL_CONTEXT;
_DPL_RW_ typedef struct _DD_PROTOCOL_CONTEXT DD_DPL_CONTEXT;
_DHL_RW_ typedef struct _DD_DHL_CONTEXT      DD_DHL_CONTEXT;

_DHL_RW_ typedef struct _DD_DISPLAY_HAL_SERVICES   DD_DISPLAY_HAL_SERVICES;
_DPL_RW_ typedef struct _DD_DISPLAY_PROTO_SERVICES DD_DISPLAY_PROTO_SERVICES;
typedef struct _DD_EXTERNAL_INTERFACE              DD_EXTERNAL_INTERFACE;

//-----------------------------------------------------------------------------
// Interface Header inc
//-----------------------------------------------------------------------------
#include "DisplayArgsInternal.h"
#ifdef _DISPLAY_INTERNAL_
#include "DisplayProtocol/DisplayProtocolInterface.h"
#include "DisplayHAL/DisplayHALInterface.h"
#include "DisplayExtInterface.h"
#endif
#include <sku_wa.h>
#include <igfxfmid.h>

///////////////////////////////////////////////////////////////////////////////
//
// CONSTANTs / ENUMs
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//
// structs / unions
//
///////////////////////////////////////////////////////////////////////////////

typedef struct UNDERRUN_ISR_CONFIG_REC
{
    DDU32 UnderrunLevel;
    DDU32 UnderrunCounter[MAX_PHYSICAL_PIPES];
} UNDERRUN_ISR_CONFIG;

typedef enum UNDERRUN_ISR_ENABLE_REC
{
    UNDERRUN_DISABLED = 0,      /* Interrupt disabled*/
    UNDERRUN_ENABLE_FLIPS_ONLY, /* Enable Under-run ISR only for Flips */
    UNDERRUN_SETMODE_AND_FLIPS, /* Enable Under-run ISR during modeset and flips */
    UNDERRUN_START_2_END,       /* Enable Under-run ISR begning from CCD_Startmodeset and flips */
} UNDERRUN_ISR_ENABLE;

_DDRW_ typedef struct _DD_DISPLAY_DATA
{
    BOOLEAN             IsSystemInTdr;
    UNDERRUN_ISR_CONFIG UnderRunISRConfig;
} DD_DISPLAY_DATA;

typedef struct _DD_PCI_DATA
{
    // Device 2 - IGD
    DDU32 PCIVendorID;
    DDU32 PCIDeviceID;
    DDU32 PCISubsystemVenderID;
    DDU32 PCISubSystemID;
    DDU32 PCIRevisionID;
    DDU32 PCISlotNumber;
    DDU32 PCIBusNumber;

    DDU32 DisplayCoreFamily; // Interpreted from device ID
    DDU32 RenderCoreFamily;
    DDU32 PchCoreFamily; // uses PCH_PRODUCT_FAMILY
    DDU32 ProductFamily;

    BOOLEAN IsIntelPrimary;
} DD_PCI_DATA;

typedef struct _DD_PLATFORM_MEMORY_DETAILS
{
    DDU32 CoreFreq;         // GFX/GMCH core frequency in MHz
    DDU32 SystemMemFreq;    // System memory frequency in MHz
    DDU32 NumOfMemChannels; // Number of memory channels
    DDU32 MaxCDDotClock;    // Maximum Pipe A dotclock supported
    DDU32 PlatformType;
} DD_PLATFORM_MEMORY_DETAILS;

typedef struct _DD_PLATFORM_PARAMETERS
{
    DD_PCI_DATA                PciData;
    DD_PLATFORM_MEMORY_DETAILS PlatformMemoryDetails;

    // SKU data
    SKU_FEATURE_TABLE *pSkuTable;

    // WA data - accessible only to GAL
    WA_TABLE *pWaTable;
} DD_PLATFORM_PARAMETERS;

typedef struct _DISPLAY_CONTEXT
{
    HW_DEV_EXT *pHwDevExt; // cached pointer

    // private data context
    DD_OSL_CONTEXT *pOSLContext;
    DD_DPL_CONTEXT *pDPLContext;
    DD_DHL_CONTEXT *pDHLContext;

    // public interfaces
    DD_DISPLAY_PROTO_SERVICES *pDPLServices;
    DD_DISPLAY_HAL_SERVICES *  pDHLServices;

    DD_EXTERNAL_INTERFACE *pExtInterface;

    DD_PLATFORM_PARAMETERS PlatformParams;

    // Display Global Data context
    DD_DISPLAY_DATA DisplayData;
} DISPLAY_CONTEXT;

///////////////////////////////////////////////////////////////////////////////
//
// MACRO routines / function declaration / inline functions
//
///////////////////////////////////////////////////////////////////////////////

#ifdef _DISPLAY_

DD_PLATFORM_PARAMETERS *GetPlatformParams();
DD_DISPLAY_DATA *       GetDisplayData();
DD_OSL_CONTEXT *        GetOSLContext();
DD_DPL_CONTEXT *        GetProtocolContext();
DD_DHL_CONTEXT *        GetHALContext();
SKU_FEATURE_TABLE *     GetSKUTable();

#if (defined(_DISPLAY_OSL_))
DD_DISPLAY_PROTO_SERVICES *GetProtocolInterface();
#endif

#if (defined(_DISPLAY_OSL_) || defined(_DISPLAY_PROTOCOL_))
DD_DISPLAY_HAL_SERVICES *GetHALInterface();
#endif

#if (defined(_DISPLAY_HAL))
WA_TABLE *              GetWATable();
DD_PLATFORM_PARAMETERS *GetPlatformParameters();
#endif

#endif // #ifdef _DISPLAY_

//-----------------------------------------------------------------------------
//
// Public methods
//
//-----------------------------------------------------------------------------

DDSTATUS DisplayHALInitialize(DISPLAY_CONTEXT *pDisplayContext);
DDSTATUS DisplayHALCleanup(DISPLAY_CONTEXT *pDisplayContext);
void     DisplayHALDumpDiagInfo(DISPLAY_CONTEXT *pDisplayContext);

DDSTATUS DisplayProtocolInitialize(DISPLAY_CONTEXT *pDisplayContext);
DDSTATUS DisplayProtocolCleanup(DISPLAY_CONTEXT *pDisplayContext);
void     DisplayProtocolDumpDiagInfo(DISPLAY_CONTEXT *pDisplayContext);

DDSTATUS ExtInterfaceInitialize(HW_DEV_EXT *pHwDev, DISPLAY_CONTEXT *pDisplayContext);
void     ExtInterfaceCleanup(HW_DEV_EXT *pHwDev, DISPLAY_CONTEXT *pDisplayContext);

DDSTATUS DisplayPwrConsInitialize(DISPLAY_CONTEXT *pDisplayContext);
DDSTATUS DisplayPcDestroy(DISPLAY_CONTEXT *pDisplayContext);
void     DisplayPwrConsInitFlagsCleanUp(HW_DEV_EXT *pHwDev);
// Forward declarations
typedef struct _CCD_CONTEXT CCD_CONTEXT;

DDSTATUS CcdStart(DISPLAY_CONTEXT *pDisplayContext, DD_OSL_INIT_ARG *pOslInitArg);
void     CcdStop(DISPLAY_CONTEXT *pDisplayContext);
void     CcdDumpDiagData(CCD_CONTEXT *pCcdContext);
void     CcdGetMaxOverlayPlanes(DISPLAY_CONTEXT *pDisplayContext, DDU32 *pNumOverlayPlanes);
DDSTATUS CcdGetMpoCaps(DISPLAY_CONTEXT *pDisplayContext, DD_GET_MPO_CAPS_ARG *pArg);
DDSTATUS CcdCheckMpo(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_CHECK_MPO *pArg);
DDSTATUS CcdFlip(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_FLIP_MPO *pArg);
#ifdef CS_ASYNC_FLIPS_ENABLED
DDSTATUS CcdNotifyCsFlip(DISPLAY_CONTEXT *pDisplayContext, DD_NOTIFY_FLIP_ARGS *pArg);
#endif
void     CcdReportFlipDone(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_RFD *pArg);
DDSTATUS CcdSetTiming(DISPLAY_CONTEXT *pDisplayContext, DD_SET_TIMING_ARG *pArg);
DDSTATUS CcdRecommendMonitorModes(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_RMM *pArg);
DDSTATUS CcdEnumVidPnCofuncModality(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_EVCM *pArg);
DDSTATUS CcdIsSupportedVidPn(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_ISV *pArg);
DDSTATUS CcdQueryChildRelations(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_QCR *pArg);
DDSTATUS CcdQueryChildStatus(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_QCS *pArg);
DDSTATUS CcdQueryConnectionChange(DISPLAY_CONTEXT *pDisplayContext, DD_QUERY_CONNECTION_CHANGE *pArg);
DDSTATUS CcdDisplayDetectControl(DISPLAY_CONTEXT *pDisplayContext, DD_DISPLAY_DETECT_CONTROL_ARGS *pArg);
DDSTATUS CcdI2CTransmitOrRecieveData(DISPLAY_CONTEXT *pDisplayContext, DD_I2C_ARGS *I2CTxArgs);
DDSTATUS CcdQueryDeviceDescriptor(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_QDD *pArg);
DDSTATUS CcdCreateTopology(DISPLAY_CONTEXT *pDisplayContext, DD_TOPOLOGY **ppTopology);
void     CcdReleaseTopology(DISPLAY_CONTEXT *pDisplayContext, DD_TOPOLOGY **ppTopology);
DDSTATUS CcdSetPointerPosition(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_SPP *pArg);
DDSTATUS CcdSetPointerShape(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_SPS *pArg);
void     CcdGetPreAllocatedMemoryForMpoPlanes(DISPLAY_CONTEXT *pDisplayContext, void **ppMem);
DDSTATUS CcdPostDisplayOwnerShip(DISPLAY_CONTEXT *pDisplayContext, DD_POST_DISPLAY_INFO *pArg);
void     CcdSetSourceVisibility(DISPLAY_CONTEXT *pDisplayContext, DD_SRC_VISIBILITY *pArg);
DDSTATUS CcdCheckSeamlessRrChangeSupport(DISPLAY_CONTEXT *pDisplayContext, DD_CHECK_SEAMLESS_RR_CHANGE_SUPPORT_ARG *pArg);
void     CcdConfigureUnderRunInterrupt(UNDERRUN_ISR_ENABLE stage, PIPE_ID pipeIndex, BOOLEAN enable);
DDU64    CcdGetConnectionChangeId(DISPLAY_CONTEXT *pDisplayContext);
DDSTATUS CcdQueryIntegratedDispColorimetry(DISPLAY_CONTEXT *pDisplayContext, DD_ARG_QIDC *pQidcArg);
void     CcdControlVsyncInterrupt(DISPLAY_CONTEXT *pDisplayContext, DD_CTRL_VSYNC_INTERRUPT_ARG *pArg);
DDSTATUS CcdGetpossibleTiledAlloc(DISPLAY_CONTEXT *pDisplayContext, DD_GET_POSSIBLE_TILING_ARGS *pArg);
BOOLEAN  CcdGetVidpnDetails(CCD_CONTEXT *pCcdContext, DD_GET_VIDPN_DETAILS *pVidpnQuery);
DDSTATUS CcdGetFirmwareTopology(DISPLAY_CONTEXT *pDisplayContext, DD_PREOS_TOPOLOGY_DATA *pPreOsTopologyData);
DDSTATUS CcdCreatePeriodicFrameNotification(DD_OSL_CONTEXT *pOSLContext, DD_PERIODIC_FRAME_CREATE_ARGS *pArg);
// to be called from DisplayDdi.c and from local function within CCD, hence keeping OSLContext as input
void     CcdDestroyPeriodicFrameNotification(DD_OSL_CONTEXT *pOSLContext, DD_PERIODIC_FRAME_ELEM *pPeriodicFrameElem);
DDSTATUS CcdGetPowerConsData(DISPLAY_CONTEXT *pDisplayContext, DD_PC_FEATURES *pPwrConsData);

// Escape related interfaces
DDSTATUS DDEscape(DISPLAY_CONTEXT *pDisplayContext, DD_ESCAPE *pEscape);

// Acpi related Interfaces
DDSTATUS AcpiServicesNotifyAcpiEvent(DISPLAY_CONTEXT *pDisplayContext, DD_NOTIFY_ACPI_EVENT_ARGS *pAcpiEventArgs);
DDSTATUS AcpiServicesGetBrightnessLevels(DISPLAY_CONTEXT *pDisplayContext, DD_GET_ACPI_BCL_LEVELS *pGetAcpiBlcLevels);

DDSTATUS CcdGetorSetHDCPProtectionLevel(DISPLAY_CONTEXT *pDisplayContext, DD_GETSETPARAM_ARGS *I2CTxArgs);
DDSTATUS CcdHDCPTransmitOrRecieveData(DISPLAY_CONTEXT *pDisplayContext, DD_HDCP_MSG_ARGS *pMsgArgs);
DDSTATUS CcdSetHDCPAuthStatus(DISPLAY_CONTEXT *pDisplayContext, DD_HDCP_AUTH_STATUS_ARGS *pAuthStatusArgs);

DDSTATUS DisplayPcBlcClientEventHandler(DISPLAY_CONTEXT *pDisplayContext, DD_BLC_DDI_PARAMS *pBlcDdiParams);
void     DisplayPcBlcSetSmoothBrightnessState(DISPLAY_CONTEXT *pDisplayContext, BOOLEAN Set);
BOOLEAN  DisplayPcBlcSetAggressivenessLevel(DISPLAY_CONTEXT *pDisplayContext, DDU8 AggrLevel);
DDSTATUS DisplayPcBlcGetBacklightReduction(DISPLAY_CONTEXT *pDisplayContext, DD_BACKLIGHT_INFO *pBacklightInfo);

DDSTATUS DisplayOSLInitialize(DISPLAY_CONTEXT *pDispContext, DD_OSL_INIT_ARG *pOslInitArg);
DDSTATUS DisplayOslCleanup(DISPLAY_CONTEXT *pDispContext);
void     DisplayOslDumpDiagData(DISPLAY_CONTEXT *pDispContext);
DDSTATUS DisplayOslSetPowerState(DD_OSL_CONTEXT *pOslContext, DD_SET_ADAPTER_PWR_ARGS *pArg);
DDSTATUS DisplayOslTdrHandler(DD_OSL_CONTEXT *pOslContext, DD_TDR_ARGS *pArg);
DDSTATUS DisplayOslGetPlatformInfo(DD_OSL_CONTEXT *pOslContext, DD_PLATFORM_INFO *pArg);
void     DisplayOSLInterruptServices(DISPLAY_CONTEXT *pDispContext, DD_INTERRUPT_ARGS *pArg);
void     DisplayOSLGetInterruptSource(DISPLAY_CONTEXT *pDispContext, DD_INTERRUPT_ARGS *pArg);
void     DisplayOSLGetEnabledInterrupts(DISPLAY_CONTEXT *pDispContext, DD_INTERRUPT_ARGS *pArg);

// Color interfaces
DDSTATUS DisplayColorManagerGetSet1DLUT(DD_OSL_CONTEXT *pDispContext, DD_COLOR_1DLUT_CONFIG_ARGS *pParams);
DDSTATUS DisplayColorManagerSetTargetColorMatrix(DD_OSL_CONTEXT *pDispContext, DD_COLOR_MATRIX_CONFIG *pTargetRelativeColorMatrix);
void     DisplayColorManagerOverrideColorInfo(DD_OSL_CONTEXT *pOSLContext, DD_COLOR_PIXEL_DESC *pOutputColorInfo, DDU32 TargetId);

// DOD related interfaces
DDSTATUS CcdGetActiveTopology(DISPLAY_CONTEXT *pDisplayContext, DD_ACTIVE_TOPOLOGY *pTopology);
DDSTATUS CcdPresentDisplayOnly(DISPLAY_CONTEXT *pDisplayContext, DD_PRESENT_DISPLAY_ONLY *pArg);

#undef _DIPLAY_CTXT_INC_START_
#endif // _DISPLAY_CTXT_H_
