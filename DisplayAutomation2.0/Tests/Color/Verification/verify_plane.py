#################################################################################################
# @file         verify_plane.py
# @brief        This script comprises of PlaneColorVerifier Base class which has all the attributes
#               required by the Plane Blocks, verification modules which will be overloaded
#               by the Derived Classes specific to each Generation when required.
# @author       Smitha B
#################################################################################################
import logging
import DisplayRegs
from Libs.Core import flip
from Libs.Core.logger import gdhm
from Tests.Color.Common import color_mmio_interface, color_constants, color_enums
from Tests.Color.Common import hdr_utility, csc_utility, gamma_utility, common_utility
from Tests.Color.Verification import feature_basic_verify

##
# @brief        PipeColorVerifier Base Class
class PlaneColorVerifier:
    gfx_index = None
    platform = None
    regs = None
    mmio_interface = color_mmio_interface.ColorMmioInterface()
    plane_csc_scalefactor = 1.0

    def verify_fp16_normalizer_programming(self, pipe, pixel_normalizer_info):
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        if is_hdr_enabled:
            ref_hdr_normalizing_factor = 0x2019
            logging.debug("Blending Mode is Linear")
            if pixel_normalizer_info.NormalizationFactor != ref_hdr_normalizing_factor:
                logging.error("FAIL: FP16 Normalizer value not matching: Expected = {0} Actual = {1}".format(
                    ref_hdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                gdhm.report_driver_bug_os("Verification failed as FP16 Normalizer value not matching: Expected = {0} Actual = {1}"
                                    .format(ref_hdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                return False
            else:
                logging.info("PASS: FP16 Normalizer value matching: Expected = {0} Actual = {1}".format(
                    ref_hdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
        else:
            ref_sdr_normalizing_factor = 0x3C00
            if pixel_normalizer_info.NormalizationFactor != ref_sdr_normalizing_factor:
                logging.error(
                    "FAIL: FP16 Normalizer value not matching: Expected = {0} Actual = {1}".format(
                        ref_sdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                gdhm.report_driver_bug_os("Verification failed as FP16 Normalizer value not matching: Expected = {0} Actual = {1}"
                            .format(ref_sdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                return False
            else:
                logging.info(
                    "PASS: FP16 Normalizer value matching: Expected = {0} Actual = {1}".format(
                        ref_sdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
            return True

    def verify_input_csc_programming(self, args: hdr_utility.PlaneArgs, pixel_format, pipe, plane):
        plane_icsc_reg_name = "PlaneInputCscCoeff"
        logging.info("PASS: Plane iCSC is enabled. Expected = ENABLE, Actual = ENABLE")
        ref_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        prog_val = csc_utility.get_plane_csc_coeffmatrix_from_reg(self.gfx_index, pipe, plane, plane_icsc_reg_name, self.regs, self.mmio_interface)
        if args.color_space is "YCBCR":
            prog_val1 = csc_utility.transform_yuv_to_rgb_matrix(prog_val)
        else:
            prog_val1 = prog_val
        if args.color_space == "YCBCR" and args.gamut == "P2020":
            ref_val = color_constants.YCbCr2RGB_2020_FullRange
        elif args.color_space == "YCBCR" and args.gamut == "P709":
            ref_val = color_constants.YCbCr2RGB_709_FullRange
        elif args.color_space == "YCBCR" and args.gamut == "P601":
            ref_val = color_constants.YCbCr2RGB_601_FullRange
        logging.debug("iCSC RefValue : %s" % ref_val)
        bpc = common_utility.get_bpc_from_pixel_format(pixel_format)
        ##
        # If color space is YCBCR, iCSC is not used for full range to limited range conversion.
        # So we don't need any range conversion.
        input = color_enums.ColorSpace.RGB if args.color_space == "RGB" else color_enums.ColorSpace.YUV
        if args.color_space != "YCBCR":
            if args.range == "STUDIO":
                ref_val1 = csc_utility.scale_csc_for_range_conversion(bpc, input, color_enums.ColorSpace.RGB,
                                                                      ref_val,
                                                                      color_enums.ConversionType.STUDIO_TO_FULL)
            elif args.range == "FULL":
                ref_val1 = csc_utility.scale_csc_for_range_conversion(bpc, input, color_enums.ColorSpace.RGB,
                                                                      ref_val, color_enums.ConversionType.FULL_TO_STUDIO)
            else:
                ref_val1 = ref_val
        else:
            ref_val1 = ref_val

        if csc_utility.compare_csc_coeff(prog_val1, ref_val1) is False:
            logging.error("FAIL: InputCSC coeff Verification Failed on Adapter :{0} Pipe {1}".format(
                self.gfx_index, pipe))
            gdhm.report_driver_bug_os("InputCSC Coeff Verification Failed on Adapter :{0} Pipe {1}".format(
                self.gfx_index, pipe))
            return False
        else:
            logging.info("PASS: InputCSC coeff Verification successful on Adapter :{0} Pipe {1}".format(
                self.gfx_index, pipe))

        conv_type = color_enums.ConversionType.STUDIO_TO_FULL if args.range == "STUDIO" else color_enums.ConversionType.FULL_TO_STUDIO
        if csc_utility.verify_plane_pre_post_offsets(self.gfx_index, self.regs, plane_icsc_reg_name, pipe, plane,
                                                     bpc,
                                                     input, color_enums.ColorSpace.RGB, conv_type,
                                                     self.mmio_interface):
            logging.info(
                "PASS: Verification of InputCSC pre and post offsets on Adapter :{0} Pipe {1} is successful".format(
                    self.gfx_index, pipe))
        else:
            logging.error(
                "FAIL:Verification of InputCSC pre and post offsets on Adapter :{0} Pipe {1} failed".format(
                    self.gfx_index, pipe))
            gdhm.report_driver_bug_os("Verification of InputCSC pre and post offsets on Adapter :{0} Pipe {1} failed".format(
                    self.gfx_index, pipe))
            return False
        return True

    def verify_plane_degamma_programming(self, args: hdr_utility.PlaneArgs, plane, pipe):
        no_samples = 131
        ref_lut = []
        prog_lut = gamma_utility.get_plane_degamma_lut_from_reg(self.regs, plane, pipe, no_samples)
        if args.gamma == "G22":
            ref_lut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC
        elif args.gamma == "G2084":
            ref_lut = color_constants.EOTF2084_DECODE_131_SAMPLES_24BPC

        if gamma_utility.compare_ref_and_programmed_gamma_lut(prog_lut, ref_lut) is False:
            logging.error("FAIL: Plane PreCSC Gamma Verification failed on Adapter : {0} Plane {1} Pipe {2}".format(
                self.gfx_index, plane, pipe))
            gdhm.report_driver_bug_os("Plane PreCSC Gamma Verification failed on Adapter : {0} Plane {1} Pipe {2}".format(
                self.gfx_index, plane, pipe))
            return False
        else:
            logging.info("PASS: Plane PreCSC Gamma Verification successful on Adapter : {0} Plane {1} Pipe {2}".format(
                self.gfx_index, plane, pipe))
        return True

    def verify_plane_csc_programming(self, args: hdr_utility.PlaneArgs, pixel_format, plane, pipe):
        ref_coeff = []
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        plane_csc_reg_name = "PlaneCscCoeff"
        prog_coeff = csc_utility.get_plane_csc_coeffmatrix_from_reg(self.gfx_index, pipe, plane, plane_csc_reg_name,
                                                                    self.regs, self.mmio_interface)
        if is_hdr_enabled:
            if args.gamut == "P709":
                ref_coeff = color_constants.BT709_TO_BT2020_RGB
            else:
                if args.gamut == "P2020":
                    ref_coeff = color_constants.BT2020_TO_BT709_RGB
        elif args.gamut == "P2020":
            #For SRGB for NON-LINEAR
            ref_coeff = color_constants.BT2020_TO_BT709_RGB
        else:
            ##
            # In case of WCG
            ref_coeff = color_constants.BT709_TO_BT2020_RGB
        if pixel_format in (flip.SB_PIXELFORMAT.SB_R16G16B16A16F, flip.SB_PIXELFORMAT.SB_R16G16B16X16F):
            logging.debug("Multiplication Scalefactor {0}".format(self.plane_csc_scalefactor))

        if color_constants.source_pixel_format_dict[pixel_format].__contains__('RGB_16161616_FLOAT'):
            ref_coeff = csc_utility.multiply_csc_with_scale_factor(ref_coeff, self.plane_csc_scalefactor)

        if csc_utility.compare_csc_coeff(prog_coeff, ref_coeff) is False:
            logging.error("FAIL: %s - Plane CSC verification failed for Plane : {0} on Adapter {1} Pipe {2}".format(plane, self.gfx_index, pipe))
            gdhm.report_driver_bug_os("Verification of Plane CSC verification for Plane : {0} on Adapter {1} Pipe {2} failed"
                                        .format(plane, self.gfx_index, pipe))
            return False
        else:
            logging.info("PASS: %s - Plane CSC verification successful for Plane : {0} on Adapter {1} Pipe {2}".format(plane, self.gfx_index, pipe))

        return True

    def verify_plane_gamma_programming(self, plane, pipe, args: hdr_utility.PlaneArgs, content_luminance, gamma_mode):
        no_samples = 35
        ref_lut = []
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        plane_str = str(plane)
        prog_lut = gamma_utility.get_plane_gamma_lut_from_register(self.regs, plane_str, pipe, no_samples)
        if is_hdr_enabled:
            if gamma_mode != 1:
                logging.error("FAIL: Plane gamma linear mode programmed incorrectly. Expected = 1 Actual = {0}".format(
                    gamma_mode))
                return False
            else:
                logging.info(
                    "PASS: Plane gamma linear mode programmed correctly. Expected = 1 Actual = {0}".format(gamma_mode))
                # if self.gamma == "G2084":
                #    @todo :Tone mapping H2H has not been enabled in the driver by default,
                #     will be enabling this verification when OS comes up with the policy for tone mapping by display
                # elif(self.gamut =="P709" and self.gamma == "G10"):
                #    @todo :Tone mapping H2S has not been enabled in the driver by default,
                #     @will be enabling this verification when OS comes up with the policy for tone mapping by display

                if args.gamut == "P709" and args.gamma == "G22":
                    for index in range(0, 33):
                        ref_lut.append(common_utility.round_up_div(
                            33 * color_constants.SDR_HDR_TONE_MAPPING_FACTOR_8_24 * content_luminance,
                            color_constants.DEFAULT_SDR_WHITE_LEVEL))

                    ref_lut.append(common_utility.round_up_div(
                        33 * color_constants.SDR_HDR_TONE_MAPPING_FACTOR_8_24 * 7 * content_luminance,
                        color_constants.DEFAULT_SDR_WHITE_LEVEL))

                    ref_lut.append(common_utility.round_up_div(
                        33 * color_constants.SDR_HDR_TONE_MAPPING_FACTOR_8_24 * 3 * content_luminance,
                        color_constants.DEFAULT_SDR_WHITE_LEVEL))

                    if gamma_utility.compare_ref_and_programmed_gamma_lut(prog_lut, ref_lut) is False:
                        logging.error(
                            "FAIL: Plane PostCSC Gamma Verification failed on Adapter : {0} Plane {1} Pipe {2}".format(
                                self.gfx_index, plane, pipe))
                        return False
                    else:
                        logging.info(
                            "PASS: Plane PostCSC Gamma Verification successful on Adapter : {0} Plane {1} Pipe {2}".format(
                                self.gfx_index, plane, pipe))
                    return True

        else:
            ref_lut = color_constants.SRGB_ENCODE_35_SAMPLES_24BPC
            logging.debug("Gamma Mode : {0}".format(gamma_mode))

            if gamma_mode != 0:
                logging.error(
                    "FAIL: Plane gamma non linear mode programmed incorrectly. Expected = 0 Actual = {0}"
                        .format(gamma_mode))
                return False
            else:
                logging.info(
                    "PASS: Plane gamma non linear mode programmed correctly. Expected = 0 Actual = {0}".format(
                        gamma_mode))
                if gamma_utility.compare_ref_and_programmed_gamma_lut(prog_lut, ref_lut) is False:
                    logging.error(
                        "FAIL: Plane PostCSC Gamma Verification failed on Adapter : {0} Plane {1} Pipe {2}".format(
                            self.gfx_index, plane, pipe))
                    return False
                else:
                    logging.info(
                        "PASS: Plane PostCSC Gamma Verification successful on Adapter : {0} Plane {1} Pipe {2}".format(
                            self.gfx_index, plane, pipe))
                return True
