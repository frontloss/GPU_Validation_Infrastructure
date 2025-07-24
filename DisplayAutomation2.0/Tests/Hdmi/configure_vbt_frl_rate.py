#
# @file configure_vbt_frl_rate.py.py
# @brief The script performs configuration of FRL Rate in VBT based on input parameter:
#       * Setup- Parse input command line parameter.
# @details Command line to configure FRL Rate in VBT
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE DEFAULT  - To Set platform default
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_12   - To Configure 12Gbps FRL Rate
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_10   - To Configure 10Gbps FRL Rate
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_8    - To Configure 8Gbps FRL Rate
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_6    - To Configure 6Gbps FRL Rate
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_3    - To Configure 3Gbps FRL Rate
#       * .\Tests\Hdmi\configure_vbt_frl_rate.py -FRL_RATE FRL_NOT_SUPPORTED  - To Configure TMDS
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

FRL_RATES = ["DEFAULT", "FRL_12", "FRL_10", "FRL_8", "FRL_6", "FRL_3", "FRL_NOT_SUPPORTED"]

frl_rate_mapping = dict([
    (0, "FRL_NOT_SUPPORTED"),
    (1, "FRL_3"),
    (2, "FRL_6"),
    (3, "FRL_8"),
    (4, "FRL_10"),
    (5, "FRL_12"),
])


##
# @brief It contains the methods to Configure FRL Rate in VBT.
class ConfigureHDMIFrlRate(unittest.TestCase):
    connected_list = []
    custom_tags = ['-FRL_RATE']
    frl_rate_passed = None
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
            if key == 'FRL_RATE':
                if value:
                    self.frl_rate_passed = str(value[0]).upper()

        if self.frl_rate_passed not in FRL_RATES:
            self.fail("Invalid argument pass.")

        enumerated_display = display_config.get_enumerated_display_info()
        if enumerated_display.Count != 1:
            self.fail("Expect only one display to be connected.")

        self.display_port = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[0].ConnectorNPortType))

        if "HDMI" not in self.display_port:
            self.fail("Expect HDMI to be connected.")


    ##
    # @brief test_setup - Verify and Configure FRL Rate in VBT and reboot system if request by OS.
    # @return - None
    def test_setup(self):
        logging.info("Setup - Check for FRL Rate in VBT and Update")

        current_value = self.get_hdmi_2_1_frl_rate_in_vbt(self.display_port)
        if current_value == self.frl_rate_passed:
            logging.info(
                "FRL Request request{} and current value{} are same".format(self.frl_rate_passed, current_value))
        else:
            self.set_hdmi_2_1_frl_rate_in_vbt(self.display_port, self.frl_rate_passed)  # Pass portname
            status, reboot_required = display_essential.restart_gfx_driver()

            if status:
                logging.info("VBT updated for Configuring FRL successfully with restarted driver.")
            elif status is False and reboot_required is True:
                if reboot_helper.reboot(self, 'test_run') is False:
                    self.fail("Failed to reboot the system")
            else:
                self.fail("Failed to restart display driver")

    ##
    # @brief RunTest - Get Current FRL Rate value and verify with requested
    # @return - None
    def test_run(self):
        # Verify
        current_status = self.get_hdmi_2_1_frl_rate_in_vbt(self.display_port)
        if current_status == self.frl_rate_passed:
            logging.info("Request FRL Rate applied{}".format(current_status))
        else:
            logging.error("Request FRL Rate not applied current{}, request{}".
                          format(current_status, self.frl_rate_passed))
            self.fail("FRL Rate not changed.")

    ##
    # @brief         Method to get HDMI2.1 FRL rate in VBT
    # @param         display_port - Port Name
    # @return        status - True if VBT change is successful, else False
    def get_hdmi_2_1_frl_rate_in_vbt(self, display_port):
        gfx_vbt = Vbt()
        current_frl = "DEFAULT"
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        is_frl_valid = display_entry.IsMaxFrlRateFieldValid
        if is_frl_valid == 1:
            current_frl = frl_rate_mapping[display_entry.MaximumFrlRate]
            logging.debug(f"Current FRL Rate in VBT: {current_frl}")

        return current_frl

        ##
        # @brief         Method to set HDMI2.1 FRL rate in VBT
        # @param         display_port - Port Name
        # @param         frl_to_set - FRL given in the command line
        # @return        status - True if VBT change is successful, else False

    def set_hdmi_2_1_frl_rate_in_vbt(self, display_port, frl_to_set):
        gfx_vbt = Vbt()
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        current_frl = self.get_hdmi_2_1_frl_rate_in_vbt(display_port)
        logging.info(f"Current FRL Rate in VBT: FRL_{current_frl}")
        logging.info(f"User defined FRL Rate to be set in VBT: {frl_to_set}")

        display_entry.IsMaxFrlRateFieldValid = 0
        if frl_to_set != "DEFAULT":
            # Set HDMI2.1 FRL to Valid and set FRL which is passed in command line
            display_entry.IsMaxFrlRateFieldValid = 1
            display_entry.MaximumFrlRate = vbt_context.MAX_FRL_RATE_MAPPING[frl_to_set]

        # Apply VBT Changes
        gfx_vbt.apply_changes()

        return True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2). \
        run(reboot_helper.get_test_suite('ConfigureHDMIFrlRate'))
    TestEnvironment.cleanup(outcome)
