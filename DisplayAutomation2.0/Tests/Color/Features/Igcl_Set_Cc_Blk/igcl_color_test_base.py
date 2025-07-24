#################################################################################################
# @file         igcl_color_test_base.py
# @brief        This script is a Feature Base class specific to IGCL Color Blocks.
#               The igcl_color_test_base performs the below functionalities
#               to setup all the infra needed by the test scripts.
#               1.setUp() -  Invokes Common class's setUp() to perform basic functionalities
#                            Updates the display caps in the Context by parsing the ETLs.
#                            Test scripts expect at least one HDR supported panel to be passed
#                            Checks for the PowerMode and switches to AC mode if required to adhere to OS Policy
#               2.identify_igcl_blocks_to_be_enabled_from_cmd_param() - Parses the command prompt to identify the blocks
#                            to be enabled through the escape
#               3.fill_color_blocks_with_user_data() - Fill the data in the format to be passed to the escape call for
#                           the blocks requested to be enabled
#               4.enable_igcl_color_ftr_and_verify() - Invokes the IGCL Escape call with the requested blocks
#                           and performs verification of the blocks
#               5.tearDown() - Performs a restore default as a cleanup after the completion of the test
# @author       Smitha B
#################################################################################################
import json
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import etl_parser, enum
from Tests.test_base import *
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_cc_block import *
from Tests.Color.Common import color_properties, color_constants, color_enums, csc_utility
from Tests.Color.Common import color_etl_utility, hdr_utility, gamma_utility, common_utility, color_igcl_wrapper, color_igcl_escapes
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify
from Tests.Color.ApplyCSC.csc_utility import *


class IGCLColorTestBase(TestBase):
    scenario = None
    hw3dlut, dglut, csc, glut, oCSC = None, None, None, None, None
    hw3dlut_info, dglut_info, matrix_info, glut_info, ocsc_info = None, None, None, None, None
    num_blocks_to_be_set = -1
    user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.ERROR.value
    init_file_path = None
    pipe_args = hdr_utility.E2EPipeArgs()

    ##
    # A dictionary of all the properties related to the displays passed from command line
    # This dictionary have a tuple of gfx_index and connector_port_type as key
    # and the value contains all the display related properties enclosed in a list
    panel_props_dict = {}

    ##
    # This dictionary contains all the necessary details to be passed to the escape function
    # The dictionary is designed in the same order as the driver structure
    igcl_color_ftr_data = {'3DLUT': None,
                           'DGLUT': None,
                           'CSC': None,
                           'GLUT': None,
                           'oCSC': None
                           }

    igcl_color_ftr_index = {'3DLUT': None,
                           'DGLUT': None,
                           'CSC': None,
                           'GLUT': None,
                           'oCSC': None
                           }

    def identify_igcl_blocks_to_be_enabled_from_cmd_param(self):
        self.hw3dlut = str(self.context_args.test.cmd_params.test_custom_tags["-HW3DLUT"][0])
        self.dglut = str(self.context_args.test.cmd_params.test_custom_tags["-DGLUT"][0])
        self.csc = str(self.context_args.test.cmd_params.test_custom_tags["-CSC"][0])
        self.glut = str(self.context_args.test.cmd_params.test_custom_tags["-GLUT"][0])
        self.oCSC = str(self.context_args.test.cmd_params.test_custom_tags["-OCSC"][0])

        ##
        # Identifying which all blocks need to be enabled by checking the command line parameters
        if self.hw3dlut == 'NONE' and self.dglut == 'NONE' and self.csc == 'NONE' and self.glut == 'NONE' \
                and self.oCSC == 'NONE':
            logging.error("FAIL : Incorrect command line! Atleast one of the blocks should be requested as part of "
                          "the command line")
            return self.num_blocks_to_be_set

        self.num_blocks_to_be_set = 1
        ##
        # Check if it is only HW3DLUT
        if self.hw3dlut not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value

        if self.dglut not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.DGLUT.value

        if self.csc not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.CSC.value

        if self.glut not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.GLUT.value

        if self.oCSC not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.OCSC.value

        if self.dglut not in 'NONE' and self.csc not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC.value
            self.num_blocks_to_be_set = 2

        if self.dglut not in 'NONE' and self.glut not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.DGLUT_GLUT.value
            self.num_blocks_to_be_set = 2

        if self.dglut not in 'NONE' and self.csc not in 'NONE' and self.glut not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC_GLUT.value
            self.num_blocks_to_be_set = 3

        if self.hw3dlut not in 'NONE' and self.dglut not in 'NONE' and self.csc not in 'NONE' and self.glut not in 'NONE' and self.oCSC not in 'NONE':
            self.user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.ALL.value
            self.num_blocks_to_be_set = 5

        logging.info("User requested {0} blocks to be enabled. Block Details : {1}".format(self.num_blocks_to_be_set,
                                                                                         color_igcl_wrapper.IgclColorBlocks(
                                                                                             self.user_req_color_blk).name))

    def fill_color_blocks_with_user_data(self):
        for color_blk, blk_data in self.igcl_color_ftr_data.items():

            if color_blk == "3DLUT":
                pass

            elif color_blk == "DGLUT":
                self.igcl_color_ftr_data['DGLUT'] = self.dglut_info

            elif color_blk == "CSC":
                self.igcl_color_ftr_data['CSC'] = self.matrix_info

            elif color_blk == "GLUT":
                self.igcl_color_ftr_data['GLUT'] = self.glut_info

            else:
                if color_blk == "oCSC":
                    self.igcl_color_ftr_data['oCSC'] = self.ocsc_info

    def setUp(self):
        self.custom_tags["-HW3DLUT"] = 'NONE'
        self.custom_tags["-DGLUT"] = 'NONE'
        self.custom_tags["-CSC"] = 'NONE'
        self.custom_tags["-GLUT"] = 'NONE'
        self.custom_tags["-OCSC"] = 'NONE'

        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()


    def prepare_color_properties(self):
        color_etl_utility.start_etl_capture()
        ##
        # Parse the command line parameters for the Color Blocks requested by the user
        self.identify_igcl_blocks_to_be_enabled_from_cmd_param()
        if color_igcl_wrapper.IgclColorBlocks(
                self.user_req_color_blk).name == color_igcl_wrapper.IgclColorBlocks.ERROR.name:
            self.fail()

        input_dglut_file_path = os.path.join(self.context_args.test.path_info.root_path,
                                             "Tests\\Color\\Features\\Igcl_Set_Cc_Blk\\input_dglut.json")

        input_csc_file_path = os.path.join(self.context_args.test.path_info.root_path,
                                           "Tests\\Color\\Features\\Igcl_Set_Cc_Blk\\input_csc_matrix.json")

        input_glut_file_path = os.path.join(self.context_args.test.path_info.root_path,
                                            "Tests\\Color\\Features\\Igcl_Set_Cc_Blk\\input_glut.json")

        ##
        # Check the JSON files to get the LUTs/Matrices corresponding to the Command Line Parameters
        with open(input_csc_file_path) as csc_file:
            input_info = json.load(csc_file)
        for index in range(0, len(input_info)):
            if input_info[index]['name'] == self.csc:
                self.matrix_info = input_info[index]['matrix']

        with open(input_dglut_file_path) as dglut_file:
            input_info = json.load(dglut_file)
        for index in range(0, len(input_info)):
            if input_info[index]['name'] == self.dglut:
                self.dglut_info = input_info[index]['dglut']

        with open(input_glut_file_path) as glut_file:
            input_info = json.load(glut_file)
            for index in range(0, len(input_info)):
                if input_info[index]['name'] == self.glut:
                    self.glut_info = input_info[index]['glut']

        with open(input_csc_file_path) as csc_file:
            input_info = json.load(csc_file)
        for index in range(0, len(input_info)):
            if input_info[index]['name'] == self.oCSC:
                self.ocsc_info = input_info[index]['matrix']

        ##
        # Fill the Data in a dictionary for each of the blocks
        self.fill_color_blocks_with_user_data()
        
        ##
        # Applying Unity Gamma
        color_common_utility.apply_unity_gamma()
        time.sleep(5)

        #
        # Stop the ETL and initialize CSC, Gamma components if OS has given any Calls
        init_etl = "Before_Invoking_Any_Escape_Calls_" + "_TimeStamp_"
        self.init_etl_path = color_etl_utility.stop_etl_capture(init_etl)
        time.sleep(3)

        if etl_parser.generate_report(self.init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
        else:
            ##
            # Start the ETL again for capturing other events
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")

            ##
            # Update the feature Capabilities such to the Test Context
            color_properties.update_feature_caps_in_context(self.context_args)

            ##
            # Initialize all the Color properties for all the panels
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    panel_props = color_properties.HDRProperties()
                    self.panel_props_dict[gfx_index, port] = panel_props

            color_properties.initialize_common_color_props(self.context_args, self.panel_props_dict)

    ##
    # Pipe Verification includes :
    # Pipe Pre CSC     - To be disabled in case of HDR; Enabled in case of SDR and perform LUT verification
    # Pipe CSC         - To be enabled and perform Matrix verification with reference matrix from ETL
    # Pipe Post CSC    - To be enabled; LUT verification including Pixel Boost Verification for eDP HDR
    # Pipe OutputCSC   - To be enabled if Pipe is in YUV or if OutputRange was in Limited in case of RGB;
    #                    Perform Matrix verification
    # HDR Verification - DPCD Verification - In Case of eDP HDR (SDP/Aux Based);
    def pipe_verification(self, gfx_index, platform, port, panel, is_smooth_brightness=False,
                          step_index=0):
        enabled_mode = hdr_utility.fetch_enabled_mode(gfx_index, platform, panel.pipe)
        enabled_mode = color_enums.ColorMode(enabled_mode).name
        ##
        # ToDo : Remove this and update all the affected APIs
        logging.info("Feature Name is {0}".format(enabled_mode))

        logging.info("")
        logging.info(
            "Performing Pipe Verification for Panel {0} on Adapter {1} attached to Pipe {2} for {3} Mode".format(
                port, gfx_index,
                panel.pipe, enabled_mode))

        cc_block = common_utility.get_color_conversion_block(platform, panel.pipe, enabled_mode)
        pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
        color_ctl_offsets = pipe_verifier.regs.get_color_ctrl_offsets(panel.pipe)

        ##
        # Performing Pipe Degamma Verification
        logging.info("")
        logging.info(
            "Performing Pipe Degamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                               panel.pipe))
        ##
        # Verification if the PreCSC block has been enabled in case of SDR and otherwise for HDR
        gamma_mode = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.GammaMode)
        gamma_mode_value = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            GammaMode=gamma_mode))
        status, verify_pipe_pre_csc_lut = hdr_utility.verify_pipe_pre_csc_gamma_enable_status(gfx_index, panel.pipe,
                                                                                              gamma_mode_value,
                                                                                              cc_block,
                                                                                              enabled_mode)
        if status is False:
            return False
        if verify_pipe_pre_csc_lut:
            self.pipe_args.dglut_curve_type = self.dglut
            if pipe_verifier.verify_pipe_degamma_programming(self.pipe_args, panel.pipe, cc_block) is False:
                return False

        ##
        # Performing Pipe CSC Verification
        logging.info("")
        logging.info(
            "Performing Pipe CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                           panel.pipe))
        ##
        # Verification if the CSC block has been enabled
        csc_mode_val = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_values = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
            CscMode=csc_mode_val))
        status, verify_pipe_csc_matrix = hdr_utility.verify_pipe_csc_enable_status(gfx_index, panel.pipe,
                                                                                   self.panel_props_dict[
                                                                                       gfx_index, port].oned_lut_param_type,
                                                                                   self.panel_props_dict[
                                                                                       gfx_index, port].gamma_ramp_type,
                                                                                   cc_block,
                                                                                   color_ctl_values)
        if status is False:
            return False
        if verify_pipe_csc_matrix:
            self.pipe_args.escape_csc = self.matrix_info
            self.pipe_args.os_relative_csc = self.panel_props_dict[gfx_index, port].os_relative_csc
            reg_name = "PipeCscCoeff" if cc_block == "CC1" else "PipeCscCc2Coeff"
            if pipe_verifier.verify_pipe_csc_programming(self.pipe_args, panel.pipe, reg_name,
                                                         feature=enabled_mode) is False:
                return False

        # ##
        # Performing Pipe Gamma Verification
        if enabled_mode == "HDR":
            self.pipe_args.is_smooth_brightness = is_smooth_brightness
            self.pipe_args.step_index = step_index
            self.pipe_args.pixel_boost = self.panel_props_dict[gfx_index, port].pixel_boost

        self.pipe_args.os_relative_lut = self.panel_props_dict[gfx_index, port].os_relative_lut

        self.pipe_args.dsb_gamma_dump = self.panel_props_dict[gfx_index, port].dsb_gamma_dump
        logging.info("")
        logging.info(
            "Performing Pipe Gamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                             panel.pipe))
        status, verify_pipe_post_csc_gamma_lut = hdr_utility.verify_pipe_post_csc_gamma_status(gfx_index,
                                                                                               panel.pipe,
                                                                                               gamma_mode_value,
                                                                                               cc_block)
        if status is False:
            return False

        if enabled_mode == "HDR":
            # # In HDR Mode, since DGLUT will be disabled by default, the GLUT will always be the correction LUT on
            # top of the OETF_2084 curve
            # Note : If any Full LUT is given, for ex : UNITY LUT in HDR Mode,
            # it might lead to a Blankout. Here, driver is not responsible as the behavior is clearly stated in the
            # Documentation and the Apps are required to adhere to the rules
            gamma_curve_type = 'OETF_2084'
            self.pipe_args.escape_correction_glut = self.glut_info
        else:
            # # If DGLUT is not specified by the User, then driver considers the GLUT as a Correction LUT on top of
            # the SRG_Gamma Curve in SDR Mode
            gamma_curve_type = 'SRGB_GAMMA_CURVE'
            ##
            # If only GLUT is given, then it will be considered as a Correction LUT
            if self.dglut in 'NONE':
                if self.glut not in 'NONE':
                    gamma_curve_type = 'CORRECTION_LUT_IN_SDR'
                    self.pipe_args.escape_correction_glut = self.glut_info
            else:
                # # If DGLUT is also specified by the user, then it is the User's responsibility to give the
                # appropriate DGLUT-GLUT pair
                # Here, the GLUT will be considered as a FULL LUT by the driver
                if self.glut not in 'NONE':
                    gamma_curve_type = self.glut
                    self.pipe_args.escape_correction_glut = self.glut_info

        self.pipe_args.glut_curve_type = gamma_curve_type
        if verify_pipe_post_csc_gamma_lut:
            if pipe_verifier.verify_pipe_gamma_programming(self.pipe_args, panel.pipe, cc_block) is False:
                return False

        ##
        # Performing Pipe oCSC Verification
        logging.info("")
        logging.debug(
            "Performing Pipe Output CSC Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index,
                                                                                                  panel.pipe))
        if self.oCSC != 'N':
            if color_ctl_values.PipeOutputCscEnable is False:
                logging.error(
                    "FAIL : Pipe oCSC on Adapter : {0}  Pipe : {1} Expected : ENABLED : Actual : {2}".format(gfx_index,
                                                                                                             panel.pipe,
                                                                                                             feature_basic_verify.BIT_MAP_DICT[
                                                                                                                 int(
                                                                                                                     color_ctl_values.PipeOutputCscEnable)]))
                self.fail()
            else:
                input = color_enums.ColorSpace.RGB
                output = color_enums.ColorSpace.RGB
                conv_type = color_enums.ConversionType.FULL_TO_FULL
                if pipe_verifier.verify_output_csc_programming(panel.pipe, 8, input, output, conv_type, igcl_input_csc=self.ocsc_info) is False:
                    return False

        return True

    def enable_igcl_color_ftr_and_verify(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                status, igcl_get_caps = fetch_igcl_color_ftrs_caps_and_verify(gfx_index,
                                                                                                 adapter.platform,
                                                                                                 panel.connector_port_type,
                                                                                                 panel.pipe,
                                                                                                 panel.target_id,
                                                                                                 self.user_req_color_blk)

                if status is False:
                    logging.error("FAIL : IGCL Support for {0} has not been reported by the driver on {1} connected "
                                  "to Pipe {2} on adapter {3} "
                                  .format(color_igcl_wrapper.IgclColorBlocks(self.user_req_color_blk).name,
                                          panel.connector_port_type, panel.pipe, gfx_index))
                    self.fail()

                igcl_set_args = color_igcl_wrapper.prepare_igcl_color_escapes_args_for_set(gfx_index, adapter.platform,
                                                                                           panel.connector_port_type,
                                                                                           panel.pipe,
                                                                                           igcl_get_caps,
                                                                                           self.user_req_color_blk,
                                                                                           self.num_blocks_to_be_set,
                                                                                           self.igcl_color_ftr_data,
                                                                                           self.igcl_color_ftr_index)
                mode_enabled = hdr_utility.fetch_enabled_mode(gfx_index, adapter.platform, panel.pipe)
                if color_igcl_escapes.set_igcl_color_feature(igcl_set_args, igcl_get_caps, panel.target_id,
                                                        self.user_req_color_blk, mode_enabled) is False:
                    logging.error("Set overall feature is failing")
                    self.fail()
                else:
                    logging.info("Set overall feature is successful")
                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                        self.fail()
        return True

    def tearDown(self):
        logging.info("Performing TearDown")

        igcl_esc_restore_default = color_igcl_wrapper.prepare_igcl_color_esc_args_for_restore_default()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if color_igcl_escapes.perform_restore_default(igcl_esc_restore_default, panel.target_id):
                    logging.info("PASS: Restore Default Values for Color Blocks")
                else:
                    logging.error("FAIL: Restore Default Values for Color Blocks")
                    self.fail()
        super().tearDown()
