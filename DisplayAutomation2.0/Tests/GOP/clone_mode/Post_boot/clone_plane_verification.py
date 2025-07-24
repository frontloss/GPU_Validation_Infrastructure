########################################################################################################################
# @file         clone_plane_verification.py
# @brief        Verifying the Expected value of a MMIO offset (related to Plane) taken from the
#               clone_mmio_dump.json with the Actual output and making the test Pass or Fail based on the
#               verification results. The Verification results are dumped into clone_Plane_Verification.log file.
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import json
import logging
import os

logger_template_pass = "{res:^5}: {ofst:<60}: {verify:<35}"
logger_template_fail = "{res:^5}: {ofst:<60}: {verify:<100}: Actual MMIO: {act}"
logger_template_dump = "{res:^5}: {ofst:<60}: {verify:<100}: Actual MMIO: {act}"

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)5s - %(message)s',
    filename='clone_Plane_Verification.log',
    filemode='w'
    )


##
# @brief        to convert offset (Hexadecimal string) to 32-bit Binary string.
# @param        hex_num
# @return       actual_mmio_value (32-bit Binary string)
def convert_hex_to_32bit_binary(hex_num):
    actual_mmio_value = int(hex_num, 16)
    actual_mmio_value &= 0xFFFFFFFF
    actual_mmio_value = str(format(actual_mmio_value, '032b'))
    return actual_mmio_value


##
# @brief        Verifying the Expected value of each plane MMIO offset and generate a log file.
# @param        final_required_json
# @return       None
def to_verify_actual_and_expected_plane(final_required_json):

    # Load the Final MMIO dump JSON that has only required offsets.
    try:
        with open(final_required_json, 'r') as final_json:
            mmio_dump_data = json.loads(final_json.read())
    except Exception as e:
        logging.info(f"error: {e}")

    # Verify the Actual MMIO dump value with the Expected MMIO dump Value.
    for ofst in mmio_dump_data:

        # Verify offset 0x7019C
        if ofst['MMIO Offset'] in ['0x7019C', '0x7119C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Surface Base Address", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70240
        elif ofst['MMIO Offset'] in ['0x70240', '0x71240']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70244
        elif ofst['MMIO Offset'] in ['0x70244', '0x71244']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70248
        elif ofst['MMIO Offset'] in ['0x70248', '0x71248']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x7024C
        elif ofst['MMIO Offset'] in ['0x7024C', '0x7124C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70250
        elif ofst['MMIO Offset'] in ['0x70250', '0x71250']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70254
        elif ofst['MMIO Offset'] in ['0x70254', '0x71254']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Watermarks", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70258
        elif ofst['MMIO Offset'] in ['0x70258', '0x71258']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane SAGV Watermark", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70180
        elif ofst['MMIO Offset'] in ['0x70180', '0x71180']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check if color format is RGB and Plane is Enabled.
                if actual_mmio_value[4:9] == '01000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Color Format is RGB"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Color Format should be RGB (bits: 27-23)",
                                                              act=ofst['Expected Output']))
                # Check if Plane is Enabled.
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Plane is Enabled"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Plane should be Enabled (bits: 31)",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70190
        elif ofst['MMIO Offset'] in ['0x70190', '0x71190']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Logic is implemented only for 1080p, need to implement the logic for other resolutions.
                # Check HActive and VActive (We are just dumping for now. Need to enhance verification to check
                # dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Height of the plane in lines is {}".format(int(
                                                             actual_mmio_value[3:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))
                # Check VActive (We are just dumping for now. Need to enhance verification to check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Width of the plane in pixels is {}".format(int(
                                                             actual_mmio_value[19:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL",
                                                          ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x7027C
        elif ofst['MMIO Offset'] in ['0x7027C', '0x7127C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Plane Buffer Config", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')


mmio_dump_path = os.path.join(os.path.dirname(__file__), '..', 'Pre_boot', 'mmio_dump.json')
mmio_dump_path = os.path.normpath(mmio_dump_path)

to_verify_actual_and_expected_plane(mmio_dump_path)
