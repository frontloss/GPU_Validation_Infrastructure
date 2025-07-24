##############################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_basic
# \remarks
# \ref ycbcr_basic.py \n
# This script performs basic color functionality such as enable/disable YCbCr on the supported
# panel.It also checks for the output color space is YUV when YCbCr is enabled and  RGB when
# YCbCr is disabled
#
# CommandLine: python ycbcr_basic.py -hdmi_b HDMI_Dell_U2709_YCBCR.EDID
#
# \author Smitha B
###############################################################################################
from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_base import *
from Tests.Color.color_verification import *


class YCbCrBasic(ColorBase):
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
        # Get the plane CSC usage
        logging.info(self.getStepInfo() + "Verifying Plane CSC status for display %s" % self.display)
        csc_usage = get_plane_csc_usage(self.display, 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1', 'PIPE_BOTTOM_COLOR')
        if not csc_usage:
            self.fail("Failed to get plane csc usage")

    def runTest(self):
        ycbcr_supported = 0
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
            # Set topology to SINGLE display configuration
            topology = enum.SINGLE

            ##
            # Apply SINGLE display configuration on YCbCr supported panel
            if self.config.set_display_configuration_ex(topology, [self.display]) is True:
                logging.info(self.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name, self.get_display_configuration([self.display])))

                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Enabling YCbCr")
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
                    logging.info(self.getStepInfo() + "Disabling YCbCr")
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
        "Test purpose: Enables YCbCr on supported panels and check for YUV output color space when YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
