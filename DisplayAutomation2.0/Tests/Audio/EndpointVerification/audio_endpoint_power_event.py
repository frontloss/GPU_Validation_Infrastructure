################################################################################################################################
# @file             audio_endpoint_power_event.py
# @brief            Verify audio endpoint enumeration and audio register programming before and after power events (S3/S4/CS/MTO)
# @details          Test scenario:
#                                1. Boot the system with edp
#                                2. Hotplug external panel
#                                3. Invoke power event based on command line
#                                4. Verify endpoints
#                                5. Sample command line: audio_endpoint_power_event.py -edp_a -hdmi_b -dp_c
#                                   -config clone -power_event s3 -d3 codec
# @author           Sridharan.V, Kumar, Rohit
################################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @class AudioEndpointPowerEvent
# @brief Verify audio endpoint enumeration and audio register programming
class AudioEndpointPowerEvent(AudioEndpointBase):

    ##
    # @brief Contains Audio Hot plug Unplug test steps
    # @return None
    def runTest(self):
        lfp_present = False

        # Set the test name for logging
        if self.d3_status is False:
            self.test_name = "Audio {0} Test".format(self.power_event_str)
        else:
            self.test_name = "Audio {0} with D3 Test".format(self.power_event_str)
        self.is_test_step = True

        logging.info("******* {0} Started *******".format(self.test_name))
        for cycle_no in range(self.iterations):

            # Print the cycle number if the number of iterations are more than 1
            if self.iterations > 1:
                logging.info("--------------Test cycle {0}-----------------".format(cycle_no + 1))

            self.print_current_topology()

            # Verify that the audio endpoints are enumerated correctly before power event
            self.verify_audio_endpoints()

            if self.d3_controller is True:
                self.verify_audio_codec_d3_state()
                self.verify_audio_controller_d3_state()
            elif self.d3_codec is True:
                self.verify_audio_codec_d3_state()

            # Invoke power event
            self.base_invoke_power_event(power_event=self.power_event_type, is_mto=self.power_event_mto)


            # Verify vdsc if the status is True
            if self.vdsc_status is True:
                self.apply_max_mode_for_all_displays()
                self.verify_vdsc_audio()

            # Verify that the audio endpoints are enumerated correctly after power event
            self.verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
