########################################################################################################################
# @file         hdr_singleplane_fullscreen.py
# @brief        This script contains test to flip single plane on single or multiple displays with different plane
#               parameters.Test verifies display color pipeline programming and also checks for underrun.
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common.hdr_base import *

##
# @brief   Contains functions to verify display color pipeline programming and also checks for underrun for single plane
class Test_HDRSinglePlane(HDRBase):
    no_of_layers = [1, 1, 1, 1]

    ##
    # @brief     Unittest runTest function
    # @return    None
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

        count = [0, 0]
        pyPlanes = []
        for index in range(0, self.no_displays):
            stMPOBlend = flip.MPO_BLEND_VAL(0)
            tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
            sdimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            ddimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            pyPlanes = []

            if not planes_verification.check_layer_reordering() and self.pixel_format[0] in self.planar_formats:
                plane1_layer = 1
            else:
                plane1_layer = 0

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes,
                                                self.current_mode[index].VtRes, self.pixel_format[0], plane1_layer,
                                                index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], tiling, sdimension,
                                     ddimension, ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[0], out_file0)

            pyPlanes.append(Plane1)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)

        if self.perform_hdr_flip(planes):
            logging.info("Flipped successfully and the Register Verification has passed")
        else:
            self.fail("SDR/HDR single plane flip verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
