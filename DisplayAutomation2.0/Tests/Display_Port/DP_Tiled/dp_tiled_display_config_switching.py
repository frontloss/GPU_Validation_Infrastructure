#######################################################################################################################
# @file         dp_tiled_display_config_switching.py
# @brief        This test verifies display config.
# @details      Applies and verifies all the display configurations - SD, DDC, ED with one of the display as
#               5k/8k Tiled
#
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledDisplayConfigSwitching(DisplayPortBase):

    ##
    # @brief        sets configuration
    # @param[in]    topology: str
    #                    topology for display i.e. SINGLE/EXTENDED
    # @return       None
    def set_tiled_config(self, topology):
        ##
        # display_list[] is list of connector port type of the displays
        display_adapter_list = []
        ##
        # flag to tell whether plugged display is tiled or not
        tiled_flag = False
        ##
        # get tiled topology to be applied on tiled display
        tiled_topology = eval("enum.%s" % (topology))
        ##
        # get the enumerated displays from SystemUtility
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
                # Check for the count of displays connected
                if enumerated_displays.Count > 1:
                    ##
                    # if topology is 'SINGLE', display_list[] will have port type of tiled display only
                    if topology == 'SINGLE':
                        for index in range(enumerated_displays.Count):
                            display_info = ("%s" % (CONNECTOR_PORT_TYPE(
                                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))
                            gfx_index = enumerated_displays.ConnectedDisplays[
                                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                            display_adapter_list.append((display_info, gfx_index))
                        ##
                        # combination_list[] is a list of combination of display
                        combination_list = display_utility.get_possible_configs(display_adapter_list, True)
                        config_combination_list = combination_list['enum.SINGLE']
                    ##
                    # if topology is 'EXTENDED'/'CLONE', display_list[] will have port type of tiled and non-tiled display
                    else:
                        for index in range(enumerated_displays.Count):
                            display_info = ("%s" % (CONNECTOR_PORT_TYPE(
                                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))
                            gfx_index = enumerated_displays.ConnectedDisplays[
                                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                            display_adapter_list.append((display_info, gfx_index))
                        ##
                        # combination_list[] is a list of combination of displays
                        combination_list = display_utility.get_possible_configs(display_adapter_list)

                        if topology == 'EXTENDED':
                            config_combination_list = combination_list['enum.EXTENDED']
                        elif topology == 'CLONE':
                            config_combination_list = combination_list['enum.CLONE']

                    each_combination_adapter_info_list = []
                    for each_combination in config_combination_list:
                        display_and_adapter_info_list = []
                        # each_combination items are in format of a Tuple (<display_port>, <gfx_index>) e.g. (dp_b, gfx_0),
                        # Extracting port and gfx index from this
                        for each_display in each_combination:
                            port = each_display[0]
                            gfx_index = each_display[1]
                            display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(port,
                                                                                                           gfx_index)
                            display_and_adapter_info_list.append(display_and_adapter_info)
                        each_combination_adapter_info_list.append(display_and_adapter_info_list)
                    ##
                    # set display configuration according to the topology
                    for current_config_list in range(len(each_combination_adapter_info_list)):
                        if self.display_config.set_display_configuration_ex(tiled_topology, each_combination_adapter_info_list[
                                current_config_list]):
                            logging.info("Set Display Configuration Success")
                            ##
                            # Check for CRC amd Underrun after setting the config on connected displays
                            self.verify_underrun_and_crc()
                        else:
                            logging.error("[Driver Issue]: Set Display Configuration Failed. Exiting .....")
                            # Gdhm bug reported in set_display_configuration_ex
                            self.fail()
                else:
                    logging.error("[Test Issue]: Not sufficient displays to apply configuration. Exiting ....")
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

    ##
    # @brief        This test method plugs the required displays, set display configs and verifies applied configs.
    # @return       None
    def runTest(self):
        ##
        # plug tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set display configuration with topology as SINGLE
        if not self.ma_flag:
            self.set_tiled_config('SINGLE')
        ##
        # set display configuration with topology as EXTENDED
        self.set_tiled_config('EXTENDED')
        ##
        # set display configuration with topology as CLONE
        self.set_tiled_config('CLONE')
        ##
        # check for platform whether ICL or not
        if 'ICL' in self.platform_list:
            ##
            # set display configuration with topology as TRICLONE,TRIEXTENDED 
            self.set_tiled_config('TRICLONE')
            self.set_tiled_config('TRIEXTENDED')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
