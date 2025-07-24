########################################################################################################################
# @file         mipi_dphy_config.py
# @brief        This file contains helper functions for verifying if DPHY and DSI registers are programmed in accordance
#               with VBT
# @author       Geesala, Sri Sumanth
########################################################################################################################
import importlib
import logging
import math

from Libs.Feature.mipi import mipi_helper as _mipi_helper
from registers.mmioregister import MMIORegister


##
# @brief        Verifies if DPHY and DSI registers are programmed with the DPHY values in accordance with VBT
# @param[in]    mipi_helper object of MipiHelper class
# @param[in]    port - port name
# @return       None
def verify_dphy_config(mipi_helper, port):
    panel_index = mipi_helper.get_panel_index_for_port(port)
    vbt_mipi_data = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index]

    ##
    # Verify Combo PHY Mode: DSI_IO_MODECTL[0] (should be configured to 'MIPI DSI Mode')
    dsi_io_modectl = importlib.import_module("registers.%s.DSI_IO_MODECTL_REGISTER" % (mipi_helper.platform))
    reg_dsi_io_modectl = MMIORegister.read("DSI_IO_MODECTL_REGISTER", "DSI_IO_MODECTL" + port, mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='DSI_IO_MODECTL' + port, field='Combo PHY Mode',
                                  expected=getattr(dsi_io_modectl, "combo_phy_mode_MIPI_DSI_MODE"),
                                  actual=reg_dsi_io_modectl.combo_phy_mode, message='expected to be MIPI_DSI_MODE')

    _verify_dphy_phy_params(mipi_helper, port, vbt_mipi_data)
    _verify_dsi_phy_params(mipi_helper, port, vbt_mipi_data)


##
# @brief        wrapper method to call appropriate PHY verification method based on platform
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port  - port name
# @param[in]    vbt_mipi_data - MipiDataStructureEntry of current panel from  Block 52 of vbt.
# @return       None
def _verify_dphy_phy_params(mipi_helper, port, vbt_mipi_data):
    if mipi_helper.platform in ['icl', 'jsl', 'tgl', 'ryf', 'adlp']:
        _verify_dphy_phy_params_icl(mipi_helper, port, vbt_mipi_data)
    elif mipi_helper.platform in ['lkf1']:
        _verify_dphy_phy_params_lkf(mipi_helper, port, vbt_mipi_data)
    else:
        logging.error("DPHY phy verification not configured for %s" % (mipi_helper.platform))
        mipi_helper.verify_fail_count += 1


##
# @brief        Verifies DPHY parameters in PHY registers. Specific to ICL and ICL based platforms.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port - port name
# @param[in]    vbt_mipi_data - MipiDataStructureEntry of current panel from  Block 52 of vbt.
# @return       None
def _verify_dphy_phy_params_icl(mipi_helper, port, vbt_mipi_data):
    if port == "_DSI0":
        ddi = '_A'
    else:
        ddi = '_B'
    data_lane_list = ['_LN0', '_LN1', '_LN3', '_AUX']  # we don't touch '_LN2'. It is clock lane.

    # from VBT fetch - Exit, Trail, Zero, Prepare for Clock(Clk) and Data(HS)
    # VBT values are in ns. Convert them to escape clocks (50ns = 1 escape clock)
    # only for THSPrepare and TClkPrepare, after converting to escape clocks, encode it with granularity of
    # 0.25 escape clocks. 0b001 = 0.25 Escape clocks
    VBT_THSTrail = int(math.ceil(vbt_mipi_data.THSTrail / 50.0))
    VBT_THSZero = vbt_mipi_data.THSPrepareHSZero - vbt_mipi_data.THSPrepare
    VBT_THSZero = int(math.ceil(VBT_THSZero / 50.0))
    VBT_THSPrepare = int(math.ceil((vbt_mipi_data.THSPrepare / 50.0) * 4))

    VBT_TClkTrail = int(math.ceil(vbt_mipi_data.TClkTrail / 50.0))
    VBT_TClkZero = vbt_mipi_data.TClkPrepareClkZero - vbt_mipi_data.TClkPrepare
    VBT_TClkZero = int(math.ceil(VBT_TClkZero / 50.0))
    VBT_TClkPrepare = int(math.ceil((vbt_mipi_data.TClkPrepare / 50.0) * 4))

    ##
    # 1. Verify Static Power Down DDI: PORT_CL_DW10[7:4] (should be set to 'Power up all lanes'). DDIA for DSI0,
    # DDIB for DSI1
    port_cl_dw10 = importlib.import_module("registers.%s.PORT_CL_DW10_REGISTER" % (mipi_helper.platform))
    reg_port_cl_dw10 = MMIORegister.read("PORT_CL_DW10_REGISTER", "PORT_CL_DW10" + ddi, mipi_helper.platform)
    panel_index = mipi_helper.get_panel_index_for_port(port)
    lane_count = mipi_helper.get_lane_count(panel_index)
    if lane_count == 4:
        expected_static_power_down_ddi = "static_power_down_ddi_POWER_UP_ALL_LANES"
    elif lane_count == 3:
        expected_static_power_down_ddi = "static_power_down_ddi_POWER_DOWN_LANE_3"
    elif lane_count == 2:
        expected_static_power_down_ddi = "static_power_down_ddi_POWER_DOWN_LANES_3_1"
    else:
        expected_static_power_down_ddi = "static_power_down_ddi_POWER_DOWN_LANES_3_1_0"
    mipi_helper.verify_and_log_helper(register='PORT_CL_DW10' + ddi, field='Static Power Down DDI',
                                  expected=getattr(port_cl_dw10, expected_static_power_down_ddi),
                                  actual=reg_port_cl_dw10.static_power_down_ddi,
                                  message='value expected is POWER_UP_ALL_LANES')

    ##
    # 2. Verify Loadgen Select: PORT_TX_DW4[31] for all lanes. DDIA for DSI0, DDIB for DSI1
    for lane_name in data_lane_list:
        reg_port_tx_dw4 = MMIORegister.read("PORT_TX_DW4_REGISTER", "PORT_TX_DW4" + lane_name + ddi,
                                            mipi_helper.platform)
        if (lane_name == '_AUX'):
            expected_loadgen_select = 0
        else:
            expected_loadgen_select = 1
        mipi_helper.verify_and_log_helper(register='PORT_TX_DW4' + lane_name + ddi, field='Loadgen Select',
                                      expected=expected_loadgen_select,
                                      actual=reg_port_tx_dw4.loadgen_select)

    ##
    # 3. Verify Latency Optimization: PORT_TX_DW2[10:8] for all lanes. DDIA for DSI0, DDIB for DSI1
    for lane_name in data_lane_list:
        reg_port_tx_dw2 = MMIORegister.read("PORT_TX_DW2_REGISTER", "PORT_TX_DW2" + lane_name + ddi,
                                            mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='PORT_TX_DW2' + lane_name + ddi, field='Latency Optimization',
                                      expected=5,
                                      actual=reg_port_tx_dw2.frclatencyoptim)

    ##
    # DPHY registers
    logging.info('--------Verifying PHY params in DPHY registers--------')
    ##
    # 1. Compare Trail: DPHY_CLK_TIMING_PARAM[2:0] (CLK_TRAIL) and DPHY_DATA_TIMING_PARAM[10:8] (HS_TRAIL)
    reg_dphy_clk_timing = MMIORegister.read("DPHY_CLK_TIMING_PARAM_REGISTER", "DPHY_CLK_TIMING_PARAM" + port,
                                            mipi_helper.platform)
    reg_dphy_data_timing = MMIORegister.read("DPHY_DATA_TIMING_PARAM_REGISTER", "DPHY_DATA_TIMING_PARAM" + port,
                                             mipi_helper.platform)

    # Don't verify these. Driver is leaving TClkTrail & THSTrail at hardware default, since programming
    # high values of THsTrail is leading to TEoT crossing DPHY spec mandated maximum values (which violates DPHY compliance).
    # verify_and_log_helper(register= 'DPHY_CLK_TIMING_PARAM' + port, field= 'CLK_TRAIL', expected= VBT_TClkTrail,
    #                           actual= dphy_clk_timing.clk_trail)
    # verify_and_log_helper(register= 'DPHY_DATA_TIMING_PARAM' + port, field= 'HS_TRAIL', expected= VBT_THSTrail,
    #                           actual= dphy_data_timing.hs_trail)

    ##
    # 2. Compare Zero: DPHY_CLK_TIMING_PARAM[23:20] (CLK_ZERO) and DPHY_DATA_TIMING_PARAM[19:16] (HS_ZERO)
    mipi_helper.verify_and_log_helper(register='DPHY_CLK_TIMING_PARAM' + port, field='CLK_ZERO', expected=VBT_TClkZero,
                                  actual=reg_dphy_clk_timing.clk_zero)
    mipi_helper.verify_and_log_helper(register='DPHY_DATA_TIMING_PARAM' + port, field='HS_ZERO', expected=VBT_THSZero,
                                  actual=reg_dphy_data_timing.hs_zero)

    ##
    # 3. Compare Prepare: DPHY_CLK_TIMING_PARAM[30:28] (CLK_PREPARE) and DPHY_DATA_TIMING_PARAM[26:24] (HS_PREPARE)
    mipi_helper.verify_and_log_helper(register='DPHY_CLK_TIMING_PARAM' + port, field='CLK_PREPARE',
                                  expected=VBT_TClkPrepare,
                                  actual=reg_dphy_clk_timing.clk_prepare)

    mipi_helper.verify_and_log_helper(register='DPHY_DATA_TIMING_PARAM' + port, field='HS_PREPARE', expected=VBT_THSPrepare,
                                  actual=reg_dphy_data_timing.hs_prepare)


##
# @brief        Verifies DPHY parameters in PHY (MiG DPHY) registers. Specific to LKF.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port - port name
# @param[in]    vbt_mipi_data - MipiDataStructureEntry of current panel from  Block 52 of vbt.
# @return       None
def _verify_dphy_phy_params_lkf(mipi_helper, port, vbt_mipi_data):
    logging.info('--------Verifying PHY params in DPHY registers--------')
    phy_lanes = ['_DL0', '_DL1', '_DL2', '_DL3', '_DL4']
    data_lanes = ['_DL0', '_DL1', '_DL3', '_DL4']
    clock_lanes = ['_DL2']
    if port == "_DSI0":
        ddi = '_A'
    else:
        ddi = '_B'

    panel_index = mipi_helper.get_panel_index_for_port(port)
    vbt_mipi_timings = _mipi_helper.VbtMipiTimings()
    vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, panel_index)
    vbt_mipi_timings.adjust_timings_for_mipi_config(mipi_helper, panel_index)
    bpp = mipi_helper.get_bpp(panel_index)
    lane_count = mipi_helper.get_lane_count(panel_index)

    # calculate UI
    dotClock = vbt_mipi_timings.pixelClockHz

    bitRate = (dotClock * bpp) / (lane_count * 1.0)
    UIinNs = (10 ** 9) / bitRate

    # calculate N (N = escape clock divider M / 8)
    reg_dsi_esc_clk_div = MMIORegister.read("DSI_ESC_CLK_DIV_REGISTER", "DSI_ESC_CLK_DIV" + port, mipi_helper.platform)
    N = int(math.ceil(reg_dsi_esc_clk_div.escape_clock_divider_m / 8.0))

    # from VBT fetch - Exit, Trail, Zero, Prepare for Clock(Clk) and Data(HS)
    # VBT values are in ns. Convert them to escape clocks (50ns = 1 escape clock)
    # only for THSPrepare and TClkPrepare, after converting to escape clocks, encode it with granularity of
    # 0.25 escape clocks. 0b001 = 0.25 Escape clocks
    # Then, convert them to words clocks (wordClock_value = escClock_value * N)
    # we program DSI controller with escClock value. So, we calculate respective wordClock value and program in DPHY.
    # we can also calculate words clocks using UI; but don't use this approach as final value won't match DSI phy
    # value. Number of Word Clocks = Roundup( Roundup( PARAM / UI ) / 8)
    VBT_THSTrail = int(math.ceil(vbt_mipi_data.THSTrail / 50.0))
    VBT_THSTrail = VBT_THSTrail * N
    VBT_THSZero = vbt_mipi_data.THSPrepareHSZero - vbt_mipi_data.THSPrepare
    VBT_THSZero = int(math.ceil(VBT_THSZero / 50.0))
    VBT_THSZero = VBT_THSZero * N
    VBT_THSPrepare = int(math.ceil((vbt_mipi_data.THSPrepare / 50.0) * 4))
    VBT_THSPrepare = int(math.ceil((VBT_THSPrepare / 4.0) * N))

    VBT_TClkTrail = int(math.ceil(vbt_mipi_data.TClkTrail / 50.0))
    VBT_TClkTrail = VBT_TClkTrail * N
    VBT_TClkZero = vbt_mipi_data.TClkPrepareClkZero - vbt_mipi_data.TClkPrepare
    VBT_TClkZero = int(math.ceil(VBT_TClkZero / 50.0))
    VBT_TClkZero = VBT_TClkZero * N
    VBT_TClkPrepare = int(math.ceil((vbt_mipi_data.TClkPrepare / 50.0) * 4))
    VBT_TClkPrepare = int(math.ceil((VBT_TClkPrepare / 4.0) * N))

    # 1. verify CBBS_CLOCK_CTRL_REG register
    hs_clock_distribution_to_right_enable = 0
    if (mipi_helper.get_lane_count(panel_index) > 2):
        hs_clock_distribution_to_right_enable = 1
    dfe_clock_divider = int(math.floor(bitRate / ((10 ** 6) * 125.0))) - 1
    logging.info('Expected values for CBBS_CLOCK_CTRL_REG register: hs_clock_distribution_to_left_enable= 1, '
                 'hs_clock_distribution_to_right_enable= %d, '
                 'hs_tx_word_clock_divider= 3, '
                 'dfe_clock_divider= %d (i.e Floor(8x/125))' % (
                     hs_clock_distribution_to_right_enable, dfe_clock_divider))

    cbbs_clock_ctrl_reg = importlib.import_module("registers.%s.CBBS_CLOCK_CTRL_REG_REGISTER" % (mipi_helper.platform))
    reg_cbbs_clock_ctrl = MMIORegister.read("CBBS_CLOCK_CTRL_REG_REGISTER", "CBBS_CLOCK_CTRL_REG" + ddi,
                                            mipi_helper.platform)

    if (reg_cbbs_clock_ctrl.hs_clock_distribution_to_left_enable == getattr(cbbs_clock_ctrl_reg,
                                                                            "hs_clock_distribution_to_left_enable_ENABLED") and
            reg_cbbs_clock_ctrl.hs_clock_distribution_to_right_enable == hs_clock_distribution_to_right_enable and
            reg_cbbs_clock_ctrl.hs_tx_word_clock_divider == getattr(cbbs_clock_ctrl_reg,
                                                                    "hs_tx_word_clock_divider_DIVIDE_BY_8") and
            reg_cbbs_clock_ctrl.dfe_clock_divider == dfe_clock_divider):
        logging.info('PASS: CBBS_CLOCK_CTRL_REG%s (for port %s) register is programmed correct' % (ddi, port))
    else:
        logging.error('FAIL: CBBS_CLOCK_CTRL_REG%s (for port %s) register is programmed wrong. Register values are '
                      'hs_clock_distribution_to_left_enable= %d, hs_clock_distribution_to_right_enable= %d, '
                      'hs_tx_word_clock_divider= %d, dfe_clock_divider= %d'
                      % (ddi, port, reg_cbbs_clock_ctrl.hs_clock_distribution_to_left_enable,
                         reg_cbbs_clock_ctrl.hs_clock_distribution_to_right_enable,
                         reg_cbbs_clock_ctrl.hs_tx_word_clock_divider, reg_cbbs_clock_ctrl.dfe_clock_divider))
        mipi_helper.verify_fail_count += 1

    # 2. verify DBBUDLN_MST_SLV_INIT_CTL register
    for lane in phy_lanes:
        reg_dbbudln_mst_slv_init_ctl = MMIORegister.read("DBBUDLN_MST_SLV_INIT_CTL_REGISTER",
                                                         "DBBUDLN_MST_SLV_INIT_CTL" + lane + ddi, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_MST_SLV_INIT_CTL' + lane + ddi, field='timer configuration',
                                      expected=1,
                                      actual=reg_dbbudln_mst_slv_init_ctl.master_slave_init_timer_configuration)

    # 3. verify DBBUDLN_TX_TIMING_CTL1 register
    for lane in phy_lanes:
        dbbudln_tx_timing_ctl = importlib.import_module(
            "registers.%s.DBBUDLN_TX_TIMING_CTL1_REGISTER" % (mipi_helper.platform))
        reg_dbbudln_tx_timing_ctl1 = MMIORegister.read("DBBUDLN_TX_TIMING_CTL1_REGISTER",
                                                       "DBBUDLN_TX_TIMING_CTL1" + lane + ddi, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_TX_TIMING_CTL1' + lane + ddi,
                                      field='early HS Tx Ready generation enable',
                                      expected=getattr(dbbudln_tx_timing_ctl,
                                                       "txhs_early_ppi_ready_generation_enable_ENABLED"),
                                      actual=reg_dbbudln_tx_timing_ctl1.txhs_early_ppi_ready_generation_enable)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_TX_TIMING_CTL1' + lane + ddi,
                                      field='early HS Tx Ready generation timer', expected=2,
                                      actual=reg_dbbudln_tx_timing_ctl1.txhs_early_ppi_ready_generation_timer)

    # 4. verify DBBUDLN_TX_TIMING_CTL2 register
    for lane in phy_lanes:
        dbbudln_tx_timing_ctl2 = importlib.import_module(
            "registers.%s.DBBUDLN_TX_TIMING_CTL2_REGISTER" % (mipi_helper.platform))
        reg_dbbudln_tx_timing_ctl2 = MMIORegister.read("DBBUDLN_TX_TIMING_CTL2_REGISTER",
                                                       "DBBUDLN_TX_TIMING_CTL2" + lane + ddi, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_TX_TIMING_CTL2' + lane + ddi,
                                      field='auto-deskew initialization',
                                      expected=getattr(dbbudln_tx_timing_ctl2,
                                                       "tx_hs_auto_initial_deskew_enable_DISABLED"),
                                      actual=reg_dbbudln_tx_timing_ctl2.tx_hs_auto_initial_deskew_enable)

    ##
    # DPHY timing params registers
    # 1. Compare Trail: DBBUDLN_TX_TIMING_CTL0[31:24] (tTRAIL) (value is zero based)
    for lane in phy_lanes:
        if lane in data_lanes:
            vbt_trail = VBT_THSTrail
        else:
            vbt_trail = VBT_TClkTrail
        reg_dbbudln_tx_timing_ctl0 = MMIORegister.read("DBBUDLN_TX_TIMING_CTL0_REGISTER",
                                                       "DBBUDLN_TX_TIMING_CTL0" + lane + ddi, mipi_helper.platform)
        # Don't verify these. Driver is leaving TClkTrail & THSTrail at hardware default, since programming
        # high values of THsTrail is leading to TEoT crossing DPHY spec mandated maximum values (which violates DPHY compliance).
        # verify_and_log_helper(register= 'DBBUDLN_TX_TIMING_CTL0' + lane + ddi, field= 'tTRAIL', expected= (vbt_trail - 1),
        #                           actual= reg_dbbudln_tx_timing_ctl0.ttrail_timer)

    ##
    # 2. Compare Zero: DBBUDLN_TX_TIMING_CTL0[23:16] (tZERO) (value is zero based)
    for lane in phy_lanes:
        if lane in data_lanes:
            vbt_zero = VBT_THSZero
        else:
            vbt_zero = VBT_TClkZero
        reg_dbbudln_tx_timing_ctl0 = MMIORegister.read("DBBUDLN_TX_TIMING_CTL0_REGISTER",
                                                       "DBBUDLN_TX_TIMING_CTL0" + lane + ddi, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_TX_TIMING_CTL0' + lane + ddi, field='tZERO',
                                      expected=(vbt_zero - 1), actual=reg_dbbudln_tx_timing_ctl0.tzero_timer)

    ##
    # 3. Compare Prepare: DBBUDLN_TX_TIMING_CTL0[15:8] (tPREPARE) (value is zero based)
    for lane in phy_lanes:
        if lane in data_lanes:
            vbt_prepare = VBT_THSPrepare
        else:
            vbt_prepare = VBT_TClkPrepare
        reg_dbbudln_tx_timing_ctl0 = MMIORegister.read("DBBUDLN_TX_TIMING_CTL0_REGISTER",
                                                       "DBBUDLN_TX_TIMING_CTL0" + lane + ddi, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DBBUDLN_TX_TIMING_CTL0' + lane + ddi, field='tPREPARE',
                                      expected=(vbt_prepare - 1), actual=reg_dbbudln_tx_timing_ctl0.tprepare_timer)


##
# @brief        Verifies DPHY parameters in DSI registers.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port - port name
# @param[in]    vbt_mipi_data - MipiDataStructureEntry of current panel from  Block 52 of vbt.
# @return       None
def _verify_dsi_phy_params(mipi_helper, port, vbt_mipi_data):
    # from VBT fetch - Exit, Trail, Zero, Prepare for Clock(Clk) and Data(HS)
    # VBT values are in ns. Convert them to escape clocks (50ns = 1 escape clock)
    # only for THSPrepare and TClkPrepare, after converting to escape clocks, encode it with granularity of 0.25 escape clocks. 0b001 = 0.25 Escape clocks
    VBT_THSTrail = int(math.ceil(vbt_mipi_data.THSTrail / 50.0))
    VBT_THSZero = vbt_mipi_data.THSPrepareHSZero - vbt_mipi_data.THSPrepare
    VBT_THSZero = int(math.ceil(VBT_THSZero / 50.0))
    VBT_THSPrepare = int(math.ceil((vbt_mipi_data.THSPrepare / 50.0) * 4))

    VBT_TClkTrail = int(math.ceil(vbt_mipi_data.TClkTrail / 50.0))
    VBT_TClkZero = vbt_mipi_data.TClkPrepareClkZero - vbt_mipi_data.TClkPrepare
    VBT_TClkZero = int(math.ceil(VBT_TClkZero / 50.0))
    VBT_TClkPrepare = int(math.ceil((vbt_mipi_data.TClkPrepare / 50.0) * 4))

    ##
    # DSI registers
    logging.info('--------Verifying PHY params in DSI registers--------')
    ##
    # 1. Compare Trail: DSI_CLK_TIMING_PARAM[2:0] (CLK_TRAIL) and DSI_DATA_TIMING_PARAM[10:8] (HS_TRAIL)
    reg_dsi_clk_timing = MMIORegister.read("DSI_CLK_TIMING_PARAM_REGISTER", "DSI_CLK_TIMING_PARAM" + port,
                                           mipi_helper.platform)
    reg_dsi_data_timing = MMIORegister.read("DSI_DATA_TIMING_PARAM_REGISTER", "DSI_DATA_TIMING_PARAM" + port,
                                            mipi_helper.platform)

    # Don't verify these. Driver is leaving TClkTrail & THSTrail at hardware default, since programming
    # high values of THsTrail is leading to TEoT crossing DPHY spec mandated maximum values (which violates DPHY compliance).
    # verify_and_log_helper(register= 'DSI_CLK_TIMING_PARAM' + port, field= 'CLK_TRAIL', expected= VBT_TClkTrail,
    #                           actual= dsi_clk_timing.clk_trail)
    # verify_and_log_helper(register= 'DSI_DATA_TIMING_PARAM' + port, field= 'HS_TRAIL', expected= VBT_THSTrail,
    #                           actual= dsi_data_timing.hs_trail)

    ##
    # 2. Compare Zero: DSI_CLK_TIMING_PARAM[23:20] (CLK_ZERO) and DSI_DATA_TIMING_PARAM[19:16] (HS_ZERO)
    mipi_helper.verify_and_log_helper(register='DSI_CLK_TIMING_PARAM' + port, field='CLK_ZERO', expected=VBT_TClkZero,
                                  actual=reg_dsi_clk_timing.clk_zero)
    mipi_helper.verify_and_log_helper(register='DSI_DATA_TIMING_PARAM' + port, field='HS_ZERO', expected=VBT_THSZero,
                                  actual=reg_dsi_data_timing.hs_zero)

    ##
    # 3. Compare Prepare: DSI_CLK_TIMING_PARAM[30:28] (CLK_PREPARE) and DSI_DATA_TIMING_PARAM [26:24] (HS_PREPARE)
    mipi_helper.verify_and_log_helper(register='DSI_CLK_TIMING_PARAM' + port, field='CLK_PREPARE',
                                  expected=VBT_TClkPrepare, actual=reg_dsi_clk_timing.clk_prepare)

    mipi_helper.verify_and_log_helper(register='DSI_DATA_TIMING_PARAM' + port, field='HS_PREPARE', expected=VBT_THSPrepare,
                                  actual=reg_dsi_data_timing.hs_prepare)
