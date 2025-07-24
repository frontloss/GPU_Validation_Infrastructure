#######################################################################################################################
# @file         polling.py
# @brief
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import subprocess
import time
from datetime import datetime
from multiprocessing import Process, Queue

from Libs.Core.sw_sim import driver_interface
from Libs.Core.wrapper import valsim_wrapper

__polling_process = None
__polled_timeline = None
__polled_timestamps = None
__stop_signal = None


##
# @brief        Internal API for polling service
# @param[in]    mmio_offsets List, list of offsets to be polled
# @param[in]    delay Number time in seconds
# @param[in]    polled_timeline list of values of selected registers
# @param[in]    polled_timestamps list of timestamps of selected registers
# @param[in]    stop_signal is a signal
# @return       None
def __polling_service(mmio_offsets, delay, polled_timeline, polled_timestamps, stop_signal):
    valsim_wrapper.load_library()
    polled_timeline.put({k: [] for k in mmio_offsets})
    polled_timestamps.put([])

    while True:
        t = datetime.now()
        temp_list = polled_timestamps.get()
        temp_list.append(t)
        polled_timestamps.put(temp_list)

        for offset in mmio_offsets:
            temp_dict = polled_timeline.get()
            temp_list = polled_timestamps.get()
            temp_dict[offset].append(driver_interface.DriverInterface().mmio_read(offset, 'gfx_0'))
            polled_timeline.put(temp_dict)
            polled_timestamps.put(temp_list)

        if not stop_signal.empty():
            break

        time.sleep(delay)


##
# @brief        Exposed API to start the polling of given features
# @param[in]    mmio_offsets [Optional], List, list of offsets to be polled
# @param[in]    delay Number, time in seconds
# @return       Boolean True if operation is successful, False otherwise
# @note         Polling service will use driver_interface library for MMIO reads and driver escape for DPCD reads. Since
#               it will be a separate process, system_utility will be loaded again, which may take up to 10-15 seconds.
def start(mmio_offsets=None, delay=1):
    global __polling_process
    global __polled_timeline
    global __polled_timestamps
    global __stop_signal

    if mmio_offsets is None:
        logging.warning("\tNo MMIO or DPCD offset passed to be polled")
        return False

    mmio_offsets = mmio_offsets if mmio_offsets is not None else []

    # Make sure there is no ongoing polling process
    # For now only one polling process is supported
    if __polling_process is not None:
        logging.warning("\tPolling process is already running")
        return False

    __polled_timeline = Queue()
    __polled_timestamps = Queue()
    __stop_signal = Queue()

    # Start the polling service with given features and delay
    __polling_process = Process(
        target=__polling_service, args=(
            mmio_offsets, delay, __polled_timeline, __polled_timestamps, __stop_signal))
    __polling_process.start()

    # Blocking the main thread until all the required modules are loaded in polling service
    temp = __polled_timestamps.get()
    __polled_timestamps.put(temp)

    return True


##
# @brief        Exposed API to stop the polling
# @return       output, tuple, polled timeline and a list of polled time stamps
def stop():
    global __polling_process
    global __stop_signal

    ##
    # Make sure polling service is running before trying to stop it
    if __polling_process is None:
        logging.warning("\tNo polling process found to stop")
        return False

    ##
    # Send the stop signal to stop the infinite loop and release all the locks
    __stop_signal.put(True)
    time.sleep(1)

    output = (__polled_timeline.get(), __polled_timestamps.get())

    ##
    # Although stop signal will terminate the polling service, we need a fail safe mechanism to terminate the process
    # if stop signal fails to terminate it
    subprocess.call('taskkill /F /T /PID ' + str(__polling_process.pid))
    __polling_process = None

    return output
