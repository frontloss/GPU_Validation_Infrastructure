########################################################################################################################
# @file         mpo_plane_format_media_youtube_resize.py
# @brief        Basic test to verify underruns during resize of plane in NV12 format.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 2 planes where 2 planes are of NV12 format.
#                 NV12 format represents media content and youtube playback.
#               * Set the boundary values of the plane based on the resolution obtained by the configuration.
#               * Resize the plane in a given direction, using the value given to resize the plane.
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
# @brief    Contains function to check underruns during resize of plane in NV12 format
class MPOPlaneFormatMediaYouTubeResize(mpo_base.MPOBase):

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
                logging.info(self.mpo_helper_dft.getStepInfo() + 'Performed flip of 2 planes: NV12_YUV_420, NV12_YUV_420')

                ##
                # Verify the register programming
                for display in range(len(self.connected_list)):
                    ##
                    # Verify the register programming
                    plane1_result = self.mpo_helper_dft.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                                       "source_pixel_format_NV12_YUV_420",
                                                       "tiled_surface_TILE_Y_LEGACY_MEMORY")

                    plane2_result = self.mpo_helper_dft.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                                       "source_pixel_format_NV12_YUV_420",
                                                       "tiled_surface_TILE_Y_LEGACY_MEMORY")

                    if not plane1_result or not plane2_result:
                        gdhm.report_bug(
                            title="[MPO][Plane scaling]Plane verification failed: NV12_YUV_420, NV12_YUV_420 on display {0}"
                                .format(self.connected_list[display]),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail(
                            'Plane verification failed: NV12_YUV_420, NV12_YUV_420 on display %s' % self.connected_list[
                                display])

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
        # set topology to CLONE configuration
        topology = enum.CLONE

        ##
        # Apply CLONE configuration
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(self.mpo_helper_dft.getStepInfo() + 'Applied display configuration %s for display %s' % (
                DisplayConfigTopology(topology).name, self.connected_list))

            ##
            # Get target id
            target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

            ##
            # Fetch current mode
            resolution = self.config.get_current_mode(target_id)

            planes = []

            rect1 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value1 = flip.MPO_BLEND_VAL(0)
            plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect1, rect1, rect1,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value1)

            rect2 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value2 = flip.MPO_BLEND_VAL(0)
            plane2 = flip.PLANE_INFO(1, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2)

            rect3 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value3 = flip.MPO_BLEND_VAL(0)
            plane3 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect3, rect3, rect3,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value3)

            rect4 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value4 = flip.MPO_BLEND_VAL(0)
            plane4 = flip.PLANE_INFO(1, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect4, rect4, rect4,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value4)

            planes.append(plane1)
            planes.append(plane2)
            planes.append(plane3)
            planes.append(plane4)

            pplanes = flip.PLANE(planes)

            ##
            # Set the boundary values of the plane based on the resolution obtained by the configuration
            self.mpo_helper_dft.set_bounds(resolution.HzRes, resolution.VtRes)

            self.mpo_helper_dft.source_rect(pplanes.stPlaneInfo[2])

            self.perform_flip(pplanes)

            ##
            # Resize the Right of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Right", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Right", 4)):
                self.perform_flip(pplanes)

            ##
            # Resize the Right of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Right", -6) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Right",
                                                                                    -6)):
                self.perform_flip(pplanes)

            ##
            # Resize the Bottom of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Bottom", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Bottom",
                                                                                    4)):
                self.perform_flip(pplanes)

            ##
            # Resize the Bottom of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Bottom", -6) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Bottom",
                                                                                     -6)):
                self.perform_flip(pplanes)

            ##
            # Resize the Left and Top of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Left", -4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Left", -4)
                   and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Top", -4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Top",
                                                                                      -4)):
                self.perform_flip(pplanes)

            ##
            # Resize the Left and Top of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Left", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Left", 4)
                   and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Top", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Top", 4)):
                self.perform_flip(pplanes)

            ##
            # Resize the Right and Bottom of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Right", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Right", 4)
                   and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Bottom", 4) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3],
                                                                                        "Bottom", 4)):
                self.perform_flip(pplanes)

            ##
            # Resize the Right and Bottom of the plane
            while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Right", -8) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3], "Right", -8)
                   and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[2], "Bottom", -8) and self.mpo_helper_dft.resize(pplanes.stPlaneInfo[3],
                                                                                         "Bottom", -8)):
                self.perform_flip(pplanes)
        else:
            self.fail('Failed to apply display configuration %s for displays %s' % (
                DisplayConfigTopology(topology).name, self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips NV12 planes and checks for underrun with various plane sizes')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
