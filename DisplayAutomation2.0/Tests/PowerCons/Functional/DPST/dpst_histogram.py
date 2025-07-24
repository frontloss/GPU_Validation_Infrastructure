########################################################################################################################
# @file         dpst_histogram.py
# @brief        Test for XPST Histogram Interrupt verification
# @author       Tulika
########################################################################################################################
import json
import logging
import re
import time
import unittest
import random

from Libs.Core import display_power, winkb_helper, display_essential
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DPST import generate_frame, dpst
from Tests.PowerCons.Functional.DPST.dpst_base import DpstBase
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload, common, dut, validator_runner


##
# @brief        This class contains histogram interrupt verification test cases for XPST
class DpstHistogram(DpstBase):
    ##
    # @brief        This class method is the entry point for XPST test cases. Helps to create the applied parameters
    #               required for XPST test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DpstHistogram, cls).setUpClass()
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

        if do_driver_restart:
            status, reboot_required = display_essential.restart_gfx_driver()
            assert status, "Failed to restart display driver"

        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

    ##
    # @brief        This class contains histogram interrupt verification test cases for XPST
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

        if do_driver_restart:
            status, reboot_required = display_essential.restart_gfx_driver()
            assert status, "Failed to restart display driver post RegKey disable"

        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)

        super(DpstHistogram, cls).tearDownClass()

    ##
    # @brief        This function verifies XPST histogram interrupt for solid color images for different resolution
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['SOLID_COLOR_IMAGE'])
    # @endcond
    def t_11_solid_color_image(self):
        display_power_ = display_power.DisplayPower()
        power_source = display_power_.get_current_powerline_status()
        power_scheme = display_power_.get_current_power_scheme()
        count = 8
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Generate pattern
                generate_frame.run_generate_frame(color=[generate_frame.Color.white, ], frame_type='Single_Frame')
                generate_frame.run_generate_frame(color=[generate_frame.Color.black, ], frame_type='Single_Frame')
                generate_frame.run_generate_frame(color=[generate_frame.Color.dark_grey, ], frame_type='Single_Frame')

                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))
                # Disable XPST via IGCL
                if dpst.set_xpst(panel, self.xpst_feature, False, power_source, power_scheme) is False:
                    logging.error(f"Failed to disable XPST via IGCL ")
                    return False, None

                # Move Image file to Log Folder
                generate_frame.move_image_file_to_folder()
                # Launch Exe
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Workload ETL
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
                time.sleep(2)
                if status is False:
                    self.fail("Failed to get ETL before Workload")
                if dpst.set_xpst(panel, self.xpst_feature, True, power_source, power_scheme) is False:
                    logging.error(f"Failed to disable XPST via IGCL ")
                    return False, None
                time.sleep(2)
                for i in range(count):
                    winkb_helper.press('RIGHT')
                    logging.info("Pressing Right and waiting for 2 seconds")
                    time.sleep(2)

                status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                if status is None:
                    self.fail("FAILED to get ETL during Workload")
                if etl_file is False:
                    self.fail("Failed to run the workload")
                generate_frame.close_exe()

                # Validate histogram interrupt for the frame change
                json_file = validator_runner.run_diana(f'golden_image', etl_file, ['DPST'])
                with open(json_file) as f:
                    data = f.read()
                    invalid_strings = re.findall('new Date\(\d+\)', data)
                    for invalid_string in invalid_strings:
                        data = data.replace(invalid_string, '"0"')
                    json_data = json.loads(data)
                    histogram_list = dpst.get_histogram_list(json_data)
                    logging.debug(f"Histogram list= {len(histogram_list)}, {histogram_list}")
                    if len(histogram_list) != count + 1:
                        self.fail(f"Histogram list Expected= {count + 1} Actual= {len(histogram_list)}")

                    # Total number of pixel count in each bin should be equal to the image size.
                    image_size = panel.current_mode.HzRes * panel.current_mode.VtRes
                    for each_bin in histogram_list:
                        pixel_count = 0
                        pixel_count += sum(each_bin)
                        logging.debug(f"Total Pixel count in each bin= {pixel_count}")
                        if pixel_count != image_size:
                            self.fail("Total pixel count does not match the image size."
                                      f"Expected= {image_size}, Actual= {pixel_count}")

    ##
    # @brief        This function verifies XPST histogram interrupt for less than 12% frame change
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['LESS_THAN_THRESHOLD'])
    # @endcond
    def t_12_less_than_threshold(self):
        count = 8
        # For Pre LNL, Guardband threshold is 12% of ImageSize. Keeping 11.5% for Below Threshold
        percent = 0.115
        for adapter in dut.adapters.values():
            #  From LNL+, Low threshold is being changed to 5% hence expecting zero interrupt for 4.5%.
            #  Even though HighThreshold Guardband is 10%,
            #  we need to consider 5% as interrupt can hit when change is more than 5% for interruptDelay frames.
            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                percent = 0.045
            for panel in adapter.panels.values():
                # Iterating between full screen solid color to 11.5% frame change
                area = percent * panel.current_mode.HzRes * panel.current_mode.VtRes
                # Generate Frame
                generate_frame.run_generate_frame(color=[generate_frame.Color.dark_grey, ], frame_type='Single_Frame')
                generate_frame.run_generate_frame(area=area,
                                                  color=[generate_frame.Color.dark_grey, generate_frame.Color.white],
                                                  frame_type='Double_Frame')

                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))

                # Move Image file to Log Folder
                generate_frame.move_image_file_to_folder()
                # Launch Exe
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Workload ETL
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
                time.sleep(2)
                if status is False:
                    self.fail("Failed to get ETL before Workload")

                time.sleep(2)
                for i in range(count):
                    winkb_helper.press('RIGHT')
                    logging.info("Pressing Right and waiting for 2 seconds")
                    time.sleep(2)

                status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                if status is None:
                    self.fail("FAILED to get ETL during Workload")
                if etl_file is False:
                    self.fail("Failed to run the workload")
                generate_frame.close_exe()

                # Validate histogram interrupt for the frame change
                json_file = validator_runner.run_diana(f'golden_image', etl_file, ['DPST'])
                with open(json_file) as f:
                    data = f.read()
                    invalid_strings = re.findall('new Date\(\d+\)', data)
                    for invalid_string in invalid_strings:
                        data = data.replace(invalid_string, '"0"')
                    json_data = json.loads(data)
                    histogram_list = dpst.get_histogram_list(json_data)
                    logging.info(f"Histogram list= {len(histogram_list)}, {histogram_list}")
                    if len(histogram_list) != 0:
                        self.fail(f"Histogram list Expected= 0 Actual= {len(histogram_list)}")

                    # Total number of pixel count in each bin should be equal to the image size.
                    image_size = panel.current_mode.HzRes * panel.current_mode.VtRes
                    for each_bin in histogram_list:
                        pixel_count = 0
                        pixel_count += sum(each_bin)
                        logging.info(f"Total Pixel count in each bin= {pixel_count}")
                        if pixel_count != image_size:
                            self.fail("Total pixel count does not match the image size."
                                      f"Expected= {image_size}, Actual= {pixel_count}")

    ##
    # @brief        This function verifies XPST histogram interrupt for random frame change greater than 12.5%
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['GREATER_THAN_THRESHOLD'])
    # @endcond
    def t_13_greater_than_threshold(self):
        count = 8
        percent = [0.125]
        threshold = 12.5
        for adapter in dut.adapters.values():
            # From PTL+, HighThreshold Guardband 10% of ImageSize. Keeping 10.5% for Greater then Threshold
            if adapter.name not in common.PRE_GEN_16_PLATFORMS:
                percent = [0.105]
                threshold = 10.5
            for panel in adapter.panels.values():
                # random but greater than threshold (12.5% for PreGen16 and 10.5% for Gen16+) frame change
                random_value = random.uniform(threshold, 100) / 100
                percent.append(random_value)
                logging.info(f"Frame change percent {percent}")

                # Generate Frame
                generate_frame.run_generate_frame(area=percent[0] * panel.current_mode.HzRes * panel.current_mode.VtRes,
                                                  color=[generate_frame.Color.white,
                                                         generate_frame.Color.black],
                                                  frame_type='Double_Frame')
                generate_frame.run_generate_frame(area=percent[1] * panel.current_mode.HzRes * panel.current_mode.VtRes,
                                                  color=[generate_frame.Color.purple,
                                                         generate_frame.Color.dark_grey],
                                                  frame_type='Double_Frame')

                if not dpst.igcl_is_xpst_supported:
                    self.fail(logging.error(f"XPST is NOT supported for {panel.port}"))

                # Move Image file to Log Folder
                generate_frame.move_image_file_to_folder()
                # Launch Exe
                generate_frame.launch_exe(panel.current_mode.HzRes, panel.current_mode.VtRes)

                # Workload ETL
                status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
                time.sleep(2)
                if status is False:
                    self.fail("Failed to get ETL before Workload")
                time.sleep(2)
                for i in range(count):
                    winkb_helper.press('RIGHT')
                    logging.info("Pressing Right and waiting for 2 seconds")
                    time.sleep(2)
                status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                if status is None:
                    self.fail("FAILED to get ETL during Workload")
                if etl_file is False:
                    self.fail("Failed to run the workload")

                # Close exe
                generate_frame.close_exe()

                # Validate histogram interrupt for the frame change
                json_file = validator_runner.run_diana(f'golden_image', etl_file, ['DPST'])
                with open(json_file) as f:
                    data = f.read()
                    invalid_strings = re.findall('new Date\(\d+\)', data)
                    for invalid_string in invalid_strings:
                        data = data.replace(invalid_string, '"0"')
                    json_data = json.loads(data)
                    histogram_list = dpst.get_histogram_list(json_data)
                    logging.info(f"Histogram list= {len(histogram_list)}, {histogram_list}")
                    if len(histogram_list) != count:
                        self.fail(f"Histogram list Expected= {count + 1} Actual= {len(histogram_list)}")

                    # Total number of pixel count in each bin should be equal to the image size.
                    image_size = panel.current_mode.HzRes * panel.current_mode.VtRes
                    for each_bin in histogram_list:
                        pixel_count = 0
                        pixel_count += sum(each_bin)
                        logging.info(f"Total Pixel count in each bin= {pixel_count}")
                        if pixel_count != image_size:
                            self.fail("Total pixel count does not match the image size."
                                      f"Expected= {image_size}, Actual= {pixel_count}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstHistogram))
    test_environment.TestEnvironment.cleanup(test_result)
