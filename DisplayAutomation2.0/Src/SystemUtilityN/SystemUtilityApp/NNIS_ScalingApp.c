#include <windows.h>
#include "NNIS_ScalingApp.h"

PVOID GetFunctionsHandle(_In_ REQUEST_TYPE requestType)
{
    PVOID          functionPointer      = NULL;
    static HMODULE NNscalingHandle = NULL;
    static HMODULE ConfigHandle  = NULL;

    if (NULL == NNscalingHandle)
    {
        NNscalingHandle = LoadLibraryA("../../../bin/SystemUtilityN.dll");

        if (NULL == NNscalingHandle)
            return NULL;
    }

    if (NULL == ConfigHandle)
    {
        ConfigHandle = LoadLibraryA("../../../bin/DisplayConfigN.dll");
        if (ConfigHandle == NULL)
            return NULL;
    }

    switch (requestType)
    {
    case IS_NNIS_SCALING_POSSIBLE:
        functionPointer =
        (pfnNNISScalingSupported == NULL) ? pfnNNISScalingSupported = (PFN_IS_NNIS_SCALING_SUPPORTED)GetProcAddress(NNscalingHandle, "Is_NNIS_ScalingSupported") : pfnNNISScalingSupported;
        break;
	case ENABLE_DISABLE_NNIS_SCALING:
        functionPointer =
        (pfnEnDsNNISScalingState == NULL) ? pfnEnDsNNISScalingState = (PFN_EN_DS_NNIS_SCALING_STATE)GetProcAddress(NNscalingHandle, "EnableDisableNNISScalingState") : pfnEnDsNNISScalingState;
        break;
	case GET_CURRENT_NNISSCALING_STATE:
        functionPointer =
        (pfnGetCurrentNNISState == NULL) ? pfnGetCurrentNNISState = (PFN_GET_CURRENT_NNIS_SCALING_STATE)GetProcAddress(NNscalingHandle, "GetCurrentNNISScalingState") : pfnGetCurrentNNISState;
        break;
	case ADD_CUSTOM_MODE:
        functionPointer =
        (pfnAddCustomMode == NULL) ? pfnAddCustomMode = (PFN_ADD_CUSTOM_MODE)GetProcAddress(NNscalingHandle, "AddCustomMode") : pfnAddCustomMode;
        break;
    case GET_ENUMERATE_DISPLAYS:
        functionPointer                            = (pfnGetEnumerateDisplays == NULL) ?
                          pfnGetEnumerateDisplays = (PFN_GET_ENUMERATE_DISPLAYS)GetProcAddress(ConfigHandle, "GetEnumerateDisplayInfo") :
                          pfnGetEnumerateDisplays;
        break;
    default:
		functionPointer = NULL;
        break;
    }

    return functionPointer;
}

BOOLEAN EnDsNNISScalingState(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo, _In_ UINT state)
{
	printf("ENTRY: EnDsNNISScalingState.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_EN_DS_NNIS_SCALING_STATE)GetFunctionsHandle(ENABLE_DISABLE_NNIS_SCALING))
    {
        printf("Failed to get function handle- EnableDisableNNISScalingState.\n");
        return FALSE;
    }

    printf("EXIT: EnDsNNISScalingState.\n");
    return (pfnEnDsNNISScalingState)(pdisplayAdapterInfo, state);

}

BOOLEAN IsNNISscalingSupport(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo)
{
    printf("ENTRY: IsNNISscalingSupport.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_IS_NNIS_SCALING_SUPPORTED)GetFunctionsHandle(IS_NNIS_SCALING_POSSIBLE))
    {
        printf("Failed to get function handle- Is_NNIS_ScalingSupported.\n");
        return FALSE;
    }

    printf("EXIT: IsNNISScalingSupport.\n");
    return (pfnNNISScalingSupported)(pdisplayAdapterInfo);
}

UINT CurrentNNISScalingState(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo)
{
    printf("ENTRY: CurrentNNISScalingState.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_GET_CURRENT_NNIS_SCALING_STATE)GetFunctionsHandle(GET_CURRENT_NNISSCALING_STATE))
    {
        printf("Failed to get function handle- Is_NN_IS_ScalingSupported.\n");
        return FALSE;
    }

    printf("EXIT: CurrentNNISScalingState.\n");
    return (pfnGetCurrentNNISState)(pdisplayAdapterInfo);
}

VOID GetEnumerateDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode)
{
    printf("ENTRY: GetEnumerateDisplayInfo.\n");
    BOOLEAN isSuccess = FALSE;

    if (NULL == (PFN_GET_ENUMERATE_DISPLAYS)GetFunctionsHandle(GET_ENUMERATE_DISPLAYS))
    {
        printf("Failed to get Enumerate Display Handle.\n");
    }

    printf("EXIT: GetEnumerateDisplayInfo.\n");
    (pfnGetEnumerateDisplays)(pEnumDisplay, pErrorCode);
}

BOOLEAN Add_Custom_Mode(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayAdapterInfo,_In_ ULONG Hz, _In_ ULONG Vt)
{
    printf("ENTRY: AddCustomMode.\n");
    
    if (NULL == (PFN_ADD_CUSTOM_MODE)GetFunctionsHandle(ADD_CUSTOM_MODE))
    {
        printf("Failed to get function handle- AddCustomMode.\n");
        return FALSE;
    }

    printf("EXIT: AddCustomMode.\n");
    return (pfnAddCustomMode)(pdisplayAdapterInfo, Hz, Vt);
}


/*int main(int argc, _TCHAR *argv[])
{
    DD_CUI_ESC_GET_SET_NN_ARGS cGetSetArgs;
    ZeroMemory(&cGetSetArgs, sizeof(DD_CUI_ESC_GET_SET_NN_ARGS));

    BOOLEAN isNNscalingSupported      = FALSE;
    
    ENUMERATED_DISPLAYS enumDisplay;
    ZeroMemory(&enumDisplay, sizeof(ENUMERATED_DISPLAYS));
    enumDisplay.Size = sizeof(ENUMERATED_DISPLAYS);
    HRESULT          errorCode;

	GetEnumerateDisplayInfo(&enumDisplay, &errorCode);
    if (IsNNscalingSupport(&enumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo))
    {
		printf("SUCCESS: GetCollageConfiguration.");
    }
            
    return 0;
}*/