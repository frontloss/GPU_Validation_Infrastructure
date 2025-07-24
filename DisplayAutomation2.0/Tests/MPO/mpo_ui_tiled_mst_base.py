########################################################################################################################
# @file         mpo_ui_tiled_mst_base.py
# @brief        The script implements unittest default functions for setUp and tearDown that will be used by MPO test
#               scripts.
# @author       Shetty,Anjali N
########################################################################################################################
import logging
import os
import unittest

from Libs.Core import enum, window_helper
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_context
from Tests.Display_Port.DP_MST import display_port_mst_base
from Tests.MPO import mpo_ui_helper

##
# @brief    Contains unittest default functions for setUp and tearDown function
class MPOUITiledMSTBase(unittest.TestCase):
    display_config = display_config.DisplayConfiguration()
    display_port = DisplayPort()
    mst_base = display_port_mst_base.DisplayPortMSTBase()
    mpo_helper = mpo_ui_helper.MPOUIHelper()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        ##
        # Parse command line
        self.mst_base.process_cmdline()

        ##
        # Get platform and OS details
        self.mpo_helper.get_platform_os()

        ##
        # 19x10 media playback
        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")

        ##
        # 4k media playback
        self.media_4k_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_3840_2160_avc.mp4")

        ##
        # Make sure media is not enabled at the beginning of the test
        window_helper.close_media_player()

        ##
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
                    else:
                        logging.info("Unplug of simulated %s display successful" % display_port)

        ##
        # Contains all free port list
        self.free_port_list = display_config.get_free_ports()
        logging.info('FREE PORT LIST: {}'.format(self.free_port_list))

        ##
        # Number of displays before the test starts
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(enumerated_displays.to_string())
        self.mst_base.number_of_displays_before_test = enumerated_displays.Count

        ##
        # get all internal display list
        internal_display_list = self.display_config.get_internal_display_list(enumerated_displays)
        if len(internal_display_list) != 0:
            for i in range(len(internal_display_list)):
                self.mst_base.internal_display_target_id_list.append(internal_display_list[i][0])
            logging.info("Internal display ID = %s" % self.mst_base.internal_display_target_id_list)
        else:
            logging.info("No internal display detected")

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        ##
        # Close the media player if not closed in the test.
        window_helper.close_media_player()

        ##
        # Close 3D application if not closed as part of test.
        if self.mpo_helper.app3d is not None:
            self.mpo_helper.app3d.close_app()

        self.mst_base.env_cleanup()

        logging.info("****************TEST ENDS HERE********************************")


if __name__ == '__main__':
    unittest.main()
