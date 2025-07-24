########################################################################################################################
# @file         plane_scalar_basic.py
# @brief        Basic test to verify if the scalar is enabled during scaling of plane.
#               * Apply Single display configuration across all the displays.
#               * Submit flips with 3 planes where 3 planes are of RGB format.
#                 RGB format represents the desktop, 3D application and media content.
#               * Verify whether scalar is enabled or not.
#               * Apply different resolutions to the planes to check for scaling of the plane
#               * Change the tile format to X, linear and Y.
#               * Submit flips and verify plane programming.
# @author       Shetty, Anjali N
########################################################################################################################
import importlib
import logging
import sys
import unittest

from Libs.Core import enum
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_base

##
# @brief    Contains function to check if the scalar is enabled during scaling of plane.
class PlaneScalarBasic(mpo_base.MPOBase):
    display = None

    ##
    # @brief            To verify whether scalar is enabled or not
    # @param[in]        display;
    # @param[in]        ps_ctl_reg;
    # @return            void
    def verify_scalar(self, display, ps_ctl_reg):
        system_utility = SystemUtility()
        machine_info = SystemInfo()
        platform = None
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        ps_ctl = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % (platform))
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)
        ps_ctl_reg = ps_ctl_reg + '_' + current_pipe
        ps_ctl_value = self.mpo_helper_dft.reg_read.read('PS_CTRL_REGISTER', ps_ctl_reg, platform, 0x0)

        if (ps_ctl_value.__getattribute__("enable_scaler") == getattr(ps_ctl, "enable_scaler_ENABLE")):
            logging.info("Scalar is enabled")
        else:
            gdhm.report_bug(
                title="[MPO][Plane scaling]Scalar is not enabled",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.critical("Scalar is not enabled")
            self.fail()

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

                ##
                # Verify the register programming
                for display in range(len(self.connected_list)):
                    self.mpo_helper_dft.verify_planes(self.connected_list[display], "PLANE_CTL_1", "source_pixel_format_RGB_8888",
                                       "tiled_surface_TILE_Y_LEGACY_MEMORY")
                    self.mpo_helper_dft.verify_planes(self.connected_list[display], "PLANE_CTL_2", "source_pixel_format_RGB_8888",
                                       "tiled_surface_TILE_Y_LEGACY_MEMORY")
                    self.mpo_helper_dft.verify_planes(self.connected_list[display], "PLANE_CTL_3", "source_pixel_format_RGB_8888",
                                       "tiled_surface_TILE_Y_LEGACY_MEMORY")

                ##
                # Verify scalar
                if (pplanes.stPlaneInfo[1].stMPOSrcRect.lRight != pplanes.stPlaneInfo[
                    1].stMPODstRect.lRight and pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom !=
                        pplanes.stPlaneInfo[1].stMPODstRect.lBottom):
                    for display in range(len(self.connected_list)):
                        self.verify_scalar(self.connected_list[display], "PS_CTRL_1")

                if (pplanes.stPlaneInfo[2].stMPOSrcRect.lRight != pplanes.stPlaneInfo[
                    2].stMPODstRect.lRight and pplanes.stPlaneInfo[2].stMPOSrcRect.lBottom !=
                        pplanes.stPlaneInfo[2].stMPODstRect.lBottom):
                    for display in range(len(self.connected_list)):
                        self.verify_scalar(self.connected_list[display], "PS_CTRL_2")

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
        topology = enum.CLONE

        ##
        # Apply SINGLE display configuration across all the displays
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied the configuration")

            ##
            # Get the display configuration
            target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
            resolution = self.config.get_current_mode(target_id)
            planes = []
            mode_list = []
            unique_mode_list = []

            rect1 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value1 = flip.MPO_BLEND_VAL(1)
            plane1 = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect1, rect1, rect1,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value1)

            rect2 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value2 = flip.MPO_BLEND_VAL(1)
            plane2 = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect2, rect2, rect2,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value2)

            rect3 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value3 = flip.MPO_BLEND_VAL(1)
            plane3 = flip.PLANE_INFO(0, 2, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect3, rect3, rect3,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value3)

            rect4 = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            blend_value4 = flip.MPO_BLEND_VAL(1)
            plane4 = flip.PLANE_INFO(1, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect4, rect4, rect4,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value4)

            rect5 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value5 = flip.MPO_BLEND_VAL(1)
            plane5 = flip.PLANE_INFO(1, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect5, rect5, rect5,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value5)

            rect6 = flip.MPO_RECT(0, 0, 1600, 900)
            blend_value6 = flip.MPO_BLEND_VAL(1)
            plane6 = flip.PLANE_INFO(1, 2, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                     flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED, rect6, rect6, rect6,
                                     flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend_value3)

            planes.append(plane1)
            planes.append(plane2)
            planes.append(plane3)
            planes.append(plane4)
            planes.append(plane5)
            planes.append(plane6)

            pplanes = flip.PLANE(planes)

            self.perform_flip(pplanes)

            ##
            # fetch all the modes supported by each of the displays connected
            supported_modes = self.config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    mode_list.append((mode.HzRes, mode.VtRes))

            for values in mode_list:
                if values not in unique_mode_list:
                    unique_mode_list.append(values)

            ##
            # Apply different resolutions to the planes to check for scaling of the plane
            for src_hres, src_vres in unique_mode_list:
                pplanes.stPlaneInfo[1].stMPOSrcRect.lRight = src_hres
                pplanes.stPlaneInfo[1].stMPOSrcRect.lBottom = src_vres
                pplanes.stPlaneInfo[2].stMPOSrcRect.lRight = src_hres
                pplanes.stPlaneInfo[2].stMPOSrcRect.lBottom = src_vres
                pplanes.stPlaneInfo[4].stMPOSrcRect.lRight = src_hres
                pplanes.stPlaneInfo[4].stMPOSrcRect.lBottom = src_vres
                pplanes.stPlaneInfo[5].stMPOSrcRect.lRight = src_hres
                pplanes.stPlaneInfo[5].stMPOSrcRect.lBottom = src_vres
                for dst_hres, dst_vres in unique_mode_list:
                    pplanes.stPlaneInfo[1].stMPODstRect.lRight = dst_hres
                    pplanes.stPlaneInfo[1].stMPOClipRect.lRight = dst_hres
                    pplanes.stPlaneInfo[1].stMPODstRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[1].stMPOClipRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[2].stMPODstRect.lRight = dst_hres
                    pplanes.stPlaneInfo[2].stMPOClipRect.lRight = dst_hres
                    pplanes.stPlaneInfo[2].stMPODstRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[2].stMPOClipRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[4].stMPODstRect.lRight = dst_hres
                    pplanes.stPlaneInfo[4].stMPOClipRect.lRight = dst_hres
                    pplanes.stPlaneInfo[4].stMPODstRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[4].stMPOClipRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[5].stMPODstRect.lRight = dst_hres
                    pplanes.stPlaneInfo[5].stMPOClipRect.lRight = dst_hres
                    pplanes.stPlaneInfo[5].stMPODstRect.lBottom = dst_vres
                    pplanes.stPlaneInfo[5].stMPOClipRect.lBottom = dst_vres

                    self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
