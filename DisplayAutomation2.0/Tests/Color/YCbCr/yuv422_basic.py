#######################################################################################################################
# @file         yuv422_basic.py
# @addtogroup   Test_Color
# @section      yuv422_basic
# @remarks      @ref yuv422_basic.py \n
#               The test script adds the ForceApplyYUV422Mode registry key and
#               performs a modeset for the registry key to take effect.
#               Verification Details :
#               1. YUV422 Mode ENABLE in PipeMisc2 register
#               2. YUV420 Mode DISABLE in PipeMisc register
#               3. oCSC ENABLE in CSCMode register
#               4. Performing verification of the coefficients and postoffset
# CommandLine:
#               python yuv422_basic.py -hdmi_b -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core import registry_access
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color import color_common_utility
from registers.mmioregister import MMIORegister
from Tests.Color.color_common_base import *
from Tests.Planes.Common import hdr_verification
from Tests.Planes.Common import hdr_constants


class YUV422Basic(ColorCommonBase):

    def set_and_verify_yuv422(self, enable_status):
        utility = system_utility.SystemUtility()
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        ##
        # Add the ForceApplyYUV422Mode through registry write
        if not registry_access.write(args=reg_args, reg_name="ForceApplyYUV422Mode",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=enable_status):
            logging.error("Failed to set the registry key to apply YUV422 mode")
            self.fail("Failed to set the registry key to apply YUV422 mode")

        ##
        # Perform a modeset for the registry key to take effect
        target_id = DisplayConfiguration().get_target_id(self.connected_list[0], self.enumerated_displays)
        current_mode = DisplayConfiguration().get_current_mode(target_id)
        supported_modes = DisplayConfiguration().get_all_supported_modes([target_id])
        for key, values in supported_modes.items():
            for mode in values:
                if mode.HzRes != current_mode.HzRes and mode.VtRes == current_mode.VtRes:
                    DisplayConfiguration().set_display_mode([mode])
                    break

        ##
        # Verify if the registry key has been successfully added
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="ForceApplyYUV422Mode")
        if enable_status == reg_value:
            logging.info("Successfully set ForceApplyYUV422Mode registry key")
        else:
            logging.error("Failed to apply ForceApplyYUV422Mode")
            self.fail()

    def runTest(self):
        self.set_and_verify_yuv422(enable_status=1)
        current_pipe = color_common_utility.get_current_pipe(self.connected_list[0])
        pipe_misc2_name = "PIPE_MISC2_" + current_pipe
        pipe_misc2_reg = MMIORegister.read("PIPE_MISC2_REGISTER", pipe_misc2_name, self.platform)

        ##
        # Verifying if YUV422 Mode in PipeMisc2 Register is enabled
        if pipe_misc2_reg.yuv_422_mode:
            logging.info("PASS : YUV422 Mode : Expected - ENABLED; Actual - ENABLED")
        else:
            logging.error("FAIL : YUV422 Mode : Expected - ENABLED; Actual - DISABLED")

        ##
        # Do not expect YUV420 Enable when YUV422 is enabled
        pipe_misc_name = "PIPE_MISC_" + current_pipe
        pipe_misc_reg = MMIORegister.read("PIPE_MISC_REGISTER", pipe_misc_name, self.platform)

        if not pipe_misc_reg.yuv420_enable:
            logging.info("PASS : YUV420 Mode : Expected - DISABLED; Actual - DISABLED")
        else:
            logging.error("FAIL : YUV420 Mode : Expected - DISABLED; Actual - ENABLED")

        ##
        # Verify if oCSC is enabled and compare the CSC Co-efficients
        csc_reg_name = "CSC_MODE_" + current_pipe
        gamma_mode_reg = MMIORegister.read("CSC_MODE_REGISTER", csc_reg_name, self.platform)
        if gamma_mode_reg.pipe_output_csc_enable == 1:
            logging.info("PASS : OutputCSC Expected : ENABLE; Actual : ENABLE")
        else:
            logging.error("FAIL : OutputCSC Expected : ENABLE; Actual : DISABLE")
            self.fail("FAIL : OutputCSC Expected : ENABLE; Actual : DISABLE")

        ##
        # Perform CSC Co-efficients comparison
        programmed_csc = color_common_utility.get_csc_coeff_matrix_from_reg(self.platform, current_pipe, csc_type="NON_LINEAR")
        transformed_matrix = hdr_verification.HDRVerification().transform_rgb_to_yuv_matrix(programmed_csc)
        base_ref_val = hdr_constants.RGB2YCbCr_709_FullRange
        scaled_ref_val = hdr_verification.HDRVerification().scale_csc_for_range_conversion(8, "RGB", "YCBCR",
                                                                                      "FULL_TO_STUDIO", base_ref_val)
        logging.debug("Programmed CSC Coefficients are %s" % transformed_matrix)
        logging.debug("Reference CSC Coefficients are %s" % scaled_ref_val)
        if color_common_utility.compare_csc_coeff(transformed_matrix, scaled_ref_val) is False:
            self.fail("FAIL : OutputCSC Coeffients are not Matching")
        else:
            logging.info("PASS : OutputCSC Coefficients Verification Successful")

        ##
        # Performing verification of PostOffsets
        if color_common_utility.csc_pre_or_post_off_verification(self.platform, current_pipe, 8, "RGB", "YCBCR", "FULL_TO_STUDIO",
                                            "OUTPUT_CSC_POSTOFF_REGISTER", "OUTPUT_CSC_POSTOFF") is False:
            logging.error("FAIL : OutputCSC POSTOFFSET Verification failed")
            self.fail("FAIL : OutputCSC POSTOFFSET Verification failed")
        else:
            logging.info("PASS : OutputCSC POSTOFFSET Verification is successful")

        ##
        # Performing verification of PreOffsets
        if color_common_utility.csc_pre_or_post_off_verification(self.platform, current_pipe, 8, "RGB", "YCBCR", "FULL_TO_STUDIO", "OUTPUT_CSC_PREOFF_REGISTER",
                                            "OUTPUT_CSC_PREOFF") is False:
            logging.error("FAIL : OutputCSC PREOFFSET Verification failed")
            self.fail("FAIL : OutputCSC PREOFFSET Verification failed")
        else:
            logging.info("PASS : OutputCSC PREOFFSET Verification is successful")

    def tearDown(self):
        self.set_and_verify_yuv422(enable_status=0)
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
