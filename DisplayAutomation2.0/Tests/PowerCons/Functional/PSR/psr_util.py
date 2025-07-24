#######################################################################################################################
# @file         psr_util.py
# @brief        PSR Libs
# @details      This is the utility providing various PSR exit events for PSR verification. This is also covering
#               various selective update
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import random
import tkinter as tk
from ctypes import windll
from datetime import datetime
from functools import partial

from Libs.Core import app_controls

__timeline = []
__time_stamps = []

MAX_EVENTS = 150
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4

##
# Per monitor DPI aware. The app will check for the DPI when it will be created and adjusts the scale factor whenever
# the DPI changes. The application will not be automatically scaled by the system.
windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)


##
# @brief        Exposed class object for color palette
class Color(object):
    primary = "#7266ba"
    success = "#27c24c"
    info = "#0071c5"
    warning = "#fad733"
    danger = "#f05050"
    dark = "#3a3f51"
    light = "#dee5e7"
    white = "#fff"
    black = "#000"


##
# @brief        Initializes master frame and its components
# @param[in]    feature to classify psr_util based on frame requirement
# @param[in]    wait_time time in ms for frame change
# @param[in]    master_frame main window of application, tkinter instance (root)
# @param[in]    callback_time number, delay for frame update in ms
# @param[in]    monitor_ids a list of monitor ids
# @param[in]    max_events number, maximum number of events that can be generated for draw_box
# @param[in]    is_new_thread boolean indicates whether frame should be destroyed after
# @param[in]    signal_queue [optional], a queue of boolean indicating status of each draw box call
# @return       None
def __init_frame(feature, wait_time, master_frame, callback_time, monitor_id, max_events, is_new_thread, signal_queue):
    mi = app_controls.get_monitor_info(monitor_id)
    width = mi.rcMonitor.right - mi.rcMonitor.left
    height = mi.rcMonitor.bottom - mi.rcMonitor.top
    events = []
    if feature == "PSR":
        events = [
            (__draw_box, "FIRST_BLOCK_START", 0, 0, 10, 4, Color.primary),
            (__draw_box, "FIRST_BLOCK_MID", int(width / 2), 0, 10, 4, Color.primary),
            (__draw_box, "FIRST_BLOCK_END", width - 10, 0, 10, 4, Color.primary),
            (__draw_box, "LAST_BLOCK_START", 0, height - 4, 10, 4, Color.primary),
            (__draw_box, "LAST_BLOCK_MID", int(width / 2), height - 4, 10, 4, Color.primary),
            (__draw_box, "LAST_BLOCK_END", width - 10, height - 4, 10, 4, Color.primary),

            (__draw_boxes, "FIRST_DIAGONAL",
             [[0, 0, 10, 4], [int(width / 2), int(height / 2), 10, 4], [width - 10, height - 4, 10, 4]], Color.success),
            (__draw_boxes, "SECOND_DIAGONAL",
             [[width - 10, 0, 10, 4], [int(width / 2), int(height / 2), 10, 4], [0, height - 4, 10, 4]], Color.info),

            (__draw_box, "FIRST_VERTICAL_LINE", 0, 0, 1, height, Color.warning),
            (__draw_box, "LAST_VERTICAL_LINE", width - 1, 0, 1, height, Color.warning),

            (__draw_box, "LEFT_HALF_SCREEN", 0, 0, int(width / 2), height, Color.danger),
            (__draw_box, "RIGHT_HALF_SCREEN", int(width / 2), 0, width, height, Color.danger),

            (__draw_box, "TOP_HALF_SCREEN", 0, 0, width, int(height / 2), Color.dark),
            (__draw_box, "BOTTOM_HALF_SCREEN", 0, int(height / 2), width, height, Color.dark),

            (__draw_box, "FULL_SCREEN", 0, 0, width, height, Color.light)
        ]

    elif feature == "DPST":
        events = [
            (__draw_box, "FIRST_VERTICAL_LINE", 0, 0, 1, height, Color.warning),
            (__draw_box, "LAST_VERTICAL_LINE", width - 1, 0, 1, height, Color.warning),
            (__draw_box, "LEFT_HALF_SCREEN", 0, 0, int(width / 2), height, Color.danger),
            (__draw_box, "RIGHT_HALF_SCREEN", int(width / 2), 0, width, height, Color.danger),
            (__draw_box, "TOP_HALF_SCREEN", 0, 0, width, int(height / 2), Color.dark),
            (__draw_box, "BOTTOM_HALF_SCREEN", 0, int(height / 2), width, height, Color.dark),
            (__draw_box, "FULL_SCREEN", 0, 0, width, height, Color.light),
        ]
        events = events * 15

    if max_events is not None and 0 < max_events < MAX_EVENTS:
        events = events[10:11]
    else:
        random.shuffle(events)

    for event in events:
        if event[0] == __draw_box:
            f = partial(event[0], event[1], master_frame, event[2], event[3],
                        event[4], event[5], event[6], monitor_id, signal_queue)
            f.__name__ = "__draw_box"
            master_frame.after(ms=callback_time, func=f)
        else:
            f = partial(event[0], event[1], master_frame, event[2], event[3], monitor_id, signal_queue)
            f.__name__ = "__draw_boxes"
            master_frame.after(ms=callback_time, func=f)
        callback_time += wait_time

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
# @param[in]    signal_queue [optional], a queue of boolean indicating status of each draw box call
# @return       None
def __draw_box(event, frame, x=0, y=0, width=1, height=1, color=None, monitor_id=None, signal_queue=None):
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
    if signal_queue is not None:
        signal_queue.put(True)
    canvas_header = tk.Canvas(frame, bg=color, height=height, width=width, highlightthickness=0)
    canvas_header.place(x=x, y=y)


##
# @brief        Helper function to draw boxes
# @param[in]    event tuple containing details to call the draw_box/ draw_boxes function
# @param[in]    frame main root window
# @param[in]    cords co-ordinates for box/boxes
# @param[in]    color color for the box
# @param[in]    monitor_id [optional], a monitor id
# @param[in]    signal_queue [optional], a queue of boolean indicating status of each draw box call
# @return       None
def __draw_boxes(event, frame, cords, color, monitor_id=None, signal_queue=None):
    global __timeline
    t = datetime.now()
    __timeline.append({
        'type': 'FRAME_UPDATE',
        'name': event,
        'monitor_id': monitor_id,
        'time_stamp': t
    })
    __time_stamps.append(t)
    if signal_queue is not None:
        signal_queue.put(True)
    for box in cords:
        canvas_header = tk.Canvas(frame, bg=color, height=box[3], width=box[2], highlightthickness=0)
        canvas_header.place(x=box[0], y=box[1])


##
# @brief        Helper function to destroy frame
# @param[in]    frame
# @return       None
def __destroy(frame):
    frame.destroy()


##
# @brief        Exposed API to run the tool
# @param[in]    monitor_ids  a list of monitor ids
# @param[in]    max_events [optional], max number of events
# @param[in]    is_new_thread [optional], boolean, indicates if a new thread has to be created
# @param[in]    signal_queue [optional], signaling the queue for syncing
# @param[in]    feature [optional], to classify psr_util based on frame requirement
# @param[in]    wait_time time in ms for frame change duration
# @return       __output a list of dictionaries containing events and respective time stamps
def run(monitor_ids, max_events=None, is_new_thread=False, signal_queue=None, feature="PSR", wait_time=2000):
    ##
    # Validate arguments
    if not isinstance(monitor_ids, list) or len(monitor_ids) < 1:
        logging.error("\tInvalid arguments: monitor_ids= {0}".format(monitor_ids))
        return None

    root = None
    for monitor_id in monitor_ids:
        title = "PSR_UTIL_" + str(monitor_id)
        if root is None:
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
            root.title(title)
            frame = tk.Frame(root)
            frame.pack()
            __init_frame(
                feature, wait_time, root, callback_time=3000, monitor_id=monitor_id, max_events=max_events,
                is_new_thread=is_new_thread, signal_queue=signal_queue)
        else:
            new_window = tk.Toplevel(root)
            new_window.overrideredirect(True)
            new_window.geometry("{0}x{1}+0+0".format(new_window.winfo_screenwidth(), new_window.winfo_screenheight()))
            new_window.title(title)
            frame = tk.Frame(new_window)
            frame.pack()
            __init_frame(
                feature, wait_time, new_window, callback_time=2000, monitor_id=monitor_id, max_events=max_events,
                is_new_thread=is_new_thread, signal_queue=signal_queue)

        ##
        # Move window to targeted panel
        f = partial(app_controls.move_windows, title, monitor_id)
        f.__name__ = "move_windows"
        root.after(ms=1000, func=f)
    root.mainloop()
    return __timeline, __time_stamps
