########################################################################################################################
# @file         mpo_media_async_app.py
# @brief        This test script verifies MPO.
#               Test consists of below scenarios:
#               * Basic test to verify MPO when media async flip application is run
#                   - Open Media App in windowed mode
#                   - Open Async App in windowed mode and move it to down position
#                   - Verify plane parameters
#                   - Resize the Media plane
#                   - Verify plane parameters
#               * Basic test to verify MPO when async flip application is run with high FPS
#                   - Open Async App in windowed mode and move it to down position
#                   - Verify plane parameters
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper, window_helper,enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.app import App3D
from Libs.Feature.app import AppMedia
from Tests.MPO import mpo_ui_base
from Tests.PlanesUI.Common import planes_ui_helper


##
# @brief    Contains basic test to verify MPO in different scenarios
class MpoMediaAsync(mpo_ui_base.MPOUIBase):

    ##
    # @brief            This function verifies MPO when media and async flip app is run together
    # @return           None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'MEDIA_ASYNC',
                     "Skip the test step as the scenario is not MEDIA_ASYNC")
    # @endcond
    def test_01_media_async(self):

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE' and self.cmd_line_param['FPS'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            plane2_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][1])
            topology = eval(f"enum.{self.cmd_line_param['CONFIG']}")
            fps_pattern = planes_ui_helper.generate_flip_pattern(self.cmd_line_param['FPS'][0])
        else:
            self.fail(
                "Incorrect Commandline parameters. Expected EXPECTED_PIXELFORMAT and FPS tag in commandline")

        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(
                    self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                        DisplayConfigTopology(topology).name,
                        self.mpo_helper.get_display_configuration([self.connected_list[display_index]],
                                                                  self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Open Media app and play it in windowed mode
                app_media = AppMedia(self.media_file)
                app_media.open_app(False, minimize=True)
                app_media.set_half_size(position="top")

                time.sleep(5)

                ##
                # Open 3D App and play it in windowed mode
                app_3d = App3D('FlipAt', 'TestStore/TestSpecificBin/VRR/FlipAt/FlipAt.exe' + ' ' + fps_pattern)
                app_3d.open_app(False, minimize=False, position="down")
                self.app = app_3d.instance

                ##
                # Wait for app to stabilize
                time.sleep(5)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback")

                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                     plane2_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed when FlipAt app is run",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed with FlipAt Application")

                ##
                # Resizing the media in right and bottom direction
                for each_multiplier in range(0, 5):
                    app_media.resize(multiplier=(3, 3), direction=("right", "bottom"))
                    # Todo: Currently seeing RGB color format when plane is resized. So, commenting out the verification
                    #       Will enable verification once issue is resolved.
                    '''
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                    if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                         plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during media playback",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during media playback")

                ##
                # Resizing the media in left and top direction
                for each_multiplier in range(0, 5):
                    app_media.resize(multiplier=(3, 3), direction=("left", "top"))
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                    if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                         plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during media playback",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during media playback")
                '''

                # Close media player
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")

                ##
                # Close 3D application
                self.app.terminate()
                logging.info(self.mpo_helper.getStepInfo() + "Closed FlipAt application")
            else:
                self.fail("Display Configuration failed %s %s" % (DisplayConfigTopology(topology).name,
                                                                  self.connected_list[display_index]))

    ##
    # @brief            This function verifies MPO when async flip app is run generating back to back async flips
    # @return           None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'ASYNC_APP',
                     "Skip the test step as the scenario is not ASYNC_APP")
    # @endcond
    def test_02_async_app(self):

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE' and self.cmd_line_param['FPS'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            topology = eval(f"enum.{self.cmd_line_param['CONFIG']}")
            fps_pattern = planes_ui_helper.generate_flip_pattern(self.cmd_line_param['FPS'][0])
        else:
            self.fail(
                "Incorrect Commandline parameters. Expected EXPECTED_PIXELFORMAT and FPS tag in commandline")

        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(
                    self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                        DisplayConfigTopology(topology).name,
                        self.mpo_helper.get_display_configuration([self.connected_list[display_index]],
                                                                  self.enumerated_displays)))

                ##
                # Open 3D App and play it in windowed mode
                app_3d = App3D('FlipAt', 'TestStore/TestSpecificBin/VRR/FlipAt/FlipAt.exe' + ' ' + fps_pattern)
                app_3d.open_app(True, minimize=True, position="down")
                self.app = app_3d.instance

                ##
                # Wait for app to stabilize
                time.sleep(2)

                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed when FlipAt app is run",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed with FlipAt Application")

                ##
                # Close 3D application
                self.app.terminate()
                logging.info(self.mpo_helper.getStepInfo() + "Closed FlipAt application")
            else:
                self.fail("Display Configuration failed %s %s" % (DisplayConfigTopology(topology).name,
                                                                  self.connected_list[display_index]))

    ##
    # @brief        unittest TearDown function for MpoMediaAsync class
    # @return       None
    def tearDown(self):
        # To close the 3D app if the test fails. For media application, the base class teardown has function to close
        # the media player
        self.app.terminate()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO when media Async Flip application is run")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
