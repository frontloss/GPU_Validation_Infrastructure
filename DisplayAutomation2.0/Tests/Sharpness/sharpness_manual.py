########################################################################################################################
# @file         sharpness_manual.py
# @brief        The script consists of unittest setup and tear down classes for Sharpness to enable/disable feature.
# @author       Prateek Joshi
########################################################################################################################

import logging
import unittest
import sys
from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Sharpness import sharpness_helper
from Tests.test_base import TestBase

MAX_LINE_WIDTH = 64


##
# @brief    Sharpness Manual helpers
class SharpnessManual(TestBase):
    sharpness_intensity = None
    sharpness_status = None
    filter_type = None

    ##
    # @brief        Unittest Setup function
    # @return       None
    def setUp(self):
        self.display_config = DisplayConfiguration()

        ##
        # Custom tag to parse sharpness parameters
        self.custom_tags["-INTENSITY"] = None
        self.custom_tags["-STATUS"] = None
        self.custom_tags["-FILTER_TYPE"] = None
        self.custom_tags["-H_RES"] = None
        self.custom_tags["-V_RES"] = None
        super().setUp()

        self.sharpness_intensity = int(self.context_args.test.cmd_params.test_custom_tags["-INTENSITY"][0])
        self.sharpness_status = str(self.context_args.test.cmd_params.test_custom_tags["-STATUS"][0])
        self.filter_type = str(self.context_args.test.cmd_params.test_custom_tags["-FILTER_TYPE"][0])
        self.hz_res = int(self.context_args.test.cmd_params.test_custom_tags["-H_RES"][0])
        self.vt_res = int(self.context_args.test.cmd_params.test_custom_tags["-V_RES"][0])

        if self.sharpness_status == "ENABLE":
            self.feature_status = sharpness_helper.Status.ENABLE
        elif self.sharpness_status == "DISABLE":
            self.feature_status = sharpness_helper.Status.DISABLE

    ##
    # @brief        RunTest function
    # @return       None
    def runTest(self):
        target_id_list = []
        include_inactive = False

        ##
        # Feature Enabling through IGCL
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if sharpness_helper.enable_disable_feature_igcl(self.sharpness_intensity, panel, self.filter_type,
                                                                self.feature_status) is False:
                    self.fail(f"FAIL: Sharpness feature is not {self.feature_status.name}d via IGCL".center(
                        MAX_LINE_WIDTH, "*"))
                logging.info(f"PASS: Sharpness feature is {self.feature_status.name}d via IGCL".center(
                    MAX_LINE_WIDTH, "*"))
                mode = self.display_config.get_current_mode(panel.target_id)
                self.hz_res, self.vt_res = mode.HzRes, mode.VtRes
                self.resolution = str(self.hz_res) + 'x' + str(self.vt_res)

        logging.info("Apply native mode with zero rotation to kick-in feature".center(MAX_LINE_WIDTH, "*"))
        ##
        # fetch the display configuration of all the displays connected
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if (panel.is_active and not include_inactive) or include_inactive:
                    target_id_list.append(panel.target_id)
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.display_config.get_all_supported_modes(target_id_list)
        for key, values in supported_modes.items():
            mode = values[0]
            mode.rotation = enum.ROTATE_0
            mode.VtRes = self.vt_res
            mode.HzRes = self.hz_res
            # Apply requested mode with zero rotation
            self.display_config.set_display_mode([mode], virtual_mode_set_aware=False, force_modeset=True)
            logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enables and Disables Sharpness for Manual testing")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
