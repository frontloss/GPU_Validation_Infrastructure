################################################################################################################################
# @file             audio_endpoint_install_uninstall.py
# @brief            Verifies installation and uninstallation of audio driver and endpoints
# @details          Test scenario:
#                                1. Boot the system with edp
#                                2. Hotplug external panel
#                                3. Uninstall audio driver
#                                4. Install audio driver
#                                5. Verify audio endpoints
#                                6. Sample command line: audio_endpoint_install_uninstall.py -edp_a
# @author           Sridharan.V, Kumar, Rohit
################################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *


##
# @class AudioEndpointInstallUninstall
# @brief Verify installation and uninstallation of audio driver
class AudioEndpointInstallUninstall(AudioEndpointBase):

    ##
    # @brief runTest
    # @return None
    def runTest(self):
        lfp_present = False

        if reboot_helper.is_reboot_scenario():
            # Install audio driver and verify
            self.install_and_verify_audio_driver()
            # Verify the endpoints after installing driver
            self.display_audio.audio_verification()
            return

        # Set the test name for logging
        self.test_name = "Audio Codec Install / Uninstall Test"
        if self.hotplug_status is True:
            self.test_name = "Audio Codec Install / Uninstall External Display Test"
        if self.hotplug_status is True and self.hotplug_event == 'INSTALL_UNINSTALL':
            self.test_name = "Audio Codec Install / Uninstall Hotplug Test"
        self.is_test_step = True

        # Step: Get the current topology print_current_topology()<br>
        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        if self.hotplug_mode == 'AFTER' and self.hotplug_event == 'INSTALL_UNINSTALL':
            self.verify_audio_endpoints()

            # Uninstall audio driver and verify
            self.uninstall_and_verify_audio_driver()

            reboot_helper.reboot(self, 'runTest')

        if self.hotplug_status is True:
            # Plug displays one by one and check for audio enumeration
            for display in self.display_list:
                display_port = list(display.keys())[0]
                if display[display_port]['is_lfp'] is False and display_port != self.mst_port:
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
                # Set and verify DP MST topology
                self.set_and_verify_mst(self.mst_port, MST_TOPOLOGY, self.mst_topology_xml)

                # Get the RAD Information for hot plug/unplug test cases
                self.mst_rad = self.get_topology_rad(self.mst_port)

            self.enumerated_displays = self.display_config.get_enumerated_display_info()

        if not (self.hotplug_mode == 'AFTER' and self.hotplug_event == 'INSTALL_UNINSTALL'):
            self.verify_audio_endpoints()
            # Uninstall audio driver and verify
            self.uninstall_and_verify_audio_driver()

            reboot_helper.reboot(self, 'runTest')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
