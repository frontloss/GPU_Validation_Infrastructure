#################################################################################################
# @file         hw_3d_lut_with_lace.py
# @brief        This is a custom script which can used to apply both SINGLE and CLONE display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of basic test function and the function  will perform below functionalities
#               1.To configure enable/disable 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               4.Verify the 3dlut persistence with lace
# @author       Vimalesh D
#################################################################################################

import sys
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *



##
# @brief - Hw3DLut basic test
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify


class Hw3DLutBasicWithLACE(Hw3DLUTBase):
    lace_version = None
    def setUp(self):
        self.custom_tags["-VERSION"] = None
        super().setUp()
        self.lace_version = str(self.context_args.test.cmd_params.test_custom_tags["-VERSION"][0])

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                              panel.pipe, panel.is_lfp, panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                              configure_dpp_hw_lut=True) is False:
                        self.fail()
                    time.sleep(2)
                    if color_escapes.configure_als_aggressiveness_level(port,panel.display_and_adapterInfo,lux=7500,aggressiveness_level=1,aggressiveness_operation=True,lux_operation=True):
                        time.sleep(2)
                        ##
                        # verify_lace_feature
                        if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,self.lace_version) is False:
                            self.fail("Lace verification failed")

                    ##
                    # Verify the registers
                    if panel.is_active and panel.is_lfp:
                        ##
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,panel.pipe,
                                           panel.transcoder, panel.target_id, self.inputfile,panel.is_lfp, enable=True) is False:
                            self.fail("HW_3D_LUT verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with Lace")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
