#################################################################################################
# @file         hw_3d_lut_with_hdr.py
# @brief        This is a custom script which can used to apply both SINGLE and CLONE display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of basic test function and the function  will perform below functionalities
#               1.To configure enable/disable 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               4.Verify the persistence after the HDR
# @author       Vimalesh D
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

    def setUp(self):
        super().setUp()
        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)

        ##
        # Check if there is at least one HDR Supported Panel requested as part of the command line
        if num_of_hdr_supported_panels == 0:
            logging.error("FAIL : At least one HDR supported panel required")
            self.fail()

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):

        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                              panel.pipe, panel.is_lfp, panel.transcoder, panel.display_and_adapterInfo, panel.target_id,
                                              configure_dpp_hw_lut=True) is False:
                        self.fail()

        # Verify if the Power Mode is in DC and switch to AC
        # This is to override the OS Policy to disable HDR
        # when running Windows HD Color content on battery Power for battery optimization
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()

        ##
        # Enable the HDR
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                ##
                # Verify the 3DLUT disabled
                if panel.is_active and panel.is_lfp:
                    ##
                    if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,panel.pipe,
                                       panel.transcoder, panel.target_id, self.inputfile,panel.is_lfp, enable=False) is False:
                        self.fail()

        ##
        # Disable the HDR
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)
        if num_of_hdr_supported_panels == 0:
            ##
            # verify 3dLUT enabled
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    ##
                    # Verify the registers
                    if panel.is_active and panel.is_lfp:
                        ##
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,panel.pipe,
                                           panel.transcoder, panel.target_id, self.inputfile,panel.is_lfp, enable=True) is False:
                            self.fail()

    ##
    # If the test enables HDR and fails in between, then HDR has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with HDR")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
