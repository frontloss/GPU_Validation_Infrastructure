##
# @file gfx_display_switch_disable_enable.py
# @brief The script verifies whether the Windod graphics driver is working properly or not by executing the following steps in sequence:
#       * Setup- Enable WinDod using regkey "WinDod" and disable enable driver
#       * Apply all possible display config combination and verify it
#       * Disable/enable graphics driver
#       * Verifies whether the graphics driver is running and active post disable/enable driver
# @author Doriwala, Nainesh P

import unittest
import logging
import sys
import itertools
from enum import Enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import system_utility, enum, registry_access, display_essential
from Libs.Core import reboot_helper, cmd_parser, display_utility
from Libs.Core.machine_info.machine_info import SystemInfo, SystemDriverType
from Libs.Core.logger import gdhm
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_context import TestContext


##
# @brief DiAna return error code
class WinDodEnableDisable(Enum):
    Disable = 0
    Enable = 1


##
# @brief It contains the methods to verify whether the Dod graphic is working properly or not
class GfxDodDriverDisplaySwDisableEnable(unittest.TestCase):
    connected_list = []
    config = DisplayConfiguration()
    obj_machine_info = SystemInfo()
    sys_util = system_utility.SystemUtility()
    plugged_display = []
    enumerated_displays = []

    ##
    # @brief Setup - Set all require registry for test.
    # @return - None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("************** TEST START **************")

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

    ##
    # @brief test_start - Verify and Update windod regkey, reboot if request by OS.
    # @return - None
    def test_setup(self):
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        logging.debug("Setup - Check for Windod Regkey value and status")
        status, reboot_required = self.enable_disable_windod_regkey(enable_disable=int(WinDodEnableDisable.Enable.value))
        if status:
            logging.info("Windod regkey updated and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_run') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief RunTest - DisplaySwitch with different possible config and disable/enable driver
    # @return - None
    def test_run(self):
        disp_list = []
        config_list = []

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as graphics driver is not enabled")
        logging.info("PASS: Graphics driver is active")

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            gdhm.report_bug(
                title="[DOD]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        ##
        #
        for disp in range(len(self.connected_list)):
            disp_list.append(self.connected_list[disp])
        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(1, len(disp_list) + 1):
            for subset in itertools.permutations(disp_list, i):
                config_list.append((topology_list[0], [subset[0]]))
                if len(subset) >= 2:
                    config_list.append((topology_list[1], list(subset)))
                    config_list.append((topology_list[2], list(subset)))

        ##
        # applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            logging.info("each_config{}".format(each_config))
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:
                logging.info("Applied display configuration: %s" % self.get_display_configuration(
                        config_list[each_config][1]))
            else:
                logging.info("Failed to apply display configuration %s %s" % (
                    DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]))

        # Disable driver
        logging.info("Step-Driver Disable: Disable the driver")
        self.assertEqual(display_essential.disable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as driver disable failed")
        # Verify driver is Disabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), False,
                         "Aborting the test as driver is not disabled")
        logging.info("PASS: Driver disable successful")

        # Enable driver
        logging.info("Step-Driver Enable: Enable the driver")
        self.assertEqual(display_essential.enable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as driver enable failed")
        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as driver is not enabled")
        logging.info("PASS: Driver enable successful")

    ##
    # @brief test_unplug_regkey_reset  - Unplug display and clear Windod regkey and reboot if request by OS
    # @return - None
    def test_unplug_regkey_reset(self):
        logging.info("unplugging display and disabling Windod")
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)

        logging.debug("Cleanup - Reset Windod Regkey value to 0")
        status, reboot_required = self.enable_disable_windod_regkey(
            enable_disable=int(WinDodEnableDisable.Disable.value))
        if status:
            logging.info("Windod regkey updated and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_cleanup') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief test_cleanup  - Dummy function to call post reboot of system requested by OS.
    # @return - None
    def test_cleanup(self):
        logging.info("****************TEST ENDS HERE********************************")

    ##
    # @brief Function to Enable or Disable Windod regkey
    # @param[in] self
    # @param[in] enable_disable - 1- Enable, 0-Disable
    # @return - bool - status True if able to update regkey else False
    #           Bool - reboot_required  True if reboot require else False
    def enable_disable_windod_regkey(self, enable_disable):
        yangra_subkey = r"igfxn\Parameters"
        legacy_subkey = r"igfx\Parameters"

        sub_key = yangra_subkey if self.sys_util.is_ddrw() is True else legacy_subkey
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SYSTEM\CurrentControlSet\Services")

        dod_reg_val, dod_reg_type = registry_access.read(args=reg_args, reg_name="WinDod", sub_key=sub_key)

        if dod_reg_val is None or dod_reg_val != enable_disable:
            reg_write = registry_access.write(reg_args, "WinDoD", registry_access.RegDataType.DWORD, enable_disable,
                                              sub_key)
            if not reg_write:
                logging.error("Fail to update WinDod regkey")
                status = False
                reboot_required = False
            else:
                status, reboot_required = display_essential.restart_gfx_driver()
        else:
            logging.debug("Updating registry value not require, Restart gfx driver skipped")
            status = True
            reboot_required = False
        return status, reboot_required

    ##
    # @brief Function to get Display configuration into string
    # @param[in] self
    # @param[in] connected_port_list - list of connected port
    # @return port_config string
    def get_display_configuration(self, connected_port_list):
        port_config_str = ""
        for each_port in connected_port_list:
            target_id = self.config.get_target_id(each_port, self.enumerated_displays)
            mode = self.config.get_current_mode(target_id)
            port_config_str = port_config_str + "\n" + mode.to_string(self.enumerated_displays)
        return port_config_str

    ##
    # @brief Function to verify driver is enabled or disabled
    # @param[in] self
    # @param[in] gfx_index - graphics adapter index like 'gfx_0'
    # @return Boolean - True - Driver enable , False- Driver disable
    def is_driver_running(self, gfx_index):
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        drivers_info = self.obj_machine_info.get_driver_info(SystemDriverType.GFX)
        for driver in range(drivers_info.Count):
            if drivers_info.DriverInfo[driver].DeviceID == adapter_info.deviceID:
                logging.debug("Device ID:{}".format(drivers_info.DriverInfo[driver].DeviceID))
                if drivers_info.DriverInfo[driver].Status != "Running":
                    logging.info("GFX driver is not running for Device ID: {}"
                                 .format(drivers_info.DriverInfo[driver].DeviceID))
                    return False
                logging.info("GFX driver is running for Device ID: {}"
                             .format(drivers_info.DriverInfo[driver].DeviceID))
        return True

    ##
    # @brief Function to TearDown  and clean WinDod regkey which enable in setup
    # @param[in] self
    # @return - None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).\
        run(reboot_helper.get_test_suite('GfxDodDriverDisplaySwDisableEnable'))
    TestEnvironment.cleanup(outcome)
