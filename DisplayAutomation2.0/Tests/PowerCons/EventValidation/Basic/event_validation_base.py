########################################################################################################################
# @file         event_validation_base.py
# @brief        Contains base class for all ETL based PowerCons tests
# @details      @ref event_validation_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all tests, and helper functions.
#
# @author       Vinod D S, Ashish Tripathi
########################################################################################################################

import logging
import os
import sys
import time
import unittest

import win32api

from Libs.Core import cmd_parser, enum, winkb_helper, registry_access, display_essential, display_power
from Libs.Core.display_config import display_config
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, desktop_controls, powercons_escapes, validator_runner, dut
from Tests.VRR import vrr

MULTI_ANIMATION_EXE = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER,
                                   "PowerCons\\MultiAnimation\\DFPS_MultiAnimation.exe")


##
# @brief        Exposed Class to write Event Validation tests for verifying display pc features
#               (blc, dpst, psr, drrs, lace). Any new Event Validation test class can inherit
#               this class to use common setUp, tearDown and helper functions for the tests.
class EventValidationBase(unittest.TestCase):
    custom_tags = {
        '-PANEL_CONFIG': ['PSR1', 'PSR2', 'STATIC_DRRS', 'SEAMLESS_DRRS', 'DPST_OVERRIDE'],
        '-AGGRLEVEL': '',
        '-LUX': '',
        '-NITS': '',
        '-CS': '',
        '-S3': '',
        '-S4': '',
        '-ASYNC': '',
        '-VSYNC': '',
        '-WINDOWED': '',
        '-FULLSCREEN': ''
    }

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    machine_info_ = SystemInfo()

    cmd_line_param = None  # Used to store command line parameters
    nits_ranges_values = None
    precision_ranges_values = None
    cmd_test_name = 'NONE'
    panel_config = None
    cmd_feature = None
    is_cs_supported = False
    power_event_type = None
    app_window_state = None
    app_flip_type = None
    blc_variant = None
    gfx_vbt = None
    is_hdr = hdr_status = None

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for Event Validation test cases. Helps to initialize some of
    #               the parameters required for Event Validation test execution. It is defined in unittest framework
    #               and being overridden here.
    # @details      This function carries out tasks like setting display config, enable simulated battery, enable HDR
    # @return       None
    @classmethod
    def setUpClass(cls):

        cls.cmd_line_param = cmd_parser.parse_cmdline(
            sys.argv, custom_tags=common.CUSTOM_TAGS + list(cls.custom_tags.keys()))

        # To handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        cls.gfx_vbt = Vbt()

        # Stop etl tracer if started during test environment initialization
        etl_tracer.stop_etl_tracer()
        cls.__prepare_test_from_command_line()
        logging.info(" SETUP: {0} ".format(cls.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))

        dut.prepare(power_source=display_power.PowerSource.DC)

        # checking panel requirement
        logging.info("Checking panel config {0} requirement".format(cls.panel_config))
        status = cls.check_panel_config(cls.panel_config)
        assert status, "FAILED to meet panel config {0} requirement (Planning Issue)".format(cls.panel_config)

        # Clear OS display off timeout values
        for pwr_line_status in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
            if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 0, pwr_line_status) is False:
                logging.warning("\tFAILED to reset display off timeout to {0}".format(pwr_line_status.name))

        # Disable driver, enable the etl tracing and enable the driver to have ETL from driver init
        logging.info("STEP: Restarting display gfx-driver")
        for adapter in dut.adapters.values():
            is_mipi_present = False
            for panel in adapter.panels.values():
                if panel.panel_type == "MIPI":
                    is_mipi_present = True
                    break

            assert display_essential.disable_driver(adapter.gfx_index), \
                "Failed to disable display gfx-driver (Test Issue)"
            time.sleep(2)
            trace_type = etl_tracer.TraceType.TRACE_ALL
            # Switch to PC ETL if test is not loglevel debug and PreGen13 (Gen9/10/11/11.5/12) or MIPI port
            if cls.cmd_line_param[0]['LOGLEVEL'] != 'DEBUG' and (
                    adapter.name in common.PRE_GEN_13_PLATFORMS or is_mipi_present):
                trace_type = etl_tracer.TraceType.TRACE_PC_ONLY

            assert etl_tracer.start_etl_tracer(trace_type), "FAILED to start ETL tracer (Test Issue)"
            time.sleep(3)
            assert display_essential.enable_driver(adapter.gfx_index), \
                "FAILED to enable display gfx-driver (Test Issue)"
            logging.info("\tSuccessfully restarted the display gfx-driver")

        logging.info(" SCENARIO: {0} ".format(cls.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))
        # LACE verification for Legacy platforms only
        if not common.IS_DDRW:
            # Applying lux= 1000 with als override
            logging.info("Step: Applying lux= 1000, override= True")
            if powercons_escapes.als_override(True, 1000) is not True:
                assert False, "Failed to apply lux= 1000 (Test Issue)"
            logging.info("\tApplied lux successfully")

    ##
    # @brief        This function is used to get the panel config, feature tag, custom flags from command line
    # @return       None
    @classmethod
    def __prepare_test_from_command_line(cls):
        # Iterate through the command line to get panel config
        assert len(cls.cmd_line_param[0]['PANEL_CONFIG']), "PANEL_CONFIG is EMPTY (Commandline Issue)"
        cls.panel_config = cls.cmd_line_param[0]['PANEL_CONFIG'][0]
        assert cls.panel_config in cls.custom_tags.get('-PANEL_CONFIG'), "PANEL_CONFIG is INVALID (Commandline Issue)"

        # Iterate through the command line to get feature tag if present
        if cls.cmd_line_param[0]['FEATURE'] != 'NONE':
            assert len(cls.cmd_line_param[0]['FEATURE']), "FEATURE is EMPTY (Commandline Issue)"
            cls.cmd_feature = cls.cmd_line_param[0]['FEATURE'][0]
            assert cls.cmd_feature in cls.custom_tags.get('-FEATURE'), "FEATURE is INVALID (Commandline Issue)"

        # Get the custom flags parsed from the command line
        for event_type in ['CS', 'S3', 'S4']:
            if cls.cmd_line_param[0][event_type] != 'NONE':
                cls.power_event_type = event_type.upper()
        for wind_state in ['FULLSCREEN', 'WINDOWED']:
            if cls.cmd_line_param[0][wind_state] != 'NONE':
                cls.app_window_state = wind_state.upper()
        for flip_type in ['ASYNC', 'VSYNC']:
            if cls.cmd_line_param[0][flip_type] != 'NONE':
                cls.app_flip_type = flip_type.upper()
        for blc_nits in ['NITS', 'HIGH_PRECISION']:
            if cls.cmd_line_param[0][blc_nits] != 'NONE':
                cls.blc_variant = blc_nits
                if cls.blc_variant == "NITS":
                    if len(cls.cmd_line_param[0][blc_nits]) != 0:
                        # [30_590_1]->['30', '590', '1']
                        cls.nits_ranges_values = cls.cmd_line_param[0][blc_nits][0].split("_", 2)
                    else:
                        assert False, "NO Nits ranges are provided (command-line issue)"
                elif cls.blc_variant == "HIGH_PRECISION" and len(cls.cmd_line_param[0][blc_nits]) != 0:
                    cls.precision_ranges_values = cls.cmd_line_param[0][blc_nits][0]
                    # [1000_2000_200] -> [1000, 2000, 200]
                    cls.precision_ranges_values = cls.precision_ranges_values.split("_", 2)

        if cls.cmd_line_param[0]['HDR'] != 'NONE':
            cls.hdr_status = True if cls.cmd_line_param[0]['HDR'][0] == 'TRUE' else False

        cls.cmd_test_name = cls.cmd_line_param[0]['FILENAME'].split("\\")[-1].split(".")[0].upper()

        # Validate the custom flags
        cls.is_cs_supported = cls.display_power_.is_power_state_supported(display_power.PowerEvent.CS)

        if cls.power_event_type == 'CS' and not cls.is_cs_supported:
            assert False, "Test needs Connected Standby enabled, but disabled in the system (Planning Issue)"

        if cls.power_event_type == 'S3' and cls.is_cs_supported:
            assert False, "Test needs Connected Standby disabled, but enabled in the system (Planning Issue)"

        if cls.cmd_test_name == 'POWER_EVENT':
            assert cls.power_event_type is not None, "CS/S3/S4 NOT specified in command line (Commandline Issue)"
            cls.cmd_test_name = cls.cmd_test_name + '_' + cls.power_event_type

        if cls.cmd_test_name == 'RUN_3D':
            if cls.app_flip_type is None or cls.app_window_state is None:
                assert False, "Fullscreen/Windowed or Async/VSync NOT specified in command line (Commandline Issue)"
            cls.cmd_test_name = cls.cmd_test_name + '_' + cls.app_flip_type + '_' + cls.app_window_state

    ##
    # @brief        This method is the exit point for Event Validation test cases. This resets the  changes done
    #               for execution of Event Validation tests
    # @return       None
    @classmethod
    def tearDownClass(cls):

        logging.info(" TEARDOWN: {0} ".format(cls.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))

        etl_tracer.stop_etl_tracer()
        do_driver_restart = False
        for adapter in dut.adapters.values():
            if cls.blc_variant == "NITS":
                for panel in adapter.panels.values():
                    status = blc.delete_lfp_nit_ranges(adapter, panel)
                    if status is False:
                        logging.warning("FAILED to delete LFP Nit ranges")
                    do_driver_restart = True if status is True else do_driver_restart

            if cls.blc_variant == "HIGH_PRECISION":
                status = blc.disable_high_precision(adapter)
                if status is False:
                    logging.warning("FAILED to disable High Precision")
                do_driver_restart = True if status is True else do_driver_restart

            # Disable HDR if specified (ForceHDRMode)
            if cls.hdr_status:
                status = blc.disable_hdr(adapter, os_aware=False)
                if status is False:
                    logging.warning("FAILED to disable HDR via INF")
                do_driver_restart = True if status is True else do_driver_restart

            if cls.panel_config == "DPST_OVERRIDE":
                status = dpst.set_bpp_override(adapter, override=False)
                if status is False:
                    logging.warning("FAILED to disable DPST BPP Override")
                do_driver_restart = True if status is True else do_driver_restart

            # Enable VRR
            vrr_status = vrr.enable(adapter)
            if vrr_status is False:
                logging.error(f"FAILED to enable VRR via reg_key on {adapter.name}")
            elif vrr_status is True:
                do_driver_restart = True
            lrr_status = lrr.enable(adapter)
            if lrr_status is False:
                logging.error(f"FAILED to enable LRR via reg_key on {adapter.name}")
            elif lrr_status is True:
                do_driver_restart = True

            if do_driver_restart:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    logging.warning("\tFAILED to restart the display-driver")
                else:
                    logging.info("\tSuccessfully restarted the display-driver")

            if not common.IS_DDRW:
                # Resetting the als override
                logging.info("STEP: Resetting ALS override & lux value to 0")
                if powercons_escapes.als_override(False, 0) is False:
                    logging.warning("\tFAILED to reset ALS override & lux value to 0")
                else:
                    logging.info("\tPASS: Successfully reset ALS override & lux value to 0")

        # Resetting the power_scheme to Balanced
        logging.info("STEP: Resetting current power scheme to POWER_SCHEME_BALANCED")
        if cls.display_power_.set_current_power_scheme(display_power.PowerScheme.BALANCED) is False:
            logging.warning("\tFAILED to reset current power scheme to POWER_SCHEME_BALANCED")
        else:
            logging.info("\tSuccessfully reset current power scheme to POWER_SCHEME_BALANCED")

        # Clearing the display time-out
        for power_line_state in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
            logging.info("STEP: Clearing display time-out for {0}".format(power_line_state.name))
            if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 0, power_line_state) is False:
                logging.warning("\tFAILED to clear display time-out")
            else:
                logging.info("\tPASS: Successfully cleared display time-out")

        # Move mouse to make sure display is in ON state before exiting the test
        win32api.SetCursorPos((400, 400))
        winkb_helper.press('ESC')
        dut.reset()

    ############################
    # Helper Functions
    ############################

    # Check the panel config
    ##
    # @brief        This method is used to check the panels support the given config
    # @param[in]    cmd_panel_config string indicating the config of the panel
    # @return       True if the given config enabling is successful, False otherwise
    @classmethod
    def check_panel_config(cls, cmd_panel_config):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                if panel.panel_type == "DP":
                    # Disable PSR
                    if psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1) is False:
                        assert False, "FAILED to restart driver after disabling PSR"
                    # Disable VRR
                    if vrr.disable(adapter) is False:
                        assert False, "FAILED to disable VRR"

                if cmd_panel_config in ['PSR1', 'PSR2']:
                    # Check panel is PSR1/2, and do the pre-requisites
                    feature = psr.UserRequestedFeature.PSR_1 if cmd_panel_config == 'PSR1' \
                        else psr.UserRequestedFeature.PSR_2
                    # Check panel supports PSR1/PSR2
                    logging.info("STEP: Checking whether eDP(s) supports {0}".format(cmd_panel_config))

                    if feature == psr.UserRequestedFeature.PSR_2 and panel.psr_caps.is_psr2_supported is False:
                        logging.error("\tFAIL: {0} does NOT support {1} (Planning Issue)".format(
                            panel.port, cmd_panel_config))
                        return False
                    elif feature == psr.UserRequestedFeature.PSR_1 and panel.psr_caps.is_psr_supported is False:
                        logging.error("\tFAIL: {0} does NOT support {1} (Planning Issue)".format(
                            panel.port, cmd_panel_config))
                        return False
                    logging.info("\tPASS: {0} supports {1}".format(panel.port, cmd_panel_config))

                    if cmd_panel_config == "PSR1":
                        # Disable PSR2
                        if psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2) is False:
                            return False
                    else:
                        # Enable PSR2
                        if psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2) is False:
                            return False

                        # Disable LRR
                        if lrr.disable(adapter=adapter) is False:
                            return False

                    # Enable PSR
                    if psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1) is False:
                        return False

                # Check panel is multi-RR panel, enable static/seamless DRRS from registry
                elif cmd_panel_config in ['STATIC_DRRS', 'SEAMLESS_DRRS']:
                    # Check panel supports multi-RR
                    logging.info("STEP: Checking whether LFP(s) supports multi RR")

                    rr_list = common.get_supported_refresh_rates(panel.target_id)
                    if panel.panel_type == "MIPI":
                        seamless_min_rr = cls.gfx_vbt.block_42.SeamlessDrrsMinRR[
                            cls.gfx_vbt.get_panel_index_for_port(panel.port)]
                        if seamless_min_rr != 0:
                            rr_list.append(seamless_min_rr)
                        if len(rr_list) < 2:
                            logging.error("\t{0} does NOT support multi RR (Planning Issue)".format(panel.port))
                            return False
                        logging.info("\tPASS: {0} supports multi RR (DTD): [MinRR= {1}, MaxRR= {2}]".format(
                            panel.port, min(rr_list), max(rr_list)))
                    else:
                        if panel.drrs_caps.is_drrs_supported is False:
                            logging.error("\t{0} does NOT support multi RR (Planning Issue)".format(panel.port))
                            return False
                        logging.info(f"{panel.drrs_caps}")

                    if not common.IS_DDRW:
                        # Enable Static DRRS
                        # @todo Requested dev to enable this regkey, once implemented, need to remove the condition
                        logging.info("STEP: Enabling {0} in {1}".format(cmd_panel_config, adapter))
                        if cmd_panel_config == 'STATIC_DRRS':
                            reg_value = registry.RegValues.DRRS.STATIC_DRRS_ENABLE
                            if registry.write(adapter.gfx_index, registry.RegKeys.DRRS.DRRS_ENABLE,
                                              registry_access.RegDataType.DWORD, reg_value) is False:
                                logging.error(f"\tFAILED to enable {cmd_panel_config} in {adapter.gfx_index}")
                                return False
                        else:
                            if drrs.enable(adapter) is False:
                                return False
                        logging.info("\tPASS: Successfully enabled {0} in {1}".format(cmd_panel_config, adapter))

                        # Enabling DRRS MAM (Needed only for Seamless ?)
                        logging.info("Step: Enabling DRRS MAM in {0}".format(adapter))
                        if registry.write(adapter.gfx_index, registry.RegKeys.DRRS.DRRS_MAM_SUPPORT,
                                          registry_access.RegDataType.DWORD, registry.RegValues.ENABLE) is False:
                            logging.error("\tFAILED to enable DRRS MAM in {0}".format(adapter.gfx_index))
                            return False
                        logging.info("\tPASS: Successfully enabled DRRS MAM in {0}".format(adapter.gfx_index))

                # Enable DPST override from registry
                elif cmd_panel_config == 'DPST_OVERRIDE':
                    if dpst.set_bpp_override(adapter, override=True) is False:
                        return False

                if bool(cls.blc_variant) is True:
                    logging.info("STEP: Adding Brightness3 support by having {0}".format(cls.blc_variant))
                    if cls.blc_variant == "NITS":
                        if blc.disable_high_precision(adapter) is False:
                            assert False, "FAILED to disable High Precision"
                        cls.nits_ranges_values = blc.create_nit_ranges(cls.nits_ranges_values)
                        if blc.add_lfp_nit_ranges(adapter, panel, cls.nits_ranges_values) is False:
                            assert False, "FAILED to create Nit Ranges"
                    elif cls.blc_variant == "HIGH_PRECISION":
                        if blc.delete_lfp_nit_ranges(adapter, panel) is False:
                            assert False, "FAILED to delete LFP Nit ranges"
                        if blc.enable_high_precision(adapter) is False:
                            assert False, "FAILED to enable High Precision"

                # Enable HDR if specified (ForceHDRMode)
                if cls.cmd_line_param[0]['HDR'] != 'NONE':
                    cls.is_hdr = panel.hdr_caps.is_hdr_supported
                    assert cls.is_hdr, f"{panel.port} does not support HDR on PIPE_{panel.pipe}"
                    if cls.is_hdr and cls.hdr_status:
                        if blc.enable_hdr(adapter) is False:
                            assert False, "FAILED to enable HDR via INF"

                # only for legacy platforms
                if not common.IS_DDRW:
                    # Enable Lace
                    if common.PLATFORM_NAME not in common.PRE_GEN_11_P_5_PLATFORMS:
                        logging.info("STEP: Enabling LACE in {0}".format(adapter.gfx_index))
                        reg_args = registry_access.LegacyRegArgs(
                            registry_access.HKey.LOCAL_MACHINE, "SOFTWARE\\Intel\\Display")
                        if registry_access.write(reg_args, "BKPDisplayLACE", registry_access.RegDataType.DWORD,
                                                 registry.RegValues.ENABLE, r"igfxcui\MISC") is False:
                            logging.error("\tFAILED to enable LACE for {0}".format(adapter.gfx_index))
                            return False
                        logging.info("\tPASS: Successfully enabled LACE for {0}".format(adapter.gfx_index))

        # Disable and enable of gfx-driver will be done while starting ETL tracer
        return True

    # Stop the the trace and start the validators verification
    ##
    # @brief        This is a helper function to stop the trace and start the validator verification
    # @return       None
    def check_validators(self):
        # Stop the trace
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("FAILED to stop ETL tracer (Test Issue)")
        logging.info("Successfully stopped ETL tracer")

        logging.info(" VERIFICATION: {0} ".format(self.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))

        ftr_group = None
        ftr_flags = ['BLC', 'DPST']

        if 'DRRS' in self.panel_config:
            ftr_group = 'DRRS'
            ftr_flags.append('DRRS')
        elif 'DPST' in self.panel_config:
            ftr_group = 'DPST_OVERRIDE'

        # Todo: DPST status state-machine need not be exercised
        if self.cmd_line_param[0]['HDR'] != 'NONE':
            ftr_flags.remove('DPST')

        pass_count = 0
        fail_count = 0
        failed_validators = []

        # DiAna verification for Yangra
        if common.IS_DDRW:
            # Converting the ETL Bytes value received from stat function to GB
            etl_file_size = round((os.stat(etl_tracer.GFX_TRACE_ETL_FILE).st_size / pow(1024, 3)), 2)
            logging.info(f"Test has generated ETL File {etl_tracer.GFX_TRACE_ETL_FILE} with size of {etl_file_size} GB")
            get_only_error = etl_file_size > 1  # if >1 GB of ETL file
            log_file = validator_runner.run_diana(self.cmd_test_name, etl_tracer.GFX_TRACE_ETL_FILE,
                                                   ftr_flags, get_only_error)
            if log_file is None:
                self.fail("FAILED to execute run_diana()")
            diana_result = validator_runner.parse_diana_output(log_file, ftr_flags)
            if diana_result is None:
                self.fail("FAILED to get DiAna result (Test Issue)")

            if bool(diana_result) is False:
                self.fail("DiAna result is empty (Test Issue)")

            for validator, report in diana_result.items():
                if report['RESULT'] == 'PASS':
                    logging.info("DiAna Validator \'{0:40}: PASSED (Log file - {1})".format(
                        validator + '\'', report["FILE"]))
                    pass_count += 1
                else:
                    logging.error("DiAna Validator \'{0:40}: FAILED (Log file - {1})\nError: \n{2}".format(
                        validator + '\'', report["FILE"], '\n'.join(report['DETAILS'])))
                    sub_component = validator.split("_", 1)[0].upper()  # BLC from BLC_DUTYCYLE
                    gdhm_title = "[PowerCons][{0}] {1} (DiAna) validator failed".format(
                        sub_component, validator)
                    gdhm.report_bug(
                        title=gdhm_title,
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    fail_count += 1
                    failed_validators.append(validator + '(DiAna)')
        # PowerCons EXE verification for Legacy
        else:
            validators = validator_runner.get_validators(group=ftr_group, feature=self.cmd_feature)
            if validators is None:
                self.fail("FAILED to get validators list (Test Issue)")
            logging.info("Selected list of validators are: {0}".format(', '.join(validators)))

            request_xml_file = validator_runner.create_validator_request(
                self.cmd_test_name, etl_tracer.GFX_TRACE_ETL_FILE, validators)
            if request_xml_file is None:
                self.fail("FAILED to create request xml file (Test Issue)")

            validator_result = validator_runner.run_validators(self.cmd_test_name, request_xml_file)
            if validator_result is None:
                self.fail("FAILED to get validators result (Test Issue)")
            for validator in validators:
                if validator in validator_result.keys():
                    if validator_result[validator]['result'].lower() == 'pass':
                        logging.info("Validator \'{0:40}: PASSED".format(validator + '\''))
                        pass_count += 1
                    else:
                        logging.error("Validator \'{0:40}: FAILED \nError: {1}".format(
                            validator + '\'', validator_result[validator]['error']))
                        sub_component = validator.split("-", 1)[0].upper()  # BLC from BLC-DUTY-CYLE
                        gdhm_title = "[PowerCons][{0}] {1} (EXE) validator failed during {2} scenario".format(
                            sub_component, validator, self.cmd_test_name)
                        gdhm.report_bug(
                            title=gdhm_title,
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        fail_count += 1
                        failed_validators.append(validator)
                else:
                    logging.error("Validator \'{0:40}: FAILED to get result".format(validator + '\''))
                    fail_count += 1
                    failed_validators.append(validator)

        if fail_count != 0:
            logging.error("SUMMARY: {2} Validators FAILED - Total= {0}, Pass= {1}, Fail= {2}".format(
                pass_count + fail_count, pass_count, fail_count))
            logging.error("Failed Validators: {0}".format(', '.join(sorted(failed_validators))))
            self.fail("FAILED Validators: {0} (Check Validator specific log file for more details)".format(
                ', '.join(sorted(failed_validators))))

        logging.info("SUMMARY: All Validators PASSED - Total= {0}".format(pass_count))
