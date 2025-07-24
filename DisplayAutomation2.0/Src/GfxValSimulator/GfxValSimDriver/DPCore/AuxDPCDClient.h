
#ifndef __AUXCLIENT_H__
#define __AUXCLIENT_H__

#include "AuxInterface.h"
#include "SidebandUtil.h"
#include "MSTTopology.h"
#include "DPCDs.h"

typedef struct _RECEIVER_CAPS
{
    DPCD_REV eDPCDRev;
    ULONG    ulMaxLinkRateDPCDAddress;
    ULONG    ulMaxLaneCountDPCDAddress;
    ULONG    ulMaxDownSpreadDPCDAddress;
} RECEIVER_CAPS, *PRECEIVER_CAPS;

BOOLEAN AUXCLIENT_ServiceIRQVectorRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo);

BOOLEAN AUXCLIENT_SideBandReadHandler(PDPCD_CLIENTINFO pDPCDClientInfo);

BOOLEAN AUXCLIENT_SideBandWriteHandler(PDPCD_CLIENTINFO pDPCDClientInfo);

BOOLEAN AUXCLIENT_VCPayloadTableUpdateRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo);

BOOLEAN AUXCLIENT_VCPayloadTableStatusRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo);

VOID AUXHELPER_GetReceiverCapability(PUCHAR pucDPCDBuff, PRECEIVER_CAPS pReceiverCaps);

#endif