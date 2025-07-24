#pragma once
#include "DriverEscape.h"
#include "DisplayEscape.h"
#include "ToolsEscape.h"
#include "DisplayConfig.h"

#define MAX_ADAPTERS 2
#define MAX_EDID_BLOCK_SIZE 128
#define MAX_EDID_BLOCK 8

#define VERIFY_STATUS(status) status == 0 ? "FAIL" : "PASS"

typedef enum _GFX_INDEX
{
    INVALID,
    GFX_0,
    GFX_1
} GFX_INDEX;

CONST PWCHAR ADAPTER_NAME[] = { L"invalid", L"gfx_0", L"gfx_1" };

typedef struct _GFX_INFO
{
    GFX_INDEX           gfxIndex;
    DRIVER_TYPE         driverType;
    GFX_ADAPTER_INFO    adapterInfo;
    ENUMERATED_DISPLAYS enumDisplays;
} GFX_INFO;

BOOLEAN ParseCmdLine(int argc, char *argv[]);
BOOLEAN DriverInit(GFX_INFO *);
VOID    LogMessage(char *, char *);
VOID    InvokeTestApi(GFX_INFO);
BOOLEAN CheckInternalPort(CONNECTOR_PORT_TYPE portType);

// Display Escape APIs

VOID CheckDpcdRead(GFX_INFO);
VOID CheckGetMiscSystemInfo(GFX_INFO);
VOID CheckGetEdidData(GFX_INFO);
VOID CheckGetDppHwLut(GFX_INFO);
VOID CheckSetDppHwLut(GFX_INFO);
VOID CheckIsXvYccSupported(GFX_INFO);
VOID CheckIsYCbCrSupported(GFX_INFO);
VOID CheckConfigureXvYcc(GFX_INFO);
VOID CheckConfigureYCbCr(GFX_INFO);
VOID CheckGetSetOutputFormat(GFX_INFO);
VOID CheckGenerateTdr(GFX_INFO);

// Yangra Escape APIs

VOID CheckYangraGetQuantisationRange(GFX_INFO);
VOID CheckYangraGetSetVrr(GFX_INFO);
VOID CheckYangraPlugUnplugWBDevice(GFX_INFO);
VOID CheckYangraQueryWB(GFX_INFO);
VOID CheckYangraDumpWBBuffer(GFX_INFO);
VOID CheckYangraAlsAggressivenessLevelOverride(GFX_INFO);
VOID CheckYangraInvokeCollage(GFX_INFO);
VOID CheckYangraQueryModeTable(GFX_INFO);
VOID CheckYangraGetSetNNScaling(GFX_INFO);
VOID CheckYangraAddCustomMode(GFX_INFO);
VOID CheckYangraGetSetCfps(GFX_INFO);
VOID CheckYangraGetSetCustomScaling(GFX_INFO);

// Legacy Escape APIs

VOID CheckLegacyGetSupportedScaling(GFX_INFO);
VOID CheckLegacyGetTargetTimings(GFX_INFO);
VOID CheckLegacyGetCurrentConfig(GFX_INFO);
// Tools Escape API

VOID CheckLegacyQueryDisplayDetails(GFX_INFO);
