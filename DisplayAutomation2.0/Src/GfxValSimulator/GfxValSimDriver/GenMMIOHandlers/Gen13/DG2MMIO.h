#ifndef __DG2_MMIO_H__
#define __DG2_MMIO_H__

#include "Gen13CommonMMIO.h"

typedef enum _GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_DG2
{
    GFX_MSTR_TILE_INTR_ADDR_DG2 = 0x190008,
} GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_DG2;

/*************************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the corresponding GT Tiles

*************************************************************************************/
typedef union _GRAPHICS_MASTER_TILE_INTERRUPT_DG2 {
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

} GRAPHICS_MASTER_TILE_INTERRUPT_DG2, *PGRAPHICS_MASTER_TILE_INTERRUPT_DG2;

C_ASSERT(4 == sizeof(GRAPHICS_MASTER_TILE_INTERRUPT_DG2));

/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/
typedef enum _HPD_STATUS_ENUM_DG2
{
    HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_DG2    = 0x0,
    HPD_STATUS_SHORT_PULSE_DETECTED_DG2           = 0x1,
    HPD_STATUS_LONG_PULSE_DETECTED_DG2            = 0x2,
    HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_DG2 = 0x3,

} HPD_STATUS_ENUM_DG2;

typedef enum _SHOTPLUG_CTL_DDI_INSTANCE_DG2
{
    SHOTPLUG_CTL_DDI_ADDR_DG2 = 0xC4030,
} SHOTPLUG_CTL_DDI_INSTANCE_DG2;

/*****************************************************************************
Description:   The status fields indicate the hot plug detect status on each DDI combo PHY port. When HPD is enabled and either a long or short pulse is detected for a port, one of
the status bits will set and the hotplug IIR will be set (if unmasked in the IMR). The status bits are sticky bits, cleared by writing 1s to the bits. Each HPD pin can be
configured as an input or output. The HPD status function will only work when the pin is configured as an input. The HPD Output Data function will only work when the HPD pin is
configured as an output.The short pulse duration is programmed in SHPD_PULSE_CNT.

******************************************************************************/
typedef union _SHOTPLUG_CTL_DDI_DG2 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 DdiaHpdStatus : DD_BITFIELD_RANGE(0, 1); // DDIA_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 DdiaHpdOutputData : DD_BITFIELD_BIT(2); // DDIA_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 DdiaHpdEnable : DD_BITFIELD_BIT(3); // DDIA_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 DdibHpdStatus : DD_BITFIELD_RANGE(4, 5); // DDIB_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 DdibHpdOutputData : DD_BITFIELD_BIT(6); // DDIB_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 DdibHpdEnable : DD_BITFIELD_BIT(7); // DDIB_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 DdicHpdStatus : DD_BITFIELD_RANGE(8, 9); // DDIC_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 DdicHpdOutputData : DD_BITFIELD_BIT(10); // DDIC_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 DdicHpdEnable : DD_BITFIELD_BIT(11); // DDIC_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 DdidHpdStatus : DD_BITFIELD_RANGE(12, 13); // DDID_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 DdidHpdOutputData : DD_BITFIELD_BIT(14); // DDID_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 DdidHpdEnable : DD_BITFIELD_BIT(15); // DDID_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); //
    };

    DDU32 Value;

} SHOTPLUG_CTL_DDI_DG2;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_DG2));
/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/

typedef enum _SHOTPLUG_CTL_TC_INSTANCE_DG2
{
    SHOTPLUG_CTL_TC_ADDR_DG2 = 0xC4034,
} SHOTPLUG_CTL_TC_INSTANCE_DG2;

/*****************************************************************************
Description:   The status fields indicate the hot plug detect status on each type C port when using non-type C connectors (legacy or static configuration). When HPD is enabled and
either a long or short pulse is detected for a port, one of the status bits will set and the hotplug IIR will be set (if unmasked in the IMR). The status bits are sticky bits,
cleared by writing 1s to the bits. The short pulse duration is programmed in SHPD_PULSE_CNT.

******************************************************************************/
typedef union _SHOTPLUG_CTL_TC_DG2 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 Tc1HpdStatus : DD_BITFIELD_RANGE(0, 1); // TC1_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc1HpdOutputData : DD_BITFIELD_BIT(2); // TC1_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc1HpdEnable : DD_BITFIELD_BIT(3); // TC1_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 31); //
    };

    DDU32 Value;

} SHOTPLUG_CTL_TC_DG2;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_DG2));

/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/

/*********************************************************************************
*********************************************************************************/
typedef enum _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_DG2
{
    SDE_ISR_ADDR_DG2 = 0xC4000,
    SDE_IMR_ADDR_DG2 = 0xC4004,
    SDE_IIR_ADDR_DG2 = 0xC4008,
    SDE_IER_ADDR_DG2 = 0xC400C,
} SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_DG2;
/*****************************************************************************
Description:  South Display Engine (SDE) interrupt bits come from events within the south display engine. The SDE_IIR bits are ORed together to generate the South/PCH Display
Interrupt Event which will appear in the North Display Engine Interrupt Control Registers. The South Display Engine Interrupt Control Registers all share the same bit definitions
from this table. Due to the possibility of back to back Hotplug events it is recommended that software filters the value read from the Hotplug ISRs. A wake pin is driven with the
inverted value of the south display interrupt event line. The output of the wake pin is used to exit any power state that may prevent the interrupt from propagating to driver. When
any interrupt is enabled, the I/O buffer will be enabled for the Wake pin.

******************************************************************************/
typedef union _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 {
    struct
    {
        /******************************************************************************************************************
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \******************************************************************************************************************/
        DDU32 ScdcDdia : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \******************************************************************************************************************/
        DDU32 ScdcDdib : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \******************************************************************************************************************/
        DDU32 ScdcDdic : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \******************************************************************************************************************/
        DDU32 ScdcDdid : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 8); //

        /******************************************************************************************************************
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \******************************************************************************************************************/
        DDU32 ScdcTypecPort1 : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(10, 15); //

        /******************************************************************************************************************
        The ISR indicates the live value of the hotplug line when hotplug detect is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port Hot
        Plug Control Register.
        \******************************************************************************************************************/
        DDU32 HotplugDdia : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************
        The ISR indicates the live value of the hotplug line when hotplug detect is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port Hot
        Plug Control Register.
        \******************************************************************************************************************/
        DDU32 HotplugDdib : DD_BITFIELD_BIT(17); //

        /******************************************************************************************************************
        The ISR indicates the live value of the hotplug line when hotplug detect is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port Hot
        Plug Control Register.
        \******************************************************************************************************************/
        DDU32 HotplugDdic : DD_BITFIELD_BIT(18); //

        /******************************************************************************************************************
        The ISR indicates the live value of the hotplug line when hotplug detect is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port Hot
        Plug Control Register.
        \******************************************************************************************************************/
        DDU32 HotplugDdid : DD_BITFIELD_BIT(19); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(20, 22); //

        /******************************************************************************************************************
        This is an active high pulse when any of the events unmasked events in GMBUS4 Interrupt Mask register occur.
        \******************************************************************************************************************/
        DDU32 Gmbus : DD_BITFIELD_BIT(23); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(24); //

        /******************************************************************************************************************
        The ISR indicates the live value of the hotplug line when hotplug detect is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port Hot
        Plug Control Register.
        \******************************************************************************************************************/
        DDU32 HotplugTypecPort1 : DD_BITFIELD_BIT(25); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(26, 31); //
    };

    DDU32 Value;

} SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2;

C_ASSERT(4 == sizeof(SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2));

/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/

typedef enum _DPALT_DP4_ENUM_DG2
{
    DPALT_DP4_2_LANES_ACCESSIBLE_DG2 = 0x0,
    DPALT_DP4_4_LANES_ACCESSIBLE_DG2 = 0x1,

} DPALT_DP4_ENUM_DG2;

typedef enum _SNPS_PHY_TYPEC_STATUS_INSTANCE_DG2
{
    SNPS_PHY_TYPEC_STATUS_PORT_A_ADDR_DG2   = 0x168400,
    SNPS_PHY_TYPEC_STATUS_PORT_B_ADDR_DG2   = 0x169400,
    SNPS_PHY_TYPEC_STATUS_PORT_C_ADDR_DG2   = 0x16A400,
    SNPS_PHY_TYPEC_STATUS_PORT_D_ADDR_DG2   = 0x16B400,
    SNPS_PHY_TYPEC_STATUS_PORT_TC1_ADDR_DG2 = 0x16D400,
} SNPS_PHY_TYPEC_STATUS_INSTANCE_DG2;

/*****************************************************************************
Description:   This register is not reset by the device 2 FLR.

******************************************************************************/
typedef union _SNPS_PHY_TYPEC_STATUS_DG2 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 27); //

        /******************************************************************************************************************
         SW asserts this signal in response to dpalt_disable request from TCA only when PHY_MISC1[select_SW_seq] register bit is set. This bit should be at default when
        PHY_MISC1[select_SW_seq] register bit is not set.
        \******************************************************************************************************************/
        DDU32 Dpalt_Disable_Ack : DD_BITFIELD_BIT(28); //

        /******************************************************************************************************************
         DP ALT mode DP2/DP4 indication - whether 2 lanes or 4 lanes are accessible to DP controller. DP2 always uses the lower 2 TX lanes.
        \******************************************************************************************************************/
        DDU32 Dpalt_Dp4 : DD_BITFIELD_BIT(29); // DPALT_DP4

        /******************************************************************************************************************
         This is a status signal for driver to read. This bit indicates DP controller acknowledge to DP Alt mode disable/enable request. This is in response to dpalt_disable
        request from TCA.
        \******************************************************************************************************************/
        DDU32 Dpalt_Disable_Ack_Status : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************
         DP Alt-mode Disable/Enable request. TCA asserts this signal to tell the DP controller that DP alt mode is disabled. The DP controller should disable lanes it controls and
        respond with dpalt_disable_ack. TCA de-asserts ths signal to let the DP controller know that DP alt mode is required. The DP controller should configure and enable lanes it
        controls.
        \******************************************************************************************************************/
        DDU32 Dpalt_DisableLiveStatus : DD_BITFIELD_BIT(31); //
    };

    DDU32 Value;

} SNPS_PHY_TYPEC_STATUS_DG2;

C_ASSERT(4 == sizeof(SNPS_PHY_TYPEC_STATUS_DG2));

/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/

typedef enum _REFCLK_MUX_SELECT_ENUM_DG2
{
    REFCLK_MUX_SELECT_100_MHZ_DG2  = 0x1, // PHY is configured for native DP and HDMI connections.
    REFCLK_MUX_SELECT_38_4_MHZ_DG2 = 0x0, // PHY is configured for type-C connections.

} REFCLK_MUX_SELECT_ENUM_DG2;

typedef enum _SNPS_PHY_REF_CONTROL_INSTANCE_DG2
{
    SNPS_PHY_REF_CONTROL_PORT_A_ADDR_DG2   = 0x168188,
    SNPS_PHY_REF_CONTROL_PORT_B_ADDR_DG2   = 0x169188,
    SNPS_PHY_REF_CONTROL_PORT_C_ADDR_DG2   = 0x16A188,
    SNPS_PHY_REF_CONTROL_PORT_D_ADDR_DG2   = 0x16B188,
    SNPS_PHY_REF_CONTROL_PORT_TC1_ADDR_DG2 = 0x16C188,
} SNPS_PHY_REF_CONTROL_INSTANCE_DG2;

/*****************************************************************************
Description:   This register is not reset by the device 2 FLR.
******************************************************************************/
typedef union _SNPS_PHY_REF_CONTROL_DG2 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 12); //

        /******************************************************************************************************************
         For additional details, please review genlock page. This field selects the PLL input mux between internal 38.4 MHz crystal and external genlock reference. During reset,
        the genlock filter PLL locks with 38.4 MHz crystal because genlock won't be enabled until after boot. XCU unit has mux selection before the filter. Note that filter is
        always selected. When genlock is started after boot:the driver has to switch over to the genlock reference (slave). Refer to the table below. Mode Reference clock slave
        genlock mux select PLL output Non genlock 38.4 MHz crystal 0 100 MHz genlock master 38.4 MHz crystal 0 100 MHz genlock slave external genlock reference 1 100 MHz
        \******************************************************************************************************************/
        DDU32 FilterPllInputMuxSelect : DD_BITFIELD_BIT(13); // FILTER_PLL_INPUT_MUX_SELECT

        /******************************************************************************************************************
        This fields indicates the status of the PLL Lock.
        \******************************************************************************************************************/
        DDU32 FilterPllLock : DD_BITFIELD_BIT(14); // FILTER_PLL_LOCK

        /******************************************************************************************************************
         Default of this register bit is set to 1 so that all Combo PHY PLLs will pick up filtered reference clock automatically. SoC will fan out this register to all 4 combo PHY
        instances. XCU unit has mux selection before the filter. Note that filter is always selected. In filter bypass output reference clock will be 38.4 MHz.
        \******************************************************************************************************************/
        DDU32 FilterPllEnable : DD_BITFIELD_BIT(15); // FILTER_PLL_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 23); //

        /******************************************************************************************************************
         The purpose of this bit is read the current status of reference clock mux select for the type-C PHY. This bit will be set by SoC for 5th (type-C PORT_TC1) DE Shim instance
        only, and comes from the strap that selects between native and type-C connectivity for the PHY.
        \******************************************************************************************************************/
        DDU32 RefclkMuxSelect : DD_BITFIELD_BIT(24); // REFCLK_MUX_SELECT

        /******************************************************************************************************************
         The purpose of this bit is to request reference clock to the PHY. Reference clock to the PHY cannot be disabled when this bit is set.
        \******************************************************************************************************************/
        DDU32 Dp_Ref_Clk_Req : DD_BITFIELD_BIT(25); // DP_REF_CLK_REQ

        /******************************************************************************************************************
         This bit when set enables the MPLLB reference clock for the PHY. This bit must remain de-asserted until the reference clock is running at the appropriate frequency. The
        clock must be glitch-free at the primary reference clock input to the PHY. PHY CR interface is not available during the time reference clock is suspended.
        \******************************************************************************************************************/
        DDU32 Dp_Ref_Clk_En : DD_BITFIELD_BIT(26); // DP_REF_CLK_EN

        /******************************************************************************************************************
         Specifies the frequency range of the input reference clock (post ref_clk_div2_en division if any). Any change in this input must be done while dp_ref_clken=0 and
        ss_ref_clken=0 and phy_reset=1 or be followed by phy_reset assertion before using the phy. This value is ignored for the TC1 instance of this register. The type-C subsystem
        has a separate register to control it.
        \******************************************************************************************************************/
        DDU32 Ref_Range : DD_BITFIELD_RANGE(27, 31); //
    };

    DDU32 Value;

} SNPS_PHY_REF_CONTROL_DG2;

C_ASSERT(4 == sizeof(SNPS_PHY_REF_CONTROL_DG2));

#define IGT_PAVP_FUSE_2 0x9120

/* DG2 specific MMIO handlers*/
BOOLEAN DG2_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG2_MMIOHANDLERS_RegisterMasterTileInterrupt(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG2_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG2_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG2_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN DG2_MMIOHANDLERS_SetMasterTileInterrupt(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN DG2_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN DG2_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

/* MMIO Read/Write handlers registered specific to DG2 */
BOOLEAN DG2_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN DG2_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_SnpsTypecConfigure100MhzRefClkMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                       PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DG2_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN DG2_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs);
#endif
