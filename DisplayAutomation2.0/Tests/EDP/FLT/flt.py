########################################################################################################################
# @file         flt.py
# @brief        Contains exposed API for FLT verification
# @author       Tulika
########################################################################################################################

import logging

from Libs.Core import display_essential
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm, html
from Libs.Core.machine_info import machine_info
from Libs.Core.vbt.vbt import Vbt
from Tests.PowerCons.Modules import dpcd

# GDHM header
GDHM_FLT = "[Display_Interfaces][EDP][FLT]"


##
# @brief        Exposed api that checks FLT support in DPCD
# @param[in]    panel Object
# @return       True Boolean if FLT is supported, False otherwise
def is_supported_in_panel(panel):
    max_down_spread = dpcd.MaxDownSpread(panel.target_id)
    if max_down_spread.no_aux_handshake_link_training != 1:
        return False
    logging.info(f"FLT supported in {panel.port}")
    return True


##
# @brief        Exposed api that enables and sets parameter for FastLinkTraining in VBT
# @param[in]    panel Object
# @param[in]    panel_index
# @return       flt_params Dictionary FastLinkTraining parameters if successful, False otherwise
def enable(panel, panel_index):
    flt_params = {'link_rate': 0, 'lane_count': 0, 'voltage_swing': 0, 'pre_emphasis': 0}
    supported_link_rates = [1.62, 2.7, 5.4, 2.16, 3.24, 4.32, 6.48, 8.1]
    intermediate_link_rates = [2.16, 3.24, 4.32, 6.48]
    PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
    if PLATFORM_NAME not in machine_info.PRE_GEN_14_PLATFORMS:
        intermediate_link_rates = [2.16, 2.43, 3.24, 4.32, 6.75]
    flt_data = 0
    gfx_vbt = Vbt()

    # Get link rate from DPCD
    link_rate = dpcd.get_link_rate(panel.target_id, True)
    logging.debug(f"\tLinkRate= {link_rate}")

    # For VBT version < 224, FLT is supported only for link rates <= 5.4 Gbps
    if gfx_vbt.version < 224:
        if link_rate > 5.4:
            logging.error(f"FLT is NOT supported for link rate {link_rate}")
            return False
        if link_rate in intermediate_link_rates:
            logging.error(f"FLT is NOT supported for intermediate link rate {link_rate}")
            return False

        flt_data |= supported_link_rates.index(link_rate)
        flt_params['link_rate'] = link_rate

    else:
        # Set link rate in units of 200 Hz
        gfx_vbt.block_27.eDPFastLinkTrainingDataRate[panel_index] = int(link_rate * 5000)

    # Reading DPCD for lane count( From VESA DP standard v1.3 table 2-139)
    lane_count = dpcd.MaxLaneCount(panel.target_id)
    flt_params['lane_count'] = lane_count.max_lane_count
    # OR 0 based index value with bit 4:7
    flt_data |= ((flt_params['lane_count'] - 1) << 4)
    training_lane_0_set = dpcd.TrainingLane0Set(panel.target_id)

    flt_params['voltage_swing'] = training_lane_0_set.voltage_swing_level
    # OR 0 based index value with bit 8:11
    flt_data |= (flt_params['voltage_swing'] << 8)

    flt_params['pre_emphasis'] = training_lane_0_set.pre_emphasis_level
    # OR 0 based index value with bit 12:15
    flt_data |= (flt_params['pre_emphasis'] << 12)

    gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt = 1 << panel_index
    gfx_vbt.block_27.FastLinkParametersEntry[panel_index] = flt_data

    if gfx_vbt.version < 224:
        logging.info(
            f"FltParameters: PanelIndex= {panel_index}, FastLinkTrainingDataRate= {flt_data}, "
            f"IsFastLinkTrainingEnabledInVbt= {gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt}")
    else:
        logging.info(
            f"FltParameters: PanelIndex= {panel_index}, FastLinkParametersEntry= {flt_data}, "
            f"IsFastLinkTrainingEnabledInVbt= {gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt}, "
            f"FastLinkTrainingDataRate= {gfx_vbt.block_27.eDPFastLinkTrainingDataRate[panel_index]}")

    if gfx_vbt.apply_changes() is False:
        logging.error("FAILED to apply VBT changes")
        return False

    # Restarting driver to reflect changes
    result, reboot_required = display_essential.restart_gfx_driver()
    if result is False:
        logging.error("\tFailed to restart display driver(Test Issue)")
        return False
    gfx_vbt.reload()

    if gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt & (1 << panel_index) != 1 << panel_index:
        logging.error("FastLinkTraining NOT enabled in VBT")
        return False

    return flt_params


##
# @brief        Exposed api to disable FLT in VBT
# @param[in]    panel_index
# @return       True Boolean if FLT is disabled else False
def disable(panel_index):
    gfx_vbt = Vbt()
    # If FLT is already disabled for selected panel, do nothing else disable
    if gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt & (1 << panel_index) != 0:
        gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt = 0
        if gfx_vbt.apply_changes() is False:
            logging.error("FAILED to apply VBT changes")
            return False

        ##
        # Restarting driver to reflect changes
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver(Test Issue)")
            return False
        gfx_vbt.reload()
        if gfx_vbt.block_27.IsFastLinkTrainingEnabledInVbt & (1 << panel_index) != 0:
            logging.error("FastLinkTraining NOT disabled in VBT")
            return False
    return True


##
# @brief        Exposed API to verify FLT  in any given ETL file
# @param[in]    panel Object
# @param[in]    etl_file Filepath complete path to etl file
# @param[in]    is_flt_enabled Boolean True if FLT enabled, else False
# @param[in]    is_flt_expected Boolean True if FLT is expected, else False
# @return       status Boolean True if verification is successful, else False
def verify(panel, etl_file, is_flt_enabled, is_flt_expected):
    html.step_start(f"Checking ModeSet to verify FLT for {panel.port}")

    # Generate reports from ETL file using EtlParser
    if etl_parser.generate_report(etl_file) is False:
        logging.error("FAILED to generate EtlParser report")
        html.step_end()
        return False

    # There should be at least one Full Mode Set in ETL to verify link training
    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN)
    if ddi_output is None:
        logging.error("No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        html.step_end()
        gdhm.report_driver_bug_di(f"{GDHM_FLT} No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False

    # There could be multiple mode set calls from OS during power event (un-init call before going to power event,
    # init call after power event etc). Consider the last mode set entry for verification.
    ddi_data = ddi_output[-1]

    # Get all SetTiming events that happened during last DDI_SETTIMINGSFROMVIDPN call
    set_timing_output = etl_parser.get_event_data(
        etl_parser.Events.SET_TIMING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)

    if set_timing_output is None:
        logging.error("No SetTiming event found")
        html.step_end()
        gdhm.report_driver_bug_di(f"{GDHM_FLT} SetTiming event not found in ETLs to verify FLT")
        return False

    # All FLT tests are targeted with SINGLE eDP case, hence there should be only one SetTiming event
    if len(set_timing_output) > 1:
        logging.warning("\tMore than one SetTiming event entries found")

    set_timing_data = set_timing_output[-1]
    logging.debug(f"\tSet Timing Data= {set_timing_data}")

    # Check for any LinkTraining function call
    link_training_output = etl_parser.get_function_data(
        etl_parser.Functions.DP_FULL_LINK_TRAINING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)
    logging.debug(f"\tLink Training Output: {link_training_output}")
    flt_output = etl_parser.get_function_data(
        etl_parser.Functions.DP_FLT, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)
    logging.debug(f"\tFLT Output: {flt_output}")

    # If there is no link training event present in ETL, it means driver followed FMS path
    # Full mode set is required to verify link training. In this case, return False.
    if link_training_output is None and flt_output is None:
        modeset_status = etl_parser.get_event_data(etl_parser.Events.FMS_STATUS_INFO)
        if modeset_status is None:
            logging.error("Modeset status NOT found in ETL")
            gdhm.report_driver_bug_di(f"{GDHM_FLT} Modeset status not found in ETL.")
            return False
        for data in modeset_status:
            logging.info(f"\tFms Status= {data.Status}")
            if data.Status == "DD_FMS_SUCCESS" and data.TargetId == panel.target_id:
                logging.error(f"FAIL: ModeSet Expected= FullModeSet, Actual= FMS")
                gdhm.report_driver_bug_di(f"{GDHM_FLT} FastLinkTraining Failed, driver is following FMS path")
                return False

    logging.info(f"PASS: ModeSet Expected= FullModeSet, Actual= FullModeSet")

    status = get_status(panel, is_flt_enabled, set_timing_data, link_training_output, flt_output, is_flt_expected)
    html.step_end()
    return status


##
# @brief        Exposed API to verify FLT given any ETL file
# @param[in]    panel Object
# @param[in]    is_flt_enabled Boolean True if FLT enabled else False
# @param[in]    set_timing_data string timing data from the etl
# @param[in]    link_training_output  string link training output from etl
# @param[in]    flt_output string fast link training output from etl
# @param[in]    is_flt_expected Boolean True if FLT is expected, else False
# @return       status Boolean True if verification is successful, else False
def get_status(panel, is_flt_enabled, set_timing_data, link_training_output, flt_output, is_flt_expected):
    html.step_start(f"Verifying FLT in the ETL for {panel.port}")
    status = True
    if link_training_output is not None and flt_output is not None:
        gdhm.report_driver_bug_di(f"{GDHM_FLT} FastLinkTraining failed and fallback to FullLinkTraining")
        logging.error("FAIL: FastLinkTraining failed and fallback to FullLinkTraining")
        html.step_end()
        return False

    # Check if any FullLinkTraining event is present
    if link_training_output is not None:
        if set_timing_data.Port == panel.port:
            if is_flt_enabled:
                if is_flt_expected:
                    logging.error("FAIL: LinkTraining status Expected= FastLinkTraining, Actual= FullLinkTraining")
                    gdhm.report_driver_bug_di(f"{GDHM_FLT} Expected= FastLinkTraining, Actual= FullLinkTraining")
                    html.step_end()
                    status = False
                else:
                    logging.info("PASS: LinkTraining status Expected= FullLinkTraining, Actual= FullLinkTraining")
            else:
                if is_flt_expected is False:
                    logging.info("PASS: LinkTraining status Expected= FullLinkTraining, Actual= FullLinkTraining")
                else:
                    logging.error("FAIL: LinkTraining status Expected= FastLinkTraining, Actual= FullLinkTraining")
                    gdhm.report_driver_bug_di(f"{GDHM_FLT} Expected= FastLinkTraining, Actual= FullLinkTraining")
                    html.step_end()
                    status = False

    # Check if FastLinkTraining event is present
    if flt_output is not None:
        if set_timing_data.Port != panel.port:
            if is_flt_enabled:
                if is_flt_expected:
                    logging.info("PASS: LinkTraining status Expected= FastLinkTraining, Actual= FastLinkTraining")
                else:
                    logging.error("FAIL: LinkTraining status Expected= FastLinkTraining, Actual= FullLinkTraining")
                    gdhm.report_driver_bug_di(f"{GDHM_FLT} Expected= FastLinkTraining, Actual= FastLinkTraining")
                    html.step_end()
                    status = False
            else:
                if is_flt_expected is False:
                    logging.info("PASS: LinkTraining status Expected= FullLinkTraining, Actual= FullLinkTraining")
                else:
                    logging.error("FAIL: LinkTraining status Expected= FullLinkTraining, Actual= FastLinkTraining")
                    gdhm.report_driver_bug_di(f"{GDHM_FLT} Expected= FullLinkTraining, Actual= FastLinkTraining")
                    html.step_end()
                    status = False
    return status


##
# @brief        Update voltage swing table selection
# @param[in]    panel_index
# @param[in]    table table selection - low or default
# @return       True if set_vswing_table is successful else False
def set_vswing_table(panel_index, table='DEFAULT'):
    logging.info(f"Setting {table} VSwing table")
    gfx_vbt = Vbt()
    table_selection = 0 if table == 'LOW' else 1

    shift = 0
    if panel_index % 2 != 0:
        shift = 3

    ##
    # VSwingPreEmphasisTableSelection
    # Bit 3:0/7:4 - based on panel index
    #               eDP Vswing Pre-emph setting table
    #               0 =  Low Power Swing setting(200 mV)
    #               1 =  Default Swing settings(400 mV)
    # https://gfxspecs.intel.com/Predator/Home/Index/20142
    logging.debug(f"\tVSwingPreEmphasisTableSelection[{int(panel_index / 2)}]= "
                  f"{hex(gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)])}")

    if (gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == table_selection:
        logging.info(f"PASS: VBT VSwingPreEmphasis Table Selection Expected= {table}, Actual= {table}")
    else:
        gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] = table_selection << shift
        if gfx_vbt.apply_changes() is False:
            logging.error("FAILED to apply VBT changes")
            return False
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\t\tFailed to disable-enable display driver")
            return False
        gfx_vbt.reload()

        ##
        # VSwingPreEmphasisTableSelection
        # Bit 3:0/7:4 - based on panel index
        #               eDP Vswing Pre-emph setting table
        #               0 =  Low Power Swing setting(200 mV)
        #               1 =  Default Swing settings(400 mV)
        # https://gfxspecs.intel.com/Predator/Home/Index/20142
        logging.debug(f"\tVSwingPreEmphasisTableSelection[{int(panel_index / 2)}]= "
                      f"{hex(gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)])}")

        if (gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == table_selection:
            logging.info(f"PASS: VBT VSwingPreEmphasis Table Selection Expected= {table}, Actual= {table}")
        else:
            logging.error(f"FAIL: VBT VSwingPreEmphasis Table Selection Expected= {table}, Actual= {table}")
            gdhm.report_driver_bug_di(f"{GDHM_FLT} VBT VSwingPreEmphasis Table Selection Failed")
            return False
    return True

