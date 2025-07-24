#######################################################################################################################
# @file         test_pipe_joiner_mode_enum.py
# @brief        Test to check all supported modes are enumerated by the driver in case of uncompressed pipe joiner.
# @details      Test Scenario:
#               1. Plugs the DP panel and applies SINGLE display config
#               2. Check the color format from the xml file and enable the color format in the driver accordingly
#               3. Verifies the enumerated modes by checking against modes present in xml for each of the platform.
#               4. Applies each of the modes present in the xml and verifies uncompressed pipe joiner programming
#               This test can be planned only with DP displays only
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import unittest

from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.test_env import test_environment
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import bpc_mapping, ColorFormat
from Tests.Display_Port.DP_Pipe_Joiner.pipe_joiner_base import PipeJoinerBase
from Tests.PowerCons.Modules import common
from Tests.VDSC.mode_enum_verifier import ModeEnumerationVerifier


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestPipeJoinerModeEnumeration(PipeJoinerBase):

    ##
    # @brief        This test method verifies the enumerated modes by the driver based on the xml file and also verifies
    #               uncompressed pipe joiner programming for each of the modes present in xml file by applying it.
    # @return       None
    def t_12_mode_enum(self) -> None:

        for port, parser in PipeJoinerBase.mode_enum_parser_dict.items():
            # Get Golden Mode and Ignore Mode Dict From the Parser.
            g_mode_dict, i_mode_dict = parser.golden_mode_dict, parser.ignore_mode_dict

            f_status = ModeEnumerationVerifier.verify_enumerated_modes(parser.gfx_index, port, g_mode_dict, i_mode_dict)
            self.assertTrue(f_status, f"Verifying Mode Enumeration Failed For {port} Display on {parser.gfx_index}")
            logging.info('Enumerated Modes and Golden Modes are Matching')

            # Iterate Through Each of the Mode in Apply Mode Dict, Apply the Mode and Verify it.
            for display_mode_block in parser.apply_mode_list:
                mode_to_apply: DisplayMode = display_mode_block.display_mode
                ModeEnumerationVerifier.log_display_modes("APPLYING:", {mode_to_apply})

                is_success: bool = ModeEnumerationVerifier.display_configuration.set_display_mode([mode_to_apply])
                self.assertTrue(is_success, "Set Display Configuration Failed.")

                bpc = bpc_mapping[display_mode_block.display_mode_control_flags.data.bpc]
                color_format = ColorFormat(display_mode_block.display_mode_control_flags.data.color_format).name

                pipe_list, plane_list, transcoder, dip_ctrl, _ = de_base_interface.get_display_context(
                    parser.gfx_index, port, bpc, color_format
                )

                display_engine = DisplayEngine()
                is_success = display_engine.verify_display_engine([port], plane_list, pipe_list, transcoder, None,
                                                                  dip_ctrl)
                self.assertTrue(is_success, "Display Engine Verification Failed")

                is_pipe_joiner_required, _ = DisplayClock.is_pipe_joiner_required(parser.gfx_index, port)
                if is_pipe_joiner_required is True:
                    is_success = PipeJoinerBase.verify_pipe_joined_display(port)
                    self.assertTrue(is_success, PipeJoinerBase.test_fail_log_template.format(port))
                    logging.info(PipeJoinerBase.test_success_log_template.format(port))

            logging.info('Applied and Verified Each of the Apply Mode Obtained From XML')


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPipeJoinerModeEnumeration))
    test_environment.TestEnvironment.cleanup(test_result)
