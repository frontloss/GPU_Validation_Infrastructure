###################################################################################################################
# @file         context.py
# @addtogroup   NorthGate
# @brief        Contains APIs to manage tool context.
# @description  @ref context.py file contains the basic functions required to manage the tool context. Pickle module is
#               used to dump and load the data. Below APIs are exposed in this file:
#               1. get()
#               To get the stored context
#
#               2. store()
#               To store the given context in file
#
#               3. delete()
#               To delete the stored context
#
# @author       Rohit Kumar
###################################################################################################################

import os
import pickle

MANUAL_EXECUTION_DATA_FILE = "tool_context.pickle"


##
# @brief        Exposed API to get stored context
# @return       context if loading is successful, {} otherwise
def get():
    if os.path.exists(MANUAL_EXECUTION_DATA_FILE):
        try:
            with open(MANUAL_EXECUTION_DATA_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(e)
            os.remove(MANUAL_EXECUTION_DATA_FILE)
    return {}


##
# @brief        Exposed API to store given context
# @param[in]    context, context data to be stored
def store(context):
    try:
        with open(MANUAL_EXECUTION_DATA_FILE, "wb") as f:
            pickle.dump(context, f)
    except Exception as e:
        print(e)
        os.remove(MANUAL_EXECUTION_DATA_FILE)


##
# @brief        Exposed API to delete context
def delete():
    if os.path.exists(MANUAL_EXECUTION_DATA_FILE):
        os.remove(MANUAL_EXECUTION_DATA_FILE)
