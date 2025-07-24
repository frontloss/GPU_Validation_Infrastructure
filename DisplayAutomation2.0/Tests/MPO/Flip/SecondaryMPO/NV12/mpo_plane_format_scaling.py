########################################################################################################################
# @file         mpo_plane_format_scaling.py
# @brief        Basic test to verify scaling of planes.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 2 planes where 1 plane is of RGB format and other plane is of NV12 format.
#                 RGB format represents the desktop and NV12 format represents media content.
#               * Apply different resolutions to the planes to check for scaling of the plane
#               * Change the tile format to X, linear and Y.
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
# @brief    Contains function to check scaling planes
class MPOPlaneFormatScaling(mpo_base.MPOBase):

    ##
    # @brief            To perform Flips
    # @param[in]        pplanes; details of planes
    # @param[in]        tile_format;
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
                logging.info(self.mpo_helper_dft.getStepInfo() + 'Performed flip of 2 planes: NV12_YUV_420, RGB_8888')
                ##
                # Verify the register programming
                for display in range(len(self.connected_list)):
                    plane1_result = self.mpo_helper_dft.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                                       "source_pixel_format_NV12_YUV_420", tile_format)
                    plane2_result = self.mpo_helper_dft.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                                       "source_pixel_format_RGB_8888", tile_format)
                    if not plane1_result or not plane2_result:
                        gdhm.report_bug(
                            title="[MPO][Plane scaling]Plane verification failed: NV12_YUV_420, RGB_8888 on display {0}"
                                .format(self.connected_list[display]),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail(
                            'Plane verification failed: NV12_YUV_420, RGB_8888 on display %s' % self.connected_list[
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
            mode_list = []
            unique_mode_list = []

            rect1 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value1 = flip.MPO_BLEND_VAL(1)
            plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect1, rect1, rect1,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value1)

            rect2 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value2 = flip.MPO_BLEND_VAL(1)
            plane2 = flip.PLANE_INFO(1, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2)

            rect3 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value3 = flip.MPO_BLEND_VAL(0)
            plane3 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect3, rect3, rect3,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value3)

            rect4 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value4 = flip.MPO_BLEND_VAL(0)
            plane4 = flip.PLANE_INFO(1, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect4, rect4, rect4,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value4)

            planes.append(plane1)
            planes.append(plane2)
            planes.append(plane3)
            planes.append(plane4)

            pplanes = flip.PLANE(planes)

            self.perform_flip(pplanes, "tiled_surface_TILE_Y_LEGACY_MEMORY")

            ##
            # Fetch all the supported modes
            supported_modes = self.config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    mode_list.append((mode.HzRes, mode.VtRes))

            for values in mode_list:
                if values not in unique_mode_list:
                    unique_mode_list.append(values)

            ##
            # Apply different resolutions to the planes to check for scaling of the plane
            for plane0_hres, plane0_vres in unique_mode_list:
                pplanes.stPlaneInfo[0].stMPOSrcRect.lRight = plane0_hres
                pplanes.stPlaneInfo[0].stMPOSrcRect.lBottom = plane0_vres
                pplanes.stPlaneInfo[0].stMPODstRect.lRight = plane0_hres
                pplanes.stPlaneInfo[0].stMPODstRect.lBottom = plane0_vres
                pplanes.stPlaneInfo[0].stMPOClipRect.lRight = plane0_hres
                pplanes.stPlaneInfo[0].stMPOClipRect.lBottom = plane0_vres
                pplanes.stPlaneInfo[2].stMPOSrcRect.lRight = plane0_hres
                pplanes.stPlaneInfo[2].stMPOSrcRect.lBottom = plane0_vres
                pplanes.stPlaneInfo[2].stMPODstRect.lRight = plane0_hres
                pplanes.stPlaneInfo[2].stMPODstRect.lBottom = plane0_vres
                pplanes.stPlaneInfo[2].stMPOClipRect.lRight = plane0_hres
                pplanes.stPlaneInfo[2].stMPOClipRect.lBottom = plane0_vres
                for plane1_src_hres, plane1_src_vres in unique_mode_list:
                    pplanes.stPlaneInfo[1].stMPOSrcRect.lRight = plane1_src_hres
                    pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom = plane1_src_vres
                    pplanes.stPlaneInfo[3].stMPOSrcRect.lRight = plane1_src_hres
                    pplanes.stPlaneInfo[3].stMPOSrcRect.lBottom = plane1_src_vres
                    for dst_hres, dst_vres in unique_mode_list:
                        pplanes.stPlaneInfo[1].stMPODstRect.lRight = dst_hres
                        pplanes.stPlaneInfo[1].stMPOClipRect.lRight = dst_hres
                        pplanes.stPlaneInfo[1].stMPODstRect.lBottom = dst_vres
                        pplanes.stPlaneInfo[1].stMPOClipRect.lBottom = dst_vres
                        pplanes.stPlaneInfo[3].stMPODstRect.lRight = dst_hres
                        pplanes.stPlaneInfo[3].stMPOClipRect.lRight = dst_hres
                        pplanes.stPlaneInfo[3].stMPODstRect.lBottom = dst_vres
                        pplanes.stPlaneInfo[3].stMPOClipRect.lBottom = dst_vres

                        self.perform_flip(pplanes, "tiled_surface_TILE_Y_LEGACY_MEMORY")

                        ##
                        # Change the tile format
                        for i in range(len(planes)):
                            pplanes.stPlaneInfo[i].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED

                        self.perform_flip(pplanes, "tiled_surface_TILE_X_MEMORY")

                        ##
                        # Change the tile format
                        for i in range(len(planes)):
                            pplanes.stPlaneInfo[i].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

                        self.perform_flip(pplanes, "tiled_surface_LINEAR_MEMORY")

                        ##
                        # Change the tile format
                        for i in range(len(planes)):
                            pplanes.stPlaneInfo[
                                i].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
        else:
            self.fail('Failed to apply display configuration %s for displays %s' % (
                DisplayConfigTopology(topology).name, self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips NV12 and RGB planes and checks for underrun with various plane scaling')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
