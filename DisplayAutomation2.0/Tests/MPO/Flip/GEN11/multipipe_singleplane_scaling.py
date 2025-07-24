########################################################################################################################
# @file         multipipe_singleplane_scaling.py
# @brief        This script contains test to verify flips on a single plane on multiple displays
# @author       Shetty, Anjali N
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO.Flip.GEN11.mpo_base import *


##
# @brief    Contains test to verify flips on a single plane on multiple displays
class Test_SinglePlaneMPO(MPOBase):
    NoLayers = [1, 1, 1, 1]

    ##
    # @brief            Unittest runTest function
    # @return           None
    def runTest(self):
        # Test_SinglePlaneMPO.format = sys.argv.pop()
        count = [0, 0]
        stMPOBlend = flip.MPO_BLEND_VAL(0)
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'])))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[0]))
        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
        sdimension = flip.MPO_RECT(0, 0, self.srcList[0][0], self.srcList[0][1])
        ddimension = flip.MPO_RECT(0, 0, self.destList[0][0], self.destList[0][1])
        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            Plane1 = flip.PLANE_INFO(self.sourceID[index], 0, 1, self.pixel_format[0], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0])
            pyPlanes.append(Plane1)

        planes = flip.PLANE(pyPlanes)

        for dimension in self.srcList:
            srcdimension = flip.MPO_RECT(0, 0, dimension[0], dimension[1])

            for dimension1 in self.destList:
                destdimension = flip.MPO_RECT(0, 0, dimension1[0], dimension1[1])
                for index in range(0, planes.uiPlaneCount):
                    planes.stPlaneInfo[index].stMPOSrcRect = srcdimension
                    planes.stPlaneInfo[index].stMPODstRect = destdimension
                    planes.stPlaneInfo[index].stMPOClipRect = destdimension

                self.performFlip(planes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips a single plane on multiple displays and checks for flickr/corruption')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
