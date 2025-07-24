#######################################################################################################################
# @file            audio_sst_tiled_verification.py
# @brief           Verifies audio endpoint and playback with tiled display covering multiple user scenarios which
#                  includes hotplug_unplug, power_event, mode set
# @details         Sample command line: audio_sst_tiled_verification.py -edp_a -dp_b_B DELL_U2715_M.EDID
#                                       DELL_U2715_DPCD.bin -dp_d DELL_U2715_S.EDID -config clone
# @author          Nivetha B
#######################################################################################################################
import sys
import logging
import unittest
from operator import attrgetter
from Libs.Core import enum, display_power
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_audio import DisplayAudio
from Tests.Audio.EndpointVerification.audio_endpoint_base import AudioEndpointBase
from Tests.Display_Port.DP_Tiled.display_port_base import DisplayPortBase


##
# @brief Verify audio endpoint and playback with tiled display
class AudioSSTTiledVerification(DisplayPortBase):
    sst_base = DisplayPortBase()
    audio = AudioEndpointBase()

    ##
    # @brief            Unittest runTest function which plugs tiled display and verifies various user
    #                   scenarios to test tiled and audio functionality
    # @return           void
    def runTest(self):
        logging.info('{:*^80}'.format('AUDIO SST TILED TEST STARTS'))
        # Plug tiled display
        self.sst_base.tiled_display_helper(action="Plug")
        # Set display configuration
        self.set_config(self.config)
        # Set tiled max mode
        self.sst_base.apply_tiled_max_modes()
        # Verify audio functions
        self.verify_audio()
        self.verify_power_events()
        self.verify_unplug_plug()
        self.verify_modeset()
        self.verify_codec_controller_d3()
        logging.info('{:*^80}'.format('AUDIO SST TILED TEST ENDS'))

    ##
    # @brief        Verifies endpoint and playback after power event
    # @return       None
    def verify_power_events(self):
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION STARTS'))
        # Invoke power event S3
        self.power_event(display_power.PowerEvent.S3, resume_time=30)
        self.sst_base.apply_tiled_max_modes()
        # Verify audio functions
        self.verify_audio()
        # Invoke power event S4
        self.power_event(display_power.PowerEvent.S4, resume_time=30)
        self.sst_base.apply_tiled_max_modes()
        # Verify audio functions
        self.verify_audio()
        logging.info('{:*^60}'.format('POWER EVENT VERIFICATION ENDS'))

    ##
    # @brief        Verifies endpoint and playback after unplug/hotplug of tiled display
    # @return       None
    def verify_unplug_plug(self):
        logging.info('{:*^60}'.format('UNPLUG_PLUG VERIFICATION STARTS'))
        self.tiled_display_helper(action="UNPLUG")
        self.verify_audio()
        self.tiled_display_helper(action="PLUG")
        self.sst_base.apply_tiled_max_modes()
        self.verify_audio()
        logging.info('{:*^60}'.format('UNPLUG_PLUG VERIFICATION ENDS'))

    ##
    # @brief        Verifies endpoint and playback after applying each mode
    # @return       None
    def verify_modeset(self):
        logging.info('{:*^60}'.format('MODESET VERIFICATION STARTS'))
        config = self.display_config.get_current_display_configuration()
        for index in range(config.numberOfDisplays):
            tiled_info_list = []
            tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index]
                                                                        .displayAndAdapterInfo)
            ##
            # Check for tiled status
            if tile_info.TiledStatus is True:
                tiled_info_list.append(config.displayPathInfo[index].displayAndAdapterInfo)
                ##
                # supported_modes_tiled[] is a list of modes supported by the tiled display
                supported_mode_dict = self.display_config.get_all_supported_modes(tiled_info_list)
                ##
                # tile_modes_list[] is a list of modes supported by the tiled display
                if self.ma_flag:
                    tile_modes_list = supported_mode_dict[(config.displayPathInfo[
                                                               index].DisplayAndAdapterInfo.adapterInfo.gfxIndex,
                                                           config.displayPathInfo[index].targetId)]
                else:
                    tile_modes_list = supported_mode_dict[config.displayPathInfo[index].targetId]
                ##
                # tile_maximum_resolution is the maximum resolution of the tiled display taken form the tile_modes_list
                tile_modes_list = sorted(tile_modes_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                tile_maximum_resolution = tile_modes_list[len(tile_modes_list) - 1]
                ##
                # Check whether the resolution from list of modes is equal to the resolution from the tiled edid
                self.tiled_edid_hz_res = tile_info.HzRes
                self.tiled_edid_vt_res = tile_info.VtRes

                is_tiled_max_mode_enumerated = (self.tiled_edid_hz_res == tile_maximum_resolution.HzRes)
                is_tiled_max_mode_enumerated &= (self.tiled_edid_vt_res == tile_maximum_resolution.VtRes)

                if is_tiled_max_mode_enumerated or self.config == 'CLONE':

                    self.set_display_mode(supported_mode_dict)
                    ##
                    # Since all displays will be active in clone mode (including non-tiled), skipping clone mode
                    # verification since tiled will not be applicable for all displays
                    if self.config != 'CLONE':
                        flag_list = self.verify_port_sync_enable()
                        for index in range(len(flag_list)):
                            adapter = "gfx_" + str(index)
                            if flag_list[index] is True:
                                logging.info("Port Sync enabled for {}".format(adapter))
                            else:
                                logging.error(
                                    "[Driver Issue]: Port Sync is not enabled for {}. Exiting .....".format(adapter))
                                gdhm.report_driver_bug_audio(
                                    title="[Audio] Port Sync is not enabled for {}. Exiting .....".format(adapter))
                                self.fail()

                else:
                    logging.error(
                        "[Driver Issue]: Modes enumerated by the Graphics driver not matching with modes in EDID")
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Modes enumerated by the Graphics driver not matching with modes in EDID")
                    self.fail()
        logging.info('{:*^60}'.format('MODESET VERIFICATION ENDS'))

    ##
    # @brief        Set display modes
    # @param[in]    supported_modes_dict: Dictionary
    #                    supported_modes_dict is a dictionary of supported modes
    # @return       None
    def set_display_mode(self, supported_modes_dict):
        for target_id, mode_list in supported_modes_dict.items():
            s_mode_list = sorted(mode_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
            modes_to_apply = (s_mode_list[0], s_mode_list[len(s_mode_list) // 2], s_mode_list[-1])

            for mode in modes_to_apply:
                ##
                # Apply the mode having the maximum resolution and different refresh rates
                modes_flag = self.display_config.set_display_mode([mode])
                if modes_flag is False:
                    logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                    ##
                    # Gdhm bug reporting handled in display_config.set_display_mode
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Failed to apply display mode. Exiting ...")
                    self.fail()
                else:
                    config = self.display_config.get_current_display_configuration()
                    for index in range(config.numberOfDisplays):
                        current_mode = self.display_config.get_current_mode(config.displayPathInfo[index]
                                                                            .displayAndAdapterInfo)
                        if mode == current_mode:
                            logging.info("Current mode is same as Requested mode")
                        else:
                            enumerated_displays = self.display_config.get_enumerated_display_info()
                            logging.error(f"Targeted mode is not matching with the current mode. \nCurrent mode is : "
                                          f"{current_mode.to_string(enumerated_displays)} \nTargeted mode is: {mode}")
                            gdhm.report_driver_bug_audio(
                                title="[Audio] Targeted mode is not matching with the current mode. "
                                      "\nCurrent mode is : "
                                      f"{current_mode.to_string(enumerated_displays)} \nTargeted mode is: {mode}")
                            self.fail()
                self.verify_audio()

    ##
    # @brief        Verifies endpoint and playback after codec and controller D3
    # @return       None
    def verify_codec_controller_d3(self):
        logging.info('{:*^60}'.format('D3 VERIFICATION STARTS'))
        # Enable Simulated Battery
        if self.display_power.enable_disable_simulated_battery(True) is False:
            gdhm.report_driver_bug_audio(
                title="[Audio] Failed to enable simulated battery")
            self.fail("\tFailed to enable simulated battery")
        else:
            self.is_simbatt_enabled = True
        # Set power line status as DC
        self.audio.set_power_line()
        self.audio.verify_audio_endpoints()
        self.audio.verify_audio_codec_d3_state()
        self.audio.verify_audio_controller_d3_state()
        self.verify_audio()
        self.audio.verify_audio_codec_d3_state()
        self.audio.verify_audio_controller_d3_state()
        logging.info('{:*^60}'.format('D3 VERIFICATION STARTS'))

    ##
    # @brief        Verifies Audio endpoint and playback
    # @return       None
    def verify_audio(self):
        display_info = []
        # Verify audio driver and endpoint
        self.audio.verify_audio_driver()
        self.audio.verify_audio_endpoints()
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
