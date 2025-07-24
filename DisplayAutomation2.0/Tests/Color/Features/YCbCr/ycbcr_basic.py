#################################################################################################
# @file         ycbcr_basic.py
# @brief        This scripts comprises of basic ycbcr test will perform below functionalities
#               1.Will perform basic() - Will perform the verify for basic enable and disable feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
# @author       Vimalesh D
#################################################################################################
import sys
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.YCbCr.ycbcr_test_base import *

##
# @brief - Ycbcr basic test
class YcbcrBasic(YcbcrBase):

    ##
    # @brief test_01_basic function - Function to perform enable disable ycbcr feature on display and
    #                                 perform register verification on all ycbcr
    #                                 supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def test_01_basic(self):

        # Enable YCbCr feature in all supported panels and verifies
        self.enable_and_verify()

        # Disable YCbCr in all the panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    disable_status = enable_disable_ycbcr(panel.connector_port_type, panel.display_and_adapterInfo, False,
                                                          self.sampling)
                    if not disable_status:
                        self.fail("Failed to disable YCbCr")
                    else:
                        logging.info("Pass: Successfully disabled YCbCr")
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(panel.connector_port_type, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, False):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format
                            (panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format(panel.connector_port_type,adapter.gfx_index))

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables YCbCr on supported panels and perform verification on all panels"
        " when YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
