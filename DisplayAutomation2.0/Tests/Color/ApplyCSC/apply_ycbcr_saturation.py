#######################################################################################################################
# @file         apply_ycbcr_saturation.py
# @addtogroup   Test_Color
# @section      apply_ycbcr_saturation
# @remarks      @ref apply_ycbcr_saturation.py \n
#               The test is targetted for TGL as part of the RCR(VSRI-4646)
#               The test script writes the registry key to support YCBCR and Saturation.
#               The test script enables YCbCr, verifies the OUTPUT_CSC registers.
#               Then applies a NON_LINEAR Csc given as part of the command line and verifies the combined csc values
#               A YCbCr disable-enable event is performed to verify the persistence
#               At the end of the test an RedBlueSwap Non-Linear CSC is applied and register level verification is performed.
#               The test script performs register level verification
# CommandLine:  python apply_ycbcr_saturation.py -hdmi_b -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.ApplyCSC.apply_csc_base import *
from Tests.Planes.Common import hdr_constants
from Tests.Planes.Common import hdr_verification


class ApplyYCbCrSaturation(ApplyCSCBase):

    def runTest(self):
        ##
        # Prepare the Reference RGBToYCb Matrix Values
        base_ref_val = hdr_constants.RGB2YCbCr_709_FullRange
        scaled_ref_val = hdr_verification.HDRVerification().scale_csc_for_range_conversion(8, "RGB", "YCBCR",
                                                                                      "FULL_TO_STUDIO", base_ref_val)

        ##
        # Prepare the reference YCbCr * Saturation Matrix
        expected_matrix_ycbcr_into_sat = color_common_utility.matrix_multiply_3X3(scaled_ref_val,
                                                                                  self.matrix_info)

        ##
        # Iterate through all the displays connected and enable YCbCr on the supported panels
        for display_index in range(self.enumerated_displays.Count):
            if str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) in self.connected_list and self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                    target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                    ycbcr_support = driver_escape.is_ycbcr_supported(target_id)
                    if ycbcr_support:
                        logging.info("Panel supports YCbCr")
                        self.ycbcr_enable_status = driver_escape.configure_ycbcr(target_id, True)
                        if not self.ycbcr_enable_status:
                            self.fail("Failed to enable YCbCr")
                        else:
                            logging.info("Successfully enabled YCbCr")
                            current_pipe = color_common_utility.get_current_pipe(self.connected_list[0])
                            ycbcr_prog_csc_val = csc_utility.get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
                            transformed_ycbcr_csc_val = hdr_verification.HDRVerification().transform_rgb_to_yuv_matrix(ycbcr_prog_csc_val)
                            logging.debug("OutputCSC Coeff with YCbCr enabled is")
                            logging.debug(transformed_ycbcr_csc_val)
                            if csc_utility.compare_csc_coeff(transformed_ycbcr_csc_val, scaled_ref_val, "OUTPUT_CSC_COEFF"):
                                logging.info("SUCCESS : YCbCr CSC Coefficients Match with Standard RGBToYCbCr(Limited) Coefficients")
                            else:
                                logging.error("FAIL : YCbCr CSC Coefficients NOT Matching with Standard RGBToYCbCr(Limited) Coefficients")
                                self.fail("FAIL : YCbCr CSC Coefficients NOT Matching with Standard RGBToYCbCr(Limited) Coefficients")

                            ##
                            # Now apply the Non-Linear CSC passed from the command line
                            saturation_csc_param = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
                            params1 = CSCPipeMatrixParams(1, saturation_csc_param)

                            if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[display_index].
                                                               DisplayAndAdapterInfo, enum.OPERATION_SET, self.csc_type, params1) is True:
                                logging.info("Successfully applied Saturation : Non-Linear CSC")
                                saturation_ycbcr_combined_csc = csc_utility.get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
                                logging.debug("Programmed Saturation and YCbCr Combined CSC is")
                                logging.debug(saturation_ycbcr_combined_csc)
                                transformed_sat_ycbcr_csc_matrix = hdr_verification.HDRVerification().transform_rgb_to_yuv_matrix(saturation_ycbcr_combined_csc)
                                logging.debug("Expected Saturation and YCbCr Combined CSC is")
                                logging.debug(expected_matrix_ycbcr_into_sat)

                                if csc_utility.compare_csc_coeff(transformed_sat_ycbcr_csc_matrix, expected_matrix_ycbcr_into_sat, "OUTPUT_CSC_COEFF"):
                                    logging.info("SUCCESS : CSC Coefficients Match")
                                else:
                                    logging.error("FAIL : CSC Coefficients NOT matching")
                                    self.fail()
                            else:
                                logging.error("Failed to set the Saturation values")
                                self.fail("Failed to set the Saturation values")
                        ##
                        # Disable and Enable YCbCr
                        if driver_escape.configure_ycbcr(target_id, False):
                            logging.info("Successfully disabled YCbCr")
                            #
                            # Verify if OutputCSC is disabled successfully
                            output_csc_after_ycbcr_disable = csc_utility.get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
                            logging.debug("OutputCSC Coeff with YCbCr disabled is")
                            logging.debug(output_csc_after_ycbcr_disable)
                            if csc_utility.compare_csc_coeff(output_csc_after_ycbcr_disable, self.matrix_info, "OUTPUT_CSC_COEFF"):
                                logging.info("SUCCESS : CSC Coefficients Match after Disable YCbCr")
                            else:
                                logging.error("FAIL : CSC Coefficients NOT Matching after Disable YCbCr")
                                self.fail("FAIL : CSC Coefficients NOT Matching after Disable YCbCr")
                            if driver_escape.configure_ycbcr(target_id, True):
                                logging.info("Successfully enabled YCbCr")
                                output_csc_after_ycbcr_re_enable = csc_utility.get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
                                transformed_ocsc_after_ycbcr_re_enable = hdr_verification.HDRVerification().transform_rgb_to_yuv_matrix(output_csc_after_ycbcr_re_enable)
                                logging.debug("OutputCSC Coeff with YCbCr enabled is")
                                logging.debug(transformed_ocsc_after_ycbcr_re_enable)
                                if csc_utility.compare_csc_coeff(transformed_ocsc_after_ycbcr_re_enable, expected_matrix_ycbcr_into_sat, "OUTPUT_CSC_COEFF"):
                                    logging.info("SUCCESS : CSC Coefficients Match after Renabling YCbCr")
                                else:
                                    logging.error("FAIL : CSC Coefficients NOT Matching after Renabling YCbCr")
                                    self.fail("FAIL : CSC Coefficients NOT Matching after Renabling YCbCr")
                            else:
                                logging.error("Failed to re-enable YCbCr")
                                self.fail("Failed to re-enable YCbCr")
                        else:
                            logging.error("Failed to disable YCbCr")
                            self.fail("Failed to disable YCbCr")

                        red_blue_swap_matrix = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
                        linear_csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(red_blue_swap_matrix))
                        rgb_swap_params = CSCPipeMatrixParams(1, linear_csc_params)
                        if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[display_index].
                                                                  DisplayAndAdapterInfo, enum.OPERATION_SET,
                                                          self.csc_type,
                                                          rgb_swap_params) is True:
                            logging.info("Successfully applied Saturation : RedBlue Swap Non-Linear CSC")
                            rgb_swap_value = csc_utility.get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
                            transformed_rgb_swap_value = hdr_verification.HDRVerification().transform_rgb_to_yuv_matrix(rgb_swap_value)
                            logging.debug("After RedBlueSwap CSC Coefficients")
                            logging.debug(rgb_swap_value)
                            expected_matrix_ycbcr_into_sat = color_common_utility.matrix_multiply_3X3(scaled_ref_val,red_blue_swap_matrix)
                            if csc_utility.compare_csc_coeff(transformed_rgb_swap_value, expected_matrix_ycbcr_into_sat,
                                                             "OUTPUT_CSC_COEFF"):
                                logging.info("SUCCESS : CSC Coefficients Match")
                            else:
                                logging.error("FAIL : CSC Coefficients NOT matching")
                                self.fail("FAIL : CSC Coefficients NOT matching")
                        else:
                            logging.error("Failed to apply Saturation : RedBlue Swap Non-Linear CSC")
                    else:
                        logging.error("YCbCr is not supported on the planned display : Unexpected Command Line")
                        self.fail("FAIL : CSC Coefficients NOT matching")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
