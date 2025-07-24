########################################################################################################################
# @file             framebuffer_verification.py
# @brief            Estimates the accuracy for graphics post processing pipeline
# @details          The program is used to compare hardware and software generated images.
# @author           Patel, Ankurkumar G
########################################################################################################################
import ctypes
import importlib
import itertools
import json
import logging
import math
import os
import shutil
import subprocess
import time
from collections import defaultdict
from configparser import ConfigParser

import win32api

from Libs.Core import enum, driver_escape
from Libs.Core import registry_access
from Libs.Core import system_utility
from Libs.Core import window_helper
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_struct as cfg_struct
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import driver_escape_args
from Tests.Color import color_common_utility
from registers.mmioregister import MMIORegister

__CAPTURE_INSTANCE = 0
__MAX_PIPE = 3
__REGISTRY_KEY = 'framecaptureinst'
dict_wd_input_select = defaultdict(lambda: "Invalid Value",
                                   {'0b0': "Pipe A", '0b101': "Pipe B", '0b110': "Pipe C", '0b111': "Pipe D"})
valid_capture_methods = ["WRITEBACK", "plane_processing"]
reg_read = MMIORegister()
INPUT_JSON = "input.json"
INPUT_SW_JSON = "SwConfig.json"
INPUT_HW_JSON = "HwConfig.json"
DIRECTORY_NAME = None
TARGET_ID = None
flattened_dict = {}


##
# @brief          COMPARISION_RECT Structure
# @details        Class to get the co-ordinates of the rectangular area
class COMPARISION_RECT(ctypes.Structure):
    _fields_ = [('origin_x', ctypes.c_long),
                ('origin_y', ctypes.c_long),
                ('width', ctypes.c_long),
                ('height', ctypes.c_long)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.origin_x = 0
        self.origin_y = 0
        self.width = 0
        self.height = 0

    ##
    # @brief        Constructor
    # @param[in]    origin_x - Origin point x-Coordinate
    # @param[in]    origin_y - Origin point y-Coordinate
    # @param[in]    width - width of the screen to be captured
    # @param[in]    height - height of the screen to be captured
    def __init__(self, origin_x, origin_y, width, height):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.width = width
        self.height = height


##
# @brief        function to get the details about platform
# @param[in]    gfx_index - Graphics Adapter Index
# @return       None
def __update_platform_details(gfx_index):
    global PLATFORM
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    PLATFORM = adapter_info.get_platform_info().PlatformName.lower()


##
# @brief        function to perform initialize and cleanup
# @param[in]    argument - action to be performed (initialize or cleanup)
# @return       None
def initialize_and_cleanup(argument):
    if argument == "initialize":
        global __CAPTURE_INSTANCE
        global __MAX_PIPE
        gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()
        logging.debug("gfx_adapter_details_dict{}".format(gfx_adapter_details_dict))
        for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():
            is_ddrw = system_utility.SystemUtility().is_ddrw(gfx_index)
            reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
            reg_value, _ = registry_access.read(args=reg_args, reg_name=__REGISTRY_KEY)
            if reg_value is None:
                registry_access.write(args=reg_args, reg_name=__REGISTRY_KEY,
                                      reg_type=registry_access.RegDataType.DWORD,
                                      reg_value=__CAPTURE_INSTANCE)
            else:
                __CAPTURE_INSTANCE = reg_value

    elif argument == "cleanup":
        time.sleep(5)
        gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()
        for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():
            is_ddrw = system_utility.SystemUtility().is_ddrw(gfx_index)
            reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
            registry_access.delete(args=reg_args, reg_name=__REGISTRY_KEY)

    else:
        logging.info("Invalid argument passed")


##
# @brief        function to get directory given platform name
# @param[in]    platform - platform name
# @return       str - directory name
def __get_directory_based_on_platform(platform):
    platform = platform.upper()
    if platform in ['ICLLP', 'JSL', 'EHL', 'LKF1']:
        return "D11"

    if platform in ['TGL', 'DG1', 'RKL', 'ADLS']:
        return "D12"

    if platform in ['DG2', 'ADLP']:
        return "D13"

    if platform in ['DG3', 'MTL', 'ELG']:
        return "D14"

    if platform in ['LNL', 'PTL', 'NVL', 'CLS']:
        return "D15"


##
# @brief        function to get the directory details from where input json need to be read
# @return       directory_path - Framebuffer verification directory path
def __update_directory_details():
    global PLATFORM
    DIRECTORY_NAME = __get_directory_based_on_platform(PLATFORM)
    directory_path = os.path.join(test_context.ROOT_FOLDER, "Libs\\Core\\Verifier\\framebuffer_verification\\DE\\",
                                  DIRECTORY_NAME)
    return directory_path


##
# @brief        function to set desktop
# @param[in]    wallpaper_image_path - wallpaper image file path
# @return       None
def __set_desktop(wallpaper_image_path):
    SPI_SETDESKWALLPAPER = 20
    path = os.path.join(test_context.TEST_STORE_FOLDER, wallpaper_image_path)  # "ExtDependency\\image\\image_1.jpeg"
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


##
# @brief        function to prepare desktop background
# @param[in]    wallpaper_image_path - wallpaper image file path
# @return       None
def __prepare_desktop_background(wallpaper_image_path):
    __set_desktop(wallpaper_image_path)
    window_helper.minimize_all_windows()
    time.sleep(5)
    window_helper.toggle_task_bar(window_helper.Visibility.HIDE)


##
# @brief        function to move the mouse  pointer to right bottom of the screen
# @param[in]    target_id - target ID of a panel
# @return       bool - True if cursor set to right bottom, False otherwise
def __move_cursor_to_right_bottom(target_id):
    disp_cfg = display_config.DisplayConfiguration()
    current_wb_mode = disp_cfg.get_current_mode(target_id)

    if current_wb_mode is None:
        return False

    logging.debug("  HzRes               : {}".format(current_wb_mode.HzRes))
    logging.debug("  VtRes               : {}".format(current_wb_mode.VtRes))

    win32api.SetCursorPos(((current_wb_mode.HzRes + 1), (current_wb_mode.VtRes + 1)))
    time.sleep(2)
    return True


##
# @brief        function to capture image on screen
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       bool -  True if source image is captured, False otherwise
def __capture_src_image(display_and_adapter_info):
    global current_wb_mode
    disp_cfg = display_config.DisplayConfiguration()
    current_wb_mode = disp_cfg.get_current_mode(display_and_adapter_info)
    screen_args = cfg_struct.ScreenCaptureArgs()
    screen_args.HzRes = current_wb_mode.HzRes
    screen_args.VtRes = current_wb_mode.VtRes
    screen_args.BPP = current_wb_mode.BPP
    status = disp_cfg.capture_screen(__CAPTURE_INSTANCE, 'gfx_0', screen_args)
    if status == 0:
        logging.error('Failed to capture source image')
        return False
    return True


##
# @brief        function to update capture instance
# @param[in]    gfx_index - Graphics Adapter Index
# @return       None
def __update_capture_instane(gfx_index):
    global __CAPTURE_INSTANCE
    __CAPTURE_INSTANCE += 1
    reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
    registry_access.write(args=reg_args, reg_name=__REGISTRY_KEY, reg_type=registry_access.RegDataType.DWORD,
                          reg_value=__CAPTURE_INSTANCE)


##
# @brief        gets the BPC value of image
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    transcoder_number - Transcoder number
# @return       modest_bpc - BPC value(8 or 10), False if current modeset is not supported
def __get_image_bpc(gfx_index, transcoder_number):
    reg_read = MMIORegister()
    wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % (PLATFORM))
    wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(transcoder_number)
    wd_trans_ctl_reg_value = reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, PLATFORM, 0x0, gfx_index)
    element_value = wd_trans_ctl_reg_value.__getattribute__(str("wd_color_mode"))
    if str(element_value) == "6":
        modeset_bpc = 10
    elif str(element_value) == "3":
        modeset_bpc = 8
    else:
        logging.debug("FAIL: Writeback devices does not support the current modeset")
        return False
    return modeset_bpc


##
# @brief        function to capture writeback image
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    target_id - target ID of writeback device
# @return       bool - True if destination image is captured, False otherwise
def __capture_writeback_image(gfx_index, target_id):
    global __CAPTURE_INSTANCE
    wb_buffer_info = driver_escape_args.WbBufferInfo()
    transcoder_number = __get_sink_index_from_target_id(target_id)
    image_bpc = __get_image_bpc(gfx_index, transcoder_number)
    start_time = time.time()
    result, wb_buffer_info = driver_escape.dump_wb_buffer(target_id, __CAPTURE_INSTANCE, wb_buffer_info, image_bpc)
    end_time = time.time()
    if result is False:
        logging.error('Failed to capture destination buffer')
        return False

    logging.debug("Start time for writeback image capture =" + str(start_time))
    logging.debug("End time for writeback image capture =" + str(end_time))
    final_time = end_time - start_time
    logging.debug("Total time for capture writeback image =" + str(final_time))

    __update_capture_instane(gfx_index)
    return True


##
# @brief        function to verify whether the target_id is valid or not
# @param[in]    target_id;
# @return       bool - True if writeback device value is b in hex, False otherwise
def __is_valid_wd_target_id(target_id):
    hex_value = hex(target_id)
    writeback_device_value = hex_value[-1]
    if writeback_device_value == "b":  # target_id converted into hex and then extracted the first 4 bits from LSB
        return True
    else:
        return False


##
# @brief        function to compare hardware and software generated images
# @param[in]    hw_image - path to hardware generated image
# @param[in]    sw_image - path to software generated image
# @param[in]    comparision_rect - structure for co-ordinates
# @param[in]    tolerance - tolerance level
# @return       count_of_pixels_not_matching - number of pixels that are not matching,
#               None if Image size or mode mismatch occurs
def __compare_hw_sw_image(hw_image, sw_image, comparision_rect, tolerance):
    from PIL import Image
    hw_image = Image.open(hw_image).convert("RGB")
    sw_image = Image.open(sw_image)
    if hw_image.size == sw_image.size and hw_image.mode == sw_image.mode:
        count_of_pixels_not_matching = 0
        for i in range(comparision_rect.origin_x, comparision_rect.width):
            for j in range(comparision_rect.origin_y, comparision_rect.height):
                pixel1 = hw_image.getpixel((i, j))
                pixel2 = sw_image.getpixel((i, j))
                diff_value = tuple(abs(x - y) for x, y in zip(pixel1, pixel2))
                if diff_value > (tolerance, tolerance, tolerance):
                    count_of_pixels_not_matching += 1
        return count_of_pixels_not_matching
    else:
        logging.error("ERROR:Images size or mode is not matching")


##
# @brief        function to get path of hardware and software images
# @return       (hw_image, sw_image) - (hardware image path, software image path)
def __get_path_of_sw_and_hw_images():
    global __CAPTURE_INSTANCE
    images_list = []
    dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
    path_to_dir = os.path.join(test_context.LOG_FOLDER, dir_name)
    for image in os.listdir(path_to_dir):
        if image.endswith('.png') and "Src_Frame" not in image:
            images_list.append(image)
    for i in range(0, len(images_list)):
        file_name, file_extension = os.path.splitext(images_list[i])
        if file_name.startswith("WB"):
            hw_image = os.path.join(path_to_dir, images_list[i])
        else:
            sw_image = os.path.join(path_to_dir, images_list[i])
    return hw_image, sw_image


##
# @brief        moves files to their respective capture instance folder
# @return       None
def __move_files_to_respective_folder():
    global __CAPTURE_INSTANCE
    dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
    path = os.path.join(test_context.LOG_FOLDER, dir_name)
    for image in os.listdir(test_context.LOG_FOLDER):
        if image.endswith('.png'):
            file_name, file_extension = os.path.splitext(image)

            if file_name[-1] == str(__CAPTURE_INSTANCE - 1):
                logging.debug("file_name{}".format(file_name))
                shutil.move(os.path.join(test_context.LOG_FOLDER, image), path)
            else:
                pass
        if image.endswith('.json'):
            logging.debug("file_name{}".format(file_name))
            shutil.move(os.path.join(test_context.LOG_FOLDER, image), path)


##
# @brief        function to verify
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    target_id - target ID of writeback device
# @param[in]    comparision_rect - COMPARISION_RECT Object
# @param[in]    tolerance - tolerance level
# @param[in]    planes_image_list - list of plane images
# @return       bool - True if framebuffer test is passed or images are matching, False otherwise
def verify(gfx_index, target_id, comparision_rect, tolerance, planes_image_list=None):
    logging.info("Verify called")
    global __MAX_PIPE
    global TARGET_ID
    global INPUT_SW_JSON
    is_dft = False
    status = False
    capture_method = None
    _configParser = ConfigParser()
    hw_image_capture_type = "WRITEBACK"
    if os.path.exists(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini")):
        _configParser.read(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini"))
        if _configParser.has_option('GENERAL', 'hw_image_capture_type'):
            capture_method = _configParser.get('GENERAL', 'hw_image_capture_type')

    disp_cfg = display_config.DisplayConfiguration()

    logging.debug('TargetID:{}'.format(target_id))

    TARGET_ID = target_id

    if planes_image_list:
        is_dft = True

    if not __move_cursor_to_right_bottom(target_id):
        logging.error('FAIL: The cursor is not moved to right bottom')
        return False

    display_and_adapter_info = disp_cfg.get_display_and_adapter_info(target_id)

    start_time = time.time()
    if is_dft is False:
        if not (__capture_src_image(display_and_adapter_info)):
            logging.error('FAIL: The source image capture failed')
            return status

    __update_platform_details(gfx_index)

    if capture_method == "WRITEBACK":
        status = __is_valid_wd_target_id(target_id)
        if status is False:
            logging.error('FAIL: The target id is not valid for writeback device ')
            return status
        __capture_writeback_image(gfx_index, target_id)
    else:
        logging.debug("Invalid Capture Method Selected %s".format(capture_method))
        return False

    directory_path = __update_directory_details()
    __parse_input_json(gfx_index, os.path.join(directory_path, INPUT_JSON))
    __move_files_to_respective_folder()

    dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
    path_to_dir = os.path.join(test_context.LOG_FOLDER, dir_name)
    INPUT_SW_JSON = os.path.join(path_to_dir, INPUT_SW_JSON)

    __generate_dves_output_image_from_json(INPUT_SW_JSON, INPUT_HW_JSON)

    end_time = time.time()
    logging.debug("Start time for capture = " + str(start_time))
    logging.debug("End time for capture = " + str(end_time))
    final_time = end_time - start_time
    logging.debug("Total time for capture hardware and software images = " + str(final_time))

    hw_image, sw_image = __get_path_of_sw_and_hw_images()
    count_of_mismatching_pixel = __compare_hw_sw_image(hw_image, sw_image, comparision_rect, tolerance)

    if count_of_mismatching_pixel > 0:
        logging.error("count_of_mismatching_pixel:{}".format(count_of_mismatching_pixel))
        logging.error("FAIL: Framebuffer Verification Failed")
        return False
    logging.debug("count_of_mismatching_pixel:{}".format(count_of_mismatching_pixel))
    logging.info("PASS: Framebuffer Verification Passed")
    return True


##
# @brief        gets the connected pipe name
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    target_id - Target ID of writeback device
# @return       dict - name of the pipe(A or B or C or D)
def __get_connected_pipe_for_wd_transcoder(gfx_index, target_id):
    transcoder_number = __get_sink_index_from_target_id(target_id)
    reg_read = MMIORegister()
    wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % (PLATFORM))
    wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(transcoder_number)
    wd_trans_ctl_reg_value = reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, PLATFORM, 0x0, gfx_index)

    return dict_wd_input_select[bin(wd_trans_ctl_reg_value.__getattribute__("wd_input_select"))][-1]


##
# @brief        generates the output image from the input json
# @param[in]    input_sw_json - the json file generated by software
# @param[in]    input_hw_json - the json file generated by hardware
# @return       None
def __generate_dves_output_image_from_json(input_sw_json, input_hw_json):
    global __CAPTURE_INSTANCE
    dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
    path_to_dir = os.path.join(test_context.LOG_FOLDER, dir_name)
    sw_json_path = os.path.join(path_to_dir, input_sw_json)
    directory_path = __update_directory_details()
    hw_json_path = os.path.join(directory_path, input_hw_json)
    dves_exe = os.path.join(test_context.COMMON_BIN_FOLDER, "DVESBackend.exe")
    start_time = time.time()
    install_process = subprocess.call([dves_exe, hw_json_path, sw_json_path])
    end_time = time.time()
    logging.debug("Start time for generating dves output image from json =" + str(start_time))
    logging.debug("End time for generating dves output image from json =" + str(end_time))
    final_time = end_time - start_time
    logging.debug("Total time for generating dves output image from json=" + str(final_time))


##
# @brief        function to read the input json
# @param[in]    input_json - path to input json
# @return       input_json_data - json data from input json
def __read_input_json(input_json):
    input_json_file = open(input_json, "r")
    input_json_data = json.load(input_json_file)

    return input_json_data


##
# @brief        function to flatten the dictionary
# @brief        element - pythonic element
# @param[in]    parent - parent json key
# @param[in]    sep - separator identifier
# @return       flattened_dict - json parsed to dictionary
def __flatten_input_json_dict(element, parent_key="", sep="/"):
    if isinstance(element, list):
        for i in range(len(element)):
            __flatten_input_json_dict(element[i], parent_key + sep + str(i) if parent_key else str(i))
    elif isinstance(element, dict):
        for key, value in element.items():
            __flatten_input_json_dict(value, parent_key + sep + key if parent_key else key)
    else:
        flattened_dict[parent_key] = element

    return flattened_dict


##
# @brief        function to iterate through json and collect unique keys
# @param[in]    input_dict - flattened dictionary
# @return       (filtered_list, filtered_list_input_output) - (list of unique keys, list of input output)
def __iterate_through_dict(input_dict):
    filtered_list = []
    filtered_list_input_output = []
    for key, value in input_dict.items():
        if "reg_name" in key or "bit_field" in key or "data_type" in key:
            filtered_list.append(key)

        if "input" in key or "output" in key:
            filtered_list_input_output.append(key)

    return filtered_list, filtered_list_input_output


##
# @brief        function to create json path
# @param[in]    txt - flattened dictionary
# @return       element_path - element path
def __create_path_from_flatten_dict(txt):
    element_path = ""

    element_list = txt.split('/')

    for each_element in element_list:
        if type(each_element) == type(str()) and len(each_element) > 1 and not str(each_element).isnumeric():
            each_element = '"{}"'.format(each_element)
            each_value = "[{}]".format(each_element)
            element_path += each_value
        else:
            each_element = int(each_element)
            each_value = "[{}]".format(each_element)
            element_path += each_value

    return element_path


##
# @brief        function to convert datatype in string to actual datatype
# @param[in]    data_type_in_str - datatype in string
# @return       any - datatype
def __str_to_datatype(data_type_in_str):
    if data_type_in_str == "bool":
        return bool
    elif data_type_in_str == "float":
        return float
    else:
        return int


##
# @brief        function to convert datatype in string to actual datatype
# @param[in]    value - CSC coefficient value
# @param[in]    start - start position of the bit
# @param[in]    end - end position of the bit
# @return       retvalue - return value
def GetValue(value, start, end):
    retvalue = value << (31 - end) & 0xffffffff
    retvalue = retvalue >> (31 - end + start) & 0xffffffff
    return retvalue


##
# @brief        function to convert CSC register format to coefficient
# @param[in]    cscCoeff - CSC Coefficient value
# @return       outVal - output value
def convert_CSC_RegFormat_to_Coeff(cscCoeff):
    outVal = 0.0
    scale_factor = 0.0

    signBit = None
    exponent = None
    mantissa = None

    positionOfPointFromRight = 0

    signBit = GetValue(cscCoeff, 15, 15)
    exponent = GetValue(cscCoeff, 12, 14)
    mantissa = int(GetValue(cscCoeff, 3, 11))

    if (exponent == 6):
        positionOfPointFromRight = 7
    elif (exponent == 7):
        positionOfPointFromRight = 8
    elif (exponent == 0):
        positionOfPointFromRight = 9
    elif (exponent == 1):
        positionOfPointFromRight = 10
    elif (exponent == 2):
        positionOfPointFromRight = 11
    elif (exponent == 3):
        positionOfPointFromRight = 12

    scale_factor = math.pow(2.0, float(positionOfPointFromRight))
    outVal = float(mantissa) / scale_factor
    if (signBit == 1):
        outVal = outVal * -1

    return outVal


##
# @brief        To get CSC-Coefficient matrix from register
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    unit_name - register name
# @param[in]    str -  current PIPE name (plane_pipe or pipe)
# @return       csc_coeff - coefficient matrix
def getCSCCoeffMatrixFromReg(gfx_index, unit_name, str):
    programmed_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    csc_coeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    register_file = importlib.import_module("registers." + PLATFORM + "." + (unit_name) + "_" + "REGISTER")
    reg = unit_name + '_' + str
    register_read_value = reg_read.read((unit_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
    base_offset = register_read_value.offset
    for i in range(0, 3):
        offset = (base_offset + i * 8)  # 2 DWORDS for each row RGB
        reg_val = driver_interface.DriverInterface().mmio_read(offset, gfx_index)
        csc_reg = reg_read.get_instance((unit_name) + "_" + "REGISTER", reg, PLATFORM, reg_val)
        programmed_val[i][0] = csc_reg.coeff1
        programmed_val[i][1] = csc_reg.coeff2
        reg_val = driver_interface.DriverInterface().mmio_read(offset + 4, gfx_index)
        csc_reg = reg_read.get_instance((unit_name) + "_" + "REGISTER", reg, PLATFORM, reg_val)
        programmed_val[i][2] = csc_reg.coeff1

    for i in range(0, 3):
        for j in range(0, 3):
            csc_coeff[i][j] = convert_CSC_RegFormat_to_Coeff(programmed_val[i][j])
    return csc_coeff


##
# @brief        To get gammaLUT values from register
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    unit_name - register name
# @param[in]    no_samples - number of samples required
# @param[in]    str - current PIPE name (plane_pipe or pipe)
# @return       lut_data - coefficient matrix
def getGammLUTFromReg(gfx_index, unit_name, no_samples, str):
    lut_data = []
    # Setting auto increment bit to 1 in index register
    module_name = unit_name + "_INDEX_REGISTER"
    reg_name = unit_name + "_INDEX_" + str
    instance = reg_read.get_instance(module_name, reg_name, PLATFORM)
    index_offset = instance.offset
    index_reg = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
    index_reg.index_auto_increment = 1
    driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)

    module_name1 = unit_name + "_INDEX_REGISTER"
    reg_name1 = unit_name + "_INDEX_" + str
    module_name = unit_name + "_DATA_REGISTER"
    reg_name = unit_name + "_DATA_" + str

    for index in range(0, no_samples):
        index_reg.index_value = index
        driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)
        index_reg = reg_read.read(module_name1, reg_name1, PLATFORM, 0x0, gfx_index)
        data_reg = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
        lut_data.append(data_reg.gamma_value)
        lut_data.sort()
    return lut_data


##
# @brief        function to get pipe gammaLUT from register
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    gamma_mode - MULTI_SEGMENT or 12BIT_GAMMA mode
# @param[in]    str_pipe - current pipe name (plane pipe or pipe - A or B or C or D)
# @return       lut_data - lut values
def getPipeGammaLUTFromReg(gfx_index, gamma_mode, str_pipe):
    reg_read = MMIORegister()
    lut_data = []
    red_lut_data = []
    green_lut_data = []
    blue_lut_data = []
    index_reg = None
    index_offset = 0
    if (gamma_mode == "MULTI_SEGMENT"):
        module_name = "PAL_PREC_MULTI_SEG_INDEX_REGISTER"
        reg_name = "PAL_PREC_MULTI_SEG_INDEX_" + str_pipe
        instance = reg_read.get_instance(module_name, reg_name, PLATFORM)
        index_offset = instance.offset
        index_reg = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
        index_reg.index_auto_increment = 1
        driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)

        # MultiSegment Palette Prec Data
        module_name = "PAL_PREC_MULTI_SEG_DATA_REGISTER"
        reg_name = "PAL_PREC_MULTI_SEG_DATA_" + str_pipe
        for index in range(0, 18, 2):
            index_reg.index_value = index
            driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)
            data_reg1 = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
            data_reg2 = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)

            lsb_blue = GetValue(data_reg1.asUint, 4, 9)
            msb_blue = GetValue(data_reg2.asUint, 0, 9)
            blue_value = (msb_blue << 6 & 0xffff) + lsb_blue
            blue_lut_data.append(blue_value)

            lsb_green = GetValue(data_reg1.asUint, 14, 19)
            msb_green = GetValue(data_reg2.asUint, 10, 19)
            green_value = (msb_green << 6 & 0xffff) + lsb_green
            green_lut_data.append(green_value)

            lsb_red = GetValue(data_reg1.asUint, 24, 29)
            msb_red = GetValue(data_reg2.asUint, 20, 29)
            red_value = (msb_red << 6 & 0xffff) + lsb_red
            red_lut_data.append(red_value)

    # Palette Prec Data
    module_name = "PAL_PREC_INDEX_REGISTER"
    reg_name = "PAL_PREC_INDEX_" + str_pipe
    instance = reg_read.get_instance(module_name, reg_name, PLATFORM)
    index_offset = instance.offset
    index_reg = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
    index_reg.index_auto_increment = 1
    driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)

    module_name = "PAL_PREC_DATA_REGISTER"
    reg_name = "PAL_PREC_DATA_" + str_pipe

    for index in range(0, 1024, 2):
        index_reg.index_value = index
        driver_interface.DriverInterface().mmio_write(index_offset, index_reg.asUint, gfx_index)
        data_reg1 = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)
        data_reg2 = reg_read.read(module_name, reg_name, PLATFORM, 0x0, gfx_index)

        lsb_red = GetValue(data_reg1.asUint, 24, 29)
        msb_red = GetValue(data_reg2.asUint, 20, 29)
        red_value = (msb_red << 6 & 0xffff) + lsb_red
        red_lut_data.append(red_value)

        lsb_green = GetValue(data_reg1.asUint, 14, 19)
        msb_green = GetValue(data_reg2.asUint, 10, 19)
        green_value = (msb_green << 6 & 0xffff) + lsb_green
        green_lut_data.append(green_value)

        lsb_blue = GetValue(data_reg1.asUint, 4, 9)
        msb_blue = GetValue(data_reg2.asUint, 0, 9)
        blue_value = (msb_blue << 6 & 0xffff) + lsb_blue
        blue_lut_data.append(blue_value)

    reg_name = "PAL_GC_MAX_" + str_pipe
    pal_gc_max_red = reg_read.read("PAL_GC_MAX_REGISTER", reg_name, PLATFORM, 0x0, gfx_index)
    red_lut_data.append(GetValue(pal_gc_max_red.asUint, 0, 31))
    pal_gc_max_green = reg_read.read("PAL_GC_MAX_REGISTER", reg_name, PLATFORM, 0x4, gfx_index)
    green_lut_data.append(GetValue(pal_gc_max_green.asUint, 0, 31))
    pal_gc_max_blue = reg_read.read("PAL_GC_MAX_REGISTER", reg_name, PLATFORM, 0x8, gfx_index)
    blue_lut_data.append(GetValue(pal_gc_max_blue.asUint, 0, 31))

    lut_data = red_lut_data + green_lut_data + blue_lut_data
    return lut_data


##
# @brief        function to get sink index from target id
# @param[in]    target_id - Target ID of device
# @return       hex_value - a single character that tells which transcoder is enabled
def __get_sink_index_from_target_id(target_id):
    hex_value = hex(target_id)
    return hex_value[-3]  # target_id converted into hex and then extracted the 8-12 bits from LSB


##
# @brief        function to read register values
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    reg_name - Registry Name
# @param[in]    bit_field - bit field to be read
# @param[in]    current_pipe - current PIPE name (plane pipe or pipe)
# @return       element_value - True if register read is successful, False otherwise
def __get_element_value(gfx_index, reg_name, bit_field, current_pipe):
    if reg_name[-1].isnumeric():
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name[:-1]) + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
    else:
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name) + "_" + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)

    element_value = register_read_value.__getattribute__(str(bit_field))
    return element_value


##
# @brief        function to convert datatype in string to datatype
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    reg_name - MMIO register Name
# @param[in]    bit_field - bit field to be read
# @param[in]    data_type - Register data type
# @return       any - Returns register value if read successful, False otherwise
def __read_register_from_json_data(gfx_index, reg_name, bit_field, data_type):
    reg_read = MMIORegister()
    global TARGET_ID
    current_pipe = __get_connected_pipe_for_wd_transcoder(gfx_index, TARGET_ID)

    if ("LUT_3D_CTL_REGISTER" == reg_name or "DPLC_CTL" == reg_name or "DPST_CTL" == reg_name):
        return
    # @ Todo : register have hardcoded values for agressiveness and laceLuxvalue, also these registers are
    #          not enabled currently, hence just returning null values for these registers.

    # to get data for pipe_modeSetBpc
    if "TRANS_WD_FUNC_CTL" in reg_name:
        register_file = importlib.import_module("registers." + PLATFORM + "." + "TRANS_WD_FUNC_CTL_REGISTER")
        reg = reg_name + "_" + __get_sink_index_from_target_id(TARGET_ID)
        register_read_value = reg_read.read("TRANS_WD_FUNC_CTL_REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_value = register_read_value.__getattribute__(str(bit_field))
        if str(element_value) == "6":
            modeset_bpc = 10
        elif str(element_value) == "3":
            modeset_bpc = 8
        else:
            logging.debug("FAIL: Writeback devices does not support the current modeset")
            return False
        return modeset_bpc

    # To get widthBeforeScaling,widthAfterScaling
    if "get_current_mode" in reg_name and "HzRes" in bit_field:
        return current_wb_mode.HzRes

    # To get heightBeforeScaling,HeightAfterScaling
    if "get_current_mode" in reg_name and "VtRes" in bit_field:
        return current_wb_mode.VtRes

    # To get plane pre csc gamma enable bit
    if "PLANE_COLOR_CTL_" in reg_name and "plane_pre_csc_gamma_enable" in bit_field:
        element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
        return __str_to_datatype(data_type)(element_value)

    # to get planeprecscLut data
    if "PLANE_PRE_CSC_GAMC_DATA" in reg_name:
        reg = reg_name + '_' + current_pipe
        return getGammLUTFromReg(gfx_index, reg_name[:18], 129, reg[-3:])

    # to get plane preoffsets
    if "PLANE_CSC_PREOFF" in reg_name and bit_field == "precsc_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name[:-1]) + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # to get plane_csc_enable bit
    if "PLANE_COLOR_CTL_" in reg_name and "plane_csc_enable" in bit_field:
        element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
        return __str_to_datatype(data_type)(element_value)

    # to get value for plane csc coefficients
    if "PLANE_CSC_COEFF" in reg_name:
        plane_coefficients = list(itertools.chain.from_iterable(
            getCSCCoeffMatrixFromReg(gfx_index, "PLANE_CSC_COEFF", reg_name[-1] + "_" + current_pipe)))
        return plane_coefficients

    # to get plane postoffsets
    if "PLANE_CSC_POSTOFF" in reg_name and bit_field == "postcsc_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name[:-1]) + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name[:-1]) + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # to get value for 1dLut postcscLut enable (True when element_value is 0 and false when value is 1)
    if "PLANE_COLOR_CTL_" in reg_name and data_type == "bool":
        element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
        return not (__str_to_datatype(data_type)(element_value))

    #  to get value for 1dLut planepostcscLut data
    if "PLANE_POST_CSC_GAMC_DATA" in reg_name:
        reg = reg_name + '_' + current_pipe
        return getGammLUTFromReg(gfx_index, reg_name[:19], 33, reg[-3:])

    # to get pipeprecscLut for pipe
    if "PRE_CSC_GAMC" in reg_name and data_type == "pipeprecscLut_data":
        return getGammLUTFromReg(gfx_index, reg_name, 33, current_pipe)

    # to get pipe preoffsets
    if "CSC_PREOFF" in reg_name and bit_field == "precsc_medium_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name) + "_" + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # to get pipe_csc_coefficients
    if "CSC_COEFF" == reg_name and bit_field == "pipe_csc_coefficients":
        return list(itertools.chain.from_iterable(getCSCCoeffMatrixFromReg(gfx_index, "CSC_COEFF", current_pipe)))

    # to get postoffsets
    if "CSC_POSTOFF" in reg_name and bit_field == "postcsc_medium_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name) + "_" + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # to get value for D11PipeMSLut data
    if reg_name == "PIPE_MISC" and data_type == "pipePostCscEOTFLut_data":
        element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
        if element_value == 1:
            return getPipeGammaLUTFromReg(gfx_index, "MULTI_SEGMENT", current_pipe)
        else:
            return []

    # to get pipepostcscLUT for pipe
    if reg_name == "GAMMA_MODE" and data_type == "pipepostcscLut_data":
        gamma_mode_offset = color_common_utility.get_register_offset((reg_name) + "_" + "REGISTER", reg_name,
                                                                     current_pipe,
                                                                     PLATFORM)
        gamma_mode_reg_value_before_resetting = driver_interface.DriverInterface().mmio_read(gamma_mode_offset,
                                                                                             gfx_index)
        if driver_interface.DriverInterface().mmio_write(gamma_mode_offset, 0, gfx_index):
            logging.debug("Successfully set GammaMode register to 0")
        else:
            logging.error("Failed set GammaMode register to 0")
        time.sleep(5)
        logging.debug("restored gamma value:{}".format(gamma_mode_reg_value_before_resetting))
        driver_interface.DriverInterface().mmio_write(gamma_mode_offset, gamma_mode_reg_value_before_resetting,
                                                      gfx_index)
        directory = __get_directory_based_on_platform(PLATFORM)
        element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
        if element_value > 0:
            hdr_mode_bit = __get_element_value(gfx_index, "PIPE_MISC", "hdr_mode", current_pipe)
            if hdr_mode_bit == 0:
                return getPipeGammaLUTFromReg(gfx_index, "12BIT_GAMMA", current_pipe)
            elif int(directory[1:3]) >= 13:
                return getPipeGammaLUTFromReg(gfx_index, "LOGARITHMIC_LUT", current_pipe)
            else:
                return getPipeGammaLUTFromReg(gfx_index, "MULTI_SEGMENT", current_pipe)

    # to get output csc preoffsets
    if "OUTPUT_CSC_PREOFF" in reg_name and bit_field == "precsc_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name) + "_" + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # to get pipe_output_csc_coefficients
    if "OUTPUT_CSC_COEFF" == reg_name and bit_field == "pipe_csc_coefficients":
        return list(
            itertools.chain.from_iterable(getCSCCoeffMatrixFromReg(gfx_index, "OUTPUT_CSC_COEFF", current_pipe)))

    # to get output csc postoffsets
    if "OUTPUT_CSC_POSTOFF" in reg_name and bit_field == "postcsc_offset":
        element_list = []
        register_file = importlib.import_module("registers." + PLATFORM + "." + (reg_name) + "_" + "REGISTER")
        reg = reg_name + '_' + current_pipe
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x0, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x4, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        register_read_value = reg_read.read((reg_name) + "_" + "REGISTER", reg, PLATFORM, 0x8, gfx_index)
        element_list.append(__str_to_datatype(data_type)(register_read_value.__getattribute__(str(bit_field))))
        return element_list

    # common lines for register read
    element_value = __get_element_value(gfx_index, reg_name, bit_field, current_pipe)
    return __str_to_datatype(data_type)(element_value)


##
# @brief           function to update the json with the value received from registers
# @param[in]       gfx_index - Graphics Adapter Index
# @param[inout]    input_json_data - data from input json
# @return          input_json_data - updated input json with required values received from registers
def __update_json_output_dict(gfx_index, input_json_data):
    global __CAPTURE_INSTANCE
    flattened_dict = __flatten_input_json_dict(input_json_data)
    filtered_list, filtered_list_input_output = __iterate_through_dict(flattened_dict)

    filtered_pair_list = [filtered_list[n: n + 3] for n in range(0, len(filtered_list), 3)]

    for i in range(len(filtered_pair_list)):
        reg_name = eval("input_json_data" + __create_path_from_flatten_dict(filtered_pair_list[i][0]))
        bit_field = eval("input_json_data" + __create_path_from_flatten_dict(filtered_pair_list[i][1]))
        data_type = eval("input_json_data" + __create_path_from_flatten_dict(filtered_pair_list[i][2]))
        reg_value = __read_register_from_json_data(gfx_index, reg_name, bit_field, data_type)
        input_json_path = '/'.join(filtered_pair_list[i][0].split())[:-9]
        exec("input_json_data" + __create_path_from_flatten_dict(input_json_path) + '=' + str(reg_value))

    for i in range(len(filtered_list_input_output)):
        input_img = eval("input_json_data" + __create_path_from_flatten_dict(filtered_list_input_output[i]))
        file_name, file_extension = os.path.splitext(input_img)
        dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
        path_to_dir = os.path.join(test_context.LOG_FOLDER, dir_name)
        if os.path.isdir(path_to_dir) is True:
            shutil.rmtree(path_to_dir)
            os.mkdir(path_to_dir)
        else:
            os.mkdir(path_to_dir)
        if "Src" in file_name:
            input_img = file_name.replace(file_name[-2:], "_" + str(__CAPTURE_INSTANCE - 1)) + file_extension
        else:
            input_img = file_name + "_" + str(__CAPTURE_INSTANCE - 1) + file_extension
        input_image_path = os.path.join(path_to_dir, input_img)
        input_image_path = '"{}"'.format(input_image_path)
        input_image_path = input_image_path.replace("\\", "\\\\")
        input_json_path = '/'.join(filtered_list_input_output[i].split())
        exec("input_json_data" + __create_path_from_flatten_dict(input_json_path) + '=' + (input_image_path))

    return input_json_data


##
# @brief        function to generate software json from updated input json
# @param[in]    output_json_data -  updated input json
# @return       status - True if output json file is created, False otherwise
def __dump_json_data_to_swconfig(output_json_data):
    global __CAPTURE_INSTANCE
    global INPUT_SW_JSON
    INPUT_SW_JSON = "SwConfig.json"
    # dir_name = "CAPTURE_INSTANCE_" + str(__CAPTURE_INSTANCE - 1)
    # path_to_dir = os.path.join(test_context.LOG_FOLDER, dir_name)
    SwConfig = os.path.join(test_context.LOG_FOLDER, INPUT_SW_JSON)
    json_handle = open(SwConfig, 'w')
    status = json.dump(output_json_data, json_handle, indent=4)
    json_handle.close()

    return status


##
# @brief        function to parse input json data
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    input_json - input JSON file path
# @return       status - True if register data is dumped in output json file, False otherwise
def __parse_input_json(gfx_index, input_json):
    # read input json
    input_json_data = __read_input_json(input_json)

    # Generate SwConfig.json data
    output_json_data = __update_json_output_dict(gfx_index, input_json_data)

    # dump the SwConfig.json data
    status = __dump_json_data_to_swconfig(output_json_data)

    return status
