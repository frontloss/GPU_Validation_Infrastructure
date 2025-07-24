########################################################################################################################
# @file         planes_ui_helper.py
# @brief        The script consists of helper functions for Planes UI Tests
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import os
import shutil
import subprocess
import sys
import time
from enum import Enum, IntEnum

from Libs.Core import registry_access, winkb_helper, window_helper, display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Feature.app import App3D, PresentAtApp, Youtube, VLC
from Libs.Feature.app import AppMedia
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.PowerCons.Modules.workload import get_app_coordinates


###############################
# Enum for Apps/Media/Actions #
###############################

##
# @brief        Registry Status Type
class RegistryStatus(IntEnum):
    DISABLE = 0
    ENABLE = 1


##
# @brief            Path to 3D Applications
class Apps(Enum):
    FLIPAT = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR\\FlipAt\\FlipAt.exe")
    CLASSICD3D = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\ClassicD3D\\ClassicD3D.exe")
    D3D12FULLSCREEN = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\D3D12FullScreen\\D3D12Fullscreen.exe")
    PRESENTAT = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\PresentAt\\D3D11PresentAt.exe")


##
# @brief            Path to media files
class Videos(Enum):
    FPS_23_976 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\23.976.mp4")
    FPS_24 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\24.000.mp4")
    FPS_25 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\25.000.mp4")
    FPS_29_970 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\29.970.mp4")
    FPS_30 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\30.000.mp4")
    FPS_59_940 = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos\\59.940.mp4")
    FPS_60 = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\60.000.mp4")
    RES_4K = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\mpo_3840_2160_avc.mp4")
    RES_5K = ""
    RES_8K = ""


##
# @brief            Path to YouTube files
class YouTube(Enum):
    RES_NORMAL = 'https://www.youtube.com/watch?v=d9MyW72ELq0'
    RES_4K = ""
    RES_8K = ""


##
# @brief            Command to install Chocolatey/VLC
class Command(Enum):
    CHOCO_INSTALL = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::" \
                    "SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex" \
                    " ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    VLC_INSTALL = "choco install vlc --proxy http://proxy-dmz.intel.com:912 -y --force --no-progress"


##
# @brief            FPS value
class FPS(Enum):
    FPS_23_976 = 23.976
    FPS_24 = 24.0
    FPS_25 = 25.0
    FPS_29_970 = 29.970
    FPS_30 = 30.0
    FPS_59_940 = 59.940
    FPS_60 = 60.0
    RES_4K = 30.0
    RES_5K = None
    RES_8K = None


####################
# Registry Updates #
####################

##
# @brief        Helper function to enable/disable AutoDetect Proxy settings
# @param[in]    value : Enum Enable or Disable
# @return       None
def enable_disable_auto_detect_proxy(value):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=r"Software\Microsoft")
    if registry_access.write(args=reg_args, reg_name="AutoDetect",
                             reg_type=registry_access.RegDataType.DWORD, reg_value=value,
                             sub_key=r"Windows\CurrentVersion\Internet Settings") is False:
        logging.error(
            f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} AutoDetect Proxy Settings")
    else:
        logging.info(
            f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} AutoDetect Proxy Settings")


##
# @brief        Helper function to enable/disable HideFirstRunExperience for Edge browser
# @param[in]    value : Enum Enable or Disable
# @return       None
def enable_disable_first_run_experience(value):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE, reg_path=r"Software\Policies")
    if registry_access.write(args=reg_args, reg_name="HideFirstRunExperience",
                             reg_type=registry_access.RegDataType.DWORD, reg_value=value,
                             sub_key=r"Microsoft\Edge") is False:
        logging.error(
            f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} HideFirstRunExperience for "
            f"Edge browser")
    else:
        logging.info(
            f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} HideFirstRunExperience for "
            f"Edge browser")


##
# @brief        Helper function to toggle Dc6v and FlipQ
# @param[in]    value     : True to disable Dc6v and enable FlipQ and false vice versa
# @param[in]    gfx_index : Graphics Adapter index
# @return       None
def disable_dc6v_enable_osflipq(value, gfx_index):
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
    dc6v_registry_value, dc6v_registry_type = registry_access.read(args=ss_reg_args, reg_name="DisplayPcFeatureControl")
    flipq_registry_value, flipq_registry_type = registry_access.read(args=ss_reg_args,
                                                                     reg_name="DisplayFeatureControl2")
    logging.info(f'DisplayFeatureControl2 initial value: {flipq_registry_value}')
    logging.info(f'DisplayPcFeatureControl initial value: {dc6v_registry_value}')
    if dc6v_registry_value is not None:
        if value:
            dc6v_reg_value = dc6v_registry_value | 0x40000
        else:
            dc6v_reg_value = dc6v_registry_value & 0xFFFBFFFF
    else:
        dc6v_reg_value = 0x40000

    if flipq_registry_value is not None:
        if value:
            flipq_reg_value = flipq_registry_value | 0x1
        else:
            flipq_reg_value = flipq_registry_value & 0xFFFFFFFE
    else:
        flipq_reg_value = 0x1

    registry_access.write(args=ss_reg_args, reg_name="DisplayPcFeatureControl",
                          reg_type=registry_access.RegDataType.DWORD, reg_value=dc6v_reg_value)
    registry_access.write(args=ss_reg_args, reg_name="DisplayFeatureControl2",
                          reg_type=registry_access.RegDataType.DWORD, reg_value=flipq_reg_value)
    logging.info(
        f"{'Disabling Dc6v' if value else 'Enabling Dc6v'} and {'enabling flipQ' if value else 'disabling flipQ'}"
        f" in registry")
    result, reboot_required = display_essential.restart_gfx_driver()
    if result is False:
        logging.error("Failed to disable-enable display driver")
        return False
    dc6v_registry_value, dc6v_registry_type = registry_access.read(args=ss_reg_args, reg_name="DisplayPcFeatureControl")
    flipq_registry_value, flipq_registry_type = registry_access.read(args=ss_reg_args,
                                                                     reg_name="DisplayFeatureControl2")
    logging.info(f'DisplayFeatureControl2 value after write: {flipq_registry_value}')
    logging.info(f'DisplayPcFeatureControl value after write: {dc6v_registry_value}')


##
# @brief        Helper function to check if OS FlipQ is disabled and OS unaware FlipQ + DC6V is enabled
# @param[in]    gfx_index : Graphics Adapter index
# @param[in]    etl_file  : Name of the ETL file
# @return       True if OS FlipQ is disbaled and OS unaware FlipQ + DC6V is enabled
def check_os_unaware_flipq_dc6v_status(gfx_index, etl_file):
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
    dc6v_registry_value, dc6v_registry_type = registry_access.read(args=ss_reg_args, reg_name="DisplayPcFeatureControl")
    flipq_registry_value, flipq_registry_type = registry_access.read(args=ss_reg_args,
                                                                     reg_name="DisplayFeatureControl2")

    if dc6v_registry_value & (1 << 18):
        dc6v_enable = False
    else:
        dc6v_enable = True

    if flipq_registry_value & 0x8:
        os_unaware_flipq_enable = True
    else:
        os_unaware_flipq_enable = False

    if dc6v_enable and os_unaware_flipq_enable and not planes_ui_verification.os_flipq_status_in_os_ftr_table(etl_file):
        logging.info("OS unaware FlipQ + DC6v is enabled")
        return True
    else:
        logging.info("OS unaware FlipQ + DC6v is disabled")
        return False


###########
# Generic #
###########

##
# @brief            Helper Function to set display configuration
# @param[in]        topology                      : Topology of displays to be plugged in
# @param[in]        display_and_adapter_info_list : Display and adapter info list
# @return           adapter_tid_dict
def set_display_config(topology, display_and_adapter_info_list):
    config = DisplayConfiguration()
    status = config.set_display_configuration_ex(topology, display_and_adapter_info_list)
    if status:
        logging.info(f"Successfully applied display configuration {DisplayConfigTopology(topology).name}"
                     f" {display_and_adapter_info_list}")
    else:
        report_to_gdhm('SFLIPQ', f"Failed to display configuration {DisplayConfigTopology(topology).name} "
                                 f"{display_and_adapter_info_list}")
        logging.error(f"Failed to display configuration {DisplayConfigTopology(topology).name} "
                      f"{display_and_adapter_info_list}")
    return status


##
# @brief            Helper function to apply_native_mode
# @param[in]        panel : Panel
# @return           mode  : Native mode
def apply_native_mode(panel):
    config = DisplayConfiguration()
    native_mode = config.get_native_mode(panel.target_id)
    if native_mode is None:
        logging.error(f"Failed to get native mode for {panel.target_id}")
        return False
    mode = config.get_current_mode(panel.target_id)
    hzres = native_mode.hActive
    vtres = native_mode.vActive
    rr = native_mode.refreshRate
    mode.HzRes, mode.VtRes, mode.refreshRate = hzres, vtres, rr
    if config.set_display_mode([mode]):
        logging.info(f"Successfully applied native display mode {mode.HzRes} X {mode.VtRes} @ {mode.refreshRate} "
                     f"Scaling : {mode.scaling} Rotation: {mode.rotation}")
    else:
        logging.error(f"Failed to apply native mode {mode.HzRes} X {mode.VtRes} @ {mode.refreshRate} "
                      f"Scaling : {mode.scaling} Rotation: {mode.rotation}")
    return mode


##
# @brief        Helper function to start ETL capture.
# @param[in]    file_name : ETL file name
# @return       status    : True if ETL started otherwise False
def start_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture.
# @param[in]    file_name     : ETL file name
# @return       etl_file_path : Path of ETL file captured
def stop_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after playback")
    return etl_file_path


##
# @brief        Helper function to get action type
# @param[in]    argument : Command line tag
# @return       value    : Argument value
def get_config_type(argument):
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if argument in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == argument:
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        raise Exception("Incorrect command line")


##
# @brief            Helper function to verify different features
# @param[in]        feature      : Name of the feature
# @param[in]        etl_file     : Name of the ETL file
# @param[in]        pipe         : Name of the pipe
# @param[in]        target_id    : Display target id
# @param[in]        adapter      : Dictionary of Adapter
# @param[in]        platform      : platform Name
# @return           status       : True if feature verification is successful else False
def verify_feature(feature, etl_file, pipe, target_id, adapter=None, platform=None):
    status = False
    if adapter is None and platform is None:
        logging.error("wrong argument passed")
    if adapter is not None and platform is None:
        platform = adapter.platform
    if feature == 'SFLIPQ':
        status_ = check_os_unaware_flipq_dc6v_status(adapter.gfx_index, etl_file)
        if status_ == 0:
            status = planes_ui_verification.verify_flipq(etl_file, pipe, target_id, platform)
        elif status == 1:
            status = planes_ui_verification.verify_flipq_dc6v(etl_file, pipe, target_id, platform)
    elif feature == 'MPO':
        status = planes_ui_verification.verify_mpo(etl_file, pipe, target_id, platform)
    elif feature == 'FLIPQ_HRR':
        status = planes_ui_verification.verify_flipq_hrr(etl_file, pipe, target_id, platform)
    elif feature == 'FLIP':
        status = planes_ui_verification.verify_flip(etl_file, pipe, target_id, platform)

    return status



#####################
# Media/App related #
#####################

##
# @brief        Helper function to generate Flip pattern for FlipAt
# @param[in]    fps          : The FPS for which pattern needs to be generated
# @return       flip_pattern : Pattern for the FlipAt application
def generate_flip_pattern(fps):
    flip_time_in_ms = 1000 // int(fps)
    flip_pattern = f"{flip_time_in_ms} 10 {flip_time_in_ms} 10"
    return flip_pattern


##
# @brief        Helper function to create an object for specified app
# @param[in]    app_type : Type of app MEDIA/3D/YOUTUBE/VLC
# @return       object of the specified app type
def create_app_instance(app_type=None):
    if app_type == 'MEDIA':
        return AppMedia(Videos[f"{get_config_type('-MEDIA_TYPE')}"].value)
    if app_type == 'FLIPAT':
        return App3D('FlipAt', Apps[app_type].value + ' ' + generate_flip_pattern(get_config_type('-FPS')))
    if app_type == 'D3D12FULLSCREEN':
        return App3D('D3D12Fullscreen', Apps[app_type].value)
    if app_type == 'CLASSICD3D':
        return App3D('ClassicD3D', Apps[app_type].value + ' ' + f"interval:{get_config_type('-INTERVAL')}" + ' ' +
                     f"buffers:{get_config_type('-BUFFER')}")
    if app_type == 'PRESENTAT':
        return PresentAtApp(Apps[app_type].value, get_config_type('-DEPTH'), get_config_type('-REPORTINTERVAL'),
                            get_config_type('-FPS'), get_config_type('-POSITION'))
    if app_type == 'YOUTUBE':
        enable_disable_auto_detect_proxy(RegistryStatus.ENABLE)
        enable_disable_first_run_experience(RegistryStatus.ENABLE)
        return Youtube(YouTube['RES_NORMAL'].value)
    if app_type == 'VLC':
        enable_disable_auto_detect_proxy(RegistryStatus.ENABLE)
        install_vlc_media_player()
        return VLC(Videos[f"{get_config_type('-MEDIA_TYPE')}"].value)
    else:
        raise Exception(f"{app_type} is not defined")


##
# @brief        Helper function to enable subtitles in Media Player
# @return       None
def enable_subtitles():
    logging.info("Enabling Subtitles")

    ##
    # Shortcut to open subtitles menu
    winkb_helper.press('ALT+L')
    logging.info("Opened subtitle menu")
    winkb_helper.press('ENTER')
    logging.info("Selected the subtitle file")

    ##
    # To hide the media controls
    winkb_helper.press('ESC')
    logging.info("Disabled media controls")


##
# @brief        Helper function to move test videos and subtitle file to Videos folder
# @param[in]    video_path : Path to the video
# @return       None
def move_files_to_videos_folder(video_path):
    VIDEOS_FOLDER_PATH = r"C:\Users\gta\Videos"
    SRT_FILE_PATH = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "SampleSubtitleFile.srt")

    ##
    # Clear the contents in Videos Folder
    for file in os.listdir(VIDEOS_FOLDER_PATH):
        os.remove(f'{VIDEOS_FOLDER_PATH}\\{file}')

    ##
    # Copy the video from SHAREDBINARY to Videos Folder
    shutil.copy(video_path, VIDEOS_FOLDER_PATH)

    ##
    # Copy the Subtitle file from TestSpecificBin to Videos Folder
    shutil.copy(SRT_FILE_PATH, VIDEOS_FOLDER_PATH)
    ##
    # Rename the srt file as that of video name.So that the file name pops up when the subtitle option is used
    srt_file_name = video_path.split('\\')[-1].split('.')
    if srt_file_name[0].isdigit():
        srt_file_name = srt_file_name[0] + '.' + srt_file_name[1] + ".srt"
    else:
        srt_file_name = video_path.split('\\')[-1].split('.')[0] + ".srt"
    srt_file = f'{VIDEOS_FOLDER_PATH}\\SampleSubtitleFile.srt'
    renamed_srt_file = f'{VIDEOS_FOLDER_PATH}\\{srt_file_name}'
    os.rename(srt_file, renamed_srt_file)


##
# @brief        Helper function to play video with subtitles
# @param[in]    video_path : Path to the video
# @param[in]    panel      : Panel
# @return       None
def play_video_with_subtitles(video_path, panel=None):
    config = DisplayConfiguration()
    move_files_to_videos_folder(video_path)
    video_name = video_path.split('\\')[-1]
    window_helper.minimize_all_windows()

    ##
    # Command to play video using commandline
    cmd_line = r'start "mswindowsvideo://" "C:\Users\gta\Videos\{0}"'.format(video_name)
    os.system(cmd_line)
    left, top, right, bottom = get_app_coordinates()
    if panel is not None:
        mode = config.get_current_mode(panel.target_id)
        logging.info(f"{mode.HzRes} X {mode.VtRes}")
        if right == mode.HzRes and bottom == mode.VtRes:
            logging.info("App is in FullScreen mode")

    ##
    # To get control of the media player
    window_helper.mouse_left_click(400, 400, True)
    time.sleep(2)

    ##
    # Scale to FullScreen
    winkb_helper.press('F11')
    time.sleep(1)

    ##
    # Enable Subtitles
    enable_subtitles()

    ##
    # Wait for a minute during video playback
    time.sleep(60)

    ##
    # Close Media Player
    window_helper.close_media_player()


##
# @brief        Helper function to install VLC media player
# @return       status : True if installation is successful else False
def install_vlc_media_player():
    if check_chocolatey_installation() is False:
        logging.info("Chocolatey not installed. Installing Chocolatey...")
        subprocess.run(f'"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" '
                       f'{Command["CHOCO_INSTALL"].value}', timeout=180)
        if check_chocolatey_installation() is False:
            assert False, "Chocolatey Installation Failed"
        logging.info("Chocolatey installed Successfully")
        logging.info("Installing VLC...")
        subprocess.run(f'"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" '
                       f'{Command["VLC_INSTALL"].value}', timeout=180)
        if check_vlc_installation() is False:
            assert False, "VLC media player Installation Failed"


##
# @brief        Helper function to check whether chocolatey is installed or not
# @return       status : True if chocolatey is installed else False
def check_chocolatey_installation():
    try:
        result = subprocess.run('choco', capture_output=True)
        if "Chocolatey" in result.stdout.decode():
            logging.info("Chocolatey is already installed. Proceeding to next step")
            return True
    except FileNotFoundError:
        return False


##
# @brief        Helper function to check whether VLC media player is installed or not
# @return       status : True if VLC media player is installed else False
def check_vlc_installation():
    try:
        subprocess.run('C:\\Program Files\\VideoLAN\\VLC\\vlc.exe', capture_output=True)
        return True
    except FileNotFoundError:
        return False


##################
# GDHM Reporting #
##################

##
# @brief            Helper function to report GDHM
# @param[in]        feature    : Any feature in planesUI [SFLIPQ/MPO/FULLFLIPQ]
# @param[in]        message    : GDHM message
# @param[in]        priority   : Priority of the GDHM bug [P1/P2/P3/P4]
# @param[in]        driver_bug : True for driver bug reporting else False
# @return           None
def report_to_gdhm(feature, message="", priority='P2', driver_bug=True):
    if message == "":
        title = f"[Display_OS_Features][Display_Planes][{feature}] verification failed"
    else:
        title = f"[Display_OS_Features][Display_Planes][{feature}] {message}"
    if driver_bug:
        gdhm.report_driver_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
    else:
        gdhm.report_test_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
