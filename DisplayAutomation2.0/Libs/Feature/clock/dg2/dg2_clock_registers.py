##
# @file   dg2_clock_registers.py
# @brief  Python helper class for doing DG2 generic functions
# @author Kruti, vadhavaniya

from Libs.Feature.clock import clock_helper as clk_helper


##
# @details Clock register class
class ClockRegister:
    MPLLB_CP = ''
    MPLLB_DIV = ''
    MPLLB_DIV2 = ''
    MPLLB_FRACN1 = ''
    MPLLB_FRACN2 = ''
    MPLLB_SSCEN = ''
    MPLLB_SSCSTEP = ''
    REF_CONTROL = ''


##
# @brief DG2 clock Registers class
class Dg2ClockRegisters:
    # Trans DDI Func mapping register offset
    TRANS_DDI_FUNC_CTL = dict([
        ('TRANS_DDI_FUNC_CTL_A', 0x60400),
        ('TRANS_DDI_FUNC_CTL_B', 0x61400),
        ('TRANS_DDI_FUNC_CTL_C', 0x62400),
        ('TRANS_DDI_FUNC_CTL_D', 0x63400)
    ])

    # DDI port mapping dictionary
    trans_ddi_port_map = dict([
        ('A', 1),
        ('B', 2),
        ('C', 3),
        ('F', 4),
        ('D', 8),
        ('E', 9)
    ])

    ##
    # @brief Get the list of active Pipes
    # @param[in] gfx_index - Graphics index on which active pipe get called
    # @return mapping of active pipes
    def get_pipe(self, gfx_index='gfx_0'):
        clock_helper = clk_helper.ClockHelper()
        trans_map_int = dict(
            map(lambda kv: (
                kv[0], clock_helper.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', str(kv[0]), gfx_index))
                , self.TRANS_DDI_FUNC_CTL.items()))
        trans_map = {k: v for k, v in trans_map_int.items() if v & 2147483648 != 0}
        return dict(map(lambda kv:
                        (
                            kv[0], clock_helper.get_value_by_range(kv[1], 27, 30, self.trans_ddi_port_map, str(kv[0])))
                        , trans_map.items()))

    ##
    # @brief function to get the pipe for the display_port
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return pipe_value in string
    def get_pipe_for_port(self, display_port, gfx_index):
        trans_map = self.get_pipe(gfx_index)
        port = str(display_port).split('_')[1]
        return str(list(trans_map)[list(trans_map.values()).index(port)]).rsplit('_', 1)[1]

    ##
    # @brief function to verify whether the PLL is Enabled and locked
    # @param[in] display_port - Display port
    # @param[in] pll - Pll register string
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_pll_enable(self, display_port, pll, gfx_index='gfx_0'):
        clock_helper = clk_helper.ClockHelper()
        pll = pll.replace('_', '')
        reg_value = clock_helper.clock_register_read(str('DPLL_ENABLE_REGISTER'), str(pll + '_PLL_ENABLE'), gfx_index)
        pll_enable = clock_helper.get_value_by_range(reg_value, 31, 31, '', pll + '_PLL_ENABLE')
        pll_lock = clock_helper.get_value_by_range(reg_value, 30, 30, '', pll + '_PLL_LOCK')
        pll_enable_str = 'ENABLED' if pll_enable == 1 else 'DISABLED'
        pll_lock_str = 'LOCKED' if pll_lock == 1 else 'UNLOCKED'

        ret = clock_helper.verify_port_clock_programming_ex(feature='{}_ENABLE'.format(pll),
                                                            parameter=["ENABLE", "LOCK"],
                                                            expected=["ENABLED", "LOCKED"],
                                                            actual=[pll_enable_str, pll_lock_str])
        return ret
