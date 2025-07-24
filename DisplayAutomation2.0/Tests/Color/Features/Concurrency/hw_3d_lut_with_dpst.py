from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.Concurrency.concurrency_utility import verify_dpst
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - Hw3DLut Concurrency test with DPST
class Hw3DLutBasicWithDPST(Hw3DLUTBase):

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self):

        # Verify if the Power Mode is in DC and switch to AC
        # DPST will enable in DC mode only
        if common_utility.apply_power_mode(display_power.PowerSource.DC) is False:
            self.fail()

        # Enable Hw3DLut feature in all supported panels and verify 3DLUT Enable
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                          panel.pipe, panel.is_lfp, panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                          configure_dpp_hw_lut=True) is False:
                    self.fail()

        ##
        # verify DPST - Expected: Enable
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if verify_dpst(adapter.gfx_index, adapter.platform, port, panel.pipe) is False:
                    self.fail("Fail: Verification of dpst failed on Adapter:{0} Pipe:{1} ".format(adapter.gfx_index,
                                                                                                  panel.pipe))

        # Disable Hw3DLut in all the panels and verify 3DLUT -Disable
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                          panel.pipe, panel.is_lfp, panel.transcoder,
                                          panel.display_and_adapterInfo, panel.target_id,
                                          configure_dpp_hw_lut=False) is False:
                    self.fail()
                # verify DPST - Expected: Enable
                if verify_dpst(adapter.gfx_index, adapter.platform, port, panel.pipe) is False:
                    self.fail("Fail: Verification of dpst failed on Adapter:{0} Pipe:{1} ".format(adapter.gfx_index,
                                                                                                  panel.pipe))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut with DPST")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)