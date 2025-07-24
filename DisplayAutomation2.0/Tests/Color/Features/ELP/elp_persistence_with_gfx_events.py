#################################################################################################
# @file         elp_persistence_with_gfx_events.py
# @brief        This scripts comprises modularized tests, where :
#               1. test functions_01_power_events() - Intends to verify ELP Persistence with S3, S4 and CS
#               2. test_02_restart_display_driver() - Intends to verify ELP Persistence with Driver Restart
#               3. test_03_monitor_turnoffon() - Intends to verify ELP Persistence with Monitor Turn Off
#               Each of the test modules perform the following :
#               The test script enables ELP on the internal displays supporting ELP.
#               The test scripts then performs various events such as Modeset, Display Switching, VideoPlayback
#               and then verifies if ELP is persisting after the events.
#               The ETLs will be captured during the events and parsed to verify
#               if there is any Blc Optimization DDI by OS.
#               If there is None, then the optimization values should persist,
#               if not, need to verify if the new optimization levels are updated in accordance to the DDI.
# Sample CommandLines:  python elp_persistence_with_gfx_events.py -edp_a SINK_EDP76 -scenario POWER_EVENT_S3
# Sample CommandLines:  python elp_persistence_with_gfx_events.py -edp_a SINK_EDP76 -scenario POWER_EVENT_S4
# Sample CommandLines:  python elp_persistence_with_gfx_events.py -edp_a SINK_EDP76 -scenario POWER_EVENT_CS
#                       python elp_persistence_with_gfx_events.py -edp_a SINK_EDP76 -scenario RESTART_DRIVER
#                       python elp_persistence_with_gfx_events.py -edp_a SINK_EDP76 -dp_d -scenario MONITOR_TURNOFFON
# @author       Smitha B
#################################################################################################
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Tests.Color.Common.common_utility import invoke_power_event
from Tests.Color.Features.ELP.elp_test_base import *

class elpPersistenceWithGfxEvents(ELPTestBase):
    ##
    # @brief - ELP persistence test with Power Events
    @unittest.skipIf(common_utility.get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        ##
        # Invoke power event
        logging.info("*** Step 2 : Invoke PowerEvents and verify ***")
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:
            event_name = "After_Resuming_from_" + power_state_dict[self.scenario].name
            self.stop_and_start_etl(event_name)
            color_properties.update_feature_caps_in_context(self.context_args)
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                        if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                            self.fail()

    ##
    # @brief - ELP persistence with driver disable-enable
    @unittest.skipIf(common_utility.get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Perform Driver Restart and verify ***")
        ##
        # Restart display driver
        for gfx_index, adapter in self.context_args.adapters.items():
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail('Fail: Failed to Restart Display driver')

            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()

    ##
    # @brief - ELP persistence with Monitor Turn off event
    @unittest.skipIf(common_utility.get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turn_offon(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Perform Monitor Turn Off-On and verify ***")
        ##
        # monitor turn off on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off Monitor")

        time.sleep(2)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()

    ##
    # @brief - ELP persistence with AC-DC switch
    #          The script enables ELP and then switches to AC Mode.
    #          While in AC Mode, script expects OS to issue the DDI with Aggressiveness Level as 'Disable'
    #          The DPCD should be updated according with the optimization level.
    #          The script then switches back to DC Mode and performs persistence verification
    #           The script also invokes an IGCL Call to set the Optimization level in DC Mode and performs verification
    @unittest.skipIf(common_utility.get_action_type() != "AC_DC_SET_ELP",
                     "Skip the  test step as the action type is not AC_DC Switch")
    def test_04_ac_dc_switch_set_elp_level(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Perform DC-AC Switch and verify ***")
        ##
        # Switch the power source to DC Mode
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()

        time.sleep(5)

        self.stop_and_start_etl("After_Switching_To_AC_Mode")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, ddi_optimization_level = color_etl_utility.get_blc_ddi3_optimization(panel.target_id)
                    logging.info("Status : {0} and Optimization Level : {1}".format(status, ddi_optimization_level))

                    if status:
                        if ddi_optimization_level in ('Disable', 'Desktop'):
                            logging.info("PASS : OS has updated the Optimization Level as 'Disable'")
                            ##
                            # Verifying that the DPCD is updated with Optimization Strength as 0 and AC Mode details
                            for gfx_index, adapter in self.context_args.adapters.items():
                                for port, panel in adapter.panels.items():
                                    if panel.is_active and panel.is_lfp:
                                        if verify_opt_level_in_dpcd(gfx_index, panel, port,
                                                                    self.user_opt_level) is True:
                                            self.fail()
                                        else:
                                            logging.info(
                                                "PASS : Optimization levels are not getting reflected in the DPCD as "
                                                "expected since the PowerSource is AC")

                    else:
                        logging.error("FAIL : OS has not updated the Optimization Level as 'Disable'")
                        gdhm.report_driver_bug_pc("[ELP] OS has not updated the Optimization Level as 'DISABLE'")
                        self.fail()

                    ##
                    # Trying to invoke the escape call to check if DPCD gets updated with the optimization level
                    # in AC Mode ---> Query for ELP; and also, when switch back to DC, what is the DPCD value - Updated or previous??
                    # Note : Ideally in IGCC, when we switch to AC Mode,
                    # the DPST Slider would not be visible, so the user will not be able to change the slider.
                    # This step is an additional confirmation to cover this path in the driver.
                    if self.enable_elp_optimization_and_verify(self.user_opt_level):
                        logging.error("FAIL : Optimization level set in AC Mode")
                        self.fail()

                    logging.info(
                        "PASS : Optimization levels are not getting reflected in the DPCD as expected since "
                        "the PowerSource is AC")

        ##
        # Switch the Power Source back to DC Mode
        logging.info("*** Step 3 : Perform AC-DC Switch and verify ***")
        status = common_utility.apply_power_mode(display_power.PowerSource.DC)
        if status is False:
            self.fail()

        time.sleep(5)

        self.stop_and_start_etl("After_Completing_AC_To_DC_Switch")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, ddi_optimization_level = color_etl_utility.get_blc_ddi3_optimization(panel.target_id)
                    logging.info("Status : {0} and Optimization Level : {1}".format(status, ddi_optimization_level))
                    if status:
                        if ddi_optimization_level not in 'Disable':
                            if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                                return False
                        else:
                            logging.error(
                                "FAIL : OS continues to update the Aggressiveness level as 'Disable' after "
                                "switching back to DC Mode")
                    else:
                        pass  # self.fail()

    @unittest.skipIf(common_utility.get_action_type() != "VIDEO_PLAYBACK",
                     "Skipped the  test step as the action type is not VIDEO_PLAYBACK")
    def test_05_video_playback(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Play SDR VideoPlayback content in Fullscreen and verify ***")
        media_list = ('MPO', 'mpo_1920_1080_avc.mp4')
        ##
        # Playing an SDR Clip in HDR Mode
        media_path = os.path.join(test_context.SHARED_BINARY_FOLDER, media_list[0])
        video_file = os.path.join(media_path, media_list[1])
        logging.info("Video File Path {0}".format(video_file))
        if common_utility.launch_videoplayback(video_file, fullscreen=True) is False:
            self.fail("Failed to launch media application")

        init_etl = "During_VideoPlayBack_"
        init_etl_path = color_etl_utility.stop_etl_capture(init_etl)

        if etl_parser.generate_report(init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
        else:
            ##
            # Start the ETL again for capturing other events
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    status, ddi_optimization_level = color_etl_utility.get_blc_ddi3_optimization(panel.target_id)
                    logging.info("Status : {0} and Optimization Level : {1}".format(status, ddi_optimization_level))
                    if ddi_optimization_level not in ('Disable', 'Desktop'):
                        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
                            self.fail()
                    else:
                        logging.error(
                            "FAIL : OS failed to update the Aggressiveness Level to 'Dynamic' during Fullscreen "
                            "VideoPlayBack scenario")
                        gdhm.report_driver_bug_pc("[ELP] OS has not updated the Aggressiveness Level to 'Dynamic' during fullscreen VPB")
                        self.fail()

        window_helper.close_media_player() # Close the video player

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels and perform persistence verification")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
