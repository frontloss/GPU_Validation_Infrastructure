##
# @file      adlp_clock_dp_dekelphy.py
# @brief     This tests Dekel phy DP PLLS are programmed correctly for platform ADLP.
# @author    Sri Sumanth Geesala


import logging

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.adlp import adlp_clock_registers
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_port import dpcd_helper
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info


##
# @brief ADLP port clock verification class for DP DekelPhy display
class AdlpClockDpDekelPhy():
    clock_helper = clk_helper.ClockHelper()

    lane_assignment_mask = {
        'PHY_TX0_ALONE': 0x1,
        'PHY_TX1_ALONE': 0x2,
        'PHY_TX2_ALONE': 0x4,
        'PHY_TX3_ALONE': 0x8
    }

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - graphics index of adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        ret = True

        ret &= self.verify_dp_dekel_phy(display_port, gfx_index)

        if (ret is True):
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]ADLP_Clock_DP_Dekelphy: PLL Register values not programmed as "
                      "per BSPEC",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL: PLL Register values not programmed as per BSPEC")
            ret = False

        return ret

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index of adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_dp_dekel_phy(self, display_port, gfx_index='gfx_0'):

        ret = True
        # getting RPLP/TWL data from sku_name since platform name is common for ADLP,RPLP and TWL in test framework
        disp_hw_info = machine_info.SystemInfo().get_gfx_display_hardwareinfo()
        if len(disp_hw_info) <= int(gfx_index[-1]):
            logging.error(f'{gfx_index} not available in enumerated adapters')
            return False
        sku_name = disp_hw_info[int(gfx_index[-1])].SkuName

        is_plat_RPLP = True if sku_name.upper() == 'RPLP' else False
        is_plat_ADLN = True if sku_name.upper() == 'ADLN' else False
        is_plat_TWL = True if sku_name.upper() == 'TWINLAKE' else False
        port_name = str(display_port).split('_')[1]
        adlp_clock_reg = adlp_clock_registers.AdlpClockRegisters()
        display_tc_port = adlp_clock_reg.trans_ddi_tc_map[port_name.upper()]
        adapter_info = self.clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)

        # Display uses PLL1 by default, PLL0 is used for DP v2.0 link rates.
        pll_selected = adlp_clock_reg.DKL_PLL1
        if link_bw in [10.0, 20.0]:     # UHBR10 and UHBR20. UHBR13.5 is not supported by ADLP.
            pll_selected = adlp_clock_reg.DKL_PLL0

        if is_plat_RPLP or is_plat_ADLN or is_plat_TWL:
            ret1, phy_values = self.rplp_get_dekel_phy_pll_ref_values(link_bw)
        else:
            ret1, phy_values = self.adlp_get_dekel_phy_pll_ref_values(link_bw)

        if ret1 is False:
            logging.error(f'Failed to get Dekel PHY PLL expected values for {link_bw}')
            return False

        ssc_enable = display_base.GetSSC(display_port, gfx_index)

        if port_name in ['F', 'G']:
            reg = 'PORT_TX_DFLEXDPSP1_FIA1'
        elif port_name in ['H', 'I']:
            reg = 'PORT_TX_DFLEXDPSP1_FIA2'
        else:
            logging.error("Invalid port configuration")
            return False
        reg_value = self.clock_helper.clock_register_read('PORT_TX_DFLEXDPSP_REGISTER', reg, gfx_index)
        if port_name in ['F', 'H']:
            assign_lane = self.clock_helper.get_value_by_range(reg_value, 0, 3, '', 'Lane assignment')
        elif port_name in ['G', 'I']:
            assign_lane = self.clock_helper.get_value_by_range(reg_value, 8, 11, '', 'Lane assignment')
        else:
            logging.error("Invalid port configuration")
            return False

        dkl_data_lanes = []
        if (assign_lane & self.lane_assignment_mask['PHY_TX0_ALONE']) or \
                (assign_lane & self.lane_assignment_mask['PHY_TX1_ALONE']):
            dkl_data_lanes.append(0)
        if (assign_lane & self.lane_assignment_mask['PHY_TX2_ALONE']) or \
                (assign_lane & self.lane_assignment_mask['PHY_TX3_ALONE']):
            dkl_data_lanes.append(1)
        if len(dkl_data_lanes) == 0:
            gdhm.report_bug(
                title='[Interfaces][Display_Engine]ADLP_Clock_DP_Dekelphy: None of the DKL PHY lanes are assigned '
                      'to display. Invalid lane configuration',
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('None of the DKL PHY lanes are assigned to display. Invalid lane configuration')

            return False

        # Phy values taken from Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/55316
        # verify registers specific to DP v2.0
        if pll_selected == adlp_clock_reg.DKL_PLL0:
            # DKLP_CMN_ANA_CMN_ANA_DWORD0
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD0 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD0_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD0_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD0.asUint,
                                                                   phy_values["HSCLK"],
                                                         'DKLP_CMN_ANA_CMN_ANA_DWORD0_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD1
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD1 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD1_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD1_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD1.asUint,
                                                                   phy_values["CORECLK"],
                                                         'DKLP_CMN_ANA_CMN_ANA_DWORD1_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD2
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD2 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD2_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD2_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD2.asUint,
                                                                   phy_values["DWORD2"],
                                                         'DKLP_CMN_ANA_CMN_ANA_DWORD2_' + display_tc_port)

            # DKLP_PLL0_SSC
            if ssc_enable == 0:
                reg_value_DKLP_PLL_SSC = self.clock_helper.read_dkl_register(
                    'DKLP_PLL_SSC_REGISTER', 'DKLP_PLL0_SSC_' + display_tc_port, display_tc_port, gfx_index)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_PLL_SSC.i_sscen_h, 0,
                                                             'DKLP_PLL0_SSC_' + display_tc_port + ' : i_sscen_h')

            if is_plat_RPLP or is_plat_ADLN or is_plat_TWL:
                # DKLP_CMN_ANA_CMN_ANA_DWORD3
                reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD3 = self.clock_helper.read_dkl_register(
                    'DKLP_CMN_ANA_CMN_ANA_DWORD3_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD3_' + display_tc_port,
                    display_tc_port, gfx_index)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD3.asUint,
                                                                       phy_values["DWORD3"],
                                                                  'DKLP_CMN_ANA_CMN_ANA_DWORD3_' + display_tc_port)

                # DKLP_CMN_ANA_CMN_ANA_DWORD4
                reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD4 = self.clock_helper.read_dkl_register(
                    'DKLP_CMN_ANA_CMN_ANA_DWORD4_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD4_' + display_tc_port,
                    display_tc_port, gfx_index)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD4.asUint,
                                                                       phy_values["DWORD4"],
                                                                  'DKLP_CMN_ANA_CMN_ANA_DWORD4_' + display_tc_port)

        # verify registers specific to link rates lower than DP v2.0
        elif is_plat_RPLP or is_plat_ADLN or is_plat_TWL:
            # DKLP_CMN_ANA_CMN_ANA_DWORD5
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD5_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.asUint,
                                                                   phy_values["HSCLK"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD6
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD6_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6.asUint,
                                                                   phy_values["CORECLK"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD7
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD7 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD7_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD7_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD7.asUint,
                                                                   phy_values["DklCoreClkPll2"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD7_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD8
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD8 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD8_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD8_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD8.asUint,
                                                                   phy_values["DklCoreClkPll3"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD8_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD9
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD9 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD9_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD9_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD9.asUint,
                                                                   phy_values["DklRefDfxPclkCtl"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD9_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD28
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD28 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD28_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD28_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD28.asUint,
                                                                   phy_values["DklCmnAnaDword28"],
                                                              'DKLP_CMN_ANA_CMN_ANA_DWORD28_' + display_tc_port)
        else:
            # DKLP_CMN_ANA_CMN_ANA_DWORD5
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD5_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.asUint,
                                                                   phy_values["HSCLK"],
                                                         'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port)

            # DKLP_CMN_ANA_CMN_ANA_DWORD6
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6 = self.clock_helper.read_dkl_register(
                'DKLP_CMN_ANA_CMN_ANA_DWORD6_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port,
                display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6.asUint,
                                                                   phy_values["CORECLK"],
                                                         'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port)

            # DKLP_PLL1_SSC
            reg_value_DKLP_PLL_SSC = self.clock_helper.read_dkl_register(
                'DKLP_PLL_SSC_REGISTER', 'DKLP_PLL1_SSC_' + display_tc_port, display_tc_port, gfx_index)
            ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_PLL_SSC.i_sscen_h,
                                                                   1 if ssc_enable else 0,
                                                         'DKLP_PLL1_SSC_' + display_tc_port + ' : i_sscen_h')

        # verify registers common to all link rates
        # DKLP_CMN_ANA_CMN_ANA_DWORD1[6:6] : post divider muxes. bit[6]==1 for DP v2.0 link rates, bit[6]==0 otherwise.
        reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD1 = self.clock_helper.read_dkl_register(
            'DKLP_CMN_ANA_CMN_ANA_DWORD1_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD1_' + display_tc_port,
            display_tc_port, gfx_index)
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD1.cfg_on_pll12coreclka_select,
            1 if pll_selected == adlp_clock_reg.DKL_PLL0 else 0,
            'DKLP_CMN_ANA_CMN_ANA_DWORD1_' + display_tc_port +'(bit 6) : post_divider_muxes')

        # disabling DP 1.4 RPL-P specific checks as of now, due to driver revert. TODO: Need to enable along with driver
        if (is_plat_RPLP or is_plat_ADLN or is_plat_TWL) and False:
            for data_lane in dkl_data_lanes:
                # DKLP_PCS_GLUE_RTT_CR_SPARE
                reg_value_DKLP_PCS_GLUE_RTT_CR_SPARE = self.clock_helper.read_dkl_register(
                    'DKLP_PCS_GLUE_RTT_CR_SPARE_REGISTER', 'DKLP_PCS_GLUE_RTT_CR_SPARE_' + display_tc_port,
                    display_tc_port, gfx_index, mmio_index=data_lane)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_PCS_GLUE_RTT_CR_SPARE.asUint,
                                                                       phy_values["PcsGlueSpare"],
                                                                  'DKLP_PCS_GLUE_RTT_CR_SPARE_' + display_tc_port)

                # DKLP_PCS_GLUE_TX1_FW_CALIB
                reg_value_DKLP_PCS_GLUE_TX1_FW_CALIB = self.clock_helper.read_dkl_register(
                    'DKLP_PCS_GLUE_TX1_FW_CALIB_REGISTER', 'DKLP_PCS_GLUE_TX1_FW_CALIB_' + display_tc_port,
                    display_tc_port, gfx_index, mmio_index=data_lane)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_PCS_GLUE_TX1_FW_CALIB.asUint,
                                                                       phy_values["PcsGlueCalib"],
                                                                  'DKLP_PCS_GLUE_TX1_FW_CALIB_' + display_tc_port)

                # DKLP_TX2_PMD_LANE_MISC_TX1_SPARE
                reg_value_DKLP_TX2_PMD_LANE_MISC_TX1_SPARE = self.clock_helper.read_dkl_register(
                    'DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_REGISTER', 'DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_' + display_tc_port,
                    display_tc_port, gfx_index, mmio_index=data_lane)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_TX2_PMD_LANE_MISC_TX1_SPARE.asUint,
                                                                       phy_values["PmdMiscSpare"],
                                                                  'DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_' + display_tc_port)

                # DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL
                reg_value_DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL = self.clock_helper.read_dkl_register(
                    'DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_REGISTER',
                    'DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_' + display_tc_port, display_tc_port, gfx_index,
                    mmio_index=data_lane)
                ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL.asUint,
                                                                       phy_values["PmdMiscCntl"],
                                                                  'DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_' +
                                                                       display_tc_port)

                # DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL
                reg_value_DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL = self.clock_helper.read_dkl_register(
                    'DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_REGISTER',
                    'DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_' + display_tc_port,
                    display_tc_port, gfx_index, mmio_index=data_lane)
                ret &= self.clock_helper.verify_port_clock_programming(
                    reg_value_DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL.asUint,
                    phy_values["PmdSuswell"], 'DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_' + display_tc_port)


        return ret

    ##
    # @brief function to get reference pll and phy values based on bspec, for ADL-P.
    # TODO: When we extend the new DKL PHY checks to ADLP, we have to merge adlp_get_dekel_phy_pll_ref_values and
    #  rplp_get_dekel_phy_pll_ref_values methods.
    # @param[in] link_bw - Link Rate.
    # @return ret - BOOL ( True /False ) , phy_values - pll values dictionary
    def adlp_get_dekel_phy_pll_ref_values(self, link_bw):
        phy_values = {}
        ret = True
        logging.debug("Getting reference dekel phy pll and phy values for link_rate = " + str(link_bw))

        # Phy values taken from Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/55316
        if link_bw == 20.0:
            phy_values = {"HSCLK": 0x00000A65, "CORECLK": 0x120814d2, "DWORD2": 0x19000404}
        elif link_bw == 10.0:
            phy_values = {"HSCLK": 0x00000165, "CORECLK": 0x120814d2, "DWORD2": 0x19000408}
        elif link_bw == 8.1:
            phy_values = {"HSCLK": 0x00000011d, "CORECLK": 0x12080512}
        elif link_bw == 5.4:
            phy_values = {"HSCLK": 0x0000111d, "CORECLK": 0x12080512}
        elif link_bw == 2.7:
            phy_values = {"HSCLK": 0x0000521d, "CORECLK": 0x12080a12}
        elif link_bw == 1.62:
            phy_values = {"HSCLK": 0x0000621d, "CORECLK": 0x12080a12}
        else:
            ret = False

        return ret, phy_values

    ##
    # @brief function to get reference pll and phy values based on bspec, for RPL-P.
    # TODO: When we extend the new DKL PHY checks to ADLP, we have to merge adlp_get_dekel_phy_pll_ref_values and
    #  rplp_get_dekel_phy_pll_ref_values methods.
    # @param[in] link_bw - Link Rate.
    # @return ret - BOOL ( True /False ) , phy_values - pll values dictionary
    def rplp_get_dekel_phy_pll_ref_values(self, link_bw):
        phy_values = {}
        ret = True
        logging.debug("Getting reference dekel phy pll and phy values for link_rate = " + str(link_bw))

        # Phy values taken from Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/55316
        if link_bw == 20.0:
            phy_values = {"HSCLK": 0x00008A65, "CORECLK": 0x000814C0, "DWORD2": 0x19000404,
                          "PcsGlueSpare": 0x01041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DWORD3": 0x05190019,
                          "DWORD4": 0x000C3200}
        elif link_bw == 10.0:
            phy_values = {"HSCLK": 0x00008165, "CORECLK": 0x000814C0, "DWORD2": 0x19000408,
                          "PcsGlueSpare": 0x01041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DWORD3": 0x05190019,
                          "DWORD4": 0x000C3200}
        elif link_bw == 8.1:
            phy_values = {"HSCLK": 0x00000811d, "CORECLK": 0x00080500,
                          "PcsGlueSpare": 0x08041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DklCoreClkPll2": 0x28003205,
                          "DklCoreClkPll3": 0x05280032, "DklRefDfxPclkCtl": 0x000C3200, "DklCmnAnaDword28": 0x041588A8}
        elif link_bw == 5.4:
            phy_values = {"HSCLK": 0x0000111d, "CORECLK": 0x00080500,
                          "PcsGlueSpare": 0x08041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DklCoreClkPll2": 0x28003205,
                          "DklCoreClkPll3": 0x051B0032, "DklRefDfxPclkCtl": 0x000C3200, "DklCmnAnaDword28": 0x04158888}
        elif link_bw == 2.7:
            phy_values = {"HSCLK": 0x0000521d, "CORECLK": 0x00080A00,
                          "PcsGlueSpare": 0x08041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DklCoreClkPll2": 0x2800320A,
                          "DklCoreClkPll3": 0x051B0032, "DklRefDfxPclkCtl": 0x000C3200, "DklCmnAnaDword28": 0x04158888}
        elif link_bw == 1.62:
            phy_values = {"HSCLK": 0x0000621d, "CORECLK": 0x00080A00,
                          "PcsGlueSpare": 0x08041000, "PcsGlueCalib": 0x00000080, "PmdMiscSpare": 0x0000000F,
                          "PmdMiscCntl": 0x0000A000, "PmdSuswell": 0x1FF00050, "DklCoreClkPll2": 0x1000320A,
                          "DklCoreClkPll3": 0x05100032, "DklRefDfxPclkCtl": 0x000C3200, "DklCmnAnaDword28": 0x04158888}
        else:
            ret = False

        return ret, phy_values



if __name__ == "__main__":
    clk = AdlpClockDpDekelPhy()
