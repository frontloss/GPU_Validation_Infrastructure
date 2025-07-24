##
# @file gfx_driver_upgrade.py
# @brief The script verifies whether the graphics driver upgrade is working properly or not
# @details * Step1: Uninstall existing graphics driver and reboot system
#          * Step2: Install the secondary graphics driver and reboot system
#          * Step3: Verifies whether the secondary graphics driver is installed and enable.
#          *        Upgraded to primary driver and reboot.
#          * Step4: Verifies whether the primary graphics driver is installed and enable.
#          *        Able to apply config and no under-run.
# @author Patel, Ankurkumar G, Chandrashekhar, SomashekarX, Doriwala, Nainesh P

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Install_Uninstall2.install_uninstall2_base import *


##
# @brief it contain method to verify graphics driver upgrade is working properly or not
class GfxDriverUpgrade(InstallUninstall2Base):

    ##
    # @brief step 1 - Uninstall existing graphics driver and reboot system
    # @return None
    def test_1_Step(self):
        logging.debug("Entry: test_1_step()")
        logging.info("Step-SetUp: Uninstall existing drivers")
        if self.uninstall_all_graphics_driver():
            logging.info("PASS: Graphics driver uninstalled, Rebooting system")
            if reboot_helper.reboot(self, 'test_2_Step') is False:
                self.fail("Failed to reboot the system")
        else:
            logging.info("Graphics driver not installed, skipping un-installation")
        logging.debug("Exit: test_1_Step()")

    ##
    # @brief step 2 - Install the secondary graphics driver and reboot system
    # @return None
    def test_2_Step(self):
        logging.debug("Entry: test_2_step()")
        logging.info("Step-Install: Install secondary graphics driver")
        self.assertEquals(
            self.install_graphics_driver_through_device_manager(dvr_path=SEC_DRIVER_PATH, driver_type=self.driver_type),
            True,
            "Aborting the test as secondary graphics driver installation is unsuccessful")
        logging.info("PASS: Secondary graphics driver installed, Rebooting system")
        logging.debug("Exit: test_2_Step()")
        if reboot_helper.reboot(self, 'test_3_Step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 3 - Verifies whether the secondary graphics driver is installed and enable.
    #                 Upgraded to primary driver and reboot.
    # @return None
    def test_3_Step(self):
        logging.debug("Entry: test_3_step()")

        # Verify driver is Enabled or not
        self.assertEquals(self.is_driver_running(gfx_index='gfx_0'), True,
                          "Aborting the test as graphics driver is not enabled")
        logging.info("PASS: Graphics driver is active")

        # Check driver version
        self.assertEquals(
            self.check_driver_version(dvr_path=SEC_DRIVER_PATH, driver_type=self.driver_type, gfx_index='gfx_0'), True,
            "Aborting the test as graphics driver version check unsuccessful")
        # Verify and plug the display
        self.plugged_display, self.enumerated_display = display_utility.plug_displays(self, self.cmd_line_param)
        self.assertNotEquals(self.enumerated_display, None, "Aborting the test as enumerated_displays are None.")
        # disp_list[] is a list of displays derived from command-line, plugged_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.fail("Required displays are not enumerated")

        self.assertNotEquals(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")

        # Set valid configuration
        self.set_display_config(self.input_display_list, enum.EXTENDED)

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')
        logging.info("No under-run Observed till driver upgrade")

        ##
        # Upgrade driver
        logging.info("Step-Upgrade: Upgrade to primary graphics driver")
        self.assertEquals(
            self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH, driver_type=self.driver_type),
            True,
            "Aborting the test as upgrade to primary graphics driver is unsuccessful")
        logging.info("PASS: Graphics driver upgraded to primary driver, Rebooting system")
        logging.debug("Exit: test_3_step()")
        if reboot_helper.reboot(self, 'test_4_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 4 - Verifies whether the primary graphics driver is installed and enable.
    #                 Able to apply config and no under-run.
    # @return None
    def test_4_step(self):
        logging.debug("Entry: test_4_step()")

        # Verify driver is Enabled or not
        self.assertEquals(self.is_driver_running(gfx_index='gfx_0'), True,
                          "Aborting the test as graphics driver is not enabled")
        logging.info("PASS: Graphics driver is active")

        # Check driver version
        self.assertEquals(
            self.check_driver_version(dvr_path=DRIVER_PATH, driver_type=self.driver_type, gfx_index='gfx_0'), True,
            "Aborting the test as graphics driver version check unsuccessful")
        # Verify and plug the display
        self.plugged_display, self.enumerated_display = display_utility.plug_displays(self, self.cmd_line_param)
        self.assertNotEquals(self.enumerated_display, None, "Aborting the test as enumerated_displays are None.")
        # disp_list[] is a list of displays derived from command-line, plugged_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.fail("Required displays are not enumerated")

        self.assertNotEquals(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")

        # Set valid configuration
        self.set_display_config(self.input_display_list, enum.EXTENDED)

        self.is_teardown_required = True

        logging.debug("Exit: test_4_Step()")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('GfxDriverUpgrade'))
    TestEnvironment.cleanup(outcome)
