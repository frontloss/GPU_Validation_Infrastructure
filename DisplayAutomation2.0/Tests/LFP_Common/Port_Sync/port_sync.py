#######################################################################################################################
# @file         port_sync.py
# @section      lfp_port_sync
# @brief        APIs for LFP port sync
# @author       Sri Sumanth Geesala
#######################################################################################################################

import logging

from Libs.Core import etl_parser
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.mipi.mipi_helper import MipiHelper, VbtMipiTimings

# Delta between ports when port sync is enabled should be max 1 scanline (HW defined). Since SW verification cannot be
# exact as HW we use SW factor. This SW factor (found based on experiment) is used to multiply with
# hardware expected limit (1 scanline time) when comparing with VBI timestamps delta.
SW_FACTOR = 50


##
# @brief        find outs whether port sync is supported by the panel connected to requested port
# @param[in]    port - string port name
# @param[in]    platform - string, name of the platform
# @return       bool - True if port sync supported else False, Bool
def is_port_sync_supported_by_panel(port, platform):
    if 'MIPI' in port:
        mipi_helper = MipiHelper(platform)
        panel_index = mipi_helper.gfx_vbt.get_panel_index_for_port(port)
        if mipi_helper.gfx_vbt.version >= 231:
            return True if (mipi_helper.gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                        1 << panel_index)) >> panel_index else False
        else:
            return True if mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].PortSyncFeature else False
    elif 'EDP' in port:
        # TODO: need to add logic later when eDP port sync feature is enabled
        return False
    else:
        return False


##
# @brief        This function verifies dual LFP port sync by comparing Pipe VBI timestamps of pipes two LFPs, within the
#               passed ETL file
# @param[in]    lfps_list - list of lfps attached
# @param[in]    etl_file_path - String, path to etl file
# @param[in]    platform - string name of the platform
# @return       bool - True if verification passed else False, Bool
def verify_dual_lfp_port_sync_using_VBI(lfps_list, etl_file_path, platform):
    ret = True
    scanline_time = 0
    mipi_helper = MipiHelper(platform)
    etl_parser_config = etl_parser.EtlParserConfig()
    etl_parser_config.vbiData = 1
    etl_parser.generate_report(etl_file_path, etl_parser_config)
    vbi_data_per_pipe = {}
    vbi_index_adjust_per_pipe = {}

    # get 1 scanline time for display
    if 'MIPI' in lfps_list[0]:
        panel_index = mipi_helper.get_panel_index_for_port('_DSI0' if lfps_list[0] == 'MIPI_A'
                                                           else '_DSI1')
        vbt_mipi_timings = VbtMipiTimings()
        vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, panel_index)
        vbt_mipi_timings.adjust_timings_for_mipi_config(mipi_helper, panel_index)
        scanline_time = vbt_mipi_timings.get_line_time(mipi_helper, panel_index)
    else:
        # TODO: need to write logic here once dual eDP port sync feature is enabled.
        pass

    all_pipe_vbi_data = etl_parser.get_vbi_data(limit=3)
    if all_pipe_vbi_data is None or len(all_pipe_vbi_data) < 3:
        logging.error("FAIL: No VBI Data found or only found less than 3 VBIs in captured ETL")
        return False
    if all_pipe_vbi_data[0].Pipe == all_pipe_vbi_data[1].Pipe == all_pipe_vbi_data[2].Pipe:
        logging.error("FAIL: First 3 VBIs in captured ETL are of same pipe {0}. This means second LFP went out of sync "
                      "with first LFP".format(all_pipe_vbi_data[0].Pipe))
        return False

    for lfp in lfps_list:
        vbi_index_adjust_per_pipe[lfp] = 0
        display_base = DisplayBase(lfp)
        pipe, ddi, transcoder = display_base.GetPipeDDIAttachedToPort(port_name=lfp,
                                                                      transcoder_mapping_details=True)
        pipe = pipe.upper()
        vbi_data = etl_parser.get_vbi_data(pipe)
        if vbi_data is None:
            logging.error("FAIL: No VBI Data found for pipe {0} of LFP {1} in captured ETL".format(pipe, lfp))
            return False
        vbi_data_per_pipe[lfp] = vbi_data

    lfp0_vbi_data = vbi_data_per_pipe[lfps_list[0]]
    lfp1_vbi_data = vbi_data_per_pipe[lfps_list[1]]

    # It's possible that 0th VBI of pipe_X maps to -1th VBI of pipe_Y (due to the ETL trace start time.
    # Then, it will be like [VBI_PipeA, VBI_PipeA, VBI_PipeB] or [VBI_PipeB, VBI_PipeA, VBI_PipeB]).
    # Then to map all next VBIs properly, we have to adjust the pipe_X's index by 1.
    diff = lfp0_vbi_data[0].TimeStamp - lfp1_vbi_data[0].TimeStamp
    display_config = DisplayConfiguration()
    target_id = display_config.get_target_id(lfps_list[0], display_config.get_enumerated_display_info())
    refresh_rate = display_config.get_current_mode(target_id).refreshRate
    # we increment index if diff of VBIs at 0th index is greater than or equal to (1 frame time - accepted delta).
    # accepted delta is required since -1th VBI of PipeA and 0th VBI1 of PipeA will have diff of 1 frame time,
    # but -1th VBI of PipeA and 0th VBI1 of PipeB will have lesser diff of port sync delta.
    if abs(diff * 1000) >= (((10 ** 6) / refresh_rate) - (scanline_time * SW_FACTOR)):
        if diff < 0:
            vbi_index_adjust_per_pipe[lfps_list[0]] += 1
        elif diff > 0:
            vbi_index_adjust_per_pipe[lfps_list[1]] += 1

    lfp0_vbi_index_adjust = vbi_index_adjust_per_pipe[lfps_list[0]]
    lfp1_vbi_index_adjust = vbi_index_adjust_per_pipe[lfps_list[1]]
    logging.info('1 scanline time = {0} us'.format(scanline_time))
    logging.info('Accepted delta between VBI of two LFPs in port sync is {0} us ({1} scanlines since SW '
                 'verification cannot be exact to 1 scanline)'.format(scanline_time * SW_FACTOR, SW_FACTOR))
    # checking for first 20 VBIs
    for index in range(20):
        # Timestamp is in ms. Convert it to us.
        delta = abs(lfp0_vbi_data[index + lfp0_vbi_index_adjust].TimeStamp -
                    lfp1_vbi_data[index + lfp1_vbi_index_adjust].TimeStamp) * 1000
        if delta < scanline_time * SW_FACTOR:
            logging.info('PASS: VBI {0} : Delta between VBIs of the two LFPs is within accepted value. '
                         'Delta = {1} us'.format(index, delta))
        else:
            logging.error('FAIL: VBI {0} : Delta between VBIs of the two LFPs is not within accepted value. '
                          'Delta = {1} us'.format(index, delta))
            ret = False

    return ret
