########################################################################################################################
# @file         dual_lfp_adjustment_fms.py
# @brief        This files contains tests to verify dual lfp adjustment with fast Modeset
# @details      With Fast ModeSet enabled, verify panel misalignment adjustment when top border or bottom border are
#               configured for dual LFP.
#               CommandLine: python dual_lfp_adjustment_fms.py -mipi_a -mipi_c -border 100 -panel1 top -panel2 bottom
#
# @author       Sri Sumanth Geesala,Neha3 Kumari
########################################################################################################################
from Libs.Core import enum, registry_access, display_essential
from Tests.LFP_Common.Dual_LFP_Adjustment.dual_lfp_adjustment_base import *


##
# @brief        This class contains tests to verify dual LFP Adjustments with Fast Modeset
class DualLfpAdjustmentFms(DualLfpAdjustmentBase):

    ##
    # @brief        The test function if to verify enabling of the FMS by setting the value of key: DisplayOptimizations
    #               to 0x1d'.
    # @return       None
    def test_1(self):
        logging.info(':Enabling the Fast ModeSet (FMS) by setting the value of key: DisplayOptimizations to 0x1d')
        key_name = "DisplayOptimizations"
        reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=0x1d) is False:
            self.fail("Enabling FMS by setting the value of key: DisplayOptimizations to [0x1d] FAILS ")
        logging.info("configuring border values in vbt with border value : {0} ".format(self.border_value))
        # configure the border values in vbt, and do reboot
        self.configure_borders_in_vbt()
        self.error_count = logging.error.counter
        if reboot_helper.reboot(self, 'test_2') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This test verifies the scalar register, resets vbt to default state and does a driver
    #               disable/enable after that.
    # @return       None
    # This test is verifying the scalar register, resetting vbt to default state and doing a driver disable / enable
    # after that.
    def test_2(self):
        logging.info("verifying scalar register ")
        logging.error = callcounted(logging.error)
        logging.error.counter = self.error_count
        # verify scalar registers for the current configuration
        self.verify_scalar_register_programming()

        # If panel is DSC enabled, verify DSC parameters
        if self.DSC_enabled:
            self.verify_dsc()

        # resetting vbt and doing driver disable/enable to reflect the changes
        logging.info('Resetting VBT to default state')
        if Vbt().reset() is False:
            self.fail('Reset Vbt failed')
        # driver disable/enable
        logging.info('doing a restart of display driver after resetting VBT')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('restarting display driver failed')

    ##
    # @brief        This function indicates the end of verification of dual lfp adjustment with FMS
    # @return       None
    def test_3(self):
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentFms'))
    TestEnvironment.cleanup(results)
