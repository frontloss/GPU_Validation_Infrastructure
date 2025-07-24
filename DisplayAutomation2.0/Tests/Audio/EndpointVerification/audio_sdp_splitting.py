################################################################################################################################
# @file              audio_sdp_splitting.py
# @brief             Verify audio endpoint enumeration, audio register programming, audio sdp enabling for each display
#                    mode set operation
# @details           Refer to wiki https://wiki.ith.intel.com/display/GfxDisplay/Audio+SDP+Splitting+for+DP1.4+-+TDS
#                    for planned test cases
#                              Test scenario:
#                                 1. Boot the system with edp
#                                 2. Hotplug xml topology passed in cmdline
#                                 3. Verify mst, dsc, endpoints, playback, sdp splitting after each modest
#                                 4. Do all powerevent and for each power event verify step 3
#                                 4. Sample command line: audio_sdp_splitting.py -dp_f -mst dp_f -xml [xml_file_path]
#                                                         -vdsc True
# @author            Veluru, Veena, Nivetha, B
################################################################################################################################

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Audio.EndpointVerification.audio_endpoint_base import *
from Tests.PowerCons.Modules import common


##
# @class AudioSdpSplitting
# @brief Verifies SDP Splitting for audio
class AudioSdpSplitting(AudioEndpointBase):
    expected_sdp_splitting = None
    ##
    # @brief runtest
    # @return None
    def t_10_basic_sdp_split(self):
        # Set the test name for logging
        self.test_name = "Audio SDP Splitting Test Basic"

        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        # Step: Set and verify display configuration
        for port, parser in self.mode_enum_parser_dict.items():
            # Iterate over each mode from the apply list and verify mode set
            for display_mode_block in parser.apply_mode_list:
                mode_obj = display_mode_block.display_mode
                gfx_index = mode_obj.displayAndAdapterInfo.adapterInfo.gfxIndex
                if self.cmd_line_param['DP2_SPLITTING'][0] == 'FALSE':
                    self.expected_sdp_splitting = False
                else:
                    self.expected_sdp_splitting = display_mode_block.display_mode_control_flags.data.sdp_splitting
                is_mode_set = self.display_config.set_display_mode([mode_obj])
                self.assertTrue(is_mode_set, f"[Driver Issue] - Set Display Mode failed for {port}")
                self.print_current_topology()
                if self.cmd_line_param['DP2_SPLITTING'] != 'NONE':
                    is_dp2p0 = self.verify_dp2(display=port)
                    if is_dp2p0:
                        logging.info("\tPASS: Expected Display Type= DP2.0, Actual= DP2.0")
                    else:
                        logging.error("\tERROR: Expected Display Type= DP2.0, Actual= Non-DP2.0")

                self.verify_dsc_audio_sdp(port, gfx_index, trans_cnt=1)

                # verify power events if passed in cmdline
                if self.power == 'CS':
                    is_cs_successful = display_power.DisplayPower().invoke_power_event(display_power.PowerEvent.CS, 60)
                    self.assertTrue(is_cs_successful, "CS Execution failed")
                    self.verify_dsc_audio_sdp(port, gfx_index)
                elif self.power == 'NON_CS':
                    is_s3_successful = display_power.DisplayPower().invoke_power_event(display_power.PowerEvent.S3, 60)
                    self.assertTrue(is_s3_successful, "S3 Execution failed")
                    self.verify_dsc_audio_sdp(port, gfx_index)

                    is_s4_successful = display_power.DisplayPower().invoke_power_event(display_power.PowerEvent.S4, 60)
                    self.assertTrue(is_s4_successful, "S4 Execution failed")
                    self.verify_dsc_audio_sdp(port, gfx_index)

                    is_mto_successful = display_power.DisplayPower().invoke_monitor_turnoff(display_power.MonitorPower.OFF_ON, 60)
                    self.assertTrue(is_mto_successful, "MTO Execution failed")
                    self.verify_dsc_audio_sdp(port, gfx_index)

    ##
    # @brief verify audio sdp splitting
    # @param[in] display_port DP_B/DP_A
    # @param[in] gfx_index on which display is connected
    # @param[in] trans_cnt transcoder count to verify sdp splitting for enabled transcoders
    # @return None
    def verify_dsc_audio_sdp(self, display_port, gfx_index, trans_cnt=1):
        vdsc_enable = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, display_port)

        # Verify that the audio endpoints are enumerated correctly and also playback
        self.verify_audio_driver()
        self.verify_audio_endpoints()

        # verify SDP splitting
        self.verify_sdp_splitting(display_port, gfx_index, self.expected_sdp_splitting, trans_cnt)


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(AudioSdpSplitting))
    TestEnvironment.cleanup(test_result)
