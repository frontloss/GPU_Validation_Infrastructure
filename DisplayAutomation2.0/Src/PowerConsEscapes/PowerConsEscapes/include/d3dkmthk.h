/******************************Module*Header**********************************\
*
* Module Name: d3dkmthk.h
*
* Content: longhorn display driver model kernel mode thunk interfaces
*
* Copyright (c) 2003 Microsoft Corporation.  All rights reserved.
\*****************************************************************************/
#ifndef _D3DKMTHK_H_
#define _D3DKMTHK_H_

#pragma warning(disable : 4214)

#include <d3dukmdt.h>

typedef struct _D3DKMT_CREATEDEVICEFLAGS
{
    UINT LegacyMode : 1; // 0x00000001
    UINT Reserved : 31;  // 0xFFFFFFFE
} D3DKMT_CREATEDEVICEFLAGS;

typedef struct _D3DKMT_CREATEDEVICE
{
    union {
        D3DKMT_HANDLE hAdapter; // in: identifies the adapter for user-mode creation
        VOID *        pAdapter; // in: identifies the adapter for kernel-mode creation
    };

    D3DKMT_CREATEDEVICEFLAGS Flags;

    D3DKMT_HANDLE             hDevice;               // out: Indentifies the device
    VOID *                    pCommandBuffer;        // out: D3D10 compatibility.
    UINT                      CommandBufferSize;     // out: D3D10 compatibility.
    D3DDDI_ALLOCATIONLIST *   pAllocationList;       // out: D3D10 compatibility.
    UINT                      AllocationListSize;    // out: D3D10 compatibility.
    D3DDDI_PATCHLOCATIONLIST *pPatchLocationList;    // out: D3D10 compatibility.
    UINT                      PatchLocationListSize; // out: D3D10 compatibility.
} D3DKMT_CREATEDEVICE;

typedef struct _D3DKMT_DESTROYDEVICE
{
    D3DKMT_HANDLE hDevice; // in: Indentifies the device
} D3DKMT_DESTROYDEVICE;

typedef enum _D3DKMT_CLIENTHINT
{
    D3DKMT_CLIENTHINT_UNKNOWN = 0,
    D3DKMT_CLIENTHINT_OPENGL  = 1,
    D3DKMT_CLIENTHINT_CDD     = 2, // Internal   ;internal
    D3DKMT_CLIENTHINT_DX7     = 7,
    D3DKMT_CLIENTHINT_DX8     = 8,
    D3DKMT_CLIENTHINT_DX9     = 9,
    D3DKMT_CLIENTHINT_DX10    = 10,
} D3DKMT_CLIENTHINT;

typedef struct _D3DKMT_CREATECONTEXT
{
    D3DKMT_HANDLE             hDevice;               // in:  Handle to the device owning this context.
    UINT                      NodeOrdinal;           // in:  Identifier for the node targetted by this context.
    UINT                      EngineAffinity;        // in:  Engine affinity within the specified node.
    D3DDDI_CREATECONTEXTFLAGS Flags;                 // in:  Context creation flags.
    VOID *                    pPrivateDriverData;    // in:  Private driver data
    UINT                      PrivateDriverDataSize; // in:  Size of private driver data
    D3DKMT_CLIENTHINT         ClientHint;            // in:  Hints which client is creating this
    D3DKMT_HANDLE             hContext;              // out: Handle of the created context.
    VOID *                    pCommandBuffer;        // out: Pointer to the first command buffer.
    UINT                      CommandBufferSize;     // out: Command buffer size (bytes).
    D3DDDI_ALLOCATIONLIST *   pAllocationList;       // out: Pointer to the first allocation list.
    UINT                      AllocationListSize;    // out: Allocation list size (elements).
    D3DDDI_PATCHLOCATIONLIST *pPatchLocationList;    // out: Pointer to the first patch location list.
    UINT                      PatchLocationListSize; // out: Patch location list size (elements).
} D3DKMT_CREATECONTEXT;

typedef struct _D3DKMT_DESTROYCONTEXT
{
    D3DKMT_HANDLE hContext; // in:  Identifies the context being destroyed.
} D3DKMT_DESTROYCONTEXT;

typedef struct _D3DKMT_CREATESYNCHRONIZATIONOBJECT
{
    D3DKMT_HANDLE                    hDevice;     // in:  Handle to the device.
    D3DDDI_SYNCHRONIZATIONOBJECTINFO Info;        // in:  Attributes of the synchronization object.
    D3DKMT_HANDLE                    hSyncObject; // out: Handle to the synchronization object created.
} D3DKMT_CREATESYNCHRONIZATIONOBJECT;

typedef struct _D3DKMT_DESTROYSYNCHRONIZATIONOBJECT
{
    D3DKMT_HANDLE hSyncObject; // in:  Identifies the synchronization objects being destroyed.
} D3DKMT_DESTROYSYNCHRONIZATIONOBJECT;

typedef struct _D3DKMT_WAITFORSYNCHRONIZATIONOBJECT
{
    D3DKMT_HANDLE hContext;                                       // in: Identifies the context that needs to wait.
    UINT          ObjectCount;                                    // in: Specifies the number of object to wait on.
    D3DKMT_HANDLE ObjectHandleArray[D3DDDI_MAX_OBJECT_WAITED_ON]; // in: Specifies the object to wait on.
} D3DKMT_WAITFORSYNCHRONIZATIONOBJECT;

typedef struct _D3DKMT_SIGNALSYNCHRONIZATIONOBJECT
{
    D3DKMT_HANDLE        hContext;                                      // in: Identifies the context that needs to signal.
    UINT                 ObjectCount;                                   // in: Specifies the number of object to signal.
    D3DKMT_HANDLE        ObjectHandleArray[D3DDDI_MAX_OBJECT_SIGNALED]; // in: Specifies the object to be signaled.
    D3DDDICB_SIGNALFLAGS Flags;                                         // in: Specifies signal behavior.
} D3DKMT_SIGNALSYNCHRONIZATIONOBJECT;

typedef struct _D3DKMT_LOCK
{
    D3DKMT_HANDLE hDevice;     // in: identifies the device
    D3DKMT_HANDLE hAllocation; // in: allocation to lock
                               // out: New handle representing the allocation after the lock.
    UINT  PrivateDriverData;   // in: Used by UMD for AcquireAperture
    UINT  NumPages;
    CONST UINT *       pPages;
    VOID *             pData; // out: pointer to memory
    D3DDDICB_LOCKFLAGS Flags; // in: Bit field defined by D3DDDI_LOCKFLAGS
} D3DKMT_LOCK;

typedef struct _D3DKMT_UNLOCK
{
    D3DKMT_HANDLE hDevice;              // in: Identifies the device
    UINT          NumAllocations;       // in: Number of allocations in the array
    CONST D3DKMT_HANDLE *phAllocations; // in: array of allocations to unlock
} D3DKMT_UNLOCK;

typedef struct _D3DKMDT_DISPLAYMODE_FLAGS
{
    UINT ValidatedAgainstMonitorCaps : 1;
    UINT Reserved : 31;
} D3DKMDT_DISPLAYMODE_FLAGS;

typedef struct _D3DKMT_DISPLAYMODE
{
    UINT                                  Width;
    UINT                                  Height;
    D3DDDIFORMAT                          Format;
    D3DDDI_RATIONAL                       RefreshRate;
    D3DDDI_VIDEO_SIGNAL_SCANLINE_ORDERING ScanLineOrdering;
    D3DDDI_ROTATION                       DisplayOrientation;
    UINT                                  DisplayFixedOutput;
    D3DKMDT_DISPLAYMODE_FLAGS             Flags;
} D3DKMT_DISPLAYMODE;

typedef struct _D3DKMT_GETDISPLAYMODELIST
{
    D3DKMT_HANDLE                  hAdapter;      // in: adapter handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: adapter's VidPN source ID
    D3DKMT_DISPLAYMODE *           pModeList;     // out:
    UINT                           ModeCount;     // in/out:
} D3DKMT_GETDISPLAYMODELIST;

typedef struct _D3DKMT_SETDISPLAYMODE
{
    D3DKMT_HANDLE                         hDevice;            // in: Identifies the device
    D3DKMT_HANDLE                         hPrimaryAllocation; // in:
    D3DDDI_VIDEO_SIGNAL_SCANLINE_ORDERING ScanLineOrdering;   // in:
    D3DDDI_ROTATION                       DisplayOrientation; // in:
} D3DKMT_SETDISPLAYMODE;

typedef struct _D3DKMT_MULTISAMPLEMETHOD
{
    UINT NumSamples;
    UINT NumQualityLevels;
    UINT Reserved; // workaround for NTRAID#Longhorn-1124385-2005/03/14-kanqiu
} D3DKMT_MULTISAMPLEMETHOD;

typedef struct _D3DKMT_GETMULTISAMPLEMETHODLIST
{
    D3DKMT_HANDLE                  hAdapter;      // in: adapter handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: adapter's VidPN source ID
    UINT                           Width;         // in:
    UINT                           Height;        // in:
    D3DDDIFORMAT                   Format;        // in:
    D3DKMT_MULTISAMPLEMETHOD *     pMethodList;   // out:
    UINT                           MethodCount;   // in/out:
} D3DKMT_GETMULTISAMPLEMETHODLIST;

typedef struct _D3DKMT_PRESENTFLAGS
{
    union {
        struct
        {
            UINT Blt : 1;                 // 0x00000001
            UINT ColorFill : 1;           // 0x00000002
            UINT Flip : 1;                // 0x00000004
            UINT FlipDoNotFlip : 1;       // 0x00000008
            UINT FlipDoNotWait : 1;       // 0x00000010
            UINT FlipRestart : 1;         // 0x00000020
            UINT DstRectValid : 1;        // 0x00000040
            UINT SrcRectValid : 1;        // 0x00000080
            UINT RestrictVidPnSource : 1; // 0x00000100
            UINT SrcColorKey : 1;         // 0x00000200
            UINT DstColorKey : 1;         // 0x00000400
            UINT LinearToSrgb : 1;        // 0x00000800
            UINT PresentCountValid : 1;   // 0x00001000
            UINT Rotate : 1;              // 0x00002000
            UINT Reserved : 18;           // 0xFFFFC000
        };
        UINT Value;
    };
} D3DKMT_PRESENTFLAGS;

typedef struct _D3DKMT_PRESENT
{
    union {
        D3DKMT_HANDLE hDevice;  // in: D3D10 compatibility.
        D3DKMT_HANDLE hContext; // in: Indentifies the context
    };
    HWND                           hWindow;       // in: window to present to
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: VidPn source ID if RestrictVidPnSource is flagged
    D3DKMT_HANDLE                  hSource;       // in: Source allocation to present from
    D3DKMT_HANDLE                  hDestination;  // in: Destination allocation whenever non-zero
    UINT                           Color;         // in: color value in ARGB 32 bit format
    RECT                           DstRect;       // in: unclipped dest rect
    RECT                           SrcRect;       // in: unclipped src rect
    UINT                           SubRectCnt;    // in: count of sub rects
    CONST RECT *             pSrcSubRects;        // in: sub rects in source space
    UINT                     PresentCount;        // in: present counter
    D3DDDI_FLIPINTERVAL_TYPE FlipInterval;        // in: flip interval
    D3DKMT_PRESENTFLAGS      Flags;               // in:
} D3DKMT_PRESENT;

typedef struct _D3DKMT_RENDERFLAGS
{
    UINT ResizeCommandBuffer : 1;     // 0x00000001
    UINT ResizeAllocationList : 1;    // 0x00000002
    UINT ResizePatchLocationList : 1; // 0x00000004
    UINT PresentRedirected : 1;       // 0x00000008
    UINT Reserved : 28;               // 0xFFFFFFF0
} D3DKMT_RENDERFLAGS;

typedef struct _D3DKMT_RENDER
{
    union {
        D3DKMT_HANDLE hDevice;  // in: D3D10 compatibility.
        D3DKMT_HANDLE hContext; // in: Indentifies the context
    };
    UINT  CommandOffset;                                          // in: offset in bytes from start
    UINT  CommandLength;                                          // in: number of bytes
    UINT  AllocationCount;                                        // in: Number of allocations in allocation list.
    UINT  PatchLocationCount;                                     // in: Number of patch locations in patch allocation list.
    VOID *pNewCommandBuffer;                                      // out: Pointer to the next command buffer to use.
    UINT  NewCommandBufferSize;                                   // in: Size requested for the next command buffer.
                                                                  // out: Size of the next command buffer to use.
    D3DDDI_ALLOCATIONLIST *pNewAllocationList;                    // out: Pointer to the next allocation list to use.
    UINT                   NewAllocationListSize;                 // in: Size requested for the next allocation list.
                                                                  // out: Size of the new allocation list.
    D3DDDI_PATCHLOCATIONLIST *pNewPatchLocationList;              // out: Pointer to the next patch location list.
    UINT                      NewPatchLocationListSize;           // in: Size requested for the next patch location list.
                                                                  // out: Size of the new patch location list.
    D3DKMT_RENDERFLAGS Flags;                                     // in:
    ULONGLONG          PresentHistoryToken;                       // in: Present history token for redirected present calls
    ULONG              BroadcastContextCount;                     // in: Specifies the number of context
                                                                  //     to broadcast this command buffer to.
    D3DKMT_HANDLE BroadcastContext[D3DDDI_MAX_BROADCAST_CONTEXT]; // in: Specifies the handle of the context to
                                                                  //     broadcast to.
} D3DKMT_RENDER;

typedef struct _D3DKMT_CREATEALLOCATIONFLAGS
{
    UINT CreateResource : 1; // 0x00000001
    UINT CreateShared : 1;   // 0x00000002
    UINT NonSecure : 1;      // 0x00000004
    UINT Reserved : 29;      // 0xFFFFFFF8
} D3DKMT_CREATEALLOCATIONFLAGS;

typedef struct _D3DKMT_CREATEALLOCATION
{
    D3DKMT_HANDLE hDevice;
    D3DKMT_HANDLE hResource;    // in/out:valid only within device
    D3DKMT_HANDLE hGlobalShare; // out:Shared handle if CreateShared
    CONST VOID *pPrivateRuntimeData;
    UINT        PrivateRuntimeDataSize;
    CONST VOID *                 pPrivateDriverData;
    UINT                         PrivateDriverDataSize;
    UINT                         NumAllocations;
    D3DDDI_ALLOCATIONINFO *      pAllocationInfo;
    D3DKMT_CREATEALLOCATIONFLAGS Flags;
} D3DKMT_CREATEALLOCATION;

typedef struct _D3DKMT_OPENRESOURCE
{
    D3DKMT_HANDLE              hDevice;                       // in : Indentifies the device
    D3DKMT_HANDLE              hGlobalShare;                  // in : Shared resource handle
    UINT                       NumAllocations;                // in : Number of allocations associated with the resource
    D3DDDI_OPENALLOCATIONINFO *pOpenAllocationInfo;           // in : Arrary of open allocation structs
    VOID *                     pPrivateRuntimeData;           // in : Caller supplied buffer where the runtime private data associated with this resource will be copied
    UINT                       PrivateRuntimeDataSize;        // in : Size in bytes of the pPrivateRuntimeData buffer
    VOID *                     pResourcePrivateDriverData;    // in : Caller supplied buffer where the driver private data associated with the resource will be copied
    UINT                       ResourcePrivateDriverDataSize; // in : Size in bytes of the pResourcePrivateDriverData buffer
    VOID *                     pTotalPrivateDriverDataBuffer; // in : Caller supplied buffer where the Driver private data will be stored
    UINT          TotalPrivateDriverDataBufferSize; // in/out : Size in bytes of pTotalPrivateDriverDataBuffer / Size in bytes of data written to pTotalPrivateDriverDataBuffer
    D3DKMT_HANDLE hResource;                        // out : Handle for this resource in this process
} D3DKMT_OPENRESOURCE;

typedef struct _D3DKMT_QUERYRESOURCEINFO
{
    D3DKMT_HANDLE hDevice;             // in : Indentifies the device
    D3DKMT_HANDLE hGlobalShare;        // in : Global resource handle to open
    VOID *        pPrivateRuntimeData; // in : Ptr to buffer that will receive runtime private data for the resource
    UINT PrivateRuntimeDataSize; // in/out : Size in bytes of buffer passed in for runtime private data / If pPrivateRuntimeData was NULL then size in bytes of buffer required for
                                 // the runtime private data otherwise size in bytes of runtime private data copied into the buffer
    UINT TotalPrivateDriverDataSize;    // out : Size in bytes of buffer required to hold all the DriverPrivate data for all of the allocations associated withe the resource
    UINT ResourcePrivateDriverDataSize; // out : Size in bytes of the driver's resource private data
    UINT NumAllocations;                // out : Number of allocations associated with this resource
} D3DKMT_QUERYRESOURCEINFO;

typedef struct _D3DKMT_DESTROYALLOCATION
{
    D3DKMT_HANDLE hDevice; // in: Indentifies the device
    D3DKMT_HANDLE hResource;
    CONST D3DKMT_HANDLE *phAllocationList; // in: pointer to an array allocation handles to destroy
    UINT                 AllocationCount;  // in: Number of allocations in phAllocationList
} D3DKMT_DESTROYALLOCATION;

#define D3DKMT_ALLOCATIONPRIORITY_DISCARD 0x28000000
#define D3DKMT_ALLOCATIONPRIORITY_LOW 0x50000000
#define D3DKMT_ALLOCATIONPRIORITY_NORMAL 0x78000000
#define D3DKMT_ALLOCATIONPRIORITY_HIGH 0xa0000000
#define D3DKMT_ALLOCATIONPRIORITY_MAXIMUM 0xc8000000

typedef struct _D3DKMT_SETALLOCATIONPRIORITY
{
    D3DKMT_HANDLE hDevice;                 // in: Indentifies the device
    D3DKMT_HANDLE hResource;               // in: Specify the resource to set priority to.
    CONST D3DKMT_HANDLE *phAllocationList; // in: pointer to an array allocation to set priority to.
    UINT                 AllocationCount;  // in: Number of allocations in phAllocationList
    CONST UINT *pPriorities;               // in: New priority for each of the allocation in the array.
} D3DKMT_SETALLOCATIONPRIORITY;

typedef enum _D3DKMT_ALLOCATIONRESIDENCYSTATUS
{
    D3DKMT_ALLOCATIONRESIDENCYSTATUS_RESIDENTINGPUMEMORY    = 1,
    D3DKMT_ALLOCATIONRESIDENCYSTATUS_RESIDENTINSHAREDMEMORY = 2,
    D3DKMT_ALLOCATIONRESIDENCYSTATUS_NOTRESIDENT            = 3,
} D3DKMT_ALLOCATIONRESIDENCYSTATUS;

typedef struct _D3DKMT_QUERYALLOCATIONRESIDENCY
{
    D3DKMT_HANDLE hDevice;                              // in: Indentifies the device
    D3DKMT_HANDLE hResource;                            // in: pointer to resource owning the list of allocation.
    CONST D3DKMT_HANDLE *             phAllocationList; // in: pointer to an array allocation to get residency status.
    UINT                              AllocationCount;  // in: Number of allocations in phAllocationList
    D3DKMT_ALLOCATIONRESIDENCYSTATUS *pResidencyStatus; // out: Residency status of each allocation in the array.
} D3DKMT_QUERYALLOCATIONRESIDENCY;

typedef struct _D3DKMT_GETRUNTIMEDATA
{
    D3DKMT_HANDLE hAdapter;
    D3DKMT_HANDLE hGlobalShare;    // in: shared handle
    VOID *        pRuntimeData;    // out: in: for a version?
    UINT          RuntimeDataSize; // in:
} D3DKMT_GETRUNTIMEDATA;

typedef enum _KMTUMDVERSION
{
    KMTUMDVERSION_DX9 = 0,
    KMTUMDVERSION_DX10,
    KMTUMDVERSION_DX11,
} KMTUMDVERSION;

typedef struct _D3DKMT_UMDFILENAMEINFO
{
    KMTUMDVERSION Version;               // In: UMD version
    WCHAR         UmdFileName[MAX_PATH]; // Out: UMD file name
} D3DKMT_UMDFILENAMEINFO;

typedef struct _D3DKMT_OPENGLINFO
{
    WCHAR UmdOpenGlIcdFileName[MAX_PATH];
    ULONG Version;
    ULONG Flags;
} D3DKMT_OPENGLINFO;

typedef struct _D3DKMT_SEGMENTSIZEINFO
{
    ULONGLONG MemorySegmentSize;
    ULONGLONG ApertureSegmentSize;
} D3DKMT_SEGMENTSIZEINFO;

typedef struct _D3DKMT_FLIPINFOFLAGS
{
    UINT FlipInterval : 1; // 0x00000001 // Set when kmd driver support FlipInterval natively
    UINT Reserved : 31;    // 0xFFFFFFFE
} D3DKMT_FLIPINFOFLAGS;

typedef struct _D3DKMT_FLIPQUEUEINFO
{
    UINT                 MaxHardwareFlipQueueLength; // Max flip can be queued for hardware flip queue.
    UINT                 MaxSoftwareFlipQueueLength; // Max flip can be queued for software flip queue for non-legacy device.
    D3DKMT_FLIPINFOFLAGS FlipFlags;
} D3DKMT_FLIPQUEUEINFO;

typedef enum _KMTQUERYADAPTERINFOTYPE
{
    KMTQAITYPE_UMDRIVERPRIVATE = 0,
    KMTQAITYPE_UMDRIVERNAME    = 1,
    KMTQAITYPE_UMOPENGLINFO    = 2,
    KMTQAITYPE_GETSEGMENTSIZE  = 3,
    KMTQAITYPE_ADAPTERGUID     = 4,
    KMTQAITYPE_FLIPQUEUEINFO   = 5,
} KMTQUERYADAPTERINFOTYPE;

typedef struct _D3DKMT_QUERYADAPTERINFO
{
    D3DKMT_HANDLE           hAdapter;
    KMTQUERYADAPTERINFOTYPE Type;
    VOID *                  pPrivateDriverData;
    UINT                    PrivateDriverDataSize;
} D3DKMT_QUERYADAPTERINFO;

typedef struct _D3DKMT_OPENADAPTERFROMHDC
{
    HDC                            hDc;           // in:  DC that maps to a single display
    D3DKMT_HANDLE                  hAdapter;      // out: adapter handle
    LUID                           AdapterLuid;   // out: adapter LUID
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // out: VidPN source ID for that particular display
} D3DKMT_OPENADAPTERFROMHDC;

typedef struct _D3DKMT_OPENADAPTERFROMDEVICENAME
{
    WCHAR                          DeviceName[32]; // in:  Name of GDI device from which to open an adapter instance
    D3DKMT_HANDLE                  hAdapter;       // out: adapter handle
    LUID                           AdapterLuid;    // out: adapter LUID
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId;  // out: VidPN source ID for that particular display
} D3DKMT_OPENADAPTERFROMDEVICENAME;

typedef struct _D3DKMT_CLOSEADAPTER
{
    D3DKMT_HANDLE hAdapter; // in: adapter handle
} D3DKMT_CLOSEADAPTER;

typedef struct _D3DKMT_GETSHAREDPRIMARYHANDLE
{
    D3DKMT_HANDLE                  hAdapter;       // in: adapter handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId;  // in: adapter's VidPN source ID
    D3DKMT_HANDLE                  hSharedPrimary; // out: global shared primary handle (if one exists currently)
} D3DKMT_GETSHAREDPRIMARYHANDLE;

typedef enum _D3DKMT_ESCAPETYPE
{
    D3DKMT_ESCAPE_DRIVERPRIVATE = 0,
    D3DKMT_ESCAPE_VIDMM         = 1,
    D3DKMT_ESCAPE_TDRDBGCTRL    = 2,
    D3DKMT_ESCAPE_VIDSCH        = 3,
} D3DKMT_ESCAPETYPE;

typedef enum _D3DKMT_TDRDBGCTRLTYPE
{
    D3DKMT_TDRDBGCTRLTYPE_FORCETDR     = 0, // Simulate a TDR
    D3DKMT_TDRDBGCTRLTYPE_DISABLEBREAK = 1, // Disable DebugBreak on timeout
    D3DKMT_TDRDBGCTRLTYPE_ENABLEBREAK  = 2, // Enable DebugBreak on timeout
} D3DKMT_TDRDBGCTRLTYPE;

typedef enum _D3DKMT_VIDMMESCAPETYPE
{
    D3DKMT_VIDMMESCAPETYPE_SETFAULT           = 0,
    D3DKMT_VIDMMESCAPETYPE_RUN_COHERENCY_TEST = 1
} D3DKMT_VIDMMESCAPETYPE;

typedef enum _D3DKMT_VIDSCHESCAPETYPE
{
    D3DKMT_VIDSCHESCAPETYPE_PREEMPTIONCONTROL = 0, // Enable/Disable preemption
} D3DKMT_VIDSCHESCAPETYPE;

typedef struct _D3DKMT_VIDMM_ESCAPE
{
    D3DKMT_VIDMMESCAPETYPE Type;
    union {
        struct
        {
            union {
                struct
                {
                    ULONG ProbeAndLock : 1;
                    ULONG SplitPoint : 1;
                    ULONG HotAddMemory : 1;
                    ULONG SwizzlingAperture : 1;
                    ULONG PagingPathLockSubRange : 1;
                    ULONG PagingPathLockMinRange : 1;
                    ULONG ComplexLock : 1;
                    ULONG FailVARotation : 1;
                    ULONG NoWriteCombined : 1;
                    ULONG NoPrePatching : 1;
                    ULONG AlwaysRepatch : 1;
                    ULONG ExpectPreparationFailure : 1;
                    ULONG Reserved : 20;
                };
                ULONG Value;
            };
        } SetFault;
    };
} D3DKMT_VIDMM_ESCAPE;

typedef struct _D3DKMT_VIDSCH_ESCAPE
{
    D3DKMT_VIDSCHESCAPETYPE Type;
    union {
        BOOL PreemptionControl; // enable/disable preemption
    };
} D3DKMT_VIDSCH_ESCAPE;

typedef struct _D3DKMT_ESCAPE
{
    D3DKMT_HANDLE      hAdapter;              // in: adapter handle
    D3DKMT_HANDLE      hDevice;               // in: device handle [Optional]
    D3DKMT_ESCAPETYPE  Type;                  // in: escape type.
    D3DDDI_ESCAPEFLAGS Flags;                 // in: flags
    VOID *             pPrivateDriverData;    // in/out: escape data
    UINT               PrivateDriverDataSize; // in: size of escape data
    D3DKMT_HANDLE      hContext;              // in: context handle [Optional]
} D3DKMT_ESCAPE;

typedef enum _D3DKMT_VIDPNSOURCEOWNER_TYPE
{
    D3DKMT_VIDPNSOURCEOWNER_UNOWNED      = 0, // Has no owner or GDI is the owner   ;internal
    D3DKMT_VIDPNSOURCEOWNER_SHARED       = 1, // Has shared owner, that is owner can yield to any exclusive owner, not available to legacy devices
    D3DKMT_VIDPNSOURCEOWNER_EXCLUSIVE    = 2, // Has exclusive owner without shared gdi primary,
    D3DKMT_VIDPNSOURCEOWNER_EXCLUSIVEGDI = 3, // Has exclusive owner with shared gdi primary and must be exclusive owner of all VidPn sources, only available to legacy devices
} D3DKMT_VIDPNSOURCEOWNER_TYPE;

typedef struct _D3DKMT_SETVIDPNSOURCEOWNER
{
    D3DKMT_HANDLE hDevice;                                  // in: Device handle
    CONST D3DKMT_VIDPNSOURCEOWNER_TYPE *pType;              // in: OwnerType array
    CONST D3DDDI_VIDEO_PRESENT_SOURCE_ID *pVidPnSourceId;   // in: VidPn source ID array
    UINT                                  VidPnSourceCount; // in: Number of valid entries in above array
} D3DKMT_SETVIDPNSOURCEOWNER;

#define D3DKMT_GETPRESENTHISTORY_MAXTOKENS 64

typedef struct _D3DKMT_GETPRESENTHISTORY
{
    D3DKMT_HANDLE hAdapter;                 // in:  Adapter handle
    ULONGLONG *   pPresentHistory;          // out: buffer for completed present tokens
    UINT          PresentHistoryTokenCount; // in/out: max/returned number of present tokens
} D3DKMT_GETPRESENTHISTORY;

typedef struct _D3DKMT_CREATEOVERLAY
{
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in
    D3DKMT_HANDLE                  hDevice;       // in: Indentifies the device
    D3DDDI_KERNELOVERLAYINFO       OverlayInfo;   // in
    D3DKMT_HANDLE                  hOverlay;      // out: Kernel overlay handle
} D3DKMT_CREATEOVERLAY;

typedef struct _D3DKMT_UPDATEOVERLAY
{
    D3DKMT_HANDLE            hDevice;     // in: Indentifies the device
    D3DKMT_HANDLE            hOverlay;    // in: Kernel overlay handle
    D3DDDI_KERNELOVERLAYINFO OverlayInfo; // in
} D3DKMT_UPDATEOVERLAY;

typedef struct _D3DKMT_FLIPOVERLAY
{
    D3DKMT_HANDLE hDevice;               // in: Indentifies the device
    D3DKMT_HANDLE hOverlay;              // in: Kernel overlay handle
    D3DKMT_HANDLE hSource;               // in: Allocation currently displayed
    VOID *        pPrivateDriverData;    // in: Private driver data
    UINT          PrivateDriverDataSize; // in: Size of private driver data
} D3DKMT_FLIPOVERLAY;

typedef struct _D3DKMT_DESTROYOVERLAY
{
    D3DKMT_HANDLE hDevice;  // in: Indentifies the device
    D3DKMT_HANDLE hOverlay; // in: Kernel overlay handle
} D3DKMT_DESTROYOVERLAY;

typedef struct _D3DKMT_WAITFORVERTICALBLANKEVENT
{
    D3DKMT_HANDLE                  hAdapter;      // in: adapter handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: adapter's VidPN Source ID
} D3DKMT_WAITFORVERTICALBLANKEVENT;

typedef struct _D3DKMT_SETGAMMARAMP
{
    D3DKMT_HANDLE                  hDevice;       // in: device handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: adapter's VidPN Source ID
    D3DDDI_GAMMARAMP_TYPE          Type;          // in: Gamma ramp type
    union {
        D3DDDI_GAMMA_RAMP_RGB256x3x16 *pGammaRampRgb256x3x16;
        D3DDDI_GAMMA_RAMP_DXGI_1 *     pGammaRampDXGI1;
    };
    UINT Size;
} D3DKMT_SETGAMMARAMP;

typedef enum _D3DKMT_DEVICEEXECUTION_STATE
{
    D3DKMT_DEVICEEXECUTION_ACTIVE  = 1,
    D3DKMT_DEVICEEXECUTION_RESET   = 2,
    D3DKMT_DEVICEEXECUTION_HUNG    = 3,
    D3DKMT_DEVICEEXECUTION_STOPPED = 4,
} D3DKMT_DEVICEEXECUTION_STATE;

typedef struct _D3DKMT_DEVICERESET_STATE
{
    union {
        struct
        {
            UINT DesktopSwitched : 1; // 0x00000001
            UINT Reserved : 31;       // 0xFFFFFFFE
        };
        UINT Value;
    };
} D3DKMT_DEVICERESET_STATE;

typedef struct _D3DKMT_PRESENT_STATS
{
    UINT          PresentCount;
    UINT          PresentRefreshCount;
    UINT          SyncRefreshCount;
    LARGE_INTEGER SyncQPCTime;
    LARGE_INTEGER SyncGPUTime;
} D3DKMT_PRESENT_STATS;

typedef struct _D3DKMT_DEVICEPRESENT_STATE
{
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // in: present source id
    D3DKMT_PRESENT_STATS           PresentStats;  // out: present stats
} D3DKMT_DEVICEPRESENT_STATE;

typedef enum _D3DKMT_DEVICESTATE_TYPE
{
    D3DKMT_DEVICESTATE_EXECUTION = 1,
    D3DKMT_DEVICESTATE_PRESENT   = 2,
    D3DKMT_DEVICESTATE_RESET     = 3,
} D3DKMT_DEVICESTATE_TYPE;

typedef struct _D3DKMT_GETDEVICESTATE
{
    D3DKMT_HANDLE           hDevice;   // in: device handle
    D3DKMT_DEVICESTATE_TYPE StateType; // in: device state type
    union {
        D3DKMT_DEVICEEXECUTION_STATE ExecutionState; // out: device state
        D3DKMT_DEVICEPRESENT_STATE   PresentState;   // in/out: present state
        D3DKMT_DEVICERESET_STATE     ResetState;     // out: reset state
    };
} D3DKMT_GETDEVICESTATE;

typedef struct _D3DKMT_CREATEDCFROMMEMORY
{
    VOID *        pMemory;     // in: memory for DC
    D3DDDIFORMAT  Format;      // in: Memory pixel format
    UINT          Width;       // in: Memory Width
    UINT          Height;      // in: Memory Height
    UINT          Pitch;       // in: Memory pitch
    HDC           hDeviceDc;   // in: DC describing the device
    PALETTEENTRY *pColorTable; // in: Palette
    HDC           hDc;         // out: HDC
    HANDLE        hBitmap;     // out: Handle to bitmap
} D3DKMT_CREATEDCFROMMEMORY;

typedef struct _D3DKMT_DESTROYDCFROMMEMORY
{
    HDC    hDc;     // in:
    HANDLE hBitmap; // in:
} D3DKMT_DESTROYDCFROMMEMORY;

typedef struct _D3DKMT_SETCONTEXTSCHEDULINGPRIORITY
{
    D3DKMT_HANDLE hContext; // in: context handle
    INT           Priority; // in: context priority
} D3DKMT_SETCONTEXTSCHEDULINGPRIORITY;

typedef struct _D3DKMT_CHANGESURFACEPOINTER
{
    HDC    hDC;             // in: dc handle
    HANDLE hBitmap;         // in: bitmap handle
    LPVOID pSurfacePointer; // in: new surface pointer
    UINT   Width;           // in: Memory Width
    UINT   Height;          // in: Memory Height
    UINT   Pitch;           // in: Memory pitch
} D3DKMT_CHANGESURFACEPOINTER;

typedef struct _D3DKMT_GETCONTEXTSCHEDULINGPRIORITY
{
    D3DKMT_HANDLE hContext; // in: context handle
    INT           Priority; // out: context priority
} D3DKMT_GETCONTEXTSCHEDULINGPRIORITY;

typedef enum _D3DKMT_SCHEDULINGPRIORITYCLASS
{
    D3DKMT_SCHEDULINGPRIORITYCLASS_IDLE         = 0,
    D3DKMT_SCHEDULINGPRIORITYCLASS_BELOW_NORMAL = 1,
    D3DKMT_SCHEDULINGPRIORITYCLASS_NORMAL       = 2,
    D3DKMT_SCHEDULINGPRIORITYCLASS_ABOVE_NORMAL = 3,
    D3DKMT_SCHEDULINGPRIORITYCLASS_HIGH         = 4,
    D3DKMT_SCHEDULINGPRIORITYCLASS_REALTIME     = 5,
} D3DKMT_SCHEDULINGPRIORITYCLASS;

typedef struct _D3DKMT_GETSCANLINE
{
    D3DKMT_HANDLE                  hAdapter;        // in: Adapter handle
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId;   // in: Adapter's VidPN Source ID
    BOOLEAN                        InVerticalBlank; // out: Within vertical blank
    UINT                           ScanLine;        // out: Current scan line
} D3DKMT_GETSCANLINE;

typedef enum _D3DKMT_QUEUEDLIMIT_TYPE
{
    D3DKMT_SET_QUEUEDLIMIT_PRESENT     = 1,
    D3DKMT_SET_QUEUEDLIMIT_PENDINGFLIP = 2,
    D3DKMT_GET_QUEUEDLIMIT_PRESENT     = 3,
    D3DKMT_GET_QUEUEDLIMIT_PENDINGFLIP = 4,
} D3DKMT_QUEUEDLIMIT_TYPE;

typedef struct _D3DKMT_SETQUEUEDLIMIT
{
    D3DKMT_HANDLE           hDevice; // in: device handle
    D3DKMT_QUEUEDLIMIT_TYPE Type;    // in: limit type
    union {
        UINT QueuedPresentLimit; // in (or out): queued present limit
        struct
        {
            D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId;          // in: adapter's VidPN source ID
            UINT                           QueuedPendingFlipLimit; // in (or out): flip pending limit
        };
    };
} D3DKMT_SETQUEUEDLIMIT;

typedef struct _D3DKMT_POLLDISPLAYCHILDREN
{
    D3DKMT_HANDLE hAdapter;           // in: Adapter handle
    BOOLEAN       NonDestructiveOnly; // in: Destructive or not
} D3DKMT_POLLDISPLAYCHILDREN;

typedef struct _D3DKMT_INVALIDATEACTIVEVIDPN
{
    D3DKMT_HANDLE hAdapter;              // in: Adapter handle
    VOID *        pPrivateDriverData;    // in: Private driver data
    UINT          PrivateDriverDataSize; // in: Size of private driver data
} D3DKMT_INVALIDATEACTIVEVIDPN;

typedef struct _D3DKMT_CHECKOCCLUSION
{
    D3DKMT_HANDLE hDevice; // in:  Device handle
    HWND          hWindow; // in:  Destination window handle
} D3DKMT_CHECKOCCLUSION;

typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATEALLOCATION)(IN OUT D3DKMT_CREATEALLOCATION *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_QUERYRESOURCEINFO)(IN OUT D3DKMT_QUERYRESOURCEINFO *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_OPENRESOURCE)(IN OUT D3DKMT_OPENRESOURCE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYALLOCATION)(IN CONST D3DKMT_DESTROYALLOCATION *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETALLOCATIONPRIORITY)(IN CONST D3DKMT_SETALLOCATIONPRIORITY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_QUERYALLOCATIONRESIDENCY)(IN CONST D3DKMT_QUERYALLOCATIONRESIDENCY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATEDEVICE)(IN OUT D3DKMT_CREATEDEVICE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYDEVICE)(IN CONST D3DKMT_DESTROYDEVICE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATECONTEXT)(IN OUT D3DKMT_CREATECONTEXT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYCONTEXT)(IN CONST D3DKMT_DESTROYCONTEXT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATESYNCHRONIZATIONOBJECT)(IN OUT D3DKMT_CREATESYNCHRONIZATIONOBJECT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYSYNCHRONIZATIONOBJECT)(IN CONST D3DKMT_DESTROYSYNCHRONIZATIONOBJECT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_WAITFORSYNCHRONIZATIONOBJECT)(IN OUT D3DKMT_WAITFORSYNCHRONIZATIONOBJECT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SIGNALSYNCHRONIZATIONOBJECT)(IN CONST D3DKMT_SIGNALSYNCHRONIZATIONOBJECT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_LOCK)(IN OUT D3DKMT_LOCK *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_UNLOCK)(IN CONST D3DKMT_UNLOCK *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETDISPLAYMODELIST)(IN OUT D3DKMT_GETDISPLAYMODELIST *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETDISPLAYMODE)(IN CONST D3DKMT_SETDISPLAYMODE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETMULTISAMPLEMETHODLIST)(IN OUT D3DKMT_GETMULTISAMPLEMETHODLIST *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_PRESENT)(IN CONST D3DKMT_PRESENT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_RENDER)(IN OUT D3DKMT_RENDER *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETRUNTIMEDATA)(IN CONST D3DKMT_GETRUNTIMEDATA *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_QUERYADAPTERINFO)(IN CONST D3DKMT_QUERYADAPTERINFO *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_OPENADAPTERFROMHDC)(IN OUT D3DKMT_OPENADAPTERFROMHDC *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_OPENADAPTERFROMDEVICENAME)(IN OUT D3DKMT_OPENADAPTERFROMDEVICENAME *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CLOSEADAPTER)(IN CONST D3DKMT_CLOSEADAPTER *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETSHAREDPRIMARYHANDLE)(IN OUT D3DKMT_GETSHAREDPRIMARYHANDLE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_ESCAPE)(IN CONST D3DKMT_ESCAPE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETVIDPNSOURCEOWNER)(IN CONST D3DKMT_SETVIDPNSOURCEOWNER *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETPRESENTHISTORY)(IN OUT D3DKMT_GETPRESENTHISTORY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATEOVERLAY)(IN OUT D3DKMT_CREATEOVERLAY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_UPDATEOVERLAY)(IN CONST D3DKMT_UPDATEOVERLAY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_FLIPOVERLAY)(IN CONST D3DKMT_FLIPOVERLAY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYOVERLAY)(IN CONST D3DKMT_DESTROYOVERLAY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_WAITFORVERTICALBLANKEVENT)(IN CONST D3DKMT_WAITFORVERTICALBLANKEVENT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETGAMMARAMP)(IN CONST D3DKMT_SETGAMMARAMP *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETDEVICESTATE)(IN OUT D3DKMT_GETDEVICESTATE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CREATEDCFROMMEMORY)(IN OUT D3DKMT_CREATEDCFROMMEMORY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_DESTROYDCFROMMEMORY)(IN CONST D3DKMT_DESTROYDCFROMMEMORY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETCONTEXTSCHEDULINGPRIORITY)(IN CONST D3DKMT_SETCONTEXTSCHEDULINGPRIORITY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETCONTEXTSCHEDULINGPRIORITY)(IN OUT D3DKMT_GETCONTEXTSCHEDULINGPRIORITY *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETPROCESSSCHEDULINGPRIORITYCLASS)(IN HANDLE, IN D3DKMT_SCHEDULINGPRIORITYCLASS);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETPROCESSSCHEDULINGPRIORITYCLASS)(IN HANDLE, OUT D3DKMT_SCHEDULINGPRIORITYCLASS *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_RELEASEPROCESSVIDPNSOURCEOWNERS)(IN HANDLE);
typedef NTSTATUS(APIENTRY *PFND3DKMT_GETSCANLINE)(IN OUT D3DKMT_GETSCANLINE *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CHANGESURFACEPOINTER)(IN CONST D3DKMT_CHANGESURFACEPOINTER *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_SETQUEUEDLIMIT)(IN CONST D3DKMT_SETQUEUEDLIMIT *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_POLLDISPLAYCHILDREN)(IN CONST D3DKMT_POLLDISPLAYCHILDREN *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_INVALIDATEACTIVEVIDPN)(IN CONST D3DKMT_INVALIDATEACTIVEVIDPN *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CHECKOCCLUSION)(IN CONST D3DKMT_CHECKOCCLUSION *);

#endif /* _D3DKMTHK_H_ */
