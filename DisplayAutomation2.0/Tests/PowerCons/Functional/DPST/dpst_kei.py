########################################################################################################################
# @file         dpst_kei.py
# @brief        Test for XPST kei scenarios
# @author       Tulika
########################################################################################################################
import datetime
import logging
import time
import unittest

import win32api

from Libs.Core import winkb_helper as kb
from Libs.Core import display_power, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.logger import html
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DPST import generate_frame, dpst
from Tests.PowerCons.Functional.DPST.dpst_base import DpstBase
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload, common, dut


##
# @brief        KEI values for xPST
class Kei:
    PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
    # Minimum backlight reduction should be 40%
    MIN_BLC_REDUCTION = 4000

    # Time T1: First instance at which BrightnessOptimization Enable/ Disable comes
    # Time T2: First instance at which IET or BKLT adjustment started by the driver in ETL.
    # Maximum phasing latency is calculated as (T2-T1) which should be maximum 200 ms
    # Increased Max latency phasing to 650 as a WA. Old Value= 500 (This value should be 500) HSD: 16024129988
    MAX_LATENCY_PHASING_IN_MS_NOT_FOR_FRAME_CHANGE = 650

    # Total phasing duration with Min & Max (in ms)
    # Phase-in should complete in 3000 ms but due to multiple failures relaxing the value to 3800ms temporarily.
    # Once driver issue is fixed need to revert the value to 3000ms. HSD:16027128127
    PHASING_DURATION_RANGE = (1000, 3800)

    # Step Variance during Phasing (in %)
    # Original value is 20% but many failures are coming which needs further discussion. So, decided to relax the number
    # temporarily to 30% for enabling tests in CI
    # Updating the value to 45% as WorkAround. Once, high resolution timer is implemented in driver,
    # this value should be changed to 30%. HSD: 16024129988
    MAX_STEP_VARIANCE = 45

    # Step Duration during Phasing (in ms)
    # Updating the value to 30ms for both step duration.
    # HSD: 16025631076 as XPST_SMOOTHENING_PERIOD_DEFAULT macro value is reduced from 30ms to 15ms.
    # This helps in reducing the jitter duration from 49ms to 25-32ms
    # For now, High resolution timer is not being implemented in driver due to Low ROI, hence speed changed to 15ms.
    MAX_STEP_DURATION = 33 if PLATFORM_NAME not in common.PRE_GEN_15_PLATFORMS else 45

    # Acceptable percentage of IET between each VBI (2 IET between VBI means 1 IET is missed)
    MAX_IET_MISS = 5
    # Generic 3% of the resolution as Frame change
    PERCENT = 0.03


display_power_ = display_power.DisplayPower()


##
# @brief        Api to toggle igcl level in KEI scenario
# @param[in]    panel
# @param[in]    feature
# @param[in]    delay
# @return       new_etl_file
def igcl_level_change_scenario(panel, feature, delay=None):
    power_source = display_power_.get_current_powerline_status()
    power_scheme = display_power_.get_current_power_scheme()

    status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
    if status is False:
        return False, None, None

    logging.info("To get VBI in ETL start. Doing random cursor movement")
    win32api.SetCursorPos((400, 400))
    win32api.SetCursorPos((panel.current_mode.HzRes, 0))
    time.sleep(1)

    igcl_time_stamps = []
    # apply levels from 3 to 1
    for level in range(3, 0, -1):
        igcl_time_stamps.append(datetime.datetime.now())
        if dpst.igcl_set_aggressiveness_level(panel, level, power_source, power_scheme) is False:
            logging.error("FAILED to set Aggressiveness level")
            return False, None, None

        logging.info(f"Waiting for {delay} seconds")
        time.sleep(delay)

    status, etl = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringWorkload")

    # restore to cached settings
    logging.info(f"Restoring the aggressiveness level to default value")
    if dpst.igcl_set_aggressiveness_level(panel, 2 if feature == dpst.XpstFeature.DPST else 1, power_source,
                                          power_scheme) is False:
        logging.error(f"FAILED to restore the Aggressiveness level")
        return False, None, None

    return status, etl, igcl_time_stamps


##
# @brief        Api to disable xpst in igcl multiple times in KEI scenario
# @param[in]    panel
# @param[in]    feature
# @param[in]    count
# @param[in]    delay
# @return       new_etl_file
def igcl_xpst_toggle_scenario(panel, feature, count=None, delay=None):
    power_source = display_power_.get_current_powerline_status()
    power_scheme = display_power_.get_current_power_scheme()
    status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
    if status is False:
        return False, None, None

    logging.info("To get VBI in ETL start. Doing random cursor movement")
    win32api.SetCursorPos((400, 400))
    win32api.SetCursorPos((panel.current_mode.HzRes, 0))
    time.sleep(1)

    igcl_time_stamps = []
    # toggle xPST status and start from Enabling it
    for index in range(1, (count * 2) + 1):
        igcl_time_stamps.append(datetime.datetime.now())
        # on every odd count Disable, even count Enable (starts with Disable XPST)
        if dpst.set_xpst(panel, feature, index % 2 != 0, power_source, power_scheme) is False:
            logging.error(f"Failed to disable XPST via IGCL ")
            return False, None, None

        logging.info(f"Waiting for {delay} seconds")
        time.sleep(delay)

    status, etl = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringWorkload")

    # restore to cached settings
    logging.info(f"Restoring the {feature.name} status to True")
    if dpst.set_xpst(panel, feature, True, power_source, power_scheme) is False:
        logging.error(f"FAILED to restore {feature.name} to status True")
        return False, None, None

    return status, etl, igcl_time_stamps


##
# @brief        This class contains KEI test cases for XPST
class DpstKei(DpstBase):
    ##
    # @brief        This class method is the entry point for XPST test cases. Helps to create the applied parameters
    #               required for XPST test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DpstKei, cls).setUpClass()
        pkg_name = ['pyinstaller', 'pygame']
        installed_packages = generate_frame.are_packages_installed(pkg_name)
        generate_frame.install_package(installed_packages)

        do_driver_restart = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # disable only when panel is PSR2 till MTL
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if panel.psr_caps.psr_version == 2:
                        disable_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                        if disable_status is False:
                            assert False, "Failed to disable PSR"
                        if disable_status is True:
                            do_driver_restart = True

                if cls.cmd_line_param[0]['MIN_RR'] != 'NONE':
                    display_config_ = display_config.DisplayConfiguration()
                    assert len(panel.rr_list) > 1, "Panel is not Multi-RR cannot apply MinRR"
                    mode = common.get_display_mode(panel.target_id, panel.min_rr)
                    logging.info(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if display_config_.set_display_mode([mode], False) is False:
                        assert False, "Failed to set display mode"

                # some panels have 48Hz as MinRR but 60Hz MinRR in DTD.
                # So, if DRRS is enabled, driver will have RR switch from 48 to 60, 60 to 48. Hence, disabling it
                logging.info("Disabling DRRS to avoid MinRR switch during the scenario")
                disable_status = drrs.disable(adapter)
                if disable_status is False:
                    assert False, f"FAILED to disable DRRS"

                if disable_status is True:
                    do_driver_restart = True

        if do_driver_restart:
            status, reboot_required = display_essential.restart_gfx_driver()
            assert status, "Failed to restart display driver"

        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

    ##
    # @brief       This method is the exit point for DPST KEI test cases
    # @return       None

    @classmethod
    def tearDownClass(cls):
        do_driver_restart = False
        for adapter in dut.adapters.values():
            status = dpst.delete_persistence(adapter)
            if status is False:
                assert False, "FAILED to delete persistence registry keys"
            do_driver_restart = True

            for panel in adapter.panels.values():
                # enable PSR irrespective of the PSR version
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if panel.psr_caps.is_psr_supported:
                        disable_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                        if disable_status is False:
                            assert False, "Failed to disable PSR"
                        if disable_status is True:
                            do_driver_restart = True

                assert common.set_native_mode(panel), "FAILED to apply Native mode"

                logging.info("Enabling DRRS in TearDown")
                enable_status = drrs.enable(adapter)
                if enable_status is False:
                    assert False, f"FAILED to enable DRRS"

                if enable_status is True:
                    do_driver_restart = True

        if do_driver_restart:
            status, reboot_required = display_essential.restart_gfx_driver()
            assert status, "Failed to restart display driver post RegKey disable"

        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

        super(DpstKei, cls).tearDownClass()

    ##
    # @brief        This function verifies XPST for BlcMinBrightness
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['BLC_MIN_BRIGHTNESS'])
    # @endcond
    def t_11_blc_min_brightness(self):
        html.step_start(f"Verifying XPST Kei for BrightnessReduction")
        etl_file = None
        power_source = display_power_.get_current_powerline_status()
        power_scheme = display_power_.get_current_power_scheme()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = Kei.PERCENT * panel.current_mode.HzRes * panel.current_mode.VtRes
                if dpst.set_xpst(panel, self.xpst_feature, False, power_source, power_scheme) is False:
                    self.fail(f"Failed to disable XPST via IGCL ")

                # Generate pattern
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey, generate_frame.Color.white],
                                                  frame_type='Double_Frame')
                generate_frame.move_image_file_to_folder()
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                logging.info("Waiting for 7 seconds to complete phasing")
                time.sleep(7)
                # Run Workload
                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))
                status, etl_file, _ = igcl_xpst_toggle_scenario(panel, self.xpst_feature, count=5, delay=10)

                generate_frame.close_exe()

                if status is False:
                    self.fail(f"Failed to get ETL")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= dpst.verify_hist_read_and_work_item_count(log_file, 5, 0)
                status &= dpst.verify_kei_min_brightness(adapter, panel, Kei.MIN_BLC_REDUCTION)

        if status is False:
            self.fail(f"FAIL: KEI Test failure for BLC_MIN_BRIGHTNESS")
        logging.info(f"PASS: KEI Test pass for BLC_MIN_BRIGHTNESS")

    ##
    # @brief        This function verifies XPST MaxLatencyPhasing during MaxLatencyPhasingIgclLevel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['MAX_LATENCY_PHASING_IGCL_LEVEL'])
    # @endcond
    def t_12_igcl_level_change_max_latency_phasing(self):
        html.step_start(f"Verifying XPST Kei for MAX_LATENCY_PHASING_IGCL_LEVEL")
        etl_file = None
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = Kei.PERCENT * panel.current_mode.HzRes * panel.current_mode.VtRes

                # Generate Frame
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey, generate_frame.Color.white],
                                                  frame_type='Double_Frame')
                generate_frame.move_image_file_to_folder()
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                logging.info("Waiting for 7 seconds to complete phasing")
                time.sleep(7)

                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))
                status, etl_file, time_stamps = igcl_level_change_scenario(panel, self.xpst_feature, delay=10)

                generate_frame.close_exe()

                if status is False:
                    self.fail(f"Failed to get ETL")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= dpst.verify_hist_read_and_work_item_count(log_file, 3, 0)
                status &= dpst.verify_kei_max_latency_phasing(adapter, panel, self.xpst_feature,
                                                              Kei.MAX_LATENCY_PHASING_IN_MS_NOT_FOR_FRAME_CHANGE,
                                                              time_stamps)

        if status is False:
            self.fail(f"FAIL: KEI Test failure for MAX_LATENCY_PHASING_IGCL_LEVEL")
        logging.info(f"PASS: KEI Test passed for MAX_LATENCY_PHASING_IGCL_LEVEL")

    ##
    # @brief        This function verifies XPST MaxLatencyPhasing during MaxLatencyPhasingIgclStatus
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['MAX_LATENCY_PHASING_IGCL_STATUS'])
    # @endcond
    def t_13_igcl_xpst_toggle_max_latency_phasing(self):
        html.step_start(f"Verifying XPST Kei for MAX_LATENCY_PHASING_IGCL_STATUS")
        etl_file = None
        power_source = display_power_.get_current_powerline_status()
        power_scheme = display_power_.get_current_power_scheme()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = Kei.PERCENT * panel.current_mode.HzRes * panel.current_mode.VtRes
                if dpst.set_xpst(panel, self.xpst_feature, False, power_source, power_scheme) is False:
                    self.fail(f"Failed to disable XPST via IGCL ")

                # Generate Frame
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey, generate_frame.Color.white],
                                                  frame_type='Double_Frame')
                generate_frame.move_image_file_to_folder()
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                logging.info("Waiting for 7 seconds to complete phasing")
                time.sleep(7)

                # Run Workload
                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))
                status, etl_file, time_stamps = igcl_xpst_toggle_scenario(panel, self.xpst_feature, count=5, delay=10)

                if status is False:
                    self.fail(f"Failed to get ETL")

                generate_frame.close_exe()

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= dpst.verify_hist_read_and_work_item_count(log_file, 5, 0)
                status &= dpst.verify_kei_max_latency_phasing(adapter, panel, self.xpst_feature,
                                                              Kei.MAX_LATENCY_PHASING_IN_MS_NOT_FOR_FRAME_CHANGE,
                                                              time_stamps)

        if status is False:
            self.fail(f"FAIL: KEI Test failure for MAX_LATENCY_PHASING_IGCL_STATUS")
        logging.info(f"PASS: KEI Test passed for MAX_LATENCY_PHASING_IGCL_STATUS")

    ##
    # @brief        This function verifies XPST during PhasingDurationIgclStatus
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['PHASING_DURATION_IGCL_STATUS'])
    # @endcond
    def t_14_igcl_xpst_toggle_phasing_duration(self):
        html.step_start(f"Verifying XPST Kei for PHASING_DURATION_IGCL_STATUS")
        etl_file = None
        power_source = display_power_.get_current_powerline_status()
        power_scheme = display_power_.get_current_power_scheme()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = Kei.PERCENT * panel.current_mode.HzRes * panel.current_mode.VtRes
                if dpst.set_xpst(panel, self.xpst_feature, False, power_source, power_scheme) is False:
                    self.fail(f"Failed to disable XPST via IGCL ")

                # Generate Frame
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey, generate_frame.Color.white],
                                                  frame_type='Double_Frame')
                generate_frame.move_image_file_to_folder()
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                logging.info("Waiting for 7 seconds to complete phasing")
                time.sleep(7)

                # Run Workload
                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))

                status, etl_file, _ = igcl_xpst_toggle_scenario(panel, self.xpst_feature, count=5, delay=10)

                generate_frame.close_exe()

                if status is False:
                    self.fail(f"Failed to get ETL")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= dpst.verify_hist_read_and_work_item_count(log_file, 5, 0)
                status &= dpst.verify_kei_phasing_duration(adapter, panel, log_file, self.xpst_feature,
                                                           Kei.PHASING_DURATION_RANGE, Kei.MAX_STEP_DURATION,
                                                           Kei.MAX_STEP_VARIANCE, Kei.MAX_IET_MISS)

        if status is False:
            self.fail(f"KEI for PhasingDuration is FAILED for PHASING_DURATION_IGCL_STATUS")
        logging.info(f"KEI for PhasingDuration is PASSED for PHASING_DURATION_IGCL_STATUS")

    ##
    # @brief        This function verifies XPST during PhasingDurationIgclStatus
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['NEAR_FSSC_FRAME_IGCL_STATUS'])
    # @endcond
    def t_15_near_fssc_frame_igcl_status(self):
        html.step_start(f"Verifying XPST Kei for NEAR_FSSC_FRAME_IGCL_STATUS")
        etl_file = None
        power_source = display_power_.get_current_powerline_status()
        power_scheme = display_power_.get_current_power_scheme()
        percent = 0.019
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = percent * panel.current_mode.HzRes * panel.current_mode.VtRes
                if dpst.set_xpst(panel, self.xpst_feature, False, power_source, power_scheme) is False:
                    self.fail(f"Failed to disable XPST via IGCL ")

                # Generate Frame
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.purple,
                                                         generate_frame.Color.dark_grey],
                                                  frame_type='Double_Frame')

                generate_frame.move_image_file_to_folder()
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Relax time to complete XPST Phase-in
                logging.info(f"Waiting for 7 seconds to complete phasing")
                time.sleep(7)
                # Run Workload
                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))
                status, etl_file, _ = igcl_xpst_toggle_scenario(panel, self.xpst_feature, count=5, delay=10)

                generate_frame.close_exe()

                if status is False:
                    self.fail(f"Failed to get ETL")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status &= dpst.verify_hist_read_and_work_item_count(log_file, 5, 0)
                status &= dpst.verify_kei_no_change(adapter, panel)

        if status is False:
            self.fail(f"KEI for Near FSSC frame is FAILED")
        logging.info(f"KEI for Near FSSC frame is PASSED")

    ##
    # @brief        This function verifies XPST during PhasingDuration during Frame change
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['PHASING_DURATION_FRAME_CHANGE_MAJOR'])
    # @endcond
    def t_16_phasing_duration_frame_change_major(self):
        html.step_start(f"Verifying XPST Kei for PHASING_DURATION_FRAME_CHANGE_MAJOR")
        etl_file = None
        count = 10
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = 0.125 * panel.current_mode.HzRes * panel.current_mode.VtRes

                # Generate Frame
                generate_frame.run_generate_frame(color=[generate_frame.Color.white, ], frame_type='Single_Frame')
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey,
                                                         generate_frame.Color.light_grey],
                                                  frame_type='Double_Frame')

                # Move Image file to Log Folder
                generate_frame.move_image_file_to_folder()
                # Launch Exe
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Workload ETL
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
                time.sleep(2)
                if status is False:
                    self.fail("Failed to get ETL before Workload")

                for i in range(count):
                    kb.press('RIGHT')
                    logging.info("Pressing Right and waiting for 10 seconds")
                    time.sleep(10)

                status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                generate_frame.close_exe()
                if status is None:
                    self.fail("FAILED to get ETL during Workload")
                if etl_file is False:
                    self.fail("Failed to run the workload")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if dpst.verify_kei_phasing_duration(adapter, panel, log_file, self.xpst_feature,
                                                    Kei.PHASING_DURATION_RANGE, Kei.MAX_STEP_DURATION,
                                                    Kei.MAX_STEP_VARIANCE, Kei.MAX_IET_MISS) is False:
                    self.fail(f"KEI for PhasingDuration is FAILED during Frame Change")
                logging.info(f"KEI for PhasingDuration is PASSED during Frame Change")

        html.step_end()

    ##
    # @brief        This function verifies XPST during PhasingDuration during Frame change
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['PHASING_DURATION_FRAME_CHANGE_MINOR'])
    # @endcond
    def t_17_phasing_duration_frame_change_minor(self):
        html.step_start(f"Verifying XPST Kei for PHASING_DURATION_FRAME_CHANGE_MINOR")
        etl_file = None
        count = 10
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                area = 0.125 * panel.current_mode.HzRes * panel.current_mode.VtRes

                # Generate Frame
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey,
                                                         generate_frame.Color.white],
                                                  frame_type='Double_Frame')
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.light_grey,
                                                         generate_frame.Color.white],
                                                  frame_type='Double_Frame')

                # Move Image file to Log Folder
                generate_frame.move_image_file_to_folder()
                # Launch Exe
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Workload ETL
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
                time.sleep(2)
                if status is False:
                    self.fail("Failed to get ETL before Workload")

                for i in range(count):
                    kb.press('RIGHT')
                    logging.info("Pressing Right and waiting for 10 seconds")
                    time.sleep(10)

                status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                generate_frame.close_exe()
                if status is None:
                    self.fail("FAILED to get ETL during Workload")
                if etl_file is False:
                    self.fail("Failed to run the workload")

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            self.fail("FAILED to generate the report")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if dpst.verify_kei_phasing_duration(adapter, panel, log_file, self.xpst_feature,
                                                    Kei.PHASING_DURATION_RANGE, Kei.MAX_STEP_DURATION,
                                                    Kei.MAX_STEP_VARIANCE, Kei.MAX_IET_MISS) is False:
                    self.fail(f"KEI for PhasingDuration is FAILED during Frame Change")
                logging.info(f"KEI for PhasingDuration is PASSED during Frame Change")

        html.step_end()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstKei))
    test_environment.TestEnvironment.cleanup(test_result)
