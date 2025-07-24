########################################################################################################################
# @file         single_pipe_port_verification.py
# @brief        Verifying the Expected value of a MMIO offset (related to Plane) taken from the
#               single_pipe_MMIO_dump.json with the Actual output and making the test Pass or Fail based on the
#               verification results. The Verification results are dumped into single_Pipe_Port_Verification.log file.
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import json
import logging
import os
import sys

logger_template_pass = "{res:^5}: {ofst:<60}: {verify:<35}"
logger_template_fail = "{res:^5}: {ofst:<60}: {verify:<100}: Actual MMIO: {act}"
logger_template_dump = "{res:^5}: {ofst:<60}: {verify:<100}: Actual MMIO: {act}"

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)5s - %(message)s',
    filename='single_port_verification.log',
    filemode='w'
    )

if len(sys.argv) < 2:
    logging.info("Expected port as argument")
    sys.exit(1)


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
# @brief        Verifying the Expected value of each port MMIO offset and generate a log file.
# @param        final_required_json
# @return       None
def to_verify_actual_and_expected_plane(final_required_json):
    port = sys.argv[1]
    port_offset_dict = {'-CTL_A': ['0x16FA00', '0x16FA04', '0x16FA08', '0x64000', '0x16FA10', '0x16FA60'],
                        '-USBC0': ['0x16F200', '0x16F204', '0x16F208', '0x64300', '0x16F210', '0x16F260'],
                        '-USBC1': ['0x16F400', '0x16F404', '0x16F408', '0x64400', '0x16F410', '0x16F460'],
                        '-USBC2': ['0x16F600', '0x16F604', '0x16F608', '0x64500', '0x16F610', '0x16F660'],
                        '-USBC3': ['0x16F800', '0x16F804', '0x16F808', '0x64600', '0x16F810', '0x16F860']}

    # Load the Final MMIO dump JSON that has only required offsets.
    try:
        with open(final_required_json, 'r') as final_json:
            mmio_dump_data = json.loads(final_json.read())
    except Exception as e:
        logging.info(f"error: {e}")

    # Verify the Actual MMIO dump value with the Expected MMIO dump Value.
    for ofst in mmio_dump_data:      
            
        # Verify offset 0x16FA00
        if (ofst['MMIO Offset'] in ['0x16FA00', '0x16F200', '0x16F400', '0x16F600', '0x16F800']
                and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Check if bit-0: HDMI FRL Shifter Enable
                if actual_mmio_value[31] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="HDMI FRL Shifter is not Enabled"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="HDMI FRL Shifter Should not be Enabled (bit: 0).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 3-1: Port Width (Need to check and write logic for other 2 types of eDP).
                if actual_mmio_value[28:31] == '011':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Port Width is 011"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Port Width should be 011 for eDP (bits: 3-1).",
                                                              act=ofst['Expected Output']))
                    
                # Check if bit-7: PHY should not be in Idle Status
                if actual_mmio_value[24] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY is not idle"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY should not be idle (bits: 7)",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 15-12: PHY Mode (This logis is for LNL, PTL, WCL. Need to check and write logic for
                # other platforms)
                if actual_mmio_value[16:20] == '1001':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Mode is set default to 1001."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Mode should be set default to 1001 (bits: "
                                                                     "15-12).",
                                                              act=ofst['Expected Output']))
                    
                # Check if bit-16: Port Reversal
                if actual_mmio_value[15] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Port is not Reversed"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Port should not be Reversed(bits: 16).",
                                                              act=ofst['Expected Output']))
                    
                # Check if bit-19-18: PHY Data Lane Width
                if actual_mmio_value[12:14] == '00':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY data lane width is 00"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY data lane width should be set to 00 for eDP "
                                                                     "(bits: 19-18).",
                                                              act=ofst['Expected Output']))
                    
                # Check if bit-24: SoC PHY Ready
                if actual_mmio_value[7] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="SoC has made the PHY ready for use."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="SoC should make the PHY ready for use "
                                                                     "(bits: 24).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x16FA04
        elif (ofst['MMIO Offset'] in ['0x16FA04', '0x16F204', '0x16F404', '0x16F604', '0x16F804']
              and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Check Power state in Ready, Powerdown New State, Powerdown Update, PHY Pulse Status, PHY Current
                # Status, Pipe Reset
                if actual_mmio_value[24:28] == '0010':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PSR and mode set link disable powerdown state is "
                                                                    "equal to 2."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PSR and mode set link disable powerdown state "
                                                                     "should be equal to 2 (bits: 7-4).",
                                                              act=ofst['Expected Output']))
                
                # Check Powerdown New State for Lane 1
                if actual_mmio_value[12:16] == '0010':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="new PHY Lane 1 powerdown state is set default to "
                                                                    "0010."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="new PHY Lane 1 powerdown state should be set "
                                                                     "default to 0010 (bits: 19-16).",
                                                              act=ofst['Expected Output']))
                    
                # Check Powerdown New State for Lane 0
                if actual_mmio_value[8:12] == '0010':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="new PHY Lane 0 powerdown state is set default to "
                                                                    "0010."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="new PHY Lane 0 powerdown state should be set "
                                                                     "default to 0010 (bits: 23-20).",
                                                              act=ofst['Expected Output']))
                    
                # Check Lane1 Powerdown Update
                if actual_mmio_value[7] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Lane1 Powerdown Update is not updated"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Lane1 Powerdown should not be Updated "
                                                                     "(bits: 24).",
                                                              act=ofst['Expected Output']))
                    
                # Check Lane0 Powerdown Update
                if actual_mmio_value[6] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Lane0 Powerdown Update is not updated"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Lane0 Powerdown should not be Updated "
                                                                     "(bits: 25).",
                                                              act=ofst['Expected Output']))
                
                # Check Lane1 PHY Pulse Status
                if actual_mmio_value[5] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Lane1 PHY Pulse Status is 1."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Lane1 PHY Pulse Status should be 1 (bits: 26).",
                                                              act=ofst['Expected Output']))
                
                # Check Lane0 PHY Pulse Status
                if actual_mmio_value[4] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Lane0 PHY Pulse Status is 1."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Lane0 PHY Pulse Status should be 1 (bits: 27).",
                                                              act=ofst['Expected Output']))
                
                # Check Lane1 PHY Current Status
                if actual_mmio_value[3] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="current PHY status of lane 1 is 0."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="current PHY status of lane 1 should be 0 (bits: "
                                                                     "28).",
                                                              act=ofst['Expected Output']))
                
                # Check Lane0 PHY Current Status
                if actual_mmio_value[2] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="current PHY status of lane 0 is 0."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="current PHY status of lane 1 should be 0 (bits: "
                                                                     "29).",
                                                              act=ofst['Expected Output']))
                    
                # Check PHY Current Status, Pipe Reset
                if actual_mmio_value[0] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Lane 1 is Out of Reset."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Lane 1 should be Out of Reset (bits: 30).",
                                                              act=ofst['Expected Output']))
                    
                # Check PHY Current Status, Pipe Reset
                if actual_mmio_value[1] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Lane 0 is Out of Reset"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Lane 0 should be Out of Reset (bits: 31).",
                                                              act=ofst['Expected Output']))
                    
            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x16FA08
        elif (ofst['MMIO Offset'] in ['0x16FA08', '0x16F208', '0x16F408', '0x16F608', '0x16F808']
              and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Check bits 3-0: Power State in Active
                if actual_mmio_value[28:] == '0000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="active powerdown state is equal to 0."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="active powerdown state should be equal to 0 ("
                                                                     "bits: 3-0).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 15-8: PLL Lane Staggering Delay
                if actual_mmio_value[16:24] == '00000000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PLL Lane Staggering Delay is equal to 0."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PLL Lane Staggering Delay should be equal to 0 "
                                                                     "(bits: 15-8).",
                                                              act=ofst['Expected Output']))
                    
            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x64000
        elif (ofst['MMIO Offset'] in ['0x64000', '0x64300', '0x64400', '0x64500', '0x64600']
              and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                    
                # Check bits 3-1: Port Width (Need to check and write logic for other 2 types of eDP).
                if actual_mmio_value[28:31] == '011':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Port Width is set to 011 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Port Width should be set to 011 for eDP (bits: "
                                                                     "3-1).",
                                                              act=ofst['Expected Output']))
                
                # Check bits 7: PHY should not be in Idle Status
                if actual_mmio_value[24] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="DDI is not idle"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="DDI should not be idle (bits: 7)",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 16: Port Reversal
                if actual_mmio_value[15] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Port Reversal is not True."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Port Reversal should not be True.",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 19-18: Data Width
                if actual_mmio_value[12:14] == '00':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY data lane width is set to 00 for eDP."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY data lane width should be set to 00 for "
                                                                     "eDP (bits: 19-18).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 31: DDI data enable and Valid output
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="DDI data and valid output is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="DDI data and valid output should be Enabled.",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x16FA10
        elif (ofst['MMIO Offset'] in ['0x16FA10', '0x16F210', '0x16F410', '0x16F610', '0x16F810']
              and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Check bits 4-0: Sync Pulse Count
                if actual_mmio_value[27:] == '11111':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Sync Pulse Count is 31(32-1)."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Sync Pulse Count should be 31(32-1) (bits: 4-0).",
                                                              act=ofst['Expected Output']))
                        
                # Check bits 18: PHY Power State
                if actual_mmio_value[13] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Power State is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Power State should be Enabled (bits: 18).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 19: PHY Power Request
                if actual_mmio_value[12] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Power Request is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Power Request should be Enabled (bits: 19).",
                                                              act=ofst['Expected Output']))

                # Check bits 27-26: In Refactor we should program PortA – 600us
                # This will fail for Legacy GOP. Because we are programming different for LNL and PTL+ Platforms.
                # need to implement Platform based verification.
                if ofst['MMIO Offset'] == '0x16FA10':
                    if actual_mmio_value[4:6] == '01':
                        logging.info(logger_template_pass.format(res="PASS",
                                                                 ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                                 verify="Time out timer value is set default to "
                                                                        "01(600us) for Port A."))
                    else:
                        logging.error(logger_template_fail.format(res="FAIL",
                                                                  ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                        ofst['Function Name']),
                                                                  verify="Time out timer value should be set default to"
                                                                         " 01(600us) for Port A (bits: 27-26).",
                                                                  act=ofst['Expected Output']))

                # Check bits 27-26: In Refactor we should program 4000us for ports other than PortA.
                else:
                    if actual_mmio_value[4:6] == '11':
                        logging.info(logger_template_pass.format(res="PASS",
                                                                 ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                       ofst['Function Name']),
                                                                 verify="Time out timer value is set default to "
                                                                        "11(4000us) for ports except Port A."))
                    else:
                        logging.error(logger_template_fail.format(res="FAIL",
                                                                  ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                        ofst['Function Name']),
                                                                  verify="Time out timer value should be set default to"
                                                                         " 11(4000us) for ports except Port A.(bits: "
                                                                         "27-26).",
                                                                  act=ofst['Expected Output']))
                    
                # Check bits 28: Time out error
                if actual_mmio_value[3] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="No Time out error."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Time out error (bits: 28).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')

        # Verify offset 0x16FA60
        elif (ofst['MMIO Offset'] in ['0x16FA60', '0x16F260', '0x16F460', '0x16F660', '0x16F860']
              and ofst['MMIO Offset'] in port_offset_dict[port]):
            logging.info(f'-----Verifying {ofst["Function Name"]} -----')
            if ofst['Expected Output'] is not None:
                actual_mmio_value = convert_hex_to_32bit_binary(ofst['Expected Output'])
                
                # Check bits 0: SSC Enable PLL B.
                if actual_mmio_value[31] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="spread-spectrum clocking on the PHY PLL B is "
                                                                    "Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="spread-spectrum clocking on the PHY PLL B "
                                                                     "should be Enabled (bits: 0s).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 8: PHY Clock Lane Select.
                if actual_mmio_value[23] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PHY Clock Lane Select is 0 for eDP"))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PHY Clock Lane Select should be 0 for eDP ("
                                                                     "bits: 8s).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 10: Forward Clock Ungate.
                if actual_mmio_value[21] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="Forward clock (Pclk) on the port slice output is "
                                                                    "Ungate."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="Forward clock (Pclk) on the port slice output "
                                                                     "should be Ungate (bits: 10).",
                                                              act=ofst['Expected Output']))
                
                # Check bits 16-12: DDI Clock Select, Need to confirm bits 8, 10, 21-31.
                if actual_mmio_value[15:20] == '01000':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="DDI Clock Select is Maxpclk."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="DDI Clock Select should be Maxpclk "
                                                                     "(bits: 16-12).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 24: PCLK Refclk Ack LN1.
                if actual_mmio_value[7] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK refclk ack for lane 1 is not Acknowledged."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK refclk ack for lane 1 should not be "
                                                                     "Acknowledged (bits: 24).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 25: PCLK Refclk Request LN1.
                if actual_mmio_value[6] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK refclk Request for lane 1 is not Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK refclk Request for lane 1 should not be "
                                                                     "Enabled (bits: 25).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 26: PCLK PLL Ack LN1.
                if actual_mmio_value[5] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PLL Ack (PLL lock) for lane 1 is "
                                                                    "Not Acknowledged."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PLL Ack (PLL lock) for lane 1 should not be "
                                                                     "Acknowledged. (bits: 26).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 27: PCLK PLL Request LN1.
                if actual_mmio_value[4] == '0':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK PLL Request LN1 for lane 1 is not Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK PLL Request LN1 for lane 1 should not be "
                                                                     "Enabled (bits: 27).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 28: PCLK Refclk Ack LN0.
                if actual_mmio_value[3] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK refclk ack for lane 0 is Acknowledged."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK refclk ack for lane 0 should be "
                                                                     "Acknowledged (bits: 28).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 29: PCLK Refclk Request LN0.
                if actual_mmio_value[2] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK refclk Request for lane 0 is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK refclk Request for lane 0 should be "
                                                                     "Enabled (bits: 29).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 30: PCLK PLL Ack LN0.
                if actual_mmio_value[1] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PLL Ack (PLL lock) for lane 0 is "
                                                                    "Acknowledged."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PLL Ack (PLL lock) for lane 0 should be "
                                                                     "Acknowledged. (bits: 30).",
                                                              act=ofst['Expected Output']))
                    
                # Check bits 31: PCLK PLL Request LN0.
                if actual_mmio_value[0] == '1':
                    logging.info(logger_template_pass.format(res="PASS",
                                                             ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                   ofst["Function Name"]),
                                                             verify="PCLK PLL Request LN1 for lane 0 is Enabled."))
                else:
                    logging.error(logger_template_fail.format(res="FAIL",
                                                              ofst="{} - {}".format(ofst['MMIO Offset'],
                                                                                    ofst["Function Name"]),
                                                              verify="PCLK PLL Request LN1 for lane 0 should be "
                                                                     "Enabled (bits: 31).",
                                                              act=ofst['Expected Output']))

            # Expected value is None
            else:
                logging.error(logger_template_pass.format(res="FAIL", ofst="{}".format(ofst['MMIO Offset']),
                                                          verify="Value not found."))
            logging.info(f'-----{ofst["Function Name"]} Verification completed-----\n\n')


mmio_dump_path = os.path.join(os.path.dirname(__file__), '..', 'Pre_boot', 'mmio_dump.json')
mmio_dump_path = os.path.normpath(mmio_dump_path)

to_verify_actual_and_expected_plane(mmio_dump_path)
