########################################################################################################################
# @file         stress_scenarios.py
# @brief        The script consists of stress test scenarios
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import time

from Libs.Core import winkb_helper
from Tests.PlanesUI.Common import planes_ui_helper


##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_one(app='MEDIA'):
    logging.info("Scenario-1: Running Basic Media Scenarios")
    app_instance = planes_ui_helper.create_app_instance(app)
    for i in range(0, 50):
        # Windowed mode
        app_instance.open_app(minimize=True)
        time.sleep(5)
        # Move to full screen
        winkb_helper.press('F11')
        logging.info(f"Changing {app} to FullScreen Mode")
        # Pause the video
        winkb_helper.press('CTRL+P')
        logging.info("Media playback paused")
        # Unpause the video
        winkb_helper.press('CTRL+P')
        logging.info("Media playback unpaused")
        # @Todo Need to simulate seek scenarios
        '''
        # Move the video forward
        winkb_helper.press('LCTRL + RIGHT')
        logging.info("Seeking the media forward for 30 seconds")
        # Move the video backward
        winkb_helper.press('LCTRL + LEFT')
        logging.info("Seeking the media backward for 10 seconds")
        '''
        app_instance.close_app()


##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_two(app):
    logging.info("Scenario-2: Resize, FullScreen-Windowed Switch and Minimize, Maximize")
    app_instance = planes_ui_helper.create_app_instance(app)
    # windowed mode
    app_instance.open_app(minimize=True)
    time.sleep(5)
    # @todo Resize api throws error after some iterations, need to change the implementation
    '''
    resize_multipliers = [(20, 20), (-10, -15), (10, 10), (-20, -15), (10, 0), (0, -20), (0, 20), (-10, 0)]
    directions = [('right', 'bottom'), ('right', 'top'), ('left', 'top'), ('left', 'bottom')]

    for direction in directions:
        for multiplier in resize_multipliers:
            app_instance.resize(multiplier, direction=direction)
            time.sleep(5)
    '''
    # FullScreen-windowed Switch along with screen minimize and maximize
    for i in range(0, 100):
        winkb_helper.press('ALT_ENTER')
        logging.info(f"Changing {app} to FullScreen Mode")
        winkb_helper.press('WIN+D')
        logging.info("Minimized the window")
        winkb_helper.press('WIN+D')
        logging.info("Maximized the window")
        winkb_helper.press('ALT_ENTER')
        logging.info(f"Changing {app} to Windowed Mode")
        time.sleep(0.5)
    app_instance.close_app()

##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_three(app):
    logging.info("Scenario-3: Open and close application")
    app_instance = planes_ui_helper.create_app_instance(app)
    # open-close
    for i in range(0, 20):
        app_instance.open_app(minimize=True)
        time.sleep(3)
        app_instance.close_app()


##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_four(app):
    logging.info("Scenario-4: Play in windowed pause, scale to full screen unpause, scale back to windowed ")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(minimize=True)
    time.sleep(5)
    for i in range(0, 100):
        winkb_helper.press('CTRL+P')
        logging.info("Media playback paused")
        winkb_helper.press('F11')
        logging.info(f"Changing {app} to FullScreen Mode")
        winkb_helper.press('CTRL+P')
        logging.info("Media playback unpaused")
        winkb_helper.press('ALT_ENTER')
        logging.info(f"Changing {app} to Windowed Mode")
    app_instance.close_app()

##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_five(app):
    logging.info("Scenario-5: Enable and Disable Charms")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True, minimize=True)
    time.sleep(5)
    # Enable and disable charms every 5 seconds, enable media controls in case of media
    for i in range(20):
        # to enable charms
        winkb_helper.press('WIN+A')
        logging.info(f"Charms is Enabled")
        time.sleep(2)
        # to disable charms
        winkb_helper.press('ESC')
        logging.info(f"Charms is disabled")
    app_instance.close_app()


##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_six(app):
    logging.info("Scenario-6: Switch between apps")
    app_instance = planes_ui_helper.create_app_instance(app)
    app_instance.open_app(is_full_screen=True, minimize=True)
    time.sleep(5)
    for i in range(0, 50):
        winkb_helper.press('ALT+TAB')
        logging.info(f"Switched the screen")
        time.sleep(0.5)
    app_instance.close_app()


'''
##
# @brief        Function to run basic media scenarios
# @param[in]    app : Name of the app
# @return       None
def scenario_seven(app):
    logging.info(
        "Scenario-7:  Open Media and 3D app and position them, Resize the media and switch between "
        "full screen and windowed ")
    # Open Media app and play it in windowed mode
    app_instance_media = planes_ui_helper.create_app_instance(app)
    app_instance_media.open_app(False, minimize=True)
    time.sleep(5)
    app_instance_media.set_half_size(position="top")
    time.sleep(5)
    # Open 3D App and play it in windowed mode
    app_instance_3D = planes_ui_helper.create_app_instance('CLASSICD3D')
    app_instance_3D.open_app(False, minimize=False, position="down")

    for i in range(0, 20):
        for each_multiplier in range(0, 10):
            app_instance_media.resize(multiplier=(3, 3), direction=("right", "bottom"))

        # Set Media app to foreground
        #app_instance_media.set_foreground(app_instance_media.instance)
        #time.sleep(2)
        for each_iteration in range(0, 50):
            winkb_helper.press('F11')
            logging.info(f"Changing {app} to FullScreen Mode")
            time.sleep(0.5)
            winkb_helper.press('ALT_ENTER')
            logging.info(f"Changing {app} to Windowed Mode")
            time.sleep(0.5)
    app_instance_3D.close_app()
'''

scenario_dict = {
    1: scenario_one,
    2: scenario_two,
    3: scenario_three,
    4: scenario_four,
    5: scenario_five,
    6: scenario_six
}
