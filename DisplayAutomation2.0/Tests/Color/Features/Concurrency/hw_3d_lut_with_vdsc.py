#######################################################################################################################
# @file         hw_3d_lut_with_vdsc.py
# @brief        Test to check VDSC programming for the VDSC display when HW 3DLut is enabled
# @details      Test Scenario:
#               1. Plugs the VDSC displays, Applies config based on the config provided in the cmd.
#               2. Enable HW 3DLut and Verify HW 3DLut is enabled for each of the display
#               3. Verifies VDSC programming for all the VDSC display in the config.
#               4. Disable HW 3DLut and Verify HW 3DLut is disabled for all displays
#               This test can be planned with MIPI, EDP and DP VDSC displays
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import Hw3DLUTBase


class HW3DLutBasicWithVDSC(Hw3DLUTBase):

    def t_01_hw_3dlut_with_vdsc(self):

        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                port = panel.connector_port_type

                self.assertTrue(panel.is_active, f"Panel connected to {panel.connector_port_type} is in inactive state")

                # Check if the connected panel is a VDSC panel
                is_dsc_supported_panel = DSCHelper.is_vdsc_supported_in_panel(adapter.gfx_index, port)
                self.assertTrue(is_dsc_supported_panel, f"VDSC supported panel is not connected on port: {port}")

                # Enable HW3DLut feature
                is_enabled = self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                    panel.pipe, panel.is_lfp, panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                    configure_dpp_hw_lut=True)
                self.assertTrue(is_enabled, "Enabling HW 3DLUT Failed for {port} VDSC panel")

                is_success = dsc_verifier.verify_dsc_programming(adapter.gfx_index, port)
                self.assertTrue(is_success, f"VDSC Verification with HW 3DLUT Failed for {port} VDSC panel")
                logging.info(f"VDSC Verification with HW 3DLUT Successful for {port} VDSC panel")

        # Disable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():

                # Disable HW3DLut feature
                is_enabled = self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                    panel.pipe, panel.is_lfp, panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                    configure_dpp_hw_lut=False)
                self.assertTrue(is_enabled, "Disabling HW 3DLUT Failed for {port} VDSC panel")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To Verify VDSC when HW 3DLUT is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
