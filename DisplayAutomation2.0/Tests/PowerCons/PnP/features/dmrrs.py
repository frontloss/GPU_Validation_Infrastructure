########################################################################################################################
# @file         dmrrs.py
# @brief        Contains PnP tests for dmrrs
# @details      PnP tests are covering 24fps video playback scenario by enabling and disabling feature
#               * this test compares C2 residency with and without DMRRS feature
#
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core import display_essential
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Modules import common
from Tests.PowerCons.PnP.tools import socwatch

name = "DMRRS"


##
# @brief        This is helper function to enable DMRRS
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    status = dmrrs.enable(adapter)
    if status is False:
        return False
    if status is True:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            return False
    return True


##
# @brief        This is helper function to disable DMRRS
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    status = dmrrs.disable(adapter)
    if status is False:
        return False
    if status is True:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            return False
    return True


##
# @brief        This is helper function to analyse C2 residency score in DMRRS Videoplayback case
# @param[in]    workload string indicating the workload name (VIDEO/APP)
# @param[in]    good_report
# @param[in]    bad_report
# @return       status False if  C2 residency is high in DMRRS Video playback case, True otherwise
def analyze(workload, good_report, bad_report):
    assert workload
    assert good_report
    assert bad_report

    status = True

    logging.info("Step: Analyzing reports for {0}".format(name))

    logging.info("Good Report: {0}".format(good_report))
    good_c0_score = socwatch.get_metric(good_report, 'PACKAGE_C0')
    good_c2_score = socwatch.get_metric(good_report, 'PACKAGE_C2')
    good_c8_score = socwatch.get_metric(good_report, 'PACKAGE_C8')
    good_c10_score = socwatch.get_metric(good_report, 'PACKAGE_C10')

    logging.info("Bad Report: {0}".format(bad_report))
    bad_c2_score = socwatch.get_metric(bad_report, 'PACKAGE_C2')

    pnp_data = {
        "C0": good_c0_score,
        "C2": good_c2_score,
        "C8": good_c8_score,
        "C10": good_c10_score,
    }

    json_obj = json.dumps(pnp_data, indent=4)
    with open("dashboard_data.txt", "w") as outfile:
        outfile.write(json_obj)

    pnp_log_file_path = os.path.join(os.getcwd(), "dashboard_data.txt")

    report_path = os.path.join(test_context.LOG_FOLDER, "dashboard_data.txt")
    if os.path.exists(pnp_log_file_path) is False:
        logging.error("{0} not found".format(pnp_log_file_path))

    os.rename(pnp_log_file_path, report_path)

    if workload == 'VIDEO':
        if good_c2_score < bad_c2_score:
            logging.info("\tPASS: C2 residency is less in DMRRS Videoplayback case {0}%".format(good_c2_score))
        else:
            error_msg = "FAIL: C2 residency is high in DMRRS Videoplayback case {0}%".format(good_c2_score)
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status


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
        logging.info(f"{key}: DMRRS Enabled(W)- {round(good_pnp_data[key],4)}, "
                     f"DMRRS Disabled(W)- {round(bad_pnp_data[key],4)}")
        if good_pnp_data[key] > bad_pnp_data[key]:
            error_msg = f"Power regression in {key}: DMRRS Enabled(W)- {round(good_pnp_data[key],4)}, " \
                        f"DMRRS Disabled(W)- {round(bad_pnp_data[key],4)}"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status
