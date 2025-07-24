########################################################################################################################
# @file         app_render_verification.py
# @brief        Contains verification logic for app rendering. Verify given app has run on given GPU.
# @author       Patel, Ankurkumar G
########################################################################################################################

import os, subprocess
import logging
import time

from Libs.Core.test_env import test_context
from Libs.Core.machine_info.machine_info import SystemInfo

##
# @brief        Verify App render
# @param[in]    app_path - App Path Location
# @param[in]    execution_time - time required for complete Execution of the App
# @param[in]    affinity - Affinity of the App to the feature.
# @return       bool - True if platform based affinity is applied, False otherwise
def verify_app_render(app_path, execution_time, affinity):
    device_id = None
    app_details_found = False
    app_name = app_path.split('/')[-1]

    etw_file_name = os.path.join(test_context.LOG_FOLDER , app_name + '_' + str(time.time()) + "_app_log.txt")
    etw_exe = os.path.join(test_context.COMMON_BIN_FOLDER, "ETWCRCMonitor.exe")

    # Log generation will happen for the time specified in execution_time
    etw_log_status = subprocess.call(["powershell.exe", etw_exe,  "-etw silent -command timeout /t " + str(execution_time) + " >" + etw_file_name])
    
    # wait for 2 seconds before parsing the etw_log file
    time.sleep(2)

    # Parse the logs           
    if not os.path.exists(etw_file_name):
        logging.info("app_log file for gpu usage not found in LOGS folder")
        return False

    with open(etw_file_name, encoding='utf-16') as f:
        lines = f.readlines()
        for line in lines:
            if device_id is None and "DxgKrnl device stats for adapter" in line:
                print(line.split(" ")[6])
                device_id = line.split(':')[2].split('(')[0]
            elif device_id and app_name in line:
                app_details_found = True
                logging.info("App %s has run on device %s " %(str(app_name) ,str(device_id)))
                break
        
    if device_id is None or app_details_found is False:
        logging.info("Not found any rendering information for app %s in etw logs" %app_name)
        return False
    
    platform_name = SystemInfo().get_platform_details(device_id).PlatformName

    if "DG" not in platform_name and affinity == "POWER_SAVING":
        logging.info("App rendering details : Expected: %s, Actaul: %s" %(str(affinity), "POWER_SAVING"))
        os.remove(etw_file_name)
        return True
    elif "DG" in platform_name and affinity == "HIGH_PERFORMANCE":
        logging.info("App rendering details : Expected: %s, Actaul: %s" %(str(affinity), "HIGH_PERFORMANCE"))
        os.remove(etw_file_name)
        return True
    elif "DG" not in platform_name and affinity == "HIGH_PERFORMANCE":
        logging.info("App rendering details : Expected: %s, Actaul: %s" %(str(affinity), "POWER_SAVING"))
        return False
    elif "DG" in platform_name and affinity == "POWER_SAVING":
        logging.info("App rendering details : Expected: %s, Actaul: %s" %(str(affinity), "HIGH_PERFORMANCE"))
        return False    


