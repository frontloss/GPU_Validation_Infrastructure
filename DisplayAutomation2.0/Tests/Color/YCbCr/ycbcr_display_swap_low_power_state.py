##############################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_display_swap_low_power_state
# \remarks
# \ref ycbcr_display_swap_low_power_state.py \n
# This script performs color functionality such as enable/disable YCbCr on the supported panel 
# and verify the Pipe CSC, output colorspace.
# and then Unplug YCbCr panel and Plug xvYCC Panel in S3 and check for xvYCC support and enable/disable xvYCC.
# Again Unplug xvYCC panel and Plug RGB Panel in S3 and verify colorspace. Unplug RGB Panel and again Plug YCbCr 
# supported panel and verify the registers.
# CommandLine: python ycbcr_display_swap_low_power_state.py -hdmi_b HDMI_Dell_U2709_YCBCR.EDID -dp_c
#
# \author Smitha B
###############################################################################################
from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_base import *
from Tests.Color.color_verification import *



class YCbCrDisplaySwapLowPower(ColorBase):
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
                    self.connected_list[index], 'gfx_0') not in [display_utility.VbtPanelType.LFP_DP,
                                                                 display_utility.VbtPanelType.LFP_MIPI]:
                if display_utility.unplug(self.connected_list[index], True) is False:
                    self.fail("Failed to unplug panel %s " % self.connected_list[index])
                else:
                    logging.debug("Successfully unplugged the DP display")
                    break

        ##
        # Apply SD on YCbCr supported HDMI Panel
        topology = enum.SINGLE
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info(
                self.getStepInfo() + "Applied the configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                             self.get_display_configuration(
                                                                                 self.connected_list)))

            self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

            ##
            # Check if YCbCr is supported
            logging.info(
                self.getStepInfo() + "Checking for YCbCr support in connected panel: %s " % self.connected_list[0])
            self.ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)
            if self.ycbcr_supported:
                ##
                # Enables YCbCr
                logging.info(self.getStepInfo() + "Panel %s supports YCbCr. Enabling YCbCr" % self.connected_list[0])
                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                if not self.ycbcr_enable_status:
                    self.fail("Failed to enable YCbCr")
                else:
                    logging.info("Successfully enabled YCbCr")

                    ##
                    # Verify Registers
                    self.display = self.connected_list[0]
                    self.verify_registers()

                    ##
                    # Unplug YCbCr supported HDMI Panel in Low Power
                    logging.info(self.getStepInfo() + "Unplugging %s panel" % self.connected_list[0])
                    if display_utility.unplug(self.connected_list[0], True) is False:
                        self.fail("Failed to unplug panel %s " % self.connected_list[0])

                    ##
                    # Plug xvYCC supported HDMI Panel in Low Power
                    logging.info(self.getStepInfo() + "Plugging in %s panel" % self.connected_list[0])
                    if display_utility.plug(self.connected_list[0], self.xvycc_edid, None, True) is False:
                        self.fail("Failed to plug panel %s " % self.connected_list[0])

                    ##
                    # Invoke s3 state
                    if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                        self.fail("Power Event POWER_STATE_S3: Failed")

                    ##
                    # Verify if xvYCC is supported
                    self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
                    self.xvycc_supported = driver_escape.is_xvycc_supported(self.target_id)

                    ##
                    # Enable xvYCC on the supported HDMI Panel
                    if self.xvycc_supported:
                        logging.info(self.getStepInfo() + "Panel supports xvYCC. Enabling xvYCC")
                        self.xvycc_enable_status = driver_escape.configure_xvycc(self.target_id, True)
                        if not self.xvycc_enable_status:
                            self.fail("Failed to enable xvYCC")
                        else:
                            logging.info("Successfully enabled xvYCC")
                            ##
                            # Verify Registers
                            self.display = self.connected_list[0]
                            self.verify_registers()

                            ##
                            # Unplug xvYCC supported HDMI Panel in Low Power
                            logging.info(
                                self.getStepInfo() + "Unplugging %s panel " % self.connected_list[0])
                            if display_utility.unplug(self.connected_list[0], True) is False:
                                self.fail("Failed to unplug panel %s " % self.connected_list[0])
                            else:
                                logging.info("Unplugged xvYCC supported panel %s" % self.connected_list[0])

                            for index in range(len(self.connected_list)):
                                if self.connected_list[index][:2] == "DP" and display_utility.get_vbt_panel_type(
                                        self.connected_list[index], 'gfx_0') not in \
                                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                                    if display_utility.plug(self.connected_list[index], self.dp_edid, self.dp_dpcd,
                                                            True) is False:
                                        self.fail("Failed to plug panel %s " % self.connected_list[index])
                                    else:
                                        logging.debug("Successfully plugged the DP display")
                                        break

                            ##
                            # Invoke s3 state
                            if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                                self.fail("Power Event POWER_STATE_S3: Failed")

                            ##
                            # Verify if the ColorSpace is RGB
                            logging.info(
                                self.getStepInfo() + "Verifying output color space for display %s" % self.display)
                            colorspace_status = get_pipe_output_colorspace('DP_C', 'PIPE_MISC', 'RGB')
                            if colorspace_status != "RGB":
                                self.fail("Pipe output color space mismatch for display: %s" % self.display)

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
                            # Plug YCbCr supported HDMI Panel in Low Power
                            logging.info(
                                self.getStepInfo() + "Plugging in YCbCr supported HDMI panel: %s" % self.connected_list[
                                    0])
                            if display_utility.plug_display(self.connected_list[0], self.cmd_line_param, True) is False:
                                self.fail(
                                    "Failed to plug display %s " % self.connected_list[0])
                            else:
                                logging.info("Plugged YCbCr supported panel %s" % self.connected_list[0])

                            ##
                            # Invoke s3 state
                            if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                                self.fail("Power Event POWER_STATE_S3: Failed")

                            ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)
                            if ycbcr_supported:
                                ##
                                # Enables YCbCr
                                logging.info(
                                    self.getStepInfo() + "Panel (target id: %d) supports YCbCr. Enabling YCbCr" % self.target_id)
                                self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                                if not self.ycbcr_enable_status:
                                    self.fail("Failed to enable YCbCr")
                                else:
                                    logging.info("Successfully enabled YCbCr")
                            else:
                                logging.debug("YCbCr is not supported on display target id: %d" % self.target_id)
                            ##
                            # Verify Registers
                            self.display = self.connected_list[0]
                            self.verify_registers()
                    else:
                        self.fail("Panel does not support xvYCC")
            else:
                self.fail("None of the panels connected support yCbCr")
        else:
            self.fail("Failed to apply display configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables YCbCr on supported panels and verifies YUV output color space with plug/unplug of "
        "YCbCr/xvYCC and RGB panels in low power state")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
