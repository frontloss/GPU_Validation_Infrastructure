########################################################################################################################
# @file         pps_verification.py
# @brief        This file contains tests for PPS verification after reboot
#
# @author       Tulika
########################################################################################################################

import logging
import math
import os
import shutil
import sys
import unittest

from Libs.Core import cmd_parser, display_power, display_utility
from Libs.Core import etl_parser
from Libs.Core.display_config import display_config
from Libs.Core import display_essential
from Libs.Core.logger import etl_tracer, gdhm, html
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.test_env import test_environment
from Libs.Core.vbt.vbt import Vbt
from Tests.LFP_Common.FMS import fms
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

# GDHM header
GDHM_PPS = "[Display_Interface][EDP][PPS]"
PRE_GEN14_BLC_DISPLAY_RAW_LCLOCK_FREQ = 19200 * 1000
DG2_AND_POST_GEN14_BLC_DISPLAY_RAW_LCLOCK_FREQ = 38400 * 1000
BLC_GRANULARITY = 1


##
# @brief        Exposed Class to write PPS tests. Any new PPS test class can inherit this class to use common setUp and
#               tearDown functions.
class PpsVerification(unittest.TestCase):
    cmd_line_param = None
    platform = None
    edp_panels = []
    edp_target_ids = {}
    display_power_ = display_power.DisplayPower()
    machine_info = SystemInfo()
    display_list = []

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for PPS test. Helps to initialize some of the parameters
    #               required for PPS test execution. It is defined in unittest framework and being overridden here.
    # @details      It parses the command line checks for eDP connections and sets display configuration
    # @return       None
    @classmethod
    def setUpClass(cls):
        display_config_ = display_config.DisplayConfiguration()

        logging.info(" SETUP: PPS_VERIFICATION".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, common.CUSTOM_TAGS)
        cls.display_list = cmd_parser.get_sorted_display_list(cls.cmd_line_param)
        cls.edp_panels = [panel for panel in cls.display_list if
                          display_utility.get_vbt_panel_type(panel, 'gfx_0') == display_utility.VbtPanelType.LFP_DP]
        if len(cls.edp_panels) == 0:
            assert False, "No eDP display is passed in the command line (Commandline Issue)"

        enumerated_displays = display_config_.get_enumerated_display_info()
        if enumerated_displays is None:
            assert False, "API get_enumerated_display_info() FAILED (Test Issue)"

        ##
        # check platform
        gfx_display_hwinfo = cls.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            cls.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        ##
        # Checking that all the eDPs passed in command line are connected and getting target ids for the same
        for edp_panel in cls.edp_panels:
            logging.info(f"Verifying test requirements for {edp_panel}")
            if display_config.is_display_attached(enumerated_displays, edp_panel) is False:
                assert False, f"{edp_panel}(eDP) NOT connected. Please run the prepare_display to plug eDP"
            logging.info("\tPASS: Connection status Expected= Connected, Actual= Connected")
            target_id = display_config_.get_target_id(edp_panel, enumerated_displays)
            if target_id == 0:
                assert False, "Target ID for {0}(eDP) is 0 (Test Issue)".format(edp_panel)
            cls.edp_target_ids[edp_panel] = target_id

        ##
        # In case of dual eDP, apply the dual edp config passed from commandline
        if len(cls.edp_panels) > 1:
            logging.info(f"Setting display config {cls.cmd_line_param['CONFIG']} {' '.join(cls.edp_panels)}")
            result = display_config_.set_display_configuration_ex(eval("enum.%s" % cls.cmd_line_param['CONFIG']),
                                                                  cls.edp_panels, enumerated_displays)
            if result is False:
                assert False, f"Set config FAILED = {cls.cmd_line_param['CONFIG']}, {' '.join(cls.edp_panels)}"
            logging.info("\tPASS: Successfully applied display configuration")
            common.print_current_topology()

    ##
    # @brief        This method is the exit point for PPS test cases. This logs the teardown phase.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        gfx_vbt = Vbt()
        logging.info(" TEARDOWN: PPS_VERIFICATION ".center(common.MAX_LINE_WIDTH, "*"))
        gfx_vbt.reset()
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver(Test Issue)")
            return False
        gfx_vbt.reload()
        logging.info("Test Cleanup Completed")

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test to verify delays and pps sequence
    # @return       None
    #@cond
    @common.configure_test(selective =["PPS_DEFAULT"])
    #@endcond
    def t_00_verify_pps_test(self):
        logging.info(" RUNTEST: VERIFY_PPS_DELAYS and PPS_ENABLE_SEQUENCE ".center(common.MAX_LINE_WIDTH, "*"))
        ##
        # Verify PPS
        html.step_start("Verifying Panel Power Sequence")
        new_etl_file = self.generate_etl("GfxTrace_pps.etl")
        for edp_panel in self.edp_panels:
            if self.__verify_delays(edp_panel) is False:
                self.fail("\tFAIL: Panel Power Sequence verification failed")
            logging.info("\tVerification of Delays successful")

            if self.__verify_pwm_frequency(edp_panel) is False:
                self.fail("\tFAIL: Panel Power Sequence verification failed")
            logging.info("\tVerification of PWM frequency and duty cycle successful")

            # Skip PPS sequence verification from ETL in case of FMS
            if fms.verify_fms_during_power_events(new_etl_file, edp_panel[-1], self.platform,
                                                  self.edp_target_ids[edp_panel], True) == fms.ModeSetType.FULL:
                if self.verify_pps_sequence() is False:
                    self.fail("\tFAIL: Panel Power Sequence verification failed")
            else:
                logging.info("Skipping PPS verification due to FMS")

        html.step_end()
        logging.info("\tPASS: Panel Power Sequence verification successful")

    ##
    # @brief        Test verify pps sequence with custom vbt
    # @return       None
    # @cond
    @common.configure_test(selective= ["PPS_BKLT_PWM"])
    # @endcond
    def t_01_verify_pps_test_custom_vbt(self):
        logging.info(" RUNTEST: VERIFY_PPS_ENABLE_SEQUENCE_CUSTOM_VBT ".center(common.MAX_LINE_WIDTH, "*"))
        html.step_start("Verifying PPS enable sequence with custom VBT")
        for edp_panel in self.edp_panels:
            if self.__modify_pwm_bklt_pps_parameter(edp_panel) is False:
                self.fail("\tFAIL: Panel Power Sequence verification with custom VBT failed")
            else:
                new_etl_file = self.generate_etl("GfxTrace_pps_custom_vbt.etl")

            if self.__verify_delays(edp_panel) is False:
                self.fail("\tFAIL: Panel Power Sequence verification with custom VBT failed")
            logging.info("\tVerification of delays with custom VBT successful")

            if self.__verify_pwm_frequency(edp_panel) is False:
                self.fail("\tFAIL: Panel Power Sequence verification with custom VBT failed")
            logging.info("\tVerification of PWM frequency and duty cycle successful")

            # Skip PPS sequence verification from ETL in case of FMS
            if fms.verify_fms_during_power_events(new_etl_file, edp_panel[-1], self.platform,
                                                  self.edp_target_ids[edp_panel], True) == "FULL_MODE_SET":
                if self.verify_pps_sequence() is False:
                    self.fail("\tFAIL: Panel Power Sequence verification with custom VBT failed")
            else:
                logging.info("Skipping PPS verification due to FMS")

        html.step_end()
        logging.info("\tPASS: Panel Power Sequence verification with custom VBT successful")

    ############################
    # Helper Function
    ############################

    # # @brief        Helper function to start ETL trace and invokes power event if needed
    # @param[in]      file_name
    # @param[in]      skip_power_event: Generates ETL report without invoking power event
    # between @return       Returns etl file path
    def generate_etl(self, file_name, skip_power_event: bool = False):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_event = display_power.PowerEvent.CS
        else:
            power_event = display_power.PowerEvent.S3

        # It will be skipped, if ETL is already started
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        if skip_power_event is True:
            logging.info("Skipping power event")

        elif self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event %s' % power_event.name)

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")

        new_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            self.fail(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")

        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_etl_file)

        if etl_parser.generate_report(new_etl_file) is False:
            logging.error(f"\tFailed to generate report for {new_etl_file}")
            return False

        return new_etl_file

    ##
    # @brief        Helper function to verify PPS delays from ETL report
    # @param[in]    panel
    # @return       verify_delay_result returns True if verification successful else false
    def __verify_delays(self, panel):
        bklt_off_timestamp = 0
        bklt_on_timestamp = 0
        data_off_timestamp = 0
        pwm_on_timestamp = 0
        pwm_off_timestamp = 0
        verify_delay_result = True
        gfx_vbt = Vbt()
        panel_index = gfx_vbt.get_lfp_panel_type(panel)

        html.step_start("Register programmed data for PPS")
        # Get Software Delay
        pps_data = etl_parser.get_event_data(etl_parser.Events.PPS_DATA)
        if pps_data is None:
            logging.error("No PPS state data found in ETL")
            html.step_end()
            return False

        for entry in range(len(pps_data)):
            logging.debug(f"PPS signal requested {pps_data[entry].PpsSignal}")
            logging.debug(f"PPS state restriction {pps_data[entry].PpsState}")

            if pps_data[entry].PpsSignal == 'DD_BKLT' and pps_data[entry].PpsState == 'OFF':
                logging.info(f"BKLT_OFF_timestamp = {pps_data[entry].TimeStamp}")
                bklt_off_timestamp = pps_data[entry].TimeStamp

            if pps_data[entry].PpsSignal == 'DD_DATA' and pps_data[entry].PpsState == 'OFF':
                logging.info(f"DATA_OFF_timestamp = {pps_data[entry].TimeStamp}")
                data_off_timestamp = pps_data[entry].TimeStamp

            if pps_data[entry].PpsSignal == 'DD_PWM' and pps_data[entry].PpsState == 'ON':
                logging.info(f"PWM_ON_timestamp = {pps_data[entry].TimeStamp}")
                pwm_on_timestamp = pps_data[entry].TimeStamp

            if pps_data[entry].PpsSignal == 'DD_PWM' and pps_data[entry].PpsState == 'OFF':
                logging.info(f"PWM_OFF_timestamp = {pps_data[entry].TimeStamp}")
                pwm_off_timestamp = pps_data[entry].TimeStamp

            if pps_data[entry].PpsSignal == 'DD_BKLT' and pps_data[entry].PpsState == 'ON':
                logging.info(f"BKLT_ON_timestamp = {pps_data[entry].TimeStamp}")
                bklt_on_timestamp = pps_data[entry].TimeStamp

        actual_t3_delay = None
        actual_t10_delay = None
        actual_t12_delay = None
        actual_t9_delay = round((data_off_timestamp - bklt_off_timestamp), 3)
        actual_pwm_on_to_backlight_enable_delay = round((bklt_on_timestamp - pwm_on_timestamp), 3)
        actual_backlight_off_to_pwm_off_delay = round((pwm_off_timestamp - bklt_off_timestamp), 3)

        # Get MMIO data from ETL
        suffix = "" if panel.split("_")[-1] == "A" else "_2"

        pp_on_delays = MMIORegister.get_instance("PP_ON_DELAYS_REGISTER", "PP_ON_DELAYS" + suffix, self.platform)
        pp_off_delays = MMIORegister.get_instance("PP_OFF_DELAYS_REGISTER", "PP_OFF_DELAYS" + suffix, self.platform)
        pp_control = MMIORegister.get_instance("PP_CONTROL_REGISTER", "PP_CONTROL" + suffix, self.platform)

        pp_on_delays_output = etl_parser.get_mmio_data(pp_on_delays.offset)
        pp_off_delays_output = etl_parser.get_mmio_data(pp_off_delays.offset)
        pp_control_output = etl_parser.get_mmio_data(pp_control.offset)

        for mmio_data in pp_on_delays_output:
            pp_on_delays.asUint = mmio_data.Data
            actual_t3_delay = pp_on_delays.power_up_delay

        for mmio_data in pp_off_delays_output:
            pp_off_delays.asUint = mmio_data.Data
            actual_t10_delay = pp_off_delays.power_down_delay

        for mmio_data in pp_control_output:
            pp_control.asUint = mmio_data.Data
            actual_t12_delay = (pp_control.power_cycle_delay - 1) * 1000  # According to bspec the value should be
            # programmed to (desired delay / 100 milliseconds) + 1

        logging.info(f"Actual Delay Data - T3_Delay= {actual_t3_delay}, T9_Delay= {actual_t9_delay}, T10_Delay= {actual_t10_delay}, "
                     f"T12_Delay= {actual_t12_delay}, PWM_on_to_backlight_enable= {actual_pwm_on_to_backlight_enable_delay},"
                     f"Backlight_off_to_PWM_off_delay= {actual_backlight_off_to_pwm_off_delay}")

        html.step_start("VBT set data for PPS")

        vbt_t3_delay = gfx_vbt.block_27.PPSEntry[panel_index].T3Delay
        # According to bspec the value is in 100us which should be converted to milliseconds
        vbt_t9_delay = gfx_vbt.block_27.PPSEntry[panel_index].T9Delay * 0.1
        vbt_t10_delay = gfx_vbt.block_27.PPSEntry[panel_index].T10Delay
        vbt_t12_delay = gfx_vbt.block_27.PPSEntry[panel_index].T12Delay

        # According to bspec the value is in 100us which should be converted to milliseconds
        vbt_pwm_on_to_backlight_enable_delay = (gfx_vbt.block_27.BacklightDelaysEntry[
                                                    panel_index].PWMOntoBackLightDelay) * 0.1
        vbt_backlight_off_to_pwm_off_delay = (gfx_vbt.block_27.BacklightDelaysEntry[
            panel_index].BacklightOfftoPWMOffDelay) * 0.1

        logging.info(f"VBT Delay Data - T3_Delay= {vbt_t3_delay}, T9_Delay= {vbt_t9_delay}, T10_Delay= {vbt_t10_delay}, "
                     f"T12_Delay= {vbt_t12_delay}, PWM_on_to_backlight_enable= {vbt_pwm_on_to_backlight_enable_delay}, "
                     f"Backlight_off_to_pwm_off_delay= {vbt_backlight_off_to_pwm_off_delay}")

        html.step_start("Verifying Delays")
        if actual_t3_delay != vbt_t3_delay:
            verify_delay_result &= False
            logging.error(f"FAIL: T3 delay Mismatch. Expected= {vbt_t3_delay}, Actual= {actual_t3_delay}")
            gdhm.report_driver_bug_di(f"{GDHM_PPS} T3 delay Mismatch.")
        else:
            logging.info(f"Pass: T3 delay programmed successfully. Expected= {vbt_t3_delay}, Actual= {actual_t3_delay}")

        if vbt_t9_delay - 100 <= actual_t9_delay <= vbt_t9_delay + 100:
            logging.info(f"Pass: T9 delay programmed successfully. Expected= {vbt_t9_delay}, Actual= {actual_t9_delay}")
        else:
            verify_delay_result &= False
            logging.error(f"FAIL: T9 delay Mismatch. Expected= {vbt_t9_delay}, Actual= {actual_t9_delay}")
            gdhm.report_driver_bug_di(f"{GDHM_PPS} T9 delay Mismatch.")

        if actual_t10_delay != vbt_t10_delay:
            verify_delay_result &= False
            logging.error(f"FAIL: T10 delay Mismatch. Expected= {vbt_t10_delay}, Actual= {actual_t10_delay}")
            gdhm.report_driver_bug_di(
                f"{GDHM_PPS} T10 delay Mismatch.")
        else:
            logging.info(
                f"Pass: T10 delay programmed successfully. Expected= {vbt_t10_delay}, Actual= {actual_t10_delay}")

        if actual_t12_delay != vbt_t12_delay:
            verify_delay_result &= False
            logging.error(f"FAIL: T12 delay Mismatch. Expected= {vbt_t12_delay}, Actual= {actual_t12_delay}")
            gdhm.report_driver_bug_di(
                f"{GDHM_PPS} T12 delay Mismatch.")
        else:
            logging.info(
                f"Pass: T12 delay programmed successfully. Expected= {vbt_t12_delay}, Actual= {actual_t12_delay}")

        if math.floor(actual_pwm_on_to_backlight_enable_delay) != vbt_pwm_on_to_backlight_enable_delay:
            verify_delay_result &= False
            logging.error(
                f"FAIL: PWM to backlight enable delay Mismatch. Expected= {vbt_pwm_on_to_backlight_enable_delay} "
                f"Actual:{actual_pwm_on_to_backlight_enable_delay}")
            gdhm.report_driver_bug_di(f"{GDHM_PPS} PWM to backlight enable delay Mismatch.")
        else:
            logging.info(
                f"Pass: PWM to backlight enable delay programmed successfully. "
                f"Expected= {vbt_pwm_on_to_backlight_enable_delay} Actual= {actual_pwm_on_to_backlight_enable_delay}")

        if math.floor(actual_backlight_off_to_pwm_off_delay) != vbt_backlight_off_to_pwm_off_delay:
            verify_delay_result &= False
            logging.error(
                f"FAIL: Backlight to PWM off delay Mismatch. Expected= {vbt_backlight_off_to_pwm_off_delay} "
                f"Actual:{actual_backlight_off_to_pwm_off_delay}")
            gdhm.report_driver_bug_di(f"{GDHM_PPS} Backlight to PWM off delay Mismatch.")
        else:
            logging.info(
                f"Pass: Backlight to PWM off delay programmed successfully. "
                f"Expected= {vbt_backlight_off_to_pwm_off_delay} Actual= {actual_backlight_off_to_pwm_off_delay}")

        html.step_end()
        return verify_delay_result

    ##
    # @brief        Helper function to verify PPS sequence from ETL report
    # @param        detachable_lfp: If True, verify PPS sequence for detachable LFP wiz. present on Port B
    #               EDP team can modify this variable name later (if needed) to validate PPS sequence per port.
    # @return       None
    @staticmethod
    def verify_pps_sequence(detachable_lfp: bool = False):
        vdd_data = []

        pps_data_timestamps = {
            "vdd_on_timestamp": [], "pwm_on_timestamp": [], "bklt_on_timestamp": [], "vdd_off_timestamp": [], "pwm_off_timestamp": [], "bklt_off_timestamp": []
        }

        html.step_start("Verifying PPS Sequence")
        pps_sequence_result = True
        pps_data = etl_parser.get_event_data(etl_parser.Events.PPS_DATA)
        if pps_data is None:
            logging.error("No PPS data found in ETL")
            html.step_end()
            return False

        # Minor Tweak to support validation of PPS sequence for dual EDP:-
        # In the ETL we will be having PPS data for both EDP A and EDP B,
        # so, we won't know for which port we are validating. Hence, retrieve the
        # port data also from the ETL and verify per port separately.
        port_to_be_validated = 'PORT_B' if detachable_lfp else 'PORT_A'

        for entry in range(len(pps_data)):
            if pps_data[entry].Port != port_to_be_validated:
                continue

            logging.debug(f'PPS data[Port]: {pps_data[entry].Port}')

            if pps_data[entry].PpsState in ["ON", "OFF"]:
                state = pps_data[entry].PpsState.lower()
                vdd_data.append(pps_data[entry].PpsState)

                if pps_data[entry].PpsSignal == "DD_VDD":
                    pps_data_timestamps[f"vdd_{state}_timestamp"].append(pps_data[entry].TimeStamp)
                    logging.debug(f"PPS signal for VDD: {pps_data[entry].PpsSignal}; PPS state: {pps_data[entry].PpsState}")

                if pps_data[entry].PpsSignal == "DD_BKLT":
                    pps_data_timestamps[f"bklt_{state}_timestamp"].append(pps_data[entry].TimeStamp)
                    logging.debug(f"PPS signal for BKLT: {pps_data[entry].PpsSignal}; PPS state: {pps_data[entry].PpsState}")

                if pps_data[entry].PpsSignal == "DD_PWM":
                    pps_data_timestamps[f"pwm_{state}_timestamp"].append(pps_data[entry].TimeStamp)
                    logging.debug(f"PPS signal for PWM: {pps_data[entry].PpsSignal}; PPS state: {pps_data[entry].PpsState}")

        if {"ON", "OFF"}.issubset(set(vdd_data)) is False:
            pps_sequence_result &= False
            logging.error("VDD check failed")
            gdhm.report_driver_bug_di(f"{GDHM_PPS} VDD check failed")
        else:
            logging.info("Pass: VDD check successful")

        # Print all the timestamps
        logging.debug(f"Timestamps - VDD OFF: {pps_data_timestamps['vdd_off_timestamp']}, PWM OFF: {pps_data_timestamps['pwm_off_timestamp']}, BKLT OFF: {pps_data_timestamps['bklt_off_timestamp']}")
        logging.debug(f"Timestamps - VDD ON: {pps_data_timestamps['vdd_on_timestamp']}, PWM ON: {pps_data_timestamps['pwm_on_timestamp']}, BKLT ON: {pps_data_timestamps['bklt_on_timestamp']}")


        # Detachable LFP's ETL will have exactly 1 round of unplug and plug
        # Hence, we expect each PPS data to be exactly 1
        if detachable_lfp:
            if all(len(pps_data_timestamps[key]) == 1 for key in
                                  ["vdd_on_timestamp", "bklt_on_timestamp", "pwm_on_timestamp", "vdd_off_timestamp",
                                   "bklt_off_timestamp", "pwm_off_timestamp"]):
                logging.info("Pass: Exactly one instance of VDD, PWM, and BCKLT is present.")
            else:
                pps_sequence_result &= False
                logging.error("There are more than one instance of VDD, PWM, and bcklt")
                logging.info(pps_data_timestamps)
                gdhm.report_driver_bug_di(f"{GDHM_PPS} PPS check failed")

        # PPS Sequence Check
        if pps_sequence_result:
            disable_sequence = True if (pps_data_timestamps["bklt_off_timestamp"][-1] < pps_data_timestamps["pwm_off_timestamp"][-1] and pps_data_timestamps["pwm_off_timestamp"][-1] < pps_data_timestamps["vdd_off_timestamp"][-1]) else False
            enable_sequence = True if (pps_data_timestamps["vdd_on_timestamp"][-1] < pps_data_timestamps["pwm_on_timestamp"][-1] and pps_data_timestamps["pwm_on_timestamp"][-1] < pps_data_timestamps["bklt_on_timestamp"][-1]) else False

            if disable_sequence and enable_sequence:
                logging.info("Pass: PPS sequence check")
            else:
                pps_sequence_result &= False
                logging.error("PPS sequence check failed")
                gdhm.report_driver_bug_di(f"{GDHM_PPS} PPS sequence check failed")

        html.step_end()
        return pps_sequence_result

    ##
    # @brief        Helper function to modify vbt
    # @param[in]    panel
    # @return       Returns True if vbt modification successful else False
    def __modify_pwm_bklt_pps_parameter(self, panel):
        gfx_vbt = Vbt()
        panel_index = gfx_vbt.get_lfp_panel_type(panel)
        # Modifiying VBT: HSD#14020999397
        if (gfx_vbt.block_27.BacklightDelaysEntry[panel_index].PWMOntoBackLightDelay == 0) and (
                gfx_vbt.block_27.BacklightDelaysEntry[panel_index].BacklightOfftoPWMOffDelay == 0):
            gfx_vbt.block_27.BacklightDelaysEntry[panel_index].PWMOntoBackLightDelay = 150
            gfx_vbt.block_27.BacklightDelaysEntry[panel_index].BacklightOfftoPWMOffDelay = 150
            if gfx_vbt.apply_changes() is False:
                logging.error(f"VBT modification failed")
                return False
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                logging.error("\tFailed to restart display driver(Test Issue)")
                return False
            gfx_vbt.reload()
            return True

    ##
    # @brief        Helper function to verify PWM frequency
    # @param[in]    panel
    # @return       status True if verification successful else False
    def __verify_pwm_frequency(self, panel):
        status = True
        actual_pwm_frequency = 0
        pwm_frequency_timestamp = 0
        duty_cycle_data = 0
        duty_cycle_timestamp = 0
        pwm_enable_data = 0
        suffix = "" if panel.split("_")[-1] == "A" else "_2"

        #verifying PWM frequency programming
        if self.platform.upper() in ['ADLP','TGL']:
            calculated_pwm_frequency = PRE_GEN14_BLC_DISPLAY_RAW_LCLOCK_FREQ / BLC_GRANULARITY / 200
        else:
            calculated_pwm_frequency = DG2_AND_POST_GEN14_BLC_DISPLAY_RAW_LCLOCK_FREQ / BLC_GRANULARITY / 200

        pwm_freq = MMIORegister.get_instance("SBLC_PWM_FREQ_REGISTER", "SBLC_PWM_FREQ" + suffix, self.platform)
        pwm_freq_output = etl_parser.get_mmio_data(pwm_freq.offset, is_write=True)
        for mmio_data in pwm_freq_output:
            pwm_freq.asUint = mmio_data.Data
            actual_pwm_frequency = pwm_freq.frequency
            pwm_frequency_timestamp = mmio_data.TimeStamp

            if calculated_pwm_frequency != actual_pwm_frequency:
                logging.error(f"FAIL: PWM frequency mismatch. Expected= {calculated_pwm_frequency}, Actual= {actual_pwm_frequency}")
                gdhm.report_driver_bug_di(f"{GDHM_PPS} PWM frequency Mismatch.")
                status &= False
            else:
                logging.info(f"Pass: PWM frequency programmed successfully. Expected= {calculated_pwm_frequency}, Actual= {actual_pwm_frequency}")

            #verifying Duty Cycle programming
            duty_cycle = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY" + suffix, self.platform)
            duty_cycle_output = etl_parser.get_mmio_data(duty_cycle.offset, is_write=True)
            for mmio_data in duty_cycle_output:
                if mmio_data.TimeStamp > pwm_frequency_timestamp:
                    duty_cycle.asUint = mmio_data.Data
                    duty_cycle_data = duty_cycle.duty_cycle
                    duty_cycle_timestamp = mmio_data.TimeStamp
                    break

            if duty_cycle_data == 0:
                logging.error("FAIL: Duty Cycle not programmed")
                gdhm.report_driver_bug_di(f"{GDHM_PPS} Duty Cycle not programmed")
                status &= False
            else:
                logging.info("Pass: Duty Cycle programmed successfully")

            #Checking if PWM frequency and duty cycle are programmed before PWM enable
            pwm_enable = MMIORegister.get_instance("SBLC_PWM_CTL1_REGISTER", "SBLC_PWM_CTL1" + suffix, self.platform)
            pwm_enable_output = etl_parser.get_mmio_data(pwm_enable.offset, is_write=True)
            for mmio_data in pwm_enable_output:
                if mmio_data.TimeStamp > duty_cycle_timestamp:
                    pwm_enable.asUint = mmio_data.Data
                    pwm_enable_data = pwm_enable.pwm_pch_enable
                    break

            if pwm_enable_data != 1:
                logging.error(f"FAIL: PWM not enabled")
                gdhm.report_driver_bug_di(f"{GDHM_PPS} PWM not enabled")
                status &= False
            else:
                logging.info(f"PASS: PWM enabled successfully")

        if not status:
            logging.info(
                f"FAIL: PWM not enabled after PWM frequency and duty cycle is programmed")
        else:
            logging.info(
                f"PASS: PWM enabled successfully after PWM frequency and duty cycle is programmed")

        html.step_end()
        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PpsVerification))
    test_environment.TestEnvironment.cleanup(test_result)