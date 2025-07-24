########################################################################################################################
# @file         async_flips_basic.py
# @brief        The basic test to verify async flip functionality through dft.
#               * Create plane parameters for async flips
#               * Submit Async flips.
#               * Verify plane programming.
# @author       Gaikwad, Suraj
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips.AsyncFlips.async_flips_base import *

##
# @brief    Contains function to check whether flips are happening or not
class AsyncFlipsBasic(AsyncFlipsBase):
    NoLayers = [1, 1, 1, 1]


    ##
    # @brief            Unittest runtest function
    # @return           void
    def runTest(self):

        st_mpo_blend = flip.MPO_BLEND_VAL(0)
        if self.cmd_line_param['PIXELFORMAT'] != "NONE":
            self.pixel_format = []
            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['PIXELFORMAT'])))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[0]))

        sdimension = flip.MPO_RECT(0, 0, self.srcList[0][0], self.srcList[0][1])
        ddimension = flip.MPO_RECT(0, 0, self.destList[0][0], self.destList[0][1])
        py_planes = []

        for index in range(0, self.NoOfDisplays):
            plane_1 = flip.PLANE_INFO(self.sourceID[index], 0, 1, self.pixel_format[0], self.tiling, sdimension,
                                      ddimension,
                                      ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, st_mpo_blend,
                                      self.color_space[0], stmpo_plane_in_flag=self.async_flip_flag)
            py_planes.append(plane_1)

        planes = flip.PLANE(py_planes)

        # First flip will be AllParams
        self.performFlip(planes)

        for index in range(0, self.no_of_flips):
            self.performFlip(planes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Generate DFT Async flips')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
