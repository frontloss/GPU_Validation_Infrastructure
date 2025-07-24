################################################################################################################################
# @file                audio_endpoint_tdr.py
# @brief               Verify audio endpoint enumeration and audio register programming for each display before and after TDR
# @details             Test scenario:
#                                   1. Boot the system with edp
#                                   2. Hotplug external panels
#                                   3. Verify endpoints after TDR.
#                                   4. Sample command line: audio_endpoint_tdr.py -edp_a -hdmi_b -dp_c -config clone
# @author              Sridharan.V, Kumar, Rohit
################################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @class AudioEndpointTDR
# @brief contains helper functions to verify audio endpoint enumeration and audio register programming
class AudioEndpointTDR(AudioEndpointBase):

    ##
    # @brief Contains Audio TDR test steps
    # @return None
    def runTest(self):
        lfp_present = False
        # Set the test name for logging
        self.test_name = "Audio TDR Test"
        self.is_test_step = True

        # Step: Get the current topology print_current_topology()<br>
        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        # Step: Verify that the audio endpoints are enumerated correctly before TDR
        self.verify_audio_endpoints()

        # Step: Generate & Verify TDR
        logging.info("Step{0}: Generating TDR".format(self.step_counter))
        self.step_counter += 1
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))

        if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
            self.fail('Failed to generate TDR')

        if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
            logging.info('\tTDR generated successfully')

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully post TDR generation")

        # Step: Verify that the audio endpoints are enumerated correctly after TDR
        self.verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
