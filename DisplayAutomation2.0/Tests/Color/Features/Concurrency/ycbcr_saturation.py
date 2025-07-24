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
import unittest

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ApplyCSC.apply_csc_base import *



##
# @brief - Hw3DLut basic test
from Tests.Color.Features.YCbCr.ycbcr_test_base import YcbcrBase
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify


class ApplyYcbcrSaturation(ApplyCSCTestBase):

    def setUp(self):
        super().setUp()
        ##
        # On TGL, RCR: supports YCbCr+Saturation, hence if the command line arguments has
        # YCbCr+Saturation support as True,
        # test needs to set the registry key to enable YCbCr and Saturation together

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if not registry_access.write(args=reg_args, reg_name="SupportYCbCrAndSaturationEnable",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=1):
            logging.error("Registry key add to enable SupportYCbCrAndSaturationEnable failed")
            self.fail()
        else:
            logging.info("Registry key add to enable SupportYCbCrAndSaturationEnable SUCCESS")
            status, reboot_required = display_essential.restart_gfx_driver()


    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        if self.matrix_name:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active:
                        if color_escapes.ycbcr_support(panel.connector_port_type, panel.display_and_adapterInfo):
                            # Enable ycbcr
                            ycbcr_enable_status = color_escapes.configure_ycbcr(panel.connector_port_type, panel.display_and_adapterInfo, True)

                            # Apply saturation slider matrix
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo, port,True) is False:
                                self.fail()

    def tearDown(self):
        ##
        # Disabling SupportYCbCrAndSaturationEnable registry key if already enabled
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if not registry_access.write(args=reg_args, reg_name="SupportYCbCrAndSaturationEnable",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=0):
            logging.error("Registry key to disable SupportYCbCrAndSaturationEnable failed")
            self.fail()
        else:
            logging.info("Registry key to disable SupportYCbCrAndSaturationEnable SUCCESS")
            status, reboot_required = display_essential.restart_gfx_driver()
        super().tearDown()



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

