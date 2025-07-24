######################################################################################
# @file         dual_lfp_adjustment_non_native_resolution.py
# @brief        This file contains tests to verify Dual Lfp Adjustment with non native resolution
# @details      It sets the non-native resolution in the MIPI panel and verifies the border adjustment in some of the
#               non-native resolution.Since non-native resolution will enable one scalar, and this adjustment feature
#               takes another scalar, the tests verify the concurrency.
#               CommandLine: python dual_lfp_adjustment_non_native_resolution.py -mipi_a -mipi_c -border 100 -panel1 top -panel2 bottom
#
# @author       Sri Sumanth Geesala, Neha3 Kumari
######################################################################################
from Libs.Core import display_essential
from Tests.LFP_Common.Dual_LFP_Adjustment.dual_lfp_adjustment_base import *


##
# @brief        This class contains tests to verify dual LFP Adjustments with non native resolution
class DualLfpAdjustmentNonNativeResolution(DualLfpAdjustmentBase):

    ##
    # @brief        This test verifies the configuration of the border values in vbt and then disables and enables the
    #               driver to reflect the changes.
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
    # @brief        This test verifies the application the non native resolution
    # @return       None
    def test_2(self):
        topology = 'CLONE'

        config = self.display_config.get_current_display_configuration()
        self.target_id_list.append(config.displayPathInfo[0].targetId)
        self.target_id_list.append(config.displayPathInfo[1].targetId)

        # supported_modes[] is a list of modes supported by the external display
        supported_modes = self.display_config.get_all_supported_modes(self.target_id_list, True, False, True)

        for key, values in supported_modes.items():
            if self.display_config.set_display_mode([values[0]]) is False:
                logging.error("FAIL: Failed to apply display mode {}. Exiting ...".format(values[0]))
            else:
                logging.info("Successfully applied the display mode {}. ".format(values[0]))

    ##
    # @brief        This test verifies the scalar register, resetting of vbt to default state and does a driver
    #               disable/enable after that.
    # @return       None
    def test_3(self):
        logging.info("verifying scalar register ")
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

    ##
    # @brief        This function indicates the end of verification of dual lfp adjustment with non native resolutions
    # @return       None
    def test_4(self):
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('DualLfpAdjustmentNonNativeResolution'))
    TestEnvironment.cleanup(results)
