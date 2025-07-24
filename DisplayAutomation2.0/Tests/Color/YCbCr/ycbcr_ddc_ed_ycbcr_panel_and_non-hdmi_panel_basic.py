##############################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_ddc_ed_ycbcr_panel_and_non-hdmi_panel_basic
# \remarks
# \ref ycbcr_ddc_ed_ycbcr_panel_and_non-hdmi_panel_basic.py \n
# This script performs color functionality such as enable/disable YCbCr on the supported panel
# with different configurations. It also checks for the output colorspace is YUV when
# YCbCr is enabled and  RGB when YCbCr is disabled
#
# CommandLine: python ycbcr_ddc_ed_ycbcr_panel_and_non-hdmi_panel_basic.py -edp_a -hdmi_b HDMI_Dell_U2709_YCBCR.EDID
#
# \author Smitha B
###############################################################################################
from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.window_helper import move_mouse_cursor
from Tests.Color.color_base import *
from Tests.Color.color_verification import *


class YCbCrDDCEDYCbCrPanelAndNonHDMIPanelBasic(ColorBase):

    def verify_registers(self):
        ##
        # Get the output colorspace of all the displays
        logging.info(self.getStepInfo() + "Verifying output color space for display %s" % self.display)
        colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC', "YUV")
        if colorspace_status != "YUV":
            self.fail("Pipe output color space mismatch for display: %s" % self.display)

        ##
        # Get the cursor status
        cursor_status = get_cursor_status(self.display, 'CUR_CTL')

        ##
        # Get the plane CSC usage
        logging.info(self.getStepInfo() + "Verifying Plane CSC status for display %s" % self.display)
        csc_usage = get_plane_csc_usage(self.display, 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1', 'PIPE_BOTTOM_COLOR')
        if not csc_usage:
            self.fail("Failed to get plane csc usage")

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
                logging.info("YCbCr is supported on panel: %s" % self.display)
                break

        if self.ycbcr_supported:

            ##
            # Set topology to CLONE, EXTENDED display configuration
            topology_list = [enum.CLONE, enum.EXTENDED]

            ##
            # Apply CLONE display configuration across all the displays
            for topology_index in range(len(topology_list)):
                if self.config.set_display_configuration_ex(topology_list[topology_index], self.connected_list) is True:
                    logging.info(self.getStepInfo() + "Applied the configuration as %s %s" % (
                        DisplayConfigTopology(topology_list[topology_index]).name,
                        self.get_display_configuration(self.connected_list)))

                    if topology_list[topology_index] == enum.EXTENDED:
                        ##
                        # Move mouse cursor
                        logging.info(self.getStepInfo() + "Moving the cursor position from panel %s to %s" % (
                            self.connected_list[0], self.connected_list[1]))
                        move_mouse_cursor(self.connected_list[0], self.connected_list[1])
                    ##
                    # Enables YCbCr
                    logging.info(self.getStepInfo() + "Enabling YCbCr on panel: %s" % self.display)
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
                        logging.info(self.getStepInfo() + "Disabling YCbCr on panel: %s" % self.display)
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
        "Test purpose: Enables YCbCr on supported panels and checks for YUV output color space in clone and extended display configurations "
        "when YCbCr is enabled")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
