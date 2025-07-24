########################################################################################################################
# @file         mpo_hflip_basic.py
# @brief        Basic test to verify horizontal flip of planes.Test verifies plane programming and also checks
#               for underrun.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 2 planes where 1 plane is of NV12 format and 1 plane is of RGB format.
#                 RGB format represents the desktop and NV12 format represents media content.
#               * Change the tile format to linear.
#               * Submit and verify plane programming.
# @author       Pai, Vinayak1
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Planes.Common.mpo_base import *


##
# @brief    Contains function to flip single or multiple planes
class MPOHFlipBsic(MPOBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []

        ##
        # Pixel format of the plane, which is input from the command line.
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'])))

        ##
        # Color space of the plane, obtained from the input pixel format.
        self.color_space.append(self.get_color_space_for_pixel_format(self.pixel_format[0]))

        ##
        # Tile format of the plane, which is input from the command line.
        self.tile_format.append(getattr(flip.SURFACE_MEMORY_TYPE, ''.join(self.cmd_line_param['INPUT_TILEFORMAT'])))

        ##
        # Source, destination and clip rectangle.
        rect = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        ##
        # Pixel format of base plane.
        pixel_format = flip.SB_PIXELFORMAT.SB_B8G8R8A8

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, pixel_format, self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            plane2 = flip.PLANE_INFO(self.source_id[index], 1, 1, self.pixel_format[0], self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0], stmpo_flip_flag=flip.MPO_FLIP_FLAGS(2))
            planes.append(plane2)
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Basic test to verify horizontal flip of planes.Test verifies plane programming "
                 "and also checks for underrun.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
