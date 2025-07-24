##
# @file    tgl_clock_dp_dekelphy.py
# @brief   This tests Dekel phy DP PLLS are programmed correctly for platform TGL.
# @author Kruti, Vadhavaniya; Doriwala, Nainesh P

import logging

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.tgl import tgl_clock_registers
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_port import dpcd_helper

clock_helper = clk_helper.ClockHelper()
tgl_clock_reg = tgl_clock_registers.TglClockRegisters()


##
# @brief TGL port clock verification class for DP DekelPhy display
class TglClockDpDekelPhy():

    lane_count_map = dict([
        (1, [1, 2, 4, 8]),
        (2, [3, 5, 12]),
        (4, 15),
    ])

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        ret = True
        port_name = str(display_port).split('_')[1]
        if port_name in ['D', 'E']:
            reg = 'PORT_TX_DFLEXDPSP1_FIA1'
        elif port_name in ['F', 'G']:
            reg = 'PORT_TX_DFLEXDPSP1_FIA2'
        elif port_name in ['H', 'I']:
            reg = 'PORT_TX_DFLEXDPSP1_FIA3'
        else:
            logging.error("Invalid port configuration")
            return False
        reg_value = clock_helper.clock_register_read('PORT_TX_DFLEXDPSP_REGISTER', reg, gfx_index)
        iom_fw_version = clock_helper.get_value_by_range(reg_value, 12, 12, '', "IomFwVersion")
        lan_count_d_f_h = clock_helper.get_value_by_range(reg_value, 0, 3, self.lane_count_map, "Lane count")
        lan_count_e_g_i = clock_helper.get_value_by_range(reg_value, 8, 11, self.lane_count_map, "Lane count")
        if port_name in ['D', 'F', 'H']:
            assign_lane = lan_count_d_f_h
        elif port_name in ['E', 'G', 'I']:
            assign_lane = lan_count_e_g_i
        else:
            logging.error("Invalid port configuration")
            return False

        if iom_fw_version and assign_lane == 2:
            logging.debug("MFD DP dongle dekel phy validation")
            ret &= self.verify_MFD_dp_dekel_phy(display_port, gfx_index)
        else:
            logging.debug("Native DP dekel phy validation")
            ret &= self.verify_dp_dekel_phy(display_port, gfx_index)

        if ret is True:
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            logging.info("FAIL: PLL Register values not programmed as per BSPEC")
            ret = False

        return ret

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return ret - BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_dp_dekel_phy(self, display_port, gfx_index='gfx_0'):

        port_name = str(display_port).split('_')[1]
        display_tc_port = tgl_clock_reg.trans_ddi_tc_map[port_name.upper()]
        reg_value_DKL_CLKTOP2_HSCLKCTL = clock_helper.read_dkl_register('DKL_CLKTOP2_HSCLKCTL_REGISTER',
                                                                        'DKL_CLKTOP2_HSCLKCTL_NULL_' + port_name,
                                                                        display_tc_port, gfx_index)
        reg_value_DKL_CLKTOP2_CORECLKCTL1 = clock_helper.read_dkl_register('DKL_CLKTOP2_CORECLKCTL1_REGISTER',
                                                                           'DKL_CLKTOP2_CORECLKCTL1_NULL_' + port_name,
                                                                           display_tc_port, gfx_index)

        reg_value_DKL_SSC = clock_helper.read_dkl_register('DKL_SSC_REGISTER', 'DKL_SSC_NULL_' + port_name,
                                                           display_tc_port, gfx_index)

        reg_value_dkl_pll_div0 = clock_helper.read_dkl_register('DKL_PLL_DIV0_REGISTER',
                                                                'DKL_PLL_DIV0_' + port_name,
                                                                display_tc_port, gfx_index)
        reg_value_dkl_pll_div1 = clock_helper.read_dkl_register('DKL_PLL_DIV1_REGISTER',
                                                                'DKL_PLL_DIV1_' + port_name,
                                                                display_tc_port, gfx_index)
        reg_value_dkl_pll_lf = clock_helper.read_dkl_register('DKL_PLL_LF_REGISTER',
                                                              'DKL_PLL_LF_' + port_name,
                                                              display_tc_port, gfx_index)
        reg_value_dkl_pll_frac_lock = clock_helper.read_dkl_register('DKL_PLL_FRAC_LOCK_REGISTER',
                                                                     'DKL_PLL_FRAC_LOCK_' + port_name,
                                                                     display_tc_port, gfx_index)
        reg_value_dkl_cmn_dig_pll_misc = clock_helper.read_dkl_register('DKL_CMN_DIG_PLL_MISC_REGISTER',
                                                                        'DKL_CMN_DIG_PLL_MISC_' + port_name,
                                                                        display_tc_port, gfx_index)
        reg_value_dkl_cmn_ana_dword28 = clock_helper.read_dkl_register('DKL_CMN_ANA_DWORD28_REGISTER',
                                                                       'DKL_CMN_ANA_DWORD28_' + port_name,
                                                                       display_tc_port, gfx_index)

        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        ssc_enable = display_base.GetSSC(display_port, gfx_index)

        ret, phy_values = self.get_dekel_phy_pll_ref_values(link_bw)

        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_SSC.i_sscen_h, 1,
                                                     'DKL_SSC_REGISTER: i_sscen_h') if ssc_enable \
            else clock_helper.verify_port_clock_programming(
            reg_value_DKL_SSC.i_sscen_h, 0, 'DKL_SSC_REGISTER: i_sscen_h')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_CLKTOP2_HSCLKCTL.asUint,
                                                          phy_values["CLKTOP2_HSCLKCTL"], 'CLKTOP2_HSCLKCTL')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_CLKTOP2_CORECLKCTL1.asUint,
                                                          phy_values["CLKTOP2_CORECLKCTL1"], 'CLKTOP2_CORECLKCTL1')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_div0.asUint,
                                                          phy_values["DKL_PLL_DIV0"], 'DKL_PLL_DIV0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_div1.asUint,
                                                          phy_values["DKL_PLL_DIV1"], 'DKL_PLL_DIV1')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_lf.asUint,
                                                          phy_values["DKL_PLL_LF"], 'DKL_PLL_LF')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_frac_lock.asUint,
                                                          phy_values["DKL_PLL_FRAC_LOCK"], 'DKL_PLL_FRAC_LOCK')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_cmn_dig_pll_misc.asUint,
                                                          phy_values["DKL_CMN_DIG_PLL_MISC"], 'DKL_CMN_DIG_PLL_MISC')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_cmn_ana_dword28.asUint,
                                                          phy_values["DKL_CMN_ANA_DWORD28"], 'DKL_CMN_ANA_DWORD28')

        return ret

    ##
    # @brief function to get reference pll and phy values based on bspec.
    # @param[in] link_bw - Link Rate.
    # @return ret :BOOL ( True /False ), pll_values (pll_values dictionary )
    def get_dekel_phy_pll_ref_values(self, link_bw):
        phy_values = []
        ret = True

        logging.debug("Get reference dekel phy pll and phy values for link_rate = " + str(link_bw))

        # Phy values taken from Bspec reference: #https://gfxspecs.intel.com/Predator/Home/Index/31475
        if link_bw == 8.1:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000011d, "CLKTOP2_CORECLKCTL1": 0x10080510,
                          "DKL_PLL_DIV0": 0x70272269, "DKL_PLL_DIV1": 0x0CDCC422,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_CMN_DIG_PLL_MISC": 0x00000000, "DKL_CMN_ANA_DWORD28": 0x14158888}
        elif link_bw == 5.4:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000121d, "CLKTOP2_CORECLKCTL1": 0x10080510,
                          "DKL_PLL_DIV0": 0x70272269, "DKL_PLL_DIV1": 0x0CDCC422,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_CMN_DIG_PLL_MISC": 0x00000000, "DKL_CMN_ANA_DWORD28": 0x14158888}
        elif link_bw == 2.7:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000521d, "CLKTOP2_CORECLKCTL1": 0x10080a12,
                          "DKL_PLL_DIV0": 0x70272269, "DKL_PLL_DIV1": 0x0CDCC422,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_CMN_DIG_PLL_MISC": 0x00000000, "DKL_CMN_ANA_DWORD28": 0x14158888}
        elif link_bw == 1.62:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000621d, "CLKTOP2_CORECLKCTL1": 0x10080a12,
                          "DKL_PLL_DIV0": 0x70272269, "DKL_PLL_DIV1": 0x0CDCC422,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_CMN_DIG_PLL_MISC": 0x00000000, "DKL_CMN_ANA_DWORD28": 0x14158888}
        else:
            ret = False

        return ret, phy_values

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly for MFD DP
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return ret - BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_MFD_dp_dekel_phy(self, display_port, gfx_index='gfx_0'):
        port_name = str(display_port).split('_')[1]
        display_tc_port = tgl_clock_reg.trans_ddi_tc_map[port_name.upper()]
        reg_value_DKL_CLKTOP2_HSCLKCTL = clock_helper.read_dkl_register('DKL_CLKTOP2_HSCLKCTL_REGISTER',
                                                                        'DKL_CLKTOP2_HSCLKCTL_NULL_' + port_name,
                                                                        display_tc_port, gfx_index)
        reg_value_DKL_CLKTOP2_CORECLKCTL1 = clock_helper.read_dkl_register('DKL_CLKTOP2_CORECLKCTL1_REGISTER',
                                                                           'DKL_CLKTOP2_CORECLKCTL1_NULL_' + port_name,
                                                                           display_tc_port, gfx_index)

        reg_value_DKL_SSC = clock_helper.read_dkl_register('DKL_SSC_REGISTER', 'DKL_SSC_NULL_' + port_name,
                                                           display_tc_port, gfx_index)

        reg_value_dkl_pll_div0 = clock_helper.read_dkl_register('DKL_PLL_DIV0_REGISTER',
                                                                'DKL_PLL_DIV0_' + port_name,
                                                                display_tc_port, gfx_index)
        reg_value_dkl_pll_div1 = clock_helper.read_dkl_register('DKL_PLL_DIV1_REGISTER',
                                                                'DKL_PLL_DIV1_' + port_name,
                                                                display_tc_port, gfx_index)
        reg_value_dkl_pll_lf = clock_helper.read_dkl_register('DKL_PLL_LF_REGISTER',
                                                              'DKL_PLL_LF_' + port_name,
                                                              display_tc_port, gfx_index)
        reg_value_dkl_pll_frac_lock = clock_helper.read_dkl_register('DKL_PLL_FRAC_LOCK_REGISTER',
                                                                     'DKL_PLL_FRAC_LOCK_' + port_name,
                                                                     display_tc_port, gfx_index)
        reg_value_dkl_cmn_dig_pll_misc = clock_helper.read_dkl_register('DKL_CMN_DIG_PLL_MISC_REGISTER',
                                                                        'DKL_CMN_DIG_PLL_MISC_' + port_name,
                                                                        display_tc_port, gfx_index)
        reg_value_dkl_bias = clock_helper.read_dkl_register('DKL_BIAS_REGISTER',
                                                            'DKL_BIAS_' + port_name,
                                                            display_tc_port, gfx_index)
        reg_value_dkl_tdc_coldst_bias = clock_helper.read_dkl_register('DKL_TDC_COLDST_BIAS_REGISTER',
                                                                       'DKL_TDC_COLDST_BIAS_' + port_name,
                                                                       display_tc_port, gfx_index)
        reg_value_dkl_xxx_tdc_cro = clock_helper.read_dkl_register('DKL_XXX_TDC_CRO_REGISTER',
                                                                       'DKL_XXX_TDC_CRO_NULL_' + port_name,
                                                                       display_tc_port, gfx_index)
        reg_value_dkl_pll1_cntr_xxxx_settings = clock_helper.read_dkl_register('DKL_PLL1_CNTR_XXXX_SETTINGS_REGISTER',
                                                                       'DKL_PLL1_CNTR_XXXX_SETTINGS_' + port_name,
                                                                       display_tc_port, gfx_index)

        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        ssc_enable = display_base.GetSSC(display_port, gfx_index)

        ret, phy_values = self.get_MFD_DP_dekel_phy_pll_ref_values(link_bw)

        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_SSC.i_sscen_h, 1,
                                                     'DKL_SSC_REGISTER: i_sscen_h') if ssc_enable \
            else clock_helper.verify_port_clock_programming(
            reg_value_DKL_SSC.i_sscen_h, 0, 'DKL_SSC_REGISTER: i_sscen_h')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_CLKTOP2_HSCLKCTL.asUint,
                                                          phy_values["CLKTOP2_HSCLKCTL"], 'CLKTOP2_HSCLKCTL')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_CLKTOP2_CORECLKCTL1.asUint,
                                                          phy_values["CLKTOP2_CORECLKCTL1"], 'CLKTOP2_CORECLKCTL1')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_div0.asUint,
                                                          phy_values["DKL_PLL_DIV0"], 'DKL_PLL_DIV0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_div1.asUint,
                                                          phy_values["DKL_PLL_DIV1"], 'DKL_PLL_DIV1')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_lf.asUint,
                                                          phy_values["DKL_PLL_LF"], 'DKL_PLL_LF')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll_frac_lock.asUint,
                                                          phy_values["DKL_PLL_FRAC_LOCK"], 'DKL_PLL_FRAC_LOCK')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_cmn_dig_pll_misc.asUint,
                                                          phy_values["DKL_CMN_DIG_PLL_MISC"], 'DKL_CMN_DIG_PLL_MISC')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_bias.asUint,
                                                          phy_values["DKL_BIAS"], 'DKL_BIAS')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_tdc_coldst_bias.asUint,
                                                          phy_values["DKL_TDC_COLDST_BIAS"], 'DKL_TDC_COLDST_BIAS')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_xxx_tdc_cro.asUint,
                                                          phy_values["DKL_XXX_TDC_CRO"], 'DKL_XXX_TDC_CRO')
        ret &= clock_helper.verify_port_clock_programming(reg_value_dkl_pll1_cntr_xxxx_settings.asUint,
                                                          phy_values["DKL_PLL1_CNTR_XXXX_SETTINGS"],
                                                     'DKL_PLL1_CNTR_XXXX_SETTINGS')
        return ret

    ##
    # @brief function to get reference pll and phy values based on bspec.
    # @param[in] link_bw - String : Link Rate.
    # @return ret :BOOL ( True /False ) ,
    # pll_values (pll_values dictionary )
    def get_MFD_DP_dekel_phy_pll_ref_values(self, link_bw):
        phy_values = []
        ret = True

        logging.debug("Get reference MFD DP dekel phy pll and phy values for link_rate = " + str(link_bw))

        # Phy values taken from Bspec reference: #https://gfxspecs.intel.com/Predator/Home/Index/49204
        if link_bw == 8.1:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000011d, "CLKTOP2_CORECLKCTL1": 0x10080510,
                          "DKL_PLL_DIV0": 0x50272228, "DKL_PLL_DIV1": 0x0CD8C40D,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_BIAS": 0xE0000000, "DKL_TDC_COLDST_BIAS": 0x00000023,
                          "DKL_XXX_TDC_CRO": 0x80008150, "DKL_PLL1_CNTR_XXXX_SETTINGS": 0x0004003F,
                          "DKL_CMN_DIG_PLL_MISC": 0x00020000}
        elif link_bw == 5.4:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000121d, "CLKTOP2_CORECLKCTL1": 0x10080510,
                          "DKL_PLL_DIV0": 0x50272228, "DKL_PLL_DIV1": 0x0CD8C40D,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_BIAS": 0xE0000000, "DKL_TDC_COLDST_BIAS": 0x00000023,
                          "DKL_XXX_TDC_CRO": 0x80008150, "DKL_PLL1_CNTR_XXXX_SETTINGS": 0x0004003F,
                          "DKL_CMN_DIG_PLL_MISC": 0x00020000}
        elif link_bw == 2.7:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000521d, "CLKTOP2_CORECLKCTL1": 0x10080a12,
                          "DKL_PLL_DIV0": 0x50272228, "DKL_PLL_DIV1": 0x0CD8C40D,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_BIAS": 0xE0000000, "DKL_TDC_COLDST_BIAS": 0x00000023,
                          "DKL_XXX_TDC_CRO": 0x80008150, "DKL_PLL1_CNTR_XXXX_SETTINGS": 0x0004003F,
                          "DKL_CMN_DIG_PLL_MISC": 0x00020000}
        elif link_bw == 1.62:
            phy_values = {"CLKTOP2_HSCLKCTL": 0x0000621d, "CLKTOP2_CORECLKCTL1": 0x10080a12,
                          "DKL_PLL_DIV0": 0x50272228, "DKL_PLL_DIV1": 0x0CD8C40D,
                          "DKL_PLL_LF": 0x00401300, "DKL_PLL_FRAC_LOCK": 0x8044B56A,
                          "DKL_BIAS": 0xE0000000, "DKL_TDC_COLDST_BIAS": 0x00000023,
                          "DKL_XXX_TDC_CRO": 0x80008150, "DKL_PLL1_CNTR_XXXX_SETTINGS": 0x0004003F,
                          "DKL_CMN_DIG_PLL_MISC": 0x00020000}
        else:
            ret = False

        return ret, phy_values


if __name__ == "__main__":
    clk = TglClockDpDekelPhy()
