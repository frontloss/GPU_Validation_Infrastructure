########################################################################################################################
# @file         clone_pipe_verification.py
# @brief        Verifying the Expected value of a MMIO offset (related to Pipe) taken from the
#               clone_mmio_dump.json with the Actual output and making the test Pass or Fail based on the
#               verification results. The Verification results are dumped into clone_Pipe_Verification.log file.
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
    filename='clone_Pipe_Verification.log',
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
# @brief        Verifying the Expected value of each pipe MMIO offset and generate a log file.
# @param        final_required_json
# @return       None
def to_verify_actual_and_expected_pipe(final_required_json):

    # Load the Final MMIO dump JSON that has only required offsets.
    try:
        with open(final_required_json, 'r') as final_json:
            mmio_dump_data = json.loads(final_json.read())
    except Exception as e:
        logging.info(f"error: {e}")

    # Verify the Actual MMIO dump value with the Expected MMIO dump Value.
    for ofst in mmio_dump_data:

        # Verify offset 0x68180
        if ofst['MMIO Offset'] in ['0x68180', '0x68980']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check the Scalar bit (bit 31)
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                               ofst['Function Name']),
                                                             verify="Scalar is Enabled"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Scalar is not Enabled (bit: 31).",
                                                              act=ofst['Expected Output']))
                                                              
            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x68174
        elif ofst['MMIO Offset'] in ['0x68174', '0x68974']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Logic is implemented only for 1080p, need to implement the logic for other resolutions.
                # Check HActive (We are just dumping for now. Need to enhance verification to check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="XSIZE is {}".format(int(actual_mmio_value[2:16], 2
                                                                                         )), act=ofst['Expected '
                                                                                                      'Output']))
                # Check VActive (We are just dumping for now. Need to enhance verification to check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="YSIZE is {}".format(int(actual_mmio_value[19:],
                                                                                         2)), act=ofst['Expected '
                                                                                                       'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')
 
        # Verify offset 0x68170
        elif ofst['MMIO Offset'] in ['0x68170', '0x68970']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                if ofst['Expected Output'] == '0x00000000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="XPOS and YPOS is Zero"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="XPOS and YPOS should be Zero (bits: 31-0).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6001C
        elif ofst['MMIO Offset'] in ['0x6001C', '0x6101C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Logic is implemented only for 1080p, need to implement the logic for other resolutions.
                # Check HActive (We are just dumping for now. Need to enhance verification to check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Source Size is {}".format(int(
                                                             actual_mmio_value[3:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))
                # Check VActive (We are just dumping for now. Need to enhance verification to check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Source Size is {}".format(int(
                                                             actual_mmio_value[19:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70030
        elif ofst['MMIO Offset'] in ['0x70030', '0x71030']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check Dithering is enabled/disabled according to BPC.
                # Dithering should be disabled for BPC in [8, 10, 12].
                if actual_mmio_value[24:27] in ['000', '001', '100']:
                    if actual_mmio_value[27] == '0':
                        logging.info(logger_template_pass.format(res="PASS",
                                                                 ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                                 verify="Dithering is Not enabled"))
                    else:
                        logging.error(logger_template_fail.format(res="FAIL",
                                                                  ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                        ofst['Function Name']),
                                                                  verify="Dithering should Not be enabled for BPCs 8, "
                                                                         "10, 12 (bit: 4).",
                                                                  act=ofst['Expected Output']))

                # Dithering should be enabled for BPC 6.
                elif actual_mmio_value[24:27] == '010':
                    if actual_mmio_value[27] == '1':
                        logging.info(logger_template_pass.format(res="PASS",
                                                                 ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                                 verify="Dithering is enable for BPC 6."))
                    else:
                        logging.error(logger_template_fail.format(res="FAIL",
                                                                  ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                        ofst['Function Name']),
                                                                  verify="Dithering should be enabled for BPC 6 "
                                                                         "(bit: 4).",
                                                                  act=ofst['Expected Output']))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="", act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x45270
        elif ofst['MMIO Offset'] in ['0x45270', '0x45274']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Extended Fraction and Line Time",
                                                     act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x7003C
        elif ofst['MMIO Offset'] in ['0x7003C', '0x7103C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Verifying B2B Transactions Max
                if int(actual_mmio_value[7:12], 2) == 16:
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="B2B Transactions Max is 16"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="B2B Transactions Max should be equal to 16 "
                                                                     "(bits: 24-20).",
                                                              act=ofst['Expected Output']))
                    
                # Verifying B2B Transactions Delay
                if int(actual_mmio_value[12:15], 2) == 1:
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="B2B Transactions Delay is 1"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="B2B Transactions Delay should be equal to 1 "
                                                                     "(bits: 19-17).",
                                                              act=ofst['Expected Output']))
                    
                # Verifying Regulate B2B Transactions
                if actual_mmio_value[15] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Regulate B2B Transactions is enabled"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Regulate B2B Transactions should be enabled "
                                                                     "(bit: 16).",
                                                              act=ofst['Expected Output']))
                    
                # Verifying B - Credits
                if int(actual_mmio_value[19:24], 2) == 10:
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="B Credits is equal to 0A"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="B Credits should be equal to 0A (bits: 12-8).",
                                                              act=ofst['Expected Output']))
                    
                # Verifying I - Credits
                if int(actual_mmio_value[24:27], 2) == 2:
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="I Credits is equal to 2"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="I Credits should be equal to 2 (bits: 7-5).",
                                                              act=ofst['Expected Output']))
                    
                # Verifying A - Credits
                if int(actual_mmio_value[28:], 2) == 8:
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="A Credits is equal to 8"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="A Credits should be equal to 8 (bits: 3-0).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset '0x44404'
        elif ofst['MMIO Offset'] in ['0x44404', '0x44414']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Verifying Vblank
                if actual_mmio_value[-1] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Vblank is not masked"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Vblank should not be masked (bit: 0).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL",
                                                          ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x51000
        elif ofst['MMIO Offset'] in ['0x51000']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="DFSM", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70038
        elif ofst['MMIO Offset'] in ['0x70038', '0x71038']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Verifying OLED Comp Size Disable
                if actual_mmio_value[1] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Pipe Underrun Recovery is Disabled"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Pipe Underrun Recovery should be disabled "
                                                                     "(bit: 30).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')


mmio_dump_path = os.path.join(os.path.dirname(__file__), '..', 'Pre_boot', 'mmio_dump.json')
mmio_dump_path = os.path.normpath(mmio_dump_path)

to_verify_actual_and_expected_pipe(mmio_dump_path)
