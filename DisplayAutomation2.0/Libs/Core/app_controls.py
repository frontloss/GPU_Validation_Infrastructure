#######################################################################################################################
# @file         app_controls.py
# @brief        Contains APIs to control apps launched during test
# @author       Rohit Kumar, Patel, Ankurkumar G
#######################################################################################################################

import ctypes
import logging
import time

import win32com.client
from win32gui import EnumWindows, GetWindowText, GetClassName, MoveWindow

from Libs.Core import window_helper, registry_access
from Libs.Core import winkb_helper as kb
from enum import Enum

AFFINITY_REGISTRY_PATH = "Software\\Microsoft\\DirectX\\UserGpuPreferences"


##
# @brief        Rect structure
# @details      defines the coordinates of the upper-left and lower-right corners of a rectangle.
class Rect(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

    ##
    # @brief        String representation of rect object
    # @return       list - rect co-ordinates
    def to_string(self):
        return list(map(int, (self.left, self.top, self.right, self.bottom)))


##
# @brief        MonitorInfo Structure
class MonitorInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_ulong),
        ('rcMonitor', Rect),
        ('rcWork', Rect),
        ('dwFlags', ctypes.c_ulong)
    ]


##
# @brief        AffinityOption Enum
class AffinityOption(Enum):
    SYSTEM_DEFAULT = 0
    POWER_SAVING = 1
    HIGH_PERFORMANCE = 2


# Dictionary for all apps supported by get_affinity/set_affinity API
affinity_apps_dict = {
    'MTA': "Microsoft.ZuneVideo_8wekyb3d8bbwe!Microsoft.ZuneVideo",
    'D3D12Fullscreen': "C:\SHAREDBINARY\920697932\MPO\D3D12FullScreen\D3D12Fullscreen.exe"
}


##
# @brief        Exposed API to get enumerated display monitors
# @return       results - list of enumerated display monitors
def get_enumerated_display_monitors():
    ##
    # Prototype for callback
    monitor_enum_proc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(Rect),
                                           ctypes.c_double)
    results = []

    ##
    # @brief        Callback function. Will be called for each connected monitor.
    # @param[in]    monitor - Monitor ID
    # @param[in]    dc - device context handle
    # @param[in]    rect - rect object
    # @param[in]    data - Application defined data
    # @return       int - 1 on successful method execution
    def _callback(monitor, dc, rect, data):
        results.append([monitor, dc, rect, data])
        return 1

    callback = monitor_enum_proc(_callback)
    ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback, 0)
    return results


##
# @brief        Exposed API to get all the enumerated windows
# @return       results - list of enumerated windows
def __get_enumerated_windows():
    results = []

    ##
    # @brief        Callback function. Will be called for each window
    # @param[in]    hwnd - handle to a top-level window
    # @param[in]    data - application-defined value given in EnumWindows or EnumDesktopWindows
    # @return       None
    def _callback(hwnd, data):
        data.append((hwnd, GetWindowText(hwnd), GetClassName(hwnd)))

    EnumWindows(_callback, results)
    return results


##
# @brief        Exposed API to get monitor information
# @param[in]    monitor - target ID of panel
# @return       mi - MonitorInfo instance
def get_monitor_info(monitor):
    mi = MonitorInfo()
    mi.cbSize = ctypes.sizeof(MonitorInfo)
    mi.rcMonitor = Rect()
    mi.rcWork = Rect()
    ctypes.windll.user32.GetMonitorInfoA(monitor, ctypes.byref(mi))
    return mi


##
# @brief        Exposed API to move given window to given monitor
# @param[in]    target_window_title - window title
# @param[in]    target_monitor_id - target ID of panel
# @return       None
def move_windows(target_window_title, target_monitor_id):
    mi = get_monitor_info(target_monitor_id)
    master_w = None
    windows_list = __get_enumerated_windows()
    for wh, wn, wd in windows_list:
        if target_window_title in wn:
            master_w = wh
    MoveWindow(master_w, mi.rcMonitor.left, mi.rcMonitor.top, mi.rcMonitor.right - mi.rcMonitor.left,
               mi.rcMonitor.bottom - mi.rcMonitor.top, 1)
    time.sleep(1)


##
# @brief            Exposed API to launch video
# @param[in]        video_file - full path to video file to be launched
# @param[in]        is_full_screen - True to launch video in full screen, False to launch it in windowed mode
# @return           None
def launch_video(video_file, is_full_screen=True):
    trial = 1
    while trial <= 3:

        # Close any previously opened media player
        window_helper.close_media_player()

        # Minimize all windows before opening media player
        window_helper.minimize_all_windows()

        window_helper.open_uri(video_file)
        time.sleep(5)

        # WA for skipping the first run dialog box on RS4 onwards
        if window_helper.get_window('Let Movies & TV access your videos library?', True):
            logging.debug("Pop up is opened for media player, closing the same.")
            kb.press("ENTER")
            time.sleep(2)
        if is_full_screen:
            kb.press('ESC')
            time.sleep(5)
            kb.press('ESC')
            time.sleep(5)

        fullscreen_playback = window_helper.get_window('Movies & TV', True) is None and \
                              (window_helper.get_window('Films & TV', True)) is None and \
                              (window_helper.get_window('Media Player', True)) is None and \
                              (window_helper.get_window('Windows Media Player', True)) is None and \
                              (window_helper.get_window('Windows Media Player Legacy', True)) is None

        if is_full_screen:
            if not fullscreen_playback:
                # Media player opened in windowed mode, put it to full screen mode
                logging.debug("changing  media player to fullscreen mode")
                kb.press("ALT_ENTER")
                time.sleep(2)
        else:
            if fullscreen_playback:
                # currently in FullScreen Mode. Change to Windowed mode
                logging.debug("Changing player to Windowed mode")
                kb.press('ESC')
                kb.press('ESC')
        if is_full_screen:
            window_helper.mouse_left_click(400, 400)
            time.sleep(2)

        wmi = win32com.client.GetObject('winmgmts:')
        process_list = [p.Name for p in wmi.InstancesOf('win32_process')]
        if "Video.UI.exe" or "Media Player" or "wmplayer.exe" in process_list:
            logging.debug("Media player is running..")
            break
        trial += 1
        if trial == 3:
            logging.error("\tMedia player is NOT running even after multiple attempts (Test Issue)")

    logging.debug("\tVideo playback started successfully in {0} mode".format("FULL SCREEN" if is_full_screen
                                                                             else "WINDOWED"))


##
# @brief        Exposed API to get application affinity
# @param[in]    app_name - Name of the application
# @return       AffinityOption - affinity option enum or None if not supported
def get_affinity(app_name):
    if str(app_name) in affinity_apps_dict:
        key_name = affinity_apps_dict[app_name]
    else:
        logging.error("get_affinity API does not support %s application" % str(app_name))
        return None

    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, AFFINITY_REGISTRY_PATH)
    value, reg_type = registry_access.read(args=reg_args, reg_name=key_name)
    logging.debug("Registry read value is : %s" % str(value))
    if value is None and reg_type is None:
        return AffinityOption.SYSTEM_DEFAULT
    elif value == "GpuPreference=0;":
        return AffinityOption.SYSTEM_DEFAULT
    elif value == "GpuPreference=1;":
        return AffinityOption.POWER_SAVING
    elif value == "GpuPreference=2;":
        return AffinityOption.HIGH_PERFORMANCE
    else:
        return AffinityOption.SYSTEM_DEFAULT


##
# @brief        Exposed API to change application affinity
# @param[in]    app_name - Name of the application
# @param[in]    affinity - affinity option enum
# @return       bool - True if successful, False otherwise
def set_affinity(app_name, affinity):
    logging.debug("Setting application affinity to %s for application %s" % (str(affinity), str(app_name)))

    if str(app_name) in affinity_apps_dict:
        key_name = affinity_apps_dict[app_name]
    else:
        logging.error("set_affinity API does not support %s application" % str(app_name))
        return None

    if affinity == AffinityOption(AffinityOption.SYSTEM_DEFAULT):
        key_value = "GpuPreference=0;"
    elif affinity == AffinityOption(AffinityOption.POWER_SAVING):
        key_value = "GpuPreference=1;"
    elif affinity == AffinityOption(AffinityOption.HIGH_PERFORMANCE):
        key_value = "GpuPreference=2;"
    else:
        logging.error("Invalid affinity option provided")
        return False

    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, AFFINITY_REGISTRY_PATH)
    status = registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.SZ,
                                   reg_value=key_name)
    logging.debug("Registry write value is: %s" % str(key_value))

    if status is True:
        logging.debug(
            "Application affinity is successfully set to %s for application %s" % (str(affinity), str(app_name)))
        return True
    else:
        logging.error(
            "Application affinity is failed to set to %s for application %s" % (str(affinity), str(app_name)))
        return False
