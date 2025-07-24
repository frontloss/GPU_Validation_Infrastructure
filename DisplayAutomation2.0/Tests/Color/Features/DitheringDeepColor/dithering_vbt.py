#################################################################################################
# @file         dithering_vbt.py
# @brief        Test verifies dithering with VBT config and Regkey settings.
# @author       Vimalesh D
#################################################################################################
import sys
import logging
import unittest
import random
from Libs.Core import registry_access, display_essential, display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt import vbt
from Tests.Color.Common import color_escapes, common_utility, color_enums
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Verification import feature_basic_verify
from Tests.test_base import TestBase


##
# @brief - Lace basic test
class DitheringVBT(TestBase):

    def setUp(self):
        self.custom_tags['-ENABLE_REGKEY_DITHERING'] = False
        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0]) > 1:
            self.enable_regkey_dithering = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0])
        else:
            self.enable_regkey_dithering = False
    ##
    # @brief test_01_lace_with_vbt function - Function to perform enable disable lace feature on display and
    #                                 perform register verification on all panels.
    # @param[in] self
    # @return None
    def runTest(self):
        default_vbt_lace_status = 0

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    power_source_list = [display_power.PowerSource.AC, display_power.PowerSource.DC]
                    scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]

                    ## Apply Power_Source AC and DC
                    for power_source in power_source_list:
                        status = common_utility.apply_power_mode(power_source)
                        if status is False:
                            self.fail()
                        gfx_vbt = vbt.Vbt(adapter.gfx_index)

                        # Skip the panel if not LFP
                        if panel.is_lfp is False:
                            continue

                        # Disable VBT-Dithering.
                        panel_index = gfx_vbt.get_lfp_panel_type(port)
                        logging.debug(f"\tPanel Index for {port}= {panel_index}")
                        panel_index = gfx_vbt.get_lfp_panel_type(port)
                        logging.debug(f"\tPanel Index for {port}= {panel_index}")
                        logging.info(gfx_vbt.block_42.GPUDitheringForBandingArtifacts)
                        logging.info((gfx_vbt.block_42.GPUDitheringForBandingArtifacts & (1 << panel_index)) >> panel_index)

                        gfx_vbt.block_42.GPUDitheringForBandingArtifacts &= ~(1 << panel_index)

                        if gfx_vbt.apply_changes() is False:
                            logging.error("VBT Failed")

                        status, reboot_required =  display_essential.restart_gfx_driver()
                        if status is False:
                            logging.error("VBT Failed")
                        gfx_vbt.reload(adapter.gfx_index)

                        logging.info((gfx_vbt.block_42.GPUDitheringForBandingArtifacts & (1 << panel_index)) >> panel_index)

                        # Enable Dithering by Regkey
                        for gfx_index, adapter in self.context_args.adapters.items():
                            reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

                            key_name = "ForceDitheringEnable"
                            value = 1
                            if registry_access.write(args=reg_args, reg_name=key_name,
                                                     reg_type=registry_access.RegDataType.DWORD,
                                                     reg_value=value) is False:
                                self.fail("Registry key add to enable SelectBPC  failed")
                            logging.info(" ForceDitheringEnable set to 1 on GFX_{0}".format(gfx_index))
                            ##
                            # restart display driver for regkey to take effect.
                            status, reboot_required = common_utility.restart_display_driver(gfx_index)
                            if status is False:
                                self.fail('Fail: Failed to Restart Display driver')

                        # Apply SDR Mode and verify dithering.
                        mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                        # Mode_list should not be None for mode switch scenario. hardcoded to enum.MDS
                        if mode_list is None:
                            mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                        for mode in mode_list:
                            apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                       mode.scaling)

                        if panel.is_lfp:
                            if feature_basic_verify.verify_dithering_feature(adapter.gfx_index, adapter.platform, panel.pipe, panel.transcoder,
                                                                             True) is False:
                                return False

                        # Enable VBT Dithering and verify Dithering
                        gfx_vbt.block_42.GPUDitheringForBandingArtifacts |= (1 << panel_index)
                        if gfx_vbt.apply_changes() is False:
                            logging.error("VBT Failed")

                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            logging.error("VBT Failed")
                        gfx_vbt.reload(adapter.gfx_index)

                        logging.info((gfx_vbt.block_42.GPUDitheringForBandingArtifacts & (1 << panel_index)) >> panel_index)

                        if panel.is_lfp:
                            if feature_basic_verify.verify_dithering_feature(adapter.gfx_index, adapter.platform, panel.pipe, panel.transcoder,
                                                                             True) is False:
                                return False

                        # Disable regkey based dithering
                        for gfx_index, adapter in self.context_args.adapters.items():
                            reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

                            key_name = "ForceDitheringEnable"
                            value = 0
                            if registry_access.write(args=reg_args, reg_name=key_name,
                                                     reg_type=registry_access.RegDataType.DWORD,
                                                     reg_value=value) is False:
                                self.fail("Registry key add to enable SelectBPC  failed")
                            logging.info(" ForceDitheringEnable set to 0 on GFX_{0}".format(gfx_index))
                            ##
                            # restart display driver for regkey to take effect.
                            status, reboot_required = common_utility.restart_display_driver(gfx_index)
                            if status is False:
                                self.fail('Fail: Failed to Restart Display driver')

                        if panel.is_lfp:
                            dithering_status = False
                            if power_source == display_power.PowerSource.DC:
                                dithering_status = True
                            if feature_basic_verify.verify_dithering_feature(adapter.gfx_index, adapter.platform, panel.pipe, panel.transcoder,
                                                                             dithering_status) is False:
                                return False

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test verifies dithering with VBT config and Regkey settings.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
