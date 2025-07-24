/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayColor.cpp
 * @brief    This file contains Implementation of DisplayColor APIs - ConfigureColorAccuracy,
 *           GetDesktopGammaColor, SetDesktopGammaColor, GetNarrowGamut, GetHueSaturation,
 *           SetHueSaturation, GetWideGamutExpansion, SetWideGamutExpansion
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "SdkSharedHeader.h"
#include "CuiSdk.h"

extern ICUIExternal8 *pCUIExternal;

/**---------------------------------------------------------------------------------------------------------*
 * @brief           ConfigureColorAccuracy (Exposed API)
 * Description      This function is used to enable/disable color accuracy
 * @param[InOut]    pNarrowGamutInfo (Pointer to _IGFX_GAMUT structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN ConfigureColorAccuracy(_Out_ IGFX_GAMUT *pNarrowGamutInfo)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pNarrowGamutInfo);

    INFO_LOG("ConfigureColorAccuracy for deviceID: %ld, enableDisable: %d", pNarrowGamutInfo->deviceUID, pNarrowGamutInfo->enableDisable);

    hr = pCUIExternal->SetDeviceData(IGFX_GET_SET_GAMUT_GUID, sizeof(IGFX_GAMUT), (BYTE *)pNarrowGamutInfo, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetDesktopGammaColor (Exposed API)
 * Description      This function has implementation to GET Desktop Gamma Color information
 * @param[Out]      pNarrowGamutInfo (Pointer to _IGFX_DESKTOP_GAMMA_ARGS structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetDesktopGammaColor(_Inout_ IGFX_DESKTOP_GAMMA_ARGS *pDesktopGammaArgs)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pDesktopGammaArgs);

    INFO_LOG("GetDesktopGammaColor for deviceID: %ld", pDesktopGammaArgs->deviceUID);

    hr = pCUIExternal->GetDeviceData(IGFX_DESKTOP_GAMMA, sizeof(IGFX_DESKTOP_GAMMA_ARGS), (BYTE *)pDesktopGammaArgs, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           SetDesktopGammaColor (Exposed API)
 * Description      This function has implementation to SET Desktop Gamma Color information
 * @param[In]       pNarrowGamutInfo (Pointer to _IGFX_DESKTOP_GAMMA_ARGS structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN SetDesktopGammaColor(_In_ IGFX_DESKTOP_GAMMA_ARGS *pDesktopGammaArgs)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pDesktopGammaArgs);

    INFO_LOG("SetDesktopGammaColor for deviceID: %ld", pDesktopGammaArgs->deviceUID);

    hr = pCUIExternal->SetDeviceData(IGFX_DESKTOP_GAMMA, sizeof(IGFX_DESKTOP_GAMMA_ARGS), (BYTE *)pDesktopGammaArgs, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetNarrowGamut (Exposed API)
 * Description      This function has implementation to GET Narraow Gamut information
 * @param[Out]      pNarrowGamutInfo (Pointer to _IGFX_GAMUT structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetNarrowGamut(_Inout_ IGFX_GAMUT *pNarrowGamutInfo)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pNarrowGamutInfo);

    INFO_LOG("GetNarrowGamut for deviceID: %ld", pNarrowGamutInfo->deviceUID);

    hr = pCUIExternal->GetDeviceData(IGFX_GET_SET_GAMUT_GUID, sizeof(IGFX_GAMUT), (BYTE *)pNarrowGamutInfo, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetHueSaturation (Exposed API)
 * Description      This function has implementation to GET Hue and Saturation information
 * @param[Out]      pHueSatInfo (Pointer to _IGFX_HUESAT_INFO structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetHueSaturation(_Inout_ IGFX_HUESAT_INFO *pHueSatInfo)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pHueSatInfo);

    INFO_LOG("GetHueSaturation for deviceID: %lu", pHueSatInfo->deviceID);

    hr = pCUIExternal->GetDeviceData(IGFX_GET_SET_HUESAT_INFO_GUID, sizeof(IGFX_HUESAT_INFO), (BYTE *)pHueSatInfo, &errorCode);
    INFO_LOG("HR -> %ld error-> %lu", status, errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           SetHueSaturation (Exposed API)
 * Description      This function has implementation to SET Hue and Saturation information
 * @param[In]       pHueSatInfo (Pointer to _IGFX_HUESAT_INFO structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN SetHueSaturation(_In_ IGFX_HUESAT_INFO *pHueSatInfo)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pHueSatInfo);

    INFO_LOG("SetHueSaturation for deviceID: %ld", pHueSatInfo->deviceID);

    hr = pCUIExternal->SetDeviceData(IGFX_GET_SET_HUESAT_INFO_GUID, sizeof(IGFX_HUESAT_INFO), (BYTE *)pHueSatInfo, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetWideGamutExpansion (Exposed API)
 * Description      This function has implementation to GET Wide Gamut Expansion
 * @param[Out]      pWideGamut (Pointer to _IGFX_GAMUT_EXPANSION structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetWideGamutExpansion(_Inout_ IGFX_GAMUT_EXPANSION *pWideGamut)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pWideGamut);

    INFO_LOG("GetWideGamutExpansion for deviceID: %ld", pWideGamut->deviceUID);

    hr = pCUIExternal->GetDeviceData(IGFX_GET_SET_GAMUT_EXPANSION_GUID, sizeof(IGFX_GAMUT_EXPANSION), (BYTE *)pWideGamut, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           SetWideGamutExpansion (Exposed API)
 * @Description     This function has implementation to SET Wide Gamut Expansion
 * @param[In]       pWideGamut (Pointer to _IGFX_GAMUT_EXPANSION structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN SetWideGamutExpansion(_In_ IGFX_GAMUT_EXPANSION *pWideGamut)
{
    DWORD   errorCode = 0;
    HRESULT hr        = S_FALSE;
    BOOLEAN status    = FALSE;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pWideGamut);

    INFO_LOG("SetWideGamutExpansion for deviceID: %ld", pWideGamut->deviceUID);

    hr = pCUIExternal->SetDeviceData(IGFX_GET_SET_GAMUT_EXPANSION_GUID, sizeof(IGFX_GAMUT_EXPANSION), (BYTE *)pWideGamut, &errorCode);
    if (SUCCEEDED(hr) && errorCode == IGFX_SUCCESS)
        status = TRUE;
    else
        ERROR_LOG("SDK Escape call failed with errorCode - %lu", errorCode);

    return status;
}