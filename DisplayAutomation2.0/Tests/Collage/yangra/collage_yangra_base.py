#######################################################################################################################
# @file         collage_yangra_base.py
# @brief        This file contains CollageYangraBase class which needs to be inherited by all the Collage Yangra tests
# @details      The CollageYangraBase class contains all the common functionalities used across multiple collage test
#               cases. Any Helper methods required for collage should be defined here.
#
# @author       Praburaj Krishnan, Goutham N
#######################################################################################################################

import collections
import json
import logging
import time
from typing import Optional, List, Tuple
from unittest import TestCase

from Libs.Core.system_utility import SystemUtility
from Libs.Core import display_utility, cmd_parser
from Libs.Core import driver_escape
from Libs.Core import enum
from Libs.Core.wrapper.driver_escape_args import CollageTileInfo
from Libs.Core.wrapper.driver_escape_args import CollageTopology, CollageModeArgs, CollageOperation, CollageType
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import TARGET_ID, DisplayConfig, DisplayInfo, DisplayAndAdapterInfo
from Libs.Core.display_power import DisplayPower
from Libs.Core.enum import Enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.sw_sim.dp_mst import DisplayPort

from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.clock import display_clock

from Tests.Collage.yangra.collage_enum_constants import Action, MAX_PIPE_INFO
from Tests.Collage.yangra.collage_xml_parser import CollageParser


##
# @brief        A class which has to be inherited by all the Collage test cases and contains setUp and tearDown methods
#               to set the environment required for the Collage test case and reset the environment after the test case
#               completes respectively.
class CollageYangraBase(TestCase):
    cmd_dict = {}
    plugged_ports_list = []
    display_config = DisplayConfiguration()
    is_pre_si_environment = False
    display_port = DisplayPort()
    displayClock = display_clock.DisplayClock()
    actual_cd_clock = None
    expected_cd_clock = 0

    ##
    # @brief        Makes sures the environment required for the test to run are properly setup.
    # @return       None
    def setUp(self) -> None:
        logging.info('Setting up Collage Yangra base class.')

        try:

            execution_environment = SystemUtility().get_execution_environment_type()
            CollageYangraBase.is_pre_si_environment = True if execution_environment in ["SIMENV_FULSIM",
                                                                                        "SIMENV_PIPE2D"] else False

            self.display_power = DisplayPower()
            self.collage_topology = CollageTopology()
            self.collage_mode_args = CollageModeArgs(CollageOperation.UNKNOWN.value)

            # Parse the xml data to get the display details for plugging.
            r_status, CollageYangraBase.cmd_dict = CollageParser.parse_collage_xml()
            logging.debug('cmd_dict: %s' % json.dumps(CollageYangraBase.cmd_dict))

            if r_status is False:
                self.tearDown()
                self.fail('Failed in setUp->CollageParser.parse_collage_xml()')

        except Exception as e:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Exception occurred in setup. Exception: {}".format(repr(e)),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Exception occurred in setup. Exception: %s' % repr(e))
            self.tearDown()
            self.fail()

    ##
    # @brief        Method which is used to plug the MST display.
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
    def plug_mst_display(self, gfx_index: str, port_name: str, topology_type: str, xml_file_name: str,
                         is_low_power: bool) -> None:
        is_success = CollageYangraBase.display_port.init_dp(port_name, topology_type)
        self.assertTrue(is_success, f"[Test Issue] - Initializing of {port_name} Failed")
        logging.info(f"Initializing {port_name} Succeeded")

        is_success = CollageYangraBase.display_port.parse_send_topology(port_name, topology_type, xml_file_name,
                                                                        is_low_power)
        self.assertTrue(is_success,
                        f"[Test Issue] - Failed to parse and send data to simulation driver for {port_name}")
        logging.info(f"Successfully parsed and send data to simulation driver for {port_name}")

        is_success = CollageYangraBase.display_port.set_hpd(port_name, attach_dettach=True, gfx_index=gfx_index)
        self.assertTrue(is_success, f"[Test Issue] - Set HPD call failed for {port_name}")
        logging.info(f"Set HPD call succeeded for {port_name}")

        # Delay until Display is enumerated on requested port.
        maximum_delay = 120
        polling_counter = 0
        is_display_attached = False
        while polling_counter <= maximum_delay:
            # Retrieving enumerated displays and checking if display is attached on requested port.
            enumerated_displays = CollageYangraBase.display_config.get_enumerated_display_info()
            is_display_attached = display_config.is_display_attached(enumerated_displays, port_name)
            if is_display_attached:
                break
            time.sleep(1)
            polling_counter += 1

        self.assertTrue(is_display_attached,
                        f"[Driver Issue] - Timeout reached! Display is not enumerated on port {port_name}")

    ##
    # @brief        Method which handles MST command lines. Retrieves port, gfx_index, xml_file_name, topology_type
    #               from cmd_dict and plug the MST display based on the data obtained from it
    # @return       None
    def handle_mst_cmd(self) -> None:
        cls = CollageYangraBase
        for key, value in cls.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None and key.startswith('DP_'):
                port_name = value['connector_port']
                gfx_index = value['gfx_index']

                xml_file_name = cls.cmd_dict[port_name]["xml_file"]
                logging.info(f"XML File Name: {xml_file_name}")

                topology_type = cls.cmd_dict[port_name]["topology_type"]
                logging.info(f"Topology Type: {topology_type}")

                cls.plug_mst_display(self, gfx_index, port_name, topology_type, xml_file_name, is_low_power=False)
                cls.plugged_ports_list.append(port_name)

    ##
    # @brief        Hot Swap display handles HOT_PLUG and UNPLUG of the display based on the action type. Function fails
    #               when plug or unplug of the display fails or when an invalid value is passed to the argument action.
    # @param[in]    action: Action
    #                   Controls the flow of the function i.e. plug the display or unplug the display.
    # @param[in]    port: Optional[str]
    #                   Port name on which the displays to be plugged. E.g. 'DP_B', 'HDMI_B', 'DP_C'
    # @param[in]    is_low_power: Optional[bool]
    #                   Boolean variable informs whether to plug in low power state or in normal mode.
    # @return       None
    def hot_swap_display(self, action: Action, port: Optional[str] = None,
                         is_low_power: Optional[bool] = False) -> None:

        logging.info('Hot plug or unplug the display based on the action. Action: %s' % action.name)

        r_status = False
        cls = CollageYangraBase
        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.debug('Enumerated display list before HotSwap: %s' % enumerated_display_info.to_string())

        # Hotplug all displays passed in the command line.
        if action is Action.HOT_PLUG_ALL:
            logging.info("Hot plugging all the displays passed in the command line.")

            # MST Case.
            if "MST" in cls.cmd_dict['CONFIG_PATH'][0]:
                cls.handle_mst_cmd(self)

            # SST Case.
            else:
                cls.plugged_ports_list, enumerated_display_info = display_utility.plug_displays(self, cls.cmd_dict)
            logging.debug('Plugged display list: %s' % cls.plugged_ports_list)

        # Hotplug display to the specified port by getting port information from cmd_dict.
        elif action is Action.HOT_PLUG and port is not None:
            logging.info("Hot plugging display on port %s: " % port)
            port_properties = cls.cmd_dict[port]
            gfx_index = port_properties['gfx_index']
            if "MST" in cls.cmd_dict['CONFIG_PATH'][0]:
                xml_file_name = port_properties["xml_file"]
                topology_type = port_properties["topology_type"]
                cls.plug_mst_display(gfx_index, port, topology_type, xml_file_name, is_low_power=False)
            else:
                panel_index = port_properties['panel_index']
                connector_port_type = port_properties['connector_port_type']
                r_status = display_utility.plug(port, is_low_power=is_low_power, port_type=connector_port_type,
                                                panelindex=panel_index, gfx_index=gfx_index)
                self.assertEquals(r_status, True, "Failed to plug display at port : %s" % port)

            cls.plugged_ports_list.append(port)

        # Do a unplug on all previously plugged ports if action is UNPLUG_ALL
        elif action is Action.UNPLUG_ALL:
            logging.info("Unplugging all the displays based on plugged port list: %s " % cls.plugged_ports_list)
            for plugged_port in cls.plugged_ports_list:
                if "MST" in cls.cmd_dict['CONFIG_PATH'][0]:
                    r_status = cls.display_port.set_hpd(plugged_port, attach_dettach=False)
                else:
                    r_status = display_utility.unplug(plugged_port)
                self.assertTrue(r_status, f"[Test Issue] - Failed to unplug display at port : {plugged_port}")

            cls.plugged_ports_list = []

        # Do a unplug on specified port if port_type is not None.
        elif action is Action.UNPLUG and port is not None:
            logging.info("Unplugging the display at port %s " % port)
            port_properties = cls.cmd_dict[port]
            gfx_index = port_properties['gfx_index']

            if "MST" in cls.cmd_dict['CONFIG_PATH'][0]:
                r_status = cls.display_port.set_hpd(port, attach_dettach=False)
            else:
                r_status = display_utility.unplug(port, is_low_power=is_low_power, gfx_index=gfx_index)

            self.assertEquals(r_status, True, "[Test Issue] - Failed to unplug display at port : %s" % port)
            cls.plugged_ports_list.remove(port)

        # Log if it's an invalid Action.
        else:

            self.assertEquals(r_status, True, "Invalid parameter for hot swap display...Exiting...")

        # Log enumerated display info after hotplug/unplug
        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.info('Enumerated display list after HotSwap: %s' % enumerated_display_info.to_string())

    ##
    # @brief        Helps to invoke other function related to collage like setting collage topology data, checking if
    #               collage is possible with the collage topology, if collage applied successfully after enabling it.
    #               Function fails if any of the above function returns False.
    # @param[in]    collage_type : CollageType
    #                   Contains the type of collage to be applied. [HORIZONTAL or VERTICAL]
    # @param[in]    display_info_list : List[DisplayInfo]
    #                   Contains adapter and display information about all the displays that will be part of collage.
    # @return       None
    def set_and_verify_collage_topology(self, collage_type: CollageType, display_info_list: List[DisplayInfo]) -> None:

        logging.info('***** Constructing and Verifying the collage topology *****')
        logging.info('Collage Type: %s' % CollageType(collage_type).name)

        cls = CollageYangraBase
        target_id_list_to_be_in_collage = cls.get_target_id_list(display_info_list)

        logging.info('Setting display config before computing max collage mode to make displays active')
        r_status = cls.set_display_config_and_verify('EXTENDED', target_id_list_to_be_in_collage)
        self.assertEquals(r_status, True, 'Aborting the test as applying the display config failed.')

        gfx_index = display_info_list[0].DisplayAndAdapterInfo.adapterInfo.gfxIndex

        display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
        self.assertTrue(display_info_list, 'DisplayInfo not found.')

        computed_max_collage_mode = cls.compute_max_collage_mode(target_id_list_to_be_in_collage, collage_type)

        # Compute possible optimal CD clock for each display and get maximum among them.
        # Temporarily Disabling PTL CD Clock Verification on Collage
        # for display_info in display_info_list:
        #     # Pixel clock is stored in 3rd index of computed max collage mode.
        #     computed_max_pixel_rate_mhz = computed_max_collage_mode[3] / 1000000
        #     child_display_info = [CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name]
        #     # This variable will be used to compare cd clock value after invoking collage.
        #     computed_expected_cd_clock = CollageYangraBase.displayClock.get_optimal_cd_clock_from_pixelclock(gfx_index, computed_max_pixel_rate_mhz, child_display_info)
        #     # Note that DSC Displays with Slice Count 1, optimal cd clock will be determined with 1ppc method
        #     self.expected_cd_clock = max(computed_expected_cd_clock, self.expected_cd_clock)
        #
        # self.assertIsNotNone(self.expected_cd_clock, "[Test Issue] : Failed to initialize clk object.")
        # logging.info(f"CD Clock before invoking collage: {self.expected_cd_clock}")

        self.set_collage_topology_data(target_id_list_to_be_in_collage, collage_type)

        is_collage_config_possible = self.is_collage_topology_possible(display_info_list)
        self.assertEquals(is_collage_config_possible, True, 'Failure at is_collage_topology_possible...Exiting...')
        # Gdhm bug reporting handled in is_collage_topology_possible

        self.enable_collage_and_verify(display_info_list)

        self.verify_max_collage_mode(computed_max_collage_mode)
        logging.info('Computed max collage mode and Actual collage mode are same.')

        self.verify_displays_in_collage()

        # Temporarily Disabling PTL CD Clock Verification on Collage
        # self.actual_cd_clock = CollageYangraBase.displayClock.get_current_cd_clock(gfx_index)

    ##
    # @brief        Fills collage topology structure based on the enumerated display information and collage type.
    # @param[in]    target_id_list_to_be_in_collage : List[int]
    #                   List of target id's which will be part of collage topology
    # @param[in]    collage_type : CollageType
    #                   Indicates type of the collage to be applied i.e. HORIZONTAL or VERTICAL
    # @note         Failure happens only if no of external displays is less than 2 or xml doesn't contain child display.
    #               To apply collage minimum of 2 external displays are required.
    # @return       None
    def set_collage_topology_data(self, target_id_list_to_be_in_collage: List[int], collage_type: CollageType) -> None:

        collage_tile_info_list = []
        total_no_of_h_tiles = total_no_of_v_tiles = 1
        no_of_target_id = len(target_id_list_to_be_in_collage)
        if no_of_target_id == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Invalid parameter - target_id_list_to_be_in_collage: {}".format(
                    target_id_list_to_be_in_collage),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        self.assertTrue(target_id_list_to_be_in_collage, 'Invalid parameter - target_id_list_to_be_in_collage')

        if collage_type is CollageType.HORIZONTAL:
            total_no_of_h_tiles = no_of_target_id
            total_no_of_v_tiles = 1
        elif collage_type is CollageType.VERTICAL:
            total_no_of_h_tiles = 1
            total_no_of_v_tiles = no_of_target_id
        elif collage_type is CollageType.COLLAGE_2_X_2:
            total_no_of_h_tiles = total_no_of_v_tiles = 2

        i = 0
        for tile_h_location in range(total_no_of_h_tiles):
            for tile_v_location in range(total_no_of_v_tiles):
                target_id = target_id_list_to_be_in_collage[i]
                collage_tile_info = CollageTileInfo(target_id, tile_h_location, tile_v_location)
                collage_tile_info_list.append(collage_tile_info)
                i = i + 1

        self.collage_mode_args.collageTopology = CollageTopology(total_no_of_h_tiles, total_no_of_v_tiles, collage_tile_info_list)
        self.collage_topology = self.collage_mode_args.collageTopology

        logging.info("Collage Topology: %s " % self.collage_topology)

    ##
    # @brief        Checks if collage is possible with the given topology data.
    # @param[in]    display_info_list : List[DisplayInfo]
    #                   Contains adapter and display information about all the displays that will be part of collage.
    # @return       is_collage_config_possible: bool
    #                   Returns True if collage is possible with the given topology on the current platform else False.
    def is_collage_topology_possible(self, display_info_list: List[DisplayInfo]) -> bool:

        display_adapter_info = display_info_list[0].DisplayAndAdapterInfo
        gfx_index = display_adapter_info.adapterInfo.gfxIndex

        logging.info('Checking if collage is possible with the given topology and platform')

        self.collage_mode_args.operation = CollageOperation.VALIDATE_COLLAGE.value
        r_status, self.collage_mode_args = driver_escape.invoke_collage(gfx_index, self.collage_mode_args)

        if r_status is True:
            if self.collage_mode_args.collageSupported is True and self.collage_mode_args.collageConfigPossible is True:
                logging.info('Collage is possible on the platform with the given topology.')
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_collage] Collage is not supported by the platform or is not possible "
                          "with the given topology.",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error('Collage is not supported by the platform or is not possible with the given topology.')
        else:
            logging.error('Escape call Failed - invoke_collage()')
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Escape call - IsCollageConfigurationPossible Failed...",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        return self.collage_mode_args.collageConfigPossible

    ##
    # @brief        Enables collage with the given collage topology by making escape call to driver using collage.dll
    # @param[in]    display_info_list : List[DisplayInfo]
    #                   Contains adapter and display information about all the displays that will be part of collage.
    # @return       None
    def enable_collage_and_verify(self, display_info_list: List[DisplayInfo]) -> None:

        # Check if collage is possible before enabling collage.
        display_adapter_info = display_info_list[0].DisplayAndAdapterInfo
        gfx_index = display_adapter_info.adapterInfo.gfxIndex

        logging.info('Enabling collage with the given collage topology.')

        self.collage_mode_args.operation = CollageOperation.ENABLE_COLLAGE.value

        r_status, self.collage_mode_args = driver_escape.invoke_collage(gfx_index, self.collage_mode_args)

        if r_status is True:
            logging.info("Escape call Passed - invoke_collage(). Enabled Collage successfully.")
        else:
            logging.error('Failure in Escape call - invoke_collage()')
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Failure in Escape call - EnableCollageConfiguration Failed...",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        self.assertEquals(r_status, True, 'Escape call Failed - invoke_collage()')

        # Delay until collage display is enumerated.
        maximum_delay = 120
        polling_counter = 0
        while polling_counter <= maximum_delay:
            time.sleep(1)
            r_status = self.is_collage_display_enumerated(display_info_list[0])
            if r_status:
                break
            polling_counter += 1

        if r_status is False:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Collage display is not enumerated.Exiting..",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertEquals(r_status, True, 'Collage display is not enumerated.Exiting...')

    ##
    # @brief        Matches the computed max collage mode and the actual collage mode.
    # @param[in]    computed_max_collage_mode: Tuple[int, int, int, int]
    #                   Tuple contains max Computed HRes, VRes and RR for the collage display.
    # @return       None
    def verify_max_collage_mode(self, computed_max_collage_mode: Tuple[int, int, int, int]) -> None:
        cls = CollageYangraBase

        collage_display_info_list = cls.get_collage_display_info_list()
        if len(collage_display_info_list) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Display info not found ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found.')

        collage_target_id = collage_display_info_list[0].TargetID

        r_status = cls.set_display_config_and_verify('SINGLE', [collage_target_id])
        self.assertEquals(r_status, True, 'Failure occurred while applying display config in verify_max_collage_mode.')
        # Gdhm bug reporting handled in set_display_config_and_verify

        collage_supported_mode_dict = cls.display_config.get_all_supported_modes([collage_target_id], sorting_flag=True)
        if len(collage_supported_mode_dict) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Failed to get supported mode for collage.",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertTrue(collage_supported_mode_dict, 'Failed to get supported mode for collage.')

        if len(collage_supported_mode_dict[collage_target_id]) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Supported collage mode list is empty",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        self.assertTrue(collage_supported_mode_dict[collage_target_id], 'Supported collage mode list is empty')

        actual_max_collage_mode = collage_supported_mode_dict[collage_target_id][-1]

        logging.info('Actual max collage mode (HRes, VRes, RR): ({}, {}, {})'.format(
            actual_max_collage_mode.HzRes,
            actual_max_collage_mode.VtRes,
            actual_max_collage_mode.refreshRate)
        )
        logging.info('Computed max collage mode (HRes, VRes, RR): ({})'.format(computed_max_collage_mode))

        # Compare Horizontal, Vertical resolution and Refresh rate of computed and actual collage mode.
        r_status = cls.display_config.set_display_mode([actual_max_collage_mode])
        self.assertEquals(r_status, True, 'Failure occurred when setting max mode for collage display')

        r_status = (computed_max_collage_mode[0] == actual_max_collage_mode.HzRes and
                    computed_max_collage_mode[1] == actual_max_collage_mode.VtRes and
                    computed_max_collage_mode[2] == actual_max_collage_mode.refreshRate)

        if r_status is False:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Verify max collage mode failed.Exiting...",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertEquals(r_status, True, 'Verify max collage mode failed.Exiting...')

    ##
    # @brief        Verification mechanism where we match the programmed and actual target id list present in collage
    #               display, to ensure all the displays which are programmed to be present in collage display are
    #               present in child_id list of collage display after enabling collage.
    # @note         Check is collage display is enumerated before invoking the function.
    # @return       None
    def verify_displays_in_collage(self) -> None:
        # Get current collage topology from the driver.
        collage_display_info_list = CollageYangraBase.get_collage_display_info_list()
        if len(collage_display_info_list) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Display info not found ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found.')

        maximum_delay = 120
        polling_counter = 0
        while polling_counter <= maximum_delay:
            # Get Current collage topology and retrieve ChildIds from them
            r_status, collage_mode_args = CollageYangraBase.get_current_collage_configuration(collage_display_info_list)
            collage_topology = collage_mode_args.collageTopology
            child_id_list_in_current_config = CollageYangraBase.get_child_id_of_collage_display(collage_topology)
            # Checking if length of retrieved child_id_list is not equal to 0
            # HSD-18023953818
            if len(child_id_list_in_current_config) != 0 and r_status is True and collage_mode_args is not None:
                break
            time.sleep(1)
            polling_counter += 1
        logging.debug('Child id list in current config: %s' % json.dumps(child_id_list_in_current_config))

        if len(child_id_list_in_current_config) == 0:
            self.fail("[Driver Issue]: Timeout reached! Child IDs for enumerated collage are 0 ")

        # Programed collage topology data from the test to the driver.
        child_id_list_programmed = CollageYangraBase.get_child_id_of_collage_display(self.collage_topology)
        logging.debug('Child id list in programmed topology data: %s' % json.dumps(child_id_list_programmed))

        # Returned collage topology from the driver to the test.
        child_id_list_returned = CollageYangraBase.get_child_id_of_collage_display(self.collage_mode_args.collageTopology)
        logging.debug('Child id list in returned topology data: %s' % json.dumps(child_id_list_returned))

        # Counter counts the value in each list.
        child_id_list_in_current_config = collections.Counter(child_id_list_in_current_config)
        child_id_list_programmed = collections.Counter(child_id_list_programmed)
        child_id_list_returned = collections.Counter(child_id_list_returned)

        # Returns True when programmed child id list (target id list), child id list from the current
        # collage configuration and child id list that is returned after enable collage all matches.
        r_status = (child_id_list_programmed == child_id_list_in_current_config and
                    child_id_list_programmed == child_id_list_returned)

        if r_status is False:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Displays in collage and displays programmed to be in collage "
                      "are different",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        self.assertEquals(r_status, True, 'Displays in collage and displays programmed to be in collage are different')
        logging.info('Displays in collage and displays programmed to be in collage are same')

    ##
    # @brief        Disables the current collage by making escape call to driver.
    # @param[in]    collage_display_info : DisplayInfo
    #                   Contains adapter and display information about collage display.
    # @return       None
    def disable_collage_and_verify(self, collage_display_info: DisplayInfo) -> None:

        collage_adapter_info = collage_display_info.DisplayAndAdapterInfo
        gfx_index = collage_adapter_info.adapterInfo.gfxIndex

        logging.info('Disabling Collage Topology on adapter : {}'.format(collage_adapter_info.adapterInfo.gfxIndex))

        if CollageYangraBase.is_collage_display_enumerated(collage_display_info) is True:
            collage_mode_args = CollageModeArgs(CollageOperation.DISABLE_COLLAGE.value)
            r_status, collage_mode_args = driver_escape.invoke_collage(gfx_index, collage_mode_args)

            if r_status is False:
                gdhm.report_bug(
                    title="[Interfaces][Display_collage] Failed to disable collage configuration",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.assertTrue(r_status, 'Escape call - invoke_collage() failed to disable collage configuration')

            maximum_delay = 120
            polling_counter = 0
            while polling_counter <= maximum_delay:
                time.sleep(1)
                r_status = CollageYangraBase.is_collage_actually_disabled(collage_display_info)
                if r_status is True:
                    break
                polling_counter += 1

            self.assertTrue(r_status, 'Collage is not disabled after disable collage escape call...Exiting...')
            logging.info('Successfully disabled collage configuration...')

        else:
            logging.warning('Collage is not enabled...Skipping collage disable call...')

    ##
    # @brief        Gets the current collage configuration that is enabled.
    # @param[in]    collage_display_info_list : List[DisplayInfo]
    #                   Contains adapter and display information about all the collage displays.
    # @return       (r_status, collage_mode_args) : Tuple[bool, CollageModeArgs]
    #                r_status
    #                   Indicates status of the escape call to the driver.
    #               collage_mode_args
    #                   Contains the all information about the displays participating in collage.
    @classmethod
    def get_current_collage_configuration(cls, collage_display_info_list: List[DisplayInfo]) -> Tuple[
        bool, CollageModeArgs]:
        display_adapter_info = collage_display_info_list[0].DisplayAndAdapterInfo
        gfx_index = display_adapter_info.adapterInfo.gfxIndex
        collage_mode_args = CollageModeArgs(CollageOperation.GET_COLLAGE.value)
        r_status, collage_mode_args = driver_escape.invoke_collage(gfx_index, collage_mode_args)

        if r_status is True:
            logging.info("Collage Mode Arguments: %s" % collage_mode_args)
        else:
            logging.error("Escape call - invoke_collage() failed to get current configuration.")
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Failed to get current collage configuration ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            collage_mode_args = None

        return r_status, collage_mode_args

    ##
    # @brief        Helper function to get the target id list of displays which is to be participated in collage.
    # @param[in]    display_info_list: List[DisplayInfo]
    #                   Contains the display information along with adapter info for the collage displays
    # @return       target_id_list_to_be_in_collage: List[int]
    #                   Returns list of target ids
    @classmethod
    def get_target_id_list(cls, display_info_list: List[DisplayInfo]) -> List[int]:

        target_id_list_to_be_in_collage = [
            display_info.TargetID
            for display_info in display_info_list
        ]

        logging.info("Target id list to be in collage: %s" % json.dumps(target_id_list_to_be_in_collage))

        return target_id_list_to_be_in_collage

    ##
    # @brief        Helper function to get the display information of collage displays.
    # @return       display_info_list: List[DisplayInfo]
    #                   Contains the display information along with adapter info for the collage displays
    @classmethod
    def get_display_info_list_to_be_in_collage(cls) -> List[DisplayInfo]:

        port_list = []
        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.debug('Enumerated display list: %s' % enumerated_display_info.to_string())

        for key, value in cls.cmd_dict.items():
            if (cmd_parser.display_key_pattern.match(key) and value['is_lfp'] is False and
                    value['is_child_display'] is True):
                port_list.append(key)

        display_info_list = [
            display_info for display_info in enumerated_display_info.ConnectedDisplays
            if CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name in port_list
        ]

        if len(display_info_list) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Display info not found ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        return display_info_list

    ##
    # @brief        Finds if any of the external display is plugged by getting external display info list.
    # @return       r_status : bool
    #                   True indicates external displays are plugged to the system.
    #                   False indicates no external display is connected to the system.
    @classmethod
    def is_external_displays_plugged(cls) -> bool:

        external_display_info_list = cls.get_external_display_info_list()

        r_status = False if len(external_display_info_list) == 0 else True

        return r_status

    ##
    # @brief        Gets the child id/target id of displays participating in collage from collage_mode_args.
    #               If collage_mode_args is not passed get the current collage configuration and get child id list.
    # @param[in]    collage_topology : CollageTopology
    #                   Contains collage child info from which collage child target id can be extracted.
    # @return       child_id_list : List[int]
    #                   Contains a list of child id's/ target id's of the displays participating in collage.
    @classmethod
    def get_child_id_of_collage_display(cls, collage_topology: CollageTopology) -> List[int]:

        child_id_list = []
        if collage_topology is not None:
            child_info_list = collage_topology.collageChildInfo
            child_id_list = [child_info.childID for child_info in child_info_list if child_info.childID != 0]
        else:
            logging.warning('Cannot retrieve child ids of collage display from collage topology')

        logging.info("Child id's of collage display: %s" % json.dumps(child_id_list))

        return child_id_list

    ##
    # @brief        Check if collage is enabled if enabled, then disable of collage has some failure even though escape
    #               call to driver succeeded.
    # @param[in]    collage_display_info : DisplayInfo
    #                   Contains the display information along with adapter info for the collage display.
    # @return       r_status : bool
    #                   Returns True if is_collage_enabled() returns False
    @classmethod
    def is_collage_actually_disabled(cls, collage_display_info: DisplayInfo) -> bool:

        r_status = CollageYangraBase.is_collage_display_enumerated(collage_display_info) is False
        if r_status is False:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Collage is not disabled after disable collage escape call",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        return r_status

    ##
    # @brief        Get collage Target id list after enabling collage and checks for the collage specific bit in the
    #               target id. if the bit is set then collage is enabled else collage is not enabled.
    # @param[in]    collage_display_info: DisplayInfo
    #                   Contains the display information along with adapter info for the collage display.
    # @return       r_status : bool
    #                   Returns True if collage bit in TARGET_ID is set, False in all other cases.
    @classmethod
    def is_collage_display_enumerated(cls, collage_display_info: DisplayInfo) -> bool:

        r_status = False
        collage_adapter_info = collage_display_info.DisplayAndAdapterInfo.adapterInfo
        collage_display_info_list = cls.get_collage_display_info_list()

        for display_info in collage_display_info_list:
            display_adapter_info = display_info.DisplayAndAdapterInfo.adapterInfo
            if (
                    (display_adapter_info.gfxIndex == collage_adapter_info.gfxIndex) and
                    (display_adapter_info.vendorID == collage_adapter_info.vendorID) and
                    (display_adapter_info.deviceID == collage_adapter_info.deviceID) and
                    (display_adapter_info.deviceInstanceID == collage_adapter_info.deviceInstanceID)
            ):
                r_status = True
                logging.info('Returning true from is_collage_display_enumerated')
                break

        return r_status

    ##
    # @brief        Helper function which gets the display info of the collage.
    # @return       collage_display_info_list : List[DisplayInfo]
    #                   Contains DisplayInformation of all enumerated collage displays.
    @classmethod
    def get_collage_display_info_list(cls) -> List[DisplayInfo]:

        logging.info('Getting Collage display information.')

        target_id = TARGET_ID()
        collage_target_id_list = []  # type : [int]
        collage_display_info_list = []  # type : [DisplayInfo]

        external_display_info_list = cls.get_external_display_info_list()
        for display_info in external_display_info_list:
            target_id.Value = display_info.TargetID
            if target_id.CollageDisplay:
                collage_display_info_list.append(display_info)
                collage_target_id_list.append(display_info.TargetID)

        logging.info("Enumerated Collage Target id list: %s" % collage_target_id_list)

        return collage_display_info_list

    ##
    # @brief        Helper function which gets the display information of all external displays
    # @return       external_display_info_list : List[DisplayInfo]
    #                   Contains display information of all external displays.
    @classmethod
    def get_external_display_info_list(cls) -> List[DisplayInfo]:

        logging.info('Getting External display information.')

        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.debug('Enumerated display list: %s' % enumerated_display_info.to_string())

        '''
        internal_display_port_list :  [[LFP TargetID, LFP Port Name]]
        Example: [['8388688','DP_A], ['8388677','DP_B']]
        '''

        internal_display_list = cls.display_config.get_internal_display_list(enumerated_display_info)
        logging.debug('Internal display list: %s' % json.dumps(internal_display_list))

        internal_display_port_list = list(display[1] for display in internal_display_list)
        logging.debug('Internal display port list: %s' % json.dumps(internal_display_port_list))

        external_display_info_list = []
        try:
            if enumerated_display_info is not None:
                external_display_info_list = list(filter(lambda display_info:
                                                         display_info.TargetID != 0 and
                                                         CONNECTOR_PORT_TYPE(
                                                             display_info.ConnectorNPortType).name not in
                                                         internal_display_port_list and
                                                         display_info.ConnectorNPortType != enum.VIRTUALDISPLAY,
                                                         enumerated_display_info.ConnectedDisplays))
        except Exception as e:
            gdhm.report_bug(
                title="[Interfaces][Display_collage] Exception in get_external_display_info_list: {}".format(repr(e)),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Exception in get_external_display_info_list: %s " % repr(e))

        return external_display_info_list

    ##
    # @brief        Sets the display config based on the topology and the target id list and verifies the applied
    #               display config.
    # @param[in]    topology: str
    #                   display config like SINGLE/CLONE/EXTENDED
    # @param[in]    target_id_list_to_be_in_collage: List[int]
    #                   Contains target id which will be part of the display config to be applied.
    # @returns      r_status: bool
    #                   Returns True if display configuration is successfully applied.
    @classmethod
    def set_display_config_and_verify(cls, topology: str, target_id_list_to_be_in_collage: List[int]) -> bool:

        r_status = True
        topology = eval('enum.%s' % topology)

        config_to_set = cls.get_display_config_to_set(topology, target_id_list_to_be_in_collage)
        cls.display_config.set_display_configuration(config_to_set)

        # Verify the applied display configuration.
        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        current_config = cls.display_config.get_current_display_configuration()
        logging.info('Current display configuration: %s' % current_config.to_string(enumerated_display_info))

        if current_config.equals(config_to_set):
            logging.info('Set display configuration is successful.')
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Failed to set display configuration with status code:{}".format(
                    config_to_set.status),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Failed to set display configuration with status code: %s' % config_to_set.status)
            r_status = False

        return r_status

    ##
    # @brief        Construct DisplayConfig object using topology and target ids passed.
    # @param[in]    topology: Enum
    # @param[in]    target_id_list: List[int]
    #                   Contains target id which will be part of the display config to be applied.
    # @returns      config_to_set: DisplayConfig
    #                   Returns the constructed display config object.
    @classmethod
    def get_display_config_to_set(cls, topology: Enum, target_id_list: List[int]) -> DisplayConfig:

        display_path = 0
        config_to_set = DisplayConfig()
        config_to_set.topology = topology

        # Construct Display path info on which the config should be applied.
        for target_id in target_id_list:
            display_adapter_info = cls.display_config.get_display_and_adapter_info(target_id)
            config_to_set.displayPathInfo[display_path].targetId = target_id
            config_to_set.displayPathInfo[display_path].displayAndAdapterInfo = display_adapter_info
            display_path += 1

        config_to_set.numberOfDisplays = display_path
        enumerated_display_info = cls.display_config.get_enumerated_display_info()
        logging.info('Trying to set display config as: %s' % config_to_set.to_string(enumerated_display_info))

        return config_to_set

    ##
    # @brief        Gets all the valid target id combination for the specified topology.
    # @param[in]    topology: str
    #                   display config like SINGLE/CLONE/EXTENDED
    # @param[in]    no_of_pipe_occupied_by_collage: Optional[int]
    #                   This is used when collage display is present. Since collage display uses multiple pipes, to know
    #                   the number of pipes used by collage this variable used based on which invalid config will be
    #                   filtered.
    # @return       valid_config_list: List[List[int]]
    #                   Contains all valid target id list for a given topology
    @classmethod
    def get_possible_Configurations(cls, topology: str, no_of_pipe_occupied_by_collage: Optional[int] = 1) -> List[
        List[int]]:

        valid_config_list = []
        topology = 'enum.' + topology

        max_pipe_count = cls.get_max_pipe_supported()
        max_possible_length = max_pipe_count - no_of_pipe_occupied_by_collage + 1
        enumerated_display_info = cls.display_config.get_enumerated_display_info()

        if enumerated_display_info is not None:

            # Get all target id that are enumerated except virtual display if any.
            target_id_list = [
                display_info.TargetID for display_info in enumerated_display_info.ConnectedDisplays
                if display_info.TargetID != 0 and display_info.ConnectorNPortType != enum.VIRTUALDISPLAY
            ]

            # Get all possible combination using the target id list.
            target_id_combination_list = display_utility.get_possible_configs(target_id_list, True)
            logging.debug("Target id combination list: %s" % target_id_combination_list)

            '''
            Filter out the target_id_list for the respective topology. This might contain some invalid target id
            permutation as the no of displays enumerated might be more than the max pipe.
            '''
            target_id_combination_list = target_id_combination_list[topology]
            logging.debug("Target id combination list for topology [%s] : %s" % (topology, target_id_combination_list))

            # Filter the invalid permutation list based on the max pipe count
            for target_id_list in target_id_combination_list:
                if len(target_id_list) <= max_possible_length:
                    valid_config_list.append(target_id_list)

        logging.info("Valid configuration list for config [%s]: %s" % (topology, valid_config_list))

        return valid_config_list

    ##
    # @brief        Get the max supported pipe by the platform by using the platform name.
    # @param[in]    gfx_index: Optional[str]
    #                   Indicates the graphics adapter for which max pipe supported has to be returned.
    # @return       max_pipe_count: int
    #                   Returns the max pipe supported by the platform.
    @classmethod
    def get_max_pipe_supported(cls, gfx_index: Optional[str] = 'gfx_0') -> int:

        max_pipe_count = 0
        gfx_adapter_dict = TestContext.get_gfx_adapter_details()
        platform_name = gfx_adapter_dict[gfx_index].get_platform_info().PlatformName.lower()
        for max_pipe, platform_list in MAX_PIPE_INFO.items():
            if platform_name in platform_list:
                max_pipe_count = max_pipe

        logging.info('Max pipe count for platform: %s is %d' % (platform_name, max_pipe_count))

        return max_pipe_count

    ##
    # @brief        get_common_modes_list: Compare mode_list1 and mode_list2,
    #               fetch common mode among them and return the updated list.
    # @param[in]    mode_list1: List[tuple]
    #               It will be of form: [(HzRes, VtRes, refreshRate, BPP, samplingMode, scanlineOrdering, pixelClockHz), (), ()], [(), ()]
    # @param[in]    mode_list2: List[tuple]
    #               It will be of form: [(HzRes, VtRes, refreshRate, BPP, samplingMode, scanlineOrdering, pixelClockHz), (), ()], [(), ()]
    # @return       updated_mode_list: List[tuple]
    @classmethod
    def get_common_modes_list(cls, mode_list1: List[tuple], mode_list2: List[tuple]) -> List[tuple]:
        updated_mode_list = []

        # Fetch common modes between mode_list1 and mode_list2
        # and append it to updated_mode_list.
        for mode1 in mode_list1:
            for mode2 in mode_list2:
                if (mode1[0] == mode2[0] and
                        mode1[1] == mode2[1] and
                        mode1[2] == mode2[2] and
                        mode1[3] == mode2[3] and
                        ((mode1[4].rgb == 1 and mode2[4].rgb == 1) or
                         (mode1[4].yuv420 == 1 and mode2[4].yuv420 == 1) or
                         (mode1[4].yuv444 == 1 and mode2[4].yuv444 == 1)) and
                        mode1[5] == mode2[5]):
                    # Common mode can have different pixel clock, Hence fetch max among them.
                    max_pixel_rate = max(mode1[6], mode2[6])
                    updated_mode_list.append(mode1) if mode1[6] == max_pixel_rate else updated_mode_list.append(mode2)

        return updated_mode_list

    ##
    # @brief        Compute max collage mode based on the max common supported mode by each of the display in the
    #               target id list.
    # @param[in]    target_id_list: List[int]
    #                   Contains the target id list that will be part of collage topology.
    # @param[in]    collage_type: CollageType
    #                   Contains the type of collage to be applied. [HORIZONTAL or VERTICAL]
    # @returns      (HRes, VRes, RR, pixel_clock): Tuple[int, int, int, int]
    #                   Returns the max horizontal, vertical resolution along with refresh rate.
    # @note        Make sure target_id_list passed are active displays, if not supported modes will not be returned.
    @classmethod
    def compute_max_collage_mode(cls, target_id_list: List[int], collage_type: CollageType) -> Tuple[int, int, int, int]:

        supported_mode_dict = cls.display_config.get_all_supported_modes(target_id_list, sorting_flag=True)

        for target_id, supported_mode_list in supported_mode_dict.items():
            logging.debug("List of supported modes for Target id: {}".format(target_id))
            for display_mode in supported_mode_list:
                logging.debug('HRes:{} VRes:{} RR:{} BPP:{}, SamplingMode: {}, ScanlineOrdering: {}, PixelClockHz: {}'.format(
                    display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
                    display_mode.samplingMode, display_mode.scanlineOrdering, display_mode.pixelClock_Hz
                ))

        # Tuple will be of the form [[(HzRes, VtRes, refreshRate, BPP, samplingMode, scanlineOrdering, pixelClockHz)], [()], [()]]
        reference_mode_list = [
            (display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
             display_mode.samplingMode, display_mode.scanlineOrdering, display_mode.pixelClock_Hz)
            for display_mode in list(supported_mode_dict.values())[0]
        ]

        logging.debug('Reference mode list')
        for display_mode in reference_mode_list:
            logging.debug('HRes:{} VRes:{} RR:{} BPP:{}, SamplingMode: {}, ScanlineOrdering: {}, PixelClockHz'.format(
                display_mode[0], display_mode[1], display_mode[2], display_mode[3], display_mode[4], display_mode[5], display_mode[6]
            ))

        '''
        Tuple will be of the form [[(HzRes, VtRes, refreshRate, BPP, samplingMode, scanlineOrdering, pixelClockHz), (), ()], [(), ()]]
        Contains all the supported modes of each display in above form.  
        '''
        all_supported_mode_list = [
            [
                (display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
                 display_mode.samplingMode, display_mode.scanlineOrdering, display_mode.pixelClock_Hz)
                for display_mode in supported_mode_list
            ]
            for supported_mode_list in list(supported_mode_dict.values())[1:]
        ]

        '''
        Reference mode tuple is no updated to hold all common modes of the displays.
        New form of reference mode tuple is [(HzRes, VtRes, refreshRate, BPP, samplingMode, scanlineOrdering, pixelClockHz), (), ()]
        '''
        for custom_display_mode_list in all_supported_mode_list:
            reference_mode_list = cls.get_common_modes_list(reference_mode_list, custom_display_mode_list)

        logging.debug('Reference mode tuple list after intersection: {}'.format(reference_mode_list))

        # Sort the reference mode list to get the max mode.
        # sorting is done based on HzRes,VtRes and refreshRate
        common_supported_mode_list = sorted(reference_mode_list,
                                            key=lambda reference_mode: (
                                                reference_mode[0], reference_mode[1], reference_mode[2]))
        max_common_supported_mode = common_supported_mode_list[-1]


        '''
        computed_max_collage_mode will be of the form (HzRes, VtRes, refreshRate, pixelClockHz)
        HzRes and VtRes are multiplied by no of target id to get the max collage mode.
        '''
        no_of_target_id = len(target_id_list)
        computed_max_collage_mode = (0, 0, 0, 0)
        if collage_type == CollageType.HORIZONTAL:
            computed_max_collage_mode = (no_of_target_id * max_common_supported_mode[0], max_common_supported_mode[1],
                                         max_common_supported_mode[2], max_common_supported_mode[6])
        elif collage_type == CollageType.VERTICAL:
            computed_max_collage_mode = (max_common_supported_mode[0], no_of_target_id * max_common_supported_mode[1],
                                         max_common_supported_mode[2], max_common_supported_mode[6])
        elif collage_type == CollageType.COLLAGE_2_X_2:
            no_of_target_id /= 2
            computed_max_collage_mode = (no_of_target_id * max_common_supported_mode[0],
                                         no_of_target_id * max_common_supported_mode[1],
                                         max_common_supported_mode[2], max_common_supported_mode[6])

        logging.info('Computed max Collage mode: {}'.format(computed_max_collage_mode))

        return computed_max_collage_mode

    ##
    # @brief        Helper functions which get the graphics adapter info from enumerated display information.
    # @return       display_and_adapter_info : DisplayAndAdapterInfo
    #                   Returns the active adapter info from the enumerated display info object.
    def get_active_adapter_info(self) -> DisplayAndAdapterInfo:

        display_and_adapter_info = DisplayAndAdapterInfo()
        enumerated_display_info = self.display_config.get_enumerated_display_info()

        logging.debug('Enumerated display information: {}'.format(enumerated_display_info.to_string()))

        for index in range(enumerated_display_info.count):
            if enumerated_display_info.ConnectedDisplays[index].IsActive is True:
                display_and_adapter_info = enumerated_display_info.ConnectedDisplays[index].DisplayAndAdapterInfo

        if display_and_adapter_info is not None and display_and_adapter_info.adapterInfo is not None:
            logging.info('Graphics adapter info: {}'.format(display_and_adapter_info.adapterInfo.to_string()))
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Failed to get DisplayAdapterInfo from enumerated display",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Failed to get DisplayAdapterInfo from enumerated display')

        return display_and_adapter_info

    ##
    # @brief        Class Method to Get the Possible Collage Types Based on the Number of Displays That will be
    #               Participating in Collage.
    # @param[in]    no_of_displays: int
    #                   No of Displays that Will be Part of Collage Across a Graphics Adapter
    # @return       collage_types: List[CollageType]
    #                   List of Possible Collage Types that is Possible with the Displays.
    @classmethod
    def get_possible_collage_types(cls, no_of_displays: int) -> List[CollageType]:
        collage_types = [CollageType.HORIZONTAL, CollageType.VERTICAL]

        if no_of_displays == 4:
            collage_types.append(CollageType.COLLAGE_2_X_2)

        return collage_types

    ##
    # @brief        Method for VDSC verification before and after invoking collage.
    #               Verifies if is_vdsc_required key is present in cmd_dict if not,
    #               skips vdsc verification then verifies if VDSC is enabled on each display present in collage
    #               and then compares with expected VDSC status. If Current VDSC status (ie. after enabling collage)
    #               and expected VDSC status matches, then returns True, otherwise False.
    # @param[in]    display_info_list: List[DisplayInfo]
    #                   Contains the list of display_info of collage_child_ports.
    # @param[in]    collage_display_info: DisplayInfo
    #                   Contains the collage_display_info.
    # @returns      is_success : bool
    #                   Returns True if Expected VDSC status on each port
    #                   matches with actual VDSC status.
    @classmethod
    def _verify_vdsc(cls, display_info_list: List[DisplayInfo],
                     collage_display_info: Optional[DisplayInfo] = None) -> bool:
        is_success = True
        collage_port = None if collage_display_info is None else CONNECTOR_PORT_TYPE(
            collage_display_info.ConnectorNPortType).name
        for display_info in display_info_list:
            display_adapter_info = display_info.DisplayAndAdapterInfo.adapterInfo
            gfx_index = display_adapter_info.gfxIndex
            child_port = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name

            # if is_vdsc_verfication not present in cmd_dict[port] then skip vdsc verification, otherwise continue
            if 'is_vdsc_required' not in cls.cmd_dict[child_port]:
                logging.info("VDSC verification is not required for given configuration..")
                continue

            logging.info(f"verifying VDSC on port {child_port}")
            expected_vdsc_status = cls.cmd_dict[child_port]['is_vdsc_required']

            if collage_display_info is None:
                # Verifying VDSC before enabling collage.
                is_vdsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, child_port)
            else:
                # Verifying VDSC after enabling collage.
                is_vdsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, collage_port, child_port)

            if is_vdsc_enabled == expected_vdsc_status:
                logging.info(
                    f"{child_port} VDSC Status Expected: {expected_vdsc_status}, Actual: {is_vdsc_enabled}")
            else:
                logging.error(
                    f"[Driver Issue] - {child_port} VDSC Status Expected: {expected_vdsc_status}, "
                    f"Actual:  {is_vdsc_enabled}")
                is_success = False
        return is_success

    ##
    # @brief        Cleanup the plugged displays after disabling collage.
    # @return       None
    def tearDown(self) -> None:

        logging.info('Cleaning up the Collage Yangra base class.')

        # Make sure collage is disabled.
        collage_adapter_info_list = self.get_collage_display_info_list()

        if len(collage_adapter_info_list) > 0:
            self.disable_collage_and_verify(collage_adapter_info_list[0])

        # clean up plugged displays if any
        external_display_info_list = CollageYangraBase.get_external_display_info_list()
        for display_info in external_display_info_list:
            plugged_port = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            self.hot_swap_display(action=Action.UNPLUG, port=plugged_port)
        if "MST" in self.cmd_dict['CONFIG_PATH'][0]:
            CollageYangraBase.display_port.uninitialize_sdk()
