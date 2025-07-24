########################################################################################################################
# @file         display_port_mst_base.py
# @brief        It contains setUp and tearDown methods of unittest framework. In setUp,
#               we parse command_line arguments and then runTest() in the test script gets executed
#               In tearDown, Test clean up will take place.
#
# @author   Praveen Bademi
########################################################################################################################
import ctypes
from ctypes import Array, c_char
import logging
import time
import unittest
from collections import namedtuple
from operator import attrgetter
from typing import List

from Libs.Core import display_utility, display_essential
from Libs.Core import enum
from Libs.Core import system_utility as sys_util
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.display_config.display_config_struct import DisplayConfig, DisplayAndAdapterInfo
from Libs.Core.display_power import DisplayPower
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.registry_access import RegDataType
from Libs.Core.sw_sim.dp_mst import DisplayPort, TOPOLOGY_STATUS_CODE, NODE_RAD_INFO
from Libs.Core.sw_sim.gfxvalsim import GfxValSim
from Libs.Feature.powercons import registry
from Tests.Display_Port.DP_MST.dp_mst_parser import DPCommandParser

DPCD_SINK_CONTROL = 0x600
DPCD_VERSION_OFFSET = 0x0
DPCD_MSTM_CAP_OFFSET = 0x21
DP_HOTPLUG_GOLDEN_VALUE = 0x00000001
DPCD_VERSION_11 = 0x11
DPCD_VERSION_12 = 0x12
DPCD_IEE_OUI_OFFSET = 0x300
MSTM_CTRL = 0x111

# delays are given in Milli Seconds
DELAY_5000_MILLISECONDS = 15000
DELAY_1000_MILLISECONDS = 1000.0
PARTIAL_TOPOLOGY_DELAY = 15
POWER_EVENT_DELAY_SECONDS = 5
TOTAL_POLLING_TIME_MS = 60 * 1000
POLLING_INTERVAL_MS = 500
ZERO = 0
FOUR = 4
RESUME_TIME = 30
HZRES_4K = 3840
VERRES_2K = 2160
HZRES_2560 = 2560
VERRES_1600 = 1600
HZRES_1920 = 1920
VERRES_1080 = 1080
HZRES_5K = 5120
VERRES_3K = 2880
HZRES_8K = 7680
VERRES_4K = 4320
REFRESH_RATE_60 = 60
REFRESH_RATE_96 = 96
REFRESH_RATE_120 = 120
ONE = 1
TWO = 2
THREE = 3
FIVE = 5
SEVEN = 7

ConfigData = namedtuple('ConfigData', ['topology', 'length'])

config_data_dict = {
    'SINGLE': ConfigData(topology=enum.SINGLE, length=1),
    'EXTENDED': ConfigData(topology=enum.EXTENDED, length=2),
    'CLONE': ConfigData(topology=enum.CLONE, length=2),
    'TRIEXTENDED': ConfigData(topology=enum.EXTENDED, length=3),
    'TRICLONE': ConfigData(topology=enum.CLONE, length=3),
    'QUADEXTENDED': ConfigData(topology=enum.EXTENDED, length=4),
    'QUADCLONE': ConfigData(topology=enum.CLONE, length=4),
}


##
# @brief        This class has to be inherited by all the test cases that tests scenarios related to MST.
class DisplayPortMSTBase(unittest.TestCase):
    ##
    # initialise the command line arguments to None
    cmd_args = None
    # Variable to keep track number of displays before and after test
    number_of_displays_before_test = None
    number_of_displays_after_test = None

    # create variable for Number of Topologies
    cleanup_ports = []
    # variable to hold port type on which topology is connected
    current_port_type = None

    # Contains target id of internal displays
    internal_display_target_id_list = []

    display_port = DisplayPort()  # Create DisplayPort object
    system_utility = sys_util.SystemUtility()  # Create SystemUtility object
    display_config = display_config.DisplayConfiguration()  # Create DisplayConfiguration object
    machine_info = SystemInfo()
    mst_modes_enum_xml_path = "Tests\\Display_Port\\DP_MST\\mst_mode_enum_xml\\"

    ##
    # @brief        This method is used to build and verify a DP1.2 Topology
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   This is the type of topology to be applied like SST, MST, MST Tiled
    # @param[in]    xml_file: str
    #                   Contains xml file path for give topology
    # @return       None
    def setnverifyMST(self, port_type: str, topology_type: str, xml_file: str) -> None:

        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type)

        # Parse and Send Topology details to Gfx Sim driver from user
        self.parse_send_topology(port_type, topology_type, xml_file)

        # Connect DP 1.2 display(s) by issuing HPD
        self.set_hpd(port_type, True)
        time.sleep(5)

        # Verify the MST Topology being created by comparing the data provided and seen in CUI DP topology page
        self.verifyTopology(port_type)

        ##
        # Read the DPCD 600h & check the HPD status
        nativeDPCDRead = True
        dpcd_length = 1

        ##
        # Read the DPCD 21h for checking if immediate branch / native device is MST capable
        dpcd_address = DPCD_MSTM_CAP_OFFSET

        mstm_cap_reg = self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None, action="MST_CAP")
        if mstm_cap_reg & 0x3 == 0x1:  # Check if bit 0 only is set
            logging.info("The Connected Display is MST Display")
        elif mstm_cap_reg & 0x3 == 0x2:  # Check if bit 1 only is set
            logging.info("The connected Display is Single Stream Sideband Message Supported Display")
        else:
            logging.error("[Test Issue]: The Connected Display is not a MST Display.")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] MST Test is running on non-MST display on port: {}".format(port_type),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # current port type on which topology is connected
        self.current_port_type = port_type

    ##
    # @brief        This method is used to build and verify a DP SST Topology
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type2: str
    #                   This is the type of topology to be applied like SST, MST, MST Tiled
    # @param[in]    xml_file2: str
    #                   Contains xml file path for give topology
    # @return       None
    def setnverifySST(self, port_type: str, topology_type2: str, xml_file2: str) -> None:

        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type2)

        # Parse and Send SST details to Gfx Sim driver from the user
        self.parse_send_topology(port_type, topology_type2, xml_file2)

        # Connect DP SST display(s) by issuing HPD
        self.set_hpd(port_type, True)

        ##
        # Read the DPCD 600h & check the HPD status
        nativeDPCDRead = True
        dpcd_length = 1

        ##
        # Read the DPCD 00h for verifying Version of Panel
        dpcd_address = DPCD_VERSION_OFFSET

        version_reg_value = self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None, action="VERSION")
        if version_reg_value == DPCD_VERSION_11:
            logging.info("The Connected Display is a SST Display")
        else:
            logging.error("[Test Issue]: The Connected Display is not a SST Display.")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Verification failed for DP SST display on port: {}".format(port_type),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # current port type on which topology is connected
        self.current_port_type = port_type

    ##
    # @brief        This method is used to apply tiled mode
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   This is the type of topology to be applied like SST, MST, MST Tiled
    # @param[in]    xml_file: str
    #                   Contains xml file path for give topology
    # @param[in]    is_slave: bool
    #                   True if slave is connected, False otherwise
    # @return       None
    def set_tiled_mode(self, port_type: str, topology_type: str, xml_file: str, is_slave: bool = False) -> None:
        # Initialize the DP port object
        self.initialize_dp(port_type, topology_type)

        # Parse and send topology to simulation driver
        self.parse_send_topology(port_type, topology_type, xml_file)

        # Issue HPD (Hotplug interrupt) to graphics driver
        self.set_hpd(port_type, True, is_slave)

        # current port type on which topology is connected
        self.current_port_type = port_type

    ##
    # @brief        This method initialises the object and process the cmd line parameters.
    # @return       None
    def setUp(self):
        # try except has been added to invoke teardown even if any failure happens in setup phase.
        try:
            self.display_power = DisplayPower()  # Create DisplayPower object
            self.requested_topology_info_dict = {}  # type: dict
            self.dp_ports_to_plug = []  # Contains the requested ports from the command line.
            self.linkloss_iteration = 0
            self.disp_sorted_list = []

            # process the command line arguments
            self.process_cmdline()

            self.valsim_handle = GfxValSim()  # GfxValSim initialization required

            # Unplug all the external displays connected apart from eDP/MIPI
            enumerated_displays = self.display_config.get_enumerated_display_info()
            logging.debug(enumerated_displays.to_string())
            for idx in range(enumerated_displays.Count):
                disp_config = enumerated_displays.ConnectedDisplays[idx]
                if disp_config.ConnectorNPortType not in [enum.DP_A, enum.MIPI_A, enum.MIPI_C]:
                    display_port = CONNECTOR_PORT_TYPE(disp_config.ConnectorNPortType)
                    display_port = str(display_port)
                    if display_port[:2] == "DP":
                        result = self.display_port.set_hpd(display_port, False)
                        if result is False:
                            logging.error("Failed to unplug simulated %s display" % display_port)
                            # Gdhm Handled in set_hpd
                        else:
                            logging.info("Unplug of simulated %s display successful" % display_port)

            # Contains all free port list
            self.free_port_list = display_config.get_free_ports()
            logging.info('FREE PORT LIST: {}'.format(self.free_port_list))

            # number of displays before the test starts
            enumerated_displays = self.display_config.get_enumerated_display_info()
            logging.debug(enumerated_displays.to_string())
            self.number_of_displays_before_test = enumerated_displays.Count

            # get all internal display list
            internal_display_list = self.display_config.get_internal_display_list(enumerated_displays)
            if len(internal_display_list) != 0:
                for i in range(len(internal_display_list)):
                    self.internal_display_target_id_list.append(internal_display_list[i][0])
                logging.info("Internal display ID = %s" % self.internal_display_target_id_list)
            else:
                logging.info("No internal display detected")

        except Exception as e:
            logging.error("Unexpected Exception occurred...Exiting...")
            self.tearDown()
            self.fail(e)

    ##
    # @brief        This method processes the cmdline parameters.
    # @return       None
    def process_cmdline(self):
        dp_command_parser = DPCommandParser()
        self.requested_topology_info_dict = dp_command_parser.requested_topology_info_dict
        self.number_of_dp_types = len(self.requested_topology_info_dict)
        self.config = dp_command_parser.requested_config
        self.dp_ports_to_plug = dp_command_parser.requested_dp_port_list
        self.linkloss_iteration = dp_command_parser.requested_linkloss_b2b_iteration
        self.disp_sorted_list = dp_command_parser.get_sorted_display_list
        self.mode_enum_xml_file_path = DisplayPortMSTBase.mst_modes_enum_xml_path + dp_command_parser.mode_enum_xml_file
        logging.info('Number of DP Types: {}'.format(self.number_of_dp_types))
        logging.info('Requested Topology Info Dict: {}'.format(self.requested_topology_info_dict))
        logging.info('Config Requested: {}'.format(self.config))
        logging.info('Requested DP ports: {}'.format(self.dp_ports_to_plug))
        logging.info('Mode Enum XML File Path: {}'.format(self.mode_enum_xml_file_path))

    ##
    # @brief        This method returns number of DP topologies types
    # @return       self.number_of_dp_types: Int
    #                   Contains number of dP types present in the command line
    def get_number_of_dptypes(self) -> int:
        return self.number_of_dp_types

    ##
    # @brief        This method returns number of free DP ports
    # @return       self.display_port.get_number_of_free_dp_ports(): Int
    #                   Contains the total number of free DP ports available
    def get_number_of_free_dp_ports(self) -> int:
        return self.display_port.get_number_of_free_dp_ports()

    ##
    # @brief        This method returns port type for the index
    # @param[in]    index: int
    #                   The index of the port to be fetched from available port list
    # @return       self.dp_ports_to_plug[index]: str
    #                   Contains the type of the port available at given index Ex: DP_B
    def get_dp_port_from_availablelist(self, index: int) -> str:
        return self.dp_ports_to_plug[index]

    ##
    # @brief        This method returns topology type which could be either SST or MST
    # @param[in]    index: int
    #                   Index of the topology to be fetched
    # @return       display_tech: str
    #                   contains the type of topology at given index EX: SST, MST
    def get_topology_type(self, index: int) -> str:
        display_tech = self.requested_topology_info_dict[index].display_tech
        logging.info('Requested Display Tech for Index {} is : {}'.format(index, display_tech))
        return display_tech

    ##
    # @brief        This method returns platform name
    # @return       platform_name: str
    #                   name of the platform EX: TGL, ADLP
    def get_platform_name(self) -> str:
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        platform_name = None
        for i in range(len(gfx_display_hwinfo)):
            platform_name = gfx_display_hwinfo[i].DisplayAdapterName
            break
        return platform_name

    ##
    # @brief        This method returns xml file name
    # @param[in]    index: int
    #                   Index of the topology
    # @return       xml_path: str
    #                   xml file path for requested topology index
    def get_xmlfile(self, index: int) -> str:
        xml_path = self.requested_topology_info_dict[index].path
        logging.info('Requested xml structure for Index {} is : {}'.format(index, xml_path))
        return xml_path

    ##
    # @brief        This is exposed API to parse and send Topology Data to Gfx val simulation driver.
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   contains topology type Ex: SST, MST
    # @param[in]    xmlfile: str
    #                   path of the xml file to be parsed
    # @param[in]    lowpower: bool
    #                   True if Low Power State, False otherwise
    # @return       None.
    def parse_send_topology(self, port_type: str, topology_type: str, xmlfile: str, lowpower: bool = False) -> None:
        retStatus = self.display_port.parse_send_topology(port_type, topology_type, xmlfile, lowpower)
        if retStatus:
            logging.info("%s data parsed and sent to simulation driver successfully" % topology_type)
        else:
            logging.error("%s data parsed and sent to simulation driver failed..." % topology_type)
            # Gdhm bug reporting handled in display_port.parse_send_topology
            self.fail()

    ##
    # @brief        This is exposed API to initialize the DP Info structure
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   contains topology type Ex: SST, MST
    # @return       None.
    def initialize_dp(self, port_type: str, topology_type: str) -> None:
        retStatus = self.display_port.init_dp(port_type, topology_type)
        if retStatus:
            logging.info("Graphics simulation driver initialized DP object successfully")
        else:
            logging.error("Graphics simulation driver initialized DP object Failed")
            # Gdhm bug reporting handled in display_port.init_dp
            self.fail()

    ##
    # @brief        This is exposed API to verify set the Hot Plug Event Notification
    # @param[in]    port_name: str
    #                   contains port name Ex: DP_B, HDMI_B
    # @param[in]    attach_dettach: bool
    #                   True if connector port has to be attached, False otherwise
    # @param[in]    is_slave: bool
    #                   True if slave is connected, False otherwise
    # @return       None.
    def set_hpd(self, port_name: str, attach_dettach: bool, is_slave: bool = False) -> None:
        retStatus = self.display_port.set_hpd(port_name, attach_dettach)
        status = False
        if retStatus:
            logging.info(
                f'Port at which display is connected/disconnected - {port_name}, attach_dettach - {attach_dettach}')

            # Get platform name
            platform = self.get_platform_name()

            # If the tiled display is connected, we won't get the slave port in enumerated displays, Hence adding delay
            # WA for DG platforms to skip verification for unplug due to OS behavior. Sometimes OS does not update
            # Unplug Status for last display
            if is_slave or (attach_dettach is False and platform in ['DG1', 'DG2', 'ELG']):
                is_pre_si_environment = self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                                 "SIMENV_PIPE2D"]

                # 5 sec delay is given for post-si, 20 sec delay is given for pre-si platforms.
                delay_in_seconds = 20 if is_pre_si_environment else 5
                time.sleep(delay_in_seconds)
                status = True
            else:
                polling_counter = 1
                max_retry_count = (TOTAL_POLLING_TIME_MS / POLLING_INTERVAL_MS)
                while polling_counter <= max_retry_count:
                    display_config = self.display_config.get_enumerated_display_info()

                    connected_displays = [str(CONNECTOR_PORT_TYPE(display_config.ConnectedDisplays[display_count].
                                                                  ConnectorNPortType)) for display_count in
                                          range(display_config.Count)]

                    if (
                            (attach_dettach is True and port_name in connected_displays) or
                            (attach_dettach is False and port_name not in connected_displays)
                    ):
                        status = True
                        break

                    time.sleep(POLLING_INTERVAL_MS / DELAY_1000_MILLISECONDS)
                    polling_counter += 1

            # If display is not enumerated within the time even after plug limit, fail the test.
            # If display is enumerated within the time limit even after unplug, fail the test.
            if status is False:
                self.fail(f'Plug / Unplug failed. attach_detach - {attach_dettach}')

            # If plug / unplug is successful, update the cleanup_ports
            if status:
                if attach_dettach:
                    logging.info("Simulation driver issued HPD (Hotplug Interrupt) to Graphics driver successfully")
                    self.cleanup_ports.append(port_name)
                else:
                    logging.info("Simulation driver issued HPD (Hotunplug Interrupt) to Graphics driver successfully")
                    self.cleanup_ports.remove(port_name)

        else:
            logging.error("Simulation driver failed to issue HPD to Graphics driver")
            # Gdhm bug reporting handled in gfxvalsim.set_hpd
            self.fail()

    ##
    # @brief        This is exposed API to Read DPCD from the offset
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    nativeDPCDRead: bool
    #                   True for Native DPCD read, False otherwise
    # @param[in]    length: int
    #                   length of DPCD Values to be read
    # @param[in]    addr: str
    #                   DPCD offset
    # @param[in]    node_rad: object
    #                   MST Relative address object
    # @param[in]    action: str
    #                   Valid DPCD actions include ['PLUG', 'VERSION', 'MST_CAP']
    # @return       dpcd_reg_val[0]: str
    #                   Return the register value
    def dpcd_read(self, port_type, nativeDPCDRead, length, addr, node_rad, action="PLUG"):
        action = action.upper()
        if action not in ['PLUG', 'VERSION', 'MST_CAP']:
            logging.error("Invalid dpcd action for display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Invalid dpcd action-'{}' received for display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()
        dpcd_flag, dpcd_reg_val = self.display_port.read_dpcd(port_type, nativeDPCDRead, length, addr, node_rad)

        if action == 'PLUG' and dpcd_flag:
            logging.info("DPCD Read Value: %s" % (dpcd_reg_val[0]))
            reg_val = dpcd_reg_val[0] & 0x000000FF
            if reg_val == DP_HOTPLUG_GOLDEN_VALUE:
                logging.info("DPCD read successful for Hotplug: Register Value: %s" % reg_val)
            else:
                logging.error("DPCD Flag:%s & Register value:%s during DPCD Read Failure" % (dpcd_flag, reg_val))
                logging.error("DPCD read failed for Hotplug. Exiting ...")
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Unexpected reg value {} at register {} during Hotplug ".
                    format(reg_val, hex(addr)),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

        elif action == 'VERSION' and dpcd_flag:
            logging.info("DPCD Version Value: %x" % dpcd_reg_val[0])
            return dpcd_reg_val[0]

        elif action == 'MST_CAP' and dpcd_flag:
            logging.info("DPCD MST CAP offset 0x21 Value: %x" % dpcd_reg_val[0])
            return dpcd_reg_val[0]

        else:
            logging.error("Read DPCD api Failed, Exiting ...")
            # Gdhm bug reporting should be handled in display_port.read_dpcd
            self.fail()

    ##
    # @brief        This is exposed API to verify topology between CUI and Driver
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    action
    #                   Valid actions include ['PLUG', 'UNPLUG']
    # @return       None.
    def verifyTopology(self, port_type: str, action: str = "PLUG") -> None:
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("[Test Issue]: Invalid plug action for display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Invalid plug action-'{}' received for display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # Topology verification is dependent on CUI SDK API's
        if not self.system_utility.is_ddrw():
            retStatus = self.display_port.verify_topology(port_type)
        else:
            # In Yangra driver CUI is not supported hence
            # making verification success by default
            if action == 'PLUG':
                retStatus = ZERO
            else:
                retStatus = FOUR
        if action == 'PLUG' and retStatus == ZERO:
            logging.info("MST Topology Verification Success, Applied and Expected topologies are matching")
        elif action == 'UNPLUG' and retStatus == FOUR:
            logging.info("MST Topology Verification Success: HPD(UNPLUG) event")
        else:
            try:
                logging.error("MST Topology Verification Failed..Status Code:%s" % TOPOLOGY_STATUS_CODE(retStatus).name)
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Topology verification Failed with Status Code: {}".
                    format(TOPOLOGY_STATUS_CODE(retStatus).name),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()
            except ValueError as Error:
                logging.error("MST Topology Verification Failed.. No Matching Status Code Fund...%s" % Error)
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Topology verification Failed with unknown error code",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

    ##
    # @brief        This is exposed API to compare native mode enumerated by Graphics driver and EDID
    # @return       None
    def verify_max_supported_mode(self) -> None:
        ## varible to keep track if we find DP displays
        found = False
        # number of active DP displays
        number_of_displays = 0
        internal_display_connected = False
        # List of DP port types
        # currently for SINGLE configuration is applied for eDP also
        # hence DP_A is also added list and native mode is verified for eDP also
        # in future if we decide not to apply SINGLE config for eDP
        # we need to remove eDP ie DP_A from port_types_list
        port_types_list = {'DP_B', 'DP_C', 'DP_D', 'DP_E', 'DP_F', 'DP_A', 'DP_G', 'DP_H', 'DP_I'}
        # List of DP active target ids
        dp_target_ids = []
        # variables to handle the case of number of display = 3 for Gen10+ platforms
        fourk_counter = 0
        twok_counter = 0
        edid_counter = 0
        # platform generation variables
        platform = None
        platform_name = None

        # call get_machine_info() to get the platform type from SystemUtility DLL
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            platform_name = gfx_display_hwinfo[i].DisplayAdapterName
            break

        if platform_name == 'SKL' or platform_name == 'KBL' or platform_name == 'GLK' or platform_name == 'CFL':
            platform = 'Gen9'
        elif platform_name == 'CNL':
            platform = 'Gen10'
        elif platform_name == 'ICL' or platform_name == 'ICLLP' or platform_name == 'ICLHP' or platform_name == 'LKF1':
            platform = 'Gen11'
        elif platform_name == 'TGL' or platform_name == 'DG1' or platform_name == 'ADLS':
            platform = 'Gen12'
        elif platform_name == 'DG2' or platform_name == 'ADLP':
            platform = 'Gen13'
        elif platform_name == 'ELG' or platform_name == 'MTL':
            platform = 'Gen14'
        elif platform_name == 'LNL':
            platform = 'Gen15'
        elif platform_name == 'PTL':
            platform = 'Gen16'

        # Get the enumerated displays from SystemUtility.DLL
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays is None:
            # Gdhm bug reporting handled in get_enumerated_display_info()
            self.fail()

        logging.info('Enumerated displays: {}'.format(enumerated_displays.to_string()))

        # find the active number of DP displays and their target ids
        for index in range(enumerated_displays.Count):
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            port_type = CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            if target_id in self.internal_display_target_id_list:
                internal_display_connected = True
                continue

            if port_type in port_types_list and enumerated_displays.ConnectedDisplays[index].IsActive:
                found = True
                number_of_displays = number_of_displays + 1
                dp_target_ids.append(target_id)

        logging.info("Number of Active DP Displays: %s" % number_of_displays)

        # For single config eDP modeset might have done, just skip this verification for eDP
        if number_of_displays == 0 and internal_display_connected is True and self.config == 'SINGLE':
            found = True

        # verify the Hor res, vertical res and refresh Rate between driver and EDIDs
        for index in range(len(dp_target_ids)):

            logging.info("Max Native Mode: Target ID: %s" % (dp_target_ids[index]))

            # Get the native mode from EDID file
            native_mode = self.display_config.get_native_mode(dp_target_ids[index])
            if native_mode is None:
                logging.error(f"Failed to get native mode for {dp_target_ids[index]}")
                self.fail()

            # Split the string and get the values of horizontal,vertical
            # resolution and RR
            edid_hzres = native_mode.hActive
            edid_verres = native_mode.vActive
            edid_refreshrate = native_mode.refreshRate

            # Get the max supported mode currently being set from Graphics driver
            current_mode = self.display_config.get_current_mode(dp_target_ids[index])

            driver_hzres = current_mode.HzRes
            driver_verres = current_mode.VtRes
            driver_refresfrate = current_mode.refreshRate

            # Sometimes RR b/w Gfx driver and EDID may vary by ~1-5%. We consider RRs are same if diff b/w RRs are
            # max deviated by 5%
            difference = abs(edid_refreshrate - driver_refresfrate)
            max_refreshrate = max(edid_refreshrate, driver_refresfrate)
            diffinpercentage = (float(difference) / max_refreshrate) * 100

            # TODO
            # incase the modes change for a platform or policies changes
            # Corresponding enhancements needs to be done
            # currently mode verification is as per the below table

            ##
            # verification of max supported mode should be as per below data
            # for DP 1.2
            # DP1.2 No.  of Displays    Max.  Resolution        Platforms supported
            #            1              4k2k @ 60Hz             All Gen9 platforms - SKL, KBL, GLK and  CFL
            #            2              25x16 @60Hz on each Display
            #            3/4            1920x1080 60Hz on each Display
            if platform == 'Gen9':
                target_refreshrate = REFRESH_RATE_60
                if number_of_displays == ONE:
                    target_hzres = HZRES_4K
                    target_verres = VERRES_2K
                elif number_of_displays == TWO:
                    target_hzres = HZRES_2560
                    target_verres = VERRES_1600
                elif number_of_displays == THREE or number_of_displays == FOUR:
                    target_hzres = HZRES_1920
                    target_verres = VERRES_1080
                # match the native resolution between driver and platform values as per above table
                if driver_hzres == target_hzres and driver_verres == target_verres and driver_refresfrate == target_refreshrate:
                    logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                 (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                # if the native resolution does not match in above case then compare between EDID and driver
                elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                    logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                 (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                else:
                    logging.error(
                        "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!." \
                        % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                    gdhm.report_bug(
                        title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                              "x{}@{}) does not match with max supported mode in EDID({})".
                        format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail()
            ##
            # verification of max supported mode should be as per below data
            # for DP 1.3 and DP 1.4
            # DP1.3/DP1.4   No.  of Displays    Max.  Resolution        Platforms supported
            #                   1               5k3k @ 60Hz             All Gen10+ (Gen10, Gen11 & Gen12) platforms - CNL, ICL and TGL+
            #                                   4k2k @ 120Hz @ 24bpp
            #                                   4k2k @ 96Hz @ 30bpp
            #                                   8kx4k@60 Hz @ 24bpp
            #                   2               4k2k @ 60Hz @ 24bpp on each display
            #                                   8k @ 60 Hz - 24bpp 4:4:4 on each display
            #                   3               1 - 4k2k @ 60Hz & 2 - 25x16 @ 60Hz
            #                   4               25x16 @ 60Hz on each Display
            #                   7               19x10 @ 60Hz on each Display - 24bpp 4:4:4
            elif platform == 'Gen10' or platform == 'Gen11' or platform == 'Gen12' or platform == 'Gen13' or \
                    platform == 'Gen14' or platform == 'Gen15' or platform == 'Gen16':
                if number_of_displays == ONE:
                    # match the native resolution between driver and platform values as per above table
                    if (
                            driver_hzres == HZRES_5K and driver_verres == VERRES_3K and driver_refresfrate == REFRESH_RATE_60) \
                            or (
                            driver_hzres == HZRES_4K and driver_verres == VERRES_2K and driver_refresfrate == REFRESH_RATE_120) \
                            or (
                            driver_hzres == HZRES_4K and driver_verres == VERRES_2K and driver_refresfrate == REFRESH_RATE_96) \
                            or (
                            driver_hzres == HZRES_8K and driver_verres == VERRES_4K and driver_refresfrate == REFRESH_RATE_60):
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    # if the native resolution does not match in above case then compare between EDID and driver
                    elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    else:
                        logging.error(
                            "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!" \
                            % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                                  "x{}@{}) does not match with max supported mode in EDID({})".
                            format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

                elif number_of_displays == TWO:
                    # match the native resolution between driver and platform values as per above table
                    if driver_hzres == HZRES_4K and driver_verres == VERRES_2K and driver_refresfrate == REFRESH_RATE_60 \
                            or (
                            driver_hzres == HZRES_8K and driver_verres == VERRES_4K and driver_refresfrate == REFRESH_RATE_60):
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    # if the native resolution does not match in above case then compare between EDID and driver
                    elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    else:
                        logging.error(
                            "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!" \
                            % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                                  "x{}@{}) does not match with max supported mode in EDID({})".
                            format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

                elif number_of_displays == FOUR:
                    # match the native resolution between driver and platform values as per above table
                    if driver_hzres == HZRES_2560 and driver_verres == VERRES_1600 and driver_refresfrate == REFRESH_RATE_60:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    # if the native resolution does not match in above case then compare between EDID and driver
                    elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    else:
                        logging.error(
                            "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!" \
                            % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                                  "x{}@{}) does not match with max supported mode in EDID({})".
                            format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

                elif number_of_displays == SEVEN:
                    # match the native resolution between driver and platform values as per above table
                    if driver_hzres == HZRES_1920 and driver_verres == VERRES_1080 and driver_refresfrate == REFRESH_RATE_60:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    # if the native resolution does not match in above case then compare between EDID and driver
                    elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                        logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    else:
                        logging.error(
                            "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!" \
                            % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                                  "x{}@{}) does not match with max supported mode in EDID({})".
                            format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

                elif number_of_displays == THREE:
                    # match the native resolution between driver and platform values as per above table
                    if driver_hzres == HZRES_4K and driver_verres == VERRES_2K and driver_refresfrate == REFRESH_RATE_60:
                        fourk_counter = fourk_counter + 1
                    elif driver_hzres == HZRES_2560 and driver_verres == VERRES_1600 and driver_refresfrate == REFRESH_RATE_60:
                        twok_counter = twok_counter + 1
                    # if the native resolution does not match in above case then compare between EDID and driver
                    elif driver_hzres == edid_hzres and driver_verres == edid_verres and diffinpercentage <= FIVE:
                        edid_counter = edid_counter + 1

            # Matching Platform is not found..exit
            else:
                logging.error("%s Platform is not supported" % platform_name)
                self.fail()

        # for Gen10+ platforms, exception case of number of displays = 3 is handled
        if (platform == 'Gen10' or platform == 'Gen11' or platform == 'Gen12' or platform == 'Gen13' or
            platform == 'Gen14' or platform == 'Gen15' or platform == 'Gen16') and number_of_displays == 3:
            if (fourk_counter == 1 and twok_counter == 2) or (fourk_counter + twok_counter + edid_counter == 3):
                logging.info("Graphics driver enumerated Max Supported mode Successfully: %sx%sx%s" % \
                             (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
            else:
                logging.error(
                    "[Driver Issue]: Max Supported Mode (Enumerated from Gfx driver): %sx%sx%s, Max Supported Mode (Present in EDID file): %s are different!" \
                    % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode))
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Max Supported Mode enumerated by Driver({}"
                          "x{}@{}) does not match with max supported mode in EDID({})".
                    format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, native_mode),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

        if found is False:
            logging.error(
                "Verify Max Supported mode enumeration failed. Port type not found: %s... Exiting" % port_type)
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Max Supported Mode enumeration failed for port: {}".format(port_type),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief        This method retrieves the RAD for port number
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @return       disp_rad: object
    #                   returns branch display rad array Object
    def get_topology_rad(self, port_type):
        retStatus, disp_rad = self.display_port.get_mst_topology_rad(port_type)
        if retStatus:
            logging.info("RAD Information retrieved successfully for the current topology")
            return disp_rad
        else:
            logging.error("RAD Information retrieve Failed")
            # Gdhm bug reporting handled in get_mst_topology_rad
            self.fail()

    ##
    # @brief        This method attachs/detaches branch/display from the full topology
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    attach_dettach: bool
    #                   True if connector port has to be attached, False otherwise
    # @param[in]    noderad: object
    #                   MST Relative address object
    # @param[in]    xmlfile: str
    #                   Path of the xml file
    # @param[in]    lowpower: bool
    #                   True if Low Power State, False otherwise
    # @return       None
    def set_partial_topology(self, port_type, attach_dettach, noderad, xmlfile, lowpower=False):
        retStatus = self.display_port.set_mst_partial_topology(port_type, attach_dettach, noderad, xmlfile, lowpower)
        time.sleep(PARTIAL_TOPOLOGY_DELAY)
        if retStatus:
            if attach_dettach is True:
                logging.info("Successfully attached branch/display from the current topology")
            else:
                logging.info("Successfully detached branch/display from the current topology")
        else:
            logging.error("Simulation driver failed to attach/detach branch/display from the current topology")
            # Gdhm bug reporting handled in set_mst_partial_topology
            self.fail()

    ##
    # @brief        This is exposed API to Plug/Unplug Topology during Lowe Power State
    # @param[in]    num_of_ports: int
    #                   Number of Ports
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    sink_plugreq: str
    #                   valid requests include: PlugSink, UnplugSink, UnPlugOldToplology and PlugNew Topology
    # @param[in]    plug_unplug_atsource: bool
    #                   True if we are plugging at depth 0 else False
    # @param[in]    topology_after_resume: str
    #                   Topology to be plugged/unplugged after resume
    # @return       None.
    def set_low_power_state(self, num_of_ports: int, port_type: str, sink_plugreq: str, plug_unplug_atsource: bool,
                            topology_after_resume: str) -> None:
        retStatus = self.display_port.set_low_power_state(num_of_ports, port_type, sink_plugreq, plug_unplug_atsource,
                                                          topology_after_resume)
        if retStatus:
            logging.info("Simulation driver issued Low Power State HPD Data to Graphics driver successfully")
        else:
            logging.info("Simulation driver issue of Low Power State HPD Data to Graphics driver failed")
            # Gdhm bug reporting handled in set_low_power_state
            self.fail()

    ##
    # @brief        This method helps in Setting Power Events- S3, S4, CS, S5
    # @param[in]    power_state: str
    #                   power state to be applied EX: s3, s4, cs, s5
    # @param[in]    resume_time: int
    #                   It is the time the system has to wait before resuming from the power state
    # @return       None
    def power_event(self, power_state: str, resume_time: int) -> None:
        if self.display_power.invoke_power_event(power_state, resume_time):
            time.sleep(POWER_EVENT_DELAY_SECONDS)
        else:
            self.fail(f"[Test Issue]: Entry or Exit from {power_state.name} power event Failed. Exiting .....")

    ##
    # @brief        This is exposed API to apply config and do mode set
    # @return       None.
    def set_config_apply_max_mode(self) -> None:

        # To have a list of target ID's
        mode_target_id_list = []

        ##
        # Get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()

        # get the combinations of target id's to set the config
        display_config, config_combination_list = self.get_all_config_combinations()

        # fill the DisplayConfig structure
        set_config = DisplayConfig()
        set_config.topology = display_config

        for current_config_list in range(len(config_combination_list)):

            targetId = config_combination_list[current_config_list]
            # Excluding the eDP target from list of target id's
            if self.config == 'SINGLE' and targetId[0] in self.internal_display_target_id_list:
                continue
            path = 0
            for index in range(len(targetId)):
                set_config.displayPathInfo[path].targetId = targetId[index]
                set_config.displayPathInfo[path].displayAndAdapterInfo = enumerated_displays.ConnectedDisplays[
                    index].DisplayAndAdapterInfo
                path += 1

            set_config.numberOfDisplays = path
            logging.info("Trying to Apply Display Configuration as : %s", set_config.to_string(enumerated_displays))
            ##
            # Apply display configuration
            self.display_config.set_display_configuration(set_config)

            ##
            # Getting current configuration
            get_config = self.display_config.get_current_display_configuration()
            logging.info("Current display configuration: %s", get_config.to_string(enumerated_displays))

            if get_config.equals(set_config):
                logging.info("Successfully applied display configuration")
            else:
                logging.error("[Driver Issue]: Failed to apply display configuration")
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Applied configuration and driver enumerated configuration "
                          "does not match",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

            mode_target_id_list = list(targetId)
            for target_id in mode_target_id_list:
                if target_id in self.internal_display_target_id_list:
                    mode_target_id_list.remove(target_id)

        ##
        # supported_modes[] is a list of modes supported by the display
        supported_modes = self.display_config.get_all_supported_modes(mode_target_id_list)
        for key, values in supported_modes.items():
            logging.info("**********Got the supported modes and applying max mode...............")
            sorted_modes_list = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
            ##
            # Apply the last mode(i.e. values[-1]) from the supported_modes[] which will be having the maximum
            # resolution
            modes_flag = self.display_config.set_display_mode([sorted_modes_list[-1]])
            if modes_flag is False:
                # Gdhm bug reporting handled in set_display_mode()
                self.fail()

            # self.verify_tiled_nontiled_mode(targetId[index],True,False)

    ##
    # @brief        This method gets list of all tiled display's target ids attached to the system.
    # @return       Boolean value, List of tiled target ids: bool, list
    #                   returns boolean value with list of target ids
    def get_tiled_displays_list(self):

        tiled_display_found = False

        # List to hold list of all tiled display's target ids
        tiled_target_ids_list = []

        # List to hold list of all non-tiled display's target ids
        nontiled_target_ids_list = []

        # get the current display config from DisplayConfig
        config = self.display_config.get_all_display_configuration()

        for index in range(config.numberOfDisplays):

            # Get target id of the display
            target_id = config.displayPathInfo[index].targetId

            # Get tiled information if display associated with target id is Tiled display
            tile_info = self.display_port.get_tiled_display_information(target_id)

            # Check for tiled status
            if tile_info.TiledStatus:
                # Tiled display found! append to the list
                tiled_target_ids_list.append(target_id)
                tiled_display_found = True

            else:
                # Tiled display found! append to the list
                nontiled_target_ids_list.append(target_id)

        if tiled_display_found:
            # If at least one tiled display found, then return TRUE and list containing tiled target ids to the caller
            return True, tiled_target_ids_list

        else:
            # Tiled display(s) not found! Return FALSE to the caller
            return False, nontiled_target_ids_list

    ##
    # @brief        This method verifies whether tiled mode (tiled could be enabled/disabled in panel OSD) applied
    #               successfully or not
    # @param[in]    tiled_target_id: int
    #                   Target id of the tiled display
    # @param[in]    is_tiled: bool
    #                   This flag indicates whether panel is tiled or not.True if tiled, False otherwise
    # @param[in]    is_sst_master_only: bool
    #                   This flag Indicates whether only master tile of SST panel is plugged
    # @return       None
    def verify_tiled_nontiled_mode(self, tiled_target_id: int, is_tiled: bool, is_sst_master_only: bool) -> None:

        # Extract Native X, Y and RR from EDID
        native_mode = self.display_config.get_native_mode(tiled_target_id)
        if native_mode is None:
            self.fail(f"Failed to get native mode for {tiled_target_id}")
        native_x_resolution = native_mode.hActive
        native_y_resolution = native_mode.vActive
        native_rr = native_mode.refreshRate
        logging.info("Native mode details of %d panel: %sx%s@%s" % (tiled_target_id, native_x_resolution,
                                                                    native_y_resolution, native_rr))

        # Get the currently applied mode from Graphics driver.
        current_mode = self.display_config.get_current_mode(tiled_target_id)
        logging.info("Current mode details of %d panel: %sx%s@%s" % (tiled_target_id, current_mode.HzRes,
                                                                     current_mode.VtRes, current_mode.refreshRate))

        # Verify whether it is tiled display or not
        if is_tiled:

            # Tiled display found! Get the corresponding tiled information
            tile_info = self.display_port.get_tiled_display_information(tiled_target_id)

            # Verify tiled display's X, Y present in the tiled information variable
            if tile_info.TiledStatus:
                tiled_x_resolution = tile_info.HzRes
                tiled_y_resolution = tile_info.VtRes
            else:
                logging.error("Tiled information not available in the Tiled display. Exiting ...")
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] DP Tiled tests are running on non-tiled display",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

            tiled_rr = native_rr  # Tiled RR is same as native resolution's RR
            logging.info("%d is Tiled panel with mode details: %sx%s@%s" % (tiled_target_id, tiled_x_resolution,
                                                                            tiled_y_resolution, tiled_rr))

            '''
                Algorithm to verify whether current and expected modes are identical or not.
            '''

            # Sometimes RR b/w Gfx driver and EDID may vary by ~1-5%. We consider RRs are same if diff b/w RRs are
            # max deviated by 5%
            # FIXME:    Commenting below lines due to https://hsdes.intel.com/resource/1606760328
            #           difference = abs(tiled_rr - current_mode.refreshRate)
            #           max_refresh_rate = max(tiled_rr,current_mode.refreshRate)
            #           diff_in_percentage = (float(difference)/max_refresh_rate) * 100

            # TODO:     For now X and Y are hard-coded to 4k & 2k respectively for 5k3k SST tiled panel but ideally,
            #           when master port only connected, Driver sets mode present in the CEA DTD timing. Currently,
            #           system utility library doesn't supports API to read timings from CEA block. Once, CEA block
            #           parsing support added, we will remove this hard-coding.

            gfx_display_hw_info_list = self.machine_info.get_gfx_display_hardwareinfo()
            if len(gfx_display_hw_info_list) != 0:
                platform_name = gfx_display_hw_info_list[0].DisplayAdapterName
            else:
                self.fail('Failed to get Platform Name. Exiting...')

            # Restrict the Max Resolution based on the panel capability as well as platform.
            if is_sst_master_only or platform_name == 'LKF1':
                tiled_x_resolution = HZRES_4K
                tiled_y_resolution = VERRES_2K

            # Verify whether current and expected modes are identical or not
            if current_mode.HzRes == tiled_x_resolution and current_mode.VtRes == tiled_y_resolution:
                logging.info("Tiled mode (enumerated by Gfx driver) and expected tiled mode (as per EDID) are "
                             "identical: %sx%s@%s" % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
            else:
                logging.error(
                    "[Driver Issue]: Tiled mode (enumerated by Gfx driver): %sx%s@%s and expected tiled mode (as per EDID): "
                    "%sx%s@%s are different!" % (current_mode.HzRes, current_mode.VtRes,
                                                 current_mode.refreshRate, tiled_x_resolution,
                                                 tiled_y_resolution, tiled_rr))
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Tiled Mode enumerated by Driver({}x{}@{}) and"
                          " Tiled EDID mode({}x{}@{}) are not matching".
                    format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, tiled_x_resolution,
                           tiled_y_resolution, tiled_rr),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

        # Tiled mode disabled! It is tiled panel but tiled mode disabled in the panel OSD
        else:
            '''
                Algorithm to verify whether current and expected modes are identical or not.
            '''
            # As the RR between driver and EDID may vary, we consider RRs are same if differences b/w RRs is
            # max 5% deviation
            # FIXME:    Commenting below lines due to https://hsdes.intel.com/resource/1606760328
            #           difference = abs(native_rr - current_mode.refreshRate)
            #           max_refresh_rate = max(native_rr,current_mode.refreshRate)
            #           diff_in_percentage = (float(difference)/max_refresh_rate) * 100

            # TODO:     For now XxYxRR are hard-coded to 4kx2k@60 for 4k2k MST tiled panel but ideally,
            #           when MST is disabled, driver sets mode present in the CEA DTD timing. Currently, system utility
            #           library doesn't supports API to read timings from CEA  block. Once, CEA block parsing support
            #           added, we will remove this hard-coding.

            tiled_mst_disable_h_res = HZRES_4K
            tiled_mst_disable_v_res = VERRES_2K
            tiled_mst_disable_rr = 30

            if current_mode.HzRes == native_x_resolution and current_mode.VtRes == native_y_resolution:
                logging.info("MST tiled disabled mode (enumerated by Gfx driver) and expected tiled disabled mode "
                             "(as per EDID) are identical")
            else:
                logging.error(
                    "[Driver Issue]: MST tiled disabled mode (enumerated by Gfx driver): %sx%s@%s and expected tiled disabled"
                    " mode (as per EDID): %sx%s@%s are different!" % (current_mode.HzRes, current_mode.VtRes,
                                                                      current_mode.refreshRate,
                                                                      tiled_mst_disable_h_res,
                                                                      tiled_mst_disable_v_res,
                                                                      tiled_mst_disable_rr))
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Tiled disabled Mode enumerated by Driver({}x{}@{}) and"
                          " Tiled disabled EDID mode({}x{}@{}) are not matching".
                    format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate,
                           tiled_mst_disable_h_res, tiled_mst_disable_v_res, tiled_mst_disable_rr),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

    ##
    # @brief        This method Verifies tiled/non-tiled applied successfully or not
    # @param[in]    is_mst: bool
    #                   Flag indicating MST or SST tiled mode. TRUE indicates MST mode and FALSE indicates SST mode
    # @param[in]    mst_status: bool
    #                   Flag indicates whether MST enabled or disabled in panel OSD
    # @param[in]    is_sst_master_only: bool
    #                   Indicates only master tile of SST panel is plugged
    # @param[in]    tiled_target_id: int
    #                   Target id of the tiled display
    # @return       None
    # @note         Below verify_tiled_mode is generic function which should work for both SST and MST tiled modes.
    #               Currently DFT based SST tiled simulation uses different function verify_tiled_mode
    #               (Display_Port/DP_Tiled/display_port_base.py).Ensure to switch to below new function when moving from
    #               DFT based to Simulation driver based approach.

    def verify_tiled_display(self, is_mst: bool, mst_status: bool, is_sst_master_only: bool,
                             tiled_target_id: int) -> None:
        if is_mst is False:

            # Set flag is_sst_master_only to FALSE to indicate we are in SST path
            logging.info("Plugged panel %d is SST tiled" % tiled_target_id)
            self.verify_tiled_nontiled_mode(tiled_target_id, True, is_sst_master_only)

        # is_MST TRUE means, we are in MST tiled path
        else:
            # Set flag is_sst_master_only to TRUE to indicate we are in MST path
            is_sst_master_only = True

            # Its MST panel and MST is enabled in panel's OSD
            if mst_status:

                logging.info("Plugged panel %d is MST tiled and MST is enabled in panel OSD" % tiled_target_id)

                # Tiled modes verification algorithm is same for both SST and MST tiled (with MST enabled in panel OSD)
                self.verify_tiled_nontiled_mode(tiled_target_id, True, is_sst_master_only)

            # Its MST panel but MST is disabled in panel's OSD
            else:
                # If we hit ELSE logic means, plugged panel is MST tiled but MST disabled in panel OSD
                logging.info("Plugged panel %d is MST tiled but MST is disabled in panel OSD" % tiled_target_id)

                self.verify_tiled_nontiled_mode(tiled_target_id, False, is_sst_master_only)

    ##
    # @brief        This method sets scaling options(min, mid and max resolutions) for the connected displays.
    # @return       None
    def set_display_scaling(self) -> None:
        # arguments are: set_mode=True, power_event = False and apply_scaling = True
        self.set_display_config_and_modes(True, False, True)

    ##
    # @brief        This method sets mode(min, mid and max resolutions) for all the configurations of connected displays
    # @return       None
    def set_display_modes(self) -> None:
        # arguments are: set_mode=True, power_event = False and apply_scaling = False
        self.set_display_config_and_modes(True, False, False)

    ##
    # @brief        This method sets all possible combinations of displays configurations for the given configuration in
    #               command line
    # @return       None
    def set_display_config(self) -> None:
        # arguments are: set_mode=False
        self.set_display_config_and_modes(False)

    ##
    # @brief        This method gets all possible combinations of displays configurations for the given configuration in
    #               command line
    # @return       tuple[object, list]
    #                   Returns tuple containing display config topology object, connector_port_list
    def get_all_config_combinations(self):
        # arguments are: set_mode=False, power_event=True
        return self.set_display_config_and_modes(False, True)

    ##
    # @brief        This method sets the supported display scaling options with different supported RRs
    # @param[in]    modelist: object
    #                   Object of Display Mode structure type
    # @param[in]    HzRes: int
    #                   Horizontal resolution
    # @param[in]    VtRes: int
    #                   vertical resolution
    # @param[in]    refresh_rate: int
    # @return       None
    def set_scaling(self, modelist, HzRes, VtRes, refresh_rate):
        # create local copy of mode list
        mode_list = list(modelist)
        # filter out only the required modes
        for mode in range(len(modelist)):
            if (modelist[mode].HzRes != HzRes or modelist[mode].VtRes != VtRes or modelist[
                mode].refreshRate != refresh_rate):
                mode_list.remove(modelist[mode])

        # variable to hold the current scaling being set
        current_scaling = None

        # apply the required modes
        for mode in range(len(mode_list)):
            # this condition makes sure that we always hit physical mode set path
            if current_scaling != mode_list[mode].scaling:
                # Apply the mode from the supported_modes with virtual mode set as True for Clone modes only, else false.
                if self.config == "CLONE" or self.config == "TRICLONE":
                    modes_flag = self.display_config.set_display_mode([mode_list[mode]], True)
                else:
                    modes_flag = self.display_config.set_display_mode([mode_list[mode]], False)
                if modes_flag is False:
                    logging.error("[Driver Issue]: Failed to apply display mode {}x{}x{}Hz. Exiting ...".
                                  format(mode_list[mode].HzRes, mode_list[mode].VtRes, mode_list[mode].refreshRate))
                    # Gdhm bug reporting handled in set_display_mode
                    self.fail()

                # for eDP, need not check DPCD
                if mode_list[mode].targetId not in self.internal_display_target_id_list:
                    # verify DPCD after mode set
                    nativeDPCDRead = True
                    dpcd_length = 1

                    ##
                    # Read the DPCD 600h for verifying Sink detected or not
                    dpcd_address = DPCD_SINK_CONTROL

                    self.dpcd_read(self.current_port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                   action="PLUG")

                current_scaling = mode_list[mode].scaling

    ##
    # @brief        This method sets mode(min, mid and max resolutions) on the connected displays.
    # @param[in]    apply_scaling: bool
    #                   True if scaling needs to be set else false
    # @return       None
    def set_modes(self, apply_scaling: bool) -> None:
        ##
        # displays_target_list[] is a list of target ids of all the displays
        displays_target_list = []
        ##
        # Get the all display config from DisplayConfig
        # ie Single/Clone/Extended
        config = self.display_config.get_current_display_configuration()
        ##
        # if configuration to be set is Extended or Single as given in the cmd line
        # append displays_target_list[] with target ids of both the primary and secondary
        # display

        # log whether scaling is requested
        logging.debug("Scaling requested:{}".format(apply_scaling))

        # TODO:
        # config variable to be handled for the Quad Clone/Extended cases
        if self.config == "CLONE" or self.config == "TRICLONE":
            ##
            # if configuration to be set is Clone as given in the cmd line then append
            # displays_target_list[] with target id of only the primary display connected
            # as per the change done in the API set_dislay_mode() in display_config.py
            displays_target_list.append(config.displayPathInfo[0].targetId)
        else:
            for index in range(config.numberOfDisplays):
                displays_target_list.append(config.displayPathInfo[index].targetId)

        ##
        # supported_modes[] is a list of modes supported by the display
        supported_modes = self.display_config.get_all_supported_modes(displays_target_list)

        for key, values in supported_modes.items():
            # Logging Supported Mode List for each Target ID
            logging.debug("SupportedModesList:")
            for value in values:
                logging.debug("Tgt_ID:{} Hres:{} Vres:{} Rot:{} RR:{} BPP:{} Scan:{}"
                              " Scal:{} Clk:{} status:{}".format(value.targetId, value.HzRes, value.VtRes,
                                                                 value.rotation, value.refreshRate, value.BPP,
                                                                 value.scanlineOrdering, value.scaling,
                                                                 value.pixelClock_Hz,
                                                                 value.status))
            # find the middle mode between min and max resolutions
            mid = (len(supported_modes[key]) - 1) // 2

            ##
            # Sorting the resolutions list.
            values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))

            # Logging Supported Mode List for each target ID after sorting
            logging.debug("Sorted Mode List")
            for value in values:
                logging.debug("Tgt_ID:{} Hres:{} Vres:{} Rot:{} RR:{} BPP:{} Scan:{}"
                              " Scal:{} Clk:{} status:{}".format(value.targetId, value.HzRes, value.VtRes,
                                                                 value.rotation, value.refreshRate, value.BPP,
                                                                 value.scanlineOrdering, value.scaling,
                                                                 value.pixelClock_Hz,
                                                                 value.status))

            if apply_scaling is False:
                ##
                # Apply the first mode(i.e. values[0]) from the supported_modes[] which will be having the minimum resolution
                modes_flag = self.display_config.set_display_mode([values[0]])
                if modes_flag is False:
                    logging.error(
                        "[Driver Issue]: Failed to apply display mode for the current configuration. Exiting ...")
                    # Gdhm bug reporting handled in set_display_mode
                    self.fail()

                # verify DPCD after mode set
                nativeDPCDRead = True
                dpcd_length = 1

                ##
                # Read the DPCD 600h for verifying Sink detected or not
                dpcd_address = DPCD_SINK_CONTROL

                # for eDP, need not check DPCD
                if key not in self.internal_display_target_id_list:
                    self.dpcd_read(self.current_port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                   action="PLUG")

            else:
                self.set_scaling(values, values[0].HzRes, values[0].VtRes, values[0].refreshRate)

            if apply_scaling is False:
                ##
                # Apply the middle mode from the supported_modes[] which will be having the minimum resolution
                # ex: if the number of supported modes is 64, then this will apply 32nd mode
                modes_flag = self.display_config.set_display_mode([values[mid - 1]])
                if modes_flag is False:
                    logging.error(
                        "[Driver Issue]: Failed to apply display mode for the current configuration. Exiting ...")
                    # Gdhm bug reporting handled in set_display_mode
                    self.fail()

                # verify DPCD after mode set
                nativeDPCDRead = True
                dpcd_length = 1

                ##
                # Read the DPCD 600h for verifying Sink detected or not
                dpcd_address = DPCD_SINK_CONTROL

                # for eDP, need not check DPCD
                if key not in self.internal_display_target_id_list:
                    self.dpcd_read(self.current_port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                   action="PLUG")

            else:
                self.set_scaling(values, values[mid - 1].HzRes, values[mid - 1].VtRes, values[mid - 1].refreshRate)

            if apply_scaling is False:
                ##
                # Apply the last mode(i.e. values[-1]) from the supported_modes[] which will be having the maximum resolution
                modes_flag = self.display_config.set_display_mode([values[-1]])
                if modes_flag is False:
                    logging.error(
                        "[Driver Issue]: Failed to apply display mode for the current configuration. Exiting ...")
                    # Gdhm bug reporting handled in set_display_mode
                    self.fail()

                # verify DPCD after mode set
                nativeDPCDRead = True
                dpcd_length = 1

                ##
                # Read the DPCD 600h for verifying Sink detected or not
                dpcd_address = DPCD_SINK_CONTROL

                # for eDP, need not check DPCD
                if key not in self.internal_display_target_id_list:
                    self.dpcd_read(self.current_port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                   action="PLUG")

            else:
                self.set_scaling(values, values[-1].HzRes, values[-1].VtRes, values[-1].refreshRate)
        # for CLONE mode, this verify_max_supported_mode() algo is not suited
        if self.config != 'CLONE':
            self.verify_max_supported_mode()

    ##
    # @brief        This method sets default Single Display(eDP) configuration
    # @return       None
    def set_default_config(self) -> None:
        # set back to default single Config(eDP) at the end of test if present before start of the test
        if len(self.internal_display_target_id_list) != 0:
            port_type = None
            enumerated_displays = self.display_config.get_enumerated_display_info()
            logging.info(f"Enumerated displays: {enumerated_displays.to_string()}")
            logging.info(f"self.internal_display_target_id_list[0]: {self.internal_display_target_id_list[0]}")

            for index in range(enumerated_displays.Count):
                logging.info(f"Enum TargetID: {enumerated_displays.ConnectedDisplays[index].TargetID}")
                if self.internal_display_target_id_list[0] == enumerated_displays.ConnectedDisplays[index].TargetID:
                    logging.info(f"port_type: {CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)}")
                    logging.info(f"port_type: {CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name}")
                    port_type = CONNECTOR_PORT_TYPE(
                        enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
                    break
            if port_type is None:
                gdhm.report_driver_bug_di("[MST] eDP Target present before the test not found")
                self.fail("FAIL: [Test Issue] eDP Target present before the test not found")

            display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
            if isinstance(display_and_adapter_info_list, list) is False:
                display_and_adapter_info_list = [display_and_adapter_info_list]
            config = eval("enum.%s" % "SINGLE")

            modeset_status = self.display_config.set_display_configuration_ex(config, display_and_adapter_info_list)
            self.assertTrue(modeset_status, "FAIL: Failed to apply default display configuration in Teardown")

            logging.info("PASS: Default modeset successfully applied")
        else:
            logging.info("PASS: eDP not present before start of the test. Skipping default modeset")

    ##
    # @brief        This method set configuration and apply modes on all the connected displays.
    # @param[in]    set_mode: bool
    #                   if True, apply the configuration on the displays i.e. SINGLE/CLONE/EXTENDED/TRIEXTENDED/TRICLONE
    #                   and set modes.If False,apply only the configuration on the displays
    #                   i.e. SINGLE/CLONE/EXTENDED/TRIEXTENDED/TRICLONE
    # @param[in]    power_event: bool
    #                   if false, apply the configuration on the displays and set modes based on set_mode flag
    #                   if True, return the configuration name and list of port type name invloved in the configuration
    # @param[in]    apply_scaling: bool
    #                   True if scaling needs to be set else false
    # @return       None
    def set_display_config_and_modes(self, set_mode: bool, power_event: bool = False,
                                     apply_scaling: bool = False) -> None:
        # TODO:
        # some enahancements required for porting to Quad Clone/Extended when 4th Pipe gets added required for Gen11.5+
        # platforms config variables to be handled for the above cases

        ##
        # target_id_list[] is list of connector port type of the displays
        target_id_list = []

        config_data = config_data_dict[self.config]

        # Get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays is None:
            # Gdhm bug reporting handled in get_enumerated_display_info
            self.fail()

        logging.info('Enumerated displays: {}'.format(enumerated_displays.to_string()))

        if enumerated_displays.Count >= 1:
            for index in range(enumerated_displays.Count):
                target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                target_id_list.append(target_id)

            # List of Combination of Displays for All the Configuration ie SINGLE, EXTENDED, CLONE
            combination_list = display_utility.get_possible_configs(target_id_list, True)

            config_combination_list = combination_list[
                'enum.' + DisplayConfigTopology(config_data.topology).name]
            config_combination_list = list(filter(lambda config_list: len(config_list) == config_data.length,
                                                  config_combination_list))
            logging.debug(
                'Display Configuration List for Topology {} : {}'.format(self.config, config_combination_list))

            if len(config_combination_list) == 0:
                logging.error('[Test Issue]: Required Number of Displays are not enumerated')
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Displays are not enumerated as per topology({})".format(self.config),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

            if power_event:
                return config_data.topology, config_combination_list
            else:

                # Remove Display Configuration List which contains only LFP.
                new_config_combination_list = [
                    target_id_list for target_id_list in config_combination_list
                    if not set(target_id_list).issubset(self.internal_display_target_id_list)
                ]

                config_combination_list = new_config_combination_list
                logging.debug('Display Config List After Removing LFP Only Config: {}'.format(config_combination_list))

                if len(config_combination_list) == 0:
                    logging.error('[Test Issue]: Required Number of Displays are not enumerated')
                    gdhm.report_bug(
                        title="[Interfaces][DP_MST] Displays are not enumerated as per expectation",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail()

                # Set Display configuration as per the command line argument.
                set_config = DisplayConfig()
                set_config.topology = config_data.topology
                for current_config_list in config_combination_list:
                    path = 0
                    for index, target_id in enumerate(current_config_list):
                        set_config.displayPathInfo[path].targetId = target_id
                        set_config.displayPathInfo[path].displayAndAdapterInfo = enumerated_displays.ConnectedDisplays[
                            index].DisplayAndAdapterInfo
                        path += 1

                    set_config.numberOfDisplays = path
                    logging.info("Trying to Apply Display Configuration as : %s",
                                 set_config.to_string(enumerated_displays))
                    logging.info("Target ID List in the Topology: {}".format(current_config_list))

                    # Apply Display Configuration
                    self.display_config.set_display_configuration(set_config)

                    # Get Current Display Configuration
                    get_config = self.display_config.get_current_display_configuration()
                    logging.info("Current display configuration: %s", get_config.to_string(enumerated_displays))

                    # Check Applied Display Config with Current Display Config
                    if get_config.equals(set_config):
                        logging.info("Successfully applied display configuration")
                    else:
                        logging.error("[Driver Issue]: Failed to apply display configuration")
                        # Gdhm bug reporting handled in set_display_configuration
                        self.fail()

                    # Set the modes on connected displays
                    if set_mode:
                        self.set_modes(apply_scaling)

        else:
            logging.error("Not sufficient displays to apply configuration. Exiting ....")
            self.fail()

    ##
    # @brief        This method cleans up any unplugged displays remaining from previous/current test execution.
    # @return       None
    def env_cleanup(self) -> None:

        # set to default config Single eDP
        self.set_default_config()

        # create local copy of list of connected ports
        connected_port_list = list(self.cleanup_ports)
        for port in connected_port_list:
            self.set_hpd(port, False)

        logging.info("INFO: Test environment cleanup successuful")

    ##
    # @brief        This method acts as helper function to get the Display and Adpater Info list of the enumerated
    #               displays.
    # @param[in]    is_lfp_info_required: bool
    #                   Includes Display and Adapter Info of the LFP panels if set to True else only returns for EFP
    # @return       display_and_adapter_info_list[DisplayAndAdapterInfo]: list
    #                   Returns the Display And Adapter Info for the Enumerated Displays.
    @classmethod
    def get_current_display_and_adapter_info_list(cls, is_lfp_info_required=True) -> List[DisplayAndAdapterInfo]:
        display_and_adapter_info_list: List[DisplayAndAdapterInfo] = []

        enumerated_displays = cls.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for each_display in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[each_display]
            port_name = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            gfx_index = display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex

            if is_lfp_info_required is False:
                if display_utility.get_vbt_panel_type(port_name, gfx_index) not in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    display_and_adapter_info_list.append(display_info.DisplayAndAdapterInfo)
            else:
                display_and_adapter_info_list.append(display_info.DisplayAndAdapterInfo)

        return display_and_adapter_info_list

    ##
    # @brief            Verifies DPCD programming for Single Stream Sideband Message Supported Display.
    # @param[in]        display_and_adapter_info: DisplayAndAdapterInfo
    #                           Display and Adapter Information for the SST Sideband Message Supported Display.
    # @return           is_success: bool
    #                       Return True if DPCD programming is correct else False.
    @classmethod
    def verify_sst_sbm_dpcd_programming(cls, display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
        is_success = True
        port_type = CONNECTOR_PORT_TYPE(display_and_adapter_info.ConnectorNPortType).name

        # RAD information is not required as we know that single stream sideband message supported display's upstream
        # device is always source device
        status, mstm_ctrl = cls.display_port.read_dpcd(port_type, native=True, length=1, addr=MSTM_CTRL, noderad=None)
        if status is False:
            logging.error(f"DPCD Read to {MSTM_CTRL} Failed for SST SBM Msg display at {port_type}")
            is_success = False
        else:
            # Check if MST_EN bit is set to 0
            mstm_ctrl = mstm_ctrl[0]
            is_mst_enabled = mstm_ctrl & 0x1 == 0x1
            if is_mst_enabled is True:
                is_success = False
                logging.error(f"[Driver Issue] - MST Enable Bit is set for SST SBM Msg Display at {port_type}")

            # Check if UP_REQ_EN bit and UPSTREAM_IS_SRC is set to 1
            is_up_req_enabled = mstm_ctrl & 0x2 == 0x2
            if is_up_req_enabled is False:
                is_success = False
                logging.error(f"[Driver Issue] - UP_REQ_EN Bit is not set for SST SBM Msg Display at {port_type}")

            # Check UPSTREAM_IS_SRC is set to 1
            is_upstream_is_src = mstm_ctrl & 0x4 == 0x4
            if is_upstream_is_src is False:
                is_success = False
                logging.error(f"[Driver Issue] - UPSTREAM_IS_SRC is not set for SST SBM Msg Display at {port_type}")

        if is_success is False:
            logging.error("[Driver Issue] - SST Sideband Message Supported Display Verification Failed.")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] SST Sideband Message Supported Display Verification Failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        return is_success

    ##
    # @brief        This method cleans up the test
    # @param[in]    dp_port_index of the topology in cmdline
    # @return       Node rad info
    def construct_node_rad(self, dp_port_index):
        node_rad = NODE_RAD_INFO()
        node_rad.NodeRAD.TotalLinkCount = self.requested_topology_info_dict[dp_port_index].total_link_count
        rem_link_count = self.requested_topology_info_dict[dp_port_index].total_link_count - \
                         self.requested_topology_info_dict[dp_port_index].parent_branch_index
        node_rad.NodeRAD.RemainingLinkCount = rem_link_count.to_bytes(1, byteorder='big')
        reg_value_buffer_size = ctypes.c_char * 7
        reg_value: Array[c_char] = reg_value_buffer_size()
        reg_value[0] = b' '

        node_rad.NodeRAD.Address = bytes(reg_value)

        return node_rad.NodeRAD

    ##
    # @brief        This functions helps to plug the requested MST Display.
    # @param[in]    port_type DP_B/DP_C etc.
    # @param[in]    topology_type SST/MST
    # @param[in]    xml_file Topology xml to plug
    # @return       None
    def plug_mst_display(self, port_type: str, topology_type: str, xml_file: str) -> None:

        logging.info(f"Plugging MST Display in {port_type}")

        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type)

        # Parse and Send Topology details to Gfx Sim driver from user
        self.parse_send_topology(port_type, topology_type, xml_file)

        # Connect DP 1.2 display(s) by issuing HPD
        self.set_hpd(port_type, True)

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Adding additional 20 second delay for pre-si environments to make simulation data reflect in driver
        is_pre_si_environment = self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                         "SIMENV_PIPE2D"]

        if is_pre_si_environment:
            time.sleep(20)

    ##
    # @brief        This method cleans up the test
    # @return       None
    def tearDown(self) -> None:
        logging.info("In tearDown()")

        status = self.display_port.uninitialize_sdk()
        if status is True:
            logging.info("Un-initialization of CUI SDK Successful in TearDown().")
        else:
            logging.error("Un-initialization of CUI SDK Failed in TearDown().")

        self.env_cleanup()

        logging.info("Test Clean Up Completed")


if __name__ == '__main__':
    unittest.main()
