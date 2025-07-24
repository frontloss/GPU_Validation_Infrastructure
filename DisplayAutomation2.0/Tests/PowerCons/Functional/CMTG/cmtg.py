########################################################################################################################
# @file         cmtg.py
# @brief        File contains all CMTG related verification APIs or wrappers
#
# @author       Bhargav Adigarla
########################################################################################################################
import logging
import os

from DisplayRegs.DisplayOffsets import PsrOffsetValues, CmtgOffsetValues, VrrOffsetValues, InterruptOffsetValues
from Libs.Core import etl_parser, app_controls
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload, common
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.VRR import vrr
from registers.mmioregister import MMIORegister

display_config_ = DisplayConfiguration()
driver_interface_ = driver_interface.DriverInterface()


##
# @brief        API to enable CMTG with regkey
# @param[in]    adapter: Adapter type
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable(adapter: Adapter):
    display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
    status = None
    if display_feature_control.disable_cmtg != 0:
        display_feature_control.disable_cmtg = 0
        status = display_feature_control.update(adapter.gfx_index)
        if status is False:
            logging.error("\tFAILED to enable CMTG via DisplayFeatureControl registry")
            return False
    logging.info("\tSuccessfully enabled CMTG via DisplayFeatureControl registry")
    return status


##
# @brief        API to disable CMTG with regkey
# @param[in]    adapter: Adapter type
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable(adapter: Adapter):
    display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
    status = None
    if display_feature_control.disable_cmtg != 1:
        display_feature_control.disable_cmtg = 1
        status = display_feature_control.update(adapter.gfx_index)
        if status is False:
            logging.error("\tFAILED to disable CMTG via DisplayFeatureControl registry")
            return False
    logging.info("\tSuccessfully disabled CMTG via DisplayFeatureControl registry")
    return status


##
# @brief        This is a helper function verify CMTG insrance
# @param[in]    adapter: Adapter
# @param[in]    panels:  list of panels to be verified
# @return       True if success else false
def verify(adapter: Adapter, panels: [Panel]) -> bool:
    status = True
    if verify_cmtg_status(adapter) is False:
        logging.error("\t CMTG status expected: ENABLED actual: DISABLED")
        __report_gdhm("CMTG not enabled")
        return False

    logging.info("\t CMTG status expected: ENABLED actual: ENABLED")
    status, slaved_panel = verify_cmtg_slave_status(adapter, panels)
    if status is False:
        logging.error("\t CMTG slave status expected: ENABLED actual: DISABLED")
        status &= False
    logging.info("\t CMTG slave status expected: ENABLED actual: ENABLED")
    if verify_cmtg_timing(adapter, slaved_panel) is False:
        logging.error("\t CMTG timings status expected: MATCHING actual: NOT MATCHING")
        __report_gdhm(f"CMTG timing not matching with Transcoder timing for {slaved_panel.port}")
        status &= False
    else:
        logging.info("\t CMTG timings status expected: MATCHING actual: MATCHING")
    if is_pll0_assigned(adapter, slaved_panel) is False:
        logging.error("\t PLL0 assigned expected: TRUE actual: FALSE")
        status &= False
    else:
        logging.info("\t PLL0 assigned expected: TRUE actual: TRUE")
    return status


##
# @brief        Verify CMTG control register
# @param[in]    adapter: Adapter object
# @return       True if enabled else False
def verify_cmtg_status(adapter):
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        cmtg_ctl = MMIORegister.read("TRANS_CMTG_CTL_REGISTER", 'TRANS_CMTG_CTL', adapter.name)
        return cmtg_ctl.cmtg_enable == 1
    else:
        for panel in adapter.panels.values():
            if panel.is_lfp is False:
                continue
            cmtg_data = adapter.regs.get_cmtg_info(panel.transcoder_type)
            if cmtg_data.CmtgEnable == 0:
                logging.error(f"CMTG disabled in {panel}")
                return False
    return True


##
# @brief        Verify panel is slave to CMTG or not
# @param[in]    adapter: Adapter object
# @param[in]    panels: Panel object
# @return       True if enabled else False
def verify_cmtg_slave_status(adapter, panels: [Panel]):
    status = False
    slaved_panel = None
    for panel in panels:
        slave_status = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", 'TRANS_DDI_FUNC_CTL2_' +
                                         panel.pipe, adapter.name)
        if slave_status.cmtg_slave_mode == 1:
            logging.info(f"CMTG slave status enabled on transcoder {panel.transcoder}")
            status = True
            slaved_panel = panel
        else:
            logging.info(f"CMTG slave status disabled on transcoder {panel.transcoder}")
    if status is False:
        __report_gdhm(f"Panel is not slave to CMTG")
    return status, slaved_panel


##
# @brief        Verify CMTG transcoder timing is same as pipe transcoder
# @param[in]    adapter: Adapter object
# @param[in]    panel: Panel object
# @return       True if enabled else False
def verify_cmtg_timing(adapter, panel):
    trans_linkm1 = MMIORegister.read("LINKM_REGISTER", 'TRANS_LINKM1_'+panel.transcoder, adapter.name)
    trans_linkn1 = MMIORegister.read("LINKN_REGISTER", 'TRANS_LINKN1_'+panel.transcoder, adapter.name)

    cmtg_data = adapter.regs.get_cmtg_info(panel.transcoder_type)

    if trans_linkm1.link_m_value != cmtg_data.CmtgLinkM:
        logging.error(f"\tCMTG timings are different with transcoder timings cmtg_trans_linkm1: {cmtg_data.CmtgLinkM}: "
                      f"pipe_linkm1: {trans_linkm1.link_m_value}")
        return False
    logging.info(f"\tCMTG timings are matching with transcoder timings cmtg_trans_linkm1: {cmtg_data.CmtgLinkM}: "
                 f"pipe_linkm1: {trans_linkm1.link_m_value}")

    if trans_linkn1.link_n_value != cmtg_data.CmtgLinkN:
        logging.error(f"\tCMTG timings are differnt with transcoder timings cmtg_trans_linkn1: {cmtg_data.CmtgLinkN}: "
                      f"pipe_linkn1: {trans_linkn1.link_n_value}")
        return False
    logging.info(
        f"\tCMTG timings are matching with transcoder timings cmtg_trans_linkn1: {cmtg_data.CmtgLinkN}:"
        f" pipe_linkn1: {trans_linkn1.link_n_value}")
    return True


##
# @brief        API to check PLL0 assigned to port
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @return       True if PLL0 assigned else false
def is_pll0_assigned(adapter: Adapter, panel: Panel) -> bool:
    pll_status = MMIORegister.read("DPCLKA_CFGCR0_REGISTER", 'DPCLKA_CFGCR0', adapter.name)
    port = panel.port.split('_')[1]
    if port == 'A' and pll_status.ddia_clock_off == 0:
        if pll_status.ddia_clock_select == 0:
            logging.info("\t PLL0 assigned to port A")
            return True
    elif port == 'B' and pll_status.ddib_clock_off == 0:
        if pll_status.ddib_clock_select == 0:
            logging.info("\t PLL0 assigned to port B")
            return True
    logging.error("\t PLL0 is not assigned")
    __report_gdhm(f"PLL0 not assigned for {panel.port}")
    return False


##
# @brief        API to check CMTG VRR enable/disable sequence
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @param[in]    method: Video or Game
# @return       True if success else False
def verify_cmtg_vrr(adapter: Adapter, panel: Panel, method=None):
    before_wl_etl = None
    during_wl_etl = None
    status = True
    etl_path = test_context.LOG_FOLDER

    if method is None:
        method = 'GAME'

    if method == 'GAME':
        etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.Classic3DCubeApp, 30, True], idle_after_wl=True)
        # Ensure async flips
        if vrr.async_flips_present(etl_file) is False:
            etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True], idle_after_wl=True)
            if vrr.async_flips_present(etl_file) is False:
                logging.warning("OS is NOT sending async flips")
                return False
        for filename in os.listdir(etl_path):
            if "GfxTraceBeforeGame" in filename:
                before_wl_etl = os.path.join(test_context.LOG_FOLDER, filename)
            if "GfxTraceDuringGame" in filename:
                during_wl_etl = os.path.join(test_context.LOG_FOLDER, filename)

    if method == 'VIDEO':
        etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [24, 60], idle_after_wl=True)
        for filename in os.listdir(etl_path):
            if "GfxTraceBeforeVideo" in filename:
                before_wl_etl = os.path.join(test_context.LOG_FOLDER, filename)
            if "GfxTraceDuringVideo" in filename:
                during_wl_etl = os.path.join(test_context.LOG_FOLDER, filename)

    logging.info("\t\t{0}".format(panel.lrr_caps))
    if panel.lrr_caps.is_lrr_2_0_supported or panel.lrr_caps.is_lrr_2_5_supported:
        # CMTG is disabled/enabled if
        # - VRR is getting enabled in variable mode (Game)
        # - On Gen13 platforms, VRR is getting enabled in any mode
        if method == 'GAME' or (
                panel.lrr_caps.is_lrr_2_0_supported and (method == 'VIDEO') and (
                adapter.name in common.GEN_13_PLATFORMS)):
            if verify_enabling_seq(adapter, panel, before_wl_etl, during_wl_etl) is False:
                status = False
                logging.error("VRR+CMTG enabling sequence verification failed")
                __report_gdhm("Verification failed for VRR+CMTG ENABLING sequence")

            if verify_disabling_seq(adapter, panel, during_wl_etl) is False:
                status = False
                logging.error("VRR+CMTG disabling sequence verification failed")
                __report_gdhm("Verification failed for VRR+CMTG DISABLING sequence")

        # CMTG should not be disabled during video playback for Gen14+ platforms.
        if panel.lrr_caps.is_lrr_2_5_supported and (method == 'VIDEO') and (
                adapter.name not in common.PRE_GEN_14_PLATFORMS):
            if verify_cmtg_during_wl(adapter, panel, during_wl_etl) is False:
                status = False
                logging.error("CMTG disabled during workload")
                __report_gdhm(f"CMTG is disabled during workload for {panel.port}")

    return status


##
# @brief        API to check CMTG status during workload
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @param[in]    etl_file: etl file
# @return       True if success else False
def verify_cmtg_during_wl(adapter, panel, etl_file):
    status = True
    cmtg_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
    mmio_only_config = etl_parser.EtlParserConfig()
    mmio_only_config.mmioData = 1
    if etl_parser.generate_report(etl_file, mmio_only_config) is False:
        raise Exception("\tFailed to generate ETL report")

    cmtg_during_game = etl_parser.get_mmio_data(cmtg_offsets.CmtgControlReg, is_write=True, start_time=None, end_time=None)
    if cmtg_during_game is None:
        logging.info(f"CMTG disabled event not present in ETL")
        return True

    for mmio_data in cmtg_during_game:
        cmtg_val = adapter.regs.get_cmtg_info(panel.transcoder_type,CmtgOffsetValues(CmtgControlReg=mmio_data.Data))
        if cmtg_val.CmtgEnable == 0:
            logging.error(f"CMTG disabled during workload {mmio_data.Data} Timestamp {mmio_data.TimeStamp}")
            status = False

    return status


##
# @brief        API to check CMTG VRR enable sequence
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @param[in]    before_wl: ETL before workload
# @param[in]    during_wl: ETL during workload
# @return       True if success else False
def verify_enabling_seq(adapter, panel, before_wl, during_wl):
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL', adapter.name)
    else:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL_' + panel.transcoder,
                                                 adapter.name)
    vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    interrupt_offsets = adapter.regs.get_interrupt_offsets()
    psr2_offsets = adapter.regs.get_psr_offsets(panel.transcoder_type)
    pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)
    dc6v_offsets = adapter.regs.get_dcstate_offsets()
    seq_data = []
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr_offset = psr2_offsets.Psr2CtrlReg
    else:
        psr_offset = 0x60902

    mmio_only_config = etl_parser.EtlParserConfig()
    mmio_only_config.mmioData = 1

    logging.info(f" ETL file name before WL {before_wl}")
    if etl_parser.generate_report(before_wl, mmio_only_config) is False:
        raise Exception("\tFailed to generate ETL report")

    cmtg_before_game = etl_parser.get_mmio_data(cmtg_offsets.offset, is_write=True, start_time=None, end_time=None)
    vrr_before_game = etl_parser.get_mmio_data(vrr_offsets.VrrControl, is_write=True, start_time=None, end_time=None)
    interrupt_before_game = etl_parser.get_mmio_data(interrupt_offsets.InterruptIER, is_write=True, start_time=None, end_time=None)
    psr2_before_game = etl_parser.get_mmio_data(psr_offset, is_write=True, start_time=None, end_time=None)
    dc6v_before_game = etl_parser.get_mmio_data(dc6v_offsets.DcStateEnable, is_write=True, start_time=None, end_time=None)
    pr_before_game = etl_parser.get_mmio_data(pr_ctl.offset, is_write=True, start_time=None, end_time=None)

    logging.info(f"cmtg_before_game: {cmtg_before_game}")
    logging.info(f"vrr_before_game: {vrr_before_game}")
    logging.info(f"interrupt_before_game: {interrupt_before_game}")
    logging.info(f"psr2_before_game: {psr2_before_game}")
    logging.info(f"dc6v_before_game: {dc6v_before_game}")
    logging.info(f"pr_before_game: {pr_before_game}")

    logging.info(f" ETL file name during WL {during_wl}")
    if etl_parser.generate_report(during_wl, mmio_only_config) is False:
        raise Exception("\tFailed to generate ETL report")

    cmtg_during_game = etl_parser.get_mmio_data(cmtg_offsets.offset, is_write=True, start_time=None, end_time=None)
    vrr_during_game = etl_parser.get_mmio_data(vrr_offsets.VrrControl, is_write=True, start_time=None, end_time=None)
    interrupt_during_game = etl_parser.get_mmio_data(interrupt_offsets.InterruptIER, is_write=True, start_time=None, end_time=None)
    psr2_during_game = etl_parser.get_mmio_data(psr_offset, is_write=True, start_time=None, end_time=None)
    dc6v_during_game = etl_parser.get_mmio_data(dc6v_offsets.DcStateEnable, is_write=True, start_time=None,
                                                end_time=None)
    pr_after_game = etl_parser.get_mmio_data(pr_ctl.offset, is_write=True, start_time=None, end_time=None)

    logging.info(f"cmtg_during_game: {cmtg_during_game}")
    logging.info(f"vrr_during_game: {vrr_during_game}")
    logging.info(f"interrupt_during_game: {interrupt_during_game}")
    logging.info(f"psr2_during_game: {psr2_during_game}")
    logging.info(f"dc6v_during_game: {dc6v_during_game}")
    logging.info(f"pr_after_game: {pr_after_game}")

    if cmtg_before_game is not None:
        seq_data = seq_data + cmtg_before_game
    if cmtg_during_game is not None:
        seq_data = seq_data + cmtg_during_game
    if vrr_before_game is not None:
        seq_data = seq_data + vrr_before_game
    if vrr_during_game is not None:
        seq_data = seq_data + vrr_during_game
    if interrupt_before_game is not None:
        seq_data = seq_data + interrupt_before_game
    if interrupt_during_game is not None:
        seq_data = seq_data + interrupt_during_game
    if psr2_before_game is not None:
        seq_data = seq_data + psr2_before_game
    if psr2_during_game is not None:
        seq_data = seq_data + psr2_during_game
    if dc6v_before_game is not None:
        seq_data = seq_data + dc6v_before_game
    if dc6v_during_game is not None:
        seq_data = seq_data + dc6v_during_game
    if panel.pr_caps.is_pr_supported:
        if pr_before_game is not None:
            seq_data = seq_data + pr_before_game
        if pr_after_game is not None:
            seq_data = seq_data + pr_after_game

    seq_data.sort(key=lambda x: x.TimeStamp)
    logging.info(f"seq_data: {seq_data}")

    # Gaming VRR Enabling sequence:
    # 1. Disable PSR/PR in driver
    # 2. Disable CMTG
    # 3. Enable VRR
    start = 0
    feature_disable = False
    for index in range(start, len(seq_data)):
        for index in range(start, len(seq_data)):
            if panel.pr_caps.is_pr_supported:
                if seq_data[index].Offset == pr_ctl.offset:
                    pr_ctl.asUint = seq_data[index].Data
                    if pr_ctl.pr_enable == 0:
                        logging.info(
                            f"PR is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                        feature_disable = True
            else:
                if seq_data[index].Offset == psr_offset:
                    data = seq_data[index].Data
                    if psr_offset == 0x60902:
                        data = data << 16
                    psr2_val = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(Psr2CtrlReg=data))
                    if psr2_val.Psr2Enable == 0:
                        logging.info(
                            f"PSR2 is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                        feature_disable = True
                    if feature_disable:
                        start = index
                        for index in range(start, len(seq_data)):
                            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                                if seq_data[index].Offset == interrupt_offsets.InterruptIER:
                                    int_val = adapter.regs.get_interrupt_info(InterruptOffsetValues(InterruptIER=seq_data[index].Data))
                                    if int_val.InterruptIER_CmtgDelayedVblank == 0:
                                        logging.info(
                                            f"CmtgDelayedVblank interrupt is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")

                                        start = index
                            for index in range(start, len(seq_data)):
                                if seq_data[index].Offset == cmtg_offsets.offset:
                                    cmtg_offsets.asUint = seq_data[index].Data
                                    if cmtg_offsets.cmtg_enable == 0:
                                        logging.info(
                                            f"CMTG is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")

                                        start = index
                                        for index in range(start, len(seq_data)):
                                            if seq_data[index].Offset == vrr_offsets.VrrControl:
                                                vrr_val = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                                                     VrrOffsetValues(VrrControl=seq_data[index].Data))
                                                if vrr_val.VrrEnable == 1:
                                                    logging.info(
                                                        f"VRR is enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                                                    logging.info("VRR enabling sequence verification successful")
                                                    return True

    logging.error("VRR enabling sequence verification failed")
    return False


##
# @brief        API to check CMTG VRR disable sequence
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @param[in]    during_wl: ETL before workload
# @return       True if success else False
def verify_disabling_seq(adapter, panel, during_wl):
    status = True
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL', adapter.name)
    else:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL_' + panel.transcoder,
                                                 adapter.name)
    vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    interrupt_offsets = adapter.regs.get_interrupt_offsets()
    psr2_offsets = adapter.regs.get_psr_offsets(panel.transcoder_type)
    dc6v_offsets = adapter.regs.get_dcstate_offsets()
    pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)
    seq_data = []
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr_offset = psr2_offsets.Psr2CtrlReg
    else:
        psr_offset = 0x60902
    mmio_only_config = etl_parser.EtlParserConfig()
    mmio_only_config.mmioData = 1

    logging.info(f" ETL file name during_wl {during_wl}")
    if etl_parser.generate_report(during_wl, mmio_only_config) is False:
        raise Exception("\tFailed to generate ETL report")

    cmtg_during_game = etl_parser.get_mmio_data(cmtg_offsets.offset, is_write=True, start_time=None, end_time=None)
    vrr_during_game = etl_parser.get_mmio_data(vrr_offsets.VrrControl, is_write=True, start_time=None, end_time=None)
    interrupt_during_game = etl_parser.get_mmio_data(interrupt_offsets.InterruptIER, is_write=True, start_time=None, end_time=None)
    psr2_during_game = etl_parser.get_mmio_data(psr_offset, is_write=True, start_time=None, end_time=None)
    psr2_status_during_game = etl_parser.get_mmio_data(psr2_offsets.Psr2StatusReg, is_write=True, start_time=None, end_time=None)
    dc6v_during_game = etl_parser.get_mmio_data(dc6v_offsets.DcStateEnable, is_write=True, start_time=None, end_time=None)
    pr_during_game = etl_parser.get_mmio_data(pr_ctl.offset, is_write=True, start_time=None, end_time=None)

    logging.info(f"cmtg_during_game: {cmtg_during_game}")
    logging.info(f"vrr_during_game: {vrr_during_game}")
    logging.info(f"interrupt_during_game: {interrupt_during_game}")
    logging.info(f"psr2_during_game: {psr2_during_game}")
    logging.info(f"dc6v_during_game: {dc6v_during_game}")
    logging.info(f"PR during game: {pr_during_game}")

    if cmtg_during_game is not None:
        seq_data = seq_data + cmtg_during_game
    if vrr_during_game is not None:
        seq_data = seq_data + vrr_during_game
    if interrupt_during_game is not None:
        seq_data = seq_data + interrupt_during_game
    if dc6v_during_game is not None:
        seq_data = seq_data + dc6v_during_game
    if panel.pr_caps.is_pr_supported:
        seq_data = seq_data + pr_during_game
    if psr2_during_game is not None:
        seq_data = seq_data + psr2_during_game

    seq_data.sort(key=lambda x: x.TimeStamp)
    logging.info(f"seq_data: {seq_data}")

    # Gaming VRR Disable Sequence :
    # 1. Disable Gaming VRR / Enable Fixed RR VRR mode from GEN14+
    # 2. Enable PSR2/PR
    # 3. Enable CMTG
    disabling_seq = False
    if psr2_status_during_game is not None:
        for index in range(0, len(psr2_status_during_game)):
            psr2_status = adapter.regs.get_psr_info(panel.transcoder_type,
                                                    PsrOffsetValues(Psr2StatusReg=psr2_status_during_game[index].Data))
            if psr2_status.Psr2DeepSleep:
                disabling_seq = True
    elif panel.pr_caps.is_pr_supported:
        disabling_seq = True

    if disabling_seq is False:
        start = 0
        check_for_psr = False
        for index in range(start, len(seq_data)):
            for index in range(start, len(seq_data)):
                if seq_data[index].Offset == vrr_offsets.VrrControl:
                    vrr_val = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                        VrrOffsetValues(VrrControl=seq_data[index].Data))
                    if adapter.name in common.GEN_13_PLATFORMS:
                        if vrr_val.VrrEnable == 0:
                            logging.info(
                                f"VRR is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                            start = index
                            check_for_psr = True
                    else:
                        # From GEN14+ , Always VRR HW mode is enabled by default
                        if vrr_val.VrrEnable:
                            logging.info(
                                f"VRR still enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                            start = index
                            check_for_psr = True
                    if check_for_psr:
                        for index in range(start, len(seq_data)):
                            if seq_data[index].Offset == psr_offset:
                                data = seq_data[index].Data
                                if psr_offset == 0x60902:
                                    data = data << 16
                                psr2_val = adapter.regs.get_psr_info(panel.transcoder_type,
                                                                     PsrOffsetValues(Psr2CtrlReg=data))
                                if psr2_val.Psr2Enable == 1:
                                    logging.info(
                                        f"PSR2 is enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at "
                                        f"{seq_data[index].TimeStamp}")
                                    return True

        logging.error("VRR disabling sequence verification failed")
        return False

    start = 0
    for index in range(start,len(seq_data)):
        for index in range(start, len(seq_data)):
            if seq_data[index].Offset == vrr_offsets.VrrControl:
                vrr_val = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                    VrrOffsetValues(VrrControl=seq_data[index].Data))
                if adapter.name in common.GEN_13_PLATFORMS:
                    if vrr_val.VrrEnable == 0:
                        logging.info(
                            f"VRR is disabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                        start = index

                else:
                    # From GEN14+ , Always VRR HW mode is enabled by default
                    if vrr_val.VrrEnable:
                        logging.info(
                            f"VRR still enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                        start = index
                if start:
                    for index in range(start, len(seq_data)):
                        if seq_data[index].Offset == psr_offset:
                            data = seq_data[index].Data
                            if psr_offset == 0x60902:
                                data = data << 16
                            psr2_val = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=data))
                            if psr2_val.Psr2Enable == 1:
                                logging.info(f"PSR2 is enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at "
                                             f"{seq_data[index].TimeStamp}")
                                start = index
                        elif seq_data[index].Offset == pr_ctl.offset:
                            pr_ctl.val = seq_data[index].Data
                            if pr_ctl.pr_enable:
                                logging.info(
                                    f"PR is enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data} at "
                                    f"{seq_data[index].TimeStamp}")
                                start = index

                                for index in range(start, len(seq_data)):
                                    if seq_data[index].Offset == cmtg_offsets.CmtgControlReg:
                                        cmtg_offsets.asUint = seq_data[index].Data
                                        if cmtg_offsets.cmtg_enable == 1:
                                            logging.info(
                                                f"CMTG is enabled {hex(seq_data[index].Offset)} - {seq_data[index].Data}"
                                                f" at {seq_data[index].TimeStamp}")
                                        if panel.pr_caps.is_pr_supported and cmtg_offsets.cmtg_sync_to_port:
                                            logging.info(f"CMTG SYNC to port bit is enabled "
                                                         f"{hex(seq_data[index].Offset)} - {seq_data[index].Data} at "
                                                         f"{seq_data[index].TimeStamp}")
                                            start = index
                                            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                                                for index in range(start, len(seq_data)):
                                                    if seq_data[index].Offset == interrupt_offsets.InterruptIER:
                                                        int_val = adapter.regs.get_interrupt_info(
                                                            InterruptOffsetValues(InterruptIER=seq_data[index].Data))

                                                        if int_val.InterruptIER_CmtgDelayedVblank == 1:
                                                            logging.info(
                                                                f"CmtgDelayedVblank interrupt is enabled {hex(seq_data[index].Offset)}"
                                                                f" - {seq_data[index].Data} at {seq_data[index].TimeStamp}")
                                                            return True
                                            logging.info("VRR disabling sequence verification is successful")
                                            return status
    logging.error("VRR disabling sequence verification failed")
    return False


##
# @brief        API to check CMTG reg accessed after CLK enabled
# @param[in]    adapter: Adapter type
# @param[in]    panel: Panel type
# @param[in]    etl_file: ETL file path
# @return       True if success else False
def verify_cmtg_reg_access(adapter, panel, etl_file):
    transcoder_enable_time, clk_enable_time = None, None
    status = True
    etl_parser.generate_report(etl_file)
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL', adapter.name)
    else:
        cmtg_offsets = MMIORegister.get_instance('TRANS_CMTG_CTL_REGISTER', 'TRANS_CMTG_CTL_' + panel.transcoder,
                                                 adapter.name)

    trans_func_ctl = MMIORegister.get_instance('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_' + panel.transcoder,
                                               adapter.name)

    clk_sel = MMIORegister.get_instance('CMTG_CLK_SEL_REGISTER', 'CMTG_CLK_SEL', adapter.name)

    trans_ddi_ctl = etl_parser.get_mmio_data(trans_func_ctl.offset, is_write=True, start_time=None, end_time=None)
    cmtg_clk_sel = etl_parser.get_mmio_data(clk_sel.offset, is_write=True)

    if cmtg_clk_sel is None:
        logging.error(f"CMTG CLK SEL mmio data not found")
        return False
    if trans_ddi_ctl is None:
        logging.error(f"TRANS_DDI_FUNC_CTL mmio data not found")
        return False

    for data in trans_ddi_ctl:
        trans_func_ctl.asUint = data.Data
        if trans_func_ctl.trans_ddi_function_enable:
            transcoder_enable_time = data.TimeStamp
            logging.info(f"Transcoder enabled at {transcoder_enable_time}ms")
            break

    if transcoder_enable_time is None:
        logging.error("Transcoder is not enabled")
        return False

    for data in cmtg_clk_sel:
        clk_sel.asUint = data.Data
        if clk_sel.cmtg_a_clk_sel != 0:
            clk_enable_time = data.TimeStamp
            logging.info(f'CMTG CLK enabled at {clk_enable_time}ms')
            break
    if clk_enable_time is None:
        logging.error("CMTG CLK is not enabled")
        return False
    cmtg_data = etl_parser.get_mmio_data(cmtg_offsets.offset, is_write=False, start_time=transcoder_enable_time, end_time=None)

    # Check CMTG CTL register read happened only after CMTG_CLK enable
    if cmtg_data is None:
        logging.info("PASS: CMTG_CTL register not read before CLK enable")
        return True
    for data in cmtg_data:
        if data.TimeStamp < clk_enable_time:
            logging.error(f"CMTG CTL register read with out CLK enable at {data.TimeStamp}ms")
            status &= False

    return status






def __report_gdhm(title):
    gdhm.report_bug(
        title="[PowerCons][CMTG] " + title,
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
