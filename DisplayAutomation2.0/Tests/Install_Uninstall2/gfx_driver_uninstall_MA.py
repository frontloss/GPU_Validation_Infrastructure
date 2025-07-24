#
# @file gfx_driver_uninstall_MA.py
# @brief The script verifies whether the graphics driver un-installation and re-installation is working properly or not
# @details * Step1: Verifies whether the integrated and discrete graphics drivers are installed and enable.
#          *        Verify driver version and check for under-run for both adapter
#          *        Uninstall integrated driver and reboot the system.
#          * Step2: Verify integrated Driver is uninstalled or not and discrete driver is installed.
#          *        check for under-run for both adapter and Uninstall discrete driver and reboot the system.
#          * Step3: Verify integrated Driver is uninstalled or not and discrete driver is un-installed or not.
#          *        check for under-run for both adapter and install discrete driver
#          *        install integrated driver and reboot the system.
#          * Step4: Verifies whether the integrated and discrete graphics drivers are installed and Running.
#          *        Plug display and apply config. Verify driver version and check for under-run for both adapter
#          *        Uninstall discrete driver and reboot the system.
#          * Step5: Verify discrete Driver is uninstalled or not and integrated driver is installed.
#          *        check for under-run for both adapter and Uninstall integrated driver and reboot the system.
#          * Step6: Verify integrated Driver is uninstalled or not and discrete driver is uninstalled or not.
#          *        check for under-run for both adapter and install Integrate driver
#          *        install Discrete driver and reboot the system.
#          * Step7: Verifies whether the integrated and discrete graphics drivers are installed and enable.
#          *        Verify driver version for both adapter
# @author Doriwala, Nainesh P


from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Install_Uninstall2.install_uninstall2_base import *


##
# @brief it contain method to verify graphics driver installation and un-installation are working properly or not for
#        for both adapter.
class GfxDriverUninstallMA(InstallUninstall2Base):

    ##
    # @brief Step1: Verifies whether the integrated and discrete graphics drivers are installed and enable.
    #               Verify driver version and check for under-run for both adapter
    #               Uninstall integrated driver and reboot the system.
    # @return None
    def test_1_Step(self):
        logging.debug("Entry: test_1_step()")
        # Verify driver is Enabled or not for integrated and Discrete graphics drivers.
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not enabled")
        logging.info("PASS: Integrated Graphics driver is active")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete graphics driver is not enabled")
        logging.info("PASS: Discrete Graphics driver is active")

        # verify integrated and discrete drivers should uninstall
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not installed")
        logging.info("PASS: Integrated graphics driver available after installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver is not installed")
        logging.info("PASS: Discrete and integrated graphics driver available after installation")

        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(
            dvr_path=DRIVER_PATH, driver_type='UWD_DCH_I', gfx_index='gfx_0'), True,
            "Aborting the test as graphics driver version check unsuccessful")
        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(
            dvr_path=DRIVER_PATH, driver_type='UWD_DCH_D', gfx_index='gfx_1'), True,
            "Aborting the test as graphics driver version check unsuccessful")

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
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed till applied display config")

        ##
        # Uninstall Integrated graphics Driver and reboot the system
        logging.info("Step-Uninstall: Uninstall Integrated graphics Driver")
        self.assertEqual(self.uninstall_graphics_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver un-installation is unsuccessful")
        logging.info("PASS: Integrated Graphics driver uninstalled Successful, Rebooting system")
        if reboot_helper.reboot(self, 'test_2_Step') is False:
            self.fail("Failed to reboot the system")
        logging.debug("Exit: test_1_Step()")

    ##
    # @brief Step2: Verify integrated Driver is uninstalled or not and discrete driver is installed.
    #               Check for under-run for both adapter and Uninstall discrete driver and reboot the system.
    # @return None
    def test_2_Step(self):
        logging.debug("Entry: test_2_step()")
        # verify integrated driver should uninstall and discrete drive should install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated graphics driver is not uninstalled")
        logging.info("PASS: Integrated graphics driver not available after un-installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver is not installed")
        logging.info("PASS: Discrete graphics driver available after un installation of integrated graphics driver")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed post integrated driver uninstall")

        ##
        # Uninstall Discrete graphics Driver and reboot the system
        logging.info("Step-Uninstall: Uninstall Discrete graphics Driver")
        self.assertEqual(self.uninstall_graphics_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver un-installation is unsuccessful")
        logging.info("PASS: Discrete Graphics driver uninstalled Successful, Rebooting system")
        if reboot_helper.reboot(self, 'test_3_Step') is False:
            self.fail("Failed to reboot the system")
        logging.debug("Exit: test_2_Step()")

    ##
    # @brief Step3: Verify integrated Driver is uninstalled or not and discrete driver is un-installed or not.
    #                Check for under-run for both adapter and install discrete driver
    #                Install integrated driver and reboot the system.
    # @return None
    def test_3_Step(self):
        logging.debug("Entry: test_3_step()")

        # verify integrated and discrete drivers should uninstall
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated graphics driver is not uninstalled")
        logging.info("PASS: Integrated graphics driver not available after un-installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), False,
                         "Aborting the test as discrete graphics driver is not uninstalled")
        logging.info("PASS: Discrete and integrated graphics driver unavailable after un-installation")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed post integrated driver uninstall")

        logging.info("Step-Install: Install Discrete graphics driver on dGPU")
        self.assertEqual(self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH,
                                                                             driver_type='UWD_DCH_D'),
                         True, "Aborting the test as discrete graphics driver installation is unsuccessful")
        logging.info("PASS: Discrete graphics driver installed")

        logging.info("Step-Install: Install integrated graphics driver on iGPU")
        self.assertEqual(self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH,
                                                                             driver_type='UWD_DCH_I'),
                         True, "Aborting the test as integrated graphics driver installation is unsuccessful")
        logging.info("PASS: integrated graphics driver installed, Rebooting system")

        if reboot_helper.reboot(self, 'test_4_Step') is False:
            self.fail("Failed to reboot the system")

        logging.debug("Exit: test_3_step()")

    ##
    # @brief Step4: Verifies whether the integrated and discrete graphics drivers are installed and Running.
    #               Plug display and apply config. Verify driver version and check for under-run for both adapter
    #               Uninstall discrete driver and reboot the system.
    # @return None
    def test_4_Step(self):
        logging.debug("Entry: test_4_step()")
        # Verify driver is Enabled or not for integrated and Discrete graphics drivers.
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not enabled")
        logging.info("PASS: Integrated Graphics driver is active")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete graphics driver is not enabled")
        logging.info("PASS: Discrete Graphics driver is active")

        # verify integrated and discrete drivers should uninstall
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not installed")
        logging.info("PASS: Integrated graphics driver available after installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver is not installed")
        logging.info("PASS: Discrete and integrated graphics driver available after installation")

        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(dvr_path=DRIVER_PATH, driver_type='UWD_DCH_I',
                                                   gfx_index='gfx_0'), True,
                         "Aborting the test as graphics driver version check unsuccessful")
        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(dvr_path=DRIVER_PATH, driver_type='UWD_DCH_D',
                                                   gfx_index='gfx_1'), True,
                         "Aborting the test as graphics driver version check unsuccessful")

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
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed till applied display config")

        ##
        # Uninstall Discrete graphics Driver and reboot the system
        logging.info("Step-Uninstall: Uninstall Discrete graphics Driver")
        self.assertEqual(self.uninstall_graphics_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver un-installation is unsuccessful")
        logging.info("PASS: Discrete Graphics driver uninstalled Successful, Rebooting system")
        if reboot_helper.reboot(self, 'test_5_Step') is False:
            self.fail("Failed to reboot the system")
        logging.debug("Exit: test_4_Step()")

    ##
    # brief Step5: Verify discrete Driver is uninstalled or not and integrated driver is installed.
    #              Check for under-run for both adapter and Uninstall integrated driver and reboot the system.
    # @return None
    def test_5_Step(self):
        logging.debug("Entry: test_5_step()")
        # verify integrated driver should uninstall and discrete drive should install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not installed")
        logging.info("PASS: Integrated graphics driver available after un-installation of discrete driver")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), False,
                         "Aborting the test as discrete graphics driver is not uninstalled")
        logging.info("PASS: Discrete graphics driver is not available after un-installation ")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed post integrated driver uninstall")

        ##
        # Uninstall Integrated graphics Driver and reboot the system
        logging.info("Step-Uninstall: Uninstall Integrated graphics Driver")
        self.assertEqual(self.uninstall_graphics_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not un-installated")
        logging.info("PASS: Integrated Graphics driver uninstalled Successful, Rebooting system")
        if reboot_helper.reboot(self, 'test_6_Step') is False:
            self.fail("Failed to reboot the system")
        logging.debug("Exit: test_5_Step()")

    ##
    # @brief Step6: Verify integrated Driver is uninstalled or not and discrete driver is uninstalled or not.
    #               Check for under-run for both adapter and install Integrate driver
    #               Install Discrete driver and reboot the system.
    # @return None
    def test_6_Step(self):
        logging.debug("Entry: test_6_step()")

        # verify integrated and discrete drivers should uninstall
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated graphics driver is not uninstalled")
        logging.info("PASS: Integrated graphics driver not available after un-installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), False,
                         "Aborting the test as discrete graphics driver is not uninstalled")
        logging.info("PASS: Discrete and integrated graphics driver unavailable after un-installation")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            self.is_teardown_required = True
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed post integrated driver uninstall")

        logging.info("Step-Install: Install integrated graphics driver on iGPU")
        self.assertEqual(self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH,
                                                                             driver_type='UWD_DCH_I'),
                         True, "Aborting the test as integrated graphics driver installation is unsuccessful")
        logging.info("PASS: integrated graphics driver installed")

        logging.info("Step-Install: Install Discrete graphics driver on dGPU")
        self.assertEqual(self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH,
                                                                             driver_type='UWD_DCH_D'),
                         True, "Aborting the test as discrete graphics driver installation is unsuccessful")
        logging.info("PASS: Discrete graphics driver installed, Rebooting system")

        if reboot_helper.reboot(self, 'test_7_Step') is False:
            self.fail("Failed to reboot the system")

        logging.debug("Exit: test_6_step()")

    ##
    # @brief Step7: Verifies whether the integrated and discrete graphics drivers are installed and enable.
    #               Verify driver version for both adapter
    # @return None
    def test_7_Step(self):
        logging.debug("Entry: test_7_step()")
        # Verify driver is Enabled or not for integrated and Discrete graphics drivers.
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not enabled")
        logging.info("PASS: Integrated Graphics driver is active")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete graphics driver is not enabled")
        logging.info("PASS: Discrete Graphics driver is active")

        # verify integrated and discrete drivers should uninstall
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not installed")
        logging.info("PASS: Integrated graphics driver available after installation")
        # verify discrete graphics driver install
        self.assertEqual(self.is_driver_installed(gfx_index='gfx_1'), True,
                         "Aborting the test as discrete graphics driver is not installed")
        logging.info("PASS: Discrete and integrated graphics driver available after installation")

        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(dvr_path=DRIVER_PATH, driver_type='UWD_DCH_I',
                                                   gfx_index='gfx_0'), True,
                         "Aborting the test as graphics driver version check unsuccessful")
        # Check installed driver version for integrated and discrete graphics drivers.
        self.assertEqual(self.check_driver_version(dvr_path=DRIVER_PATH, driver_type='UWD_DCH_D',
                                                   gfx_index='gfx_1'), True,
                         "Aborting the test as graphics driver version check unsuccessful")

        self.is_teardown_required = True

        logging.debug("Exit: test_7_Step()")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.runner.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('GfxDriverUninstallMA'))
    TestEnvironment.cleanup(outcome)
