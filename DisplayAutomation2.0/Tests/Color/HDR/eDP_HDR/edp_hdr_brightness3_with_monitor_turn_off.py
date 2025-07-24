#######################################################################################################################
# @file                 edp_hdr_brightness3_with_monitor_turn_off.py
# @addtogroup           Test_Color
# @section              edp_hdr_brightness3_with_monitor_turn_off
# @remarks              @ref edp_hdr_brightness3_with_monitor_turn_off.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux) which will be input from the test command line
#                       The script then invokes the API to set the OS Brightness Slider level to 78 level
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Pixel Compensation factor is calculated as BrightnessInNits/SDRWhiteLevelInNits,
#                       both values taken from the ETL.The Input Lut is then multiplied
#                       with the pixel compensation factor and OETF is applied on the input values,
#                       which is then combined with the OS Relative LUT for generating the Reference LUT
#                       which are compared with the programmed pipe gamma values, programmed by DSB in case of TGL, mmio otherwise
#                       Test Script performs a Monitor TurnOff-On event and
#                       verifies if the Pipe Gamma values are persisting after the event which implies that the Brightness values are persisting.
#
# Sample CommandLines:  python edp_hdr_brightness3_with_monitor_turn_off.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python edp_hdr_brightness3_with_monitor_turn_off.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR.os_hdr_base import  *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class eDPHDRBrightness3WithMonitorTurnOffOn(OSHDRBase, eDPHDRBase):
    def runTest(self):
        brightness_val_in_context, sdr_white_level_in_context = 0, 0
        brightness_level = 78
        os_relative_lut_in_context = []

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

        time.sleep(5)

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
                    display_utility.get_vbt_panel_type(display, gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:

                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID

                current_pipe = color_common_utility.get_current_pipe(str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))

                os_relative_lut_in_context = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
                if os_relative_lut_in_context is False:
                    self.fail("OSGiven1DLUT NOT event found in ETLs (OS Issue)")

                result, brightness_val_in_context, sdr_white_level_in_context = edp_hdr_utility.set_and_verify_brightness3_for_a_slider_level(
                    self.platform, current_pipe, target_id, brightness_level, os_relative_lut_in_context)
                if result is False:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR]Gamma verification failed for Brightness Slider Level")
                    self.fail(
                        "Gamma verification for Brightness Slider Level %s FAILED" % brightness_level)
                else:
                    logging.info(
                        "Gamma verification for Brightness Slider Level %s SUCCESSFUL" % brightness_level)

        ##
        # Perform Monitor Turn Off Event on eDP
        for display in self.connected_list:
            if display_utility.get_vbt_panel_type(display, 'gfx_0') in [display_utility.VbtPanelType.LFP_DP,
                                                                        display_utility.VbtPanelType.LFP_MIPI]:
                if color_common_utility.monitor_turn_off_on_events() is False:
                    self.fail()
                else:
                    logging.info("Successfully performed the Monitor Turn Off Event")
                    ##
                    # Due to smooth brightness, the brightness change will be applied in phases depending on the Transition time and the active RR.
                    # Currently OS is giving the Transition time as 200ms, hence waiting with a buffer added to it as 500ms
                    time.sleep(0.005)
                    driver_restart_path = color_common_utility.stop_etl_capture("After_Performing_MonitorTurnOff_Event_TimeStamp_")
                    if etl_parser.generate_report(driver_restart_path) is False:
                        logging.error("\tFailed to generate EtlParser report")
                        self.fail()
                    else:
                        for display_index in range(self.enumerated_displays.Count):
                            display = str(CONNECTOR_PORT_TYPE(
                                self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
                            gfx_index = self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                            if display in self.connected_list and \
                                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive and \
                                    display_utility.get_vbt_panel_type(display, gfx_index) in \
                                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:

                                event = "MonitorTurnOff"
                                current_pipe = color_common_utility.get_current_pipe(display)
                                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                                if edp_hdr_utility.verify_brightness3_persistence_after_an_event(event, self.platform,
                                                                                                 current_pipe,
                                                                                                 target_id,
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

        color_common_utility.stop_etl_capture("Completed_MonitorTurnOffandOnEvent")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
