/*===========================================================================
; ETWLogging.c - ETW and Console logging layer implementation
;----------------------------------------------------------------------------
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
;
;   File Description:
;       ETW and Console logging layer implementation
;
;   Revision History:
;--------------------------------------------------------------------------*/
#include "..\CommonInclude\ETWLogging.h"
#include "..\DriverInterfaces\SimDriver.h"
#include "..\VBTSimulation\VBTSimulation.h"
#define DELAY_ONE_MICROSECOND (-10)
#define DELAY_ONE_MILLISECOND (DELAY_ONE_MICROSECOND * 1000)

typedef enum _FUNCTION_STAGE
{
    FUNCTION_ENTRY = 0,
    FUNCTION_EXIT
} FUNCTION_STAGE;

#define LOG_MAX_BUFFER 512

/***********************************************************************************/
/*                    Logging Layer services                                    */
/***********************************************************************************/

/**
 *Redirects the Log messages to the ETL and the console
 *
 *@param[in]     Level           Debug message level from Critical to Verbose
 *@param[in]     Function        Function which generated this message
 *@param[in]     Line            Line no at which the message was generated
 *@param[in]     MessageFormat   Message Format
 *@return    Appropriate NTSTATUS value
 */
void LOG_DebugMessage(IN IN const char *Function, IN UINT32 Line, const char *DebugMessageFmt, ...)
{
    NTSTATUS Status                      = 0;
    char     PrintBuffer[LOG_MAX_BUFFER] = { 0 };
    va_list  ArgList;
    va_start(ArgList, DebugMessageFmt);

    // replaced strsafe functions with RTL* functions because of a compiler crash while compiling with static analysis option
    Status = RtlStringCchVPrintfA((LPTSTR)PrintBuffer, LOG_MAX_BUFFER, (LPCTSTR)DebugMessageFmt, ArgList);
    if (0 == Status)
    {
        EventWriteDebugPrint_Info(NULL, PrintBuffer, Function, Line);
        // forward the debug message to the console as well

        // DbgPrint("%s:: %s", Function, PrintBuffer);
    }
    va_end(ArgList);

    return;
}

/**
 *Adds Function Entry messages to the ETL and the console
 *
 *@param[in]     Function        Function which generated this message
 *@param[in]     Status          Return Status of the Function
 *@return    Appropriate NTSTATUS value
 */
void LOG_FunctionEntry(IN const char *Function, IN UINT32 Status)
{
    // ETL
    EventWriteFunctionTrack_Info(NULL, Function, FUNCTION_ENTRY, Status);
    // Console
    // DbgPrint(" --> Function Entry : %s \r\n", Function);
}

/**
 *Adds Function Exit messages to the ETL and the console
 *
 *@param[in]     Function        Function which generated this message
 *@param[in]     Status          Return Status of the Function
 *@return    Appropriate NTSTATUS value
 */
void LOG_FunctionExit(IN const char *Function, IN UINT32 Status)
{
    // ETL
    EventWriteFunctionTrack_Info(NULL, Function, FUNCTION_EXIT, Status);
    // Increase the criticality if the function failed

    // DbgPrint("<-- Function Exit : %s with Success Code %d. \r\n", Function, Status);
}

/**
 *Dumps the structure to the ETL
 *
 *@param[in]     Function        Function which generated this message
 *@param[in]     Structure       Name of the Structure getting dumped
 *@param[in]     Size            Size of the Structure getting dumped
 *@param[in]     Data            Data of the Structure getting dumped
 *@param[in]     Message         Any Message which needs to be added with this dump
 *@return    Appropriate NTSTATUS value
 */
void LOG_StructureDump(IN const char *Function, IN UINT32 Line, IN const char *StructureName, IN UINT32 Size, IN unsigned char *Data, IN const char *Message)
{
    // ETL
    EventWriteStructureDump_Info(NULL, StructureName, Size, Data, Message, Function, Line);
}

NTSTATUS GfxMarkTraceStart(IN PDRIVER_OBJECT pHwDevExt, IN void *pArgs)
{
    NTSTATUS Status = STATUS_SUCCESS;
    VBTSIMULATION_DumpVBTToETW();
    return Status;
}

NTSTATUS
OsFreeIoWorkItem(IN PIO_WORKITEM pIoWorkItem)
{
    NTSTATUS Status = STATUS_INVALID_PARAMETER;
    if (pIoWorkItem == NULL)
    {
        return Status;
    }

    IoFreeWorkItem(pIoWorkItem);

    Status = STATUS_SUCCESS;
    return Status;
}

ULONG GfxGenericProcessWorkItem(IN PVOID pDeviceObject, IN PGENERIC_WORKITEM_ARGS pGenericWorkItemArgs)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    NTSTATUS          Status        = STATUS_INVALID_PARAMETER;

    if (pGenericWorkItemArgs)
    {
        // Here call the function of interest
        if (pGenericWorkItemArgs->pfnFunc(pGenericWorkItemArgs->pHwDev, pGenericWorkItemArgs->pfnArgs) != 0)
        {
            GFXVALSIM_DBG_MSG("Error Msg");
        }

        // Free up the work item allocated
        OsFreeIoWorkItem(pGenericWorkItemArgs->pWorkItem);
        // Now free up generic arguments (never in stack)
        if (NULL != pGenericWorkItemArgs->pfnArgs)
        {
            pstPortingObj->pfnFreeMem(pGenericWorkItemArgs->pfnArgs);
        }
        // Now free up generic work item struct
        pstPortingObj->pfnFreeMem(pGenericWorkItemArgs);
    }

    Status = STATUS_SUCCESS;
    return Status;
}

NTSTATUS GfxGenericQueueWorkItem(IN PDRIVER_OBJECT pHwDev, IN PGENERIC_QUEUE_WORKITEM_ARGS pQueueWorkItemArgs)
{
    GFXVALSIM_FUNC_ENTRY();
    NTSTATUS               ntStatus             = STATUS_UNSUCCESSFUL;
    PGENERIC_WORKITEM_ARGS pGenericWorkItemArgs = NULL;
    PPORTINGLAYER_OBJ      pstPortingObj        = GetPortingObj();
    KIRQL                  CurrentIrql          = KeGetCurrentIrql();
    do
    {
        if (CurrentIrql > DISPATCH_LEVEL)
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        else
        {
            pGenericWorkItemArgs = pstPortingObj->pfnAllocateMem(sizeof(GENERIC_WORKITEM_ARGS), TRUE);

            if (pGenericWorkItemArgs)
            {
                if (pQueueWorkItemArgs->ulArgSize)
                {
                    pGenericWorkItemArgs->pfnArgs = pstPortingObj->pfnAllocateMem(pQueueWorkItemArgs->ulArgSize, TRUE);
                    if (NULL == pQueueWorkItemArgs->pfnArgs)
                    {
                        ntStatus = STATUS_UNSUCCESSFUL;
                        break;
                    }
                }
                pGenericWorkItemArgs->pHwDev  = pHwDev;
                pGenericWorkItemArgs->pfnFunc = pQueueWorkItemArgs->pfnFunc;
                if (pQueueWorkItemArgs->ulArgSize && NULL != pGenericWorkItemArgs->pfnArgs)
                {
                    if (0 != memcpy_s(pGenericWorkItemArgs->pfnArgs, pQueueWorkItemArgs->ulArgSize, pQueueWorkItemArgs->pfnArgs, pQueueWorkItemArgs->ulArgSize))
                    {
                        ntStatus = STATUS_INVALID_PARAMETER;
                        break;
                    }
                    pGenericWorkItemArgs->ulArgSize = pQueueWorkItemArgs->ulArgSize;
                }
                pGenericWorkItemArgs->pWorkItem = IoAllocateWorkItem(pHwDev->DeviceObject);
                if (NULL != pGenericWorkItemArgs->pWorkItem)
                {
                    // Insert work item into work queue
                    IoQueueWorkItem(pGenericWorkItemArgs->pWorkItem, GfxGenericProcessWorkItem, DelayedWorkQueue, (PVOID)pGenericWorkItemArgs);
                    ntStatus = STATUS_SUCCESS;
                }
            }
        }
    } while (FALSE);
    GFXVALSIM_FUNC_EXIT((ntStatus == STATUS_SUCCESS) ? 0 : 1);
    return ntStatus;
}

DECLSPEC_NOINLINE
void __stdcall GfxMcGenControlCallbackV2(_In_ LPCGUID SourceId, _In_ ULONG ControlCode, _In_ UCHAR Level, _In_ ULONGLONG MatchAnyKeyword, _In_ ULONGLONG MatchAllKeyword,
                                         _In_opt_ PEVENT_FILTER_DESCRIPTOR FilterData, _Inout_opt_ void *CallbackContext)
{
    NTSTATUS NtStatus;

    PDRIVER_OBJECT pHwDev    = (PDRIVER_OBJECT)CallbackContext;
    BOOLEAN        IsEnabled = FALSE;
    switch (ControlCode)
    {
    case EVENT_CONTROL_CODE_ENABLE_PROVIDER:
        if (MatchAnyKeyword & 0x7FFFFFFF)
        {
            IsEnabled = TRUE;
        }
        break;

    case EVENT_CONTROL_CODE_DISABLE_PROVIDER:
        IsEnabled = FALSE;
        break;

    default:
        break;
    }

    if (IsEnabled)
    {
        GENERIC_QUEUE_WORKITEM_ARGS WorkItemArgs;
        WorkItemArgs.pfnFunc   = GfxMarkTraceStart;
        WorkItemArgs.pfnArgs   = &Level;
        WorkItemArgs.ulArgSize = sizeof(Level);
        NtStatus               = GfxGenericQueueWorkItem(pHwDev, &WorkItemArgs);
    }

    return;
}