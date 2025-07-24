########################################################################################################################
# @file         fms_reboot.py
# @brief        This file contains tests for FMS verification after reboot
# @author       Kruti Vadhavaniya
########################################################################################################################

import os
import shutil

from Libs.Core import display_utility, enum, display_essential
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.test_env import test_environment
from Libs.Feature.mipi.mipi_helper import MipiHelper
from Tests.LFP_Common.FMS import fms
from Tests.LFP_Common.FMS.fms_base import *


##
# @brief        This class contains tests for FMS verification after reboot
class LfpFmsReboot(unittest.TestCase):
    machine_info = SystemInfo()
    config = display_config.DisplayConfiguration()

    cmd_line_param = None
    edp_panels = []
    edp_target_ids = {}
    port_list = []

    ##
    # @brief        This class method is the entry point for FMS reboot test cases.
    #               It does the initializations and setup required for LFP FMS reboot test execution.
    # @details      This function gets the platform info, parses command line arguments for display list and custom tags
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        self.display_list = cmd_parser.get_sorted_display_list(self.cmd_line_param)
        self.edp_panels = [panel for panel in self.display_list if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                           display_utility.VbtPanelType.LFP_DP]
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        self.platform = None
        logging.info("Starting Test Setup")

        ##
        # check platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        if self.display_list.__contains__("MIPI_A") or self.display_list.__contains__("MIPI_C"):

            ##
            # Stop the ETL tracer started during TestEnvironment initialization
            etl_tracer.stop_etl_tracer()

            # Initialize MIPI verifier. This will contain helper functions
            self.mipi_helper = MipiHelper(self.platform)

            if self.mipi_helper.dual_LFP_MIPI:
                ##
                # apply ED MIPI LFP1 + MIPI LFP2, in case of dual LFP MIPI
                result = self.config.set_display_configuration_ex(enum.EXTENDED,
                                                                  ["MIPI_A", "MIPI_C"],
                                                                  self.enumerated_displays)
                self.assertNotEquals(result, False,
                                     "Aborting the test as applying ED MIPI LFP1 + MIPI LFP2 config failed.")
            else:
                ##
                # apply SD MIPI configuration, in case single LFP MIPI
                result = self.config.set_display_configuration_ex(enum.SINGLE, ["MIPI_A"],
                                                                  self.enumerated_displays)
                self.assertNotEquals(result, False, "Aborting the test as applying SD MIPI display config failed.")
        else:
            ##
            # Checking that all the eDPs passed in command line are connected and getting target ids for the same
            for edp_panel in self.edp_panels:
                logging.info("Verifying test requirements for {0}".format(edp_panel))
                if display_config.is_display_attached(self.enumerated_displays, edp_panel) is False:
                    assert False, "{0}(eDP) NOT connected. Please run the prepare_display to plug eDP".format(
                        edp_panel)
                logging.info("\tPASS: Connection status Expected= Connected, Actual= Connected")
                target_id = self.config.get_target_id(edp_panel, self.enumerated_displays)
                if target_id == 0:
                    assert False, "Target ID for {0}(eDP) is 0 (Test Issue)".format(edp_panel)
                self.edp_target_ids[edp_panel] = target_id

            ##
            # In case of dual eDP, apply the dual edp config passed from commandline
            if len(self.edp_panels) > 1:
                logging.info("Setting display config {0} {1}".format(self.cmd_line_param['CONFIG'],
                                                                     ' '.join(self.edp_panels)))
                result = self.config.set_display_configuration_ex(
                    eval("enum.%s" % self.cmd_line_param['CONFIG']),
                    self.edp_panels, self.enumerated_displays)
                if result is False:
                    assert False, "Set config FAILED = {0} {1} (Test Issue)".format(
                        self.cmd_line_param['CONFIG'], ' '.join(self.edp_panels))
                logging.info("\tPASS: Successfully applied display configuration")
                common.print_current_topology("\t")

            logging.info("Test Setup Completed")

    ##
    # @brief        This method is the exit point for LFP FMS reboot tests.
    #               This also checks for TDR and reports and logs if found
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Starting Test Cleanup")

        ##
        # Unplug the displays and restore the configuration to the initial configuration.
        for display in self.plugged_display:
            logging.info("Trying to unplug {0}".format(display))
            flag = display_utility.unplug(display)
            self.assertNotEquals(self.enumerated_displays, None, "Aborting the test as enumerated_displays is None")

            result = display_config.is_display_attached(self.enumerated_displays, display)
            self.assertNotEquals(result, True, "Aborting the test as unplugging the display failed.")

            if len(self.edp_panels) is not 0:
                if not common.IS_DDRW:
                    fms.disable()

            ##
            # Check TDR.
            result = display_essential.detect_system_tdr(gfx_index='gfx_0')
            self.assertNotEquals(result, True, "Aborting the test as TDR happened while executing the test")

        logging.info("Test Cleanup Completed")

    ##
    # @brief        This function verifies LFP FMS after reboot
    # @return       None
    def runTest(self):
        if reboot_helper.is_reboot_scenario() is True:
            logging.info("\tResumed from the power event POWER_STATE_S5 successfully")

            if etl_tracer.stop_etl_tracer() is False:
                self.fail("Failed to stop Boot ETL Tracer")

            # Make sure boot etl file is present
            new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, "GfxBootTrace_fms.etl")
            if os.path.exists(etl_tracer.GFX_BOOT_TRACE_ETL_FILE):
                shutil.move(etl_tracer.GFX_BOOT_TRACE_ETL_FILE, new_boot_etl_file)
            else:
                self.fail("GfxBootTrace.etl not found")

            ##
            # Verify FastModeSet
            logging.info("Step: Verifying FMS")

            for display in self.display_list:
                port = "DSI0" if display.__contains__("MIPI_A") else display.split("_")[-1]
                for target_id in self.edp_target_ids:
                    result = fms.verify_fms_during_power_events(new_boot_etl_file, port, self.platform, target_id)
                    if result is False:
                        self.fail("FAIL: Display is not active")
                    if result != "FAST_MODE_SET":
                        gdhm.report_driver_bug_di(f"{fms.GDHM_FMS} ModeSet Expected= FAST_MODE_SET, Actual= {result}")
                        self.fail(f"FAIL: ModeSet Expected= FAST_MODE_SET, Actual= {result}")
                    logging.info("PASS: ModeSet Expected= FAST_MODE_SET, Actual= FAST_MODE_SET")
            return

        ##
        # Start Boot ETL Tracer
        if etl_tracer.start_etl_tracer(tracing_options=etl_tracer.TraceType.TRACE_WITH_BOOT) is False:
            self.fail("Failed to start Boot ETL Tracer(Test Issue)")

        ##
        # Invoke S5 power event
        logging.info("Step: Triggering power event POWER_STATE_S5 for {0} seconds".format(
            common.POWER_EVENT_DURATION_DEFAULT))
        if reboot_helper.reboot(self, callee="runTest") is False:
            self.fail("Failed to reboot the system(Test Issue)")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('LfpFmsReboot'))
    test_environment.TestEnvironment.cleanup(outcome)
