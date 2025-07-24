########################################################################################################################
# @file         watermark_ui_base.py
# @brief        The script consists of unittest setUp and tearDown classes for WatermarkUI Tests.
#                   * Parse command line.
#                   * Plug and unplug of displays.
# @author       Gopikrishnan R
########################################################################################################################
import logging
import unittest
from collections import OrderedDict

from Tests.test_base import TestBase
from Libs.Core import enum
from threading import Thread
from Libs.Feature.display_watermark.watermark import DisplayWatermark
import time

LINE_WIDTH = 64


##
# @brief    Contains setUp and tearDown functions for WatermarkUI
class WatermarkUIBase(TestBase):
    media_type = None
    scenario = None
    fps = None
    interval = None
    buffer = None
    depth = None
    cancel = None
    app = []
    feature = None
    get_target_ids = None
    wm = DisplayWatermark()
    test_end = False

    ##
    # @brief        Unittest Setup function
    # @return       None
    def setUp(self):
        logging.info("TEST STARTS HERE".center(LINE_WIDTH, "*"))
        self.custom_tags['-MEDIA_TYPE'] = ['FPS_23_976', 'FPS_24', 'FPS_25', 'FPS_29_970', 'FPS_30', 'FPS_59_940',
                                           'FPS_60', 'RES_4K', 'RES_5K', 'RES_8K']
        self.custom_tags['-SCENARIO'] = [
            # Display Events
            'MODE_SWITCH', 'ROTATION', 'DISPLAY_SWITCH', 'HOTPLUG_UNPLUG', 'RESTART_DRIVER', 'POWER_EVENT_S3',
            'POWER_EVENT_S4', 'GENERATE_TDR',
        ]
        self.custom_tags['-FPS'] = ['24', '30', '45', '100', '150', '500', '750', '900', '1000']
        self.custom_tags['-INTERVAL'] = None
        self.custom_tags['-BUFFER'] = None
        self.custom_tags['-APP'] = ['FLIPAT', 'MEDIA', 'CLASSICD3D', 'D3D12FULLSCREEN', 'PRESENTAT']

        super().setUp()
        self.media_type = str(self.context_args.test.cmd_params.test_custom_tags['-MEDIA_TYPE'][0])
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags['-SCENARIO'][0])
        self.fps = self.context_args.test.cmd_params.test_custom_tags['-FPS'][0]
        self.interval = self.context_args.test.cmd_params.test_custom_tags['-INTERVAL'][0]
        self.app.append(self.context_args.test.cmd_params.test_custom_tags['-APP'][0])
        self.target_id_list = []
        self.current_target_id_list = []

    ##
    # @brief            Get the list of target_ids for displays connected
    # @param[in]        include_inactive   : Flag to indicate whether active/all display to be included
    # @return           target_id_list     : List of all target ids
    def get_target_id_list(self, include_inactive=False):
        target_id_list = []
        ##
        # fetch the display configuration of all the displays connected
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if (panel.is_active and not include_inactive) or include_inactive:
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
        self.test_end = True
        logging.info("TEST ENDS HERE".center(LINE_WIDTH, "*"))
        logging.info("Apply native mode with Zero Rotation")
        target_id_list = self.get_target_id_list(include_inactive=True)
        ##
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.config.get_all_supported_modes(target_id_list)
        for key, values in supported_modes.items():
            mode = values[0]

            mode.rotation = enum.ROTATE_0
            # Apply Native mode with zero rotation
            self.config.set_display_mode([mode])
            logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
