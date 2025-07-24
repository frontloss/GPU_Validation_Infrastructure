########################################################################################################################
# @file         mpo_ma_snapmode_media.py
# @brief        Basic test to verify plane format getting enabled on video app during mode change across all the displays
#               connected.
#               * Fetch the display configuration of all the displays connected.
#               * Apply SINGLE display configuration across all the displays.
#               * Fetch all the modes supported by each of the displays connected.
#               * Close the Video App.
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper, cmd_parser
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ma_ui_base
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE


##
# @brief    Contains function to check plane format getting enabled on video app during mode change
class PlaneFormatResolutionSwitchSnapmode(mpo_ma_ui_base.MPOMAUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        connected_list = []
        display_list = []
        gfx_list = []
        target_id_list = []
        display_adapter_list = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        connected_list.append((value['connector_port'], value['gfx_index']))
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
                            topology = eval("enum.%s" % (value[i]))
                    else:
                        for i in range(0, len(self.display_details)):
                            topology = eval("enum.%s" % (value))
        pixel_format2 = self.mpo_helper.get_pixel_format_value('RGB8888')

        ##
        # Get enumerated display details.
        enumerated_displays = self.display_config.get_enumerated_display_info()

        display_info = self.display_config.get_all_display_configuration()

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
        # play media file in windowed mode
        self.mpo_helper.play_media(self.media_file, False)

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
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane format for Media in CLONE mode")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_1',
                                                               gfx_list[i].lower()):
                    self.mpo_helper.report_to_gdhm_verifcation_failure("Media", topology, False)
                    self.mpo_helper.fail_statement("Media", topology, False)
                else:
                    logging.info(f"Plane verification passed for media App in windowed mode with CLONE config")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in CLONE mode")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_2',
                                                               gfx_list[i].lower()):
                    self.mpo_helper.report_to_gdhm_verifcation_failure("Desktop", topology, False)
                    self.mpo_helper.fail_statement("Desktop", topology, False)
                else:
                    logging.info("Plane verification passed for Desktop window in windowed mode with CLONE config")

                if self.wm.verify_watermarks(gfx_index=gfx_list[i].lower()) is not True:
                    self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[i].lower()))
                logging.info("Watermark verification passed")

        else:
            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane format for Media in EXTENDED mode")
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_1', pixel_format,
                                                gfx_list[0].lower()):
                self.mpo_helper.report_to_gdhm_verifcation_failure("Media", topology, False)
                self.mpo_helper.fail_statement("Media", topology, False)
            else:
                logging.info(f"Plane verification passed for media App in windowed mode with EXTENDED config")

            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in EXTENDED mode")
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_2', pixel_format2,
                                                  gfx_list[0].lower()):
                self.mpo_helper.report_to_gdhm_verifcation_failure("Media", topology, False)
                self.mpo_helper.fail_statement("Media", topology, False)
            else:
                logging.info("Plane verification passed for Desktop window in windowed mode with EXTENDED config")

            ##
            # Watermark verification after playing 3D App in windowed mode
            if self.wm.verify_watermarks(gfx_index=gfx_list[0].lower()) is not True:
                self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[0].lower()))
            logging.info("Watermark verification passed")

            winkb_helper.press("CTRL+T")

        # logging.info("Enabled repeat option on media playback application")
        winkb_helper.snap_left()
        logging.info(self.mpo_helper.getStepInfo() + "Enabled left snap mode")

        time.sleep(5)

        ##
        # Close the Video App
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO is getting enabled on video playback in snap mode with mode change"
                 "across all the connected display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
