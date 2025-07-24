##
# @file     dg1_clock_edp.py
# @brief  This tests EDP PLLS are programmed correctly for platform DG1. Can be used in EDP tests.
# @author  Kruti Vadhavaniya

import logging

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.dg1 import dg1_clock_registers
from Libs.Feature.display_port import dpcd_helper
from Libs.Core.logger import gdhm

clock_helper = clk_helper.ClockHelper()
dg1_clock_reg = dg1_clock_registers.Dg1ClockRegisters()
edp = 0


##
# @brief Clock register class
class ClockRegister():
    DPLL_CFGCR0 = ''
    DPLL_CFGCR1 = ''
    DPLL_SSC = ''


##
# @brief edp/Dp Clock CFGCR0 register class
class EdpClockCFGCR0():
    SSC_ENABLE = 0
    DCO_INT = 0
    DCO_FRAC = 0


##
# @brief edp/Dp Clock CFGCR1 register class
class EdpClockCFGCR1():
    PDIV = 0
    KDIV = 0
    QDIV = 0
    QDIV_RATIO = 0
    CENTRAL_FREQ = 0


##
# @brief Central frequency mapping dictionary
central_frequency_map = dict([
    (9600, 0),
    (9000, 1),
    (8400, 3)
])


##
# @brief DG1 edp clock verification class
class Dg1ClockEdp():
    # Mapping of the listed DPLLs that can be used
    ddi_pll_0_1_map = dict([
        ('DPLL0', 0),
        ('DPLL1', 1),
        ('DPLL2', 2)
    ])

    ddi_pll_2_3_map = dict([
        ('DPLL2', 0),
        ('DPLL3', 1)
    ])

    # Mapping of the listed Reference Frequencies
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2),
        (25, 3)
    ])

    ##
    # @brief function to validate EDP Pll divider values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        logging.debug("Check for which DPLL is being used")
        reg_value_DPCLKA0_CFGCR0 = clock_helper.clock_register_read('DPCLKA0_CFGCR0_REGISTER', 'DPCLKA0_CFGCR0', gfx_index)
        reg_value_DPCLKA1_CFGCR0 = clock_helper.clock_register_read('DPCLKA1_CFGCR0_REGISTER', 'DPCLKA1_CFGCR0', gfx_index)
        if str(display_port).upper().__contains__('_A'):
            dpllValue = clock_helper.get_value_by_range(reg_value_DPCLKA0_CFGCR0, 0, 1, self.ddi_pll_0_1_map, 'DPLL')
        elif str(display_port).upper().__contains__('_B'):
            dpllValue = clock_helper.get_value_by_range(reg_value_DPCLKA0_CFGCR0, 2, 3, self.ddi_pll_0_1_map, 'DPLL')
        elif str(display_port).upper().__contains__('_C'):
            dpllValue = clock_helper.get_value_by_range(reg_value_DPCLKA1_CFGCR0, 0, 1, self.ddi_pll_2_3_map, 'DPLL')
        elif str(display_port).upper().__contains__('_D'):
            dpllValue = clock_helper.get_value_by_range(reg_value_DPCLKA1_CFGCR0, 2, 3, self.ddi_pll_2_3_map, 'DPLL')
        else:
            logging.info("ERROR:Provided port is not valid for Dash-G")

        ClockRegister.DPLL_CFGCR0 = dpllValue + '_CFGCR0'
        ClockRegister.DPLL_CFGCR1 = dpllValue + '_CFGCR1'
        ClockRegister.DPLL_SSC = dpllValue + '_SSC'

        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        reg_value = clock_helper.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        ref_clk = clock_helper \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")

        ret, pll_values = self.get_edp_pll_ref_values(link_bw, ref_clk)

        if (ret is True):
            if (True == self.verify_edp_pll(pll_values, display_port, gfx_index)):
                logging.debug("PASS : PLL Register values Programmed as per BSPEC")
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine]DG1_Clock_EDP: PLL Register values {0} not programmed as "
                          "per BSPEC".format(pll_values),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL : PLL Register values NOT Programmed as per BSPEC")
                ret = False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]DG1_Clock_EDP:Failed getting reference pll values"
                      " for: link rate {0} ref clk {1}".format(str(link_bw), str(ref_clk)),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Failed getting Reference PLL values for Link Rate: "
                          + str(link_bw) + "ref clk :" + str(ref_clk))
            ret = False

        return ret

    ##
    # @brief function to validate EDP Pll divider values are programmed correctly.
    # @param[in] pll_values - Pll_values dictionary
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which register read
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_edp_pll(self, pll_values, display_port, gfx_index='gfx_0'):
        ret = True

        dco_integer = pll_values["dco_integer"]
        dco_fraction = pll_values["dco_fraction"]
        pdiv = pll_values["pdiv"]
        kdiv = pll_values["kdiv"]
        qdiv_mode = pll_values["qdiv_mode"]
        qdiv_ratio = pll_values["qdiv_ratio"]
        ssc_enable = clock_helper.get_ssc_from_dpcd(display_port, gfx_index)

        reg_DPLL_CFGCR0 = clock_helper.clock_register_read('DPLL_CFGCR0_REGISTER', ClockRegister.DPLL_CFGCR0, gfx_index)
        reg_DPLL_CFGCR1 = clock_helper.clock_register_read('DPLL_CFGCR1_REGISTER', ClockRegister.DPLL_CFGCR1, gfx_index)
        reg_DPLL_SSC = clock_helper.clock_register_read('DPLL_SSC_REGISTER', ClockRegister.DPLL_SSC, gfx_index)

        reg_read_CFGCR0 = EdpClockCFGCR0()
        reg_read_CFGCR0.SSC_ENABLE = clock_helper.get_value_by_range(reg_DPLL_SSC, 9, 9, '', 'SSC Enable')
        reg_read_CFGCR0.DCO_INT = clock_helper.get_value_by_range(reg_DPLL_CFGCR0, 0, 9, '', 'DCO Integer')
        reg_read_CFGCR0.DCO_FRAC = clock_helper.get_value_by_range(reg_DPLL_CFGCR0, 10, 24, '', 'DCO Fraction')

        reg_read_CFGCR1 = EdpClockCFGCR1()
        reg_read_CFGCR1.PDIV = clock_helper.get_value_by_range(reg_DPLL_CFGCR1, 2, 5, '', 'PDIV')
        reg_read_CFGCR1.KDIV = clock_helper.get_value_by_range(reg_DPLL_CFGCR1, 6, 8, '', 'KDIV')
        reg_read_CFGCR1.QDIV = clock_helper.get_value_by_range(reg_DPLL_CFGCR1, 9, 9, '', 'QDIV')
        reg_read_CFGCR1.QDIV_RATIO = clock_helper.get_value_by_range(reg_DPLL_CFGCR1, 10, 17, '', 'QDIV Ratio')
        reg_read_CFGCR1.CENTRAL_FREQ = clock_helper.get_value_by_range(reg_DPLL_CFGCR1, 0, 1, central_frequency_map,
                                                                       'Central Frequency')

        # read from vbt and dpcd dpcd:0x3h oth bit = 0:no ssc 1: upto 50% downspread

        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR0),
                                                             parameter=['DCO Integer', 'DCO Fraction'],
                                                             expected=[dco_integer, dco_fraction],
                                                             actual=[reg_read_CFGCR0.DCO_INT, reg_read_CFGCR0.DCO_FRAC])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_SSC),
                                                             parameter=['SSC Enable'],
                                                             expected=[ssc_enable], actual=[reg_read_CFGCR0.SSC_ENABLE])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR1),
                                                             parameter=['PDiv', 'KDiv', 'QDiv Mode', 'QDIV Ratio'],
                                                             expected=[pdiv, kdiv, qdiv_mode, qdiv_ratio],
                                                             actual=[reg_read_CFGCR1.PDIV, reg_read_CFGCR1.KDIV,
                                                                reg_read_CFGCR1.QDIV, reg_read_CFGCR1.QDIV_RATIO])

        if (reg_read_CFGCR1.CENTRAL_FREQ != 8400):
            logging.warning("{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: [{act}]".format(res="WARN",
                                                                                                   feature="DPCLKA_CFGCR0 & {} - Central Frequency in MHz".format(
                                                                                                       ClockRegister.DPLL_CFGCR1),
                                                                                                   exp="[{0}]".format(
                                                                                                       '8400'), act=str(
                    reg_read_CFGCR1.CENTRAL_FREQ)))
        else:
            ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR1),
                                                                 parameter="Central Frequency in MHz",
                                                                 expected=['8400'], actual=[
                    str(reg_read_CFGCR1.CENTRAL_FREQ)])  # 11 : 8400 MHz . SW should not program

        return ret

    ##
    # @brief function to get reference pll divider values based on bspec.
    # @param[in] link_bw - Link Rate.
    # @param[in] ref_clk : Reference Clock for platform.
    # @return ret - BOOL ( True /False ), pll_values (pll_values dictionary )
    def get_edp_pll_ref_values(self, link_bw, ref_clk):
        pll_values = []
        ret = True

        logging.debug("Get Reference EDP PLL Values for ref_clk = " + str(ref_clk)
                      + " & link_rate = " + str(link_bw))

        if ref_clk == 38.4:
            if link_bw == 5.4:
                pll_values = {"dco_integer": 0x1A5, "dco_fraction": 0x7000, "pdiv": 0b0010,
                              "kdiv": 0b001, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            elif link_bw == 2.7:
                pll_values = {"dco_integer": 0x1A5, "dco_fraction": 0x7000, "pdiv": 0b0010,
                              "kdiv": 0b010, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            elif link_bw == 1.62:
                pll_values = {"dco_integer": 0x1A5, "dco_fraction": 0x7000, "pdiv": 0b0100,
                              "kdiv": 0b010, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            elif link_bw == 3.24:
                pll_values = {"dco_integer": 0x1A5, "dco_fraction": 0x7000, "pdiv": 0b0100,
                              "kdiv": 0b001, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}

            elif link_bw == 2.16:
                pll_values = {"dco_integer": 0x1C2, "dco_fraction": 0x0000, "pdiv": 0b0001,
                              "kdiv": 0b010, "qdiv_mode": 0b1, "qdiv_ratio": 0x02}
            elif link_bw == 4.32:
                pll_values = {"dco_integer": 0x1C2, "dco_fraction": 0x0000, "pdiv": 0b0001,
                              "kdiv": 0b010, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            elif link_bw == 6.48:
                pll_values = {"dco_integer": 0x1FA, "dco_fraction": 0x2000, "pdiv": 0b0010,
                              "kdiv": 0b001, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            elif link_bw == 8.1:
                pll_values = {"dco_integer": 0x1A5, "dco_fraction": 0x7000, "pdiv": 0b0001,
                              "kdiv": 0b001, "qdiv_mode": 0b0, "qdiv_ratio": 0x00}
            else:
                ret = False
        else:
            ret = False

        return ret, pll_values


if __name__ == "__main__":
    clk = Dg1ClockEdp()
    clk.verify_clock('DP_A', 'gfx_0')
