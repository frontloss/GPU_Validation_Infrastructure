##
# @file         flip_helper.py
# @brief        This script contains helper functions that will be used by Dxflips test scripts
# @author       Sunaina Ashok

import logging
import os
import subprocess
import sys
import time
from subprocess import Popen

from enum import IntEnum

from Libs.Core import winkb_helper, registry_access, display_essential, display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower, PowerSource
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper import control_api_wrapper
from Libs.Feature import socwatch
from Tests.Flips import flip_verification
from Tests.Flips.Dxflips.dxflips_base import dxflip_base
from Tests.test_base import TestBase

FLIP_AT_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR\\FlipAt")
FLIPMODEL_D3_D12_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\FlipModelD3D12")
TRIV_FLIP_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\TrivFlip")
SOC_WATCH_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "SocWatch_2021_1_1")
CLASSICD3D_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
CLASSICD3D_SYNC_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\ClassicD3D")
MOVING_RECTANGLE = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
PRESENTMON_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PresentMon")

# Registry path
INTEL_GMM_PATH = "SOFTWARE\\Intel"


##
# @brief        FPS Type
class FpsType(IntEnum):
    HIGH_FPS = 0
    LOW_FPS = 1
    MAX_FPS = 2


##
# @brief        Registry Status Type
class RegistryStatus(IntEnum):
    DISABLE = 0
    ENABLE = 1


stepCounter = 0
__app_state = dict()
config = DisplayConfiguration()

PRESENTMON_LOG_PATH = None


##
# @brief        Helper function to get the step value for logging
# @return       Step count
def getStepInfo():
    global stepCounter
    stepCounter = stepCounter + 1
    return "STEP-%d: " % stepCounter


##
# @brief        Helper function to get the display configuration
# @param[in]    connected_port_list : List of connected port
# @param[in]    enumerated_displays : Enumerated displays
# @return       Port config
def get_display_configuration(connected_port_list, enumerated_displays):
    port_config_str = ""
    for each_port in connected_port_list:
        target_id = config.get_target_id(each_port, enumerated_displays)
        mode = config.get_current_mode(target_id)
        port_config_str = port_config_str + "\n" + mode.to_string(enumerated_displays)
    return port_config_str


##
# @brief        Helper function to start ETL capture
# @param[in]    file_name : Name of the File
# @return       status    : Value indicating the result of the start_etl_tracer
def start_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    file_name = file_name + '.etl'
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture
# @param[in]    file_name     : Name of the File to stop ETL Capture
# @return       etl_file_path : Path of ETL file captured
def stop_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    file_name = file_name + '.etl'
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after playback")
    return etl_file_path


##
# @brief        Helper function to get the path of the app
# @param[in]    app_name : Name of the app
# @return       path     : Path to the app
def get_path(app_name):
    app = {
        'FLIPAT': os.path.join(FLIP_AT_FOLDER, "FlipAt.exe"),
        'TRIVFLIP': os.path.join(TRIV_FLIP_FOLDER, "TrivFlip11.exe -emulatedfs -fs -syncinterval 0 -fmt b8g8r8a8 "
                                                   "-bufcount 2 -framelatency 2"),
        'FLIPMODELD3D12': os.path.join(FLIPMODEL_D3_D12_FOLDER, "FlipModelD3D12.exe"),
        'CLASSICD3D': os.path.join(CLASSICD3D_FOLDER, "Classic3DCubeApp.exe"),
        'CLASSICD3D_SYNC': os.path.join(CLASSICD3D_SYNC_FOLDER, "ClassicD3D.exe"),
        'DOTA': os.path.join(FLIP_AT_FOLDER, "dota2.exe"),
        'GTA': os.path.join(CLASSICD3D_FOLDER, "gta5.exe"),
        'CONTROL': os.path.join(FLIPMODEL_D3_D12_FOLDER, "control_dx12.exe"),
        'RECTANGLE': os.path.join(MOVING_RECTANGLE, "MovingRectangleApp.exe")
    }
    return app.get(app_name.upper(), "App not found")


##
# @brief        Helper function to enable/disable developer mode
# @param[in]    value : Enum Enable or Disable
# @return       None
def enable_disable_developer_mode(value):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE, reg_path=r"Software\Microsoft")
    if registry_access.write(args=reg_args, reg_name="AllowDevelopmentWithoutDevLicense",
                             reg_type=registry_access.RegDataType.DWORD, reg_value=value,
                             sub_key=r"Windows\CurrentVersion\AppModelUnlock") is False:
        report_to_gdhm("ASYNCFLIPS", f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} Developer "
                                     f"mode on Windows", driver_bug=False)
        logging.error(
            f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} Developer mode on Windows")
    else:
        logging.info(
            f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} Developer mode on Windows")


##
# @brief        Helper function to enable/disable ForceFlipTrueImmediateMode
# @param[in]    value : Enum Enable or Disable
# @return       None
def enable_disable_flip_true_immediate_flips(value):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                             reg_path=r"System\CurrentControlSet")
    if registry_access.write(args=reg_args, reg_name="ForceFlipTrueImmediateMode",
                             reg_type=registry_access.RegDataType.DWORD,
                             reg_value=2 if value == RegistryStatus.ENABLE else 0,
                             sub_key=r"Control\GraphicsDrivers\Scheduler") is False:
        report_to_gdhm("ASYNCFLIPS",
                       f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} "
                       f"ForceFlipTrueImmediateMode", driver_bug=False)
        logging.error(
            f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} ForceFlipTrueImmediateMode")
    logging.info(
        f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} ForceFlipTrueImmediateMode")
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        assert False, "Failed to restart display driver"


##
# @brief        Helper function to enable/disable SpeedFrameEnable
# @param[in]    value : Enum Enable or Disable
# @param[in]    panel : panel data
# @return       None
def enable_disable_speed_sync(value, panel):
    ss_registry_args = registry_access.StateSeparationRegArgs(panel.display_and_adapterInfo.adapterInfo.gfxIndex)
    status = registry_access.write(args=ss_registry_args, reg_name="SpeedFrameEnable",
                                   reg_type=registry_access.RegDataType.DWORD,
                                   reg_value=value, sub_key="GMM")
    if status is False:
        logging.error(f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} SpeedFrameEnable")
    else:
        logging.info(f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} SpeedFrameEnable")

    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        assert False, "Failed to restart display driver"


##
# @brief        Helper function to play any application
# @param[in]    app          : Name of the app
# @param[in]    bfullscreen  : Mode in which application has to be launched
# @param[in]    fps_pattern  : FPS pattern in which app has to be run
# @param[in]    fps_pattern2 : FPS pattern in which app has to be run
# @return       None
def play_app(app, bfullscreen, fps_pattern=None, fps_pattern2=None):
    mode = "full screen mode " if bfullscreen else "windowed mode"
    logging.info(getStepInfo() + f"Launching {app} App in {mode}")
    path_to_app = get_path(app)

    if app.upper() == "FLIPAT" or app.upper() == "DOTA":
        if fps_pattern is not None:
            path_to_app += ' ' + ' '.join(map(str, fps_pattern))
        if fps_pattern2 is not None:
            path_to_app += ' ' + ' '.join(map(str, fps_pattern2))
        dxflip_base.app = Popen(path_to_app, cwd=os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER))
        fullscreen(bfullscreen, app)

    if app.upper() == "TRIVFLIP":
        dxflip_base.app = subprocess.Popen(path_to_app)
        fullscreen(bfullscreen, app)

    if app.upper() == "FLIPMODELD3D12" or app.upper() == "CONTROL":
        enable_disable_developer_mode(RegistryStatus.ENABLE)
        enable_disable_flip_true_immediate_flips(RegistryStatus.ENABLE)
        dxflip_base.app = subprocess.Popen(path_to_app)
        fullscreen(bfullscreen, app)
        winkb_helper.press('CTRL+K')
        logging.info(f"{app} is running in Vsync Off mode")

    if app.upper() == "CLASSICD3D" or app.upper() == "GTA":
        dxflip_base.app = subprocess.Popen(path_to_app)
        fullscreen(bfullscreen, app)
        logging.info(f"{app} is running in fullscreen mode")

    if app.upper() == "RECTANGLE":
        dxflip_base.app = subprocess.Popen(path_to_app)
        fullscreen(bfullscreen, app)
        logging.info(f"{app} is running in fullscreen mode")

    if dxflip_base.app is None:
        title = f"[Display_OS_Features][Display_Flips] {app} application did not open in {mode}"
        gdhm.report_test_bug_os(title, problem=gdhm.ProblemClassification.APP_CRASH)
        raise Exception(f"{app} application did not open in {mode}")
    logging.info(f"Launched {app} app successfully in {mode}")


##
# @brief            Helper function to choose verify function based on feature
# @param[in]        feature  : Name of the feature
# @param[in]        etl_file : Name of the ETL file
# @param[in]        pipe     : Pipe Name [A/B/C/D]
# @param[in]        eg_parameters     : Eg mode passed from command line and RR extracted from Scenario
# @return           status   : True if feature is present in ETL file else False
def verify_feature(feature, etl_file, pipe, eg_parameters=None):
    return {
        'SPEEDFRAME': lambda etl_file, pipe: flip_verification.verify_speedframe(etl_file, pipe),
        'ASYNCFLIPS': lambda etl_file, pipe: flip_verification.verify_asyncflips(etl_file, pipe),
        'VSYNC_OFF': lambda etl_file, pipe: flip_verification.verify_asyncflips(etl_file, pipe),
        'VSYNC_ON': lambda etl_file, pipe: flip_verification.verify_syncflips(etl_file, pipe),
        'SMOOTH_SYNC': lambda etl_file, pipe: flip_verification.verify_smooth_sync(etl_file, pipe),
        'ENDURANCE_GAMING': lambda etl_file, pipe: flip_verification.verify_endurance_gaming(etl_file, pipe,
                                                                                             eg_parameters)
    }.get(feature.upper())(etl_file, pipe)


##
# @brief            Helper function to choose verify ASync Flip Latency
# @param[in]        feature  : Name of the feature
# @param[in]        etl_file : Name of the ETL file
# @param[in]        pipe    : pipe data
# @return           status   : True if feature is present in ETL file else False
def verify_async_flip_latency(feature, etl_file, pipe):
    return {
        'ASYNCFLIPS': lambda etl_file, pipe: flip_verification.verify_flip_latency(etl_file, pipe)
    }.get(feature.upper())(etl_file, pipe)


##
# @brief        Helper function to get the action type from commandline
# @param[in]    argument : Action Argument
# @param[in]    no_exception : by default False, make True to avoid exception if  argument not found in commandline
# @return       argument value
def get_action_type(argument, no_exception=False):
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if argument in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == argument:
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        if no_exception:
            return None
        raise Exception("Incorrect command line")


##
# @brief        Helper function to get max RR
# @return       max_refresh_rate : Maximum refresh rate value
def get_max_RR():
    refresh_rate = []
    ##
    # Get current display configuration.
    current_config = config.get_current_display_configuration()
    NoOfDisplays = current_config.numberOfDisplays

    for index in range(NoOfDisplays):
        ##
        # Get current applied mode.
        current_mode = config.get_current_mode(current_config.displayPathInfo[index].targetId)
        refresh_rate.append(current_mode.refreshRate)
    max_refresh_rate = max(refresh_rate)
    return max_refresh_rate


##
# @brief        Helper function to get FPS pattern
# @param[in]    fpstype    : FPS in which app has to be run
# @return       fpspattern : FPS Pattern
def get_fps_pattern(fpstype):
    fpspattern = []
    refresh_rate = get_max_RR()
    if fpstype == FpsType.HIGH_FPS:
        x = ((1 / refresh_rate) * pow(10, 3)) - ((1 / refresh_rate) * pow(10, 3)) / 2
        y = ((1 / refresh_rate) * pow(10, 3)) - ((1 / refresh_rate) * pow(10, 3)) / 3
        fpspattern = [x, 1, y, 1, 100]
    elif fpstype == FpsType.LOW_FPS:
        x = ((1 / refresh_rate) * pow(10, 3)) + ((1 / refresh_rate) * pow(10, 3)) / 2
        y = ((1 / refresh_rate) * pow(10, 3)) + ((1 / refresh_rate) * pow(10, 3)) / 3
        fpspattern = [x, 1, y, 1, 100]
    elif fpstype == FpsType.MAX_FPS:
        # x = (1 / 1000) * pow(10, 3)
        fpspattern = [1, 1, 1, 1, 100, 1, 1, 1, 1, 100]
    return fpspattern


##
# @brief            Helper function to get failure statements
# @param[in]        feature        : Name of the feature
# @return           fail_statement : Statements of failure for matched features
def fail_statements(feature):
    fail_statement = {
        'ASYNCFLIPS': "Async Flips are not present",
        'SPEEDFRAME': "Speed frame is not enabled: Async flips are seen",
        'VSYNC_OFF': "Async Flips are not present",
        'VSYNC_ON': "Sync Flips are not present",
        'SMOOTH_SYNC': "Smooth Sync verification failed",
        'ENDURANCE_GAMING': 'FPS is not limited according to EG mode'
    }
    return fail_statement.get(feature.upper(), "Feature not found")


##
# @brief            Helper function to report GDHM
# @param[in]        feature    : Async flips related feature
# @param[in]        message    : GDHM message
# @param[in]        priority   : Priority of the GDHM bug [P1/P2/P3/P4]
# @param[in]        driver_bug : True for driver bug reporting else False
# @return           None
def report_to_gdhm(feature, message="", priority='P2', driver_bug=True):
    if message == "":
        if feature == "ASYNCFLIPS":
            title = f"[Display_OS_Features][Display_Flips][{feature}] verification failed"
        else:
            title = f"[Display_OS_Features][Gaming_Features][{feature}] verification failed"
    else:
        if feature == "ASYNCFLIPS":
            title = f"[Display_OS_Features][Display_Flips][{feature}] {message}"
        else:
            title = f"[Display_OS_Features][Gaming_Features][{feature}] {message}"
    if driver_bug:
        gdhm.report_driver_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
    else:
        gdhm.report_test_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))


##
# @brief            Helper function to scale to full screen
# @param[in]        bfullscreen : Mode in which application has to be launched
# @param[in]        app         : Name of the app
# @return           None
def fullscreen(bfullscreen, app):
    time.sleep(5)
    if bfullscreen:
        if app.upper() == 'FLIPAT' or app.upper() == 'RECTANGLE':
            winkb_helper.press(' ')
            time.sleep(2)
        if app.upper() == 'FLIPMODELD3D12' or app.upper() == 'TRIVFLIP':
            winkb_helper.press('F11')
            time.sleep(2)
        if app.upper() == 'CLASSICD3D':
            winkb_helper.press('F5')
            time.sleep(2)
        if app.upper() == 'DOTA':
            winkb_helper.press(' ')
            time.sleep(2)
        if app.upper() == 'CONTROL':
            winkb_helper.press('F11')
            time.sleep(2)
        if app.upper() == 'GTA':
            winkb_helper.press('F5')
            time.sleep(2)
    else:
        pass


##
# @brief        Helper function to close app function
# @param[in]    app : Name of the application
# @return       None
def close_app(app):
    dxflip_base.app.terminate()
    ##
    # To disable developer mode and flips
    if app == "FLIPMODELD3D12" or app == "CONTROL":
        enable_disable_developer_mode(RegistryStatus.DISABLE)
        enable_disable_flip_true_immediate_flips(RegistryStatus.DISABLE)


##
# @brief        Helper function to toggle Vsync for different apps
# @param[in]    app       : Name of the application
# @param[in]    iteration : Iteration count
# @return       None
def toggle_vsync(app, iteration):
    if app == "FLIPAT" or app == "DOTA":
        winkb_helper.press('V')
        logging.info(f"Toggled to Vsync {'on' if iteration % 2 == 0 else 'off'}")

    if app == "FLIPMODELD3D12" or app == "CONTROL":
        winkb_helper.press('CTRL+K')
        logging.info(f"Toggled to Vsync {'on' if iteration % 2 == 0 else 'off'}")


##
# @brief           Helper function to simulate FlipAt app for different FPS
# @param[in]       fps
# @return          None
def setFps(fps):
    if fps == "HIGHFPS":
        fps_pattern_high = get_fps_pattern(FpsType.HIGH_FPS)
        return fps_pattern_high, None

    elif fps == "LOWFPS":
        fps_pattern_low = get_fps_pattern(FpsType.LOW_FPS)
        return fps_pattern_low, None

    elif fps == "MAX_FPS":
        fps_pattern_max = get_fps_pattern(FpsType.MAX_FPS)
        return fps_pattern_max, None

    else:
        fps_pattern_high = get_fps_pattern(FpsType.HIGH_FPS)
        fps_pattern_low = get_fps_pattern(FpsType.LOW_FPS)
        return fps_pattern_high, fps_pattern_low


##
# @brief        Helper function to switch between AC/DC mode
# @param[in]    flag : True for DC and False for AC mode
# @return       None
def ac_dc_switch(flag):
    display_power = DisplayPower()
    display_power.enable_disable_simulated_battery(flag)
    power_type = PowerSource.DC if flag is True else PowerSource.AC

    if display_power.set_current_powerline_status(power_type) is False:
        report_to_gdhm("ASYNCFLIPS", f"Failed to set the power line status to {'DC' if flag is True else 'AC'}",
                       driver_bug=False)
        return False
    else:
        return True


##
# @brief        Helper function to get IO bandwidth
# @return       io_requests_bw : I/O bandwidth
def get_io_bandwidth_using_socwatch():
    io_requests_bw = 0.0

    ##
    # Run SocWatch for "duration" seconds (-t duration), capture starts after 5 seconds (-s 5)
    # and polling happens for every 1000ms (--polling -n 1000)
    soc_command = "socwatch --polling -n 1000 -t 180 -s 5 -f sys"
    result = socwatch.run_socwatch(SOC_WATCH_PATH, soc_command)
    if result:
        soc_logfile_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")
        result, soc_output = socwatch.parse_socwatch_output(soc_logfile_path)
        if result:
            io_requests_bw = soc_output[socwatch.SocWatchFields.IO_REQUESTS]
            logging.debug("IO Request Memory Bandwidth in PSR: %s", io_requests_bw)
        else:
            report_to_gdhm("ASYNCFLIPS", "Failed to parse SocWatch Logs", driver_bug=False)
            logging.error("Aborting the test as SocWatch log parse is failed")
    else:
        report_to_gdhm("ASYNCFLIPS", "Failed to run SocWatch Logs", driver_bug=False)
        logging.error("Aborting the test as running the SocWatch failed")
    return io_requests_bw


##
# @brief            Helper function get async flip feature
# @param[in]        async_feature : Async Flip Features
# @return           Feature value
def get_async_feature_value(async_feature):
    feature = {
        "APPLICATION_DEFAULT": control_api_args.CTL_BIT(0),
        "VSYNC_OFF": control_api_args.CTL_BIT(1),
        "VSYNC_ON": control_api_args.CTL_BIT(2),
        "SMOOTH_SYNC": control_api_args.CTL_BIT(3),
        "SPEEDFRAME": control_api_args.CTL_BIT(4),
        "CAPPED_FPS": control_api_args.CTL_BIT(5)
    }
    return feature.get(async_feature.upper(), "Feature not found")


##
# @brief            Helper function to get app name
# @param[in]        app_name : Name of the App
# @return           Complete Name of the Application
def get_app_name(app_name):
    app = {
        "FLIPAT": "FlipAt.exe",
        "FLIPMODELD3D12": "FlipModelD3D12.exe",
        "CLASSICD3D": "Classic3DCubeApp.exe",
        "TRIVFLIP": "TrivFlip11.exe",
        "GLOBAL": "",
        "DOTA": "dota2.exe",
        "GTA": "gta5.exe",
        "CONTROL": "control_dx12.exe"
    }
    return app.get(app_name.upper(), "Application Name not found")


##
# @brief            Helper function to Gaming Sync Mode
# @param[in]        gaming_sync_mode : Name of the Gaming Sync Mode
# @return           Complete Name of the Gaming Sync Mode
def get_gaming_sync_mode_name(gaming_sync_mode):
    sync_mode = {
        'INVALID': 'DD_GAMING_SYNC_MODE_INVALID',
        'APPLICATION_DEFAULT': 'DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT',
        'VSYNC_OFF': 'DD_GAMING_SYNC_MODE_VSYNC_OFF',
        'VSYNC_ON': 'DD_GAMING_SYNC_MODE_VSYNC_ON',
        'SMOOTH_SYNC': 'DD_GAMING_SYNC_MODE_SMOOTH_SYNC',
        'SPEED_FRAME': 'DD_GAMING_SYNC_MODE_SPEED_FRAME',
        'CAPPED_FPS': 'DD_GAMING_SYNC_MODE_CAPPED_FPS'
    }
    return sync_mode.get(gaming_sync_mode.upper(), "Gaming Sync Mode not available")


##
# @brief            Enable/disable Async Features through IGCL
# @param[in]        feature  : Name of Async Flip Feature
# @param[in]        panel    : Panel Info
# @param[in]        app_name : Name of the App
# @return           status   : True if operation is successful, else False
def enable_disable_asyncflip_feature(feature, panel, app_name='GLOBAL'):
    argsSet3DFeature = control_api_args.ctl_3d_feature_getset_t()
    argsSet3DFeature.bSet = True
    argsSet3DFeature.ApplicationName = get_app_name(app_name).encode()
    setFlipMode = get_async_feature_value(feature)
    logging.debug(f"App Name- {argsSet3DFeature.ApplicationName}")

    # Workaround to enable Speed Frame till feature is enabled by default in driver
    if feature == "SPEEDFRAME":
        enable_disable_speed_sync(RegistryStatus.ENABLE, panel)

    logging.info(f"Applying feature - {feature} for App - {app_name} with Flip mode - {setFlipMode}")
    if control_api_wrapper.get_set_gaming_flip_modes(argsSet3DFeature, setFlipMode, panel.target_id) is False:
        report_to_gdhm(feature, f"Failed to {'disable' if feature == 'APPLICATION_DEFAULT' else 'enable'} via IGCL")
        return False
    return True


##
# @brief            Helper Function to play any application
# @param[in]        app         : Name of the application
# @param[in]        fps         : None by default, otherwise(HIGHFPS/LOWFPS/HIGHLOWFPS)
# @param[in]        bfullscreen : True if fullscreen, otherwise False
# @param[in]        feature     : Feature passed from command line
# @return           etl file
def run_dx_app(app, fps, bfullscreen, feature=None):
    mode = "fullscreen" if bfullscreen else "windowed"
    logging.info(f"Opening App {app} in {mode} mode")

    # Minimize all windows
    winkb_helper.press('WIN+M')

    # Start ETL capture
    etl_file_name = "Before_fullscreen_scenario" if bfullscreen else "Before_windowed_scenario"
    if start_etl_capture(etl_file_name) is False:
        assert False, "FAIL: Failed to start GfxTrace"

    if app == "FLIPAT" or app == "DOTA":
        fps_pattern, fps_pattern2 = setFps(fps)
    else:
        fps_pattern = None
        fps_pattern2 = None

    # Open any app
    play_app(app, bfullscreen=bfullscreen, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)

    # App will run for one minute
    time.sleep(60)

    # Close the application
    close_app(app)

    logging.info(getStepInfo() + "Closed {0} App".format(app))

    # Stop ETL Trace
    etl_file_name = "After_fullscreen_scenario" if bfullscreen else "After_windowed_scenario"
    etl_file = stop_etl_capture(etl_file_name)

    if feature == "ENDURANCE_GAMING":
        global PRESENTMON_LOG_PATH

        # Minimize all windows
        winkb_helper.press('WIN+M')

        # play the app
        play_app(app, bfullscreen, fps_pattern, fps_pattern2)

        # capture the presentmon logs for 60 secs
        logging.info("Starting PresentMon capturing")
        PRESENTMON_LOG_PATH = start_presentmon_and_capture(app)
        logging.info("Stopping PresentMon capturing")
        if not PRESENTMON_LOG_PATH:
            logging.error("Failed to log from PresentMon !!")

        # close the app
        close_app(app)
    return etl_file


##
# @brief            Helper Function to play any application and start presentmon logging
# @param[in]        app         : Name of the application
# @return           log_file_path
def start_presentmon_and_capture(app):
    app_name = get_app_name(app)
    logging.info(f'App name: {app_name}')
    presentmon_path = os.path.join(PRESENTMON_APP, 'PresentMon-2.2.0-x64.exe')
    logging.info(f'Presentmon executable path: {presentmon_path}')
    log_start_time = round(time.time())
    log_path = os.path.join(test_context.LOG_FOLDER, f'presentmon_{log_start_time}.csv')
    logging.info(f'Presentmon logs path: {log_path}')
    time.sleep(3)
    process_output = subprocess.run(
        f'{presentmon_path} -process_name {app_name} -timed 60 -terminate_after_timed -output_file {log_path}')

    if process_output.returncode != 0:
        logging.error(f'Process exited with code {process_output.returncode}.')
        return
    return log_path


##
# @brief            Helper function to get EG control values
# @param[in]        eg_control : EG control string
# @return           EG control value for passed command line parameter
def get_eg_control_value(eg_control):
    return {
        'TURN_OFF': 0,
        'TURN_ON': 1,
        'AUTO': 2
    }[eg_control]


##
# @brief            Helper function to get EG mode values
# @param[in]        eg_mode : EG mode string
# @return           EG control value for passed command line parameter
def get_eg_mode_value(eg_mode):
    return {
        'BETTER_PERFORMANCE': 0,
        'BALANCED': 1,
        'MAXIMUM_BATTERY': 2
    }[eg_mode]


##
# @brief        Helper function to enable/disable EG
# @param[in]    eg_control : EG Control Flag to determine Feature ON/OFF/Auto controls
# @param[in]    eg_mode    : EG Mode Flag to determine mode to be enabled Balanced/Maximum Battery/Better Performance
# @return       status     : True if Endurance Gaming is successfully enabled/disabled else False
def enable_disable_endurance_gaming(eg_control, eg_mode):
    enumerated_displays = config.get_enumerated_display_info()
    display_details_list = TestBase.context_args.test.cmd_params.display_details

    ##
    # 3D Feature set args
    argsSet3DFeature = control_api_args.ctl_3d_feature_getset_t()
    argsSet3DFeature.bSet = True

    setEnduranceGamingArgs = control_api_args.ctl_endurance_gaming_t()
    setEnduranceGamingArgs.EGControl = get_eg_control_value(eg_control)
    setEnduranceGamingArgs.EGMode = get_eg_mode_value(eg_mode)

    logging.info("EG Control {} EG Mode {}".format(setEnduranceGamingArgs.EGControl, setEnduranceGamingArgs.EGMode))

    for display_index in range(len(display_details_list)):
        targetid = config.get_target_id(display_details_list[display_index].connector_port,
                                        enumerated_displays)
        logging.info("Set Endurance Gaming via Control Library")
        if control_api_wrapper.get_set_endurance_gaming(argsSet3DFeature, setEnduranceGamingArgs, targetid):
            logging.info("Pass:  Set Endurance Gaming via Control Library")
        else:
            logging.error("Fail: Set Endurance Gaming via Control Library")
            return False

    getEnduranceGamingArgs = control_api_args.ctl_endurance_gaming_t()
    argsGet3DFeature = control_api_args.ctl_3d_feature_getset_t()
    argsGet3DFeature.bSet = False

    for display_index in range(len(display_details_list)):
        targetid = config.get_target_id(display_details_list[display_index].connector_port,
                                        enumerated_displays)
        logging.info("Get Endurance Gaming via Control Library")
        if control_api_wrapper.get_set_endurance_gaming(argsGet3DFeature, getEnduranceGamingArgs, targetid):
            logging.info("Pass:  Get Endurance Gaming via Control Library")
        else:
            logging.error("Fail: Get Endurance Gaming via Control Library")
            return False

    return True


##
# @brief        Helper function to enable/disable EG
# @param[in]    eg_control : EG Control Flag to determine Feature ON/OFF/Auto controls
# @param[in]    eg_mode    : EG Mode Flag to determine mode to be enabled Balanced/Maximum Battery/Better Performance
# @return       status     : True if Endurance Gaming is successfully enabled/disabled else False
def enable_disable_endurance_gaming_registry(eg_control, eg_mode):
    # setting endurance gaming using control api
    enumerated_displays = config.get_enumerated_display_info()
    display_details_list = TestBase.context_args.test.cmd_params.display_details

    argsSet3DFeature = control_api_args.ctl_3d_feature_getset_t()
    argsSet3DFeature.bSet = True

    setEnduranceGamingArgs = control_api_args.ctl_endurance_gaming_t()
    setEnduranceGamingArgs.EGControl = get_eg_control_value(eg_control)
    setEnduranceGamingArgs.EGMode = get_eg_mode_value(eg_mode)

    logging.info("EG Control {} EG Mode {}".format(setEnduranceGamingArgs.EGControl, setEnduranceGamingArgs.EGMode))

    for display_index in range(len(display_details_list)):
        target_id = config.get_target_id(display_details_list[display_index].connector_port,
                                        enumerated_displays)
        logging.info("Get Endurance Gaming via Control Library")
        if control_api_wrapper.get_set_endurance_gaming(argsSet3DFeature, setEnduranceGamingArgs, target_id):
            logging.info("Pass:  Get Endurance Gaming via Control Library")
        else:
            logging.error("Fail: Get Endurance Gaming via Control Library")
            return False

    return True


##
# @brief        Helper function to setup registry for endurance gaming
# @param[in]    set_key : true if needs to set the EG registry key
# @return       boolean     : True if Endurance Gaming is successfully enabled/disabled else False
def eg_registry_setup(set_key):
    legacy_registry_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                         reg_path=INTEL_GMM_PATH)
    if set_key:
        if registry_access.write(args=legacy_registry_args, sub_key="EG", reg_name="EGSoCThrottling",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=1) is False:
            return False
        logging.info('Successfully created EGSoCThrottling Registry Key')
    else:
        if registry_access.delete(args=legacy_registry_args, sub_key="EG", reg_name="EGSoCThrottling") is False:
            return False
        logging.info('Successfully deleted EGSoCThrottling Registry Key')

    # Driver restart
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("Failed to restart display driver")
        return False
    logging.info("Driver restarted successful")
    return True


##
# @brief        Helper function to setup registry for endurance gaming
# @param[in]    display_pwr : Display_power passed from dxflips_base class
# @param[in]    ac_to_dc : toggles from AC to DC battery if true
# @param[in]    dc_to_ac : toggles from DC to AC battery if true
# @return       boolean     : true if toggled battery mode successfully
def toggle_battery(display_pwr, ac_to_dc=False, dc_to_ac=False):
    logging.info("Enabling Simulated Battery")
    if display_pwr.enable_disable_simulated_battery(True) is False:
        logging.error("Failed to enable Simulated Battery")
        return False
    logging.info("PASS: Enabled Simulated Battery successfully")
    if ac_to_dc:
        if display_pwr.set_current_powerline_status(display_power.PowerSource.DC) is False:
            return False
        return True
    if dc_to_ac:
        if display_pwr.set_current_powerline_status(display_power.PowerSource.AC) is False:
            return False
        return True