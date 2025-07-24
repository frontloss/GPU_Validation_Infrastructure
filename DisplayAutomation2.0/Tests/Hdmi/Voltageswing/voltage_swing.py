########################################################################################################################
# @file         voltage_swing.py
# @brief        Voltage swings configurations and tests for Multiple Platforms
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
# @brief        VoltageSwing Function
class VoltageSwing(HdmiModeBase):
    reset_vbt = False

    ##
    # @brief        setUp() will inherit the instances from the setUp() of HdmiModeBase
    # @return       None
    def setUp(self):

        super(VoltageSwing, self).setUp()
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
        time.sleep(10)

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
        time.sleep(10)

        if self.platform.upper() == 'GLK' and display_port == "HDMI_B":
            ##
            # Verify PASSIVE LEVEL SHIFTER FOR GEMINILAKE for PORT B
            # In Geminilake -Port B  passive level shifter values will programming based on Pixel clock

            # Get the display Target ID
            display_target_id = self.display_config.get_target_id(display_port, self.enumerated_displays)

            # Get Supported /Enumerated Modes by driver for the display
            supported_mode_list = self.display_config.get_all_supported_modes([display_target_id], False)
            self.assertIsNotNone(supported_mode_list, "Modes query failed for %s " % display_port)
            driver_mode_list = supported_mode_list[display_target_id]
            verified_voltage_swing = 0
            for driver_mode in driver_mode_list:
                if ((driver_mode.HzRes == 3840 and driver_mode.VtRes == 2160 and driver_mode.scaling == enum.MDS
                     and driver_mode.refreshRate == 30 and driver_mode.scanlineOrdering == enum.PROGRESSIVE)
                        or (driver_mode.HzRes == 1920 and driver_mode.VtRes == 1080 and driver_mode.scaling == enum.MDS
                            and driver_mode.refreshRate == 60 and driver_mode.scanlineOrdering == enum.PROGRESSIVE)):
                    set_mode_status = self.display_config.set_display_mode([driver_mode])
                    if set_mode_status is False:
                        logging.error("Failed to apply display mode :%s. Exiting ..." % driver_mode.to_string(
                            self.enumerated_displays))
                        self.fail()
                    vs_test_parameters_obj = voltage_swing.VoltageSwingTestParameters(display_port=display_port,
                                                                                      is_active_level_shifter=False)
                    self.run_status &= voltage_swing.verify_voltage_swing(vs_test_parameters_obj)
                    verified_voltage_swing += 1
            if verified_voltage_swing != 2:
                logging.error(
                    "FAIL: Test Case didn't verified voltage swing for both 3840x2160 and 1920x1080 modes, Please check log")
                self.fail()
        else:
            ##
            # Verify voltage swing programming from 0 to max level or index by setting the voltage swing values in VBT
            vs_test_parameters_obj = voltage_swing.VoltageSwingTestParameters(display_port=display_port)
            max_level_shifter_level_or_index = voltage_swing_helper.get_hdmi_max_level_shifter_configuration_level(
                self.platform)
            for level in range(0, max_level_shifter_level_or_index + 1):
                logging.info(
                    "***********%s Validate voltage swing for level : %s ** **********" % (display_port, level))
                set_vbt_status = voltage_swing_helper.set_vbt_hdmi_level_shifter_configuration(self.platform,
                                                                                               display_port, level)
                self.assertTrue(set_vbt_status,
                                "Failed to set VBT with level_shifter config with Level/index=%s" % level)
                self.reset_vbt = True
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail('FAIL - Restarting display driver failed after setting VBT')
                self.run_status &= voltage_swing.verify_voltage_swing(vs_test_parameters_obj)

        if self.run_status is False:
            self.fail("FAIL : Verify VoltageSwing ")

    ##
    # @brief        Tear Down function
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

        super(VoltageSwing, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
