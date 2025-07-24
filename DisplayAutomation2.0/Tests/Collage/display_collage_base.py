######################################################################################
# @file         display_collage_base.py
# @brief        This file contains DisplayCollageBase class which needs to be inherited by all the Collage Legacy tests
# @details      It contains setUp and tearDown methods of unittest framework. In setUp, we parse command_line arguments
#               and then runTest() in the test script gets executed In tearDown, Test clean up will take place.
#
# @author       Praveen Bademi
######################################################################################
import copy
import ctypes
import logging
import os
import sys
import time
import unittest
from typing import Optional, List, Any

from Libs.Core import cmd_parser, display_utility
from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayConfig
from Libs.Core.display_power import DisplayPower
from Libs.Core.sw_sim.dp_mst import DisplayPort, TOPOLOGY_STATUS_CODE
from Libs.Core.sw_sim.gfxvalsim import GfxValSim
from Libs.Core.test_env.test_context import TestContext
from Libs.Feature import display_collage
from Libs.Feature.display_collage import IGFX_SYSTEM_CONFIG_DATA_N_VIEW, IGFX_TEST_CONFIG_EX

# delays are given in Milli Seconds
DPCD_SINK_CONTROL = 0x600
DPCD_VERSION_OFFSET = 0x0
DP_HOTPLUG_GOLDEN_VALUE = 0x00000001
DPCD_VERSION_11 = 0x11
# delays are given in Milli Seconds
DELAY_5000_MILLISECONDS = 5000
DELAY_1000_MILLISECONDS = 1000.0
GFXSIM_DISPLAY_TOPOLOGIES_MATCHING = 0
GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT = 4
RESUME_TIME = 60
INTERNAL_DISPLAY = 265988


##
# @brief        A class which has to be inherited by all the Collage test cases and contains setUp and tearDown methods
#               to set the environment required for the Collage test case and reset the environment after the test case
#               completes respectively.
class DisplayCollageBase(unittest.TestCase):
    # initialise the command line arguments to None
    cmd_args = None
    # If we want to verify DP MST on 4 port simultaneously then custom_tags needs to be updated with tp4
    my_custom_tags = ['-TP1', '-XML1', '-TP2', '-XML2', '-TP3', '-XML3', '-COLMODE', '-NP']
    # Create list for XML file
    xmlPath = ['-', '-', '-', '-', '-']
    # Create list for topology types
    topology = ['-', '-', '-', '-', '-']
    # initialise the command line arguments to None 
    number_of_ports = None
    # Variables to keep track number of displays before and after test
    number_of_displays_before_test = None
    number_of_displays_after_test = None
    # create list for DP Port Type required during cleanup
    cleanup_ports = []

    ##
    # @brief        setUp() initialises the object and process the cmd line parameters.
    # @return       None
    def setUp(self) -> None:
        # try except has been added to invoke teardown even if any failure happens in setup phase.
        try:
            ##
            # Create DisplayPort object
            self.display_port = DisplayPort()
            ##
            # Create DisplayPower object
            self.display_power = DisplayPower()
            ##
            # Create Collage object
            self.collage = display_collage.Collage()
            ##
            # Create DisplayPower object
            self.display_power = DisplayPower()
            ##
            # Create DisplayConfiguration object
            self.display_config = DisplayConfiguration()

            # GfxValSim initialization required
            self.valsim_handle = GfxValSim()

            # process the command line arguments
            self.process_cmdline()

            # number of displays before the test starts
            enumerated_displays = self.display_config.get_enumerated_display_info()
            self.number_of_displays_before_test = enumerated_displays.Count
        except Exception as e:
            logging.error("Unexpected Exception occurred...Exiting...")
            self.tearDown()
            self.fail(e)

    ##
    # @brief        process_cmdline() processes the cmdline parameters.
    # @return       None
    def process_cmdline(self) -> None:
        self.cmd_args = sys.argv
        self.cmd_dict = cmd_parser.parse_cmdline(self.cmd_args, self.my_custom_tags)
        self.config = self.cmd_dict['CONFIG']

        # Loop through the dictionary
        # find the number of topologies from the command line
        # find the Topology Type from command line
        # create a list of Topology Types and XML Files ie topology and xmlPath resp
        for key, value in self.cmd_dict.items():
            if key in ['TP1', 'TP2', 'TP3']:
                if value != 'NONE':
                    # find the index of TP1,TP2,TP3 etc from my_custom_tags
                    # divide it by 2 to find the insert position(index) in topology list
                    # below is the mapping of indices between topology list and my_custom_tags
                    #       index(my_custom_tags)   index(topology)
                    # TP1           0                        0
                    # TP2           2                        1
                    # TP3           4                        2 and so on
                    insert_pos = self.my_custom_tags.index('-' + key) // 2
                    dp_type_value = value[0]
                    self.topology[insert_pos] = dp_type_value

            # save the xml file path from command line
            elif key in ['XML1', 'XML2', 'XML3']:
                if value != 'NONE':
                    # find the index of XML1,XML2,XML3 etc from my_custom_tags
                    # divide it by 2 to find the insert position(index) in xmlPath list
                    # below is the mapping of indices between xmlPath list and my_custom_tags
                    #       index(my_custom_tags)   index(xmlPath)
                    # XML1           1                        0
                    # XML2           3                        1
                    # XML3           5                        2 and so on
                    insert_pos = self.my_custom_tags.index('-' + key) // 2
                    xml = value[0]
                    self.xmlPath[insert_pos] = os.path.join(TestContext.panel_input_data(), "DP_MST_TILE", xml)

            # for Horizontal or Vertical Collage flags
            elif key == 'COLMODE':
                self.collagemode = value[0]

            # Number of ports to which displays are connected
            elif key == 'NP':
                self.number_of_ports = int(value[0])

    ##
    # @brief        get_number_of_ports() returns number of ports to which display connected
    # @return       number_of_ports: int
    #                   Returns the Number of ports
    def get_number_of_ports(self) -> int:
        return self.number_of_ports

    ##
    # @brief        get_topology_type() returns topology type which could be either SST or MST or HDMI
    # @param[in]    index: int
    #                   Represents the position of the topology in the command line
    # @return       topology: str
    #                   Returns the topology name based on the index position.
    def get_topology_type(self, index: int) -> str:
        return self.topology[index]

    ##
    # @brief        get_xmlfile() returns xml file name
    # @param[in]    index: int
    #                   Represents the position of the xml file path in the command line
    # @return       xmlPath: str
    #                   Returns the xml file path based on the index position
    def get_xmlfile(self, index: int) -> str:
        return self.xmlPath[index]

    ##
    # @brief        get_dp_port_from_availablelist() returns port type for the index
    # @param[in]    index: int
    #                   Represents the position of the dp port in the command line
    # @return       Returns the port type from the free dp port list for the specified index
    def get_dp_port_from_availablelist(self, index: int) -> str:
        return self.display_port.get_free_dp_port_type(index)

    ##
    # @brief        get_number_of_free_dp_ports() returns number of free DP ports
    # @return       Returns the number of free dp ports
    def get_number_of_free_dp_ports(self) -> int:
        return self.display_port.get_number_of_free_dp_ports()

    ## 
    # @brief        setnverifydp() function call is used to build a DP MST/SST Topology
    # @param[in]    port_type: str
    #                   Port name in which the topology has to be plugged
    # @param[in]    topology_type: str
    #                   Name of the topology like SST, MST
    # @param[in]    xml_file: str
    #                   XML File path for the topology
    # @param[in]    lowpower: Optional[bool]
    #                   True indicates plug has to be done in lowpower, False for normal plug
    # @return       None
    def setnverifydp(self, port_type: str, topology_type: str, xml_file: str, lowpower: Optional[bool] = False) -> None:
        retstatus = self.display_port.setdp(port_type, topology_type, xml_file, lowpower)
        if retstatus:
            logging.info("HotPlug Event to the Display Port is successfull")
        else:
            logging.error("HotPlug Event to the Display Port is failed")
            self.fail()

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        self.cleanup_ports.append(port_type)

        ##
        # Read the DPCD 600h & check the HPD status
        #
        nativeDPCDRead = True
        dpcd_length = 1

        if topology_type == 'MST':
            # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP
            # topology page
            self.verifytopology(port_type)

            ##
            # Read the DPCD 600h for verifying Sink detected or not
            dpcd_address = DPCD_SINK_CONTROL

            # DPCD Read API is failing from driver side and hence we have commented for now
            self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None, action="PLUG")
        else:
            ##
            # Read the DPCD 00h for verifying Version of Panel
            dpcd_address = DPCD_VERSION_OFFSET

            version_reg_value = self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                               action="VERSION")
            if version_reg_value == DPCD_VERSION_11:
                logging.info("The Connected Display is a SST Display")
            else:
                logging.error("The Connected Display is not a SST Display")
                self.fail()

    ##
    # @brief        Exposed API to verify topology between CUI and Driver
    # @param[in]    port_type: str
    #                   Port name in which the topology has to be plugged
    # @param[in]    action: str
    #                   Action tells whether to verify the topology after plug or unplug
    # @return       None
    def verifytopology(self, port_type: str, action: Optional[str] = "PLUG") -> None:
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("Invalid plug action for display. Exiting .....")
            self.fail()
        retStatus = self.display_port.verify_topology(port_type)
        if action == 'PLUG' and retStatus == GFXSIM_DISPLAY_TOPOLOGIES_MATCHING:
            logging.info("MST Topology Verification Success, Applied and Expected topologies are matching")
        elif action == 'UNPLUG' and retStatus == GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT:
            logging.info("MST Topology Verification Success: HPD(UNPLUG) event")
        else:
            try:
                logging.error(
                    "MST Topology Verification Failed.. Status Code:%s" % TOPOLOGY_STATUS_CODE(retStatus).name)
                self.fail()
            except ValueError as Error:
                logging.error("MST Topology Verification Failed.. No Matching Status Code Fund...%s" % Error)
                self.fail()

    ##
    # @brief        Exposed API to Read DPCD from the offset
    # @param[in]    port_type: str
    #                   Port name in which the topology has to be plugged
    # @param[in]    nativeDPCDRead: bool
    #                   Indicates if its a native dpcd read or remote dpcd read
    # @param[in]    length: int
    #                   Length of the data that has to be read
    # @param[in]    addr: int
    #                   Offset from which the data has to be read
    # @param[in]    node_rad: Any
    #                   Node rad indicates the path of the downstream displays
    # @param[in]    action: str
    #                   Indicates action type for which DPCD read happens.
    # @return       Returns dpcd_reg_val if the action is "VERSION"
    def dpcd_read(self, port_type: str, nativeDPCDRead: bool, length: int, addr: int, node_rad: Any,
                  action: Optional[str] = "PLUG") -> int:
        action = action.upper()
        if action not in ['PLUG', 'VERSION']:
            logging.error("Invalid plug action for display. Exiting .....")
            self.fail()
        dpcd_flag, dpcd_reg_val = self.display_port.read_dpcd(port_type, nativeDPCDRead, length, addr, node_rad)

        if action == 'PLUG' and dpcd_flag:
            logging.info("DPCD Read Value: %s" % (dpcd_reg_val[0]))
            reg_val = dpcd_reg_val[0] & 0x000000FF
            if reg_val == DP_HOTPLUG_GOLDEN_VALUE:
                logging.info("DPCD read successful for Hotplug: Register Value: %s" % reg_val)
            else:
                logging.error("DPCD Flag:%s & Register value:%s during DPCD Read Failure" % (dpcd_flag, reg_val))
                logging.error("DPCD read failed for Hotplug . Exiting ...")
                self.fail()

        elif action == 'VERSION' and dpcd_flag:
            logging.info("DPCD Version Value: %x" % (dpcd_reg_val[0]))
            return dpcd_reg_val[0]

        else:
            logging.error("Read DPCD api Failed, Exiting ...")
            self.fail()

    ##
    # @brief        Exposed API to verify set the Hot Plug Event Notification
    # @param[in]    port_type: str
    #                   Port Name to which the display has to be plugged or unplugged
    # @param[in]    attach_detach: bool
    #                   True if display has to be attached, False to detach
    # @return       None
    def set_hpd(self, port_type: str, attach_detach: bool) -> None:
        retStatus = self.display_port.set_hpd(port_type, attach_detach)
        if retStatus:
            if attach_detach:
                logging.info("Simulation driver issued HPD (Hotplug Interrupt) to Graphics driver successfully")
                self.cleanup_ports.append(port_type)
            else:
                logging.info("Simulation driver issued HPD (Hotunplug Interrupt) to Graphics driver successfully")
                self.cleanup_ports.remove(port_type)
        else:
            logging.error("Simulation driver failed to issue HPD to Graphics driver")
            self.fail()

    ##
    # @brief        Exposed API to get the collage feature support information
    # @return       None.
    def get_collage_info(self) -> None:
        retStatus = self.collage.get_collage_info()
        if retStatus:
            logging.info("Collage Information retrieval is successfully")
        else:
            logging.error("Collage Information retrieval failed")
            self.fail()

    ##
    # @brief        Exposed API to verify if collage is enabled
    # @return       None.
    def is_collage_enabled(self) -> None:
        retStatus = self.collage.is_collage_enabled()
        if retStatus:
            logging.info("Collage Mode is Enabled")
        else:
            logging.info("Collage Mode is not enabled")
            self.fail()

    ##
    # @brief        Exposed API to verify if collage is disabled
    # @return       None.
    def is_collage_disabled(self) -> None:
        retStatus = self.collage.is_collage_enabled()
        print(retStatus)
        if retStatus is not True:
            logging.info("Collage Mode is Disabled")
        else:
            logging.info("Collage Mode is not disabled")
            self.fail()

    ##
    # @brief        Exposed API to apply collage mode
    # @param[in]    supported_config: IGFX_TEST_CONFIG_EX
    #                   Contains information about the displays for which collage will be applied.
    # @param[in]    mode_set: bool
    #                   True to try different mode set for collage, False otherwise
    # @return       None.
    def apply_collage_mode(self, supported_config: IGFX_TEST_CONFIG_EX, mode_set: Optional[bool] = False) -> None:
        # check is it Horizontal/vertical collage
        if self.collagemode == 'HOR':
            is_horizantal = True
        else:
            is_horizantal = False

        # get the number of connected displays excluding eDP
        enumerated_displays = self.display_config.get_enumerated_display_info()
        num_displays = enumerated_displays.Count
        internal_display_list = self.display_config.get_internal_display_list(enumerated_displays)
        if len(internal_display_list) != 0:
            num_displays = num_displays - len(internal_display_list)
        logging.info("Number of Displays Connected: %s" % num_displays)

        # currently collage is supported with 2 or 3 displays
        # if number of displays is more than 3, collage will be set with 3 displays
        # minimum2 displays are needed to apply collage
        if num_displays < 2:
            logging.error("Not enough display connected to apply Collage Mode")
            self.fail()
        elif num_displays >= 4:
            num_displays = 3
        else:
            num_displays = 2

        found = None
        # create a structure type of IGFX_SYSTEM_CONFIG_DATA_N_VIEW
        system_config_ex_data = display_collage.IGFX_SYSTEM_CONFIG_DATA_N_VIEW()
        # size  of the structure IGFX_SYSTEM_CONFIG_DATA_N_VIEW with a pointer to IGFX_DISPLAY_CONFIG_DATA_EX
        system_config_view_data_size = (ctypes.sizeof(ctypes.c_ulong) * 2) + (
                ctypes.sizeof(ctypes.c_uint) * 2) + ctypes.sizeof(display_collage.IGFX_DISPLAY_CONFIG_DATA_EX)
        # totoal input/output buffer size
        uiSize = system_config_view_data_size + (
                ctypes.sizeof(display_collage.IGFX_DISPLAY_CONFIG_DATA_EX) * (num_displays - 1))

        # out of all the supported configs ie Singledisplay,DDC,Tri Clone, Tri ED etc, filter out only Collage configs
        # populate the IGFX_SYSTEM_CONFIG_DATA_N_VIEW structure with device ids of connected displays and operating mode
        for index in range(supported_config.dwNumTotalCfg):
            system_config_ex_data.DispCfg[0].dwDisplayUID = supported_config.ConfigList[index].dwPriDevUID
            # check for DUAL HOR COLLAGE
            if is_horizantal is True and num_displays == 2 \
                    and (supported_config.ConfigList[
                             index].dwOperatingMode == display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE):
                system_config_ex_data.DispCfg[1].dwDisplayUID = supported_config.ConfigList[index].dwSecDevUID
                system_config_ex_data.dwOpMode = display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE
                found = True
                logging.info(
                    "Collage Mode: Dual Horizontal  VID: %s %s" % (system_config_ex_data.DispCfg[0].dwDisplayUID,
                                                                   system_config_ex_data.DispCfg[1].dwDisplayUID))

            # check for TRI HOR COLLAGE
            elif is_horizantal is True and num_displays == 3 \
                    and (supported_config.ConfigList[
                             index].dwOperatingMode == display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE):
                system_config_ex_data.DispCfg[1].dwDisplayUID = supported_config.ConfigList[index].dwSecDevUID
                system_config_ex_data.DispCfg[2].dwDisplayUID = supported_config.ConfigList[index].dwThirdDevUID
                system_config_ex_data.dwOpMode = display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE
                found = True
                logging.info(
                    "Collage Mode: Tri Horizontal  VID: %s %s %s" % (system_config_ex_data.DispCfg[0].dwDisplayUID,
                                                                     system_config_ex_data.DispCfg[1].dwDisplayUID,
                                                                     system_config_ex_data.DispCfg[2].dwDisplayUID))

            # check for DUAL VER COLLAGE
            elif is_horizantal is not True and num_displays == 2 \
                    and (supported_config.ConfigList[
                             index].dwOperatingMode == display_collage.GFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE):
                system_config_ex_data.DispCfg[1].dwDisplayUID = supported_config.ConfigList[index].dwSecDevUID
                system_config_ex_data.dwOpMode = display_collage.GFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE
                found = True
                logging.info("Collage Mode: Dual Vertical  VID: %s %s" % (system_config_ex_data.DispCfg[0].dwDisplayUID,
                                                                          system_config_ex_data.DispCfg[
                                                                              1].dwDisplayUID))

            # check for TRI HOR COLLAGE
            elif is_horizantal is not True and num_displays == 3 \
                    and (supported_config.ConfigList[
                             index].dwOperatingMode == display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE):
                system_config_ex_data.DispCfg[1].dwDisplayUID = supported_config.ConfigList[index].dwSecDevUID
                system_config_ex_data.DispCfg[2].dwDisplayUID = supported_config.ConfigList[index].dwThirdDevUID
                system_config_ex_data.dwOpMode = display_collage.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE
                found = True
                logging.info(
                    "Collage Mode: Tri Vertical  VID: %s %s %s" % (system_config_ex_data.DispCfg[0].dwDisplayUID,
                                                                   system_config_ex_data.DispCfg[1].dwDisplayUID,
                                                                   system_config_ex_data.DispCfg[2].dwDisplayUID))

            # once a collage config is found, apply the collage mode
            # set the number of displays, size propoerly
            if found:
                found = False
                system_config_ex_data.uiSize = uiSize

                system_config_ex_data.dwFlags = 0
                system_config_ex_data.uiNDisplays = num_displays

                retStatus = self.collage.apply_collage_mode(system_config_ex_data)
                if retStatus:
                    logging.info("Collage Mode is applied successfully")
                    # Function call to check if Collage is applied
                    self.is_collage_enabled()
                else:
                    logging.error("Apply Collage Mode failed")
                    self.fail()

                # Wait for the simulation driver to reflect the MST connection status in CUI
                time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

                # If mode needs not be applied, set collage with default config
                if mode_set is True:
                    self.mode_set_collage(system_config_ex_data, num_displays)

    ##
    # @brief        Exposed API to verify set the modes for collage.
    # @param[in]    system_config_ex_data: IGFX_SYSTEM_CONFIG_DATA_N_VIEW
    #                   Contains all the information of the display to get/set the modes for collage.
    # @param[in]    num_displays: int
    #                   Number of displays that are part of collage.
    # @return       None.
    def mode_set_collage(self, system_config_ex_data: IGFX_SYSTEM_CONFIG_DATA_N_VIEW, num_displays: int) -> None:
        # create local copy of system_config_ex_data for Min Mode
        system_config_ex_data_min = copy.deepcopy(system_config_ex_data)
        # create local copy of system_config_ex_data for Random(middle) Mode
        system_config_ex_data_mid = copy.deepcopy(system_config_ex_data)

        for display_index in range(num_displays):
            # get all the supported for the targeted device id
            retStatus, mode_list = self.collage.get_supported_modes_collage(system_config_ex_data, display_index)
            if retStatus:
                logging.info("All the supported Modes for applied Collage retirieved successfully")
            else:
                logging.info("The supported Modes for applied Collage retirieval failed")
                self.fail()

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

            # fill the IGFX_SYSTEM_CONFIG_DATA_N_VIEW structure with max resolution for the targeted device id's
            system_config_ex_data.DispCfg[display_index].Resolution.dwHzRes = mode_list.vmlModes[
                mode_list.vmlNumModes - 1].dwHzRes
            system_config_ex_data.DispCfg[display_index].Resolution.dwVtRes = mode_list.vmlModes[
                mode_list.vmlNumModes - 1].dwVtRes
            system_config_ex_data.DispCfg[display_index].Resolution.dwRR = mode_list.vmlModes[
                mode_list.vmlNumModes - 1].dwRR

            # fill the IGFX_SYSTEM_CONFIG_DATA_N_VIEW structure with min resolution for the targeted device id's
            system_config_ex_data_min.DispCfg[display_index].Resolution.dwHzRes = mode_list.vmlModes[0].dwHzRes
            system_config_ex_data_min.DispCfg[display_index].Resolution.dwVtRes = mode_list.vmlModes[0].dwVtRes
            system_config_ex_data_min.DispCfg[display_index].Resolution.dwRR = mode_list.vmlModes[0].dwRR

            # fill the IGFX_SYSTEM_CONFIG_DATA_N_VIEW structure with random resolution for the targeted device id's
            # random mode is min + max / 2
            mid = mode_list.vmlNumModes // 2
            system_config_ex_data_mid.DispCfg[display_index].Resolution.dwHzRes = mode_list.vmlModes[mid].dwHzRes
            system_config_ex_data_mid.DispCfg[display_index].Resolution.dwVtRes = mode_list.vmlModes[mid].dwVtRes
            system_config_ex_data_mid.DispCfg[display_index].Resolution.dwRR = mode_list.vmlModes[mid].dwRR

        # currently applying only Max mode
        retStatus = self.collage.apply_collage_mode(system_config_ex_data)
        if retStatus:
            logging.info("Collage Mode is applied successfully with Max Resolution %sx%s@%s"
                         % (system_config_ex_data.DispCfg[0].Resolution.dwHzRes,
                            system_config_ex_data.DispCfg[0].Resolution.dwVtRes,
                            system_config_ex_data.DispCfg[0].Resolution.dwRR))
            # Function call to check if Collage is applied
            self.is_collage_enabled()
        else:
            logging.error("Apply Collage Mode failed for Max Resolution")
            self.fail()

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # currently applying only Min mode
        retStatus = self.collage.apply_collage_mode(system_config_ex_data_min)
        if retStatus:
            logging.info("Collage Mode is applied successfully with Min Resolution %sx%s@%s"
                         % (system_config_ex_data_min.DispCfg[0].Resolution.dwHzRes,
                            system_config_ex_data_min.DispCfg[0].Resolution.dwVtRes,
                            system_config_ex_data_min.DispCfg[0].Resolution.dwRR))
            # Function call to check if Collage is applied
            self.is_collage_enabled()
        else:
            logging.error("Apply Collage Mode failed for Min Resolution")
            self.fail()

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # currently applying only Random mode
        retStatus = self.collage.apply_collage_mode(system_config_ex_data_mid)
        if retStatus:
            logging.info("Collage Mode is applied successfully with Random Resolution %sx%s@%s"
                         % (system_config_ex_data_mid.DispCfg[0].Resolution.dwHzRes,
                            system_config_ex_data_mid.DispCfg[0].Resolution.dwVtRes,
                            system_config_ex_data_mid.DispCfg[0].Resolution.dwRR))
            # Function call to check if Collage is applied
            self.is_collage_enabled()
        else:
            logging.error("Apply Collage Mode failed for Mid Resolution")
            self.fail()

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

    ##
    # @brief        Exposed API to get the all supported configs Singledisplay,DDC,Tri Clone, Tri ED, Dual/Tri Collage
    #               for Hor and Vertical
    # @return       config_ex: IGFX_TEST_CONFIG_EX
    #                   Returns the supported config else fails the test case.
    def get_supported_config(self) -> IGFX_TEST_CONFIG_EX:
        retStatus, config_ex = self.collage.get_supported_config()
        if retStatus:
            logging.info("All the supported Configs retrieved successfully")
            return config_ex
        else:
            logging.info("Supported Configs retrieval failed")
            self.fail()

    ##
    # @brief        Exposed API to verify is it a single enclosure
    # @param[in]    port_type: str
    #                   Port name for which the display is plugged
    # @return       True if its a single close, False otherwise
    def is_single_enclosure(self, port_type: str) -> bool:
        found = False
        # Get the enumerated displays
        enumerated_displays = self.display_config.get_enumerated_display_info()

        # the core logic here is for single enclosures, Horizontal resolution will be less than vertical resolution
        # find the active number of DP displays and thier target ids
        for index in range(enumerated_displays.Count):
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            enum_port_type = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name

            if enum_port_type == port_type and enumerated_displays.ConnectedDisplays[index].IsActive:
                # Get the native mode from EDID file
                native_mode = self.display_config.get_native_mode(target_id)
                if native_mode is None:
                    logging.error(f"Failed to get native mode for {target_id}")
                    self.fail()
                native_xres = native_mode.hActive
                native_yres = native_mode.vActive
                if native_xres < native_yres:
                    logging.info("It's EIZO Panel with resolution: %s x %s" % (native_xres, native_yres))
                    return True
                else:
                    logging.info("It's Normal(Non-EIZO) Panel with resolution: %s x %s" % (native_xres, native_yres))
                    return False
        if found is not True:
            logging.error("Connected Port type not found: %s... Exiting" % port_type)
            self.fail()

    ##
    # @brief        Setting Power Events- S3, S4, CS, S5
    # @param[in]    power_state: enum
    #                   Power State to be invoked
    # @param[in]    resume_time: int
    #                   It is the time the system has to wait before resuming from the power state
    # @return       None.
    def power_event(self, power_state: enum, resume_time: int) -> None:
        if self.display_power.invoke_power_event(power_state, resume_time):
            time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)
        else:
            self.fail("Entry or Exit from %s power event Failed. Exiting ....." % power_state.name)

    ##
    # @brief        switching Display Config between Collage Displays
    # @return       None.
    def set_display_config(self) -> None:
        # TODO:
        # some enahancements required for porting to Quad Clone/Extended when 4th Pipe gets added required for Gen11.5+
        # platforms. config variables to be handled for the above cases

        ##
        # target_id_list[] is list of connector port type of the displays
        target_id_list = []
        ##
        # tri_config_comb_list[] is list of connector port
        # types for applying TriExtended/TriClone config
        tri_config_comb_list = []
        ##
        # dual_config_comb_list[] is list of connector port
        # types for applying Extended/Clone config
        dual_config_comb_list = []
        display_config = None
        config_combination_list = None

        # configuration to be applied ie SINGLE/CLONE/EXTENDED/TRIEXTENDED/TRICLONE
        config = self.config

        # TODO:
        # config variables to be handled for the Quad Clone/Extended cases
        if config == 'TRICLONE':
            disp_config = 'CLONE'
            ##
            # Get display topology to be applied on connected display
            display_config = eval("enum.%s" % disp_config)
        elif config == 'TRIEXTENDED':
            disp_config = 'EXTENDED'
            ##
            # Get display topology to be applied on connected display
            display_config = eval("enum.%s" % disp_config)
        elif config == 'SINGLE' or config == 'EXTENDED' or config == 'CLONE':
            ##
            # Get display topology to be applied on connected display
            display_config = eval("enum.%s" % config)
        ##
        # Get the enumerated displays
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays.Count >= 1:
            for index in range(enumerated_displays.Count):
                target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                # exclude the eDP
                # if target_id == INTERNAL_DISPLAY:
                #    continue                    
                target_id_list.append(target_id)

            ##
            # combination_list[] is a list of combination of displays for all the configuration ie SINGLE, EXTENDED,
            # CLONE
            if config == 'SINGLE':
                combination_list = display_utility.get_possible_configs(target_id_list, True)
            else:
                combination_list = display_utility.get_possible_configs(target_id_list)

            # TODO:
            # config variables to be handled for the Quad Clone/Extended cases

            ##
            # If config is 'SINGLE',combination_list[] will have single port types
            # eg. [['DP_A'], ['DP_B']...]
            if config == 'SINGLE':
                # get the list of SINGLE displays
                # currently for SINGLE configuration is applied for eDP also
                # in future if we decide not to apply SINGLE config for eDP
                # we need to remove eDP ie ['DP_A'] from config_combination_list
                config_combination_list = combination_list['enum.SINGLE']
            ##
            # If config is 'EXTENDED'/'CLONE',combination_list[] will have combination of port types
            # eg. [['DP_A', 'DP_B'], ['DP_B', 'DP_A']...]
            elif config == 'EXTENDED' or config == 'CLONE':
                # get the list of EXTENDED displays
                config_combination_list = combination_list['enum.' + config]
                for comb_list in config_combination_list:
                    if len(comb_list) == 2:
                        dual_config_comb_list.append(comb_list)
                        config_combination_list = dual_config_comb_list
            ##
            # If config is 'TRIEXTENDED'/'TRICLONE',combination_list[] will have combination of port types
            # eg. [['DP_A', 'DP_B','DP_C'], ['DP_C', 'DP_B', 'DP_A']...]
            elif config == 'TRIEXTENDED':
                config_combination_list = combination_list['enum.EXTENDED']
                for comb_list in config_combination_list:
                    if len(comb_list) == 3:
                        tri_config_comb_list.append(comb_list)
                        config_combination_list = tri_config_comb_list
            elif config == 'TRICLONE':
                config_combination_list = combination_list['enum.CLONE']
                for comb_list in config_combination_list:
                    if len(comb_list) == 3:
                        tri_config_comb_list.append(comb_list)
                        config_combination_list = tri_config_comb_list

            ##
            # Set display configuration according to the config
            ##
            # Prepare display configuration object
            set_config = DisplayConfig()
            set_config.topology = display_config
            for current_config_list in range(len(config_combination_list)):
                targetId = config_combination_list[current_config_list]
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
                    logging.error("Failed to apply display configuration")
                    self.fail()

    ##
    # @brief        env_cleanup() cleans up any unplugged displays remaining from previous/current test execution.
    # @return       True if environment cleanup is successful/False if failed.
    def env_cleanup(self) -> bool:
        # create local copy of list of connected ports
        connected_port_list = list(self.cleanup_ports)
        for port in connected_port_list:
            self.set_hpd(port, False)

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # number of displays after the test compltes
        enumerated_displays = self.display_config.get_enumerated_display_info()
        # compare number of display before and after test
        # both should match if cleanup is successful
        self.number_of_displays_after_test = enumerated_displays.Count
        if self.number_of_displays_after_test == self.number_of_displays_before_test:
            return True
        else:
            logging.error("Number of Displays after test %s and before test %s"
                          % (self.number_of_displays_after_test, self.number_of_displays_before_test))
            return False

    ##
    # @brief        Gets all the dp ports from the command line
    # @return       port_list: List[str]
    #                   List of dp port names from the command line.
    def get_dp_ports_to_plug(self) -> List[str]:
        port_list = []

        for key, value in self.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None and key.startswith('DP_'):
                port_list.append(key)

        return port_list

    ##
    # @brief        Cleans up the test
    # @return       None
    def tearDown(self) -> None:
        logging.info("In tearDown()")
        status = self.display_port.uninitialize_sdk()
        if status is True:
            logging.info("Uninitialization of CUI SDK Successful in TearDown().")
        else:
            logging.error("Uninitialization of CUI SDK Failed in TearDown().")
        env_flag = self.env_cleanup()
        if env_flag:
            logging.info("Environment CleanUp Successful in TearDown().")
        else:
            logging.error("Environment CleanUp Failed in TearDown().Exiting ...")
            self.fail()

        logging.info("Test Clean Up Completed")


if __name__ == '__main__':
    unittest.main()
