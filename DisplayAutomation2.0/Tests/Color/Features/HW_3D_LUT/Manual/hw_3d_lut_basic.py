#################################################################################################
# @file         hw_3d_lut_basic.py
# @brief        This is a custom script which can used to apply SINGLE/CLONE/EXTENDED display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of test_01_basic,  test_02_basic_stress and test_03_verify_3dlut, the function  will
#               perform below functionalities
#               1.To configure enable/disable 3dlut for Basic scenario for the display through command line
#               2.To configure enable/disable 3dlut for 5 iterations for Stress scenario
#               3.Verify the persistence of 3dlut after the event
# @author       Pooja A
#################################################################################################

import sys
import logging
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *
from Tests.Color.Features.HW_3D_LUT import hw_3dlut


##
# @brief - Hw3DLut basic test
class Hw3DLutBasic(Hw3DLUTBase):

    ##
    # @brief        Providing flexibility in command line to enable/disable HW3DLuT
    # @return       None
    def setUp(self):
        self.custom_tags["-STATUS"] = None
        self.custom_tags["-SCENARIO"] = "VERIFY"
        super().setUp()
        self.hw_3dlut_verify = hw_3dlut.verify
        self.status = str(self.context_args.test.cmd_params.test_custom_tags["-STATUS"][0])
        if self.status == 'ENABLE':
            self.status = True
        else:
            self.status = False

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the test step as the action type is not basic")
    def test_01_basic(self):

        # Enable/Disable Hw3DLut feature in all supported panels and verify through command line
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp, panel.transcoder,
                                                  panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=bool(self.status)) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, bool(self.status)) is False:
                            self.fail()
                            
    # # @brief        test_01_basic_stress() executes 5 iterations of enable/disable of hw3dlut and performing
    # register level verification @return       None
    @unittest.skipIf(get_action_type() != "STRESS", "Skip the test step as the action type is not stress")
    def test_02_basic_stress(self):

        # Enable/Disable Hw3DLut feature in all supported panels and verify
        for index in range(0, 5):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active:
                        # enabling hw3dlut in every iteration
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                      panel.pipe, panel.is_lfp, panel.transcoder,
                                                      panel.display_and_adapterInfo, panel.target_id,
                                                      configure_dpp_hw_lut=True) is False:
                                self.fail()
                        else:
                            if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                                self.fail()
                        import time
                        time.sleep(2)
                        # disabling hw3dlut in every iteration
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                      panel.pipe, panel.is_lfp, panel.transcoder,
                                                      panel.display_and_adapterInfo, panel.target_id,
                                                      configure_dpp_hw_lut=False) is False:
                                self.fail()
                        else:
                            if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
                                self.fail()

    ##
    # @brief        test_03_verify_3dlut() to verify persistence of hw3dlut across all supported panels
    # @return       None
    @unittest.skipIf(get_action_type() != "VERIFY", "Skip the test step as the action type is not verify")
    def test_03_verify_3dlut(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.pipe in self.three_dlut_enable_pipe:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        logging.info("Started 3DLUT verification for enabled pipe {0} available in the list".format(
                            panel.pipe))
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type, panel.pipe,
                                           panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                           bool(self.status), via_igcl=False) is False:
                            self.fail()
                    else:
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                           panel.pipe, panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                           bool(self.status), via_igcl=True) is False:
                            logging.error(
                                "Verification failed for 3DLUT support via IGCL after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                            self.fail()
                
                else:
                    logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                        panel.pipe))
    
    ##
    # @brief        Teardown to skip the base class teardown to avoid Lace Disable
    # @return       None
    def tearDown(self):
        logging.info("----3DLUT Manual Test Operation completed----")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose To apply both SINGLE or CLONE display configuration and apply and verify 3dlut")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
