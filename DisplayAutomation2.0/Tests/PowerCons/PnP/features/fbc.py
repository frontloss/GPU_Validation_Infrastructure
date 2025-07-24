########################################################################################################################
# @file         fbc.py
# @brief        Contains PnP tests for fbc
# @details      PnP tests are covering Idle scenario by enabling and disabling feature
#               * this test compares IO BW, HW pnp numbers with and without FBC feature
#
# @author       Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core import display_essential
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Functional.PSR import psr
from Libs.Feature.display_fbc import fbc
from Tests.PowerCons.PnP.tools import socwatch

name = "FBC"


##
# @brief        This is helper function to enable fbc
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
    if psr_status is False:
        return False
    if psr_status is True:
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            return False
    return fbc.enable(adapter.gfx_index)


##
# @brief        This is helper function to disable fbc
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    return fbc.disable(adapter.gfx_index)


##
# @brief        This is a helper function to analyse PnP data
# @param[in]    workload string indicating the workload (IDLE_DESKTOP/SCREEN_UPDATE/...)
# @param[in]    good_report
# @param[in]    bad_report
# @return       status
def analyze(workload, good_report, bad_report):
    assert workload
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
    good_io_requests = socwatch.get_metric(good_report, 'IO_READS') + socwatch.get_metric(good_report, 'IO_WRITES')

    logging.info("Bad Report: {0}".format(bad_report))
    bad_dc_state_count = socwatch.get_metric(bad_report, 'DC_STATE_COUNT')
    bad_c0_score = socwatch.get_metric(bad_report, 'PACKAGE_C0')
    bad_c2_score = socwatch.get_metric(bad_report, 'PACKAGE_C2')
    bad_c8_score = socwatch.get_metric(bad_report, 'PACKAGE_C8')
    bad_io_requests = socwatch.get_metric(bad_report, 'IO_READS') + socwatch.get_metric(bad_report, 'IO_WRITES')

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

    if good_io_requests < bad_io_requests:
        logging.info(f"\tPASS: IO Bandwidth is more in FBC enabled case - {good_io_requests}%")
    else:
        error_msg = f"\tFAIL: IO Bandwidth is less in FBC enabled case - {good_io_requests}%"
        logging.error(error_msg)
        gdhm.report_bug(
            title="[PnP]" + error_msg,
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
        logging.info(f"{key}: FBC Enabled(W)- {round(good_pnp_data[key],4)}, "
                     f"FBC Disabled(W)- {round(bad_pnp_data[key],4)}")
        if good_pnp_data[key] > bad_pnp_data[key]:
            error_msg = f"Power regression in {key}: FBC Enabled(W)- {round(good_pnp_data[key],4)}, " \
                        f"FBC Disabled(W)- {round(bad_pnp_data[key],4)}"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status
