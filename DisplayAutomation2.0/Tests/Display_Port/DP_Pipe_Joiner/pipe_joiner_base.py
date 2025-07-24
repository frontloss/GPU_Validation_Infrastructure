#######################################################################################################################
# @file         pipe_joiner_base.py
# @brief        This file contains PipeJoinerFields and PipeJoiner base class which should be inherited by all pipe
#               joiner related tests.
# @details      pipe_joiner_base.py contains PipeJoiner class which implements setup member method to setup the
#               environment required for all the uncompressed PipeJoiner test cases and tearDown member method to reset
#               the environment by unplugging the displays, un-initializing CUI sdk, resetting any registry values etc
#               Also contains some helper methods and variables that are required for the PipeJoiner test cases.
#               PipeJoinerFields class contains the data members that has to verified for uncompressed pipe joiner.
#
# @author       Praburaj Krishnan
#######################################################################################################################

from __future__ import annotations

import logging
import sys
import time
from typing import List, Iterator, Dict, Tuple
from unittest import TestCase

from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayInfo, TARGET_ID, DisplayAndAdapterInfo
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.system_utility import SystemUtility
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumXMLParser

from Tests.Display_Port.DP_MST.dp_mst_parser import DPCommandParser
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

success_log_template = "{} Expected: {} Actual: {}"
error_log_template = "[Driver Issue] - {} [Mismatch] Expected: {} Actual: {}"


##
# @brief        Contains the Pipe Joiner Fields to be Verified for Pipe Joiner to Work.
class PipeJoinerFields:

    ##
    # @brief        Initializes the data members of pipe joiner fields to False by default.
    def __init__(self) -> None:
        self.big_joiner_enable = False
        self.master_big_joiner_enable = False
        self.uncompressed_joiner_master = False
        self.uncompressed_joiner_slave = False

    ##
    # @brief        Compares Two Pipe Joiner Fields and Returns True if All the Fields Matches in Both the Object.
    # @param[in]    other: PipeJoinerFields
    #                   Contains the other PipeJoinerFields(Expected) Which Will be Used For Comparison.
    # @return       is_equal: bool
    #                   Returns True if the expected and actual values are same, False otherwise.
    def __eq__(self, other: PipeJoinerFields) -> bool:
        is_equal = True

        if isinstance(other, PipeJoinerFields) is True:
            zip_iterator = zip(self.__dict__.items(), other.__dict__.items())

            for (a_key, a_value), (e_key, e_value) in zip_iterator:
                if a_value == e_value:
                    logging.info(success_log_template.format(a_key, e_value, a_value))
                else:
                    logging.error(error_log_template.format(a_key, e_value, a_value))
                    is_equal = False

        return is_equal


##
# @brief        Contains All the Helper Functions and Verification Functions Required for PipeJoiner Test Cases.
class PipeJoinerBase(TestCase):
    cmd_dict = {}
    plugged_ports_list = []
    display_port = DisplayPort()
    system_utility = SystemUtility()
    display_config = DisplayConfiguration()
    is_pre_si_environment = False
    mst_port_name_list = []
    external_display_list = []
    test_success_log_template = "Pipe Joiner Verification Successful for {} display"
    test_fail_log_template = "[Driver Issue] - Pipe Joiner Verification failed for {} display"
    mode_enum_parser_dict: Dict[str, ModeEnumXMLParser] = {}
    cmd_line_displays: List[str] = []
    dp_xml_path = "Tests\\Display_Port\\DP_PIPE_JOINER\\dp_uc_pipe_joiner\\"

    ##
    # @brief        This member method is the entry point for any pipe joiner test case. Helps to initialize some of the
    #               parameters required for pipe joiner the test execution and also makes plug call according to the
    #               command line.
    # @return       None
    def setUp(self) -> None:

        cls = PipeJoinerBase

        logging.debug("Entering Setup phase of the test case.")

        try:

            execution_environment = PipeJoinerBase.system_utility.get_execution_environment_type()
            cls.is_pre_si_environment = True if execution_environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"] else False

            custom_tags = ['-PLUG_TOPOLOGIES', '-XML']
            cls.cmd_dict = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + custom_tags)

            cls.cmd_line_displays = cmd_parser.get_sorted_display_list(cls.cmd_dict)
            logging.debug("Displays in the command line: {}".format(cls.cmd_line_displays))

            for port in cls.cmd_line_displays:
                internal_panel_type_list = [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]
                if display_utility.get_vbt_panel_type(port, 'gfx_0') not in internal_panel_type_list:
                    cls.external_display_list.append(port)
            logging.debug("External Display list in the command line: {}".format(cls.external_display_list))

            if cls.cmd_dict['PLUG_TOPOLOGIES'] != 'NONE':
                self._handle_dp_2_0_plug()
            elif cls.cmd_dict['XML'] != 'NONE':
                self._handle_mode_enum_cmd()
            else:
                logging.info("Hot plugging all the displays passed in the command line.")
                cls.plugged_ports_list, enumerated_display_info = display_utility.plug_displays(self, cls.cmd_dict)
                logging.info('Plugged display list: {}'.format(cls.plugged_ports_list))

            common.print_current_topology()

        except Exception as e:
            logging.error('[Test Issue] - Exception occurred in setup. Exception: {}'.format(repr(e)))
            self.tearDown()
            self.fail()

        logging.debug("Exiting Setup phase of the test case.")

    ##
    # @brief        Private method which handles DP2.0 command lines. Creates DP command parser object which helps
    #               to parse the command line and plug the display based on the data obtained from it.
    # @return       None
    def _handle_dp_2_0_plug(self) -> None:
        logging.debug("Handling DP2.0 plug")

        dp_mst_command_parser = DPCommandParser()
        requested_topology_info_dict = dp_mst_command_parser.requested_topology_info_dict
        PipeJoinerBase.mst_port_name_list = dp_mst_command_parser.requested_dp_port_list

        for index, port_name in enumerate(PipeJoinerBase.mst_port_name_list):
            xml_file_name = requested_topology_info_dict[index].path
            topology_type = requested_topology_info_dict[index].display_tech
            logging.debug("XML File Name: {}".format(xml_file_name))
            logging.debug("Topology Type: {}".format(topology_type))
            self._plug_mst_display('gfx_0', port_name, topology_type, xml_file_name, is_low_power=False)

    ##
    # @brief        Private method which handles uncompressed pipe joiner mode enumeration command lines, initializes
    #               the mode enumeration xml parser and plugs the display with the help of the parsed data from the xml.
    # @return       None
    def _handle_mode_enum_cmd(self) -> None:
        xml_file_list: List[str] = PipeJoinerBase.cmd_dict['XML']
        self.assertEqual(len(xml_file_list), len(PipeJoinerBase.cmd_line_displays), "[Test Issue] - Invalid command.")

        internal_panel_type_list = [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]

        for port, xml_file_name in zip(PipeJoinerBase.cmd_line_displays, xml_file_list):
            xml_file_path = PipeJoinerBase.dp_xml_path + xml_file_name.lower()
            xml_parser = ModeEnumXMLParser('gfx_0', port, xml_file_path)
            if display_utility.get_vbt_panel_type(port, 'gfx_0') not in internal_panel_type_list:
                if xml_parser.mst_topology_path is not None:
                    PipeJoinerBase.mst_port_name_list.append(port)
                    display_tech, mst_topology_path = xml_parser.display_tech, xml_parser.mst_topology_path
                    self._plug_mst_display('gfx_0', port, display_tech, mst_topology_path, False)
                else:
                    is_success = display_utility.plug(port=port, edid=xml_parser.edid_file, dpcd=xml_parser.dpcd_file)
                    self.assertTrue(is_success, "Failed to Plug Display at {}".format(port))

            xml_parser.parse_and_construct_mode_tables()
            PipeJoinerBase.mode_enum_parser_dict[port] = xml_parser

    ##
    # @brief        Private method which is used to plug the DP2.0 display.
    # @param[in]    gfx_index: str
    #                    Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Represents the name of the port in which the display has to be plugged. E.g. dp_b, dp_c
    # @param[in]    topology_type: str
    #                   Represents whether its MST/SST
    # @param[in]    xml_file_name: str
    #                   Contains the MST topology information.
    # @param[in]    is_low_power: bool
    #                   True to plug in low power mode, False to plug in normal mode
    # @return       None
    def _plug_mst_display(self, gfx_index: str, port_name: str, topology_type: str, xml_file_name: str,
                          is_low_power: bool) -> None:
        cls = PipeJoinerBase

        is_success = cls.display_port.init_dp(port_name, topology_type)
        self.assertTrue(is_success, "Initializing of {} Failed".format(port_name))
        logging.info("Initializing {} Succeeded".format(port_name))

        is_success = cls.display_port.parse_send_topology(port_name, topology_type, xml_file_name, is_low_power)
        self.assertTrue(is_success, "Failed to parse and send data to simulation driver for {}".format(port_name))
        logging.info("Successfully parsed and send data to simulation driver for {}".format(port_name))

        is_success = cls.display_port.set_hpd(port_name, attach_dettach=True, gfx_index=gfx_index)
        self.assertTrue(is_success, "Set HPD call failed for {}".format(port_name))
        logging.info("Set HPD call succeeded for {}".format(port_name))

        time.sleep(20) if cls.is_pre_si_environment is True else time.sleep(15)

    ##
    # @brief        Verifies If the Registers Related to PipeJoiner are Programmed Correctly based on the Target ID and
    #               Port Name of the DP Display.
    # @param[in]    port_name: str
    #                   Port Name in Which the Pipe Joined Display is Plugged.
    # @return       is_success: bool
    #                   Returns True if the Registers are Programmed Correctly, False Otherwise.
    @classmethod
    def verify_pipe_joined_display(cls, port_name: str) -> bool:
        is_success = True

        display_base = DisplayBase(port_name)
        master_pipe, ddi, transcoder = display_base.GetPipeDDIAttachedToPort(port_name, transcoder_mapping_details=True)
        master_pipe = master_pipe.split('_')[-1].upper()
        transcoder = transcoder.split('_')[-1].upper()
        logging.info(f'Target ID: {display_base.targetId} is connected to Port: {port_name}, Transcoder: {transcoder},'
                     f' Pipe: {master_pipe}')

        # Check Master Pipe Programming.
        actual_pipe_joiner_fields = cls.get_actual_pipe_joiner_fields(master_pipe)
        expected_pipe_joiner_fields = cls.get_expected_pipe_joiner_fields(is_master_pipe=True)

        if actual_pipe_joiner_fields == expected_pipe_joiner_fields:
            logging.info('Actual and Expected Pipe Joiner Fields for Master Pipe: {} are Same'.format(master_pipe))
        else:
            logging.error(f'[Driver Issue] - Actual and Expected Pipe Joiner Fields for Master Pipe: {master_pipe} are '
                          f'Mismatching')
            is_success = False

        # Check Slave Pipe Programming.
        slave_pipe = chr(ord(master_pipe) + 1)
        actual_pipe_joiner_fields = cls.get_actual_pipe_joiner_fields(slave_pipe)
        expected_pipe_joiner_fields = cls.get_expected_pipe_joiner_fields(is_master_pipe=False)

        if actual_pipe_joiner_fields == expected_pipe_joiner_fields:
            logging.info('Actual and Expected Pipe Joiner Fields for Slave Pipe: {} are Same'.format(slave_pipe))
        else:
            logging.error(f'[Driver Issue] - Actual and Expected Pipe Joiner Fields for Slave Pipe: {slave_pipe} are '
                          f'Mismatching')
            is_success = False

        return is_success

    ##
    # @brief        Reads the Register Value Based on the Pipe Information and Creates PipeJoinerField Object and Fills
    #               the Data.
    # @param[in]    pipe: str
    #                   Pipe Name For Which PIPE_DSS_CTL1_REGISTER value has to be Read.
    # @return       actual_pipe_joiner_fields: PipeJoinerFields
    #                   Contains the Driver Programmed Value.
    @classmethod
    def get_actual_pipe_joiner_fields(cls, pipe: str) -> PipeJoinerFields:

        dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + pipe, common.PLATFORM_NAME)
        actual_pipe_joiner_fields = PipeJoinerFields()
        actual_pipe_joiner_fields.big_joiner_enable = bool(dss_ctl1.big_joiner_enable)
        actual_pipe_joiner_fields.master_big_joiner_enable = bool(dss_ctl1.master_big_joiner_enable)
        actual_pipe_joiner_fields.uncompressed_joiner_slave = bool(dss_ctl1.uncompressed_joiner_slave)
        actual_pipe_joiner_fields.uncompressed_joiner_master = bool(dss_ctl1.uncompressed_joiner_master)

        return actual_pipe_joiner_fields

    ##
    # @brief        Creates the Object for PipeJoinerFields and Fills the Value Based on Whether it's a Master Pipe or
    #               Slave Pipe.
    # @param[in]    is_master_pipe: bool
    #                   True if the Expected Pipe Joiner Fields for Master Pipe, False Otherwise.
    # @return       expected_pipe_joiner_fields: PipeJoinerFields
    #                   Contains the Expected PipeJoiner Values.
    @classmethod
    def get_expected_pipe_joiner_fields(cls, is_master_pipe: bool) -> PipeJoinerFields:

        expected_pipe_joiner_fields = PipeJoinerFields()
        expected_pipe_joiner_fields.big_joiner_enable = False
        expected_pipe_joiner_fields.master_big_joiner_enable = False
        expected_pipe_joiner_fields.uncompressed_joiner_master = is_master_pipe
        expected_pipe_joiner_fields.uncompressed_joiner_slave = False if is_master_pipe else True

        return expected_pipe_joiner_fields

    ##
    # @brief        Helper function which gets the display information of all external displays
    # @return       external_display_info_list : Iterator[DisplayInfo]
    #                   Contains display information of all external displays.
    @classmethod
    def get_external_display_info_list(cls) -> Iterator[DisplayInfo]:

        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        assert enumerated_display_info, "Enumerated Display Information is None."

        logging.info('Enumerated Display Information: {}'.format(enumerated_display_info.to_string()))

        try:
            external_display_info_list = [
                display_info
                for display_info in enumerated_display_info.ConnectedDisplays
                if (CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name in cls.external_display_list and
                    display_info.TargetID != 0 and
                    display_info.ConnectorNPortType != enum.VIRTUALDISPLAY and
                    display_utility.get_vbt_panel_type(CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name,
                                                       display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex) not in
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]
                    )
            ]
        except Exception as e:
            logging.error("[Test Issue] - Exception in get_external_display_info_list: {}".format(repr(e)))
            assert False, "[Test Issue] - Failed to Get External Display Info List"

        return external_display_info_list

    ##
    # @brief        Helper function which gets the display and adapter information of all external displays
    # @return       external_display_and_adapter_info_list : List[DisplayAndAdapterInfo]
    #                   Contains display and adapter information of all external displays.
    @classmethod
    def get_external_display_and_adapter_info_list(cls) -> List[DisplayAndAdapterInfo]:
        external_display_info_list: Iterator[DisplayInfo] = cls.get_external_display_info_list()

        external_display_and_adapter_info_list = [
            display_info.DisplayAndAdapterInfo
            for display_info in external_display_info_list
            if CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name in cls.external_display_list
        ]

        return external_display_and_adapter_info_list

    ##
    # @brief       Helper Function to Unplug the All the External Displays That are present in the command line.
    # @return      None
    @classmethod
    def unplug_external_displays(cls) -> None:

        external_display_info_list = cls.get_external_display_info_list()

        logging.info('Unplugging External Displays')

        is_success = True
        for display_info in external_display_info_list:
            gfx_index = display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex
            port = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name

            if port in cls.external_display_list:
                logging.info("Unplugging Display Plugged at {} on {}".format(port, gfx_index))

                if port not in PipeJoinerBase.mst_port_name_list:
                    is_success = display_utility.unplug(gfx_index=gfx_index, port=port) and is_success
                else:
                    is_success = cls.display_port.set_hpd(port, attach_dettach=False) and is_success
                    time.sleep(20) if cls.is_pre_si_environment is True else time.sleep(15)

        assert is_success, "[Test Issue] - Failed to Unplug All External Displays."

        logging.info('Successfully unplugged the Connected External Displays.')


    ##
    # @brief        This method is the exit point for all pipe joiner test cases. This method takes care of unplugging
    #               the displays, resetting any of the registry, un-initialize sdk if any etc. Bring back the
    #               environment before the test has ran.
    # @return       None
    def tearDown(self) -> None:
        cls = PipeJoinerBase

        logging.debug("Entering Teardown phase of the test case.")

        # Unplug Any External Displays If Plugged.
        PipeJoinerBase.unplug_external_displays()

        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.info('Enumerated Display Information: {}'.format(enumerated_display_info.to_string()))

        is_success = cls.display_port.uninitialize_sdk()
        self.assertTrue(is_success, "Failed to un-initialize CUI SDK")
        logging.info("Uninitialized the CUI SDK is Successfully")

        logging.debug("Exiting Teardown phase of the test case.")
