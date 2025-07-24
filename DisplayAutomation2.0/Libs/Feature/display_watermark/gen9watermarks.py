######################################################################################
# @file             gen9watermarks.py
# @addtogroup       PyLibs_DisplayWatermark
# @brief            GEN10 specific module for DisplayWatermark
# @author           Suraj Gaikwad, Bhargav Adigarla
######################################################################################
import importlib
import logging

import math
from Libs.Feature.display_watermark import watermark_base
from Libs.Feature.display_watermark import watermark_utils as wm_util
from Libs.Feature.powercons import registry
from Libs.Core.logger import gdhm


##
# @brief        This class contains Gen9 watermark and dbuf verification API's
class Gen9Watermarks(watermark_base.DisplayWatermarkBase):
    max_pipes = wm_util.MAX_PIPES
    max_planes = wm_util.MAX_PLANES

    ##
    # @brief        Gen9Watermarks default __init__ function
    # @param[in]    gfx_index as optional
    def __init__(self, gfx_index='gfx_0'):
        watermark_base.DisplayWatermarkBase.__init__(self, gfx_index=gfx_index)

    ##
    # @brief        Verifies watermark values programmed by driver for GEN9
    # @param[in]    is_48hz_verification as optional if called 48hz test
    # @param[in]    gfx_index as optional
    # @return       True if watermark verification was done on a minimum of 1 plane, else False
    def verify_watermarks(self, is_48hz_verification=False, gfx_index = 'gfx_0'):
        logging.info("GEN9 Watermarks Verification Module")

        max_pipes = self.max_pipes
        max_planes = self.max_planes

        plane_list = self.get_plane_params(max_pipes, max_planes, gfx_index)
        pipe_list = self.get_pipe_params(max_pipes, is_48hz_verification, gfx_index)

        self.print_pipe_params(pipe_list, max_pipes)
        self.print_plane_params(plane_list, max_pipes, max_planes)

        programmed_lp_wm = self.get_programmed_lp_watermarks(max_pipes, max_planes, gfx_index)
        latency = self.get_memory_latency()

        programmed_trans_wm = self.get_programmed_trans_watermarks(max_pipes, max_planes, gfx_index)
        programmed_line_time = self.get_programmed_line_time(max_pipes, gfx_index)

        workarounds = self.get_workarounds(plane_list, pipe_list, max_pipes, max_planes, gfx_index)

        status = self.check_min_dbuf_needed(plane_list, max_planes, max_pipes, gfx_index)

        ##
        # Skipping the exact WM level checks due to current limitation for arbitrated BW workaround verification.
        # Enabling WM verification with only check for Min DBuf distribution.
        # Enabling WM0 verification for all planes , WM0-7 verification for single display
        # TODO: Enable below WM verification after fixing the issue of arbitrated BW WA check.

        logging.info("INFO: Gen9 Workarounds status: {} {} ".format(workarounds[0], workarounds[1]))

        expected_line_time, expected_lp_wm, expected_trans_wm = self.get_expected_watermarks(plane_list, pipe_list,
                                                                                             latency, workarounds,
                                                                                             max_pipes, max_planes)

        status = self.verify_wm_line_time(expected_line_time, programmed_line_time, max_pipes, pipe_list)

        logging.info("====== Planes Watermarks Verification started =====")
        if status is True:
            status = self.verify_lp_watermarks_gen9(expected_lp_wm, programmed_lp_wm, max_pipes, max_planes, plane_list, gfx_index)
        if status is True:
            if self.platform == 'bxt':
                status = self.verify_trans_wm(expected_trans_wm, programmed_trans_wm, max_pipes, max_planes, plane_list)
        logging.info("====== Planes Watermarks Verification ended =====")

        logging.info("======Cursor Watermarks verification started ========")
        cursor_plane_list = self.get_cursor_plane_params(max_pipes, gfx_index)

        programmed_cur_lp_wm = self.get_programmed_cursor_lp_watermarks(max_pipes, gfx_index)
        programmed_cur_trans_wm = self.get_programmed_cursor_trans_watermarks(max_pipes, gfx_index)

        expected_line_time, expected_cur_lp_wm, expected_cur_trans_wm = self.get_expected_watermarks(cursor_plane_list,
                                                                                                     pipe_list, latency,
                                                                                                     workarounds,
                                                                                                     max_pipes, 1)
        # setting plane count to 1 since there is only 1 cursor plane per pipe

        if status is True:
            status = self.verify_lp_watermarks_gen9(expected_cur_lp_wm, programmed_cur_lp_wm, max_pipes, 1,
                                                    cursor_plane_list, gfx_index)
            # setting plane count to 1 since there is only 1 cursor plane per pipe
        if status is True:
            if self.platform == 'bxt':
                status = self.verify_trans_wm(expected_cur_trans_wm, programmed_cur_trans_wm, max_pipes, 1,
                                              cursor_plane_list)
                # setting plane count to 1 since there is only 1 cursor plane per pipe
        logging.info("======Cursor Watermarks verification ended ========")
        return status

    ##
    # @brief        Check if minimum Dbuf is allocated for each active plane
    # @param[in]    plane_list of type PLANE()
    # @param[in]    plane_count
    # @param[in]    pipe_count
    # @param[in]    gfx_index as optional
    # @return       True if min Dbuf is allocated; False, otherwise
    def check_min_dbuf_needed(self, plane_list, plane_count, pipe_count, gfx_index='gfx_0'):

        ##
        # BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/12716
        # Note: Current implementation is only for 0 degree rotation scenarios
        # TODO: Extend this function for all 90/180/270 degree rotation scenarios

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
                    if (plane_obj.uiPlaneTilingFormat == wm_util.SURFACE_MEMORY_X_TILED) or \
                            (plane_obj.uiPlaneTilingFormat == wm_util.SURFACE_MEMORY_LINEAR):

                        if 'PLANAR' in wm_util.GEN9_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']:
                            min_dbuf_needed = 2 * wm_util.MIN_DBUF_X_TILE
                            # Calculate separate for Y and UV plane
                        else:
                            min_dbuf_needed = wm_util.MIN_DBUF_X_TILE

                    ##
                    # Planes using Y tiled memory formats must allocate blocks for a minimum number of scan-lines worth
                    # of data.
                    #
                    # Y tiled minimum allocation = Ceil [(4 * Plane source width * Plane Bpp)/512] * MinScanLines/4 + 3
                    #
                    # For YUV 420 Planar formats (NV12, P0xx), buffer allocation is done for Y and UV surfaces
                    # separately. Treat Y and UV surface as 2 separate planes. Also, the plane height and plane width
                    # for the UV plane should be halved.
                    else:
                        if 'PLANAR' in wm_util.GEN9_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']:
                            min_dbuf_needed = (math.ceil(float(4 * (plane_obj.lPlaneHorizontal / 2) *
                                                               plane_obj.uiPlaneBpp) / 512) * 8 / 4 + 3 +
                                               # UV Plane
                                               math.ceil(float(4 * plane_obj.lPlaneHorizontal *
                                                               plane_obj.uiPlaneBpp) / 512) * 8 / 4 + 3
                                               # Y Plane
                                               )
                        else:
                            min_dbuf_needed = math.ceil(
                                float(4 * plane_obj.lPlaneHorizontal * plane_obj.uiPlaneBpp) / 512) * 8 / 4 + 3

                    ##
                    # For Planar formats on Gen9/10, half of the buffer will be stored in PLANE_NV12_BUF_CFG registers
                    if 'PLANAR' in wm_util.GEN9_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']:
                        plane_nv12_buf_reg = 'PLANE_NV12_BUF_CFG_' + wm_util.PLANE_NAME[plane_idx] + '_' + \
                                             wm_util.PIPE_NAME[pipe_idx]
                        plane_nv12_buf = self.mmio_read.read('PLANE_BUF_CFG_REGISTER', plane_nv12_buf_reg,
                                                             self.platform, gfx_index=gfx_index)

                        plane_obj.uiBufferAllocated = plane_obj.uiBufferAllocated + \
                            plane_nv12_buf.__getattribute__("buffer_end") - \
                            plane_nv12_buf.__getattribute__("buffer_start") + 1

                    ##
                    # Compare actual and expected min dbuf allocated
                    if plane_obj.uiBufferAllocated < min_dbuf_needed:
                        logging.critical("FAIL: Minimum DBuf not allocated for PLANE_{}_{}:"
                                         "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                         .format(wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated))
                        status = False
                        gdhm.report_bug(
                            title="[OS][DBUF] Minimum DBuf not allocated for PLANE_{}_{}:"
                                  "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                .format(wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E1
                        )
                    else:
                        logging.info("PASS: Minimum DBuf allocated for PLANE_{}_{}:"
                                     "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                     .format(wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                             min_dbuf_needed, plane_obj.uiBufferAllocated))

        return status

    ##
    # @brief        Check if workarounds are applicable
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    pipe_count
    # @param[in]    plane_count (parameters help re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional
    # @return       WATERMARK() object containing list of all plane watermark blocks and lines
    def get_workarounds(self, plane_list, pipe_list, pipe_count, plane_count, gfx_index='gfx_0'):

        arbitrated_bw = self.get_arbitrated_bw(plane_list, pipe_list, pipe_count, plane_count)
        system_bw = self.get_system_bw(gfx_index)
        memory_rank, memory_channel = self.get_memory_rank_channel()
        is_tile_y_plane = self.check_for_tile_y(plane_list, pipe_count, plane_count)
        wa = [False, False]

        if is_tile_y_plane and (arbitrated_bw > system_bw * 0.2):
            wa[0] = True
        elif (arbitrated_bw > system_bw * 0.35) and (memory_rank == 1) and (memory_channel == 2):
            wa[1] = True
        elif arbitrated_bw > system_bw * 0.6:
            wa[1] = True

        return wa

    ##
    # @brief        Get Arbitrated BW
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    pipe_count
    # @param[in]    plane_count (parameters help re-usability for future platforms if needed)
    # @return       arbitrated bandwidth in MHZ
    def get_arbitrated_bw(self, plane_list, pipe_list, pipe_count, plane_count):
        active_pipes = 0
        max_pipe_bw = 0
        for pipe_idx in range(pipe_count):
            if pipe_list[pipe_idx].fPixelRate != 0:
                active_pipes += 1
                active_planes = 0
                max_plane_bw = 0
                for plane_idx in range(plane_count):
                    if plane_list[plane_idx].bStatus:
                        active_planes += 1
                        plane_bw = pipe_list[pipe_idx].fPixelRate * pipe_list[pipe_idx].fPipeDownscalingFactor * \
                            plane_list[pipe_idx * plane_count + plane_idx].fPlaneDownscalingFactor * \
                            plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp
                        if plane_bw > max_plane_bw:
                            max_plane_bw = plane_bw
                pipe_bw = active_planes * max_plane_bw
                if pipe_bw > max_pipe_bw:
                    max_pipe_bw = pipe_bw

        return active_pipes * max_pipe_bw * 1.0

    ##
    # @brief        Get system BW
    # @param[in]    gfx_index as optional
    # @return       system bandwidth in MHZ
    def get_system_bw(self, gfx_index='gfx_0'):

        if self.platform == 'bxt':
            memory_freq_reg = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_FREQUENCY_BXT, gfx_index)
            memory_freq_ratio = self.read_from_mmio_value(memory_freq_reg, wm_util.BITMAP_MEMORY_FREQ_RATIO_BXT)
            # in BXT case , memory frequency is in steps of 133.33Mhz
            raw_system_bw = memory_freq_ratio * 133.33
        else:
            memory_freq_reg = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_FREQUENCY_GEN9, gfx_index)
            memory_freq_ratio = self.read_from_mmio_value(memory_freq_reg, wm_util.BITMAP_MEMORY_FREQ_RATIO_GEN9)
            # in non BXT case , memory frequency is in steps of 133.33 * 16 = 2133.28 Mhz
            memory_rank, memory_channel_count = self.get_memory_rank_channel()
            raw_system_bw = memory_freq_ratio * 2133.28 * memory_channel_count
        return raw_system_bw

    ##
    # @brief        Get memory rank and channel
    # @return       memory rank and memory channel
    def get_memory_rank_channel(self):
        memory_channel_count = 0
        memory_rank = 1
        memory_rank_ch_0 = 1
        memory_rank_ch_1 = 1

        if self.platform == 'bxt':
            memory_channel_0 = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_FREQUENCY_BXT, 'gfx_0')
            memory_channel_1 = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_FREQUENCY_BXT, 'gfx_0')
            if self.read_from_mmio_value(memory_channel_0, wm_util.BITMAP_MEMORY_CHANNEL_0_BXT) != 0:
                memory_channel_count += 1
            if self.read_from_mmio_value(memory_channel_1, wm_util.BITMAP_MEMORY_CHANNEL_1_BXT) != 0:
                memory_channel_count += 1
        else:
            memory_channel_0 = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_CHANNEL_0_GEN9, 'gfx_0')
            memory_channel_1 = self.driver_interface_.mmio_read(wm_util.REG_MEMORY_CHANNEL_1_GEN9, 'gfx_0')
            if memory_channel_0 > 0:
                memory_channel_count += 1
            if memory_channel_1 > 0:
                memory_channel_count += 1
            #  # if any one slot has dual rank memory, then consider as dual rank
            if (memory_channel_0 & wm_util.BITMAP_MEMORY_RANK_SLOT_0_GEN9 != 0) or (
                    memory_channel_0 & wm_util.BITMAP_MEMORY_RANK_SLOT_1_GEN9 != 0):
                memory_rank_ch_0 = 2
            if (memory_channel_1 & wm_util.BITMAP_MEMORY_RANK_SLOT_0_GEN9 != 0) or (
                    memory_channel_1 & wm_util.BITMAP_MEMORY_RANK_SLOT_1_GEN9 != 0):
                memory_rank_ch_1 = 2
                #  # if both slots have single rank memory then consider as dual rank ,
                # since default value of 0 denotes single rank ,  we need to check if channel is enabled as well
            if ((memory_channel_0 & wm_util.BITMAP_MEMORY_CHANNEL_ENABLE_GEN9) > 0) and (
                    (memory_channel_0 & wm_util.BITMAP_MEMORY_RANK_SLOT_0_GEN9) == 0) and (
                    (memory_channel_0 & wm_util.BITMAP_MEMORY_RANK_SLOT_1_GEN9) == 0):
                memory_rank_ch_0 = 2
            if ((memory_channel_1 & wm_util.BITMAP_MEMORY_CHANNEL_ENABLE_GEN9) > 0) and (
                    (memory_channel_1 & wm_util.BITMAP_MEMORY_RANK_SLOT_0_GEN9) == 0) and (
                    (memory_channel_1 & wm_util.BITMAP_MEMORY_RANK_SLOT_1_GEN9) == 0):
                memory_rank_ch_1 = 2
            memory_rank = min(memory_rank_ch_0, memory_rank_ch_1)

        return memory_rank, memory_channel_count

    ##
    # @brief        Check expected watermarks based on spec
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    latency list
    # @param[in]    workarounds list
    # @param[in]    pipe_count
    # @param[in]    plane_count (parameters help re-usability for future platforms if needed)
    # @return       LINETIME(), WATERMARK() and TRANSWATERMARK() objects
    def get_expected_watermarks(self, plane_list, pipe_list, latency, workarounds, pipe_count, plane_count):
        exp_watermarks = []
        exp_trans_watermarks = []
        exp_line_time = []

        for pipe_idx in range(0, pipe_count):
            exp_line_time_obj = watermark_base.PipeLinetimeObj()
            adjusted_pipe_pixel_rate = pipe_list[pipe_idx].fPixelRate * pipe_list[
                pipe_idx].fPipeDownscalingFactor
            adjusted_pipe_pixel_rate = (adjusted_pipe_pixel_rate * 2) if pipe_list[pipe_idx].bIsInterlaced \
                is True else adjusted_pipe_pixel_rate
            pipe_hor_total = pipe_list[pipe_idx].lHorizontalTotal
            if adjusted_pipe_pixel_rate > 0:
                exp_line_time_obj.fLineTime = round(8.0 * pipe_hor_total / adjusted_pipe_pixel_rate)
                if self.platform == 'bxt':
                    exp_line_time_obj.fLineTime = math.floor(exp_line_time_obj.fLineTime / 2)
            exp_line_time.append(exp_line_time_obj)
            for plane_idx in range(0, plane_count):
                exp_trans_wm_obj = watermark_base.PlaneTransWatermarkObj()
                for level in range(0, wm_util.LATENCY_LEVELS):
                    exp_plane_wm_obj = watermark_base.PlaneWatermarkObj()
                    current_latency = latency[level]
                    adjusted_plane_pixel_rate = round(adjusted_pipe_pixel_rate * plane_list[pipe_idx * plane_count +
                                                      plane_idx].fPlaneDownscalingFactor, 2)
                    bpp = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp
                    source_width = plane_list[pipe_idx * plane_count + plane_idx].lPlaneHorizontal
                    tiling = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat
                    tiling_text = wm_util.MEMORY_TILING_LIST.get(
                        plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat)

                    buffer_allocated = plane_list[pipe_idx * plane_count + plane_idx].uiBufferAllocated
                    plane_status = plane_list[pipe_idx * plane_count + plane_idx].bStatus

                    if adjusted_plane_pixel_rate > 0 and plane_status:
                        if (plane_list[pipe_idx * plane_count + plane_idx].uiPlaneRotation ==
                            wm_util.ROTATION_90) or \
                                (plane_list[pipe_idx * plane_count + plane_idx].uiPlaneRotation ==
                                 wm_util.ROTATION_270):
                            if plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 1:
                                tile_y_min_lines = 16
                            elif plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 2:
                                tile_y_min_lines = 8
                            else:
                                tile_y_min_lines = 4
                        else:
                            tile_y_min_lines = 4

                        if workarounds[0]:
                            tile_y_min_lines = tile_y_min_lines * 2
                            if tiling == wm_util.SURFACE_MEMORY_X_TILED:
                                current_latency = current_latency + 15

                        if workarounds[1]:
                            current_latency = current_latency + 15

                        method1 = round(current_latency *
                                        float(adjusted_plane_pixel_rate) * bpp / wm_util.DBUF_BLOCK_SIZE, 2)

                        bytes_per_line = source_width * bpp
                        if tiling == wm_util.SURFACE_MEMORY_LINEAR:
                            blocks_per_line = math.ceil(bytes_per_line / wm_util.DBUF_BLOCK_SIZE) + 1
                        elif tiling == wm_util.SURFACE_MEMORY_Y_LEGACY_TILED:
                            blocks_per_line = math.ceil(
                                tile_y_min_lines * bytes_per_line / wm_util.DBUF_BLOCK_SIZE) / tile_y_min_lines
                        else:
                            blocks_per_line = math.ceil(bytes_per_line / wm_util.DBUF_BLOCK_SIZE)
                        method2 = round(math.ceil(
                            current_latency * adjusted_plane_pixel_rate / pipe_hor_total) * blocks_per_line, 2)

                        tile_y_min_blocks = tile_y_min_lines * blocks_per_line

                        lt_microseconds = pipe_hor_total / adjusted_plane_pixel_rate

                        if tiling == wm_util.SURFACE_MEMORY_X_TILED or \
                                tiling == wm_util.SURFACE_MEMORY_LINEAR:
                            if (bytes_per_line * pipe_hor_total / wm_util.DBUF_BLOCK_SIZE < 1) and (
                                    bytes_per_line / wm_util.DBUF_BLOCK_SIZE < 1):
                                sel_result_blocks = method2
                            elif buffer_allocated >= blocks_per_line:
                                sel_result_blocks = min(method1, method2)
                            elif current_latency >= lt_microseconds:
                                sel_result_blocks = min(method1, method2)
                            else:
                                sel_result_blocks = method1
                        else:
                            sel_result_blocks = max(method2, tile_y_min_blocks)

                        result_blocks = math.ceil(sel_result_blocks) + 1
                        result_lines = math.ceil(sel_result_blocks / blocks_per_line)

                        if level > 0 and tiling == wm_util.SURFACE_MEMORY_Y_LEGACY_TILED:
                            result_blocks = result_blocks + tile_y_min_blocks
                            result_lines = result_lines + tile_y_min_lines
                        if level > 0 and tiling != wm_util.SURFACE_MEMORY_Y_LEGACY_TILED:
                            result_blocks = result_blocks + 1

                        exp_plane_wm_obj.bStatus = False if ((result_blocks >= buffer_allocated) or (
                                (level > 0) and (result_lines > 31))) else True
                        exp_plane_wm_obj.fResultBlocks = result_blocks if exp_plane_wm_obj.bStatus is True else 0
                        exp_plane_wm_obj.fResultLines = result_lines if exp_plane_wm_obj.bStatus is True else 0
                        logging.debug("WM_{}_{}_{} adjustedpixclk={} bpp={} width={} tile={}({}) htotal={} "
                                      "blkperline={} M1={} M2={} YMin={} ResBlk={} ResLin={}"
                                      .format(wm_util.PLANE_NAME[plane_idx],
                                              wm_util.PIPE_NAME[pipe_idx], level, adjusted_plane_pixel_rate,
                                              bpp, source_width, tiling, tiling_text, pipe_hor_total, blocks_per_line,
                                              method1, method2, tile_y_min_blocks, exp_plane_wm_obj.fResultBlocks,
                                              exp_plane_wm_obj.fResultLines))

                        if level == 0:
                            transition_offset_blocks = wm_util.TRANS_MINIMUM_GEN9 + wm_util.TRANS_AMOUNT_GEN9
                            transition_y_min = 2 * tile_y_min_blocks
                            if (tiling == wm_util.SURFACE_MEMORY_X_TILED) or (
                                    tiling == wm_util.SURFACE_MEMORY_LINEAR):
                                trans_result_blocks = sel_result_blocks + transition_offset_blocks
                            else:
                                trans_result_blocks = max(sel_result_blocks,
                                                          transition_y_min) + transition_offset_blocks
                            trans_result_blocks = math.ceil(trans_result_blocks) + 1
                            if tiling != wm_util.SURFACE_MEMORY_Y_LEGACY_TILED:
                                trans_result_blocks = trans_result_blocks + 1
                            exp_trans_wm_obj.bStatus = False if (trans_result_blocks >= buffer_allocated) else True
                            exp_trans_wm_obj.fResultBlocks = trans_result_blocks if exp_trans_wm_obj.bStatus is True \
                                else 0

                    exp_watermarks.append(exp_plane_wm_obj)
                exp_trans_watermarks.append(exp_trans_wm_obj)

        return exp_line_time, exp_watermarks, exp_trans_watermarks

    ##
    # @brief        compare main and lp watermarks WM0-WM7
    # @param[in]    exp_wm as expected watermark
    # @param[in]    prog_wm as programmed watermarks
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    plane_list struct containing plane objects of type PLANEOBJ()
    # @param[in]    gfx_index as optional
    # @return       bool
    def verify_lp_watermarks_gen9(self, exp_wm, prog_wm, pipe_count, plane_count, plane_list, gfx_index='gfx_0'):
        is_cursor_wm = False
        wm_status = True
        failure = ''
        if plane_count > 1:
            # Display Plane verification
            status = False
        else:
            # Cursor Plane verification,
            # Sometimes no cursor plane may be enabled, this is fine, so start with True return status
            status = True
            is_cursor_wm = True

        skip_lpwm_check = False
        test_ctrl_flag = registry.FeatureTestControl(gfx_index)
        if test_ctrl_flag.cxsr_disable == 1:
            logging.warning(
                "FeatureTestControl Registry: Expected = CxSR Enable(Bit0: 0) Actual = CxSR disable (Bit0: 1): "
                "Skipping LP Watermark verification")
            skip_lpwm_check = True

        for pipe_idx in range(pipe_count):
            status = True
            for plane_idx in range(plane_count):
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    for level in range(wm_util.LATENCY_LEVELS):
                        if level != 0 and skip_lpwm_check:
                            exp_wm_status = False
                        else:
                            exp_wm_status = exp_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                   wm_util.LATENCY_LEVELS + level].bStatus
                        prog_wm_status = prog_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                 wm_util.LATENCY_LEVELS + level].bStatus
                        exp_wm_result_blocks = exp_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                      wm_util.LATENCY_LEVELS + level].fResultBlocks
                        prog_wm_result_blocks = prog_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                        wm_util.LATENCY_LEVELS + level].fResultBlocks
                        exp_wm_result_lines = exp_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                     wm_util.LATENCY_LEVELS + level].fResultLines
                        prog_wm_result_lines = prog_wm[pipe_idx * plane_count * wm_util.LATENCY_LEVELS + plane_idx *
                                                       wm_util.LATENCY_LEVELS + level].fResultLines
                        ##
                        # Check for current config is single and verify all WM for active display
                        # TO DO enable this code once driver issue resolve.
                        # if (self.current_config is "SINGLE"):
                        #     logging.info("for single display case")
                        #     if exp_wm_status is not prog_wm_status:
                        #         # WM Status Mismatch
                        #         failure = '--> WM STATUS MISMATCH'
                        #         status = False
                        #     if (exp_wm_status is True) and (prog_wm_status is True):
                        #         if exp_wm_result_blocks != prog_wm_result_blocks:
                        #             # WM Results blocks Mismatch
                        #             failure = '--> BLOCKS/LINES MISMATCH'
                        #             status = False
                        #         if exp_wm_result_lines != prog_wm_result_lines:
                        #             # WM Results line Mismatch
                        #             failure = '--> BLOCKS/LINES MISMATCH'
                        #             status = False
                        #     logging.info('{}: {}_{}_{}\t[WM_Status, Blocks, Lines]\t'
                        #                  'Expected: [{}, {}, {}]\tActual: [{}, {}, {}]\t{}'
                        #                  .format('PASS' if status is True else 'FAIL',
                        #                          'PLANE_WM_' + str(PLANE_NAME[plane_idx]) if is_cursor_wm is False
                        #                          else 'CUR_WM', PIPE_NAME[pipe_idx], level,
                        #                          str(exp_wm_status).upper(), int(exp_wm_result_blocks),
                        #                          int(exp_wm_result_lines),
                        #                          str(prog_wm_status).upper(), int(prog_wm_result_blocks),
                        #                          int(prog_wm_result_lines), failure))
                        # ##
                        # # Current config is not single and verify WM0 for all planes.
                        # else:
                        #     logging.info("for multi display config")
                        if level == 0:
                            if exp_wm_status is not prog_wm_status:
                                # WM Status Mismatch
                                failure = '--> WM STATUS MISMATCH'
                                status = False
                            logging.info('{}: {}_{}_{}\t[WM_Status]\t'
                                         'Expected: [{}]\tActual: [{}]\t{}'
                                         .format('PASS' if status is True else 'FAIL',
                                                 'PLANE_WM_' + str(
                                                     wm_util.PLANE_NAME[plane_idx]) if is_cursor_wm is False
                                                 else 'CUR_WM', wm_util.PIPE_NAME[pipe_idx], level,
                                                 str(exp_wm_status).upper(),
                                                 str(prog_wm_status).upper(), failure))
                        logging.debug('level: {},\t wm_status{},\t status{}'.format(level, wm_status, status))
                        wm_status = wm_status & status
                        status = True  # restoring back to true for next loop
                        failure = ''  # restoring string back to null
                        logging.debug('updated wm_status:{}\t'.format(wm_status))
        return wm_status
