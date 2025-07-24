#######################################################################################################################
# @file         test_escape_set2.py
# @brief        Combination of tests to verify all Yangra based escape calls under set-2
# @details      Test Scenario:
#               1. Pre-requisite - Plug the Non-VRR and Multi-RR supported eDP display (for CFPS).
#               2. Plug 2 displays(HDMI/DP) of identical panel model (for Collage).
#               3. Verifies all the required Escape calls.
#               Supported command-lines:
#               1. test_escape_set2.py -gfx_0 -EDP_A SINK_EDP045 -DP_B SINK_DPS043 -DP_D SINK_DPS043
#               Note: Test supports only command-lines with Panel Sink Index passed for all displays
#
# @author       Kiran Kumar Lakshmanan, Chandrakanth Pabolu,
#######################################################################################################################
import logging
import time
import unittest
from typing import List, Dict

from Libs.Core import display_utility
from Libs.Core import driver_escape, reboot_helper
from Libs.Core.display_config.display_config_enums import DriverType
from Libs.Core.logger import html
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import driver_escape_args as args
from Tests.ULT.DriverEscape.test_escape_base import DriverEscapeBase

DELAY_5_SECONDS = 5  # Delay for Collage Verification


##
# @brief        DriverEscapeSet2 Class
class DriverEscapeSet2(DriverEscapeBase):

    ##
    # @brief    Test: Validate Collage
    # @details  Pre-requisite: plug two EFPs of same panel index
    # @return   None
    @html.step("Validate Display Collage")
    def test_17_validate_collage(self):
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        collage_type_list: List[int] = [args.CollageType.HORIZONTAL.value, args.CollageType.VERTICAL.value]
        target_id_list: Dict[int, str] = {}

        for collage_type in collage_type_list:
            logging.info(f"Step: Applying {args.CollageType(collage_type).name}")
            enum_displays = self.display_config_.get_enumerated_display_info()
            logging.debug(f"Enumerated Displays - {enum_displays.to_string()}")
            for ports in self.port_list:
                for gfx_index, port in ports.items():
                    # Collage not possible on LFPs
                    if display_utility.get_vbt_panel_type(port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                        continue
                    target_id = self.display_config_.get_target_id(port, enum_displays)
                    if target_id != 0 and target_id not in target_id_list.keys():
                        target_id_list[target_id] = port

            if not bool(target_id_list):
                self.fail("[Collage][Setup] Minimum of 2 displays of same panel type required for collage operation")

            # Get Collage supported Target ID List
            logging.debug(f"[Collage][Setup] Collage Target ID list: {target_id_list}")
            collage_topology = args.CollageTopology()
            display_index = 0
            for target_id, _ in target_id_list.items():
                collage_topology.collageChildInfo[display_index].childID = target_id
                if collage_type == args.CollageType.HORIZONTAL.value:
                    collage_topology.collageChildInfo[display_index].hTileLocation = display_index
                    collage_topology.collageChildInfo[display_index].vTileLocation = 0
                    collage_topology.totalNumberOfHTiles += 1
                    collage_topology.totalNumberOfVTiles = 1
                else:
                    collage_topology.collageChildInfo[display_index].hTileLocation = 0
                    collage_topology.collageChildInfo[display_index].vTileLocation = display_index
                    collage_topology.totalNumberOfHTiles = 1
                    collage_topology.totalNumberOfVTiles += 1
                display_index += 1
            logging.info(f"[Collage] Collage Topology: \n{collage_topology}")
            collage_args = args.CollageModeArgs(args.CollageOperation.VALIDATE_COLLAGE.value, collage_topology)

            # Validate Collage
            status, collage_args = driver_escape.invoke_collage(self.gfx_index, collage_args)
            if not status:
                self.fail("[Collage][Validate] Collage Escape call Failed")
            logging.info("[Collage][Validate] Collage Escape call Passed")

            # Verification condition: Check if collage is possible with plugged displays
            logging.info(
                f"[Collage] Support - {collage_args.collageSupported}; Possible - {collage_args.collageConfigPossible}")
            if collage_args.collageSupported is not True or collage_args.collageConfigPossible is not True:
                self.fail("[Collage][Verify] Collage is not possible on the platform with the given topology")
            logging.info("[Collage][Verify] Collage is possible on the platform with the given topology")

            # Enable Collage
            collage_args.operation = args.CollageOperation.ENABLE_COLLAGE.value
            status, collage_args = driver_escape.invoke_collage(self.gfx_index, collage_args)

            # Wait for 5 Seconds to reflect the changes after enabling collage.
            # Wait for additional 5 seconds if its pre-si environment.
            execution_environment = SystemUtility().get_execution_environment_type()
            additional_delay = DELAY_5_SECONDS if execution_environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"] else 0
            time.sleep(DELAY_5_SECONDS + additional_delay)
            if not status:
                self.fail(f"[Collage][Enable] Collage Escape call Failed")
            logging.info(f"[Collage][Enable] Collage Escape call Passed")

            # Get Collage
            collage_args1 = args.CollageModeArgs(args.CollageOperation.GET_COLLAGE.value, collage_topology)
            status1, collage_args1 = driver_escape.invoke_collage(self.gfx_index, collage_args1)
            if not status1:
                self.fail("[Collage][Get] Collage Escape call Failed")
            logging.info("[Collage][Get] Collage Escape call Passed")

            # Disable Collage
            collage_args = args.CollageModeArgs(args.CollageOperation.DISABLE_COLLAGE.value)
            status, collage_args = driver_escape.invoke_collage(self.gfx_index, collage_args)
            if not status:
                self.fail("[Collage][Disable] Collage Escape call Failed")
            logging.info("[Collage][Disable] Collage Escape call Passed")

            # Verification condition: Check if collage is disabled
            if not (collage_args.collageTopology.totalNumberOfHTiles == 0 and
                    collage_args.collageTopology.totalNumberOfVTiles == 0):
                self.fail("[Collage][Verify] Failed to Disable Collage")
            logging.info("[Collage][Verify] Collage is Disabled")

    ##
    # @brief    Test: Validate Capped FPS
    # @details  Pre-requisite: eDP connected without VRR support and having multi-RR capabilities
    # @return   None
    @html.step("Validate Capped FPS")
    def test_21_validate_cfps(self):
        if self.driver_branch != DriverType.YANGRA:
            logging.info("Skipping this test, since it is supported only with Yangra Driver")
            return

        cfps_state_list: List[int] = [args.CappedFpsState.ENABLE.value, args.CappedFpsState.AUTO.value]
        # Get Escape call
        cfps_args = args.CappedFpsArgs()
        cfps_args.opCode = args.CappedFpsOpcode.GET_CAPPED_FPS.value
        status, cfps_args = driver_escape.get_set_cfps(self.gfx_index, cfps_args)
        if not status:
            self.fail("[Cfps][Get] CFPS Escape call Failed")
        logging.info("[Cfps][Get] CFPS Escape call Passed")

        # Verification condition: Check if CFPS is supported on plugged display
        if cfps_args.cappedFpsSupport is not True:
            self.fail("[Cfps][Verify] CFPS not supported with display plugged")
        logging.info("[Cfps][Verify] CFPS is supported with display plugged")

        if cfps_args.cappedFpsState == args.CappedFpsState.DISABLE:
            logging.warning("[Cfps][Info] CFPS is disabled")

        # Iteration 0: Set to Enable and Verify
        # Iteration 1: Reset to default state and Verify
        for cfps_state in cfps_state_list:
            # Set Escape call
            cfps_args.opCode = args.CappedFpsOpcode.SET_CAPPED_FPS.value
            cfps_args.cappedFpsState = cfps_state
            status, cfps_args = driver_escape.get_set_cfps(self.gfx_index, cfps_args)
            if not status:
                self.fail("[Cfps][Set] CFPS Escape call Failed")
            logging.info(f"[Cfps][Set] CFPS Escape call ({args.CappedFpsState(cfps_state).name}) Passed")

            # Verification condition: Check if CFPS State set to requested state
            cfps_args2 = args.CappedFpsArgs()
            cfps_args2.opCode = args.CappedFpsOpcode.GET_CAPPED_FPS.value
            status2, cfps_args2 = driver_escape.get_set_cfps(self.gfx_index, cfps_args2)
            if not status2:
                self.fail("[Cfps][Verify] Get CFPS Escape call Failed")

            # Verification condition: Compare Applied and Expected CFPS states
            if cfps_args2.cappedFpsState != cfps_state:
                self.fail(f"[Cfps][Verify] Failed to {args.CappedFpsState(cfps_state).name} CFPS")
            logging.info(f"[Cfps][Verify] CFPS set to {args.CappedFpsState(cfps_state).name}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    result = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite("DriverEscapeSet2"))
    test_environment.TestEnvironment.cleanup(result)
