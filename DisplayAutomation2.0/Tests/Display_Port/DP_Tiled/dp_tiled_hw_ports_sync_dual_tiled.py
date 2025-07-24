#######################################################################################################################
# @file         dp_tiled_hw_ports_sync_dual_tiled.py
# @brief        This test verifies dual Tiled.
# @details      This test applies 8k on both the tiled displays and verifies port sync.
# @author       Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledHWPortSyncDualTiled(DisplayPortBase):

    ##
    # @brief        This test plugs required displays, set config, applies max mode.
    # @return       None
    def runTest(self):
        ##
        # Plug the Tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        self.plugged_target_ids = self.display_target_ids()
        logging.info("Target ids after tiled displays plug :%s" % self.plugged_target_ids)

        ##
        # get list of ports for tiled displays
        tiled_port_list = self.get_tiled_ports()
        if len(tiled_port_list) < 2:
            self.fail("This test needs 2 tiled displays connected")

        tiled_topology = eval("enum.%s" % (self.config))

        ##
        # set display configuration with topology as given in cmd line
        result = self.display_config.set_display_configuration_ex(tiled_topology, tiled_port_list)
        self.assertEquals(result, True, "Aborting the test as applying the display config failed.")

        ##
        # Apply 5K3K/8k4k resolution and check for applied mode
        self.apply_tiled_max_modes()

    ##
    # @brief        Return display port_name as a list.
    # @return       list of port_names
    def get_tiled_ports(self):
        tiled_target_ids = []

        for targetId in self.plugged_target_ids:
            tile_info = self.display_port.get_tiled_display_information(targetId)
            if tile_info.TiledStatus:
                tiled_target_ids.append(targetId)

        tiled_connected_ports = []

        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays is not None:
            for index in range(enumerated_displays.Count):
                if enumerated_displays.ConnectedDisplays[index].TargetID in tiled_target_ids:
                    port_name = str(
                        CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
                    tiled_connected_ports.append(port_name)
        else:
            self.fail("get_enumerated_display_info returned None.")

        return tiled_connected_ports

    ##
    # @brief        plugs/unplugs the tiled display.
    # @param[in]    action: str
    #                    action for display i.e. plug/unplug etc.
    # @param[in]    low_power: Boolean
    #                    low_power True or false
    # @return       None
    def tiled_display_helper(self, action="Plug", low_power=False):
        action = action.upper()
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("[Test Issue]: Invalid plug action for tiled display. Exiting .....")
            self.fail()
        ##
        # separate the master and slave tile information given through the cmd line
        dp_panel1_master = self.ma_dp_panels[0][0]
        dp_panel1_slave = self.ma_dp_panels[0][1]
        dp_panel2_master = self.ma_dp_panels[0][2]
        dp_panel2_slave = self.ma_dp_panels[0][3]

        ##
        # The first DP display mentioned dp_panels in the cmd line will be the port type for
        # Master Tile Display which will have the Master.EDID and the DPCD passed
        # along with it. Hence, setting the values in master_panel & slave_panel
        # according to the index of the cmd line dictionary.
        if dp_panel1_master['index'] == 1:
            master_panel1 = dp_panel1_master
            slave_panel1 = dp_panel1_slave
        else:
            master_panel1 = dp_panel1_slave
            slave_panel1 = dp_panel1_master

        if dp_panel2_master['index'] == 3:
            master_panel2 = dp_panel2_master
            slave_panel2 = dp_panel2_slave
        else:
            master_panel2 = dp_panel2_slave
            slave_panel2 = dp_panel2_master

        ##
        # Accessing EDID and DPCD parameter list
        master_tile_edid1 = master_panel1['edid_name']
        slave_tile_edid1 = slave_panel1['edid_name']
        master_tile_dpcd1 = master_panel1['dpcd_name']
        slave_tile_dpcd1 = slave_panel1['dpcd_name']
        master_tile_edid2 = master_panel2['edid_name']
        slave_tile_edid2 = slave_panel2['edid_name']
        master_tile_dpcd2 = master_panel2['dpcd_name']
        slave_tile_dpcd2 = slave_panel2['dpcd_name']

        if master_tile_dpcd1:
            master_tile_dpcd1 = master_panel1['dpcd_name']
        else:
            master_tile_dpcd1 = slave_tile_dpcd1

        if master_tile_dpcd2:
            master_tile_dpcd2 = master_panel2['dpcd_name']
        else:
            master_tile_dpcd2 = slave_tile_dpcd2

        ##
        # Check for valid EDID and DPCD names passed through cmd line
        if (master_tile_edid1 not in self.valid_edid_list) or (slave_tile_edid1 not in self.valid_edid_list) or \
                (master_tile_dpcd1 not in self.valid_dpcd_list) or (master_tile_edid2 not in self.valid_edid_list) or \
                (slave_tile_edid2 not in self.valid_edid_list) or (master_tile_dpcd2 not in self.valid_dpcd_list):
            logging.error("[Test Issue]: Invalid Master/Slave/DPCD files given through command line. Exiting ...")
            self.fail()

        master_plug = slave_plug = False
        if action == "PLUG":
            master_plug = slave_plug = True
        elif action == "UNPLUG":
            master_plug = slave_plug = False

        ##
        # call plug_unplug_tiled_display() from DisplayPort DLL to plug the tiled display
        result1 = self.display_port.plug_unplug_tiled_display(master_plug, slave_plug, master_panel1['connector_port'],
                                                              slave_panel1['connector_port'], master_tile_edid1,
                                                              slave_tile_edid1, master_tile_dpcd1, low_power)
        time.sleep(5)
        self.check_plug_unplug_status(action, result1, master_plug, slave_plug)

        result2 = self.display_port.plug_unplug_tiled_display(master_plug, slave_plug, master_panel2['connector_port'],
                                                              slave_panel2['connector_port'], master_tile_edid2,
                                                              slave_tile_edid2, master_tile_dpcd2, low_power)
        time.sleep(5)
        self.check_plug_unplug_status(action, result2, master_plug, slave_plug)


    ##
    # @brief        Checks for plug/unplug tiled display failure and log information accordingly
    # @param[in]    action: str
    #                    action for display i.e. plug/unplug etc.
    # @param[in]    result: Boolean
    #                    result True or false
    # @param[in]    master_plug: Boolean
    #                    master_plug True or false
    # @param[in]    slave_plug: Boolean
    #                    slave_plug True or false
    # @param[in]    low_power: Boolean
    #                    low_power True or false
    # @return       None
    def check_plug_unplug_status(self, action, result, master_plug, slave_plug, low_power="False"):
        if (action == "PLUG") and (result is False):
            logging.error("Hotplug of Tiled Displays failed. Exiting .....")
            self.fail()
        elif (action == "UNPLUG") and (result is False):
            logging.error("Unplug of Tiled Displays failed. Exiting .....")
            self.fail()
        elif action == "UNPLUG" and (result is True) and (master_plug is False) and (slave_plug is False) and (
                low_power is False):
            logging.info("Unplug of Tiled Displays Successful when System is active")
        elif action == "PLUG" and (result is True) and (master_plug is True) and (slave_plug is True) and (
                low_power is False):
            logging.info("Hotplug of Tiled Displays Successful when System is active")

   ##
    # @brief Cleans up the test
    # @return - None
    def tearDown(self):
        status = self.display_port.uninitialize_sdk()
        if status is True:
            logging.info("Uninitialization of CUI SDK Successful in TearDown().")
        else:
            logging.error("Uninitialization of CUI SDK Failed in TearDown().")

        ##
        # Unplug of tiled displays
        self.tiled_display_helper(action="UNPLUG")
        time.sleep(Delay_5_Secs)
        ##
        # get target ids after tiled display unplugged
        post_unplug_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % post_unplug_target_ids)

        logging.info("Test Clean Up")

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
