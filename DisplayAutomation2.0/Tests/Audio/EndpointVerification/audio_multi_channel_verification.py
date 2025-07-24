########################################################################################################################
# @file              audio_multi_channel_verification.py
# @brief             Verifies audio endpoint enumeration and multi-channel playback.
# @details           Test scenario:
#                                 1. Boot the system with edp
#                                 2. Hotplug external panel
#                                 3. Verify audio endpoint enumeration.
#                                 4. Verify audio playback with different sample rates based on command line
#                                 5. Sample command line: audio_multi_channel_verification.py -edp_a -hdmi_b
#                                                         -multi_channel 2c16b
# @author            Nivetha B
########################################################################################################################
import re
import subprocess
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_audio import DisplayAudio
from Tests.Audio.EndpointVerification.audio_endpoint_base import *


##
# @class        AudioMultiChannelVerification
# @brief        Verify audio endpoint enumeration and audio register programming
class AudioMultiChannelVerification(AudioEndpointBase):

    ##
    # @brief Contains Audio Basic test steps
    # @return None
    def runTest(self):
        logging.info('{:*^80}'.format('AUDIO MULTI CHANNEL TEST STARTS'))
        self.print_current_topology()

        # Set display configuration as single for each display and verify audio endpoints and playback
        for display in self.display_list:
            display_port = list(display.keys())[0]
            display_port = (display[display_port]['connector_port'])
            # Set and verify display configuration using set_display_config()
            self.set_display_config(display_list=[display_port], topology=enum.SINGLE)

            VerifierCfg.audio_playback_verification = False
            self.verify_audio_endpoints()

            enum_displays = self.display_config.get_enumerated_display_info()
            for i in range(enum_displays.Count):
                port = disp_cfg.cfg_enum.CONNECTOR_PORT_TYPE(enum_displays.ConnectedDisplays[i].ConnectorNPortType).name
                if enum_displays.ConnectedDisplays[i].IsActive is True:
                    display_adapter_info = enum_displays.ConnectedDisplays[i].DisplayAndAdapterInfo
                    if DisplayAudio().is_audio_capable(display_adapter_info):
                        display = enum_displays.ConnectedDisplays[i]
                        endpoint_name_info = subprocess.check_output([DEVCON_EXE_PATH, "status",
                                                                      "MMDEVAPI\AudioEndpoints"],
                                                                     universal_newlines=True)
                        string = "HD Audio Driver for Display Audio"
                        if re.search(r'Name', endpoint_name_info, re.I):
                            lines = endpoint_name_info.split("\n")
                            for line in range(len(lines)):
                                if (lines[line].find(string)) != -1:
                                    last_index = lines[line].find("(")
                                    endpoint_name = lines[line][10:last_index - 1]
                                    self.verify_multiCh_playback(display=display, port=port, endpoint_name=endpoint_name)




if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
