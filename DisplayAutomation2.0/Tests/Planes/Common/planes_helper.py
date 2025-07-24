########################################################################################################################
# @file         planes_helper.py
# @brief        The script consists of helper functions for DFT based testing.
#               * Color space mapping for pixel formats.
#               * Create resource for planes.
#               * Free resources allocated for the planes.
# @author       Shetty, Anjali N
########################################################################################################################

import logging
import os
import time

from Libs.Core import etl_parser, flip
from Libs.Core.logger import etl_tracer
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister
from registers.lnl.PIPE_SCANLINE_REGISTER import *
from Libs.Core import registry_access


ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
SIMPLE_FLIPQ_DEPTH = 16

resource = []
platform = []
mpo = flip.MPO()
machine_info = SystemInfo()

gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
for i in range(len(gfx_display_hwinfo)):
    platform.append(str(gfx_display_hwinfo[i].DisplayAdapterName).lower())

##
# 7ms delay from CCD to HAL layer + Additional wait for 1 frame
SCANLINE_MODE_WAIT = 0.007000 + 0.016000

##
# One frame delay to queue the flips
SINGLE_FRAME_DELAY = 0.016000


##
# @brief            Get the color space for provided pixel format.
# @param[in]        pixel_format pixel format of the plane.
# @return           Color space for the given pixel format.
def get_color_space_for_pixel_format(pixel_format):
    if pixel_format < 14:
        color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
    else:
        color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

    return color_space


##
# @brief            To create resource
# @param[in]        pplanes; Pointer to structure containing the plane info
# @return           void
def create_resource(pplanes):
    ##
    # Create 2 resources and use the resource for alternate flips
    for index in range(0, flip.MAX_RESOURCE):
        planes = []
        resource_creation = mpo.create_resource(pplanes)
        if resource_creation:
            for plane_index in range(0, pplanes.uiPlaneCount):
                planes.append(
                    pplanes.stPlaneInfo[plane_index].stResourceInfo[pplanes.stPlaneInfo[plane_index].iResourceInUse])
                logging.info("Successfully created resource {}".format(index))
                logging.info("GMM Block {} Virtual address {} Surface size {} Pitch {}"
                             .format(pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                         pplanes.stPlaneInfo[plane_index].iResourceInUse].ullpGmmBlock,
                                     pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                         pplanes.stPlaneInfo[plane_index].iResourceInUse].ullpUserVirtualAddress,
                                     pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                         pplanes.stPlaneInfo[plane_index].iResourceInUse].ullSurfaceSize,
                                     pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                         pplanes.stPlaneInfo[plane_index].iResourceInUse].ulPitch))
                pplanes.stPlaneInfo[plane_index].iResourceInUse = \
                    (1, 0)[pplanes.stPlaneInfo[plane_index].iResourceInUse]
        else:
            raise Exception("Failed to create resource")


##
# @brief            To free resources
# @param[in]        pplanes; Pointer to structure containing the plane info
# @return           void
def free_resource(pplanes):
    ##
    # Free all the resources
    for index in range(0, flip.MAX_RESOURCE):
        resource_in_use = index
        for plane_index in range(0, pplanes.uiPlaneCount):
            pplanes.stPlaneInfo[plane_index].iResourceInUse = resource_in_use
            free = mpo.free_resource(
                pplanes.stPlaneInfo[plane_index].stResourceInfo[pplanes.stPlaneInfo[plane_index].iResourceInUse])
            if free:
                logging.info("Successfully freed the resource")
            else:
                raise Exception("Failed to free resource")


##
# @brief            Helper function to start ETL capture.
# @return           status; True if ETL started otherwise False
def start_etl_capture():
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_Before_Scenario_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief            Helper function to stop ETL capture.
# @return           etl_file_path; path of ETL file captured
def stop_etl_capture():
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_After_Scenario.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after FlipQ scenario")
    return etl_file_path


##
# @brief            Verification of FlipQ
# @param[in]        etl_file; ETL file to be verified
# @param[in]        presentation_delay; Presentation delay
# @param[in]        display; Display details
# @param[in]        no_of_display; no of displays connected
# @param[in]        pixel_format; pixel format of the plane
# @param[in]        gfx_adapter_index; Gfx Adapter index
# @return           True if verification is successful else False
def verify_flipq(etl_file, presentation_delay, display, no_of_display, pixel_format, gfx_adapter_index='gfx_0'):
    delay = []
    flip_details = []
    unique_plane_id = []
    mmio_data_list = []
    hw_queue_flip_count = 0

    gfx_index = gfx_adapter_index.split('_')
    gfx_index = int(gfx_index[1])

    display_base_obj = DisplayBase(display, platform[gfx_index], gfx_index=gfx_adapter_index)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_adapter_index)
    current_pipe = chr(int(current_pipe) + 65)


    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ##
    # Get flip data for sync flips
    flip_data = etl_parser.get_event_data(etl_parser.Events.DFT_FLIP_SYNC_ADDRESS)

    ##
    # Generate delay list
    for plane_data in flip_data:
        pipe = plane_data.Pipe.split('_')
        pipe = pipe[1]
        if pipe == current_pipe:
            if plane_data.PlaneID not in unique_plane_id:
                unique_plane_id.append(plane_data.PlaneID)
            delay.append(plane_data.PresentationTimeStamp - plane_data.DisplayTime)

            ##
            # Get UV address for planar formats
            if pixel_format in [flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_P010YUV420,
                                flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_P016YUV420]:
                flip_details.append(
                    (((plane_data.PresentationTimeStamp - plane_data.DisplayTime) / 1000000), plane_data.AddressUv, plane_data.PlaneID,
                     (plane_data.TimeStamp / 1000)))
            ##
            # Get plane address for all formats except for planar formats
            else:
                flip_details.append((((plane_data.PresentationTimeStamp - plane_data.DisplayTime) / 1000000), plane_data.Address, plane_data.PlaneID,
                                 (plane_data.TimeStamp / 1000)))

    ##
    # Verify if delay count is matching
    if (len(presentation_delay) / no_of_display) != len(delay):
        logging.error("Delay count is not matching ETL {} Test {}".format(len(delay), len(presentation_delay)))
        return False

    ##
    # Generate surface address MMIO data list for each planes
    for index in unique_plane_id:
        plane_surf_reg_name = 'PLANE_SURFLIVE_' + str(index + 1) + '_' + current_pipe
        plane_surf = MMIORegister.get_instance("PLANE_SURFLIVE_REGISTER", plane_surf_reg_name, platform[gfx_index])
        offset = plane_surf.offset
        mmio_data_list.append(etl_parser.get_mmio_data(offset))

    ##
    # For each address in sync flip, create a list of all the MMIO address writes between
    # Plane data time stamp + Presentation delay and Plane data time stamp + Presentation delay +
    # (Scanline mode delay / 1Khz mode delay)
    for data in flip_details:
        address_list = []
        plane_address = data[1]
        plane_timestamp_and_presentation_delay = data[3] + data[0]
        plane_id = data[2]

        ##
        # No of flips in Hw queue
        if plane_id == 0:
            hw_queue_flip_count = hw_queue_flip_count + 1

        ##
        # Create address list for all the MMIO surface writes within the allowed range
        for mmio in mmio_data_list[plane_id]:
            if mmio.Data == plane_address:
                mmio_timestamp_seconds = mmio.TimeStamp / 1000
                if plane_timestamp_and_presentation_delay <= mmio_timestamp_seconds \
                        <= (plane_timestamp_and_presentation_delay + SCANLINE_MODE_WAIT):
                    address_list.append(mmio.Data)
                elif mmio_timestamp_seconds > (plane_timestamp_and_presentation_delay + SCANLINE_MODE_WAIT):
                    break
                else:
                    continue

        ##
        # Verify if the flip address is part of Live surface reads
        if plane_address in address_list:
            logging.debug("Verified surface address {}".format(hex(plane_address)))
        else:
            logging.error("Verification failed for surface address {}".format(hex(plane_address)))
            return False

    return True


##
# @brief            Simple FlipQ tail offset details ADLP+
# @param[in]        value; FlipQ tail offset string
# @return           Simple FlipQ tail offset for the requested queue
def get_flipq_tail_offset(value):
    return {
        'FLIP_Q0_PIPE_A_FPQ_TAIL': 0x5F12C,
        'FLIP_Q1_PIPE_A_FPQ_TAIL': 0x5F13C,
        'FLIP_Q0_PIPE_B_FPQ_TAIL': 0x5F52C,
        'FLIP_Q1_PIPE_B_FPQ_TAIL': 0x5F53C,
        'FLIP_Q0_PIPE_C_FPQ_TAIL': 0x5F92C,
        'FLIP_Q1_PIPE_C_FPQ_TAIL': 0x5F93C,
        'FLIP_Q0_PIPE_D_FPQ_TAIL': 0x5FD2C,
        'FLIP_Q1_PIPE_D_FPQ_TAIL': 0x5FD3C,
    }[value]


##
# @brief            Simple FlipQ tail offset details
# @param[in]        value; FlipQ tail offset string
# @return           Simple FlipQ tail offset for the requested queue
def get_simple_flipq_tail_offset(value):
    return {
        'SIMPLE_FLIP_Q_PIPE_A_TAIL': 0x85FA8,
    }[value]


##
# @brief            Verification of Simple FlipQ MMIO
# @param[in]        etl_file; ETL file to be verified
# @param[in]        display; display to be verified
# @param[in]        queue; queue to be verified
# @param[in]        queue_size; no od elements queued from test
# @param[in]        gfx_adapter_index; graphics adapter index
# @return           True if verification is successful else False
def verify_flipq_mmio(etl_file, display, queue, queue_size, gfx_adapter_index='gfx_0'):
    tail_index_data = []
    gfx_index = gfx_adapter_index.split('_')
    gfx_index = int(gfx_index[1])

    display_base_obj = DisplayBase(display, platform[gfx_index], gfx_index=gfx_adapter_index)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_adapter_index)
    pipe = chr(int(current_pipe) + 65)

    ##
    # Generate ETL report
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ##
    # Get Queue offset based on platform
    if platform[gfx_index] in ['tgl']:
        flipq_tail = 'SIMPLE_FLIP_Q_PIPE_' + pipe + '_TAIL'
        offset = get_simple_flipq_tail_offset(flipq_tail)
    else:
        queue = str(queue)
        flipq_tail = 'FLIP_Q' + queue + '_PIPE_' + pipe + '_FPQ_TAIL'
        offset = get_flipq_tail_offset(flipq_tail)

    ##
    # Get MMIO data
    mmio_data = etl_parser.get_mmio_data(offset, is_write=True)
    if mmio_data is None:
        logging.error(f"No write event for {offset} found in ETL")
        return False

    # Get DFTFlipAllParam data
    dft_flip_all_param_data = etl_parser.get_event_data(etl_parser.Events.DFT_FLIP_ALL_PARAM)
    if dft_flip_all_param_data is None:
        logging.error(f"No DFT FlipAllParam event found in ETL")
        return False

    ##
    # The TailPointer update needs to be considered only after the DFTAllParam Flip
    for data in mmio_data:
        if data.TimeStamp > dft_flip_all_param_data[0].TimeStamp:
            tail_index_data.append(data.Data)

    ##
    # Verify the tail index count is matching queue count
    if len(tail_index_data) != queue_size:
        logging.error("Tail index increment count is not matching")
        return False
    return True


##
# @brief            To get pipe offset value.
# @param[in]        scanlinecountoffset
# @return           Offset value.
def get_pipe_offset(scanlinecountoffset):
    return {
        'PIPE_SCANLINE_A': 0x70000,
        'PIPE_SCANLINE_B': 0x71000,
        'PIPE_SCANLINE_C': 0x72000,
        'PIPE_SCANLINE_D': 0x73000
    }[scanlinecountoffset]


##
# @brief            Get the ulScanlineCountOffset.
# @param[in]        display
# @param[in]        gfx_adapter_index
# @return           Value of ulScanlineCountOffset offset.
def get_scanlinecount_offset(display, gfx_adapter_index='gfx_0'):
    gfx_index = gfx_adapter_index.split('_')
    gfx_index = int(gfx_index[1])

    display_base_obj = DisplayBase(display, platform[gfx_index], gfx_index=gfx_adapter_index)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_adapter_index)
    pipe = chr(int(current_pipe) + 65)

    Pipe_offset = 'PIPE_SCANLINE_' + pipe
    scanlinecountoffset = get_pipe_offset(Pipe_offset)

    return scanlinecountoffset


##
# @brief            Get FlipQ status.
# @param[in]        gfx_adapter_index
# @return           FlipQ status
def get_flipq_status(gfx_adapter_index='gfx_0'):
    flipq_enabled = False

    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_adapter_index)
    registry_value, registry_type = \
        registry_access.read(args=ss_reg_args, reg_name="DisplayFeatureControl2")

    if registry_value is not None and registry_value & (1 << 0):
        flipq_enabled = True

    return flipq_enabled






