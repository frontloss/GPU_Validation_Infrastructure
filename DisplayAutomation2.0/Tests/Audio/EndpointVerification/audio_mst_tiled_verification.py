#######################################################################################################################
# @file            audio_mst_tiled_verification.py
# @brief           Verifies audio endpoint and playback with MST tiled display covering multiple user scenarios which
#                  includes hotplug_unplug, power_event, codec controller D3
# @details         Sample command line: audio_mst_tiled_verification.py -edp_a -dp_b -plug_topologies
#                                       MST_TILED_1 -config single
# @author          Nivetha B
#######################################################################################################################
import logging
import sys
import unittest

from Libs.Core import enum, display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_audio import DisplayAudio
from Tests.Audio.EndpointVerification.audio_endpoint_base import AudioEndpointBase
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase



##
# @brief Verify audio endpoint and playback with MST tiled display
class AudioMSTTiledVerification(DisplayPortMSTBase):
    mst_base = DisplayPortMSTBase()
    audio_base = AudioEndpointBase()
    topology_type = None
    port_type = None
    xml_file = None

    ##
    # @brief            Unittest runTest function which plugs MST tiled display and verifies various user scenarios to
    #                   test tiled and audio functionality
    # @return           void
    def runTest(self):
        logging.info('{:*^80}'.format('AUDIO MST TILED TEST STARTS'))
        dp_port_index = 0
        self.mst_base.process_cmdline()
        # Requested ports should be present in free port list
        if not set(self.mst_base.dp_ports_to_plug).issubset(set(self.free_port_list)):
            self.fail("Not Enough free ports available. Exiting")

        # Get the port type from available free DP ports
        self.port_type = self.mst_base.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type from the command line
        self.topology_type = self.mst_base.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        self.xml_file = self.mst_base.get_xmlfile(dp_port_index)

        # Tiled Display is being plugged in - MST Tiled Display.
        self.mst_base.set_tiled_mode(self.port_type, self.topology_type, self.xml_file)

        # Set display config and apply max mode
        self.mst_base.set_config_apply_max_mode()

        # Get tiled displays list.
        is_tiled_display, tiled_target_ids_list = self.mst_base.get_tiled_displays_list()
        logging.info("Tiled Display List {}".format(tiled_target_ids_list))

        # Verify if the display is detected as Tiled Display - MST Tiled Display and apply tiled mode
        if is_tiled_display:
            self.mst_base.verify_tiled_display(True, True, True, tiled_target_ids_list[0])
        else:
            self.fail("MST Tiled display not found")

        # Verify audio functions
        self.verify_audio()
        self.verify_power_events()
        self.verify_unplug_plug()
        self.verify_codec_controller_d3()
        self.unplug_panel_plug_branch()
        logging.info('{:*^80}'.format('AUDIO MST TILED TEST ENDS'))

    ##
    # @brief        Verifies endpoint and playback after power event
    # @return       None
    def verify_power_events(self):
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION STARTS'))
        # Invoke power event S3
        self.power_event(display_power.PowerEvent.S3, resume_time=30)
        self.mst_base.set_config_apply_max_mode()
        # Verify audio functions
        self.verify_audio()
        # Invoke power event S4
        self.power_event(display_power.PowerEvent.S4, resume_time=30)
        self.mst_base.set_config_apply_max_mode()
        # Verify audio functions
        self.verify_audio()
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION ENDS'))

    ##
    # @brief        Verifies endpoint and playback after unplug/hotplug of MST tiled display
    # @return       None
    def verify_unplug_plug(self):
        logging.info('{:*^50}'.format('UNPLUG PLUG OF FULL TOPOLOGY VERIFICATION STARTS'))
        self.mst_base.set_hpd(self.port_type, False)
        self.verify_audio()
        # Tiled Display is being plugged in - MST Tiled Display and apply tiled mode
        self.mst_base.set_tiled_mode(self.port_type, self.topology_type, self.xml_file)
        self.mst_base.set_config_apply_max_mode()
        self.verify_audio()
        logging.info('{:*^50}'.format('UNPLUG PLUG OF FULL TOPOLOGY VERIFICATION ENDS'))

    ##
    # @brief        Verifies endpoint and playback by unplugging panel and plug of branch
    # @return       None
    def unplug_panel_plug_branch(self):
        logging.info('{:*^40}'.format('UNPLUG PANEL AND PLUG OF BRANCH VERIFICATION STARTS'))
        # Get the RAD Information
        rad = self.get_topology_rad(self.port_type)
        self.set_partial_topology(self.port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None)
        self.verify_audio()
        logging.info('{:*^40}'.format('UNPLUG PANEL AND PLUG OF BRANCH VERIFICATION ENDS'))

    ##
    # @brief        Verifies endpoint and playback after codec and controller D3
    # @return       None
    def verify_codec_controller_d3(self):
        logging.info('{:*^60}'.format('D3 VERIFICATION STARTS'))
        # Enable Simulated Battery
        if self.display_power.enable_disable_simulated_battery(True) is False:
            self.fail("\tFailed to enable simulated battery")
        else:
            self.is_simbatt_enabled = True
        # Set power line status as DC
        self.audio_base.set_power_line()
        self.audio_base.verify_audio_endpoints()
        self.audio_base.verify_audio_codec_d3_state()
        self.audio_base.verify_audio_controller_d3_state()
        self.verify_audio()
        self.audio_base.verify_audio_codec_d3_state()
        self.audio_base.verify_audio_controller_d3_state()
        logging.info('{:*^60}'.format('D3 VERIFICATION ENDS'))

    ##
    # @brief        Verifies Audio endpoint and playback
    # @return       None
    def verify_audio(self):
        display_info = []
        # Verify audio driver and endpoint
        self.audio_base.verify_audio_driver()
        self.audio_base.verify_audio_endpoints()
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays.Count != 0:
            for i in range(enumerated_displays.Count):
                if enumerated_displays.ConnectedDisplays[i].IsActive is True:
                    display_adapter_info = enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo
                    if DisplayAudio().is_audio_capable(display_adapter_info):
                        display_info.append(enumerated_displays.ConnectedDisplays[i])
        endpoint_name_list = DisplayAudio().get_audio_endpoint_name(only_unique_endpoint=False)
        for display in display_info:
            for endpoint_name in endpoint_name_list:
                status = DisplayAudio().audio_playback_verification(display_info=display,
                                                                    end_point_name=endpoint_name)
                if status:
                    logging.info(f"\tPass: Audio Playback Verification success for {endpoint_name}")
                else:
                    self.assertTrue(endpoint_name, 'Audio playback verification failed')
            break


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
