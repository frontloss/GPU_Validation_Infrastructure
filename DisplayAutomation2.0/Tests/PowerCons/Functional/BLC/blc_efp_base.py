########################################################################################################################
# @file         blc_efp_base.py
# @brief        This file contains the base class for EFP BLC test cases.
# @author       Tulika
########################################################################################################################
import logging
import os
import re
import subprocess
import sys
import unittest

from Libs.Core import cmd_parser, display_essential, etl_parser
from Libs.Core import display_power
from Libs.Core.display_config import display_config
from Libs.Core.logger import html
from Libs.Core.vbt.vbt import Vbt
from Libs.prepare_display_setup import port_index_mapping
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Modules import dut, common
from registers.mmioregister import MMIORegister

BRIGHTNESS_LIST = [1, 61, 47, 0, 100, 30, 89]
ACTUAL_BRIGHTNESS = [0x8D0, 0xE3EC, 0xAEF9, 0x8D0, 0x17700, 0x6FC0, 0x14C53]


##
# @brief        Exposed Class for EFP BLC tests. Any new EFP BLC test can inherit this class to use common setUp and
#               tearDown functions.
class BlcEfpBase(unittest.TestCase):
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    instance_id = None

    ##
    # @brief        This class method is the entry point for EFP BLC test cases which inherit this class.
    #               It does the initializations and setup required for EFP BLC test execution.
    # @details      This function parses command line arguments for display list and custom tags
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info("SETUP: EFP BLC BASE ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]
        dut.prepare()
        cls.instance_id = blc.get_monitor_instance_id()
        if cls.instance_id is None:
            assert False, "Monitor Key InstanceID not found"


    ##
    # @brief        This method is the exit point for EFP BLC tests.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info("TEARDOWN: EFP BLC BASE ".center(common.MAX_LINE_WIDTH, "*"))
        vbt = Vbt()
        if vbt.reset() is False:
            assert False, "Failed to restore VBT from driver"
        logging.info("Successfully restored VBT from driver")
        status, reboot_required = display_essential.restart_gfx_driver()
        assert status, "Failed to restart driver"
        logging.info("Successfully restarted driver")
        if blc.delete_brightness_control_regkey(cls.instance_id) is False:
            logging.warning("Failed to delete BrightnessControl regkey")
        dut.reset()

    ################
    # Test Function
    ################

    ##
    # @brief       This tests does VBT changes require for the EFP BLC
    # @return      None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Applying VBT and Regkey changes for BLC support on External Panel")
        if blc.add_brightness_control_regkey(self.instance_id) is False:
            self.fail("Failed to add BrightnessControl regkey")
        # VBT Changes
        for adapter in dut.adapters.values():
            gfx_vbt = Vbt(adapter.gfx_index)
            if gfx_vbt.version < 256:
                self.fail("FAIL: VBT version not supported")

            # Setting No Local Flat Panel in LFP configuration
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[0].DeviceClass = 0x0
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[1].DeviceClass = 0x0

            # Take panel index to apply FE
            efp_index = [efp_indices for efp_indices in port_index_mapping[adapter.name]['EFP']]
            for index in efp_index:
                if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].EFPPanelIndex == 254:
                    gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].EFPPanelIndex = 2
            if gfx_vbt.apply_changes() is False:
                self.fail("FAIL: Failed to apply VBT changes")
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("FAIL: Failed to restart display driver after VBT update")
            gfx_vbt.reload()

    ##
    # @brief        Exposed API to validate the BLC feature
    # @param[in]    scenario
    # @return       None
    def verify_efp_blc(self, scenario: blc.Scenario = None):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    continue
                brightness_args = [None, None, None, None, BRIGHTNESS_LIST]
                workload_status = blc.run_workload(adapter, scenario, brightness_args)
                if workload_status[1] is False:
                    self.fail("FAILED to run the workload")
                if workload_status[0] is None:
                    self.fail("ETL file not found")

            html.step_start("VERIFICATION PHASE")
            if os.path.exists(workload_status[0]) is False:
                self.fail(f"{workload_status[0]} not Found")
            # Generate reports from ETL file using EtlParser
            logging.info("Step: Generating EtlParser Report for {0}".format(workload_status[0]))
            if etl_parser.generate_report(workload_status[0]) is False:
                self.fail("\tFAILED to generate ETL Parser report (Test Issue)")
            logging.info("\tPASS: Successfully generated ETL Parser report")
            pwm_duty = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY", adapter.name)
            pwm_duty_output = etl_parser.get_mmio_data(pwm_duty.offset, is_write=True)
            if pwm_duty_output is None:
                self.fail(f"\tNo MMIO entry found for register SBLC_PWM_DUTY")

            actual_brightness_index = 0
            next_index = 0
            previous_data = None
            for index in range(len(pwm_duty_output)-1):
                if (index <= next_index) and (next_index != 0):
                    continue
                if pwm_duty_output[index].Data != previous_data and pwm_duty_output[index + 1].Data != previous_data:
                    start_time = pwm_duty_output[index].TimeStamp
                    # For B2 panel phase-in should complete in 20 steps
                    next_index = index + 19
                    end_time = pwm_duty_output[next_index].TimeStamp
                    if pwm_duty_output[next_index].Data != ACTUAL_BRIGHTNESS[actual_brightness_index]:
                        self.fail(f"Brightness slider value does NOT match. "
                                  f"Expected= {ACTUAL_BRIGHTNESS[actual_brightness_index]}, "
                                  f"Actual= {pwm_duty_output[next_index].Data}")

                    logging.info(f"Brightness slider value Matched. Expected= "
                                 f"{ACTUAL_BRIGHTNESS[actual_brightness_index]}, "
                                 f"Actual= {pwm_duty_output[next_index].Data}")
                    actual_brightness_index += 1
                    previous_data = pwm_duty_output[next_index].Data
                    if round((end_time - start_time), 3) > 500:
                        self.fail(f"Phase-in completed. Expected= 350ms, Actual= {round((end_time - start_time), 3)}ms")
                    logging.info(
                        f"Phase-in completed. Expected= 350ms, Actual= {round((end_time - start_time), 3)}ms")
