#################################################################################################
# @file         hw_3d_lut_with_acm.py
# @brief        This is a custom script which can used to apply both SINGLE and CLONE display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of basic test function and the function  will perform below functionalities
#               1.To configure enable/disable 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               4.Verify the persistence after the ACM
# @author       Shivani Santoshi
#################################################################################################

import sys
import time

from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import color_properties
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *
from Tests.Color.Verification import feature_basic_verify


##
# @brief - Hw3DLut basic test
class Hw3DLutBasicWithHDR(Hw3DLUTBase):
    hdrtestbase = HDRTestBase()
    
    def setUp(self):
        self.custom_tags['-ENABLE_WCG'] = False
        super().setUp()
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_WCG"][0]) > 1:
            self.enable_wcg = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_WCG"][0])
        else:
            self.enable_wcg = False
    
    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        
        # Verify if the Power Mode is in DC and switch to AC
        # This is to override the OS Policy to disable HDR
        # when running Windows HD Color content on battery Power for battery optimization
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()
        
        self.hdrtestbase.enable_wcg = self.enable_wcg
        
        ##
        # Enable the ACM
        if self.hdrtestbase.toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()
        
        # Enable Hw3DLut feature in all supported panels and verify after enabling ACM
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                        self.fail()
        
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY":
                    logging.info(
                        "Verifying 3DLUT support via IGCL for panel connected to port {0} pipe {1} on adapter {2} after enbling ACM"
                        .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                    if panel.pipe in self.three_dlut_enable_pipe:
                        logging.info(
                            "Started 3DLUT verification for enabled pipe {0} available in the list".format(panel.pipe))
                        if not hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=True):
                            logging.error("Verification failed for 3DLUT support via IGCL for panel connected to "
                                          "port {0} pipe {1} on adapter {2} with ACM enabled"
                                          .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                            self.fail()
                    else:
                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list"
                                     .format(panel.pipe))
        
        ##
        # Disable the ACM
        if self.hdrtestbase.toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()
        
        ##
        # verify 3dLUT disabled
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type, panel.pipe,
                                       panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                       enable=False, via_igcl=True) is False:
                        self.fail()
    
    ##
    # If the test enables ACM and fails in between, then ACM has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if self.hdrtestbase.toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with ACM")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
