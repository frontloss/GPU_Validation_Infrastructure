#######################################################################################################################
# @file     powercons_escapes.py
# @brief    Python wrapper helper module providing multiple powercons escapes interface to driver
#
# @author   Ashish Tripathi, Vinod D S
#######################################################################################################################

import ctypes
import os

from Libs.Core.test_env import test_context

powercons_escapes_dll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'PowerConsEscapes.dll'))


##
# @brief set driver to use ALS override data
#
# @param[in] override    Boolean argument to override
# @param[in] lux		 lux value in integer
# @return  status pErrorCode contains error if any
def als_override(override, lux):
    error_info = ctypes.HRESULT()
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.HRESULT))
    func = prototype(('AlsOverride', powercons_escapes_dll))
    status = func(override, lux, ctypes.byref(error_info))
    return status
