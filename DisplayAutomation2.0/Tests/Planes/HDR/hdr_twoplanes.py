########################################################################################################################
# @file         hdr_twoplanes.py
# @brief        This script contains test to flip two planes on single or multiple displays with different plane
#               parameters.Test verifies display color pipeline programming and also checks for underrun.
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common.hdr_base import *

##
# @brief    Contains functions to verify display color pipeline programming and also checks for underrun for two planes
class Test_TwoPlanesHDR(HDRBase):
    no_of_layers = [2, 2, 2, 2]

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

        stMPOBlend = flip.MPO_BLEND_VAL(0)
        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
        pyPlanes = []
        for index in range(0, self.no_displays):
            sdimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            ddimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)

            ##
            # The Rectangle members should have an even value. CheckMPO failure will be observed if input to the driver for destination panning position is an odd value.
            # This is a known bspec restriction. Hence performing a rounding to make the values Even.
            left = self.current_mode[index].HzRes // 4 if (self.current_mode[index].HzRes // 4) % 2 == 0 else ((self.current_mode[index].HzRes // 4) - 1)
            top = self.current_mode[index].VtRes // 4 if (self.current_mode[index].VtRes // 4) % 2 == 0 else ((self.current_mode[index].VtRes // 4) - 1)
            right = self.current_mode[index].HzRes // 4 * 3 if (self.current_mode[index].HzRes // 4 * 3) % 2 == 0 else ((self.current_mode[index].HzRes // 4 * 3) - 1)
            bottom = self.current_mode[index].VtRes // 4 * 3 if (self.current_mode[index].VtRes // 4 * 3) % 2 == 0 else ((self.current_mode[index].VtRes // 4 * 3) - 1)
            sdimension2 = flip.MPO_RECT(left, top, right, bottom)
            ddimension2 = flip.MPO_RECT(left, top, right, bottom)
            pyPlanes = []

            if not planes_verification.check_layer_reordering() and self.pixel_format[1] in self.planar_formats:
                plane1_layer = 0
                plane2_layer = 1
            else:
                plane1_layer = 1
                plane2_layer = 0

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes,
                                                self.current_mode[index].VtRes, self.pixel_format[0], plane1_layer,
                                                index)
            out_file1 = self.convert_png_to_bin(self.path[1], self.current_mode[index].HzRes / 2,
                                                self.current_mode[index].VtRes / 2, self.pixel_format[1], plane2_layer,
                                                index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], tiling, sdimension1,
                                     ddimension1, ddimension1, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[0], out_file0)
            Plane2 = flip.PLANE_INFO(self.source_id[index], plane2_layer, 1, self.pixel_format[1], tiling, sdimension2,
                                     ddimension2, ddimension2, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[1], out_file1)

            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)
        if self.perform_hdr_flip(planes):
            logging.info("Flipped successfully and the Register Verification has passed")

        else:
            self.fail("SDR/HDR two plane flips verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
