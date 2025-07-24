########################################################################################################################
# @file         vdd.py
# @brief        This file contains VDD verification APIs
#
# @author       Akshaya Nair
########################################################################################################################

import logging
import os
import shutil
import sys
import time

from Libs.Core import display_power, enum, etl_parser
from Libs.Core import reboot_helper
from Libs.Core.logger import etl_tracer, gdhm, html
from Libs.Core.test_env import test_context
from Tests.PowerCons.Modules import common, dut, workload

# GDHM header
GDHM_VDD = "[Display_Interface][EDP][VDD]"

##
# @brief        This function verifies VDD status from ETL report
# @param[in]    etl_file
# @return       True if VDD turned OFF else False
# @cond
# @endcond
def verify_vdd_status_powerevent(etl_file):
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate report for {0}".format(etl_file))
        return False

    pps_data = etl_parser.get_event_data(etl_parser.Events.PPS_DATA)
    if pps_data is None:
        logging.error("No PPS data found in ETL")
        return False

    for entry in range(len(pps_data)):
        if pps_data[entry].PpsSignal == "DD_VDD":
            logging.debug(f"PPS signal : {pps_data[entry].PpsSignal}, state : {pps_data[entry].PpsState} ")
            if pps_data[entry].PpsState == "OFF":
                logging.info(f"Driver is turning VDD OFF")
                return True

    logging.error(f"Driver is not turning VDD OFF")
    return False


##
# @brief        This function verifies VDD status from ETL report
# @param[in]    etl_file - ETL file path
# @param[in]    port - Port for which VDD status is to be verified
# @return       True if VDD turned OFF else False
def verify_vdd_status(etl_file, port):
    vdd_state = []
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate report for {0}".format(etl_file))
        return False

    pps_data = etl_parser.get_event_data(etl_parser.Events.PPS_DATA)
    if pps_data is None:
        logging.error("No PPS data found in ETL")
        return False

    for entry in range(len(pps_data)):
        if pps_data[entry].Port == port:
            if pps_data[entry].PpsSignal == "DD_VDD":
                logging.debug(f"PPS signal : {pps_data[entry].PpsSignal}, state : {pps_data[entry].PpsState}")
                vdd_state.append(pps_data[entry].PpsState)

    if reboot_helper.is_reboot_scenario() is True and len(vdd_state) == 0:
        logging.info(f"Driver is turning VDD OFF")
        return True
    elif reboot_helper.is_reboot_scenario() is False and vdd_state[-1] == "OFF":
        logging.info(f"Driver is turning VDD OFF")
        return True
    else:
        logging.error(f"Driver is not turning VDD OFF")
        return False


##
# @brief         API to stop existing ETL
# @param[in]     file_name_after_stopping_etl string, name which needs to be updated after stopping existing ETL
# @return        status, stopped_etl, True if successful, False otherwise
def stop_existing_etl(file_name_after_stopping_etl: str = "GfxTrace"):
    html.step_start("Stopping existing ETL tracer")
    # Stop existing ETL
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("\tFAILED to stop existing ETL Tracer")
        return False, None
    logging.info("\tSuccessfully stopped existing ETL Tracer")

    etl_file = etl_tracer.GFX_BOOT_TRACE_ETL_FILE if reboot_helper.is_reboot_scenario() is True else etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_file) is False:
        logging.error(etl_file + " NOT found.")
        return False, None

    stopped_etl = os.path.join(test_context.LOG_FOLDER, file_name_after_stopping_etl + '.' + str(time.time()) + ".etl")
    os.rename(etl_file, stopped_etl)
    logging.info(f"\tSuccessfully renamed ETL file to {stopped_etl}")
    return True, stopped_etl
