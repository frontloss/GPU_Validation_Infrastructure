##############################################################################################
# \file             hw_3d_lut_dc_states.py
# \addtogroup       Test_Color
# \section          hw_3d_lut_dc_states
# \ref              hw_3d_lut_dc_states.py \n
# \remarks          This script performs color functionality such as getting the hardware 3D
#                   LUT info and then setting the LUT data. It checks for the enabling of 3D
#                   LUT after setting the LUT data and also after enetring the different DC
#                   states.
#
# CommandLine:      python hw_3d_lut_dc_states.py -edp_a -hdmi_b
#
# \author           Anjali Shetty
###############################################################################################

from Libs.Core import  display_essential, display_power, registry_access
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Hw_3D_LUT.hw_3d_lut_base import *

class Hw3DLutDcStates(Hw3DLUTBase):
    disp_power = display_power.DisplayPower()

    def test_before_reboot(self):
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
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=1)

            ##
            # restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()

        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # Apply SINGLE display configuration
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info("Successfully applied the configuration")
            target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

            ##
            # Get the target id of the display
            target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
            cui_dpp_hw_lut_info = DppHwLutInfo(target_id, DppHwLutOperation.UNKNOWN.value, 0)
            ##
            # Get the DPP Hw LUT info
            result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(self.internal_gfx_adapter_index,
                                                                       cui_dpp_hw_lut_info)
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
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,pipe_status,"DISABLED","NOT_LOADED","DISABLED") is False:
                self.fail()

            ##
            # Invoke S3 state
            if self.disp_power.invoke_power_event(display_power.PowerEvent.S3, 60):
                ##
                # Verify the 3D LUT registers
                pipe_status, hw_3d_lut_status, hw_lut_buffer_status = verify_3d_lut(self.connected_list[0])
                if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,pipe_status,"DISABLED","NOT_LOADED","DISABLED") is False:
                    self.fail()
            ##
            # Invoke S4 state
            if self.disp_power.invoke_power_event(display_power.PowerEvent.S4, 60):
                time.sleep(10)
                ##
                # Verify the 3D LUT registers
                pipe_status, hw_3d_lut_status, hw_lut_buffer_status = verify_3d_lut(self.connected_list[0])
                if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,pipe_status,"DISABLED","NOT_LOADED","DISABLED") is False:
                    self.fail()

        else:
            logging.info("Failed to apply the configuration")

        ##
        # Apply different configurations
        config_list = [(enum.SINGLE, [self.connected_list[1]]), (enum.SINGLE, [self.connected_list[0]]),
                       (enum.CLONE, self.connected_list)]
        for config in range(0, len(config_list)):
            if self.config.set_display_configuration_ex(config_list[config][0], config_list[config][1]) is True:
                logging.info("Successfully applied the configuration")
                ##
                # Verify the 3D LUT registers
                if config != 0:
                    pipe_status, hw_3d_lut_status, hw_lut_buffer_status = verify_3d_lut(self.connected_list[0])
                    if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,pipe_status,"DISABLED","NOT_LOADED","DISABLED") is False:
                        self.fail()
            else:
                logging.info("Failed to apply the configuration")

        if not self.utility.is_ddrw():
            registry_access.write(args=reg_args, reg_name="SupportedCustomLUT",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)
            registry_access.write(args=reg_args, reg_name="EnabledDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)
            registry_access.write(args=reg_args, reg_name="SupportedDPP",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)
            registry_access.write(args=reg_args, reg_name="EnableHardware3DLUT",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=0)

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    def test_after_reboot(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Hw3DLutDcStates'))
    TestEnvironment.cleanup(outcome)
