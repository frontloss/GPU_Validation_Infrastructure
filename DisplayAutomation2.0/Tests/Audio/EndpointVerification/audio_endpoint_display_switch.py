################################################################################################################################
# @file            audio_endpoint_display_switch.py
# @brief           Verify audio endpoint enumeration and audio register programming for each display after display switch
# @details         Test scenario:
#                               1. Boot the system with edp
#                               2. Connect external panels
#                               3. Apply config from command line and perform display switching for all connected panels
#                               4. Sample command line: audio_endpoint_display_switch.py -edp_a -hdmi_b -dp_c
# @author Sridharan.V, Kumar, Rohit
################################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *
from Libs.Core.Verifier.common_verification_args import VerifierCfg

##
# @class AudioEndpointDisplaySwitch
# @brief  Verifies audio endpoint enumeration and audio register programming
class AudioEndpointDisplaySwitch(AudioEndpointBase):

    ##
    # @brief Contains Audio Display Switch test steps
    # @return None
    def runTest(self):

        # Set the test name for logging
        if self.power_event_status is True and self.d3_status is True:
            self.test_name = "Audio Codec Display Switch After {0} with D3 Test".format(self.power_event_str)
        if self.power_event_status is False and self.d3_status is True:
            self.test_name = "Audio Codec Display Switch with D3 Test"
        if self.power_event_status is True and self.d3_status is False:
            self.test_name = "Audio Display Switch After {0} Test".format(self.power_event_str)
        if self.power_event_status is False and self.d3_status is False:
            self.test_name = "Audio Display Switch Test"

        self.is_test_step = True

        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        connected_displays = []
        temp_displays = []
        for display in self.display_list:
            display_port = list(display.keys())[0]
            display_port = (display[display_port]['connector_port'])
            connected_displays.append(display_port)
            if self.mst_status is True:
                if self.mst_displays < 2 and len(display_port) < 2:
                    gdhm.report_test_bug_audio(
                        title="[Audio] Display Switch test case needs minimum 2 displays")
                    self.fail("Display Switch test case needs minimum 2 displays")
            else:
                if len(display_port) < 2:
                    gdhm.report_test_bug_audio(
                        title="[Audio] Display Switch test case needs minimum 2 displays")
                    self.fail("Display Switch test case needs minimum 2 displays")

        if self.power_event_status is True:
            # Invoke power event
            self.base_invoke_power_event(power_event=self.power_event_type, is_mto=self.power_event_mto)

        self.config_list = display_utility.get_possible_configs(connected_displays)
        for config, display_list in self.config_list.items():
            topology = eval("%s" % config)

            # Avoids repeated configurations from the display list
            if config != "enum.SINGLE":
                for displays in display_list:
                    sorted_display = sorted(displays, key=lambda x: x[-1])
                    if len(self.display_list) == len(sorted_display):
                        if sorted_display not in temp_displays:
                            temp_displays.append(sorted_display)
                display_list = temp_displays

            for displays in display_list:
                if self.d3_controller is True:
                    self.verify_audio_codec_d3_state()
                    self.verify_audio_controller_d3_state()
                elif self.d3_codec is True:
                    self.verify_audio_codec_d3_state()

                # Step: Set all the possible Display Configurations one by one
                self.set_display_config(display_list=displays, topology=topology)

                # Verify vdsc if the status is True
                if self.vdsc_status is True:
                    self.apply_max_mode_for_all_displays()
                    if config == "enum.SINGLE":
                        self.verify_vdsc_audio_single(displays)
                    else:
                        self.verify_vdsc_audio()

                # Step: Verify that the audio endpoints are enumerated correctly for each display configuration
                self.verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
