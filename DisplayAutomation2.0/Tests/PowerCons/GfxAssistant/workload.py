#######################################################################################################################
# @file         workload.py
# @brief        Contains APIs to run workloads (idle desktop, video, game etc...)
#
# @author       Ashish Tripathi, Rohit Kumar
#######################################################################################################################

import logging
import pickle
import random
import subprocess
import time
from typing import Dict

import win32api
import win32con
import win32gui

from Libs.Core import window_helper, app_controls, display_power
from Libs.Core import winkb_helper as kb
from Libs.Core.logger import html
from Tests.PowerCons.Functional.PSR import psr_util
from Tests.PowerCons.Modules import common
from Tests.PowerCons.GfxAssistant.workload_context import *

__vrr_app_state: Dict[str, object] = dict()
__monitor_id_mapping = None
__handle = None
__display_power = display_power.DisplayPower()


##
# @brief        Helper API to run the workload
# @param[in]    workload IDLE_DESKTOP/SCREEN_UPDATE/...
# @param[in]    workload_args list
#                   IDLE_DESKTOP = [duration]
#                   SCREEN_UPDATE = [monitor_ids]
#                   VIDEO_PLAYBACK = [media_fps, duration, pause=False, trace_video_playback_only=True]
#                       media_fps, Number
#                       duration, Number, in seconds
#                       pause[optional], Boolean - pause video in between for 5 seconds
#                       trace_video_playback_only[optional], Boolean - Option to control whether to include video
#                                                                      opening/closing events in traces
#                       power_event_during_playback[optional], Enum - CS/S3/S4
#                       power_source_event_during_playback[optional], Enum - AC/DC
#                   VIDEO_PLAYBACK_WITH_MOUSE_MOVE
#                   [media_fps, duration, start_delay=5, mouse_move_count=1, move_delay=15]
#                       media_fps, Number
#                       duration, Number, in seconds
#                       start_delay, Number, in seconds, delay before first mouse move event.
#                       mouse_move_count, Number, total number of mouse move events
#                       move_delay, Number, in seconds, delay between mouse move events
#                   GAME_PLAYBACK = [app, duration, full_screen]
#                       app, String, targeted app
#                       duration, Number, in seconds
#                       full_screen, Boolean
#                       power_event_during_playback[optional], Enum - CS/S3/S4
#                       power_source_event_during_playback[optional], Enum - AC/DC
#                       app_config[optional], object, app configuration
# @return       result, Status
def run(workload: Workload, workload_args):
    assert workload

    if workload == Workload.IDLE_DESKTOP:
        return __idle_desktop(workload_args)
    if workload == Workload.SCREEN_UPDATE:
        return __screen_update(workload_args)
    if workload == Workload.VIDEO_PLAYBACK:
        return __video_playback(workload_args)
    if workload == Workload.VIDEO_PLAYBACK_WITH_MOUSE_MOVE:
        return __video_playback_with_mouse_move(workload_args)
    if workload == Workload.GAME_PLAYBACK:
        return __game_playback(workload_args)

    return None


##
# @brief        Helper function to handle a power event during any workload
# @param[in]    power_event indicates the power state CS/S3/S4 ...
# @param[in]    power_source indicates the connected power source AC/DC
# @param[in]    delay number indicating the delay for power event/ power source change
# @return       True if power event or power source change was successful, False otherwise
def __handle_event_during_workload(power_event, power_source, delay=None):
    if delay is not None:
        time.sleep(delay)

    if power_event is not None:
        logging.info("\tTriggering power event {0} for 20 seconds".format(power_event.name))
        if __display_power.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            logging.error('\t\tFailed to invoke power event {0}'.format(power_event))
            return None
        logging.info("\t\tResumed from power event {0} successfully".format(power_event.name))

    if power_source is not None:
        logging.info("\tSetting Power Line Status to {0}".format(power_source))
        if not __display_power.set_current_powerline_status(power_source):
            logging.error("Failed to switch power line status to {0} (Test Issue)".format(power_source.name))
            return None
        logging.info("\t\tPASS: Expected Power Line status= {0}, Actual= {0}".format(power_source.name))
    return True


##
# @brief        Helper function to run the idle desktop workload
# @param[in]    workload_args contains the duration for idle desktop
# @return       True if desktop was idle successfully for the given duration
def __idle_desktop(workload_args):
    duration = workload_args[0]
    kb.press('WIN+M')
    html.step_start("Running Workload IDLE_DESKTOP for {0} seconds".format(duration))
    logging.info("\tKeeping desktop idle for {0} seconds".format(duration))
    time.sleep(duration)
    kb.press('ALT+TAB')

    return True


##
# @brief        Helper function to run the screen update workload
# @param[in]    workload_args contains the monitor id's required for screen update
# @return       True if screen update is successful
def __screen_update(workload_args):
    monitor_ids = workload_args[0]
    kb.press('WIN+M')
    html.step_start("Running Workload SCREEN_UPDATE")
    logging.info("\tPSR utility started")
    psr_util.run(monitor_ids)
    logging.info("\tPSR utility closed")
    kb.press('ALT+TAB')

    return True


##
# @brief        Helper function to run the video playback workload
# @param[in]    workload_args contains the video and duration of the playback
# @param[in]    mouse_args contains info on mouse movement during the playback
# @return       True if video playback is successful
def __video_playback(workload_args, mouse_args=None):
    video = workload_args[0]
    duration = workload_args[1]
    pause = False if len(workload_args) < 3 else workload_args[2]
    power_event_during_playback = None if len(workload_args) < 5 else workload_args[4]
    power_source_event_during_playback = None if len(workload_args) < 6 else workload_args[5]

    kb.press('WIN+M')

    html.step_start(f"Running Workload VIDEO_PLAYBACK for {duration} seconds")
    logging.info(f"\tVideo Playback started : {video}")
    app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, video))

    if mouse_args is not None:
        time.sleep(20 + mouse_args[0])  # delay before moving the mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 600, 600)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 605, 605)
        if mouse_args[0] < (duration / 2):
            time.sleep(int(duration / 2) - mouse_args[0])
    else:
        # Due to Win Qual sighting - DMRRS won't hit for ~20seconds
        time.sleep(int(duration / 2) + 20)

    # Handle pause/play event
    if pause is True:
        kb.press(' ')  # Pause
        time.sleep(5)
        logging.info("\tPaused video for 5 seconds")
        kb.press(' ')  # Play

    # Handle sleep/hibernate or power source switching during workload
    if __handle_event_during_workload(power_event_during_playback, power_source_event_during_playback) is not True:
        return None

    if mouse_args is not None:
        for _ in range(mouse_args[1] - 1):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 600, 600)
            time.sleep(0.2)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 605, 605)
            time.sleep(mouse_args[2])
        if ((mouse_args[1] - 1) * mouse_args[2]) < (duration / 2):
            time.sleep(int((duration / 2) - ((mouse_args[1] - 1) * mouse_args[2])))
    else:
        time.sleep(int(duration / 2))

    window_helper.close_media_player()
    logging.info("\tClosing video playback")

    return True


##
# @brief        Helper function to run the video playback workload with mouse mouse
# @param[in]    workload_args contains the video and duration of the playback
# @return       True if video playback is successful
def __video_playback_with_mouse_move(workload_args):
    # 5 seconds, 1 mouse event, 15 seconds
    mouse_args = [5, 1, 15]
    if len(workload_args) > 2:
        mouse_args[0] = workload_args[2]
    if len(workload_args) > 3:
        mouse_args[1] = workload_args[3]
    if len(workload_args) > 4:
        mouse_args[2] = workload_args[4]
    workload_args = workload_args[:2]

    return __video_playback(workload_args, mouse_args)


##
# @brief        Exposed API to open any VRR app
# @param[in]    app_name app to be opened
# @param[in]    full_screen True if app is expected to be launched in full screen mode, False otherwise
# @param[in]    graphics_setting graphics setting for AngryBots
# @param[in]    app_config Classic3DCubeAppConfig, app configuration for workload tests
# @return       True if operation is successful, False otherwise
def __open_app(app_name, full_screen, graphics_setting=None, app_config=None):
    global __vrr_app_state
    global __monitor_id_mapping
    global __handle

    if not full_screen:
        window_helper.minimize_all_windows()
        time.sleep(1)

    os.chdir(VRR_BIN_FOLDER)
    if app_name == Apps.AngryBotsGame:
        os.chdir(ANGRY_BOTS_FOLDER)

    # Workload test configuration
    if app_name == Apps.Classic3DCubeApp and app_config is not None:
        app_name += ' adapter:{0}'.format(app_config.adapter)
        app_name += ' gpupriority:{0}'.format(app_config.gpu_priority)
        app_name += ' interval:{0}'.format(app_config.interval)
        app_name += ' buffers:{0}'.format(app_config.buffers)
        app_name += ' presentationmodel:{0}'.format(app_config.presentation_model.name)
        app_name += ' rotationspeed:{0}'.format(app_config.rotation_speed)
        app_name += ' windowcount:{0}'.format(app_config.window_count)

        if app_config.gdi_compatible:
            app_name += ' gdicompatible'

        if app_config.dcomp:
            app_name += ' dcomp'

        if app_config.object_y_position is not None:
            app_name += ' yposition:{0}'.format(app_config.object_y_position)

        if app_config.test_display_mode_change:
            app_name += ' testdisplaymodechange'

        if app_config.test_window_device_destruction:
            app_name += ' testwindowdevicedestruction'

        if app_config.test_full_screen:
            app_name += ' testfullscreen'

        logging.info("\tAppConfig: {0}".format(app_name))

    try:
        process = subprocess.Popen(app_name)
    except Exception as e:
        logging.error("\tsubprocess.Popen('{0}') API call failed(Test Issue)".format(app_name))
        logging.error("\t{0}".format(e))
        return False

    # Breather after opening the app
    time.sleep(5)

    # make sure app is the top most active window
    if not full_screen:
        title = None
        if app_name == Apps.AngryBotsGame:
            title = AppWindowTitles.AngryBotsGameConfiguration
        if app_name == Apps.MovingRectangleApp:
            title = AppWindowTitles.MovingRectangleApp
        if app_name == Apps.Classic3DCubeApp:
            title = AppWindowTitles.Classic3DCubeApp
        try:
            __get_window_handle(title)
            if __handle is None:
                logging.warning("\tUnable to find the window handle for {0}".format(app_name))
            else:
                win32gui.SetForegroundWindow(__handle)
        except Exception as e:
            logging.warning(e)

    if app_name == Apps.AngryBotsGame:
        __vrr_app_state = {
            'app': app_name, 'process': process, 'full_screen': full_screen
        }

        # AngryBots app stores its state every time. To open the app with right settings we are storing the app state.
        angry_bots_previous_state = __get_app_state()
        if angry_bots_previous_state is not None:
            # There exists a previously stored state
            if angry_bots_previous_state['full_screen'] == full_screen:
                # No need to change the full screen setting if it is same
                full_screen = False
                __vrr_app_state['full_screen'] = angry_bots_previous_state['full_screen']
            else:
                # Toggle full screen setting otherwise
                __vrr_app_state['full_screen'] = not angry_bots_previous_state['full_screen']
                full_screen = True

        # Store current settings
        __store_app_state({'full_screen': __vrr_app_state['full_screen']})

        # In AngryBots settings, max resolution is at bottom of the list. Press down keys to select max resolution
        for _ in range(50):
            kb.press('DOWN')

        # AngryBots game opens in windowed mode by default
        # Change if required
        time.sleep(0.5)
        kb.press('TAB')
        if full_screen:
            time.sleep(0.5)
            kb.press(' ')

        # Set Graphics settings
        time.sleep(0.5)
        kb.press('TAB')
        for _ in range(graphics_setting - 1):
            kb.press('DOWN')

        # Play
        time.sleep(0.5)
        kb.press('TAB')
        time.sleep(0.5)
        kb.press('ENTER')

        # Wait for SplashScreen Animation to finish
        time.sleep(10)

        if not full_screen:
            title = AppWindowTitles.AngryBotsGame
            try:
                __get_window_handle(title)
                if __handle is None:
                    logging.warning("\tUnable to find the window handle for {0}".format(app_name))
                else:
                    win32gui.SetForegroundWindow(__handle)
            except Exception as e:
                logging.warning(e)

    else:
        logging.debug("\tFPS Factor: 0")
        logging.debug("\tSpeed Factor: 1")
        logging.debug("\tVSync Status: DISABLED")
        __vrr_app_state = {
            'app': app_name, 'process': process, 'fps': 0, 'speed': 1, 'vsync': False,
            'full_screen': False, 'state': True
        }

        if full_screen:
            app_action(app_name, AppActions.ENABLE_FULL_SCREEN)
            logging.debug("\tFullScreen Status: ENABLED")
            time.sleep(1)
        else:
            logging.debug("\tFullScreen Status: DISABLED")

    os.chdir(test_context.ROOT_FOLDER)

    return True


##
# @brief        Exposed API to close the app
# @return       True
def __close_app():
    global __vrr_app_state
    subprocess.call('taskkill /F /T /PID ' + str(__vrr_app_state['process'].pid))
    window_helper.restore_all_windows()
    return True


##
# @brief
# @param[in]    app
# @param[in]    action
# @return       True if operation is successful, False otherwise
def app_action(app, action):
    global __vrr_app_state

    # Validate arguments
    if not (0 <= action < AppActions.APP_ACTION_MAX):
        logging.error("\tInvalid arguments: action= {0}".format(action.name))
        return False

    # Validate VRR App state
    if bool(__vrr_app_state) is False:
        logging.error("\tNo running app found. App State= {0}".format(__vrr_app_state))
        return False

    if app == Apps.AngryBotsGame:
        if action == AngryBotsActions.MOVE_DOWN:
            for _ in range(40):
                kb.press('DOWN')
        if action == AngryBotsActions.MOVE_UP:
            for _ in range(40):
                kb.press('UP')
        if action == AngryBotsActions.MOVE_LEFT:
            for _ in range(40):
                kb.press('LEFT')
        if action == AngryBotsActions.MOVE_RIGHT:
            for _ in range(40):
                kb.press('RIGHT')
        return True

    if action == AppActions.OPEN:
        pass
    if action == AppActions.CLOSE:
        pass
    if action == AppActions.ENABLE_FULL_SCREEN:
        if __vrr_app_state['full_screen'] is False:
            if __vrr_app_state['app'] == Apps.MovingRectangleApp:
                kb.press(' ')
            if __vrr_app_state['app'] == Apps.Classic3DCubeApp:
                kb.press('F5')
            __vrr_app_state['full_screen'] = True
            time.sleep(2)

    if action == AppActions.DISABLE_FULL_SCREEN:
        if __vrr_app_state['full_screen'] is True:
            if __vrr_app_state['app'] == Apps.MovingRectangleApp:
                kb.press(' ')
            if __vrr_app_state['app'] == Apps.Classic3DCubeApp:
                kb.press('ECS')
            __vrr_app_state['full_screen'] = False

    if action == AppActions.FORCE_FULL_SCREEN:
        if __vrr_app_state['app'] == Apps.MovingRectangleApp:
            kb.press(' ')
        if __vrr_app_state['app'] == Apps.Classic3DCubeApp:
            kb.press('F5')
        __vrr_app_state['full_screen'] = True
        time.sleep(2)

    if action == AppActions.INCREASE_SPEED:
        if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
            kb.press('RIGHT')
        __vrr_app_state['speed'] += 1
    if action == AppActions.DECREASE_SPEED:
        if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
            kb.press('LEFT')
        __vrr_app_state['speed'] -= 1
    if action == AppActions.INCREASE_FPS:
        if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
            kb.press('UP')
        __vrr_app_state['fps'] += 0.5
    if action == AppActions.DECREASE_FPS:
        if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
            kb.press('DOWN')
        __vrr_app_state['fps'] -= 0.5
    if action == AppActions.ENABLE_VSYNC:
        if __vrr_app_state['vsync'] is False:
            if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
                kb.press('V')
            __vrr_app_state['vsync'] = True
    if action == AppActions.DISABLE_VSYNC:
        if __vrr_app_state['vsync'] is True:
            if __vrr_app_state['app'] in [Apps.MovingRectangleApp]:
                kb.press('V')
            __vrr_app_state['vsync'] = False
    time.sleep(0.5)
    return True


##
# @brief        Helper API to increase FPS in currently running VRR app
# @param[in]    app
# @return
def increase_fps(app):
    global __vrr_app_state
    change_in_fps_factor = 30

    if __vrr_app_state['app'] not in [Apps.MovingRectangleApp]:
        return None

    for _ in range(change_in_fps_factor):
        app_action(app, AppActions.INCREASE_FPS)
    return change_in_fps_factor


##
# @brief        Helper API to decrease FPS in currently running VRR app
# @param[in]    app String, targeted app
# @return       change_in_fps_factor, double, if successful, None otherwise
def decrease_fps(app):
    global __vrr_app_state
    change_in_fps_factor = 30

    if __vrr_app_state['app'] not in [Apps.MovingRectangleApp]:
        return None

    for _ in range(change_in_fps_factor):
        app_action(app, AppActions.DECREASE_FPS)
    return change_in_fps_factor


##
# @brief        Helper API to get app state
# @return       app_state, dict, if successful, None otherwise
def __get_app_state():
    if not os.path.exists(GAME_STATE):
        return None

    with open(GAME_STATE, "rb") as f:
        return pickle.load(f)


##
# @brief        Helper API to store app state
# @param[in]    app_sate, dict
# @return       None
def __store_app_state(app_state):
    with open(GAME_STATE, "wb") as f:
        pickle.dump(app_state, f)


##
# @brief        Helper API to store app state
# @param[in]    hwnd
# @param[in]    title
# @return       None
def __window_enum_callback(hwnd, title):
    global __handle

    # Skip if handle has been already assigned
    if __handle is not None:
        return

    if title.lower() in str(win32gui.GetWindowText(hwnd)).lower():
        __handle = hwnd


##
# @brief        Helper function to get the window handle given the window title
# @param[in]    window_title string
# @return       handle number, Requested window handle if successful, None otherwise
def __get_window_handle(window_title):
    global __handle
    if window_title is None:
        __handle = None
        return
    __handle = None

    # Enumerate all the windows, and search for the given title
    win32gui.EnumWindows(__window_enum_callback, window_title)


##
# @brief        Helper function for game playback
# @param[in]    workload_args string containing the info required for game play back
# @return       True if game playback was successful, False otherwise
def __game_playback(workload_args):
    app = workload_args[0]
    duration = workload_args[1]
    full_screen = workload_args[2]
    power_event_during_playback = None if len(workload_args) < 4 else workload_args[3]
    power_source_event_during_playback = None if len(workload_args) < 5 else workload_args[4]
    app_config = None if len(workload_args) < 6 else workload_args[5]

    html.step_start("Running Workload GAME_PLAYBACK ({0}) for {1} seconds".format(app, duration))

    # Close any pop up notification before opening the app
    # Pressing WIN+A twice will open and close the notification center, which will close all notification toasts
    kb.press('WIN+A')
    time.sleep(1)
    kb.press('WIN+A')
    time.sleep(1)

    # Open given VRR testing app for each panel
    if __open_app(app, full_screen, AngryBotsGraphicsSettings.FASTEST, app_config) is False:
        logging.error("\tFailed to open {0} app(Test Issue)".format(app))
        return False
    logging.info("\tLaunched {0} app successfully".format(app))

    # Handle sleep/hibernate or power source switching during workload
    if __handle_event_during_workload(power_event_during_playback, power_source_event_during_playback, 5) is not True:
        return None

    # No actions are available for Classic3DCube app to increase or decrease FPS
    # Let the app run for 30 seconds and return
    if app == Apps.Classic3DCubeApp:
        logging.debug("\tRotate 3D cube for 30 seconds")
        time.sleep(duration)
    elif app == Apps.AngryBotsGame:
        # Repeat randomly chosen movement for 2 seconds.
        if duration < 15:
            duration = 15
        for _ in range(int(duration / 2)):
            action = AngryBotsActions(random.randint(0, AngryBotsActions.ACTION_MAX))
            logging.debug("\t{0} for 2 seconds".format(action.name))
            app_action(app, action)
    else:
        if duration < 60:
            duration = 60

        # Set the speed factor to 15 to make the tearing clear
        for _ in range(14):
            app_action(app, AppActions.INCREASE_SPEED)

        # Decrease and increase FPS two times to check basic VRR functionality
        # Pattern :
        #   Decrease FPS by 30 intervals (15 seconds) -> run app with constant FPS (15 seconds)
        #   -> Increase FPS by 30 intervals (15 seconds) -> run app with constant FPS (15 seconds)
        # One iteration takes around 60 seconds
        for _ in range(int(duration / 60)):
            change_in_fps_factor = decrease_fps(app)
            if change_in_fps_factor is not None:
                logging.debug("\tFPS Factor decreased by {0} steps".format(change_in_fps_factor))
            else:
                logging.warning("\tDecreasing FPS is not available in the App {0}".format(app))

            # Wait for some time to verify low FPS
            time.sleep(15)

            # Increase FPS
            change_in_fps_factor = increase_fps(app)
            if change_in_fps_factor is not None:
                logging.debug("\tFPS Factor increased by {0} steps".format(change_in_fps_factor))
            else:
                logging.debug("\tIncreasing FPS is not available in the App {0}".format(app))

            # Wait for some time to verify high FPS
            time.sleep(15)

    if __close_app() is False:
        logging.error("\tFailed to close {0} app(Test Issue)".format(app))
        return None

    logging.info("\tClosed the app successfully")
    html.step_end()
    return True
