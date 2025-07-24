########################################################################################################################
# @file         mipi_link_related.py
# @brief        This file contains helper functions for verifying MIPI Link Config
# @author       Geesala, Sri Sumanth
########################################################################################################################

import importlib
import logging

from Libs.Feature.mipi import mipi_helper as _mipi_helper
from registers.mmioregister import MMIORegister


##
# @brief        Verifies whether link configuration is programmed correct.
# @param[in]    mipi_helper object of MipiHelper class
# @param[in]    port - port name
# @return       None
def verify_link_config(mipi_helper, port):
    panel_index = mipi_helper.get_panel_index_for_port(port)

    VBT_clock_stop = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].ClockStop
    VBT_eotp_disabled = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].EOTDisabled
    bpp = mipi_helper.get_bpp(panel_index)
    lane_count = mipi_helper.get_lane_count(panel_index)
    vbt_mipi_timings = _mipi_helper.VbtMipiTimings()
    vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, panel_index)
    vbt_mipi_timings.adjust_timings_for_mipi_config(mipi_helper, panel_index)
    dotClock = vbt_mipi_timings.pixelClockHz
    DSI_link_freq_Ghz = (dotClock * bpp) / (lane_count * pow(10, 9) * 1.0)

    ##
    # 1. Compare Clock-stop enable/disable: TRANS_DSI_FUNC_CONF[9:8]
    trans_dsi_func_conf = importlib.import_module("registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))
    reg_trans_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                                mipi_helper.platform)
    if VBT_clock_stop == 0:
        mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='continuous_clock',
                                      expected=getattr(trans_dsi_func_conf, "continuous_clock_CONTINUOUS_HS_CLOCK"),
                                      actual=reg_trans_dsi_func_conf.continuous_clock, message='VBT_clock_stop= 0')
    elif VBT_clock_stop == 1:
        if reg_trans_dsi_func_conf.continuous_clock != getattr(trans_dsi_func_conf,
                                                               "continuous_clock_CONTINUOUS_HS_CLOCK"):
            logging.info(
                'PASS: TRANS_DSI_FUNC_CONF%s - continuous_clock - VBT_clock_stop= %d \t \t Expected= 0 or 2 \t Actual= %d'
                % (port, VBT_clock_stop, reg_trans_dsi_func_conf.continuous_clock))
        else:
            logging.error(
                'FAIL: TRANS_DSI_FUNC_CONF%s - continuous_clock - VBT_clock_stop= %d \t \t Expected= 0 or 2 \t Actual= %d'
                % (port, VBT_clock_stop, reg_trans_dsi_func_conf.continuous_clock))
            mipi_helper.verify_fail_count += 1

    ##
    # 2. Compare EOTp-disabled: TRANS_DSI_FUNC_CONF[0]
    mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='EOTp-disabled',
                                  expected=VBT_eotp_disabled,
                                  actual=reg_trans_dsi_func_conf.eotp_disabled)

    trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (mipi_helper.platform))
    reg_trans_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port,
                                               mipi_helper.platform)

    ##
    # 3. Verify Scrambling bit: TRANS_DDI_FUNC_CTL[0]. Scrambling must be enabled when the Link frequency is greater than 2.5 Gbps
    if (DSI_link_freq_Ghz > 2.5):
        mipi_helper.verify_and_log_helper(register='TRANS_DDI_FUNC_CTL' + port, field='Scrambling enable',
                                      expected=getattr(trans_ddi_func_ctl, "hdmi_scrambling_enabled_ENABLE"),
                                      actual=reg_trans_ddi_func_ctl.hdmi_scrambling_enabled,
                                      message='DSI link freq= %f. Scrambling must be enabled when link frequency is greater than 2.5 Gbps' % (
                                          DSI_link_freq_Ghz))

    ##
    # 4. Verify Link Calibration: TRANS_DSI_FUNC_CONF[5:4]. Link Calibration must be enabled if the Link frequency is operating above 1.5 Gbps
    if (DSI_link_freq_Ghz > 1.5):
        if (reg_trans_dsi_func_conf.link_calibration == getattr(trans_dsi_func_conf,
                                                                "link_calibration_CALIBRATION_ENABLED___INITIAL_ONLY") or
                reg_trans_dsi_func_conf.link_calibration == getattr(trans_dsi_func_conf,
                                                                    "link_calibration_CALIBRATION_ENABLED___INITIAL_AND_PERIODIC")):
            logging.info('PASS: TRANS_DSI_FUNC_CONF%s - Link Calibration -  DSI link freq= %d. '
                         'Link Calibration must be enabled when the Link frequency is operating above 1.5 Gbps \t \t Expected= 2 or 3 \t '
                         'Actual= %d' % (port, DSI_link_freq_Ghz, reg_trans_dsi_func_conf.link_calibration))
        else:
            logging.error('FAIL: TRANS_DSI_FUNC_CONF%s - Link Calibration -  DSI link freq= %d. '
                          'Link Calibration must be enabled when the Link frequency is operating above 1.5 Gbps \t \t Expected= 2 or 3 \t '
                          'Actual= %d' % (port, DSI_link_freq_Ghz, reg_trans_dsi_func_conf.link_calibration))
            mipi_helper.verify_fail_count += 1

    ##
    # 5. Verify Tx slew rate programming for TGL. https://gfxspecs.intel.com/Predator/Home/Index/49188
    if mipi_helper.platform == 'tgl':
        data_lane_list = ['_LN0', '_LN1', '_LN3', '_AUX']  # we don't touch '_LN2'. It is clock lane.
        if port == "_DSI0":
            ddi = '_A'
        else:
            ddi = '_B'

        if (DSI_link_freq_Ghz <= 1.5):
            for lane_name in data_lane_list:
                reg_port_tx_dw1 = MMIORegister.read("PORT_TX_DW1_REGISTER", "PORT_TX_DW1" + lane_name + ddi,
                                                    mipi_helper.platform)
                mipi_helper.verify_and_log_helper(register='PORT_TX_DW1' + lane_name + ddi, field='o_tx_slew_ctrl',
                                              expected=3, actual=reg_port_tx_dw1.o_tx_slew_ctrl)
        else:
            for lane_name in data_lane_list:
                reg_port_tx_dw1 = MMIORegister.read("PORT_TX_DW1_REGISTER", "PORT_TX_DW1" + lane_name + ddi,
                                                    mipi_helper.platform)
                mipi_helper.verify_and_log_helper(register='PORT_TX_DW1' + lane_name + ddi, field='o_tx_slew_ctrl',
                                              expected=0, actual=reg_port_tx_dw1.o_tx_slew_ctrl)

        if (DSI_link_freq_Ghz == 2.5):
            reg_port_tx_dw6 = MMIORegister.read("PORT_TX_DW6_REGISTER", "PORT_TX_DW6_LN2" + ddi,
                                                mipi_helper.platform)
            mipi_helper.verify_and_log_helper(register='PORT_TX_DW6_LN2' + ddi, field='o_ldo_ref_sel_cri',
                                          expected=3, actual=reg_port_tx_dw6.o_ldo_ref_sel_cri)
        else:
            reg_port_tx_dw6 = MMIORegister.read("PORT_TX_DW6_REGISTER", "PORT_TX_DW6_LN2" + ddi,
                                                mipi_helper.platform)
            mipi_helper.verify_and_log_helper(register='PORT_TX_DW6_LN2' + ddi, field='o_ldo_ref_sel_cri',
                                          expected=0, actual=reg_port_tx_dw6.o_ldo_ref_sel_cri)


##
# @brief        Verifies if timeouts are programmed in accordance with VBT.
# @param[in]    mipi_helper object of MipiHelper class
# @param[in]    port - port name
# @return       None
def verify_timeouts(mipi_helper, port):
    ##
    # 1. Compare LP_Rx_TimeOut: DSI_LRX_H_TO[15:0]
    # Expected Max LP RX TimeOut = (183 EscClks +(N*8*2) EscClks) +Extra(4 EscClks). N=32 for now
    # This calculation is based on DPHY 1.2 spec
    Expected_lp_rx_h_timeout = (183 + (32 * 16) + 4)
    reg_lrx_h_to = MMIORegister.read("DSI_LRX_H_TO_REGISTER", "DSI_LRX_H_TO" + port, mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='DSI_LRX_H_TO' + port, field='LP_Rx_TimeOut',
                                  expected=Expected_lp_rx_h_timeout,
                                  actual=reg_lrx_h_to.lp_rx_h_timeout)

    ##
    # 2. Compare TurnAround_TimeOut: DSI_TA_TO [15:0]
    # Expected Max TA TimeOut = 14 EscClks + 1 Extra EscClks (Expected Max TA TimeOut for LKF = 134 EscClks + 1 Extra EscClks to support DCS read functionality)
    # This calculation is based on DPHY 1.2 spec
    if mipi_helper.platform == 'lkf1':
        Expected_turnaround_timeout = (134 + 1)
    else:
        Expected_turnaround_timeout = (14 + 1)
    reg_ta_to = MMIORegister.read("DSI_TA_TO_REGISTER", "DSI_TA_TO" + port, mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='DSI_TA_TO' + port, field='TurnAround_TimeOut',
                                  expected=Expected_turnaround_timeout,
                                  actual=reg_ta_to.turnaround_timeout)

    ##
    # 3. HS_Tx_TimeOut: DSI_HTX_TO[31:16] is not programmed by s/w. Kept default. Printing this value for debug purposes.
    reg_htx_to = MMIORegister.read("DSI_HTX_TO_REGISTER", "DSI_HTX_TO" + port, mipi_helper.platform)
    logging.info('INFO: DSI_HTX_TO%s - HS_Tx_TimeOut= %d' % (port, reg_htx_to.hs_tx_timeout))

    ##
    # 4. DeviceReset_Timer: DSI_PWAIT_TO[31:16] is not programmed by s/w. Kept default. Printing this value for debug purposes.
    reg_pwait_to = MMIORegister.read("DSI_PWAIT_TO_REGISTER", "DSI_PWAIT_TO" + port, mipi_helper.platform)
    logging.info('INFO: DSI_PWAIT_TO%s - DeviceReset_Timer= %d' % (port, reg_pwait_to.peripheral_reset_timeout))

    ##
    # 5. Peripheral_Response_Timeout: DSI_PWAIT_TO[15:0]. s/w programs this value to default value and not configurable through vbt. Printing this value for debug purposes.
    logging.info(
        'INFO: DSI_PWAIT_TO%s - Peripheral_Response_Timeout= %d' % (port, reg_pwait_to.peripheral_response_timeout))


##
# @brief        Verifies if pixel format and number of data lanes are programmed in accordance with VBT.
# @param[in]    mipi_helper object of MipiHelper class
# @param[in]    port - port name
# @return       None
def verify_pixel_format_data_lanes(mipi_helper, port):
    panel_index = mipi_helper.get_panel_index_for_port(port)

    # get pixel format and number of data lanes from VBT
    VBT_pixel_format = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].VideoModeColorFormat
    VBT_no_of_data_lanes = mipi_helper.get_lane_count(panel_index)

    ##
    # 1. verify color format: TRANS_DSI_FUNC_CONF[18:16]
    reg_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                          mipi_helper.platform)
    if mipi_helper.DSC_enabled:
        VBT_pixel_format = 0b111  # In DSC case, overwrite VBT pixel format with 'compressed' (vbt values for this field is 1 more than reg).
    mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='pixel format',
                                  expected=mipi_helper.decode_pixel_format(VBT_pixel_format - 1),
                                  actual=mipi_helper.decode_pixel_format(reg_dsi_func_conf.pixel_format))

    ##
    # 2. verify number of data lanes: TRANS_DDI_FUNC_CTL[3:1]. Data lane count is stored as 0 based in register field.
    reg_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port,
                                         mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_DDI_FUNC_CTL' + port, field='number of data lanes',
                                  expected=VBT_no_of_data_lanes,
                                  actual=(reg_ddi_func_ctl.port_width_selection + 1))
