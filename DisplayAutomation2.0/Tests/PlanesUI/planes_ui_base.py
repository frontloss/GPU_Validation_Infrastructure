########################################################################################################################
# @file         planes_ui_base.py
# @brief        The script consists of unittest setUp and tearDown classes for PlanesUI Tests.
#                   * Parse command line.
#                   * Plug and unplug of displays.
# @author       Gopikrishnan R
########################################################################################################################
import logging
import unittest
from collections import OrderedDict

from Libs.Core import enum, window_helper
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.test_base import TestBase

LINE_WIDTH = 64


##
# @brief    Contains setUp and tearDown functions for PlanesUI
class PlanesUIBase(TestBase):
    media_type = None
    scenario = None
    fps = None
    interval = None
    buffer = None
    depth = None
    cancel = None
    app = []
    feature = None
    iteration = None
    get_target_ids = None

    ##
    # @brief        Unittest Setup function
    # @return       None
    def setUp(self):
        logging.info("TEST STARTS HERE".center(LINE_WIDTH, "*"))
        self.custom_tags['-MEDIA_TYPE'] = ['FPS_23_976', 'FPS_24', 'FPS_25', 'FPS_29_970', 'FPS_30', 'FPS_59_940',
                                           'FPS_60', 'RES_4K', 'RES_5K', 'RES_8K']
        self.custom_tags['-SCENARIO'] = [
            # Basic
            'FULLSCREEN_AND_WINDOWED', 'FULLSCREEN_AND_WINDOWED_WITH_CHARMS', 'SNAPMODE', 'WINDOWED', 'OPEN_AND_CLOSE',
            'FULLSCREEN_AND_WINDOWED_PRESENTAT', 'MEDIA_FULLSCREEN_WITH_CAPTIONS'
            # UI app events
                                                 'DRAG', 'RESIZE', 'WINDOW_SWITCH', 'MIN_MAX', 'PLAY_PAUSE',
            # Concurrency
            'ASYNC_AND_MEDIA', '48Hz', 'HDR', 'PIPE_AND_PLANE_SCALAR',
            # Display Events
            'MODE_SWITCH', 'ROTATION', 'DISPLAY_SWITCH', 'HOTPLUG_UNPLUG', 'RESTART_DRIVER', 'POWER_EVENT_S3',
            'POWER_EVENT_S4', 'GENERATE_TDR',
            # Custom Events
            'PAUSE_VIDEO_S3_PLAY_VIDEO', 'PAUSE_VIDEO_CS_PLAY_VIDEO', 'PAUSE_VIDEO_S4_PLAY_VIDEO', 'AC_DC',
            'RR_MAX_MIN_MAX', 'FULLSCREEN_WINDOWED_FULLSCREEN'
            # Stress
                              'STRESS'
        ]
        self.custom_tags['-FPS'] = ['24', '30', '45', '100', '150', '500', '750', '900', '1000']
        self.custom_tags['-INTERVAL'] = None
        self.custom_tags['-BUFFER'] = None
        self.custom_tags['-APP'] = ['FLIPAT', 'MEDIA', 'CLASSICD3D', 'D3D12FULLSCREEN', 'PRESENTAT', 'YOUTUBE', 'VLC']
        self.custom_tags['-FEATURE'] = ['SFLIPQ', 'FULLFLIPQ', 'MPO', 'FLIPQ_HRR', 'FLIP']
        self.custom_tags['-ITERATION'] = None

        # PresentAt Related (FPS parameter will also be used, if 0 is used then panel RR will be the FPS)
        self.custom_tags['-DEPTH'] = None
        self.custom_tags['-CANCEL'] = None
        self.custom_tags['-REPORTINTERVAL'] = ["REPORT_ALL_FLIPS", "REPORT_ALTERNATE_FLIPS", "REPORT_MAX_QUEUE_SIZE"]
        self.custom_tags['-POSITION'] = ["FULLSCREEN", "LEFT_PANE", "RIGHT_PANE"]

        super().setUp()
        self.media_type = str(self.context_args.test.cmd_params.test_custom_tags['-MEDIA_TYPE'][0])
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags['-SCENARIO'][0])
        self.fps = self.context_args.test.cmd_params.test_custom_tags['-FPS'][0]
        self.interval = self.context_args.test.cmd_params.test_custom_tags['-INTERVAL'][0]
        self.buffer = self.context_args.test.cmd_params.test_custom_tags['-BUFFER'][0]
        self.depth = self.context_args.test.cmd_params.test_custom_tags['-DEPTH'][0]
        self.cancel = self.context_args.test.cmd_params.test_custom_tags['-CANCEL'][0]
        self.app = self.context_args.test.cmd_params.test_custom_tags['-APP']
        self.feature = str(self.context_args.test.cmd_params.test_custom_tags['-FEATURE'][0])
        self.iteration = self.context_args.test.cmd_params.test_custom_tags['-ITERATION'][0]
        self.target_id_list = []
        self.current_target_id_list = []

        for gfx_index, adapter in self.context_args.adapters.items():
            if adapter.platform == 'MTL' and self.feature == 'SFLIPQ':
                planes_ui_helper.disable_dc6v_enable_osflipq(True, gfx_index)

    ##
    # @brief            Get the list of target_ids for displays connected
    # @param[in]        include_inactive   : Flag to indicate whether active/all display to be included
    # @param[in]        include_lfp        : Flag to indicate whether internal display to be included
    # @return           target_id_list     : List of all target ids
    def get_target_id_list(self, include_inactive=False, include_lfp=None):
        target_id_list = []
        ##
        # fetch the display configuration of all the displays connected
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if (panel.is_active and not include_inactive) or include_inactive:
                    if include_lfp is None or panel.is_lfp == include_lfp:
                        target_id_list.append(panel.target_id)

        return target_id_list

    ##
    # @brief            Get the dictionary having key values as targetid:(gfx_index,panel)
    # @return           adapter_tid_dict
    def get_tid_adapter_dict(self):
        adapter_tid_dict = OrderedDict()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    adapter_tid_dict[panel.target_id] = (port, gfx_index)
        return adapter_tid_dict

    ##
    # @brief        unittest tearDown function
    # @return       None
    def tearDown(self):
        window_helper.close_media_player()
        window_helper.close_dx_apps()
        window_helper.close_browser()
        if 'YOUTUBE' in self.app:
            planes_ui_helper.enable_disable_auto_detect_proxy(planes_ui_helper.RegistryStatus.DISABLE)
            planes_ui_helper.enable_disable_first_run_experience(planes_ui_helper.RegistryStatus.DISABLE)
        if 'VLC' in self.app:
            planes_ui_helper.enable_disable_auto_detect_proxy(planes_ui_helper.RegistryStatus.DISABLE)
        for gfx_index, adapter in self.context_args.adapters.items():
            if adapter.platform == 'MTL' and self.feature == 'SFLIPQ':
                planes_ui_helper.disable_dc6v_enable_osflipq(False, gfx_index)

        logging.info("Apply native mode with Zero Rotation")
        target_id_list = self.get_target_id_list(include_inactive=True, include_lfp=True)
        ##
        # fetch all the modes supported by the display in target_id_list
        if target_id_list:
            supported_modes = self.config.get_all_supported_modes(target_id_list)
            for key, values in supported_modes.items():
                mode = values[0]

                mode.rotation = enum.ROTATE_0
                # Apply Native mode with zero rotation
                self.config.set_display_mode([mode])
                logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                    mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
            logging.info("TEST ENDS HERE".center(LINE_WIDTH, "*"))
        super().tearDown()


if __name__ == '__main__':
    unittest.main()