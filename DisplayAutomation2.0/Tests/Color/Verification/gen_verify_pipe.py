#################################################################################################
# @file         gen_verify_pipe.py
# @brief        This script comprises of Pipe Verification Modules specific to each Generation
#               defined under respective Gen class definition.
#               All the Gen Classes inherit from the Base Class PipeColorVerifier
#               The AutoGen register interface will be instantiated and initialized based on platform
#               and gfx_index.
#               APIs exposed :
#               1. get_pipe_verifier_instance()
#               In addition, APIs from the BaseClass can be overloaded and exposed as required
# @author       Smitha B
#################################################################################################
from Tests.Color.Verification.verify_pipe import *


##
# @brief        Exposed API to get the pipe verifier instance based on Platform and GfxIndex
# @param[in]    platform, str - Ex :'ICLLP', 'JSL', 'EHL'
# @param[in]    gfx_index, str - Ex : 'gfx_0', 'gfx_1'
# @return       PipeColorVerifier object based on Platform and GfxIndex
def get_pipe_verifier_instance(platform: str, gfx_index: str) -> PipeColorVerifier:
    if platform in ['ICLLP', 'JSL', 'EHL']:
        return Gen11PipeColorVerifier(platform, gfx_index)

    if platform in ['LKF1']:
        return Gen11PipeColorVerifier(platform, gfx_index)

    if platform in ['TGL', 'DG1', 'RKL', 'ADLS']:
        return Gen12PipeColorVerifier(platform, gfx_index)

    if platform in ['DG2', 'ADLP']:
        return Gen13PipeColorVerifier(platform, gfx_index)

    if platform in ['DG3', 'MTL', 'ELG']:
        return Gen14PipeColorVerifier(platform, gfx_index)

    if platform in ['LNL']:
        return Gen15PipeColorVerifier(platform, gfx_index)

    if platform in ['PTL', 'CLS', 'NVL']:
        return Gen16PipeColorVerifier(platform, gfx_index)

##
# @brief        PipeColorVerifier class for Gen11 derived from PipeColorVerifier
class Gen11PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.is_multi_seg = True

    def verify_pipe_gamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe, cc_block):
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        if type(args) is hdr_utility.E2EPipeArgs:
            reference_gamma_lut = gamma_utility.generate_reference_pipe_gamma_lut_with_pixel_boost(
                color_constants.INPUT_3SEGMENT_LUT_524Samples_8_24FORMAT,
                args.pixel_boost,
                args.os_relative_lut)
            programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register_legacy(self.gfx_index, self.platform, is_hdr_enabled, pipe,
                                            self.gamma_lut_size)

            if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                logging.error(
                    "FAIL : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                        self.gfx_index,
                        pipe))
                return False
            logging.info(
                "PASS : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".format(
                    self.gfx_index,
                    pipe))
        else:
            reference_gamma_lut = color_constants.MultiSegment_OETF_2084_Encode_524_Samples_16bpc
            programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register_legacy(self.gfx_index, self.regs,
                                                                                         is_hdr_enabled, pipe,
                                                                                         self.gamma_lut_size)
            if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                return False
        return True


##
# @brief        PipeColorVerifier class for Gen12 derived from PipeColorVerifier
class Gen12PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        # Total samples in HDR : 524
        # In case of HDR: Size of MultiSegmentLut : 9(Already taken care in the func)
        # Size of Extended Registers Lut : 3 (Already taken care in the func) (Applies for SDR)
        # Size of PalPrec : 512 (Applies for SDR case also)
        self.gamma_lut_size = 1024

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
            reg_val_lut_3d_data = self.regs.get_hw3dlut_info(pipe,
                                                             Hw3dLutOffsetsValues(LutData=reg_val_lut_3d_data))
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
                                                                                                         reg_val,
                                                                                                         ref_val))
                logging.error(
                    " FAIL : HW 3D LUT Data programming verification on Adapter:{0} Pipe:{1} failed ".format(
                        self.gfx_index, pipe))

                return status
            index += 1
        logging.info(
            " PASS : HW 3D LUT Data programming verification on Adapter:{0} Pipe:{1} passed ".format(self.gfx_index,
                                                                                                     pipe))

        status = True
        return status

    def verify_pipe_degamma_programming(self, pipe_args, pipe, cc_block):
        reference_degamma_lut = color_constants.SRGB_Decode_35_Samples_16bpc
        programmed_degamma_lut = gamma_utility.get_pipe_degamma_lut_from_register(self.regs,
                                                                                  cc_block, pipe,
                                                                                  self.sdr_degamma_lut_size)
        logging.info("Reference DeGamma Lut {0}".format(reference_degamma_lut))
        logging.info("Programmed Degamma Lut {0}".format(programmed_degamma_lut))
        if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_degamma_lut, programmed_degamma_lut) is False:
            logging.error("FAIL : Pipe De Gamma Verification failed on Adapter : {0}  Pipe : {1}"
                          .format(self.gfx_index, pipe))
            return False
        logging.info("PASS : Pipe De Gamma Verification successful on Adapter : {0}  Pipe : {1}"
                     .format(self.gfx_index, pipe))
        return True

    ##
    # Verify Pipe Gamma for E2E HDR and SDR cases
    def verify_pipe_gamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe, cc_block):
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        lut_size = 524 if is_hdr_enabled else 515
        if type(args) is hdr_utility.E2EPipeArgs:
            ##
            # Performing verification with the values collected from the ETL
            if is_hdr_enabled:
                if args.escape_correction_glut is None or args.escape_correction_glut.__len__() == 0:
                    reference_gamma_lut = gamma_utility.generate_reference_pipe_gamma_lut_with_pixel_boost(
                        color_constants.INPUT_3SEGMENT_LUT_524Samples_8_24FORMAT,
                        args.pixel_boost,
                        args.os_relative_lut)
                else:
                    reference_gamma_lut = gamma_utility.prepare_correction_ref_gamma_lut_in_hdr_mode(
                        base_lut=color_constants.INPUT_3SEGMENT_LUT_524Samples_8_24FORMAT,
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
            # # @todo : All the additional logs to be removed once the Driver precision issue has been
            #  resolved-16014267622
            logging.debug("Reference Gamma")
            logging.debug("*" * 128)
            logging.debug("{0}".format(reference_gamma_lut))
            logging.debug("*" * 128)
            logging.debug("")
            logging.debug("")

            ##
            # Performing verification with the values collected by reading the registers
            if args.is_smooth_brightness is False:
                programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register_legacy(self.gfx_index, self.regs, is_hdr_enabled, pipe,
                                                self.gamma_lut_size)

                __temp_prog_lut = []
                for index in range(0, len(programmed_gamma_lut), 3):
                    __temp_prog_lut.append(programmed_gamma_lut[index])
                programmed_gamma_lut = __temp_prog_lut

                logging.info("")
                logging.info("Register based Programmed Gamma LUT")
                logging.info("*" * 128)
                logging.info("{0}".format(programmed_gamma_lut))
                logging.info("*" * 128)
                logging.info("")

                if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                    logging.error(
                        "FAIL : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                            self.gfx_index,
                            pipe))

                    return False
                logging.info(
                    "PASS : Register Based Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".format(
                        self.gfx_index,
                        pipe))
        else:
            reference_gamma_lut = color_constants.MultiSegment_OETF_2084_Encode_524_Samples_16bpc if is_hdr_enabled else color_constants.SRGB_ENCODE_515_SAMPLES_16BPC
            programmed_gamma_lut = gamma_utility.get_pipe_gamma_lut_from_register_legacy(self.gfx_index, self.regs,
                                                                                         is_hdr_enabled, pipe,
                                                                                         self.gamma_lut_size)
            final_gamma_lut = []
            for index in range(0, len(programmed_gamma_lut), 3):
                final_gamma_lut.append(programmed_gamma_lut[index])
            programmed_gamma_lut = final_gamma_lut
            if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                logging.error(
                    "FAIL : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} failed ".format(
                        self.gfx_index,
                        pipe))
                return False
            logging.info(
                "PASS : Pipe Gamma Verification on Adapter : {0}  Pipe : {1} successful ".format(
                    self.gfx_index,
                    pipe))
        return True

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
            if video_dip_enable_vsc_status == 0:
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
                        and (vsc_data.DipType == "DIP_VSC"):
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
        return status


##
# @brief        PipeColorVerifier class for Gen13 derived from PipeColorVerifier
class Gen13PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.sdr_degamma_lut_size = 131

    def select_reference_lut_for_degamma_block(self, dglut_curve_type, cc_block):

        ##
        # By default, if no IGCL LUT is applied, driver will enable DGLUT block with SRGB Degamma Curve
        ref_dglut = color_constants.SRGB_DECODE_131SAMPLES_16BPC if cc_block == "CC1" \
            else color_constants.SRGB_DECODE_131SAMPLES_12BPC[0:129]

        if dglut_curve_type == 'UNITY_LUT':
            ref_dglut = color_constants.SRGB_DECODE_131SAMPLES_16BPC if cc_block == "CC1" \
        else color_constants.UNITY_DECODE_131SAMPLES_12BPC[0:129]

        if dglut_curve_type == 'SRGB_GAMMA_CURVE':
            ref_dglut = color_constants.SRGB_DECODE_131SAMPLES_16BPC if cc_block == "CC1" \
        else color_constants.SRGB_GAMMA_CURVE_FOR_DEGAMMA_131SAMPLES_12BPC[0:129]

        return ref_dglut

    def verify_pipe_degamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe,
                                        cc_block):
        if type(args) is hdr_utility.E2EPipeArgs:
            reference_degamma_lut = self.select_reference_lut_for_degamma_block(args.dglut_curve_type, cc_block)
        else:
            reference_degamma_lut = color_constants.SRGB_DECODE_131SAMPLES_16BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                           0:129]

        logging.info("*" * 128)
        logging.info("Reference Degamma lut is")
        logging.info(reference_degamma_lut)
        logging.info("*" * 128)
        logging.info("")
        logging.info("")
        self.sdr_degamma_lut_size = 131 if cc_block == "CC1" else 129
        programmed_degamma_lut = gamma_utility.get_pipe_degamma_lut_from_register(self.regs, cc_block, pipe,
                                                                                  self.sdr_degamma_lut_size)
        logging.info("*" * 128)
        logging.info("Programmed Degamma lut is")
        logging.info(programmed_degamma_lut)
        logging.info("*" * 128)
        logging.info("")
        logging.info("")

        if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_degamma_lut, programmed_degamma_lut) is False:
            logging.error("FAIL : Pipe PreCSC Verification failed on Adapter : {0}  Pipe : {1}"
                          .format(self.gfx_index, pipe))
            return False
        logging.info("PASS : Pipe PreCSC Verification successful on Adapter : {0}  Pipe : {1}"
                     .format(self.gfx_index, pipe))
        return True


##
# @brief        PipeColorVerifier class for Gen14 derived from PipeColorVerifier
class Gen14PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.sdr_degamma_lut_size = 131

    def select_reference_luts_for_degamma_block(self, dglut_curve_type, cc_block):

        ##
        # By default, if no IGCL LUT is applied, driver will enable DGLUT block with SRGB Degamma Curve
        ref_dglut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131_SAMPLES_24BPC[
                                                                                                        0:129]
        if dglut_curve_type == 'UNITY_LUT':
            ref_dglut = color_constants.UNITY_DECODE_131SAMPLES_24BPC if cc_block == "CC1" else color_constants.UNITY_DECODE_131SAMPLES_24BPC[
                                                                                                        0:129]

        if dglut_curve_type == 'SRGB_GAMMA_CURVE':
            ref_dglut = color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc if cc_block == "CC1" else color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc[
                                                                                                                      0:129]

        return ref_dglut


    def verify_pipe_degamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe, cc_block):
        if type(args) is hdr_utility.E2EPipeArgs:
            reference_degamma_lut = self.select_reference_luts_for_degamma_block(args.dglut_curve_type, cc_block)
        else:
            reference_degamma_lut = color_constants.SRGB_DECODE_131SAMPLES_16BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                           0:129]
        logging.info("*"*128)
        logging.info("Reference Degamma lut is")
        logging.info(reference_degamma_lut)
        logging.info("*"*128)
        logging.info("")
        logging.info("")
        self.sdr_degamma_lut_size = 131 if cc_block == "CC1" else 129
        programmed_degamma_lut = gamma_utility.get_pipe_degamma_lut_from_register(self.regs, cc_block, pipe, self.sdr_degamma_lut_size)
        logging.info("*" * 128)
        logging.info("Programmed Degamma lut is")
        logging.info(programmed_degamma_lut)
        logging.info("*" * 128)
        logging.info("")
        logging.info("")

        if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_degamma_lut, programmed_degamma_lut) is False:
            logging.error("FAIL : Pipe PreCSC Verification failed on Adapter : {0}  Pipe : {1}"
                          .format(self.gfx_index, pipe))
            return False
        logging.info("PASS : Pipe PreCSC Verification successful on Adapter : {0}  Pipe : {1}"
                     .format(self.gfx_index, pipe))
        return True


##
# @brief        PipeColorVerifier class for Gen15 derived from PipeColorVerifier
class Gen15PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.sdr_degamma_lut_size = 131

    def select_reference_luts_for_degamma_block(self, dglut_curve_type, cc_block):

        ##
        # By default, if no IGCL LUT is applied, driver will enable DGLUT block with SRGB Degamma Curve
        ref_dglut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                        0:129]
        if dglut_curve_type == 'UNITY_LUT':
            ref_dglut = color_constants.UNITY_DECODE_131SAMPLES_24BPC if cc_block == "CC1" else color_constants.UNITY_DECODE_131SAMPLES_24BPC[
                                                                                                        0:129]

        if dglut_curve_type == 'SRGB_GAMMA_CURVE':
            ref_dglut = color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc if cc_block == "CC1" else color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc[
                                                                                                                      0:129]

        return ref_dglut

    def verify_pipe_degamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe, cc_block):
        if type(args) is hdr_utility.E2EPipeArgs:
            reference_degamma_lut = self.select_reference_luts_for_degamma_block(args.dglut_curve_type, cc_block)
        else:
            reference_degamma_lut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                            0:129]
        self.sdr_degamma_lut_size = 131 if cc_block == "CC1" else 129
        programmed_degamma_lut = gamma_utility.get_pipe_degamma_lut_from_register(self.regs, cc_block, pipe, self.sdr_degamma_lut_size)
        if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_degamma_lut, programmed_degamma_lut) is False:
            logging.error("FAIL : Pipe PreCSC Verification failed on Adapter : {0}  Pipe : {1}"
                          .format(self.gfx_index, pipe))
            return False
        logging.info("PASS : Pipe PreCSC Verification successful on Adapter : {0}  Pipe : {1}"
                     .format(self.gfx_index, pipe))
        return True


##
# @brief        PipeColorVerifier class for Gen16 derived from PipeColorVerifier
class Gen16PipeColorVerifier(PipeColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.sdr_degamma_lut_size = 131

    def select_reference_luts_for_degamma_block(self, dglut_curve_type, cc_block):

        ##
        # By default, if no IGCL LUT is applied, driver will enable DGLUT block with SRGB Degamma Curve
        ref_dglut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                        0:129]
        if dglut_curve_type == 'UNITY_LUT':
            ref_dglut = color_constants.UNITY_DECODE_131SAMPLES_24BPC if cc_block == "CC1" else color_constants.UNITY_DECODE_131SAMPLES_24BPC[
                                                                                                        0:129]

        if dglut_curve_type == 'SRGB_GAMMA_CURVE':
            ref_dglut = color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc if cc_block == "CC1" else color_constants.SRGB_DECODE_With_SRGB_Gamma_Curve_131_samples_24bpc[
                                                                                                                      0:129]

        return ref_dglut

    def verify_pipe_degamma_programming(self, args: Union[hdr_utility.E2EPipeArgs, hdr_utility.DFTPipeArgs], pipe, cc_block):
        if type(args) is hdr_utility.E2EPipeArgs:
            reference_degamma_lut = self.select_reference_luts_for_degamma_block(args.dglut_curve_type, cc_block)
        else:
            reference_degamma_lut = color_constants.SRGB_DECODE_131_SAMPLES_24BPC if cc_block == "CC1" else color_constants.SRGB_DECODE_131SAMPLES_12BPC[
                                                                                                            0:129]
        self.sdr_degamma_lut_size = 131 if cc_block == "CC1" else 129
        programmed_degamma_lut = gamma_utility.get_pipe_degamma_lut_from_register(self.regs, cc_block, pipe, self.sdr_degamma_lut_size)
        if gamma_utility.compare_ref_and_programmed_gamma_lut(reference_degamma_lut, programmed_degamma_lut) is False:
            logging.error("FAIL : Pipe PreCSC Verification failed on Adapter : {0}  Pipe : {1}"
                          .format(self.gfx_index, pipe))
            return False
        logging.info("PASS : Pipe PreCSC Verification successful on Adapter : {0}  Pipe : {1}"
                     .format(self.gfx_index, pipe))
        return True
