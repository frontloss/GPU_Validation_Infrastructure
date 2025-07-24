########################################################################################################################
# @file         mpo_two_planes_resize_odd.py
# @brief        To flip single or multiple planes on single or multiple displays and perform plane pixel and tile format
#               switching. Test verifies plane programming and also checks for underrun.
#               * Parse the command line.
#               * Apply specific pixel format and fill plane parameters for two planes.
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Set the boundary based on the resolution obtained.
#               * Perform resize.
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Pai, Vinayak1
########################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Planes.Common.mpo_base import *


##
# @brief    Contains function to flip single or multiple planes, perform plane pixel and tile format switching
class MPOTwoPlanesResize(MPOBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []
        result = True

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
                                     self.color_space[0])
            planes.append(plane2)
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Set the boundary values of the plane based on the resolution obtained by the configuration
        self.set_bounds(self.current_mode.HzRes, self.current_mode.VtRes)

        self.source_rect(pplanes.stPlaneInfo[0])

        while result:
            for index in range(0, pplanes.uiPlaneCount):
                if pplanes.stPlaneInfo[index].uiLayerIndex == 1:
                    ##
                    # Resize the Right, Bottom of the plane
                    result = self.resize(pplanes.stPlaneInfo[index], "Right", -35) and \
                             self.resize(pplanes.stPlaneInfo[index], "Bottom", -35)
                    if result:
                        ##
                        # Check for the hardware support for the plane parameters and flip the content.
                        self.perform_flip(pplanes)

        result = True

        while result:
            for index in range(0, pplanes.uiPlaneCount):
                if pplanes.stPlaneInfo[index].uiLayerIndex == 1:
                    ##
                    # Resize the Right, Bottom of the plane
                    result = self.resize(pplanes.stPlaneInfo[index], "Right", 35) and \
                             self.resize(pplanes.stPlaneInfo[index], "Bottom", 35)
                    if result:
                        ##
                        # Check for the hardware support for the plane parameters and flip the content.
                        self.perform_flip(pplanes)

        result = True

        while result:
            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes)
            for index in range(0, pplanes.uiPlaneCount):
                if pplanes.stPlaneInfo[index].uiLayerIndex == 1:
                    ##
                    # Resize the Left, Top of the plane
                    result = self.resize(pplanes.stPlaneInfo[index], "Left", 35) and \
                             self.resize(pplanes.stPlaneInfo[index], "Top", 35)

                    if result:
                        ##
                        # Check for the hardware support for the plane parameters and flip the content.
                        self.perform_flip(pplanes)

        result = True

        while result:
            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes)
            for index in range(0, pplanes.uiPlaneCount):
                if pplanes.stPlaneInfo[index].uiLayerIndex == 1:
                    ##
                    # Resize the Left, Top of the plane
                    result = self.resize(pplanes.stPlaneInfo[index], "Left", 35) and \
                             self.resize(pplanes.stPlaneInfo[index], "Top", 35)

                    if result:
                        ##
                        # Check for the hardware support for the plane parameters and flip the content.
                        self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip two planes of specified formats on single or multiple displays and perform "
                 "plane resize. Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)