########################################################################################################################
# @file         cfps_base.py
# @brief        Base class for all CFPS tests
# @details      This file implements setUp and tearDown methods of unittest framework.
#               In setUp, command_line arguments are parsed, eDP panel's existence is checked.
#               In tearDown method, the displays which were plugged in the setUp method are unplugged and TDR check is
#               done.
# @author       Vinod D S
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import enum, cmd_parser, display_essential, display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar, VerifyScalarProgramming
from Libs.Feature.display_fbc import fbc
from Libs.Feature.powercons import registry
from Tests.Color.Verification import feature_basic_verify
from Tests.Display_Decompression.Playback.decomp_verifier import get_pixel_format, verify_render_decomp, get_app_name
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Modules import common, dut
from Tests.VRR import vrr


##
# @brief        Exposed Class to write Cfps tests. Any new Cfps test class can inherit this class to use common setUp
#               and tearDown functions.
class CfpsBase(unittest.TestCase):
    cmd_line_param = None
    is_auto = False
    power_event = None
    display_config_ = DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    under_run_monitor_ = UnderRunStatus()
    is_cs_supported = None

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for DPST test cases. Helps to initialize some of the
    #               parameters required for Cfps test execution. It is defined in unittest framework and being
    #               overridden here.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios, checks for the power event and validates custom flags in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: CFPS_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-CS', '-S3', '-S4'])

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if isinstance(cls.cmd_line_param[0]['STATE'], list):
            if 'AUTO' in cls.cmd_line_param[0]['STATE']:
                cls.is_auto = True

        # Check whether power event case
        if cls.cmd_line_param[0]['CS'] != 'NONE':
            cls.power_event = display_power.PowerEvent.CS
        if cls.cmd_line_param[0]['S3'] != 'NONE':
            cls.power_event = display_power.PowerEvent.S3
        if cls.cmd_line_param[0]['S4'] != 'NONE':
            cls.power_event = display_power.PowerEvent.S4

        # Validate the custom flags
        cls.is_cs_supported = cls.display_power_.is_power_state_supported(display_power.PowerEvent.CS)
        if cls.power_event == display_power.PowerEvent.CS and not cls.is_cs_supported:
            assert False, "Test needs Connected Standby enabled, but disabled in the system (Planning Issue)"
        if cls.power_event == display_power.PowerEvent.S3 and cls.is_cs_supported:
            assert False, "Test needs Connected Standby disabled, but enabled in the system (Planning Issue)"

        # Enable Simulated Battery
        assert cls.display_power_.enable_disable_simulated_battery(True), "FAILED to enable Simulated Battery"
        dut.prepare()

    ##
    # @brief        This method is the exit point for Cfps test cases. This resets the environment changes done
    #               for execution of Cfps tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: CFPS_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        for adapter in dut.adapters.values():
            # Panel being None, will enable for all the panels in adapter
            if cfps.enable(adapter, panel=None, is_auto=True) is False:
                assert False, f"FAILED to restore CFPS for {adapter.name} (Test Issue)"
            if adapter.is_vrr_supported is True:
                assert vrr.enable(adapter), "Failed to enable VRR"
        # Re-setting power plan to default power plan POWER_SCHEME_BALANCED as it is getting set in
        logging.info(f"Step: Setting current power plan to POWER_SCHEME_BALANCED")
        for power_line_state in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
            if cls.display_power_.set_current_powerline_status(power_line_state) is False:
                assert False, f"Failed to set current power line status to {power_line_state.name}"
            if cls.display_power_.set_current_power_scheme(display_power.PowerScheme.BALANCED) is False:
                assert False, "FAILED to set current power scheme (Test Issue)"
            logging.info("\tSet current power scheme successfully")
        dut.reset()

    ##
    # @brief        This method is the exit point for Cfps test cases in CfpsBase test class. This resets the
    #               environment changes done for execution of Cfps tests
    # @return       None
    def tearDown(self):
        self.under_run_monitor_.verify_underrun()
        for gfx_index in dut.adapters:
            display_essential.detect_system_tdr(gfx_index=gfx_index)

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function to make sure all the requirements are met before test.
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        for adapter in dut.adapters.values():
            feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
            if feature_test_control.dfps_disable == 0:
                feature_test_control.dfps_disable = 1
                if feature_test_control.update(adapter.gfx_index) is False:
                    assert False, "FAILED to update registry - FeatureTestControl"
                status, reboot_required = display_essential.restart_gfx_driver()
                assert status, "FAILED to restart display driver"

    ##
    # @brief        Test function is to enable Cfps for the connected adapters. It logs a failure message if the
    #               enabling is not successful
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_cfps(self):
        for adapter in dut.adapters.values():
            # Panel being None, will enable for all the panels in adapter
            if cfps.enable(adapter, None, self.is_auto) is False:
                self.fail(f"FAILED to enable CFPS for {adapter.name} (Test Issue)")

    ############################
    # Helper Function
    ############################

    ##
    # @brief        Helper function to handle all the common steps required for all the tests like opening/closing of
    #               game, cfps verification etc.
    # @param[in]    full_screen Boolean, True= game will be played in full screen mode, False= windowed mode
    # @param[in]    power_event [optional] Enum, CS/S3/S4
    # @param[in]    concurrent_feature [optional]
    # @return       Boolean True if cfps verification is successful, None OS not sending Async flips, False otherwise
    @staticmethod
    def validate_cfps(full_screen, power_event=None, concurrent_feature=cfps.Feature.NONE):
        etl_file, _ = cfps.run_workload(full_screen, power_event)

        cfps_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"Step: Verifying CFPS for adapter {adapter.gfx_index}")
                cfps_status &= cfps.verify(adapter, etl_file)
                feature_status = True
                if concurrent_feature != cfps.Feature.NONE:
                    concurrent_feature_name = cfps.Feature(concurrent_feature).name
                    logging.info(f"Verifying {concurrent_feature_name} for "
                                 f"{panel.port}(PIPE_{panel.pipe}) on {adapter.gfx_index}")
                    if concurrent_feature == cfps.Feature.HDR:
                        feature_status &= feature_basic_verify.verify_hdr_feature(panel.gfx_index, adapter.name,
                                                                                  panel.pipe,
                                                                                  enable=True)
                    if concurrent_feature == cfps.Feature.FBC:
                        feature_status &= fbc.verify_adapter_fbc(adapter.gfx_index)
                    elif concurrent_feature == cfps.Feature.RENDER_DECOMPRESSION:
                        source_format = get_pixel_format('RGB_8888')
                        feature_status &= verify_render_decomp(panel, source_format, etl_file,
                                                               get_app_name('MOVINGRECTANGLEAPP'))
                    elif concurrent_feature == cfps.Feature.MPO:
                        feature_status &= pc_external.verify_mpo(adapter, panel, etl_file)
                    elif concurrent_feature == cfps.Feature.FLIPQ:
                        feature_status &= planes_ui_verification.verify_flipq(etl_file, panel.pipe, panel.target_id,
                                                                              adapter.name)
                    elif concurrent_feature == cfps.Feature.PIPE_SCALAR:
                        feature_status &= VerifyScalarProgramming([DisplayScalar(panel.port, "MAR")])
                    # TODO: Add hardware rotation verification
                    cfps_status &= feature_status
                    logging_str = f"{concurrent_feature_name} verification for {panel.port}(PIPE_{panel.pipe})"
                    if feature_status is False:
                        logging.error(f"FAIL: {logging_str}")
                    else:
                        logging.info(f"PASS: {logging_str}")

        return cfps_status

    ##
    # @brief        Helper function to check that CFPS is expected or not
    # @param[in]    power_plan Boolean, power plan enum
    # @param[in]    power_source Boolean, power source enum
    # @return       Boolean True if cfps expected, False otherwise
    @staticmethod
    def is_cfps_expected(self, power_plan, power_source):
        # According to current driver policy, HighPerformance plan will not be applied when CS is enabled
        if (self.is_auto is False) or \
                (self.is_auto and power_source == display_power.PowerSource.DC and
                 (power_plan != display_power.PowerScheme.HIGH_PERFORMANCE or self.is_cs_supported)):
            return True
        return False

    ##
    # @brief        Helper function to handle all the common steps required for all the tests like opening/closing of
    #               game, cfps verification with parameters like power plan, power source and power event  .
    # @param[in]    full_screen Boolean, True= game will be played in full screen mode, False= windowed mode
    # @param[in]    power_plan
    # @param[in]    power_source indicates the power source connected AC/DC
    # @param[in]    power_event [optional] Enum, CS/S3/S4
    # @return       None
    def validate_cfps_with(self, full_screen, power_plan, power_source, power_event=None):

        method = "FULL_SCREEN" if full_screen else "WINDOWED"

        # Switch Power line status
        logging.info(f"Step: Setting power line status to {power_source.name}")
        if not self.display_power_.set_current_powerline_status(power_source):
            self.fail("FAILED to switch power line status (Test Issue)")

        # Set power_scheme
        logging.info(f"Step: Setting current power plan to {power_plan.name}")
        if self.display_power_.set_current_power_scheme(power_plan) is False:
            self.fail(f"FAILED to set current power scheme (Test Issue)")
        logging.info("\tSet current power scheme successfully")

        status = self.validate_cfps(full_screen, power_event)
        restrictions = f"{method}, {power_plan.name}, {power_source.name}, Auto= {self.is_auto}, " \
                       f"CS Supported= {self.is_cs_supported}"

        if status is None:
            self.fail(f"Verification Skipped: OS is not sending async flips with {restrictions}")
        logging.info(f"Step: Verifying CFPS for {restrictions}")
        if self.is_cfps_expected(self, power_plan, power_source):
            if status is False:
                gdhm.report_bug(
                    title=f"[PowerCons][CFPS] CFPS is NOT functional with {restrictions} (Unexpected)",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail(f"FAIL: CFPS is NOT Functional with {restrictions} (Unexpected)")
            logging.info(f"PASS: CFPS is Functional with {restrictions} (Expected)")
        else:
            if status:
                gdhm.report_bug(
                    title=f"[PowerCons][CFPS] CFPS is functional with {restrictions} (Unexpected)",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail(f"FAIL: CFPS is Functional with {restrictions} (Unexpected)")
            logging.info(f"PASS: CFPS is NOT functional with {restrictions} (Expected)")
