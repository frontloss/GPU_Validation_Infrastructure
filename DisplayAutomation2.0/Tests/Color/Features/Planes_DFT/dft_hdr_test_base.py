############################################################################################
# \file         dft_hdr_test_base.py
# \section      dft_hdr_test_base
# \remarks      This script contains helper function that will be used in HDR test scripts.
# \ref          dft_hdr_test_base.py \n
# \author       Smitha B
###########################################################################################
import xml.etree.ElementTree as ET
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip, registry_access
from Libs.Core.logger import gdhm
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Tests.Color.Common.common_utility import apply_mode
from Tests.Color.Common import color_escapes, gamma_utility, common_utility, hdr_utility, color_enums, color_properties
from Tests.Color.Verification import feature_basic_verify
from Tests.Color.Verification import gen_verify_pipe, gen_verify_plane
from Tests.Planes.Common.planes_verification import check_layer_reordering
from Tests.test_base import *
from Tests.Planes.Common import planes_verification

BT2020_LINEAR = 2
PLANE_MAX = 3
XML_PATH = os.path.join(test_context.ROOT_FOLDER, "Tests\\Color\\Features\\Planes_DFT\\INPUT_XML")


class DFT_HDRBase(TestBase):
    native_mode, HzRes, VtRes, rr = None, None, None, None
    hdr_metadata = flip.HDR_INFO()
    pixel_format, color_space, blending_mode, panel_caps, flip_metadata, path = [], [], [], [], [], []
    output_range, panel_mode_dict = {}, {}
    mpo = flip.MPO()
    display_config = DisplayConfiguration()
    plane_count = 0
    layer_reordering = None
    ##
    # SB_PIXELFORMAT values for planar formats
    planar_formats = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

    def setUp(self):
        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        ##
        # DFT Tests are not supported in Multi-adapter scenarios, hence checking if there is only one adapter
        if self.context_args.adapters.__len__() > 1:
            logging.error("DFT Tests are not supported on multi-adapters!")
            gdhm.report_driver_bug_os("DFT Tests are not supported on multi-adapter system")
            self.fail()

        ##
        # Fetch the user input for scenario and the OS Brightness slider value
        self.xml_file = self.context_args.test.cmd_params.test_custom_tags["-INPUTFILEPATH"][0]

        ##
        # To parse the input xml and populate the attributes required for the test
        self.parse_xml(self.xml_file)

        ##
        # Perform all the setup required for Linear Mode Tests
        if self.blending_mode[0] == BT2020_LINEAR:
            if 'ExecutionEnv.PRE_SI_SIM' in str(self.context_args.test.exec_env):
                reg_read_status, reg_value = common_utility.read_registry(gfx_index="GFX_0", reg_name="ForceHDRMode")

                logging.info("ForceHDR Mode registry key was enabled.Need to disable it to configure Linear CSC")
                if common_utility.write_registry(gfx_index="GFX_0", reg_name="ForceHDRMode",
                                                 reg_datatype=registry_access.RegDataType.DWORD, reg_value=1,
                                                 driver_restart_required=True) is False:
                    logging.error("Registry key add to disable ForceHDRMode failed")
                    return reg_read_status
                logging.info("Registry key add to disable ForceHDRMode is successful and test proceeds to configure "
                             "Linear CSC")
            else:
                self.toggle_hdr_on_all_supported_panels(enable=True)
        else:
            logging.info("Blending Mode is not Linear - HDRModeset is not required")

        ##
        # Applying the Native Mode before starting the test
        for gfx_index, adapter in self.context_args.adapters.items():
            for panel_name, panel_attributes in adapter.panels.items():
                if panel_attributes.is_active:
                    if apply_mode(panel_attributes.display_and_adapterInfo) is False:
                        self.fail()
                    mode = common_utility.get_current_mode(panel_attributes.target_id)
                    self.panel_mode_dict[gfx_index, panel_name] = mode

        ##
        # Applying Unity Gamma LUT since from 19H1 onwards, OS applies a non-linear LUT on boot
        gamma_utility.apply_gamma()

        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief        To parse the input xml and populate the attributes required for the test
    # @param[in]    Input XML file name
    # @return       None
    def parse_xml(self, xml_file):
        xml_file = os.path.join(XML_PATH, xml_file)
        tree = ET.parse(xml_file)
        input = tree.getroot()

        plane = input.findall("./Plane")

        for element in plane:
            ##
            # Get the plane info from the XML file
            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, element.find("./SourcePixelFormat").text))
            self.color_space.append(getattr(flip.MPO_COLOR_SPACE_TYPE, element.find("./ColorSpace").text))
            self.path.append(os.path.join(test_context.SHARED_BINARY_FOLDER, element.find("./ImageFilePath").text))

        pipe = input.findall("./Pipe")

        for element in pipe:
            ##
            # Get the pipe info from the XML file
            self.blending_mode.append(getattr(color_enums.BlendingMode, element.find("./BlendingMode").text))
            for gfx_index, adapter in self.context_args.adapters.items():
                for panel_name, panel_attributes in adapter.panels.items():
                    if panel_name[:2] in 'DP':
                        self.output_range[gfx_index, panel_name] = color_enums.RgbQuantizationRange.FULL.value
                    else:
                        self.output_range[gfx_index, panel_name] = color_enums.RgbQuantizationRange.LIMITED.value
            self.panel_caps.append(getattr(color_enums.PanelCaps, element.find("./PanelCaps").text))

        ##
        # Fetching the Metadata only in case of Linear Tests
        hdr_metadata = input.findall("./HDRMetadata")
        for element in hdr_metadata:
            ##
            # Get the HDR Metadata info from the XML file
            eotf = int(element.find("./EOTF").text)
            primaries_x = list(map(int, element.find("./DisplayPrimariesX").text.split(",")))
            primaries_y = list(map(int, element.find("./DisplayPrimariesY").text.split(",")))
            whitepoint_x = int(element.find("./WhitePointX").text)
            whitepoint_y = int(element.find("./WhitePointY").text)
            maxlum = int(element.find("./MaxLuminance").text)
            minlum = int(element.find("./MinLuminance").text)
            max_cll = int(element.find("./MaxCLL").text)
            max_fall = int(element.find("./MaxFALL").text)

            self.hdr_metadata = flip.HDR_INFO(eotf, primaries_x, primaries_y, whitepoint_x, whitepoint_y, maxlum,
                                              minlum,
                                              max_cll,
                                              max_fall)
            ##
            # Translation of the HDR10 Luminance data in Reference Metadata
            # by converting to milli nits before comparing with the programmed
            self.flip_metadata = [eotf, primaries_x[0], primaries_y[0], primaries_x[1], primaries_y[1], primaries_x[2],
                                  primaries_y[2], whitepoint_x, whitepoint_y,
                                  int((maxlum / 1000)), (minlum * 10), int((max_cll / 1000)), int((max_fall / 1000))]

    ##
    # @brief Function to enable HDR on all the panels supporting HDR
    def toggle_hdr_on_all_supported_panels(self, enable: bool) -> bool:
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if color_escapes.configure_hdr(port, panel.display_and_adapterInfo,
                                                   enable=enable) is False:
                        return False
                    ##
                    # For simplicity, DFT tests do not exercise the Brightness Sliders and any pixel boost verification
                    # Hence, sporadically, we can see a mismatch between the Programmed and the Reference Gamma LUTs
                    # This happens as the Base LUT will not be multiplied with Pixel Boost while constructing the Reference LUT
                    # Here, reference LUT is directly taken as the static OETF_2084_10KNits_513Samples_8_24_FORMAT
                    # Hence, to overcome the sporadic issue, setting the Brightness Slider to a particular level to match this LUT.
                    # The Brightness Slider and the OS B3 value in Nits are not Linear, hence after multiple experiments,
                    # it has been figured out that at Brightness level 47, the LUTs are comparable
                    if panel.is_lfp:
                        if enable is False:
                            color_properties.set_b3_slider(str(100))
                        else:
                            color_properties.set_b3_slider(str(47))

                    if feature_basic_verify.verify_hdr_feature(gfx_index, adapter.platform, panel.pipe,
                                                               enable=enable) is False:
                        return False
        return True

    ##
    # @brief        To invoke the utility to convert NG input file to raw dump given the buffer parameters
    # @param[in]    PNG input file name
    # @param[in]    Output HRes of buffer
    # @param[in]    Output VRes of buffer
    # @param[in]    Source Pixel format
    # @param[in]    Layer index of the plane
    # @param[in]    Display index
    # @return       Output file name
    def convert_png_to_bin(self, input_file, width, height, pixel_format, layer_index, display_name):
        str1 = '_' + str(layer_index) + str(display_name) + '.bin'
        output_file = input_file.replace('.png', str1)
        if os.path.exists(output_file):
            os.remove(output_file)
        executable = 'ImageFormater.exe'
        commandline = executable + ' -i ' + input_file + ' -w ' + str(width) + ' -h ' + str(height) + ' -f ' + str(
            pixel_format) + ' -o ' + output_file
        logging.debug("ImageFormatter commandline : %s", commandline)
        currentdir = os.getcwd()
        os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
        logging.debug("Current path : %s", os.getcwd())
        os.system(commandline)
        os.chdir(currentdir)
        return output_file

    ##
    # @brief        Get the no of planes created for given source id
    # @param[in]	source_id Source id of the plane
    # @param[in]	planes Pointer to structure @ref _PLANE containing the plane info
    # @return       Plane count per source id
    def get_plane_count_for_source_id(self, source_id, planes):
        plane_count = 0
        for index in range(0, planes.uiPlaneCount):
            if source_id == planes.stPlaneInfo[index].iPathIndex:
                plane_count = plane_count + 1
        return plane_count

    ##
    # @brief        Perform Plane Verification
    # @param[in]	source_id Source id of the plane
    # @param[in]	planes Pointer to structure @ref _PLANE containing the plane info
    # @return       Plane count per source id
    def plane_verification(self, gfx_index, platform, panel, plane, pixel_format, color_space_enum):
        logging.info("")
        logging.info(
            "Performing Plane Verification on Adapter {0} on Plane {1} Pipe {2}".format(gfx_index, plane, panel.pipe))

        self.color_space, self.gamut, self.gamma, self.range = hdr_utility.decode_color_space_enum_value(
            color_space_enum)
        plane_verifier = gen_verify_plane.get_plane_verifier_instance(self.context_args.adapters[gfx_index].platform,
                                                                      gfx_index)
        is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, panel.pipe)
        plane_args = hdr_utility.PlaneArgs(self.color_space, pixel_format, self.gamma, self.gamut, self.range)
        plane_ctl_info = plane_verifier.regs.get_plane_ctl_info(plane, panel.pipe)
        pixel_format = plane_ctl_info.SourcePixelFormat
        ##
        # Performing FP16 Normalizer Verification
        pixel_normalizer_info = plane_verifier.regs.get_plane_pixel_normalizer_info(plane, panel.pipe)
        logging.info(
            "Performing FP16Normalization Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                 panel.pipe))
        status, fp16_normalizer_enable = hdr_utility.verify_fp16_normalizer_enable_status(pixel_format, gfx_index,
                                                                                          panel.pipe, plane,
                                                                                          pixel_normalizer_info,
                                                                                          is_hdr_enabled)
        if status is False:
            return False
        if fp16_normalizer_enable:
            if plane_verifier.verify_fp16_normalizer_programming(panel.pipe, pixel_normalizer_info) is False:
                return False
        ##
        # Performing InputCSC Verification
        logging.info("Performing InputCSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                 panel.pipe))
        plane_color_ctl_info = plane_verifier.regs.get_plane_color_ctl_info(plane, panel.pipe)
        status, verify_icsc_matrix = hdr_utility.verify_input_csc_enable_status(pixel_format, self.range, gfx_index,
                                                                                panel.pipe,
                                                                                plane, plane_color_ctl_info)
        if status is False:
            return False
        if verify_icsc_matrix:
            if plane_verifier.verify_input_csc_programming(plane_args, pixel_format, panel.pipe, plane) is False:
                return False
        ##
        # If content range is limited and color space is YCbCr, then use HW for range correction
        if self.range == "STUDIO" and self.color_space == "YCBCR":
            if plane_color_ctl_info.YuvRangeCorrectionDisable == 1:
                logging.error("For Limited range and YCBCR color space content : "
                              "expected yuv_range_correction_output = 0, actual yuv_range_correction_output = 1 ")
                gdhm.report_driver_bug_os("[{0}] Limited range and YCBCR color space content Adapter: {1} "
                                          "Expected yuv_range_correction_output = 0, Actual yuv_range_correction_output = {2}"
                                          .format(platform, gfx_index, plane_color_ctl_info.YuvRangeCorrectionDisable))
                return False
            if plane_color_ctl_info.YuvRangeCorrectionOutput != 0:
                logging.error("for limited range and YCBCR Colorspace content:"
                              "expected yuv_range_correction_output = 0, actual yuv_range_correction_output = 1")
                gdhm.report_driver_bug_os("[{0}] Limited range and YCBCR Colorspace content Adapter: {1} "
                                          "Expected yuv_range_correction_output = 0, Actual yuv_range_correction_output = {2}"
                                          .format(platform, gfx_index, plane_color_ctl_info.YuvRangeCorrectionOutput))
                return False
            if plane_color_ctl_info.RemoveYuvOffset != 0:
                logging.error("FAIL : For limited range and YCBCR Colorspace content:"
                              " expected remove_yuv_offset = 0, actual remove_yuv_offset = 1")
                gdhm.report_driver_bug_os("[{0}] Limited range and YCBCR Colorspace content Adapter: {1} "
                                          " Expected remove_yuv_offset = 0, Actual remove_yuv_offset = {2}"
                                          .format(platform, gfx_index, plane_color_ctl_info.RemoveYuvOffset))
                return False

        logging.info("")
        logging.info(
            "Performing Plane PreCSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                            panel.pipe))
        if is_hdr_enabled and self.gamma != "G10":
            if plane_color_ctl_info.PlanePreCscGammaEnable is False:
                logging.error(
                    "FAIL: Plane PreCSC Gamma not enabled when Gamut {0} and HDR Mode on Adapter {1} Plane {2} Pipe {3}. Expected = ENABLE, Actual = DISABLE"
                        .format(self.gamut, gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane PreCSC Gamma not enabled when Gamut {1} and HDR Mode on Adapter {2} Plane {3} Pipe {4} Expected = ENABLE, Actual = DISABLE"
                        .format(platform, self.gamut, gfx_index, plane, panel.pipe))
                return False
        elif self.gamut == "P2020" and is_hdr_enabled is False:
            if plane_color_ctl_info.PlanePreCscGammaEnable is False:
                logging.error(
                    "FAIL: Plane PreCSC Gamma not enabled with Gamut {0} and SDR Mode on Adapter {1} Plane {2} Pipe {3}. Expected = ENABLE, Actual = DISABLE"
                        .format(self.gamut, gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane PreCSC Gamma not enabled with Gamut {1} and SDR Mode on Adapter {2} Plane {3} Pipe {4} Expected = ENABLE, Actual = DISABLE"
                        .format(platform, self.gamut, gfx_index, plane, panel.pipe))
                return False
        elif self.gamut == "P709" and is_hdr_enabled:
            if plane_color_ctl_info.PlanePreCscGammaEnable is False:
                logging.error(
                    "FAIL: Plane PreCSC Gamma not enabled with Gamut {0} and HDR Mode on Adapter {1} Plane {2} Pipe {3}. Expected = ENABLE, Actual = DISABLE"
                        .format(self.gamut, gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane PreCSC Gamma not enabledwith Gamut {1} and HDR Mode on Adapter {2} Plane {3} Pipe {4} Expected = ENABLE, Actual = DISABLE"
                        .format(platform, self.gamut, gfx_index, plane, panel.pipe))
                return False
        else:
            if self.gamut == "P709" and (is_hdr_enabled is False):
                if plane_color_ctl_info.PlanePreCscGammaEnable:
                    logging.info(
                        "Pass: Plane PreCSC Gamma is enabled with Gamut {0} on Adapter {1} Plane {2} Pipe {3}. Expected = DISABLE, Actual = ENABLE".format(self.gamut, gfx_index, plane, panel.pipe))
        if plane_color_ctl_info.PlanePreCscGammaEnable:
            if plane_verifier.verify_plane_degamma_programming(plane_args, plane, panel.pipe) is False:
                return False

        ##
        # Performing Plane CSC Verification
        logging.info("Performing Plane CSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                  panel.pipe))
        if is_hdr_enabled and self.gamut != "P2020":
            if plane_color_ctl_info.PlaneCscEnable is False:
                logging.error(
                    "FAIL: Plane CSC not enabled for 709->2020 conversion on Adapter {0} Plane {1} Pipe {2}. Expected "
                    "= ENABLE Actual = DISABLE "
                        .format(gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane CSC not enabled for 709->2020 conversion on Adapter {1} Plane {2} Pipe {3} Expected "
                    "= ENABLE Actual = DISABLE "
                        .format(platform, gfx_index, plane, panel.pipe))
                return False

        elif is_hdr_enabled is False and self.gamut != "P709":
            if plane_color_ctl_info.PlaneCscEnable is False:
                logging.error(
                    "FAIL: Plane CSC not enabled for 2020->709 conversion. Expected = ENABLE Actual = DISABLE on Adapter {0} Plane {1} Pipe {2}"
                        .format(gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane CSC not enabled for 2020->709 conversion. Expected = ENABLE Actual = DISABLE on Adapter {1} Plane {2} Pipe {3}"
                        .format(platform, gfx_index, plane, panel.pipe))
                return False
        else:
            if plane_color_ctl_info.PlaneCscEnable:
                logging.error(
                    "FAIL: Plane CSC Expected = DISABLE Actual = ENABLE on Adapter {0} Plane {1} Pipe {2}"
                        .format(gfx_index, plane, panel.pipe))
                gdhm.report_driver_bug_os(
                    "[{0}] Plane CSC Expected = DISABLE Actual = ENABLE on Adapter {1} Plane {2} Pipe {3}"
                        .format(platform, gfx_index, plane, panel.pipe))
                return False
            else:
                logging.info(
                    "PASS: Plane CSC Expected = DISABLE Actual = DISABLE on Adapter {0} Plane {1} Pipe {2}"
                        .format(self.gamut, gfx_index, plane, panel.pipe))

        if plane_color_ctl_info.PlaneCscEnable:
            logging.info(
                "PASS: Plane CSC Expected = ENABLE Actual = ENABLE on Adapter {0} Plane {1} Pipe {2}"
                    .format(self.gamut, gfx_index, plane, panel.pipe))
            if plane_verifier.verify_plane_csc_programming(plane_args, pixel_format, plane, panel.pipe) is False:
                return False

        ##
        # Performing Plane PostCSC Gamma Verification
        logging.info(
            "Performing Plane PostCSC Gamma Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                   panel.pipe))
        if plane_color_ctl_info.PlaneGammaDisable == 0:
            logging.info(
                "PASS: Plane PostCSC Gamma enabled on Adapter {0} Plane {1} on Pipe {2}. Expected = ENABLE, Actual = ENABLE"
                    .format(gfx_index, plane, panel.pipe))
        else:
            logging.info("Skipped verifying Plane Gamma as it is not enabled")
        logging.info("PASS : Plane Verification is Successful on Adapter {0}  Pipe {1}".format(gfx_index, panel.pipe))
        return True

    ##
    # Pipe Verification includes :
    # Pipe Pre CSC     - To be disabled in case of HDR; Enabled in case of SDR and perform LUT verification
    # Pipe CSC         - To be enabled and perform Matrix verification with reference matrix from ETL
    # Pipe Post CSC    - To be enabled; LUT verification including Pixel Boost Verification for eDP HDR
    # Pipe OutputCSC   - To be enabled if Pipe is in YUV or if OutputRange was in Limited in case of RGB;
    #                    Perform Matrix verification
    # HDR Verification - DPCD Verification - In Case of eDP HDR (SDP/Aux Based);
    def pipe_verification(self, gfx_index, platform, port, panel, panel_caps, output_range):
        logging.info("")
        logging.info(
            "Performing Pipe Verification for Panel {0} on Adapter {1} attached to Pipe {2}".format(port, gfx_index,
                                                                                                    panel.pipe))
        pipe_args = hdr_utility.DFTPipeArgs()
        is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, panel.pipe)
        feature = "HDR" if is_hdr_enabled is True else "SDR"
        cc_block = common_utility.get_color_conversion_block(platform, panel.pipe, feature)

        pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
        color_ctl_offsets = pipe_verifier.regs.get_color_ctrl_offsets(panel.pipe)
        ##
        # Performing Pipe Degamma Verification
        logging.info(
            "Performing Pipe Degamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                               panel.pipe))
        # ##
        # # Verification if the PreCSC block has been enabled in case of SDR and otherwise for HDR
        gamma_mode = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.GammaMode)
        gamma_mode_value = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            GammaMode=gamma_mode))

        status, verify_pipe_pre_csc_lut = hdr_utility.verify_pipe_pre_csc_gamma_enable_status(gfx_index, panel.pipe,
                                                                                              gamma_mode_value,
                                                                                              cc_block, feature)
        if status is False:
            return False
        if verify_pipe_pre_csc_lut:
            if pipe_verifier.verify_pipe_degamma_programming(pipe_args, panel.pipe, cc_block) is False:
                return False

        ##
        # Performing Pipe CSC Verification
        logging.info("")
        logging.info("Performing Pipe CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                    panel.pipe))
        ##
        # Verification if the CSC block has been enabled
        csc_mode_val = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_values = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            CscMode=csc_mode_val))
        if color_ctl_values.PipeCscEnable:
            pipe_args.panel_caps = panel_caps
            logging.info(
                "PASS : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                panel.pipe,
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(0)],
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(
                                                                                                        color_ctl_values.PipeCscEnable)]))
            if pipe_verifier.verify_pipe_csc_programming(pipe_args, panel.pipe) is False:
                # @todo : Debug the issue separately
                return False
        else:
            if is_hdr_enabled:
                if panel_caps not in (color_enums.PanelCaps.SDR_BT2020_RGB, color_enums.PanelCaps.SDR_BT2020_YUV420,
                                      color_enums.PanelCaps.HDR_BT2020_RGB,
                                      color_enums.PanelCaps.HDR_BT2020_YUV420):
                    logging.error(
                        "FAIL : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                        panel.pipe,
                                                                                                        feature_basic_verify.BIT_MAP_DICT[
                                                                                                            int(0)],
                                                                                                        feature_basic_verify.BIT_MAP_DICT[
                                                                                                            int(
                                                                                                                color_ctl_values.PipeCscEnable)]))
                    gdhm.report_driver_bug_os(
                        "Pipe CSC on failed for Pipe : {0}  Adapter : {1} Expected {2} : Actual {3}"
                            .format(panel.pipe, gfx_index, feature_basic_verify.BIT_MAP_DICT[int(0)],
                                    feature_basic_verify.BIT_MAP_DICT[int(color_ctl_values.PipeCscEnable)]))
                    return False
            else:
                if panel_caps in (color_enums.PanelCaps.SDR_BT2020_RGB, color_enums.PanelCaps.SDR_BT2020_YUV420,
                                  color_enums.PanelCaps.HDR_BT2020_RGB,
                                  color_enums.PanelCaps.HDR_BT2020_YUV420):
                    logging.error(
                        "FAIL : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                        panel.pipe,
                                                                                                        feature_basic_verify.BIT_MAP_DICT[
                                                                                                            int(0)],
                                                                                                        feature_basic_verify.BIT_MAP_DICT[
                                                                                                            int(
                                                                                                                color_ctl_values.PipeCscEnable)]))
                    gdhm.report_driver_bug_os("Pipe CSC on Pipe : {0}  Adapter : {1} Expected {2} : Actual {3}"
                                              .format(panel.pipe, gfx_index, feature_basic_verify.BIT_MAP_DICT[int(0)],
                                                      feature_basic_verify.BIT_MAP_DICT[
                                                          int(color_ctl_values.PipeCscEnable)]))
                    return False

        ##
        # Performing Pipe Gamma Verification
        logging.info("")
        logging.info("Performing Pipe Gamma Verification")
        logging.info("")
        logging.info(
            "Performing Pipe Gamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                             panel.pipe))

        status, verify_pipe_post_csc_gamma_lut = hdr_utility.verify_pipe_post_csc_gamma_status(gfx_index, panel.pipe,
                                                                                               gamma_mode_value,
                                                                                               cc_block)
        if status is False:
            return False
        if verify_pipe_post_csc_gamma_lut:
            if 'ExecutionEnv.POST_SI' in str(self.context_args.test.exec_env):
                # As part of Pre-si Brightness api was not functioning, so restricting only to Post-si
                if pipe_verifier.verify_pipe_gamma_programming(pipe_args, panel.pipe, cc_block) is False:
                    return False

        ##
        # Performing Pipe oCSC Verification
        logging.info(" ")
        logging.debug(
            "Performing Pipe Output CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                  panel.pipe))
        csc_mode_data = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_value = pipe_verifier.regs.get_colorctl_info(panel.pipe,
                                                               ColorCtlOffsetsValues(CscMode=csc_mode_data))
        status, pipe_output_csc_enabled, input, output, conv_type = hdr_utility.verify_pipe_output_status(gfx_index,
                                                                                                          panel.pipe,
                                                                                                          color_ctl_value,
                                                                                                          gamma_mode_value,
                                                                                                          output_range)
        if status is False:
            return False
        if pipe_output_csc_enabled:
            if pipe_verifier.verify_output_csc_programming(panel.pipe, 8, input, output, conv_type) is False:
                return False
        if is_hdr_enabled:
            pipe_args.reference_metadata = self.flip_metadata
            logging.info("Reference Metadata {0}".format(self.flip_metadata))
            if hdr_utility.hdr_verification(pipe_args, gfx_index, platform, port, panel) is False:
                return False
        logging.info(
            "PASS : Pipe Verification is successful for Panel {0} attached to Pipe {1} on Adapter {2}".format(
                port, panel.pipe, gfx_index))
        return True

    ##
    # @brief            Verification of plane programming
    # @param[in]	    plane_count; No of planes currently enabled
    # @param[in]	    layerindex; layerIndex
    # @param[in]	    gfx_index; gfx_index
    # @return		    plane_id; plane_id for the corresponding layer index
    def get_plane_id_from_layerindex(self, plane_count, layerindex, gfx_index):
        if not check_layer_reordering(gfx_index):
            plane_id = PLANE_MAX - layerindex
        else:
            plane_id = plane_count - layerindex

        return plane_id

    def tearDown(self):
        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)
        for gfx_index, adapter in self.context_args.adapters.items():
            for panel_name, panel_attributes in adapter.panels.items():
                if 'ExecutionEnv.PRE_SI_SIM' in str(self.context_args.test.exec_env):
                    reg_read_status, reg_value = common_utility.read_registry(gfx_index="GFX_0", reg_name="ForceHDRMode")
                    logging.info(
                        "ForceHDR Mode registry key was enabled.Need to disable it to configure Linear CSC")
                    if common_utility.write_registry(gfx_index="GFX_0", reg_name="ForceHDRMode",
                                                     reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                                     driver_restart_required=True) is False:
                        logging.error("Registry key add to disable ForceHDRMode failed")
                        return reg_read_status
                    logging.info(
                        "Registry key add to disable ForceHDRMode is successful and test proceeds to configure "
                        "Linear CSC")
                else:
                    if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel_attributes.pipe):
                        if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
                            self.fail()
                    else:
                        logging.debug("{0} is Non-HDR Panel; No specific clean-up required".format(panel_name))
        ##
        # Apply Unity Gamma as part of clean-up
        gamma_utility.apply_gamma()
        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        super().tearDown()

        logging.info('********************* TEST  ENDS HERE **************************')
