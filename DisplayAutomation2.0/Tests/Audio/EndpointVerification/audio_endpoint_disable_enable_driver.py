################################################################################################################################
# @file           audio_endpoint_disable_enable_driver.py
# @brief          Verifies audio endpoint enumeration by disabling and enabling graphics,audio Controller and Codec
# @details        Test scenario:
#                              1. Boot the system with edp
#                              2. Disable/enable gfx driver and verify endpoints
#                              3. Disable codec/controller and verify endpoints
#                              4. Fails the test:
#                                               a. gfx_driver/codec/controller enable/disable is not happening properly.
#                                               b. If Audio driver disable is not happening properly.
#                                               c. If audio endpoint verification fails
#                              5. Sample command line: audio_endpoint_disable_enable_driver.py -edp_a -hdmi_b
#                                 -config clone
# @author         Kumar, Rohit
################################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *


##
# @brief Verifies audio endpoint enumeration with disabling and enabling graphics and audio driver
# @class AudioEndpointDisableEnableDriver
class AudioEndpointDisableEnableDriver(AudioEndpointBase):
    ##
    # @brief runTest
    # @return None
    def runTest(self):
        lfp_present = False

        # Based on the command line information set the test name for logging
        if self.hotplug_status is True:
            self.test_name = "Audio Disable / Enable Hotplug Test"
        else:
            self.test_name = "Audio Disable / Enable Test"

        logging.info("******* {0} Started *******".format(self.test_name))
        for cycle_no in range(self.iterations):

            # Print the cycle number if the number of iterations are more than 1
            if self.iterations > 1:
                logging.info("--------------Test cycle {0}-----------------".format(cycle_no + 1))

            # Step: Get the current topology
            self.print_current_topology()

            multi_adapter = False
            for display in self.display_list:
                display_port = list(display.keys())[0]
                display_port_info = display[display_port]
                if display_port_info['gfx_index'] == 'GFX_1':
                    multi_adapter = True

            if self.hotplug_status is True:
                # Plug displays one by one and check for audio enumeration
                for display in self.display_list:
                    display_port = list(display.keys())[0]
                    if display[display_port]['is_lfp'] is False and display_port != self.mst_port:
                        if disp_cfg.is_display_attached(self.enumerated_displays, display_port,
                                                        display[display_port]['gfx_index']) is False:
                            if self.hotplug_mode == 'IN':
                                self.base_hot_plug(
                                    display=display,
                                    low_power=True,
                                    power_event=self.power_event_type,
                                    is_mto=self.power_event_mto
                                )
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
                    # Set and verify DP MST topology
                    self.set_and_verify_mst(self.mst_port, MST_TOPOLOGY, self.mst_topology_xml)

                    # Get the RAD Information for hot plug/unplug test cases
                    self.mst_rad = self.get_topology_rad(self.mst_port)

                self.enumerated_displays = self.display_config.get_enumerated_display_info()

            # Disable Gfx driver
            logging.info("Step{0}: Disabling Gfx Driver".format(self.step_counter))
            self.step_counter += 1
            self.assertEquals(display_essential.disable_driver('gfx_0'), True,
                              "Aborting the test as disabling gfx driver failed")
            logging.info("\tPASS: Expected Gfx Driver status for GFX_0= DISABLED, Actual= DISABLED")
            if multi_adapter is True:
                self.assertEquals(display_essential.disable_driver('gfx_1'), True,
                                  "Aborting the test as disabling gfx driver failed")
                logging.info("\tPASS: Expected Gfx Driver status for GFX_1= DISABLED, Actual= DISABLED")
            self.is_gfx_driver_enabled = False
            time.sleep(5)

            # Verify that the audio endpoints are not present after disabling Gfx drivers
            no_of_endpoints = self.display_audio.get_audio_endpoints()
            if no_of_endpoints == 0:
                logging.info("\tPASS: Expected Audio Endpoints= 0, Actual= 0")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Expected Audio Endpoints= 0, Actual= {0} after disabling gfx driver"
                    .format(no_of_endpoints))
                self.fail("Expected Audio Endpoints= 0, Actual= {0} after disabling gfx driver"
                          .format(no_of_endpoints))

            # Enable Gfx driver
            logging.info("Step{0}: Enabling Gfx Driver".format(self.step_counter))
            self.step_counter += 1
            self.assertEquals(display_essential.enable_driver('gfx_0'), True,
                              "Aborting the test as disabling gfx driver failed")
            logging.info("\tPASS: Expected Gfx Driver status for GFX_0= ENABLED, Actual= ENABLED")
            if multi_adapter is True:
                self.assertEquals(display_essential.enable_driver('gfx_1'), True,
                                  "Aborting the test as enabling gfx driver failed")
                logging.info("\tPASS: Expected Gfx Driver status for GFX_1= ENABLED, Actual= ENABLED")
            self.is_gfx_driver_enabled = True

            # Verify that the audio endpoints are enumerated correctly after enabling Gfx drivers
            self.verify_audio_endpoints()

            # Disable and verify Audio driver
            self.disable_and_verify_audio_codec(port_info=display_port_info)

            # Verify that the audio endpoints are not present after disabling audio codec driver
            no_of_endpoints = self.display_audio.get_audio_endpoints()
            if no_of_endpoints == 0:
                logging.info("\tPASS: Expected Audio Endpoints= 0, Actual= 0")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Expected Audio Endpoints= 0, Actual= {0} after disabling codec".format(
                        no_of_endpoints))
                self.fail("Expected Audio Endpoints= 0, Actual= {0} after disabling codec".format(no_of_endpoints))

            self.enable_and_verify_audio_codec(port_info=display_port_info)

            self.verify_audio_endpoints()

            # Disable and verify audio controller
            self.disable_and_verify_audio_controller()

            # Verify that the audio endpoints are enumerated correctly
            time.sleep(5)
            no_of_endpoints = self.display_audio.get_audio_endpoints()
            if no_of_endpoints == 0:
                logging.info("\tPASS: Expected Audio Endpoints= 0, Actual= 0")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Expected Audio Endpoints= 0, Actual= {0} after disabling controller"
                    .format(no_of_endpoints))
                self.fail("Expected Audio Endpoints= 0, Actual= {0} after disabling controller"
                          .format(no_of_endpoints))

            # Enable and verify audio controller
            self.enable_and_verify_audio_controller()

            self.verify_audio_endpoints()

            # Verify vdsc if the status is True
            if self.vdsc_status is True:
                # Apply max mode so that VDSC can be enabled
                self.apply_max_mode_for_all_displays()
                self.verify_vdsc_audio()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
