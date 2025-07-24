##################################################################################################################################
# @file              audio_endpoint_basic.py
# @brief             Verifies audio endpoint enumeration and audio register programming for each display. AudioEndpointBasic contains the functions which verifies audio codec and controller D3 state and also verifies audio endpoints and VDSC for all connected displays.
# @details           Test scenario:
#                                 1. Boot the system with edp
#                                 2. Hotplug external panel
#                                 3. Verify audio codec/controller D3 state.
#                                 4. Verify audio endpoints
#                                 5. Sample command line: audio_endpoint_basic.py -edp_a
# @author            Sridharan.V, Kumar, Rohit
################################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @class AudioEndpointBasic
# @brief Verify audio endpoint enumeration and audio register programming
class AudioEndpointBasic(AudioEndpointBase):

    ##
    # @brief Contains Audio Basic test steps
    # @return None
    def runTest(self):

        # Set the test name for logging
        self.test_name = "Audio Basic Test"
        self.is_test_step = True

        ##
        # Step: Get the current topology
        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        if self.d3_controller is True:
            self.verify_audio_codec_d3_state()
            self.verify_audio_controller_d3_state()

        elif self.d3_codec is True:
            self.verify_audio_codec_d3_state()

        # Apply Max mode so that VDSC can be enabled
        if self.vdsc_status is True:
            self.apply_max_mode_for_all_displays()

        # Set display configuration as single for each display and verify audio endpoints
        for display in self.display_list:
            display_port = list(display.keys())[0]
            display_port = (display[display_port]['connector_port'])
            ##
            # Step: Set and verify display configuration using set_display_config()<br>
            self.set_display_config(display_list=[display_port], topology=enum.SINGLE)

            # Verify vdsc if the status is True
            if self.vdsc_status is True:
                self.verify_vdsc_audio()

            ##
            # Step: Verify that the audio endpoints are enumerated correctly using verify_audio_endpoints()<br>
            self.verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
