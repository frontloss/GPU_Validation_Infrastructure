import os
import sys
import json
import logging
from copy import deepcopy

from Libs.Core import enum, registry_access, system_utility
from Libs.Core.wrapper.driver_escape_args import CSCPipeMatrixParams
from Libs.Core.test_env import test_context
from DisplayRegs.DisplayArgs import TranscoderType
from Tests.Color.ApplyCSC.csc_utility import get_csc_coeff_matrix_from_reg
from Tests.Color.Common.color_enums import ConversionType, YuvSampling, ColorSpace
from Tests.Color.Common.csc_utility import compare_csc_coeff
from Tests.Color.Features.ApplyCSC import apply_csc
from Tests.Color.Verification import gen_verify_pipe
from Tests.test_base import TestBase
from Tests.Color.Common import color_enums, common_utility, csc_utility, color_escapes, hdr_utility
from Tests.Color.Common.common_utility import get_action_type
from Libs.Core.logger import gdhm

##
# @brief - To perform setUp and tearDown functions
class ApplyCSCTestBase(TestBase):
    scenario = None
    set_range = None
    matrix_info = None

    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):
        input_csc_file_path = os.path.join(self.context_args.test.path_info.root_path,
                                           "Tests\\Color\\Features\\ApplyCSC\\input_csc_matrix.json")
        self.custom_tags["-CSC_TYPE"] = None
        self.custom_tags["-MATRIX_INFO"] = None
        super().setUp()

        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.csc_type = str(self.context_args.test.cmd_params.test_custom_tags["-CSC_TYPE"][0])
        self.matrix_name = str(self.context_args.test.cmd_params.test_custom_tags["-MATRIX_INFO"][0])

        with open(input_csc_file_path) as f:
            csc_info = json.load(f)
        for index in range(0, len(csc_info)):
            if csc_info[index]['name'] == self.matrix_name:
                self.matrix_info = csc_info[index]['matrix']

        self.csc_type = color_enums.CscMatrixType.LINEAR_CSC.value if self.csc_type == 'LINEAR_CSC' else color_enums.CscMatrixType.NON_LINEAR_CSC.value

    ##
    # @brief         Wrapper to - verify the register for ocsc, pre and post offsets and
    #                             gamma ctrl register for linear
    # @param[in]     gfx_index - gfx_0 or gfx_1
    # @param[in]     platform - platform Info
    # @param[in]     pipe - pipe_info
    # @return        True or False
    def enable_and_verify(self, gfx_index, platform, pipe, display_and_adapterInfo, port, configure_csc=True):
        pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
        pipe_args = hdr_utility.E2EPipeArgs()

        cc_block = common_utility.get_color_conversion_block(platform, pipe)

        #
        # update this parameter for ref_csc_value
        pipe_args.os_relative_csc = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        pipe_args.escape_csc = self.matrix_info
        if configure_csc:
            if color_escapes.configure_pipe_csc(port, display_and_adapterInfo, self.csc_type, self.matrix_info, True) is False:
                return False

        if self.csc_type == color_enums.CscMatrixType.LINEAR_CSC.value:
            reg_name = "PipeCscCoeff" if cc_block == "CC1" else "PipeCscCc2Coeff"
            if pipe_verification.verify_pipe_csc_programming(pipe_args, pipe, reg_name=reg_name):
                if apply_csc.verify_gamma_ctrl_prog_linear_mode(gfx_index, platform, pipe,
                                                                color_conv_blk=cc_block) is False:
                    self.fail()
            else:
                self.fail()
        else:
            if pipe_verification.verify_pipe_csc_programming(pipe_args, pipe, 'PipeOutputCscCoeff') is False:
                self.fail()

    ##
    # @brief unittest TearDown function
    # @param[in] self
    # @return None
    def tearDown(self):
        ##
        # Apply Identity Matrix at the end of the test
        ## @ note: will confirm the below implementation with ULT
        param = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo, self.csc_type, param, True) is False:
                        logging.info(
                            "Failed to apply {0} Identity CSC after completion of the test on {1}".format(color_enums.CscMatrixType(
                                self.csc_type).name, panel.connector_port_type))
                        self.fail(
                            "Failed to apply Identity CSC after completion of the test on {0}".format(panel.connector_port_type))
        super().tearDown()
