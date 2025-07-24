######################################################################################
# @file             gen11watermarks.py
# @addtogroup       PyLibs_DisplayWatermark
# @brief            GEN11 specific module for DisplayWatermark
# @author           Suraj Gaikwad, Bhargav Adigarla
######################################################################################
import logging

import math
from Libs.Feature.display_watermark import watermark_base
from Libs.Feature.display_watermark import watermark_utils as wm_utils
from Libs.Core.logger import gdhm


##
# @brief        This class contains Gen11 watermark and dbuf verification API's
class Gen11Watermarks(watermark_base.DisplayWatermarkBase):
    max_pipes = wm_utils.MAX_PIPES_GEN11
    max_planes = wm_utils.MAX_PLANES_GEN11

    ##
    # @brief        Gen11Watermarks default __init__ function
    # @param[in]    gfx_index as optional
    def __init__(self, gfx_index='gfx_0'):
        watermark_base.DisplayWatermarkBase.__init__(self, gfx_index=gfx_index)

    ##
    # @brief        Verifies watermark values programmed by driver for GEN11
    # @param[in]    is_48hz_verification as optional if called 48hz test
    # @param[in]    gfx_index as optional
    # @param[in]    min_dbuf_check as optional
    # @return       True if watermark verification was done on a minimum of 1 plane, else False
    def verify_watermarks(self, is_48hz_verification=False, gfx_index = 'gfx_0', min_dbuf_check=False):

        max_pipes = self.max_pipes
        max_planes = self.max_planes

        plane_list = self.get_plane_params(max_pipes, max_planes, gfx_index)
        pipe_list = self.get_pipe_params(max_pipes, is_48hz_verification, gfx_index)

        self.print_pipe_params(pipe_list, max_pipes)
        self.print_plane_params(plane_list, max_pipes, max_planes)

        # get_programmed_lp_watermarks() and get_memory_latency() are same as Gen9, so inherit from Gen9
        programmed_lp_wm = self.get_programmed_lp_watermarks(max_pipes, max_planes, gfx_index)
        latency = self.get_memory_latency(gfx_index)

        programmed_trans_wm = self.get_programmed_trans_watermarks(max_pipes, max_planes, gfx_index)
        programmed_line_time = self.get_programmed_line_time(max_pipes, gfx_index)

        # No workarounds for Gen11
        workarounds = [False, False]

        logging.info("============= DBUF DISTRIBUTION VERIFICATION STARTED =============")
        status = self.check_min_dbuf_needed(plane_list, max_planes, max_pipes)
        logging.info("============== DBUF DISTRIBUTION VERIFICATION ENDED ==============")

        if status is True:
            expected_line_time, expected_lp_wm, expected_trans_wm = self.get_expected_watermarks(plane_list, pipe_list,
                                                                                                 latency, workarounds,
                                                                                                 max_pipes, max_planes)

            status = self.verify_wm_line_time(expected_line_time, programmed_line_time, max_pipes, pipe_list)
        else:
            logging.info('Linetime verification skipped !!')

        logging.info("============= PLANES WATERMARK VERIFICATION STARTED =============")
        if status is True:
            status = self.verify_lp_watermarks(expected_lp_wm, programmed_lp_wm, max_pipes, max_planes, plane_list, gfx_index)
        else:
            logging.info('Planes Main and LP Watermark verification skipped !!')
        if status is True:
            status = self.verify_trans_wm(expected_trans_wm, programmed_trans_wm, max_pipes, max_planes, plane_list)
        else:
            logging.info('Planes Transition Watermark verification skipped !!')
        logging.info("============== PLANES WATERMARK VERIFICATION ENDED ==============")

        cursor_plane_list = self.get_cursor_plane_params(max_pipes, gfx_index)

        programmed_cur_lp_wm = self.get_programmed_cursor_lp_watermarks(max_pipes, gfx_index)
        programmed_cur_trans_wm = self.get_programmed_cursor_trans_watermarks(max_pipes, gfx_index)

        # Setting plane count to 1 since there is only 1 cursor plane per pipe
        expected_line_time, expected_cur_lp_wm, expected_cur_trans_wm = self.get_expected_watermarks(cursor_plane_list,
                                                                                                     pipe_list, latency,
                                                                                                     workarounds,
                                                                                                     max_pipes, 1)

        logging.info("============= CURSOR WATERMARK VERIFICATION STARTED =============")
        if status is True:
            # Setting plane count to 1 since there is only 1 cursor plane per pipe
            status = self.verify_lp_watermarks(expected_cur_lp_wm, programmed_cur_lp_wm, max_pipes, 1,
                                               cursor_plane_list, gfx_index)
        else:
            logging.info('Cursor Main and LP Watermark verification skipped !!')
        if status is True:
            # Setting plane count to 1 since there is only 1 cursor plane per pipe
            status = self.verify_trans_wm(expected_cur_trans_wm, programmed_cur_trans_wm, max_pipes, 1,
                                          cursor_plane_list)
        else:
            logging.info('Cursor Transition Watermark verification skipped !!')
        logging.info("============== CURSOR WATERMARK VERIFICATION ENDED ==============")

        return status

    ##
    # @brief        Check expected watermarks based on spec
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    latency list
    # @param[in]    workarounds list
    # @param[in]    pipe_count
    # @param[in]    plane_count (parameters help re-usability for future platforms if needed)
    # @return       GEN11WATERMARK() object containing list of all active plane expected watermark blocks and lines
    def get_expected_watermarks(self, plane_list, pipe_list, latency, workarounds, pipe_count, plane_count):
        exp_watermarks = []
        exp_trans_watermarks = []
        exp_line_time = []
        for pipe_idx in range(0, pipe_count):
            exp_line_time_obj = watermark_base.PipeLinetimeObj()
            adjusted_pipe_pixel_rate = pipe_list[pipe_idx].fPixelRate * pipe_list[pipe_idx].fPipeDownscalingFactor
            adjusted_pipe_pixel_rate = (adjusted_pipe_pixel_rate * 2) if pipe_list[pipe_idx].bIsInterlaced is True \
                else adjusted_pipe_pixel_rate
            pipe_hor_total = pipe_list[pipe_idx].lHorizontalTotal
            if adjusted_pipe_pixel_rate > 0:
                exp_line_time_obj.fLineTime = math.ceil(8.0 * pipe_hor_total / adjusted_pipe_pixel_rate)
            exp_line_time.append(exp_line_time_obj)
            for plane_idx in range(0, plane_count):
                exp_trans_wm_obj = watermark_base.PlaneTransWatermarkObj()
                for level in range(0, wm_utils.LATENCY_LEVELS):
                    exp_plane_wm_obj = watermark_base.PlaneWatermarkObj()
                    current_latency = latency[level]
                    adjusted_plane_pixel_rate = round(adjusted_pipe_pixel_rate * plane_list[pipe_idx * plane_count +
                                                      plane_idx].fPlaneDownscalingFactor, 2)
                    bpp = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp
                    pixel_format_text = self.get_pixel_format_text(plane_list[pipe_idx * plane_count +
                                                                              plane_idx].uiPixelFormat)
                    yuv_component = plane_list[pipe_idx * plane_count + plane_idx].uiPlanarYUV420Component

                    # NV12 and P0xx formats UV surface is in plane < 4 and its bpp is 2 times Y surface bpp
                    # Y surface will be there in plane 4 and above
                    if pixel_format_text in ['YUV 420 PLANAR 8 BPC', 'YUV10 420 PLANAR 10 BPC',
                                             'YUV 420 PLANAR 12 BPC', 'YUV 420 PLANAR 16 BPC'] and (yuv_component == 0):
                        bpp = bpp * 2
                    source_width = plane_list[pipe_idx * plane_count + plane_idx].lPlaneHorizontal
                    tiling = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat
                    pipe_hor_total = pipe_list[pipe_idx].lHorizontalTotal
                    buffer_allocated = plane_list[pipe_idx * plane_count + plane_idx].uiBufferAllocated
                    plane_status = plane_list[pipe_idx * plane_count + plane_idx].bStatus
                    dbuf_block_size = wm_utils.DBUF_BLOCK_SIZE_YF if (tiling == wm_utils.SURFACE_MEMORY_Y_F_TILED) and \
                                                                     (bpp == 8) else wm_utils.DBUF_BLOCK_SIZE
                    tiling_text = wm_utils.MEMORY_TILING_LIST.get(plane_list[pipe_idx * plane_count +
                                                                             plane_idx].uiPlaneTilingFormat)

                    if adjusted_plane_pixel_rate > 0 and plane_status is True:
                        if (plane_list[
                                pipe_idx * plane_count + plane_idx].uiPlaneRotation == wm_utils.ROTATION_90) \
                                or (plane_list[pipe_idx * plane_count + plane_idx].uiPlaneRotation ==
                                    wm_utils.ROTATION_270):
                            if plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 1:
                                tile_y_min_lines = 16
                            elif plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 2:
                                tile_y_min_lines = 8
                            else:
                                tile_y_min_lines = 4
                        else:
                            tile_y_min_lines = 4

                        method1 = round((current_latency * adjusted_plane_pixel_rate * bpp / dbuf_block_size), 2) + 1

                        bytes_per_line = source_width * bpp
                        if tiling == wm_utils.SURFACE_MEMORY_LINEAR:
                            blocks_per_line = math.ceil(bytes_per_line / dbuf_block_size) + 1
                        elif tiling == wm_utils.SURFACE_MEMORY_Y_LEGACY_TILED:
                            blocks_per_line = math.ceil((tile_y_min_lines *
                                                         bytes_per_line / dbuf_block_size) + 1) / tile_y_min_lines
                        else:
                            blocks_per_line = math.ceil(bytes_per_line / dbuf_block_size) + 1
                        method2 = round(math.ceil(current_latency * adjusted_plane_pixel_rate / pipe_hor_total) *
                                        blocks_per_line, 2)

                        tile_y_min_blocks = tile_y_min_lines * blocks_per_line

                        lt_microseconds = pipe_hor_total / adjusted_plane_pixel_rate

                        if tiling == wm_utils.SURFACE_MEMORY_X_TILED or tiling == wm_utils.SURFACE_MEMORY_LINEAR:
                            if (bpp * pipe_hor_total / dbuf_block_size < 1) and (bytes_per_line / dbuf_block_size < 1):
                                sel_result_blocks = method2
                            elif buffer_allocated >= blocks_per_line:
                                sel_result_blocks = method2
                            elif current_latency >= lt_microseconds:
                                sel_result_blocks = method2
                            else:
                                sel_result_blocks = method1
                        else:
                            sel_result_blocks = max(method2, tile_y_min_blocks)

                        result_blocks = math.ceil(sel_result_blocks) + 1
                        result_lines = math.ceil(sel_result_blocks / blocks_per_line)

                        if tiling == wm_utils.SURFACE_MEMORY_Y_LEGACY_TILED:
                            if result_lines % tile_y_min_lines == 0:
                                extra_lines = tile_y_min_lines
                            else:
                                extra_lines = (tile_y_min_lines * 2) - (result_lines % tile_y_min_lines)
                            min_dbuf = (result_lines + extra_lines) * blocks_per_line
                        else:
                            min_dbuf = math.ceil(result_blocks + (result_blocks * 0.1))

                        exp_plane_wm_obj.bStatus = False if ((result_blocks >= buffer_allocated) or
                                                             (min_dbuf >= buffer_allocated) or
                                                             ((level > 0) and (result_lines > 31))
                                                             ) else True
                        exp_plane_wm_obj.fResultBlocks = result_blocks if exp_plane_wm_obj.bStatus is True else 0
                        exp_plane_wm_obj.fResultLines = result_lines if exp_plane_wm_obj.bStatus is True else 0

                        logging.debug(
                            "WM_{}_{}_{} adjustedpixclk={} bpp={} width={} tile={}({}) htotal={} blkperline={} "
                            "M1={} M2={} YMin={} ResBlk={} ResLin={}".format(
                                wm_utils.PLANE_NAME[plane_idx], wm_utils.PIPE_NAME[pipe_idx], level,
                                adjusted_plane_pixel_rate, bpp,
                                source_width, tiling, tiling_text, pipe_hor_total, blocks_per_line, method1, method2,
                                tile_y_min_blocks, exp_plane_wm_obj.fResultBlocks, exp_plane_wm_obj.fResultLines))

                        if level == 0:
                            transition_offset_blocks = wm_utils.TRANS_MINIMUM_GEN11 + wm_utils.TRANS_AMOUNT_GEN11
                            transition_y_min = 2 * tile_y_min_blocks
                            if (tiling == wm_utils.SURFACE_MEMORY_X_TILED) or (
                                    tiling == wm_utils.SURFACE_MEMORY_LINEAR):
                                trans_result_blocks = sel_result_blocks + transition_offset_blocks
                            else:
                                trans_result_blocks = max(sel_result_blocks, transition_y_min) + \
                                                      transition_offset_blocks
                            trans_result_blocks = math.ceil(trans_result_blocks) + 1

                            exp_trans_wm_obj.bStatus = False if (trans_result_blocks >= buffer_allocated) else True
                            exp_trans_wm_obj.fResultBlocks = trans_result_blocks if \
                                exp_trans_wm_obj.bStatus is True else 0

                    exp_watermarks.append(exp_plane_wm_obj)
                exp_trans_watermarks.append(exp_trans_wm_obj)

        return exp_line_time, exp_watermarks, exp_trans_watermarks

    ##
    # @brief        Check if minimum Dbuf is allocated for each active plane
    # @param[in]    plane_list of type PLANE()
    # @param[in]    plane_count
    # @param[in]    pipe_count
    # @return       True if min Dbuf is allocated; False, otherwise
    def check_min_dbuf_needed(self, plane_list, plane_count, pipe_count):

        ##
        # BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/12716
        # Note: Current implementation is only for 0/180 degree rotation scenarios
        # TODO: Extend this function for all 90/270 degree rotation scenarios

        status = True

        for pipe_idx in range(pipe_count):
            for plane_idx in range(plane_count):
                min_dbuf_needed = 0
                plane_obj = plane_list[pipe_idx * plane_count + plane_idx]

                ##
                # Check for Min DBuf for each enabled plane on all the pipes
                if plane_obj.bStatus:

                    ##
                    # Planes using Linear or X tiled memory formats must allocate a minimum of 8 blocks.
                    if (plane_obj.uiPlaneTilingFormat == wm_utils.SURFACE_MEMORY_X_TILED) or \
                            (plane_obj.uiPlaneTilingFormat == wm_utils.SURFACE_MEMORY_LINEAR):

                        if 'PLANAR' in wm_utils.GEN11_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']:
                            min_dbuf_needed = 2 * wm_utils.MIN_DBUF_X_TILE  # Calculate separate for Y and UV plane
                        else:
                            min_dbuf_needed = wm_utils.MIN_DBUF_X_TILE

                    ##
                    # Planes using Y tiled memory formats must allocate blocks for a minimum number of scan-lines worth
                    # of data.
                    #
                    # Y tiled minimum allocation = Ceiling [(4*Plane source width * Plane Bpp)/512] * MinScanLines/4 + 3
                    #
                    # For YUV 420 Planar formats (NV12, P0xx), buffer allocation is done for Y and UV surfaces
                    # separately. Treat Y and UV surface as 2 separate planes with UV plane will have double the bpp of
                    # Y plane

                    else:
                        min_scanlines_y_tile = 8
                        bpp = plane_obj.uiPlaneBpp
                        if ('PLANAR' in wm_utils.GEN11_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']) and \
                                (plane_obj.uiPlanarYUV420Component == 0):
                            bpp = bpp * 2

                        min_dbuf_needed = math.ceil(
                            float(4 * plane_obj.lPlaneHorizontal * bpp) / 512) * min_scanlines_y_tile / 4 + 3

                    ##
                    # Compare actual and expected min dbuf allocated
                    if plane_obj.uiBufferAllocated < min_dbuf_needed:
                        logging.critical("FAIL: Minimum DBuf not allocated for PLANE_{}_{}:"
                                         "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                         .format(wm_utils.PLANE_NAME[plane_idx],
                                                 wm_utils.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated))
                        status = False
                        gdhm.report_bug(
                            title="[OS][DBUF] Minimum DBuf not allocated for PLANE_{}_{}:"
                                  "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                .format(wm_utils.PLANE_NAME[plane_idx], wm_utils.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E1
                        )
                    else:
                        logging.info("PASS: Minimum DBuf allocated for PLANE_{}_{}:"
                                     "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                     .format(wm_utils.PLANE_NAME[plane_idx], wm_utils.PIPE_NAME[pipe_idx],
                                             min_dbuf_needed, plane_obj.uiBufferAllocated))
        return status
