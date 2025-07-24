########################################################################################################################
# @file         planeformat_logoff_s0ix_s3s4.py
# @brief        Basic test to verify plane format getting enabled with no corruption on video app during display switch.
#               * Apply SINGLE display configuration on display1.
#               * Play the Video app in window mode.
#               * Verify the plane format for SINGLE display configuration.
#               * Invoke s3 and s4 state.
#               * Close the video app.
# @author       Balasubramnayam, Smitha
# @todo         Implement logoff
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check plane format getting enabled with no corruption on video app during display switch
class PlaneformatLogoffs0ixS3S4(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        disp_power = DisplayPower()

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_YUV_422_PACKED_8_BPC"

        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # Apply SINGLE display configuration on display1
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info(self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.mpo_helper.get_display_configuration([self.connected_list[0]], self.enumerated_displays)))
            winkb_helper.press('WIN+M')

            #
            # Play the Video app in Window Mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press('CTRL+T')
            # logging.info("Enabling Repeat option on video playback app")
            # The Opened Application will play for 30 secs
            time.sleep(30)

            # #
            # Verify the plane format
            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
            if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Plane verification failed during media playback",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed during media playback")


            ##
            # The media app will play for 1 minute
            logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info("Watermark verification passed")


            ##
            # Invoke S3/CS state
            if disp_power.is_power_state_supported(PowerEvent.CS):
                if disp_power.invoke_power_event(PowerEvent.CS, 60) is False:
                    self.fail(f"Failed to invoke CS PowerEvent")
            elif disp_power.invoke_power_event(PowerEvent.S3, 60) is False:
                self.fail(f"Failed to invoke S3 PowerEvent")

            time.sleep(5)

            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            logging.info("Watermark verification passed after S3/CS state")



            ##
            # Invoke S4 state
            disp_power.invoke_power_event(PowerEvent.S4, 60)
            time.sleep(10)

            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            logging.info("Watermark verification passed after S4 state")



            ##
            # Close the Video App
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

        else:
            logging.info(
                "Failed to apply display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                    self.connected_list[0]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify MPO getting enabled during media playback \
                and check for under run across S3/S4 state")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
