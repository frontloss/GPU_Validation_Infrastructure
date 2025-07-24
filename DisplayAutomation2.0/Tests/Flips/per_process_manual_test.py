########################################################################################################################
# @file         per_process_manual_test.py
# @brief        The script contains verification and ETL parsing logic for Per Process Manual tests
#               Usage:
#                  per_process_manual_test.py [-h] [-GAME] [-GLOBAL] [-PER_GAME] [-ETL_PATH PATH]
# @author       Joshi, Prateek
########################################################################################################################
import argparse
import logging
import os
import sys

from Libs import env_settings
from Libs.Core import etl_parser
from Libs.Core.logger import display_logger
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper
from Tests.VirtualDisplay.Yangra import virtual_display_helper

LINE_WIDTH = 100
SIZE_OF_PROCESS_CONFIG_TABLE = 128

# Folder path
__ETL_FOLDER = test_context.ROOT_FOLDER
ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1


##
# @brief            API to parse the commandline
# @return           args : argument list
def prepare_parser():
    parser = argparse.ArgumentParser(description='Process the Command line Arguments.')
    parser.add_argument('-GAME', type=str,
                        help='Determines the name of Game')
    parser.add_argument('-GLOBAL', type=str, choices=['SMOOTH_SYNC', 'VSYNC_ON', 'CAPPED_FPS', 'SPEED_SYNC',
                                                      'VSYNC_OFF'],
                        help='Determines the Global Gaming Feature')
    parser.add_argument('-PER_GAME', choices=['SMOOTH_SYNC', 'VSYNC_ON', 'CAPPED_FPS', 'SPEED_SYNC', 'VSYNC_OFF'],
                        type=str, help='Determines the Per Process Gaming Feature')
    parser.add_argument('-ETL_PATH', default='None', type=str, help='Path to ETL File to verify')
    args_data = parser.parse_args()
    return args_data


########################################################################################################################
# Verification


##
# @brief            Verify Per Process Gaming Features.
# @param[in]        etl_file; name of the ETL file to be verified.
# @param[in]        game_name; Game name.
# @param[in]        game_setting; Per_Game Gaming Feature Setting.
# @return           True if verification is pass else False.
def verify_per_process_manual(etl_file, game_name, game_setting):
    logging.info(" Per Process Verification ".center(LINE_WIDTH, "*"))
    process_data = []
    process_config_data_list = []
    valid_entries = 0
    add_count, remove_count = 0, 0
    update_flip_count = 0
    process_id = 0

    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate EtlParser report, Rerun")
        return False

    ##
    # Get Process config data
    process_config_table_data = etl_parser.get_event_data(etl_parser.Events.PROCESS_CONFIG_TABLE)
    if process_config_table_data is None:
        logging.error("\tFAIL: Event process_config_table_data missing from ETL, Collect ETL Again - Start ETL before "
                      "game launch")
        return False

    ##
    # Get Flip Process Details
    flip_process_data = etl_parser.get_event_data(etl_parser.Events.FLIP_PROCESS_DETAILS)
    if flip_process_data is None:
        logging.error("\tFAIL: Event flip_process_data missing from ETL, Collect ETL Again - Start ETL before game "
                      "launch ")
        return False

    ##
    # Get Layer Index for Plane ID data
    layer_index_plane_id_data = etl_parser.get_event_data(etl_parser.Events.HW_PLANE_LAYER_INDEX)
    if layer_index_plane_id_data is None:
        logging.error("\tFAIL: Event layer_index_plane_id_data missing from ETL, Collect ETL Again - Start ETL before "
                      "game launch ")
        return False

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(game_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")
            else:
                process_id = each_flip_process.ProcessId

    ##
    # Validate Process Config Table Entry
    for each_process_config in process_config_table_data:
        if valid_entries < each_process_config.NumValidEntries:
            valid_entries = each_process_config.NumValidEntries
        if each_process_config.ProcessId == process_id:

            # Check if Action is Read, then continue to check for next entry in ProcessConfigTable
            if each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_READ':
                continue

            ##
            # Verify Gaming mode when action is add
            logging.debug("Verify Gaming mode when action is add")
            if each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_ADD':
                if flip_helper.get_gaming_sync_mode_name(game_setting) != each_process_config.GamingSyncMode:
                    logging.error(f"Gaming mode is not matching with expected mode Applied "
                                  f"{each_process_config.GamingSyncMode} Expected "
                                  f"{flip_helper.get_gaming_sync_mode_name(game_setting)}")
                add_count = add_count + 1
            process_config_data_list.append((each_process_config.ProcessId, each_process_config.ProcessName,
                                             each_process_config.GamingSyncMode, each_process_config.FlipSubmissionDone,
                                             each_process_config.Action, each_process_config.TimeStamp))

            ##
            # Check if Action is Update flip submission when Gaming feature is applied with FlipSubmissionDone as True
            logging.debug("Verify Gaming mode when action is update flip submission")
            if (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION') \
                    and (each_process_config.FlipSubmissionDone == 'True'):
                logging.info(f"Gaming Feature - {each_process_config.GamingSyncMode} is set during timestamp "
                             f"- {each_process_config.TimeStamp}")
            elif (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_REF_COUNT') and \
                    (each_process_config.FlipSubmissionDone == 'True'):
                logging.info(f"Gaming Feature - {each_process_config.GamingSyncMode} reference count updated "
                             f"during timestamp - {each_process_config.TimeStamp}")

            ##
            # Verify Gaming mode when action is remove / update reference count
            logging.debug("Verify Gaming mode when action is remove / update reference count")
            if (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_REMOVE') or \
                    (each_process_config.Action == 'DD_PROCESS_ENTRY_ACTION_UPDATE_REF_COUNT'):
                if each_process_config.GamingSyncMode != 'DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT':
                    logging.error(f"Gaming mode is not matching with expected mode Applied "
                                  f"{each_process_config.GamingSyncMode} Expected "
                                  f"DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT with Action {each_process_config.Action}")
                remove_count = remove_count + 1

            process_data.append((each_process_config.ProcessName, each_process_config.GamingSyncMode,
                                 each_process_config.FlipSubmissionDone,
                                 each_process_config.Action, each_process_config.TimeStamp))

    for flip_sub_event in process_data:
        if flip_sub_event[3] == 'DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION':
            logging.info(f"Gaming {flip_sub_event[0]} Feature is enabled, flips received from "
                         f"game/app")
            update_flip_count += 1
        else:
            continue

    if update_flip_count == 0:
        logging.error(f"Gaming Feature is not enabled, we did not get Mpo3Flip call for game/app "
                      f"- No UPDATE_FLIP_SUBMISSION from Game/App")

    if add_count != remove_count:
        logging.warning(f"Add and remove counts are not matching Add Count - {add_count} Remove Count - {remove_count}")

    if valid_entries > SIZE_OF_PROCESS_CONFIG_TABLE:
        logging.warning(f"Exceeded process config table entry size, Value: {valid_entries}")

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(game_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")

    for data_element in process_data:
        logging.info(f"ProcessConfigTable - {data_element} \n ")

    logging.debug(f" DEBUG PURPOSE ONLY \n ".center(100, "*"))

    for config_element in process_config_data_list:
        logging.debug(f" Process Config Table List - {config_element} \n ")


########################################################################################################################
# Main Code
logging.info("Test purpose: Verify Per Process Gaming Features from Manual ETLs")
env_settings.set('SIMULATION', 'simulation_type', 'NONE')
TestEnvironment.load_dll_module()
display_logger._initialize(console_logging=True)
args = prepare_parser()
etl_path = args.ETL_PATH.replace('\\', '\\\\')
virtual_display_helper.initialize(sys.argv)
logging.info("  Parsing ETL to verify Per Process   ".center(LINE_WIDTH, "*"))
logging.info(f" ETL File Path: {etl_path}")
status = verify_per_process_manual(etl_path, args.GAME, args.PER_GAME)
if status is False:
    logging.error("Collect ETL again - Events are missing in ETL")

logging.info("  Verify log with below parameters, If parameters are correct. Mark Test case as Pass else Fail !! \n ")
logging.info("  We should see these entries in Process Config table log \n "
             " Feature - Gaming feature passed in command line should match for all entries \n "
             "For a. Action - DD_PROCESS_ENTRY_ACTION_NO_ACTION - (In case if we get No Action event, verify "
             "       expectation -process name and feature should match from command line)\n"
             "    b. Action - DD_PROCESS_ENTRY_ACTION_ADD - Process name and feature should match from command line \n"
             "    c. Action - DD_PROCESS_ENTRY_ACTION_READ - Process name and feature should match from command line \n"
             "    d. Action - DD_PROCESS_ENTRY_ACTION_UPDATE_FLIP_SUBMISSION - Process name, feature and flag as true "
             "       should match from command line \n "
             "    e. Action - DD_PROCESS_ENTRY_ACTION_UPDATE_SYNC_MODE - Process name should name \n "
             "    f. Action - DD_PROCESS_ENTRY_ACTION_REMOVE - Process name should match from command line with "
             "       feature as DD_GAMING_SYNC_MODE_APPLICATION_DEFAULT \n")
sys.exit("  Per Process verification completed  ".center(LINE_WIDTH, "*"))
