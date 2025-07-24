#######################################################################################################################
# @file         super_wet_ink.py
# @brief        APIs to verify superWetInk behavior
#
# @author       Nivetha B
#######################################################################################################################

import logging
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm
from Libs.Feature.display_watermark import watermark as wm
from DisplayRegs.DisplayOffsets import PsrOffsetValues
from Tests.PowerCons.Modules import dut

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.functionData = 1
ETL_PARSER_CONFIG.psrData = 1


##
# @brief        Exposed API to verify SuperWetInk
# @param[in]    adapter - Adapter target adapter object
# @param[in]    panel - panel to verify superWetInk
# @param[in]    etl_file - etl_file to verify superWetInk
# @return       True if operation is successful, False otherwise
def verify(adapter, panel, etl_file):
    status = True
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate ETL report")
        return False
    status &= __check_psr_status(adapter, panel)
    status &= __check_min_dbuf_status()
    return status


##
# @brief        Verification of superWetInk behavior
# @param[in]    etl_file - etl_file for verification of superWetInk
# @return       status : True/False
def validate_superwetink(etl_file):
    status = True
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            if not verify(adapter, panel, etl_file):
                logging.error(f"Verification of superWetInk failed")
                status = False
    return status


##
# @brief        Helper function to get UMD escape call active period time stamps from ETL
# @return       a list of tuples (umd_active_start_time_stamp, umd_active_end_time_stamp) if UMD escape entry/exit
#               trace events are present in ETL, None otherwise
def get_umd_event_data():
    output = []

    fbr_escape_call = etl_parser.get_psr_event_data(etl_parser.Events.DISPLAY_PC_PSR_PR_PROCESS)
    if fbr_escape_call is None:
        logging.error("No FBR change escape call event found in ETL. SuperWetInk is not enabled")
        gdhm.report_driver_bug_os("No FBR change escape call event found in ETL. SuperWetInk is not enabled")
        return False

    # Filtering out FBR enabled and disabled cases
    enable_event_data = [_ for _ in fbr_escape_call if _.Operation == "DISPLAY_PC_OPERATION_EVENT_FBR_EVENT" and
                         _.Field1 == 1]

    disable_event_data = [_ for _ in fbr_escape_call if _.Operation == "DISPLAY_PC_OPERATION_EVENT_FBR_EVENT" and
                          _.Field1 == 0]

    for enable_event in range(len(enable_event_data)):
        time_stamp = None
        for disable_event in disable_event_data:
            if enable_event < len(enable_event_data) - 1:
                if enable_event_data[enable_event].TimeStamp < disable_event.TimeStamp < \
                        enable_event_data[enable_event + 1].TimeStamp:
                    if time_stamp is None:
                        time_stamp = disable_event.TimeStamp
                    break
            else:
                if enable_event_data[enable_event].TimeStamp < disable_event.TimeStamp:
                    if time_stamp is None:
                        time_stamp = disable_event.TimeStamp
                    break

        if time_stamp is not None:
            output.append((enable_event_data[enable_event].TimeStamp, time_stamp))

    logging.info(f"FBR enable escape call event found at {output}")

    return output


##
# @brief        Helper API to verify PSR status during UMD escape call active period
# @param[in]    adapter - Adapter
# @param[in]    panel - Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_psr_status(adapter, panel):
    status = True
    gdhm_error_msg = None
    psr_mmio_ctl_output = None
    psr_reg = None
    logging.info("\tVerifying PSR status")
    if not panel.psr_caps.is_psr_supported:
        logging.info(f"PSR is not supported by the panel")
        return status
    umd_active_period = get_umd_event_data()
    if umd_active_period is None:
        logging.error("\t\tNo UMD escape call found in ETL")
        return False

    psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
    for umd_active_start, umd_active_end in umd_active_period:
        if panel.psr_caps.psr_version == 1:
            # get the mmio offsets for PSR1 SRD CTL register
            psr_mmio_ctl_output = etl_parser.get_mmio_data(psr_regs.SrdCtlReg, is_write=True,
                                                           start_time=umd_active_start, end_time=umd_active_end)
            psr_reg = f"SRD_CTL_{panel.transcoder}"

        if panel.psr_caps.psr_version == 2:
            # get the mmio offsets for PSR2 CTL register
            psr_mmio_ctl_output = etl_parser.get_mmio_data(psr_regs.Psr2CtrlReg, is_write=True,
                                                           start_time=umd_active_start, end_time=umd_active_end)
            psr_reg = f"PSR2_CTL_{panel.transcoder}"

        if psr_mmio_ctl_output is None:
            logging.info(f"No MMIO output found for {psr_reg}")
        else:
            for mmio_data in psr_mmio_ctl_output:
                offset = PsrOffsetValues(SrdCtlReg=mmio_data.Data) if panel.psr_caps.psr_version == 1 else \
                    PsrOffsetValues(Psr2CtrlReg=mmio_data.Data)
                psr_info = adapter.regs.get_psr_info(panel.transcoder_type, offset)
                reg_status = psr_info.SrdEnable if panel.psr_caps.psr_version == 1 else psr_info.Psr2Enable
                if reg_status:
                    logging.error(f"{psr_reg} = {mmio_data.Data} at {mmio_data.TimeStamp}"
                                  f" 31st bit Expected= Disabled, Actual= Enabled")
                    gdhm_error_msg = f"[OsFeatures][VRR] PSR status:Expected= Disabled, Actual= Enabled"
                    status = False

    if status is False:
        gdhm.report_driver_bug_os(title=gdhm_error_msg)
    return status


##
# @brief        Helper API to verify PSR status during UMD escape call active period
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_min_dbuf_status():
    logging.info("\tVerifying min DBuf status")
    if not wm.DisplayWatermark().verify_watermarks(gfx_index="gfx_0", min_dbuf_check=True):
        logging.error('FAIL : Min DBuf requirements are not met!')
        return False
    logging.info('Min DBuf requirements are met')
    return True
