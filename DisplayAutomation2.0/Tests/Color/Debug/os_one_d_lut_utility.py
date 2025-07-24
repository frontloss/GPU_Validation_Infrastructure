import logging
from Tests.Color.Common import color_etl_utility


##
# To dump all the OS OneDLUT from the ETL for a given target-id
# The OneDLUT will be of size 12288 - Contains all three Blue-Green-Red channels
def dump_all_os_one_dluts_in_etl(target_id):
    os_lut = color_etl_utility.get_os_one_d_lut_from_etl(target_id)
    logging.info("Total No of OS calls : %d " %len(os_lut))
    logging.info("")
    logging.info("")
    logging.info("")
    for index in range(0, len(os_lut)):
        logging.info("*" * 128)
        logging.info("OS OneDLUT Call : %d" %index)
        logging.info(os_lut[index])
        logging.info("*"  * 128)
        logging.info("")
        logging.info("")
        logging.info("")
    return os_lut


##
# If we want to dump only one channel - Assuming that all three channels have the same value
def dump_one_channel_in_os_one_d_lut(os_lut):
    for index in range(0, len(os_lut)):
        logging.info("*" * 128)
        os_one_channel_list = list(dict.fromkeys(os_lut[index]))
        logging.info(os_one_channel_list)
        logging.info("*" * 128)
        logging.info("")
        logging.info("")
        logging.info("")


##
# To verify if all the OS calls are same;
# If the OS calls have changed, then identifies the indices where the different OS calls have started
def dump_unique_os_lut_data(os_lut):
    unique_luts = 1
    res = all(ele == os_lut[0] for ele in os_lut)
    if res:
        logging.info("There is no change in OS OneDLUTs throughout the ETL")
    else:
        logging.info("There are several different OS OneDLUTs in the ETL")
        ##
        # To logging.info the indices where the different OS calls have started
        ref_index = 0
        reference_lut = os_lut[0]
        for index in range(0, len(os_lut)):
            if reference_lut != os_lut[index]:
                logging.info("LUT %d is repeated : %d times before a new LUT comes in at index : %d" % (ref_index, (index-ref_index), index))
                reference_lut = os_lut[index]
                ref_index = index
                unique_luts += 1
    logging.info("Total unique OS LUTs %d" %unique_luts)


##
# To logging.info each B-G-R channels separately
def print_channels_one_d_lut(os_lut):
    blue_lut = []
    green_lut = []
    red_lut = []
    for index in range(0, len(os_lut), 3):
        blue_lut.append(os_lut[index])
        green_lut.append(os_lut[index + 1])
        red_lut.append(os_lut[index + 2])
    logging.info("*" * 128)
    logging.info("\t\t\t\t\t\t BLUE CHANNEL")
    logging.info(blue_lut)
    logging.info("*" *128)
    logging.info("")
    logging.info("")
    logging.info("")
    logging.info("*" * 128)
    logging.info("\t\t\t\t\t\t GREEN CHANNEL")
    logging.info(green_lut)
    logging.info("*" *128)
    logging.info("")
    logging.info("")
    logging.info("")
    logging.info("*" * 128)
    logging.info("\t\t\t\t\t\t RED CHANNEL")
    logging.info(red_lut)
    logging.info("*" *128)


