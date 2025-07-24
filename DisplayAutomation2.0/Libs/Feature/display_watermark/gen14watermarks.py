######################################################################################
# @file             gen14watermarks.py
# @addtogroup       PyLibs_DisplayWatermark
# @brief            GEN14 specific module for DisplayWatermark
# @author           Suraj Gaikwad, Bhargav Adigarla
######################################################################################
import importlib
import logging
import math

from Libs.Feature.display_watermark import watermark_base
from Libs.Feature.display_watermark import watermark_utils as wm_util
from Libs.Feature.display_watermark import gen14_dbuf_table


##
# @brief        This class contains Gen14 watermark and dbuf verification API's
class Gen14Watermarks(watermark_base.DisplayWatermarkBase):
    max_pipes = wm_util.MAX_PIPES_GEN14
    max_planes = wm_util.MAX_PLANES_GEN14
    sagv_latency = 0

    ##
    # @brief        Gen14Watermarks default __init__ function
    # @param[in]    gfx_index as optional
    def __init__(self, gfx_index='gfx_0'):
        watermark_base.DisplayWatermarkBase.__init__(self, gfx_index=gfx_index)

    ##
    # @brief        Verifies watermark values programmed by driver for GEN14
    # @param[in]    is_48hz_verification as optional if called 48hz test
    # @param[in]    gfx_index as optional
    # @param[in]    min_dbuf_check as optional
    # @return       True if watermark verification was done on a minimum of 1 plane, else False
    def verify_watermarks(self, is_48hz_verification=False, gfx_index = 'gfx_0', min_dbuf_check=False):
        max_pipes = self.max_pipes
        max_planes = self.max_planes
        latency = []

        plane_list = self.get_plane_params(max_pipes, max_planes, gfx_index)
        pipe_list = self.get_pipe_params(max_pipes, is_48hz_verification, gfx_index)

        self.print_pipe_params(pipe_list, max_pipes)
        self.print_plane_params(plane_list, max_pipes, max_planes)

        # get_programmed_lp_watermarks() and get_memory_latency() are same as Gen9, so inherit from Gen9
        programmed_lp_wm = self.get_programmed_lp_watermarks(max_pipes, max_planes, gfx_index)
        latency = self.gen14_get_memory_latency()
        logging.info("Memory Latencies in microseconds L0:{} L1:{} L2:{} L3:{} L4:{} L5:{}"
                     .format(latency[0], latency[1], latency[2], latency[3], latency[4], latency[5]))

        programmed_trans_wm = self.get_programmed_trans_watermarks(max_pipes, max_planes, gfx_index)
        programmed_line_time = self.get_programmed_line_time(max_pipes, gfx_index)

        # No workarounds for GEN14
        workarounds = [False, False]

        logging.info("============= DBUF DISTRIBUTION VERIFICATION STARTED =============")
        status = self.validate_dbuf_distribution(pipe_list, plane_list, max_pipes, max_planes, gfx_index)

        if status is True:
            status = self.check_min_dbuf_needed(plane_list, max_planes, max_pipes)
        else:
            logging.info('Validation of Min DBuf allocation skipped !!')
        logging.info("============== DBUF DISTRIBUTION VERIFICATION ENDED ==============")
        expected_lp_wm = expected_sagv_wm = expected_trans_wm = expected_trans_sagv_wm = None

        if status is True:
            expected_line_time, expected_lp_wm, expected_trans_wm, expected_sagv_wm, expected_trans_sagv_wm = \
                self.get_expected_watermarks(plane_list, pipe_list,latency, workarounds,max_pipes, max_planes)
            status = self.verify_wm_line_time(expected_line_time, programmed_line_time, max_pipes, pipe_list)
        else:
            logging.info('Linetime verification skipped !!')

        logging.info("============= PLANES WATERMARK VERIFICATION STARTED =============")
        if status is True:
            status = self.verify_lp_watermarks(expected_lp_wm, programmed_lp_wm, max_pipes, max_planes, plane_list, gfx_index)
            if self.platform in ['mtl']:
                status_sagv = self.verify_sagv_watermark(expected_sagv_wm, max_pipes, max_planes, plane_list, gfx_index=gfx_index)
                status &= status_sagv

        else:
            logging.info('Planes Main and LP Watermark verification skipped !!')
        if status is True:
            status = self.verify_trans_wm(expected_trans_wm, programmed_trans_wm, max_pipes, max_planes, plane_list)
            if self.platform in ['mtl']:
                status_sagv = self.verify_trans_sagv_watermark(expected_trans_sagv_wm, max_pipes, max_planes,
                                                               plane_list, gfx_index =gfx_index)
                status &= status_sagv

        else:
            logging.info('Planes Transition Watermark verification skipped !!')
        logging.info("============== PLANES WATERMARK VERIFICATION ENDED ==============")

        '''
        cursor_plane_list = self.get_cursor_plane_params(max_pipes, gfx_index)

        programmed_cur_lp_wm = self.get_programmed_cursor_lp_watermarks(max_pipes, gfx_index)
        programmed_cur_trans_wm = self.get_programmed_cursor_trans_watermarks(max_pipes, gfx_index)

        # Setting plane count to 1 since there is only 1 cursor plane per pipe
        expected_line_time, expected_cur_lp_wm, expected_cur_trans_wm, \
            expected_cur_sagv_wm, expected_cur_trans_sagv_wm= self.get_expected_watermarks(cursor_plane_list,
                                                                                                     pipe_list, latency,
                                                                                                     workarounds,
                                                                                                     max_pipes, 1)

        # Note: Disabling Cursor WM as Cursor is not exercised and observing sporadic errors in GTA
        # due to Cursor not connected to all systems.
        # TODO: Revisit once Cursor issues are fixed and can be enabled in cadence.
        logging.info("============= CURSOR WATERMARK VERIFICATION STARTED =============")
        if status is True:
            # Setting plane count to 1 since there is only 1 cursor plane per pipe
            status = self.verify_lp_watermarks(expected_cur_lp_wm, programmed_cur_lp_wm, max_pipes, 1,
                                               cursor_plane_list, gfx_index)
            if self.platform in ['mtl']:
                status_sagv = self.verify_sagv_watermark(expected_cur_sagv_wm, max_pipes, max_planes, plane_list,
                                                         is_cursor_wm=True, gfx_index=gfx_index)
                status &= status_sagv
        else:
            logging.info('Cursor Main and LP Watermark verification skipped !!')
        if status is True:
            # Setting plane count to 1 since there is only 1 cursor plane per pipe
            status = self.verify_trans_wm(expected_cur_trans_wm, programmed_cur_trans_wm, max_pipes, 1,
                                          cursor_plane_list)
            if self.platform in ['mtl']:
                status_sagv = self.verify_trans_sagv_watermark(expected_cur_trans_sagv_wm, max_pipes, max_planes,
                                                               plane_list, is_cursor_wm=True)
                status &= status_sagv
        else:
            logging.info('Cursor Transition Watermark verification skipped !!')
        logging.info("============== CURSOR WATERMARK VERIFICATION ENDED ==============")
        '''

        return status

    ##
    # @brief        Check expected watermarks based on spec
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    latency list
    # @param[in]    workarounds list
    # @param[in]    pipe_count
    # @param[in]    plane_count (parameters help re-usability for future platforms if needed)
    # @return       GEN14WATERMARK() object containing list of all active plane expected watermark blocks and lines
    def get_expected_watermarks(self, plane_list, pipe_list, latency, workarounds, pipe_count, plane_count):
        exp_watermarks = []
        exp_trans_watermarks = []
        exp_watermarks_sagv = []
        exp_trans_watermarks_sagv = []
        exp_line_time = []

        for pipe_idx in range(0, pipe_count):
            exp_line_time_obj = watermark_base.PipeLinetimeObj()
            adjusted_pipe_pixel_rate = pipe_list[pipe_idx].fPixelRate * \
                pipe_list[pipe_idx].fPipeDownscalingFactor
            adjusted_pipe_pixel_rate = (adjusted_pipe_pixel_rate * 2) if \
                pipe_list[pipe_idx].bIsInterlaced is True else adjusted_pipe_pixel_rate
            pipe_hor_total = pipe_list[pipe_idx].lHorizontalTotal
            if adjusted_pipe_pixel_rate > 0:
                exp_line_time_obj.fLineTime = math.ceil(8.0 * pipe_hor_total / adjusted_pipe_pixel_rate)
            exp_line_time.append(exp_line_time_obj)
            for plane_idx in range(0, plane_count):
                exp_trans_wm_obj = watermark_base.PlaneTransWatermarkObj()
                exp_trans_wm_sagv_obj = watermark_base.PlaneTransWatermarkObj()
                exp_plane_wm_sagv_obj = watermark_base.PlaneWatermarkObj()
                for level in range(0, wm_util.LATENCY_LEVELS):
                    exp_plane_wm_obj = watermark_base.PlaneWatermarkObj()
                    current_latency = latency[level]
                    adjusted_plane_pixel_rate = round(adjusted_pipe_pixel_rate *
                                                      plane_list[pipe_idx * plane_count +
                                                                 plane_idx].fPlaneDownscalingFactor, 2)
                    bpp = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp
                    pixel_format_text = self.get_pixel_format_text(
                        plane_list[pipe_idx * plane_count + plane_idx].uiPixelFormat)
                    yuv_component = plane_list[pipe_idx * plane_count + plane_idx].uiPlanarYUV420Component

                    # NV12 and P0xx formats UV surface is in plane < 6 and its bpp is 2 times Y surface bpp
                    # Y surface will be there in plane 6 or 7
                    if pixel_format_text in ['YUV 420 PLANAR 8 BPC', 'YUV10 420 PLANAR 10 BPC',
                                             'YUV 420 PLANAR 12 BPC', 'YUV 420 PLANAR 16 BPC'] and (yuv_component == 0):
                        bpp = bpp * 2
                    source_width = plane_list[pipe_idx * plane_count + plane_idx].lPlaneHorizontal
                    tiling = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat
                    pipe_hor_total = pipe_list[pipe_idx].lHorizontalTotal
                    buffer_allocated = plane_list[pipe_idx * plane_count + plane_idx].uiBufferAllocated
                    plane_status = plane_list[pipe_idx * plane_count + plane_idx].bStatus
                    dbuf_block_size = wm_util.DBUF_BLOCK_SIZE
                    tiling_text = wm_util.MEMORY_TILING_LIST.get(plane_list[pipe_idx * plane_count +
                                                                            plane_idx].uiPlaneTilingFormat)

                    if adjusted_plane_pixel_rate > 0 and plane_status is True:
                        if (plane_list[
                                pipe_idx * plane_count + plane_idx].uiPlaneRotation == wm_util.ROTATION_90) \
                                or (plane_list[pipe_idx * plane_count + plane_idx].uiPlaneRotation ==
                                    wm_util.ROTATION_270):
                            if plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 1:
                                tile_y_min_lines = 16
                            elif plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp == 2:
                                tile_y_min_lines = 8
                            else:
                                tile_y_min_lines = 4
                        else:
                            tile_y_min_lines = 4
                        # Step-1 Method1 calculation
                        method1 = round((current_latency * adjusted_plane_pixel_rate * bpp / dbuf_block_size), 2) + 1
                        method1_sagv = round((self.sagv_latency * adjusted_plane_pixel_rate * bpp /
                                              dbuf_block_size), 2) + 1

                        # Step-2 Method 2 calculation
                        bytes_per_line = source_width * bpp
                        if tiling == wm_util.SURFACE_MEMORY_LINEAR:
                            blocks_per_line = math.ceil(bytes_per_line / dbuf_block_size) + 1
                        elif tiling in [wm_util.SURFACE_MEMORY_TILED_4,
                                        wm_util.SURFACE_MEMORY_Y_LEGACY_TILED]:
                            blocks_per_line = math.ceil((tile_y_min_lines *
                                                         bytes_per_line / dbuf_block_size) + 1) / tile_y_min_lines
                        else:
                            blocks_per_line = math.ceil(bytes_per_line / dbuf_block_size) + 1
                        method2 = round(math.ceil(current_latency * adjusted_plane_pixel_rate / pipe_hor_total) *
                                        blocks_per_line, 2)
                        method2_sagv = round(math.ceil(self.sagv_latency * adjusted_plane_pixel_rate / pipe_hor_total) *
                                             blocks_per_line, 2)

                        # Step-3 Calculate Y tile minimum
                        tile_y_min_blocks = tile_y_min_lines * blocks_per_line

                        # Step-4 Select Watermark result
                        lt_microseconds = pipe_hor_total / adjusted_plane_pixel_rate

                        if tiling == wm_util.SURFACE_MEMORY_X_TILED or tiling == wm_util.SURFACE_MEMORY_LINEAR:
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

                        if tiling == wm_util.SURFACE_MEMORY_X_TILED or tiling == wm_util.SURFACE_MEMORY_LINEAR:
                            if (bpp * pipe_hor_total / dbuf_block_size < 1) and (bytes_per_line / dbuf_block_size < 1):
                                sel_result_blocks_sagv = method2_sagv
                            elif buffer_allocated >= blocks_per_line:
                                sel_result_blocks_sagv = method2_sagv
                            elif self.sagv_latency >= lt_microseconds:
                                sel_result_blocks_sagv = method2_sagv
                            else:
                                sel_result_blocks_sagv = method1_sagv
                        else:
                            sel_result_blocks_sagv = max(method2_sagv, tile_y_min_blocks)

                        # Step-5 Convert Result result to block and lines
                        result_blocks = math.ceil(sel_result_blocks) + 1
                        result_blocks_sagv = math.ceil(sel_result_blocks_sagv) + 1
                        result_lines = math.ceil(sel_result_blocks / blocks_per_line)
                        result_lines_sagv = math.ceil(sel_result_blocks_sagv / blocks_per_line)

                        if tiling in [wm_util.SURFACE_MEMORY_TILED_4,
                                      wm_util.SURFACE_MEMORY_Y_LEGACY_TILED]:
                            if result_lines % tile_y_min_lines == 0:
                                extra_lines = tile_y_min_lines
                                extra_lines_sagv = tile_y_min_lines
                            else:
                                extra_lines = (tile_y_min_lines * 2) - (result_lines % tile_y_min_lines)
                                extra_lines_sagv = (tile_y_min_lines * 2) - (result_lines_sagv % tile_y_min_lines)
                            min_dbuf = (result_lines + extra_lines) * blocks_per_line
                            min_dbuf_sagv = (result_lines_sagv + extra_lines_sagv) * blocks_per_line
                        else:
                            min_dbuf = math.ceil(result_blocks + (result_blocks * 0.1))
                            min_dbuf_sagv = math.ceil(result_blocks_sagv + (result_blocks_sagv * 0.1))

                        # Step-6 Compare against the maximum
                        exp_plane_wm_obj.bStatus = False if ((result_blocks >= buffer_allocated) or
                                                             (min_dbuf >= buffer_allocated) or
                                                             ((level > 0) and (result_lines > 255))) else True

                        if exp_plane_wm_obj.bStatus == True and level>0:
                            exp_plane_wm_obj.bStatus = True if self.verify_vblank_requirement\
                                                               (pipe_list[pipe_idx].fPixelRate,
                                                                pipe_list[pipe_idx].lHorizontalTotal,
                                                                pipe_idx, plane_idx, exp_watermarks[0].fResultLines,
                                                                current_latency) is True else False

                        exp_plane_wm_obj.fResultBlocks = result_blocks if exp_plane_wm_obj.bStatus is True else 0
                        exp_plane_wm_obj.fResultLines = result_lines if exp_plane_wm_obj.bStatus is True else 0

                        logging.debug(
                            "WM_{}_{}_{} adjustedpixclk={} bpp={} width={} tile={}({}) htotal={} blkperline={} "
                            "M1={} M2={} YMin={} ResBlk={} ResLin={}".format(
                                wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx], level,
                                adjusted_plane_pixel_rate, bpp,
                                source_width, tiling, tiling_text, pipe_hor_total, blocks_per_line, method1, method2,
                                tile_y_min_blocks, exp_plane_wm_obj.fResultBlocks, exp_plane_wm_obj.fResultLines))

                        # For Transition Watermark
                        if level == 0:
                            # Calculate transition offset
                            transition_offset_blocks = wm_util.TRANS_MINIMUM_GEN11 + wm_util.TRANS_AMOUNT_GEN11
                            # Calculate transition Y tile minimum
                            transition_y_min = 2 * tile_y_min_blocks
                            # Select Watermark result
                            if (tiling == wm_util.SURFACE_MEMORY_X_TILED) or (
                                    tiling == wm_util.SURFACE_MEMORY_LINEAR):
                                trans_result_blocks = sel_result_blocks + transition_offset_blocks
                            else:
                                trans_result_blocks = max(sel_result_blocks, transition_y_min) + \
                                                      transition_offset_blocks
                            trans_result_blocks = math.ceil(trans_result_blocks) + 1
                            # Compare againts max and update resultblock
                            exp_trans_wm_obj.bStatus = False if (trans_result_blocks >= buffer_allocated) else True
                            exp_trans_wm_obj.fResultBlocks = trans_result_blocks if \
                                exp_trans_wm_obj.bStatus is True else 0

                            if self.platform in ['mtl']:
                                # Calculate SAGV WM using the SAGV latency
                                exp_plane_wm_sagv_obj.bStatus = False if ((result_blocks_sagv >= buffer_allocated) or
                                                                          (min_dbuf_sagv >= buffer_allocated) or
                                                                          (min_dbuf >= buffer_allocated) or
                                                                          ((level > 0) and (result_lines_sagv > 255))) \
                                    else True
                                exp_plane_wm_sagv_obj.fResultBlocks = result_blocks_sagv if \
                                    exp_plane_wm_sagv_obj.bStatus is True else 0
                                exp_plane_wm_sagv_obj.fResultLines = result_lines_sagv if \
                                    exp_plane_wm_sagv_obj.bStatus is True else 0

                                logging.debug(
                                    "SAGV_WM_{}_{} adjustedpixclk={} bpp={} width={} tile={}({}) htotal={} blkperline={} "
                                    "M1={} M2={} YMin={} ResBlk={} ResLin={} MinDbuf={}".format(
                                        wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                        adjusted_plane_pixel_rate, bpp, source_width, tiling, tiling_text,
                                        pipe_hor_total, blocks_per_line, method1_sagv, method2_sagv,
                                        tile_y_min_blocks, exp_plane_wm_sagv_obj.fResultBlocks,
                                        exp_plane_wm_sagv_obj.fResultLines, min_dbuf_sagv))

                                # Calculate Trans SAGV WM using SAGV latency
                                if (tiling == wm_util.SURFACE_MEMORY_X_TILED) or \
                                        (tiling == wm_util.SURFACE_MEMORY_LINEAR):
                                    trans_result_blocks_sagv = sel_result_blocks_sagv + transition_offset_blocks
                                else:
                                    trans_result_blocks_sagv = max(sel_result_blocks_sagv, transition_y_min) + \
                                                          transition_offset_blocks
                                trans_result_blocks_sagv = math.ceil(trans_result_blocks_sagv) + 1
                                # Compare againts max and update resultblock
                                exp_trans_wm_sagv_obj.bStatus = False if \
                                    (trans_result_blocks_sagv >= buffer_allocated) else True
                                exp_trans_wm_sagv_obj.fResultBlocks = trans_result_blocks_sagv if \
                                    exp_trans_wm_sagv_obj.bStatus is True else 0

                                logging.debug("TRANS_SAGV_WM_{}_{} tile={}({}) TransResBlk={} SelResBlks={} "
                                              "TransYmin={}"
                                              .format(wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                                      tiling, tiling_text, sel_result_blocks_sagv, transition_y_min,
                                                      exp_trans_wm_sagv_obj.fResultBlocks, ))

                    exp_watermarks.append(exp_plane_wm_obj)
                exp_trans_watermarks.append(exp_trans_wm_obj)

                exp_watermarks_sagv.append(exp_plane_wm_sagv_obj)
                exp_trans_watermarks_sagv.append(exp_trans_wm_sagv_obj)

        return exp_line_time, exp_watermarks, exp_trans_watermarks, exp_watermarks_sagv, exp_trans_watermarks_sagv

    ##
    # @brief        Get memory latency values
    # @return       list containing latencies
    def gen14_get_memory_latency(self):
        latency = [0 for _ in range(6)]

        # If latency WM0 is zero then add fabric latency of 6 microseconds
        fabric_latency = 6

        current_exec_env = self.system_utility.get_execution_environment_type()
        if current_exec_env is None:
            raise Exception('Test failed to identify the current execution environment')
        if current_exec_env in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            # Temp latencies hardcoded in xml used in pre-si env (only for Yangra)
            # For Post-Si, it will use the actual Mem latencies fetched from GTDRIVER MAILBOX
            latency = [4, 4, 4, 4, 4, 4, 4, 4]
            self.sagv_latency += latency[0]
        else:
            data_0 = self.driver_interface_.mmio_read(wm_util.LATENCY_SAGV, 'gfx_0')
            data_1 = self.driver_interface_.mmio_read(wm_util.LATENCY_LP0_LP1, 'gfx_0')
            data_2 = self.driver_interface_.mmio_read(wm_util.LATENCY_LP2_LP3, 'gfx_0')
            data_3 = self.driver_interface_.mmio_read(wm_util.LATENCY_LP4_LP5, 'gfx_0')
            logging.info("Punit values: LATENCY_SAGV - value0 {0}, LATENCY_LP0_LP1 - value1 {1}, "
                         "LATENCY_LP2_LP3 - value2 {2}, LATENCY_LP4_LP5 - value3 {3}"
                         .format(hex(data_0), hex(data_1), hex(data_2), hex(data_3)))

            self.sagv_latency = data_0 & 0x00001FFF
            latency[0] = data_1 & 0x00001FFF
            latency[1] = (data_1 & 0x1FFF0000) >> 16
            latency[2] = data_2 & 0x00001FFF
            latency[3] = (data_2 & 0x1FFF0000) >> 16
            latency[4] = data_3 & 0x00001FFF
            latency[5] = (data_3 & 0x1FFF0000) >> 16

        if latency[0] == 0:
            for i in range(0, len(latency)):
                latency[i] = latency[i] + fabric_latency

        # Memory latency level SAGV = SAGV block time + memory latency level 0
        self.sagv_latency += latency[0]

        logging.info("Memory Latencies in microseconds L0:{} L1:{} L2:{} L3:{} L4:{} L5:{}"
                     .format(latency[0], latency[1], latency[2], latency[3], latency[4], latency[5]))
        logging.info("SAGV Latency in microseconds :{}".format(self.sagv_latency))

        # Latency values should be in strict order
        for index in range(1,6):
            if latency[index] != 0 and latency[index] < latency[0]:
                latency[index] = latency[0]
            else:
                break

        return latency

    ##
    # @brief        Validate DBuf distribution across all active pipes
    # @param[in]    pipe_list of type PIPE()
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    gfx_index as optional
    # @return       True, if dbuf distribution is valid; False, otherwise
    def validate_dbuf_distribution(self, pipe_list, plane_list, pipe_count, plane_count, gfx_index='gfx_0'):
        enabled_pipes = 0
        status = True

        gen14_dbuf_distribution = gen14_dbuf_table.gen14_mtl_dbuf_distribution

        dbuf_ctl_value = importlib.import_module("registers.%s.DBUF_CTL_REGISTER" % self.platform)

        ##
        # Find all active pipes list
        for pipe_idx in range(0, pipe_count):
            if pipe_list[pipe_idx].bIsPipeEnable is True:
                enabled_pipes = enabled_pipes | (1 << pipe_list[pipe_idx].iPipeId)

        current_dbuf_allocations = gen14_dbuf_distribution[enabled_pipes]['allocation']
        current_enabled_slices = gen14_dbuf_distribution[enabled_pipes]['slices_enabled']

        ##
        # Verify Dbuf Slice Power state
        for slice_id in current_enabled_slices:
            dbuf_ctl_reg = 'DBUF_CTL_' + slice_id
            dbuf_ctl = self.mmio_read.read('DBUF_CTL_REGISTER', dbuf_ctl_reg, self.platform, gfx_index=gfx_index)

            if dbuf_ctl.__getattribute__("dbuf_power_state") == getattr(dbuf_ctl_value, 'dbuf_power_state_DISABLE'):
                logging.error('DBUF_CTL_{} status mismatch. \tExpected: Power State Enable (Bit30: 1) '
                              '\tActual: Power State Disable (Bit30: 0)'.format(slice_id))
                status = False
            else:
                logging.debug('DBUF_CTL_{} enable'.format(slice_id))

        ##
        # Verify MBus joined mode status
        current_mbus_joined = gen14_dbuf_distribution[enabled_pipes]['mbus_joined']

        mbus_ctl_value = importlib.import_module("registers.%s.MBUS_CTL_REGISTER" % self.platform)
        mbus_ctl = self.mmio_read.read('MBUS_CTL_REGISTER', 'MBUS_CTL', self.platform, gfx_index=gfx_index)

        mbus_joined_mode = mbus_ctl.__getattribute__("mbus_joining")
        mbus_hashing_mode = '2X2_HASHING' if mbus_ctl.__getattribute__("hashing_mode") == \
                                             getattr(mbus_ctl_value, 'hashing_mode_2X2_HASHING') else '1X4_HASHING'

        if current_mbus_joined:
            if mbus_joined_mode != getattr(mbus_ctl_value, 'mbus_joining_ENABLE'):
                logging.error('MBUS_CTL status mismatch. \tExpected: MBUS Joining Enable (Bit31: 1) '
                              '\tActual: MBUS Joining Disable (Bit31: 0)')
                status = False
            else:
                logging.debug('MBus running in Joined mode with Hashing as {}'.format(mbus_hashing_mode))
        else:
            if mbus_joined_mode != getattr(mbus_ctl_value, 'mbus_joining_DISABLE'):
                logging.error('MBUS_CTL status mismatch. \tExpected: MBUS Joining Disable (Bit31: 0) '
                              '\tActual: MBUS Joining Enable (Bit31: 1)')
                status = False
            else:
                logging.debug('MBus running in Dis-joined mode with Hashing as {}'.format(mbus_hashing_mode))

        ##
        # Verify the DBuf allocations for all the planes
        for pipe_idx in range(0, pipe_count):
            if pipe_list[pipe_idx].bIsPipeEnable is True:
                pipe_buf_start = current_dbuf_allocations[pipe_list[pipe_idx].iPipeId][0]
                pipe_buf_end = current_dbuf_allocations[pipe_list[pipe_idx].iPipeId][1]

                ##
                # Log the Pipe DBuf boundaries
                logging.info("DBuf boundaries for PIPE_{} are => Start:{} \tEnd:{}"
                             .format(wm_util.PIPE_NAME[pipe_idx], pipe_buf_start, pipe_buf_end))

                ##
                # Verify Cursor DBuf distribution. It should be within the Pipe Dbuf boundaries
                cursor_buf_reg = 'CUR_BUF_CFG_' + wm_util.PIPE_NAME[pipe_idx]
                cursor_buf = self.mmio_read.read('PLANE_BUF_CFG_REGISTER', cursor_buf_reg, self.platform, gfx_index=gfx_index)

                cursor_buf_start = cursor_buf.__getattribute__("buffer_start")
                cursor_buf_end = cursor_buf.__getattribute__("buffer_end")

                logging.debug("DBuf boundaries for CURSOR_PLANE_{} are --> \tStart:{} \tEnd:{}"
                              .format(wm_util.PIPE_NAME[pipe_idx], cursor_buf_start, cursor_buf_end))

                if (((cursor_buf_start != 0) or (cursor_buf_end != 0)) and
                        ((cursor_buf_start < pipe_buf_start) or (cursor_buf_end > pipe_buf_end))):
                    logging.error("CURSOR_PLANE_{} [DBuf:{}-{}] exceeds PIPE_{} [DBuf:{}-{}] DBuf allocation boundaries"
                                  .format(wm_util.PIPE_NAME[pipe_idx], cursor_buf_start, cursor_buf_end,
                                          wm_util.PIPE_NAME[pipe_idx], pipe_buf_start, pipe_buf_end))
                    status = False

                ##
                # Verify Plane DBuf distribution for all the Planes in that Pipe.
                # It should be within the Pipe Dbuf boundaries
                for plane_idx in range(0, plane_count):
                    plane_obj = plane_list[pipe_idx * plane_count + plane_idx]
                    if plane_obj.bStatus:
                        # Check Dbuf distribution for only currently active planes and not for all the planes.
                        plane_buf_reg = 'PLANE_BUF_CFG_' + wm_util.PLANE_NAME[plane_idx] + '_' + \
                                        wm_util.PIPE_NAME[pipe_idx]
                        plane_buf = self.mmio_read.read('PLANE_BUF_CFG_REGISTER', plane_buf_reg, self.platform, gfx_index=gfx_index)

                        plane_buf_start = plane_buf.__getattribute__("buffer_start")
                        plane_buf_end = plane_buf.__getattribute__("buffer_end")

                        logging.debug("DBuf boundaries for PLANE_{}_{} are --> \tStart:{} \tEnd:{}"
                                      .format(wm_util.PLANE_NAME[plane_idx],
                                              wm_util.PIPE_NAME[pipe_idx], plane_buf_start, plane_buf_end))

                        if (((plane_buf_start != 0) or (plane_buf_end != 0)) and
                                ((plane_buf_start < pipe_buf_start) or (plane_buf_end > pipe_buf_end))):
                            logging.error("PLANE_{}_{} [DBuf:{}-{}] exceeds Pipe_{} [DBuf:{}-{}] DBuf allocation "
                                          "boundaries" .format(wm_util.PLANE_NAME[plane_idx],
                                                               wm_util.PIPE_NAME[pipe_idx],
                                                               plane_buf_start, plane_buf_end,
                                                               wm_util.PIPE_NAME[pipe_idx],
                                                               pipe_buf_start, pipe_buf_end))
                            status = False
            return status

    ##
    # @brief        Check if minimum Dbuf is allocated for each active plane
    # @param[in]    plane_list of type PLANE()
    # @param[in]    plane_count
    # @param[in]    pipe_count
    # @param[in]    is_async_flip_check as optional
    # @return       True if min Dbuf is allocated; False, otherwise
    def check_min_dbuf_needed(self, plane_list, plane_count, pipe_count, is_async_flip_check=False):
        ##
        # BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/49255
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
                    if (plane_obj.uiPlaneTilingFormat == wm_util.SURFACE_MEMORY_X_TILED) or \
                            (plane_obj.uiPlaneTilingFormat == wm_util.SURFACE_MEMORY_LINEAR):

                        if 'PLANAR' in wm_util.GEN11_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']:
                            min_dbuf_needed = 2 * wm_util.MIN_DBUF_X_TILE  # Calculate separate for Y and UV plane
                        else:
                            min_dbuf_needed = wm_util.MIN_DBUF_X_TILE

                    ##
                    # Planes using Y tiled memory formats must allocate blocks for a minimum number of scan-lines worth
                    # of data.
                    #
                    # Y tiled minimum allocation = Ceil [(4 * Plane source width * Plane Bpp)/512] * MinScanLines/4 + 3
                    #
                    # For YUV 420 Planar formats (NV12, P0xx), buffer allocation is done for Y and UV surfaces
                    # separately. Treat Y and UV surface as 2 separate planes with UV plane will have double the bpp of
                    # Y plane

                    else:
                        min_scanlines_y_tile = 8
                        bpp = plane_obj.uiPlaneBpp
                        if ('PLANAR' in wm_util.GEN11_PIXEL_FORMAT_DICT[plane_obj.uiPixelFormat]['pixel_format']) and \
                                (plane_obj.uiPlanarYUV420Component == 0):
                            bpp = bpp * 2

                        min_dbuf_needed = math.ceil(float(4 * plane_obj.lPlaneHorizontal * bpp) / 512) * \
                            min_scanlines_y_tile / 4 + 3

                    ##
                    # Compare actual and expected min dbuf allocated
                    if plane_obj.uiBufferAllocated < min_dbuf_needed:
                        # By default, actual dbuf allocated should be atleast equal to or more than minimum dbuf
                        # required for that plane
                        logging.critical("FAIL: Minimum DBuf not allocated for PLANE_{}_{}:"
                                         "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                         .format(wm_util.PLANE_NAME[plane_idx],
                                                 wm_util.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated))
                        status = False

                    elif (is_async_flip_check is True) and (plane_obj.bAsyncFlip is True) and \
                            (plane_obj.uiBufferAllocated != min_dbuf_needed):
                        # For Gen13+ platforms, for async flips, the actual dbuf allocated should be exactly equal to
                        # the minimum dbuf required by that plane
                        # [HSD-14011035368][VPMG-6974]: Use minimum watermarks for async flip
                        logging.critical("FAIL: Minimum DBuf not allocated for PLANE_{}_{} with Async Flips:"
                                         "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                         .format(wm_util.PLANE_NAME[plane_idx],
                                                 wm_util.PIPE_NAME[pipe_idx],
                                                 min_dbuf_needed, plane_obj.uiBufferAllocated))
                        status = False

                    else:
                        logging.info("PASS: Minimum DBuf allocated for PLANE_{}_{}:"
                                     "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                                     .format(wm_util.PLANE_NAME[plane_idx], wm_util.PIPE_NAME[pipe_idx],
                                             min_dbuf_needed, plane_obj.uiBufferAllocated))

        return status

    ##
    # @brief        Compare expected and programmed SAGV WM
    # @param[in]    exp_sagv_wm
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    plane_list
    # @param[in]    is_cursor_wm as optional
    # @param[in]    gfx_index as optional
    # @return       True if successful else false
    def verify_sagv_watermark(self, exp_sagv_wm, pipe_count, plane_count, plane_list, is_cursor_wm=False, gfx_index='gfx_0'):

        plane_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)
        level = wm_util.SAGV_WM_LATENCY_LEVEL

        wm_status = True
        failure = ''
        prog_sagv_wm = []

        for pipe_idx in range(0, pipe_count):
            if is_cursor_wm is False:
                ##
                # Fetch the Programmed SAGV WM value for each plane
                for plane_idx in range(0, plane_count):
                    plane_wm = watermark_base.PlaneWatermarkObj()
                    plane_wm_offset = 'PLANE_WM_' + wm_util.PLANE_NAME[plane_idx] + '_' + \
                                      wm_util.PIPE_NAME[pipe_idx]
                    plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', plane_wm_offset, self.platform,
                                                       extra_offset=(level *
                                                                     wm_util.NEXT_REGISTER_OFFSET), gfx_index=gfx_index)
                    ##
                    # Fetch the Programmed SAGV WM value
                    plane_wm.bStatus = True if (plane_wm_reg.__getattribute__("enable") !=
                                                getattr(plane_wm_value, 'enable_DISABLE')) else False
                    plane_wm.fResultBlocks = plane_wm_reg.__getattribute__("blocks") if plane_wm.bStatus else 0
                    plane_wm.fResultLines = plane_wm_reg.__getattribute__("lines") if plane_wm.bStatus else 0

                    prog_sagv_wm.append(plane_wm)
            else:
                ##
                # Fetch the Programmed SAGV WM value for cursor plane
                plane_count = 1
                cur_plane_wm = watermark_base.PlaneWatermarkObj()

                cur_plane_wm_offset = 'CUR_WM_' + wm_util.PIPE_NAME[pipe_idx]
                cur_plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', cur_plane_wm_offset, self.platform,
                                                       extra_offset=(level *
                                                                     wm_util.NEXT_REGISTER_OFFSET), gfx_index=gfx_index)

                cur_plane_wm.bStatus = True if (cur_plane_wm_reg.__getattribute__("enable") !=
                                                getattr(plane_wm_value, 'enable_DISABLE')) else False

                cur_plane_wm.fResultBlocks = cur_plane_wm_reg.__getattribute__("blocks") if cur_plane_wm.bStatus else 0

                cur_plane_wm.fResultLines = cur_plane_wm_reg.__getattribute__("lines") if cur_plane_wm.bStatus else 0

                prog_sagv_wm.append(cur_plane_wm)

        for pipe_idx in range(0, pipe_count):
            for plane_idx in range(0, plane_count):
                ##
                # Verify the Programmed SAGV WM with Expected SAGV WM
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    status = True
                    # Compare only if the Plane is enabled

                    exp_sagv_wm_status = exp_sagv_wm[pipe_idx * plane_count + plane_idx].bStatus
                    exp_sagv_wm_result_blocks = exp_sagv_wm[pipe_idx * plane_count + plane_idx].fResultBlocks
                    exp_sagv_wm_result_lines = exp_sagv_wm[pipe_idx * plane_count + plane_idx].fResultLines

                    prog_sagv_wm_status = prog_sagv_wm[pipe_idx * plane_count + plane_idx].bStatus
                    prog_sagv_wm_result_blocks = prog_sagv_wm[pipe_idx * plane_count + plane_idx].fResultBlocks
                    prog_sagv_wm_result_lines = prog_sagv_wm[pipe_idx * plane_count + plane_idx].fResultLines

                    if exp_sagv_wm_status is not prog_sagv_wm_status:
                        # WM Status Mismatch
                        failure = '--> WM STATUS MISMATCH'
                        status = False
                    if (exp_sagv_wm_status is True) and (prog_sagv_wm_status is True):
                        if exp_sagv_wm_result_blocks != prog_sagv_wm_result_blocks:
                            # WM Results blocks Mismatch
                            failure = '--> BLOCKS/LINES MISMATCH'
                            status = False
                        if exp_sagv_wm_result_lines != prog_sagv_wm_result_lines:
                            # WM Results line Mismatch
                            failure = '--> BLOCKS/LINES MISMATCH'
                            status = False

                    logging.info('{}: {}_{}_SAGV\t[WM_Status, Blocks, Lines]\t'
                                 'Expected: [{}, {}, {}]\tActual: [{}, {}, {}]\t{}'
                                 .format('PASS' if status is True else 'FAIL',
                                         'PLANE_WM_' + str(
                                             wm_util.PLANE_NAME[plane_idx]) if is_cursor_wm is False
                                         else 'CUR_WM', wm_util.PIPE_NAME[pipe_idx],
                                         str(exp_sagv_wm_status).upper(), int(exp_sagv_wm_result_blocks),
                                         int(exp_sagv_wm_result_lines),
                                         str(prog_sagv_wm_status).upper(), int(prog_sagv_wm_result_blocks),
                                         int(prog_sagv_wm_result_lines), failure))
                    wm_status = wm_status & status

        return wm_status

    ##
    # @brief        Compare expected and programmed SAGV WM
    # @param[in]    exp_trans_sagv_wm
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    plane_list
    # @param[in]    is_cursor_wm as optional
    # @param[in]    gfx_index as optional
    # @return       bool
    def verify_trans_sagv_watermark(self, exp_trans_sagv_wm, pipe_count, plane_count, plane_list, is_cursor_wm=False, gfx_index='gfx_0'):

        plane_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)
        level = wm_util.TRANS_SAGV_WM_LATENCY_LEVEL

        wm_status = True
        failure = ''
        prog_trans_sagv_wm = []

        for pipe_idx in range(0, pipe_count):
            if is_cursor_wm is False:
                ##
                # Fetch the Programmed SAGV WM value for each plane
                for plane_idx in range(0, plane_count):
                    plane_wm = watermark_base.PlaneWatermarkObj()
                    plane_wm_offset = 'PLANE_WM_' + wm_util.PLANE_NAME[plane_idx] + '_' + \
                                      wm_util.PIPE_NAME[pipe_idx]
                    plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', plane_wm_offset, self.platform,
                                                       extra_offset=(level * wm_util.NEXT_REGISTER_OFFSET), gfx_index=gfx_index)
                    ##
                    # Fetch the Programmed SAGV WM value
                    plane_wm.bStatus = True if (plane_wm_reg.__getattribute__("enable") !=
                                                getattr(plane_wm_value, 'enable_DISABLE')) else False
                    plane_wm.fResultBlocks = plane_wm_reg.__getattribute__("blocks") if plane_wm.bStatus else 0

                    prog_trans_sagv_wm.append(plane_wm)
            else:
                ##
                # Fetch the Programmed SAGV WM value for cursor plane
                plane_count = 1
                cur_plane_wm = watermark_base.PlaneWatermarkObj()

                cur_plane_wm_offset = 'CUR_WM_' + wm_util.PIPE_NAME[pipe_idx]
                cur_plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', cur_plane_wm_offset, self.platform,
                                                       extra_offset=(level * wm_util.NEXT_REGISTER_OFFSET), gfx_index=gfx_index)

                cur_plane_wm.bStatus = True if (cur_plane_wm_reg.__getattribute__("enable") !=
                                                getattr(plane_wm_value, 'enable_DISABLE')) else False
                cur_plane_wm.fResultBlocks = cur_plane_wm_reg.__getattribute__("blocks") if cur_plane_wm.bStatus else 0

                prog_trans_sagv_wm.append(cur_plane_wm)

        for pipe_idx in range(0, pipe_count):
            for plane_idx in range(0, plane_count):
                ##
                # Verify the Programmed SAGV WM with Expected SAGV WM
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    status = True
                    # Compare only if the Plane is enabled

                    exp_trans_sagv_wm_status = exp_trans_sagv_wm[pipe_idx * plane_count + plane_idx].bStatus
                    exp_trans_sagv_wm_result_blocks = exp_trans_sagv_wm[pipe_idx * plane_count +
                                                                        plane_idx].fResultBlocks

                    prog_trans_sagv_wm_status = prog_trans_sagv_wm[pipe_idx * plane_count + plane_idx].bStatus
                    prog_trans_sagv_wm_result_blocks = prog_trans_sagv_wm[pipe_idx * plane_count +
                                                                          plane_idx].fResultBlocks

                    if exp_trans_sagv_wm_status is not prog_trans_sagv_wm_status:
                        # WM Status Mismatch
                        failure = '--> WM STATUS MISMATCH'
                        status = False
                    if (exp_trans_sagv_wm_status is True) and (prog_trans_sagv_wm_status is True):
                        if exp_trans_sagv_wm_result_blocks != prog_trans_sagv_wm_result_blocks:
                            # WM Results blocks Mismatch
                            failure = '--> BLOCKS MISMATCH'
                            status = False

                    logging.info('{}: {}_{}_TRANS_SAGV\t[WM_Status, Blocks]\t'
                                 'Expected: [{}, {}]\tActual: [{}, {}]\t{}'
                                 .format('PASS' if status is True else 'FAIL',
                                         'PLANE_WM_' + str(
                                             wm_util.PLANE_NAME[plane_idx]) if is_cursor_wm is False
                                         else 'CUR_WM', wm_util.PIPE_NAME[pipe_idx],
                                         str(exp_trans_sagv_wm_status).upper(), int(exp_trans_sagv_wm_result_blocks),
                                         str(prog_trans_sagv_wm_status).upper(), int(prog_trans_sagv_wm_result_blocks),
                                         failure))
                    wm_status = wm_status & status

        return wm_status
