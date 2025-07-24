#######################################################################################################################
# @file         fast_lace_track_iet_with_partA_partB_change.py
# @addtogroup   Test_Color
# @section      fast_lace_track_iet_with_partA_partB_change.py
# @remarks      @ref  fast_lace_track_iet_with_partA_partB_change.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux .
#               For different static images the IET computed is verified to have changed for each image with change in Part A and Part B
#               sections of the buffer
# @author       Soorya R
#######################################################################################################################
import win32api
from Tests.Color.LACE.lace_base import *


class LACETrackIETWithPartChange(LACEBase):

    def runTest(self):
        iet_data_firsttile_list = []
        iet_data_lasttile_list = []
        IMAGE_FILE = ["citylights.bmp", "earth.bmp", "mountains_partB.bmp", "oceansunrise.bmp"]

        # LACE enable
        lux_val = 8500
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[0], lux=lux_val,
                                                           lux_operation=True):
            logging.info(" Als Lux override set successfully - Lux : %d" % lux_val)

        for index in range(len(self.lfp_target_ids)):
            time.sleep(20)  # For PartA and PartB histogram load and IE programming completion
            if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index], lux_val):
                self.fail("Verify FastLACE register programming failed for LACE Enable !!")
        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)

        ##
        ## Set Cursor Position to (500,500)
        win32api.SetCursorPos((500, 500))

        ##
        # Flip image
        for index in range(0, 4):
            self.display_staticimage(IMAGE_FILE[index])
            logging.info("Image Displayed !!")
            time.sleep(5)
            # Disable IE enable bit before IET read
            self.disable_ieenable_function()
            # Get IET from registers
            for pipe in range(len(self.lfp_pipe_ids)):
                self.disable_ieenable_function()
                # Get IET from registers
                for pipe in range(len(self.lfp_pipe_ids)):
                    tile_x, tile_y = self.get_no_of_tiles(self.lfp_target_ids[pipe])
                    ## Print this and check what is coming for each image
                    iet_data_firsttile_list.append([read_iet_from_registers_for_single_tile(pipe, 0, 0)])
                    iet_data_lasttile_list = read_iet_from_registers_for_single_tile(pipe, tile_x, tile_y)
                time.sleep(8)

        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)

        logging.info(" iet_data_firsttile_list is %s" % iet_data_firsttile_list)

        ##
        # Verify that successive IETs are not same for different images
        for pipe in range(len(self.lfp_pipe_ids)):
            iet_first_tile_pair = [(0, 1), (1, 2), (2, 3)]
            iet_last_tile_pair = [(1, 2)]
            for index in range(len(iet_first_tile_pair)):
                previous_image = iet_first_tile_pair[index][0]
                current_image = iet_first_tile_pair[index][1]
                logging.debug("Previous Image IET Data :")
                logging.debug(iet_data_firsttile_list[previous_image])
                logging.debug("Current Image IET Data :")
                logging.debug(iet_data_firsttile_list[current_image])
                if iet_data_firsttile_list[previous_image] == iet_data_firsttile_list[current_image]:
                    logging.error(" Pipe : %s Part A  IET data remains same for two different buffers !!",
                                  chr(int(self.lfp_pipe_ids[pipe]) + 65))
                    self.fail()

            # Part B
            previous_image = iet_last_tile_pair[0][0]
            current_image = iet_last_tile_pair[0][1]
            if iet_data_lasttile_list[previous_image] == iet_data_lasttile_list[current_image]:
                logging.error(" Pipe : %s Part B IET data remains same for two different buffers !!",
                              chr(int(self.lfp_pipe_ids[pipe]) + 65))
                self.fail()

        # LACE disable
        lux_val = 150
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[0], lux=lux_val,
                                                           lux_operation=True):
            logging.info(" Als Lux override set successfully - Lux : %d" % lux_val)

        for index in range(len(self.lfp_target_ids)):
            time.sleep(2)  # For PartA and PartB histogram load and IE programming completion
            if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index], lux_val):
                self.fail("Verify FastLACE register programming failed for LACE Disable !!")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
