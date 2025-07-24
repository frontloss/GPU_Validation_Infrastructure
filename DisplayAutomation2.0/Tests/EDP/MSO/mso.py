########################################################################################################################
# @file                 mso.py
# @addtogroup           MSO
# @section              MSO_Libs
# @brief                This file contains MSO verification APIs
#
# @author               Bhargav Adigarla
########################################################################################################################

import logging

from Libs.Core import registry_access, driver_escape, enum, display_essential
from Libs.Core.logger import gdhm
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dpcd
from registers.mmioregister import MMIORegister

# GDHM header
GDHM_MSO_COG = "[Display_Interfaces][EDP][MSO_COG]"

MSO_VALID_LiNKS = [2, 4]


##
# @brief        API to check MSO support on given display
# @param[in]    target_id target id of the panel
# @return       Boolean, True, if MSO is supported by given panel, False if not supported
# @note         For display to support MSO: DPCD: 0x7A4 must be 2 or 4
def is_mso_supported_in_panel(target_id):
    mso_caps = dpcd.EdpMsoCaps(target_id)
    if mso_caps.no_of_links in MSO_VALID_LiNKS:
        return True
    return False


##
# @brief        API to verify mode enumeration w.r.t MSO on given display
# @param[in]    panel
# @param[in]    pixel_overlap_count Count of pixel overlap
# @return       Boolean, True, if mode enumeration is correct, False if not correct
# @note         OS reported mode should be equals to hactive_in_edid x num_of_links
# @note         OS reported pixel clk should be equals to pixel_clk_in_edid x num_of_links
def verify_timing(panel, pixel_overlap_count=0):
    mode = common.get_display_mode(panel.target_id)
    logging.debug(
        "current mode is {0}x{1}@{2} with Pixel overlap count: {3}".format(mode.HzRes, mode.VtRes, mode.refreshRate,
                                                                           pixel_overlap_count))
    edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.target_id)
    if not edid_flag:
        logging.error(f"Failed to get EDID data for target_id : {panel.target_id}")
        assert edid_flag, "Failed to get EDID data"

    # pixel clock will be in EDID[54], EDID[55] in multiples of 10000
    # ex:- EDID[54] = 0x01, EDID[55]= 0x1D, pixel_clock = 0x1D01 = 7425 = 74.25Mhz
    edid_pclk = (edid_data[55] << 8) | edid_data[54]

    # hactive will be in 56th byte and msb of 58th byte
    # ex:- EDID[56] = 0x12, EDID[58] = 0x34, hactive = 0x312
    edid_hactive = edid_data[56] | ((edid_data[58] >> 4) << 8)

    if mode.pixelClock_Hz == edid_pclk * 10000:
        logging.info("\tPASS: pixel clock Actual= {0}, Expected= {1}".
                     format(edid_pclk * 10000, mode.pixelClock_Hz))
    else:
        logging.error("\tFAIL: pixel clock Actual= {0}, Expected= {1}".
                      format(edid_pclk * 10000, mode.pixelClock_Hz))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Pixel clock verification failed")
        return False

    expected_hactive = edid_hactive - (pixel_overlap_count * panel.mso_caps.no_of_segments)

    if (mode.HzRes != expected_hactive) and (mode.HzRes != (expected_hactive - 16)):
        logging.error("\tFAIL: Mode Actual= {0}, Expected= {1}".format(mode.HzRes, expected_hactive))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Mode enumeration verification failed")
        return False
    logging.info("\tPASS: Mode Actual= {0}, Expected= {1}".format(mode.HzRes, expected_hactive))
    return True


##
# @brief        API to apply pixel overlap count from Registry
# @param[in]    count expected pixel overlap count value in range (1,8)
# @return       Boolean, True, if writing to registry successful else False
def set_pixel_overlap_count_registry(count):
    reg_args = registry_access.StateSeparationRegArgs("gfx_0")
    reg_key = 'DisplayOverlapValMSO'
    status = registry_access.write(args=reg_args, reg_name=reg_key, reg_type=registry_access.RegDataType.DWORD,
                                   reg_value=count)
    if status is False:
        logging.error("Writing to the Registry Failed")
        return False

    # If value is updated then restart the driver
    if status is True:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\t\tFailed to restart display driver")
            return False
    return True


##
# @brief        API to verify pixel overlap count
# @param[in]    panel
# @return       Boolean, True, if actual and expected pixel overlap count matches else False
# @note         Pixel overlap count value for eDP should be in range of 1 to 8
def verify_pixel_overlap_count(panel):
    reg_args = registry_access.StateSeparationRegArgs("gfx_0")
    expected_pixel_overlap_count, reg_type = registry_access.read(args=reg_args, reg_name='DisplayOverlapValMSO')

    if common.PLATFORM_NAME == 'ICLLP' or common.PLATFORM_NAME == 'JSL':
        if panel.pipe == 'A':
            dss_ctl1 = MMIORegister.read("DSS_CTL1_REGISTER", 'DSS_CTL1', common.PLATFORM_NAME)
        else:
            dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + panel.pipe, common.PLATFORM_NAME)
    else:
        dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + panel.pipe, common.PLATFORM_NAME)

    actual_pixel_overlap_count = dss_ctl1.overlap

    if (expected_pixel_overlap_count != actual_pixel_overlap_count) or \
            ((expected_pixel_overlap_count not in range(1, 9)) or (actual_pixel_overlap_count not in range(1, 9))):
        logging.error("FAIL: MSO Pixel overlap count doesn't match. Expected= {0} , Actual= {1}".format(
            expected_pixel_overlap_count, actual_pixel_overlap_count))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Pixel overlap count verification failed")
        return False
    logging.info("PASS: MSO Pixel overlap count. Expected= {0} , Actual= {1}".format(expected_pixel_overlap_count,
                                                                                     actual_pixel_overlap_count))
    return True


##
# @brief        API to verify MSO on given display
# @param[in]    panel
# @return       Boolean, True, if MSO is enabled, False if not enabled
# @note         Verifying if splitter is enabled, and mode enumeration is proper.
def verify(panel):
    if common.PLATFORM_NAME == 'ICLLP' or common.PLATFORM_NAME == 'JSL':
        if panel.pipe == 'A':
            dss_ctl1 = MMIORegister.read("DSS_CTL1_REGISTER", 'DSS_CTL1', common.PLATFORM_NAME)
        else:
            dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + panel.pipe, common.PLATFORM_NAME)
    else:
        dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + panel.pipe, common.PLATFORM_NAME)

    if dss_ctl1.splitter_enable == 1:
        logging.info("\tMSO enabled for Pipe {0}".format(panel.pipe))
        if common.PLATFORM_NAME not in common.PRE_GEN_13_PLATFORMS:
            expected_splitter_configuration = 0 if panel.mso_caps.no_of_segments == 2 else 1
            if expected_splitter_configuration == dss_ctl1.splitter_configuration:
                logging.info("\tPASS: Splitter configuration expected = {0} actual = {1}".
                             format(expected_splitter_configuration, dss_ctl1.splitter_configuration))
            else:
                logging.info("\tFAIL: Splitter configuration expected = {0} actual = {1}".
                             format(expected_splitter_configuration, dss_ctl1.splitter_configuration))
                gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Splitter configuration programming failed")
                return False
    else:
        logging.error("\tMSO disabled for Pipe {0}".format(panel.pipe))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} DSS CTL1 Splitter disabled")
        return False

    lanes = dpcd.MaxLaneCount(panel.target_id)
    max_lane_count = lanes.max_lane_count
    pixel_overlap_count = dss_ctl1.overlap

    if max_lane_count and panel.mso_caps.no_of_segments in MSO_VALID_LiNKS and max_lane_count >= panel.mso_caps.no_of_segments:
        expected_lane_count = max_lane_count
    else:
        logging.error(
            "\tNot a valid lane-link combination links = {0} lanes = {1}".format(panel.mso_caps.no_of_segments, max_lane_count))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Not a valid lane-link combination")
        return False

    lane_count_set = dpcd.LaneCountSet(panel.target_id)
    if lane_count_set.lane_count_set == expected_lane_count:
        logging.info("\tPASS: lane count expected = {0} actual = {1}".
                     format(expected_lane_count, lane_count_set.lane_count_set))
    else:
        logging.info("\tFAIL: lane count expected = {0} actual = {1}".
                     format(expected_lane_count, lane_count_set.lane_count_set))
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} lane count programming failed")
        return False

    if verify_timing(panel) is False:
        return False

    return True


##
# @brief        API to check if MSO is enabled throughout the workload using polling data
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    polling_data list containing the timestamp and values of given offsets at provided intervals
# @return       True if MSO was enabled throughout the workload, False otherwise
def is_mso_enabled(adapter, panel, polling_data):
    dss_ctl1 = MMIORegister.get_instance("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + panel.pipe, adapter.name)
    polling_timeline = polling_data[0]
    if dss_ctl1.offset not in polling_timeline.keys():
        logging.error(f"Polling data does not contain the entry for PIPE_DSS_CTL1_P{panel.pipe}")
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Polling data does not contain the entry for PIPE")
        return False
    dss_ctl_data = polling_timeline[dss_ctl1.offset]
    if len(dss_ctl_data) < 1:
        logging.error(f"No Values found in the values list of PIPE_DSS_CTL1_P{panel.pipe} offset")
        gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} No Values found in the values list of PIPE")
        return False
    for i in range(len(dss_ctl_data)):
        dss_ctl1.asUint = polling_timeline[dss_ctl1.offset][i]
        if dss_ctl1.splitter_enable == 0:
            logging.error(f"Splitter bit of PIPE_DSS_CTL1_P{panel.pipe} disabled during workload")
            gdhm.report_driver_bug_di(f"{GDHM_MSO_COG} Splitter bit of PIPE disabled during workload")
            return False
    return True
