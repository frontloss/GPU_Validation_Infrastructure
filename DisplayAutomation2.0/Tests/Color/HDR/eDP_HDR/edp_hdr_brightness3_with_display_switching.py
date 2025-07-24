#######################################################################################################################
# @file                 edp_hdr_brightness3_with_display_switching.py
# @addtogroup           Test_Color
# @section              edp_hdr_brightness3_with_display_switching
# @remarks              @ref edp_hdr_brightness3_with_display_switching.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux)
#                       and external displays(could be HDR/non-HDR) which are input from the test command line.
#                       The script then invokes the API to set the OS Brightness Slider level to 25 level
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pixel Compensation factor is calculated as BrightnessInNits/SDRWhiteLevelInNits,
#                       both values taken from the ETL.The Input Lut is then multiplied
#                       with the pixel compensation factor and OETF is applied on the input values,
#                       which is then combined with the OS Relative LUT for generating the Reference LUT
#                       and compared with the programmed pipe gamma values, programmed by DSB in case of TGL, mmio otherwise
#                       Different Display Switching scenarios such as (ED, SD on Display1, SD on Display2 and so on
#                       are applied and after each modeset, verifying if the Pipe Gamma values are persisting
#                       which implies that the Brightness values are persisting.
#
# Sample CommandLines:  python edp_hdr_brightness3_with_display_switching.py -edp_a SINK_EDP76 -hdmi_b SamsungJS9500_HDR.bin -config EXTENDED
# Sample CommandLines:  python edp_hdr_brightness3_with_display_switching.py -edp_a SINK_EDP76 -hdmi_b SamsungJS9500_HDR.bin -dp_d Benq_SW320.bin DP_HDR_DPCD.txt -config EXTENDED
# @author       Smitha B
#######################################################################################################################
from Libs.Core import enum
import itertools
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class eDPHDRBrightness3WithDisplaySwitching(OSHDRBase, eDPHDRBase):

    def runTest(self):
        brightness_val_in_context, sdr_white_level_in_context = 0, 0
        brightness_level = 25
        os_relative_lut_in_context = []
        topology_list = [enum.SINGLE,enum.EXTENDED]
        display_config_list = []
        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Verify HDR Caps
        if color_parse_etl_events.fetch_and_verify_hdr_caps_from_etl() is False:
            self.fail("Failed to verify HDR caps from ETL")

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
        # In case of dual eDP HDR Configs, have to fetch the OSOneDLUT for each TargetID
        for display_index in range(self.enumerated_displays.Count):
            display = str(
                CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            gfx_index = self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive and \
                    display_utility.get_vbt_panel_type(display, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:

                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID

                current_pipe = color_common_utility.get_current_pipe(str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))

                os_relative_lut_in_context = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
                if os_relative_lut_in_context is False:
                    self.fail("OSGiven1DLUT NOT event found in ETLs (OS Issue)")

                result, brightness_val_in_context, sdr_white_level_in_context = edp_hdr_utility.set_and_verify_brightness3_for_a_slider_level(
                    self.platform, current_pipe, target_id, brightness_level,os_relative_lut_in_context)
                if result is False:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR]Gamma verification failed for Brightness Slider Level")
                    self.fail(
                        "Gamma verification for Brightness Slider Level %s FAILED" % brightness_level)
                else:
                    logging.info(
                        "Gamma verification for Brightness Slider Level %s SUCCESSFUL" % brightness_level)

        color_common_utility.stop_etl_capture("AfterSettingSlider_BeforeSwitchingScenarios_TimeStamp_")

        ##
        # Apply all the combinations of configurations on the displays
        for i in range(2, len(self.connected_list) + 1):
            for subset in itertools.permutations(self.connected_list, i):
                for j in range(1, len(topology_list)):
                    display_config_list.append((topology_list[0], [subset[0]]))
                    display_config_list.append((topology_list[j], list(subset)))

        for each_config in range(len(display_config_list)):
            topology = display_config_list[each_config][0]
            displays_list = display_config_list[each_config][1]
            if color_common_utility.display_switch(topology, displays_list) is False:
                self.fail()
            else:
                time.sleep(0.005)
                stress_display_event = "Applying_" + DisplayConfigTopology(topology).name + "_TimeStamp_"
                color_common_utility.stop_etl_capture(stress_display_event)
                for display in displays_list:
                    if display_utility.get_vbt_panel_type(display, 'gfx_0') in \
                            [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                        event = "DisplaySwitch"
                        current_pipe = color_common_utility.get_current_pipe(display)
                        target_id = DisplayConfiguration().get_target_id(display, self.enumerated_displays)
                        if edp_hdr_utility.verify_brightness3_persistence_after_an_event(event, self.platform,
                                                                                         current_pipe, target_id,
                                                                                         os_relative_lut_in_context,
                                                                                         brightness_val_in_context,
                                                                                         sdr_white_level_in_context) is False:
                            color_common_utility.gdhm_report_app_color(
                                title="[COLOR]Gamma verification failed for Brightness Slider Level")
                            self.fail(
                                "Gamma verification for Brightness Slider Level %s FAILED AFTER performing %s" % (
                                brightness_level, event))
                        else:
                            logging.info(
                                "Gamma verification for Brightness Slider Level %s SUCCESSFUL AFTER performing %s" % (
                                brightness_level, event))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
