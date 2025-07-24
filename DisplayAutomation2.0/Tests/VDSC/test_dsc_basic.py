#######################################################################################################################
# @file         test_dsc_basic.py
# @brief        Test to check VDSC programming for the VDSC display with the max mode supported by it.
# @details      Test Scenario:
#               1. Plugs the VDSC displays, Applies the Extended mode if more than one display is connected else SINGLE
#               2. Applies max mode for each of the VDSC display in the topology.
#               3. Verifies VDSC programming for all the VDSC display in the topology.
#               4. Also verifies display engine programming for MST display (1 stream case)
#               This test can be planned with MIPI, EDP and DP VDSC displays
#
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
import unittest

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDSCBasic(VdscBase):
    # The mapping between samplingMode and ColorFormat Enum
    sampling_mode_color_format_dict = {1: ColorFormat.RGB, 2: ColorFormat.YUV420, 4: ColorFormat.YUV422,
                                       8: ColorFormat.YUV444}

    ##
    # @brief        This Test method verifies dsc programming for VDSC display at its max resolution.
    # @return       None
    def t_11_test_dsc_basic(self) -> None:

        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        self.assertIsNotNone(enumerated_displays, "[Test Issue] - API get_enumerated_display_info() FAILED")

        is_success, config = VdscBase.get_config_to_apply()
        self.assertTrue(is_success, "[Planning Issue] - Invalid Command Line")

        topology_name = DisplayConfigTopology(config.topology).name

        logging.info("Applying Display Config {} for {}".format(topology_name, config.port_list))
        is_success = VdscBase._display_config.set_display_configuration_ex(config.topology, config.port_list)
        self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")

        common.print_current_topology()

        for adapter_display_dict in VdscBase.vdsc_panels:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed
            [(gfx_index, port)] = adapter_display_dict.items()

            adapter_info = VdscBase.cmd_line_adapters[gfx_index]
            platform = adapter_info.get_platform_info().PlatformName.upper()
            if platform == "ELG":
                display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, gfx_index)
                is_success, supported_modes = DisplayConfiguration().get_all_supported_modes_igcl(display_adapter_info)
                self.assertTrue(is_success, "IGCL API failed")
                self.assertIsNotNone(supported_modes, "Failed to get supported modes")

                max_mode = VdscBase.get_max_mode(supported_modes)
                is_success = VdscBase._display_config.set_higher_pixel_clock_mode(display_adapter_info, max_mode)
                self.assertTrue(is_success, "[Driver Issue] - Failed to Apply Display Mode on {}".format(port))

                current_mode = VdscBase._display_config.get_current_mode(display_adapter_info)
                color_format = ColorFormat(current_mode.samplingMode.Value)

            else:
                max_mode = common.get_display_mode(VdscBase.vdsc_target_ids[port])
                self.assertIsNotNone(max_mode, "Failed to Get Max Mode.")

                # Set Max Mode For Each of the Display
                is_success = VdscBase._display_config.set_display_mode([max_mode], False)
                self.assertTrue(is_success, "[Driver Issue] - Failed to Apply Display Mode on {}".format(port))

                # For now the max_mode in the EDIDs used for this test case contains at least RGB color format which
                # will be represented by the samplingMode structure. The mapping between samplingMode and ColorFormat
                # Enum is defined at dictionary sampling_mode_color_format_dict
                sampling_mode_list = self.prepare_sampling_mode_string(max_mode.samplingMode).strip().split(' ')

                # TODO: Currently this test supports testing of only RGB mode. Can be modified later (if needed) to support validation of all possible sampling mode
                if 'RGB' in sampling_mode_list:
                    color_format = ColorFormat.RGB
                else:
                    self.fail("[Test Issue]: This test doesn't support validation of modes other than RGB")

            test_data = {TestDataKey.COLOR_FORMAT: color_format}

            common.print_current_topology()

            # True indicates only 1 MST display is currently active
            is_one_mst_display = (len(VdscBase.mst_port_name_list) == 1 and len(config.port_list) == 1)
            tiled_ports = [tiled_ports for tiled_ports in VdscBase.sst_tiled_port_name_list if port in tiled_ports[0]]

            # Verify DSC Programming works for 1 MST display case or multiple SST displays
            if (len(VdscBase.mst_port_name_list) == 0 or is_one_mst_display is True) and len(tiled_ports) == 0:
                is_success = dsc_verifier.verify_dsc_programming(gfx_index, port, test_data)
                self.assertTrue(is_success, f"[Driver Issue] - Incorrect DSC Programming at {port} on {gfx_index}")
                logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(port, gfx_index))
            elif len(tiled_ports) == 1:
                is_success = dsc_verifier.verify_dsc_programming(gfx_index, port, test_data, tiled_ports[0][1])
                self.assertTrue(is_success, f"[Driver Issue] - Incorrect DSC Programming at {port} on {gfx_index}")
                logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(port, gfx_index))
            else:
                logging.warning("Skipping DSC Verification as More than 1 Display is connected to the MST branch")

            # Verifying only for 1 MST display case as multi-pipe support is not added in display engine.
            # For SST display it's not invoked since pipe ganged mode support is not added in display engine.
            if is_one_mst_display is True:
                pipe_list, plane_list, transcoder, dip_ctrl, _ = de_base_interface.get_display_context(
                    gfx_index, port, 8, color_format.name
                )
                display_engine = DisplayEngine()
                is_success = display_engine.verify_display_engine([port], plane_list, pipe_list, transcoder, None,
                                                                  dip_ctrl)
                self.assertTrue(is_success, "[Driver Issue] - Display Engine Verification Failed")
            else:
                logging.warning("Skipping DE Verification as More than 1 Display is connected to the MST branch device")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDSCBasic))
    test_environment.TestEnvironment.cleanup(test_result)
