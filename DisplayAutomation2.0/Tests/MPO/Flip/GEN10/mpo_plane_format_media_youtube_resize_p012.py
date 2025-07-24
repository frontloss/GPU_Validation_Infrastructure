########################################################################################################################
# @file         mpo_plane_format_media_youtube_resize_p012.py
# @brief        Basic test to verify underruns during resize of plane in P012 YUV format.
#               * Apply Single display configuration across all the displays.
#               * Submit 2 flips, where 1 plane is of P012 format and another with YUV 422 with 8 BPC.
#                 P012 format and YUV 422 format represents media content.
#               * Set the boundary values of the plane based on the resolution obtained by the configuration.
#               * Resize the plane in a given direction, using value given to resize the plane.
#               * Submit flips and verify plane programming.
# @author       Balasubramanyam, Smitha
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
# @brief    Contains function to check underruns during resize of plane in P012 YUV format
class MPOPlaneFormatMediaYouTubeResizeP012(mpo_base.MPOBase):
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

                logging.info(
                    self.mpo_helper_dft.getStepInfo() + 'Performed flip of 2 planes: P012_YUV_420_12_BIT, YUV_422_PACKED_8_BPC')
                ##
                # Verify the register programming
                plane1_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_1',
                                                   "source_pixel_format_P012_YUV_420_12_BIT",
                                                   "tiled_surface_TILE_Y_LEGACY_MEMORY")

                plane2_result = self.mpo_helper_dft.verify_planes(self.display, 'PLANE_CTL_2',
                                                   "source_pixel_format_YUV_422_PACKED_8_BPC",
                                                   "tiled_surface_TILE_Y_LEGACY_MEMORY")

                if not plane1_result or not plane2_result:
                    gdhm.report_bug(
                        title="[MPO][Plane scaling]Plane verification failed: P012_YUV_420_12_BIT, YUV_422_PACKED_8_BPC",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail('Plane verification failed: P012_YUV_420_12_BIT, YUV_422_PACKED_8_BPC')

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
                logging.info(self.mpo_helper_dft.getStepInfo() + "Applied display configuration %s for display %s" % (
                    DisplayConfigTopology(topology).name, self.connected_list[display_index]))
                self.display = self.connected_list[display_index]

                ##
                # Get the display configuration
                target_id = self.config.get_target_id(self.connected_list[display_index], self.enumerated_displays)
                resolution = self.config.get_current_mode(target_id)

                planes = []

                rect1 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
                blend_value1 = flip.MPO_BLEND_VAL(0)
                plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_YUV422,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect1, rect1, rect1,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value1, 0, None, 0)

                rect2 = flip.MPO_RECT(0, 0, resolution.HzRes // 2, resolution.VtRes // 2)
                blend_value2 = flip.MPO_BLEND_VAL(0)
                plane2 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_P012YUV420,
                                         flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2, 0, None, 10)

                planes.append(plane1)
                planes.append(plane2)

                pplanes = flip.PLANE(planes)

                ##
                # Set the boundary values of the plane based on the resolution obtained by the configuration
                self.mpo_helper_dft.set_bounds(resolution.HzRes, resolution.VtRes)

                self.mpo_helper_dft.source_rect(pplanes.stPlaneInfo[1])

                self.perform_flip(pplanes)

                ##
                # Resize the Right of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Right", 4)):
                    self.perform_flip(pplanes)

                ##
                # Resize the Left of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Left", 4)):
                    self.perform_flip(pplanes)

                ##
                # Resize the Left of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Left", -4)):
                    self.perform_flip(pplanes)

                ##
                # Resize the Bottom of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Bottom", 2)):
                    self.perform_flip(pplanes)

                ##
                # Resize the Top of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[1], "Top", 2)):
                    self.perform_flip(pplanes)

                ##
                # Resize the Right, Bottom of the plane
                while (self.mpo_helper_dft.resize(pplanes.stPlaneInfo[0], "Right", -4) and self.mpo_helper_dft.resize(
                        pplanes.stPlaneInfo[1], "Bottom", -2)):
                    self.perform_flip(pplanes)
            else:
                self.fail("Failed to apply display configuration %s for display %s" % (
                    DisplayConfigTopology(topology).name, self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Flips RGB and P010 YUV planes and checks for underrun"
                 " during plane resize")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
