########################################################################################################################
# @file         hw_accuracy_tm_lut_two_planes_assignment_swap.py
# @brief        This script contains  test to flip single plane on single with specified parameters . Disable all color
#               blocks ,program the TM HW block with a targeted LUT and capture the output dump for image comparison
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Color_HWAccuracy import hw_accuracy_programregisters
from Tests.Planes.Common.hdr_base import *

TMLUT_DATA_171_SAMPLES_4000_to_400_NITS = [65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536,
                                           65536, 65536, 65536, 65536, 65536, 65536, 65536, 65534,
                                           65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                           65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                           65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                           65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                           65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 64798,
                                           64064, 63328, 62594, 61858, 61124, 60388, 59654, 58468,
                                           57282, 56098, 54912, 53890, 52866, 51844, 50822, 48996, 47172, 45602, 44034,
                                           42690, 41346, 40194, 39042, 38048, 37056, 36200, 35344,
                                           34604, 33864, 33220, 32576, 32014, 31452, 30960, 30466, 30030, 29596, 29210,
                                           28824, 28140, 27530, 26984, 26496, 26058, 25664, 25310,
                                           24990, 24702, 24440, 24200, 23982, 23782, 23596, 23420, 23254, 22934, 22614,
                                           22276, 21908, 21512, 21088, 20646, 20194, 19740, 19290,
                                           18852, 18426, 18018, 17628, 17256, 16904, 16254, 15668, 15128, 14616, 14120,
                                           13640, 13182, 12750, 12346, 11968, 11616, 11290, 10980,
                                           10680, 10390, 10104, 9564, 9070, 8626, 8224, 7862, 7534, 7232, 6958, 6702,
                                           6452, 6214, 5992, 5784, 5592, 5412, 5242
                                           ]

##
# @brief    Contains function to test hardware accuracy of TMLUT
class Test_HWAccuracy_TMLUT(HDRBase):
    NoLayers = [1, 1, 1, 1]
    reg_program = hw_accuracy_programregisters.HW_Accuracy_Programming()

    ##
    # @brief            Unittest runTest function
    # @return           None
    def runTest(self):

        self.parse_xml(self.xml)
        self.set_native_mode()

        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)
        pyPlanes = []
        for index in range(0, self.no_displays):
            stMPOBlend = flip.MPO_BLEND_VAL(0)
            tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
            sdimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes / 2, self.current_mode[index].VtRes)
            ddimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes / 2, self.current_mode[index].VtRes)
            sdimension2 = flip.MPO_RECT(self.current_mode[index].HzRes / 2, 0,
                                        self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            ddimension2 = flip.MPO_RECT(self.current_mode[index].HzRes / 2, 0,
                                        self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            pyPlanes = []

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes / 2,
                                                self.current_mode[index].VtRes, self.pixel_format[0], 0, index)
            out_file1 = self.convert_png_to_bin(self.path[1], self.current_mode[index].HzRes / 2,
                                                self.current_mode[index].VtRes, self.pixel_format[1], 0, index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], 1, 1, self.pixel_format[0], tiling, sdimension1,
                                     ddimension1,
                                     ddimension1, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0], out_file0)
            Plane2 = flip.PLANE_INFO(self.source_id[index], 0, 1, self.pixel_format[1], tiling, sdimension2,
                                     ddimension2,
                                     ddimension2, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[1], out_file1)
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)

        if self.perform_flip_hwaccuracy(planes):
            logging.info("Flipped successfully ")

            display_base_obj = DisplayBase(self.connected_list[0])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[0])
            pipe_id = current_pipe

            str_pipe = chr(int(current_pipe) + 65)
            str_plane_pipe = "1_" + str_pipe

            self.reg_program.resetAllColorRegisters(str_plane_pipe, str_pipe)

            # LM_TONEMAPPING_CTL - TM assigned to Plane 1
            self.driver_interface_.mmio_write(0x68300, 0x80000000, 'gfx_0')
            self.driver_interface_.mmio_write(0x68B00, 0x80000000, 'gfx_0')

            self.reg_program.program_gamma_lut_registers("LM_TONEFACT", 171, TMLUT_DATA_171_SAMPLES_4000_to_400_NITS,
                                                         str_plane_pipe)

            input('Enter')

            # LM_TONEMAPPING_CTL - TM assigned to Plane 2
            self.driver_interface_.mmio_write(0x68300, 0x80000001, 'gfx_0')
            self.driver_interface_.mmio_write(0x68B00, 0x80000001, 'gfx_0')

            input('Enter')

        else:
            self.fail("SDR two plane flip failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
