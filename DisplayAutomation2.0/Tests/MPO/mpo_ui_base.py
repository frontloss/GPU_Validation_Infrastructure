########################################################################################################################
# @file         mpo_ui_base.py
# @brief        The script implements unittest default functions for setUp and tearDown that will be used by MPO test
#               scripts.
# @author       Ilamparithi Mahendran , Balasubramanyam,Smitha
########################################################################################################################

import logging
import os
import sys
import unittest

from Libs.Core import cmd_parser, display_utility, enum, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Tests.MPO import mpo_ui_helper


##
# @brief    Contains unittest default functions for setUp and tearDown function
class MPOUIBase(unittest.TestCase):
    connected_list = []
    mytags = ['-expected_pixelformat', '-check_crc', '-scenario', '-fps']
    platform = None
    target_id = None
    config = DisplayConfiguration()
    wm = DisplayWatermark()
    system_utility = SystemUtility()
    machine_info = SystemInfo()
    mpo_helper = mpo_ui_helper.MPOUIHelper()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        ##
        # Get platform and OS details
        self.mpo_helper.get_platform_os()

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.mytags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Get the machine info
        system_utility = SystemUtility()
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.os_info = self.machine_info.get_os_info()

        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")
        self.media_4k_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_3840_2160_avc.mp4")
        window_helper.close_browser()
        window_helper.close_media_player()
        window_helper.kill_process_by_name("Maps.exe")
        self.under_run_status = UnderRunStatus()
        self.under_run_status.clear_underrun_registry()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        status = False
        system_utility = SystemUtility()
        window_helper.close_browser()
        window_helper.close_media_player()
        window_helper.kill_process_by_name("Maps.exe")

        if self.mpo_helper.app3d is not None:
            self.mpo_helper.app3d.close_app()

        if self.under_run_status.verify_underrun() is True:
            logging.error("Underrun seen in the test")

        ##
        # Unplugging all external displays
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)

        ##
        # Fetching list of eDP's attached to the DUT
        display_list = self.config.get_internal_display_list(self.enumerated_displays)

        ##
        # Update the eDP Resolution and RR back to default in case of any changes
        for display in display_list:
            target_id = display[0]
            native_mode = self.config.get_native_mode(target_id)
            if native_mode is not None:
                edid_hzres = native_mode.hActive
                edid_vtres = native_mode.vActive
                edid_refreshrate = native_mode.refreshRate

                supported_modes = self.config.get_all_supported_modes([target_id])
                for key, values in supported_modes.items():
                    for mode in values:
                        if mode.HzRes == edid_hzres and mode.VtRes == edid_vtres and mode.refreshRate == edid_refreshrate \
                                and mode.scaling == enum.MDS:
                            status = self.config.set_display_mode([mode])
                            logging.info(self.mpo_helper.getStepInfo() + "Applied Display mode: %s" %
                                         mode.to_string(self.enumerated_displays))
                if status:
                    logging.info("Successfully applied native mode")
                else:
                    logging.error("Failed to apply native mode")
            else:
                logging.error(f"Failed to get native mode for {target_id}")

        logging.info("****************TEST ENDS HERE********************************")


if __name__ == '__main__':
    unittest.main()
