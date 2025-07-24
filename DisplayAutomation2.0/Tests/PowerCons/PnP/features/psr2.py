########################################################################################################################
# @file         psr2.py
# @brief        Contains PnP tests for psr2
# @details      PnP tests are covering Idle and 24fps video playback scenario by enabling and disabling feature
#               * this test compares PSR2 Deep sleep, Su, c10, c8, residency with and without psr2 feature
#
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core import display_essential
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common
from Tests.PowerCons.PnP.tools import socwatch

name = "PSR2"

# Below numbers collected from last 15 driver runs on same machine
# These numbers will change in future based on BKC installation upgrade

GOLDEN_NUMBERS = {
    'ICLLP': {'C10': 0, 'Link_Off': 0, 'C8': 0, 'PSR2_SU': 0},
    'TGL': {'C10': 0, 'Link_Off': 0, 'C8': 0, 'PSR2_SU': 0},
    'ADLP': {'C10': 0, 'Link_Off': 0, 'C8': 0, 'PSR2_SU': 0}
}


##
# @brief        This is helper function to enable psr2
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
    if status is False:
        return False
    if status is True:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            return False
    return True


##
# @brief        This is helper function to disable psr2
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
    if psr_status is False:
        return False
    psr2_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
    if psr2_status is False:
        return False
    if psr_status or psr2_status:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            return False
    return True


##
# @brief        This is a helper function to analyse PnP with psr2
# @param[in]    workload string indicating the workload (IDLE_DESKTOP/SCREEN_UPDATE/...)
# @param[in]    good_report
# @param[in]    bad_report
# @return       status
def analyze(workload, good_report, bad_report):
    assert good_report
    assert bad_report

    status = True

    logging.info("Step: Analyzing reports for {0}".format(name))

    logging.info("Good Report: {0}".format(good_report))
    good_dc_state_count = socwatch.get_metric(good_report, 'DC_STATE_COUNT')
    good_c0_score = socwatch.get_metric(good_report, 'PACKAGE_C0')
    good_c2_score = socwatch.get_metric(good_report, 'PACKAGE_C2')
    good_c8_score = socwatch.get_metric(good_report, 'PACKAGE_C8')
    good_c10_score = socwatch.get_metric(good_report, 'PACKAGE_C10')
    link_on = socwatch.get_metric(good_report, 'LINK_ON')
    psr2_su = socwatch.get_metric(good_report, 'PSR2_SU')
    psr2_deep_sleep = socwatch.get_metric(good_report, 'PSR2_DEEP_SLEEP')
    good_io_requests = socwatch.get_metric(good_report, 'IO_READS') + socwatch.get_metric(good_report, 'IO_WRITES')

    logging.info("Bad Report: {0}".format(bad_report))
    bad_c0_score = socwatch.get_metric(bad_report, 'PACKAGE_C0')
    bad_c2_score = socwatch.get_metric(bad_report, 'PACKAGE_C2')
    bad_c8_score = socwatch.get_metric(bad_report, 'PACKAGE_C8')
    bad_io_requests = socwatch.get_metric(bad_report, 'IO_READS') + socwatch.get_metric(bad_report, 'IO_WRITES')

    pnp_data = {
        "C0": good_c0_score,
        "C2": good_c2_score,
        "C8": good_c8_score,
        "C10": good_c10_score,
        "link_on": link_on,
        "psr2_su": psr2_su,
        "deep_sleep": psr2_deep_sleep,
    }
    json_obj = json.dumps(pnp_data, indent=4)
    with open("dashboard_data.txt", "w") as outfile:
        outfile.write(json_obj)

    pnp_log_file_path = os.path.join(os.getcwd(), "dashboard_data.txt")

    report_path = os.path.join(test_context.LOG_FOLDER, "dashboard_data.txt")
    if os.path.exists(pnp_log_file_path) is False:
        logging.error("{0} not found".format(pnp_log_file_path))

    os.rename(pnp_log_file_path, report_path)

    if workload == 'IDLE':
        if psr2_deep_sleep > GOLDEN_NUMBERS[common.PLATFORM_NAME]['Link_Off']:
            logging.info("\tPASS: System in PSR2 deep sleep state for {0}%".format(psr2_deep_sleep))
            logging.info("\tPASS: System in PSR2 selective update state for {0}%".format(psr2_su))
            logging.info("\tPASS: System in PSR2 Link on state for {0}%".format(link_on))
        else:
            error_msg = "FAIL: System is not in PSR2 deep sleep state in idle state {0}".format(psr2_deep_sleep)
            logging.error(error_msg)
            logging.error("\tSystem in PSR2 selective update state for {0}%".format(psr2_su))
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if good_c10_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']:
            logging.info("\tPASS: C10 hitting in PSR2 Idle case - {0}%".format(good_c10_score))
        else:
            error_msg = "FAIL: C10 not hitting in PSR2 Idle case - {0}%".format(good_c10_score)
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if good_dc_state_count > 0:
            logging.info("\tPASS: System is entering into DC states count {0}".format(good_dc_state_count))
        else:
            error_msg = "FAIL: System is not entering into DC states"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if bad_c8_score > 0:
            logging.info("\tPASS: C8 hitting in Non-PSR Idle case {0}%".format(bad_c8_score))
        else:
            error_msg = "FAIL: C8 is not hitting in Non-PSR Idle case {0}%".format(bad_c8_score)
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    if workload == 'SCREEN_UPDATE':
        if psr2_deep_sleep > GOLDEN_NUMBERS[common.PLATFORM_NAME]['Link_Off']:
            logging.info("\tPASS: System in PSR2 deep sleep state for {0}%".format(psr2_deep_sleep))
            logging.info("\tPASS: System in PSR2 selective update state for {0}%".format(psr2_su))
            logging.info("\tPASS: System in PSR2 Link on state for {0}%".format(link_on))
        else:
            error_msg = "FAIL: System is not in PSR2 deep sleep state in idle state Actual {0}". format(psr2_deep_sleep)
            logging.error(error_msg)
            logging.error("\tSystem in PSR2 selective update state for {0}%".format(psr2_su))
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if good_c10_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']:
            logging.info("\tPASS: C10 hitting in PSR2 screen update case - {0}%".format(good_c10_score))
        else:
            error_msg = "FAIL: C10 not hitting in PSR2 screen update case - {0}%".format(good_c10_score)
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if good_dc_state_count > 0:
            logging.info("\tPASS: System is entering into DC states count {0}".format(good_dc_state_count))
        else:
            error_msg = "FAIL: System is not entering into DC states"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if bad_c8_score > 0:
            logging.info("\tPASS: C8 hitting in Non-PSR screen update case {0}%".format(bad_c8_score))
        else:
            error_msg = "FAIL: C8 is not hitting in Non-PSR screen update case {0}%".format(bad_c8_score)
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    if workload == 'VIDEO':
        if psr2_su > GOLDEN_NUMBERS[common.PLATFORM_NAME]['PSR2_SU']:
            logging.info("\tPASS: System in PSR2 selective update state for {0}%".format(psr2_su))
            logging.info("\tPASS: System in PSR2 Link on state for {0}%".format(link_on))
        else:
            error_msg = "System in PSR2 selective update state for {0}%".format(psr2_su)
            logging.error(error_msg)
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        if good_c8_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C8']:
            logging.info("\tPASS: C8 hitting in PSR2 video playback {0}%".format(good_c8_score))
        else:
            error_msg = "FAIL: C8 is not hitting in PSR2 video playback {0}%".format(good_c8_score)
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
        logging.info(f"{key}: PSR2 Enabled(W)- {round(good_pnp_data[key],4)}, "
                     f"PSR2 Disabled(W)- {round(bad_pnp_data[key],4)}")
        if good_pnp_data[key] > bad_pnp_data[key]:
            error_msg = f"Power regression in {key}: PSR2 Enabled(W)- {round(good_pnp_data[key],4)}, " \
                        f"PSR2 Disabled(W)- {round(bad_pnp_data[key],4)}"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status
