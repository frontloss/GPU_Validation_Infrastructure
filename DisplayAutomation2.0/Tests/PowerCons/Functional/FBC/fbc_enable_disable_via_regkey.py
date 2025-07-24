########################################################################################################################
# @file         fbc_enable_disable_via_regkey.py
# @brief        Test for FBC enable & disable sequence verification
#
# @author       Chandrakanth Reddy y
########################################################################################################################

import os
import time

from Libs.Core import etl_parser, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.FBC.fbc_base import *
from registers.mmioregister import MMIORegister

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.mmioData = 1

##
# @brief        This class contains FBC enable & disable sequence tests
class FbcEnableDisable(FbcBase):
    psr2_supported = False
    display_config = DisplayConfiguration()

    ##
    # @brief Unit-test setup function. 
    # @param[in] - void
    # @return - void 
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("Test Start")

    ##
    # @brief        Test to disable FBC on all adapters and verify FBC disable
    # @return       None
    def test_11_disable_fbc_on_all_adapters(self):
        for adapter in dut.adapters.values():
            is_reboot_required = False
            # Stop the ETL tracer started during TestEnvironment initialization
            status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeFbcDisable")
            if status is False:
                self.fail("Failed to stop ETL tracer")

            logging.info(f"Disabling FBC on Adapter {adapter.gfx_index}")
            fbc_disable_status = fbc.disable(adapter.gfx_index)
            if fbc_disable_status is False:
                self.fail(f"FAIL : FBC disable failed on {adapter.gfx_index}")
            if fbc_disable_status is True:
                driver_restart_status, is_reboot_required = display_essential.restart_gfx_driver()
                if driver_restart_status is False:
                    self.fail("Failed to restart graphics driver")

            status, etl_during_fbc_disable = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringFbcDisable")
            if status is False:
                self.fail("Failed to stop ETL tracer")

            data = {'adapter': adapter, 'check_fbc_enable': False, 'etl_file': etl_during_fbc_disable}
            # Reboot the system if required after driver restart
            if is_reboot_required:
                if reboot_helper.reboot(self, 'verify_fbc_enable_disable', data) is False:
                    self.fail("Failed to reboot the system")
            self.verify_fbc_enable_disable(data, reboot_happened=False)

    ##
    # @brief        API to enable FBC on all adapters and verify FBC enable
    # @return       None
    def test_12_enable_fbc_on_all_adapters(self):
        for adapter in dut.adapters.values():
            is_reboot_required = False
            # Stop the ETL tracer started during TestEnvironment initialization
            status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeFbcEnable")
            if status is False:
                self.fail("Failed to stop ETL tracer")

            logging.info(f"Enabling FBC on Adapter {adapter.gfx_index}")
            fbc_enable_status = fbc.enable(adapter.gfx_index)
            if fbc_enable_status is False:
                self.fail(f"FAIL : FBC enable failed on {adapter.gfx_index}")
            if fbc_enable_status is True:
                driver_restart_status, is_reboot_required = display_essential.restart_gfx_driver()
                if driver_restart_status is False:
                    self.fail("Failed to restart graphics driver")

            status, etl_during_fbc_enable = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringFbcEnable")
            if status is False:
                self.fail("Failed to stop ETL tracer")

            data = {'adapter': adapter, 'check_fbc_enable': True, 'etl_file': etl_during_fbc_enable }
            # Reboot the system if required after driver restart
            if is_reboot_required:
                if reboot_helper.reboot(self, 'verify_fbc_enable_disable', data) is False:
                    self.fail("Failed to reboot the system")
            self.verify_fbc_enable_disable(data, reboot_happened=False)

    ##
    # @brief        API to verify FBC on all adapters
    # @return       None
    def test_13_verify_fbc_on_all_adapters(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # SKIP FBC verification if PSR supported panel is connected.
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on {panel} on {adapter.name}")
                    continue

                # Check FBC status if PSR edp panel is connected
                # FBC + PSR1 is supported on MTL C0 stepping
                is_psr1_panel = panel.psr_caps.is_psr_supported and not panel.psr_caps.is_psr2_supported
                is_mtl_c0 = adapter.name in ['MTL'] and adapter.cpu_stepping >= 4
                sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
                is_fbc_psr1_possible = is_psr1_panel and (is_mtl_c0 or (adapter.name in ['MTL'] and sku_name in ['ARL']))
                if panel.is_lfp and panel.psr_caps.is_psr_supported and adapter.name in common.PRE_GEN_15_PLATFORMS and not is_fbc_psr1_possible:
                    if self.check_fbc_psr_concurrency(adapter, panel) is False:
                        gdhm.report_driver_bug_pc(f"[Powercons][FBC] FBC concurrency check with PSR is failed on Pipe-{panel.pipe}")
                        self.fail(f"FBC concurrency check with PSR is failed on Pipe-{panel.pipe}")
                    logging.info(f"Panel is PSR supported. Skipping FBC verification for the panel {panel} as it is PSR supported")
                    time.sleep(1)
                    continue
                
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringFbcVerification")
                if not status:
                    self.fail("Failed to get ETL Trace")
                logging.info("\tStart FBC Verification")
                if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                    self.fail("FAIL : FBC verification")
                logging.info("\tPASS : FBC verification")
    

    ##
    # @brief        API to verify FBC enable and FBC disable
    # @param[in]    data  Object
    # @param[in]    reboot_happened True if system reboot happened
    # @return       None
    def verify_fbc_enable_disable(self, data=None, reboot_happened=True):
        if reboot_happened and data is None:
            data = reboot_helper._get_reboot_data()
        adapter = data['adapter']
        check_fbc_enable = data['check_fbc_enable']
        file_name = data['etl_file']
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)

        for panel in adapter.panels.values():
            plane_ctl_reg = MMIORegister.get_instance('PLANE_CTL_REGISTER', 'PLANE_CTL_1_' + panel.pipe, adapter.name)
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                fbc_ctl_reg = MMIORegister.get_instance('FBC_CTL_REGISTER', 'FBC_CTL', adapter.name)
            else:
                fbc_ctl_reg = MMIORegister.get_instance('FBC_CTL_REGISTER', 'FBC_CTL_' + panel.pipe, adapter.name)

            # SKIP FBC verification if PSR supported panel is connected.
            if check_fbc_support(adapter, panel) is False:
                logging.info(f"SKIP: FBC is not supported on {panel} on {adapter.name}")
                continue

            # Check FBC status if PSR edp panel is connected
            # FBC + PSR1 is supported on MTL C0 stepping
            is_psr1_panel = panel.psr_caps.is_psr_supported and not panel.psr_caps.is_psr2_supported
            is_mtl_c0 = adapter.name in ['MTL'] and adapter.cpu_stepping >= 4
            sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
            is_fbc_psr1_possible = is_psr1_panel and (is_mtl_c0 or (adapter.name in ['MTL'] and sku_name in ['ARL']))
            if panel.pr_caps.is_pr_supported:
                logging.info(f"Skipping FBC sequence verification on {panel} due to single Plane usage")
                continue
            if panel.is_lfp:
                if panel.psr_caps.is_psr_supported and adapter.name in common.PRE_GEN_15_PLATFORMS and not is_fbc_psr1_possible:
                    if self.check_fbc_psr_concurrency(adapter, panel) is False:
                        gdhm.report_driver_bug_pc(f"[Powercons][FBC] FBC concurrency check with PSR is failed on Pipe-{panel.pipe}")
                        self.fail(f"FBC concurrency check with PSR is failed on Pipe-{panel.pipe}")
                    logging.info(f"Panel is PSR supported. Skipping FBC verification for the panel {panel} as it is PSR supported")
                    time.sleep(1)
                    continue
                # GEN15+: FBC with PSR2 can be enabled only with Multi-plane
                if panel.psr_caps.is_psr2_supported:
                    logging.info(f"Skipping FBC sequence verification on {panel} due to single Plane usage")
                    time.sleep(1)
                    continue

            fbc_enable_status = fbc.get_fbc_enable_status(adapter.gfx_index, panel.pipe)
            if check_fbc_enable:
                if fbc_enable_status is False:
                    gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC did not get enabled in driver")
                    self.fail(f"FAIL : FBC did not get enabled in driver on {adapter.gfx_index}")
                logging.info(f"PASS : FBC Enable Success on {adapter.gfx_index}")

                # Verify FBC Enable Sequence
                if verify_fbc_enable_sequence(adapter.name, panel.pipe, plane_ctl_reg, fbc_ctl_reg, etl_file_path) is False:
                    self.fail("FBC enable sequence verification Failed")
                logging.info("FBC Enable verification Successful")
            else:
                if fbc_enable_status is True:
                    gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC did not get disabled in driver")
                    self.fail(f"FAIL : FBC did not get disabled in driver on {adapter.gfx_index}")
                logging.info(f"PASS : FBC Disable Success on {adapter.gfx_index}")

                # Verify FBC Disable Sequence
                if verify_fbc_disable_sequence(adapter.name, plane_ctl_reg, fbc_ctl_reg, etl_file_path) is False:
                    self.fail("FBC disable sequence verification Failed")
                logging.info("FBC disable verification Successful")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Complete")


##
# @brief        API to verify FBC disable sequence
# @param[in]    adapter_name String
# @param[in]    plane_ctl_reg instance
# @param[in]    fbc_ctl_reg instance
# @param[in]    input_etl_file_path Input ETL file path
# @return       result, true, false
def verify_fbc_disable_sequence(adapter_name, plane_ctl_reg, fbc_ctl_reg, input_etl_file_path):
    # Before the last plane is disabled, FBC should be disabled first,
    #  wait for a VBlank, and plane 1A should be disabled only after that
    logging.info(f"\tGenerating EtlParser Report for {input_etl_file_path}")
    if etl_parser.generate_report(input_etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")
    plane_disable_time = fbc_disable_time = 0, 0

    fbc_ctl = etl_parser.get_mmio_data(fbc_ctl_reg.offset, is_write=True)
    if fbc_ctl is None:
        logging.error("FBC CTL Register data is Empty")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC CTL Register data is Empty")
        return False
    plane_ctl = etl_parser.get_mmio_data(plane_ctl_reg.offset, is_write=True)
    if plane_ctl is None:
        logging.error("Plane1A MMIO data is Empty")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] Plane1A MMIO data is Empty")
        return False

    for val in fbc_ctl:
        fbc_ctl_reg.asUint = val.Data
        if fbc_ctl_reg.enable_fbc:
            continue
        fbc_disable_time = val.TimeStamp
        logging.info(f"FBC is disabled at {val.TimeStamp}")
        break
    if fbc_disable_time == 0:
        logging.error('FBC is not disabled during driver disable')
        gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC is not disabled during driver disable")
        return False

    for plane in plane_ctl:
        plane_ctl_reg.asUint = plane.Data
        if plane_ctl_reg.plane_enable:
            continue
        plane_disable_time = plane.TimeStamp
        logging.info(f"Plane is disabled at {plane.TimeStamp}")
        break
    if plane_disable_time == 0:
        logging.error("Plane1A is not disabled during driver disable")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] Plane1A is not disabled during driver disable")
        return False
    # For Gen13+ FBC can be enabled before or after the plane. There is no required order for plane enabling and
    # disabling relative to FBC enabling and disabling, and FBC can be enabled for multiple frames
    # while plane is disabled.
    if adapter_name in common.PRE_GEN_13_PLATFORMS:
        if plane_disable_time > fbc_disable_time:
            logging.info("PASS : FBC Disabled before plane 1A disable")
            return True
        if plane_disable_time <= fbc_disable_time:
            logging.error("FAIL : PLANE 1A was disabled without waiting for VBI")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] PLANE 1A was disabled without waiting for VBI")
        return False

    return True


##
# @brief        API to verify FBC enable sequence
# @param[in]    adapter_name String
# @param[in]    pipe A/B
# @param[in]    plane_ctl_reg instance
# @param[in]    fbc_ctl_reg instance
# @param[in]    input_etl_file_path Input ETL file path
# @return       result, true, false
def verify_fbc_enable_sequence(adapter_name, pipe, plane_ctl_reg, fbc_ctl_reg, input_etl_file_path):
    logging.info(f"\tGenerating EtlParser Report for {input_etl_file_path}")
    if etl_parser.generate_report(input_etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")
    # After the first plane is enabled, we should wait for one VBlank
    # at least before enabling FBC.

    plane_enable_time = fbc_enable_time = 0, 0
    pg1_enable_time = 0
    fbc_wa_enable_time = 0
    fbc_chicken_wa_enable = False
    fbc_chicken, fbc_chicken_reg = None, None

    pwr_well_ctl_reg = MMIORegister.get_instance('PWR_WELL_CTL_REGISTER', 'PWR_WELL_CTL2', adapter_name)
    fbc_ctl = etl_parser.get_mmio_data(fbc_ctl_reg.offset, is_write=True)
    if fbc_ctl is None:
        logging.error("FBC CTL Register data is Empty")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC CTL Register data is Empty")
        return False
    plane_ctl = etl_parser.get_mmio_data(plane_ctl_reg.offset, is_write=True)
    if plane_ctl is None:
        logging.error("Plane1A MMIO data is Empty")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] Plane1A MMIO data is Empty")
        return False
    if adapter_name in common.PRE_GEN_15_PLATFORMS and adapter_name not in ['DG2', 'ELG']:
        fbc_chicken_reg = MMIORegister.get_instance('FBC_CHICKEN_REGISTER', 'FBC_CHICKEN_' + pipe, adapter_name)
        fbc_chicken = etl_parser.get_mmio_data(fbc_chicken_reg.offset, is_write=True)
        if fbc_chicken is None:
            logging.error("Fbc_chicken Register data is Empty")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] Fbc_chicken Register data is Empty")
            return False
        # HSD - 16015460418 : WA to fix panel flicker issue with specific desktop backgrounds
        # Driver will Set FBCChicken register bit 13 to TRUE to fix the issue.
        for val in fbc_chicken:
            fbc_chicken_reg.asUint = val.Data
            if fbc_chicken_reg.force_slb_invalidation:
                fbc_chicken_wa_enable = True
                break
        if fbc_chicken_wa_enable is False:
            logging.error(f"FBC Chicken BIT 13(force_slb_invalidation) is not enabled by driver")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC Chicken BIT 13(force_slb_invalidation) is not enabled by driver")
            return False
        logging.info(f"FBC Chicken BIT 13(force_slb_invalidation) enabled by driver")
    for val in fbc_ctl:
        fbc_ctl_reg.asUint = val.Data
        if fbc_ctl_reg.enable_fbc == 0:
            continue
        fbc_enable_time = val.TimeStamp
        logging.info(f"FBC is enabled at {val.TimeStamp}")
        break
    if fbc_enable_time == 0:
        logging.error("FBC is not enabled after driver enable")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC is not enabled after driver enable")
        return False

    for plane in plane_ctl:
        plane_ctl_reg.asUint = plane.Data
        if plane_ctl_reg.plane_enable == 0:
            continue
        plane_enable_time = plane.TimeStamp
        logging.info(f"Plane is enabled at {plane.TimeStamp}")
        break
    if plane_enable_time == 0:
        logging.error("Plane1A is not enabled after driver enable")
        gdhm.report_driver_bug_pc("[PowerCons][FBC] Plane1A is not enabled after driver enable")
        return False
    # For Gen13+ FBC can be enabled before or after the plane. There is no required order for plane enabling and
    # disabling relative to FBC enabling and disabling, and FBC can be enabled for multiple frames
    # while plane is disabled.
    if adapter_name in common.PRE_GEN_13_PLATFORMS:
        if fbc_enable_time > plane_enable_time:
            logging.info("PASS : FBC enabled after plane enable")
        elif fbc_enable_time < plane_enable_time:
            logging.error("FAIL : FBC enabled before plane enable")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC enabled before plane enable")
            return False
        # HSD - 22013320089 Verify FBC chicken bit WA enabled after PG1 Enable
        pwr_well_ctl = etl_parser.get_mmio_data(pwr_well_ctl_reg.offset, is_write=True)
        if pwr_well_ctl is None:
            logging.error("Power_well_Ctl2 Register data is Empty")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] Power_well_Ctl2 Register data is Empty")
            return False
        for val in pwr_well_ctl:
            pwr_well_ctl_reg.asUint = val.Data
            if pwr_well_ctl_reg.power_well_2_state == 1:
                pg1_enable_time = val.TimeStamp
                break
        for val in fbc_chicken:
            if (val.Data >> 14) & 1:
                fbc_wa_enable_time = val.TimeStamp
                break
        if pg1_enable_time > fbc_wa_enable_time:
            logging.error("FBC chicken Bit is programmed before the PG1 Enable")
            gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC chicken Bit is programmed before the PG1 Enable")
            return False
        logging.info("FBC chicken Bit is programmed after the PG1 Enable")
    return True
    

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('FbcEnableDisable'))
    TestEnvironment.cleanup(outcome)
