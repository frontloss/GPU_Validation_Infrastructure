#######################################################################################################################
# @file        generate_frame.py
# @brief       Workload to generate different DPST patterns with various selective update
# @author      Tulika
#######################################################################################################################

import logging
import math
import os
import win32api
from enum import IntEnum

import pkgutil
import subprocess
import shutil
import time
import tkinter as tk
from ctypes import windll
from datetime import datetime
from functools import partial

from Libs.Core import app_controls, winkb_helper, registry_access
from Libs.Core.test_env import test_context
from Tests.PowerCons.Modules import desktop_controls

__timeline = []
__time_stamps = []

PROCESS_PER_MONITOR_DPI_AWARE = 2

##
# Per monitor DPI aware. The app will check for the DPI when it will be created and adjusts the scale factor whenever
# the DPI changes. The application will not be automatically scaled by the system.
windll.user32.SetProcessDPIAware(PROCESS_PER_MONITOR_DPI_AWARE)


##
# @brief        Registry Status Type
class RegistryStatus(IntEnum):
    DISABLE = 0
    ENABLE = 1


##
# @brief        Exposed class object for color palette
class Color(object):
    white = "#ffffff"
    black = "#000000"
    dark_grey = "#404040"
    light_grey = "#c0c0c0"
    purple = "#e0d0f0"


##
# @brief        Api to generate custom frame
# @param[in]    monitor_ids a list of monitor ids
# @param[in]    percent frame change in percentage
# @param[in]    color frame color
# @param[in]    frame_type frame_type
# @return       None
def __frame_type(monitor_id, area, color, frame_type):
    events = []
    mi = app_controls.get_monitor_info(monitor_id)
    width = mi.rcMonitor.right - mi.rcMonitor.left
    height = mi.rcMonitor.bottom - mi.rcMonitor.top
    match frame_type:
        case 'Single_Frame':
            events = [
                (__draw_box, "FULL_SCREEN", 0, 0, width, height, color[0]),
            ]
        case 'Double_Frame':
            events = [
                (__draw_box, "FULL_SCREEN", 0, 0, width, height, color[0]),
                (__draw_box, "CUSTOM_SCREEN", width / 2, height / 2, math.sqrt(area), math.sqrt(area), color[1])
            ]
    return events


##
# @brief        Initializes master frame and its components
# @param[in]    master_frame main window of application, tkinter instance (root)
# @param[in]    callback_time number, delay for frame update in ms
# @param[in]    monitor_ids a list of monitor ids
# @param[in]    is_new_thread boolean indicates whether frame should be destroyed after
# @param[in]    wait_time time in ms for frame change
# @param[in]    percent frame change in percentage
# @param[in]    color frame color
# @param[in]    frame_type frame_type
# @return       None
def __init_frame(master_frame, callback_time, monitor_id, is_new_thread, wait_time, area, color,
                 frame_type):
    events = __frame_type(monitor_id, area, color, frame_type)
    for event in events:
        if event[0] == __draw_box:
            f = partial(event[0], event[1], master_frame, event[2], event[3],
                        event[4], event[5], event[6], monitor_id)
            f.__name__ = "__draw_box"
            master_frame.after(ms=callback_time, func=f)
        callback_time += wait_time

    f = desktop_controls.create_display_bmp
    f.__name__ = "create_display_bmp"
    master_frame.after(ms=callback_time, func=f)

    if not is_new_thread:
        f = partial(__destroy, master_frame)
        f.__name__ = "__destroy"
        master_frame.after(ms=callback_time, func=f)


##
# @brief        Helper function to draw box based on the position and the size
# @param[in]    event tuple containing details to call the draw_box/ draw_boxes function
# @param[in]    frame main root window
# @param[in]    x [optional], x co-ordinate of a frame
# @param[in]    y [optional], y co-ordinate of a frame
# @param[in]    width [optional], width of the frame
# @param[in]    height [optional], height of the frame
# @param[in]    color [optional], color of the box
# @param[in]    monitor_id [optional], a monitor id
# @return       None
def __draw_box(event, frame, x=0, y=0, width=1, height=1, color=None, monitor_id=None):
    global __timeline
    global __time_stamps

    t = datetime.now()
    __timeline.append({
        'type': 'FRAME_UPDATE',
        'name': event,
        'monitor_id': monitor_id,
        'time_stamp': t
    })
    __time_stamps.append(t)
    canvas_header = tk.Canvas(frame, bg=color, height=height, width=width, highlightthickness=0)
    canvas_header.place(x=x, y=y)


##
# @brief        Helper function to destroy frame
# @param[in]    frame
# @return       None
def __destroy(frame):
    frame.destroy()


##
# @brief        Exposed API to generate frame
# @param[in]    is_new_thread [optional], boolean, indicates if a new thread has to be created
# @param[in]    wait_time time in ms for frame change
# @param[in]    area of the custom screen
# @param[in]    color frame color
# @param[in]    frame_type frame_type
# @return       None
def run_generate_frame(is_new_thread=False, wait_time=1000, area=None, color=None, frame_type=None):
    monitors = app_controls.get_enumerated_display_monitors()
    monitor_ids = [_[0] for _ in monitors]
    time.sleep(4)  # keeping delay for the ETL to start to make system idle
    logging.info("Step: Launching DPST Generate Frame App for continuous frame update")

    if not isinstance(monitor_ids, list) or len(monitor_ids) < 1:
        logging.error(f"\tInvalid arguments: monitor_ids= {monitor_ids}")
        return None

    root = None
    for monitor_id in monitor_ids:
        title = "DPST_WORKLOAD_" + str(monitor_id)
        if root is None:
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
            root.title(title)
            frame = tk.Frame(root)
            frame.pack()
            __init_frame(
                root, callback_time=3000, monitor_id=monitor_id, is_new_thread=is_new_thread,
                wait_time=wait_time, area=area, color=color, frame_type=frame_type)
        ##
        # Move window to targeted panel
        f = partial(app_controls.move_windows, title, monitor_id)
        f.__name__ = "move_windows"
        root.after(ms=1000, func=f)
    root.mainloop()


##
# @brief        Close the XPST image exe
# @return       None
def close_exe():
    logging.info("Closing XPST Image Exe")
    status = os.system('taskkill /f /im launch_frame.exe')
    if status != 0:
        raise AssertionError("XPST Image exe NOT closed")


##
# @brief        Open the XPST image exe
# @param[in]    width of the screen
# @param[in]    height of the screen
# @return       None
def launch_exe(width, height):
    logging.info("Launching XPST Image Exe")
    status = subprocess.run(f"pyinstaller --onefile --noconsole Tests\\PowerCons\\Functional\\DPST\\launch_frame.py",
                            capture_output=True)
    if status.returncode != 0:
        assert False, "Exe not generated"
    winkb_helper.press('WIN+M')
    command = ["-WIDTH", str(width), "-HEIGHT", str(height)]
    path_to_exe = os.path.join(test_context.ROOT_FOLDER, "dist\\launch_frame.exe")
    subprocess.Popen([path_to_exe] + command)
    time.sleep(20)
    # move cursor to right bottom
    win32api.SetCursorPos((win32api.GetSystemMetrics(0) + 1, win32api.GetSystemMetrics(1) + 1))


##
# @brief        Move Images to Log Folder
# @return       None
def move_image_file_to_folder():
    dir_name = "DpstKeiImages"
    path = os.path.join(test_context.LOG_FOLDER, dir_name)
    if os.path.isdir(path) is True:
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    for image in os.listdir(test_context.ROOT_FOLDER):
        if image.endswith('.png'):
            shutil.move(os.path.join(test_context.ROOT_FOLDER, image), path)


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
# @brief        Helper function to check python packages
# @param[in]    pkg_names
# @return       installed_packages
def are_packages_installed(pkg_names):
    installed_packages = {}
    available_modules = [module_info.name.upper() for module_info in pkgutil.iter_modules()]
    for pkg_name in pkg_names:
        installed_packages[pkg_name] = pkg_name.upper() in available_modules

    return installed_packages


##
# @brief        Helper function to install python packages
# @param[in]    installed_packages
# @return       None
def install_package(installed_packages):
    for package, install_status in installed_packages.items():
        if not install_status:
            pkg_install_cmd = f"pip install {package} --proxy http://proxy-dmz.intel.com:912"
            status = subprocess.run(pkg_install_cmd, capture_output=True)
            if status.returncode != 0:
                raise AssertionError(f"{package} not Installed")
        else:
            logging.info(f"{package} installed successfully")
