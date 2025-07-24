########################################################################################################################
# @file         caso_manual_test.py
# @brief        The script contains verification and ETL parsing logic for CASO tests
#               Usage:
#                  caso_manual_test.py [-h] [-TYPE {CASO,ETL}] [-D3D {11,12}] [-SYNC_INTERVAL {SYNC_0,SYNC_1,SYNC_WT}]
#                  [-DISPLAY_MODE {DEFAULT,MAX}] [-BUFFER_SIZE {DEFAULT,MAX}] [-WINDOWED_MODE {WINDOWED,FULLSCREEN}]
#                  [-PATH PATH]
# @author       Pai, Vinayak1
########################################################################################################################
import argparse
import logging
import os
import subprocess
import sys
import time

from Libs.Core import etl_parser, winkb_helper
from Libs.Core.test_env import test_context

LINE_WIDTH = 100

# Folder path
__CASO_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "CASO\\D3D11_CASO")
__VRR_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")

# App path
__CASO_APP_PATH = os.path.join(__CASO_FOLDER, "DXGICrossAdapterScanOutPresent.exe --functional")
__CLASSICD3D_APP_PATH = os.path.join(__VRR_FOLDER, "Classic3DCubeApp.exe adapter:1")

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.flipData = 1


##
# @brief            API to verify surface memory address
# @param[in]        etl_file : Path of the ETL file to be verified
# @param[in]        pipe     :
# @return           status   : True if Async Flips are present else False
def verify_surface_memory_type(etl_file, pipe):
    flip_details = []
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    flip_data = etl_parser.get_flip_data('PIPE_' + pipe)
    for plane_data in flip_data:
        if len(plane_data.FlipAllParamList) != 0:
            for flip_all_param in plane_data.FlipAllParamList:
                flip_details.append(('allparam', flip_all_param.SurfMemType, flip_all_param.ScanX, flip_all_param.ScanY,
                                     (flip_all_param.TimeStamp / 1000)))

    time_difference_list = [flip_details[i + 1][4] - flip_details[i][4] for i in range(len(flip_details) - 1)]
    max_time_difference = max(time_difference_list)
    index = time_difference_list.index(max_time_difference)

    if (flip_details[index][1] != 1) and (flip_details[index + 1][1] != 1):
        return False

    print("The details of the maximum difference flips")
    print("------------------------------------------------------------------------------------------")
    print("Surface Memory Type\t\tScan X\t\t\tScan Y\t\t\tTimeStamp")
    print("%s\t\t\t%.2f\t\t\t%.2f\t\t\t%.2f" % (
        "Linear    " if flip_details[index][1] == 1 else "Non-Linear", flip_details[index][2], flip_details[index][3],
        flip_details[index][4]))
    print("%s\t\t\t%.2f\t\t\t%.2f\t\t\t%.2f" % (
        "Linear    " if flip_details[index + 1][1] == 1 else "Non-Linear", flip_details[index + 1][2],
        flip_details[index + 1][3], flip_details[index + 1][4]))
    print("------------------------------------------------------------------------------------------")
    return True


##
# @brief            API to verify CASO using app
# @param[in]        d3d_version       : D3D Runtime value [11/12]
# @param[in]        sync_interval     : Sync Interval value [SYNC_0, SYNC_1, SYNC_WT]
# @param[in]        display_mode      : Displays Modes [MIN, MAX]
# @param[in]        buffer_size       : Buffer Size [MIN/MAX]
# @param[in]        windowed_mode     : Windowed mode [WINDOWED/ FULLSCREEN]
# @return           status            : True if CASO is enabled, otherwise False
def verify_caso_using_app(d3d_version, sync_interval, display_mode, buffer_size, windowed_mode):
    status = True
    # todo : Add caso registry check once valsim support is available in HG config
    stdout = open_close_caso_app(d3d_version, sync_interval, display_mode, buffer_size, windowed_mode)
    status &= get_result_from_output(stdout)
    if status:
        print("Test Passed!!".center(LINE_WIDTH, "*"))
    else:
        print("Test Failed!!".center(LINE_WIDTH, "*"))


######################
#  Helper Functions  #
######################

##
# @brief            API to open/close the CASO app
# @param[in]        d3d_version       : D3D Runtime value [11/12]
# @param[in]        sync_interval     : Sync Interval value [SYNC_0, SYNC_1, SYNC_WT]
# @param[in]        display_mode      : Displays Modes [MIN, MAX]
# @param[in]        buffer_size       : Buffer Size [MIN/MAX]
# @param[in]        windowed_mode     : Windowed mode [WINDOWED/ FULLSCREEN]
# @return           stdout            : A file that contains the log of the app
def open_close_caso_app(d3d_version, sync_interval, display_mode, buffer_size, windowed_mode):
    # To minimize all the windows
    winkb_helper.press('WIN+M')

    with open('result.txt', 'w') as app_log_file:
        process = subprocess.Popen(str(__CASO_APP_PATH), stdout=subprocess.PIPE)

        # D3D type
        if d3d_version == 12:
            winkb_helper.press('1')
            time.sleep(0.05)

        # Display Mode
        if display_mode == 'MAX':
            for key_press in range(0, 3):
                winkb_helper.press('2')
                time.sleep(0.05)

        # Buffer Size
        if buffer_size == 'MAX':
            winkb_helper.press('4')
            time.sleep(0.05)

        # Sync Interval
        if sync_interval != 'SYNC_1':
            if sync_interval == 'SYNC_WT':
                winkb_helper.press('5')
            if sync_interval == 'SYNC_0':
                for key_press in range(0, 2):
                    winkb_helper.press('5')
                    time.sleep(0.05)

        # Windowed Mode
        if windowed_mode == 'FULLSCREEN':
            winkb_helper.press('6')
            time.sleep(0.05)

        # App will be open for 60 seconds
        time.sleep(60)

        # Close the App
        winkb_helper.press('ALT+F4')

        stdout, _ = process.communicate()
        return stdout


##
# @brief            API to open/close Classic3d Cube App
# @return           status : None
def open_close_classic3D_app():
    # To minimize all the windows
    winkb_helper.press('WIN+M')

    classic3d_app = subprocess.Popen(__CLASSICD3D_APP_PATH)

    # To scale to FullScreen
    winkb_helper.press('F5')

    # App will be open for 20 seconds
    time.sleep(20)

    # Close the App
    classic3d_app.terminate()


##
# @brief            API to get the result from the output
# @param[in]        stdout : output from the app
# @return           status : True if CASO is enabled, otherwise False
def get_result_from_output(stdout):
    stdout = stdout.decode("utf-8")
    status = True
    if "Hybrid 1-copy (CASO) mode." in stdout:
        status &= True
        print("PASS: CASO is Enabled!!".center(LINE_WIDTH, "*"))
        return status
    else:
        status &= False
    print("FAIL: CASO is Disabled!!".center(LINE_WIDTH, "*"))
    return status


'''
Valsim support for HG setup is not available, API will be used once support is available
##
# @brief            API to check whether CASO is enabled in registry or not
# @return           status : True if CASO is enabled in registry, otherwise False
def check_caso_in_registry():
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
    reg_value, _ = registry_access.read(args=reg_args, reg_name="KmFtrControl")
    if reg_value == 2 or reg_value == 3:
        print("*****************PASS: CASO is Enabled in Registry!!*****************")
        return True
    print("*****************FAIL: CASO is Disabled in Registry!!*****************")
    return False
'''


##
# @brief            API to parse the commandline
# @return           args : argument list
def prepare_parser():
    parser = argparse.ArgumentParser(description='Process the Command line Arguments.')
    parser.add_argument('-TYPE', default='CASO', choices=['CASO', 'ETL'], type=str.upper,
                        help='Determines the type of run')
    parser.add_argument('-D3D_VERSION', default=11, choices=[11, 12], type=int, help='Determines the version of D3D apps')
    parser.add_argument('-SYNC_INTERVAL', default='SYNC_1', choices=['SYNC_0', 'SYNC_1', 'SYNC_WT'], type=str.upper,
                        help='Determines the type of sync interval')
    parser.add_argument('-DISPLAY_MODE', default='DEFAULT', choices=['DEFAULT', 'MAX'], type=str.upper,
                        help='Determines the display mode')
    parser.add_argument('-BUFFER_SIZE', default='DEFAULT', choices=['DEFAULT', 'MAX'], type=str.upper,
                        help='Determines the buffer size')
    parser.add_argument('-WINDOWED_MODE', default='WINDOWED', choices=['WINDOWED', 'FULLSCREEN'], type=str.upper,
                        help='Determines the screen')
    parser.add_argument('-PATH', default='None', type=str, help='Path to ETL File')
    args = parser.parse_args()
    return args


######################
#     Main Code      #
######################

args = prepare_parser()
if "CASO" in args.TYPE:
    print("Running CASO App and verifying CASO".center(LINE_WIDTH, "*"))
    verify_caso_using_app(args.D3D_VERSION, args.SYNC_INTERVAL, args.DISPLAY_MODE, args.BUFFER_SIZE, args.WINDOWED_MODE)
    sys.exit("CASO verification completed".center(LINE_WIDTH, "*"))
if 'ETL' in args.TYPE and args.PATH != 'None':
    etl_path = args.PATH.replace('\\', '\\\\')
    print("Parsing ETL to get the Surface Memory Type".center(LINE_WIDTH, "*"))
    print(f"ETL File Path: {etl_path}")
    status = verify_surface_memory_type(etl_path, "A")
    if status:
        print("Test Passed!! Surface Memory Type is Linear during CASO checkout".center(LINE_WIDTH, "*"))
    else:
        print("Test Failed!! Surface Memory Type is Non-Linear during CASO checkout".center(LINE_WIDTH, "*"))
    sys.exit("ETL verification completed".center(LINE_WIDTH, "*"))
else:
    sys.exit("Incomplete commandline. Please Provide -PATH <path to the etl file> parameter".center(LINE_WIDTH, "*"))
