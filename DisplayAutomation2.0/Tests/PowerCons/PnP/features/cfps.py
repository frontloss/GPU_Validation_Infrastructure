########################################################################################################################
# @file         cfps.py
# @brief        Contains PnP tests for cfps
# @details      PnP tests are covering cfps game playback scenario by enabling and disabling feature
#               * this test compares hw power numbers with and without cfps feature
#
# @author       Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core.test_env import test_context
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Modules import common

name = "CFPS"


##
# @brief        This is helper function to enable cfps
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    return cfps.enable(adapter)


##
# @brief        This is helper function to disable cfps
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    return cfps.disable(adapter)


##
# @brief        This is a helper function to analyse PnP with cfps
# @param[in]    workload string indicating the workload (IDLE_DESKTOP/SCREEN_UPDATE/...)
# @param[in]    good_report
# @param[in]    bad_report
# @return       status
def analyze(workload, good_report, bad_report):
    return True


##
# @brief        This is a helper function to analyse PnP HW metrics.
# @param[in]    good_report : dictionary containing HW metrics with feature enabled
# @param[in]    bad_report  : dictionary containing HW metrics with feature disabled
# @return       status
def analyze_hw(good_report, bad_report):
    assert good_report
    assert bad_report
    status = True

    if common.PLATFORM_NAME in ['TGL', 'ICLLP']:
        good_pnp_data = {
            "BACKLIGHT": good_report[' BACKLIGHT Power (W)'],
            "VCC_IN_AUX": good_report[' VDD2_CPU Power (W)'],
            "VDD2_CPU": good_report[' VDD2_MEM Power (W)'],
            "VDD2_MEM": good_report[' VCCIN_AUX Power (W)']
        }
    else:
        good_pnp_data = {
            "VBATA_VCCCORE_IN": good_report[' VBATA_VCCCORE_IN Power (W)'],
            "VBATA_VCCGT_IN": good_report[' VBATA_VCCGT_IN Power (W)'],
            "VCC1P8_CPU": good_report[' VCC1P8_CPU Power (W)'],
            "VCC1P05_CPU": good_report[' VCC1P05_CPU Power (W)'],
            "VBATA_VCCIN_AUX_IN": good_report[' VBATA_VCCIN_AUX_IN Power (W)'],
            "VDD2_CPU": good_report[' VDD2_CPU Power (W)'],
            "VDD2_MEM": good_report[' VDD2_MEM Power (W)'],
            "V1P8U_MEM": good_report[' V1P8U_MEM Power (W)']
        }

    with open(os.path.join(test_context.LOG_FOLDER, "dashboard2_data.txt"), "w") as outfile:
        outfile.write(json.dumps(good_pnp_data, indent=4))

    if common.PLATFORM_NAME in ['TGL', 'ICLLP']:
        bad_pnp_data = {
            "BACKLIGHT": bad_report[' BACKLIGHT Power (W)'],
            "VCC_IN_AUX": bad_report[' VDD2_CPU Power (W)'],
            "VDD2_CPU": bad_report[' VDD2_MEM Power (W)'],
            "VDD2_MEM": bad_report[' VCCIN_AUX Power (W)']
        }
    else:
        bad_pnp_data = {
            "VBATA_VCCCORE_IN": bad_report[' VBATA_VCCCORE_IN Power (W)'],
            "VBATA_VCCGT_IN": bad_report[' VBATA_VCCGT_IN Power (W)'],
            "VCC1P8_CPU": bad_report[' VCC1P8_CPU Power (W)'],
            "VCC1P05_CPU": bad_report[' VCC1P05_CPU Power (W)'],
            "VBATA_VCCIN_AUX_IN": bad_report[' VBATA_VCCIN_AUX_IN Power (W)'],
            "VDD2_CPU": bad_report[' VDD2_CPU Power (W)'],
            "VDD2_MEM": bad_report[' VDD2_MEM Power (W)'],
            "V1P8U_MEM": bad_report[' V1P8U_MEM Power (W)']
        }

    for key in good_pnp_data:
        logging.info(f"{key}: CFPS Enabled(W)- {round(good_pnp_data[key], 4)}, "
                     f"CFPS Disabled(W)- {round(bad_pnp_data[key], 4)}")

    return status
