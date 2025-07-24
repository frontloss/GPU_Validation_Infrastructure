#ifndef __PORTEDROUTINES_H__
#define __PORTEDROUTINES_H__

#define SIZEOF(x) (sizeof(x) / 4)

#include <math.h>

// This global Bias will make any timer schedule to expire 16milisec before the asked DueTime to account for
// the scheduling and context switch latency
#define GLOBAL_ENV_TIMER_BIAS 16 // 15milisec

#ifdef __USERMODE
#include <windows.h>
#include <malloc.h>
#include <objbase.h>
#include <rpc.h>
#include <stdio.h>

#define PORTABLE_THREAD_ROUTINE_SIGNATURE(ThreadRoutine, pvThreadContext) DWORD ThreadRoutine(LPVOID pvThreadContext)

typedef LPTHREAD_START_ROUTINE PDP_THREAD_START_ROUTINE;

#define PORTABLE_TIMER_CALLBACK_SIGNATURE(ThreadRoutine, pvTimerCbContext) \
    VOID CALLBACK TimerAPCProc(_In_opt_ LPVOID lpArgToCompletionRoutine, _In_ DWORD dwTimerLowValue, _In_ DWORD dwTimerHighValue);

typedef VOID CALLBACK (*PDP_TIMER_CALLBACK_ROUTINE)(_In_opt_ LPVOID lpArgToCompletionRoutine, _In_ DWORD dwTimerLowValue, _In_ DWORD dwTimerHighValue);

#define PRIORITY_NO_INCREMENT 0
#define PRIORITY_INCREMENT_BY_1 IO_PARALLEL_INCREMENT
#define PRIORITY_INCREMENT_BY_2 IO_SERIAL_INCREMENT
#define PRIORITY_INCREMENT_BY_6 IO_KEYBOARD_INCREMENT
#define PRIORITY_INCREMENT_BY_8 IO_SOUND_INCREMENT

#endif

#ifdef __KERNELMODE

#include <ntddk.h>
#include <ntdef.h>
#include <wdmguid.h>
#include <Ntddvdeo.h>

typedef PVOID  LPVOID;
typedef ULONG  DWORD;
typedef PULONG LPDWORD;

#pragma warning(disable : 4127)
#pragma warning(disable : 4100)
#pragma warning(disable : 4214)
#pragma warning(disable : 4201)

#define PORTABLE_THREAD_ROUTINE_SIGNATURE(ThreadRoutine, pvThreadContext) VOID ThreadRoutine(PVOID pvThreadContext)
typedef KSTART_ROUTINE PDP_THREAD_START_ROUTINE;

#define PORTABLE_TIMER_CALLBACK_SIGNATURE(ThreadRoutine, pvTimerCbContext) VOID ThreadRoutine(PKDPC Dpc, PVOID pvTimerCbContext, PVOID pvSystemArg1, PVOID pvSystemArg2)
// typedef VOID(*PDP_TIMER_CALLBACK_ROUTINE)(PVOID pvTimerCbContext, PVOID pvSystemArg1, PVOID pvSystemArg2);
typedef PKDEFERRED_ROUTINE PDP_TIMER_CALLBACK_ROUTINE;

#define SIMDRV_THREAD_PRIORITY 12
//#define SIMDRV_DATAREGPROCESSOR_THREAD_PRIORITY 15
#define SIMDRV_DATAREGPROCESSOR_THREAD_PRIORITY LOW_REALTIME_PRIORITY

#define PRIORITY_NO_INCREMENT IO_NO_INCREMENT
#define PRIORITY_INCREMENT_BY_1 IO_PARALLEL_INCREMENT
#define PRIORITY_INCREMENT_BY_2 IO_SERIAL_INCREMENT
#define PRIORITY_INCREMENT_BY_6 IO_KEYBOARD_INCREMENT
#define PRIORITY_INCREMENT_BY_8 IO_SOUND_INCREMENT

#endif

#define MAX_PATH_SIZE 260
#define PERISTENCE_FILE_LOCATION L"\\SystemRoot\\"
#define PERISTENCE_FILE_NAME L"_SimDrvPersistenceFile.txt"

typedef enum _FILE_OPEN_MODE
{
    eReadBin,
    eWriteBin,
    eRWBin,
    eAppendBin,
    eReadAppendBin,
    eReadText,
    eWriteText,
    eRWText,
    eAppendText,
    eReadAppendText

} FILE_OPEN_MODE,
*PFILE_OPEN_MODE;

typedef enum _FILE_CREATE_STATUS
{
    eInvalidResult = 0,
    eFileCreated   = 1,
    eFileOpened    = 2,
    eFileExists    = 3,

} FILE_CREATE_STATUS,
*PFILE_CREATE_STATUS;

typedef struct _DP_FILEHANDLLE
{

#ifdef __USERMODE

    FILE *fp;

#endif

#ifdef __KERNELMODE

    HANDLE         hHandle;
    UNICODE_STRING UnicodeString;

#endif

} DP_FILEHANDLLE, *PDP_FILEHANDLLE;

typedef struct _DP_EVENT
{
    BOOLEAN bIsEventIntialized;

#ifdef __USERMODE

    HANDLE hEvent;

#endif

#ifdef __KERNELMODE

    KEVENT kEvent;

#endif

} DP_EVENT, *PDP_EVENT;

typedef struct _DP_LIST_HEAD
{

    struct _DP_LIST_ENTRY *fLink;
    struct _DP_LIST_ENTRY *bLink;

#ifdef __USERMODE

    CRITICAL_SECTION CritListLock;

#endif

#ifdef __KERNELMODE

    KIRQL      OldIrql;
    KSPIN_LOCK SpinListLock;

#endif

} DP_LIST_HEAD, *PDP_LIST_HEAD;

typedef struct _DP_LIST_ENTRY
{
    struct _DP_LIST_ENTRY *fLink;
    struct _DP_LIST_ENTRY *bLink;

} DP_LIST_ENTRY, *PDP_LIST_ENTRY;

typedef struct _DP_LOCK
{
#ifdef __USERMODE

    CRITICAL_SECTION CritListLock;

#endif

#ifdef __KERNELMODE

    KIRQL      OldIrql;
    KSPIN_LOCK SpinListLock;

#endif

} DP_LOCK, *PDP_LOCK;

typedef struct _DP_TIMER
{

#ifdef __USERMODE

    HANDLE           hTimer;
    PTIMERAPCROUTINE CallBackRoutine;

#endif

#ifdef __KERNELMODE

    KTIMER kTimer;
    KDPC   Dpc;

#endif

} DP_TIMER, *PDP_TIMER;

typedef struct _DP_LOOKASIDE_LIST_HEAD
{
    DP_LIST_HEAD DPListHead;
    ULONG        ulEntrySize;
    ULONG        ulMaxNumEntries;
    ULONG        ulInitialNumEntries;
    ULONG        ulCurrentNumEntries;
    ULONG        ulExpandFactor;

} DP_LOOKASIDE_LIST_HEAD, *PDP_LOOKASIDE_LIST_HEAD;

typedef struct _PORTINGLAYER_OBJ
{
    void *(*pfnAllocateMem)(unsigned int ulSize, BOOLEAN bZeroMemory);
    void (*pfnFreeMem)(void *pMemPtr);

    BOOLEAN (*pfnInitializeListHead)(PDP_LIST_HEAD pDPListHead);
    PDP_LIST_ENTRY (*pfnInterlockedInsertHeadList)(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pDPListEntry);
    PDP_LIST_ENTRY (*pfnInterlockedInsertTailList)(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pDPListEntry);
    PDP_LIST_ENTRY (*pfnInterlockedRemoveHeadList)(PDP_LIST_HEAD pDPListHead);
    PDP_LIST_ENTRY (*pfnInterLockedTraverseList)(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pListEntry);
    BOOLEAN (*pfnIsListEmpty)(PDP_LIST_HEAD pDPListHead);
    BOOLEAN (*pfnPurgeList)(PDP_LIST_HEAD pDPListHead);
    HANDLE (*pfnCreateThread)(LPVOID lpThreadData, PDP_THREAD_START_ROUTINE pfnRoutine, LPDWORD pldwThreadID, LONG ulThreadPriority, LONG ulBasePriority);
    BOOLEAN (*pfnTermninateThread)(void);
    BOOLEAN (*pfnTerminateThreadAndExitCleanly)(HANDLE hThreadHandler, PDP_EVENT pstThreadKillEvent, PULONG pulTimeOutIn100NanosecUnit);
    BOOLEAN (*pfnInitializeDPEvent)(PDP_EVENT pstDPEvent, BOOLEAN bManualReset, BOOLEAN bInitialState);
    BOOLEAN (*pfnSetDPEvent)(PDP_EVENT pstDPEvent, ULONG ulPriorityIncrement);
    BOOLEAN (*pfnClearDPEvent)(PDP_EVENT pstDPEvent);
    BOOLEAN (*pfnDPWaitForSingleEvent)(PDP_EVENT pstDPEvent, PULONG pulTimeOutMilliSec);
    ULONG (*pfnDPWaitForMultipleEvents)(PDP_EVENT *ppstEventList, ULONG ulEventCount, BOOLEAN bWaitAll, PULONG pulTimeOutMilliSec);
    BOOLEAN (*pfnInitializeDPLock)(PDP_LOCK pstDPLock);
    void (*pfnAcquireDPLock)(PDP_LOCK pstDPLock);
    void (*pfnReleaseDPLock)(PDP_LOCK pstDPLock);
    BOOLEAN (*pfnDelayExecutionThread)(ULONG ulDelayinMiliSeconds);
    BOOLEAN (*pfnInitializeDPTimer)(PDP_TIMER pDPTimer, BOOLEAN bIsSyncTimer);
    BOOLEAN(*pfnSetDPTimer)
    (PDP_TIMER pDPTimer, LARGE_INTEGER liDueTimeMilisec, LONG lPeriod, ULONG ulEnvBiasInMiliSec, PDP_TIMER_CALLBACK_ROUTINE pfnTimerCallBack, PVOID pvCallbackContext);
    BOOLEAN (*pfnInitializeLookAsideList)(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, ULONG ulEntrySize, ULONG ulInitialNumEntries, ULONG ulMaxNumEntries, ULONG ulExpandFactor);
    PDP_LIST_ENTRY (*pfnGetEntryFromLookAsideList)(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead);
    void (*pfnReturnEntryToLookAsideList)(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, PDP_LIST_ENTRY pDPListEntry);
    BOOLEAN (*pfnPurgeLookAsideList)(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead);
    void (*pfnInterLockedIncrement)(PULONG pulValue);
    void (*pfnInterLockedDecrement)(PULONG pulValue);
    LONG (*pfnInterLockedExchange)(PLONG pulTarget, LONG ulValue);
    BOOLEAN (*pfnCreateGuid)(GUID *pGuid);
    BOOLEAN (*pfnFileCreate)(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode, PFILE_CREATE_STATUS peFileCreateStatus);
    BOOLEAN (*pfnFileOpen)(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode);
    BOOLEAN (*pfnFileRead)(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucBuff, ULONG ulBuffSize, LONGLONG ullByteOffset, ULONG ulCount, PULONG pulBytesRead);
    BOOLEAN (*pfnFileWrite)(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucWriteBuff, ULONG ulWriteLength, LONGLONG ullByteOffset);
    BOOLEAN (*pfnFileClose)(PDP_FILEHANDLLE pstFileHandle);
    BOOLEAN (*pfnIsFileOpen)(PDP_FILEHANDLLE pstFileHandle);
    VOID (*pfnGetPersistenceFilePath)(PVOID pGfxAdapterContext, WCHAR *filePath);

} PORTINGLAYER_OBJ, *PPORTINGLAYER_OBJ;

#ifdef __USERMODE
#define IS_VALID_EVENT_OBJ(pstDPEvent) ((pstDPEvent)->hEvent != NULL) ? TRUE : FALSE
#endif

#ifdef __KERNELMODE
#define IS_VALID_EVENT_OBJ(pstDPEvent) ((pstDPEvent != NULL) ? TRUE : FALSE)
#endif

PPORTINGLAYER_OBJ GetPortingObj(void);
BOOLEAN           PORTINGLAYER_Init(void);

#endif