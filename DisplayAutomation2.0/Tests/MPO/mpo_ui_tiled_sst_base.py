########################################################################################################################
# @file         mpo_ui_tiled_sst_base.py
# @brief        The script implements unittest default functions for setUp and tearDown that will be used by MPO test
#               scripts.
# @author       Shetty,Anjali N
########################################################################################################################
import logging
import os
import unittest

from Libs.Core import window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.system_utility import SystemUtility
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_context
from Tests.Display_Port.DP_Tiled import display_port_base
from Tests.MPO import mpo_ui_helper

##
# @brief    Contains unittest default functions for setUp and tearDown function
class MPOUITiledSSTBase(unittest.TestCase):
    config = DisplayConfiguration()
    display_port = DisplayPort()
    mpo_helper = mpo_ui_helper.MPOUIHelper()
    sst_base = display_port_base.DisplayPortBase()
    system_utility = SystemUtility()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

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

        self.machine_info = SystemInfo()
        self.gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        for i in range(len(self.gfx_display_hwinfo)):
            self.sst_base.platform_list.append(str(self.gfx_display_hwinfo[i].DisplayAdapterName).upper())
            self.sst_base.adapter_list_to_verify.append(self.gfx_display_hwinfo[i].gfxIndex)
        if len(self.sst_base.platform_list) > 1:
            self.sst_base.ma_flag = True

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

        enumerated_displays = self.config.get_enumerated_display_info()
        ##
        # is_internal_display_connected() tells whether an internal display is connected or not.
        internal_display_list = self.config.get_internal_display_list(enumerated_displays)
        if enumerated_displays.Count >= 2 and len(internal_display_list) != 0:
            ##
            # unplug tiled display
            self.sst_base.tiled_display_helper("Unplug")

        logging.info("****************TEST ENDS HERE********************************")


if __name__ == '__main__':
    unittest.main()
