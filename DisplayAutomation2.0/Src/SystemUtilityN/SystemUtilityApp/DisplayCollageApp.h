#include "../SystemUtilityN/HeaderFiles/DisplayCollage.h"

#ifndef DISPLAY_COLLAGE_APP_H
#define DISPLAY_COLAAGE_APP_H

#pragma pack(push, DISPLAY_COLLAGE_APP_H)
#pragma pack(1)

typedef enum _REQUEST_TYPE
{
    GET_COLLAGE_CONFIG      = 0,
    IS_COLLAGE_POSSIBLE     = 1,
    ENABLE_COLLAGE_CONFIG   = 2,
    DISABLE_COLLAGE_CONFIG  = 3,
    GET_ENUMERATED_DISPLAYS = 4
} REQUEST_TYPE;

typedef HRESULT(__cdecl *PFN_GET_ENUMERATED_DISPLAYS)(PENUMERATED_DISPLAYS, HRESULT *);

// Collage Specific function pointers.
typedef HRESULT(__cdecl *PFN_DISABLE_COLLAGE_CONFIG)(PDISPLAY_AND_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_GET_COLLAGE_CONFIG)(PDISPLAY_AND_ADAPTER_INFO, PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS);
typedef HRESULT(__cdecl *PFN_ENABLE_COLLAGE_CONFIG)(PDISPLAY_AND_ADAPTER_INFO, PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS);
typedef HRESULT(__cdecl *PFN_IS_COLLAGE_POSSIBLE)(PDISPLAY_AND_ADAPTER_INFO, PDD_CUI_ESC_COLLAGE_TOPOLOGY, PBOOLEAN, PBOOLEAN);

PFN_GET_COLLAGE_CONFIG      pfnGetCollageConfig      = NULL;
PFN_IS_COLLAGE_POSSIBLE     pfnIsCollagePossible     = NULL;
PFN_ENABLE_COLLAGE_CONFIG   pfnEnableCollageConfig   = NULL;
PFN_DISABLE_COLLAGE_CONFIG  pfnDisableCollageConfig  = NULL;
PFN_GET_ENUMERATED_DISPLAYS pfnGetEnumeratedDisplays = NULL;

// Collage DLL functions
BOOLEAN DisableCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo);
BOOLEAN GetCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _Out_ PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS cConfigurationInfo);
BOOLEAN EnableCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _Inout_ PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS cConfigurationInfo);
BOOLEAN IsCollageConfigurationPossible(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _In_ PDD_CUI_ESC_COLLAGE_TOPOLOGY collageTopology, _Out_ PBOOLEAN isCollageSupported,
                                       _Out_ PBOOLEAN isCollageConfigPossible);

// DisplayConfig DLL functions
VOID GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode);

#pragma pack(pop, DISPLAY_COLLAGE_APP_H)
#endif // ! DISPLAY_COLLAGE_APP_H