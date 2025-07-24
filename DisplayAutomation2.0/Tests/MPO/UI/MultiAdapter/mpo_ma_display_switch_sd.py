########################################################################################################################
# @file         mpo_ma_display_switch_sd.py
# @brief        Basic test to verify plane format getting enabled on video app during display switch.
#               * Create a configuration list of various topologies and the displays connected.
#               * Play 3D app in Metro mode.
#               * Apply each configuration across the displays connected.
#               * Verify plane programming.
#               * Close the 3D App.
# @author       Pai, Vinayak1
########################################################################################################################
import itertools
import logging
import sys
import time
import unittest

from Libs.Core import enum, cmd_parser
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ma_ui_base


##
# @brief    Contains function to check plane format getting enabled on video app during display switch
class MPODisplaySwitchSD(mpo_ma_ui_base.MPOMAUIBase):
    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        config_list = []
        display_list = []
        gfx_list = []
        final_display_list = []
        final_gfx_list = []
        topo_list = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if key == 'EXPECTED_PIXELFORMAT':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            pixel_format = self.mpo_helper.get_pixel_format_value(value[i])
                    else:
                        for i in range(0, len(self.display_details)):
                            pixel_format = self.mpo_helper.get_pixel_format_value(value[0])

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        disp_list = self.display_details.items()

        #
        # Get enumerated display details.
        enumerated_displays = self.display_config.get_enumerated_display_info()

        ##
        # Get current display configuration.
        config, connector_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(disp_list) + 1):
            for subset in itertools.permutations(disp_list, i):
                for j in range(1, len(topology_list)):
                    config_list.append((topology_list[0], [subset[0]]))
                    config_list.append((topology_list[j], list(subset)))

        ##
        # To create a separate list of Displays and Graphics adapter from the config_list
        # ex: final_display list = [['DP_A', 'HDMI_B'],[DP_A]]
        #     final_gfx_list = [[GFX_0], [GFX_1]]
        for key, value in config_list:
            gfx_temp_list = []
            display_temp_list = []
            topo_list.append(key)
            for a_tuple in value:
                gfx_temp_list.append(a_tuple[0])
                display_temp_list.append(a_tuple[1])
            display_list.append(display_temp_list)
            gfx_list.append(gfx_temp_list)

        for i in display_list:
            final_display_list.append(self.mpo_helper.remove_nested_list(i))
        for i in gfx_list:
            final_gfx_list.append(self.mpo_helper.remove_nested_list(i))

        ##
        # Play the 3Dapp in Metro Mode
        self.mpo_helper.play_3d_app(True)
        time.sleep(2)

        ##
        # applying each configuration across the displays connect
        for i in range(0, len(final_display_list)):
            for j in range(0, len(final_gfx_list[i])):
                if self.display_config.set_display_configuration_ex(topo_list[i], final_display_list[i]) is True:
                    logging.info(self.mpo_helper.getStepInfo() + "Applied display configuration: %s"
                                 % self.mpo_helper.get_display_configuration([final_display_list[i][j]],
                                                                             enumerated_displays,
                                                                             self.mpo_helper.list_to_str(
                                                                                 final_gfx_list[i][j]).lower()))

                    #  Delay needed after maximising the app to fix HSD-18023454744,
                    #  adding maximise before the existing delay
                    self.mpo_helper.app3d.maximise()
                    time.sleep(6)

                    if topo_list[i] == enum.SINGLE:
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App in SINGLE mode")
                        if not self.mpo_helper.verify_planes(self.mpo_helper.list_to_str([final_display_list[i][j]]),
                                                             'PLANE_CTL_1',
                                                             pixel_format,
                                                             self.mpo_helper.list_to_str(final_gfx_list[i][j]).lower()):
                            self.mpo_helper.report_to_gdhm_verifcation_failure("3D App", topo_list[i], True)
                            self.mpo_helper.fail_statement("3D App", topo_list[i], True)
                        else:
                            logging.info(
                                "Plane verification passed for 3D App in fullscreen mode with SINGLE config")

                        time.sleep(10)

                        ##
                        # verify watermark
                        if self.wm.verify_watermarks(
                                gfx_index=self.mpo_helper.list_to_str(final_gfx_list[i][j]).lower()) is not True:
                            self.fail("Error Observed in watermark verification")
                        logging.info("Watermark verification passed")

                    if topo_list[i] == enum.EXTENDED:
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App in EXTENDED mode")
                        if not self.mpo_helper.verify_planes(self.mpo_helper.list_to_str([final_display_list[i][0]]),
                                                             'PLANE_CTL_1',
                                                             pixel_format,
                                                             self.mpo_helper.list_to_str(final_gfx_list[i][0]).lower()):
                            self.mpo_helper.report_to_gdhm_verifcation_failure("3D App", topo_list[i], True)
                            self.mpo_helper.fail_statement("3D App", topo_list[i], True)
                        else:
                            logging.info(
                                "Plane verification passed for 3D App in fullscreen mode with EXTENDED config")

                        ##
                        # verify watermark
                        if self.wm.verify_watermarks(
                                gfx_index=self.mpo_helper.list_to_str(final_gfx_list[i][0]).lower()) is not True:
                            self.fail("Error Observed in watermark verification")
                        logging.info("Watermark verification passed")

                    if topo_list[i] == enum.CLONE:
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App in CLONE mode")
                        if not self.mpo_helper.verify_planes(self.mpo_helper.list_to_str([final_display_list[i][j]]),
                                                             'PLANE_CTL_1',
                                                             pixel_format,
                                                             self.mpo_helper.list_to_str(final_gfx_list[i][j]).lower()):
                            self.mpo_helper.report_to_gdhm_verifcation_failure("3D App", topo_list[i], True)
                            self.mpo_helper.fail_statement("3D App", topo_list[i], True)
                        else:
                            logging.info(
                                "Plane verification passed for 3D App in fullscreen mode with CLONE config")

                        time.sleep(10)

                        ##
                        # verify watermark
                        if self.wm.verify_watermarks(
                                gfx_index=self.mpo_helper.list_to_str(final_gfx_list[i][j]).lower()) is not True:
                            self.fail("Error Observed in watermark verification")
                        logging.info("Watermark verification passed")

                else:
                    logging.info("Failed to apply display configuration %s %s" % (
                        DisplayConfigTopology(topo_list[i]).name, display_list))
        ##
        # Close the 3Dapp
        self.mpo_helper.app3d.close_app()
        logging.info(self.mpo_helper.getStepInfo() + "Closed 3D App")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify enabling of MPO with 3D App and change in display mode")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
