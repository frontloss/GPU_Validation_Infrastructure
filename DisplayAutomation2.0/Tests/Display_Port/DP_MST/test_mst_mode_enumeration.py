#######################################################################################################################
# @file         test_mst_mode_enumeration.py
# @brief        Test to check all supported modes are enumerated by the driver for MST/DP2.0 display
# @details      Test Scenario:
#               1. Plugs the MST/DP2.0/MST Tiled panel and applies SINGLE display config
#               2. Verifies the enumerated modes by checking against modes present in xml for each of the platform.
#               3. Applies each of the modes present in the xml and verifies DE/VDSC programming if required for
#               non-tiled displays only.
#               This test can be planned only with MST/DP2.0/MST Tiled displays
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import unittest
from typing import List

from Libs.Core import enum
from Libs.Core.display_config.display_config_struct import DisplayMode, TARGET_ID
from Libs.Core.test_env import test_environment
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_engine.de_base import display_scalar
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat, DisplayModeBlock, ModeEnumXMLParser
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumHelper
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase
from Tests.PowerCons.Modules import common
from Tests.VDSC.mode_enum_verifier import ModeEnumerationVerifier


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestMSTModeEnumeration(DisplayPortMSTBase):
    parser = None
    port = None

    ##
    # @brief        Exposed API to Apply and Verify All the Modes That are Defined in the XML.
    # @param[in]    gfx_index: str
    #                   Graphics Index On Which the Display is Plugged. Currently, unused but Will be Used Once
    #                   Set Display Mode and Verify DSC Supports MA Scenarios.
    # @param[in]   port: str
    #                   Contains the Port Name on Which the Display is Plugged.
    # @param[in]   apply_mode_list: List[DisplayModeBlock]
    #                   Dictionary Containing Set of Modes That Needs to be Applied, Which are Parsed From the XML.
    # @return       is_success: bool
    #                   Returns True if All Modes Defined the XML are Applied Successfully and DE and DSC verification
    #               is successful else False.
    @classmethod
    def apply_mode_and_verify(cls, gfx_index: str, port: str, apply_mode_list: List[DisplayModeBlock]) -> bool:
        is_success = True
        RSCALE_DICT = {0: 'Unsupported', 1: 'CI', 2: 'FS', 4: 'MAR', 8: 'CAR', 64: 'MDS'}
        display_engine = DisplayEngine()

        # Iterate Through Each of the Mode in Apply Mode Dict, Apply the Mode and Verify it.
        for display_mode_block in apply_mode_list:
            mode_to_apply: DisplayMode = display_mode_block.display_mode
            logging.info("APPLYING - {} on display at {} - {}".format(mode_to_apply, gfx_index, port))
            if mode_to_apply.scaling != 64:
                is_success &= cls.display_config.set_display_mode([mode_to_apply], False)
            else:
                is_success &= cls.display_config.set_display_mode([mode_to_apply])

            color_format = ColorFormat(display_mode_block.display_mode_control_flags.data.color_format)
            test_data = {TestDataKey.COLOR_FORMAT: color_format}

            ports = [port]
            scaling = RSCALE_DICT[mode_to_apply.scaling]
            pipe_list, plane_list, transcoder_list, _, scalar_list = de_base_interface.get_display_context(
                gfx_index, port, 8, color_format.name, scaling
            )

            if TARGET_ID(Value=mode_to_apply.targetId).TiledDisplay == 0:
                if mode_to_apply.scaling != 64:
                    is_success &= display_scalar.VerifyScalarProgramming(scalar_list)
                is_success &= display_engine.verify_display_engine(ports, plane_list, pipe_list, transcoder_list,
                                                                   gfx_index=gfx_index)

                is_success &= dsc_verifier.verify_dsc_programming(gfx_index, port, test_data)

        return is_success

    ##
    # @brief        This test enables YUV formats based on the color format mentioned in the Mode Enum XML file.
    # @details      YUV422 Mode - Need to set reg key to force all modes to be treated as YUV422 -> OS unaware way.
    #               YUV420 Mode - Need not be handled as separate modes are created in edid with YUV420 support only.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_enable_yuv_formats(self) -> None:
        der_cls = TestMSTModeEnumeration
        der_cls.port = self.get_dp_port_from_availablelist(0)
        der_cls.parser = ModeEnumXMLParser('gfx_0', der_cls.port, self.mode_enum_xml_file_path)

        ##
        # Getting color format from xml and setting reg key in case of YUV422
        if der_cls.parser.color_format == "YUV422":
            is_success = ModeEnumHelper.enable_yuv422_mode(der_cls.parser.gfx_index, 1)
            self.assertTrue(is_success, "Enabling YUV422 Mode in driver using reg key failed.")
            logging.info("Force Applying YUV422 mode using reg key succeeded")

    ##
    # @brief        This test method verifies the enumerated modes by the driver based on the xml file and also verifies
    #               DE and VDSC programming if the display is non-tiled.
    # @return       None
    def t_12_mode_enumeration(self) -> None:
        cls = DisplayPortMSTBase
        der_cls = TestMSTModeEnumeration

        display_tech, mst_topology_path = der_cls.parser.display_tech, der_cls.parser.mst_topology_path

        self.setnverifyMST(der_cls.port, display_tech, mst_topology_path)

        self.display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(der_cls.port)

        logging.info(f"Applying Single Display configuration on {der_cls.port}")
        is_success = cls.display_config.set_display_configuration_ex(enum.SINGLE, [self.display_and_adapter_info])
        self.assertTrue(is_success, f"Applying Single Display Config on {der_cls.port} Failed")
        common.print_current_topology()

        der_cls.parser.parse_and_construct_mode_tables()

        # Get Golden Mode and Ignore Mode Dict From the Parser.
        g_mode_dict, i_mode_dict = der_cls.parser.golden_mode_dict, der_cls.parser.ignore_mode_dict

        f_status = ModeEnumerationVerifier.verify_enumerated_modes(der_cls.parser.gfx_index, der_cls.port, g_mode_dict,
                                                                   i_mode_dict)
        self.assertTrue(f_status,
                        f"Verifying Mode Enumeration Failed For {der_cls.port} Display on {der_cls.parser.gfx_index}")
        logging.info('Enumerated Modes and Golden Modes are Matching')

        f_status = TestMSTModeEnumeration.apply_mode_and_verify(der_cls.parser.gfx_index, der_cls.port,
                                                                der_cls.parser.apply_mode_list)
        self.assertTrue(f_status, f"Applying all modes in XML Failed For {der_cls.port} on {der_cls.parser.gfx_index}")
        logging.info('Applied and Verified Each of the Apply Mode Obtained From XML')

    ##
    # @brief        This test enables YUV formats based on the color format mentioned in the Mode Enum XML file.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_13_disable_yuv_formats(self) -> None:
        der_cls = TestMSTModeEnumeration
        if der_cls.parser.color_format == "YUV422":
            is_success = ModeEnumHelper.enable_yuv422_mode(der_cls.parser.gfx_index, 0)
            self.assertTrue(is_success, "Disabling YUV422 Mode in driver using reg key failed.")
            logging.info("Disabling YUV422 mode using reg key succeeded")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestMSTModeEnumeration))
    test_environment.TestEnvironment.cleanup(test_result)
