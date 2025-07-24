########################################################################################################################
# @file         writeback_mode_config_scenarios.py
# @brief        The test scenario tests the following functionalities.
#                * Verify whether the devices are correctly plugged and enumerated.
#                * Verify whether all the configurations can be applied or not.
#                * Verify whether all the possible modes are applied or not
# @author       Patel, Ankurkumar G
########################################################################################################################
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Writeback.writeback_base import *

##
# @brief    Contains unitest runTest function to verify whether all possible configurations and modes are applied or not
class WritebackModeConfig(WritebackBase):
    plugged_display_list = []

    ##
    # @brief        unittest runTest function
    # @param[in]    self; Object of writeback base class
    # @return       void
    def test_run(self):

        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_and_verify_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        # for debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Set all valid configurations
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            self.plugged_display_list.append(str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)))
            logging.debug("Plugged display = %s" % self.plugged_display_list[display_count])

        logging.info("Step2 - Apply all possible configs")
        self.assertEquals(self.apply_possible_configs(self.plugged_display_list), True,
                          "Aborting the test as Apply config failed")
        logging.info("\tPASS: All Configurations applied successfully")

        # Set extended configuration
        self.apply_config_on_all_devices(enum.EXTENDED)
        time.sleep(5)

        # Set all possible Modes
        logging.info("Step3 - Set all possible modes")
        self.assertEquals(self.set_possible_modes(), True, "Aborting the test as set mode failed")
        logging.info("\tPASS: Modeset applied successfully")

        # Apply SD Writeback 
        logging.info("Step4 - Apply SD writeback device")
        enumerated_display = self.disp_config.get_enumerated_display_info()
        if self.disp_config.set_display_configuration_ex(enum.SINGLE, ["WD_0"], enumerated_display) is False:
            self.fail('Failed to apply display configuration %s %s' % (
                DisplayConfigTopology(enum.SINGLE).name, ["WD_0"]))
        logging.info('/tPASS: Successfully applied the display configuration as %s %s' % (
            DisplayConfigTopology(enum.SINGLE).name, ["WD_0"]))
        time.sleep(10)

        # Disable/Enable driver 
        logging.info("Step5 - Disable/Enable driver in SD writeback config")
        status, reboot_required = display_essential.restart_gfx_driver()
        if status:
            logging.info("Successfully restarted driver.")
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


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('WritebackModeConfig'))
    TestEnvironment.cleanup(outcome)
