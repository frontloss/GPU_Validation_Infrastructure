########################################################################################################################
# @file         hdr_singleplane_with_3dlut.py
# @brief        This script contains test to flip single plane on LFP along with 3D LUT feature enabled. Test verifies
#               display color pipeline programming and also checks for underrun.
# @author       R Soorya
########################################################################################################################
from Libs.Core import driver_escape
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import DppHwLutInfo, DppHwLutOperation
from Tests.Planes.Common.hdr_base import *

##
# @brief   Contains functions to verify display color pipeline programming and also checks for underrun for single plane
class Test_SinglePlaneWith3DLUT(HDRBase):
    no_of_layers = [1, 1, 1, 1]

    ##
    # @brief     Unittest runTest function
    # @return    None
    def runTest(self):
        self.parse_xml(self.xml)
        if self.blending_mode[0] == BT2020_LINEAR:
            logging.error("3D LUT is not supported in Linear mode")
            self.fail()

        self.set_native_mode()

        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)

        count = [0, 0]

        pyPlanes = []
        internal_gfx_adapter_index = 'gfx_0'
        for index in range(0, self.no_displays):

            target_id = self.display_config.get_target_id(self.connected_list[0], self.enumerated_displays)
            cui_dpp_hw_lut_info = DppHwLutInfo(target_id, DppHwLutOperation.UNKNOWN.value, 0)
            result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(internal_gfx_adapter_index, cui_dpp_hw_lut_info)
            if result is False:
                logging.error(f'Escape call failed : get_dpp_hw_lut() for {target_id}')
            bin_file_path = "Color\Hw3DLUT\CustomLUT\\" + "CustomLUT_no_R.bin"
            path = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)

            cui_dpp_hw_lut_info = DppHwLutInfo(target_id, DppHwLutOperation.APPLY_LUT.value,
                                               cui_dpp_hw_lut_info.depth)
            if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
                self.fail(f'Invalid bin file path provided : {path}!')

            ##
            # Set the DPP Hw LUT Info
            result = driver_escape.set_dpp_hw_lut(internal_gfx_adapter_index, cui_dpp_hw_lut_info)
            if result is False:
                logging.error(f'Escape call failed : get_dpp_hw_lut() for {target_id}')

            stMPOBlend = flip.MPO_BLEND_VAL(0)
            tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
            sdimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            ddimension = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)
            pyPlanes = []

            if not planes_verification.check_layer_reordering() and self.pixel_format[0] in self.planar_formats:
                plane1_layer = 1
            else:
                plane1_layer = 0

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes,
                                                self.current_mode[index].VtRes, self.pixel_format[0], plane1_layer,
                                                index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], tiling, sdimension,
                                     ddimension, ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[0], out_file0)

            pyPlanes.append(Plane1)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)

        if self.perform_hdr_flip(planes):
            logging.info("Flipped successfully and the Register Verification has passed")
        else:
            self.fail("SDR/HDR single plane flip verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
