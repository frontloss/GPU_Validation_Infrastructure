#ifndef __DPCDMODEL_H__
#define __DPCDMODEL_H__
#include "AuxInterface.h"

// copies and stores the DPCD model data sent from userspace into local context.
// Initializes stDPCDModelData and ucDPCDTransactionIndex. This will be called after plug call from userspace and before issuing HPD interrupt.
BOOLEAN DPCDMODEL_LoadDPCDModelData(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType, PDPCD_MODEL_DATA pstDPCDModelData);

// cleans up stDPCDModelData and resets ucDPCDTransactionIndex to 0. This will be called during unplug.
BOOLEAN DPCDMODEL_CleanupDPCDModelData(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType);

#endif