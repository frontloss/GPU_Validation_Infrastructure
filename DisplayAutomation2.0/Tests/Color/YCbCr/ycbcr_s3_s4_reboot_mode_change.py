##############################################################################################
# @file     ycbcr_s3_s4_reboot_mode_change.py
# @brief    This script performs color functionality such as enable/disable YCbCr on the supported panel
#           after power events like S3, S4, Reboot and display mode changes. It also checks for the output
#           colorspace is YUV when YCbCr is enabled and RGB when YCbCr is disabled
#           CommandLine: python ycbcr_s3_s4_reboot_mode_change.py -hdmi_b HDMI_Dell_U2709_YCBCR.EDID
# @author   Smitha B
###############################################################################################

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_base import *
from Tests.Color.color_verification import *

class YCbCrS3S4RebootModeChange(ColorBase):

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

    def test_before_reboot(self):
        logging.info("Test Before Reboot")
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
            # Apply SINGLE display configuration on YCbCr supported panel
            if self.config.set_display_configuration_ex(topology, [self.display]) is True:
                logging.info(self.getStepInfo() + "Applied Display configuration as %s %s" % (
                    DisplayConfigTopology(topology).name, self.get_display_configuration([self.display])))

                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Enabling YCbCr on panel %s" % self.display)
                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                if not self.ycbcr_enable_status:
                    self.fail("Failed to enable YCbCr")
                else:
                    logging.info("Successfully enabled YCbCr")
                    ##
                    # Verify Registers
                    self.verify_registers()

                    ##
                    # Invoke s3 state
                    logging.info(self.getStepInfo() + "Invoking POWER_STATE_S3 event")
                    if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60):
                        logging.info("S3 Power Event: Success")
                    else:
                        self.fail("S3 Power Event: Failed")

                    logging.info(self.getStepInfo() + "Invoking POWER_STATE_S3 event")
                    if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60):
                        logging.info("S3 Power Event: Success")
                    else:
                        self.fail("S3 Power Event: Failed")

                    time.sleep(2)

                    ##
                    # Verify Registers
                    self.verify_registers()

                    ##
                    # Invoke s4 state
                    logging.info(self.getStepInfo() + "Invoking POWER_STATE_S4 event")
                    if self.display_power.invoke_power_event(display_power.PowerEvent.S4, 60):
                        logging.info("S4 Power Event: Success")
                    else:
                        self.fail("S4 Power Event: Failed")

                    time.sleep(2)

                    ##
                    # Verify Registers
                    self.verify_registers()

                    if reboot_helper.reboot(self, 'test_after_reboot') is False:
                        self.fail("Failed to reboot the system")
            else:
                self.fail("Failed to apply display configuration as %s %s" % (
                    DisplayConfigTopology(topology).name, self.display))

        else:
            self.fail("None of the panels connected support YCbCr")

    def test_after_reboot(self):
        logging.info("After reboot")
        self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

        ##
        # Check if YCbCr is supported
        self.ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)

        if self.ycbcr_supported:
            self.display = self.connected_list[0]
            ##
            # Get the output colorspace
            logging.info(self.getStepInfo() + "Verifying output color space for display %s" % self.connected_list[0])
            colorspace_status = get_pipe_output_colorspace(self.connected_list[0], 'PIPE_MISC', 'YUV')
            if colorspace_status != "YUV":
                self.fail("Pipe output color space mismatch for display: %s" % self.display)

            ##
            # Apply non native resolution and verify registers
            supported_modes = self.config.get_all_supported_modes([self.target_id])
            for key, values in supported_modes.items():
                mode = values[0]
                logging.info(
                    self.getStepInfo() + "Applying display mode: %s" % mode.to_string(self.enumerated_displays))
                if self.config.set_display_mode([mode]):
                    logging.info("Mode set successful")
                else:
                    self.fail("Mode set failed")

                ##
                # Verify Registers
                self.verify_registers()
                break

        ##
        # Disables YCbCr
        disable_status = driver_escape.configure_ycbcr(self.target_id, False)
        if not disable_status:
            self.fail("Failed to disable YCbCr")
        else:
            logging.info("Successfully disabled YCbCr")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enabled YCbCr on supported panel and checks for the persistency of YUV color space "
                 "after S3, S4 and system reboot")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('YCbCrS3S4RebootModeChange'))
    TestEnvironment.cleanup(outcome)
