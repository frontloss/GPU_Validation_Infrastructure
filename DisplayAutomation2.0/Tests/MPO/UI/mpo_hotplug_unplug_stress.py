########################################################################################################################
# @file         mpo_hotplug_unplug_stress.py
# @brief        Basic test to verify mpo getting enabled with no corruption with 3D apps during hotplug/unplug.
#               * Plug the displays.
#               * Apply CLONE and EXTENDED configuration across the displays connected.
#               * Play the 3D app in Metro Mode.
#               * Unplug the displays.
#               * WM verification after display Unplug.
#               * Plug the displays and WM verification after display Plug.
#               * Close the 3D app.
#               * Unplug the displays.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, window_helper, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.hw_emu.hotplug_emulator_utility import HotPlugEmulatorUtility
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_helper

##
# @brief    Contains function to check mpo getting enabled with no corruption with 3D apps during hotplug/unplug
class MPOHotPlugUnplugStress(unittest.TestCase):
    connector_port_list = []
    hotplug_emulator_utility = HotPlugEmulatorUtility()
    wm = DisplayWatermark()
    stepCounter = 0
    mpo_helper = mpo_ui_helper.MPOUIHelper()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************TEST STARTS HERE*******************")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connector_port_list.insert(value['index'], value['connector_port'])

        if len(self.connector_port_list) <= 0:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("Minimum 1 display is required to run the test")

        self.under_run_status = UnderRunStatus()
        self.under_run_status.clear_underrun_registry()
        self.stepCounter = 0

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        config = DisplayConfiguration()

        ##
        # Plug the displays
        logging.info(self.mpo_helper.getStepInfo() + "Plugging in displays: %s" % self.connector_port_list[1:])
        for i in range(1, len(self.connector_port_list)):
            if self.hotplug_emulator_utility.hot_plug(self.connector_port_list[i], 0):
                logging.info("Plug successful on display %s" % self.connector_port_list[i])
            else:
                logging.error("Plug for display %s failed" % self.connector_port_list[i])

        time.sleep(5)

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.CLONE, enum.EXTENDED]

        ##
        # applying each configuration across the displays connected
        for each_config in range(len(topology_list)):
            if config.set_display_configuration_ex(topology_list[each_config], self.connector_port_list) is True:
                logging.info("Applied display configuration as  %s for %s" % (
                    DisplayConfigTopology(topology_list[each_config]).name, self.connector_port_list))
                ##
                # Play the 3Dapp in Metro Mode
                self.mpo_helper.play_maps(True)
                time.sleep(2)

                for i in range(15):
                    logging.info(self.mpo_helper.getStepInfo() + "Hot unplugging on ports: %s" % self.connector_port_list[1:])
                    ##
                    # Unplug the displays connected
                    for i in range(1, len(self.connector_port_list)):
                        if self.hotplug_emulator_utility.hot_unplug(self.connector_port_list[i], 0):
                            logging.info("Unplug Successful on port %s" % self.connector_port_list[i])
                        else:
                            logging.error("Unplug failed on port  %s" % self.connector_port_list[i])

                    time.sleep(10)

                    ##
                    # WM verification after display Unplug
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                    if self.wm.verify_watermarks() is not True:
                        self.fail("Error Observed in watermark verification")
                    else:
                        logging.info("Watermark verification passed")

                    ##
                    # Plug the displays
                    logging.info(self.mpo_helper.getStepInfo() + "Hot plugging on ports: %s" % self.connector_port_list[1:])
                    for i in range(1, len(self.connector_port_list)):
                        if self.hotplug_emulator_utility.hot_plug(self.connector_port_list[i], 0):
                            logging.info("Plug Successful on port %s" % self.connector_port_list[i])
                        else:
                            logging.error("Plug failed on port %s" % self.connector_port_list[i])

                    time.sleep(10)

                    ##
                    # WM verification after display Plug
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                    if self.wm.verify_watermarks() is not True:
                        self.fail("Error Observed in watermark verification")
                    else:
                        logging.info("Watermark verification passed")

                time.sleep(5)

                ##
                # Close the 3Dapp
                window_helper.kill_process_by_name("Maps.exe")
                logging.info(self.mpo_helper.getStepInfo() + "Closed Maps application")

            else:
                self.fail("Failed to apply display configuration as %s for %s" % (
                    DisplayConfigTopology(topology_list[each_config]).name, self.connector_port_list))

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test Clean Up")
        if self.under_run_status.verify_underrun() is True:
            logging.error("Underrun seen in the test")

        ##
        # Unplug the displays connected
        logging.info("Unplugging all plugged external displays: %s" % self.connector_port_list[1:])
        for i in range(1, len(self.connector_port_list)):
            if self.hotplug_emulator_utility.hot_unplug(self.connector_port_list[i], 0):
                logging.info("Unplug successful on port %s" % self.connector_port_list[i])
            else:
                logging.error("Unplug failed on port  %s" % self.connector_port_list[i])
        logging.info("************TEST ENDS HERE*******************")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Verifies enabling of MPO when 3D App is running with hotplug and unplug of displays")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
