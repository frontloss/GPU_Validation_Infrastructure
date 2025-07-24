########################################################################################################################
# @file         dpst_concurrency.py
# @brief        Test for DPST/OPST with concurrent features
#
# @author       Ashish Tripathi
########################################################################################################################
import random
import time
from operator import attrgetter

from Libs.Core.wrapper import control_api_args
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.context import GfxDriverType
from Libs.Core.display_config import display_config
from Libs.Core import enum, registry_access
from Libs.Feature.powercons import registry

from Tests.Color.Common import color_escapes
from Tests.Color.Features.OverrideBpcEncoding import override_bpc_encoding
from Tests.PowerCons.Functional.DPST.dpst_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Functional.pc_external import enable_disable_lace
from Tests.PowerCons.Modules import workload
from Libs.Core.wrapper import control_api_wrapper


##
# @brief        This class contains basic test cases for DPST/OPST
class DpstBasic(DpstBase):
    ##
    # @brief        This function verifies DPST/OPST with VDSC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC"])
    # @endcond
    def t_11_dpst_vdsc(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.vdsc_caps.is_vdsc_supported is False:
                    self.fail("VDSC panel is not connected (Planning Issue)")
                if panel.psr_caps.is_psr2_supported:
                    if common.PLATFORM_NAME in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                        logging.info("PSR2 needs to be disabled to enable VDSC")
                        psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                        if psr_status is False:
                            self.fail(f"FAILED to disable PSR2 for {panel.port}")
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail(f"FAILED to restart display driver for {adapter.name}")
                        break   # INF is common for all panels in an adapter

        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(
            etl_file, self.workload_method, workload.PowerSource.DC_MODE, concurrent_feature=dpst.Feature.VDSC)
        if test_status is False:
            self.fail("FAIL: {0} feature verification with VDSC".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with VDSC".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with LACE
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LACE"])
    # @endcond
    def t_12_dpst_lace(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if adapter.name in ['TGL', 'DG1', 'DG2'] and panel.pipe == 'B':
                    logging.warning(f"LACE is not supported on PIPE {panel.pipe} on {panel.port}")
                    continue
                status, _ = enable_disable_lace(adapter, panel, True, adapter.gfx_index)
                if status is False:
                    self.fail(f"FAILED to enable LACE on {panel.pipe}")

        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE,
                                         concurrent_feature=dpst.Feature.LACE, expect_sfsu_enable=False)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if adapter.name in ['TGL', 'DG1', 'DG2'] and panel.pipe == 'B':
                    logging.warning(f"LACE is not supported on PIPE {panel.pipe} on {panel.port}")
                    continue
                status, _ = enable_disable_lace(adapter, panel, False, adapter.gfx_index)
                if status is False:
                    self.fail(f"FAILED to disable LACE on {panel.pipe}")
        if test_status is False:
            self.fail("FAIL: {0} feature verification with LACE".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with LACE".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with 3D LUT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["3D_LUT"])
    # @endcond
    def t_13_dpst_3d_lut(self):
        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(
            etl_file, self.workload_method, workload.PowerSource.DC_MODE, concurrent_feature=dpst.Feature._3DLUT)
        if test_status is False:
            self.fail("FAIL: {0} feature verification with 3D LUT".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with 3D LUT".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with Pipe Scalar
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PIPE_SCALAR"])
    # @endcond
    def t_14_dpst_pipe_scalar(self):
        test_status = True
        display_config_ = display_config.DisplayConfiguration()
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                all_supported_modes = display_config_.get_all_supported_modes([panel.target_id])
                mode_with_mar = None
                for _, modes in all_supported_modes.items():
                    modes = sorted(modes, key=attrgetter('HzRes', 'refreshRate'))
                    for mode in modes:
                        if mode.scaling == enum.MAR:
                            mode_with_mar = mode
                            break

                if mode_with_mar is None:
                    logging.error(f"FAILED to get supported mode with MAR for {panel.port}")
                    test_status &= False
                    continue
                logging.info(f"Native mode with MAR for {panel.port}= {mode_with_mar.HzRes}x{mode_with_mar.VtRes}")
                test_status &= display_config_.set_display_mode([mode_with_mar], False)
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE,
                                                  concurrent_feature=dpst.Feature.PIPE_SCALAR, expect_sfsu_enable=False)
                test_status &= common.set_native_mode(panel)

        if test_status is False:
            self.fail("FAIL: {0} feature verification with PIPE SCALAR".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with PIPE SCALAR".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST by changing other feature registry key values. This test can extend
    #               and include other required reg keys
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["REG_KEY"])
    # @endcond
    def t_15_dpst_psr(self):
        test_status = True
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                # Disable complete PSR2 using PSR2Disable
                logging.info("Disabling PSR2 via reg key (PSR2Disable)")
                psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR2 for {panel.port}")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(
                    etl_file, self.workload_method, workload.PowerSource.DC_MODE, expect_sfsu_enable=False)

                # Re-enable complete PSR2 using PSR2Disable
                logging.info("Enabling PSR2 via reg key (PSR2Disable)")
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr_status is False:
                    self.fail("FAILED to enable PSR2 through registry key")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("FAILED to restart the driver")
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

                # Disable complete PSR using FeatureTestControl
                logging.info("Disabling complete PSR from FeatureTestControl")
                psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR for {panel.port}")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(
                    etl_file, self.workload_method, workload.PowerSource.DC_MODE, expect_sfsu_enable=False)

                # Re-enable complete PSR using FeatureTestControl
                logging.info("Enabling complete PSR from FeatureTestControl")
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status is False:
                    self.fail("FAILED to enable PSR through registry key")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("FAILED to restart the driver")
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

                # Disable PSR in AC mode using PsrDisableInAc. No impact to DPST and DPST_SF
                logging.info("Disabling complete PSR in AC mode via reg key (PsrDisableInAc)")
                psr_status = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=False)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR in AC mode for {panel.port}")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")

                # Do AC/ DC switch to get PSR code path enable not work in AC mode
                if workload.change_power_source(workload.PowerSource.AC_MODE) is False:
                    self.fail("FAILED to switch in AC mode")
                time.sleep(2)
                if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
                    self.fail("FAILED to switch in DC mode")

                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

                # Re-enable PSR in AC mode using PsrDisableInAc. No impact to DPST and DPST_SF
                logging.info("Enabling complete PSR in AC mode via reg key (PsrDisableInAc)")
                psr_status = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=True)
                if psr_status is False:
                    self.fail(f"FAILED to enable PSR in AC mode for {panel.port}")
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")
                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

        if test_status is False:
            self.fail("FAIL: {0} feature verification with different reg keys".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with different reg keys".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with AC and DC power source
    #               together with BPC and Encoding update.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["BPC"])
    # @endcond
    def t_16_dpst_bpc_with_ac_dc(self):
        power_source_list = [workload.PowerSource.AC_MODE, workload.PowerSource.DC_MODE]
        power_plan = self.display_power_.get_current_power_scheme()
        for power_source in power_source_list:
            # Apply Power Source AC/DC
            if workload.change_power_source(power_source) is False:
                self.fail("Failed to switch power source to AC/DC mode")

            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    # Set feature params after updating power source
                    # IGCL Escape for AC Mode can do get/set query(Expected), but DPST/OPST should not function.
                    # IGCL Escape for AC Mode by default for get query will return feature as enabled with respect to
                    # features like OPST/OPST set in VBT.
                    enable = True if power_source == power_source.DC_MODE else False
                    if dpst.set_xpst(panel, self.xpst_feature, enable, power_source, power_plan) is False:
                        self.fail(f"Failed to set status:{enable} for {self.xpst_feature_str}")

                    feature_params = dpst.get_status(panel.target_id, power_source, power_plan)
                    if feature_params is None:
                        self.fail("Fail: IGCL Get status failed for target_id:{0}".format(panel.target_id))
                    if (feature_params.is_dpst_supported is False and self.xpst_feature == dpst.XpstFeature.DPST) or (
                            feature_params.is_opst_supported is False and self.xpst_feature == dpst.XpstFeature.OPST):
                        self.fail(f"\tFail:{self.xpst_feature_str} is not supported for {panel.port}")

                    if power_source == power_source.AC_MODE:
                        if (feature_params.is_dpst_enabled is True and self.xpst_feature == dpst.XpstFeature.DPST) or (
                                feature_params.is_opst_enabled is True and self.xpst_feature == dpst.XpstFeature.OPST):
                            logging.error(f"\t\t{feature_params}")
                            self.fail(f"{self.xpst_feature} is enabled in AC Mode for {panel.port}")
                    elif power_source == power_source.DC_MODE:
                        if (feature_params.is_dpst_enabled is False and self.xpst_feature == dpst.XpstFeature.DPST) or (
                                feature_params.is_opst_enabled is False and self.xpst_feature == dpst.XpstFeature.OPST):
                            logging.error(f"\t\t{feature_params}")
                            self.fail(f"{self.xpst_feature} is not enabled in DC Mode for {panel.port}")

                    status, combo_bpc_encoding, default_bpc, default_encoding = color_escapes.get_bpc_encoding(
                        panel.target_id, GfxDriverType.YANGRA, dpst.Feature.NONE)
                    if status is False:
                        self.fail(f"Fail: Failed to get the override bpc and encoding for {panel.port}")

                    # Update panel default color depth and color format
                    bpc = str(default_bpc)
                    encoding = str(default_encoding)
                    status = color_escapes.set_bpc_encoding(panel.target_id, bpc, encoding, GfxDriverType.YANGRA,
                                                            True, dpst.Feature.NONE)
                    if status is False:
                        self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.port}")

                    status, combo_bpc_encoding, default_bpc, default_encoding = color_escapes.get_bpc_encoding(
                        panel.target_id, GfxDriverType.YANGRA, dpst.Feature.NONE)
                    if status is False:
                        self.fail(f"Fail: Failed to get the override bpc and encoding for {panel.port}")

                    # From bpc and encoding mask, pick random color depth and color format and set via IGCL
                    # Will ensure  DPST/OPST verified with different color format and color depth
                    random.shuffle(combo_bpc_encoding)
                    bpc = str(combo_bpc_encoding[0][0])
                    encoding = str(combo_bpc_encoding[0][1])
                    status = color_escapes.set_bpc_encoding(panel.target_id, bpc, encoding, GfxDriverType.YANGRA,
                                                            True, dpst.Feature.NONE)

                    # Wait for registers to take effect after setting the bpc and encoding as the modeset will happen
                    time.sleep(2)
                    if status is False:
                        self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.port}")
                    adapter_info = test_context.TestContext.get_gfx_adapter_details()[adapter.gfx_index]
                    platform_name = adapter_info.get_platform_info().PlatformName
                    if override_bpc_encoding.verify(adapter.gfx_index, platform_name, panel.pipe,
                                                    str(1), panel.transcoder_type.value, bpc, encoding) is False:
                        self.fail(f"Fail: Failed to verify override bpc and encoding for {panel.port}")
                    logging.info(f"Pass: Register verification for override BPC and Encoding for {panel.port}")

            etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
            if etl_file is False:
                self.fail("Failed to run the workload")
            if self.validate_xpst(etl_file, self.workload_method, power_source) is False:
                self.fail(f"FAIL: {self.xpst_feature_str} feature verification with {power_source.name} mode")
            logging.info(f"PASS: {self.xpst_feature_str} feature verification with {power_source.name} mode")

    ##
    # @brief        This function verifies DPST by toggling PSR using IGCL
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR_IGCL"])
    # @endcond
    def t_17_dpst_psr_igcl(self):
        test_status = True
        igcl_power_source = control_api_args.ctl_power_source_v.DC.value
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
        # Disable complete PSR using IGCL
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info("Disabling PSR using IGCL")
                psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=False, pwr_src=igcl_power_source,
                                                             power_plan=igcl_power_plan)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR using IGCL")
                # break the loop because IGCL will do for all the displays
                break

        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE,
                                          expect_sfsu_enable=False, is_psr_enabled_in_igcl=False)

        # Enable complete PSR using IGCL
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info("Enabling PSR using IGCL")
                psr_status = psr.enable_disable_psr_via_igcl(panel, enable_psr=True, pwr_src=igcl_power_source,
                                                             power_plan=igcl_power_plan)
                if psr_status is False:
                    self.fail(f"FAILED to enable PSR using IGCL")
                # break the loop because IGCL will do for all the displays
                break

        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

        if test_status is False:
            self.fail("FAIL: {0} feature verification with different reg keys".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with different reg keys".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST by toggling PSR using IGCL
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR_VBT"])
    # @endcond
    def t_18_dpst_psr_vbt(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                # Disable PSR in VBT
                if psr.update_vbt(adapter, panel, False) is False:
                    self.fail("Failed to disable PSR in VBT")
                logging.info("Successfully disabled PSR in VBT")

                dut.refresh_panel_caps(adapter)
                dut.refresh_vbt_data(adapter)

                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(
                    etl_file, self.workload_method, workload.PowerSource.DC_MODE, expect_sfsu_enable=False)

                # Re-enable PSR in VBT
                if psr.update_vbt(adapter, panel, True) is False:
                    self.fail("Failed to enable PSR in VBT")
                logging.info("Successfully enabled PSR in VBT")

                dut.refresh_panel_caps(adapter)
                dut.refresh_vbt_data(adapter)

                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("FAILED to run the workload")
                test_status &= self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)

        message = f"{self.xpst_feature_str} feature verification with VBT settings"
        if test_status is False:
            self.fail(f"FAIL: {message}")
        logging.info(f"PASS: {message}")

    ##
    # @brief        This function verifies DPST/OPST with VDSC disable -> S4 -> VDSC enable
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC_DISABLE_S4_VDSC_ENABLE"])
    # @endcond
    def t_19_dpst_vdsc(self):
        test_status = self._vdsc_scenario_with_power_event(display_power.PowerEvent.S4)
        message = f"{self.xpst_feature_str} feature verification with VDSC disable -> S4 -> VDSC enable"
        if test_status is False:
            self.fail(f"FAIL: {message}")
        logging.info(f"PASS: {message}")

    ##
    # @brief        This function verifies DPST/OPST with VDSC disable -> CS -> VDSC enable
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC_DISABLE_CS_VDSC_ENABLE"])
    # @endcond
    def t_20_dpst_vdsc(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("Test needs CS supported system, but it is S3 supported (Planning Issue)")

        test_status = self._vdsc_scenario_with_power_event(display_power.PowerEvent.CS)
        message = f"{self.xpst_feature_str} feature verification with VDSC disable -> CS -> VDSC enable"
        if test_status is False:
            self.fail(f"FAIL: {message}")
        logging.info(f"PASS: {message}")

    def _vdsc_scenario_with_power_event(self, power_event):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.vdsc_caps.is_vdsc_supported is False:
                    self.fail("VDSC panel is not connected (Planning Issue)")

            # Disabled VDSC
            status = registry.write(adapter.gfx_index, "eDPCompressionDisable", registry_access.RegDataType.DWORD, 0x1)
            if status is False:
                self.fail("FAILED to disable VDSC (eDPCompressionDisable= 0x1)")
            if status is True:
                driver_status, reboot_required = display_essential.restart_gfx_driver()
                if driver_status is False:
                    self.fail("\tFailed to restart display driver after disabling VDSC")
            logging.info("Successfully disabled VDSC")

            # update context saying VDSC is not supported so required verification can be done in other API
            for panel in adapter.panels.values():
                panel.vdsc_caps.is_vdsc_supported = False

        # Scenario and verification with VDSC disabled
        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)
        if test_status is False:
            self.fail("FAIL: {0} feature verification with VDSC".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with VDSC".format(self.xpst_feature_str))

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail("FAILED to invoke PowerEvent (Test Issue)")
        logging.info(f"\tSuccessfully invoked from PowerEvent {power_event.name}")

        # Scenario and verification with VDSC disabled
        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(etl_file, self.workload_method, workload.PowerSource.DC_MODE)
        if test_status is False:
            self.fail("FAIL: {0} feature verification with VDSC".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with VDSC".format(self.xpst_feature_str))

        # Enabled VDSC
        for adapter in dut.adapters.values():
            status = registry.write(adapter.gfx_index, "eDPCompressionDisable", registry_access.RegDataType.DWORD, 0x0)
            if status is False:
                self.fail("FAILED to enable VDSC (eDPCompressionDisable= 0x0)")
            if status is True:
                driver_status, reboot_required = display_essential.restart_gfx_driver()
                if driver_status is False:
                    self.fail("\tFailed to restart display driver after disabling VDSC")
            logging.info("Successfully enabled VDSC")

            # update context saying VDSC is supported so required verification can be done in other API
            for panel in adapter.panels.values():
                panel.vdsc_caps.is_vdsc_supported = True

        # Scenario and verification with VDSC Enabled
        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")
        test_status = self.validate_xpst(
            etl_file, self.workload_method, workload.PowerSource.DC_MODE, concurrent_feature=dpst.Feature.VDSC)

        return test_status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstBasic))
    test_environment.TestEnvironment.cleanup(test_result)
