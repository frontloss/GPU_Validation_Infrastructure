#######################################################################################################################
# @file         dp_tiled_modeset.py
# @brief        This test applies modes on tiled displays.
# @details      This test apply all modes on all the connected displays.
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledModeSet(DisplayPortBase):
    tiled_edid_hz_res = None
    tiled_edid_vt_res = None

    ##
    # @brief        Set display modes
    # @param[in]    supported_modes_dict: Dictionary
    #                    supported_modes_dict is a dictionary of supported modes
    # @return       None
    def set_display_mode(self, supported_modes_dict):
        for target_id, mode_list in supported_modes_dict.items():
            s_mode_list = sorted(mode_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
            modes_to_apply = (s_mode_list[0], s_mode_list[len(s_mode_list) // 2], s_mode_list[-1])

            for mode in modes_to_apply:
                ##
                # Apply the mode having the maximum resolution and different refresh rates
                modes_flag = self.display_config.set_display_mode([mode])
                if modes_flag is False:
                    logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                    ##
                    # Gdhm bug reporting handled in display_config.set_display_mode
                    self.fail()
                ##
                # Check for CRC amd Under-run
                self.verify_underrun_and_crc()

    ##
    # @brief        sets mode and checks for port sync enable.
    # @return       None
    def performTest(self):
        ##
        # Get the current display config from DisplayConfig
        config = self.display_config.get_current_display_configuration()

        for index in range(config.numberOfDisplays):
            tiled_info_list = []
            tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index].displayAndAdapterInfo)
            tiled_info_list.append(config.displayPathInfo[index].displayAndAdapterInfo)
            ##
            # supported_modes_tiled[] is a list of modes supported by the tiled display
            supported_mode_dict = self.display_config.get_all_supported_modes(tiled_info_list)
            ##
            # Check for tiled status
            if tile_info.TiledStatus is True:
                ##
                # tile_modes_list[] is a list of modes supported by the tiled display
                if self.ma_flag:
                    tile_modes_list = supported_mode_dict[(config.displayPathInfo[
                            index].DisplayAndAdapterInfo.adapterInfo.gfxIndex, config.displayPathInfo[index].targetId)]
                else:
                    tile_modes_list = supported_mode_dict[config.displayPathInfo[index].targetId]
                ##
                # tile_maximum_resolution is the maximum resolution of the tiled display taken form the tile_modes_list
                tile_modes_list = sorted(tile_modes_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                tile_maximum_resolution = tile_modes_list[len(tile_modes_list) - 1]
                ##
                # Check whether the resolution from list of modes is equal to the resolution from the tiled edid
                self.tiled_edid_hz_res = tile_info.HzRes
                self.tiled_edid_vt_res = tile_info.VtRes

                is_tiled_max_mode_enumerated = (self.tiled_edid_hz_res == tile_maximum_resolution.HzRes)
                is_tiled_max_mode_enumerated &= (self.tiled_edid_vt_res == tile_maximum_resolution.VtRes)

                if is_tiled_max_mode_enumerated or self.config == 'CLONE':

                    self.set_display_mode(supported_mode_dict)
                    ##
                    # Last applied mode will be a max mode, port sync is verified after that
                    if self.config != 'CLONE':
                        flag_list = self.verify_port_sync_enable()
                        for index in range(len(flag_list)):
                            adapter = "gfx_" + str(index)
                            if flag_list[index] is True:
                                logging.info("Port Sync enabled for {}".format(adapter))
                            else:
                                logging.error("[Driver Issue]: Port Sync is not enabled for {}. Exiting .....".format(adapter))
                                gdhm.report_bug(
                                    title="[Interfaces][DP_Tiled]  Driver failed to enable port sync",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail()

                else:
                    logging.error(
                        "[Driver Issue]: Modes enumerated by the Graphics driver not matching with modes in EDID. Exiting...")
                    gdhm.report_bug(
                        title="[Interfaces][DP_Tiled] Driver enumerated modes and edid modes are not matching",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail()
            elif tile_info.TiledStatus is False:
                self.set_display_mode(supported_mode_dict)

    ##
    # @brief        sets configuration and modes.
    # @param[in]    topology: str
    #                    topology for display i.e. SINGLE/EXTENDED
    # @return       None
    def set_tiled_config_and_modes(self, topology):
        ##
        # display_list[] is list of displays
        display_adapter_list = []
        ##
        # get tiled topology to be applied on tiled display
        tiled_topology = eval("enum.%s" % topology)

        enumerated_displays = self.display_config.get_enumerated_display_info()

        for index in range(enumerated_displays.Count):
            display_info = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            gfx_index = enumerated_displays.ConnectedDisplays[
                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            display_adapter_list.append((display_info, gfx_index))

        combination_list = display_utility.get_possible_configs(display_adapter_list, True)
        if topology == 'SINGLE':
            config_combination_list = combination_list['enum.SINGLE']
        elif topology == 'EXTENDED' and enumerated_displays.Count > 1:
            config_combination_list = combination_list['enum.EXTENDED']
        elif topology == 'CLONE' and enumerated_displays.Count > 1:
            config_combination_list = combination_list['enum.CLONE']
        else:
            logging.error(
                "[Test Issue]: Invalid display configuration or number of display count insufficient. Exiting .....")
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
                # Apply all modes to tiled and non-tiled displays connected
                self.performTest()
            else:
                logging.error("[Driver Issue]: Set Display Configuration Failed. Exiting ....")
                ##
                # Gdhm bug reported in set_display_configuration_ex
                self.fail()


    ##
    # @brief        This test plugs required displays, set config and perform test.
    # @return       None
    def runTest(self):
        # Plug the tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # Get plugged target ids
        self.plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % self.plugged_target_ids)
        ##
        # Set tiled mode and config from the command line
        self.set_tiled_config_and_modes(self.config)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
