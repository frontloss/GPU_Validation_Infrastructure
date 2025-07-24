########################################################################################################################
# @file         mpo_base.py
# @brief        The script consists of unittest setup and tear down classes for MPO.
#               * Parse command line.
#               * Plug and unplug of displays.
#               * Apply display configuration.
#               * Enable and disable DFT.
# @author       Shetty, Anjali N
########################################################################################################################
import importlib
import sys
import unittest
import logging
import time
from registers.mmioregister import MMIORegister
from Libs.Core import display_utility, cmd_parser, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_master_control import VerificationMethod
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Core import flip
from Tests.Planes.Common import planes_verification, planes_helper
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.display_engine import de_master_control
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core import system_utility as sys_util
from Libs.Feature.presi.presi_crc import start_plane_processing
from registers.mmioregister import MMIORegister

reg_read = MMIORegister()
system_info = SystemInfo()
platform = []


##
# @brief    Base class for MPO tests
class MPOBase(unittest.TestCase):
    connected_list = []
    source_id = []
    pixel_format = []
    color_space = []
    tile_format = []
    dst_list = []
    source_list = []
    no_of_displays = 0
    step = 0
    pipeID = []
    display_config = DisplayConfiguration()
    underrun = UnderRunStatus()
    wm = DisplayWatermark()
    mpo = flip.MPO()
    de_access = de_master_control.DisplayEngine()
    ##
    # SB_PIXELFORMAT values for planar formats
    planar_formats = [15, 17, 18, 19]


    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        ##
        # Custom tags for input pixel format and tile format.
        my_tags = ['-input_pixelformat', '-input_tileformat', '-input_xml', '-wait_for_vbi']

        ##
        # Parse the command line.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, my_tags)

        ##
        # Obtain display port list from the command line.
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        ##
        # Verify and plug the display.
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Apply display configuration as specified in the command line.
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Step %s Failed to apply display configuration %s %s' %
                      (self.get_step_info(), DisplayConfigTopology(topology).name, self.connected_list))
        else:
            logging.info('Step %s Successfully applied the display configuration as %s %s' %
                         (self.get_step_info(), DisplayConfigTopology(topology).name, self.connected_list))

        ##
        # Get current display configuration.
        current_config = self.display_config.get_current_display_configuration()
        self.no_of_displays = current_config.numberOfDisplays
        for index in range(0, self.no_of_displays):
            self.source_id.append(index)
            display_base_obj = DisplayBase(self.connected_list[index])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[index])
            self.pipeID.append(current_pipe)
        ##
        # Get current applied mode.
        self.current_mode = self.display_config.get_current_mode(current_config.displayPathInfo[0].targetId)

        ##
        # Source list and destination list for portrait and landscape panels.
        if self.current_mode.HzRes < self.current_mode.VtRes:
            self.src_list = [(1200, 1920), (1080, 1920), (900, 1600), (720, 1280), (540, 960), (360, 640)]
            self.dest_list = [(1200, 1920), (1080, 1920), (900, 1600), (720, 1280), (540, 960), (360, 640)]
        else:
            self.src_list = [(5120, 2880), (4096, 2160), (3840, 2160), (2560, 1440), (1920, 1080), (1024, 768)]
            self.dest_list = [(5120, 2880), (4096, 2160), (3840, 2160), (2560, 1440), (1920, 1080), (1024, 768)]


        for res in self.dest_list:
            if res[0] <= self.current_mode.HzRes and res[1] <= self.current_mode.VtRes:
                self.dst_list.append(res)

        for res in self.src_list:
            if res[0] <= self.current_mode.HzRes and res[1] <= self.current_mode.VtRes:
                self.source_list.append(res)

        self.wait_for_vbi_after_flip = self.cmd_line_param['WAIT_FOR_VBI'] != "NONE"

        ##
        # Start underrun monitor.
        self.underrun.clear_underrun_registry()

        ##
        # Enable DFT.
        self.mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief            Get the color space for provided pixel format.
    # @param[in]        pixel_format pixel format of the plane.
    # @return           Color space for the given pixel format.
    def get_color_space_for_pixel_format(self, pixel_format):
        if pixel_format < 14:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
        else:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

        return color_space

    ##
    # @brief            Get the no of planes created for given source id.
    # @param[in]	    source_id Source id of the plane.
    # @param[in]	    pplanes Pointer to structure PLANE containing the plane info.
    # @return		    Plane count for the given source id.
    def get_plane_count_for_source_id(self, source_id, pplanes):
        plane_count = 0
        for index in range(0, pplanes.uiPlaneCount):
            if source_id == pplanes.stPlaneInfo[index].iPathIndex:
                plane_count = plane_count + 1

        return plane_count

    ##
    # @brief        Get the step value for logging.
    # @return       Step count.
    def get_step_info(self):
        self.step = self.step + 1
        return self.step

    ##
    # @brief            To perform flips
    # @param[in]        pplanes; Pointer to structure
    # @param[in]        wait_for_vbi_flag; flag to specify to wait for VBI
    # @return           void
    def perform_flip(self, pplanes, wait_for_vbi_flag=True):
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
            # if wait for vbi flag is present, wait until next VBI, currently it is done only for PIPE_A, gfx_0
            if wait_for_vbi_flag or self.wait_for_vbi_after_flip:
                self.wait_for_vbi(0, "gfx_0")

            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                system_utility = sys_util.SystemUtility()
                exec_env = system_utility.get_execution_environment_type()
                if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_adapter_index='gfx_0'):
                    start_plane_processing()
                logging.info("*****************Plane verification started*****************")
                for index in range(0, pplanes.uiPlaneCount):
                    plane_count = self.get_plane_count_for_source_id(pplanes.stPlaneInfo[index].iPathIndex, pplanes)
                    pipe_id = self.pipeID[pplanes.stPlaneInfo[index].iPathIndex]
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

                    if exec_env == 'SIMENV_PIPE2D' and planes_helper.get_flipq_status(gfx_adapter_index='gfx_0'):
                        gfx_display_hwinfo = system_info.get_gfx_display_hardwareinfo()
                        for i in range(len(gfx_display_hwinfo)):
                            platform.append(str(gfx_display_hwinfo[i].DisplayAdapterName).lower())
                        current_pipe = chr(int(pipe_id) + 65)

                        ##
                        # Import PIPE_FRMCNT_REGISTER module.
                        frame_cnt = importlib.import_module("registers.%s.PIPE_FRMCNT_REGISTER" % platform[0])

                        frame_cnt_reg = 'PIPE_FRMCNT_' + current_pipe

                        ##
                        # Read PLANE_CTL_REGISTER values.
                        frame_cnt_val = reg_read.read('PIPE_FRMCNT_REGISTER', frame_cnt_reg, platform[0], 0x0)

                        current_frame_cnt_val = frame_cnt_val.__getattribute__("pipe_frame_counter")
                        logging.info(f"Frame counter value {current_frame_cnt_val}")

                        count = 0
                        while True:
                            time.sleep(600)
                            count = count + 1
                            logging.info(f"Reading Frame counter after {count * 10} mins")
                            frame_cnt_val = reg_read.read('PIPE_FRMCNT_REGISTER', frame_cnt_reg, platform[0],
                                                          0x0)
                            updated_frame_cnt_val = frame_cnt_val.__getattribute__("pipe_frame_counter")
                            logging.info(f"Frame counter value {updated_frame_cnt_val}")
                            if updated_frame_cnt_val > current_frame_cnt_val:
                                logging.info(
                                    f"Frame cnt val current_frame_cnt_val {current_frame_cnt_val} updated_frame_cnt_val {updated_frame_cnt_val}")
                                break
                            elif count > 5:
                                logging.info("Count exceeded")
                                break

                    if pplanes.stPlaneInfo[index].bEnabled:
                        if not planes_verification.verify_planes(pipe_id, plane_id, pixel_format, tile_format, width, scalar_enable,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lRight,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lTop,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                             pplanes.stPlaneInfo[index].bEnabled):
                            gdhm.report_bug(
                                title="[MPO]Plane verification failed for Pipe: {} Plane: {} Pixel format: {} Tile format: {}"
                                    .format(pipe_id, plane_id, planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]),
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail(
                                "Plane verification failed for Pipe: {} Plane: {} Pixel format: {} Tile format: {}"
                                    .format(pipe_id, plane_id, planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]))
                        else:
                            logging.info(
                                "Plane verification passed for Pipe: {} Plane: {} Pixel format: {} Tile format: {}"
                                    .format(pipe_id, plane_id, planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]))
                    else:
                        if not planes_verification.verify_plane_status(pipe_id, plane_id, pplanes.stPlaneInfo[index].bEnabled):
                            gdhm.report_bug(
                                title="[MPO]Plane status verification failed for Pipe: {} Plane: {}"
                                    .format(pipe_id, plane_id),
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane status verification failed for Pipe: {} Plane: {}"
                                      .format(pipe_id, plane_id))
                        else:
                            logging.info("Plane status verification passed for Pipe: {} Plane {}"
                                         .format(pipe_id, plane_id))

                logging.info("*****************Plane verification ended*****************")

                if VerificationMethod.WATERMARK in self.de_access.verification_list:
                    if not self.wm.verify_watermarks():
                        self.fail("Fail: Watermark verification failed for {} planes with pixel formats {}"
                              .format(pplanes.uiPlaneCount, format))
                else:
                    logging.info("Watermark verification skipped")

                if self.underrun.verify_underrun():
                    logging.error("Fail: Underrun occurred after flipping {} planes with pixel formats {}"
                              .format(pplanes.uiPlaneCount, format))
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm.report_bug(
                    title="[MPO]Resource creation failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Resource creation failed")
            else:
                gdhm.report_bug(
                    title="[MPO]Set source address failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Set source address failed")
        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm.report_bug(
                title="[MPO]Resource creation failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Resource creation failed")
        else:
            logging.info("Driver did not meet the plane requirements")
            return

    ##
    # @brief            Wait until the next VBI
    # @param[in]        pipe_id ; pipe id
    # @param[in]        gfx_id ; gfx adapter index
    # @return           void
    def wait_for_vbi(self, pipe_id, gfx_id="gfx_0"):
        environment = sys_util.SystemUtility().get_execution_environment_type()
        # If environment is Pre-si then only exercise this, on POST-SI, it is internally handled
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            return
        logging.info("Waiting until next VBI")
        reg_read = MMIORegister()
        current_pipe = chr(int(pipe_id) + 65)
        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        platform = []
        for i in range(len(gfx_display_hwinfo)):
            platform.append(str(gfx_display_hwinfo[i].DisplayAdapterName).lower())

        previous_frame_count = reg_read.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_" + current_pipe,
                                             platform[0].upper(),
                                             gfx_index=gfx_id)
        while True:
            current_frame_count = reg_read.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_" + current_pipe,
                                                platform[0].upper(),
                                                gfx_index=gfx_id)

            logging.debug(f"Current Framecount {current_frame_count.pipe_frame_counter}")
            if current_frame_count.pipe_frame_counter != previous_frame_count.pipe_frame_counter:
                break

    ##
    # @brief            Calculate the source width and height
    # @param[in]        plane_info The plane whose width and height should be calculated
    # @return           void
    def source_rect(self, plane_info):
        self.source_width = plane_info.stMPOSrcRect.lRight - plane_info.stMPOSrcRect.lLeft
        self.source_height = plane_info.stMPOSrcRect.lBottom - plane_info.stMPOSrcRect.lTop

    ##
    # @brief            Set the boundary values of the plane
    # @param[in]        hres; horizontal boundary
    # @param[in]        vres; vertical boundary
    # @return           void
    def set_bounds(self, hres, vres):
        self.source_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.destination_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.clip_bound = flip.MPO_RECT(0, 0, hres, vres)

    ##
    # @brief            Resize the plane according to the given direction
    # @param[in]        plane_info; The plane to be resized
    # @param[in]        cdirection; The direction in which the plane has to be resized
    # @param[in]        ivalue;  The value to resize the plane
    # @return           Returns 1(True) on resizing the plane; else 0(False)
    def resize(self, plane_info, cdirection, ivalue):
        shrink_factor = 3

        if (cdirection == "Right"):
            plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight + ivalue
            plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight + ivalue
            if (plane_info.stMPODstRect.lRight > self.destination_bound.lRight
                    or plane_info.stMPODstRect.lRight <= plane_info.stMPODstRect.lLeft):
                plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight - ivalue
                plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if shrink_factor >= (self.source_width / ldst_width):
                plane_info.stMPOSrcRect.lRight = plane_info.stMPODstRect.lRight

            if (plane_info.stMPODstRect.lRight > self.clip_bound.lRight):
                plane_info.stMPOClipRect.lRight = self.clip_bound.lRight

        elif (cdirection == "Left"):
            plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft + ivalue
            plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft + ivalue
            if (plane_info.stMPODstRect.lLeft < self.destination_bound.lLeft
                    or plane_info.stMPODstRect.lLeft >= plane_info.stMPODstRect.lRight):
                plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft - ivalue
                plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if shrink_factor >= (self.source_width / ldst_width):
                plane_info.stMPOSrcRect.lLeft = plane_info.stMPODstRect.lLeft

            if (plane_info.stMPODstRect.lLeft < self.clip_bound.lLeft):
                plane_info.stMPOClipRect.lLeft = self.clip_bound.lLeft

        elif (cdirection == "Bottom"):
            plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom + ivalue
            plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom + ivalue
            if (plane_info.stMPODstRect.lBottom > self.destination_bound.lBottom
                    or plane_info.stMPODstRect.lBottom <= plane_info.stMPODstRect.lTop):
                plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom - ivalue
                plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if shrink_factor >= (self.source_height / ldst_height):
                plane_info.stMPOSrcRect.lBottom = plane_info.stMPODstRect.lBottom

            if (plane_info.stMPODstRect.lBottom > self.clip_bound.lBottom):
                plane_info.stMPOClipRect.lBottom = self.clip_bound.lBottom

        elif (cdirection == "Top"):
            plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop + ivalue
            plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop + ivalue
            if (plane_info.stMPODstRect.lTop < self.destination_bound.lTop
                    or plane_info.stMPODstRect.lTop >= plane_info.stMPODstRect.lBottom):
                plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop - ivalue
                plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if shrink_factor >= (self.source_height / ldst_height):
                plane_info.stMPOSrcRect.lTop = plane_info.stMPODstRect.lTop

            if (plane_info.stMPODstRect.lTop < self.clip_bound.lTop):
                plane_info.stMPOClipRect.lTop = self.clip_bound.lTop

        return True

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test cleanup")

        ##
        # Disable DFT.
        self.mpo.enable_disable_mpo_dft(False, 1)

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)


if __name__ == '__main__':
    unittest.main()