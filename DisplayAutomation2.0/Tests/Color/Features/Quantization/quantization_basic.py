#################################################################################################
# @file         quantization_test_basic.py
# @brief        This scripts comprises of basic quantization test will perform below functionalities
#               1.test_01_basic() - Will apply the mode and bpc will be set based on commandline
#               and  perform register verification for OCSC,Coeff,Pre/post off and quantization range
# @author       Vimalesh D
#################################################################################################
import random

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.test_base import *
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Features.Quantization.quantization_test_base import *
from Tests.Color.Verification import feature_basic_verify


##
# @brief - Quantisation basic test
class QuantizationTestBasic(QuantizationTestBase):
    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the  test step as the action type is not basic")
    def test_01_basic(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Check virtual display incase single display hotplug-unplug scenario
                if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                    if self.bpc in [10, 12]:
                        bpc = "BPC12" if self.bpc == 12 else "BPC10"
                        # Update panel default color depth and color format
                        if color_escapes.set_bpc_encoding(panel.display_and_adapterInfo, bpc, "RGB",
                                                          GfxDriverType.YANGRA, panel.is_lfp) is False:
                            self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.target_id}")
                        if feature_basic_verify.verify_transcoder_bpc(adapter.gfx_index, adapter.platform,
                                                                      panel.transcoder, self.bpc) is False:
                            self.fail("Fail: Register verification for transcoder BPC failed")
                        logging.info("Pass: Register verification for BPC")
                    mode_list = get_modelist_subset(panel.display_and_adapterInfo.TargetID, 2, enum.MDS)
                    for mode in mode_list:
                        if not apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                          mode.scaling):
                            self.fail("Failed to apply display mode {0} X {1} @ {2} Scaling : {3}"
                                      .format(mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling))
                        self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform,
                                               panel.pipe, str(1), panel.transcoder, panel.connector_port_type,
                                               configure_avi=True)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the quantization range and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
