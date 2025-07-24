##############################################################################################
# \file             hw_3d_lut_negative_testing.py
# \addtogroup       Test_Color
# \section          hw_3d_lut_negative_testing
# \ref              hw_3d_lut_negative_testing.py \n
# \remarks          This script performs disabling of hardware 3D LUT and verifies if the
#                   hardware 3D LUT is disabled during the lid events.
#
# CommandLine:      python hw_3d_lut_negative_testing.py -edp_a -hdmi_b
#
# \author           Anjali Shetty
###############################################################################################
from Libs.Core import registry_access, display_essential
from Libs.Core.hw_emu.hotplug_emulator_utility import HotPlugEmulatorUtility
from Libs.Core.hw_emu.she_utility import LidSwitchState
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Hw_3D_LUT.hw_3d_lut_base import *


class Hw3DLUTNegativeTesting(Hw3DLUTBase):
    hotplug_emulator_utility = HotPlugEmulatorUtility()

    def test_before_reboot(self):
        logging.info("Before reboot")

        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SOFTWARE\Intel\IGFX\DPP")
        if not self.utility.is_ddrw():
            registry_access.write(args=reg_args, reg_name="SupportedCustomLUT",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=1)
            registry_access.write(args=reg_args, reg_name="EnabledDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=1)
            registry_access.write(args=reg_args, reg_name="SupportedDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=1)
            registry_access.write(args=reg_args, reg_name="EnableHardware3DLUT",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()

        if self.hotplug_emulator_utility.hot_plug(self.connected_list[1], 0):
            logging.info("Plug Successful")
        else:
            logging.info("Plug failed")

        ##
        # Close the lid
        lid_close = self.hotplug_emulator_utility.lid_switch(LidSwitchState.CLOSE, 0)
        if not lid_close:
            logging.info("Failed to close the lid")
            self.fail()
        else:
            logging.info("Lid event successful")

        time.sleep(2)

        if reboot_helper.reboot(self, 'test_after_reboot1') is False:
            self.fail("Failed to reboot the system")

    def test_after_reboot1(self):
        logging.info("After reboot")
        config = display_config.DisplayConfiguration()

        ##
        # Open the lid
        lid_open = self.hotplug_emulator_utility.lid_switch(LidSwitchState.OPEN, 0)
        if not lid_open:
            logging.info("Failed to open the lid")
            self.fail()
        else:
            logging.info("Lid event successful")

        ##
        # Get the target id of the display
        target_id = config.get_target_id(self.connected_list[0], self.enumerated_displays)
        cui_dpp_hw_lut_info = DppHwLutInfo(target_id, DppHwLutOperation.UNKNOWN.value, 0)

        ##
        # Get the DPP Hw LUT info
        result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(self.internal_gfx_adapter_index, cui_dpp_hw_lut_info)
        if result is False:
            logging.error(f'Escape call failed : get_dpp_hw_lut() for {target_id}')
        path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\Hw3DLUT\CustomLUT\CustomLUT_no_B.bin")

        cui_dpp_hw_lut_info = DppHwLutInfo(target_id, DppHwLutOperation.APPLY_LUT.value, cui_dpp_hw_lut_info.depth)
        if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
            self.fail(f'Invalid bin file path provided : {path}!')

        ##
        # Set the DPP Hw LUT Info
        result = driver_escape.set_dpp_hw_lut(self.internal_gfx_adapter_index, cui_dpp_hw_lut_info)
        if result is False:
            logging.error(f'Escape call failed : set_dpp_hw_lut() for {target_id}')

        ##
        # Verify the 3D LUT registers
        pipe_status, hw_3d_lut_status, hw_lut_buffer_status = verify_3d_lut(self.connected_list[0])
        if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, None, pipe_status, "Enabled", None, "DISABLED") is False:
            self.fail()
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SOFTWARE\Intel\IGFX\DPP")
        if not self.utility.is_ddrw():
            registry_access.write(args=reg_args, reg_name="SupportedCustomLUT",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)
            registry_access.write(args=reg_args, reg_name="EnabledDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)
            registry_access.write(args=reg_args, reg_name="SupportedDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)

        if reboot_helper.reboot(self, 'test_after_reboot2') is False:
            self.fail("Failed to reboot the system")

    def test_after_reboot2(self):
        pass

    def tearDown(self):
        logging.info("Test Clean Up")

        exc_tuple = sys.exc_info()
        if exc_tuple.count(None) != len(exc_tuple):
            if self.hotplug_emulator_utility.hot_unplug(self.connected_list[1], 0):
                logging.info("Unplug Successful")
            else:
                logging.info("Unplug failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Hw3DLUTNegativeTesting'))
    TestEnvironment.cleanup(outcome)
