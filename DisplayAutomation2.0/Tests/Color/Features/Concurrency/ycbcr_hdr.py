#################################################################################################
# @file         ycbcr_hdr.py
# @brief        This scripts comprises of basic ycbcr test will perform below functionalities
#               1.Will perform basic() - Will perform the verify for basic enable and disable feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
# @author       Vimalesh D
#################################################################################################
import sys
import time

from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import color_properties
from Tests.Color.Common.color_properties import FeatureCaps
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.YCbCr.ycbcr_test_base import *


##
# @brief - Ycbcr basic test
class YcbcrBasic(YcbcrBase):

    def setUp(self):
        super().setUp()

        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)

        ##
        # Check if there is at least one HDR Supported Panel requested as part of the command line
        if num_of_hdr_supported_panels == 0:
            logging.error("FAIL : At least one HDR supported panel required")
            self.fail()

    def runTest(self):

        # Enable YCbCr feature in all supported panels and verifies
        self.enable_and_verify()


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

        ##
        # verify YCbCr is disabled
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, False):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                            panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Fail: Register verification for YCbCr panel {0} on {1} passed ".format
                                  (panel.connector_port_type, adapter.gfx_index))

        ##
        # Disable the HDR
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        num_of_hdr_supported_panels = color_properties.update_feature_caps_in_context(self.context_args)
        if num_of_hdr_supported_panels == 0:
            ##
            # verify YCbCr is enabled
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                                 self.context_args.adapters[gfx_index].panels[port])
                    if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                                  panel.transcoder, self.sampling, True):
                            logging.info(
                                "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                panel.connector_port_type, adapter.gfx_index))
                        else:
                            self.fail("Fail: Register verification for YCbCr panel {0} on {1} passed ".format
                                      (panel.connector_port_type, adapter.gfx_index))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables YCbCr on supported panels and perform verification on all panels"
        " when YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
