#################################################################################################
# @file         verify_pipe.py
# @brief        This script comprises of PipeColorVerifier Base class which has all the attributes
#               required by the Pipe Blocks, verification modules which will be overloaded
#               by the Derived Classes specific to each Generation when required.
# @author       Smitha B
#################################################################################################
import logging
import ctypes
from typing import Union
import DisplayRegs
from DisplayRegs.DisplayOffsets import TransDDiOffsetsValues, AviInfoOffsetsValues, Hw3dLutOffsetsValues, \
    VideoDipCtlOffsetsValues, TransMsaMiscOffsetsValues
from Libs.Core.wrapper.driver_escape_args import ColorModel
from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Libs.Core import registry_access, display_essential, etl_parser
from Tests.Color.Common import color_escapes, color_mmio_interface, color_enums, color_constants
from Tests.Color.Common import color_igcl_escapes, color_igcl_wrapper
from Tests.Color.Common import common_utility, csc_utility, hdr_utility, gamma_utility
from Tests.Color.Verification import feature_basic_verify
from Tests.Color.Common.color_enums import ColorSpace, ConversionType
from Libs.Core.logger import gdhm

##
# @brief        PipeColorVerifier Base Class


class PipeColorVerifier:
    gfx_index = None
    platform = None
    regs = None
    mmio_interface = color_mmio_interface.ColorMmioInterface()
    sdr_degamma_lut_prec = 16
    sdr_degamma_lut_size = 35
    gamma_lut_size = 1020

    def verify_sdp_data(self, gfx_index, display_and_adapter_info, is_lfp, current_pipe, hdr_caps_support, psr_status):
        status = True
        ##
        # Bit 3 of DPCD Address 0x2210(DPRX_FEATURE_ENUMERATION_LIST) is expected to be set,
        # which indicates the capability of the sink, based on this source decides to send the SDP
        dprx_ftr_enum_list_val = color_escapes.fetch_dpcd_data(
            color_enums.DP1p4VscExtSdpDPCDOffset.VSC_EXT_SDP_DPCD.value,
            display_and_adapter_info)
        vsc_sdp_ext_for_colorimetry_supported = common_utility.get_bit_value(dprx_ftr_enum_list_val, 3, 3)
        msa_misc_offset = self.regs.get_trans_msa_misc_offset(current_pipe)

        if vsc_sdp_ext_for_colorimetry_supported:
            # # For an eDP HDR panel, Bit 6 of DPCD Address 0x341 also indicates the support for Colorimetry/Metadata
            # via SDP.
            if is_lfp:
                edp_hdr_caps = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_HDR_CAPS_BYTE1.value,
                                                             display_and_adapter_info)
                edp_hdr_support_sdp_for_colorimetry = common_utility.get_bit_value(edp_hdr_caps, 6, 6)
                if hdr_caps_support:
                    if edp_hdr_support_sdp_for_colorimetry == 0:
                        logging.warning("Panel has Aux Based HDR Support and Colorimetry with SDP support was False")
                        logging.info("Aux Based HDR Panel connected. SKipping VSC SDP data check")
                        return True
                if edp_hdr_support_sdp_for_colorimetry == 0:
                    logging.error("EDP HDR: DPCD has no support for colorimetry")
                    return False

            ##
            # DP Source device sets the 6th Bit of the MSA_MISC register to indicate that the PixelEncoding/Colorimetry
            # information is being set via VSC and the Sink should ignore the Misc1 bit 7 data.
            msa_misc_value = self.mmio_interface.read(gfx_index, msa_misc_offset.MsaMiscOffset)
            msa_misc_data = self.regs.get_trans_msa_misc_info(current_pipe, TransMsaMiscOffsetsValues(MsaMiscOffset=msa_misc_value))
            if msa_misc_data == 0:
                logging.error(
                    "FAIL : MSA MISC1 Bit 6 has not been set by the DP Source to indicate Colorimetry/PixelEncoding via VSC")
                return False
            logging.info(
                "PASS : MSA MISC1 Bit 6 has been set by the DP Source to indicate Colorimetry/PixelEncoding via VSC")

            ##
            # Register: VIDEO_DIP_CTL - VideodipEnableVsc bit(20th bit)
            # Verifying the 20th bit of VIDEO_DIP_CTL Register to be set to 1
            video_dip_ctl_offset = self.regs.get_video_dip_ctl_offset(current_pipe).VideoDipOffset
            video_dip_ctl_data = self.mmio_interface.read(self.gfx_index, video_dip_ctl_offset)
            video_dip_enable_vsc_status = self.regs.get_video_dip_info(current_pipe, VideoDipCtlOffsetsValues(VideoDipOffset=video_dip_ctl_data))

            # For Gen12 - VSC DIP VSC status should be enabled for both PSR enable & disable
            # For Gen13 + MTL - VSC DIP VSC Status should be enabled only for PSR disable case
            if is_lfp and psr_status is False:
                if video_dip_enable_vsc_status.video_dip_ctl_off == 0:
                    logging.error("FAIL : Enable VSC Bit(20) of the VIDEO DIP CTL register has not been set")
                    return False
            logging.info("PASS : Enable VSC Bit(20) of the VIDEO DIP CTL register has been set")
            ##
            # Performing the Header Bytes verification
            # Note : For an eDP Interface, the VSC SDP may also be used to communicate the PSR control information
            # "Port":"PORT_A","Pipe":"PIPE_A","Protocol"
            # DIP HEADER BYTES
            # HB0 - Secondary data Packet type = 0x0
            # HB1 - Secondary data Packet type = 0x7
            # HB2 - BIT [4:0] Revision Number
            #       01h - supports only 3D stereo
            #       02h - supports 3D stereo + PSR
            #       03h - supports 3D stereo + PSR2
            #       04h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate
            #       05h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate + Pixel Encoding/Colorimetry format
            #      BIT [7:5] - Reserved - all Zeros
            # HB3 - BIT [4:0] Number of Valid data bytes
            #       01h - VSC SDP supports only 3D stereo (HB2 = 01h)
            #       08h - VSC SDP supports 3D stereo + PSR (HB2 = 02h)
            #       0Ch - VSC SDP supports 3D stereo + PSR2 (HB2 = 03h)
            #       0Eh - supports 3D stereo + PSR/PSR2 + Y-co_ordinate (HHB2 = 04h)
            #       13h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate + Pixel Encoding/Colorimetry format (HB2 = 05h)
            #      BIT [7:5] - Reserved - all Zeros
            if video_dip_enable_vsc_status.video_dip_ctl_off_vsc == 0x2:  # H/W controls data only
                info_frame = etl_parser.get_event_data(etl_parser.Events.INFO_FRAME_DATA)
                if info_frame is None:
                    logging.error("VSC DIP Data is not found in ETL")
                    set_timing_event_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING_COLOR)
                    if set_timing_event_output is None:
                        logging.info("No Event found for SET_TIMING in ETL")
                        logging.info("As Modeset not happened,Infoframe will not send to HAL(Expected)")
                        return True
                    else:
                        return False
                for vsc_data in info_frame:
                    if (vsc_data.Pipe == 'PIPE_' + current_pipe) and (vsc_data.Port == "PORT_" + current_pipe) \
                            and (vsc_data.DipType == "DIP_VSC") and (vsc_data.Enable is True):
                        if vsc_data.DipSize == 0:
                            logging.error("VSC_SDP enable is true but vsc_data_DipSize is zero")
                            status = False

                        sdp_data = vsc_data.DipData.split('-')
                        logging.info(f"VSC DIP Data= {sdp_data}")
                        if int(sdp_data[0]) != 0:
                            logging.error("HB0 val Expected= 0, Actual= {0}".format(sdp_data[0]))
                            status = False
                        if int(sdp_data[1]) != 7:
                            logging.error("HB1 val Expected= 0x7, Actual= {0}".format(sdp_data[1]))
                            status = False
                        ##
                        # HB2(Revision Number) == 0x5 indicates VSC SDP supporting 3D stereo, PSR2, and Pixel Encoding/
                        # Colorimetry Format indication
                        if int(sdp_data[2]) != 5:
                            logging.error(f"HB2 val Expected= 0x5, Actual= {0}".format(sdp_data[2]))
                            status = False

                        ##
                        # HB3(Number of Valid Bytes) == 0x13 indicates VSC SDP supporting 3D stereo, + PSR2,
                        # + Pixel Encoding/ Colorimetry Format indication (HB2 = 05h)
                        if int(sdp_data[3]) != 13:
                            logging.error(f"HB3 val Expected= 0x13, Actual= {0}".format(sdp_data[3]))
                            status = False

                        ##
                        # Extracting PixelEncoding and Colorimetry Format for comparison
                        pixel_encoding = int(sdp_data[16]) >> 4
                        colorimetry_format = int(sdp_data[16]) & 0xf
                        if pixel_encoding != color_enums.PixelEncoding.RGB.value:
                            logging.error("DB16[7:4] pixel format Expected= RGB,  Actual = {0}".format(
                                color_enums.PixelEncoding.RGB.name))
                            status = False
            """
            if is_lfp is False:
                # Header verification DIP_DRM and DIP_AVI follows HDMI_PROTOCOL
                info_frame = etl_parser.get_event_data(etl_parser.Events.INFO_FRAME_DATA)
                if info_frame is None:
                    logging.error("Infoframe is not found in ETL")
                    set_timing_event_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING_COLOR)
                    if set_timing_event_output is None:
                        logging.info("No Event found for SET_TIMING in ETL")
                        logging.info("As Modeset not happened,Infoframe will not send to HAL(Expected)")
                        return True
                    else:
                        return False

                for info in info_frame:
                    if (info.Pipe == 'PIPE_' + current_pipe) and (info.Port == "PORT_" + current_pipe) \
                            and (info.DipType == "DIP_AVI"):
                        avi_data = info.DipData.split('-')
                        logging.info(f"AVI DIP Data= {avi_data}")
                        # AVI HEADER ID
                        if int(avi_data[0]) != 0:
                            logging.error(f" val Expected= 0x1, Actual= {0}".format(drm_data[0]))
                            status = False
                        # AVI HEADER TYPE
                        if int(avi_data[1]) != 130:
                            logging.error(f" val Expected= 0x1, Actual= {0}".format(drm_data[0]))
                            status = False
                        # AVI HEADER BYTE 1
                        if int(avi_data[2]) != 29:
                            logging.error(f" val Expected= 0x1, Actual= {0}".format(drm_data[0]))
                            status = False
                        # AVI HEADER BYTE 2
                        if int(avi_data[2]) != 76:
                            logging.error(f" val Expected= 0x1, Actual= {0}".format(drm_data[0]))
                            status = False
                    if (info.Pipe == 'PIPE_' + current_pipe) and (info.Port == "PORT_" + current_pipe) \
                            and (info.DipType == "DIP_DRM"):
                        drm_data = info.DipData.split('-')
                        logging.info(f"AVI DIP Data= {drm_data}")
                        # DRM Version:
                        if int(drm_data[0]) != 1:
                            logging.error(f" val Expected= 0x1, Actual= {0}".format(drm_data[0]))
                            status = False
                        # DRM Length:
                        if int(drm_data[1]) != 26:
                            logging.error(f" val Expected= 0x1A, Actual= {0}".format(drm_data[1]))
                            status = False
                        # DRM Type:
                        if int(drm_data[2]) != 135:
                            logging.error(f" val Expected= 0x87, Actual= {0}".format(drm_data[2]))
                            status = False
            """
        return status

    def verify_metadata(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], display: str, is_lfp: bool,
                        pipe: str, display_and_adapter_info, pcon=False) -> bool:

        if type(args) is hdr_utility.E2EPipeArgs:

            ##
            # Verify if Default and Flip Metadata are matching
            if hdr_utility.verify_default_and_flip_metadata_from_etl(args.default_metadata,
                                                                     args.flip_metadata) is False:
                return False

            reference_metadata = hdr_utility.rearrange_default_metadata(args.default_metadata.programmed_metadata)

            if is_lfp:
                target_nits = expected_max_cll = expected_po_max_cll = args.desired_max_cll
                expected_max_fall = expected_po_max_fall = args.desired_max_fall

                ##
                # Updating the reference metadata with the MaxCLL and MaxFALL from the EDID
                reference_metadata[9] = expected_max_cll
                reference_metadata[11] = reference_metadata[12] = expected_max_fall
        else:
            if is_lfp:
                target_nits = expected_max_cll = expected_po_max_cll = args.reference_metadata[11]
                expected_max_fall = expected_po_max_fall = args.reference_metadata[12]
            reference_metadata = args.reference_metadata

        if is_lfp:
            edp_hdr_caps = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_HDR_CAPS_BYTE1.value,
                                                         display_and_adapter_info)
            sdp_enable = common_utility.get_bit_value(edp_hdr_caps, 6, 6)
            if sdp_enable == 0:
                if hdr_utility.verify_metadata_aux_dpcd(display_and_adapter_info,
                                                        expected_max_cll, expected_max_fall, target_nits,
                                                        expected_po_max_cll, expected_po_max_fall) is False:
                    return False
                return True
        ##
        # Take the latest Default Metadata from the list of metadata available
        programmed_metadata = hdr_utility.fetch_programmed_metadata(self.gfx_index, self.platform, display, is_lfp,
                                                                    pipe, pcon)
        logging.info("Reference Metadata {0}".format(reference_metadata))
        logging.info("Programmed Metadata {0}".format(programmed_metadata))
        index = 0
        for reg_val, ref_val in zip(programmed_metadata, reference_metadata):
            if reg_val != ref_val:
                logging.error(
                    "Metadata programming not matching at index {0} Programmed Val : {1} Expected Val : {2} on Adapter : {3} Pipe : {4}".format(
                        index,
                        reg_val, ref_val, self.gfx_index, pipe))
                return False
            index += 1
        logging.info(
            "PASS : Metadata Verification is successful on Adapter {0} and Pipe {1}".format(self.gfx_index, pipe))
        return True


    def verify_pipe_csc_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe,
                                    reg_name="PipeCscCoeff", feature=None):
        if type(args) is hdr_utility.E2EPipeArgs:
            if args.escape_csc is None or args.escape_csc.__len__() == 0:
                input_matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
            else:
                input_matrix = args.escape_csc

            if feature == "WCG":
                rgb_xyz_matrix = color_constants.BT2020_RGB_to_XYZ_conversion
                xyz_rgb_matrix = color_constants.XYZ_to_BT709_RGB_conversion

            elif feature == "HDR":
                rgb_xyz_matrix = color_constants.BT2020_RGB_to_XYZ_conversion
                xyz_rgb_matrix = color_constants.XYZ_to_BT2020_RGB_conversion

            else:
                rgb_xyz_matrix = color_constants.BT709_RGB_to_XYZ_conversion
                xyz_rgb_matrix = color_constants.XYZ_to_BT709_RGB_conversion

            interim_matrix1 = csc_utility.matrix_multiply_3x3(args.os_relative_csc, rgb_xyz_matrix)
            interim_matrix2 = csc_utility.matrix_multiply_3x3(xyz_rgb_matrix, interim_matrix1)
            reference_pipe_csc = csc_utility.matrix_multiply_3x3(input_matrix, interim_matrix2)

        else:
            is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
            reference_pipe_csc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            if is_hdr_enabled:
                if args.panel_caps == color_enums.PanelCaps.SDR_709_RGB or args.panel_caps == color_enums.PanelCaps.SDR_709_YUV420:
                    reference_pipe_csc = color_constants.BT2020_TO_BT709_RGB
                elif args.panel_caps == color_enums.PanelCaps.HDR_DCIP3_RGB or args.panel_caps == color_enums.PanelCaps.HDR_DCIP3_YUV420:
                    reference_pipe_csc = color_constants.BT2020_TO_DCIP3_RGB
            else:
                if (args.panel_caps in (color_enums.PanelCaps.SDR_BT2020_RGB, color_enums.PanelCaps.SDR_BT2020_YUV420,
                                        color_enums.PanelCaps.HDR_BT2020_RGB,
                                        color_enums.PanelCaps.HDR_BT2020_YUV420)):
                    reference_pipe_csc = color_constants.BT709_TO_BT2020_RGB

        programmed_pipe_csc = csc_utility.get_pipe_csc_coeffmatrix_from_reg(self.gfx_index, pipe, reg_name, self.regs,
                                                                            self.mmio_interface)
        logging.info("*" * 128)
        logging.info("Programmed CSC {0}".format(programmed_pipe_csc))
        logging.info("Reference CSC {0}".format(reference_pipe_csc))
        logging.info("*" * 128)
        if csc_utility.wa_compare_csc_coeff(programmed_pipe_csc, reference_pipe_csc) is False:
            logging.error("FAIL : Verification of Pipe CSC Coeff matrix on Adapter : {0}  Pipe : {1} failed".format(
                self.gfx_index,
                pipe))
            gdhm.report_driver_bug_os("Verification of Pipe CSC Coeff matrix on Adapter : {0}  Pipe : {1} failed"
                                        .format(self.gfx_index,pipe))
            return False
        logging.info(
            "PASS : Verification of Pipe CSC Coeff matrix on Adapter : {0} Pipe : {1} is successful".format(
                self.gfx_index,
                pipe))
        return True

    def verify_pipe_gamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe,
                                      cc_block):
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        self.gamma_lut_size = 1020 if is_hdr_enabled else 1024
        lut_size = 515 if cc_block == "CC1" else 513
        if type(args) is hdr_utility.E2EPipeArgs:
            if is_hdr_enabled:
                if args.escape_correction_glut is None or args.escape_correction_glut.__len__() == 0:
                    reference_gamma_lut = gamma_utility.generate_reference_pipe_gamma_lut_with_pixel_boost(
                        color_constants.INPUT_BaseLUT_513Samples_8_24_FORMAT_Gen13, args.pixel_boost,
                        args.os_relative_lut)
                else:
                    reference_gamma_lut = gamma_utility.prepare_correction_ref_gamma_lut_in_hdr_mode(
                        base_lut=color_constants.INPUT_BaseLUT_513Samples_8_24_FORMAT_Gen13,
                        correction_lut=args.escape_correction_glut, os_relative_lut=args.os_relative_lut,
                        pixel_boost=args.pixel_boost)
            else:
                if args.glut_curve_type == 'CORRECTION_LUT_IN_SDR':
                    reference_gamma_lut = gamma_utility.prepare_correction_ref_gamma_lut_in_sdr_mode(
                        args.escape_correction_glut, args.os_relative_lut, lut_size)

                else:
                    if args.glut_curve_type is None:
                        args.glut_curve_type = "SRGB_GAMMA_CURVE"

                    reference_gamma_lut = gamma_utility.prepare_full_ref_gamma_lut_in_sdr_mode(args.os_relative_lut,
                                                                                               lut_size,
                                                                                               args.glut_curve_type)
            __temp_ref_lut = []
            for index in range(0, len(reference_gamma_lut), 3):
                __temp_ref_lut.append(reference_gamma_lut[index])

            reference_gamma_lut = __temp_ref_lut
            reference_gamma_lut = reference_gamma_lut if cc_block == "CC1" else reference_gamma_lut[0:513]

            logging.info("Reference Programmed Gamma LUT")
            logging.info("*" * 128)
            logging.info("{0}".format(reference_gamma_lut))
            logging.info("*" * 128)
            logging.info("")
            logging.info("")

            reg_args = registry_access.StateSeparationRegArgs(self.gfx_index)
            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayFeatureControl")
            gamma_register_write_using_mmio = common_utility.get_bit_value(reg_value, 22, 22)

            ##
            # DSB Buffer Logic - only if need for debug
            programmed_gamma_lut = gamma_utility.get_programmed_dsb_pipe_gamma_data_from_etl(self.regs, pipe,
                                                                                             cc_block,
                                                                                             args.dsb_gamma_dump,
                                                                                             self.gamma_lut_size,
                                                                                             args.is_smooth_brightness,
                                                                                             args.step_index)
            logging.debug("ETL Based Programmed DSB Gamma LUT")
            logging.debug("*" * 128)
            logging.debug("{0}".format(programmed_gamma_lut))
            logging.debug("*" * 128)
            logging.debug("")
            logging.debug("")


            if gamma_utility.compare_ref_and_programmed_gamma_log_lut(reference_gamma_lut,
                                                                      programmed_gamma_lut) is False:
                logging.debug("Error : ETL Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".
                              format(self.gfx_index, pipe))

            ##
            # Performing verification with the values collected by reading the registers
            programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register(self.gfx_index, self.regs,
                                                                                  cc_block, pipe,
                                                                                  self.gamma_lut_size)

            __temp_prog_lut = []
            for index in range(0, len(programmed_gamma_lut), 3):
                __temp_prog_lut.append(programmed_gamma_lut[index])
            programmed_gamma_lut = __temp_prog_lut
            programmed_gamma_lut = programmed_gamma_lut if cc_block == "CC1" else programmed_gamma_lut[0:513]

            logging.info("Register based Programmed Gamma LUT")
            logging.info("")
            logging.info("*" * 128)
            logging.info("{0}".format(programmed_gamma_lut))
            logging.info("*" * 128)
            logging.info("")
            logging.info("")
            if is_hdr_enabled is False:
                if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut,
                                                                      programmed_gamma_lut) is False:
                    logging.error("FAIL : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} "
                                  "failed ".format(
                        self.gfx_index,
                        pipe))
                    gdhm.report_driver_bug_os("Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} "
                                  "failed ".format(self.gfx_index,pipe))
                    return False
                else:
                    logging.info("PASS : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} "
                                 "successful ".format(
                        self.gfx_index,
                        pipe))
            else:
                if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut,
                                                                      programmed_gamma_lut) is False:
                    logging.error(
                        "FAIL : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                            self.gfx_index,
                            pipe))
                    gdhm.report_driver_bug_os("Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} "
                                              "failed ".format(self.gfx_index, pipe))
                    return False
                else:
                    logging.info(
                        "PASS : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".format(
                            self.gfx_index,
                            pipe))
        else:
            if is_hdr_enabled:
                ##
                # Performing verification with the values collected by reading the registers
                reference_gamma_lut = color_constants.OETF_2084_10KNits_513Samples_8_24_FORMAT

                programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register(self.gfx_index, self.regs,
                                                                                      cc_block, pipe,
                                                                                      self.gamma_lut_size)

                __temp_prog_lut = []
                for index in range(0, len(programmed_gamma_lut), 3):
                    __temp_prog_lut.append(programmed_gamma_lut[index])
                programmed_gamma_lut = __temp_prog_lut
                programmed_gamma_lut = programmed_gamma_lut if cc_block == "CC1" else programmed_gamma_lut[0:513]

                logging.info("Reference Programmed Gamma LUT")
                logging.info("*" * 128)
                logging.info("{0}".format(reference_gamma_lut))
                logging.info("*" * 128)
                logging.info("")
                logging.info("")

                logging.info("Programmed Gamma LUT")
                logging.info("*" * 128)
                logging.info("{0}".format(programmed_gamma_lut))
                logging.info("*" * 128)
                logging.info("")
                logging.info("")

                if gamma_utility.compare_ref_and_programmed_gamma_log_lut(reference_gamma_lut,
                                                                          programmed_gamma_lut) is False:
                    logging.error(
                        "FAIL : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                            self.gfx_index,
                            pipe))
                    gdhm.report_driver_bug_os("Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed "
                                    .format(self.gfx_index,pipe))
                    return False
                logging.info("PASS : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} "
                             "successful ".format(self.gfx_index,pipe))
            else:
                reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC if cc_block == "CC1" else color_constants.SRGB_ENCODE_515_SAMPLES_16BPC[
                                                                                                              0:513]

                programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register(self.gfx_index, self.regs,
                                                                                      cc_block, pipe,
                                                                                      self.gamma_lut_size)
                final_lut = []
                for index in range(0, len(programmed_gamma_lut), 3):
                    final_lut.append(programmed_gamma_lut[index])

                programmed_gamma_lut = final_lut

                logging.info("Reference Programmed Gamma LUT")
                logging.info("*" * 128)
                logging.info("{0}".format(reference_gamma_lut))
                logging.info("*" * 128)
                logging.info("")
                logging.info("")

                logging.info("Programmed Gamma LUT")
                logging.info("*" * 128)
                logging.info("{0}".format(programmed_gamma_lut))
                logging.info("*" * 128)
                logging.info("")
                logging.info("")

                if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut,
                                                                      programmed_gamma_lut) is False:
                    logging.error(
                        "FAIL : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                            self.gfx_index,
                            pipe))
                    gdhm.report_driver_bug_os("Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed "
                                        .format(self.gfx_index,pipe))
                    return False
                logging.info(
                    "PASS : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".format(
                        self.gfx_index,
                        pipe))

        return True

    ##
    # @brief         Function to verify - register verification - OCSC enable/disable, OCSC COEFF, PRE/POST
    #                offset verification
    # @param[in]     gfx_index - gfx_0 or gfx_1
    # @param[in]     platform - platform Info
    # @param[in]     pipe - pipe_info
    # @param[in]     bpc - BPC 8,10,12
    # @param[in]     input - RGB/YCBCR Color Space enum
    # @param[in]     output - RGB/YCBCR Color Space enum
    # @param[in]     conv_type - FULL_TO_STUDIO,STUDIO_TO_FULL,STUDIO_TO_STUDIO,FULL_TO_FULL
    # @return        status - True on Success, False otherwise
    def verify_output_csc_programming(self, pipe: str, bpc: int, input: ColorSpace, output: ColorSpace,
                                      conv_type: ConversionType,
                                      color_model: int = ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value,
                                      igcl_input_csc=None) -> bool:

        color_model_dict = {2: "RGB2YCbCr_601_FullRange", 3: "RGB2YCbCr_709_FullRange",
                            4: "RGB2YCbCr_2020_FullRange"}
        base_ref_coeff = None
        programmed_value = None
        output_csc_coeff_reg_name = "PipeOutputCscCoeff"
        is_hdr_supported = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        base_value = csc_utility.get_pipe_csc_coeffmatrix_from_reg(self.gfx_index, pipe, output_csc_coeff_reg_name,
                                                                   self.regs, self.mmio_interface)

        if input == ColorSpace.RGB and output == ColorSpace.YUV:
            programmed_value = csc_utility.transform_rgb_to_yuv_matrix(base_value)
            if is_hdr_supported:
                base_ref_coeff = color_constants.RGB2YCbCr_2020_FullRange
            else:
                if color_model == ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value:
                    base_ref_coeff = color_constants.RGB2YCbCr_709_FullRange
                else:
                    base_ref_coeff = getattr(color_constants, color_model_dict[color_model])

        elif input == ColorSpace.RGB and output == ColorSpace.RGB:
            programmed_value = base_value
            if igcl_input_csc is not None:
                base_ref_coeff = igcl_input_csc
            else:
                base_ref_coeff = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

            logging.info("Base Ref is {0}".format(base_ref_coeff))
        ref_value = csc_utility.scale_csc_for_range_conversion(bpc, input, output, base_ref_coeff, conv_type)
        logging.info("Programmed OutputCSC {0}".format(programmed_value))
        logging.info("Reference OutputCSC {0}".format(ref_value))
        if csc_utility.compare_csc_coeff(programmed_value, ref_value):
            logging.info("PASS : Verification of Output CSC Coeff matrix on Adapter :{0} Pipe{1} is successful ".format(
                self.gfx_index, pipe))
        else:
            logging.error(
                "FAIL : Verification of Output CSC Coeff matrix on Adapter :{0} Pipe{1} failed".format(self.gfx_index,
                                                                                                       pipe))
            gdhm.report_driver_bug_os("Verification of Output CSC Coeff matrix on Adapter :{0} Pipe{1} failed"
                                                                            .format(self.gfx_index, pipe))
            return False

        if csc_utility.verify_pipe_pre_post_offsets(self.regs, self.gfx_index, output_csc_coeff_reg_name, pipe, bpc,
                                                    input, output, conv_type, self.mmio_interface):
            logging.info(
                "PASS: Verification of Output CSC pre and post offsets on Adapter :{0} Pipe{1} is successful".format(
                    self.gfx_index, pipe))
        else:
            logging.error("FAIL:Verification of Output CSC pre and post offsets on Adapter :{0} Pipe{1} failed".format(
                self.gfx_index, pipe))
            gdhm.report_driver_bug_os("Verification of Output CSC pre and post offsets on Adapter :{0} Pipe{1} failed".format(
                self.gfx_index, pipe))
            return False

        return True

    ##
    # @brief         Function to verify - register verification - avi infoframe quantisation verification
    # @param[in]     transcoder - transcoder Info
    # @param[in]     plane - 1,2,3,4,5,6,7
    # @param[in]     pipe - A,B,C,D
    # @param[in]     expected_range - LIMITED/FULL
    # @return        status - True on Success, False otherwise
    def verify_quantization_range(self, transcoder: str, plane: str, pipe: str, expected_range: int) -> bool:
        status = False
        transcoder = DisplayRegs.DisplayRegsInterface.TranscoderType(transcoder).name
        trans_ddi_mode_dict = {0: "HDMI", 2: "DP_MST", 3: "DP_SST", 4: "DP2_0_32B_SYMBOL_MODE"}

        trans_ddi_func_offset = self.regs.get_trans_ddi_offsets(transcoder)
        data = self.mmio_interface.read(self.gfx_index, trans_ddi_func_offset.FuncCtrlReg)
        trans_ddi_value = self.regs.get_trans_ddi_info(transcoder, TransDDiOffsetsValues(FuncCtrlReg=data))

        data_byte = 1 # based on AVI trancoder prog - it will be always 1
        avi_dip_offsets = self.regs.get_avi_info_offsets(data_byte, pipe)
        avi_dip_data = self.mmio_interface.read(self.gfx_index, avi_dip_offsets.QuantRange)
        avi_dip_value = self.regs.get_avi_info(data_byte, pipe, AviInfoOffsetsValues(QuantRange=avi_dip_data))

        if "HDMI" in trans_ddi_mode_dict[trans_ddi_value.DdiModeSelect]:
            quantisation_range = common_utility.get_bit_value(avi_dip_value.QuantRange, 26, 27)
        else:
            quantisation_range = common_utility.get_bit_value(avi_dip_value.QuantRange, 13, 15)

        if quantisation_range != expected_range:
            logging.error(
                " FAIL : Quant Range on Adapter:{0} Transcoder:{1} Pipe:{2} Expected:{3} and Actual:{4}".format(
                    self.gfx_index, transcoder, pipe, expected_range, quantisation_range))
            gdhm.report_driver_bug_os("Failed to get Quantization Range on Adapter:{0} Transcoder:{1} Pipe:{2} Expected:{3} and Actual:{4}"
                            .format(self.gfx_index, transcoder, pipe, expected_range, quantisation_range))
        else:
            logging.info(
                " PASS : Quant Range on Adapter:{0} Transcoder:{1} Pipe:{2} Expected:{3} and Actual:{4}".format(
                    self.gfx_index, transcoder, pipe, expected_range, quantisation_range))
            status = True
        return status


    ##
    # @brief         Function to verify HW_3D_LUT data
    # @param[in]     gfx_index - gfx_0 or gfx_1
    # @param[in]     pipe - A,B,C,D
    # @param[in]     expected_lut - list
    # @return        status - True on Success, False otherwise
    def verify_hw3dlut(self, gfx_index: str, platform, port, pipe: str, transcoder, target_id, expected_lut: list):
        status = False
        prog_lut = []

        Lut_offsets = self.regs.get_3dlut_offsets(pipe)

        self.mmio_interface.write(gfx_index, Lut_offsets.LutIndex, 0x00002000)
        for i in range(0, 4913):
            reg_val_lut_3d_data = self.mmio_interface.read(gfx_index, Lut_offsets.LutData)
            reg_val_lut_3d_data = self.regs.get_hw3dlut_info(pipe, Hw3dLutOffsetsValues(LutData=reg_val_lut_3d_data))
            reg_blue = common_utility.get_bit_value(reg_val_lut_3d_data.Lut3Ddata, 0, 9)
            reg_green = common_utility.get_bit_value(reg_val_lut_3d_data.Lut3Ddata, 10, 19)
            reg_red = common_utility.get_bit_value(reg_val_lut_3d_data.Lut3Ddata, 20, 29)
            prog_lut.append(reg_red)
            prog_lut.append(reg_green)
            prog_lut.append(reg_blue)

        self.mmio_interface.write(gfx_index, Lut_offsets.LutIndex, 0x00000000)

        ##
        # Lut data verify
        index = 0
        for reg_val, ref_val in zip(prog_lut, expected_lut):
            if reg_val != ref_val:
                logging.error(
                    "LUT values not matching Index : {0} ProgrammedVal : {1} Expected val : {2} ".format(index,
                                                                                                reg_val, ref_val))
                logging.error(" FAIL : HW 3D LUT Data programming verification on Adapter:{0} Pipe:{1} failed ".format(
                    self.gfx_index, pipe))
                gdhm.report_driver_bug_os("HW 3D LUT Data programming verification on Adapter:{0} Pipe:{1} failed"
                                          .format(self.gfx_index, pipe))
                return status
            index += 1
        logging.info(
            " PASS : HW 3D LUT Data programming verification on Adapter:{0} Pipe:{1} passed ".format(self.gfx_index,
                                                                                                     pipe))

        status = True
        return status

    def verify_lace(self):
        logging.info("Base Class : LACE Verification")

    def verify_scaler(self):
        logging.info("Base Class : Scaler Verification")
