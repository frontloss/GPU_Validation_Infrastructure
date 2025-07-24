########################################################################################################################
# @file         mpo_plane_disable.py
# @brief        To Validate if programming plane parameters is done only for enabled planes in pipe. Test
#               verifies plane programming and also checks for underrun.
#               * Parse the command line.
#               * Apply specific pixel format and fill plane parameters for two planes.
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Disable the RGB plane, so that only NV12 plane is active
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Enable the RGB plane, Both planes will be active
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Sunaina Ashok
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip
from Tests.Planes.Common import mpo_base


##
# @brief    Contains function to flip three planes of specified formats with one plane disabled
class MPOPlanesDisable(mpo_base.MPOBase):
    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []

        ##
        # Pixel format of the plane, which is input from the command line.
        for i in range(0, len(self.cmd_line_param['INPUT_PIXELFORMAT'])):
            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'][i])))
            self.color_space.append(self.get_color_space_for_pixel_format(self.pixel_format[i]))

        ##
        # Tile format of the plane, which is input from the command line.
        for i in range(0, len(self.cmd_line_param['INPUT_TILEFORMAT'])):
            self.tile_format.append(
                getattr(flip.SURFACE_MEMORY_TYPE, ''.join(self.cmd_line_param['INPUT_TILEFORMAT'][i])))

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
        # Fill plane parameters for RGB plane
        for index in range(0, self.no_of_displays):
            plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, pixel_format, self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Fill plane parameters for NV12 plane
        for index in range(0, self.no_of_displays):
            plane2 = flip.PLANE_INFO(self.source_id[index], 1, 1, self.pixel_format[0], self.tile_format[0], rect,
                                     rect, rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            planes.append(plane2)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Disable the RGB plane, NV12 plane is active here
        for index in range(0, self.no_of_displays):
            pplanes.stPlaneInfo[index].bEnabled = 0

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Enable the RGB plane, Both planes are active
        for index in range(0, self.no_of_displays):
            pplanes.stPlaneInfo[index].bEnabled = 1

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To Validate if programming plane parameters is done only for enabled planes in pipe." 
    "Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)