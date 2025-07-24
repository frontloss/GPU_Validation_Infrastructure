########################################################################################################################
# @file         mpo_ma_two_planes_scaling.py
# @brief        Basic test to flip two planes of specified formats on each display across multiple adapters and perform
#               plane scaling. Test verifies plane programming and also checks for underrun.
#               * Parse the command line.
#               * Fill plane parameters based on command line arguments for two plane.
#               * Check for the hardware support for the plane parameters and flip the content.
#               * Get the source and destination dimensions of the plane.
#               * Perform scaling.
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Shetty, Anjali N
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Planes.Common.mpo_ma_base import *

##
# @brief     Contains function to flip two planes of specified formats on each display and perform plane scaling
class MPOMATwoPlanesScaling(MPOMABase):


    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []
        pplanes = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if key == 'INPUT_PIXELFORMAT':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            ##
                            # Pixel format of the plane, which is input from the command line.
                            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(value[i])))

                            ##
                            # Color space of the plane, obtained from the input pixel format.
                            self.color_space.append(self.get_color_space_for_pixel_format(self.pixel_format[i]))
                    else:
                        for i in range(0, len(self.display_details)):
                            ##
                            # Pixel format of the plane, which is input from the command line.
                            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(value[0])))

                            ##
                            # Color space of the plane, obtained from the input pixel format.
                            self.color_space.append(self.get_color_space_for_pixel_format(self.pixel_format[0]))

                if key == 'INPUT_TILEFORMAT':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            ##
                            # Tile format of the plane, which is input from the command line.
                            self.tile_format.append(getattr(flip.SURFACE_MEMORY_TYPE, ''.join(value[i])))
                    else:
                        for i in range(0, len(self.display_details)):
                            ##
                            # Tile format of the plane, which is input from the command line.
                            self.tile_format.append(getattr(flip.SURFACE_MEMORY_TYPE, ''.join(value[0])))

        ##
        # Pixel format of base plane.
        pixel_format = flip.SB_PIXELFORMAT.SB_B8G8R8A8

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Fill plane parameters.
        for key, value in self.display_details.items():
            planes.append([])
            index = list(self.display_details).index(key)
            rect = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            for source_id in range(0, len(value)):
                plane1 = flip.PLANE_INFO(source_id, 0, 1, pixel_format, self.tile_format[index], rect, rect,
                                         rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                         self.color_space[index])
                plane2 = flip.PLANE_INFO(source_id, 1, 1, self.pixel_format[index], self.tile_format[index], rect, rect,
                                         rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                         self.color_space[index])
                planes[index].append(plane1)
                planes[index].append(plane2)

            pplanes.insert(index, flip.PLANE(planes[index]))

            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes[index], key.lower())

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
                for key, value in self.display_details.items():
                    adapter_index = list(self.display_details).index(key)
                    for index in range(0, pplanes[adapter_index].uiPlaneCount):
                        if pplanes[adapter_index].stPlaneInfo[index].uiLayerIndex == 1:
                            pplanes[adapter_index].stPlaneInfo[index].stMPOSrcRect = src_dimension
                            pplanes[adapter_index].stPlaneInfo[index].stMPODstRect = dst_dimension
                            pplanes[adapter_index].stPlaneInfo[index].stMPOClipRect = dst_dimension

                    ##
                    # Check for the hardware support for the plane parameters and flip the content.
                    self.perform_flip(pplanes[adapter_index], key.lower())


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip two planes of specified formats on each display across multiple adapters "
                 "and perform plane scaling. Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
