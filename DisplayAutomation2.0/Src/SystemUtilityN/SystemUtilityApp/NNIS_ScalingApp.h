#include "../SystemUtilityN/HeaderFiles/NNIS_Scalar.h"

#ifndef NNIS_SCALING_APP_H
#define NNIS_SCALING_APP_H

#pragma pack(push, NNIS_SCALING_APP_H)
#pragma pack(1)

typedef enum _REQUEST_TYPES
{
    IS_NNIS_SCALING_POSSIBLE      = 0,
	ENABLE_DISABLE_NNIS_SCALING   = 1,
	GET_CURRENT_NNISSCALING_STATE = 2,
	ADD_CUSTOM_MODE                = 3,
	GET_ENUMERATE_DISPLAYS         = 4
} REQUEST_TYPE;

// function pointers.
typedef HRESULT(__cdecl *PFN_GET_ENUMERATE_DISPLAYS)(PENUMERATED_DISPLAYS, HRESULT *);
typedef HRESULT(__cdecl *PFN_IS_NNIS_SCALING_SUPPORTED)(PDISPLAY_AND_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_EN_DS_NNIS_SCALING_STATE)(PDISPLAY_AND_ADAPTER_INFO,UINT);
typedef HRESULT(__cdecl *PFN_GET_CURRENT_NNIS_SCALING_STATE)(PDISPLAY_AND_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_ADD_CUSTOM_MODE)(PDISPLAY_AND_ADAPTER_INFO,ULONG,ULONG);

PFN_GET_ENUMERATE_DISPLAYS       pfnGetEnumerateDisplays = NULL;
PFN_IS_NNIS_SCALING_SUPPORTED      pfnNNISScalingSupported   = NULL;
PFN_EN_DS_NNIS_SCALING_STATE       pfnEnDsNNISScalingState   = NULL;
PFN_GET_CURRENT_NNIS_SCALING_STATE pfnGetCurrentNNISState = NULL;
PFN_ADD_CUSTOM_MODE                 pfnAddCustomMode = NULL;

// DLL functions
BOOLEAN IsNNISScalingSupport(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo);
BOOLEAN EnDsNNISScalingState(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _In_ UINT state);
UINT CurrentNNISScalingState(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo);
BOOLEAN Add_Custom_Mode(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _In_ ULONG Hz, _In_ ULONG Vt);

// DisplayConfig DLL functions
VOID GetEnumerateDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode);

#pragma pack(pop, NNIS_SCALING_APP_H)
#endif // ! NNIS_SCALING_APP_H