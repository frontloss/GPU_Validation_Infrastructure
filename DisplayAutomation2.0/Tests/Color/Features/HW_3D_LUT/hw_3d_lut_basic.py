#################################################################################################
# @file         hw_3d_lut_basic.py
# @brief        This is a custom script which can used to apply SINGLE/CLONE/EXTENDED display configurations
#               and apply a combination of all the bin files on displays connected.
#               This scripts comprises of basic test function and the function  will perform below functionalities
#               1.To configure enable/disable 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################

import sys
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - Hw3DLut basic test
class Hw3DLutBasic(Hw3DLUTBase):

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the  test step as the action type is not basic")
    def test_01_basic(self):

        # Enable Hw3DLut feature in all supported panels and verify.
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

        # Disable Hw3DLut in all the panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=False) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
                            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose To apply both SINGLE or CLONE display configuration and apply and verify 3dlut")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
