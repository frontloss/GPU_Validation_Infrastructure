#################################################################################################################
# @file         lrr_negative.py
# @brief        Contains LRR negative tests
#
# @author       Rohit Kumar
#################################################################################################################

from Libs.Core import etl_parser
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr


##
# @brief        This class contains negative tests to verify LRR
class LrrNegativeTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        LRR negative test with min RR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MIN_RR"])
    # @endcond
    def t_11_min_rr(self):

        for gfx_index, adapter in dut.adapters.items():
            hrr_status = hrr.disable(adapter)
            dut.refresh_panel_caps(adapter)
            if hrr_status is False:
                self.fail(f"FAILED to disable HRR on {adapter.name}")
            if hrr_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("Failed to restart display driver after reg-key update")

        monitor_ids = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                monitor_ids.append(panel.monitor_id)
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("Successfully applied display mode")
                html.step_end()

        etl_file, polling_data = workload.run(
            workload.SCREEN_UPDATE,
            [monitor_ids],
            [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
        )

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, RrSwitchingMethod.UNSUPPORTED, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR negative verification with min RR")
        logging.info("PASS: LRR negative verification with min RR")

        etl_file, polling_data = workload.run(
            workload.IDLE_DESKTOP,
            [self.duration_in_seconds],
            [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
        )

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, Method.IDLE, RrSwitchingMethod.UNSUPPORTED, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR negative verification with min RR")
        logging.info("PASS: LRR negative verification with min RR")

        etl_file, polling_data = workload.run(
            workload.VIDEO_PLAYBACK_USING_FILE,
            [self.video_file, self.duration_in_seconds, False],
            [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
        )

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, Method.VIDEO, RrSwitchingMethod.UNSUPPORTED, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR negative verification with min RR")
        logging.info("PASS: LRR negative verification with min RR")

    ##
    # @brief        This function resets RR to default high RR
    # @details      This function resets RR to default high RR as lrr_negative.py tests are not resetting to high RR
    # @return       None
    @classmethod
    def tearDownClass(cls):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if cls.display_config_.set_display_mode([mode], False) is False:
                    assert False, "FAILED to set display mode"
                logging.info("Successfully applied display mode")
                html.step_end()
        super(LrrNegativeTest, cls).tearDownClass()

    ##
    # @brief        LRR negative test to after set display mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["ASYNC"])
    # @endcond
    def t_12_async_flip(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("Successfully applied display mode")

        etl_file, _ = workload.run(
            workload.GAME_PLAYBACK,
            [workload.Apps.Classic3DCubeApp, self.duration_in_seconds, True]
        )

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.verify_link_m_with_vrr(adapter, panel, etl_file)

    ##
    # @brief        LRR negative test based on LinkM, VTotal values
    # @param[in]    adapter Adapter
    # @param[in]    panel Panel
    # @param[in]    etl_file String, path to ETL file
    # @return       None
    def verify_link_m_with_vrr(self, adapter, panel, etl_file):
        if etl_parser.generate_report(etl_file, vrr.ETL_PARSER_CONFIG) is False:
            self.fail("FAILED to generate ETL report")
        logging.info("Successfully generated ETL report")

        logging.info(f"Step: Verifying {self.feature.name} for {panel.port}")
        vrr_active_period = vrr.get_vrr_active_period(adapter, panel)

        if vrr_active_period is None:
            logging.warning("\tNo VRR active period found")
            return

        timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
        offset = timing_offsets.LinkM
        if self.feature in [LrrVersion.LRR2_5]:
            offset = timing_offsets.VTotal

        for vrr_active_start, vrr_active_end in vrr_active_period:
            mmio_data = etl_parser.get_mmio_data(offset, True, vrr_active_start, vrr_active_end)
            if mmio_data is None:
                if self.feature in [LrrVersion.LRR1_0]:
                    logging.info(
                        f"\tPASS: LinkM is not changing in VRR active period ({vrr_active_start}, {vrr_active_start})")
                elif self.feature in [LrrVersion.LRR2_5]:
                    logging.info(
                        f"\tPASS: VTotal is not changing in VRR active period ({vrr_active_start}, {vrr_active_end})")
                return

            current_value = mmio_data[0].Data
            for mmio in mmio_data:
                if mmio.Data != current_value:
                    if self.feature in [LrrVersion.LRR1_0]:
                        self.fail("LinkM is changing while VRR is active")
                    elif self.feature in [LrrVersion.LRR2_5]:
                        self.fail("VTotal is changing while VRR is active")

            if self.feature in [LrrVersion.LRR1_0]:
                logging.info(
                    f"\tPASS: LinkM is not changing in VRR active period ({vrr_active_start}, {vrr_active_end})")
            elif self.feature in [LrrVersion.LRR2_5]:
                logging.info(
                    f"\tPASS: VTotal is not changing in VRR active period ({vrr_active_start}, {vrr_active_end})")

    ##
    # @brief        LRR Negative test for registry keys
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["REG_KEY"])
    # @endcond
    def t_13_no_lrr(self):
        test_status = True
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

            logging.info(f"Disabling LRR via reg_key on {adapter.name}")
            lrr_status = lrr.disable(adapter)
            if lrr_status is False:
                self.fail("FAILED to disable via reg_key")
            if lrr_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"Successfully to restart display driver for {adapter.name}")

            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                if self.method == Method.IDLE:
                    etl_file, polling_data = workload.run(
                        workload.IDLE_DESKTOP,
                        [self.duration_in_seconds],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                else:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )

                status = True
                if lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method) is False:
                    if self.method == Method.IDLE and self.feature in [LrrVersion.LRR2_0, LrrVersion.LRR2_5]:
                        status &= False

                if status is True:
                    logging.info(f"{self.feature.name} Feature is NOT functional for {panel.port}")
                else:
                    test_status &= False
                    logging.error(f"{self.feature.name} Feature is functional for {panel.port}")

            logging.info(f"Enabling {self.feature.name} back on {adapter.name}")
            lrr_status = lrr.enable(adapter)
            if lrr_status is False:
                self.fail(f"FAILED to enable LRR{self.feature} via reg_key on {adapter.name}")
            if lrr_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"Successfully to restart display driver for {adapter.name}")

        if test_status is False:
            self.fail("FAIL: LRR Negative test verification with reg_keys")
        logging.info("PASS: LRR Negative test verification with reg_keys")

    ##
    # @brief        LRR Negative test for 314h source based VTotal DPCD value not present
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_SOURCE_BASED_VTOTAL_DPCD"])
    # @endcond
    def t_14_no_lrr_dpcd(self):
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

            for panel in adapter.panels.values():
                logging.info(f"\t{panel.lrr_caps}")
                if panel.is_lfp is False:
                    continue
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )

                if lrr.verify(adapter, panel, etl_file, polling_data, Method.VIDEO, RrSwitchingMethod.UNSUPPORTED) is False:
                    logging.error("FAIL: LRR Negative DPCD 314h test verification")
                    self.fail("FAIL: LRR Negative DPCD 314h test verification")
                logging.info("PASS: LRR Negative DPCD 314h test verification")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrNegativeTest))
    test_environment.TestEnvironment.cleanup(test_result)
