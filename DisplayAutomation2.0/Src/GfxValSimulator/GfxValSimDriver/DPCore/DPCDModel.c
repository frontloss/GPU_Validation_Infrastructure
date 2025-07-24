#include "DPCDModel.h"
#include "..\CommonInclude\ETWLogging.h"

// stores the DPCD model data sent from userspace into local context.
// Initializes stDPCDModelData and ucDPCDTransactionIndex. This will be called after plug call from userspace and before issuing HPD interrupt.
BOOLEAN DPCDMODEL_LoadDPCDModelData(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType, PDPCD_MODEL_DATA pstDPCDModelData)
{
    BOOLEAN          bret = TRUE;
    PDPCD_MODEL_DATA pstDestDPCDModelData;

    if (pstDPAuxInterface == NULL || pstDPCDModelData == NULL)
    {
        GFXVALSIM_DBG_MSG("ERROR: DP Aux Interface is NULL or DPCD Model data passed is NULL !!.. Exiting..\n");
        return FALSE;
    }

    // Note: pstDPCDModelData == NULL is not allowed. For usage of this DPCD model data for link training with plug call,
    // in case user calls plug without DPCD model data, library has to fill 1 transaction data to make Link training successful in 1st transaction itself.
    if (eTopologyType == eDPSST)
    {
        pstDestDPCDModelData = &(pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData.stDPCDModelData);
        memcpy_s(pstDestDPCDModelData, sizeof(DPCD_MODEL_DATA), pstDPCDModelData, sizeof(DPCD_MODEL_DATA));
        pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData.ucDPCDTransactionIndex = 0;
    }
    else if (eTopologyType == eDPMST)
    {
        pstDestDPCDModelData = &(pstDPAuxInterface->pstDP12Topology->stDPCDConfigData.stDPCDModelData);
        memcpy_s(pstDestDPCDModelData, sizeof(DPCD_MODEL_DATA), pstDPCDModelData, sizeof(DPCD_MODEL_DATA));
        pstDPAuxInterface->pstDP12Topology->stDPCDConfigData.ucDPCDTransactionIndex = 0;
    }

    return bret;
}

// cleans up stDPCDModelData and resets ucDPCDTransactionIndex to 0. This will be called during unplug.
BOOLEAN DPCDMODEL_CleanupDPCDModelData(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType)
{
    BOOLEAN bret = TRUE;

    if (pstDPAuxInterface == NULL)
    {
        GFXVALSIM_DBG_MSG("ERROR: DP Aux Interface is NULL!!.. Exiting..\n");
        return FALSE;
    }

    if (eTopologyType == eDPSST)
    {
        memset(&(pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData.stDPCDModelData), 0, sizeof(DPCD_MODEL_DATA));
        pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData.ucDPCDTransactionIndex = 0;
    }
    else if (eTopologyType == eDPMST)
    {
        memset(&(pstDPAuxInterface->pstDP12Topology->stDPCDConfigData.stDPCDModelData), 0, sizeof(DPCD_MODEL_DATA));
        pstDPAuxInterface->pstDP12Topology->stDPCDConfigData.ucDPCDTransactionIndex = 0;
    }

    return bret;
}