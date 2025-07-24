######################################################################################
# \file
# \section edp_hdr_utility
# \remarks
# \ref edp_hdr_utility.py \n
# This script contains helper functions that will be used by edp_hdr test scripts
#
# \author   Smitha B
######################################################################################
import logging
import time
from Libs.Core import display_utility
from Libs.Core import etl_parser
from Tests.Color import color_common_utility
from Tests.Color import color_common_constants
from Tests.Color import color_parse_etl_events


##
# @brief verify_dpcd_edp_brightness_nits() - To fetch and verify the value programmed at DPCD address 0x354
# @param[in] -  enumerated_displays - To get the target_id based on the enumerated displays(only LFP)
def verify_dpcd_edp_brightness_nits(enumerated_displays):
    for index in range(enumerated_displays.Count):
        vbt_panel_type = display_utility.get_vbt_panel_type(
            enumerated_displays.ConnectedDisplays[index].ConnectorNPortType,
            enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
        if vbt_panel_type in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
            lsb_nits_value = color_common_utility.fetch_dpcd_data(color_common_constants.EDP_BRIGHTNESS_NITS_BYTE0_LSB,enumerated_displays.ConnectedDisplays[index].TargetID)
            msb_nits_value = color_common_utility.fetch_dpcd_data(color_common_constants.EDP_BRIGHTNESS_NITS_BYTE1_MSB,enumerated_displays.ConnectedDisplays[index].TargetID)
            nits_value = (msb_nits_value << 8) | lsb_nits_value
            logging.info("Nits Value in the DPCD is %s" % nits_value)


##
# Interface used by the test cases to verify the persistence of the Brightness slider set as part of the test case.
# The events can be DisplaySwitch, DriverDisableEnable, HDRDisableEnable, MonitorTurnOff, HotplugUnplug
# If OS is not giving any new BrightnessValue, SDRWhiteLevel, OSRelative LUT, the function uses the values available in the context
# If new DDI calls are issued by OS, then the values are compared with the values in context, if they are not same(except OS relative LUT),
# Then the test has to be reporting the issue and fail the test as an OS Issue, since the Brightness or SDRWhiteLevel is not expected to change after an event
# if the sliders are untouched during the event.
def verify_brightness3_persistence_after_an_event(event, platform, current_pipe, target_id, os_relative_lut_in_context, brightness_in_context, sdr_white_level_in_context):
    os_relative_lut_after_event = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
    if os_relative_lut_after_event is False:
        logging.info(
            "No new OneDLUTData from OS, hence will be using the LUT already available in the context")
        os_relative_lut_after_event = os_relative_lut_in_context

    ##
    # Get the brightness value from OS again
    brightness_val_in_nits_after_event = color_parse_etl_events.get_brightness3_in_nits_from_etl(target_id)
    ##
    # After HotUnplug and Plug, not expecting OS to give a SetBrightness3 DDI call with a different BrightnessValue
    if brightness_val_in_nits_after_event is not False:
        logging.info(
            "Brightness Value given by OS after performing %s event is %s" % (event,brightness_val_in_nits_after_event))
        if brightness_val_in_nits_after_event == brightness_in_context:
            logging.info(
                "BrightnessValueInNits %s AFTER performing %s event is MATCHING BrightnessValueInNits %s in Context" % (brightness_val_in_nits_after_event, event, brightness_in_context))
        else:
            logging.error(
                "BrightnessValueInNits %s AFTER performing %s event is NOT MATCHING BrightnessValueInNits %s in Context" % (
                brightness_val_in_nits_after_event, event, brightness_in_context))
            return False
    else:
        logging.info("No new Brightness value, using the BrightnessValue already in context %s" % brightness_in_context)
        brightness_val_in_nits_after_event = brightness_in_context
    ##
    # Get the SDRWhiteLevel value from OS again
    sdr_white_level_after_event = color_parse_etl_events.get_sdr_white_level_from_etl(target_id)
    if sdr_white_level_after_event is False:
        logging.info(
            "No new SDRWhiteLevel, hence will be using the LUT already available in the context %s" % sdr_white_level_in_context)
        sdr_white_level_after_event = sdr_white_level_in_context
    else:
        if sdr_white_level_after_event == sdr_white_level_in_context:
            logging.info(
                "SDRWhiteLevelInNits : %s AFTER performing %s event is MATCHING SDRWhiteLevelInNits : %s in Context" % (
                sdr_white_level_after_event, event, sdr_white_level_in_context))
        else:
            logging.error(
                "BrightnessValueInNits : %s AFTER performing %s event is NOT MATCHING BrightnessValueInNits : %s in Context" % (
                    brightness_val_in_nits_after_event, event, brightness_in_context))
            return False

    pixel_boost_after_event = brightness_val_in_nits_after_event / sdr_white_level_after_event
    logging.info("PixelBoost value after performing %s event is %s" % (event, pixel_boost_after_event))

    if color_common_utility.fetch_ref_hdr_gamma_and_programmed_gamma_and_compare(platform, current_pipe,
                                                        os_relative_lut_after_event,
                                                        color_common_constants.OS_RELATIVE_LUT_SIZE,pixel_boost=pixel_boost_after_event) is False:
        return False
    return True


##
# Interface used by the test cases to Set the Brightness Slider level.
# The function invokes the respective ETL parsing functions for each of the components(OSRelativeLUT, Brightness, SDRWhiteLevel)
# Invokes the function to generate reference LUT, Programmed LUT and performs verification.
# Function returns the result, brightness_val_in_context, sdr_white_level_in_context, os_relative_lut_in_context
def set_and_verify_brightness3_for_a_slider_level(platform, current_pipe, target_id, brightness_level, os_relative_lut):
    brightness_val_in_nits = 0
    sdr_white_level_in_nits = 0
    ##
    # Set the OS Brightness Slider to the level iterating through the list
    color_common_utility.set_os_brightness(brightness_level, delay=0)

    ##
    # Due to smooth brightness, the brightness change will be applied in phases depending on the Transition time and the active RR.
    # Currently OS is giving the Transition time as 200ms, hence waiting with a buffer added to it as 500ms
    time.sleep(0.005)

    brightness_level = "Setting_Brightness_level_to_" + str(brightness_level) + "_" + "TimeStamp_"
    brightness_file_path = color_common_utility.stop_etl_capture(brightness_level)
    if etl_parser.generate_report(brightness_file_path) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False, brightness_val_in_nits, sdr_white_level_in_nits
    else:
        ##
        # Note : Currently there are no APIs to set the SDRWhiteLevel Slider.
        #        Hence considering only the default value given by OS.
        sdr_white_level_in_nits = color_parse_etl_events.get_sdr_white_level_from_etl(target_id)
        if sdr_white_level_in_nits is False:
            return False, brightness_val_in_nits, sdr_white_level_in_nits

        logging.info("SDRWhiteLevel is %s" % sdr_white_level_in_nits)

        brightness_val_in_nits = color_parse_etl_events.get_brightness3_in_nits_from_etl(target_id)
        if brightness_val_in_nits is False:
            return False, brightness_val_in_nits, sdr_white_level_in_nits
        else:
            logging.info("BrightnessValueInNits is %s" % brightness_val_in_nits)
            pixel_boost = brightness_val_in_nits / sdr_white_level_in_nits
            logging.info("Pixel Boost Value is %s" % pixel_boost)

            if color_common_utility.fetch_ref_hdr_gamma_and_programmed_gamma_and_compare(platform, current_pipe, os_relative_lut,
                                                                                color_common_constants.OS_RELATIVE_LUT_SIZE, pixel_boost=pixel_boost) is False:
                return False, brightness_val_in_nits, sdr_white_level_in_nits
    return True, brightness_val_in_nits, sdr_white_level_in_nits