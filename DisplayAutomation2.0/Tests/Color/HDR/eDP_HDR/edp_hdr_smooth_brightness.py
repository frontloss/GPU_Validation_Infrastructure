#######################################################################################################################
# @file                 edp_hdr_smooth_brightness.py
# @addtogroup           Test_Color
# @section              edp_hdr_smooth_brightness
# @remarks              @ref edp_hdr_smooth_brightness.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux)
#                       which is an input parameter from the test command line.
#                       The script then invokes the API to set the OS Brightness Slider level to a particular level
#                       to save the current applied brightness in context. Apply different modesets
#                       with different refresh rates which is a parameter to calculate the total number of steps
#                       across which the transition from Current Brightness to Target Brightness will be applied
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Pixel Compensation factor is calculated as BrightnessInNits/SDRWhiteLevelInNits,
#                       both values taken from the ETL.The Input Lut is then multiplied
#                       with the pixel compensation factor and OETF is applied on the input values,
#                       which is then combined with the OS Relative LUT for generating the Reference LUT
#                       which are compared with the programmed pipe gamma values, programmed by DSB in case of TGL, mmio otherwise
#                       Above Gamma LUT verification is performed for each step in the transition
#                       Smaller ETLs are collected after each Slider level is set and parsed individually
#                       to verify the PipeGamma values
# Sample CommandLines:  python edp_hdr_smooth_brightness.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python edp_hdr_smooth_brightness.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class eDPHDRSmoothBrightness(OSHDRBase, eDPHDRBase):

    def runTest(self):
        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Verify HDR Caps
        if color_parse_etl_events.fetch_and_verify_hdr_caps_from_etl() is False:
            self.fail("Failed verification of HDR caps from ETL")

        ##
        # Enable HDR
        super().toggle_and_verify_hdr(toggle="ENABLE")

        ##
        # Apply Unity Gamma at the beginning of the test after enabling HDR
        color_common_utility.apply_unity_gamma()

        ##
        # Stop the ETL after enabling HDR, to get the SDRWhiteLevel value
        hdr_etl_path = color_common_utility.stop_etl_capture("After_Enabling_HDR_TimeStamp_")
        if etl_parser.generate_report(hdr_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Iterate through all the enumerated, active displays mentioned in the command line
        # Applying different modes and calculating the SmoothBrightness changes
        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            gfx_index = self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive and \
                    display_utility.get_vbt_panel_type(display, gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:

                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID

                current_pipe = color_common_utility.get_current_pipe(str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))

                ##
                # Prepare a mode_list with different refresh rates
                mode_list = []
                current_mode = self.config.get_current_mode(target_id)
                logging.debug("Current mode: %sX%s @%s %s" % (
                    current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
                supported_modes = self.config.get_all_supported_modes([target_id])
                for key, values in supported_modes.items():
                    for mode in values:
                        if mode.HzRes == current_mode.HzRes and mode.VtRes == current_mode.VtRes and mode.scaling == current_mode.scaling:
                            if mode.refreshRate == 30 or mode.refreshRate == 24 or mode.refreshRate == 59 or mode.refreshRate == 60:
                                mode_list.append(mode)

                logging.debug("Length of the modelist is %s" %len(mode_list))

                os_relative_lut_in_context = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
                if os_relative_lut_in_context is False:
                    self.fail("OSGiven 1DLUT NOT event found in ETLs (OS Issue)")

                ##
                # Change Brightness Slider to have the current brightness level in context
                brightness_slider_level = 0
                logging.info("Setting Brightness Slider to %s to save the current applied brightness in context" %brightness_slider_level)
                result, current_applied_brightness, current_applied_sdr_white_level = edp_hdr_utility.set_and_verify_brightness3_for_a_slider_level(
                    self.platform, current_pipe, target_id, brightness_slider_level, os_relative_lut_in_context)
                if result is False:
                    self.fail(
                        "Gamma verification for Brightness Slider Level %s FAILED" % brightness_slider_level)
                else:
                    logging.info(
                        "Gamma verification for Brightness Slider Level %s SUCCESSFUL" % brightness_slider_level)

                ##
                # List of Slider levels including both forward and backward movement of the sliders
                brightness_change_list = [90, 50, 51, 0]

                ##
                # Apply Modes with different Refresh Rates since it plays a role in
                # calculating the number of frames the brightness transition should span across
                for mode_index in range(len(mode_list)):

                    if self.config.set_display_mode([mode_list[mode_index]]):
                        logging.info("Successfully applied a ModeSet with HzRes : %s, VtRes : %s, RefreshRate : %s" %(mode_list[mode_index].HzRes, mode_list[mode_index].VtRes, mode_list[mode_index].refreshRate))
                    etl_name = "4kModeSetWithRR_" + str(mode_list[mode_index].refreshRate) + "TimeStamp_"
                    time.sleep(2)
                    color_common_utility.stop_etl_capture(etl_name)
                    ##
                    # Calculating the number of frames across which the brightness will be applied in phases
                    for index in range(len(brightness_change_list)):
                        ##
                        # Set the OS Brightness Slider to the level iterating through the list
                        color_common_utility.set_os_brightness(brightness_change_list[index], delay=0)
                        ##
                        # Due to smooth brightness, the brightness change will be applied in phases depending on the Transition time and the active RR.
                        # Currently OS is giving the Transition time as 200ms, hence waiting with a buffer added to it as 500ms
                        time.sleep(0.005)

                        brightness_level = "Setting_Brightness_level_to_" + str(brightness_change_list[index]) + "_" + "TimeStamp_"
                        brightness_file_path = color_common_utility.stop_etl_capture(brightness_level)
                        if etl_parser.generate_report(brightness_file_path) is False:
                            logging.error("\tFailed to generate EtlParser report")

                        ##
                        # Fetching the transition_time_in_milli_nits given by OS from the ETl
                        transition_time_in_milli_nits = color_parse_etl_events.get_smooth_brightness_transition_time_from_etl(
                            target_id) / 1000
                        total_transition_steps = int(transition_time_in_milli_nits * mode_list[mode_index].refreshRate)
                        logging.info("Total No. of steps for brightness transition from Current to Target Brightness Val : %s" % total_transition_steps)

                        ##
                        # Fetch the Target BrightnessValue in Nits given by OS from the ETL
                        target_brightness_val = color_parse_etl_events.get_brightness3_in_nits_from_etl(target_id)
                        if target_brightness_val is False:
                            self.fail("No Brightness3 event found in ETLs")
                        else:
                            total_delta_in_brightness = target_brightness_val - current_applied_brightness
                            logging.debug("Current Applied Brightness %s" %current_applied_brightness)
                            logging.debug("Target_Brightness_level %s" % target_brightness_val)
                            logging.debug("Total Delta in Brightness %s" % total_delta_in_brightness)

                            delta_in_phases = total_delta_in_brightness / total_transition_steps
                            logging.debug("Delta Brightness to be applied in each step is %s" %  delta_in_phases)
                            ##
                            # Pixel Boost Verification to be performed for each of Phase
                            for each_step in range(0, total_transition_steps):
                                phased_brightness = current_applied_brightness + delta_in_phases
                                ##
                                # For the next iteration, current_applied_brightness should be updated
                                current_applied_brightness = phased_brightness
                                pixel_boost = phased_brightness / current_applied_sdr_white_level
                                logging.debug("Pixel Boost in Step %s is %s" %(each_step, pixel_boost))
                                if color_common_utility.fetch_ref_hdr_gamma_and_programmed_gamma_and_compare(self.platform, current_pipe, os_relative_lut_in_context,
                                                                                                             color_common_constants.OS_RELATIVE_LUT_SIZE,
                                                                                                             pixel_boost=pixel_boost, is_smooth_brightness=True, total_steps=total_transition_steps, step_index=each_step) is False:

                                    self.fail("Gamma verification for Phase %s while applying Brightness Slider Level %s FAILED" % (each_step, brightness_change_list[index]))
                                else:
                                    logging.info("Gamma verification for Phase %s while applying Brightness Slider Level %s SUCCESSFUL" % (each_step, brightness_change_list[index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
