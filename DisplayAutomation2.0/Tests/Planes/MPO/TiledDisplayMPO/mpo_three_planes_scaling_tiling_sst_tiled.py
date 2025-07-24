########################################################################################################################
# @file         mpo_three_planes_scaling_tiling_sst_tiled.py
# @brief        Basic test to flip three planes of specified formats on tiled display and perform plane scaling and tile
#               switch. Test verifies plane programming and also checks for underrun.
#               * Parse the command line.
#               * Fill plane parameters based on command line arguments for three planes.
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Get the source and destination dimensions of the plane.
#               * Perform scaling.
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Change the tile format to X and linear for all planes and flip the content.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import flip
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common import mpo_tiled_sst_base

##
# @brief    Contains function to flip three planes of specified formats on tiled display, perform plane scaling and tile switch
class MPOThreePlanesScalingTilingSSTTiled(mpo_tiled_sst_base.MPOTiledBaseSST):


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
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            plane1 = flip.PLANE_INFO(0, 0, 1, pixel_format, self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            plane2 = flip.PLANE_INFO(0, 1, 1, self.pixel_format[0], self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            plane3 = flip.PLANE_INFO(0, 2, 1, self.pixel_format[1], self.tile_format[1], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[1])
            planes.append(plane3)
            planes.append(plane2)
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Source dimension of the plane.
        for sdimension in self.src_list:
            src_dimension = flip.MPO_RECT(0, 0, sdimension[0], sdimension[1])

            ##
            # Destination dimension of the plane.
            for ddimension in self.dst_list:
                dst_dimension = flip.MPO_RECT(0, 0, ddimension[0], ddimension[1])

                ##
                # Perform scaling.
                for index in range(0, pplanes.uiPlaneCount):
                    if pplanes.stPlaneInfo[index].uiLayerIndex == 1:
                        pplanes.stPlaneInfo[index].stMPOSrcRect = src_dimension
                        pplanes.stPlaneInfo[index].stMPODstRect = dst_dimension
                        pplanes.stPlaneInfo[index].stMPOClipRect = dst_dimension

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)

                ##
                # Change the tile format of all the planes to X tile.
                for index in range(0, pplanes.uiPlaneCount):
                    pplanes.stPlaneInfo[index].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)

                ##
                # Change the tile format of all the planes to linear.
                for index in range(0, pplanes.uiPlaneCount):
                    pplanes.stPlaneInfo[index].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)

                ##
                # Perform scaling.
                for index in range(0, pplanes.uiPlaneCount):
                    if pplanes.stPlaneInfo[index].uiLayerIndex == 2:
                        pplanes.stPlaneInfo[index].stMPOSrcRect = src_dimension
                        pplanes.stPlaneInfo[index].stMPODstRect = dst_dimension
                        pplanes.stPlaneInfo[index].stMPOClipRect = dst_dimension

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)

                ##
                # Change the tile format of all the planes to X tile.
                for index in range(0, pplanes.uiPlaneCount):
                    pplanes.stPlaneInfo[index].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)

                ##
                # Change the tile format of all the planes to linear.
                for index in range(0, pplanes.uiPlaneCount):
                    pplanes.stPlaneInfo[index].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip three planes of specified formats on tiled display and perform "
                 "plane scaling and tile switch. Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)