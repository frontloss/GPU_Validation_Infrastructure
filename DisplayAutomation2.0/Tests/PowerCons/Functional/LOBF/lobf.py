########################################################################################################################
# @file         lobf.py
# @brief        Contains APIs to verify LOBF
#
# @author       Bhargav Adigarla
########################################################################################################################
import logging
import math
import os
import subprocess
import time

from Libs.Core import etl_parser
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Tests.PowerCons.Functional.CMTG import cmtg
from Tests.PowerCons.Functional.DCSTATES import dc_state
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.PSR import psr, pr
from Tests.PowerCons.Modules import common, dpcd
from Tests.VRR import vrr
from registers.mmioregister import MMIORegister

AUX_LESS_WAKE_TIME = {
    1620: 103,
    2160: 95,
    2430: 94,
    2700: 90,
    3240: 89,
    3780: 86,
    4320: 86,
    5400: 83,
    6480: 82,
    6750: 82,
    8100: 81
}

MEDIA_FPS = 24
__FRAME_UPDATE_PATH = os.path.join(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons"), "FrameUpdate.exe")

##
# @brief        Verify ALPM capability of a panel
# @param[in]    panel - panel object
# @return       True if supported else False
def is_alpm_supported(panel):
    alpm_caps = dpcd.AlpmCaps(panel.target_id)
    return alpm_caps.aux_less_alpm_cap == 1


##
# @brief        Verify LOBF enabled in driver
# @param[in]  adapter - adapter object
# @param[in]    panel - panel object
# @return       True if supported else False
def is_lobf_enabled_in_driver(adapter, panel):
    alpm_info = adapter.regs.get_alpm_info(panel.pipe)
    return alpm_info.LinkOffBetweenFramesEnable == 1


##
# @brief        Verify AUX less LOBF enabled in driver
# @param[in]  adapter - adapter object
# @param[in]    panel - panel object
# @return       True if supported else False
def verify_auxless(adapter, panel):
    alpm_info = adapter.regs.get_alpm_info(panel.pipe)
    return alpm_info.AlpmAuxLessEnable == 1


##
# @brief        Verify AUX wake LOBF enabled in driver
# @param[in]  adapter - adapter object
# @param[in]    panel - panel object
# @return       True if supported else False
def verify_auxwake(adapter, panel):
    alpm_info = adapter.regs.get_alpm_info(panel.pipe)
    if alpm_info.AlpmAuxLessEnable:
        logging.error(f"Aux-less ALPM enabled for Aux-wake supported panel")
        return False
    if is_lobf_enabled_in_driver(adapter, panel):
        logging.error(f"LOBF enabled in driver for Aux-wake supported panel")
        return False
    return True


##
# @brief        Verify LOBF restrictions in driver
# @param[in]  adapter - adapter object
# @param[in]    panel - panel object
# @return       True if restrictions satisfied else False
def verify_restrictions(adapter, panel):
    try:
        frame_update = subprocess.Popen(__FRAME_UPDATE_PATH)
        time.sleep(3)
    except Exception as e:
        logging.error(e)
        frame_update = None
    ##
    # Get eDP DPCD version
    edp_dpcd_rev = dpcd.get_edp_revision(panel.target_id)
    if edp_dpcd_rev is None or edp_dpcd_rev == dpcd.EdpDpcdRevision.EDP_UNKNOWN:
        logging.error("\tInvalid eDP version found")
        return False

    if edp_dpcd_rev < edp_dpcd_rev.EDP_DPCD_1_5:
        logging.error("\tALPM supported from eDP1.5 onwards")
        return None

    if panel.vrr_caps.is_vrr_supported is False:
        logging.error(f"VRR not supported in {panel}")
        return False
    logging.info(f"VRR supported in {panel}")
    vrr_data = adapter.regs.get_vrr_info(panel.transcoder_type)
    if not (vrr_data.VrrVmax == vrr_data.VrrVmin and vrr_data.VrrVmin == vrr_data.VrrFlipLine):
        logging.error("panel is not at fixed refresh rate")
        return False
    logging.info("panel is at fixed refresh rate")
    if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1):
        logging.error(f"PSR1 enabled in {panel}")
        return False
    logging.info(f"PSR1 disabled in driver on {panel}")

    if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2):
        logging.error(f"PSR2 enabled in {panel}")
        return False
    logging.info(f"PSR2 disabled in driver on {panel}")

    if pr.is_enabled_in_driver(adapter, panel):
        logging.error(f"PR enabled in driver on {panel}")
        return False
    logging.info(f"PR disabled in driver on {panel}")
    video_dip_ctl = MMIORegister.read('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder, adapter.name,
                                      gfx_index=adapter.gfx_index)
    if video_dip_ctl.adaptive_sync_sdp_enable == 0x0:
        logging.error(f'Adaptive Sync SDP is disabled in driver on {panel.port}')
        gdhm.report_driver_bug_pc(f"[LOBF] Adaptive Sync SDP not enabled")
        return False
    if adapter.name not in common.GEN_16_PLATFORMS:
        if cmtg.verify_cmtg_slave_status(adapter, [panel]) is False:
            logging.error("CMTG Slave mode not enabled")
            return False

        if cmtg.verify_cmtg_timing(adapter, panel) is False:
            logging.error(f"cmtg verification failed")
            return False
        logging.info("CMTG timing verification successful")
    if verify_timing_support(adapter, panel) is False:
        logging.error(f"{panel} doesn't meet timing requirements")
        return False
    try:
        if frame_update is not None:
            frame_update.kill()
    except Exception as e:
        logging.error(e)
    return True


##
# @brief        Exposed API to verify PR timing support
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if enabled, False otherwise
def verify_timing_support(adapter, panel):
    status = True
    vblank_reg = MMIORegister.read(
        'TRANS_VBLANK_REGISTER', 'TRANS_VBLANK_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    v_total = MMIORegister.read(
        'TRANS_VTOTAL_REGISTER', 'TRANS_VTOTAL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    h_total = MMIORegister.read(
        'TRANS_HTOTAL_REGISTER', 'TRANS_HTOTAL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    vsync = MMIORegister.read(
        'TRANS_VSYNC_REGISTER', 'TRANS_VSYNC_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    alpm_ctl = MMIORegister.read(
        'ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    vrr_vmax = MMIORegister.read('TRANS_VRR_VMAX_REGISTER', 'TRANS_VRR_VMAX_' + panel.transcoder, adapter.name,
                                 gfx_index=adapter.gfx_index)

    context_latency = vblank_reg.vertical_blank_start - v_total.vertical_active
    if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
        vblank_size = v_total.vertical_total - v_total.vertical_active
        sdp_pos = v_total.vertical_total - vsync.vertical_sync_start
    else:
        vblank_size = vrr_vmax.vrr_vmax - v_total.vertical_active
        sdp_pos = vrr_vmax.vrr_vmax - vsync.vertical_sync_start
    link_rate_mbs = panel.link_rate * 1000
    line_time_micro_sec = math.ceil(
        (h_total.horizontal_total + 1) // (panel.native_mode.pixelClock_Hz // (1000 * 1000)))
    # math.ceil(AUX_LESS_WAKE_TIME[link_rate_mbs] / line_time_micro_sec)
    wake_time = alpm_ctl.aux_less_wake_time
    min_sleep_time = alpm_ctl.alpm_entry_check
    logging.debug(f"line time = {line_time_micro_sec} us. Link rate = {link_rate_mbs} mbps")
    logging.debug(f"wake time = {wake_time} , min sleep time = {min_sleep_time} context latency = {context_latency} "
                  f"vblank size = {vblank_size}, sdp_pos = {sdp_pos}")
    # LOBF can only be enabled if the AS SDP is positioned outside of Window 1
    if (context_latency + vblank_size) < sdp_pos:
        logging.error(f"Adaptive sync SDP is position check failed")
        gdhm.report_driver_bug_pc(f"[LOBF] Adaptive sync SDP is position check failed")
        return False
    # // Bspec formula for enabling is as follows
    #     // ((ContextLatency + Guardband) > (FirstSdpPosition + WakeTime))
    #     // but it will never work for us as GB > T1 , as GB = Vblank - SCL today in driver & SCL = 0 most of the time.
    #     // resulting in the rule chaning to  (0 + GB)  > (GB + Waketime).
    #     // since the purpose of this rule is to check if we can wake before GB let us check
    #     // if currentvblank is bigger than GB + Waketime + minimum sleep time.
    #     // if the above is true, then we can sleep for the remaining time , then wake before GB starts.
    if vblank_size < (sdp_pos + wake_time):
        logging.error("Vblank size is not meeting the ALPM sleep time")
        gdhm.report_driver_bug_pc("[LOBF] Vblank size is not meeting the ALPM sleep time")
        return False
    return status


##
# @brief        Exposed API to verify LOBF feature
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file ETL file path
# @param[in]    method APP/VIDEO/IDLE
# @return       status Boolean, True, if enabled, False otherwise
def verify_lobf(adapter, panel, etl_file, method):
    etl_parser.generate_report(etl_file)
    status = False
    alpm_ctl = MMIORegister.get_instance('ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name)
    alpm_ctl_data = etl_parser.get_mmio_data(alpm_ctl.offset, is_write=True)
    if alpm_ctl_data is None:
        logging.error(f"No MMIO entries found for offset-{hex(alpm_ctl.offset)} in ETL")
        return True

    if method == 'VIDEO':
        if dmrrs.verify(adapter, panel, etl_file, MEDIA_FPS) is False:
            return False
        for mmio_data in alpm_ctl_data:
            alpm_ctl.asUint = mmio_data.Data
            if alpm_ctl.link_Off_between_frames_enable == 0:
                logging.error(f"LOBF disabled in driver at {mmio_data.TimeStamp} ms")
                gdhm.report_driver_bug_pc(f"[LOBF] LOBF disabled during Fixed RR switch")
                return False

    elif method == 'GAME':
        if vrr.verify(adapter, panel, etl_file) is False:
            return False
        for mmio_data in alpm_ctl_data:
            alpm_ctl.asUint = mmio_data.Data
            if alpm_ctl.link_Off_between_frames_enable == 0:
                logging.info(f"LOBF disabled in driver at {mmio_data.TimeStamp} ms")
                status = True
                break
    else:
        if dc_state.verify_dc6_vbi(etl_file) is True:
            logging.error(f"Dc6 enabled on LOBF panel {panel.port}")
            return False
        for mmio_data in alpm_ctl_data:
            alpm_ctl.asUint = mmio_data.Data
            if alpm_ctl.link_Off_between_frames_enable == 0:
                logging.error(f"LOBF disabled in driver at {mmio_data.TimeStamp} ms")
                gdhm.report_driver_bug_pc(f"[LOBF] LOBF disabled during Fixed RR switch")
                return False
    return status
