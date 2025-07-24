########################################################################################################################
# @file         mipi_command_mode.py
# @brief        This file contains helper functions for verifying Mipi in command mode
# @author       Geesala, Sri Sumanth
########################################################################################################################

import importlib
import logging

from registers.mmioregister import MMIORegister


##
# @brief        This function verifies if required register bits are programmed to enable MIPI in command mode.
#               Applicable for command mode only.
# @param[in]    mipi_helper object of MipiHelper class
# @param[in]    port - port name
# @return       None
def verify_command_mode_enable_bits(mipi_helper, port):
    panel_index = mipi_helper.get_panel_index_for_port(port)
    logging.info('VBT: DSIUsage= %d' % (mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].DSIUsage))

    ##
    # 1. compare mode of operation :TRANS_DSI_FUNC_CONF[29:28]
    trans_dsi_func_conf = importlib.import_module("registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))
    reg_trans_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                                mipi_helper.platform)

    if (reg_trans_dsi_func_conf.mode_of_operation == getattr(trans_dsi_func_conf,
                                                             "mode_of_operation_COMMAND_MODE_NO_GATE")
            or reg_trans_dsi_func_conf.mode_of_operation == getattr(trans_dsi_func_conf,
                                                                    "mode_of_operation_COMMAND_MODE_TE_GATE")):
        logging.info('PASS: TRANS_DSI_FUNC_CONF%s - MIPI is running in command mode' % (port))
    else:
        logging.error('FAIL: TRANS_DSI_FUNC_CONF%s - MIPI is not running in command mode' % (port))
        mipi_helper.verify_fail_count += 1

    ##
    # 2. verify if transcoder DDI function is enabled :TRANS_DDI_FUNC_CTL[31]
    trans_dsi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (mipi_helper.platform))
    reg_trans_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port,
                                               mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_DDI_FUNC_CTL' + port, field='Transcoder DDI function enable',
                                       expected=getattr(trans_dsi_func_ctl, "trans_ddi_function_enable_ENABLE"),
                                       actual=reg_trans_ddi_func_ctl.trans_ddi_function_enable)

    ##
    # 3. verify if transcoder is enabled :TRANS_CONF[31]
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
    # 5. Verify if DDI powerwell enable is programmed. PWR_WELL_CTL_DDI[1] (DDI A -for DSI0), PWR_WELL_CTL_DDI[3]
    # (DDI B -for DSI1)
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
    # 6. Verify 'util pin enable' and 'util pin direction'. Need not be programmed in dual link.
    if (mipi_helper.dual_link == 0 and
            reg_trans_dsi_func_conf.te_source == getattr(trans_dsi_func_conf,
                                                         "te_source_OUT_OF_BAND_TE_EVENT_SOURCE_I_E__GPIO")):
        logging.info('MIPI is in single-link command mode and TE events received out-of band. '
                     'In this case, Util pin should be enabled and Util pin direction should be input')

        util_pin_ctl = importlib.import_module("registers.%s.UTIL_PIN_CTL_REGISTER" % (mipi_helper.platform))
        reg_util_pin_ctl = MMIORegister.read("UTIL_PIN_CTL_REGISTER", "UTIL_PIN_CTL", mipi_helper.platform)

        if (reg_util_pin_ctl.util_pin_enable == getattr(util_pin_ctl, "util_pin_enable_ENABLE") and
                reg_util_pin_ctl.util_pin_direction == getattr(util_pin_ctl, "util_pin_direction_INPUT")):
            logging.info('PASS: UTIL_PIN_CTL - Util pin is enabled and Util pin direction is input')
        else:
            logging.error('FAIL: UTIL_PIN_CTL - Util pin is programmed wrong. Util pin = %d, Util pin direction= %d' % (
                reg_util_pin_ctl.util_pin_enable, reg_util_pin_ctl.util_pin_direction))
            mipi_helper.verify_fail_count += 1
