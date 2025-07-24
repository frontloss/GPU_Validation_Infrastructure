#######################################################################################################################
# @file         dp_tiled_cursor.py
# @brief        This test verifies cursor movement.
# @details      This test checks whether SW Cursor is able to move from tiled to non-tiled display
#               and within master/slave tiles.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledCursor(DisplayPortBase):
    plugged_target_ids = []
    display_list = []
    prim_display = None
    sec_display = None

    ##
    # @brief        sets configuration and modes
    # @param[in]    topology: str
    #                    topology for display i.e. SINGLE/EXTENDED
    # @return       None
    def set_config_and_modes(self, topology):
        ##
        # flag to tell whether plugged display is tiled or not
        tiled_flag = False
        display_info = None
        ##
        # get tiled topology to be applied on tiled display
        tiled_topology = eval("enum.%s" % (topology))
        ##
        # get the enumerated displays fro, SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_all_display_configuration()
        for index in range(config.numberOfDisplays):
            tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index].targetId)
            ##
            # check for tiled status
            if tile_info.TiledStatus is True:
                tiled_flag = True
                ##
                # if topology is 'SINGLE', display_list[] will have port type of tiled display only
                if topology == 'SINGLE':
                    for index in range(enumerated_displays.Count):
                        tile_info = self.display_port.get_tiled_display_information(self.plugged_target_ids[index])
                        ##
                        # check for tiled status and append the port type to display_list[]
                        if tile_info.TiledStatus is True:
                            display_info = str(
                                CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
                            self.display_list.append(display_info)
                    ##
                    # combination_list[] is a list of combination of display
                    combination_list = display_utility.get_possible_configs(self.display_list, True)
                    config_combination_list = combination_list['enum.SINGLE']
                    self.prim_display = config_combination_list[0][0]
                ##
                # if topology is 'EXTENDED', display_list[] will have port type of tiled and non-tiled display
                else:
                    for index in range(enumerated_displays.Count):
                        display_info = str(
                            CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
                        display_target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                        tile_info = self.display_port.get_tiled_display_information(display_target_id)
                        if tile_info.TiledStatus is True:
                            tiled_display_info = str(
                                CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
                            self.display_list.append(tiled_display_info)
                        else:
                            self.display_list.append(display_info)
                    ##
                    # Setting Tiled Display as Primary and eDP(DP_A) as secondary
                    if self.display_list[0] == 'DP_A':
                        self.display_list[0], self.display_list[-1] = self.display_list[-1], self.display_list[0]
                    ##
                    # combination_list[] is a list of combination of displays
                    combination_list = display_utility.get_possible_configs(self.display_list)
                    if topology == 'EXTENDED' and enumerated_displays.Count > 1:
                        config_combination_list = combination_list['enum.EXTENDED']
                        self.prim_display = config_combination_list[0][0]
                        self.sec_display = config_combination_list[0][1]
                        config_combination_list = [config_combination_list[0]]
                    elif topology == 'CLONE':
                        logging.error("[Test Issue]: Config CLONE cannot be applied in this test. Exiting .....")
                        self.fail()
                    else:
                        logging.error(
                            "[Test Issue]: Either not a valid configuration or number of display count insufficient. Exiting .....")
                        self.fail()
                ##
                # set display configuration according to the topology
                for current_config_list in range(len(config_combination_list)):
                    if self.display_config.set_display_configuration_ex(tiled_topology,
                                                                        config_combination_list[current_config_list]):
                        logging.info("Set Display Configuration Success")
                        ##
                        # Check for CRC amd Underrun after setting the config
                        self.verify_underrun_and_crc()
                        ##
                        # Apply 5K3K/8k4k resolution and check for port sync enable
                        self.apply_tiled_max_modes()
                    else:
                        logging.error("Set Display Configuration Failed. Exiting .....")
                        # Gdhm bug reported in set_display_configuration_ex
                        self.fail()
        ##
        # check for tiled flag
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

    ##
    # @brief        This test method plugs the required displays, set display config and mode
    #               and verifies SW cursor movement on tiled display.
    # @return       None
    def runTest(self):
        display1 = None
        display2 = None
        ##
        # plug tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get plugged target ids
        self.plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % self.plugged_target_ids)
        ##
        # set tiled mode and config from the command line
        self.set_config_and_modes(self.config)
        ##
        # get the enumerated displays information from SystemUtility
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        config = self.display_config.get_current_display_configuration()
        for index in range(config.numberOfDisplays):
            ##
            # if config == 'EXTENDED' then display1 = DP_A and display2 = DP_B/DP_C/DP_D
            if self.config == "EXTENDED":
                display1, display2 = self.display_list
            ##
            # if config == 'SINGLE' then display1 = Master Tile Port and display2 = Slave Tile Port
            else:
                tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index].targetId)
                ##
                # check for tiled status
                if tile_info.TiledStatus is True:
                    ##
                    # getting the master tiled port
                    tiled_port = CONNECTOR_PORT_TYPE(
                        self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
                    master_panel = self.ma_dp_panels[0][0]
                    slave_panel = self.ma_dp_panels[0][1]
                    master_port_id = master_panel['connector_port']
                    slave_port_id = slave_panel['connector_port']
                    ##
                    # display1 will be port type of master tile
                    display1 = tiled_port
                    ##
                    # display2 will be port type of slave tile
                    if master_port_id == tiled_port:
                        display2 = slave_port_id
                    else:
                        display2 = master_port_id

        if self.config == 'EXTENDED':
            ##
            # Call move_mouse_cursor() from window_helper to move the cursor randomly
            # between the connected displays. This API needs a rework for restricting cursor
            # movement within the boundary of the display
            '''
            mouse_flag = window_helper.move_mouse_cursor(display1, display2)
            if mouse_flag:
                logging.info("move_mouse_cursor Success")
            else:
                logging.error("move_mouse_cursor Failed. Exiting ...")
                self.fail()
            '''
            ##
            # Call tiled_move_cursor() from display_port_base to move the cursor randomly
            # between master and slave tiles
            self.tiled_move_cursor(display1, display2)
        else:
            ##
            # Call move_mouse_cursor() from window_helper to move the cursor randomly
            # between the connected displays. This API needs a rework for restricting cursor
            # movement within the boundary of the display
            '''
            mouse_flag = window_helper.move_mouse_cursor(display1, display1)
            if mouse_flag:
                logging.info("move_mouse_cursor Success")
            else:
                logging.error("move_mouse_cursor Failed. Exiting ...")
                self.fail()
            '''
            ##
            # Call tiled_move_cursor() from display_port_base to move the cursor randomly
            # between master and slave tiles. Here, we give master and slave port separately
            # as the function is capable of handling both.
            self.tiled_move_cursor(display1, display2)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
