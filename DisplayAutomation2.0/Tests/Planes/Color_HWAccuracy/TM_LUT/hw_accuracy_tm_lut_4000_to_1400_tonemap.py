########################################################################################################################
# @file         hw_accuracy_tm_lut_4000_to_1400_tonemap.py
# @brief        This script contains  test to flip single plane on single with specified parameters . Disable all color
#               blocks ,program the TM HW block with a targeted LUT and capture the output dump for image comparison
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Color_HWAccuracy import hw_accuracy_programregisters
from Tests.Planes.Common.hdr_base import *

TMLUT_DATA_171_SAMPLES_4000_to_1400_NITS = [65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536,
                                            65536, 65536, 65536, 65536, 65536, 65536, 65536,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534,
                                            65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65534, 65532,
                                            65528, 65522, 65512, 65496, 65430, 65300, 65066,
                                            64704, 64196, 63544, 62768, 61892, 60950, 59966, 58964, 57966, 56984, 56028,
                                            55106, 54224, 52574, 51078, 49692, 48354, 47006,
                                            45644, 44296, 42992, 41752, 40584, 39492, 38472, 37506, 36570, 35646, 34730,
                                            32960, 31326, 29846, 28512, 27304, 26206, 25206,
                                            24288, 23430, 22586, 21750, 20974, 20250, 19576, 18944, 18352]

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
            sdimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            ddimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            pyPlanes = []

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes,
                                                self.current_mode[index].VtRes, self.pixel_format[0], 0, index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, self.pixel_format[0], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0], out_file0)
            pyPlanes.append(Plane1)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)

        if self.perform_flip_hwaccuracy(planes):
            logging.info("Flipped successfully ")

            display_base_obj = DisplayBase(self.connected_list[0])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[0])
            pipe_id = current_pipe

            str_pipe = chr(int(current_pipe) + 65)
            str_plane_pipe = "1_" + str_pipe

            self.reg_program.resetAllColorRegisters(str_plane_pipe, str_pipe)

            # LM_TONEMAPPING_CTL
            self.driver_interface_.mmio_write(0x68300, 0x80000000, 'gfx_0')
            self.driver_interface_.mmio_write(0x68B00, 0x80000000, 'gfx_0')

            self.reg_program.program_gamma_lut_registers("LM_TONEFACT", 171, TMLUT_DATA_171_SAMPLES_4000_to_1400_NITS,
                                                         str_plane_pipe)

            input('Enter')

        else:
            self.fail("SDR single plane flip failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
