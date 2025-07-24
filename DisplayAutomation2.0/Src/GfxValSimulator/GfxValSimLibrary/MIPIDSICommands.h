#include <Windows.h>

#pragma pack(push, SIMDRV_MIPI_DSI)
#pragma pack(1)

/* MIPI DSI COMMANDS trigger selection type */
typedef enum _SIMDRV_MIPI_DSI_EVENT
{
    SIMDRV_MIPI_DSI_NONE        = 0,
    SIMDRV_MIPI_DSI_CAPS         = 1,
    SIMDRV_MIPI_DSI_TRANSMISSION = 2,
    SIMDRV_MIPI_DSI_RESET        = 3,
} SIMDRV_MIPI_DSI_EVENT;

// For MIPI DSI Feature
typedef struct _SIMDRV_MIPI_ARGS
{
    SIMDRV_MIPI_DSI_EVENT ulMipiEventType; // MipiDsiCaps = 1, MipiDsiTransmission = 2, MipiDsiReset = 3,
    unsigned long ulTargetId;
    PVOID         pArgs; //contains acutal buffer caps/transmission/reset
} SIMDRV_MIPI_ARGS, *PSIMDRV_MIPI_ARGS;

#pragma pack(pop, SIMDRV_MIPI_DSI)
