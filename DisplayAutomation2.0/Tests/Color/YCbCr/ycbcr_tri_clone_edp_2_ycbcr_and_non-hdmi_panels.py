##############################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_s3_s4_reboot_mode_change
# \remarks
# \ref ycbcr_s3_s4_reboot_mode_change.py \n
# This script performs color functionality such as enable/disable YCbCr on the supported panel 
# and verify the Pipe CSC, output colorspace.
# and then Unplug YCbCr panel and Plug xvYCC Panel and check for xvYCC support and enable/disable xvYCC.
# Again Unplug xvYCC panel and Plug RGB Panel and verify colorspace. 
#
# CommandLine: python ycbcr_tri_clone_edp_2_ycbcr_and_non-hdmi_panels.py -edp_a -hdmi_b HDMI_Dell_U2709_YCBCR.EDID -dp_c
#
# \author Smitha B
###############################################################################################

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_base import *
from Tests.Color.color_verification import *


class YCbCrTriCloneeDP2YCbCrAndNonHDMIPanels(ColorBase):
    xvycc_edid = 'HDMI_DELL_U2711_XVYCC.EDID'
    dp_edid = 'DP_3011.EDID'
    dp_dpcd = 'DP_3011_dpcd.txt'

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
        self.enumerated_displays = self.config.get_enumerated_display_info()

        for index in range(len(self.connected_list)):
            if self.connected_list[index][:2] == "DP" and display_utility.get_vbt_panel_type(
                    self.connected_list[index], 'gfx_0') not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                if display_utility.unplug(self.connected_list[index], True) is False:
                    self.fail("Failed to unplug panel %s " % self.connected_list[index])
                else:
                    logging.debug("Successfully unplugged the DP display")
                    break

        ##
        # Apply CLONE on all the plugged displays
        topology = enum.CLONE
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0], self.connected_list[1]]) is True:
            logging.info(
                self.getStepInfo() + "Applied Display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                                 self.get_display_configuration(
                                                                                     self.connected_list)))

            self.target_id = self.config.get_target_id(self.connected_list[1], self.enumerated_displays)

            ##
            # Check if YCbCr is supported
            logging.info(
                self.getStepInfo() + "Checking for YCbCr support in connected panel: %s " % self.connected_list[1])
            ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)
            if ycbcr_supported:
                logging.info("YCbCr is supported on panel %s" % self.connected_list[1])
                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Enabling YCbCr on panel: %s" % self.connected_list[1])
                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                if not self.ycbcr_enable_status:
                    self.fail("Failed to enable YCbCr on panel: %s" % self.connected_list[1])
                else:
                    logging.info("Successfully enabled YCbCr on panel: %s" % self.connected_list[1])

                    ##
                    # Verify Registers
                    self.display = self.connected_list[1]
                    self.verify_registers()

                    ##
                    # Plug DP and apply Tri-Clone display configuration
                    for index in range(len(self.connected_list)):
                        if self.connected_list[index][:2] == "DP" and display_utility.get_vbt_panel_type(
                                self.connected_list[index], 'gfx_0') not in \
                                [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                            if display_utility.plug(self.connected_list[index], self.dp_edid, self.dp_dpcd,
                                                    False) is False:
                                self.fail("Failed to plug panel %s " % self.connected_list[index])
                            else:
                                logging.debug("Successfully plugged the DP display")
                                break

                    ##
                    # Verify the registers for each of the plugged displays
                    if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
                        logging.info(self.getStepInfo() + "Applied Display configuration as %s" % (
                            DisplayConfigTopology(topology).name))
                        # self.get_display_configuration(self.connected_list)))

                        self.display = self.connected_list[0]
                        logging.info(self.getStepInfo() + "Verifying output color space for panel %s" % self.display)
                        colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC', 'RGB')
                        if colorspace_status != "RGB":
                            self.fail("Pipe output color space mismatch for display: %s" % self.display)

                        ##
                        # Get the cursor status
                        cursor_status = get_cursor_status(self.display, 'CUR_CTL')
                        ##
                        # Verify Registers for YCbCr
                        self.display = self.connected_list[1]
                        self.verify_registers()
                        ##
                        # Verify Registers for DP
                        if len(self.connected_list) > 2:
                            self.display = self.connected_list[2]
                            ##
                            # Get the output colorspace
                            logging.info(
                                self.getStepInfo() + "Verifying output color space for panel %s" % self.display)
                            colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC', 'RGB')
                            if colorspace_status != "RGB":
                                self.fail("Pipe output color space mismatch for display: %s" % self.display)

                        ##
                        # Get the cursor status
                        cursor_status = get_cursor_status(self.display, 'CUR_CTL')
                        # #
                        # Unplug YCbCr supported HDMI Panel
                        logging.info("Unplug YCbCr supported HDMI Panel")
                        if display_utility.unplug(self.connected_list[1], False) is False:
                            self.fail("Failed to plug display %s" % self.connected_list[1])

                        ##
                        # Plug xvYCC supported HDMI Panel
                        logging.info(self.getStepInfo() + "Plugging in xvYCC supported HDMI Panel")
                        if display_utility.plug(self.connected_list[1], self.xvycc_edid) is False:
                            self.fail("Failed to plug display %s" % self.connected_list[1])

                        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
                            logging.info(self.getStepInfo() + "Applied Display configuration as %s" % (
                                DisplayConfigTopology(topology).name))
                            # self.get_display_configuration(self.connected_list)))
                            ##
                            # Verify if xvYCC is supported
                            logging.info(
                                self.getStepInfo() + "Verifying if xvYCC is supported by %s" % self.connected_list[1])
                            self.target_id = self.config.get_target_id(self.connected_list[1], self.enumerated_displays)
                            self.xvycc_supported = driver_escape.is_xvycc_supported(self.target_id)

                            ##
                            # Enable xvYCC on the supported HDMI Panel
                            if self.xvycc_supported:
                                logging.info(self.getStepInfo() + "Enabling xvYCC on panel %s" % self.connected_list[1])
                                self.xvycc_enable_status = driver_escape.configure_xvycc(self.target_id, True)
                                if not self.xvycc_enable_status:
                                    self.fail("Failed to enable xvYCC")
                                else:
                                    ##
                                    # Verify Registers for eDP
                                    ##
                                    # Get the output colorspace
                                    self.display = self.connected_list[0]
                                    logging.info(
                                        self.getStepInfo() + "Verifying output color space for display %s" % self.display)
                                    colorspace_status = get_pipe_output_colorspace(self.connected_list[0], 'PIPE_MISC',
                                                                                   'RGB')
                                    if colorspace_status != "RGB":
                                        self.fail("Pipe output color space mismatch for display: %s" % self.display)

                                    ##
                                    # Get the cursor status
                                    cursor_status = get_cursor_status(self.display, 'CUR_CTL')

                                    ##
                                    # Verify Registers for xvYCC Panel
                                    logging.info(self.getStepInfo() + "Verifying Registers for xvYCC Panel")
                                    self.display = self.connected_list[1]
                                    self.verify_registers()
                                    xvycc_status = get_xvycc_status(self.display, 'VIDEO_DIP_CTL')
                                    if not xvycc_status:
                                        self.fail("xvYCC is not enabled")

                                    ##
                                    # Verify Registers for DP
                                    if len(self.connected_list) > 2:
                                        self.display = self.connected_list[2]
                                        ##
                                        # Get the output colorspace
                                        logging.info(
                                            self.getStepInfo() + "Verifying output color space for panel %s" % self.display)
                                        colorspace_status = get_pipe_output_colorspace(self.display, 'PIPE_MISC',
                                                                                       'RGB')
                                        if colorspace_status != "RGB":
                                            self.fail(
                                                "Pipe output color space mismatch for display: %s" % self.display)
                            else:
                                self.fail("Panel doesnt support xvYCC")
            else:
                self.fail("None of the panels connected support yCbCr")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Enables YCbCr on supported panels, verifies YUV/RGB output color space when YCbCr/xvYCC is enabled, "
                 "swaps YCbCr panel with xvYCC panel in different configurations")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
