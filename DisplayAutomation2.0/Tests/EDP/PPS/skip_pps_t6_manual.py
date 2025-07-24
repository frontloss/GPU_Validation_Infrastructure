##############################################
# @file         skip_pps_t6_manual.py
# @brief        The script contains verification and ETL parsing logic for T6 delay and skip pps semi auto tests
#               Usage: skip_pps_t6_manual.py [-h] [-TYPE {VBT,T6, SKIP_PPS}] [-T6_DELAY {4000,3000,2000}] [-PATH PATH]
# @author       Tulika
########################################################################################################################
import argparse
import logging
import sys

from Libs import env_settings
from Libs.Core import etl_parser, display_essential
from Libs.Core.logger import display_logger
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from registers.mmioregister import MMIORegister

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'

LINK_IDLE_PATTERN = 4
LINK_NORMAL_PATTERN = 3
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName


##
# @brief        Fetch DDI Set Timings from VIDPN
# @return       ddi_timestamp
def fetch_set_ddi_vid_pin():
    is_d_state_expected = True
    d0_entry_time = None
    d0_state = False

    d_state_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_PWR_CONS_D0_D3_STATE_CHANGE)
    if d_state_data is None:
        logging.error("No D state data event found in ETLs")
        return False

    if is_d_state_expected is True:
        for data in d_state_data:
            if data.IsD0 == 1:
                d0_state = True
                d0_entry_time = data.TimeStamp
                logging.debug(f"D0_EntryTime: {d0_entry_time}")
                break

    if d0_state is False and is_d_state_expected is True:
        logging.error("No D0 Entry found in ETL. Skipping FMS Verification")
        return False

    # There should be at least one mode set in ETL to verify link training
    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN, start_time=d0_entry_time)
    if ddi_output is None:
        logging.error("No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False
    ##
    # There could be multiple mode set calls from OS during power event (uninit call before going to power event,
    # init call after power event etc). Consider the last mode set entry for verification.
    ddi_data = ddi_output[-1]
    return ddi_data.StartTime


##
# @brief        Fetch link idle pattern time
# @return       start_time
def fetch_link_idle():
    start_time = fetch_set_ddi_vid_pin()
    link_idle = MMIORegister.get_instance("DP_TP_CTL_REGISTER", "DP_TP_CTL_A", PLATFORM_NAME)
    link_idle_output = etl_parser.get_mmio_data(link_idle.offset, is_write=True, start_time=start_time)
    if link_idle_output is None:
        logging.error("\tNo MMIO Entries found for register DP_TP_CTL_A")
        return False
    for mmio_data in link_idle_output:
        link_idle.asUint = mmio_data.Data
        if LINK_IDLE_PATTERN == link_idle.dp_link_training_enable:
            logging.info(f"Link idle pattern found")
            start_time = mmio_data.TimeStamp
            logging.info(f"Start Time: {start_time}")
            break
    return start_time


##
# @brief        Fetch link normal pattern time
# @return       end_time
def fetch_link_normal():
    end_time = 0
    start_time = fetch_link_idle()
    link_idle = MMIORegister.get_instance("DP_TP_CTL_REGISTER", "DP_TP_CTL_A", PLATFORM_NAME)
    link_idle_output = etl_parser.get_mmio_data(link_idle.offset, is_write=True, start_time=start_time)
    if link_idle_output is None:
        logging.error("\tNo MMIO Entries found for register DP_TP_CTL_A")
        return False
    for mmio_data in link_idle_output:
        link_idle.asUint = mmio_data.Data
        if LINK_NORMAL_PATTERN == link_idle.dp_link_training_enable:
            logging.info(f"Link normal pattern found")
            end_time = mmio_data.TimeStamp
            logging.info(f"End Time: {end_time}")
            break
    return end_time


##
# @brief        Fetch T6 Delay
# @return       delay_time int, time taken to switch from idle to normal pattern
def calculate_t6_delay():
    start_time = fetch_link_idle()
    end_time = fetch_link_normal()
    delta_time = round((end_time - start_time) / 1000)
    return delta_time


##
# @brief        Modify T6 Parameter
# @return       True if configured else False
def modify_t6_parameter():
    gfx_vbt = Vbt()
    logging.info(gfx_vbt.version)
    if gfx_vbt.version < 260:
        logging.error("VBT version is less than 260. T6 parameter is not supported")
        return False
    logging.info(gfx_vbt.block_27.T6DelayLinkIdleTime[4])
    if gfx_vbt.block_27.T6DelayLinkIdleTime[4] != args.T6_DELAY:
        gfx_vbt.block_27.T6DelayLinkIdleTime[4] = args.T6_DELAY
        if gfx_vbt.apply_changes() is False:
            logging.error(f"VBT modification failed")
            return False
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver(Test Issue)")
            return False
        gfx_vbt.reload()
    else:
        logging.info("VBT has required value")
    return True


##
# @brief        Function to verify PPS register
# @return       True if configured else False
def verify_pps_register():
    pp_on_delays = MMIORegister.get_instance("PP_ON_DELAYS_REGISTER", "PP_ON_DELAYS", PLATFORM_NAME)
    pp_off_delays = MMIORegister.get_instance("PP_OFF_DELAYS_REGISTER", "PP_OFF_DELAYS", PLATFORM_NAME)
    pp_control = MMIORegister.get_instance("PP_CONTROL_REGISTER", "PP_CONTROL", PLATFORM_NAME)

    pp_on_delays_output = etl_parser.get_mmio_data(pp_on_delays.offset, is_write=True)
    pp_off_delays_output = etl_parser.get_mmio_data(pp_off_delays.offset, is_write=True)
    pp_control_output = etl_parser.get_mmio_data(pp_control.offset, is_write=True)

    if pp_on_delays_output is not None:
        logging.error("\tMMIO write entry found for register PP_ON_DELAYS (Not Expected)")
        return False

    if pp_off_delays_output is not None:
        logging.error("\tMMIO write entry found for register PP_OFF_DELAYS (Not Expected)")
        return False

    if pp_control_output is not None:
        logging.error("\tMMIO write entry found for register PP_CONTROL (Not Expected)")
        return False
    logging.info(f"{COLOR_GREEN}PASS: PPS MMIO Register Programming Not Found {COLOR_END}")
    return True


##
# @brief        Verify LFP status
# @return       True if configured else False
def verify_lfp_status():
    set_timing_data = None
    disable_timestamp = []
    enable_timestamp = []

    set_timing_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING, event_filter='')

    if set_timing_output is None:
        logging.error("No SetTiming event found in ETLs (Driver Issue)")
        return False

    logging.info(f"SetTiming Data: {set_timing_data}")

    disable = False
    for set_timing_data in set_timing_output:
        if set_timing_data.Enable is False:
            disable_timestamp.append(set_timing_data.TimeStamp)
            disable = True
        elif disable and set_timing_data.Enable is True:
            enable_timestamp.append(set_timing_data.TimeStamp)
            disable = False

    if len(disable_timestamp) != len(enable_timestamp):
        logging.error("Mismatch in timestamps")
        return False

    for disable, enable in zip(disable_timestamp, enable_timestamp):
        logging.info(f"Enable Time: {enable_timestamp} - Disable Time: {disable_timestamp}")
        skip_pps_delta_time = round((enable - disable), 3)
        if skip_pps_delta_time > 40:
            return False
        logging.info(f"{COLOR_GREEN}Skip PPS Delta Time: {skip_pps_delta_time} ms {COLOR_END}")
        logging.info(f"{COLOR_GREEN}PASS: SKIP PPS Verification {COLOR_END}")
        return True


##
# @brief            API to parse the commandline
# @return           args : argument list
def prepare_parser():
    parser = argparse.ArgumentParser(description='Process the Command line Arguments.')
    parser.add_argument('-TYPE', choices=['VBT', 'T6', 'SKIP_PPS'], type=str.upper,
                        help='Determines the type of run')
    parser.add_argument('-T6_DELAY', choices=[40000, 30000, 24567, 0], type=int,
                        help='Determines the value of T6 delay')
    parser.add_argument('-VALUE', choices=[40000, 30000, 24567], type=float,
                        help='Expected T6 delay')
    parser.add_argument('-PATH', default='None', type=str, help='Path to ETL File')
    args = parser.parse_args()
    return args


######################
#     Main Code      #
######################

if __name__ == '__main__':
    env_settings.set('SIMULATION', 'simulation_type', 'NONE')
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    args = prepare_parser()

    if (args.T6_DELAY or 0 == args.T6_DELAY) and args.TYPE == 'VBT':
        logging.info("Running T6 delay..")
        if modify_t6_parameter():
            logging.info(f"{COLOR_GREEN} VBT T6 delay configured {COLOR_END}")
        else:
            logging.error(f"{COLOR_RED} VBT T6 delay NOT configured {COLOR_END}")

    elif args.PATH is not None:
        etl_path = args.PATH.replace('\\', '\\\\')
        logging.info("Parsing ETL...")
        logging.info(f"ETL File Path: {etl_path}")
        if etl_parser.generate_report(etl_path) is False:
            logging.error(f"{COLOR_RED} Failed to generate ETL Parser report (Test Issue) {COLOR_END}")
            sys.exit("ETL Parsing Failed")

        if args.TYPE == 'T6':
            delta_time = calculate_t6_delay()
            logging.info(f"{COLOR_GREEN} Expected T6 delay : {args.VALUE / 10000} seconds {COLOR_END}")
            logging.info(f"{COLOR_GREEN} Actual T6 delay   : {delta_time} seconds {COLOR_END}")

            if (args.VALUE / 10000) <= delta_time <= (args.VALUE / 10000) + 1:
                logging.info(f"{COLOR_GREEN} PASS: T6 Delay {COLOR_END}")
            else:
                logging.error(f"{COLOR_RED} FAIL: T6 Delay {COLOR_END}")

        if args.TYPE == 'SKIP_PPS':
            if verify_pps_register() is False:
                logging.error(f"{COLOR_RED} FAIL: PPS Register programmed {COLOR_END}")
                sys.exit("FAIL: PPS Register programmed")
            if verify_lfp_status() is False:
                logging.error(f"{COLOR_RED} FAIL: SKIP PPS Verification {COLOR_END}")
                sys.exit("FAIL: SKIP PPS Verification")
    else:
        logging.error(f"Incomplete commandline. Please check the usage")