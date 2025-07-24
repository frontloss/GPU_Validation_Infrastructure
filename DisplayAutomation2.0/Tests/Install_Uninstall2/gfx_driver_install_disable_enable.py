##
# @file gfx_driver_install_disable_enable.py
# @brief The script verifies whether the graphics driver disable enable is working properly or not
# @details * Step1: Verifies whether the primary graphics driver is installed and enable.
#          *        Verify primary driver version and check for underrun
#          *        Disable Driver and check driver status as disable/not running
#          *        enable driver and check driver status as enable/Running
# @author Patel, Ankurkumar G, Chandrashekhar, SomashekarX, Doriwala, Nainesh P
from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Install_Uninstall2.install_uninstall2_base import *

##
# @brief it contain method to verify graphics driver disable enable is working properly or not
class GfxDriverInstallDisableEnable(InstallUninstall2Base):

    ##
    # @brief step 1 - Verifies whether the primary graphics driver is installed and enable.
    #                 Verify primary driver version and check for underrun
    #                 Disable Driver and check driver status as disable/not running
    #                 enable driver and check driver status as enable/Running
    # @return None
    def runTest(self):

        # Verify driver is Enabled or not
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True,
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
        logging.info("PASS: No underrun observed till driver disable")

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
        self.assertEqual(self.is_driver_running(gfx_index='gfx_0'), True, "Aborting the test as driver is not enabled")
        logging.info("PASS: Driver enable successful")

        self.is_teardown_required = True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
