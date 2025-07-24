########################################################################################################################
# @file         mpo_rotation.py
# @brief        Basic test to verify hardware rotation and plane format getting enabled with no corruption on 3Dapp
#               with rotation
#               * Fetch the display configuration of all the displays connected.
#               * Play the Metro 3D app in Metro Mode.
#               * Verify the plane format for SINGLE display configuration.
#               * rotate the display to 180, 270 and 0 degrees while the Video app is open.
#               * Close the App.
# @author       Balasubramnayam, Smitha
########################################################################################################################
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
# @brief    Contains function to check hardware rotation and plane format getting enabled with no corruption on 3Dapp
class MPORotation(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_RGB_8888"

        target_id_list = []
        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        ##
        # Apply SINGLE display configuration across all the displays
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info("Applied the configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                  self.mpo_helper.get_display_configuration(
                                                                      [self.connected_list[display_index]], self.enumerated_displays)))
                ##
                # Open the Metro 3D App in metro mode  :
                self.mpo_helper.play_3d_app(True)
                time.sleep(6)
                ##
                # fetch all the modes supported by each of the displays connected
                supported_modes = self.config.get_all_supported_modes(target_id_list)
                for key, values in supported_modes.items():
                    for mode in values:
                        ##
                        # rotate the display to 90 degrees while the 3D app is open
                        mode.rotation = enum.ROTATE_90
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Applying Display mode with rotation set to 90: mode %s" % (
                            mode.to_string(self.enumerated_displays)))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        ##
                        # rotate the display to 180 degrees while the 3D app is open
                        mode.rotation = enum.ROTATE_180
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Applying Display mode with rotation set to 180: mode %s" % (
                            mode.to_string(self.enumerated_displays)))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        ##
                        # rotate the display to 270 degrees while the 3D app is open
                        mode.rotation = enum.ROTATE_270
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Applying Display mode with rotation set to 270: mode %s" % (
                            mode.to_string(self.enumerated_displays)))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        ##
                        # rotate the display to 0 degrees while the 3D app is open
                        mode.rotation = enum.ROTATE_0
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Applying Display mode with rotation set to 0: mode %s" % (
                            mode.to_string(self.enumerated_displays)))
                        ##
                        # Verify the plane format
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App")
                        if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                  plane1_pixelformat):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed during 3D App",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed during 3D App")

                ##
                # Close the 3Dapp
                self.mpo_helper.app3d.close_app()
                logging.info(self.mpo_helper.getStepInfo() + "Closed 3D Application")

            else:
                self.fail(
                    "Failed to apply display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                        self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to  verify MPO getting enabled during Display rotation with 3D App running")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
