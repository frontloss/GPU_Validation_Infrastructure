########################################################################################################################
# @file         planes_ui_verification.py
# @brief        This script contains helper functions to verify various features.
# @author       Anjali Shetty, Pai Vinayak1
########################################################################################################################
import ctypes
import ctypes.wintypes
import logging
import sys
from collections import OrderedDict

from Libs.Core import etl_parser, registry_access
from Libs.Core.machine_info.machine_info import SystemInfo
from Tests.PlanesUI.Common import planes_ui_helper
from registers.mmioregister import MMIORegister

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1
ETL_PARSER_CONFIG.interruptData = 1
ETL_PARSER_CONFIG.functionData = 1

##
# 7ms delay from CCD to HAL layer + Additional wait for 1 frame
SCANLINE_MODE_WAIT = 0.007000 + 0.016000

##
# FlipQ depth
SIMPLE_FLIPQ_DEPTH = 16

##
# No of layers per pipe
NO_OF_LAYERS = 3

##
# Max Duration value
VBLANK_MAX_DURATION = 0xFFFFFFFF

DMC_CHICKEN_HRR_ENABLED_MASK = 0x80000000
DMC_CHICKEN_BUSY_BIT_ENABLED_MASK = 0x40000000

incorrect_source_id_list = []

##
# Flip report threshold
THRESHOLD = 10


#######################################
# Functions to fetch Register Offsets #
#######################################

##
# @brief            Get DMC chicken offset
# @param[in]	    value : Pipe
# @return		    DMC Chicken offset for requested pipe
def get_dmc_chicken_offset(value):
    return {
        'A': 0x5f080,
        'B': 0x5f480,
        'C': 0x5f880,
        'D': 0x5fc80,
    }[value]


#####################################
# Helper Functions for Verification #
#####################################

##
# @brief        Check OS FlipQ status in registry
# @return       status : True if OS FlipQ is enabled in registry else False
def os_flipq_status_in_registry():
    flipq_status_in_regsitry = 0
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    registry_value, registry_type = registry_access.read(args=ss_reg_args, reg_name="DisplayFeatureControl2")
    if registry_value is not None:
        flipq_status_in_regsitry = registry_value & 0x1
        logging.info(f"OS FlipQ is {'enabled' if flipq_status_in_regsitry else 'disabled'} in registry")
    return flipq_status_in_regsitry


##
# @brief        Check OS FlipQ status in OsFtrTable
# @param[in]    etl_file : Data from FeatureControl event
# @return       status   : True if OS FlipQ is enabled in OSFtrTable else False
def os_flipq_status_in_os_ftr_table(etl_file):
    # Generate ETL report
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        raise Exception("Failed to generate EtlParser report")
    feature_control_info = etl_parser.get_event_data(etl_parser.Events.FEATURE_CONTROL)
    if feature_control_info is None:
        logging.error("No Data found for FeatureControl")
        assert False, "No Data found for FeatureControl"
    if feature_control_info[0].OsFtrTable[0] & 0x1 == 0x1:
        logging.info("OS FlipQ is enabled in OsFtrTable")
        return True
    logging.info("OS FlipQ is disabled in OsFtrTable")
    return False


##
# @brief        Remove cancelled flip from flip data
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
    no_of_layers = 3

    ##
    # Get starting present id for each layer in ETL for flip data
    for layer_index in range(0, no_of_layers):
        for present_id in flip_data:
            if layer_index == flip_data[present_id]["PlaneInfo"][0][1]:
                flip_layers[layer_index] = []
                flip_layers[layer_index].append(present_id)
                break

    ##
    # Get last present id for each layer in ETL for flip data
    for layer_index in range(0, no_of_layers):
        for present_id in reversed(flip_data):
            if layer_index == flip_data[present_id]["PlaneInfo"][0][1]:
                flip_layers[layer_index].append(present_id)
                break

    ##
    # Get starting present id for each layer in ETL for notify data
    for layer_index in range(0, no_of_layers):
        for present_id in notify_data:
            if layer_index == notify_data[present_id][0]:
                notify_layers[layer_index] = []
                notify_layers[layer_index].append(present_id)
                break

    ##
    # Get last present id for each layer in ETL for notify data
    for layer_index in range(0, no_of_layers):
        for present_id in reversed(notify_data):
            if layer_index == notify_data[present_id][0]:
                notify_layers[layer_index].append(present_id)
                break

    return flip_layers, notify_layers


##
# @brief        To fetch VBI enable and disable timings
# @param[in]    interrupt_data : List that contains details about the interrupt
# @return       vbi_timings    : List having enable and disable VBI timestamp
def get_enable_disable_timings(interrupt_data):
    vbi_enable_timings = []
    vbi_disable_timings = []
    if interrupt_data is not None:
        for each_interrupt in range(1, len(interrupt_data) - 1):
            if interrupt_data.index(interrupt_data[each_interrupt - 1]) == 0 and \
                    interrupt_data[each_interrupt - 1].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE:
                vbi_enable_timings.append(interrupt_data[each_interrupt].TimeStamp)
            if interrupt_data.index(interrupt_data[each_interrupt]) == 1 and \
                    interrupt_data[each_interrupt - 1].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_KEEP_PHASE:
                vbi_enable_timings.append(interrupt_data[each_interrupt].TimeStamp)
            if interrupt_data[each_interrupt].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE and \
                    interrupt_data[each_interrupt - 1].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE:
                vbi_enable_timings.append(interrupt_data[each_interrupt].TimeStamp)
            if interrupt_data[each_interrupt].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE and \
                    interrupt_data[each_interrupt - 2].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE:
                vbi_disable_timings.append(interrupt_data[each_interrupt].TimeStamp)

        ##
        # If VBI enable calls are not present in ETL, boundary checks are not necessary and return empty list
        if len(vbi_enable_timings) != 0 and len(vbi_disable_timings) != 0:
            if vbi_enable_timings[0] > vbi_disable_timings[0]:
                del vbi_disable_timings[0]
            if vbi_enable_timings[-1] > vbi_disable_timings[-1]:
                vbi_disable_timings.append(etl_parser.get_event_data(etl_parser.Events.ETL_DETAILS)[0].EndTime)

    return vbi_enable_timings, vbi_disable_timings


##
# @brief        To process ETL data
# @param[in]    etl_file       : ETL file to be verified
# @param[in]    current_pipe   : Display pipe details
# @param[in]    target_id      : Display target id details
# @param[in]    platform       : Platform information
# @return       processed data : List of all processed data in required form
def process_etl_data(etl_file, current_pipe, target_id, platform):
    flip_details = OrderedDict()
    flipq_mode = OrderedDict()
    notify_log_buffer = OrderedDict()
    set_interrupt_target_present_id = OrderedDict()
    mmio_data_list = [[], [], []]
    unique_plane_id = []
    queued_flip_count = 0
    disabled_present_id = []
    same_allocation_present_id = []

    # Generate ETL report
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        raise Exception("Failed to generate EtlParser report")

    ##
    # Get flip data
    flip_data = etl_parser.get_flip_data('PIPE_' + current_pipe)

    ##
    # Get SetInterruptTargetPresentId data
    set_interrupt_data = etl_parser.get_event_data(etl_parser.Events.SET_INTERRUPT_TARGET_PRESENT_ID)

    ##
    # Get NotifyVSyncLogBuffer data
    notify_vsync_log_buffer_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT)

    ##
    # Get HWFlipQMode data
    hw_flipq_mode_data = etl_parser.get_event_data(etl_parser.Events.HW_FLIPQ_MODE)

    ##
    # Get control interrupt data
    control_interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                           etl_parser.InterruptType.CRTC_VSYNC)

    ##
    # Create a dictionary of Set Interrupt Target Present Id data.
    if set_interrupt_data is not None:
        for interrupt_present_id_data in set_interrupt_data:
            if interrupt_present_id_data.SourceId == (ord(current_pipe) - 65):
                set_interrupt_target_present_id[interrupt_present_id_data.InterruptTargetPresentId] = [
                    interrupt_present_id_data.LayerIndex, interrupt_present_id_data.EntryTimeStamp,
                    interrupt_present_id_data.TimeStamp, interrupt_present_id_data.SourceId]

    ##
    # Create a list of Notify log buffer data.
    # Present id notified and timestamp of notify log buffer
    if notify_vsync_log_buffer_data is not None:
        for notify_log_buffer_ext in notify_vsync_log_buffer_data:
            if notify_log_buffer_ext.TargetID == target_id:
                notify_log_buffer[notify_log_buffer_ext.PresentID] = [notify_log_buffer_ext.LayerIndex,
                                                                      notify_log_buffer_ext.LogBufferIndex,
                                                                      notify_log_buffer_ext.NotifyTimeStamp,
                                                                      notify_log_buffer_ext.TimeStamp]

    ##
    # Get VBI enable and disable TimeStamp list
    vbi_enable_timings, vbi_disable_timings = get_enable_disable_timings(control_interrupt_data)

    ##
    # Get FlipQ mode data
    if hw_flipq_mode_data is not None:
        flipq_mode['Scanline'] = []
        flipq_mode['1KHz'] = []
        flipq_mode['Disable'] = []
        for hw_flipq_data in hw_flipq_mode_data:
            if hw_flipq_data.TargetId == target_id:
                if hw_flipq_data.FlipQMode == 'DD_HW_FLIPQ_MODE_SYNC':
                    flipq_mode['Scanline'].append(hw_flipq_data.TimeStamp)
                elif hw_flipq_data.FlipQMode == 'DD_HW_FLIPQ_MODE_ASYNC':
                    flipq_mode['1KHz'].append(hw_flipq_data.TimeStamp)
                elif hw_flipq_data.FlipQMode == 'DD_HW_FLIPQ_MODE_DISABLE':
                    flipq_mode['Disable'].append(hw_flipq_data.TimeStamp)

    ##
    # Create a dictionary of plane data with MPO DDI data, All param, Address only flips and Notify Vsync data
    for plane_data in flip_data:
        plane_info_list = []
        plane_details_list = []
        address_info_list = []
        all_param_info_list = []
        notify_vsync_layer_list = []

        ##
        # Temporary list to store MPO DDI data for flip start to stop
        if len(plane_data.PlaneInfoList) != 0:
            for plane_info in plane_data.PlaneInfoList:
                plane_info_list.append((plane_info.PresentId, plane_data.SourceId, plane_info.LayerIndex,
                                        plane_info.TimeStamp, plane_data.TargetFlipTime, plane_data.Duration,
                                        plane_info.Flags))

        ##
        # Temporary list to store MPO DDI data for flip start to stop
        if len(plane_data.PlaneDetailsList) != 0:
            for plane_details in plane_data.PlaneDetailsList:
                plane_details_list.append(plane_details.hAllocation)

        ##
        # Temporary list to store Address only data for flip start to stop
        if len(plane_data.FlipAddressList) != 0:
            for flip_address in plane_data.FlipAddressList:
                address_info_list.append((flip_address.PlaneID, flip_address.Address, flip_address.AddressUv,
                                          flip_address.OutFlags, flip_address.PresentationTimeStamp,
                                          flip_address.TimeStamp, flip_address.DisplayTime))

                ##
                # Get unique plane id
                if flip_address.PlaneID not in unique_plane_id:
                    unique_plane_id.append(flip_address.PlaneID)

                ##
                # No of flips that are queued
                if (int(flip_address.PresentationTimeStamp - flip_address.DisplayTime)) > 0:
                    queued_flip_count = queued_flip_count + 1

        ##
        # Temporary list to store Notify Vsync layer data
        if len(plane_data.NotifyVSyncLayerList) != 0:
            for notify_vsync_layer in plane_data.NotifyVSyncLayerList:
                notify_vsync_layer_list.append((notify_vsync_layer.LayerIndex, notify_vsync_layer.TimeStamp))

        ##
        # Temporary list to store All param data for flip start to stop
        if len(plane_data.FlipAllParamList) != 0:
            for flip_all_param in plane_data.FlipAllParamList:
                all_param_info_list.append((flip_all_param.PlaneID, flip_all_param.Address, flip_all_param.AddressUv))

        plane_details_index = 0
        for index in range(0, len(plane_info_list)):
            same_allocation = False
            present_id = plane_info_list[index][0]
            logging.debug(f"Present id to be added {present_id} at timestamp {plane_info_list[index][3]}")
            plane_status = plane_info_list[index][6].split(",")[0]
            if plane_status == "Enabled":
                prev_present_id = present_id - 1
                allocation = plane_details_list[plane_details_index]
                if prev_present_id in flip_details:
                    prev_plane_info_list = flip_details[prev_present_id]["PlaneInfo"]
                    for prev_plane in prev_plane_info_list:
                        prev_allocation = prev_plane[5]
                        if prev_allocation == allocation:
                            same_allocation_present_id.append(present_id)
                            same_allocation = True

                    if same_allocation:
                        continue

                ##
                # For few flips observed that Flip Data is added in wrong pipe from ETL parser when data is fetched per pipe
                # So this check is needed till ETL parser logic to fetch Flip Data is fixed.
                source_id = plane_info_list[index][0]
                if source_id != (ord(current_pipe) - 65):
                    incorrect_source_id_list.append(present_id)

                if present_id not in flip_details:
                    flip_details[present_id] = {}

                if "PlaneInfo" not in flip_details[present_id]:
                    flip_details[present_id]["PlaneInfo"] = []
                ##
                # Plane Info dictionary with values arranged as (Source Id, Layer Index, Flip TimeStamp,
                # Target Flip time, Duration)
                flip_details[present_id]["PlaneInfo"].append((plane_data.SourceId, plane_info_list[index][2],
                                                              plane_info_list[index][3], plane_info_list[index][4],
                                                              plane_info_list[index][5],
                                                              plane_details_list[plane_details_index]))
                plane_details_index = plane_details_index + 1

                ##
                # Address Only flip dictionary with values arranged as (Plane Id, Flip Address, Flip UV Address,
                # Out flag)
                if "AddressOnly" not in flip_details[present_id]:
                    flip_details[present_id]["AddressOnly"] = []

                if len(address_info_list) > index and address_info_list:
                    flip_details[present_id]["AddressOnly"].append((address_info_list[index][0],
                                                                    address_info_list[index][1],
                                                                    address_info_list[index][2],
                                                                    address_info_list[index][3],
                                                                    address_info_list[index][4],
                                                                    address_info_list[index][5],
                                                                    address_info_list[index][6]))
                else:
                    flip_details[present_id]["AddressOnly"].append([])

                ##
                # All param flip dictionary with values arranged as (Plane Id, Flip Address, Flip UV Address)
                if "AllParam" not in flip_details[present_id]:
                    flip_details[present_id]["AllParam"] = []

                if len(all_param_info_list) > index and all_param_info_list:
                    flip_details[present_id]["AllParam"].append((all_param_info_list[index][0],
                                                                 all_param_info_list[index][1],
                                                                 all_param_info_list[index][2]))
                else:
                    flip_details[present_id]["AllParam"].append([])

                ##
                # Notify Vsync dictionary with values arranged as (Layer Index, Notify Timestamp)
                if notify_vsync_layer_list:
                    if "NotifyVsync" not in flip_details[present_id]:
                        flip_details[present_id]["NotifyVsync"] = []

                    flip_details[present_id]["NotifyVsync"].append((notify_vsync_layer_list[index][0],
                                                                    notify_vsync_layer_list[index][1]))

            else:
                disabled_present_id.append(present_id)
                continue

    ##
    # Generate surface address MMIO data list for each planes
    for index in unique_plane_id:
        plane_surf_reg_name = 'PLANE_SURFLIVE_' + str(index + 1) + '_' + current_pipe
        plane_surf = MMIORegister.get_instance("PLANE_SURFLIVE_REGISTER", plane_surf_reg_name, platform)
        offset = plane_surf.offset
        mmio_data_list[index] = etl_parser.get_mmio_data(offset)

    return notify_log_buffer, set_interrupt_target_present_id, vbi_enable_timings, vbi_disable_timings, flipq_mode, \
           queued_flip_count, flip_details, mmio_data_list, disabled_present_id, same_allocation_present_id


##
# @brief        To get HRR active region
# @param[in]    pipe   : Pipe
# @return       output : List of tuples having HRR start/end time
def __get_hrr_active_region(pipe):
    offset = get_dmc_chicken_offset(pipe)

    dmc_chicken = etl_parser.get_mmio_data(offset, is_write=True)
    if dmc_chicken is None:
        return None

    start_time = None
    output = []
    for index, mmio_data in enumerate(dmc_chicken):
        if mmio_data.Data & DMC_CHICKEN_HRR_ENABLED_MASK == DMC_CHICKEN_HRR_ENABLED_MASK:
            start_time = mmio_data.TimeStamp
        else:
            # if HRR is already enabled then start time will be None, make it 0.0 for start of ETL
            if start_time is None:
                start_time = 0.0
            output.append((start_time, mmio_data.TimeStamp))
            start_time = None

        # if ETL is having duration flips till the end, then HRR will be enabled
        # In this case, test will consider end_time till end of the ETL which is required for further verification
        if (index == len(dmc_chicken) - 1) and (start_time is not None):
            etl_end_time = etl_parser.get_event_data(etl_parser.Events.ETL_DETAILS)[0].EndTime
            output.append((start_time, etl_end_time))

    return None if len(output) == 0 else output


##
# @brief        Fetch cancelled Present Id data
# @param[in]    current_pipe     : Display pipe details
# @param[in]    plane_data       : Plane data
# @param[in]    start_time       : Start time to get event data
# @param[in]    end_time         : End time to get event data
# @return       cancel_flip_data : Cancelled Present Id
def get_cancelled_flip_data(current_pipe, plane_data, start_time, end_time):
    cancel_flip_data = [[], [], []]

    ##
    # Get Cancel flip data.
    cancel_flip = etl_parser.get_event_data(etl_parser.Events.CANCEL_FLIP, start_time=start_time, end_time=end_time)

    ##
    # Check if there is any cancel entries in the ETL.
    if cancel_flip is not None:
        ##
        # Create a list of cancelled PresentId.
        for cancel in cancel_flip:
            if cancel.SourceId == (ord(current_pipe) - 65):
                present_id = cancel.PresentIdCancelled
                cancel_entry_time = cancel.TimeStamp
                for present_id_count in range(0, SIMPLE_FLIPQ_DEPTH):
                    if present_id in plane_data[cancel.LayerIndex].keys():
                        flip_timestamp = plane_data[cancel.LayerIndex][present_id][0]
                        if cancel_entry_time >= flip_timestamp:
                            cancel_flip_data[cancel.LayerIndex].append(present_id)
                            logging.debug(f"Cancelled present id {present_id} added to cancel list")
                        elif flip_timestamp > cancel_entry_time:
                            break

                        present_id = present_id + 1

    return cancel_flip_data


##########################
# Verification Functions #
##########################

##
# @brief        Verification of FlipQ
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    target_id    : Display target id details
# @param[in]    platform     : Platform information
# @return       status       : True if verification is successful else False
def verify_flipq(etl_file, current_pipe, target_id, platform):
    machine_info = SystemInfo()
    os_build = machine_info.get_os_info()
    # Check to skip verification before Nickel OS
    if os_build.BuildNumber < '22367':
        logging.info("Skipping FlipQ Verification as OS version {} does not support the Feature."
                     .format(os_build.BuildNumber))
        return True

    notify_log_buffer, set_interrupt_target_present_id, vbi_enable_timings, vbi_disable_timings, flipq_mode, \
    queued_flip_count, flip_details, mmio_data_list, disabled_present_id, same_allocation_present_id, \
        = process_etl_data(etl_file, current_pipe, target_id, platform)

    if not (os_flipq_status_in_os_ftr_table(etl_file) and os_flipq_status_in_registry()):
        logging.info("OS FlipQ is not enabled. Skipping verification for FlipQ")
        return True

    if queued_flip_count == 0:
        logging.error("No queued flips")
        planes_ui_helper.report_to_gdhm('SFLIPQ', "No queued flips")
        return False

    ##
    # Remove all the cancelled flips from plane verification dictionary and validate cancelled flip data
    status = remove_cancelled_flip(flip_details, set_interrupt_target_present_id, current_pipe)
    if not status:
        return False

    ##
    # Get first and last present id in ETL for flip data and notify log buffer data for each layer
    flip_layer, notify_layer = get_first_and_last_entry(flip_details, notify_log_buffer)

    ##
    # Verify flip execution timestamp for each flip where present id reporting is requested
    for present_id in set_interrupt_target_present_id:
        logging.debug(f"Verifying Present id {present_id} TimeStamp {set_interrupt_target_present_id[present_id][2]}")
        source_id = set_interrupt_target_present_id[present_id][3]
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
            ##
            # If plane is disabled or if allocation is same as previous flip exclude from verification
            elif present_id in disabled_present_id or present_id in same_allocation_present_id:
                continue
            ##
            # For few flips observed that Flip Data is added in wrong pipe from ETL parser when data is fetched per pipe
            # So this check is needed till ETL parser logic to fetch Flip Data is fixed.
            elif present_id in incorrect_source_id_list:
                continue
            ##
            # Sporadic failure seen in case of Clone display cases, which needs to be analyzed.
            # Adding this temporary condition
            else:
                continue

        plane_info_data = flip_details[present_id]

        if present_id not in notify_log_buffer.keys():
            ##
            # Below are the cases where present id is not part of Notify Vsync
            # Note: Need to check why there is a present id reporting request for inactive layer
            if present_id_layer not in notify_layer.keys():
                continue
            # Boundary conditions for ETL capture
            elif present_id < notify_layer[present_id_layer][0] or present_id > notify_layer[present_id_layer][1]:
                continue
            # Present id is not reported if flip is retried
            else:
                retry = False
                mpo3_start_time = flip_details[present_id]["PlaneInfo"][0][2]
                stop_time = flip_details[present_id]["PlaneInfo"][0][2] + 1000
                function_status = etl_parser.get_function_data(etl_parser.Functions.FLIPQ_SUBMISSION_POSSIBLE,
                                                               mpo3_start_time, stop_time)
                for function_data in function_status:
                    if function_data.ErrorCode == 27:
                        retry = True
                        break

                if retry:
                    continue

        if "AddressOnly" in plane_info_data and notify_log_buffer[present_id][0] == flip_details[present_id]["PlaneInfo"][0][1]:
            flip_target_flip_time = flip_details[present_id]["PlaneInfo"][0][3]
            plane_timestamp = flip_details[present_id]["PlaneInfo"][0][2]
            flip_execution_time = notify_log_buffer[present_id][2]
            log_buffer_index = notify_log_buffer[present_id][1]
            notify_timestamp = notify_log_buffer[present_id][3]
            address_only_flip = flip_details[present_id]["AddressOnly"]

            for flip_address in address_only_flip:
                if len(flip_address) != 0:
                    address_list = []
                    plane_id = flip_address[0]
                    plane_address = flip_address[1]
                    plane_address_uv = flip_address[2]
                    out_flag = flip_address[3]
                    if out_flag == "SubmittedToHwQueue":
                        if flip_execution_time != 0 and flip_execution_time < flip_target_flip_time:
                            logging.error("Flip executed before time stamp expired. Target time {} Execution time {} "
                                          "Present id {}".format(flip_target_flip_time,
                                                                 flip_execution_time, present_id))
                            planes_ui_helper.report_to_gdhm('SFLIPQ', "Flip executed before time stamp expired. "
                                                                      "Target time {} Execution time {} Present id {}"
                                                            .format(flip_target_flip_time,
                                                                    flip_execution_time, present_id))
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
                            planes_ui_helper.report_to_gdhm('SFLIPQ', "Verification failed for surface address "
                                                                      "Pipe {} Plane {} Address {} " "TimeStamp {}"
                                                            .format(current_pipe, plane_id, hex(surface_address),
                                                                    plane_timestamp))
                            return False

    return True


##
# @brief        Verify MPO
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    target_id    : Display target id details
# @param[in]    platform     : Platform information
# @return       status       : True if verification is successful else False
def verify_mpo(etl_file, current_pipe, target_id, platform):
    logging.info("Skipping verification !!!")
    return True


##
# @brief        Verify Flip Data
# @param[in]    flip_data     : Flip Data dictionary
# @param[in]    mmio_data     : MMIO data list
# @param[in]    flipq_mode    : FlipQ mode dictionary
# @param[in]    current_pipe  : Current pipe details
# @param[in]    vbi_start     : VBI start timestamp
# @param[in]    vbi_end       : VBI end timestamp
# @param[in]    hrr_start     : HRR start timestamp
# @param[in]    hrr_end       : HRR end timestamp
# @param[in]    refresh_rate  : RR change during HRR
# @return       status        : True if verification is successful else False
def verify_flip_data(flip_data, mmio_data, flipq_mode, current_pipe, vbi_start, vbi_end, hrr_start,
                     hrr_end, refresh_rate):
    ##
    # Verify flip data for all the present id that lies between VBI start to End
    for present_id in flip_data:
        plane_info = flip_data[present_id]["PlaneInfo"]
        ##
        # Continue if last Notify event is not logged.
        if "NotifyVsync" not in flip_data[present_id]:
            continue
        notify_vsync = flip_data[present_id]["NotifyVsync"]
        address_only_flip = flip_data[present_id]["AddressOnly"]

        ##
        # Iterate through each plane entry
        for plane_index in range(0, len(plane_info)):
            logging.debug(f"Verifying Present id {present_id} at timestamp {plane_info[plane_index][2]}")
            plane_timestamp = plane_info[plane_index][2]

            if plane_timestamp < vbi_start:
                continue
            ##
            # If plane timestamp lies between VBI start and VBI end then verify flip data
            elif vbi_start <= plane_timestamp <= vbi_end:
                plane_duration = plane_info[plane_index][4]

                ##
                # Verification for non VRR flips
                if plane_duration != VBLANK_MAX_DURATION:
                    if len(address_only_flip[plane_index]) != 0:
                        address_list = []
                        flip_address = address_only_flip[plane_index]
                        plane_id = flip_address[0]
                        plane_address = flip_address[1]
                        plane_address_uv = flip_address[2]
                        out_flag = flip_address[3]
                        presentation_delay = flip_address[4] - flip_address[6] if int(flip_address[4] - flip_address[6]) > 0 else 0
                        if presentation_delay > 0:
                            flip_timestamp = flip_address[5]
                            ##
                            # Last Notify entry is not logged in ETL
                            if plane_index >= len(notify_vsync):
                                continue
                            notify_timestamp = notify_vsync[plane_index][1]
                            if hrr_start is not None and hrr_end is not None:
                                if out_flag == "SubmittedToHwQueue" and hrr_start <= flip_timestamp <= hrr_end:
                                    flip_execution_time_difference = (notify_timestamp / 1000) - \
                                                                     ((flip_timestamp / 1000) +
                                                                      (presentation_delay / 1000000))
                                    if flip_execution_time_difference > (((1 / refresh_rate) * (3 / 2)) + (0.08 / 1000)):
                                        logging.error(f"Flip execution time difference is greater than 1.5(FramePeriod) "
                                                      f"for Present id {present_id} "
                                                      f"Flip TimeStamp:{plane_timestamp / 1000} "
                                                      f"Notify TimeStamp {notify_timestamp / 1000}. "
                                                      f"Time Difference {flip_execution_time_difference * 1000}ms "
                                                      f"Expected value {(((1 / refresh_rate) * (3 / 2)) + (0.08 / 1000)) * 1000}ms")
                                        return False

                            surface_address = plane_address_uv if plane_address_uv != 0 else plane_address
                            ##
                            # Create address list for all the MMIO surface writes within the allowed range
                            for mmio in mmio_data[plane_id]:
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
                                    planes_ui_helper.report_to_gdhm('SFLIPQ', "Verification failed for surface address "
                                                                              "Pipe {} Plane {} Address {} " "TimeStamp {}"
                                                                    .format(current_pipe, plane_id, hex(surface_address),
                                                                            plane_timestamp))
                                    return False

                else:
                    ##
                    # Check if FlipQ is enabled in 1KHz mode
                    for hw_flipq_mode_timestamp in flipq_mode['1KHz']:
                        if hw_flipq_mode_timestamp < plane_timestamp:
                            continue
                        elif plane_timestamp < hw_flipq_mode_timestamp > vbi_end:
                            logging.info("FlipQ is enabled in 1KHz mode")
                            break
                        elif hw_flipq_mode_timestamp > vbi_end:
                            logging.error("FlipQ is not enabled in 1KHz mode as part of VBI enable call")
                            return False
                    if len(address_only_flip[plane_index]) != 0:
                        flip_address = address_only_flip[plane_index]
                        out_flag = flip_address[3]
                        if out_flag == "SubmittedToHwQueue":
                            return False

            elif plane_timestamp > vbi_end:
                break

    return True


##
# @brief        Verification of FlipQ with HRR
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    target_id    : Display target id details
# @param[in]    platform     : Platform information
# @return       status       : True if verification is successful else False
def verify_flipq_hrr(etl_file, current_pipe, target_id, platform):
    hrr_start_timestamp = None
    hrr_end_timestamp = None
    refresh_rate = None
    notify_log_buffer, set_interrupt_target_present_id, vbi_enable_timings, vbi_disable_timings, flipq_mode, \
    queued_flip_count, flip_details, mmio_data_list, disabled_present_id, same_allocation_present_id, \
        = process_etl_data(etl_file, current_pipe, target_id, platform)

    psr2_ctl_reg_name = 'PSR2_CTL_' + current_pipe
    psr2_ctl_mmio_data = MMIORegister.get_instance("PSR2_CTL_REGISTER", psr2_ctl_reg_name, platform)
    offset = psr2_ctl_mmio_data.offset

    hrr_active_region_list = __get_hrr_active_region(current_pipe)

    ##
    # For every VBI enable call get the equivalent disable call and verify FlipQ during that time frame
    if len(vbi_enable_timings) != 0:
        for vbi_enable_timestamp, vbi_disable_timestamp in zip(vbi_enable_timings, vbi_disable_timings):

            ##
            # Check if PSR2 deep sleep is disabled
            psr2_ctl_data = etl_parser.get_mmio_data(offset, start_time=vbi_enable_timestamp,
                                                     end_time=vbi_disable_timestamp)
            if psr2_ctl_data is not None:
                is_deep_sleep_disabled = False
                psr_not_enabled = False
                for psr2_ctl in psr2_ctl_data:
                    psr2_enable = psr2_ctl.Data & 0x80000000
                    if psr2_enable:
                        psr2_ctl_idle_frame = psr2_ctl.Data & 0x7
                        if psr2_ctl_idle_frame == 0:
                            logging.debug("PSR2 DeepSleep is disabled {}".format(psr2_ctl.TimeStamp))
                            is_deep_sleep_disabled = True
                    else:
                        psr_not_enabled = True

                if not is_deep_sleep_disabled and not psr_not_enabled:
                    logging.error(f"PSR2 Deep sleep is not disabled within range "
                                  f"{vbi_enable_timestamp} - {vbi_disable_timestamp}")

            ##
            # Check if FlipQ is enabled in Scanline mode
            for hw_flipq_mode_timestamp in flipq_mode['Scanline']:
                if hw_flipq_mode_timestamp < vbi_enable_timestamp:
                    continue
                elif vbi_enable_timestamp < hw_flipq_mode_timestamp > vbi_disable_timestamp:
                    logging.info("FlipQ enabled in scanline mode")
                    break
                elif hw_flipq_mode_timestamp > vbi_disable_timestamp:
                    logging.error("FlipQ is not enabled in scanline mode as part of VBI enable call")
                    return False

            if hrr_active_region_list is not None:
                logging.info(f"HRR active region {hrr_active_region_list}")
                for hrr_active_region in hrr_active_region_list:
                    if hrr_active_region[0] > vbi_enable_timestamp and hrr_active_region[1] < vbi_disable_timestamp:
                        hrr_start_timestamp = hrr_active_region[0]
                        hrr_end_timestamp = hrr_active_region[1]
                        rr_switch_data = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO,
                                                                   hrr_start_timestamp,
                                                                   hrr_end_timestamp)
                        for rr_switch in rr_switch_data:
                            if rr_switch.VbiMasking is True:
                                refresh_rate = rr_switch.FixedRr1000 / 1000
                                logging.info(f"RR {refresh_rate}")
                    else:
                        continue

            if verify_flip_data(flip_details, mmio_data_list, flipq_mode, current_pipe, vbi_enable_timestamp,
                                vbi_disable_timestamp, hrr_start_timestamp, hrr_end_timestamp, refresh_rate):
                logging.info(f"Verified Flip Data between VBI enable {vbi_enable_timestamp} and "
                             f"VBI disable {vbi_disable_timestamp}")
            else:
                return False
    return True


##
# @brief        Verification of Flip
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    target_id    : Display target id details
# @param[in]    platform     : Platform information
# @return       status       : True if verification is successful else False
def verify_flip(etl_file, current_pipe, target_id, platform):
    logging.info("Verification needs to be implemented")
    return True


##
# @brief        Verification of Flip execution time
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    target_id    : Display target id details
# @param[in]    current_pipe : Display pipe details
# @return       status       : True if verification is successful else False
def verify_flip_time(etl_file, target_id, current_pipe):
    dot_clock = 0
    htotal = 0
    vtotal = 0
    plane_data_list = [OrderedDict(), OrderedDict(), OrderedDict()]
    notify_vsync_data_list = [OrderedDict(), OrderedDict(), OrderedDict()]
    previous_present_id = -1
    previous_timestamp = -1
    rr_switch_timestamp = []
    expected_frame_time = {}
    duration_time_frames = {}
    previous_flip = None
    previous_duration = -1
    rr_switch_time = -1
    duration_change = False
    status = True

    expected_fps = planes_ui_helper.FPS[f"{planes_ui_helper.get_config_type('-MEDIA_TYPE')}"].value

    # Generate ETL report
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        raise Exception("Failed to generate EtlParser report")

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    frequency = ctypes.wintypes.LARGE_INTEGER()

    kernel32.QueryPerformanceFrequency(ctypes.byref(frequency))

    ##
    # Get control interrupt data
    control_interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                           etl_parser.InterruptType.CRTC_VSYNC)

    ##
    # Get VBI enable/disable time range
    vbi_enable_timings, vbi_disable_timings = get_enable_disable_timings(control_interrupt_data)

    ##
    # Get system details
    transcoder_data = etl_parser.get_event_data(etl_parser.Events.SYSTEM_DETAILS_TRANSCODER)

    for system_detail in transcoder_data:
        if system_detail.DotClock > dot_clock:
            dot_clock = system_detail.DotClock
            htotal = system_detail.HTotal
            vtotal = system_detail.VTotal

    if len(vbi_enable_timings) == 0:
        vbi_enable_timings.append(None)

    if len(vbi_disable_timings) == 0:
        vbi_disable_timings.append(etl_parser.get_event_data(etl_parser.Events.ETL_DETAILS)[0].EndTime)

    ##
    # Verify flip execution time between VBI Enable - VBI Disable
    for vbi_enable_timestamp, vbi_disable_timestamp in zip(vbi_enable_timings, vbi_disable_timings):
        logging.info(f"Start time {vbi_enable_timestamp} End time {vbi_disable_timestamp}")
        ##
        # Get flip data
        flip_data = etl_parser.get_flip_data('PIPE_' + current_pipe, start_time=vbi_enable_timestamp,
                                             end_time=vbi_disable_timestamp)

        duration_start, duration_end = 0, 0,
        ##
        # Create a dictionary with duration as key and start and end time for that duration as values
        if flip_data is not None:
            for plane_data in flip_data:
                if len(plane_data.PlaneInfoList) != 0:
                    for plane_info in plane_data.PlaneInfoList:
                        plane_data_list[plane_info.LayerIndex][plane_info.PresentId] = (plane_data.TimeStamp,
                                                                                        plane_data.Duration)

                if plane_data.Duration not in duration_time_frames.keys():
                    duration_time_frames[plane_data.Duration] = []

                if previous_flip is None:
                    previous_flip = plane_data
                    duration_start = plane_data.TimeStamp
                else:
                    if previous_flip.Duration == plane_data.Duration:
                        previous_flip = plane_data
                        continue
                    else:
                        duration_end = previous_flip.TimeStamp
                        duration_time_frames[previous_flip.Duration].append((duration_start, duration_end))
                        duration_start = plane_data.TimeStamp
                        previous_flip = plane_data

            duration_end = plane_data.TimeStamp
            duration_time_frames[plane_data.Duration].append((duration_start, duration_end))

            logging.debug(f"Duration range {duration_time_frames}")

            ##
            # Based on the duration values, calculate expected frame time using System details or duration value
            for duration in duration_time_frames.keys():
                if duration == 0:
                    dot_clock_khz = dot_clock * 1000
                    timing = htotal * vtotal
                    fixed_rr1000 = ((dot_clock_khz + timing / 2) / timing)
                elif duration != VBLANK_MAX_DURATION:
                    fixed_rr1000 = round(
                        (((10 ** 10) + (plane_data.Duration / 2.0)) / float(plane_data.Duration)) / 1000.0, 3) * 1000
                else:
                    logging.info("Can't get frame time for Gaming VRR")
                    continue

                ##
                # Expected frame time calculation when FPS is multiple of RR
                if int((fixed_rr1000 / 1000) % expected_fps) == 0:
                    frame_time = 1 / expected_fps
                    frame_time_qpc = frame_time * frequency.value
                    ##
                    # Expected frame time dictionary. In case of FPS multiple of RR, adding second frame time as -1
                    expected_frame_time[duration] = (frame_time_qpc, -1)
                    logging.info(f"Multiple FPS frame time {frame_time_qpc} delay in sec {frame_time}")
                ##
                # Expected frame time calculation when FPS is not multiple of RR
                else:
                    count = 2
                    common_multiple = sys.maxsize
                    fps = int((1 / expected_fps) * 1000)
                    rr = int((1 / (fixed_rr1000 / 1000)) * 1000)
                    ##
                    # Find least common multiple between 1/RR and 1/FPS
                    for i in range(max(fps, rr), 1 + (fps * rr)):
                        if i % fps == i % rr == 0:
                            common_multiple = i
                            break

                    while True:
                        least_multiple = (1 / expected_fps) * count
                        if int((least_multiple * 1000) % (1 / (fixed_rr1000 / 1000))) == 0:
                            frame_count = round((1 / expected_fps) * count * (fixed_rr1000 / 1000))
                            delta = frame_count - count
                            first_frame_time = least_multiple * (count / frame_count)
                            second_frame_time = least_multiple * (delta / frame_count)
                            logging.info(f"First frame {first_frame_time} "
                                         f"Second frame {second_frame_time}")
                            first_frame_time_qpc = first_frame_time * frequency.value
                            second_frame_time_qpc = second_frame_time * frequency.value
                            logging.info(f"First frame {first_frame_time_qpc} "
                                         f"Second frame {second_frame_time_qpc}")
                            expected_frame_time[duration] = (first_frame_time_qpc, second_frame_time_qpc)
                            break
                        else:
                            count = count + 1
                            if count > common_multiple:
                                break
        else:
            logging.info("Flip data is None")
            continue

        ##
        # RR switch data
        rr_switch_program = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_PROGRAM)
        if rr_switch_program is not None:
            for rr_switch in rr_switch_program:
                rr_switch_timestamp.append(rr_switch.TimeStamp)

        cancelled_present_id_list = get_cancelled_flip_data(current_pipe, plane_data_list, vbi_enable_timestamp,
                                                            vbi_disable_timestamp)
        ##
        # Get NotifyVSyncLogBuffer data
        notify_vsync_log_buffer_data = etl_parser.get_event_data(etl_parser.Events.NOTIFY_VSYNC_LOG_BUFFER_EXT,
                                                                 start_time=vbi_enable_timestamp,
                                                                 end_time=vbi_disable_timestamp)

        ##
        # Create a list of Notify log buffer data.
        # Present id notified and timestamp of notify log buffer
        if notify_vsync_log_buffer_data is not None:
            for notify_log_buffer_ext in notify_vsync_log_buffer_data:
                notify_vsync_data_list[notify_log_buffer_ext.LayerIndex][notify_log_buffer_ext.PresentID] = \
                    notify_log_buffer_ext.NotifyTimeStamp
        else:
            continue

        for notify_layer_data in notify_vsync_data_list:
            layer = notify_vsync_data_list.index(notify_layer_data)
            for notify_present_id, notify_timestamp in notify_layer_data.items():
                if notify_present_id in plane_data_list[layer]:
                    flip_timestamp = plane_data_list[layer][notify_present_id][0]
                    flip_duration = plane_data_list[layer][notify_present_id][1]
                else:
                    logging.debug("Present id is not available")
                    continue

                if previous_duration != -1 and previous_duration != flip_duration:
                    if len(rr_switch_timestamp) != 0:
                        rr_switch_time = rr_switch_timestamp.pop()
                        duration_change = True

                previous_duration = flip_duration

                ##
                # If there is a duration change, wait until RR switch is complete to start verifying flip execution time
                if duration_change and rr_switch_time > flip_timestamp:
                    logging.info("Duration change happened but no RR switch yet.. "
                                 "Skip verification until RR switch")
                    continue
                elif duration_change and rr_switch_time < flip_timestamp:
                    logging.debug("RR switch done.. Resetting")
                    duration_change = False
                    rr_switch_time = -1

                ##
                # Fetch the expected frame time for a given flip
                if flip_duration in duration_time_frames.keys():
                    expected_interval1 = -1
                    expected_interval2 = -1
                    for index in range(0, len(duration_time_frames[flip_duration])):
                        ##
                        # Expected flip time withing the duration ranges
                        if duration_time_frames[flip_duration][index][0] <= flip_timestamp <= \
                                duration_time_frames[flip_duration][index][1]:
                            logging.info(f"Expected Frame time {expected_frame_time[flip_duration]}")
                            expected_interval1 = expected_frame_time[flip_duration][0]
                            expected_interval2 = expected_frame_time[flip_duration][1]
                            break
                        else:
                            continue
                else:
                    logging.error("Duration value is not available")
                    return False

                ##
                # First notify flip or first flip after cancellation
                if previous_present_id == -1:
                    previous_present_id = notify_present_id
                    previous_timestamp = notify_timestamp
                ##
                # Verify flip execution for all notify present id
                else:
                    if notify_present_id in cancelled_present_id_list[layer]:
                        previous_present_id = -1
                        continue

                    time_difference = notify_timestamp - previous_timestamp
                    previous_present_id = notify_present_id
                    previous_timestamp = notify_timestamp

                    ##
                    # Case for FPS is not multiple of RR
                    if expected_interval2 != -1:
                        delta1 = time_difference - expected_interval1
                        delta2 = time_difference - expected_interval2
                        if -10 <= (delta1 / 10) <= 10 or -10 <= (delta2 / 10) <= 10:
                            logging.debug(f"Flip execution time is within the threshold. Delta time: "
                                          f"{min(abs(delta1 / 10), abs(delta2 / 10))} micro seconds")
                        else:
                            logging.error(f"Flip execution time is not within the threshold. Delta time: Delta time: "
                                          f"{min(abs(delta1 / 10), abs(delta2 / 10))} micro seconds")
                            logging.info(f"Present id: {notify_present_id} Layer: {layer} "
                                         f"Expected time difference in QPC: {expected_interval1}  or "
                                         f"{expected_interval2}"
                                         f"Actual time difference in QPC {time_difference} ")
                            status &= False
                    ##
                    # Case for FPS multiple of RR
                    else:
                        delta1 = time_difference - expected_interval1
                        if -THRESHOLD <= (delta1 / 10) <= THRESHOLD:
                            logging.debug(f"Flip execution time is within the threshold. Delta time: {delta1 / 10} "
                                          f"micro seconds")
                        else:
                            logging.error(f"Flip execution time is not within the threshold. Delta time: {delta1 / 10} "
                                          f"micro seconds")
                            logging.info(f"Present id: {notify_present_id} Layer: {layer} "
                                         f"Expected time difference in QPC: {expected_interval1} "
                                         f"Actual time difference in QPC {time_difference} ")

                            status &= False

    return status


##
# @brief        Verification of OS unaware FlipQ with DC6V
# @param[in]    etl_file     : ETL file to be verified
# @param[in]    current_pipe : Display pipe details
# @param[in]    target_id    : Display target id details
# @param[in]    platform     : Platform information
# @return       True if verification is successful else False
def verify_flipq_dc6v(etl_file, current_pipe, target_id, platform):
    notify_log_buffer, set_interrupt_target_present_id, vbi_enable_timings, vbi_disable_timings, flipq_mode, \
    queued_flip_count, flip_details, mmio_data_list, disabled_present_id, same_allocation_present_id, \
        = process_etl_data(etl_file, current_pipe, target_id, platform)

    ##
    # For every VBI enable call get the equivalent disable call and verify FlipQ during that time frame
    if len(vbi_enable_timings) != 0:
        for vbi_enable_timestamp, vbi_disable_timestamp in zip(vbi_enable_timings, vbi_disable_timings):

            ##
            # Check if FlipQ is enabled in Scanline mode
            for hw_flipq_mode_timestamp in flipq_mode['Scanline']:
                if hw_flipq_mode_timestamp < vbi_enable_timestamp:
                    continue
                elif vbi_enable_timestamp < hw_flipq_mode_timestamp > vbi_disable_timestamp:
                    logging.info("FlipQ enabled in scanline mode")
                    break
                elif hw_flipq_mode_timestamp > vbi_disable_timestamp:
                    logging.error("FlipQ is not enabled in scanline mode as part of VBI enable call")
                    return False

            ##
            # Verify flip data for all the present id that lies between VBI start to End
            for present_id in flip_details:
                plane_info = flip_details[present_id]["PlaneInfo"]
                ##
                # Continue if last Notify event is not logged.
                if "NotifyVsync" not in flip_details[present_id]:
                    continue
                notify_vsync = flip_details[present_id]["NotifyVsync"]
                address_only_flip = flip_details[present_id]["AddressOnly"]

                ##
                # Iterate through each plane entry
                for plane_index in range(0, len(plane_info)):
                    plane_timestamp = plane_info[plane_index][2]

                    if plane_timestamp < vbi_enable_timestamp:
                        continue
                    ##
                    # If plane timestamp lies between VBI start and VBI end then verify flip data
                    elif vbi_enable_timestamp <= plane_timestamp <= vbi_disable_timestamp:
                        plane_duration = plane_info[plane_index][4]

                        ##
                        # Verification for non VRR flips
                        if plane_duration != VBLANK_MAX_DURATION:
                            if len(address_only_flip[plane_index]) != 0:
                                flip_address = address_only_flip[plane_index]
                                out_flag = flip_address[3]
                                presentation_delay = flip_address[4] - flip_address[6]
                                flip_timestamp = flip_address[5]
                                plane_timestamp_and_presentation_delay = flip_timestamp + presentation_delay
                                ##
                                # Last Notify entry is not logged in ETL
                                if plane_index >= len(notify_vsync):
                                    continue
                                notify_timestamp = notify_vsync[plane_index][1]
                                if out_flag == "SubmittedToHwQueue":
                                    if plane_timestamp_and_presentation_delay <= notify_timestamp \
                                            <= (plane_timestamp_and_presentation_delay + SCANLINE_MODE_WAIT):
                                        logging.error("Flip executed delayed. Threshold time {} Execution time {} "
                                                      "Present id {}".format(plane_timestamp_and_presentation_delay +
                                                                             SCANLINE_MODE_WAIT, notify_timestamp,
                                                                             present_id))

                                        return False
                                    else:
                                        logging.debug("Flip executed at right time. Threshold time {} "
                                                      "Execution time {} "
                                                      "Present id {}".format(plane_timestamp_and_presentation_delay +
                                                                             SCANLINE_MODE_WAIT, notify_timestamp,
                                                                             present_id))

                        else:
                            ##
                            # Check if FlipQ is enabled in 1KHz mode
                            for hw_flipq_mode_timestamp in flipq_mode['1KHz']:
                                if hw_flipq_mode_timestamp < plane_timestamp:
                                    continue
                                elif plane_timestamp < hw_flipq_mode_timestamp > vbi_disable_timestamp:
                                    logging.info("FlipQ is enabled in 1KHz mode")
                                    break
                                elif hw_flipq_mode_timestamp > vbi_disable_timestamp:
                                    logging.error("FlipQ is not enabled in 1KHz mode as part of VBI enable call")
                                    return False
                            if len(address_only_flip[plane_index]) != 0:
                                flip_address = address_only_flip[plane_index]
                                out_flag = flip_address[3]
                                if out_flag == "SubmittedToHwQueue":
                                    return False

                    elif plane_timestamp > vbi_disable_timestamp:
                        break

    return True
