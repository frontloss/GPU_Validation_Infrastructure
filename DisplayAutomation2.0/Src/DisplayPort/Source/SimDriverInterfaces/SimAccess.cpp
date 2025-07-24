#include "DisplayPort.h"

HANDLE hGfxValSimHandle;

/*
 * @brief        Initialize Gfx val simulation driver
 * @param[In]    DP device content
 * @return       BOOL. Returns TRUE if Simulation driver initialization successful otherwise FALSE
 */
BOOL InitializeGfxValSimulator(PDPDeviceContext pstDPDevContext)
{
    BOOL bStatus = TRUE;

    do
    {
        if (hGfxValSimHandle != NULL)
        {
            bStatus = FALSE;
            break;
        }

        /* Get a handle to DP Stub driver */
        hGfxValSimHandle = CreateFile("\\\\.\\SimDrvDosDev",              /* Device Name */
                                      GENERIC_READ | GENERIC_WRITE,       /* Desired Access*/
                                      FILE_SHARE_READ | FILE_SHARE_WRITE, /* Share Mode*/
                                      NULL,                               /* Default Security Attributes*/
                                      OPEN_EXISTING,                      /* Creation disposition*/
                                      0,                                  /* Flags & Attributes*/
                                      NULL                                /* Template File*/
        );

        if (INVALID_HANDLE_VALUE == hGfxValSimHandle)
        {
            TRACE_LOG(DEBUG_LOGS, "[DisplayPort.DLL] Error in opening the Gfx Val Simulation driver handle with error code: %d \n", GetLastError());
            return FALSE;
        }
        else
        {
            TRACE_LOG(DEBUG_LOGS, "[DisplayPort.DLL]: Able to get handle to Gfx Val Simulation driver successfully.\n");

            /* Save the handle to DIVA in the DP device context for future use */
            pstDPDevContext->hGfxValSimHandle = hGfxValSimHandle;
            pstDPDevContext->bGfxValSimStatus = TRUE;
        }
    } while (FALSE);

    return bStatus;
}