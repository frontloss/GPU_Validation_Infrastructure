########################################################################################################################
# @file         async_flips_min_dbuf_check.py
# @brief        This script contains test to flip two planes (sync and async) of specified formats on single or multiple
#               displays and perform check for min dbuf allocation for async flips. Test verifies plane programming and
#               also checks for underrun.
# @author       Gaikwad, Suraj
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import flip
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_watermark import watermark_base, watermark_utils, watermark
from Tests.Planes.Common.mpo_base import MPOBase

##
# NOTE: This test is applicable for Gen13+ platforms only

##
# @brief    Contains function to flip two planes on single or multiple displays and perform check for min dbuf
#           allocation for async flips
class AsyncFlipsMinDbufCheck(MPOBase):

    async_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x2)
    wm_base_obj = watermark_base.DisplayWatermarkBase()
    wm_obj = watermark.DisplayWatermark()
    gen_wm_obj = wm_obj._DisplayWatermark__get_wm_obj()     # Get WM Object based on current platform gen
    max_planes = gen_wm_obj.max_planes
    max_pipes = gen_wm_obj.max_pipes
    planes_list = gen_wm_obj.get_plane_params(max_pipes, max_planes)

    ##
    # @brief     Unittest runTest function
    # @return    None
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
        src_rect = flip.MPO_RECT(0, 0, self.src_list[0][0], self.src_list[0][1])
        dest_rect = flip.MPO_RECT(0, 0, self.dest_list[0][0], self.dest_list[0][1])

        ##
        # Pixel format of base plane.
        pixel_format = flip.SB_PIXELFORMAT.SB_B8G8R8A8

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            # Sync flips plane
            plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, pixel_format, self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            # Async flips plane
            plane2 = flip.PLANE_INFO(self.source_id[index], 1, 1, self.pixel_format[0], self.tile_format[0],
                                     src_rect, dest_rect, dest_rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     blend, self.color_space[0], stmpo_plane_in_flag=self.async_flip_flag)
            planes.append(plane2)
            planes.append(plane1)

        pplanes = flip.PLANE(planes)

        # First flip will be AllParams for Async flip plane
        self.perform_flip(pplanes)

        # Perform flips and check for Min Dbuf restriction on Async flips
        for index in range(0, 10):
            self.perform_flip(pplanes)

            # Test applicable for Gen13+ platforms only
            if not (watermark_utils.platform in watermark_utils.GEN9_PLATFORMS or
                    watermark_utils.platform in watermark_utils.GEN10_PLATFORMS or
                    watermark_utils.platform in watermark_utils.GEN11_PLATFORMS):
                if self.gen_wm_obj.check_min_dbuf_needed(self.planes_list, self.max_planes, self.max_pipes,
                                                         is_async_flip_check=True) is False:
                    self.fail("Minimum DBUF not allocated for Async flips plane")
                else:
                    logging.info("Minimum DBUF allocated for Async flips plane")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip two planes (sync and async) of specified formats on single or multiple "
                 "displays and perform check for min dbuf allocation for async flips.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
