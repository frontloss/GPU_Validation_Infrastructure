#################################################################################################
# @file         hdr_persistence_gfx_events.py
# @brief        This scripts comprises modularized tests, where :
#               1. test functions_01_power_events() - Intends to verify HDR Persistence with S3, S4 and CS
#               2. test_02_restart_display_driver() - Intends to verify HDR Persistence with Driver Restart
#               3. test_03_monitor_turnoffon() - Intends to verify HDR Persistence with Monitor Turn Off
#               Each of the test modules perform the following :
#               The test script enables HDR on the displays supporting HDR,
#               which is an input parameter from the test command line.
#               Additionally, for an eDP_HDR display the script invokes the API
#               to set the OS Brightness Slider level to a value provided in the command line.
#               If Brightness Slider level has not been given as an input, script sets the slider
#               to a random value other than the Current Brightness value
#               Verification Details:
#               The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#               Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#               Pipe_Misc register is also verified for HDR_Mode
#               Plane and Pipe Verification is performed by iterating through each of the displays
#               Metadata verification, by comparing the Default and Flip Metadata is performed,
#               along with register verification
# Sample CommandLines:  python hdr_persistence_with_gfx_events.py -edp_a SINK_EDP050 -scenario POWER_EVENT_S3
# Sample CommandLines:  python hdr_persistence_with_gfx_events.py -edp_a SINK_EDP050 -scenario POWER_EVENT_S4
# Sample CommandLines:  python hdr_persistence_with_gfx_events.py -edp_a SINK_EDP050 -scenario POWER_EVENT_CS
#                       python hdr_persistence_with_gfx_events.py -edp_a SINK_EDP050 -scenario RESTART_DRIVER
#                       python hdr_persistence_with_gfx_events.py -edp_a SINK_EDP050 -dp_d -scenario MONITOR_TURNOFFON
# @author       Smitha B
#################################################################################################
from Tests.Color.Common.common_utility import invoke_power_event
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class HDRPersistenceWithGfxEvents(HDRTestBase):

    @unittest.skipIf(common_utility.get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        ##
        # Invoke power event
        logging.info("*** Step 2 : Invoke PowerEvents and verify ***")
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:

            event = "Invoking_Power_Event_" + power_state_dict[self.scenario].name
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


    @unittest.skipIf(common_utility.get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Perform Driver Restart and verify ***")


        ##
        # Restart display driver
        for gfx_index, adapter in self.context_args.adapters.items():
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail('Fail: Failed to Restart Display driver')
            logging.info('Pass: Display driver restarted successfully')

            event = "Driver_Restart_TimeStmp_"
            color_properties.update_feature_caps_in_context(self.context_args)
            if self.update_common_color_props_for_all(event) is False:
                self.fail()
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                        self.fail()
                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                        self.fail()



    @unittest.skipIf(common_utility.get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turn_offon(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()
        logging.info("*** Step 2 : Perform Monitor Turn Off-On and verify ***")

        ##
        # monitor turn off on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off Monitor")

        event = "Monitor_TurnOff_TimeStmp_"
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
                else:
                    logging.error("Panel {0} is inactive".format(port))
                    self.fail("Panel {0} is inactive".format(port))


    @unittest.skipIf(common_utility.get_action_type() != "AC_DC",
                     "Skip the  test step as the action type is not AC_DC Switch")
    def test_03_ac_dc_switch(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()
        logging.info("*** Step 2 : Perform AC-DC Switch and verify ***")

        ##
        # Switch the power source to DC Mode
        status = common_utility.apply_power_mode(display_power.PowerSource.DC)
        if status is False:
            self.fail()

        event = "Switching_DC_Mode_TimeStmp_"
        color_properties.update_feature_caps_in_context(self.context_args)
        if self.update_common_color_props_for_all(event) is False:
            self.fail()

        ##
        # Verify if HDR has been disabled across all the panels
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                        logging.error(
                            "HDR is still enabled in DC Mode on Panel : {0} Adapter : {1} Pipe {2}".format(port,
                                                                                                           gfx_index,
                                                                                                           panel.pipe))
                        self.fail()
                    if self.enable_wcg:
                        logging.info("Performing Plane and Pipe Verification for WCG in DC Mode")
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                            self.fail()
                        if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                            self.fail()

        ##
        # Switch the Power Source to AC Mode
        logging.info("*** Step 2 : Perform DC-AC Switch and verify ***")
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()

        event = "Switching_Back_to_AC_Mode_TimeStmp_"
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


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables HDR on supported panels and perform persistence verification on all panels"
        " when HDR is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
