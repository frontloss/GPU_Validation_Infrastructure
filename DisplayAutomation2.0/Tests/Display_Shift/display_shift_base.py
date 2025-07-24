########################################################################################################################
# @file         display_shift_base.py
# @brief        The script consists of unittest setup and tear down classes for display shifting.
#                   * Parse command line.
#                   * Apply display configuration.
# @author       Nivetha.B
########################################################################################################################
import logging
import sys
import unittest
import time

from Libs.Core import cmd_parser, enum
from Libs.Core import display_utility
from Libs.Core import display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.wrapper import control_api_wrapper
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

MAX_LINE_WIDTH = 64
MAX_DISPLAY_SHIFT_TIME = 6


##
# @brief - Control Library Test Base
class DisplayShiftBase(unittest.TestCase):
    gfx_index = None
    gfx_index_after_switch = None
    connected_list = []
    custom_tags = ['-POWER_EVENT', '-ITERATION']
    display_config = DisplayConfiguration()
    display_power = display_power.DisplayPower()
    iterations = 1

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info(" SETUP: DISPLAY_SHIFT_BASE ".center(MAX_LINE_WIDTH, "*"))

        self.test_name = sys.argv[0]

        # Parse command line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
                    self.display = value['connector_port']

        self.underrun = UnderRunStatus()

        self.current_config = self.display_config.get_current_display_configuration()

        # set ITERATION based on the command line
        if self.cmd_line_param['ITERATION'] != 'NONE':
            if self.cmd_line_param['ITERATION'][0] and int(self.cmd_line_param['ITERATION'][0]) > 1:
                self.iterations = int(self.cmd_line_param['ITERATION'][0])

    ##
    # @brief        Gets the current adapter owning the Mux
    # @param[in]    log_enable - True if need to log the adapter owning display
    # @return       gfx_index - Graphics adapter index
    def get_adapter_owning_mux(self, log_enable=False):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        gfx_index = None
        for index in range(enumerated_displays.Count):
            if display_utility.VbtPanelType.LFP_DP:
                gfx_index = enumerated_displays.ConnectedDisplays[
                    index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                if log_enable:
                    if gfx_index == 'gfx_0':
                        logging.info("Current display is owned by INTEGRATED")
                    else:
                        logging.info("Current display is owned by DISCRETE")
        return gfx_index

    ##
    # @brief        Verifies System is CS enabled or not
    # @param[in]    expected_status - bool, True if CS else False
    # @return       None
    def verify_system_power_settings(self, expected_status=False):
        status = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)
        if expected_status == status:
            logging.info(f"\tPASS: Expected CS System: {expected_status}, Actual CS System: {expected_status}")
        else:
            self.fail(f"FAIL: Expected CS System: {expected_status}, Actual CS System: {expected_status}")

    ##
    # @brief        Invoke power event based on command line param
    # @return       None
    def base_invoke_power_event(self):
        if self.cmd_line_param['POWER_EVENT'] != 'NONE':
            if self.cmd_line_param['POWER_EVENT'][0] == 'CS':
                self.verify_system_power_settings(True)
                power_event = display_power.PowerEvent.CS
            elif self.cmd_line_param['POWER_EVENT'][0] == 'S3':
                power_event = display_power.PowerEvent.S3
                self.verify_system_power_settings()
            elif self.cmd_line_param['POWER_EVENT'][0] == 'S4':
                power_event = display_power.PowerEvent.S4
                self.verify_system_power_settings()
            if self.display_power.invoke_power_event(power_event) is False:
                self.fail(f'Failed to invoke power event {power_event}')

    ##
    # @brief        Gets the adapter owning mux and do a display shift and verifies the status
    # @param[in]    power - bool, True if power event
    # @return       None
    def verify_display_shift(self, power=False):
        gfx_index_before_switch = self.get_adapter_owning_mux(log_enable=True)
        if power:
            if gfx_index_before_switch != self.gfx_index_after_switch:
                logging.error("Display switch verification failed after Power event")
                self.fail(f"Adapter expected after power event: "
                          f"Expected: {self.gfx_index_after_switch}, Actual: {gfx_index_before_switch}")
            else:
                logging.info(f"Adapter expected after power event: "
                             f"Expected: {self.gfx_index_after_switch}, Actual: {gfx_index_before_switch}")
        start_time = time.time()
        display_shift_status = control_api_wrapper.display_shift()
        end_time = time.time()
        # Calculate the time taken to shift from IGPU/DGPU
        shifting_time = end_time - start_time
        adapter_index_after_switch = "gfx_1" if gfx_index_before_switch == "gfx_0" else "gfx_0"
        if display_shift_status and shifting_time < MAX_DISPLAY_SHIFT_TIME:
            if self.verify_adapter_owning_mux(expected_adapter=adapter_index_after_switch):
                logging.info(f"Display shift from {gfx_index_before_switch} - {adapter_index_after_switch} is successful"
                             f" in {shifting_time:.2f} seconds")
        else:
            logging.error(f"Fail: Expected: {adapter_index_after_switch}, Actual: {gfx_index_before_switch} failed"
                          f" after {shifting_time:.2f} seconds")
            self.fail(f"Fail: Expected: {adapter_index_after_switch}, Actual: {gfx_index_before_switch} failed after "
                          f"{shifting_time:.2f} seconds")

    ##
    # @brief        Verifies the current and expected adapters
    # @param[in]    expected_adapter - Expected Adapter index
    # @return       None
    def verify_adapter_owning_mux(self, expected_adapter):
        current_adapter = self.get_adapter_owning_mux()
        if current_adapter == expected_adapter:
            return True
        return False

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: DISPLAY_SHIFT_BASE ".center(MAX_LINE_WIDTH, "*"))

        logging.info(" TEST ENDS ".center(MAX_LINE_WIDTH, "*"))


if __name__ == '__main__':
    unittest.main()
