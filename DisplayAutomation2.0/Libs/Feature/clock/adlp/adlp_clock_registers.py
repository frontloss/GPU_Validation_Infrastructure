##
# @file   adlp_clock_registers.py
# @brief  Python helper class for doing ADLP generic functions
# @author Kruti, vadhavaniya

from Libs.Feature.clock import clock_helper as clk_helper


##
# @brief ADLP clock Registers class
class AdlpClockRegisters:
    DKL_PLL0 = 'PLL0'
    DKL_PLL1 = 'PLL1'
    # TypeC to port mapping dictionary
    trans_ddi_tc_map = dict([
        ('F', 'TC1'),
        ('G', 'TC2'),
        ('H', 'TC3'),
        ('I', 'TC4')
    ])

    ##
    # @brief function to verify whether the PLL is Enabled and locked
    # @param[in] display_port - Display port
    # @param[in] pll - pll register string
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_pll_enable(self, display_port, pll, gfx_index='gfx_0'):
        clock_helper = clk_helper.ClockHelper()
        reg_value = clock_helper.clock_register_read(str('DPLL_ENABLE_REGISTER'), str(pll + '_ENABLE'), gfx_index)
        pll_enable = clock_helper.get_value_by_range(reg_value, 31, 31, '', pll + '_ENABLE')
        pll_lock = clock_helper.get_value_by_range(reg_value, 30, 30, '', pll + '_LOCK')
        pll_enable_str = 'ENABLED' if pll_enable == 1 else 'DISABLED'
        pll_lock_str = 'LOCKED' if pll_lock == 1 else 'UNLOCKED'

        ret = clock_helper.verify_port_clock_programming_ex(feature='{}_ENABLE'.format(pll),
                                                            parameter=["{} ENABLE".format(display_port),
                                                                  "{} LOCK".format(display_port)],
                                                            expected=["ENABLED", "LOCKED"],
                                                            actual=[pll_enable_str, pll_lock_str])
        return ret
