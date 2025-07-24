#ifndef __LKF_R_MMIO_H__
#define __LKF_R_MMIO_H__

#include "Gen12CommonMMIO.h"

BOOLEAN LKFR_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN LKFR_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN LKFR_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN LKFR_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                             PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN LKFR_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN LKFR_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

/*MMIO Read/Write handlers registered specific to LKF-R*/
BOOLEAN LKFR_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN LKFR_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN LKFR_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN LKFR_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

#endif