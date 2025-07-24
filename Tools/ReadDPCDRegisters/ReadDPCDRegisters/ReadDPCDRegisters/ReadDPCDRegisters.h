/* DLL's header include*/
#pragma once

/* System header(s) */
#include <windows.h>

/* Constants*/
#define MAX_DISPLAYS	16

typedef enum _CONNECTOR_PORT_TYPE
{
	DispNone = 0,
	DP_A,
	MIPI_DSI_0,
	MIPI_DSI_1,
	CRT,
	DP_B,
	DP_C,
	DP_D,
	DP_E,
	DP_F,
	DP_TYPE_C_B,
	DP_TYPE_C_C,
	DP_TYPE_C_D,
	DP_TYPE_C_E,
	DP_TYPE_C_F,
	DP_TBT_B,
	DP_TBT_C,
	DP_TBT_D,
	DP_TBT_E,
	DP_TBT_F,
	HDMI_B,
	HDMI_C,
	HDMI_D,
	HDMI_E,
	HDMI_F,
	DVI_B,
	DVI_C,
	DVI_D,
	DVI_E,
	DVI_F,
	VirtualDisplay,
	WIDI,
	WD_0,
	WD_1
}CONNECTOR_PORT_TYPE;

/* Contains enumerated display specific */
typedef struct _DISPLAY_INFO
{
	_Out_ CONNECTOR_PORT_TYPE		ConnectorNPortType;							/**< Connected Display Type (EDP/DP/HDMI)*/
	_Out_ UINT						TargetID;									/**< Windows monitor ID*/
	_Out_ CHAR						FriendlyDeviceName[128];					/**< Display Name (eg Digital Display / Built-in Display)*/
	_Out_ BOOLEAN					IsActive;									/**< Display device is active or not */
}DISPLAY_INFO, *PDISPLAY_INFO;

/* Contains enumerated display details*/
typedef struct _ENUMERATED_DISPLAYS
{
	_In_  INT							Size;									/**< Size of ENUMERATED_DISPLAYS*/
	_Out_ DISPLAY_INFO				ConnectedDisplays[MAX_DISPLAYS];			/**< Connected Display List*/
	_Out_ INT							Count;									/**< No of connected display (active or inactive)*/
}ENUMERATED_DISPLAYS, *PENUMERATED_DISPLAYS;

/* Exposed API function pointers of SystemUtility DLL*/
typedef HRESULT(__cdecl *PFN_EDISPLAY_INFO_ADD)(PENUMERATED_DISPLAYS, HRESULT*);
typedef bool(__cdecl *PFN_DPCDREAD)(ULONG ulStartOffset, UINT targetID, ULONG ulDpcdBuffer[], UINT dpcdBufferSize);

/* Helper function to call the exposed APIs*/
HMODULE LoadSystemUtilityDLL();
HMODULE LoadDispConfDLL();
void ReadDPCDRegisters();



