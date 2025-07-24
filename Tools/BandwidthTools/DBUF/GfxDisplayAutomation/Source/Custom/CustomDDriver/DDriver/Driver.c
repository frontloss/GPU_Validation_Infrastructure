#include <ntddk.h>
#include <wdf.h>

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject, PUNICODE_STRING pRegistryPath){
	NTSTATUS status = STATUS_SUCCESS;
	
	DbgPrint("DDriver:: DriverEntry Call\n");
	UNREFERENCED_PARAMETER(pDriverObject);
	UNREFERENCED_PARAMETER(pRegistryPath);
	
	KeBugCheck(MANUALLY_INITIATED_CRASH);
	
	return status;
}