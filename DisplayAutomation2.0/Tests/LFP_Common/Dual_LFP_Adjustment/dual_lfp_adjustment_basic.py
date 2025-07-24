######################################################################################
# @file         dual_lfp_adjustment_basic.py
# @brief        Verify panel misalignment adjustment when top border or bottom border are configured for dual LFP.
# @details      CommandLine: python dual_lfp_adjustment_basic.py -mipi_a -mipi_c -border 100 -panel1 top -panel2 bottom
#
# @author       Sri Sumanth Geesala,Neha3 Kumari
######################################################################################
from Libs.Core import display_essential
from Tests.LFP_Common.Dual_LFP_Adjustment.dual_lfp_adjustment_base import *


##
# @brief        This class contains basic Dual Lfp Adjustment basic tests
class DualLfpAdjustmentBasic(DualLfpAdjustmentBase):

    ##
    # @brief        This test configures the border values in vbt and then disables and enables the driver to
    #               reflect the changes.
    # @return       None
    def test_1(self):
        logging.info("configuring border values in vbt with border value :{0}  ".format(self.border_value))
        # configure the border values in vbt, and do driver disable/enable
        self.configure_borders_in_vbt()
        # driver disable/enable
        logging.info('doing a disable-enable of display driver after setting VBT')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('restarting display driver failed')

    ##
    # @brief        This test verifies the scalar register,resetting vbt to default state and does a driver
    #               disable/enable after that.
    # @return       None
    def test_2(self):
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
        # driver restart
        logging.info('doing a restart of display driver after resetting VBT')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('restarting display driver failed')

    ##
    # @brief        This test is used for logging the end of Dual Lfp Adjustment basic tests.
    # @return       None
    def test_3(self):
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentBasic'))
    TestEnvironment.cleanup(results)
