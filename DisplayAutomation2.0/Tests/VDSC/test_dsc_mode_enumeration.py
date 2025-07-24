#######################################################################################################################
# @file         test_dsc_mode_enumeration.py
# @brief        Test to check all supported modes are enumerated by the driver for VDSC display and to verify DSC
#               programming for each of the mode. Supports RGB, YUV444, YUV422 and YUV420 mode verification.
# @details      Test Scenario:
#               1. Plugs the VDSC panel and applies SINGLE display config
#               2. Check the color format from the xml file and enable the color format in the driver accordingly
#               3. Verifies the enumerated modes by checking against modes present in xml for each of the platform.
#               4. Applies each of the modes present in the xml and verifies VDSC programming
#               This test can be planned only with DP VDSC displays
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import unittest

from Libs.Core.test_env import test_environment
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumHelper

from Tests.Color.Common import color_escapes
from Tests.PowerCons.Modules import common
from Tests.VDSC.mode_enum_verifier import ModeEnumerationVerifier
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDSCModeEnumeration(VdscBase):

    ##
    # @brief        This test enables YUV formats based on the color format mentioned in the Mode Enum XML file.
    # @details      YUV444 Mode - Need to make escape call to change pipe color format -> OS unaware way.
    #               YUV422 Mode - Need to set reg key to force all modes to be treated as YUV422 -> OS unaware way.
    #               YUV420 Mode - Need not be handled as separate modes are created in edid with YUV420 support only.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_enable_yuv_formats(self) -> None:

        logging.debug("Enabling YUV Formats based on Mode Enum XML file Color Format ")

        # Create list of display_adapter_info
        display_adapter_info_list = []
        for port, parser in VdscBase.mode_enum_parser_dict.items():
            display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, parser.gfx_index)
            if type(display_adapter_info) is list:
                display_adapter_info = display_adapter_info[0]
            display_adapter_info_list.append(display_adapter_info)

        # Apply display configuration for display_adapter_info_list
        is_success = VdscBase._display_config.set_display_configuration_ex(VdscBase.topology, display_adapter_info_list)
        self.assertTrue(is_success, "[Driver Issue] - Failed to apply display configuration")

        for port, parser in VdscBase.mode_enum_parser_dict.items():
            if parser.color_format == "YUV444":
                display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, parser.gfx_index)
                if type(display_adapter_info) is list:
                    display_adapter_info = display_adapter_info[0]
                is_success = color_escapes.configure_ycbcr(port, display_adapter_info, True)
                self.assertTrue(is_success, "[Driver Issue] - Enabling YUV444 through escape call failed.")
                logging.info("Enabling YUV444 through escape call succeeded")
            elif parser.color_format == "YUV422":
                is_success = ModeEnumHelper.enable_yuv422_mode(parser.gfx_index, 1)
                self.assertTrue(is_success, "Enabling YUV422 Mode in driver using reg key failed.")
                logging.info("Force Applying YUV422 mode using reg key succeeded")

    ##
    # @brief        This test method verifies the enumerated modes by the driver based on the xml file and also verifies
    #               VDSC programming for each of the modes present in xml file by applying it.
    # @return       None
    def t_12_mode_enum(self) -> None:

        for port, parser in VdscBase.mode_enum_parser_dict.items():

            # Create list of display_adapter_info
            display_adapter_info_list = []
            display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, parser.gfx_index)
            if type(display_adapter_info) is list:
                display_adapter_info = display_adapter_info[0]
            display_adapter_info_list.append(display_adapter_info)

            # Apply display configuration for display_adapter_info_list
            is_success = VdscBase._display_config.set_display_configuration_ex(VdscBase.topology,
                                                                               display_adapter_info_list)
            self.assertTrue(is_success, "[Driver Issue] - Failed to apply display configuration")

            # Get Golden Mode and Ignore Mode Dict From the Parser.
            g_mode_dict, i_mode_dict = parser.golden_mode_dict, parser.ignore_mode_dict

            f_status = ModeEnumerationVerifier.verify_enumerated_modes(parser.gfx_index, port, g_mode_dict, i_mode_dict)
            self.assertTrue(f_status, f"Verifying Mode Enumeration Failed For {port} Display on {parser.gfx_index}")
            logging.info('Enumerated Modes and Golden Modes are Matching')

            f_status = ModeEnumerationVerifier.apply_mode_and_verify(parser.gfx_index, port, parser.apply_mode_list)
            self.assertTrue(f_status, f"Applying Modes and Verifying DSC Failed For {port} on {parser.gfx_index}")
            logging.info('Applied and Verified Each of the Apply Mode Obtained From XML')

    ##
    # @brief        This test enables YUV formats based on the color format mentioned in the Mode Enum XML file.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_13_disable_yuv_formats(self) -> None:

        logging.debug("Disabling YUV Formats based on Mode Enum XML file Color Format ")

        for port, parser in VdscBase.mode_enum_parser_dict.items():
            if parser.color_format == "YUV444":
                display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, parser.gfx_index)
                if type(display_adapter_info) is list:
                    display_adapter_info = display_adapter_info[0]
                is_success = color_escapes.configure_ycbcr(port, display_adapter_info, False)
                self.assertTrue(is_success, "Disabling YUV444 through escape call failed.")
                logging.info("Disabling YUV444 mode through escape call succeeded")
            elif parser.color_format == "YUV422":
                is_success = ModeEnumHelper.enable_yuv422_mode(parser.gfx_index, 0)
                self.assertTrue(is_success, "Disabling YUV422 Mode in driver using reg key failed.")
                logging.info("Disabling YUV422 mode using reg key succeeded")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDSCModeEnumeration))
    test_environment.TestEnvironment.cleanup(test_result)
