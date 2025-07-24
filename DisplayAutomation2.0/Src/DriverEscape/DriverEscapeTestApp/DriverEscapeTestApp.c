#include "DriverEscapeTestApp.h"
#include "log.h"
#include "ColorArgs.h"

char *   LIBRARY_NAME          = "DriverEscapeApp";
GFX_INFO gfxInfo[MAX_ADAPTERS] = { 0 };

int main(int argc, char *argv[])
{
    do
    {
        Initialize("DriverEscapeTestAppLog.txt", true);

        if (FALSE == ParseCmdLine(argc, argv))
        {
            ERROR_LOG("Please check the command line args passed.");
            break;
        }

        for (int gfxCount = 0; gfxCount < argc - 1 && gfxCount < MAX_ADAPTERS; gfxCount++)
        {
            if (FALSE == DriverInit(&gfxInfo[gfxCount]))
            {
                ERROR_LOG("Driver Initialization Failed.");
                break;
            }
            InvokeTestApi(gfxInfo[gfxCount]);
        }

        Cleanup();
    } while (FALSE);

    return 0;
}

BOOLEAN ParseCmdLine(int argc, char *argv[])
{
    BOOLEAN flag         = TRUE;
    INT     adapterIndex = 0;
    do
    {
        if (argc <= 1)
        {
            printf("No gfx index passed. Accepted gfx Index types are (gfx_0, gfx_1)");
            ERROR_LOG("No graphics index passed!");
            flag = FALSE;
            break;
        }

        for (int i = 1; i < argc; i++)
        {
            if (_stricmp((argv[i]), "gfx_0") == 0)
            {
                INFO_LOG("Identified gfx Index as \"gfx_0\"");
                gfxInfo[adapterIndex++].gfxIndex = GFX_0;
            }
            else if (_stricmp((argv[i]), "gfx_1") == 0)
            {
                INFO_LOG("Identified gfx Index as \"gfx_1\"");
                gfxInfo[adapterIndex++].gfxIndex = GFX_1;
            }
            else
            {
                gfxInfo[adapterIndex++].gfxIndex = INVALID;
                printf("Invalid index passed. Accepted gfx Index types are (\'gfx_0\', \'gfx_1\')");
                ERROR_LOG("Invalid Graphics Index passed : %s at cmd args Index %d ", argv[i], i);
                flag = FALSE;
                continue;
            }
        }
    } while (FALSE);
    return flag;
}

BOOLEAN DriverInit(GFX_INFO *gfxInfo)
{
    BOOLEAN flag   = TRUE;
    HRESULT pError = S_FALSE;

    do
    {
        gfxInfo->enumDisplays.Size = sizeof(ENUMERATED_DISPLAYS);

        GetEnumeratedDisplayInfo(&gfxInfo->enumDisplays, &pError);
        INFO_LOG("Number of Displays connected : %d", gfxInfo->enumDisplays.Count);

        if (S_FALSE == pError)
        {
            ERROR_LOG("Failed to get enumerated display info!");
            flag = FALSE;
            break;
        }

        for (int i = 0; i < gfxInfo->enumDisplays.Count; i++)
        {
            if (wcscmp(gfxInfo->enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter.gfxIndex, ADAPTER_NAME[gfxInfo->gfxIndex]) == S_OK)
            {
                gfxInfo->adapterInfo = gfxInfo->enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter;
                break;
            }
        }

        ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
        adapterInfoGdiName.adapterInfo           = gfxInfo->adapterInfo;

        if (FALSE == GetAdapterDetails(&adapterInfoGdiName))
        {
            ERROR_LOG("Failed to Get Adapter GdiDeviceName!");
            flag = FALSE;
            break;
        }

        gfxInfo->driverType = GetDriverType(adapterInfoGdiName);
        if (gfxInfo->driverType == DRIVER_UNKNOWN)
        {
            ERROR_LOG("Failed to Get Adapter GdiDeviceName!");
            flag = FALSE;
        }
    } while (FALSE);
    return flag;
}

VOID InvokeTestApi(GFX_INFO gfxInfo)
{
    do
    {
        if (gfxInfo.driverType == YANGRA_DRIVER)
        {
            LogMessage("Driver Type", "Yangra");

            // Yangra Escape APIs
            CheckYangraQueryModeTable(gfxInfo);
            CheckYangraGetSetVrr(gfxInfo);
            // CheckYangraPlugUnplugWBDevice(gfxInfo);
            // CheckYangraQueryWB(gfxInfo);
            // CheckYangraDumpWBBuffer(gfxInfo);
            CheckYangraAlsAggressivenessLevelOverride(gfxInfo);
            CheckYangraInvokeCollage(gfxInfo);
            CheckYangraGetSetNNScaling(gfxInfo);
            CheckYangraAddCustomMode(gfxInfo);
            CheckYangraGetSetCfps(gfxInfo);
            CheckYangraGetQuantisationRange(gfxInfo);
            CheckYangraGetSetCustomScaling(gfxInfo);
        }
        else if (gfxInfo.driverType == LEGACY_DRIVER)
        {
            LogMessage("Driver Type", "Legacy");

            // Legacy Escape APIs
            CheckLegacyGetSupportedScaling(gfxInfo);
            CheckLegacyGetTargetTimings(gfxInfo);
            CheckLegacyGetCurrentConfig(gfxInfo);

            // Tools Escape API
            CheckLegacyQueryDisplayDetails(gfxInfo);
        }

        // Common Display escape APIs
        CheckDpcdRead(gfxInfo);
        CheckGetMiscSystemInfo(gfxInfo);
        CheckGetEdidData(gfxInfo);
        CheckGetDppHwLut(gfxInfo);
        CheckSetDppHwLut(gfxInfo);
        CheckIsXvYccSupported(gfxInfo);
        CheckIsYCbCrSupported(gfxInfo);
        CheckConfigureXvYcc(gfxInfo);
        CheckConfigureYCbCr(gfxInfo);
        CheckGetSetOutputFormat(gfxInfo);
        CheckGenerateTdr(gfxInfo);
    } while (FALSE);
}

VOID CheckDpcdRead(GFX_INFO gfxInfo)
{
    BOOLEAN status     = FALSE;
    ULONG   offset     = 0x600;
    UINT    bufferSize = 1;
    ULONG   buffer     = 0;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status = DpcdRead(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, offset, bufferSize, &buffer);
        if (buffer == 0)
        {
            printf("DPCD Read Panel Power ON bit is set to 0");
            break;
        }
        LogMessage("DpcdRead", VERIFY_STATUS(status));
    }
}

// Get Misc System Info
VOID CheckGetMiscSystemInfo(GFX_INFO gfxInfo)
{
    BOOLEAN                       status         = FALSE;
    MISC_ESC_GET_SYSTEM_INFO_ARGS MiscSystemInfo = { 0 };

    status = GetMiscSystemInfo(&gfxInfo.adapterInfo, &MiscSystemInfo);
    LogMessage("GetMiscSystemInfo", VERIFY_STATUS(status));
}

// Get EDID Data
VOID CheckGetEdidData(GFX_INFO gfxInfo)
{
    BOOLEAN status = FALSE;
    BYTE    edidData[MAX_EDID_BLOCK * MAX_EDID_BLOCK_SIZE];
    UINT    pNumEdidBlock = 0;
    INT     compareFlag   = 0;
    BYTE    header[8]     = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00 };

    memset(edidData, 0, MAX_EDID_BLOCK * MAX_EDID_BLOCK_SIZE);

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status      = GetEdidData(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, edidData, &pNumEdidBlock);
        compareFlag = memcmp(header, edidData, _countof(header));

        printf("\nEDID header Validation : %s for display with TargetID : %d",
            VERIFY_STATUS((compareFlag == 0 ? TRUE : FALSE)), gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.ConnectorNPortType);
        LogMessage("GetEdidData", VERIFY_STATUS(status));
    }
}

// Get DPPHWLUT Info
VOID CheckGetDppHwLut(GFX_INFO gfxInfo)
{
    BOOLEAN             status          = FALSE;
    CUI_DPP_HW_LUT_INFO cuiDppHwLutInfo = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        cuiDppHwLutInfo.displayID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;

        status = GetDPPHWLUTN(&gfxInfo.adapterInfo, &cuiDppHwLutInfo);
        LogMessage("GetDPPHWLUT", VERIFY_STATUS(status));
    }
}

// Set DPPHWLUT Info
VOID CheckSetDppHwLut(GFX_INFO gfxInfo)
{
    BOOLEAN             status          = FALSE;
    CUI_DPP_HW_LUT_INFO cuiDppHwLutInfo = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        cuiDppHwLutInfo.displayID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
        cuiDppHwLutInfo.depth     = 17;
        cuiDppHwLutInfo.opType    = APPLY_LUT;
        if (_countof(cuiDppHwLutInfo.lutData) == _countof(customLutNoBlue))
        {
            memcpy_s(cuiDppHwLutInfo.lutData, _countof(cuiDppHwLutInfo.lutData), customLutNoBlue, _countof(customLutNoBlue));
        }
        else
        {
            ERROR_LOG("Lut Data Size mismatch between structure member and byte input array (customLutNoBlue) provided.");
            continue;
        }

        status = SetDPPHWLUTN(&gfxInfo.adapterInfo, &cuiDppHwLutInfo);
        LogMessage("SetDPPHWLUT CustomLut_No_B", VERIFY_STATUS(status));

        if (FALSE == status)
        {
            ERROR_LOG("Applying Default is skipped.");
            continue;
        }

        if (_countof(cuiDppHwLutInfo.lutData) == _countof(customLutNoBlue))
        {
            memcpy_s(cuiDppHwLutInfo.lutData, _countof(cuiDppHwLutInfo.lutData), customLutDefault, _countof(customLutDefault));
        }
        else
        {
            ERROR_LOG("Lut Data Size mismatch between structure member and byte input array (customLutDefault) provided.");
            continue;
        }

        status = SetDPPHWLUTN(&gfxInfo.adapterInfo, &cuiDppHwLutInfo);
        LogMessage("SetDPPHWLUT CustomLut_Default", VERIFY_STATUS(status));
    }
}

// Check if XvYcc is supported
VOID CheckIsXvYccSupported(GFX_INFO gfxInfo)
{
    BOOLEAN status = FALSE;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage("IsXvYccSupported. Unsupported Port Type for XvYcc.", VERIFY_STATUS(status));
            continue;
        }
        else
        {
            status = IsXvYccSupported(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo);
            LogMessage("IsXvYccSupported", VERIFY_STATUS(status));
        }
    }
}

// Check if YCbCr is supported
VOID CheckIsYCbCrSupported(GFX_INFO gfxInfo)
{
    BOOLEAN status = FALSE;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage("IsYCbCrSupported. Unsupported Port Type for YCbCr.", VERIFY_STATUS(status));
            continue;
        }
        else
        {
            status = IsYCbCrSupported(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo);
            LogMessage("IsYCbCrSupported", VERIFY_STATUS(status));
        }
    }
}

// Configure XvYcc
VOID CheckConfigureXvYcc(GFX_INFO gfxInfo)
{
    BOOLEAN status    = FALSE;
    BOOLEAN isEnabled = FALSE;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage("ConfigureXvYcc. Unsupported Port Type for XvYcc.", VERIFY_STATUS(status));
            continue;
        }
        else
        {
            // Disabling XvYcc
            status = ConfigureXvYcc(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled);
            LogMessage("ConfigureXvYcc DISABLE XvYcc", VERIFY_STATUS(status));

            if (FALSE == status)
            {
                ERROR_LOG("Failed to Disable XvYcc");
            }
            else
            {
                // Enabling XvYcc
                isEnabled = TRUE;
                status    = ConfigureXvYcc(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled);
                LogMessage("ConfigureXvYcc ENABLE XvYcc", VERIFY_STATUS(status));
                if (FALSE == status)
                {
                    ERROR_LOG("Failed to Enable XvYcc");
                }
                // Disabling Again
                isEnabled = FALSE;
                status    = ConfigureXvYcc(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled);
            }
        }
    }
}

// Configure YCbCr
VOID CheckConfigureYCbCr(GFX_INFO gfxInfo)
{
    BOOLEAN status    = FALSE;
    BOOLEAN isEnabled = FALSE;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage("ConfigureYCbCr. Unsupported Port Type for YCbCr.", VERIFY_STATUS(status));
            continue;
        }
        else
        {
            // Disabling XvYcc
            // 5 -> DD_COLOR_MODEL_YCBCR_PREFERRED
            status = ConfigureYCbCr(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled, 5);
            LogMessage("ConfigureYCbCr DISABLE YCbCr", VERIFY_STATUS(status));

            if (FALSE == status)
            {
                ERROR_LOG("Failed to Disable YCbCr");
            }
            else
            {
                // Enabling XvYcc
                isEnabled = TRUE;
                status    = ConfigureYCbCr(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled, 5);
                LogMessage("ConfigureYCbCr ENABLE YCbCr", VERIFY_STATUS(status));
                if (FALSE == status)
                {
                    ERROR_LOG("Failed to Enable YCbCr");
                }
                // Disabling Again
                isEnabled = FALSE;
                status    = ConfigureYCbCr(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, isEnabled, 5);
            }
        }
    }
}

// Generate Tdr
VOID CheckGenerateTdr(GFX_INFO gfxInfo)
{
    BOOLEAN status     = FALSE;
    BOOLEAN displayTdr = TRUE;

    status = GenerateTdr(&gfxInfo.adapterInfo, displayTdr);
    LogMessage("GenerateTdr", VERIFY_STATUS(status));
}

// Get Supported Scaling for Legacy Driver
VOID CheckLegacyGetSupportedScaling(GFX_INFO gfxInfo)
{
    BOOLEAN           status           = FALSE;
    CUI_ESC_MODE_INFO modeInfo         = { 0 };
    USHORT            supportedScaling = 0;

    modeInfo.sourceX        = 0;
    modeInfo.sourceY        = 0;
    modeInfo.refreshRate    = 0;
    modeInfo.eScanLineOrder = CUI_ESC_PROGRESSIVE;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status = LegacyGetSupportedScaling(&gfxInfo.adapterInfo, gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID, modeInfo, &supportedScaling);
        LogMessage("LegacyGetSupportedScaling", VERIFY_STATUS(status));
    }
}

// Get Target Timings for Legacy Driver
VOID CheckLegacyGetTargetTimings(GFX_INFO gfxInfo)
{
    BOOLEAN                          status                = FALSE;
    CUI_ESC_CONVERT_RR_RATIONAL_ARGS convertRrRationalArgs = { 0 };
    CUI_ESC_PATH_INFO                pathInfo              = { 0 };
    CUI_ESC_MODE_INFO                modeInfo              = { 0 };
    USHORT                           supportedScaling      = 0;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        pathInfo.targetID      = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
        pathInfo.sourceID      = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.sourceID;
        pathInfo.eModeInfoType = CUI_ESC_MODE_PINNED;

        modeInfo.sourceX                            = 1920;
        modeInfo.sourceY                            = 1080;
        modeInfo.colorBPP                           = (4 * 8);
        modeInfo.eScanLineOrder                     = CUI_ESC_PROGRESSIVE;
        modeInfo.refreshRate                        = 60;
        modeInfo.stCurrentCompensation.compensation = 64;

        pathInfo.stModeInfo = modeInfo;

        convertRrRationalArgs.stTopology.numOfPaths             = 1;
        convertRrRationalArgs.stTopology.ignoreUnsupportedModes = 1;

        convertRrRationalArgs.stTopology.stPathInfo[0] = pathInfo;

        status = LegacyGetTargetTimings(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &convertRrRationalArgs);
        LogMessage("LegacyGetTargetTimings", VERIFY_STATUS(status));
    }
}

// Get/Set Vrr for Yangra Driver
VOID CheckYangraGetSetVrr(GFX_INFO gfxInfo)
{
    BOOLEAN                     status        = FALSE;
    DD_CUI_ESC_GET_SET_VRR_ARGS getSetVrrArgs = { 0 };

    getSetVrrArgs.operation = DD_CUI_ESC_VRR_OPERATION_GET_INFO;

    status = YangraGetSetVrr(&gfxInfo.adapterInfo, &getSetVrrArgs);
    LogMessage("YangraGetSetVrr", VERIFY_STATUS(status));
}

// Plug/Unplug WB Device for Yangra Driver (TBI)
VOID CheckYangraPlugUnplugWBDevice(GFX_INFO gfxInfo)
{
    BOOLEAN              status = FALSE;
    DD_ESC_WRITEBACK_HPD wbHpd  = { 0 };

    // wbHpd.deviceID = (ULONG)target_id; // Change this plugging device ID

    // Plug call
    wbHpd.hotPlug       = PLUG_WB;
    wbHpd.resolution.cX = 0;
    wbHpd.resolution.cY = 0;

    status = YangraPlugUnplugWBDevice(&gfxInfo.adapterInfo, wbHpd, NULL);
    LogMessage("YangraPlugUnplugWBDevice PLUG", VERIFY_STATUS(status));

    // Unplug call
    wbHpd.hotPlug  = UNPLUG_WB;
    wbHpd.deviceID = wbHpd.deviceID;

    status = YangraPlugUnplugWBDevice(&gfxInfo.adapterInfo, wbHpd, NULL);
    LogMessage("YangraPlugUnplugWBDevice UNPLUG", VERIFY_STATUS(status));
}

// Query WB Feature Enabled for Yangra Driver (TBI)
VOID CheckYangraQueryWB(GFX_INFO gfxInfo)
{
    BOOLEAN                 status      = FALSE;
    DD_WRITEBACK_QUERY_ARGS wbQueryArgs = { 0 };

    status = YangraQueryWB(&gfxInfo.adapterInfo, &wbQueryArgs);
    LogMessage("YangraQueryWB", VERIFY_STATUS(status));
}

// Dump WB Buffer Args & Info for Yangra Driver (TBI)
VOID CheckYangraDumpWBBuffer(GFX_INFO gfxInfo)
{
    BOOLEAN           status       = FALSE;
    DD_WB_BUFFER_ARGS wbBufferArgs = { 0 };
    DD_WB_BUFFER_INFO wbBufferInfo = { 0 };
    UINT              imageBpc     = 8;

    // TBI - Plug call and Dump
    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status = YangraDumpWBBuffer(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, 0, &wbBufferInfo, imageBpc);
        LogMessage("YangraDumpWBBuffer Buffer Size", VERIFY_STATUS(status));
    }

    if (wbBufferArgs.bufferSize > 0)
    {
        for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
        {
            status = YangraDumpWBBuffer(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, 0, &wbBufferInfo, imageBpc);
            LogMessage("YangraDumpWBBuffer Buffer Info", VERIFY_STATUS(status));
        }
    }
}

// Als Aggressiveness Level Override for Yangra Driver
VOID CheckYangraAlsAggressivenessLevelOverride(GFX_INFO gfxInfo)
{
    BOOLEAN status   = FALSE;
    BOOLEAN luxOp    = TRUE;
    BOOLEAN aggOp    = TRUE;
    INT     lux      = 3500;
    INT     aggLevel = 2;

    status = YangraAlsAggressivenessLevelOverride(&gfxInfo.adapterInfo, luxOp, aggOp, lux, aggLevel);
    LogMessage("YangraAlsAggressivenessLevelOverride", VERIFY_STATUS(status));
}

// Invoke Collage Operations for Yangra Driver
VOID CheckYangraInvokeCollage(GFX_INFO gfxInfo)
{
    BOOLEAN                              status          = FALSE;
    DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS collageModeArgs = { 0 };
    CUI_ESC_COLLAGE_TYPE                 collageType[2]  = { CUI_ESC_HORIZONTAL_COLLAGE, CUI_ESC_VERTICAL_COLLAGE };

    for (int type = 0; type < (sizeof(collageType) / sizeof(CUI_ESC_COLLAGE_TYPE)); type++)
    {
        DD_CUI_ESC_COLLAGE_TOPOLOGY collageTopology;

        ZeroMemory(&collageTopology, sizeof(DD_CUI_ESC_COLLAGE_TOPOLOGY));

        for (int i = 0, j = 0; i < gfxInfo.enumDisplays.Count; ++i)
        {
            if (gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType != DP_A)
            {
                collageTopology.collageChildInfo[j].childID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
                switch (collageType[type])
                {
                case CUI_ESC_HORIZONTAL_COLLAGE:
                    collageTopology.collageChildInfo[j].hTileLocation = j;
                    collageTopology.collageChildInfo[j].vTileLocation = 0;
                    collageTopology.totalNumberOfHTiles               = j + 1;
                    collageTopology.totalNumberOfVTiles               = 1;

                    break;
                case CUI_ESC_VERTICAL_COLLAGE:
                    collageTopology.collageChildInfo[j].hTileLocation = 0;
                    collageTopology.collageChildInfo[j].vTileLocation = j;
                    collageTopology.totalNumberOfHTiles               = 1;
                    collageTopology.totalNumberOfVTiles               = j + 1;
                    break;
                default:
                    break;
                }
                ++j;
            }
        }

        collageModeArgs.collageTopology = collageTopology;

        // Validate Collage
        collageModeArgs.operation = DD_CUI_ESC_COLLAGE_OPERATION_VALIDATE;
        status                    = YangraInvokeCollage(&gfxInfo.adapterInfo, &collageModeArgs);
        LogMessage("YangraInvokeCollage VALIDATE", VERIFY_STATUS(status));

        // Enable Collage
        collageModeArgs.operation = DD_CUI_ESC_COLLAGE_OPERATION_ENABLE;
        status                    = YangraInvokeCollage(&gfxInfo.adapterInfo, &collageModeArgs);
        LogMessage("YangraInvokeCollage ENABLE", VERIFY_STATUS(status));

        // Get Collage
        collageModeArgs.operation = DD_CUI_ESC_COLLAGE_OPERATION_GET;
        status                    = YangraInvokeCollage(&gfxInfo.adapterInfo, &collageModeArgs);
        LogMessage("YangraInvokeCollage GET", VERIFY_STATUS(status));

        // Disable Collage
        collageModeArgs.operation = DD_CUI_ESC_COLLAGE_OPERATION_DISABLE;
        status                    = YangraInvokeCollage(&gfxInfo.adapterInfo, &collageModeArgs);
        LogMessage("YangraInvokeCollage DISABLE", VERIFY_STATUS(status));
    }
}

// Get Query Mode Table for Yangra Driver
VOID CheckYangraQueryModeTable(GFX_INFO gfxInfo)
{
    BOOLEAN                       status              = FALSE;
    DD_ESC_QUERY_MODE_TABLE_ARGS  modeTableArgs       = { 0 };
    DD_ESC_QUERY_MODE_TABLE_ARGS *pQueryModeTableArgs = NULL;
    DD_SOURCE_MODE_INFO *         pSrcModeTable       = NULL;

    modeTableArgs.modeInfo->targetID = gfxInfo.enumDisplays.ConnectedDisplays[0].panelInfo.targetID;

    // Get Number of Soruce and Target Modes
    status = YangraQueryModeTable(&gfxInfo.enumDisplays.ConnectedDisplays[0].panelInfo, &modeTableArgs);

    pQueryModeTableArgs = (DD_ESC_QUERY_MODE_TABLE_ARGS *)calloc(
    1, (sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + sizeof(DD_TIMING_INFO) * modeTableArgs.numTgtModes + sizeof(DD_SOURCE_MODE_INFO) * modeTableArgs.numSrcModes));

    pQueryModeTableArgs->numPinnedTgt         = 0;
    pQueryModeTableArgs->numSrcModes          = 0;
    pQueryModeTableArgs->numTgtModes          = 0;
    pQueryModeTableArgs->modeInfo[0].targetID = gfxInfo.enumDisplays.ConnectedDisplays[0].panelInfo.targetID;

    // Get Mode Table
    status = YangraQueryModeTable(&gfxInfo.enumDisplays.ConnectedDisplays[0].panelInfo, pQueryModeTableArgs);
    LogMessage("YangraQueryModeTable", VERIFY_STATUS(status));

    free(pQueryModeTableArgs);
}

// Query Display Details For Legacy Driver
VOID CheckLegacyQueryDisplayDetails(GFX_INFO gfxInfo)
{
    BOOLEAN                             status              = FALSE;
    TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS queryDisplayDetails = { 0 };
    for (int i = 0, j = 0; i < gfxInfo.enumDisplays.Count; ++i)
    {
        queryDisplayDetails.ulDisplayUID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;

        ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
        adapterInfoGdiName.adapterInfo           = gfxInfo.adapterInfo;
        if (FALSE == GetAdapterDetails(&adapterInfoGdiName))
        {
            ERROR_LOG("Failed to get Adapter Details");
        }

        status = LegacyQueryDisplayDetails(adapterInfoGdiName, &queryDisplayDetails);
        LogMessage("LegacyQueryDisplayDetails", VERIFY_STATUS(status));
    }
}

// Get Set NNScaling For Yangra Driver
VOID CheckYangraGetSetNNScaling(GFX_INFO gfxInfo)
{
    BOOLEAN                    status       = FALSE;
    DD_CUI_ESC_GET_SET_NN_ARGS getSetNnArgs = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        // Get NN Scaling
        getSetNnArgs.OpCode = DD_CUI_ESC_GET_NN_SCALING_STATE;
        status              = YangraGetSetNNScaling(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter, &getSetNnArgs);
        LogMessage("YangraGetSetNNScaling GET NN Scaling", VERIFY_STATUS(status));

        // Set NN Scaling
        getSetNnArgs.OpCode = DD_CUI_ESC_SET_NN_SCALING_STATE;
        status              = YangraGetSetNNScaling(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter, &getSetNnArgs);
        LogMessage("YangraGetSetNNScaling SET NN Scaling", VERIFY_STATUS(status));
    }
}

// Add Custom Mode For Yangra Driver
VOID CheckYangraAddCustomMode(GFX_INFO gfxInfo)
{
    BOOLEAN status      = FALSE;
    ULONG   hResolution = 1920;
    ULONG   vResolution = 1080;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status = YangraAddCustomMode(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, hResolution, vResolution);
        LogMessage("YangraAddCustomMode", VERIFY_STATUS(status));
    }
}

// Get Current Config For Legacy Driver
VOID CheckLegacyGetCurrentConfig(GFX_INFO gfxInfo)
{
    BOOLEAN                         status           = FALSE;
    CUI_ESC_QUERY_COMPENSATION_ARGS compensationArgs = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        status = LegacyGetCurrentConfig(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &compensationArgs);
        LogMessage("LegacyGetCurrentConfig", VERIFY_STATUS(status));
    }
}

// Get Set BPC and Encoding
void CheckGetSetOutputFormat(GFX_INFO gfxInfo)
{
    BOOLEAN                            status             = FALSE;
    IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT outputFormatArgs   = { 0 };
    ADAPTER_INFO_GDI_NAME              adapterInfoGdiName = { 0 };
    DRIVER_TYPE                        driverBranch       = DRIVER_UNKNOWN;

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {

        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage(" Unsupported Port Type for overide bpc and encoding.", VERIFY_STATUS(status));
            continue;
        }
        else
        {

            adapterInfoGdiName.adapterInfo = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter;
            driverBranch                   = GetDriverType(adapterInfoGdiName);

            if (driverBranch == LEGACY_DRIVER)
            {
                outputFormatArgs.opType    = CUI_ESC_COLORSPACE_OPTYPE_GET;
                outputFormatArgs.displayID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
                status                     = GetSetOutputFormat(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &outputFormatArgs);
                LogMessage("LegacyGetSetOutputFormat---Get call", VERIFY_STATUS(status));
                outputFormatArgs.opType                 = CUI_ESC_COLORSPACE_OPTYPE_SET;
                outputFormatArgs.overrideBpc            = 4;
                outputFormatArgs.overrideEncodingFormat = 16;
                status                                  = GetSetOutputFormat(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &outputFormatArgs);
                LogMessage("LegacyGetSetOutputFormat---Set call", VERIFY_STATUS(status));
            }
            else if (driverBranch == YANGRA_DRIVER)
            {
                outputFormatArgs.opType    = 0;
                outputFormatArgs.displayID = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
                status                     = GetSetOutputFormat(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &outputFormatArgs);
                LogMessage("YangraGetSetOutputFormat---Get call", VERIFY_STATUS(status));
                outputFormatArgs.opType                 = 1;
                outputFormatArgs.overrideBpc            = 4;
                outputFormatArgs.overrideEncodingFormat = 16;
                status                                  = GetSetOutputFormat(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &outputFormatArgs);
                LogMessage("YangraGetSetOutputFormat---Set call", VERIFY_STATUS(status));
            }
        }
    }
}

// Get Set CFPS For Yangra Driver
VOID CheckYangraGetSetCfps(GFX_INFO gfxInfo)
{
    BOOLEAN                            status         = FALSE;
    DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS getSetCfpsArgs = { 0 };

    // Get CFPS

    getSetCfpsArgs.OpCode = DD_CUI_ESC_GET_CAPPED_FPS;

    status = YangraGetSetCfps(&gfxInfo.adapterInfo, &getSetCfpsArgs);
    LogMessage("GET YangraGetSetCfps", VERIFY_STATUS(status));

    // Set CFPS

    if (getSetCfpsArgs.CappedFpsState == DD_CUI_ESC_CAPPED_FPS_STATE_DISABLE)
        getSetCfpsArgs.CappedFpsState = DD_CUI_ESC_CAPPED_FPS_STATE_ENABLE;
    else if (getSetCfpsArgs.CappedFpsState == DD_CUI_ESC_CAPPED_FPS_STATE_ENABLE)
        getSetCfpsArgs.CappedFpsState = DD_CUI_ESC_CAPPED_FPS_STATE_DISABLE;
    else
        getSetCfpsArgs.CappedFpsState = DD_CUI_ESC_CAPPED_FPS_STATE_AUTO;

    getSetCfpsArgs.OpCode = DD_CUI_ESC_SET_CAPPED_FPS;

    status = YangraGetSetCfps(&gfxInfo.adapterInfo, &getSetCfpsArgs);
    LogMessage("SET YangraGetSetCfps", VERIFY_STATUS(status));
}

VOID CheckYangraGetQuantisationRange(GFX_INFO gfxInfo)
{
    BOOLEAN                                       status          = FALSE;
    DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS avi_info_struct = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {

        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            INFO_LOG(" Unsupported Port Type for getting quantisation range.", VERIFY_STATUS(status));
            continue;
        }
        else
        {
            avi_info_struct.Operation = 0;
            avi_info_struct.TargetID  = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;

            status = YangraGetSetQuantisationRange(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &avi_info_struct);
            LogMessage("CheckYangraGetQuantisationRange", VERIFY_STATUS(status));

            avi_info_struct.AVIInfoFrame.QuantRange = 2;
            avi_info_struct.Operation               = 1;
            avi_info_struct.TargetID                = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;

            status = YangraGetSetQuantisationRange(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &avi_info_struct);
            LogMessage("CheckYangraSetQuantisationRange", VERIFY_STATUS(status));

            avi_info_struct.Operation = 0;
            avi_info_struct.TargetID  = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;

            status = YangraGetSetQuantisationRange(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo, &avi_info_struct);
            LogMessage("CheckYangraGetQuantisationRange", VERIFY_STATUS(status));
        }
    }
}

// Get Set Custom Scaling For Yangra Driver
VOID CheckYangraGetSetCustomScaling(GFX_INFO gfxInfo)
{
    BOOLEAN                        status                  = FALSE;
    DD_ESC_SET_CUSTOM_SCALING_ARGS getSetCustomScalingArgs = { 0 };

    for (int i = 0; i < gfxInfo.enumDisplays.Count; i++)
    {
        if (FALSE == CheckInternalPort(gfxInfo.enumDisplays.ConnectedDisplays[i].ConnectorNPortType))
        {
            LogMessage(" Unsupported Port Type for Custom Scaling.", VERIFY_STATUS(status));
            continue;
        }
        else
        {

            // Get Custom Scaling
            getSetCustomScalingArgs.Get      = TRUE;
            getSetCustomScalingArgs.TargetId = gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.targetID;
            status                           = YangraGetSetCustomScaling(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter, &getSetCustomScalingArgs);
            LogMessage("YangraGetSetCustomScaling GET custom Scaling", VERIFY_STATUS(status));

            // Set Custom Scaling
            getSetCustomScalingArgs.Enable         = TRUE;
            getSetCustomScalingArgs.Get            = FALSE;
            getSetCustomScalingArgs.CustomScalingX = 90;
            getSetCustomScalingArgs.CustomScalingY = 90;

            status = YangraGetSetCustomScaling(&gfxInfo.enumDisplays.ConnectedDisplays[i].panelInfo.gfxAdapter, &getSetCustomScalingArgs);
            LogMessage("YangraGetSetCustomScaling SET custom Scaling", VERIFY_STATUS(status));
        }
    }
}

// LogMessage function implements reusable INFO Logging and console print (Internal API)
VOID LogMessage(char *str, char *status)
{
    printf("\n%-60s -> %5s", str, status);
    INFO_LOG("%-80s -> %5s", str, status);
}

// To Check if the current port is eDP/MIPI - Color features
BOOLEAN CheckInternalPort(CONNECTOR_PORT_TYPE portType)
{
    BOOLEAN             flag               = TRUE;
    CONNECTOR_PORT_TYPE unsupportedPorts[] = { DP_A, MIPI_A, MIPI_C };

    for (int j = 0; j < sizeof(unsupportedPorts) / sizeof(unsupportedPorts[0]); j++)
    {
        if (unsupportedPorts[j] == portType)
        {
            flag = FALSE;
            break;
        }
    }
    return flag;
}
