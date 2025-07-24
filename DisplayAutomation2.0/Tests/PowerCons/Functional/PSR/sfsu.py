#######################################################################################################################
# @file         sfsu.py
# @brief        Contains sfsu verification APIs
#
# @author     Chandrakanth Reddy
#######################################################################################################################

import logging
import math
import os
import subprocess
import time
from enum import IntEnum

from Libs.Core import etl_parser
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Feature.powercons import registry
from Libs.Feature.vdsc.dsc_verifier import verify_dsc_programming
from Tests.Planes.Common import planes_verification
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dpcd
from registers.mmioregister import MMIORegister

TOTAL_SCAN_LINES_PER_BLOCK_GEN12 = 4
TOTAL_SCAN_LINES_PER_BLOCK_GEN13 = 1
TOTAL_SCAN_LINES_PER_BLOCK = 0
TEST_DURATION = 20
DSC_SLICE_HEIGHT = 0
SCAN_LINE_ALIGNMENT_4 = False
__PSR_UTIL_PATH = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "psrutil.exe")


##
# @brief        Enum class for Selective Update Type
class SuType(IntEnum):
    SU_NONE = 0
    SU_PARTIAL_FRAME_UPDATE = 1
    SU_CONTINUOUS_UPDATE = 2
    SU_SINGLE_FULL_FRAME_UPDATE = 3


##
# @brief        Enum class for Event type
class EventType(IntEnum):
    EVENT_IDLE = 0
    CURSOR_MOVE = 1
    CURSOR_CHANGE = 2
    KEYPRESS = 3
    BLC_DPST = 4
    DEFAULT = 5


##
# @brief        Helper Function to update block size
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       None
def __update_block_size(adapter, panel):
    global TOTAL_SCAN_LINES_PER_BLOCK
    global SCAN_LINE_ALIGNMENT_4

    edp_rev = dpcd.get_edp_revision(panel.target_id)
    psr_capability = dpcd.PsrCapability(panel.target_id)
    psr_granularity = dpcd.PsrGranularity(panel.target_id)
    if adapter.name in common.GEN_12_PLATFORMS:
        TOTAL_SCAN_LINES_PER_BLOCK = TOTAL_SCAN_LINES_PER_BLOCK_GEN12
        if panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4_B:
            if panel.psr_caps.su_granularity_supported and panel.psr_caps.su_y_granularity:
                TOTAL_SCAN_LINES_PER_BLOCK = max(TOTAL_SCAN_LINES_PER_BLOCK_GEN12, panel.psr_caps.su_y_granularity)
    else:
        # Gen13+ Platforms
        TOTAL_SCAN_LINES_PER_BLOCK = TOTAL_SCAN_LINES_PER_BLOCK_GEN13
        # Check VDSC programming & support
        __verify_vdsc(adapter, panel)
        if panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4_B:
            if panel.psr_caps.su_granularity_supported and panel.psr_caps.su_y_granularity:
                TOTAL_SCAN_LINES_PER_BLOCK = max(TOTAL_SCAN_LINES_PER_BLOCK_GEN13, panel.psr_caps.su_y_granularity)
        if panel.pr_caps.is_pr_supported and (panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_5):
            if panel.pr_caps.pr_su_granularity_needed and panel.pr_caps.su_y_granularity:
                TOTAL_SCAN_LINES_PER_BLOCK = max(TOTAL_SCAN_LINES_PER_BLOCK_GEN13, panel.pr_caps.su_y_granularity)

        # HSD-16012753785- PSR2 scan line granularity (TCON issue)WA to use 4 scan lines in case DPCD returns 0
        if (panel.psr_caps.is_psr2_supported and (
                (panel.edp_caps.edp_revision <= dpcd.EdpDpcdRevision.EDP_DPCD_1_4_A) or (
                panel.psr_caps.su_granularity_supported is False))) or (
                panel.pr_caps.is_pr_supported and panel.pr_caps.pr_su_granularity_needed is False):
            SCAN_LINE_ALIGNMENT_4 = True


##
# @brief        Helper Function to calculate block size
# @param[in]    adapter Adapter
# @param[in]    rect_data rectangle data
# @param[in]    bottom boolean
# @return       None
def __calculate_block(adapter, rect_data, bottom=False):
    if adapter.name not in common.GEN_12_PLATFORMS + ['DG2']:
        if DSC_SLICE_HEIGHT != 0:
            if bottom:
                rect_data = math.ceil(rect_data / DSC_SLICE_HEIGHT) * DSC_SLICE_HEIGHT
            else:
                rect_data = (rect_data // DSC_SLICE_HEIGHT) * DSC_SLICE_HEIGHT
    if adapter.name in common.GEN_12_PLATFORMS + ['DG2']:
        remainder = rect_data % TOTAL_SCAN_LINES_PER_BLOCK
        rect_data = int((rect_data + (TOTAL_SCAN_LINES_PER_BLOCK - remainder)) // TOTAL_SCAN_LINES_PER_BLOCK)
        # End scan line should be multiple of 4 plus 1 for Gen12
        if adapter.name in common.GEN_12_PLATFORMS and remainder and bottom:
            rect_data += 1
    else:
        scan_line_cnt = TOTAL_SCAN_LINES_PER_BLOCK
        if SCAN_LINE_ALIGNMENT_4:
            # Align scan line to multiple of 4
            # HSD-16012753785- PSR2 scan line granularity (TCON issue)WA to use 4 scan lines in case DPCD returns 0
            scan_line_cnt = TOTAL_SCAN_LINES_PER_BLOCK_GEN12
        if bottom:
            rect_data = math.ceil(rect_data / scan_line_cnt) * scan_line_cnt
            # For GEN13+ - End scanline should be multiple of 4 minus 1 (i.e N-1)
            if adapter.name not in common.PRE_GEN_13_PLATFORMS:
                rect_data = rect_data - 1
        else:
            rect_data = math.floor(rect_data / scan_line_cnt) * scan_line_cnt
    return rect_data


##
# @brief        Helper Function to verify VDSC programming and update slice height
# @param[in]    adapter object
# @param[in]    panel object
# @return       None
def __verify_vdsc(adapter, panel):
    global DSC_SLICE_HEIGHT
    # In Gen13 we will program the SU region in terms of 1 scan line
    # PSR2 + VDSC is supported on ADL-P onwards
    if panel.vdsc_caps.is_vdsc_supported:
        edp_dss_ctl2 = MMIORegister.read('PIPE_DSS_CTL2_REGISTER', 'PIPE_DSS_CTL2_P' + panel.pipe,
                                         adapter.name, gfx_index=adapter.gfx_index)
        assert verify_dsc_programming(adapter.gfx_index, panel.port), "DSC verification failure"
        # Adjust the SU region to dsc slice height , if DSC is enabled
        if edp_dss_ctl2.left_branch_vdsc_enable:
            dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", 'PPS3_0_' + panel.pipe, adapter.name,
                                         gfx_index=adapter.gfx_index)
            logging.info(f"DSC slice height = {dsc_pps3.slice_height}")
            DSC_SLICE_HEIGHT = dsc_pps3.slice_height


##
# @brief        This Function is used to check psr with util app
# @param[in]    event_type enum to indicate the type of event
# @param[in]    edp_position
# @param[in]    duration number
# @return       enum SuType
def check_psr_with_util_app(event_type, edp_position, duration=20):
    cmd_line = "%s c:clock d:%s x:300 y:200" % (__PSR_UTIL_PATH, edp_position)
    if event_type == EventType.CURSOR_MOVE:
        cmd_line = "%s c:cursormove d:%s" % (__PSR_UTIL_PATH, edp_position)
    elif event_type == EventType.CURSOR_CHANGE:
        cmd_line = "%s c:cursorchange d:%s x:300 y:200 n:50" % (__PSR_UTIL_PATH, edp_position)
    elif event_type == EventType.KEYPRESS:
        cmd_line = "%s c:keypress d:%s t:%s" % (__PSR_UTIL_PATH, edp_position, duration)

    p_util = None
    if event_type != EventType.EVENT_IDLE:
        p_util = subprocess.Popen(cmd_line)

    time.sleep(3 + duration)  # Breather for the app which is just launched + event duration
    if event_type != EventType.EVENT_IDLE:
        p_util.terminate()


##
# @brief        Exposed API to verify Dirty Rect calculation
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    etl_file String, path to ETL file
# @param[in]    method verification method(video/cursor/app)
# @param[in]    feature enum, FFSU/SFSU
# @param[in]    dpst_enable bool, dpst_enable status
# @param[in]    is_basic [optional] , if False verify dirty rect calculation also
# @return       status Boolean, True if verification is successful, False otherwise
def verify_sfsu(adapter, panel, etl_file, method, feature, dpst_enable, is_basic=False):
    assert etl_file, "parameter etl_file is missing"
    assert panel
    assert adapter
    status = True
    async_flips_present = False
    cff_ctl = None
    pr_ctl = None

    if panel.pipe_joiner_tiled_caps.is_pipe_joiner_require:
        logging.info(f'Skipping dirty rectangle programming for PIPE Joiner display')
        return True

    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name)
    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)

    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    sf_plane_ctl = MMIORegister.get_instance("SEL_FETCH_PLANE_CTL_REGISTER", f"SEL_FETCH_PLANE_CTL_{plane_id}_{panel.pipe}",
                                             adapter.name)
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        pr_ctl = MMIORegister.get_instance("TRANS_DP2_CTL_REGISTER", f"TRANS_DP2_CTL_{panel.transcoder}", adapter.name)

    etl_parser.generate_report(etl_file)
    flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe)
    if flip_data is None:
        logging.error("\tFLIP data is empty")
        gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] Flip Data is Empty in ETL")
        return False
    logging.info("No.of flips :{}".format(len(flip_data)))
    logging.info("Verifying {0} status on {1} . May take few mins....".format(psr.UserRequestedFeature(feature).name,
                                                                               panel))
    gdhm_message = set()
    for flip in flip_data:
        for plane_info in flip.PlaneInfoList:
            if plane_info.Flags == '':
                continue
            if 'FlipImmediate' in plane_info.Flags:
                async_flips_present = True
                logging.debug("\tAsync flip received")
                if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                    # Wa_22018697067 - PSR2 will be disabled for Async flip on MTL
                    # PSR/PR will be disabled for ASYNC flips from LNL+ - https://hsdes.intel.com/appstore/article/#/14019644643
                    if __verify_psr_pr_disable_for_async_flips(feature, flip, psr2_ctl, pr_ctl) is False:
                        gdhm_message.add("PSR disable verification failed with ASYNC flips")
                        logging.error(f"{feature} verification failed with ASYNC flips during workload {method}")
                        status &= False
                else:
                    # For Pre-Gen14 platforms, PSR2 should switch to Continuous Full fetch for Async flips
                    if feature >= psr.UserRequestedFeature.PSR2_SFSU and __verify_cff_for_async_flips(adapter, flip, psr2_man_trk, cff_ctl) is False:
                        gdhm_message.add("[PowerCons][PSR_SFSU] CFFU was not enabled for Async flips")
                        status &= False

            for data in flip.MmioDataList:
                # Checking whether Manual tracking got enabled for all flips in PSR2_MAN_TRK_CTL
                if data.Offset == psr2_man_trk.offset and data.IsWrite:
                    psr2_man_trk.asUint = data.Data
                    # Check psr2_manual_tracking_enable bit only for Gen12 Platforms
                    if adapter.name in common.GEN_12_PLATFORMS and psr2_man_trk.psr2_manual_tracking_enable == 1:
                        logging.debug("\tPSR2_MAN_TRK_CTL_{0}: Manual Tracking Enabled= {1} on TimeStamp= {2}"
                                      .format(panel.transcoder, psr2_man_trk.psr2_manual_tracking_enable,
                                              data.TimeStamp))
                    # For Gen13+ psr2_man_trk Reg Bit fields got changed and psr2_manual_tracking_enable bit is removed
                    # and sf_partial_frame_enable bit is used to check Manual Tracking enable status
                    elif psr2_man_trk.sf_partial_frame_enable == 1:
                        logging.debug("\tPSR2_MAN_TRK_CTL_{0}: partial update Enabled= {1} on TimeStamp= {2}"
                                      .format(panel.transcoder, psr2_man_trk.sf_partial_frame_enable,
                                              data.TimeStamp))
                    # In Gen15, for Panel Replay cases, driver will enable/disable manual tracking based on SU support in DPCD 0xB0h and Pipe scalar enable
                    # Skipping the manual tracking check for Panel Replay in Gen15 as the same is being covered in pr.py 
                    elif psr2_man_trk.sf_partial_frame_enable == 0 and not (feature == psr.UserRequestedFeature.PANEL_REPLAY and adapter.name in common.GEN_15_PLATFORMS):
                        logging.error("FAIL : Manual tracking is Disabled at {}".format(data.TimeStamp))
                        gdhm_message.add("[PowerCons][PSR_SFSU] Manual Tracking disabled")
                        status &= False

    # Verify Selective fetch enable during workload
    # Selective Fetch should not get disabled during any workload
    # It should be enabled until the plane is enabled
    # @todo : To be enabled as part of https://jira.devtools.intel.com/browse/VSDI-40816
    # if panel.is_lfp and feature > psr.UserRequestedFeature.PSR_2:
    #     sel_fetch_data = etl_parser.get_mmio_data(sf_plane_ctl.offset)
    #     if sel_fetch_data is None:
    #         logging.warning("Selective Fetch Plane CTL register data is not present in the ETL")
    #     else:
    #         for sf_val in sel_fetch_data:
    #             sf_plane_ctl.asUint = sf_val.Data
    #             if sf_plane_ctl.selective_fetch_plane_enable == 1:
    #                 continue
    #             logging.error(f"Selective Fetch was disabled during workload {method} at {sf_val.TimeStamp}")
    #             gdhm.report_driver_bug_pc(f"[PowerCons][PSR_SFSU] Selective Fetch was disabled during workload {method}")
    #             return False
    #         logging.info(f"SUCCESS : Selective Fetch verification during workload {method}")

    if is_basic or (async_flips_present and feature == psr.UserRequestedFeature.PSR2_SFSU):
        if not status:
            for message in gdhm_message:
                gdhm.report_driver_bug_pc(message)
        logging.info("PASS : Successfully verified PSR2 Manual Tracking, Selective Fetch and Continuous Full Fetch")
        return status

    # update block size based on platform
    __update_block_size(adapter, panel)
    # verify dirty rectangle calculation
    # @todo - Disabled dirty rectangle verification due to a known bug : https://hsdes.intel.com/appstore/article/#/18024248787
    # JIRA to enable dirty rectangle verification : https://jira.devtools.intel.com/browse/VSDI-34125
    logging.info("Temporary WA : Skipping dirty rectangle verification until VSDI-34125 gets implemented")
    verify_cff(adapter, panel, flip_data, method)
    return status
    # vbi_data = etl_parser.get_vbi_data('PIPE_' + panel.pipe)
    # if vbi_data is None:
    #     logging.error("\tVBI data is empty")
    #     gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] VBI Data is Empty in ETL")
    #     return False
    # if __verify_dirty_rect(adapter, panel, method, feature, dpst_enable, sf_plane_ctl, psr2_man_trk, flip_data, vbi_data):
    #     return status
    # logging.error("Dirty Rectangle verification Failed")
    # return False


##
# @brief        Internal API to verify CFF
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    method verification method(video/cursor/app)
# @param[in]    flip_data list
# @return       status Boolean, True if verification is successful, False otherwise
def verify_cff(adapter, panel, flip_data, method='video'):
    status = True
    if adapter.name not in ['MTL'] and method not in ["VIDEO"]:
        return status

    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name)
    for flip in flip_data:
        for data in flip.MmioDataList:
            for flip_address in flip.FlipAddressList:
                if flip.PlaneCount >= 2:
                    if data.Offset == psr2_man_trk.offset and data.IsWrite:
                        psr2_man_trk.asUint = data.Data
                        # Check if CFF bit is set
                        if psr2_man_trk.sf_continuous_full_frame == 1:
                            logging.info(f"CFF is enabled for Address only flip at: {data.TimeStamp}")
                        # Check if CFF bit is cleared
                        elif flip_address.PlaneID == 0:
                            if psr2_man_trk.sf_continuous_full_frame == 0:
                                logging.info(f"PASS : CFF bit was cleared at {data.TimeStamp}")
                            else:
                                logging.error(f"FAIL: CFF bit was not cleared within the flip at {data.TimeStamp}")
                                status = False
    return status

##
# @brief        Internal API to verify Dirty Rect calculation
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    method verification method(video/cursor/app)
# @param[in]    feature enum, SFSU/FFSU
# @param[in]    dpst_enable bool, dpst_enable_status
# @param[in]    sf_plane_ctl  register instance
# @param[in]    psr2_man_trk register instance
# @param[in]    flip_data list
# @param[in]    vbi_data list
# @return       status Boolean, True if verification is successful, False otherwise
def __verify_dirty_rect(adapter, panel, method, feature, dpst_enable, sf_plane_ctl, psr2_man_trk, flip_data, vbi_data):
    assert adapter
    assert panel
    fail_count = 0
    status = True
    full_frame_count = 0
    last_vbi_time_stamp = 0
    sf_count = 0
    vbi_count = 0
    dpst_time_stamp = 0
    dpst_phase_in = False
    dpst_phase_in_time = 0
    dpst_phase_done_time = 0
    prev_data = None
    sel_fetch_status = None
    histogram_interrupt_enable = False
    repeat_count = True
    su_type = SuType.SU_NONE
    all_param = False

    # HSD-14014971492 - WA for PSR2 + MSO panel to program start region always 0
    wa_14014971492_status = False
    if adapter.name in common.PRE_GEN_14_PLATFORMS or (adapter.name in ['MTL'] and adapter.cpu_stepping == 0):
        wa_14014971492_status = True

    prev_dpst_phase_in_type = None
    v_total = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name)
    v_active = v_total.vertical_active + 1
    # Driver will not switch to full fetch during DPST phasing post Gen-15
    # Need to re-consider the below check as a part of the JIRA : https://jira.devtools.intel.com/browse/VSDI-34799
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        # Check PSR CLIENT EVENT for Phasing & Phase out
        # {"PipeId":"PIPE_A","Operation":"PSR_DPST_PHASE_EVENT","Field1":0,"Field2":0,"TimeStamp":122.9376}
        psr_dpst_data = etl_parser.get_psr_event_data(etl_parser.Events.PSR_DPST_PHASE_EVENT)
        if psr_dpst_data is None:
            logging.info("No DPST Data found in PSR Client event in the ETL")
        else:
            for client_event in psr_dpst_data:
                if client_event.PipeId != 'PIPE_' + panel.pipe:
                    continue

                if client_event.Field1:  # Field1 -> DpstPhaseAdjustmentInProgress
                    dpst_phase_in_time = client_event.TimeStamp
                    prev_dpst_phase_in_type = client_event.Operation
                    dpst_phase_done_time = 0
                    continue
                if client_event.Field1 == 0 and client_event.Operation == prev_dpst_phase_in_type:
                    dpst_phase_done_time = client_event.TimeStamp
                else:
                    continue

                if dpst_phase_in_time and dpst_phase_done_time:
                    if __verify_full_fetch_with_dpst_phasing(adapter, panel, dpst_phase_in_time, dpst_phase_done_time,
                                                                psr2_man_trk) is False:
                        return False
                    dpst_phase_in_time = dpst_phase_done_time = 0
                    prev_dpst_phase_in_type = None

    # Check whether driver is switching to Full Fetch during Cursor Event
    if feature == psr.UserRequestedFeature.PSR2_SFSU:
        cursor_status, full_frame_count = __verify_cursor_event(adapter, panel, psr2_man_trk, method)
        if cursor_status is False:
            logging.error("FAIL : Cursor status verification")
            gdhm.report_driver_bug_pc("[Powercons][PSR] Driver did not switch to Full Fetch during cursor events")
            return False
        logging.info("SUCCESS : Full fetch verification during Cursor Event")

    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)

    # Selective fetch is for single video plane only, otherwise Driver will switch to FF
    # Verify dirty rectangle calculation
    last_video_flip_data = None
    pos = 0
    for index, vbi in enumerate(vbi_data):
        if index > len(vbi_data) - 2:
            break
        pipe_id = ord(panel.pipe) - 65
        if vbi_count:
            vbi_count += 1

        man_trk = []
        cff_ctl_data = []
        sff_ctl_data = []
        for index in range(pos, len(flip_data)):
            # Cache every Video Flip Data for the comparison if the next flip is DWM Plane flip
            if last_video_flip_data is not None and flip_data[index].PlaneInfoList[0].LayerIndex == 0:
                flip_data[index] = last_video_flip_data

            if flip_data[index].TimeStamp > vbi.TimeStamp:
                break
            elif last_vbi_time_stamp < flip_data[index].TimeStamp < vbi.TimeStamp:
                # Need to be re-looked as a part of the JIRA : https://jira.devtools.intel.com/browse/VSDI-34799
                # Driver will not switch to full fetch during DPST phasing post Gen-15
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    # Update DPST timer val for every flip
                    dpst_time_stamp = __update_dpst_time_stamp(dpst_time_stamp, flip_data[index])
                    # For every 2 Secs from the start of flip
                    # driver will change the Manual tracking to FFFU and enable Histogram interrupts
                    if dpst_enable and dpst_time_stamp and method not in [
                        'CURSOR'] and sel_fetch_status and (repeat_count is False) \
                            and (int((flip_data[index].TimeStamp - dpst_time_stamp) // 1000) > 2) and (dpst_phase_in is False):
                        if su_type not in [SuType.SU_CONTINUOUS_UPDATE, SuType.SU_SINGLE_FULL_FRAME_UPDATE]:
                            logging.error(
                                f"Driver didn't switch to Full Fetch after 2 sec timeout. current Type = {SuType(su_type).name} and "
                                f"current time = {flip_data[index].TimeStamp} and prev time = {dpst_time_stamp}")
                            return False
                        if not histogram_interrupt_enable:
                            logging.error(
                                f"\tHistogram interrupt is not re-enabled after 2 sec. Current= {flip_data[index].TimeStamp}, prev= {dpst_time_stamp}")
                            return False

                if flip_data[index].PlaneInfoList[0].LayerIndex == 1:
                    last_video_flip_data = flip_data[index]

                for mmio_data in flip_data[index].MmioDataList:
                    if flip_data[index].IsAllParam:
                        all_param = True
                        # For AllParam Sync Flip , Selective Fetch for Plane will be enabled/disabled
                        # based on the restrictions
                        if mmio_data.IsWrite is True and mmio_data.Offset == sf_plane_ctl.offset:
                            sf_plane_ctl.asUint = mmio_data.Data
                            if sf_plane_ctl.selective_fetch_plane_enable == 0:
                                logging.error(f"Selective Fetch is Disabled at {mmio_data.TimeStamp}")
                                return False
                    if mmio_data.IsWrite and mmio_data.Offset == psr2_man_trk.offset:
                        man_trk.append(mmio_data)
                    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                        if mmio_data.Offset == cff_ctl.offset:
                            cff_ctl_data.append(mmio_data)
                        if mmio_data.Offset == sff_ctl.offset:
                            sff_ctl_data.append(mmio_data)
                if not man_trk:
                    logging.debug(f"No Entry found for PSR2_MAN_TRK during the flip at {flip_data[index].TimeStamp}")
                    pos += 1
                    continue
                status, full_frame_count, sf_count, fail_count = __verify_dirty_rect_calculation(adapter, panel,
                                                                                                 flip_data[index],
                                                                                                 v_active,
                                                                                                 psr2_man_trk,
                                                                                                 man_trk,
                                                                                                 cff_ctl_data,
                                                                                                 sff_ctl_data,
                                                                                                 full_frame_count,
                                                                                                 sf_count,
                                                                                                 fail_count, 
                                                                                                 wa_14014971492_status)
                pos += 1
        last_vbi_time_stamp = vbi.TimeStamp

    logging.info(f"Total no.of Selective fetch updates happened = {sf_count}")
    logging.info(f"Total no.of full frame updates happened = {full_frame_count}")

    # HSD - 16011135426 - OS is not giving dirty rectangle values correctly
    # With PSR2 + VDSC panel, most of the times OS is giving Dirt rect data with full frame values only
    # skipping this check for PSR2 + VDSC supported panel
    if (panel.vdsc_caps.is_vdsc_supported is False) and method in ['VIDEO',
                                                                   'VIDEO_CURSOR'] and \
            all_param is False and sf_count == 0:
        error_title = f"selective update not happened with {method}"
        logging.error(error_title)
        gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] " + error_title)
        return False
    if fail_count:
        logging.error("Total no.of Dirty Rectangle Failures:{}".format(fail_count))
        status = False
        gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] Dirty rectangle verification failed")
    return status


##
# @brief        Exposed API to get man_trk register instance (SU type for SFSU)
# @param[in]    adapter object
# @param[in]    panel object
# @return       su_type enum
def get_man_trk_status(adapter, panel):
    cff_ctl = None
    sff_ctl = None
    psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder, adapter.name)
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.read("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.read("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
    _, su_type = verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl)
    logging.info("\tCurrent SU Type:{}".format(SuType(su_type).name))
    return su_type


##
# @brief        Internal API to get Selective Update mode status
# @param[in]    adapter_name        Adapter/Platform name
# @param[in]    psr2_man_trk        Register instance
# @param[in]    cff_ctl             Register instance
# @param[in]    sff_ctl             Register instance
# @param[in]    requested_su_mode   Expected SU mode(SU/CFF/SFF)
# @return       verification_status True if SU mode verification is successful, False otherwise
#               actual_su_mode      Actual SU mode according to the respective registers
def verify_su_mode(adapter_name, psr2_man_trk=None, cff_ctl=None, sff_ctl=None, requested_su_mode=[]):
    verification_status = True
    actual_su_mode = SuType.SU_NONE
    if adapter_name in common.PRE_GEN_15_PLATFORMS and psr2_man_trk is None:
        logging.info('PSR2 Manual Track Register data is None')
        gdhm.report_driver_bug_pc("[PowerCons] [PSR_SFSU] PSR2 Manual Track Register data is None")
        return actual_su_mode, None

    if adapter_name in common.PRE_GEN_15_PLATFORMS:
        if psr2_man_trk.sf_partial_frame_enable:
            if psr2_man_trk.sf_continuous_full_frame:
                actual_su_mode = SuType.SU_CONTINUOUS_UPDATE
            elif psr2_man_trk.sf_single_full_frame:
                actual_su_mode = SuType.SU_SINGLE_FULL_FRAME_UPDATE
            else:
                actual_su_mode = SuType.SU_PARTIAL_FRAME_UPDATE
    else:
        if SuType.SU_CONTINUOUS_UPDATE in requested_su_mode and cff_ctl is None:
            logging.error('CFF/SFF CTL Register data is None')
            gdhm.report_driver_bug_pc("[PowerCons] [PSR_SFSU] CFF_CTL Register data is None")
            return None, actual_su_mode
        if SuType.SU_SINGLE_FULL_FRAME_UPDATE in requested_su_mode and sff_ctl is None:
            logging.error('CFF/SFF CTL Register data is None')
            gdhm.report_driver_bug_pc("[PowerCons] [PSR_SFSU] SFF_CTL Register data is None")
            return None, actual_su_mode
        # For Gen-15+ platforms there are dedicated registers for CFF and SFF
        if cff_ctl.sf_continuous_full_frame:
            actual_su_mode = SuType.SU_CONTINUOUS_UPDATE
        elif sff_ctl.sf_single_full_frame:
            actual_su_mode = SuType.SU_SINGLE_FULL_FRAME_UPDATE
        elif psr2_man_trk is not None and psr2_man_trk.sf_partial_frame_enable == 1:
            actual_su_mode = SuType.SU_PARTIAL_FRAME_UPDATE

    if requested_su_mode is not None and actual_su_mode not in requested_su_mode:
        verification_status = False
    return verification_status, actual_su_mode


##
# @brief        Internal API to calculate selective fetch region
# @param[in]    adapter Adapter
# @param[in]    panel panel object
# @param[in]    data Flip data
# @param[in]    v_active int, vertical active region
# @return       tuple (top_block, bottom_block)
def __calculate_selective_update_region(adapter, panel, data, v_active, psr2_mso_wa_status):
    rect_top = list()
    rect_bottom = list()
    top_block = 0
    bottom_block = 0

    for plane_info in data.PlaneDetailsList:
        # Src Res & Dest Res are same .
        if plane_info.SrcRight == plane_info.DestRight and plane_info.SrcBottom == plane_info. \
                DestBottom:
            if plane_info.DirtyRectBottom > v_active:
                logging.error("OS is giving rect size greater than screen res. DirtyRectBottom = {0} and "
                              "V active = {1}".format(plane_info.DirtyRectBottom, v_active))
                gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] OS is giving wrong Dirty Rect Data")
                rect_bottom.append(plane_info.DestBottom)
            else:
                rect_bottom.append(plane_info.DirtyRectBottom)
            rect_top.append(plane_info.DirtyRectTop)
        else:
            rect_top.append(plane_info.DestTop)
            rect_bottom.append(plane_info.DestBottom)

        if panel.mso_caps.is_mso_supported and psr2_mso_wa_status:
            # In TGL block starts from 1
            top_block = 1 if adapter.name in common.GEN_12_PLATFORMS else 0
        else:
            top_block = __calculate_block(adapter, min(rect_top))
        bottom_block = __calculate_block(adapter, max(rect_bottom), bottom=True)
    return top_block, bottom_block


##
# @brief        Internal API to verify whether driver is switching to Full Fetch during cursor event
# @param[in]    psr2_man_trk Register instance
# @param[in]    method Type of workload
# @return       cursor_verification_status - True if driver had switched to Full Fetch during cursor event, False otherwise
#               full_frame_count - Number of Full Frame updates happened
def __verify_cursor_event(adapter, panel, psr2_man_trk, method):
    full_frame_count = 0
    cursor_verification_status = True
    full_fetch_verification_happened = False
    cursor_event_data = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETPOINTERPOSITION)
    cff_ctl = None
    sff_ctl = None
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
    if cursor_event_data is None:
        logging.info(f"No cursor event during the workload : {method}")
        return None, full_frame_count
    for cursor_event in cursor_event_data:
        su_data_during_cursor_event = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True, start_time=cursor_event.StartTime, end_time=cursor_event.EndTime)
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            cff_data_during_cursor_event = etl_parser.get_mmio_data(cff_ctl.offset, start_time=cursor_event.StartTime, end_time=cursor_event.EndTime)
            sff_data_during_cursor_event = etl_parser.get_mmio_data(sff_ctl.offset, start_time=cursor_event.StartTime, end_time=cursor_event.EndTime)
        if not su_data_during_cursor_event:
            logging.debug(f"No MMIO writes found for PSR2_MAN_TRK during cursor event between {cursor_event.StartTime} and {cursor_event.EndTime}")
            continue
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            if not cff_data_during_cursor_event:
                logging.debug(f"No MMIO writes found for CFF_CTL_REGISTER during cursor event between {cursor_event.StartTime} and {cursor_event.EndTime}")
                continue
            if not sff_data_during_cursor_event:
                logging.debug(f"No MMIO writes found for SFF_CTL_REGISTER during cursor event between {cursor_event.StartTime} and {cursor_event.EndTime}")
                continue

        full_fetch_verification_happened = True
        psr2_man_trk.asUint = su_data_during_cursor_event[-1].Data
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            cff_ctl.asUint = cff_data_during_cursor_event[-1].Data
            sff_ctl.asUint = sff_data_during_cursor_event[-1].Data
        _, su_type = verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl)
        if su_type not in [SuType.SU_SINGLE_FULL_FRAME_UPDATE, SuType.SU_CONTINUOUS_UPDATE]:
            logging.error(f"Full Fetch is not enabled during Cursor Event between {cursor_event.StartTime} and {cursor_event.EndTime}")
            logging.info(f"SU Type during cursor event from {cursor_event.StartTime} and {cursor_event.EndTime} : {su_type}")
            cursor_verification_status = False
        else:
            logging.debug(f"Full Fetch is enabled for Cursor Event between {cursor_event.StartTime} and {cursor_event.EndTime}")
            full_frame_count +=1
    # Keeping full_fetch_verification_happened flag to not fail cursor event verification if there are no MMIO writes during all cursor events
    # Reason - If driver is already in full fetch mode during cursor events, it will not write FF values to the PSR2_MAN_TRK register again
    if not full_fetch_verification_happened:
        return None, full_frame_count
    return cursor_verification_status, full_frame_count


##
# @brief        Internal API to verify full fetch with dpst phasing
# @param[in]    start_time indicates the start time
# @param[in]    end_time indicates the end time
# @param[in]    psr2_man_trk register instance
# @return       True if Continuous Full Fetch is enabled during Dpst Phasing,
#               False when Continuous Full Fetch is not enabled during DPST Phasing,
#               None otherwise
def __verify_full_fetch_with_dpst_phasing(adapter, panel, start_time, end_time, psr2_man_trk):
    logging.info(f"\t STEP:Verifying CFFU with phasing between {start_time} and {end_time}")
    cff_ctl = None
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
    su_type = SuType.SU_NONE
    # Check for CFF register related MMIO writes during DPST phasing
    # There is a possibility for the driver to not write MMIO regiter if it is already in FullFetch
    # Validation is assuming, if there are no MMIO writes, driver is alredy in FullFetch
    # Keeping a flag(cff_verification_happened) to check whether CFF register writes are present during the flip or not
    psr2_man_trk_data = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True, start_time=start_time, end_time=end_time)
    if psr2_man_trk_data is None:
        logging.warning("No Entry found for PSR2_MAN_TRK during phasing")
        return None
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        for man_trk_val in psr2_man_trk_data:
            psr2_man_trk.asUint = man_trk_val.Data
            man_trk_status, su_type = verify_su_mode(adapter.name, psr2_man_trk, None, None, [SuType.SU_CONTINUOUS_UPDATE])
            if not man_trk_status:
                logging.debug(f"\tContinuous Full Fetch is not enabled at {man_trk_val.TimeStamp}. Current SU type ={ SuType(su_type).name}")
                continue
            logging.info("\tPASS:Continuous Full Fetch is enabled during Dpst Phasing")
            return True
    else:
        # There is a dedicated register for CFF from Gen-15 onwards
        cff_data = etl_parser.get_mmio_data(cff_ctl.offset, is_write=True, start_time=start_time, end_time=end_time)
        pos = 0
        if cff_data is None:
            logging.warning("No Entry found for CFF_CTL_REGISTER during DPST phasing")
            return None
        for data in cff_data:
            cff_ctl.asUint = data.Data
            cff_status, su_type = verify_su_mode(adapter.name, None, cff_ctl, None, [SuType.SU_CONTINUOUS_UPDATE])
            if not cff_status:
                logging.debug(f"\tContinuous Full Fetch is not enabled at {data.TimeStamp}. Current SU type ={ SuType(su_type).name}")
                continue
            logging.info("\tPASS:Continuous Full Fetch is enabled during DPST Phasing")
            return True
    logging.error(f"\tContinuous Full Fetch is not enabled during DPST phasing. Current SU type = {SuType(su_type).name}")
    return False


def __update_dpst_time_stamp(time_stamp, data):
    status = False
    # Update DPST time stamp for every flip
    if time_stamp and data.TimeStamp > time_stamp:
        interrupt_ctl_2 = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2, start_time=time_stamp,
                                                  end_time=data.TimeStamp)
        if interrupt_ctl_2 is not None:
            interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                           etl_parser.InterruptType.CRTC_VSYNC)
            if interrupt_data is not None:
                for interrupt in interrupt_data:
                    # update prev_flip time stamp with Vsync disable interrupt time stamp
                    if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE]:
                        logging.info(
                            f"\t\tVBI disable notification received at {interrupt.TimeStamp}")
                        if time_stamp < interrupt.TimeStamp < data.TimeStamp:
                            time_stamp = interrupt.TimeStamp
                            status = True
        if status is False:
            # update prev_flip time stamp with current flip time stamp if VSYNC disable call is not received from OS
            time_stamp = data.TimeStamp
    return time_stamp


def __verify_dirty_rect_calculation(adapter, panel, flip, v_active, psr2_man_trk, man_trk, cff_ctl_data, sff_ctl_data, full_frame_count, sf_count, fail_count, psr2_mso_wa_status):
    status = True
    cff_ctl = None
    sff_ctl = None
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
        cff_ctl.asUint = cff_ctl_data[-1]
        sff_ctl.asUint = sff_ctl_data[-1]
    psr2_man_trk.asUint = man_trk[-1].Data
    top_block, bottom_block = __calculate_selective_update_region(adapter, panel, flip, v_active, psr2_mso_wa_status)
    _, su_type = verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl)
    logging.debug(f"\tSU Type : {SuType(su_type).name}")
    if su_type in [SuType.SU_SINGLE_FULL_FRAME_UPDATE, SuType.SU_CONTINUOUS_UPDATE] \
            or flip.PlaneCount > 1:
        full_frame_count += 1
    else:
        start_address = psr2_man_trk.su_region_start_address
        end_address = psr2_man_trk.su_region_end_address
        if top_block == start_address and bottom_block == end_address:
            logging.info("\tPASS : DIRTY RECTANGLE values Expected = {0} Actual = {1}".format(
                (top_block, bottom_block), (start_address, end_address)))
            sf_count += 1
        else:
            status = False
            fail_count += 1
            logging.error("\tFAIL : DIRTY RECTANGLE values Expected = {0} Actual = {1}".format(
                (top_block, bottom_block), (start_address, end_address)))
            logging.debug(f"Flip data : {flip}")
            logging.debug(f"Timestamp of Dirty Rectangle Failure : {flip.TimeStamp}")
    return status, full_frame_count, sf_count, fail_count


##
# @brief        Internal API to verify CFF for ASYNC Flips
# @param[in]    adapter             Adapter object
# @param[in]    flip_data           Mpo3 Flip Data
# @param[in]    psr2_man_trk        Register instance
# @param[in]    cff_ctl             Register instance
# @return       True if CFF verification is successful, False otherwise
def __verify_cff_for_async_flips(adapter, flip_data, psr2_man_trk, cff_ctl):
    cff_status = True
    cff_verification_happened = False
    # Check for CFF register related MMIO writes during the ASYNC Flip
    # There is a possibility for the driver to not write MMIO regiter if it is already in FullFetch
    # Validation is assuming, if there are no MMIO writes, driver is alredy in FullFetch
    # Keeping a flag(cff_verification_happened) to check whether CFF register writes are present during the flip or not
    for mmio_data in flip_data.MmioDataList:
        if adapter.name in common.PRE_GEN_15_PLATFORMS and mmio_data.Offset == psr2_man_trk.offset and mmio_data.IsWrite:
            psr2_man_trk.asUint = mmio_data.Data
            status, _ = verify_su_mode(adapter.name, psr2_man_trk, None, None, [SuType.SU_CONTINUOUS_UPDATE])
            cff_status &= status
            cff_verification_happened = True

        if adapter.name not in common.PRE_GEN_15_PLATFORMS and mmio_data.Offset == cff_ctl.offset and mmio_data.IsWrite:
            cff_ctl.asUint = mmio_data.Data
            status, _ = verify_su_mode(adapter.name, None, cff_ctl, None, [SuType.SU_CONTINUOUS_UPDATE])
            cff_status &= status
            cff_verification_happened = True

    if not cff_verification_happened:
        logging.debug(f"No CFF register writes found for the ASYNC flip at {flip_data.TimeStamp}")
        return True

    if cff_status is False:
        logging.error(f"Continuous Full Frame bit is not set for Async flip at {flip_data.TimeStamp}")
        return False
    logging.debug(f"Continuous Full Frame is enabled for Async flip at {flip_data.TimeStamp}")
    return True


################################################################################################################################################################################################################################################
# API's below this partition are a part of SFSU verification refactor according to VBI Optimization.
# There is a driver bug where Dirty Rectangle values are not being programmed as expected : https://hsdes.intel.com/appstore/article/#/18024248787
# Below API's will remain to be unused until the issue gets resolved from the driver and they will work only after OsAwareFlipQ is enabled by default -
# - (NotifyVsyncLogBuffer data will come in the ETL only after OsAwareFlipQ Enable)
################################################################################################################################################################################################################################################


##
# @brief        Internal API to verify Dirty Rect calculation
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    method verification method(video/cursor/app)
# @param[in]    feature enum, SFSU/FFSU
# @param[in]    dpst_enable bool, dpst_enable_status
# @param[in]    sf_plane_ctl  register instance
# @param[in]    psr2_man_trk register instance
# @param[in]    flip_data list
# @param[in]    vbi_data list
# @return       status Boolean, True if verification is successful, False otherwise
def __verify_dirty_rect_vbi_opt(adapter, panel, method, feature, dpst_enable, sf_plane_ctl, psr2_man_trk, flip_data, vbi_data):
    assert adapter
    assert panel
    fail_count = 0
    status = True
    full_frame_count = 0
    sf_count = 0
    dpst_phase_in_time = 0
    dpst_phase_done_time = 0
    all_param = False
    prev_dpst_phase_in_type = None

    # HSD-14014971492 - WA for PSR2 + MSO panel to program start region always 0
    wa_14014971492_status = False
    if adapter.name in common.PRE_GEN_14_PLATFORMS or (adapter.name in ['MTL'] and adapter.cpu_stepping == 0):
        wa_14014971492_status = True

    v_total = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name)
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
    v_active = v_total.vertical_active + 1
    prev_dpst_phase_in_type = None

    # Check whether driver is switching to Full Fetch during DPST phasing
    # Check PSR CLIENT EVENT for Phasing & Phase out
    # {"PipeId":"PIPE_A","Operation":"PSR_DPST_PHASE_EVENT","Field1":0,"Field2":0,"TimeStamp":122.9376}
    psr_dpst_data = etl_parser.get_psr_event_data(etl_parser.Events.PSR_DPST_PHASE_EVENT)
    # Need to re-consider the below check as a part of the JIRA : https://jira.devtools.intel.com/browse/VSDI-34799
    if psr_dpst_data is None:
        logging.info("No DPST Data found in PSR Client event in the ETL")
    else:
        for client_event in psr_dpst_data:
            if client_event.PipeId != 'PIPE_' + panel.pipe:
                continue

            if client_event.Field1:  # Field1 -> DpstPhaseAdjustmentInProgress
                dpst_phase_in_time = client_event.TimeStamp
                prev_dpst_phase_in_type = client_event.Operation
                dpst_phase_done_time = 0
                continue
            if client_event.Field1 != 0 or client_event.Operation != prev_dpst_phase_in_type:
                continue
            dpst_phase_done_time = client_event.TimeStamp

            if dpst_phase_in_time and dpst_phase_done_time:
                if __verify_full_fetch_with_dpst_phasing(adapter, panel, dpst_phase_in_time, dpst_phase_done_time,
                                                            psr2_man_trk) is False:
                    gdhm.report_driver_bug_pc("[PowerCons][PSR2] Continuous Full Fetch is not enabled during DPST phasing")
                    return False
                dpst_phase_in_time = dpst_phase_done_time = 0
                prev_dpst_phase_in_type = None
        logging.info("SUCCESS : Full Fetch verification during DPST Phasing")

    # Check whether driver is switching to Full Fetch during Cursor Event
    if feature == psr.UserRequestedFeature.PSR2_SFSU:
        cursor_status, full_frame_count = __verify_cursor_event(adapter, panel, psr2_man_trk, method)
        if cursor_status is False:
            logging.error("FAIL : Cursor status verification")
            gdhm.report_driver_bug_pc("[Powercons][PSR] Driver did not switch to Full Fetch during cursor events")
            return False
        logging.info("SUCCESS : Full fetch verification during Cursor Event")

    # Verify Dirty Rectangle Programming
    notify_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT)
    notify_present_id_list = []
    dwm_flip_list = []
    video_flip_list = []
    if notify_data is None:
        logging.error("Notify VSync Log Buffer data is empty")
        gdhm.report_driver_bug_os("[OsFeatures][Display_Flips] Notify VSync Log Buffer data is empty")
        return False
    for notify_log_buffer_ext in notify_data:
        notify_present_id_list.append(notify_log_buffer_ext.PresentID)
    pos = 0
    for index in range(pos, len(flip_data)):
        union_top_block = None
        union_bottom_block = None
        # Cache the flips in the respective Lists based on LayerID.
        # Reason for iterating through the length of PlaneDetailsList -
        # In multi-plane flip, if one of the plane is not enabled(Check for 'Enabled' in Flags field of PlaneInfoList), we will not get plane details for the disabled Plane from driver.
        # This being the case we will end up having only one entry for Plane Details in multi-plane flip.
        # Disadvantage of the below logic - We will always cache the Plane Details List to the respective cache based on first Layer Index entry.
        # i.e It will always be cached to DWM flip list as we will not have any corresponding data for identifying layer index in the PlaneDetailsList.
        for plane_index_1 in range(len(flip_data[index].PlaneDetailsList)):
            if flip_data[index].PlaneInfoList[plane_index_1].LayerIndex == 0:
                dwm_flip_list.append(flip_data[index].PlaneDetailsList[plane_index_1])
            else:
                video_flip_list.append(flip_data[index].PlaneDetailsList[plane_index_1])

        man_trk = []
        cff_ctl_data = []
        sff_ctl_data = []
        for mmio_data in flip_data[index].MmioDataList:
            if flip_data[index].IsAllParam:
                all_param = True
                # For AllParam Sync Flip , Selective Fetch for Plane will be enabled/disabled
                # based on the restrictions
                if mmio_data.IsWrite is True and mmio_data.Offset == sf_plane_ctl.offset:
                    sf_plane_ctl.asUint = mmio_data.Data
                    if sf_plane_ctl.selective_fetch_plane_enable == 0:
                        logging.error(f"Selective Fetch is Disabled at {mmio_data.TimeStamp}")
                        gdhm.report_driver_bug_pc("[PowerCons][PSR] Selective Fetch was disabled for AllParam flip")
                        return False
            if mmio_data.IsWrite and mmio_data.Offset == psr2_man_trk.offset:
                man_trk.append(mmio_data)
            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                if mmio_data.Offset == cff_ctl.offset:
                    cff_ctl_data.append(mmio_data)
                if mmio_data.Offset == sff_ctl.offset:
                    sff_ctl_data.append(mmio_data)
        if not man_trk or (not dwm_flip_list and not video_flip_list):
            if (not dwm_flip_list and not video_flip_list):
                logging.info(f"No DWM/Video flip data for flip {flip_data[index].TimeStamp}")
            else:
                logging.debug(f"No PSR2_MAN_TRK writes during the flip at {flip_data[index].TimeStamp}")
        else:
            # Consider all flips in both DWM and Video list to get the combined Top and Bottom block values
            union_top_block, union_bottom_block = calculate_union(adapter, panel, v_active, dwm_flip_list, video_flip_list, wa_14014971492_status)

            # Verify Dirty Rectangle Calculation - Start and end offsets programmed by the driver during the current flip vs Expected Top and bottom block from MPO3 flip data
            status, full_frame_count, sf_count, fail_count = __verify_dirty_rect_calculation_vbi_opt(adapter, panel, flip_data[index], psr2_man_trk, man_trk, cff_ctl_data, sff_ctl_data, full_frame_count, sf_count, fail_count, union_top_block, union_bottom_block)

        # Clear the cache based on LayerID if the flip has FlipDone Interrupt
        for plane_index_2 in range(len(flip_data[index].PlaneDetailsList)):
            # Disadvantage of the below logic - If flip done would have come for Video flip and not for DWM flip in multi-plane, single PlaneDetails entry, we will end up missing the cache clearence
            # Although, in the above case, expectation is, flip done interrupt should come for both layers. So the logic should still work
            if flip_data[index].PlaneInfoList[plane_index_2].PresentId in notify_present_id_list:
                if flip_data[index].PlaneInfoList[plane_index_2].LayerIndex == 0:
                    dwm_flip_list = []
                else:
                    if flip_data[index].PlaneInfoList[plane_index_2].LayerIndex == 1:
                        video_flip_list = []
        pos += 1

    logging.info(f"Total no.of Selective fetch updates happened = {sf_count}")
    logging.info(f"Total no.of full frame updates happened = {full_frame_count}")

    # HSD - 16011135426 - OS is not giving dirty rectangle values correctly
    # With PSR2 + VDSC panel, most of the times OS is giving Dirt rect data with full frame values only
    # skipping this check for PSR2 + VDSC supported panel
    if (panel.vdsc_caps.is_vdsc_supported is False) and method in ['VIDEO',
                                                                   'VIDEO_CURSOR'] and \
            all_param is False and sf_count == 0:
        error_title = f"selective update not happened with {method}"
        logging.error(error_title)
        gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] " + error_title)
        return False
    if fail_count:
        logging.error(f"Total no.of Dirty Rectangle Failures:{fail_count}")
        gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] Dirty Rectangle verification failed")
        status = False
    return status


##
# @brief        Internal API to verify Dirty Rectangle calcualtion - MPO3 Flip vs Man Trk Register
# @param[in]    flip                  MPO3 Flip Data
# @param[in]    psr2_man_trk          Register instance
# @param[in]    man_trk_list          List of PSR2 Man Trk writes during the flip
# @param[in]    full_frame_count      Number of full frame updates happened
# @param[in]    sf_count              Number of selective updates happened
# @param[in]    fail_count            Number of Dirty Rectangle failures
# @param[in]    top_block             Top block value of the flip
# @param[in]    bottom_block          Bottom block value of the flip 
# @return       verification status, No. of Full Frame Updates, No. of Selective Updates, No. of Dirty Rectangle failures
def __verify_dirty_rect_calculation_vbi_opt(adapter, panel, flip, psr2_man_trk, man_trk_list, cff_ctl_data, sff_ctl_data, full_frame_count, sf_count, fail_count, top_block, bottom_block):
    status = True
    psr2_man_trk.asUint = man_trk_list[-1].Data
    cff_ctl = None
    sff_ctl = None
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
        cff_ctl.asUint = cff_ctl_data[-1].Data
        sff_ctl.asUint = sff_ctl_data[-1].Data
    _, su_type = verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl)
    if not status:
        logging.error("SU mode status verification failed")
        return False
    logging.debug(f"\tSU Type : {SuType(su_type).name}")
    if su_type in [SuType.SU_SINGLE_FULL_FRAME_UPDATE, SuType.SU_CONTINUOUS_UPDATE] \
            or flip.PlaneCount > 1:
        full_frame_count += 1
    else:
        start_address = psr2_man_trk.su_region_start_address
        end_address = psr2_man_trk.su_region_end_address
        if panel.psr_caps.early_transport_supported or panel.pr_caps.early_transport_supported:
            logging.info(f"Updating Top Block to 0 for Early Transport supported panel")
            top_block = 0  # Plane & pipe re-size will happen in case of Early transport to match SU region height
        if top_block == start_address and bottom_block == end_address:
            logging.info("\tPASS : DIRTY RECTANGLE values Expected = {0} Actual = {1}".format(
                (top_block, bottom_block), (start_address, end_address)))
            sf_count += 1
        else:
            status = False
            fail_count += 1
            logging.error("\tFAIL : DIRTY RECTANGLE values Expected = {0} Actual = {1}".format(
                (top_block, bottom_block), (start_address, end_address)))
            logging.debug(f"Flip data : {flip}")
            logging.error(f"Timestamp of Dirty Rectangle Failure : {flip.TimeStamp}")
    return status, full_frame_count, sf_count, fail_count


##
# @brief        Internal API to calculate the block union of all pending flips in cache
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    v_active Vertical Active region
# @param[in]    dwm_flip_list list, List of pending DWM Flips
# @param[in]    video_flip_list list, List of pending Video Flips
# @param[in]    psr2_mso_wa_status Boolean, Indicates the status of PSR2 MSO WA
# @return       Union of top blocks and bottom blocks of all pending flips
def calculate_union(adapter, panel, v_active, dwm_flip_list, video_flip_list, psr2_mso_wa_status):
    lst_top_block_dwm = []
    lst_bottom_block_dwm = []
    union_top_block = None
    union_bottom_block = None
    for d_flip in dwm_flip_list:
        top_block_dwm, bottom_block_dwm = __calculate_selective_update_region_vbi_opt(adapter, panel, d_flip, v_active, psr2_mso_wa_status)
        lst_top_block_dwm.append(top_block_dwm)
        lst_bottom_block_dwm.append(bottom_block_dwm)

    lst_top_block_video = []
    lst_bottom_block_video = []
    for v_flip in video_flip_list:
        top_block_video, bottom_block_video = __calculate_selective_update_region_vbi_opt(adapter, panel, v_flip, v_active, psr2_mso_wa_status)
        lst_top_block_video.append(top_block_video)
        lst_bottom_block_video.append(bottom_block_video)

    union_top_block = min(min(lst_top_block_dwm, default=999999), min(lst_top_block_video, default=999999))
    union_bottom_block = max(max(lst_bottom_block_dwm, default=0), max(lst_bottom_block_video, default=0))

    return union_top_block, union_bottom_block


##
# @brief        Internal API to calculate selective fetch region
# @param[in]    adapter Adapter
# @param[in]    panel panel object
# @param[in]    data Flip data
# @param[in]    v_active int, vertical active region
# @param[in]    psr2_mso_wa_status Boolean, Indicates the status of PSR2 MSO WA
# @return       tuple (top_block, bottom_block)
def __calculate_selective_update_region_vbi_opt(adapter, panel, flip_plane_info, v_active, psr2_mso_wa_status):
    rect_top = list()
    rect_bottom = list()
    top_block = 0
    bottom_block = 0

    # For DWM Plane flip - Src Res & Dest Res will be same
    if flip_plane_info.SrcRight != flip_plane_info.DestRight or flip_plane_info.SrcBottom != flip_plane_info. \
            DestBottom:
        rect_top.append(flip_plane_info.DestTop)
        rect_bottom.append(flip_plane_info.DestBottom)
    else:
        if flip_plane_info.DirtyRectBottom > v_active:
            logging.error(f"OS is giving rect size greater than screen res. DirtyRectBottom = {flip_plane_info.DirtyRectBottom} and "
                          f"V active = {v_active}")
            gdhm.report_driver_bug_pc("[PowerCons][PSR_SFSU] OS is giving invalid Dirty Rect Data")
            rect_bottom.append(flip_plane_info.DestBottom)
        else:
            rect_bottom.append(flip_plane_info.DirtyRectBottom)
        rect_top.append(flip_plane_info.DirtyRectTop)

    if panel.mso_caps.is_mso_supported and psr2_mso_wa_status:
        # In TGL block starts from 1
        top_block = 1 if adapter.name in common.GEN_12_PLATFORMS else 0
    else:
        top_block = __calculate_block(adapter, min(rect_top))
    bottom_block = __calculate_block(adapter, max(rect_bottom), bottom=True)
    return top_block, bottom_block


##
# @brief        Internal API to calculate selective fetch region
# @param[in]    adapter Adapter
# @param[in]    panel panel object
# @param[in]    flip Flip data
# @param[in]    top dirtyRect top
# @param[in]    bottom  dirty rect bottom
# @return       result True if verification is successful , False otherwise
def __verify_selective_fetch_programming(adapter, panel, top, bottom, start_time, end_time):
    if not (panel.psr_caps.early_transport_supported or panel.pr_caps.early_transport_supported):
        return True
    status = True
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    sf_plane_instance = MMIORegister.get_instance("SEL_FETCH_PLANE_OFFSET_REGISTER",
                                                  "SEL_FETCH_PLANE_OFFSET_" + str(plane_id) + "_" + panel.pipe,
                                                  adapter.name)
    sf_plane_size_instance = MMIORegister.get_instance("SEL_FETCH_PLANE_SIZE_REGISTER",
                                                       "SEL_FETCH_PLANE_SIZE_" + str(plane_id) + "_" + panel.pipe,
                                                       adapter.name)
    sf_plane_pos_instance = MMIORegister.get_instance("SEL_FETCH_PLANE_POS_REGISTER",
                                                      "SEL_FETCH_PLANE_POS_" + str(plane_id) + "_" + panel.pipe,
                                                      adapter.name)

    pipe_srcsz_instance = MMIORegister.get_instance("PIPE_SRCSZ_REGISTER", "PIPE_SRCSZ_ERLY_TPT_" + panel.pipe,
                                                    adapter.name)
    cur_pos_instance = MMIORegister.get_instance("CUR_POS_ERLY_TPT_REGISTER", "CUR_POS_ERLY_TPT_" + panel.pipe,
                                                 adapter.name)

    sf_plane_pos_offset_data = etl_parser.get_mmio_data(sf_plane_instance.offset, is_write=True, start_time=start_time,
                                                        end_time=end_time)
    sf_plane_size_data = etl_parser.get_mmio_data(sf_plane_size_instance.offset, is_write=True, start_time=start_time,
                                                  end_time=end_time)
    sf_plane_pos_data = etl_parser.get_mmio_data(sf_plane_pos_instance.offset, is_write=True, start_time=start_time,
                                                 end_time=end_time)
    pipe_srcsz_data = etl_parser.get_mmio_data(pipe_srcsz_instance.offset, is_write=True, start_time=start_time,
                                               end_time=end_time)
    cur_pos_data = etl_parser.get_mmio_data(cur_pos_instance.offset, is_write=True, start_time=start_time,
                                            end_time=end_time)
    cursor = etl_parser.get_event_data(etl_parser.Events.CURSOR_POS, start_time=start_time, end_time=end_time)
    if sf_plane_pos_offset_data is None:
        logging.error(f"No entries found for mmio SEL_PLANE_OFFSET offset {sf_plane_instance.offset}")
        return False
    if sf_plane_size_data is None:
        logging.error(f"No entries found for mmio SEL_PLANE_SIZE offset {sf_plane_size_instance.offset}")
        return False
    if sf_plane_pos_data is None:
        logging.error(f"No entries found for mmio SEL_PLANE_POS offset {sf_plane_pos_instance.offset}")
        return False
    if pipe_srcsz_data is None:
        logging.error(f"No entries found for mmio PIPE_SRCSZ_ERLY_TPT offset {pipe_srcsz_instance.offset}")
        return False
    sf_plane_instance.asUint = sf_plane_pos_offset_data[-1].Data
    sf_plane_size_instance.asUint = sf_plane_size_data[-1].Data
    sf_plane_pos_instance.asUint = sf_plane_pos_data[-1].Data
    pipe_srcsz_instance.asUint = pipe_srcsz_data[-1].Data
    # where there is no cursor event during workload, cur_pos_erly_tpt mmio writes will not present in ETL
    if cursor:
        cur_pos_instance.asUint = cur_pos_data[-1].Data
        if cursor[-1].y <= top <= bottom:
            logging.info(f"Cursor is inside of SU region")
        elif (cursor[-1].y - bottom) > 0:
            # cursor is placed after the su region. Need to extend Su region to include cursor position
            bottom = __calculate_block(adapter, bottom + (cursor[-1].y - bottom), bottom=True)
            logging.info(f"New SU bottom value with cursor included = {bottom}")

        # CUR_POS_ERLY_TPT Y position = MAX(-1 * <Cursor vertical size from CUR_CTL base on cursor modeselect setting> + 1, CUR_POS Y Position - Update region Y position)
        if cur_pos_instance.y_position_magnitude != max(-1, cursor[-1].y):
            logging.error(f"Expected Cursor pos = {cursor[-1].y} Actual = {cur_pos_instance.y_position_magnitude}")
            status = False

    # For Early transport, Plane & pipe size re-sized to SU region size . Y position always start from 0
    if sf_plane_pos_instance.y_position != 0:
        logging.error(f"Expected SF Plane pos = {0} Actual = {sf_plane_pos_instance.y_position}")
        status &= False
    if top != sf_plane_instance.start_y_position:
        logging.error(f"Expected SF Plane offset = {top} Actual = {sf_plane_instance.start_y_position}")
        status &= False
    if (bottom - top) != sf_plane_size_instance.height:
        logging.error(f"Expected SF Plane size = {bottom - top} Actual = {sf_plane_size_instance.height}")
        status &= False

    # PIPE SRCZ check
    if (bottom - top) != pipe_srcsz_instance.vertical_source_size + 1:
        logging.error(f"Expected Pipe vertical size= {bottom - top} Actual= {pipe_srcsz_instance.vertical_source_size}")
        status &= False
    return status


##
# @brief        Internal API to verify Psr disable for ASYNC Flips
# @param[in]    adapter_name    Adapter name
# @param[in]    feature         Feature to validate (PSR2/PR)
# @param[in]    flip_data       MPO3 Flip entry
# @param[in]    psr2_ctl        PSR2_CTL Register instance
# @param[in]    pr_ctl          PR CTL Register instance(TRANS_DP2_CTL_REGISTER)
# @return       True if PSR disable verification with ASYNC flip is successful, False otherwise
def __verify_psr_pr_disable_for_async_flips(feature, flip_data, psr2_ctl, pr_ctl):
    feature_to_validate = ""
    if psr.UserRequestedFeature.PSR_2 <= feature < psr.UserRequestedFeature.PANEL_REPLAY:
        feature_to_validate = "PSR2"
    elif feature == psr.UserRequestedFeature.PANEL_REPLAY:
        feature_to_validate = "PANEL_REPLAY"

    if feature_to_validate == "":
        logging.error("Invalid feature name given for Async flip verification")
        return False

    # Wa_22018697067 - PSR2 will be disabled for Async flip on MTL
    # PSR/PR will be disabled for ASYNC flips from LNL+ - https://hsdes.intel.com/appstore/article/#/14019644643
    for mmio_data in flip_data.MmioDataList:
        if not mmio_data.IsWrite or mmio_data.Offset != psr2_ctl.offset:
            continue
        if feature_to_validate == "PSR2" and mmio_data.IsWrite and mmio_data.Offset == psr2_ctl.offset:
            logging.info(f"Found {feature_to_validate} CTL entry with val ={hex(mmio_data.Data)} at {mmio_data.TimeStamp}")
            psr2_ctl.asUint = mmio_data.Data
            if psr2_ctl.psr2_enable:
                logging.error("PSR2 not disabled for Async flip")
                return False
            logging.info(f"PASS: PSR2 disabled for Async flip at {flip_data.TimeStamp}")
        elif feature_to_validate == "PANEL_REPLAY" and mmio_data.IsWrite and mmio_data.Offset == pr_ctl.offset:
            logging.info(f"Found {feature_to_validate} CTL entry with val ={hex(mmio_data.Data)} at {mmio_data.TimeStamp}")
            pr_ctl.asUint = mmio_data.Data
            if pr_ctl.pr_enable:
                logging.error("PR not disabled for Async flip")
                return False
            logging.info(f"PASS: PR disabled for Async flip at {flip_data.TimeStamp}")
    return True

