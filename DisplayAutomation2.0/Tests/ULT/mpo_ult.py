###############################################################################
# \ref      mpo_ult.py
# \brief    Tests to verify MPO API's
# \author   Anjali Shetty
###############################################################################
import unittest

from Libs.Core.test_env.test_environment import *
from Libs.Core.flip import *
from Libs.Core.display_config.display_config import *
from Libs.Core.test_env import test_environment
from Libs.Core.gta import gta_state_manager
from Libs.Core import test_header
from Libs.Core.logger import display_logger


class mpo_ult(unittest.TestCase):
    platform_name = None
    mpo = MPO()
    system_utility = SystemUtility()
    config = DisplayConfiguration()
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    for i in range(len(gfx_display_hwinfo)):
        platform_name = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break

    def setUp(self):

        ##
        # Enable the DFT framework and feature
        self.mpo.enable_disable_mpo_dft(True, 1)

        enumerated_displays = self.config.get_enumerated_display_info()
        self.targetid = enumerated_displays.ConnectedDisplays[0].TargetID

    def perform_flip(self, pplanes):
        ##
        # Check for Multiplane overlay support
        checkmpo_result = self.enable_mpo.check_mpo(pplanes)
        if checkmpo_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
            ##
            # Present the planes on the screen
            ssa_result = self.enable_mpo.set_source_address_mpo(pplanes)
            if ssa_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
                logging.info("Successfully flipped plane content")
                time.sleep(5)
            elif ssa_result == PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                self.fail("Resource creation failed")
            else:
                self.fail("Set source address failed")

        elif checkmpo_result == PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            self.fail("Resource creation failed")
        else:
            self.fail("Check MPO failed")

    def test_1_mpo_default_dwm_plane(self):
        logging.info("Test1 - MPO DWM Plane")
        planes = []

        mode = self.config.get_current_mode(self.targetid)

        source_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        destination_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        clip_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)

        plane_attributes = PLANE_INFO(0, 0, 1, PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                      SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                      source_rect_coordinates, destination_rect_coordinates, clip_rect_coordinates,
                                      MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, MPO_BLEND_VAL(0))
        planes.append(plane_attributes)

        pplanes = PLANE(planes)

        self.perform_flip(pplanes)

    def test_2_dwm_scaling_blending(self):
        logging.info("Test2 - MPO DWM Plane with scaling and blending")
        planes = []

        mode = self.config.get_current_mode(self.targetid)

        source_rect_coordinates2 = MPO_RECT(0, 0, 1024, 768)
        source_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        destination_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        clip_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)

        plane1_attributes = PLANE_INFO(0, 0, 1, PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                       SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                       source_rect_coordinates, destination_rect_coordinates, clip_rect_coordinates,
                                       MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, MPO_BLEND_VAL(1))
        plane2_attributes = PLANE_INFO(0, 1, 1, PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                       SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                       source_rect_coordinates2, destination_rect_coordinates, clip_rect_coordinates,
                                       MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, MPO_BLEND_VAL(0))

        planes.append(plane1_attributes)
        planes.append(plane2_attributes)

        pplanes = PLANE(planes)

        self.perform_flip(pplanes)

    def test_3_nv12_linear(self):
        logging.info("Test3 - NV12 with Linear Format")
        planes = []

        mode = self.config.get_current_mode(self.targetid)

        source_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        destination_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        clip_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)

        plane_attributes = PLANE_INFO(0, 0, 1, PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                      SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR,
                                      source_rect_coordinates, destination_rect_coordinates, clip_rect_coordinates,
                                      MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, MPO_BLEND_VAL(0))
        planes.append(plane_attributes)

        pplanes = PLANE(planes)

        self.perform_flip(pplanes)

    @unittest.skipIf(
        platform_name in ['IVB', 'HSW', 'VLV', 'BDW', 'APL', 'CHV', 'SKL', 'BXT', 'KBL', 'CNL', 'GLK', 'CFL'],
        "HFlip is not supported")
    def test_4_hflip(self):
        logging.info("Test3 - HFlip")
        planes = []

        mode = self.config.get_current_mode(self.targetid)

        source_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        destination_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)
        clip_rect_coordinates = MPO_RECT(0, 0, mode.HzRes, mode.VtRes)

        plane_attributes = PLANE_INFO(0, 0, 1, PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420,
                                      SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                      source_rect_coordinates, destination_rect_coordinates, clip_rect_coordinates,
                                      MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, MPO_BLEND_VAL(0),
                                      stmpo_flip_flag=MPO_FLIP_FLAGS(2))
        planes.append(plane_attributes)

        pplanes = PLANE(planes)

        self.perform_flip(pplanes)

    def tearDown(self):
        ##
        # Disable the DFT framework and feature
        self.mpo.enable_disable_mpo_dft(False, 1)


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()

