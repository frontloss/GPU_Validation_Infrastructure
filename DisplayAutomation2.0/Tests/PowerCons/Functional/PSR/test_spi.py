#################################################################################################################
# @file         test_spi.py
# @brief        Contains Short Pulse Interrupt tests
#
# @author       Chandrakanth Reddy
#################################################################################################################
import logging

from Libs.Core import etl_parser
from Libs.Core.display_config import display_config_enums
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import common, dut, dpcd
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains tests to verify Spi
class SpiSimulate(PsrBase):
    display_config = DisplayConfiguration()
    spi_count = 1
    thread_list = []

    ##
    # @brief        This method is the exit point for SPI test cases. This resets the environment changes done
    #               for execution of SPI tests
    # @return       None
    @classmethod
    def tearDown(cls):
        if cls.thread_list:
            logging.info("Resetting the environment changes done for the execution of SPI tests")
            for t in cls.thread_list:
                t.join()

    ##
    # @brief        This function verifies PSR with SPI simulation
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_idle_state(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.pr_caps.is_pr_supported is False and (panel.psr_caps.is_psr_supported is False):
                    continue
                # Trigger SPI in IDLE Case
                time.sleep(3)
                if panel.psr_caps.is_psr_supported:
                    status = pc_external.update_panel_dpcd(adapter.gfx_index, panel.port,
                                                           dpcd.Offsets.PSR2_ERROR_STATUS, 0x1)
                elif panel.pr_caps.is_pr_supported:
                    status = pc_external.update_panel_dpcd(adapter.gfx_index, panel.port,
                                                           dpcd.Offsets.PANEL_REPLAY_ERROR_STATUS, 0x1)
                if status is False:
                    self.fail("DPCD update failed")

                logging.info("Triggering SPI in IDLE Case for {}".format(panel))
                # Start ETL Tracer if not started
                if etl_tracer.start_etl_tracer() is False:
                    self.fail("Failed to start etl trace")

                if pc_external.trigger_spi(adapter, panel, 1, self.spi_count) is False:
                    self.fail("SPI simulation Failed")

                time.sleep(2)

                status, etl_file_path = workload.etl_tracer_stop_existing_and_start_new('GfxTrace_SPI_Simulation_')
                if status is False:
                    self.fail('Failed to start new etl trace')

                if etl_parser.generate_report(etl_file_path) is False:
                    self.fail("Failed to generate EtlParser report")
                logging.info(f"Successfully generated report for ETL file : {etl_file_path}")

                self.verify_psr_pr_during_spi(adapter, panel)

                # reset the value at the end of verification
                if panel.psr_caps.is_psr_supported:
                    status = pc_external.update_panel_dpcd(adapter.gfx_index, panel.port,
                                                           dpcd.Offsets.PSR2_ERROR_STATUS, 0x0)
                elif panel.pr_caps.is_pr_supported:
                    status = pc_external.update_panel_dpcd(adapter.gfx_index, panel.port,
                                                           dpcd.Offsets.PANEL_REPLAY_ERROR_STATUS, 0x0)
                if status is False:
                    self.fail("DPCD reset failed")
                time.sleep(10)
                if panel.pr_caps.is_pr_supported is False:
                    # PSR will be enabled after next Vsync enable
                    logging.info(f"Verifying {self.feature_str} enable back after Vsync enable")
                    if psr.is_psr_enabled_in_driver(adapter, panel, self.feature) is False:
                        logging.error(f"{self.feature_str} not enabled back after SPI")
                        status &= False
        if status is False:
            self.fail("SPI verification failed")
        logging.info(f"SPI verification successful")

    ##
    # @brief        This function verifies PSR enable during mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_mode_set(self):
        status = True
        mode_list = []
        enumerated_displays = self.display_config.get_enumerated_display_info()
        # Trigger SPI during Mode set
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if len(panel.rr_list) > 1:
                    for rr in panel.rr_list:
                        mode_list.extend([common.get_display_mode(panel.target_id, rr, limit=1)])
                else:
                    mode_list = common.get_display_mode(panel.target_id, limit=2, scaling=True)
                if mode_list is not None:
                    mode = mode_list[0]
                    scaling = display_config_enums.Scaling(mode.scaling).name
                    logging.info(f"Applying display mode - {scaling} : {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config.set_display_mode([mode], enumerated_displays=enumerated_displays, force_modeset=True) is False:
                        self.fail("Failed to apply mode")
                    time.sleep(5)
                    status &= psr.is_psr_enabled_in_driver(adapter, panel, self.feature)
                    status &= psr.verify_sink_failures(panel, self.feature)
                    # apply default mode at end
                    mode = panel.native_mode
                    scaling = display_config_enums.Scaling(mode.scaling).name
                    logging.info(f"Applying default mode - {scaling} : {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config.set_display_mode([mode], enumerated_displays=enumerated_displays) is False:
                        self.fail(f"Failed to apply default mode")

        if status is False:
            self.fail(f"{self.feature_str} enable check after modeset failed")
        logging.info(f"{self.feature_str} verification successful")

    ##
    # @brief Verify PSR Disable and enable during SPI simulation
    # @param[in]    adapter Adapter object
    # @param[in]    panel Panel object
    # @return None
    def verify_psr_pr_during_spi(self, adapter, panel):
        feature_disabled = False
        aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]

        if psr.UserRequestedFeature.PSR_2 <= self.feature < psr.UserRequestedFeature.PANEL_REPLAY:
            psr2_ctl = MMIORegister.read("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
            if psr2_ctl.psr2_enable == 0:
                logging.error(f"PSR2 is not enabled after SPI on {panel.port}")
                self.fail("PSR2 not enabled after SPI")
            logging.info(f"PASS: PSR2 not enabled after SPI")
            psr_offset = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
            psr_data = etl_parser.get_mmio_data(psr_offset.offset, is_write=True)
            if psr_data is None:
                logging.error(f"Driver did not disable PSR during SPI")
                self.fail("No MMIO data for PSR2_CTL")
            for data in psr_data:
                if adapter.name in common.PRE_GEN_14_PLATFORMS:
                    psr_offset.asUint = data.Data
                else:
                    psr_offset.asUint = data.Data << 16
                if psr_offset.psr2_enable == 0:
                    feature_disabled = True
                    logging.info(f"PSR2 disabled during SPI")
                    break
        elif self.feature == psr.UserRequestedFeature.PSR_1:
            srd_ctl = MMIORegister.read("SRD_CTL_REGISTER", "SRD_CTL_" + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
            if srd_ctl.srd_enable == 0:
                logging.error(f"PSR1 is not enabled after SPI on {panel.port}")
                self.fail("PSR1 not enabled after SPI")
            logging.info(f"PASS: PSR1 enabled after SPI")
            psr_offset = MMIORegister.get_instance("SRD_CTL_REGISTER", "SRD_CTL_" + panel.transcoder, adapter.name)
            psr_data = etl_parser.get_mmio_data(psr_offset.offset, is_write=True)
            if psr_data is None:
                logging.error(f"Driver did not disable PSR during SPI")
                self.fail("No MMIO data for PSR1")
            for data in psr_data:
                psr_offset.asUint = data.Data
                if psr_offset.srd_enable == 0:
                    feature_disabled = True
                    logging.info(f"PSR2 disabled during SPI")
                    break
        else:
            pr_ctl = MMIORegister.read("TRANS_DP2_CTL_REGISTER", "TRANS_DP2_CTL_" + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
            # PR needs link training to enable back after SPI
            if pr_ctl.pr_enable:
                logging.error(f"PR is not disabled after SPI on {panel.port}")
                self.fail("PR not disabled after SPI")
            feature_disabled = True
            logging.info(f"PASS: PR disabled after SPI")
        if feature_disabled is False:
            logging.error(f"{self.feature_str} not disabled during SPI")
            self.fail("Feature not disabled during SPI")
        logging.info("Checking whether driver has cleared all the sink errors in DPCD after SPI")
        dpcd_offset = dpcd.Offsets.PANEL_REPLAY_ERROR_STATUS if self.feature == psr.UserRequestedFeature.PANEL_REPLAY \
            else dpcd.Offsets.PSR2_ERROR_STATUS
        psr_error_status_data = etl_parser.get_dpcd_data(dpcd_offset, channel=aux)
        expected_error_status_value = None
        actual_error_status_value = None
        for error_data in psr_error_status_data:
            # Driver is expected to program 1 to the respective sink failure bit to reset the sink failure during SPI
            # Compare the latest read and latest write data for Sink Device PSR Status Field(2006h) in DPCD -
            # to make sure driver is resetting all the sink failures during SPI
            logging.debug(f"\tDPCD data : {error_data}")
            if not error_data.IsWrite:
                expected_error_status_value = error_data.Data
            else:
                actual_error_status_value = error_data.Data

        if expected_error_status_value != actual_error_status_value:
            gdhm.report_driver_bug_pc("[Powercons] [PSR_PR] Driver did not clear Sink Errors after SPI")
            self.fail("FAIL: Driver did not clear Sink Error(s) after SPI")
        logging.info("PASS: Driver has successfully cleared all the sink errors after SPI")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(SpiSimulate))
    test_environment.TestEnvironment.cleanup(test_result)
