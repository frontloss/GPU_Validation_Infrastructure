######################################################################################
# \file         os_hdr_verification.py
# \section      os_hdr_verification
# \remarks      This script contains helper functions to perform functional verification of HDR
# \ref          os_hdr_verification.py \n
# \author       Smitha B
######################################################################################
import ctypes
import logging
import importlib
from Libs.Core import system_utility as sys_utility
from Libs.Core.display_config.display_config_enums import HDRErrorCode, CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Core import enum
from registers.mmioregister import MMIORegister
from Tests.Color import color_verification
from Tests.Color.color_common_utility import get_current_pipe
FEATURE_ENABLE_DISABLE_SUCCESS = 0


class OSHDRVerification(object):
    reg_read = MMIORegister()

    def is_error(self, feature, error_code, op_type):
        if error_code == HDRErrorCode(FEATURE_ENABLE_DISABLE_SUCCESS).value:
            logging.info("Feature : %s : %s : SUCCESS" %(feature, op_type))
            return True
        else:
            logging.error("Feature : %s  %s : FAILURE; Error_Code : %s" %(feature, op_type, HDRErrorCode(error_code).name))
            return False

    def verify_hdr_mode(self, display, hdr_enable_status, platform):
        current_pipe = get_current_pipe(display)

        pipe_misc = importlib.import_module("registers.%s.PIPE_MISC_REGISTER" % platform)
        pipe_misc_reg = 'PIPE_MISC' + '_' + current_pipe
        pipe_misc_reg_value = self.reg_read.read('PIPE_MISC_REGISTER', pipe_misc_reg, platform)
        status = False
        if hdr_enable_status == "ENABLE":
            if pipe_misc_reg_value.__getattribute__("hdr_mode") == getattr(pipe_misc, 'hdr_mode_ENABLE'):

                logging.info('PASS: %s - HDR Enable Status: Expected = ENABLE, Actual = ENABLE' % pipe_misc_reg)
                status = True
            else:
                logging.error('FAIL: %s - HDR Enable Status: Expected = ENABLE, Actual = DISABLE' % pipe_misc_reg)
                status = False
        else:
            if pipe_misc_reg_value.__getattribute__("hdr_mode") == getattr(pipe_misc, 'hdr_mode_DISABLE'):

                logging.info('PASS: %s - HDR Enable Status: Expected = DISABLE, Actual = DISABLE' % pipe_misc_reg)
                status = True
            else:
                logging.error('FAIL: %s - HDR Enable Status: Expected = DISABLE, Actual = ENABLE' % pipe_misc_reg)
                status = False

        if status:
            return True
        else:
            gdhm.report_bug(
                title="[Color][OSHDR] PIPE_MISC for register verification failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

    def verify_hdr_persistence(self, event_name, enumerated_displays, platform, display_list, overlay="NO", topology="NOTCLONE"):
        display = ""
        os_hdr_status = ""
        plane_status = ""
        for display_index in range(enumerated_displays.Count):
            os_hdr_status = False
            plane_status = False
            if str(CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) in display_list:
                if enumerated_displays.ConnectedDisplays[display_index].IsActive:
                    display = str(CONNECTOR_PORT_TYPE(
                        enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
                    ##
                    # Verify PIPE_MISC for register verification
                    if topology == "NOTCLONE":
                        if self.verify_hdr_mode(display, "ENABLE", platform) is False:
                            logging.error("HDR is not enabled after %s  and config: %s"%(event_name, topology))
                            return os_hdr_status
                        else:
                            logging.info("HDR was still enabled after %s and config %s"%(event_name, topology))
                            os_hdr_status = True
                            if overlay == "YES":

                                if color_verification.get_video_sprite_status(display, 'PLANE_CTL_2',
                                                                              'PLANE_COLOR_CTL_1'):
                                    logging.error("FAIL: Video Plane Status Expected: Disable and Actual:Enable")
                                    plane_status = False
                                    return plane_status
                                else:
                                    logging.info("PASS: Video Plane Status Expected: Disable and Actual:Disable")
                                    plane_status = True

                    else:
                        if self.verify_hdr_mode(display, "DISABLE", platform) is False:
                            logging.error("HDR was enabled after %s and config %s" % (event_name, topology))
                            return os_hdr_status
                        else:
                            logging.info("HDR was disabled after %s and config %s" % (event_name, topology))
                            os_hdr_status = True
                else:
                    logging.error("Plugged display %s was  inactive" % (CONNECTOR_PORT_TYPE(
                        enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))
                    logging.error("Plugged display was  inactive")
                    return os_hdr_status

        if os_hdr_status is True and overlay == "NO" and plane_status is "True":
            return os_hdr_status
        elif os_hdr_status is True and overlay == "YES" and plane_status is "True":
            return os_hdr_status
