########################################################################################################################
# @file         mipi_video_mode.py
# @brief        This file contains helper functions for verifying if required register bits are programmed to enable
#               MIPI in video mode
# @author       Geesala, Sri Sumanth
########################################################################################################################
import importlib
import logging

from registers.mmioregister import MMIORegister


##
# @brief        Verifies if required register bits are programmed to enable MIPI in video mode. Applicable for
#               video mode only
# @param[in]    mipi_helper - MipiHelper object containing VBT and helper fields and functions
# @param[in]    port - port name
# @return       None
def verify_video_mode_enable_bits(mipi_helper, port):
    VBT_mode_of_operation = None
    panel_index = mipi_helper.get_panel_index_for_port(port)
    VideoTransferMode = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].VideoTransferMode
    trans_dsi_func_conf = importlib.import_module("registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))

    if (VideoTransferMode == 0b01):
        VBT_mode_of_operation = getattr(trans_dsi_func_conf, "mode_of_operation_VIDEO_MODE_SYNC_PULSE")
    elif (VideoTransferMode == 0b10):
        VBT_mode_of_operation = getattr(trans_dsi_func_conf, "mode_of_operation_VIDEO_MODE_SYNC_EVENT")
    elif (VideoTransferMode == 0b11):
        VBT_mode_of_operation = getattr(trans_dsi_func_conf,
                                        "mode_of_operation_VIDEO_MODE_SYNC_EVENT")  # 0b11 is burst mode in VBT. For burst mode also, we program as sync event.
    if (mipi_helper.DSC_enabled):
        VBT_mode_of_operation = getattr(trans_dsi_func_conf,
                                        "mode_of_operation_VIDEO_MODE_SYNC_EVENT")  # If compression is enabled, we program as sync event.

    ##
    # 1. compare mode of operation :TRANS_DSI_FUNC_CONF[29:28].
    reg_trans_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                                mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port, field='Mode of operation',
                                  expected=VBT_mode_of_operation,
                                  actual=reg_trans_dsi_func_conf.mode_of_operation,
                                  message='expected MIPI to run in Video mode')

    ##
    # 2. verify if transcoder DDI function is enabled :TRANS_DDI_FUNC_CTL[31]
    trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (mipi_helper.platform))
    reg_trans_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port,
                                               mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_DDI_FUNC_CTL' + port, field='Transcoder DDI function enable',
                                  expected=getattr(trans_ddi_func_ctl, "trans_ddi_function_enable_ENABLE"),
                                  actual=reg_trans_ddi_func_ctl.trans_ddi_function_enable)

    ##
    # 3. verify if timing generator is enabled :TRANS_CONF[31]
    if not (
            port == "_DSI1" and mipi_helper.dual_link == 1):  # SW doesn't explicitly enable DSI1 transcoder for dual link case
        trans_conf = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % (mipi_helper.platform))
        reg_trans_conf = MMIORegister.read("TRANS_CONF_REGISTER", "TRANS_CONF" + port, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='TRANS_CONF' + port, field='transcoder enable',
                                      expected=getattr(trans_conf, "transcoder_enable_ENABLE"),
                                      actual=reg_trans_conf.transcoder_enable)

    ##
    # 4. read and display the pipe connected to :TRANS_DDI_FUNC_CTL[14:12]
    logging.info(
        'INFO: TRANS_DDI_FUNC_CTL%s - pipe connected is %s' % (port, mipi_helper.get_connected_pipe_to_dsi_port(port)))

    ##
    # 5. Verify if DDI powerwell enable is programmed. PWR_WELL_CTL_DDI[1] (DDI A for DSI0), PWR_WELL_CTL_DDI[3] (DDI B for DSI1)
    pwr_well_ctl_ddi = importlib.import_module("registers.%s.PWR_WELL_CTL_DDI_REGISTER" % (mipi_helper.platform))
    reg_pwr_well_ctl_ddi = MMIORegister.read("PWR_WELL_CTL_DDI_REGISTER", "PWR_WELL_CTL_DDI2", mipi_helper.platform)
    if (port == "_DSI0"):
        mipi_helper.verify_and_log_helper(register='PWR_WELL_CTL_DDI2', field='ddi_a_io_power_request (for DSI0)',
                                      expected=getattr(pwr_well_ctl_ddi, "ddi_a_io_power_request_ENABLE"),
                                      actual=reg_pwr_well_ctl_ddi.ddi_a_io_power_request)

    if (port == "_DSI1"):
        mipi_helper.verify_and_log_helper(register='PWR_WELL_CTL_DDI2', field='ddi_b_io_power_request (for DSI1)',
                                      expected=getattr(pwr_well_ctl_ddi, "ddi_b_io_power_request_ENABLE"),
                                      actual=reg_pwr_well_ctl_ddi.ddi_b_io_power_request)


    ##
    # 6. Verify guardband value for lp to hs communication ADLP_WA: 16012360555(https://gfxspecs.intel.com/Predator/Home/Index/54369)
    if mipi_helper.platform.upper() == "ADLP":
        expected_lp_to_hs_wakeup_guardband = 0x4 # ADLP_WA: 16012360555

        if port == "_DSI0":
            register_dsi_chkn_offset_name = "DSI_CHKN_REG0_0"
        else:
            register_dsi_chkn_offset_name = "DSI_CHKN_REG0_1"

        dsi_chkn_reg0 = importlib.import_module("registers.%s.DSI_CHKN_REG0_REGISTER" % (mipi_helper.platform))
        reg_dsi_chkn_reg0 = MMIORegister.read("DSI_CHKN_REG0_REGISTER", register_dsi_chkn_offset_name, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register=register_dsi_chkn_offset_name, field='lp_to_hs_wakeup_guardband',
                                      expected=expected_lp_to_hs_wakeup_guardband,
                                      actual=reg_dsi_chkn_reg0.lp_to_hs_wakeup_guardband)
