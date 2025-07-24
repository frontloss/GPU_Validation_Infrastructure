########################################################################################################################
# @file     optical_sensor_base.py
# @brief    remarks This script contains helper functions that will be used by optical sensor based validation script
# @author   ashishk2
########################################################################################################################

import logging
import math
import os
import sys
import threading
import unittest

import matplotlib.pyplot as plt
from Libs.Core.wrapper import sensor_wrapper

from Libs.Core import cmd_parser
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context


##
# @brief        OpticalSensorBase
class OpticalSensorBase(unittest.TestCase):
    display_config_ = DisplayConfiguration()
    sensor_graph_path = os.path.join(test_context.LOG_FOLDER, "sensor_data.pdf")

    ##
    # @brief        setUp
    # @return       None
    def setUp(self):

        # Default values for cmd line
        self.analog_input_index = 3
        self.sample_rate = 1000
        self.duration_in_seconds = 10
        self.panel_info = {}
        self.platform = None
        self.input_display_list = []

        # Parse the commandline params
        cmd_line_param = cmd_parser.parse_cmdline(sys.argv, ['-INDEX', '-RATE', '-DURATION'])
        self.analog_input_index = int(cmd_line_param['INDEX'][0])
        self.sample_rate = int(cmd_line_param['RATE'][0])
        self.duration_in_seconds = int(cmd_line_param['DURATION'][0])

        logging.info("App config values are: analog_input_index: {}, sample_rate: {}, duration_in_seconds: {}"
                     .format(self.analog_input_index, self.sample_rate, self.duration_in_seconds))

        self.input_display_list = cmd_parser.get_sorted_display_list(cmd_line_param)

        logging.info("Input display list is : {}".format(self.input_display_list))

        # Load sensorUtil dll
        sensor_wrapper.load_library()


    ##
    # @brief        This method helps in capturing sensor data and processing it.
    # @param[in]    index - AnalogInputIndex, optical sensor connected to DAQ device index
    # @param[in]    sample_rate - Rate at which data will be captured
    # @param[in]    duration - Duration for which data needs to be captured
    # @param[in]    result
    # @return       result - Sensor Data Thread result
    def capture_sensor_data_thread(self, index, sample_rate, duration, result):

        result = True
        status = False
        logging.info("Sample rate : {0}, captured duration: {1}s".
                     format(sample_rate, duration))
        step_count = 1 / 256
        logging.info("Step count: {0:0.8f}".format(step_count))
        status, sensor_data_array = sensor_wrapper.get_captured_sensor_data(index, sample_rate, duration)
        if not status:
            gdhm.report_bug(
                title="[OpticalSensor] Dll call to capture sensor data Failed ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Capture of sensor data Failed")

        num_sample = int(sample_rate * duration)
        neg_count = 0
        min_val = sensor_data_array[0]
        if min_val < 0:
            min_val = 0
        max_val = sensor_data_array[0]

        for sample_index in range(num_sample):
            if sensor_data_array[sample_index] < 0:
                sensor_data_array[sample_index] = 0
                neg_count += 1
            if sensor_data_array[sample_index] < min_val:
                min_val = sensor_data_array[sample_index]
            if sensor_data_array[sample_index] > max_val:
                max_val = sensor_data_array[sample_index]
        logging.info("min value:{0}, max value: {1}, negative value count:{2}".format(min_val, max_val, neg_count))

        # Returning from here as normalization will throw divide by zero error
        if max_val == min_val:
            logging.error("Divide by Zero error, as Max_Val:{0}, Min_val:{1} are same".format(max_val, min_val))
            return False

        for sample_index in range(num_sample):
            normalized_val = (sensor_data_array[sample_index] - min_val) / (max_val - min_val)
            if normalized_val < step_count:
                sensor_data_array[sample_index] = 0
            else:
                sensor_data_array[sample_index] = normalized_val

        digital_list = []
        for sample_index in range(num_sample):
            if sensor_data_array[sample_index] > 0.75:
                digital_list.append(sensor_data_array[sample_index])
                sensor_data_array[sample_index] = 1
            else:
                digital_list.append(sensor_data_array[sample_index])
                sensor_data_array[sample_index] = 0
        sam_size = len(digital_list)
        f = plt.figure()
        plt.plot(range(sam_size), digital_list)
        plt.ylabel('Normalized Voltage')
        plt.xlabel('Time in milliseconds')
        f.savefig(self.sensor_graph_path, bbox_inches='tight')

        # Calculate blankout and its time period
        blankout_dict = {}
        has_zero_occured = False
        zero_count = 0
        blankout_count = 0
        blankout_duration = 0
        for sample_index in range(num_sample):
            if sensor_data_array[sample_index] == 0 and not has_zero_occured:
                has_zero_occured = True
                zero_count = zero_count + 1
            if sensor_data_array[sample_index] == 0 and has_zero_occured:
                zero_count = zero_count + 1
            if sensor_data_array[sample_index] == 1 and has_zero_occured:
                blankout_count = blankout_count + 1
                blankout_dict[blankout_count] = zero_count
                zero_count = 0
                has_zero_occured = False
        for key, value in blankout_dict.items():
            logging.info("Blankout number: {}, Blankout_duration in ms: {}".format(key, value))
            blankout_duration = value

        if blankout_count > 1 or blankout_duration < 1000 or blankout_duration > 2200:
            logging.error("Blankout count: {} and Blankout_duration: {}".format(blankout_count, blankout_duration))
            result = False

        return result


##
# @brief        A Custom class for thread is created so that thread returns status when
#               join is called from the main, otherwise by default join returns NONE but it should
#               return either True or False from capture_sensor_data_thread function.
class ThreadWithReturnValue(threading.Thread):
    ##
    # @brief        run
    # @return        None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    ##
    # @brief        Join
    # @return       optical_sensor_base.ThreadWithReturnValue.run - thread return
    def join(self):
        threading.Thread.join(self)
        return self._return
