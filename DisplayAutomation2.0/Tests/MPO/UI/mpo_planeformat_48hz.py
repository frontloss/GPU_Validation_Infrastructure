########################################################################################################################
# @file         mpo_planeformat_48hz.py
# @brief        Basic test to verify the media playback is in MPO mode and checks whether display has switched to 48Hz
#               during media playback on single display eDP.
#               * Plug a single edp display.
#               * Open Media app and play 24fps media on 48hz panel in maximized mode.
#               * Verify the plane format and watermark.
#               * Verify if the display was at 48Hz and calculate the hit count.
#               * Close the MPO app.
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import os
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base
from registers.mmioregister import MMIORegister
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core.test_env import test_context

##
# @brief    Contains function to check whether display has switched to 48Hz during media playback on single eDP
class PlaneFormat48Hz(mpo_ui_base.MPOUIBase):
    expected_refresh_rate = 48

    ##
    # @brief            Get register values
    # @param[in]        display
    # @return           trans link m value
    def get_register_value(self, display):
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        reg_read = MMIORegister()

        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)

        if self.platform in ['skl', 'kbl', 'cfl', 'glk', 'icllp', 'jsl']:
            trans_linkm_reg = "TRANS_LINKM1_EDP"
        else:
            trans_linkm_reg = "TRANS_LINKM1_" + current_pipe

        trans_linkm_value = reg_read.read('LINKM_REGISTER', trans_linkm_reg, self.platform, 0x0)

        return trans_linkm_value.link_m_value

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_YUV_422_PACKED_8_BPC"

        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos/24.000.mp4")

        if len(self.connected_list) != 1:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Test can run only on Single eDP display",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("Test can run only on Single eDP display")

        if 'DP_A' not in self.connected_list:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]eDP should be part of display list to run this test",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("eDP should be part of display list to run this test")

        display_1 = self.connected_list[0]
        if not self.config.set_display_configuration_ex(enum.SINGLE, [display_1]):
            self.fail("Display Configuration failed as %s %s" % (DisplayConfigTopology(enum.SINGLE).name, display_1))
        else:
            logging.info(self.mpo_helper.getStepInfo() + "Applied display configuration as %s %s" % (
                DisplayConfigTopology(enum.SINGLE).name, self.mpo_helper.get_display_configuration([display_1], self.enumerated_displays)))

        winkb_helper.press('WIN+M')

        trans_linkm_reg_value = self.get_register_value(display_1)
        trans_linkm1_edp_reg_value_1 = trans_linkm_reg_value & 0x00FFFFFF

        ##
        # Open Media app and plays it in maximized mode
        self.mpo_helper.play_media(self.media_file, True)

        ##
        # The opened app will play for 30 seconds
        time.sleep(30)

        ##
        # To enable repeat
        winkb_helper.press('CTRL+T')
        # logging.info("Enabling repeat option on media playback application")

        ##
        # Verify the plane format
        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
        if not self.mpo_helper.verify_planes(display_1, 'PLANE_CTL_1', plane1_pixelformat):
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Plane verification failed during media playback",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Plane verification failed during media playback")

        ##


        logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
        if self.wm.verify_watermarks(is_48hz_test=True) is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info("Watermark verification passed")



        ##
        # verify if the display was at 48Hz
        logging.info(self.mpo_helper.getStepInfo() + "Verifying if Display refresh rate set to 48Hz")
        current_mode = self.config.get_current_mode(
            self.config.get_current_display_configuration().displayPathInfo[0].targetId)

        ##
        # Check whether system is hitting 48Hz for 12 times and record the hit count
        hit_count = 0
        hit_status = False
        ratio = float(trans_linkm1_edp_reg_value_1) / current_mode.refreshRate

        for trial in range(10):  # Considering 10 trials
            current_linkm_reg_value = self.get_register_value(display_1)
            current_edp_link_m1_value = current_linkm_reg_value & 0x00FFFFFF
            actual_refresh_rate = current_edp_link_m1_value / ratio
            logging.debug("Trial %s of 10: Refresh rate of the panel is %sHz" % (trial, actual_refresh_rate))
            # Keeping 0.02 as deviation
            if (actual_refresh_rate >= (self.expected_refresh_rate - 0.02)) \
                    and (actual_refresh_rate <= (self.expected_refresh_rate + 0.02)):
                hit_count += 1
                hit_status = True


        logging.info("48Hz feature hit rate is %s out of 12" % hit_count)

        ##
        # Close the MPO app at the end of the test

        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

        if hit_status is False:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Display refresh rate has not been switched to 48Hz",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Display refresh rate has not been switched to 48Hz")
        else:
            logging.info("Display refresh rate has been switched to 48Hz")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify media playback in MPO mode with display switched to 48Hz (eDP)")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
