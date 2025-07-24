################################################################################################################################
# @file            audio_endpoint_property_page_verification.py
# @brief           Verify audio property page data for each display
# @details         Sample command line: audio_endpoint_property_page_verification.py -edp_a -hdmi_b -dp_c -config clone
# @author          Sridharan.V, Kumar, Rohit
################################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @brief Verify audio property page data for each display
class AudioEndpointPropertyPageVerification(AudioEndpointBase):

    ##
    # @brief runtest
    # @return None
    def runTest(self):

        # Set the test name for logging
        self.test_name = "Audio Property Page Verification Test"
        self.is_test_step = True

        # Step: Get the current topology print_current_topology()<br>
        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        # Set Display Configuration
        self.set_display_config()

        if self.enumerated_displays.Count < 1:
            self.fail("No enumerated display found")

        for enumerated_display in self.enumerated_displays.ConnectedDisplays:

            # If display is active and audio capable verify the property page details one by one for each display
            if enumerated_display.IsActive is True:
                display_id = enumerated_display.TargetID
                display_name = enumerated_display.FriendlyDeviceName
                edid_supported_formats = []
                property_page_supported_formats = []

                # Get EDID Data for enumerated display
                edid_data = self.display_audio.get_edid_data(display_id)
                if edid_data is None:
                    gdhm.report_test_bug_audio(
                        title="[Audio] Failed to get EDID data for {0}".format(display_name))
                    self.fail("Failed to get EDID data for {0}".format(display_name))

                # Get Property Page details for enumerated display
                property_page_details = self.display_audio.get_property_page_details(display_name)
                if property_page_details is None:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Failed to get Property Page Details for {0}".format(display_name))
                    self.fail("Failed to get Property Page Details for {0}".format(display_name))

                logging.info("EDID data from panel {0}".format(display_name))
                logging.info("{0} endpoint supports maximum {1} channels in EDID".format(display_name,
                                                                                         edid_data.MaxNumberOfChannels))

                # Supported formats in EDID
                for audio_format_index in range(0, edid_data.NumFormats):
                    audio_format = [edid_data.AudFormat[audio_format_index].BitDepth,
                                    edid_data.AudFormat[audio_format_index].SampleRate]
                    if edid_data.AudFormat[
                        audio_format_index].BitDepth != 20 and audio_format not in edid_supported_formats:
                        edid_supported_formats.insert(audio_format_index, audio_format)

                logging.info("{0} endpoint supported formats in EDID:".format(display_name))
                for audio_format in edid_supported_formats:
                    logging.info("{0}-bits, {1} Hz".format(audio_format[0], audio_format[1]))

                logging.info("{0} Property Page Details".format(display_name))
                logging.info("{0} endpoint supports maximum {1} channels in property page".format(display_name,
                                                                                                  property_page_details.MaxNumberOfChannels))

                # Supported formats in Property Page
                for audio_format_index in range(0, property_page_details.NumFormats):
                    audio_format = [property_page_details.AudFormat[audio_format_index].BitDepth,
                                    property_page_details.AudFormat[audio_format_index].SampleRate]
                    if property_page_details.AudFormat[
                        audio_format_index].BitDepth != 20 and audio_format not in property_page_supported_formats:
                        property_page_supported_formats.insert(audio_format_index, audio_format)

                logging.info("{0} endpoint supported formats in property page:".format(display_name))
                for audio_format in property_page_supported_formats:
                    logging.info("{0}-bits, {1} Hz".format(audio_format[0], audio_format[1]))

                if edid_data.MaxNumberOfChannels == property_page_details.MaxNumberOfChannels:
                    logging.info("Channel verification passed successfully")
                else:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Channel verification failed")
                    self.fail("Channel verification failed")

                for edid_audio_format in edid_supported_formats:
                    if edid_audio_format not in property_page_supported_formats:
                        gdhm.report_driver_bug_audio(
                            title="[Audio] ({0}-bits,{1} Hz) is not found in Property Page Details"
                            .format(edid_audio_format[0], edid_audio_format[1]))
                        self.fail("({0}-bits,{1} Hz) is not found in Property Page Details".format(edid_audio_format[0],
                                                                                                   edid_audio_format[
                                                                                                       1]))

                for property_page_audio_format in property_page_supported_formats:
                    if property_page_audio_format not in edid_supported_formats:
                        gdhm.report_driver_bug_audio(
                            title="[Audio] ({0}-bits,{1} Hz) is not found in EDID Data"
                            .format(property_page_audio_format[0], property_page_audio_format[1]))
                        self.fail("({0}-bits,{1} Hz) is not found in EDID Data".format(property_page_audio_format[0],
                                                                                       property_page_audio_format[1]))

                logging.info("Supported Format verification passed successfully")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
