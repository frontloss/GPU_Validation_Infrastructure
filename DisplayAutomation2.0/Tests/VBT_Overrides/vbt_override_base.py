######################################################################################
# @file         vbt_override_base.py
# @brief        Base class for vbt override feature
# @details      Displays are external displays dp_b, dp_c, hdmi_b, hdmi_c, etc
# @author       Kumar V, Arun, Veluru, Veena
######################################################################################

import logging
import random
import sys
import time
import unittest

from Libs import env_settings
from Libs.Core import cmd_parser, reboot_helper, display_utility, display_essential
from Libs.Core.display_config import display_config, display_config_enums
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.vbt import vbt_context
from Libs.Core.vbt.vbt import Vbt
from Tests.Display_Port.DP_MST.dp_mst_parser import DPCommandParser
from Tests.PowerCons.Modules import common

##
# @brief        TestVbtSwingOverride base class : To be used in VBT Override tests
class VbtOverrideBase(unittest.TestCase):
    dp_mst_base = DisplayPort()

    ##
    # @brief        setup function. Initiaize required variables and call function to parse cmdlines
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUpClass")

        # Variable Initializing
        self.restrict_linkrate = ""
        self.input_display_list = []
        self.gfx_adapter_list = []
        self.custom_tags = ['-RESTRICT', '-PLUG_TOPOLOGIES']
        self.panel_index = {}
        self.config = display_config.DisplayConfiguration()
        self.gfx_vbt = Vbt()
        self.get_display_list_panel_index()
        self.platform = None


        simulation_type = env_settings.get('SIMULATION', 'simulation_type')
        # Changing Phy Buffer values is not recommended with real displays / emulators
        self.assertEqual(simulation_type, 'GFXVALSIM', "Test valid only for sink simulation mode")

        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        self.platform = gfx_display_hwinfo[0].DisplayAdapterName

        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUpClass")

    ##
    # @brief        tearDown function. Unplugs all Displays and resets VBT to default
    # @return       None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.info("Unplugging all External Displays")
        enum_display_dict = self.get_display_names()

        for display in enum_display_dict.keys():
            if display_utility.get_vbt_panel_type(display, 'gfx_0') not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                self.unplug_display(display)

    ##
    # @brief        This method helps to Unplug given display.
    # @param[in]    port - Name of display port (ex: DP_B, HDMI_C, etc).
    # @return       bool - True if request is success else False.
    def unplug_display(self, port):
        if display_utility.unplug(port) is False:
            logging.error("{} Unplug Call Failed".format(port))

        # Verify UnPlugged Display is not enumerated
        time.sleep(15)
        enumerated_displays = self.config.get_enumerated_display_info()
        logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())
        if display_config.is_display_attached(enumerated_displays, port) is False:
            logging.debug("{} Unplug Successful".format(port))
            return True

        logging.error("{} Unplug Call Passed but it is still attached".format(port))
        return False

    ##
    # @brief        This method returns currently emulated display name and target id.
    # @return       enum_display_dict - Dictionary Display Name as Key and Target ID as Value.
    def get_display_names(self):
        enum_display_dict = {}
        enumerated_displays = self.config.get_enumerated_display_info()
        for index in range(0, enumerated_displays.Count):
            port = display_config_enums.CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].
                                                            ConnectorNPortType).name
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            enum_display_dict[port] = target_id
        return enum_display_dict

    ##
    # @brief        get_display_list_panel_index function.
    #               This method gets display list and panel index from command line
    # @return       populates display_list and panel_index dictionary with key=port and value=panel index
    def get_display_list_panel_index(self):
        # Parse the commandline params
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        # input_display_list[] is a list of Port Names from user args
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if self.input_display_list.__contains__(value['connector_port']):
                        adapter = self.gfx_adapter_list[self.input_display_list.index(value['connector_port'])]
                    if not self.input_display_list.__contains__(value['connector_port']) or (
                            self.input_display_list.__contains__(value['connector_port']) and adapter != value[
                        'gfx_index']):
                        if (value['gfx_index'] == None):
                            value['gfx_index'] = 'gfx_0'
                    self.input_display_list.insert(value['index'], value['connector_port'])
                    self.panel_index[value['connector_port']] = value['panel_index']
                    self.gfx_adapter_list.insert(value['index'], value['gfx_index'].lower())

        if self.cmd_line_param['RESTRICT'] != 'NONE':
            self.restrict_linkrate = self.cmd_line_param['RESTRICT']


    ##
    # @brief        This method disables vswing override settings in vbt
    # @return       bool - True if request is success else False.
    def vbt_disable_vswing_override(self):
        self.clear_swing_override_table()
        for index in range(10):  # clear vswing override flag for every efp index
            self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].Flags1 &= 0b11011111
        return self.push_vbt_change()

    ##
    # @brief        This method fills custom vswing values in vbt
    # @return       None
    def clear_swing_override_table(self):
        # fill each block value with random values 0 or 1
        if self.platform == 'ICLLP':
            for i in range(4):
                for j in range(110):
                    self.gfx_vbt.block_57.VSwingPreempTables[i].VswingPreempTableFields[j] = 0

        elif self.platform == 'TGL':
            for i in range(6):
                for j in range(110):
                    self.gfx_vbt.block_57.VSwingPreempTables[i].VswingPreempTableFields[j] = 0

        elif self.platform == 'DG1':
            for i in range(4):
                for j in range(110):
                    self.gfx_vbt.block_57.VSwingPreempTables[i].VswingPreempTableFields[j] = 0
        elif self.platform == 'ADLP':
            for i in range(6):
                for j in range(110):
                    self.gfx_vbt.block_57.VSwingPreempTables[i].VswingPreempTableFields[j] = 0

        else:
            logging.error("Invalid Platform. VBT Vswing Override Verification not supported on Platform {}".format(
                self.platform))

    ##
    # @brief        This method enables vswing override settings in vbt
    # @param[in]    index - EFP panel index from VBT block 2
    # @return       bool - True if request is success else False.
    def vbt_enable_vswing_override(self, index):
        self.fill_swing_override_table()
        self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].Flags1 |= 0b00100000
        return self.push_vbt_change()

    ##
    # @brief        This method fills custom vswing values in vbt
    # @return       None
    def fill_swing_override_table(self):
        vbt_override_supported_platform_list = ['ICLLP', 'TGL', 'DG1', 'ADLP', 'MTL']
        # fill each block value with random values 0 or 1
        if self.platform in vbt_override_supported_platform_list:
            for i in range(6):
                for j in range(110):
                    self.gfx_vbt.block_57.VSwingPreempTables[i].VswingPreempTableFields[j] = random.randint(0, 1)
        else:
            logging.error("Invalid Platform. VBT Vswing Override Verification not supported on Platform {}".format(
                self.platform))

    ##
    # @brief        This method applies the VBT changes requested
    # @return       Bool. True if request is success else False.
    def push_vbt_change(self):
        if self.gfx_vbt.apply_changes() is False:
            logging.error('VBT apply changes failed')
            return False
        else:
            # Restart Display driver for changes to take effect
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error('Failed to Restart Display driver')
                return False
            logging.info('VBT apply changes passed')
            return True

    ##
    # @brief        This method checks VBT Block2 if requested port is supported
    # @param[in]    display_port - Name of display port (ex: DP_A, MIPI_A, etc).
    # @return       bool - True if request is success else False and Index from Block 2 if supported
    def get_port_status_vbt(self, display_port):
        vbt_efp_port_number = vbt_context.DVO_PORT_MAPPING[display_port]
        for index in range(10):
            stblock2_dvo_port = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DVOPort
            stblock2_device_class = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass
            if vbt_efp_port_number == stblock2_dvo_port and stblock2_device_class != 0:
                return True, index
        return False, 0

    ##
    # @brief        This method plugs the mst topology passed
    # @param[in]    gfx_index to plug the display on
    # @param[in]    port_name e.g. dp_b, dp_c
    # @param[in]    topology_type MST/SST
    # @param[in]    xml_file_name  Contains the MST topology information.
    # @param[in]    is_low_power True to plug in low power mode, False to plug in normal mode
    # @return       None
    def plug_mst_display(self, gfx_index, port_name, topology_type, xml_file_name, is_low_power):

        is_success = VbtOverrideBase.dp_mst_base.init_dp(port_name, topology_type)
        self.assertTrue(is_success, "Initializing of {} Failed".format(port_name))
        logging.info("Initializing {} Succeeded".format(port_name))

        is_success = VbtOverrideBase.dp_mst_base.parse_send_topology(port_name, topology_type, xml_file_name, is_low_power)
        self.assertTrue(is_success, "Failed to parse and send data to simulation driver for {}".format(port_name))
        logging.info("Successfully parsed and send data to simulation driver for {}".format(port_name))

        is_success = VbtOverrideBase.dp_mst_base.set_hpd(port_name, attach_dettach=True, gfx_index=gfx_index)
        self.assertTrue(is_success, "Set HPD call failed for {}".format(port_name))
        logging.info("Set HPD call succeeded for {}".format(port_name))

        time.sleep(20)

        common.print_current_topology()

    ##
    # @brief        This method plugs the mst topology passed
    # @return       None
    def plug_mst_topologies(self):

        dp_mst_command_parser = DPCommandParser()
        requested_topology_info_dict = dp_mst_command_parser.requested_topology_info_dict
        port_name_list = dp_mst_command_parser.requested_dp_port_list

        index = 0
        while index < len(port_name_list):
            port_name = port_name_list[index]

            xml_file_name = requested_topology_info_dict[index].path
            logging.info("XML File Name: {}".format(xml_file_name))

            topology_type = requested_topology_info_dict[index].display_tech
            logging.info("Topology Type: {}".format(topology_type))

            self.plug_mst_display('gfx_0', port_name, topology_type, xml_file_name, is_low_power=False)

            if topology_type == 'SST':
                s_port_name = port_name_list[index + 1]
                s_xml_file_name = requested_topology_info_dict[index + 1].path
                logging.info("Slave XML File Name: {}".format(s_xml_file_name))

                s_topology_type = requested_topology_info_dict[index + 1].display_tech
                logging.info("Slave Topology Type: {}".format(s_topology_type))

                self.plug_mst_display('gfx_0', s_port_name, s_topology_type, s_xml_file_name, False)
                index = index + 1

            index = index + 1

        return True



