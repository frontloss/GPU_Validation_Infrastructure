
#ifndef __GEN11p5MMIO_H__
#define __GEN11p5MMIO_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "Gen11p5InterruptRegisters.h"
#include "CommonMMIO.h"

#define DDI_AUX_CTL_A_GEN11P5 0x64010
#define DDI_AUX_CTL_B_GEN11P5 0x64110
#define DDI_AUX_CTL_C_GEN11P5 0x64210
#define DDI_AUX_CTL_D_GEN11P5 0x64310
#define DDI_AUX_CTL_E_GEN11P5 0x64410
#define DDI_AUX_CTL_F_GEN11P5 0x64510
#define DDI_AUX_CTL_G_GEN11P5 0x64610
#define DDI_AUX_CTL_H_GEN11P5 0x64710
#define DDI_AUX_CTL_I_GEN11P5 0x64810

#define DDI_AUX_DATA_A_START_GEN11P5 0x64014 // 64014h - 64027h
#define DDI_AUX_DATA_A_END_GEN11P5 0x64024

#define DDI_AUX_DATA_B_START_GEN11P5 0x64114 // 64114h - 64127h
#define DDI_AUX_DATA_B_END_GEN11P5 0x64124

#define DDI_AUX_DATA_C_START_GEN11P5 0x64214 // 64214h - 64227h
#define DDI_AUX_DATA_C_END_GEN11P5 0x64224

#define DDI_AUX_DATA_D_START_GEN11P5 0x64314 // 64314h - 64327h
#define DDI_AUX_DATA_D_END_GEN11P5 0x64324

#define DDI_AUX_DATA_E_START_GEN11P5 0x64414 // 64414h - 64427h
#define DDI_AUX_DATA_E_END_GEN11P5 0x64424

#define DDI_AUX_DATA_F_START_GEN11P5 0x64514 // 64514h - 64527h
#define DDI_AUX_DATA_F_END_GEN11P5 0x64524

#define DDI_AUX_DATA_G_START_GEN11P5 0x64614 // 64614h - 64627h
#define DDI_AUX_DATA_G_END_GEN11P5 0x64624

#define DDI_AUX_DATA_H_START_GEN11P5 0x64714 // 64714h - 64727h
#define DDI_AUX_DATA_H_END_GEN11P5 0x64724

#define DDI_AUX_DATA_I_START_GEN11P5 0x64814 // 64814h - 64827h
#define DDI_AUX_DATA_I_END_GEN11P5 0x64824

#define GMBUS0 0xC5100
#define GMBUS1 0xC5104
#define GMBUS2 0xC5108
#define GMBUS3 0xC510C
#define GMBUS4 0xC5110
#define GMBUS5 0xC5120

typedef enum _DDI_BUF_CTL_INSTANCE_D11P5
{
    DDI_BUF_CTL_A_ADDR_D11P5     = 0x64000,
    DDI_BUF_CTL_B_ADDR_D11P5     = 0x64100,
    DDI_BUF_CTL_C_ADDR_D11P5     = 0x64200,
    DDI_BUF_CTL_USBC1_ADDR_D11P5 = 0x64300,
    DDI_BUF_CTL_USBC2_ADDR_D11P5 = 0x64400,
    DDI_BUF_CTL_USBC3_ADDR_D11P5 = 0x64500,
    DDI_BUF_CTL_USBC4_ADDR_D11P5 = 0x64600,
    DDI_BUF_CTL_USBC5_ADDR_D11P5 = 0x64700,
    DDI_BUF_CTL_USBC6_ADDR_D11P5 = 0x64800,
} DDI_BUF_CTL_INSTANCE_D11P5;

/*****************************************************************************
Description:  Do not read or write the register when the associated power well is disabled.

******************************************************************************/
typedef union _DDI_BUF_CTL_D11P5 {
    struct
    {
        /******************************************************************************************************************
        Strap indicating whether a display was detected on this port during initialization. It signifies the level of the port detect pin at boot. This bit is only informative. It
        does not prevent this port from being enabled in hardware. This field only indicates the DDIA detection. Detection for other ports is read from SFUSE_STRAP.

        \******************************************************************************************************************/
        DDU32 InitDisplayDetected : DD_BITFIELD_BIT(0); // INIT_DISPLAY_DETECTED

        /******************************************************************************************************************
        This bit selects the number of lanes to be enabled on the DDI link for DisplayPort.

        Programming Notes:
        Restriction : When in DisplayPort mode the value selected here must match the value selected in TRANS_DDI_FUNC_CTL attached to this DDI.Restriction : This field must not be
        changed while the DDI is enabled.

        \******************************************************************************************************************/
        DDU32 DpPortWidthSelection : DD_BITFIELD_RANGE(1, 3); // DP_PORT_WIDTH_SELECTION

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(4); // RESERVED

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(5, 6); // RESERVED

        /******************************************************************************************************************
        This bit indicates when the DDI buffer is idle.

        \******************************************************************************************************************/
        DDU32 DdiIdleStatus : DD_BITFIELD_BIT(7); // DDI_IDLE_STATUS

        /******************************************************************************************************************
        Specifies the number of symbol clocks delay used to stagger assertion/deassertion of the port lane enables. The target time recommended by circuit team is 100ns or greater.
        The delay should be programmed based on link clock frequency. This staggering delay is ONLY required when the port is used in USB Type C mode. Otherwise the default delay
        is zero which means no staggering. Example: 270MHz link clock = 1/270MHz = 3.7ns. (100ns/3.7ns)=27.02 symbols. Round up to 28.

        \******************************************************************************************************************/
        DDU32 UsbTypeCDpLaneStaggeringDelay : DD_BITFIELD_RANGE(8, 15); //

        /******************************************************************************************************************
        This field enables lane reversal within the port.  Lane reversal swaps the data on the lanes as they are output from the port.

        Programming Notes:
        Restriction : This field must not be changed while the DDI is enabled.
        DDI E does not support reversal.Type-C/TBT dynamic connections:
        The DDIs going to thunderbolt or USB-C DP alternate mode should not be reversed here. The reversal is taken care of in the FIA.
        Static/fixed connections (DP/HDMI) through FIA:
        In the case of static connections such as "No pin assignment (Non Type-C DP)", DDIs will use this lane reversal bit.
        All other connections:
        DDIs will use this lane reversal bit.

        \******************************************************************************************************************/
        DDU32 PortReversal : DD_BITFIELD_BIT(16); // PORT_REVERSAL

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 23); // RESERVED

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(24, 27); // RESERVED

        /******************************************************************************************************************
        Enables adjustment of Phy parameters such as voltage swing and pre emphasis outside lnik training process.
        This field is conditioned on "override training enable" (DDI_BUF_CTL[29]).

        \******************************************************************************************************************/
        DDU32 PhyParamAdjust : DD_BITFIELD_BIT(28); // PHY_PARAM_ADJUST

        /******************************************************************************************************************
        This field enables the override on the training enable signal that tells the DDI I/O to pick up any DDI voltage swing and pre-emphasis changes.

        \******************************************************************************************************************/
        DDU32 OverrideTrainingEnable : DD_BITFIELD_BIT(29); // OVERRIDE_TRAINING_ENABLE

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(30); // RESERVED

        /******************************************************************************************************************
        This bit enables the DDI buffer.

        \******************************************************************************************************************/
        DDU32 DdiBufferEnable : DD_BITFIELD_BIT(31); // DDI_BUFFER_ENABLE
    };

    DDU32 Value;

} DDI_BUF_CTL_D11P5;

C_ASSERT(4 == sizeof(DDI_BUF_CTL_D11P5));

typedef enum _PWR_WELL_CTL_DDI_INSTANCE_D11P5
{
    PWR_WELL_CTL_DDI1_ADDR_D11P5 = 0x45450,
    PWR_WELL_CTL_DDI2_ADDR_D11P5 = 0x45454,
    PWR_WELL_CTL_DDI4_ADDR_D11P5 = 0x4545C,
} PWR_WELL_CTL_DDI_INSTANCE_D11P5;

/*****************************************************************************
Description:  This register is used for display power control. There are multiple instances of this register format to allow software components to have parallel control of the
display power. PWR_WELL_CTL _DDI1 is generally used for BIOS to control power. PWR_WELL_CTL_DDI2 is generally used for driver to control power. The power enable requests from all
sources are logically ORd together to enable the power, so the power will only disable after all sources have requested the power to disable. When a power well is disabled (powered
down), access to any registers in the power well will complete, but write data will be dropped and read data will be all zeroes. The display connections diagram indicates which
functional blocks are contained in each power well. The display MMIO register specification has a field for each register to indicate which power well it is in. PWR_WELL_CTL_DDI4
is used for debug power well control.Restriction : The power request field must not be changed for a resource while a power enable/disable for that resource is currently in
progress, as indicated by power well state for that resource.

******************************************************************************/
typedef union _PWR_WELL_CTL_DDI_D11P5 {
    struct
    {
        /******************************************************************************************************************
        This field indicates the status of power for DDI A IO.

        \******************************************************************************************************************/
        DDU32 DdiAIoPowerState : DD_BITFIELD_BIT(0); // DDI_A_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI A IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 DdiAIoPowerRequest : DD_BITFIELD_BIT(1); // DDI_A_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for DDI B IO.

        \******************************************************************************************************************/
        DDU32 DdiBIoPowerState : DD_BITFIELD_BIT(2); // DDI_B_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI B IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 DdiBIoPowerRequest : DD_BITFIELD_BIT(3); // DDI_B_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for DDI C IO.

        \******************************************************************************************************************/
        DDU32 DdiCIoPowerState : DD_BITFIELD_BIT(4); // DDI_C_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI C IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 DdiCIoPowerRequest : DD_BITFIELD_BIT(5); // DDI_C_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for USBC1 IO.

        \******************************************************************************************************************/
        DDU32 Usbc1IoPowerState : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        This field requests power for USBC1 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc1IoPowerRequest : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC2 IO.

        \******************************************************************************************************************/
        DDU32 Usbc2IoPowerState : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************
        This field requests power for USBC2 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc2IoPowerRequest : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC3 IO.

        \******************************************************************************************************************/
        DDU32 Usbc3IoPowerState : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************
        This field requests power for USBC3 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc3IoPowerRequest : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC4 IO.

        \******************************************************************************************************************/
        DDU32 Usbc4IoPowerState : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************
        This field requests power for USBC4 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc4IoPowerRequest : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC5 IO.

        \******************************************************************************************************************/
        DDU32 Usbc5IoPowerState : DD_BITFIELD_BIT(14); //

        /******************************************************************************************************************
        This field requests power for USBC5 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc5IoPowerRequest : DD_BITFIELD_BIT(15); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC6 IO.

        \******************************************************************************************************************/
        DDU32 Usbc6IoPowerState : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************
        This field requests power for USBC6 IO to enable or disable.

        \******************************************************************************************************************/
        DDU32 Usbc6IoPowerRequest : DD_BITFIELD_BIT(17); //

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 31); // RESERVED
    };

    DDU32 Value;

} PWR_WELL_CTL_DDI_D11P5;

C_ASSERT(4 == sizeof(PWR_WELL_CTL_DDI_D11P5));

BOOLEAN GEN11P5MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN11P5MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN11P5MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN11P5MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                               PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN GEN11P5MMIOHANDLERS_SetupInterruptRegistersForTE(PMMIO_INTERFACE pstMMIOInterface, MIPI_DSI_PORT_TYPE ePortType);

BOOLEAN GEN11P5MMIOHANDLERS_DdiBufferControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11P5MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
#endif // !__GEN11p5MMIO_H__
