########################################################################################################################
# @file         port_sync.py
# @brief        Contains PnP tests for port_sync
# @details      PnP tests are covering Idle and 24fps video playback scenario by enabling and disabling feature
#               * this test compares PSR2 Deep sleep, Su, c10, c8, residency with and without port_sync feature
#
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import os
import logging
import json
from Libs.Core.test_env import test_context
from Libs.Core import display_essential
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.logger import gdhm
from Tests.PowerCons.Modules import dut
from Tests.PowerCons.Modules import common
from Tests.PowerCons.PnP.tools import socwatch

name = "PORT_SYNC"

# Below numbers collected from last 15 driver runs on same machine
# These numbers will change in future based on BKC installation upgrade

GOLDEN_NUMBERS = {
    'ADLP': {'C10': 0, 'Link_Off': 0, 'C8': 0, 'PSR2_SU': 0}
}


##
# @brief        This is helper function to enable port sync
# @param[in]    adapter Adapter object
# @return       True if the enabling is successful, False otherwise
def enable(adapter):
    gfx_vbt = Vbt()
    set_vbt = False
    lfp_panels = []
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            if panel.is_lfp is True:
                lfp_panels.append(panel)
    panel1_index = gfx_vbt.block_40.PanelType
    panel1_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << panel1_index)) >> panel1_index
    if panel1_port_sync_bit != 1:
        gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << panel1_index)
        set_vbt = True
    else:
        logging.info("Port sync enabled in VBT for panel1")

    if len(lfp_panels) == 2:
        panel2_index = gfx_vbt.block_40.PanelType2
        panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << panel2_index)) >> panel2_index
        if panel2_port_sync_bit != 1:
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << panel2_index)
            set_vbt = True
        else:
            logging.info("Port sync enabled in VBT for panel2")

    if set_vbt is True:
        if gfx_vbt.apply_changes() is False:
            logging.error('Setting VBT block 52 failed')
            return False
        else:
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart driver")
                return False
            gfx_vbt.reload()
            logging.info("Port sync enabled in VBT for panel1")
            logging.info("Port sync enabled in VBT for panel2")
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("Failed to restart driver")


##
# @brief        This is helper function to disable port sync
# @param[in]    adapter Adapter object
# @return       True if the disabling is successful, False otherwise
def disable(adapter):
    gfx_vbt = Vbt()
    set_vbt = False
    lfp_panels = []
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            if panel.is_lfp is True:
                lfp_panels.append(panel)
    panel1_index = gfx_vbt.block_40.PanelType
    panel1_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << panel1_index)) >> panel1_index
    if panel1_port_sync_bit != 0:
        gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits & ~(1 << panel1_index)
        set_vbt = True
    else:
        logging.info("Port sync enabled in VBT for panel1")

    if len(lfp_panels) == 2:
        panel2_index = gfx_vbt.block_40.PanelType2
        panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << panel2_index)) >> panel2_index
        if panel2_port_sync_bit != 0:
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits & ~(1 << panel2_index)
            set_vbt = True
        else:
            logging.info("Port sync enabled in VBT for panel2")

    if set_vbt is True:
        if gfx_vbt.apply_changes() is False:
            logging.error('Setting VBT block 52 failed')
            return False
        else:
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart driver")
                return False
            gfx_vbt.reload()
            logging.info("Port sync enabled in VBT for panel1")
            logging.info("Port sync enabled in VBT for panel2")
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("Failed to restart driver")


##
# @brief        This is a helper function to analyse PnP with port sync
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
            logging.error("\tFAIL: System is not in PSR2 deep sleep state in idle state Actual {0} expected {1}".
                          format(psr2_deep_sleep, GOLDEN_NUMBERS[common.PLATFORM_NAME]['Link_Off']))
            logging.error("\tSystem in PSR2 selective update state for {0}%".format(psr2_su))
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            status = False

        if good_c10_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']:
            logging.info("\tPASS: C10 hitting in PSR2 Idle case - {0}%".format(good_c10_score))
        else:
            logging.error("\tFAIL: C10 not hitting in PSR2 Idle case - {0}% Expected {1}".format(good_c10_score,
                                                                        GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']))
            status = False

        if good_dc_state_count > 0:
            logging.info("\tPASS: System is entering into DC states count {0}".format(good_dc_state_count))
        else:
            logging.error("\tFAIL: System is not entering into DC states")
            status = False

        if bad_c8_score > 0:
            logging.info("\tPASS: C8 hitting in Non-PSR Idle case {0}%".format(bad_c8_score))
        else:
            logging.error("\tFAIL: C8 is not hitting in Non-PSR Idle case {0}%".format(bad_c8_score))
            status = False

    if workload == 'SCREEN_UPDATE':
        if psr2_deep_sleep > GOLDEN_NUMBERS[common.PLATFORM_NAME]['Link_Off']:
            logging.info("\tPASS: System in PSR2 deep sleep state for {0}%".format(psr2_deep_sleep))
            logging.info("\tPASS: System in PSR2 selective update state for {0}%".format(psr2_su))
            logging.info("\tPASS: System in PSR2 Link on state for {0}%".format(link_on))
        else:
            logging.error("\tFAIL: System is not in PSR2 deep sleep state in idle state Actual {0} expected {1}".
                          format(psr2_deep_sleep, GOLDEN_NUMBERS[common.PLATFORM_NAME]['Link_Off']))
            logging.error("\tSystem in PSR2 selective update state for {0}%".format(psr2_su))
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            status = False

        if good_c10_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']:
            logging.info("\tPASS: C10 hitting in PSR2 screen update case - {0}%".format(good_c10_score))
        else:
            logging.error("\tFAIL: C10 not hitting in PSR2 screen update case - {0}% Expected {1}".format(good_c10_score,
                                                                        GOLDEN_NUMBERS[common.PLATFORM_NAME]['C10']))
            status = False

        if good_dc_state_count > 0:
            logging.info("\tPASS: System is entering into DC states count {0}".format(good_dc_state_count))
        else:
            logging.error("\tFAIL: System is not entering into DC states")
            status = False

        if bad_c8_score > 0:
            logging.info("\tPASS: C8 hitting in Non-PSR screen update case {0}%".format(bad_c8_score))
        else:
            logging.error("\tFAIL: C8 is not hitting in Non-PSR screen update case {0}%".format(bad_c8_score))
            status = False

    if workload == 'VIDEO':
        if psr2_su > GOLDEN_NUMBERS[common.PLATFORM_NAME]['PSR2_SU']:
            logging.info("\tPASS: System in PSR2 selective update state for {0}%".format(psr2_su))
            logging.info("\tPASS: System in PSR2 Link on state for {0}%".format(link_on))
        else:
            logging.error("\tSystem in PSR2 selective update state for {0}% Expected {1}".
                          format(psr2_su, GOLDEN_NUMBERS[common.PLATFORM_NAME]['PSR2_SU']))
            logging.error("\tSystem in PSR2 Link on state for {0}%".format(link_on))
            status = False

        if good_c8_score > GOLDEN_NUMBERS[common.PLATFORM_NAME]['C8']:
            logging.info("\tPASS: C8 hitting in PSR2 video playback {0}%".format(good_c8_score))
        else:
            logging.error("\tFAIL: C8 is not hitting in PSR2 video playback {0}% Expected {1}%".format(good_c8_score,
                                                                        GOLDEN_NUMBERS[common.PLATFORM_NAME]['C8']))
            status = False

        # @todo: Need to add BW after socwatch fix

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
        logging.info(f"{key}: PortSync Enabled(W)- {round(good_pnp_data[key],4)}, "
                     f"PortSync Disabled(W)- {round(bad_pnp_data[key],4)}")
        if good_pnp_data[key] > bad_pnp_data[key]:
            error_msg = f"Power regression in {key}: PortSync Enabled(W)- {round(good_pnp_data[key],4)}, " \
                        f"PortSync Disabled(W)- {round(bad_pnp_data[key],4)}"
            logging.error(error_msg)
            gdhm.report_bug(
                title="[PnP]"+error_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    return status
