#include <windows.h>
#include "DisplayCollageApp.h"

PVOID GetFunctionHandle(_In_ REQUEST_TYPE requestType)
{
    PVOID          functionPointer      = NULL;
    static HMODULE displayCollageHandle = NULL;
    static HMODULE displayConfigHandle  = NULL;

    if (NULL == displayCollageHandle)
    {
        displayCollageHandle = LoadLibraryA("../../../bin/SystemUtilityN.dll");

        if (NULL == displayCollageHandle)
            return NULL;
    }

    if (NULL == displayConfigHandle)
    {
        displayConfigHandle = LoadLibraryA("../../../bin/DisplayConfigN.dll");
        if (displayConfigHandle == NULL)
            return NULL;
    }

    switch (requestType)
    {
    case GET_COLLAGE_CONFIG:
        functionPointer =
        (pfnGetCollageConfig == NULL) ? pfnGetCollageConfig = (PFN_GET_COLLAGE_CONFIG)GetProcAddress(displayCollageHandle, "GetCollageConfiguration") : pfnGetCollageConfig;
        break;
    case IS_COLLAGE_POSSIBLE:
        functionPointer = (pfnIsCollagePossible == NULL) ? pfnIsCollagePossible = (PFN_IS_COLLAGE_POSSIBLE)GetProcAddress(displayCollageHandle, "IsCollageConfigurationPossible") :
                                                           pfnIsCollagePossible;
        break;
    case ENABLE_COLLAGE_CONFIG:
        functionPointer                          = (pfnEnableCollageConfig == NULL) ?
                          pfnEnableCollageConfig = (PFN_ENABLE_COLLAGE_CONFIG)GetProcAddress(displayCollageHandle, "EnableCollageConfiguration") :
                          pfnEnableCollageConfig;
        break;
    case DISABLE_COLLAGE_CONFIG:
        functionPointer                           = (pfnDisableCollageConfig == NULL) ?
                          pfnDisableCollageConfig = (PFN_DISABLE_COLLAGE_CONFIG)GetProcAddress(displayCollageHandle, "DisableCollageConfiguration") :
                          pfnDisableCollageConfig;
        break;
    case GET_ENUMERATED_DISPLAYS:
        functionPointer                            = (pfnGetEnumeratedDisplays == NULL) ?
                          pfnGetEnumeratedDisplays = (PFN_GET_ENUMERATED_DISPLAYS)GetProcAddress(displayConfigHandle, "GetEnumeratedDisplayInfo") :
                          pfnGetEnumeratedDisplays;
        break;
    default:
        break;
    }

    return functionPointer;
}

BOOLEAN GetCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _Out_ PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS cConfigurationInfo)
{
    printf("ENTRY: GetCollageConfiguration.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_GET_COLLAGE_CONFIG)GetFunctionHandle(GET_COLLAGE_CONFIG))
    {
        printf("Failed to get Collage Configuration handle.\n");
        return FALSE;
    }

    printf("EXIT: GetCollageConfiguration.\n");
    return (pfnGetCollageConfig)(pdisplayAdapterInfo, cConfigurationInfo);
}

BOOLEAN IsCollageConfigurationPossible(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _In_ PDD_CUI_ESC_COLLAGE_TOPOLOGY collageTopology, _Out_ PBOOLEAN isCollageSupported,
                                       _Out_ PBOOLEAN isCollageConfigPossible)
{
    printf("ENTRY: IsCollageConfigurationPossible.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_IS_COLLAGE_POSSIBLE)GetFunctionHandle(IS_COLLAGE_POSSIBLE))
    {
        printf("Failed to get IsCollageConfigurationPossible handle.\n");
        return FALSE;
    }

    printf("EXIT: IsCollageConfigurationPossible.\n");
    return (pfnIsCollagePossible)(pdisplayAdapterInfo, collageTopology, isCollageSupported, isCollageConfigPossible);
}

BOOLEAN EnableCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _Inout_ PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS cConfigurationInfo)
{
    printf("ENTRY: EnableCollageConfiguration.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_ENABLE_COLLAGE_CONFIG)GetFunctionHandle(ENABLE_COLLAGE_CONFIG))
    {
        printf("Failed to get Enable Collage Configuration Handle.\n");
        return FALSE;
    }

    printf("EXIT: EnableCollageConfiguration.\n");
    return (pfnEnableCollageConfig)(pdisplayAdapterInfo, cConfigurationInfo);
}

BOOLEAN DisableCollageConfiguration(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo)
{
    printf("ENTRY: DisableCollageConfiguration.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_DISABLE_COLLAGE_CONFIG)GetFunctionHandle(DISABLE_COLLAGE_CONFIG))
    {
        printf("Failed to get Disable Collage Configuration Handle.\n");
        return FALSE;
    }

    printf("EXIT: DisableCollageConfiguration.\n");
    return (pfnDisableCollageConfig)(pdisplayAdapterInfo);
}

VOID GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode)
{
    printf("ENTRY: GetEnumeratedDisplayInfo.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_GET_ENUMERATED_DISPLAYS)GetFunctionHandle(GET_ENUMERATED_DISPLAYS))
    {
        printf("Failed to get Enumerated Display Handle.\n");
    }

    printf("EXIT: GetEnumeratedDisplayInfo.\n");
    (pfnGetEnumeratedDisplays)(pEnumDisplay, pErrorCode);
}

int main(int argc, _TCHAR *argv[])
{
    DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS collageConfiguration;
    ZeroMemory(&collageConfiguration, sizeof(DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS));

    DD_CUI_ESC_COLLAGE_TOPOLOGY collageTopology;
    ZeroMemory(&collageTopology, sizeof(DD_CUI_ESC_COLLAGE_TOPOLOGY));

    BOOLEAN isCollageSupported      = FALSE;
    BOOLEAN isCollageConfigPossible = FALSE;

    ENUMERATED_DISPLAYS enumDisplay;
    ZeroMemory(&enumDisplay, sizeof(ENUMERATED_DISPLAYS));
    enumDisplay.Size = sizeof(ENUMERATED_DISPLAYS);

    HRESULT          errorCode;
    REQUEST_TYPE     requestType = IS_COLLAGE_POSSIBLE;
    CUI_COLLAGE_TYPE collageType = CUI_COLLAGE_TYPE_HORIZONTAL;
    BOOLEAN          toStop      = 0;

    do
    {
        switch (requestType)
        {
        case GET_COLLAGE_CONFIG:
            GetEnumeratedDisplayInfo(&enumDisplay, &errorCode);
            if (GetCollageConfiguration(&enumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, &collageConfiguration))
            {
                printf("SUCCESS: GetCollageConfiguration.");
            }
            break;
        case IS_COLLAGE_POSSIBLE:
            // For Horizontal collage.
            GetEnumeratedDisplayInfo(&enumDisplay, &errorCode);
            if (errorCode == S_OK)
            {
                printf("SUCCESS: GetEnumeratedDisplayInfo.\n");
                for (int i = 0, j = 0; i < enumDisplay.Count; ++i)
                {
                    if (enumDisplay.ConnectedDisplays[i].ConnectorNPortType != DP_A)
                    {
                        collageTopology.CollageChildInfo[j].ChildId = enumDisplay.ConnectedDisplays[i].TargetID;
                        switch (collageType)
                        {
                        case CUI_COLLAGE_TYPE_HORIZONTAL:
                            collageTopology.CollageChildInfo[j].HTileLocation = j;
                            collageTopology.CollageChildInfo[j].VTileLocation = 0;
                            collageTopology.TotalNumberOfHTiles               = j + 1;
                            collageTopology.TotalNumberOfVTiles               = 1;

                            break;
                        case CUI_COLLAGE_TYPE_VERTICAL:
                            collageTopology.CollageChildInfo[j].HTileLocation = 0;
                            collageTopology.CollageChildInfo[j].VTileLocation = j;
                            collageTopology.TotalNumberOfHTiles               = 1;
                            collageTopology.TotalNumberOfVTiles               = j + 1;
                            break;
                        default:
                            break;
                        }
                        ++j;
                    }
                }
                if (IsCollageConfigurationPossible(&enumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, &collageTopology, &isCollageSupported, &isCollageConfigPossible))
                {
                    printf("SUCCESS: IsCollageConfigurationPossible.\n");
                    printf("IsCollageSupported: %d\n", isCollageSupported);
                    printf("IsCollagePossible:%d\n", isCollageConfigPossible);
                }
            }
            break;
        case ENABLE_COLLAGE_CONFIG:
            GetEnumeratedDisplayInfo(&enumDisplay, &errorCode);
            if (errorCode == S_OK)
            {
                printf("SUCCESS: GetEnumeratedDisplayInfo.\n");
                for (int i = 0, j = 0; i < enumDisplay.Count; ++i)
                {
                    if (enumDisplay.ConnectedDisplays[i].ConnectorNPortType != DP_A)
                    {
                        collageTopology.CollageChildInfo[j].ChildId = enumDisplay.ConnectedDisplays[i].TargetID;
                        switch (collageType)
                        {
                        case CUI_COLLAGE_TYPE_HORIZONTAL:
                            collageTopology.CollageChildInfo[j].HTileLocation = j;
                            collageTopology.CollageChildInfo[j].VTileLocation = 0;
                            collageTopology.TotalNumberOfHTiles               = j + 1;
                            collageTopology.TotalNumberOfVTiles               = 1;
                            break;
                        case CUI_COLLAGE_TYPE_VERTICAL:
                            collageTopology.CollageChildInfo[j].HTileLocation = 0;
                            collageTopology.CollageChildInfo[j].VTileLocation = j;
                            collageTopology.TotalNumberOfHTiles               = 1;
                            collageTopology.TotalNumberOfVTiles               = j + 1;
                            break;
                        default:
                            break;
                        }
                        ++j;
                    }
                }
                memcpy(&collageConfiguration.CollageTopology, &collageTopology, sizeof(collageTopology));
                if (EnableCollageConfiguration(&enumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, &collageConfiguration))
                {
                    printf("SUCCESS: EnableCollageConfiguration.\n");
                }
            }
            break;
        case DISABLE_COLLAGE_CONFIG:
            if (DisableCollageConfiguration(&enumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo))
            {
                printf("SUCCESS: DisableCollageConfiguration.\n");
            }
            break;
        case GET_ENUMERATED_DISPLAYS:
            GetEnumeratedDisplayInfo(&enumDisplay, &errorCode);
            if (errorCode == S_OK)
            {
                for (int i = 0; i < enumDisplay.Count; ++i)
                {
                    enumDisplay.ConnectedDisplays[i].TargetID;
                }
            }
            break;
        }
    } while (toStop);
    getchar();
    return 0;
}