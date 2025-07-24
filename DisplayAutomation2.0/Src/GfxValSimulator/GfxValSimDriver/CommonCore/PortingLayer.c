#include "PortingLayer.h"
#include "..\DriverInterfaces\SimDriver.h"
#include "..\CommonInclude\ETWLogging.h"

#define LLABS(value) ((value < 0) ? -(value) : (value))
#define REPLACE_CHARECTER(string, src, dest)         \
    {                                                \
        if (NULL != string)                          \
        {                                            \
            for (INT i = 0; i < wcslen(string); i++) \
            {                                        \
                if (string[i] == src)                \
                {                                    \
                    string[i] = dest;                \
                }                                    \
            }                                        \
        }                                            \
    }

// IMP NOTES: HANDLE should also be done in a portable way in order for this to be portable across OS'es. Missed this

void *PORTINGLAYER_AllocateMemory(unsigned int ulSize, BOOLEAN bZeroMemory);
void  PORTINGLAYER_FreeMemory(void *pMemPtr);

BOOLEAN        PORTINGLAYER_InitializeListHead(PDP_LIST_HEAD pListHead);
PDP_LIST_ENTRY PORTINGLAYER_InterlockedInsertHeadList(PDP_LIST_HEAD pListHead, PDP_LIST_ENTRY pListEntry);
PDP_LIST_ENTRY PORTINGLAYER_InterlockedInsertTailList(PDP_LIST_HEAD pListHead, PDP_LIST_ENTRY pListEntry);
PDP_LIST_ENTRY PORTINGLAYER_InterlockedRemoveHeadList(PDP_LIST_HEAD pListHead);
PDP_LIST_ENTRY PORTINGLAYER_InterLockedTraverseList(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pListEntry);
BOOLEAN        PORTINGLAYER_PurgeList(PDP_LIST_HEAD pListHead);
HANDLE         PORTINGLAYER_CreateThread(LPVOID lpThreadData, PDP_THREAD_START_ROUTINE pfnRoutine, LPDWORD pldwThreadID, LONG ulThreadPriority, LONG ulBasePriority);
BOOLEAN        PORTINGLAYER_TerminateThread(void);
BOOLEAN        PORTINGLAYER_TerminateThreadAndExitCleanly(HANDLE hThreadHandle, PDP_EVENT pstThreadKillEvent, PULONG pulTimeOutIn100NanosecUnit);
BOOLEAN        PORTINGLAYER_IsListEmpty(PDP_LIST_HEAD pDPListHead);

BOOLEAN PORTINGLAYER_InitializeDPEvent(PDP_EVENT pstDPEvent, BOOLEAN bManualReset, BOOLEAN bInitialState);

BOOLEAN PORTINGLAYER_SetDPEvent(PDP_EVENT pstDPEvent, ULONG ulPriorityIncrement);

BOOLEAN PORTINGLAYER_ClearDPEvent(PDP_EVENT pstDPEvent);

BOOLEAN PORTINGLAYER_DPWaitForSingleEvent(PDP_EVENT pstDPEvent, PULONG pulTimeOutMilliSec);

BOOLEAN PORTINGLAYER_InitializeDPLock(PDP_LOCK pstDPLock);

void PORTINGLAYER_AcquireDPLock(PDP_LOCK pstDPLock);

void PORTINGLAYER_ReleaseDPLock(PDP_LOCK pstDPLock);

ULONG PORTINGLAYER_DPWaitForMultipleEvents(PDP_EVENT *ppstEventList, ULONG ulEventCount, BOOLEAN bWaitAll, PULONG pulTimeOutMilliSec);

BOOLEAN PORTINGLAYER_DelayExecutionThread(ULONG ulDelayinMiliSeconds);

BOOLEAN PORTINGLAYER_InitializeDPTimer(PDP_TIMER pDPTimer, BOOLEAN bIsSyncTimer);

BOOLEAN PORTINGLAYER_SetDPTimer(PDP_TIMER pDPTimer, LARGE_INTEGER liDueTimeMilisec, LONG lPeriod, ULONG ulEnvBiasInMiliSec, PDP_TIMER_CALLBACK_ROUTINE pfnTimerCallBack,
                                PVOID pvCallbackContext);

BOOLEAN PORTINGLAYER_InitializeLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, ULONG ulEntrySize, ULONG ulInitialNumEntries, ULONG ulMaxNumEntries,
                                             ULONG ulExpandFactor);

PDP_LIST_ENTRY PORTINGLAYER_GetEntryFromLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead);

void PORTINGLAYER_ReturnEntryToLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, PDP_LIST_ENTRY pDPListEntry);

BOOLEAN PORTINGLAYER_PurgeLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead);

void PORTINGLAYER_InterLockedIncrement(PULONG pulValue);

void PORTINGLAYER_InterLockedDecrement(PULONG pulValue);

LONG PORTINGLAYER_InterLockedExchange(PLONG pulTarget, LONG ulValue);

BOOLEAN PORTINGLAYER_CreatGuid(GUID *pGuid);

BOOLEAN PORTINGLAYER_FileCreate(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode, PFILE_CREATE_STATUS peFileCreateStatus);

BOOLEAN PORTINGLAYER_FileOpen(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode);

BOOLEAN PORTINGLAYER_FileRead(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucBuff, ULONG ulBuffSize, LONGLONG ullByteOffset, ULONG ulCount, PULONG pulBytesRead);

BOOLEAN PORTINGLAYER_FileWrite(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucWriteBuff, ULONG ulWriteLength, LONGLONG ullByteOffset);

BOOLEAN PORTINGLAYER_FileClose(PDP_FILEHANDLLE pstFileHandle);

BOOLEAN PORTINGLAYER_IsFileOpen(PDP_FILEHANDLLE pstFileHandle);

VOID PORTINGLAYER_GetPersistenceFilePath(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, WCHAR *filePath);

PPORTINGLAYER_OBJ g_pstPortingLayerObj = NULL;

PPORTINGLAYER_OBJ GetPortingObj(void)
{
    return g_pstPortingLayerObj;
}

BOOLEAN PORTINGLAYER_Init(void)
{
    BOOLEAN bRet = FALSE;

    g_pstPortingLayerObj = PORTINGLAYER_AllocateMemory(sizeof(PORTINGLAYER_OBJ), TRUE);

    if (g_pstPortingLayerObj)
    {
        g_pstPortingLayerObj->pfnAllocateMem                   = PORTINGLAYER_AllocateMemory;
        g_pstPortingLayerObj->pfnFreeMem                       = PORTINGLAYER_FreeMemory;
        g_pstPortingLayerObj->pfnInitializeListHead            = PORTINGLAYER_InitializeListHead;
        g_pstPortingLayerObj->pfnInterlockedInsertHeadList     = PORTINGLAYER_InterlockedInsertHeadList;
        g_pstPortingLayerObj->pfnInterlockedInsertTailList     = PORTINGLAYER_InterlockedInsertTailList;
        g_pstPortingLayerObj->pfnInterlockedRemoveHeadList     = PORTINGLAYER_InterlockedRemoveHeadList;
        g_pstPortingLayerObj->pfnInterLockedTraverseList       = PORTINGLAYER_InterLockedTraverseList;
        g_pstPortingLayerObj->pfnIsListEmpty                   = PORTINGLAYER_IsListEmpty;
        g_pstPortingLayerObj->pfnPurgeList                     = PORTINGLAYER_PurgeList;
        g_pstPortingLayerObj->pfnCreateThread                  = PORTINGLAYER_CreateThread;
        g_pstPortingLayerObj->pfnTermninateThread              = PORTINGLAYER_TerminateThread;
        g_pstPortingLayerObj->pfnTerminateThreadAndExitCleanly = PORTINGLAYER_TerminateThreadAndExitCleanly;
        g_pstPortingLayerObj->pfnInitializeDPEvent             = PORTINGLAYER_InitializeDPEvent;
        g_pstPortingLayerObj->pfnSetDPEvent                    = PORTINGLAYER_SetDPEvent;
        g_pstPortingLayerObj->pfnClearDPEvent                  = PORTINGLAYER_ClearDPEvent;
        g_pstPortingLayerObj->pfnDPWaitForSingleEvent          = PORTINGLAYER_DPWaitForSingleEvent;
        g_pstPortingLayerObj->pfnDPWaitForMultipleEvents       = PORTINGLAYER_DPWaitForMultipleEvents;
        g_pstPortingLayerObj->pfnInitializeDPLock              = PORTINGLAYER_InitializeDPLock;
        g_pstPortingLayerObj->pfnAcquireDPLock                 = PORTINGLAYER_AcquireDPLock;
        g_pstPortingLayerObj->pfnReleaseDPLock                 = PORTINGLAYER_ReleaseDPLock;
        g_pstPortingLayerObj->pfnDelayExecutionThread          = PORTINGLAYER_DelayExecutionThread;
        g_pstPortingLayerObj->pfnInitializeDPTimer             = PORTINGLAYER_InitializeDPTimer;
        g_pstPortingLayerObj->pfnSetDPTimer                    = PORTINGLAYER_SetDPTimer;
        g_pstPortingLayerObj->pfnInitializeLookAsideList       = PORTINGLAYER_InitializeLookAsideList;
        g_pstPortingLayerObj->pfnGetEntryFromLookAsideList     = PORTINGLAYER_GetEntryFromLookAsideList;
        g_pstPortingLayerObj->pfnReturnEntryToLookAsideList    = PORTINGLAYER_ReturnEntryToLookAsideList;
        g_pstPortingLayerObj->pfnPurgeLookAsideList            = PORTINGLAYER_PurgeLookAsideList;
        g_pstPortingLayerObj->pfnInterLockedIncrement          = PORTINGLAYER_InterLockedIncrement;
        g_pstPortingLayerObj->pfnInterLockedDecrement          = PORTINGLAYER_InterLockedDecrement;
        g_pstPortingLayerObj->pfnInterLockedExchange           = PORTINGLAYER_InterLockedExchange;
        g_pstPortingLayerObj->pfnCreateGuid                    = PORTINGLAYER_CreatGuid;
        g_pstPortingLayerObj->pfnFileCreate                    = PORTINGLAYER_FileCreate;
        g_pstPortingLayerObj->pfnFileOpen                      = PORTINGLAYER_FileOpen;
        g_pstPortingLayerObj->pfnFileRead                      = PORTINGLAYER_FileRead;
        g_pstPortingLayerObj->pfnFileWrite                     = PORTINGLAYER_FileWrite;
        g_pstPortingLayerObj->pfnFileClose                     = PORTINGLAYER_FileClose;
        g_pstPortingLayerObj->pfnIsFileOpen                    = PORTINGLAYER_IsFileOpen;
        g_pstPortingLayerObj->pfnGetPersistenceFilePath        = PORTINGLAYER_GetPersistenceFilePath;

        bRet = TRUE;
    }

    return bRet;
}

void *PORTINGLAYER_AllocateMemory(unsigned int ulSize, BOOLEAN bZeroMemory)
{
    void *pMemPtr = NULL;

#ifdef __USERMODE

    pMemPtr = malloc(ulSize);

#endif

#ifdef __KERNELMODE

    if (KeGetCurrentIrql() <= DISPATCH_LEVEL)
    {
        pMemPtr = ExAllocatePoolWithTag(NonPagedPoolNx, ulSize, SIMDRV_ALLOC_TAG);
    }
    if (pMemPtr == NULL)
    {
        GFXVALSIM_DBG_MSG("Memory Allocation failed.");
    }
#endif

    if (bZeroMemory && pMemPtr)
    {
        memset(pMemPtr, 0, ulSize);
    }

    if (pMemPtr == NULL)
    {
        GFXVALSIM_FUNC_EXIT(1);
    }
    return pMemPtr;
}

void PORTINGLAYER_FreeMemory(void *pMemPtr)
{
    do
    {
        if (pMemPtr == NULL)
        {
            break;
        }

#ifdef __USERMODE

        free(pMemPtr);

#endif

#ifdef __KERNELMODE

        if (KeGetCurrentIrql() <= DISPATCH_LEVEL)
        {
            ExFreePoolWithTag(pMemPtr, SIMDRV_ALLOC_TAG);
        }

#endif

    } while (FALSE);

    return;
}

//************** List Related***************************//
BOOLEAN PORTINGLAYER_InitializeListHead(PDP_LIST_HEAD pDPListHead)
{
    BOOLEAN bRet = TRUE;

    do
    {
        if (pDPListHead == NULL)
        {
            bRet = FALSE;
            break;
        }

        pDPListHead->fLink = (PDP_LIST_ENTRY)pDPListHead;
        pDPListHead->bLink = (PDP_LIST_ENTRY)pDPListHead;

#ifdef __USERMODE

        if (!InitializeCriticalSectionAndSpinCount(&pDPListHead->CritListLock, 200))
        {
            bRet = FALSE;
        }

#endif

#ifdef __KERNELMODE

        KeInitializeSpinLock(&pDPListHead->SpinListLock);

#endif

    } while (FALSE);

    if (bRet == FALSE)
    {
        GFXVALSIM_FUNC_EXIT(!bRet);
    }
    return bRet;
}

BOOLEAN PORTINGLAYER_IsListEmpty(PDP_LIST_HEAD pDPListHead)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pDPListHead == NULL)
        {
            bRet = TRUE;
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        if ((pDPListHead->fLink == (PDP_LIST_ENTRY)pDPListHead) && (pDPListHead->bLink == (PDP_LIST_ENTRY)pDPListHead))
        {
            bRet = TRUE;
        }

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

    } while (FALSE);

    return bRet;
}

PDP_LIST_ENTRY PORTINGLAYER_InterlockedInsertTailList(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pDPListEntry)
{
    PDP_LIST_ENTRY pLastHeadEntry = NULL;

    do
    {

        if (pDPListHead == NULL || pDPListEntry == NULL)
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        pLastHeadEntry = pDPListHead->bLink;

        pDPListHead->bLink->fLink = pDPListEntry;
        pDPListEntry->bLink       = pDPListHead->bLink;
        pDPListHead->bLink        = pDPListEntry;
        pDPListEntry->fLink       = (PDP_LIST_ENTRY)pDPListHead;

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

    } while (FALSE);

    return pLastHeadEntry;
}

PDP_LIST_ENTRY PORTINGLAYER_InterlockedInsertHeadList(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pDPListEntry)
{
    PDP_LIST_ENTRY pLastTailEntry = NULL;

    do
    {

        if (pDPListHead == NULL || pDPListEntry == NULL)
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        pLastTailEntry = pDPListHead->fLink;

        pDPListEntry->fLink       = pDPListHead->fLink;
        pDPListEntry->bLink       = (PDP_LIST_ENTRY)pDPListHead;
        pDPListHead->fLink->bLink = pDPListEntry;
        pDPListHead->fLink        = pDPListEntry;

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

    } while (FALSE);

    return pLastTailEntry;
}

PDP_LIST_ENTRY PORTINGLAYER_InterlockedRemoveHeadList(PDP_LIST_HEAD pDPListHead)
{
    PDP_LIST_ENTRY pEntry = NULL;

    do
    {
        if (pDPListHead == NULL || (pDPListHead->fLink == (PDP_LIST_ENTRY)pDPListHead && pDPListHead->bLink == (PDP_LIST_ENTRY)pDPListHead))
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        pEntry = pDPListHead->fLink;

        pDPListHead->fLink->fLink->bLink = (PDP_LIST_ENTRY)pDPListHead;
        pDPListHead->fLink               = pDPListHead->fLink->fLink;

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

    } while (FALSE);

    return pEntry;
}

// If pListEntry == NULL, that means we are starting the list traverse so we use listhead to get the next entry
// otherwise we use ListEntry to get its next entry. Once the next entry is equal to the ListHead that means
// we have traversed the whole list and we return list
// There could be another implementation were ListEntry is the only input and this function just returns the next node
// In which case the caller would have to keep comparing it with the ListHead in its code to see if we have reached the end
PDP_LIST_ENTRY PORTINGLAYER_InterLockedTraverseList(PDP_LIST_HEAD pDPListHead, PDP_LIST_ENTRY pListEntry)
{
    PDP_LIST_ENTRY pEntry = NULL;

    do
    {

        if (pDPListHead == NULL)
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        if (pListEntry == NULL)
        {
            pEntry = pDPListHead->fLink;
        }
        else
        {
            pEntry = pListEntry->fLink;
        }

        if (pEntry == (PDP_LIST_ENTRY)pDPListHead)
        {
            pEntry = NULL;
        }

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

    } while (FALSE);

    return pEntry;
}

BOOLEAN PORTINGLAYER_PurgeList(PDP_LIST_HEAD pDPListHead)
{
    BOOLEAN        bRet         = FALSE;
    PDP_LIST_ENTRY pDPListEntry = NULL;

    do
    {

        if (pDPListHead == NULL)
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPListHead->SpinListLock, &pDPListHead->OldIrql);

#endif

        while (pDPListHead->fLink != NULL && pDPListHead->fLink != (PDP_LIST_ENTRY)pDPListHead)
        {
            pDPListEntry       = pDPListHead->fLink;
            pDPListHead->fLink = pDPListHead->fLink->fLink;
            PORTINGLAYER_FreeMemory(pDPListEntry);
        }

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPListHead->SpinListLock, pDPListHead->OldIrql);

#endif

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_InitializeLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, ULONG ulEntrySize, ULONG ulInitialNumEntries, ULONG ulMaxNumEntries,
                                             ULONG ulExpandFactor)
{
    BOOLEAN        bRet       = TRUE;
    PDP_LIST_ENTRY pListEntry = NULL;
    ULONG          ulCount    = 0;

    do
    {
        if (pDPLookAsideListHead == NULL || ulEntrySize <= sizeof(PDP_LIST_ENTRY) || ulInitialNumEntries == 0 || ulInitialNumEntries > ulMaxNumEntries)
        {
            bRet = FALSE;
            break;
        }

        PORTINGLAYER_InitializeListHead(&pDPLookAsideListHead->DPListHead);
        pDPLookAsideListHead->ulEntrySize         = ulEntrySize;
        pDPLookAsideListHead->ulInitialNumEntries = pDPLookAsideListHead->ulCurrentNumEntries = ulInitialNumEntries;
        pDPLookAsideListHead->ulMaxNumEntries                                                 = ulMaxNumEntries;
        pDPLookAsideListHead->ulExpandFactor                                                  = ulExpandFactor;

        for (ulCount; ulCount < ulInitialNumEntries; ulCount++)
        {
            pListEntry = PORTINGLAYER_AllocateMemory(ulEntrySize, TRUE);

            if (pListEntry == NULL)
            {
                bRet = FALSE;
                break;
            }

            // Insert the just created entry at the Tail

            pListEntry->fLink                             = (PDP_LIST_ENTRY)&pDPLookAsideListHead->DPListHead;
            pListEntry->bLink                             = pDPLookAsideListHead->DPListHead.bLink;
            pDPLookAsideListHead->DPListHead.bLink->fLink = pListEntry;
            pDPLookAsideListHead->DPListHead.bLink        = pListEntry;
        }

    } while (FALSE);

    return bRet;
}

PDP_LIST_ENTRY PORTINGLAYER_GetEntryFromLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead)
{
    PDP_LIST_ENTRY pListEntry      = NULL;
    ULONG          ulNumNewEntries = 0;
    ULONG          ulCount         = 0;

#ifdef __USERMODE

    EnterCriticalSection(&pDPLookAsideListHead->DPLock.CritListLock);

#elif __KERNELMODE

    KeAcquireSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, &pDPLookAsideListHead->DPListHead.OldIrql);

#endif

    if (pDPLookAsideListHead->DPListHead.fLink != (PDP_LIST_ENTRY)pDPLookAsideListHead && pDPLookAsideListHead->DPListHead.bLink != (PDP_LIST_ENTRY)pDPLookAsideListHead &&
        pDPLookAsideListHead->DPListHead.fLink != pDPLookAsideListHead->DPListHead.bLink)
    {
        // So list is not empty therefore get an entry // Remove Head List
        pListEntry = pDPLookAsideListHead->DPListHead.fLink;

        pDPLookAsideListHead->DPListHead.fLink->fLink->bLink = (PDP_LIST_ENTRY)&pDPLookAsideListHead->DPListHead;
        pDPLookAsideListHead->DPListHead.fLink               = pDPLookAsideListHead->DPListHead.fLink->fLink;
    }
    else
    {
        ulNumNewEntries = min((pDPLookAsideListHead->ulMaxNumEntries - pDPLookAsideListHead->ulCurrentNumEntries), pDPLookAsideListHead->ulExpandFactor);
        pDPLookAsideListHead->ulCurrentNumEntries += ulNumNewEntries;

        for (ulCount = 0; ulCount < ulNumNewEntries - 1; ulCount++)
        {
            pListEntry = PORTINGLAYER_AllocateMemory(pDPLookAsideListHead->ulEntrySize, TRUE);

            if (pListEntry)
            {
                // Insert Tail List
                pListEntry->fLink                             = (PDP_LIST_ENTRY)&pDPLookAsideListHead->DPListHead;
                pListEntry->bLink                             = pDPLookAsideListHead->DPListHead.bLink;
                pDPLookAsideListHead->DPListHead.bLink->fLink = pListEntry;
                pDPLookAsideListHead->DPListHead.bLink        = pListEntry;
            }
            else
            {
                break;
            }
        }

        pListEntry = PORTINGLAYER_AllocateMemory(pDPLookAsideListHead->ulEntrySize, TRUE);
    }

#ifdef __USERMODE

    LeaveCriticalSection(&pDPListHead->DPLock.CritListLock);

#elif __KERNELMODE

    KeReleaseSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, pDPLookAsideListHead->DPListHead.OldIrql);

#endif

    return pListEntry;
}

void PORTINGLAYER_ReturnEntryToLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead, PDP_LIST_ENTRY pDPListEntry)
{

    do
    {
        if (pDPLookAsideListHead == NULL || pDPListEntry == NULL)
        {
            // Assert
            break;
        }

        // Zero out the entry being returned to the lookaside list
        memset(pDPListEntry, 0, pDPLookAsideListHead->ulEntrySize);

#ifdef __USERMODE

        EnterCriticalSection(&pDPLookAsideListHead->> DPLock.CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, &pDPLookAsideListHead->DPListHead.OldIrql);

#endif

        // Insert Tail List
        pDPListEntry->fLink                           = (PDP_LIST_ENTRY)&pDPLookAsideListHead->DPListHead;
        pDPListEntry->bLink                           = pDPLookAsideListHead->DPListHead.bLink;
        pDPLookAsideListHead->DPListHead.bLink->fLink = pDPListEntry;
        pDPLookAsideListHead->DPListHead.bLink        = pDPListEntry;

#ifdef __USERMODE

        LeaveCriticalSection(&pDPListHead->DPLock.CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, pDPLookAsideListHead->DPListHead.OldIrql);

#endif

    } while (FALSE);
}

BOOLEAN PORTINGLAYER_PurgeLookAsideList(PDP_LOOKASIDE_LIST_HEAD pDPLookAsideListHead)
{
    BOOLEAN        bRet         = FALSE;
    PDP_LIST_ENTRY pDPListEntry = NULL;

    do
    {

        if (pDPLookAsideListHead == NULL)
        {
            break;
        }

#ifdef __USERMODE

        EnterCriticalSection(&pDPLookAsideListHead->DPListHead.CritListLock);

#elif __KERNELMODE

        KeAcquireSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, &pDPLookAsideListHead->DPListHead.OldIrql);

#endif

        pDPLookAsideListHead->ulCurrentNumEntries = 0;
        pDPLookAsideListHead->ulEntrySize         = 0;
        pDPLookAsideListHead->ulExpandFactor      = 0;
        pDPLookAsideListHead->ulInitialNumEntries = 0;
        pDPLookAsideListHead->ulMaxNumEntries     = 0;

        while (pDPLookAsideListHead->DPListHead.fLink != NULL && pDPLookAsideListHead->DPListHead.fLink != (PDP_LIST_ENTRY)&pDPLookAsideListHead->DPListHead)
        {
            pDPListEntry                           = pDPLookAsideListHead->DPListHead.fLink;
            pDPLookAsideListHead->DPListHead.fLink = pDPLookAsideListHead->DPListHead.fLink->fLink;
            PORTINGLAYER_FreeMemory(pDPListEntry);
        }

#ifdef __USERMODE

        LeaveCriticalSection(&pDPLookAsideListHead->DPListHead.CritListLock);

#elif __KERNELMODE

        KeReleaseSpinLock(&pDPLookAsideListHead->DPListHead.SpinListLock, pDPLookAsideListHead->DPListHead.OldIrql);

#endif

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}
HANDLE PORTINGLAYER_CreateThread(LPVOID lpThreadData, PDP_THREAD_START_ROUTINE pfnRoutine, LPDWORD pldwThreadID, LONG ulThreadPriority, LONG ulBasePriority)
{
    HANDLE hThreadHandle = NULL;

#ifdef __USERMODE

    hThreadHandle = CreateThread(NULL, // Non-inheriable
                                 0,    // Default Stack size
                                 pfnRoutine, lpThreadData,
                                 0, // Thread runs immediately after creation not suspended
                                 pldwThreadID);

#endif

#ifdef __KERNELMODE

    NTSTATUS  ntStatus    = STATUS_UNSUCCESSFUL;
    KPRIORITY OldPriority = 0;

    ntStatus = PsCreateSystemThread(&hThreadHandle, SYNCHRONIZE, NULL, NULL, NULL, pfnRoutine, lpThreadData);

    if (ntStatus == STATUS_SUCCESS)
    {

        if (ulBasePriority)
        {
            // Call KeSetBasePriority
        }

        if (ulThreadPriority)
        {
            PKTHREAD pkThread = NULL;
            ntStatus          = ObReferenceObjectByHandle(hThreadHandle, GENERIC_ALL, *PsThreadType, KernelMode, &pkThread, NULL);

            if (ntStatus == STATUS_SUCCESS)
            {
                OldPriority = KeSetPriorityThread(pkThread, ulThreadPriority);

                if (OldPriority == ulThreadPriority)
                {
                    // Assert
                }

                ObDereferenceObject(pkThread);
            }
        }
    }
    else
    {
        GFXVALSIM_DBG_MSG("Failed to create Thread: %ld", ntStatus);
    }

#endif

    return hThreadHandle;
}

BOOLEAN PORTINGLAYER_TerminateThread(void)
{
    BOOLEAN bRet = TRUE;

    do
    {
#ifdef __USERMODE

#endif

#ifdef __KERNELMODE
        GFXVALSIM_FUNC_ENTRY();
        if (STATUS_SUCCESS != PsTerminateSystemThread(STATUS_SUCCESS))
        {
            bRet = FALSE;
        }
        GFXVALSIM_FUNC_EXIT(!bRet);
#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_TerminateThreadAndExitCleanly(HANDLE hThreadHandle, PDP_EVENT pstThreadKillEvent, PULONG pulTimeOutIn100NanosecUnit)
{
    BOOLEAN bRet = FALSE;

    do
    {
#ifdef __USERMODE

#endif

#ifdef __KERNELMODE

        NTSTATUS      ntStatus   = STATUS_UNSUCCESSFUL;
        LARGE_INTEGER ullTimeout = { 0 };
        PKTHREAD      pKThread   = NULL;

        ntStatus = ObReferenceObjectByHandle(hThreadHandle, EVENT_QUERY_STATE, *PsThreadType, KernelMode, &pKThread, NULL);

        if (!NT_SUCCESS(ntStatus) || pKThread == NULL)
        {
            break;
        }

        ntStatus = ZwClose(hThreadHandle);

        if (!NT_SUCCESS(ntStatus))
        {
            break;
        }

        KeSetEvent(&pstThreadKillEvent->kEvent, PRIORITY_NO_INCREMENT, FALSE);

        if (pulTimeOutIn100NanosecUnit)
        {
            ullTimeout.QuadPart = -1 * (*pulTimeOutIn100NanosecUnit);
        }

        ntStatus = KeWaitForSingleObject(pKThread, Executive, KernelMode, FALSE, ((pulTimeOutIn100NanosecUnit == NULL) ? NULL : &ullTimeout));

        if (NT_SUCCESS(ntStatus))
        {
            bRet = TRUE;
        }

        ObDereferenceObject(pKThread);

#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_InitializeDPEvent(PDP_EVENT pstDPEvent, BOOLEAN bManualReset, BOOLEAN bInitialState)
{
    BOOLEAN bRet = TRUE;

#ifdef __USERMODE

    pstDPEvent->hEvent = CreateEvent(NULL, bManualReset, bInitialState, NULL);
    if (pstDPEvent->hEvent)
    {
        pstDPEvent->bIsEventIntialized = TRUE;
    }
    else
    {
        bRet = FALSE;
    }

#endif

#ifdef __KERNELMODE

    KeInitializeEvent(&pstDPEvent->kEvent, (bManualReset ? NotificationEvent : SynchronizationEvent), bInitialState);
    pstDPEvent->bIsEventIntialized = TRUE;

#endif

    return bRet;
}

BOOLEAN PORTINGLAYER_SetDPEvent(PDP_EVENT pstDPEvent, ULONG ulPriorityIncrement)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstDPEvent == NULL)
        {
            break;
        }

#ifdef __USERMODE

        bRet = SetEvent(pstDPEvent->hEvent);

#endif

#ifdef __KERNELMODE

        KIRQL CurrentIrql = KeGetCurrentIrql();

        if (CurrentIrql > DISPATCH_LEVEL)
        {
            break;
        }

        bRet = !KeSetEvent(&pstDPEvent->kEvent, ulPriorityIncrement, FALSE);

#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_ClearDPEvent(PDP_EVENT pstDPEvent)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstDPEvent == NULL)
        {
            break;
        }

#ifdef __USERMODE

        bRet = ResetEvent(pstDPEvent->hEvent);

#endif

#ifdef __KERNELMODE

        KIRQL CurrentIRQL = KeGetCurrentIrql();

        if (CurrentIRQL > DISPATCH_LEVEL)
        {
            break;
        }

        KeClearEvent(&pstDPEvent->kEvent);

#endif

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_DPWaitForSingleEvent(PDP_EVENT pstDPEvent, PULONG pulTimeOutIn100NanosecUnit)
{
    BOOLEAN bRet = TRUE;

    do
    {
        if (pstDPEvent == NULL)
        {
            bRet = FALSE;
            break;
        }

#ifdef __USERMODE
        DWORD dwTimeOut = 0;

        // Divide by 10000 as Usermode wait function can only take timeout in Miliseconds
        // So if the usermode call to this function needs 1 ms timeout then 1ms = 10000 100Nanoseconds
        (pulTimeOutIn100NanosecUnit == NULL) ? (dwTimeOut = INFINITE) : (dwTimeOut = *pulTimeOutIn100NanosecUnit / 10000);

        // Need to check the return of this function too //TBD
        WaitForSingleObject(pstDPEvent->hEvent, dwTimeOut);
#endif

#ifdef __KERNELMODE

        NTSTATUS      ntStatus   = STATUS_UNSUCCESSFUL;
        LARGE_INTEGER ullTimeout = { 0 };

        if (pulTimeOutIn100NanosecUnit)
        {
            ullTimeout.QuadPart = -1 * (*pulTimeOutIn100NanosecUnit);
        }

        ntStatus = KeWaitForSingleObject(&pstDPEvent->kEvent, Executive, KernelMode, FALSE, ((pulTimeOutIn100NanosecUnit == NULL) ? NULL : &ullTimeout));

        if (ntStatus == STATUS_TIMEOUT)
        {
            // Printf here for debug purposes
        }

        if (ntStatus != STATUS_SUCCESS)
        {
            bRet = FALSE;
            // Printf here for debug purposes
        }

#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_InitializeDPLock(PDP_LOCK pstDPLock)
{
    BOOLEAN bRet = TRUE;

    do
    {
        if (pstDPLock == NULL)
        {
            bRet = FALSE;
            break;
        }

#ifdef __USERMODE
        bRet = InitializeCriticalSectionAndSpinCount(&pstDPLock->CritListLock, 4000);
#endif

#ifdef __KERNELMODE
        KeInitializeSpinLock(&pstDPLock->SpinListLock);
#endif

    } while (FALSE);

    return bRet;
}

void PORTINGLAYER_AcquireDPLock(PDP_LOCK pstDPLock)
{
    do
    {
        if (pstDPLock == NULL)
        {
            // Assert
            break;
        }

#ifdef __USERMODE
        EnterCriticalSection(&pstDPLock->CritListLock);
#endif

#ifdef __KERNELMODE
        KeAcquireSpinLock(&pstDPLock->SpinListLock, &pstDPLock->OldIrql);
#endif

    } while (FALSE);

    return;
}

void PORTINGLAYER_ReleaseDPLock(PDP_LOCK pstDPLock)
{
    do
    {
        if (pstDPLock == NULL)
        {
            // Assert
            break;
        }

#ifdef __USERMODE
        LeaveCriticalSection(&pstDPLock->CritListLock);
#endif

#ifdef __KERNELMODE
        KeReleaseSpinLock(&pstDPLock->SpinListLock, pstDPLock->OldIrql);
#endif

    } while (FALSE);

    return;
}

ULONG PORTINGLAYER_DPWaitForMultipleEvents(PDP_EVENT *ppstEventList, ULONG ulEventCount, BOOLEAN bWaitAll, PULONG pulTimeOutIn100NanosecUnit)
{
    ULONG   ulCount = 0;
    BOOLEAN bRet    = TRUE;
    ULONG   ulIndex = MAXIMUM_WAIT_OBJECTS; // This marcro has the same name and value in user as well as kernel mode

    do
    {
        if (ulEventCount == 0 || ppstEventList == NULL || ulEventCount > MAXIMUM_WAIT_OBJECTS)
        {
            break;
            // Assert
        }

#ifdef __USERMODE

        DWORD dwTimeOut = 0;

        HANDLE *pHandleList = NULL;

        DWORD dwWaitRet = WAIT_FAILED;

        pHandleList = (HANDLE *)malloc(ulEventCount * sizeof(HANDLE));

        if (pHandleList == NULL)
        {
            break;
        }

        (pulTimeOutIn100NanosecUnit == NULL) ? (dwTimeOut = INFINITE) : (dwTimeOut = *pulTimeOutIn100NanosecUnit / 10000);

        for (ulCount = 0; ulCount < ulEventCount; ulCount++)
        {
            if (*ppstEventList == NULL)
            {
                free(pHandleList);
                bRet = FALSE;
                break;
            }

            pHandleList[ulCount] = (*ppstEventList)->hEvent;
            ppstEventList++;
        }

        if (bRet == FALSE)
        {
            break;
        }

        dwWaitRet = WaitForMultipleObjects(ulEventCount, pHandleList, bWaitAll, dwTimeOut);

        if (bWaitAll == TRUE && dwWaitRet != WAIT_OBJECT_0)
        {
            // Assert
        }
        else if (bWaitAll == FALSE && (dwWaitRet >= = WAIT_OBJECT_0 && dwWaitRet < (WAIT_OBJECT_0 + ulEventCount)))
        {
            ulIndex = dwWaitRet - WAIT_OBJECT_0;
        }
        else
        {
            // Assert (dwWaitRet == WAIT_TIMEOUT || dwWaitRet == WAIT_FAILED)
        }

        free(pHandleList);

#endif

#ifdef __KERNELMODE
        NTSTATUS      ntStatus         = STATUS_UNSUCCESSFUL;
        LARGE_INTEGER TimeOut          = { 0 };
        PVOID *       pEventList       = NULL;
        PKWAIT_BLOCK  pkWaitBlockArray = NULL;

        if (pulTimeOutIn100NanosecUnit)
        {
            TimeOut.QuadPart = -1 * (*pulTimeOutIn100NanosecUnit);
        }

        pEventList = (PVOID *)ExAllocatePoolWithTag(NonPagedPool, sizeof(PVOID) * ulEventCount, SIMDRV_ALLOC_TAG);

        if (pEventList == NULL)
        {
            break;
        }

        for (ulCount = 0; ulCount < ulEventCount; ulCount++)
        {
            if (*ppstEventList == NULL)
            {
                ExFreePool(pEventList);
                bRet = FALSE;
                break;
            }

            pEventList[ulCount] = &ppstEventList[ulCount]->kEvent;
        }

        if (ulEventCount > THREAD_WAIT_OBJECTS)
        {
            pkWaitBlockArray = ExAllocatePoolWithTag(NonPagedPool, sizeof(KWAIT_BLOCK) * ulEventCount, SIMDRV_ALLOC_TAG);

            if (pkWaitBlockArray == NULL)
            {
                // ASSERT
            }
        }

        ntStatus = KeWaitForMultipleObjects(ulEventCount, pEventList, (bWaitAll ? WaitAll : WaitAny), Executive, KernelMode, FALSE,
                                            ((pulTimeOutIn100NanosecUnit == NULL) ? NULL : &TimeOut), pkWaitBlockArray);

        if (bWaitAll == TRUE && ntStatus != STATUS_SUCCESS)
        {
            // Assert
        }
        else if (bWaitAll == FALSE && (ntStatus >= STATUS_WAIT_0 && ntStatus <= STATUS_ABANDONED_WAIT_63))
        {
            ulIndex = ntStatus - STATUS_WAIT_0;
        }
        else
        {
            // Assert (dwWaitRet == WAIT_TIMEOUT || dwWaitRet == WAIT_FAILED)
        }

        ExFreePool(pEventList);

        if (pkWaitBlockArray)
        {
            ExFreePool(pkWaitBlockArray);
        }

#endif

    } while (FALSE);

    return ulIndex;
}

BOOLEAN PORTINGLAYER_DelayExecutionThread(ULONG ulDelayinMiliSeconds)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (ulDelayinMiliSeconds == 0)
        {
            // Assert
            break;
        }

#ifdef __USERMODE

#endif

#ifdef __KERNELMODE

        /*KeDelayExecutionThread( KernelMode,
                                FALSE,
                                pstLargeInteger);*/

#endif

    } while (FALSE);

    return bRet;
}

// BOOLEAN PORTINGLAYER_InitializeDPDeferredProcedure(PDP_DEFERRED_PROCEDURE pDPDeferredProcedure)
//{
//    BOOLEAN bRet = FALSE;
//
//    do
//    {
//        if (pDPDeferredProcedure == NULL)
//        {
//            //Assert
//            break;
//        }
//
//#ifdef __USERMODE
//
//#endif
//
//#ifdef __KERNELMODE
//
//        KeInitializeDpc(
//            pDPDeferredProcedure->Dpc,
//            DeferredRoutine,
//            IN PVOID  DeferredContext
//        );
//
//
//#endif
//
//
//    } while (FALSE);
//
//    return;
//
//
//}

BOOLEAN PORTINGLAYER_InitializeDPTimer(PDP_TIMER pDPTimer, BOOLEAN bIsSyncTimer)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pDPTimer == NULL)
        {
            // Assert
            break;
        }

#ifdef __USERMODE

        pDPTimer->hTimer = CreateWaitableTimer(NULL, (bSyncTimer == TRUE ? FALSE : TRUE), NULL);

        pDPTimer->CallBackRoutine = pfnTimerCallBack;

#endif

#ifdef __KERNELMODE

        KeInitializeTimerEx(&pDPTimer->kTimer, (bIsSyncTimer == TRUE ? SynchronizationTimer : NotificationTimer));

#endif

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_SetDPTimer(PDP_TIMER pDPTimer, LARGE_INTEGER liDueTimeMilisec, LONG lPeriod, ULONG ulEnvBiasInMiliSec, PDP_TIMER_CALLBACK_ROUTINE pfnTimerCallBack,
                                PVOID pvCallbackContext)
{
    BOOLEAN bRet = FALSE;
    do
    {
        if (pDPTimer == NULL)
        {
            // Assert
            break;
        }

        if (ulEnvBiasInMiliSec)
        {
            if (LLABS(liDueTimeMilisec.QuadPart) > 2 * ulEnvBiasInMiliSec)
            {
                liDueTimeMilisec.QuadPart = liDueTimeMilisec.QuadPart + ulEnvBiasInMiliSec * 10000;
            }

            lPeriod = lPeriod - ulEnvBiasInMiliSec;
        }

#ifdef __USERMODE

        bRet = SetWaitableTimer(&pDPTimer->kTimer, &liDueTimeMilisec, lPeriod, pfnTimerCallBacks, pvCallbackContext, false);

#endif

#ifdef __KERNELMODE

        KeInitializeDpc(&pDPTimer->Dpc, pfnTimerCallBack, pvCallbackContext);
        bRet = KeSetTimerEx(&pDPTimer->kTimer, liDueTimeMilisec, lPeriod, &pDPTimer->Dpc);

        // bRet will be true if the timer was already set. This should be an error condition
        bRet = bRet == TRUE ? FALSE : TRUE;
#endif

    } while (FALSE);

    return bRet;
}

void PORTINGLAYER_InterLockedIncrement(PULONG pulValue)
{
}

void PORTINGLAYER_InterLockedDecrement(PULONG pulValue)
{
}

LONG PORTINGLAYER_InterLockedExchange(PLONG pulTarget, LONG ulValue)
{
    LONG retVal = -1;

#ifdef __USERMODE

#endif

#ifdef __KERNELMODE

    retVal = InterlockedExchange(pulTarget, ulValue);

#endif

    return retVal;
}

BOOLEAN PORTINGLAYER_CreatGuid(GUID *pGuid)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pGuid == NULL)
        {
            break;
        }

#ifdef __USERMODE

        if (S_OK == UuidCreate(pGuid))
        {
            bRet = TRUE;
            break;
        }

#endif

#ifdef __KERNELMODE

        // This function is behaving oddly. Creating GUID but not returning Successs. So blindly calling temporarily till I find another function
        /*
        if (STATUS_SUCCESS == ExUuidCreate(pGuid))
        {
            bRet = TRUE;
            break;
        }
        */

        ExUuidCreate(pGuid);
        bRet = TRUE;

#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_FileCreate(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode, PFILE_CREATE_STATUS peFileCreateStatus)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();
    do
    {

        if (pstFileHandle == NULL)
        {
            break;
        }

#ifdef __USERMODE

        PWCHAR puwFileMode = NULL;
        size_t errorVal    = 0;
        switch (eMode)
        {

        case eReadBin:
            puwFileMode = L"rb";
            break;
        case eWriteBin:
            puwFileMode = L"wb";
            break;
        case eRWBin:
            puwFileMode = L"wb+";
            break;
        case eAppendBin:
            puwFileMode = L"ab";
            break;
        case eReadAppendBin:
            puwFileMode = L"ab+";
            break;
        case eReadText:
            puwFileMode = L"rt";
            break;
        case eWriteText:
            puwFileMode = L"wt";
            break;
        case eRWText:
            puwFileMode = L"wt+";
            break;
        case eAppendText:
            puwFileMode = L"at";
            break;
        case eReadAppendText:
            puwFileMode = L"at+";
            break;

        default:
            break;
        }

        if (puwFilePath)
        {
            // This needs to be updated for createfile
            bRet = !_wfopen_s(&pstFileHandle->fp, puwFilePath, puwFileMode);
        }

#endif

#ifdef __KERNELMODE

        ACCESS_MASK        AccessMask          = SYNCHRONIZE;
        NTSTATUS           ntStatus            = STATUS_UNSUCCESSFUL;
        IO_STATUS_BLOCK    IoStatusBlock       = { 0 };
        OBJECT_ATTRIBUTES  stObjAttribs        = { 0 };
        LARGE_INTEGER      AllocationSize      = { 0 };
        ULONG              ulAttributes        = OBJ_KERNEL_HANDLE; //| OBJ_EXCLUSIVE;
        ULONG              uCreateOptions      = FILE_WRITE_THROUGH | FILE_SYNCHRONOUS_IO_NONALERT | FILE_SEQUENTIAL_ONLY | FILE_NON_DIRECTORY_FILE;
        KIRQL              CurrentIRQL         = KeGetCurrentIrql();
        PSIMDEV_EXTENTSION pSimDrvExtension    = NULL;
        HANDLE             deviceDirPathHandle = NULL;
        UNICODE_STRING     exProceedureName;
        NTSTATUS (*pfnIoGetDeviceDirectory)() = NULL;

        pSimDrvExtension = GetSimDrvExtension();
        if (NULL == pSimDrvExtension)
        {
            return bRet;
        }

        if (CurrentIRQL > PASSIVE_LEVEL)
        {
            break;
        }

        pstFileHandle->UnicodeString.Length = MAX_PATH_SIZE;
        pstFileHandle->UnicodeString.Buffer = ExAllocatePoolWithTag(NonPagedPool, MAX_PATH_SIZE, SIMDRV_ALLOC_TAG);

        if (pucFilePath)
        {
            // ntStatus = RtlAnsiStringToUnicodeString(&pstFileHandle->UnicodeString, pucFilePath, FALSE);
        }

        RtlInitUnicodeString(&exProceedureName, L"IoGetDeviceDirectory");
        pfnIoGetDeviceDirectory = MmGetSystemRoutineAddress(&exProceedureName);

        if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber) && (NULL != pfnIoGetDeviceDirectory))
        {
            ntStatus = pfnIoGetDeviceDirectory(pSimDrvExtension->pstPhysicalDeviceObject, DeviceDirectoryData, 0, NULL, &deviceDirPathHandle);
            if (!NT_SUCCESS(ntStatus))
            {
                GFXVALSIM_DBG_MSG("IoGetDeviceDirectory call failed!");
                return bRet;
            }
        }

        if (puwFilePath)
        {
            RtlInitUnicodeString(&pstFileHandle->UnicodeString, puwFilePath);
        }

        InitializeObjectAttributes(&stObjAttribs, &pstFileHandle->UnicodeString, ulAttributes, deviceDirPathHandle, NULL);

        switch (eMode)
        {
        case eReadBin:
            AccessMask |= FILE_READ_DATA;
            break;

        case eWriteBin:
            AccessMask |= FILE_WRITE_DATA;
            break;

        case eRWBin:
            AccessMask |= FILE_READ_DATA | FILE_WRITE_DATA;
            break;

        default:
            break;
        }

        ntStatus =
        ZwCreateFile(&pstFileHandle->hHandle, AccessMask, &stObjAttribs, &IoStatusBlock, &AllocationSize, FILE_ATTRIBUTE_NORMAL, 0, FILE_OPEN_IF, uCreateOptions, NULL, 0);

        if (ntStatus == STATUS_SUCCESS)
        {
            if (peFileCreateStatus)
            {
                if (IoStatusBlock.Information == FILE_OPENED)
                {
                    *peFileCreateStatus = eFileOpened;
                }
                else if (IoStatusBlock.Information == FILE_CREATED)
                {
                    *peFileCreateStatus = eFileCreated;
                }
                else if (IoStatusBlock.Information == FILE_EXISTS)
                {
                    *peFileCreateStatus = eFileExists;
                }
            }

            bRet = TRUE;
        }
        else
        {
            GFXVALSIM_DBG_MSG("ZwCreateFile call failed!");
        }
        if (deviceDirPathHandle)
        {
            ZwClose(deviceDirPathHandle);
        }

#endif

    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PORTINGLAYER_FileOpen(PDP_FILEHANDLLE pstFileHandle, const char *pucFilePath, const wchar_t *puwFilePath, FILE_OPEN_MODE eMode)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();
    do
    {

        if (pstFileHandle == NULL)
        {
            break;
        }

#ifdef __USERMODE

        PWCHAR puwFileMode = NULL;
        size_t errorVal    = 0;
        switch (eMode)
        {

        case eReadBin:
            puwFileMode = L"rb";
            break;
        case eWriteBin:
            puwFileMode = L"wb";
            break;
        case eRWBin:
            puwFileMode = L"wb+";
            break;
        case eAppendBin:
            puwFileMode = L"ab";
            break;
        case eReadAppendBin:
            puwFileMode = L"ab+";
            break;
        case eReadText:
            puwFileMode = L"rt";
            break;
        case eWriteText:
            puwFileMode = L"wt";
            break;
        case eRWText:
            puwFileMode = L"wt+";
            break;
        case eAppendText:
            puwFileMode = L"at";
            break;
        case eReadAppendText:
            puwFileMode = L"at+";
            break;

        default:
            break;
        }

        if (puwFilePath)
        {

            bRet = !_wfopen_s(&pstFileHandle->fp, puwFilePath, puwFileMode);
        }

#endif

#ifdef __KERNELMODE

        ACCESS_MASK        AccessMask          = SYNCHRONIZE;
        NTSTATUS           ntStatus            = STATUS_UNSUCCESSFUL;
        IO_STATUS_BLOCK    IoStatusBlock       = { 0 };
        OBJECT_ATTRIBUTES  stObjAttribs        = { 0 };
        ULONG              ulAttributes        = OBJ_KERNEL_HANDLE; //| OBJ_EXCLUSIVE;
        ULONG              ulOpenOptions       = FILE_WRITE_THROUGH | FILE_SYNCHRONOUS_IO_NONALERT | FILE_SEQUENTIAL_ONLY | FILE_NON_DIRECTORY_FILE;
        KIRQL              CurrentIRQL         = KeGetCurrentIrql();
        PSIMDEV_EXTENTSION pSimDrvExtension    = NULL;
        HANDLE             deviceDirPathHandle = NULL;
        UNICODE_STRING     exProceedureName;
        NTSTATUS (*pfnIoGetDeviceDirectory)() = NULL;

        pSimDrvExtension = GetSimDrvExtension();
        if (NULL == pSimDrvExtension)
        {
            return bRet;
        }

        if (CurrentIRQL > PASSIVE_LEVEL)
        {
            break;
        }

        pstFileHandle->UnicodeString.Length = MAX_PATH_SIZE;
        pstFileHandle->UnicodeString.Buffer = ExAllocatePoolWithTag(NonPagedPool, MAX_PATH_SIZE, SIMDRV_ALLOC_TAG);

        if (pucFilePath)
        {
            // ntStatus = RtlAnsiStringToUnicodeString(&pstFileHandle->UnicodeString, pucFilePath, FALSE);
        }
        RtlInitUnicodeString(&exProceedureName, L"IoGetDeviceDirectory");
        pfnIoGetDeviceDirectory = MmGetSystemRoutineAddress(&exProceedureName);

        if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber) & (NULL != pfnIoGetDeviceDirectory))
        {
            ntStatus = pfnIoGetDeviceDirectory(pSimDrvExtension->pstPhysicalDeviceObject, DeviceDirectoryData, 0, NULL, &deviceDirPathHandle);
            if (!NT_SUCCESS(ntStatus))
            {
                GFXVALSIM_DBG_MSG("IoGetDeviceDirectory call failed!");
                return bRet;
            }
        }

        if (puwFilePath)
        {
            RtlInitUnicodeString(&pstFileHandle->UnicodeString, puwFilePath);
        }

        InitializeObjectAttributes(&stObjAttribs, &pstFileHandle->UnicodeString, ulAttributes, deviceDirPathHandle, NULL);

        switch (eMode)
        {
        case eReadBin:
            AccessMask |= FILE_READ_DATA;
            break;

        case eWriteBin:
            AccessMask |= FILE_WRITE_DATA;
            break;

        case eRWBin:
            AccessMask |= FILE_READ_DATA | FILE_WRITE_DATA;
            break;

        default:
            break;
        }

        ntStatus = ZwOpenFile(&pstFileHandle->hHandle, AccessMask, &stObjAttribs, &IoStatusBlock, 0, ulOpenOptions);

        if (ntStatus == STATUS_SUCCESS)
        {
            bRet = TRUE;
        }
        else
        {
            GFXVALSIM_DBG_MSG("ZwOpenFile call failed!");
        }
        if (deviceDirPathHandle)
        {
            ZwClose(deviceDirPathHandle);
        }

#endif

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PORTINGLAYER_FileRead(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucBuff, ULONG ulBuffSize, LONGLONG ullByteOffset, ULONG ulCount, PULONG pulBytesRead)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();
    do
    {
        if (NULL == pstFileHandle || NULL == pstFileHandle->hHandle)
        {
            break;
        }

#ifdef __USERMODE

        size_t errorVal0 = 0;
        size_t errorVal1 = 0;
        size_t errorVal2 = 0;

        _set_errno(0);
        sBytesRead = fread_s(pucBuff, ulBuffSize, ulElementSize, ulCount, pstFileHandle->fp);

        errorVal0 = errno;
        errorVal1 = feof(pstFileHandle->fp);
        errorVal2 = feof(pstFileHandle->fp);
#endif

#ifdef __KERNELMODE

        NTSTATUS        ntStatus      = STATUS_UNSUCCESSFUL;
        IO_STATUS_BLOCK IoStatusBlock = { 0 };
        KIRQL           CurrentIRQL   = KeGetCurrentIrql();
        LARGE_INTEGER   ByteOffset    = { 0 };

        if (CurrentIRQL != PASSIVE_LEVEL)
        {
            // ASSERT
        }

        ByteOffset.QuadPart = ullByteOffset;

        ntStatus = ZwReadFile(pstFileHandle->hHandle, NULL, NULL, NULL, &IoStatusBlock, pucBuff, ulBuffSize, &ByteOffset, NULL);

        if (ntStatus == STATUS_SUCCESS)
        {
            bRet = TRUE;
            if (pulBytesRead)
            {
                // This type conversation can lead to loss of data if file size if too big. size_t is of pointer size on a given platform
                *pulBytesRead = (ULONG)IoStatusBlock.Information;
            }
        }
        else
        {
            GFXVALSIM_DBG_MSG("ZwReadFile call failed!");
        }

#endif

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PORTINGLAYER_FileWrite(PDP_FILEHANDLLE pstFileHandle, PUCHAR pucWriteBuff, ULONG ulWriteLength, LONGLONG ullByteOffset)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();
    do
    {
        if (pstFileHandle == NULL || NULL == pstFileHandle->hHandle)
        {
            break;
        }

#ifdef __USERMODE

#endif

#ifdef __KERNELMODE

        NTSTATUS        ntStatus      = STATUS_UNSUCCESSFUL;
        IO_STATUS_BLOCK IoStatusBlock = { 0 };
        KIRQL           CurrentIRQL   = KeGetCurrentIrql();
        LARGE_INTEGER   ByteOffset    = { 0 };

        if (CurrentIRQL != PASSIVE_LEVEL)
        {
            // ASSERT
        }

        ByteOffset.QuadPart = ullByteOffset;

        ntStatus = ZwWriteFile(pstFileHandle->hHandle, NULL, NULL, NULL, &IoStatusBlock, pucWriteBuff, ulWriteLength, &ByteOffset, NULL);

        if (ntStatus == STATUS_SUCCESS)
        {
            if (IoStatusBlock.Information == ulWriteLength)
            {
                bRet = TRUE;
            }
            else
            {
                GFXVALSIM_DBG_MSG("ZwWriteFile call failed!");
            }
        }

#endif

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PORTINGLAYER_FileClose(PDP_FILEHANDLLE pstFileHandle)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstFileHandle == NULL)
        {
            break;
        }

#ifdef __USERMODE

        if (EOF == fclose(pstFileHandle->fp))
        {
            break;
        }

#endif

#ifdef __KERNELMODE

        if (STATUS_SUCCESS != ZwClose(pstFileHandle->hHandle))
        {
            break;
        }

#endif

        bRet = FALSE;

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_PrintMessage(ULONG ulDebugLevel, const char *DebugMessageFmt, ...)
{
    BOOLEAN bRet = FALSE;
    do
    {
#ifdef __USERMODE

#endif

#ifdef __KERNELMODE
#endif

    } while (FALSE);

    return bRet;
}

BOOLEAN PORTINGLAYER_IsFileOpen(PDP_FILEHANDLLE pstFileHandle)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstFileHandle == NULL)
        {
            break;
        }

#ifdef __USERMODE

        bRet = pstFileHandle->fp ? TRUE : FALSE;

#endif

#ifdef __KERNELMODE

        bRet = pstFileHandle->hHandle ? TRUE : FALSE;

#endif

    } while (FALSE);

    return bRet;
}

VOID PORTINGLAYER_GetPersistenceFilePath(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, WCHAR *filePath)
{
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    WCHAR              tempPath[MAX_PATH_STRING_LEN];

    pSimDrvExtension = GetSimDrvExtension();
    do
    {
        if (NULL == pSimDrvExtension || NULL == pGfxAdapterContext)
            break;

        memset(filePath, 0, MAX_PATH_STRING_LEN);
        memset(tempPath, 0, MAX_PATH_STRING_LEN);

        /* Return presistance file path with adapter context ex PCI&VEN_8086&DEV_0166&SUBSYS_21F917AA&REV_09_SimDrvPersistenceFile.txt */
        wcscpy(tempPath, pGfxAdapterContext->PCIBusDeviceId); /*Replacing ‘\’ charecter with ‘&’ in PCIBusDeviceId string.Since we cannot create a file which has ‘\’ charecter */
        REPLACE_CHARECTER(tempPath, L'\\', '&');
        wcscat_s(tempPath, MAX_PATH_STRING_LEN, PERISTENCE_FILE_NAME);

        if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber))
        {
            wcscpy(filePath, tempPath);
        }
        else
        {
            wcscpy(filePath, PERISTENCE_FILE_LOCATION);
            wcscat_s(filePath, MAX_PATH_STRING_LEN, tempPath);
        }

    } while (FALSE);
}