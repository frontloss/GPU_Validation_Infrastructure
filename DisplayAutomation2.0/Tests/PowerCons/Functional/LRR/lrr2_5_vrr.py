########################################################################################################################
# @file         lrr2_5_vrr.py
# @brief        This file contains the LRR 2.5 concurrency test with VRR.
#               PSR2 should not be enabled during gaming.
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import LrrVersion
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr
from Tests.VRR.vrr_concurrency import TestConcurrency


##
# @brief        This class contains LRR 2_5 concurrency tests with Vrr
class LrrVrr(LrrBase):
    duration_in_seconds = 30  # minimum duration for game play

    ##
    # @brief        This class method is the entry point for any LRR concurrency test cases. Helps to initialize
    #               the parameters required for LRR test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(LrrVrr, cls).setUpClass()
        # Get App from command line
        if cls.cmd_line_param[0]['APP'] == 'NONE':
            # If App is not present in command line, set default apps for present OS
            cls.app = workload.Apps.Classic3DCubeApp
            if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_19H1:
                cls.app = workload.Apps.MovingRectangleApp
        else:
            if cls.cmd_line_param[0]['APP'][0] == 'RECTANGLE':
                cls.app = workload.Apps.MovingRectangleApp
            if cls.cmd_line_param[0]['APP'][0] == 'CUBE':
                cls.app = workload.Apps.Classic3DCubeApp
            if cls.cmd_line_param[0]['APP'][0] == 'ANGRYBOTS':
                cls.app = workload.Apps.AngryBotsGame
            if cls.cmd_line_param[0]['APP'][0] == 'FLIPAT':
                cls.app = workload.Apps.FlipAt
                # Get Game for FlipAt app
                if cls.cmd_line_param[0]['GAME'] != 'NONE':
                    cls.game = workload.FLIP_AT_GAME_ARGUMENT_MAPPING.get(cls.cmd_line_param[0]['GAME'][0], 1)
                # Get manual FPS pattern for FlipAt app
                if cls.cmd_line_param[0]['PATTERN'] != 'NONE':
                    cls.pattern = cls.cmd_line_param[0]['PATTERN']

        # Get game playback duration
        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration_in_seconds = int(cls.cmd_line_param[0]['DURATION'][0]) * 60  # convert into seconds

        # VRR tests need at least one VRR supported platform
        assert dut.is_feature_supported('VRR'), "None of the adapter supports VRR(Planning Issue)"

        # LRR2.5 feature is expected from command line
        assert cls.feature == LrrVersion.LRR2_5, "This test requires LRR2.5 feature to verify concurrency with VRR"

    ##
    # @brief        Test function to make sure VRR got enabled successfully
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_enable_vrr(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start(f"Enabling VRR with LOW & HIGH FPS solution for {adapter.name}")
            if vrr.enable(adapter, True, True) is False:
                self.fail("FAILED to enable VRR with LOW & HIGH FPS solution")
            logging.info("PASS: Successfully enabled VRR with LOW & HIGH FPS solution")
            html.step_end()

    ##
    # @brief        Test function to make sure that there is at least one adapter-panel combination which supports VRR
    #               and LRR 2.5. Failure of this test will stop the execution of the test.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_12_requirements(self):
        html.step_start("Verifying adapter and panel requirements for LRR2.5 and VRR concurrency")
        status = False
        for adapter in dut.adapters.values():
            # check if adapter supports VRR
            if not adapter.is_vrr_supported:
                logging.info(f"VRR is not supported on {adapter.gfx_index}")
                continue
            for panel in adapter.panels.values():
                logging.debug(f"Panel {panel.port} LRR caps : {panel.lrr_caps}")
                logging.debug(f"Panel {panel.port} VRR caps : {panel.vrr_caps}")
                if panel.lrr_caps.is_lrr_2_5_supported and panel.vrr_caps.is_vrr_supported:
                    status = True

        if not status:
            self.fail("There should be at least one adapter panel combination supporting LRR2.5 and VRR")
        html.step_end()

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test function test existence of VRR with LRR2_5
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_13_lrr2_5_vrr(self):
        # Run the game playback workload
        etl_file, _ = workload.run(workload.GAME_PLAYBACK, [self.app, self.duration_in_seconds, True])
        # VRR is expected to be enabled during game playback
        # PSR2 is not expected in active regions
        status = True
        for adapter in dut.adapters.values():
            if not adapter.is_vrr_supported:
                logging.info(f"VRR is not supported on {adapter.gfx_index}")
                continue

            for panel in adapter.panels.values():
                logging.info(f"Step: Verification of VRR and LRR2.5 for {panel.port} on {adapter.gfx_index}")
                if (not panel.lrr_caps.is_lrr_supported) or (not panel.vrr_caps.is_vrr_supported):
                    logging.info(f"Skipping Verification on {panel.port} as LRR2.5 and VRR do not co-exist on panel")
                    continue

                # verify VRR by passing ETL file
                vrr_status = vrr.verify(adapter, panel, etl_file)
                if not vrr_status:
                    logging.error(f"FAIL: VRR Verification for {panel.port} on {adapter.gfx_index}")
                    status &= False
                else:
                    logging.info(f"PASS: VRR Verification for {panel.port} on {adapter.gfx_index}")

                # Check PSR2 in active regions
                psr2_status = TestConcurrency.check_psr_status(adapter, panel, True)
                if not psr2_status:
                    logging.error(f"FAIL: PSR2 Verification for {panel.port} on {adapter.gfx_index}")
                    status &= False
                else:
                    logging.info(f"PASS: PSR2 Verification for {panel.port} on {adapter.gfx_index}")

                # Check if VTotal values are changing in VRR active regions
                vtotal_status = lrr.is_vtotal_changing(adapter, panel, etl_file)
                if not vtotal_status:
                    logging.error(f"FAIL: VTotal change observed for {panel.port} on {adapter.gfx_index}")
                    status &= False
                else:
                    logging.info(f"PASS: VTotal change not observed for {panel.port} on {adapter.gfx_index}")

        if not status:
            self.fail("FAIL: LRR2.5 concurrency test with VRR failed")
        logging.info("PASS: LRR2.5 concurrency test with VRR passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrVrr))
    test_environment.TestEnvironment.cleanup(test_result)
