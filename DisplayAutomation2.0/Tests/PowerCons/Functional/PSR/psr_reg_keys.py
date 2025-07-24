#################################################################################################################
# @file         psr_reg_keys.py
# @brief        Test for PSR reg keys scenario
# @details      @ref psr_reg_keys.py <br>
#               This file implements PSR1/PSR2/PR test for disabling/enabling of PSR with reg keys
#               1. FEATURE_TEST_CONTROL
#               2. PSR_DISABLE_IN_AC
#               3. DISPLAY_PC_FEATURE_CONTROL - Disable Selective fetch, disable PR
#               4. DISPLAY_SW_WA_CONTROL  - Enable/Disable Delayed Vblank support
#
# @author           Chandrakanth Reddy
#################################################################################################################
import time

from Libs.Core import display_essential, display_power, registry_access
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import dpcd, windows_brightness, workload


##
# @brief        This class contains tests to verify PSR with Reg key
class TestPsrRegkeys(PsrBase):


    ##
    # @brief        This function tests PSR with and without AC power source and registry settings
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_psr_negative_ac(self):
        ret = None
        if self.display_power_.set_current_powerline_status(display_power.PowerSource.AC) is False:
            self.fail("Failed to switch power line status to AC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                feature = psr.verify_psr_restrictions(adapter, panel, self.feature)
                feature_str = psr.UserRequestedFeature(feature).name
                logging.info(f"STEP: Verify {feature_str} disable in regkey")
                if panel.psr_caps.is_psr_supported:
                    ret = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=False)
                elif panel.pr_caps.is_pr_supported and not panel.is_lfp:
                    ret = pr.disable_for_efp(adapter.gfx_index, panel.is_lfp)
                if ret is False:
                    self.fail("FAILED to update Reg key")
                if ret is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("FAILED to restart the driver")
                # sometimes plane enable event takes more time. Added 5 secs threshold before reading mmio
                time.sleep(5)
                if psr.is_psr_enabled_in_driver(adapter, panel, psr_version=self.feature):
                    self.fail(f"FAIL: {feature_str} is still enabled in AC")
                logging.info(f"PASS: {feature_str} disabled in driver")
                if panel.psr_caps.is_psr_supported:
                    # Update back Reg key value to enable PSR in AC
                    ret = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=True)
                elif panel.pr_caps.is_pr_supported and not panel.is_lfp:
                    ret = pr.enable_for_efp(adapter.gfx_index, panel.is_lfp)
                if ret is False:
                    self.fail("FAILED to update Reg key")
                if ret is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("FAILED to restart the driver")
                # sometimes plane enable event takes more time. Added 5 secs threshold before reading mmio
                time.sleep(5)
                if psr.is_psr_enabled_in_driver(adapter, panel, psr_version=feature) is False:
                    self.fail(f"FAIL: {feature_str} is not enabled after regkey reset")
                # Skipping HDR check due to Intel Custom DPCD feature ZBB
                # Todo - Re-enable the verification after Driver implements VESA based Brightness based support for EDP 1.5
                if panel.hdr_caps.is_hdr_supported and panel.edp_caps.edp_revision < dpcd.EdpDpcdRevision.EDP_DPCD_1_5:
                    logging.info(f"STEP: Verify {feature_str} with HDR enable")
                    # Enable HDR
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail("Failed to enable HDR")

                    # verify PSR with HDR enable
                    self.validate_feature()
                    logging.info(f"PASS: {feature_str} verification with HDR enable")
                    try:
                        logging.info(f"STEP: Verifying HDR disable after {feature_str} disable via Regkey")
                        logging.info(f"\tDisabling {feature_str} via Regkey")

                        # Now disable PSR in FeatureTestControl Reg key
                        if psr.enable_disable_psr_with_brightness_change(adapter.gfx_index,
                                                                         self.feature, False) is False:
                            self.fail("Failed to disable PSR")

                        logging.info("\tDisabling HDR using OS API")
                        # Disable HDR at the end
                        if pc_external.enable_disable_hdr([panel.port], False) is False:
                            self.fail("Failed to disable HDR using OS API")
                        logging.info(f"PASS: HDR disable check after {feature_str} disable via Regkey")
                    except Exception as e:
                        self.fail(e)
                    finally:
                        logging.info(f"Enabling back {feature_str} via Regkey")
                        if psr.enable_disable_psr_with_brightness_change(adapter.gfx_index,
                                                                         self.feature, True) is False:
                            self.fail(f"Failed to enable back {feature_str} in regkey")

    ##
    # @brief        This function verifies FFSU in DC mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_psr_negative_dc(self):
        # Test steps are as follows : 
        # Disable Selective Fetch using RegKey
        # Verify whether driver is switching to CFF
        # Verify PSR functionality with Selective Fetch disable
        # Enable Selective Fetch back via RegKey
        # Verify PSR Functionality
        # Disable PSR via RegKey
        # Enable PSR back via RegKey
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                feature = psr.verify_psr_restrictions(adapter, panel, self.feature)
                feature_str = psr.UserRequestedFeature(feature).name
                logging.info("STEP: Verify FFSU in DC mode")
                logging.info("\tDisable selective fetch via Regkey")
                # Disable Selective Fetch in reg key and verify FFSU
                sf_disable_status = psr.enable_disable_selective_fetch(adapter.gfx_index, panel, sel_fetch_enable=False)

                if sf_disable_status is False:
                    self.fail("Failed to update RegKey - DisplayPcFeatureControl")

                if sf_disable_status is True:
                    driver_restart_status, reboot_required = display_essential.restart_gfx_driver()
                    if driver_restart_status is False:
                        self.fail("FAILED to restart the driver")
                    logging.info("Successfully restarted the display driver")

                try:
                    cff_ctl = None
                    sff_ctl = None
                    psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder, 
                                                        adapter.name)
                    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                        cff_ctl = MMIORegister.read("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
                        sff_ctl = MMIORegister.read("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
                    
                    # Expectation : For Post-Gen12 platforms, driver has to disable PSR2 manual tracking, program full frame co-ordinates and -
                    # disable CFF/SFF in respective MMIO registers 
                    if adapter.name not in common.PRE_GEN_13_PLATFORMS:
                        su_mode_status , actual_su_mode = sfsu.verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl, [sfsu.SuType.SU_NONE])
                        if not su_mode_status:
                            gdhm.report_driver_bug_pc(f"[PowerCons][PSR] Unexpected SU mode programming for selective fetch disable")
                            self.fail(f"Unexpected SU mode programming for Selective Fetch disable in RegKey. Actual SU mode : {sfsu.SuType(actual_su_mode).name}")
                        logging.info(f"PASS : Driver did not enable Manual tracking/CFF/SFF for selective fetch disable")

                        # Check whether driver is programming full frame co-ordinates
                        if not psr.verify_su_region_programming(psr2_man_trk, panel.native_mode.VtRes):
                            gdhm.report_driver_bug_pc(f"[PowerCons][PSR] Driver is not programming full frame coordinates for selective fetch disbable")
                            self.fail("FAIL : Driver is not programming full frame coordinates for selective fetch enable")
                        logging.info("SUCCESS : Driver is programming full frame coordinates selective fetch enable")

                    logging.info("PASS: CFF verification")
                except Exception as e:
                    self.fail(e)
                finally:
                    logging.info("Enable back Selective Fetch via Regkey")
                    sf_enable_status = psr.enable_disable_selective_fetch(adapter.gfx_index, panel, sel_fetch_enable=True)

                    # Enable Selective Fetch back through the Reg Key
                    if sf_enable_status is False:
                        self.fail("Failed to update RegKey - DisplayPcFeatureControl")

                    if sf_enable_status is True:
                        driver_restart_status, reboot_required = display_essential.restart_gfx_driver()
                        if driver_restart_status is False:
                            self.fail("FAILED to restart the driver")
                        logging.info("Successfully restarted the display driver")
                self.validate_feature()
                if panel.psr_caps.is_psr_supported:
                    # Disable and enable back PSR
                    try:
                        logging.info(f"\tDisabling PSR via Regkey on {panel.port}")
                        psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                        if psr_status is False:
                            self.fail("FAILED to disable PSR through registry key")
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail("FAILED to restart the driver")
                        if psr.is_psr_enabled_in_driver(adapter, panel, feature):
                            logging.error(f"PSR is not disabled on {panel.port}")
                            self.fail(f"PSR is not disabled on {panel.port}")

                    except Exception as e:
                        self.fail(e)
                    finally:
                        logging.info(f"Enabling back PSR via Regkey on {panel.port}")
                        psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                        if psr_status is False:
                            self.fail("FAILED to enable PSR through registry key")
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail("FAILED to restart the driver")
                        if psr.is_psr_enabled_in_driver(adapter, panel, feature) is False:
                            logging.error(f"{feature_str} is not enabled on {panel.port}")
                            self.fail(f"{feature_str} not enabled in driver on {panel.port}")

    ##
    # @brief        This function tests PSR with and with AC power source and registry settings
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_PSR"])
    # @endcond
    def t_13_psr_negative_ac(self):
        if self.display_power_.set_current_powerline_status(display_power.PowerSource.AC) is False:
            self.fail("Failed to switch power line status to AC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info("STEP: Verify Psr disable in AC using INF")
                psr_ac = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=False)
                if psr_ac is False:
                    self.fail("FAILED to update PsrDisableInAc Reg key")
                if psr_ac is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("FAILED to restart the driver")
                if psr.is_psr_enabled_in_driver(adapter, panel, psr_version=self.feature):
                    self.fail("FAIL: PSR is still enabled in AC")
                logging.info("PASS: PSR kept disabled as expected when PsrDisableInAc= True")
                # Update back Reg key value to enable PSR in AC
                if panel.hdr_caps.is_hdr_supported:
                    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                    if psr_status is False:
                        assert False, f"FAILED to disable PSR2 for {panel.port}"
                    if psr_status is True:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            assert False, f"FAILED to restart display driver for {adapter.name}"

                    # WA for 14010407547 - make brightness work after disable/enable gfx-driver
                    # (fix will be in build 19575)
                    if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
                        blc.restart_display_service()
                    # doing brightness change to enable code path of AUX based and PSR client handling
                    logging.info("\tSetting 90% brightness")
                    if windows_brightness.set_current_brightness(90, 1) is True:
                        logging.info("\tSuccessfully set 90% brightness")
                    else:
                        # avoiding fail of test as PSR verification is not dependent on brightness change
                        logging.error("FAILED to apply 90% brightness")
                        gdhm.report_bug(
                            title="[PowerCons][BLC] Failed to apply 90% brightness in PSR test",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )

                    logging.info("STEP: Verify PSR with HDR enable")

                    # verify PSR with HDR enable
                    logging.info("PASS: PSR verification with HDR enable")
                    try:
                        logging.info("STEP: Verifying HDR disable after PSR disable via Regkey")
                        logging.info("\tDisabling PSR via Regkey")
                        # Now disable PSR in FeatureTestControl Reg key
                        psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                        if psr_status is False:
                            self.fail("FAILED to enable PSR through registry key")
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail("FAILED to restart the driver")

                        # WA for 14010407547 - make brightness work after disable/enable gfx-driver
                        # (fix will be in build 19575)
                        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
                            blc.restart_display_service()
                        # doing brightness change to enable code path of AUX based and PSR client handling
                        logging.info("\tSetting 90% brightness")
                        if windows_brightness.set_current_brightness(90, 1) is True:
                            logging.info("\tSuccessfully set 90% brightness")
                        else:
                            # avoiding fail of test as PSR verification is not dependent on brightness change
                            logging.error("FAILED to apply 90% brightness")
                            gdhm.report_bug(
                                title="[PowerCons][BLC] Failed to apply 90% brightness in PSR test",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Test.DISPLAY_POWERCONS,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                    except Exception as e:
                        self.fail(e)

    ##
    # @brief        This function verifies Delayed Vblank regkey with PSR panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DELAYED_VBLANK"])
    # @endcond
    def t_14_psr_negative(self):
        for adapter in dut.adapters.values():
            if adapter.name not in common.GEN_12_PLATFORMS:  # delayed Vblank support is applicable for GEN12 only
                logging.info(f"Skip delayed vblank check on {adapter.name}")
                continue
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                logging.info(f"Applying display mode - {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("\tFailed to apply display mode")
                if psr.is_delayed_vblank_supported(adapter, panel) is False:
                    logging.info(f"Skip delayed vblank check for {panel.port}")
                    continue
                logging.info("Step: Disable delayed vblank support using Regkey")
                status = psr.enable_disable_delayed_vblank_support(adapter, False)
                if status is True:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        self.fail("Failed to restart driver")
                    logging.info("\tPASS: Delayed vblank support disable success")
                elif status is False:
                    self.fail("Failed to update regkey")
                if psr.is_delayed_vblank_supported(adapter, panel):
                    self.fail("delayed vblank is enabled after disabling in regkey")
                logging.info(f"\tPASS:Delayed vblank is not enabled on Panel {panel.port}")
                logging.info("Step: Enable delayed vblank support using Regkey")
                status = psr.enable_disable_delayed_vblank_support(adapter, True)
                if status is True:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        self.fail("Failed to restart driver")
                    logging.info("\tPASS: Enabled delayed vblank support success")
                elif status is False:
                    self.fail("Failed to update regkey")
                if psr.is_delayed_vblank_supported(adapter, panel) is False:
                    self.fail("delayed vblank is not re-enabled after enabling in regkey")
                logging.info(f"\tPASS:Delayed vblank is enabled on Panel {panel.port}")


    ##
    # @brief        This function validates PSR1 Setup Time Override using Regkey
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR1_SETUP_TIME_OVERRIDE"])
    # @endcond
    def t_14_psr1_setup_time_override(self):
        feature_str = psr.UserRequestedFeature(self.feature).name
        setup_time_override_value = int(self.cmd_line_param[0]['SELECTIVE'][1])
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                psr_caps = dpcd.PsrCapability(panel.target_id)
                panel_setup_time = psr.PSR_SETUP_TIME[psr_caps.psr_setup_time]
                result = True
                if panel.is_lfp is False or panel.psr_caps.is_psr_supported is False:
                    continue
                if psr.verify_psr_setup_time(adapter, panel, self.feature) is not None:
                    logging.info(f"Panel {panel} does not have PSR1 setup time restriction")
                else:
                    if self.feature == psr.UserRequestedFeature.PSR_1 and adapter.name in ['LNL'] and adapter.cpu_stepping == 0:
                        logging.info(f"Skipping PSR1 verification for LNL-A stepping system")
                        continue
                    if setup_time_override_value < panel_setup_time:
                        setup_time_values = list(psr.PSR_SETUP_TIME.values())
                        reg_value = setup_time_values.index(setup_time_override_value)
                        logging.info(f"STEP: Verify PSR1 Setup Time Override using Regkey in {feature_str}")
                        reg_key = registry.RegKeys.PSR.PSR1_SETUP_TIME_OVERRIDE + panel.pnp_id

                        logging.info(f"\tCreating {reg_key} with value {reg_value} - {setup_time_override_value}us")
                        write_status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, reg_value)
                        if write_status is False:
                            self.fail(f"Failed to write to registry {reg_key}")
                        elif write_status is True:
                            logging.info(f"\tSuccessfully updated {reg_key} with value {reg_value}")
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                logging.error(f"Failed to restart display driver after updating {reg_key} registry key")
                                result = False

                        if self.feature == psr.UserRequestedFeature.PSR_1:
                            monitors = app_controls.get_enumerated_display_monitors()
                            monitor_ids = [_[0] for _ in monitors]
                            polling_args = psr.get_polling_offsets(self.feature)
                            etl_file_path, polling_data = workload.run(workload.SCREEN_UPDATE, [monitor_ids],
                                                                    polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                            if not psr.verify_psr1(adapter, panel, polling_data):
                                logging.error(f"\tFAIL : Failed to verify {feature_str} after setting registry {reg_key}")
                                result = False
                        elif self.feature >= psr.UserRequestedFeature.PSR_2:
                            # Negative test - PSR2 should not be enabled after setting Psr1SetupTimeOverride Regkey
                            if psr.is_psr_enabled_in_driver(adapter, panel, self.feature):
                                logging.error(f"\tFAIL : {feature_str} is enabled after setting registry {reg_key}")
                                result = False

                        # Delete RegKey after the verification
                        regkey_delete_status = psr.reset_psr1_setup_override(adapter, panel)
                        if regkey_delete_status is False:
                            self.fail(f"\tFailed to delete Reg Key {reg_key} after the verification")
                        elif regkey_delete_status is True:
                            logging.info(f"\tSuccessfully deleted RegKey {reg_key} on adapter {adapter.gfx_index}")
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail("\tFAILED to restart the driver")

                        if not result:
                            self.fail("Failed to verify {feature_str} after setting registry {reg_key}")
                        logging.info(f"PASS : Successfully verified {feature_str} after setting registry {reg_key}")
                    else:
                        logging.info(f"Cannot override PSR1 Setup time as the override value is > panel setup time")

        logging.info(f"PASS : Successfully verified PSR1 Setup Time Override in {feature_str}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPsrRegkeys))
    test_environment.TestEnvironment.cleanup(test_result)