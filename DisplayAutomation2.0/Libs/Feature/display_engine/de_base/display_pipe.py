#####################################################################################################
# @file     display_pipe.py
# @brief    Python wrapper exposes interfaces for Display Pipe Verification
# @details  display_pipe.py provides interface's to Verify Display Pipe Configuration
#           for all connected displays, to check if the frame counter is Active.
#           User-Input : DisplayPipe() object - targetID, platform name(skl,icl,..)
#           pipe color space(RGB,YUV), If YUV, pass YUV420 mode (BYPASS, FULLBLEND)
# @note     Supported display interfaces are MIPI, EDP, DP, HDMI\n
# @author   Aafiya Kaleem
##################################################################################################

import logging
import math
import os
import time
from Libs.Core.machine_info import machine_info
from Libs.Core import system_utility as sys_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core import enum
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.vdsc.dsc_enum_constants import DSCEngine
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from registers.mmioregister import MMIORegister

# Pipe Ganged and Tiled modes have PIPEEXCESS added in Pipe Source Size
PIPEEXCESS = 4


##
# @brief YUV420 Mode
class YUV420_MODE(object):
    BYPASS = 0
    FULLBLEND = 1


##
# @brief Pipe output color space
class COLOR_SPACE(object):
    RGB = 0
    YUV = 1


##
# @brief YUV420 Enable/Disable
class YUV420_STATE(object):
    DISABLE = 0
    ENABLE = 1


##
# @brief Pipe Class to do Pipe related verifications
class DisplayPipe(display_base.DisplayBase):
    rrate = ''

    ##
    # @brief Initializes Pipe object
    # @param[in] display_port display to verify
    # @param[in] pipe_color_space color space if RGB/YUV420/YUV444
    # @param[in] YUV420_mode YUV mode of the display if FULLBLEND/BYPASS
    # @param[in] hres horizontal resolution
    # @param[in] vres vertical resolution
    # @param[in] dithering_enabled is enabled/disabled
    # @param[in] gfx_index graphics adapter
    def __init__(self, display_port=None, pipe_color_space=None, YUV420_mode=None,
                 hres=None, vres=None, dithering_enabled=None, gfx_index='gfx_0'):
        self.display_port = display_port
        self.pipe_color_space = pipe_color_space  # RGB,YUV420,YUV444
        self.YUV420_mode = YUV420_mode  # FULLBLEND,BYPASS
        self.hres = hres
        self.vres = vres
        self.dithering_enabled = dithering_enabled  # False/True
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


logger_template = "{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: {act}"


##
# @brief Fill DisplayPipe() instance for the display
# @param[in] pipeObj DisplayPipe() instance
# @param[in] gfx_index graphics adapter
# @return None
def FillPipeStruct(pipeObj, gfx_index='gfx_0'):
    config = display_config.DisplayConfiguration()
    connected_pipe = pipeObj.pipe_suffix
    display_and_adapter_info = config.get_display_and_adapter_info_ex(pipeObj.display_port, gfx_index)

    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(gfx_index, pipeObj.display_port)
    if is_pipe_joiner_required:
        logging.debug("Pipe Joiner is Enabled on Port".format(pipeObj.display_port))

    if (pipeObj.hres is None) or (pipeObj.vres is None):
        scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (connected_pipe), pipeObj.platform,
                                        gfx_index=gfx_index)
        logging.debug("PS_CTRL_1_" + connected_pipe + "--> Offset : "
                      + format(scalar1_reg.offset, '08X') + " Value :" + format(scalar1_reg.asUint, '08X'))

        scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (connected_pipe), pipeObj.platform,
                                        gfx_index=gfx_index)
        logging.debug("PS_CTRL_2_" + connected_pipe + "--> Offset : "
                      + format(scalar2_reg.offset, '08X') + " Value :" + format(scalar2_reg.asUint, '08X'))

        target_mode = config.get_display_timings(display_and_adapter_info)
        source_mode = config.get_current_mode(display_and_adapter_info)
        if ((scalar1_reg.enable_scaler and (scalar1_reg.scaler_binding == 0)) or
                (scalar2_reg.enable_scaler and (scalar1_reg.scaler_binding == 0))):
            logging.debug("PS_CTRL_1_{} & PS_CTRL_2_{} SCALAR is Enabled".format(connected_pipe, connected_pipe))
            if is_pipe_joiner_required:
                s_h_active, t_h_active = source_mode.HzRes, target_mode.hActive
                pipeObj.hres = get_pipe_width(gfx_index, pipeObj, no_of_pipe_required, s_h_active, t_h_active, True,
                                              source_mode.scaling)
            else:
                pipeObj.hres = source_mode.HzRes
            pipeObj.vres = source_mode.VtRes
            pipeObj.rrate = source_mode.refreshRate
        else:
            logging.debug("PS_CTRL_1_{} & PS_CTRL_2_{} SCALAR is Disabled".format(connected_pipe, connected_pipe))
            t_h_active = target_mode.hActive
            if is_pipe_joiner_required:
                pipeObj.hres = get_pipe_width(gfx_index, pipeObj, no_of_pipe_required, t_h_active, t_h_active, False,
                                              source_mode.scaling)
            else:
                pipeObj.hres = target_mode.hActive
            pipeObj.vres = target_mode.vActive
            pipeObj.rrate = (target_mode.vSyncNumerator // target_mode.vSyncDenominator)

    if pipeObj.pipe_color_space is None:
        pipeObj.pipe_color_space = "RGB"
    if pipeObj.YUV420_mode is None:
        pipeObj.YUV420_mode = "FULLBLEND"


##
# @brief        Helper function to calculate the pipe source width in pipe joiner cases.
# @param[in]    gfx_index: str
#                   Contains the Graphics adapter index in which the display is plugged.
# @param[in]    pipe_object: DisplayPipe
#                   Contains the pipe programming related data for the plugged display.
# @param[in]    no_of_pipe_required: int
#                   Contains the no of pipes required to driver the display at current resolution.
# @param[in]    s_h_active: int
#                   Indicates source horizontal active width.
# @param[in]    t_h_active: int
#                   Indicates target horizontal active width.
# @param[in]    is_scalar_enabled: bool
#                   True if scalar is enabled for the current mode, False otherwise.
# @param[in]    scaling_mode: enum
#                   Tells the scaling of the current mode.
# @return       pipe_width: int
#                   Returns the expected pipe source width based on bspec calculation for pipe joiner cases.
def get_pipe_width(gfx_index, pipe_object, no_of_pipe_required, s_h_active, t_h_active, is_scalar_enabled,
                   scaling_mode) -> int:
    is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, pipe_object.display_port)

    # Uncompressed Pipe Joiner case
    if is_dsc_enabled is False:
        plane_width = int(s_h_active / no_of_pipe_required)

        if is_scalar_enabled and scaling_mode not in [enum.MDS, enum.CI]:
            plane_width = plane_width + PIPEEXCESS

        return plane_width

    # Reading the register directly since slice width will be verified in the DSC programming.
    r_offset = 'PPS3_' + str(DSCEngine.LEFT.value) + '_' + pipe_object.pipe_suffix
    dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", r_offset, pipe_object.platform, gfx_index=gfx_index)
    slice_count = math.ceil(t_h_active / dsc_pps3.slice_width)
    no_of_slice_per_pipe = slice_count / no_of_pipe_required

    # Pixel Replication logic is supported from ELG
    # Basically calculates the pipe width along with the pixels that has to be replicated to make it even.
    if pipe_object.platform in ["ELG"]:
        pipe_width = (int(math.ceil(s_h_active / slice_count) * no_of_slice_per_pipe + 1) & ~1)
    else:
        # Prior to ELG there is no pixel replication logic in HW. Driver also doesn't handle this case as there is no
        # standard modes that will result in odd slice width when dividing 8 slice. Modeset will fail if such resolution
        # is applied. Ideally driver should prune this mode if such case arises.
        # E.g 4500x2160, 4500/8 = 562.5 (pic width not evenly divisible by slice width case)
        pipe_width = (s_h_active / slice_count) * no_of_slice_per_pipe

    # Pipe excess is added only when scalar is enabled and when the scaling is not MDS or CI
    if is_scalar_enabled is True and scaling_mode not in [enum.MDS, enum.CI]:
        # For Ultra Pipe Joiner PIPE B and PIPE C will have excess pixels added on both sides.
        # Hence, pipe excess is multiplied by 2 only for those two pipes
        if no_of_pipe_required == 4 and pipe_object.pipe_suffix in ['B', 'C']:
            pipe_width = pipe_width + (2 * PIPEEXCESS)
        else:
            pipe_width = pipe_width + PIPEEXCESS

    return pipe_width


##
# @brief Verify if source BPC is equal to target BPC when dithering is enabled.
# @param[in] pipeObj DisplayPipe() object
# @param[in] gfx_index
# @return bool return true if MMIO programming is correct else false
def VerifyDithering(pipeObj, gfx_index='gfx_0'):
    reg = MMIORegister.read("PIPE_MISC_REGISTER", "PIPE_MISC_%s" % (pipeObj.pipe_suffix), pipeObj.platform,
                            gfx_index=gfx_index)
    logging.debug("PIPE_MISC_" + pipeObj.pipe_suffix + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

    if pipeObj.dithering_enabled is None:
        logging.debug("INFO : Dithering Enabled is NOT set by user.Assigning it to MMIO value")
        pipeObj.dithering_enabled = reg.dithering_enable

    dithering = 1 if pipeObj.dithering_enabled else 0
    if reg.dithering_enable == dithering:
        dithering_str = 'ENABLED' if dithering == 1 else 'DISABLED'
        logging.info(logger_template.format(res="PASS", feature="PIPE_MISC_{} - Dithering".format(pipeObj.pipe_suffix),
                                            exp="{}({})".format(dithering, dithering_str), act=reg.dithering_enable))
        if reg.dithering_enable:
            bpc = display_base.GetTranscoderBPC(pipeObj, gfx_index)

            if bpc == reg.dithering_bpc:
                logging.info("{res:^5}: {feature:<60}: Source  : {exp:<20}  Target: {act}".format(res="PASS",
                                                                                                  feature='Source BPC and Target BPC Matching',
                                                                                                  exp=reg.dithering_bpc,
                                                                                                  act=bpc))
                return True
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PIPE]: Source BPC and Target BPC Mis-Matched! Expected: {0} "
                          "Actual: {1}".format(reg.dithering_bpc, bpc),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("{res:^5}: {feature:<60}: Source  : {exp:<20}  Target: {act}".format(res="FAIL",
                                                                                                   feature='Source BPC and Target BPC doesnot Match',
                                                                                                   exp=reg.dithering_bpc,
                                                                                                   act=bpc))
                return False
        return True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PIPE]: PIPE_MISC_{0} - Dithering status check mis-matched! Expected: "
                  "{1} Actual: {2}".format(pipeObj.pipe_suffix, dithering, reg.dithering_enable),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL",
                                             feature="PIPE_MISC_{} - Dithering [1-->ENABLED, 0-->DISABLED]".format(
                                                 pipeObj.pipe_suffix),
                                             exp=dithering, act=reg.dithering_enable))
    return False


##
# @brief Verify if the frame count is incrementing, no hangs seen.
# @param[in] pipeObj DisplayPipe() object instance
# @param[in] gfx_index graphics adapter
# @return bool true if there is change in frame count else false
def VerifyFrameCount(pipeObj, gfx_index='gfx_0'):
    pipe = pipeObj.pipe_suffix
    retry = 1

    while (retry <= 5):  # framecounter loops back to 0 after (2^32)-1, sometimes we see failures sporadically.
        # Will retry 2 more times if the failure is seen and then report out,if it is failing consistently.
        start = MMIORegister.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_%s" % (pipe), pipeObj.platform,
                                  gfx_index=gfx_index)
        logging.debug("PIPE_FRMCNT_" + pipe + "--> Offset : "
                      + format(start.offset, '08X') + " Value :" + format(start.asUint, '08X'))

        # Added 2 seconds of delay as we were observing frame counter increment after 1 second : HSD-18025368168
        time.sleep(2)  # wait for 2sec, measure frames/sec
        end = MMIORegister.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_%s" % (pipe), pipeObj.platform,
                                gfx_index=gfx_index)
        logging.debug("PIPE_FRMCNT_" + pipe + "--> Offset : "
                      + format(end.offset, '08X') + " Value :" + format(end.asUint, '08X'))

        logging.debug("INFO : Frame Counter Before and After :"
                      + str(start.pipe_frame_counter) + "   " + str(end.pipe_frame_counter))
        if (abs(end.pipe_frame_counter - start.pipe_frame_counter) >= 2):
            # keeping count(2) low for fulsim, because frame increment is slow on fulsim
            # we can either check for frame increment or compare with refresh rate here
            logging.info("{res:^5}: {feature:<60}: Before  : {bef:<20}  After : {aft}".format(res="INFO",
                                                                                              feature="PIPE_FRMCNT_{} - Frame Counter".format(
                                                                                                  pipe),
                                                                                              bef=start.pipe_frame_counter,
                                                                                              aft=end.pipe_frame_counter))
            break
        else:
            logging.debug("WARN : Pipe Frame Counter is NOT ACTIVE for Iteration : %s" % (retry))
            retry = retry + 1
    if retry == 6:  # if frame counter is not active after retrying 5 times, report it out
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PIPE]: Pipe Frame counter is NOT ACTIVE even after 3rd retry",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("ERROR : Pipe Frame Counter is NOT ACTIVE")
        return False
    else:
        return True


##
# @brief Verify if the pipe scanline count is incrementing, no hangs seen.
# @param[in] pipeObj DisplayPipe() object instance
# @param[in] gfx_index graphics adapter
# @return bool true if there is change in pipe scanline count else false
def VerifyScanlineCount(pipeObj, gfx_index='gfx_0'):
    pipe = pipeObj.pipe_suffix
    retry = 1

    pipe_frmcnt_reg = MMIORegister.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_%s" % (pipe), pipeObj.platform,
                                        gfx_index=gfx_index)
    pipe_scanline_reg = MMIORegister.read("PIPE_SCANLINE_REGISTER", "PIPE_SCANLINE_%s" % (pipe), pipeObj.platform,
                                          gfx_index=gfx_index)
    start_scanline_count = pipe_scanline_reg.line_counter_for_display + (
            pipeObj.vres * pipe_frmcnt_reg.pipe_frame_counter)

    while (retry <= 3):  # scanline counter increments very slow in pipe2d.
        # fulsim will increment multiple frames within 5 sec. But, pipe2d may/may not increase even 1 scanline in 5 sec (unpredictable).
        # Will retry 2 more times if the failure is seen and then report out,if it is failing consistently.
        time.sleep(5)  # wait for 5 sec, before reading scanline count again.

        pipe_frmcnt_reg = MMIORegister.read("PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_%s" % (pipe), pipeObj.platform,
                                            gfx_index=gfx_index)
        pipe_scanline_reg = MMIORegister.read("PIPE_SCANLINE_REGISTER", "PIPE_SCANLINE_%s" % (pipe), pipeObj.platform,
                                              gfx_index=gfx_index)
        end_scanline_count = pipe_scanline_reg.line_counter_for_display + (
                pipeObj.vres * pipe_frmcnt_reg.pipe_frame_counter)

        logging.debug("INFO : Scanline Counter (adjusted with frame count) Before = {0} and After = {1}".format(
            start_scanline_count, end_scanline_count))
        if (abs(end_scanline_count - start_scanline_count) >= 1):
            # keeping count(1) low for fulsim, because scanline increment is very slow on pipe2d
            logging.info("{res:^5}: {feature:<60}: Before  : {bef:<20}  After : {aft}".format(res="INFO",
                                                                                              feature="PIPE_SCANLINE_{} - Scanline Counter (adjusted with frame count)".format(
                                                                                                  pipe),
                                                                                              bef=start_scanline_count,
                                                                                              aft=end_scanline_count))
            break
        else:
            logging.debug("WARN : Pipe Scanline Counter is NOT ACTIVE for Iteration : %s" % (retry))
            retry = retry + 1
    if retry == 4:  # if scanline counter is not active after retrying 3 times, report it out
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PIPE]: Pipe Scanline counter is NOT ACTIVE even after 3rd retry",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("ERROR : Pipe Scanline Counter is NOT ACTIVE")
        return False
    else:
        return True


##
# @brief Verify the connected display pipe configuration(resolution, color_space,...).
# @param[in] pipeObj DisplayPipe() class object instance
# @param[in] gfx_index graphics adapter
# @return bool return true,if pipe configuration is correct, else return false
def VerifyConnectedPipe(pipeObj, gfx_index='gfx_0'):
    def cmp(a, b):
        return (a > b) - (a < b)

    pipe = pipeObj.pipe.split("PIPE_")

    reg = MMIORegister.read("PIPE_SRCSZ_REGISTER", "PIPE_SRCSZ_%s" % (pipe[1]), pipeObj.platform, gfx_index=gfx_index)
    logging.debug("PIPE_SRCSZ_" + pipe[1] + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

    if not (reg.horizontal_source_size + 1) % 2 and (reg.vertical_source_size + 1) <= 4320:
        if reg.horizontal_source_size == pipeObj.hres - 1 and reg.vertical_source_size == pipeObj.vres - 1:
            logging.info(logger_template.format(res="PASS",
                                                feature="PIPE_SRCSZ_{} - Pipe Source Size (HActive x VActive)".format(
                                                    pipe[1]),
                                                exp="{} x {}".format(pipeObj.hres, pipeObj.vres),
                                                act="{} x {}".format(reg.horizontal_source_size + 1,
                                                                     reg.vertical_source_size + 1)))

            reg = MMIORegister.read("PIPE_MISC_REGISTER", "PIPE_MISC_%s" % (pipe[1]), pipeObj.platform,
                                    gfx_index=gfx_index)
            logging.debug("PIPE_MISC_" + pipe[1] + " --> Offset : "
                          + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

            if pipeObj.platform in display_base.yuv422_supported_platform_list:
                reg1 = MMIORegister.read("PIPE_MISC2_REGISTER", "PIPE_MISC2_%s" % (pipe[1]), pipeObj.platform,
                                         gfx_index=gfx_index)
                logging.debug("PIPE_MISC2_" + pipe[1] + " --> Offset : "
                              + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))

            if (pipeObj.pipe_color_space == "RGB"):
                if (reg.pipe_output_color_space_select == COLOR_SPACE.RGB):
                    logging.info(
                        logger_template.format(res="PASS", feature="PIPE_MISC_{} - Color Space".format(pipe[1]),
                                               exp="{}({})".format(COLOR_SPACE.RGB, pipeObj.pipe_color_space),
                                               act=reg.pipe_output_color_space_select))
                    return True
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][PIPE]:Pipe_Misc_{0} - Color space check failed! "
                              "Expected:{1}({2}) Actual:{3}".format(pipe[1], COLOR_SPACE.RGB, pipeObj.pipe_color_space,
                                                                    reg.pipe_output_color_space_select),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(
                        logger_template.format(res="FAIL", feature="PIPE_MISC_{} - Color Space".format(pipe[1]),
                                               exp="{}({})".format(COLOR_SPACE.RGB, pipeObj.pipe_color_space),
                                               act=reg.pipe_output_color_space_select))
                    return False

            elif (pipeObj.pipe_color_space == "YUV420"):
                yuv420_mode = True
                ## From Gen15 onwards, bit 26 of PIPE_MISC_REG is reserved. So checking bit26 only if platfrom is Pre Gen15.
                if pipeObj.platform in machine_info.PRE_GEN_15_PLATFORMS:
                    yuv420_mode = (((pipeObj.YUV420_mode == "BYPASS") and (reg.yuv420_mode == YUV420_MODE.BYPASS)) or
                            ((pipeObj.YUV420_mode == "FULLBLEND") and (reg.yuv420_mode == YUV420_MODE.FULLBLEND)))
                if yuv420_mode:
                        if pipeObj.platform in display_base.yuv422_supported_platform_list:
                            expected_yuv_values = [1, 1, 0]
                            actual_yuv_values = [int(reg.pipe_output_color_space_select), int(reg.yuv420_enable),
                                                 int(reg1.yuv_422_mode)]
                        else:
                            expected_yuv_values = [1, 1]
                            actual_yuv_values = [int(reg.pipe_output_color_space_select), int(reg.yuv420_enable)]

                        if cmp(actual_yuv_values, expected_yuv_values) == 0:
                            logging.info(
                                "res= PASS, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act = {}".
                                    format(expected_yuv_values, actual_yuv_values))
                            return True
                        else:
                            gdhm.report_bug(
                                title="[Interfaces][Display_Engine][PIPE]:Mismatch in Expected and Actual YUV values for YUV420"
                                      " color space. Expected: {} Actual: {}".format(expected_yuv_values,
                                                                                     actual_yuv_values),
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            logging.error(
                                "res= FAIL, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act = {}".
                                    format(expected_yuv_values, actual_yuv_values))
                            return False
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][PIPE]:User-input for YUV420 Mode is NOT Correct.Expected:"
                              " (BYPASS, FULLBLEND) Actual: {}".format(pipeObj.YUV420_mode),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error("ERROR : User-input for YUV420 Mode is NOT Correct. Pass <BYPASS or FULLBLEND>")
                    return False

            elif (pipeObj.pipe_color_space == "YUV444"):
                if pipeObj.platform in display_base.yuv422_supported_platform_list:
                    expected_yuv_values = [1, 0, 0]
                    actual_yuv_values = [int(reg.pipe_output_color_space_select), int(reg.yuv420_enable),
                                         int(reg1.yuv_422_mode)]
                else:
                    expected_yuv_values = [1, 0]
                    actual_yuv_values = [int(reg.pipe_output_color_space_select), int(reg.yuv420_enable)]

                    if cmp(actual_yuv_values, expected_yuv_values) == 0:
                        logging.info(
                            "res= PASS, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act ="
                            " {}".format(expected_yuv_values, actual_yuv_values))
                        return True
                    else:
                        gdhm.report_bug(
                            title="[Interfaces][Display_Engine][PIPE]:Mismatch in Expected and Actual YUV values for YUV444"
                                  " color space. Expected: {} Actual: {}".format(expected_yuv_values,
                                                                                 actual_yuv_values),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        logging.error(
                            "res= FAIL, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act"
                            " = {}".format(expected_yuv_values, actual_yuv_values))
                    return False

            elif pipeObj.pipe_color_space == "YUV422" and pipeObj.platform in display_base.yuv422_supported_platform_list:
                expected_yuv_values = [1, 0, 1]
                actual_yuv_values = [int(reg.pipe_output_color_space_select), int(reg.yuv420_enable),
                                     int(reg1.yuv_422_mode)]

                if cmp(actual_yuv_values, expected_yuv_values) == 0:
                    logging.info(
                        "res= PASS, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act = {}".
                            format(expected_yuv_values, actual_yuv_values))
                    return True
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][PIPE]:Mismatch in Expected and Actual YUV values for YUV422"
                              " color space. Expected: {} Actual: {}".format(expected_yuv_values, actual_yuv_values),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(
                        "res= FAIL, values=[COLOR_FORMAT_YUV, YUV_420_ENABLE, YUV_422_ENABLE], exp = {}, act = "
                        "{}".format(expected_yuv_values, actual_yuv_values))
                    return False
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PIPE]:User-input for PIPE Color Space is NOT Correct.Expected: "
                          "(RGB, YUV420, YUV444, YUV422(Gen 13+)) Actual: {}".format(pipeObj.pipe_color_space),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    "ERROR : User-Input for PIPE Color Space is NOT Correct. Pass <RGB or YUV420 or YUV444 or "
                    "YUV422(Supported Gen13 onwards)>")
                return False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PIPE]:PIPE_SRCSZ_{0} - Pipe Source Size check failed! Expected: "
                      "{1} x {2} Actual: {3} x {4}".format(pipe[1], pipeObj.hres, pipeObj.vres,
                                                           reg.horizontal_source_size + 1,
                                                           reg.vertical_source_size + 1),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL",
                                                 feature="PIPE_SRCSZ_{} - Pipe Source Size (HActive x VActive)".format(
                                                     pipe[1]),
                                                 exp="{} x {}".format(pipeObj.hres, pipeObj.vres),
                                                 act="{} x {}".format(reg.horizontal_source_size + 1,
                                                                      reg.vertical_source_size + 1)))
            return False
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PIPE]:BSPEC Violation -Pipe Horizontal/Vertical Source Size {} X {}".format(
                reg.horizontal_source_size + 1, reg.vertical_source_size + 1),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Pipe Horizontal/Vertical Source Size {} X {} is Violating the BSPEC Limitations.".format(
            reg.horizontal_source_size + 1, reg.vertical_source_size + 1))


##
# @brief Verify display pipe programming for the list of DisplayPipe() object.
# @param[in] pipeList DisplayPipe() object instance to specify port_name,
#              pipe color space output(RGB or YUV), if YUV mode(BYPASS or FULLBLEND)
# @param[in] gfx_index graphics adapter
# @return bool Return true if MMIO programming for passed targetID is correct, else return false
def VerifyPipeProgramming(pipeList, gfx_index='gfx_0'):
    status = fail_count = False
    system_utility = sys_utility.SystemUtility()

    for pipeObj in pipeList:
        if pipeObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PIPE]:ERROR : {} port is NOT Connected to any Pipe".format(
                    pipeObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : " + pipeObj.display_port + " NOT Connected to any Pipe. Check if it is Connected")
            return False

        FillPipeStruct(pipeObj, gfx_index)

        logging.info(
            "******* PIPE Verification for {} (Target ID : {}) : {} x {} @ {} *******".format(str(pipeObj.display_port),
                                                                                              pipeObj.targetId,
                                                                                              str(pipeObj.hres),
                                                                                              str(pipeObj.vres),
                                                                                              str(pipeObj.rrate)))

        status = VerifyConnectedPipe(pipeObj, gfx_index)
        if (status is False):
            fail_count = True

        current_exec_env = system_utility.get_execution_environment_type()
        if current_exec_env is None:
            raise Exception('Test failed to identify the current execution environment')
        # in pre-si environment, verify scanline counter since 1 frame time in pre-si will take long time and be unpredictable
        if current_exec_env in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            status = VerifyScanlineCount(pipeObj, gfx_index)
        # in post-si, verify frame counter
        else:
            status = VerifyFrameCount(pipeObj, gfx_index)
        if (status is False):
            fail_count = True

        status = VerifyDithering(pipeObj, gfx_index)
        if (status is False):
            fail_count = True

    if (fail_count):
        return False
    else:
        return status


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    pipeList = []
    pipeList.append(DisplayPipe("DP_A"))
    # pipeList.append(DisplayPipe("DP_A","RGB",None,1920,1080,True))

    result = VerifyPipeProgramming(pipeList, 'gfx_0')
    if result is False:
        # GDHM handled in VerifyPipeProgramming(pipeList, gfx_index)
        logging.error("FAIL : verifyPipeProgramming")
    else:
        logging.info("PASS : verifyPipeProgramming")
