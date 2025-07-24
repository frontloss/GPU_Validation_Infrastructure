
#include "ExternalCallBacks.h"
#include "..\\DriverInterfaces\\SimDrvToGfx.h"

BOOLEAN EXTERNALCALLBACKS_GenerateSPI(PVOID pGfxAdapterContext, ULONG ulPortNum)
{
    PORT_CONNECTOR_INFO ConnectorInfo = {
        0,
    };
    PGFX_ADAPTER_CONTEXT pTempGfxAdapterContext = pGfxAdapterContext;

    BOOLEAN bRet  = FALSE;
    ConnectorInfo = COMMRXHANDLERS_GetConnectorInfo(pTempGfxAdapterContext->pstRxInfoArr, ulPortNum);
    bRet          = SIMDRVTOGFX_GenerateHPDorSPI(pTempGfxAdapterContext, ulPortNum, FALSE, FALSE, ConnectorInfo);

    return bRet;
}