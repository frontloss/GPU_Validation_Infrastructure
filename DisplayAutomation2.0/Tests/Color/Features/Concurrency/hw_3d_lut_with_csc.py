#################################################################################################
# @file         hw_3d_lut_with_gamma.py
# @brief        This is a custom script which can used to apply both SINGLE and CLONE display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of basic test function and the function  will perform below functionalities
#               1.To configure enable/disable 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               4.Verify the persistence after the non- unity gamma values
# @author       Vimalesh D
#################################################################################################
import logging
import logging
import sys
import time
import unittest
import random
import os

from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import gamma_utility, hdr_utility
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - Hw3DLut basic test
from Tests.Color.HDR.Gen11_Flip.MPO3H.HDRConstants import SRGB_Encode_515_Samples_16bpc
from Tests.Color.Verification import gen_verify_pipe


class Hw3DLutBasicWithGamma(Hw3DLUTBase):

    def setUp(self):
        self.custom_tags["-INPUTFILE"] = None
        bin_files = ["CustomLUT_no_R.bin", "CustomLUT_no_G.bin", "CustomLUT_no_B.bin"]
        super().setUp()

        if len(str(self.context_args.test.cmd_params.test_custom_tags["-INPUTFILE"][0])) > 1:
            self.inputfile = str(self.context_args.test.cmd_params.test_custom_tags["-INPUTFILE"][0])
        else:
            self.inputfile = random.choice(bin_files)
        bin_file_path = "Color\\Hw3DLUT\\CustomLUT\\" + self.inputfile
        self.inputfile = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self):
        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Apply a csc matrix and verify before enabling HDR
                    logging.info(
                        "*** Step 1 : Invoke the escape call to apply CSC input from Command Line and verify ***")
                    for gfx_index, adapter in self.context_args.adapters.items():
                        for port, panel in adapter.panels.items():
                            if color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo, self.csc_type,
                                                                self.matrix_info, True) is False:
                                logging.error(
                                    "FAIL : Driver failed to apply CSC on {0} connected to {1} on Adapter {2}".format(
                                        port, panel.pipe, gfx_index))
                                self.fail()
                    ##
                    # Applying Gamma with a scalefactor of r_factor=0.5, g_factor=0.75, b_factor= 0.9
                    gamma_utility.apply_gamma(r_factor=0.5, g_factor=0.75, b_factor= 0.9)
                    ##
                    # Apply a csc matrix and verify before enabling HDR
                    logging.info(
                        "*** Step 1 : Invoke the escape call to apply CSC input from Command Line and verify ***")
                    for gfx_index, adapter in self.context_args.adapters.items():
                        for port, panel in adapter.panels.items():
                            if color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo, self.csc_type,
                                                                self.matrix_info, True) is False:
                                logging.error(
                                    "FAIL : Driver failed to apply CSC on {0} connected to {1} on Adapter {2}".format(
                                        port, panel.pipe, gfx_index))
                                self.fail()
                    for gfx_index, adapter in self.context_args.adapters.items():
                        for port, panel in adapter.panels.items():
                            ##
                            # Verify the 3DLUT disabled
                            if panel.is_active and panel.is_lfp:
                                if panel.is_active:

                                    pipe_args = hdr_utility.E2EPipeArgs()
                                    pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(
                                        self.context_args.adapters[gfx_index].platform, gfx_index)
                                    color_ctl_offsets = pipe_verifier.regs.get_color_ctrl_offsets(panel.pipe)

                                    ##
                                    # Performing Pipe Degamma Verification
                                    logging.info(
                                        "Performing Pipe Degamma Verification for {0} on Adapter : {1}  Pipe : {2}".format(port,
                                                                                                                           gfx_index,
                                                                                                                           panel.pipe))
                                    # ##
                                    # # Verification if the PreCSC block has been enabled in case of SDR
                                    gamma_mode = pipe_verifier.mmio_interface.read(gfx_index, color_ctl_offsets.GammaMode)
                                    gamma_mode_value = pipe_verifier.regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
                                        GammaMode=gamma_mode))

                                    cc_block = common_utility.get_color_conversion_block(adapter.platform, panel.pipe)
                                    if gamma_mode_value.PreCscGammaEnable:
                                        if pipe_verifier.verify_pipe_degamma_programming(panel.pipe, cc_block):

                                            if gamma_mode_value.PostCscGammaEnable:
                                                if pipe_verifier.verify_pipe_gamma_programming(pipe_args, panel.pipe, cc_block) is False:
                                                    self.fail()
                                    else:
                                        self.fail()
                                ##
                                if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                                   panel.pipe,panel.transcoder, panel.target_id,panel.is_lfp, self.inputfile, enable=True) is False:
                                    self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with HDR")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
