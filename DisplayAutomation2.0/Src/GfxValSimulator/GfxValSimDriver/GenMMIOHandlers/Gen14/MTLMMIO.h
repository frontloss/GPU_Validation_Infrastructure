#ifndef __MTL_MMIO_H__
#define __MTL_MMIO_H__

#include "Gen14CommonMMIO.h"

typedef enum _GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_MTL
{
    GFX_MSTR_TILE_INTR_ADDR_MTL = 0x190008,
} GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_MTL;

/*************************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the corresponding GT Tiles

*************************************************************************************/
typedef union _GRAPHICS_MASTER_TILE_INTERRUPT_MTL {
    struct
    {
        DDU32 Tile0 : DD_BITFIELD_BIT(0);
        DDU32 Tile1 : DD_BITFIELD_BIT(1);
        DDU32 Tile2 : DD_BITFIELD_BIT(2);
        DDU32 Tile3 : DD_BITFIELD_BIT(3);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 30); // RESERVED
        /* This is the master control for graphics interrupts. This must be enabled for any of these interrupts to propagate to PCI device 2 interrupt processing*/
        DDU32 MasterInterrupt : DD_BITFIELD_BIT(31);
    };
    DDU32 Value;

} GRAPHICS_MASTER_TILE_INTERRUPT_MTL, *PGRAPHICS_MASTER_TILE_INTERRUPT_MTL;

C_ASSERT(4 == sizeof(GRAPHICS_MASTER_TILE_INTERRUPT_MTL));

#define IGT_PAVP_FUSE_2 0x9120

/* MTL specific MMIO handlers*/
BOOLEAN MTL_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN MTL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN MTL_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHanlder(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN MTL_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN MTL_MMIOHANDLERS_PICAHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN MTL_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs);
BOOLEAN MTL_MMIOHANDLERS_Psr1MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN MTL_MMIOHANDLERS_Psr2MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN PTL_SetEdpOnTypeC(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortNum);
BOOLEAN PTL_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN PTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN NVL_MMIOHANDLERS_SetupIOMRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                      PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN ELG_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
#endif
