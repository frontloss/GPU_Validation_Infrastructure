########################################################################################################################
# @file         planeformat_media_display_switch_tiled_sst.py
# @brief        Basic test to verify register programming and also check for underrun during basic video playback and
#               display switch scenario on Tiled Display and non tiled display.
#               * Get the DP panel details from the command line and plug tiled display.
#               * Get enumerated display information.
#               * Create a configuration list of various topologies and the displays connected.
#               * Play media content in fullscreen.
#               * Verify plane programming for SINGLE and EXTENDED configuration.
#               * Close the media player.
# @author       Shetty, Anjali N
########################################################################################################################
import itertools
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_tiled_sst_base

##
# @brief    Contains function to check register programming and underrun during basic video playback and display switch scenario
class PlaneFormatMediaDisplaySwitchTiledSST(mpo_ui_tiled_sst_base.MPOUITiledSSTBase):
    display_list = []
    config_list = []

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Expected pixel format
        pixel_format = self.mpo_helper.get_pixel_format_value('YUV420_8BPC')

        ##
        # Get the DP panel details from the command line
        self.sst_base.process_cmdline()

        ##
        # Plug tiled display
        self.sst_base.tiled_display_helper("Plug")

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        ##
        # Get enumerated display info
        enumerated_displays = self.config.get_enumerated_display_info()

        for index in range(enumerated_displays.Count):
            display_info = str(
                CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
            self.display_list.append(display_info)

        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(self.display_list) + 1):
            for subset in itertools.permutations(self.display_list, i):
                for j in range(1, len(topology_list)):
                    self.config_list.append((topology_list[0], [subset[0]]))
                    self.config_list.append((topology_list[j], list(subset)))

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Play media content in fullscreen
        self.mpo_helper.play_media(self.media_file, True)

        ##
        # Enable repeat in the video playback
        winkb_helper.press("CTRL+T")

        time.sleep(30)

        for each_config in range(0, len(self.config_list)):
            if self.config.set_display_configuration_ex(self.config_list[each_config][0],
                                                        self.config_list[each_config][1]) is True:

                #  Delay needed after maximising the app to fix HSD-18023454744,
                #  adding maximise before the existing delay
                self.mpo_helper.app_media.maximise()

                # Todo: Remove as part of VSDI-31758
                time.sleep(5)

                ##
                # Get current display config from DisplayConfig
                current_config = self.config.get_all_display_configuration()

                ##
                # Verify plane programming for SINGLE and EXTENDED configuration
                if self.config_list[each_config][0] == enum.SINGLE or self.config_list[each_config][0] == enum.EXTENDED:
                    for index in range(0, len(self.config_list[each_config][1])):
                        tile_info = self.display_port.get_tiled_display_information(
                            current_config.displayPathInfo[index].targetId)

                        ##
                        # If tiled status is true and index is 0. Primary display is tiled display
                        if tile_info.TiledStatus is True and index == 0:
                            ##
                            # Verify plane programming
                            logging.info("************************Plane verification started************************")
                            if not self.mpo_helper.verify_planes_sst(pixel_format, 'PLANE_CTL_1'):
                                gdhm.report_bug(
                                    title="[MPO]Plane verification failed during fullscreen "
                                          "video playback on Tiled display",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail(
                                    "Plane verification failed during fullscreen video playback on Tiled display")
                            else:
                                logging.info(
                                    "Plane verification passed for fullscreen video playback on Tiled display")
                            logging.info("*************************Plane verification ended*************************")
                        elif index == 0:
                            ##
                            # Verify plane programming
                            logging.info("************************Plane verification started************************")
                            display = self.config_list[each_config][1][0]
                            if not self.mpo_helper.verify_planes(display, 'PLANE_CTL_1', pixel_format):
                                gdhm.report_bug(
                                    title="[MPO]Plane verification failed during fullscreen "
                                          "video playback on non Tiled display",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail(
                                    "Plane verification failed during fullscreen video playback on non Tiled display {}"
                                        .format(display))
                            else:
                                logging.info(
                                    "Plane verification passed for fullscreen video playback on non Tiled display {}"
                                        .format(display))
                            logging.info("*************************Plane verification ended*************************")

            else:
                self.fail("Failed to apply display configuration")

        ##
        # Close the media player
        window_helper.close_media_player()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify for register programming and also check for underrun during basic"
                 "video playback and display switch scenario on Tiled Display and non tiled display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
