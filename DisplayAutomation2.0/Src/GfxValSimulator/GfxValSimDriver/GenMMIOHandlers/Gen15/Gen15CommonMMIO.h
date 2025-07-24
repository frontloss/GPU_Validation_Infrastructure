
#ifndef __GEN15MMIO_H__
#define __GEN15MMIO_H__

#include "..\\CommonMMIO.h"
#include "..\\..\\CommonInclude\\BitDefs.h"
#include "..\\..\\CommonInclude\\\DisplayDefs.h"

#define DDI_AUX_CTL_A_GEN15 0x16FA10
#define DDI_AUX_CTL_B_GEN15 0x16FC10
#define DDI_AUX_CTL_TC1_GEN15 0x16F210
#define DDI_AUX_CTL_TC2_GEN15 0x16F410
#define DDI_AUX_CTL_TC3_GEN15 0x16F610
#define DDI_AUX_CTL_TC4_GEN15 0x16F810

#define DDI_AUX_DATA_A_START_GEN15 0x16FA14
#define DDI_AUX_DATA_A_END_GEN15 0x16FA24

#define DDI_AUX_DATA_B_START_GEN15 0x16FC14
#define DDI_AUX_DATA_B_END_GEN15 0x16FC24

#define DDI_AUX_DATA_TC1_START_GEN15 0x16F214
#define DDI_AUX_DATA_TC1_END_GEN15 0x16F224

#define DDI_AUX_DATA_TC2_START_GEN15 0x16F414
#define DDI_AUX_DATA_TC2_END_GEN15 0x16F424

#define DDI_AUX_DATA_TC3_START_GEN15 0x16F614
#define DDI_AUX_DATA_TC3_END_GEN15 0x16F624

#define DDI_AUX_DATA_TC4_START_GEN15 0x16F814
#define DDI_AUX_DATA_TC4_END_GEN15 0x16F824

typedef enum _HDMI_FRL_SHIFTER_ENABLE_ENUM_D15
{
    HDMI_FRL_SHIFTER_DISABLE_D15 = 0x0,
    HDMI_FRL_SHIFTER_ENABLE_D15  = 0x1,

} HDMI_FRL_SHIFTER_ENABLE_ENUM_D15;

typedef enum _TCSS_POWER_STATE_ENUM_D15
{
    TCSS_POWER_STATE_DISABLED_D15 = 0x0,
    TCSS_POWER_STATE_ENABLED_D15  = 0x1,

} TCSS_POWER_STATE_ENUM_D15;

typedef enum _TCSS_POWER_REQUEST_ENUM_D15
{
    TCSS_POWER_REQUEST_DISABLE_D15 = 0x0,
    TCSS_POWER_REQUEST_ENABLE_D15  = 0x1,

} TCSS_POWER_REQUEST_ENUM_D15;

typedef enum _TYPEC_PHY_OWNERSHIP_ENUM_D15
{
    TYPEC_PHY_OWNERSHIP_RELEASE_OWNERSHIP_D15 = 0x0,
    TYPEC_PHY_OWNERSHIP_TAKE_OWNERSHIP_D15    = 0x1,

} TYPEC_PHY_OWNERSHIP_ENUM_D15;

typedef enum _PHY_MODE_ENUM_D15
{
    PHY_MODE_CUSTOM_SERDES_D15 = 0x9,

} PHY_MODE_ENUM_D15;

typedef enum _PHY_LINK_RATE_ENUM_D15
{
    PHY_LINK_RATE_RATE_PROGRAMMED_THROUGH_MESSAGE_BUS_D15 = 0xF,

} PHY_LINK_RATE_ENUM_D15;

typedef enum _SOC_PHY_READY_ENUM_D15
{
    SOC_PHY_READY_NOT_READY_D15 = 0x0,
    SOC_PHY_READY_READY_D15     = 0x1,

} SOC_PHY_READY_ENUM_D15;

typedef enum _PORT_BUF_CTL1_INSTANCE_D15
{
    PORT_BUF_CTL1_USBC1_ADDR_D15 = 0x16F200,
    PORT_BUF_CTL1_USBC2_ADDR_D15 = 0x16F400,
    PORT_BUF_CTL1_USBC3_ADDR_D15 = 0x16F600,
    PORT_BUF_CTL1_USBC4_ADDR_D15 = 0x16F800,
    PORT_BUF_CTL1_A_ADDR_D15     = 0x16FA00,
    PORT_BUF_CTL1_B_ADDR_D15     = 0x16FC00,
} PORT_BUF_CTL1_INSTANCE_D15;

typedef enum _PIN_ASSIGNMENT_ENUM_D15
{
    PIN_ASSIGNMENT_ASSIGNMENT_C_D15 = 0x3,
    PIN_ASSIGNMENT_ASSIGNMENT_D_D15 = 0x4,
    PIN_ASSIGNMENT_ASSIGNMENT_E_D15 = 0x5,

} PIN_ASSIGNMENT_ENUM_D15;

typedef enum _TCSS_DDI_STATUS_INSTANCE_D15
{
    TCSS_DDI_STATUS_1_ADDR_D15 = 0x161500,
    TCSS_DDI_STATUS_2_ADDR_D15 = 0x161504,
    TCSS_DDI_STATUS_3_ADDR_D15 = 0x161508,
    TCSS_DDI_STATUS_4_ADDR_D15 = 0x16150C,
} TCSS_DDI_STATUS_INSTANCE_D15;

/*****************************************************************************
Description:

******************************************************************************/
typedef union _PORT_BUF_CTL1_D15 {
    struct
    {
        /******************************************************************************************************************
        This field enables the HDMI 2.1 FRL 18b to 20b shifting and data output.
        \******************************************************************************************************************/
        DDU32 HdmiFrlShifterEnable : DD_BITFIELD_BIT(0); // HDMI_FRL_SHIFTER_ENABLE

        /******************************************************************************************************************
        This field selects the number of transmit lanes to use.

        Programming Notes:
        Restriction : The value selected here must match the width selected in DDI_CTL_DE attached to this port and follow the restrictions listed there.
        \******************************************************************************************************************/
        DDU32 PortWidth : DD_BITFIELD_RANGE(1, 3); //

        /******************************************************************************************************************
        This field indicates the status of TCSS power.
        \******************************************************************************************************************/
        DDU32 TcssPowerState : DD_BITFIELD_BIT(4); // TCSS_POWER_STATE

        /******************************************************************************************************************
        This field requests TypeC Subsystem to power up to be accessible for display use. This field is ignored for ports not associated with type-C ports.
        \******************************************************************************************************************/
        DDU32 TcssPowerRequest : DD_BITFIELD_BIT(5); // TCSS_POWER_REQUEST

        /******************************************************************************************************************
         This field is configured to take ownership of the type-C PHY as part of the type-C connect and disconnect flows. This field is ignored for ports not associated with type-C
        ports. The ownership is de-asserted during reset preparation for FLR and warm resets.
        \******************************************************************************************************************/
        DDU32 TypecPhyOwnership : DD_BITFIELD_BIT(6); // TYPEC_PHY_OWNERSHIP

        /******************************************************************************************************************
        This bit indicates when the PHY is idle (electrical idle and power state Ready).
        \******************************************************************************************************************/
        DDU32 IdleStatus : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(8, 10); //

        /******************************************************************************************************************
        This field selects which IO path to use. It must not be switched while port is enabled.
        \******************************************************************************************************************/
        DDU32 IoSelect : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        PHYs that have frequency programmed in dividers through message bus use the default 1001 setting.
        \******************************************************************************************************************/
        DDU32 PhyMode : DD_BITFIELD_RANGE(12, 15); // PHY_MODE

        /******************************************************************************************************************
        This field indicates data has been lane reversed in the DDI.

        Programming Notes:
        Restriction : The value selected here must match the reversal selected in DDI_CTL_DE attached to this port and follow the restrictions listed there.
        \******************************************************************************************************************/
        DDU32 PortReversal : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(17); //

        /******************************************************************************************************************
         This value represents PHY data lane width. This field propagates to all PHY lanes assigned to display.

        Programming Notes:
        Restriction : The value selected here must match the value selected in DDI_CTL_DE attached to this port.
        \******************************************************************************************************************/
        DDU32 DataWidth : DD_BITFIELD_RANGE(18, 19); //

        /******************************************************************************************************************
        PHYs that have frequency programmed in dividers through message bus use the default all 1s setting.
        \******************************************************************************************************************/
        DDU32 PhyLinkRate : DD_BITFIELD_RANGE(20, 23); // PHY_LINK_RATE

        /******************************************************************************************************************
        This field indicates the SoC has made the PHY ready for use.
        \******************************************************************************************************************/
        DDU32 SocPhyReady : DD_BITFIELD_BIT(24); // SOC_PHY_READY

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(25, 27); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(28, 29); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(30, 31); //
    };

    DDU32 Value;

} PORT_BUF_CTL1_D15;

C_ASSERT(4 == sizeof(PORT_BUF_CTL1_D15));

/*****************************************************************************
Description:
******************************************************************************/
typedef union _TCSS_DDI_STATUS_D15 {
    struct
    {
        /******************************************************************************************************************
        HPD live status for dp_alt_mode. This drives the DP-alt HPD wire to DE.
        \******************************************************************************************************************/
        DDU32 Hpd_Live_Status_Alt : DD_BITFIELD_BIT(0); //
        /******************************************************************************************************************
        HPD live status for TBT. This drives the TBT HPD wire to DE.
        \******************************************************************************************************************/
        DDU32 Hpd_Live_Status_Tbt : DD_BITFIELD_BIT(1); //
        /******************************************************************************************************************
        PHY and FIA are ready for use for display in DP-alt or native/fixed/legacy modes. The value is a don't care for thunderbolt. PHY_READY_FOR_DE (AKA DPPMS)
        \******************************************************************************************************************/
        DDU32 Ready : DD_BITFIELD_BIT(2); //
        /******************************************************************************************************************
        Readback of display phy ownership wire (driven from DE), AKA SSS (safe state status).
        \******************************************************************************************************************/
        DDU32 Sss : DD_BITFIELD_BIT(3); //
        /******************************************************************************************************************
        Which type_c/TBT port HPD is sent from.
        \******************************************************************************************************************/
        DDU32 Src_Port_Num : DD_BITFIELD_RANGE(4, 7); //
        /******************************************************************************************************************
        HPD flow is in progress.
        \******************************************************************************************************************/
        DDU32 Hpd_In_Progress : DD_BITFIELD_BIT(8); //
        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 24); //

        /******************************************************************************************************************
         This field provides the type-C DP-alt pin assignment. Assignment D has 2 lanes available for display. Assignment C and E have 4 lanes available for display.
        \******************************************************************************************************************/
        DDU32 PinAssignment : DD_BITFIELD_RANGE(25, 28); // PIN_ASSIGNMENT

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); //
    };
    DDU32 Value;

} TCSS_DDI_STATUS_D15;
C_ASSERT(4 == sizeof(TCSS_DDI_STATUS_D15));

BOOLEAN GEN15_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN15_CMN_MMIOHANDLERS_PinAssignmentWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN15_CMN_MMIOHANDLERS_PinAssignmentReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

#endif // !__GEN15MMIO_H__
