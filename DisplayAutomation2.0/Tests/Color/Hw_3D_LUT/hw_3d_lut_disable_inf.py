##############################################################################################
# \file             hw_3d_lut_disable_inf.py
# \addtogroup       Test_Color
# \section          hw_3d_lut_disable_inf
# \ref              hw_3d_lut_disable_inf.py \n
# \remarks          This script performs disabling of hardware 3D LUT and verifies if the
#                   hardware 3D LUT is disabled.
#
# CommandLine:      python hw_3d_lut_disable_inf.py -edp_a
#
# \author           Anjali Shetty
###############################################################################################
from Libs.Core import registry_access, display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Hw_3D_LUT.hw_3d_lut_base import *


class Hw3DLutDisableInf(Hw3DLUTBase):
    def runTest(self):
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
            # restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()

        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # Apply SINGLE display configuration
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied the configuration")

            ##
            # Verify the 3D LUT registers
            pipe_status, hw_3d_lut_status, hw_lut_buffer_status = verify_3d_lut(self.connected_list[0])
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, None,pipe_status,"Enabled",None,"DISABLED") is False:
                self.fail()
            if not self.utility.is_ddrw():
                registry_access.write(args=reg_args, reg_name="SupportedCustomLUT",
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=0)
                registry_access.write(args=reg_args, reg_name="EnabledDPP",
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=0)
                registry_access.write(args=reg_args, reg_name="SupportedDPP",
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=0)
                registry_access.write(args=reg_args, reg_name="EnableHardware3DLUT",
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=0)

                ##
                # Restart display driver
                status, reboot_required = display_essential.restart_gfx_driver()

        else:
            logging.info("Failed to apply the configuration")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
