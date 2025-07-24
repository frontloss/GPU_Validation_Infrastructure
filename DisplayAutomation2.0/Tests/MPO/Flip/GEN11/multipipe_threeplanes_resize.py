########################################################################################################################
# @file         multipipe_threeplanes_resize.py
# @brief        This script contains test to verify flips on 3 planes on multiple displays with different sizes
# @author       Shetty, Anjali N
########################################################################################################################
import time

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO.Flip.GEN11.mpo_base import *

##
# @brief    Contains test to verify flips on 3 planes on multiple displays with different sizes
class Test_ThreePlanesMPO(MPOBase):
    NoLayers = [3, 3, 3, 3]

    ##
    # @brief            Unittest runTest function
    # @return           None
    def runTest(self):
        # Test_ThreePlanesMPO.format1 = sys.argv.pop()
        # Test_ThreePlanesMPO.format2 = sys.argv.pop()
        count = [0, 0]
        stMPOBlend = flip.MPO_BLEND_VAL(0)
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'][0])))
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'][1])))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[0]))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[1]))
        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
        sdimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        ddimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        dwmpixelFormat = flip.SB_PIXELFORMAT.SB_B8G8R8A8
        dwmdimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        dwmcolorspace = self.getColorSpaceForPixelFormat(dwmpixelFormat)
        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            Plane1 = flip.PLANE_INFO(self.sourceID[index], 2, 1, self.pixel_format[0], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0])
            Plane2 = flip.PLANE_INFO(self.sourceID[index], 1, 1, self.pixel_format[1], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[1])
            Plane3 = flip.PLANE_INFO(self.sourceID[index], 0, 1, dwmpixelFormat, tiling, dwmdimension, dwmdimension,
                                     dwmdimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     dwmcolorspace)
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)
            pyPlanes.append(Plane3)

        planes = flip.PLANE(pyPlanes)
        rightFactor = self.current_mode.HzRes // 20
        bottomFactor = self.current_mode.VtRes // 20

        for index1 in range(1, 20):
            # upscaling
            self.performFlip(planes)
            time.sleep(5)
            for index in range(0, planes.uiPlaneCount):
                if (index % 3 == 0):
                    planes.stPlaneInfo[index].stMPODstRect.lRight += rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lBottom += bottomFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lRight += rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lBottom += bottomFactor
                elif (index % 3 == 1):
                    planes.stPlaneInfo[index].stMPODstRect.lLeft += rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lTop += bottomFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lLeft += rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lTop += bottomFactor
        rightFactor = self.current_mode.HzRes // 20
        bottomFactor = self.current_mode.VtRes // 20
        for index1 in range(1, 15):
            self.performFlip(planes)
            time.sleep(5)
            for index in range(0, planes.uiPlaneCount):
                if (index % 3 == 0):
                    planes.stPlaneInfo[index].stMPODstRect.lRight -= rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lBottom -= bottomFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lRight -= rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lBottom -= bottomFactor
                elif (index % 3 == 1):
                    planes.stPlaneInfo[index].stMPODstRect.lLeft -= rightFactor
                    planes.stPlaneInfo[index].stMPODstRect.lTop -= bottomFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lLeft -= rightFactor
                    planes.stPlaneInfo[index].stMPOClipRect.lTop -= bottomFactor


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips 3 planes on multiple displays with different sizes'
                 ' and checks for flickr/corruption')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
