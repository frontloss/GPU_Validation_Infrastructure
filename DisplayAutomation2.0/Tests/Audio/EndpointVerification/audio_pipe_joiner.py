#######################################################################################################################
# @file         audio_pipe_joiner.py
# @brief        Test to check Uncompressed pipe joiner programming and audio for the plugged display with the max mode.
# @details      Test Scenario:
#               1. Plugs the displays, Applies the Extended mode if more than one display is connected else SINGLE
#               2. Applies max mode for each of the display in the topology and verify audio endpoint and playback.
#               3. Verifies uncompressed pipe joiner programming for each of the pipe joined display in the topology.
#               This test should have at least one DP panel with higher resolution.
#               4. Sample command: Tests\Audio\EndpointVerification\audio_pipe_joiner.py
#                                   -DP_F 8k_30hz_16bpc.bin HBR3_DPCD.txt
#
# @author       Nivetha B
#######################################################################################################################

from typing import List
from typing import Iterator

from Libs.Core.display_config import display_config_enums
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.display_config.display_config_struct import DisplayInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_audio import DisplayAudio
from Tests.Display_Port.DP_Pipe_Joiner.pipe_joiner_base import PipeJoinerBase
from Tests.Audio.EndpointVerification.audio_endpoint_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class AudioPipeJoinerTest(AudioEndpointBase):
    config_to_apply = None

    ##
    # @brief Contains Audio Basic test steps
    # @return None
    def runTest(self):
        lfp_present = False
        logging.info('{:*^80}'.format('AUDIO PIPEJOINER VERIFICATION TEST STARTS'))
        self.print_current_topology()
        # verify audio endpoints and playback
        self.verify_audio()
        # set max mode and verify pipe joiner
        self.set_max_and_verify_pipejoiner()
        # Verify pipe joiner after unplug/plug of displays
        self.verify_unplug_plug()
        # Verify pipe joiner after power event
        if self.power_event:
            self.verify_power_event()
        # Verify codec and controller D3 state
        self.verify_codec_controller_d3()

    ##
    # @brief        Set max mode supported and verify pipe joiner
    # @return       None
    def set_max_and_verify_pipejoiner(self):
        external_display_info_list: Iterator[DisplayInfo] = PipeJoinerBase.get_external_display_info_list()

        enumerated_displays = self.display_config.get_enumerated_display_info()
        display_adapter_info_list: List[DisplayAndAdapterInfo] = []
        for index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[index]
            if display_utility.get_vbt_panel_type(CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name, 'gfx_0') \
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                display_adapter_info_list.append(display_info.DisplayAndAdapterInfo)

        self.print_current_topology()
        self.verify_audio()

        for display_info in external_display_info_list:
            port_name = display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            gfx_index = display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex
            is_pipe_joiner_required, _ = DisplayClock.is_pipe_joiner_required(gfx_index, port_name)
            if is_pipe_joiner_required is True:
                is_success = PipeJoinerBase.verify_pipe_joined_display(port_name)
                self.assertTrue(is_success, PipeJoinerBase.test_fail_log_template.format(port_name))
                logging.info(PipeJoinerBase.test_success_log_template.format(port_name))
                # verify audio endpoints and playback
                self.verify_audio()

    ##
    # @brief        Verifies Audio endpoint and playback
    # @return       None
    def verify_audio(self):
        # Verify audio driver and endpoint
        self.verify_audio_driver()
        self.verify_audio_endpoints()
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays.Count != 0:
            for i in range(enumerated_displays.Count):
                port = disp_cfg.cfg_enum.CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
                if enumerated_displays.ConnectedDisplays[i].IsActive is True:
                    display_adapter_info = enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo
                    if DisplayAudio().is_audio_capable(display_adapter_info):
                        display = enumerated_displays.ConnectedDisplays[i]
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
                                    if self.multi_channel:
                                        self.verify_multiCh_playback(display=display, port=port,
                                                                     endpoint_name=endpoint_name)
                                    else:
                                        status = DisplayAudio().audio_playback_verification(display_info=display,
                                                                                            end_point_name=endpoint_name
                                                                                            )
                                        if status:
                                            logging.info(
                                                f"\tPass: 2ch 16bit 48KHz -> Audio Playback Verification success for "
                                                f"{endpoint_name}")
                                        else:
                                            self.assertTrue(endpoint_name, 'Audio playback verification failed')

    ##
    # @brief        Verifies endpoint and playback after unplug/hotplug in S4 of display
    # @return       None
    def verify_unplug_plug(self):
        logging.info('{:*^60}'.format('UNPLUG_PLUG VERIFICATION STARTS'))
        plugged_displays_during_test = self.plugged_display[:]
        for display in plugged_displays_during_test:
            self.base_unplug(display)
            self.verify_audio()
        for display in self.display_list:
            display_port = list(display.keys())[0]
            if display[display_port]['is_lfp'] is False and display_port != self.mst_port:
                if disp_cfg.is_display_attached(self.enumerated_displays, display_port,
                                                display[display_port]['gfx_index']) is False:
                    if self.power_event:
                        self.base_hot_plug(display=display, low_power=True, power_event=display_power.PowerEvent.S4,
                                           is_mto=False)
                    else:
                        self.base_hot_plug(display=display)
                    self.set_max_and_verify_pipejoiner()

    ##
    # @brief        Verifies pipejoiner, endpoint and playback after power event
    # @return       None
    def verify_power_event(self):
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION STARTS'))
        # Invoke power event S3
        if self.display_power.invoke_power_event(display_power.PowerEvent.S3, sleep_time=30) is False:
            gdhm.report_driver_bug_os(title=f"[Audio] Failed To Invoke Power Event: {display_power.PowerEvent.S3}")
            self.fail(f'Failed to invoke power event {display_power.PowerEvent.S3}')
        self.set_max_and_verify_pipejoiner()
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION ENDS'))

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
        self.set_power_line()
        self.verify_audio_codec_d3_state()
        self.verify_audio_controller_d3_state()
        self.set_max_and_verify_pipejoiner()
        self.verify_audio_codec_d3_state()
        self.verify_audio_controller_d3_state()
        logging.info('{:*^60}'.format('D3 VERIFICATION ENDS'))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
