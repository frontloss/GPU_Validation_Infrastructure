########################################################################################################################
# @file         fms.py
# @addtogroup   EDP
# @section      FMS_Libs
# @brief        This file contians API's for FMS tests on eDP
#
# @author       Bhargav Adigarla, Rohit Kumar
########################################################################################################################

import logging

from Libs.Core import enum, registry_access, display_essential
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import common


##
# @brief        This is a helper function to change FMS setting
# @param[in]    reg_value Number, registry value
# @return       status, Boolean, True if operation is successful, False otherwise
def __change_fms(reg_value):
    status = registry.write(
        "gfx_0", registry.RegKeys.FMS.DISPLAY_OPTIMIZATION, registry_access.RegDataType.DWORD, reg_value)
    if status is False:
        logging.error("\tFailed to update {0} in registry(Test Issue)".format(
            registry.RegKeys.FMS.DISPLAY_OPTIMIZATION))
        return False
    result, reboot_required = display_essential.restart_gfx_driver()
    if status and result is False:
        logging.error("\tFailed to restart display driver(Test Issue)")
        return False
    return True


##
# @brief        Exposed API to enable FMS
# @return       status, Boolean, True if operation is successful, False otherwise
# @note         FMS is always enabled in Yangra and can not be disabled using registry key
def enable():
    if common.IS_DDRW:
        return True
    return __change_fms(registry.RegValues.FMS.ENABLED)


##
# @brief        Exposed API to disable FMS
# @return       status, Boolean, True if operation is successful, False otherwise
def disable():
    if common.IS_DDRW:
        return False
    return __change_fms(registry.RegValues.FMS.DISABLED)


##
# @brief        Exposed API to verify FLT given any ETL file
# @param[in]    etl_file FilePath, complete path to etl file
# @param[in]    fms_config list of boolean values
# @return       Boolean, True if verification is successful, False otherwise
def verify(etl_file, fms_config):
    status = True

    ##
    # Generate reports from ETL file using EtlParser
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False

    if common.IS_DDRW:
        ##
        # There should be at least one mode set in ETL to verify link training
        ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN)
        if ddi_output is None:
            gdhm.report_bug(
                title="[EDP][FMS] DDI_SETTIMINGSFROMVIDPN event not found to verify FMS",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.warning("\tNo DDI_SETTIMINGSFROMVIDPN event found in ETLs (Driver Issue)")
            return False

        ##
        # There could be multiple mode set calls from OS during power event (uninit call before going to power event,
        # init call after power event etc). Consider the last mode set entry for verification.
        ddi_data = ddi_output[-1]

        set_timing_output = etl_parser.get_event_data(
            etl_parser.Events.SET_TIMING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)

        if set_timing_output is None:
            gdhm.report_bug(
                title="[EDP][FMS] SetTiming event not found to verify FMS",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.warning("\tNo SetTiming event found in ETLs(Driver Issue)")

        ##
        # All FLT tests are targeted with SINGLE eDP case, hence there should be only one SetTiming event
        if len(set_timing_output) > 1:
            logging.warning("\tMore than one SetTiming event entries found")

        set_timing_data = set_timing_output[-1]
        logging.info("\t{0}".format(set_timing_data))

        link_training_output = etl_parser.get_function_data(
            etl_parser.Functions.DP_FULL_LINK_TRAINING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)
        flt_output = etl_parser.get_function_data(
            etl_parser.Functions.DP_FLT, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)

        ##
        # If there is no link training event present in ETL, it means driver followed FMS path
        if link_training_output is None and flt_output is None:
            logging.info("\tPASS: ModeSet Expected= FastModeSet, Actual= FastModeSet[{0}ms]".format(
                ddi_data.ExecTime))
            return True
        status = False
        gdhm.report_bug(
            title="[EDP][FMS] FastModeSet verification failed",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.info("\tFAIL: ModeSet Expected= FastModeSet, Actual= FullModeSet[{0}ms] (Driver Issue)".
                     format(ddi_data.ExecTime))
    else:
        ##
        # There should be at least one mode set in ETL to verify link training
        mode_set_output = etl_parser.get_event_data(etl_parser.Events.MSG)
        if mode_set_output is None:
            gdhm.report_bug(
                title="[EDP][FMS] SetTiming event not found to verify FMS",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.warning("\tNo SetTiming event found in ETLs (Driver Issue)")
            return False
        mode_set_count = 0
        mode_set_data = []
        for msg in mode_set_output:
            if "GfxParserDxgkDdiSetTimingsFromVidPn" in msg:
                logging.debug("\t{0}".format(msg))
                mode_set_data.append([_.split("=") for _ in msg.split(":")[1].split(",")])
                mode_set_count += 1

        if mode_set_count != 1:
            if mode_set_count == 0:
                logging.warning("\tNo SetTiming event found in ETLs (Driver Issue)")
                return False
            logging.warning("\tModeSet count Expected= 1, Actual= {0}".format(mode_set_count))
        mode_set_data = mode_set_data[-1]

        ##
        # Get Full Link Training event data
        link_training_output = etl_parser.get_event_data(etl_parser.Events.DP_LINK_TRAINING)

        ##
        # Get FLT event data
        flt_output = etl_parser.get_event_data(etl_parser.Events.DP_FAST_LINK_TRAINING)

        ##
        # If there is no link training event present in ETL, it means driver followed FMS path
        # Full mode set is required to verify link training
        if link_training_output is None and flt_output is None:
            if len(mode_set_data) > 2:
                logging.info(
                    "\tPASS: ModeSet Expected= FastModeSet, Actual= FastModeSet[{0}ms]".format(mode_set_data[2][1]))
                return True
            else:
                logging.info("\tPASS: ModeSet Expected= FastModeSet, Actual= FastModeSet")
                return True
        else:
            if len(mode_set_data) > 2:
                logging.error(
                    "\tFAIL: ModeSet Expected= FastModeSet, Actual= FullModeSet[{0}ms] (Driver Issue)".format(
                        mode_set_data[2][1]))
                status = False
                gdhm.report_bug(
                    title="[EDP][FMS] FastModeSet verification failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )

            else:
                logging.error("\tFAIL: ModeSet Expected= FastModeSet, Actual= FullModeSet[{0}ms] (Driver Issue)")
                gdhm.report_bug(
                    title="[EDP][FMS] FastModeSet verification failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )

                status = False
    return status
