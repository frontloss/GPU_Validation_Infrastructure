#######################################################################################################################
# @file         edp_hdr_brightness3_with_video_playback.py
# @addtogroup   Test_Color
# @section      edp_hdr_brightness3_with_video_playback
# @remarks      @ref edp_hdr_brightness3_with_video_playback.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux) which will be input from the test command line
#                       The script then invokes the API to set the OS Brightness Slider level to 91 level
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Pixel Compensation factor is calculated as BrightnessInNits/SDRWhiteLevelInNits,
#                       both values taken from the ETL.The Input Lut is then multiplied
#                       with the pixel compensation factor and OETF is applied on the input values
#                       which are compared with the programmed pipe gamma values
#                       Test Script launches the video playback in fullscreen and verifies if the Pipe Gamma values
#                       are persisting after the event which implies that the Brightness values are persisting.
# CommandLine:  python os_hdr_basic.py -edp_a SINK_EDP50 -config SINGLE
#               python os_hdr_basic.py -hdmi_b  SamsungJS9500_HDR.bin -config SINGLE
#               python os_hdr_basic.py -dp_b  Benq_SW320.bin  DP_HDR_DPCD.txt -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.Gen11_Flip.MPO3H import HDRConstants
from Tests.Color.HDR.OSHDR.os_hdr_base import  *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class eDPHDRBrightness3WithVideoPlayback(OSHDRBase, eDPHDRBase):

    def runTest(self):

        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Verify HDR Caps
        if super().fetch_and_verify_hdr_caps_from_etl() is False:
            self.fail("Failed verification of HDR caps from ETL")

        ##
        # Enable HDR
        super().toggle_and_verify_hdr(toggle="ENABLE")

        ##
        # Stop the ETL after enabling HDR, to get the SDRWhiteLevel value
        hdr_etl_path = color_common_utility.stop_etl_capture("After_Enabling_HDR_TimeStamp_")
        if etl_parser.generate_report(hdr_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Note : Currently there are no APIs to set the SDRWhiteLevel Slider.
        #        Hence considering only the default value given by OS 80%
        # sdr_white_level = super().get_sdr_white_level_from_etl()
        #if sdr_white_level is False:
        #    logging.error("No SDRWhiteLevel Value available in the ETLs")
        #    self.fail()
        #logging.info("SDRWhiteLevel is %s" % sdr_white_level[1])
        # Hard coding to 80% as default by OS as ETL Event WA
        sdr_white_level = 80
        logging.info("SDRWhiteLevel is %s" % sdr_white_level)

        ##
        # Check Out Brightness App
        brightness_slider_level = 91
        brightness_list = []
        ref_pipe_gamma_lut = []
        color_common_utility.set_os_brightness(brightness_slider_level, delay=0)
        brightness_level = "Setting_Brightness_level_to_" + str(brightness_slider_level) + "_"
        brightness_file_path = color_common_utility.stop_etl_capture(brightness_level)
        if etl_parser.generate_report(brightness_file_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()
        else:
            edp_hdr_brightness3_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_BRIGHTNESS3)
            if edp_hdr_brightness3_data is None:
                logging.error("\tNo DisplayBrightness3 event found in ETLs (OS Issue)")
            else:
                for each_entry_in_brightness3 in range(len(edp_hdr_brightness3_data)):
                    brightness_list.append(edp_hdr_brightness3_data[each_entry_in_brightness3])

                for index1 in range(len(brightness_list)):
                    logging.info("TargetID : %d BrightnessMillinits : %d; TransitionTimeMs : %d" % (
                        brightness_list[index1].TargetId, brightness_list[index1].BrightnessMillinits,
                        brightness_list[index1].TransitionTimeMs))

                    brightness_val_in_nits = brightness_list[index1].BrightnessMillinits / 1000
                    ##
                    # Fetch DPCD and check if the Nits Value is written into the DPCD
                    edp_hdr_utility.verify_dpcd_edp_brightness_nits(self.enumerated_displays)
                    pixel_boost = brightness_val_in_nits / sdr_white_level
                    logging.info("Pixel Boost Value is %s" % pixel_boost)
                    ref_pipe_gamma_lut = edp_hdr_utility.generate_reference_pipe_gamma_lut_with_pixel_boost(
                        HDRConstants.INPUT_3SEGMENT_LUT_524Samples_8_24FORMAT, pixel_boost)
                    logging.debug("Reference Pipe Gamma LUT")
                    logging.debug(ref_pipe_gamma_lut)

                    ##
                    # Since the brightness is applied in phases, it takes 12 frames for the target slider value
                    # to be applied which will be 200ms given by OS and also depends on the ActiveRR
                    time.sleep(0.005)
                    ##
                    # Read the programmed Gamma values and compare the reference and the programmed values
                    if edp_hdr_utility.fetch_and_verify_gamma_registers_for_edp_hdr(self.connected_list,
                                                                                    ref_pipe_gamma_lut,
                                                                                    self.platform) is False:
                        logging.error("Failed the verification of gamma programmed registers for EDP HDR")
                        self.fail("Failed the verification of gamma programmed registers for EDP HDR")

        ##
        # Launch the video_playback
        if color_common_utility.video_play_back(is_full_screen=True) is False:
            self.fail("Failed to launch media application")
        else:
            ##
            # Read the programmed Gamma values and compare the reference and the programmed values
            if edp_hdr_utility.fetch_and_verify_gamma_registers_for_edp_hdr(self.connected_list,
                                                                            ref_pipe_gamma_lut,
                                                                            self.platform) is False:
                logging.error("Failed the verification of programmed gamma register for EDP HDR")
                self.fail("Failed the verification of programmed gamma register for EDP HDR")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
