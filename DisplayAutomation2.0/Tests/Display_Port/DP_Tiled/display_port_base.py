#######################################################################################################################
# @file         display_port_base.py
# @brief        This file contains DP_Tiled base class which should be inherited by all Tiled related tests.
# @details      display_port_base.py contains DisplayPortBase class which implements setUp method to setup the
#               environment required for all the Tiled test cases and tearDown method to reset the environment by
#               unplugging the displays, un-initialize sdk etc.
#               Also contains some helper methods and variables that are required for the Tiled test cases.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru
#######################################################################################################################

import logging
import re
import sys
import time
import unittest
from operator import attrgetter
from random import randint
from typing import List, Dict, Any

import win32api

from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum  # Do not remove this import as it will used by eval function to evaluate config enums
from Libs.Core import reboot_helper
from Libs.Core import window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import TARGET_ID
from Libs.Core.display_power import DisplayPower
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.sw_sim.dp_mst import DisplayPort, TargetIDsOfTiles
from Libs.Core.system_utility import SystemUtility
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from registers.mmioregister import MMIORegister

##
# Regular expressions to parse keys in the Output dictionary
# E.g.: EDP_A, EDP_F, DP_B, etc
DP_pattern = re.compile('DP_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))
HDMI_pattern = re.compile('HDMI_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))
EDP_pattern = re.compile('EDP_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))
MIPI_pattern = re.compile('MIPI_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))

Cursor_A_Register = 0x70800
Cursor_B_Register = 0x71080
Cursor_C_Register = 0x72080
Cursor_D_Register = 0x73080
Delay_5_Secs = 5
Delay_After_Power_Event = 10
Resume_Time = 60
CRC_PATTERN_MATCH_LENGTH = 6

target_ids_of_tiles = TargetIDsOfTiles()


##
# @brief        A class which has to be inherited by all the Tiled test cases and contains some class methods, test
#               methods to set the environment required for the Tiled test case to run and also contains helper methods
#               which is used across Tiled test cases.
class DisplayPortBase(unittest.TestCase):
    ##
    # initialise the command line arguments to None
    cmd_args = None
    cmd_list = []
    cmd_line_displays = []
    plug_val = None

    # below variables hold values from 0 to n adapters present,
    # e.g.[adapter0[{panel1}, {panel2}..], adapter1[[{panel1}, {panel2}..]..]
    ma_dp_panels: List[List[Dict[str, Any]]] = []
    ma_hdmi_panels: List[List[Dict[str, Any]]] = []
    ma_edp_panels: List[List[Dict[str, Any]]] = []
    ma_mipi_panels: List[List[Dict[str, Any]]] = []

    ##
    # List of DDIs/Ports
    dp_ports_list = []
    ##
    # Non-tiled panels (DP, HDMI, eDP & MIPI) list
    other_panel_count = None
    non_tile_target_list = []
    tile_target_list = []
    target_id_tiled = None
    under_run_status = UnderRunStatus()
    primary_display = None
    secondary_display = None
    bpc = None
    ma_flag = False
    platform_list = []
    adapter_list_to_verify = []
    ##
    # Create DisplayConfiguration object
    display_config = DisplayConfiguration()
    # Create DisplayPort object
    display_port = DisplayPort()
    ##
    # valid_edid_list[] is a list of valid edid names that can be given as input through the cmd
    valid_edid_list = ['DELL_U2715_M.EDID', 'DELL_U2715_S.EDID', 'DELL_U2715_M1.EDID', 'DELL_U2715_S1.EDID',
                       'DELL_U3218_M.bin', 'DELL_U3218_S.bin', 'DELL_U3218_M1.bin', 'DELL_U3218_S1.bin',
                       'DELL_U3218_M_VRR.bin', 'DELL_U3218_S_VRR.bin', 'DELL_U2715_M_DID2.bin', 'DELL_U2715_S_DID2.bin']
    ##
    # valid_dpcd_list[] is a list of valid dpcd that can be given as input through the cmd
    valid_dpcd_list = ['DELL_U2715_DPCD.bin', 'DELL_U3218_DPCD.bin', 'DELL_U3218_DPCD_VRR.bin', 'UHBR10_LC2_SST_DPCD.bin']

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any Tiled test case.
    #               It initialises the object and process the cmd line parameters.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        ##
        # try except has been added to invoke teardown even if any failure happens in setup phase.
        try:
            ##
            # Create SystemUtility object
            self.system_utility = SystemUtility()
            ##
            # Create DisplayPower object
            self.display_power = DisplayPower()
            self.dp_ports_list = ['DP_A', 'DP_B', 'DP_C', 'DP_D', 'DP_E', 'DP_F', 'DP_G', 'DP_H', 'DP_I']
            ##
            # get the pre_plugged target ids
            pre_plug_target_ids = self.display_target_ids()
            logging.info("Target ids during setup %s" % pre_plug_target_ids)
            ##
            # get the platform type
            self.machine_info = SystemInfo()
            self.gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
            for i in range(len(self.gfx_display_hwinfo)):
                self.platform_list.append(str(self.gfx_display_hwinfo[i].DisplayAdapterName).upper())
                self.adapter_list_to_verify.append(self.gfx_display_hwinfo[i].gfxIndex)
            if len(self.platform_list) > 1:
                self.ma_flag = True

            self.process_cmdline()
            ##
            # Start monitoring under-run
            self.under_run_status.clear_underrun_registry()
        except Exception as e:
            logging.error("[Test Issue]: Unexpected Exception occurred...Exiting...")
            self.tearDown()
            self.fail(e)

    ##
    # @brief        Processes the cmdline parameters.
    # @return       None
    def process_cmdline(self):
        self.cmd_args = sys.argv
        no_of_lfp_panels = 0
        # added "-selective" custom tags for VRR test case for tiled panel. Please don't remove that tag.
        self.cmd_list = cmd_parser.parse_cmdline(self.cmd_args, custom_tags=['-BPC', '-color_format', '-selective',
                                                                             '-power_events'])
        self.cmd_line_displays = cmd_parser.get_sorted_display_list(self.cmd_list)
        logging.info(f"Cmd Line Displays: {self.cmd_line_displays}")
        # Cmd line for MA will be returned as a list with each list item belonging to each adapter
        # converting SA returned value(dictionary) to list
        if type(self.cmd_list) is not list:
            self.cmd_list = [self.cmd_list]

        for i in range(len(self.cmd_list)):
            dp_panels = []
            hdmi_panels = []
            edp_panels = []
            mipi_panels = []
            adapter_info = self.cmd_list[i]
            self.config = adapter_info['CONFIG']
            for key, value in adapter_info.items():
                if "-BPC" in sys.argv and key == 'BPC':
                    self.bpc = int(adapter_info['BPC'][0])
                if "-COLOR_FORMAT" in sys.argv and key == 'COLOR_FORMAT':
                    self.color_format = adapter_info['COLOR_FORMAT'][0]
                if "-POWER_EVENTS" in sys.argv and key == 'POWER_EVENTS':
                    self.power_events = adapter_info['POWER_EVENTS']
                if DP_pattern.match(key) is not None:
                    dp_panels.append(value)
                elif HDMI_pattern.match(key) is not None:
                    hdmi_panels.append(value)
                elif EDP_pattern.match(key) is not None:
                    edp_panels.append(value)
                elif MIPI_pattern.match(key) is not None:
                    mipi_panels.append(value)

            ##
            # other_panel_count is count of panels other than tiled(DPs)
            self.other_panel_count = len(hdmi_panels) + len(edp_panels) + len(mipi_panels)
            if self.platform_list[i] in ['SKL', 'KBL', 'GLK', 'CNL'] and self.other_panel_count > 1:
                logging.error("[Test Issue]: Incorrect display config for tiled display. Exiting .....")
                self.fail()
            if self.platform_list[i] in ['ICLLP'] and self.other_panel_count > 2:
                logging.error("[Test Issue]: Incorrect display config for tiled display. Exiting .....")
                self.fail()
            ##
            # displays_list[] is a list of total displays
            self.displays_list = list(dp_panels + hdmi_panels + edp_panels + mipi_panels)
            if len(dp_panels) < 2:
                logging.error("[Test Issue]: Insufficient DP panels for tiled display. Exiting .....")
                self.fail()

            self.ma_dp_panels.append(dp_panels)
            self.ma_hdmi_panels.append(hdmi_panels)
            self.ma_edp_panels.append(edp_panels)
            self.ma_mipi_panels.append(mipi_panels)

            # breaking the loop when it looped over all the adapters
            if i+1 == len(self.platform_list):
                break

    ##
    # @brief        Plugs/unplugs non-tiled displays
    # @param[in]    action: str
    #                    action for display i.e. plug/unplug
    # @param[in]    low_power: Boolean
    #                    low_power True or false
    # @return       None
    def non_tiled_display_helper(self, action="Plug", low_power=False):
        ##
        # plug displays other than edp and tiled
        action = action.upper()
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("[Test Issue]: Invalid plug action for non tiled display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] Invalid plug action-'{}' received for tiled display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        for adapter_index in range(len(self.ma_hdmi_panels)):
            gfx_index = "gfx_" + str(adapter_index)
            hdmi_panels_per_adapter = self.ma_hdmi_panels[adapter_index]
            if action == "PLUG":
                plug_val = display_utility.plug(hdmi_panels_per_adapter['connector_port'],
                                                hdmi_panels_per_adapter['edid_name'], None, low_power,
                                                gfx_index=gfx_index)
                if plug_val is True:
                    logging.info("HDMI display plug successful on adapter {}".format(gfx_index))
                else:
                    logging.error("Failed to plug HDMI display on adapter {}. Exiting .....".format(gfx_index))
                    # Gdhm reporting handled in plug
                    self.fail()

                target_ids = self.display_target_ids()
                logging.info("Target Ids :%s" % target_ids)
            elif action == "UNPLUG":
                plug_val = display_utility.unplug(hdmi_panels_per_adapter['connector_port'], low_power,
                                                  gfx_index=gfx_index)
                if plug_val is True:
                    logging.info("HDMI display Unplug successful on adapter {}".format(gfx_index))
                else:
                    logging.error("HDMI display Unplug unsuccessful")
                    logging.error("Failed to Unplug HDMI display. Exiting .....")
                    # Gdhm reporting handled in unplug
                    self.fail()
                target_ids = self.display_target_ids()
                logging.info("Target Ids :%s" % target_ids)
        ##
        # Check for CRC amd Underrun after plug/unplug of non-tiled display
        self.verify_underrun_and_crc()

    ##
    # @brief        Plugs/unplugs the tiled displays
    # @param[in]    action: str
    #                    action for display i.e. plug/unplug
    # @param[in]    low_power: Boolean
    #                    low_power True or false
    # @return       None
    def tiled_display_helper(self, action="Plug", low_power=False):
        action = action.upper()
        if action not in ['PLUG', 'UNPLUG', 'MASTER_PORT_PLUG']:
            logging.error("[Test Issue]: Invalid plug action for tiled display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] Invalid plug action-'{}' received for tiled display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        for i in range(len(self.ma_dp_panels)):
            gfx_index = "gfx_" + str(i)
            ##
            # separate the master and slave tile information given through the cmd line
            dp_panel1 = self.ma_dp_panels[i][0]
            dp_panel2 = self.ma_dp_panels[i][1]
            ##
            # The first DP display mentioned in the cmd line will be the port type for
            # Master Tile Display which will have the Master.EDID and the DPCD passed
            # along with it.
            master_panel = dp_panel1
            slave_panel = dp_panel2

            ##
            # Accessing EDID and DPCD parameter list
            master_tile_edid = master_panel['edid_name']
            master_tile_dpcd = master_panel['dpcd_name']
            slave_tile_edid = slave_panel['edid_name']
            slave_tile_dpcd = slave_panel['dpcd_name']
            if master_tile_dpcd:
                master_tile_dpcd = master_panel['dpcd_name']
            else:
                master_tile_dpcd = slave_tile_dpcd
            ##
            # Check for valid EDID and DPCD names passed through cmd line
            if (master_tile_edid not in self.valid_edid_list) or (slave_tile_edid not in self.valid_edid_list) or \
                    (master_tile_dpcd not in self.valid_dpcd_list):
                logging.error(" Invalid Master/Slave/DPCD files given through command line. Exiting ...")
                self.fail()

            master_plug = False
            slave_plug = False
            if action == "PLUG":
                master_plug = slave_plug = True
            elif action == "UNPLUG":
                master_plug = slave_plug = False
            ##
            # call plug_unplug_tiled_display() from DisplayPort DLL to plug the tiled display
            result = self.display_port.plug_unplug_tiled_display(master_plug, slave_plug,
                                                                 master_panel['connector_port'],
                                                                 slave_panel['connector_port'], master_tile_edid,
                                                                 slave_tile_edid, master_tile_dpcd, low_power,
                                                                 gfx_index=gfx_index)
            logging.info("For Adapter {}...".format(i))

            ##
            # Check for plug/unplug tiled display failure and log information accordingly
            if (action == "PLUG") and (result is False):
                logging.error("Hotplug of Tiled Display failed on adapter {}. Exiting .....".format(gfx_index))
                # gdhm reporting handled in plug_unplug_tiled_display
                self.fail()
            elif (action == "UNPLUG") and (result is False):
                logging.error("Unplug of Tiled Display failed on adapter {}. Exiting .....".format(gfx_index))
                # gdhm reporting handled in plug_unplug_tiled_display
                self.fail()
            elif action == "UNPLUG" and (result is True) and (master_plug is False) and (slave_plug is False) and (
                    low_power is False):
                logging.info("Unplug of Tiled Display Successful on {} when System is active".format(gfx_index))
            elif action == "UNPLUG" and (result is True) and (master_plug is False) and (slave_plug is False) and (
                    low_power is True):
                logging.info(
                    "Unplug of Tiled Display Successful on {} when System in Low-Power state".format(gfx_index))
            elif action == "PLUG" and (result is True) and (master_plug is True) and (slave_plug is True) and (
                    low_power is False):
                logging.info("Hotplug of Tiled Display Successful on {} when System is active".format(gfx_index))
            elif action == "PLUG" and (result is True) and (master_plug is True) and (slave_plug is True) and (
                    low_power is True):
                logging.info("Hotplug of Tiled Display Successful on {} when System in Low-Power state".format(gfx_index))

            ##
            # Check for CRC amd Underrun after plug/unplug of tiled display
            self.verify_underrun_and_crc()

    ##
    # @brief        Plugs/unplugs the master/slave port
    # @param[in]    action: str
    #                    action for display i.e. Slave_Port_Unplug or Master_Port_Plug etc.
    # @param[in]    low_power: Boolean
    #                    low_power True or false
    # @return       None
    def plug_master_or_unplug_slave(self, action="Slave_Port_Unplug", low_power=False):
        action = action.upper()
        if action not in ['MASTER_PORT_PLUG', 'SLAVE_PORT_UNPLUG']:
            logging.error("[Test Issue]: Invalid plug action for tiled display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] Invalid plug action-'{}' received for tiled display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        for i in range(len(self.ma_dp_panels)):
            gfx_index = "gfx_" + str(i)
            ##
            # separate the master and slave tile information given through the cmd line
            dp_panel1 = self.ma_dp_panels[i][0]
            dp_panel2 = self.ma_dp_panels[i][1]
            ##
            # The first DP display mentioned in the cmd line will be the port type for
            # Master Tile Display which will have the Master.EDID and the DPCD passed
            # along with it.
            master_panel = dp_panel1
            slave_panel = dp_panel2

            ##
            # Accessing EDID and DPCD parameter list
            master_tile_edid = master_panel['edid_name']
            master_tile_dpcd = master_panel['dpcd_name']
            slave_tile_edid = slave_panel['edid_name']
            slave_tile_dpcd = slave_panel['dpcd_name']
            if master_tile_dpcd:
                master_tile_dpcd = master_panel['dpcd_name']
            else:
                master_tile_dpcd = slave_tile_dpcd

            ##
            # Check for valid EDID and DPCD names passed through cmd line
            if (master_tile_edid not in self.valid_edid_list) or (slave_tile_edid not in self.valid_edid_list) or \
                    (master_tile_dpcd not in self.valid_dpcd_list):
                logging.error(
                    "[Test Issue]: Invalid Master/Slave/DPCD files given through command line. Exiting ...")
                self.fail()
            ##
            # call plug_unplug_tiled_display() from DisplayPort DLL to plug the tiled display
            result = self.display_port.plug_master_or_unplug_slave_port(action.upper(),
                                                                        master_panel['connector_port'],
                                                                        slave_panel['connector_port'],
                                                                        master_tile_edid,
                                                                        slave_tile_edid, master_tile_dpcd,
                                                                        low_power, gfx_index=gfx_index)
            ##
            # Check for master plug/slave unplug failure and log information accordingly
            if (action == "MASTER_PORT_PLUG") and (result is False):
                logging.error("Master Port Plug failed on {}. Exiting .....".format(gfx_index))
                # gdhm reporting handled in plug_master_or_unplug_slave_port
                self.fail()
            elif (action == "SLAVE_PORT_UNPLUG") and (result is False):
                logging.error("Slave Port Unplug  failed on {}. Exiting .....".format(gfx_index))
                # gdhm reporting handled in plug_master_or_unplug_slave_port
                self.fail()

            elif action == "MASTER_PORT_PLUG" and result is True and low_power is False:
                logging.info("Master port plug successful on {} when system is active".format(gfx_index))
            elif action == "MASTER_PORT_PLUG" and result is True and low_power is True:
                logging.info("Master port plug successful on {} when system is in low power".format(gfx_index))
            elif action == "SLAVE_PORT_UNPLUG" and result is True and low_power is False:
                logging.info("Slave Unplug successful on {} when system is active".format(gfx_index))
            elif action == "SLAVE_PORT_UNPLUG" and result is True and low_power is True:
                logging.info("Slave Unplug successful on {} when system is in low power".format(gfx_index))

    ##
    # @brief        Setting Power Events- S3, S4, CS
    # @param[in]    power_state : str
    #                    power_state for RVP i.e. S3, S4, CS
    # @param[in]    resume_time : Int
    #                    resume_time in seconds
    # @return       None
    def power_event(self, power_state, resume_time):
        if self.display_power.invoke_power_event(power_state, resume_time):
            time.sleep(Delay_5_Secs)
            ##
            # Check for CRC amd Underrun after power event
            self.verify_underrun_and_crc()
        else:
            self.fail("[Test Issue]: Entry or Exit from power event Failed. Exiting .....")

    ##
    # @brief        Parses enumerated display and find the target IDs connected
    # @return       list of target ids
    def display_target_ids(self):
        display_target_ids = []
        ##
        # get the target ids after tiled display gets plugged
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays is not None:
            for index in range(enumerated_displays.Count):
                target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                display_target_ids.append(target_id)
        return display_target_ids

    ##
    # @brief        sets mode and checks for port sync enable
    # @return       None
    def apply_tiled_max_modes(self):
        logging.info("----- Applying Tiled Maximum Modes -----")
        ##
        # tiled_modes[] is a list of 5k3k/8k4k modes and different refresh rates
        tiled_modes = []
        tile_target_list = []
        tiled_display_adapter_list = []
        supported_modes_tiled = []
        tile_modes_list = []
        gfx_index = None
        flag = False
        tiled_flag = False
        ##
        # get the enumerated displays fro, SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(f"Enumerated displays: {enumerated_displays.to_string()}")
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_all_display_configuration()
        logging.info(f"current config: {config.to_string(enumerated_displays)}")

        for index in range(config.numberOfDisplays):
            tiled_target_id = config.displayPathInfo[index].targetId
            logging.info("Tile info for targetID %s", tiled_target_id)
            conn_port_type = str(CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
            #conn_port_type = str(CONNECTOR_PORT_TYPE(config.displayPathInfo[index].displayAndAdapterInfo.ConnectorNPortType))
            gfx_index = config.displayPathInfo[index].displayAndAdapterInfo.adapterInfo.gfxIndex
            display_adapter_info = self.display_config.get_display_and_adapter_info_ex(conn_port_type, gfx_index)
            tile_info = self.display_port.get_tiled_display_information(display_adapter_info)
            ##
            # check for tiled status
            if tile_info.TiledStatus:
                tiled_flag = True
                tiled_display_adapter_list.append(display_adapter_info)
                tile_target_list.append(config.displayPathInfo[index].targetId)
                ##
                # supported_modes_tiled[] is a list of modes supported by the tiled display
                supported_modes_tiled = self.display_config.get_all_supported_modes(tiled_display_adapter_list)

                ##
                # tile_modes_list[] is a list of modes supported by the tiled display
                if not self.ma_flag:
                    tile_modes_list = supported_modes_tiled[tiled_target_id]
                else:
                    tile_modes_list = supported_modes_tiled[(gfx_index, tiled_target_id)]

                ##
                # tile_maximum_resolution is the maximum resolution of the tiled display taken form the tile_modes_list[]
                tile_modes_list = sorted(tile_modes_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                if len(tile_modes_list) > 1:
                    tile_maximum_resolution = tile_modes_list[len(tile_modes_list) - 1]
                ##
                # check whether the resolution from list of modes is equal to the resolution from the tiled edid
                tiled_edid_hz_res = tile_info.HzRes
                tiled_edid_vt_res = tile_info.VtRes
                logging.info("Tiled Resolution from EDID for targetID %s on %s : %s x %s",
                             (config.displayPathInfo[index].targetId), gfx_index, tiled_edid_hz_res, tiled_edid_vt_res)
                logging.info("Tiled Resolution from Driver for targetID %s on %s : %s x %s",
                             (config.displayPathInfo[index].targetId), gfx_index,
                             tile_maximum_resolution.HzRes, tile_maximum_resolution.VtRes)
                if (tiled_edid_hz_res == tile_maximum_resolution.HzRes) and \
                        (tiled_edid_vt_res == tile_maximum_resolution.VtRes):

                    flag = True
                    for key, values in supported_modes_tiled.items():
                        values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                        for mode in values:
                            ##
                            # set all modes with HzRes = 5k/8k and VtRes = 3k/4k with various refresh rates
                            if mode.HzRes == tiled_edid_hz_res and mode.VtRes == tiled_edid_vt_res:
                                tiled_modes.append(mode)
                else:
                    logging.error(
                        "Modes enumerated by the Graphics driver not matching with modes in EDID. Exiting .....")
                    gdhm.report_bug(
                        title="[Interfaces][DP_Tiled] Driver enumerated modes and edid modes are not matching",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail()

        if tiled_flag is False:
            logging.error("[Test Issue]: Display doesn't support Tiled modes. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] DP Tiled tests are running on non-tiled displays",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        if flag:
            logging.info("Applying 5k3k/8k4k Tiled Modes @ different RRs")
            for tile_mode in tiled_modes:
                self.log_mode_info(tile_mode, enumerated_displays)
                ##
                # apply the mode having the maximum resolution and different refresh rates
                modes_flag = self.display_config.set_display_mode([tile_mode])
                if modes_flag is False:
                    logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                    ##
                    # Gdhm bug reported in display_config.set_display_mode
                    self.fail()
                ##
                # Comparing current mode with targeted mode
                current_mode = self.display_config.get_current_mode(tile_mode.displayAndAdapterInfo)
                if current_mode == tile_mode:
                    logging.info("Current mode is same as targeted mode")
                else:
                    enumerated_displays = self.display_config.get_enumerated_display_info()
                    logging.error(
                        "Targeted mode is not matching with the current mode. \nCurrent mode is : {} \nTargeted mode is: {}".format(
                            current_mode.to_string(enumerated_displays), tile_mode.to_string(enumerated_displays)))
                    self.fail()

                ##
                # If BPC is passed in command line, verifying transcoder's BPC with expected BPC.
                if "-BPC" in sys.argv:
                    for index in range(enumerated_displays.Count):
                        if enumerated_displays.ConnectedDisplays[index].TargetID == tile_mode.targetId:
                            port_name = str(
                                CONNECTOR_PORT_TYPE(
                                    enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
                            gfx_index = enumerated_displays.ConnectedDisplays[
                                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                            transcoder_bpc = DSCHelper.get_source_bpc(gfx_index, port_name)
                            if transcoder_bpc == self.bpc:
                                logging.info("Expected BPC value is same as Transcoder BPC")
                            else:
                                self.fail(
                                    "Expected BPC is not matching with Tanscoder BPC. Expected BPC = %s, Transcoder PBC = %s" %
                                    (self.bpc, transcoder_bpc))

                ##
                # Check for CRC amd Underrun
                self.verify_underrun_and_crc()
                ##
                # check for port sync enable
                flag_list = self.verify_port_sync_enable()
                for index in range(len(flag_list)):
                    adapter = "gfx_" + str(index)
                    if flag is True:
                        logging.info("Port Sync enabled on adapter {}".format(adapter))
                    else:
                        logging.error("[Driver Issue]: Port Sync is not enabled for {}. Exiting .....".format(adapter))
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled] Port sync could not be enabled by driver",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

    ##
    # @brief        sets mode and checks for port sync enable.
    # @return       None
    def apply_and_verify_non_tiled_max_mode(self):
        logging.info("----- Applying Non Tiled Max Mode -----")
        non_tiled_flag = False
        ##
        # get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            conn_port = str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
            gfx_index = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display_utility.get_vbt_panel_type(conn_port, gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                continue
            time.sleep(Delay_5_Secs)
            if conn_port in self.dp_ports_list:
                display_adapter_info = [enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo]
                ##
                # supp_modes_non_tiled[] is a list of modes supported by the non tiled display
                supp_modes_non_tiled = self.display_config.get_all_supported_modes(display_adapter_info)
                for key, values in supp_modes_non_tiled.items():
                    for mode in values:
                        ##
                        # check whether 4k@60 Hz is enumerated by the graphics driver or not
                        if (mode.HzRes == 3840 or mode.HzRes == 4096) and mode.VtRes == 2160 and mode.refreshRate == 60:
                            non_tiled_flag = True
                            self.log_mode_info(mode, enumerated_displays)
                            ##
                            #  apply the 4k@60 Hz from the supp_modes_non_tiled[] enumerated by the graphics driver
                            modes_flag = self.display_config.set_display_mode([mode])
                            if modes_flag is False:
                                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                gdhm.report_bug(
                                    title="[Interfaces][DP_Tiled] DP Mode Set failed for Port '{}' for resolution"
                                          " {}x{}@{}".format(conn_port, mode.HzRes, mode.VtRes, mode.refreshRate),
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail()
                            ##
                            # Comparing current mode with targeted mode
                            current_mode = self.display_config.get_current_mode(mode.displayAndAdapterInfo)
                            if current_mode == mode:
                                logging.info("Current mode is same as targeted mode")
                            else:
                                enumerated_displays = self.display_config.get_enumerated_display_info()
                                logging.error(
                                    "Targeted mode is not matching with the current mode. \nCurrent mode is : {} \nTargeted mode is: {}".format(
                                        current_mode.to_string(enumerated_displays),
                                        mode.to_string(enumerated_displays)))
                                self.fail()
                            ##
                            #  Check for CRC amd Underrun
                            self.verify_underrun_and_crc()
                    ##
                    # if 4k@60 Hz is not enumerated by the graphics driver then fail the test
                    if not non_tiled_flag:
                        logging.error("[Driver Issue]: 4k@60Hz not enumerated by the graphics driver. Exiting ...")
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled] DP 4k@60Hz Mode is not enumerated",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()
                if display_adapter_info:
                    ##
                    # Verify Current Mode
                    current_mode = self.display_config.get_current_mode(display_adapter_info[0])
                    if ((current_mode.HzRes == 3840) or (current_mode.HzRes == 4096)) and current_mode.VtRes == 2160 \
                            and current_mode.refreshRate == 60:
                        logging.info("Current mode is %s x %s @ %s Hz" %
                                     (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                    else:
                        logging.error("[Driver Issue]: Current mode is not 4k@60Hz. Exiting .....")
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled] DP 4k@60Hz Mode is not enumerated",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()
                else:
                    logging.error("No DP Display found. Exiting ...")
                    self.fail()

    ##
    # @brief        sets mode and checks for port sync enable.
    # @return       Boolean
    # @return       Tiled_target_id : Target ID of tiled display
    def tiled_display_adapter_info(self):
        flag = None
        tiled_display_adapter_info = []
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_all_display_configuration()
        for index in range(config.numberOfDisplays):
            display_adapter_info = config.displayPathInfo[index].displayAndAdapterInfo
            tile_info = self.display_port.get_tiled_display_information(display_adapter_info)
            ##
            # check for tiled status
            if tile_info.TiledStatus:
                tiled_display_adapter_info.append(display_adapter_info)
                flag = True
            else:
                continue
        if flag:
            return True, tiled_display_adapter_info
        else:
            return False, 0

    ##
    # @brief        Check for applied mode status.
    # @return       Boolean
    def verify_tiled_mode(self):
        tiled_flag, tiled_display_adapter_info_list = self.tiled_display_adapter_info()
        tiled_hz_res = None
        tiled_vt_res = None

        for tiled_display_adapter_info in tiled_display_adapter_info_list:
            gfx_index = tiled_display_adapter_info.adapterInfo.gfxIndex
            ##
            # check current tiled mode
            if tiled_flag:
                tile_info = self.display_port.get_tiled_display_information(tiled_display_adapter_info)
                if tile_info.TiledStatus:
                    tiled_hz_res = tile_info.HzRes
                    tiled_vt_res = tile_info.VtRes
            else:
                logging.error("[Test Issue]: Tiled display is not found on {}. Exiting ... ".format(gfx_index))
                gdhm.report_bug(
                    title="[Interfaces][DP_Tiled] DP Tiled tests are running on non-tiled displays on {}".format(
                        gfx_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()
            current_mode = self.display_config.get_current_mode(tiled_display_adapter_info)
            if current_mode.HzRes == tiled_hz_res and current_mode.VtRes == tiled_vt_res \
                    and current_mode.refreshRate == 60:
                logging.info(
                    "Current mode is %s x %s @ %s" % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
                return True
            else:
                logging.error("[Driver Issue]: Current mode is not 5k3k@60Hz. Exiting .....")
                gdhm.report_bug(
                    title="[Interfaces][DP_Tiled] Failed to apply Tiled mode of 5k3k@60Hz",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

    ##
    # @brief        Check if the given display is tiled or not by checking 22nd bit of the tiled target id.
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    port_type - String representation of CONNECTOR_PORT_TYPE
    # @return       is_target_id_tiled - Boolean . Returns True if bit 22nd of target ID is set to 1, else returns False
    def is_tiled_target(self, gfx_index, port_type) -> bool:
        display_adapter_info = self.display_config.get_display_and_adapter_info_ex(port_type, gfx_index)
        target_id = TARGET_ID(Value=display_adapter_info.TargetID)
        is_target_id_tiled = target_id.TiledDisplay == 1
        return is_target_id_tiled

    ##
    # @brief        Verifies whether port sync is enabled or not.
    # @return       port_sync_status : Boolean
    def verify_port_sync_enable(self):
        port_sync_status_list = []
        for each_platform, adapter in zip(self.platform_list, self.adapter_list_to_verify):
            port_sync_status = False
            logging.info("Port Sync for Adapter {}".format(adapter))
            ##
            # the below code gets executed if platform is SKL/KBL/CNL/GLK
            if each_platform in ["SKL", "KBL", "GLK", "CNL", "CFL"]:
                ddi_list = ["TRANS_DDI_FUNC_CTL_A", "TRANS_DDI_FUNC_CTL_B", "TRANS_DDI_FUNC_CTL_C"]

                for ddi in ddi_list:
                    ddi_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", ddi, gfx_index=adapter)

                    if ddi_reg.port_sync_mode_enable == 1:
                        if ddi_reg.port_sync_mode_master_select == 0b01:
                            logging.info(" Transcoder A Master is enabled")
                        if ddi_reg.port_sync_mode_master_select == 0b10:
                            logging.info(" Transcoder B Master is enabled")
                        if ddi_reg.port_sync_mode_master_select == 0b11:
                            logging.info(" Transcoder C Master is enabled")
                        port_sync_status = True
                        break
                    else:
                        port_sync_status = False
            ##
            # the below code gets executed for ICL and above platforms
            else:
                ddi_list = ["TRANS_DDI_FUNC_CTL2_A", "TRANS_DDI_FUNC_CTL2_B", "TRANS_DDI_FUNC_CTL2_C",
                            "TRANS_DDI_FUNC_CTL2_D"]

                for ddi in ddi_list:
                    ddi_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", ddi)

                    if ddi_reg.port_sync_mode_enable == 1:
                        if ddi_reg.port_sync_mode_master_select == 0b001:
                            logging.info(" Transcoder A Master is enabled")
                        if ddi_reg.port_sync_mode_master_select == 0b010:
                            logging.info(" Transcoder B Master is enabled")
                        if ddi_reg.port_sync_mode_master_select == 0b011:
                            logging.info(" Transcoder C Master is enabled")
                        if ddi_reg.port_sync_mode_master_select == 0b100:
                            logging.info(" Transcoder C Master is enabled")
                        port_sync_status = True
                        break
                    else:
                        port_sync_status = False
            port_sync_status_list.append(port_sync_status)

        return port_sync_status_list

    ##
    # @brief         Helper function which will set the mouse cursor position across the display monitors
    # @param[in]     src_port : str
    #                connector_port_type of the source display
    # @param[in]     dst_port : str
    #                connector_port_type of the destination display
    # @return        None
    def tiled_move_cursor(self, src_port, dst_port):
        src_path_index = dst_path_index = -1
        ##
        # Get the enumerated display information
        enumerated_info = self.display_config.get_enumerated_display_info()
        ##
        # call display_config
        get_config = self.display_config.get_current_display_configuration()

        for index in range(len(self.ma_dp_panels)):
            master_panel = self.ma_dp_panels[index][0]
            slave_panel = self.ma_dp_panels[index][1]
            master_port_id = master_panel['connector_port']
            slave_port_id = slave_panel['connector_port']
            ##
            # Fetch the target ID of the displays based on the connector_port_type
            src_target_id = self.display_config.get_target_id(src_port, enumerated_info)
            dst_target_id = self.display_config.get_target_id(dst_port, enumerated_info)
            ##
            # check if the target ids are valid and fetch the path index of the displays based on the target ID
            for index in range(0, get_config.numberOfDisplays):
                if get_config.displayPathInfo[index].targetId == src_target_id:
                    src_path_index = index
                if get_config.displayPathInfo[index].targetId == dst_target_id:
                    dst_path_index = index

            if master_port_id == src_port:
                master_tiled_port = master_port_id
                slave_tiled_port = slave_port_id
            else:
                master_tiled_port = slave_port_id
                slave_tiled_port = master_port_id
            ##
            # enumerate the display monitors
            monitor_dimension = window_helper.enum_display_monitors()
            logging.info("Monitor Dimensions: %s" % monitor_dimension)
            if self.config == 'EXTENDED':
                ##
                # Set Cursor position on non-tiled display and check for the cursor register whether enabled or not
                # Let's say Display1 = 5k3k and Display2 = 1920x1080, monitor_dimension will be
                # [[0,0,5120,2880],[5120,0,7040,1080]]. For setting the cursor position on the non-tiled Display2, we
                # will randomly set the cursor position taking X and Y coordinates between (5120,7040)x(0,1080).
                non_tiled_x = randint(monitor_dimension[dst_path_index][0], monitor_dimension[dst_path_index][2])
                non_tiled_y = randint(monitor_dimension[dst_path_index][1], monitor_dimension[dst_path_index][3])
                logging.info("X Coordinates of Cursor on Non-Tiled Display: %s" % non_tiled_x)
                logging.info("Y Coordinates of Cursor on Non-Tiled Display: %s" % non_tiled_y)
                ##
                # Set the cursor position by using SetCursorPos() which is a Win32 API
                win32api.SetCursorPos((non_tiled_x, non_tiled_y))
                ##
                # Verify the cursor position after setting it
                self.verify_cursor_position(non_tiled_x, non_tiled_y, dst_port)
                ##
                # Read Cursor Register
                # TODO: Currently as a work-around, driver enables SW cursor for Tiled Display if Tiled Display
                # is a part of the topology. Below logic to verify HW cursor enabled/not will be commented for
                # now until Graphics driver enables HW cursor.
                '''
                cursor_status = self.read_cursor_register(dst_port)
                if cursor_status is True:
                    logging.info("Non-Tiled Display %s Cursor Register is enabled" % dst_port)
                else:
                    logging.error("Non-Tiled Display %s Cursor Register is not enabled. Exiting ..." % dst_port)
                    self.fail()
                '''
            if self.config == 'EXTENDED' or self.config == 'SINGLE':
                ##
                # Set Cursor position on master and slave tiled display and check for the cursor register whether
                # enabled or not.
                # Let's say Display1(Tiled) = 5k3k and Display2 = 1920x1080, monitor_dimension will be
                # [[0,0,5120,2880],[5120,0,7040,1080]]. For setting the cursor position on the master tile of Display1,
                # we will randomly set the cursor position between (0 to 2560)x2880 and also on slave tile of Display1 between
                # (2560 to 5120)x2880.
                master_x = randint(monitor_dimension[src_path_index][0], (monitor_dimension[src_path_index][2]) / 2)
                master_y = randint(monitor_dimension[src_path_index][1], monitor_dimension[src_path_index][3])
                logging.info("X Coordinates of Cursor on master tile: %s" % master_x)
                logging.info("Y Coordinates of Cursor on master tile: %s" % master_y)
                ##
                # Set the cursor position by using SetCursorPos() which is a Win32 API
                win32api.SetCursorPos((master_x, master_y))
                ##
                # Verify the cursor position after setting it
                self.verify_cursor_position(master_x, master_y, master_tiled_port)
                ##
                # Read Cursor Register
                '''
                cursor_status = self.read_cursor_register(master_tiled_port)
                if cursor_status is True:
                    logging.info("Master Tiled %s Cursor Register is enabled" % master_tiled_port)
                else:
                    logging.error("Master Tiled %s Cursor Register is not enabled. Exiting ..." % master_tiled_port)
                    self.fail()
                '''
                ##
                # Set Cursor position on slave tiled display and check for the cursor register whether enabled or not
                slave_x = randint(monitor_dimension[src_path_index][2] / 2, monitor_dimension[src_path_index][2])
                slave_y = randint(monitor_dimension[src_path_index][1], monitor_dimension[src_path_index][3])
                logging.info("X Coordinates of Cursor on slave tile: %s" % slave_x)
                logging.info("Y Coordinates of Cursor on slave tile: %s" % slave_y)
                ##
                # Set the cursor position by using SetCursorPos() which is a Win32 API
                win32api.SetCursorPos((slave_x, slave_y))
                ##
                # Verify the cursor position after setting it
                self.verify_cursor_position(slave_x, slave_y, slave_tiled_port)
                ##
                # Read Cursor Register
                '''
                cursor_status = self.read_cursor_register(slave_tiled_port)
                if cursor_status is True:
                    logging.info("Slave Tiled %s Cursor Register is enabled" % slave_tiled_port)
                else:
                    logging.error("Slave Tiled %s Cursor Register is not enabled. Exiting ..." % slave_tiled_port)
                    self.fail()
                '''

    ##
    # @brief         Verify the cursor position after setting the position of the cursor by calling GetCursorPos()
    # @param[in]     x : Int
    #                X coordinate of the cursor position
    # @param[in]     y : Int
    #                Y coordinate of the cursor position
    # @param[in]     port_type : str
    #                connector_port_type of the displays across which the cursor position has to be set
    # @return        None
    def verify_cursor_position(self, x, y, port_type):
        ##
        # Verify the cursor position by using GetCursorPos() which is a Win32 API
        h_x, h_y = win32api.GetCursorPos()
        if h_x == x and h_y == y:
            logging.info("Verify Cursor position successful")
        else:
            logging.error("[Driver Issue]: Verify Cursor position failed at:%s x %s. Exiting ..." % (h_x, h_y))
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] Verification of cursor position failed at:{} x {}".format(h_x, h_y),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief         Verify whether the Cursor Register is enabled or not
    # @param[in]     port_type : str
    #                connector_port_type of the display for which cursor position is to be read
    # @return        Bool
    # TODO: Currently as a work-around, driver enables SW cursor for Tiled Display if Tiled Display
    # is a part of the topology. Below logic to verify HW cursor enabled/not will be commented for
    # now until Graphics driver enables HW cursor.
    def read_cursor_register(self, port_type):
        driver_interface_ = driver_interface.DriverInterface()

        cursor_status = False
        if port_type == 'DP_A':
            reg_val = driver_interface_.mmio_read(Cursor_A_Register, 'gfx_0')
            reg_val = hex(reg_val)[:-1]
            if (int(reg_val, 16) & 0x3f) == 0:
                cursor_status = False
            else:
                cursor_status = True
        if port_type == 'DP_B':
            reg_val = driver_interface_.mmio_read(Cursor_B_Register, 'gfx_0')
            reg_val = hex(reg_val)[:-1]
            if (int(reg_val, 16) & 0x3f) == 0:
                cursor_status = False
            else:
                cursor_status = True
        if port_type == 'DP_C':
            reg_val = driver_interface_.mmio_read(Cursor_C_Register, 'gfx_0')
            reg_val = hex(reg_val)[:-1]
            if (int(reg_val, 16) & 0x3f) == 0:
                cursor_status = False
            else:
                cursor_status = True
        if port_type == 'DP_D':
            reg_val = driver_interface_.mmio_read(Cursor_D_Register, 'gfx_0')
            reg_val = hex(reg_val)[:-1]
            if (int(reg_val, 16) & 0x3f) == 0:
                cursor_status = False
            else:
                cursor_status = True
        return cursor_status

    ##
    # @brief         set configuration on the connected displays
    # @param[in]     topology : str
    #                topology to be applied i.e. single/extended/clone/triclone/triextended
    # @param[in]     no_of_combinations : Int
    #                Y coordinate of the cursor position
    # @return        None
    def set_config(self, topology, no_of_combinations=2):
        ##
        # flag to tell whether plugged display is tiled or no
        tiled_flag = False
        ##
        # get tiled topology to be applied on tiled display
        tiled_topology = eval("enum.%s" % (topology))
        ##
        # get the enumerated displays fro, SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.info(f"Enumerated displays: {enumerated_displays.to_string()}")
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_all_display_configuration()
        logging.info(f"current config: {config.to_string(enumerated_displays)}")

        for index in range(config.numberOfDisplays):
            tile_info = self.display_port.get_tiled_display_information(
                config.displayPathInfo[index].displayAndAdapterInfo)
            ##
            # check for tiled status
            if tile_info.TiledStatus is True:
                tiled_flag = True
                display_adapter_list = []
                ##
                # if topology is 'SINGLE', display_list[] will have port type of tiled display only
                if topology == 'SINGLE':
                    for i in range(enumerated_displays.Count):
                        tiled_display_info = self.display_port.get_tiled_display_information(
                            enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo)
                        ##
                        # check for tiled status and append the port type to display_list[]
                        if tiled_display_info.TiledStatus is True:
                            display_info = str(
                                CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType))
                            gfx_index = enumerated_displays.ConnectedDisplays[
                                i].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                            display_adapter_list.append((display_info, gfx_index))
                    ##
                    # combination_list[] is a list of combination of display+adapter
                    combination_list = display_utility.get_possible_configs(display_adapter_list, True)

                    config_combination_list = combination_list['enum.SINGLE']
                    self.primary_display = config_combination_list[0][0][0]
                ##
                # if topology is 'EXTENDED', display_list[] will have port type of tiled and non-tiled display
                else:
                    for i in range(enumerated_displays.Count):
                        display_info = str(
                            CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType))
                        gfx_index = enumerated_displays.ConnectedDisplays[
                            i].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                        display_adapter_list.append((display_info, gfx_index))
                    ##
                    # combination_list[] is a list of combination of displays
                    combination_list = display_utility.get_possible_configs(display_adapter_list)

                    if topology == 'EXTENDED' and enumerated_displays.Count > 1:
                        if no_of_combinations == 1:
                            config_combination_list = combination_list['enum.EXTENDED']
                            self.primary_display = config_combination_list[0][0][0]
                            self.secondary_display = config_combination_list[0][1][0]
                            config_combination_list = [config_combination_list[0]]
                        else:
                            config_combination_list = combination_list['enum.EXTENDED']
                    elif topology == 'CLONE':
                        if no_of_combinations == 1:
                            config_combination_list = combination_list['enum.CLONE']
                            self.primary_display = config_combination_list[0][0][0]
                            self.secondary_display = config_combination_list[0][1][0]
                            config_combination_list = [config_combination_list[0]]
                        else:
                            config_combination_list = combination_list['enum.CLONE']
                    else:
                        logging.error(
                            "[Test Issue]: Either not a valid configuration or number of display count insufficient. "
                            "Exiting .....")
                        self.fail()

                each_combination_adapter_info_list = []
                for each_combination in config_combination_list:
                    display_and_adapter_info_list = []
                    # each_combination items are in format of a Tuple (<display_port>, <gfx_index>) e.g. (dp_b, gfx_0),
                    # Extracting port and gfx index from this
                    for each_display in each_combination:
                        port = each_display[0]
                        gfx_index = each_display[1]
                        display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(port, gfx_index)
                        display_and_adapter_info_list.append(display_and_adapter_info)

                    each_combination_adapter_info_list.append(display_and_adapter_info_list)

                ##
                # set display configuration according to the topology
                for i in range(len(each_combination_adapter_info_list)):
                    if self.display_config.set_display_configuration_ex(tiled_topology, each_combination_adapter_info_list[i]):
                        ##
                        # Check for CRC amd Underrun after setting the config
                        self.verify_underrun_and_crc()
                    else:
                        logging.error("Set Display Configuration Failed. Exiting .....")
                        # Gdhm bug reported in set_display_configuration_ex
                        self.fail()
        if tiled_flag is False:
            logging.error("[Test Issue]: Display doesn't support Tiled modes. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] DP Tiled tests are running on non-tiled displays",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief         logging set modes information as a string
    # @param[in]     mode : DisplayMode
    #                mode that is being set
    # @param[in]     enumerated_displays : EnumeratedDisplays
    #                enumerated_displays information from system_utility
    # @param[in]     rotation : Bool
    # @return        None
    def log_mode_info(self, mode, enumerated_displays, rotation=False):
        mode_str = mode.to_string(enumerated_displays)
        gfx_index = mode.displayAndAdapterInfo.adapterInfo.gfxIndex
        index = int(str(gfx_index).split("_")[1])
        logging.info("Logging Mode Info for adapter {}".format(gfx_index))
        master_panel = self.ma_dp_panels[index][0]
        master_tile_edid = master_panel['edid_name']
        if rotation:
            if mode_str[:4] == self.primary_display:
                resolution_str = mode_str[:4] + ' (' + master_tile_edid + '), ' + mode_str[6:]
                logging.info("Rotating Primary Display  %s on adapter %s", resolution_str, gfx_index)
            else:
                resolution_str = mode_str[:4] + ' (' + master_tile_edid + '), ' + mode_str[6:]
                logging.info("Rotating Secondary Display %s on adapter %s", resolution_str, gfx_index)
        else:
            if mode_str[:4] == self.primary_display:
                resolution_str = mode_str[:4] + '(' + master_tile_edid + ')' + mode_str[4:]
                logging.info("Setting mode on Primary Display %s on adapter %s", resolution_str, gfx_index)
            else:
                resolution_str = mode_str[:4] + '(' + master_tile_edid + ')' + mode_str[4:]
                logging.info("Setting mode on Secondary Display %s on adapter %s", resolution_str, gfx_index)

    ##
    # @brief         logging current modes information as a string
    # @param[in]     mode : mode to print the info of
    # @param[in]     enumerated_displays : EnumeratedDisplays
    #                enumerated_displays information from system_utility
    # @param[in]     rotation : Bool
    # @return        None
    def current_mode_info(self, mode, enumerated_displays, rotation=False):

        curr_mode = self.display_config.get_current_mode(mode.displayAndAdapterInfo)
        curr_mode_str = curr_mode.to_string(enumerated_displays)
        for i in range(len(self.ma_dp_panels)):
            master_panel = self.ma_dp_panels[i][0]
            master_tile_edid = master_panel['edid_name']
            if rotation:
                if curr_mode_str[:4] == self.primary_display:
                    resolution_str = curr_mode_str[:4] + ' (' + master_tile_edid + '), ' + curr_mode_str[6:]
                    logging.info("Current Mode Set on Primary Display %s", resolution_str)
                else:
                    resolution_str = curr_mode_str[:4] + ' (' + master_tile_edid + '), ' + curr_mode_str[6:]
                    logging.info("Current Mode Set on Secondary Display %s", resolution_str)
            else:
                if curr_mode_str[:4] == self.primary_display:
                    resolution_str = curr_mode_str[:4] + '(' + master_tile_edid + ')' + curr_mode_str[4:]
                    logging.info("Current Mode Set on Primary Display %s", resolution_str)
                else:
                    resolution_str = curr_mode_str[:4] + '(' + master_tile_edid + ')' + curr_mode_str[4:]
                    logging.info("Current Mode Set on Primary Display %s", resolution_str)

    ##
    # @brief        Get Current Refresh Rate of all the connected displays
    # @return       dict : Dictionary
    #               Dictionary where key = TargetID of all the current active displays
    #               and value = current refresh rate of all the current active displays
    def get_current_rr_and_targetid(self):
        dict = {}
        ##
        # get the current display config details
        config = self.display_config.get_current_display_configuration()
        ##
        # get the number of active displays to get the target id and refresh rate one by one
        for index in range(config.numberOfDisplays):
            target_id = config.displayPathInfo[index].targetId
            display_adapter_info = config.displayPathInfo[index].displayAndAdapterInfo
            gfx_index = config.displayPathInfo[index].displayAndAdapterInfo.adapterInfo.gfxIndex
            ##
            # call get_current_mode() to get the current refresh rate of the connected displays
            curr_mode = self.display_config.get_current_mode(display_adapter_info)
            curr_refresh_rate = curr_mode.refreshRate
            key = target_id + "_" + gfx_index
            dict[key] = curr_refresh_rate
        return dict

    ##
    # @brief        Verifies for Underrun and CRCs
    # @return       None
    def verify_underrun_and_crc(self):
        ##
        # Verify Under-run
        self.under_run_status.verify_underrun()

        '''
        # TODO: Currently, more rework is required for CRC verification from the API level.
        ##
        # call get_current_rr_and_targetid() which returns a dictionary having target ids and refresh rates
        dict = self.get_current_rr_and_targetid()
        ##
        # Verify whether the dictionary is empty or not
        if bool(dict):
            for target_id, refresh_rate in dict.items():
                pattern_match = []
                ##
                # calculate the pattern match value according to the refresh rate of the display
                # e.g. if RR = 60Hz then pattern_match = [295, 295, 295, 295, 295, 295],
                # if RR = 40 then pattern_match = [195, 195, 195, 195, 195, 195]
                pattern_match += CRC_PATTERN_MATCH_LENGTH * [(refresh_rate * 5) - 5]
                logging.info("CRC Pattern Match List for TargetID: %s at Refresh Rate: %s is %s"% (target_id,
                                                                                                     refresh_rate, pattern_match))
                # call ComputeCRC() from valdi_crc_logger.py to compute the CRC values
                result = ComputeCRC(targetid = target_id, custom_pattern = pattern_match)
                if result:
                    logging.info("CRC Verification passed for TargetID: %s and custom pattern: %s"% (target_id, pattern_match))
                else:
                    logging.error("CRC Verification failed for TargetID: %s and custom pattern: %s. Exiting ..."% (target_id, pattern_match))
                    self.fail()
        else:
            logging.error("ComputeCRC failed as no TargetID and RefreshRate were given for calculating pattern match list. Exiting ...")
            self.fail()
        '''

    ##
    # @brief        Unit-test teardown function to uninitialize CUI SDK, unplug of tiled displays and verifies underruns
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        status = self.display_port.uninitialize_sdk()
        if status is True:
            logging.info("Uninitialization of CUI SDK Successful in TearDown().")
        else:
            logging.error("Uninitialization of CUI SDK Failed in TearDown().")

        ##
        # unplug tiled display
        self.tiled_display_helper(action="UNPLUG")
        time.sleep(Delay_5_Secs)
        ##
        # get target ids after tiled display unplugged
        post_plug_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % post_plug_target_ids)
        time.sleep(Delay_5_Secs)
        ##
        # Check for CRC amd Underrun
        self.verify_underrun_and_crc()
        logging.info("Test Clean Up")


if __name__ == '__main__':
    unittest.main()
