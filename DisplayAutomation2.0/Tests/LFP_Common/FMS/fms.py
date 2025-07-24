########################################################################################################################
# @file         fms.py
# @brief        This files contains helper functions for LFP_ Commons FMS test cases
# @author       Tulika
########################################################################################################################

import logging

from Libs.Core import registry_access, display_essential
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm, html
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

# GDHM header
GDHM_FMS = "[Display_Interfaces][EDP][FMS]"


##
# @brief This class has the values for enable and disable sequence
class RegisterStatus:
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    NONE = "NONE"


##
# @brief This class has the values for htotal vtotal status
class HtotalVtotalStatus:
    READ = "READ"
    WRITE = "WRITE"


##
# @brief  This class has the registers required for mode set verification
class Register:
    TRANS_DDI = "TRANS_DDI_FUNC_CTL_REGISTER"
    BACKLIGHT = "SBLC_PWM_CTL1_REGISTER"
    TRANSCODER = "TRANS_CONF_REGISTER"
    PLL = "DPCLKA_CFGCR0_REGISTER"


##
# @brief This class has the values for modeset
class ModeSetType:
    FULL = "FULL_MODE_SET"
    FAST = "FAST_MODE_SET"
    INVALID_FMS_SEQUENCE = "INVALID_FMS_SEQUENCE"


##
# @brief        Exposed API to enable FMS
# @return       status - Boolean, True if operation is successful, False otherwise
# @note         FMS is always enabled in Yangra and can not be disabled using registry key
def enable():
    if common.IS_DDRW:
        return True
    return __change_fms(registry.RegValues.FMS.ENABLED)


##
# @brief        Exposed API to disable FMS
# @return       status - Boolean, True if operation is successful, False otherwise
def disable():
    if common.IS_DDRW:
        return False
    return __change_fms(registry.RegValues.FMS.DISABLED)


##
# @brief        Check if driver is following full mode set path or fast mode set path during power events
# @param[in]    etl_file string, path to the etl file
# @param[in]    transcoder
# @param[in]    platform string, name of the platform
# @param[in]    target_id of the edp panel
# @param[in]    is_d_state_expected True if is_d_state_expected else False
# @return       FULL_MODE_SET, FAST_MODE_SET, MODE_SET_FAILED
def verify_fms_during_power_events(etl_file, transcoder, platform, target_id, is_d_state_expected=False):
    reg_list = [Register.TRANS_DDI, Register.BACKLIGHT, Register.TRANSCODER, Register.PLL]
    reg_status = {
        Register.TRANS_DDI: [None, None],
        Register.BACKLIGHT: [None, None],
        Register.TRANSCODER: [None, None],
        Register.PLL: [None, None]
    }

    html.step_start(f"Verifying Mode Set for port_{transcoder}")

    if target_id is None:
        logging.error(f"Target Id is None (Invalid)")
        html.step_end()
        return False

    # Generate reports from ETL file using EtlParser
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate EtlParser report")
        html.step_end()
        return False

    d_state_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_PWR_CONS_D0_D3_STATE_CHANGE)

    # d_state_data not expected for reboot and display switch scenario
    if d_state_data is not None:
        if is_d_state_expected is False:
            logging.error("Unexpected D0/D3 state data found in ETL")
            gdhm.report_driver_bug_di(f"{GDHM_FMS} Unexpected D0/D3 state data found in ETL")
            html.step_end()
            return False
    # d_state_data is expected for power events(s3, hibernate)
    if d_state_data is None:
        if is_d_state_expected is True:
            logging.error("D0/D3 state data not found in ETL. Skipping FMS Verification")
            gdhm.report_driver_bug_di(f"{GDHM_FMS} D0/D3 state data not found in ETL.")
            html.step_end()
            return False

    d0_entry_time = None
    D0_State = False
    if is_d_state_expected is True:
        for data in d_state_data:
            if data.IsD0 == 1:
                D0_State = True
                d0_entry_time = data.TimeStamp
                logging.debug(f"D0_EntryTime: {d0_entry_time}")
                break

    if D0_State is False and is_d_state_expected is True:
        logging.error("No D0 Entry found in ETL. Skipping FMS Verification")
        gdhm.report_driver_bug_di(f"{GDHM_FMS} No D0 Entry found in ETL.")
        html.step_end()
        return False

    # There should be at least one mode set in ETL to verify link training
    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN, start_time=d0_entry_time)
    if ddi_output is None:
        logging.error("No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        gdhm.report_driver_bug_di(f"{GDHM_FMS} No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False
    ##
    # There could be multiple mode set calls from OS during power event (uninit call before going to power event,
    # init call after power event etc). Consider the last mode set entry for verification.
    ddi_data = ddi_output[-1]

    # Check H_Total and V_Total mmio registers
    htotal_vtotal_status = __check_htotal_vtotal_mmio(transcoder, platform, d0_entry_time)
    logging.debug(f"Htotal and Vtotal {htotal_vtotal_status} found")

    fast_mode_set = True
    status = True
    for register in reg_list:
        html.step_start(f"Verifying MMIO status for {register}", True)
        reg_status = __read_modeset_registers(transcoder, platform, reg_status, register, d0_entry_time, ddi_data,
                                              ddi_output)
        # Check for Full Mode Set
        if reg_status[register][0] == RegisterStatus.DISABLE and reg_status[register][1] == RegisterStatus.ENABLE:
            logging.info(f"Disable and Enable sequence found for {register}, state change")
            fast_mode_set = False

        # Checking PLL separately because enable pll programming is not expected in FMS(Fast modes set) path.
        if register == Register.PLL and reg_status[register][1] != RegisterStatus.ENABLE:
            logging.info(f"No enable pll programming is found for {register} in fms path (Expected)")
        elif reg_status[register][1] == RegisterStatus.ENABLE:
            logging.info(f"Enable sequence found for {register}, no state change")
        else:
            status = False
            fast_mode_set = False
            logging.error(f"FAIL: Invalid FMS Sequence found for {register}")
            gdhm.report_driver_bug_di(f"{GDHM_FMS} Invalid FMS Sequence found for {register}")
        html.step_end()

    modeset_status = etl_parser.get_event_data(etl_parser.Events.FMS_STATUS_INFO)
    if modeset_status is None:
        if platform not in common.GEN_12_PLATFORMS:
            logging.error("Modeset status NOT found in ETL")
            gdhm.report_driver_bug_di(f"{GDHM_FMS} Modeset status not found in ETL.")
            return False
        else:
            logging.info(f"{platform} does not support seamless CD clock change hence FmsStatus is not logged")
    else:
        for data in modeset_status:
            logging.info(f"\tFms Status= {data.Status}")

    if fast_mode_set:
        for data in modeset_status:
            if data.Status == "DD_FMS_SUCCESS" and data.TargetId == target_id:
                logging.info("Driver followed FMS path")

    if not fast_mode_set:
        return ModeSetType.FULL if status else ModeSetType.INVALID_FMS_SEQUENCE
    return ModeSetType.FAST


##
# @brief        Verifies if driver is following full mode set path or fast mode set path
# @param[in]    etl_file string, path to the etl file
# @param[in]    transcoder
# @param[in]    platform string, name of the platform
# @return       FULL_MODE_SET, FAST_MODE_SET, MODE_SET_FAILED
def verify_fms(etl_file, transcoder, platform):
    reg_list = [Register.TRANS_DDI, Register.BACKLIGHT, Register.TRANSCODER, Register.PLL]
    reg_status = {
        Register.TRANS_DDI: [None, None],
        Register.BACKLIGHT: [None, None],
        Register.TRANSCODER: [None, None],
        Register.PLL: [None, None]
    }

    html.step_start(f"Verifying Mode Set for port_{transcoder}")

    # Generate reports from ETL file using EtlParser
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate EtlParser report")
        html.step_end()
        return False

    d0_entry_time = None
    # There should be at least one mode set in ETL to verify link training
    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN, start_time=d0_entry_time)
    if ddi_output is None:
        logging.error("No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        gdhm.report_driver_bug_di(f"{GDHM_FMS} No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False
    ##
    # There could be multiple mode set calls from OS during power event (uninit call before going to power event,
    # init call after power event etc). Consider the last mode set entry for verification.
    ddi_data = ddi_output[-1]

    # Check H_Total and V_Total mmio registers
    htotal_vtotal_status = __check_htotal_vtotal_mmio(transcoder, platform, d0_entry_time)
    logging.debug(f"Htotal and Vtotal {htotal_vtotal_status} found")

    fast_mode_set = True
    for register in reg_list:
        html.step_start(f"Verifying MMIO status for {register}", True)
        reg_status = __read_modeset_registers(transcoder, platform, reg_status, register, d0_entry_time, ddi_data,
                                              ddi_output)
        if reg_status[register][0] == RegisterStatus.DISABLE and reg_status[register][1] == RegisterStatus.ENABLE:
            logging.info(f"Disable and Enable sequence found for {register}, state change")
            fast_mode_set = False
        else:
            logging.info(f"No state change for {register}")
        html.step_end()

    if not fast_mode_set:
        return ModeSetType.FULL
    return ModeSetType.FAST


##
# @brief        Read the modeset registers post D0 timestamp
# @param[in]    transcoder
# @param[in]    platform string name of the platform
# @param[in]    reg_status dictionary to maintain the mmio reg enable/disable sequence in case of modeset
# @param[in]    register current register
# @param[in]    d0_entry_time timestamp at which system wakes up post low power state
# @param[in]    ddi_data
# @param[in]    ddi_output
# @return       reg_status dictionary where key is the mmio reg and value is enable/disable sequence as list {reg:[D,E]}
def __read_modeset_registers(transcoder, platform, reg_status: dict, register, d0_entry_time, ddi_data, ddi_output):
    reg_instance = None
    if register == Register.TRANS_DDI:
        reg_instance = MMIORegister.get_instance(register, "TRANS_DDI_FUNC_CTL_" + transcoder, platform)

    elif register == Register.BACKLIGHT:
        reg_suffix = ['', '_2']
        if transcoder in ["DSI0", 'A']:
            index = 0
        else:
            index = 1
        reg_instance = MMIORegister.get_instance(register, "SBLC_PWM_CTL1" + reg_suffix[index], platform)

    elif register == Register.TRANSCODER:
        reg_instance = MMIORegister.get_instance(register, "TRANS_CONF_" + transcoder, platform)

    elif register == Register.PLL:
        dpclka_cfgcr0 = MMIORegister.read(register, 'DPCLKA_CFGCR0', platform)
        dpll_value_from_register = dpclka_cfgcr0.ddia_clock_select if transcoder in ['DSI0', "A"] \
            else dpclka_cfgcr0.ddib_clock_select
        if dpll_value_from_register == 0:
            dpll_value = 'DPLL0'
        elif dpll_value_from_register == 1:
            dpll_value = 'DPLL1'
        else:
            dpll_value = 'DPLL4'
        reg_instance = MMIORegister.get_instance("DPLL_ENABLE_REGISTER", dpll_value + "_ENABLE", platform)

    reg_status = __check_mmio_sequence(transcoder, reg_instance, register, reg_status, d0_entry_time, ddi_data,
                                       ddi_output)
    return reg_status


##
# @brief        Check the mmio regs enable/disable sequence post D0 and update the reg_status dictionary.
# @param[in]    transcoder
# @param[in]    register_instance instance with current register offset and value
# @param[in]    register current register
# @param[in]    reg_status dictionary to maintain the mmio reg enable/disable sequence in case of modeset
# @param[in]    d0_entry_time timestamp at which system wakes up post low power state
# @param[in]    ddi_data
# @param[in]    ddi_output
# @return       reg_status dictionary where key is the mmio reg and value is enable/disable sequence as list {reg:[D,E]}
def __check_mmio_sequence(transcoder, reg_instance, register, reg_status, d0_entry_time, ddi_data, ddi_output):
    # In Modeset, the mmio reg enable/disable sequence determines the 'Fast' or 'Full' mode set
    # All below steps should be followed for data collected post D0 timestamp
    # Steps:
    # 1. Check the last mmio write entry for each register, It should be 'Enable' irrespective of Full or Fast modeset
    # 2. Check the rest of the mmio write entry, If any disable sequence found, return Full Mode Set
    # 3. If write entry not found for disable, then check the first mmio read(post D0) for the register it will be
    #    either enable or disable, if enable return Fast Mode Set else return Full Mode Set

    mmio_write = etl_parser.get_mmio_data(reg_instance.offset, is_write=True, start_time=d0_entry_time)
    mmio_read = etl_parser.get_mmio_data(reg_instance.offset, is_write=False, start_time=d0_entry_time)
    if mmio_write is None and mmio_read is None:
        logging.warning(f"NO MMIO Entries found for register {register}")
        return reg_status

    if mmio_write is not None:
        for data in mmio_write:
            reg_enable = None
            if ddi_output is not None:
                if ddi_data.StartTime < data.TimeStamp < ddi_data.EndTime:
                    reg_instance.asUint = data.Data
                    reg_enable = __get_reg_offset(reg_instance, register)
            else:
                if transcoder == "DSI0":
                    reg_instance.asUint = data.Data
                    reg_enable = __get_reg_offset(reg_instance, register)

            logging.info(f"Offset= {hex(data.Offset)}, Value= {hex(data.Data)} at {data.TimeStamp}ms")

            if reg_enable == 0:
                # Check mmio write entry, for disable sequence, but that should not be the last entry
                if len(mmio_write) > 1 and mmio_write.index(data) != len(mmio_write) - 1:
                    logging.info(f"\t{register} MMIO write entry for DISABLE found")
                    reg_status[register][0] = RegisterStatus.DISABLE

            elif reg_enable == 1:
                # Check mmio write entry, for enable sequence, but that should be the last mmio write entry
                if mmio_write.index(data) == len(mmio_write) - 1:
                    logging.info(f"\t{register} MMIO write entry for ENABLE found")
                    reg_status[register][1] = RegisterStatus.ENABLE

    # If write entry not found for disable, then check the first mmio read(post D0), to get register status
    if not (reg_status[register][0] == RegisterStatus.DISABLE and reg_status[register][1] == RegisterStatus.ENABLE):
        reg_enable = None
        for data in mmio_read:
            if ddi_output is not None:
                if ddi_data.StartTime < data.TimeStamp < ddi_data.EndTime:
                    reg_instance.asUint = data.Data
                    reg_enable = __get_reg_offset(reg_instance, register)
            else:
                if transcoder == "DSI0":
                    reg_instance.asUint = data.Data
                    reg_enable = __get_reg_offset(reg_instance, register)

            logging.info(f"Offset= {hex(data.Offset)}, Value= {hex(data.Data)} at {data.TimeStamp}ms")

            if reg_enable == 1:
                logging.info(f"\t{register} MMIO read entry for ENABLE found")
                reg_status[register][0] = RegisterStatus.ENABLE
                break
            if reg_enable == 0:
                logging.info(f"\t{register} MMIO read entry for DISABLE found")
                reg_status[register][0] = RegisterStatus.DISABLE
                break
    return reg_status


##
# @brief        Api to get register offsets
# @param[in]    register_instance instance with current register offset and value
# @param[in]    register current register
# @return       reg_enable
def __get_reg_offset(register_instance, register):
    reg_enable = None
    if register == Register.TRANS_DDI:
        reg_enable = register_instance.trans_ddi_function_enable
    elif register == Register.BACKLIGHT:
        reg_enable = register_instance.pwm_pch_enable
    elif register == Register.TRANSCODER:
        reg_enable = register_instance.transcoder_enable
    elif register == Register.PLL:
        reg_enable = register_instance.pll_enable
    return reg_enable


##
# @brief        Check Htotal and Vtotal registers for read/write enteries post D0
# @param[in]    transcoder
# @param[in]    platform string, name of the platform
# @param[in]    d0_entry_time timestamp at which system wakes up post low power state
# @return       Write if write entries found else Read
def __check_htotal_vtotal_mmio(transcoder, platform, d0_entry_time):
    html.step_start("Verifying MMIO status for TRANS_HTOTAL_REGISTER and TRANS_VTOTAL_REGISTER")
    trans_mmio_write_status = True
    trans_mmio_read_status = True
    trans_htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + transcoder, platform)
    trans_vtotal = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + transcoder, platform)

    trans_htotal_mmio_write = etl_parser.get_mmio_data(trans_htotal.offset, is_write=True,
                                                       start_time=d0_entry_time)
    trans_vtotal_mmio_write = etl_parser.get_mmio_data(trans_vtotal.offset, is_write=True,
                                                       start_time=d0_entry_time)
    if trans_htotal_mmio_write is None:
        logging.info(f"\tNO MMIO write entries found for register TRANS_HTOTAL_{transcoder}")
        trans_mmio_write_status &= False
    else:
        logging.info(f"\tMMIO write entry found for register TRANS_HTOTAL_{transcoder}")

    if trans_vtotal_mmio_write is None:
        logging.info(f"\tNO MMIO write entries found for register TRANS_VTOTAL_{transcoder}")
        trans_mmio_write_status &= False
    else:
        logging.info(f"\tMMIO write entry found for register TRANS_VTOTAL_{transcoder}")

    if trans_mmio_write_status is True:
        html.step_end()
        return HtotalVtotalStatus.WRITE

    trans_htotal_mmio_read = etl_parser.get_mmio_data(trans_htotal.offset, is_write=False,
                                                      start_time=d0_entry_time)
    trans_vtotal_mmio_read = etl_parser.get_mmio_data(trans_vtotal.offset, is_write=False,
                                                      start_time=d0_entry_time)

    if trans_htotal_mmio_read is None:
        logging.info(f"\tNO MMIO read entries found for register TRANS_HTOTAL_{transcoder}")
        trans_mmio_read_status &= False
    else:
        logging.info(f"\tMMIO read entry found for register TRANS_HTOTAL_{transcoder}")

    if trans_vtotal_mmio_read is None:
        logging.info(f"\tNO MMIO read entries found for register TRANS_VTOTAL_{transcoder}")
        trans_mmio_read_status &= False
    else:
        logging.info(f"\tMMIO read entry found for register TRANS_VTOTAL_{transcoder}")

    html.step_end()
    if trans_mmio_read_status is True and trans_mmio_write_status is False:
        return HtotalVtotalStatus.READ
    return None


##
# @brief        Helper function to change FMS setting
# @param[in]    reg_value - Number, registry value
# @return       status - Boolean, True if operation is successful, False otherwise
def __change_fms(reg_value):
    reg_key = registry.RegKeys.FMS.DISPLAY_OPTIMIZATION
    status = registry.write("gfx_0", reg_key, registry_access.RegDataType.DWORD, reg_value)
    if status is False:
        logging.error(f"\tFailed to update  reg-key {reg_key}= {reg_value} (Test Issue)")
        return False
    result, reboot_required = display_essential.restart_gfx_driver()
    if status and result is False:
        logging.error("\tFailed to restart display driver(Test Issue)")
        return False
    logging.info(f"\tSuccessfully updated reg-key {reg_key}= {reg_value}")
    return True
