#################################################################################################
# @file         hw_3d_lut_base.py
# @brief        This scripts comprises of below functions.
#               1.setUp() -  To apply the display config and update the custom tags.
#               2.tearDown() - To unplug the display and restore to default for updated the feature caps
#               3.enable_and_verify() - Will configure the aviinfo and verify the registers
# @author       Vimalesh D
#################################################################################################
import logging
import os
import sys
import time
import unittest
import random

from Libs.Core.test_env import test_context
from Tests.Color.Common.color_constants import POST_GEN14_PLATFORMS
from Tests.Color.Features.HW_3D_LUT import hw_3dlut
from Tests.PowerCons.Modules import polling
from Tests.test_base import TestBase
from Libs.Core import registry_access
from DisplayRegs.DisplayArgs import TranscoderType
from Libs.Core.wrapper import control_api_wrapper
from Tests.Color.Common import color_escapes, common_utility, color_enums, color_constants, color_igcl_escapes, \
    color_properties, color_igcl_wrapper
from Libs.Core.logger import gdhm
from registers.mmioregister import MMIORegister

##
# @brief get_action_type
# @param[in] None
# @return argument value
def get_action_type():
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if '-SCENARIO' in tag_list and '-INPUTFILE' in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == '-SCENARIO':
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        assert False, "Wrong Commandline!! : Test_name.py -SCENARIO SCENARIO_NAME -INPUTFILE CustomLUT_no_R.bin"


##
# @brief - To perform setUp and tearDown functions
class Hw3DLUTBase(TestBase):
    scenario = None
    inputfile = None
    bpc = None
    three_dlut_enable_pipe = []

    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):
        lfp_panel_count = 0
        self.custom_tags["-BPC"] = None
        self.custom_tags["-INPUTFILE"] = None
        bin_files = ["CustomLUT_no_R.bin", "CustomLUT_no_G.bin", "CustomLUT_no_B.bin"]

        super().setUp()
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.bpc = str(self.context_args.test.cmd_params.test_custom_tags["-BPC"][0])

        if len(str(self.context_args.test.cmd_params.test_custom_tags["-INPUTFILE"][0])) > 1:
            self.inputfile = str(self.context_args.test.cmd_params.test_custom_tags["-INPUTFILE"][0])
        else:
            self.inputfile = random.choice(bin_files)
        bin_file_path = "Color\\Hw3DLUT\\CustomLUT\\" + self.inputfile
        self.inputfile = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)


    ##
    # @brief         Wrapper to - configure 3dlut and verify the register for 3dlut ctl and data
    # @param[in]     gfx_index - gfx_0 or gfx_1
    # @param[in]     port - port_type
    # @param[in]     platform - platform Info
    # @param[in]     pipe - pipe
    # @param[in]     transcoder - transcoder
    # @param[in]     display_and_adapterInfo - display_and_adapter_info
    # @param[in]     configure_dpp_hw_lut - Enable or Disable 3DLUT
    # @return        True on Success ,False on Failure.
    def enable_and_verify(self, gfx_index, port, platform, pipe, is_lfp, transcoder, display_and_adapterInfo, target_id,
                          configure_dpp_hw_lut):

        if not color_escapes.configure_dpp_hw_lut(port, display_and_adapterInfo, self.inputfile, configure_dpp_hw_lut):
            return False
        else:
            self.three_dlut_enable_pipe.append(pipe)
            logging.info("3DLUT enabled on pipe {0}".format(pipe))
            
        hw_3dlut.setup_for_verify(self.context_args.test.exec_env,gfx_index, platform, pipe)
        if not hw_3dlut.verify(gfx_index, platform, port, pipe, transcoder, target_id, self.inputfile, is_lfp,
                               configure_dpp_hw_lut):
            return False
    
    ##
    # @brief         Wrapper to - configure 3dlut and verify the register for 3dlut ctl and data
    def enable_and_verify_via_igcl(self, adapter, panel, enable):
        
        if enable is True:
            logging.info("Enabling 3DLUT support via IGCL for panel connected to port {0} pipe {1} on adapter {2}"
                         .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
            if not color_igcl_escapes.enable_verify_3d_lut_via_igcl(adapter, adapter.gfx_index, panel, self.inputfile):
                logging.error("Failed to enable 3DLUT support via IGCL for panel connected to port {0} pipe {1} on adapter {2}"
                             .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                return False
            else:
                self.three_dlut_enable_pipe.append(panel.pipe)
                logging.info("3DLUT enabled on pipe {0}" .format(panel.pipe))
                
        else:
            igcl_esc_restore_default = color_igcl_wrapper.prepare_igcl_color_esc_args_for_restore_default()
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active:
                        if color_igcl_escapes.perform_restore_default(igcl_esc_restore_default, panel.target_id):
                            logging.info("PASS: Restore Default Values for Color Blocks")
                            self.three_dlut_enable_pipe.clear()
                        else:
                            logging.error("FAIL: Restore Default Values for Color Blocks")
                            self.fail()
                            
        hw_3dlut.setup_for_verify(self.context_args.test.exec_env, adapter.gfx_index, adapter.platform, panel.pipe)
        if not hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type, panel.pipe, panel.transcoder,
                               panel.target_id, self.inputfile, panel.is_lfp, enable, via_igcl=True):
            return False

    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    feature_caps = color_properties.FeatureCaps()
                    feature_caps = common_utility.get_psr_caps(panel.target_id, feature_caps)
                    if feature_caps.PSRSupport:
                        logging.info("TearDown: Enable PSR")
                        if adapter.platform in POST_GEN14_PLATFORMS:
                            logging.info("Skip: Platform :{0} PSR/DC state Enable for 3DLUT".format(adapter.platform))
                        else:
                            if color_igcl_escapes.enable_disable_psr_via_igcl(panel.target_id, port, True) is False:
                                self.fail("Failed to enable PSR")
        super().tearDown()
