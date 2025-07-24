#################################################################################################################
# @file         lrr_reg_keys.py
# @brief        Contains LRR Reg Keys tests
#
# @author       Rohit Kumar
#################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential, reboot_helper
from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import LrrVersion, Method
from Tests.PowerCons.Functional.LRR.lrr_base import VIDEO_FILE_MAPPING
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload, common, dut
from Tests.PowerCons.Modules.dut_context import RrSwitchingMethod
from Tests.PowerCons.Modules.workload import PowerSource


##
# @brief        This class contains LRR Reg key tests
class LrrRegKeysTest(unittest.TestCase):
    feature = LrrVersion.LRR1_0
    video_file = VIDEO_FILE_MAPPING['24']
    is_feature_override = False
    method = Method.IDLE
    duration_in_seconds = 30
    polling_delay_in_seconds = 0.01

    ##
    # @brief        This class method is the entry point for LRR Reg Key test cases. Helps to initialize the
    #               parameters required test execution.
    # @details      This function checks for feature support and initializes parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    # @cond
    @reboot_helper.__(reboot_helper.setup)
    # @endcond
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(self.cmd_line_param, list):
            self.cmd_line_param = [self.cmd_line_param]

        if self.cmd_line_param[0]['FEATURE'] != 'NONE':
            if self.cmd_line_param[0]['FEATURE'][0] == 'LRR1':
                self.feature = LrrVersion.LRR1_0
                self.rr_switching_method = RrSwitchingMethod.CLOCK
            elif self.cmd_line_param[0]['FEATURE'][0] == 'LRR2':
                self.feature = LrrVersion.LRR2_0
                self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
            elif self.cmd_line_param[0]['FEATURE'][0] == 'LRR2.5':
                self.feature = LrrVersion.LRR2_5
                if common.PLATFORM_NAME in common.PRE_GEN_14_PLATFORMS:
                    self.rr_switching_method = RrSwitchingMethod.VTOTAL_SW
                else:
                    self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
            elif self.cmd_line_param[0]['FEATURE'][0] == 'NO_LRR':
                self.feature = LrrVersion.NO_LRR
                self.rr_switching_method = RrSwitchingMethod.UNSUPPORTED

            if len(self.cmd_line_param[0]['FEATURE']) > 1:
                if self.cmd_line_param[0]['FEATURE'][1] == 'OVERRIDE':
                    self.is_feature_override = True

        if self.cmd_line_param[0]['METHOD'] != 'NONE':
            if self.cmd_line_param[0]['METHOD'][0] == "IDLE":
                self.method = Method.IDLE
            elif self.cmd_line_param[0]['METHOD'][0] == "VIDEO":
                self.method = Method.VIDEO

        dut.prepare(power_source=PowerSource.DC_MODE)

    ##
    # @brief        This method is the exit point for LRR reg key test cases. This resets the environment changes done
    #               for execution of tests
    # @return       None
    # @cond
    @reboot_helper.__(reboot_helper.teardown)
    # @endcond
    def tearDown(self):
        for gfx_index, adapter in dut.adapters.items():
            if adapter.name in dut.PRE_GEN_12_PLATFORMS:
                continue

            lrr.reset_lrr_caps_override(adapter)

        dut.reset()

    ##
    # @brief        This function tests LRR with registry settings before reboot
    # @return       None
    def test_before_reboot(self):
        for adapter in dut.adapters.values():
            logging.info(f"Step: Enabling {self.feature.name} on {adapter.name}")
            lrr_status = lrr.enable(adapter)
            if lrr_status is False:
                self.fail(f"FAILED to enable LRR{self.feature} via reg_key on {adapter.name}")
            if lrr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"Successfully to restart display driver for {adapter.name}")

        # Skip registry override if not requested from commandline.
        if self.is_feature_override is False:
            return

        # Override LRR version from registry key
        for gfx_index, adapter in dut.adapters.items():
            if adapter.is_yangra is False:
                continue
            for port, panel in adapter.panels.items():
                if lrr.override_lrr_caps(adapter, panel, self.feature) is False:
                    self.fail("FAILED to create LRRVersionCapsOverride registry")

        reboot_helper.reboot(self, 'test_after_reboot')

    ##
    # @brief        This function tests LRR with registry settings after reboot
    # @return       None
    def test_after_reboot(self):
        dut.prepare()

        html.step_start(f"Verifying adapter and panel requirements for LRR")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"{panel}")
                logging.info(f"\t{panel.psr_caps}")
                logging.info(f"\t{panel.drrs_caps}")
                logging.info(f"\t{panel.lrr_caps}")
                logging.info(f"\t{panel.vrr_caps}")
                if self.feature == LrrVersion.NO_LRR and panel.lrr_caps.is_lrr_supported:
                    logging.info("LRR override is with NO_LRR, falling back to legacy path")
                    self.feature = LrrVersion.LRR1_0 if panel.lrr_caps.is_lrr_1_0_supported else LrrVersion.LRR2_0
                    if panel.lrr_caps.is_lrr_1_0_supported:
                        self.rr_switching_method = RrSwitchingMethod.CLOCK
                    elif panel.lrr_caps.is_lrr_2_0_supported:
                        self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                    elif panel.lrr_caps.is_lrr_2_5_supported:
                        if common.PLATFORM_NAME in common.PRE_GEN_14_PLATFORMS:
                            self.rr_switching_method = RrSwitchingMethod.VTOTAL_SW
                        else:
                            self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
        html.step_end()

        status = True

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.method == Method.IDLE:
                    etl_file, polling_data = workload.run(
                        workload.IDLE_DESKTOP,
                        [self.duration_in_seconds],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                else:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )

                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR verification with override registry settings")
        logging.info("PASS: LRR verification with override registry settings")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    output = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('LrrRegKeysTest'))
    test_environment.TestEnvironment.cleanup(output)
