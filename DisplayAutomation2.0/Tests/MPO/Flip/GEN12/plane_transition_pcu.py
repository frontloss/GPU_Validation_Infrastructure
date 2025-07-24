########################################################################################################################
# @file         plane_transition_pcu.py
# @brief        This script consists of unittest runTest function which is used to make transisition on planes
# @author       Shetty, Anjali N
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO.Flip.GEN11.mpo_base import *

##
# @brief    Contains unititest runTest function to make transisition on planes
class PlaneTransition(MPOBase):
    NoLayers = [3, 3, 3, 3]

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        # self.format1 = sys.argv.pop()
        # self.format2 = sys.argv.pop()

        stMPOBlend = flip.MPO_BLEND_VAL(0)
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'][0])))
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'][1])))

        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[0]))
        self.color_space.append(self.getColorSpaceForPixelFormat(self.pixel_format[1]))
        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED

        sdimension = flip.MPO_RECT(0, 0, self.srcList[0][0], self.srcList[0][1])
        ddimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        dwmpixelFormat = flip.SB_PIXELFORMAT.SB_B8G8R8A8
        dwmdimension = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        dwmcolorspace = self.getColorSpaceForPixelFormat(dwmpixelFormat)

        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            Plane1 = flip.PLANE_INFO(self.sourceID[index], 2, 0, self.pixel_format[0], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[0])
            Plane2 = flip.PLANE_INFO(self.sourceID[index], 1, 0, self.pixel_format[1], tiling, sdimension, ddimension,
                                     ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     self.color_space[1])
            Plane3 = flip.PLANE_INFO(self.sourceID[index], 0, 1, dwmpixelFormat, tiling, dwmdimension, dwmdimension,
                                     dwmdimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                     dwmcolorspace)
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)
            pyPlanes.append(Plane3)

        planes = flip.PLANE(pyPlanes)

        for src_dimension in self.srcList:

            planes.stPlaneInfo[0].MPOSrcRect = flip.MPO_RECT(0, 0, src_dimension[0], src_dimension[1])
            planes.stPlaneInfo[1].MPOSrcRect = flip.MPO_RECT(0, 0, src_dimension[0], src_dimension[1])

            self.performFlip(planes)

            planes.stPlaneInfo[0].bEnabled = 0
            planes.stPlaneInfo[1].bEnabled = 0

            for src_dimension in self.srcList:
                planes.stPlaneInfo[0].MPOSrcRect = flip.MPO_RECT(0, 0, src_dimension[0], src_dimension[1])
                planes.stPlaneInfo[1].MPOSrcRect = flip.MPO_RECT(0, 0, src_dimension[0], src_dimension[1])

                self.performFlip(planes)

                planes.stPlaneInfo[0].bEnabled = 1
                planes.stPlaneInfo[1].bEnabled = 1

                self.performFlip(planes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
