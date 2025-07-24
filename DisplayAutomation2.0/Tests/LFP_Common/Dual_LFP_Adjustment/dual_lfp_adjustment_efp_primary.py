######################################################################################
# @file         dual_lfp_adjustment_efp_primary.py
# @brief        The tests in this file verify dual LFP adjustment persistence during different dual LFP cases
# @details      It simulates another external panel and makes it as primary, and then verify the border adjustment in
#               two secondary MIPI panels. Since external panel is primary, it will define the orientation
#               CommandLine: python dual_lfp_adjustment_efp_primary.py -mipi_a -mipi_c -dp_d -border 100 -panel1 top
#                             -panel2 bottom
#
# @author       Sri Sumanth Geesala,Neha3 Kumari
######################################################################################
import time

from Libs.Core import display_utility, display_essential
from Libs.Core import enum
from Tests.LFP_Common.Dual_LFP_Adjustment.dual_lfp_adjustment_base import *


##
# @brief        This class contains tests to verify dual LFP persistence when an external monitor is connected and made
#               primary
class DualLfpAdjustmentEfpPrimary(DualLfpAdjustmentBase):

    ##
    # @brief        This test verifies configuring of the border values in vbt and then disables and enables the
    #               driver to reflect the changes
    # @return       None
    def test_1(self):
        logging.info("configuring border values in vbt with border value :{0}  ".format(self.border_value))
        # configure the border values in vbt, and do driver disable/enable
        self.configure_borders_in_vbt()
        # driver disable/enable
        logging.info('doing a restart of display driver after setting VBT')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('restarting display driver failed')

    ##
    # @brief        This test plugs the external display, verifies the border values and then unplugs the display
    # @return       None
    def test_2(self):
        plugged_display, enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        config_combination_list = [[plugged_display[0], self.lfps_in_cmdline[0], self.lfps_in_cmdline[1]]]
        for config in config_combination_list:
            time.sleep(10)
            logging.info('Applying CLONE %s+%s+%s config' % (config[0], config[1], config[2]))
            time.sleep(10)
            result = self.display_config.set_display_configuration_ex(enum.CLONE, config, enumerated_displays)
            time.sleep(10)
            self.assertNotEquals(result, False, "Aborting the test as applying CLONE %s+%s+%s config failed." % (
                config[0], config[1], config[2]))
        logging.info('Verifying the scalar register')
        # verify scalar registers for the current configuration
        self.verify_scalar_register_programming()

        # If panel is DSC enabled, verify DSC parameters
        if self.DSC_enabled:
            self.verify_dsc()

        # resetting vbt and doing driver disable/enable to reflect the changes
        logging.info('Resetting VBT to default state')
        if self.gfx_vbt.reset() is False:
            self.fail('Reset Vbt failed')
        # driver disable/enable
        logging.info('doing a restart of display driver after resetting VBT')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('restarting display driver failed')

        # unplugging the external port that is being plugged
        display_utility.unplug(plugged_display[0])

    ##
    # @brief        This test indicates the end of verification
    # @return       None
    def tes1t_3(self):
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentEfpPrimary'))
    TestEnvironment.cleanup(results)
