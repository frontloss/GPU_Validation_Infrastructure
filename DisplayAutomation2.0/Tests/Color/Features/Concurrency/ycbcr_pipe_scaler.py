#################################################################################################
# @file         ycbce_scaler.py
# @brief        This scripts comprises of basic ycbcr test will perform below functionalities
#               1.Will perform basic() - Will perform the verify for basic enable and disable feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
# @author       Vimalesh D
#################################################################################################
import sys
import time

from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import color_properties
from Tests.Color.Common.color_properties import FeatureCaps
from Tests.Color.Features.Concurrency.concurrency_utility import verify_pipe_scaler
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.YCbCr.ycbcr_test_base import *


##
# @brief - Ycbcr basic test
class YcbcrPipeScaler(YcbcrBase):


    def runTest(self):

        # Enable YCbCr feature in all supported panels and verifies
        self.enable_and_verify()
        ##
        # verify pipe scaler enabled
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                if verify_pipe_scaler(adapter.gfx_index,adapter.platform,plane_id,panel.pipe) is False:
                    self.fail()
        ##
        # verify YCbCr is disabled
        # Disable YCbCr in all the panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    disable_status = enable_disable_ycbcr(panel.connector_port_type, panel.display_and_adapterInfo, False,
                                                          self.sampling)
                    if not disable_status:
                        self.fail("Fail: Failed to disable YCbCr")
                    else:
                        logging.info("Pass: Successfully disabled YCbCr")
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(panel.connector_port_type, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, False):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format
                            (panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Fail: Register verification for YCbCr panel {0} on {1} passed ".format(panel.connector_port_type,
                                                                                                          adapter.gfx_index))
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify_pipe_scaler(adapter.gfx_index,adapter.platform,plane_id,panel.pipe):
                        self.fail()



if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Configure YUV444/420 on HDMI/DP panels and verify pipe scaler enabled or disabled")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
