########################################################################################################################
# @file         sensor_wrapper.py
# @brief        Contains wrapper functions calling sensor util CDLL exposed APIs.
# @author       ashishk2
########################################################################################################################
import ctypes
import logging
import math
import os

from Libs.Core.test_env import test_context


##
# @brief        SensorInfo Structure
class SensorInfo(ctypes.Structure):
    _fields_ = [("AnalogInputIndex", ctypes.c_ulong),
                ("SamplingRate", ctypes.c_ulong),
                ("DurationOfCapture", ctypes.c_double)]


_sensor_dll = None


##
# @brief        Sensor Util Load Library.
# @return       None
def load_library():
    global _sensor_dll
    try:
        _sensor_dll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'SensorUtil.dll'))
    except IOError as error:
        logging.error("Unable to load SensorUtil DLL! Error : {0}".format(error))


##
# @brief        Wrapper API to capture sensor data
# @param[in]    index - AnalogInputIndex, optical sensor connected to DAQ device index
# @param[in]    sample_rate - Rate at which data will be captured
# @param[in]    duration - Duration for which data needs to be captured
# @return       (status,output) - (True on Success, False otherwise, Sensor data output)
def get_captured_sensor_data(index, sample_rate, duration):
    app_data = SensorInfo(index, sample_rate, duration)
    py_capture_sample = _sensor_dll.CaptureSensorData
    if not math.isinf(app_data.SamplingRate * app_data.DurationOfCapture):
        number_of_samples = int(app_data.SamplingRate * app_data.DurationOfCapture)
    else:
        logging.error("Infinity Error")
        return False, (ctypes.c_double * 1)(0.0)
    sensor_data_array = (ctypes.c_double * number_of_samples)(0.0)
    sensor_data_array_length = len(sensor_data_array)
    py_capture_sample.restype = ctypes.c_int
    py_capture_sample.argtypes = [ctypes.POINTER(SensorInfo), ctypes.POINTER(ctypes.c_double * number_of_samples), ctypes.c_int]
    status = py_capture_sample(ctypes.byref(app_data), ctypes.byref(sensor_data_array), sensor_data_array_length)
    output = [sensor_data_array[i] for i in range(sample_rate * duration)]
    return status, output
