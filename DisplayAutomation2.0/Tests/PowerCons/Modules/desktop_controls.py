#######################################################################################################################
# @file desktop_controls.py
# @brief Python wrapper helper module providing multiple desktop controls
# @details      @ref desktop_controls.py exposes below APIs:
#               Contains:
#                   1. Desktop Control API's for mouse movements, screen saver, notifications, taskbar ...
#                   2. Power Management API's for setting and getting timeouts
#                   3. Power Management API's for getting windows os version
# @author Ashish Tripathi
#######################################################################################################################

import base64
import ctypes
import logging
import os
import re
import subprocess
import time
from enum import IntEnum

import win32api
import win32con
import win32gui
import win32ui

from Libs.Core import display_power, enum, registry_access
from Libs.Core.display_config import display_config

##
# Registry Paths
__REG_PATH_DESKTOP = "Control Panel\\Desktop"
__REG_PATH_POLICIES_EXPLORER = "Software\\Policies\\Microsoft\\Windows\\Explorer"
__REG_PATH_ADVANCED = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
__REG_PATH_CURSOR = "Control Panel\\Cursors"


##
# @brief        This class indicates the list of Desktop States
class DesktopState(ctypes.Structure):
    _members_ = [
        ('is_screen_saver_active', ctypes.c_bool),
        ('sleep_time_out', ctypes.c_int),
        ('display_time_out', ctypes.c_int),
        ('power_scheme', ctypes.c_int)
    ]


##
# @brief        This class contains the List of time-out for display and sleep
class TimeOut(IntEnum):
    TIME_OUT_DISPLAY = 0
    TIME_OUT_SLEEP = 1


##
# @brief        Checks for cursor move after interval of 'time_in_sec' time
# @param[in]    time_in_sec mouse cursor movement will be compared after 'time_in_sec' seconds
# @return       True,   if cursor is moved
#               None,   if invalid cursor info/argument
#               False,  otherwise
def is_mouse_cursor_moved(time_in_sec):
    ##
    # verify the argument is a positive integer
    if time_in_sec <= 0:
        return None

    # checks for the cursor info
    cursor_info = win32gui.GetCursorInfo()
    if cursor_info == 0:
        return None

    # wait for 'time_in_sec' seconds
    time.sleep(time_in_sec)

    # checks again for the cursor info
    updated_cursor_info = win32gui.GetCursorInfo()
    if updated_cursor_info == 0:
        return None

    # Compare the position of mouse cursor which is present at index [2]
    if cursor_info[2] == updated_cursor_info[2]:
        return True
    return False


##
# @brief        Checks for change in shape of cursor after interval of 'time_in_sec' time
# @param[in]    time_in_sec mouse cursor shape change will be compared after 'time_in_sec' seconds
# @return       True,   if mouse cursor shape is same
#               None,   if invalid cursor info/argument
#               False,  otherwise
def is_mouse_cursor_shape_changed(time_in_sec):
    ##
    # verify the argument is a positive integer
    if time_in_sec <= 0:
        return None
    ##
    # checks for the cursor info
    cursor_info = win32gui.GetCursorInfo()
    if cursor_info is None:
        logging.error("Invalid cursor info")
        return None

    ##
    # wait for 'time_in_sec' seconds
    time.sleep(time_in_sec)

    ##
    # checks again for the cursor info
    updated_cursor_info = win32gui.GetCursorInfo()
    if updated_cursor_info[2] is None:
        logging.error("NO cursor found after waiting {0} seconds".format(time_in_sec))
        return None

    ##
    # Type of cursor is compared which is present at index [1]
    if cursor_info[1] == updated_cursor_info[1]:
        return True
    return False


##
# @brief        switches desktop clock visibility from task bar
# @param[in]    show_clock Boolean to hide/show clock
# @return       True,   if the clock was previously visible, the return value is 24 and
#                       if the clock was previously hidden, the return value is zero
#               False,  otherwise
def show_clock_in_taskbar(show_clock):
    # get task bar handle
    task_bar_handle = win32gui.FindWindow("Shell_TrayWnd", None)

    # get notification tray area handle
    tray_area_handle = win32gui.FindWindowEx(task_bar_handle, None, "TrayNotifyWnd", None)

    # get clock handle from the tray
    clock_handle = win32gui.FindWindowEx(tray_area_handle, None, "TrayClockWClass", None)

    # switching visibility status
    return_status = win32gui.ShowWindow(clock_handle, win32con.SW_SHOW if show_clock else win32con.SW_HIDE)

    # if the clock is previously visible, then the return value is 24 for show/hide operation
    # if the clock is previously hidden, then the return value is 0 for show/hide operation
    return True if return_status in (24, 0) else False


##
# @brief        enable/disable screen saver
# @param[in]    enable_screen_saver Boolean to enable/disable screen saver
# @return       True,   if writing in registry is successful
#               False,  otherwise
def enable_disable_screen_saver(enable_screen_saver):
    ##
    # enable/disable screen saver value
    key_value = "1" if enable_screen_saver else "0"
    ##
    # writing in registry
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, __REG_PATH_DESKTOP)
    return registry_access.write(reg_args, "ScreenSaveActive", registry_access.RegDataType.SZ, key_value)


##
# @brief        reads registry for the screen saver status
# @return       True,   if reading registry is successful
#               None,   if reading registry is failed
#               False,  otherwise
def is_screen_saver_enabled():
    ##
    # reading in registry
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, __REG_PATH_DESKTOP)
    registry_value, registry_type = registry_access.read(reg_args, "ScreenSaveActive")

    if None in (registry_value, registry_type):
        return None
    return True if registry_value == "1" else False


##
# @brief        enable/disable notification center
# @param[in]    disable_notification_center Boolean to enable/disable notification center
# @return       True,   if writing in registry is successful
#               False,  otherwise
def enable_disable_notification_center(disable_notification_center):
    ##
    # show/hide action center
    key_value = 0x1 if disable_notification_center else 0x0

    ##
    # writing in registry
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, __REG_PATH_POLICIES_EXPLORER)
    return registry_access.write(reg_args, "DisableNotificationCenter", registry_access.RegDataType.DWORD, key_value)


##
# @brief        enable/disable balloon notifications
# @param[in]    enable_balloon_notification Boolean to enable/disable balloon notifications
# @return       True,   if writing in registry is successful
#               False,  otherwise
def enable_disable_balloon_notification(enable_balloon_notification):
    # disable/enable balloon notification/tips
    key_value = 0x1 if enable_balloon_notification else 0x0

    # writing in registry
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, __REG_PATH_ADVANCED)
    return registry_access.write(reg_args, "EnableBalloonTips", registry_access.RegDataType.DWORD, key_value)


##
# @brief        switches notification area/tray visibility from task bar
# @param[in]    show Boolean to hide/show notification area
# @return       True,   if the area was previously visible, the return value is 24 or
#                       if the area was previously hidden, the return value is zero
#               False, otherwise
def show_notification_area(show):
    ##
    # get task bar handle
    task_bar_handle = win32gui.FindWindow("Shell_TrayWnd", None)

    ##
    # get notification tray area handle
    tray_area_handle = win32gui.FindWindowEx(task_bar_handle, None, "TrayNotifyWnd", None)

    ##
    # switching visibility status
    return_status = win32gui.ShowWindow(tray_area_handle,
                                        win32con.SW_SHOW if show else win32con.SW_HIDE)
    ##
    # if the area is previously visible, then the return value is 24 for show/hide operation
    # if the area is previously hidden, then the return value is 0 for show/hide operation
    return True if return_status in (24, 0) else False


##
# @brief        Keeps the task bar unhidden by moving the cursor from bottom left to bottom right of the screen
# @note         This function assumes that the task bar is positioned at the bottom of screen
# @return       None,   if no display found
def preview_task_bar():
    cursor_x = 0
    ##
    # stepping for mouse cursor move
    mouse_move_step = 10
    ##
    # default mouse cursor path location
    cursor_location = r"C:\Windows\Cursors\aero_arrow.cur"

    config = display_config.DisplayConfiguration()
    enum_displays = config.get_enumerated_display_info()
    ##
    # checks for No Display found
    if enum_displays is None:
        return None
    target_id = config.get_target_id('DP_A', enum_displays)
    mode = config.get_current_mode(target_id)
    win32api.ShowCursor(True)

    ##
    # Switching to the default cursor shape
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.CURRENT_USER, __REG_PATH_CURSOR)
    registry_access.write(reg_args, "Arrow", registry_access.RegDataType.EXPAND_SZ, cursor_location)
    ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETCURSORS, 0, 0,
                                               win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)

    ##
    # setting cursor position to the bottom left of the screen
    # SetCursorPos (origin, height of the display)
    win32api.SetCursorPos((0, mode.VtRes))

    ##
    # move the mouse cursor from left bottom to right bottom
    for i in range(0, (mode.HzRes / mouse_move_step)):
        cursor_x += mouse_move_step
        win32api.SetCursorPos((cursor_x, mode.VtRes))
        ##
        # breather
        time.sleep(1)


##
# @brief        gets handle to desktop window and store the screen image in bmp file
# @return       image_name  name of the created image file
#               None,       if Failed to create Device context/bitmap compatible with the device
# @note         This function assumes that the display is not cloned/extended
def create_display_bmp():
    ##
    # width, height  of the screen of the primary display monitor, in pixels
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    ##
    # width, height  of the screen of the virtual display monitor which is extended to the left, in pixels
    # note: it will be zero until display is extended to the left
    screen_x = 0
    screen_y = 0

    if 0 in (screen_width, screen_height):
        logging.error("Retrieving of system metrics for primary display failed")
        return None
    ##
    # get handle to the desktop window
    desktop_1 = win32gui.GetDesktopWindow()

    ##
    # create a device context
    desktop_dc = win32gui.GetWindowDC(desktop_1)
    if desktop_dc is None:
        logging.error("Failed to create Device Context")
        return None
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    ##
    # create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC()
    if mem_dc is None:
        logging.error("Failed to create Compatible Device Context")
        return None
    ##
    # create a bitmap object
    screen_shot = win32ui.CreateBitmap()

    ##
    # creates a bitmap compatible with the device that is associated with the specified device context
    screen_shot.CreateCompatibleBitmap(img_dc, screen_width, screen_height)
    bmp = mem_dc.SelectObject(screen_shot)
    if bmp is None:
        logging.error("Failed to create bitmap compatible with the device")
        return None

    ##
    # copy the screen into our memory device context
    # (0, 0) - (x co-ordinate, y co-ordinate) upper left corner of the destination rectangle
    # (screen_width, screen_height) - (width, height) of the source and destination rectangles
    # img_dc - handle to the source device context
    # (screen_x, screen_y) - (x-coordinate, y-coordinate) of the upper-left corner of the source rectangle
    #  win32con.SRCCOPY - raster-operation code. These codes define how the color data for the source rectangle
    #                     is to be combined with the color data for the destination rectangle
    #                     to achieve the final color
    mem_dc.BitBlt((0, 0), (screen_width, screen_height), img_dc, (screen_x, screen_y), win32con.SRCCOPY)
    mem_dc.SelectObject(bmp)

    ##
    # Generate random name for image name and joining for file extension ".png"
    image_name = str(time.time()) + ".png"

    ##
    # saving temporarily to .bmp file to compare with another screen shot
    screen_shot.SaveBitmapFile(mem_dc, image_name)

    ##
    # deletes the device context
    mem_dc.DeleteDC()

    ##
    # Delete object which will make the handle no more valid
    win32gui.DeleteObject(screen_shot.GetHandle())
    return image_name


##
# @brief        API compares two bmp image file
# @param[in]    image_1 first image to be compared
# @param[in]    image_2 second image to be compared
# @return       True,   if image is same
#               None,   if failed in reading file
#               False,  otherwise
# @note         this function should be called after create_display_bmp(),
#               user has to remove these saved images after getting the results with "os.remove(image_name)"
def compare_bmp_image(image_1, image_2):
    if os.path.isfile(image_1) and os.path.isfile(image_2):
        with open(image_1, "rb") as imageFile:
            # convert binary data into ASCII-safe "text" for first image
            first_image = base64.b64encode(imageFile.read())

        with open(image_2, "rb") as imageFile:
            # convert binary data into ASCII-safe "text" for second image
            second_image = base64.b64encode(imageFile.read())

        if None in (first_image, second_image):
            logging.error("One/Both of the image file/s is/are NULL")
            return None

        elif first_image == second_image:
            logging.debug("Both images are SAME")
            return True

        else:
            logging.debug("Both images are DIFFERENT")
            return False
    else:
        logging.error("One/Both image file/s doesn't exist")
        return None


##
# @brief        API verifies that the screen is same or not with the help of image
# @param[in]    time_in_sec images will be compared after 'time_in_sec' seconds
# @return       True,   if image is static - images will be removed
#               False,  otherwise - images won't be removed for interrupt check
def is_static_image(time_in_sec):
    image_1 = create_display_bmp()
    time.sleep(time_in_sec)  # breather
    image_2 = create_display_bmp()
    compared_results = compare_bmp_image(image_1, image_2)
    ##
    # removing .bmp image file after comparing image
    os.remove(image_1)
    os.remove(image_2)
    return True if compared_results else False


##
# @brief        Exposed API for setting sleep time-out.
# @param[in]    time_out_type should be given enum for "display" and "sleep" respectively for setting time-out
# @param[in]    time_in_min [optional], if given, time in minutes will be set for sleep time-out. If
#               time_in_min is not given, then sleep time-out for current active power plan will be set to 30 mins
# @param[in]    power_line_status [optional], if given, sleep time-out will be set for this power line. If
#               power_line_status is not given, then sleep time-out will be set for the current active power line
# @return       True,   if executed correctly
#               False,  otherwise
def set_time_out(time_out_type, time_in_min=30, power_line_status=None):
    disp_power = display_power.DisplayPower()

    power_cfg_query = ['powercfg.exe', '/change']

    ##
    # if power line is not passed, get the current power line status
    if power_line_status is None:
        power_line_status = disp_power.get_current_powerline_status()

    if time_out_type == TimeOut.TIME_OUT_DISPLAY:
        if power_line_status == display_power.PowerSource.AC:
            power_cfg_query.append('monitor-timeout-ac')
        elif power_line_status == display_power.PowerSource.DC:
            power_cfg_query.append('monitor-timeout-dc')

    elif time_out_type == TimeOut.TIME_OUT_SLEEP:
        if power_line_status == display_power.PowerSource.AC:
            power_cfg_query.append('standby-timeout-ac')
        elif power_line_status == display_power.PowerSource.DC:
            power_cfg_query.append('standby-timeout-dc')

    power_cfg_query.append(str(time_in_min))
    ##
    # Execute the powercfg query and get the output
    sleep_time_out_return_value = subprocess.check_output(power_cfg_query, stderr=subprocess.STDOUT,
                                                          universal_newlines=True)
    if sleep_time_out_return_value != 0:
        return True
    return False


##
# @brief        Exposed API for getting sleep time-out for specified power state or will go with current state
# @param[in]    time_out_type should be given enum for "display" and "sleep" respectively for getting time-out
# @param[in]    power_plan [optional], if given, sleep time-out will be returned for this power plan. If
#               power_plan is not given, then sleep time-out of current active power plan will be returned
# @param[in]    power_line_status [optional], if given, sleep time-out will be returned for this power line. If
#               power_line_status is not given, then sleep time-out of the current active power line will be
#               returned
# @return       match_time_out.group('time'), time in minutes if executed correctly
#               None,                        otherwise
def get_time_out(time_out_type, power_plan=None, power_line_status=None):
    disp_power = display_power.DisplayPower()

    ##
    # If power_plan is not passed, get the current power plan
    if power_plan is None:
        power_plan = disp_power.get_current_power_scheme()

    if power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid power plan")
        return None

    ##
    # Set alias for power scheme. Consider default as BALANCED and point out
    power_scheme = 'SCHEME_BALANCED'  # enum.POWER_SCHEME_BALANCED
    if power_plan == display_power.PowerScheme.POWER_SAVER:
        power_scheme = 'SCHEME_MAX'
    elif power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_scheme = 'SCHEME_MIN'

    time_out_query_output = None
    if time_out_type == TimeOut.TIME_OUT_DISPLAY:
        ##
        # Execute the powercfg query and get the output
        time_out_query_output = subprocess.check_output(
            ['powercfg.exe', '/query', power_scheme, 'SUB_VIDEO',
             'VIDEOIDLE'], stderr=subprocess.STDOUT, universal_newlines=True)
        if time_out_query_output == '' or time_out_query_output is None:
            return None

    elif time_out_type == TimeOut.TIME_OUT_SLEEP:
        ##
        # Execute the powercfg query and get the output
        time_out_query_output = subprocess.check_output(
            ['powercfg.exe', '/query', power_scheme, 'SUB_SLEEP', 'STANDBYIDLE'], stderr=subprocess.STDOUT,
            universal_newlines=True)
        if time_out_query_output == '' or time_out_query_output is None:
            return None

    ##
    # if power line is not passed, get the current power line status
    if power_line_status is None:
        power_line_status = disp_power.get_current_powerline_status()

    if power_line_status == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    match_time_out = None
    if power_line_status == display_power.PowerSource.AC:
        ac_time_out_pattern = r" +Current AC Power Setting Index: (?P<time>[x0-9a-f]{10})"
        match_time_out = re.search(ac_time_out_pattern, time_out_query_output, re.I)
    elif power_line_status == display_power.PowerSource.DC:
        dc_time_out_pattern = r" +Current DC Power Setting Index: (?P<time>[x0-9a-f]{10})"
        match_time_out = re.search(dc_time_out_pattern, time_out_query_output, re.I)

    if match_time_out is None:
        return None
    else:
        ##
        # returning time in minutes
        return int(match_time_out.group('time'), 16) / 60


##
# @brief      API for save values for screen saver active, display time-out and sleep time-out
# @return     saved_desktop_state object of type saved desktop state (screen-saver active, display and sleep time-out)
#             False, otherwise
def save_desktop_state():
    disp_power = display_power.DisplayPower()
    saved_desktop_state = DesktopState()
    # getting and storing screen saver state
    saved_desktop_state.is_screen_saver_active = is_screen_saver_enabled()
    if saved_desktop_state.is_screen_saver_active is None:
        logging.error("Failed to read screen-saver value")
        return False

    ##
    # getting and storing current power scheme
    saved_desktop_state.power_scheme = disp_power.get_current_power_scheme()
    if saved_desktop_state.power_scheme is None:
        logging.error("Failed to get power scheme")
        return False

    ##
    # getting and storing display time-out for current power plan
    saved_desktop_state.display_time_out = get_time_out(TimeOut.TIME_OUT_DISPLAY)
    if saved_desktop_state.display_time_out is None:
        logging.error("Failed to get display time-out for current power plan")
        return False

    ##
    # getting and storing sleep time-out for both AC and DC state
    saved_desktop_state.sleep_time_out = get_time_out(TimeOut.TIME_OUT_SLEEP)
    if saved_desktop_state.sleep_time_out is None:
        logging.error("Failed to get sleep time-out for current power plan")
        return False
    return saved_desktop_state


##
# @brief        API clear the desktop by hiding clock, disabling notifications
#               and setting display, sleep time-out to "NEVER"
# @return       True,   if desktop is cleared
#               False,  otherwise
def clear_desktop():
    disp_power = display_power.DisplayPower()

    ##
    # disable screen saver
    return_status = enable_disable_screen_saver(False)
    if return_status is False:
        logging.error("Failed to disable screen-saver")
        return False
    logging.debug("Disabling screen saver")

    ##
    # hide the clock
    return_status = show_clock_in_taskbar(False)
    if return_status is False:
        logging.error("Failed to Hide desktop clock")
        return False
    logging.debug("Hiding clock")

    ##
    # disable balloon notifications
    return_status = enable_disable_balloon_notification(False)
    if return_status is False:
        logging.error("Failed to disable balloon notification")
        return False
    logging.debug("Hiding balloon notification")

    ##
    # hide tray notification area
    return_status = show_notification_area(False)
    if return_status is False:
        logging.error("Failed to hide notification area")
        return False
    logging.debug("Hiding notification area")

    ##
    # disable action center
    return_status = enable_disable_notification_center(False)
    if return_status is False:
        logging.error("Failed to disable notification center")
        return False
    logging.debug("Disabling notification center")

    ##
    # setting value for turn-off display to "NEVER" for current power scheme
    return_status = set_time_out(TimeOut.TIME_OUT_DISPLAY, 0)
    if return_status is False:
        return False
    logging.debug("Changing turn-off display to NEVER")

    ##
    # changing value for system sleep to "NEVER" for current power scheme
    return_status = set_time_out(TimeOut.TIME_OUT_SLEEP, 0)
    if return_status is False:
        return False
    logging.debug("Changing system sleep to NEVER")

    logging.info("Desktop is cleared")

    return True


##
# @brief        This API restores the desktop by showing clock, enabling notifications
#               and values of display, sleep time-out
# @param[in]    saved_desktop_state
# @return       True,   if executed correctly
#               False,  otherwise
def restore_desktop(saved_desktop_state):
    disp_power = display_power.DisplayPower()

    ##
    # enable screen saver
    return_status = enable_disable_screen_saver(saved_desktop_state.is_screen_saver_active)
    if return_status is False:
        logging.error("Failed to enable screen-saver")
        return False
    logging.debug("Restoring screen saver state")

    ##
    # show clock
    return_status = show_clock_in_taskbar(True)
    if return_status is False:
        logging.error("Failed to show desktop clock")
        return False
    logging.debug("Showing clock")

    ##
    # show balloon notifications
    return_status = enable_disable_balloon_notification(True)
    if return_status is False:
        logging.error("Failed to enable balloon notification")
        return False
    logging.debug("Showing balloon notification")

    ##
    # show notification area
    return_status = show_notification_area(True)
    if return_status is False:
        logging.error("Failed to show notification area")
        return False
    logging.debug("Showing notification-area")

    ##
    # enable action center
    logging.debug("Enabling action-center")
    return_status = enable_disable_notification_center(True)
    if return_status is False:
        logging.error("Failed to enable notification center")
        return False

    ##
    # display time out for current power state
    display_time_out = saved_desktop_state.display_time_out
    return_status = set_time_out(TimeOut.TIME_OUT_DISPLAY, display_time_out)
    if return_status is False:
        return False
    logging.debug("Restoring display time-out value")

    ##
    # restore sleep time out for current power state
    sleep_time_out = saved_desktop_state.sleep_time_out
    return_status = set_time_out(TimeOut.TIME_OUT_SLEEP, sleep_time_out)
    if return_status is False:
        return False
    logging.debug("Restoring sleep time-out value")

    logging.info("Desktop is restored")
    return True


##
# @brief        This API is used to get the version of windows os
# @return       version of OS, if found
#               'UNKNOWN',  otherwise
def get_win_os_version():
    output = os.popen('ver.exe').read().replace('\n', '')
    # https://en.wikipedia.org/wiki/Windows_10_version_history#Version_1903
    # https://en.wikipedia.org/wiki/Windows_10_version_history
    build_branch = dict()
    build_branch['19H1'] = [10018282, 10099999]
    build_branch['RS5'] = [10017627, 10018282]
    build_branch['RS4'] = [10017134, 10017627]
    build_branch['RS3'] = [10016299, 10017134]
    build_branch['RS2'] = [10014870, 10016299]
    build_branch['RS1'] = [10014310, 10014870]
    build_branch['TH2'] = [10010586, 10014310]
    build_branch['TH1'] = [10010240, 10010586]

    branch = "UNKNOWN"

    ##
    # Regular expression for grouping major, minor and build from build number
    os_version_pattern = r"^[a-zA-Z []+(?P<major>\d{2}).(?P<minor>\d).(?P<build>\d{5}).[0-9.]+\]$"
    ver_match = re.match(os_version_pattern, output)
    if ver_match is not None:
        ##
        # making build number 12.3.45678 as one number 12345678
        result = int(ver_match.group('build'))
        result += int(ver_match.group('minor')) * 100000
        result += int(ver_match.group('major')) * 1000000

        for key, value in build_branch.items():
            if value[0] <= result < value[1]:
                branch = key
                break

    return branch
