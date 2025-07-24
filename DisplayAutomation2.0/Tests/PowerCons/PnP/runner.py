########################################################################################################################
# @file         runner.py
# @brief        Runner script for PnP tests
#
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import sys
import time
import unittest
import logging

from Libs.Core import app_controls, cmd_parser, display_power, enum
from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.PnP.features import cfps, dc6, dc6v, dmrrs, dpst, drrs, fbc, hdr, \
    hrr, lace, lrr1, lrr2_5, port_sync, psr1, psr2, vrr
from Tests.PowerCons.PnP.tools import socwatch, powermeter
from Tests.PowerCons.Modules import workload as wl
from Tests.Color import color_common_utility

FEATURES = [cfps, dc6, dc6v, dmrrs, dpst, drrs, fbc, hdr, hrr, lace, lrr1, lrr2_5, port_sync, psr1, psr2, vrr]


##
# @brief        This class contains tests for verifying Pnp
class PnpRunner(unittest.TestCase):
    workload = "IDLE"  # idle / video
    duration = 120  # seconds

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This function is the entry point for the PnP tests in this class. It initialises some of
    #               the parameters required for the execution of the PnP test. It parses the command line
    #               params and prepares the display setup
    # @return       None
    @classmethod
    def setUpClass(cls):
        cmd_line_args = cmd_parser.parse_cmdline(sys.argv, common.CUSTOM_TAGS)

        if cmd_line_args['FEATURE'] != 'NONE':
            cls.feature = eval("{0}".format(cmd_line_args['FEATURE'][0].replace(".", "_").lower()))

        if cmd_line_args['WORKLOAD'] != 'NONE':
            cls.workload = cmd_line_args['WORKLOAD'][0]

        if cmd_line_args['DURATION'] != 'NONE':
            cls.duration = int(cmd_line_args['DURATION'][0])

        dut.prepare(power_source=display_power.PowerSource.DC)

    ##
    # @brief        This function is the exit point for the PnP tests in this class. It resets the setup created for
    #               executing tests of this class.
    # @return       None
    @classmethod
    def tearDown(cls):
        dut.reset()

    ##
    # @brief        This function verifies the enabling, disabling and analysis of PnP features
    # @return       None
    def runTest(self):
        status = True
        self.feature.enable(dut.adapters['gfx_0'])
        self.run_tools()
        self.run_workload()

        time.sleep(20)

        enabled_soc_op = socwatch.get_socwatch_log()
        enabled_pm_op = powermeter.get_pm_log()

        self.feature.disable(dut.adapters['gfx_0'])

        self.run_tools()
        self.run_workload()

        time.sleep(20)

        disabled_soc_op = socwatch.get_socwatch_log()
        disabled_pm_op = powermeter.get_pm_log()

        self.feature.enable(dut.adapters['gfx_0'])

        if self.feature.analyze(self.workload, enabled_soc_op, disabled_soc_op) is False:
            status = False
            logging.error("{0} SW PnP verification failed with {1} workload".format(self.feature.name, self.workload))

        if self.feature.analyze_hw(enabled_pm_op, disabled_pm_op) is False:
            status = False
            logging.error("{0} HW PnP verification failed with {1} workload".format(self.feature.name, self.workload))

        if status is False:
            self.fail(logging.error("{0} PnP verification failed with {1} workload".format(self.feature.name, self.workload)))

    def run_tools(self):
        socwatch.run_socwatch(self.duration)
        time.sleep(5)
        powermeter.run_pm(self.duration-5)

    def run_workload(self):
        if self.workload == 'IDLE':
            wl.run(wl.IDLE_DESKTOP, [self.duration])
        elif self.workload == 'VIDEO':
            wl.run(wl.VIDEO_PLAYBACK, [24, self.duration])
        elif self.workload == "SCREEN_UPDATE":
            monitors = app_controls.get_enumerated_display_monitors()
            monitor_ids = [_[0] for _ in monitors]
            etl_file, _ = wl.run(wl.SCREEN_UPDATE, [monitor_ids])
        elif self.workload == "HDR_VIDEO":
            color_common_utility.video_play_back(is_full_screen=True)
        elif self.workload == "GAME":
            etl_file, _ = wl.run(wl.GAME_PLAYBACK, [wl.Apps.AngryBotsGame, self.duration, True])


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
