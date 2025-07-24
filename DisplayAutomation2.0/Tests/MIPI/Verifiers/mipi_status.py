########################################################################################################################
# @file         mipi_status.py
# @brief        This file contains helper functions for verifying MIPI status bits
# @author       Geesala, Sri Sumanth
########################################################################################################################
import importlib
import logging

from registers.mmioregister import MMIORegister


##
# @brief        Checks status bits and returns whether mipi state is active or not. Checks Transcoder state and
#               powerwell state. Checks for all mipi ports sent as parameter list
# @param[in]    mipi_helper - MipiHelper object containing VBT and helper fields and functions
# @param[in]    port_list - list of port names
# @return       returns mipi active or inactive state
def check_mipi_status_bits(mipi_helper, port_list):
    logging.info('Checking MIPI status')
    ret = True

    # for each DSI port
    for index in range(len(port_list)):
        port = port_list[index]
        # check transcoder State (TRANS_CONF[30])
        trans_conf = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % (mipi_helper.platform))
        reg_trans_conf = MMIORegister.read("TRANS_CONF_REGISTER", "TRANS_CONF" + port, mipi_helper.platform)
        verify_ret = mipi_helper.verify_and_log_helper(register='TRANS_CONF' + port, field='Transcoder state',
                                                   expected=getattr(trans_conf, "transcoder_state_ENABLED"),
                                                   actual=reg_trans_conf.transcoder_state)
        ret = ret and verify_ret

        # check DDI IO Powerwell State (PWR_WELL_CTL_DDI[0 for DDIA][2 for DDIB])
        pwr_well_ctl_ddi = importlib.import_module("registers.%s.PWR_WELL_CTL_DDI_REGISTER" % (mipi_helper.platform))
        reg_pwr_well_ctl_ddi = MMIORegister.read("PWR_WELL_CTL_DDI_REGISTER", "PWR_WELL_CTL_DDI2", mipi_helper.platform)
        if port == "_DSI0":
            verify_ret = mipi_helper.verify_and_log_helper(register='PWR_WELL_CTL_DDI2',
                                                       field='ddi_a_io_power_state (for DSI0)',
                                                       expected=getattr(pwr_well_ctl_ddi,
                                                                        "ddi_a_io_power_state_ENABLED"),
                                                       actual=reg_pwr_well_ctl_ddi.ddi_a_io_power_state)
            ret = ret and verify_ret
        if port == "_DSI1":
            verify_ret = mipi_helper.verify_and_log_helper(register='PWR_WELL_CTL_DDI2',
                                                       field='ddi_b_io_power_state (for DSI1)',
                                                       expected=getattr(pwr_well_ctl_ddi,
                                                                        "ddi_b_io_power_state_ENABLED"),
                                                       actual=reg_pwr_well_ctl_ddi.ddi_b_io_power_state)
            ret = ret and verify_ret

        # read and display the pipe connected to :TRANS_DDI_FUNC_CTL[14:12]
        logging.info('INFO: TRANS_DDI_FUNC_CTL%s - pipe connected is %s' % (
            port, mipi_helper.get_connected_pipe_to_dsi_port(port)))

    return ret
