#################################################################################################
# @file         hdr_test_base.py
# @brief        This script is a Feature Base class specific to HDR.
#               The hdr_test_base performs the below functionalities
#               to setup all the infra needed by the test scripts.
#               1.setUp() -  Invokes Common class's setUp() to perform basic functionalities
#                            Updates the display caps in the Context by parsing the ETLs.
#                            Test scripts expect at least one HDR supported panel to be passed
#                            Checks for the PowerMode and switches to AC mode if required to adhere to OS Policy
#               2.enable_hdr_on_all_supported_panels_and_verify() - Enables HDR on all the supported panels
#                                                                   and performs basic verification
#               3.initialize_panel_color_properties() - Initializes all the Color related properties of a panel
#               4.tearDown() - Disables HDR enabled on all HDR supported panels.
#                              In case of an eDP HDR panel, sets the OS Brightness slider to 100.
#                              Applies Unity Gamma and invokes the Common Base Class's tearDown()
# @author       Smitha
#################################################################################################
import logging
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import registry_access, display_essential
from Libs.Core import etl_parser, enum
from Libs.Core import etl_parser, enum,window_helper
from Libs.Core import display_power
from Tests.test_base import *
from Tests.Color.Common import color_properties, color_escapes, color_constants, color_enums
from Tests.Color.Common import color_etl_utility, hdr_utility, gamma_utility, common_utility, csc_utility
from Tests.Color.Verification import feature_basic_verify
from Tests.Color.Verification import gen_verify_pipe, gen_verify_plane
from Tests.Color import color_common_utility
from Libs.Core.machine_info.machine_info import SystemInfo

class HDRTestBase(TestBase):
    scenario = None
    b3_val = None
    enable_wcg = False
    enable_regkey_dithering = False
    pipe_args = hdr_utility.E2EPipeArgs()
    init_file_path = None
    bpc = 8
    ##
    # A dictionary of all the properties related to the displays passed from command line
    # This dictionary have a tuple of gfx_index and connector_port_type as key
    # and the value contains all the display related properties enclosed in a list
    panel_props_dict = {}
    hdr_metadata_gdhm = {}
    lace1p0_reg_value = None
    lace1p0_status = None

    def setUp(self):
        self.custom_tags["-B3_SLIDER"] = 0
        self.custom_tags["-SMOOTH_BRIGHTNESS"] = False
        self.custom_tags["-SCENARIO"] = 'AC_DC'
        self.custom_tags['-ENABLE_WCG'] = False
        self.custom_tags['-ENABLE_REGKEY_DITHERING'] = False
        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        ##
        # Fetch the user input for scenario and the OS Brightness slider value
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.b3_val = self.context_args.test.cmd_params.test_custom_tags["-B3_SLIDER"]
        if self.b3_val == 'NONE' or self.b3_val is None:
            logging.debug("Brightness Slider Level is not specified by the Command Line")
        else:
            self.b3_val = self.b3_val[0]
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_WCG"][0]) > 1:
            self.enable_wcg = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_WCG"][0])
        else:
            self.enable_wcg = False
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0]) > 1:
            self.enable_regkey_dithering = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0])
        else:
            self.enable_regkey_dithering = False
        ##
        # Iterate through the connected panels and identify if the panel is HDR Capable
        # and update the context about the details of the HDR Supported panel
        # At least one of the panels connected should be HDR supported, otherwise test will fail due to config issues
        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)

        ##
        # Check if there is at least one HDR Supported Panel requested as part of the command line
        if num_of_hdr_supported_panels == 0:
            logging.info("Enable WCG Status is {0}".format(self.enable_wcg))
            if self.enable_wcg is False:
                logging.error("FAIL : At least one HDR supported panel is required")
                self.fail()

        ##
        # If WCG is requested to be enabled, there should be at least one internal SDR panel to be connected
        wcg_lfp = 0
        if self.enable_wcg:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.FeatureCaps.HDRSupport is False:
                        panel.FeatureCaps.WCGSupport = True
                        wcg_lfp += 1

            if wcg_lfp == 0:
                logging.error("FAIL : At least one WCG supported panel is required")
                self.fail()

        # Enable Lace1.0 coverage for ARL, MTL
        self.lace1p0_status, self.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")
        if SystemInfo().get_sku_name('gfx_0') == 'ARL':
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        if self.enable_regkey_dithering:
            for gfx_index, adapter in self.context_args.adapters.items():
                reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

                key_name = "ForceDitheringEnable"
                value = 1
                if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=value) is False:
                    self.fail("Registry key add to enable SelectBPC  failed")
                logging.info(" ForceDitheringEnable set to 1 on GFX_{0}".format(gfx_index))
                ##
                # restart display driver for regkey to take effect.
                status, reboot_required = common_utility.restart_display_driver(gfx_index)
                if status is False:
                    self.fail('Fail: Failed to Restart Display driver')
        ##
        # Verify if the Power Mode is in DC and switch to AC
        # This is to override the OS Policy to disable HDR
        # when running Windows HD Color content on battery Power for battery optimization
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()

    ##
    # Initialize all the generic Color Properties related to a panel first time after enabling HDR by parsing ETL
    # Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
    # Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
    def initialize_common_color_props(self):

        ##
        # Initialize all the Color Properties related to eDP HDR panels
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.HDRSupport:
                    logging.info("")
                    logging.info(
                        "Initializing eDP  color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}".format(
                            port, gfx_index, panel.pipe))
                    edp_hdr_props = self.panel_props_dict[gfx_index, port]
                    if color_properties.initialize_edp_hdr_props(panel.target_id, edp_hdr_props) is False:
                        self.fail()
                    self.panel_props_dict[gfx_index, port] = edp_hdr_props

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                panel_props = self.panel_props_dict[gfx_index, port]
                if panel.is_active:
                    logging.info("")
                    logging.info(
                        "Initializing all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}".format(
                            port, gfx_index, panel.pipe))
                    if color_properties.initialize_panel_color_properties(panel.target_id, panel.pipe, gfx_index,
                                                                          panel_props) is False:
                        self.fail()
                    self.panel_props_dict[gfx_index, port] = panel_props

    ##
    # @brief Enable HDR on all the supported panels
    #        Initialize all the color properties of the panel by parsing the ETLs
    #        Perform Plane and Pipe Verification
    def enable_hdr_and_verify(self) -> bool:
        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            return False

        ##
        # Apply Unity Gamma at the beginning of the test after enabling HDR
        color_common_utility.apply_unity_gamma()
        time.sleep(5)

        ##
        # Initialize all the Color properties for all the panels
        self.initialize_common_color_props()

        ##
        # Perform Plane and Pipe Verification after Enabling HDR
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                    return False
                if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                    self.fail()

        return True


    ##
    # Update all the generic Color Properties related to a panel after performing an event
    # Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
    # Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
    def update_common_color_props(self, after_event, target_id, current_pipe, is_lfp, gfx_index, panel_props, wcg_support_status):
        if after_event is not None:
            init_etl = "After_Performing_" + after_event + "_" + "TimeStamp_"
            init_etl_path = color_etl_utility.stop_etl_capture(init_etl)
            time.sleep(5)
            if etl_parser.generate_report(init_etl_path) is False:
                logging.error("\tFailed to generate EtlParser report")
                return False
            else:
                ##
                # Start the ETL again for capturing other events
                if color_etl_utility.start_etl_capture() is False:
                    logging.error("Failed to Start Gfx Tracer")
                    return False

        if is_lfp:
            if color_properties.initialize_edp_hdr_props(target_id, panel_props, wcg_support_status) is False:
                self.fail()
        else:
            if color_properties.initialize_panel_color_properties(target_id, current_pipe, gfx_index,
                                                                  panel_props) is False:
                self.fail()

    ##
    # Update all the generic Color Properties related to a panel after performing an event
    # Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
    # Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
    def update_common_color_props_for_all(self, after_event):
        if after_event is not None:
            init_etl = "After_Performing_" + after_event + "_" + "TimeStamp_"
            init_etl_path = color_etl_utility.stop_etl_capture(init_etl)

            if etl_parser.generate_report(init_etl_path) is False:
                logging.error("\tFailed to generate EtlParser report")
                return False
            else:
                ##
                # Start the ETL again for capturing other events
                if color_etl_utility.start_etl_capture() is False:
                    logging.error("Failed to Start Gfx Tracer")
                    return False

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                panel_props = self.panel_props_dict[gfx_index, port]
                if panel.FeatureCaps.HDRSupport is False:
                    panel.FeatureCaps.WCGSupport = True
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.HDRSupport:
                    if color_properties.initialize_edp_hdr_props(panel.target_id, panel_props, panel.FeatureCaps.WCGSupport) is False:
                        self.fail()
                if panel.is_active:
                    if color_properties.initialize_panel_color_properties(panel.target_id, panel.pipe, gfx_index,
                                                                          panel_props) is False:
                        self.fail()


    ##
    # @brief        Enables or Disables HDR
    # @param[in]    port_name  ConnectorNPortType of the display
    # @param[in]    display_and_adapter_info- DisplayAndAdapterInfo Struct of the display
    # @param[in]    enable - Boolean value to either enable or disable
    # @return       status - True on Success, False otherwise
    def fetch_enabled_feature(self, gfx_index, platform, panel):
        feature = "SDR"
        if feature_basic_verify.hdr_status(gfx_index, platform, panel.pipe):
            feature = "HDR"
        else:
            if self.enable_wcg:
                panel.FeatureCaps.WCGSupport = True
                feature = "WCG"
        return feature

    ##
    # Pipe Verification includes :
    # Pipe Pre CSC     - To be disabled in case of HDR; Enabled in case of SDR and perform LUT verification
    # Pipe CSC         - To be enabled and perform Matrix verification with reference matrix from ETL
    # Pipe Post CSC    - To be enabled; LUT verification including Pixel Boost Verification for eDP HDR
    # Pipe OutputCSC   - To be enabled if Pipe is in YUV or if OutputRange was in Limited in case of RGB;
    #                    Perform Matrix verification
    # HDR Verification - DPCD Verification - In Case of eDP HDR (SDP/Aux Based);
    def pipe_verification(self, gfx_index, platform, port, panel, is_smooth_brightness=False, step_index=0):

        logging.info("")
        feature = self.fetch_enabled_feature(gfx_index, platform, panel)
        logging.info(
            "Performing Pipe Verification for Panel {0} on Adapter {1} attached to Pipe {2} for feature {3}".format(
                port, gfx_index,
                panel.pipe, feature))

        # # @todo : pass only the feature details - to be updated in several tests
        is_hdr_enabled = True if feature == "HDR" else False
        cc_block = common_utility.get_color_conversion_block(platform, panel.pipe, feature)
        pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
        color_ctl_offsets = pipe_verifier.regs.get_color_ctrl_offsets(panel.pipe)
        ##
        # Performing Pipe Degamma Verification
        logging.info("")
        logging.info("Performing Pipe Degamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                        panel.pipe))
        ##
        # Verification if the PreCSC block has been enabled in case of SDR and otherwise for HDR
        gamma_mode = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.GammaMode)
        gamma_mode_value = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            GammaMode=gamma_mode))
        status, verify_pipe_pre_csc_lut = hdr_utility.verify_pipe_pre_csc_gamma_enable_status(gfx_index, panel.pipe,
                                                                                              gamma_mode_value,
                                                                                              cc_block, feature)
        if status is False:
            return False
        if verify_pipe_pre_csc_lut:
            if pipe_verifier.verify_pipe_degamma_programming(self.pipe_args, panel.pipe, cc_block) is False:
                return False

        ##
        # Performing Pipe CSC Verification
        logging.info("")
        logging.info(
            "Performing Pipe CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index, panel.pipe))
        ##
        # Verification if the CSC block has been enabled
        self.pipe_args.os_relative_csc = self.panel_props_dict[gfx_index, port].os_relative_csc
        csc_mode_val = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_values = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            CscMode=csc_mode_val))
        status, verify_pipe_csc_matrix = hdr_utility.verify_pipe_csc_enable_status(gfx_index, panel.pipe,
                                                                                   self.panel_props_dict[
                                                                                       gfx_index, port].oned_lut_param_type,
                                                                                   self.panel_props_dict[
                                                                                       gfx_index, port].gamma_ramp_type, cc_block,
                                                                                   color_ctl_values)
        if status is False:
            return False
        if verify_pipe_csc_matrix:
            reg_name = "PipeCscCoeff" if cc_block == "CC1" else "PipeCscCc2Coeff"
            if pipe_verifier.verify_pipe_csc_programming(self.pipe_args, panel.pipe, reg_name, feature=feature) is False:
                return False

        if self.enable_regkey_dithering:
            if feature_basic_verify.verify_dithering_feature(gfx_index, platform, panel.pipe, panel.transcoder,
                                                             True) is False:
                self.fail()

        ##
        # Performing Pipe Gamma Verification
        if is_hdr_enabled:
            self.pipe_args.is_smooth_brightness = is_smooth_brightness
            self.pipe_args.step_index = step_index
            self.pipe_args.pixel_boost = self.panel_props_dict[gfx_index, port].pixel_boost
            self.pipe_args.desired_max_cll = panel.HDRDisplayCaps.desired_max_cll
            self.pipe_args.desired_max_fall = panel.HDRDisplayCaps.desired_max_fall
            self.pipe_args.default_metadata = self.panel_props_dict[gfx_index, port].default_metadata
            self.pipe_args.flip_metadata = self.panel_props_dict[gfx_index, port].flip_metadata
        self.pipe_args.bpc = self.panel_props_dict[gfx_index, port].bpc
        self.pipe_args.os_relative_lut = self.panel_props_dict[gfx_index, port].os_relative_lut
        self.pipe_args.dsb_gamma_dump = self.panel_props_dict[gfx_index, port].dsb_gamma_dump
        logging.info("")
        logging.info("Performing Pipe Gamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                      panel.pipe))
        status, verify_pipe_post_csc_gamma_lut = hdr_utility.verify_pipe_post_csc_gamma_status(gfx_index, panel.pipe,
                                                                                               gamma_mode_value,
                                                                                               cc_block)
        if status is False:
            return False
        if verify_pipe_post_csc_gamma_lut:
            if pipe_verifier.verify_pipe_gamma_programming(self.pipe_args, panel.pipe, cc_block) is False:
                return False

        ##
        # Performing Pipe oCSC Verification
        logging.info("")
        logging.debug(
            "Performing Pipe Output CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                  panel.pipe))
        csc_mode_data = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_value = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(CscMode=csc_mode_data))
        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
        output_range = csc_utility.get_output_range(gfx_index, platform, plane_id,
                                                    panel.pipe, panel.transcoder, pipe_verifier.mmio_interface)

        status, pipe_output_csc_enabled, input, output, conv_type = hdr_utility.verify_pipe_output_status(gfx_index,
                                                                                                          panel.pipe,
                                                                                                          color_ctl_value,
                                                                                                          gamma_mode_value,
                                                                                                          output_range)
        if status is False:
            return False

        if pipe_output_csc_enabled:
            if pipe_verifier.verify_output_csc_programming(panel.pipe, self.pipe_args.bpc, input, output, conv_type) is False:
                return False
        if is_hdr_enabled:
            if hdr_utility.hdr_verification(self.pipe_args, gfx_index, platform, port, panel,
                                            self.pipe_args.bpc) is False:
                return False
        logging.info(
            "PASS : Pipe Verification is successful for Panel {0} attached to Pipe {1} on Adapter {2}".format(
                port, panel.pipe, gfx_index))
        return True


    ##
    # Plane Verification includes :
    # FP16 Normalization     - To be enabled for planes with FP16 PixelFormat and verify normalization factor;
    #                          disabled otherwise
    # Plane Input CSC        - To be enabled for planes with YUV PixelFormat
    # Plane Pre CSC Gamma    - To be enabled; LUT verification including Pixel Boost Verification for eDP HDR
    # Plane CSC              - To be enabled if Pipe is in YUV or if OutputRange was in Limited in case of RGB;
    # Plane Post CSC Gamma   - Perform Matrix verification
    def plane_verification(self, gfx_index, platform, panel, plane, port):
        self.pipe_args = hdr_utility.E2EPipeArgs()

        plane_verifier = gen_verify_plane.get_plane_verifier_instance(platform, gfx_index)
        feature = self.fetch_enabled_feature(gfx_index, platform, panel)
        is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, panel.pipe)
        self.pipe_args.flip_metadata = self.panel_props_dict[gfx_index, port].flip_metadata if is_hdr_enabled else None
        plane_color_ctl_info = plane_verifier.regs.get_plane_color_ctl_info(plane, panel.pipe)
        plane_ctl_info = plane_verifier.regs.get_plane_ctl_info(plane, panel.pipe)
        pixel_format = plane_ctl_info.SourcePixelFormat
        plane_args = hdr_utility.PlaneArgs(color_enums.ColorSpace.RGB, pixel_format)
        logging.info("")
        logging.info("Performing Plane Verification on Adapter {0}  Pipe {1}".format(gfx_index, panel.pipe))
        ##
        # Performing FP16 Normalizer Verification
        pixel_normalizer_info = plane_verifier.regs.get_plane_pixel_normalizer_info(plane, panel.pipe)
        logging.info(
            "Performing FP16Normalization Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                 panel.pipe))
        logging.info("Pixel Format is {0}".format(color_constants.source_pixel_format_dict[pixel_format]))
        status, fp16_normalizer_enable = hdr_utility.verify_fp16_normalizer_enable_status(pixel_format, gfx_index,
                                                                                          panel.pipe, plane,
                                                                                          pixel_normalizer_info,
                                                                                          feature)
        if status is False:
            return False
        if fp16_normalizer_enable:
            if plane_verifier.verify_fp16_normalizer_programming(panel.pipe, pixel_normalizer_info) is False:
                return False

        ##
        # Performing InputCSC Verification
        logging.info("")
        logging.info("Performing InputCSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                                 panel.pipe))
        status, verify_icsc_matrix = hdr_utility.verify_input_csc_enable_status(pixel_format, 'FULL', gfx_index,
                                                                                panel.pipe, plane, plane_color_ctl_info)
        if status is False:
            return False
        if verify_icsc_matrix:
            # @todo - Matrix verification to be updated once able to get ColorSpace Enum from the ETLs
            pass

        ##
        # Performing Plane PreCSC Gamma Verification
        logging.info("")
        logging.info(
            "Performing Plane PreCSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                            panel.pipe))
        status, verify_pre_csc_gamma_lut = hdr_utility.verify_pre_csc_gamma_enable_status(pixel_format, gfx_index,
                                                                                          panel.pipe, plane,
                                                                                          plane_color_ctl_info)
        if status is False:
            return False
        if verify_pre_csc_gamma_lut:
            # @todo - LUT verification to be updated once able to get ColorSpace Enum from the ETLs
            pass

        ##
        # @todo : To be updated with Plane CSC verification once able to get ColorSpace Enum from the ETLs
        if panel.is_lfp and self.enable_wcg is True and plane_color_ctl_info.PlaneCscEnable:
            if plane_verifier.verify_plane_csc_programming(plane_args, pixel_format, plane, panel.pipe) is False:
                return False

        ##
        # Performing Plane PostCSC Verification
        logging.info("")
        logging.info(
            "Performing Plane PostCSC Verification on Adapter {0} Plane {1} Pipe {2}".format(gfx_index, plane,
                                                                                             panel.pipe))
        status, verify_post_csc_gamma_lut = hdr_utility.verify_post_csc_gamma_enable_status(gfx_index, plane,
                                                                                            panel.pipe,
                                                                                            plane_color_ctl_info,
                                                                                            feature)
        if status is False:
            return False
        if verify_post_csc_gamma_lut:
            # @todo - LUT verification to be updated once able to get ColorSpace Enum from the ETLs
            pass
        logging.info(
            "PASS : Plane Verification is Successful on Adapter {0}  Pipe {1}".format(gfx_index, panel.pipe))
        return True

    def verify_feature_modeset_from_os(self, pipe: str, enable: bool, feature: str = 'HDR'):
        status, self.bpc = color_etl_utility.fetch_feature_modeset_details_from_os(pipe, feature)
        if enable and status is False:
            logging.error("FAIL : {0} Modeset from OS failed on Pipe {1}".format(feature, pipe))
            return False, self.bpc
        logging.info("PASS : {0} Modeset from OS is successful on Pipe {1}".format(feature, pipe))
        logging.info("BPC is {0}".format(self.bpc))
        return True, self.bpc

    ##
    # @brief Function to enable HDR on all the panels supporting HDR
    def toggle_hdr_on_all_supported_panels(self, enable: bool) -> bool:
        toggle_option = 'Enabling' if enable else 'Disabling'
        feature = "WCG" if self.enable_wcg else "HDR"
        logging.debug("Feature is {0}".format(feature))


        ##
        # Configure HDR by invoking the OS API on all the supported panels
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if color_escapes.configure_hdr(port, panel.display_and_adapterInfo,
                                                   enable=enable, feature=feature) is False:
                        return False
                    if feature == "HDR" and panel.is_lfp:
                        ##
                        # If the request is to disable
                        if enable is False:
                            self.b3_val = str(100)
                        color_properties.set_b3_slider(self.b3_val)
                else:
                    logging.error("Panel Inactive")
                    self.fail()

        ##
        # Collect and parse the ETL once HDR is enabled across all the panels
        # Verify if OS has issued the HDR Modeset and driver has programmed HDR mode accordingly
        init_etl = "After_" + toggle_option + feature + "_TimeStamp_"
        self.init_etl_path = color_etl_utility.stop_etl_capture(init_etl)

        if etl_parser.generate_report(self.init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
        else:
            ##
            # Start the ETL again for capturing other events
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                status, self.bpc = self.verify_feature_modeset_from_os(panel.pipe, enable, feature)
                if status is False:
                    return False
                panel_props = color_properties.HDRProperties()
                panel_props.bpc = self.bpc
                self.panel_props_dict[gfx_index, port] = panel_props
                if feature == 'HDR':
                    if feature_basic_verify.verify_hdr_feature(gfx_index, adapter.platform, panel.pipe,
                                                               enable=enable) is False:
                        return False
                if self.enable_regkey_dithering:
                    if feature_basic_verify.verify_dithering_feature(adapter.gfx_index, adapter.platform, panel.pipe, panel.transcoder,
                                                                     True) is False:
                        self.fail()
        return True

    ##
    # Disables HDR enabled on all HDR supported panels.
    # In case of an eDP HDR panel, sets the OS Brightness slider to 100
    # Applies Unity Gamma and invokes the Common Base Class's tearDown()
    def tearDown(self):
        logging.info("Performing TearDown")
        for gfx_index, adapter in self.context_args.adapters.items():
            if self.enable_regkey_dithering:
                self.enable_regkey_dithering = False
                if common_utility.write_registry(gfx_index=gfx_index, reg_name="ForceDitheringEnable",
                                                 reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                                 driver_restart_required=True) is False:
                    logging.error("Failed to enable ForceDitheringEnable registry key")
                    self.fail("Failed to disable ForceDitheringEnable registry key")
                logging.info("Registry key add to disable ForceDitheringEnable is successful")

        if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        # Resetting LACE to default version
        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD,
                                         reg_value=self.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            self.fail("Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")

        ##
        # Apply Unity Gamma as part of clean-up
        gamma_utility.apply_gamma()
        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        super().tearDown()
