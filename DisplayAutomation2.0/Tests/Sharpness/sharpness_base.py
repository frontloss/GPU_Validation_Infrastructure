########################################################################################################################
# @file         sharpness_base.py
# @brief        The script consists of unittest setup and tear down classes for Sharpness.
# @author       Prateek Joshi
########################################################################################################################

import logging
import unittest

from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Tests.Sharpness import sharpness_helper
from Tests.test_base import TestBase
MAX_LINE_WIDTH = 64


##
# @brief    Contains unittest setUp and tearDown functions to parse the command line, plug and unplug the displays.
class SharpnessBase(TestBase):
    connected_list = []
    display_config = DisplayConfiguration()
    filter, strength, scenario = None, None, None
    resolution = None
    hz_res, vt_res = None, None

    ##
    # @brief        Unittest Setup function
    # @return       None
    def setUp(self):
        logging.info(" TEST STARTS ".center(MAX_LINE_WIDTH, "*"))
        self.custom_tags["-FILTER"] = ['ADAPTIVE', 'NON_ADAPTIVE']
        self.custom_tags["-STRENGTH"] = ['25', '50', '75', '100', '-30', '150']
        self.custom_tags["-MEDIA_TYPE"] = ['RES_4K', 'FPS_60']
        self.custom_tags['-SCENARIO'] = ['FULLSCREEN', 'WINDOWED', 'OPEN_AND_CLOSE', 'PIPE_AND_PLANE_SCALAR', 'HDR',
                                         'INTENSITY']
        super().setUp()
        self.filter_type = str(self.context_args.test.cmd_params.test_custom_tags["-FILTER"][0])
        self.strength = str(self.context_args.test.cmd_params.test_custom_tags["-STRENGTH"][0])
        self.media_type = str(self.context_args.test.cmd_params.test_custom_tags["-MEDIA_TYPE"][0])
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        logging.debug(f"Enabling Sharpness with Intensity - {self.strength}, Filter Type - "
                      f"{self.filter_type}")
        self.target_id_list = []
        include_inactive = False

        ##
        # Start ETL capture
        if sharpness_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Feature Enabling through IGCL
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_helper.enable_disable_feature_igcl(self.strength, panel, self.filter_type,
                                                                sharpness_helper.Status.ENABLE) is False:
                    self.fail(f"FAIL: Sharpness feature is not enabled via IGCL")
                logging.info(f"PASS: Sharpness feature is enabled via IGCL")
                mode = self.display_config.get_current_mode(panel.target_id)
                self.hz_res, self.vt_res = mode.HzRes, mode.VtRes

        logging.info("Apply native mode with Zero Rotation")
        ##
        # fetch the display configuration of all the displays connected
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if (panel.is_active and not include_inactive) or include_inactive:
                    self.target_id_list.append(panel.target_id)
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.display_config.get_all_supported_modes(self.target_id_list)
        for key, values in supported_modes.items():
            mode = values[0]
            mode.rotation = enum.ROTATE_0
            # Apply Native mode with zero rotation
            self.display_config.set_display_mode([mode], virtual_mode_set_aware= False, force_modeset=True)
            logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
            self.resolution = str(mode.HzRes) + 'x' + str(mode.VtRes)

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
    # @brief        unittest TearDown function
    # @return       None
    def tearDown(self):
        logging.info(" TEST ENDS ".center(MAX_LINE_WIDTH, "*"))
        logging.debug(f"Disabling Sharpness with current Intensity - {self.strength}, Filter Type - "
                      f"{self.filter_type}")
        ##
        # Feature Disabling through IGCL
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_helper.enable_disable_feature_igcl(self.strength, panel, self.filter_type,
                                                                sharpness_helper.Status.DISABLE) is False:
                    self.fail(f"FAIL: Sharpness feature is not disabled via IGCL")
                logging.info(f"PASS: Sharpness feature is disabled via IGCL")
        super().tearDown()


sharpness_base = SharpnessBase()
if __name__ == '__main__':
    unittest.main()
