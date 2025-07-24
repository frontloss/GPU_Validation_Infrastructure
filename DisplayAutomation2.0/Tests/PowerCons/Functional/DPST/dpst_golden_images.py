########################################################################################################################
# @file         dpst_golden_images.py
# @brief        Test for DPST golden values with decided image scenarios
#
# @author       Ashish Tripathi
########################################################################################################################
import json
import os
import re
import subprocess
import time
import win32api
from Libs.Core import winkb_helper as kb
from Libs.Core.logger import html

from Libs.Core.test_env import test_environment
from Libs.Core.display_config import display_config
from Tests.PowerCons.Functional.DPST.GoldenNumbers import golden_numbers_mapping

from Tests.PowerCons.Functional.DPST.dpst_base import *
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import validator_runner
from Tests.PowerCons.Modules import workload

DELTA_PHASE_TOLERANCE_COUNT = 15
# Keeping tolerance because histogram values of an images can not be exact same for each bin in every run.
# For now, tolerance is 0.05%. For ex for 1920 x 1080 image size tolerance will be approx 1000 pixels.
HISTOGRAM_TOLERANCE = 0.05
config_ = display_config.DisplayConfiguration()


##
# @brief        API to compare LUT target values from DiAna output
# @param[in]    frame_size string, XxY_LEVEL_#
# @param[in]    json_data json, json output from DiAna
# @param[in]    image_name string, required for the values to be compared for respective image
# @return       bool, True if pass, False otherwise
def verify_lut_target_values(frame_size: str, json_data, image_name: str):
    current_lut_target = {}
    count = 0
    event_name = "DpstRunAlgorithm"
    field_name = "LUT"
    for msg in json_data['ReportQueue']:
        if event_name + '(' in msg['Header']:
            for event in [msg['Header']]:
                ind = event.index(field_name + "= ")
                arr = (event[ind + len(field_name + "= "):]).split(',')
                lut_list = []
                for a in arr[0:33]:
                    lut_list.append(int(a))
                current_lut_target[count] = lut_list  # take 33 values only
                count += 1
    if frame_size not in golden_numbers_mapping.LUT_TARGET_SINGLE_IMAGE:
        logging.error(f"LUT Target values are not available for {frame_size}")
        return False
    logging.info(f"Comparing LUT Target values of {image_name} for {frame_size}")
    golden_values = golden_numbers_mapping.LUT_TARGET_SINGLE_IMAGE[frame_size][image_name]
    if current_lut_target != golden_values:
        logging.error(f"LUT target values are not equal."
                      f" Expected= {golden_values}, Actual= {current_lut_target}")
        return False
    logging.info("LUT Target values are equal")
    return True


##
# @brief        API to compare Multiplier Lut Current from DiAna output
# @param[in]    frame_size string, XxY_LEVEL_#
# @param[in]    json_data json, json output from DiAna
# @param[in]    image_name string, required for the values to be compared for respective image
# @return       bool, True if pass, False otherwise
def verify_multiplier_lut_current(frame_size, json_data, image_name: str):
    field_values = []
    multiplier_lut_current = {}
    event_name = "Dpst7xPhaseCoordinatorSmoothenDpstLutTemporalFilter"
    field_name = "MultiplierLutCurrent"
    iir_count = 0
    golden_values = golden_numbers_mapping.MULTIPLIER_LUT_CURRENT_SINGLE_IMAGE[frame_size][image_name]
    for msg in json_data['ReportQueue']:
        if 'Dpst7xPhaseCoordinatorIIRFilterCoefficient(' in msg['Header']:
            if iir_count != 0:
                multiplier_lut_current[iir_count] = field_values
            field_values = []
            iir_count += 1
        if event_name + '(' in msg['Header']:
            for event in [msg['Header']]:
                ind = event.index(field_name + "= ")
                arr = (event[ind + len(field_name + "= "):]).split(',')
                field_values.append(arr[0])
    if frame_size not in golden_numbers_mapping.MULTIPLIER_LUT_CURRENT_SINGLE_IMAGE:
        logging.error(f"Multiplier LUT current values are not available for {frame_size}")
        return False
    logging.info(f"Comparing Multiplier LUT current values of {image_name} for {frame_size}")
    logging.info(f"Expected= {golden_values}, Actual= {multiplier_lut_current}")
    if multiplier_lut_current == golden_values:
        logging.info("Multiplier LUT Current values are equal")
        return True

    if len(multiplier_lut_current) != len(golden_values):
        logging.error(f"\tNumber of phase-in is not same. Expected= {len(golden_values)}, "
                      f"Actual= {len(multiplier_lut_current)}")
        return False

    logging.info("\tMultiplier LUT Current values are not equal. Verifying delta is in tolerance")
    diff_values = []
    for k in multiplier_lut_current:
        if multiplier_lut_current[k] != golden_values[k]:
            diff_values.append(k)

    # log to GDHM instead failing the tests. Start failing the test when results are consistent
    if len(diff_values) > DELTA_PHASE_TOLERANCE_COUNT:
        gdhm_title = "[PowerCons][DPST7] Multiplier LUT current values are not within tolerance"
        gdhm.report_bug(
            title=gdhm_title,
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("\tMultiplier LUT current values are not within tolerance. Below are the delta")
        for val in diff_values:
            logging.error(f"\tExpected= {multiplier_lut_current[val]}, Actual= {golden_values[val]}")

    status = True
    logging.info("\tVerifying that delta values are having difference of +1 or -1")
    for keys in diff_values:
        logging.info(f"Verifying values, GoldenData= {golden_values[keys]}, EtlData= {multiplier_lut_current[keys]}")
        for idx in range(len(multiplier_lut_current[keys])):
            if multiplier_lut_current[keys][idx] != golden_values[keys][idx]:
                if abs(int(multiplier_lut_current[keys][idx]) - int(golden_values[keys][idx])) != 1:
                    logging.error("\tDelta values are having more difference than 1. Below are the values")
                    logging.error(f"\tExpected: {multiplier_lut_current[keys]}, Actual= {golden_values[keys]}")
                    status &= False
                else:
                    logging.info("\tValues are within tolerance +1 or -1")
    return status


##
# @brief        API to verify histogram golden values
# @param[in]    json_data json, json output from DiAna
# @param[in]    panel object, Panel
# @param[in]    count total number of iterations
# @param[in]    feature - XpstFeature
# @return       bool, True if pass, False otherwise
def verify_histogram_golden_value(json_data, panel, count, feature):
    status = True
    total_images = 3
    html.step_start("Verifying Histogram golden values")
    frame = f"{panel.current_mode.HzRes}x{panel.current_mode.VtRes}_FULLSCREEN_HISTOGRAM_{dpst.XpstFeature(feature).name}"
    histogram_list = dpst.get_histogram_list(json_data)
    logging.info(f"Current Histogram Values= {histogram_list}")
    if len(histogram_list) == 0:
        logging.error(f"Histogram list is empty for {frame}")
        html.step_end()
        return False

    status, image_size = dpst.verify_histogram_count_and_image_size(panel, histogram_list, total_images, count)
    if status is False:
        logging.error(f"Histogram count and image size verification failed for {frame}")
        html.step_end()
        return False

    # Verification of histogram golden values
    if frame not in golden_numbers_mapping.HISTOGRAM_IMAGE:
        logging.error(f"Histogram Target values are not available for {frame}")
        html.step_end()
        return False

    for each_count in range(len(histogram_list)):
        if each_count % total_images == 0:
            image_name = 'BLACK'
        elif each_count % total_images == 1:
            image_name = 'WHITE'
        else:
            image_name = 'GREY'
        logging.info(f"Comparing Histogram Target values of {image_name} for {frame}")
        golden_values = golden_numbers_mapping.HISTOGRAM_IMAGE[frame][image_name]
        for i in range(0, 32):
            if histogram_list[each_count][i] != golden_values[i]:
                difference = abs(golden_values[i] - histogram_list[each_count][i])
                tolerance = (difference/image_size) * 100
                logging.debug(f"Histogram tolerance percentage due to different histogram values= {tolerance}")
                if tolerance >= HISTOGRAM_TOLERANCE:
                    logging.error(f"Histogram target values are not equal."
                                  f" Expected= {golden_values}, Actual= {histogram_list[each_count]}")
                    status = False

    if status:
        logging.info(f"Histogram target values are equal for feature {dpst.XpstFeature(feature).name}")
    else:
        logging.error(f"Invalid histogram values programmed for feature {dpst.XpstFeature(feature).name}")
        gdhm.report_driver_bug_pc(f"[XPST] Invalid histogram values programmed for feature {dpst.XpstFeature(feature).name}")

    html.step_end()
    return status


##
# @brief        This class contains transition of image test cases for DPST
class DpstGoldenImages(DpstBase):
    ##
    # @brief        This class method is the entry point for DPST test cases. Helps to initialize some of the
    #               parameters required for DPST test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DpstGoldenImages, cls).setUpClass()
        for adapter in dut.adapters.values():
            do_driver_restart = False
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported:
                    status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if status is False:
                        assert False, "FAILED to disable PSR via reg-key"
                    do_driver_restart = True if status is True else do_driver_restart
                    break
            if do_driver_restart:
                result, reboot_required = display_essential.restart_gfx_driver()
                assert result, "FAILED to restart the driver"
                logging.info(f"Successfully restarted the driver for {adapter.gfx_index}")

    ##
    # @brief        This class method is the exit point for DPST test cases. Helps to restore the applied parameters
    #               required for DPST test execution.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        super(DpstGoldenImages, cls).tearDownClass()
        for adapter in dut.adapters.values():
            do_driver_restart = False
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported:
                    psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if psr_status is False:
                        assert False, "FAILED to enable PSR via reg-key"
                    do_driver_restart = True if psr_status is True else do_driver_restart
                    break
            if do_driver_restart:
                result, reboot_required = display_essential.restart_gfx_driver()
                assert result, "FAILED to restart the driver"
                logging.info(f"Successfully restarted the driver for {adapter.gfx_index}")

    ##
    # @brief        This function verifies DPST with Golden Images in DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['LEVEL_6', 'FULLSCREEN'])
    # @endcond
    def t_11_level_6_full_screen(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                for _ in range(1, 5):
                    etl_file = dpst.run_workload(
                        dpst.WorkloadMethod.GOLDEN_IMAGE, dpst.FrameChangeType.SINGLE, image_number=_)
                    if etl_file is False:
                        self.fail("Failed to run the workload")
                    json_file = validator_runner.run_diana(f'golden_image_{_}', etl_file, ['dpst'])
                    with open(json_file) as f:
                        data = f.read()
                        invalid_strings = re.findall('new Date\(\d+\)', data)
                        for invalid_string in invalid_strings:
                            data = data.replace(invalid_string, '"0"')
                        json_data = json.loads(data)
                        mode = config_.get_native_mode(panel.display_info.DisplayAndAdapterInfo)
                        if mode is None:
                            self.fail(f"Failed to get native mode for {panel.display_info.DisplayAndAdapterInfo}")
                        frame_size = f"{mode.__str__().split('@')[0]}_{dpst.Aggressiveness(dpst.Aggressiveness.LEVEL_6).name}" \
                                     f"_FULLSCREEN_{self.max_smoothening_speed}"
                        status &= verify_lut_target_values(frame_size, json_data, f'IMAGE{_}')
                        status &= verify_multiplier_lut_current(frame_size, json_data, f'IMAGE{_}')
        if status is False:
            self.fail("Golden Number comparison FAILED")
        logging.info("Golden Number comparison PASSED")

    ##
    # @brief        This function verifies DPST with Golden Images in DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['LEVEL_6', 'WINDOWED'])
    # @endcond
    def t_12_level_6_windowed_screen(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                for _ in range(1, 5):
                    etl_file = dpst.run_workload(
                        dpst.WorkloadMethod.GOLDEN_IMAGE, dpst.FrameChangeType.SINGLE, dpst.WindowMode.WINDOWED, _)
                    if etl_file is False:
                        self.fail("Failed to run the workload")
                    json_file = validator_runner.run_diana(f'golden_image_{_}', etl_file, ['dpst'])
                    with open(json_file) as f:
                        data = f.read()
                        invalid_strings = re.findall('new Date\(\d+\)', data)
                        for invalid_string in invalid_strings:
                            data = data.replace(invalid_string, '"0"')
                        json_data = json.loads(data)
                        mode = config_.get_native_mode(panel.display_info.DisplayAndAdapterInfo)
                        if mode is None:
                            self.fail(f"Failed to get native mode for {panel.display_info.DisplayAndAdapterInfo}")
                        frame_size = f"{mode.__str__().split('@')[0]}_{dpst.Aggressiveness(dpst.Aggressiveness.LEVEL_6).name}" \
                                     f"_WINDOWED_{self.max_smoothening_speed}"
                        status &= verify_lut_target_values(frame_size, json_data, f'IMAGE{_}')
                        status &= verify_multiplier_lut_current(frame_size, json_data, f'IMAGE{_}')
        if status is False:
            self.fail("Golden Number comparison FAILED")
        logging.info("Golden Number comparison PASSED")

    ##
    # @brief        This function verifies FULLSCREEN HISTOGRAM for solid color images in DC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['FULLSCREEN', 'HISTOGRAM'])
    # @endcond
    def t_13_level_6_full_screen_histogram(self):
        status = True
        full_screen_mode = dpst.WindowMode.FULLSCREEN
        __APPLICATIONS_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "Applications")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                flag = True
                trial_count = 1
                while flag and trial_count < 3:
                    process = subprocess.Popen(os.path.join(__APPLICATIONS_FOLDER, "SolidImages.exe"))
                    time.sleep(self.delay)
                    # move cursor to right bottom corner
                    win32api.SetCursorPos((win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)))
                    status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceBeforeWorkload")
                    if status is None:
                        self.fail("FAILED to get ETL before Workload")
                    for i in range(0, self.count):
                        if full_screen_mode == dpst.WindowMode.FULLSCREEN:
                            kb.press('0')
                            time.sleep(self.delay)
                            kb.press('1')
                            time.sleep(self.delay)
                            kb.press('2')
                            time.sleep(self.delay)

                    status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
                    if status is None:
                        self.fail("FAILED to get ETL during Workload")

                    process.kill()

                    if etl_file is False:
                        self.fail("Failed to run the workload")

                    json_file = validator_runner.run_diana(f'golden_image', etl_file, ['DPST'])
                    with open(json_file) as f:
                        data = f.read()
                        invalid_strings = re.findall('new Date\(\d+\)', data)
                        for invalid_string in invalid_strings:
                            data = data.replace(invalid_string, '"0"')
                        json_data = json.loads(data)
                        histogram_list = dpst.get_histogram_list(json_data)
                        if len(histogram_list) != 30:
                            trial_count += 1
                            logging.info(f"Total no of histogram. Expected= 30, Actual= {len(histogram_list)}")
                            logging.info(f"Trying to launch app for the {trial_count} time to get correct histogram "
                                         f"and avoid any app issue")
                        else:
                            status &= verify_histogram_golden_value(json_data, panel, self.count, self.xpst_feature)
                            flag = False

        if status is False:
            self.fail(f"Golden Number comparison FAILED for feature {dpst.XpstFeature(self.xpst_feature).name}")
        logging.info(f"Golden Number comparison PASSED for feature {dpst.XpstFeature(self.xpst_feature).name}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstGoldenImages))
    test_environment.TestEnvironment.cleanup(test_result)
