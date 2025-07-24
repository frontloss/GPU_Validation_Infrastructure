#####################################################################################################################################
# @file         cnl_verify_register_programming.py
# @addtogroup   PyLibs_HDMI
# @brief        Verifies Register Programming
# @remarks
#               ref: cnl_verify_register_programming.py \n
#               Python class to validate ICL HDMI register programming \n
#               <ul>
#               <li> ref:  verify_registers        	\n copybrief verify_registers \n
#               </li>
#               </ul>
# @author       Girish Y D
####################################################################################################################################
import importlib
import logging

from Tests.Hdmi.utility.edid_mode_info import *
from Tests.Hdmi.verification.verify_helper import validate_feature
from registers.mmioregister import MMIORegister


##
# @brief        CnlVerifyRegisterProgramming Class
class CnlVerifyRegisterProgramming:
    ddi_select_map = dict([
        (0b000, 'None'),
        (0b001, 'B'),
        (0b010, 'C'),
        (0b011, 'D'),
        (0b100, 'E'),
        (0b101, 'F')
    ])
    edp_input_select_map = dict([
        (0b000, 'A'),
        (0b101, 'B'),
        (0b110, 'C')
    ])
    DDI_SUFFIX_ARRAY = ['A', 'B', 'C', 'D', 'E', 'F']
    DITHERING_BPC_ARRAY = [6, 8, 10, 12]
    DISPLAY_TYPE_ARRAY = ["HDMI", "DVI", "DP_MST", "DP_SST"]
    BITSPERCOLOR_ARRAY = [6, 8, 10, 12]
    test_parameters = None
    edid_parameters = None
    pipe_suffix = None
    trans_suffix = None
    ddi_suffix = None

    ##
    # @brief        Test Parameter is of object of class EDIDModeInfo()
    # @param[in]    test_parameters - Paraameters to be tested
    # @param[in]    edid_parameters - Parameters in the EDID
    def __init__(self, test_parameters, edid_parameters):
        self.test_parameters = test_parameters
        self.edid_parameters = edid_parameters
        self.platform = 'cnl'
        result, result_dict = self.get_enabled_pipe_transcoder_ddi_suffix()
        self.pipe_suffix = result_dict.get("pipe_suffix")
        self.trans_suffix = result_dict.get("trans_suffix")
        self.ddi_suffix = result_dict.get("ddi_suffix")
        if result is False or self.pipe_suffix is None or self.trans_suffix is None or self.ddi_suffix is None:
            err_msg = "NO transcoder enabled for display port %s" % self.test_parameters.display_port
            raise Exception(err_msg)

        if self.ddi_suffix not in self.DDI_SUFFIX_ARRAY:
            err_msg = "ERROR : Incorrect self.ddi_suffix : %s" % self.ddi_suffix
            raise Exception(err_msg)

    ##
    # @brief        Verify Plane ctl1
    # @return       result
    def verify_plane_ctl_1(self):
        result = True
        logging.debug("****************************************************************************")

        ##
        # PLANE_CTL_1
        plane_ctl_reg_module = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform)
        plane_ctl_1_reg_offset_name = 'PLANE_CTL_1' + '_' + self.pipe_suffix
        plane_ctl_1_reg = MMIORegister.read("PLANE_CTL_REGISTER", plane_ctl_1_reg_offset_name, self.platform)

        ##
        # Verify Plane is Enabled  (bits range 31:31)
        plane_enable = plane_ctl_1_reg.plane_enable
        expected_plane_enable = plane_ctl_reg_module.__getattribute__("plane_enable_ENABLE")
        feature_name = plane_ctl_1_reg_offset_name + '_' + "plane_enable"
        result &= validate_feature(plane_enable, expected_plane_enable, feature_name)
        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verify_video_dip_gcp
    # @return       result
    def verify_video_dip_gcp(self):
        result = True
        logging.debug("****************************************************************************")
        ##
        # VIDEO_DIP_GCP
        video_dip_gcp_reg_module = importlib.import_module("registers.%s.VIDEO_DIP_GCP_REGISTER" % self.platform)
        video_dip_gcp_reg_offset_name = 'VIDEO_DIP_GCP' + '_' + self.pipe_suffix
        video_dip_gcp_reg = MMIORegister.read("VIDEO_DIP_GCP_REGISTER", video_dip_gcp_reg_offset_name, self.platform)

        ##
        # Verify gcp_color_indication  (bits range 2:2)
        gcp_color_indication = video_dip_gcp_reg.gcp_color_indication
        expected_gcp_color_indication_attribute_name = ""
        if self.test_parameters.expectedBPC in [6, 8]:
            expected_gcp_color_indication_attribute_name = "gcp_color_indication_DONT_INDICATE"
        elif self.test_parameters.expectedBPC in [10, 12]:
            expected_gcp_color_indication_attribute_name = "gcp_color_indication_INDICATE"
        else:
            logging.error("ERROR : Incorrect test_parameters.expectedBPC  : %s",
                          self.test_parameters.expectedBPC)
            return False
        expected_gcp_color_indication = video_dip_gcp_reg_module.__getattribute__(
            expected_gcp_color_indication_attribute_name)
        feature_name = video_dip_gcp_reg_offset_name + '_' + "gcp_color_indication"
        result &= validate_feature(gcp_color_indication, expected_gcp_color_indication, feature_name)
        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verigy Video dip ctl
    # @return       result - Video dip ctl result
    def verify_video_dip_ctl(self):
        result = True
        logging.debug("****************************************************************************")

        ##
        # VIDEO_DIP_CTL
        video_dip_ctl_reg_module = importlib.import_module("registers.%s.VIDEO_DIP_CTL_REGISTER" % self.platform)
        video_dip_ctl_reg_offset_name = 'VIDEO_DIP_CTL' + '_' + self.pipe_suffix
        video_dip_ctl_reg = MMIORegister.read("VIDEO_DIP_CTL_REGISTER", video_dip_ctl_reg_offset_name, self.platform)

        ##
        # Verify vdip_enable_gcp is enabled if bpp is not 8   (bits range 16:16)
        vdip_enable_gcp = video_dip_ctl_reg.vdip_enable_gcp
        expected_vdip_enable_gcp_attribute_name = ""
        if self.test_parameters.expectedBPC in [6, 8]:
            expected_vdip_enable_gcp_attribute_name = "vdip_enable_gcp_DISABLE_GCP_DIP"
        elif self.test_parameters.expectedBPC in [10, 12]:
            expected_vdip_enable_gcp_attribute_name = "vdip_enable_gcp_ENABLE_GCP_DIP"
        else:
            logging.error("ERROR : Incorrect test_parameters.expectedBPC  : %s",
                          self.test_parameters.expectedBPC)
            return False
        expected_vdip_enable_gcp = video_dip_ctl_reg_module.__getattribute__(expected_vdip_enable_gcp_attribute_name)
        feature_name = video_dip_ctl_reg_offset_name + '_' + "vdip_enable_gcp"
        result &= validate_feature(vdip_enable_gcp, expected_vdip_enable_gcp, feature_name)

        ##
        # If vdip_enable_gcp is enabled call verify VIDEO_DIP_GCP_REGISTER
        if vdip_enable_gcp == video_dip_ctl_reg_module.__getattribute__("vdip_enable_gcp_ENABLE_GCP_DIP"):
            result &= self.verify_video_dip_gcp()

        ##
        # Check vdip_enable_avi is enabled for hdmi  (Bits Range 12:12)
        vdip_enable_avi = video_dip_ctl_reg.vdip_enable_avi
        expected_vdip_enable_avi = video_dip_ctl_reg_module.__getattribute__("vdip_enable_avi_ENABLE_AVI_DIP")
        feature_name = video_dip_ctl_reg_offset_name + '_' + "vdip_enable_avi"
        result &= validate_feature(vdip_enable_avi, expected_vdip_enable_avi, feature_name)

        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verify Pipe
    # @return       result - Pipe verification result
    def verify_pipe_misc(self):
        result = True
        logging.debug("****************************************************************************")
        ##
        # PIPE_MISC
        pipe_misc_reg_module = importlib.import_module("registers.%s.PIPE_MISC_REGISTER" % self.platform)
        pipe_misc_reg_offset_name = 'PIPE_MISC' + '_' + self.pipe_suffix
        pipe_misc_reg = MMIORegister.read("PIPE_MISC_REGISTER", pipe_misc_reg_offset_name, self.platform)

        ##
        # Check yuv420 is enabled or not (Bits Range 27:27)
        yuv420_enable = pipe_misc_reg.yuv420_enable
        expected_yuv420_enable_attribute_name = ""
        if self.test_parameters.expectedPixelFormat in ["RGB", "YUV444"]:
            expected_yuv420_enable_attribute_name = "yuv420_enable_DISABLE"
        elif self.test_parameters.expectedPixelFormat == "YUV420":
            expected_yuv420_enable_attribute_name = "yuv420_enable_ENABLE"
        else:
            logging.error("ERROR : Incorrect test_parameters.expectedPixelFormat  : %s",
                          self.test_parameters.expectedPixelFormat)
            return False
        expected_yuv420_enable = pipe_misc_reg_module.__getattribute__(expected_yuv420_enable_attribute_name)
        feature_name = pipe_misc_reg_offset_name + '_' + "yuv420_enable"
        result &= validate_feature(yuv420_enable, expected_yuv420_enable, feature_name)

        ##
        # If yuv420 is enabled check yuv420 mode is FULL BLEND MODE
        # Currently YUV420 BYPASS MODE is supported, so always when YUV420 is enabled it will be in FULL BLEND MODE
        if yuv420_enable == pipe_misc_reg_module.__getattribute__("yuv420_enable_ENABLE"):
            # yuv420_mode Bits range 26:26
            yuv420_mode = pipe_misc_reg.yuv420_mode
            expected_yuv420_mode = pipe_misc_reg_module.__getattribute__("yuv420_mode_FULL_BLEND")
            feature_name = pipe_misc_reg_offset_name + '_' + "yuv420_mode"
            result &= validate_feature(yuv420_mode, expected_yuv420_mode, feature_name)

        ##
        # Check pipe output color Space value is RGB or YUV
        # pipe_output_color_space = hdmi_helper.get_register_value_by_range(pipe_misc_reg.asUint, 11, 11,
        #                                                                   pipe_misc_reg_offset_name + '_' + "pipe_output_color_space")
        pipe_output_color_space = pipe_misc_reg.pipe_output_color_space_select
        expected_pipe_output_color_space_attribute_name = ""
        if self.test_parameters.expectedPixelFormat == "RGB":
            expected_pipe_output_color_space_attribute_name = "pipe_output_color_space_select_RGB"
        elif self.test_parameters.expectedPixelFormat in ["YUV444", "YUV420"]:
            expected_pipe_output_color_space_attribute_name = "pipe_output_color_space_select_YUV"
        else:
            logging.error("ERROR : Incorrect test_parameters.expectedPixelFormat  : %s",
                          self.test_parameters.expectedPixelFormat)
            return False
        expected_pipe_output_color_space = pipe_misc_reg_module.__getattribute__(
            expected_pipe_output_color_space_attribute_name)
        feature_name = pipe_misc_reg_offset_name + '_' + "pipe_output_color_space"
        result &= validate_feature(pipe_output_color_space, expected_pipe_output_color_space, feature_name)

        ##
        # If Dithering Enabled Enabled check dithering bpc
        # dithering_enable - Bits Range 4:4)
        dithering_enable = pipe_misc_reg.dithering_enable
        if dithering_enable:
            ##
            # Check dithering Bits per Color   - (Bits Range 5:7)
            dithering_bpc = pipe_misc_reg.dithering_bpc
            expected_dithering_bpc_attribute_name = ""
            if self.test_parameters.expectedBPC in self.DITHERING_BPC_ARRAY:
                expected_dithering_bpc_attribute_name = "bits_per_color_%s_BPC" % self.test_parameters.expectedBPC
            else:
                logging.error("ERROR : Incorrect test_parameters.expectedBPC  : %s",
                              self.test_parameters.expectedBPC)
                return False
            expected_dithering_bpc = pipe_misc_reg_module.__getattribute__(expected_dithering_bpc_attribute_name)
            feature_name = pipe_misc_reg_offset_name + '_' + "dithering_bpc"
            result &= validate_feature(dithering_bpc, expected_dithering_bpc, feature_name)

        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verify Trans Configuration
    # @return       result - Trans Configuration result
    def verify_trans_conf(self):
        result = True
        logging.debug("****************************************************************************")
        ##
        # TRANS_CONF
        trans_conf_reg_module = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % self.platform)
        trans_conf_reg_offset_name = 'TRANS_CONF' + '_' + self.trans_suffix
        trans_conf_reg = MMIORegister.read("TRANS_CONF_REGISTER", trans_conf_reg_offset_name, self.platform)

        #
        # Verify transcoder_enable  is Enabled  (Bits Range  31:31)
        transcoder_enable = trans_conf_reg.transcoder_enable
        expected_transcoder_enable = trans_conf_reg_module.__getattribute__("transcoder_enable_ENABLE")
        feature_name = trans_conf_reg_offset_name + '_' + "transcoder_enable"
        result &= validate_feature(transcoder_enable, expected_transcoder_enable, feature_name)

        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verify Trans ddi Function ctl
    # @return       result - Result of the verification
    def verify_trans_ddi_func_ctl(self):
        result = True
        logging.debug("****************************************************************************")
        ##
        # TRANS_DDI_FUNC_CTL
        trans_ddi_func_ctl_reg_module = importlib.import_module(
            "registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (self.platform))
        trans_ddi_func_ctl_reg_offset_name = 'TRANS_DDI_FUNC_CTL' + '_' + self.trans_suffix
        trans_ddi_func_ctl_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl_reg_offset_name,
                                                   self.platform)

        ##
        # trans_ddi_function_enable is Enabled (Bits Range 31:31)
        trans_ddi_function_enable = trans_ddi_func_ctl_reg.trans_ddi_function_enable
        expected_trans_ddi_function_enable = trans_ddi_func_ctl_reg_module.__getattribute__(
            "trans_ddi_function_enable_ENABLE")
        feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "trans_ddi_function_enable"
        result &= validate_feature(trans_ddi_function_enable, expected_trans_ddi_function_enable, feature_name)

        ##
        # ddi_select  (Bits Range  28:30)
        ddi_select = trans_ddi_func_ctl_reg.ddi_select
        expected_ddi_select_attribute_name = ""
        if self.ddi_suffix == 'A':
            expected_ddi_select_attribute_name = "ddi_select_NONE"
        else:
            expected_ddi_select_attribute_name = "ddi_select_DDI_%s" % (self.ddi_suffix)
        expected_ddi_select = trans_ddi_func_ctl_reg_module.__getattribute__(expected_ddi_select_attribute_name)
        feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "ddi_select"
        result &= validate_feature(ddi_select, expected_ddi_select, feature_name)

        ##
        # trans_ddi_mode_select  (Bits Range 24:26)
        trans_ddi_mode_select = trans_ddi_func_ctl_reg.trans_ddi_mode_select
        expected_trans_ddi_mode_select_attribute_name = ""
        if self.edid_parameters.display_type in self.DISPLAY_TYPE_ARRAY:
            expected_trans_ddi_mode_select_attribute_name = "trans_ddi_mode_select_%s" % self.edid_parameters.display_type
        else:
            logging.error("ERROR : Incorrect edid_parameters.display_type %s" % self.edid_parameters.display_type)
            return False
        expected_trans_ddi_mode_select = trans_ddi_func_ctl_reg_module.__getattribute__(
            expected_trans_ddi_mode_select_attribute_name)
        feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "trans_ddi_mode_select"
        result &= validate_feature(trans_ddi_mode_select, expected_trans_ddi_mode_select, feature_name)
        ##
        # Check Bits per Color (Bits Range 20:22)
        bits_per_color = trans_ddi_func_ctl_reg.bits_per_color
        expected_bits_per_color_attribute_name = ""
        if self.test_parameters.expectedBPC in self.BITSPERCOLOR_ARRAY:
            expected_bits_per_color_attribute_name = "bits_per_color_%s_BPC" % self.test_parameters.expectedBPC
        else:
            logging.error("ERROR : Incorrect test_parameters.bits_per_color %s" % self.test_parameters.bits_per_color)
            return False
        expected_bits_per_color = trans_ddi_func_ctl_reg_module.__getattribute__(expected_bits_per_color_attribute_name)
        feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "bits_per_color"
        result &= validate_feature(bits_per_color, expected_bits_per_color, feature_name)

        ##
        # If the display  is HDMI verify high_tmds_char_rate , scrambling bits
        if trans_ddi_mode_select == trans_ddi_func_ctl_reg_module.__getattribute__("trans_ddi_mode_select_HDMI"):
            if self.test_parameters.expectedSymbolClockMHz <= 0:
                logging.error(
                    "ERROR : Incorrect test_parameters.expectedSymbolClockMHz %s" % self.test_parameters.expectedSymbolClockMHz)
                return False
            ##
            # Check TMDS Car rate is enabled if pixel clock is > 340mhz else disabled (Bits Range 4:4)
            high_tmds_char_rate = trans_ddi_func_ctl_reg.high_tmds_char_rate
            expected_high_tmds_char_rate = trans_ddi_func_ctl_reg_module.__getattribute__("high_tmds_char_rate_DISABLE")
            if self.test_parameters.expectedSymbolClockMHz > 340:
                expected_high_tmds_char_rate = trans_ddi_func_ctl_reg_module.__getattribute__(
                    "high_tmds_char_rate_ENABLE")
            feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "high_tmds_char_rate"
            result &= validate_feature(high_tmds_char_rate, expected_high_tmds_char_rate, feature_name)
            ##
            # check hdmi scrambling enabled if pixel Clock > 340
            # check hdmi scrambling enabled for pixel Clock <= 340 based on EDID bit for lte_340Mcsc_Scramble
            # (Bits Range 0:0)
            hdmi_scrambling_enabled = trans_ddi_func_ctl_reg.hdmi_scrambling_enabled
            expected_hdmi_scrambling_enabled = trans_ddi_func_ctl_reg_module.__getattribute__(
                "hdmi_scrambling_enabled_DISABLE")
            if self.test_parameters.expectedSymbolClockMHz > 340 or self.edid_parameters.LTE340MhzScramble is True:
                expected_hdmi_scrambling_enabled = trans_ddi_func_ctl_reg_module.__getattribute__(
                    "hdmi_scrambling_enabled_ENABLE")
            feature_name = trans_ddi_func_ctl_reg_offset_name + '_' + "hdmi_scrambling_enabled"
            result &= validate_feature(hdmi_scrambling_enabled, expected_hdmi_scrambling_enabled, feature_name)

        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Verify Registers
    # @return       result - Result of the verification
    def verify_registers(self):
        result = True
        result &= self.verify_trans_conf()
        result &= self.verify_trans_ddi_func_ctl()
        result &= self.verify_pipe_misc()
        result &= self.verify_video_dip_ctl()
        result &= self.verify_plane_ctl_1()

        # TODO : Call Verify_clock after interface implementation for CNL
        # display_clock = DisplayClock()
        # result &= display_clock.verify_clock(self.test_parameters.display_port)

        logging.debug("****************************************************************************")
        if result is True:
            logging.info("Register Verification Passed")
        else:
            logging.error("Register Verification failed")
        logging.debug("****************************************************************************")
        return result

    ##
    # @brief        Get Enabled Pipe , Transcoder DDI suffix
    # @return       (bool,str) - (result,out_params) - Result of the verification
    def get_enabled_pipe_transcoder_ddi_suffix(self):
        '''
            Get pipe, transcoder, ddi suffix enabled for display
        '''
        logging.debug("****************************************************************************")
        trans_suffix_offsets = ['A', 'B', 'C']
        result = False
        ddi_suffix = None
        pipe_suffix = None
        trans_suffix = None

        display_port = self.test_parameters.display_port
        trans_conf_register = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % self.platform)
        trans_ddi_func_ctl_register = importlib.import_module(
            "registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (self.platform))

        if (display_port == "DP_A" or display_port == "EDP_A" or display_port == "MIPI_A" or display_port == "MIPI_B"):
            trans_suffix = "EDP"
            ddi_suffix = "A"
            if (display_port == "MIPI_A"):
                trans_suffix = "DSI0"
                ddi_suffix = "A"
            elif (display_port == "MIPI_B"):
                trans_suffix = "DSI1"
                ddi_suffix = "B"
            ##
            # TRANS_CONF
            trans_conf = 'TRANS_CONF' + '_' + trans_suffix
            trans_conf_obj = MMIORegister.read("TRANS_CONF_REGISTER", trans_conf, self.platform)
            transcoder_enable = trans_conf_obj.transcoder_enable  # (Bits Range 31:31)

            ##
            # TRANS_DDI_FUNC_CTL
            trans_ddi_func_ctl = 'TRANS_DDI_FUNC_CTL' + '_' + self.trans_suffix
            trans_ddi_func_ctl_obj = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl, self.platform)
            trans_ddi_function_enable = trans_ddi_func_ctl_obj.trans_ddi_function_enable  # (Bits Range 31:31)
            if (transcoder_enable == trans_conf_register.__getattribute__("transcoder_enable_ENABLE")
                    and trans_ddi_function_enable == trans_ddi_func_ctl_register.__getattribute__(
                        "trans_ddi_function_enable_ENABLE")):
                edp_input_select = trans_ddi_func_ctl_obj.edp_input_select  # (Bits Range 12:14)
                pipe_suffix = self.edp_input_select_map.get(edp_input_select)
                return True, pipe_suffix, trans_suffix, ddi_suffix

        else:

            for suffix in trans_suffix_offsets:
                ##
                # TRANS_CONF
                trans_conf = 'TRANS_CONF' + '_' + suffix
                trans_conf_obj = MMIORegister.read("TRANS_CONF_REGISTER", trans_conf, self.platform)
                transcoder_enable = trans_conf_obj.transcoder_enable  # (Bits Range 31:31)

                ##
                # TRANS_DDI_FUNC_CTL
                trans_ddi_func_ctl = 'TRANS_DDI_FUNC_CTL' + '_' + suffix
                trans_ddi_func_ctl_obj = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl,
                                                           self.platform)
                trans_ddi_function_enable = trans_ddi_func_ctl_obj.trans_ddi_function_enable  # (Bits Range 31:31)

                if (transcoder_enable == trans_conf_register.__getattribute__("transcoder_enable_ENABLE")
                        and trans_ddi_function_enable == trans_ddi_func_ctl_register.__getattribute__(
                            "trans_ddi_function_enable_ENABLE")):
                    ddi_select = trans_ddi_func_ctl_obj.ddi_select
                    if self.ddi_select_map.get(ddi_select) == '{portSuffix}'.format(
                            portSuffix=display_port[-1:].upper()):
                        ddi_suffix = self.ddi_select_map.get(ddi_select)
                        pipe_suffix = suffix
                        trans_suffix = suffix
                        result = True
                        break
        logging.debug("****************************************************************************")
        out_params = {"pipe_suffix": pipe_suffix, "trans_suffix": trans_suffix, "ddi_suffix": ddi_suffix}
        return result, out_params


if __name__ == "__main__":
    test_parameters = TestModeInfo(3840, 2160, 60, 1)
    test_parameters.display_port = "HDMI_B"
    edid_parameters = HdmiEDIDInfo()
    result, return_params = CnlVerifyRegisterProgramming(test_parameters,
                                                         edid_parameters).get_enabled_pipe_transcoder_ddi_suffix()
    print("Result : %s" % result)
    print("PIPE_SUFFIX : %s" % return_params.get("pipe_suffix"))
    print("TRANS_SUFFIX : %s" % return_params.get("trans_suffix"))
    print("DDI_SUFFIX : %s" % return_params.get("ddi_suffix"))
