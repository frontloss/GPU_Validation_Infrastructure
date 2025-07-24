########################################################################################################################
# @file         vrr_registry.py
# @brief        Contains registry key check for VRR
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core import enum, registry_access, display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.powercons import registry
from Tests.VRR.vrr_base import *


##
# @brief        This class contains VRR registry tests. This class inherits the VrrBase class.
#               This class contains a method to check if VRR is working as expected with correct registry entry values,
#               a method to check if the updates to the registry are successful or not.
class VrrRegistryTest(VrrBase):

    ##
    # @brief        Test function to check if VRR works as expected with correct registry entries
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_registry_enabled(self):
        if self.verify_vrr(True) is False:
            self.fail(f"VRR is not working with {registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE} registry key enabled")
        logging.info("\tPASS: VRR verification passed successfully")

        # Disable VRR from registry key
        self.update_vrr_registry(False)

        # Verify that VRR is not getting enabled
        if self.verify_vrr(True, negative=True, expected_vrr=False) is False:
            self.fail(f"VRR is working with {registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE} registry key disabled")
        logging.info("\tPASS: VRR verification passed successfully")

        # Enable VRR back from registry key
        self.update_vrr_registry(True)

    ##
    # @brief        Test function to check if it is possible to update registry keys and restart driver
    # @param[in]    enable indicates if the the registry entry has to be enabled or disabled
    # @return       None
    def update_vrr_registry(self, enable):
        value = registry.RegValues.ENABLE if enable else registry.RegValues.DISABLE
        for gfx_index, adapter in dut.adapters.items():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start(
                f"{'Enabling' if enable else 'Disabling'} VRR from registry "
                f"{registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE}")
            status = registry.write(gfx_index, registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE,
                                    registry_access.RegDataType.DWORD, value)
            if status is False:
                self.fail(f"Failed to update registry key {registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE}")

            logging.info("\tPASS: Updated registry key successfully")
            logging.info("\tRestarting the display driver after updating registry key")
            result, reboot_required = display_essential.restart_gfx_driver()
            if status and result is False:
                self.fail("Failed to restart display driver")
            logging.info("\t\tPASS: Restarted display driver successfully")
            html.step_end()


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VrrRegistryTest))
    TestEnvironment.cleanup(test_result)
