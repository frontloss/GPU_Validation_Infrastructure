##############################################################################################
# \file             hw_3d_lut_2pipe_multi_display_displayswap.py
# \addtogroup       Test_Color
# \section          hw_3d_lut_2pipe_multi_display_displayswap
# \ref              hw_3d_lut_2pipe_multi_display_displayswap.py \n
# \remarks          This script performs color functionality such as getting the hardware 3D
#                   LUT info and then setting the LUT data. It checks for the enabling of 3D
#                   LUT after setting the LUT data.
#
# CommandLine:      python hw_3d_lut_2pipe_multi_display_displayswap.py -mipi_a -mipi_c -dp_d
#
# \author           Soorya R, Smitha B
###############################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Hw_3D_LUT.hw_3d_lut_base import *


class Hw3DLutSingleDisplayCheck(Hw3DLUTBase):
    def runTest(self):
        utility = sys_utility.SystemUtility()

        ##
        # set topology to SINGLE display configuration
        topology = enum.CLONE
        ##
        # Apply SINGLE display configuration
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied the configuration")

            ##
            # Get the target id of the display
            target_id1 = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
            target_id2 = self.config.get_target_id(self.connected_list[1], self.enumerated_displays)
            target_id3 = self.config.get_target_id(self.connected_list[2], self.enumerated_displays)
            logging.info("targetIDs : %s,%s,%s", hex(target_id1), hex(target_id2), hex(target_id3))

            cui_dpp_hw_lut_info1 = DppHwLutInfo(target_id1, DppHwLutOperation.UNKNOWN.value, 0)
            cui_dpp_hw_lut_info2 = DppHwLutInfo(target_id2, DppHwLutOperation.UNKNOWN.value, 0)
            ##
            # Get the DPP Hw LUT info
            result1, cui_dpp_hw_lut_info1 = driver_escape.get_dpp_hw_lut(self.internal_gfx_adapter_index,
                                                                         cui_dpp_hw_lut_info1)
            if result1 is False:
                logging.error(f'Escape call failed : get_dpp_hw_lut() for {target_id1}')
            result2, cui_dpp_hw_lut_info2 = driver_escape.get_dpp_hw_lut(self.internal_gfx_adapter_index,
                                                                         cui_dpp_hw_lut_info2)
            if result2 is False:
                logging.error(f'Escape call failed : get_dpp_hw_lut() for {target_id2}')
            path1 = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\\Hw3DLUT\\CustomLUT\\CustomLUT_no_G.bin")
            path2 = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\\Hw3DLUT\\CustomLUT\\CustomLUT_no_G.bin")

            cui_dpp_hw_lut_info1 = DppHwLutInfo(target_id1, DppHwLutOperation.APPLY_LUT.value,
                                                cui_dpp_hw_lut_info1.depth)
            cui_dpp_hw_lut_info2 = DppHwLutInfo(target_id2, DppHwLutOperation.APPLY_LUT.value,
                                                cui_dpp_hw_lut_info2.depth)
            if cui_dpp_hw_lut_info1.convert_lut_data(path1) is False:
                self.fail(f'Invalid bin file path provided : {path1}!')
            if cui_dpp_hw_lut_info2.convert_lut_data(path2) is False:
                self.fail(f'Invalid bin file path provided : {path2}!')

            ##
            # Set the DPP Hw LUT Info
            self.resetLUTReady(self.connected_list[0])
            self.resetLUTReady(self.connected_list[1])
            result1 = driver_escape.set_dpp_hw_lut(self.internal_gfx_adapter_index, cui_dpp_hw_lut_info1)
            if result1 is False:
                logging.error(f'Escape call failed : set_dpp_hw_lut() for {target_id1}')
            result2 = driver_escape.set_dpp_hw_lut(self.internal_gfx_adapter_index, cui_dpp_hw_lut_info2)
            if result2 is False:
                logging.error(f'Escape call failed : set_dpp_hw_lut() for {target_id2}')

            logging.info("Applied 3D LUT !!")
            ##
            # Plane processing

            exec_env = self.utility.get_execution_environment_type()
            if exec_env == 'SIMENV_FULSIM':
                self.perform_plane_processing()
                ##
                # Wait for the hardware to finish loading the LUT buffer into internal working RAM
                time.sleep(120)

            elif exec_env != 'SIMENV_FULSIM' and exec_env != 'POST_SI_ENV':
                self.wait_for_frame_cntr_incr(0)

            ##
            # Verify the 3D LUT registers
            current_pipe_0 = self.get_current_pipe(self.connected_list[0])
            hw_3d_lut_status, hw_lut_buffer_status = self.verify_3dlut(current_pipe_0, "CustomLUT_no_G.bin")
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,None,"DISABLED","NOT_LOADED",None) is False:
                self.fail()

            current_pipe_1 = self.get_current_pipe(self.connected_list[1])
            hw_3d_lut_status, hw_lut_buffer_status = self.verify_3dlut(current_pipe_1, "CustomLUT_no_G.bin")
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,None,"DISABLED","NOT_LOADED",None) is False:
                self.fail()

            topology = enum.SINGLE

            if self.config.set_display_configuration_ex(topology, [self.connected_list[2]]) is True:
                logging.info("Successfully applied the configuration")

            time.sleep(10)

            topology = enum.CLONE

            if self.config.set_display_configuration_ex(topology,
                                                        [self.connected_list[0], self.connected_list[1]]) is True:
                logging.info("Successfully applied the configuration")

            time.sleep(10)

            # exec_env = self.utility.get_execution_environment_type()
            if exec_env == 'SIMENV_FULSIM':
                self.perform_plane_processing()
                ##
                # Wait for the hardware to finish loading the LUT buffer into internal working RAM
                time.sleep(120)

            elif exec_env != 'SIMENV_FULSIM' and exec_env != 'POST_SI_ENV':
                self.wait_for_frame_cntr_incr(0)

            hw_3d_lut_status, hw_lut_buffer_status = self.verify_3dlut(current_pipe_0, "CustomLUT_no_G.bin")
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,None,"DISABLED","NOT_LOADED",None) is False:
                self.fail()

            hw_3d_lut_status, hw_lut_buffer_status = self.verify_3dlut(current_pipe_1, "CustomLUT_no_G.bin")
            if self.gdhm_hw_3d_lut_logging_check(hw_3d_lut_status, hw_lut_buffer_status,None,"DISABLED","NOT_LOADED",None) is False:
                self.fail()

        else:
            logging.error("Failed to apply the configuration")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
