##
# @file gfx_driver_uninstall.py
# @brief The script verifies whether the graphics driver un-installation and re-installation is working properly or not
# @details * Step1: Uninstall existing graphics driver and reboot system
#          * Step2: Install the primary graphics driver and reboot system
#          * Step3: Verifies whether the primary graphics driver is installed and enable.
#          *        Verify primary driver version and check for under-run
#          *        Uninstall Primary driver and reboot the system.
#          * Step4: Verify Driver is uninstall or not and reboot system
#          * Step5: Install primary graphics driver and reboot system
#          * Step6: Verifies whether the primary graphics driver is installed and enable.Verify primary driver version
# @author Patel, Ankurkumar G, Chandrashekhar, SomashekarX, Doriwala, Nainesh P


from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Install_Uninstall2.install_uninstall2_base import *


##
# @brief it contain method to verify graphics driver installation and un-installation are working properly or not
class GfxDriverUninstall(InstallUninstall2Base):

    ##
    # @brief step 1 - Verifies whether the primary graphics driver is installed and enable.
    #                 Verify primary driver version and check for underrun
    #                 Uninstall Primary driver and reboot the system.
    # @return None
    def test_1_Step(self):
        logging.debug("Entry: test_1_step()")

        # Verify driver is Enabled or not
        self.assertEquals(self.is_driver_running(gfx_index='gfx_0'), True,
                          "Aborting the test as graphics driver is not enabled")
        logging.info("PASS: Graphics driver is active")

        # Verify and plug the display
        self.plugged_display = self.plug_require_display()
        self.enumerated_display = self.config.get_enumerated_display_info()

        self.assertNotEqual(self.enumerated_display, None, "Aborting the test as enumerated_displays are None.")
        # disp_list[] is a list of displays derived from command-line,
        # plugged_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.is_teardown_required = True
            self.fail("Required displays are not enumerated")

        self.assertNotEqual(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")
        display_adapter_info_list = []
        for item in self.input_display_list:
            logging.info("0: {}, 1: {}".format(item[0], item[1]))
            display_adapter_info_list.append(self.config.get_display_and_adapter_info_ex(item[0], item[1]))
        self.assertEqual(self.config.set_display_configuration_ex(self.config_type, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No underrun observed till driver uninstall")

        ##
        # Uninstall Driver and reboot the system
        logging.info("Step-Uninstall: Uninstall primary driver")
        self.assertEquals(self.uninstall_graphics_driver(gfx_index='gfx_0'), True,
                          "Aborting the test as primary graphics driver uninstallation is unsuccessful")
        logging.info("PASS: Graphics driver uninstalled, Rebooting system")
        logging.debug("Exit: test_1_Step()")
        if reboot_helper.reboot(self, 'test_2_Step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 2 - Verify Driver is uninstall or not and reboot system
    # @return None
    def test_2_Step(self):
        logging.debug("Entry: test_2_step()")
        self.assertEquals(self.is_driver_installed(gfx_index='gfx_0'), False,
                          "Aborting the test as graphics driver is not uninstalled")
        logging.info("PASS: No graphics driver available after un-installation")
        logging.debug("Exit: test_2_step()")
        if reboot_helper.reboot(self, 'test_3_Step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 3 - Install primary graphics driver and reboot system
    # @return None
    def test_3_Step(self):
        logging.debug("Entry: test_3_step()")
        logging.info("Step-CleanUp: Install primary driver after test completion")
        self.assertEquals(
            self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH, driver_type=self.driver_type),
            True,
            "Aborting the test as primary graphics driver installation is unsuccessful")
        logging.info("PASS: Primary graphics driver installed again. Rebooting system")
        logging.debug("Exit: test_3_step()")
        if reboot_helper.reboot(self, 'test_4_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 4 - Verifies whether the primary graphics driver is installed and enable.
    #                 Verify primary driver version
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

        self.is_teardown_required = True

        logging.debug("Exit: test_4_step()")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('GfxDriverUninstall'))
    TestEnvironment.cleanup(outcome)
