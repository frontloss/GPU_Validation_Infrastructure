########################################################################################################################
# @file         hw_3d_lut_with_igcl_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API
#               and HW 3D LUT verification
#                   * Enable/restore/verify  Pixel Transformation of 3DLUT API.
# @author       Vimalesh D
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import display_essential, reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Tests.Color.Common import color_constants, color_igcl_wrapper, color_igcl_escapes
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_cc_block import fetch_igcl_color_ftrs_caps_and_verify
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - Enable/restore/verify 3DLUT Pixel Transformation Control Library Test
class Hw3DLutIgclApi(Hw3DLUTBase):


    ##
    # @brief        setup for 3DLUT igcl to decide the status for the subtest
    # @return       None
    def setUp(self):
        self.custom_tags["-STATUS"] = None
        super().setUp()
        self.status = str(self.context_args.test.cmd_params.test_custom_tags["-STATUS"][0])
        if self.status == 'ENABLE':
            self.status = True
        else:
            self.status = False

    ##
    # @brief            test_01_basic() executes the actual test steps to enable 3DLUT.
    # @return           void
    @unittest.skipIf(get_action_type() != "ENABLE", "Skip the test step as the action type is not basic")
    def test_01_enable(self):
        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    # The dictionary is designed as it uses existing igcl color escape api for preparing the args
                    igcl_color_ftr_data = {'3DLUT': None, 'DGLUT': None, 'CSC': None, 'GLUT': None, 'oCSC': None}
                    igcl_color_ftr_index = {'3DLUT': None, 'DGLUT': None, 'CSC': None, 'GLUT': None, 'oCSC': None}

                    user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value
                    status, igcl_get_caps = fetch_igcl_color_ftrs_caps_and_verify(gfx_index,
                                                                                  adapter.platform,
                                                                                  panel.connector_port_type,
                                                                                  panel.pipe,
                                                                                  panel.target_id,
                                                                                  user_req_color_blk)
                    if status is False:
                        logging.error("FAIL : IGCL Support for {0} has not been reported by the driver on {1} connected "
                                      "to Pipe {2} on adapter {3} "
                                      .format(color_igcl_wrapper.IgclColorBlocks(user_req_color_blk).name,
                                              panel.connector_port_type, panel.pipe, gfx_index))
                        self.fail()
                    if "R.BIN" in self.inputfile:
                        sample_lut_name  = "NO_RED"
                    elif "G.BIN" in self.inputfile:
                        sample_lut_name = "NO_GREEN"
                    else:
                        sample_lut_name = "NO_BLUE"

                    igcl_color_ftr_data['3DLUT']  = str(sample_lut_name)
                    igcl_set_args = color_igcl_wrapper.prepare_igcl_color_escapes_args_for_set(gfx_index, adapter.platform,
                                                                                               panel.connector_port_type,
                                                                                               panel.pipe,
                                                                                               igcl_get_caps,
                                                                                               user_req_color_blk,
                                                                                               1,
                                                                                               igcl_color_ftr_data,
                                                                                               igcl_color_ftr_index)
                    argsLutConfig = color_igcl_wrapper.prepare_igcl_set_args_for_3dlut(igcl_get_caps,
                                                                                       igcl_color_ftr_index['3DLUT'])
                    igcl_set_args.pBlockConfigs = igcl_get_caps.pBlockConfigs
                    if control_api_wrapper.set_3dlut(igcl_set_args, argsLutConfig, panel.target_id):
                        logging.info("Set HW_3DLUT feature is successful")
                    else:
                        self.fail("Set HW_3DLUT feature is failure")
                    if feature_basic_verify.verify_hw3dlut_feature(gfx_index, adapter.platform, panel.pipe,
                                                                   self.status) is False:
                        self.fail("Fail: HW_3D_LUT Expected: Enabled Actual: Not Enabled")
                    logging.info("Pass: Set 3DLUT Pixel Transformation")


    ##
    # @brief            test_01_basic() executes the actual test steps to restore to default.
    # @return           void
    @unittest.skipIf(get_action_type() != "DISABLE", "Skip the test step as the action type is not basic")
    def test_02_disable(self):
        igcl_esc_restore_default = color_igcl_wrapper.prepare_igcl_color_esc_args_for_restore_default()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if color_igcl_escapes.perform_restore_default(igcl_esc_restore_default, panel.target_id):
                        logging.info("PASS: Restore Default Values for Color Blocks")
                    else:
                        logging.error("FAIL: Restore Default Values for Color Blocks")
                        self.fail()


    ##
    # @brief            test_01_basic() executes the actual test steps to verify 3DLUT.
    # @return           void
    @unittest.skipIf(get_action_type() != "VERIFY", "Skip the test step as the action type is not basic")
    def test_03_verify(self):
        ##
        # HW3DLUT should not persist after reboot scenario
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # verify_hw3dlut_feature
                    if feature_basic_verify.verify_hw3dlut_feature(gfx_index, adapter.platform, panel.pipe,
                                                                   self.status) is False:
                        self.fail("Fail: HW_3D_LUT not persisted after reboot")
                    logging.info("HW_3D_LUT persisted after reboot")

    ##
    # @brief        Teardown to skip the base class teardown to avoid Lace Disable
    # @return       None
    def tearDown(self):
        logging.info("----Lace Manual Test Operation completed----")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set 3DLUT API Verification with Manual scenario')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)