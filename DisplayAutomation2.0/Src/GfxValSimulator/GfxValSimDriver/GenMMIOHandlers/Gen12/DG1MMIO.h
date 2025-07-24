#ifndef __DG1_MMIO_H__
#define __DG1_MMIO_H__

#include "Gen12CommonMMIO.h"
#include "DG1InterruptRegisters.h"

/* DG1 specific MMIO handlers*/
BOOLEAN DG1_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG1_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG1_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG1_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN DG1_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN DG1_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

/* MMIO Read/Write handlers registered specific to DG1 */
BOOLEAN DG1_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG1_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG1_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN DG1_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs);
#endif
