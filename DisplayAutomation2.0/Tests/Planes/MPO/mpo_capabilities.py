########################################################################################################################
# @file         mpo_capabilities.py
# @brief        Basic test to verify MPO capabilities. Test will verify maximum number of supported planes by generating
#               RGB and YUV planes.
# @author       Ashok, Sunaina
########################################################################################################################
import logging
import unittest
import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common import mpo_base
from Libs.Core import flip
from Libs.Core.logger import gdhm

##
# @brief    Contains function to check MPO Capabilities
class MPOCapabilities(mpo_base.MPOBase):
    mpo = flip.MPO()

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []
        planes1 = []

        pmpocaps_args_ddrw = flip.MPO_CAPS_ARGS_DDRW(0, 0)
        mpocaps_result = self.mpo.get_mpo_caps(pmpocaps_args_ddrw)
        if mpocaps_result:
            ##
            # Source, destination and clip rectangle.
            rect1 = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

            rect2 = flip.MPO_RECT(0, 0, 1024, 768)

            ##
            # Blend value.
            blend = flip.MPO_BLEND_VAL(0)
            counter_RGB = 0

            # Condition to generate MaxPlanes-1 no of RGB planes and 1 YUV plane
            for index in range(0, pmpocaps_args_ddrw.MaxPlanes - 1):
                plane1 = flip.PLANE_INFO(0, index, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR, rect2, rect2, rect2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
                counter_RGB += 1
                planes.append(plane1)

            plane2 = flip.PLANE_INFO(0, counter_RGB, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR, rect1, rect1, rect1,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
            planes.append(plane2)

            pplanes = flip.PLANE(planes)

            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes)

            ##
            # Condition to generate MaxPlanes-1 no of YUV planes and 1 RGB plane
            plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR, rect1, rect1, rect1,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
            planes1.append(plane1)

            for index in range(1, pmpocaps_args_ddrw.MaxPlanes):
                plane2 = flip.PLANE_INFO(0, index, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR, rect2, rect2, rect2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
                planes1.append(plane2)

            pplanes = flip.PLANE(planes1)

            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes)

        else:
            gdhm.report_bug(
                title="[MPO]Getting MPO capabilities failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Getting MPO capabilities failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test for verification of MPO capabilities")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
