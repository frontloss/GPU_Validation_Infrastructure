########################################################################################################################
# @file         window_helper.py
# @brief        Helper module to access windows UI intefaces for window only
# @author       BEERESH
########################################################################################################################
import ctypes
import logging
import os
import random
import subprocess
import sys
import time
from Libs.Core.logger import gdhm
from Lib.enum import IntEnum  # @Todo: Override with Built-in python3 enum script path

# Don't remove below import, known issue : https://stackoverflow.com/questions/58631512/pywin32-and-python-3-8-0
import pywintypes
import win32api
import win32con
import win32ui
import win32gui

from Libs.Core import enum, registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.winkb_helper import press


##
# @brief        Visibility Enum
class Visibility(IntEnum):
    HIDE = 0
    SHOW = 1


##
# A module which provides an interface to the native win32 GUI API
from win32gui import (
    MoveWindow,
    GetWindowRect,
    IsWindowVisible,
    GetWindowPlacement
)

if sys.platform != 'win32':
    raise Exception('The _window_win module should only be loaded on a Windows system.')

SPI_SETDESKWALLPAPER = 20

# Flags for SetWindowPos:
SWP_NOMOVE = ctypes.c_uint(0x0002)
SWP_NOSIZE = ctypes.c_uint(0x0001)

# Flags for ShowWindow:
SW_MAXIMIZE = 3
SW_MINIMIZE = 6
SW_RESTORE = 9

SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
CloseWindow = ctypes.windll.user32.CloseWindow
GetWindowRect = ctypes.windll.user32.GetWindowRect
SetWindowPos = ctypes.windll.user32.SetWindowPos
ShowWindow = ctypes.windll.user32.ShowWindow

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

PROCESS_VIDEO_PLAYER = ["Video.UI.exe", "Media Player", "wmplayer.exe", "Microsoft.Media.Player.ex", "VLC media player"]
PROCESS_DX_APPS = ["D3D12", "ClassicD3D", "BOOSTEDAPP", "Snip & Sketch", "Snipping Tool", "Presentation API Window",
                   "ScreenSketch.exe"]
PROCESS_WEB_BROWSER = ["iexplore.exe", "MicrosoftEdge.exe", "msedge.exe"]


##
# @brief        _Rect Structure
class _Rect(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]

    ##
    # @brief        Checks for equality of objects
    # @param[in]    another_rect - Comparison object
    # @return       bool - True if both objects have equal values, False otherwise
    def equals(self, another_rect):
        if (self.left == another_rect.left and self.right == another_rect.right
                and self.top == another_rect.top and self.bottom == another_rect.bottom):
            logging.info("Rectangles are equal")
            return True
        else:
            return False

    ##
    # @brief        Overridden str method of _Rect Class
    # @return       str - String representation of _Rect class
    def __str__(self):
        return "%dx%d, %dx%d" % (self.left, self.right, self.top, self.bottom)


##
# @brief        Window class
class Window(object):

    ##
    # @brief        Constructor
    # @param[in]    hwnd - Window handle
    def __init__(self, hwnd):
        self._hwnd = hwnd  # Window handle

    ##
    # @brief        Set Window Position
    # @param[in]    x - x coordinate
    # @param[in]    y - y coordinate
    # @param[in]    width - width of the window
    # @param[in]    height - height of the window
    # @return       None
    def set_position(self, x, y, width, height):
        SetWindowPos(self._hwnd, None, x, y, width, height, ctypes.c_uint(0))

    ##
    # @brief        Move window to top-left corner position
    # @param[in]    x - x coordinate
    # @param[in]    y - y coordinate
    # @return       None
    def move(self, x, y):
        """Move window top-left corner to position"""
        SetWindowPos(self._hwnd, None, x, y, 0, 0, SWP_NOSIZE)

    ##
    # @brief        Resize current window
    # @param[in]    width - window width
    # @param[in]    height - window height
    # @return       None
    def resize(self, width, height):
        """Change window size"""
        SetWindowPos(self._hwnd, None, 0, 0, width, height, SWP_NOMOVE)

    ##
    # @brief        Maximize window
    # @return       None
    def maximize(self):
        ShowWindow(self._hwnd, SW_MAXIMIZE)

    ##
    # @brief        Set foreground window
    # @return       None
    def set_foreground(self):
        SetForegroundWindow(self._hwnd)

    ##
    # @brief        Minimize Window
    # @return       None
    def minimize(self):
        ShowWindow(self._hwnd, SW_MINIMIZE)

    ##
    # @brief        Restore Window
    # @return       None
    def restore(self):
        ShowWindow(self._hwnd, SW_RESTORE)

    ##
    # @brief        Close Window
    # @return       None
    def close(self):
        CloseWindow(self._hwnd)

    ##
    # @brief        Get position of Window
    # @return       rect - _Rect object
    def get_position(self):
        """Returns tuple of 4 numbers: (x, y)s of top-left and bottom-right corners"""
        rect = _Rect()
        GetWindowRect(self._hwnd, ctypes.pointer(rect))
        return rect


##
# @brief        Get all visible windows
# @return       titles - visible windows list
def get_windows():
    """Return dict: {'window title' : window handle} for all visible windows"""
    titles = {}

    ##
    # @brief        Get visible window title
    # @param[in]    hwnd - Window handle
    # @param[in]    lparam - None
    # @return       bool - True after function execution
    def foreach_window(hwnd, lparam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles[buff.value] = hwnd
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)

    return titles


##
# @brief        Get Window
# @param[in]    title - Window title
# @param[in]    exact - True if search is exact match, False otherwise
# @return       object - Window object if visible, None otherwise
def get_window(title, exact=False):
    """Return Window object if 'title' or its part found in visible windows titles, else return None
    Return only 1 window found first
    Args:
        title: unicode string
        exact (bool): True if search only exact match
    """
    titles = get_windows()
    hwnd = titles.get(title, None)
    if not hwnd and not exact:
        for k, v in titles.items():
            if title in k:
                hwnd = v
                break
    if hwnd:
        return Window(hwnd)
    else:
        return None


##
# @brief        Opens target file
# @param[in]    file_name - shell namespace object
# @return       None
def open_uri(file_name):
    logging.debug("openuri: %s", file_name)
    try:
        win32api.ShellExecute(None, "open", file_name, None, None, win32con.SW_MAXIMIZE)
    except Exception as e:
        logging.warning(e)
        # Sometime OS might throw Access Denied exception while trying to access the file (if it is being used by
        # other process). In this case, wait for 1 sec and try again.
        time.sleep(1)
        win32api.ShellExecute(None, "open", file_name, None, None, win32con.SW_MAXIMIZE)


##
# @brief        Opens a specific web page
# @param[in]    uri_path - Web Page URI
# @param[in]    full_screen - True if web page is to be opened in full screen, False otherwise
# @return       obj_ie - Window object
def open_web_page(uri_path, full_screen=False):
    close_browser()
    open_uri(uri_path)
    time.sleep(5)

    obj_ie = get_window("Internet Explorer")
    if obj_ie is None:
        obj_ie = get_window("Microsoft")

    time.sleep(1)
    obj_ie.set_foreground()
    obj_ie.maximize()
    if full_screen is True:
        time.sleep(5)

        x = 500
        y = 500
        mouse_left_click(x, y, True)
        time.sleep(2)
    return obj_ie


##
# @brief        Kills process by process ID
# @param[in]    pid - process ID
# @return       None
def kill_process(pid):
    __PROCESS_TERMINATE = 1
    handle = ctypes.windll.kernel32.OpenProcess(__PROCESS_TERMINATE, False, pid)
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.CloseHandle(handle)


##
# @brief        Kills process by Name
# @param[in]    process_name - Name of the process
# @return       bool - True if process is killed, False otherwise
def kill_process_by_name(process_name):
    pid = 0
    task_manager_lines = os.popen("tasklist").readlines()
    for line in task_manager_lines:
        try:
            current_process = line[0:28].strip()
            if current_process == process_name:
                pid = int(line[29:34])
                break
        except:
            pass

    if pid > 0:
        kill_process(pid)
        return True
    else:
        print("Not able to find process %s" % process_name)
        return False


##
# @brief        Close all browsers
# @return       None
def close_browser():
    for process in PROCESS_WEB_BROWSER:
        kill_process_by_name(process)


##
# @brief        Get current Display resolution
# @return       (int, int) - (width, height)
def get_current_resolution():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


##
# @brief        Close all media players
# @return       None
def close_media_player():
    for process in PROCESS_VIDEO_PLAYER:
        kill_process_by_name(process)


##
# @brief        Close all dx apps
# @return       None
def close_dx_apps():
    for process in PROCESS_DX_APPS:
        kill_process_by_name(process)


##
# @brief        Opens Media File
# @param[in]    media_path - media file path
# @param[in]    full_screen - True to apply full screen to media player window, False otherwise
# @param[in]    minimize_windows - True to minimize all windows, False otherwise
# @return       media_player_handle - Window object
def open_media_file(media_path, full_screen=False, minimize_windows=True):
    machine_info = SystemInfo()
    os_info = machine_info.get_os_info()

    ##
    # Close any previously opened media player
    close_media_player()

    ##
    # Minimize all windows before opening media player
    if minimize_windows is True:
        minimize_all_windows()

    open_uri(media_path)
    time.sleep(5)

    ##
    # WA for skipping the first run dialog box on RS4 and RS5
    if '16299' < os_info.BuildNumber <= '18000':
        if get_window('Let Movies & TV access your videos library?', True):
            logging.debug("Popup is opened")
            press("ENTER")
            time.sleep(2)
        press('ESC')
        time.sleep(5)
        press('ESC')
        time.sleep(5)

    if get_window('Movies & TV', True) is None and get_window('Films & TV', True) is None:
        ##
        # Media player opened in full screen mode, bring it back to windowed mode
        press("ALT_ENTER")
        time.sleep(2)

        ##
        # Remove focus from play/pause button
        press("ESC")
        time.sleep(2)

        ##
        # Second attempt to check if the media player running in windowed mode or not
        if get_window('Movies & TV', True) is None and get_window('Films & TV', True) is None:
            logging.error('Failed to open Movies & TV/Films & TV app')
            gdhm.report_driver_bug_di(title='[WindowHelper] Failed to open Movies & TV/Films & TV app')
            return None
        else:
            logging.debug('Movies & TV/Films & TV app opened in windowed mode')

    media_player_handle = get_window('Movies & TV', True)
    if media_player_handle is None:
        media_player_handle = get_window('Films & TV', True)

    if full_screen is True:
        time.sleep(5)

        press("ALT_ENTER")
        time.sleep(2)

        ##
        # Remove focus from play/pause button
        press("ESC")
        time.sleep(2)

    return media_player_handle


##
# @brief        Opens Map
# @param[in]    full_screen - True if map is to be opened in full screen, False otherwise
# @return       obj_window - Window object
def open_maps(full_screen=False):
    kill_process_by_name("Maps.Windows.exe")
    time.sleep(2)
    open_uri("bingmaps:")
    time.sleep(3)

    obj_window = get_window("Maps")
    obj_window.set_foreground()
    obj_window.maximize()

    if full_screen is True:
        time.sleep(5)

        x = 500
        y = 500
        mouse_left_click(x, y, True)

        time.sleep(2)
    return obj_window


##
# @brief        Minimize all windows
# @return       bool - True if all windows is successfully minimized, False otherwise
def minimize_all_windows():
    minimize_all = 419
    wm_command = 0x0111
    find_window = ctypes.windll.user32.FindWindowA

    handle = find_window("Shell_traywnd".encode(), None)
    window = win32ui.CreateWindowFromHandle(handle)
    result = window.SendMessage(wm_command, minimize_all, 0)
    if result == 0:
        logging.debug("Minimizing all Windows")
        return True
    return False


##
# @brief        Restore all windows
# @return       bool - True if restoring all windows is successful, False otherwise
def restore_all_windows():
    minimize_all = 416
    wm_command = 0x0111
    find_window = ctypes.windll.user32.FindWindowA

    handle = find_window("Shell_traywnd".encode(), None)
    window = win32ui.CreateWindowFromHandle(handle)
    result = window.SendMessage(wm_command, minimize_all, 0)
    if result == 0:
        logging.debug("Restoring all Windows")
        return True
    return False


##
# @brief        Hide or show the task bar
# @param[in]    option - Enum of type TOGGLE
# @return       bool - True if task bar toggle is successful, False otherwise
def toggle_task_bar(option):
    user32 = ctypes.WinDLL("user32")
    un_hide_task_bar = 0x40
    hide_task_bar = 0x80

    handle = user32.FindWindowW(u"Shell_traywnd", u"")

    if option == Visibility.HIDE:
        logging.debug("Toggle task bar : Hide")
        return user32.SetWindowPos(handle, 0, 0, 0, 0, 0, hide_task_bar) != 0

    elif option == Visibility.SHOW:
        logging.debug("Toggle task bar : Show")
        return user32.SetWindowPos(handle, 0, 0, 0, 0, 0, un_hide_task_bar) != 0


##
# @brief        Get list of all connected monitors
# @details      enum_display_monitors function enumerates display monitors that intersect a region formed
#               by the intersection of a specified clipping rectangle. EnumDisplayMonitors calls an application-defined
#               MonitorEnumProc callback function once for each monitor that is enumerated.
# @return       monitors - list of display monitors.
def enum_display_monitors():
    monitors = []
    monitor_enum_proc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong,
                                           ctypes.POINTER(ctypes.wintypes.RECT), ctypes.c_double)

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitors.append((lprcMonitor.contents.left, lprcMonitor.contents.top,
                         lprcMonitor.contents.right, lprcMonitor.contents.bottom))
        return 1

    ctypes.windll.user32.EnumDisplayMonitors(0, 0, monitor_enum_proc(callback), 0)
    return monitors


##
# @brief        Get list of all connected monitors
# @details      get_enum_display_monitors_list function enumerates display monitors that intersect a region
#               formed by the intersection of a specified clipping rectangle.
# @return       results - list of display monitors with monitor handle and dimension.
#               example of single display edp:  [(<PyHANDLE:65537>, <PyHANDLE:0>, (0, 0, 1280, 853))]
def get_enum_display_monitors_list():
    return win32api.EnumDisplayMonitors()


##
# @brief        Enumerates all the top-level windows on the screen by passing handle to each window
# @return       results - list of top-level windows.
def enum_windows():
    from win32gui import EnumWindows, GetWindowText, GetClassName
    results = []

    def _handler(hwnd, results):
        results.append((hwnd, GetWindowText(hwnd), GetClassName(hwnd)))

    EnumWindows(_handler, results)
    return results


##
# @brief        Helper function which will set the mouse cursor position across the display monitors
# @param[in]    src_port - Source Connector port
# @param[in]    dst_port - Destination Connector port
# @return       bool - True if cursor moved to destination, False otherwise
def move_mouse_cursor(src_port, dst_port):
    is_src_id_valid = is_dst_id_valid = False
    src_path_index = dst_path_index = -1

    ##
    # Get the enumerated display information
    # Call display_config
    disp_cfg_handle = display_config.DisplayConfiguration()
    enumerated_info = disp_cfg_handle.get_enumerated_display_info()

    get_config = disp_cfg_handle.get_current_display_configuration()

    ##
    # Fetch the target ID of the displays based on the connector_port_type
    src_target_id = disp_cfg_handle.get_target_id(src_port, enumerated_info)
    dst_target_id = disp_cfg_handle.get_target_id(dst_port, enumerated_info)

    ##
    # Check if the target ids are valid and fetch the path index of the displays based on the target ID
    for index in range(0, get_config.numberOfDisplays):
        if get_config.displayPathInfo[index].targetId == src_target_id:
            is_src_id_valid = True
            src_path_index = index
        if get_config.displayPathInfo[index].targetId == dst_target_id:
            is_dst_id_valid = True
            dst_path_index = index

    if not (is_src_id_valid and is_dst_id_valid):
        logging.error("Invalid Port Type")
        gdhm.report_driver_bug_di(title="[WindowHelper] Invalid Port Type")
        return False

    ##
    # Enumerate the display monitors
    monitor_dimension = enum_display_monitors()

    ##
    # Obtain random x,y co-ordinates, across the monitors, between which the mouse cursor position is set
    src_x_coordinate = random.randint(monitor_dimension[src_path_index][0], monitor_dimension[src_path_index][2])
    dst_x_coordinate = random.randint(monitor_dimension[dst_path_index][0], monitor_dimension[dst_path_index][2])
    src_y_coordinate = random.randint(monitor_dimension[src_path_index][1], monitor_dimension[src_path_index][3])
    dst_y_coordinate = random.randint(monitor_dimension[dst_path_index][1], monitor_dimension[dst_path_index][3])

    ##
    # Constant values which are added to increment x,y
    inc_x_coordinate = ((src_x_coordinate - dst_x_coordinate) // 100)
    inc_y_coordinate = ((src_y_coordinate - dst_y_coordinate) // 100)
    x, y = src_x_coordinate, src_y_coordinate
    while True:
        if (src_x_coordinate < x > dst_x_coordinate or src_x_coordinate > x < dst_x_coordinate) or \
                (src_y_coordinate > y < dst_y_coordinate or src_y_coordinate < y > dst_y_coordinate):
            break
        x -= inc_x_coordinate
        y -= inc_y_coordinate
        win32api.SetCursorPos((x, y))
        time.sleep(0.05)
    return x == dst_x_coordinate and y == dst_y_coordinate


##
# @brief        Helper function which will drag the app to the specified screen in Extended mode
# @param[in]    target_port - The target port the app should be moved to
# @param[in]    gfx_adapter - Graphics adapter value, default is "gfx_0"
# @param[in]    app_name - Name or subString of the app to move eg: "Movies & TV"
# @return       None
def drag_app_across_screen(app_name, target_port, gfx_adapter="gfx_0"):
    disp_config = display_config.DisplayConfiguration()
    displayconfig = disp_config.get_config()

    display_index_list = [i for i in range(displayconfig.numberOfDisplays) if
                          CONNECTOR_PORT_TYPE(displayconfig.displayPathInfo[i].displayAndAdapterInfo.ConnectorNPortType)
                          .name == target_port and
                          displayconfig.displayPathInfo[i].displayAndAdapterInfo.adapterInfo.gfxIndex == gfx_adapter]
    # if the specified gfx_adapter:port pair was not found in the active displays raise error
    if display_index_list == []:
        logging.error(f"specified port was not found for port:{target_port} gfx_adapter:{gfx_adapter}")
        gdhm.report_driver_bug_di(f"[WindowHelper] Specified port not in active displays for gfx_adapter {gfx_adapter}")
        raise Exception("Specified port not in the active displays")
    else:
        tar_index = display_index_list[0]

    # updating Monitor dimension dictionary based on list return by get_config API.
    monitor_dimension = {}  # [(0, (0, 0, 1280, 853)), (1, (1910, 0, 1280, 0))]
    monitor_dimension_from_enum_display = get_enum_display_monitors_list()
    if monitor_dimension_from_enum_display is None:
        logging.error("get_enum_display_monitor_list_fail")
        gdhm.report_driver_bug_di(title="[WindowHelper] Failed to get monitor list")
        return
    for display_config_index in range(displayconfig.numberOfDisplays):
        for enum_display_index in range(len(monitor_dimension_from_enum_display)):
            monitor_data = win32api.GetMonitorInfo(monitor_dimension_from_enum_display[enum_display_index][0])
            if monitor_data["Device"] == displayconfig.displayPathInfo[display_config_index]. \
                    displayAndAdapterInfo.ViewGdiDeviceName:
                monitor_dimension[display_config_index] = monitor_data["Monitor"]

    flag = False
    win_index = None
    win_bottom_index = None
    for hwnd, text, cls in enum_windows():
        if app_name in text:
            flag = True
            left, top, right, bottom = GetWindowPlacement(hwnd)[4]
            for i in range(len(monitor_dimension)):
                l, t, r, b = monitor_dimension[i]
                if left in range(l, r) and top in range(t, b):
                    win_index = i
                if right in range(l, r) and bottom in range(t, b):
                    win_bottom_index = i

            if win_index is None:
                logging.error("Unable to find the screen for App coordinates")
                gdhm.report_driver_bug_di(title="[WindowHelper] Unable to find screen for App coordinates")
                logging.info(
                    f"App coordinates->{l},{t},{r},{b} was not found in any of the screen coordinates "
                    f"{monitor_dimension}")
                raise Exception("Unable to find screen for App coordinates")

            # if the app is running in the same display where the move is requested, then return
            if win_index == tar_index:
                logging.warning("App is playing in the same screen where move has been requested")
                return

            # If app is spanning across two displays raise exception, issue a warning, but move to the target screen
            elif win_index != win_bottom_index and win_bottom_index != None:
                logging.warning("App is currently played across two different displays")

            # Obtain 'width' and 'height' of the application window
            width = right - left
            height = bottom - top

            # if the app is playing in maximised mode make it windowed mode prior to dragging
            if GetWindowPlacement(hwnd)[1] == win32con.SW_MAXIMIZE:
                ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
                time.sleep(1)
                left, top, right, bottom = GetWindowPlacement(hwnd)[4]
                if GetWindowPlacement(hwnd)[1] != win32con.SW_SHOWNORMAL:
                    logging.error("Unable to set the app in windowed mode")
                    gdhm.report_driver_bug_di(title="[WindowHelper] Unable to set the app in windowed mode")
                    raise Exception("Unable to set the app in windowed mode")

            screen_width, screen_height = abs(monitor_dimension[tar_index][0] - monitor_dimension[tar_index][2]), abs(
                monitor_dimension[tar_index][1] - monitor_dimension[tar_index][3])

            # define the target to which the app has to be moved to, this is wrt to the (left,top) coordinates of the
            # app to be moved

            y_target, x_target = monitor_dimension[tar_index][1] + random.randrange(0, 50), \
                                 monitor_dimension[tar_index][0] + random.randrange(0, 50)

            # define m and n to know the rate and direction of movement of x and y coordinates respectively
            # if m or n is positive then the respective coordinate has to increase, otherwise decrease

            m = (x_target - left) // 10
            n = (y_target - top) // 10

            # define the steps for movement of x and y coordinates - mx and my, which will be depending on the value
            # of m and n if m and n are 0, then then set both of them as 10. if y > x, the my will be set 10 and
            # mx will be a number between 1-10, depending on the slope, if y < x, vice versa.

            if n == 0 or m == 0:
                mx = my = 10
            else:
                slope = abs(n / m)
                if slope > 1:
                    my, mx = 10, max(int(10 / slope), 1)
                else:
                    my, mx = max(int(10 * slope), 1), 10

            current_x, current_y = left, top
            logging.info(
                f"Moving {text} to the specified screen target: {gfx_adapter}:{target_port} top:{x_target},"
                f"left:{y_target},width:{screen_width // 2},height:{screen_height // 2}")

            # move the app to the target screen in increments of mx and my, resize the app with respect to the target
            # screen limits to ensure the app is never over the screen limits. eg : if the source app coordinates (
            # left,top) is (50,50) and the destination coordinates (xt,yt) are (1200,-400), m is +ve, n is -ve. 0 <
            # slope < 1, mx = 10 and 1 <= my < 10, the loop will be executed until both the coordinates are equal to
            # target coordinates. The min and max in the loop ensures the increment/decrement will make the
            # coordinates fall over the specified x_target and y_target limits.

            while current_x != x_target or current_y != y_target:
                current_x = min(current_x + mx, x_target) if m > 0 else max(current_x - mx, x_target)
                current_y = min(current_y + my, y_target) if n > 0 else max(current_y - my, y_target)
                MoveWindow(hwnd, current_x, current_y, screen_width // 2, screen_height // 2, 1)
                time.sleep(.001)

    if not flag:
        logging.error('The app is not in the list of opened apps')
        gdhm.report_test_bug_di(title='[WindowHelper] The app is not in the list of opened apps')
        raise Exception('The app is not in the list of opened apps')

    return


##
# @brief        Prepares desktop to capture CRC in pre-silicon environment
# @param[in]    action - True to minimize desktop apps, False to restore to default state
# @return       None
def show_desktop_bg_only(action):
    if action is True:
        win32api.ShowCursor(False)
        minimize_all_windows()
        toggle_task_bar(Visibility.HIDE)
    else:
        win32api.ShowCursor(True)
        restore_all_windows()
        toggle_task_bar(Visibility.SHOW)


##
# @brief        API to hide or unhide desktop icons
# @param[in]    action - True to hide icons, False to unhide
# @return       result - True if desktop icons hidden successfully, False otherwise
def hide_desktop_icons(action):
    if action is True:
        key_value = 0x1
    else:
        key_value = 0x0

    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                             reg_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
    registry_access.write(args=reg_args, reg_name="HideIcons", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=key_value)

    ##
    # Restart the driver to make changes take effect
    result, reboot_required = display_essential.restart_gfx_driver()
    if not result:
        logging.error("Aborting the test as Display driver restart failed")

    return result


##
# @brief        Mouse left click
# @param[in]    x - x coordinate of mouse click position
# @param[in]    y - y coordinate of mouse click position
# @param[in]    is_double_click - True to perform double click, False for single click
# @return       None
def mouse_left_click(x, y, is_double_click=False):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    if is_double_click is True:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


##
# @brief        Mouse right click
# @param[in]    x - x coordinate of mouse click position
# @param[in]    y - y coordinate of mouse click position
# @return       None
def mouse_right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


##
# @brief        Random mouse scroll
# @param[in]    x - x coordinate of mouse click position
# @param[in]    y - y coordinate of mouse click position
# @param[in]    scroll_duration - duration to scroll
# @return       None
def random_mouse_scroll(x, y, scroll_duration):
    win32api.SetCursorPos((x, y))
    start_time = time.time()
    while time.time() - start_time < scroll_duration:
        # One wheel click is defined as WHEEL_DELTA, which is 120.
        # Negative value - rotated backward, Positive value - rotated forward
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -120, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 120, 0)


##
# @brief        Exposed API to find process is running
# @param[in]    process_name string, name of the process
# @return       True if process is running, False if process is not running, None if failed to do operation
def is_process_running(process_name):
    task_manager_out = subprocess.run('tasklist', capture_output=True)
    task_manager_lines = task_manager_out.stdout.decode()

    if task_manager_out.returncode != 0 or len(task_manager_lines) == 0:
        logging.error("Not able to get tasklist")
        return None

    for line in task_manager_lines.splitlines():
        try:
            current_process = line[0:28].strip()
            if process_name in current_process:
                logging.info(f"Process: {process_name} is running")
                return True
        except Exception as e:
            logging.error(f"Exception occurred while fetching tasklist. {e}")

    logging.info(f"Process: {process_name} is NOT running")
    return False


##
# @brief        Exposed API to set cursor position in middle of the application
# @param[in]    hwnd - Window handle
# @return       None
def move_cursor_to_application_center(hwnd):
    x0, x1, y0, y1 = win32gui.GetWindowRect(hwnd)
    mid_x, mid_y = int(x0 + (x1 - x0) * 0.75), y0 + int((y1 - y0) * 0.75)
    win32api.SetCursorPos((mid_x, mid_y // 2))


##
# @brief        Exposed API to get window handle
# @param[in]    text - window title
# @return       handle - Window handle if API is open, else None
def get_window_handle(text):
    for handle, app_txt, _ in enum_windows():
        app_txt = app_txt.upper()
        if app_txt.find(text) >= 0:
            return handle
    return None


##
# @brief        set_app_in_foreground : Set the app to foreground
# @param[in]    hwnd                  : App handle
# @return       None
def set_app_in_foreground(hwnd):
    win32gui.SetForegroundWindow(hwnd)

##
# @brief        Mouse wheel scroll
# @param[in]    x - x coordinate of mouse click position
# @param[in]    y - y coordinate of mouse click position
# @param[in]    scroll_duration - duration to scroll
# @return       None
def mouse_wheel_scroll(x, y, scroll_duration):
    start_time = time.time()
    while time.time() - start_time < scroll_duration:
        # One wheel click is defined as WHEEL_DELTA, which is 120.
        # Negative value - rotated backward, Positive value - rotated forward
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -120, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 120, 0)


##
# @brief        Setting given image as desktop background
# @param[in]    image - path to the image to set
# @return       None
def set_image_as_desktop_background(image):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, 0)


if __name__ == '__main__':
    open_maps()
