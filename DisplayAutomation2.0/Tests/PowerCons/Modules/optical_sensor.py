#######################################################################################################################
# @file         optical_sensor.py
# @addtogroup   PowerCons
# @section      Libs
# @brief
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import os
import subprocess
import time
from multiprocessing import Process, Queue

from Libs.Core.wrapper import sensor_wrapper
from Libs.Core.wrapper import valsim_wrapper

__sensor_utility_process = None
__samples: Queue = Queue()
__stop_signal: Queue = Queue()


##
# @brief        Internal API for polling service
# @param[in]    index:       AnalogInputIndex, optical sensor connected to DAQ device index
# @param[in]    sample_rate: Rate at which data will be captured
# @param[in]    duration:    Duration for which data needs to be captured
# @param[in]    samples
def __sensor_utility_service(index, sample_rate, duration, samples, stop_signal):
    valsim_wrapper.load_library()
    sensor_wrapper.load_library()

    # Unblock main thread by putting some data in queue
    samples.put([])

    status, sensor_data = sensor_wrapper.get_captured_sensor_data(index, sample_rate, duration)
    samples.put(sensor_data)

    # Wait for stop call
    while True:
        if not stop_signal.empty():
            break

        time.sleep(1)


##
# @brief        Exposed API to start the sampling
# @param[in]    index:       AnalogInputIndex, optical sensor connected to DAQ device index
# @param[in]    sample_rate: Rate at which data will be captured
# @param[in]    duration:    Duration for which data needs to be captured
# @return       Boolean, True if operation is successful, False otherwise
def start(index=3, sample_rate=1000, duration=30):
    global __sensor_utility_process
    global __samples
    global __stop_signal

    # Make sure there is no ongoing sensor utility process
    # For now only one process is supported
    if __sensor_utility_process is not None:
        logging.warning("\tSensor Utility process is already running")
        return False

    __samples = Queue()
    __stop_signal = Queue()

    # Start the sensor utility service
    __sensor_utility_process = Process(
        target=__sensor_utility_service, args=(index, sample_rate, duration, __samples, __stop_signal))
    __sensor_utility_process.start()

    return True


##
# @brief        Exposed API to stop the sensor utility service
# @return       output, list, samples from sensor utility
def stop():
    global __sensor_utility_process
    global __stop_signal
    global __samples

    # Make sure sensor utility service is running before trying to stop it
    if __sensor_utility_process is None:
        logging.warning("\tNo sensor utility process found to stop")
        return False

    output = __samples.get()

    # Send the stop signal to stop the infinite loop and release all the locks
    __stop_signal.put(True)
    time.sleep(1)

    # Although stop signal will terminate the sensor utility service, we need a fail safe mechanism to terminate
    # the process if stop signal fails to terminate it
    subprocess.call('taskkill /F /T /PID ' + str(__sensor_utility_process.pid))
    __sensor_utility_process = None

    return output
