################################################################################################################
# @file         mst_i2c_aux_read_write.py
# @brief        Verify i2c Aux read and write operation on all downstream displays in the topology
# @author       Praveen Bademi
################################################################################################################

import sys
import unittest
import logging
from typing import List

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import display_utility
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import TARGET_ID, DisplayAndAdapterInfo
from Libs.Core import driver_escape
from Tests.Display_Port.DP_MST.display_port_mst_base import config_data_dict, DPCD_IEE_OUI_OFFSET
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief        This class contains several methods that perform i2c aux read/write operation and verifies it
class I2CAuxReadWrite(DisplayPortMSTBase):

    ##
    # @brief        This method verifies i2x aux read and write operation for all the downstream displays in the
    #               topology
    # @return       None
    def test_i2c_aux_read_write(self):
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays is None or enumerated_displays.Count == 0:
            self.fail("Plugged displays are not enumerated")

        logging.info('Enumerated displays: {}'.format(enumerated_displays.to_string()))

        display_adapter_info_list: List[DisplayAndAdapterInfo] = []

        for index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[index]
            if display_utility.get_vbt_panel_type(CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name, 'gfx_0') \
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                display_adapter_info_list.append(display_info.DisplayAndAdapterInfo)

        topology = config_data_dict[self.config].topology
        self.display_config.set_display_configuration_ex(topology, display_adapter_info_list)

        # Test I2C Aux Read for each of the downstream displays.
        self.i2c_aux_read(display_adapter_info_list)

        # Test I2C Aux Write for each of the downstream displays.
        self.i2c_aux_write(display_adapter_info_list)

    ##
    # @brief        This method performs i2x aux read operation for each of the display on each adapter in the given
    #               display adapter info list
    # @param[in]    display_adapter_info_list: List[DisplayAndAdapterInfo]
    #                   Each entry in the list is Object of type DisplayAndAdapterInfo
    # @return       None
    def i2c_aux_read(self, display_adapter_info_list: List[DisplayAndAdapterInfo]):

        expected_data = [0x0, 0x1b, 0xc5]

        for display_and_adapter_info in display_adapter_info_list:
            target_id = TARGET_ID(Value=display_and_adapter_info.TargetID)

            # Sink Index greater than zero indicates that the device is not directly connected to the source.
            if target_id.SinkIndex > 0:
                is_success, read_data = driver_escape.i2c_aux_read(display_and_adapter_info, DPCD_IEE_OUI_OFFSET, 3)
                if is_success is True:
                    self.verify_data_read(expected_data, read_data)
                else:
                    self.fail("I2C Aux Read Failed for display with target id = {}".format(target_id.Value))

    ##
    # @brief        This method performs i2x aux write operation for each of the display on each adapter in the given
    #               display adapter info list
    # @param[in]    display_adapter_info_list: List[DisplayAndAdapterInfo]
    #                   Each entry in the list is Object of type DisplayAndAdapterInfo
    # @return       None
    def i2c_aux_write(self, display_adapter_info_list: List[DisplayAndAdapterInfo]):
        data_to_write = [0x1, 0x1, 0x1]

        for display_and_adapter_info in display_adapter_info_list:
            target_id = TARGET_ID(Value=display_and_adapter_info.TargetID)

            # Sink Index greater than zero indicates that the device is not directly connected to the source.
            if target_id.SinkIndex > 0:
                is_success = driver_escape.i2c_aux_write(display_and_adapter_info, DPCD_IEE_OUI_OFFSET, data_to_write)

                if is_success is True:
                    logging.info("I2C Aux Write Passed for display with target id = {}".format(target_id.Value))

                    is_success, read_data = driver_escape.i2c_aux_read(display_and_adapter_info, DPCD_IEE_OUI_OFFSET, 3)
                    if is_success is True:
                        self.verify_data_read(data_to_write, read_data)
                    else:
                        self.fail("I2C Aux Read Failed for display with target id = {}".format(target_id.Value))

    ##
    # @brief        This method verifies if the data read during i2c_aux_read matches the expected data
    # @param[in]    expected_data: list
    #                   Expected data list
    # @param[in]    read_data: list
    #                   DPCD value list that we got from i2c_aux_read
    # @return       None
    def verify_data_read(self, expected_data, read_data):
        if expected_data == read_data:
            logging.info("PASS - Expected Data = {}, Actual Data = {}".format(expected_data, read_data))
        else:
            self.fail("FAIL - Expected Data = {}, Actual Data = {}".format(expected_data, read_data))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
