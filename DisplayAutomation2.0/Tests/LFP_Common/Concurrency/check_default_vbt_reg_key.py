########################################################################################################################
# @file         check_default_vbt_reg_key.py
# @section      Tests
# @brief        Contains Default VBT check for DMRRS, DRRS, VRR feature and verification.
#
# @author       Nainesh Doriwala, Ashish Tripathi
########################################################################################################################
from Libs.Core.logger import gdhm, html
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.powercons import registry
from Tests.LFP_Common.Concurrency.concurrency_base import *
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import LrrVersion
from Tests.PowerCons.Functional.LRR.lrr import Method
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut, workload
from Tests.PowerCons.Modules.dut_context import RrSwitchingMethod
from Tests.VRR import vrr


##
# @brief        This class contains Default VBT check tests. This class inherits the  ConcurrencyBase class.
#               This class contains methods to check if Default feature enable in VBT and feature working as expected
class DefaultFeatureCheck(ConcurrencyBase):
    status = True

    feature_default_vbt = {
        "ADLP": {"VRR": True, "DMRRS": True, "DRRS": True},
        "DG2": {"VRR": True, "DMRRS": True, "DRRS": True},
        "MTL": {"VRR": True, "DMRRS": True, "DRRS": True},
        "TGL": {"VRR": True, "DMRRS": True, "DRRS": True}
    }

    feature_default_regkey = {
        "ADLP": {"VRR": True, "DMRRS": True, "DRRS": True, "LRR": True},
        "DG2": {"VRR": True, "DMRRS": True, "DRRS": True, "LRR": True},
        "MTL": {"VRR": True, "DMRRS": True, "DRRS": True, "LRR": True},
        "TGL": {"VRR": True, "DMRRS": True, "DRRS": True, "LRR": True}
    }

    ##
    # @brief        This class method is the entry point for any VRR VBT test cases. Helps to initialize some of
    #               the parameters required for VRR test execution with VBT.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DefaultFeatureCheck, cls).setUpClass()
        for gfx_index, adapter in dut.adapters.items():
            assert adapter.name in cls.feature_default_regkey.keys(), f"Test is not supported on {adapter.name}"
            assert adapter.name in cls.feature_default_vbt.keys(), f"Test is not supported on {adapter.name}"

    ##
    # @brief        Test function to check if VRR is working as expected with VBT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR", "DEFAULT_VBT_REGKEY"])
    # @endcond
    def t_11_vrr_vbt(self):
        logging.info('{:*^80}'.format('VRR Regkey Verification starts'))
        html.step_start("Verifying default behaviour of VRR", True)
        html.step_end()
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"VRR is not supported for {panel.port}. Verification is not needed")
                    continue
                if vrr.is_enable_in_vbt(adapter, panel) is not self.feature_default_vbt[adapter.name]["VRR"]:
                    logging.error(f"\tVRR is not enabled by default in VBT for {panel.port} on {adapter.name}")
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] VRR is not enabled by default in VBT")
                    status = False

                # read reg_key and check for default value.
                reg_key = registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE
                reg_value = registry.read(adapter.gfx_index, reg_key)
                if reg_value is None:
                    html.step_end()
                    self.fail(f"\tFAILED to read {reg_key}")

                is_disable = reg_value != registry.RegValues.ENABLE
                if self.feature_default_regkey[adapter.name]["VRR"] is is_disable:
                    logging.error(f"\tVRR is not enabled by default in regkey for {panel.port} on {adapter.name}")
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] VRR is not enabled by default in reg-key")
                    status = False

                if not status:
                    logging.error(f"\tDefault value of VRR feature not enable for {adapter.gfx_index}, {panel.port}")
                    html.step_end()
                    self.fail(f"Default value of VRR feature not enable for {panel.port} on {adapter.name}")
                logging.info(f"Default value of VRR feature enable for {adapter.gfx_index}, {panel.port}")

                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )
                if vrr.async_flips_present(etl_file) is False:
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] OS is NOT sending async flips")
                    html.step_end()
                    self.fail("OS is NOT sending async flips")

                if vrr.verify(adapter, panel, etl_file) is False:
                    logging.error("VRR verification fail with default VBT and regkey")
                    html.step_end()
                    self.fail("VRR verification fail with default VBT and feature")
                logging.info("VRR verification pass with default VBT and feature")
        logging.info('{:*^80}'.format('VRR Regkey Verification ends'))
        html.step_end()

    ##
    # @brief        This function verifies DMRRS Functionality with Default VBT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS", "DEFAULT_VBT_REGKEY"])
    # @endcond
    def t_12_dmrrs_vbt(self):
        logging.info('{:*^80}'.format('DMRRS Regkey Verification starts'))
        html.step_start("Verifying default behaviour of DMRRS", True)
        html.step_end()
        status = True
        media_fps = 24
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.drrs_caps.is_dmrrs_supported:
                    logging.info(f"DMRRS is not supported on {adapter.name}. Verification is not needed")
                    continue
                html.step_start(f"Verifying DMRRS for {panel.port}")
                if dmrrs.is_enabled_in_vbt(adapter, panel) is not self.feature_default_vbt[adapter.name]["DMRRS"]:
                    logging.error(f"\tDMRRS is not enabled by default in VBT for {panel.port} on {adapter.name}")
                    gdhm.report_driver_bug_pc(
                        f"[PowerCons][DMRRS] DMRRS is not enabled by default in VBT for {panel.port}"
                    )
                    status = False

                # default reg-key value check
                reg_key = registry.RegKeys.PC.FEATURE_CONTROL
                reg_value = registry.read(adapter.gfx_index, reg_key)
                if reg_value is None:
                    self.fail(f"\tFAILED to read {reg_key}")

                logging.info(f"DisplayPcFeatureControl reg-key value= {hex(reg_value)}")
                if panel.is_lfp:
                    is_disable = reg_value & registry.RegValues.DRRS.DMRRS_DISABLE_INTERNAL_PANEL_PC_FTR_CTL != 0
                    if self.feature_default_regkey[adapter.name]["DMRRS"] is is_disable:
                        logging.error(f"\tLFP DMRRS is not enabled by default in regkey "
                                      f"for {panel.port} on {adapter.name}")
                        gdhm.report_driver_bug_pc(
                            f"[PowerCons][DMRRS] LFP DMRRS is not enabled by default in reg-key for {panel.port}")
                        status = False
                else:
                    is_disable = reg_value & registry.RegValues.DRRS.DMRRS_DISABLE_EXTERNAL_PANEL_PC_FTR_CTL != 0
                    if self.feature_default_regkey[adapter.name]["DMRRS"] is is_disable:
                        logging.error(f"\tEFP DMRRS is not enabled by default in regkey "
                                      f"for {panel.port} on {adapter.name}")
                        gdhm.report_driver_bug_pc(
                            f"[PowerCons][DMRRS] EFP DMRRS is not enabled by default in reg-key for {panel.port}")
                        status = False

                if not status:
                    logging.error(f"DMRRS feature not enable by default either in VBT / regkey for {adapter.name}")
                    html.step_end()
                    self.fail(f"DMRRS feature not enable by default either in VBT / regkey for {adapter.name}")

                if panel.drrs_caps.is_dmrrs_supported is False:
                    logging.info(f"DMRRS is not supported for {panel.port}. Verification is not needed")
                    continue

                logging.info(f"DMRRS feature enable by default in VBT / regkey for {adapter.name}")
                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                if etl_file_path is None:
                    html.step_end()
                    self.fail("FAILED to run the workload")

                if dmrrs.verify(adapter, panel, etl_file_path, media_fps) is False:
                    html.step_end()
                    self.fail("FAIL: DMRRS is NOT functional")
                logging.info("PASS: DMRRS is functional")
            logging.info('{:*^80}'.format('DMRRS Regkey Verification ends'))
            html.step_end()

    ##
    # @brief        This function verifies DRRS Functionality with Default VBT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DRRS", "DEFAULT_VBT_REGKEY"])
    # @endcond
    def t_13_drrs_vbt(self):
        logging.info('{:*^80}'.format('DRRS Regkey Verification starts'))
        html.step_start("Verifying default behaviour of DRRS", True)
        html.step_end()
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False or not panel.drrs_caps.is_drrs_supported:
                    logging.info(f"DRRS is not supported on {adapter.name}. Verification is not needed")
                    continue
                html.step_start(f"Verifying DRRS for {panel.port}")
                if drrs.is_enable_in_vbt(adapter, panel) is not self.feature_default_vbt[adapter.name]["DRRS"]:
                    logging.error(f"\tDRRS is not enabled by default in VBT for {panel.port} on {adapter.name}")
                    gdhm.report_driver_bug_pc(
                        f"[PowerCons][DRRS] DRRS is NOT enabled by default in VBT for {panel.port}")
                    status = False

                # DRRS enable check need to update.
                feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
                is_disable = feature_test_control.dps_disable != 0
                if self.feature_default_regkey[adapter.name]["DRRS"] is is_disable:
                    logging.error(f"\tDRRS is not enabled by default in reg-key for {adapter.name}")
                    gdhm.report_driver_bug_pc("[PowerCons][DRRS] DRRS is not enabled by default in reg-key")
                    status = False
                if not status:
                    logging.error(f"DRRS feature not enable by default either in VBT / regkey for {adapter.gfx_index}")
                    html.step_end()
                    self.fail(f"DRRS feature not enable by default either in VBT / regkey for {adapter.gfx_index}")
                logging.info(f"PASS: DRRS feature enable by default in VBT / regkey for {adapter.gfx_index}")

                if panel.drrs_caps.is_drrs_supported is False:
                    logging.info(f"DRRS is not supported for {panel.port}. Verification is not needed")
                    continue

                if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
                    html.step_end()
                    self.fail("FAILED to switch PowerSource")

                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                if etl_file is None:
                    html.step_end()
                    self.fail("FAILED to run the workload")

                if (panel.lrr_caps.is_lrr_2_0_supported or panel.lrr_caps.is_lrr_2_5_supported) and (
                        psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2)):
                    rr_change_status = drrs.is_rr_changing(adapter, panel, etl_file)
                    logging.info("Checking for any RR change (Expectation: RR should not change)")
                    if rr_change_status:
                        gdhm.report_driver_bug_pc("[PowerCons][DRRS] IDLE DRRS is functional on LRR2/2.5 panel")
                        html.step_end()
                        self.fail("\tRefreshRate change is detected (Unexpected)")
                    if rr_change_status is None:
                        html.step_end()
                        self.fail("\tETL report generation FAILED")
                    logging.info("No RefreshRate change detected (Expected)")
                else:
                    if drrs.verify(adapter, panel, etl_file) is False:
                        gdhm.report_driver_bug_pc("[PowerCons][DRRS] IDLE DRRS is NOT functional")
                        self.fail("DRRS is NOT functional")
                    logging.info("DRRS is Functional")
            logging.info('{:*^80}'.format('DRRS Regkey Verification ends'))
            html.step_end()

    ##
    # @brief        This function verifies LRR Functionality with Default regkey
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LRR", "DEFAULT_VBT_REGKEY"])
    # @endcond
    def t_14_lrr_regkey(self):
        logging.info('{:*^80}'.format('LRR Regkey Verification starts'))
        html.step_start("Verifying default behaviour of LRR", True)
        polling_delay_in_seconds = 0.01
        status = True
        # Get LRR version supported by panel and populate RR switching method
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False or not panel.lrr_caps.is_lrr_supported:
                    logging.info(f"LRR is not supported for {panel.port}. Verification is not needed")
                    continue
                if panel.lrr_caps.is_lrr_1_0_supported:
                    self.rr_switching_method = RrSwitchingMethod.CLOCK
                elif panel.lrr_caps.is_lrr_2_0_supported:
                    self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                elif panel.lrr_caps.is_lrr_2_5_supported:
                    if common.PLATFORM_NAME in common.PRE_GEN_14_PLATFORMS:
                        self.rr_switching_method = RrSwitchingMethod.VTOTAL_SW
                    else:
                        self.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                else:
                    self.rr_switching_method = RrSwitchingMethod.UNSUPPORTED

                lrr_regkey = registry.RegKeys.PSR.PSR2_DRRS_ENABLE
                is_lrr_disable = registry.read(adapter.gfx_index, lrr_regkey) != 1
                if self.feature_default_regkey[adapter.name]["LRR"] is is_lrr_disable:
                    logging.error(f"\tLRR is not enabled by default in reg-key for {adapter.name}")
                    gdhm.report_driver_bug_os("[OsFeatures][LRR] LRR is not enabled by default in reg-key")
                    status = False
                if not status:
                    html.step_end()
                    self.fail(f"FAIL: LRR is not enabled by default via regkey for {adapter.gfx_index}")
                logging.info(f"PASS: LRR is enabled by default via regkey for {adapter.gfx_index}")

                if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
                    html.step_end()
                    self.fail("FAILED to switch PowerSource")

                etl_file, polling_data = workload.run(workload.IDLE_DESKTOP, [30],
                                                      [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2),
                                                       polling_delay_in_seconds])

                if etl_file is None:
                    html.step_end()
                    self.fail("FAILED to run the workload")

                # Verify LRR behavior based on IDLE/Video Method
                lrr_verification_idle = lrr.verify(adapter, panel, etl_file, polling_data, Method.IDLE,
                                              self.rr_switching_method)
                if not lrr_verification_idle:
                    gdhm.report_driver_bug_os(f"[OsFeatures][LRR] Idle Desktop LRR is NOT functional")
                    self.fail(f"FAIL: LRR regkey Verification with Method= Idle failed")
                logging.info(f"PASS: LRR Basic Verification with Method= Idle")

                etl_file, polling_data = workload.run(workload.VIDEO_PLAYBACK_USING_FILE,
                    ['24.000.mp4', 30, False], [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2),
                                                polling_delay_in_seconds])

                if etl_file is None:
                    html.step_end()
                    self.fail("FAILED to run the workload")

                # Verify LRR behavior based on IDLE/Video Method
                lrr_verification_video = lrr.verify(adapter, panel, etl_file, polling_data, Method.VIDEO,
                                              self.rr_switching_method)

                if not lrr_verification_video:
                    gdhm.report_driver_bug_os(f"[OsFeatures][LRR] Video LRR is NOT functional")
                    self.fail(f"FAIL: LRR regkey Verification with Method= Video failed")
                logging.info(f"PASS: LRR Basic Verification with Method= Video")

            logging.info('{:*^80}'.format('LRR Regkey Verification ends'))
            html.step_end()


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DefaultFeatureCheck))
    TestEnvironment.cleanup(test_result)
