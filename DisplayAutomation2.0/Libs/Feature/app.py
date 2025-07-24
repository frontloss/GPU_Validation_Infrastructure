########################################################################################################################
# @file         app.py
# @brief        The file contains basic apps and associated functions:
#               * Abstract app base class with generic functions.
#               * Base class contains mandatory methods that child classes have to implement
#               * Different app classes, which implements various methods
#               * Factory class which facilitates creation of different app objects
# @author       Gopikrishnan R
########################################################################################################################
import getpass
import logging
import os
import random
import subprocess
import time
from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from subprocess import Popen, PIPE

import win32api
import win32com.client
import win32con
import win32gui

from Libs.Core import window_helper, winkb_helper, registry_access


##
# # @brief    Enum for the support app title to search for getting the handle
class AppText(Enum):
    MOVIES_AND_TV = "Movies & TV"
    MEDIA_PLAYER = "Media Player"
    WINDOWS_MEDIA_PLAYER = "Windows Media Player"
    FILMS_AND_TV = "Films & TV"
    FLIPAT = "D3D12"
    CLASSICD3D = "ClassicD3D"
    D3D12FULLSCREEN = "D3D12"
    BOOSTED_APP = "BOOSTEDAPP"
    SNIP_AND_SKETCH = "Snip & Sketch"
    SNIPPING_TOOL = "Snipping Tool"
    PRESENTAT = "Presentation API Window"
    YOUTUBE = "YouTube"
    VLC = "VLC media player"


##
# @brief        Registry Status Type
class RegistryStatus(IntEnum):
    DISABLE = 0
    ENABLE = 1


##
# # @brief    Abstract Base class for app and associated functions, apps should inherit this class and implement the
# mandatory methods
class App(ABC):
    app_text = None

    ##
    # @brief        open_app        : Abstract method
    # @param[in]    is_full_screen  : Bool, whether the app has to be opened in full screen/not
    # @param[in]    minimize        : Bool, whether all current windows have to be minimized prior to opening the app
    # @param[in]    position        : Where the app has to be opened on screen, top or bottom
    # @return       None
    @abstractmethod
    def open_app(self, is_full_screen, minimize, position):
        pass

    ##
    # @brief        close_app : abstract method
    # @return       None
    @abstractmethod
    def close_app(self):
        pass

    ##
    # @brief        set_app_path : Abstract method
    # @param[in]    app_path     : Direction to which the app has to be snapped to left/right
    # @param[in]    cwd          : App handle
    # @return       None
    @abstractmethod
    def set_app_path(self, app_path, cwd=None):
        pass

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @param[in]    hwnd       : App handle
    # @return       None
    @classmethod
    def snap_mode(cls, hwnd, direction):
        cls.set_foreground(hwnd)
        if direction == "right":
            winkb_helper.snap_right()
            winkb_helper.press("ESC")
        else:
            winkb_helper.snap_left()
            winkb_helper.press("ESC")

    ##
    # @brief        drag       : To drag the app in the direction specified
    # @param[in]    panel      : Panel value to which the app has to be dragged
    # @param[in]    gfx_index  : Gfx adapter to which the app has to be dragged
    # @param[in]    hwnd       : App handle
    # @return       None
    @classmethod
    def drag(cls, panel, gfx_index, hwnd):
        cls.set_foreground(hwnd)
        window_helper.drag_app_across_screen(AppText[cls.app_text.upper()].value, panel, gfx_index)

    ##
    # @brief        set_foreground : Set the app to foreground
    # @param[in]    hwnd           : App handle
    # @return       None
    @staticmethod
    def set_foreground(hwnd):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    ##
    # @brief        maximise  : Method to maximise the current window
    # @param[in]    hwnd      : App handle
    # @return       None
    @classmethod
    def maximise(cls, hwnd):
        logging.info(f"Maximising window for {cls.app_text}")
        cls.set_foreground(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    ##
    # @brief        snap_mode  : Static_method to enable media controls while playing media
    # @return       None
    @staticmethod
    def enable_media_controls():
        pass

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    cls           : Class
    # @param[in]    hwnd          : App handle
    # @param[in]    position      : Where the app should be positioned, top or bottom of the screen
    # @return       None
    @classmethod
    def set_half_size(cls, hwnd, position="top"):
        monitor_dimension = window_helper.enum_display_monitors()
        screen_index = cls._get_app_screen(hwnd)
        ml, mt, mr, mb = monitor_dimension[screen_index]
        screen_width, screen_height = abs(mr - ml), abs(mt - mb)
        rand_x, rand_y = random.sample(range(0, 100), 2)
        if position == "down":
            window_helper.MoveWindow(hwnd, ml + screen_width // 2, mt + screen_height // 2, screen_width // 2 - 50,
                                     screen_height // 2 - 50, True)
        else:
            window_helper.MoveWindow(hwnd, ml + rand_x, mt + rand_y, screen_width // 2 - 50, screen_height // 2 - 50,
                                     True)

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    cls        : Class
    # @param[in]    hwnd       : App handle
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @param[in]    resolution : Optional parameter, the current app-rectangle size
    # @return       directions
    @classmethod
    def resize(cls, hwnd, multiplier, direction, resolution=None):
        cls.set_foreground(hwnd)
        if resolution is None:
            x0, y0, x1, y1 = window_helper.GetWindowPlacement(hwnd)[4]
        else:
            x0, y0, x1, y1 = resolution

        monitor_dimension = window_helper.enum_display_monitors()
        screen_index = cls._get_app_screen(hwnd)
        sl_left, sl_top, sl_right, sl_bottom = monitor_dimension[screen_index]

        mx, my = multiplier
        logging.info(f"Resizing {cls.app_text} by {10 * abs(mx)} pixels width and {10 * abs(my)} pixels height")
        dirX, dirY = direction
        logging.info(f"Resizing {cls.app_text} in {direction[0]}-{direction[1]} direction")
        directions = {"right": x1, "left": x0, "top": y0, "bottom": y1}

        if dirX == "left":
            mx = -mx
        if dirY == "top":
            my = -my

        xs, ys = 0, 0
        logging.debug(f"app coordinates before resize{directions}")
        logging.debug(f"screen coordinates {monitor_dimension[screen_index]}")
        while xs != abs(mx) or ys != abs(my):
            if xs != abs(mx):
                if dirX == "right":
                    directions[dirX] = min((directions[dirX] + 10), sl_right) if mx > 0 else max(
                        (directions[dirX] - 10),
                        directions["left"])
                else:
                    directions[dirX] = min((directions[dirX] + 10), directions["right"]) if mx > 0 else max(
                        (directions[dirX] - 10), sl_left)
                xs += 1
            if ys != abs(my):
                if dirY == "bottom" and abs(my != ys):
                    directions[dirY] = min((directions[dirY] + 10), sl_bottom) if my > 0 else max(
                        (directions[dirY] - 10),
                        directions["top"])
                else:
                    directions[dirY] = min((directions[dirY] + 10), directions["bottom"]) if my > 0 else max(
                        (directions[dirY] - 10), sl_top)
                ys += 1
            logging.debug(f"current app coordinates{directions}")
            width = directions["right"] - directions["left"]
            height = directions["bottom"] - directions["top"]

            window_helper.MoveWindow(hwnd, directions["left"], directions["top"],
                                     width, height, True)

            time.sleep(0.01)

        return (directions["left"], directions["top"],
                directions["right"], directions["bottom"])

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    hwnd          : App handle
    # @return       None
    @staticmethod
    def _get_app_screen(hwnd):
        monitor_dimension = window_helper.enum_display_monitors()
        win_index = None
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        for i in range(len(monitor_dimension)):
            l, t, r, b = monitor_dimension[i]
            win_index = i

        if win_index is None:
            logging.error("Unable to find screen for App coordinates")
            logging.info(
                f"App coordinates->{l},{t},{r},{b} was not found in any of the screen coordinates {monitor_dimension}")
            raise Exception("Unable to find screen for App coordinates")

        return win_index

    ##
    # @brief        _enable_disable_developer_mode : Enables/disables developer mode
    # @param[in]    value                          : Enum Enable or Disable
    # @return       None
    @staticmethod
    def _enable_disable_developer_mode(value):
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"Software\Microsoft")
        if registry_access.write(args=reg_args, reg_name="AllowDevelopmentWithoutDevLicense",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=value,
                                 sub_key=r"Windows\CurrentVersion\AppModelUnlock") is False:
            logging.error(
                f"Failed to {'Enable' if value == RegistryStatus.ENABLE else 'Disable'} Developer mode on Windows")
        else:
            logging.info(
                f"Successfully {'Enabled' if value == RegistryStatus.ENABLE else 'Disabled'} Developer mode on Windows")

    ##
    # @brief        disable_push_notifications : Disables push notifications
    # @return       None
    @staticmethod
    def disable_push_notifications():
        logging.debug("Disabling Push Notifications")
        hkey = "HKEY_CURRENT_USER"
        registry_path = "Software\\Microsoft\\Windows\\CurrentVersion"
        key_name = "PushNotifications"
        value = 0x0
        cmd = "bin\subinacl"
        os.system('%s /keyreg %s\%s /grant="%s"=f' % (cmd, hkey, hkey + "\\" + registry_path, getpass.getuser()))
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=registry_path)
        registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                              reg_value=value)

    ##
    # @brief        snap_mode  : Static_method to enable charms
    # @return       None
    @staticmethod
    def enable_charms():
        winkb_helper.press('WIN+P')
        logging.info("Enabled charms(WIN + P)")
        time.sleep(1)

    ##
    # @brief        snap_mode  : Static_method to disable charms
    # @return       None
    @staticmethod
    def disable_charms():
        winkb_helper.press('ESC')
        logging.info("Disabled charms (WIN + P)")
        time.sleep(1)

    ##
    # @brief        screenshot : To capture screen
    # @param[in]    name       : substring to be in the captured file name
    # @return       None
    @staticmethod
    def screenshot():
        import PIL.ImageGrab
        screenshot = PIL.ImageGrab.grab()
        filename = os.path.join(os.getcwd(), "Logs", f"Screenshot_{time.time()}.jpg")
        screenshot.save(filename)
        logging.info(f"Screenshot saved f{filename}")

    ##
    # @brief        open_media_using_cmd : Enables/disables developer mode
    # @param[in]    media_file           : Path to media file
    # @return       status               : True or False
    @staticmethod
    def open_media_using_cmd(media_file):
        media_applications = ["Films & TV", "Media Player", "Movies & TV", "Windows Media Player",
                              "Windows Media Player Legacy"]
        window_helper.close_media_player()
        time.sleep(3)
        cmd_line = r'start "mswindowsvideo://" "{0}"'.format(media_file)
        os.system(cmd_line)
        active_application_list = window_helper.get_windows().keys()
        app_name = list(set(media_applications) & set(active_application_list))
        hwnd = None if list(set(media_applications) & set(active_application_list)) == [] else \
            [x[0] for x in window_helper.enum_windows() if app_name[0] in x[1]][0]
        return hwnd


##
# # @brief    Class for Media
class AppMedia(App):
    app_text = AppText.MOVIES_AND_TV

    ##
    # @brief        __init__  : Function of the class
    # @param[in]    file_path : Path to the media file
    def __init__(self, file_path):
        self.instance = None
        self.hwnd = None
        self.fullscreen = None
        self.resolution = None
        self.media_file = file_path

    ##
    # @brief        set_app_path : Currently not implemented for Media as it is not required
    # @param[in]    file_path    : path of the file
    # @return       None
    def set_app_path(self, file_path):
        return NotImplemented

    ##
    # @brief            __play_media : To play media
    # @param[in]        media_file   : Media that needs to be played
    # @param[in]	    fullscreen  : Mode in which 3D application to be launched
    # @return		    media_window_handle
    def __play_media(self, media_file, fullscreen):
        active_media_app = None
        media_applications = ["Films & TV", "Media Player", "Movies & TV", "Windows Media Player",
                              "Windows Media Player Legacy"]

        mode = " full screen mode" if fullscreen else " windowed mode"

        flag = True
        count = 0

        while flag and count < 5:
            logging.debug("Launching media playback application in" + mode)

            self.disable_push_notifications()

            window_helper.open_uri(media_file)
            time.sleep(5)

            active_application_list = window_helper.get_windows().keys()
            logging.debug(f"Active apps Trial:{count}: {active_application_list}")

            flag = True if list(set(media_applications) & set(active_application_list)) == [] else False

            if flag:
                time.sleep(5)
                flag = True if list(set(media_applications) & set(active_application_list)) == [] else False
                if flag:
                    count += 1
                    if count >= 5:
                        logging.error(f"Active Application List: {active_application_list}")
                        raise Exception("Active Media Applications not found")
                    continue

            active_media_app = list(set(media_applications) & set(active_application_list))[0]
            self.app_text = active_media_app

            # sleep for 5 more seconds to confirm the app is still open
            time.sleep(5)
            flag = True if list(set(media_applications) & set(active_application_list)) == [] else False
            if flag:
                if count < 5:
                    count += 1
                    logging.info(f"App instance not present in active applications, trying again Attempt {count}")
                else:
                    raise Exception("All attempts to open the app Failed")

        media_window_handle = window_helper.get_window(active_media_app, True)
        if media_window_handle is None:
            raise Exception(f"Application {self.app_text} didn't open")

        try:
            self.hwnd = [x[0] for x in window_helper.enum_windows() if self.app_text in x[1]][0]
            logging.debug(f"handle: {self.hwnd}")
        except IndexError:
            raise Exception(f"Handle NOT found for {self.app_text}")
        self.set_foreground(self.hwnd)
        logging.info(f"Successfully launched {self.app_text} application in {mode}")
        return media_window_handle

    ##
    # @brief            check_app_status_and_controls : To check active status and controls of the app
    # @return		    status                        : True or False
    def check_app_status_and_controls(self):
        self.hwnd = self.open_media_using_cmd(self.media_file)
        if self.hwnd:
            winkb_helper.press('ESC')
            time.sleep(2)
            return True
        else:
            self.hwnd = self.open_media_using_cmd(self.media_file)
            if self.hwnd:
                winkb_helper.press('ESC')
                time.sleep(2)
                return True
            else:
                return False

    ##
    # @brief        open_app        : Function which facilitates opening of the app
    # @param[in]    is_full_screen  : Bool, whether the app has to be opened in full screen/not
    # @param[in]    minimize        : Bool, whether all current windows have to be minimized prior to opening the app
    # @param[in]    position        : Where the app has to be opened on screen, top or bottom
    # @return       None
    def open_app(self, is_full_screen=False, minimize=False, position="top"):
        # Close all the media player previously opened
        window_helper.close_media_player()
        time.sleep(3)

        self.fullscreen = is_full_screen
        if minimize:
            # Minimize all the windows
            winkb_helper.press('WIN+M')

        ##
        # Play media content in windowed mode
        self.instance = self.__play_media(self.media_file, fullscreen=is_full_screen)

        ##
        # Enable repeat
        winkb_helper.press("CTRL+T")

        if is_full_screen:
            if self.app_text is AppText.MEDIA_PLAYER:
                winkb_helper.press('F11')
            else:
                # Play the video in full screen mode
                winkb_helper.press("ALT_ENTER")
            time.sleep(2)

            ##
            # Remove focus from play/pause button
            winkb_helper.press('ESC')
            time.sleep(0.2)

    ##
    # @brief        close app : Function for closing the app
    # @return       None
    def close_app(self):
        # Close media player
        window_helper.close_media_player()
        logging.info(f"Closed {self.app_text} application")

    ##
    # @brief        enable media controls : Function for enabling media controls in media playback
    # @return       None
    def enable_media_controls(self):
        # enable media controlled when the app in windowed mode
        if not self.fullscreen:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            rand_x, rand_y = random.randrange(left, right), random.randrange(top, bottom // 2)
            win32api.SetCursorPos((rand_x, rand_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 5, 5)
        logging.info("Enabled media controls")

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed eg(("right", "bottom"))
    # @return       None
    def resize(self, multiplier, direction):
        self.resolution = super().resize(self.hwnd, multiplier, direction, self.resolution)

    ##
    # @brief        maximise        : Maximising the screen
    # @return       None
    def maximise(self):
        super().maximise(self.hwnd)

    ##
    # @brief        drag       : To drag the app in the direction specified
    # @param[in]    panel      : Panel value to which the app has to be dragged
    # @param[in]    gfx_index  : Gfx adapter to which the app has to be dragged
    # @return       None
    def drag(self, panel, gfx_index):
        super().drag(panel, gfx_index, self.hwnd)

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        super().set_half_size(self.hwnd, position)

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        super().snap_mode(self.hwnd, direction)

    ##
    # @brief        disable_controls_in_fullscreen  : Disable player controls in fullscreen by clicking in the middle
    # @return       None
    def disable_controls_in_fullscreen(self):
        self.set_foreground(self.hwnd)
        logging.info("Emulating left click to exit display controls")
        x0, y0, x1, y1 = win32gui.GetWindowRect(self.hwnd)
        mid_x, mid_y = int(x0 + (x1 - x0) * 0.75), y0 + int((y1 - y0) * 0.75)
        win32api.SetCursorPos((mid_x, mid_y // 2))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mid_x, mid_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mid_x, mid_y, 0, 0)
        time.sleep(5)

    ##
    # @brief        pause_resume  : Pause or resume while playing the video
    # @return       None
    def pause_resume(self):
        self.set_foreground(self.hwnd)
        winkb_helper.press(' ')

    ##
    # @brief        get_current_screen_size  : Get the current dimensions of the player, can be used for debug
    # @return       None
    def get_current_screen_size(self):
        self.set_foreground(self.hwnd)
        logging.info(win32gui.GetWindowPlacement(self.hwnd))
        return dict(zip(("left", "top", "right", "bottom"), win32gui.GetWindowPlacement(self.hwnd)[4]))


##
# @brief    Factory class for various app objects
class App3D(App):
    app_text = AppText.FLIPAT

    ##
    # @brief        __init__  : Function of the class
    # @param[in]    app_name  : Str, name of the app
    # @param[in]    app_path  : Str, path of the app
    # @param[in]    cwd       : Str, current working directory
    def __init__(self, app_name, app_path=None, cwd=None):
        self.instance = None
        self.hwnd = None
        self.fullscreen = None
        self.resolution = None
        self.app_text = app_name
        self.cwd = None
        self.developer_mode = False
        if app_path is not None:
            self.set_app_path(app_path, cwd)

    ##
    # @brief        set_app_path    : Set path for the app
    # @param[in]    app_path        : Str, path of the app
    # @param[in]    cwd             : Str, current working directory
    # @return       None
    def set_app_path(self, app_path, cwd=None):
        self.app_path = app_path
        self.cwd = cwd

    ##
    # @brief        open_app              : Function which facilitates opening of the app
    # @param[in]    is_full_screen        : Bool, whether the app has to be opened in full screen/not
    # @param[in]    minimize              : Bool, whether all current windows have to be minimized prior to opening the
    #                                       app
    # @param[in]    position              : Str, where the app has to be placed (top/bottom)
    # @param[in]    enable_developer_mode : Bool, whether to enable developer mode or not
    # @param[in]    close_dx_apps         : Bool, whether to close existing dx apps/not
    # @return       None
    def open_app(self, is_full_screen=False, minimize=False, position="top", enable_developer_mode=False,
                 close_dx_apps=False):
        app_window_handle = None
        # Close all the dx-apps previously opened
        if close_dx_apps:
            window_helper.close_dx_apps()
        if enable_developer_mode:
            self._enable_disable_developer_mode(RegistryStatus.ENABLE)
            self.developer_mode = True
        if minimize:
            # Minimize all the windows
            winkb_helper.press('WIN+M')
        mode = "full screen mode " if is_full_screen else "windowed mode"
        logging.info(f"Launching {self.app_text} App in {mode}")

        self.instance = Popen(self.app_path, cwd=self.cwd)
        time.sleep(5)
        active_application_list = window_helper.get_windows().keys()
        logging.info(f"Active apps: {active_application_list}")
        try:
            app_window_handle = window_helper.get_window(AppText[self.app_text.upper()].value)
            logging.info(f'In Try app_window_handle = {app_window_handle}')
            if app_window_handle is None:
                raise TypeError
        except TypeError:
            active_application_list = window_helper.get_windows().keys()
            logging.debug(f"Active apps Try1: {active_application_list}")
            count = 0
            while count < 3:
                count += 1
                self.instance = Popen(self.app_path, cwd=self.cwd)
                time.sleep(5)
                active_application_list = window_helper.get_windows().keys()
                logging.debug(f"Active apps Try-2: {active_application_list}")
                try:
                    app_window_handle = window_helper.get_window(AppText[self.app_text.upper()].value)
                    if app_window_handle is None:
                        raise TypeError
                    else:
                        break
                except TypeError:
                    if count < 3:
                        pass
                    else:
                        logging.error(f"Active Application List: {active_application_list}")
                        raise Exception("Active Applications not found")
        if self.instance is None:
            raise Exception(f"{self.app_text} Application did not open in {mode}")
        logging.info(f"Launched {self.app_text} App successfully in {mode}")
        if app_window_handle is None:
            raise Exception(f"Application {self.app_text} didn't open")
        self.hwnd = [x[0] for x in window_helper.enum_windows() if AppText[self.app_text.upper()].value in x[1]][0]
        self.fullscreen = is_full_screen
        if not is_full_screen:
            self.set_half_size(position=position)
        else:
            if self.app_text.upper() == 'FLIPAT':
                winkb_helper.press(' ')
                time.sleep(0.2)
            if self.app_text.upper() == 'FLIPMODELD3D12' or self.app_text.upper() == 'TRIVFLIP':
                winkb_helper.press('F11')
                time.sleep(0.2)
            if self.app_text.upper() == 'CLASSICD3D':
                winkb_helper.press('F5')
                time.sleep(0.2)
            if self.app_text.upper() == 'D3D12FULLSCREEN':
                winkb_helper.press('ALT_ENTER')
                time.sleep(0.2)
        return app_window_handle

    ##
    # @brief        close app : Function for closing the app
    # @return       status    : Boolean to denote the status
    def close_app(self):
        if self.instance is None:
            logging.warning("App instance is not open")
            return False

        self.instance.terminate()
        self.instance = None
        logging.info(f"Closed {self.app_text}")
        ##
        # To disable developer mode
        if self.developer_mode:
            self._enable_disable_developer_mode(RegistryStatus.DISABLE)
        return True

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @return       None
    def resize(self, multiplier, direction):
        self.resolution = super().resize(self.hwnd, multiplier, direction, self.resolution)

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        super().set_half_size(self.hwnd, position)

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        super().snap_mode(self.hwnd, direction)

    ##
    # @brief        maximise : Maximising the screen
    # @return       None
    def maximise(self):
        super().maximise(self.hwnd)


##
# @brief    Class for PresentAt, derived from 3DApp
class PresentAtApp(App3D):
    app_text = "PRESENTAT"

    ##
    # # @brief    Enum for orientation of the app in screen
    class ORIENTATION(Enum):
        FULLSCREEN = 0
        LEFT_PANE = 1
        RIGHT_PANE = 2

    ##
    # # @brief    Enum for setting the interval for calling setInterruptTargetpresentID
    class SETINTGTPIDINTERVAL(Enum):
        REPORT_ALL_FLIPS = 0
        REPORT_ALTERNATE_FLIPS = 1
        REPORT_MAX_QUEUE_SIZE = 2

    isValid = staticmethod(lambda val, cls: val in cls.__members__)

    ##
    # @brief        __init__            : Function of the class
    # @param[in]    app_path            : Path of the app
    # @param[in]    queueDepth          : QueueDepth
    # @param[in]    setInTgtPIDInterval : Interval at which setInterruptTargetPresentID has to be called
    # @param[in]    fps                 : FPS of the app
    # @param[in]    position            : The position of app in the screen
    def __init__(self, app_path, queueDepth=8, setInTgtPIDInterval="REPORT_ALL_FLIPS", fps=0,
                 position="FULLSCREEN"):
        assert self.isValid(position, self.ORIENTATION), "INVALID orientation"
        assert self.isValid(setInTgtPIDInterval,
                            self.SETINTGTPIDINTERVAL), "INVALID SetInterruptTargetPresentID Interval"
        self.position = self.ORIENTATION[position]
        self.setInTgtPIDInterval = self.SETINTGTPIDINTERVAL[setInTgtPIDInterval]
        self.fps = fps
        self.queueDepth = queueDepth
        self.app_path = app_path
        self.cwd = None
        self.developer_mode = False
        self.resolution = None

    ##
    # @brief        open_app              : Function which facilitates opening of the app
    # @param[in]    is_full_screen        : Bool, whether the app has to be opened in full screen/not - keeping for
    #                                       compatibility
    # @param[in]    minimize              : Bool, whether all current windows have to be minimized prior to opening
    #                                       the app
    # @return       app_instance          : App instance
    def open_app(self, is_full_screen=False, minimize=False):
        logging.info(f"Launching {self.app_text} App in {self.position}")

        self.app_path = self.app_path + f" -d {self.queueDepth} -r {self.setInTgtPIDInterval.value} " \
                                        f"-rr {self.fps} -p {self.position.value}"

        # making fullscreen True, as the parent calls set_half_size for windowed mode, which is not required here
        return super().open_app(is_full_screen=True)


##
# @brief    Factory class for various app objects
class BoostedApp(App):
    app_text = AppText.BOOSTED_APP

    ##
    # @brief        __init__  : Function of the class
    # @param[in]    cwd       : Str, current working directory
    def __init__(self, cwd=None):
        self.instance = None
        self.hwnd = None
        self.set_app_path()

    ##
    # @brief        set_app_path : Set path of the app
    # @return       None
    # todo app is not currently deployed to sharedbinary, as it has issues, have to move the app after resolving this
    def set_app_path(self):
        self.cwd = NotImplemented

    ##
    # @brief        open_app : Function which facilitates opening of the app
    # @return       status   : App opened succesfully or not
    def open_app(self):
        cmdline = "te.exe ./virtualrefreshrate.dll /name:*durationimplementation*".split()
        command = [os.path.join(self.cwd, cmdline[0])] + cmdline[1:]
        self.instance = Popen(command, shell=True, stdout=PIPE, cwd=self.cwd)
        if self.instance:
            logging.info("Opened the virtualRefreshRate tool with durationImplementation test")
        else:
            logging.error("Unable to open VirtualRefreshRateTool")
            return False
        return True

    ##
    # @brief        close app : Function for closing the app
    # @return       None
    def close_app(self):
        if self.instance is None:
            logging.warning("App instance is not open")
            return False
        self.instance.terminate()
        logging.info("Closed the virtualRefreshRate tool")
        self.instance = None

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @return       None
    def resize(self, multiplier, direction):
        return NotImplemented

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        return NotImplemented

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        return NotImplemented


##
# @brief    Factory class for various app objects
class SnipSketch(App):
    app_text = AppText.SNIP_AND_SKETCH

    ##
    # @brief        __init__ : Function of the class
    def __init__(self):
        self.instance = None
        self.hwnd = None
        self.set_app_path()

    ##
    # @brief        set_app_path : Set path of the app
    # @return       None
    def set_app_path(self):
        self.cmdline = ["start", "ms-penworkspace://Capture"]

    ##
    # @brief        open_app        : Function which facilitates opening of the app
    # @param[in]    maximize        : Bool, whether the current window need to be maximized or not
    # @return       status          : Opening app successful or not
    def open_app(self, maximize=True):
        trials_left = 3
        while True:
            self.instance = Popen(self.cmdline, shell=True)
            time.sleep(1)
            try:
                self.hwnd = [x[0] for x in window_helper.enum_windows()
                             if self.app_text.value.upper() in x[1].upper()][0]
                break
            except AssertionError as e:
                trials_left -= 1
                logging.error(f"Failure while opening the app, Trying again : Trials left {trials_left}")
                if not trials_left:
                    logging.error(f"Assertion error : {e}")
                    return False
                time.sleep(10)
            except IndexError:
                time.sleep(5)
                if self.instance:
                    flag = False
                    for text_ in [AppText.SNIPPING_TOOL.value, self.app_text.value]:
                        for handle, app_txt, _ in window_helper.enum_windows():
                            if app_txt.upper() == text_.upper():
                                self.hwnd = handle
                                flag = True
                                break
                        if flag:
                            break
                    if not flag:
                        trials_left -= 1
                        logging.error(f"Failure while opening the app, Trying again : Trials left {trials_left}")
                        if not trials_left:
                            return False
                        time.sleep(10)
                    else:
                        break
                else:
                    logging.error(f"App instance not open for {self.app_text}")
                    return False

        if maximize is True:
            self.maximise()
        else:
            self.snap_mode("right")
        return True

    ##
    # @brief        open_app : Function which facilitates opening of the app
    # @param[in]    duration : Duration for which drawing on the app has to be done
    # @return       None
    def draw_random(self, duration):
        start_time = time.time()
        for text_ in [AppText.SNIPPING_TOOL.value, self.app_text.value]:
            for handle, app_txt, _ in window_helper.enum_windows():
                if app_txt.upper() == text_.upper():
                    self.hwnd = handle
        self.set_foreground(self.hwnd)
        x0, y0, x1, y1 = win32gui.GetWindowRect(self.hwnd)
        mul = [(-3, -3), (-3, 3), (3, 3), (3, -3)]
        mid_x, mid_y = int(x0 + (x1 - x0) * 0.75), y0 + int((y1 - y0) * 0.75)
        win32api.SetCursorPos((mid_x, mid_y // 2))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mid_x, mid_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mid_x, mid_y, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mid_x, mid_y, 0, 0)
        randlist = [list(random.randrange(10, 70) for i in range(2)) for i in range(5)]
        logging.info("Drawing randomly on snip and sketch app")
        while time.time() - start_time < duration:
            random.shuffle(randlist)
            for rand_x, rand_y in randlist:
                for mx, my in mul:
                    i, j = rand_x, rand_y // 2
                    while mx != 0 or my != 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, mx, my, 0, 0)
                        logging.debug(f"current mouse coordinate mouse_x:{mx}, mouse_y:{my}")
                        time.sleep(0.00005)
                        if i != 0:
                            i -= 1
                        else:
                            mx = 0
                        if j != 0:
                            j -= 1
                        else:
                            my = 0
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logging.info("Stopping the inking")

    ##
    # @brief        random_mouse_move : Function which helps to move the mouse cursor randomly across screen
    # @param[in]    duration          : Duration for which drawing on the app has to be done
    # @return       None
    def random_mouse_move(self, duration):
        start_time = time.time()
        randlist = [list(random.randrange(10, 70) for i in range(2)) for i in range(5)]
        mul = [(-3, -3), (-3, 3), (3, 3), (3, -3)]
        logging.debug("Moving the mouse randomly")
        while time.time() - start_time < duration:
            random.shuffle(randlist)
            for rand_x, rand_y in randlist:
                for mx, my in mul:
                    i, j = rand_x, rand_y // 2
                    while mx != 0 or my != 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, mx, my, 0, 0)
                        logging.debug(f"current mouse coordinate mouse_x:{mx}, mouse_y:{my}")
                        time.sleep(0.00005)
                        if i != 0:
                            i -= 1
                        else:
                            mx = 0
                        if j != 0:
                            j -= 1
                        else:
                            my = 0
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logging.debug("Stopping the mouse movement")

    ##
    # @brief        close app : Function for closing the app
    # @return       None
    def close_app(self):
        logging.info(f"Closing {self.app_text.value}")
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        logging.info(f"Closed {self.app_text}")

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @return       None
    def resize(self, multiplier, direction):
        return NotImplemented

    ##
    # @brief        maximise : maximising the screen
    # @return       None
    def maximise(self):
        super().maximise(self.hwnd)

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        return NotImplemented

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        super().snap_mode(self.hwnd, direction)

    ##
    # @brief        drag       : To drag the app in the direction specified
    # @param[in]    panel      : Panel value to which the app has to be dragged
    # @param[in]    gfx_index  : Gfx adapter to which the app has to be dragged
    # @return       None
    def drag(self, panel, gfx_index):
        super().drag(panel, gfx_index, self.hwnd)


##
# @brief    Class for YouTube
class Youtube(App):
    app_text = "YOUTUBE"

    ##
    # @brief        __init__   : Function of the class
    # @param[in]    video_path : Path to YouTube video
    # @param[in]    cwd        : Current working directory
    def __init__(self, video_path=None, cwd=None):
        self.hwnd = None
        if video_path is not None:
            self.set_app_path(video_path, cwd)

    ##
    # @brief        set_app_path    : Set path for the app
    # @param[in]    video_path      : Str, path to youtube video
    # @param[in]    cwd             : Str, current working directory
    # @return       None
    def set_app_path(self, video_path, cwd=None):
        self.video_path = video_path
        self.cwd = cwd

    ##
    # @brief        open_app              : Function which facilitates opening of the app
    # @param[in]    is_full_screen        : Bool, whether the app has to be opened in full screen/not
    # @param[in]    minimize              : Bool, whether all current windows have to be minimized
    # @param[in]    position              : Where the app has to be opened on screen, top or bottom
    # @param[in]    close_web_browser     : Bool, close previously opened web browsers
    # @return       app_handle            : Window handle of the app
    def open_app(self, is_full_screen=False, minimize=False, position="top", close_web_browser=True):
        mode = "fullscreen" if is_full_screen else "windowed"
        logging.info(f"Launching {self.app_text} in {mode} mode")
        window_helper.close_browser()
        time.sleep(3)

        if minimize:
            # Minimize all the windows
            winkb_helper.press('WIN+M')

        ##
        # Open YouTube in windowed/fullscreen mode
        handle = window_helper.open_web_page(self.video_path, is_full_screen)

        ##
        # To skip before you continue to YouTube popup
        for i in range(4):
            winkb_helper.press('TAB')
            time.sleep(0.2)
        winkb_helper.press('ENTER')

        self.hwnd = [x[0] for x in window_helper.enum_windows() if AppText[self.app_text.upper()].value in x[1]][0]

        if is_full_screen:
            winkb_helper.press('F')
            time.sleep(1)

        return self.hwnd

    ##
    # @brief        close app : Function for closing the app
    # @return       None
    def close_app(self):
        window_helper.close_browser()
        logging.info(f"Closed {self.app_text}")

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*multiplier) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @return       None
    def resize(self, multiplier, direction):
        return NotImplemented

    ##
    # @brief        maximise : Maximising the screen
    # @return       None
    def maximise(self):
        return NotImplemented

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        return NotImplemented

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        super().snap_mode(self.hwnd, direction)

    ##
    # @brief        drag       : To drag the app in the direction specified
    # @param[in]    panel      : Panel value to which the app has to be dragged
    # @param[in]    gfx_index  : Gfx adapter to which the app has to be dragged
    # @return       None
    def drag(self, panel, gfx_index):
        super().drag(panel, gfx_index, self.hwnd)

    ##
    # @brief        enable_disable_captions : Function to enable and disable captions
    # @return       None
    @staticmethod
    def enable_disable_captions():
        winkb_helper.press('C')

    ##
    # @brief        enable_disable_fullscreen : Function to enable and disable fullscreen
    # @return       None
    @staticmethod
    def enable_disable_fullscreen():
        winkb_helper.press('F')

    ##
    # @brief        enable_disable_cinema_mode : Function to enable and disable cinema mode
    # @return       None
    @staticmethod
    def enable_disable_cinema_mode():
        winkb_helper.press('T')

    ##
    # @brief        enable_disable_mini_player : Function to enable and disable mini player
    # @return       None
    @staticmethod
    def enable_disable_mini_player():
        winkb_helper.press('I')

    ##
    # @brief        play_pause : Function to play and pause
    # @return       None
    @staticmethod
    def play_pause():
        winkb_helper.press('K')

    ##
    # @brief        seek_forward : Function to seek forward 5 seconds
    # @return       None
    @staticmethod
    def seek_forward():
        winkb_helper.press('SHIFT+RIGHT')

    ##
    # @brief        seek_backward : Function to seek backward 5 seconds
    # @return       None
    @staticmethod
    def seek_backward():
        winkb_helper.press('SHIFT+LEFT')


##
# @brief    Class for VLC
class VLC(App):
    app_text = "VLC"

    ##
    # @brief        __init__   : Function of the class
    # @param[in]    video_path : Path to media file
    # @param[in]    cwd        : Current working directory
    def __init__(self, video_path=None, cwd=None):
        self.hwnd = None
        if video_path is not None:
            self.set_app_path(video_path, cwd)

    ##
    # @brief        set_app_path    : Set path for the app
    # @param[in]    video_path      : Str, path to youtube video
    # @param[in]    cwd             : Str, current working directory
    # @return       None
    def set_app_path(self, video_path, cwd=None):
        self.video_path = video_path
        self.cwd = cwd

    ##
    # @brief        open_app              : Function which facilitates opening of the app
    # @param[in]    is_full_screen        : Bool, whether the app has to be opened in full screen/not
    # @param[in]    minimize              : Bool, whether all current windows have to be minimized
    # @param[in]    position              : Where the app has to be opened on screen, top or bottom
    # @return       app_handle            : Window handle of the app
    def open_app(self, is_full_screen=False, minimize=False, position="top"):
        mode = "fullscreen" if is_full_screen else "windowed"
        logging.info(f"Launching {self.app_text} in {mode} mode")
        window_helper.close_media_player()
        time.sleep(3)

        if minimize:
            # Minimize all the windows
            winkb_helper.press('WIN+M')

        ##
        # Open media in windowed/fullscreen mode
        subprocess.run(f'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe {self.video_path}')

        winkb_helper.press('ENTER')

        ##
        # Enable repeat
        winkb_helper.press("L")

        self.hwnd = [x[0] for x in window_helper.enum_windows() if AppText[self.app_text.upper()].value in x[1]][0]

        if is_full_screen:
            winkb_helper.press('F')

        return self.hwnd

    ##
    # @brief        close app : Function for closing the app
    # @return       None
    def close_app(self):
        window_helper.close_media_player()
        logging.info(f"Closed {self.app_text}")

    ##
    # @brief        resize     : To resize the app in the direction with the multiplier value specified.
    # @param[in]    multiplier : Pixel multiplier value (10*mult) to be decreased in x and y direction resp.
    # @param[in]    direction  : Direction from which the resize has to be performed
    # @return       None
    def resize(self, multiplier, direction):
        return NotImplemented

    ##
    # @brief        maximise : Maximising the screen
    # @return       None
    def maximise(self):
        return NotImplemented

    ##
    # @brief        set_half_size : Set the app dimensions to half the size of the playing screen
    # @param[in]    position      : Position of the app
    # @return       None
    def set_half_size(self, position="top"):
        return NotImplemented

    ##
    # @brief        snap_mode  : Method to put the app in snap mode
    # @param[in]    direction  : Direction to which the app has to be snapped to left/right
    # @return       None
    def snap_mode(self, direction):
        super().snap_mode(self.hwnd, direction)

    ##
    # @brief        drag       : To drag the app in the direction specified
    # @param[in]    panel      : Panel value to which the app has to be dragged
    # @param[in]    gfx_index  : Gfx adapter to which the app has to be dragged
    # @return       None
    def drag(self, panel, gfx_index):
        super().drag(panel, gfx_index, self.hwnd)

    ##
    # @brief        enable_fullscreen : Function to enable fullscreen
    # @return       None
    @staticmethod
    def enable_fullscreen():
        winkb_helper.press('F')

    ##
    # @brief        disable_fullscreen : Function to disable fullscreen
    # @return       None

    @staticmethod
    def disable_fullscreen():
        winkb_helper.press('ESC')

    ##
    # @brief        play_pause : Function to play and pause
    # @return       None
    @staticmethod
    def play_pause():
        winkb_helper.press(' ')

    ##
    # @brief        seek_forward : Function to seek forward 4 seconds
    # @return       None
    @staticmethod
    def seek_forward():
        winkb_helper.press('SHIFT+RIGHT')

    ##
    # @brief        seek_backward : Function to seek backward 4 seconds
    # @return       None
    @staticmethod
    def seek_backward():
        winkb_helper.press('SHIFT+LEFT')
