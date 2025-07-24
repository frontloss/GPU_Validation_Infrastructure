#pragma once

#ifdef __KERNELMODE
#include "wdm.h"
#include <ntstrsafe.h>
#else
#include "Windows.h"
#endif // __KERNELMODE

#include "IntelGfxValSimCrimson.h"

#define VALSIMDBG_OFF (0x00000000)
#define VALSIMDBG_CRITICAL (0x00000001)
#define VALSIMDBG_NORMAL (0x00000002)
#define VALSIMDBG_VERBOSE (0x00000004)
#define VALSIMDBG_FUNCTION (0x80000000)
#define VALSIMDBG_NONCRITICAL (0x00000010)
#define VALSIMDBG_CRITICAL_DEBUG (0x00000020)
#define VALSIMDBG_VERBOSE_VERBOSITY (0x00000040)
#define VALSIMDBG_PROTOCAL (0x00000100)

typedef ULONG (*PGENERIC_GFXFUNCTION)(PDRIVER_OBJECT, PVOID);

typedef struct _GENERIC_WORKITEM_ARGS
{
    // Work item object
    PIO_WORKITEM pWorkItem;

    // Device extention
    PDRIVER_OBJECT pHwDev;

    // Function & arguments to be called from within the work item
    PGENERIC_GFXFUNCTION pfnFunc;
    PVOID                pfnArgs; // Note: Should not be a variable in stack, should be NON_PAGED
    ULONG                ulArgSize;
} GENERIC_WORKITEM_ARGS, *PGENERIC_WORKITEM_ARGS;

typedef struct _GENERIC_QUEUE_WORKITEM_ARGS
{
    // Function & arguments to be called from within the work item
    PGENERIC_GFXFUNCTION pfnFunc;
    PVOID                pfnArgs;
    ULONG                ulArgSize;
} GENERIC_QUEUE_WORKITEM_ARGS, *PGENERIC_QUEUE_WORKITEM_ARGS;

NTSTATUS GfxMarkTraceStart(IN PDRIVER_OBJECT pHwDevExt, IN void *pArgs);

NTSTATUS GfxGenericQueueWorkItem(PDRIVER_OBJECT pHwDev, PGENERIC_QUEUE_WORKITEM_ARGS pQueueWorkItemArgs);

// General Logging functions
void LOG_DebugMessage(IN const char *Function, IN UINT32 Line, IN const char *DebugMessageFmt, ...);

// Function Entry Exit logging
void LOG_FunctionEntry(IN const char *Function, IN UINT32 Status);

void LOG_FunctionExit(IN const char *Function, IN UINT32 Status);

void LOG_StructureDump(IN const char *Function, IN UINT32 Line, IN const char *StructureName, IN UINT32 Size, IN unsigned char *Data, IN const char *Message);

EXTERN_C __declspec(selectany) REGHANDLE Intel_Gfx_ValSimDiverTrackingHandle = (REGHANDLE)0;

DECLSPEC_NOINLINE // __inline
void __stdcall GfxMcGenControlCallbackV2(_In_ LPCGUID SourceId, _In_ ULONG ControlCode, _In_ UCHAR Level, _In_ ULONGLONG MatchAnyKeyword, _In_ ULONGLONG MatchAllKeyword,
                                         _In_opt_ PEVENT_FILTER_DESCRIPTOR FilterData, _Inout_opt_ void *CallbackContext);

#define GFXVALSIM_DBG_MSG(DebugMessageFmt, ...) LOG_DebugMessage(__FUNCTION__, __LINE__, DebugMessageFmt, __VA_ARGS__)
#define GFXVALSIM_FUNC_ENTRY() LOG_FunctionEntry(__FUNCTION__, 0)
#define GFXVALSIM_FUNC_EXIT(Status) LOG_FunctionExit(__FUNCTION__, Status)
#define GFXVALSIM_STRUCT_DUMP(StructureName, Data, Message) LOG_StructureDump(__FUNCTION__, __LINE__, #StructureName, sizeof(StructureName), (UCHAR *)Data, Message)
#define GFXVALSIM_HPD_MSG(Port, Attach, Event, portconnector) EventWriteHPD_info(NULL, Port, Attach, Event, portconnector)
#define GFXVALSIM_VBT_MSG(TotalSize, HeaderSize, FooterSize, size, data, headerdata) EventWriteVbtDump_Info(NULL, TotalSize, HeaderSize, FooterSize, size, data, headerdata)
#define GFXVALSIM_AUXCTRL_REG(port, aux_ctl_reg) EventWriteAuxInterface_CtrlReg(NULL, port, aux_ctl_reg)
#define GFXVALSIM_GMBUS_STATE(currentstate, nextstate) EventWriteGmbus_State(NULL, currentstate, nextstate)
#define GFXVALSIM_AUX_READ(DPCDAddr, ReadLength, DPCDReadBuff) EventWriteAux_Read(NULL, DPCDAddr, ReadLength, DPCDReadBuff)
#define GFXVALSIM_AUX_WRITE(DPCDAddr, ReadLength, DPCDReadBuff) EventWriteAux_Write(NULL, DPCDAddr, ReadLength, DPCDReadBuff)

#define GFXVALSIM_SB_READ(size, data, status) EventWriteSdeband_MST_Info(NULL, size, data, status, __FUNCTION__)
#define GFXVALSIM_HPDSTATUS(platform, Offset, Value, Offset_1, Value_1, Offset_2, Value_2, Offset_3, Value_3) \
    EventWriteHpdEnableStatus_Info(NULL, platform, Offset, Value, Offset_1, Value_1, Offset_2, Value_2, Offset_3, Value_3)

#define GFXVALSIM_PCI_CONFIG_DATA(offset, size, PciConfigData) EventWritePciConfig_Info(NULL, offset, size, PciConfigData)

#define GFXVALSIM_SYSTEM_INFO(platform, pch) EventWriteSystemDetails(NULL, platform, pch)

#define GFXVALSIM_GFX_POWER_STATE_NOTIFICATION(Platform, Device_power_state, Power_Action) EventWritePowerState_info(NULL, Platform, Device_power_state, Power_Action)
#define LOG_MMIO_READ(RegOffset, RegValue, platform) EventWriteValSim_MMIO_Read(NULL, RegOffset, RegValue, platform)
#define LOG_MMIO_WRITE(RegOffset, RegValue, platform) EventWriteValSim_MMIO_Write(NULL, RegOffset, RegValue, platform)

#define LOG_GMBUS_READ(RegOffset, RegValue) EventWriteI2CAux_Read(NULL, RegOffset, RegValue)
#define LOG_GMBUS_WRITE(RegOffset, RegValue) EventWriteI2CAux_Write(NULL, RegOffset, RegValue)
#define LOG_SYSTEM_DETAILS(Platform, pch, Size, VbtData) EventWriteSystem_Details_Task(NULL, Platform, pch, Size, VbtData)
#define LOG_VALSIM_DPCD(Offset, Value, Result) EventWriteValsim_DPCD(NULL, Offset, Value, Result)
/* Test ETL Event Start */
#define LOG_MEDIA_ACTION(TargetId, Operation) EventWriteMediaAction(NULL, TargetId, Operation)
/* Test ETL Event End */
