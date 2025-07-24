######################################################################################
# @file         dual_lfp_adjustment_power_events.py
# @brief        This file contains tests for dual lfp adjustment with power events
# @details      Verify panel misalignment adjustment when top border or bottom border are configured for dual LFP,
#               after resume from power events like CS/S3,S4,S5.
#               CommandLine: python dual_lfp_adjustment_power_events.py -mipi_a -mipi_c -border 100 -panel1 top
#               -panel2 bottom
#
# @author       Sri Sumanth Geesala,Neha3 Kumari
######################################################################################
from Libs.Core import display_essential, display_power, enum
from Tests.LFP_Common.Dual_LFP_Adjustment.dual_lfp_adjustment_base import *


##
# @brief        This class contains tests to verify dual LFP Adjustments with power events
class DualLfpAdjustmentPowerEvents(DualLfpAdjustmentBase):

    ##
    # @brief        This test verifies the configuration of the border values in vbt and does a system reboot after that
    # @return       None
    def test_1(self):
        # configure the border values in vbt, and do reboot
        logging.info("configuring border values in vbt with border value : {0} ".format(self.border_value))
        self.configure_borders_in_vbt()
        # do system reboot
        logging.info('doing a system reboot after setting VBT')
        if reboot_helper.reboot(self, 'test_2') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This test verifies the scalar register after applying various power events like CS/S3,S4,S5
    # @return       None
    def test_2(self):
        # verify scalar registers for he cutrrent configuration
        logging.info("Verifying the scalar register before going to sleep (CS/S3).............")
        self.verify_scalar_register_programming()

        # If panel is DSC enabled, verify DSC parameters
        if self.DSC_enabled:
            self.verify_dsc()

        if self.display_power.is_power_state_supported(display_power.PowerEvent.CS) is True:
            self.display_power.invoke_power_event(display_power.PowerEvent.CS, 10)
        else:
            self.display_power.invoke_power_event(display_power.PowerEvent.S3, 10)
        logging.info("Verifying the scalar register after CS/S3..........")
        # verify scalar registers for the current configuration
        self.verify_scalar_register_programming()

        # If panel is DSC enabled, verify DSC parameters
        if self.DSC_enabled:
            self.verify_dsc()

        # doing system hibernate s4=HIBERNATE
        self.display_power.invoke_power_event(display_power.PowerEvent.S4, 10)
        logging.info("Verifying the scalar register after S4...............")
        # verify scalar registers for the current configuration
        self.verify_scalar_register_programming()

        # If panel is DSC enabled, verify DSC parameters
        if self.DSC_enabled:
            self.verify_dsc()

        self.error_count = logging.error.counter
        if reboot_helper.reboot(self, 'test_3') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This test verifies the scalar register after S5 and does a driver disable/enable after resetting vbt
    # @return       None
    def test_3(self):
        logging.info("Verifying the scalar register after S5...............")
        logging.error = callcounted(logging.error)
        logging.error.counter = self.error_count
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
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentPowerEvents'))
    TestEnvironment.cleanup(results)
