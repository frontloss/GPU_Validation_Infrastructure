#
# @file configure_vbt_link_rate.py.py
# @brief The script performs configuration of Link Rate in VBT based on input parameter:
#       * Setup- Parse input command line parameter.
# @details Command line to configure Link Rate in VBT
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE DEFAULT  - To Set platform Max
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_1.62
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_2.7
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_5.4
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_8.1
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_10
#       * .\Tests\Display_Port\configure_vbt_link_rate.py -LINK_RATE LR_13.5
# @author Chandrakanth P

import logging
import sys
import unittest

from Libs.Core import display_essential
from Libs.Core import reboot_helper, cmd_parser
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt import vbt_context
from Libs.Core.vbt.vbt import Vbt

LINK_RATES = ["DEFAULT", "LR_1.62", "LR_2.7", "LR_5.4", "LR_8.1", "LR_10", "LR_13.5", "LR_20"]

vbt_to_link_rate_mapping = dict([
    (0, "DEFAULT"),
    (1, "LR_1.62"),
    (2, "LR_2.7"),
    (3, "LR_5.4"),
    (4, "LR_8.1"),
    (5, "LR_10"),
    (6, "LR_13.5"),
    (7, "LR_20"),
   ])

link_rate_to_vbt_mapping = dict([
    ("DEFAULT", 0),
    ("LR_1.62", 1),
    ("LR_2.7", 2),
    ("LR_5.4", 3),
    ("LR_8.1", 4),
    ("LR_10", 5),
    ("LR_13.5", 6),
    ("LR_20", 7),
   ])

##
# @brief It contains the methods to Configure Link Rate in VBT.
class ConfigureDPLinkRate(unittest.TestCase):
    connected_list = []
    custom_tags = ['-LINK_RATE']
    link_rate_passed = None
    display_port = None

    ##
    # @brief Setup - Parse command lines input parameter.
    # @return - None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("************** TEST START **************")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        display_config = DisplayConfiguration()
        for key, value in self.cmd_line_param.items():
            if key == 'LINK_RATE':
                if value:
                    self.link_rate_passed = str(value[0]).upper()

        if self.link_rate_passed not in LINK_RATES:
            self.fail("Invalid argument pass.")

        enumerated_display = display_config.get_enumerated_display_info()
        if enumerated_display.Count != 1:
            self.fail("Expect only one display to be connected.")

        self.display_port = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[0].ConnectorNPortType))

        if "DP" not in self.display_port:
            self.fail("Expect DP to be connected.")

    ##
    # @brief test_setup - Verify and Configure Link Rate in VBT and reboot system if request by OS.
    # @return - None
    def test_setup(self):
        logging.info("Setup - Check for Link Rate in VBT and Update")

        current_value = self.get_dp_link_rate_in_vbt(self.display_port)
        if current_value == self.link_rate_passed:
            logging.info(
                "Link Rate request{} and current value{} are same".format(self.link_rate_passed, current_value))
        else:
            self.set_dp_link_rate_in_vbt(self.display_port, self.link_rate_passed)
            status, reboot_required = display_essential.restart_gfx_driver()

            if status:
                logging.info("VBT updated for Configuring Link Rate successfully with restarted driver.")
            elif status is False and reboot_required is True:
                if reboot_helper.reboot(self, 'test_run') is False:
                    self.fail("Failed to reboot the system")
            else:
                self.fail("Failed to restart display driver")

    ##
    # @brief RunTest - Get Current Link Rate value and verify with requested
    # @return - None
    def test_run(self):
        # Verify
        current_status = self.get_dp_link_rate_in_vbt(self.display_port)
        if current_status == self.link_rate_passed:
            logging.info("Request Link Rate applied {}".format(current_status))
        else:
            logging.error("Request Link Rate not applied current {}, request {}".
                          format(current_status, self.link_rate_passed))
            self.fail("Link Rate not changed.")

    ##
    # @brief         Method to get DP Link rate in VBT
    # @param         display_port - Port Name
    # @return        status - True if VBT change is successful, else False
    def get_dp_link_rate_in_vbt(self, display_port):
        gfx_vbt = Vbt()
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        current_link_rate = vbt_to_link_rate_mapping[display_entry.DpMaxLinkRate]
        logging.info(f"Current Link Rate in VBT: {current_link_rate}")

        return current_link_rate

        ##
        # @brief         Method to set DP Link rate in VBT
        # @param         display_port - Port Name
        # @param         link_rate_to_set - Link Rate given in the command line
        # @return        status - True if VBT change is successful, else False
    def set_dp_link_rate_in_vbt(self, display_port, link_rate_to_set):
        gfx_vbt = Vbt()
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        current_link_rate = self.get_dp_link_rate_in_vbt(display_port)
        logging.info(f"Current Link Rate in VBT: {current_link_rate}")
        logging.info(f"User defined Link Rate to be set in VBT: {link_rate_to_set}")

        # Set DP Link Rate as per command line
        display_entry.DpMaxLinkRate = link_rate_to_vbt_mapping[link_rate_to_set]

        # Apply VBT Changes
        gfx_vbt.apply_changes()

        return True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2). \
        run(reboot_helper.get_test_suite('ConfigureDPLinkRate'))
    TestEnvironment.cleanup(outcome)
