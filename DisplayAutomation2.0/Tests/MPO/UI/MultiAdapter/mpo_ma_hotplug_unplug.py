########################################################################################################################
# @file         mpo_ma_hotplug_unplug.py
# @brief        Basic test to verify enabling of MPO when 3D App is running with hotplug and unplug of displays.
#               * Run the 3D Application in Windowed mode.
#               * Unplug all the displays.(except DP_A)
#               * Parse the command line and plug all the displays
#               * Verify plane programming.
#               * Close the 3D App.
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, display_utility
from Libs.Core import winkb_helper, enum
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ma_ui_base
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE


##
# @brief            To plug multiple displays
# @param[in]        display_details; List of tuples containing (connector_port, gfx_index, edid_name, dpcd_name)
# @return           False if plugging of display is failed
def plug_require_display(display_details):
    if 'DP' in display_details[0]:
        if display_details[2] is None:
            dp_edid = 'DP_3011.EDID'
            dp_dpcd = 'DP_3011_dpcd.txt'
        else:
            dp_edid = display_details[2]
            dp_dpcd = display_details[3]
        if display_utility.plug(port=display_details[0], edid=dp_edid, dpcd=dp_dpcd,
                                gfx_index=display_details[1].lower()) is False:
            return False

    elif 'HDMI' in display_details[0]:
        if display_details[2] is None:
            hdmi_edid = 'HDMI_Dell_3011.EDID'
        else:
            hdmi_edid = display_details[2]
        if display_utility.plug(port=display_details[0], edid=hdmi_edid,
                                gfx_index=display_details[1].lower()) is False:
            return False


##
# @brief Contains function to check enabling of MPO when 3D App is running with hotplug and unplug of displays
class HotPlugUnplug(mpo_ma_ui_base.MPOMAUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        connected_list = []
        display_list = []
        gfx_list = []
        display_adapter_list = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        connected_list.append(
                            (value['connector_port'], value['gfx_index'], value['edid_name'], value['dpcd_name']))

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

        winkb_helper.press('WIN+M')

        ##
        # play 3D application in windowed mode
        self.mpo_helper.play_3d_app(False)

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        ##
        # unplug of displays
        for key, value in self.display_details.items():
            for display in value:
                if display != 'DP_A':
                    logging.info("Trying to unplug %s", display)
                    display_utility.unplug(display, gfx_index=key.lower())

        ##
        # plugging multiple displays
        for each_display in connected_list:
            if each_display[0] != 'DP_A':
                plug_require_display(each_display)

        display_config = disp_cfg.DisplayConfiguration()

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

        for index in range(enumerated_displays.Count):
            display_info = ("%s" % (CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))
            gfx_index = enumerated_displays.ConnectedDisplays[
                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            display_adapter_list.append((display_info, gfx_index))

        for each_display in display_adapter_list:
            display_list.append(each_display[0])
            gfx_list.append(each_display[1])

        ##
        # Checking whether eDP is present in the Display List and fetching the index of the eDP
        edp_connected = False
        edp_index = 0
        for i in range(0, len(display_list)):
            if display_list[i] == 'DP_A':
                edp_connected = True
                edp_index = i
                break

        ##
        # Make sure DP_A is present in the Display List or else report bug
        if not edp_connected:
            gdhm.report_bug(title="[MPO][Planes MultiAdapter]DP_A not found", problem_classification=gdhm.ProblemClassification.FUNCTIONALITY, component=gdhm.Component.Driver.DISPLAY_OS_FEATURES, priority=gdhm.Priority.P3, exposure=gdhm.Exposure.E3)
            self.fail("DP_A is expected for the test to verify planes")

        if topology == enum.CLONE:
            for i in range(0, len(display_list)):
                logging.info(self.mpo_helper.getStepInfo() + f"Verifying plane format for 3D App in CLONE mode")
                if not self.mpo_helper.verify_plane_status(display_list[i], 'PLANE_CTL_1',
                                                           gfx_list[i].lower()):
                    self.mpo_helper.report_to_gdhm_verifcation_failure("3D App", topology, False)
                    self.mpo_helper.fail_statement("3D_App", topology, False)
                else:
                    logging.info("Plane verification passed for 3D App in windowed mode with CLONE config ")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
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
            logging.info(self.mpo_helper.getStepInfo() + f"Verifying plane format for 3D App in EXTENDED mode")
            logging.info(f"Display List: {display_list}")
            if not self.mpo_helper.verify_planes(display_list[edp_index], 'PLANE_CTL_1', pixel_format,
                                                 gfx_list[edp_index].lower(), 'D3D12', self):
                self.mpo_helper.report_to_gdhm_verifcation_failure("3D App", topology, False)
                self.mpo_helper.fail_statement("3D_App", topology, False)
            else:
                logging.info("Plane verification passed for 3D App in windowed mode with EXTENDED config")

            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
            if not self.mpo_helper.verify_planes(display_list[0], 'PLANE_CTL_2', pixel_format2, gfx_list[0].lower(),
                                                 'D3D12', self):
                self.mpo_helper.report_to_gdhm_verifcation_failure("Desktop", topology, False)
                self.mpo_helper.fail_statement("Desktop", topology, False)
            else:
                logging.info("Plane verification passed for Desktop window in windowed mode with EXTENDED config")

            ##
            # Watermark verification after playing 3D App in windowed mode
            if self.wm.verify_watermarks(gfx_index=gfx_list[0].lower()) is not True:
                self.fail("Error Observed in watermark verification on Adapter: {}".format(gfx_list[0].lower()))
            logging.info("Watermark verification passed")

        ##
        # Close the MPO app
        self.mpo_helper.app3d.close_app()
        logging.info(self.mpo_helper.getStepInfo() + "Closed Media App")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Verifies enabling of MPO when 3D App is running with hotplug and unplug of displays")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
