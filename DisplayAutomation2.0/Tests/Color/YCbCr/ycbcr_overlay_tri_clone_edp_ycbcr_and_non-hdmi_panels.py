###############################################################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_overlay_tri_clone_edp_ycbcr_and_non-hdmi_panels
# \remarks
# \ref ycbcr_overlay_tri_clone_edp_ycbcr_and_non-hdmi_panels.py \n
# This script performs color functionality such as enable/disable YCbCr on the supported panel
# when the overlay application is playing in Clone configuration. It applies particular mode on HDMI panel.
# It also checks whether the output colorspace is YUV when YCbCr is enabled and RGB when YCbCr is disabled
#
# CommandLine: python ycbcr_overlay_tri_clone_edp_ycbcr_and_non-hdmi_panels.py -hdmi_b HDMI_Dell_U2709_YCBCR.EDID -dp_c -edp_a
#
# \author Anjali Shetty
###############################################################################################################################
import subprocess

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_base import *
from Tests.Color.color_common_utility import gdhm_report_app_color
from Tests.Color.color_verification import *


class YCbCrOverlayTriCloneEDPYCbCrAndNonHDMIPanels(ColorBase):
    display = 0

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

        ##
        # Get Video Sprite Status
        logging.info(self.getStepInfo() + "Verifying video sprite status for display %s" % self.display)
        video_sprite_status = get_video_sprite_status(self.display, 'PLANE_CTL_2', 'PLANE_COLOR_CTL_1')
        if not video_sprite_status:
            self.fail("Failed to get video sprite status")

    def runTest(self):
        ycbcr_supported = 0

        ##
        # Get the target id of the display
        logging.info(self.getStepInfo() + "Checking for YCbCr support in connected panels: %s " % self.connected_list)
        for display_index in range(len(self.connected_list)):
            self.target_id = self.config.get_target_id(self.connected_list[display_index], self.enumerated_displays)

            ##
            # Check if YCbCr is supported
            ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)
            if ycbcr_supported:
                self.display = self.connected_list[display_index]
                logging.info("YCbCr is supported on panel %s" % self.display)
                break

        if ycbcr_supported:
            ##
            # Set topology to CLONE display configuration
            topology = enum.CLONE

            ##
            # Apply CLONE display configuration across all the displays
            if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
                logging.info(self.getStepInfo() + "Applied Display configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.get_display_configuration(self.connected_list)))

                ##
                # Open the overlay application
                logging.info(self.getStepInfo() + "Launching overlay(dx9_overlay) application")
                self.app = subprocess.Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
                if not self.app:
                    gdhm_report_app_color(title="[COLOR]Failed to launch dx9_overlay App", component=gdhm.Component.Test.DISPLAY_OS_FEATURES, problem_classification = gdhm.ProblemClassification.OTHER)
                    self.fail("Failed to launch overlay application")
                else:
                    logging.info("Successfully launched overlay application")
                time.sleep(5)

                native_mode = self.config.get_native_mode(self.target_id)
                if native_mode is None:
                    self.fail(f"Failed to get native mode for {self.target_id}")
                HzRes = native_mode.hActive
                VtRes = native_mode.vActive
                rr = native_mode.refreshRate
                ##
                # Apply particular mode on HDMI
                supported_modes = self.config.get_all_supported_modes([self.target_id])
                result = False
                for key, values in supported_modes.items():
                    for mode in values:
                        if mode.HzRes == HzRes and mode.VtRes == VtRes and mode.refreshRate == rr and mode.scaling == enum.MDS:
                            result = self.config.set_display_mode([mode])
                            break

                if result:
                    current_mode = self.config.get_current_mode(self.target_id)
                    logging.info("Mode is %sX%s@%s with scaling : %s" % (
                        current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
                else:
                    logging.error("Failed to apply the required mode")
                    self.fail("Failed to apply the required mode")

                ##
                # Get the output colorspace
                logging.info(self.getStepInfo() + "Verifying output color space for panel %s" % self.display)
                colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC', 'RGB')
                if colorspace_status != "RGB":
                    self.fail("Pipe output color space mismatch for display: %s" % self.display)

                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Enabling YCbCr on panel %s" % self.display)
                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                if not self.ycbcr_enable_status:
                    self.fail("Failed to enable YCbCr")
                else:
                    logging.info("Successfully enabled YCbCr")
                    ##
                    # Verify the registers
                    self.verify_registers()

                    ##
                    # Disables YCbCr
                    logging.info(self.getStepInfo() + "Disabling YCbCr on panel %s" % self.display)
                    disable_status = driver_escape.configure_ycbcr(self.target_id, False)
                    if not disable_status:
                        self.fail("Failed to disable YCbCr")
                    else:
                        logging.info("Successfully disabled YCbCr")

                ##
                # Close the overlay application
                self.app.terminate()
                logging.info(self.getStepInfo() + "Closed overlay application")
            else:
                self.fail("Failed to apply Display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                              self.connected_list))
        else:
            self.fail("None of the panels connected support yCbCr")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables YCbCr on supported panels with overlay application running in clone configuration. Checks for YUV output "
        "color space when YCbCr is enabled and RGB when YCbCr is disabled")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
