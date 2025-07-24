########################################################################################################################
# @file         mpo_dft_helper.py
# @brief        The script implements common helper functions given below that will be used by MPO test scripts:
#               * Get register dump value.
#               * Verify watermark.
#               * Check if the underrun and downscaling has occured.
#               * Verify the register programming.
#               * Obtain the shrink and stretch factor of the plane.
#               * Set the boundary values of the plane.
#               * Calculate the source width and height.
#               * Resize the plane according to the given direction.
# @author       Ashok, Sunaina
########################################################################################################################
import importlib
import logging

from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core.machine_info.machine_info import SystemInfo
from registers.mmioregister import MMIORegister
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Core import flip
from Libs.Core.logger import gdhm

##
# @brief    Contains helper functions that will be used by MPO test scripts
class MPODFTHelper(object):
    platform = None
    machine_info = SystemInfo()
    reg_read = MMIORegister()
    wm = DisplayWatermark()
    underrun = UnderRunStatus()
    source_bound = None
    destination_bound = None
    clip_bound = None
    source_value = None
    source_width = None
    source_height = None
    stepCounter = 0

    ##
    # @brief            Get platform details
    # @return		    void
    def get_platform(self):
        ##
        # Get machine info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

    ##
    # @brief            Get the step value for logging
    # @return           Step count
    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter

    ##
    # @brief            Get regdump value
    # @param[in]        regdump; Register dump value
    # @param[in]        bitfieldname; Field name which has to be searched in regdump
    # @return           Register dump value else return empty string
    def get_enum_for_bitfield(self, regdump, bitfieldname):
        for bit in regdump:
            if bitfieldname in bit:
                return bit.split(':')[1]
        return ""

    ##
    # @brief            Verify watermark
    # @return           True if watermark verification was done, else False
    def verify_watermark(self):
        logging.info(self.getStepInfo() + "Verifying watermark")
        if self.wm.verify_watermarks() is not True:
            logging.critical("Watermark Error Observed")
            return False
        return True

    ##
    # @brief            Check if the underrun has occured
    # @return           True if underrun has occured, else False
    def verify_underrun(self):
        logging.info(self.getStepInfo() + "Checking for Underrun")
        if self.underrun.verify_underrun():
            logging.error("Underrun Occured")
            return True
        return False

    ##
    # @brief            Check if downscaling has occurred
    # @param[in]        plane_info; Information about planes
    # @return           True if downscaling is seen, else False
    def downscaling(self, plane_info):
        if (plane_info.stMPOSrcRect.lRight - plane_info.stMPOSrcRect.lLeft > plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft):
            return True
        return False

    ##
    # @brief            Verify the register programming
    # @param[in]        display; The display
    # @param[in]        plane_ctl_reg; The name of the register
    # @param[in]        expected_pixel_format; The pixel format
    # @param[in]        expected_tile_format; The tile format
    # @param[in]        hflips; Horizontal flips
    # @return           void
    def verify_planes(self, display, plane_ctl_reg, expected_pixel_format, expected_tile_format, hflips=False):

        reg_read = MMIORegister()

        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % (self.platform))
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)
        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
        plane_ctl_value = self.reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        reg_dump = reg_read.dump_register(plane_ctl_value)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")
        if (plane_enable == getattr(plane_ctl, "plane_enable_DISABLE")):
            logging.critical("FAIL: %s - Plane enable status: Expected = ENABLE Actual = %s" % (
                plane_ctl_reg, self.get_enum_for_bitfield(reg_dump, 'plane_enable')))
            return False
        else:
            logging.info("PASS: %s - Plane enable status: Expected = ENABLE Actual = %s" % (
                plane_ctl_reg, self.get_enum_for_bitfield(reg_dump, 'plane_enable')))

        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        if (source_pixel_format == getattr(plane_ctl, expected_pixel_format)):
            logging.info("PASS: %s: Plane Pixel format - Expected = %s Actual = %s" % (
                plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                self.get_enum_for_bitfield(reg_dump, 'source_pixel_format')))
        else:
            logging.critical("FAIL: %s: Plane Pixel format - Expected = %s Actual = %s" % (
                plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                self.get_enum_for_bitfield(reg_dump, 'source_pixel_format')))
            return False

        source_tile_format = plane_ctl_value.__getattribute__("tiled_surface")
        logging.info("%s: Plane tile format - Queried: %s, Programmed:%s" % (
            plane_ctl_reg, expected_tile_format.replace('tiled_surface_', ''),
            self.get_enum_for_bitfield(reg_dump, 'tiled_surface')))

        if hflips:
            if plane_ctl_value.__getattribute__("horizontal_flip") == getattr(plane_ctl, 'horizontal_flip_ENABLE'):
                logging.info("PASS: %s: Horizontal Flip - Expected = %s Actual = %s" % (
                    plane_ctl_reg, 'ENABLE', self.get_enum_for_bitfield(reg_dump, 'horizontal_flip')))
            else:
                logging.critical("FAIL: %s: Horizontal Flip - Expected = %s Actual = %s" % (
                    plane_ctl_reg, 'ENABLE', self.get_enum_for_bitfield(reg_dump, 'horizontal_flip')))
                return False

        return True

    ##
    # @brief            Obtain the shrink and stretch factor of the plane
    # @param[in]        epixel_format; The pixel format of the plane
    # @return           Returns the shrink and stretch factor
    def get_shrink_stretch_factor(self, epixel_format):
        if (
                epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_YUV422 or epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_P010YUV420 or epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_P012YUV420 or epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_P016YUV420):
            return 1, 5
        elif (
                epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8 or epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_B10G10R10X2):
            return 2.999, 5
        elif (epixel_format == flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420):
            return 1.99, 5

    ##
    # @brief            Set the boundary values of the plane
    # @param[in]        hres; Horizontal boundary
    # @param[in]        vres; Vertical boundary
    # @return           None
    def set_bounds(self, hres, vres):
        self.source_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.destination_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.clip_bound = flip.MPO_RECT(0, 0, hres, vres)

    ##
    # @brief            Calculate the source width and height
    # @param[in]        plane_info; The plane whose width and height should be calculated
    # @return           void
    def source_rect(self, plane_info):
        self.source_width = plane_info.stMPOSrcRect.lRight - plane_info.stMPOSrcRect.lLeft
        self.source_height = plane_info.stMPOSrcRect.lBottom - plane_info.stMPOSrcRect.lTop

    ##
    # @brief            Resize the plane according to the given direction
    # @param[in]        plane_info; The plane to be resized
    # @param[in]        cdirection; The direction in which the plane has to be resized
    # @param[in]        ivalue; The value to resize the plane
    # @return           Returns 1(True) on resizing the plane; else 0(False)
    def resize(self, plane_info, cdirection, ivalue):
        shrink_fator, stretch_factor = self.get_shrink_stretch_factor(plane_info.ePixelFormat)

        if (cdirection == "Right"):
            plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight + ivalue
            plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight + ivalue
            if (
                    plane_info.stMPODstRect.lRight > self.destination_bound.lRight or plane_info.stMPODstRect.lRight <= plane_info.stMPODstRect.lLeft):
                plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight - ivalue
                plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if (shrink_fator >= (self.source_width / ldst_width) >= (1 / stretch_factor)):
                plane_info.stMPOSrcRect.lRight = plane_info.stMPODstRect.lRight

            if (plane_info.stMPODstRect.lRight > self.clip_bound.lRight):
                plane_info.stMPOClipRect.lRight = self.clip_bound.lRight

        elif (cdirection == "Left"):
            plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft + ivalue
            plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft + ivalue
            if (
                    plane_info.stMPODstRect.lLeft < self.destination_bound.lLeft or plane_info.stMPODstRect.lLeft >= plane_info.stMPODstRect.lRight):
                plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft - ivalue
                plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if (shrink_fator >= (self.source_width / ldst_width) >= (1 / stretch_factor)):
                plane_info.stMPOSrcRect.lLeft = plane_info.stMPODstRect.lLeft

            if (plane_info.stMPODstRect.lLeft < self.clip_bound.lLeft):
                plane_info.stMPOClipRect.lLeft = self.clip_bound.lLeft

        elif (cdirection == "Bottom"):
            plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom + ivalue
            plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom + ivalue
            if (
                    plane_info.stMPODstRect.lBottom > self.destination_bound.lBottom or plane_info.stMPODstRect.lBottom <= plane_info.stMPODstRect.lTop):
                plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom - ivalue
                plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if (shrink_fator >= (self.source_height / ldst_height) >= (1 / stretch_factor)):
                plane_info.stMPOSrcRect.lBottom = plane_info.stMPODstRect.lBottom

            if (plane_info.stMPODstRect.lBottom > self.clip_bound.lBottom):
                plane_info.stMPOClipRect.lBottom = self.clip_bound.lBottom

        elif (cdirection == "Top"):
            plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop + ivalue
            plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop + ivalue
            if (
                    plane_info.stMPODstRect.lTop < self.destination_bound.lTop or plane_info.stMPODstRect.lTop >= plane_info.stMPODstRect.lBottom):
                plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop - ivalue
                plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if (shrink_fator >= (self.source_height / ldst_height) >= (1 / stretch_factor)):
                plane_info.stMPOSrcRect.lTop = plane_info.stMPODstRect.lTop

            if (plane_info.stMPODstRect.lTop < self.clip_bound.lTop):
                plane_info.stMPOClipRect.lTop = self.clip_bound.lTop

        return True

    ##
    # @brief        Helper function to report GDHM bug when resource creation failed
    # @return       void
    def report_to_gdhm_resource_creation_failure(self):
        gdhm.report_bug(
            title="[MPO][Plane scaling]Resource creation failed",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

    ##
    # @brief        Helper function to report GDHM bug when set source address failed
    # @return       void
    def report_to_gdhm_set_source_address_failure(self):
        gdhm.report_bug(
            title="[MPO][Plane scaling]Set source address failed",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

