#################################################################################################
# @file         lace_vbt.py
# @brief        Test calls for get and set lace functionality with vbt scenario
# @author       Vimalesh D
#################################################################################################
import sys
import logging
import unittest
from Libs.Core import registry_access, display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt import vbt
from Tests.Color.Common import color_escapes, common_utility, color_enums
from Tests.Color.Features.Lace.lace_base import *


##
# @brief - Lace basic test
class LaceVBT(LACEBase):
    ##
    # @brief test_01_lace_with_vbt function - Function to perform enable disable lace feature on display and
    #                                 perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "VBT",
                     "Skip the  test step as the action type is not basic")
    def test_01_lace_with_vbt(self):
        default_vbt_lace_status = 0
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        status = False
                        gfx_vbt = vbt.Vbt(adapter.gfx_index)

                        # Skip the panel if not LFP
                        if panel.is_lfp is False:
                            continue
                        panel_index = gfx_vbt.get_lfp_panel_type(port)
                        logging.debug(f"\tPanel Index for {port}= {panel_index}")
                        vbt_lace_support = (gfx_vbt.block_44.LaceEnable[0] & (1 << panel_index)) >> panel_index
                        vbt_lace_status = (gfx_vbt.block_44.LaceStatus[0] & (1 << panel_index)) >> panel_index
                        lace_aggressiveness_level = gfx_vbt.block_44.AggressivenessProfile[panel_index] & 0x0f
                        logging.info(vbt_lace_status)
                        logging.info(vbt_lace_support)

                        gfx_vbt = common_utility.disable_lace_in_vbt(gfx_vbt, panel_index, adapter.gfx_index)

                        vbt_lace_status = (gfx_vbt.block_44.LaceStatus[0] & (1 << panel_index)) >> panel_index
                        vbt_lace_support = (gfx_vbt.block_44.LaceEnable[0] & (1 << panel_index)) >> panel_index
                        if vbt_lace_status == 0 and vbt_lace_support == 0:
                            logging.info("Lace disabled in VBT")

                            if color_igcl_escapes.get_lace_config(0, panel.display_and_adapterInfo) is False:
                                if color_igcl_escapes.set_lace_config(2, 1, 90, panel.display_and_adapterInfo) is False:
                                    logging.info("PASS: Lace was not enabled")
                                else:
                                    status = False
                            else:
                                status = False
                        else:
                            logging.error("Lace not disabled in VBT")
                            status = False
                        if status == False:
                            gdhm.report_driver_bug_os("Failed to disable Lace in VBT" 
                                                        "on adapter : {0} platform : {1}"
                                                        .format(adapter.gfx_index, adapter.platform))
                            self.fail("Failed to disable and verify Lace in VBT")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info(
                                "Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                                    panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))
                        
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        # Restore back
                        gfx_vbt = vbt.Vbt(adapter.gfx_index)
                        panel_index = gfx_vbt.get_lfp_panel_type(port)
                        gfx_vbt = vbt.Vbt(adapter.gfx_index)
                        gfx_vbt = common_utility.enable_lace_in_vbt(gfx_vbt, panel_index, adapter.gfx_index)

                        vbt_lace_status = (gfx_vbt.block_44.LaceStatus[0] & (1 << panel_index)) >> panel_index
                        vbt_lace_support = (gfx_vbt.block_44.LaceEnable[0] & (1 << panel_index)) >> panel_index
                        if vbt_lace_status == 1 and vbt_lace_support == 1:
                            logging.info("Lace enabled in VBT")
                        else:
                            gdhm.report_driver_bug_os("Failed to restore Lace in VBT on adapter: {0} platform: {1} - "
                                                        "VBT_Lace_status: {2}, VBT_Lace_support: {3}"
                                                        .format(adapter.gfx_index,adapter.platform,
                                                                vbt_lace_status,vbt_lace_support))
                            self.fail("Failed to restore Lace in VBT")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enables and Disables lace on  panels and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
