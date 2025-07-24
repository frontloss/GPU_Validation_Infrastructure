########################################################################################################################
# @file         vbt.py
# @brief        Contains VBT related APIs
# @details      vbt module contains the class definition for Vbt class. Vbt class represents a VBT data structure for
#               any given adapter. More on VBT: https://gfxspecs.intel.com/Predator/Home/Index/20118
#
#               To read and parse the VBT for any given adapter, an object of class Vbt can be created by passing
#               adapter index. It will get the current VBT through ValSim and parse all the blocks mentioned in
#               blocks_to_parse list (if available in VBT). For each block a data member will be created, which can be
#               accessed through class object. Blocks are mutable and can be changed using assignment operator. To apply
#               the changes, apply_changes() API needs to be called with the same object. Apart from blocks, several
#               other properties like VBT size, VBT version, adapter index are attached to the object.
#
#               For examples of above APIs see Tests/ULT/vbt_simulation_ult.py
#
#               *** Reading and applying VBT from a file ***
#               VBT data can be read from a file by passing full path of the .bin file to Vbt constructor. After
#               creating the VBT object, apply_changes() API can be called to apply the VBT read from file. Rest of the
#               APIs will work as expected including parsing of all the blocks.
#
#               *** How to add a new block ***
#               Please make sure block bit map structure has been added in vbt_context.py already
#               Step 1: Add block number in blocks_to_parse list in Vbt class
#               Step 2: Add a dummy data member with block_<block_id> in Vbt __init__ method
#               Done!
#
# @author       Rohit Kumar, Sri Sumanth Geesala
########################################################################################################################

import array
import ctypes
import logging
import math
import os
import struct

from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.test_env import state_machine_manager
from Libs.Core.vbt import vbt_context

MAX_LFP_PORTS = 2


##
# @brief        VBT blocks_to_parse Array Initialisation
class Vbt(object):
    blocks_to_parse = [1, 2, 9, 12, 27, 40, 42, 43, 44, 46, 52, 56, 57, 58]

    ##
    # @brief        Constructor
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    file_path - full path to VBT file
    def __init__(self, gfx_index='gfx_0', file_path=None):
        # Validate arguments
        if gfx_index is None or not isinstance(gfx_index, str) or not gfx_index.lower().startswith('gfx_'):
            gdhm.report_bug(
                "[VbtLib] Invalid arguments: gfx_index= {0}".format(gfx_index),
                gdhm.ProblemClassification.OTHER,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            raise Exception("Invalid arguments: gfx_index= {0}".format(gfx_index))

        if file_path is not None and (
                not isinstance(file_path, str) or not os.path.exists(file_path) or not file_path.endswith('.bin')):
            gdhm.report_bug(
                "[VbtLib] Invalid arguments: file_path= {0}".format(file_path),
                gdhm.ProblemClassification.OTHER,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            raise Exception("Invalid arguments: file_path= {0}".format(file_path))

        gfx_index = gfx_index.lower()
        self._vbt_data = []
        self.size = None  # Size of the VBT
        self.version = None  # VBT version
        self.gfx_index = gfx_index  # Adapter index
        self.vbt_header = vbt_context.VbtHeader()
        self.bdb_header = vbt_context.BdbHeader()
        self.gfx_val_sim = gfxvalsim.GfxValSim()

        # Define all the blocks to be parsed
        self.block_1 = None
        self.block_2 = None
        self.block_9 = None
        self.block_12 = None
        self.block_27 = None
        self.block_40 = None
        self.block_42 = None
        self.block_43 = None
        self.block_44 = None
        self.block_46 = None
        self.block_52 = None
        self.block_56 = None
        self.block_57 = None
        self.block_58 = None

        # Read from registry or given file
        self.reload(gfx_index, file_path)

    ############################
    # Internal Helper Functions
    ############################

    ##
    # @brief        Helper API to get block instance from vbt_context based on block id and vbt version
    # @param[in]    block_id - VBT Block Number
    # @return       block - block instance from vbt_context
    def __get_block_instance(self, block_id):
        # Validate arguments
        if not isinstance(block_id, int):
            logging.warning("Invalid arguments: block_id= {0}".format(block_id))
            return None

        # All block structures in vbt_context.py follow below naming convention
        # Block[block_id]Vbt[vbt_version]
        block_str = 'Block{0}Vbt'.format(block_id)

        # Get all the structures from vbt_context starting with given block_id
        # for block_id 2, block_instances can be [Block2Vbt203, Block2Vbt212, ...]
        block_instances = [_ for _ in dir(vbt_context) if (block_str in _ and 'Fields' not in _)]

        # If there is no structure found with given block_id, return None
        if len(block_instances) == 0:
            logging.debug("VBT Block {0} definition not found".format(block_id))
            return None

        # If a structure is present with current VBT version, directly create an object and return
        # for block_id 2 and VBT version 224, if Block2Vbt224 is there in vbt_context.py, return it
        if block_str + str(self.version) in block_instances:
            return eval('vbt_context.{0}()'.format(block_str + str(self.version)))

        # If structure with current VBT version is not present, search for latest structure with VBT version < current
        # for block_id 2, if structures present in vbt_context are [Block2Vbt203, Block2Vbt216, Block2Vbt224]
        # Block2Vbt203 will be selected for VBT version 203-215
        # Block2Vbt216 will be selected for VBT version 216-223
        # Block2Vbt224 will be selected for VBT version 224+
        block = None
        active_vbt_version = 0
        for block_vbt_version in block_instances:
            vbt_version = int(block_vbt_version.split('Vbt')[1])
            if active_vbt_version < vbt_version < self.version:
                block = eval('vbt_context.{0}()'.format(block_vbt_version))
                active_vbt_version = vbt_version
        return block

    ##
    # @brief        Helper API to parse VBT blocks
    # @return       None
    def __parse_blocks(self):
        # Get header bytes
        block_size = ctypes.sizeof(vbt_context.VbtHeaderFields)
        for index in range(block_size):
            self.vbt_header.byte_data[index] = self._vbt_data[index]

        block_size = ctypes.sizeof(vbt_context.BdbHeaderFields)
        for index in range(block_size):
            self.bdb_header.byte_data[index] = self._vbt_data[int(self.vbt_header.BiosDataOffset) + index]

        # Set VBT version
        self.version = self.bdb_header.Version
        assert self.version > 0, "Invalid VBT version"

        start_index = self.vbt_header.BiosDataOffset + self.bdb_header.HeaderSize

        # Evaluate block size and iterate through vbt data to extract block bytes
        while len(self._vbt_data) > (start_index + 2):
            # First byte will represent block id for each block
            block_id = self._vbt_data[start_index:(start_index + 1)]
            start_index += 1

            # Next two bytes will have block size
            block_size = (self._vbt_data[start_index: (start_index + 2)])
            start_index += 2

            # un-marshal the block id and block size from byte array
            block_id = struct.unpack('<B', block_id)[0]
            block_size = struct.unpack('<H', block_size)[0]

            # Compute block end offset using block size and start offset
            end_index = start_index + block_size

            # Extract block blob from VBT blob along with BlockId (1byte) + BlockSize(2bytes)
            block_data = self._vbt_data[(start_index - 3): end_index]

            if block_size > vbt_context.BLOCK_SIZE_MAX or block_size + 3 != len(block_data):
                logging.debug(f"Skipping Block_{block_id} parse. size_from_vbt:{block_size + 3},"
                              f" allocated:{len(block_data)} BLOCK_SIZE_MAX:{vbt_context.BLOCK_SIZE_MAX}.")
                continue

            if block_id in self.blocks_to_parse:
                block = self.__get_block_instance(block_id)
                if block is not None:
                    for index in range(block_size + 3):
                        block.byte_data[index] = block_data[index]
                    setattr(self, 'block_{0}'.format(block_id), block)

            # End index of the previous block is the starting index of the next block
            start_index = end_index

    ##
    # @brief        Helper API to set any VBT block
    # @param[in]    block_number - VBT Block Number
    # @return       status - True if operation is successful, False otherwise
    def __set_block(self, block_number):
        ##
        # Validate arguments
        if not isinstance(block_number, int) or block_number <= 0 or block_number not in self.blocks_to_parse:
            logging.warning("\tInvalid arguments: block_number= {0}".format(block_number))
            return False

        # Make sure targeted block was parsed properly.
        if eval(f'self.block_{block_number}') is None:
            return False

        start_index = self.vbt_header.BiosDataOffset + self.bdb_header.HeaderSize

        # Evaluate block size and iterate through VBT_Blob to extract block blob
        # Extracted block blob will added to blocks list
        while len(self._vbt_data) > (start_index + 2):
            block_id = self._vbt_data[start_index:(start_index + 1)]
            start_index += 1

            block_size = (self._vbt_data[start_index: (start_index + 2)])
            start_index += 2

            # un-marshal the block id and block size from byte array
            block_id = struct.unpack('<B', block_id)[0]
            block_size = struct.unpack('<H', block_size)[0]

            # Compute block end offset using block size and start offset
            end_index = start_index + block_size

            if block_id == block_number:
                byte_index = 0
                for index in range((start_index - 3), end_index):
                    self._vbt_data[index] = eval('self.block_{0}.byte_data[{1}]'.format(block_id, byte_index))
                    byte_index += 1
                return True

            # End index of the previous block is the starting index of the next block
            start_index = end_index
        return False

    ############################
    # Exposed APIs
    ############################

    ##
    # @brief        Exposed API to apply the updated VBT
    # @details      A driver restart is required after this API. User is responsible for driver restart call.
    # @return       status - True if operation is successful, False otherwise
    def apply_changes(self):
        for block_id in self.blocks_to_parse:
            if self.__set_block(block_id) is False:
                logging.debug("Failed to update VBT block {0}".format(block_id))

        # Recalculate and update VBT checksum, since we modified VBT data
        sum_vbt_data = 0
        for index in range(len(self._vbt_data)):
            if index != vbt_context.VBT_CHECKSUM_OFFSET:  # byte 26 is VBT checksum. Shouldn't add this to sum.
                sum_vbt_data += self._vbt_data[index]
        new_checksum = (int(math.ceil(sum_vbt_data / 256.0)) * 256) - sum_vbt_data
        self._vbt_data[vbt_context.VBT_CHECKSUM_OFFSET] = new_checksum

        state_machine_manager.StateMachine().update_vbt_state_change(self.gfx_index, True)
        # Write VBT
        return self.gfx_val_sim._configure_vbt(self.gfx_index, self._vbt_data, len(self._vbt_data))

    ##
    # @brief        Exposed API to reload the VBT
    # @details      To re-read the current VBT through ValSim. This call is equivalent to creating a new class object.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    file_path - full path to VBT file
    # @return       None
    def reload(self, gfx_index='gfx_0', file_path=None):
        if file_path is not None:
            with open(file_path, "rb") as f:
                self._vbt_data = f.read()
            self._vbt_data = array.array('B', self._vbt_data)
            if len(self._vbt_data) == 0:
                gdhm.report_bug(
                    "[VbtLib] Failed to read VBT from file {0}".format(file_path),
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                raise Exception("Failed to read VBT from file {0}".format(file_path))
            self.size = len(self._vbt_data)
        else:
            self._vbt_data = self.gfx_val_sim._get_default_vbt(gfx_index)
            if self._vbt_data is None:
                logging.error("Failed to read default VBT")
                return None
            self._vbt_data = array.array('B', self._vbt_data)
            self.size = len(self._vbt_data)

        self.__parse_blocks()
        state_machine_manager.StateMachine().update_vbt_state_change(self.gfx_index, True)

    ##
    # @brief        Exposed API to reset the VBT
    # @details      To revert the current VBT to actual platform VBT. A driver restart is required after this API.
    #               User is responsible for driver restart.
    # @return       None
    def reset(self):
        self.gfx_val_sim._reset_vbt(self.gfx_index)
        state_machine_manager.StateMachine().update_vbt_state_change(self.gfx_index, True)

    ##
    # @brief        Exposed API to dump the VBT in a file
    # @param[in]    file_path - Absolute path to the output bin file
    # @return       status - True if operation is successful, False otherwise
    def _dump(self, file_path):
        # Validate arguments
        if not isinstance(file_path, str):
            logging.warning("Invalid arguments: file_path= {0}".format(file_path))
            return False
        if self._vbt_data is None or len(self._vbt_data) == 0:
            logging.error("VBT data is Empty or None")
            return False

        s = struct.pack('B' * len(self._vbt_data), *self._vbt_data)
        with open(file_path, 'wb') as f:
            f.write(s)

        return True

    ##
    # @brief        Exposed API to get supported ports by VBT
    # @details      Note: Do not use this method within tests or feature modules.
    # @return       enabled_ports -  dictionary of connector port and port type
    #               Example: {'DP_A': 'EMBEDDED', 'DP_B': 'NATIVE', 'HDMI_C': 'NATIVE'}
    def _get_supported_ports(self):
        enabled_ports = {}
        if self.block_2 is None:
            return enabled_ports
        for display_device in self.block_2.DisplayDeviceDataStructureEntry:
            if display_device.DeviceHandle <= 0 or display_device.DeviceClass == 0:
                continue

            # Below is special case and only valid until SKL. To be removed when we move to GLK/CNL
            # Hack due to how GOP team maintained VBT :(
            device_class = vbt_context.DeviceClass()
            device_class.value = display_device.DeviceClass
            if self.block_12.LvdsActiveConfiguration == 0 and device_class.InternalConnection:
                continue

            port_name = vbt_context.DVO_PORT_NAMES.get(display_device.DVOPort, None)
            if display_device.TypeC:
                if display_device.Tbt:
                    port_type = "TC_TBT"
                else:
                    port_type = "TC"
            elif display_device.Tbt:
                port_type = "TBT"
            else:
                port_type = "NATIVE"

            enabled_ports[port_name] = port_type
            if display_device.DeviceClass == vbt_context.DEVICE_CLASS['PLUS']:
                hdmi_port = "HDMI_{0}".format(port_name[-1:])
                enabled_ports[hdmi_port] = "PLUS"
                enabled_ports[port_name] = "PLUS"

            if display_device.DeviceClass == vbt_context.DEVICE_CLASS['LFP_DP']:
                enabled_ports[port_name] = "EMBEDDED"

            if display_device.DeviceClass == vbt_context.DEVICE_CLASS['LFP_MIPI']:
                enabled_ports[port_name] = "EMBEDDED"

        return enabled_ports

    ##
    # @brief        gets the panel index for the requested port in VBT.
    # @details      VBT supports multiple panels data; so need to find index for current port.
    # @param[in]    port - connector port
    # @return       index - VBT Panel Index
    def get_panel_index_for_port(self, port):
        if port in ['MIPI_A', 'MIPI_C', 'EDP_A', 'EDP_B']:
            # WA: To be fixed as part of VSDI-22181
            port = port[1:] if port in ['EDP_A', 'EDP_B'] else port
            return self.get_lfp_panel_type(port)
        else:
            vbt_efp_port_number = vbt_context.DVO_PORT_MAPPING[port]
            hdmi_efp_port_number = vbt_efp_port_number

            if port.startswith("HDMI"):
                # For DP PLUS connections, port name starts with HDMI but the physical port will be DP.
                # Convert the HDMI port name to DP equivalent and get the DVO port mapping
                temp_port = "DP_" + port[-1]
                hdmi_efp_port_number = vbt_context.DVO_PORT_MAPPING[temp_port]

            for index in range(10):
                stblock2_dvo_port = self.block_2.DisplayDeviceDataStructureEntry[index].DVOPort
                stblock2_device_class = self.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass
                if stblock2_dvo_port in [vbt_efp_port_number, hdmi_efp_port_number] and stblock2_device_class != 0:
                    return index
            return -1

    ##
    # @brief        Helper function to get LFP panel type
    # @param[in]    port - connector port name
    # @return       panel_index - panel index of given port
    def get_lfp_panel_type(self, port: str) -> int:
        logging.info(f"--------- Step: Get LFP Panel Type for port_name {port} ---------")
        panel_index = None
        for index in range(MAX_LFP_PORTS):
            port_name = vbt_context.DVO_PORT_NAMES[self.block_2.DisplayDeviceDataStructureEntry[index].DVOPort]
            if port_name == port:
                panel_index = self.block_40.PanelType if index == 0 else self.block_40.PanelType2
                break
        logging.info(f"\tReturning panel_index for LFP port {port} - {panel_index}")
        return panel_index
