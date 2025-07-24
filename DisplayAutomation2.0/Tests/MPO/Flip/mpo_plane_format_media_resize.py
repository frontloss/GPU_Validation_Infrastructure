########################################################################################################################
# @file         mpo_plane_format_media_resize.py
# @brief        Basic test to verify underruns during resize of plane in YUV422 format.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 2 planes where 1 plane is of YUV422 format and 1 plane is of RGB format.
#                 RGB format represents the desktop and YUV422 format represents media content.
#               * Set the boundary values of the plane based on the resolution obtained by the configuration.
#               * Resize the plane in a given direction, using value given to resize the plane.
#               * Submit flips and verify plane programming.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_base

##
# @brief    Contains function to check underruns during resize of plane in YUV422 format
class MPOPlaneFormatMediaResize(mpo_base.MPOBase):
    display = None

    ##
    # @brief            To perform Flips
    # @param[in]        pplanes; details of planes
    # @return           void
    def perform_flip(self, pplanes):
        ##
        # Check for Multiplane overlay support
        checkmpo_result = self.enable_mpo.check_mpo(pplanes)
        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:

            ##
            # Present the planes on the screen
            ssa_result = self.enable_mpo.set_source_address_mpo(pplanes)
            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:

                logging.info(self.mpo_helper_dft.getStepInfo() + 'Performed flip of 2 planes: YUV_422_PACKED_8_BPC, RGB_8888')
                ##
                # Verify the register programming
                plane1_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_1',
                                                   "source_pixel_format_YUV_422_PACKED_8_BPC",
                                                   "tiled_surface_TILE_Y_LEGACY_MEMORY")

                plane2_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_2',
                                                   "source_pixel_format_RGB_8888",
                                                   "tiled_surface_TILE_Y_LEGACY_MEMORY")

                if not plane1_result or not plane2_result:
                    gdhm.report_bug(
                        title="[MPO][Plane scaling]Plane verification failed: YUV_422_PACKED_8_BPC, RGB_8888",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail('Plane verification failed: YUV_422_PACKED_8_BPC, RGB_8888')

                if self.mpo_helper_dft.verify_watermark() is not True:
                    self.fail('Watermark error observed')

                if self.mpo_helper_dft.verify_underrun():
                    logging.error("Underrun occurred")
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                self.mpo_helper_dft.report_to_gdhm_resource_creation_failure()
                self.fail("Resource creation failed")
            else:
                self.mpo_helper_dft.report_to_gdhm_set_source_address_failure()
                self.fail("Set source address failed")

        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            self.mpo_helper_dft.report_to_gdhm_resource_creation_failure()
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

                rect2 = flip.MPO_RECT(0, 0, 1600, 900)
                blend_value2 = flip.MPO_BLEND_VAL(0)
                plane2 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_YUV422,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2)

                planes.append(plane1)
                planes.append(plane2)

                pplanes = flip.PLANE(planes)

                ##
                # Set the boundary values of the plane based on the resolution obtained by the configuration
                self.mpo_helper_dft.set_bounds(resolution.HzRes, resolution.VtRes)

                self.mpo_helper_dft.source_rect(pplanes.stPlaneInfo[1])

                self.perform_flip(pplanes)

                ##
                # Resize the Bottom, Right of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", 3)):
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", 3)
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", -2)
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", -2)
                    self.perform_flip(pplanes)

                pplanes.stPlaneInfo[1].stMPOSrcRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPODstRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPOClipRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPOSrcRect.lTop = 900
                pplanes.stPlaneInfo[1].stMPODstRect.lTop = 900
                pplanes.stPlaneInfo[1].stMPOClipRect.lTop = 900
                pplanes.stPlaneInfo[1].stMPOSrcRect.lRight = 1920
                pplanes.stPlaneInfo[1].stMPODstRect.lRight = 1920
                pplanes.stPlaneInfo[1].stMPOClipRect.lRight = 1920
                pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom = 1080
                pplanes.stPlaneInfo[1].stMPODstRect.lBottom = 1080
                pplanes.stPlaneInfo[1].stMPOClipRect.lBottom = 1080

                ##
                # Resize the Bottom, Right of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", 3)):
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", 3)
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", -2)
                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", -2)
                    self.perform_flip(pplanes)

                ##
                # Resize the Left, Top of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Left", -8) and self.mpo_helper_dft.resize(
                        pplanes.stPlaneInfo[1], "Top", -8)):
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Left", 6)
                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Top", 6)
                    self.perform_flip(pplanes)

                pplanes.stPlaneInfo[1].stMPOSrcRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPODstRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPOClipRect.lLeft = 1600
                pplanes.stPlaneInfo[1].stMPOSrcRect.lRight = 3200
                pplanes.stPlaneInfo[1].stMPODstRect.lRight = 3200
                pplanes.stPlaneInfo[1].stMPOClipRect.lRight = 3200
                pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom = 1800
                pplanes.stPlaneInfo[1].stMPODstRect.lBottom = 1800
                pplanes.stPlaneInfo[1].stMPOClipRect.lBottom = 1800

                ##
                # Resize the Left, Bottom of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Left", -3)):
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", -3)
                    self.perform_flip(pplanes)

                ##
                # Resize the Bottom, Right of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", 3)):
                    self.perform_flip(pplanes)

                    self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", -3)
                    self.perform_flip(pplanes)
            else:
                self.fail('Failed to apply display configuration %s for display %s'
                          % (DisplayConfigTopology(topology).name, self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips YUV_422_PACKED_8_BPC and RGB planes and  checks for watermark/underrun errors')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
