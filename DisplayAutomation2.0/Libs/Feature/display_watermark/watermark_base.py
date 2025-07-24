######################################################################################
# @file         watermark_base.py
# @addtogroup   PyLibs_DisplayWatermark
# @brief        Base Class contains common methods that can be used across GEN specific modules
# @author       Kumar V,Arun, Bhargav Adigarla
######################################################################################
import importlib
import logging
import math
import time

from collections import defaultdict
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_watermark import watermark_utils
from Libs.Feature.display_watermark.watermark import GDHM_FEATURE_TAG
from Libs.Feature.powercons import registry
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.vdsc import dsc_verifier

from registers.mmioregister import MMIORegister


##
# @brief        This class contains helper functions for watermark and dbuf calculations
class DisplayWatermarkBase:

    ##
    # @brief        DisplayWatermarkBase default __init__ function
    # @param[in]    gfx_index as optional
    def __init__(self, gfx_index='gfx_0'):
        self.platform = None
        self.current_config = None
        self.system_utility = system_utility.SystemUtility()
        self.driver_interface_ = driver_interface.DriverInterface()
        self.machine_info = SystemInfo()
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            if str(gfx_display_hwinfo[i].gfxIndex).lower() == gfx_index:
                self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
                break

        # Taking common WM verification path for all Gen11 and Gen11p5 platforms
        if self.platform in ['icllp', 'iclhp', 'lkf1', 'jsl']:
            self.platform = 'icl'
        self.config = display_config.DisplayConfiguration()
        self.mmio_read = MMIORegister()

    ##
    # @brief        Get a bitmapped value from mmio register value
    # @param[in]    mmio_value - value read from mmio offset
    # @param[in]    bit_map - bitmapping of required bits to be read
    # @return       int type bpp value
    def read_from_mmio_value(self, mmio_value, bit_map):
        for x in range(32):
            if ((bit_map >> x) & 1) == 1:
                value = (mmio_value & bit_map) >> x
                return value
        return 0

    ##
    # @brief        Get bpp from pixel format
    # @param[in]    pixel_format value from mmio
    # @return       int type bpp value
    def get_bpp_from_pixel_format(self, pixel_format):
        if (self.platform in watermark_utils.GEN11_PLATFORMS or self.platform in watermark_utils.GEN12_PLATFORMS or
                self.platform in watermark_utils.GEN13_PLATFORMS or self.platform in watermark_utils.GEN14_PLATFORMS
                or self.platform in watermark_utils.GEN15_PLATFORMS or self.platform in watermark_utils.GEN16_PLATFORMS
                or self.platform in watermark_utils.GEN17_PLATFORMS):
            return watermark_utils.GEN11_PIXEL_FORMAT_DICT[pixel_format]['BPP']
        elif self.platform in watermark_utils.GEN10_PLATFORMS:
            return watermark_utils.GEN10_PIXEL_FORMAT_DICT[pixel_format]['BPP']
        elif self.platform in watermark_utils.GEN9_PLATFORMS:
            return watermark_utils.GEN9_PIXEL_FORMAT_DICT[pixel_format]['BPP']
        else:
            logging.error("ERROR: UNKNOWN PLATFORM in GET BPP CALL ")
            return 0

    ##
    # @brief        Read the raw latency values from GTDriver MailBox register
    # @param[in]    gfx_index as optional
    # @return       list containing raw latencies
    def read_latency_value_from_mailbox(self, gfx_index='gfx_0'):

        # As per Bspec with Error code =06h and Run/busy=1
        get_latency_command = 0x80000006

        # Write the Mailbox register value
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_DATA0, 0, gfx_index)
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_DATA1, 0, gfx_index)
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_INTERFACE, get_latency_command,
                                          gfx_index)

        # Poll on REG_GTDRIVER_MAILBOX_INTERFACE with 150us timeout for Busy bit to become 0 (similar to driver)
        # This is to ensure that the data values are read correctly
        for i in range(15):
            value = self.driver_interface_.mmio_read(watermark_utils.REG_GTDRIVER_MAILBOX_INTERFACE, gfx_index)
            if value & 0x80000000 == 0:
                break
            time.sleep(0.00001)  # 10us

        # Read the Set One Latency Value
        data0 = self.driver_interface_.mmio_read(watermark_utils.REG_GTDRIVER_MAILBOX_DATA0, gfx_index)
        logging.info("Latencies 1st set = %s" % hex(data0))

        # Write the Mailbox register value
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_DATA0, 1, gfx_index)
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_DATA1, 0, gfx_index)
        self.driver_interface_.mmio_write(watermark_utils.REG_GTDRIVER_MAILBOX_INTERFACE, get_latency_command,
                                          gfx_index)

        # Poll on REG_GTDRIVER_MAILBOX_INTERFACE with 150us timeout for Busy bit to become 0 (similar to driver)
        # This is to ensure that the data values are read correctly
        for i in range(15):
            value = self.driver_interface_.mmio_read(watermark_utils.REG_GTDRIVER_MAILBOX_INTERFACE, gfx_index)
            if value & 0x80000000 == 0:
                break
            time.sleep(0.00001)  # 10us

        # Read the Set Two Latency Value
        data1 = self.driver_interface_.mmio_read(watermark_utils.REG_GTDRIVER_MAILBOX_DATA0, gfx_index)
        logging.info("Latencies 2nd set = %s" % hex(data1))

        latency = []
        for i in range(8):
            latency.append(0)

        # Latency for Watermark 0-7
        latency[0] = (data0 & 0x000000FF)
        latency[1] = (data0 & 0x0000FF00) >> 8
        latency[2] = (data0 & 0x00FF0000) >> 16
        latency[3] = (data0 & 0xFF000000) >> 24

        latency[4] = (data1 & 0x000000FF)
        latency[5] = (data1 & 0x0000FF00) >> 8
        latency[6] = (data1 & 0x00FF0000) >> 16
        latency[7] = (data1 & 0xFF000000) >> 24

        # Latency values should be in strict order
        for index in range(1, 8):
            if latency[index] != 0 and latency[index] < latency[0]:
                latency[index] = latency[0]
            else:
                break

        return latency

    ##
    # @brief        Get memory latency values
    # @param[in]    gfx_index as optional
    # @return       list containing latencies
    def get_memory_latency(self, gfx_index='gfx_0'):

        latency = self.read_latency_value_from_mailbox(gfx_index)

        # If latency WM0 is zero then add fabric latency of 2 micros seconds
        fabric_latency = 2
        fabric_latency_ipc = 4

        if latency[0] == 0:
            for i in range(0, len(latency)):
                latency[i] = latency[i] + fabric_latency

        # WA : if ipc is enabled for kbl , then increase latency by 4 on all levels
        arb_ctl2 = self.driver_interface_.mmio_read(0x45004, gfx_index)
        ipc_status = self.read_from_mmio_value(arb_ctl2, 0x00000008)

        if (self.platform == 'kbl') and (ipc_status == 1):
            for i in range(0, len(latency)):
                latency[i] = latency[i] + fabric_latency_ipc

        if self.platform == 'icl':
            # ICL and above platforms
            if self.system_utility.is_ddrw(gfx_index) is True:
                # Yangra driver
                current_exec_env = self.system_utility.get_execution_environment_type()
                if current_exec_env is None:
                    raise Exception('Test failed to identify the current execution environment')
                if current_exec_env in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
                    # Temp latencies hardcoded in xml used in pre-si env (only for Yangra)
                    # For Post-Si, it will use the actual Mem latencies fetched from GTDRIVER MAILBOX
                    latency = [4, 4, 4, 4, 4, 4, 4, 4]
            else:
                # Mainline driver
                # temporary latencies hardcoded in driver for pre-si checkout since GTMAILBOX read from PCU will fail
                latency = [2, 4, 20, 37, 82, 102, 102, 257]
        logging.info("Memory Latencies in microseconds L0:{} L1:{} L2:{} L3:{} L4:{} L5:{} L6:{} L7:{}"
                     .format(latency[0], latency[1], latency[2], latency[3], latency[4], latency[5], latency[6],
                             latency[7]))
        return latency

    ##
    # @brief        Get and Cache Plane Parameters to USe for expected watermark calculation
    # @param[in]    pipe_count, plane_count (parameters help re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional
    # @return       list of all planes, each of type PLANEOBJ
    def get_plane_params(self, pipe_count, plane_count, gfx_index='gfx_0'):
        planes = []

        plane_ctl_value = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform)

        for pipe_idx in watermark_utils.PIPE_NAME[:pipe_count]:
            for plane_idx in watermark_utils.PLANE_NAME[:plane_count]:
                plane = PlaneObj()

                plane_ctl_reg = 'PLANE_CTL_' + plane_idx + '_' + pipe_idx
                plane_ctl = self.mmio_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, gfx_index=gfx_index)

                plane_size_reg = 'PLANE_SIZE_' + plane_idx + '_' + pipe_idx
                plane_size = self.mmio_read.read('PLANE_SIZE_REGISTER', plane_size_reg, self.platform,
                                                 gfx_index=gfx_index)

                plane_buf_reg = 'PLANE_BUF_CFG_' + plane_idx + '_' + pipe_idx
                plane_buf = self.mmio_read.read('PLANE_BUF_CFG_REGISTER', plane_buf_reg, self.platform,
                                                gfx_index=gfx_index)

                plane.bStatus = True if (plane_ctl.__getattribute__("plane_enable") !=
                                         getattr(plane_ctl_value, 'plane_enable_DISABLE')) else False

                plane.lPlaneHorizontal = plane_size.__getattribute__("width") + 1

                plane.lPlaneVertical = plane_size.__getattribute__("height") + 1

                plane.uiPlaneRotation = plane_ctl.__getattribute__("plane_rotation")
                if self.platform in watermark_utils.PRE_GEN_14_PLATFORMS:
                    plane.bRCStatus = True if (plane_ctl.__getattribute__("render_decomp") !=
                                               getattr(plane_ctl_value, 'render_decomp_DISABLE')) else False

                plane.uiPlaneTilingFormat = plane_ctl.__getattribute__("tiled_surface")

                plane.uiPixelFormat = plane_ctl.__getattribute__("source_pixel_format")

                plane.uiBufferAllocated = 0 if (not plane.bStatus) else \
                    plane_buf.__getattribute__("buffer_end") - plane_buf.__getattribute__("buffer_start") + 1

                plane.uiPlaneBpp = self.get_bpp_from_pixel_format(plane.uiPixelFormat)
                plane.fPlaneDownscalingFactor = self.get_plane_downscale_factor(
                    watermark_utils.PLANE_NAME.index(plane_idx),
                    watermark_utils.PIPE_NAME.index(pipe_idx), plane, gfx_index=gfx_index)
                ##
                # planar_yuv420_component register definition field is only applicable for Yangra platforms (Gen 11+)
                if self.platform not in watermark_utils.GEN9_PLATFORMS and \
                        self.platform not in watermark_utils.GEN10_PLATFORMS:
                    plane.uiPlanarYUV420Component = 0 if (plane_ctl.__getattribute__("planar_yuv420_component") ==
                                                          getattr(plane_ctl_value, 'planar_yuv420_component_UV')) else 1

                plane.bAsyncFlip = True if (plane_ctl.__getattribute__("async_address_update_enable")
                                            == getattr(plane_ctl_value, 'async_address_update_enable_ASYNC')) else False

                planes.append(plane)
        return planes

    ##
    # @brief        Get and Cache Cursor Plane Parameters to Use for expected watermark calculation
    # @param[in]    pipe_count (parameters help re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional
    # @return       list of all cursor planes, each of type PLANEOBJ
    def get_cursor_plane_params(self, pipe_count, gfx_index='gfx_0'):
        cur_planes = []

        for pipe_idx in watermark_utils.PIPE_NAME[:pipe_count]:
            cur_plane = PlaneObj()

            cur_ctl_reg = 'CUR_CTL_' + pipe_idx
            cur_plane_ctl = self.mmio_read.read('CUR_CTL_REGISTER', cur_ctl_reg, self.platform, gfx_index=gfx_index)

            cur_buf_cfg_reg = 'CUR_BUF_CFG_' + pipe_idx
            cur_plane_buf = self.mmio_read.read('PLANE_BUF_CFG_REGISTER', cur_buf_cfg_reg, self.platform,
                                                gfx_index=gfx_index)

            cursor_mode = cur_plane_ctl.__getattribute__("cursor_mode_select")

            cur_plane.bStatus = True if (cursor_mode != 0) else False
            cur_plane.lPlaneHorizontal = watermark_utils.CURSOR_DETAILS_DICT[cursor_mode]['size']
            cur_plane.lPlaneVertical = cur_plane.lPlaneHorizontal  # cursor is always a square plane

            cur_plane.uiBufferAllocated = 0 if (not cur_plane.bStatus) else \
                cur_plane_buf.__getattribute__("buffer_end") - cur_plane_buf.__getattribute__("buffer_start") + 1

            cur_plane.uiPlaneBpp = watermark_utils.CURSOR_DETAILS_DICT[cursor_mode]['BPP']
            cur_plane.uiPlaneTilingFormat = watermark_utils.SURFACE_MEMORY_X_TILED  # cursor plane is x-tiled

            cur_planes.append(cur_plane)

        return cur_planes

    ##
    # @brief        Get Plane downscaling factor
    # @param[in]    plane_idx, pipe_idx to check corresponding scalars
    # @param[in]    plane_obj of type PLANEOBJ()
    # @param[in]    gfx_index as optional
    # @return       Plane downscaling factor as a float
    def get_plane_downscale_factor(self, plane_idx, pipe_idx, plane_obj, gfx_index='gfx_0'):
        down_scale_factor = 1.0

        ps_ctl_value = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % self.platform)

        ps_size_offset = 'PS_WIN_SZ_' + watermark_utils.PLANE_NAME[0] + '_' + watermark_utils.PIPE_NAME[pipe_idx]

        ps_ctl_offset = 'PS_CTRL_' + watermark_utils.PLANE_NAME[0] + '_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps1_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps_ctl_offset, self.platform, gfx_index=gfx_index)

        ps2_ctl_offset = 'PS_CTRL_' + watermark_utils.PLANE_NAME[1] + '_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps2_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps2_ctl_offset, self.platform, gfx_index=gfx_index)

        if (ps1_ctl.__getattribute__("enable_scaler") == getattr(ps_ctl_value, 'enable_scaler_DISABLE')) and \
                (ps2_ctl.__getattribute__("enable_scaler") == getattr(ps_ctl_value, 'enable_scaler_DISABLE')):
            return down_scale_factor

        if (ps1_ctl.__getattribute__("enable_scaler") == getattr(ps_ctl_value, 'enable_scaler_ENABLE')) and \
                (ps1_ctl.__getattribute__("scaler_binding") == (plane_idx + 1)):
            logging.debug("Scalar 1 is attached to Pipe: %s plane: %s", watermark_utils.PIPE_NAME[pipe_idx],
                          watermark_utils.PLANE_NAME[plane_idx])
            ps_size = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_size_offset, self.platform, gfx_index=gfx_index)

        elif (ps2_ctl.__getattribute__("enable_scaler") == getattr(ps_ctl_value, 'enable_scaler_ENABLE')) and \
                (ps2_ctl.__getattribute__("scaler_binding") == (plane_idx + 1)):
            logging.debug("Scalar 2 is attached to Pipe: %s plane: %s", watermark_utils.PIPE_NAME[pipe_idx],
                          watermark_utils.PLANE_NAME[plane_idx])
            ps_size_offset = 'PS_WIN_SZ_' + watermark_utils.PLANE_NAME[1] + '_' + watermark_utils.PIPE_NAME[pipe_idx]
            ps_size = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_size_offset, self.platform, gfx_index=gfx_index)
        else:
            logging.debug("No Scalar attached to Pipe: %s plane: %s", watermark_utils.PIPE_NAME[pipe_idx],
                          watermark_utils.PLANE_NAME[plane_idx])
            return down_scale_factor

        scalar_height = ps_size.__getattribute__("ysize")

        scalar_width = ps_size.__getattribute__("xsize")

        hor_downscale_factor = round(float(plane_obj.lPlaneHorizontal) / scalar_width, 1)
        ver_downscale_factor = round(float(plane_obj.lPlaneVertical) / scalar_height, 1)

        logging.debug("Downscale factor hor:%d ver:%d" % (hor_downscale_factor, ver_downscale_factor))

        if ver_downscale_factor < 1:
            ver_downscale_factor = 1

        if hor_downscale_factor < 1:
            hor_downscale_factor = 1

        down_scale_factor = hor_downscale_factor * ver_downscale_factor
        return round(down_scale_factor, 2)

    ##
    # @brief        Get and Cache Pipe Parameters to Use for expected watermark calculation
    # @param[in]    pipe_count (parameter helps re-usability for future platforms if needed)
    # @param[in]    is_48hz_verification True if low rr enabled else false as optional
    # @param[in]    gfx_index as optional param
    # @return       list of all pipes and their parameters
    def get_pipe_params(self, pipe_count, is_48hz_verification=False, gfx_index='gfx_0'):
        pipes = []
        gfx_index_list = []
        gfx_display_dict = defaultdict(list)

        self.current_config, display_list, display_and_adapter_info_list = self.config.get_current_display_configuration_ex()
        for each_display_and_adapter_info in display_and_adapter_info_list:
            gfx_index_list.append(each_display_and_adapter_info.adapterInfo.gfxIndex)

        for k, v in zip(display_list, gfx_index_list):
            gfx_display_dict[k].append(v)

        for pipe_idx in range(0, pipe_count):
            pipe = PipeObj()
            is_pipe_joiner_required, no_of_pipe_required = False, 1
            for display, index_list in gfx_display_dict.items():
                for index in index_list:
                    if index == gfx_index:
                        adapter_info = self.config.get_display_and_adapter_info_ex(display, gfx_index)
                        if type(adapter_info) is list:
                            adapter_info = adapter_info[0]

                        mode = self.config.get_current_mode(adapter_info)
                        timing = self.config.get_display_timings(adapter_info)

                        display_obj = display_base.DisplayBase(display, gfx_index=gfx_index)
                        if (display_obj.pipe == "PIPE_A" and pipe_idx == 0) or \
                                (display_obj.pipe == "PIPE_B" and pipe_idx == 1) or \
                                (display_obj.pipe == "PIPE_C" and pipe_idx == 2) or \
                                (display_obj.pipe == "PIPE_D" and pipe_idx == 3):
                            pipe.lHorizontalTotal = timing.hTotal
                            pipe.fPixelRate = round((float(timing.vSyncNumerator) / 1000000), 2)  # convert to MHz
                            pipe.fPipeDownscalingFactor = self.get_pipe_downscale_factor(pipe_idx, gfx_index)
                            pipe.bIsInterlaced = True if (
                                    mode.scanlineOrdering == watermark_utils.INTERLACED) else False
                            ##
                            # Overwrite the pixel clock if it is 48hz scenario
                            if is_48hz_verification is True and 'DP_' in display:
                                from Libs.Feature.display_engine.de_base.display_transcoder import \
                                    GetPixelClockFromDataAndLinkMN
                                pipe.fPixelRate = round(GetPixelClockFromDataAndLinkMN(display, gfx_index) / 1000000, 2)

                            is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(
                                gfx_index, display)

                            if pipe.fPixelRate > 0:
                                pipe.bIsPipeEnable = True
                                pipe.iPipeId = pipe_idx
            pipes.append(pipe)
            if is_pipe_joiner_required is True:
                for _ in range(1, no_of_pipe_required):
                    adj_pipe = PipeObj()
                    adj_pipe.lHorizontalTotal = pipe.lHorizontalTotal
                    adj_pipe.fPixelRate = pipe.fPixelRate
                    adj_pipe.fPipeDownscalingFactor = pipe.fPipeDownscalingFactor
                    adj_pipe.bIsInterlaced = pipe.bIsInterlaced
                    adj_pipe.bIsPipeEnable = True
                    adj_pipe.iPipeId = pipe_idx + 1
                    pipes.append(adj_pipe)

        logging.info("Current Display Configuration is {} with displays {}".format(self.current_config, display_list))
        return pipes

    ##
    # @brief        Get Pipe downscaling factor
    # @param[in]    pipe_idx to check corresponding scalars
    # @param[in]    gfx_index as optional param
    # @return       Pipe downscaling factor as a float
    def get_pipe_downscale_factor(self, pipe_idx, gfx_index='gfx_0'):
        downscale = 1.0

        ps_ctl_value = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % self.platform)

        ps_ctl_offset = 'PS_CTRL_1_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps1_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps_ctl_offset, self.platform, gfx_index=gfx_index)
        ps2_ctl_offset = 'PS_CTRL_2_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps2_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps2_ctl_offset, self.platform, gfx_index=gfx_index)

        pipe_srcsz_offset = 'PIPE_SRCSZ_' + watermark_utils.PIPE_NAME[pipe_idx]
        pipe_srcsz = self.mmio_read.read('PIPE_SRCSZ_REGISTER', pipe_srcsz_offset, self.platform, gfx_index=gfx_index)
        ps_win_sz1_offset = 'PS_WIN_SZ_1_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps_win_sz1 = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_win_sz1_offset, self.platform, gfx_index=gfx_index)
        ps_win_sz2_offset = 'PS_WIN_SZ_2_' + watermark_utils.PIPE_NAME[pipe_idx]
        ps_win_sz2 = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_win_sz2_offset, self.platform, gfx_index=gfx_index)

        if (ps1_ctl.__getattribute__('enable_scaler') != getattr(ps_ctl_value, 'enable_scaler_DISABLE')) & \
                (ps1_ctl.__getattribute__('scaler_binding') == getattr(ps_ctl_value, 'scaler_binding_PIPE_SCALER')):
            downscale = downscale * max((pipe_srcsz.__getattribute__('horizontal_source_size') /
                                         ps_win_sz1.__getattribute__('xsize')), 1)
            downscale = downscale * max((pipe_srcsz.__getattribute__('vertical_source_size') /
                                         ps_win_sz1.__getattribute__('ysize')), 1)

        if (ps2_ctl.__getattribute__('enable_scaler') != getattr(ps_ctl_value, 'enable_scaler_DISABLE')) & \
                (ps2_ctl.__getattribute__('scaler_binding') == getattr(ps_ctl_value, 'scaler_binding_PIPE_SCALER')):
            downscale = downscale * max((pipe_srcsz.__getattribute__('horizontal_source_size') /
                                         ps_win_sz2.__getattribute__('xsize')), 1)
            downscale = downscale * max((pipe_srcsz.__getattribute__('vertical_source_size') /
                                         ps_win_sz2.__getattribute__('ysize')), 1)
        return round(downscale, 2)

    ##
    # @brief        Get Programmed watermarks from HW
    # @param[in]    pipe_count, plane_count (parameters help re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional param
    # @return       list of all plane watermark blocks and lines
    def get_programmed_lp_watermarks(self, pipe_count, plane_count, gfx_index='gfx_0'):
        watermarks = []

        plane_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)

        for pipe_idx in range(0, pipe_count):
            for plane_idx in range(0, plane_count):
                for wm_level in range(0, watermark_utils.LATENCY_LEVELS):
                    plane_wm = PlaneWatermarkObj()

                    plane_wm_offset = 'PLANE_WM_' + watermark_utils.PLANE_NAME[plane_idx] + '_' + \
                                      watermark_utils.PIPE_NAME[pipe_idx]
                    plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', plane_wm_offset, self.platform,
                                                       extra_offset=(wm_level * watermark_utils.NEXT_REGISTER_OFFSET),
                                                       gfx_index=gfx_index)

                    plane_wm.bStatus = True if (plane_wm_reg.__getattribute__("enable") !=
                                                getattr(plane_wm_value, 'enable_DISABLE')) else False
                    plane_wm.fResultBlocks = plane_wm_reg.__getattribute__("blocks") if plane_wm.bStatus else 0
                    plane_wm.fResultLines = plane_wm_reg.__getattribute__("lines") if plane_wm.bStatus else 0

                    watermarks.append(plane_wm)
        return watermarks

    ##
    # @brief        Get Programmed watermarks from HW
    # @param[in]    pipe_count
    # @param[in]    gfx_index as optional param
    # @return       list of all plane watermark blocks and lines
    def get_programmed_cursor_lp_watermarks(self, pipe_count, gfx_index='gfx_0'):
        cur_watermarks = []

        cur_plane_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)

        for pipe_idx in range(0, pipe_count):
            for wm_level in range(0, watermark_utils.LATENCY_LEVELS):
                cur_plane_wm = PlaneWatermarkObj()

                cur_plane_wm_offset = 'CUR_WM_' + watermark_utils.PIPE_NAME[pipe_idx]
                cur_plane_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', cur_plane_wm_offset, self.platform,
                                                       extra_offset=(wm_level * watermark_utils.NEXT_REGISTER_OFFSET),
                                                       gfx_index=gfx_index)

                cur_plane_wm.bStatus = True if (cur_plane_wm_reg.__getattribute__("enable") !=
                                                getattr(cur_plane_wm_value, 'enable_DISABLE')) else False

                cur_plane_wm.fResultBlocks = cur_plane_wm_reg.__getattribute__("blocks") if cur_plane_wm.bStatus else 0

                cur_plane_wm.fResultLines = cur_plane_wm_reg.__getattribute__("lines") if cur_plane_wm.bStatus else 0

                cur_watermarks.append(cur_plane_wm)
        return cur_watermarks

    ##
    # @brief        Get Programmed Plane Transitional Watermarks from hardware
    # @param[in]    pipe_count, plane_count (parameter helps re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional param
    # @return       trans_watermark list with collection of objects of type PLANETRANSWATERMARKOBJ
    def get_programmed_trans_watermarks(self, pipe_count, plane_count, gfx_index='gfx_0'):
        trans_watermarks = []

        plane_trans_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)

        for pipe_idx in range(0, pipe_count):
            for plane_idx in range(0, plane_count):
                trans_wm = PlaneTransWatermarkObj()

                plane_trans_wm_reg = 'PLANE_TRANS_WM_' + watermark_utils.PLANE_NAME[plane_idx] + '_' + \
                                     watermark_utils.PIPE_NAME[pipe_idx]
                trans_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', plane_trans_wm_reg, self.platform,
                                                   gfx_index=gfx_index)

                trans_wm.bStatus = True if (trans_wm_reg.__getattribute__("enable") !=
                                            getattr(plane_trans_wm_value, 'enable_DISABLE')) else False
                trans_wm.fResultBlocks = trans_wm_reg.__getattribute__("blocks") if trans_wm.bStatus else 0

                trans_watermarks.append(trans_wm)
        return trans_watermarks

    ##
    # @brief        Get Programmed Cursor Transitional Watermarks from hardware
    # @param[in]    pipe_count (parameter helps re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional param
    # @return       trans_watermark list with collection of objects of type PLANETRANSWATERMARKOBJ
    def get_programmed_cursor_trans_watermarks(self, pipe_count, gfx_index='gfx_0'):
        cur_trans_watermarks = []

        cur_trans_wm_value = importlib.import_module("registers.%s.PLANE_WM_REGISTER" % self.platform)

        for pipe_idx in range(0, pipe_count):
            cur_trans_wm = PlaneTransWatermarkObj()

            cur_trans_wm_offset = 'CUR_WM_TRANS_' + watermark_utils.PIPE_NAME[pipe_idx]
            cur_trans_wm_reg = self.mmio_read.read('PLANE_WM_REGISTER', cur_trans_wm_offset, self.platform,
                                                   gfx_index=gfx_index)

            cur_trans_wm.bStatus = True if (cur_trans_wm_reg.__getattribute__("enable") !=
                                            getattr(cur_trans_wm_value, 'enable_DISABLE')) else False
            cur_trans_wm.fResultBlocks = cur_trans_wm_reg.__getattribute__("blocks") if cur_trans_wm.bStatus else 0

            cur_trans_watermarks.append(cur_trans_wm)
        return cur_trans_watermarks

    ##
    # @brief        Get Programmed Linetime from hardware
    # @param[in]    pipe_count (parameter helps re-usability for future platforms if needed)
    # @param[in]    gfx_index as optional param
    # @return       line_time list with collection of objects of type PIPELINETIMEOBJ
    def get_programmed_line_time(self, pipe_count, gfx_index='gfx_0'):
        mmio_read = MMIORegister()
        line_time = []

        for pipe_idx in range(0, pipe_count):
            line_time_obj = PipeLinetimeObj()

            line_time_offset = 'WM_LINETIME_' + watermark_utils.PIPE_NAME[pipe_idx]
            line_time_reg = mmio_read.read('WM_LINETIME_REGISTER', line_time_offset, self.platform, gfx_index=gfx_index)

            line_time_obj.fLineTime = line_time_reg.__getattribute__('line_time')
            line_time.append(line_time_obj)
        return line_time

    ##
    # @brief        Check if any plane is ytiled
    # @param[in]    plane_list of type PLANE()
    # @param[in]    pipe_count, plane_count (parameters help re-usability for future platforms if needed)
    # @return       BOOL
    def check_for_tile_y(self, plane_list, pipe_count, plane_count):
        for pipe_idx in range(pipe_count):
            for plane_idx in range(plane_count):
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus and \
                        (plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat ==
                         watermark_utils.SURFACE_MEMORY_Y_LEGACY_TILED):
                    return True
        return False

    ##
    # @brief        Print Plane Params
    # @param[in]    plane_list
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @return       none
    def print_plane_params(self, plane_list, pipe_count, plane_count):
        for pipe_idx in range(pipe_count):
            for plane_idx in range(plane_count):
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    hor = plane_list[pipe_idx * plane_count + plane_idx].lPlaneHorizontal
                    ver = plane_list[pipe_idx * plane_count + plane_idx].lPlaneVertical
                    tiling = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneTilingFormat
                    tiling_text = watermark_utils.MEMORY_TILING_LIST.get(plane_list[pipe_idx * plane_count +
                                                                                    plane_idx].uiPlaneTilingFormat)
                    rc = 'Yes' if plane_list[pipe_idx * plane_count + plane_idx].bRCStatus else 'No'
                    down_scale = plane_list[pipe_idx * plane_count + plane_idx].fPlaneDownscalingFactor
                    buf = plane_list[pipe_idx * plane_count + plane_idx].uiBufferAllocated
                    bpp = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneBpp
                    rotation = plane_list[pipe_idx * plane_count + plane_idx].uiPlaneRotation
                    rotation_text = watermark_utils.ROTATION_LIST.get(plane_list[pipe_idx * plane_count +
                                                                                 plane_idx].uiPlaneRotation)
                    pixel_format = plane_list[pipe_idx * plane_count + plane_idx].uiPixelFormat
                    pixel_format_text = self.get_pixel_format_text(plane_list[pipe_idx * plane_count +
                                                                              plane_idx].uiPixelFormat)
                    flip_type = 'Async' if plane_list[pipe_idx * plane_count + plane_idx].bAsyncFlip else 'Sync'

                    logging.info("INFO: Plane{}{} Enabled (X x Y)={}x{} Tiling={}({}) RC={}"
                                 " D.Scale={} DBuf={} BPP={} Angle={}({}) PixelFormat={}({}) FlipType={}"
                                 .format(watermark_utils.PLANE_NAME[plane_idx], watermark_utils.PIPE_NAME[pipe_idx],
                                         hor, ver, tiling, tiling_text, rc, down_scale, buf, bpp, rotation,
                                         rotation_text, pixel_format, pixel_format_text, flip_type)
                                 )

    ##
    # @brief        Get Pixel Format in Text Form for logging
    # @param[in]    pixel_format_value from mmio
    # @return       string type pixel format
    def get_pixel_format_text(self, pixel_format_value):

        if self.platform in watermark_utils.GEN11_PLATFORMS or self.platform in watermark_utils.GEN12_PLATFORMS or \
                self.platform in watermark_utils.GEN13_PLATFORMS or self.platform in watermark_utils.GEN14_PLATFORMS or \
                self.platform in watermark_utils.GEN15_PLATFORMS or self.platform in watermark_utils.GEN16_PLATFORMS or \
                self.platform in watermark_utils.GEN17_PLATFORMS:
            return watermark_utils.GEN11_PIXEL_FORMAT_DICT[pixel_format_value]['pixel_format']
        elif self.platform in watermark_utils.GEN10_PLATFORMS:
            return watermark_utils.GEN10_PIXEL_FORMAT_DICT[pixel_format_value]['pixel_format']
        elif self.platform in watermark_utils.GEN9_PLATFORMS:
            return watermark_utils.GEN9_PIXEL_FORMAT_DICT[pixel_format_value]['pixel_format']
        else:
            logging.error("ERROR: UNKNOWN PLATFORM IN GET PIXEL FORMAT")
            return "UNKNOWN"

    ##
    # @brief        Print Pipe Params
    # @param[in]    pipe_list, pipe_count objects
    # @return       none
    def print_pipe_params(self, pipe_list, pipe_count):
        for pipe_idx in range(pipe_count):
            if pipe_list[pipe_idx].fPixelRate > 0:
                pipe = watermark_utils.PIPE_NAME[pipe_idx]
                clk = pipe_list[pipe_idx].fPixelRate
                htotal = pipe_list[pipe_idx].lHorizontalTotal
                pipe_down_scale = pipe_list[pipe_idx].fPipeDownscalingFactor
                is_interlaced = pipe_list[pipe_idx].bIsInterlaced
                logging.info("INFO: Pipe{} Enabled PixelClock={}Mhz HTotal={} DownscaleFac={} IsInterlaced={}"
                             .format(pipe, clk, htotal, pipe_down_scale, is_interlaced))

    ##
    # @brief        Print Watermark Values from input watermark list
    # @param[in]    watermarks, pipe_count, plane_count: struct containing watermarks for all plane objects
    # @return       none
    def print_watermarks(self, watermarks, pipe_count, plane_count):
        logging.info("PRINT WATERMARKS")
        for pipe_idx in range(pipe_count):
            for plane_idx in range(plane_count):
                for level in range(watermark_utils.LATENCY_LEVELS):
                    logging.info("INFO: WM_{}_{}_{} status={}"
                                 .format(watermark_utils.PLANE_NAME[plane_idx], watermark_utils.PIPE_NAME[pipe_idx],
                                         level,
                                         watermarks[
                                             pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                                             plane_idx * watermark_utils.LATENCY_LEVELS + level].bStatus))
                    logging.info("INFO: WM_{}_{}_{} Result Blocks={}"
                                 .format(watermark_utils.PLANE_NAME[plane_idx], watermark_utils.PIPE_NAME[pipe_idx],
                                         level,
                                         watermarks[
                                             pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                                             plane_idx * watermark_utils.LATENCY_LEVELS + level].fResultBlocks))
                    logging.info("INFO: WM_{}_{}_{} Result Lines={}"
                                 .format(watermark_utils.PLANE_NAME[plane_idx], watermark_utils.PIPE_NAME[pipe_idx],
                                         level,
                                         watermarks[
                                             pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                                             plane_idx * watermark_utils.LATENCY_LEVELS + level].fResultLines))

    ##
    # @brief        compare main and lp watermarks WM0-WM7
    # @param[in]    exp_wm, prog_wm: expected watermark exp_wm, programmed watermarks prog_wm
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    plane_list: struct containing plane objects of type PLANEOBJ()
    # @param[in]    gfx_index as optional param
    # @return       bool
    def verify_lp_watermarks(self, exp_wm, prog_wm, pipe_count, plane_count, plane_list, gfx_index='gfx_0'):
        is_cursor_wm = False
        is_plane_enabled = False
        wm_status = True
        failure = ''
        if plane_count == 1:
            is_cursor_wm = True

        skip_lpwm_check = False
        test_ctrl_flag = registry.FeatureTestControl(gfx_index)
        logging.debug("FeatureTestControl Registry: Actual ={}".format(hex(test_ctrl_flag.value)))
        if test_ctrl_flag.cxsr_disable == 1:
            logging.warning("FeatureTestControl Registry: Expected = CxSR Enable(Bit0: 0) "
                            "Actual = CxSR disable (Bit0: 1): Skipping LP Watermark verification")
            skip_lpwm_check = True

        for pipe_idx in range(pipe_count):
            for plane_idx in range(plane_count):

                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    is_plane_enabled = True
                    status = True
                    failure = ''
                    for level in range(watermark_utils.LATENCY_LEVELS):
                        if level != 0 and skip_lpwm_check:
                            exp_wm_status = False
                        else:
                            exp_wm_status = exp_wm[
                                pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                                plane_idx * watermark_utils.LATENCY_LEVELS + level].bStatus
                        prog_wm_status = prog_wm[
                            pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                            plane_idx * watermark_utils.LATENCY_LEVELS + level].bStatus
                        exp_wm_result_blocks = exp_wm[
                            pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                            plane_idx * watermark_utils.LATENCY_LEVELS + level].fResultBlocks
                        prog_wm_result_blocks = prog_wm[
                            pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                            plane_idx * watermark_utils.LATENCY_LEVELS +
                            level].fResultBlocks
                        exp_wm_result_lines = exp_wm[
                            pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                            plane_idx * watermark_utils.LATENCY_LEVELS + level].fResultLines
                        prog_wm_result_lines = prog_wm[
                            pipe_idx * plane_count * watermark_utils.LATENCY_LEVELS +
                            plane_idx * watermark_utils.LATENCY_LEVELS + level].fResultLines

                        if exp_wm_status is not prog_wm_status:
                            # WM Status Mismatch
                            failure = '--> WM STATUS MISMATCH'
                            status = False
                        if (exp_wm_status is True) and (prog_wm_status is True):
                            if exp_wm_result_blocks != prog_wm_result_blocks:
                                # WM Results blocks Mismatch
                                failure = '--> BLOCKS/LINES MISMATCH'
                                status = False
                            if exp_wm_result_lines != prog_wm_result_lines:
                                # WM Results line Mismatch
                                failure = '--> BLOCKS/LINES MISMATCH'
                                status = False

                        logging.info('{}: {}_{}_{}\t[WM_Status, Blocks, Lines]\t'
                                     'Expected: [{}, {}, {}]\tActual: [{}, {}, {}]\t{}'
                                     .format('PASS' if status is True else 'FAIL',
                                             'PLANE_WM_' + str(
                                                 watermark_utils.PLANE_NAME[plane_idx]) if is_cursor_wm is False
                                             else 'CUR_WM', watermark_utils.PIPE_NAME[pipe_idx], level,
                                             str(exp_wm_status).upper(), int(exp_wm_result_blocks),
                                             int(exp_wm_result_lines),
                                             str(prog_wm_status).upper(), int(prog_wm_result_blocks),
                                             int(prog_wm_result_lines), failure))
                        wm_status = wm_status & status
        if wm_status is False:
            gdhm.report_test_bug_os(f"{GDHM_FEATURE_TAG} PLANE_LP_WM Verification Failed - Blocks/Lines Mismatch ")
        if is_plane_enabled is False and is_cursor_wm is False:
            logging.warning("No planes enabled during Watermark verification !!")
            return True
        return wm_status

    ##
    # @brief        Verify Transition Watermark values
    # @param[in]    exp_trans_wm
    # @param[in]    prog_trans_wm
    # @param[in]    pipe_count
    # @param[in]    plane_count
    # @param[in]    plane_list struct
    # @return       bool
    def verify_trans_wm(self, exp_trans_wm, prog_trans_wm, pipe_count, plane_count, plane_list):
        is_cursor_wm = False
        is_plane_enabled = False
        wm_status = True
        failure = ''
        if plane_count == 1:
            is_cursor_wm = True

        for pipe_idx in range(pipe_count):

            for plane_idx in range(plane_count):
                if plane_list[pipe_idx * plane_count + plane_idx].bStatus:
                    is_plane_enabled = True
                    status = True
                    failure = ''
                    exp_trans_status = exp_trans_wm[pipe_idx * plane_count + plane_idx].bStatus
                    prog_trans_status = prog_trans_wm[pipe_idx * plane_count + plane_idx].bStatus
                    exp_trans_result_blocks = exp_trans_wm[pipe_idx * plane_count +
                                                           plane_idx].fResultBlocks
                    prog_trans_result_blocks = prog_trans_wm[pipe_idx * plane_count +
                                                             plane_idx].fResultBlocks
                    if exp_trans_status is not prog_trans_status:
                        # Trans WM Status Mismatch
                        failure = '--> WM STATUS MISMATCH'
                        status = False
                    if (exp_trans_status is True) and (prog_trans_status is True):
                        if exp_trans_result_blocks != prog_trans_result_blocks:
                            # Trans WM Results blocks Mismatch
                            failure = '--> BLOCKS MISMATCH'
                            status = False

                    logging.info('{}: {}_{}\t[WM_Status, Blocks]\t\tExpected: [{}, {}]\t\tActual: [{}, {}]\t{}'
                                 .format('PASS' if status is True else 'FAIL',
                                         'PLANE_TRANS_WM_' + str(
                                             watermark_utils.PLANE_NAME[plane_idx]) if is_cursor_wm is False else
                                         'CUR_WM_TRANS', watermark_utils.PIPE_NAME[pipe_idx],
                                         str(exp_trans_status).upper(), int(exp_trans_result_blocks),
                                         str(prog_trans_status).upper(), int(prog_trans_result_blocks), failure))
                    wm_status = wm_status & status
        if wm_status is False:
            gdhm.report_test_bug_os(f"{GDHM_FEATURE_TAG} TRANS_WM Verification Failed - Blocks/Lines Mismatch ")
        if is_plane_enabled is False and is_cursor_wm is False:
            logging.warning("No planes enabled during Watermark verification !!")
            return True
        return wm_status

    ##
    # @brief        Verify Watermark linetime values
    # @param[in]    exp_lt: expected linetimes
    # @param[in]    prog_lt : programmed linetimes
    # @param[in]    pipe_count: pipe count struct
    # @param[in]    pipe_list : pipe_list struct
    # @return       bool
    def verify_wm_line_time(self, exp_lt, prog_lt, pipe_count, pipe_list):
        status = False
        for pipe_idx in range(pipe_count):
            if pipe_list[pipe_idx].fPixelRate > 0:
                status = True
                exp_line_time = exp_lt[pipe_idx].fLineTime
                prog_line_time = prog_lt[pipe_idx].fLineTime
                if exp_line_time == prog_line_time:
                    logging.info("PASS: WM_LINETIME_{} Expected Linetime={} Actual Linetime={}"
                                 .format(watermark_utils.PIPE_NAME[pipe_idx], exp_line_time, prog_line_time))
                else:
                    logging.error("FAIL: LINETIME MISMATCH: WM_LINETIME_{} Expected Linetime={} Actual Linetime={}"
                                  .format(watermark_utils.PIPE_NAME[pipe_idx], exp_line_time, prog_line_time))
                    gdhm.report_driver_bug_os(f"{GDHM_FEATURE_TAG} FAIL: LINETIME MISMATCH ")
                    status = False
                    break
        return status

    ##
    # @brief        Verify Watermark linetime values
    # @param[in]    pixelclk: pipe pixel clock
    # @param[in]    htotal: pipe htotal
    # @param[in]    pipe : pipe id
    # @param[in]    plane: plane id
    # @param[in]    lines : WM0 lines
    # @param[in]    pclatency : latency of current WM level
    # @param[in]    gfx_index : index
    # @return       bool
    # https://gfxspecs.intel.com/Predator/Home/Index/70087
    def verify_vblank_requirement(self, pixelclk, htotal, pipe, plane, lines, pclatency, gfx_index="gfx_0"):
        ps_fill_time = 0
        fs_time = 0
        ss_time = 0
        s1_hor_downscale = 1.0
        s1_ver_downscale = 1.0
        s2_hor_downscale = 1.0
        s2_ver_downscale = 1.0
        dsc_pre_fill_time = 0
        downscaling_factor = 1

        ps_ctl_value = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % self.platform)
        ps_ctl_offset = 'PS_CTRL_1_' + watermark_utils.PIPE_NAME[pipe]
        ps1_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps_ctl_offset,
                                      self.platform, gfx_index=gfx_index)
        ps2_ctl_offset = 'PS_CTRL_2_' + watermark_utils.PIPE_NAME[pipe]
        ps2_ctl = self.mmio_read.read('PS_CTRL_REGISTER', ps2_ctl_offset,
                                      self.platform, gfx_index=gfx_index)

        pipe_srcsz_offset = 'PIPE_SRCSZ_' + watermark_utils.PIPE_NAME[pipe]
        pipe_srcsz = self.mmio_read.read('PIPE_SRCSZ_REGISTER', pipe_srcsz_offset,
                                         self.platform, gfx_index=gfx_index)
        ps_win_sz1_offset = 'PS_WIN_SZ_1_' + watermark_utils.PIPE_NAME[pipe]
        ps_win_sz1 = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_win_sz1_offset,
                                         self.platform, gfx_index=gfx_index)
        ps_win_sz2_offset = 'PS_WIN_SZ_2_' + watermark_utils.PIPE_NAME[pipe]
        ps_win_sz2 = self.mmio_read.read('PS_WIN_SZ_REGISTER', ps_win_sz2_offset,
                                         self.platform, gfx_index=gfx_index)

        pipe_misc = importlib.import_module("registers.%s.PIPE_MISC_REGISTER" % self.platform)
        pipe_misc_reg = 'PIPE_MISC' + '_' + watermark_utils.PIPE_NAME[pipe]
        pipe_misc_reg_value = self.mmio_read.read('PIPE_MISC_REGISTER', pipe_misc_reg, self.platform,
                                                  gfx_index=gfx_index)
        yuv420_enable = pipe_misc_reg_value.__getattribute__('yuv420_enable')
        if yuv420_enable:
            downscaling_factor = 2

        pixelclk_in_khz = pixelclk * 1000
        linetimeNs = (htotal * 1000000) / pixelclk_in_khz
        linetimeNs = (math.ceil(linetimeNs / 125)) * 125

        if self.platform in watermark_utils.PRE_GEN_16_PLATFORMS:
            wm0_prefill_time = 20000 + lines * linetimeNs
        else:
            wm0_prefill_time = lines * linetimeNs

        if (ps1_ctl.__getattribute__('enable_scaler') != getattr(ps_ctl_value, 'enable_scaler_DISABLE')) & \
                (ps1_ctl.__getattribute__('scaler_binding') == getattr(ps_ctl_value, 'scaler_binding_PIPE_SCALER')):
            s1_hor_downscale = max((pipe_srcsz.__getattribute__('horizontal_source_size') /
                                    ps_win_sz1.__getattribute__('xsize')), 1)
            s1_ver_downscale = max((pipe_srcsz.__getattribute__('vertical_source_size') /
                                    ps_win_sz1.__getattribute__('ysize')), 1)
            fs_time = 4 * linetimeNs

        if (ps2_ctl.__getattribute__('enable_scaler') != getattr(ps_ctl_value, 'enable_scaler_DISABLE')) & \
                (ps2_ctl.__getattribute__('scaler_binding') == getattr(ps_ctl_value, 'scaler_binding_PIPE_SCALER')):
            s2_hor_downscale = max((pipe_srcsz.__getattribute__('horizontal_source_size') /
                                    ps_win_sz2.__getattribute__('xsize')), 1)
            s2_ver_downscale = max((pipe_srcsz.__getattribute__('vertical_source_size') /
                                    ps_win_sz2.__getattribute__('ysize')), 1)
            ss_time = 4 * linetimeNs * s1_hor_downscale * s1_ver_downscale

        ps_fill_time = fs_time + ss_time

        dsc_reg = 'PIPE_DSS_CTL2_P' + watermark_utils.PIPE_NAME[pipe]
        dsc_reg_value = self.mmio_read.read('PIPE_DSS_CTL2_REGISTER', dsc_reg, self.platform, gfx_index=gfx_index)
        dsc_enabled = dsc_reg_value.__getattribute__('left_branch_vdsc_enable')

        if dsc_enabled:
            dsc_pre_fill_time = 1.5 * linetimeNs * s1_ver_downscale * s1_hor_downscale * s2_ver_downscale * \
                                s2_hor_downscale * downscaling_factor

        vblank_offset = 'TRANS_VBLANK_' + watermark_utils.PIPE_NAME[pipe]
        vblank = self.mmio_read.read('TRANS_VBLANK_REGISTER', vblank_offset, self.platform, gfx_index=gfx_index)
        vblank_time = (vblank.__getattribute__('vertical_blank_end') - vblank.__getattribute__(
            'vertical_blank_start')) * linetimeNs
        if vblank_time == 0:  # Handling pipe joiner mode
            vblank_offset = 'TRANS_VBLANK_' + watermark_utils.PIPE_NAME[pipe - 1]
            vblank = self.mmio_read.read('TRANS_VBLANK_REGISTER', vblank_offset, self.platform, gfx_index=gfx_index)
            vblank_time = (vblank.__getattribute__('vertical_blank_end') - vblank.__getattribute__(
                'vertical_blank_start')) * linetimeNs

        if vblank_time == 0:  # Handling for MIPI panels
            return True

        if self.platform not in ['lnl']:
            line_time_req = linetimeNs + (pclatency * 1000) + wm0_prefill_time + ps_fill_time + dsc_pre_fill_time
            logging.debug(f"Line Time Requirement - {line_time_req}")
        else:
            line_time_req = linetimeNs + wm0_prefill_time + ps_fill_time + dsc_pre_fill_time
            logging.debug(f"Line Time Requirement for LNL - {line_time_req}")

        if line_time_req >= vblank_time:
            gdhm.report_driver_bug_os(f"{GDHM_FEATURE_TAG} Linetime requirement is greater/equal to VBlank time")
            return False
        return True


##
# @brief        This class contains all plane parameters as its members
class PlaneObj(object):

    ##
    # @brief        PlaneObj default __init__ function
    def __init__(self):
        self.bStatus = False
        self.lPlaneHorizontal = 0
        self.lPlaneVertical = 0
        self.uiPlaneTilingFormat = 0
        self.bRCStatus = False
        self.fPlaneDownscalingFactor = 1.0
        self.uiBufferAllocated = 0
        self.uiPlaneBpp = 0
        self.uiPlaneRotation = 0
        self.uiPixelFormat = 0
        self.uiPlanarYUV420Component = 0
        self.bAsyncFlip = 0


##
# @brief        This class contains all pipe parameters as its members
class PipeObj(object):

    ##
    # @brief        PipeObj default __init__ function
    def __init__(self):
        self.fPixelRate = 0.0
        self.lHorizontalTotal = 0
        self.fPipeDownscalingFactor = 1.0
        self.bIsInterlaced = False
        self.bIsPipeEnable = False
        self.iPipeId = -1


##
# @brief        This class contains line time value as its member
class PipeLinetimeObj(object):

    ##
    # @brief        PipeLinetimeObj default __init__ function
    def __init__(self):
        self.fLineTime = 0.0


##
# @brief        This class contains WM blocks and lines and enabled status as its members
class PlaneWatermarkObj(object):

    ##
    # @brief        PlaneWatermarkObj default __init__ function
    def __init__(self):
        self.bStatus = False
        self.fResultBlocks = 0
        self.fResultLines = 0


##
# @brief        This class contains WM blocks and enabled status as its members
class PlaneTransWatermarkObj(object):

    ##
    # @brief        PlaneTransWatermarkObj default __init__ function
    def __init__(self):
        self.bStatus = False
        self.fResultBlocks = 0
