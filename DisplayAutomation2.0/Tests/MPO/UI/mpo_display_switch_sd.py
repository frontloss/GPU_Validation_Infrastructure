########################################################################################################################
# @file         mpo_display_switch_sd.py
# @brief        Basic test to verify plane format getting enabled with no corruption on video app during display switch.
#               * Create a configuration list of various topologies and the displays connected.
#               * Play 3D app in Metro mode.
#               * Apply each configuration across the displays connected.
#               * Close the Video App.
#               * Verify the plane format.
# @author       Shetty, Anjali N
########################################################################################################################
import itertools
import logging
import sys
import time
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check plane format getting enabled with no corruption on video app during display switch
class MPODisplaySwitchSD(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        disp_list = []
        config_list = []

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_RGB_8888"

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        ##
        #
        for disp in range(len(self.connected_list)):
            disp_list.append(self.connected_list[disp])
        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(disp_list) + 1):
            for subset in itertools.permutations(disp_list, i):
                for j in range(1, len(topology_list)):
                    config_list.append((topology_list[0], [subset[0]]))
                    config_list.append((topology_list[j], list(subset)))

        ##
        # Play the 3Dapp in Metro Mode
        self.mpo_helper.play_3d_app(True)
        time.sleep(2)

        ##
        # applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:

                #  Delay needed after maximising the app to fix HSD-18023454744,
                #  adding maximise before the existing delay
                self.mpo_helper.app3d.maximise()

                # Todo: Remove as part of VSDI-31758
                time.sleep(6)


                logging.info(self.mpo_helper.getStepInfo() + "Applied display configuration: %s" % self.mpo_helper.get_display_configuration(
                    config_list[each_config][1], self.enumerated_displays))
                if config_list[each_config][0] == enum.SINGLE:
                    ##
                    # Verify the plane format
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App")
                    if not self.mpo_helper.verify_planes(config_list[each_config][1][0], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed with 3D App running",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed with 3D App running")



                    if self.wm.verify_watermarks() is not True:
                        self.fail("Error Observed in watermark verification")
                    logging.info("Watermark verification passed")

            else:
                logging.info("Failed to apply display configuration %s %s" % (
                    DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]))

        ##
        # Close the 3Dapp
        self.mpo_helper.app3d.close_app()
        logging.info(self.mpo_helper.getStepInfo() + "Closed 3D App")

        # to-do : implement tablet mode


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify enabling of MPO with 3D App and change in display mode")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
