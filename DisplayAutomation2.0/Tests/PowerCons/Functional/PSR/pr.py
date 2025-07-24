#######################################################################################################################
# @file         pr.py
# @brief        Contains Panel Replay verification APIs
#
# @author       Chandrakanth Reddy
#######################################################################################################################

import logging
import math

from Libs.Core import display_utility, etl_parser
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Feature.powercons import registry
from Tests.Planes.Common import planes_verification
from Tests.PowerCons.Modules import common, dpcd
from Tests.PowerCons.Functional.PSR import sfsu
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

##
# @brief        Exposed API to check if given PR is supported or not
# @param[in]    target_id target_id of Panel
# @param[in]    port DP_A/HDMI_B
# @param[in]    gfx_index gfx0/gfx_1
# @return       status Boolean, True, if enabled, False otherwise
def is_supported_in_panel(target_id, port, gfx_index):
    panel_type = display_utility.get_vbt_panel_type(port, gfx_index)
    if panel_type == display_utility.VbtPanelType.HDMI:
        logging.info("PR is not supported on HDMI Panel")
        return False
    pr_support = dpcd.PanelReplayCapsSupported(target_id)
    if panel_type == display_utility.VbtPanelType.LFP_DP:
        edp_dpcd_rev = dpcd.get_edp_revision(target_id)
        if edp_dpcd_rev is None or edp_dpcd_rev == dpcd.EdpDpcdRevision.EDP_UNKNOWN:
            logging.error("\tFailed to get eDP DPCD revision")
            return False
        if edp_dpcd_rev < dpcd.EdpDpcdRevision.EDP_DPCD_1_5:
            logging.error(f"Expected panel EDP revision = 1.5 Actual = {edp_dpcd_rev.name}")
            return False
        # Check for DPCD 0x2Eh (ALPM Caps) for PR support
        alpm_caps = dpcd.get(target_id, dpcd.Offsets.ALPM_CAP)
        # BIT6 - MSA_TIMING_PAR_IGNORED should be set.
        msa_timing = dpcd.get(target_id, dpcd.Offsets.DOWN_STREAM_PORT_COUNT)
        # Adaptive Sync SDP support is mandatory for EDP PR
        as_sdp_caps = dpcd.get(target_id, dpcd.Offsets.ADAPTIVE_SYNC_CAPABILITY)
        if alpm_caps and pr_support.panel_replay_support and msa_timing.msa_timing_par_ignored and \
                as_sdp_caps.adaptive_sync_sdp_supported and as_sdp_caps.as_sdp_first_half_line:
            return True
        return False
    # For External DP
    return pr_support.panel_replay_support == 1


##
# @brief        Exposed API to enable PR in regkey for external panel
# @param[in]    gfx_index string, gfx_0, gfx_1
# @return       True if given pr is enabled, False otherwise ,None if expected value is already present
def enable_for_efp(gfx_index):
    # todo - Need to remove this check after PR is enabled by default in driver INF for external displays
    display_pc = registry.DisplayPcFeatureControl(gfx_index)
    display_pc.DisableDpPanelReplay = 0
    status = display_pc.update(gfx_index)
    if status is False:
        logging.error("\tFailed to update DisplayPcFeatureControl Registry")
        return False
    logging.info("\tSuccessfully enabled Panel Replay in Regkey")
    return status


##
# @brief        Exposed API to disable PR in regkey for external panel
# @param[in]    gfx_index string, gfx_0, gfx_1
# @return       True if given pr is enabled, False otherwise, None if expected value is already present
def disable_for_efp(gfx_index):
    # todo - Need to remove this check after DP PR enabled by default in driver INF for external displays
    display_pc = registry.DisplayPcFeatureControl(gfx_index)
    display_pc.DisableDpPanelReplay = 1
    status = display_pc.update(gfx_index)
    if status is False:
        logging.error("\tFailed to update DisplayPcFeatureControl Registry")
        return False
    logging.info("\tSuccessfully disabled Panel Replay in Regkey")
    return True


##
# @brief        Exposed API to check if given PR is enabled in driver or not
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if enabled, False otherwise
def is_enabled_in_driver(adapter, panel):
    pr_ctl = MMIORegister.read(
        'TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    if panel.is_lfp:
        # When PR is Enabled (TRANS_DP2_CTL) and
        # ALPM is Disabled, then PR will operate in DP mode (i.e. the main link will not be turned off)
        # ALPM is Enabled, then PR will operate in eDP mode (i.e. the main link will be turned off when idle)
        alpm_ctl = MMIORegister.read(
            'ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        return (pr_ctl.pr_enable and alpm_ctl.alpm_enable and alpm_ctl.alpm_aux_less_enable) == 1
    return pr_ctl.pr_enable == 1


##
# @brief        Exposed API to verify PR
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if enabled, False otherwise
def verify(adapter, panel):
    status = True
    cff_ctl = None
    sff_ctl = None
    logging.info(f"STEP: verifying Panel replay on {panel.port}")
    pr_status = dpcd.SinkPanelReplayEnableAndConfiguration(panel.target_id)
    if not pr_status.panel_replay_enable_in_sink:
        logging.error("PR is not enabled in sink dpcd")
        gdhm.report_driver_bug_pc(f"[Panel_Replay] Panel Replay not enabled in {panel.port} dpcd")
        return False
    logging.info("PR enabled in sink DPCD")
    # SU support in panel will be enabled by driver only on GEN14+ platforms
    if adapter.name not in common.PRE_GEN_14_PLATFORMS:
        pr_caps = dpcd.PanelReplayCapsSupported(panel.target_id)
        if pr_caps.selective_update_support and (pr_status.selective_update_enable == 0):
            logging.error("selective update is not enabled in sink dpcd")
            gdhm.report_driver_bug_pc(f"[Panel_Replay] Panel Replay not enabled in {panel.port} dpcd")
            return False
        logging.info("Selective update enabled in sink DPCD")
    if panel.is_lfp is False:
        if adapter.name in common.PRE_GEN_16_PLATFORMS:
            srd_status = MMIORegister.read(
                'SRD_STATUS_REGISTER', 'SRD_STATUS_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
            if srd_status.srd_state != 0x7:
                logging.error(f"SRD entry with link-on is not enabled with Panel Replay on {panel.port}")
                gdhm.report_driver_bug_pc(f"[Panel_Replay] SRD entry with Link-on not enable on {panel.port}")
                return False
            logging.info("SRD entry with LINK-ON enabled")
        else:
            psr2_status = MMIORegister.read("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder,
                                                    adapter.name, gfx_index=adapter.gfx_index)
            logging.info(f"PR state = {psr2_status.psr2_pr_state}")
            if psr2_status.link_status != 0x1:
                logging.error(f"PR entry with link-on is not enabled with Panel Replay on {panel.port}")
                gdhm.report_driver_bug_pc(f"[Panel_Replay] PR entry with Link-on not enable on {panel.port}")
                return False
            logging.info("DP PR with LINK-ON enabled")
        man_trk = MMIORegister.read(
            'PSR2_MAN_TRK_CTL_REGISTER', 'PSR2_MAN_TRK_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        pr_support_dpcd_data = dpcd.PanelReplayCapsSupported(panel.target_id)
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
            sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)

        # For Gen13+ platforms, driver will enable disable manual tracking based on pipe scalar enable and SU support in DPCD 0xB0h
        # Following code chunk will verify the same
        if adapter.name not in common.PRE_GEN_13_PLATFORMS:
            if pr_support_dpcd_data.selective_update_support and man_trk.sf_partial_frame_enable == 0:
                logging.error(f"Manual tracking not enabled with SU support on {panel.port}")
                gdhm.report_driver_bug_pc(f"[Panel_Replay] Manual tracking not enabled with SU support on {panel.port}")
                return False
            if not pr_support_dpcd_data.selective_update_support and man_trk.sf_partial_frame_enable != 0:
                logging.error(f"Manual tracking is enabled without SU support {panel.port}")
                gdhm.report_driver_bug_pc(f"[Panel_Replay] Manual tracking enabled without SU support on {panel.port}")
                return False

        if adapter.name in common.GEN_13_PLATFORMS:
            su_mode_status , actual_su_mode = sfsu.verify_su_mode(adapter.name, man_trk, cff_ctl, sff_ctl, [sfsu.SuType.SU_NONE])
            if not su_mode_status:
                gdhm.report_driver_bug_pc(f"[PowerCons][Panel_Replay] Unexpected SU mode programming for Panel Replay")
                logging.error(f"Unexpected SU mode programming for Panel replay. Actual SU mode : {sfsu.SuType(actual_su_mode).name}")
                return False
            logging.info(f"PASS : Driver did not enable Manual tracking/CFF/SFF for Panel replay")

        logging.info(f"PASS: PR Verification on {panel.port}")
    else:
        video_dip_ctl = MMIORegister.read('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder, adapter.name,
                                          gfx_index=adapter.gfx_index)
        if video_dip_ctl.adaptive_sync_sdp_enable == 0x0:
            logging.error(f'AS SDP is disabled in driver on {panel.port}')
            gdhm.report_driver_bug_pc(f"AS SDP not enabled in driver on EDP_{panel.port}")
            return False
        status &= verify_aux_less_alpm(panel, adapter)
    return status


##
# @brief        Exposed API to verify PR timing support
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if enabled, False otherwise
def verify_pr_timing_support(adapter, panel):
    status = True
    vblank_reg = MMIORegister.read(
        'TRANS_VBLANK_REGISTER', 'TRANS_VBLANK_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    v_total = MMIORegister.read(
        'TRANS_VTOTAL_REGISTER', 'TRANS_VTOTAL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    alpm_ctl = MMIORegister.read(
        'ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    psr2_ctl = MMIORegister.read(
        'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    vsync = MMIORegister.read(
        'TRANS_VSYNC_REGISTER', 'TRANS_VSYNC_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    vrr_vmax = MMIORegister.read('TRANS_VRR_VMAX_REGISTER', 'TRANS_VRR_VMAX_' + panel.transcoder, adapter.name,
                                 gfx_index=adapter.gfx_index)

    context_latency = vblank_reg.vertical_blank_start - v_total.vertical_active
    if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
        vblank_size = v_total.vertical_total - vblank_reg.vertical_blank_start
        sdp_pos = v_total.vertical_total - vsync.vertical_sync_start
    else:
        vblank_size = vrr_vmax.vrr_vmax - vblank_reg.vertical_blank_start
        sdp_pos = vrr_vmax.vrr_vmax - vsync.vertical_sync_start
    if alpm_ctl.alpm_aux_less_enable:
        wake_time = alpm_ctl.aux_less_wake_time
    else:
        wake_time = psr2_ctl.io_buffer_wake
    min_sleep_time = alpm_ctl.alpm_entry_check

    adaptive_sync_capability = dpcd.AdaptiveSyncCapability(panel.target_id)  # address 0x2214
    sdp_one_line_earlier = dpcd.AdaptiveSyncSdpTransmissionTimingConfig(panel.target_id)  # address 0x11B
    if adaptive_sync_capability.as_sdp_first_half_line and sdp_one_line_earlier.as_sdp_one_line_earlier_enable:
        sdp_pos = sdp_pos + 1
    # (Set Context Latency + Guardband ) > (T1 Position + WakeTime) -
    # make sure HW have enough time to wake before T1 position and transmit AS SDP @ T1(AS SDP)
    logging.debug(f"Vblank size = {vblank_size} context latency = {context_latency} sdp_pos = {sdp_pos} "
                  f"wake_time = {wake_time} min sleep time = {min_sleep_time}")
    # Vblank lines > ( T1 postion + Waketime + MinSleep lines)
    # Ensure that HW sleep minimum amount of time (5us) before driver wake the link & transmit the AS SDP
    if vblank_size < (sdp_pos + wake_time):
        logging.error("sleep time check for AS SDP failed")
        status = None
    if status is None and is_enabled_in_driver(adapter, panel):
        logging.error("PR enabled in driver with timing mismatch")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]EDP PR enabled for timing not supported panel {panel.port}")
        return False
    return status


##
# @brief        Exposed API to verify Aux less ALPM programming
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if enabled, False otherwise
def verify_aux_less_alpm(panel, adapter):
    status = True
    alpm_ctl = MMIORegister.read(
        'ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    port_alpm_ctl = MMIORegister.read(
        'PORT_ALPM_CTL_REGISTER', 'PORT_ALPM_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder, adapter.name,
                                gfx_index=adapter.gfx_index)
    if alpm_ctl.alpm_enable == 0:
        logging.error(f"ALPM is not enabled on EDP {panel.port}")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]EDP Alpm disabled on {panel.port}")
        status = False
    if alpm_ctl.alpm_aux_less_enable == 0:
        logging.error(f"Aux less ALPM is not enabled on {panel.port}")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]EDP Aux less Alpm disabled on {panel.port}")
        status = False
    if alpm_ctl.alpm_aux_less_enable != port_alpm_ctl.alpm_aux_less_enable:
        gdhm.report_driver_bug_pc(f"[Panel_Replay]EDP PORT Aux less ALPM value not matching with ALPM CTL register val")
        status = False
    if alpm_ctl.aux_less_sleep_hold_time != 0x0:
        logging.error(f"Aux less sleep hold time not programmed to 50 symbols on {panel.port}")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]Aux less sleep hold time not programmed to 50 symbols on {panel.port}")
        status = False

    # ALPM Entry Check = 2 + CEILING( 5us /t line )  .  5 us = minimum EDP Main link sleep time
    line_time_micro_sec = math.ceil(
        (h_total.horizontal_total + 1) // (panel.native_mode.pixelClock_Hz // (1000 * 1000)))
    logging.info(f"panel line time = {line_time_micro_sec}")
    alpm_entry_val = 2 + math.ceil(5 / line_time_micro_sec)
    if alpm_ctl.alpm_entry_check != alpm_entry_val:
        logging.error(f"Aux less entry check val expected = {alpm_entry_val} Actual = {alpm_ctl.alpm_entry_check} "
                      f"on {panel.port}")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]Invalid ALPM entry value programmed on {panel.port}")
        status = False

    link_rate_mbs = int(dpcd.get_link_rate(panel.target_id, True) * 1000)
    logging.info(f"panel link rate = {link_rate_mbs} mbps")
    # AUX-Less WakeTime = CEIL( ((PHY P2 to P0) + tLFPS_Period Max + tSilence Max + tPHY Establishment + tCDS) / tline)
    #
    # where:
    # C10_PHY_P2_TO_P0_NS 12000
    # The tLFPS_Period, Max term is 800ns
    # The tSilence, Max term is 180ns
    # The tPHY Establishment (a.k.a. t1) term is 50us
    # The tCDS term is 1 or 2 times t2
    #        t2 = Number ML_PHY_LOCK patterns * tML_PHY_LOCK
    #        Number ML_PHY_LOCK patterns = (7 + CEILING(6.5us / tML_PHY_LOCK) + 1)
    #        tML_PHY_LOCK = TPS4 Length * ( 10 / (Link Rate in MHz) )
    #        TPS4 Length = 252 Symbols
    # todo - Above formula to be used to calculate wake time if the value not present in AUX_LESS_WAKE_TIME dictionary
    wake_time = int(AUX_LESS_WAKE_TIME[link_rate_mbs] / line_time_micro_sec)
    if alpm_ctl.aux_less_wake_time != wake_time:
        logging.warning(f"AuxLess wake time expected= {wake_time} Actual= {alpm_ctl.aux_less_wake_time} on {panel.port}")
    pr_alpm_ctl = MMIORegister.read('PR_ALPM_CTL_REGISTER', 'PR_ALPM_CTL_' + panel.transcoder, adapter.name,
                                    gfx_index=adapter.gfx_index)
    if pr_alpm_ctl.rfb_update_control != 0x0:  # HW controls the RFB update in AS SDP DB0[3]
        logging.error(f"RFB update control bit is not set in AS SDP on {panel.port}")
        gdhm.report_driver_bug_pc(f"[Panel_Replay]EDP RFB update control bit is not set on {panel.port}")
        status = False
    logging.info("Aux less ALPM programming verification successful")
    return status


##
# @brief        Exposed API to verify Pr Hw entry & exit
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file etl_file path
# @param[in]    method APP/Video
# @return       status Boolean, True, if disabled, False otherwise
def verify_pr_hw_state(adapter, panel, etl_file, method='APP'):
    if panel.is_lfp and panel.pipe not in ['A', 'B']:
        logging.warning(f"PR is not supported in Pipe-{panel.pipe}")
        return True

    entry_count = 0
    pr_disable = False
    srd_link_on = False
    etl_parser.generate_report(etl_file)
    srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)
    psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
    pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)

    # External DP Panle Replay -> PR main link should be always ON
    # EDP panel Replay -> PR main link should turn off and PSR entry should happen
    pr_data = etl_parser.get_mmio_data(pr_ctl.offset)
    if method in ['GAME']:
        if pr_data is None:
            logging.error("MMIO data not found for TRANS_DP2_CTL_REGISTER")
            gdhm.report_driver_bug_pc("TRANS_DP2_CTL_REGISTER mmio data not found in etl")
            return False
        for pr_val in pr_data:
            pr_ctl.asUint = pr_val.Data
            if pr_ctl.pr_enable == 0:
                logging.info("PR is disabled in driver during Game")
                pr_disable = True
                break
        if pr_disable is False:
            logging.error("PR not disabled during Game workload")
            gdhm.report_driver_bug_pc(f"PR not disabled during Game workload")
            return False
    if panel.is_lfp is False:
        if adapter.name in common.PRE_GEN_16_PLATFORMS:
            srd_data = etl_parser.get_mmio_data(srd_status.offset)
            if srd_data is None:
                logging.error("MMIO data not found for SRD_STATUS register")
                return False
            for data in srd_data:
                srd_status.asUint = data.Data
                # Link should be always on with PR external display
                if srd_status.srd_state == 0x2:
                    entry_count += 1
                if srd_status.srd_state == 0x7:
                    srd_link_on = True
        else:
            psr2_data = etl_parser.get_mmio_data(psr2_status.offset)
            for data in psr2_data:
                psr2_status.asUint = data.Data
                # PR with link on
                if  psr2_status.link_status == 0x1:
                    srd_link_on = True
        if entry_count == 0:
            logging.info(f"\tPASS: PR Entry Count on external display = {entry_count}")
        else:
            logging.error(f"\tFAIL: PR Entry Count on external display. Expected = 0 Actual = {entry_count}")
            gdhm.report_driver_bug_pc("[Powercons][PR]PR Entry Happened on External display")
            return False
        if srd_link_on:
            logging.info(f"PR with Link-on is enabled on {panel.port}")
            return True
        else:
            logging.error(f"\tFAIL: PR with Link ON not enabled")
            gdhm.report_driver_bug_pc("[Powercons][PR]PR Link-On mode not enabled on External display")
            return False
    # for LFP panel
    psr2_data = etl_parser.get_mmio_data(psr2_status.offset)
    if psr2_data is None:
        logging.error("MMIO data not found for PSR2_STATUS register")
        return False
    for data in psr2_data:
        psr2_status.asUint = data.Data
        # PR entry with link off
        if psr2_status.psr2_pr_state == 0x2 and psr2_status.link_status == 0x0:
            entry_count += 1

    if method == 'APP':
        if entry_count > 0:
            logging.info(f"\tPASS: PR Entry Count on Internal display = {entry_count}")
            return True
        logging.error(f"\tFAIL: PR Entry Count on internal display. Expected = non-zero Actual = {entry_count}")
        gdhm.report_driver_bug_pc("[Powercons][PR]PR Entry not Happened")
    # Todo - Need to check PR entry only during max duration flips. Sometimes there is Zero duration flip in between
    #  during workload due to this PR is getting enabled and PR entry happening.
    # else:
    #     if entry_count == 0:
    #         logging.info(f"\tPASS: PR Entry Count on internal display = {entry_count}")
    #         return True
    #     logging.error(f"\tFAIL: PR Entry Count on internal display . Expected = 0 Actual = {entry_count}")
    #     gdhm.report_driver_bug_pc("[Powercons][PR]PR Entry Happened")
    return True


##
# @brief        Exposed API to verify Pr disable sequence using etl
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    h_total htotal value
# @param[in]    v_total vtotal value
# @return       status Boolean, True, if successful, False otherwise
def verify_pr_disable_sequence(adapter, panel, h_total, v_total):
    pr_disable_in_sink = False
    as_sdp = False
    pr_disable_time = None
    plane_disable_time = None

    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe,
                                          adapter.name)
    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)
    psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
    srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)

    pr_val = etl_parser.get_mmio_data(pr_ctl.offset, is_write=True)
    psr2_status_val = etl_parser.get_mmio_data(psr2_status.offset)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset, is_write=True)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset, is_write=True)
    srd_status_data = etl_parser.get_mmio_data(srd_status.offset)

    if (pr_val is None) or (psr2_status_val is None):
        logging.error(f"PR registers data not found in etl")
        gdhm.report_driver_bug_pc("[PowerCons][PR] PR registers data not found in etl")
        return False
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] VIDEO_DIP_CTL_{panel.transcoder} data not found in etl")
        return False
    if plane_data is None:
        logging.error(f"PLANE_CTL_{panel.pipe} data not found")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] PLANE_CTL_{panel.pipe} data not found in etl")
        return False
    if (panel.is_lfp is False) and (srd_status_data is None):
        logging.error(f"SRD_CTL_{panel.pipe} data not found")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] SRD_CTL_{panel.transcoder} data not found in etl")
        return False

    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    pr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PANEL_REPLAY_ENABLE_AND_CONFIGURATION, channel=aux)
    if pr_conf is None:
        logging.error("DPCD 0x1B0H data not found")
        gdhm.report_driver_bug_pc("[PowerCons][PR] DPCD 0x1B0H data not found")
        return False
    pr_configuration = dpcd.SinkPanelReplayEnableAndConfiguration(panel.target_id)
    for dpcd_data in pr_conf:
        if not dpcd_data.IsWrite:
            continue
        pr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if pr_configuration.panel_replay_enable_in_sink == 0:
            pr_disable_in_sink = True
            break
    if pr_disable_in_sink is False:
        logging.error("driver did not disable psr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PR] Driver did not disable PR in sink")
        return False
    logging.info("Driver disabled PR in sink DPCD (0x1B0h)")
    if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
        vertical_total = v_total.vertical_total
    else:
        vertical_total = v_total.vrr_vmax
    rr = round(
        float(panel.native_mode.pixelClock_Hz) / (
                (h_total.horizontal_total + 1) * (vertical_total + 1)), 3)
    logging.debug(f"Panel Refresh Rate = {rr}")
    for val in pr_val:
        pr_ctl.asUint = val.Data
        if pr_ctl.pr_enable == 0:
            logging.info(f"PR disabled at {val.TimeStamp}ms")
            pr_disable_time = val.TimeStamp
            break
    if pr_disable_time is None:
        logging.error("PR is not disabled in driver")
        return False
    for plane in plane_data:
        plane_ctl.asUint = plane.Data
        if plane_ctl.plane_enable:
            continue
        plane_disable_time = plane.TimeStamp
        logging.info(f"Plane{panel.pipe} is disabled at {plane.TimeStamp}")
        break
    if plane_disable_time is None:
        logging.error(f"Plane{panel.pipe} is not disabled during driver disable")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] Plane is not disabled during driver disable")
        return False
    if pr_disable_time > plane_disable_time:
        logging.error(f"PR disabled after plane disable")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] PR disabled after plane disable")
        return False
    if panel.is_lfp:
        video_dip_ctl.asUint = dip_ctl[-1].Data
        if video_dip_ctl.adaptive_sync_sdp_enable == 0x0:
            as_sdp = True
        logging.info(f"Adaptive sync sdp enabled in driver")
        if as_sdp is False:
            logging.error(f"Adaptive sync sdp not disabled in driver")
            gdhm.report_driver_bug_pc(f"[PowerCons][PR] Adaptive sync sdp not disabled in driver")
            return False

    # verify PR Inactive state in HW
    # Max wait time for PR IDLE/Inactive state = 2 full frame
    # https://gfxspecs.intel.com/Predator/Home/Index/68920
    time_out = round((1000 * 2) / rr, 4)  # milli secs
    idle_state = False
    for ctl_val in pr_val:
        pr_ctl.asUint = ctl_val.Data
        if pr_ctl.pr_enable == 1:
            continue
        if panel.is_lfp:
            for status_val in psr2_status_val:
                psr2_status.asUint = status_val.Data
                # Make sure that the current PSR2 Status Register read is after PR Disable
                if status_val.TimeStamp < ctl_val.TimeStamp:
                    continue
                if psr2_status.psr2_pr_state == 0:
                    idle_state = True
                    logging.info(f"PR returned to Inactive state at {status_val.TimeStamp} ms")
                    if status_val.TimeStamp > (ctl_val.TimeStamp + time_out):
                        logging.error(f"PR not returned to Inactive state before {time_out} ms")
                        gdhm.report_driver_bug_pc("[PowerCons][PR] PR not returned to Inactive with in 2 frames")
                        return False
        else:
            for status_val in srd_status_data:
                srd_status.asUint = status_val.Data
                # Make sure that the current PSR2 Status Register read is after PR Disable
                if status_val.TimeStamp < ctl_val.TimeStamp:
                    continue
                if srd_status.srd_state == 0:
                    logging.info(f"PR returned to Inactive state at {status_val.TimeStamp}")
                    idle_state = True
                    if status_val.TimeStamp > (ctl_val.TimeStamp + time_out):
                        logging.error(f"PR not returned to Inactive state before {time_out} ms")
                        gdhm.report_driver_bug_pc("[PowerCons][PR] PR not returned to Inactive with in 2 frames")
                        return False
    if idle_state:
        logging.info(f"PR returned to Inactive state with in 2 frames")
        return True
    logging.error("PR did not return to Inactive state")
    gdhm.report_driver_bug_pc("[PowerCons][PR] PR not returned to Inactive with in 2 frames")
    return False


##
# @brief        Exposed API to verify Pr enable sequence using etl
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if successful, False otherwise
def verify_pr_enable_sequence(adapter, panel):
    pr_enable_in_sink = False
    alpm_enable = False
    as_sdp = False
    pr_enable_time = None
    plane_enable_time = None
    pr_dpcd_enable_time = None
    lt_start = 0

    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe,
                                          adapter.name)
    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)

    pr_val = etl_parser.get_mmio_data(pr_ctl.offset, is_write=True)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset, is_write=True)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset, is_write=True)

    if pr_val is None:
        logging.error(f"PR registers data not found in etl")
        gdhm.report_driver_bug_pc("[PowerCons][PR] PR registers data not found in etl")
        return False
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] VIDEO_DIP_CTL_{panel.transcoder} data not found in etl")
        return False
    if plane_data is None:
        logging.error(f"PLANE_CTL_{panel.pipe} data not found")
        gdhm.report_driver_bug_pc(f"[PowerCons][PR] PLANE_CTL_{panel.pipe} data not found in etl")
        return False

    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    link_training_start = etl_parser.get_dpcd_data(0x102, channel=aux, is_write=True)
    if link_training_start is None:
        logging.error("DPCD 0x102 data not found in etl")
        gdhm.report_driver_bug_pc("[PowerCons][PR] DPCD 0x102H data not found in etl")
        return False
    for val in link_training_start:
        if val.Data:
            lt_start = val.TimeStamp
            logging.info(f"Link training started at {lt_start} ms")
            break
    pr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PANEL_REPLAY_ENABLE_AND_CONFIGURATION, channel=aux, is_write=True)
    if pr_conf is None:
        logging.error("DPCD 0x1B0H data not found in etl")
        gdhm.report_driver_bug_pc("[PowerCons][PR] DPCD 0x1B0H data not found in etl")
        return False
    pr_configuration = dpcd.SinkPanelReplayEnableAndConfiguration()
    for dpcd_data in pr_conf:
        if not dpcd_data.IsWrite:
            continue
        pr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if pr_configuration.panel_replay_enable_in_sink == 1:
            pr_enable_in_sink = True
            pr_dpcd_enable_time = dpcd_data.TimeStamp
            logging.info(f"PR enabled in DPCD at {pr_dpcd_enable_time} ms")
            break
    if pr_enable_in_sink is False:
        logging.error("driver did not enable pr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PR] Driver did not enable PR in sink")
        return False
    logging.info("Driver enabled PR in sink DPCD (0x1B0h)")
    if panel.is_lfp:
        if pr_dpcd_enable_time > lt_start:
            logging.error(f"PR not enabled before Link training start")
            gdhm.report_driver_bug_pc("[PowerCons][PR] PR not enabled before Link training start")
            return False
        logging.info("PR enabled before link training start")
    for val in pr_val:
        pr_ctl.asUint = val.Data
        if pr_ctl.pr_enable == 0:
            logging.info(f"PR enabled in mmio at {val.TimeStamp} ms")
            pr_enable_time = val.TimeStamp
            break
    if pr_enable_time is None:
        logging.error("PR is not enabled in driver")
        return False
    for plane in plane_data:
        plane_ctl.asUint = plane.Data
        if plane_ctl.plane_enable:
            continue
        plane_enable_time = plane.TimeStamp
        logging.info(f"Plane{panel.pipe} is enabled at {plane.TimeStamp} ms")
        break
    if plane_enable_time is None:
        logging.error(f"Plane{panel.pipe} is not enabled during driver enable")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Plane is not enabled during driver enable")
        return False
    if pr_enable_time < plane_enable_time:
        logging.error("PR enabled before plane enable")
        gdhm.report_driver_bug_pc("[PowerCons][PR] PR enabled before plane enable")
        return False
    if panel.is_lfp:
        video_dip_ctl.asUint = dip_ctl[-1].Data
        if video_dip_ctl.adaptive_sync_sdp_enable == 0x1:
            as_sdp = True
        logging.info("Adaptive sync sdp enabled in driver")
        if as_sdp is False:
            logging.error("Adaptive sync sdp not enabled in driver")
            gdhm.report_driver_bug_pc("[PowerCons][PR] Adaptive sync sdp not enabled in driver")
            return False
        if panel.pr_caps.aux_less_alpm:
            alpm_ctl = MMIORegister.get_instance('ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name)
            alpm_ctl_data = etl_parser.get_mmio_data(alpm_ctl.offset)
            for alpm_val in alpm_ctl_data:
                alpm_ctl.asUint = alpm_val.Data
                if alpm_ctl.alpm_enable and alpm_ctl.alpm_aux_less_enable:
                    alpm_enable = True
                    logging.info(f"Aux less ALPM enabled at {alpm_val.TimeStamp} ms")
                    break
            if alpm_enable is False:
                logging.error("Aux less ALPM not enabled in driver")
                gdhm.report_driver_bug_pc("[PowerCons][PR] Aux less ALPM not enabled in driver")
                return False
    return True
