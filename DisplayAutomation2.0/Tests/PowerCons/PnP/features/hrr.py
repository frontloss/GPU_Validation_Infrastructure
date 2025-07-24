########################################################################################################################
# @file         hrr.py
# @brief        Contains PnP tests for hrr
# @details      PnP tests are covering 24fps video playback scenario by enabling and disabling feature
#               * this test compares C0 residency with and without hrr feature
#
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core import display_essential
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Tests.PowerCons.Functional.DMRRS import hrr, dmrrs
from Tests.PowerCons.Modules import common
from Tests.PowerCons.PnP.tools import socwatch

name = "HRR"


##
# @brief        This is helper function to enable HRR
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    dmrrs_status = dmrrs.enable(adapter)
    if dmrrs_status is False:
        return False

    hrr_status = hrr.enable(adapter)
    dut.refresh_panel_caps(adapter)
    if hrr_status is False:
        return False

    if dmrrs_status or hrr_status:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver after reg-key update")
            return False
    return True


##
# @brief        This is helper function to enable HRR
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    dmrrs_status = dmrrs.disable(adapter)
    if dmrrs_status is False:
        return False

    hrr_status = hrr.disable(adapter)
    dut.refresh_panel_caps(adapter)
    if hrr_status is False:
        return False

    if dmrrs_status or hrr_status:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver after reg-key update")
            return False
    return True


##
# @brief        This is a helper function to analyse C0 residency score in HRR with video playback
# @param[in]    workload string indicating the workload name (VIDEO/APP)
# @param[in]    good_report string, report with feature enabled
# @param[in]    bad_report string, tool report with feature disabled
# @return       status
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

    logging.info("Bad Report: {0}".format(bad_report))
    bad_c0_score = socwatch.get_metric(bad_report, 'PACKAGE_C0')
    bad_c2_score = socwatch.get_metric(bad_report, 'PACKAGE_C2')

    pnp_data = {
        "C0": good_c0_score,
        "C2": good_c2_score,
        "C8": good_c8_score,
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
        if good_c0_score < bad_c0_score:
            logging.info("\tPASS: C0 residency is less in HRR Videoplayback case {0}%".format(good_c0_score))
        else:
            error_msg = "FAIL: C0 residency is high in HRR Videoplayback case hrr enable - {0}% hrr disable {1}%".\
                format(good_c0_score, bad_c0_score)
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
        logging.info(f"{key}: HRR Enabled(W)- {round(good_pnp_data[key],4)}, "
                     f"HRR Disabled(W)- {round(bad_pnp_data[key],4)}")
        if good_pnp_data[key] > bad_pnp_data[key]:
            error_msg = f"Power regression in {key}: HRR Enabled(W)- {round(good_pnp_data[key],4)}, " \
                        f"HRR Disabled(W)- {round(bad_pnp_data[key],4)}"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status
