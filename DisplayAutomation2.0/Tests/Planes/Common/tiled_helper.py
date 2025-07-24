########################################################################################################################
# @file         tiled_helper.py
# @brief        This script contains helper functions that will be used by MPO test scripts to process the command line.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import re

from Libs.Core import cmd_parser, enum
from Libs.Core import display_utility
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config import DisplayConfiguration
from Tests.Display_Port.DP_Tiled import display_port_base

DP_pattern = re.compile('DP_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))

##
# @brief    Contains function to process the commandline for MPO test scripts
class TiledDisplayHelper(object):
    config = DisplayConfiguration()
    sst_base = display_port_base.DisplayPortBase()


    ##
    # @brief            To process command line
    # @param[in]        cmd_line_param; command line parameters
    # @return           void
    def process_command_line(self, cmd_line_param):
        ##
        # Get the DP panel details from the command line
        for key, value in cmd_line_param.items():
            if DP_pattern.match(key) is not None:
                self.sst_base.dp_panels.append(value)

        if len(self.sst_base.dp_panels) < 2:
            logging.error("[Test Issue]: Insufficient DP panels for tiled display.")
            raise Exception("[Test Issue]: Insufficient DP panels for tiled display.")

        pre_plug_displays = self.config.get_enumerated_display_info()

        ##
        # Tiled specific command lines not provided, checking for the wired tile config
        if pre_plug_displays is not None:
            for index in range(pre_plug_displays.Count):
                target_id = pre_plug_displays.ConnectedDisplays[index].TargetID
                conn_port_type = str(CONNECTOR_PORT_TYPE(pre_plug_displays.ConnectedDisplays[index].ConnectorNPortType))
                if display_utility.get_vbt_panel_type(conn_port_type, 'gfx_0') in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    continue
                if conn_port_type in self.sst_base.dp_ports_list:
                    tiled_display_info = self.sst_base.display_port.get_tiled_display_information(target_id)

                    if tiled_display_info.TiledStatus == 1:
                        logging.info("Tiled Display is already plugged.")
                        self.sst_base.tile_target_id = pre_plug_displays.ConnectedDisplays[index].TargetID
                        self.sst_base.tile_config_found = True
                    else:
                        logging.error("[Test Issue]: Tile display configuration not found.")
                        raise Exception("[Test Issue]: Tile display configuration not found.")
                else:
                    logging.error("[Test Issue]: Tile display configuration not found.")
                    raise Exception("[Test Issue]: Tile display configuration not found.")
