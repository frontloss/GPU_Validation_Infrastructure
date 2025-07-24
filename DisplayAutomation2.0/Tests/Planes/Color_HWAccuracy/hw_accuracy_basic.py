########################################################################################################################
# @file         hw_accuracy_basic.py
# @brief        This script contains test to flip single plane on single with specified parameters . Disable all color
#               blocks and capture the output dump for image comparison
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Color_HWAccuracy import hw_accuracy_programregisters
from Tests.Planes.Common.hdr_base import *

##
# @brief    Contains basic test to check hardware accuracy
class Test_HWAccuracy_Basic(HDRBase):
    NoLayers = [1, 1, 1, 1]
    reg_program = hw_accuracy_programregisters.HW_Accuracy_Programming()

    ##
    # @brief            Unittest runTest function
    # @return           None
    def runTest(self):

        self.parse_xml(self.xml)
        if self.blending_mode[0] == BT2020_LINEAR:
            self.setup_for_linear_mode()
        else:
            logging.info("Blending Mode is not Linear - ForceHDRMode Regkey need not be set")

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
            logging.info("Flipped successfully and the Register Verification has passed")

            display_base_obj = DisplayBase(self.connected_list[0])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[0])
            pipe_id = current_pipe

            str_pipe = chr(int(current_pipe) + 65)
            str_plane_pipe = "1_" + str_pipe

            self.reg_program.resetAllColorRegisters(str_plane_pipe, str_pipe)

            input('Enter')

        else:
            self.fail("SDR/HDR single plane flip verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
