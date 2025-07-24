########################################################################################################################
# @file         c10_with_cs.py
# @brief        Contains PnP tests for connected standby
# @details      PnP tests are covering cs scenario putting system to CS
#
# @author       Bhargav Adigarla
########################################################################################################################

import logging
import sys
import unittest
import os
import json

from Libs.Core import cmd_parser, driver_escape, display_power, enum
from Libs.Core.gta import gta_state_manager
from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment, test_context
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.PnP.tools import socwatch, powermeter

# Below numbers collected from last 15 driver runs on same machine
# These numbers will change in future based on BKC installation upgrade
GOLDEN_NUMBERS = {
    'ICLLP': {'C10': 0},
    'TGL':   {'C10': 0},
    'ADLP':  {'C10': 0}
}


##
# @brief        This class contains tests covering cs scenario PnP tests with Connected Standby. This class inherits
#               unittest.Testcase and implements setUpClass and TeardownClass functions which initialise and
#               cleanup the setup required for verification of PnP in Connected standby scenario.
class PnpRunner(unittest.TestCase):
    tool = socwatch
    duration = 120  # seconds

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This function is the entry point for the PnP with Connected Standby Tests. It initialises some of
    #               the parameters required for the execution of the PnP tests in CS scenario. It parses the
    #               command line params and prepares the display setup
    # @return       None
    @classmethod
    def setUpClass(cls):
        cmd_line_args = cmd_parser.parse_cmdline(sys.argv, common.CUSTOM_TAGS)

        if cmd_line_args['DURATION'] != 'NONE':
            cls.duration = int(cmd_line_args['DURATION'][0])

        dut.prepare(power_source=display_power.PowerSource.DC)

    ##
    # @brief        This function is the exit point for the PnP with Connected Standby Tests. It resets the setup done
    #               done for the execution of PnP test cases with Connected Standby scenario
    # @return       None
    @classmethod
    def tearDown(cls):
        dut.reset()

    ##
    # @brief        This function verifies the PnP with connected standby
    # @return       None
    def runTest(self):

        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system(Planning Issue)")

        adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
        # Set power component to Idle for all adapters before invoking power events
        for gfx_index in adapter_info_dict.keys():
            status = driver_escape.configure_adapter_power_component(gfx_index, False)
            if status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(f"{'PASS' if status is True else 'FAIL'}: Configuring 'Idle' status for {gfx_index} adapter")

        gta_state_manager.configure_tc(launch=False)  # Kill ThinClient during powerevent. Can kill TC if already killed

        powermeter.run_pm(self.duration-5)
        socwatch_output = socwatch.run_soc_watch_with_cs(self.duration)

        c10_score = socwatch.get_metric(socwatch_output, 'PACKAGE_C10')
        good_report = powermeter.get_pm_log()

        # Set power component to Active for all adapters after resuming
        for gfx_index in adapter_info_dict.keys():
            status = driver_escape.configure_adapter_power_component(gfx_index, True)
            if status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(f"{'PASS' if status is True else 'FAIL'}: Configuring 'Active' status for {gfx_index} adapter")

        pnp_data = {
            "C10": c10_score,
        }
        json_obj = json.dumps(pnp_data, indent=4)
        with open("dashboard_data.txt", "w") as outfile:
            outfile.write(json_obj)
        outfile.close()

        pnp_log_file_path = os.path.join(os.getcwd(), "dashboard_data.txt")

        report_path = os.path.join(test_context.LOG_FOLDER, "dashboard_data.txt")
        if os.path.exists(pnp_log_file_path) is False:
            logging.error("{0} not found".format(pnp_log_file_path))

        os.rename(pnp_log_file_path, report_path)

        if c10_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']:
            logging.info("System entering to C10 with CS: {0}".format(c10_score))
        else:
            self.fail("System not entering to C10 with CS: {0}".format(c10_score))

        if common.PLATFORM_NAME in ['TGL', 'ICLLP']:
            good_pnp_data = {
                "BACKLIGHT": good_report[' BACKLIGHT Power (W)'],
                "VCC_IN_AUX": good_report[' VDD2_CPU Power (W)'],
                "VDD2_CPU": good_report[' VDD2_MEM Power (W)'],
                "VDD2_MEM": good_report[' VCCIN_AUX Power (W)']
            }
        else:
            good_pnp_data = {
                "VBATA_VCCCORE_IN": good_report[' VBATA_VCCCORE_IN Power (W)'],
                "VBATA_VCCGT_IN": good_report[' VBATA_VCCGT_IN Power (W)'],
                "VCC1P8_CPU": good_report[' VCC1P8_CPU Power (W)'],
                "VCC1P05_CPU": good_report[' VCC1P05_CPU Power (W)'],
                "VBATA_VCCIN_AUX_IN": good_report[' VBATA_VCCIN_AUX_IN Power (W)'],
                "VDD2_CPU": good_report[' VDD2_CPU Power (W)'],
                "VDD2_MEM": good_report[' VDD2_MEM Power (W)'],
                "V1P8U_MEM": good_report[' V1P8U_MEM Power (W)']
            }

        with open(os.path.join(test_context.LOG_FOLDER, "dashboard2_data.txt"), "w") as outfile:
            outfile.write(json.dumps(good_pnp_data, indent=4))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
