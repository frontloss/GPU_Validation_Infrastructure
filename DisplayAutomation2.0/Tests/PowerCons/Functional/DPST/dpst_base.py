########################################################################################################################
# @file         dpst_base.py
# @brief        Contains base class for all DPST and OPST tests
# @details      @ref dpst_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all DPST and OPST tests, and helper functions.
#
# @author       Ashish Tripathi
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser, window_helper, display_essential
from Libs.Core import display_power
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar, VerifyScalarProgramming
from Libs.Feature.display_fbc import fbc
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Modules import common, desktop_controls, dut, windows_brightness, workload
from registers.mmioregister import MMIORegister

MAX_MILLI_PERCENT = blc.MilliPercentage.MAX.value
MIN_MILLI_PERCENT = blc.MilliPercentage.MIN.value
MAX_PERCENT = blc.Percentage.MAX.value
MIN_PERCENT = blc.Percentage.MIN.value


##
# @brief        Exposed Class to write DPST/OPST tests. Any new DPST/OPST test can inherit this class to use common
#               setUp and tearDown functions.
class DpstBase(unittest.TestCase):
    hdr_status = False
    cmd_line_param = None  # used to store command line parameters
    xpst_feature = dpst.XpstFeature.DPST  # Default assigned with DPST
    xpst_feature_str = dpst.XpstFeature(xpst_feature).name  # Default assigned with DPST
    bpp_override_required = False
    dpst_threshold = None
    display_power_ = display_power.DisplayPower()
    lower_threshold = None
    upper_threshold = None
    disable_boost_nit_ranges = None
    nit_ranges = None
    max_smoothening_speed = None
    max_fall = None
    is_nits_supported = False
    is_high_precision = False
    level_without_dpst = []
    level_with_dpst = []
    no_of_ranges = 0
    nit_range = []
    count = None
    delay = None
    offsets = None

    # Default aggressiveness Level 1 with OPST and aggressiveness Level 6 with DPST.
    # in setup phase will be default for DPST
    aggressiveness_level = {
        gfx_index: dpst.Aggressiveness.LEVEL_6
        for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
    }

    ############################
    # Default UnitTest Functions
    ############################
    ##
    # @brief        This class method is the entry point for DPST/OPST test cases. Helps to initialize few of the
    #               parameters required for SPI test execution. It is defined in unittest framework and being overridden
    #               here
    # @details      This function checks for feature support and initializes parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-CS', '-MIN_RR'])

        # To handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if cls.cmd_line_param[0]['OPST'] != 'NONE':
            cls.xpst_feature = dpst.XpstFeature.OPST

        logging.info(" SETUP: {0}".format(cls.xpst_feature_str).center(common.MAX_LINE_WIDTH, "*"))

        cls.workload_method = dpst.WorkloadMethod.IDLE
        if isinstance(cls.cmd_line_param[0]['METHOD'], list):
            if 'IMAGE' in cls.cmd_line_param[0]['METHOD']:
                cls.workload_type = dpst.WorkloadMethod.GOLDEN_IMAGE
            elif 'APP' in cls.cmd_line_param[0]['METHOD']:
                cls.workload_method = dpst.WorkloadMethod.PSR_UTIL

        if cls.cmd_line_param[0]['BLC_THRESHOLD'] != 'NONE':
            cls.dpst_threshold = int(cls.cmd_line_param[0]['BLC_THRESHOLD'][0])

        if cls.cmd_line_param[0]['LOWER_BLC_THRESHOLD'] != 'NONE':
            cls.lower_threshold = int(cls.cmd_line_param[0]['LOWER_BLC_THRESHOLD'][0])

        if cls.cmd_line_param[0]['UPPER_BLC_THRESHOLD'] != 'NONE':
            cls.upper_threshold = int(cls.cmd_line_param[0]['UPPER_BLC_THRESHOLD'][0])

        cls.is_high_precision = cls.cmd_line_param[0]['HIGH_PRECISION'] != 'NONE'
        cls.disable_boost_nit_ranges = cls.cmd_line_param[0]['NIT_RANGES_FFFF'] != 'NONE'

        if cls.cmd_line_param[0]['NIT_RANGES'] != 'NONE':
            cls.nit_ranges = cls.cmd_line_param[0]['NIT_RANGES'][0].split("_")
            if cls.nit_ranges is None:
                assert False, "NO Nits ranges are provided (command-line issue)"
            cls.nit_ranges = blc.create_nit_ranges(cls.nit_ranges)
            cls.is_nits_supported = True

        # default iteration will keep as 10
        cls.count = 10
        if cls.cmd_line_param[0]['COUNT'] != 'NONE':
            cls.count = int(cls.cmd_line_param[0]['COUNT'][0])

        # Keeping default delay is 1 sec
        cls.delay = 1
        if cls.cmd_line_param[0]['TIME_DELAY'] != 'NONE':
            cls.delay = int(cls.cmd_line_param[0]['TIME_DELAY'][0])

        # default smoothening speed in driver is 800
        cls.max_smoothening_speed = 800
        if cls.cmd_line_param[0]['MAX_SMOOTHENING_SPEED'] != 'NONE':
            cls.max_smoothening_speed = int(cls.cmd_line_param[0]['MAX_SMOOTHENING_SPEED'][0])

        if (cls.dpst_threshold is not None) and (MIN_PERCENT <= cls.dpst_threshold <= MAX_PERCENT) is False:
            assert False, "Threshold value will be in percent within range (0 - 100) (Commandline issue)"

        if (cls.lower_threshold is not None and cls.lower_threshold < MIN_MILLI_PERCENT) or \
                (cls.upper_threshold is not None and cls.upper_threshold > MAX_MILLI_PERCENT):
            assert False, "Threshold value will be in milli-percent within range (0 - 100000) (Commandline issue)"

        # Iterate through the command line to get BPC_Value to override registry for 6BPC
        cls.bpp_override_required = cls.cmd_line_param[0]['BPC_VALUE'][0] == '6'

        dut.prepare(power_source=workload.PowerSource.DC_MODE)

        max_fall = 0
        for adapter in dut.adapters.values():
            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                cls.offsets = dpst.get_polling_offsets(adapter, cls.xpst_feature)
            if cls.cmd_line_param[0]['LEVEL'] != 'NONE':
                cls.aggressiveness_level[adapter.gfx_index] = int(cls.cmd_line_param[0]['LEVEL'][0])
            for idx, panel in enumerate(adapter.panels.values()):
                if cls.xpst_feature == dpst.XpstFeature.OPST:
                    vbt_params = dpst.XpstVbtParams()
                    vbt_params.dpst_status = False
                    vbt_params.opst_status = True
                    if dpst.configure_vbt(adapter, panel, vbt_params) is False:
                        assert False, "OPST : Failed to apply VBT change to OPST"

                if cls.cmd_line_param[0]['HDR'] != 'NONE':
                    assert panel.hdr_caps.is_hdr_supported, f"{panel.port} does not support HDR on PIPE_{panel.pipe}"
                    cls.hdr_status = True if cls.cmd_line_param[0]['HDR'][0] == 'TRUE' else False
                if (panel.max_fall and panel.max_cll) != 0:
                    cls.is_nits_supported = True
                    # consider only for first LFP
                    if idx == 0:
                        max_fall = panel.max_fall

        # Hiding the task-bar to make sure that there's no update on screen
        assert window_helper.toggle_task_bar(window_helper.Visibility.HIDE), "FAILED to hide the task-bar"
        logging.info("\tSuccessfully hide the task-bar")

        # Clear display off timeout values in OS
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, workload.PowerSource.AC_MODE) is False:
            logging.warning("FAILED to reset display off timeout values in AC")
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, workload.PowerSource.DC_MODE) is False:
            logging.warning("FAILED to reset display off timeout values in DC")

        max_nits = max_fall if cls.nit_ranges is None else int(cls.nit_ranges[-1][1])

        if (cls.dpst_threshold or cls.lower_threshold or cls.upper_threshold) is not None:
            thresholds = [cls.dpst_threshold, cls.lower_threshold, cls.upper_threshold]
            blc_args = [cls.is_high_precision, cls.is_nits_supported, max_nits]
            levels = dpst.generate_brightness_levels(thresholds, blc_args)
            cls.level_without_dpst = levels[0]
            cls.level_with_dpst = levels[1]

    ##
    # @brief        This method is the exit point for DPST/OPST test cases. This resets the environment changes done
    #               for execution of DPST/OPST tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: {0} ".format(cls.xpst_feature_str).center(common.MAX_LINE_WIDTH, "*"))
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                assert dpst.set_default_vbt(adapter, panel), "FAILED to set default VBT"

            do_driver_restart = False
            if cls.nit_ranges is not None:
                for panel in adapter.panels.values():
                    status = blc.delete_lfp_nit_ranges(adapter, panel)
                    if status is False:
                        assert False, f"FAILED to delete Nit Ranges for {panel.port}"
                    do_driver_restart = True if status is True else do_driver_restart
            if cls.bpp_override_required:
                status = dpst.set_bpp_override(adapter, override=False)
                if status is False:
                    assert False, "FAILED to disable BPP override"
                do_driver_restart = True if status is True else do_driver_restart
            if cls.hdr_status:
                status = blc.disable_hdr(adapter, os_aware=False)
                if status is False:
                    assert False, "FAILED to disable HDR"
                do_driver_restart = True if status is True else do_driver_restart
            if (cls.lower_threshold or cls.upper_threshold or cls.dpst_threshold) is not None:
                status = dpst.delete_dpst_backlight_threshold(adapter)
                if status is False:
                    assert False, "FAILED to delete threshold INF"
                do_driver_restart = True if status is True else do_driver_restart

            if cls.is_high_precision is not False:
                status = blc.disable_high_precision(adapter)
                if status is False:
                    assert False, "FAILED to disable High Precision"
                do_driver_restart = True if status is True else do_driver_restart
            elif cls.disable_boost_nit_ranges:
                status = blc.delete_boost_nit_ranges(adapter)
                if status is False:
                    assert False, "FAILED to delete boost nit ranges"
                do_driver_restart = True if status is True else do_driver_restart

            if do_driver_restart:
                result, reboot_required = display_essential.restart_gfx_driver()
                assert result, "FAILED to restart display driver"

        dut.reset()

        if window_helper.toggle_task_bar(window_helper.Visibility.SHOW):
            logging.info("\tSuccessfully un-hide the task-bar")
        else:
            logging.warning("\tFAILED to un-hide the task-bar")

    ############################
    # Test Function
    ############################
    ##
    # @brief        Common requirement test for DPST test cases. All requirement tests will start with t_0
    #               Verifies common hardware and software requirements for all the tests.
    # @note         This is a critical test. Failure of this test will stop the execution of other tests.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        for adapter in dut.adapters.values():
            do_driver_restart = False
            for panel in adapter.panels.values():
                if panel.is_lfp and panel.bpc == 6:
                    logging.info("Checking DPST is NOT functional on 6BPC panel when override INF is not set")
                    if dpst.verify_igcl_values(adapter, panel, self.xpst_feature, False, 0) is False:
                        self.fail("DPST is enabled in IGCL on 6 BPC panel without BPP Override Regkey")
                    logging.info("\tDPST is NOT enabled in IGCL (Expected)")
                    ctl_val = MMIORegister.read('DPST_CTL_REGISTER', 'DPST_CTL_' + panel.pipe,
                                                adapter.name, gfx_index=adapter.gfx_index)
                    if ctl_val.ie_histogram_enable == 1:
                        self.fail("\tDPST is enabled in MMIO on 6BPC panel")
                    logging.info("\tDPST is NOT enabled in MMIO (Expected)")

                if self.bpp_override_required:
                    assert panel.bpc == 6, "FAIL: {0} does NOT support 6 BPC (Planning Issue)".format(panel.port)
                    logging.info("\tPASS: {0} supports 6BPC for overriding the BPP for {1}".format(
                        panel.port, self.xpst_feature_str))
                    status = dpst.set_bpp_override(adapter, override=True)
                    if status is False:
                        assert False, "FAILED to enable BPP override"
                    do_driver_restart = True if status is True else do_driver_restart
                if self.nit_ranges is not None:
                    status = blc.add_lfp_nit_ranges(adapter, panel, self.nit_ranges)
                    if status is False:
                        assert False, "FAILED to add nit ranges"
                    do_driver_restart = True if status is True else do_driver_restart

            if self.hdr_status:
                status = blc.enable_hdr(adapter)
                if status is False:
                    assert False, "FAILED to enable HDR"
                do_driver_restart = True if status is True else do_driver_restart

            if self.dpst_threshold is not None:
                status = dpst.set_dpst_backlight_threshold(adapter, dpst.Threshold.OLD, self.dpst_threshold)
                if status is False:
                    assert False, "FAILED to configure DPST threshold"
                do_driver_restart = True if status is True else do_driver_restart
            if self.lower_threshold is not None:
                status = dpst.set_dpst_backlight_threshold(adapter, dpst.Threshold.LOWER, self.lower_threshold)
                if status is False:
                    assert False, "FAILED to configure DPST lower threshold"
                do_driver_restart = True if status is True else do_driver_restart
            if self.upper_threshold is not None:
                status = dpst.set_dpst_backlight_threshold(adapter, dpst.Threshold.UPPER, self.upper_threshold)
                if status is False:
                    assert False, "FAILED to configure DPST upper threshold"
                do_driver_restart = True if status is True else do_driver_restart

            if self.is_high_precision:
                status = blc.enable_high_precision(adapter)
                if status is False:
                    assert False, "FAILED to enable High Precision"
                do_driver_restart = True if status is True else do_driver_restart
            elif self.disable_boost_nit_ranges:
                status = blc.disable_boost_nit_ranges(adapter)
                if status is False:
                    assert False, "FAILED to disable boost nit ranges"
                do_driver_restart = True if status is True else do_driver_restart

            if do_driver_restart:
                result, reboot_required = display_essential.restart_gfx_driver()
                assert result
            dut.refresh_panel_caps(adapter)

        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()

        if windows_brightness.set_current_brightness(100, 1) is False:
            assert False, "FAILED to apply 100% brightness"
        logging.info("Successfully applied 100% brightness")

    ##
    # @brief        Common requirement test for DPST test cases to verify default settings in IGCL
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_default_igcl_settings(self):
        for adapter in dut.adapters.values():
            gfx_vbt = vbt.Vbt(adapter.gfx_index)
            # CAPI is supported from Gen13+
            if adapter.name in common.PRE_GEN_13_PLATFORMS:
                continue
            sku_name = None
            if adapter.name in ['ADLP']:
                sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
            for panel in adapter.panels.values():
                is_dpst = self.xpst_feature == dpst.XpstFeature.DPST
                # Default DPST level, PreMTL: 6, MTL+: 2,
                # Default OPST level, ADL+: 1
                if is_dpst:
                    if sku_name in ['TwinLake']:
                        expected_level = 3
                    elif adapter.name in common.PRE_GEN_14_PLATFORMS:
                        expected_level = 6
                    else:
                        expected_level = 2
                    expected_status = False if panel.hdr_caps.is_aux_only_brightness else True
                else:
                    expected_level = 2
                    if adapter.name in common.PRE_GEN_15_PLATFORMS:
                        expected_level = 1
                    expected_status = True
                if dpst.verify_igcl_values(adapter, panel, self.xpst_feature, expected_status, expected_level) is False:
                    self.fail("IGCL values are not matching (Unexpected)")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Exposed API to validate the DPST/OPST feature in power source
    # @param[in]    etl_file
    # @param[in]    method enum, WorkloadMethod
    # @param[in]    power_src enum, PowerSource
    # @param[in]    expect_epsm_enable bool, optional
    # @param[in]    concurrent_feature enum, Feature to be verified for concurrency
    # @param[in]    expect_sfsu_enable bool, optional
    # @param[in]    is_psr_enabled_in_igcl bool, optional
    # @return       True if successful, False otherwise
    def validate_xpst(self, etl_file, method: dpst.WorkloadMethod, power_src=workload.PowerSource.DC_MODE,
                      expect_epsm_enable=None, concurrent_feature=dpst.Feature.NONE, expect_sfsu_enable=True,
                      is_psr_enabled_in_igcl=True):
        workload_type_str = dpst.WorkloadMethod(method).name
        pwr_src_str = workload.PowerSource(power_src).name

        # Verify DPST for each adapter and LFP
        status = True
        skip_report_generate = False
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                logging.info("STEP: Verifying {0} on {1}-{2}".format(
                    self.xpst_feature_str, adapter.name, panel.port))
                restriction = "[Method= {0}, AggressivenessLevel= {1}, AUX_ONLY= {2}, HDR= {3}]".format(
                    workload_type_str, self.aggressiveness_level[adapter.gfx_index],
                    panel.hdr_caps.is_aux_only_brightness, self.hdr_status)
                logging.info(f"DPST restriction {restriction}")

                dpst_status = dpst.verify(adapter, panel, etl_file, skip_report_generate, self.xpst_feature,
                                          True, expect_sfsu_enable, is_psr_enabled_in_igcl)
                if dpst_status is None:
                    self.fail("FAILED to verify DPST feature")
                skip_report_generate = True
                if (power_src == workload.PowerSource.AC_MODE) or (method == dpst.WorkloadMethod.IDLE) or \
                        self.aggressiveness_level[adapter.gfx_index] == 1 or \
                        (panel.hdr_caps.is_aux_only_brightness and self.xpst_feature == dpst.XpstFeature.DPST) or \
                        self.hdr_status :
                    # DPST should not give IE histogram in (AC+NonCS) or IDLE condition or AUX based brightness
                    if dpst_status:
                        logging.error("\t\tFAIL: {0} is working on {1}(PIPE_{2})= NOT EXPECTED".format(
                            self.xpst_feature_str, panel.port, panel.pipe))
                        gdhm_title = "[PowerCons][DPST] DPST is working on {0}(PIPE_{1}) with {2}".format(
                            panel.port, panel.pipe, restriction)
                        gdhm.report_bug(
                            title=gdhm_title,
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        status = False
                    else:
                        logging.info("\t\tPASS: {0} is NOT working on {1}(PIPE_{2})= EXPECTED".format(
                            self.xpst_feature_str, panel.port, panel.pipe))
                else:
                    # DPST should give IE histogram
                    if dpst_status:
                        logging.info("\tPASS: {0} is working on {1}(PIPE_{2})= EXPECTED".format(
                            self.xpst_feature_str, panel.port, panel.pipe))
                    else:
                        logging.error("\t\tFAIL: {0} is NOT working on {1}(PIPE_{2})= NOT EXPECTED".format(
                            self.xpst_feature_str, panel.port, panel.pipe))
                        gdhm_title = "[PowerCons][{3}] {3} is NOT working on {0}(PIPE_{1}) with {2})".format(
                            panel.port, panel.pipe, restriction, self.xpst_feature_str)
                        gdhm.report_driver_bug_pc(gdhm_title)
                        status = False

                    if expect_epsm_enable is not None:
                        logging.info("STEP: Verifying EPSM on {0}-{1}".format(adapter.name, panel.port))
                        epsm_status = dpst.verify_epsm(etl_file)
                        actual_epsm = "Enabled" if epsm_status else "Disabled"
                        expected_epsm = "Enabled" if expect_epsm_enable else "Disabled"
                        restriction = "Method= App"
                        if epsm_status == expect_epsm_enable:
                            logging.info("\tPASS: EPSM= {0}, Expected= {0}".format(actual_epsm))
                        else:
                            logging.error("\tFAIL: EPSM= {0}, Expected= {1}".format(actual_epsm, expected_epsm))
                            gdhm_title = "[PowerCons][DPST] EPSM is {0} in driver [Expected= {1},{2}]".format(
                                actual_epsm, expected_epsm, restriction)
                            gdhm.report_driver_bug_pc(gdhm_title)
                            status = False

                feature_status = True
                if concurrent_feature != dpst.Feature.NONE:
                    concurrent_feature_name = dpst.Feature(concurrent_feature).name
                    logging.info(f"Verifying {concurrent_feature_name} for "
                                 f"{panel.port}(PIPE_{panel.pipe}) on {adapter.gfx_index}")
                    if concurrent_feature == dpst.Feature.FBC:
                        feature_status &= fbc.verify_adapter_fbc(adapter.gfx_index)
                    elif concurrent_feature == dpst.Feature.LACE:
                        feature_status &= pc_external.get_lace_status(adapter, panel)
                    elif concurrent_feature == dpst.Feature._3DLUT:
                        feature_status &= pc_external.verify_3dlut(adapter, panel)[0]
                    elif concurrent_feature == dpst.Feature.VDSC:
                        feature_status &= dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port)
                    elif concurrent_feature == dpst.Feature.PIPE_SCALAR:
                        feature_status &= VerifyScalarProgramming([DisplayScalar(panel.port, "MAR")])

                    status &= feature_status
                    logging_str = f"{concurrent_feature_name} verification for {panel.port}(PIPE_{panel.pipe})"
                    if feature_status is False:
                        logging.error(f"FAIL: {logging_str}")
                    else:
                        logging.info(f"PASS: {logging_str}")

        return status
