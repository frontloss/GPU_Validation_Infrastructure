#######################################################################################################################
# @file         test_dsc_bpc.py
# @brief        Test to check VDSC programming with VDSC display by varying the BPC using the Reg Key
# @details      Test Scenario:
#               1. Plugs the VDSC panel and applies SINGLE display config
#               2. Gets the supported BPC list based on the platform.
#               3. Iterates through each of the BPC, sets it in the Registry, Verifies the set bpc in transcoder.
#               4. Verifies the VDSC programming for the plugged display.
#               This test can be planned only with DP VDSC displays Only one display should be planned.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import unittest

from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDSCBitsPerComponent(VdscBase):

    ##
    # @brief        This test method verifies dsc programming of the VDSC display by setting all possible BPC for a
    #               given platform.
    # @return       None
    def t_11_bpc(self) -> None:

        # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed
        [(gfx_index, port)] = VdscBase.vdsc_panels[0].items()
        is_success = VdscBase._display_config.set_display_configuration_ex(self.topology, [port])
        self.assertTrue(is_success, "Failed to apply display configuration")

        # Get Supported BPC For Current Platform
        bpc_list = DSCHelper.get_supported_bpc_list(gfx_index)

        # Iterate Through Each BPC, Set BPC in the Registry, Verify Source BPC, and DSC Programming.
        for bpc in bpc_list:
            logging.info("Checking DSC Programming with {} BPC".format(bpc))
            is_success = DSCHelper.set_bpc_in_registry(gfx_index, bpc)
            self.assertTrue(is_success, "Setting Source BPC Failed.")

            set_bpc = DSCHelper.get_bpc_from_registry(gfx_index)
            self.assertTrue(set_bpc == bpc, "Written BPC in Registry is Not Same as Read BPC")

            transcoder_bpc = DSCHelper.get_source_bpc(gfx_index, port)
            self.assertTrue(set_bpc == transcoder_bpc, "Transcoder BPC Differs From BPC Value in Registry")

            is_success = dsc_verifier.verify_dsc_programming(gfx_index, port)
            self.assertTrue(is_success, "DSC Verification Failed For {} BPC at {} on {}".format(bpc, port, gfx_index))

            logging.info("DSC Verification Successful For {} BPC at {} on {}".format(bpc, port, gfx_index))

    ##
    # @brief        This static method restores the value of BPC registry to the default value
    # @return       None
    def t_12_disable_bpc(self) -> None:

        for gfx_index in VdscBase.cmd_line_adapters.keys():
            # For each adapter restore the BPC registry value to default
            is_success = DSCHelper.enable_disable_bpc_registry(gfx_index=gfx_index, enable_bpc=0)
            self.assertTrue(is_success, "Failed to disable SELECT_BPC Registry")

            logging.info("Disabling SELECT_BPC is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDSCBitsPerComponent))
    test_environment.TestEnvironment.cleanup(test_result)
