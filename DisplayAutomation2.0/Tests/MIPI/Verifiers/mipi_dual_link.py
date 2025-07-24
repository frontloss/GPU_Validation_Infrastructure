########################################################################################################################
# @file         mipi_dual_link.py
# @brief        This file contains helper functions for verifying MIPI Dual Link Config
# @author       Geesala, Sri Sumanth
########################################################################################################################

import importlib
import logging

from Libs.Feature.mipi import mipi_helper as _mipi_helper
from registers.mmioregister import MMIORegister


##
# @brief        Verifies if required register bits are programmed for MIPI to run in dual link mode.
# @param[in]    mipi_helper object of MipiHelper class
# @return       None
def verify_dual_link_config(mipi_helper):
    dss_ctl1 = None
    reg_dss_ctl1 = None
    reg_dss_ctl2 = None
    ##
    # 1. verify if 'Splitter enable' bit is enabled :DSS_CTL1[31]
    if mipi_helper.platform in ['icl', 'jsl']:
        dss_ctl1 = importlib.import_module("registers.%s.DSS_CTL1_REGISTER" % (mipi_helper.platform))
        reg_dss_ctl1 = MMIORegister.read("DSS_CTL1_REGISTER", "DSS_CTL1", 'icl')
    elif mipi_helper.platform in ['lkf1', 'tgl', 'ryf', 'adlp']:
        dss_ctl1 = importlib.import_module("registers.%s.PIPE_DSS_CTL1_REGISTER" % (mipi_helper.platform))
        reg_dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", "PIPE_DSS_CTL1_PA", 'lkf1')

    mipi_helper.verify_and_log_helper(register='DSS_CTL1', field='Dual link (splitter_enable)',
                                  expected=getattr(dss_ctl1, "splitter_enable_ENABLE"),
                                  actual=reg_dss_ctl1.splitter_enable)

    ##
    # 2. compare 'Dual link mode' bit with vbt :DSS_CTL1[24]
    # VBT: dual link support values: 0b01 = Dual link front back mode 0b10 = Dual link Interleave mode
    # register bit: 0b0 = Front-Back mode, 0b1 = Interleave mode
    VBT_dual_link_mode = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[mipi_helper.panel1_index].DualLinkSupport
    dual_link_modes = ['Front-Back', 'Interleaved']
    mipi_helper.verify_and_log_helper(register='DSS_CTL1', field='Dual link mode',
                                  expected=dual_link_modes[VBT_dual_link_mode - 1],
                                  actual=dual_link_modes[reg_dss_ctl1.dual_link_mode])

    # if front-back mode
    if (reg_dss_ctl1.dual_link_mode == getattr(dss_ctl1, "dual_link_mode_FRONT_BACK_MODE")):
        ##
        # 3. compare 'Overlap' value with vbt :DSS_CTL1[19:16]
        VBT_overlap = mipi_helper.gfx_vbt.block_42.PixelOverlapCount[mipi_helper.panel1_index]
        mipi_helper.verify_and_log_helper(register='DSS_CTL1', field='Pixel Overlap', expected=VBT_overlap,
                                      actual=reg_dss_ctl1.overlap,
                                      message='Overlap has to be programmed in front-back mode')

        ##
        # 4. if front-back mode, 'Right DL Buffer Target Depth' :DSS_CTL2[11:0] should be programmed(should be equal to hactive/2 + overlap)
        vbt_mipi_timings = _mipi_helper.VbtMipiTimings()
        vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, mipi_helper.panel1_index)
        vbt_mipi_timings.adjust_timings_for_mipi_config(mipi_helper, mipi_helper.panel1_index)
        VBT_hactive = vbt_mipi_timings.hactive

        if mipi_helper.platform in ['icl', 'jsl']:
            reg_dss_ctl2 = MMIORegister.read("DSS_CTL2_REGISTER", "DSS_CTL2", mipi_helper.platform)
        elif mipi_helper.platform in ['lkf1', 'tgl', 'ryf', 'adlp']:
            reg_dss_ctl2 = MMIORegister.read("PIPE_DSS_CTL2_REGISTER", "PIPE_DSS_CTL2_PA", mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='DSS_CTL2', field='Right DL Buffer Target Depth',
                                      expected=(VBT_hactive + VBT_overlap),
                                      actual=reg_dss_ctl2.right_dl_buffer_target_depth)

    ##
    # 5. check Port Sync Mode Enable bit :TRANS_DDI_FUNC_CTL2[4]
    reg_ddi_func_ctl2_0 = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", "TRANS_DDI_FUNC_CTL2_DSI0",
                                            mipi_helper.platform)
    reg_ddi_func_ctl2_1 = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", "TRANS_DDI_FUNC_CTL2_DSI1",
                                            mipi_helper.platform)
    if (reg_ddi_func_ctl2_0.port_sync_mode_enable == 1 and reg_ddi_func_ctl2_1.port_sync_mode_enable == 1):
        logging.info(
            'PASS: TRANS_DDI_FUNC_CTL2 - Port Sync Mode Enable bit \t \t Expected= [1 (DSI0), 1 (DSI1)] \t Actual= [%d, %d]'
            % (reg_ddi_func_ctl2_0.port_sync_mode_enable, reg_ddi_func_ctl2_1.port_sync_mode_enable))
    else:
        logging.error(
            'FAIL: TRANS_DDI_FUNC_CTL2 - Port Sync Mode Enable bit \t \t Expected= [1 (DSI0), 1 (DSI1)] \t Actual= [%d, %d]'
            % (reg_ddi_func_ctl2_0.port_sync_mode_enable, reg_ddi_func_ctl2_1.port_sync_mode_enable))
        mipi_helper.verify_fail_count += 1


##
# @brief        finds whether required register bits are programmed on the current port
#               to enable port sync in dual MIPI case.
# @param[in]    mipi_helper  object of MipiHelper class
# @param[in]    port  port name
# @return       True if all required bits are enabled, False otherwise
def is_dual_mipi_port_sync_enabled(mipi_helper, port):
    reg_ddi_func_ctl2 = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", "TRANS_DDI_FUNC_CTL2" + port,
                                          mipi_helper.platform)
    logging.info('TRANS_DDI_FUNC_CTL2{0} - Port Sync Mode Enable = {1} \t \t Dual pipe sync enable = '
                 '{2}'.format(port, reg_ddi_func_ctl2.port_sync_mode_enable, reg_ddi_func_ctl2.dual_pipe_sync_enable))

    if reg_ddi_func_ctl2.port_sync_mode_enable == 1 and reg_ddi_func_ctl2.dual_pipe_sync_enable == 1:
        return True
    else:
        return False
