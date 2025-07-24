###############################################################################
# @file   display_audio_ult.py
# @brief  display_audio_ult.py tests API's for display_audio.py
# @author Kumar, Rohit
###############################################################################

import logging

from Libs.Core.test_env.test_environment import *
from Libs.Feature.display_audio import *


##
# @brief    Fetches audio Controller loaded
# @return   None
def is_audio_controller_present():
    audio_driver, device_id, _ = audio.get_audio_controller()
    logging.info("******************* Driver Information *******************")
    if audio_driver is not None:
        if audio_driver == AudioControllerType.INTEL:
            logging.info("Intel Audio Controller is present")
        if audio_driver == AudioControllerType.MS:
            logging.info("MS Audio Controller is present")
        if audio_driver == AudioControllerType.NONE:
            logging.info("No Audio Controller is present")
    else:
        logging.error("Return value is none")


##
# @brief    Fetches audio Codec loaded
# @return   None
def is_audio_driver_present():
    audio_driver = audio.get_audio_driver()
    logging.info("******************* Driver Information *******************")
    if audio_driver is not None:
        if audio_driver == AudioCodecDriverType.INTEL:
            logging.info("Intel Audio Driver is present")
        if audio_driver == AudioCodecDriverType.MS:
            logging.info("MS Audio Driver is present")
        if audio_driver == AudioCodecDriverType.ACX:
            logging.info("ACX Audio Driver is present")
        if audio_driver == AudioCodecDriverType.NONE:
            logging.info("No Audio Driver is present")
    else:
        logging.error("Return value is none")


##
# @brief    Fetches audio endpoints present
# @return   None
def get_audio_endpoints():
    audio_endpoints = audio.get_audio_endpoints()
    logging.info("******************* Audio Endpoints Information *******************")
    if audio_endpoints is not None:
        logging.info("Number of Audio Endpoints : {0}".format(audio_endpoints))
    else:
        logging.error("Return value is none")


##
# @brief    Audio verification for the number of endpoints loaded
# @return   None
def audio_verification():
    endpoint_status, endpoint_count = audio.audio_verification()
    verification_status = endpoint_status
    logging.info("******************* Audio Verification Information *******************")
    if verification_status is not None:
        if verification_status is True:
            logging.info("Audio verification passed")
        else:
            logging.info("Audio verification failed")
    else:
        logging.error("Return value is none")


if __name__ == '__main__':
    # Initializing test environment
    TestEnvironment.initialize()

    audio = DisplayAudio()

    is_audio_controller_present()
    is_audio_driver_present()
    get_audio_endpoints()
    audio_verification()
