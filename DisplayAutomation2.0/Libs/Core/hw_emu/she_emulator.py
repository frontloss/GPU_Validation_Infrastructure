###############################################################################################
# @file         she_emulator.py
# @brief        Port and featuers about SHE Emulator
# @author       Sharath M, Sri Sumanth Geesala
################################################################################################

import os
import time
import math
import logging
from enum import Enum
from typing import NamedTuple, Optional
from xml.etree import ElementTree
from Libs import env_settings
from Libs.Core import reboot_helper
from Libs.Core.test_env import test_context
from Libs.Core.cmd_parser import display_key_pattern
from Libs.Core.core_base import singleton
from Libs.Core.hw_emu import serial_interface
from Libs.Core.hw_emu.emulator_helper import TiledPanelInfo, HubDisplayInfo
from Libs.Core.logger import gdhm

EMULATOR_PORT_NUM_OPCODES = 7
SHE_CONFIG_XML_FILE = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'SheConnectionConfigs.xml')
PARADE_FILE_PATH = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST\\SHE_Parade_Chip_DPCD_Address_Map.txt')

# Ignore these offsets while writing DPCD
IGNORE_DPCD_OFFSET = ['0x100', '0x101', '0x120', '0x160', '0x202', '0x203', '0x204', '0x205',
                      '0x206', '0x207', '0x208', '0x209', '0x20A', '0x20B', '0x20C', '0x20D',
                      '0x20E', '0x20F', '0x280']

# Clear these offsets before writing any new DPCD
CLEAR_DPCD_DICT = {
    '0x0': '16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
    '0x60': '16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
    '0x90': '1 0',
    '0x120': '1 0',
    '0x160': '1 0',
    '0x200': '1 0',
    '0x280': '1 0',
    '0x2200': '16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'}


##
# @brief        Enums for Ports of Emulator device
class EmulatorPortType(Enum):
    IO_PORT1 = 0
    IO_PORT2 = 1
    IO_PORT3 = 2
    IO_PORT4 = 3
    IO_PORT5 = 4
    IO_PORT6 = 5
    IO_PORT7 = 6
    IO_PORT8 = 7
    IO_PORT9 = 8
    IO_PORT10 = 9
    IO_PORT11 = 10
    IO_PORT12 = 11
    EMULATOR_PORT1 = 12
    EMULATOR_PORT2 = 13
    EMULATOR_PORT3 = 14
    IO_PORT13 = 15
    IO_PORT14 = 16
    IO_PORT15 = 17
    IO_PORT16 = 18
    IO_PORT17 = 19
    IO_PORT18 = 20
    IO_PORT19 = 21
    IO_PORT20 = 22
    IO_PORT21 = 23
    IO_PORT22 = 24
    IO_PORT23 = 25
    IO_PORT24 = 26
    EMULATOR_PORT4 = 27
    EMULATOR_PORT5 = 28
    EMULATOR_PORT6 = 29

    ##
    # @brief        Helper method to check if enum exists
    # @param[in]    key - enum name
    # @return       bool - True if enum exists, False otherwise
    @classmethod
    def has_enum(cls, key):
        return key in cls._member_names_


##
# Dictionary of Memory addresses in emulator
FirmwareMemoryAddress = {
    'FIRMWARE_STARTSTOP':           ' 01 13 02 01 ',
    'CRC_ENABLE':                   ' 01 08 77 01 ',
    'DONGLE_BIT':                   ' 01 09 05 01 ',
    'EXTD_CAPABILITY_ENABLE':       ' 01 09 253 01 ',
    'EXTD_CAPABILITY':              ' 01 09 254 01 ',
    'DP_DPCD_01':                   ' 01 09 01 01 ',  # Sink Address space for DPCD01
    'DP_DPCD_02':                   ' 01 09 02 01 ',  # Sink Address space for DPCD02
    'DP_DPCD_ADDRESS_PAGE0_0_127':  ' 08 00 ',        # for read
    'DP_DPCD_ADDRESS_PAGE1_0_127':  ' 09 00 ',
    'DP_FAST_CRC_ADDRESS':          ' 09 64 6 ',
    'CHECK_VSC_MISC':               ' 01 08 44 01 ',
    'MASK_BPC_VSC':                 ' 01 08 104 01 ',
    'BPC_VSC_RESULT':               ' 01 08 108 01 ',
    'BPC_MISC_RESULT':              ' 01 08 43 01 ',
    'HDR_STATUS_01':                ' 01 08 102 01 ',
    'HDR_HEADER':                   ' 01 08 103 4 ',
    'HDR_STATUS_02':                ' 01 08 99 01 ',
    'HDR_PACKET':                   ' 01 08 107 15 '
}

##
# Dictionary of emulator commands composed using emulator Firmware memory addresses and values to be written
EmulatorCommands = {
    'STOP_FIRMWARE':                                FirmwareMemoryAddress['FIRMWARE_STARTSTOP'] + "05",
    'START_FIRMWARE':                               FirmwareMemoryAddress['FIRMWARE_STARTSTOP'] + "00",
    'ENABLE_CRC':                                   FirmwareMemoryAddress['CRC_ENABLE'] + "03",
    'WRITE_DONGLE_DISABLE':                         FirmwareMemoryAddress['DONGLE_BIT'] + "00",
    'ENABLE_EXTD_CAPABILITY_FOR_DONGLE_DISABLE':    FirmwareMemoryAddress['EXTD_CAPABILITY_ENABLE'] + "21",
    'EXTD_CAPABILITY_WRITE_DONGLE_DISABLE':         FirmwareMemoryAddress['EXTD_CAPABILITY'] + "00",
    'COLOR_FORMAT_DATA':                            FirmwareMemoryAddress['EXTD_CAPABILITY_ENABLE'] + "76",
    'HDR_WRITE_DATA_01':                            FirmwareMemoryAddress['HDR_STATUS_01'] + "135",
    'HDR_WRITE_DATA_02':                            FirmwareMemoryAddress['HDR_STATUS_02'] + "00"
}

# Dictionary for types of various emulators connected
# (one emulator board will have three emulators with different DP/HDMI combinations possible).
EmulatorDisplayType = {
    0: ["NONE", "NONE", "NONE"],
    1: ["DP", "NONE", "NONE"],
    2: ["DP", "DP", "NONE"],
    3: ["DP", "DP", "DP"],
    4: ["DP", "DP", "HDMI"],
    5: ["DP", "HDMI", "DP"],
    6: ["DP", "HDMI", "HDMI"],
    7: ["HDMI", "HDMI", "HDMI"],
    8: ["HDMI", "HDMI", "DP"],
    9: ["HDMI", "DP", "DP"],
    10: ["HDMI", "DP", "HDMI"],
    11: ["HDMI", "NONE", "NONE"],
    12: ["HDMI", "HDMI", "NONE"],
    13: ["DP", "HDMI", "NONE"],
    14: ["NONE", "NONE", "NONE"]
}

# Dictionary for opcodes for Emulator ports
# Opcodes are in this order: hotplug, hotunplug, EDID_Read, EDID Write, DPCD Write, CRC read, MSA Read
OpcodesForEmulatorPort = {
    EmulatorPortType.IO_PORT1: [1, 2],
    EmulatorPortType.IO_PORT2: [3, 4],
    EmulatorPortType.IO_PORT3: [5, 6],
    EmulatorPortType.IO_PORT4: [7, 8],
    EmulatorPortType.IO_PORT5: [9, 10],
    EmulatorPortType.IO_PORT6: [11, 12],
    EmulatorPortType.IO_PORT7: [13, 14],
    EmulatorPortType.IO_PORT8: [15, 16],
    EmulatorPortType.IO_PORT9: [17, 18],
    EmulatorPortType.IO_PORT10: [19, 20],
    EmulatorPortType.IO_PORT11: [21, 22],
    EmulatorPortType.IO_PORT12: [23, 24],
    # e.g: 33 - hotplug, 34 - hotunplug, 35 - EDID_Read, 36 - EDID Write, 37 - DPCD Write, 38 - CRC read, 39 - MSA Read
    EmulatorPortType.EMULATOR_PORT1: [33, 34, 35, 36, 37, 38, 39],
    EmulatorPortType.EMULATOR_PORT2: [40, 41, 42, 43, 44, 45, 46],
    EmulatorPortType.EMULATOR_PORT3: [47, 48, 49, 50, 51, 52, 53],
    EmulatorPortType.IO_PORT13: [1, 2],
    EmulatorPortType.IO_PORT14: [3, 4],
    EmulatorPortType.IO_PORT15: [5, 6],
    EmulatorPortType.IO_PORT16: [7, 8],
    EmulatorPortType.IO_PORT17: [9, 10],
    EmulatorPortType.IO_PORT18: [11, 12],
    EmulatorPortType.IO_PORT19: [13, 14],
    EmulatorPortType.IO_PORT20: [15, 16],
    EmulatorPortType.IO_PORT21: [17, 18],
    EmulatorPortType.IO_PORT22: [19, 20],
    EmulatorPortType.IO_PORT23: [21, 22],
    EmulatorPortType.IO_PORT24: [23, 24],
    EmulatorPortType.EMULATOR_PORT4: [33, 34, 35, 36, 37, 38, 39],
    EmulatorPortType.EMULATOR_PORT5: [40, 41, 42, 43, 44, 45, 46],
    EmulatorPortType.EMULATOR_PORT6: [47, 48, 49, 50, 51, 52, 53]
}


##
# @brief        DP Link rates enum
class DpLinkRate(Enum):
    RBR = " 06 "
    HBR = " 0A "
    HBR2 = " 14 "
    HBR3 = " 1E "


##
# @brief        DP Lane Count enum
class DpLaneCount(Enum):
    Lane_1 = " E1 "
    Lane_2 = " E2 "
    Lane_4 = " E4 "


##
# @brief        MSA Parameters
class MSAParameters(NamedTuple):
    X_value: int
    Y_value: int
    refresh_rate: float
    BPC: int
    link_rate: float
    lane_count: int


##
# @brief        Color Format enum
class ColorFormat(Enum):
    RGB = 0
    YUV422 = 1
    YUV444 = 2
    YUV420 = 3


##
# @brief        SHE UTILITY Class
@singleton
class SheUtility:

    ##
    # @brief        SHE Utility constructor.
    def __init__(self):
        self.device_connection_status = False
        self.com_ports = []
        self.connected_device_type = []
        # display_to_emulator_port_map dict will have key= display_port and value= list of emulator_ports.
        # e.g: 'DP_D': [EmulatorPortType.EMULATOR_PORT1]
        self.display_to_emulator_port_map = {}
        self.last_edid_loaded = {}
        self.last_dpcd_loaded = {}

    ##
    # @brief    As per the current setup, get display port to emulator port mappings connected.
    # @return   display_to_emulator_port_mapping - returns a Dictionary of connector port type and emulator port list
    def __get_display_to_emulator_port_mapping(self):
        display_to_emulator_port_mapping = {}
        she_config = env_settings.get('SIMULATION', 'she_config')
        if she_config is not None:
            if not os.path.exists(SHE_CONFIG_XML_FILE):
                logging.error(f'No xml file present at location {SHE_CONFIG_XML_FILE}')
                return

            xml_root = ElementTree.parse(SHE_CONFIG_XML_FILE).getroot()
            for config in xml_root.findall('SheConfig'):
                if config.get('ConfigName') == she_config:
                    for connection in config.findall('Connection'):
                        display_port = connection.get('DisplayPort')
                        emulator_ports = connection.get('EmulatorPort')
                        emulator_ports = [port.strip() for port in emulator_ports.split(',')]

                        # check for display_port and emulator_ports read from xml are valid or not
                        emulator_ports_valid = all([EmulatorPortType.has_enum(port) for port in emulator_ports])
                        if display_key_pattern.match(display_port) and emulator_ports_valid:
                            emulator_ports = ['EmulatorPortType.' + port for port in emulator_ports]
                            emulator_ports = [eval(port) for port in emulator_ports]
                            display_to_emulator_port_mapping[display_port] = emulator_ports
                        else:
                            logging.error(f'Invalid display_port ({display_port}) or  emulator_ports '
                                          f'({emulator_ports}) given in xml')
                    break
            else:
                logging.error(f'{she_config} not found in {SHE_CONFIG_XML_FILE}')
        else:
            logging.error('she_config key not found in env_settings (config.ini)')

        logging.info(f'display_to_emulator_port_map= {display_to_emulator_port_mapping}')
        return display_to_emulator_port_mapping

    ##
    # @brief        Initialize the Emulator by getting Serial Port and Device Port connections.
    # @return       device_connection_status - True if initialization is successful, False otherwise
    def initialize(self):

        self.device_connection_status, self.com_ports, hw_ids = \
            serial_interface.get_connected_com_ports_and_hw_ids()
        if not self.device_connection_status:
            logging.error('None of the serial ports are connected')
            return self.device_connection_status
        self.display_to_emulator_port_map = self.__get_display_to_emulator_port_mapping()

        for hw_id in hw_ids:
            # for SHE 1.0, hw_ids will be 'SHE_CONNECTED'
            if hw_id == 'SHE_CONNECTED':
                config_number = 0  # SHE 1.0 supports only I/O ports, not emulator ports. So config number is 0.
                emulator_ports = EmulatorDisplayType[config_number]
                self.connected_device_type.extend(emulator_ports)
            # for SHE 2.0, hw_ids will be like 'SHE2_0_x'
            elif 'SHE2_0_' in hw_id:
                config_number = int(hw_id.replace('SHE2_0_', ''))
                emulator_ports = EmulatorDisplayType[config_number]
                self.connected_device_type.extend(emulator_ports)

        self.device_connection_status = self.__emulator_initialization(self.com_ports, self.connected_device_type)

        # Unplug all emulator ports to cleanup any leftover plugged ports from last test run.
        # Skip this if test did reboot, since we have to retain the plugged ports in this case.
        if not reboot_helper.is_reboot_scenario():
            for index in range(3 * len(self.com_ports)):
                emulator_port = eval('EmulatorPortType.EMULATOR_PORT' + str(index + 1))
                if self.__hot_plug_unplug(emulator_port, False, 0):
                    logging.debug(f'Successfully cleared HPD on {emulator_port}')
                else:
                    logging.error(f'Failed to clear HPD on {emulator_port}')

        return self.device_connection_status

    ##
    # @brief        helper function do the initialization sequence type of emulators connected.
    # @param[in]    comports - list of comports connected
    # @param[in]    emulator_port_types - list of emulator port types like DP, HDMI, NO Emulator
    # @return       bool - True if initialization successful for all emulators passed, False otherwise
    def __emulator_initialization(self, comports, emulator_port_types):
        if not emulator_port_types:
            return False

        for index in range(0, len(emulator_port_types)):
            emulator_port = eval('EmulatorPortType.EMULATOR_PORT' + str(index + 1))
            if emulator_port_types[index] == "DP":
                if index / 3 < 1:
                    comport = comports[0]  # Emulator board 0 connected on comport 0
                else:
                    comport = comports[1]  # Emulator board 1 connected on comport 1

                if not self.__initialize_dp_emulator(comport, emulator_port):
                    return False

        return True

    ##
    # @brief        helper function do the initialization sequence DP emulator.
    # @param[in]    comport - connected comport name
    # @param[in]    emulator_port - EmulatorPortType enum
    # @return       status - True if initialization sequence successful, False otherwise
    def __initialize_dp_emulator(self, comport, emulator_port):
        status = True

        if not comport or not emulator_port:
            logging.error('Comport or emulator_port passed are None')
            return False

        port_opcode = OpcodesForEmulatorPort[emulator_port][4]

        # Command to Stop Firmware
        data = str(port_opcode) + EmulatorCommands['STOP_FIRMWARE']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending STOP_FIRMWARE command ({data}), on port {comport} and '
                          f'{emulator_port.name}')
            return status

        # Command to enable CRC
        data = str(port_opcode) + EmulatorCommands['ENABLE_CRC']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending ENABLE_CRC command ({data}), on port {comport} and '
                          f'{emulator_port.name}')
            return status

        # Command to Write Dongle disable bit
        data = str(port_opcode) + EmulatorCommands['WRITE_DONGLE_DISABLE']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending WRITE_DONGLE_DISABLE command ({data}), on port {comport} and '
                          f'{emulator_port.name}')
            return status

        # Command to enable Extended Capability field to Write Dongle disable bit
        data = str(port_opcode) + EmulatorCommands['ENABLE_EXTD_CAPABILITY_FOR_DONGLE_DISABLE']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending ENABLE_EXTD_CAPABILITY_FOR_DONGLE_DISABLE command ({data}), on port '
                          f'{comport} and {emulator_port.name}')
            return status

        # Command to  Extended Capability field Write Dongle disable bit
        data = str(port_opcode) + EmulatorCommands['EXTD_CAPABILITY_WRITE_DONGLE_DISABLE']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending EXTD_CAPABILITY_WRITE_DONGLE_DISABLE command ({data}), on port '
                          f'{comport} and {emulator_port.name}')
            return status

        # Command to Start Firmware
        data = str(port_opcode) + EmulatorCommands['START_FIRMWARE']
        status = status and serial_interface.serial_port_write(comport, data)
        time.sleep(2)
        if not status:
            logging.error(f'Failed when sending START_FIRMWARE command ({data}), on port {comport} and '
                          f'{emulator_port.name}')
            return status

        # Give 2 sec delay after all the initialization
        time.sleep(2)

        return status

    ##
    # @brief        helper function to get the details of a particular emulator_port.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @return       com_port, emulator_display_type - comport name and the emulator display type
    def __get_com_port_and_emulator_display_type(self, emulator_port):

        com_port = None
        emulator_display_type = "NONE"

        if not self.com_ports:
            return None
        if not self.connected_device_type:
            return None

        if len(self.com_ports) == 1:
            com_port = self.com_ports[0]
            if emulator_port == EmulatorPortType.EMULATOR_PORT1:
                emulator_display_type = self.connected_device_type[0]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT2:
                emulator_display_type = self.connected_device_type[1]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT3:
                emulator_display_type = self.connected_device_type[2]

        elif len(self.com_ports) == 2:
            if EmulatorPortType.IO_PORT1.value <= emulator_port.value < EmulatorPortType.EMULATOR_PORT3.value:
                com_port = self.com_ports[0]
            elif EmulatorPortType.IO_PORT13.value <= emulator_port.value < EmulatorPortType.EMULATOR_PORT6.value:
                com_port = self.com_ports[1]

            if emulator_port == EmulatorPortType.EMULATOR_PORT1:
                emulator_display_type = self.connected_device_type[0]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT2:
                emulator_display_type = self.connected_device_type[1]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT3:
                emulator_display_type = self.connected_device_type[2]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT4:
                emulator_display_type = self.connected_device_type[3]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT5:
                emulator_display_type = self.connected_device_type[4]
            elif emulator_port == EmulatorPortType.EMULATOR_PORT6:
                emulator_display_type = self.connected_device_type[5]

        return com_port, emulator_display_type

    ##
    # @brief        Plug  and unplug the display with specified delay for next operation.
    # @param[in]    emulator_port - EmulatorPortType enum for connected display
    # @param[in]    plugState - True for plug request, False for unplug request
    # @param[in]    delay - delay in ms
    # @return       bool - True if plug or unplug successful (only guarantees serial write command happened properly),
    #                   False otherwise
    def __hot_plug_unplug(self, emulator_port, plug_state, delay):
        status = False
        comport, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)
        logging.debug(f'For emulator_port {emulator_port}: comport = {comport}, '
                      f'emulator_display_type = {emulator_display_type}')

        if comport is None:
            logging.error("Device is not Initialized Properly")
            return status

        opcodes = OpcodesForEmulatorPort[emulator_port]
        if plug_state is True:
            opcode = opcodes[0]
        else:
            opcode = opcodes[1]

        data = str(opcode) + ' ' + str(delay)
        logging.debug(f'Data being sent for serial write = {data}')
        status = serial_interface.serial_port_write(comport, data)

        # wait for 5 sec so that emulator hardware actually brings up/down display.
        # We cannot do other operations like MSA read before this is ready.
        if status is True:
            time.sleep(5)

        return status

    ##
    # @brief        clear sink related dpcd before writing any new dpcd.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @param[in]    com_port - Serial Communication Port
    # @param[in]    parade_dict - parade address mapping data dictionary
    # @return       status - True if clear dpcd is successful, False otherwise
    @staticmethod
    def __clear_dpcd(emulator_port: EmulatorPortType, com_port: str, parade_dict: dict) -> bool:
        status = False

        # opcode for dpcd_write
        dpcd_write_opcode = OpcodesForEmulatorPort[emulator_port][4]

        for hex_address, dataStr in CLEAR_DPCD_DICT.items():
            data_to_port = ""

            if hex_address in parade_dict.keys():
                # Opcode, Length of Parade Address, Parade Address, Length of list of int(byte data) followed by data
                # Ex: 37 1 09 00 16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                data_to_port += str(dpcd_write_opcode) + " " + str(len(parade_dict[hex_address])) + " " + str(
                    parade_dict[hex_address][0]) + " " + dataStr

                status = serial_interface.serial_port_write(com_port, data_to_port)
                if status is False:
                    logging.error("Failed to write clear dpcd on {emulator_port}")
                    return status

                time.sleep(4)

        logging.info(f'Clear DPCD Successful on {emulator_port}')

        return status

    ##
    # @brief        write edid file data to serial port.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @param[in]    edid_path - path of the edid file
    # @return       bool - True if edid write to serial port is successful, False otherwise
    def __write_edid(self, emulator_port: EmulatorPortType, edid_path: str) -> bool:

        # skip edid load onto emulator, if same edid was loaded last time.
        if emulator_port in self.last_edid_loaded.keys() and self.last_edid_loaded[emulator_port] == edid_path:
            logging.debug(f'EDID {os.path.basename(edid_path)} is already loaded on {emulator_port}')
            return True

        status = False
        com_port, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)

        if com_port is None:
            logging.error("Device is not Initialized Properly")
            return False

        # opcode for edid_write
        edid_write_opcode = OpcodesForEmulatorPort[emulator_port][3]

        # valid edid file extension is ".bin" or ".EDID"
        if (not edid_path.endswith(".bin")) and (not edid_path.endswith(".EDID")):
            logging.error(f'Invalid edid file extension! Expected: [".bin", ".EDID"]')
            return False

        block_length = 16
        data_block = ""

        # Read all bytes at once
        try:
            with open(edid_path, "rb") as edid_bin_file:
                edid_data = edid_bin_file.read()
        except OSError as err:
            logging.error(f'Failed to read the EDID file {os.path.basename(edid_path)}: {err}')
            return False

        # length of edid should always be multiple of 128 bytes
        # TODO: remove this condition once it is fixed in hardware: len(edid_data) > 256
        if len(edid_data) % 128 != 0 or len(edid_data) > 256:
            logging.error(f'Invalid EDID File {os.path.basename(edid_path)}! No.of bytes is not a multiple of 128')
            return False

        for byte_index in range(len(edid_data)):
            data_block += str(edid_data[byte_index]) + " "

            if (byte_index + 1) % block_length == 0:
                # Write data of 19 bytes in order: Opcode ,  Length of EDID data block(Number :16), Index of
                # Data block(Number:0-15), 16 bytes of Data block with decimal values
                # Ex: 36 16 9 20 32 21 17 6 35 9 7 7 131 1 0 0 2 58 128
                data_to_port = (str(edid_write_opcode) + " " + str(block_length) + " " + str(math.ceil(
                    byte_index / block_length) - 1) + " " + data_block)

                # Refresh the data block so that it can take next 16 bytes
                data_block = ""

                # send data to serial port
                logging.debug(f'serial data: {data_to_port}')
                status = serial_interface.serial_port_write(com_port, data_to_port)

                if status is False:
                    logging.error(f"Failed to write edid data on {emulator_port}")
                    return status

                time.sleep(4)

        logging.info(f'EDID write successful with {os.path.basename(edid_path)} on {emulator_port}')
        self.last_edid_loaded[emulator_port] = edid_path

        return status

    ##
    # @brief        write dpcd file data to serial port.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @param[in]    dpcd_path - path of the edid file
    # @return       bool - True if dpcd write to serial port is successful, False otherwise
    def __write_dpcd(self, emulator_port: EmulatorPortType, dpcd_path: str) -> bool:

        # skip dpcd load onto emulator, if same dpcd was loaded last time.
        if emulator_port in self.last_dpcd_loaded.keys() and self.last_dpcd_loaded[emulator_port] == dpcd_path:
            logging.debug(f'DPCD {os.path.basename(dpcd_path)} is already loaded on {emulator_port}')
            return True

        data_dict = {}
        parade_dict = {}

        com_port, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)

        if com_port is None:
            logging.error("Device is not Initialized Properly")
            return False

        # opcode for dpcd_write
        dpcd_write_opcode = OpcodesForEmulatorPort[emulator_port][4]

        # Read Parade file at once and Prepare Parade Data Dictionary, sample line -> 0x60 : 09 253 112,09 254
        try:
            with open(PARADE_FILE_PATH, "r") as parade_file:
                for line in parade_file.readlines():
                    if line.startswith(";") is False:
                        line = line.replace("253 ", "")
                        parade_dict[line.split(":")[0].strip()] = line.split(":")[1].strip().split(",")
        except OSError as err:
            logging.error(f'Failed to read Parade file {os.path.basename(PARADE_FILE_PATH)}: {err}')
            return False

        # Read DPCD file at once and Prepare DPCD Data Dictionary
        # sample line -> 0x60: 0x01, 0x21, 0x02, 0x00, 0x2B, 0x00, 0x00, 0x00, 0x00, 0x01.
        try:
            with open(dpcd_path, "r") as dpcd_txt_file:
                for line in dpcd_txt_file.readlines():
                    if line.startswith(";") is False:
                        line = line.replace(".", "")
                        # convert byte data of dpcd byte address to int, and store its string value
                        data_dict[line.split(":")[0]] = [str(int(byte_data.strip(), 16)) for byte_data in
                                                         line.split(":")[1].split(",")]
        except OSError as err:
            logging.error(f'Failed to read DPCD file {os.path.basename(dpcd_path)}: {err}')
            return False

        # stop firmware before writing dpcd to serial port
        stop_fw = str(dpcd_write_opcode) + EmulatorCommands['STOP_FIRMWARE']
        status = serial_interface.serial_port_write(com_port, stop_fw)
        if status is False:
            logging.error(f'Failed to write stop firmware on {emulator_port}')
            return status

        time.sleep(2)

        # clear all sink related dpcd before writing any new dpcd
        status = self.__clear_dpcd(emulator_port, com_port, parade_dict)
        time.sleep(4)
        if status is False:
            logging.error("Failed to clear the DPCD values on {emulator_port}")
            return status

        for hex_address, dataList in data_dict.items():
            data_to_port = ""

            # write to serial port only if given dpcd hex address is found in Parade dictionary key and not
            # found in ignore_dpcd_offset list, else skip
            if hex_address in parade_dict.keys() and hex_address not in IGNORE_DPCD_OFFSET:

                # Opcode, Length of Parade Address, Parade Address, Length of list of int(byte data),
                # List of int(byte data)
                # Ex: 37 1 09 00 16 17 10 132 0 1 0 0 0 0 0 0 0 0 0 0 0
                data_to_port += str(dpcd_write_opcode) + " " + str(len(parade_dict[hex_address])) + " " + str(
                    parade_dict[hex_address][0]) + " " + str(len(dataList)) + " " + " ".join(dataList)

                logging.debug(f'Serial data: {data_to_port}')

                status = serial_interface.serial_port_write(com_port, data_to_port)
                if status is False:
                    logging.error(f'Failed to write dpcd data on {emulator_port}')
                    return status

                time.sleep(4)

        # start firmware after writing dpcd to serial port
        start_fw = str(dpcd_write_opcode) + EmulatorCommands['START_FIRMWARE']
        status = serial_interface.serial_port_write(com_port, start_fw)
        if status is False:
            logging.error(f'Failed to write start firmware on {emulator_port}')
            return status

        time.sleep(2)

        logging.info(f'DPCD  write successful with {os.path.basename(dpcd_path)} on {emulator_port}')
        self.last_dpcd_loaded[emulator_port] = dpcd_path

        return status

    ##
    # @brief        API to issue plug to emulator
    # @param[in]    gfx_adapter_info - Graphics Adapter Index
    # @param[in]    display_port - connector port type
    # @param[in]    edid_path - EDID file path
    # @param[in]    dpcd_path - DPCD file path
    # @param[in]    is_low_power - Pass True if panel to be plugged in Low Power state
    # @param[in]    port_type - The type of connected port
    # @param[in]    sink_index - indicates the index of displays connected on same display_port via hub/dock
    # @return       status - True on Success, False otherwise
    def plug(self, gfx_adapter_info, display_port, edid_path, dpcd_path, is_low_power, port_type, sink_index=0):
        if is_low_power:
            # emulator will issue HPD after 30 sec from receiving command. But call will return immediately.
            delay = 30
        else:
            delay = 0

        emulator_ports = self.display_to_emulator_port_map[display_port]
        if sink_index >= len(emulator_ports):
            logging.error(f'Wrong sink_index sent. index sent= {sink_index} and num_disps on port {display_port}= '
                          f'{len(emulator_ports)}')
            return False
        emulator_port = emulator_ports[sink_index]

        # logic for loading EDID and DPCD onto emulator before issuing plug.
        if "HDMI" not in display_port:
            status = self.__write_dpcd(emulator_port, dpcd_path)
            if status is False:
                logging.error(f'Failed to load DPCD {os.path.basename(dpcd_path)} on {emulator_port}')
                return status

        status = self.__write_edid(emulator_port, edid_path)
        if status is False:
            logging.error(f'Failed to load EDID {os.path.basename(edid_path)} on {emulator_port}')
            return status

        status = self.__hot_plug_unplug(emulator_port, True, delay)

        if status is False:
            logging.error(f'Failed to plug port {display_port} on {gfx_adapter_info.gfxIndex}')
            return False

        logging.info(f'Plug successful on port {display_port} on {gfx_adapter_info.gfxIndex}')

        return status

    ##
    # @brief        Reads MSA timings from emulator and checks for non-zero timings.
    #                   If hotplug is successful and display is up and active, timings values will be non-zero.
    # @param[in]    gfx_adapter_info - Graphics adapter info
    # @param[in]    display_port - connector port type
    # @param[in]    sink_index - indicates the index of displays connected on same display_port via hub/dock
    # @return       bool - True if timings are non-zero, False otherwise
    def is_emulator_timing_non_zero(self, gfx_adapter_info, display_port, sink_index=0):
        if display_port == 'DP_A':
            return True
        emulator_ports = self.display_to_emulator_port_map[display_port]
        if sink_index >= len(emulator_ports):
            logging.error(f'Wrong sink_index sent. index sent= {sink_index} and num_disps on port {display_port}= '
                          f'{len(emulator_ports)}')
            return False
        emulator_port = emulator_ports[sink_index]

        # SHE 1.0 uses IO_PORT to directly control the HPD line of the cable connected between RVP port and panel.
        # So MSA params can't be read in this case.
        if 'IO_PORT' in emulator_port.name:
            return True
        else:
            status, MSA_values = self.read_MSA_parameters_from_emulator(emulator_port)
            if status is True and MSA_values.X_value != 0 and MSA_values.Y_value != 0 and MSA_values.refresh_rate != 0:
                logging.info(f'Display is active on port {display_port} on {gfx_adapter_info.gfxIndex}')
                return True
            else:
                logging.error(f'Display is not active on port {display_port} on {gfx_adapter_info.gfxIndex}')
                return False

    ##
    # @brief        API to issue unplug to emulator
    # @param[in]    gfx_adapter_info - Graphics Adapter Index
    # @param[in]    display_port - connector port type
    # @param[in]    is_low_power - Pass True if panel to be plugged in Low Power state
    # @param[in]    port_type - The type of display port
    # @param[in]    sink_index - indicates the index of displays connected on same display_port via hub/dock
    # @return       bool - True on Success, False otherwise
    def unplug(self, gfx_adapter_info, display_port, is_low_power, port_type, sink_index=0):
        if is_low_power:
            # emulator will issue HPD after 30 sec from receiving command. But call will return immediately.
            delay = 30
        else:
            delay = 0

        emulator_ports = self.display_to_emulator_port_map[display_port]
        if sink_index >= len(emulator_ports):
            logging.error(f'Wrong MST index sent. index sent= {sink_index} and num_disps on port {display_port}= '
                          f'{len(emulator_ports)}')
            return False
        emulator_port = emulator_ports[sink_index]

        if self.__hot_plug_unplug(emulator_port, False, delay):
            logging.info(f'Unplug successful on port {display_port} on {gfx_adapter_info.gfxIndex}')
            return True
        else:
            logging.error(f'Failed to unplug port {display_port} on {gfx_adapter_info.gfxIndex}')
            return False

    ##
    # @brief        Exposed API to plug MST tiled display using emulator.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    port - Port name to which the display has to be plugged.
    # @param[in]    tiled_panel_info - Contains all information about the tiled panel like edid, dpcd
    # @param[in]    delay - Delay after which the plug has to happen.
    # @return       is_success - Returns True if the plugged is display is detected and has valid timing.
    def plug_mst_tiled_display(self, gfx_index: str, port: str, tiled_panel_info: TiledPanelInfo,
                               delay: int = 0) -> bool:
        is_low_power_plug = False if delay == 0 else True
        m_emulator_port, s_emulator_port = self.display_to_emulator_port_map[port]

        # TODO: need to add logic for loading EDID and DPCD onto emulator before issuing plug.
        logging.info(f"Plugging MST Master Tiled on port={port} emu_port={m_emulator_port} on {gfx_index}")
        is_success = self.__hot_plug_unplug(m_emulator_port, True, delay)

        # Adding additional delay as MST hub is present in between the System and the Emulator which causes delay in
        # detection sometimes. Sleep is not required when plug in low power state as plug happens in low power mode.
        if is_low_power_plug is False:
            time.sleep(5)

        logging.info(f"MST Master Tiled plug status={is_success}")

        if is_success is True and tiled_panel_info.slave_tiled_edid_path is not None:
            logging.info(f"Plugging MST Slave Tiled on port={port} emu_port={s_emulator_port} on {gfx_index}")
            is_success = self.__hot_plug_unplug(s_emulator_port, True, delay)

            # Adding additional delay as MST hub is present in between the System and the Emulator which causes delay in
            # detection sometimes. Sleep is not required when plug in low power state as plug happens in low power mode.
            if is_low_power_plug is False:
                time.sleep(5)

            # Check if plugged display has valid timing data
            logging.info(f"MST Slave Tiled plug status={is_success}")

        return is_success

    ##
    # @brief        Exposed API to plug SST tiled display using emulator.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    m_port - Port name to which the master port of the tiled display has to be plugged
    # @param[in]    s_port - Port name to which the slave port of the tiled display has to be plugged
    # @param[in]    tiled_panel_info - Contains all information about the tiled panel like edid, dpcd
    # @param[in]    delay - Delay after which the plug has to happen.
    # @return       is_success - Returns True if the plugged is display is detected and has valid timing.
    def plug_sst_tiled_display(self, gfx_index: str, m_port: str, s_port: Optional[str],
                               tiled_panel_info: TiledPanelInfo, delay: int = 0) -> bool:
        m_emulator_port: EmulatorPortType = self.display_to_emulator_port_map[m_port][0]

        # TODO: need to add logic for loading EDID and DPCD onto emulator before issuing plug.
        logging.info(f"Plugging SST Master Tiled on port={m_port} emu_port={m_emulator_port} on {gfx_index}")
        is_success = self.__hot_plug_unplug(m_emulator_port, True, delay)
        time.sleep(5)

        # Check if plugged display has valid timing data
        logging.info(f"SST Master Tiled plug status={is_success}")

        if s_port is not None and tiled_panel_info.slave_tiled_edid_path is not None and is_success is True:
            s_emulator_port = self.display_to_emulator_port_map[s_port][0]

            logging.info(f"Plugging SST Slave Tiled on port={s_port} emu_port={s_emulator_port} on {gfx_index}")
            is_success = self.__hot_plug_unplug(s_emulator_port, True, delay)
            time.sleep(5)

            logging.info("Skipping MSA timing check as display might not goto tiled mode after plugging slave port")

        return is_success

    ##
    # @brief        Exposed API to plug display to the TBT hub
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    port - The Port address in String form.
    # @param[in]    hub_display_info - Contains all information about the display to be plugged to the TBT hub
    #                   like edid, dpcd, port type and also the index of the hub port.
    # @param[in]    delay - Delay after which the un-plug has to happen.
    # @return       is_success - Returns True if the plugged is display is detected and has valid timing.
    def plug_display_to_tbt_hub(self, gfx_index: str, port: str, hub_display_info: HubDisplayInfo,
                                delay: int = 0) -> bool:
        emulator_port_tuple = self.display_to_emulator_port_map[port]
        emulator_port = emulator_port_tuple[hub_display_info.port_index]
        logging.info(f"Hot Plug Issued to Port={port} Emu Port={emulator_port} Gfx Index={gfx_index}")

        is_success = self.__hot_plug_unplug(emulator_port, True, delay)
        time.sleep(10)

        logging.debug("Function plug_display_to_tbt_hub status: {}".format(is_success))
        return is_success

    ##
    # @brief        Exposed API to unplug MST tiled display from the emulator.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    port - Port name from which the display has to be unplugged
    # @param[in]    delay - Delay after which the plug has to happen
    # @return       is_success - Returns True if the display is unplugged successfully, False otherwise
    def unplug_mst_tiled_display(self, gfx_index: str, port: str, delay: int = 0) -> bool:
        is_low_power_plug = False if delay == 0 else True
        m_emulator_port, s_emulator_port = self.display_to_emulator_port_map[port]

        logging.info(f"Unplugging MST Slave Tiled on port={port} emu_port={s_emulator_port} on {gfx_index}")
        s_port_status = self.__hot_plug_unplug(s_emulator_port, False, delay)

        # Adding additional delay as MST hub is present in between the System and the Emulator which causes delay in
        # detection sometimes. Sleep is not required when unplugging in low power state as unplug happens in low power
        # mode.
        if is_low_power_plug is False:
            time.sleep(5)
        logging.info(f"MST Slave Tiled unplug status={s_port_status}")

        logging.info(f"Unplugging MST Master Tiled on port={port} emu_port={m_emulator_port} on {gfx_index}")
        m_port_status = self.__hot_plug_unplug(m_emulator_port, False, delay)

        # Adding additional delay as MST hub is present in between the System and the Emulator which causes delay in
        # detection sometimes.Sleep is not required when unplugging in low power state as unplug happens in low power
        # mode.
        if is_low_power_plug is False:
            time.sleep(5)
        logging.info(f"MST Master Tiled unplug status={m_port_status}")

        is_success = m_port_status and s_port_status

        logging.debug(f"Function unplug_mst_tiled_display status: {is_success}")
        return is_success

    ##
    # @brief        Exposed API to unplug MST tiled display from the emulator.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    m_port - Port name to which the master port of the tiled display is connected.
    # @param[in]    s_port - Port name to which the slave port of the tiled display is connected.
    # @param[in]    delay - Delay after which the un-plug has to happen
    # @return       is_success - Returns True if the display is unplugged successfully, False otherwise
    def unplug_sst_tiled_display(self, gfx_index: str, m_port: Optional[str], s_port: Optional[str] = None,
                                 delay: int = 0) -> bool:
        m_port_status = s_port_status = True

        if m_port is not None:
            m_emulator_port: EmulatorPortType = self.display_to_emulator_port_map[m_port][0]
            logging.info(f"Unplugging SST Master Tiled on port={m_port} emu_port={m_emulator_port} on {gfx_index}")
            m_port_status = self.__hot_plug_unplug(m_emulator_port, False, delay)
            logging.info(f"SST Master Tiled unplug status={m_port_status}")

        if s_port is not None:
            s_emulator_port: EmulatorPortType = self.display_to_emulator_port_map[s_port][0]
            logging.info("Unplugging SST Slave Tiled on port={s_port} emu_port={m_emulator_port} on {gfx_index}")

            s_port_status = self.__hot_plug_unplug(s_emulator_port, False, delay)
            logging.info(f"SST Master Tiled unplug status={s_port_status}")

        is_success = m_port_status and s_port_status

        logging.debug(f"Function unplug_sst_tiled_display status: {is_success}")
        return is_success

    ##
    # @brief        Exposed API to un-plug display from the TBT hub connected in emulator
    # @param[in]    gfx_index - Graphics adapter index
    # @param [in]   port - String info of the Port Address
    # @param[in]    hub_display_info - Contains index of the TBT hub port to which un-plug has to be issued.
    #                   This index maps to the corresponding emulator port.
    # @param[in]    delay - Delay after which the un-plug has to happen.
    # @return       is_success - Returns True if the display is unplugged successfully
    def unplug_display_to_tbt_hub(self, gfx_index: str, port: str, hub_display_info: HubDisplayInfo, delay: int = 0):
        emulator_port_tuple = self.display_to_emulator_port_map[port]
        emulator_port = emulator_port_tuple[hub_display_info.port_index]
        logging.info(f"Hot Un-plug Issued to Port={port} Emu Port={emulator_port} Gfx Index={gfx_index}")

        is_success = self.__hot_plug_unplug(emulator_port, False, delay)
        time.sleep(10)

        logging.debug("Function unplug_display_to_tbt_hub status: {}".format(is_success))
        return is_success

    ##
    # @brief        Read MSA Parameters of display.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @return       (status, MSA_values) - (True if Serial port operation is successful False otherwise, MSA Parameters)
    def read_MSA_parameters_from_emulator(self, emulator_port):
        status = False
        MSA_values = MSAParameters(0, 0, 0.0, 0, 0.0, 0)

        comport, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)

        if comport is None or emulator_display_type is None:
            logging.error("Device is not Initialized Properly")
            return status, MSA_values

        if emulator_display_type != "DP":
            logging.error(f"Reading MSA Values is not supported for {emulator_port.name}")
            return status, MSA_values

        opcodes = OpcodesForEmulatorPort[emulator_port]
        if len(opcodes) == 7:
            opcode = opcodes[6]
        else:
            logging.error(f'Reading MSA Values is not supported for {emulator_port.name}')
            return status, MSA_values

        write_data = str(opcode) + FirmwareMemoryAddress['DP_DPCD_ADDRESS_PAGE0_0_127']
        status, read_data = serial_interface.serial_port_read(comport, write_data)

        if not status or read_data is None:
            logging.error('Serial read of DP_DPCD_ADDRESS_PAGE0_0_127 failed.')
            return False, MSA_values
        if len(read_data) < 114:
            logging.error(f'Serial read of DP_DPCD_ADDRESS_PAGE0_0_127 unsuccessful. Num of bytes read ='
                          f' {len(read_data)}')
            return False, MSA_values

        x_value_hex = read_data[64] + read_data[65] + read_data[62] + read_data[63]  # address 32, 31
        y_value_hex = read_data[76] + read_data[77] + read_data[74] + read_data[75]  # address 38,37

        x_value = int(x_value_hex, 16)
        y_value = int(y_value_hex, 16)

        # address 53, 52, 51. Combine NVID
        MVID_hex = read_data[106] + read_data[107] + read_data[104] + read_data[105] + read_data[102] + read_data[103]
        # address 56, 55, 54
        NVID_hex = read_data[112] + read_data[113] + read_data[110] + read_data[111] + read_data[108] + read_data[109]
        MVID = int(MVID_hex, 16)
        NVID = int(NVID_hex, 16)

        Htotal_hex = read_data[56] + read_data[57] + read_data[54] + read_data[55]  # address 28, 27
        Vtotal_hex = read_data[68] + read_data[69] + read_data[66] + read_data[67]  # address 34, 33
        Htotal = int(Htotal_hex, 16)
        Vtotal = int(Vtotal_hex, 16)

        # read link rate and lane count from emulator
        write_data = str(opcode) + FirmwareMemoryAddress['DP_DPCD_ADDRESS_PAGE1_0_127']
        status, read_data = serial_interface.serial_port_read(comport, write_data)
        if not status or read_data is None:
            logging.error(f'Serial read of DP_DPCD_ADDRESS_PAGE1_0_127 failed.')
            return False, MSA_values
        if len(read_data) < 68:
            logging.error(f'Serial read of DP_DPCD_ADDRESS_PAGE1_0_127 unsuccessful. Num of bytes read ='
                          f' {len(read_data)}')
            return False, MSA_values

        link_rate_dpcd_value_hex = read_data[64] + read_data[65]
        lane_count_dpcd_value_hex = read_data[67]

        link_rate_dpcd_value_dec = int(link_rate_dpcd_value_hex, 16)
        lane_count_dpcd_value_dec = int(lane_count_dpcd_value_hex, 16)

        link_rate_Ghz = 0.27 * link_rate_dpcd_value_dec
        link_rate_Ghz = int(link_rate_Ghz * 100) / 100.0
        link_rate_Hz = link_rate_Ghz * (10 ** 9)

        if link_rate_Ghz != 1.62 and link_rate_Ghz != 2.7 and link_rate_Ghz != 5.4 and link_rate_Ghz != 8.1:
            logging.error(f"Invalid Link Rate: {link_rate_Ghz}")
            return False, MSA_values

        if MVID == 0 or NVID == 0 or link_rate_Hz == 0 or Htotal == 0 or Vtotal == 0:
            logging.error(f"One of these parameters are zero, so display on {emulator_port} didn't come active."
                          f" MVID= {MVID}, NVID= {NVID}, link_rate_Hz= {link_rate_Hz}, Htotal = {Htotal}, "
                          f"Vtotal= {Vtotal}")
            return False, MSA_values

        F_stream_clk = ((MVID * 1.0) / NVID) * (link_rate_Hz / 10.0)
        RR_Hz = (F_stream_clk / (Htotal * Vtotal))

        # BPC Read
        BPC_value = 0
        BPC_FROM_VSC = '4'
        BPC_FROM_MISC = '0'
        BPC_VSC_MASK = '7'
        crc_read_opcode = OpcodesForEmulatorPort[emulator_port][5]

        # Write data to check for VSC/MISC
        write_data = str(crc_read_opcode) + FirmwareMemoryAddress['CHECK_VSC_MISC']
        status, read_data = serial_interface.serial_port_read(comport, write_data)

        if not status or read_data is None:
            gdhm.report_bug(
                title="[Interfaces][SHE Emulator] Failed to read BPC data from Emulator: {}".format(emulator_port),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f'BPC Read failed.')
            return False, MSA_values

        # Check if data is coming from VSC Registers
        if read_data[0] == BPC_FROM_VSC:
            # Write data to check if value is 7
            write_data = str(crc_read_opcode) + FirmwareMemoryAddress['MASK_BPC_VSC']
            status, read_data = serial_interface.serial_port_read(comport, write_data)

            if not status or read_data is None:
                gdhm.report_bug(
                    title="[Interfaces][SHE Emulator] Failed to read BPC data from Emulator: {}".format(emulator_port),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f'BPC Read failed.')
                return False, MSA_values

            # Check for vsc_mask registers
            if read_data[1] == BPC_VSC_MASK:
                # Write data to get bpc_result
                write_data = str(crc_read_opcode) + FirmwareMemoryAddress['BPC_VSC_RESULT']
                status, read_data = serial_interface.serial_port_read(comport, write_data)

                if not status or read_data is None:
                    gdhm.report_bug(
                        title="[Interfaces][SHE Emulator] Failed to read BPC data from Emulator: {}".format(
                            emulator_port),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(f'BPC Read failed.')
                    return False, MSA_values

                bpc_result_str = str(read_data[0]) + str(read_data[1])
                # Perform AND Operation with 7 which is sink side formula to get the BPC Value
                bpc_result = int(bpc_result_str, base=16) & 7
                logging.debug("BPC result value in VSC {} ".format(bpc_result))

                if bpc_result == 0:
                    BPC_value = 6
                elif bpc_result == 1:
                    BPC_value = 8
                elif bpc_result == 2:
                    BPC_value = 10
                elif bpc_result == 3:
                    BPC_value = 12
                elif bpc_result == 4:
                    BPC_value = 16

        # Check if data is coming from MISC Registers
        elif read_data[1] == BPC_FROM_MISC:
            # Write data to get bpc_result
            write_data = str(crc_read_opcode) + FirmwareMemoryAddress['BPC_MISC_RESULT']
            status, read_data = serial_interface.serial_port_read(comport, write_data)

            if not status or read_data is None:
                gdhm.report_bug(
                    title="[Interfaces][SHE Emulator] Failed to read BPC data from Emulator: {}".format(emulator_port),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f'BPC Read failed.')
                return False, MSA_values

            bpc_result_str = str(read_data[0]) + str(read_data[1])
            # Perform AND Operation with 224 which is sink side formula to get the BPC Value
            bpc_result = int(bpc_result_str, base=16) & 224
            logging.debug("BPC result value in MISC {} ".format(bpc_result))

            if bpc_result == 0:
                BPC_value = 6
            elif bpc_result == 32:
                BPC_value = 8
            elif bpc_result == 64:
                BPC_value = 10
            elif bpc_result == 96:
                BPC_value = 12
            elif bpc_result == 128:
                BPC_value = 16

        MSA_values = MSAParameters(x_value, y_value, RR_Hz, BPC_value, link_rate_Ghz, lane_count_dpcd_value_dec)
        logging.info(f'Mode on {emulator_port} as per emulator= {MSA_values.X_value} x {MSA_values.Y_value} '
                     f'@{MSA_values.refresh_rate}, BPC_value= {MSA_values.BPC}, '
                     f'link_rate_Ghz= {MSA_values.link_rate}, lane_count= {MSA_values.lane_count}')

        return status, MSA_values

    ##
    # @brief        Read CRC Values of display.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @param[in]    no_of_frames - Number of Frames for which CRC is needed
    # @return       (status, RGB_values) -  (True if Serial port operation is successful False otherwise,
    #               List of CRC values(R G B Values))
    def read_CRC_values_from_emulator(self, emulator_port, no_of_frames):
        status = False
        RGB_values = []
        if no_of_frames <= 0 or no_of_frames > 60:
            no_of_frames = 1

        comport, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)
        if comport is None or emulator_display_type is None:
            logging.error("Device is not Initialized Properly")
            return status, RGB_values
        if emulator_display_type != "DP":
            logging.error("Reading CRC Values is not supported for " + str(emulator_port.name))
            return status, RGB_values

        opcodes_for_disptypes = OpcodesForEmulatorPort[emulator_port]
        if len(opcodes_for_disptypes) == 7:
            opcode = opcodes_for_disptypes[5]
        else:
            logging.error(f'Reading CRC Values is not supported for {emulator_port.name}')
            return status, RGB_values

        write_data = str(opcode) + ' ' + str(no_of_frames) + FirmwareMemoryAddress['DP_FAST_CRC_ADDRESS']
        status, read_data = serial_interface.serial_port_read(comport, write_data)
        if not status or read_data is None:
            logging.error(f'Serial read of DP_FAST_CRC_ADDRESS failed.')
            return False, RGB_values
        if len(read_data) < no_of_frames * 12:
            logging.error(f'Serial read of DP_FAST_CRC_ADDRESS unsuccessful for {no_of_frames} frames. '
                          f'Num of bytes read = {len(read_data)}')
            return False, RGB_values

        offset = 12
        for i in range(0, no_of_frames):
            offset_delta = offset * i
            R_value = read_data[2 + offset_delta] + read_data[3 + offset_delta] + read_data[0 + offset_delta] + \
                      read_data[1 + offset_delta]  # address 65, 64
            G_value = read_data[6 + offset_delta] + read_data[7 + offset_delta] + read_data[4 + offset_delta] + \
                      read_data[5 + offset_delta]  # address 67, 66
            B_value = read_data[10 + offset_delta] + read_data[11 + offset_delta] + read_data[8 + offset_delta] + \
                      read_data[9 + offset_delta]  # address 69, 68
            RGB_values.append([R_value, G_value, B_value])
            logging.debug(f'R_value= {R_value}, G_value= {G_value}, B_value= {B_value}')

        return status, RGB_values

    ##
    # @brief        Get Color Format of display
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @return       status (True/False) and Color Format of the Display (RGB/YUV)
    def get_color_format_from_emulator(self, emulator_port):
        color_format = ""
        dpcd_write_opcode = OpcodesForEmulatorPort[emulator_port][4]
        comport, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)

        # Stop firmware before writing dpcd to serial port
        stop_fw = str(dpcd_write_opcode) + EmulatorCommands['STOP_FIRMWARE']
        status = serial_interface.serial_port_write(comport, stop_fw)
        if status is False:
            logging.error(f'Failed to write stop firmware on {emulator_port}')
            return status, color_format

        time.sleep(2)

        # Write data after stop FW
        write_data = str(dpcd_write_opcode) + EmulatorCommands['COLOR_FORMAT_DATA']
        status = serial_interface.serial_port_write(comport, write_data)

        if status is False:
            logging.error(f'Failed to write Color Format Data on {emulator_port}')
            return status, color_format

        time.sleep(2)

        # Write data to get color format integer
        crc_read_opcode = OpcodesForEmulatorPort[emulator_port][5]
        write_data = str(crc_read_opcode) + FirmwareMemoryAddress['EXTD_CAPABILITY']
        status, read_data = serial_interface.serial_port_read(comport, write_data)

        if not status or read_data is None:
            gdhm.report_bug(
                title="[Interfaces][SHE Emulator] Failed to read Color Format data from Emulator: {}".format(emulator_port),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f'Color Format Read failed.')
            return False, color_format

        logging.debug("Color Format Read data {}".format(read_data))

        color_fmt = str(read_data[1])
        color_format_int = int(color_fmt, base=16)

        logging.debug("Color Fmt {}".format(color_fmt))

        color_format = ColorFormat(color_format_int).name

        # Command to Start Firmware after reading required data
        start_fw = str(dpcd_write_opcode) + EmulatorCommands['START_FIRMWARE']
        status = serial_interface.serial_port_write(comport, start_fw)
        if status is False:
            logging.error(f'Failed to write start firmware on {emulator_port}')
            return status

        time.sleep(2)

        return status, color_format

    ##
    # @brief        Get HDR Status of display.
    # @param[in]    emulator_port - EmulatorPortType enum for connected Display
    # @return       status (True/False) and HDR Status of the Display (True/False)
    def get_hdr_status_from_emulator(self, emulator_port):
        hdr_status = False

        dpcd_write_opcode = OpcodesForEmulatorPort[emulator_port][4]
        comport, emulator_display_type = self.__get_com_port_and_emulator_display_type(emulator_port)

        write_data = str(dpcd_write_opcode) + EmulatorCommands['HDR_WRITE_DATA_01']
        status = serial_interface.serial_port_write(comport, write_data)

        if status is False:
            logging.error(f'Failed to write HDR Data_01 on {emulator_port}')
            return status, hdr_status

        time.sleep(2)

        # Write data to get HDR Header
        crc_read_opcode = OpcodesForEmulatorPort[emulator_port][5]
        write_data = str(crc_read_opcode) + FirmwareMemoryAddress['HDR_HEADER']

        status, read_data = serial_interface.serial_port_read(comport, write_data)

        if not status or read_data is None:
            gdhm.report_bug(
                title="[Interfaces][SHE Emulator] Failed to read HDR data from Emulator: {}".format(emulator_port),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f'HDR Status Read failed.')
            return False, hdr_status

        hdr_header = str(read_data)
        # Sample HDR Header = 00070513 as received from serial port - 8 Characters
        # HDR Header format which needs to be displayed = 00 07 05 13 - 12 Characters
        # So we add spaces between every two characters of 00070513, and then length becomes 12 characters

        # Add Space between every two characters to get the data in correct format
        temp = " ".join(hdr_header[i:i + 2] for i in range(0, len(hdr_header), 2))
        hdr_header = temp[0:11]

        write_data = str(dpcd_write_opcode) + EmulatorCommands['HDR_WRITE_DATA_02']
        status = serial_interface.serial_port_write(comport, write_data)

        if status is False:
            logging.error(f'Failed to write HDR Data_02 on {emulator_port}')
            return status, hdr_status

        time.sleep(2)

        # Write data to get HDR Packet
        write_data = str(crc_read_opcode) + FirmwareMemoryAddress['HDR_PACKET']
        status, read_data = serial_interface.serial_port_read(comport, write_data)

        if not status or read_data is None:
            gdhm.report_bug(
                title="[Interfaces][SHE Emulator] Failed to read HDR data from Emulator: {}".format(emulator_port),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f'HDR Status Read failed.')
            return False, hdr_status

        hdr_packet = str(read_data)
        # Add Space between every two characters to get the data in correct format
        hdr_temp = " ".join(hdr_packet[i:i + 2] for i in range(0, len(hdr_packet), 2))
        hdr_packet = hdr_temp[0:43]

        if not hdr_packet.startswith("00"):
            hdr_status = True

        if hdr_status:
            logging.info("HDR Status: HDR Enabled")
            logging.debug("HDR Header {}".format(hdr_header))
            logging.debug("HDR Packet {}".format(hdr_packet))
        else:
            logging.info("HDR Status: HDR Disabled")

        return status, hdr_status
