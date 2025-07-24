########################################################################################################################
# @file         prepare_display_setup.py
# @brief        Usage:
#               To do prepare display:
#                   prepare_display_setup.py -TEST [entire test command line]
#               To reset all steps/simulations done by prepare display:
#                   prepare_display_setup.py -RESET TRUE
#
#               Follow below steps to configure ports in VBT and enable eDP simulation for a new platform:
#                   1. Update port_config dictionary for targeted platform
#                   2. Update ddc_bus_mapping dictionary for ports available in targeted platform
#                   3. Update efp_index_mapping dictionary based on EFP ports available in new platform
#                   Done!
#
# @note         We are restricting VBT preparation for LFP ports on EDP_A and EDP_B
# @note         A/D ports are mux configured in JSL. Script will disable 'D' if requested port is 'A' and vice-versa.
# @note         There is no pre-defined EFP index for DP_A or HDMI_A, hence these ports will be enabled at the end, when
#               all the requested LFP and EFP ports are configured. Any index which is free, will be considered for
#               these ports.
# @author       Sri Sumanth Geesala, Rohit Kumar
########################################################################################################################

import logging
import os
import sys
import unittest
from enum import Enum
from typing import Any
from xml.etree import ElementTree

from Libs import env_settings
from Libs.Core import cmd_parser, display_utility, reboot_helper, system_utility, driver_escape
from Libs.Core import display_essential, display_utility
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context, test_environment
from Libs.Core.vbt import vbt, vbt_context
from Libs.Core.wrapper.valsim_args import GfxPchFamily
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

LFP = 0
EFP = 1
LFP_EFP = 2
DE_HPD_INTERRUPT_2 = 0x44478

##
# All simulated eDP EDIDs have serial abc1230. Byte representation of 'ab' 'c1' '23' '00' in reverse
SIMULATED_EDP_SERIAL = [0x00, 0x23, 0xC1, 0xAB]

# List of DPCD offsets that should be checked for 'is_same_panel' condition. All the values should match.
DPCD_CAPS_OFFSETS = [
    0x007, 0x310, 0x311, 0x312, 0x313,  # VRR caps
    0x02E, 0x070,  # PSR caps
    0x314,  # LRR caps
]
DPCD_CAPS_OFFSETS += list(range(0x340, 0x356))  # HDR & B3 caps
DPCD_CAPS_OFFSETS += list(range(0x060, 0x070))  # VDSC caps 60h to 6Fh

##
# Port configuration (LFP/EFP) for all platforms
platform_port_configuration = {
    'APL': {'A': LFP, 'B': EFP, 'C': EFP},
    'KBL': {'A': LFP, 'B': EFP, 'C': EFP},
    'SKL': {'A': LFP, 'B': EFP, 'C': EFP, 'D': EFP},
    'CFL': {'A': LFP, 'B': EFP, 'C': EFP, 'D': EFP},
    'GLK': {'A': LFP, 'B': EFP, 'C': EFP},
    'CNL': {'A': LFP, 'B': EFP, 'C': EFP, 'D': EFP, 'E': EFP},
    'ICLLP': {'A': LFP, 'B': EFP, 'C': EFP, 'D': EFP, 'E': EFP, 'F': EFP},
    'JSL': {'A': LFP, 'B': EFP, 'C': EFP, 'D': EFP, 'E': EFP, 'F': EFP},
    'LKF1': {'A': LFP, 'C': LFP, 'D': EFP, 'E': EFP},
    'ICLHP': {'A': LFP_EFP, 'B': EFP, 'C': EFP, 'D': EFP, 'E': EFP, 'F': EFP},
    'TGL': {'A': LFP_EFP, 'B': LFP_EFP, 'C': LFP_EFP, 'D': EFP, 'E': EFP, 'F': EFP, 'G': EFP},
    'RYF': {'A': LFP_EFP, 'B': LFP_EFP, 'C': LFP_EFP, 'D': EFP, 'E': EFP},
    'DG1': {'A': LFP_EFP, 'B': LFP_EFP, 'C': EFP, 'D': EFP},
    'RKL': {'A': LFP_EFP, 'B': LFP_EFP, 'C': EFP, 'D': EFP},
    'LKFR': {'A': LFP_EFP, 'B': LFP_EFP, 'D': EFP, 'E': EFP},
    'DG2': {'A': LFP_EFP, 'B': LFP_EFP, 'C': EFP, 'D': EFP, 'F': EFP},
    'ADLS': {'A': LFP_EFP, 'B': LFP_EFP, 'C': EFP, 'D': EFP, 'E': EFP},
    'ADLP': {'A': LFP_EFP, 'B': LFP_EFP, 'C': LFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
    'MTL': {'A': LFP_EFP, 'B': LFP_EFP, 'C': LFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
    'ELG': {'A': LFP_EFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
    'LNL': {'A': LFP_EFP, 'B': LFP_EFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
    'PTL': {'A': LFP_EFP, 'B': LFP_EFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
    'NVL': {'A': LFP_EFP, 'B': EFP, 'F': EFP, 'G': EFP, 'H': EFP, 'I': EFP},
}

##
# DDC Bus mapping for all platforms
ddc_bus_mapping = {
    'APL': {'B': 0x01, 'C': 0x02, 'D': 0x03, 'F': 0x04},
    'KBL': {'B': 0x05, 'C': 0x04, 'D': 0x06},
    'SKL': {'B': 0x05, 'C': 0x04, 'D': 0x06},
    'CFL': {'B': 0x01, 'C': 0x02, 'D': 0x03, 'F': 0x04},
    'GLK': {'B': 0x01, 'C': 0x02, 'D': 0x03, 'F': 0x04},
    'CNL': {'B': 0x01, 'C': 0x02, 'D': 0x03, 'F': 0x04},
    'ICLLP': {'B': 0x02, 'C': 0x04, 'D': 0x05, 'E': 0x06, 'F': 0x07},
    'JSL': {'B': 0x02, 'C': 0x04, 'D': 0x05, 'E': 0x06, 'F': 0x07},
    'LKF1': {'D': 0x04, 'E': 0x05},
    'ICLHP': {'B': 0x02, 'C': 0x04, 'D': 0x05, 'E': 0x06, 'F': 0x07},
    'TGL': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04, 'E': 0x05, 'F': 0x06, 'G': 0x07},
    'RYF': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04, 'E': 0x05},
    'DG1': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04},
    'RKL': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04},
    'LKFR': {'A': 0x01, 'B': 0x02, 'D': 0x04, 'E': 0x05},
    'DG2': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04, 'F': 0x05},
    'ADLS': {'A': 0x01, 'B': 0x02, 'C': 0x03, 'D': 0x04, 'E': 0x05},
    'ADLP': {'A': 0x01, 'B': 0x02, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
    'MTL': {'A': 0x01, 'B': 0x02, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
    'ELG': {'A': 0x01, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
    'LNL': {'A': 0x01, 'B': 0x02, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
    'PTL': {'A': 0x01, 'B': 0x02, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
    'NVL': {'A': 0x01, 'B': 0x02, 'F': 0x03, 'G': 0x04, 'H': 0x05, 'I': 0x06},
}

##
# Temporary changes until migrated fully to PCH changes.
# DDC Bus mapping for all platforms
pch_ddc_bus_mapping = {
    GfxPchFamily.PCH_CMP_H: {'B': 0x01, 'C': 0x02, 'D': 0x03},
}

##
# VBT Port Index mapping for all platforms
port_index_mapping = {
    'APL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'KBL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'SKL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'CFL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'GLK': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'CNL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'ICLLP': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'JSL': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'LKF1': {'LFP': [0, 1], 'EFP': [2, 3]},
    'ICLHP': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'TGL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6, 7, 8]},
    'RYF': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6]},
    'DG1': {'LFP': [0], 'EFP': [1, 2, 3, 4]},
    'RKL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5]},
    'LKFR': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5]},
    'DG2': {'LFP': [0], 'EFP': [1, 2, 3, 4]},
    'ADLS': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'ADLP': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6, 7, 8]},
    'MTL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6]},
    'ELG': {'LFP': [0], 'EFP': [1, 2, 3, 4, 5]},
    'LNL': {'LFP': [0], 'EFP': [0, 1, 2, 3]},
    'PTL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5]},
    'NVL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6]},
    'CLS': {'LFP': [0], 'EFP': [1, 2, 3]},
}

##
# @brief        PrepareDisplaySetup Class
class PrepareDisplaySetup(unittest.TestCase):
    system_utility_ = None
    display_config_ = None
    driver_interface_ = None
    display_list = {}  # Contains adapter wise display list. {'gfx_0': ['DP_A']}
    param_list = {}  # Contains adapter wise display parameters {'gfx_0': {'DP_A': {'edid_name':''}}}
    requested_lfp_list = {}  # Contains adapter wise LFP list
    requested_efp_list = {}  # Contains adapter wise EFP list
    platform_vbt_list = {}  # contains adapter wise VBT objects (like {'gfx_0': vbt_obj1, 'gfx_1': vbt_obj2}
    platform_info = {}
    skip_reboot = False

    ##
    # @brief        Constructor
    # @param[in]   args command line arguments used to fill the instance members
    # @param[in]   kwargs keyword arguments used to fill the instance members
    def __init__(self, *args, **kwargs):
        super(PrepareDisplaySetup, self).__init__(*args, **kwargs)
        self.skip_reboot = False

        self.system_utility_ = system_utility.SystemUtility()
        self.display_config_ = display_config.DisplayConfiguration()
        self.driver_interface_ = driver_interface.DriverInterface()
        self.system_info = machine_info.SystemInfo()

        self.platform_info = {
            gfx_index: {
                'gfx_index': gfx_index,
                'name': adapter_info.get_platform_info().PlatformName,
                'pch': GfxPchFamily(self.driver_interface_.get_platform_details(gfx_index).GfxPchFamily)
            }
            for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
        }

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        Setup method
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self) -> None:
        # Clear GDHM report (if any)
        gdhm.clear_report()

        ##
        # prepare_display_setup.py takes entire command line as input, which includes all the custom tags present in the
        # command line. The command line parser asks to define custom tags beforehand. Hence, we need to pass all the
        # custom tags present in command line to parse_cmdline() API.
        custom_tags = cmd_parser.get_custom_tag()
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        self.cmd_params = cmd_parser.parse_cmdline(sys.argv, custom_tags)

        # Handle multi-adapter scenario
        if not isinstance(self.cmd_params, list):
            self.cmd_params = [self.cmd_params]

        # Get display list, display parameters, LFPs, EFPs for each platform
        for platform in self.platform_info.values():
            adapter = platform['gfx_index']  # gfx_0
            self.display_list[adapter] = [
                display_info[adapter] for display_info in cmd_parser.get_sorted_display_list(self.cmd_params)
                if adapter in display_info.keys()]

            # cmd_params contain adapter parameters based on index. index 0 represents parameters for gfx_0
            # Using the same to get display parameters for given adapter and display
            # See parse_cmdline() API in cmd_parser module for more info
            # param_list = {'gfx_0': {'DP_A': {'index': 0, 'edid_name': '', ...}}, 'gfx_1': {'HDMI_C': {...}, ...}}
            self.param_list[adapter] = {}
            for display, params in self.cmd_params[int(adapter[-1])].items():
                if cmd_parser.display_key_pattern.match(display) is None:
                    continue
                display = '_'.join(display.split('_')[:2])
                if 'EDP' in display:
                    display = display[1:]
                if display in self.display_list[adapter]:
                    self.param_list[adapter][display] = params

            self.requested_lfp_list[adapter] = []
            self.requested_efp_list[adapter] = []
            for port_name in self.display_list[adapter]:
                if self.param_list[adapter][port_name]['is_lfp'] is True:
                    self.requested_lfp_list[adapter].append(port_name)
                else:
                    self.requested_efp_list[adapter].append(port_name)

            # As there is no fixed block assigned for external DP_A/HDMI_A, we are computing it at the last by finding a
            # free element in get_index(). Moving DP_A/HDMI_A to the end of EFP list.
            for port_name in ['DP_A', 'HDMI_A']:
                if port_name in self.requested_efp_list[adapter]:
                    self.requested_efp_list[adapter].remove(port_name)
                    self.requested_efp_list[adapter].append(port_name)

            # Rearranging display list to keep LFPs first. Port present first in the list will be enabled first, this
            # way, preference is given to LFPs.
            self.display_list[adapter] = self.requested_lfp_list[adapter] + self.requested_efp_list[adapter]
            dut_info = self.system_info.get_platform_details(adapter_dict[adapter].deviceID)

        # Validate given command line for each adapter
        for platform in self.platform_info.values():
            # Make sure VBT simulation is supported on targeted platform
            if platform['name'] not in platform_port_configuration.keys():
                gdhm.report_bug(
                    f"[PrepareDisplaySetup] VBT Simulation not supported on {platform['name']} ",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                self.fail(f"VBT simulation is NOT supported on {platform['name']}")

            # Validate each targeted display
            for display in self.display_list[platform['gfx_index']]:
                ddi = display.split('_')[1]

                # Make sure requested port is supported by platform
                if ddi not in platform_port_configuration[platform['name']].keys():
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] Unsupported port {display} requested on {platform['name']}",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"Port {display} is NOT supported on {platform['name']}(CommandLine Issue)")

                # Make sure requested LFP port is supported by platform
                if self.param_list[platform['gfx_index']][display]['is_lfp'] and \
                        platform_port_configuration[platform['name']][ddi] == EFP:
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] Unsupported LFP port {display} is requested on {platform['name']}",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"LFP port {display} is NOT supported on {platform['name']}(CommandLine Issue)")

                # Make sure requested EFP port is supported by platform
                if not self.param_list[platform['gfx_index']][display]['is_lfp'] and \
                        platform_port_configuration[platform['name']][ddi] == LFP:
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] Unsupported EFP port {display} requested on {platform['name']}",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"EFP port {display} is NOT supported on {platform['name']}(CommandLine Issue)")

                # @note EDP_C is not supported for now. Fail if present in command line.
                if display == 'DP_C' and self.param_list[platform['gfx_index']][display]['is_lfp']:
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] LFP port {display} is NOT supported(CommandLine Issue)",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"LFP port {display} is NOT supported(CommandLine Issue)")

            disp_list = self.display_list[platform['gfx_index']]
            if platform['name'] == 'PTL' and dut_info.SkuName != "WCL":
                if 'HDMI_B' in disp_list or (
                        'DP_B' in disp_list and not self.param_list[platform['gfx_index']]['DP_B']['is_lfp']):
                    self.fail("DP_B/HDMI_B ports cannot be configured in PTL(CommandLine Issue)")

                tc1_ports = {'DP_F', 'HDMI_F'}
                if 'DP_B' in disp_list and tc1_ports.intersection(set(disp_list)):
                    self.fail("Port_B and Port_F cannot be combined in PTL. (CommandLine Issue)")
            self.validate_vbt_index_commandline()

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        # @note WA for ValSim plug/unplug. If pre-si yangra, write 0x0 to 0x44478. Only after this register is reset
        # to 0x0 ValSim plug/unplug will work in pre-si yangra.
        if self.system_utility_.get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            for platform in self.platform_info.values():
                if self.driver_interface_.mmio_write(DE_HPD_INTERRUPT_2, 0x0, gfx_index=platform['gfx_index']) is False:
                    logging.error(f"Failed to write DE_HPD_INTERRUPT_2({hex(DE_HPD_INTERRUPT_2)}) "
                                  f"for {platform['name']}")
                else:
                    logging.info(f"DE_HPD_INTERRUPT_2({hex(DE_HPD_INTERRUPT_2)}) register offset is reset to 0x0 "
                                 f"for {platform['name']}")

        # Prepare_Display script should not fail due to UnderRun/TDR issue, it will be logged as warning.
        # UnderRun/TDR occurred during prepare display will be reported and tracked through gdhm.

        # Verify UnderRun and Clear underrun registry so that it will not fail during Test Environment cleanup
        UnderRunStatus.verify_underrun()
        UnderRunStatus.clear_underrun_registry()
        UnderRunStatus.skip_underrun_check = True
        VerifierCfg.underrun = Verify.SKIP
        VerifierCfg.tdr = Verify.SKIP

        # Verify and Clear TDR so that it will not fail during Test Environment cleanup
        for platform in self.platform_info.values():
            display_essential.detect_system_tdr(gfx_index=platform['gfx_index'])

    ##
    # @brief        Runtest Method
    # @return       None
    def runTest(self) -> None:
        is_driver_restart_required = False
        is_reboot_required = False
        is_adlp_platform = any([_platform['name'] == 'ADLP' for _platform in self.platform_info.values()])
        is_ptl_platform = any([_platform['name'] == 'PTL' for _platform in self.platform_info.values()])

        for platform in self.platform_info.values():
            self.platform_vbt_list[platform['gfx_index']] = vbt.Vbt(platform['gfx_index'])

        # Handle reset request
        if self.cmd_params[0]['RESET'] != 'NONE':
            if reboot_helper.is_reboot_scenario():
                # This block will be executed after reboot only
                logging.info("\tPASS: VBT reset completed successfully")
                return

            # Reset VBT for each platform
            logging.info("Step: Reset VBT simulation")
            for platform in self.platform_info.values():
                logging.info(f"\tResetting VBT for {platform['name']}")
                if self.platform_vbt_list[platform['gfx_index']].reset() is False:
                    self.fail(f"Failed to reset VBT for {platform['name']}")

            # Every reset request requires reboot. Set reboot_required flag to True
            is_reboot_required = True
        else:
            # Handle VBT configuration
            if not reboot_helper.is_reboot_scenario():
                if is_ptl_platform and self.is_port_f_present():
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    connected_disps = [
                        CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[count].ConnectorNPortType).name
                        for count in range(enumerated_displays.Count)]
                    if 'DP_B' in connected_disps and display_utility.unplug(port='DP_B') is False:
                        self.fail("Failed to unplug DP_B")
                    logging.info(f"Unplug of DP_B is successful")
                    is_reboot_required = True

                # WA to reboot the driver in case of dual eDP in ADLP platform
                elif is_adlp_platform and self.is_edp_b_present():
                    is_reboot_required = self.handle_vbt_configuration()
                else:
                    is_driver_restart_required = self.handle_vbt_configuration()
            else:
                # verifying ports in case of reboot case
                self.verify_port_configuration()

            # Handle MIPI panel simulation
            is_reboot_required |= self.handle_mipi_simulation()

            if (is_driver_restart_required is True) and (is_reboot_required is False):
                logging.info(f"Step: Restart display driver")
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False and reboot_required is True:
                    logging.info("\tFailed to restart driver, rebooting system as requested by OS.")
                    is_reboot_required = reboot_required
                elif status is False and reboot_required is False:
                    self.fail("Failed to restart display driver")

                # verifying ports in case of non-reboot case, i.e in this case only driver restart sufficed.
                if not is_reboot_required:
                    self.verify_port_configuration()

            # Handle eDP simulation if at least one Yangra platform is present
            is_reboot_required |= self.handle_edp_simulation()

        # Reboot the system, if reboot_required flag is not set
        if self.skip_reboot is False:
            if is_reboot_required and reboot_helper.reboot(self, 'runTest') is False:
                self.fail("Failed to reboot the system")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Helper function for verifying if requested ports are configured with appropriate vbt index
    # @param[in]    gfx_vbt - Vbt, VBT object from vbt module
    # @param[in]    platform - dictionary, Platform info
    # @param[in]    supported_ports - dictionary, Existing supported ports for given platform
    # @return       status - True if verification successful, False if VBT needs to be configured
    def verify_port_index_configuration(self, gfx_vbt: vbt.Vbt, platform: dict, supported_ports: dict) -> bool:
        for display in self.display_list[platform['gfx_index']]:
            params = self.param_list[platform['gfx_index']][display]
            display_type = display.split('_')[0]  # DP/HDMI/...

            # Step 1: Check for Supported Ports to be configured in current platform
            port_type = 'EMBEDDED' if params['is_lfp'] else params['connector_port_type']
            if not (display in supported_ports and supported_ports[display] == port_type):
                # Return here since requested port is not available in the supported port list
                force_lfp_tag = env_settings.get('SIMULATION', 'lfp_simulation')
                if port_type == 'EMBEDDED' and force_lfp_tag != 'ENABLE':
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] LFP port simulation request received with invalid config.ini settings",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(
                        f'LFP port {display} requested for simulation, but LFP simulation is disabled in config.ini')
                logging.info(f"Requested port(s) is/are not present in supported port list!")
                return False
            else:
                # Proceed to check for vbt_index mapping for current port
                logging.debug(f"Requested port {display} already configured {port_type} in supported port list")

            # Step 2: Check matching VBT port index for requested display and expected VBT configuration
            if params['vbt_index'] is not None:
                # If commandline contains vbt index, verify if requested port is configured in VBT
                display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[int(params['vbt_index'].split("_")[-1])]
                if not (vbt_context.DVO_PORT_MAPPING[display] == display_entry.DVOPort and
                        vbt_context.DEVICE_CLASS["LFP_" + display_type] == display_entry.DeviceClass):
                    # If requested vbt index is not configured to requested port. Perform Disable ports in next step
                    logging.info(f"Different VBT indices observed for {display}")
                    return False

        logging.info(f"Requested ports are already configured in supported port list")
        return True

    ##
    # @brief        Helper function to obtain port name based on DVO Port mapping data
    # @param[in]    gfx_vbt - Vbt, VBT object from vbt module
    # @param[in]    index - int, VBT port index to fetch the display type
    # @return       port_name - Return port name if DeviceClass is mapped to valid display type Else None
    def get_display_type(self, gfx_vbt: vbt.Vbt, index: int) -> Any:
        if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass == 0x0:
            return None
        return vbt_context.DVO_PORT_NAMES[gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DVOPort]

    ##
    # @brief        Helper function to Validate vbt index custom command lines
    # @return       None
    def validate_vbt_index_commandline(self) -> None:
        logging.info("Step: Validate VBT index option in commandline")
        self.vbt_config = {}

        for platform in self.platform_info.values():
            adapter = platform['gfx_index']
            # Default values to VBT index configuration type
            self.vbt_config[adapter] = {'LFP': VbtConfigType.DYNAMIC, 'EFP': VbtConfigType.DYNAMIC}

            # update static / dynamic based on validation pass criteria
            lfp_current_config = []
            efp_current_config = []
            for display, params in self.cmd_params[int(adapter[-1])].items():
                if cmd_parser.display_key_pattern.match(display) is None:
                    continue

                vbt_config = VbtConfigType.STATIC if params['vbt_index'] is not None else VbtConfigType.DYNAMIC
                lfp_current_config.append(vbt_config) if params['is_lfp'] is True else efp_current_config.append(
                    vbt_config)
                # Validate if last character in vbt_index parameter is integer
                if vbt_config == VbtConfigType.STATIC and not params['vbt_index'].split("_")[-1].isdigit():
                    self.fail(f"Invalid VBT index parameter passed - {params['vbt_index']}")
                # Validate if the requested VBT index is present in port_index_mapping dictionary
                if params['vbt_index'] is not None and int(params['vbt_index'].split("_")[-1]) not in \
                        port_index_mapping[platform['name']]['LFP' if params['is_lfp'] else 'EFP']:
                    self.fail(f"Invalid VBT index {params['vbt_index']} for {display} passed in commandline")

            if not all(config == lfp_current_config[0] for config in lfp_current_config) or \
                    not all(config == efp_current_config[0] for config in efp_current_config):
                self.fail("Invalid commandline passed!")

            self.vbt_config[adapter]['LFP'] = VbtConfigType(list(set(lfp_current_config))[0]) \
                if len(lfp_current_config) > 0 else VbtConfigType.DYNAMIC
            self.vbt_config[adapter]['EFP'] = VbtConfigType(list(set(efp_current_config))[0]) \
                if len(efp_current_config) > 0 else VbtConfigType.DYNAMIC
            logging.debug(f"  Updating VBT config for LFP as {self.vbt_config[adapter]['LFP']}")
            logging.debug(f"  Updating VBT config for EFP as {self.vbt_config[adapter]['EFP']}")

    ##
    # @brief        Helper function for handling VBT configuration
    # @return       status - Boolean, True if a reboot is required, False otherwise
    def handle_vbt_configuration(self) -> bool:
        status = False

        # Configure VBT for each platform
        for platform in self.platform_info.values():
            logging.info(f"Step: Configure display ports in VBT for {platform['name']}")

            platform_status = False
            gfx_vbt = self.platform_vbt_list[platform['gfx_index']]
            supported_ports = display_config.get_supported_ports(gfx_index=platform['gfx_index'])
            logging.info(f"Initial VBT index configuration - {platform['name']}")
            self.log_vbt_configuration(gfx_vbt, platform)

            # Step 1: Verification of ports
            is_port_index_updated = self.verify_port_index_configuration(gfx_vbt, platform, supported_ports)

            for display in self.display_list[platform['gfx_index']]:
                params = self.param_list[platform['gfx_index']][display]
                ddi = display.split('_')[1]  # A/B/C/...

                # Disable on board LSPCON
                # 2nd bit in Flags1, specify lspcon status
                # 0 - disabled, 1 - enabled
                if params['is_lfp'] is False and platform['name'] in ['CFL', 'GLK']:
                    if display in supported_ports.keys():
                        index, _ = self.get_index(gfx_vbt, ddi, False, platform)
                        if index is not None:
                            is_lspcon_enabled = (gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].Flags1 >> 2) & 1
                            if is_lspcon_enabled:
                                logging.info(f"\t{display}: Disabling on-board LSPCON")
                                gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].Flags1 &= (~(1 << 2))
                                logging.info(f"\t\tDisplayEntry: Index= {index}, Flags1= "
                                             f"{hex(gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].Flags1)}")
                                platform_status = True

                if platform['name'] == 'PTL' and ddi in ['B', 'F']:
                    port_ddi = 'B' if ddi == 'F' else 'F'
                    index, _ = self.get_index(gfx_vbt, port_ddi, not params['is_lfp'], platform)
                    self.disable_port(gfx_vbt, index, port_ddi, not params['is_lfp'], platform)
                    platform_status = True

            # If requested ports are either not in supported port list or mismatched with vbt_index
            if is_port_index_updated is False:
                # Step 2: Disable all ports
                self.disable_ports(gfx_vbt, platform)

                # Step 3: Enable all ports
                self.enable_ports(gfx_vbt, platform)

                platform_status = True

            if platform_status is False:
                logging.info(f"\tAll requested ports in {platform} are already enabled. Skipping VBT simulation.")
            else:
                if gfx_vbt.apply_changes() is False:
                    self.fail(f"Setting VBT block failed for {platform['name']}")

            logging.info(f"Final VBT index configuration - {platform['name']}")
            self.log_vbt_configuration(gfx_vbt, platform)
            status |= platform_status

        return status

    ##
    # @brief        Helper function for handling MIPI panel simulation
    # @return       status - Boolean, True if driver restart is required, False otherwise
    def handle_mipi_simulation(self) -> bool:
        force_lfp_tag = env_settings.get('SIMULATION', 'lfp_simulation')
        if force_lfp_tag != 'ENABLE':
            logging.info("LFP simulation is disabled in config.ini. Skipping MIPI simulation.")
            return False

        if reboot_helper.is_reboot_scenario():
            # This block will be executed only after reboot
            self.verify_mipi_simulation()
            return False

        # Handle MIPI panel simulation
        is_reboot_required = False
        for platform in self.platform_info.values():
            gfx_vbt = self.platform_vbt_list[platform['gfx_index']]
            gfx_index = platform['gfx_index']
            mipi_ports_requested = [port for port in self.requested_lfp_list[platform['gfx_index']] if 'MIPI' in port]
            if len(mipi_ports_requested) == 0:
                continue

            logging.info(f"Step: Simulate requested MIPI(s) on {platform['name']}")

            platform_status = False
            for port in mipi_ports_requested:
                params = self.param_list[gfx_index][port]

                # if 'panel_index' is not passed in cmdline, filling default MIPI PanelIndex.
                if params['panel_index'] is None:
                    if platform['name'] == 'LKF1':
                        # LKF POR panel (contains both block 42 (for vbt_version < 229) and 58 (for vbt_version >= 229))
                        params['panel_index'] = 'MIP001'
                    elif platform['name'] == 'TGL':
                        if gfx_vbt.version < 229:
                            # using LKF POR panel since block 58 not present in VBT version < 229
                            params['panel_index'] = 'MIP001'
                        else:
                            # WA: using LKF panel for TGL since TGL panel has known underrun issue (1608585678).
                            # Change this to MIP005 once issue fixed.
                            params['panel_index'] = 'MIP001'
                            # TGL POR panel. Uses new block 58 for timing data (block 42 not doable for this panel)
                            # params['panel_index'] = 'MIP005'
                    else:
                        params['panel_index'] = 'MIP001'

                panel_index = gfx_vbt.get_lfp_panel_type(port)

                # parse MIPI xml, check if requested MIPI panel is already connected (check based on PnP Id)
                requested_panel_info = display_utility.get_panel_edid_dpcd_info(port, params['panel_index'], True)
                mipi_xml_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "MIPI", requested_panel_info["edid"])
                if not os.path.exists(mipi_xml_file):
                    self.fail(f"No MIPI xml file present at location {mipi_xml_file}")

                xml_root = ElementTree.parse(mipi_xml_file).getroot()
                mfg_name = product_code = serial_num = week_of_mfg = year_of_mfg = 0
                for field in xml_root.findall('Field'):
                    path = field.find('Path').text
                    value = field.find('Value').text
                    if 'IdMfgName' in path:
                        mfg_name = int(value, 16)
                    if 'IdProductCode' in path:
                        product_code = int(value, 16)
                    if 'IDSerialNumber' in path:
                        serial_num = int(value, 16)
                    if 'WeekOfMfg' in path:
                        week_of_mfg = int(value, 16)
                    if 'YearOfMfg' in path:
                        year_of_mfg = int(value, 16)

                input_panel_pnp_id = str(mfg_name) + str(product_code) + str(serial_num) + str(week_of_mfg)
                input_panel_pnp_id += str(year_of_mfg)

                mfg_name = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IdMfgName
                product_code = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IdProductCode
                serial_num = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IDSerialNumber
                week_of_mfg = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].WeekOfMfg
                year_of_mfg = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].YearOfMfg
                current_panel_pnp_id = str(mfg_name) + str(product_code) + str(serial_num) + str(week_of_mfg)
                current_panel_pnp_id += str(year_of_mfg)
                if input_panel_pnp_id == current_panel_pnp_id:
                    logging.info(f"\tVBT PNP ID is matched for {port}. Verifying Panel enumeration")
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    if display_config.is_display_attached(enumerated_displays, port, gfx_index) is False:
                        self.fail(f"Panel is not enumerated on {port}")
                    logging.info(f"\tPanel is enumerated on {port}")
                    continue

                logging.info(f"\tPlugging {params['panel_index']} using {requested_panel_info['edid']} on port {port}")

                # parse MIPI xml, set MIPI panel data in VBT
                for field in xml_root.findall('Field'):
                    block_no = field.find('Block').text
                    path = field.find('Path').text
                    value = field.find('Value').text

                    vbt_expression = 'gfx_vbt.block_' + str(block_no) + '.' + str(path) + ' = ' + str(value)
                    vbt_expression = vbt_expression.replace('{panel_index}', str(panel_index))
                    cur_block = eval('gfx_vbt.block_' + str(block_no))
                    if cur_block is not None:
                        exec(vbt_expression)
                platform_status = True

            if platform_status:
                # if we are simulating dual link MIPI panel, we have to disable MIPI_C (DSI_1) port,
                # since dual link will internally use both MIPI ports to drive single MIPI display
                if gfx_vbt.block_52.MipiDataStructureEntry[gfx_vbt.block_40.PanelType].DualLinkSupport != 0:
                    temp_index, _ = self.get_index(gfx_vbt, 'C', True, platform)
                    disable_port_status = self.disable_port(gfx_vbt, temp_index, 'C', True, platform)
                    logging.info(f" VBT port disable status for dual link MIPI scenario - {disable_port_status}")
                # apply VBT since MIPI panel related fields were updated in VBT
                if gfx_vbt.apply_changes() is False:
                    self.fail(f"Setting VBT block failed for {platform['name']}")

            # After MIPI panel simulation, reboot is recommended. Driver disable-enable causes issues with certain
            # cases.
            # e.g. In pre-si when changing from port_sync panel to non_port_sync panel, pre-si environment is crashing
            # if we do driver disable-enable. In all cases, system reboot works and is recommended.
            is_reboot_required |= platform_status

        # end of operations for this platform

        return is_reboot_required

    ##
    # @brief        Helper function for verifying status after performing MIPI panel simulation
    # @return       None
    def verify_mipi_simulation(self) -> None:

        status = True
        # after MIPI simulation in VBT, make sure all requested MIPI panels are simulated successfully or not
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for platform in self.platform_info.values():
            logging.info(f"Step: Verify simulated MIPI(s) for {platform['name']}")
            for port in self.requested_lfp_list[platform['gfx_index']]:
                if 'MIPI' not in port:
                    continue
                if display_config.is_display_attached(
                        enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                    logging.error(f"\t{port}: NOT simulated")
                    status = False
                else:
                    logging.info(f"\t{port}: Simulated successfully")

        if status is False:
            gdhm.report_bug(
                f"[PrepareDisplaySetup] MIPI simulation is not working",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            self.fail("Requested MIPI(s) are NOT simulated. MIPI simulation is NOT working.")
        logging.info("\tPASS: All requested MIPI panels are simulated successfully")

    ##
    # @brief        Helper function for handling eDP simulation
    # @return       status- Boolean, True if a reboot is required, False otherwise
    def handle_edp_simulation(self) -> bool:
        if reboot_helper.is_reboot_scenario():
            # This block will be executed only after reboot
            force_lfp_tag = env_settings.get('SIMULATION', 'lfp_simulation')
            if force_lfp_tag != 'ENABLE':
                return False

            status = True
            for platform in self.platform_info.values():
                logging.info(f"Step: Verify simulated eDP(s) for {platform['name']}")
                # Make sure all requested eDP panels are simulated successfully or not
                enumerated_displays = self.display_config_.get_enumerated_display_info()
                for port in self.requested_lfp_list[platform['gfx_index']]:
                    if 'DP' not in port:
                        continue
                    if display_config.is_display_attached(
                            enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\t{port}: NOT simulated")
                        status = False
                    else:
                        logging.info(f"\t{port}: Simulated successfully")

            if status is False:
                gdhm.report_bug(
                    f"[PrepareDisplaySetup] eDP simulation is not working",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                self.fail("Requested eDP(s) are NOT simulated. EDP simulation is NOT working.")
            logging.info("\tPASS: All requested eDP panels are simulated successfully")
            return False

        force_lfp_tag = env_settings.get('SIMULATION', 'lfp_simulation')
        if force_lfp_tag != 'ENABLE':
            logging.info("LFP simulation is disabled in config.ini. Skipping eDP simulation.")
            return False

        status = False
        for platform in self.platform_info.values():
            logging.info(f"Step: Simulate requested eDP(s) on {platform['name']}")

            enumerated_displays = self.display_config_.get_enumerated_display_info()
            target_id_mapping = dict()
            for display_index in range(enumerated_displays.Count):
                display = enumerated_displays.ConnectedDisplays[display_index]
                if platform['gfx_index'] == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                    target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

            # Handle lfp_none : unplug already connected LFP if requested
            if self.cmd_params[int(platform['gfx_index'][-1])]['LFP_NONE'] != 'NONE':
                for port in target_id_mapping.keys():
                    vbt_panel_type = display_utility.get_vbt_panel_type(port, platform['gfx_index'])
                    if vbt_panel_type != display_utility.VbtPanelType.LFP_DP or not display_config.is_display_attached(
                            enumerated_displays, port, gfx_index=platform['gfx_index']):
                        continue

                    # Get EDID of connected panel
                    edid_flag, connected_panel_edid, _ = driver_escape.get_edid_data(target_id_mapping[port])
                    if not edid_flag:
                        logging.error(f"Failed to get EDID data for target_id : {target_id_mapping[port]}")
                        self.fail()
                    if connected_panel_edid[12:16] != SIMULATED_EDP_SERIAL:
                        logging.error(f"\t{port} is a physical LFP panel. Can not be unplugged. (Planning Issue)")
                        continue

                    if display_utility.unplug(port=port, is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to unplug {port}")
                    else:
                        logging.info(f"\tUnplugged {port} successfully")
                        status = True

            # Skip eDP simulation if there is no eDP panel present in command line
            if len(self.requested_lfp_list[platform['gfx_index']]) < 1:
                logging.info(f"\tNo eDP panel requested for {platform['name']}. Skipping eDP simulation.")
                continue

            for port in self.requested_lfp_list[platform['gfx_index']]:
                if 'DP' not in port:
                    continue

                params = self.param_list[platform['gfx_index']][port]

                # First check if there is any LFP present on requested port or not, if not, simulation is required.
                # No need to check any further
                if display_config.is_display_attached(
                        enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                    self.__initialize_lfp_port(platform['gfx_index'], port)
                    if display_utility.plug(
                            port=port, edid=params['edid_name'], dpcd=params['dpcd_name'],
                            panelindex=params['panel_index'], is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to plug {port}")
                    status = True
                    continue

                # If some panel is already present, check if connected and requested panels are same or not. If same,
                # skip eDP simulation, otherwise plug the requested panel

                # Get EDID of connected panel
                edid_flag, connected_panel_edid, _ = driver_escape.get_edid_data(target_id_mapping[port])
                if not edid_flag:
                    logging.error(f"Failed to get EDID data for target_id : {target_id_mapping[port]}")
                    self.fail()
                # Get EDID file path from PanelInputData.xml
                requested_panel_info = display_utility.get_panel_edid_dpcd_info(port, params['panel_index'], True)
                edid_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "eDP_DPSST",
                                         requested_panel_info["edid"])
                dpcd_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST',
                                         requested_panel_info['dpcd'])
                if not os.path.exists(edid_file):
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] No EDID File Found",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"No EDID file present at location {edid_file}")

                if not os.path.exists(dpcd_file):
                    gdhm.report_bug(
                        f"[PrepareDisplaySetup] No DPCD File Found",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"No DPCD file present at location {dpcd_file}")

                with open(edid_file, "rb") as f:
                    requested_edid_data = f.read()
                requested_edid_data = [int(b) for b in requested_edid_data]

                # Check number of extension blocks
                is_same_panel = True
                if connected_panel_edid[126] == requested_edid_data[126]:
                    # For each extension block, verify the checksum
                    for block_index in range(connected_panel_edid[126] + 1):
                        checksum_index = (128 * block_index) + 127
                        if connected_panel_edid[checksum_index] != requested_edid_data[checksum_index]:
                            is_same_panel = False
                            break
                else:
                    is_same_panel = False

                # Do a DPCD capability check to handle same EDID but different DPCD case.
                if is_same_panel:
                    # Get DPCD offsets and values present in DPCD file
                    requested_dpcd_data = {}
                    with open(dpcd_file) as f:
                        for line in f.readlines():
                            line = line.strip()
                            if line.startswith(';') or ':' not in line:
                                continue
                            start_offset = int(line.split(':')[0], 0)
                            values = line.split(':')[1].strip().split('.')[0].split(',')
                            for value in values:
                                requested_dpcd_data[start_offset] = int(value, 16)
                                start_offset += 1

                    # Read DPCD data from connected panel
                    current_dpcd_data = {}
                    for offset in DPCD_CAPS_OFFSETS:
                        dpcd_flag, dpcd_value = driver_escape.read_dpcd(target_id_mapping[port], offset)
                        if dpcd_flag is False:
                            logging.error(
                                f"Failed to read DPCD for target_id ({target_id_mapping[port]}) at offset ({offset})")
                        current_dpcd_data[offset] = dpcd_value[0]

                    for offset, value in current_dpcd_data.items():
                        if value != requested_dpcd_data.get(offset, 0):
                            is_same_panel = False
                            logging.debug(
                                f"\tDPCD offset {hex(offset)} value is not matching. "
                                f"Requested= {hex(requested_dpcd_data.get(offset, 0))}, Current= {hex(value)}")
                            logging.info(f"\tDPCD is not matching with panel connected on {port}")
                            break

                if is_same_panel:
                    logging.info(f"\tRequested eDP panel is already connected on {port}")
                else:
                    ##
                    # Check whether connected panel is Physical or Simulated
                    if connected_panel_edid[12:16] != SIMULATED_EDP_SERIAL:
                        logging.warning(f"\tA different physical eDP panel is connected on {port}")
                    self.__initialize_lfp_port(platform['gfx_index'], port)
                    if display_utility.plug(
                            port=port, edid=params['edid_name'], dpcd=params['dpcd_name'],
                            panelindex=params['panel_index'], is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to plug {port}")
                    status = True
        return status

    ##
    # @brief        Helper function for Disabling specific port in VBT
    # @param[in]    gfx_vbt- Vbt, VBT object from vbt module
    # @param[in]    index- integer, VBT port index
    # @param[in]    ddi- string, Port DDI
    # @param[in]    is_lfp- boolean, True if Embedded display Else False
    # @param[in]    platform- dictionary, Platform info
    # @return       status- boolean, True if disable successful Else False
    def disable_port(self, gfx_vbt: vbt.Vbt, index: int, ddi: Any, is_lfp: Any, platform: dict) -> bool:
        if ddi is None:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass = 0x0  # Disabled requested VBT index
            return True

        if is_lfp:
            if platform_port_configuration[platform['name']][ddi] not in [LFP, LFP_EFP]:
                logging.error(f"LFP port with ddi {ddi} not supported in - {platform['name']}")
                return False
        else:
            if platform_port_configuration[platform['name']][ddi] not in [LFP_EFP, EFP]:
                logging.error(f"EFP port with ddi {ddi} not supported in - {platform['name']}")
                return False

        # call disable port for individual display to be simulated
        if index is not None:
            # Check if port is already disabled
            if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass == 0x0:
                logging.error(f"Port at VBT index {index} Already disabled")
                return False

            # Check if port is LFP/EFP
            if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass in \
                    [vbt_context.DEVICE_CLASS['LFP_MIPI'], vbt_context.DEVICE_CLASS['LFP_DP']]:
                if not is_lfp:
                    return False
            else:
                if is_lfp:
                    return False

            logging.info("\t\tDisabling {0} on DDI {1}".format("LFP" if is_lfp else "EFP", ddi))
            logging.info(f"\t\t\tDisplayEntry: Index= {index}, DeviceClass= 0x0")
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass = 0x0
        else:
            logging.error(f" Invalid Index {index} passed to be disabled !!")
        return True

    ##
    # @brief        Helper function for Disable all required port(s) in VBT
    # @param[in]    gfx_vbt- Vbt, VBT object from vbt module
    # @param[in]    platform- dictionary, Platform info
    # @return       None
    def disable_ports(self, gfx_vbt: vbt.Vbt, platform: dict) -> None:
        logging.info(f"Step: Disable Ports on '{platform['name']}'")
        for panel_type in self.vbt_config[platform['gfx_index']].keys():
            if self.vbt_config[platform['gfx_index']][panel_type] == VbtConfigType.STATIC:
                # Disable all configured VBT indices for requested panel type (LFP/EFP)
                valid_port_index_list = [port for port in port_index_mapping[platform['name']][panel_type]]
                for index in valid_port_index_list:
                    status = self.disable_port(gfx_vbt, index, None, None, platform)
                    logging.info(f"{'PASS' if status is True else 'FAIL'}: Disable port index {index} for {panel_type}")

        for display in self.display_list[platform['gfx_index']]:
            params = self.param_list[platform['gfx_index']][display]
            ddi = display.split('_')[1]  # A/B/C/...

            # Skip disable port for EFPs with no corresponding LFP mapping
            if params['is_lfp'] is False and ddi not in ['A', 'B'] and platform['name'] != 'JSL':
                continue

            # To disable ddi B with alternative connector port types during MIPI_C scenario
            if ddi == 'C' and display.startswith('MIPI'):
                ddi = 'B'

            # Disable all configured VBT index for alternative panel type (LFP in case EFP requested and vice-versa)
            # - If EDP_A / MIPI_A in display_list, disable port for DP_A / HDMI_A
            # - If EDP_B / MIPI_C in display_list, disable port for DP_B / HDMI_B
            # - If DP_A / HDMI_A in display_list, disable port for EDP_A / MIPI_A
            # - If DP_B / HDMI_B in display_list, disable port for EDP_B / MIPI_C
            ddi_list = ['B', 'C'] if (params['is_lfp'] is False and ddi == 'B') else [ddi]

            # Call Disable ports for corresponding LFP / EFP mapping indices
            for ddi in ddi_list:
                index, is_port_configured = self.get_index(gfx_vbt, ddi, not params['is_lfp'], platform)
                if is_port_configured is True:
                    logging.info(f"Step: Disable already configured {'EFP' if params['is_lfp'] else 'LFP'} Ports")
                    status = self.disable_port(gfx_vbt, index, ddi, not params['is_lfp'], platform)
                    logging.info(f"{'PASS' if status is True else 'FAIL'}: Disable port index {index} for ddi - {ddi}")

    ##
    # @brief        Helper function for Enable all required port(s) in VBT
    # @param[in]    gfx_vbt- Vbt, VBT object from vbt module
    # @param[in]    platform- dictionary, Platform info
    # @return       None
    def enable_ports(self, gfx_vbt: vbt.Vbt, platform: dict) -> None:
        logging.info(f"Step: Enable requested ports on '{platform['name']}'")
        enabled_index_list = []

        for display in self.display_list[platform['gfx_index']]:
            params = self.param_list[platform['gfx_index']][display]
            ddi = display.split('_')[1]  # A/B/C/...
            display_type = display.split('_')[0]  # DP/HDMI/...

            if params['vbt_index'] is not None:
                index = int(params['vbt_index'].split("_")[-1])
            else:
                index, _ = self.get_index(gfx_vbt, ddi, params['is_lfp'], platform, enabled_index_list)

            # Append current index to enabled port index list to exclude the same in next iteration
            enabled_index_list.append(index)

            logging.info(f"\tEnabling port {display} on VBT index - {index}")
            display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

            # set DeviceClass, DVOPort, DDCBus, AuxChannel
            display_entry.DVOPort = vbt_context.DVO_PORT_MAPPING[display_type + '_' + ddi]
            display_entry.AuxChannel = vbt_context.AUX_CHANNEL_MAPPING[ddi]

            if params['is_lfp']:
                display_entry.DeviceClass = vbt_context.DEVICE_CLASS['LFP_' + display_type]
                if index == 0:  # If vbt index is 0, Configure PANEL #01
                    gfx_vbt.block_40.PanelType = index
                elif index == 1:  # Elif vbt index is 1, Configure PANEL #02
                    gfx_vbt.block_40.PanelType2 = index
                else:  # Invalid case
                    logging.error(f"Invalid index {index} passed to configure LFP Panel type.")

                # Set LFP capabilities
                # Bit6: Panel EDID support, 0= Disable, 1= Enable
                if display_type == 'MIPI':
                    gfx_vbt.block_40.LfpCapabilities &= ~(1 << 6)
                else:
                    gfx_vbt.block_40.LfpCapabilities |= (1 << 6)

                logging.info("\t\tLfpCapabilities: PanelEdidSupport= {0}".format(
                    ((gfx_vbt.block_40.LfpCapabilities & 0x40) >> 6)))
            else:
                display_entry.DDCBus = ddc_bus_mapping[platform['name']][ddi]

                # Set HDMI2.1 FRL to Valid and set 12GT/s
                display_entry.IsMaxFrlRateFieldValid = 1
                display_entry.MaximumFrlRate = vbt_context.MAX_FRL_RATE_MAPPING['FRL_12']

                if platform['name'] == 'RKL' and platform['pch'] in pch_ddc_bus_mapping.keys():
                    display_entry.DDCBus = pch_ddc_bus_mapping[platform['pch']][ddi]

                if params['connector_port_type'] == 'PLUS':
                    # change DVO port to DP if display type is HDMI and connector port type is plus
                    display_entry.DVOPort = vbt_context.DVO_PORT_MAPPING['DP' + '_' + ddi]
                    display_entry.DeviceClass = vbt_context.DEVICE_CLASS[params['connector_port_type']]
                else:
                    display_entry.DeviceClass = vbt_context.DEVICE_CLASS[display_type]

                display_entry.TypeC = display_entry.Tbt = 0  # disable TypeC and TBT by default
                if display_type == 'DP' and params['connector_port_type'] in ['TC', 'TBT', 'TC_TBT']:
                    if 'TC' in params['connector_port_type']:
                        display_entry.TypeC |= 1

                    if 'TBT' in params['connector_port_type']:
                        display_entry.Tbt |= 1

            logging.info(
                "\t\tDisplayEntry: Index= {0}, DeviceClass= {1}, DVOPort= {2}, AuxChannel= {3}, "
                "DDCBus= {4}, TypeC= {5}, Tbt= {6}, IsMaxFrlRateFieldValid= {7}, MaximumFrlRate= {8}".format(
                    index, hex(display_entry.DeviceClass), hex(display_entry.DVOPort),
                    hex(display_entry.AuxChannel), hex(display_entry.DDCBus), hex(display_entry.TypeC),
                    display_entry.Tbt, display_entry.IsMaxFrlRateFieldValid, display_entry.MaximumFrlRate))

    ##
    # @brief        Helper function for get vbt port index from vbt object
    # @param[in]    gfx_vbt- Vbt, VBT object from vbt module
    # @param[in]    ddi- string, Port DDI
    # @param[in]    is_lfp- boolean, True if Embedded display Else False
    # @param[in]    platform- dictionary, Platform info
    # @param[in]    exclude_index_list- list, Optional parameter to ignore certain enabled VBT index/indices.
    #                                         Only to be used in enable_ports() method to get configurable free index.
    # @return       (file_handle, log_file) - (int, str), (log file handle, log file path)
    #               (, ) , Tuple[int, bool]
    #                           Returns matching vbt index along with True if index already configured in vbt else False
    def get_index(self, gfx_vbt: vbt.Vbt, ddi: str, is_lfp: bool, platform: dict, exclude_index_list: list = None) -> (
            int, bool):
        if exclude_index_list is None:
            exclude_index_list = []
        lfp_index_map = [lfp_indices for lfp_indices in port_index_mapping[platform['name']]['LFP']]
        efp_index_map = [efp_indices for efp_indices in port_index_mapping[platform['name']]['EFP']]

        index_map = lfp_index_map if is_lfp else efp_index_map

        # Check for already configured VBT for given ddi
        for temp_index in index_map:
            display_name = self.get_display_type(gfx_vbt, temp_index)
            temp_ddi = display_name[-1] if display_name is not None else ""
            if ddi == temp_ddi:
                logging.info(f"Case 1: Existing VBT Index ({temp_index}, {ddi})")
                return temp_index, True

        # Check for free VBT index for configuring given ddi
        for temp_index in index_map:
            display_name = self.get_display_type(gfx_vbt, temp_index)
            if display_name is None:
                logging.info(f"Case 2: New VBT Index ({temp_index}, {ddi})")
                return temp_index, False

        # Available index list gives usable vbt index for enabling requested ports
        available_index_list = list(set(index_map) - set(exclude_index_list))
        temp_index = available_index_list[0] if len(available_index_list) > 0 else None
        logging.info(f"Case 3: New VBT Index ({temp_index}, {ddi})")
        return temp_index, False

    ##
    # @brief        Helper function to verify port configuration
    # @return       None
    def verify_port_configuration(self) -> None:
        # Validate whether requested ports are enabled successfully or not for each platform
        status = True
        for platform in self.platform_info.values():
            logging.info(f"Step: Verify display port configuration in VBT for {platform['name']}")
            supported_ports = display_config.get_supported_ports(gfx_index=platform['gfx_index'])
            logging.info(f"\tSupported Ports= {supported_ports}")
            platform_status = True
            for display in self.display_list[platform['gfx_index']]:
                params = self.param_list[platform['gfx_index']][display]
                port_type = 'EMBEDDED' if params['is_lfp'] else params['connector_port_type']
                if not (display in supported_ports and supported_ports[display] == port_type):
                    platform_status = False

            if platform_status:
                logging.info("\tPASS: All requested ports are enabled")
            else:
                logging.error("\tFAIL: All requested ports are NOT enabled")
            status &= platform_status

        if status is False:
            gdhm.report_bug(
                f"[PrepareDisplaySetup] VBT simulation is not working",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            self.fail("Requested ports are NOT enabled. VBT simulation is NOT working.")

    ##
    # @brief        Helper function to check EDP_B present in configuration
    # @return       bool - True if EDP_B present else false
    def is_edp_b_present(self):
        for platform in self.platform_info.values():
            for display in self.display_list[platform['gfx_index']]:
                ddi = display.split('_')[1]  # A/B/C/...
                params = self.param_list[platform['gfx_index']][display]
                if params['is_lfp'] is True and ddi == 'B':
                    return True
        return False

    ##
    # @brief        Helper function to check Port_F present in configuration
    # @return       bool - True if Port_F present else false
    def is_port_f_present(self):
        for platform in self.platform_info.values():
            for display in self.display_list[platform['gfx_index']]:
                ddi = display.split('_')[1]  # A/B/C/...
                if ddi == 'F':
                    return True
        return False

    ##
    # @brief        Initialize LFP Ports
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    port - Graphics Port Index
    # @return       None
    def __initialize_lfp_port(self, gfx_index: str, port: str):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status = self.driver_interface_.initialize_lfp_ports(adapter_info, [port])
        if status is False:
            self.fail(f"Failed to initialized LFP port {port} on {gfx_index}")

    ##
    # @brief        Logs Current VBT Configuration for given platform
    # @param[in]    gfx_vbt- VBT data
    # @param[in]    platform- Platform details
    # @return       None
    def log_vbt_configuration(self, gfx_vbt: vbt.Vbt, platform: dict) -> None:
        vbt_config = {}
        for index, vbt_index in enumerate(port_index_mapping[platform['name']]['LFP']):
            display = self.get_display_type(gfx_vbt, vbt_index)
            lfp_mipi_or_dp = True if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[vbt_index].DeviceClass in [
                vbt_context.DEVICE_CLASS['LFP_MIPI'], vbt_context.DEVICE_CLASS['LFP_DP']] else False
            vbt_config['LFP' + str(index + 1)] = display if (display is not None and lfp_mipi_or_dp) else None
        for index, vbt_index in enumerate(port_index_mapping[platform['name']]['EFP']):
            display = self.get_display_type(gfx_vbt, vbt_index)
            lfp_mipi_or_dp = True if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[vbt_index].DeviceClass not in [
                vbt_context.DEVICE_CLASS['LFP_MIPI'], vbt_context.DEVICE_CLASS['LFP_DP']] else False
            vbt_config['EFP' + str(index + 1)] = display if (display is not None and lfp_mipi_or_dp) else None
        logging.info(f"  {platform['gfx_index']}: {vbt_config}")


##
# @brief        Types of VBT Configurations possible.
class VbtConfigType(Enum):
    DYNAMIC = 0  # No VBT index passed in command line
    STATIC = 1  # VBT index passed in command line


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    output = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PrepareDisplaySetup'))
    test_environment.TestEnvironment.cleanup(output)
