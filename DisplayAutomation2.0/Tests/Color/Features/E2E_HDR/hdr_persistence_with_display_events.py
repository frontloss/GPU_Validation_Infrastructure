#######################################################################################################################
# @file                 hdr_persistence_with_display_events.py
# @addtogroup           Test_Color
# @section              hdr_persistence_with_display_events
# @remarks              @ref hdr_persistence_with_display_events.py \n
# @brief                This scripts comprises modularized tests, where :
#                       1. test_01_hotplug_unplug() - Intends to verify HDR Persistence with HotUnplug-Plug of displays
#                       2. test_02_mode_switch() - Intends to verify HDR Persistence with various modesets
#                       3. test_03_display_switch() - Intends to verify HDR Persistence with different topologies
#                       4. test_03_video_playback() - Intends to verify HDR with Videoplayback scenario
#                       Each of the test modules perform the following :
#               		The test script enables HDR on the displays supporting HDR,
#               		which is an input parameter from the test command line.
#               		Additionally, for an eDP_HDR display the script invokes the API
#               		to set the OS Brightness Slider level to a value provided in the command line.
#               		If Brightness Slider level has not been given as an input, script sets the slider
#               		to a random value other than the Current Brightness value
#               		Verification Details:
#               		The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#               		Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#               		Pipe_Misc register is also verified for HDR_Mode
#               		Plane and Pipe Verification is performed by iterating through each of the displays
#               		Metadata verification, by comparing the Default and Flip Metadata is performed,
#               		along with register verification
# Sample CommandLines:  python hdr_persistence_with_display_events.py -edp_a SINK_EDP050
#                       -hdmi_b SamsungJS9500_HDR.bin -scenario HOTPLUG_UNPLUG
#                       python hdr_persistence_with_display_events.py -edp_a SINK_EDP050 -scenario MODE_SWITCH
#                       python hdr_persistence_with_display_events.py -edp_a SINK_EDP050 -dp_d -scenario DISPLAY_SWITCH
#                       python hdr_persistence_with_display_events.py -edp_a SINK_EDP050 -dp_d -scenario VIDEO_PLAYBACK
#
# @author       Smitha B
#######################################################################################################################
import random
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import window_helper
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class HDRPersistenceWithDisplayEvents(HDRTestBase):

    @unittest.skipIf(common_utility.get_action_type() != "HOTPLUG_UNPLUG",
                     "Skipped the  test step as the action type is not HOTPLUG_UNPLUG")
    def test_01_hotplug_unplug(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()


        logging.info("*** Step 2 : Perform Unplug of all external panels and verify ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":

                    ##
                    # unplug and verify
                    if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                           panel.port_type):
                        event = "Unplug_Of_" + port
                        for gfx_index, adapter in self.context_args.adapters.items():
                            for port, panel in adapter.panels.items():
                                ##
                                # Update the HDR Caps after performing the Unplug of Display Event
                                color_properties.update_feature_caps_in_context(self.context_args)
                                if self.update_common_color_props_for_all(event) is False:
                                    self.fail()
                                if panel.is_active:
                                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                        self.fail()
                    else:
                        self.fail("Fail : Fail to unplug the port")


        ##
        # Performing Plug of all the unplugged displays
        logging.info("*** Step 3 : Perform Plug of all external panels and verify ***")
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details

        self.plug_display(display_details_list)
        metadata_scenario = color_properties.HDRMetadataScenario()
        metadata_scenario.hotplug = 1
        event = "Plug_Of_All_external_Displays"
        color_properties.update_feature_caps_in_context(self.context_args)
        if self.update_common_color_props_for_all(event) is False:
            self.fail()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                        self.fail()
                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                        self.fail()
        metadata_scenario.hotplug = 0


    @unittest.skipIf(common_utility.get_action_type() != "MODE_SWITCH", "Skipped the test step as the action type is not MODE_SWITCH")
    def test_02_mode_switch(self):
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Perform Mode Switch and verify ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Store the current mode
                    current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                    mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                    if mode_list is None:
                        mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                    for mode in mode_list:
                        common_utility.apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)

                        panel_props = self.panel_props_dict[gfx_index, port]
                        event = "ModeSet_" + str(mode.HzRes) + "X" + str(mode.VtRes) + "@" + str(mode.refreshRate)
                        logging.info(
                            "Updating all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}"
                            " after mode-set event".format(
                                port, gfx_index, panel.pipe))
                        color_properties.update_feature_caps_in_context(self.context_args)
                        if self.update_common_color_props_for_all(event) is False:
                            self.fail()
                        if panel.is_active:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                                self.fail()
                            if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                self.fail()
                    ##
                    # Switch back to the previous current mode
                    common_utility.apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                               current_mode.refreshRate, current_mode.scaling)

                    ##
                    # Verify the registers
                    panel_props = self.panel_props_dict[gfx_index, port]
                    event = "ModeSet_" + str(current_mode.HzRes) + "X" + str(current_mode.VtRes) + "@" + str(current_mode.refreshRate)
                    logging.info(
                        "Updating all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}"
                        " after mode-set event".format(
                            port, gfx_index, panel.pipe))
                    color_properties.update_feature_caps_in_context(self.context_args)
                    if self.update_common_color_props_for_all(event) is False:
                        self.fail()
                    if panel.is_active:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                            self.fail()
                        if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                            self.fail()


    @unittest.skipIf(common_utility.get_action_type() != "DISPLAY_SWITCH",
                     "Skipped the  test step as the action type is not DISPLAY_SWITCH")
    def test_03_display_switch(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        display_list: list = []
        ##
        logging.info("*** Step 2 : Apply different display configs and verify ***")
        # Applying Single Display Config on each of the panels and performing register verification
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                display_list.append(panel.display_and_adapterInfo)
                if panel.is_active and (panel.FeatureCaps.HDRSupport or self.enable_wcg):
                    if common_utility.display_switch(topology=enum.SINGLE,
                                      display_and_adapter_info_list=[panel.display_and_adapterInfo]):
                        logging.info("Pass : Applied {0} config on {1}".format(DisplayConfigTopology(enum.SINGLE).name, port))
                        event = "DispConfig_" + DisplayConfigTopology(enum.SINGLE).name
                        ##
                        # Update the HDR Caps after performing the Unplug of Display Event
                        color_properties.update_feature_caps_in_context(self.context_args)
                        if self.update_common_color_props_for_all(event) is False:
                            self.fail()
                        if panel.is_active:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                                self.fail()
                            if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                self.fail()

        # If commandline topology was Extended then applied config will be Clone
        # If commandline topology was Clone then applied config will be Extended
        logging.info("Topology in context {0}".format(self.test_params_from_cmd_line.topology))
        if display_list.__len__() > 1 and self.test_params_from_cmd_line.topology == enum.SINGLE:
            #if self.test_params_from_cmd_line.topology != 1:
            topology = enum.CLONE if self.test_params_from_cmd_line.topology == 3 else enum.EXTENDED

            if common_utility.display_switch(topology, display_list):
                logging.info("Pass : Applied {0} config".format(DisplayConfigTopology(topology).name))
                event = "DispConfig_" + DisplayConfigTopology(topology).name
                ##
                # Update the HDR Caps after performing the Unplug of Display Event
                color_properties.update_feature_caps_in_context(self.context_args)
                if self.update_common_color_props_for_all(event) is False:
                    self.fail()
                if topology == enum.CLONE:
                    for gfx_index, adapter in self.context_args.adapters.items():
                        for port, panel in adapter.panels.items():
                            if panel.is_active:
                                if panel.FeatureCaps.HDRSupport:
                                    if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                                        logging.error("FAIL : HDR Enable Status in CLONE config - Expected {0}; Actual {1} on {2} on pipe {3}".format("DISABLE", "ENABLE", port, panel.pipe))
                                        self.fail()
                                    logging.info("PASS : HDR Enable Status in CLONE config - Expected {0}; Actual {1} on on {2} on pipe {3}".format("DISABLE", "DISABLE", port, panel.pipe))
                                else:
                                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                        self.fail()

                    ##
                    # Switching back to Extended Config
                    topology = enum.EXTENDED
                    if common_utility.display_switch(topology, display_list):
                        logging.info(
                            "Pass : Applied {0} config".format(DisplayConfigTopology(topology).name))
                    else:
                        logging.error("Failed to apply Extended config")
                else:
                    for gfx_index, adapter in self.context_args.adapters.items():
                        for port, panel in adapter.panels.items():
                            if panel.is_active:
                                ##
                                # Verify the registers
                                if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                    self.fail()

            else:
                self.fail("Failed to apply display config")

        ##
        # Switching back to Extended Config.
        if display_list.__len__() > 1:
            topology = enum.EXTENDED
            if common_utility.display_switch(topology, display_list):
                logging.info(
                    "Pass : Applied {0} config".format(DisplayConfigTopology(topology).name))
            else:
                logging.error("Failed to apply Extended config")




    @unittest.skipIf(common_utility.get_action_type() != "VIDEO_PLAYBACK",
                     "Skipped the  test step as the action type is not VIDEO_PLAYBACK")
    def test_03_video_playback(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Play HDR VideoPlayback content in Fullscreen and verify ***")
        media_list = [('Color\\HDR\\Video', 'Life_of_Pi_draft_Ultra-HD_HDR.mp4')]
        for index in range(0, len(media_list)):
            ##
            # Playing an SDR Clip in HDR Mode
            media_path = os.path.join(test_context.SHARED_BINARY_FOLDER, media_list[index][0])
            video_file = os.path.join(media_path, media_list[index][1])
            if common_utility.launch_videoplayback(video_file, fullscreen=True) is False:
                self.fail("Failed to launch media application")
            event = "VideoPlayBack"
            ##
            # Update the HDR Caps after performing the Unplug of Display Event
            color_properties.update_feature_caps_in_context(self.context_args)
            if self.update_common_color_props_for_all(event) is False:
                self.fail()
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                            self.fail()
                        if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                            self.fail()

        window_helper.close_media_player()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
