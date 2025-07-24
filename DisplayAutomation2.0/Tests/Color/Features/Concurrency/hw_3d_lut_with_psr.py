import sys
import time

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.Concurrency import concurrency_utility
from Tests.PowerCons.Functional.PSR import psr
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *
from Tests.PowerCons.Modules.dut_context import Adapter
from Tests.PowerCons.Functional.DCSTATES.dc_state import verify_dc5_dc6
from Libs.Core.logger import gdhm


##
# @brief - Hw3DLut basic test
class Hw3DLutBasicWithPSR(Hw3DLUTBase):
    feature = None

    def setUp(self):
        ##
        # Add a custom tag to parse the User requested PSR Feature
        self.custom_tags["-PSR_VERSION"] = ['PSR1', 'PSR2']
        super().setUp()
        self.feature = str(self.context_args.test.cmd_params.test_custom_tags["-PSR_VERSION"][0])

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        feature_enum = {"PSR1": 1, "PSR2": 2}
        ##
        # Check if at least one of the panels plugged as part of command line request support PSR
        logging.info("*** Step 1 : Check if at least one panel supports PSR ***")
        num_of_psr_panels = 0
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if psr.is_feature_supported_in_panel(panel.target_id, feature_enum[self.feature]):
                    logging.debug(
                        "{0} connected to Pipe {1} on Adapter {2} supports {3}".format(port, panel.pipe, gfx_index,
                                                                                       self.feature))
                    num_of_psr_panels = +1

            if num_of_psr_panels == 0:
                logging.error("FAIL : At least one panel should support PSR")
                gdhm.report_driver_bug_os("[{0}] At least one panel should support PSR for "
                                            "Adapter: {1} Pipe".format(adapter.platform,gfx_index))
                self.fail()

        is_psr2 = True if self.feature == psr.UserRequestedFeature.PSR_2 == 2 else False

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable Hw3DLut feature in all supported panels and verify
                if panel.is_lfp and panel.is_active:
                    if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                              panel.pipe, panel.is_lfp, panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                              configure_dpp_hw_lut=True) is False:
                        self.fail()

                    # DC 5/6 state verification with workload as APP
                    adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
                    adapter_info = adapter_info_dict[gfx_index.lower()]
                    temp = Adapter(gfx_index, adapter_info)
                    if verify_dc5_dc6(temp, method="APP"):
                        logging.info("DC5/6 verification is successful")
                    else:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with PSR")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
