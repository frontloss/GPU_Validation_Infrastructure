#include <stdbool.h>

#ifndef __SIMDRV_GFX_COMMON__
#define __SIMDRV_GFX_COMMON__

//#include "..\\GenMMIOHandlers\\CommonMMIO.h"

//{A9CD4D20-CCB8-414F-B035-827A042E0687}
DEFINE_GUID(SIMDRV_INTERFACE_GUID, 0xa9cd4d20, 0xccb8, 0x414f, 0xb0, 0x35, 0x82, 0x7a, 0x4, 0x2e, 0x6, 0x87);

// Gfx simulation registry path
#define SIMDRV_REG_PATH L"\\Registry\\Machine\\System\\CurrentControlSet\\Services\\GfxValSimDriver"

// Gfx simulation registry key name
#define SIMDRV_REG_KEYNAME L"GfxValSimEnabled"

// Below Macro should be save as MAX_DP_PORT in DPIOCTL.h
#define SIMDRVGFX_MAX_DP_PORTS 6

#define SIMDRV_GFX_SHARED_OBJ_NAME \
    L"\\CallBack\\SIMDRV_GFX_SharedCBObj" // Shared object used by both the drivers for registering with CallBack Object OR Notifying on CallBack Object while establishing Driver
                                          // to Driver
#define SIMDRV_GFX_OBJ_ATTRIB (OBJ_CASE_INSENSITIVE | OBJ_PERMANENT | OBJ_KERNEL_HANDLE)
#define GFX_SIMDRV_INTERFACE_VERSION 0x1     // Version 1
#define GFX_SIMDRV_MINCOMPATIBLE_VERSION 0x1 // Version 1

// Error codes used by Gfx and SimDrv driver to indicate the operation success/failure..
#define SIMDRVGFX_STATUS_SUCCESS 0x00000000            // Set if any requested operation is successfull..
#define SIMDRVGFX_ERROR_VERSION_MISMATCH 0x00000001    // Set if versions are not mismatching beyond minimum support backward compatibility..
#define SIMDRVGFX_ERROR_NO_MEMORY 0x00000002           // Set if the failure of Interface call is due to memory allocation failures.
#define SIMDRVGFX_ERROR_NO_BANDWIDTH 0x00000004        // Set if failure in allocating requested bandwidth during mode set etc.
#define SIMDRVGFX_ERROR_INVALID_REQUEST 0x00000008     // Set if there is any wrong input parameters while calling the other module interface..
#define SIMDRVGFX_ERROR_INTERFACE_NOT_READY 0x00000010 // Set if a call is happening to module which has already notified of not ready to receive any calls..

//
typedef enum _REGRW_EXEC_SITE
{
    eNoExecHw    = 0,
    eExecHW      = 1,
    eReadCombine = 2,

} REGRW_EXEC_SITE,
*PREGRW_EXEC_SITE;

//*****************************************************************
// Structures used as Parameters for both SimDrv and GFX Call Backs
//*****************************************************************

// Enum indicating reason why either GFX or SimDrv driver is READY or NOTREADY
// Can be used by both GFX and SIMDRV Drivers to indicate the status.
typedef enum _SIMDRV_GFX_READY_REASON
{
    SIMDRV_GFX_READY_UNDEFINED = 0,
    SIMDRV_GFX_NOT_READY_DRV_UNLOAD,
    SIMDRV_GFX_NOT_READY_PM_ENTRY,
    SIMDRV_GFX_NOT_READY_INIT_FAILURE, // Could be due to reasons like Version mismatch beyond backward compatibility, any allocation failure etc..
    SIMDRV_GFX_READY_DRV_LOADED,
    SIMDRV_GFX_READY_PM_RESUME,
} SIMDRV_GFX_READY_REASON,
*PSIMDRV_GFX_READY_REASON;

typedef enum _SIMDRV_GFX_READINESS
{
    SIMDRV_GFX_READINESS_UNDEFINED      = 0,
    SIMDRV_GFX_READY                    = 1,
    SIMDRV_GFX_NOT_READY_INTERFACE_KILL = 2,
    SIMDRV_GFX_NOT_READY_INTERFACE_UP   = 3
} SIMDRV_GFX_READINESS,
*PSIMDRV_GFX_READINESS;

//****************************************************************
// Structures used as Parameters for SimDrv Call Backs..
//****************************************************************

typedef enum _SIMDRV_SP_INT_ID
{
    eDPortA_SIMDRV_SPI = 1,
    eDPortB_SIMDRV_SPI = 2,
    eDPortC_SIMDRV_SPI = 3,
    eDPortD_SIMDRV_SPI = 4,
    eDPortE_SIMDRV_SPI = 5,
    eDPortF_SIMDRV_SPI = 6,
    eWiGigPort_SIMDRV_SPI,
    eUndefined_SIMDRV_SPI
} SIMDRV_SP_INT_ID;

typedef struct _SIMDRV_SPI_EVENT_DATA
{
    unsigned long  ulPort;
    unsigned long  ulHandleEvent; // Uses the ENUM SPI_EVENT_TYPE
    unsigned char  ucValidDisplayUidCount;
    unsigned char  ucReserved1;
    unsigned short usReserved2;
    unsigned long  ulDisplayUidList[3]; // Display for which event is generated

} SIMDRV_SPI_EVENT_DATA, *PSIMDRV_SPI_EVENT_DATA;

typedef struct _SIMDRV_SPI_ALLEVENTS_DATA
{
    SIMDRV_SPI_EVENT_DATA stSPIEventData[SIMDRVGFX_MAX_DP_PORTS * 2]; // This is even to add even for HDMI related ports..
    unsigned long         ulNumEventsDetected;                        // Num Events actually Detected based on SPI..
    unsigned long         ulMaxNumEvents;                             // Maximum Events that can be actually detected. Should be initialized to SIMDRVGFX_MAX_DP_PORTS
} SIMDRV_SPI_ALLEVENTS_DATA, *PSIMDRV_SPI_ALLEVENTS_DATA;

// Reason for Gfx Sim driver notification
typedef enum _GFXCB_EVENT_TYPE
{
    EventInvalid      = -1,
    GenerateInterrupt = 1,
    DisplayHooks      = 2,
    TriggerDSB        = 3,
    ReadPCIConfig     = 4,
    ReadOPROM         = 5,
    MMIOAccess        = 6,
    MipiDsiCommand       = 7,
    Brightness3Command = 8,
    GetDriverWaTable   = 9,
    GetDiagnosticsData = 10,
    WakeLock           = 11,
} GFXCB_EVENT_TYPE,
*PGFXCB_EVENT_TYPE;

typedef struct _SIMDRV_INTERRUPT_ARGS
{
    BOOLEAN (*pfnRoutineToSynchronize)(PVOID);
    PVOID pvRoutineArgs;

} SIMDRV_INTERRUPT_ARGS, *PSIMDRV_INTERRUPT_ARGS;

typedef struct _SIMDRV_GFX_STATUS_ARGS
{
    SIMDRV_GFX_READINESS eSimDrvOrGfxReady; // GFX OR SimDrv Driver status.. Based on direction of call, it is an indication to say GFX is Ready or SimDrv Driver is Ready.TRUE is
                                            // Ready and FALSE is Not Ready..
    SIMDRV_GFX_READY_REASON eReadyReason;   // Reason for GFX\SimDrv being Ready or Not Ready.. Comes from SIMDRV_GFX_READY_REASON.

} SIMDRV_GFX_STATUS_ARGS, *PSIMDRV_GFX_STATUS_ARGS;

typedef struct _SIMDRV_READ_PCI_CONFIG
{
    unsigned int   ulSize;
    unsigned int   ulOffset;
    unsigned char *pBuffer;
} SIMDRV_READ_PCI_CONFIG;

typedef struct _GFXCALLBACK_ARGS
{
    unsigned long          ulStatus; // Interface handler to fill in the error status of success\failure properly.
    GFXCB_EVENT_TYPE       eGfxCbEvent;
    SIMDRV_INTERRUPT_ARGS  stSimDrvIntArgs;
    PVOID                  stSimDrvDisplayArgs; // DISPLAY DFT Hooks args
    SIMDRV_READ_PCI_CONFIG stSimReadPCIConfigArgs;
    ULONG                  ulOpregionPhyBase;
} GFXCALLBACK_ARGS, *PGFXCALLBACK_ARGS;

typedef struct _SIMDRV_CB_POWER_STATE_ARGS
{
    DEVICE_POWER_STATE DevicePowerState;
    POWER_ACTION       ActionType;
} SIMDRV_CB_POWER_STATE_ARGS, *PSIMDRV_CB_POWER_STATE_ARGS;

typedef struct _SIMDRV_CB_MMIO_ARGS
{
    unsigned long  ulRegOffset;
    unsigned long *pulRegVal;
    bool           bStateModified;
} SIMDRV_CB_MMIO_ARGS, *PSIMDRV_CB_MMIO_ARGS;

typedef struct _SIMDRV_CB_OPROM_ARGS
{
    UCHAR *        pBuffer;
    unsigned long  ulOffset;
    unsigned long  ulSize;
    unsigned long *pulBytesRead;
} SIMDRV_CB_OPROM_ARGS, *PSIMDRV_CB_OPROM_ARGS;

//For MIPI DSI Feature
typedef struct _SIMDRV_CB_MIPI_ARGS
{
    unsigned long ulMipiEventType; // MipiDsiCaps = 1, MipiDsiTransmission = 2, MipiDsiReset = 3,
    unsigned long  ulTargetId;
    PVOID pArgs;
} SIMDRV_CB_MIPI_ARGS, *PSIMDRV_CB_MIPI_ARGS;

typedef enum _SIMDRV_CB_REQUEST_TYPE
{
    SIMDRV_CB_INVALID_REQUEST,
    SIMDRV_CB_REQUEST_GFX_POWER_STATE,
    SIMDRV_CB_REQUEST_GFX_STATE,
    SIMDRV_CB_REQUEST_GFX_READ_MMIO,
    SIMDRV_CB_REQUEST_GFX_WRITE_MMIO,
    SIMDRV_CB_REQUEST_READ_OP_ROM,
} SIMDRV_CB_REQUEST_TYPE;

typedef struct _SIMDRV_CB_GENERIC_HANDLER_ARGS
{
    SIMDRV_CB_REQUEST_TYPE SimDrvCbRequestType;
    union {
        struct
        {
            SIMDRV_CB_MMIO_ARGS        SimDrvCbMmioArgs;
            SIMDRV_CB_POWER_STATE_ARGS SimDrvCbPowerStateArgs;
            SIMDRV_CB_OPROM_ARGS       SimDrvCbOpRomArgs;
            SIMDRV_GFX_STATUS_ARGS     SimDrvCbGfxStatusArgs;
        };
    };
} SIMDRV_CB_GENERIC_HANDLER_ARGS, *PSIMDRV_CB_GENERIC_HANDLER_ARGS;

/////////////////////////////////////////////////////////
// GFX Exposed CallBack Interface definitions..
/////////////////////////////////////////////////////////

typedef BOOLEAN (*PFN_GFXCB_GENERIC_HANDLER)(void *pGfxHwDev, PGFXCALLBACK_ARGS pGfxCallbackArgs);

typedef BOOLEAN (*PFN_GFXCB_GET_PLATFORMINFO)(void *pGfxHwDev, void *pPlatformInfo);

//////////////////////////////////////////////////////////////
// Simulation driver exposed callBack interface definitions..
//////////////////////////////////////////////////////////////

typedef BOOLEAN (*PFN_NOTIFY_SIMDRV_STATUS)(void *pGfxHwDev);
typedef NTSTATUS (*PFN_SIMDRVCB_GENERIC_HANDLER)(void *pvSimDrvContext, void *pGfxHwDev, SIMDRV_CB_GENERIC_HANDLER_ARGS *pSimDrvCbGenericHandlerArgs);

#pragma pack(1)

typedef struct _GFX_EXPOSED_INTERFACES
{

    // Callback function called by Simualation driver to notify its Load/Unload (Ready) status to graphics driver
    PFN_NOTIFY_SIMDRV_STATUS pfnSimDrvCb_SimDrvtaStusNotification;

    // Callback function called by Simulation Driver into Gfx for various functionalities such as generating HPD etc.
    PFN_GFXCB_GENERIC_HANDLER pfnGfxCb_GenericHandler;

    // Callback function called by Simulation Driver into Gfx to get Platform information
    PFN_GFXCB_GET_PLATFORMINFO pfnGfxCb_GetPlatformInfo;

} GFX_EXPOSED_INTERFACES, *PGFX_EXPOSED_INTERFACES;

// This structure should be common between SimDRV and GFX. It would contain data and functions ptrs to functions implemented in
// SimDrv to call into SimDrv and function ptrs to functions implemented in Gfx to call into Gfx.
// No need for two different structures for SimDrv and Gfx to achieve the above
typedef struct _SIMDRVGFX_INTERFACE_DATA
{
    unsigned long ulSize; // Size of Allocation.
    PKEVENT       pEventSimDrvDone;
    unsigned long ulSimDrvInterfaceVersion; // Simulation Driver Interface Version. Actual running version for Data structure\Interface access will be based on which Interface
                                            // version is lower to maintain backward compatibility. If versions are too backward beyond the minimum compatible version defined
                                            // below, then connection setup would be a failure.
    unsigned long ulMinCompatibleVersion;   // Minimum Version to which the current version of Driver is Backward Compatible to..

    void *                       pvSimDrvToGfxContext;
    PFN_SIMDRVCB_GENERIC_HANDLER pfnSimDrvCb_GenericHandler;
    GFX_EXPOSED_INTERFACES       stGfxExposedInterfaces;

    // Graphics driver's hardware context. Filled by Gfx driver during KMIF setup and later on passed to Gfx driver during calls
    void *          pvGfxHwDev;
    DEVICE_OBJECT*  pGfxPhysicalDeviceObject; // Graphics driver's device object will be use for querying display adapter details
    BOOLEAN         isDisplayLessAdapter;
    BOOLEAN         displayOnlyDriver;
    LUID            gfxAdapterLuid;
    GUID            gfxAdapterGuid;
} SIMDRVGFX_INTERFACE_DATA, *PSIMDRVGFX_INTERFACE_DATA;

#pragma pack()

#endif // ! __SIMDRV_GFX_COMMON__
