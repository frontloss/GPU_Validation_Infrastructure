######################################################################################
# @file     color_common_utility.py
# @brief    This script contains helper functions that will be used by Color test scripts
# @author   Smitha B
######################################################################################

import os
import logging
import time
import subprocess
import math

from Libs.Core import display_power
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import etl_parser
from Libs.Core import window_helper, winkb_helper, driver_escape, registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper.driver_escape_args import AviInfoOperation
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Tests.Color import color_parse_etl_events
from Tests.Color.ColorTransforms import color_transforms_constants
from Tests.Color.HDR.Gen11_Flip.MPO3H import HDRConstants
from Tests.Color.RGBQuantisation import rgb_verification
from Tests.Planes.Common import hdr_verification
from registers.mmioregister import MMIORegister


##
# Get the platform info
def get_platform_info():
    platform = None
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break
    return platform


#
# Get_bit_value
def get_bit_value(value, start, end):
    retvalue = value << (31 - end) & 0xffffffff
    retvalue = retvalue >> (31 - end + start) & 0xffffffff
    return retvalue


#
# Get_current_pipe
def get_current_pipe(display):
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe_notation = chr(int(current_pipe) + 65)
    logging.info("Current pipe : Pipe %s ", current_pipe_notation)
    return current_pipe_notation


##
# Fetch DPCD_data from the required dpcd_address
def fetch_dpcd_data(dpcd_address, target_id):
    flag, dpcd_value = driver_escape.read_dpcd(target_id, dpcd_address)
    if flag is False:
        logging.error("Failed to read DPCD Address %s" % dpcd_address)
    logging.debug("DPCD Address %s : %s" % (hex(dpcd_address), dpcd_value[0]))
    return dpcd_value[0]


############################
# Test Function
############################


##
# @brief invoke_power_states() Set the power state S3/CS, S4, S5
# @param[in] - power_state i.e. S3/CS, S4, S5 etc.
# @return - True -On Success,False -On Failure
def invoke_power_states(power_state):
    display_power_ = display_power.DisplayPower()

    logging.info("Invoking POWER_STATE event %s" % power_state.name)
    # Invoke S3/CS state
    if power_state == display_power.PowerEvent.S3:
        if display_power_.is_power_state_supported(display_power.PowerEvent.S3):
            power_state = display_power.PowerEvent.S3
        else:
            power_state = display_power.PowerEvent.CS
            logging.info("System does not support S3; hence invoking CS state")
    if not display_power_.invoke_power_event(power_state, 0):
        logging.error("Power Event: %s FAILURE" % power_state.name)
        return False
    else:
        logging.info("Power Event : %s SUCCESS" % power_state.name)
        return True


##
# @brief launch_overlay() Launch the overlay application
# @param[in] - None
# @return - True -On Success,False -On Failure
def launch_overlay():
    app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                           cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
    if not app:
        logging.error("Failed to launch overlay application")
        gdhm.report_bug(
            title="[Color][OSHDR] Failed to launch overlay application",
            problem_classification=gdhm.ProblemClassification.OTHER,
            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False
    else:
        logging.info("Successfully launched overlay application")
        return True, app


##
# @brief video_play_back() Launch the HDR Clip and do the windows event as set Fullscreen/Pause/Play/Windowed Mode
# @param[in] -  is_full_screen -i.e bool, default video will be launched in full screen
# @return - True -On Success,False -On Failure
def video_play_back(is_full_screen=True):
    machine_info = SystemInfo()
    media_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO")

    ##
    # @TO-DO Need to upload hdr videos
    video_file = os.path.join(media_path, 'mpo_1920_1080_avc.mp4')
    ##
    # Close any previously opened media player
    window_helper.close_media_player()

    ##
    # Minimize all windows before opening media player
    window_helper.minimize_all_windows()

    window_helper.open_uri(video_file)
    time.sleep(5)

    media_window_handle = window_helper.get_window('Movies & TV', True) is None or (window_helper.get_window
                                                                                    ('Films & TV', True)) is None

    if media_window_handle:
        if is_full_screen:
            ##
            # Media player opened in windowed mode, put it to full screen mode
            logging.debug("Changing  media player to fullscreen mode")
            window_helper.press("ALT_ENTER")
            winkb_helper.press(' ')  # Pause the video
            time.sleep(5)
            winkb_helper.press(' ')  # Play the video
            time.sleep(10)

        else:
            # currently in FullScreen Mode. Change to Windowed mode
            logging.debug("Changing player to Windowed mode")
            window_helper.press('ESC')
            window_helper.press('ESC')
            winkb_helper.press(' ')  # Pause the video
            time.sleep(5)
            winkb_helper.press(' ')  # Play the video
            time.sleep(10)
        window_helper.close_media_player()
    else:
        logging.error("Failed to launch Movies & TV application")
        gdhm.report_bug(
            title="[Color][OSHDR] Failed to launch Movies & TV application",
            problem_classification=gdhm.ProblemClassification.OTHER,
            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False


##
# @brief display_switch() Perform display_switching across display for Single/Clone/Extended
# @param[in] -  Topology -i.e Single/Clone/Extended
# @param[in] - connected_list -i.e [EDP/HDMI/DP]
# @return - True -On Success,False -On Failure
def display_switch(topology, connected_list):
    config = display_config.DisplayConfiguration()
    if config.set_display_configuration_ex(topology, connected_list) is True:
        return True
    else:
        return False


##
# @brief monitor_turn_off_on_events() Perform Monitor Turn OFF/ON across displays
# @return - True -On Success,False -On Failure
def monitor_turn_off_on_events():
    logging.info("Invoking Monitor Turn OFF")
    display_power_ = display_power.DisplayPower()
    if display_power_.invoke_monitor_turnoff(display_power.MonitorPower.OFF, 5) is False:
        logging.error("Failed to Turned Off Monitor")
        return False
    logging.info("Successfully turned Off Monitor")

    ##
    # Invoke Monitor Turn on
    logging.info("Invoking Monitor Turn ON")
    if display_power_.invoke_monitor_turnoff(display_power.MonitorPower.ON, 5) is False:
        logging.error("Failed to Turned On Monitor")
        return False
    logging.info("Successfully turned On Monitor")
    return True


##
# @brief apply_native_mode() Apply native modeset across displays with refresh rate
# @param[in] - connected_list -i.e [EDP/HDMI/DP]
# @param[in] - enumerated_displays - Info from display Utility
# @param[in] - refresh_rate -Info from display config
# @return - True -On Success,False -On Failure
def apply_native_mode(connected_list, enumerated_displays, refresh_rate):
    result = False
    config = display_config.DisplayConfiguration()
    target_id = config.get_target_id(connected_list, enumerated_displays)
    supported_modes = config.get_all_supported_modes([target_id])
    native_mode = config.get_native_mode(target_id)
    if native_mode is None:
        logging.error(f"Failed to get native mode for {target_id}")
        return False
    hzres = native_mode.hActive
    vtres = native_mode.vActive
    rr = native_mode.refreshRate

    logging.info("Native mode is %s %s %s" % (hzres, vtres, rr))

    for key, values in supported_modes.items():
        for mode in values:
            if mode.HzRes == hzres and mode.VtRes == vtres and mode.scaling == enum.MDS:
                if refresh_rate is not None:  # To apply the native resolution with refresh rate
                    if mode.refreshRate == refresh_rate:
                        mode.refreshRate = refresh_rate
                result = config.set_display_mode([mode])
                break

    if result:
        current_mode = config.get_current_mode(target_id)
        logging.info("Successfully applied display mode  %sX%s@%s with scaling : %s" % (
            current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
        return True
    else:
        gdhm.report_bug(
            title="[Color][OSHDR]Failed to apply the required modeset",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False


##
# @brief hotunplug_plug_display_etl_trace() Performs Unplug and Plug across all connected displays
# @param[in] - cmdline_args_dict - Command line dictionary
# @param[in] -cmd_parser - To parse commandline with args
# @param[in] - connected_list -i.e [EDP/HDMI/DP]
# @return - True -On Success,False -On Failure
def hotunplug_plug_display_etl_trace(cmdline_args_dict, cmd_parser, connected_list):
    hdmi_edid = ""
    dp_edid = ""
    dp_dpcd = ""

    for key, value in cmdline_args_dict.items():
        if cmd_parser.display_key_pattern.match(key) is not None:
            connector_port_name = value['connector_port']
            if connector_port_name[:2] == 'DP':
                ##
                # Assign default edid_name if it is None
                if value['edid_name'] is not None:
                    dp_edid = value['edid_name']
                    ##
                # Assign default dpcd_name if it is None
                if value['dpcd_name'] is not None:
                    dp_dpcd = value['dpcd_name']

            if connector_port_name[:4] == 'HDMI':
                # Assign default edid_name if it is None
                if value['edid_name'] is not None:
                    hdmi_edid = value['edid_name']
    ##
    #  Unplug activity
    for display in connected_list:
        if (display_utility.get_vbt_panel_type(display, 'gfx_0') in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]) is False:

            if display_utility.unplug(display) is False:
                logging.error("Failed to unplug %s" % display)
                return False
            else:
                logging.info("Successfully unplugged %s" % display)
    time.sleep(5)
    ##
    # Hotplug activity
    for display in connected_list:
        if (display_utility.get_vbt_panel_type(display, 'gfx_0') in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]) is False:
            if display[:2] == "DP":
                if display_utility.plug(display, dp_edid, dp_dpcd) is False:
                    logging.info("Failed to plug %s" % display)
                    return False
                else:
                    logging.info("Plugged %s successfully" % display)
            elif display[:4] == "HDMI":
                if display_utility.plug(display, hdmi_edid) is False:
                    logging.info("Failed to plug %s" % display)
                    return False
                else:
                    logging.info("Plugged %s successfully" % display)
    return True


##
# @brief        Helper function to check if Power_mode was DC and then switch to AC Mode for enabling HDR
# @return       Get:Invalid- Power_mode, Set: True -On Success, False -On Failure
def check_and_apply_power_mode():

    disp_power = display_power.DisplayPower()
    current_power_state = disp_power.get_current_powerline_status()
    status = False

    ##
    # Enable Simulated Battery
    simbat_status_failed = "FAILED_TO_ENABLE_SIMBAT"
    if disp_power.enable_disable_simulated_battery(True) is False:
        logging.error("Failed to enable simulated battery")
        return simbat_status_failed, status
    else:
        logging.info("Successfully enabled simulated battery")

    if current_power_state == 255:
        return "Failed due to Invalid power line status", status
    else:
        if current_power_state == 0:
            ##
            # Setting power line to ac mode
            status = disp_power.set_current_powerline_status(display_power.PowerSource.AC)
            if status:
                return "Switched from DC mode to AC mode successfully", status
            else:
                return "Switching to AC mode failed, as HDR won't enpable in DC Mode", status

        else:
            status = True
            return "No switch required as power Source is already in AC", status


##
# @brief        Helper function to start ETL capture.
# @return       status, True if ETL started otherwise False
def start_etl_capture(test_function_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_Before_Scenario_' + test_function_name + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture.
# @return       etl_file_path, path of ETL file captured
def stop_etl_capture(test_function_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_' + test_function_name + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        logging.debug("Generated ETL file name {0}".format(file_name))
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after test function")
    return etl_file_path


# @brief set_os_brightness() Invoking OS API to set the OS Brightness Slider
# @param[in] -  brightness_slider_value - Any value between 0 to 100
# @param[in] -  delay - default is 0;
def set_os_brightness(brightness_slider_value, delay=0):
    executable = 'SetMonitorBrightness.exe'
    commandline = executable + ' ' + str(brightness_slider_value) + ' ' + str(delay)
    currentdir = os.getcwd()
    os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
    os.system(commandline)
    os.chdir(currentdir)
    logging.info("OS_brightness set Successfully to %s level" %brightness_slider_value)


def apply_lut(lut, num_of_samples, input_value):
    temp = input_value * (num_of_samples - 1)
    x1 = int(math.floor(temp))
    x2 = x1 if (x1 == (num_of_samples-1)) else x1+1
    y1 = lut[x1]
    y2 = lut[x2]
    x = temp
    if x2 == x1:
        output = y1
    else:
        y = y1 + (((x-x1) * (y2-y1)) / (x2-x1))
        output = y

    return output


def get_mantissa(bin_mantissa):
    sum = 1.0 #implied 2^0
    #sum from n = 0 to 22 bn^(-(n+1))
    i = 22
    while (i >= 0):
        bit = bin_mantissa >> i & 1
        power = pow(2, i - 23)
        sum += power * bit
        i = i-1
    return sum


def get_exponent(bin_expo):
    sum = 0.0
    # convert binary char to int
    i=7
    while i >= 0:
        bit = bin_expo >> i & 1
        power = pow(2,i)
        sum += power * bit
        i-=1
    return (sum-127) #; //adjust


def convert_int_to_float(int_value):
    sign_mask = 0x80000000
    expo_mask = 0x7F800000
    mantissa_mask = 0x7FFFFF
    mantissa = int_value & mantissa_mask
    expo = (int_value & expo_mask) >> 23
    sign = (int_value & sign_mask) >> 31
    isign = -1 if sign == 0b1 else 1
    float_val = isign * get_mantissa(mantissa) * pow(2,get_exponent(expo))
    return float_val


##
#
def get_register_offset(module_name, reg_name, current_pipe, platform):
    reg_name = reg_name + "_" + current_pipe
    instance = MMIORegister.get_instance(module_name, reg_name, platform)
    return instance.offset


# @brief        Helper function to mutliply two 3x3 matrices
# @return       returns the resultant matrix
def matrix_multiply_3X3(matrix1, matrix2):
    res_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(0, 3):
        for j in range(0, 3):
            res_matrix[i][j] = 0
            for k in range(0, 3):
                res_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
    return res_matrix


##
# Utility to get ColorConversionBlock
def get_color_conversion_block(platform, current_pipe):
    if platform in ("icllp", "lkf1", "ehl", "jsl", "tgl", "adls" "rkl", "dg1"):
        color_conv_blk = "cc1"
    else:
        # On D13+ platforms, for Pipe A and B, CC2 Blocks will be used,
        # for other pipes, CC1 blocks will be used
        if current_pipe in ("A", "B"):
            color_conv_blk = "cc2"
        else:
            color_conv_blk = "cc1"
    return color_conv_blk


#####################################################################################
#####################  All functions related to Pipe DeGamma ########################
#####################################################################################

##
# Utility to fetch information about DeGamma enable\disable based on SDR\HDR Mode
def verify_degamma_enable(platform, current_pipe, hdr_mode=False):
    color_conv_blk = get_color_conversion_block(platform, current_pipe)
    gamma_reg_name = "GAMMA_MODE" + "_" + current_pipe
    gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_reg_name, platform)
    if color_conv_blk == "cc1":
        if hdr_mode:
            if gamma_mode_reg.pre_csc_gamma_enable:
                logging.error("FAIL: Pipe Pre CSC Gamma : Expected = DISABLE Actual = ENABLE")
                gdhm_report_app_color(title="[COLOR]Failed due to Pipe Pre CSC Gamma enabled")
                return False
            else:
                logging.info("PASS: In HDR Mode, Pipe Pre CSC Gamma : Expected = DISABLE Actual = DISABLE")
        else:
            if gamma_mode_reg.pre_csc_gamma_enable:
                logging.info("PASS: Pipe Pre CSC Gamma : Expected = ENABLE Actual = ENABLE")
            else:
                logging.error("FAIL: Pipe Pre CSC Gamma : Expected = ENABLE Actual = DISABLE")
                gdhm_report_app_color(title="[COLOR]Failed due to Pipe Pre CSC Gamma disabled")
                return False
    else:
        if hdr_mode:
            if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                logging.error("FAIL: Pipe Pre CSC CC2 Gamma : Expected = DISABLE Actual = ENABLE")
                gdhm_report_app_color(title="[COLOR]Failed due to Pipe Pre CSC CC2 Gamma enabled")
                return False
            else:
                logging.info("PASS: In HDR Mode, Pipe Pre CSC CC2 Gamma : Expected = DISABLE Actual = DISABLE")
        else:
            if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                logging.info("PASS: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = ENABLE")
            else:
                logging.error("FAIL: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = DISABLE")
                gdhm_report_app_color(title="[COLOR]Failed due to Pipe Pre CSC Gamma disabled")
                return False
    return True


##
# Utility to fetch the DeGamma Data from MMIO Registers
def get_degamma_lut_from_register(platform, current_pipe):
    color_conv_blk = get_color_conversion_block(platform, current_pipe)
    lut_data = []
    # Setting auto increment bit to 1 in index register
    if color_conv_blk == "cc1":
        index_module_name = 'PRE_CSC_GAMC_INDEX_REGISTER'
        index_reg_name = 'PRE_CSC_GAMC_INDEX'
        index_offset = get_register_offset(index_module_name, index_reg_name, current_pipe, platform)
        index_reg_name = 'PRE_CSC_GAMC_INDEX_' + current_pipe
        index_reg = MMIORegister.read(index_module_name, index_reg_name, platform)
        data_module_name = 'PRE_CSC_GAMC_DATA_REGISTER'
        data_reg_name = 'PRE_CSC_GAMC_DATA_' + current_pipe
        no_samples = 35
    else:
        index_module_name = 'POST_CSC_CC2_INDEX_REGISTER'
        index_reg_name = 'POST_CSC_CC2_INDEX'
        index_offset = get_register_offset(index_module_name, index_reg_name, current_pipe, platform)
        index_reg = MMIORegister.read(index_module_name, index_reg_name, platform)
        data_module_name = 'POST_CSC_CC2_DATA_REGISTER'
        data_reg_name = 'POST_CSC_CC2_DATA_' + current_pipe
        no_samples = 131

    for index in range(0, no_samples):
        index_reg.index_value = index
        driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, 'gfx_0')
        data_reg = MMIORegister.read(data_module_name, data_reg_name, platform)
        lut_data.append(data_reg.gamma_value)
    return lut_data


#####################################################################################
#####################  All functions related to Pipe CSC ############################
#####################################################################################
##
# Decoding the OneDLut given by OS
def decode_os_csc_data(os_csc_data):
    csc_lut, csc_lut_in_single_prec_format, flat_matrix = [], [], []
    for index in range(0, len(os_csc_data), 4):
        ##
        # Just to make sure that only one byte is being considered
        val1 = int(os_csc_data[index]) & 0xFF
        val2 = int(os_csc_data[index + 1]) & 0xFF
        val3 = int(os_csc_data[index + 2]) & 0xFF
        val4 = int(os_csc_data[index + 3]) & 0xFF
        value = val4 << 24 | val3 << 16 | val2 << 8 | val1
        csc_lut.append(value)

    for index in range(0, len(csc_lut)):
        csc_lut_in_single_prec_format.append(convert_int_to_float(csc_lut[index]))

    ##
    # Create a 3x4 matrix from a flat matrix
    csc_lut = [csc_lut_in_single_prec_format[i:i+4] for i in range(0, len(csc_lut_in_single_prec_format),4)]
    ##
    # Considering only 3x3 matrix and discarding the 3x1 matrix
    for i in range(0, 3):
        for j in range(0, 3):
            flat_matrix.append(csc_lut[i][j])
    csc_data = [flat_matrix[i:i+3] for i in range(0,len(flat_matrix), 3)]

    return csc_data


##
# Utility to generate reference XYZ - RGB matrix, based on SDR\HDR Mode
def generate_reference_csc_matrix(os_csc_data, hdr_mode=True):
    if hdr_mode:
        rgb_xyz_matrix = color_transforms_constants.BT2020_RGB_to_XYZ_conversion
        xyz_rgb_matrix = color_transforms_constants.XYZ_to_BT2020_RGB_conversion
    else:
        rgb_xyz_matrix = color_transforms_constants.BT709_RGB_to_XYZ_conversion
        xyz_rgb_matrix = color_transforms_constants.XYZ_to_BT709_RGB_conversion

    inter_matrix = matrix_multiply_3X3(os_csc_data, rgb_xyz_matrix)
    reference_lut = matrix_multiply_3X3(xyz_rgb_matrix, inter_matrix)

    return reference_lut


##
# Utility to convert CSC Coefficients from register format as float coefficients(defined as per BSpec)
def convert_csc_regformat_to_coeff(csc_coeff):
    position_of_point_from_right = 0

    sign_bit = get_bit_value(csc_coeff, 15, 15)
    exponent = get_bit_value(csc_coeff, 12, 14)
    mantissa = int(get_bit_value(csc_coeff, 3, 11))

    if exponent == 6:
        position_of_point_from_right = 7
    elif exponent == 7:
        position_of_point_from_right = 8
    elif exponent == 0:
        position_of_point_from_right = 9
    elif exponent == 1:
        position_of_point_from_right = 10
    elif exponent == 2:
        position_of_point_from_right = 11
    elif exponent == 3:
        position_of_point_from_right = 12

    scale_factor = math.pow(2.0, float(position_of_point_from_right))
    out_val = float(mantissa) / scale_factor
    if sign_bit:
        out_val = out_val * -1

    return out_val


##
# Utility to fetch the CSC coefficients from register
def get_csc_coeff_matrix_from_reg(platform, current_pipe, csc_type="LINEAR"):
    color_conv_blk = get_color_conversion_block(platform, current_pipe)
    if csc_type == "LINEAR":
        unit_name = "CSC_COEFF" if color_conv_blk == "cc1" else "CSC_CC2_COEFF"
    else:
        unit_name = "OUTPUT_CSC_COEFF"

    platform = get_platform_info()
    programmed_val = [[0,0,0],[0,0,0],[0,0,0]]
    csc_coeff = [[0,0,0],[0,0,0],[0,0,0]]

    module_name = unit_name + "_REGISTER"
    reg_name = unit_name + "_" + current_pipe
    instance = MMIORegister.get_instance(module_name, reg_name,platform)
    base_offset = instance.offset
    for i in range(0, 3):
        offset = (base_offset + i*8 ) # 2 DWORDS for each row RGB
        reg_val = driver_interface.DriverInterface().mmio_read(offset, 'gfx_0')
        csc_reg = MMIORegister.get_instance(module_name,reg_name,platform,reg_val)
        programmed_val[i][0]= csc_reg.coeff1
        programmed_val[i][1]= csc_reg.coeff2
        reg_val = driver_interface.DriverInterface().mmio_read(offset+4, 'gfx_0')
        csc_reg =MMIORegister.get_instance(module_name,reg_name,platform,reg_val)
        programmed_val[i][2]= csc_reg.coeff1

    for i in range(0,3):
        for j in range(0,3):
            csc_coeff[i][j] = convert_csc_regformat_to_coeff(programmed_val[i][j])

    return csc_coeff


##
# Utility to identify whether the csc matrix is Identity or otherwise
def identify_csc_matrix_type(csc_matrix):
    reference_identity_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    if csc_matrix == reference_identity_matrix:
        return "IDENTITY"
    return "NON_IDENTITY"


##
# @brief  Utility to get programmed pre/post Offset register values
# Output programmed_offset list
def get_programmed_offset_val(platform, current_pipe, module_name, reg_name):
    offset = get_register_offset(module_name, reg_name, current_pipe, platform)
    programmed_offset = []
    for index in range(0, 3):
        programmed_offset.append(driver_interface.DriverInterface().mmio_read(offset, 'gfx_0'))
        offset += 4
    return programmed_offset


##
# Utility to compare programmed and reference CSC.
# In case of an Identity CSC, difference between programmed and reference should be 0
# In Non-Identity case, an error of difference of 0.005 is accepted
def compare_csc_coeff(prog_csc_val, ref_csc_value):
    threshold = 0 if identify_csc_matrix_type(ref_csc_value) == "IDENTITY" else 0.005
    logging.debug("Programmed CSC Value is %s" %prog_csc_val)
    logging.debug("Reference CSC Value is %s" %ref_csc_value)
    result = True
    for i in range(0,3):
        for j in range(0,3):
            if prog_csc_val[i][j] * ref_csc_value[i][j] >= 0.0:
                logging.debug("Difference in value is %s" % (math.fabs(prog_csc_val[i][j] - ref_csc_value[i][j])))
                diff_value = abs(ref_csc_value[i][j] - prog_csc_val[i][j])
                if diff_value > 0:
                    error_percentage = (diff_value / ref_csc_value[i][j]) / 100
                    if error_percentage > threshold:
                        logging.error("Error Percentage is %s @index %s; Expected_Value is %s; Programmed_Value is %s" % (i, j, ref_csc_value[i][j], prog_csc_val[i][j]))
                        return False
            else:
                return False
    return result


# @brief        output_csc_coeff_verfication - Helper function to generate prog and ref values and compare
# @return       returns the status True/False
def output_csc_coeff_verfication(platform, pipe, bpc, input, output, conv_type):

    status = False
    prog_csc_coeff = get_csc_coeff_matrix_from_reg(platform, pipe, csc_type="NON_LINEAR")
    identity_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ref_csc_coeff = hdr_verification.HDRVerification().scale_csc_for_range_conversion(bpc, input, output, conv_type, identity_matrix)

    logging.debug("Programmed CSC Coefficients are %s" % prog_csc_coeff)
    logging.debug("Reference CSC Coefficients are %s" % ref_csc_coeff)
    if compare_csc_coeff(prog_csc_coeff, ref_csc_coeff) is False:
        logging.error("OutputCSC Coeffients are not Matching")
        return status
    else:
        logging.info("OutputCSC Coefficients Verification Successful")
        status = True
        return status


# @brief        csc_pre_or_post_off_verification - Helper function to generate prog and ref values for pre/post
#               and compare the values
# @return       returns the status True/False
def csc_pre_or_post_off_verification(platform,pipe,bpc,input,output,conv_type,module_name,reg_name):

    status = False
    if module_name != "OUTPUT_CSC_PREOFF_REGISTER":
        reference_offset = hdr_verification.HDRVerification().get_offsets_for_range_conversion(bpc, input, output,conv_type)
    else:
        reference_offset = [0, 0, 0]
    programmed_offset = get_programmed_offset_val(platform,pipe,module_name,reg_name)

    logging.debug("Reference values are %s" % reference_offset)
    logging.debug("Programmed values are %s" % programmed_offset)

    if reference_offset == programmed_offset:
        logging.info("PASS : %s Verification is successful" % reg_name)
        status = True
    else:
        logging.error("FAIL : %s Verification failed" % reg_name)
    return status


#####################################################################################
#####################  All functions related to Pipe Gamma ##########################
#####################################################################################
##
# Decoding the OneDLut given by OS
def decode_os_one_d_lut(os_given_1d_lut):
    one_d_lut = []
    one_d_lut_in_single_prec_format = []
    for index in range(0, len(os_given_1d_lut)):
        ##
        # Just to make sure that only 32 bits/Uint32 is being considered
        val = int(os_given_1d_lut[index]) & 0xFFFFFFFF
        one_d_lut.append(val)

    for index in range(0, len(one_d_lut)):
        one_d_lut_in_single_prec_format.append(convert_int_to_float(one_d_lut[index]))
    return one_d_lut_in_single_prec_format


##
# @brief set_os_brightness() Invoking OS API to set the OS Brightness Slider
# @param[in] -  current_pipe - Current pipe assigned to the display
# @param[in] -  gamma_mode - Gamma mode programmed in the Gamma_Mode register;
#                           In case of Gen11 and Gen12 - MULTI_SEGMENTED; Gen13 - LOGARITHMIC
def apply_unity_gamma(r_factor=1, g_factor=1, b_factor=1):
    logging.info("Trying to apply Gamma LUT with R_ScaleFactor : %s, G_ScaleFactor : %s, B_ScaleFactor : %s" % (r_factor, g_factor, b_factor))
    executable = 'UnityGamma.exe' + ' ' + '-r' + ' ' + repr(r_factor) + ' ' + '-g' + ' ' + repr(g_factor) + ' ' + '-b' + ' ' + repr(b_factor)
    current_dir = os.getcwd()
    os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
    os.system(executable)
    os.chdir(current_dir)
    logging.info("Successfully applied Gamma LUT with R_ScaleFactor : %s, G_ScaleFactor : %s, B_ScaleFactor : %s" % (r_factor, g_factor, b_factor))

##
# @brief oetf_2084() To apply to 2084 OETF curve for the given input values
# @param[in] -  input_val - Current pipe assigned to the display
def oetf_2084(input_val, src_max_luminance=10000.0):
    m1 = 0.1593017578125
    m2 = 78.84375
    c1 = 0.8359375
    c2 = 18.8515625
    c3 = 18.6875
    cf = 1.0
    output = 0.0
    if input_val != 0.0:
        cf = src_max_luminance / 10000.0
        input_val = input_val * cf
        output = pow(((c1 + (c2 * pow(input_val, m1))) / (1 + (c3 * pow(input_val, m1)))), m2)
    return output


##
# Generate Reference Gamma with Scale Factor
def generate_ref_gamma_with_scale_factor(gamma_lut, r_factor=1, g_factor=1, b_factor=1):
    gamma_lut_scaled = []
    for index in range(0, len(gamma_lut)):
        gamma_lut_scaled.append(min((gamma_lut[index] * b_factor), 65535))
        gamma_lut_scaled.append(min((gamma_lut[index] * g_factor), 65535))
        gamma_lut_scaled.append(min((gamma_lut[index] * r_factor), 65535))
    return gamma_lut_scaled


##
# @brief generate_reference_pipe_gamma_lut() To multiply the Pixel Boost values with the Input Values and apply OETF 2084 on the Lut
# @param[in] -  lut_input_val - Static Input_Lut values created
# @param[in] -  pixel_boost - In case of eDP, pixel_boost value to be considered.
#                             For external panels, pixel_boost = 1.0
# @param[in] - os_relative_lut - Relative LUT given by OS
# @param[in] - num_of_samples -  No. of samples in relative LUT given by OS
def generate_reference_pipe_gamma_lut_with_pixel_boost(lut_input_val, pixel_boost, os_relative_lut, num_of_samples):
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []
    ##
    # Creating three separate LUTs for three channels from the OS relative LUT
    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(0, len(lut_input_val)):
        pixel_boosted_val = (lut_input_val[index] * pixel_boost) / 16777216
        base_val = oetf_2084(pixel_boosted_val)
        if base_val > 1.0:
            base_val = 1.0

        combined_val_b = apply_lut(blue_channel, 4096, base_val)
        combined_val_g = apply_lut(green_channel, 4096, base_val)
        combined_val_r = apply_lut(red_channel, 4096, base_val)

        convert_to_16_bit_b = min(round(65535.0 * combined_val_b), 65535)
        convert_to_16_bit_g = min(round(65535.0 * combined_val_g), 65535)
        convert_to_16_bit_r = min(round(65535.0 * combined_val_r), 65535)

        reference_pipe_gamma_lut.append(convert_to_16_bit_b)
        reference_pipe_gamma_lut.append(convert_to_16_bit_g)
        reference_pipe_gamma_lut.append(convert_to_16_bit_r)

    logging.debug("Reference HDR Gamma LUT")
    logging.debug(reference_pipe_gamma_lut)
    return reference_pipe_gamma_lut


##
# Utility to verify PipeGamma enable\disable
def verify_pipe_gamma_enable(platform, current_pipe):
    color_conv_blk = get_color_conversion_block(platform, current_pipe)
    gamma_reg_name = "GAMMA_MODE" + "_" + current_pipe
    gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_reg_name, platform)
    if color_conv_blk == "cc1":
        if gamma_mode_reg.post_csc_gamma_enable == 1:
            logging.info("PASS: Pipe Post CSC Gamma : Expected = ENABLE, Actual = ENABLE")
        else:
            logging.error("FAIL: Pipe Post CSC Gamma : Expected = ENABLE, Actual = DISABLE")
            return False
    else:
        if gamma_mode_reg.post_csc_cc2_gamma_enable == 1:
            logging.info("PASS: Pipe Post CSC CC2 Gamma  : Expected = ENABLE, Actual = ENABLE")
        else:
            logging.error("FAIL: Pipe Post CSC CC2 Gamma : Expected = ENABLE, Actual = DISABLE")
            return False
    return True


##
# Utility to get the gamma mode
def get_gamma_mode(current_pipe, platform):
    gamma_mode_reg_name = "GAMMA_MODE_" + current_pipe
    module_name = "GAMMA_MODE_REGISTER"
    instance = MMIORegister.get_instance(module_name, gamma_mode_reg_name, platform)
    gamma_mode_reg_offset = instance.offset
    gamma_mode_reg_value = driver_interface.DriverInterface().mmio_read(gamma_mode_reg_offset, 'gfx_0')
    gamma_mode = get_bit_value(gamma_mode_reg_value, 0, 1)
    if gamma_mode == 3:
        if platform in ("icllp", "ehl", "jsl", "lkf1" "tgl", "adls", "rkl", "dg1"):
            gamma_mode = "MULTI_SEGMENT"
        else:
            gamma_mode = "LOGARITHMIC"
    elif gamma_mode == 2:
        gamma_mode = "12BIT_GAMMA"

    return gamma_mode


##
# Utility to decode the gamma block for all three channels
def decode_gamma_data_block(hdr_gamma_data, lut_size):
    programmed_hdr_gamma_lut = []
    for index in range(0, lut_size, 2):
        ##
        # Decoding for Blue Channel
        lsb_for_blue = get_bit_value(hdr_gamma_data[index], 4, 9)
        msb_for_blue = get_bit_value(hdr_gamma_data[index + 1], 0, 9)
        blue_value = (msb_for_blue << 6) | lsb_for_blue
        programmed_hdr_gamma_lut.append(blue_value)

        ##
        # Decoding for Green Channel
        lsb_for_green = get_bit_value(hdr_gamma_data[index], 14, 19)
        msb_for_green = get_bit_value(hdr_gamma_data[index + 1], 10, 19)
        green_value = (msb_for_green << 6) | lsb_for_green
        programmed_hdr_gamma_lut.append(green_value)

        ##
        # Decoding for Red Channel
        lsb_for_red = get_bit_value(hdr_gamma_data[index], 24, 29)
        msb_for_red = get_bit_value(hdr_gamma_data[index + 1], 20, 29)
        red_value = (msb_for_red << 6) | lsb_for_red
        programmed_hdr_gamma_lut.append(red_value)

    return programmed_hdr_gamma_lut


##
# Fetch the MMIO_Values from the mmio block for Gamma
def fetch_hdr_gamma_mmio_data_from_etl(platform, current_pipe, multi_segment_support=False, is_smooth_brightness=False, step_index=0):
    mapping_seg_arr = {}
    mapping_data_arr = {}
    segment_1 = []
    segment_2_and_3 = []
    if platform in ("icllp", "ehl", "jsl"):
        if multi_segment_support:
            multi_seg_index_offset = get_register_offset("PAL_PREC_MULTI_SEG_INDEX_REGISTER", "PAL_PREC_MULTI_SEG_INDEX", current_pipe, platform)
            multi_seg_data_offset = get_register_offset("PAL_PREC_MULTI_SEG_DATA_REGISTER", "PAL_PREC_MULTI_SEG_DATA", current_pipe, platform)

            mmio_output_multi_seg_index = etl_parser.get_mmio_data(multi_seg_index_offset)
            mmio_output_multi_seg_data = etl_parser.get_mmio_data(multi_seg_data_offset)

            for seg_index in range(0, len(mmio_output_multi_seg_index)):
                index_in_seg_write = get_bit_value(mmio_output_multi_seg_index[seg_index].Data, 0, 4)
                mapping_seg_arr[index_in_seg_write] = mmio_output_multi_seg_data[seg_index].Data


            for index in range(len(mapping_seg_arr)):
                segment_1.append(mapping_seg_arr[index])

        pal_prec_index_offset = get_register_offset("PAL_PREC_INDEX_REGISTER","PAL_PREC_INDEX", current_pipe,platform)
        pal_prec_data_offset = get_register_offset("PAL_PREC_DATA_REGISTER","PAL_PREC_DATA", current_pipe,platform)
        mmio_output_pal_index = etl_parser.get_mmio_data(pal_prec_index_offset)
        mmio_output_pal_data = etl_parser.get_mmio_data(pal_prec_data_offset)

        for pal_index in range(0, len(mmio_output_pal_index)):
            index_in_pal_write = get_bit_value(mmio_output_pal_index[pal_index].Data, 0, 9)
            mapping_data_arr[index_in_pal_write] = mmio_output_pal_data[pal_index].Data

        for index in range(len(mapping_data_arr)):
            segment_2_and_3.append(mapping_data_arr[index])

    if platform in ("rkl", "dg1"):
        multi_seg_data_offset = get_register_offset("PAL_PREC_MULTI_SEG_DATA_REGISTER", "PAL_PREC_MULTI_SEG_DATA", current_pipe, platform)
        mmio_output_multi_seg_data = etl_parser.get_mmio_data(multi_seg_data_offset)

        gamma_dump_1 = [mmio_output_multi_seg_data[i * 18:(i + 1) * 18] for i in range((len(mmio_output_multi_seg_data) + 18 - 1) // 18)]
        if is_smooth_brightness:
            gamma_dump_1 = gamma_dump_1[step_index]
        else:
            gamma_dump_1 = gamma_dump_1[-1]

        for index in range(0, len(gamma_dump_1)):
            segment_1.append(gamma_dump_1[index].Data)

        pal_prec_data_offset = get_register_offset("PAL_PREC_DATA_REGISTER", "PAL_PREC_DATA",current_pipe, platform)
        mmio_output_pal_data = etl_parser.get_mmio_data(pal_prec_data_offset)

        gamma_dump_2_and_3 = [mmio_output_pal_data[i * 1024:(i + 1) * 1024] for i in range((len(mmio_output_pal_data) + 1024 - 1) // 1024)]
        if is_smooth_brightness:
            gamma_dump_2_and_3 = gamma_dump_2_and_3[step_index]
        else:
            gamma_dump_2_and_3 = gamma_dump_2_and_3[-1]

        for index in range(0, len(gamma_dump_2_and_3)):
            segment_2_and_3.append(gamma_dump_2_and_3[index].Data)

    if platform in ("dg2", "adlp", "adls", "mtl", "elg", "lnl"):
        post_csc_cc2_data_offset = get_register_offset("POST_CSC_CC2_DATA_REGISTER", "POST_CSC_CC2_DATA",
                                                                        current_pipe, platform)

        mmio_output_pal_cc2_data = etl_parser.get_mmio_data(post_csc_cc2_data_offset)
        gamma_dump_2_and_3 = [mmio_output_pal_cc2_data[i * 1020:(i + 1) * 1020] for i in range((len(mmio_output_pal_cc2_data) + 1020 - 1) // 1020)]
        if is_smooth_brightness:
            gamma_dump_2_and_3 = gamma_dump_2_and_3[step_index]
        else:
            gamma_dump_2_and_3 = gamma_dump_2_and_3[-1]
        for index in range(0, len(gamma_dump_2_and_3)):
            segment_2_and_3.append(gamma_dump_2_and_3[index].Data)

    ##
    # In case of Gen13 platforms, segment_1 will be emppty, since it is a logarithmic Lut and has only 1 segment
    gamma_lut = segment_1 + segment_2_and_3
    programmed_hdr_gamma_data = decode_gamma_data_block(gamma_lut, len(gamma_lut))
    return programmed_hdr_gamma_data


##
# Combine the multi segments fetched from the ETL to create the LUT of 524 samples
def combine_hdr_gamma_segments_from_etl(current_pipe, platform, gamma_lut, is_ext_registers_available=False):
    if is_ext_registers_available:
        reg_name = "PAL_GC_MAX_" + current_pipe
        pal_gc_max = MMIORegister.read("PAL_GC_MAX_REGISTER", reg_name, platform)
        gamma_lut.append(get_bit_value(pal_gc_max.asUint, 0, 16))
        gamma_lut.append(get_bit_value(pal_gc_max.asUint, 0, 16))
        gamma_lut.append(get_bit_value(pal_gc_max.asUint, 0, 16))

        reg_name = "PAL_EXT_GC_MAX_" + current_pipe
        pal_ext_gc_max = MMIORegister.read("PAL_EXT_GC_MAX_REGISTER", reg_name, platform)
        gamma_lut.append(get_bit_value(pal_ext_gc_max.asUint, 0, 18))
        gamma_lut.append(get_bit_value(pal_ext_gc_max.asUint, 0, 18))
        gamma_lut.append(get_bit_value(pal_ext_gc_max.asUint, 0, 18))

        reg_name = "PAL_EXT2_GC_MAX_" + current_pipe
        pal_ext2_gc_max = MMIORegister.read("PAL_EXT2_GC_MAX_REGISTER", reg_name, platform)
        gamma_lut.append(get_bit_value(pal_ext2_gc_max.asUint, 0, 18))
        gamma_lut.append(get_bit_value(pal_ext2_gc_max.asUint, 0, 18))
        gamma_lut.append(get_bit_value(pal_ext2_gc_max.asUint, 0, 18))

    logging.debug("Programmed Gamma LUT")
    logging.debug(gamma_lut)
    return gamma_lut


##
# Prepare the complete Gamma LUT by having the all three segments
def prepare_programmed_mmio_hdr_gamma_lut_from_etl(current_pipe, platform, is_smooth_brightness=False, step_index=0):
    gamma_data = []
    if platform in ("icllp", "ehl", "jsl", "rkl", "dg1"):
        programmed_gamma_data = fetch_hdr_gamma_mmio_data_from_etl(platform, current_pipe, multi_segment_support=True, is_smooth_brightness=is_smooth_brightness, step_index=step_index)
        gamma_data = combine_hdr_gamma_segments_from_etl(current_pipe, platform, programmed_gamma_data, is_ext_registers_available=True)

    if platform in ("dg2", "adlp", "adls", "mtl", "elg", "lnl"):
        gamma_data = fetch_hdr_gamma_mmio_data_from_etl(platform, current_pipe, is_smooth_brightness=is_smooth_brightness, step_index=step_index)
    return gamma_data


##
# Decoding the Gamma values from the ETL. The Gamma dump will be of the form (value, offset) pair.
def prepare_programmed_dsb_hdr_gamma_lut_from_etl(current_pipe, platform, dsb_gamma_lut):
    reg_read = MMIORegister()
    pal_prec_multi_seg_data_offset = None
    pal_prec_data_offset = None
    gamma_cc2_data_offset =None
    multi_seg_data = []
    pal_prec_data = []
    gamma_cc2_data = []
    if platform in ("tgl", "rkl", "adls"):
        reg_name_multi_seg = "PAL_PREC_MULTI_SEG_DATA" + '_' + current_pipe
        module_name_multi_seg = "PAL_PREC_MULTI_SEG_DATA_REGISTER"
        instance = reg_read.get_instance(module_name_multi_seg, reg_name_multi_seg, platform)
        pal_prec_multi_seg_data_offset = instance.offset

    if platform in ("tgl", "rkl", "adls"):
        reg_name_pal_prec = "PAL_PREC_DATA" + '_' + current_pipe
        module_name_pal_prec = "PAL_PREC_DATA_REGISTER"
        instance = reg_read.get_instance(module_name_pal_prec, reg_name_pal_prec, platform)
        pal_prec_data_offset = instance.offset
    else:
        reg_name_pal_prec = "POST_CSC_CC2_DATA" + '_' + current_pipe
        module_name_pal_prec = "POST_CSC_CC2_DATA_REGISTER"
        instance = reg_read.get_instance(module_name_pal_prec, reg_name_pal_prec, platform)
        gamma_cc2_data_offset = instance.offset

    decoded_gamma_lut = []
    for index in range(0, len(dsb_gamma_lut), 4):
        ##
        # In the ETL Parser, the byte array is converted as an Int array,
        # where each byte is stored within 4 bytes.
        # Only the 1st byte will have meaningful data,
        # hence extracting the LSB Byte and concatinating it to form a 32bit value
        val1 = dsb_gamma_lut[index] & 0xFF
        val2 = dsb_gamma_lut[index + 1] & 0xFF
        val3 = dsb_gamma_lut[index + 2] & 0xFF
        val4 = dsb_gamma_lut[index + 3] & 0xFF

        value = val4 << 24 | val3 << 16 | val2 << 8 | val1
        decoded_gamma_lut.append(value)

    ##
    # First two bytes dont have any Gamma data, hence ignoring it.
    for index in range(3, len(decoded_gamma_lut)):
        val = get_bit_value(decoded_gamma_lut[index], 0, 19)
        if platform in ("tgl", "rkl", "adls"):
            if val == pal_prec_multi_seg_data_offset:
                multi_seg_data.append(decoded_gamma_lut[index - 1])
            elif val == pal_prec_data_offset:
                pal_prec_data.append(decoded_gamma_lut[index - 1])
        else:
            if val == gamma_cc2_data_offset:
                gamma_cc2_data.append(decoded_gamma_lut[index - 1])

        index = index + 1
    if platform in ("tgl", "rkl", "adls"):
        programmed_multi_seg_gamma = decode_gamma_data_block(multi_seg_data, 18)
        programmed_pal_prec_gamma = decode_gamma_data_block(pal_prec_data, 1024)
        programmed_gamma_data = programmed_multi_seg_gamma + programmed_pal_prec_gamma
        programmed_gamma_lut = combine_hdr_gamma_segments_from_etl(current_pipe, platform, programmed_gamma_data, is_ext_registers_available=True)
    else:
        programmed_gamma_lut = decode_gamma_data_block(gamma_cc2_data, 1024)

    return programmed_gamma_lut


##
# Compare the reference and programmed data. If the difference is greater than 0, then the error percentage is calculated
# An error percentage of 0.005 is acceptable due to 16bit precision.
def compare_ref_and_programmed_gamma_lut(ref_pipe_gamma_lut, programmed_gamma_lut):
    logging.info("Reference Gamma {0}".format(ref_pipe_gamma_lut))
    logging.info("programmed_gamma_lut {0}".format(programmed_gamma_lut))
    for index in range(1, len(programmed_gamma_lut)):
        diff_value = abs(ref_pipe_gamma_lut[index] - programmed_gamma_lut[index])
        if diff_value > 0:
            error_percentage = (diff_value / ref_pipe_gamma_lut[index]) / 100
            if error_percentage > 0.005:
                logging.error("Error Percentage is %s @index %s; Expected_Value is %s; Programmed_Value is %s" %(error_percentage, index, ref_pipe_gamma_lut[index], programmed_gamma_lut[index]))
                return False
            else:
                logging.debug("Error Percentage is %s @index %s; Expected_Value is %s; Programmed_Value is %s" %(error_percentage, index, ref_pipe_gamma_lut[index], programmed_gamma_lut[index]))
    return True


##
# An interface which calls APIs to generate the reference and programmed data
# Also, invokes the API to compare the reference and programmed data
def fetch_ref_hdr_gamma_and_programmed_gamma_and_compare(platform, current_pipe, os_relative_lut, os_lut_size, pixel_boost=1, is_smooth_brightness=False, total_steps=1, step_index=0):
    sku_name = SystemInfo().get_sku_name("gfx_0")
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
    reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayFeatureControl")
    gamma_register_write_using_mmio = get_bit_value(reg_value, 22, 22)

    ref_pipe_gamma_lut = generate_reference_pipe_gamma_lut_with_pixel_boost(HDRConstants.INPUT_3SEGMENT_LUT_524Samples_8_24FORMAT, pixel_boost, os_relative_lut, os_lut_size)
    if sku_name != "RPLS":
        ##
        # Read from the Gamma registers from the ETL
        programmed_gamma_lut = []
        if gamma_register_write_using_mmio != 1:
            if platform in ("tgl", "rkl", "adls"):
                pipe_id = "PIPE_" + current_pipe
                gamma_dump = color_parse_etl_events.get_dsb_gamma_from_etl(pipe_id, is_smooth_brightness, total_steps, step_index)
                if gamma_dump is False:
                    return False
                programmed_gamma_lut = prepare_programmed_dsb_hdr_gamma_lut_from_etl(current_pipe, platform,
                                                                                                 gamma_dump)
        else:
            programmed_gamma_lut = prepare_programmed_mmio_hdr_gamma_lut_from_etl(current_pipe,platform, is_smooth_brightness, step_index)
        return compare_ref_and_programmed_gamma_lut(ref_pipe_gamma_lut, programmed_gamma_lut)
    else:
        # ReWrite HDR test have verification logic in gen_verify_pipe.Hence skipping verification
        # to duplication.
        return True


# @brief        Helper function to get device ID for passed display
# @return       returns the device ID
def get_device_id(display):
    config = display_config.DisplayConfiguration()
    device_id = 0
    dp_exists, hdmi_exists = False, False
    if display == "DP_A" or display == "MIPI_A":
        device_id = 4096
    elif display[:2] == "DP" and display != "DP_A":
        device_id = 256
    elif display[:4] == "HDMI":
        enumerated_displays = config.get_enumerated_display_info()
        for each_display in range(enumerated_displays.Count):
            if cfg_enum.CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[each_display].ConnectorNPortType).name[:2] == "DP" and \
                    cfg_enum.CONNECTOR_PORT_TYPE(
                        enumerated_displays.ConnectedDisplays[each_display].ConnectorNPortType).name != "DP_A":
                dp_exists = True
                break
        if dp_exists:
            device_id = 512
        else:
            device_id = 256
    return device_id


##
# @brief        Helper function to perform SRGB encoding
# @return       returns the lut values
def get_srgb_encoding(input_value):
    if input_value <= 0.0031308:
        output = input_value * 12.92
    else:
        output = (1.055 * pow(input_value, 1.0 / 2.4)) - 0.055
    return output


##
# @brief        Helper function to perform SRGB decoding
# @return       returns the lut values
def get_srgb_decoding(input_value):
    if input_value <= 0.04045:
        output = input_value / 12.92
    else:
        output = pow(((input_value + 0.055) / 1.055), 2.4)
    return output


##
# @brief        Helper function to generate SRGB encoded lut value for the input size
# @return       returns the lut values
def generate_srgb_encodinglut():
    output_lut = []
    lut_size = 131
    for i in range(0, lut_size):
        input_value = (i / (lut_size - 1))
        output_lut.append(get_srgb_encoding(input_value))
    return output_lut


##
# @brief        Helper function to generate SRGB decoded lut value for the input size
# @return       returns the lut values
def generate_srgb_decoding_lut(lut_size):
    output_lut = []
    for i in range(0, lut_size):
        input_value = (i / (lut_size - 1))
        bit_value = min(get_srgb_decoding(input_value) * 16777216, 16777216)
        output_lut.append(bit_value)
    return output_lut


##
# @brief set_bpc_registry() to set bpc value and if passed restart display driver
# @param[in] -  bpc - values as 8/10/12
def set_bpc_registry(bpc=8):
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
    bpc = int(bpc)
    if registry_access.write(args=reg_args, reg_name="SelectBPCFromRegistry",
                             reg_type=registry_access.RegDataType.DWORD, reg_value=bpc) is False:
        logging.error("Registry key add to enable SelectBPCFromRegistry failed")
    else:
        logging.info("Passed : Registry key add to enable SelectBPCFromRegistry")

    if registry_access.write(args=reg_args, reg_name="SelectBPC", reg_type=registry_access.RegDataType.DWORD,
                             reg_value=1) is False:
        logging.error("Registry key add to set SelectBPC failed")
    else:
        logging.info("Passed : Registry key add to set SelectBPC")

    status, reboot_required = display_essential.restart_gfx_driver()


##
# @brief clean_bpc_registry() to clear bpc value
def clean_bpc_registry():
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")

    if registry_access.delete(args=reg_args, reg_name="SelectBPCFromRegistry") is False:
        logging.error("failed to delete selectebpcfromregistry")

    if registry_access.delete(args=reg_args, reg_name="SelectBPC") is False:
        logging.error("failed to delete selectebpc registry")

##
# @brief clean_bpc_persistence_registry() to clear override persistence key
def clean_bpc_persistence_registry(target_id, pnpid):
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")

    registry_access.delete(args=reg_args, reg_name="OverrideOutputFormatPersistance_" + target_id + "_" + str(pnpid))


##
# @brief -VIDEO_DIP_DATA consists of set of offset range from 0x60220 to 0x6023F as VIDEO_DIP_AVI_DATA_A_* based on pipe A,B,C,D
#         For HDMI cases first four bytes will be header data type,version,checksum,avi length till 0x60223
#         From 0x60224 payload data will be programmed from 24 to 32 bits
# @param -pipe -current pipe info
def get_quantisation_range(platform, pipe):
    driver_interface_ = driver_interface.DriverInterface()

    base = MMIORegister.get_instance("VIDEO_DIP_AVI_HEADER_BYTE_REGISTER", "VIDEO_DIP_AVI_DATA_%s_0" % pipe, platform)
    offset = base.offset + 4
    reg_value = driver_interface_.mmio_read(offset, 'gfx_0')
    quantisation_range = get_bit_value(reg_value, 26, 27)
    return quantisation_range


# @brief        get_set_avi_info- Helper function to get and set the custom avi infoframe
# @param        enumerated_displays, display_index, avi_info, quant_range
# @return       returns status True/False and output
def get_set_avi_info(enumerated_displays, display_index, avi_info, quant_range):
    status = False
    quantisation_range = rgb_verification.RgbQuantisationRange

    ##
    # GET custom_avi_infoframe_args
    avi_info.TargetID = enumerated_displays.ConnectedDisplays[display_index].TargetID
    avi_info.Operation = AviInfoOperation.GET.value

    status, avi_info = driver_escape.get_set_quantisation_range(
        enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo, avi_info)
    if status:
        logging.info("Successfully get the avi_info through escape")
    else:
        return "Failed to get the avi_info", status

    ##
    # SET Quantisation range
    avi_info.AVIInfoFrame.QuantRange = quant_range
    avi_info.Operation = AviInfoOperation.SET.value

    status, avi_info = driver_escape.get_set_quantisation_range(enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,avi_info)
    if status:
        return "Successfully set the quantisation range: %s through escape" % quantisation_range(quant_range).name, status
    else:
        return "Failed set the quantisation range: %s through escape" % quantisation_range(quant_range).name, status


# @brief        verify_quantisation_range_and_ocsc - Helper function to verify quant_range,
#               ocsc,ocsc coeff and pre/post off#
# @return       returns the status True/False and output
def verify_quantisation_range_and_ocsc(platform, pipe, bpc, set_range, expected_range, conv_type, input="RGB", output="RGB"):
    status = False
    quantisation_range = rgb_verification.RgbQuantisationRange
    dip_quant_range = get_quantisation_range(platform,pipe)

    if dip_quant_range == expected_range:

        logging.info("Pass: Applied quantisation range through escape ->{0} and driver programmed quantisation range ->{1}".format(quantisation_range(set_range).name,quantisation_range(dip_quant_range).name))
        ##
        # Verify Output_csc status enable/disable
        csc_reg_name = "CSC_MODE" + "_" + pipe
        csc_mode_reg = MMIORegister.read("CSC_MODE_REGISTER", csc_reg_name, platform)

        if csc_mode_reg.pipe_output_csc_enable == 1:
            logging.info("Pass: In {0} range, Output csc status Expected:Enable and Actual:Enable".format(quantisation_range(dip_quant_range).name))

            ##
            # Verify oCSC coeff
            if output_csc_coeff_verfication(platform, pipe, bpc, input, output,conv_type) is False:
                return "Programmed oCSC coeff not matching with ref_off", status
            ##
            # Verify oCSC post-off
            if csc_pre_or_post_off_verification(platform, pipe, bpc, input, output, conv_type, "OUTPUT_CSC_POSTOFF_REGISTER", "OUTPUT_CSC_POSTOFF") is False:
                return "Programmed oCSC Post off not matching with ref_off", status
            ##
            # Verify oCSC pre-off
            if csc_pre_or_post_off_verification(platform, pipe, bpc, input, output, conv_type, "OUTPUT_CSC_PREOFF_REGISTER", "OUTPUT_CSC_PREOFF") is False:
                return "Programmed oCSC pre off not matching with ref_off", status
            status = True
            return "Passed: Verification of quantisation range and output csc", status
        else:
            status = True
            return "Pass: In %s range, Output csc status Expected:Disable and Actual: Disable" % quantisation_range(dip_quant_range).name, status

    else:
        logging.error("Fail: Quantisation_range Mismatch  Excepted: %s and Actual %s" % (quantisation_range(expected_range).name, quantisation_range(dip_quant_range).name))
        return "Quantisation_range got Mismatch", status


def gdhm_report_app_color(title="[COLOR]bug", component= gdhm.Component.Driver.DISPLAY_OS_FEATURES, problem_classification = gdhm.ProblemClassification.FUNCTIONALITY, priority=gdhm.Priority.P2, exposure=gdhm.Exposure.E2):
    gdhm.report_bug(
        title=title,
        problem_classification= problem_classification,
        component=component,
        priority=priority,
        exposure=exposure
    )
