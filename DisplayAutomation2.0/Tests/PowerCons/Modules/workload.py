#######################################################################################################################
# @file         workload.py
# @brief        Contains APIs to run workloads (idle desktop, video, game etc...)
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import os
import pickle
import random
import subprocess
import threading
import time
import win32api
import win32con
import win32gui
from typing import List
from Libs.Core import registry_access
from Libs.Core import window_helper, app_controls, display_power
from Libs.Core import winkb_helper as kb
from Libs.Core.display_config import display_config
from Libs.Core.display_essential import generate_tdr, detect_system_tdr, clear_tdr
from Libs.Core.logger import etl_tracer, html
from Libs.Core.test_env import test_context
from Libs.Feature import app
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr_util
from Tests.PowerCons.GfxAssistant.workload import __handle_event_during_workload
from Tests.PowerCons.Modules import common, polling, optical_sensor, dut, dut_context
from enum import IntEnum, Enum
from multiprocessing import Queue
from win32gui import GetWindowPlacement

IDLE_DESKTOP = 1
SCREEN_UPDATE = 2
VIDEO_PLAYBACK = 3
VIDEO_PLAYBACK_WITH_MOUSE_MOVE = 4
GAME_PLAYBACK = 6
VIDEO_PLAYBACK_USING_FILE = 7
GAME_PLAYBACK_WITH_OPTICAL_SENSOR = 8
BOOSTED_APP = 9
VIDEO_PLAYBACK_USING_FILE_WITH_MOUSE_MOVE = 10
VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS = 11
GAME_PLAYBACK_WITH_CUSTOM_EVENTS = 12

DEFAULT_GAME_PLAYBACK_DURATION = 30  # in seconds

__GAME_STATE = os.path.join(test_context.ROOT_FOLDER, "game_state.pickle")
__VRR_BIN_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
__ANGRY_BOTS_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "AngryBots")
__vrr_app_state = dict()
__monitor_id_mapping = None
__handle = None
__display_power = display_power.DisplayPower()

FLIP_AT_GAME_ARGUMENT_MAPPING = {
    "DESTINY_2": 1,
    "FORTNITE": 2,
    "CIVILIZATION_VI": 3,
    "FALLEN_ORDER": 4,
    "JURASSIC_WORLD": 5,
    "NO_MAN_SKY": 6
}


##
# @brief        Exposed object class for all VRR apps
class Apps:
    MovingRectangleApp = "MovingRectangleApp.exe"
    AngryBotsGame = "AngryBotsGame.exe"
    Classic3DCubeApp = "Classic3DCubeApp.exe"
    FlipAt = "FlipAt\\FlipAt.exe"


##
# @brief        Exposed enum class for common App actions
class AppActions(IntEnum):
    OPEN = 0
    CLOSE = 1
    ENABLE_FULL_SCREEN = 2
    DISABLE_FULL_SCREEN = 3
    FORCE_FULL_SCREEN = 4
    INCREASE_SPEED = 5
    DECREASE_SPEED = 6
    INCREASE_FPS = 7
    DECREASE_FPS = 8
    ENABLE_VSYNC = 9
    DISABLE_VSYNC = 10
    APP_ACTION_MAX = 11


##
# @brief        Exposed enum class for AngryBots graphics settings
class AngryBotsGraphicsSettings(IntEnum):
    FASTEST = 0
    FAST = 1
    SIMPLE = 2
    GOOD = 3
    BEAUTIFUL = 4
    FANTASTIC = 5


##
# @brief        Exposed enum class for AngryBots actions
class AngryBotsActions(IntEnum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    ACTION_MAX = 4


##
# @brief        Exposed enum class for Presentation model
class PresentationModel(IntEnum):
    DXGI_SWAP_EFFECT_DISCARD = 0
    DXGI_SWAP_EFFECT_SEQUENTIAL = 1
    DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL = 3


##
# @brief        Helper object class for all VRR app window titles. These titles are used to search for the app window
#               and make it active.
class __AppWindowTitles:
    MovingRectangleApp = "D3D12 Fullscreen sample"
    AngryBotsGameConfiguration = "AngryBots Configuration"
    AngryBotsGame = "AngryBots"
    Classic3DCubeApp = "ClassicD3D: Window"


##
# @brief        Helper object class for Classic 3DCube App
class Classic3DCubeAppConfig:
    adapter = 0
    gdi_compatible = False  # Render a string GDI text that blends with D3D content
    gpu_priority = 0  # Set a scheduling priority for the application D3D device
    interval = 0  # Sets present interval
    buffers = 2  # Sets number of buffers in the swap chain
    dcomp = False  # Use DComp (Direct Composition Technology) composition and effects
    rotation_speed = 1
    object_y_position = None
    window_count = 1
    test_display_mode_change = False
    test_window_device_destruction = False
    test_full_screen = False


##
# @brief        Helper object class for FlipAtApp App
class FlipAtAppConfig:
    pattern_1 = [6, 3, 18, 1, 100]
    pattern_2 = [6, 3, 18, 1, 100]
    primary_color = [85, 78, 15]
    secondary_color = [80, 73, 15]
    game_args = [0, 1]
    game_index = None
    v_sync = False


##
# @brief        Exposed enum class for PowerSource
class PowerSource(IntEnum):
    DC_MODE = 0
    AC_MODE = 1


##
# @brief    Exposed enum class for AppType
class AppType(IntEnum):
    BROWSER = 0
    WORDPAD = 1


def __handle_event_during_workload(power_event, power_source, delay=None):
    if delay is not None:
        time.sleep(delay)

    if power_event is not None:
        if __display_power.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            return None

    if power_source is not None:
        if not __display_power.set_current_powerline_status(power_source):
            return None
    return True


def __verify_watermark(gfx_index, delay, wm_status_q):
    time.sleep(delay)  # Adding delay so that the thread executing the workload starts
    wm_status_q.put(drrs.verify_watermark_drrs(gfx_index))


def __idle_desktop(workload_args, polling_args):
    polling_timeline = None
    polling_time_stamps = None
    duration = workload_args[0]

    # Causes flip at end of IDLE workload: useful for enable/disable duration calculation
    end_screen_update = False if len(workload_args) < 2 else workload_args[1]
    # gfx_index is passed as a parameter for watermark verification
    gfx_index_for_wm = None if len(workload_args) < 3 else workload_args[2]
    with_mpo = False if len(workload_args) < 4 else workload_args[3]
    power_source_event = None if len(workload_args) < 5 else workload_args[4]

    wm_status_q = None
    watermark_thread = None

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeIdleDesktop.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    kb.press('WIN+M')

    if with_mpo:
        kb.press('WIN+P')
        time.sleep(1)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        if gfx_index_for_wm:
            return None, None, None
        return None, None

    html.step_start(f"Running Workload IDLE_DESKTOP for {duration} seconds")

    if polling_args is not None:
        offsets = polling_args[0]
        polling_delay = polling_args[1]
        logging.info(f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
        polling.start(offsets, polling_delay)

    if power_source_event is not None:
        if change_power_source(power_source_event) is False:
            return False

    # Watermark verification during IDLE workload
    if gfx_index_for_wm:
        wm_status_q = Queue()
        # Create thread for watermark verification and execute watermark verification during the IDLE workload
        watermark_thread = threading.Thread(target=__verify_watermark, name='verify_watermark', args=(gfx_index_for_wm,
                                                                                                      15, wm_status_q))
        logging.info("Started Watermark verification during IDLE workload.")
        watermark_thread.start()

    logging.info(f"\tKeeping desktop idle for {duration - 10} seconds")
    time.sleep(duration - 10)

    if gfx_index_for_wm:
        watermark_thread.join()  # ensure the watermark thread ends

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling is stopped")

    logging.info("\tSuccessfully Stopped the workload")
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("FAILED to stop ETL Tracer")
        if gfx_index_for_wm:
            return None, None, None
        return None, None

    if with_mpo:
        kb.press('ESC')

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringIdleDesktop-' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("FAILED to start ETL Tracer")
        if gfx_index_for_wm:
            return None, None, None
        return None, None

    kb.press('ALT+TAB')
    if gfx_index_for_wm:
        if wm_status_q.get():
            return etl_file_path, (polling_timeline, polling_time_stamps), True
        return etl_file_path, (polling_timeline, polling_time_stamps), False
    return etl_file_path, (polling_timeline, polling_time_stamps)


def __screen_update(workload_args, polling_args):
    polling_timeline = None
    polling_time_stamps = None
    monitor_ids = workload_args[0]

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeScreenUpdate.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    kb.press('WIN+M')

    if etl_tracer.start_etl_tracer() is False:
        logging.error("FAILED to start ETL Tracer")
        return None, None

    html.step_start("Running Workload SCREEN_UPDATE")

    if polling_args is not None:
        offsets = polling_args[0]
        polling_delay = polling_args[1]
        logging.info(f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
        polling.start(offsets, polling_delay)

    logging.info("\tPSR utility is started")
    utility_timeline, utility_time_stamps = psr_util.run(monitor_ids)
    logging.info("\tPSR utility is closed")

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling is stopped")

    if etl_tracer.stop_etl_tracer() is False:
        logging.error("FAILED to stop ETL Tracer")
        return None, None

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringScreenUpdate-' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        # Delay before renaming the ETL file to avoid events getting missed
        time.sleep(2)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("FAILED to start ETL Tracer")
        return None, None

    kb.press('ALT+TAB')
    return etl_file_path, (polling_timeline, polling_time_stamps, utility_timeline, utility_time_stamps)


def __boosted_app(workload_args, polling_args):
    polling_timeline = None
    polling_time_stamps = None
    duration = workload_args[0]
    assert len(workload_args) > 1, "Panel not passed"
    panel = workload_args[1]
    power_event_during_bfr = None if len(workload_args) < 3 else workload_args[2]
    power_source_event_during_bfr = None if len(workload_args) < 4 else workload_args[3]
    maximized = True if len(workload_args) < 5 else workload_args[4]
    # @todo handling for negative scenarios
    # negative = True if len(workload_args) < 6 else workload_args[5]

    if not etl_tracer.stop_etl_tracer():
        logging.error("Failed to stop ETL capture")
        return None

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeBoost.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    kb.press('WIN+M')

    bapp = app.SnipSketch()

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return None
    logging.info("Stated ETL Capture")
    time.sleep(5)

    html.step_start(f"Running Workload BOOSTED_APP for {duration} seconds on {panel.port}")

    if bapp.open_app(maximize=maximized) is False:
        logging.error("Failed to open the Boosted APp")
        return None
    # @todo drag for extended scenarios
    # bapp.drag(panel.port, panel.gfx_index)
    # if maximized:
    #     bapp.maximise()
    time.sleep(5)
    bapp.draw_random(duration)

    if polling_args is not None:
        # time.sleep(10)  # Adding a 10 seconds delay before starting the polling to wait for RR switching
        offsets = polling_args[0]
        polling_delay = polling_args[1]
        logging.info("\tPolling started. Delay= {0}s, Offsets= {1}".format(polling_delay, list(map(hex, offsets))))
        polling.start(offsets, polling_delay)

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling stopped")

    # Handle sleep/hibernate or power source switching during workload
    if power_event_during_bfr is not None or power_source_event_during_bfr is not None:
        html.step_end()
    if __handle_event_during_workload(power_event_during_bfr, power_source_event_during_bfr) is not True:
        return None
    if power_event_during_bfr is not None:
        html.step_start("Continuing Workload Boosted App after power event")
    if power_source_event_during_bfr is not None:
        html.step_start("Continuing Workload Boosted App after power source switch")
    if power_source_event_during_bfr is not None or power_event_during_bfr is not None:
        # drawing for the specified duration after switching to the power event/power source specified
        bapp.draw_random(duration)

    bapp.close_app()
    logging.info("Waiting for 10 seconds so that refresh rate is switched back to normal state")

    time.sleep(10)

    if etl_tracer.stop_etl_tracer() is False:
        logging.error("Failed to stop ETL Tracer")
        return None
    logging.info("ETL capture stopped successfully")

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringBoostedApp-' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    return etl_file_path, (polling_timeline, polling_time_stamps)


def __video_playback(workload_args, polling_args, mouse_args=None, use_default_video_file=True, idle_after_wl=False):
    polling_timeline = None
    polling_time_stamps = None
    media_file = workload_args[0]
    duration = workload_args[1]
    pause = False if len(workload_args) < 3 else workload_args[2]
    trace_video_playback_only = False if len(workload_args) < 4 else workload_args[3]
    power_event_during_playback = None if len(workload_args) < 5 else workload_args[4]
    power_source_event_during_playback = None if len(workload_args) < 6 else workload_args[5]
    video_fullscreen = True if len(workload_args) < 7 else workload_args[6]
    loop_video = False if len(workload_args) < 8 else workload_args[7]

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeVideo.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    kb.press('WIN+M')

    if trace_video_playback_only is False:
        if etl_tracer.start_etl_tracer() is False:
            logging.error("FAILED to start ETL Tracer")
            return None
        logging.info("\tSuccessfully started ETL Tracer")

    html.step_start(f"Running Workload VIDEO_PLAYBACK for {duration} seconds")
    if use_default_video_file:
        logging.info(f"\tVideo Playback is started : {media_file:.3f}.mp4")
        app_controls.launch_video(
            os.path.join(common.TEST_VIDEOS_PATH, f"{media_file:.3f}.mp4"), is_full_screen=video_fullscreen)
    else:
        logging.info(f"\tVideo Playback is started : {media_file}")
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, media_file), is_full_screen=video_fullscreen)

    # Handle playback of video
    if loop_video is True:
        kb.press('CTRL+T')  # play in loop
        logging.info("\tPlaying the video in loop")

    if trace_video_playback_only:
        if etl_tracer.start_etl_tracer() is False:
            logging.error("FAILED to start ETL Tracer")
            return None
    logging.info("\tSuccessfully started ETL Tracer")

    if polling_args is not None:
        time.sleep(10)  # Adding a 10 seconds delay before starting the polling to wait for RR switching
        offsets = polling_args[0]
        polling_delay = polling_args[1]
        logging.info(f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
        polling.start(offsets, polling_delay)

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
    if power_event_during_playback is not None or power_source_event_during_playback is not None:
        html.step_end()
    if __handle_event_during_workload(power_event_during_playback, power_source_event_during_playback) is not True:
        return None
    if power_event_during_playback is not None:
        html.step_start("Continuing Workload VIDEO_PLAYBACK after power event")
    if power_source_event_during_playback is not None:
        html.step_start("Continuing Workload VIDEO_PLAYBACK after power source switch")

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

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling is stopped")

    if trace_video_playback_only:
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("FAILED to stop ETL Tracer")
            return None
        logging.info("Successfully stopped ETL Tracer")

    window_helper.close_media_player()
    logging.info("\tClosing video playback")

    if idle_after_wl:
        kb.press('WIN+M')
        logging.info("Keeping system idle for 10 seconds for idle after workload scenario")
        time.sleep(10)
        kb.press('ALT+TAB')

    if trace_video_playback_only is False:
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("FAILED to stop ETL Tracer")
            return None
        logging.info("Successfully stopped ETL Tracer")

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringVideoPlayback-' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        # Delay before renaming the ETL file to avoid events getting missed
        time.sleep(2)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return None
    logging.info("\tSuccessfully started ETL Tracer")

    return etl_file_path, (polling_timeline, polling_time_stamps)


def __video_playback_with_mouse_move(workload_args, polling_args, use_default_video_file=True):
    # 5 seconds, 1 mouse event, 15 seconds
    mouse_args = [5, 1, 15]
    if len(workload_args) > 2:
        mouse_args[0] = workload_args[2]
    if len(workload_args) > 3:
        mouse_args[1] = workload_args[3]
    if len(workload_args) > 4:
        mouse_args[2] = workload_args[4]
    workload_args = workload_args[:2]
    return __video_playback(workload_args, polling_args, mouse_args)


def __video_playback_with_custom_events(workload_args, polling_args):
    polling_timeline = None
    polling_time_stamps = None
    launch_new_video = True if len(workload_args) < 1 else workload_args[0]
    exit_with_closed_video = True if len(workload_args) < 2 else workload_args[1]
    media_file = workload_args[2]
    duration = 30 if len(workload_args) < 4 else workload_args[3]
    loop_video = False if len(workload_args) < 5 else workload_args[4]
    pause_video_before_exit = True if len(workload_args) < 6 else workload_args[5]
    unpause_video_before_entry = True if len(workload_args) < 7 else workload_args[6]

    html.step_start(f"Running {media_file} VIDEO_PLAYBACK for {duration} seconds")
    if launch_new_video:
        logging.info("\tMinimizing to Desktop screen")
        kb.press('WIN+M')

        status, _ = etl_tracer_stop_existing_and_start_new('GfxTraceBeforeVideoPlayback')
        if status is False:
            html.step_end()
            return None, None

        # launch new video
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, f"{media_file:.3f}.mp4"), is_full_screen=True)

        if polling_args is not None:
            time.sleep(10)  # Adding a 10 seconds delay before starting the polling to wait for RR switching
            offsets = polling_args[0]
            polling_delay = polling_args[1]
            logging.info(
                f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
            polling.start(offsets, polling_delay)

        # Breather
        time.sleep(5)
        # Handle playback of video
        if loop_video is True:
            logging.info("\tPlaying the video in loop")
            kb.press('CTRL+T')  # play in loop

        # Due to Win Qual sighting - DMRRS won't hit for ~20seconds
        time.sleep(int(duration / 2) + 20)
    else:
        is_video_playing = False
        for process in window_helper.PROCESS_VIDEO_PLAYER:
            logging.debug(f"\tChecking {process} is running")
            if window_helper.is_process_running(process) is True:
                is_video_playing = True
                break

        if is_video_playing is False:
            logging.error("NO video player is running")
            html.step_end()
            return None, None

        if unpause_video_before_entry:
            logging.info("\tVideo is Un-paused")
            kb.press(' ')  # Play the video

        status, _ = etl_tracer_stop_existing_and_start_new('GfxTraceBeforeVideoPlayback')
        if status is False:
            html.step_end()
            return None, None

        if polling_args is not None:
            time.sleep(10)  # Adding a 10 seconds delay before starting the polling to wait for RR switching
            offsets = polling_args[0]
            polling_delay = polling_args[1]
            logging.info(
                f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
            polling.start(offsets, polling_delay)

        # wait for 5 secs, as the scroll bar disappears after 5 seconds
        time.sleep(5)

        if loop_video is True:
            logging.info("\tPlaying the video in loop")
            kb.press('CTRL+T')  # play in loop

        # Due to Win Qual sighting - DMRRS won't hit for ~20seconds
        time.sleep(int(duration / 2) + 20)

    if exit_with_closed_video:
        logging.info("\tClosing video playback")
        window_helper.close_media_player()

    status, etl_file_path = etl_tracer_stop_existing_and_start_new('GfxTraceDuringVideoPlayback')
    if status is False:
        html.step_end()
        return None, None

    # Pause the video
    if pause_video_before_exit:
        logging.info("\tVideo is Paused")
        kb.press(' ')

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling is stopped")

    html.step_end()
    return etl_file_path, (polling_timeline, polling_time_stamps)


##
# @brief        Exposed API to open any VRR app
# @param[in]    app_name - app to be opened
# @param[in]    full_screen - True if app is expected to be launched in full screen mode, False otherwise
# @param[in]    graphics_setting - graphics setting for AngryBots
# @param[in]    app_config - (Classic3DCubeAppConfig) app configuration for workload tests
# @return       True if operation is successful, False otherwise
def open_gaming_app(app_name, full_screen, graphics_setting=None, app_config=None):
    global __vrr_app_state
    global __monitor_id_mapping
    global __handle

    if not full_screen:
        window_helper.minimize_all_windows()
        time.sleep(1)

    os.chdir(__VRR_BIN_FOLDER)
    if app_name == Apps.AngryBotsGame:
        os.chdir(__ANGRY_BOTS_FOLDER)

    # Workload test configuration
    if app_name == Apps.Classic3DCubeApp and app_config is not None:
        app_name += ' adapter:{0}'.format(app_config.adapter)
        app_name += ' gpupriority:{0}'.format(app_config.gpu_priority)
        app_name += ' interval:{0}'.format(app_config.interval)
        app_name += ' buffers:{0}'.format(app_config.buffers)
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

    if app_name == Apps.FlipAt:
        if app_config is not None:
            if app_config.pattern_1 is not None:
                app_name += ' ' + ' '.join(map(str, app_config.pattern_1))

            if app_config.pattern_2 is not None:
                app_name += ' ' + ' '.join(map(str, app_config.pattern_2))

            if app_config.primary_color is not None:
                app_name += ' ' + ' '.join(map(str, app_config.primary_color))

            if app_config.secondary_color is not None:
                app_name += ' ' + ' '.join(map(str, app_config.secondary_color))

            if app_config.game_index is not None:
                app_name += ' ' + ' '.join(map(str, app_config.game_args))
                app_name += ' ' + str(app_config.game_index)
        else:
            app_config = FlipAtAppConfig()
            app_config.game_index = 2

    try:
        logging.info(app_name)
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
            title = __AppWindowTitles.AngryBotsGameConfiguration
        if (app_name == Apps.MovingRectangleApp) or ("FlipAt" in app_name):
            title = __AppWindowTitles.MovingRectangleApp
        if app_name == Apps.Classic3DCubeApp:
            title = __AppWindowTitles.Classic3DCubeApp
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
            title = __AppWindowTitles.AngryBotsGame
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

        if "FlipAt" in app_name:
            logging.info("key press 'f' for changing color in application")
            kb.press('f')
            if app_config.v_sync is True:
                app_action(app_name, AppActions.ENABLE_VSYNC)
                logging.debug("\tVSync Status: ENABLED")
                time.sleep(1)
            else:
                logging.debug("\tVSync Status: DISABLED")

    os.chdir(test_context.ROOT_FOLDER)

    return True


##
# @brief        Exposed API to close the app
# @return       True if operation is successful, False otherwise
def close_gaming_app():
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
            if (__vrr_app_state['app'] == Apps.MovingRectangleApp) or ("FlipAt" in __vrr_app_state['app']):
                kb.press(' ')
            if __vrr_app_state['app'] == Apps.Classic3DCubeApp:
                kb.press('F5')
            __vrr_app_state['full_screen'] = True
            time.sleep(2)

    if action == AppActions.DISABLE_FULL_SCREEN:
        if __vrr_app_state['full_screen'] is True:
            if (__vrr_app_state['app'] == Apps.MovingRectangleApp) or ("FlipAt" in __vrr_app_state['app']):
                kb.press(' ')
            if __vrr_app_state['app'] == Apps.Classic3DCubeApp:
                kb.press('ESC')
            __vrr_app_state['full_screen'] = False

    if action == AppActions.FORCE_FULL_SCREEN:
        if (__vrr_app_state['app'] == Apps.MovingRectangleApp) or ("FlipAt" in __vrr_app_state['app']):
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
            if (__vrr_app_state['app'] == Apps.MovingRectangleApp) or ("FlipAt" in __vrr_app_state['app']):
                kb.press('V')
            __vrr_app_state['vsync'] = True
    if action == AppActions.DISABLE_VSYNC:
        if __vrr_app_state['vsync'] is True:
            if (__vrr_app_state['app'] == Apps.MovingRectangleApp) or ("FlipAt" in __vrr_app_state['app']):
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
    if not os.path.exists(__GAME_STATE):
        return None

    with open(__GAME_STATE, "rb") as f:
        return pickle.load(f)


##
# @brief        Helper API to store app state
# @param[in]    app_sate, dict
def __store_app_state(app_state):
    with open(__GAME_STATE, "wb") as f:
        pickle.dump(app_state, f)


def __window_enum_callback(hwnd, title):
    global __handle

    # Skip if handle has been already assigned
    if __handle is not None:
        return

    if title.lower() in str(win32gui.GetWindowText(hwnd)).lower():
        __handle = hwnd


##
# @brief        Helper function to get the window handle given the window title
# @param[in]    window_title, string
# @return       handle, number, Requested window handle if successful, None otherwise
def __get_window_handle(window_title):
    global __handle
    if window_title is None:
        __handle = None
        return
    __handle = None

    # Enumerate all the windows, and search for the given title
    win32gui.EnumWindows(__window_enum_callback, window_title)


def __game_playback(workload_args, polling_args, optical_sensor_args, idle_after_wl=False):
    polling_timeline = None
    polling_time_stamps = None
    optical_sensor_samples = None

    app = workload_args[0]
    duration = workload_args[1]
    full_screen = workload_args[2]
    power_event_during_playback = None if len(workload_args) < 4 else workload_args[3]
    power_source_event_during_playback = None if len(workload_args) < 5 else workload_args[4]
    app_config = None if len(workload_args) < 6 else workload_args[5]

    html.step_start("Running Workload GAME_PLAYBACK ({0}) for {1} seconds".format(app, duration))

    if app == Apps.AngryBotsGame:
        path = os.path.join(__ANGRY_BOTS_FOLDER, Apps.AngryBotsGame)
    elif app == Apps.MovingRectangleApp:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.MovingRectangleApp)
    elif app == Apps.Classic3DCubeApp:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.Classic3DCubeApp)
    else:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.FlipAt)

    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=r"Software\Microsoft")
    if registry_access.write(args=reg_args, reg_name=path, reg_type=registry_access.RegDataType.SZ,
                             reg_value="GpuPreference=0;VRREligibleOverride=1",
                             sub_key=r"DirectX\UserGpuPreferences") is False:
        logging.error(f"\tFailed to update value ='GpuPreference=0;VRREligibleOverride=1' for {path=}")

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeGamePlayback.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return None, None

    # Close any pop up notification before opening the app
    # Pressing WIN+A twice will open and close the notification center, which will close all notification toasts
    kb.press('WIN+A')
    time.sleep(1)
    kb.press('WIN+A')
    time.sleep(1)

    # Open given VRR testing app for each panel
    if open_gaming_app(app, full_screen, AngryBotsGraphicsSettings.FASTEST, app_config) is False:
        logging.error(f"\tFailed to open {app} app(Test Issue)")
        return False
    logging.info(f"\tLaunched {app} app successfully")

    if polling_args is not None:
        offsets = polling_args[0]
        polling_delay = polling_args[1]
        logging.info(f"\tPolling of register is started. Delay= {polling_delay}s, Offsets= {list(map(hex, offsets))}")
        polling.start(offsets, polling_delay)

    if optical_sensor_args is not None:
        sensor_index = optical_sensor_args[0]
        sensor_sample_rate = optical_sensor_args[1]
        sensor_duration = duration - 1
        logging.info(f"\tSensor Utility Started. {sensor_index=} {sensor_sample_rate=} {sensor_duration=}s")
        optical_sensor.start(sensor_index, sensor_sample_rate, sensor_duration)

    # Handle sleep/hibernate or power source switching during workload
    if power_event_during_playback is not None or power_source_event_during_playback is not None:
        html.step_end()
    if __handle_event_during_workload(power_event_during_playback, power_source_event_during_playback, 5) is not True:
        return None
    if power_event_during_playback is not None:
        html.step_start("Continuing Workload GAME_PLAYBACK after power event")
    if power_source_event_during_playback is not None:
        html.step_start("Continuing Workload GAME_PLAYBACK after power source switch")

    # No actions are available for Classic3DCube app to increase or decrease FPS
    # Let the app run for 30 seconds and return
    if app in [Apps.Classic3DCubeApp, Apps.FlipAt]:
        if app == Apps.Classic3DCubeApp:
            logging.debug(f"\tRotate 3D cube for {duration} seconds")
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

    if optical_sensor_args is not None:
        time.sleep(2)
        optical_sensor_samples = optical_sensor.stop()
        file_name = 'OpticalSensorData.' + str(time.time()) + '.txt'
        sensor_data_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        with open(sensor_data_file_path, "w") as f:
            f.write("\n".join(map(str, optical_sensor_samples)))
        logging.info(f"\t\tOptical Sensor Utility stopped. Dumped the data in {file_name}.")

    if close_gaming_app() is False:
        logging.error("\tFailed to close {0} app(Test Issue)".format(app))
        return None, None

    logging.info("\tClosed the app successfully")

    if idle_after_wl:
        kb.press('WIN+M')
        logging.info("Keeping system idle for 10 seconds for idle after workload scenario")
        time.sleep(10)
        kb.press('ALT+TAB')

    if polling_args is not None:
        polling_timeline, polling_time_stamps = polling.stop()
        logging.info("\tPolling is stopped")

    if etl_tracer.stop_etl_tracer() is False:
        logging.error("Failed to stop ETL Tracer")
        return None, None

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringGamePlayback.' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return None, None

    html.step_end()
    if optical_sensor_args is not None:
        return etl_file_path, (polling_timeline, polling_time_stamps), optical_sensor_samples

    return etl_file_path, (polling_timeline, polling_time_stamps)


##
# @brief        Helper API to get workload traces and polling data
# @param[in]    workload_args list
#                       GAME_PLAYBACK_WITH_CUSTOM_EVENTS = [app, duration, full_screen, use_existing_game,
#                                   exit_without_closed_game, app_config]
#                       app, String, targeted app
#                       duration, Number, in seconds
#                       full_screen, Boolean
#                       use_existing_game, Boolean
#                       exit_without_closed_game, Boolean - AC/DC
#                       app_config[optional], object, app configuration
# @return       status, etl_file if successful, False, None otherwise
def __game_playback_with_custom_events(workload_args):
    etl_file_path = None

    app = workload_args[0]
    duration = workload_args[1]
    full_screen = workload_args[2]
    use_existing_game = False if len(workload_args) < 4 else workload_args[3]
    exit_without_closed_game = False if len(workload_args) < 5 else workload_args[4]
    app_config = None if len(workload_args) < 6 else workload_args[5]

    html.step_start("Running Workload GAME_PLAYBACK_WITH_CUSTOM_EVENTS ({0}) for {1} seconds".format(app, duration))

    if app == Apps.AngryBotsGame:
        path = os.path.join(__ANGRY_BOTS_FOLDER, Apps.AngryBotsGame)
    elif app == Apps.MovingRectangleApp:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.MovingRectangleApp)
    elif app == Apps.Classic3DCubeApp:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.Classic3DCubeApp)
    else:
        path = os.path.join(__VRR_BIN_FOLDER, Apps.FlipAt)

    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=r"Software\Microsoft")
    if registry_access.write(args=reg_args, reg_name=path, reg_type=registry_access.RegDataType.SZ,
                             reg_value="GpuPreference=0;VRREligibleOverride=1",
                             sub_key=r"DirectX\UserGpuPreferences") is False:
        logging.error(f"\tFailed to update value ='GpuPreference=0;VRREligibleOverride=1' for {path=}")

    # if request to launch new game or use existing one.
    if not use_existing_game:
        etl_tracer.stop_etl_tracer()
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            etl_file_path = os.path.join(
                test_context.LOG_FOLDER, 'GfxTraceBeforeGamePlayback.' + str(time.time()) + '.etl')
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")
            return False, None

        # Close any pop up notification before opening the app
        # Pressing WIN+A twice will open and close the notification center, which will close all notification toasts
        kb.press('WIN+A')
        time.sleep(1)
        kb.press('WIN+A')
        time.sleep(1)

        # Open given VRR testing app for each panel
        if open_gaming_app(app, full_screen, AngryBotsGraphicsSettings.FASTEST, app_config) is False:
            logging.error(f"\tFailed to open {app} app(Test Issue)")
            return False, None
        logging.info(f"\tLaunched {app} app successfully")

        # No actions are available for Classic3DCube app to increase or decrease FPS
        # Let the app run for 30 seconds and return
        if app in [Apps.Classic3DCubeApp, Apps.FlipAt]:
            if app == Apps.Classic3DCubeApp:
                logging.debug(f"\tRotate 3D cube for {duration} seconds")
            time.sleep(duration)
        elif app == Apps.AngryBotsGame:
            # Repeat randomly chosen movement for 2 seconds.
            if duration < 15:
                duration = 15
            for _ in range(int(duration / 2)):
                action = AngryBotsActions(random.randint(0, AngryBotsActions.ACTION_MAX))
                logging.debug("\t{0} for 2 seconds".format(action.name))
                app_action(app, action)
    if not exit_without_closed_game:
        if close_gaming_app() is False:
            logging.error("\tFailed to close {0} app(Test Issue)".format(app))
            return False, None

        logging.info("\tClosed the app successfully")

        if etl_tracer.stop_etl_tracer() is False:
            logging.error("Failed to stop ETL Tracer")
            return False, None

        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTraceDuringGamePlayback.' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")
            return False, None

    html.step_end()

    return True, etl_file_path


##
# @brief        Helper API to get workload traces and polling data
# @param[in]    workload IDLE_DESKTOP/SCREEN_UPDATE/...
# @param[in]    workload_args list
#                   IDLE_DESKTOP = [duration,
#                                   end_screen_update to ensure a flip at the end of the workload
#                                   gfx_index_for_wm, gfx_index of adapter for watermark verification
#                                   with_mpo, bool flag to enable small window during IDLE Desktop for MPO
#                                   power_source_event enum, PowerSource to switch the mode during IDLE Desktop]
#                   SCREEN_UPDATE = [monitor_ids
#                                    gfx_index_for_wm, gfx_index of adapter for watermark verification]
#                   VIDEO_PLAYBACK = [media_fps, duration, pause=False, trace_video_playback_only=True,
#                                       power_event_during_playback,
#                                       power_source_event_during_playback, video_fullscreen=True, loop_video=False]
#                       media_fps, Number
#                       duration, Number, in seconds
#                       pause[optional], Boolean - pause video in between for 5 seconds
#                       trace_video_playback_only[optional], Boolean - Option to control whether to include video
#                                                                      opening/closing events in traces
#                       power_event_during_playback[optional], Enum - CS/S3/S4
#                       power_source_event_during_playback[optional], Enum - AC/DC
#                       video_fullscreen[optional], Boolean - Option to control video fullscreen
#                       loop_video[optional], Boolean - Option to control video playback in loop
#                   VIDEO_PLAYBACK_WITH_MOUSE_MOVE
#                   [media_fps, duration, start_delay=5, mouse_move_count=1, move_delay=15]
#                       media_fps, Number
#                       duration, Number, in seconds
#                       start_delay, Number, in seconds, delay before first mouse move event.
#                       mouse_move_count, Number, total number of mouse move events
#                       move_delay, Number, in seconds, delay between mouse move events
#                   GAME_PLAYBACK = [app, duration, full_screen, power_event_duration_playback,
#                                   power_source_event_during_playback, app_config]
#                       app, String, targeted app
#                       duration, Number, in seconds
#                       full_screen, Boolean
#                       power_event_during_playback[optional], Enum - CS/S3/S4
#                       power_source_event_during_playback[optional], Enum - AC/DC
#                       app_config[optional], object, app configuration
#                   VIDEO_PLAYBACK_USING_FILE = [duration, video_file_name]
#                       duration, Number, in seconds
#                       video_file_name name of the video file to be played
#                   VIDEO_PLAYBACK_USING_FILE_WITH_MOUSE_MOVE
#                   [media_file, duration, start_delay=5, mouse_move_count=1, move_delay=15]
#                       media_fps, Number
#                       duration, Number, in seconds
#                       start_delay, Number, in seconds, delay before first mouse move event.
#                       mouse_move_count, Number, total number of mouse move events
#                       move_delay, Number, in seconds, delay between mouse move events
#                   VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS
#                   [launch_new_video, exit_with_closed_video, media_file, duration, loop_video]
#                   launch_new_video, Boolean, play video in existing player(already launched) or launch new player
#                   exit_with_closed_video, Boolean, exit the scenario by closing the video player
#                   media_file, name of the video file to be played
#                   duration, Number, in seconds
#                   loop_video, Boolean - Option to control video playback in loop
#                   BOOSTED_APP = [duration,panel, power_event, power_source, negative=negative]
#                       duration, Number in seconds.
#                   GAME_PLAYBACK_WITH_CUSTOM_EVENTS = [app, duration, full_screen, ,
# #                                   , app_config]
# #                       app, String, targeted app
# #                       duration, Number, in seconds
# #                       full_screen, Boolean
# #                       power_event_during_playback[optional], Enum - CS/S3/S4
# #                       power_source_event_during_playback[optional], Enum - AC/DC
# #                       app_config[optional], object, app configuration
# @param[in]    polling_args [optional] list, [poll_offset_list, polling_delay]
# @param[in]    optical_sensor_args [optional] list, [sensor_index=3, sample_rate=1000]
# @param[in]    idle_after_wl [optional], system will be in idle after workload if true
# @return       result, tuple, (etl_file, polling_data) if successful, None otherwise
def run(workload, workload_args, polling_args=None, optical_sensor_args=None, idle_after_wl=False):
    assert workload

    if workload == IDLE_DESKTOP:
        return __idle_desktop(workload_args, polling_args)
    if workload == BOOSTED_APP:
        return __boosted_app(workload_args, polling_args)
    if workload == SCREEN_UPDATE:
        return __screen_update(workload_args, polling_args)
    if workload == VIDEO_PLAYBACK:
        if idle_after_wl:
            return __video_playback(workload_args, polling_args, use_default_video_file=True, idle_after_wl=True)
        else:
            return __video_playback(workload_args, polling_args, use_default_video_file=True)
    if workload == VIDEO_PLAYBACK_USING_FILE:
        return __video_playback(workload_args, polling_args, None, use_default_video_file=False)
    if workload == VIDEO_PLAYBACK_WITH_MOUSE_MOVE:
        return __video_playback_with_mouse_move(workload_args, polling_args, use_default_video_file=True)
    if workload == VIDEO_PLAYBACK_USING_FILE_WITH_MOUSE_MOVE:
        return __video_playback_with_mouse_move(workload_args, polling_args, use_default_video_file=False)
    if workload == VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS:
        return __video_playback_with_custom_events(workload_args, polling_args)
    if workload == GAME_PLAYBACK:
        return __game_playback(workload_args, polling_args, optical_sensor_args, idle_after_wl)
    if workload == GAME_PLAYBACK_WITH_CUSTOM_EVENTS:
        return __game_playback_with_custom_events(workload_args)

    return None


########################################################################################################################
# From this partition, there would be new and recommended approach for using workload sequencing as per the requirement.
# Above workload usage needs to be moved to a newer approach. Once done, it will be deprecated
########################################################################################################################
##
# @brief        exposed method to execute list of events
# @param[in]    working_sequence List, list of actions to be done using Enums from current file only
# @return       status,  collected_etl, bool, dir
def execute(working_sequence: List):
    collected_etl = {Etl.START: [], Etl.STOP: []}

    status = True
    for steps in working_sequence:
        html.step_start(f"Executing [{steps}]", True)
        html.step_end()
        if not isinstance(steps, Etl):
            status = steps.trigger()
        else:
            status, etl_file = steps.trigger()
            if status:
                collected_etl[steps.action].append(etl_file)

        if status is False:
            break
    logging.info(f"ETLs generated from scenario= {collected_etl}")
    return status, collected_etl


##
# @brief        Exposed enum class for complete path of available Video Files
class VideoFile(Enum):
    FPS_24 = os.path.join(common.TEST_VIDEOS_PATH, '24.000.mp4')
    FPS_25 = os.path.join(common.TEST_VIDEOS_PATH, '25.000.mp4')
    FPS_30 = os.path.join(common.TEST_VIDEOS_PATH, '30.000.mp4')
    FPS_23_976 = os.path.join(common.TEST_VIDEOS_PATH, '23.976.mp4')
    FPS_29_970 = os.path.join(common.TEST_VIDEOS_PATH, '29.970.mp4')
    FPS_59_940 = os.path.join(common.TEST_VIDEOS_PATH, '59.940.mp4')
    FPS_30_BLANK = os.path.join(common.TEST_VIDEOS_PATH, '30.000_FPS_WITH_BLANK.mp4')


##
# @brief        Exposed enum class for RotateScreen
# @note         enum value is in parity with Rotation in display_config_enums.py
class RotateScreen(IntEnum):
    TO_0 = 1
    TO_90 = 2
    TO_180 = 3
    TO_270 = 4


##
# @brief    Exposed object class for App Process names
class AppProcessName:
    BROWSER = "msedge.exe"
    WORDPAD = "wordpad.exe"
    SYSTEM_SETTINGS = "SystemSettings.exe"


##
# @brief         Exposed API to change power source
# @param[in]     power_source enum, PowerSource
# @return        True if successful, False otherwise
def change_power_source(power_source: PowerSource):
    power_source_str = PowerSource(power_source).name
    status = True

    if __display_power.is_simulated_battery_enabled() is False:
        if __display_power.enable_disable_simulated_battery(True) is False:
            logging.error("Failed to enable SimulatedBattery")
            return False
    logging.info("Simulated Battery is already ENABLED")

    status &= __display_power.set_current_powerline_status(power_source)

    if status is False:
        logging.error(f"FAILED to switch power source to {power_source_str} (Test Issue)")
        return False

    logging.info(f"Successfully switched to {power_source_str}")
    return True


##
# @brief        Exposed enum class for PowerSource
class SwitchPowerSource(object):
    DC = 0
    AC = 1

    ##
    # @brief       Initializer for PowerSource instances
    # @param[in]    action attribute, action attribute from class SwitchPowerSource
    def __init__(self, action):
        self.action = action

    ##
    # @brief        Overridden str method
    # @return       string representation for PowerSource
    def __repr__(self):
        return f"PowerSource: {display_power.PowerSource(self.action).name}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       string representation for PowerSource
    def trigger(self):
        return change_power_source(PowerSource(self.action))


##
# @brief        Exposed enum class for PowerEvent
# @note         enum value is in parity with PowerEventState in display_power.py
class InvokePowerEvent(object):
    CS = 0
    S3 = 1
    S4 = 2
    S5 = 3

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class InvokePowerEvent
    # @param[in]    sleep_time optional, Sleep duration from resuming the system from power state
    def __init__(self, action, sleep_time: int = common.POWER_EVENT_DURATION_DEFAULT):
        self.action = action
        self.sleep_time = sleep_time

    ##
    # @brief        Overridden str method
    # @return       string representation for PowerEvent
    def __repr__(self):
        return f"InvokePowerEvent: {display_power.PowerEvent(self.action).name}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True if power event successful, False otherwise
    def trigger(self):
        if self.action is None:
            return False
        return display_power.DisplayPower().invoke_power_event(display_power.PowerEvent(self.action), self.sleep_time)


##
# @brief        Exposed enum class for Video
class Video(object):
    LAUNCH_IN_FULLSCREEN = "LAUNCH_IN_FULLSCREEN"
    LAUNCH_IN_WINDOWED = "LAUNCH_IN_WINDOWED"
    CLOSE = "CLOSE"
    PAUSE = "PAUSE"
    UN_PAUSE = "UN_PAUSE"
    SWITCH_TO_WINDOWED_MODE = "SWITCH_TO_WINDOWED_MODE"
    SWITCH_TO_FULLSCREEN_MODE = "SWITCH_TO_FULLSCREEN_MODE"
    ENABLE_LOOP_VIDEO = "ENABLE_LOOP_VIDEO"
    DISABLE_LOOP_VIDEO = "DISABLE_LOOP_VIDEO"

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class Video
    # @param[in]    path optional, complete path to media file
    def __init__(self, action, path: str = None):
        self.action = action
        self.path = path
        self.with_full_screen = self.action == Video.LAUNCH_IN_FULLSCREEN

    ##
    # @brief        Overridden str method
    # @return       string representation for Video
    def __repr__(self):
        return f"Video: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        if self.action in [Video.LAUNCH_IN_FULLSCREEN, Video.LAUNCH_IN_WINDOWED]:
            if self.path is None:
                logging.error("Path is not provided. Video Launch cannot be executed with path as None")
                return False
            if os.path.exists(self.path) is False:
                logging.error(f"{self.path} does NOT exist. Video Launch cannot be executed with file not exist")
                return False
            return VideoPlayer.launch(self.path, self.with_full_screen)
        if Video.CLOSE == self.action:
            return VideoPlayer.close()
        if Video.PAUSE == self.action:
            return VideoPlayer.toggle_play_pause(to_pause=True)
        if Video.UN_PAUSE == self.action:
            return VideoPlayer.toggle_play_pause(to_pause=False)
        if Video.SWITCH_TO_WINDOWED_MODE == self.action:
            return VideoPlayer.toggle_window(to_fullscreen=False)
        if Video.SWITCH_TO_FULLSCREEN_MODE == self.action:
            return VideoPlayer.toggle_window(to_fullscreen=True)
        if Video.ENABLE_LOOP_VIDEO == self.action:
            return VideoPlayer.toggle_loop_video(to_enable=True)
        if Video.DISABLE_LOOP_VIDEO == self.action:
            return VideoPlayer.toggle_loop_video(to_enable=False)


##
# @brief        Exposed enum class for Mouse events
class Mouse(object):
    CLICK_LEFT = "CLICK_LEFT"
    CLICK_RIGHT = "CLICK_RIGHT"
    SCROLL_RANDOM = "SCROLL_RANDOM"
    CURSOR_MOVE_RANDOM = "CURSOR_MOVE_RANDOM"

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class App
    def __init__(self, action):
        self.action = action

    ##
    # @brief        Overridden str method
    # @return       string representation for Mouse
    def __repr__(self):
        return f"App: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        if Mouse.CLICK_LEFT == self.action:
            return MouseEvents.click_left()
        if Mouse.CLICK_RIGHT == self.action:
            return MouseEvents.click_right()
        if Mouse.SCROLL_RANDOM == self.action:
            return MouseEvents.scroll_random()
        if Mouse.CURSOR_MOVE_RANDOM == self.action:
            return MouseEvents.move_random()


##
# @brief        Exposed enum class for DxApplications
class DxSnipAndSketchApplication(object):
    LAUNCH_SNIPTOOL_IN_MAXIMIZED = "LAUNCH_SNIPTOOL_IN_MAXIMIZED"
    LAUNCH_SNIPTOOL_IN_WINDOWED = "LAUNCH_SNIPTOOL_IN_WINDOWED"
    CLOSE = "CLOSE"
    DRAW_RANDOM = "DRAW_RANDOM"

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class DxApplication
    def __init__(self, action):
        self.action = action
        self.maximized = self.action == DxSnipAndSketchApplication.LAUNCH_SNIPTOOL_IN_MAXIMIZED

    ##
    # @brief        Overridden str method
    # @return       string representation for DxApplication
    def __repr__(self):
        return f"App: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        if self.action in [DxSnipAndSketchApplication.LAUNCH_SNIPTOOL_IN_WINDOWED,
                           DxSnipAndSketchApplication.LAUNCH_SNIPTOOL_IN_MAXIMIZED]:
            return DxAppSnipAndSketchActivities.launch(self.maximized)
        if DxSnipAndSketchApplication.CLOSE == self.action:
            return DxAppSnipAndSketchActivities.close()
        if DxSnipAndSketchApplication.DRAW_RANDOM == self.action:
            return DxAppSnipAndSketchActivities.draw_random()


##
# @brief        Exposed enum class for WindowApplication
class WindowApplication:
    LAUNCH_IN_MAXIMIZED = "LAUNCH_IN_MAXIMIZED"
    LAUNCH_IN_WINDOWED = "LAUNCH_IN_WINDOWED"
    CLOSE = "CLOSE"
    MOVE_WINDOW_RANDOM_SAME_SCREEN = "MOVE_WINDOW_RANDOM_SAME_SCREEN"

    ##
    # @brief        Overridden call method
    # @param[in]    action - action attribute from class WindowApplication
    # @param[in]    app_name - exe name of the app to launch/close
    # @param[in]    app_path - Path/URL of the page to open
    def __init__(self, action, app_name=None, app_path=None):
        self.action = action
        self.maximized = self.action == WindowApplication.LAUNCH_IN_MAXIMIZED
        self.app_name = app_name
        self.app_path = app_path

    ##
    # @brief        Overridden str method
    # @return       string representation for App
    def __repr__(self):
        return f"App: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        if self.action in [WindowApplication.LAUNCH_IN_WINDOWED, WindowApplication.LAUNCH_IN_MAXIMIZED] and \
                self.app_name is not None:
            return WinAppActivities.launch(self.maximized, self.app_name, self.app_path)
        if WindowApplication.CLOSE == self.action:
            return WinAppActivities.close(self.app_name)
        if WindowApplication.MOVE_WINDOW_RANDOM_SAME_SCREEN == self.action:
            return WinAppActivities.move_window_random_same_screen()


##
# @brief        Exposed enum class for Game
class Game(object):
    LAUNCH_IN_FULLSCREEN = "LAUNCH_IN_FULLSCREEN"
    LAUNCH_IN_WINDOWED = "LAUNCH_IN_WINDOWED"
    CLOSE = "CLOSE"

    ##
    # @brief        Overridden call method
    # @param[in]    action - action attribute from class Game
    # @param[in]    application
    def __init__(self, action, application):
        self.action = action
        self.with_full_screen = self.action == Game.LAUNCH_IN_FULLSCREEN
        self.app = application

    ##
    # @brief        Overridden str method
    # @return       string representation for Game
    def __repr__(self):
        return f"Game: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        status = True
        vrr_bin_folder = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
        if self.action == Game.LAUNCH_IN_FULLSCREEN:
            if self.app == Apps.Classic3DCubeApp:
                path = os.path.join(vrr_bin_folder, Apps.Classic3DCubeApp)
            else:
                path = os.path.join(vrr_bin_folder, Apps.FlipAt)

            reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                                     reg_path=r"Software\Microsoft")
            if registry_access.write(args=reg_args, reg_name=path, reg_type=registry_access.RegDataType.SZ,
                                     reg_value="GpuPreference=0;VRREligibleOverride=1",
                                     sub_key=r"DirectX\UserGpuPreferences") is False:
                logging.error(f"\tFailed to update value ='GpuPreference=0;VRREligibleOverride=1' for {path=}")
                return False

            # Open given VRR testing app for each panel
            if open_gaming_app(self.app, True, None, None) is False:
                logging.error(f"\tFailed to open {self.app} app(Test Issue)")
                return False
            logging.info(f"\tLaunched {self.app} app successfully")
        if self.action == Game.LAUNCH_IN_WINDOWED:
            if self.app == Apps.Classic3DCubeApp:
                path = os.path.join(vrr_bin_folder, Apps.Classic3DCubeApp)
            else:
                path = os.path.join(vrr_bin_folder, Apps.FlipAt)

            reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                                     reg_path=r"Software\Microsoft")
            if registry_access.write(args=reg_args, reg_name=path, reg_type=registry_access.RegDataType.SZ,
                                     reg_value="GpuPreference=0;VRREligibleOverride=1",
                                     sub_key=r"DirectX\UserGpuPreferences") is False:
                logging.error(f"\tFailed to update value ='GpuPreference=0;VRREligibleOverride=1' for {path=}")
                return False
            # Open given VRR testing app
            if open_gaming_app(self.app, False, None, None) is False:
                logging.error(f"\tFailed to open {self.app} app(Test Issue)")
                return False
            logging.info(f"\tLaunched {self.app} app successfully")
        if self.action == Game.CLOSE:
            if close_gaming_app() is False:
                logging.error("\tFailed to close {0} app(Test Issue)".format(self.app))
                return False
            logging.info("\tClosed the app successfully")
        return status


##
# @brief        Exposed enum class for Windowed keypress event
class KeyBoardPress(object):
    WIN_M = "WIN_M"
    WIN_A = "WIN_A"
    WIN_D = "WIN_D"
    ALT_TAB = "ALT_TAB"
    ALT_ENTER = "ALT_ENTER"
    SPACE_BAR = "SPACE_BAR"
    WIN_I = "WIN_I"

    ##
    # @brief        Overridden call method
    # @param[in]    keyboard_action - Keyboard action to be performed
    def __init__(self, keyboard_action):
        self.action = keyboard_action

    ##
    # @brief        Overridden str method
    # @return       string representation for Wait
    def __repr__(self):
        return f"Keyboard Press : {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       None
    def trigger(self):
        if self.action is None:
            logging.error("Required key board press is not provided. cannot be executed as None")
            return False
        if self.action == KeyBoardPress.WIN_M:
            return kb.press("WIN+M")
        elif self.action == KeyBoardPress.WIN_A:
            return kb.press("WIN+A")
        elif self.action == KeyBoardPress.WIN_D:
            return kb.press("WIN+D")
        elif self.action == KeyBoardPress.WIN_I:
            return kb.press("WIN+I")
        elif self.action == KeyBoardPress.ALT_TAB:
            return kb.press("ALT+TAB")
        elif self.action == KeyBoardPress.ALT_ENTER:
            return kb.press("ALT+ENTER")
        elif self.action == KeyBoardPress.SPACE_BAR:
            return kb.press(" ")


##
# @brief        Exposed enum class for TDR related action
class Tdr(object):
    GENERATE = "GENERATE"
    DETECT = "DETECT"
    CLEAR = "CLEAR"

    ##
    # @brief        Overridden call method
    # @param[in]    action - action attribute from class TDR
    # @param[in]    gfx_index - graphics adapter index
    def __init__(self, action, gfx_index):
        self.action = action
        self.gfx_index = gfx_index

    ##
    # @brief        Overridden str method
    # @return       string representation for Game
    def __repr__(self):
        return f"TDR action: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       None
    def trigger(self):
        if self.action == Tdr.GENERATE:
            return generate_tdr(self.gfx_index, is_displaytdr=True)
        elif self.action == Tdr.DETECT:
            return detect_system_tdr(self.gfx_index)
        elif self.action == Tdr.CLEAR:
            return clear_tdr()
        else:
            return False


##
# @brief        Exposed enum class for Mode
class Mode(object):
    ROTATE_SCREEN_TO_0 = "ROTATE_SCREEN_TO_0"
    ROTATE_SCREEN_TO_90 = "ROTATE_SCREEN_TO_90"
    ROTATE_SCREEN_TO_180 = "ROTATE_SCREEN_TO_180"
    ROTATE_SCREEN_TO_270 = "ROTATE_SCREEN_TO_270"
    REFRESH_RATE_MAX = "REFRESH_RATE_MAX"
    REFRESH_RATE_MIN = "REFRESH_RATE_MIN"
    RESOLUTION_MIN = "RESOLUTION_MIN"
    RESOLUTION_MAX = "RESOLUTION_MAX"

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class Mode
    # @param[in]    adapter object, dut Adapter object
    # @param[in]    panel object, dut Panel object
    def __init__(self, action, adapter: dut_context.Adapter, panel: dut_context.Panel):
        self.action = action
        self.adapter = adapter
        self.panel = panel

    ##
    # @brief        Overridden str method
    # @return       string representation for Mode
    def __repr__(self):
        return f"Mode: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, True, if successful, False otherwise
    def trigger(self):
        mode = display_config.DisplayConfiguration().get_current_mode(self.panel.target_id)

        if self.action == Mode.ROTATE_SCREEN_TO_0:
            mode.rotation = RotateScreen.TO_0
        elif self.action == Mode.ROTATE_SCREEN_TO_90:
            mode.rotation = RotateScreen.TO_90
        elif self.action == Mode.ROTATE_SCREEN_TO_180:
            mode.rotation = RotateScreen.TO_180
        elif self.action == Mode.ROTATE_SCREEN_TO_270:
            mode.rotation = RotateScreen.TO_270
        elif self.action == Mode.REFRESH_RATE_MIN:
            mode = common.get_display_mode(self.panel.target_id, self.panel.min_rr)
        elif self.action == Mode.REFRESH_RATE_MAX:
            mode = common.get_display_mode(self.panel.target_id, self.panel.max_rr)
        elif self.action == Mode.RESOLUTION_MIN:
            modes = common.get_display_mode(self.panel.target_id, refresh_rate=self.panel.max_rr, limit=2)
            mode = modes[-1]
        elif self.action == Mode.RESOLUTION_MAX:
            modes = common.get_display_mode(self.panel.target_id, refresh_rate=self.panel.max_rr, limit=2)
            mode = modes[0]

        html.step_start(f"Applying {self.action} ({mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz)")
        status = display_config.DisplayConfiguration().set_display_mode([mode], False)
        # with rotation observed failing in refresh panel caps , ignoring for rotation.
        if self.action not in [Mode.ROTATE_SCREEN_TO_0, Mode.ROTATE_SCREEN_TO_90,
                               Mode.ROTATE_SCREEN_TO_180, Mode.ROTATE_SCREEN_TO_270]:
            dut.refresh_panel_caps(self.adapter)
        html.step_end()
        return status


##
# @brief        Exposed enum class for Etl
class Etl(object):
    START = "START"
    STOP = "STOP"

    ##
    # @brief        Overridden call method
    # @param[in]    action attribute, action attribute from class Etl
    # @param[in]    file_name optional, file_name to be given after stopping ETL
    def __init__(self, action, file_name: str = None):
        self.action = action
        # Default ETL name for ETL
        if file_name is None:
            self.file_name = "GfxTrace" if self.action == Etl.START else "WorkloadTrace"
        else:
            self.file_name = file_name

    ##
    # @brief        Overridden str method
    # @return       string representation for Etl
    def __repr__(self):
        return f"ETL: {self.action}"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       bool, str, True and etl_file if successful, False and None otherwise
    def trigger(self):
        # check to make sure File name is string type only
        if not isinstance(self.file_name, str):
            logging.error(f"{self.file_name} is not of String type")
            return False, None
        return etl_tracer_stop_existing_and_start_new(self.file_name)


##
# @brief        Exposed enum class for Wait
class Wait(object):

    ##
    # @brief        Overridden call method
    # @param[in]    delay int, time to wait for specific seconds
    def __init__(self, delay: int):
        self.time = delay

    ##
    # @brief        Overridden str method
    # @return       string representation for Wait
    def __repr__(self):
        return f"WAIT: {self.time} seconds"

    ##
    # @brief        Method to trigger the event (not to be used outside current file)
    # @return       None
    def trigger(self):
        if self.time is None:
            logging.error("Required wait time is not provided. Wait cannot be executed with time as None")
            return False
        return time.sleep(self.time)


##
# @brief        Exposed enum class for VideoPlayer actions
class VideoPlayer:
    ##
    # @brief        Exposed method to launch video
    # @param[in]    media_file str, complete path to the media file
    # @param[in]    with_full_screen bool, True for Fullscreen, False for Windowed mode
    # @return       None
    @staticmethod
    def launch(media_file: str, with_full_screen: bool) -> None:
        html.step_start(f"Launching {media_file} Video in {'Fullscreen' if with_full_screen else 'Windowed'} mode")
        app_controls.launch_video(media_file, with_full_screen)
        logging.info(f"\tVideo is Playing in {'Fullscreen' if with_full_screen else 'Windowed'} mode ")
        html.step_end()

    ##
    # @brief        Exposed method to close video
    # @return       None
    @staticmethod
    def close() -> None:
        html.step_start(f"Closing Video")
        window_helper.close_media_player()
        html.step_end()

    ##
    # @brief        Exposed method to toggle window of VideoPlayer
    # @param[in]    to_fullscreen bool, this will be just for logging purpose. Either way code will press "ALT+Enter"
    # @return       bool, True if successful False otherwise
    @staticmethod
    def toggle_window(to_fullscreen: bool) -> bool:
        html.step_start(f"Toggle Window mode of the player")
        is_video_playing = False
        for process in window_helper.PROCESS_VIDEO_PLAYER:
            logging.debug(f"\tChecking {process} is running")
            if window_helper.is_process_running(process) is True:
                is_video_playing = True
                break

        if is_video_playing is False:
            logging.error("\tNO Video Player process found")
            html.step_end()
            return False

        kb.press("ALT_ENTER")
        logging.info(f"\tSuccessfully toggled video player to {'Fullscreen' if to_fullscreen else 'Windowed'}")
        html.step_end()
        return True

    ##
    # @brief        Exposed method to toggle Play/ Pause of VideoPlayer
    # @param[in]    to_pause bool, this will be just for logging purpose. Either way code will press "SPACE"
    # @return       bool, True if successful False otherwise
    @staticmethod
    def toggle_play_pause(to_pause: bool) -> bool:
        html.step_start(f"{'Pausing' if to_pause else 'Un-pausing'} the video")
        is_video_playing = False
        for process in window_helper.PROCESS_VIDEO_PLAYER:
            logging.debug(f"\tChecking {process} is running")
            if window_helper.is_process_running(process) is True:
                is_video_playing = True
                break
        if is_video_playing is False:
            logging.error("\tNO Video Player process found")
            html.step_end()
            return False

        kb.press(" ")
        logging.info(f"\tSuccessfully {'Paused' if to_pause else 'Un-paused'} the video")
        html.step_end()
        return True

    ##
    # @brief        Exposed method to toggle loop button of VideoPlayer.
    # @param[in]    to_enable bool, this will be just for logging purpose. Either way code will press "CTRL+T"
    # @return       bool, True if successful False otherwise
    @staticmethod
    def toggle_loop_video(to_enable: bool) -> bool:
        html.step_start(f"{'Enabling' if to_enable else 'Disabling'} looping of video")
        is_video_playing = False
        for process in window_helper.PROCESS_VIDEO_PLAYER:
            logging.debug(f"\tChecking {process} is running")
            if window_helper.is_process_running(process) is True:
                is_video_playing = True
                break
        if is_video_playing is False:
            logging.error("\tNO Video Player process found")
            html.step_end()
            return False

        kb.press("CTRL+T")
        logging.info(f"\tSuccessfully {'Enabled' if to_enable else 'Disabled'} looping of video")
        html.step_end()
        return True


##
# @brief Exposed enum class for Mouse actions
class MouseEvents:
    ##
    # @brief        Exposed method to click left.
    # @return       None
    @staticmethod
    def click_left() -> bool:
        html.step_start(f"Mouse Left click")
        left, top, right, bottom = get_app_coordinates()
        if None in (left, top, right, bottom):
            return False
        window_helper.mouse_left_click(left, top)
        html.step_end()
        return True

    ##
    # @brief        Exposed method to click right
    # @return       None
    @staticmethod
    def click_right() -> bool:
        html.step_start(f"Mouse right click")
        left, top, right, bottom = get_app_coordinates()
        if None in (left, top, right, bottom):
            return False
        window_helper.mouse_right_click(left, top)
        html.step_end()
        return True

    ##
    # @brief        Exposed method to scroll randomly
    # @return       None
    @staticmethod
    def scroll_random() -> bool:
        html.step_start(f"Scroll randomly")
        left, top, right, bottom = get_app_coordinates()
        if None in (left, top, right, bottom):
            return False
        window_helper.random_mouse_scroll(top // 2, bottom // 2, 30)
        html.step_end()
        return True

    ##
    # @brief        Random mouse movement
    # @return       None
    @staticmethod
    def move_random() -> bool:
        html.step_start(f"Random mouse movement")
        bapp = app.SnipSketch()
        if bapp is None:
            return False
        bapp.random_mouse_move(30)
        html.step_end()
        return True


##
# @brief        Exposed enum class for DxAppSnipAndSketchActivities actions
class DxAppSnipAndSketchActivities:
    ##
    # @brief        Exposed method to launch Snipping tool
    # @param[in]    is_maximized - True if maximized, False otherwise
    # @return       None
    @staticmethod
    def launch(is_maximized) -> None:
        html.step_start(f"Launching Snipping tool")
        bapp = app.SnipSketch()
        bapp.open_app(is_maximized)
        html.step_end()

    ##
    # @brief        Exposed method to close snipping tool
    # @return       None
    @staticmethod
    def close() -> None:
        html.step_start(f"Closing Dx App")
        window_helper.close_dx_apps()
        html.step_end()

    ##
    # @brief        Exposed method to draw randomly
    # @return       None
    @staticmethod
    def draw_random() -> None:
        html.step_start(f"Drawing randomly")
        bapp = app.SnipSketch()
        bapp.draw_random(30)
        html.step_end()

##
# @brief        Exposed enum class for WindowApp Activities
class WinAppActivities:
    ##
    # @brief        Exposed method to launch Window app
    # @param[in]    is_maximized - True if maximized, False otherwise
    # @param[in]    application_type - exe name of the app to launch
    # @param[in]    app_path - Path/URL of the page to open
    # @return       None
    @staticmethod
    def launch(is_maximized, application_type: AppType, app_path) -> None:
        html.step_start(f"Launching {app} Application in {'Fullscreen' if is_maximized else 'Windowed'} mode")
        if application_type == AppType.BROWSER:
            window_helper.open_uri(app_path)
        if application_type == AppType.WORDPAD:
            subprocess.Popen(["write.exe", app_path])
        if is_maximized:
            kb.press('ALT+" "')
            kb.press('x')
        html.step_end()

    ##
    # @brief        Exposed method to close Window app
    # @param[in]    app_to_open_close - exe name of the app to close
    # @return       None
    @staticmethod
    def close(app_to_open_close) -> None:
        html.step_start(f"Closing Window Application")
        window_helper.kill_process_by_name(app_to_open_close)
        html.step_end()

    ##
    # @brief        Exposed method to move window across same screen randomly
    # @return       None
    @staticmethod
    def move_window_random_same_screen() -> None:
        html.step_start(f"Moving Window randomly across screen")
        kb.press('ALT+" "')
        # Restore incase if app is maximized
        kb.press('r')
        kb.press('ALT+" "')
        kb.press('m')
        # Select to move the window
        kb.press('LEFT')
        MouseEvents.move_random()
        window_helper.close_dx_apps()
        html.step_end()


##
# @brief         Exposed API to stop existing ETL and start new
# @param[in]     file_name_after_stopping_etl string, name which needs to be updated after stopping existing ETL
# @return        status, stopped_etl, True if successful, False otherwise
def etl_tracer_stop_existing_and_start_new(file_name_after_stopping_etl: str = "GfxTrace"):
    html.step_start("Stopping existing ETL tracer and Starting New")
    # Stop existing ETL
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("\tFAILED to stop existing ETL Tracer")
        html.step_end()
        return False, None
    logging.info("\tSuccessfully stopped existing ETL Tracer")

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
        logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        html.step_end()
        return False, None

    stopped_etl = os.path.join(test_context.LOG_FOLDER, file_name_after_stopping_etl + '.' + str(time.time()) + ".etl")
    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, stopped_etl)
    logging.info(f"\tSuccessfully renamed ETL file to {stopped_etl}")

    # Start new ETL
    if etl_tracer.start_etl_tracer() is False:
        logging.error("\tFAILED to start new ETL tracer (Test Issue)")
        html.step_end()
        return False, None
    logging.info("\tSuccessfully started new ETL Tracer")

    html.step_end()
    return True, stopped_etl


##
# @brief         Exposed API to get the app co-ordinates
# @return        l, r, t, b -> Left, right, top, bottom co-ordinates of the app
def get_app_coordinates():
    # Base code taken from drag_app_across_screen() of window_helper.py file
    displayconfig = display_config.DisplayConfiguration().get_config()

    # updating Monitor dimension dictionary based on list return by get_config API.
    monitor_dimension = {}  # [(0, (0, 0, 1280, 853)), (1, (1910, 0, 1280, 0))]
    monitor_dimension_from_enum_display = window_helper.get_enum_display_monitors_list()
    if monitor_dimension_from_enum_display is None:
        logging.error("get_enum_display_monitor_list_fail")
        return None, None, None, None
    for display_config_index in range(displayconfig.numberOfDisplays):
        for enum_display_index in range(len(monitor_dimension_from_enum_display)):
            monitor_data = win32api.GetMonitorInfo(monitor_dimension_from_enum_display[enum_display_index][0])
            if monitor_data["Device"] == displayconfig.displayPathInfo[display_config_index]. \
                    displayAndAdapterInfo.ViewGdiDeviceName:
                monitor_dimension[display_config_index] = monitor_data["Monitor"]

    l, t, r, b = 0, 0, 0, 0
    win_index = None
    for hwnd, text, cls in window_helper.enum_windows():
        left, top, right, bottom = GetWindowPlacement(hwnd)[4]
        for i in range(len(monitor_dimension)):
            l, t, r, b = monitor_dimension[i]
            if left in range(l, r) and top in range(t, b):
                win_index = i

        if win_index is None:
            logging.error("Unable to find screen for App coordinates")
            logging.info(
                f"App coordinates->{l},{t},{r},{b} was not found in any of the screen coordinates "
                f"{monitor_dimension}")
            raise Exception("Unable to find screen for App coordinates")
    return l, t, r, b
