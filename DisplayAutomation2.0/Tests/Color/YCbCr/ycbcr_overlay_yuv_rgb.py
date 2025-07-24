##############################################################################################
# @file     ycbcr_overlay_yuv_rgb.py
# @brief    This script performs color functionality such as enable/disable YCbCr on the supported panel
#           when the overlay application is playing. It checks for the output colorspace is YUV when
#           YCbCr is enabled and  RGB when YCbCr is disabled. It also applies different resolutions and
#           checks for the output colorspace. It plays the overlay application in full screen and
#           windowed mode.
#           CommandLine: python ycbcr_overlay_yuv_rgb.py -hdmi_b HDMI_Dell_U2709_YCBCR.EDID
# @author Smitha B
###############################################################################################

import subprocess

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.winkb_helper import press
from Tests.Color.color_base import *
from Tests.Color.color_common_utility import gdhm_report_app_color
from Tests.Color.color_verification import *


class YCbCrOverlayYUVRGB(ColorBase):

    def verify_registers(self):
        ##
        # Get the output colorspace
        logging.info(self.getStepInfo() + "Verifying output color space for display %s" % self.display)
        colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC', 'YUV')
        if colorspace_status != "YUV":
            self.fail("Pipe output color space mismatch for display: %s" % self.display)

        ##
        # Get the cursor status
        cursor_status = get_cursor_status(self.display, 'CUR_CTL')

    def runTest(self):

        ##
        # Get the target id of the display
        logging.info(self.getStepInfo() + "Checking for YCbCr support in connected panels: %s " % self.connected_list)
        for display_index in range(len(self.connected_list)):
            self.target_id = self.config.get_target_id(self.connected_list[display_index], self.enumerated_displays)

            ##
            # Check if YCbCr is supported
            self.ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)

            if self.ycbcr_supported:
                self.display = self.connected_list[display_index]
                logging.info("YCbCr is supported on panel %s" % self.display)
                break

        if self.ycbcr_supported:
            ##
            # set topology to SINGLE display configuration
            topology = enum.SINGLE

            ##
            # Apply SINGLE display configuration
            if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
                logging.info(self.getStepInfo() + "Applied Display configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.get_display_configuration(self.connected_list)))

                ##
                # Open the overlay application
                logging.info(self.getStepInfo() + "Launching overlay application(dx9_overlay)")
                self.app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
                if not self.app:
                    gdhm_report_app_color(title="[COLOR]Failed to launch dx9_overlay App",
                                          component=gdhm.Component.Test.DISPLAY_OS_FEATURES, problem_classification = gdhm.ProblemClassification.OTHER)
                    self.fail("failed to launch overlay app")
                else:
                    logging.info("Launched overlay app")
                time.sleep(5)

                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Enabling YCbCr on panel %s" % self.display)
                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                if not self.ycbcr_enable_status:
                    self.fail("Failed to enable YCbCr")
                else:
                    logging.info("Successfully enabled YCbCr")
                    ##
                    # Verify the Registers
                    self.verify_registers()

                    ##
                    # Get Video Sprite Status
                    video_sprite_status = get_video_sprite_status(self.display, 'PLANE_CTL_2', 'PLANE_COLOR_CTL_1')
                    if not video_sprite_status:
                        self.fail("Failed to get video sprite status")

                ##
                # Close the overlay application
                self.app.terminate()
                logging.info(self.getStepInfo() + "Closed overlay application")

                time.sleep(2)

                ##
                # Open the overlay application
                logging.info(self.getStepInfo() + "Launching overlay(dx9_overlay) application")
                self.app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
                if not self.app:
                    gdhm_report_app_color(title="[COLOR]Failed to launch dx9_overlay App",
                                          component=gdhm.Component.Test.DISPLAY_OS_FEATURES, problem_classification = gdhm.ProblemClassification.OTHER)
                    self.fail("Failed to launch overlay application")
                else:
                    logging.info("Successfully launched overlay application")
                time.sleep(5)

                ##
                # Verify the Registers
                self.verify_registers()

                self.app.terminate()
                logging.info(self.getStepInfo() + "Closed overlay application")

                ##
                # Get all the supported modes and change the color depth to 16BPP
                supported_modes = self.config.get_all_supported_modes([self.target_id])

                for key, values in supported_modes.items():
                    for mode in values:
                        ##
                        # Set all the supported modes
                        logging.info(
                            self.getStepInfo() + "Applying display mode: %s" % mode.to_string(self.enumerated_displays))
                        self.config.set_display_mode([mode])

                        ##
                        # Verify the Registers
                        self.verify_registers()
                        break

                ##
                # Invoke s3 state
                logging.info(self.getStepInfo() + "Invoking POWER_STATE_S3 event")
                if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60):
                    logging.info("Power Event POWER_STATE_S3: Success")
                else:
                    logging.error("Power Event POWER_STATE_S3: Failed")

                time.sleep(2)

                ##
                # Open the overlay application
                logging.info(self.getStepInfo() + "Launching overlay(dx9_overlay) application")
                self.app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
                if not self.app:
                    gdhm_report_app_color(title="[COLOR]Failed to launch PresentTester App",  component=gdhm.Component.Test.DISPLAY_OS_FEATURES,problem_classification = gdhm.ProblemClassification.OTHER)
                    self.fail("Failed to launch overlay application")
                else:
                    logging.info("Successfully launched overlay application")
                time.sleep(5)

                ##
                # Verify the Registers
                self.verify_registers()

                ##
                # Go to full screen and windowed mode multiple times
                fullscreen = True
                for i in range(10):

                    press('F2')
                    if fullscreen:
                        mode = "full screen"
                    else:
                        mode = "windowed"
                    fullscreen = not fullscreen

                    logging.info(self.getStepInfo() + "Changed mode of overlay application to %s " % mode)
                    time.sleep(1)
                    ##
                    # Verify the Registers
                    self.verify_registers()

                ##
                # Close the overlay application
                self.app.terminate()
                logging.info(self.getStepInfo() + "Closed overlay application")

                ##
                # Disables YCbCr
                logging.info(self.getStepInfo() + "Disabling YCbCr on panel %s" % self.display)
                disable_status = driver_escape.configure_ycbcr(self.target_id, False)
                if not disable_status:
                    self.fail("Failed to disable YCbCr")
                else:
                    logging.info("Successfully disabled YCbCr")

        else:
            self.fail("None of the panels connected support yCbCr")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables YCbCr on supported panels with overlay application running in fullscreen / windowed mode. Checks for YUV output "
        "color space when YCbCr is enabled and RGB when YCbCr is disabled with different resolutions and power events applied")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
