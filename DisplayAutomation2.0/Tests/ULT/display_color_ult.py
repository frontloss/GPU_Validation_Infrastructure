######################################################################################
# \file
# \section display_color_base
# \remarks
# \ref display_color_ult.py \n
# Each function in this base will verify the functionality of DisplayColor.dll and system_utility.dll.
# Commandline : python Tests\ULT\display_color_ult.py <Display1><Display2>< ... >
# \author   Raghupathy, Dushyanth Kumar
######################################################################################
from Libs.Core.test_env.test_environment import *
from Libs.Feature.display_color import *


def isXvyccSupportedByDisplayId(target_id):
    try:
        result = color.is_xvycc_supported_by_display_id(target_id)

        if result == 1:
            logging.info("Pass: Getting XVYCC Support by Display ID {} is Success".format(target_id))
            logging.info("XVYCC is Supported")

        elif result == 0:
            logging.info("Pass: Getting XVYCC Support by Display ID {} is Success".format(target_id))
            logging.info("XVYCC is Not Supported")

        else:
            logging.error("Fail: Getting XVYCC Support by Display ID {} is Failed".format(target_id))

    except Exception as ex:
        logging.error("Fail: Getting XVYCC Support by Display ID {} is Failed".format(target_id))
        logging.debug("Exception Msg: {}".format(ex))


def isYcbcrSupportedByDisplayId(target_id):
    try:
        result = color.is_ycbcr_supported_by_display_id(target_id)

        if result == 1:
            logging.info("Pass: Getting YCBCR Support by Display ID {} is Success".format(target_id))
            logging.info("YCBCR is Supported")

        elif result == 0:
            logging.info("Pass: Getting YCBCR Support by Display ID {} is Success".format(target_id))
            logging.info("YCBCR is Not Supported")

        else:
            logging.error("Fail: Getting YCBCR Support by Display ID {} is Failed".format(target_id))

    except Exception as ex:
        logging.error("Fail: Getting YCBCR Support by Display ID {} is Failed".format(target_id))
        logging.debug("Exception Msg: {}".format(ex))


def enableDisableXvycc(target_id):
    try:
        status = True
        if color.enable_disable_xvycc(target_id, True):
            if color.is_xvycc_supported_by_display_id(target_id) is True:
                logging.info("Pass: Enable XVYCC is Success")
            else:
                logging.info("Fail: Failed to Enable XVYCC")
                status = False
        else:
            logging.error("Fail: Failed to Enable XVYCC")
            status = False

        if color.enable_disable_xvycc(target_id, False):
            if color.is_xvycc_supported_by_display_id(target_id) is False:
                logging.info("Pass: Disable XVYCC is Success")
            else:
                logging.info("Fail: Failed to Disable XVYCC")
                status = False
        else:
            logging.error("Fail: Failed to Disable XVYCC")
            status = False

        if status:
            logging.info('EnableDisableXvycc Success')
        else:
            logging.error('EnableDisableXvycc Failed')

    except Exception as ex:
        logging.error("Fail: Failed to Disable XVYCC")
        logging.debug("Exception Msg: {}".format(ex))


def enableDisableYcbcr(target_id):
    try:
        status = True
        if color.enable_disable_ycbcr(target_id, True):
            if color.is_ycbcr_supported_by_display_id(target_id) is True:
                logging.info("Pass: Enable YCBCR is Success")
            else:
                logging.info("Fail: Failed to Enable YCBCR")
                status = False
        else:
            logging.error("Fail: Failed to Enable YCBCR")
            status = False

        if color.enable_disable_ycbcr(target_id, False):
            if color.is_ycbcr_supported_by_display_id(target_id) is False:
                logging.info("Pass: Disable YCBCR is Success")
            else:
                logging.info("Fail: Failed to Disable YCBCR")
                status = False
        else:
            logging.error("Fail: Failed to Disable YCBCR")
            status = False

        if status:
            logging.info('EnableDisableYcbcr Success')
        else:
            logging.error('enableDisableYcbcr Failed')

    except Exception as ex:
        logging.error("Fail: Failed to Disable YCBCR")
        logging.debug("Exception Msg: {}".format(ex))


if __name__ == '__main__':
    # Initializing test environment
    TestEnvironment.initialize()

    color = Color()
    config = DisplayConfiguration()

    enumerated_displays = config.get_enumerated_display_info()
    for index in range(enumerated_displays.Count):
        targetid = enumerated_displays.ConnectedDisplays[index].TargetID

        isXvyccSupportedByDisplayId(targetid)
        isYcbcrSupportedByDisplayId(targetid)

        # enableDisableXvycc(targetid)
        # enableDisableYcbcr(targetid)
