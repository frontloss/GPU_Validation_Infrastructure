########################################################################################################################
# @file         multipipe_twoplanes_scaling.py
# @brief        This script contains test to verify flips on 2 planes on multiple displays with different sizes
# @author       Shetty, Anjali N
########################################################################################################################
import random

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO.Flip.GEN11.mpo_base import *

##
# @brief    Contains test to verify flips on 2 planes on multiple displays with different sizes
class Test_TwoPlanesMPO(MPOBase):
    NoLayers = [2, 2, 2, 2]

    ##
    # @brief            Unittest runTest function
    # @return           None
    def runTest(self):
        # Test_TwoPlanesMPO.format = sys.argv.pop()
        count = [0, 0]
        stMPOBlend = flip.MPO_BLEND_VAL(0)
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'])))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[0]))
        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
        sdimension = flip.MPO_RECT(0, 0, self.srcList[0][0], self.srcList[0][1])
        ddimension = flip.MPO_RECT(0, 0, self.destList[0][0], self.destList[0][1])
        dwmpixelFormat = flip.SB_PIXELFORMAT.SB_B8G8R8A8
        dwmdimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        dwmcolorspace = self.getColorSpaceForPixelFormat(dwmpixelFormat)
        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            Plane1 = flip.PLANE_INFO(self.sourceID[index], 1, 1, self.pixel_format[0], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0])
            Plane2 = flip.PLANE_INFO(self.sourceID[index], 0, 1, dwmpixelFormat, tiling, dwmdimension, dwmdimension,
                                     dwmdimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     dwmcolorspace)
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)

        planes = flip.PLANE(pyPlanes)

        for dimension in self.srcList:
            srcdimension = flip.MPO_RECT(0, 0, dimension[0], dimension[1])
            count[0] += 1
            count[1] = 0
            for dimension1 in self.destList:
                destdimension = flip.MPO_RECT(0, 0, dimension1[0], dimension1[1])
                count[1] += 1

                for index in range(0, self.NoOfDisplays):
                    for index in range(0, planes.uiPlaneCount):
                        if (index % 2 == 0):
                            planes.stPlaneInfo[index].stMPOSrcRect = srcdimension
                            planes.stPlaneInfo[index].stMPODstRect = destdimension
                            planes.stPlaneInfo[index].stMPOClipRect = destdimension

                self.performFlip(planes)
                top = random.randint(100, 300)
                left = random.randint(100, 500)
                logging.info(self.getStepInfo() + "Changing position from 0,0 to %d,%d ", top, left)
                for index in range(0, self.NoOfDisplays):
                    for index in range(0, planes.uiPlaneCount):
                        if (index % 2 == 0):
                            planes.stPlaneInfo[index].stMPODstRect.lTop = top
                            planes.stPlaneInfo[index].stMPODstRect.lLeft = left
                            planes.stPlaneInfo[index].stMPOClipRect.lTop = top
                            planes.stPlaneInfo[index].stMPOClipRect.lLeft = left
                self.performFlip(planes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips 2 planes on multiple displays with different sizes'
                 ' and checks for flickr/corruption')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
