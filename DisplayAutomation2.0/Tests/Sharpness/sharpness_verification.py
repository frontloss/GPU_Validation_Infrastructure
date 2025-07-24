########################################################################################################################
# @file         sharpness_verification.py
# @brief        This script contains helper functions to verify Sharpness feature.
# @author       Prateek Joshi
########################################################################################################################
import logging

from enum import Enum, IntEnum
from Libs.Core import etl_parser
from Libs.Core.machine_info import machine_info
from registers.mmioregister import MMIORegister

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1
MAX_LINE_WIDTH = 64

ADAPTIVE_SHARPNESS_SUPPORT_PLATFORM = machine_info.GEN_15_PLATFORMS
LEGACY_SHARPNESS_SUPPORT_PLATFORM = machine_info.PRE_GEN_15_PLATFORMS
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName


##
# @brief    Enum for Tap Filters
class TapFilter(IntEnum):
    _Three = 0,
    _Five = 1,
    _Seven = 2


##
# @brief        Helper function to generate ETL report.
# @param[in]    panel             : panel object
# @param[in]    etl_file_path     : ETL file path to generate report
# @return       ps2_ctl_data, ps2_ctl_reg, sharpness_ctl_data, ps_sharpness_ctl_reg, sharpness_lut_data, \
#         ps_sharpness_lut_data_reg, sharpness_lut_index_data, ps_sharpness_lut_index_reg
# : Flip data from ETL with Register instance
def extract_etl_data(panel, etl_file_path):
    start_data = None
    scaler_data = None
    ps2_ctl_data, sharpness_ctl_data, sharpness_lut_data, sharpness_lut_index_data = None, None, None, None

    if etl_parser.generate_report(etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report [Test Issue]")
        return False

    # Get MMIO register instance for Sharpness Registers
    ps2_ctl_reg = MMIORegister.get_instance("PS_CTRL_REGISTER", f"PS_CTRL_2_{panel.pipe}", PLATFORM_NAME)
    ps_sharpness_ctl_reg = MMIORegister.get_instance("PS_SHARPNESS_CTRL_REGISTER", f"PS_SHARPNESS_CTRL_{panel.pipe}",
                                                     PLATFORM_NAME)
    ps_sharpness_lut_data_reg = MMIORegister.get_instance("PS_SHRPLUT_DATA_REGISTER", f"PS_SHRPLUT_DATA_{panel.pipe}",
                                                          PLATFORM_NAME)
    ps_sharpness_lut_index_reg = MMIORegister.get_instance("PS_SHRPLUT_INDEX_REGISTER", f"PS_SHRPLUT_INDEX_{panel.pipe}"
                                                           , PLATFORM_NAME)

    scaler_data = etl_parser.get_event_data(etl_parser.Events.SCALER_INFO)
    if scaler_data is None:
        logging.warning("\tWARNING: Event scaler_data missing from ETL ")
    else:
        logging.debug(f"Scaler Data - {scaler_data}")
        for scaler_enable_flag in scaler_data:
            if scaler_enable_flag.EnableFlag:
                logging.debug(f"Scaler Timestamp - {scaler_enable_flag.TimeStamp}")
                start_data = scaler_enable_flag.TimeStamp

        ps2_ctl_offset = ps2_ctl_reg.offset
        sharpness_ctl_offset = ps_sharpness_ctl_reg.offset
        sharpness_lut_data_offset = ps_sharpness_lut_data_reg.offset
        sharpness_lut_index_offset = ps_sharpness_lut_index_reg.offset

        logging.debug(f"DEBUG: Offsets - ps2_ctl_offset {ps2_ctl_offset}, ps_sharpness_ctl_offset - {sharpness_ctl_offset},"
                      f" sharpness_lut_data_offset - {sharpness_lut_data_offset},"
                      f" sharpness_lut_index_offset - {sharpness_lut_index_offset}")

        ps2_ctl_data = etl_parser.get_mmio_data(ps2_ctl_offset, is_write=True, is_cpu_mmio=True, start_time=start_data,
                                                end_time=None)
        sharpness_ctl_data = etl_parser.get_mmio_data(sharpness_ctl_offset, is_write=True, is_cpu_mmio=True,
                                                      start_time=start_data, end_time=None)
        sharpness_lut_data = etl_parser.get_mmio_data(sharpness_lut_data_offset, is_write=True, is_cpu_mmio=True,
                                                      start_time=start_data, end_time=None)
        sharpness_lut_index_data = etl_parser.get_mmio_data(sharpness_lut_index_offset, is_write=True, is_cpu_mmio=True,
                                                            start_time=start_data, end_time=None)

        if sharpness_lut_data is None:
            logging.error("\t sharpness_lut_data is Empty ")
            return False

    return ps2_ctl_data, ps2_ctl_reg, sharpness_ctl_data, ps_sharpness_ctl_reg, sharpness_lut_data, \
        ps_sharpness_lut_data_reg, sharpness_lut_index_data, ps_sharpness_lut_index_reg


##
# @brief        Helper function to generate ETL report.
# @param[in]    panel             : panel object
# @param[in]    etl_file_path     : ETL file path to generate report
# @return       ps_coef_data, ps_coef_data_offset, ps_coef_index_data, ps_coef_index_offset, ps1_ctl_data,
# ps1_ctl_offset: MMIO data from ETL with Register instance
def extract_legacy_etl_data(etl_file_path, panel):
    if etl_parser.generate_report(etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report [Test Issue]")
        return False

    # Get MMIO register instance for Sharpness Registers
    ps1_ctl_reg = MMIORegister.get_instance("PS_CTRL_REGISTER", f"PS_CTRL_1_{panel.pipe}", PLATFORM_NAME)
    ps_coef_data_reg = MMIORegister.get_instance("PS_COEF_DATA_REGISTER", f"PS_COEF_SET_0_DATA_1_{panel.pipe}",
                                                 PLATFORM_NAME)
    ps_coef_index_reg = MMIORegister.get_instance("PS_COEF_INDEX_REGISTER", f"PS_COEF_SET_0_INDEX_1_{panel.pipe}",
                                                  PLATFORM_NAME)

    etl_parser.generate_report(etl_file_path)

    ps1_ctl_offset = ps1_ctl_reg.offset
    ps_coef_data_offset = ps_coef_data_reg.offset
    ps_coef_index_offset = ps_coef_index_reg.offset
    logging.debug(f"DEBUG: Offsets - ps1 {ps1_ctl_offset}, ps_data - {ps_coef_data_offset}, ps_index - "
                  f"{ps_coef_index_offset}")

    ps_coef_data = etl_parser.get_mmio_data(ps_coef_data_offset, is_write=True, is_cpu_mmio=True)
    ps_coef_index_data = etl_parser.get_mmio_data(ps_coef_index_offset, is_write=True, is_cpu_mmio=True)
    ps1_ctl_data = etl_parser.get_mmio_data(ps1_ctl_offset, is_write=True, is_cpu_mmio=True)

    if ps_coef_data is None:
        logging.error("Sharpness PS_COEF_DATA_REGISTER MMIO data is Empty")
        return False

    return ps_coef_data, ps_coef_data_reg, ps_coef_index_data, ps_coef_index_reg, ps1_ctl_data, ps1_ctl_reg


##
# @brief        Helper function to verify PS_CTRL Reg for Sharpness.
# @param[in]    ps2_ctl_data  : Sharpness MMIO Data from ETL
# @param[in]    ps2_ctl_reg    : Register instance
# @return       status     : True if PS_CTRL verification pass, False otherwise
def verify_ps_ctrl(ps2_ctl_data, ps2_ctl_reg):
    logging.info(" PS_CTRL Register Verification ".center(MAX_LINE_WIDTH, "*"))

    for ps_ctl in ps2_ctl_data:
        ps2_ctl_reg.asUint = ps_ctl.Data
        if ps2_ctl_reg.offset == ps_ctl.Offset:
            if ps2_ctl_reg.enable_scaler == 1:
                logging.info(f"\t Scalar is enabled for Sharpness - {ps2_ctl_reg.enable_scaler} during "
                             f"TimeStamp - {ps_ctl.TimeStamp}")
                return True
            elif ps2_ctl_reg.enable_scaler == 0:
                logging.error(f"\t Scalar is disabled for Sharpness - {ps2_ctl_reg.enable_scaler} during "
                              f"TimeStamp - {ps_ctl.TimeStamp}")
                return False


##
# @brief        Helper function to verify get_expected_filer_size for Sharpness.
# @param[in]    resolution    : resolution
# @return       resolution    : return tap filter
def get_expected_filer_size(resolution):
    return {
        '1920x1080': '_Three',
        '2560x1440': '_Five',
        '3840x2160': '_Seven'
    }[resolution]


##
# @brief        Helper function to verify PS_SHARPNESS_CTRL for Sharpness.
# @param[in]    sharpness_ctl_data  : sharpness_ctl_data Data from ETL
# @param[in]    ps_sharpness_ctl_reg : Register instance
# @param[in]    strength            : sharpness strength
# @param[in]    resolution          : resolution
# @return       status              : True if PS_CTRL verification pass, False otherwise
def verify_ps_sharpness_ctrl(sharpness_ctl_data, ps_sharpness_ctl_reg, strength, resolution):
    logging.info(" PS_SHARPNESS_CTRL Verification ".center(MAX_LINE_WIDTH, "*"))
    status = True
    filter_size = get_expected_filer_size(resolution)

    for sharpness_data in sharpness_ctl_data:
        ps_sharpness_ctl_reg.asUint = sharpness_data.Data
        if (ps_sharpness_ctl_reg.offset == sharpness_data.Offset) and sharpness_data.IsWrite:
            if ps_sharpness_ctl_reg.sharpness_filter_enable == 1:
                logging.info(f"\t Sharpness Filter is enabled - {ps_sharpness_ctl_reg.sharpness_filter_enable} during "
                             f"TimeStamp - {sharpness_data.TimeStamp}")
                status &= True
            elif ps_sharpness_ctl_reg.sharpness_filter_enable == 0:
                logging.error(f"\t Sharpness Filter is disabled - {ps_sharpness_ctl_reg.sharpness_filter_enable} "
                              f"during TimeStamp - {sharpness_data.TimeStamp}")
                status &= False
            if ps_sharpness_ctl_reg.sharpness_filter_size == TapFilter[filter_size]:
                logging.info(f"\t Sharpness Filter Size is matching with expected - {TapFilter[filter_size]} "
                             f"actual - {ps_sharpness_ctl_reg.sharpness_filter_size} size during TimeStamp - "
                             f"{sharpness_data.TimeStamp}")
                status &= True
            else:
                logging.error(f"\t Sharpness Filter Size is not matching with expected - {TapFilter[filter_size]} "
                              f"actual - {ps_sharpness_ctl_reg.sharpness_filter_size} size during TimeStamp - "
                              f"{sharpness_data.TimeStamp}")
                status &= False

            if int(ps_sharpness_ctl_reg.strength) == strength:
                logging.info(f"\t Sharpness Strength is matching with expected {strength} actual - "
                             f"{ps_sharpness_ctl_reg.strength} during TimeStamp - {sharpness_data.TimeStamp}")
                status &= True
            else:
                logging.error(f"\t Sharpness Strength is not matching with expected {strength} actual - "
                              f"{ps_sharpness_ctl_reg.strength} during TimeStamp - {sharpness_data.TimeStamp}")
                status &= False

    return status


##
# @brief        Helper function to verify PS_SHRPLUT_DATA Reg for Sharpness.
# @param[in]    sharpness_lut_data         : Flip Data from ETL
# @param[in]    ps_sharpness_lut_data_reg  : Register instance
# @return       status                     : True if PS_CTRL verification pass, False otherwise
def verify_ps_sharpness_lut(sharpness_lut_data, ps_sharpness_lut_data_reg):
    logging.info(" PS_SHRPLUT_DATA Verification ".center(MAX_LINE_WIDTH, "*"))
    status = True

    for lut_data in sharpness_lut_data:
        ps_sharpness_lut_data_reg.asUint = lut_data.Data
        if (ps_sharpness_lut_data_reg.offset == lut_data.Offset) and lut_data.IsWrite:
            if ps_sharpness_lut_data_reg.adaptive_sharpness_lut_data != 0:
                logging.info(f"\t Adaptive Sharpness Lut Data is non zero (programmed)- "
                             f"{ps_sharpness_lut_data_reg.adaptive_sharpness_lut_data}  during TimeStamp - "
                             f"{lut_data.TimeStamp}")
                status &= True
            elif ps_sharpness_lut_data_reg.adaptive_sharpness_lut_data == 0:
                logging.error(f"\t Adaptive Sharpness Lut Data is zero (not programmed)- "
                              f"{ps_sharpness_lut_data_reg.adaptive_sharpness_lut_data} during TimeStamp - "
                              f"{lut_data.TimeStamp}")
                status &= False
    return status


##
# @brief        Helper function to verify PS_SHRPLUT_INDEX_DATA for Sharpness.
# @param[in]    sharpness_lut_index_data    : sharpness_lut_index_data from ETL
# @param[in]    ps_sharpness_lut_index_reg  : Register instance
# @return       status                      : True if PS_SHRPLUT_INDEX_DATA verification pass, False otherwise
def verify_ps_sharpness_lut_index(sharpness_lut_index_data, ps_sharpness_lut_index_reg):
    logging.info(" PS_SHRPLUT_INDEX_DATA Verification ".center(MAX_LINE_WIDTH, "*"))
    status = True

    for lut_index in sharpness_lut_index_data:
        lut_index.asUint = lut_index.Data
        if (ps_sharpness_lut_index_reg.offset == lut_index.Offset) and lut_index.IsWrite:
            if ps_sharpness_lut_index_reg.index_value != 0:
                logging.info(f"\t Index value controls access to Sharpness LUT entries -"
                             f" {ps_sharpness_lut_index_reg.index_value} during TimeStamp - {lut_index.TimeStamp}")
                status &= True
            else:
                logging.error(f"\t Index value to Sharpness LUT entries is zero -"
                              f" {ps_sharpness_lut_index_reg.index_value} during TimeStamp - {lut_index.TimeStamp}")
                status &= False

            if ps_sharpness_lut_index_reg.index_auto_increment == 0b0:
                logging.info(f"\t Index Auto Increment is not incremented automatically "
                             f"{ps_sharpness_lut_index_reg.index_auto_increment} during TimeStamp - "
                             f"{lut_index.TimeStamp}")
            elif ps_sharpness_lut_index_reg.index_auto_increment == 0b1:
                logging.info(f"\t Index Auto Increment is incremented automatically with each read/write to reg"
                             f"{ps_sharpness_lut_index_reg.index_auto_increment} during TimeStamp - "
                             f"{lut_index.TimeStamp}")

    return status


##
# @brief        Helper function to verify Sharpness
# @param[in]    etl_file    : ETL file
# @param[in]    panel       : Panel data
# @param[in]    strength    : Sharpness strength
# @param[in]    filter_type : Filter Type
# @param[in]    resolution  : Resolution
# @return       status      : True if sharpness verification pass, False otherwise
def verify_sharpness(etl_file, panel, strength, filter_type, resolution):
    if filter_type == 'ADAPTIVE':
        verify_sharpness_adaptive(etl_file, panel, strength, resolution)
    elif filter_type == 'NON_ADAPTIVE':
        verify_legacy_sharpness_non_adaptive(etl_file, panel)
    else:
        logging.error("Planning Issue: Filter Type is not available in test command line")
        return False


##
# @brief        Helper function to verify Adaptive Sharpness
# @param[in]    etl_file    : ETL file
# @param[in]    panel       : Panel data
# @param[in]    strength    : Sharpness strength
# @param[in]    resolution  : Resolution
# @return       status      : True if sharpness verification pass, False otherwise
def verify_sharpness_adaptive(etl_file, panel, strength, resolution):
    ps_ctl_status, sharpness_ctl_status, sharpness_lut_status, sharpness_lut_index_status = True, True, True, True

    ps2_ctl_data, ps2_ctl_reg, sharpness_ctl_data, ps_sharpness_ctl_reg, sharpness_lut_data, \
        ps_sharpness_lut_data_reg, sharpness_lut_index_data, \
        ps_sharpness_lut_index_reg = extract_etl_data(panel, etl_file)

    if ps2_ctl_data is not None:
        # Verify PS_CTRL_REGISTER Programming
        if verify_ps_ctrl(ps2_ctl_data, ps2_ctl_reg):
            logging.info("Pass: PS_CTRL_REGISTER Programming, Scalar is enabled for Sharpness")
            ps_ctl_status &= True
        else:
            logging.error("Fail: PS_CTRL_REGISTER Programming, Scalar is not enabled for Sharpness")
            ps_ctl_status &= False

    if sharpness_ctl_data is not None:
        # Verify PS_SHARPNESS_CTRL Programming
        if verify_ps_sharpness_ctrl(sharpness_ctl_data, ps_sharpness_ctl_reg, strength, resolution):
            logging.info("Pass: PS_SHARPNESS_CTRL Programming")
            sharpness_ctl_status &= True
        else:
            logging.error("Fail: PS_SHARPNESS_CTRL Register Programming")
            sharpness_ctl_status &= False

    if sharpness_lut_data is not None:
        # Verify PS_SHARPNESS_LUT_CTRL Programming
        if verify_ps_sharpness_lut(sharpness_lut_data, ps_sharpness_lut_data_reg):
            logging.info("Pass: PS_SHARPNESS_LUT_CTRL Programming")
            sharpness_lut_status &= True
        else:
            logging.error("Fail: PS_SHARPNESS_LUT_CTRL Register Programming")
            sharpness_lut_status &= False

    if sharpness_lut_index_data is not None:
        # Verify PS_SHARPNESS_LUT_INDEX_CTRL Programming
        if verify_ps_sharpness_lut_index(sharpness_lut_index_data, ps_sharpness_lut_index_reg):
            logging.info("Pass: PS_SHARPNESS_LUT_INDEX_CTRL Programming")
            sharpness_lut_index_status &= True
        else:
            logging.error("Fail: PS_SHARPNESS_LUT_INDEX_CTRL Register Programming")
            sharpness_lut_index_status &= False

    if ps_ctl_status and sharpness_ctl_status and sharpness_lut_status and sharpness_lut_index_status:
        logging.info("Pass: SHARPNESS Programming Verification")
        return True
    return False


##
# @brief        Helper function to verify PS_COEF_DATA for  Legacy Sharpness.
# @param[in]    ps_coef_data    : Sharpness MMIO Data from ETL
# @param[in]    ps_coef_data_reg : Register instance
# @return       status       : True if PS_COEF_DATA verification pass, False otherwise
def verify_ps_coef_data(ps_coef_data, ps_coef_data_reg):
    logging.info(" PS_COEF_DATA Verification ".center(MAX_LINE_WIDTH, "*"))
    status = True
    ps_coef_data_value = []

    for coef_data in ps_coef_data:
        if coef_data.Offset == ps_coef_data_reg.offset:
            ps_coef_data_reg.asUint = coef_data.Data
            ps_coef_data_value.append(ps_coef_data_reg.asUint)
    logging.debug(f"DEBUG: co_eff_data_value_list - {ps_coef_data_value}")

    for coef_data in ps_coef_data:
        ps_coef_data_reg.asUint = coef_data.Data
        if coef_data.Offset == ps_coef_data_reg.offset:
            if ps_coef_data_reg.coefficient1 != 0:
                logging.info(f"\t PS COEF 1 Data is non zero (programmed)- "
                             f"{ps_coef_data_reg.coefficient1}  during TimeStamp - {coef_data.TimeStamp}")
                status &= True
            elif ps_coef_data_reg.coefficient2 != 0:
                logging.info(f"\t PS COEF 2 Data is non zero (programmed)- "
                             f"{ps_coef_data_reg.coefficient2} during TimeStamp - {coef_data.TimeStamp}")
                status &= True
            elif ps_coef_data_reg.coefficient1 == 0 and coef_data.coefficient2 == 0:
                logging.error(f"\t PS COEF Data is zero (non programmed)- {ps_coef_data_reg.coefficient1} and "
                              f"{ps_coef_data_reg.coefficient2}  during TimeStamp - {coef_data.TimeStamp}")
                status &= False
    return status


##
# @brief        Helper function to verify PS_COEF_INDEX for Legacy Sharpness.
# @param[in]    ps_coef_index_data : Sharpness MMIO Data from ETL
# @param[in]    ps_coef_index_reg : Register instance
# @return       status        : True if PS_COEF_INDEX verification pass, False otherwise
def verify_ps_coef_index(ps_coef_index_data, ps_coef_index_reg):
    logging.info(" PS_COEF_INDEX Verification ".center(MAX_LINE_WIDTH, "*"))
    status = True

    for coef_index in ps_coef_index_data:
        ps_coef_index_reg.asUint = coef_index.Data
        if coef_index.Offset == ps_coef_index_reg.offset:
            if ps_coef_index_reg.index_value != 0:
                logging.info(f"\t Index value is programmed with array of scaler coefficient values "
                             f"- {ps_coef_index_reg.index_value} during TimeStamp - {coef_index.TimeStamp}")
                status &= True
            else:
                logging.error(f"\t Index value is not programmed with array of scaler coefficient values "
                              f"- {ps_coef_index_reg.index_value} during TimeStamp - {coef_index.TimeStamp}")
                status &= False
            if ps_coef_index_reg.index_auto_increment == 0:
                logging.info(f"\t Index value is not incremented / No read-write to data register"
                             f"- {ps_coef_index_reg.index_auto_increment} during TimeStamp - {coef_index.TimeStamp}")
            elif ps_coef_index_reg.index_auto_increment == 1:
                logging.info(f"\t Index value is incremented with each read/write to data register "
                             f"- {ps_coef_index_reg.index_auto_increment} during TimeStamp - {coef_index.TimeStamp}")
    return status


##
# @brief        Helper function to verify Non-Adaptive Sharpness.
# @param[in]    etl_file   : ETL file
# @param[in]    panel      : Panel object
# @return       status     : True if sharpness verification pass, False otherwise
def verify_legacy_sharpness_non_adaptive(etl_file, panel):
    ps_ctl_status, ps_coef_data_status, ps_coef_index_status = True, True, True

    ps_coef_data, ps_coef_data_reg, ps_coef_index_data, ps_coef_index_reg, ps1_ctl_data, ps1_ctl_reg = \
        extract_legacy_etl_data(etl_file, panel)

    # Verify PS_COEF_DATA_REGISTER Programming
    if verify_ps_coef_data(ps_coef_data, ps_coef_data_reg):
        logging.info("Pass: PS_COEFFICIENT_DATA Register Programming")
        ps_coef_data_status &= True
    else:
        logging.error("Fail: PS_COEFFICIENT_DATA Register Programming")
        ps_coef_data_status &= False

    # Verify PS_COEF_INDEX_REGISTER Programming
    if verify_ps_coef_index(ps_coef_index_data, ps_coef_index_reg):
        logging.info("Pass: PS_COEFFICIENT_INDEX Register Programming")
        ps_coef_index_status &= True
    else:
        logging.error("Fail: PS_COEFFICIENT_INDEX Register Programming")
        ps_coef_index_status &= False

    if ps_coef_data_status and ps_coef_index_status:
        logging.info("Pass: Sharpness Programming Verification")
        return True
    return False
