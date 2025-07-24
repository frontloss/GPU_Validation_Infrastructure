########################################################################################################################
# @file         yt_scenarios.py
# @brief        The script consists of stress test scenarios for YouTube
# @author       Pai, Vinayak1
########################################################################################################################
import subprocess
import time
import logging

from Libs.Core import window_helper, winkb_helper
from Tests.PlanesUI.Common import planes_ui_helper


##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_one(app='YOUTUBE'):
    logging.info("Running Scenario One")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True)
    app_instance.enable_disable_fullscreen()
    time.sleep(60)
    app_instance.enable_disable_captions()
    time.sleep(60)
    for i in range(10):
        app_instance.enable_disable_captions()
    app_instance.close_app()

    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.enable_disable_fullscreen()
    time.sleep(60)
    # @todo need to 4K and 8k Videos
    #window_helper.open_uri(planes_ui_helper.YouTube['RES_4K'].value)
    #time.sleep(60)
    #window_helper.open_uri(planes_ui_helper.YouTube['RES_8K'].value)
    #time.sleep(60)
    app_instance.enable_disable_cinema_mode()
    time.sleep(60)
    app_instance.close_app()


##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_two(app):
    logging.info("Running Scenario Two")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True)
    for i in range(10):
        app_instance.play_pause()
        time.sleep(10)
    app_instance.enable_disable_cinema_mode()
    for i in range(10):
        app_instance.play_pause()
        time.sleep(10)
    app_instance.enable_disable_fullscreen()
    for i in range(10):
        app_instance.play_pause()
        time.sleep(10)
    app_instance.seek_forward()
    time.sleep(10)
    app_instance.seek_backward()
    time.sleep(10)
    for i in range(10):
        app_instance.seek_forward()
        time.sleep(5)
        app_instance.seek_backward()
        time.sleep(5)
    app_instance.close_app()


##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_three(app):
    logging.info("Running Scenario Three")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True)
    for i in range(10):
        app_instance.play_pause()
        time.sleep(10)
        app_instance.enable_disable_captions()
        time.sleep(10)
    app_instance.enable_disable_cinema_mode()
    for i in range(10):
        app_instance.enable_disable_captions()
        time.sleep(10)
    app_instance.enable_disable_fullscreen()
    for i in range(10):
        app_instance.play_pause()
        time.sleep(10)
        app_instance.enable_disable_captions()
        time.sleep(10)
    app_instance.close_app()


##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_four(app):
    logging.info("Running Scenario Four")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True)
    for i in range(10):
        app_instance.enable_disable_cinema_mode()
        time.sleep(10)
    app_instance.enable_disable_cinema_mode()
    time.sleep(2)
    for i in range(10):
        app_instance.enable_disable_fullscreen()
        time.sleep(10)
    for i in range(10):
        app_instance.enable_disable_captions()
        time.sleep(5)
    for i in range(2):
        app_instance.enable_disable_cinema_mode()
    for i in range(10):
        app_instance.enable_disable_fullscreen()
    app_instance.close_app()



##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_five(app):
    logging.info("Running Scenario Five")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(minimize=True)
    time.sleep(10)
    for i in range(10):
        winkb_helper.press('WIN+D')
        time.sleep(2)
    winkb_helper.snap_left()
    subprocess.Popen("notepad")
    time.sleep(2)
    winkb_helper.snap_right()
    time.sleep(30)
    winkb_helper.press('WIN+M')
    winkb_helper.press('ALT+TAB')
    time.sleep(10)
    window_helper.kill_process_by_name('Notepad.exe')
    app_instance.close_app()


##
# @brief            Function to run basic YouTube scenarios
# @param[in]        app : Name of the app
# @return           None
def scenario_six(app):
    logging.info("Running Scenario Six")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app()
    winkb_helper.snap_right()
    app_instance_media = planes_ui_helper.create_app_instance('MEDIA')
    app_instance_media.open_app(is_full_screen=False)
    winkb_helper.snap_left()
    subprocess.Popen("notepad")
    time.sleep(2)
    window_helper.kill_process_by_name('Notepad.exe')
    winkb_helper.press('CTRL+P')
    app_instance.play_pause()
    app_instance_media.close_app()
    time.sleep(2)
    subprocess.Popen('notepad')
    time.sleep(10)
    window_helper.kill_process_by_name('Notepad.exe')
    app_instance.close_app()


scenario_dict = {
    1: scenario_one,
    2: scenario_two,
    3: scenario_three,
    4: scenario_four,
    5: scenario_five,
    6: scenario_six
}
