#######################################################################################################################
# @file                 hdr_with_audio.py
# @addtogroup           Test_Color
# @section              hdr_with_audio
# @remarks              @ref hdr_with_audio.py \n
#                       The test script enables HDR on eDP_HDR displays,
#                       which is an input parameter from the test command line.
#                       The script can handle both Aux and SDP variety of displays.
#                       The script invokes the API to set the OS Brightness Slider level
#                       to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value
#                       The script then iterates through a list of brightness levels,
#                       performing a stress test.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification; DPCD verification is performed.
#                       In case of Aux based panel, DPCD verification is performed.
# Sample CommandLines:  python hdr_with_audio.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_audio.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Audio.EndpointVerification.audio_endpoint_base import *


class HDRWithAudio(HDRTestBase):
    d3_codec, d3_controller = False, False

    def setUp(self):
        self.custom_tags["-D3"] = None
        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        if 'CODEC' in self.context_args.test.cmd_params.test_custom_tags["-D3"][0]:
            self.d3_codec = True
        if 'CONTROLLER' in self.context_args.test.cmd_params.test_custom_tags["-D3"][0]:
            self.d3_controller = True

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()

        if self.d3_controller is True:
            AudioBase().verify_audio_codec_d3_state()
            AudioBase().verify_audio_controller_d3_state()

        elif self.d3_codec is True:
            AudioBase().verify_audio_codec_d3_state()

        # Verify VDSC if the status is True
        if AudioBase().vdsc_status is True:
            AudioBase().verify_vdsc_audio()

        ##
        # Step: Verify that the audio endpoints are enumerated correctly using verify_audio_endpoints()
        AudioBase().verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
