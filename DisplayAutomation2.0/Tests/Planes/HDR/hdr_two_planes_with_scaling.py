########################################################################################################################
# @file         hdr_two_planes_with_scaling.py
# @brief        This script contains test to flip two planes on single or multiple displays with different plane
#               parameters. Test verifies display color pipeline programming and also checks for underrun.
# @author       R Soorya
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_common_utility import get_bit_value
from Libs.Core.machine_info.machine_info import SystemInfo
from Tests.Planes.Common.hdr_base import *


##
# @brief    Contains functions to verify display color pipeline programming and also checks for underrun for two planes
class Test_TwoPlanesHDR_Scaling(HDRBase):
    no_of_layers = [2, 2, 2, 2]
    machine_info = SystemInfo()
    ##
    # @brief     Unittest runTest function
    # @return    None
    def runTest(self):

        self.parse_xml(self.xml)
        if self.blending_mode[0] == BT2020_LINEAR:
            self.setup_for_linear_mode()
        else:
            logging.info("Blending Mode is not Linear - ForceHDRMode Regkey need not be set")

        self.set_native_mode()
        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)

        stMPOBlend = flip.MPO_BLEND_VAL(0)

        tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
        pyPlanes = []
        for index in range(0, self.no_displays):
            sdimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes,
                                        self.current_mode[index].VtRes)  # downscaling
            ##
            # Downscaling is supported only upto a shrink factor of 2 and not beyond
            ddimension1 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes - 2, self.current_mode[index].VtRes)
            sdimension2 = flip.MPO_RECT(00, 0, self.current_mode[index].HzRes // 3, self.current_mode[index].VtRes // 3)
            ddimension2 = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes // 2,
                                        self.current_mode[index].VtRes // 2)  # Upscaling
            pyPlanes = []

            if not planes_verification.check_layer_reordering() and self.pixel_format[1] in self.planar_formats:
                plane1_layer = 0
                plane2_layer = 1
            else:
                plane1_layer = 1
                plane2_layer = 0

            out_file0 = self.convert_png_to_bin(self.path[0], self.current_mode[index].HzRes,
                                                self.current_mode[index].VtRes, self.pixel_format[0], plane1_layer,
                                                index)
            out_file1 = self.convert_png_to_bin(self.path[1], self.current_mode[index].HzRes / 3,
                                                self.current_mode[index].VtRes / 3, self.pixel_format[1], plane2_layer,
                                                index)
            Plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], tiling, sdimension1,
                                     ddimension1, ddimension1, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[0], out_file0)
            Plane2 = flip.PLANE_INFO(self.source_id[index], plane2_layer, 1, self.pixel_format[1], tiling, sdimension2,
                                     ddimension2, ddimension2, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                     stMPOBlend, self.color_space[1], out_file1)

            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayFeatureControl")
        enable_linear_scaling_support = get_bit_value(reg_value, 20, 20)
        ##
        # For all platforms upto ADLP, the Linear Scaling Support would be False by default
        # This includes DG2
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        ##
        # All platforms upto ADLP (Gen13) to have th
        if enable_linear_scaling_support == 0:
            if self.blending_mode[0] == BT2020_LINEAR:
                if self.platform in "dg2":
                    if self.perform_hdr_flip(planes) is False:
                        logging.info("PASS: CheckMPO failure Expected since test tried to perform Linear Scaling in "
                                     "HDR mode")
                    else:
                        logging.error("Failed to Perform Flip in HDR Mode")
                        self.fail()
                ##
                # On ADLP+ platforms, in Linear Blending Mode, the CheckMPO will not be failed
                else:
                    if self.perform_hdr_flip(planes):
                        logging.info("Successfully performed flip")
                    else:
                        logging.error("Failed to Perform Flip in HDR Mode")
                        self.fail()
            ##
            # In Non-Linear Blending Mode,
            else:
                if self.perform_hdr_flip(planes):
                    logging.info("Flipped successfully and the Register Verification has passed")
                else:
                    self.fail("SDR/HDR single plane flip verification failed")
        else:
            if self.perform_hdr_flip(planes):
                logging.info("Flipped successfully and the Register Verification has passed")
            else:
                self.fail("SDR/HDR single plane flip verification failed")

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
