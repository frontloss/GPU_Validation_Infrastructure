########################################################################################################################
# @file         mpo_3d_apps.py
# @brief        This test script performs various operations like enabling charms and app switch screen on 3D app.
#               * Start Underrun monitor.
#               * Open 3d app and play it in maximized mode.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Keep app running and try enabling and disabling charms to simulate planes enable/disable.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Close the 3d app.
#               * Stop underrun monitor and check if any underrun was observed during the test execution.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to perform operations like enabling charms and app switch screen on 3D app
class MPO3DApps(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(self.mpo_helper.getStepInfo() + "Applied Display configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))
            winkb_helper.press('WIN+M')

            ##
            # Open Maps app and plays it in maximized mode
            self.mpo_helper.play_3d_app(True)

            ##
            # The opened app will play for 1 minute
            time.sleep(60)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D app in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during 3D App running in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during 3D App running in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D app in CLONE mode")
                for display in range(0, len(self.connected_list)):
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during 3D App running in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during 3D App running in CLONE mode")



            ##
            # When the MPO app is open try enabling and disabling charms to simulate planes enable/disable
            for iteration in range(1, 10):
                winkb_helper.press('WIN+A')
                logging.info(self.mpo_helper.getStepInfo() + "Enabled charms (WIN+A)")
                time.sleep(1)

                ##
                # Verify the plane format for EXTENDED mode
                if topology == enum.EXTENDED:
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D app in EXTENDED mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', 'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during 3D App running in EXTENDED mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during 3D App running in EXTENDED mode")
                    if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Charms in EXTENDED mode")
                        if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2',
                                                  'source_pixel_format_RGB_8888'):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed when Charms enabled  in EXTENDED mode",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed when Charms enabled in EXTENDED mode")
                ##
                # Verify the plane format for CLONE mode
                else:
                    for display in range(0, len(self.connected_list)):
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for 3D app in CLONE mode")
                        if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                                  'source_pixel_format_RGB_8888'):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed during 3D App running  in CLONE mode",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed during 3D App running  in CLONE mode")
                        if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Charms in CLONE mode")
                            if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                                      'source_pixel_format_RGB_8888'):
                                gdhm.report_bug(
                                    title="[MPO][Plane formats]Plane verification failed when Charms enabled in CLONE mode",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail("Plane verification failed when charms enabled in CLONE mode")

                winkb_helper.press('ESC')
                logging.info(self.mpo_helper.getStepInfo() + "Disabled charms")
                time.sleep(1)

            ##
            # Close the 3Dapp
            self.mpo_helper.app3d.close_app()
            logging.info(self.mpo_helper.getStepInfo() + "Closed 3D App")

        else:
            logging.info("Failed to apply display configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                          self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify occurrence of under run during various operations like"
                 "enabling/disabling of charms with media playback application running")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
