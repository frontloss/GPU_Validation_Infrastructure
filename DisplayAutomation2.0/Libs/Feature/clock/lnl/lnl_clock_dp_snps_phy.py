######################################################################################
# @file         lnl_clock_dp_snps_phy.py
# @brief        Contains DP specific part of LNL Synopsys PHY (both C10 and C20) verification and expected value tables.
# @details      Bspec references:
#               https://gfxspecs.intel.com/Predator/Home/Index/68862
# @author       Goutham N
######################################################################################

from enum import Enum
import logging

from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.clock.lnl import lnl_clock_helper
from Libs.Feature.clock import clock_helper as clk_helper
from DisplayRegs.Gen15 import LnlSnpsPhyRegisters
from Tests.PowerCons.Modules import dpcd
from Libs.Core import display_utility


##
# @brief        This is an enumeration definition for DP RATE IN CUSTOM SERDES
class DpRateInCustomSerdes(Enum):
    RATE_1_62 = 0, 1.62
    RATE_2_7 = 1, 2.7
    RATE_5_4 = 2, 5.4
    RATE_8_1 = 3, 8.1
    RATE_2_16 = 4, 2.16
    RATE_2_43 = 5, 2.43
    RATE_3_24 = 6, 3.24
    RATE_4_32 = 7, 4.32
    RATE_10 = 8, 10
    RATE_13_5 = 9, 13.5
    RATE_20 = 10, 20


##
# @brief        This is an enumeration definition for DP link rates(Gbps) used for Snps C20 Phy register programming
class DpLinkRate(float, Enum):
    RBR = 1.62
    HBR = 2.7
    HBR2 = 5.4
    HBR3 = 8.1
    UHBR13P5 = 13.5
    UHBR10 = 10
    UHBR20 = 20


##
# @brief        This is an enumeration definition for DP and eDP link rates(Gbps) used for Snps C10 Phy register programming
class C10DpLinkRate(float, Enum):
    LR_1P62 = 1.62
    LR_2P16 = 2.16
    LR_2P43 = 2.43
    LR_2P7 = 2.7
    LR_3P24 = 3.24
    LR_4P32 = 4.32
    LR_5P4 = 5.4
    LR_6P75 = 6.75
    LR_8P1 = 8.1


# Below expected value data are based on "C20 DP PLL Programming Table (consolidated)" in Bspec page
# https://gfxspecs.intel.com/Predator/Home/Index/68862
# 16'hCF2C
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_2 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                            0x0, 0x0]))
# 16'hCF2D
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x5800, 0x4800, 0x4800, 0x4800, 0x4800,
                                                            0x4800, 0x4800]))
# 16'hCF2E
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_0 = dict(zip(DpLinkRate, [0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBEA0,
                                                            0xBE21, 0xBE20]))
# 16'hCDA7
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_3 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                             0x0, 0x0]))
# 16'hCDA8
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_2 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                             0x0, 0x0]))
# 16'hCDA9
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x0005, 0x0005, 0x0005, 0x0005, 0x0005,
                                                             0x0005, 0x0005]))
# 16'hCDAA
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_0 = dict(zip(DpLinkRate, [0x0500, 0x0500, 0x0500, 0x0500, 0x0500,
                                                             0x0500, 0x0500]))

# MPLLB registers (only for RBR, HBR, HBR2, HBR3, UHBR13P5)
# 16'hCB50
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_10 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0]))

# 16'hCB51
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_9 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0]))

# 16'hCB52
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_8 = dict(zip(DpLinkRate, [0x6000, 0x5000, 0x5000, 0x7800, 0x4800]))

# 16'hCB53
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_7 = dict(zip(DpLinkRate, [0x0001, 0x0001, 0x0001, 0x0001, 0x0001]))

# 16'hCB54
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_6 = dict(zip(DpLinkRate, [0x2000, 0x2000, 0x2000, 0x2000, 0x2000]))

# 16'hCB55
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_5 = dict(zip(DpLinkRate, [0x4C34, 0x3F81, 0x3F81, 0x5F42, 0xBD00]))

# 16'hCB56
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_4 = dict(zip(DpLinkRate, [0x5AB8, 0x4B9A, 0x4B9A, 0x7166, 0xE100]))

# 16'hCB57
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_3 = dict(zip(DpLinkRate, [0xBFC1, 0xBFC1, 0xBFC1, 0xBFC1, 0xFFC1]))

# 16'hCB58
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_2 = dict(zip(DpLinkRate, [0xCD9A, 0xCC9C, 0xCC9C, 0x8D98, 0x1B17]))

# 16'hCB59
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x2120, 0x2110, 0x2108, 0x2108, 0x2205]))

# 16'hCB5A
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_0 = dict(zip(DpLinkRate, [0x50A8, 0x308C, 0x108C, 0x10D2, 0x015F]))

# MPLLA registers (only for UHBR10, UHBR20)
# 16'hCCE7
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_9 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x0001, 0x0001]))
# 16'hCCE8
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_8 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x3555, 0x3555]))
# 16'hCCE9
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_7 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x0003, 0x0003]))
# 16'hCCEA
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_6 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x4000, 0x4000]))
# 16'hCCEB
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_5 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x8C00, 0x8C00]))
# 16'hCCEC
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_4 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xA6AB, 0xA6AB]))
# 16'hCCED
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_3 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xC025, 0xC025]))
# 16'hCCEE
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_2 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xC025, 0xC025]))
# 16'hCCEF
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_1 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xD105, 0xD105]))
# 16'hCCF0
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_0 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x3104, 0x3104]))

# Below expected value data are based on "C10 DP PLL Programming Table (consolidated)" in Bspec page
# https://gfxspecs.intel.com/Predator/Home/Index/68862
# 0xC00
EXPECTED_PHY_C10_VDR_PLL0 = dict(zip(C10DpLinkRate, [0xB4, 0x4, 0x34, 0xF4, 0xB4,
                                                     0x4, 0xF4, 0xB4, 0x34]))
# 0xC01
EXPECTED_PHY_C10_VDR_PLL1 = dict(zip(C10DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                     0x0, 0x0, 0x0, 0x0]))
# 0xC02
EXPECTED_PHY_C10_VDR_PLL2 = dict(zip(C10DpLinkRate, [0x30, 0xA2, 0xDA, 0xF8, 0x30,
                                                     0xA2, 0xF8, 0x3E, 0x84]))
# 0xC03
EXPECTED_PHY_C10_VDR_PLL3 = dict(zip(C10DpLinkRate, [0x1, 0x1, 0x1, 0x0, 0x1,
                                                     0x1, 0x0, 0x1, 0x1]))
# 0xC04
EXPECTED_PHY_C10_VDR_PLL4_SSC = dict(zip(C10DpLinkRate, [0x26, 0x33, 0x39, 0x20, 0x26,
                                                         0x33, 0x20, 0xA8, 0x30]))
# 0xC05
EXPECTED_PHY_C10_VDR_PLL5_SSC = dict(zip(C10DpLinkRate, [0x0C, 0x10, 0x12, 0x0A, 0x0C,
                                                         0x10, 0x0A, 0x0C, 0x0F]))
# 0xC06
EXPECTED_PHY_C10_VDR_PLL6_SSC = dict(zip(C10DpLinkRate, [0x98, 0x75, 0xE3, 0x29, 0x98,
                                                         0x75, 0x29, 0x33, 0x3D]))
# 0xC07
EXPECTED_PHY_C10_VDR_PLL7_SSC = dict(zip(C10DpLinkRate, [0x46, 0xB3, 0xE9, 0x10, 0x46,
                                                         0xB3, 0x10, 0x54, 0x98]))
# 0xC08
EXPECTED_PHY_C10_VDR_PLL8_SSC = dict(zip(C10DpLinkRate, [0x1, 0x1, 0x1, 0x1, 0x1,
                                                         0x1, 0x1, 0x1, 0x1]))
# 0xC09
EXPECTED_PHY_C10_VDR_PLL9 = dict(zip(C10DpLinkRate, [0x1, 0x1, 0x1, 0x1, 0x1,
                                                     0x1, 0x1, 0x1, 0x1]))
# 0xC0A
EXPECTED_PHY_C10_VDR_PLL10 = dict(zip(C10DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                      0x0, 0x0, 0x0, 0x0]))
# 0xC0B
EXPECTED_PHY_C10_VDR_PLL11 = dict(zip(C10DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                      0x0, 0x0, 0x0, 0x0]))
# 0xC0C
EXPECTED_PHY_C10_VDR_PLL12 = dict(zip(C10DpLinkRate, [0xC0, 0x0, 0x20, 0xA0, 0xC0,
                                                      0x0, 0xA0, 0xC8, 0xF0]))
# 0xC0D
EXPECTED_PHY_C10_VDR_PLL13 = dict(zip(C10DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                      0x0, 0x0, 0x0, 0x0]))
# 0xC0E
EXPECTED_PHY_C10_VDR_PLL14 = dict(zip(C10DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0,
                                                      0x0, 0x0, 0x0, 0x0]))
# 0xC0F
EXPECTED_PHY_C10_VDR_PLL15 = dict(zip(C10DpLinkRate, [0x2, 0x2, 0x2, 0x1, 0x1,
                                                      0x1, 0x0, 0x0, 0x0]))
# 0xC10
EXPECTED_PHY_C10_VDR_PLL16 = dict(zip(C10DpLinkRate, [0x84, 0x85, 0x85, 0x84, 0x85,
                                                      0x85, 0x84, 0x85, 0x84]))
# 0xC11
EXPECTED_PHY_C10_VDR_PLL17 = dict(zip(C10DpLinkRate, [0x4F, 0x0F, 0x8F, 0x4F, 0x4F,
                                                      0x0F, 0x4F, 0x8F, 0x0F]))
# 0xC12
EXPECTED_PHY_C10_VDR_PLL18 = dict(zip(C10DpLinkRate, [0xE5, 0xE6, 0xE6, 0xE5, 0xE6,
                                                      0xE6, 0xE5, 0xE6, 0xE5]))
# 0xC13
EXPECTED_PHY_C10_VDR_PLL19 = dict(zip(C10DpLinkRate, [0x23, 0x23, 0x23, 0x23, 0x23,
                                                      0x23, 0x23, 0x23, 0x23]))
# 0xC20
EXPECTED_PHY_C10_VDR_CMN0 = dict(zip(C10DpLinkRate, [0x21, 0x21, 0x21, 0x21, 0x21,
                                                     0x21, 0x21, 0x21, 0x21]))
# 0xC30
EXPECTED_PHY_C10_VDR_TX0 = dict(zip(C10DpLinkRate, [0x10, 0x10, 0x10, 0x10, 0x10,
                                                    0x10, 0x10, 0x10, 0x10]))
# 0xC70
EXPECTED_PHY_C10_VDR_CONTROL1 = dict(zip(C10DpLinkRate, [0x6, 0x6, 0x6, 0x6, 0x6,
                                                         0x6, 0x6, 0x6, 0x6]))


##
# @brief        This is the class containing LNL DP Snps Phy related verifications
class LnlClockDpSnpsPhy:

    ##
    # @brief        Function that will be called from tests for LNL clock verification on DP displays
    # @param[in]    display_port   port name like DP_F, HDMI_B, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_clock(self, display_port: str, gfx_index: str) -> bool:
        ret = True
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        # Ports A and B use C10 PHY.
        # for PTL+ Port B use C20 PHY, Skipping PLL verification for Port_B
        if display_port == 'DP_B' and self.platform in ["PTL", "NVL"]:
            return ret
        ret &= self.verify_dp_snps_phy(display_port, gfx_index)

        if ret is True:
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            gdhm.report_test_bug_di("[Interfaces][Display_Engine]LNL_Clock_DP_Snps_Phy: PLL Register values not "
                                    "programmed as per BSPEC")
            logging.error("FAIL: PLL Register values not programmed as per BSPEC")

        return ret

    ##
    # @brief        wrapper function for DP Snps Phy verification
    # @param[in]    display_port   port name like DP_B, DP_F_TC, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_dp_snps_phy(self, display_port: str, gfx_index: str) -> bool:
        clock_helper = clk_helper.ClockHelper()
        port_name = str(display_port).split('_')[1]
        lnl_clock_helper_obj = lnl_clock_helper.LnlClockHelper()
        display_port_name = lnl_clock_helper_obj.ddi_to_bspec_name_map[port_name.upper()]
        target_id = clock_helper.get_target_id(display_port, gfx_index)

        # Ports A and B use C10 PHY.
        if 'USBC' not in display_port_name:
            # TODO: Temporary WA for SRAM register read failures, commenting out C10 PHY register reads
            # HSD: https://hsdes.intel.com/appstore/article/#/18025630496
            # TODO: Revisit when there is a permanent solution for C10 PHY reg read
            try:
                is_lfp = display_utility.get_vbt_panel_type(display_port, gfx_index) in \
                         [display_utility.VbtPanelType.LFP_DP]
            except Exception as e:
                logging.error("Exception : {0}".format(e))
                is_lfp = False
            if is_lfp:
                psr_ver = dpcd.get_psr_version(target_id)
                edp_rev = dpcd.get_edp_revision(target_id)
                # PSR1 is supported only on eDP 1.3+ panels
                # PSR2 is supported only on eDP 1.4+ panels
                if ((edp_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_3) and (psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_1) or
                        (edp_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4 and psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_2)):
                    return True
            return self.__verify_dp_snps_c10_phy(display_port, gfx_index)
        # All USBC ports use C20 PHY.
        else:
            # TODO: Temporary WA for SRAM register read failures, commenting out C20 PHY register reads
            # HSD: https://hsdes.intel.com/appstore/article/#/16018474191
            # TODO: Revisit when there is a permanent solution for C20 PHY reg read
            return True
            # return self.__verify_dp_snps_c20_phy(display_port, gfx_index)

    ##
    # @brief        this function contains eDP/DP Snps C10 Phy specific verification. For eDP/DP, C10 PHY uses MPLLB.
    # @param[in]    display_port   port name like EDP_A, DP_B, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_dp_snps_c10_phy(self, display_port: str, gfx_index: str) -> bool:

        ret = True
        clock_helper = clk_helper.ClockHelper()
        lnl_clock_helper_obj = lnl_clock_helper.LnlClockHelper()
        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        link_rate_enum = C10DpLinkRate(link_bw)
        is_ssc = clock_helper.get_ssc_from_dpcd(display_port, gfx_index)

        # Program PHY_C10_VDR_CONTROL1[2] to '1' before reading back programmed PHY configuration over the message bus.
        # As of now ignoring this to see if C10 PHY reads works properly without this operation.
        # TODO: If it doesn't work, we need to create API for write_C10_phy_vdr.

        # Read all C10 VDR registers
        snps = lnl_clock_helper_obj.read_all_c10_vdr_registers_helper(display_port, gfx_index)

        # Verify PLL specific VDR registers
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL0[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll0.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL1',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL1[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll1.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL2',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL2[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll2.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL3',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL3[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll3.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL4',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL4_SSC[link_rate_enum] if
                                                                  is_ssc else 0],
                                                             actual=[snps.phy_c10_vdr_pll4.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL5',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL5_SSC[link_rate_enum] if
                                                                  is_ssc else 0],
                                                             actual=[snps.phy_c10_vdr_pll5.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL6',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL6_SSC[link_rate_enum] if
                                                                  is_ssc else 0],
                                                             actual=[snps.phy_c10_vdr_pll6.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL7',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL7_SSC[link_rate_enum] if
                                                                  is_ssc else 0],
                                                             actual=[snps.phy_c10_vdr_pll7.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL8',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL8_SSC[link_rate_enum] if
                                                                  is_ssc else 0],
                                                             actual=[snps.phy_c10_vdr_pll8.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL9',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL9[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll9.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL10',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL10[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll10.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL11',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL11[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll11.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL12',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL12[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll12.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL13',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL13[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll13.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL14',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL14[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll14.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL15',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL15[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll15.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL16',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL16[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll16.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL17',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL17[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll17.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL18',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL18[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll18.value])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL19',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_PLL19[link_rate_enum]],
                                                             actual=[snps.phy_c10_vdr_pll19.value])

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CMN0.offset
        phy_c10_vdr_cmn0_value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_CMN0',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_CMN0[link_rate_enum]],
                                                             actual=[phy_c10_vdr_cmn0_value])

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_TX0.offset
        phy_c10_vdr_tx0_value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_TX0',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_TX0[link_rate_enum]],
                                                             actual=[phy_c10_vdr_tx0_value])

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CONTROL1.offset
        phy_c10_vdr_control1_value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_CONTROL1',
                                                             parameter='reg_value',
                                                             expected=[EXPECTED_PHY_C10_VDR_CONTROL1[link_rate_enum]],
                                                             actual=[phy_c10_vdr_control1_value])

        # Program custom width in VDR register at offset 0xD02 to match the link protocol (8b/10b mode (value 0) always
        # for C10 displays)
        offset = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_width = LnlSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_VDR_CUSTOM_WIDTH',
                                                             parameter='CUSTOM_WIDTH',
                                                             expected=[0],
                                                             actual=[vdr_custom_width.CustomWidth])

        return ret

    ##
    # @brief        this function contains DP Snps C20 Phy specific verification
    # @param[in]    display_port   port name like DP_G, DP_F_TC, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_dp_snps_c20_phy(self, display_port: str, gfx_index: str) -> bool:

        ret = True
        lnl_clock_helper_obj = lnl_clock_helper.LnlClockHelper()
        clock_helper = clk_helper.ClockHelper()
        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        link_rate_enum = DpLinkRate(link_bw)
        self.is_dp2p0 = True if link_rate_enum in [DpLinkRate.UHBR10, DpLinkRate.UHBR13P5,
                                                   DpLinkRate.UHBR20] else False

        # Read PHY_C20_VDR_CUSTOM_SERDES_RATE[0].CONTEXT_TOGGLE.
        # This tells which context's register set driver has programmed.
        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CUSTOM_SERDES.offset
        value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_serdes = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_CUSTOM_SERDES(offset, value)
        if vdr_custom_serdes.ContextToggle == 0:
            current_context = 'A'
        else:
            current_context = 'B'
        logging.info(f'Current selected context for {display_port} = CONTEXT_{current_context}')

        # Verify SRAM GENERIC <A/B> TX CNTX CFG <N> registers
        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_2.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_2_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_2',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_2[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_2_value])

        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_1.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_1_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_1',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_1[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_1_value])

        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_0.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_0_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_0',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_0[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_0_value])

        # Verify SRAM GENERIC <A/B> CMN CNTX CFG <N> registers
        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_3.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_3_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_3',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_3[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_3_value])

        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_2.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_2_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_2',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_2[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_2_value])

        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_1.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_1_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_1',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_1[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_1_value])

        offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_0.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_0_value = lnl_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='RAM_GENERIC_CMN_CNTX_CFG_0',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_0[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_0_value])

        # Verify MPLLB registers (only for RBR, HBR, HBR2, HBR3, UHBR13P5)
        if link_rate_enum not in [DpLinkRate.UHBR10, DpLinkRate.UHBR20]:
            # Read all C20 SRAM MPLL registers
            snps = lnl_clock_helper_obj.read_all_c20_sram_mpll_registers_helper(gfx_index, display_port,
                                                                                current_context,
                                                                                'MPLLB')

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_10',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_10[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_10.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_9',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_9[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_9.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_8',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_8[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_8.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_7',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_7[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_7.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_6',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_6[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_6.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_5',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_5[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_5.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_4',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_4[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_4.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_3',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_3[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_3.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_2',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_2[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_2.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_1',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_1[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_1.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLB_CNTX_CFG_0',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_0[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mpllb_cntx_cfg_0.value])

        # Verify MPLLA registers (only for UHBR10, UHBR20)
        else:
            # Read all C20 SRAM MPLL registers
            snps = lnl_clock_helper_obj.read_all_c20_sram_mpll_registers_helper(gfx_index, display_port,
                                                                                current_context, 'MPLLA')

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_9',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_9[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_9.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_8',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_8[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_8.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_7',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_7[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_7.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_6',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_6[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_6.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_5',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_5[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_5.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_4',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_4[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_4.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_3',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_3[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_3.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_2',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_2[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_2.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_1',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_1[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_1.value])

            ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_MPLLA_CNTX_CFG_0',
                                                                 parameter=f'Reg value (of CONTEXT_{current_context})',
                                                                 expected=[EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_0[
                                                                          link_rate_enum]],
                                                                 actual=[snps.sram_generic_mplla_cntx_cfg_0.value])

        # Program custom width in VDR register at offset 0xD02 to match the link protocol (DP 2.0, HDMI 2.1, etc.)
        offset = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = lnl_clock_helper_obj.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_width = LnlSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_VDR_CUSTOM_WIDTH',
                                                             parameter=f'CUSTOM_WIDTH',
                                                             expected=[2 if self.is_dp2p0 else 0],
                                                             actual=[vdr_custom_width.CustomWidth])

        # Verify PHY_C20_VDR_CUSTOM_SERDES_RATE register bits
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'DpRateInCustomSerdes',
                                                             expected=[link_bw],
                                                             actual=[DpRateInCustomSerdes(
                                                            vdr_custom_serdes.DpRateInCustomSerdes).value[1]])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'IsDp',
                                                             expected=[1],
                                                             actual=[vdr_custom_serdes.IsDp])

        return ret
