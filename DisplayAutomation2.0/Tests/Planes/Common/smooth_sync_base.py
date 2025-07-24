########################################################################################################################
# @file     smooth_sync_base.py
# @brief    This script contains helper functions that will be used by Smooth Sync tests.
# @author   Gaikwad, Suraj
########################################################################################################################

import importlib
import logging
import math
import sys
import unittest

from Libs.Core import flip, enum
from Libs.Core.cmd_parser import parse_cmdline, display_key_pattern
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_utility import plug_displays, unplug
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.system_utility import SystemUtility
from Libs.Core.wrapper import control_api_wrapper
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_watermark import watermark, watermark_utils
from Tests.Planes.Common import planes_verification
from registers.mmioregister import MMIORegister


##
# @brief    Base class for Smooth Sync Tests
class SmoothSyncBase(unittest.TestCase):
    src_list = []
    dest_list = []
    currentMode = []
    sourceID = []
    color_space = []
    path = []
    panelCaps = []
    connected_list = []
    wm = watermark.DisplayWatermark()
    mpo = flip.MPO()
    is_ddrw = SystemUtility().is_ddrw()
    display_config = None
    step = 0
    pipe_id = []
    machine_info = SystemInfo()
    platform = None
    NoLayers = list()
    async_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x2)
    sync_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x1)
    # Default pixel_format and tiling. Can be overridden through command line
    pixel_format = [flip.SB_PIXELFORMAT.SB_R10G10B10A2, flip.SB_PIXELFORMAT.SB_R10G10B10A2]
    tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILE4
    scalar_enable = []

    ##
    # @brief            Unittest setUp function
    # @return           None
    def setUp(self):
        logging.info("Step " + str(self.get_step_info()) + ": ****** TEST STARTS HERE ******************")
        self.test_name = sys.argv[0]
        my_tags = ['-pixelformat', '-tiling']
        self.cmd_line_param = parse_cmdline(sys.argv, my_tags)

        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if self.cmd_line_param['TILING'] != "NONE":
            self.tiling = getattr(flip.SURFACE_MEMORY_TYPE, ''.join(self.cmd_line_param['TILING']))

        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        self.display_config = display_config.DisplayConfiguration()
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.connected_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.connected_list))

        self.underrun = UnderRunStatus()

        self.current_config = self.display_config.get_current_display_configuration()
        self.NoOfDisplays = self.current_config.numberOfDisplays
        for index in range(0, self.NoOfDisplays):
            # self.sourceID.append(self.current_config.displayPathInfo[index].sourceId)
            self.sourceID.append(index)
            display_base_obj = display_base.DisplayBase(self.connected_list[index])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[index])
            self.pipe_id.append(current_pipe)

        self.current_mode = self.display_config.get_current_mode(self.current_config.displayPathInfo[0].targetId)

        ##
        # Source list and destination list for portrait and landscape panels.
        if self.current_mode.HzRes < self.current_mode.VtRes:
            self.src_list = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
            self.dest1_list = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
        else:
            self.src_list = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160), (5120, 2880)]
            self.dest1_list = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160), (5120, 2880)]

        for res in self.dest1_list:
            if res[0] <= self.current_mode.HzRes and res[1] <= self.current_mode.VtRes:
                self.dest_list.append(res)

        self.enable_disable_smooth_sync_feature(True)

        self.mpo.enable_disable_mpo_dft(True, 1)

        ##
        # Get the machine info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

    ##
    # @brief        Enable/Disables SmoothSyncFeatureState
    # @param[in]    self; Object of smooth sync base class
    # @param[in]    enable_feature; Flag to enable/disable SmoothSyncFeatureState registry
    # @return       None
    def enable_disable_smooth_sync_feature(self, enable_feature):
        from Libs.Core.wrapper import control_api_args
        from Libs.Core.wrapper import control_api_wrapper
        ctl_3d_feature_args = control_api_args.ctl_3d_feature_getset_t()
        ctl_3d_feature_args.bSet = True
        ctl_3d_feature_args.ApplicationName = b""
        setFlipMode = control_api_args.CTL_BIT(3) if enable_feature else control_api_args.CTL_BIT(0)
        feature = "Smooth Sync" if setFlipMode == 8 else "Application Default"
        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            if control_api_wrapper.get_set_gaming_flip_modes(ctl_3d_feature_args, setFlipMode, targetid) is False:
                self.fail(f"{feature} is not enabled via control library")
            logging.info(f"Pass: {feature} is enabled via control library")

    ##
    # @brief        Get the color space for provided pixel format.
    # @param[in]    pixel_format pixel format of the plane.
    # @return       Color space for the given pixel format.
    def get_color_space_for_pixel_format(self, pixel_format):
        if pixel_format < 14:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
        else:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

        return color_space

    ##
    # @brief        Get the step value for logging.
    # @return       Step count.
    def get_step_info(self):
        self.step = self.step + 1
        return self.step

    ##
    # @brief        Get the no of planes created for given source id.
    # @param[in]	source_id Source id of the plane.
    # @param[in]	pplanes Pointer to structure PLANE containing the plane info.
    # @return		Plane count for the given source id.
    def get_plane_count_for_source_id(self, source_id, pplanes):
        plane_count = 0
        for index in range(0, pplanes.uiPlaneCount):
            if source_id == pplanes.stPlaneInfo[index].iPathIndex:
                plane_count = plane_count + 1

        return plane_count

    ##
    # @brief        To perform flips
    # @param[in]    pplanes Pointer to structure PLANE containing the plane info.
    # @return       void
    def performFlip(self, pplanes):
        format = ""

        logging.info("Step %s: Checking for the hardware support for plane parameters" % self.get_step_info())

        ##
        # Check for the hardware support for plane parameters
        checkmpo_result = self.mpo.check_mpo3(pplanes)

        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("Step %s: Flipping the planes and verifying the planes" % self.get_step_info())
            ##
            # Flip the content
            ssa_result = self.mpo.set_source_address_mpo3(pplanes)
            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                logging.info("*****************Plane verification started*****************")
                for index in range(0, pplanes.uiPlaneCount):
                    plane_count = self.get_plane_count_for_source_id(pplanes.stPlaneInfo[index].iPathIndex, pplanes)
                    pipe_id = pplanes.stPlaneInfo[index].iPathIndex
                    plane_id = planes_verification.get_plane_id_from_layerindex(plane_count, pplanes.stPlaneInfo[index].uiLayerIndex, gfx_index='gfx_0')
                    pixel_format = pplanes.stPlaneInfo[index].ePixelFormat
                    tile_format = pplanes.stPlaneInfo[index].eSurfaceMemType
                    width = pplanes.stPlaneInfo[index].stMPOSrcRect.lRight - pplanes.stPlaneInfo[
                        index].stMPOSrcRect.lLeft
                    if (pplanes.stPlaneInfo[index].stMPOSrcRect.lRight != pplanes.stPlaneInfo[index].stMPODstRect.lRight
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lBottom != pplanes.stPlaneInfo[
                                index].stMPODstRect.lBottom
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lLeft != pplanes.stPlaneInfo[
                                index].stMPODstRect.lLeft
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lTop != pplanes.stPlaneInfo[
                                index].stMPODstRect.lTop):
                        scalar_enable = 1
                    else:
                        scalar_enable = 0

                    format += planes_verification.get_register_string_from_pixel_format(pixel_format)[20:]

                    if pplanes.stPlaneInfo[index].bEnabled:
                        if not planes_verification.verify_planes(pipe_id, plane_id, pixel_format, tile_format, width,
                                                                 scalar_enable,
                                                                 pplanes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                                                 pplanes.stPlaneInfo[index].stMPOClipRect.lRight,
                                                                 pplanes.stPlaneInfo[index].stMPOClipRect.lTop,
                                                                 pplanes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                                                 pplanes.stPlaneInfo[index].bEnabled):
                            self.fail("Plane verification failed for Pipe: {} Plane: {} Pixel format: {} "
                                      "Tile format: {}".format(pipe_id, plane_id,
                                                               planes_verification.get_register_string_from_pixel_format(
                                                                   pixel_format)[20:],
                                                               planes_verification.get_register_string_from_tile_format(
                                                                   tile_format)[14:]))
                        else:
                            logging.info(
                                "Plane verification passed for Pipe: {} Plane: {} Pixel format: {} "
                                "Tile format: {}".format(pipe_id, plane_id,
                                                         planes_verification.get_register_string_from_pixel_format(
                                                             pixel_format)[20:],
                                                         planes_verification.get_register_string_from_tile_format(
                                                             tile_format)[14:]))
                    else:
                        if not planes_verification.verify_plane_status(pipe_id, plane_id,
                                                                       pplanes.stPlaneInfo[index].bEnabled):
                            self.fail("Plane status verification failed for Pipe: {} Plane: {}"
                                      .format(pipe_id, plane_id))
                        else:
                            logging.info("Plane status verification passed for Pipe: {} Plane {}"
                                         .format(pipe_id, plane_id))

                logging.info("*****************Plane verification ended*****************")

                if not self.wm.verify_watermarks():
                    self.fail("Fail: Watermark verification failed for {} planes with pixel formats {}"
                              .format(pplanes.uiPlaneCount, format))

                if self.underrun.verify_underrun():
                    logging.error("Fail: Underrun occurred after flipping {} planes with pixel formats {}"
                                  .format(pplanes.uiPlaneCount, format))
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                self.fail("Resource creation failed")
            else:
                self.fail("Set source address failed")
        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            self.fail("Resource creation failed")
        else:
            logging.info("Driver did not meet the plane requirements")

    ##
    # @brief        Verify Smooth Sync feature
    # @param[in]	planes Pointer to structure PLANE containing the plane info.
    # @return		True if verification Passes; False, otherwise
    def verify_smooth_sync(self, planes):

        for index in range(0, planes.uiPlaneCount):
            pipe_id = self.pipe_id[planes.stPlaneInfo[index].iPathIndex]
            plane_id = planes_verification.get_plane_id_from_layerindex(self.NoLayers[pipe_id], planes.stPlaneInfo[index].uiLayerIndex, gfx_index='gfx_0')
            if self.smooth_sync_register_verification(pipe_id, plane_id, planes, index) is True:
                logging.info("Smooth Sync register verification passed")
                return True
            return False

    ##
    # @brief        Smooth Sync register verification
    # @param[in]	pipe_id Pipe under verification.
    # @param[in]	plane_id Plane under verification.
    # @param[in]	planes Pointer to structure PLANE containing the plane info.
    # @param[in]	index Index of the plane from planes structure which is under verification.
    # @return		True if verification Passes; False, otherwise
    def smooth_sync_register_verification(self, pipe_id, plane_id, planes, index):
        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform)

        current_pipe = chr(int(pipe_id) + 65)

        plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe
        plane_ctl_value = MMIORegister().read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")

        if plane_enable == getattr(plane_ctl, "plane_enable_ENABLE"):

            ss_enable = plane_ctl_value.__getattribute__("smooth_sync_plane_enable")

            if ss_enable == getattr(plane_ctl, "smooth_sync_plane_enable_SMOOTH_SYNC_ENABLED"):
                logging.info("Smooth Sync Back Plane enabled on plane id %s" % plane_ctl_reg)

                ##
                # Verify the adjacent Smooth Sync plane is enabled or not
                if self.verify_adjacent_smooth_sync_plane(pipe_id, plane_id + 1) is True:
                    logging.info("Smooth Sync Front Plane enabled on plane id PLANE_CTL_%s_%s" %
                                 (str(plane_id + 1), current_pipe))
                    result = True
                    ##
                    # Compare register programming for Smooth Sync Front Plane and Back Plane
                    status = self.compare_planes(planes, index, pipe_id, plane_id, plane_id + 1)
                    result = result and status
                    if status is True:
                        logging.info('Comparison of register programming for Front Plane and Back Plane successful')
                    else:
                        logging.error('Comparison of register programming for Front Plane and Back Plane failed')

                    ##
                    # Check for Min DBuf allocation for front plane
                    status = self.check_min_dbuf_for_front_plane(pipe_id, plane_id + 1)
                    result = result and status
                    if status is True:
                        logging.info("Verification of Min DBuf allocation for Front Plane successful")
                    else:
                        logging.error("Verification of Min DBuf allocation for Front Plane failed")
                        return False

                    ##
                    # Check for Min DBuf allocation for front plane
                    self.check_line_number_advertisement(pipe_id, plane_id + 1)

                    return result

                logging.error("Smooth Sync Front Plane not enabled on plane id PLANE_CTL_%s_%s" %
                              (str(plane_id + 1), current_pipe))
                return False
            else:
                logging.info("Smooth Sync not enabled on plane id %s" % plane_ctl_reg)
                # Not returning False here, because SS might not be enabled for all the planes.

    ##
    # @brief        Verify if Smooth Sync enables 1 more plane for the current plane (Front plane + Back plane)
    # @param[in]	pipe_id Pipe under verification.
    # @param[in]	plane_id Plane under verification.
    # @return		True if verification Passes; False, otherwise
    def verify_adjacent_smooth_sync_plane(self, pipe_id, plane_id):

        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform)

        current_pipe = chr(int(pipe_id) + 65)

        plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe
        plane_ctl_value = MMIORegister().read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")
        ss_enable = plane_ctl_value.__getattribute__("smooth_sync_plane_enable")

        ##
        # Plane should be enabled without the smooth sync bit set
        if (plane_enable == getattr(plane_ctl, "plane_enable_ENABLE")) and \
                (ss_enable == getattr(plane_ctl, "smooth_sync_plane_enable_SMOOTH_SYNC_DISABLED")):
            return True
        return False

    ##
    # @brief       Check if the register programming for the 2 planes is same or not
    # @param[in]   pplanes
    # @param[in]   index for the plane flipped
    # @param[in]   pipe_id
    # @param[in]   plane1_id
    # @param[in]   plane2_id
    # @return      True if register programming matches; False, otherwise
    def compare_planes(self, pplanes, index, pipe_id, plane1_id, plane2_id):
        pixel_format = pplanes.stPlaneInfo[index].ePixelFormat
        tile_format = pplanes.stPlaneInfo[index].eSurfaceMemType
        width = pplanes.stPlaneInfo[index].stMPOSrcRect.lRight - pplanes.stPlaneInfo[
            index].stMPOSrcRect.lLeft
        if (pplanes.stPlaneInfo[index].stMPOSrcRect.lRight != pplanes.stPlaneInfo[index].stMPODstRect.lRight
                or pplanes.stPlaneInfo[index].stMPOSrcRect.lBottom != pplanes.stPlaneInfo[
                    index].stMPODstRect.lBottom
                or pplanes.stPlaneInfo[index].stMPOSrcRect.lLeft != pplanes.stPlaneInfo[
                    index].stMPODstRect.lLeft
                or pplanes.stPlaneInfo[index].stMPOSrcRect.lTop != pplanes.stPlaneInfo[
                    index].stMPODstRect.lTop):
            scalar_enable = 1
        else:
            scalar_enable = 0

        verify_plane1 = planes_verification.verify_planes(pipe_id, plane1_id, pixel_format, tile_format, width,
                                                          scalar_enable,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lRight,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lTop,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                                          pplanes.stPlaneInfo[index].bEnabled)

        verify_plane2 = planes_verification.verify_planes(pipe_id, plane2_id, pixel_format, tile_format, width,
                                                          scalar_enable,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lRight,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lTop,
                                                          pplanes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                                          pplanes.stPlaneInfo[index].bEnabled)

        return verify_plane1 and verify_plane2

    ##
    # @brief       Check if minimum Dbuf is allocated for each active plane
    # @param[in]   pipe_id Pipe under verification.
    # @param[in]   plane_id Plane under verification.
    # @return      True if min Dbuf is allocated; False, otherwise
    def check_min_dbuf_for_front_plane(self, pipe_id, plane_id):
        ##
        # BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/49255?dstFilter=DG2&mode=Filter
        # Note: Current implementation is only for 0/180 degree rotation scenarios
        # Note: Not handling  scenarios for "Planar" pixel formats, as Smooth Sync is only supported for RGB formats

        current_pipe = chr(int(pipe_id) + 65)

        plane_buf_reg = 'PLANE_BUF_CFG_' + str(plane_id) + '_' + current_pipe
        plane_buf = MMIORegister().read('PLANE_BUF_CFG_REGISTER', plane_buf_reg, self.platform, 0x0)
        actual_buf_allocated = plane_buf.__getattribute__("buffer_end") - plane_buf.__getattribute__("buffer_start") + 1

        plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe
        plane_ctl_value = MMIORegister().read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_size_reg = 'PLANE_SIZE_' + str(plane_id) + '_' + current_pipe
        plane_size_value = MMIORegister().read('PLANE_SIZE_REGISTER', plane_size_reg, self.platform)

        ##
        # Planes using Linear or X tiled memory formats must allocate a minimum of 8 blocks.
        if self.tiling in [flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR,
                           flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED]:
            min_dbuf_needed = 8

        ##
        # Planes using Y tiled memory formats must allocate blocks for a minimum number of scan-lines worth
        # of data.
        #
        # Y tiled minimum allocation = Ceil [(4 * Plane source width * Plane Bpp)/512] * MinScanLines/4 + 3
        else:
            pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
            plane_bpp = watermark_utils.GEN11_PIXEL_FORMAT_DICT[pixel_format]['BPP']
            plane_source_width = plane_size_value.__getattribute__("width") + 1
            min_dbuf_needed = math.ceil(float(4 * plane_source_width * plane_bpp) / 512) * 8 / 4 + 3

        ##
        # Compare actual and expected min dbuf allocated
        if actual_buf_allocated < min_dbuf_needed:
            logging.critical("FAIL: Minimum DBuf not allocated for PLANE_{}_{}:"
                             "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                             .format(str(plane_id), current_pipe, min_dbuf_needed, actual_buf_allocated))
            return False
        else:
            logging.info("PASS: Minimum DBuf allocated for PLANE_{}_{}:"
                         "\t Min DBuf required: {}\t Actual allocated Dbuf: {}"
                         .format(str(plane_id), current_pipe, min_dbuf_needed, actual_buf_allocated))
            return True

    ##
    # @brief        Check line number advertisement for Smooth Sync front Plane
    # @param[in]	pipe_id Pipe under verification.
    # @param[in]	plane_id Plane under verification.
    # @return       None
    def check_line_number_advertisement(self, pipe_id, plane_id):

        ##
        # https://gfxspecs.intel.com/Predator/Home/Index/50418?dstFilter=DG2&mode=Filter
        # https://gfxspecs.intel.com/Predator/Home/Index/50382

        plane_chicken = importlib.import_module("registers.%s.PLANE_CHICKEN_REGISTER" % self.platform)

        current_pipe = chr(int(pipe_id) + 65)

        plane_chicken_reg = 'PLANE_CHICKEN_' + str(plane_id) + '_' + current_pipe
        plane_chicken_value = MMIORegister().read('PLANE_CHICKEN_REGISTER', plane_chicken_reg, self.platform, 0x0)

        line_num_advt_enable = plane_chicken_value.__getattribute__("enable_line_number_start_advertisement")

        if line_num_advt_enable == getattr(plane_chicken, "enable_line_number_start_advertisement_ENABLE"):
            plane_surflive_reg = 'PLANE_SURFLIVE_' + str(plane_id) + '_' + current_pipe
            plane_surflive_value = MMIORegister().read('PLANE_SURFLIVE_REGISTER', plane_surflive_reg, self.platform,
                                                       0x0)
            logging.info("Line Number Advertised for Front Plane Plane_{}_{} = {}"
                         .format(plane_id, current_pipe,
                                 plane_surflive_value.__getattribute__("live_surface_base_address")))
        else:
            logging.info("Line Number advertisement not enabled for Front Plane Plane_{}_{}"
                         .format(plane_id, current_pipe))

    ##
    # @brief        Toggle line number advertisement
    # @param[in]	pipe_id Pipe under verification.
    # @param[in]	enable True to enable; False, otherwise
    # @return		None
    def toggle_line_number_advertisement(self, pipe_id, enable):

        driver_interface_ = driver_interface.DriverInterface()
        ##
        # https://gfxspecs.intel.com/Predator/Home/Index/50382
        plane_chicken = importlib.import_module("registers.%s.PLANE_CHICKEN_REGISTER" % self.platform)
        current_pipe = chr(int(pipe_id) + 65)

        for plane_id in range(1, watermark_utils.MAX_PLANES_GEN13 + 1):
            plane_chicken_reg = 'PLANE_CHICKEN_' + str(plane_id) + '_' + current_pipe
            plane_chicken_value = MMIORegister().read('PLANE_CHICKEN_REGISTER', plane_chicken_reg, self.platform,
                                                      0x0).asUint

            if enable:
                # Enable line number advertisement
                value = plane_chicken_value | (1 << 3)  # Set the 3rd bit
                if driver_interface_.mmio_write(getattr(plane_chicken, plane_chicken_reg), value, 'gfx_0') is False:
                    logging.error('Failed to write the PLANE_CHICKEN_{}_{} register with value {}')
            else:
                # Disable line number advertisement
                value = plane_chicken_value & ~(1 << 3)  # Reset the 3rd bit
                if driver_interface_.mmio_write(getattr(plane_chicken, plane_chicken_reg), value, 'gfx_0') is False:
                    logging.error('Failed to write the PLANE_CHICKEN_{}_{} register with value {}')

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        self.mpo.enable_disable_mpo_dft(False, 1)
        self.enable_disable_smooth_sync_feature(False)
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            unplug(display)
        logging.info("Step " + str(self.get_step_info()) + ": ****** TEST ENDS HERE ******************")


if __name__ == '__main__':
    unittest.main()
