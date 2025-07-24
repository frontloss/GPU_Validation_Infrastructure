########################################################################################################################
# @file         multipipe_twoplanes_resize.py
# @brief        This script contains test to verify flips on 2 planes on multiple displays with different sizes
# @author       Shetty, Anjali N
########################################################################################################################
import time

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
        sdimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        ddimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
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

        rightFactor = self.current_mode.HzRes // 10
        bottomFactor = self.current_mode.VtRes // 10
        for index1 in range(1, 10):
            self.performFlip(planes)

            time.sleep(5)
            for index in range(0, planes.uiPlaneCount):
                if (index % 2 == 0):
                    planes.stPlaneInfo[index].stMPODstRect.lRight += rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lBottom += bottomFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lRight += rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lBottom += bottomFactor

        rightFactor = self.current_mode.HzRes // 10
        bottomFactor = self.current_mode.VtRes // 10
        for index1 in range(1, 10):
            self.performFlip(planes)

            time.sleep(5)
            for index in range(0, planes.uiPlaneCount):
                if (index % 2 == 0):
                    planes.stPlaneInfo[index].stMPODstRect.lRight -= rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lBottom -= bottomFactor

                    planes.stPlaneInfo[index].stMPOClipRect.lRight -= rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lBottom -= bottomFactor


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips 2 planes on multiple displays with different sizes'
                 ' and checks for flickr/corruption')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
