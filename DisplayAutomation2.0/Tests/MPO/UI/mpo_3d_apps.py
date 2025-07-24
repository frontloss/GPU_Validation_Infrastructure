########################################################################################################################
# @file         mpo_3d_apps.py
# @brief        This test script performs various operations like enabling charms and app switch screen on 3D app.
#               * Start Underrun monitor.
#               * Open 3d app and play it in maximized mode.
#               * Verify the plane format.
#               * Keep app running and try enabling and disabling charms to simulate planes enable/disable.
#               * Verify the plane format.
#               * Close the 3d app.
#               * Stop underrun monitor and check if any underrun was observed during the test execution.
# @author       Shrivastava,Shubhangi , Ilamparithi Mahendran , Balasubramanyam,Smitha
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_base


##
# @brief    Contains funtion to performs various operations like enabling charms and app switch screen on 3D app
class MPO3DApps(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        topology = enum.SINGLE

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_RGB_8888"

        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.mpo_helper.get_display_configuration([self.connected_list[display_index]],
                                                              self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Open Maps app and plays it in maximized mode
                self.mpo_helper.play_3d_app(True)

                ##
                # The opened app will play for 1 minute
                time.sleep(60)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane format for 3D App")
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
                else:
                    logging.info("Plane verification passed for 3D App")

                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                logging.info("Watermark verification passed")

                ##
                # When the MPO app is open try enabling and disabling charms to simulate planes enable/disable
                for iteration in range(1, 10):
                    winkb_helper.press('WIN+A')
                    logging.info(self.mpo_helper.getStepInfo() + "Enabled Charms window")
                    time.sleep(1)
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D App")
                    if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                         plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification for 3D App failed",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification for 3D App failed")
                    if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Charms window")
                        if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                             plane1_pixelformat):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification for Charms window failed",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification for Charms window failed")
                    winkb_helper.press('ESC')
                    logging.info(self.mpo_helper.getStepInfo() + "Disabled Charms window")
                    time.sleep(1)

                ##
                # Close the MPO app at the end of the test
                self.mpo_helper.app3d.close_app()
                logging.info(self.mpo_helper.getStepInfo() + "Closed 3D App")

            else:
                logging.info(
                    "Failed to apply display configuration as %s %s" % (DisplayConfigTopology(topology),
                                                                        self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO getting enabled with 3D App running and Charms window enabled")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
