########################################################################################################################
# @file         gen9_voltage_swing.py
# @brief        Voltage swings configurations and tests for Gen 9 Platform
# @author       Girish Y D
########################################################################################################################
from Libs.Core import display_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.voltage_swing import voltage_swing
from Libs.Feature.voltage_swing import voltage_swing_helper
from Tests.Hdmi.mode.hdmi_mode_base import *


##
# @brief        GEN9VoltageSwing Class
class GEN9VoltageSwing(HdmiModeBase):
    reset_vbt = False

    ##
    # @brief        setUp() will inherit the instances from the setUp() of HdmiModeBase
    # @return       None
    def setUp(self):

        super(GEN9VoltageSwing, self).setUp()
        ##
        # Check only 1 display panel input  is received in cmd line
        self.assertEqual(len(self.display_list), 1, "None or more than 1 display panel input received")

        # Unplug all the external displays connected apart from eDP/MIPI
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(enumerated_displays.to_string())
        for idx in range(enumerated_displays.Count):
            disp_config = enumerated_displays.ConnectedDisplays[idx]
            if disp_config.ConnectorNPortType not in [enum.DP_A, enum.MIPI_A, enum.MIPI_C]:
                display_port = CONNECTOR_PORT_TYPE(disp_config.ConnectorNPortType)
                display_port = str(display_port)
                result = display_utility.unplug(display_port)
                self.assertTrue(result, "Failed to unplug simulated %s display" % display_port)
                if self.plugged_displays is not None and display_port in self.plugged_displays:
                    self.plugged_displays.remove(display_port)
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(self.enumerated_displays.to_string())

    ##
    # @brief        Test run
    # @return       None
    def runTest(self):
        self.run_status = True
        ##
        # Plug display
        display_panel = self.display_list[0]
        display_port = display_panel['connector_port']
        edid_file = display_panel['edid_name']
        result = display_utility.plug(display_port, edid_file)
        self.assertTrue(result, "Failed to plug simulated display panel to %s" % display_port)
        time.sleep(5)

        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(self.enumerated_displays.to_string())
        result = display_config.is_display_attached(self.enumerated_displays, display_port)
        self.assertTrue(result, "%s Display is not attached" % display_port)
        logging.info("PASS : Plugged display to %s" % display_port)
        self.plugged_displays.append(display_port)

        ##
        # Set Single display Display config With display passed
        result = self.display_config.set_display_configuration_ex(enum.SINGLE, [display_port], self.enumerated_displays)
        self.assertTrue(result, "Failed to perform SD config for %s " % display_port)
        logging.debug(self.enumerated_displays.to_string())
        logging.info("PASS : Switch to config - SD %s" % display_port)
        time.sleep(5)

        ##
        # Verify voltage swing programming from 0 to max level or index by setting the voltage swing values in VBT
        vs_test_parameters_obj = voltage_swing.VoltageSwingTestParameters(display_port=display_port)
        max_level_shifter_level_or_index = voltage_swing_helper.get_hdmi_max_level_shifter_configuration_level(
            self.platform)
        iboost_enabled = 1
        iboost_magnitude_index = 0
        for level in range(0, max_level_shifter_level_or_index + 1):
            iboost_magnitude = voltage_swing_helper.iboost_magnitude_array[iboost_magnitude_index]
            logging.info("***%s Validate voltage swing for level : %s; iboost_enabled : %s; iboost_magnitude: %s ***"
                         % (display_port, level, iboost_enabled, iboost_magnitude))
            set_vbt_iboost_status = voltage_swing_helper.set_iboost_details(self.platform, display_port, level,
                                                                            iboost_enabled,
                                                                            iboost_magnitude)
            self.assertTrue(set_vbt_iboost_status,
                            "Failed to set VBT for %s with iboostdetails-iboost_enabled:%s, iboost_magnitude:%s" % (
                                display_port, iboost_enabled, iboost_magnitude))
            self.reset_vbt = True
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail('FAIL - Restarting display driver failed after setting VBT')

            self.run_status &= voltage_swing.verify_voltage_swing(vs_test_parameters_obj)

            iboost_magnitude_index += 1
            if iboost_magnitude_index == 3:
                iboost_magnitude_index = 0

        if self.run_status is False:
            self.fail("FAIL : GEN9VoltageSwing ")

    ##
    # @brief        Cleans up the test
    # @return       None
    def tearDown(self):

        if self.reset_vbt is True:
            reset_vbt__status = voltage_swing_helper.reset_vbt_and_restart_driver()
            self.assertTrue(reset_vbt__status, "Failed to reset VBT")

        ##
        # Unplug the displays which are plugged
        if self.plugged_displays is not None:
            for i in range(len(self.plugged_displays)):
                display_port = self.plugged_displays.pop()
                result = display_utility.unplug(display_port)
                self.assertTrue(result, "Failed to unplug simulated %s display" % display_port)

        super(GEN9VoltageSwing, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
