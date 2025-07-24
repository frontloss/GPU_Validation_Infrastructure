#ifndef __SIMDRVTOGFX_H__
#define __SIMDRVTOGFX_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "SimDriver.h"
#include "SIMDRV_GFX_COMMON.h"
#include "CommonRxHandlers.h"

#define MAX_SUPPORTED_ADAPTERS 16
#define PRESI_ENV_DETECT_REG 0x180F08
#define PRESI_ENV_ENABLE_BIT 0x80000000

typedef enum _GFX_ADAPTER_SERVICE_TYPE
{
    GFX_ADAPTER_SERVICE_ADD    = 0,
    GFX_ADAPTER_SERVICE_REMOVE = 1,
    GFX_ADAPTER_SERVICE_MAX    = 2,
} GFX_ADAPTER_SERVICE_TYPE;

typedef struct _GFX_ADAPTER_CONTEXT
{
    WCHAR                  PCIBusDeviceId[MAX_PATH_STRING_LEN];
    WCHAR                  PCIBusInstanceId[MAX_PATH_STRING_LEN];
    PVOID                  pvGfxHwDev;
    LUID                   gfxAdapterLuid;
    GUID                   gfxAdapterGuid;
    BOOLEAN                isDisplayLessAdapter;
    BOOLEAN                displayOnlyDriver;
    ULONG                  devicePowerState;
    ULONG                  powerAction;
    BOOLEAN                bIsGfxReady;
    PRX_INFO_ARR           pstRxInfoArr;
    PVOID                  pStaticExpansionRomHeader;
    PVOID                  pvSimPersistenceDataS3S4;
    PVOID                  pvSimPersistenceData;
    PVOID                  pvExpansionRomHeader;
    PVOID                  pVbtbase;
    DDU32                  pVbtsize;
    DDU32                  OPRomTotalSize;
    BOOLEAN                bIsPreSi;
    GFX_EXPOSED_INTERFACES GfxExposedInterfaces;
    PVOID                  pstSimDrvGfxContext;
} GFX_ADAPTER_CONTEXT, *PGFX_ADAPTER_CONTEXT; // Adapter details for multi-adapter usecases. This information will distinguish hardware device extension belongs to which adapter

typedef enum _SIMDRV_GFX_ACCESS_REQUEST_TYPE
{
    SIMDRV_GFX_ACCESS_REQUEST_READ,
    SIMDRV_GFX_ACCESS_REQUEST_WRITE,
} SIMDRV_GFX_ACCESS_REQUEST_TYPE;

typedef struct _SIMDRV_MMIO_ACCESS_ARGS
{
    SIMDRV_GFX_ACCESS_REQUEST_TYPE accessType;
    ULONG                          offset;
    PULONG                         pValue;
} SIMDRV_MMIO_ACCESS_ARGS, *PSIMDRV_MMIO_ACCESS_ARGS;

typedef struct _VALSIM_PLATFORM_INFO
{
    ULONG  GfxPlatform;
    ULONG  GfxPchFamily;
    UINT32 GfxGmdId;
} VALSIM_PLATFORM_INFO, *PVALSIM_PLATFORM_INFO;

typedef struct _SIMDRVGFX_CONTEXT
{
    VOID *                    pvSimDrvGfxCallBackObj;  /* Simulation driver-Gfx shared callback Object */
    VOID *                    pvRegisteredCBObjHandle; /* Simulation driver-Gfx shared callback Object Handle Place holder */
    GFXVALSIM_FEATURE_CONTROL featureControl;
    INT                       gfxAdapterCount;
    GFX_ADAPTER_CONTEXT       GfxAdapterContext[MAX_SUPPORTED_ADAPTERS];

    VOID (*pfnUpdateAdapterContext)(struct _SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, GFX_ADAPTER_SERVICE_TYPE requestType, PGFX_ADAPTER_CONTEXT pGfxAdapterContext);
    PVOID (*pfnGetAdapterContext)(struct _SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, WCHAR *pPCIBusDeviceId, WCHAR *pPCIBusInstanceId);
    PVOID (*pfnGetAdapterContextEx)(struct _SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, PVOID pvGfxHwDev);

} SIMDRVGFX_CONTEXT, *PSIMDRVGFX_CONTEXT;

NTSTATUS SIMDRVTOGFX_InitSimDrvToGfxInterfaces(PSIMDRVGFX_CONTEXT *ppstSimDrvGfxContext);

BOOLEAN SIMDRVTOGFX_GenerateHPDorSPI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PORT_TYPE ePortType, BOOLEAN bHPD, BOOLEAN bAttachOrDetach, PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN SIMDRVTOGFX_GenerateTE(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, MIPI_DSI_PORT_TYPE ePortType);

NTSTATUS SIMDRVTOGFX_EnableDisableGfxSimulationMode(BOOLEAN bSetGfxSimMode);

BOOLEAN SIMDRVTOGFX_CleanUp(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext);

BOOLEAN SIMDRVTOGFX_Display_Hooks(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_Trigger_Dsb(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_Trigger_MIPI_DSI_Commands(PGFX_ADAPTER_CONTEXT pstGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_Trigger_Brightness3_Commands(PGFX_ADAPTER_CONTEXT pstGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

NTSTATUS SIMDRVTOGFX_RegDeRegCallBack(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext, BOOLEAN bRegister);

BOOLEAN SIMDRVTOGFX_MMIO_Access(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_HwMmioAccess(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, PULONG pulRegValue, SIMDRV_GFX_ACCESS_REQUEST_TYPE simRequestType);

BOOLEAN SIMDRVTOGFX_WAKE_LOCK_Access(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_GfxReadMMIOHandler(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, PULONG pulRegVal, bool* pbStateModified);

BOOLEAN SIMDRVTOGFX_GfxWriteMMIOHandler(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, ULONG ulRegVal, bool* pbStateModified);

BOOLEAN SIMDRVTOGFX_GetDriverWaTable(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG inBufferSize, PVOID pOutputBuffer, ULONG outBufferSize);

BOOLEAN SIMDRVTOGFX_GetDisplayAdapterCaps(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext, PVOID pOutputBuffer, ULONG outBufferSize);

BOOLEAN SIMDRVTOGFX_GetBuffer(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, GFXCB_EVENT_TYPE eventType, PVOID pInputBuffer, ULONG bufferSize);

BOOLEAN SIMDRVTOGFX_TriggerScdcInterrupt(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSCDC_ARGS pstScdcArgs);
#endif