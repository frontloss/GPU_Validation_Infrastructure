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
@file ExtInterface.h
@brief External Interface header
*/

#pragma once

#define MAX_STALL_PROCESSOR_DELAY 50

typedef struct _DD_ALLOCATE_MEM_ARGS
{
    void ** ppDestMem;
    DDU32   Size;
    BOOLEAN IsPageable;
    DDU32   Flags;
    DDU8 *  FileName;
    DDU8 *  FunctionName;
    DDU32   LineNumber;
} DD_ALLOCATE_MEM_ARGS;

typedef struct _DD_ZERO_MEM_ARGS
{
    void *pMem;
    DDU32 Size;
} DD_ZERO_MEM_ARGS;

typedef struct _DD_ALLOCATE_MEM_FROM_LIST_ARGS
{
    void *pAllocatedMem;
    void *pLookAsideList;
} DD_ALLOCATE_MEM_FROM_LIST_ARGS;

typedef struct _DD_CREATE_LOOK_ASIDE_LIST_ARGS
{
    void *  pLookAsideList;
    DDU32   Size;
    BOOLEAN Pageable;
} DD_CREATE_LOOK_ASIDE_LIST_ARGS;

typedef struct _DD_CREATE_KE_QUEUE_ELEMENT_ARGS
{
    void * pKeQueue;
    void * pListEntry;
    DDS64 *pTimeout;
} DD_CREATE_KE_QUEUE_ELEMENT_ARGS;

typedef struct _DD_CREATE_KE_QUEUE_ARGS
{
    void **pKeQueue;
    DDU32  Count;
} DD_CREATE_KE_QUEUE_ARGS;

typedef struct _DD_WAIT_FOR_SINGLE_OBJ_ARG
{
    void * pEvent;
    DDS64 *pTimeout;

} DD_WAIT_FOR_SINGLE_OBJ_ARG;

typedef void (*PFN_DD_DPC_DEFERRED_ROUTINE)(void *, void *, void *, void *);
typedef struct _DD_DPC_QUEUE_ARGS
{
    // Function & arguments to be called from within the work item
    PFN_DD_DPC_DEFERRED_ROUTINE Func;
    void **                     pDPCObject;
    void *                      pDeferredContext;
} DD_DPC_QUEUE_ARGS;

typedef struct _DD_INSERT_DPC_QUEUE_ARGS
{
    void *pDPCObject;
    void *pDPCCallbackParameter1;
    void *pDPCCallbackParameter2;
} DD_INSERT_DPC_QUEUE_ARGS;

typedef void (*PFN_DD_THREAD_START_ROUTINE)(void *);
typedef struct _DD_CREATE_SYSTEM_THREAD_ARGS
{
    PFN_DD_THREAD_START_ROUTINE pFunc;
    void *                      pStartContext;
    void *                      pThreadObject;
} DD_CREATE_SYSTEM_THREAD_ARGS;

typedef DDU32 (*PFN_DD_POWER_PLAN_NOTIFICATION_ROUTINE)(LPCGUID SettingGuid, void *Value, DDU32 ValueLength, void *Context);
typedef struct _DD_CREATE_POWER_PLAN_ARGS
{
    PFN_DD_POWER_PLAN_NOTIFICATION_ROUTINE pFunc;
    GUID                                   Guid;
    void *                                 Context;
    void **                                pHandle;
} DD_CREATE_POWER_PLAN_ARGS;

typedef enum _DD_EVENT_TYPE
{
    DD_EVENT_TYPE_NOTIFICATIONEVENT,
    DD_EVENT_TYPE_SYNCHRONIZATIONEVENT,
    DD_EVENT_TYPE_MAX
} DD_EVENT_TYPE;

typedef struct _DD_EVENT_OBJ
{
    void *        pEvent;
    DD_EVENT_TYPE EventType;
    BOOLEAN       IsSingled;
} DD_EVENT_OBJ;

typedef struct _DD_EVENT_ARG
{
    void *pEvent;
    DDU32 Priority;
} DD_EVENT_ARG;

// Timer Routine structures
typedef struct _DD_CREATE_TIMER_ARGS
{
    DD_PERIODIC_TIMER_OBJECT *pTimerObject;
    void *                    pCallbackfn;
    void *                    pContext;
    DD_TIMER_TYPE             TimerType;
} DD_CREATE_TIMER_ARGS;

typedef struct _DD_SET_TIMER_ARGS
{
    DD_PERIODIC_TIMER_OBJECT *pTimerObject;
    DD_LARGE_INTEGER          ExpireTime;
    DDU32                     Period;
    DDU32                     TolerableDelay;
} DD_SET_TIMER_ARGS;

typedef struct _DD_PCI_CFG_ACCESS_ARGS
{
    IN DDU32 BusNum;
    IN DDU32 DeviceNum;
    IN DDU32 FunctionNum;
    IN DDU32 RegNum;
    IN DDU32 Size;
    IN OUT void *pBuffer;
} DD_PCI_CFG_ACCESS_ARGS;

typedef struct _DD_MAP_NONGFX_IO_SPACE
{
    IN DD_LARGE_INTEGER PhyAddr;
    IN DDU32 Size;
    IN BOOLEAN IsCached;
    OUT DDU8 *pVirtualAddr;
} DD_MAP_NONGFX_IO_SPACE;

typedef struct _DD_UNMAP_NONGFX_IO_SPACE
{
    IN DDU8 *pVirtualAddr;
    IN DDU32 Size;
} DD_UNMAP_NONGFX_IO_SPACE;

typedef struct _DD_REGISTRY_ACCESS_ARGS
{
    void *  pRegistryPath; // Valid only if Absolute registry path is being read
    PDDWSTR pValueName;
    void *  pValueData;
    DDU32   MaxValueLength;
} DD_REGISTRY_ACCESS_ARGS;

//
// struct DD_INDICATE_CONNECTION_STATUS_ARGS: Description
//
typedef struct _DD_INDICATE_CONNECTION_STATUS_ARGS
{
    DDU8                  NumDisplays;
    DD_CONNECTION_STATUS *pDisplays;
} DD_INDICATE_CONNECTION_STATUS_ARGS;
typedef struct _DD_NOTIFY_DISPLAY_EVENT_ARGS
{
    DDU32   DisplayUID;
    BOOLEAN IsDisplayAttached;
} DD_NOTIFY_DISPLAY_EVENT_ARGS;

typedef struct _DD_SYNCHRONIZE_EXECUTION_ARGS
{
    void *   SynchronizeRoutine;
    void *   Context;
    DDU32    MessageNumber;
    BOOLEAN *ReturnValue;
} DD_SYNCHRONIZE_EXECUTION_ARGS;

// ========================================================
//  Work item related struct
// ========================================================
typedef DDU32 (*PFN_DD_GENERIC_FUNCTION)(HW_DEV_EXT *, void *);

typedef struct _DD_GENERIC_QUEUE_WORKITEM_ARGS
{
    // Function & arguments to be called from within the work item
    PFN_DD_GENERIC_FUNCTION Func;
    void *                  pArgs;
    DDU32                   ArgSize;
} DD_GENERIC_QUEUE_WORKITEM_ARGS;

typedef enum _DD_PIPE_EVENT_TYPE
{
    DD_UNDERRUN_EVENT = 0,
    DD_SCANLINE_EVENT = 1,
    DD_PIPE_EVENT_MAX,
} DD_PIPE_EVENT_TYPE;

typedef struct _DD_PIPE_EVENT_SERVICE_ARGS
{
    PIPE_ID             PipeId;
    DD_PIPE_EVENT_TYPE  EventType;
    INTERRUPT_OPERATION Operation;
} DD_PIPE_EVENT_SERVICE_ARGS_ST;

typedef struct _DD_PORT_EVENT_SERVICE_ARGS
{
    DD_PORT_TYPE           Port;
    DD_PORT_CONNECTOR_TYPE PortConnectorType;
    DD_PORT_EVENT_TYPE     EventType;
    INTERRUPT_OPERATION    Operation;
} DD_PORT_EVENT_SERVICE_ARGS_ST;

typedef enum _DD_VIRTUAL_INTR_EMULATION
{
    DD_VIRTUAL_VBI_EMULATION,
    DD_VIRTUAL_HPD_EMULATION
} DD_VIRTUAL_INTR_EMULATION;

typedef struct _DD_VIRTUAL_INTERRUPT_EMULATION_ARGS
{
    DD_VIRTUAL_INTR_EMULATION InterruptType;
    DD_PORT_TYPE              Port;
    PIPE_ID                   PipeId;
} DD_VIRTUAL_INTERRUPT_EMULATION_ARGS;

typedef enum _DD_SURFACE_USAGE
{
    DD_SURFACE_USAGE_INVALID,
    DD_SURFACE_USAGE_CURSOR,
    DD_SURFACE_USAGE_DOD_PRESENT,
    DD_SURFACE_USAGE_WIGIG,
    DD_SURFACE_USAGE_MAX
} DD_SURFACE_USAGE;

typedef struct _DD_GMM_RESOURCE_ARGS
{
    DD_IN DD_SURFACE_USAGE Usage;
    DD_IN DDU32 SurfaceWidth;
    DD_IN DDU32 SurfaceHeight;
    DD_OUT HANDLE hAllocation;
    DD_OUT DDU32 OsAddress;
    DD_OUT DDU32 HwStartAddress;
    DD_OUT HANDLE pLinearAddress;
} DD_GMM_RESOURCE_ARGS;

//----------------------------------------------------------------
// Synchronization related structs
//
// currently supporting spinlocks and mutex, assuming no recursive locking

/*
#define DECL_LOCKED_RES(type,name) \
struct _DD_LOCKED_RESOURCE##type\
{\
DD_LOCKING_OBJ_ST *__pLock;\
union{\
DDU8 Data[1];\
type __Data##__LINE__;\
} u;\
DDU32 __Size;\
DDSTATUS(*Get)(type *pData);\
DDSTATUS(*Set)(type *pData);\
} name

#define INIT_LOCKED_RES(type,name) {name.__pLock  = Alloc;  );
*/

//----------------------------------------------------------------|
//----------------------------------------------------------------|
//
//      External Interface func table
//
//----------------------------------------------------------------|
typedef struct _DD_EXTERNAL_INTERFACE
{
    /* Memory related interfaces */
    // Method to allocate memory
    void (*AllocateMem)(HW_DEV_EXT *pHwDev, DD_ALLOCATE_MEM_ARGS *pArgs);

    // Method to free memory
    void (*FreeMem)(HW_DEV_EXT *pHwDev, void *pMem);

    // Method to create look aside list
    void (*CreateLookAsideList)(HW_DEV_EXT *pHwDev, DD_CREATE_LOOK_ASIDE_LIST_ARGS *pArgs);
    // Method to delete look aside list
    void (*DeleteLookAsideList)(HW_DEV_EXT *pHwDev, void *pLookAsideList);
    // Method to allocate memory from look aside list
    void (*AllocateMemFromList)(HW_DEV_EXT *pHwDev, DD_ALLOCATE_MEM_FROM_LIST_ARGS *pArgs);
    // Method to Free memory allocated from look aside list
    void (*FreeMemToList)(HW_DEV_EXT *pHwDev, DD_ALLOCATE_MEM_FROM_LIST_ARGS *pArgs);

    DDSTATUS (*AllocateCursorBuffers)(HW_DEV_EXT *pHwDev, DD_CURSOR_INFO *pCursorInfo);
    void (*FreeCursorBuffers)(HW_DEV_EXT *pHwDev, DD_CURSOR_INFO *pCursorInfo);

    // Method to create Ke Queue
    DDSTATUS (*CreateKeQueue)(HW_DEV_EXT *pHwDev, DD_CREATE_KE_QUEUE_ARGS *pArgs);
    // Method to delete Ke Queue
    DDSTATUS (*DeleteKeQueue)(HW_DEV_EXT *pHwDev, void *pQueueObject);
    // Method to insert head element to queue
    DDSTATUS (*InsertHeadQueue)(HW_DEV_EXT *pHwDev, DD_CREATE_KE_QUEUE_ELEMENT_ARGS *pArgs);
    // Method to insert element to queue
    DDSTATUS (*InsertQueue)(HW_DEV_EXT *pHwDev, DD_CREATE_KE_QUEUE_ELEMENT_ARGS *pArgs);
    // Method to remove element to queue
    DDSTATUS (*RemoveQueue)(HW_DEV_EXT *pHwDev, DD_CREATE_KE_QUEUE_ELEMENT_ARGS *pArgs);

    // Method to create dpc
    DDSTATUS (*CreateDpc)(HW_DEV_EXT *pHwDev, DD_DPC_QUEUE_ARGS *pArgs);
    // Method to delete dpc
    DDSTATUS (*DeleteDpc)(HW_DEV_EXT *pHwDev, void *pDpcObject);
    // Method to insert into dpc
    BOOLEAN (*InsertDpc)(HW_DEV_EXT *pHwDev, DD_INSERT_DPC_QUEUE_ARGS *pArgs);

    // Method to create event
    DDSTATUS (*CreateEvent)(HW_DEV_EXT *pHwDev, DD_EVENT_OBJ *pArg);
    // Method to delete event
    DDSTATUS (*DeleteEvent)(HW_DEV_EXT *pHwDev, void *pEventObj);
    // Method to set event
    DDSTATUS (*SetEvent)(HW_DEV_EXT *pHwDev, DD_EVENT_ARG *pArg);
    // Method to wait on dispatcher object
    DDSTATUS (*WaitForSingleObject)(HW_DEV_EXT *pHwDev, DD_WAIT_FOR_SINGLE_OBJ_ARG *pArg);

    // Method to initialize the thread object
    DDSTATUS (*SystemThreadInitialize)(HW_DEV_EXT *pHwDev, DD_CREATE_SYSTEM_THREAD_ARGS *pArg);
    // Method to dereference an object
    void (*ObDereferenceObject)(HW_DEV_EXT *pHwDev, void *pObDereferenceObject);

    // Method to register power plan change notificaiton
    DDSTATUS (*RegisterPowerPlanSettings)(HW_DEV_EXT *pHwDev, DD_CREATE_POWER_PLAN_ARGS *pArg);
    // Method to un-register power plan change notificaiton
    DDSTATUS (*UnRegisterPowerPlanSettings)(HW_DEV_EXT *pHwDev, void *pObDereferenceHandle);

    // Methods for OS Timer
    DD_PERIODIC_TIMER_OBJECT *(*CreateTimer)(HW_DEV_EXT *pHwDev, DD_CREATE_TIMER_ARGS *pTimerArgs);
    DDSTATUS (*SetTimer)(HW_DEV_EXT *pHwDev, DD_SET_TIMER_ARGS *pSetTimerArgs);
    DDSTATUS (*CancelTimer)(HW_DEV_EXT *pHwDev, DD_PERIODIC_TIMER_OBJECT *pTimerObject);
    void (*DestroyTimer)(HW_DEV_EXT *pHwDev, DD_PERIODIC_TIMER_OBJECT *pTimerObject);

    // DDSTATUS(*MapPhysicalToAddress) (HW_DEV_EXT *pHwDev, DD_MAP_NONGFX_IO_SPACE *pArgs);
    void (*MapNonGfxIOSpace)(HW_DEV_EXT *pHwDev, DD_MAP_NONGFX_IO_SPACE *pArgs);

    // DDSTATUS(*UnMapPhysicalTo) (HW_DEV_EXT *pHwDev, DD_UNMAP_NONGFX_IO_SPACE *pArg);
    void (*UnMapNonGfxIOSpace)(HW_DEV_EXT *pHwDev, DD_UNMAP_NONGFX_IO_SPACE *pArg);

    /* PCI config read/write interfaces */
    // PCI Read Config
    DDSTATUS (*PCIReadCfgReg)(HW_DEV_EXT *pHwDev, DD_PCI_CFG_ACCESS_ARGS *pArgs);
    void (*CreateUnicodeString)(WCHAR *pValueName, DDU32 Size, WCHAR *pStr1, DDU32 TargetID);

    /* Registry read/write related interfaces */
    // Registry read/writes
    DDSTATUS (*ReadRegistryValue)(HW_DEV_EXT *pHwDev, DD_REGISTRY_ACCESS_ARGS *pArg);
    DDSTATUS (*ReadRegistryValueAbsolutePath)(HW_DEV_EXT *pHwDev, DD_REGISTRY_ACCESS_ARGS *pArg);
    DDSTATUS (*WriteRegistryValue)(HW_DEV_EXT *pHwDev, DD_REGISTRY_ACCESS_ARGS *pArg);

    /* Timer callbacks */
    // This function returns a DDU32 value indicating the number of 100-nanosecond units that are added to the system time each time the interval clock interrupts
    DDU32 (*QueryTimeIncrement)(HW_DEV_EXT *pHwDev);

    // This function gives the count of the interval timer interrupts that have occurred since the system was booted.
    void (*QueryTickCount)(HW_DEV_EXT *pHwDev, DD_LARGE_INTEGER *pTickCount);

    // Save and restore floating point
    DDSTATUS (*SaveFloatingPointState)(HW_DEV_EXT *pHwDev, void *pArg);
    DDSTATUS (*RestoreFloatingPointState)(HW_DEV_EXT *pHwDev, void *pArg);

    /* Delay routines */
    // This function will do a CPU busy wait loop. use this only for smaller delays such as few us to 10ms
    // For larger delays like 15ms or above, use DelayExecutionThread
    void (*TimedDelay)(HW_DEV_EXT *pHwDev, DDU32 IntervalInus); // Interval in micro seconds

    // This function Leads the current Thread to 'Wait State' so that OS can schedule some other Thread. It gets back the thread to 'Active State' after the specified time.
    DDSTATUS (*DelayExecutionThread)(HW_DEV_EXT *pHwDev, DDU32 IntervalInus); // Interval in micro seconds

    // This function gets the current time in microseconds.
    DDU64 (*QueryPerformanceCounter)(HW_DEV_EXT *pHwDev);

    /* New MMIO services to do MMIO read/writes */
    void (*ReadDDU8)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU8 *pData);
    void (*WriteDDU8)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU8 Data);
    void (*ReadDDU16)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU16 *pData);
    void (*WriteDDU16)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU16 Data);
    void (*ReadDDU32)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU32 *pData);
    void (*WriteDDU32)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU32 Data);
    void (*WriteOffset)(HW_DEV_EXT *pHwDev, DDU32 Offset, void *pData, DDU32 Size);
    void (*GetRegMem)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU32 *pData);

    // For Gen11 and beyond - direct access to interrupt registers - no need to go through standard reg access / force-wake handling
    void (*ReadDDU32Direct)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU32 *pData);
    void (*WriteDDU32Direct)(HW_DEV_EXT *pHwDev, DDU32 Offset, DDU32 Data);

    /* Misc services */
    // Function to obtain current system time
    void (*GetSystemTime)(HW_DEV_EXT *pHwDev, DD_LARGE_INTEGER *pCurrentTime);

    // IRQL related -> returns the current IRQL
    DDU8 (*GetCurrentIrql)(HW_DEV_EXT *pHwDev);

    DDSTATUS (*PanelEventNotification)(HW_DEV_EXT *pHwDev, DDU32 Event);

    //------------------------------------------
    /* Interrupt services related */
    //------------------------------------------
    // TBD: EventService/PortEventService; New interface to be defined. Removed old one as it was calling into IntVtbl->pfnEventService
    DDSTATUS (*PortEventService)(HW_DEV_EXT *pHwDev, DD_PORT_EVENT_SERVICE_ARGS_ST *pArg);
    DDSTATUS (*PipeEventService)(HW_DEV_EXT *pHwDev, DD_PIPE_EVENT_SERVICE_ARGS_ST *pArg);
    void (*AddEventHandlerToCurrentInterruptList)(HW_DEV_EXT *pHwDev, DDU32 EngClass, DDU32 BitIdx, DDU64 InstanceBit);
    void (*UpdateInterruptToEventTranslationArray)(HW_DEV_EXT *pHwDev, void *pIntrptBitArray);

    // callback to indicate child connection status
    DDSTATUS (*IndicateConnectionStatus)(HW_DEV_EXT *pHwDev, DD_NOTIFY_DISPLAY_EVENT_ARGS *pArg);

    // callback to notify OPM of the connection status
    DDSTATUS (*NotifyOPM)(HW_DEV_EXT *pHwDev, DD_NOTIFY_OPM_ARGS *pArg);

    // callback to notify GT PC of teh display changes
    DDSTATUS (*NotifyGTPC)(HW_DEV_EXT *pHwDev, DD_GT_PC_NOTIFY_EVENT_ARGS *pArg);

    //------------------------------------------
    /* Synchronization services */
    //------------------------------------------

    // Function to Synchronize execution with ISR
    DDSTATUS (*SynchronizeExecution)(HW_DEV_EXT *pHwDev, DD_SYNCHRONIZE_EXECUTION_ARGS *pArg);

    DDSTATUS (*InitializeLock)(HW_DEV_EXT *pHwDev, DD_LOCKING_OBJ_ST *pArg);
    DDSTATUS (*AcquireLock)(HW_DEV_EXT *pHwDev, DD_LOCKING_OBJ_ST *pArg);
    DDSTATUS (*ReleaseLock)(HW_DEV_EXT *pHwDev, DD_LOCKING_OBJ_ST *pArg);
    DDSTATUS (*CleanupLock)(HW_DEV_EXT *pHwDev, DD_LOCKING_OBJ_ST *pArg);
    // callback to Acquire Lock
    // DDSTATUS(*AcquireLockToSerialize) (HW_DEV_EXT *pHwDev, DD_SERIAL_LOCK_TYPE eLockType);

    // callback to Release Lock
    // DDSTATUS(*ReleaseLockToSerialize) (HW_DEV_EXT *pHwDev, DD_SERIAL_LOCK_TYPE eLockType);

    // Atomic Operations
    DDS32 (*InterLockedExchange)(HW_DEV_EXT *pHwDev, DDS32 *pDestination, DDS32 Value);
    DDS32 (*InterLockedCompareExchange)(HW_DEV_EXT *pHwDev, DDS32 *pDestination, DDS32 ReplacedValue, DDS32 CompareValue);
    BOOLEAN (*InterLockedBitTestAndSet)(HW_DEV_EXT *pHwDev, DDS32 *pBase, DDS32 Bit);
    BOOLEAN (*InterLockedBitTestAndReset)(HW_DEV_EXT *pHwDev, DDS32 *pBase, DDS32 Bit);
    DDS32 (*InterLockedOr)(HW_DEV_EXT *pHwDev, DDS32 *pDestination, DDS32 Value);
    /** return value at \c *pAdd */
    DDS32 (*InterLockedRead)(HW_DEV_EXT *pHwDev, DDS32 *pAdd);

    // SPI event object handler interface to Miniport
    DDSTATUS (*SPIEventObjectHandler)(HW_DEV_EXT *pHwDev, DD_EVENTOBJ_PARAMS *pEventObjParams);

    // Method to get surface attributes
    void (*GetSurfaceAttributes)(HW_DEV_EXT *pHwDev, DD_GET_SURF_ATTRIB_ARGS *pArgs);
    // Method to get surface position
    void (*GetSurfacePosition)(HW_DEV_EXT *pHwDev, DD_GET_SURF_POSITION_ARGS *pArgs);
    // Method to get compressionn related details from GMM
    void (*GetCompressionDetails)(HW_DEV_EXT *pHwDev, DD_GET_COMPRESSION_DEATILS_ARGS *pArgs);
    // Method to Allocate the surface
    DDSTATUS (*AllocateGMMResource)(HW_DEV_EXT *pHwDev, DD_GMM_RESOURCE_ARGS *pArgs);
    // Method to Release the surface
    DDSTATUS (*ReleaseGMMResource)(HW_DEV_EXT *pHwDev, HANDLE hAllocation);
    // Method to get OS additional target modes
    DDSTATUS (*GetOsAdditionalTargetModes)(HW_DEV_EXT *pHwDev, DD_GET_OS_ADDITIONAL_TARGET_MODE_ARG *pArg);
    // Method to Acquire EDID from OS post any overrides applied by OS
    DDSTATUS (*AcquireMonitorDescriptorFromOs)(HW_DEV_EXT *pHwDev, DD_OVERRIDE_MONITOR_DESCRIPTOR_ARG *pArg);
    // Method to release memory allocated during 'AcquireMonitorDescriptorFromOs'
    void (*ReleaseMonitorDescriptorFromOs)(HW_DEV_EXT *pHwDev, DD_OVERRIDE_MONITOR_DESCRIPTOR_ARG *pArg);
    // Callback to OS for indicating new connection states are available
    DDSTATUS (*IndicateConnectorConnectionChangeToOS)(HW_DEV_EXT *pHwDev);

    // interrupt related
    void (*NotifyVSyncToOs)(HW_DEV_EXT *pHwDev, DD_CB_VSYNC_ARG *pArgs);
    void (*NotifyPeriodicMonitoredFenceToOs)(HW_DEV_EXT *pHwDev, DD_CB_PERIODICMONITOREDFENCE_ARG *pArgs);
    DDU32 (*GetPreAllocmemSizeForNotifyVSyncToOs)(HW_DEV_EXT *pHwDev);
    // WI
    DDSTATUS (*GenericQueueWorkItem)(HW_DEV_EXT *pHwDev, DD_GENERIC_QUEUE_WORKITEM_ARGS *pArgs);

    // ACPI Callback
    DDSTATUS (*EvaluateAcpiMethod)(HW_DEV_EXT *pHwDev, DD_ACPI_EVAL_METHOD_INOUT_ARGS *pInOutArgs);

    // create Guid
    DDSTATUS (*CreateNewGUID)(HW_DEV_EXT *pHwDev, GUID *pNewGuid);

    // method to communicate with HDCP Service
    DDSTATUS (*CallHDCPService)(HW_DEV_EXT *pHwDev, DD_HDCP_SRVC_REQUEST *pArg);
    void (*ExProbeForWrite)(void *pAddress, DDU32 Size, DDU32 Alignment);

    // GPIO related
    DDSTATUS (*WriteGpioPin)(HW_DEV_EXT *pHwDev, DDU16 GPIOResourceIndex, DDU32 GpioState);

    // PC related, use din escape call to get GT PC feature related details
    DDSTATUS (*PwrConsUserPolicyEvent)(HW_DEV_EXT *pHwDev, void *pArg);

    // Virtual Interrupt
    void (*EmulateVirtualInterrupt)(HW_DEV_EXT *pHwDev, DD_VIRTUAL_INTERRUPT_EMULATION_ARGS *pArg);
    //
    // TBD: Below ones needs to be reviewed and added as and when needed

    // Function for obtaining HAS simulation information
    // DDSTATUS(*GetSimInfo) (HW_DEV_EXT *pHwDev, SIM_ENV *pSimEnv, SIM_CNTL_TABLE *pSimCntlTable);

    // Functions for dumping register list and range in OCA blob
    /*  DDSTATUS (*OCADumpRegisterList)   (HW_DEV_EXT *pHwDev,
            OCA_REG_LIST                        *pRegList,
            DDU32                               NumListRegs,
            void                                *pDebugBuf,
            DDU32                               DebugBufAvailSize,
            DDU32                               *pOutputSize);

            DDSTATUS (*OCADumpRegisterRange)  (HW_DEV_EXT *pHwDev,
            OCA_REG_RANGE                       *pRegRange,
            DDU32                               NumRegRanges,
            void                                *pDebugBuf,
            DDU32                               DebugBufAvailSize,
            DDU32                               *pOutputSize);*/

    // Function to notify display CSC activation
    /*
    DDSTATUS(*NotifyUserModeForEvent)(HW_DEV_EXT *pHwDev, DDU32 ulEvent);

    // Function to read WM/CDClock Values from PCU Mailbox.
    DDSTATUS(*ReadValueFromPCUMailbox)(HW_DEV_EXT *pHwDev, DD_PCU_MAILBOX_OPERATION *pArg);

    //ISP ISR Notification
    DDSTATUS(*NotifyISPInterrupt) (HW_DEV_EXT *pHwDev);
    DDSTATUS(*NotifyLPEAudioEvent) (HW_DEV_EXT *pHwDev, DDU32 ulEvent, DDU32 ulPipeID, void *pNotificationBuff, DDU32 ulNotificationBuffLen);
    DDSTATUS(*NotifyLPEAudioISR) (HW_DEV_EXT *pHwDev, DDU32 ulPipeID);
    DDSTATUS(*NotifyLPEAudioHdcpSessionStatus)(HW_DEV_EXT *pHwDev, DDU32 ulPipeID, DDU32 ulHDCPStat);
    DDSTATUS(*IsVGTGPUPassthrough)(HW_DEV_EXT *pHwDev);
    */

    //  DDSTATUS (*QueueWorkItem) (HW_DEV_EXT *pHwDev, SBGENERICWORKITEM_ARGS *pstGenericWorkItemArgs);

    // WiGig specific interfaces for SW P2P communication with WINIC Driver
    /*  DDSTATUS (*WiGigWNICPassThrough) (HW_DEV_EXT *pHwDev, PASSTHROUGH_DATA *pData);
        DDSTATUS (*WNICNotifyTFDTailPointerStatus) (HW_DEV_EXT *pHwDev, IGD_TFD_WRITE_TAIL_PTR_ARGS *pData);
        DDSTATUS (*WiGigNotifyTFDAllocation) (HW_DEV_EXT *pHwDev, IGD_NOTIFY_TFD_PTR_ARGS *pData);
        DDSTATUS (*WiGigAllocateChannelBandwidth) (HW_DEV_EXT *pHwDev, IGD_ALLOC_CHANNEL_BW_ARGS *pData);
        DDSTATUS (*WiGigNotifyTerminateSession) (HW_DEV_EXT *pHwDev, IGD_TERMINATE_ARGS *pData);
        DDSTATUS (*WiGigNotifyIGDStatus)(HW_DEV_EXT *pHwDev, WNIC_IGD_STATUS_ARGS *pData);
        //WiGig specific interfaces for SW P2P communication with Audio Driver
        DDSTATUS (*NotifyWiGiGPathEnable)(HW_DEV_EXT *pHwDev, GFX_AUDIO_WIGIG_MODESET_NOTIFY_ARGS *pData);
        DDSTATUS (*NotifyWiGiGReset)(HW_DEV_EXT *pHwDev, GFX_AUDIO_WIGIG_RESET_NOTIFY_ARGS *pData);
        DDSTATUS (*NotifyPowerGate)(HW_DEV_EXT *pHwDev, GFX_AUDIO_POWER_GATE_NOTIFY_ARGS *pData);
        //WiGig interfaces used for memory allocation from GMM
        DDSTATUS (*AllocateMemoryForWGBox) (HW_DEV_EXT *pHwDev, SB_WGBOX_PARAMS* pData);
        DDSTATUS (*FreeGmmAllocatedMemory)(HW_DEV_EXT *pHwDev, void *pGMMBlockDesc);*/

    /*
    DDSTATUS(*GetPixelReferenceSurfaceIndexToMOCS)(HW_DEV_EXT *pHwDev);
    DDSTATUS(*GetPinningLimit) (HW_DEV_EXT *pHwDev, DDU32 *pulPinnedMemory);

    // DFT initialization
    DDSTATUS(*GfxValStubDisplayFeatureInitialize)(HW_DEV_EXT *pHwDev);

    DDSTATUS(*ProcessSPIEvent)(HW_DEV_EXT *pHwDev, DD_SPI_DATA *pArg);

    // Method to get current power source (AC/DC)
    DDSTATUS(*GetCurrentPowerSource) (HW_DEV_EXT *pHwDev);

    DDSTATUS(*GetMaxNumTPVPipesSupported) (HW_DEV_EXT *pHwDev, DDU32 *pulMaxTPVPipes);



    //Power Conservation third-level DPST-3 interrupt managing
    DDSTATUS(*HandleThirdLevelInterrupt) (HW_DEV_EXT *pHwDev, void *pInterruptType);

    // Function to write into MCHBAR registers of Device 0.
    DDSTATUS(*WriteMCHBARDev0Reg) (HW_DEV_EXT *pHwDev, DDU32 ulOffset, DDU32 ulData);

    //To do IO Read Writes
    DDSTATUS(*ReadIOPortDDU32)(HW_DEV_EXT *pHwDev, DDU32 ulOffset);
    DDSTATUS(*WriteIOPortDDU32)(HW_DEV_EXT *pHwDev, DDU32 ulOffset, DDU32 ulData);
    */
    //  DDSTATUS (*GetTileOffsetInfo) (HW_DEV_EXT *pHwDev, SB_GET_TILE_OFFSET *pTileOffsetInfo);
    // SKU/WA interface

    //
    // Interface(s) derived from KCH
    // All KCH specific interfaces are private to GAL
    //

    //#if defined(MP_SB_ETW_LOGGING)
    // Use ETW framework for logging
    // DDSTATUS((*SendSBEventsToETWFW)(HW_DEV_EXT *pHwDev, SB_ETW_EVENTS eventType, void *pDataFromSBForETW, CHAR *pFunctionName, CHAR *pStructName, DDU32 ulSize);
    //#endif
} DD_EXTERNAL_INTERFACE;

DD_EXTERNAL_INTERFACE *GetExternalInterface();

#ifdef _DISPLAY_INTERNAL_

HW_DEV_EXT *GetHwDevExt();

// (** internal to Display **)
// allocate non-paged zeroed-out mem block
DD_INLINE void *__DD_AllocMem(DDU32 Size, DDU8 *FileName, DDU8 *FunctionName, DDU32 LineNumber)
{
    DD_ALLOCATE_MEM_ARGS   allocMemArg   = { 0 };
    DD_EXTERNAL_INTERFACE *pExtInterface = GetExternalInterface();
    void *                 pBuffer       = NULL;

    if (pExtInterface && Size > 0)
    {
        allocMemArg.Flags        = 0;
        allocMemArg.IsPageable   = FALSE;
        allocMemArg.ppDestMem    = &pBuffer;
        allocMemArg.Size         = Size;
        allocMemArg.FileName     = FileName;
        allocMemArg.FunctionName = FunctionName;
        allocMemArg.LineNumber   = LineNumber;
        pExtInterface->AllocateMem(GetHwDevExt(), &allocMemArg);
    }

    return pBuffer;
}

// (** internal to Display **)
// frees memory and clears pointer
DD_INLINE void __DD_SafeFreeMem(void **ppMem)
{
    DD_EXTERNAL_INTERFACE *pExtInterface = GetExternalInterface();

    if (ppMem && *ppMem)
    {
        if (pExtInterface)
        {
            pExtInterface->FreeMem(GetHwDevExt(), *ppMem);
            *ppMem = NULL;
        }
    }
}

//-----------------------------------------------------------------------------
//
// Mem operation related macros

// Alloc non-paged zeroed-out mem block
// Ensuring that the trace events are available only for RELEASE INTERNAL and DEBUG Drivers

#if (_DEBUG || _RELEASE_INTERNAL)
#define DD_LEAKTRACKER 1
#endif

#ifdef DD_LEAKTRACKER
#define DD_ALLOC_MEM(size) __DD_AllocMem(size, (DDU8 *)__FILE__, (DDU8 *)__FUNCTION__, __LINE__)
#else
#define DD_ALLOC_MEM(size) __DD_AllocMem(size, NULL, NULL, __LINE__)
#endif
// free mem and Nullify pointer
#define DD_SAFE_FREE(ptr) __DD_SafeFreeMem((void **)&(ptr))

/**--------------------------------------------------------------------------
 * @brief Wrapper for registry read at OSL layer
 *
 * Description:
 * @param pValueName:
 * @param *pulValue:
 * @return DDSTATUS
 * \callgraph
 *---------------------------------------------------------------------------*/
DD_INLINE DDSTATUS __DD_ReadRegistry(PDDWSTR pValueName, DDU32 *pulValue)
{
    DD_EXTERNAL_INTERFACE * pExtInt     = GetExternalInterface();
    HW_DEV_EXT *            pExtContext = GetHwDevExt();
    DDSTATUS                Status;
    DD_REGISTRY_ACCESS_ARGS RegAccessArg = { 0 };

    DDASSERT(pExtInt);
    DDASSERT(pExtContext);

    *pulValue                   = 0;
    RegAccessArg.pRegistryPath  = NULL;
    RegAccessArg.pValueData     = pulValue;
    RegAccessArg.MaxValueLength = sizeof(*pulValue);
    RegAccessArg.pValueName     = pValueName;

    Status = pExtInt->ReadRegistryValue(pExtContext, &RegAccessArg);

    return Status;

} // End of DisplayPwrConsPolicyReadRegistry()

/**--------------------------------------------------------------------------
 * @brief Wrapper for registry write at OSL layer
 *
 * Description:
 * @param pValueName:
 * @param pulValue:
 * @return DDSTATUS
 * \callgraph
 *---------------------------------------------------------------------------*/
DD_INLINE DDSTATUS __DD_WriteRegistry(PDDWSTR pValueName, DDU32 Value)
{
    DD_EXTERNAL_INTERFACE * pExtInt      = GetExternalInterface();
    HW_DEV_EXT *            pExtContext  = GetHwDevExt();
    DDSTATUS                Status       = DDS_UNSUCCESSFUL;
    DD_REGISTRY_ACCESS_ARGS RegAccessArg = { 0 };

    DDASSERT(pExtInt);
    DDASSERT(pExtContext);

    DISP_FUNC_ENTRY();

    RegAccessArg.pRegistryPath  = NULL;
    RegAccessArg.pValueData     = &Value;
    RegAccessArg.MaxValueLength = sizeof(Value);
    RegAccessArg.pValueName     = pValueName;

    Status = pExtInt->WriteRegistryValue(pExtContext, &RegAccessArg);

    DISP_FUNC_EXIT();

    return Status;

} // End of DisplayPwrConsPolicyWriteRegistry()

/**--------------------------------------------------------------------------
 * @brief Wrapper for registry read binary reg key at OSL layer
 *
 * Description:
 * @param pValueName:
 * @param *pData:
 * @param MaxBytes:
 * @return DDSTATUS
 * \callgraph
 *---------------------------------------------------------------------------*/
DD_INLINE DDSTATUS __DD_ReadBinaryRegKey(PDDWSTR pValueName, void *pData, DDU32 MaxBytes)
{
    DD_EXTERNAL_INTERFACE * pExtInt      = GetExternalInterface();
    HW_DEV_EXT *            pExtContext  = GetHwDevExt();
    DDSTATUS                Status       = DDS_UNSUCCESSFUL;
    DD_REGISTRY_ACCESS_ARGS RegAccessArg = { 0 };

    DDASSERT(pExtInt);
    DDASSERT(pExtContext);

    DISP_FUNC_ENTRY();

    RegAccessArg.pRegistryPath  = NULL;
    RegAccessArg.pValueData     = pData;
    RegAccessArg.MaxValueLength = MaxBytes;
    RegAccessArg.pValueName     = pValueName;

    Status = pExtInt->ReadRegistryValue(pExtContext, &RegAccessArg);

    DISP_FUNC_EXIT();

    return Status;

} // End of DisplayPwrConsReadBinaryRegKey()

/**--------------------------------------------------------------------------
 * @brief Wrapper for registry write binary reg key at OSL layer
 *
 * Description:
 * @param pValueName:
 * @param *pData:
 * @param MaxBytes:
 * @return DDSTATUS
 * \callgraph
 *---------------------------------------------------------------------------*/
DD_INLINE DDSTATUS __DD_BinaryRegKey(PDDWSTR pValueName, void *pData, DDU32 MaxBytes)
{
    DD_EXTERNAL_INTERFACE * pExtInt      = GetExternalInterface();
    HW_DEV_EXT *            pExtContext  = GetHwDevExt();
    DDSTATUS                Status       = DDS_UNSUCCESSFUL;
    DD_REGISTRY_ACCESS_ARGS RegAccessArg = { 0 };

    DDASSERT(pExtInt);
    DDASSERT(pExtContext);

    DISP_FUNC_ENTRY();

    RegAccessArg.pRegistryPath  = NULL;
    RegAccessArg.pValueData     = pData;
    RegAccessArg.MaxValueLength = MaxBytes;
    RegAccessArg.pValueName     = pValueName;

    Status = pExtInt->WriteRegistryValue(pExtContext, &RegAccessArg);

    DISP_FUNC_EXIT();

    return Status;
} // End of DisplayPwrConsWriteBinaryRegKey()

#endif // #ifdef _DISPLAY_INTERNAL_
