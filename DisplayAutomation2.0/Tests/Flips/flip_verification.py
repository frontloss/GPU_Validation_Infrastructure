##
# @file         flip_verification.py
# @brief        This script contains helper functions to verify AsyncFlips related features.
# @author       Sunaina Ashok

import logging
import math
from collections import OrderedDict
import csv
from Libs.Core import etl_parser
from Libs.Core.machine_info import machine_info
from registers.mmioregister import MMIORegister
from Tests.Flips import flip_helper
from Tests.Planes.Common import planes_verification

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1
platform = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
SIZE_OF_PROCESS_CONFIG_TABLE = 128
MAX_PLANES_PER_PIPE = 5
MAX_LINE_WIDTH = 64
MAX_PLANES = 3


##################
# Helper Functions
##################


##
# @brief            Helper function to verify SpeedFrame
# @param[in]        etl_file : Name of the ETL file to be verified
# @param[in]        pipe     : Pipe value
# @return           status   : True if Sync flips are present in ETL else False
def verify_speedframe(etl_file, pipe):
    logging.info(" SPEEDFRAME Feature Verification ".center(MAX_LINE_WIDTH, "*"))
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data('PIPE_' + pipe)

    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    is_async_flip = False
    for flip in flip_data:
        for plane_info in flip.PlaneInfoList:
            if "FlipImmediate" in plane_info.Flags:
                is_async_flip = True

    if is_async_flip:
        for flip in flip_data:
            for flipaddress in flip.FlipAddressList:
                if flipaddress.Async == True:
                    return False
    else:
        logging.warning("No Async Flips found")
        return True
    logging.info("Speed Frame is enabled : No Async flips are present")
    return True


##
# @brief            Helper function to verify ASync Flips
# @param[in]        etl_file : Name of the ETL file to be verified
# @param[in]        pipe     : Pipe value
# @return           status   : True if Async Flips are present else False
def verify_asyncflips(etl_file, pipe):
    logging.info(" ASync Flips Verification ".center(MAX_LINE_WIDTH, "*"))
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data('PIPE_' + pipe)

    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    is_async_flip = False
    for flip in flip_data:
        for plane_info in flip.PlaneInfoList:
            if "FlipImmediate" in plane_info.Flags:
                is_async_flip = True
    logging.info(f"Async Flips are {'Enabled' if is_async_flip else 'Disabled'}")
    return True if is_async_flip else False


##
# @brief            Helper function to verify Sync Flips
# @param[in]        etl_file      : Name of the ETL file to be verified
# @param[in]        pipe          : Pipe value
# @return           status        : True if sync Flips are present else False
def verify_syncflips(etl_file, pipe):
    logging.info(" Sync Flips Verification ".center(MAX_LINE_WIDTH, "*"))
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data('PIPE_' + pipe)

    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    is_async_flip = False
    for flip in flip_data:
        for plane_info in flip.PlaneInfoList:
            if "FlipImmediate" in plane_info.Flags:
                is_async_flip = True

    if is_async_flip:
        for flip in flip_data:
            for flipaddress in flip.FlipAddressList:
                if flipaddress.Async == True:
                    return False
    else:
        logging.warning("No ASync Flips found")
        return True
    logging.info("VSync On enabled : No Async flips are present")
    return True


##
# @brief            Helper function to verify_vsync_rate
# @param[in]        etl_file      : Name of the ETL file to be verified
# @param[in]        pipe          : Pipe value
# @param[in]        app_name      : app_name
# @return           status        : True if sync Flips are present else False
def verify_vsync_rate(etl_file, pipe, app_name):
    notify_log_buffer = OrderedDict()
    previous_timestamp = -1
    game_layer_index = -1
    mpo3flip_details = OrderedDict()
    ref_rate = 0

    logging.info(" Sync Flips Verification ".center(MAX_LINE_WIDTH, "*"))
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data('PIPE_' + pipe)
    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    ##
    # Get Process config data
    process_config_table_data = etl_parser.get_event_data(etl_parser.Events.PROCESS_CONFIG_TABLE)
    if process_config_table_data is None:
        logging.error("\tFAIL: Event process_config_table_data missing from ETL ")
        return False

    ##
    # Get Flip Process Details
    flip_process_data = etl_parser.get_event_data(etl_parser.Events.FLIP_PROCESS_DETAILS)
    if flip_process_data is None:
        logging.error("\tFAIL: Event flip_process_data missing from ETL ")
        return False

    ##
    # Get Layer Index for Plane ID data
    layer_index_plane_id_data = etl_parser.get_event_data(etl_parser.Events.HW_PLANE_LAYER_INDEX)
    if layer_index_plane_id_data is None:
        logging.error("\tFAIL: Event layer_index_plane_id_data missing from ETL ")
        return False

    ##
    # Get RR
    transcoder_data = etl_parser.get_event_data(etl_parser.Events.SYSTEM_DETAILS_TRANSCODER)
    if transcoder_data is not None:
        for transcoder in transcoder_data:
            ref_rate = transcoder.RR
        flip_time_ms = (1 / ref_rate) * 1000
    else:
        logging.error("FAIL: SYSTEM_DETAILS_TRANSCODER data missing from ETL ")
        return False

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(app_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")
            else:
                game_layer_index = each_flip_process.LayerIndex
                logging.debug(f"Flip Process Details, Process Name - {each_flip_process.ProcessName}, "
                              f" Process Flag - {each_flip_process.ProcessFlags}, "
                              f" Layer Index - {each_flip_process.LayerIndex}, Timestamp -{each_flip_process.TimeStamp}")

    start_time, end_time = get_feature_enable_timestamp(process_config_table_data)

    if platform in ['ELG', 'LNL']:
        # Create list of MPO3Flip data
        for plane_data in flip_data:
            if len(plane_data.PlaneInfoList) != 0:
                for mpo3flip in plane_data.PlaneInfoList:
                    if mpo3flip.LayerIndex == game_layer_index:
                        mpo3flip_details[mpo3flip.PresentId] = {}
                        mpo3flip_details[mpo3flip.PresentId][mpo3flip.LayerIndex] = mpo3flip.TimeStamp

        # Get NotifyVSyncLogBuffer data
        notify_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT,
                                                start_time=start_time, end_time=end_time)

        # Create a list of Notify log buffer data
        if notify_data is not None:
            for notify_log_buffer_ext in notify_data:
                if notify_log_buffer_ext.LayerIndex == game_layer_index:
                    notify_log_buffer[notify_log_buffer_ext.PresentID] = {}
                    notify_log_buffer[notify_log_buffer_ext.PresentID][notify_log_buffer_ext.LayerIndex] = \
                        notify_log_buffer_ext.TimeStamp

        for key, value in notify_log_buffer.items():
            present_id = key
            for layer, current_timestamp in value.items():
                if previous_timestamp == -1:
                    previous_timestamp = current_timestamp
                else:
                    difference = current_timestamp - previous_timestamp
                    previous_timestamp = current_timestamp
                    if abs(difference - flip_time_ms) <= 1:
                        logging.debug(f" VSync reporting is within RR of the Panel, Delta TS - {difference}, "
                                      f"Flip TS - {flip_time_ms} for PresentID - {notify_data[0]}")
                    else:
                        mpo3_current_timestamp = mpo3flip_details[present_id][layer]
                        mpo3_previous_timestamp = mpo3flip_details[present_id - 1][layer]
                        difference = mpo3_current_timestamp - mpo3_previous_timestamp
                        if abs(difference - flip_time_ms) <= 1:
                            logging.error(f"VSync reporting is not within RR of Panel. "
                                          f"Diff - {difference}, Flip time {flip_time_ms} for PresentID - {notify_data[0]}")
                            return False
                        else:
                            continue
        logging.info("VSync reporting is within RR of the Panel")
    else:
        logging.info("Verification is not enabled for PreLNL platforms")
    return True


##
# @brief            Helper function to verify Smooth Sync
# @param[in]        etl_file      : Name of the ETL file to be verified
# @param[in]        pipe          : Pipe value
# @param[in]        plane_id_list : Plane ID list
# @param[in]        start_time    : Start time for verification.
# @param[in]        end_time      : End time for verification.
# @return           status        : True if SmoothSync is enabled else False
def verify_smooth_sync(etl_file, pipe, plane_id_list=None, start_time=None, end_time=None):
    logging.info(" Smooth Sync Feature Verification ".center(MAX_LINE_WIDTH, "*"))

    test_app_list = ['FlipAt.exe', 'FlipModelD3D12.exe', 'Classic3DCubeApp.exe', 'ClassicD3D.exe', 'dota2.exe',
                     'gta5.exe', 'control_dx12.exe', 'MovingRectangleApp.exe']

    appevents = flip_helper.get_action_type("-APPEVENTS", True)
    scenario = flip_helper.get_action_type("-SCENARIO", True)

    plane_id = None
    status = True
    status &= verify_asyncflips(etl_file, pipe)
    if not status:
        return False

    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data(f'PIPE_{pipe}')
    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    flip_process_data = etl_parser.get_event_data(etl_parser.Events.FLIP_PROCESS_DETAILS)
    if flip_process_data is None:
        logging.error("\tFAIL: Event flip_process_data missing from ETL ")
        return False

    ##
    # Get Process config data
    process_config_table_data = etl_parser.get_event_data(etl_parser.Events.PROCESS_CONFIG_TABLE)
    if process_config_table_data is None:
        logging.error("\tFAIL: Event process_config_table_data missing from ETL ")
        return False

    start_time = None
    end_time = None
    toggled_timestamps = []
    for config_index in range(0, len(process_config_table_data) - 1):
        if process_config_table_data[config_index].Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION':
            toggled_timestamps.append(process_config_table_data[config_index].TimeStamp)
        if process_config_table_data[config_index].Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION' and \
                process_config_table_data[config_index + 1].Action == 'DD_PROCESS_ENTRY_ACTION_REMOVE':
            end_time = process_config_table_data[config_index + 1].TimeStamp

    # feature start time
    start_time = toggled_timestamps[0]

    start_end_pairs = []
    if len(toggled_timestamps) == 1:
        start_end_pairs.append((toggled_timestamps[0], end_time))
    else:
        if appevents == "FULLSCREEN_WINDOWED" or appevents == "VSYNCSWITCH":
            start_end_pairs.clear()
            threshold = 0
            if appevents == "FULLSCREEN_WINDOWED":
                threshold = 28          # fullscreen_windowed transition happens after 30secs
            elif appevents == "VSYNCSWITCH":
                threshold = 9           # vsync switch transition happens after 10secs
            for idx in range(0, len(toggled_timestamps) - 1):
                if toggled_timestamps[idx + 1] / 1000 - toggled_timestamps[idx] / 1000 > threshold:
                    start_end_pairs.append((toggled_timestamps[idx], toggled_timestamps[idx + 1]))
        elif appevents != "FULLSCREEN_WINDOWED":
            for timestamp_index in range(len(toggled_timestamps) - 1):
                previous_timestamp = round(round((toggled_timestamps[timestamp_index]) / 1000))
                next_timestamp = round(round((toggled_timestamps[timestamp_index + 1]) / 1000))
                if previous_timestamp not in range(next_timestamp - 2, next_timestamp + 2) and previous_timestamp > 5:
                    start_end_pairs.append((toggled_timestamps[timestamp_index], toggled_timestamps[timestamp_index + 1]))
            start_end_pairs.append((toggled_timestamps[len(toggled_timestamps) - 1], end_time))

    logging.debug(f"App toggled_timestamps: {toggled_timestamps}")
    logging.debug(f"Prepared start_end_pairs: {start_end_pairs}")

    if status:
        if plane_id_list is None:
            if not planes_verification.check_layer_reordering():
                logging.debug("layer reordering not required as Platform is D15+")
                for each_flip_process in flip_process_data:
                    if each_flip_process.ProcessName in test_app_list:
                        layer_index = each_flip_process.LayerIndex
                        if appevents == "WINDOWED" or appevents == "3DAPP_MEDIA" or scenario == "MODE_SWITCH" or scenario == "RESTART_DRIVER":
                            plane_id = MAX_PLANES - (layer_index + 1)
                            while len(start_end_pairs) != 1 and scenario != "MODE_SWITCH":
                                start_end_pairs.pop(0)
                        elif appevents == "FULLSCREEN" or appevents == "VSYNCSWITCH" or scenario == "POWER_EVENT_S3" or scenario == "POWER_EVENT_S4":
                            plane_id = MAX_PLANES - layer_index
                            while len(start_end_pairs) != 1 and appevents != "VSYNCSWITCH":
                                start_end_pairs.pop(0)

                if appevents == "VSYNCSWITCH":
                    for vsync_check in range(0, len(start_end_pairs)):
                        start_time = start_end_pairs[vsync_check][0]
                        end_time = start_end_pairs[vsync_check][1]
                        logging.debug(
                            f"Appevents: {appevents}: ON\n Feature will be Off, Skipping the verification !") if vsync_check % 2 == 0 else logging.debug(
                            f"Appevents: {appevents}: OFF")
                        if vsync_check % 2 != 0:
                            status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                            status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time,
                                                                        end_time)
                elif appevents != "FULLSCREEN_WINDOWED":
                    logging.debug(f"Appevents: {appevents}") if appevents is not None else logging.debug(
                        f"Scenario: {scenario}")
                    start_time = start_end_pairs[0][0]
                    end_time = start_end_pairs[0][1]
                    status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                    status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time, end_time)
                elif appevents == "FULLSCREEN_WINDOWED":
                    for fswd_check in range(0, len(start_end_pairs)):
                        # toggle the plane_ctl from 2-3 -> 1-2 (transition from FS to WD and back)
                        if fswd_check % 2 == 0:
                            plane_id = 2
                        else:
                            plane_id = 1
                        start_time = start_end_pairs[fswd_check][0]
                        end_time = start_end_pairs[fswd_check][1]
                        logging.debug(f"Appevents: FULLSCREEN") if fswd_check % 2 == 0 else logging.debug("Appevents: WINDOWED")
                        status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                        status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time,
                                                                    end_time)
            else:
                plane_id = 1
                if appevents == "FULLSCREEN_WINDOWED":
                    for fswd_check in range(0, len(start_end_pairs)):
                        start_time = start_end_pairs[fswd_check][0]
                        end_time = start_end_pairs[fswd_check][1]
                        logging.debug(f"Appevents: FULLSCREEN") if fswd_check % 2 == 0 else logging.debug("Appevents: WINDOWED")
                        status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                        status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time, end_time)
                elif appevents == "VSYNCSWITCH":
                    for vsync_check in range(0, len(start_end_pairs)):
                        start_time = start_end_pairs[vsync_check][0]
                        end_time = start_end_pairs[vsync_check][1]

                        logging.debug(
                            f"Appevents: {appevents}: ON\n Feature will be Off, Skipping the verification !") if vsync_check % 2 == 0 else logging.debug(
                            f"Appevents: {appevents}: OFF")
                        if vsync_check % 2 != 0:
                            status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                            status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time,
                                                                        end_time)
                else:
                    logging.debug(f"Appevents: {appevents}")
                    status &= plane_verification(str(plane_id), pipe, start_time, end_time)
                    status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time, end_time)
        else:
            for index in range(0, len(plane_id_list)):
                plane_id = plane_id_list[index][0]
                smooth_sync_status = plane_verification(str(plane_id), pipe, start_time, end_time)
                status &= smooth_sync_status
                if smooth_sync_status:
                    status &= verify_adjacent_smooth_sync_plane(str(plane_id + 1), pipe, start_time, end_time)
                else:
                    continue
    logging.info(f"Smooth Sync is {'Enabled' if status else 'Disabled'}")
    return True if status else False


##
# @brief         Helper function to verify plane
# @param[in]     plane_id : Plane id to be checked
# @param[in]     pipe     : Current pipe that is being used(A/B/C/D)
# @param[in]     start_timestamp : Start Timestamp
# @param[in]     end_timestamp   : End Timestamp
# @return        status   : True if Smooth sync back plane is enabled, False otherwise
def plane_verification(plane_id, pipe, start_timestamp=None, end_timestamp=None):
    logging.info(" Plane Verification ".center(MAX_LINE_WIDTH, "*"))
    logging.info(f"Start time: {start_timestamp}, End Time: {end_timestamp}")
    reg_name = "PLANE_CTL" + "_" + plane_id + "_" + pipe
    plane_ctl_instance = MMIORegister.get_instance("PLANE_CTL_REGISTER", reg_name, platform)
    flip_data = etl_parser.get_flip_data("PIPE_" + pipe, start_time=start_timestamp, end_time=end_timestamp)

    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl_instance.asUint = ctl_data.Data
            if (ctl_data.Offset == plane_ctl_instance.offset) and ctl_data.IsWrite:
                if plane_ctl_instance.plane_enable == 1:
                    logging.debug("Plane enable bit is enabled")
                    if plane_ctl_instance.smooth_sync_plane_enable == 0 and \
                            plane_ctl_instance.async_address_update_enable == 0:
                        logging.warning(f"Sync Flips on plane id {reg_name} during Back Plane check with timestamp "
                                        f"{ctl_data.TimeStamp / 1000}, Ignoring for verification")
                        continue
                    else:
                        logging.debug("Smooth Sync plane enable bit is enabled")
                        logging.info(f"Smooth Sync Back Plane enabled on plane id {reg_name}")
                        return True
                else:
                    logging.error(f"Plane enable bit is disabled - timestamp {ctl_data.TimeStamp}")
    logging.error(f"FAIL: Smooth Sync Back Plane disabled on plane id {reg_name}")
    return False


##
# @brief         Helper function to verify adjacent smooth sync plane
# @param[in]     plane_id : Plane id to be checked
# @param[in]     pipe     : Current pipe that is being used(A/B/C/D)
# @param[in]     start_timestamp : Start Timestamp
# @param[in]     end_timestamp   : End Timestamp
# @return        status   : True if plane is enabled without the smooth sync bit set; False, otherwise
def verify_adjacent_smooth_sync_plane(plane_id, pipe, start_timestamp=None, end_timestamp=None):
    logging.info(" Adjacent Smooth Sync Plane Verification ".center(MAX_LINE_WIDTH, "*"))
    logging.info(f"Start time: {start_timestamp}, End Time: {end_timestamp}")
    reg_name = "PLANE_CTL" + "_" + plane_id + "_" + pipe
    plane_ctl_instance = MMIORegister.get_instance("PLANE_CTL_REGISTER", reg_name, platform)
    flip_data = etl_parser.get_flip_data("PIPE_" + pipe, start_time=start_timestamp, end_time=end_timestamp)

    if flip_data is None:
        logging.warning("No flip data found in EtlParser Report")
        return False

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl_instance.asUint = ctl_data.Data
            # Plane should be enabled without the smooth sync bit set
            if (ctl_data.Offset == plane_ctl_instance.offset) and ctl_data.IsWrite:
                if plane_ctl_instance.plane_enable == 1:
                    logging.debug("Plane enable bit is enabled")
                    if plane_ctl_instance.smooth_sync_plane_enable == 1:
                        logging.debug("Smooth Sync plane enable bit is enabled")
                        logging.info(f"Smooth Sync Front Plane disabled on plane id {reg_name}, "
                                     f"timestamp {ctl_data.TimeStamp / 1000}")
                    else:
                        logging.debug("Smooth Sync plane enable bit is disabled")
                        logging.info(f"Smooth Sync Front Plane enabled on plane id {reg_name}")
                        return True
    logging.error(f"FAIL: Smooth Sync Front Plane disabled on plane id {reg_name}")
    return False


##
# @brief            Get FPS limit for EG
# @param[in]        eg_mode; EG mode that is set
# @return           Targeted FPS
def get_fps_limit(eg_mode):
    target_fps = []
    target_fps.append(60)
    target_fps.append(45)
    target_fps.append(30)
    actual_targeted_fps = 0

    rr = flip_helper.get_max_RR()

    if rr >= 60:
        if rr == 60:
            actual_targeted_fps = target_fps[eg_mode]
        else:
            actual_targeted_fps = math.floor(rr / round(rr / target_fps[eg_mode]))

    return actual_targeted_fps


##
# @brief         Verify Capped FPS
# @param[in]     etl_file      : ETL file path
# @param[in]     pipe          : Current pipe that is being used(A/B/C/D)
# @param[in]     plane_id_list : Plane id list
# @return        fps_capped if True else False
def verify_capped_fps(etl_file, pipe, plane_id_list):
    logging.info(" Capped FPS Feature Verification ".center(MAX_LINE_WIDTH, "*"))
    start_timestamp = None
    end_timestamp = None

    # Iterate plane_id_list to get the start and end timestamp of feature enabled
    for index in range(0, len(plane_id_list)):
        start_timestamp = plane_id_list[index][1]
        if index >= len(plane_id_list) - 1:
            end_timestamp = None
        else:
            end_timestamp = plane_id_list[index + 1][1]

    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data("PIPE_" + pipe, start_time=start_timestamp, end_time=end_timestamp)
    if flip_data is None:
        logging.error("\t\tFAIL: No Flip data found")
        return False
    logging.info("\t\tNumber of incoming flips: {0}".format(len(flip_data)))

    vbi_data = etl_parser.get_vbi_data("PIPE_" + pipe, start_timestamp, end_timestamp)
    if vbi_data is None:
        logging.error("\t\tFAIL: No VBI data found")
        return False
    logging.info("\t\tNumber of VBIs reported to OS: {0}".format(len(vbi_data)))

    vbi_flip_mapping = {}  # Holds vbi & flip mapping per layer { vbi_time_stamp : { layer_index : [flip_time_stamps]}}
    pos = 0
    first_vbi_timestamp = None
    last_vbi_timestamp = None
    # Segregating the flips per layer per vbi
    for vbi in vbi_data:
        vbi_flip_mapping[vbi.TimeStamp] = {}
        if first_vbi_timestamp is None:
            first_vbi_timestamp = vbi.TimeStamp
        last_vbi_timestamp = vbi.TimeStamp
        for index in range(pos, len(flip_data)):
            # If the flip being processed is after vbi, then break fo the current iteration tagging to vbi
            if flip_data[index].TimeStamp > vbi.TimeStamp:
                break
            # Flip data for each layer index, do the vbi & flip mapping
            for layer_flip in flip_data[index].PlaneInfoList:
                if layer_flip.LayerIndex not in vbi_flip_mapping[vbi.TimeStamp].keys():
                    vbi_flip_mapping[vbi.TimeStamp][layer_flip.LayerIndex] = [flip_data[index].TimeStamp]
                else:
                    vbi_flip_mapping[vbi.TimeStamp][layer_flip.LayerIndex].append(flip_data[index].TimeStamp)
            pos += 1

    # Check that no. of VBI are less than or equal to RR
    vbi_num = round(len(vbi_data) * 1000 / (last_vbi_timestamp - first_vbi_timestamp), 0)
    logging.info("\t\tNumber of VBIs per second= {0}".format(vbi_num))

    # Print the VBI(s) where multiple flips are coming (violating CFPS logic)
    fps_capped = True
    flip_capped_status = [None for _ in range(MAX_PLANES_PER_PIPE)]
    for vbi, flip_info in sorted(vbi_flip_mapping.items()):
        for layer_index, flip in sorted(flip_info.items()):
            if len(flip) > 1:
                if flip_capped_status[layer_index] is not None:
                    logging.info(
                        "\t\tVBI - {0}ms: {1} flips are seen for layer {2} -> {3} "
                        "({4} flips were seen in previous VBI -> {5})".format(
                            vbi, len(flip), layer_index, flip,
                            len(flip_capped_status[layer_index]), flip_capped_status[layer_index]))
                    fps_capped = False
                else:
                    logging.info("\t\tVBI - {0}ms: {1} flips are seen for layer {2} -> {3} ".format(
                        vbi, len(flip), layer_index, flip))
                flip_capped_status[layer_index] = flip
            else:
                flip_capped_status[layer_index] = None
        # Clear the tagging for the layers which are not involved in current vbi
        for plane in range(MAX_PLANES_PER_PIPE):
            if plane not in flip_info.keys():
                flip_capped_status[plane] = None

    if fps_capped:
        logging.info("\t\tFPS is capped (there are NO consecutive 2 flips or more than 2 flips in single VBI)")
    else:
        logging.warning("\t\tFPS is NOT capped (there are consecutive 2 flips or more than 2 flips in single VBI)")

    return fps_capped


##
# @brief            To verify Frame Limiting.
# @param[in]        etl_file; name of the ETL file to be verified.
# @param[in]        pipe; Pipe value.
# @return           True if Frame limiting verification passes.
def verify_frame_limiting(etl_file, pipe):
    pass
    ##
    # To be used for Frame limiting with minor changes
    # feature_status = []
    # start_time = 0
    # end_time = 0
    # eg_mode = []
    # plane_entry = []
    # plane_notify = {}
    # start_found = False
    # end_found = False
    # previous_flip_done = 0
    # if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
    #     logging.error("Failed to generate EtlParser report")
    #     return False
    #
    # pipe = 'PIPE_' + pipe
    # feature_data = etl_parser.get_event_data(etl_parser.Events.FEATURE_STATUS)
    #
    # for feature in feature_data:
    #     if feature.Feature == 'DD_DIAG_FEATURE_ENDURANCE_GAMING':
    #         if start_found is False and feature.Enable is True:
    #             start_found = True
    #             start_time = feature.TimeStamp
    #             eg_mode = feature.Param1
    #         elif start_found is True and feature.Enable is False:
    #             end_found = True
    #             end_time = feature.TimeStamp
    #
    #         if start_found is True and end_found is True:
    #             feature_status.append((start_time / 1000, eg_mode, end_time / 1000))
    #             start_found = False
    #             end_found = False
    #
    # if start_found is True and end_found is False:
    #     feature_status.append((start_time / 1000, eg_mode, None))
    #
    # for index in range(0, len(feature_status)):
    #     target_fps = get_fps_limit(feature_status[index][1])
    #     frame_limiter = (1 / target_fps) * 1000
    #
    #     flip_data = etl_parser.get_flip_data(pipe, start_time=feature_status[index][0],
    #                                          end_time=feature_status[index][2])
    #     if flip_data is None:
    #         continue
    #
    #     for flip in flip_data:
    #         for plane_info in flip.PlaneInfoList:
    #             if "FlipImmediate" in plane_info.Flags:
    #                 plane_entry.append((plane_info.PresentId, plane_info.TimeStamp))
    #
    #         for vsync_info in flip.NotifyVSyncLayerList:
    #             if vsync_info.PresentID in plane_notify.keys():
    #                 plane_notify[vsync_info.PresentID].append(vsync_info.TimeStamp)
    #             else:
    #                 plane_notify[vsync_info.PresentID] = []
    #                 plane_notify[vsync_info.PresentID].append(vsync_info.TimeStamp)
    #
    #     for plane_index in range(0, len(plane_entry)):
    #         if plane_entry[plane_index][0] in plane_notify.keys():
    #             logging.info("Present id {}".format(plane_entry[plane_index][0]))
    #             current_flip_done = plane_notify[plane_entry[plane_index][0]][0]
    #             if previous_flip_done != 0:
    #                 if current_flip_done - previous_flip_done < frame_limiter:
    #                     logging.debug("Verification successful. Time difference {} Frame limiter {}"
    #                                   .format((current_flip_done - previous_flip_done), frame_limiter))
    #                 else:
    #                     logging.error("Verification failed. Time difference {} Frame limiter {}"
    #                                   .format((current_flip_done - previous_flip_done), frame_limiter))
    #             previous_flip_done = current_flip_done


##
# @brief            To verify Endurance Gaming.
# @param[in]        etl_file; name of the ETL file to be verified.
# @param[in]        pipe; Pipe value.
# @param[in]        eg_parameters; EG Mode passed from the command line and RR from the scenario
# @return           True if EG is enabled and FPS is getting limited as per EG mode applied.
def verify_endurance_gaming(etl_file, pipe, eg_parameters):
    logging.debug("FUNC_ENTRY: verify_endurance_gaming ")
    logging.info(" Verification Start".center(64, "*"))
    eg_mode = eg_parameters[0]
    refresh_rate = eg_parameters[1]
    is_vrr_supported = eg_parameters[2]
    actual_fps = get_fps_from_presentmon_logs(flip_helper.PRESENTMON_LOG_PATH)
    logging.info(f"FPS captured from PresentMon: {actual_fps}")
    expected_fps = eg_expected_fps(refresh_rate, eg_mode, is_vrr_supported)
    expected_fps_range = range(expected_fps - 3, expected_fps + 4)
    logging.info(f"Expected FPS (EG- {eg_mode}, RR- {refresh_rate}): {expected_fps_range}")
    if (actual_fps in expected_fps_range) is False:
        logging.error(
            f"EG Verification Failed, Actual FPS: {actual_fps} is not meeting the Expected FPS range: {expected_fps_range}")
        logging.debug("FUNC_EXIT: verify_endurance_gaming ")
        return False
    else:
        logging.info(
            f"EG Verification Passed, Actual FPS: {actual_fps} is meeting the Expected FPS range: {expected_fps_range}")
        logging.debug("FUNC_EXIT: verify_endurance_gaming ")
        return True


##
# @brief            Get feature enable timestamp.
# @param[in]        process_config_table_data: Process config table entry.
# @return           Start and End time of feature.
def get_feature_enable_timestamp(process_config_table_data):
    start_time = None
    end_time = None
    for config_index in range(0, len(process_config_table_data) - 1):
        if process_config_table_data[config_index].Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION' and \
                process_config_table_data[config_index + 1].Action == 'DD_PROCESS_ENTRY_ACTION_REMOVE':
            start_time = process_config_table_data[config_index].TimeStamp
            end_time = process_config_table_data[config_index + 1].TimeStamp

    return start_time, end_time


##
# @brief            Verify Per Process Gaming Features.
# @param[in]        etl_file; name of the ETL file to be verified.
# @param[in]        game_name; Game name.
# @param[in]        game_setting; Per_Game Gaming Feature Setting.
# @return           True if verification is pass else False.
def verify_per_process(etl_file, game_name, game_setting):
    logging.info(" Per Process Verification ".center(MAX_LINE_WIDTH, "*"))
    process_data = []
    plane_id_list = []
    pipe_list = []
    game_layer_index = -1
    timestamp = 0
    valid_entries = 0
    add_count, remove_count = 0, 0
    update_flip_count = 0
    process_id = 0

    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ##
    # Get Process config data
    process_config_table_data = etl_parser.get_event_data(etl_parser.Events.PROCESS_CONFIG_TABLE)
    if process_config_table_data is None:
        logging.error("\tFAIL: Event process_config_table_data missing from ETL ")
        return False

    ##
    # Get Flip Process Details
    flip_process_data = etl_parser.get_event_data(etl_parser.Events.FLIP_PROCESS_DETAILS)
    if flip_process_data is None:
        logging.error("\tFAIL: Event flip_process_data missing from ETL ")
        return False

    ##
    # Get Layer Index for Plane ID data
    layer_index_plane_id_data = etl_parser.get_event_data(etl_parser.Events.HW_PLANE_LAYER_INDEX)
    if layer_index_plane_id_data is None:
        logging.error("\tFAIL: Event layer_index_plane_id_data missing from ETL ")
        return False

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(game_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")
            else:
                process_id = each_flip_process.ProcessId
                logging.debug(f"Flip Process Details, Process Name - {each_flip_process.ProcessName},"
                              f" Process ID - {each_flip_process.ProcessId}, "
                              f" Process Flag - {each_flip_process.ProcessFlags}, "
                              f" Layer Index - {each_flip_process.LayerIndex}, Timestamp -{each_flip_process.TimeStamp}")

    ##
    # Validate Process Config Table Entry
    for each_process_config in process_config_table_data:
        if valid_entries < each_process_config.NumValidEntries:
            valid_entries = each_process_config.NumValidEntries
        if each_process_config.ProcessId == process_id:

            # Check if Action is Read, then continue to check for next entry in ProcessConfigTable
            if each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_READ':
                continue

            ##
            # Verify Gaming mode when action is add
            logging.debug("Verify Gaming mode when action is add")
            if each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_ADD':
                if flip_helper.get_gaming_sync_mode_name(game_setting) != each_process_config.GamingSyncMode:
                    logging.error(f"Gaming mode is not matching with expected mode Applied "
                                  f"{each_process_config.GamingSyncMode} Expected "
                                  f"{flip_helper.get_gaming_sync_mode_name(game_setting)}")
                logging.info(f"Gaming mode is matching with expected mode Applied "
                             f"{each_process_config.GamingSyncMode} Expected"
                             f" {flip_helper.get_gaming_sync_mode_name(game_setting)}")
                add_count = add_count + 1
            process_data.append((each_process_config.GamingSyncMode, each_process_config.FlipSubmissionDone,
                                 each_process_config.Action))

            ##
            # Check if Action is Update flip submission when Gaming feature is applied with FlipSubmissionDone as True
            logging.debug("Verify Gaming mode when action is update flip submission")
            if (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION') \
                    and (each_process_config.FlipSubmissionDone == 'True'):
                logging.info(f"Gaming Feature - {each_process_config.GamingSyncMode} is set during timestamp "
                             f"- {each_process_config.TimeStamp}")
                logging.debug(f" ProcessName - {each_process_config.ProcessName}, "
                              f" ProcessId - {each_process_config.ProcessId}, "
                              f" GamingSyncMode - {each_process_config.GamingSyncMode}, "
                              f" HeadIndex - {each_process_config.HeadIndex}, "
                              f" RefCount - {each_process_config.RefCount}, "
                              f" FlipSubmissionDone - {each_process_config.FlipSubmissionDone}, "
                              f" Action - {each_process_config.Action}")
            elif (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_REF_COUNT') and \
                    (each_process_config.FlipSubmissionDone == 'True'):
                logging.info(f"Gaming Feature - {each_process_config.GamingSyncMode} reference count updated "
                             f"during timestamp - {each_process_config.TimeStamp}")
                logging.debug(f" ProcessName - {each_process_config.ProcessName}, "
                              f" ProcessId - {each_process_config.ProcessId}, "
                              f" GamingSyncMode - {each_process_config.GamingSyncMode}, "
                              f" HeadIndex - {each_process_config.HeadIndex}, "
                              f" RefCount - {each_process_config.RefCount}, "
                              f" FlipSubmissionDone - {each_process_config.FlipSubmissionDone}, "
                              f" Action - {each_process_config.Action}")
            else:
                logging.error(f"Gaming Feature - "f"{each_process_config.GamingSyncMode} is not set during "
                              f"timestamp {each_process_config.TimeStamp}")
                logging.error(f" ProcessConfigTable: ProcessName - {each_process_config.ProcessName}, "
                              f" ProcessId - {each_process_config.ProcessId}, "
                              f" GamingSyncMode - {each_process_config.GamingSyncMode}, "
                              f" HeadIndex - {each_process_config.HeadIndex}, "
                              f" RefCount - {each_process_config.RefCount}, "
                              f" FlipSubmissionDone - {each_process_config.FlipSubmissionDone}, "
                              f" Action - {each_process_config.Action}")

            ##
            # Verify Gaming mode when action is remove / update reference count
            logging.debug("Verify Gaming mode when action is remove / update reference count")
            if (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_REMOVE') or \
                    (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_REF_COUNT'):
                if each_process_config.GamingSyncMode != 'DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT':
                    logging.error(f"Gaming mode is not matching with expected mode Applied "
                                  f"{each_process_config.GamingSyncMode} Expected "
                                  f"DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT with Action {each_process_config.Action}")
                logging.info(f"Gaming mode is matching with expected mode Applied "
                             f"{each_process_config.GamingSyncMode} Expected "
                             f"DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT with Action {each_process_config.Action}")
                remove_count = remove_count + 1

            process_data.append((each_process_config.GamingSyncMode, each_process_config.FlipSubmissionDone,
                                 each_process_config.Action))

    for flip_sub_event in process_data:
        if flip_sub_event[2] == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION':
            logging.info(f"Gaming {flip_sub_event[0]} Feature is enabled, flips received from "
                         f"game/app")
            update_flip_count += 1
        else:
            continue

    if update_flip_count == 0:
        logging.error(f"Gaming Feature is not enabled, we did not get Mpo3Flip call for game/app")
        return False

    if add_count != remove_count:
        logging.warning(f"Add and remove counts are not matching Add Count - {add_count} Remove Count - {remove_count}")

    if valid_entries > SIZE_OF_PROCESS_CONFIG_TABLE:
        logging.warning(f"Exceeded process config table entry size, Value: {valid_entries}")

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(game_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")
            else:
                game_layer_index = each_flip_process.LayerIndex
                logging.debug(f"Flip Process Details, Process Name - {each_flip_process.ProcessName}, "
                              f" Process Flag - {each_flip_process.ProcessFlags}, "
                              f" Layer Index - {each_flip_process.LayerIndex}, Timestamp -{each_flip_process.TimeStamp}")

    for hw_plane_layer in layer_index_plane_id_data:
        if hw_plane_layer.LayerIndexMap == game_layer_index:
            plane_id_list.append((hw_plane_layer.LayerIndexMap, hw_plane_layer.TimeStamp, hw_plane_layer.PipeId))
            if hw_plane_layer.PipeId not in pipe_list:
                pipe_list.append(hw_plane_layer.PipeId)

    start_time, end_time = get_feature_enable_timestamp(process_config_table_data)

    if verify_gaming_feature(etl_file, game_setting, pipe_list, plane_id_list, start_time, end_time) is True:
        logging.info(f"Per Process Gaming Feature - {game_setting} verified for Game/App - {game_name}")
        return True
    else:
        logging.error(f"Per Process Gaming Feature Verification failed - {game_setting} Game/App - {game_name}")
        return False


##
# @brief            Verify Gaming Features for Per Process.
# @param[in]        etl_file      : Name of the ETL file to be verified.
# @param[in]        game_setting  : Per Game Gaming Feature.
# @param[in]        pipe_list     : Global Gaming Feature Setting.
# @param[in]        plane_id_list : Per Game Gaming Feature Setting.
# @param[in]        start_time    : Start time for verification.
# @param[in]        end_time      : End time for verification.
# @return           True if verification is pass else False.
def verify_gaming_feature(etl_file, game_setting, pipe_list, plane_id_list, start_time, end_time):
    status = False

    for pipe in pipe_list:
        pipe = chr(int(pipe) + 65)
        if flip_helper.get_gaming_sync_mode_name(game_setting) == 'DD_GAMING_SYNC_MODE_SMOOTH_SYNC':
            status = verify_smooth_sync(etl_file, pipe, plane_id_list, start_time, end_time)
        elif flip_helper.get_gaming_sync_mode_name(game_setting) == 'DD_GAMING_SYNC_MODE_VSYNC_ON':
            status = verify_syncflips(etl_file, pipe)
        elif flip_helper.get_gaming_sync_mode_name(game_setting) == 'DD_GAMING_SYNC_MODE_VSYNC_OFF':
            status = verify_asyncflips(etl_file, pipe)
        elif flip_helper.get_gaming_sync_mode_name(game_setting) == 'DD_GAMING_SYNC_MODE_CAPPED_FPS':
            status = verify_capped_fps(etl_file, pipe, plane_id_list)
        elif flip_helper.get_gaming_sync_mode_name(game_setting) == 'DD_GAMING_SYNC_MODE_SPEED_FRAME':
            status = verify_speedframe(etl_file, pipe)

    return status


##
# @brief            Verify Flip Latency.
# @param[in]        etl_file    : Name of the ETL file to be verified.
# @param[in]        pipe       : pipe object.
# @return           True if verification is pass else False.
def verify_flip_latency(etl_file, pipe):
    global scanlines
    logging.info(" Async Flip Latency Verification ".center(MAX_LINE_WIDTH, "*"))
    mpo3flip_details = []
    notify_vsync_details = OrderedDict()
    timestamp_diff = []
    vtotal, htotal, rr = 0, 0, 0
    pixel_clock = 0
    index = 0

    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ##
    # Get Flip data
    flip_data = etl_parser.get_flip_data(f"PIPE_{pipe}")

    if flip_data is None:
        logging.error("\tFAIL: flip_data missing from ETL ")
        return False

    transcoder_data = etl_parser.get_event_data(etl_parser.Events.SYSTEM_DETAILS_TRANSCODER)
    if transcoder_data is not None:
        for transcoder in transcoder_data:
            vtotal = transcoder.VTotal
            htotal = transcoder.HTotal
            rr = transcoder.RR
        pixel_clock = vtotal * htotal * rr
        logging.info(f"VTotal - {vtotal}, HTotal - {htotal}, RR - {rr}, Pixel Clock - {pixel_clock}")
    else:
        logging.error("FAIL: system details transcoder data missing from ETL ")
        return False

    ##
    # Get Notify VSync data
    for plane_data in flip_data:
        if platform in machine_info.PRE_GEN_15_PLATFORMS:
            if len(plane_data.NotifyVSyncLayerList) != 0:
                for notify_data in plane_data.NotifyVSyncLayerList:
                    if notify_data.PresentID not in notify_vsync_details:
                        notify_vsync_details[notify_data.PresentID] = notify_data.TimeStamp / 1000

        ##
        # Get Plane Info List data
        if len(plane_data.PlaneInfoList) != 0:
            for mpo3flip in plane_data.PlaneInfoList:
                mpo3flip_details.append((mpo3flip.Flags, mpo3flip.PresentId, (mpo3flip.TimeStamp / 1000)))

    if len(notify_vsync_details) == 0:
        notify_vsync_log_buffer_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT)
        if notify_vsync_log_buffer_data is not None:
            for notify_log_buffer_ext in notify_vsync_log_buffer_data:
                notify_vsync_details[notify_log_buffer_ext.PresentID] = notify_log_buffer_ext.TimeStamp / 1000

    mpo3flip_present_id_time = [tup[1:3] for tup in mpo3flip_details]

    for notify_present_id, notify_timestamp in notify_vsync_details.items():
        # logging.debug(f"Notify data PresentID {notify_present_id} Time {notify_timestamp}")
        mpo3_present_id = mpo3flip_present_id_time[index][0]
        if notify_present_id < mpo3_present_id:
            continue
        elif notify_present_id > mpo3_present_id:
            continue
        else:
            timestamp_diff.append(notify_timestamp - mpo3flip_present_id_time[index][1])
            # logging.debug(f"Notify PresentID {notify_present_id} MPO3 PresentID {mpo3flip_present_id_time[index][0]}")
            index = index + 1

    logging.debug(f"TimeStamp difference between Flip-NotifyVSync for respective PresentID's - {sum(timestamp_diff)}")
    average_diff = (sum(timestamp_diff) / len(timestamp_diff))
    logging.debug(f"Avg TimeStamp in mS between Flip-NotifyVSync - {average_diff / 1000}mS ")
    logging.info(f"Avg TimeStamp in S between Flip-NotifyVSync - {average_diff}S ")

    # one line time  = HTotal / Pixel_Clock = 1 / (VTotal * RR)
    if pixel_clock != 0:
        one_line_time = 1 / (rr * vtotal)
        logging.info(f"one_line_time - {one_line_time} ")
        # need to divide the flip delay time with the line time
        scanlines = (average_diff / one_line_time)
        logging.info(f"Average Scanlines - {scanlines}")
    else:
        logging.error("Failed to fetch VTotal and pixel clock")
        return False

    scanline_threshold = 30 if platform in ['ELG'] else 20

    if scanlines > scanline_threshold:
        logging.error(f"Avg Scanlines are greater than {scanline_threshold} lines, Flip-NotifyVSync is taking "
                      f"{scanlines} lines")
        return False

    logging.info(f"Avg Scanlines are less than {scanline_threshold} lines, Flip-NotifyVSync is taking {scanlines} "
                 f"lines")
    return True


##
# @brief            Calculate the average fps from the presentmon log.
# @param[in]        file_path    : presentmon log file path.
# @return           avg_fps.
def get_fps_from_presentmon_logs(file_path):
    logging.debug("FUNC_ENTRY: get_fps_from_presentmon_logs ")
    try:
        with open(rf"{file_path}", "r") as file:
            csvfile = csv.reader(file)
            avg_fps = 0
            no_of_samples = 0
            for sample in csvfile:
                if sample[9] != 'FrameTime':
                    avg_fps += float(sample[9])
                    no_of_samples += 1
            fps = round(1000 / (avg_fps / no_of_samples))
            logging.info(f"FPS captured from PresentMon: {fps}")
            logging.debug("FUNC_EXIT: get_fps_from_presentmon_logs ")
            return fps
    except Exception as e:
        logging.error(f"Exception occurred: {e}")


##
# @brief            Gets the expected FPS from the EG perspective.
# @param[in]        refresh_rate    : Refresh rate of the panel.
# @param[in]        eg_mode    : EG Mode in which the app is running.
# @param[in]        is_vrr_supported    : true if vrr is supported, else false.
# @return           expected FPS range.
def eg_expected_fps(refresh_rate, eg_mode, is_vrr_supported):
    logging.debug("FUNC_ENTRY: eg_expected_fps ")
    expected_fps = None
    target_fps = {"MAXIMUM_BATTERY": 30, "BALANCED": 40, "BETTER_PERFORMANCE": 60}

    if is_vrr_supported:
        if 47 <= refresh_rate < 61:
            if eg_mode == "MAXIMUM_BATTERY":
                expected_fps = 30
            if eg_mode == "BALANCED":
                expected_fps = 48
            if eg_mode == "BETTER_PERFORMANCE":
                expected_fps = 60
        else:
            expected_fps = target_fps[eg_mode]

    if refresh_rate in range(58, 62):
        refresh_rate = 60
    elif refresh_rate in range(88, 92):
        refresh_rate = 90
    elif refresh_rate in range(118, 122):
        refresh_rate = 120
    elif refresh_rate in range(142, 146):
        refresh_rate = 144
    elif refresh_rate in range(163, 167):
        refresh_rate = 165
    elif refresh_rate in range(238, 242):
        refresh_rate = 240

    if refresh_rate >= 60 and not is_vrr_supported:
        expected_fps = math.floor(refresh_rate / math.floor(refresh_rate / target_fps[eg_mode]))
    logging.info(f"Expected FPS: {expected_fps}")
    logging.debug("FUNC_ENTRY: eg_expected_fps ")
    return expected_fps