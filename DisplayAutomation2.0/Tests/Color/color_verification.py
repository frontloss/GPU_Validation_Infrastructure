import importlib
import logging
import os
import time
import pythoncom
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Libs.Core.wrapper import cui_sdk_wrapper as cui_sdk
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister
from Tests.Color.color_common_utility import gdhm_report_app_color

reg_read = MMIORegister()
machine_info = SystemInfo()
##
# Get the platform info
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break


##
# @brief        Check the output colorspace
# @param[in]    display The diaplay type
# @param[in]    pipe_misc_reg The register name
# @return       Returns the output colorspace
def get_pipe_output_colorspace(display, pipe_misc_reg, expected_csc=None):
    pipe_misc = importlib.import_module("registers.%s.PIPE_MISC_REGISTER" % (platform))
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)
    pipe_misc_reg = pipe_misc_reg + '_' + current_pipe

    pipe_misc_reg_value = reg_read.read('PIPE_MISC_REGISTER', pipe_misc_reg, platform)

    if pipe_misc_reg_value.__getattribute__("pipe_output_color_space_select") == getattr(pipe_misc,
                                                                                         'pipe_output_color_space_select_YUV'):
        programmed_csc = "YUV"
    else:
        programmed_csc = "RGB"


    if programmed_csc == expected_csc:
        logging.info("PASS: %s: Expected CSC = %s, Actual CSC = %s" % (pipe_misc_reg, expected_csc, programmed_csc))
    else:
        gdhm_report_app_color(title="[COLOR]Failed due to pipe output color space mismatch")
        logging.critical(
            "FAIL: %s: Expected CSC = %s, Actual CSC = %s" % (pipe_misc_reg, expected_csc, programmed_csc))

    return programmed_csc


##
# @brief        Verify Pipe Bottom Color CSC Enable status
# @param[in]    reg_bottom_color The Pipe Bottom Color Register
# @param[in]    current_pipe The pipe assigned to the display
# @return       returns True if bottom CSC is enabled; else returns False
def verify_pipe_bottom_status (reg_bottom_color, current_pipe):
    pipe_bottom_color = importlib.import_module("registers.%s.PIPE_BOTTOM_COLOR_REGISTER" % platform)
    pipe_bottom_color_reg = reg_bottom_color + '_' + current_pipe
    pipe_bottom_color_reg_value = reg_read.read('PIPE_BOTTOM_COLOR_REGISTER', pipe_bottom_color_reg, platform)
    if pipe_bottom_color_reg_value.__getattribute__("pipe_csc_enable") == getattr(pipe_bottom_color,
                                                                                  'pipe_csc_enable_ENABLE'):
        logging.info('PASS: %s - Bottom CSC Enable status: Expected = ENABLE, Actual = ENABLE' % pipe_bottom_color_reg)
        return True
    else:
        logging.critical(
            'FAIL: %s - Bottom CSC Enable status: Expected = ENABLE, Actual = DISABLE' % pipe_bottom_color_reg)
        return False


    ##
    # @brief        Get plane CSC usage
    # @param[in]    display The diaplay type
    # @param[in]    reg_val The register name
    # @param[in]    reg_botton_color The register name
    # @return       returns True if bottom CSC is enabled; else returns False
def get_plane_csc_usage(display, plane_ctl_reg, plane_color_ctl_reg, reg_bottom_color):
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)

    plane_ctl_1 = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform)
    plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
    plane_ctl_reg_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform)

    if plane_ctl_reg_value.__getattribute__("plane_enable") == getattr(plane_ctl_1, 'plane_enable_ENABLE'):
        logging.info('PASS: %s - Plane enable status: Expected = ENABLE, Actual = ENABLE' % plane_ctl_reg)
    else:
        logging.critical('FAIL: %s - Plane enable status: Expected = ENABLE, Actual = DISABLE' % plane_ctl_reg)
        gdhm_report_app_color(title="[COLOR]Failed due to plane disabled")
        return False

    if platform == 'skl' or platform == 'kbl' or platform == 'cfl':
        if plane_ctl_reg_value.__getattribute__("pipe_csc_enable") == getattr(plane_ctl_1, 'pipe_csc_enable_ENABLE'):
            logging.info('PASS: %s - Pipe CSC enable status: Expected = ENABLE, Actual = ENABLE' % plane_ctl_reg)
        else:
            gdhm_report_app_color(title="[COLOR]Failed due to pipe csc disabled")
            logging.critical('FAIL: %s - Pipe CSC enable status : Expected = ENABLE, Actual = DISABLE' % plane_ctl_reg)
            return False
        if verify_pipe_bottom_status(reg_bottom_color, current_pipe) is False:
            return False

    elif platform == 'glk' or platform == 'cnl':
        plane_color_ctl = importlib.import_module("registers.%s.PLANE_COLOR_CTL_REGISTER" % (platform))
        plane_color_ctl_reg = plane_color_ctl_reg + '_' + current_pipe
        plane_color_ctl_val = reg_read.read('PLANE_COLOR_CTL_REGISTER', plane_color_ctl_reg, platform)

        if plane_color_ctl_val.__getattribute__("pipe_csc_enable") == getattr(plane_color_ctl,
                                                                              'pipe_csc_enable_ENABLE'):
            logging.info('PASS: %s - Pipe CSC enable status: Expected = ENABLE, Actual = ENABLE' % plane_color_ctl_reg)
        else:
            gdhm_report_app_color(title="[COLOR]Failed due to pipe csc disabled")
            logging.critical(
                'FAIL: %s - Pipe CSC enable status: Expected = ENABLE, Actual = DISABLE' % plane_color_ctl_reg)
            return False

        if verify_pipe_bottom_status(reg_bottom_color, current_pipe) is False:
            return False
    else:
        # csc_mode = importlib.import_module("registers.%s.CSC_MODE_REGISTER" % (platform))
        csc_mode_reg = 'CSC_MODE' + '_' + current_pipe
        csc_mode_val = reg_read.read('CSC_MODE_REGISTER', csc_mode_reg, platform)
        if csc_mode_val.__getattribute__("pipe_output_csc_enable") == 1:
            logging.info('PASS: %s - Pipe CSC enable status: Expected = ENABLE, Actual = ENABLE' % csc_mode_reg)
        else:
            gdhm_report_app_color(title="[COLOR]Failed due to pipe csc disabled")
            logging.critical(
                'FAIL: %s - Pipe CSC enable status: Expected = ENABLE, Actual = DISABLE' % csc_mode_reg)
            return False
    return True


##
# @brief        Get xvYCC status
# @param[in]    display The diaplay type
# @param[in]    dip_reg The register name
# @return       returns True if GMP is enabled; else returns False
def get_xvycc_status(display, video_dip_reg):
    video_dip = importlib.import_module("registers.%s.VIDEO_DIP_CTL_REGISTER" % platform)
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)
    video_dip_reg = video_dip_reg + '_' + current_pipe
    video_dip_reg_value = reg_read.read('VIDEO_DIP_CTL_REGISTER', video_dip_reg, platform)
    if video_dip_reg_value.__getattribute__("vdip_enable_gmp") == getattr(video_dip, 'vdip_enable_gmp_ENABLE_GMP_DIP'):
        logging.info("On Transcoder %s Gamut Metadata Packet-GMP Enabled or ON" % current_pipe)
        return True
    else:
        gdhm_report_app_color(title="[COLOR]Failed to Gamut Metadata Packet disabled")
        logging.info("On Transcoder %s Gamut Metadata Packet-GMP Disabled or OFF" % current_pipe)
        return False


##
# @brief        Get Cursor status
# @param[in]    display The diaplay type
# @param[in]    cursor_reg The register name
# @return       returns True if cursor is enabled; else returns False
def get_cursor_status(display, cursor_reg):
    cur_ctl = importlib.import_module("registers.%s.CUR_CTL_REGISTER" % platform)
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)
    cursor_reg = cursor_reg + '_' + current_pipe
    cur_ctl_value = reg_read.read('CUR_CTL_REGISTER', cursor_reg, platform)
    if cur_ctl_value.__getattribute__("cursor_mode_select") == getattr(cur_ctl, 'cursor_mode_select_DISABLE'):
        logging.debug("Cursor %s is disabled" % current_pipe)
        return False
    else:
        if platform in ('skl', 'kbl', 'cfl', 'glk', 'cnl'):
            if cur_ctl_value.__getattribute__("pipe_csc_enable") == getattr(cur_ctl, 'pipe_csc_enable_ENABLE'):
                logging.debug("Cursor %s is enabled and Cursor %s is using CSC" % (current_pipe, current_pipe))
            else:
                logging.debug("Cursor %s is enabled and Cursor %s is not using CSC" % (current_pipe, current_pipe))
        return True


##
# @brief        Get Video Plane Source Pixel Format
# @param[in]    plane_ctl_reg plane control register value
# @return       None
def get_sprite_plane_source_pixel_format(plane_ctl_value):
    pipe_csc_enable = plane_ctl_value.__getattribute__("source_pixel_format")
    if pipe_csc_enable == 0:
        logging.debug("Source Pixel Format is YUV 16-bit 4:2:2")
    elif pipe_csc_enable == 1:
        logging.debug("Source Pixel Format is RGB 32-bit 2:10:10:10")
    elif pipe_csc_enable == 2:
        logging.debug("Source Pixel Format is RGB 32-bit 8:8:8:8")
    elif pipe_csc_enable == 3:
        logging.debug("Source Pixel Format is RGB 64-bit 16:16:16:16")
    elif pipe_csc_enable == 4:
        logging.debug("Source Pixel Format is YUV 32-bit 4:4:4")
    elif pipe_csc_enable == 5:
        logging.debug("Source Pixel Format is RGB 32-bit XR_BIAS 10:10:10")
    else:
        logging.debug("Source Pixel Format is NA")


##
# @brief        Get Video Sprite Status
# @param[in]    display The diaplay type
# @param[in]    plane_ctl_reg The register name
# @return       returns True if video sprite is enabled; else returns False
def get_video_sprite_status(display, plane_ctl_reg, plane_color_ctl_reg):
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)
    plane_ctl_2 = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform)
    plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
    plane_result = []
    status = False
    # Max Try 5 times to check plane enable status
    for count in range(5):
        plane_ctl_reg_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform)
        if plane_ctl_reg_value.__getattribute__("plane_enable") == getattr(plane_ctl_2, 'plane_enable_ENABLE'):
            logging.info('PASS: %s - Plane enable status: Expected = ENABLE, Actual = ENABLE' % plane_ctl_reg)
            get_sprite_plane_source_pixel_format(plane_ctl_reg_value)
            plane_result.append('Enabled')
            status = True
            break
        time.sleep(1)
        plane_result.append('Disabled')
    if status is not True:
        logging.debug("Plane enable status re-tries --> {}".format(plane_result))
        logging.critical('FAIL: %s - Plane enable status: Expected = ENABLE, Actual = DISABLE' % plane_ctl_reg)
        if platform not in ['skl', 'kbl', 'cfl']:
            logging.info("Video %s is disabled" % current_pipe)
            logging.info("%s disabled and color conversion status not available" % current_pipe)
    return status


##
# @brief        Get Wide Gamut Status
# @param[in]    display The diaplay type
# @param[in]    cge_register The Color Gamut Expansion register
# @param[in]    csc_register The Color Space Conversion register
# @param[in]    lut_register The LUT register
# @return       returns Wide Gamut Slider Level
def get_widegamut_status(display, cge_register, plane_ctl_reg, plane_clr_ctl_reg, lut_register, exp_level):
    driver_interface_ = driver_interface.DriverInterface()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)

    wg_slider_level = 0
    cge_ctl = importlib.import_module("registers.%s.CGE_CTRL_REGISTER" % platform)
    cge_register = cge_register + '_' + current_pipe
    cge_ctl_reg_val = reg_read.read('CGE_CTRL_REGISTER', cge_register, platform)

    if platform == 'skl' or platform == 'kbl' or platform == 'cfl':
        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform)
        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
        plane_ctl_reg_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform)
        if (plane_ctl_reg_value.__getattribute__("pipe_csc_enable") == getattr(plane_ctl,
                                                                               'pipe_csc_enable_ENABLE')) and (
                cge_ctl_reg_val.__getattribute__("cge_enable") == getattr(cge_ctl, 'cge_enable_DISABLE')):
            wg_slider_level = 1
    else:
        plane_color_ctl = importlib.import_module("registers.%s.PLANE_COLOR_CTL_REGISTER" % (platform))
        plane_color_ctl_reg = plane_clr_ctl_reg + '_' + current_pipe
        plane_color_ctl_reg_value = reg_read.read('PLANE_COLOR_CTL_REGISTER', plane_color_ctl_reg, platform)
        if (plane_color_ctl_reg_value.__getattribute__("pipe_csc_enable") == getattr(plane_color_ctl,
                                                                                     'pipe_csc_enable_ENABLE')) and (
                cge_ctl_reg_val.__getattribute__("cge_enable") == getattr(cge_ctl, 'cge_enable_DISABLE')):
            wg_slider_level = 1

    if cge_ctl_reg_val.__getattribute__("cge_enable") == getattr(cge_ctl, 'cge_enable_ENABLE'):
        lut_register = lut_register + '_' + current_pipe
        module_name = 'CGE_WEIGHT_' + 'REGISTER'
        instance = MMIORegister.get_instance(module_name, lut_register, platform)
        lut_reg_offset = instance.offset

        lut_reg_value_0 = driver_interface_.mmio_read(lut_reg_offset, 'gfx_0')
        lut_reg_value_1 = driver_interface_.mmio_read(lut_reg_offset + 4, 'gfx_0')
        lut_reg_value_2 = driver_interface_.mmio_read(lut_reg_offset + 8, 'gfx_0')
        lut_reg_value_3 = driver_interface_.mmio_read(lut_reg_offset + 12, 'gfx_0')
        lut_reg_value_4 = driver_interface_.mmio_read(lut_reg_offset + 16, 'gfx_0')

        if ((168430090 == lut_reg_value_0) and (319687178 == lut_reg_value_1) and (538975512 == lut_reg_value_2) and (
                538976288 == lut_reg_value_3) and (32 == lut_reg_value_4)):
            wg_slider_level = 4
        elif ((0 == lut_reg_value_0) and (218497024 == lut_reg_value_1) and (538974739 == lut_reg_value_2) and (
                538976288 == lut_reg_value_3) and (32 == lut_reg_value_4)):
            wg_slider_level = 3
        elif ((0 == lut_reg_value_0) and (100859904 == lut_reg_value_1) and (319819018 == lut_reg_value_2) and (
                538778134 == lut_reg_value_3) and (32 == lut_reg_value_4)):
            wg_slider_level = 2
    if exp_level != wg_slider_level:
        gdhm_report_app_color(title="[COLOR]Failed to set the expansion level")
    return wg_slider_level


def verify_hue_saturation_with_golden_values(display, my_line):
    my_file = open(
        os.path.join(test_context.TestContext.root_folder(), "Tests\Color\HueSaturation\GoldenHueSaturation.txt"))
    loglist = my_file.readlines()
    my_file.close()

    driver_interface_ = driver_interface.DriverInterface()
    ##
    # Get the platform info
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)
    pipe_misc_reg_name = 'CSC_COEFF_' + current_pipe
    module_name = 'CSC_COEFF_' + 'REGISTER'
    instance = MMIORegister.get_instance(module_name, pipe_misc_reg_name, platform)
    offset = instance.offset
    my_reg_val = []
    ##
    # Read the register values into a list
    for i in range(0, 6):
        reg_value = driver_interface_.mmio_read(offset, 'gfx_0')
        my_reg_val.append(reg_value)
        offset = offset + 4

    for line in loglist:
        if my_line == line.rstrip('\n'):
            index = loglist.index(line)
            for i in range(6):
                index += 1
                if hex(my_reg_val[i]) != loglist[index].rstrip('\n'):
                    return False
                return True


def get_pipe_bpc(display):
    reg_read = MMIORegister()
    machine_info = SystemInfo()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break
    trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (platform))
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)

    if display == "DP_A" and platform != 'tgl':
        trans_ddi_func_reg = 'TRANS_DDI_FUNC_CTL_EDP'
    else:
        trans_ddi_func_reg = 'TRANS_DDI_FUNC_CTL_' + current_pipe

    trans_ddi_func_reg_ctl = reg_read.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_func_reg, platform)

    if (trans_ddi_func_reg_ctl.__getattribute__("bits_per_color") == getattr(trans_ddi_func_ctl,
                                                                             'bits_per_color_6_BPC')):
        logging.info("Color Format: 6BPC")
        pipe_bpc = 6
    elif (trans_ddi_func_reg_ctl.__getattribute__("bits_per_color") == getattr(trans_ddi_func_ctl,
                                                                               'bits_per_color_8_BPC')):
        logging.info("Color Format: 8BPC")
        pipe_bpc = 8
    elif (trans_ddi_func_reg_ctl.__getattribute__("bits_per_color") == getattr(trans_ddi_func_ctl,
                                                                               'bits_per_color_10_BPC')):
        logging.info("Color Format: 10BPC")
        pipe_bpc = 10

    elif (trans_ddi_func_reg_ctl.__getattribute__("bits_per_color") == getattr(trans_ddi_func_ctl,
                                                                               'bits_per_color_12_BPC')):
        logging.info("Color Format: 12BPC")
        pipe_bpc = 12
    else:
        logging.info("Color Format: Unknown >> Error!!!")
        pipe_bpc = -1

    return pipe_bpc, trans_ddi_func_reg


def verify_dithering(display_list, framebuffer_bpc, expected_pixelformat):
    reg_read = MMIORegister()

    # trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (platform))
    pipe_misc_reg = importlib.import_module("registers.%s.PIPE_MISC_REGISTER" % (platform))
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % (platform))

    for display in range(0, len(display_list)):
        dithering_status = "Disabled"
        pipe_bpc = 0

        ##
        # Get the current pipe
        display_base_obj = DisplayBase(display_list[display])
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display_list[display])
        current_pipe = chr(int(current_pipe) + 65)

        pipe_conf_reg = 'PIPE_MISC_' + current_pipe

        pipe_conf_reg_ctl = reg_read.read('PIPE_MISC_REGISTER', pipe_conf_reg, platform)

        plane_ctl_reg = 'PLANE_CTL_1_' + current_pipe
        plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform)

        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        logging.info("Source Pixel format is %s" % source_pixel_format)
        if (source_pixel_format == getattr(plane_ctl, expected_pixelformat)):
            logging.info("Pixel format register verification passed")
        else:
            logging.critical("Pixel format register verification failed")
            return False

        ##
        # Check if dithering is enabled
        if (pipe_conf_reg_ctl.__getattribute__("dithering_enable") == getattr(pipe_misc_reg,
                                                                              'dithering_enable_ENABLE')):
            logging.info("Dithering is enabled")
            dithering_status = "Enabled"

            ##
            # Check the dithering type
            if (pipe_conf_reg_ctl.__getattribute__("dithering_type") == getattr(pipe_misc_reg,
                                                                                'dithering_type_SPATIAL')):
                logging.info("Dithering type: Spatial")
            elif (pipe_conf_reg_ctl.__getattribute__("dithering_type") == getattr(pipe_misc_reg, 'dithering_type_ST1')):
                logging.info("Dithering type: Spatio-Temporal 1")
            elif (pipe_conf_reg_ctl.__getattribute__("dithering_type") == getattr(pipe_misc_reg, 'dithering_type_ST2')):
                logging.info("Dithering type: Spatio-Temporal 2")
            else:
                logging.info("Dithering type: Temporal")
        else:
            logging.info("Dithering is disabled")

        pipe_bpc, _ = get_pipe_bpc(display_list[display])

        if framebuffer_bpc > pipe_bpc and dithering_status == "Disabled" and display_list[display][:4] != "HDMI":
            return False
        elif dithering_status == "Enabled" and (framebuffer_bpc == pipe_bpc or framebuffer_bpc < pipe_bpc) and \
                display_list[display][:4] == "HDMI":
            return False
        elif display_list[display] == "DP_A" and (pipe_bpc != 6 and pipe_bpc != 8):
            return False
        elif display_list[display][:4] == "HDMI" and ((framebuffer_bpc == 16 and pipe_bpc != 12) and pipe_bpc != 8):
            return False
        elif (display_list[display][:2] == "DP" and display_list[display] != "DP_A") and (
                (framebuffer_bpc == 10 and pipe_bpc != 10) and pipe_bpc != 8):
            return False

    return True


def getBPC(bpc):
    bpc_map = {
        6: "6BPC",
        8: "8BPC",
        10: "10BPC",
        12: "12BPC"
    }
    return bpc_map.get(bpc, "Invalid BPC")


def deep_color_verification(display, expected_bpc=None):
    ##
    # Verify for each of the displays
    result = False
    pipe_bpc, register_name = get_pipe_bpc(display)
    if (display == 'DP_A' and pipe_bpc == 6) or (display == 'DP_A' and pipe_bpc == 8):
        logging.info("Bits per color for %s is %s " % (display, getBPC(pipe_bpc)))
        result = True
    elif (display[:2] == "DP" and display != "DP_A") and pipe_bpc == expected_bpc:
        logging.info("Bits per color for %s is %s " % (display, getBPC(pipe_bpc)))
        result = True
    elif display[:4] == 'HDMI' and pipe_bpc == expected_bpc:
        logging.info("Bits per color for %s is %s " % (display, getBPC(pipe_bpc)))
        result = True

    if result:
        # For DP_A, BPC needs to be either 6 or 8. Expected BPC is not used
        if display == 'DP_A':
            logging.info("PASS: %s : Expected = %s Actual = %s" % (register_name, getBPC(pipe_bpc), getBPC(pipe_bpc)))
        else:
            logging.info(
                "PASS: %s : Expected = %s Actual = %s" % (register_name, getBPC(expected_bpc), getBPC(pipe_bpc)))

    else:
        if display == 'DP_A':
            gdhm_report_app_color(title="[COLOR]Transcoder BPC output verification was failed")
            logging.info('FAIL: %s : Expected = %s or %s Actual = %d' % (register_name, getBPC(6), getBPC(8), pipe_bpc))
        else:
            gdhm_report_app_color(title="[COLOR]Transcoder BPC output verification was failed")
            logging.error(
                "FAIL: %s : Expected = %s Actual = %s" % (register_name, getBPC(expected_bpc), getBPC(pipe_bpc)))

    return result


##
# @brief            Verify the register programming
# @param[in]        display The display
# @return           pipe_status The pipe status which is either enabled or disabled
# @return           hw_3d_lut_status The Hw LUT status which is either enabled or disabled
# @return           hw_lut_buffer_status The Hw LUT buffer status which is either loaded or not
def verify_3d_lut(display):
    driver_interface_ = driver_interface.DriverInterface()
    reg_read = MMIORegister()
    pipe_status = "DISABLED"
    hw_3d_lut_status = "DISABLED"
    hw_lut_buffer_status = "NOT_LOADED"

    ##
    # Get the platform type
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break

    ##
    # Import the register values
    lut_3d_ctl = importlib.import_module("registers.%s.LUT_3D_CTL_REGISTER" % (platform))
    lut_3d_index = importlib.import_module("registers.%s.LUT_3D_INDEX_REGISTER" % (platform))
    lut_3d_data = importlib.import_module("registers.%s.LUT_3D_DATA_REGISTER" % (platform))
    trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (platform))
    trans_conf = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % (platform))

    ##
    # Get the current pipe value
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)

    if display == "DP_A":
        trans_conf_reg = 'TRANS_CONF_EDP'
        trans_ddi_func_reg = 'TRANS_DDI_FUNC_CTL_EDP'
    else:
        trans_conf_reg = 'TRANS_CONF_' + current_pipe
        trans_ddi_func_reg = 'TRANS_DDI_FUNC_CTL_' + current_pipe

    trans_ddi_func_reg_ctl = reg_read.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_func_reg, platform)
    trans_conf_reg_ctl = reg_read.read('TRANS_CONF_REGISTER', trans_conf_reg, platform)

    reg_ctl = 'LUT_3D_CTL_' + current_pipe
    reg_val_lut_3d_ctl = reg_read.read('LUT_3D_CTL_REGISTER', reg_ctl, platform)

    reg_index = 'LUT_3D_INDEX_' + current_pipe
    reg_index_offset = getattr(lut_3d_index, reg_index)
    driver_interface_.mmio_write(reg_index_offset, 0x00002000, 'gfx_0')

    ##
    # Check if the pipe is enabled
    if (trans_conf_reg_ctl.__getattribute__("transcoder_enable") == getattr(trans_conf, 'transcoder_enable_ENABLE')):
        if (trans_ddi_func_reg_ctl.__getattribute__("edp_dsi_input_select") == getattr(trans_ddi_func_ctl,
                                                                                       'edp_dsi_input_select_PIPE_A')):
            logging.info("Pipe A is enabled")
            pipe_status = "Enabled"

            ##
            # Check if the HW 3D LUT is enabled
            lut_3d_enable = reg_val_lut_3d_ctl.__getattribute__("lut_3d_enable")
            if lut_3d_enable == getattr(lut_3d_ctl, 'lut_3d_enable_ENABLE'):
                logging.info("Hw 3D LUT is enabled on pipe A")
                hw_3d_lut_status = "Enabled"

                ##
                # Read the 3D LUT data
                reg_data = 'LUT_3D_DATA' + '_' + current_pipe
                reg_data_offset = getattr(lut_3d_data, reg_data)
                for i in range(0, 4913):
                    reg_val_lut_3d_data = driver_interface.DriverInterface().mmio_read(reg_data_offset, 'gfx_0')
                    logging.info("%s" % reg_val_lut_3d_data)

                ##
                # Check if the new LUT is ready
                new_lut_ready = reg_val_lut_3d_ctl.__getattribute__("new_lut_ready")
                if new_lut_ready == getattr(lut_3d_ctl, 'new_lut_ready_NEW_LUT_NOT_READY'):
                    logging.info("Hardware finished loading the lut buffer into internal working RAM")
                    hw_lut_buffer_status = "Finished"
                else:
                    logging.info("Hardware did not load the lut buffer into internal working RAM")
                    hw_lut_buffer_status = "NOT_LOADED"

            else:
                logging.info("Hw 3D LUT is disabled on pipe A")
                hw_3d_lut_status = "DISABLED"

    else:
        logging.info("Pipe A is disabled")
        pipe_status = "DISABLED"

    driver_interface_.mmio_write(reg_index_offset, 0x00000000, 'gfx_0')

    return pipe_status, hw_3d_lut_status, hw_lut_buffer_status


def verify_mpo_color_coexistence(display, plane_ctl_reg, plane_color_ctl_reg, expected_pixel_format):
    plane_csc = "disabled"
    plane_gamma = "disabled"
    format_verify = False
    reg_read = MMIORegister()

    ##
    # Get the current pipe
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe = chr(int(current_pipe) + 65)

    ##
    # Get the platform info
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break

    trans_conf = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % (platform))
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % (platform))

    if display == "DP_A":
        trans_conf_reg = 'TRANS_CONF_EDP'
    else:
        trans_conf_reg = 'TRANS_CONF_' + current_pipe

    trans_conf_val = reg_read.read('TRANS_CONF_REGISTER', trans_conf_reg, platform)

    ##
    # Check if the pipe is enabled
    if trans_conf_val.__getattribute__("transcoder_enable") == getattr(trans_conf, 'transcoder_enable_ENABLE'):
        logging.info("Pipe enabled")
    else:
        logging.info("Pipe disabled")

    plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
    plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform)
    plane_enable = plane_ctl_value.__getattribute__("plane_enable")

    ##
    # Check if the plane is enabled
    if (plane_enable == getattr(plane_ctl, "plane_enable_DISABLE")):
        logging.critical("Plane is not enabled")
    else:
        logging.info("Plane is enabled")

    source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

    ##
    # Check the pixel format
    if (source_pixel_format == getattr(plane_ctl, expected_pixel_format)):
        logging.info("Pixel format register verification passed")
        format_verify = True
    else:
        logging.critical("Pixel format register verification failed")

    if platform == 'skl' or platform == 'kbl' or platform == 'cfl':
        ##
        # Check the plane CSC status
        if (plane_ctl_value.__getattribute__("plane_yuv_to_rgb_csc_dis") == getattr(plane_ctl,
                                                                                    'plane_yuv_to_rgb_csc_dis_ENABLE')):
            logging.info("Plane CSC is enabled")
            plane_csc = "enabled"
        else:
            logging.info("Plane CSC is disabled")

        ##
        # Check plane gamma status
        if (plane_ctl_value.__getattribute__("plane_gamma_disable") == getattr(plane_ctl,
                                                                               'plane_gamma_disable_ENABLE')):
            logging.info("Plane gamma enabled")
            plane_gamma = "enabled"
    else:
        plane_color_ctl = importlib.import_module("registers.%s.PLANE_COLOR_CTL_REGISTER" % (platform))
        plane_color_ctl_reg = plane_color_ctl_reg + '_' + current_pipe
        plane_color_ctl_val = reg_read.read('PLANE_COLOR_CTL_REGISTER', plane_color_ctl_reg, platform)

        ##
        # Check plane CSC status
        if (plane_color_ctl_val.__getattribute__("plane_csc_mode") != getattr(plane_color_ctl,
                                                                              'plane_csc_mode_BYPASS')):
            logging.info("Plane CSC enabled")
            plane_csc = "enabled"
        else:
            logging.info("Plane CSC disabled")

        ##
        # Check plane gamma status
        if (plane_color_ctl_val.__getattribute__("plane_gamma_disable") == getattr(plane_color_ctl,
                                                                                   'plane_gamma_disable_ENABLE')):
            logging.info("Plane gamma enabled")
            plane_gamma = "enabled"
        else:
            logging.info("Plane gamma disabled")
    return plane_csc, plane_gamma, format_verify

##
# @brief        Get WideGamut info and check if WideGamut is supported
# @param[in]    device id of the connected display
# @return       bool - Feature supported flag
def is_wide_gamut_supported(dev_id: int) -> bool:
    status = False
    title = ""
    component = ""
    wide_gamut = cui_sdk.GamutExpansion(device_id=dev_id)
    sdk_status, wide_gamut = cui_sdk.get_wide_gamut_expansion(wide_gamut)
    if sdk_status:
        if wide_gamut.isFeatureSupported:
            logging.info(f"WideGamut is supported on {dev_id}")
            status = True
        else:
            title = "[COLOR] WideGamut is not supported "
            component = gdhm.Component.Test.DISPLAY_OS_FEATURES
            logging.error(f"WideGamut is not supported on {dev_id}")
    else:
        title = "[COLOR] wide gamut is not supported "
        component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: get_wide_gamut_expansion() for device_id {dev_id}")
        assert sdk_status, f"SDK call failed: get_wide_gamut_expansion() for device_id {dev_id}"
    if status is False:
        gdhm_report_app_color(title=title,component=component)
    return status

##
# @brief        Set WideGamut expansion level and verify the set values
# @param[in]    device id of the connected display
# @param[in]    expansion level integer value
# @return       bool - verification status
def set_and_verify_wg_expansion_level(dev_id: int, exp_level: int) -> bool:
    status = False
    title = ""
    component= ""
    expected_wide_gamut = cui_sdk.GamutExpansion(device_id=dev_id, gamut_expansion_level=exp_level)
    sdk_status = cui_sdk.set_wide_gamut_expansion(expected_wide_gamut)
    if sdk_status:
        logging.info(f"Wide Gamut Expansion level set to {exp_level} for device_id {dev_id}")
        actual_wide_gamut = cui_sdk.GamutExpansion(device_id=dev_id)
        sdk_status, actual_wide_gamut = cui_sdk.get_wide_gamut_expansion(actual_wide_gamut)
        if sdk_status:
            if actual_wide_gamut.gamutExpansionLevel == expected_wide_gamut.gamutExpansionLevel:
                logging.info(f"Wide Gamut Expansion Level verified successfully.")
                status = True
            else:
                title = "[COLOR] Failed to set Wide Gamut Expansion Level "
                component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
                logging.error(f"Failed to set Wide Gamut Expansion Level.")
                logging.error(
                    f"gamutExpansionLevel: Expected={expected_wide_gamut.gamutExpansionLevel}, Actual={actual_wide_gamut.gamutExpansionLevel}")
        else:
            title = "[COLOR] SDK call: get_wide_gamut_expansion() failed "
            component = gdhm.Component.Test.DISPLAY_OS_FEATURES
            logging.error(f"SDK call failed: get_wide_gamut_expansion() for device_id {dev_id}")
    else:
        title = "[COLOR] wide gamut is not supported "
        component = gdhm.Component.Test.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: set_wide_gamut_expansion() for device_id {dev_id}")
    if status is False:
        gdhm_report_app_color(title=title, component=component)
    return status

##
# @brief        Get Narrow Gamut and check if NarrowGamut is supported
# @param[in]    device id of the connected display
# @return       bool - Feature supported flag
def is_narrow_gamut_supported(dev_id: int) -> bool:
    status = False
    title = ""
    component = ""
    narrow_gamut = cui_sdk.Gamut(device_id=dev_id)
    sdk_status, narrow_gamut = cui_sdk.get_narrow_gamut(narrow_gamut)
    if sdk_status:
        if narrow_gamut.isFeatureSupported:
            logging.info(f"NarrowGamut is supported on {dev_id}")
            status = True
        else:
            title = "[COLOR] NarrowGamut is not supported "
            component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
            logging.error(f"NarrowGamut is not supported on {dev_id}")
    else:
        title = "[COLOR] Narrow gamut is not supported "
        component = gdhm.Component.Test.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: get_narrow_gamut() for device_id {dev_id}")
        assert sdk_status, f"SDK call failed: get_narrow_gamut() for device_id {dev_id}"
    if status is False:
        gdhm_report_app_color(title=title, component=component)
    return status

##
# @brief        Set Color accuracy and verify the set values
# @param[in]    device id of the connected display
# @param[in]    enable/disable boolean flag
# @return       bool - verification status
def configure_and_verify_color_accuracy(dev_id: int, flag: bool) -> bool:
    status = False
    title = ""
    component = ""
    expected_narrow_gamut = cui_sdk.Gamut(device_id=dev_id, enable_disable=flag)
    config_state = 'Enable' if flag else 'Disable'
    sdk_status = cui_sdk.configure_color_accuracy(gamut=expected_narrow_gamut)
    if sdk_status:
        logging.info(f"Narrow Gamut Flag set to {config_state} for device_id {dev_id}")
        actual_narrow_gamut = cui_sdk.Gamut(device_id=dev_id, enable_disable=flag)
        sdk_status, actual_narrow_gamut = cui_sdk.get_narrow_gamut(gamut_args=actual_narrow_gamut)
        if sdk_status:
            if actual_narrow_gamut.enableDisable == expected_narrow_gamut.enableDisable:
                logging.info(f"Narrow Gamut color accuracy configuration '{config_state}d' successfully.")
                status = True
            else:
                logging.error(f"Failed to set Narrow Gamut Expansion Level.")
                component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
                logging.error(
                    f"gamutExpansionLevel: Expected={expected_narrow_gamut.enableDisable}, Actual={actual_narrow_gamut.enableDisable}")
        else:
            title = "[COLOR] Narrow gamut is not supported "
            component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
            logging.error(f"SDK call failed: get_narrow_gamut() for device_id {dev_id}")
    else:
        title = "[COLOR] SDK call: configure_color_accuracy() failed "
        component = gdhm.Component.Test.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: configure_color_accuracy() for device_id {dev_id}")

    if status is False:
        gdhm_report_app_color(title=title, component=component)
    return status

##
# @brief        Get HueSat info and check if HueSat is supported
# @param[in]    device id of the connected display
# @return       bool - Feature supported flag
def is_hue_sat_supported(dev_id: int) -> bool:
    status = False
    title = ""
    hue_sat = cui_sdk.HueSatInfo(device_id=dev_id)
    sdk_status, hue_sat = cui_sdk.get_hue_sat_info(hue_sat)
    if sdk_status:
        if hue_sat.isFeatureSupported:
            logging.info(f"Hue and Saturation supported on {dev_id}")
            status = True
        else:
            title = "[COLOR]Hue and Saturation not supported"
            component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
            logging.error(f"Hue and Saturation not supported on {dev_id}")
    else:
        title = "[COLOR] Failed to get hue and saturation valyes"
        component = gdhm.Component.Test.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: get_hue_sat_info() for device_id {dev_id}")
        assert sdk_status, f"SDK call failed: get_hue_sat_info() for device_id {dev_id}"
    if status is False:
        gdhm_report_app_color(title=title,component=component)
    return status

##
# @brief        Get HueSat info and verify if set
# @param[in]    expected hue_sat info structure
# @return       bool - verification status
def verify_hue_sat_info(expected_hue_sat: cui_sdk.HueSatInfo) -> bool:
    status = False
    title = ""
    component = ""
    actual_hue_sat = cui_sdk.HueSatInfo(device_id=expected_hue_sat.deviceID)
    current_hue = expected_hue_sat.hueSettings.currentValue
    current_sat = expected_hue_sat.saturationSettings.currentValue
    sdk_status, actual_hue_sat = cui_sdk.get_hue_sat_info(actual_hue_sat)
    if sdk_status:
        if current_hue == actual_hue_sat.hueSettings.currentValue and \
                current_sat == actual_hue_sat.saturationSettings.currentValue:
            logging.info(f"hue_value: {current_hue} and sat_value: {current_sat} set successfully.")
            status = True
        else:
            title ="[COLOR]Failed to set Hue and Saturation"
            component = gdhm.Component.Driver.DISPLAY_OS_FEATURES
            logging.error("Failed to set Hue and Saturation values!")
            logging.error(f"hue_value: Expected={current_hue}, Actual={actual_hue_sat.hueSettings.currentValue}")
            logging.error(f"sat_value: Expected={current_sat}, Actual={actual_hue_sat.saturationSettings.currentValue}")
    else:
        title = "[COLOR] Failed to set hue and saturation vales "
        component = gdhm.Component.Test.DISPLAY_OS_FEATURES
        logging.error(f"SDK call failed: get_hue_sat_info() for device_id {expected_hue_sat.deviceID}")
        assert sdk_status, f"SDK call failed: get_hue_sat_info() for device_id {expected_hue_sat.deviceID}"
    if status is False:
        gdhm_report_app_color(title=title, component = component)
    return status
