########################################################################################################################
#########################################
# @file         mpo_ma_planeformat_media.py
# @brief        This test script verifies enabling of MPO during media playback across multiple adapters
#               * Open Media app and play it in maximized mode
#               * Verify the plane programming
#               * Close Media app
#               * Open Media app and play it in windowed mode
#               * Verify the plane programming
#               * Close Media app
# @author       Sunaina Ashok
########################################################################################################################
#########################################

import logging
import time
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Libs.Core import enum, winkb_helper, window_helper, cmd_parser
from Tests.MPO import mpo_ma_ui_base
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE

##
# @brief    Contains functions that performs media controls and verify plane
class MPOPlaneFormatMedia(mpo_ma_ui_base.MPOMAUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        display_list = []
        gfx_list = []
        connected_list = []
        display_adapter_list = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        connected_list.append(
                            (value['connector_port'], value['gfx_index']))
                if key == 'EXPECTED_PIXELFORMAT':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            pixel_format = self.mpo_helper.get_pixel_format_value(value[i])
                    else:
                        for i in range(0, len(self.display_details)):
                            pixel_format = self.mpo_helper.get_pixel_format_value(value[0])

                if key == 'CONFIG':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            topology = eval("enum.%s" %(value[i]))
                    else:
                        for i in range(0, len(self.display_details)):
                            topology = eval("enum.%s" % (value))
        pixel_format2 = self.mpo_helper.get_pixel_format_value('RGB8888')

        ##
        # Get enumerated display details.
        enumerated_displays = self.display_config.get_enumerated_display_info()

        ##
        # Get current display configuration.
        config, connector_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        ##
        # Apply display configuration across adapters.
        if self.display_config.set_display_configuration_ex(topology, display_and_adapter_info_list) is False:
            self.fail('Step %s Failed to apply display configuration %s %s' %
                      (self.mpo_helper.getStepInfo(), DisplayConfigTopology(topology).name, connector_port))
        else:
            logging.info('Step %s Successfully applied the display configuration as %s %s' %
                         (self.mpo_helper.getStepInfo(), DisplayConfigTopology(topology).name, connector_port))

        winkb_helper.press('WIN+M')

        ##
        # Open Media app and plays it in maximized mode
        self.mpo_helper.play_media(self.media_file, True)

        ##
        # To enable 'Repeat' option in the Video App
        winkb_helper.press("CTRL+T")

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        for index in range(enumerated_displays.Count):
            display_info = ("%s" % (CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))
            gfx_index = enumerated_displays.ConnectedDisplays[
                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            display_adapter_list.append((display_info, gfx_index))

        for each_display in display_adapter_list:
            display_list.append(each_display[0])
            gfx_list.append(each_display[1])

        if topology == enum.CLONE:
            for i in range(0, len(display_list)):
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane format for media playback application in full screen mode")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_1', gfx_list[i].lower()):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback application",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback application")
                else:
                    logging.info("Plane verification passed for media playback application")
                ##
                # Watermark verification
                if self.wm.verify_watermarks(gfx_index=gfx_list[i].lower()) is not True:
                    self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[i].lower()))
                logging.info("Watermark verification passed")
        else:
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_1', pixel_format, gfx_list[0].lower()):
                gdhm.report_bug(
                    title="[MPO][Plane formats]Plane verification failed during media playback application",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed during media playback application in full screen mode")
            else:
                logging.info("Plane verification passed for media playback application App in full screen mode")

            ##
            # Watermark verification
            if self.wm.verify_watermarks(gfx_index=gfx_list[0].lower()) is not True:
                self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[0].lower()))
            logging.info("Watermark verification passed")

        ##
        # Close the media app
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")

        ##
        # Opens media app and plays it in windowed screen mode
        self.mpo_helper.play_media(self.media_file, False)

        ##
        # To enable 'Repeat' option in the Video App
        winkb_helper.press("CTRL+T")

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        if topology == enum.CLONE:
            for i in range(0, len(display_list)):
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane format for media playback application in windowed mode")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_1', gfx_list[i].lower()):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback application",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback application in windowed mode")
                else:
                    logging.info("Plane verification passed for media playback application in windowed mode")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_2',
                                                     gfx_list[i].lower()):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed for Desktop window",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop window")
                else:
                    logging.info("Plane verification passed for Desktop window")

                if self.wm.verify_watermarks(gfx_index=gfx_list[i].lower()) is not True:
                    self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[i].lower()))
                logging.info("Watermark verification passed")
        else:
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_1', pixel_format, gfx_list[0].lower()):
                gdhm.report_bug(
                    title="[MPO][Plane formats]Plane verification failed during media playback application",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed during media playback application in windowed mode")
            else:
                logging.info("Plane verification passed for media playback application in windowed mode")

            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_2', pixel_format2, gfx_list[0].lower()):
                gdhm.report_bug(
                    title="[MPO][Plane formats]Plane verification failed for Desktop window",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed for Desktop window")
            else:
                logging.info("Plane verification passed for Desktop window")

                ##
                # Watermark verification
            if self.wm.verify_watermarks(gfx_index=gfx_list[0].lower()) is not True:
                self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[0].lower()))
            logging.info("Watermark verification passed")

        ##
        # Close the media app
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose:Test to verify enabling of MPO during media playback across multiple adapters")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)