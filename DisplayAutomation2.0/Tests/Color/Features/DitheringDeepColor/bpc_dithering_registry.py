#################################################################################################
# @file         bpc_dithering_registry.py
# @brief        This is a custom script which can used to perform below functionalities
#               1.To set bpc through write registry
#               2.To perform DFT flip and register verification for transcoder bpc and dithering
# @author       Vimalesh D
#################################################################################################
import sys
import logging
import unittest
import win32api
from Libs.Core import registry_access
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.flip import MPO, SB_PIXELFORMAT, MPO_BLEND_VAL, SURFACE_MEMORY_TYPE, MPO_RECT, PLANE_INFO, \
    MPO_PLANE_ORIENTATION, MPO_COLOR_SPACE_TYPE, PLANE
from Libs.Core.test_env.context import GfxDriverType
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import common_utility, color_escapes
from Tests.Color.Common.common_utility import get_bpc_from_pixel_format
from Tests.Color.Verification.feature_basic_verify import verify_dithering_feature, verify_transcoder_bpc
from Tests.test_base import TestBase


##
# @brief - To perform BPC and Dithering verification on panels.
class DitheringBPC(TestBase):

    ##
    # @brief Contains bpc and dithering verification test steps
    # @return None
    def runTest(self):
        config = DisplayConfiguration()

        bpc_list = ["BPC8", "BPC10", "BPC12"]
        pyPlanes = []
        pixel_format_dict = {"SB_R8G8B8A8": SB_PIXELFORMAT.SB_R8G8B8A8,
                             "SB_B10G10R10A2": SB_PIXELFORMAT.SB_B10G10R10A2,
                             "SB_R16G16B16X16F": SB_PIXELFORMAT.SB_R16G16B16X16F}

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                expected_dithering_status = False
                mpo = MPO()
                for transcoder_bpc in bpc_list:
                    # Update panel default color depth and color format
                    if color_escapes.set_bpc_encoding(panel.display_and_adapterInfo, transcoder_bpc,
                                                      "RGB", GfxDriverType.YANGRA, panel.is_lfp) is False:
                        self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.target_id}")

                    ##
                    # Enable DFT
                    mpo.enable_disable_mpo_dft(True, 1)

                    ##
                    # Update plane params
                    resolution = config.get_current_mode(panel.target_id)
                    stMPOBlend = MPO_BLEND_VAL(0)
                    tiling = SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

                    sdimension = MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
                    ddimension = MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)

                    for pixel_format in pixel_format_dict.values():
                        index = 0
                        Plane1 = PLANE_INFO(index, 0, 1, pixel_format, tiling, sdimension, ddimension,
                                            ddimension, MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                            MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709)
                        pyPlanes.append(Plane1)
                        planes = PLANE(pyPlanes)
                        common_utility.perform_flip(planes, adapter.gfx_index)

                        # verify transcoder bpc
                        if verify_transcoder_bpc(adapter.gfx_index, adapter.platform, panel.transcoder, transcoder_bpc) is False:
                            self.fail()

                        frame_buffer_bpc = get_bpc_from_pixel_format(pixel_format)
                        ##
                        # Compare frambuffer BPC and panel BPC
                        if transcoder_bpc != frame_buffer_bpc:
                            expected_dithering_status = True

                        # Verify dithering
                        if verify_dithering_feature(adapter.gfx_index, adapter.platform, panel.pipe, panel.transcoder,
                                                    expected_dithering_status) is False:
                            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
