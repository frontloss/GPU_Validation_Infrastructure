########################################################################################################################
# @file         conditional_async_flip_sync.py
# @brief        Conditional sync with maximmediateflipline below current scanline
# @author       Jadhav, Anagha A
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Conditional_Async_Flip.conditional_async_base import *
from Tests.Planes.Common import planes_helper


##
# @brief    Contains function to check Conditional sync with maximmediateflipline below current scanline.
class ConditionalSyncFlip(ConditionalAsyncBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []
        mpo_delay_args = []

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
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            if not planes_verification.check_layer_reordering() and self.pixel_format[0] in self.planar_formats:
                plane1_layer = 1
            else:
                plane1_layer = 0

            plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], self.tile_format[0], rect,
                         rect, rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                         self.color_space[0], ulmax_immediate_flipLine=50)

            planes.append(plane1)

        for display in self.connected_list:
            uiScanlineCountOffset = planes_helper.get_scanlinecount_offset(display)
            for i in range(2, 7):
                plane1DelayArgs = flip.MPO_FLIP_DELAY_ARGS(False, True, uiScanLineToWait=self.current_mode.VtRes / i,
                                                           uiScanlineCountOffset=uiScanlineCountOffset,
                                                           uiFrameCountOffset=0)
                mpo_delay_args.append(plane1DelayArgs)
                pplanes = flip.PLANE(planes, stMpoFlipDelayArgs=mpo_delay_args)
                ##
                # Check for the hardware support for the plane parameters and flip the content.
                self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To check Conditional sync with maximmediateflipline below current scanline")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
