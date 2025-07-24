#######################################################################################################################
# @file         test_pipe_joiner_basic.py
# @brief        Test to check Uncompressed pipe joiner programming for the plugged display with the max mode supported.
# @details      Test Scenario:
#               1. Plugs the displays, Applies the Extended mode if more than one display is connected else SINGLE
#               2. Applies max mode for each of the display in the topology and verify the max mode.
#               3. Verifies uncompressed pipe joiner programming for each of the pipe joined display in the topology.
#               This test should have at least one DP panel with higher resolution.
#
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
import sys
import unittest
from collections import namedtuple
from typing import Iterator

from Libs.Core.display_config.display_config_struct import DisplayInfo
from Libs.Core import enum
from Libs.Core.display_config import display_config_enums
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Tests.PowerCons.Modules import common
from Tests.Display_Port.DP_Pipe_Joiner.pipe_joiner_base import PipeJoinerBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class PipeJoinerBasicTest(PipeJoinerBase):

    ##
    # @brief        This Test method helps to perform all the test steps.
    # @return       None
    def runTest(self) -> None:

        # Fail the Test if None of the Plugged Displays are Enumerated.
        enumerated_displays = PipeJoinerBase.display_config.get_enumerated_display_info()
        self.assertIsNotNone(enumerated_displays, "[Test Issue] - API get_enumerated_display_info() FAILED")

        config_tuple = namedtuple('config', ['topology', 'display_and_adapter_info_list'])
        config_to_apply = None

        external_display_info_list: Iterator[DisplayInfo] = PipeJoinerBase.get_external_display_info_list()
        external_display_and_adapter_info_list = PipeJoinerBase.get_external_display_and_adapter_info_list()

        if len(external_display_and_adapter_info_list) == 1:
            config_to_apply = config_tuple(enum.SINGLE, external_display_and_adapter_info_list)
        elif len(external_display_and_adapter_info_list) == 2:
            config_to_apply = config_tuple(enum.EXTENDED, [external_display_and_adapter_info_list[0],
                                                           external_display_and_adapter_info_list[1]])
        elif len(external_display_and_adapter_info_list) >= 3:
            self.assertTrue(False, '[Test Issue] - Un-Supported Command Line.')

        is_success = PipeJoinerBase.display_config.set_display_configuration_ex(
            config_to_apply.topology,
            config_to_apply.display_and_adapter_info_list
        )

        self.assertTrue(is_success, "[Driver Issue] - Set Display Configuration Failed.")
        common.print_current_topology()

        for display_info in external_display_info_list:
            port_name = display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            gfx_index = display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex

            # Get Max Mode
            max_mode = common.get_display_mode(display_info.TargetID)
            self.assertIsNotNone(max_mode, "Failed to Get Max Mode.")

            # Set Max Mode For the Display
            is_success = PipeJoinerBase.display_config.set_display_mode([max_mode], False)
            self.assertTrue(is_success, f"[Driver Issue] - Failed to Apply Display Mode on {port_name}")

            common.print_current_topology()

            display_engine = DisplayEngine()
            is_success = display_engine.verify_display_engine()
            self.assertTrue(is_success, "Display Engine Verification Failed")

            is_pipe_joiner_required, _ = DisplayClock.is_pipe_joiner_required(gfx_index, port_name)
            if is_pipe_joiner_required is True:
                is_success = PipeJoinerBase.verify_pipe_joined_display(port_name)
                self.assertTrue(is_success, PipeJoinerBase.test_fail_log_template.format(port_name))
                logging.info(PipeJoinerBase.test_success_log_template.format(port_name))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
