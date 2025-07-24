#######################################################################################################################
# @file         test_display_switch.py
# @brief        Test to check VDSC programming during display switching scenarios with VDSC and Non VDSC displays.
# @details      Test Scenario:
#               1. Gets the combination of displays based on the no. of displays plugged.
#               2. Iterates through the list and applies each of the config. Verifies DSC programming for each of the
#               active display.
#               This test can be planned with MIPI, EDP and DP displays with a minimum of two displays and maximum of
#               four displays.
#
# @author       Bhargav Adigarla, Praburaj Krishnan
#######################################################################################################################

import logging
import unittest
from collections import namedtuple
from typing import Dict

from Libs.Core import enum
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains test case to check if test environment is right for the display switch test case
#               and another test case which does display switch and verifies the VDSC programming.
class TestDisplaySwitch(VdscBase):
    config_list = []

    ##
    # @brief        Helper function to create config list with different combinations based on the number of displays
    #               connected.
    # @return       None
    @classmethod
    def set_config_list(cls) -> None:
        config_tuple = namedtuple('config', ['topology', 'display_adapter_info_list'])

        vdsc_panel_list = []
        for adapter_display_dict in VdscBase.vdsc_panels:
            [(gfx_index, port)] = adapter_display_dict.items()
            display_and_adapter_info_list = VdscBase._display_config.get_display_and_adapter_info_ex(port, gfx_index)
            if type(display_and_adapter_info_list) is list:
                vdsc_panel_list.extend(display_and_adapter_info_list)
            else:
                vdsc_panel_list.append(display_and_adapter_info_list)

        non_vdsc_panel_list = []
        for adapter_display_dict in VdscBase.non_vdsc_panels:
            [(gfx_index, port)] = adapter_display_dict.items()
            display_and_adapter_info_list = VdscBase._display_config.get_display_and_adapter_info_ex(port, gfx_index)
            if type(display_and_adapter_info_list) is list:
                non_vdsc_panel_list.extend(display_and_adapter_info_list)
            else:
                non_vdsc_panel_list.append(display_and_adapter_info_list)

        # Limiting non vdsc panel to 1 to avoid complexity
        if len(vdsc_panel_list) == 1 and len(non_vdsc_panel_list) == 1:  # Case for 1 VDSC and 1 Non-VDSC panel.
            TestDisplaySwitch.config_list = [
                config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                config_tuple(enum.SINGLE, [non_vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [non_vdsc_panel_list[0], vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[0], non_vdsc_panel_list[0]]),
                config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
            ]
        elif len(vdsc_panel_list) == 2:
            if len(non_vdsc_panel_list) == 1:  # Case for 2 VDSC panels and 1 Non-VDSC panel.
                TestDisplaySwitch.config_list = [
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0], non_vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], non_vdsc_panel_list[0]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
                ]
            else:  # Case for 2 VDSC panels
                TestDisplaySwitch.config_list = [
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
                ]
        elif len(vdsc_panel_list) == 3:
            if len(non_vdsc_panel_list) == 1:  # Case for 3 VDSC panels and 1 Non-VDSC panel.
                TestDisplaySwitch.config_list = [
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[2]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], vdsc_panel_list[2]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[2], vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[0], vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], vdsc_panel_list[2],
                                                 non_vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[2], vdsc_panel_list[0],
                                                 non_vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[0], vdsc_panel_list[1],
                                                 non_vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [non_vdsc_panel_list[0], vdsc_panel_list[2], vdsc_panel_list[0],
                                                 vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
                ]
            else:  # Case for 3 VDSC panels.
                TestDisplaySwitch.config_list = [
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[2]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[2]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[1]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], vdsc_panel_list[2]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[2], vdsc_panel_list[0]]),
                    config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[0], vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                    config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
                ]
        elif len(vdsc_panel_list) == 4 and len(non_vdsc_panel_list) == 0:  # Case for 4 VDSC panels only.
            TestDisplaySwitch.config_list = [
                config_tuple(enum.SINGLE, [vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[1]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[2]]),
                config_tuple(enum.SINGLE, [vdsc_panel_list[3]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], vdsc_panel_list[2]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[2], vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[0], vdsc_panel_list[3]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[3], vdsc_panel_list[2], vdsc_panel_list[0]]),
                config_tuple(enum.SINGLE, [vdsc_panel_list[2]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[0], vdsc_panel_list[1], vdsc_panel_list[2],
                                             vdsc_panel_list[3]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[1], vdsc_panel_list[0], vdsc_panel_list[3],
                                             vdsc_panel_list[2]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[2], vdsc_panel_list[3], vdsc_panel_list[1],
                                             vdsc_panel_list[0]]),
                config_tuple(enum.EXTENDED, [vdsc_panel_list[3], vdsc_panel_list[2], vdsc_panel_list[0],
                                             vdsc_panel_list[1]]),
                config_tuple(enum.SINGLE, [vdsc_panel_list[1]]),
                config_tuple(enum.SINGLE, [vdsc_panel_list[0]])
            ]

    ##
    # @brief        Test Case that runs before doing display switch to check if if at least two displays are connected.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_display_switch_requirements(self) -> None:
        TestDisplaySwitch.set_config_list()

        if (len(VdscBase.vdsc_panels) == 0) or TestDisplaySwitch.config_list is False:
            self.fail("[Command Line Issue] - At least two displays are required for DisplaySwitch test")

    ##
    # @brief        Test case which acts a wrapper to invoke the display switch function which verifies VDSC
    #               programming after every display switch based on the config list created.
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_display_switch(self) -> None:
        self._verify_vdsc_with_display_switch()

    ##
    # @brief        Sets each display config from the config list created and verifies VDSC programming.
    # @return       None
    def _verify_vdsc_with_display_switch(self) -> None:

        config_list_display_switch = self._get_display_config_list(TestDisplaySwitch.config_list)

        for config in config_list_display_switch:
            topology = config.topology
            display_adapter_info_list = config.display_adapter_info_list

            is_success = VdscBase._display_config.set_display_configuration_ex(topology, display_adapter_info_list)
            self.assertTrue(is_success, "Applying Display Config Failed")

            supported_mode_dict = VdscBase._display_config.get_all_supported_modes(display_adapter_info_list,
                                                                                   sorting_flag=True)
            for target_id, supported_mode_list in supported_mode_dict.items():
                logging.debug(f"List of supported modes for Target id: {target_id}")

                for display_mode in supported_mode_list:
                    logging.debug(f'HRes:{display_mode.HzRes} VRes:{display_mode.VtRes} RR:{display_mode.refreshRate}'
                                  f' BPP:{display_mode.BPP}')

            for display_adapter_info in display_adapter_info_list:
                port = cfg_enum.CONNECTOR_PORT_TYPE(display_adapter_info.ConnectorNPortType).name
                gfx_index = display_adapter_info.adapterInfo.gfxIndex

                # currently gfx_index 0 is used for mst cases, will be made MA compatible after phase 2 changes
                # Jira link: https://jira.devtools.intel.com/browse/VSDI-21011
                if port in VdscBase.mst_port_name_list and gfx_index == 'gfx_0':
                    logging.warning(f"Skipping DSC verification for MST display plugged at {port} on {gfx_index}")
                    continue

                is_vdsc_panel = DSCHelper.is_vdsc_supported_in_panel(gfx_index, port)
                if is_vdsc_panel:
                    is_success = dsc_verifier.verify_dsc_programming(gfx_index, port)
                    self.assertTrue(is_success, f"DSC Verification Failed For {port} on {gfx_index}")
                    logging.info(f"DSC Verification Successful For {port} on {gfx_index}")

    ##
    # @brief       Create Display config List for display switch for the current platform
    # @param[in]   config_list with all possible display configs combinations with connected displays
    # @return      display_config_switch_list List a subset of config_list with possible cogit pnfigs for the platform
    def _get_display_config_list(self, config_list: list) -> list:
        display_config_switch_list = []
        platform = None

        for config in config_list:
            display_adapter_info_list = config.display_adapter_info_list

            platform_display_dict: Dict[str, int] = {}
            for display_adapter_info in display_adapter_info_list:
                gfx_index = display_adapter_info.adapterInfo.gfxIndex
                adapter_info = VdscBase.cmd_line_adapters[gfx_index]
                platform = adapter_info.get_platform_info().PlatformName.upper()
                platform_display_dict[platform] = platform_display_dict.setdefault(platform, 0) + 1

            # For LNL consider only configs with displays <= 3 as LNL supports only 3 displays max
            if "LNL" in platform_display_dict.keys() and platform_display_dict['LNL'] > 3:
                continue

            display_config_switch_list.append(config)

        return display_config_switch_list


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
