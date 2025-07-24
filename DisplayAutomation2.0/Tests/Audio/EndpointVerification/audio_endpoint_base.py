################################################################################################################################
# @file            audio_endpoint_base.py
# @brief           AudioEndpointBase provides setUp and tearDown functions from unittest framework. AudioEndpointBase contains the basic functions required to plug and unplug the displays during the test. Also contains the functions to collect the Matthew and wpp logs.
# @details         Test scenario:
#                               1.Boot the system with edp
#                               2. Hotplug external panels based on command line
#                               3. Unplug the plugged displays during test
# @author          Sridharan.v, Kumar, Rohit
################################################################################################################################

from Libs.Core import reboot_helper

from Tests.Audio.display_audio_base import *
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify


##
# @class AudioEndpointBase
# @brief Base Class for Audio Endpoint Verification Test Cases
class AudioEndpointBase(AudioBase):

    @reboot_helper.__(reboot_helper.setup)
    ##
    # @brief setup
    # @return None
    def setUp(self):
        VerifierCfg.underrun = Verify.SKIP_FAILURE
        super(AudioEndpointBase, self).setUp()
        platform = None
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for gfx_index in adapter_dict.keys():
            platform = self.machine_info.get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName
        if self.hotplug_status is False:
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            # Plug and verify the non DP-MST displays
            for display in self.display_list:
                display_port = list(display.keys())[0]
                if display[display_port]['is_lfp'] is False and display_port != self.mst_port:
                    if platform not in ["ELG"]:
                        if disp_cfg.is_display_attached(self.enumerated_displays, display_port,
                                                        display[display_port]['gfx_index']) is False:
                            self.base_hot_plug(display)
                    else:
                        self.base_hot_plug(display)

            topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
            if not self.mst_status and topology != enum.SINGLE:
                disp_list = []
                for display in self.display_list:
                    display_port = list(display.keys())[0]
                    display_port = (display[display_port]['connector_port'])
                    disp_list.append(display_port)
                self.set_display_config(display_list=disp_list, topology=topology)

            # Plug the DP MST displays for MST test cases.
            # In case of sdp splitting, we are using mode enum parser to plug the topology
            if self.mst_status is True and self.sdp_splitting is not True:
                # Set and verify DP MST topology
                self.set_and_verify_mst(self.mst_port, MST_TOPOLOGY, self.mst_topology_xml)
                for display in self.display_list:
                    display_port = list(display.keys())[0]
                    if display[display_port]['is_lfp']:
                        self.plugged_display.insert(0, display_port)

                for disp in self.plugged_display:
                    if isinstance(disp, dict):
                        display_port = list(disp.keys())[0]
                        self.plugged_display.insert(disp[display_port]['index'], (disp[display_port]['connector_port']))
                        break

                self.plugged_display = [display for display in self.plugged_display if not isinstance(display, dict)]
                if self.cmd_line_param['CONFIG'] != 'SINGLE':
                    topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
                    self.set_display_config(display_list=self.plugged_display, topology=topology)

            self.enumerated_displays = self.display_config.get_enumerated_display_info()

    @reboot_helper.__(reboot_helper.teardown)
    ##
    # @brief teardown
    # @return None
    def tearDown(self):
        VerifierCfg.underrun = Verify.SKIP_FAILURE

        self.is_test_step = False

        logging.info("******* {0} Completed *******".format(self.test_name))

        if self.display_port is not None:
            status = self.display_port.uninitialize_sdk()
            if status is True:
                logging.info("Uninitialization of CUI SDK Successful in TearDown().")
            else:
                logging.error("Uninitialization of CUI SDK Failed in TearDown().")

        self.stop_audio_logging()
        time.sleep(1)

        if self.move_wpp_logs is True:
            self.copy_wpplogs()

        if self.start_matthew_logs is True:
            self.stop_acx_matthew_logging()
            if self.move_matthew_logs is True:
                if self.acx_matthew_error is False:
                    self.copy_acx_matthew_log()
            self.acx_matthew_log_cleanup()

        # Make sure graphics driver is enabled back in case of failure
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for adapter_index in adapter_dict:
            # Make sure graphics driver is enabled back in case of failure
            if self.is_gfx_driver_enabled is False:
                display_essential.enable_driver(adapter_index)

            # Make sure audio driver is enabled back in case of failure
            if self.is_audio_codec_driver_enabled is False:
                self.display_audio.enable_audio_driver(adapter_index)

            # Make sure audio controller is enabled back in case of failure
            if self.is_audio_controller_enabled is False:
                self.display_audio.disable_enable_audio_controller(action="enable", gfx_index=adapter_index)

        # Make sure audio driver is installed back in case of failure
        # TODO: Add MultiAdapter support for Audio driver installation.
        if self.is_audio_driver_installed is False:
            self.display_audio.install_audio_driver()

        # Unplug displays
        plugged_displays_during_test = self.plugged_display[:]
        for display in plugged_displays_during_test:
            if display != self.mst_port:
                self.base_unplug(display)
            else:
                status = self.display_port.set_hpd(self.mst_port, False)
                if status:
                    logging.info("\tUnplug of {0} successful".format(self.mst_port))
                else:
                    gdhm.report_test_bug_audio(title="[Audio] Simulation driver failed to issue HPD to Graphics driver")
                    logging.error("Simulation driver failed to issue HPD to Graphics driver")
