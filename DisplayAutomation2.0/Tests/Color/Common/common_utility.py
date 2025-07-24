#######################################################################################################################
# @file         common_utility.py
# @brief        This script contains common functions that will be used by Color test scripts.
#               Exposed common functions:
# 				1)gdhm_report_app_color()
# 				2)invoke_power_event()
# 				3)plug_unplug()
# 				4)get_modelist_subset()
# 				5)read_registry()
# 				6)write_registry()
# 				7)invoke_monitor_turnoffon()
# 				8)launch_overlay()
# 				9)launch_videoplayback()
# 				10)apply_mode()
# 				11)get_color_conversion_block()
# 				12)get_bpc_from_pixel_format()
#               13)get_bit_value()
#               14)restart_display_driver()
#               15)display_switch()
#               16)set_bpc_registry()
#               17)perform_plane_processing
#               18)get_action_type
#               19)enable_lace_in_vbt
#               20)disable_lace_in_vbt
# @author       Vimalesh D
#######################################################################################################################
import ctypes
import logging
import os, sys
import math
import subprocess
import time
from operator import attrgetter

from DisplayRegs import NonAutoGenRegs
from Libs.Core import enum, window_helper, display_power, display_utility, flip, winkb_helper, \
    registry_access, display_essential
from Libs.Core.display_config import display_config, display_config_enums
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.registry_access import RegDataType
from Libs.Core.wrapper import control_api_args, control_api_wrapper

from Tests.Color.Common import color_mmio_interface
from Tests.Color.Common.color_enums import SamplingMode
from Tests.Color import Common
from Tests.Color.Features.Concurrency import concurrency_utility
from Tests.PowerCons.Modules import windows_brightness, dpcd, polling


##
# @brief        Helper function to call GDHM API to report bug
# @param[in]    title - HSD bug title
# @param[in]    component from Component class
# @param[in]    problem_classification  from ProblemClassification class
# @param[in]    priority from Priority class
# @param[in]    exposure  from Exposure class
# @return       None



def gdhm_report_app_color(title="[COLOR]bug", component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                          problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                          priority=gdhm.Priority.P2, exposure=gdhm.Exposure.E2):
    gdhm.report_bug(
        title="[COLOR]" + title,
        problem_classification=problem_classification,
        component=component,
        priority=priority,
        exposure=exposure
    )


##
# @brief        Helper function to invoke power events
# @param[in]    event - PowerEvent CS/S3/S4
# @return       True or False
def invoke_power_event(event: display_power.PowerEvent) -> bool:
    status = False
    delay = 30
    display_power_ = display_power.DisplayPower()
    is_cs_supported = display_power_.is_power_state_supported(display_power.PowerEvent.CS)
    if event == display_power.PowerEvent.CS and not is_cs_supported:
        event = display_power.PowerEvent.S3
        logging.info("System does not support CS; hence invoking S3 state")
    elif event == display_power.PowerEvent.S3 and is_cs_supported:
        event = display_power.PowerEvent.CS
        logging.info("System does not support S3; hence invoking CS state")

    logging.info("Invoking POWER_STATE event {0}".format(event.name))

    # Adding 60 seconds delay for power event CS
    if event == display_power.PowerEvent.CS:
        delay = 60
    if not display_power_.invoke_power_event(event, delay):
        logging.error("FAIL : Power Event: {0} FAILURE".format(event.name))
    else:
        logging.info("Power Event :{0}  SUCCESS".format(event.name))
        status = True
    return status


##
# @brief        Helper function to get modelist
# @param[in]    display_and_adapterInfo - display_and_adapterInfo - Target ID and Complete Adapter ID details
# @param[in]    no_of_modes - No of modes for display
# @param[in]    expected_scaling - CI, FS, MAR, CAR, MDS
# @return       subset_modelist - modedict
def get_modelist_subset(display_and_adapterInfo: DisplayAndAdapterInfo, no_of_modes: int,
                        expected_scaling: int = enum.MDS, refresh_rate: int = None, hzres: int = None, vtres: int = None):
    mode_list = []
    display_config_ = display_config.DisplayConfiguration()
    all_supported_modes = display_config_.get_all_supported_modes(
        [display_and_adapterInfo])

    for keys, modes in all_supported_modes.items():
        modes = sorted(modes, key=attrgetter('HzRes'), reverse=True)
        if no_of_modes == 1 and expected_scaling == enum.MDS and refresh_rate is None:
            mode_list.append(modes[0])  # Max/Native
            break
        if no_of_modes == 2 and expected_scaling == enum.MDS and refresh_rate is None:
            mode_list.append(modes[0])  # Max
            mode_list.append(modes[-1])  # Min
            break

        if no_of_modes == -1 and expected_scaling == -1:
            for mode in modes:
                if mode.HzRes == hzres and mode.VtRes == vtres:
                    mode_list.append(mode)
            return mode_list

        for mode in modes:
            if mode.scaling == expected_scaling:
                mode_list.append(mode)
                if no_of_modes == len(mode_list):
                    break
            if mode.refreshRate == refresh_rate:
                mode_list.append(mode)
                if no_of_modes == len(mode_list):
                    break
    if len(mode_list) < 1:
        return None
    return mode_list


##
# @brief      Helper function to apply mode based on adapter and display and verify with mode
#              If HzRes,VtRes ,RR , Scaling is passed that mode is applied otehrwise native mode is applied
# @param[in]  display_and_adapterInfo - display_and_adapterInfo info
# @param[in]  hzres - hresolution
# @param[in]  vtres - vresolution
# @param[in]  rr - resolution
# @param[in]  scaling - CI, FS, MAR, CAR, MDS
# @param[in]  sampling_mode - RGB or YUV420
# @return     status True or False
def apply_mode(display_and_adapterInfo: DisplayAndAdapterInfo, hzres: int = None, vtres: int = None, rr: int = None,
               scaling: int = None, sampling_mode: int = SamplingMode.RGB.value):
    status = False
    config = display_config.DisplayConfiguration()
    mode = config.get_current_mode(display_and_adapterInfo)
    supported_modes = config.get_all_supported_modes([display_and_adapterInfo.TargetID])

    if hzres is None:
        native_mode = config.get_native_mode(display_and_adapterInfo.TargetID)
        if native_mode is None:
            logging.error(f"Failed to get native mode for {display_and_adapterInfo.TargetID}")
            return False
        hzres = native_mode.hActive
        vtres = native_mode.vActive
        rr = native_mode.refreshRate
        scaling = enum.MDS

    if sampling_mode == SamplingMode.YUV420.value:
        for key, modes in supported_modes.items():
            # do reverse and apply samplingmode instead of native mode
            modes = sorted(modes, key=attrgetter('HzRes'), reverse=True)
            for mode in modes:
                if mode.samplingMode.Value == 2:  # Sampling Mode (1 - RGB, 2 - YUV420)
                    logging.info("Applying YUV Mode")
                    break
    else:
        logging.info("Applying native mode")
        mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling = hzres, vtres, rr, scaling

    result = config.set_display_mode([mode])

    if result:
        current_mode = config.get_current_mode(display_and_adapterInfo)
        if (current_mode.HzRes == mode.HzRes and current_mode.VtRes == mode.VtRes and
                current_mode.refreshRate == mode.refreshRate and current_mode.scaling == mode.scaling):
            logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3}".format(
                current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
            status = True
    return status


##
# @brief      Helper function to get the current mode based on adapter and display
# @param[in]  display_and_adapterInfo - display_and_adapterInfo info
# @return     current_mode - DisplayMode()
def get_current_mode(display_and_adapterInfo: DisplayAndAdapterInfo):
    config = display_config.DisplayConfiguration()
    current_mode = config.get_current_mode(display_and_adapterInfo)
    return current_mode


##
# @brief        Helper function to read registry
# @param[in]    gfx_index - gfx_0 or gfx_1
# @param[in]    reg_hkey_path - path of the registry
# @param[in]    sub_key -  sub-key of the registry path - ex: "igfxcui\MISC"
# @param[in]    reg_name -  name of the registry
# @return       status, reg_value
def read_registry(gfx_index: str, reg_name: str, reg_hkey_path: registry_access.HKey = None,
                  sub_key: str = None):
    status = False
    if reg_hkey_path is not None and sub_key is not None:
        reg_args = registry_access.LegacyRegArgs(hkey=reg_hkey_path, reg_path=sub_key)
    else:
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

    value, reg_type = registry_access.read(args=reg_args, reg_name=reg_name, sub_key=sub_key)

    if reg_type is None:
        value = 0
        logging.info("Read Registry : {0} is not present in the reg key path".format(reg_name))
        return status, value
    if value is None and reg_type is not None:
        logging.info(" Read Registry : {0} , Value :NONE".format(reg_name))
        return status, value
    if registry_access.RegDataType(reg_type).name == "BINARY":
        reg_value = int.from_bytes(value, byteorder="little")
    else:
        reg_value = value
    status = True
    logging.info("Read Registry : {0} , Value : {1}".format(reg_name, value))
    return status, reg_value


##
# @brief        set_bpc_registry() to set bpc value and if passed restart display driver
# @param[in]    gfx_index - gfx adapter index
# @param[in]    display_and_adapterinfo - DisplayAndAdapterInfo Struct of the display
# @param[in] -  bpc - values as 8/10/12
# @return      True -On Success,False -On Failure
def set_bpc_registry(gfx_index: str, display_and_adapterinfo, bpc: int = 8):
    if write_registry(gfx_index=gfx_index, reg_name="SelectBPCFromRegistry",
                      reg_datatype=registry_access.RegDataType.DWORD, reg_value=bpc,
                      display_and_adapterInfo=display_and_adapterinfo,driver_restart_required=True) is False:
        return False
    if write_registry(gfx_index=gfx_index, reg_name="SelectBPC",
                      reg_datatype=registry_access.RegDataType.DWORD, reg_value=1,
                      driver_restart_required=True) is False:
        return False
    return True


def delete_registry(adapter, reg_name):
    logging.info("Deleting Registry Key {0} from {1}".format(reg_name, adapter))
    reg_args = registry_access.StateSeparationRegArgs(gfx_index=adapter)
    status = registry_access.delete(args=reg_args, reg_name=reg_name)
    if status is False:
        logging.error("FAIL: : Delete Registry Key {0} failed".format(reg_name))
    logging.info("PASS : Delete Registry Key {0}success".format(reg_name))
    return status

##
# @brief        Helper function to write registry
# @param[in]    gfx_index - gfx_0 or gfx_1
# @param[in]    reg_hkey_path - path of the registry
# @param[in]    sub_key -  sub-key of the registry path - ex: "igfxcui\MISC"
# @param[in]    reg_name -  name of the registry
# @param[in]    reg_value - registry value
# @param[in]    reg_datatype -  DWORD/BINARY/QWORD
# @param[in]    driver_restart_required - True or False
# @param[in]    display_and_adapterInfo - display_and_adapterInfo info
# @return       status True or False
def write_registry(gfx_index: str, reg_name: str, reg_value: any, reg_datatype: RegDataType,
                   reg_hkey_path: registry_access.HKey = None, sub_key: str = None,
                   driver_restart_required: bool = None, display_and_adapterInfo=None):
    if reg_hkey_path is not None and sub_key is not None:
        reg_args = registry_access.LegacyRegArgs(hkey=reg_hkey_path, reg_path=sub_key)
    else:
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

    status = registry_access.write(args=reg_args, reg_name=reg_name, reg_type=reg_datatype,
                                   reg_value=reg_value)
    if status:
        logging.info("PASS : Write Registry - {0} ,Value : {1}".format(reg_name, reg_value))
        if driver_restart_required:
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                logging.error('Failed to Restart Display driver')
                status = False
                return status
            logging.info('Display driver restarted successfully')
        else:
            logging.info("Applying modeset if restart display driver not required")
            if apply_mode(display_and_adapterInfo) is False:
                logging.error("FAIL : Modeset after write registry failed")
                status = False
                return status

        logging.info("Reading registry back after write registry")
        status, read_reg_value = read_registry(gfx_index, reg_name, reg_hkey_path, sub_key)
        if read_reg_value == reg_value:
            logging.info("Registry_name: {0} Expected : {1} Actual : {2}".format(reg_name, read_reg_value, reg_value))
            status = True
        else:
            logging.error(
                "Registry_name: {0} Expected : {1} Actual : {2}".format(reg_name, read_reg_value, reg_value))
            gdhm.report_driver_bug_os(
                "Register {0} verification failed - Expected : {1} Actual : {2}".format(reg_name, read_reg_value,
                                                                                        reg_value))
            status = False
    else:
        logging.error("FAIL : Write Registry - Regname: {0} ,Value : {1}".format(reg_name, reg_value))
        gdhm.report_driver_bug_di("Registry {0} Write Failed - Value: {1}".format(reg_name, reg_value))
    return status


##
# @brief        Helper function to Turn Off/On Monitor
# @return       status True or False
# @todo          Need to remove the enum import
def invoke_monitor_turnoffon():
    status = False
    logging.info("Invoking Monitor Turn OFF")
    display_power_ = display_power.DisplayPower()
    is_cs_supported = display_power_.is_power_state_supported(display_power.PowerEvent.CS)
    if not is_cs_supported:
        if display_power_.invoke_monitor_turnoff(display_power.MonitorPower.OFF_ON, 5) is False:
            logging.error("Failed to Turned OFF_ON Monitors")
        else:
            logging.info("Successfully turned OFF_ON Monitors")
            status = True
    else:
        logging.info(
            "Monitor turnoff does not work in connected standby enabled system,hence skipping monitor turnoff_on event")
        status = True

    return status


##
# @brief        Helper function to launch overlay application
# @return        status, app True or False
def launch_overlay():
    status = False
    app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                           cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
    if not app:
        logging.error("Failed to launch overlay application")
    else:
        logging.info("Successfully launched overlay application")
        status = True
    return status, app


##
# @brief        Helper function to launch and perform video playback scenario
# @param[in]    video_file_path - HDR Video file path
# @param[in]    fullscreen - True or False
# @return        status True or False
def launch_videoplayback(video_file_path: str, fullscreen: bool = True):
    status = False
    ##
    # Close any previously opened media player
    window_helper.close_media_player()
    ##
    # Minimize all windows before opening media player
    window_helper.minimize_all_windows()
    window_helper.open_uri(video_file_path)
    time.sleep(5)
    media_window_handle = window_helper.get_window('Movies & TV', True) is None or (window_helper.get_window
                                                                                    ('Films & TV', True)) is None
    if media_window_handle:
        if fullscreen:
            ##
            # Media player opened in windowed mode, put it to full screen mode
            logging.debug("Changing  media player to Fullscreen mode")
            window_helper.press("ALT_ENTER")
            winkb_helper.press(' ')  # Pause the video
            time.sleep(5)
            winkb_helper.press(' ')  # Play the video
            time.sleep(10)
        else:
            # currently in FullScreen Mode. Change to Windowed mode
            logging.debug("Changing media player to Windowed mode")
            window_helper.press('ESC')
            window_helper.press('ESC')
            winkb_helper.press(' ')  # Pause the video
            time.sleep(5)
            winkb_helper.press(' ')  # Play the video
            time.sleep(10)
        window_helper.close_media_player()
    else:
        title = "Failed to launch VideoPlayback application"
        logging.error("FAIL :" + title)
        gdhm_report_app_color(title=title)
        return status
    return True


##
# @brief      Get bpp from pixel format
# @param[in]  pixel_format -  value
# @return      bpc -  value
def get_bpc_from_pixel_format(pixel_format: int):
    bpc = 8
    if ((pixel_format >= flip.SB_PIXELFORMAT.SB_8BPP_INDEXED) and (
            pixel_format < flip.SB_PIXELFORMAT.SB_R10G10B10X2)):
        bpc = 8
    elif ((pixel_format >= flip.SB_PIXELFORMAT.SB_R10G10B10X2) and (
            pixel_format < flip.SB_PIXELFORMAT.SB_R16G16B16X16F)):
        bpc = 10
    elif ((pixel_format >= flip.SB_PIXELFORMAT.SB_R16G16B16X16F) and (
            pixel_format < flip.SB_PIXELFORMAT.SB_MAX_PIXELFORMAT)):
        bpc = 16
    elif (pixel_format in (
            flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_YUV422, flip.SB_PIXELFORMAT.SB_YUV444_8)):
        bpc = 8
    elif (pixel_format in (
            flip.SB_PIXELFORMAT.SB_P010YUV420, flip.SB_PIXELFORMAT.SB_YUV422_10, flip.SB_PIXELFORMAT.SB_YUV444_10)):
        bpc = 10
    elif (pixel_format in (
            flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_YUV422_12, flip.SB_PIXELFORMAT.SB_YUV444_12)):
        bpc = 12
    elif (pixel_format in (
            flip.SB_PIXELFORMAT.SB_P016YUV420, flip.SB_PIXELFORMAT.SB_YUV422_16, flip.SB_PIXELFORMAT.SB_YUV444_16)):
        bpc = 16

    return bpc


##
# @brief         Function to get the specified bit range value
# @param[in]     value - gfx adapter index
# @param[in]     start - bit position
# @param[in]     end - bit position
# @return        retvalue
def get_bit_value(value: int, start: int, end: int):
    retvalue = value << (31 - end) & 0xffffffff
    retvalue = retvalue >> (31 - end + start) & 0xffffffff
    return retvalue


##
# @brief         Function to disable and enable driver
# @param[in]     gfx_index - gfx adapter index
# @return        disable_status and enable_status as 0 or 1
def restart_display_driver(gfx_index: str):
    status, reboot_required = display_essential.restart_gfx_driver()
    return status, reboot_required


##
# @brief       display_switch() Perform display_switching across display for Single/Clone/Extended
# @param[in]   topology -i.e Single/Clone/Extended
# @param[in]   display_and_adapter_info_list -i.e [EDP/HDMI/DP]
# @return      True -On Success,False -On Failure
def display_switch(topology, display_and_adapter_info_list):
    config = display_config.DisplayConfiguration()
    return bool(config.set_display_configuration_ex(topology, display_and_adapter_info_list))


##
# @brief        Helper function to apply the requested power mode
# @param[in]    Power Source enum
# @return       Boolean - True if the action is successful; else False
def apply_power_mode(power_line_state: display_power.PowerSource):
    disp_power = display_power.DisplayPower()
    ##
    # Enable Simulated Battery
    if disp_power.enable_disable_simulated_battery(True) is False:
        logging.error("Failed to enable simulated battery")
        return False
    logging.debug("Successfully enabled simulated battery")
    if power_line_state == display_power.PowerSource.AC or power_line_state == display_power.PowerSource.DC:
        if disp_power.set_current_powerline_status(power_line_state) is False:
            logging.error("Failed to switch power line status")
            return False
        return True
    else:
        logging.error("Invalid PowerLine State")
        return False


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
    time.sleep(5)
    logging.info("Successfully set OS_brightness slider level to {0}".format(brightness_slider_value))
    # @todo - Identify why the GetBrightness() sporadically fails and uncomment the below code
    # current_brightness = windows_brightness.get_current_brightness()
    # if current_brightness != brightness_slider_value:
    #     logging.error("Failed to set OS_brightness slider level to {0}".format(brightness_slider_value))
    #     return False
    # else:
    #     logging.info("Successfully set OS_brightness slider level to {0}".format(brightness_slider_value))
    #     return True


##
# Get Color Conversion Block
def get_color_conversion_block(platform, current_pipe, feature='SDR'):
    ##
    # In case of SDR Mode, CC2 blocks are available only on Pipe A and B
    # Reverts to CC1 if any other pipe
    if feature in 'SDR' and current_pipe in ('A', 'B') and platform not in ('TGL', 'DG1', 'RKL', 'ADLS'):
        cc_block = "CC2"
    else:
        cc_block = "CC1"

    logging.info("CC Block is {0}".format(cc_block))
    return cc_block


##
# @brief perform_plane_processing
# @param[in] gfx_index
# @return None
def perform_plane_processing(gfx_index):
    logging.info("Performing plane processing")

    ##
    # These registers are used as scratch pad data storage space
    offset = NonAutoGenRegs.OFFSET_SWF_32.SWF_32
    value = 0x1
    color_mmio_interface.ColorMmioInterface().write(gfx_index, offset, value)


##
# @brief verify dc_state disable
# @return True on success or False on Failure
def verify_dc_state_disable():
    ## Verify DC state also disabled.
    # 0x45504 - DC State en offset and start polling
    # Before this PSR was already disabled.
    # start the polling and have delay and stop the polling and verify DC state
    polling.start([0x45504], 1)
    time.sleep(10) # Keep idle for 10 secs for enough breath for idle
    # Stop the polling and get the timeline
    polling_timeline, time_stamps = polling.stop()
    mmio_value = 0
    itr = 0
    for time_stamp in time_stamps:
        if time_stamp in time_stamps:
            itr+=1
            if itr < (len(time_stamps)-1):
                mmio_value = polling_timeline[0x45504][time_stamps.index(time_stamp)]
                if mmio_value is None:
                    continue
                if mmio_value == 1:
                    # dc5_states
                    logging.error("\tDC state value={0} (TimeStamp={1})".format(mmio_value,
                                                                                time_stamp))
                    return mmio_value
                elif mmio_value == 2:
                    # dc6_state
                    logging.error("\tDC state value={0} (TimeStamp={1})".format(mmio_value,
                                                                                time_stamp))
                    return mmio_value
                elif mmio_value == 3:
                    logging.error("\tDC state value={0} (TimeStamp={1})".format(mmio_value,
                                                                                time_stamp))
                    return mmio_value
            logging.info("\tDC state value={0} (TimeStamp={1})".format(mmio_value, time_stamp))
    return mmio_value


##
# @brief        To flip with the given input parameters
# @param[in]	planes Pointer to structure @ref _PLANE containing the plane info
# @return       Boolean,status of the flip
def perform_flip(planes, gfx_index):
    ##
    # Check for the hardware support for plane parameters
    logging.info("Invoking CheckMPO to verify if HW supports flipping of requested plane(s)")
    checkmpo_result = flip.MPO().check_mpo3(planes, gfx_index)
    if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
        logging.info("Flipping the planes and verifying the planes")
        ##
        # Flip the content
        ssa_result = flip.MPO().set_source_address_mpo3(planes)

        if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("Successfully flipped planes")
        elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            logging.error("Resource creation failed")
            gdhm.report_driver_bug_os(f"Resource creation failed during SetSourceAddressMPO3 for Adpater: {gfx_index}")
            return False
        else:
            logging.error("Set source address failed")
            return False
    elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
        logging.error("Resource creation failed")
        gdhm.report_driver_bug_os(f"Resource Creation failed during CheckMPO for Adpater: {gfx_index}")
        return False
    else:
        logging.error("Driver didn't meet the plane requirements !!")
        gdhm.report_driver_bug_os(f"Driver didn't meet the plane requirements for Adapter: {gfx_index}")
        return False
    return True


##
# @brief get_action_type
# @param[in] None
# @return argument value
def get_action_type():
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if '-SCENARIO' in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == '-SCENARIO':
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        assert False, "Wrong Commandline!! Usage: Test_name.py -SCENARIO SCENARIO_NAME -SAMPLING SAMPLING_TYPE"


def round_up_div(x, y):
    if x % y == 0:
        result = int(x / y)
    else:
        result = int(math.ceil((x) / (y)))
    return result


def get_psr_caps(target_id, feature_caps):
    edp_rev = dpcd.get_edp_revision(target_id)
    alpm_caps = dpcd.get(target_id, dpcd.Offsets.ALPM_CAP)
    feature_caps.PSRSupport = False
    feature_caps.PSRVersion = 0

    # Edp DPCD version
    if edp_rev == dpcd.EdpDpcdRevision.EDP_UNKNOWN:
        return feature_caps

    # Get eDP supported PSR version
    psr_ver = dpcd.get_psr_version(target_id)
    if psr_ver == dpcd.EdpPsrVersion.EDP_PSR_UNKNOWN:
        logging.error("\tFailed to get eDP PSR version")
        return feature_caps

    # PSR1 is supported only on eDP 1.3+ panels
    if (edp_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_3) and (psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_1):
        feature_caps.PSRSupport = True
        feature_caps.PSRVersion = 1
    # Get granularity support
    psr_capability = dpcd.PsrCapability(target_id)

    # PSR2 is supported only on eDP 1.4+ panels
    if edp_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4:
        if alpm_caps and (psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_2):
            feature_caps.PSRSupport = True
            feature_caps.PSRVersion = 2
    return feature_caps


def disable_lace_in_vbt(gfx_vbt, panel_index, gfx_index):
    gfx_vbt.block_44.LaceEnable[0] &= (0 << panel_index)
    gfx_vbt.block_44.LaceStatus[0] &= (0 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("\tGetting VBT_BLOCK_44 failed(Test Issue)")
    ##
    # Restarting driver to reflect changes
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver(Test Issue)")
        return False

    gfx_vbt.reload(adapter.gfx_index)
    return gfx_vbt


def enable_lace_in_vbt(gfx_vbt, panel_index, gfx_index):
    gfx_vbt.block_44.LaceEnable[0] &= (1 << panel_index)
    gfx_vbt.block_44.LaceStatus[0] &= (1 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("\tGetting VBT_BLOCK_44 failed(Test Issue)")
    ##
    # Restarting driver to reflect changes
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver(Test Issue)")
        return False

    gfx_vbt.reload(adapter.gfx_index)
    return gfx_vbt


def read_feature_status_in_vbt(gfx_vbt, feature, panel_index):
    initial_vbt_status = {"LACE": None, "ELP": None, "OPST": None, "DPST": None}
    if feature == 'LACE':
        lace_initial_status = (gfx_vbt.block_44.LaceStatus[0] & (1 << panel_index)) >> panel_index
        initial_vbt_status['LACE'] = bool(lace_initial_status)

    if feature == 'ELP' or feature == 'OPST':
        dpst_initial_status = (gfx_vbt.block_44.DpstEnable[0] & (1 << panel_index)) >> panel_index
        initial_vbt_status['DPST'] = bool(dpst_initial_status)
        logging.info("DPST Status in the VBT is {0}".format(bool(dpst_initial_status)))

        opst_initial_status = (gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index
        initial_vbt_status['OPST'] = bool(opst_initial_status)
        logging.info("OPST Status in the VBT is {0}".format(bool(opst_initial_status)))

        elp_initial_status = (gfx_vbt.block_44.ELP[0] & (1 << panel_index)) >> panel_index
        initial_vbt_status['ELP'] = bool(elp_initial_status)
        logging.info("ELP Status in the VBT is {0}".format(bool(elp_initial_status)))

        aggresiveness_profile2 = gfx_vbt.block_44.AgressivenessProfile2[panel_index]
        logging.info("AggressivenessLevel is {0}".format(aggresiveness_profile2))

        return initial_vbt_status


def update_color_feature_status_in_vbt(gfx_index, gfx_vbt, panel_index, feature, enable_status):
    if feature == 'LACE':
        if enable_status is False:
            logging.info("Disabling lace")
            gfx_vbt.block_44.LaceEnable[0] &= (0 << panel_index)
            gfx_vbt.block_44.LaceStatus[0] &= (0 << panel_index)
        else:
            logging.info("Enabling lace")
            gfx_vbt.block_44.LaceEnable[0] &= (1 << panel_index)
            gfx_vbt.block_44.LaceStatus[0] |= (1 << panel_index)

    if feature == 'ELP':
        if enable_status is False:
            gfx_vbt.block_44.ELP[0] &= (0 << panel_index)
        else:
            gfx_vbt.block_44.ELP[0] |= (1 << panel_index)

    if feature == 'OPST':
        if enable_status is False:
            gfx_vbt.block_44.OPST[0] &= (0 << panel_index)
        else:
            gfx_vbt.block_44.OPST[0] |= (1 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("Failed to update {0} feature changes in VBT".format(feature))
        return False

    logging.info("Successfully updated {0} feature changes in VBT".format(feature))
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver after VBT update")
        return False

    gfx_vbt.reload()
    return True


def toggle_psr_and_verify(gfx_index, platform, target_id, port, pipe, transcoder, enable: bool):
    from Tests.Color.Common import color_properties
    feature_caps = color_properties.FeatureCaps()
    feature_caps = get_psr_caps(target_id, feature_caps)
    if feature_caps.PSRSupport:
        ##
        # Disable the PSR
        if Common.color_igcl_escapes.enable_disable_psr_via_igcl(target_id, port, enable) is False:
            return False

        if Common.color_igcl_escapes.get_psr_status_via_igcl(target_id,enable) is False:
            return False

        time.sleep(2)
        ##
        # Verify PSR Feature is disabled
        is_psr2 = True if feature_caps.PSRVersion == 2 else False
        # DG2 Won't support PSR2
        if is_psr2 and (platform in "DG2"):
            return True
        # Based on expectation enable/Disable PSR and fail based on DC State
        concurrency_utility.verify_psr(gfx_index, platform, port, pipe, transcoder, is_psr2, enable)
        # Verify DC state disable
        dc_state_status = verify_dc_state_disable()
        if dc_state_status > 0 and enable is False:
            return False
        elif (dc_state_status < 0 or dc_state_status is None) and enable:
            return False
    return True
