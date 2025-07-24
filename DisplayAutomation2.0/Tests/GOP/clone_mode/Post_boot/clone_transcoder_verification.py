########################################################################################################################
# @file         clone_transcoder_verification.py
# @brief        Verifying the Expected value of a MMIO offset (related to Plane) taken from the
#               clone_mmio_dump.json with the Actual output and making the test Pass or Fail based on the
#               verification results. The Verification results are dumped into clone_Transcoder_Verification.log
#               file.
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
    filename='clone_Transcoder_Verification.log',
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
# @brief        Verifying the Expected value of each Transcoder MMIO offset and generate a log file.
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

        # Verify offset 0x60400
        if ofst['MMIO Offset'] in ['0x60400', '0x61400']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bits 0: HDMI Scrambling not Enabled
                if actual_mmio_value[31] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="HDMI Scrambling is not Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="HDMI Scrambling should not be Enabled (bits: 0).",
                                                              act=ofst['Expected Output']))

                # Check bits 3-1: Port Width (Need to check and write logic for other 2 types of eDP, HDMI, DP).
                if actual_mmio_value[28:31] == '011':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Port Width is 011 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Port Width should be 011 for eDP (bits: 3-1).",
                                                              act=ofst['Expected Output']))

                # Check bits 4: High TMDS Char Rate
                if actual_mmio_value[27] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="High TMDS Char Rate is not Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="High TMDS Char Rate should not be Enabled ("
                                                                     "bits: 4).",
                                                              act=ofst['Expected Output']))

                # Check bits 17-16: Sync Polarity
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Polarity of Hsync and Vsync (bits: 16-17).",
                                                         act=ofst['Expected Output']))

                # Check bits 22-20: Bits Per Color
                if actual_mmio_value[9:12] == '000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Bits Per Color (BPC) is 8."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Bits Per Color (BPC) should be 8 (bits: 22-20).",
                                                              act=ofst['Expected Output']))

                # Check bits 26-24: TRANS DDI Mode Select
                if actual_mmio_value[5:8] == '010':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="TRANS DDI Mode Select is set to 010 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="TRANS DDI Mode Select should be set to 010 for "
                                                                     "eDP (bits: 26-24).",
                                                              act=ofst['Expected Output']))

                # Check bits 30-27: DDI Select
                if actual_mmio_value[1:5] == '0001':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="DDI Select is set to 0001 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="DDI Select should be set to 0001 for eDP (bits: "
                                                                     "30-27).",
                                                              act=ofst['Expected Output']))

                # Check bits 31: TRANS DDI Function Enable
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Transcoder DDI function is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Transcoder DDI function should be Enabled ("
                                                                     "bits: 31).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x46140
        elif ofst['MMIO Offset'] in ['0x46140', '0x46144']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 31-28: Trans Clock Select
                if actual_mmio_value[0:4] == '0001':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Trans Clock Select is set to 0001 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Trans Clock Select should be set to 0001 for "
                                                                     "eDP (bits: 31-28).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL",
                                                          ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x70008
        elif ofst['MMIO Offset'] in ['0x70008', '0x71008']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 31: Transcoder Enable
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Transcoder is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Transcoder should be Enabled (bits: 31).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60040
        elif ofst['MMIO Offset'] in ['0x60040', '0x61040']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Transcoder Link M Value 1", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F040
        elif ofst['MMIO Offset'] in ['0x6F040', '0x6F140']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Transcoder Link M Value 1 CMTG0",
                                                     act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60044
        elif ofst['MMIO Offset'] in ['0x60044', '0x61044']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Transcoder Link N Value 1", act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F044, 0x6F144
        elif ofst['MMIO Offset'] in ['0x6F044', '0x6F144']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            # WM need some extra calculation. So just dumping the value.
            logging.info(logger_template_dump.format(res="DUMP", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                     verify="Transcoder Link N Value 1 CMTG0",
                                                     act=ofst['Expected Output']))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60000
        elif ofst['MMIO Offset'] in ['0x60000', '0x61000']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Active (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Active is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Total (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Total is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F000
        elif ofst['MMIO Offset'] in ['0x6F000', '0x6F100']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Active (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Active is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Total (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Total is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60004
        elif ofst['MMIO Offset'] in ['0x60004', '0x61004']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Blank Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Blank Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Blank End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Blank End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F004
        elif ofst['MMIO Offset'] in ['0x6F004', '0x6F104']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Blank Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Blank Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Blank End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Blank End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60008
        elif ofst['MMIO Offset'] in ['0x60008', '0x61008']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Sync Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Sync Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Sync End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Sync End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F008, 0x6F108
        elif ofst['MMIO Offset'] in ['0x6F008', '0x6F108']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Horizontal Sync Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Sync Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Horizontal Sync End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Horizontal Sync End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6000C
        elif ofst['MMIO Offset'] in ['0x6000C', '0x6100C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Active (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Active is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Total (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Total is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F00C
        elif ofst['MMIO Offset'] in ['0x6F00C', '0x6F10C']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Active (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Active is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Total (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Total is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60010
        elif ofst['MMIO Offset'] in ['0x60010', '0x61010']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Blank Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Blank Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Blank End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Blank End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F010
        elif ofst['MMIO Offset'] in ['0x6F010', '0x6F110']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Blank Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Blank Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Blank End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Blank End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60014
        elif ofst['MMIO Offset'] in ['0x60014', '0x61014']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Sync Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Sync Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Sync End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Sync End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x6F014
        elif ofst['MMIO Offset'] in ['0x6F014', '0x6F114']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 13-0: Vertical Sync Start (We are just dumping for now. Need to enhance verification to
                # check dynamically)
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Sync Start is {}".format(int(
                                                             actual_mmio_value[18:], 2) + 1), act=ofst['Expected '
                                                                                                       'Output']))
                # Check bits 29-16: Vertical Sync End (Logic written only for 1080p. Need to check other two cases of
                # eDP and write logic for them.)
                # We are just dumping for now. Need to enhance verification to check dynamically
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Vertical Sync End is {}".format(int(
                                                             actual_mmio_value[2:16], 2) + 1), act=ofst['Expected '
                                                                                                        'Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x60540
        elif ofst['MMIO Offset'] in ['0x60540', '0x61540']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 10-8: DP Link Training Enable
                if actual_mmio_value[21:24] == '011':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="DP Link not in Training."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="DP Link should not be in Training (bits: 10-8).",
                                                              act=ofst['Expected Output']))

                # Check bits 18: Enhanced Framing Enable
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Enhanced Framing (bits: 18).",
                                                         act=ofst['Expected Output']))

                # Check bits 30: FEC Enable
                if actual_mmio_value[1] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="FEC is not Enable"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="FEC should not be Enable (bits: 30).",
                                                              act=ofst['Expected Output']))

                # Check bits 31: Transport Enable
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Transport is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Transport should be Enabled (bits: 31).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x46070
        elif ofst['MMIO Offset'] in ['0x46070']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 7-0: PLL Ratio
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="CDCLK PLL divider ratio (bits: 7-0).",
                                                         act=ofst['Expected Output']))

                # Check bits 30: PLL Lock
                if actual_mmio_value[1] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Status of the CDCLK PLL is Locked."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Status of the CDCLK PLL should be Locked (bits: "
                                                                     "30).",
                                                              act=ofst['Expected Output']))

                # Check bits 31: PLL Enable
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="CDCLK PLL is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="CDCLK PLL should be Enabled (bits: 31).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x46008
        elif ofst['MMIO Offset'] in ['0x46008']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 15-0: Squash Waveform
                logging.info(logger_template_dump.format(res="DUMP",
                                                         ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                               ofst["Function Name"]),
                                                         verify="Squash Waveform (bits: 15-0).",
                                                         act=ofst['Expected Output']))

                # Check bits 27-24: Squash Window Size
                if actual_mmio_value[4:8] == '1111':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Squash Window Size is default equalto 16."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Squash Window Size should be default equalto 16 "
                                                                     "(bits: 27-24).",
                                                              act=ofst['Expected Output']))

                # Check bits 31: Squash Enable
                logging.info(logger_template_dump.format(res="DUMP",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Squashing (bits: 31).",
                                                             act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x46000
        elif ofst['MMIO Offset'] in ['0x46000']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bits 21-19: CD2X Pipe Select
                if actual_mmio_value[10:13] == '000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="CD2X Pipe Select is set to 000 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="CD2X Pipe Select should be set to 000 for eDP ("
                                                                     "bits: 21-19).",
                                                              act=ofst['Expected Output']))

                # Check bits 22-23: CD2X Divider Select (for only LNL 10 and for others 00. Need to check the 
                # platformspecific implementation. Added for PTL+ platforms for now.)
                if actual_mmio_value[8:10] == '00':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="CD2X Divider Select is default set to 00."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="CD2X Divider Select should be default set to 00 ("
                                                              "bits: 23-22).",
                                                              act=ofst['Expected Output']))

                # Check bits 25: MDCLK Source Select
                if actual_mmio_value[6] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="Source for the memory clock MDCLK is default "
                                                                    "CD2XCLK."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Source for the memory clock MDCLK should be "
                                                                     "default CD2XCLK (bits: 25).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0xC4030
        elif ofst['MMIO Offset'] in ['0xC4030']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 3: DDIA HPD Enable
                if actual_mmio_value[28] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="DDIA HPD is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="DDIA HPD should be Enabled (bits: 3).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0xC4000
        elif ofst['MMIO Offset'] in ['0xC4000']:
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])

                # Check bit 16: Hotplug DDIA
                if actual_mmio_value[15] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst['Function Name']),
                                                             verify="EDP Hotplug is Detected."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="EDP Hotplug should be Detected. (bits: 16).",
                                                              act=ofst['Expected Output']))

                # Check bit 17: Hotplug DDIB
                if actual_mmio_value[14] == '0':
                    logging.info(logger_template_pass.format(res="PASS", ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                               ofst['Function Name']),
                                                             verify="Hotplug DDIB is not Detected."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst['Function Name']),
                                                              verify="Hotplug DDIB should not be Detected. (bits: 17).",
                                                              act=ofst['Expected Output']))

                # Check bit 3: DDIA HPD Enable
                logging.info(logger_template_dump.format(res="DUMP",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PICA Interrupt (bits: 31).",
                                                             act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')


mmio_dump_path = os.path.join(os.path.dirname(__file__), '..', 'Pre_boot', 'mmio_dump.json')
mmio_dump_path = os.path.normpath(mmio_dump_path)

to_verify_actual_and_expected_plane(mmio_dump_path)
