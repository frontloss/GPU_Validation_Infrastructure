########################################################################################################################
# @file         mpo_min_planesize.py
# @brief        Test to verify minimum plane size. Test fails if there is check MPO failure.
#               * Parse the command line.
#               * Fill plane parameters.
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Ashok, Sunaina
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common.mpo_base import *

##
# @brief    Contains function to check minimum plane size
class MPOMinPlanesize(MPOBase):

    ##
    # @brief            To get minimum plane size
    # @param[in]        pixel_format; expected pixel format
    # @return           minimum plane size
    def minimum_plane_size(self, pixel_format):
        return {
            flip.SB_PIXELFORMAT.SB_B8G8R8X8: 4,
            flip.SB_PIXELFORMAT.SB_B8G8R8A8: 4,
            flip.SB_PIXELFORMAT.SB_R8G8B8A8: 4,
            flip.SB_PIXELFORMAT.SB_R8G8B8X8: 4,
            flip.SB_PIXELFORMAT.SB_R10G10B10X2: 4,
            flip.SB_PIXELFORMAT.SB_R10G10B10A2: 4,
            flip.SB_PIXELFORMAT.SB_B10G10R10X2: 4,
            flip.SB_PIXELFORMAT.SB_B10G10R10A2: 4,
            flip.SB_PIXELFORMAT.SB_R16G16B16X16F: 2,
            flip.SB_PIXELFORMAT.SB_R16G16B16A16F: 2,
            flip.SB_PIXELFORMAT.SB_YUV422: 8,
            flip.SB_PIXELFORMAT.SB_P010YUV420: 8,
            flip.SB_PIXELFORMAT.SB_P012YUV420: 8,
            flip.SB_PIXELFORMAT.SB_P016YUV420: 8,
            flip.SB_PIXELFORMAT.SB_NV12YUV420: 16,
            flip.SB_PIXELFORMAT.SB_YUV422_12: 4,
            flip.SB_PIXELFORMAT.SB_YUV422_16: 4,
            flip.SB_PIXELFORMAT.SB_YUV444_8: 4,
            flip.SB_PIXELFORMAT.SB_YUV444_16: 2
        }[pixel_format]

    ##
    # @brief            To get minimum plane size WA
    # @param[in]        pixel_format; expected pixel format
    # @return           minimum plane size
    def minimum_plane_size_WA(self, pixel_format):
        return {
            flip.SB_PIXELFORMAT.SB_B8G8R8X8: 6,
            flip.SB_PIXELFORMAT.SB_B8G8R8A8: 6,
            flip.SB_PIXELFORMAT.SB_R8G8B8A8: 6,
            flip.SB_PIXELFORMAT.SB_R8G8B8X8: 6,
            flip.SB_PIXELFORMAT.SB_R10G10B10X2: 6,
            flip.SB_PIXELFORMAT.SB_R10G10B10A2: 6,
            flip.SB_PIXELFORMAT.SB_B10G10R10X2: 6,
            flip.SB_PIXELFORMAT.SB_B10G10R10A2: 6,
            flip.SB_PIXELFORMAT.SB_R16G16B16X16F: 4,
            flip.SB_PIXELFORMAT.SB_R16G16B16A16F: 4,
            flip.SB_PIXELFORMAT.SB_YUV422: 10,
            flip.SB_PIXELFORMAT.SB_P010YUV420: 12,
            flip.SB_PIXELFORMAT.SB_P012YUV420: 12,
            flip.SB_PIXELFORMAT.SB_P016YUV420: 12,
            flip.SB_PIXELFORMAT.SB_NV12YUV420: 20,
            flip.SB_PIXELFORMAT.SB_YUV422_12: 6,
            flip.SB_PIXELFORMAT.SB_YUV422_16: 6,
            flip.SB_PIXELFORMAT.SB_YUV444_8: 6,
            flip.SB_PIXELFORMAT.SB_YUV444_16: 4
        }[pixel_format]

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
        rect = flip.MPO_RECT(0, 0, self.minimum_plane_size(self.pixel_format[0]), self.current_mode.VtRes)

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)
        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, self.pixel_format[0], self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)

        ##
        # Source, destination and clip rectangle.
        rect = flip.MPO_RECT(0, 0, self.minimum_plane_size_WA(self.pixel_format[0]), self.current_mode.VtRes)

        ##
        # Fill plane parameters with source, destination and clip rectangle.
        for index in range(0, pplanes.uiPlaneCount):
            pplanes.stPlaneInfo[index].stMPOSrcRect = rect
            pplanes.stPlaneInfo[index].stMPODstRect = rect
            pplanes.stPlaneInfo[index].stMPOClipRect = rect

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test for verification of minimum plane size")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
