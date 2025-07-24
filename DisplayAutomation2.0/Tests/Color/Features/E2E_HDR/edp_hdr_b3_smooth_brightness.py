#######################################################################################################################
# @file                 edp_hdr_b3_smooth_brightness.py
# @addtogroup           Test_Color
# @section              edp_hdr_b3_smooth_brightness
# @remarks              @ref edp_hdr_b3_smooth_brightness.py \n
#                       The test script enables HDR on eDP_HDR display/s,
#                       which is an input parameter from the test command line.
#                       The script can handle both Aux and SDP varity of displays.
#                       The script invokes the API to set the OS Brightness Slider level
#                       to a value provided in the command line.
#                       If no value is provided, then the script fetches the current brightness and
#                       sets a random value other than the current level.
#                       Apply different modesets with different refresh rates
#                       which is a parameter to calculate the total number of steps
#                       across which the transition from Current Brightness to Target Brightness will be applied
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python edp_hdr_b3_smooth_brightness.py -edp_a SINK_EDP050 -config SINGLE
# Sample CommandLines:  python edp_hdr_b3_smooth_brightness.py -edp_a SINK_EDP076 -config SINGLE
# @author       Smitha B
#######################################################################################################################
import time

from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class eDPHDRB3SmoothBrightness(HDRTestBase):

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Apply Modes with different RR and verify ***")
        panel_mode_dict = {}
        rr_list = [30, 24, 59, 60]
        ##
        # Prepare a mode_list with different refresh rates
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                current_mode = common_utility.get_current_mode(panel.display_and_adapterInfo)
                logging.debug("Current mode: %sX%s @%s %s" % (
                    current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
                for index in range(0, rr_list.__len__()):
                    mode = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS, refresh_rate=rr_list[index])
                    if mode.__len__() != 0:
                        panel_mode_dict[gfx_index, port] = mode[0]

        ##
        # List of Slider levels including both forward and backward movement of the sliders
        brightness_change_list = [90, 50, 51, 0]
        ##
        # Apply Modes with different Refresh Rates since it plays a role in
        # calculating the number of frames the brightness transition should span across
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp and panel.is_active and panel.FeatureCaps.HDRSupport:
                    if self.config.set_display_mode([panel_mode_dict[gfx_index, port]]):
                        logging.info("Successfully applied a ModeSet with HzRes : %s, VtRes : %s, RefreshRate : %s" % (
                        panel_mode_dict[gfx_index, port].HzRes, panel_mode_dict[gfx_index, port].VtRes, panel_mode_dict[gfx_index, port].refreshRate))

                    current_applied_brightness = self.panel_props_dict[gfx_index, port].b3_value
                    ##
                    # Calculating the number of frames across which the brightness will be applied in phases
                    for index in range(len(brightness_change_list)):
                        panel_props = self.panel_props_dict[gfx_index, port]
                        ##
                        # Set the OS Brightness Slider to the level iterating through the list
                        if hdr_utility.set_b3_slider_and_fetch_b3_info(panel.target_id,
                                                                       brightness_change_list[index],
                                                                       panel_props):
                            # # Due to smooth brightness, the brightness change will be applied in phases depending
                            # on the Transition time and the active RR. Currently OS is giving the Transition time as
                            # 200ms, hence waiting with a buffer added to it as 500ms
                            time.sleep(0.005)
                            total_transition_steps = int(self.panel_props_dict[gfx_index, port].b3_transition_time * panel_mode_dict[gfx_index, port].refreshRate)
                            logging.info(
                                "Total No. of steps for brightness transition from Current to Target Brightness Val : "
                                "%s" % total_transition_steps)

                            total_delta_in_brightness = self.panel_props_dict[gfx_index, port].b3_value - current_applied_brightness
                            logging.info("Current Applied Brightness {0}".format(current_applied_brightness))
                            logging.info("Target_Brightness_level {0}".format(self.panel_props_dict[gfx_index, port].b3_value))
                            logging.info("Total Delta in Brightness {0}".format(total_delta_in_brightness))

                            ##
                            # delta_in_phases specifies what is the delta brightness to be applied in each phase
                            delta_in_phases = total_delta_in_brightness / total_transition_steps
                            logging.info("Delta Brightness to be applied in each step is {0}".format(delta_in_phases))
                            #
                            # Pixel Boost Verification to be performed for each of Phase
                            for each_step in range(0, total_transition_steps):
                                phased_brightness = current_applied_brightness + delta_in_phases
                                current_applied_brightness = phased_brightness
                                ##
                                # For the next iteration, current_applied_brightness should be updated
                                self.panel_props_dict[gfx_index, port].b3_value = phased_brightness
                                self.panel_props_dict[gfx_index, port].pixel_boost = phased_brightness / \
                                                                                     self.panel_props_dict[
                                                                                         gfx_index, port].sdr_white_level
                                logging.info("Pixel Boost in Step {0} is {1}".format(each_step, self.panel_props_dict[gfx_index, port].pixel_boost))

                                if self.pipe_verification(gfx_index, adapter.platform, port,
                                                              panel, is_smooth_brightness=True, step_index=each_step) is False:
                                    self.fail()
                            current_applied_brightness = self.panel_props_dict[gfx_index, port].b3_value
                        else:
                            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
