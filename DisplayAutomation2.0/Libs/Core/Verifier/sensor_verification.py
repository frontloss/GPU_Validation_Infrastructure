########################################################################################################################
# @file     sensor_verification.py
# @brief    This module is used to check corruption using sensor modules
# @author   Chandrakanth Pabolu, Kumar, Ashish3
########################################################################################################################
import logging

from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify


##
# @brief    API to initialize sensor verification module
# @return   None
def initialize():
    pass


##
# @brief        verify and detect corruption using sensors
# @return       None
def verify():
    if VerifierCfg.sensor_verification == Verify.SKIP:
        logging.info("Sensor verification is skipped")
        return


##
# @brief        API to cleanup sensor verification module
# @return       None
def cleanup():
    pass
