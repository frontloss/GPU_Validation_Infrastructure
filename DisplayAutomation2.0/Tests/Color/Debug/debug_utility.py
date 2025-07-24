########################################################################################################################
# @file         debug_utility.py
# @brief        The test script contains Etl parsing  logic for collecting debug data
#               Usage:debug_utility.py [-h] [-TYPE TYPE] [-PATH PATH]
#               optional arguments:
#               -h, --help  show this help message and exit
#               -TYPE TYPE  Type
#               -PATH PATH  Path to ETL File
#               example - python debug_utility.py -etl <path_to_etl>
# @author       Siva Thangaraja
########################################################################################################################
import argparse
import logging
import os

from Libs.Core import etl_parser
from Tests.Color.Debug import os_one_d_lut_utility

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOG_FOLDER = os.path.join(ROOT_FOLDER, 'Logs')
LINE_WIDTH = 64
etl_path = None


##
# @brief            API to parse the commandline
# @return           args : argument list
def prepare_parser():
    parser = argparse.ArgumentParser(description='Process the Command line Arguments.')
    parser.add_argument('-TYPE', default='ETL', type=str.upper, help='Type')
    parser.add_argument('-PATH', default='None', type=str, help='Path to ETL File')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = prepare_parser()
    scriptName = os.path.basename(__file__).replace(".py", ".txt")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(filename=scriptName,
                        filemode='w',
                        format=FORMAT,
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    if 'ETL' in args.TYPE and args.PATH != 'None':
        etl_path = args.PATH.replace('\\', '\\\\')
    else:
        assert False, "Provide the Etl file path"

    logging.debug("Parsing ETL for Color".center(LINE_WIDTH, "*"))
    logging.debug(f"ETL File Path: {etl_path}")

    if etl_parser.generate_report(etl_path) is False:
        assert False, "Failed to generate EtlParser report"
    logging.debug("Successfully generated EtlParser report")

    ##
    # To fetch target id
    os_mode_data = etl_parser.get_event_data(etl_parser.Events.TRANSLATED_OS_MODE)
    if os_mode_data is None:
        assert False, "Translated OS Mode Data not Found"

    target_id_set = set()
    for each_data in os_mode_data:
        target_id_set.add(each_data.TargetId)
    logging.debug(f"TargetId: {target_id_set}")

    ##
    # The fetch pipe id
    set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)
    if set_timing_data is None:
        assert False, "Set Timing Data not Found"

    pipe_set = set()
    for each_data in set_timing_data:
        pipe_set.add(each_data.Pipe)
    logging.debug(f"Pipe: {pipe_set}")

    ##
    # To Dump all the OS OneDLUT for a target id
    for each_target_id in target_id_set:
        logging.debug(f"Dumping OS OneDLUT for target_id {each_target_id}".center(LINE_WIDTH, "*"))
        os_lut = os_one_d_lut_utility.dump_all_os_one_dluts_in_etl(each_target_id)

        ##
        # To verify if all the OS OneDLuts are same in the ETL
        # If there are different Luts, identify the indices where there are different LUTs
        os_one_d_lut_utility.dump_unique_os_lut_data(os_lut)

        ##
        # To dump only one channel - Assuming that all three channels have the same value
        os_one_d_lut_utility.dump_one_channel_in_os_one_d_lut(os_lut)

        ##
        # To print each B-G-R channels separately
        for lut_index in range(0, len(os_lut)):
            os_one_d_lut_utility.print_channels_one_d_lut(os_lut[lut_index])

    logging.debug("Dumped the color data successfully".center(LINE_WIDTH, "*"))
