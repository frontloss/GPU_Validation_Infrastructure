##
# @file         flipq_helper.py
# @brief        The script consists of helper functions for OS based FlipQ testing.
# @author       Anjali Shetty

import logging
import os
import subprocess
import sys
import time
from collections import OrderedDict

from Libs.Core import etl_parser, registry_access, winkb_helper, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Tests.FlipQ.flipq_base import flip_base
from registers.mmioregister import MMIORegister

config = DisplayConfiguration()

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1

##
# 7ms delay from CCD to HAL layer + Additional wait for 1 frame
SCANLINE_MODE_WAIT = 0.007000 + 0.016000

##
# FlipQ depth
SIMPLE_FLIPQ_DEPTH = 8

##
# No of layers per pipe
NO_OF_LAYERS = 3


###########
# Generic #
###########

##
# @brief        Helper function to get action type
# @param[in]    argument : Command line tag
# @return       argument value
def get_action_type(argument):
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if argument in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == argument:
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        raise Exception("Incorrect command line")


##
# @brief        Helper function to start ETL capture
# @param[in]    file_name : ETL file name
# @return       status    : True if ETL started otherwise False
def start_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture.
# @param[in]    file_name     : ETL file name
# @return       etl_file_path : Path of ETL file captured
def stop_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after playback")
    return etl_file_path


#########################
# Media and App Related #
#########################

##
# @brief        Helper function get media file
# @param[in]    content_type : Type of media content
# @return       media content path
def get_media_file(content_type):
    return {
        '24FPS': os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos/24.000.mp4"),
        '60FPS': os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")
    }[content_type]


##
# @brief        Helper function play and close media
# @param[in]    play       : Boolean flag to indicate play or close media
# @param[in]    fullscreen : Boolean flag to indicate fullscreen or windowed media playback
# @return       media handle
def play_close_media(play, fullscreen=True):
    if play:
        ##
        # Get media file path
        media_file = get_media_file(flip_base.content_type)

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Play media content in windowed mode
        media_handle = flip_base.mpo_helper.play_media(media_file, fullscreen)

        ##
        # Enable repeat
        winkb_helper.press("CTRL+T")

        return media_handle

    else:
        ##
        # Close media player
        window_helper.close_media_player()
        logging.info("Closed media application")


##
# @brief        Helper function to minimise and maximise media application
# @return       status of function
def media_max_min():
    ##
    # Minimize video playback window
    winkb_helper.press('WIN+D')
    logging.info("Minimized the window")

    ##
    # Wait for 10 seconds after minimize
    time.sleep(10)

    ##
    # Maximize video playback window
    winkb_helper.press('WIN+D')
    logging.info("Maximized the window")

    ##
    # Wait for 10 seconds after maximizing
    time.sleep(10)

    return True


##
# @brief        Helper function to switch between media and desktop
# @return       status of function
def media_window_switch():
    ##
    # Switch to fullscreen
    winkb_helper.press('ALT_ENTER')
    logging.info("Switched to fullscreen")

    ##
    # Wait for a minute after switching to fullscreen
    time.sleep(60)

    ##
    # Switch to windowed mode
    winkb_helper.press('ALT_ENTER')
    logging.info("Switched to windowed mode")

    ##
    # Wait for a minute after switching to windowed mode
    time.sleep(60)

    return True


##
# @brief        Helper function to close and open media
# @return       status of function
def media_close_open():
    ##
    # Close media player
    window_helper.close_media_player()
    logging.info("Closed media player")

    ##
    # Wait for 10 seconds after close
    time.sleep(10)

    ##
    # Play media in windowed mode
    play_close_media(True, False)

    return True


##
# @brief        Helper function to play and pause media
# @return       status of function
def media_play_pause():
    ##
    # Pause video
    winkb_helper.press(' ')
    logging.info("Paused the video")

    ##
    # Wait for 10 seconds after pause
    time.sleep(10)

    ##
    # Play video
    winkb_helper.press(' ')
    logging.info("Continue playing the video")

    ##
    # Wait for 10 seconds after play
    time.sleep(10)

    return True


##
# @brief        Helper function to perform media cancel event
# @param[in]    action : Different media actions to be performed
# @return       status : Status of the event performed
def perform_media_cancel_event(action):
    event = {
        'MAX_MIN': media_max_min,
        'CLOSE_OPEN': media_close_open,
        'WINDOW_SWITCH': media_window_switch,
        'PLAY_PAUSE': media_play_pause
    }
    status = event.get(action)
    return status()


##
# @brief        Helper function to minimise and maximise 3D App
# @param[in]    app    : App handle
# @return       status : Status of function
def max_min_3d_app(app):
    ##
    # Minimize 3D window
    winkb_helper.press('WIN+D')
    logging.info("Minimized the window")

    ##
    # Wait for 10 seconds after minimize
    time.sleep(10)

    ##
    # Maximize 3D window
    winkb_helper.press('WIN+D')
    logging.info("Maximized the window")

    ##
    # Wait for 10 seconds after maximizing
    time.sleep(10)

    return True


##
# @brief        Helper function to open and close 3D app
# @param[in]    app    : App handle
# @return       status : Status of function
def close_open_3d_app(app):
    ##
    # Close 3D application
    app.terminate()
    logging.info("Closed 3D application")

    ##
    # Wait for 10 seconds after closing the 3D application
    time.sleep(10)

    ##
    # Open 3D Application
    app = \
        subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:' + flip_base.interval +
                         'buffers:' + flip_base.buffer)
    if app is not None:
        logging.info("Successfully launched 3D application")
    else:
        raise Exception("Failed to launch 3D application")

    ##
    # Wait for 10 seconds after launching the 3D application
    time.sleep(10)

    app.terminate()

    return True


##
# @brief        Helper function to switch between 3D app and Desktop
# @param[in]    app    : App handle
# @return       status : Status of function
def window_switch_3d_app(app):
    ##
    # Switch to fullscreen
    winkb_helper.press('F5')
    logging.info("Switched to fullscreen")

    ##
    # Wait for a minute after switching to fullscreen
    time.sleep(60)

    ##
    # Switch to windowed mode
    winkb_helper.press('F5')
    logging.info("Switched to windowed mode")

    ##
    # Wait for a minute after switching to windowed mode
    time.sleep(60)

    return True


##
# @brief        Helper function to perform 3D application cancel event
# @param[in]    action : Different 3D cancel actions to be performed
# @return       status : Status of the event performed
def perform_3d_app_cancel_event(action):
    return {
        'MAX_MIN': max_min_3d_app,
        'CLOSE_OPEN': close_open_3d_app,
        'WINDOW_SWITCH': window_switch_3d_app
    }.get(action)


##################
# GDHM Reporting #
##################

##
# @brief            Helper function to report GDHM
# @param[in]        message    : GDHM message
# @param[in]        priority   : Priority of the GDHM bug [P1/P2/P3/P4]
# @param[in]        driver_bug : True for driver bug reporting else False
# @return           None
def report_to_gdhm(message="", priority='P2', driver_bug=True):
    if message == "":
        title = f"[Display_OS_Features][Display_Planes][SFLIPQ] verification failed"
    else:
        title = f"[Display_OS_Features][Display_Planes][SFLIPQ] {message}"
    if driver_bug:
        gdhm.report_driver_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
    else:
        gdhm.report_test_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))


#################################
# FlipQ Helper and Verification #
#################################

##
# @brief        Helper function to check status of OS FlipQ
# @return       OS FlipQ status
def os_flipq_enable_status():
    flipq_enable_status = 0
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    registry_value, registry_type = registry_access.read(args=ss_reg_args, reg_name="DisplayFeatureControl2")
    if registry_value is not None:
        flipq_enable_status = registry_value & 0x1

    return flipq_enable_status


##
# @brief        Helper function to remove cancelled flip from flip data
# @param[in]    flip_data                       : Flip data to be updated with cancelled flips
# @param[in]    set_interrupt_target_present_id : Set interrupt data to be updated with cancelled flips
# @param[in]    current_pipe                    : Display pipe details
# @return       status                          : False if incorrect present id is cancelled, else True
def remove_cancelled_flip(flip_data, set_interrupt_target_present_id, current_pipe):
    cancel_flip_data = []

    ##
    # Get Cancel flip data.
    cancel_flip = etl_parser.get_event_data(etl_parser.Events.CANCEL_FLIP)

    ##
    # Check if there is any cancel entries in the ETL.
    if cancel_flip is not None:
        ##
        # Create a list of cancel entries.
        for cancel in cancel_flip:
            cancel_flip_data.append((cancel.SourceId, cancel.LayerIndex, cancel.PresentIdCancelRequested,
                                     cancel.PresentIdCancelled, cancel.TimeStamp))
    ##
    # Update Flip data based on cancel request.
    for cancel_data in cancel_flip_data:
        source_id = cancel_data[0]
        ##
        # Check for each pipe
        if source_id == (ord(current_pipe) - 65):
            requested_present_id = cancel_data[2]
            cancelled_present_id = cancel_data[3]

            ##
            # Check if cancelled flip is of non zero value.
            # Cancelled Flip with Present id 0 is flip that is already executed.
            if cancelled_present_id != 0:
                ##
                # Present id of cancelled flip should not be less than present id requested for cancel.
                # All the flips queued after the requested present id can be cancelled.
                if cancelled_present_id < requested_present_id:
                    logging.error("Present id cancelled is incorrect. Cancelled id {} Requested id {}".format(
                        cancelled_present_id, requested_present_id))
                    report_to_gdhm("Present id cancelled is incorrect. Cancelled id {} Requested id {}"
                                   .format(cancelled_present_id, requested_present_id))
                    return False
                else:
                    present_id = cancelled_present_id
                    cancel_entry_time = cancel_data[4]

                    ##
                    # Remove all the queued flips post cancel call.
                    # Max 8 flips can be queued. All the flips queued until cancel timestamp needs to be removed.
                    for present_id_count in range(0, SIMPLE_FLIPQ_DEPTH):
                        if present_id in flip_data.keys():
                            flip_timestamp = flip_data[present_id]["PlaneInfo"][0][2]
                            if cancel_entry_time >= flip_timestamp:
                                del flip_data[present_id]
                                if present_id in set_interrupt_target_present_id:
                                    del set_interrupt_target_present_id[present_id]
                            elif flip_timestamp > cancel_entry_time:
                                break

                            present_id = present_id + 1

    return True


##
# @brief        Get first and last entry time for flip data
# @param[in]    flip_data   : Flip data to fetch start and end present id for each layer
# @param[in]    notify_data : Notify data to fetch start and end present id for each layer
# @return       flip_layers : Start and end present id for each layer
def get_first_and_last_entry(flip_data, notify_data):
    flip_layers = OrderedDict()
    notify_layers = OrderedDict()

    ##
    # Get starting present id for each layer in ETL for flip data
    for layer_index in range(0, NO_OF_LAYERS):
        for present_id in flip_data:
            if layer_index == flip_data[present_id]["PlaneInfo"][0][1]:
                flip_layers[layer_index] = []
                flip_layers[layer_index].append(present_id)
                break

    ##
    # Get last present id for each layer in ETL for flip data
    for layer_index in range(0, NO_OF_LAYERS):
        for present_id in reversed(flip_data):
            if layer_index == flip_data[present_id]["PlaneInfo"][0][1]:
                flip_layers[layer_index].append(present_id)
                break

    ##
    # Get starting present id for each layer in ETL for notify data
    for layer_index in range(0, NO_OF_LAYERS):
        for present_id in notify_data:
            if layer_index == notify_data[present_id][0]:
                notify_layers[layer_index] = []
                notify_layers[layer_index].append(present_id)
                break

    ##
    # Get last present id for each layer in ETL for notify data
    for layer_index in range(0, NO_OF_LAYERS):
        for present_id in reversed(notify_data):
            if layer_index == notify_data[present_id][0]:
                notify_layers[layer_index].append(present_id)
                break

    return flip_layers, notify_layers


##
# @brief        Verification of FlipQ
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    platform     : Platform information
# @return       status       : True if verification is successful else False
def verify_flipq(etl_file, current_pipe, platform):
    flip_details = OrderedDict()
    unique_plane_id = []
    mmio_data_list = []
    address_list = []
    set_interrupt_target_present_id = OrderedDict()
    queued_flip_count = 0
    notify_log_buffer = OrderedDict()

    machine_info = SystemInfo()
    os_build = machine_info.get_os_info()
    # Check to skip verification before Nickel OS
    if os_build.BuildNumber < '22367':
        logging.info("Skipping FlipQ Verification as OS version {} does not support the Feature."
                     .format(os_build.BuildNumber))
        return True

    # Generate ETL report
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ##
    # Get flip data
    flip_data = etl_parser.get_flip_data('PIPE_' + current_pipe)

    ##
    # Get SetInterruptTargetPresentId data
    interrupt_data = etl_parser.get_event_data(etl_parser.Events.SET_INTERRUPT_TARGET_PRESENT_ID)

    ##
    # Get NotifyVSyncLogBuffer data
    notify_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT)

    ##
    # Create a dictionary of Set Interrupt Target Present Id data.
    if interrupt_data is not None:
        for interrupt_present_id_data in interrupt_data:
            if interrupt_present_id_data.SourceId == (ord(current_pipe) - 65):
                set_interrupt_target_present_id[interrupt_present_id_data.InterruptTargetPresentId] = [
                    interrupt_present_id_data.LayerIndex, interrupt_present_id_data.EntryTimeStamp,
                    interrupt_present_id_data.TimeStamp]

    ##
    # Create a list of Notify log buffer data.
    # Present id notified and timestamp of notify log buffer
    if notify_data is not None:
        for notify_log_buffer_ext in notify_data:
            notify_log_buffer[notify_log_buffer_ext.PresentID] = [notify_log_buffer_ext.LayerIndex,
                                                                  notify_log_buffer_ext.LogBufferIndex,
                                                                  notify_log_buffer_ext.NotifyTimeStamp,
                                                                  notify_log_buffer_ext.TimeStamp]

    ##
    # Create a dictionary of plane data with MPO DDI data, All param and Address only flips data
    for plane_data in flip_data:
        plane_info_list = []
        address_info_list = []
        all_param_info_list = []

        ##
        # Temporary list to store MPO DDI data for flip start to stop
        if len(plane_data.PlaneInfoList) != 0:
            for plane_info in plane_data.PlaneInfoList:
                plane_info_list.append((plane_info.PresentId, plane_data.SourceId, plane_info.LayerIndex,
                                        plane_info.TimeStamp, plane_data.TargetFlipTime))

        ##
        # Temporary list to store Address only data for flip start to stop
        if len(plane_data.FlipAddressList) != 0:
            for flip_address in plane_data.FlipAddressList:
                address_info_list.append((flip_address.PlaneID, flip_address.Address, flip_address.AddressUv,
                                          flip_address.OutFlags))

                ##
                # Get unique plane id
                if flip_address.PlaneID not in unique_plane_id:
                    unique_plane_id.append(flip_address.PlaneID)

                ##
                # No of flips that are queued
                if (int(flip_address.PresentationTimeStamp - flip_address.DisplayTime)) > 0:
                    queued_flip_count = queued_flip_count + 1

        ##
        # Temporary list to store All param data for flip start to stop
        if len(plane_data.FlipAllParamList) != 0:
            for flip_all_param in plane_data.FlipAllParamList:
                all_param_info_list.append((flip_all_param.PlaneID, flip_all_param.Address, flip_all_param.AddressUv))

        for index in range(0, len(plane_info_list)):
            present_id = plane_info_list[index][0]
            flip_details[present_id] = {}

            if present_id in flip_details:
                flip_details[present_id]["PlaneInfo"] = []
                ##
                # Plane Info dictionary with values arranged as (Source Id, Layer Index, Flip TimeStamp,
                # Target Flip time)
                flip_details[present_id]["PlaneInfo"].append((plane_data.SourceId, plane_info_list[index][2],
                                                              plane_info_list[index][3], plane_info_list[index][4]))

                ##
                # Address Only flip dictionary with values arranged as (Plane Id, Flip Address, Flip UV Address,
                # Out flag)
                if address_info_list:
                    if "AddressOnly" not in flip_details[present_id]:
                        flip_details[present_id]["AddressOnly"] = []

                    flip_details[present_id]["AddressOnly"].append((address_info_list[index][0],
                                                                    address_info_list[index][1],
                                                                    address_info_list[index][2],
                                                                    address_info_list[index][3]))

                ##
                # All param flip dictionary with values arranged as (Plane Id, Flip Address, Flip UV Address)
                if all_param_info_list:
                    if "AllParam" not in flip_details[present_id]:
                        flip_details[present_id]["AllParam"] = []

                    flip_details[present_id]["AllParam"].append((all_param_info_list[index][0],
                                                                 all_param_info_list[index][1],
                                                                 all_param_info_list[index][2]))

    if queued_flip_count == 0:
        logging.error("No queued flips")
        report_to_gdhm("No queued flips")
        return False

    ##
    # Remove all the cancelled flips from plane verification dictionary and validate cancelled flip data
    status = remove_cancelled_flip(flip_details, set_interrupt_target_present_id, current_pipe)
    if not status:
        return False

    ##
    # Generate surface address MMIO data list for each planes
    for index in unique_plane_id:
        plane_surf_reg_name = 'PLANE_SURFLIVE_' + str(index + 1) + '_' + current_pipe
        plane_surf = MMIORegister.get_instance("PLANE_SURFLIVE_REGISTER", plane_surf_reg_name, platform)
        offset = plane_surf.offset
        mmio_data_list.append(etl_parser.get_mmio_data(offset))

    ##
    # Get first and last present id in ETL for flip data and notify log buffer data for each layer
    flip_layer, notify_layer = get_first_and_last_entry(flip_details, notify_log_buffer)

    ##
    # Verify flip execution timestamp for each flip where present id reporting is requested
    for present_id in set_interrupt_target_present_id:
        present_id_layer = set_interrupt_target_present_id[present_id][0]
        ##
        # Exclude set interrupt present id if logged before flip data and notify data.
        # Also exclude set interrupt present id if logged after flip data and notify data.
        if present_id not in flip_details.keys():
            ##
            # Note: Need to check why there is a present id reporting request for inactive layer
            if present_id_layer not in flip_layer.keys():
                continue
            elif present_id < flip_layer[present_id_layer][0] or present_id > flip_layer[present_id_layer][1]:
                continue
        if present_id not in notify_log_buffer.keys():
            ##
            # Note: Need to check why there is a present id reporting request for inactive layer
            if present_id_layer not in notify_layer.keys():
                continue
            elif present_id < notify_layer[present_id_layer][0] or present_id > notify_layer[present_id_layer][1]:
                continue

        plane_info_data = flip_details[present_id]
        if "AddressOnly" in plane_info_data:
            flip_target_flip_time = flip_details[present_id]["PlaneInfo"][0][3]
            plane_timestamp = flip_details[present_id]["PlaneInfo"][0][2]
            flip_execution_time = notify_log_buffer[present_id][2]
            log_buffer_index = notify_log_buffer[present_id][1]
            notify_timestamp = notify_log_buffer[present_id][3]
            address_only_flip = flip_details[present_id]["AddressOnly"]

            for flip_address in address_only_flip:
                address_list = []
                plane_id = flip_address[0]
                plane_address = flip_address[1]
                plane_address_uv = flip_address[2]
                out_flag = flip_address[3]
                if out_flag == "SubmittedToHwQueue":
                    if flip_execution_time < flip_target_flip_time:
                        logging.error("Flip executed before time stamp expired. Target time {} Execution time {} "
                                      "Present id {}".format(flip_target_flip_time, flip_execution_time, present_id))
                        report_to_gdhm("Flip executed before time stamp expired. Target time {} Execution time {} "
                                       "Present id {}".format(flip_target_flip_time, flip_execution_time, present_id))
                        return False

                surface_address = plane_address_uv if plane_address_uv != 0 else plane_address
                ##
                # Create address list for all the MMIO surface writes within the allowed range
                for mmio in mmio_data_list[plane_id]:
                    if mmio.Data == surface_address:
                        if plane_timestamp <= mmio.TimeStamp <= notify_timestamp:
                            address_list.append(mmio.Data)
                        elif mmio.TimeStamp > notify_timestamp:
                            break
                        else:
                            continue

                ##
                # Verify if the flip address is part of MMIO surface writes
                if address_list:
                    if surface_address in address_list:
                        logging.debug("Verified surface address {}".format(hex(surface_address)))
                    else:
                        logging.error("Verification failed for surface address Pipe {} Plane {} Address {} "
                                      "TimeStamp {}"
                                      .format(current_pipe, plane_id, hex(surface_address), plane_timestamp))
                        report_to_gdhm("Verification failed for surface address Pipe {} Plane {} Address {} "
                                       "TimeStamp {}"
                                       .format(current_pipe, plane_id, hex(surface_address), plane_timestamp))
                        return False

    return True
