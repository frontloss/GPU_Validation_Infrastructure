################################################################################################################################
# @file             audio_endpoint_hotplug_unplug.py
# @brief            Verifies audio endpoint enumeration and audio register programming for each hot plug / unplug of displays
# @details          Test scenario:
#                                1. Boot the system with edp
#                                2. Hotplug external panel
#                                3. Apply config from command line and verify audio endpoints
#                                4. Unplug external pane and verify audio endpoints
#                                5. Sample command line: audio_endpoint_hotplug_unplug.py -edp_a -hdmi_b -dp_c
#                                   -config clone -hotplug true
# @author           Sridharan.V, Kumar, Rohit
################################################################################################################################

from Libs.Core import window_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @class AudioEndpointHotplugUnplug
# @brief Verifies audio endpoint enumeration and audio register programming
class AudioEndpointHotplugUnplug(AudioEndpointBase):

    ##
    # @brief runtest
    # @return None
    def runTest(self):
        lfp_present = False

        # Set the test name for logging
        if self.d3_status is False and self.power_event_status is False and self.hotplug_mode is None:
            self.test_name = "Audio Hot plug / Unplug Test"
        if self.d3_status is True and self.power_event_status is False and self.hotplug_mode is None:
            self.test_name = "Audio Codec Hot plug / Unplug with D3 Test"
        if self.d3_status is False and self.power_event_status is True and self.hotplug_mode == 'AFTER':
            self.test_name = "Audio Hot plug / Unplug after {0} Test".format(self.power_event_str)
        if self.d3_status is False and self.power_event_status is True and self.hotplug_mode == 'IN':
            self.test_name = "Audio Hot plug / Unplug in {0} Test".format(self.power_event_str)
        if self.d3_status is True and self.power_event_status is True and self.hotplug_mode == 'AFTER':
            self.test_name = "Audio Codec Hot plug / Unplug after {0} with D3 Test".format(self.power_event_str)
        if self.d3_status is True and self.power_event_status is True and self.hotplug_mode == 'IN':
            self.test_name = "Audio Codec Hot plug / Unplug in {0} with D3 Test".format(self.power_event_str)
        self.is_test_step = True

        logging.info("******* {0} Started *******".format(self.test_name))

        for cycle_no in range(0, self.iterations):

            # Print the cycle number if the number of iterations are more than 1
            if self.iterations > 1:
                logging.info("--------------Test cycle {0}-----------------".format(cycle_no + 1))

            self.print_current_topology()

            if self.d3_controller is True:
                self.verify_audio_codec_d3_state()
                self.verify_audio_controller_d3_state()
            elif self.d3_codec is True:
                self.verify_audio_codec_d3_state()

            if self.power_event_mto:
                # Work around for 'plug-in during low power state' issue
                window_helper.minimize_all_windows()

            if self.power_event_status is True and self.hotplug_mode == 'AFTER':
                # Invoke power event
                self.base_invoke_power_event(power_event=self.power_event_type, is_mto=self.power_event_mto)

            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            # Plug displays one by one and check for audio enumeration
            for display in self.display_list:
                display_port = list(display.keys())[0]
                if display_port != self.mst_port and display[display_port]['is_lfp'] is False:
                    if disp_cfg.is_display_attached(self.enumerated_displays, display_port,
                                                    display[display_port]['gfx_index']) is False:
                        if self.hotplug_mode == 'IN':
                            self.base_hot_plug(display=display, low_power=True, power_event=self.power_event_type,
                                               is_mto=self.power_event_mto)
                        else:
                            self.base_hot_plug(display)

            if not self.mst_status:
                disp_list = []
                for display in self.display_list:
                    display_port = list(display.keys())[0]
                    display_port = (display[display_port]['connector_port'])
                    disp_list.append(display_port)
                topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
                self.set_display_config(display_list=disp_list, topology=topology)

            # Plug the DP MST displays for MST test cases
            if self.mst_status is True:
                if self.hotplug_mode == 'IN':
                    # Set and verify DP MST topology
                    self.set_and_verify_mst(self.mst_port, MST_TOPOLOGY, self.mst_topology_xml, low_power=True,
                                            power_event=self.power_event_type, is_mto=self.power_event_mto)
                else:
                    # Set and verify DP MST topology
                    self.set_and_verify_mst(self.mst_port, MST_TOPOLOGY, self.mst_topology_xml)

                # Get the RAD Information for hot plug/unplug test cases
                self.mst_rad = self.get_topology_rad(self.mst_port)

            # Verify vdsc if the status is True
            if self.vdsc_status is True:
               # Apply Max mode so that VDSC can be enabled
               self.apply_max_mode_for_all_displays()
               self.verify_vdsc_audio()

            # Verify that the audio endpoints are enumerated correctly
            self.verify_audio_endpoints()

            self.enumerated_displays = self.display_config.get_enumerated_display_info()

            # Unplug displays one by one and verify audio enumeration
            logging.info("Unplug display and Verify Audio Enumeration")
            plugged_displays_during_test = self.plugged_display[:]
            rad_index = 0
            for display in plugged_displays_during_test:
                if display != self.mst_port:
                    if self.hotplug_mode == 'IN':
                        self.base_unplug(display=display, low_power=True, power_event=self.power_event_type,
                                         is_mto=self.power_event_mto)
                    else:
                        self.base_unplug(display)

                    # Verify that the audio endpoints are enumerated correctly
                    self.verify_audio_endpoints()
                else:
                    self.display_port.set_hpd(port_type=self.mst_port, attach_dettach=False)
                    time.sleep(8)
                    rad_index += 1

            if self.power_event_mto:
                # Work around for 'plug-in during low power state' issue
                window_helper.restore_all_windows()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
