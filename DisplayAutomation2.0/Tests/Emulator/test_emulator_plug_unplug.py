#######################################################################################################################
# @file         test_emulator_plug_unplug.py
# @brief        Contains test cases for Plug/Unplug of panel with Display Emulator, Different Power Event
#               scenarios with Display Emulator
# @details      Test Scenarios:
#                   1. Plug the Display and check if Display is enumerated or not
#                   2. Unplug the Display and check if display is not detected
#                   3. Trigger Power Events and check if display is enumerated or not after resuming from low power
# @author       Gopi Krishna
#######################################################################################################################
import logging
import os
import unittest
import time

from Libs.Core import display_power, display_utility, enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains two test cases,one for plug/unplug stress testing and the second one is for
#               verifying if display is enumerated for different power event scenarios
class PlugUnplugWithEmulator(EmulatorTestBase):

    ##
    # @brief        This test Plugs the Display, checks if display is enumerated, Unplugs the display and checks
    #               if display is not detected for specified number of iterations
    # @return       None
    # @cond
    @common.configure_test(selective=['PLUG_UNPLUG'])
    # @endcond
    def t_1_plug_unplug(self):
        # Gets the List of HDMI Ports that are passed in cmd line
        self.port_list = self.emulator_command_parser.port_list
        logging.info("HDMI Port List {}".format(self.port_list))

        iteration_count = int(self.emulator_command_parser.cmd_dict["ITERATION"][0])

        # Iterating port list
        for port_name in self.port_list:
            emulator_ports = self.she_utility.display_to_emulator_port_map[port_name]
            emulator_port = emulator_ports[0]

            # Get Panel Index from cmd line dictionary
            panel_index = self.emulator_command_parser.cmd_dict[port_name]['panel_index']
            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # Getting EDID Info as per panel index
            data = display_utility.get_panel_edid_dpcd_info(port=port_name, panel_index=panel_index)
            edid = data['edid']
            edid_path = os.path.join(TestContext.panel_input_data(), 'HDMI', edid)

            logging.info("Edid name as per panel index: {}".format(edid))

            # Looping for specified number of iterations in cmdline
            for counter in range(1, iteration_count + 1):
                logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, port_name))

                # Plug the Display
                logging.info("Plugging Display on {}".format(port_name))
                if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, False, None):
                    gdhm.report_bug(
                        title="[Interfaces][HDMI] Display Emulator plug failure on port {}".format(port_name),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plug not Successful on port {}".format(port_name))

                # Giving time for emulator read to happen properly
                time.sleep(2)

                # Read and Verify Timing Info after plugging the display to check if display is enumerated
                logging.info("{0}Verifying Timing Information after Plugging the Display{0}".format("*" * 5))
                status = self.check_timing_info_from_emulator(emulator_port, True)
                self.assertTrue(status, "FAIL: Display is not active on port {} after plug".format(port_name))
                logging.info("PASS: Display is active on port {} after plug".format(port_name))

                # Read and Verify CRC Values after plugging the display to check if display is enumerated
                logging.info("{0}Verifying CRC Values after Plugging the Display{0}".format("*" * 5))
                status = self.check_blankout_using_crc_from_emulator(emulator_port, True)
                self.assertTrue(status, "FAIL: Display is not active on port {} after plug".format(port_name))
                logging.info("PASS: Display is active on port {} after plug".format(port_name))

                # Unplug the Display
                logging.info("Unplugging Display on {}".format(port_name))
                if not self.she_utility.unplug(gfx_adapter_info, port_name, False, None):
                    gdhm.report_bug(
                        title="[Interfaces][HDMI] Display Emulator unplug failure on port {}".format(port_name),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("UnPlug not Successful on port {}".format(port_name))

                # Read and Verify Timing Info after unplugging the display to check if display is not enumerated
                logging.info("{0}Verifying Timing Information after Unplugging the Display{0}".format("*" * 5))
                status = self.check_timing_info_from_emulator(emulator_port, False)
                self.assertTrue(status, "FAIL: Display is still active on port {} after unplug".format(port_name))
                logging.info("PASS: Display is not active on port {} after unplug".format(port_name))

                # Read and Verify CRC Values after unplugging the display to check if display is not enumerated
                logging.info("{0}Verifying CRC Values after Unplugging the Display{0}".format("*" * 5))
                status = self.check_blankout_using_crc_from_emulator(emulator_port, False)
                self.assertTrue(status, "FAIL: Display is still active on port {} after plug".format(port_name))
                logging.info("PASS: Display is not active on port {} after unplug".format(port_name))

    ##
    # @brief        This test Plugs the Display, triggers S3 for all the specified scenarios and checks if
    #               display is enumerated after resuming from low power
    # @return       None
    # @cond
    @common.configure_test(selective=['S3'])
    # @endcond
    def t_2_power_event_s3(self):

        # Gets the List of HDMI Ports that are passed in cmd line
        self.port_list = self.emulator_command_parser.port_list
        logging.info("HDMI Port List {}".format(self.port_list))

        lp_state = display_power.PowerEvent.S3

        # Iterating HDMI port list
        for port_name in self.port_list:
            emulator_ports = self.she_utility.display_to_emulator_port_map[port_name]
            emulator_port = emulator_ports[0]

            logging.debug("Emulator Ports {}".format(emulator_ports))

            # Get Panel Index from cmd line dictionary
            panel_index = self.emulator_command_parser.cmd_dict[port_name]['panel_index']
            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # Getting EDID Info as per panel index
            data = display_utility.get_panel_edid_dpcd_info(port=port_name, panel_index=panel_index)
            edid = data['edid']
            edid_path = os.path.join(TestContext.panel_input_data(), 'HDMI', edid)

            logging.info("Edid name as per panel index: {}".format(edid))

            # Plug the display
            logging.info("Plugging Display on {}".format(port_name))
            if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, False, None):
                self.fail("Plug not Successful on port {}".format(port_name))

            logging.info("{0}Started Verification for Power Event Scenario 1{0}".format("*" * 5))
            status = self.unplug_during_low_power(gfx_adapter_info, port_name, edid_path, emulator_port, lp_state,
                                                  lp_state.name)
            self.assertTrue(status, "Power Event Scenario 1 Verification Failure on {}".format(port_name))
            logging.info("Power Event Scenario 1 Verification Successful on {}".format(port_name))

            time.sleep(3)

            logging.info("{0}Started Verification for Power Event Scenario 2{0}".format("*" * 5))
            status = self.low_power_and_resume_event(port_name, emulator_port, lp_state, lp_state.name)
            self.assertTrue(status, "Power Event Scenario 2 Verification Failure on {}".format(port_name))
            logging.info("Power Event Scenario 2 Verification Successful on {}".format(port_name))

            time.sleep(3)

            logging.info("{0}Started Verification for Power Event Scenario 3{0}".format("*" * 5))
            status = self.plug_during_low_power(gfx_adapter_info, port_name, edid_path, emulator_port, lp_state,
                                                lp_state.name)
            self.assertTrue(status, "Power Event Scenario 3 Verification Failure on {}".format(port_name))
            logging.info("Power Event Scenario 3 Verification Successful on {}".format(port_name))

    ##
    # @brief        Function to trigger and verify power event scenario 1 with HDMI
    #               1. Plug the display                2. Go to S3/S4
    #               3. Unplug the display in S3/S4     4. Resume from S3/S4
    #               5. Plug the display after resuming 6. Check if display is enumerated
    # @param[in]    gfx_adapter_info - Graphics and Adapter Info
    # @param[in]    port_name
    # @param[in]    edid_path
    # @param[in]    emulator_port
    # @param[in]    lp_state
    # @param[in]    pstate_name
    # @return       True/False
    def unplug_during_low_power(self, gfx_adapter_info, port_name, edid_path, emulator_port, lp_state, pstate_name):
        logging.info("Power Event Scenario Description:\n1. Plug the display\n2. Go to Low Power state\n"
                     "3. Unplug the display in Low Power state\n""4. Resume from Low Power state\n"
                     "5. Plug the display after resuming from Low Power\n6. Check if Display is Enumerated")

        # Unplug the display after entering low power state
        if not self.she_utility.unplug(gfx_adapter_info, port_name, True, None):
            logging.error("Unplug Failure on {}".format(emulator_port))
            return False

        # Enter into Low Power State
        is_success = self.display_power.invoke_power_event(lp_state, 60)

        if is_success:
            time.sleep(10)
            # Plug the display after resuming from low power state
            if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, False, None):
                logging.error("Plug Failure on {}".format(emulator_port))
                return False

            time.sleep(2)

            # Read and Verify Timing Info after resuming from Low Power
            logging.info("{0}Verifying Timing Information after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_timing_info_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error("FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

            # Read and Verify CRC Values after resuming from Low Power
            logging.info("{0}Verifying CRC Values after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_blankout_using_crc_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error("FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

        else:
            logging.error("Failed to Invoke Power Event")
            gdhm.report_bug(
                title="[Interfaces][HDMI] Failed to invoke Power Event {}".format(pstate_name),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        return is_success

    ##
    # @brief        Function to trigger and verify power event scenario 2 with HDMI
    #               1. Plug the display        2. Go to S3/S4
    #               3. Resume from S3/S4       4. Check if display is enumerated
    # @param[in]    port_name
    # @param[in]    emulator_port -  used to plug
    # @param[in]    lp_state
    # @param[in]    pstate_name
    # @return       True/False
    def low_power_and_resume_event(self, port_name, emulator_port, lp_state, pstate_name):
        logging.info("Power Event Scenario Description:\n1. Plug the display\n2. Go to Low Power state\n"
                     "3. Resume from Low Power state\n4. Check if Display is Enumerated")

        # Display will be Plugged already
        # Enter into Low Power State
        is_success = self.display_power.invoke_power_event(lp_state)

        if is_success:
            time.sleep(10)

            # Read and Verify Timing Info after resuming from Low Power
            logging.info("{0}Verifying Timing Information after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_timing_info_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error("FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

            # Read and Verify CRC Values after resuming from Low Power
            logging.info("{0}Verifying CRC Values after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_blankout_using_crc_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error(
                    "FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

        else:
            logging.error("Failed to Invoke Power Event")
            gdhm.report_bug(
                title="[Interfaces][HDMI] Failed to invoke Power Event {}".format(pstate_name),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return is_success

    ##
    # @brief            Function to trigger and verify power event scenario 3 with HDMI
    #                   1. Go to S3/S4           2. Plug the display
    #                   3. Resume from S3/S4   4. Check if display is enumerated
    # @param[in]        gfx_adapter_info
    # @param[in]        port_name
    # @param[in]        edid_path
    # @param[in]        emulator_port
    # @param[in]        lp_state
    # @param[in]        pstate_name
    # @return           True/False
    def plug_during_low_power(self, gfx_adapter_info, port_name, edid_path, emulator_port, lp_state, pstate_name):
        logging.info("Power Event Scenario Description:\n1. Go to Low Power state\n2. Plug the display\n"
                     "3. Resume from Low Power state\n4. Check if Display is Enumerated")

        # Unplug the display before plugging it in low power
        if not self.she_utility.unplug(gfx_adapter_info, port_name, False, None):
            logging.error("Unplug Failure on {}".format(emulator_port))
            return False

        # Plug the display in low power
        if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, True, None):
            logging.error("Plug Failure on {}".format(emulator_port))
            return False

        # Enter into Low Power State
        is_success = self.display_power.invoke_power_event(lp_state)

        if is_success:
            time.sleep(10)

            # Read and Verify Timing Info after resuming from Low Power
            logging.info("{0}Verifying Timing Information after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_timing_info_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error("FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

            # Read and Verify CRC Values after resuming from Low Power
            logging.info("{0}Verifying CRC Values after resuming from Low Power{0}".format("*" * 5))
            is_success = self.check_blankout_using_crc_from_emulator(emulator_port, True)
            if is_success:
                logging.info("PASS: Display is active on port {} after resuming from low power".format(port_name))
            else:
                logging.error(
                    "FAIL: Display is not active on port {} after resuming from low power".format(port_name))
                return is_success

        else:
            logging.error("Failed to Invoke Power Event")
            gdhm.report_bug(
                title="[Interfaces][HDMI] Failed to invoke Power Event {}".format(pstate_name),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return is_success


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PlugUnplugWithEmulator))
    test_environment.TestEnvironment.cleanup(test_result)