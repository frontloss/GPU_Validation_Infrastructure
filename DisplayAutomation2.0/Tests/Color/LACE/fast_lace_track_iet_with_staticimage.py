#######################################################################################################################
# @file         fast_lace_track_iet_with_staticimages.py
# @addtogroup   Test_Color
# @section      fast_lace_track_iet_with_staticimages.py
# @remarks      @ref fast_lace_track_iet_with_staticimages.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux .
#               For different static images the IET computed is verified to have changed for each image with buffer change
# @author       Soorya R
#######################################################################################################################
import win32api
from Tests.Color.LACE.lace_base import *


class LACETrackIETWithStaticImages(LACEBase):

    def runTest(self):
        IMAGE_FILE = ["earth.bmp", "oceansunrise.bmp", "citylights.bmp", "driveway.bmp"]
        iet_data_list = []
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
        # Set Cursor Position to (500,500)
        win32api.SetCursorPos((500, 500))

        ##
        # Flip image
        for index in range(0, 4):
            self.display_staticimage(IMAGE_FILE[index])
            logging.info("Image Displayed !!")
            time.sleep(5)
            # Disable IE enable bit before IET read
            self.disable_ieenable_function()
            time.sleep(2)
            # Get IET from registers
            for pipe in range(len(self.lfp_pipe_ids)):
                iet_data = read_iet_from_registers_for_single_tile(pipe, 0, 0)
                iet_data_list.append(iet_data)

        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)

        ##
        # Verify that successive IETs are not same for different images
        for pipe in range(len(self.lfp_pipe_ids)):
            low = 1 * (pipe + 1)
            high = 4 * (pipe + 1)

            for n in range(low, high):

                if iet_data_list[n - 1] == iet_data_list[n]:
                    logging.info("List : %d --> %s \n  List : %d --> %s ", n - 1, str(iet_data_list[n - 1]), n,
                                 str(iet_data_list[n]))
                    logging.error(" Pipe : %s IET data remains same for two different buffers !!",
                                  chr(int(self.lfp_pipe_ids[pipe]) + 65))
                    self.fail()

        if self.underrun.verify_underrun():
            logging.error("Underrun Occured")

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
