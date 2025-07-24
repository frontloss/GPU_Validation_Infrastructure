########################################################################################################################
# @file         hflip_basic.py
# @brief        Basic test to verify horizontal flip of planes.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 2 planes where 1 plane is of NV12 format and 1 plane is of RGB format.
#                 RGB format represents the desktop and NV12 format represents media content.
#               * Apply different resolutions to the planes to check for scaling of the plane
#               * Change the tile format to X, linear and Y.
#               * Submit and verify plane programming.
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_base
from Libs.Core import flip
from Libs.Core.logger import gdhm

##
# @brief    Contains function to check horizontal flip of planes
class HFlip(mpo_base.MPOBase):
    display = None


    ##
    # @brief            To perform Flips
    # @param[in]        pplanes; details of planes
    # @param[in]        tile_format
    # @return           void
    def perform_flip(self, pplanes, tile_format):
        ##
        # Check for Multiplane overlay support
        checkmpo_result = self.enable_mpo.check_mpo(pplanes)
        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:

            ##
            # Present the planes on the screen
            ssa_result = self.enable_mpo.set_source_address_mpo(pplanes)
            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:

                logging.info(self.mpo_helper_dft.getStepInfo() + 'Performed flip of 2 planes: NV12_YUV_420 (with hflip), RGB_8888')
                ##
                # Verify the register programming
                plane1_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_1',
                                                   "source_pixel_format_NV12_YUV_420",
                                                   tile_format, True)
                plane2_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_2',
                                                   "source_pixel_format_RGB_8888",
                                                   tile_format)
                if not plane1_result or not plane2_result:
                    gdhm.report_bug(
                        title="[MPO][HFlip]Plane verification failed: NV12_YUV_420 (with hflip), RGB_8888",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail('Plane verification failed: NV12_YUV_420 (with hflip), RGB_8888')

                if self.mpo_helper_dft.verify_watermark() is not True:
                    self.fail('Watermark error observed')

                if self.mpo_helper_dft.verify_underrun():
                    logging.error("Underrun occurred")
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm.report_bug(
                    title="[MPO][HFlip]Resource creation failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Resource creation failed")
            else:
                gdhm.report_bug(
                    title="[MPO][HFlip]Set source address failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Set source address failed")

        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm.report_bug(
                title="[MPO][HFlip]Resource creation failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Resource creation failed")
        else:
            logging.info("Driver did not meet the requirements")


    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # Apply SINGLE display configuration across all the displays
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(self.mpo_helper_dft.getStepInfo() + 'Applied display configuration %s for display %s' % (
                    DisplayConfigTopology(topology).name, self.connected_list[display_index]))
                self.display = self.connected_list[display_index]

                ##
                # Get the display configuration
                target_id = self.config.get_target_id(self.connected_list[display_index], self.enumerated_displays)
                resolution = self.config.get_current_mode(target_id)

                planes = []

                rect1 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
                blend_value1 = flip.MPO_BLEND_VAL(1)
                plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect1, rect1, rect1,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value1)

                rect2 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
                blend_value2 = flip.MPO_BLEND_VAL(0)
                plane2 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2,
                                         stmpo_flip_flag=flip.MPO_FLIP_FLAGS(2))

                planes.append(plane1)
                planes.append(plane2)

                pplanes = flip.PLANE(planes)

                self.perform_flip(pplanes, "tiled_surface_TILE_Y_LEGACY_MEMORY")

                ##
                # Different resolutions of the screen
                plane_resolutions = [(3840, 2160), (3200, 1800), (2560, 1440), (1920, 1080), (1600, 900), (800, 600)]

                ##
                # Apply different resolutions to the planes to check for scaling of the plane
                for plane0_hres, plane0_vres in plane_resolutions:
                    pplanes.stPlaneInfo[0].stMPOSrcRect.lRight = plane0_hres
                    pplanes.stPlaneInfo[0].stMPOSrcRect.lBottom = plane0_vres
                    pplanes.stPlaneInfo[0].stMPODstRect.lRight = plane0_hres
                    pplanes.stPlaneInfo[0].stMPODstRect.lBottom = plane0_vres
                    pplanes.stPlaneInfo[0].stMPOClipRect.lRight = plane0_hres
                    pplanes.stPlaneInfo[0].stMPOClipRect.lBottom = plane0_vres
                    for plane1_src_hres, plane1_src_vres in plane_resolutions:
                        pplanes.stPlaneInfo[1].stMPOSrcRect.lRight = plane1_src_hres
                        pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom = plane1_src_vres
                        for dst_hres, dst_vres in plane_resolutions:
                            pplanes.stPlaneInfo[1].stMPODstRect.lRight = dst_hres
                            pplanes.stPlaneInfo[1].stMPOClipRect.lRight = dst_hres
                            pplanes.stPlaneInfo[1].stMPODstRect.lBottom = dst_vres
                            pplanes.stPlaneInfo[1].stMPOClipRect.lBottom = dst_vres

                            ##
                            # Change the tile format
                            pplanes.stPlaneInfo[
                                0].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
                            pplanes.stPlaneInfo[
                                1].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED

                            self.perform_flip(pplanes, "tiled_surface_TILE_Y_LEGACY_MEMORY")

                            ##
                            # Change the tile format
                            pplanes.stPlaneInfo[0].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED
                            pplanes.stPlaneInfo[1].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED

                            self.perform_flip(pplanes, "tiled_surface_TILE_X_MEMORY")

                            ##
                            # Change the tile format
                            pplanes.stPlaneInfo[0].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
                            pplanes.stPlaneInfo[1].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

                            self.perform_flip(pplanes, "tiled_surface_LINEAR_MEMORY")
            else:
                self.fail('Failed to apply display configuration %s for display %s'
                          % (DisplayConfigTopology(topology).name, self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips NV12_YUV_420 and RGB planes and checks for horizontal support of planes')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
