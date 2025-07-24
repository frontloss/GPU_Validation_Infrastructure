##
# @file gfx_driver_install_disable_enable_MA.py
# @brief The script verifies whether the graphics driver disable enable is working properly or not in case of MA
# @details * Verifies whether the primary graphics driver is installed and enable.
#          * Verify primary driver version and check for under-run
#          * Disable Driver and check driver status as disable/not running
#          * Enable driver and check driver status as enable/Running
# @author Doriwala, Nainesh P
from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Install_Uninstall2.install_uninstall2_base import *


##
# @brief it contain method to verify graphics driver disable enable is working properly or not for both adapter.
class GfxDriverInstallDisableEnableMA(InstallUninstall2Base):

    ##
    # @brief runTest - Verifies whether the primary graphics driver is installed and enable.
    #           * Verify primary driver version and check for under-run
    #           * Disable Driver and check driver status as disable/not running
    #           * Enable driver and check driver status as enable/Running
    # @return None
    def runTest(self):
        logging.debug("Entry: Run-test start")

        # Verify driver is Enabled or not for integrated and Discrete graphics drivers.
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated graphics driver is not enabled")
        logging.info("PASS: Integrated Graphics driver is active")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete graphics driver is not enabled")
        logging.info("PASS: Discrete Graphics driver is active")

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
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed till applied display config")

        ##
        # @ Disable both graphics driver one by one
        logging.info("Step-Driver Disable: Disable both drivers")
        # Disable integrated Driver
        logging.info("Disabling integrated Graphics driver")
        self.assertEqual(display_essential.disable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver disable failed")

        # Verify integrated graphics driver is Disabled or not and Discrete graphics driver is enable or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated driver is not disabled")
        logging.info("PASS: Integrate graphics Driver disable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver is not Enabled")
        logging.info("PASS: Discrete graphics Driver is enable")

        # Disable Discrete graphics driver
        logging.info("Disabling Discrete Graphics driver")
        self.assertEqual(display_essential.disable_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver disable failed")

        # Verify integrated and discrete graphics drivers are Disabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated driver is not disabled")
        logging.info("PASS: Integrate graphics Driver disable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), False,
                         "Aborting the test as Discrete driver is not disabled")
        logging.info("PASS: Discrete graphics Driver Disable successful")

        ##
        # Enable both graphics driver one by one
        logging.info("Step-Driver Enable: Enable the driver")
        # Enable Discrete Graphics driver
        logging.info("Enabling Discrete Graphics Driver")
        self.assertEqual(display_essential.enable_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver enable failed")

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver is not enabled")
        logging.info("PASS: Discrete Driver enable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated driver is enabled")
        logging.info("PASS: Integrate graphics Driver is disable")

        # Enabling Integrated Graphics Driver
        logging.info("Enabling Integrated Graphics Driver")
        self.assertEqual(display_essential.enable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver enable failed")

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver is not enabled")
        logging.info("PASS: Discrete Driver enable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver is not enabled")
        logging.info("PASS: Integrate graphics Driver is enable")

        # Set valid configuration post both driver enable
        self.assertEqual(self.config.set_display_configuration_ex(self.config_type, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")

        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed till driver disable")

        ##
        # @ Disable both graphics driver one by one discrete followed by integrated
        logging.info("Step-Driver Disable: Disable the driver")
        # Disable Discrete graphics driver
        logging.info("Disabling Discrete Graphics driver")
        self.assertEqual(display_essential.disable_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver disable failed")

        # Verify integrated graphics driver is enabled or not and Discrete graphics driver is disable or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver is not Enabled")
        logging.info("PASS: Integrate graphics Driver is enable")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), False,
                         "Aborting the test as Discrete driver is not Disabled")
        logging.info("PASS: Discrete graphics Driver Disable successful")

        # Disable integrated Driver
        logging.info("Disabling integrated Graphics driver")
        self.assertEqual(display_essential.disable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver disable failed")

        # Verify integrated graphics driver is Disabled or not and Discrete graphics driver is enable or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), False,
                         "Aborting the test as integrated driver is not disabled")
        logging.info("PASS: Integrate graphics Driver disable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), False,
                         "Aborting the test as Discrete driver is not disabled")
        logging.info("PASS: Discrete graphics Driver disable successful")

        ##
        # Enable both graphics driver one by one Integrated followed by Discrete
        logging.info("Step-Driver Enable: Enable the driver")
        # Enabling Integrated Graphics Driver
        logging.info("Enabling Integrated Graphics Driver")
        self.assertEqual(display_essential.enable_driver(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver enable failed")

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), False,
                         "Aborting the test as Discrete driver is enable")
        logging.info("PASS: Discrete Driver is Disable")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver is not enabled")
        logging.info("PASS: Integrate graphics Driver is enable")

        # Enable Discrete Graphics driver
        logging.info("Enabling Discrete Graphics Driver")
        self.assertEqual(display_essential.enable_driver(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver enable failed")

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_1'), True,
                         "Aborting the test as Discrete driver is not enabled")
        logging.info("PASS: Discrete Driver enable successful")
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
                         "Aborting the test as integrated driver is not enabled")
        logging.info("PASS: Integrate graphics Driver is enable")

        # Set valid configuration post both driver enable
        self.assertEqual(self.config.set_display_configuration_ex(self.config_type, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")
        ##
        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')
        logging.info("PASS: No under-run observed till driver disable")

        self.is_teardown_required = True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)