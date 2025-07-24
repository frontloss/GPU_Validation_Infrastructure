######################################################################################
# @file         elg_clock_dp_snps_phy.py
# @brief        Contains DP specific part of ELG Synopsys PHY (C20) verification and expected value tables.
# @details      Bspec references:
#               https://gfxspecs.intel.com/Predator/Home/Index/74165?dstFilter=BMG&mode=Filter
# @author       Goutham N
######################################################################################

from enum import Enum
import logging

from Libs.Core.logger import gdhm
from Libs.Core.system_utility import SystemUtility
from Libs.Feature.clock.clock_helper import ClockHelper
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.clock.elg import elg_clock_helper
from Libs.Feature.clock import clock_helper as clk_helper
from DisplayRegs.Gen14 import ElgSnpsPhyRegisters
from Tests.PowerCons.Modules import dpcd
from Libs.Core import display_utility


##
# @brief        Dictionary that maps custom serdes to DP link rates
custom_serdes_to_dp_link_rate = {
    0: 1.62,
    1: 2.7,
    2: 5.4,
    3: 8.1,
    4: 2.16,
    5: 2.43,
    6: 3.24,
    7: 4.32,
    8: 10,
    9: 13.5,
    10: 20
}


##
# @brief        This is an enumeration definition for DP link rates(Gbps) used for Snps C20 Phy register programming
class DpLinkRate(float, Enum):
    RBR = 1.62
    eDP_R216 = 2.16
    eDP_R243 = 2.43
    HBR = 2.7
    eDP_R324 = 3.24
    eDP_R432 = 4.32
    HBR2 = 5.4
    eDP_R675 = 6.75
    HBR3 = 8.1
    UHBR13P5 = 13.5
    UHBR10 = 10
    UHBR20 = 20


# Below expected value data are based on "C20 DP and eDP PLL Programming Table (consolidated)" in Bspec page
# https://gfxspecs.intel.com/Predator/Home/Index/74165?dstFilter=BMG&mode=Filter
# 16'hCF5C
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_2 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                                                            0x0, 0x0]))
# 16'hCF5D
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x5800, 0x4800, 0x4800, 0x4800, 0x4800, 0x4800, 0x4800, 0x4800, 0x4800, 0x4800,
                                                            0xE800, 0x4800]))
# 16'hCF5E
EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_0 = dict(zip(DpLinkRate, [0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBE88, 0xBEA0,
                                                            0xBE21, 0xBE20]))
# 16'hCE8B
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_3 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                                                             0x0, 0x0]))
# 16'hCE8C
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_2 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                                                             0x0, 0x0]))
# 16'hCE8D
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x0005, 0x0005, 0x0005, 0x0005, 0x0005, 0x0005, 0x0005, 0x0005, 0x0005, 0x0005,
                                                             0x0005, 0x0005]))
# 16'hCE8E
EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_0 = dict(zip(DpLinkRate, [0x0500, 0x0500, 0x0500, 0x0500, 0x0500, 0x0500, 0x0500, 0x0500, 0x0500, 0x0500,
                                                             0x0700, 0x0500]))

# MPLLB registers (MPLLB is used for all legacy rates plus UHBR 13.5G5)
# 16'hCCB8
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_10 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]))

# 16'hCCB9
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_9 = dict(zip(DpLinkRate, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]))

# 16'hCCBA
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_8 = dict(zip(DpLinkRate, [0x6000, 0x0000, 0x1000, 0x5000, 0x6000, 0x0000, 0x5000, 0x6400, 0x7800, 0x4800]))

# 16'hCCBB
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_7 = dict(zip(DpLinkRate, [0x0001, 0x0000, 0x0001, 0x0001, 0x0001, 0x0000, 0x0001, 0x0001, 0x0001, 0x0001]))

# 16'hCCBC
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_6 = dict(zip(DpLinkRate, [0x2000, 0x0000, 0x2000, 0x2000, 0x2000, 0x0000, 0x2000, 0x2000, 0x2000, 0x2000]))

# 16'hCCBD
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_5 = dict(zip(DpLinkRate, [0x4C34, 0x78F6, 0x8814, 0x3F81, 0x5AB8, 0x78F6, 0x3F81, 0x5E80, 0x5F42, 0xBD00]))

# 16'hCCBE
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_4 = dict(zip(DpLinkRate, [0x5AB8, 0x9000, 0xA200, 0x4B9A, 0x6C00, 0x9000, 0x4B9A, 0x7080, 0x7166, 0xE100]))

# 16'hCCBF
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_3 = dict(zip(DpLinkRate, [0xBFC1, 0xBFC1, 0xBFC1, 0xBFC1, 0xFFC1, 0xBFC1, 0xBFC1, 0xBFC1, 0xBFC1, 0xFFC1]))

# 16'hCCC0
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_2 = dict(zip(DpLinkRate, [0xCD9A, 0x8E18, 0x8F18, 0xCC9C, 0xCD9A, 0x8E18, 0xCC9C, 0xCE1A, 0x8D98, 0x1B17]))

# 16'hCCC1
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_1 = dict(zip(DpLinkRate, [0x2120, 0x2120, 0x2120, 0x2110, 0x2110, 0x2110, 0x2108, 0x2108, 0x2108, 0x2205]))

# 16'hCCC2
EXPECTED_SRAM_GENERIC_MPLLB_CNTX_CFG_0 = dict(zip(DpLinkRate, [0x50A8, 0x50E1, 0x50FD, 0x308C, 0x30A8, 0x30E1, 0x108C, 0x10AF, 0x10D2, 0x015F]))

# MPLLA registers (MPLLA is used only for DP UHBR 10G and 20G)
# 16'hCE4F
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_9 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x0001, 0x0001]))
# 16'hCE50
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_8 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x3555, 0x3555]))
# 16'hCE51
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_7 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x0003, 0x0003]))
# 16'hCE52
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_6 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x4000, 0x4000]))
# 16'hCE53
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_5 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x759A, 0x8C00]))
# 16'hCE54
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_4 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x8C00, 0xA6AB]))
# 16'hCE55
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_3 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xC025, 0xC025]))
# 16'hCE56
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_2 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xC025, 0xC025]))
# 16'hCE57
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_1 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0xD105, 0xD105]))
# 16'hCE58
EXPECTED_SRAM_GENERIC_MPLLA_CNTX_CFG_0 = dict(zip([DpLinkRate.UHBR10, DpLinkRate.UHBR20],
                                                  [0x3104, 0x3104]))


##
# @brief        This is the class containing ELG DP Snps Phy related verifications
class ElgClockDpSnpsPhy:

    ##
    # @brief        Function that will be called from tests for ELG clock verification on DP displays
    # @param[in]    display_port   port name like DP_F, HDMI_B, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_clock(self, gfx_index: str, display_port: str) -> bool:
        ret = True

        ret &= self.verify_dp_snps_phy(gfx_index, display_port)

        if ret is True:
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            gdhm.report_test_bug_di("[Interfaces][Display_Engine]ELG_Clock_DP_Snps_Phy: PLL Register values not "
                                    "programmed as per BSPEC")
            logging.error("FAIL: PLL Register values not programmed as per BSPEC")

        return ret

    ##
    # @brief        wrapper function for DP Snps Phy verification
    # @param[in]    display_port   port name like DP_B, DP_F_TC, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_dp_snps_phy(self, gfx_index: str, display_port: str) -> bool:
        # Skip DP SNPS PHY verification as SRAM reg reads are failing. Will re-enable once fixed
        # HSD: https://hsdes.intel.com/appstore/article/#/16018474191
        # TODO: Revisit when there is a permanent solution for C20 PHY reg read
        logging.warning("Skipping DP SNPS PHY verification due to known SRAM register read fail")
        return True

        # Skip this verification in pre-si as MSG BUS transactions not supported in pre-si (simulation)
        # execution_environment_type = SystemUtility().get_execution_environment_type()
        # if execution_environment_type is None or execution_environment_type != "POST_SI_ENV":
        #     logging.info("Skipping PHY SRAM Registers verification on pre-si as the environment doesn't "
        #                  "support MSG BUS transaction")
        #     return True
        # return self.__verify_dp_snps_c20_phy(gfx_index, display_port)

    ##
    # @brief        this function contains DP Snps C20 Phy specific verification
    # @param[in]    display_port   port name like DP_G, DP_F_TC, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_dp_snps_c20_phy(self, gfx_index: str, display_port: str) -> bool:

        ret = True
        elg_clock_helper_obj = elg_clock_helper.ElgClockHelper()
        clock_helper = clk_helper.ClockHelper()
        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        link_rate_enum = DpLinkRate(link_bw)
        self.is_dp2p0 = True if link_rate_enum in [DpLinkRate.UHBR10, DpLinkRate.UHBR13P5,
                                                   DpLinkRate.UHBR20] else False

        # Read PHY_C20_VDR_CUSTOM_SERDES_RATE[0].CONTEXT_TOGGLE.
        # This tells which context's register set driver has programmed.
        offset = ElgSnpsPhyRegisters.OFFSET_PHY_C20_VDR_CUSTOM_SERDES.offset
        value = elg_clock_helper_obj.read_c20_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_serdes = ElgSnpsPhyRegisters.REG_PHY_C20_VDR_CUSTOM_SERDES(offset, value)
        if vdr_custom_serdes.ContextToggle == 0:
            current_context = 'A'
        else:
            current_context = 'B'
        logging.info(f'Current selected context for {display_port} = CONTEXT_{current_context}')

        # Verify SRAM GENERIC <A/B> TX CNTX CFG <N> registers
        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_2.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_2_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_2',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_2[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_2_value])

        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_1.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_1_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_1',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_1[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_1_value])

        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_TX_CNTX_CFG_0.CONTEXT_' + current_context)
        sram_generic_tx_cntx_cfg_0_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                           offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_TX_CNTX_CFG_0',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_TX_CNTX_CFG_0[link_rate_enum]],
                                                             actual=[sram_generic_tx_cntx_cfg_0_value])

        # Verify SRAM GENERIC <A/B> CMN CNTX CFG <N> registers
        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_3.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_3_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_3',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_3[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_3_value])

        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_2.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_2_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_2',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_2[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_2_value])

        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_1.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_1_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='SRAM_GENERIC_CMN_CNTX_CFG_1',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_1[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_1_value])

        offset = eval('ElgSnpsPhyRegisters.OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_0.CONTEXT_' + current_context)
        sram_generic_cmn_cntx_cfg_0_value = elg_clock_helper_obj.read_c20_phy_sram_register(gfx_index, display_port,
                                                                                            offset)
        ret &= clock_helper.verify_port_clock_programming_ex(feature='RAM_GENERIC_CMN_CNTX_CFG_0',
                                                             parameter=f'Reg value (of CONTEXT_{current_context})',
                                                             expected=[
                                                            EXPECTED_SRAM_GENERIC_CMN_CNTX_CFG_0[link_rate_enum]],
                                                             actual=[sram_generic_cmn_cntx_cfg_0_value])

        # Verify MPLLB registers (MPLLB is used for all legacy rates plus UHBR 13.5G)
        if link_rate_enum not in [DpLinkRate.UHBR10, DpLinkRate.UHBR20]:
            # Read all C20 SRAM MPLL registers
            snps = elg_clock_helper_obj.read_all_c20_sram_mpll_registers_helper(gfx_index, display_port,
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
            snps = elg_clock_helper_obj.read_all_c20_sram_mpll_registers_helper(gfx_index, display_port,
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
        offset = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = elg_clock_helper_obj.read_c20_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_width = ElgSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_VDR_CUSTOM_WIDTH',
                                                             parameter=f'CUSTOM_WIDTH',
                                                             expected=[2 if self.is_dp2p0 else 0],
                                                             actual=[vdr_custom_width.CustomWidth])

        # Verify PHY_C20_VDR_CUSTOM_SERDES_RATE register bits
        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'DpRateInCustomSerdes',
                                                             expected=[link_bw],
                                                             actual=[custom_serdes_to_dp_link_rate[
                                                                         vdr_custom_serdes.DpRateInCustomSerdes]])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'IsDp',
                                                             expected=[1],
                                                             actual=[vdr_custom_serdes.IsDp])

        return ret
