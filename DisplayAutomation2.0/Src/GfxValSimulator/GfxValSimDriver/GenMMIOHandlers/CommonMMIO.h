#ifndef __COMMONMMIO_H__
#define __COMMONMMIO_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\DriverInterfaces\PlatformInfo.h"
#include "..\\DriverInterfaces\\SIMDRV_GFX_COMMON.h"
#include "..\\DriverInterfaces\\CommonIOCTL.h"

#define GFX_MMIO_FILE_SIZE (5 * 1024 * 1024)
#define GFX_MMIO_BASE_OFFSET 0x9000
#define MAX_MMMIO_OFFSETS_HANDLED 100
#define MAX_GEN_MMIO_OFFSETS_STORED 100
#define OFFSET_INVALID 0xFFFFFFFF
#define MAX_TEST_MMIO_OFFSETS_STORED 10

typedef enum _GEN_OFFSET_INDEX
{
    eReserved1 = 0,
    eReserved2 = 1,
    eReserved3 = 2,
    eReserved4 = 3,
    eReserved5 = 4,
    eReserved6 = 5,

    eINDEX_DDI_AUX_DATA_A_START = 6,
    eINDEX_DDI_AUX_DATA_A_END   = 7,
    eINDEX_DDI_AUX_CTL_A        = 8,

    eINDEX_DDI_AUX_DATA_B_START = 9,
    eINDEX_DDI_AUX_DATA_B_END   = 10,
    eINDEX_DDI_AUX_CTL_B        = 11,

    eINDEX_DDI_AUX_DATA_C_START = 12,
    eINDEX_DDI_AUX_DATA_C_END   = 13,
    eINDEX_DDI_AUX_CTL_C        = 14,

    eINDEX_DDI_AUX_DATA_D_START = 15,
    eINDEX_DDI_AUX_DATA_D_END   = 16,
    eINDEX_DDI_AUX_CTL_D        = 17,

    eINDEX_DDI_AUX_DATA_E_START = 18,
    eINDEX_DDI_AUX_DATA_E_END   = 19,
    eINDEX_DDI_AUX_CTL_E        = 20,

    eINDEX_DDI_AUX_DATA_F_START = 21,
    eINDEX_DDI_AUX_DATA_F_END   = 22,
    eINDEX_DDI_AUX_CTL_F        = 23,

    eINDEX_DDI_AUX_DATA_G_START = 24,
    eINDEX_DDI_AUX_DATA_G_END   = 25,
    eINDEX_DDI_AUX_CTL_G        = 26,

    eINDEX_DDI_AUX_DATA_H_START = 27,
    eINDEX_DDI_AUX_DATA_H_END   = 28,
    eINDEX_DDI_AUX_CTL_H        = 29,

    eINDEX_DDI_AUX_DATA_I_START = 30,
    eINDEX_DDI_AUX_DATA_I_END   = 31,
    eINDEX_DDI_AUX_CTL_I        = 32,

    MAX_OFFSET_INDEX // THIS VALUE SHOULDN'T be More than MAX_GEN_MMIO_OFFSETS_STORED!!!

} GEN_OFFSET_INDEX;

// Read and Write Handlers could be combined into one later on!!
typedef BOOLEAN (*PFN_MMIO_READ_HANDLER)(PVOID pstMMIOHandlerInfo, ULONG pulMMIOOffset, PULONG pulReadData, PVOID peRegRWExecSite);
typedef BOOLEAN (*PFN_MMIO_WRITE_HANDLER)(PVOID pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PVOID peRegRWExecSite);

typedef BOOLEAN (*PFN_MMIO_HANDLER_INITROUTINE)(PVOID pstMMIOHandlerInfo, PVOID pvCallerNonPersistedData, ULONG ulCallerNonPersistedSize);

// Update routine can be used to update any of the Handler data dynamically whenever needed.
typedef BOOLEAN (*PFN_MMIO_HANDLER_UPDATEROUTINE)(PVOID pstMMIOHandlerInfo, PVOID pvContext);
typedef BOOLEAN (*PFN_MMIO_HANDLER_CLEANUPROUTINE)(PVOID pstMMIOHandlerInfo);

typedef BOOLEAN (*PFN_REGISTER_GMBUS_MMIO_HANDLERS)(PVOID pstMMIOInterface, PVOID pvPrivateData, PORT_TYPE ePortType);

typedef enum _MMIO_ACCESS_TYPE
{
    eMMIORead = 0,
    eMMIOWrite

} MMIO_ACCESS_TYPE,
*PMMIO_ACCESS_TYPE;

typedef struct _GLOBAL_MMIO_REGISTER_DATA
{
    ULONG  ulMMIOBaseOffset;
    PUCHAR ucMMIORegisterFile;

} GLOBAL_MMIO_REGISTER_DATA, *PGLOBAL_MMIO_REGISTER_DATA;

typedef struct _MMIO_HANDLER_INFO
{
    PVOID                     pAdapterInfo;
    DP_LIST_ENTRY             pListEntry;
    DP_LOCK                   pMMIOSpinLock;
    PORT_TYPE                 ePortType;
    MMIO_ACCESS_TYPE          eMMIOAccessType;
    GLOBAL_MMIO_REGISTER_DATA stGlobalMMORegData;
    ULONG                     ulMMIOStartOffset;
    ULONG                     ulMMIOEndOffset;
    ULONG                     ulMMIOData;
    PVOID                     pvPrivateData;         // Meant for Handler's private usage
    ULONG                     ulDwordArray[10];      // Incase you just need only a few DWORD worth of private data, use this instead of MALLOC/ExAllocate for efficiency
    PVOID                     pvCallerPersistedData; // This data is passed by the caller registering and is guarenteed to be persisted throughout the registered
                                                     // Handlers lifetime
    PVOID pvCallerNonPersistedData;                  // This is passed by the caller registering and is NOT guarenteed to be persisted. Hence the Handler should
                                                     // Should copy the data

    BOOLEAN               bReadHandlerlessRegistration;
    REGRW_EXEC_SITE       eRegReadExecSite;
    PFN_MMIO_READ_HANDLER pfnMMIOReadHandler;

    PFN_MMIO_WRITE_HANDLER pfnMMIOWriteHandler;

    PFN_MMIO_HANDLER_UPDATEROUTINE pfnMMIOUpdateRoutine;

    PFN_MMIO_HANDLER_CLEANUPROUTINE pfnMMIOCleanUpRoutine;

} MMIO_HANDLER_INFO, *PMMIO_HANDLER_INFO;

typedef struct _MMIO_HANDLER_ARRAY
{
    ULONG             ulNumRegisteredHandlers;
    MMIO_HANDLER_INFO stMMIOHandlerList[MAX_MMMIO_OFFSETS_HANDLED];

} MMIO_HANDLER_ARRAY, *PMMIO_HANDLER_ARRAY;

typedef struct _MMIO_INFO
{
    ULONG ulMMIOOffset;
    ULONG ulMMIOData;
} MMIO_INFO, *PMMIO_INFO;

typedef struct _TEST_MMIO_ARRAY
{
    ULONG     ulNumRegisters;
    MMIO_INFO stMMIOList[MAX_TEST_MMIO_OFFSETS_STORED];

} TEST_MMIO_ARRAY, *PTEST_MMIO_ARRAY;

typedef struct _MMIO_INTERFACE
{
    IGFX_PLATFORM             eIGFXPlatform;
    PCH_PRODUCT_FAMILY        ePCHProductFamily;
    SIMDRV_GFX_GMD_ID         stGfxGmdId;
    BOOLEAN                   bInterfaceInitialized;
    BOOLEAN                   bGeneralMMIOInitalized;
    MMIO_HANDLER_ARRAY        stMMIOHandlerArr;
    GLOBAL_MMIO_REGISTER_DATA stGlobalMMORegData;
    BOOLEAN                   bTestInitMMIOPresent;
    TEST_MMIO_ARRAY           stTestMMIOArray;

    // GenBased MMIO Offsets Repository;
    // Below array gets intialized in platform specific MMIO files different for each platform
    PULONG pulGenMMIOOffsetArray;

} MMIO_INTERFACE, *PMMIO_INTERFACE;

// Below function could have a init function per MMIO to set the initial state of the regs
BOOLEAN COMMONMMIOHANDLERS_RegisterMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bForceRegister, ULONG ulMMIOStartOffset, ULONG ulMMIOEndOffset,
                                                ULONG ulMMIOInitialState, PVOID pvCallerPersistedData, PVOID pvCallerNonPersistedData, ULONG ulCallerNonPersistedSize,
                                                BOOLEAN bReadHandlerlessRegistration, REGRW_EXEC_SITE eRegReadExecSite, PFN_MMIO_READ_HANDLER pfnMMIOReadHandler,
                                                PFN_MMIO_WRITE_HANDLER pfnMMIOWriteHandler, PFN_MMIO_HANDLER_INITROUTINE pfnMMIOInitRoutine,
                                                PFN_MMIO_HANDLER_UPDATEROUTINE pfnMMIOUpdateRoutine, PFN_MMIO_HANDLER_CLEANUPROUTINE pfnMMIOCleanUpRoutine);

BOOLEAN COMMONMMIOHANDLERS_RegisterPlatormBasedGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN COMMONMMIOHANDLERS_GetPortAuxRegOffsets(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PULONG pulDataStartReg, PULONG pulDataEndReg, PULONG pulControlReg);

BOOLEAN COMMONMMIOHANDLERS_RegisterPortAuxHandlers(PMMIO_INTERFACE pstMMIOInterface, PVOID pvCallerPersistedData, PORT_TYPE ePortType);
BOOLEAN COMMONMMIOHANDLERS_RegisterGMBUSHandlers(PMMIO_INTERFACE pstMMIOInterface, PVOID pvPrivateData, PORT_TYPE ePortType);

BOOLEAN COMMONMMIOHANDLERS_InitMMIOInterfaceForPlatform(PMMIO_INTERFACE pstMMIOInterface, PLATFORM_INFO stPlatformInfo);

BOOLEAN COMMONMMIOHANDLERS_UpdateMMIOInitialStateMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface, ULONG ulMMIOOffset, ULONG ulMMIOInitialState);

// This will Called via App initiated IOCTL to generate HPD
BOOLEAN COMMONMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                              PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN COMMONMMIOHANDLERS_SetupInterruptRegistersForTE(PMMIO_INTERFACE pstMMIOInterface, MIPI_DSI_PORT_TYPE ePortType);

BOOLEAN COMMONMMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN COMMONMMIOHANDLERS_InvokeUpdateRoutineForOffset(PMMIO_INTERFACE pstMMIOInterface, ULONG ulMMIOOffset, PVOID pvUpdateData);

BOOLEAN COMMONMMIOHANDLERS_CleanUp(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN COMMONMMIOHANDLERS_VerifyeDPSimulation(PVOID pvRxInfoArr, PVOID pvMMIOInterface);

BOOLEAN COMMONMMIOHANDLERS_SetupScdcInterrupt(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs);
BOOLEAN COMMONMMIOHANDLERS_SetEdpTypeCMappingInfo(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortNum);

#endif