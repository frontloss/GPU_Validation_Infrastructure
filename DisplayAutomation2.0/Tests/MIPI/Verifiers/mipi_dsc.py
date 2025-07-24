########################################################################################################################
# @file         mipi_dsc.py
# @brief        This file contains helper functions for verifying MIPI DSC config
# @author       Geesala, Sri Sumanth
########################################################################################################################

import importlib
import logging

from Libs.Core.logger import gdhm
from Libs.Feature.mipi import mipi_helper as _mipi_helper
from registers.mmioregister import MMIORegister


##
# @brief        Verifies DSC configuration register bits based on current MIPI mode.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port_list - list of port names
# @return       None
def verify_dsc_config(mipi_helper, port_list):
    if mipi_helper.platform in ['icl', 'jsl']:
        _verify_dsc_config_icl(mipi_helper, port_list)
    elif mipi_helper.platform in ['lkf1', 'tgl', 'ryf', 'adlp']:
        _verify_dsc_config_lkf1(mipi_helper, port_list)
    else:
        gdhm.report_bug(
            title="[MIPI][DSC] DSC verification not configured",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("DSC verification not configured for %s" % (mipi_helper.platform))
        mipi_helper.verify_fail_count += 1


##
# @brief        Verifies DSC configuration register bits based on current MIPI mode. Specific to ICL.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port_list - list of port names
# @return       None
def _verify_dsc_config_icl(mipi_helper, port_list):
    splitter_enable = 0
    expected_left_vdsc_engine = 0
    expected_right_vdsc_engine = 0
    logging.info('Checking DSC configuration')

    dss_ctl1 = importlib.import_module("registers.%s.DSS_CTL1_REGISTER" % (mipi_helper.platform))
    reg_dss_ctl1 = MMIORegister.read("DSS_CTL1_REGISTER", "DSS_CTL1", mipi_helper.platform)
    splitter_enable = reg_dss_ctl1.splitter_enable
    logging.info('Splitter= %d' % (splitter_enable))
    logging.info('Number of ports= %d' % (len(port_list)))
    dsc_slices_per_line = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[
        mipi_helper.panel1_index].DSCSlicesPerLine
    logging.info('DSC slices per line= %d' % (dsc_slices_per_line))
    ##
    # 1. Verify whether Left (DSS_CTL2[31] for DSI0) and right (DSS_CTL2[15] for DSI1) branches VDSC are enabled/disabled.
    # for dual link and dual LFP MIPI cases
    if (len(port_list) == 2):
        expected_left_vdsc_engine = 1
        expected_right_vdsc_engine = 1
    # for single link with one VDSC engine or two VDSC engines cases
    else:
        # if slices per line is greater than 1, both left and right VDSC engines should be enabled; only one otherwise
        if (dsc_slices_per_line == 1):
            if (port_list[0] == "_DSI0"):
                expected_left_vdsc_engine = 1
            elif (port_list[0] == "_DSI1"):
                expected_right_vdsc_engine = 1
        else:
            expected_left_vdsc_engine = 1
            expected_right_vdsc_engine = 1

    reg_dss_ctl2 = MMIORegister.read("DSS_CTL2_REGISTER", "DSS_CTL2", mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='DSS_CTL2', field='Left VDSC engine enable',
                                  expected=expected_left_vdsc_engine,
                                  actual=reg_dss_ctl2.left_branch_vdsc_enable)
    mipi_helper.verify_and_log_helper(register='DSS_CTL2', field='Right VDSC engine enable',
                                  expected=expected_right_vdsc_engine,
                                  actual=reg_dss_ctl2.right_branch_vdsc_enable)

    ##
    # 2. Verify if Joiner is enabled/disabled. For single link with splitter enabled, joiner (DSS_CTL1[30]) should be enabled.
    # For single link with only left engine enabled (when dsc_slices_per_line==1), dual link and dual LFP MIPI cases, joiner should be disabled.
    if (len(port_list) == 1 and dsc_slices_per_line > 1):
        mipi_helper.verify_and_log_helper(register='DSS_CTL1', field='Joiner enable',
                                      expected=getattr(dss_ctl1, "joiner_enable_ENABLE"),
                                      actual=reg_dss_ctl1.joiner_enable,
                                      message='Joiner should be enabled, for single link with both left and right engines enabled')
    else:
        mipi_helper.verify_and_log_helper(register='DSS_CTL1', field='Joiner enable',
                                      expected=getattr(dss_ctl1, "joiner_enable_DISABLE"),
                                      actual=reg_dss_ctl1.joiner_enable,
                                      message='Joiner should be disabled for cases - single link with only left engine enabled, dual link or dual LFP MIPI')

    ##
    # 3. Verify pixel format (TRANS_DSI_FUNC_CONF[18:16]). This should be set to 'Compressed' (110b).
    for port in port_list:
        dsi_func_conf = importlib.import_module("registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))
        reg_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                              mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='pixel format',
                                      expected='Compressed',
                                      actual=mipi_helper.decode_pixel_format(reg_dsi_func_conf.pixel_format))

    ##
    # Verify dsc picture parameter set
    for port in port_list:
        _verify_dsc_pps_parameters(mipi_helper, port, mipi_helper.get_connected_pipe_to_dsi_port(port),
                                   expected_left_vdsc_engine,
                                   expected_right_vdsc_engine)


##
# @brief        Verifies DSC configuration register bits based on current MIPI mode. For LKF1+ platforms.
# @param[in]    mipi_helper - object of MipiHelper class
# @param[in]    port_list - list of port names
# @return       None
def _verify_dsc_config_lkf1(mipi_helper, port_list):
    expected_left_vdsc_engine = expected_right_vdsc_engine = 0
    trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (mipi_helper.platform))
    pipe_suffix_dict = {getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_A"): '_PA',
                        getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_B"): '_PB',
                        getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_C"): '_PC',
                        getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_D"): '_PD',
                        }
    if mipi_helper.dual_LFP_MIPI:
        num_pipes = 2
    else:
        num_pipes = 1

    pipes_list = []
    for port in port_list:
        reg_trans_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port,
                                                   mipi_helper.platform)
        pipe_suffix = pipe_suffix_dict[reg_trans_ddi_func_ctl.edp_dsi_input_select]
        pipes_list.append(pipe_suffix)

        if num_pipes == 1:
            break

    dsc_slices_per_line = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[
        mipi_helper.panel1_index].DSCSlicesPerLine
    logging.info('DSC slices per line= %d' % (dsc_slices_per_line))

    # for each pipe, verify left branch VDSC enable, left branch VDSC enable and joiner
    for index in range(num_pipes):
        pipe = pipes_list[index]
        port = port_list[index]  # current port on this pipe
        splitter_enable = 0
        expected_left_vdsc_engine = 0
        expected_right_vdsc_engine = 0

        pipe_dss_ctl1 = importlib.import_module("registers.%s.PIPE_DSS_CTL1_REGISTER" % (mipi_helper.platform))

        reg_pipe_dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", "PIPE_DSS_CTL1" + pipe, mipi_helper.platform)
        reg_pipe_dss_ctl2 = MMIORegister.read("PIPE_DSS_CTL2_REGISTER", "PIPE_DSS_CTL2" + pipe, mipi_helper.platform)
        splitter_enable = reg_pipe_dss_ctl1.splitter_enable
        logging.info('Pipe %s: Splitter= %d' % (pipe, splitter_enable))

        ##
        # 1. Verify whether Left (PIPE_DSS_CTL2[31]) and right (PIPE_DSS_CTL2[15]) branches VDSC are enabled/disabled.
        # for dual link case
        if mipi_helper.dual_link:
            expected_left_vdsc_engine = 1
            expected_right_vdsc_engine = 1
        # for single link or dual LFP MIPI(for port on this pipe) cases. with one VDSC engine or two VDSC engines cases
        else:
            expected_left_vdsc_engine = 1
            if dsc_slices_per_line > 1:
                expected_right_vdsc_engine = 1

        mipi_helper.verify_and_log_helper(register='PIPE_DSS_CTL2' + pipe, field='Left VDSC engine enable',
                                      expected=expected_left_vdsc_engine,
                                      actual=reg_pipe_dss_ctl2.left_branch_vdsc_enable, message='port= %s' % (port))

        mipi_helper.verify_and_log_helper(register='PIPE_DSS_CTL2' + pipe, field='Right VDSC engine enable',
                                      expected=expected_right_vdsc_engine,
                                      actual=reg_pipe_dss_ctl2.right_branch_vdsc_enable, message='port= %s' % (port))

        ##
        # 2. Verify if Joiner is enabled/disabled.
        # For single link or Dual LFP MIPI(for port on this pipe) with dsc_slices_per_line > 1, joiner (PIPE_DSS_CTL1[30]) should be enabled.
        # For single link or Dual LFP MIPI(for port on this pipe) with dsc_slices_per_line == 1 , or dual link cases, joiner should be disabled.
        if (mipi_helper.dual_link == 0 and dsc_slices_per_line > 1):
            mipi_helper.verify_and_log_helper(register='PIPE_DSS_CTL1' + pipe, field='Joiner enable',
                                          expected=getattr(pipe_dss_ctl1, "joiner_enable_ENABLE"),
                                          actual=reg_pipe_dss_ctl1.joiner_enable,
                                          message='port= %s. For single link or Dual LFP MIPI with dsc_slices_per_line > 1, joiner should be enabled' % (
                                              port))
        else:
            mipi_helper.verify_and_log_helper(register='PIPE_DSS_CTL1' + pipe, field='Joiner enable',
                                          expected=getattr(pipe_dss_ctl1, "joiner_enable_DISABLE"),
                                          actual=reg_pipe_dss_ctl1.joiner_enable,
                                          message='port= %s. For single link or Dual LFP MIPI with dsc_slices_per_line == 1, or dual link cases, joiner should be disabled' % (
                                              port))
    # end of for

    ##
    # 3. Verify pixel format (TRANS_DSI_FUNC_CONF[18:16]). This should be set to 'Compressed' (110b).
    for port in port_list:
        trans_dsi_func_conf = importlib.import_module(
            "registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))
        reg_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                              mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='pixel format',
                                      expected='Compressed',
                                      actual=mipi_helper.decode_pixel_format(reg_dsi_func_conf.pixel_format))

    ##
    # Verify dsc picture parameter set
    for port in port_list:
        _verify_dsc_pps_parameters(mipi_helper, port, mipi_helper.get_connected_pipe_to_dsi_port(port),
                                   expected_left_vdsc_engine,
                                   expected_right_vdsc_engine)


##
# @brief        Verifies DSC PPS parameters.
# @param[in]    mipi_helper - MIPI Helper
# @param[in]    port - name of port to verify
# @param[in]    pipe_suffix - pipe on which this port is connected
# @param[in]    expected_left_vdsc_engine - expected enable/disable of left vdsc engine
# @param[in]    expected_right_vdsc_engine - expected enable/disable of left vdsc engine
# @return       None
def _verify_dsc_pps_parameters(mipi_helper, port, pipe_suffix, expected_left_vdsc_engine, expected_right_vdsc_engine):
    logging.info("**************MIPI DSC PPS PARAMETER VERIFICATION START : {} **************".format(port))
    pipes_list = []
    vdsc_engine_index_list = []
    port_log_format = port.replace('_', '')

    num_slices_per_line_vbt_map = dict([
        (1, 1),
        (2, 2),
        (4, 4),
        (6, 8),
        (8, 16),
        (10, 32),
        (12, 64),
        (16, 128),
        (20, 256),
        (24, 512)
    ])
    panel_index = mipi_helper.get_panel_index_for_port(port)

    vbt_panel_data = mipi_helper.gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index]
    vbt_mipi_timings = _mipi_helper.VbtMipiTimings()
    vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, panel_index)
    expected_pic_width = vbt_mipi_timings.hactive
    expected_pic_height = vbt_mipi_timings.vactive

    bpc_bits = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[panel_index].DSCColorDepthCapabilities
    vbt_bpc_value_for_current_panel = 8 if bpc_bits & 0b0010 else 10 if bpc_bits & 0b0100 else 12

    bpp_bits = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[panel_index].DSCMaximumBitsPerPixel
    vbt_bpp_value_for_current_panel = 6 if bpp_bits == 0 else 8 if bpp_bits == 1 else 10 if bpp_bits == 2 else 12

    slice_width_bits = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[panel_index].DSCSlicesPerLine
    vbt_slice_width_value_for_current_panel = vbt_mipi_timings.hactive / num_slices_per_line_vbt_map[slice_width_bits]

    vbt_slice_height_value_for_current_panel = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[
        panel_index].DSCSliceHeight

    # if left and right engine both are enable then picture width will be half of hactive
    if (expected_right_vdsc_engine == 1 and expected_left_vdsc_engine == 1):
        # HW will add overlap, SW shouldn't add it
        expected_pic_width = vbt_mipi_timings.hactive / 2

    if expected_left_vdsc_engine == 1:
        vdsc_engine_index_list.append("0")
    if expected_right_vdsc_engine == 1:
        vdsc_engine_index_list.append("1")

    for i in range(len(vdsc_engine_index_list)):
        # BPC verification
        reg_dsc_pps_0 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_0",
                                          "PPS0_%s_%s" % (vdsc_engine_index_list[i], pipe_suffix), mipi_helper.platform)
        actual_bits_per_component_left_vdsc_engine = reg_dsc_pps_0.bits_per_component
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_0_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='bits_per_component (for ' + port_log_format + ')', expected=vbt_bpc_value_for_current_panel,
            actual=actual_bits_per_component_left_vdsc_engine)

        # BPP verification
        reg_dsc_pps_1 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_1",
                                          "PPS1_%s_%s" % (vdsc_engine_index_list[i], pipe_suffix), mipi_helper.platform)
        actual_bits_per_pixel_left_vdsc_engine = reg_dsc_pps_1.bits_per_pixel / 16  # bits per pixel is stored in X.Y format. 9:4 bits are integer and 3:0 are fractional
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_1_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='bits_per_pixel (for ' + port_log_format + ')', expected=vbt_bpp_value_for_current_panel,
            actual=actual_bits_per_pixel_left_vdsc_engine)

        # slice width,height verification
        reg_dsc_pps_3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3",
                                          "PPS3_%s_%s" % (vdsc_engine_index_list[i], pipe_suffix), mipi_helper.platform)
        actual_slice_width_left_vdsc_engine = reg_dsc_pps_3.slice_width
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_3_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='slice_width (for ' + port_log_format + ')', expected=vbt_slice_width_value_for_current_panel,
            actual=actual_slice_width_left_vdsc_engine)
        actual_slice_height_left_vdsc_engine = reg_dsc_pps_3.slice_height
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_3_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='slice_height (for ' + port_log_format + ')', expected=vbt_slice_height_value_for_current_panel,
            actual=actual_slice_height_left_vdsc_engine)

        # picture width,height verification
        reg_dsc_pps_2 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_2",
                                          "PPS2_%s_%s" % (vdsc_engine_index_list[i], pipe_suffix), mipi_helper.platform)
        actual_picture_width_left_vdsc_engine = reg_dsc_pps_2.pic_width
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_2_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='pic_width (for ' + port_log_format + ')', expected=expected_pic_width,
            actual=actual_picture_width_left_vdsc_engine)
        actual_pic_height_left_vdsc_engine = reg_dsc_pps_2.pic_height
        mipi_helper.verify_and_log_helper(
            register='DSC_PICTURE_PARAMETER_SET_2_' + vdsc_engine_index_list[i] + "_" + pipe_suffix,
            field='pic_height (for ' + port_log_format + ')', expected=expected_pic_height,
            actual=actual_pic_height_left_vdsc_engine)

    logging.info("**************MIPI DSC PPS PARAMETER VERIFICATION END : {} **************".format(port))
